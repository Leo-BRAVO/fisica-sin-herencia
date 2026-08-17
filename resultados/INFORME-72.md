# INFORME-72 — ACTA DEL PRERREGISTRO 62: con el rival correcto, el lazo gana — y el criterio era fácil, como dije antes de correrlo
**17 de agosto de 2026. Las mismas regiones del INFORME-69, contra el reparto de quien no sabe
nada.**
**Datos crudos:** `resultados/p62-lazo2/medida.json`. Módulo: `codigo/lazo2.py` (puerta 8/8).
**VEREDICTO, con las palabras del archivo de datos:** *EL LAZO LE GANA AL RIVAL TRIVIAL — la región
buena se lleva 9.758 contra el 5.0 del uniforme y el televisor 0.242 contra el mismo 5.0. `poder`
queda listo para conectarse, con el 20.7% de G14 escrito.*

---

## 1. LOS NÚMEROS

| región | `curable` (G14) | `poder` (G13) | recibe | el uniforme le habría dado |
|---|---|---|---|---|
| **buena** | 0.0827 | **0.2328** | **9.758** | 5.0 |
| **televisor** | 0.0776 | 0.0 | **0.242** | 5.0 |

| criterio congelado | pedía | salió | |
|---|---|---|---|
| **A** los órganos miden | ni un número a mano | ✔ | ✔ |
| **B** el televisor pierde | por debajo del techo congelado en el prerregistro 49 | **0.242** | ✔ |
| **C** la buena gana | por encima del piso congelado en el prerregistro 49 | **9.758** | ✔ |
| **E'** le gana al uniforme | buena > 5.0 **y** tv < 5.0 | **9.758 / 0.242** | ✔ |
| **F** el uniforme es ciego | no mira ninguna medida | ✔ | ✔ |

## 2. LO QUE ESTO CORRIGE, y lo que no
**Corrige el rival, no el resultado.** El INFORME-69 midió exactamente estos mismos números; lo
único que estaba mal era **contra quién los comparaba**. Puse mis propios 0.30 y 0.10 —una
diferencia **tres veces mayor** que la real— en el papel de «línea base tonta», y perdí contra mi
propia suposición optimista por **9.758 frente a 9.875**.

**Contra el rival que pide la Regla 11 —el uniforme, 5.0 y 5.0— el lazo gana por goleada.**

> **Y lo dije antes de correrlo: este era el prerregistro más flojo de la serie.** Su criterio
> principal ya se sabía que iba a aprobar. **Su valor no está en el resultado sino en poner el
> rival correcto donde puse el equivocado**, y en que quede escrito que el error no fue del lazo.

## 3. LO QUE ARRASTRA, y va en el acta porque va en los datos
**Todo `curable` de esta tabla sale de `incertidumbre.py`, que mide SIN SELLO VIGENTE y cuya ficha
reprueba: la propiedad ajena «ruido» explica un 20.7% extra de la lectura, cuando el criterio pedía
≤15% (INFORME-60).**

Está escrito **dentro del archivo de datos**, no solo aquí. Y tiene una consecuencia concreta:

> **Si ese defecto se arregla algún día, este resultado hay que rehacerlo.** No porque el reparto
> vaya a cambiar de signo —lo que separa las dos regiones es `poder`, 0.2328 contra 0.0, no
> `curable`— sino porque **un número de un instrumento contaminado no se hereda sin volver a
> mirarlo**.

## 4. LO QUE ESTO HABILITA
**`poder` queda listo para conectarse al lazo de producción**, con el 20.7% escrito al lado. Pero
**conectarlo es un acto, no un resultado**: cablear un órgano al lazo que decide el gasto de
atención de Diego **es otro prerregistro**, y hasta que exista, `poder` sigue midiendo sin decidir
—el mismo blindaje de activación que lleva desde el 8 de agosto—.

## 5. LO QUE **NO** SE AFIRMA
- **Nada del universo.**
- **NO se retira el INFORME-69.** Aquel acta midió bien y comparó mal, y las dos cosas están
  escritas en él.
- **NO se limpia el error nº21 del catálogo.** Un catálogo no se limpia rehaciendo un estudio: el
  incidente queda, con sus números, para siempre.
- **NO se afirma que `poder` mida bien el empowerment.** Se afirma que el lazo lo usa y que su
  número es el que separa las dos regiones.
- **NO se tocó `lazo_atencion.py`, `poder.py`, `incertidumbre.py` ni `atencion.py`.**

## 6. LA PREGUNTA QUE SIGUE ABIERTA (Regla 18)
> **¿Cuántas de mis «líneas base tontas» son en realidad suposiciones mías?** La abrió el
> INFORME-69 y **este acta no la cierra**: arregla **una**. Las demás siguen sin revisarse, y
> revisarlas es mecánico.
