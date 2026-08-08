# Prerregistro 22 — Los ojos que se ganan su dimensión, con la varianza medida — 8 de agosto de 2026
**Estado: BORRADOR pendiente de firma del director. Rehace el prerregistro-21 con el diseño que la evidencia del 21 exigió. Se corre cuando el latido termine los nulos por barajado (no antes: una sola casa para el cómputo).**

## Por qué se rehace (lo que el 21 enseñó, medido)
1. **El 21 tenía una BANDA DESCUBIERTA** (0.05–0.10) y el resultado cayó justo ahí → INCONCLUSO.
   Aquí el criterio no tiene huecos.
2. **La varianza tiene DOS fuentes y solo medimos una.** Medido el 8-ago con 8 sorteos por
   dimensión: la dispersión por **sorteo de surrogado** es pequeña (**±0.010–0.015**), pero el
   valor de d=6 (−0.085) solo se explica por la otra fuente: **la semilla de entrenamiento**.
   Con una sola semilla por candidata, un mal entrenamiento se disfraza de veredicto.
3. **Reportar un solo sorteo es elegir el que salió:** el +0.0964 que se reportó para d=2 era el
   MÁXIMO de su rango; su media real es **+0.0770**. El instrumento ya fue corregido para
   promediar N surrogados y reportar su desviación (congelado en el banco).

## Lo que la evidencia YA sostiene (y no hace falta re-descubrir)
Con 8 surrogados por dimensión, sobre los ojos ya entrenados del 21:
| d | ganancia honesta | desviación |
|---|---|---|
| 2 | +0.0770 | ±0.0152 |
| 4 *(ojos actuales de Diego)* | **+0.0089** | ±0.0069 |
| 8 | +0.0800 | ±0.0102 |
**d=4 está separada de d=2 y d=8 por ~5 desviaciones.** Que los ojos actuales tengan ganancia
honesta casi nula es robusto. Lo que NO está resuelto es cuál dimensión gana: d=2 y d=8 empatan
dentro del error, y esa es exactamente la pregunta del 22.

## Diseño
- **Candidatas:** d ∈ {2, 3, 4, 6, 8}. **5 semillas de entrenamiento por candidata** (25 ojos).
- **Medición:** ganancia honesta con **8 surrogados** por ojo → cada candidata trae media y
  desviación **entre semillas** (la fuente dominante) y **entre surrogados** (la menor).
- **Jueces:** 3/6/9 congelados, invisibles a todo el proceso — como siempre.
- **Sonda:** rival lineal (no gasta el motor simbólico). El veredicto simbólico lo da después la
  campaña completa, solo para la ganadora.

## Criterio SIN HUECOS (las tres zonas cubren todo el eje, fijadas antes de correr)
Sea `g*` la mejor media y `σ*` su desviación entre semillas:
- **GANA una dimensión** si `g* − σ* > 0.05` **Y** supera a la segunda por más de la suma de sus
  desviaciones (separación real, no ruido). → esa d es la representación legítima; corre campaña.
- **EMPATE TÉCNICO** si `g* − σ* > 0.05` pero no se separa de la segunda → se declara empate, se
  elige la **más simple** (menor d) por parsimonia, y se registra que la elección fue por navaja
  y no por evidencia.
- **NINGUNA SIRVE** si `g* − σ* ≤ 0.05` → ninguna representación de este aparato captura dinámica
  más allá de la textura; **la certificación predictiva de N-002-E2 y N-003-E2 se degrada
  formalmente a estructural** y se registra sin maquillaje.

## Predicción comprometida
Por lo ya medido, espero **empate técnico entre d=2 y d=8** con d=4 claramente por debajo. Si eso
se confirma, la lectura es incómoda y honesta: **la ganancia honesta de este aparato no depende
monótonamente de la dimensión**, y habría que buscar la causa en otro sitio (fps, pérdida, o el
límite del propio autoencoder) antes de declarar ninguna representación buena.

## Coste y ejecución
25 entrenamientos × ~4 min ≈ 2 h. Se ejecuta **en la nube por el latido**, como item de cola con
su reconstrucción declarada — no a mano, para que quede cronometrado por G10 y auditado por los
tres guardianes.

- **Firmado:** PENDIENTE — Leo, director.
