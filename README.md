# Bandeja de publicación · ¿Y eso por qué? (@eso.porque)

Repositorio **público** y **temporal**: los vídeos pasan aquí unos minutos para que Metricool los copie a su servidor. Después se borran.

```
pendientes/<archivo>.mp4   ← vídeos listos para programar
cola.json                  ← metadatos de cada vídeo pendiente (título, descripción, etiquetas…)
publicados.json            ← registro de lo ya programado (fecha, id de Metricool)
herramientas/bandeja.py    ← estado · payloads · cerrar · limpiar
PUBLICAR.md                ← instrucciones para el chat que programa en Metricool
```

Formato de cada entrada de `cola.json`:
```json
{"archivo": "por_que_x", "titulo": "¿Por qué X? 🌈", "descripcion": "texto completo con hashtags",
 "etiquetas": ["...", "..."], "lista": "El mundo que nos rodea", "tipo": "short", "categoria": "EDUCATION", "madeForKids": false}
```
`tipo` es `short` para los reels y `video` para los vídeos largos 16:9.
`madeForKids` por defecto es `false` (si se omite el campo, `bandeja.py` ya lo pone en `false`).
Los `short` se programan siempre en YouTube **y** TikTok (mismo vídeo, mismo horario); los `video` solo en YouTube.
