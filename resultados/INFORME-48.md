# INFORME-48 — ACTA DEL PRERREGISTRO 42: ganó la hipótesis que yo quería, y ganar destapó algo peor
**10 de agosto de 2026. Autorizado por el director ("la 1 sí"). Cinco semillas nuevas: 71, 73, 79, 83, 89.**
**Datos crudos de este acta: `resultados/p42-unico-apto/veredicto.json`.** Prerregistro:
`registros/prerregistro-42.md`. Módulo sellado: `codigo/unico_apto.py`.

---

## 1. QUÉ SE HIZO, en una frase
El prereg-35 había quedado **PARCIAL** porque pedía que `altura` fuera el **único** canal apto y en
dos mundos `contacto` también pasaba. Se preguntó de nuevo, con el criterio congelado antes de
correr y **sobre cinco mundos que nadie había visto** — los cinco viejos quedaron quemados al haber
generado la hipótesis.

## 2. EL RESULTADO CRUDO

| semilla | mesa / suelta / masa / x | aptos | elegido | auto(`altura`) | margen sobre el mejor ajeno |
|---|---|---|---|---|---|
| 71 | 0.63 / 1.30 / 0.30 / 0.98 | `altura` | `altura` | 0.5748 | — (sin ajenos) |
| **73** | 0.65 / 1.30 / 0.41 / 0.99 | **`art1`**, `altura` | `altura` | 0.5245 | **−0.4552** |
| 79 | — | `altura`, `contacto` | `altura` | 0.6211 | +0.3038 |
| 83 | — | `altura` | `altura` | 0.5515 | — |
| 89 | — | `altura` | `altura` | 0.5664 | — |

- **`altura` elegida 5 de 5.** Línea base tonta (elegir uno de 7 canales al azar) = 0.1429.
  **Ganancia sobre la línea base: +0.8571.**
- **Un solo apto: 3 de 5** — pedía 4. **H-AISLAR pierde.**
- **Margen ≥ 0.10: 4 de 5** — pedía 4. Junto con el 5/5 de la elección, **H-VARIOS gana.**

## 3. EL VEREDICTO, por el criterio congelado: **H-VARIOS**
El escalón 1 **no** debe exigir un único apto; basta con que el canal objetivo sea el elegido y
gane con margen. **Y era la hipótesis que yo quería**, cosa que dejé escrita en el prerregistro
antes de correr, precisamente para que se pudiera descontar al leerme.

## 4. LO QUE EL CRITERIO NO ANTICIPÓ, Y ES LO MÁS IMPORTANTE DE ESTE ESTUDIO

**En el mundo 73, el canal apto que acompañó a `altura` no fue `contacto`. Fue `art1` — una
articulación del propio brazo de Diego.**

| canal (mundo 73) | autopredictible | obediencia neta | ¿legal? | ¿no-mío? |
|---|---|---|---|---|
| art0 | 1.0000 | 0.1234 | sí | **no** |
| **art1** | 0.9797 | **0.0297** | sí | **SÍ** ← techo 0.05 |
| art2 | 0.9998 | 0.6559 | sí | no |
| **altura** | 0.5245 | **0.0000** | sí | sí |

`art1` pasó el techo de obediencia (0.0297 contra un techo de 0.05) y **el instrumento declaró
"no-mía" una parte del cuerpo de Diego**. `altura` ganó igual — pero **ganó por el desempate**
(0.0000 < 0.0297), no porque el criterio hubiera excluido al intruso.

**Y aquí está la lección incómoda:** la cláusula "único apto" que este estudio acaba de derogar
**habría marcado el mundo 73 como problema**. H-VARIOS lo declara victoria limpia. Es decir: **la
hipótesis que yo prefería ganó, y al ganar dejó pasar un error peor que el que resolvía.**
`contacto` colándose era inocuo — el contacto de verdad no es Diego. **Un brazo suyo colándose no
lo es**, porque el escalón 1 existe exactamente para separar su cuerpo de lo que no lo es.

## 5. QUÉ **NO** SE HACE AHORA, y por qué es lo importante
**No se mueve el criterio.** Sería la tercera vez que la misma tentación aparece con otra cara, y
es justo lo que el director puso como condición al pasar a observador: *"no alteramos resultados ni
ponemos el happy path"*. El veredicto es **H-VARIOS**, con el número que salió.

**No se declara nodo.** Esto es un estudio sobre un instrumento nuestro, no sobre el universo.

**Lo que sí se hace:** el hallazgo del mundo 73 **abre una pregunta nueva y se registra como tal**
(Regla 18). La pregunta no es *"¿cuántos aptos se admiten?"* — ésa acaba de contestarse. Es otra:

> **¿Por qué una articulación del propio brazo puede parecer no-obediente?** El techo de obediencia
> se cruzó por 0.0297 contra 0.05. Si el mando de Diego a veces no predice su propio brazo, el
> problema no está en cuántos aptos se admiten: está en que **la señal de mando no captura todo lo
> que el brazo hace** — y eso es una limitación del instrumento que ningún criterio de conteo
> arregla.

Eso exige su propio prerregistro, con su propia línea base y su propio señuelo. **No se escribe
hoy**, porque escribirlo con este resultado caliente delante es exactamente cómo nació el error que
este estudio vino a corregir.

## 6. LO QUE ESTE ESTUDIO NO PUEDE AFIRMAR
- **Nada sobre el universo.** Es sobre cómo leer un instrumento nuestro.
- **No revive el prereg-35**, que se queda como quedó (Regla 8). Lo que cambia es el criterio de los
  estudios **futuros**.
- **No dice que el escalón 1 sea correcto.** Dice que su cláusula de unicidad era la exigencia
  equivocada — y de paso, que tiene un problema distinto y peor que nadie había visto.

## 7. LA DECISIÓN QUE LE TOCA AL DIRECTOR
Ninguna urgente. Pero **queda registrado que el resultado favorece a lo que yo proponía**, y que la
única razón por la que eso es creíble es que el criterio estaba congelado, las semillas eran nuevas
y la confesión iba escrita antes de correr. **Si alguna vez le parece que le estoy dando la razón a
mí mismo con demasiada facilidad, éste es el estudio que hay que releer para comprobarlo.**
