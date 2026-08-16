# Prerregistro 52 — EL SEGUNDO MOTOR: buscar lo que NO cambia — 11 de agosto de 2026
**Fase 5 del PLAN MAESTRO 01. Peldaño (Regla 9): Fase 1 — propiedad de nuestro código, no del
universo.**
**Estado: FIRMADO antes de escribir `invariantes.py`.**

---

## 0. POR QUÉ UN SEGUNDO MOTOR, y por qué NO para sustituir al primero
`sindy4` tiene una limitación que **ningún arreglo de umbral resuelve**: solo puede expresar
mezclas de **seis piezas fijas** (`1, x, v, x², xv, v²`). **Si la ley del mundo no está ahí, no la
verá ni con el umbral perfecto — y no dirá "no sé mirar eso": dirá "no vi nada".**

**El segundo motor no compite por ser mejor. Compite por fallar de otra manera.** Y es la única
forma de detectar esa jaula desde fuera: **si encuentra estructura donde `sindy4` no ve nada, la
jaula existe y está medida.**

## 1. QUÉ HACE, y por qué es una forma distinta de mirar
`sindy4` pregunta **"¿cómo cambian las cosas?"** — busca una ecuación de movimiento.
`invariantes.py` pregunta **"¿qué NO cambia?"** — busca una **cantidad conservada**.

Es la idea del teorema de Noether, pero **al revés y sin heredar nada**: no se parte de una
simetría conocida, se buscan combinaciones de las lecturas cuyo valor **se mantiene constante a lo
largo de la trayectoria**. Y tiene una propiedad que ninguna ecuación de movimiento tiene:
**una cantidad conservada se descubre MIRANDO, sin intervenir.**

**Método, sin física humana:** se construye un diccionario de funciones del estado —**sin el
término constante**, porque una constante se conserva trivialmente y sería una respuesta vacía—,
se normaliza por las escalas de los propios datos, y se busca la dirección de **mínima variación**.
Si esa dirección varía mucho menos que las demás y **se mantiene fuera de muestra**, hay invariante.

## 2. LA PREGUNTA
> ¿Puede un motor que solo busca lo que no cambia **encontrar un invariante donde lo hay**,
> **callar donde no lo hay**, y **discrepar de `sindy4` en algún caso** — que es lo único que
> justifica tener dos?

## 3. LA LÍNEA BASE TONTA (Reglas 11 y 12)
**Declarar que cualquier dirección es invariante.** Se le gana exigiendo dos cosas que la línea
base tonta no cumple: **una separación clara respecto de la siguiente dirección** (si todas varían
parecido, no hay invariante, hay ruido) y **que la constancia se mantenga en el tramo que no vio**.

## 4. EL DISEÑO, congelado
- **Diccionario sin término constante:** `x, v, x², xv, v²`.
- **Adimensionalización** por las escalas de los propios datos — la lección de `sindy4`: un corte
  con unidades se mueve con la escala.
- **Fuera de muestra:** se busca en el 70% de la trayectoria y se comprueba en el 30% restante.
- **Se declara invariante** si, en el tramo no visto, la **variación relativa ≤ 0.05** y hay un
  **salto ≥ 10×** respecto de la siguiente dirección menos variable.
- **Cuatro mundos:** oscilador **sin** amortiguar (tiene invariante), oscilador **amortiguado** (no
  lo tiene: la energía se disipa), **barajado** y **ruido puro**.

## 5. LOS CRITERIOS CONGELADOS

| | criterio | pide |
|---|---|---|
| **A** | **encuentra lo que hay** | En el oscilador **sin amortiguar**, declara invariante en **5 de 5** semillas |
| **B** | **calla donde no hay** | En el oscilador **amortiguado** —donde la cantidad se disipa— **no declara** invariante en **5 de 5** |
| **C** | **nulos** | En **columnas barajadas por separado** y en **ruido puro**, no declara invariante en **5 de 5** cada uno |

