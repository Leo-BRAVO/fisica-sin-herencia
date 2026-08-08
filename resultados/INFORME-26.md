# INFORME 26 — La dimensión intrínseca de los tres mundos, y un item que llevaba horas atascado en silencio — 8 de agosto de 2026

## Lo que se midió (cierra la deuda de dimensión: 3/3)
La primera pregunta que el método debía hacerle a todo sistema nuevo —¿cuántas variables esconde
esto?— ya está respondida en los tres mundos del proyecto (`dimension.py`, TwoNN + participación PCA):

| Mundo | Columnas disponibles | TwoNN (dimensión intrínseca) | Lectura |
|---|---|---|---|
| Michigan (ángulos) | 4 | **~2.5 – 3.1** | el sistema vive en un subespacio: hay redundancia, la representación sobra un poco |
| Caída (píxeles centrados) | 4 | **~2.3** | dinámica de baja dimensión, como corresponde a un cuerpo que cae |
| **Latentes p14 (los ojos de Diego)** | 8 | **~6.2** | el conjunto visitado casi LLENA su espacio |

## La observación que abre pregunta (no la cierra)
El péndulo doble tiene 4 grados de libertad reales. Los ángulos de Michigan dan ~3 (por debajo,
como se espera de un estimador con ruido). Pero los latentes de Diego dan **~6.2 de 8** — es decir,
su espacio de estados apenas se comprime. Interpretación cautelosa y declarada como hipótesis:
**sus ojos podrían estar codificando bastante más que la dinámica del péndulo** (textura, deriva de
apariencia, ruido de compresión del video), que llenaría dimensiones sin ser física.
- **Reserva honesta:** TwoNN sobre ~2.000 puntos con ruido tiende a sobreestimar, y la comparación
  entre espacios de distinta naturaleza (ángulos vs latentes) no es limpia. Esto es un DIAGNÓSTICO
  que motiva un experimento, no un veredicto. No se toca ningún nodo con esto.
- **Conecta con el INFORME-25:** si buena parte del latente es textura suave y no dinámica, se
  entiende que su predictibilidad viva en el espectro — y refuerza que el nulo por barajado
  (ya encolado) es el que debe dictar sentencia.

## El hallazgo de gobernanza (por qué esto no había corrido solo)
El item `aud01-dimension-tres-mundos` llevaba horas **atascado sin que nada avisara**: tenía tipo
`re-analisis-herramienta` (el latido solo toma `re-analisis`) y una ruta imposible
(`"datos/procesados/dp_morpheus + caida + mendeley_epoca2"` — tres carpetas en un campo de una).
El latido lo saltaba en silencio, corrida tras corrida.
**Regla operativa nueva:** todo item de la cola debe ser ejecutable por sí solo — un mundo, una
ruta real, un tipo que el latido tome. Un item que nadie puede ejecutar es una tarea que parece
pendiente y nunca lo estará. `coherencia.py` gana el caso que lo vigila.
