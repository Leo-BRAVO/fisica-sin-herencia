# INFORME-62 — ACTA DEL PRERREGISTRO 52: hay dos motores porque el primero es CIEGO justo donde el segundo ve
**11 de agosto de 2026. Cinco mundos × cinco semillas nuevas (71, 73, 79, 83, 89) × dos motores.**
**Datos crudos:** `resultados/p52-invariantes/medida.json`; diagnóstico de la §4,
`resultados/p52-invariantes/diagnostico.json`. Módulo: `codigo/invariantes.py` (puerta 7/7).
**VEREDICTO, con las mismas palabras del archivo de datos:** *SEGUNDO MOTOR EN PIE — encuentra lo
que hay, calla donde no lo hay, no depende de las unidades y DISCREPA de sindy4.*

---

## 1. LA TABLA, que es el informe entero

| mundo | **invariantes** | **`sindy4`** |
|---|---|---|
| oscilador **sin amortiguar** | **5 de 5** | **0 de 5** |
| oscilador **amortiguado** | **0 de 5** | **5 de 5** |
| filas barajadas | 5 de 5 | 0 de 5 |
| columnas barajadas | 0 de 5 | 0 de 5 |
| ruido puro | 0 de 5 | 0 de 5 |

**Los dos motores son exactamente opuestos en los dos mundos reales.** Y ninguno de los dos se
inventa nada: los dos callan en los dos nulos.

| criterio congelado | salió | |
|---|---|---|
| **A** encuentra lo que hay | 5 de 5 en el mundo con cantidad conservada | ✔ |
| **B** calla donde se disipa | 0 de 5 en el amortiguado | ✔ |
| **C** nulos | 0 de 5 en columnas barajadas y en ruido puro | ✔ |
| **D** no depende de las unidades | ×1: 5, ×1000: 5 | ✔ |
| **E** los dos motores discrepan | y en **los dos** mundos reales | ✔ |

## 2. POR QUÉ EL CRITERIO E ERA EL QUE JUSTIFICABA LA FASE
Estaba escrito antes de correr: *"dos motores que siempre coinciden son un motor con un gasto
doble de auditoría"*, y el veredicto **FUNCIONA PERO NO APORTA** estaba preparado para ese caso.

**No hizo falta.** No es que discrepen en algún caso raro: **discrepan en todos los casos donde hay
algo que encontrar, y en direcciones opuestas.**

## 3. LO QUE `sindy4` NO PODÍA VER — la jaula, medida
El `DIAGNOSTICO-MOTOR-01` advirtió que el diccionario de seis piezas podía ser una jaula, y que
**si la ley no cabía ahí el motor no diría "no sé mirar eso" sino "no vi nada"**. Aquí está el
caso, y es más agudo de lo que esperaba: **la ley del oscilador sin amortiguar SÍ cabe en el
diccionario** —es `dx/dt = v`, `dv/dt = −0.9x`— **y aun así `sindy4` no la ve nunca.**

## 4. LA CAUSA, medida y no supuesta

| | condición de la matriz | tope del motor |
|---|---|---|
| **sin amortiguar** | **732978794549068.6** | 1000000.0 |
| **amortiguado** | **56.1** | 1000000.0 |

**Nueve órdenes de magnitud de diferencia entre dos mundos que solo se distinguen en un término de
rozamiento.** Y la razón es exacta, no estadística:

> **Si `x² + v²` se conserva, entonces las columnas `1`, `x²` y `v²` del diccionario son
> linealmente dependientes.** La matriz se vuelve singular **por construcción**, y la guarda de
> condición —la que en el INFORME-58 mató la alucinación— dispara y el motor calla.

**LA EXISTENCIA MISMA DE UNA CANTIDAD CONSERVADA ES LO QUE CIEGA AL BUSCADOR DE ECUACIONES.** No
es mala suerte ni un umbral mal puesto: es una consecuencia algebraica. Subiendo el tope a 10¹⁴
sigue sin declarar nada, así que **no se arregla aflojando la guarda.**

**Y el segundo motor ve justo ahí**, porque busca precisamente esa dependencia en vez de tropezar
con ella. **La complementariedad no es una casualidad afortunada: es estructural.**

## 5. LO QUE LA PUERTA ME CORRIGIÓ ANTES DE QUE EXISTIERA UN DATO
Puse como nulo el **barajado de filas**, copiado de `sindy3`. La puerta reprobó, **y tenía razón**:
sobre filas barajadas este motor **sí** encuentra el invariante, y hace bien. **Barajar el tiempo
destruye una ecuación diferencial, porque las derivadas necesitan el orden; pero no toca una
cantidad conservada:** `x²+v²` vale lo mismo visites los puntos en el orden que los visites.

**Copié el nulo de otro motor sin preguntarme si aplicaba al mío.** Un nulo tiene que destruir **la
estructura que el motor busca**, y cada motor busca una distinta. El nulo correcto —barajar cada
columna por separado, que rompe la relación entre `x` y `v`— **sí** lo deja mudo, 0 de 5.

**Y el barajado de filas no se tiró: se conservó como mundo, y no cuenta para el criterio C ni
puede ser la única fuente del E** — allí la discrepancia sería una consecuencia trivial de la
definición. **No hizo falta:** E se cumple en los dos mundos reales por sí solo.

## 6. LO QUE **NO** SE AFIRMA
- **Nada del universo.** Es una propiedad de nuestro código en nuestro simulador.
- **No se afirma que la cantidad hallada sea "la energía".** Es una combinación de columnas sin
  nombre — el motor devolvió `x²` y `v²` con pesos casi iguales. **Ponerle nombre sería herencia**,
  y ese nombre lo pone el comparador, del lado humano, si alguna vez procede.
- **No se afirma que `sindy4` esté mal.** Su guarda de condición hace lo correcto: **calla cuando
  no tiene cifras que dar.** Lo que este acta añade es **dónde** eso le pasa, y que es sistemático.
- **No entra en ningún torneo todavía.** Eso exige declarar los pisos del panel (prerregistro 51),
  y va aparte.

## 7. LA PREGUNTA QUE ABRE (Regla 18)
> **¿Cuántos mundos hay donde los dos motores callan a la vez, y no porque no haya nada?** Hoy
> sabemos de una forma de estructura que `sindy4` no puede ver y `invariantes` sí. **Nada garantiza
> que entre los dos cubran todo** — y el mismo argumento que justificó el segundo motor justifica
> preguntarse por un tercero. La diferencia es que ahora hay una manera de medirlo: **buscar mundos
> donde uno vea y el otro no.**

## 8. LO QUE LE TOCA AL DIRECTOR
Ninguna decisión urgente. Un hecho para la lista: **desde hoy hay dos motores vivos y cada
resultado tendrá que decir con cuál se midió.** Es el coste que se aceptó al autorizar la Fase 5, y
**la tabla de arriba dice que valió la pena**: sin el segundo, el oscilador sin amortiguar habría
seguido dando *"no vi nada"* para siempre, y lo habríamos leído como *"no hay ley"*.
