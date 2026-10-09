# Cómo programar lo pendiente en Metricool

Datos fijos: marca de Metricool **blogId 7108507**, zona horaria **Europe/Madrid**, canal ¿Y eso por qué?.
Redes: **siempre YouTube + TikTok para los "short"** (mismo vídeo, mismo slot); los "video" (16:9 largos) van **solo a YouTube**.
Ritmo: **2 publicaciones al día, 10:00 y 16:00**, sin huecos, a continuación de la última ya programada (un slot por vídeo, no por red).
**La fuente de verdad es Metricool, no `publicados.json`**: los huecos se calculan siempre con `getScheduledPosts` (solo posts de YouTube, incluidos los ya publicados de hoy), nunca con el registro (se desfasó en septiembre).
**Instagram (reels)**: cuando haya reel, mismo día que el short, a las 12:00 (si YouTube es 10:00) o 19:00 (si es 16:00); `instagramData {autoPublish: true, type: REEL, showReelOnFeed: true, isAiGenerated: false}` y caption propio.
**Vídeo largo del dinosaurio** (`has_bebido_agua_de_dinosaurio`, tipo "video"): en Metricool está como **borrador**; NO publicar hasta que el usuario lo diga.

1. `python3 herramientas/bandeja.py estado` → si no hay pendientes, avisa y termina.
2. Comprueba que cada mp4 pendiente es accesible:
   `curl -s -o /dev/null -w "%{http_code}\n" https://raw.githubusercontent.com/holapleiades-hub/publicacionesvideos/main/pendientes/<archivo>.mp4` → tiene que dar 200.
3. Mira lo programado en Metricool con `getScheduledPosts` (blogId 7108507, timezone Europe/Madrid, desde hoy hasta +45 días; si el rango da error de tamaño, consúltalo en ventanas más cortas).
   Anota la última fecha programada y las horas ya ocupadas (mira solo `providers[].network == "youtube"` para calcular huecos: es la red que marca el ritmo).
4. `python3 herramientas/bandeja.py payloads --desde <día siguiente al último programado, o mañana> --ocupadas "<fechas ocupadas AAAA-MM-DDTHH:MM separadas por comas>"`
   → crea `payloads.json` con `date`, `red` e `info` ya listos para cada vídeo (dos entradas -youtube y tiktok- por cada "short", una sola por cada "video").
5. Para cada entrada de `payloads.json`, EN ORDEN (primero youtube, luego tiktok del mismo archivo): llama a `createScheduledPost` con `blogId: "7108507"`, `date` y `info` **tal cual** (no reescribas textos).
   Comprueba en la respuesta que `media[0]` empieza por `https://static.metricool.com/` (= Metricool ya tiene su copia) y que el estado es PENDING.
   Para el payload de tiktok, sustituye `media` en el `info` por el `media[0]` (static.metricool.com) que te devolvió el createScheduledPost de youtube del mismo archivo, en vez de subir otra vez el mp4 desde GitHub.
   Si falla uno, NO lo cierres: sigue con los demás y avisa al final.
6. Por cada archivo con (al menos) su post de youtube creado bien:
   `python3 herramientas/bandeja.py cerrar <archivo> <date> youtube=<id>,<uuid> [tiktok=<id>,<uuid>]` (omite `tiktok=...` si ese post falló o no aplica).
7. `git add -A && git commit -m "Programados" && git push`, y luego `python3 herramientas/bandeja.py limpiar` (borra los mp4 de la historia).
8. Responde con una tabla corta: día · hora · título · redes (YT/TikTok), y el enlace del calendario https://app.metricool.com/planner/calendar?blogId=7108507

Reglas: no publiques nada que no esté en `cola.json`; no cambies títulos, descripciones ni etiquetas (solo el CTA/hashtag final de TikTok, según la convención ya usada: "Síguenos" + #aprendeentiktok en vez de "Suscríbete" + #shorts); no borres ni muevas posts ya programados salvo que el usuario lo pida.
