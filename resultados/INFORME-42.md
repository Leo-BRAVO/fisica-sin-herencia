# INFORME-42 — ACTA DEL PRERREGISTRO 35 (escalera): réplica real en cinco mundos, y **PARCIAL por la cláusula "único apto"**
**10 de agosto de 2026.** Corrida oficial completa: 5 semillas, las tres guardianas verdes en cada
una, commiteadas en `main` (`a5c70b3`, `6755c15`, `228f333`, `86d3af1`, `ac7eadd`).

Esta es la ronda que el INFORME-39 pidió: **la caída ya no es una sola caída medida cinco veces.**
Cada semilla tiene su propia mesa, su propia altura de soltada, su propia masa y su propia
posición. Todos los números cambian. Y el criterio firmado **no se cumple del todo**.

---

## 1. LA TABLA COMPLETA

| s | mesa / suelta / masa / x | E1 aptos | autopred. de `altura` | E2 efecto vs nulo | VOE flota | VOE atraviesa | nulo aire | nulo mesa |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.507 / 1.157 / 0.232 / 1.144 | `altura` | 0.4175 | 2.392 vs 0.119 | +0.2855 | +0.1068 | +0.0312 | −0.0141 |
| 2 | 0.446 / 1.284 / 0.274 / 0.954 | `altura` | 0.5026 | 2.544 vs 0.137 | +0.2147 | +0.1942 | −0.0104 | +0.0013 |
| 3 | 0.644 / 1.210 / 0.293 / 1.142 | `altura` | 0.4519 | 2.382 vs 0.126 | +0.2915 | +0.1325 | −0.0204 | +0.0067 |
| 4 | 0.697 / 1.468 / 0.428 / 1.108 | `altura`, **`contacto`** | 0.6121 | 2.695 vs 0.176 | +0.2264 | +0.1759 | −0.0235 | −0.0409 |
| 5 | 0.526 / 1.545 / 0.277 / 0.963 | `altura`, **`contacto`** | 0.6489 | 2.687 vs 0.172 | +0.4454 | +0.1279 | −0.0211 | +0.0036 |

**Comparar en vertical con el INFORME-39 es el punto de todo este prerregistro:** allí
`autopredictible` valía 0.5403 cinco veces y el efecto 2.544 cinco veces. Aquí van de **0.4175 a
0.6489** y de **2.382 a 2.695**. Ahora sí hay cinco mediciones de cinco realizaciones.

## 2. QUÉ REPLICÓ Y QUÉ NO

### Replicó 5/5 (y esto es lo que faltaba)
- **Escalón 2**, la ligadura contacto→no-caída: hallado en las cinco, efecto entre 2.38 y 2.70
  contra nulos entre 0.119 y 0.176. **Entre catorce y veinte veces su nulo, en cinco mundos.**
- **Examen VOE**: flotar sorprende entre +0.215 y +0.445; atravesar entre +0.107 y +0.194. Los diez
  por encima del piso de 0.05.
- **Nulos naturales**: los diez por debajo del techo de 0.05 (el mayor en magnitud, −0.0409).
- **El señuelo de ruido**: rechazado por ilegal en las cinco (autopredictibilidad 0.001 a 0.0025,
  contra un piso de 0.30). El criterio sigue discriminando por la razón correcta.

### NO replicó: la cláusula "único apto" — 3/5
El criterio firmado dice: *"escalón 1 declara `altura` (o `vel_z`) como **único** apto"*, en ≥4/5.

`altura` es apto en **5/5**. Pero en las semillas 4 y 5 **`contacto` también pasa**. Tres de cinco
está por debajo del umbral. **VEREDICTO: PARCIAL.**

## 3. POR QUÉ PASA — el mecanismo, no la excusa

| s | autopredictibilidad de `contacto` | piso | ¿legal? |
|---|---|---|---|
| 1 | 0.2271 | 0.30 | no |
| 4 | **0.3160** | 0.30 | **sí, por 0.016** |
| 5 | **0.3160** | 0.30 | **sí, por 0.016** |

Las semillas 4 y 5 son las de **soltada más alta** (1.468 y 1.545). Una caída más larga cambia el
ritmo de la señal de contacto —más tiempo cayendo, menos tiempo tocando— y la vuelve más regular,
lo justo para cruzar el piso. **Cruza por 0.016 sobre 0.30: es un aprobado raspado, no un rival
robusto.**

### Lo que NO voy a hacer, y por qué se dice aquí
`contacto` **no es un error**: es física de soporte legítima, no-mía y legal, y de hecho el caso 1
de la Regla 31 del prereg-29 siempre aceptó `contacto` como candidato válido. Sería facilísimo
declarar esto conseguido diciendo que "el espíritu del criterio se cumple".

**No se hace.** El criterio decía **único**, se firmó antes de mirar, y se aplica como está escrito.
Relajarlo ahora que conozco el resultado sería mover la portería — el mismo vicio que este proyecto
lleva treinta y cinco prerregistros combatiendo. Queda **PARCIAL**, y el criterio se discute en un
prerregistro nuevo si hay que discutirlo, nunca en el acta que lo evalúa.

## 4. UN HALLAZGO LATERAL QUE VALE LA PENA REGISTRAR

En el mundo fijo, `flota` daba **+0.9999** en las cinco semillas — y el ajuste interno tenía un
coeficiente de 3.500, un número que delata degeneración. Con mundos variables da entre **+0.215 y
+0.445**. Sigue siendo la sorpresa más grande de las dos (flotar sin apoyo es más imposible que
atravesar una mesa), pero ahora es **una medición y no una saturación**. El 0.9999 anterior era el
instrumento desbordado, no una certeza.

## 5. LO QUE SE AFIRMA Y LO QUE NO

**Se afirma:** la ligadura contacto→no-caída y la discriminación posible/imposible de la física de
soporte **replican en cinco mundos distintos**, no en uno repetido. Esa era la duda abierta del
INFORME-39 y queda cerrada.

**No se afirma:**
- que el escalón 1 aísle un **único** canal no-yo. Con la mesa y la soltada altas, no lo hace.
- que esto sea física del universo: sigue siendo PyBullet.

## 6. PROPUESTA AL DIRECTOR (Regla 15)
1. **No escribir todavía el nodo de la escalera.** Es la misma decisión que tomé en el INFORME-39 y
   por un motivo distinto: entonces faltaba réplica, ahora falta que el criterio se cumpla entero.
2. **Prerregistrar la pregunta que esto abre**, que es más interesante que el propio fallo: *¿debe
   el escalón 1 aislar UN canal, o es correcto que declare no-yos varios?* Un mundo tiene más de
   una cosa que no soy yo. Puede que el criterio "único" fuera nuestro, no del mundo — pero eso se
   decide **antes** de mirar los datos, no después.
3. **Congelar como caso del banco** que `contacto` cruza el piso a soltada alta, para que el día que
   alguien toque el piso de 0.30 sepa exactamente qué se mueve.

## 7. TRAZA
- Prerregistro: `registros/prerregistro-35.md` (firmado 10-ago-2026, rangos congelados allí).
- Código: `codigo/soporte.py`, 11/11 casos de Regla 31.
- Datos crudos: `resultados/p35-soporte-variable-s{1..5}/resumen.json`.
