# INFORME-69 — ACTA DEL PRERREGISTRO 58: el lazo funciona, y mi «línea base tonta» no era tonta sino favorable
**11 de agosto de 2026. `poder` e `incertidumbre` midiendo de verdad, sin un solo número escrito
a mano.**
**Datos crudos:** `resultados/p58-lazo/medida.json`. Módulo: `codigo/lazo_atencion.py` (puerta 8/8).
**VEREDICTO, con las mismas palabras del archivo de datos:** *MEDIR DE VERDAD NO MEJORA EL REPARTO
— `poder` sigue desconectado, y ahora con esa razon escrita.*

---

## 1. LOS NÚMEROS

| región | `curable` (medido por G14) | `poder` (medido por el órgano) | recibe |
|---|---|---|---|
| **buena** | 0.0827 | **0.2328** | **9.758** |
| **televisor** | 0.0776 | **0.0** | **0.242** |

| criterio congelado | pedía | salió | |
|---|---|---|---|
| **A** los órganos miden | ni un número a mano | ✔ | ✔ |
| **B** el televisor pierde | por debajo del techo congelado en el prerregistro 49 | **0.242** | ✔ |
| **C** la buena gana | por encima del piso congelado en el prerregistro 49 | **9.758** | ✔ |
| **D** el contrato se respeta | rango [0,1] verificado | ✔ | ✔ |
| **E** le gana a mis números | la buena no recibe menos | **9.758 < 9.875** | ✘ |

## 2. EL HALLAZGO QUE IMPORTA, y está en la primera tabla
**Las dos ignorancias medidas son casi idénticas: 0.0827 y 0.0776.**

> **G14 por sí solo NO habría distinguido la región buena del televisor.** Lo que las separa
> —enteramente— es el **empowerment: 0.2328 contra 0.0.**

**Ése es el argumento entero para conectar `poder`**, y no lo tenía antes: hasta hoy sabía que el
órgano estaba desconectado; ahora sé que **es el único factor que separa las dos regiones.** Sin
él, la prioridad `curable · poder` se quedaría en dos números casi iguales y el reparto sería casi
uniforme.

## 3. POR QUÉ FALLA EL CRITERIO E, y el error es mío
**Mi «línea base tonta» eran mis propios números escritos a mano: `curable` 0.30 para la buena y
0.10 para el televisor.** La realidad medida es **0.0827 y 0.0776** — mucho menos separadas.

**Yo había inventado una diferencia tres veces mayor de la que existe.** Así que el criterio E no
comparaba contra un rival tonto: **comparaba contra una ficción favorable que yo mismo escribí.**

> Una línea base tonta tiene que ser **tonta**, no **cómoda**. La correcta aquí era el **reparto
> uniforme** —5.0 y 5.0—, y contra ése el lazo medido gana por goleada. **Elegí como rival mi
> propia suposición optimista, que es justo lo que el estudio venía a desmontar.**

**Y aun así no toco el criterio.** Falla, el veredicto se queda, y `poder` **sigue formalmente
desconectado** hasta que un estudio con la línea base correcta diga otra cosa. **Mover E ahora
sería premiarme por haberlo elegido mal.**

Queda en `disciplina.py` como **error nº21: «línea base tonta que no es tonta, sino favorable»**.

## 4. LO QUE SÍ QUEDA DEMOSTRADO
- **El lazo se puede cerrar.** Los dos órganos miden, el contrato aguanta, y **ni un número lo
  escribo yo**.
- **El televisor pierde igual: 0.242 de 10.** La reparación de la Fase 3 **sobrevive** al pasar de
  mis números a medidas reales — que era el riesgo verdadero de este estudio.
- **`poder` es el que hace el trabajo.** Medido, no supuesto.

## 5. LO QUE **NO** SE AFIRMA
- **NO se conecta `poder` al lazo de producción.** El criterio E falla y eso manda.
- **NO se afirma que `poder` mida bien el empowerment**; se afirma que el lazo lo usa y que su
  número es el que separa. Que la medida sea correcta lo dice su ficha, y esa **sí** la pasó.
- **NO se toca `poder.py` ni `atencion.py`.** Los dos están sellados.
- **Nada del universo.**

## 6. LA PREGUNTA QUE ABRE (Regla 18)
> **¿Cuántas de mis «líneas base tontas» son en realidad suposiciones mías?** La Regla 11 pide un
> rival trivial, y hoy descubrí que en un caso puse **mi propia hipótesis** en ese papel. **Revisar
> las demás es mecánico y no lo he hecho.**

## 7. LO QUE LE TOCA AL DIRECTOR
Una decisión pequeña y concreta: **el estudio que corrija la línea base es de tres líneas** —
cambiar el rival por el reparto uniforme— **pero es un prerregistro nuevo, no una edición de éste.**
Si lo autoriza, `poder` se conecta con evidencia limpia. **Si no, se queda desconectado y el motivo
queda escrito.**
