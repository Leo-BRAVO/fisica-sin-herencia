# INFORME-46 — ACTA DEL PRERREGISTRO 37: **NO CONCLUYENTE POR INSTRUMENTO**, por dos motivos distintos
**10 de agosto de 2026.** Corrida oficial completa: 5 semillas, tres guardianas verdes en cada una,
commiteadas en `main`.

El módulo escribió **"EMPATE TOTAL"** en las cinco. **Esa etiqueta es incorrecta y la retiro.** No
fue un empate: la vara no pudo medir, y esta vez por **dos fallos independientes**, los dos míos.

---

## 1. LA TABLA COMPLETA

| s | pesado | dirigido | azaroso | pasivo | dir − aza | dir − pas | reparto del dirigido |
|---|---|---|---|---|---|---|---|
| 1 | sitio 0 | 0.9868 | 0.9883 | 0.9868 | −0.0016 | **0.0000** | [22, 2] |
| 2 | sitio 1 | 0.9885 | 0.9883 | 0.9885 | +0.0002 | **0.0000** | [2, 22] |
| 3 | sitio 0 | 0.9868 | 0.9883 | 0.9868 | −0.0015 | **0.0000** | [22, 2] |
| 4 | sitio 1 | 0.9885 | 0.9856 | 0.9885 | +0.0029 | **0.0000** | [2, 22] |
| 5 | sitio 0 | 0.9868 | 0.9881 | 0.9868 | −0.0013 | **0.0000** | [22, 2] |

## 2. FALLO 1 — la condición PASIVO es tautológica

`dirigido − pasivo = 0.0000 exacto` **en las cinco semillas**. Cero exacto cinco veces no es un
resultado: es la firma de una identidad.

Y lo es. En mi código, el pasivo **hereda literalmente los episodios del dirigido**, y el puntaje se
calcula **solo** a partir de esos episodios. Las dos condiciones son el mismo número por
construcción.

**Es exactamente la misma enfermedad que el prereg-32 cazó el 9 de agosto** — allí encarnado y
pasivo daban 0.0000 exacto porque las medidas de soporte no consultaban los comandos. Lo diagnostiqué
entonces, escribí la cura, y **volví a construirlo mal un día después en otro módulo**.

Lo agravante: **mi propia Regla 31 lo dijo**. El caso 3 imprime *"el pasivo HEREDA sus episodios:
empatar es el suelo, no un éxito"*. Escribí la advertencia y dejé correr el estudio igual. La
advertencia estaba en el sitio equivocado: debía ser **un fallo**, no una nota.

## 3. FALLO 2 — la medida satura tras dos toques

Medido después, sobre el mismo mundo:

| toques | puntaje |
|---|---|
| 2 (uno por sitio, y uno sin tocar) | 0.0000 |
| **4 (dos por sitio)** | **0.9725** |
| 8 | 0.9830 |
| 24 (lo que corrimos) | 0.9868 |

**Con dos toques por objeto la respuesta ya está al 97%.** Los veinte toques restantes compran
**0.014**.

**Elegir bien no puede importar en una tarea que se resuelve tocando cada cosa una vez.** Con dos
objetos y una sola propiedad oculta, el espacio de preguntas tiene tamaño dos: no hay estrategia
que ganar. El azaroso llega igual porque **es imposible no llegar**.

## 4. LA PREDICCIÓN REGISTRADA SE CUMPLIÓ — y mejor de lo que yo sabía

En el prereg-37 escribí, antes de correr:

> *"NO tengo confianza en que gane al azaroso. Con dos objetos y una sola propiedad, el espacio de
> preguntas es minúsculo... Si sale empate, la lectura honesta será que el mundo era demasiado
> simple para que elegir importara, y la cura es más objetos y más propiedades, no un umbral más
> bajo."*

Eso es exactamente lo que pasó, y ahora tiene **número**: la saturación al cuarto toque. La
predicción era correcta y la registré antes; es lo único que salvó a este estudio de leerse como un
resultado.

## 5. LO QUE SÍ FUNCIONÓ, y no es poco
- **El brazo tocó.** Es la primera vez en la historia del proyecto que Diego **interviene** sobre
  algo que no es su propio cuerpo. El sentido del tacto pasó de encenderse 1 vez cada 10.000 pasos
  a encenderse en cada toque.
- **La Regla 31 cazó dos bugs antes de correr**: el asentamiento que delataba la masa a simple
  vista, y mi `std` que medía la geometría del montaje en vez del movimiento.
- **El señuelo del agitador funcionó**: tocar siempre el mismo sitio puntúa 0.0000, porque un sitio
  nunca tocado no aporta separación.
- **El mundo sin duda dio ~0**, como debía.
- **El dirigido exploró** (reparto 22/2): fue al sitio que menos conocía. La política hace lo que
  dice hacer; lo que no existe es una tarea donde eso valga algo.

## 6. LO QUE NO SE AFIRMA
- **No se afirma que elegir no sirva.** Se afirma que **en esta tarea no puede medirse**, porque se
  resuelve sin elegir.
- **No se afirma nada sobre la condición pasiva.** Esa comparación no existió.
- **Ninguna afirmación causal sale de aquí.** El proyecto sigue en cero.

## 7. PROPUESTA AL DIRECTOR (Regla 15)
Un prerregistro nuevo, con **tres** cambios y no uno — porque los tres fallos son independientes:

1. **Un mundo donde elegir cueste.** Más objetos (6–8) y más de una propiedad oculta, de modo que
   el número de toques **no alcance** para probarlo todo. Si sobran toques, no hay estrategia.
2. **Un pasivo que no sea una copia.** Debe ver episodios de **otro** agente —como el
   `pasivo-ajeno` del prereg-32, que sí funcionó— y no los propios del dirigido.
3. **Una medida sin techo.** El puntaje actual llega a 0.97 con cuatro toques: hay que medir algo
   que siga creciendo, como cuántas propiedades quedan por resolver tras un presupuesto fijo.

**Y una regla nueva para el banco, que es la lección barata de hoy:** *si una Regla 31 imprime una
advertencia sobre una condición, esa advertencia debe ser un FALLO, no una nota.* Hoy escribí
"empatar es el suelo, no un éxito" y dejé correr cinco semillas de todos modos.

## 8. TRAZA
- Prerregistro: `registros/prerregistro-37.md` (firmado 10-ago-2026).
- Código: `codigo/experimentar.py`, 7/7 casos de Regla 31 — que aprobaron, y aun así el estudio no
  midió. **Aprobar la Regla 31 no garantiza que la pregunta sea medible: solo que el instrumento
  hace lo que dice.**
- Datos crudos: `resultados/p37-experimentar-s{1..5}/resumen.json`.
