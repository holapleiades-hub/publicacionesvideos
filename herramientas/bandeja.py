#!/usr/bin/env python3
"""Bandeja de publicación de ¿Y eso por qué? (repositorio PÚBLICO holapleiades-hub/publicacionesvideos).

  python3 herramientas/bandeja.py estado
      → lista lo pendiente (cola.json) y lo ya publicado.
  python3 herramientas/bandeja.py payloads --desde AAAA-MM-DD [--horas 10:00,16:00] [--ocupadas "AAAA-MM-DDTHH:MM,..."]
      → escribe payloads.json con un post de Metricool por cada vídeo pendiente, en huecos libres
        (por defecto 2 al día, 10:00 y 16:00, hora de Madrid) a partir de esa fecha, saltando las ocupadas.
        Los "short" generan SIEMPRE dos entradas (youtube + tiktok, mismo slot); los "video" solo youtube.
  python3 herramientas/bandeja.py revisar
      → check de razón de publicación: marca como BLOQUEADO todo vídeo que dependa de otro (vídeo largo, parte 2...)
        que aún no esté publicado de verdad. `payloads` salta los bloqueados.
  python3 herramientas/bandeja.py cerrar <archivo> <fecha> youtube=<id>,<uuid> [tiktok=<id>,<uuid>]
      → saca el vídeo de la cola, lo apunta en publicados.json (con el id/uuid de cada red) y borra el mp4 de pendientes/.
  python3 herramientas/bandeja.py limpiar
      → reescribe la historia (un único commit) para que los mp4 ya borrados no ocupen sitio. Hace push -f.
"""
import json, os, re, sys, subprocess, datetime as dt
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = 'https://raw.githubusercontent.com/holapleiades-hub/publicacionesvideos/main/pendientes/'
cola_p, pub_p = os.path.join(R, 'cola.json'), os.path.join(R, 'publicados.json')
load = lambda p: json.load(open(p)) if os.path.exists(p) else []
save = lambda p, d: json.dump(d, open(p, 'w'), ensure_ascii=False, indent=1)
git = lambda *a: subprocess.run(['git', '-C', R, *a], check=True)

def estado():
    c, p = load(cola_p), load(pub_p)
    print(f'PENDIENTES ({len(c)}):')
    for x in c: print('  -', x['archivo'], '|', x['titulo'], '| existe mp4:', os.path.exists(os.path.join(R, 'pendientes', x['archivo'] + '.mp4')), '| BLOQUEADO: ' + bloqueado(x) if bloqueado(x) else '')
    print(f'PUBLICADOS/PROGRAMADOS ({len(p)}): últimos 5')
    for x in p[-5:]: print('  -', x['fecha'], x['archivo'])

REMITE = re.compile(r'v[ií]deo (largo|completo|entero)|parte (2|dos)|siguiente parte|pr[oó]ximo v[ií]deo largo|en el canal', re.I)

def publicado_de_verdad(archivo):
    """True solo si el vídeo está en publicados.json, SIN 'estado' (borrador/en espera) y con fecha ya pasada."""
    from zoneinfo import ZoneInfo
    for p in load(pub_p):
        if p['archivo'] == archivo:
            if p.get('estado'): return False
            f = dt.datetime.fromisoformat(p['fecha'])
            if f.tzinfo is None: f = f.replace(tzinfo=ZoneInfo('Europe/Madrid'))
            return f <= dt.datetime.now(ZoneInfo('Europe/Madrid'))
    return False

def bloqueado(x):
    """Motivo por el que NO se puede programar este vídeo, o None. Un reel nunca sale 'porque sí'."""
    d = x.get('depende_de')
    if d and not publicado_de_verdad(d):
        return f'depende de "{d}", que NO está publicado (borrador, programado o inexistente)'
    if not d and REMITE.search(x.get('descripcion', '')) and not x.get('sin_dependencia'):
        return 'su texto remite a otro vídeo (largo/completo/parte 2) pero no declara depende_de: revísalo con el usuario'
    return None

def revisar():
    c = load(cola_p); mal = 0
    for x in c:
        m = bloqueado(x)
        print(('BLOQUEADO ' if m else 'OK        ') + x['archivo'] + (' → ' + m if m else '')); mal += bool(m)
    print(f'{mal} bloqueados de {len(c)}')

def slots(desde, horas, ocupadas):
    d = dt.date.fromisoformat(desde)
    while True:
        for h in horas:
            s = f'{d.isoformat()}T{h}'
            if s not in ocupadas: yield s
        d += dt.timedelta(days=1)

