# Primer análisis: impacto de quitar "No, made for kids" · ¿Y eso por qué?

Fecha del análisis: 2026-09-27 (canal creado 2026-09-25, 2 días antes)

## Qué pasó

Los 4 vídeos publicados hasta ahora salieron marcados como **"hecho para niños"** (`madeForKids: true`), la opción por defecto de YouTube cuando no se indica lo contrario. Con esa etiqueta activada, YouTube desactiva para ese vídeo:

- Recomendaciones personalizadas (el algoritmo de Shorts deja de empujarlo a usuarios según sus intereses).
- Notificaciones a suscriptores.
- Comentarios.
- Anuncios personalizados.

El 27/09, con el canal prácticamente sin tracción, se quitó manualmente la etiqueta en YouTube (`madeForKids: false`) en los 4 vídeos ya publicados, y se cambió el valor por defecto en `bandeja.py`/`cola.json` para que todo lo nuevo se programe ya sin ella.

## Datos: antes vs. ahora

| Métrica | Antes (con made-for-kids) | Ahora (sin made-for-kids), mismo día | 
|---|---|---|
| Suscriptores | 0 | 4 |
| Vistas totales (agregado canal) | ~10 | 10 (el agregado del canal tarda en actualizarse; ver detalle por vídeo abajo) |

Detalle por vídeo (vistas, snapshot más reciente vía scraping de YouTube):

| Vídeo | Publicado | Vistas |
|---|---|---|
| ¿Por qué se te duerme la pierna? | 2026-09-27 10:00 | 42 |
| ¿Por qué duele la cabeza al comer helado? | 2026-09-27 16:00 | 644 |
| ¿Por qué se arrugan los dedos en el agua? | 2026-10-03* | 415 |
| ¡No bosteces! ¿Por qué bostezamos? | 2026-09-26 23:56 | 56 |
| **Total** | | **1.157** |

\* Este vídeo aparece programado más adelante en `publicados.json`; su presencia ya publicada en YouTube indica que se subió/gestionó también por fuera de este flujo de Metricool en algún momento — coherente con los duplicados que detectaste y borraste tú mismo durante esta sesión. Queda anotado como punto a vigilar (ver "Cosas a vigilar" abajo).

La suma de vistas por vídeo (1.157) es ya muy superior a las ~10 vistas que mostraba el agregado del canal antes del cambio; el contador agregado del canal tarda en refrescar y no es el dato más fiable a corto plazo, así que la lectura correcta es la suma por vídeo.

## Lectura causal

La coincidencia temporal es directa: en las horas siguientes a quitar `madeForKids` en los 4 vídeos ya publicados, el canal pasó de prácticamente cero tracción a las cifras de arriba, y ganó sus primeros 4 suscriptores. Mecanismo plausible y bien documentado: un Short marcado "para niños" queda fuera del circuito de recomendación personalizada de Shorts, que es la principal fuente de descubrimiento para un canal nuevo sin audiencia propia. Quitar la etiqueta reactiva ese circuito.

**Nivel de confianza: alto, pero no es una prueba controlada.** Es un solo cambio, en un solo canal, con pocas horas de datos, así que no se puede aislar al 100% de otros factores (por ejemplo, que varios Shorts llevaban ya 24-48h publicados y podían estar entrando en su ventana normal de arranque del algoritmo). Dicho esto, el salto es demasiado grande y demasiado inmediato para explicarlo solo por eso, y encaja con el comportamiento conocido de la etiqueta. Si el ritmo de vistas se mantiene o crece en las próximas 24-48h (con los próximos vídeos ya naciendo sin la etiqueta), quedaría prácticamente confirmado.

## Cosas a vigilar

1. **Duplicados**: ya se han detectado y borrado vídeos duplicados publicados fuera de este flujo (ver el vídeo de "dedos arrugados" arriba). Antes de cada tanda de programación, conviene contrastar `publicados.json` contra el listado real del canal en YouTube (vía TubeAlfred) para detectar publicaciones manuales que no pasaron por Metricool/`bandeja.py`.
2. **madeForKids en nuevas publicaciones**: ya queda en `false` por defecto en `cola.json`/`bandeja.py` (ver README). Confirmar periódicamente que ningún vídeo nuevo se cuela con el valor por defecto de YouTube (`true`) si se sube por fuera de este flujo.
3. **Repetir el chequeo en 24-48h**: comparar vistas/suscriptores para confirmar que la tendencia se sostiene y no es solo el pico inicial de publicar 4 vídeos casi seguidos.
