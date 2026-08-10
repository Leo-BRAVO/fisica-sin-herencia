# Prerregistro 36 — Medir la VARA antes de volver a medir a Diego — 10 de agosto de 2026
**Estado: FIRMADO por el director el 10-ago-2026 ("adelante con todo").**
**Este prerregistro no mide a Diego. Mide el instrumento con el que íbamos a medirlo.**

## Por qué
El INFORME-40 cerró la segunda mitad del prereg-30 como **NO CONCLUYENTE POR INSTRUMENTO**:

| Semilla | Política contingente PLANTADA — razón sobre línea base | ¿alcanza el 1.5×? |
|---|---|---|
| 1 | 1.3420 | no |
| 2 | 1.1875 | no |
| 3 | **0.8449** | no |
| 4 | 1.9871 | **sí** |
| 5 | 1.6493 | **sí** |

La política contingente está **construida a propósito para tener la firma**. Solo la exhibió **2 de
5 veces**, y en la semilla 3 se movió **menos que su propia línea base** — conductualmente absurdo
para una política diseñada para moverse más donde hay efecto.

Diego tampoco la exhibió (0/5), que es lo que predije por escrito. **Pero esa ausencia no puede
certificarse con un instrumento que falla el 60% de las veces sobre un caso conocido.**

### El error de diseño que lo permitió, dicho con su nombre
El caso B1 del banco congelado probaba el control positivo con **una sola semilla** — la 2, que
resultó ser de las que funcionan a esa duración. **Un control positivo de una sola muestra no es un
control positivo: es una anécdota que aprueba.** Protegimos el falso positivo (caso B2: "si el
instrumento ve la firma donde no la hay, mide su propio ruido") y dejamos abierto el simétrico:
**que no la vea donde sí la hay**.

## Qué se construye (`codigo/espejo2.py`, función `calibrar`)
Un barrido de la **duración de fase** —400, 800, 1600, 3200 pasos— con **tres políticas** por celda
y 5 semillas cada una:

| Política | Qué es | Qué debe pasar |
|---|---|---|
| **contingente** | el control positivo plantado | dispara **5/5** |
| **ciega** | el balbuceo que Diego hace hoy | dispara **0/5** |
| **agitada** | **SEÑUELO NUEVO** — el mismo presupuesto finito de esfuerzo, repartido **al azar**, sin mirar el móvil | **nunca específica** |

**El señuelo agitado es la pieza que faltaba.** Se mueve más y de forma desigual, pero nada de eso
viene de la contingencia. Una vara que lo corone está midiendo **actividad**, no contingencia. Es
el análogo exacto del señuelo de ruido que salvó a la escalera de soporte del prereg-29 — y su
ausencia aquí es la misma clase de agujero que allí se tapó.

### La cifra que diagnostica
`dispersion_ciega` — la desviación de la razón entre semillas **con la política ciega**. Si la
dispersión de la línea base es del orden del efecto buscado (0.5 sobre 1.0), la vara **no puede**
ver ese efecto por mucho que insistamos, y alargar las fases sería tiempo tirado. Esa es la
sospecha que registro antes de correr; la medición dirá.

## Regla 31 declarada antes de correr (tres casos nuevos)
| Caso | Qué exige | Coste |
|---|---|---|
| **Veredicto de calibración** | con el positivo en 2/5 —exactamente lo que pasó— la vara **debe** declararse NO usable; con 5/5 debe recomendar esa duración | función pura, no simula nada |
| **Control positivo multi-semilla** | la tasa se mide sobre **varias** semillas y se registra cuál es. No se exige que sea 1.0: se exige **medirla**, que es justo lo que no se hizo | 3 semillas |
| **Señuelo agitado** | moverse más sin contingencia **no** puede ser coronado | 1 corrida |

El primero es el más importante y el más barato: **la lógica que falló, blindada.** El bug del
prereg-30 no estuvo en la física, estuvo en leer "una semilla pasó" como "el instrumento
funciona". Esa lectura ahora es imposible: está congelada en el banco como un caso que reprueba.

## Los dos desenlaces, y qué se hace con cada uno
- **Si alguna duración da 5/5 / 0/5 / señuelo rechazado:** se adopta **la más corta** que lo logre,
  y **recién entonces** se prerregistra volver a preguntarle a Diego por sus firmas.
- **Si NINGUNA lo logra:** se escribe como resultado que **las firmas conductuales no son medibles
  con este diseño**, y el prereg-30 B queda cerrado en no concluyente **de forma permanente** hasta
  que alguien proponga otro instrumento. No se vuelve a preguntar a Diego con una vara que no pasa
  su propio examen. Ese desenlace se acepta por escrito **antes** de conocerlo.

## Qué NO se autoriza
- **No se toca el criterio 1.5×**, ni la ganancia 0.6, ni la definición de especificidad. Mover el
  umbral hasta que el control positivo pase sería fabricar el resultado: la vara se declararía
  buena por construcción. Solo se mueve **la duración**, que es cuántas muestras se toman — no qué
  se considera una firma.
- **La política contingente sigue sin entrar al genoma.** Es control positivo del instrumento, como
  se firmó en el prereg-30.
- **Esto no reabre el agujero A.** El gemelo quedó conseguido 5/5 y es nodo del árbol (H-001).

## Firmado
Leo, director — 10-ago-2026, aprobación en conversación ("adelante con todo").
