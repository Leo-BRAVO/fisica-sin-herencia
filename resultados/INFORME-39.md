# INFORME-39 — ACTA DEL PRERREGISTRO 29: la escalera de soporte **CONSEGUIDA 5/5, CON UNA SALVEDAD QUE VALE MÁS QUE EL 5/5**
**10 de agosto de 2026.** Corrida oficial completa: 5 semillas, las tres guardianas verdes en cada
una, commiteadas en `main` (`75cea55`, `e65c15c`, `9ad0d12`, `e272ecd`, `1d964b9`).

Esta acta declara el criterio prerregistrado **cumplido**, y a continuación explica por qué el
número **5/5 promete más independencia de la que realmente hay**. Lo segundo no es una nota al
pie: es el hallazgo principal del acta.

---

## 1. EL CRITERIO, TAL COMO SE FIRMÓ
> **CONSEGUIDO** si en ≥4/5 semillas: escalón 1 declara `altura` (o `vel_z`) como único apto,
> escalón 2 supera su nulo, y ambos exámenes VOE dan sorpresa > 0.05 con nulo natural < 0.05.

## 2. LA TABLA COMPLETA

| Semilla | E1: único apto | autopredictible | obediencia neta | E2: efecto vs nulo | VOE flota | VOE atraviesa | Nulo aire | Nulo mesa |
|---|---|---|---|---|---|---|---|---|
| 1 | `altura` | 0.5403 | 0.0000 | 2.544 vs 0.1397 | +0.9999 | **+0.0948** | +0.0283 | −0.0221 |
| 2 | `altura` | 0.5403 | 0.0000 | 2.544 vs 0.1397 | +0.9999 | **+0.1756** | −0.0125 | +0.0007 |
| 3 | `altura` | 0.5403 | 0.0000 | 2.544 vs 0.1397 | +0.9999 | **+0.1951** | −0.0256 | +0.0238 |
| 4 | `altura` | 0.5403 | 0.0000 | 2.544 vs 0.1397 | +0.9999 | **+0.1285** | −0.0290 | −0.0311 |
| 5 | `altura` | 0.5403 | 0.0000 | 2.544 vs 0.1397 | +0.9999 | **+0.1342** | −0.0234 | +0.0022 |

**Cinco de cinco en las tres condiciones.** Ningún nulo natural se acercó al techo de 0.05 (el
mayor, +0.0283); ninguna sorpresa se quedó cerca del piso de 0.05 (la menor, +0.0948, casi el
doble).

### El escalón 1, canal por canal — lo que sí varió
En las cinco semillas los tres canales del brazo fueron **rechazados por míos**, y sus cifras
**sí cambian de semilla a semilla** porque el balbuceo cambia:

| Semilla | art0 | art1 | art2 | ruido (señuelo) |
|---|---|---|---|---|
| 1 | 0.0735 | 0.0841 | 0.7032 | rechazado por **ilegal** |
| 2 | 0.0571 | 0.0806 | 0.6913 | rechazado por **ilegal** |
| 3 | 0.1167 | 0.1416 | 0.8204 | rechazado por **ilegal** |
| 4 | 0.1164 | 0.1070 | 0.7519 | rechazado por **ilegal** |
| 5 | 0.0998 | 0.0708 | 0.7391 | rechazado por **ilegal** |

El señuelo de ruido —el canal que **tampoco obedece** y que hundía al nivel B viejo— fue
rechazado en las cinco por autopredictibilidad 0.0035, muy por debajo del piso 0.30. Esa parte
del experimento **sí replicó cinco veces de verdad**: cinco balbuceos distintos, cinco rechazos.

---

## 3. LA SALVEDAD: CINCO MEDICIONES NO SON CINCO RÉPLICAS

Mírese la tabla de §2 en vertical. En el escalón 1, `autopredictible` es **0.5403 en las cinco**.
En el escalón 2, el efecto es **2.544 y el nulo 0.1397 en las cinco**. No aproximadamente: idéntico
hasta el último dígito.

**Eso no es una coincidencia notable: es una consecuencia del diseño.** La semilla gobierna el
balbuceo del brazo, y **el brazo nunca toca al objeto que cae**. La caída es la misma caída, desde
la misma altura, con la misma masa, en las cinco corridas. Estamos midiendo **una sola realización
del fenómeno, cinco veces**.

Lo que eso significa, sin suavizar:
- **La parte que replica de verdad** es el rechazo: cinco cuerpos distintos, y en los cinco el
  criterio supo decir "esto soy yo, esto no". Eso es una réplica legítima y es lo que el prereg-29
  existía para arreglar del nivel B.
- **La parte que NO replica** es la aceptación: que `altura` sea legal y no-mía se comprobó una
  vez y se contó cinco. Un número que aparece idéntico cinco veces no ha sido sometido a prueba
  cinco veces.
- **El examen VOE sí varía** (0.0948 a 0.1951, y los nulos naturales cambian de signo), porque el
  predictor se entrena sobre trayectorias que sí dependen de la semilla. Ese escalón está mejor
  sostenido que los otros dos.

**Nadie nos señaló esto.** Salió de leer la propia tabla en vertical, que es exactamente la
disciplina que el proyecto dice tener. Queda escrito aquí antes de que sirva de argumento a nadie.

---

## 4. LO QUE SE AFIRMA Y LO QUE NO

**Se afirma:** en el Gimnasio, con el `DISENO` congelado, Diego distingue lo posible de lo
imposible en física de soporte —flotar sin apoyo y atravesar una mesa sólida le sorprenden por
encima de su propio nulo natural— y el canal que gobierna esa física queda correctamente
clasificado como **no-mío y legal**, mientras sus propias articulaciones y un señuelo de ruido
quedan fuera.

**No se afirma:**
- que esto sea física del universo — es PyBullet haciendo de mundo; el nodo sería
  `sobre-el-simulador`;
- que Diego "entienda la gravedad";
- **que el escalón 1 y el escalón 2 estén replicados en cinco condiciones independientes.** No lo
  están. Están medidos cinco veces sobre una condición.

## 5. PROPUESTA AL DIRECTOR (Regla 15 — yo propongo, usted decide)

**Propongo NO escribir todavía el nodo del árbol.** El criterio prerregistrado se cumplió y así
queda registrado; pero un nodo es memoria permanente de Diego, y prefiero que nazca de cinco
caídas distintas y no de una repetida cinco veces.

**Segunda ronda propuesta (necesita su firma y su propio prerregistro):** que la semilla mueva
también la caída — altura inicial, masa del objeto, posición de soltada, y posición de la mesa —
de modo que las cinco semillas sean cinco mundos y no cinco miradas al mismo. La predicción que
comprometo por escrito, antes de correrla: **espero que replique igual**, porque el señuelo de
ruido ya demostró que el criterio discrimina por la razón correcta. Si no replicara, este acta se
habría escrito a tiempo.

## 6. TRAZA
- Prerregistro: `registros/prerregistro-29.md` (firmado 9-ago-2026, umbrales congelados allí).
- Código: `codigo/soporte.py`. Banco: 7/7 casos de Regla 31, congelados.
- Datos crudos: `resultados/p29-soporte-s{1..5}/resumen.json`.
- Cotejo cruzado con el prereg-32: los cinco valores de `atraviesa` de esta acta reaparecen
  **idénticos** en la condición `pasivo-propio` del INFORME-41, corrida por otro módulo y en otro
  día. Dos caminos independientes, el mismo número.