def payloads(desde, horas, ocupadas):
    from zoneinfo import ZoneInfo
    c = load(cola_p); out = []; g = slots(desde, horas, ocupadas)
    for x in c:
        m = bloqueado(x)
        if m:
            print('BLOQUEADO (no se programa):', x['archivo'], '→', m); continue
        slot = next(g)
        off = dt.datetime.fromisoformat(slot).replace(tzinfo=ZoneInfo('Europe/Madrid')).strftime('%z')
        date = f"{slot}:00{off[:3]}:{off[3:]}"
        media = [RAW + x['archivo'] + '.mp4']
        base_text = x['descripcion']
        tipo = x.get('tipo', 'short')
        yt_info = {"autoPublish": True, "descendants": [], "draft": False, "firstCommentText": "", "hasNotReadNotes": False,
                "media": media, "mediaAltText": [], "providers": [{"network": "youtube"}],
                "publicationDate": {"dateTime": slot + ':00', "timezone": "Europe/Madrid"}, "shortener": False, "smartLinkData": {"ids": []},
                "text": base_text,
                "youtubeData": {"title": x['titulo'], "type": tipo, "privacy": "public", "tags": x['etiquetas'],
                                "category": x.get('categoria', 'EDUCATION'), "madeForKids": x.get('madeForKids', False), "isAiGeneratedContent": False}}
        out.append({"archivo": x['archivo'], "red": "youtube", "date": date, "info": json.dumps(yt_info, ensure_ascii=False)})
        if tipo == 'short':
            # Mismo vídeo, mismo slot, texto adaptado a la convención ya usada en el canal (CTA y hashtag de TikTok).
            tt_text = base_text.replace('¡Suscríbete para no perderte la próxima pregunta!',
                                         '¡Síguenos para no perderte la próxima pregunta!').replace('#shorts', '#aprendeentiktok')
            tt_info = {"autoPublish": True, "descendants": [], "draft": False, "firstCommentText": "", "hasNotReadNotes": False,
                    "media": media, "mediaAltText": [], "providers": [{"network": "tiktok"}],
                    "publicationDate": {"dateTime": slot + ':00', "timezone": "Europe/Madrid"}, "shortener": False, "smartLinkData": {"ids": []},
                    "text": tt_text,
                    "tiktokData": {"privacyOption": "PUBLIC_TO_EVERYONE", "title": x['titulo'], "photoCoverIndex": 0}}
            out.append({"archivo": x['archivo'], "red": "tiktok", "date": date, "info": json.dumps(tt_info, ensure_ascii=False)})
    save(os.path.join(R, 'payloads.json'), out)
    for o in out: print(o['date'], o['red'], o['archivo'])
    print('→ payloads.json (no se sube al repo)')

def cerrar(archivo, fecha, *redes):
    c = load(cola_p); p = load(pub_p)
    x = next(v for v in c if v['archivo'] == archivo)
    c = [v for v in c if v['archivo'] != archivo]
    entry = {"archivo": archivo, "titulo": x['titulo'], "fecha": fecha}
    for r in redes:
        red, ids = r.split('=')
        mid, uuid = ids.split(',')
        entry[red] = {"metricool_id": mid, "uuid": uuid}
    p.append(entry)
    save(cola_p, c); save(pub_p, p)
    f = os.path.join(R, 'pendientes', archivo + '.mp4')
    if os.path.exists(f): os.remove(f)
    print('cerrado', archivo)

def limpiar():
    git('checkout', '-q', '--orphan', '_tmp'); git('add', '-A')
    subprocess.run(['git', '-C', R, '-c', 'user.name=Claude', '-c', 'user.email=noreply@anthropic.com', 'commit', '-qm', 'Bandeja: estado actual'], check=True)
    subprocess.run(['git', '-C', R, 'branch', '-D', 'main'], check=False)
    git('branch', '-m', 'main'); git('push', '-f', 'origin', 'main')
    print('historia limpia')

if __name__ == '__main__':
    a = sys.argv[1:]
    if not a or a[0] == 'estado': estado()
    elif a[0] == 'payloads':
        desde = a[a.index('--desde') + 1]
        horas = a[a.index('--horas') + 1].split(',') if '--horas' in a else ['10:00', '16:00']
        ocup = set(a[a.index('--ocupadas') + 1].split(',')) if '--ocupadas' in a else set()
        payloads(desde, horas, ocup)
    elif a[0] == 'revisar': revisar()
    elif a[0] == 'cerrar': cerrar(a[1], a[2], *a[3:])
    elif a[0] == 'limpiar': limpiar()
    else: print(__doc__)
