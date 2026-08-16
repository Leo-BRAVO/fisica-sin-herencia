# INFORME-63 — LOS 8 ÓRGANOS SIN EXAMINAR: reprueban los 8, y mi expectativa era demasiado optimista
**11 de agosto de 2026. Fase 6 del PLAN MAESTRO 01. Los ocho módulos del genoma que nunca habían
pasado por LA PUERTA.**
**Datos crudos:** `resultados/p-fase6-organos.json`.
**VEREDICTO:** *reprueban 8 de 8 — pero 8 de 8 reprueban por NO DECLARAR lo que miden, que no es
lo mismo que tener una medida rota.*

---

## 1. LO QUE DECLARÉ ANTES, y en qué me equivoqué
El PLAN MAESTRO 01 lo dejó escrito antes de correr, para que se me pudiera descontar:

> *"Expectativa declarada, para que se me pueda descontar: de 6 examinados reprobaron 3. Espero
> que de estos 8 reprueben entre 2 y 5. Si aprueban los 8, diré que la muestra anterior fue mala
> suerte y lo escribiré con esas palabras."*

**Reprobaron 8. Mi expectativa era demasiado optimista y falló por el lado que no había previsto:**
preparé la frase para el caso de que aprobaran todos, y no para el caso de que no aprobara
ninguno. **Un rango que solo se equivoca por un lado no era un rango honesto.**

## 2. PERO EL MOTIVO CAMBIA LA LECTURA, y hay que separarlo con cuidado

| paso de la puerta | cuántos fallan |
|---|---|
| **0 — manifiesto** (no declara qué mide) | **8** |
| **1 — fórmulas** (consecuencia del anterior) | **8** |
| **3 — ficha de sanidad** (no expone `_metodo_sanidad`) | **5** |
| 2 — sin pisar nombres | 2 |
| 7 — escritura limpia | 1 |

**Los 8 fallan por lo mismo: NUNCA FUERON CONSTRUIDOS PARA SER EXAMINADOS.** No declaran qué clase
de medida hacen, ni sus fórmulas, ni si sus condiciones comparten datos, ni exponen una ficha de
sanidad.

> **Esto NO es "ocho órganos rotos". Es "ocho órganos que nadie puede comprobar".** Y las dos
> cosas son graves de forma distinta: los tres REPROBADOS anteriores —sueño, atención,
> incertidumbre— fallaron **una medida concreta contra un criterio declarado**. Éstos fallan
> antes: **no hay criterio contra el que fallar.**
>
> **Confundir las dos cosas sería deshonesto en las dos direcciones**: exagera si digo "ocho
> órganos defectuosos", y minimiza si digo "solo es papeleo". **Un órgano que publica números en
> cada ronda de vida y no declara qué mide puede estar midiendo mal para siempre sin que nadie lo
> note** — que es exactamente por lo que este barrido existía.

## 3. Y DOS DE LOS TRES HALLAZGOS DE CÓDIGO SON **FALSOS POSITIVOS MÍOS**
Los revisé uno por uno en vez de contarlos:

- **`descubrir._iaaft`** — *"'x' se asigna FUERA del bucle y vuelve a asignarse DENTRO"*. **Falso
  positivo.** IAAFT es un algoritmo **iterativo**: `x` se inicializa y se refina en cada vuelta.
  Eso no es pisar un valor, es la forma de escribir un bucle.
- **`interocepcion.coste_de`** — *"'ultimo' se asigna FUERA y vuelve a asignarse DENTRO"*. **Falso
  positivo también.** `ultimo = None` antes del bucle es un **inicializador**.
- **`cerebro.py:115`** — *"'prog' se calcula y no se usa"*. **Éste sí es real**, y en este
  proyecto cuenta: **una variable muerta es una afirmación falsa sobre lo que hace el código.**

**El detector de "pisar nombres" no distingue un INICIALIZADOR de un valor CLOBBERADO**, y ése es
un defecto de mi instrumento, no de los órganos.

**Y no lo arreglo hoy.** Aflojar un detector **después** de verlo dispararme en contra es
exactamente el movimiento que este proyecto prohíbe. Va en su propio prerregistro, con la prueba
por los dos lados: **debe seguir cazando un valor realmente pisado y dejar pasar un inicializador.**

## 4. LO QUE VI Y NO ES UN VEREDICTO DE LA PUERTA
Al correr `percepcion2`, **tres de sus cuatro entrenamientos divergieron**: la pérdida pasó de
65.76263 a 40202.47179, a 1822767.04958 y a 10123561.48734 en cuatro épocas.

**No lo cuento como hallazgo del barrido** —la puerta reprobó ese módulo por el manifiesto, no por
esto— y **no afirmo que sea un defecto**: puede ser una configuración de prueba con paso demasiado
grande. **Lo escribo porque verlo y callarlo sería peor**, y porque es exactamente el tipo de cosa
que un módulo sin ficha de sanidad puede llevar meses haciendo sin que nadie lo mire.

## 5. LO QUE **NO** SE AFIRMA
- **No se afirma que los 8 órganos midan mal.** Se afirma que **no se puede saber**, que es una
  situación distinta y en algunos aspectos peor.
- **No se afirma que ponerles manifiesto los arregle.** Declarar qué mides es el requisito para
  poder comprobarlo, no la comprobación.
- **No se toca ningún órgano.** Ponerles manifiesto y ficha es trabajo de ocho prerregistros, uno
  por órgano, porque cada ficha declara criterios que pueden reprobar.
- **Nada del universo.**

## 6. LA PREGUNTA QUE ABRE (Regla 18)
> **¿Cuánto de lo que Diego "sabe" viene de órganos que nadie puede comprobar?** Los 8 publican
> números en cada ronda de vida y alimentan a los demás. La cadena G14→G8 nos enseñó que un
> número inflado viaja: **el daño no se queda en el módulo que lo produce.** Falta el mapa de qué
> consume qué de estos ocho, y el `contratos.py` de la Fase 3 es la herramienta para hacerlo.

## 7. LO QUE LE TOCA AL DIRECTOR
Una decisión de orden, no urgente: **son ocho prerregistros, uno por órgano.** Es el trabajo más
largo y menos vistoso del plan y **es donde está la mayor parte de la ignorancia que nos queda**:
5 órganos sellados de 15, 2 reprobados con medida, y **8 sobre los que no sabemos ni preguntar**.
