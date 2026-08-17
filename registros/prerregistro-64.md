# Prerregistro 64 — EL LATENTE Y LA CANTIDAD CONSERVADA: medirla, NO imponerla — 17 de agosto de 2026
**Item 27 de la crítica externa («regularización física del latente», HNN/LNN). Autorizado por el
director («adelante con todo»). Peldaño (Regla 9): Fase 1.**
**Estado: FIRMADO después de la lectura previa del catálogo y antes de escribir
`latente_conservado.py`.**

---

## 0. LO QUE PEDÍA EL ITEM, Y POR QUÉ NO LO HAGO ASÍ
La crítica externa proponía **regularizar el latente con estructura hamiltoniana** — entrenar el
autoencoder con una pérdida que empuje hacia coordenadas canónicas y una energía conservada.

**No lo hago, y la razón es la Regla 27.**

> Una pérdida hamiltoniana **le está diciendo a Diego que el mundo conserva algo**. Eso no es una
> arquitectura: **es una ley de la física humana metida por la puerta de atrás**, y de las más
> caras — la conservación de la energía costó siglos. Si se la regalamos y luego «descubre» que
> hay una cantidad conservada, **no ha descubierto nada: ha repetido lo que le pusimos en la
> pérdida.**

**Lo que sí es legal, y es lo que este estudio hace: MEDIR si esa estructura aparece sola.**

- **Entrenar** sigue siendo con **pérdida de píxel y nada más**, exactamente como está publicado.
- **Medir** si el latente resultante admite una cantidad casi constante **es cosa nuestra**, del
  lado humano, y no toca ni un peso de Diego.

**Medir no es enseñar.** Ésa es la frontera entera de la Regla 27, y este estudio se queda de este
lado.

## 1. LA PREGUNTA
> ¿El latente del **cuello de botella espacial** (keypoints) admite una **cantidad conservada** que
> el latente de **píxeles planos** no admite — buscada fuera de muestra y sin imponer nada?

Es la versión medible de la queja original: *«el autoencoder confunde el fondo con la física»*.

## 2. LO QUE SE CONSTRUYE, y lo que NO se toca
- **`latente_conservado.py`**: **importa** de `ojos_keypoint` —sellado— la escena, las dos
  arquitecturas y `entrenar`; y de `invariantes` —sellado— **los tres umbrales y la medida de
  calidad**. No copia ninguno.
- **Lo único propio es el diccionario**: `invariantes.buscar` está escrito para **dos** variables y
  el latente tiene **más**. Se generaliza a todos los términos lineales y cuadráticos de las
  columnas del latente.
- **NO se edita `ojos_keypoint.py`, `ojos_brazo.py` ni `invariantes.py`.**
- **NO se cambia ninguna pérdida.** Ni una línea de entrenamiento distinta de lo publicado.

## 3. LO QUE ESA GENERALIZACIÓN CUESTA, y hay que decirlo ANTES
**Un diccionario más grande encuentra invariantes más fácilmente por casualidad.** Con más términos
hay más direcciones donde una combinación puede salir casi constante sin que signifique nada.

> **Por eso el nulo no es un adorno aquí: es el criterio que manda.** Si el nulo también encuentra
> invariantes, la medida no vale y el estudio se descarta entero, gane lo que gane el keypoint.

**El nulo correcto es el del prerregistro 52 (ENMIENDA 1): barajar CADA COLUMNA por separado.**
Eso destruye la relación entre columnas —que es donde vive un invariante— y conserva la
distribución de cada una. Barajar filas no serviría: una cantidad conservada vale lo mismo en
cualquier orden, y ése fue el error nº8 del catálogo.

## 4. LA LÍNEA BASE TONTA (Reglas 11 y 12)
**El latente de píxeles**, entrenado sobre las mismas escenas, con las mismas semillas y las mismas
épocas. Es el rival correcto porque **lo único que cambia entre los dos es el cuello de botella**.

## 5. LA POTENCIA, calculada ANTES (error nº26)
Criterio de conteo sobre semillas, con `P(X ≥ k | n, p=0.5)`:

