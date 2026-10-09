# Análisis 2026-10-04 — estado de la cola, estadísticas y cambios aplicados

Fuente de datos: Metricool (marca 7108507, Europe/Madrid). Sustituye al análisis del 27-09 en lo que respecta al estado de la cola.

## 1. Qué pasó con el hueco de hoy
- El registro `publicados.json` y el cálculo de slots estaban desfasados respecto a Metricool: fechas 1–2 días corridas en las primeras 30 entradas y dos compilaciones ("5_misterios_de_tu_cuerpo", "5_preguntas_rarisimas_de_tu_cuerpo_2") que ya no existen en Metricool ni en el canal, pero seguían ocupando slots.
- Resultado: huecos en el calendario real y hoy 16:00 vacío; el short del mar salado se publicó a mano el 04-10 10:45 y se comió el slot de mañana 10:00.

## 2. Cambios aplicados hoy
1. **Cola adelantada dos slots**: hoy 16:00 sale "lucecitas" (YT+TikTok, IG a las 19:00). Sin huecos desde hoy hasta el final.
2. **Recomendación 2 — TikTok para los 10 shorts que no lo tenían**: arcoíris, Luna, estrellas parpadean, trueno, barco, Tierra (no caemos), pompas, hojas, gatos, flamencos. Ahora los 35 shorts publicados/programados tienen YouTube + TikTok.
3. **Instagram**: reels programados en los 4 primeros vídeos de la cola (lucecitas, arcoíris, Luna, estrellas) además de los 3 ya publicados. IG va en serio; la audiencia baja (~170 vistas/reel, 0 likes) es sobre todo por haber publicado poco.
4. **Vídeo largo del dinosaurio** (`has_bebido_agua_de_dinosaurio`) pasado a **borrador**: no se publica hasta que se decida. El short del dinosaurio sí sale (10-10 16:00).
5. **Registro sincronizado** con Metricool (fechas reales, ids y uuid de YT/TikTok/IG) y eliminadas las dos entradas fantasma. `PUBLICAR.md` actualizado: la fuente de verdad es Metricool, convención de Instagram y nota del vídeo largo.

## 3. Calendario actual (YouTube; TikTok mismo slot; IG +2h/+3h donde hay reel)
| Día | 10:00 | 16:00 |
|---|---|---|
| 04-10 | (publicado) mar salado | lucecitas |
| 05-10 | arcoíris | Luna |
| 06-10 | estrellas parpadean | trueno |
| 07-10 | barco | Tierra (no caemos) |
| 08-10 | pompas | hojas |
| 09-10 | gatos | flamencos |
| 10-10 | búhos | dinosaurio (short) |
| 11-10 | océanos | agua de la Tierra |
| 12-10 | nube con patas | estrellas fugaces |
| 13-10 | tierra mojada | — (fin de la cola) |

**Autonomía: hasta el 13-10 a las 10:00 (18 slots). Hace falta reponer stock.**

## 4. Estadísticas (Metricool)
- YouTube shorts: media ~1.170 vistas/short (rango 1.057–1.519; "pierna" 546), ~2,0 % de likes sobre vistas, 7 comentarios en total.
- Suscriptores: 57 ganados (~0,38 % de las vistas); el contador del canal (15.007 vistas) va por detrás de la suma por vídeo (18.764).
- TikTok: media ~264 vistas/short (cebolla 887). Siete posts tempranos figuran con 0 vistas: puede ser falta de sincronización de datos, no necesariamente cero real.
- Instagram: ~170 vistas/reel, 0 likes (muestra de 3 reels).
- Mejores horas (Metricool): 10:00 y 16:00 son los picos locales entre semana; fin de semana ~la mitad de actividad.

## 5. Cautelas
- Muestras pequeñas (3 reels de IG, 7 comentarios): no sacar conclusiones fuertes aún.
- Datos de TikTok incompletos en los primeros posts.
- Varios shorts (dinosaurio, agua de la Tierra y posiblemente alguno más) mencionan en su texto "vídeo largo"; con el largo en borrador esos textos apuntan a algo que no existe. Pendiente de decidir: editar textos o publicar el largo antes.

## 6. Pendientes / siguientes pasos
- Crear más vídeos (el usuario lo hará) y programarlos con `PUBLICAR.md`.
- El usuario probará el nuevo CTA; comparar vistas/likes/suscriptores antes y después en unas 2 semanas.
- Añadir reels de IG al resto de shorts programados (ahora solo los 4 primeros) y mantener la constancia diaria.
