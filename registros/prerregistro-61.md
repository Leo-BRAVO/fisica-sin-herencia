# Prerregistro 61 — EL CONTACTO, OTRA VEZ, con la potencia calculada ANTES — 17 de agosto de 2026
**Rehace el prerregistro 60, que su propio nulo anuló. Autorizado por el director («adelante con
todo»). Peldaño (Regla 9): Fase 1.**
**Estado: FIRMADO después de la lectura previa del catálogo y antes de escribir `contacto2.py`.**

---

## 0. POR QUÉ HAY UN SEGUNDO INTENTO
El prerregistro 60 no falló por la política: **falló por mi criterio**. Congelé «gana en 4 de 5» y
**el azar pasa ese criterio el 18.75% de las veces**. El nulo lo pasó —ganó 4 de 5— y anuló el
estudio. Está en el INFORME-71 y en el catálogo como **error nº26**.

> **Esto NO es «subir las semillas hasta que salga».** El estudio 60 está publicado con su
> veredicto y no se toca. Lo que cambia aquí es **el diseño**, y el número de semillas **sale de
> una binomial, no de mi gusto** — y se escribe antes de correr nada.

## 1. LA CUENTA, hecha delante
Para un criterio de «k de n» comparado contra una moneda justa, `P(X ≥ k | n, p=0.5)`:

| n | k | el azar lo pasa |
|---|---|---|
| 5 | 4 | **18.8%** ← el del prerregistro 60 |
| 5 | 5 | 3.1% |
| 10 | 8 | **5.5%** — no basta |
| 10 | 9 | 1.1% |
| **15** | **12** | **1.8%** |

**Se elige n = 15 y k = 12.** No el «9 de 10», aunque su probabilidad sea menor: **con 15 semillas
hay más capacidad de ver un efecto real** que con 10, y exigir 9 de 10 castiga a un efecto
moderado tanto como al azar. **12 de 15 es el equilibrio, y queda congelado con su 1.8% escrito.**

## 2. LO QUE SE CONSTRUYE, y lo que NO se toca
- **`contacto2.py`**: **importa** `politica_contacto` —el mundo, las tres políticas, el medidor y
  los dos guardianes de la Regla 27— y **solo cambia el número de semillas y el criterio de
  conteo**. Ni una línea de física copiada.
- **NO se edita `politica_contacto.py`.** Está **sellado**: editarlo mataría su sello y dejaría
  irreproducible el INFORME-71.
- **Todo lo demás se hereda tal cual**: mismo mundo, mismo radio, mismos 20000 pasos, mismo saco
  de acciones para las tres políticas.

## 2.bis LA LÍNEA BASE TONTA (Reglas 11 y 12)
**Se hereda entera del prerregistro 60: el balbuceo** — elegir al azar entre los mismos candidatos,
sin mirar la observación. Es el rival trivial que pide la Regla 11 y es **ciego por construcción**.

*(Esta sección se añadió después de correr, porque `reglas.py` marcó que el prerregistro no
nombraba su línea base. **No cambia ningún criterio**: el balbuceo ya era el rival en la tabla de
abajo y en el código heredado. Lo que faltaba era escribirlo.)*

## 3. LOS CRITERIOS CONGELADOS

| | criterio | pide |
|---|---|---|
| **A** | **el cortafuegos aguanta** | la señal declara solo `error_de_prediccion_propio` y la observación no lleva etiquetas humanas |
| **B** | **el mundo sordo no premia** | donde el contacto **no hace nada**, la intrínseca supera al balbuceo en **menos de 12 de 15** |
| **C** | **la intrínseca busca sola** | supera al balbuceo en **12 de 15 o más** (el azar: 1.8%) |
| **D** | **el nulo no gana** | la barajada supera al balbuceo en **menos de 12 de 15** |
| **E** | **no se puede inventar contacto** | con radio 0, **todas** las políticas dan exactamente 0.0 |

**Se publica además, sin poder de veto:** la diferencia mediana entre intrínseca y balbuceo. Un
conteo de signos dice **si** hay efecto; no dice **cuánto**.

## 4. LO QUE SE ESPERA, y qué se dirá EN CADA CASO
**Espero que C falle**, porque el 60 apuntaba en esa dirección: 2 de 5, y una corrida suelta de la
intrínseca quedó por debajo del balbuceo.

- **Si no falla C**, se escribe que **la curiosidad sola basta para buscar el contacto** — y será un
  resultado en contra de lo que yo esperaba, que es el que más vale.
- **Si falla C**, se escribe que **la curiosidad sola NO basta**, con un diseño que **sí tenía
  potencia** — y entonces el item 30 queda cerrado con una respuesta, no con un empate.
- **Si falla D otra vez**, el problema no es la potencia sino el nulo, y hay que rehacer el nulo.

## 5. REGLA 31 — sobre MI PROCEDIMIENTO
La hereda entera de `politica_contacto`, que ya la pasó: control positivo (la mano derecha marca
**0.937**), señuelo (radio 0 da **0.0**), relación metamórfica con **base 0.05 y no 0.0** y factor
derivado del **cubo del radio**, y las dos pruebas del cortafuegos por los dos lados.
**`SUJETO` sigue siendo la política intrínseca, y la Regla 31 no la llama.**

Lo único **propio** de este módulo es el criterio de conteo, y se examina por los dos lados: «12 de
15» debe **aprobar** con 12 victorias y **reprobar** con 11.

## 6. CUÁNDO SE ABANDONA (Regla 13)
Igual que el 60: **A** o **E** fallando descartan el estudio; **B** o **D** fallando lo anulan
aunque C salga a favor. **Y el criterio C no se mueve pase lo que pase.**

## 7. LO QUE **NO** SE AFIRMA
- **Nada del universo.**
- **NO se retira el INFORME-71.** Aquel estudio dijo lo que midió y se queda.
- **NO se afirma que 15 semillas sean suficientes para un efecto pequeño.** 12 de 15 detecta un
  efecto **consistente**; uno débil podría escapársele, y eso se dirá si C falla por poco.
- **NO se conecta la política a nada.**

## 8. FIRMA
Avanza por **quórum adversarial**: el criterio que decide **lo escribí esperando que falle**, el
nulo y el mundo sordo pueden anularlo aunque salga a mi favor, y la probabilidad del azar está
**escrita antes de correr**. Revocable con una palabra del director.