| n | k | el azar lo pasa |
|---|---|---|
| 5 | 4 | 18.8% — **no vale**, es el error que anuló el prerregistro 60 |
| **15** | **12** | **1.8%** |

**Se congelan 15 semillas y 12 de 15**, y las semillas son **nuevas**: 277, 281, 283, 293, 307,
311, 313, 317, 331, 337, 347, 349, 353, 359, 367. Ninguna quemada en el banco ni usada en los
prerregistros 56 y 57.

## 6. LOS CRITERIOS CONGELADOS

| | criterio | pide |
|---|---|---|
| **A** | **no se impone nada** | las dos arquitecturas se entrenan con la pérdida publicada; el módulo no define ninguna pérdida propia |
| **B** | **el nulo no encuentra nada** | con las columnas barajadas por separado, **ni un invariante** en **ninguno** de los dos latentes, en las 15 semillas. Si aparece uno, **se descarta el estudio entero** |
| **C** | **el keypoint conserva más** | el latente de keypoints admite invariante en **más** semillas que el de píxeles, en **12 de 15 o más** comparaciones pareadas (el azar: 1.8%) |
| **D** | **el juicio es fuera de muestra** | la dirección se busca en el primer 70% y se juzga en el 30% que no vio, con el mismo salto mínimo que exige `invariantes` |

## 7. LO QUE SE ESPERA, y qué se dirá EN CADA CASO
**No tengo expectativa firme**, y es la primera vez en varios estudios que puedo decir eso
honestamente: el INFORME-67 mostró que el keypoint gana en R² contra la verdad, pero **R² alto no
implica cantidad conservada** — son dos cosas distintas y ninguna implica la otra.

- **Si falla C**, se escribe que **el cuello de botella espacial no produce estructura conservada**,
  y que la mejora del INFORME-67 es de precisión, no de física.
- **Si no falla C**, se escribe que **la estructura aparece sola, sin regularizador**, y entonces
  **imponer un hamiltoniano sería aún menos defendible**: estaríamos pagando con herencia humana
  algo que sale gratis.
- **Si falla B**, se descarta todo: el diccionario grande estaría fabricando invariantes.

## 8. REGLA 31 — sobre MI PROCEDIMIENTO, los dos lados
- **Control positivo:** sobre un oscilador **hecho a mano** con invariante conocido, el buscador
  generalizado **lo encuentra**. Si no lo encuentra, el instrumento está roto.
- **Señuelo:** sobre **ruido puro**, no encuentra ninguno.
- **`SUJETO` declarado:** el sujeto son **los latentes**. La Regla 31 **no los toca**: trabaja con
  trayectorias hechas a mano.
- **Relación metamórfica con MECANISMO:** más **ruido de medida** sobre la trayectoria, peor la
  calidad del invariante — el ruido de medida se suma a lo ya ocurrido y ensucia el valor de
  cualquier cantidad conservada. **De medida y NO de proceso**: el de proceso excita el sistema y
  no entierra nada (LECCIÓN-RUIDO-01). **Base 0.001 y no 0.0.**

## 9. CUÁNDO SE ABANDONA (Regla 13, con número)
- **Si falla B —un solo invariante en el nulo— se abandona el estudio entero**, sin excepción.
- **Si falla el control positivo de la Regla 31, se abandona el instrumento**: un buscador que no
  encuentra un invariante que sí está, no puede decir nada sobre uno que no está.

## 10. LO QUE **NO** SE AFIRMA
- **Nada del universo.**
- **NO se afirma que la cantidad hallada sea «la energía».** Es **una combinación que se queda
  quieta**, sin nombre y sin unidades. Ponerle nombre sería exactamente lo que la Regla 27 prohíbe.
- **NO se entrena nada con estructura física**, ni ahora ni como consecuencia de este resultado.
- **NO se retira ningún informe anterior.**

## 11. FIRMA
Avanza por **quórum adversarial**: el **nulo puede descartar el estudio entero**, el criterio C
puede decir que el cuello de botella **no sirve para esto**, y **no declaro expectativa** porque no
la tengo. Revocable con una palabra del director.