> ### ENMIENDA 1 — el nulo de barajar NO es transferible entre motores. Escrita ANTES de correr, 11-ago-2026
> **La puerta reprobó la Regla 31 antes de que existiera un dato, y el equivocado era yo.**
>
> Había puesto como nulo el **barajado de filas** — el mismo que usa `sindy3`. **Y sobre él, el
> motor de invariantes encuentra el invariante, correctamente.** Barajar el orden temporal
> destruye una ecuación diferencial, porque las derivadas necesitan el orden; **pero no toca una
> cantidad conservada**: `x²+v²` vale lo mismo visites los puntos en el orden que los visites.
>
> **Copié el nulo de otro motor sin preguntarme si aplicaba al mío.** Un nulo tiene que destruir
> **la estructura que el motor busca**, y cada motor busca una distinta.
>
> **El nulo correcto para un buscador de invariantes es barajar CADA COLUMNA POR SEPARADO:** eso
> rompe la relación entre `x` y `v` —la superficie donde vive el invariante— conservando la
> distribución de cada una. Ahí sí no debe declarar nada.
>
> **El barajado de filas no se tira: se conserva como MUNDO del estudio**, precisamente porque los
> dos motores deberían comportarse distinto en él. Pero **no cuenta para el criterio C**, y
> **tampoco puede ser la única fuente del criterio E** — si la única discrepancia entre los dos
> motores fuera ésa, sería una consecuencia trivial de la definición y no un aporte, y se
> escribiría así.
| **D** | **no depende de las unidades** | El mismo mundo ×1000 da **el mismo veredicto** en las 5 semillas. Es la lección de `sindy4`, aplicada desde el primer día |
| **E** | **los dos motores DISCREPAN en algún caso** | Existe al menos un mundo donde uno declara y el otro no. **Si coincidieran siempre, el segundo motor no aporta nada y se dice así** |

**El criterio E es el que justifica la fase entera.** Dos motores que siempre coinciden son un
motor con un gasto doble de auditoría.

## 6. REGLA 31 — sobre MI PROCEDIMIENTO, los dos lados
- **Control positivo (debe aprobar):** sobre una serie construida a mano donde **yo pongo** una
  cantidad exactamente conservada, el motor la encuentra.
- **Señuelo / control negativo (debe fallar):** sobre ruido puro no declara nada; y **el
  diccionario no lleva término constante**, para que la respuesta trivial *"la constante se
  conserva"* **no sea representable**.
- **La medida responde:** al añadir ruido de **medida** creciente, la constancia empeora. *(De
  medida y no de proceso — la `LECCION-RUIDO-01`, que ya me costó tres módulos.)*
- **Base distinta de cero** en toda relación metamórfica. Sexta vez que lo escribo este mes.
- **No se prueba aquí nada sobre `sindy4`.** La comparación entre motores es el criterio E, es
  decir, **resultado**, no requisito de entrada. Es el error que dejó NULO al prerregistro 45.

## 7. CUÁNDO SE ABANDONA (Regla 13, con número)
- Si falla **A**, el motor **se descarta**: uno que no encuentra un invariante que existe y es
  exacto no sirve para nada.
- Si falla **B** o **C**, **se descarta igual**: un motor que declara invariantes donde no los hay
  es el defecto de `sindy3` con otro nombre, y sería peor tenerlo que no tenerlo.
- Si falla **E**, el motor **funciona pero no aporta**, y se escribe exactamente así: *"coincide
  siempre con `sindy4`, luego duplicar la auditoría no está justificado"*.

## 8. LO QUE **NO** SE AFIRMA
- **Nada del universo.** Que el motor encuentre una cantidad conservada en nuestro simulador no
  dice nada sobre el mundo real.
- **No se afirma que la cantidad hallada sea "la energía".** Es una combinación de columnas sin
  nombre. **Ponerle nombre sería herencia**, y el nombre lo pone el comparador —del lado humano—
  si alguna vez procede.
- **No entra en ningún torneo todavía.** Eso exige declarar los pisos del panel, y va aparte.

## 9. FIRMA
Avanza por **quórum adversarial**: **B y C mandan descartar el motor** si declara de más, el
criterio **E** puede dejar la fase entera en "no aporta", y la respuesta trivial se hace
irrepresentable quitando la constante del diccionario en vez de prohibiéndola con un chequeo.
Revocable con una palabra del director.
