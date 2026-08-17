# INFORME-75 — ACTA DEL PRERREGISTRO 64: el estudio queda DESCARTADO por su propio nulo, y era el riesgo que estaba escrito
**17 de agosto de 2026. 15 semillas, los dos latentes entrenados sobre la misma escena, con la
pérdida de píxel publicada y ni una línea de física impuesta.**
**Datos crudos:** `resultados/p64-latente/medida.json`. Módulo: `codigo/latente_conservado.py`
(puerta 8/8).
**VEREDICTO, con las palabras del archivo de datos:** *SE DESCARTA EL ESTUDIO ENTERO — el nulo
encontró invariantes en 4 semillas: el diccionario grande los está fabricando.*

---

## 1. LOS NÚMEROS

| | de 15 semillas |
|---|---|
| el latente **keypoint** admite invariante | **1** |
| el latente **píxel** admite invariante | **0** |
| **el NULO admite invariante** | **4** ← esto lo tumba todo |

| criterio congelado | pedía | salió | |
|---|---|---|---|
| **A** no se impone nada | ninguna pérdida propia | ✔ | ✔ |
| **B** el nulo no encuentra nada | **cero** invariantes en el nulo | **4** | ✘ |
| **C** el keypoint conserva más | ≥ 12 de 15 | 1 | ✘ |
| **D** el juicio es fuera de muestra | 70% busca / 30% juzga | ✔ | ✔ |

## 2. QUÉ SIGNIFICA, y qué NO significa
**El nulo baraja cada columna del latente por separado.** Eso destruye la relación entre columnas
—que es donde vive una cantidad conservada— y conserva la distribución de cada una. **Si ahí
aparece un «invariante», es que el buscador se lo está inventando.**

Apareció en **4 de 15**.

> **Por eso el criterio B manda, y manda descartarlo TODO.** No se puede leer nada de las otras
> filas: si el instrumento fabrica invariantes una de cada cuatro veces, el «1 de 15» del keypoint
> **no distingue de cero**, y el «0 de 15» del píxel tampoco dice nada.

**Lo que NO se puede concluir, y quiero que quede claro porque la tentación es fuerte:**
**NO se ha demostrado que el cuello de botella espacial no conserve nada.** Se ha demostrado que
**esta forma de buscarlo no sirve**. Son cosas distintas y confundirlas sería exactamente el error
que el nulo existe para impedir.

## 3. POR QUÉ PASÓ, y estaba escrito ANTES de correr
El prerregistro lo dijo en su sección 3, palabra por palabra:

> *«Un diccionario más grande encuentra invariantes más fácilmente por casualidad. (…) Por eso el
> nulo no es un adorno aquí: es el criterio que manda.»*

`invariantes.py` trabaja con **2 variables y 5 términos**. Aquí el latente tiene más columnas, y
todos sus productos de dos en dos dan **muchos más términos**. Con tantas direcciones disponibles,
que **alguna** salga casi constante en el tramo de juicio deja de ser informativo.

**El riesgo se nombró, se puso un criterio que podía matarlo, y lo mató.** Eso es el método
funcionando, no fallando.

## 4. LO QUE SÍ QUEDA, y es lo que el item 27 pedía de verdad
El item 27 pedía **regularizar el latente con estructura hamiltoniana**. **No se hizo, y la razón
es la Regla 27:**

> Una pérdida hamiltoniana **le está diciendo a Diego que el mundo conserva algo**. Es una ley de
> la física humana metida por la puerta de atrás, y de las más caras. Si se la regalamos y luego
> «descubre» que hay una cantidad conservada, **no ha descubierto nada: ha repetido lo que le
> pusimos en la pérdida.**

**Eso sigue en pie, y no depende de este resultado.** Lo que este estudio intentó —y no logró— fue
la versión legal: **medir** si la estructura aparece sola. Entrenar no se tocó: el criterio A
aprobó y el módulo no define ninguna pérdida propia, comprobado con AST.

## 5. LO QUE ME COSTÓ ESCRIBIR EL CRITERIO A, y va aquí porque es gracioso y es real
El chequeo de «este módulo no define ninguna pérdida» falló **dos veces contra sí mismo**:
1. La primera versión buscaba la cadena `def perdida` en el propio archivo — **y esa cadena estaba
   en el chequeo**. Se marcó a sí misma. Es la **tercera vez** que un detector mío confunde una
   cadena con código.
2. La segunda usaba AST, pero la función se llamaba `define_alguna_perdida` — **y su propio nombre
   contenía la palabra que buscaba**. Se volvió a marcar.

La tercera funciona. Va escrito en el código, en su docstring, para que nadie lo «arregle» sin
saber por qué se llama como se llama.

## 6. LO QUE **NO** SE AFIRMA
- **Nada del universo.**
- **NO se afirma que los latentes no conserven nada.** El instrumento no vale; los datos de los
  latentes **no se interpretan**.
- **NO se afirma que `invariantes.py` esté mal.** Su diccionario de 5 términos pasó su propio nulo
  en el prerregistro 52. **Lo que no aguanta es mi generalización.**
- **NO se toca ninguna pérdida, ni ahora ni como consecuencia.**
- **NO se editó `ojos_keypoint.py`, `ojos_brazo.py` ni `invariantes.py`.**

## 7. LA PREGUNTA QUE ABRE (Regla 18)
> **¿Cuántos términos aguanta un buscador de invariantes antes de empezar a fabricarlos?**
> `invariantes` aguanta 5. Mi generalización, con muchos más, no. **En medio hay un número y no lo
> he buscado** — y buscarlo es un estudio en sí mismo: subir términos de uno en uno y ver dónde el
> nulo empieza a encontrar cosas.

## 8. LO QUE LE TOCA AL DIRECTOR
**Nada urgente.** El item 27 queda respondido en lo que importaba: **no se impone estructura
física, y la razón está escrita**. La versión medible se intentó y **el instrumento no dio la
talla**, con el motivo publicado.

Si algún día quiere retomarlo, el camino ya no es «buscar un invariante en el latente» sino
**primero encontrar cuántos términos aguanta el buscador**, y eso es un prerregistro nuevo.
