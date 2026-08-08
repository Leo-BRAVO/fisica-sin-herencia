# INFORME 21 — El primer gen nuevo fracasa su examen… y en el fracaso deja dos lecciones y una foto reveladora — 8 de agosto de 2026

## Qué se hizo
Se construyó `curiosidad2.py` — el gen G2 del GENOMA-DIEGO: la ecuación del impulso (elegir el
estudio por PROGRESO DE COMPRESIÓN reciente, medido en bits, en vez de por "dónde estoy peor") —
y se corrió la Etapa A del prerregistro-18 (FIRMADO): el backtest sobre las dos decisiones
históricas de la curiosidad v1, reconstruidas usando solo la información anterior a cada decisión.

## Resultado en una frase
**FRACASO del criterio prerregistrado (0/2 decisiones lo cumplen) — se registra tal cual; la
autopsia muestra que la ecuación acertó en su promesa central (asignó interés CERO a las dos
regiones estériles que la v1 eligió) y que el criterio falló por dos defectos de mi implementación
que el propio backtest desenterró.**

## Los números (resultados/curiosidad2-backtest/reporte.json)
| Decisión de la v1 | Prioridad v2 de esa región | Ranking v2 en ese momento |
|---|---|---|
| reintento caída (deseo 1) | **0.000 bits** (última de 6) | mendeley 0.68 · dp-centroides 0.54 · zenodo 0.44 · … |
| reintento dp-centroides (deseo 2) | 0.539 bits (2ª) | mendeley 0.68 primera |

El criterio exigía además que la región fértil (dp-latentes) puntuara sobre la estéril elegida —
y puntuó 0.0 en ambas decisiones. Por eso: FRACASO formal.

## La autopsia (por qué la fértil dio cero y la estéril vieja dio 0.54)
1. **Contaminación del récord por mini-campañas internas:** el récord de dp-latentes lo fijó una
   corrida INTERNA del bucle interior (p14-inner-d4, 2 semillas, jueces internos — otra vara).
   Cuando p14-final llegó con la vara real, no "superó" ese récord manzanas-contra-naranjas y la
   región pareció estancada. Lección: **los récords de una región solo se comparan entre campañas
   con la misma clase de jueces; las corridas internas del bucle no puntúan récords.**
2. **El artefacto de la ventana escasa:** con solo 2 intentos históricos, la ventana de progreso
   retrocede hasta "cero conocimiento" y una región VIEJA y dormida (dp-centroides, cuyo récord
   era de la semana anterior) aparece como si acabara de progresar. Lección: **el progreso es por
   intentos RECIENTES, no por intentos a secas — sin noción de frescura, lo rancio parece nuevo.**

## La foto reveladora (lo que el fracaso no borra)
Reconstruidas las dos decisiones, la curiosidad v1 eligió LAS DOS VECES una región que la ecuación
ranquea en la mitad inferior — y en el deseo 1 eligió exactamente la última (caída, interés 0.000:
tres intentos sin un bit nuevo). Ambos deseos, sabemos hoy, fracasaron tal como la ecuación habría
anticipado con solo el pasado. La promesa central — *aburrirse donde el progreso murió* — quedó
fotografiada; lo que falló fue mi métrica de "dónde está naciendo", por las dos causas de arriba.

## Gobernanza (Regla 8, sin excepciones)
- El criterio NO se re-evalúa con arreglos post-hoc: FRACASO registrado.
- Las dos correcciones (excluir corridas internas de los récords; frescura temporal) son cambios
  de diseño → **prerregistro-18b en BORRADOR**, pendiente de firma del director. Solo entonces se
  re-corre el backtest, con el criterio nuevo firmado ANTES.
- Los casos del gen quedaron congelados en el banco (aburrimiento universal ante memoria plana;
  progreso positivo ante récord que mejora): 26/26 OK.

## Qué decide el director
1. Firmar (o corregir) el prerregistro-18b cuando lo lea.
2. Sigue pendiente lo de siempre: las 5 corridas encoladas en su máquina (la cuarentena de
   E2-N-004 espera) y la fusión de esta rama a main para que la tarea horaria vea la cola nueva.
