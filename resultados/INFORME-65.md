# INFORME-65 — ACTA DEL PRERREGISTRO 54: cuatro órganos de Diego no están conectados a nada
**11 de agosto de 2026. El censo de los 15 órganos del genoma: conexión, efecto, unicidad y
atribución.**
**Datos crudos:** `resultados/p54-anatomia/medida.json`. Módulo: `codigo/anatomia.py` (puerta 8/8).
**VEREDICTO, con las mismas palabras del archivo de datos:** *HAY 4 ORGANO(S) DESCONECTADO(S) y 0
numero(s) duplicado(s) — el censo le gana a la suposicion de que todos hacen falta.*

---

## 1. LOS CUATRO CRITERIOS CONGELADOS

| | criterio | salió | |
|---|---|---|---|
| **A** | el censo distingue | encuentra el huérfano plantado y no inventa ninguno donde no los hay | ✔ |
| **B** | no acusa por no estar sellado | el censo **no mira los sellos**, a propósito | ✔ |
| **C** | la atribución se mide | los 15 reciben tipo derivado del código; **0 chocan** con lo declarado | ✔ |
| **D** | le gana a la línea base tonta | **4 huérfanos**. La suposición de que todos hacían falta era falsa | ✔ |

## 2. LOS CUATRO DESCONECTADOS
**`curiosidad2` · `interocepcion` · `memoria` · `poder`** — ningún módulo que no sea una prueba o
un guardián los importa.

Y **comprobé a mano que no se usan por nombre dinámico** antes de publicarlo, porque ése habría
sido exactamente el mismo falso positivo que este mismo día tuve que corregir en otro detector.
Las únicas menciones que existen son las listas de `peticiones.py`, escritas hoy.

## 3. EL CASO DE `poder`, que me contradice a mí mismo
En la `INVESTIGACION-01` escribí, hace unas horas, que `poder.py` era *"probablemente la pieza más
valiosa e infrautilizada del repositorio"*. **Ahora está medido, y era peor de lo que dije: no
está infrautilizada. No se usa en absoluto.**

Y el detalle es más fino que el conteo: **`atencion.py` sí usa la idea de poder** —su prioridad es
`curable · poder`— **pero nunca importa `poder.py`.** El número le llega **escrito a mano en los
casos de prueba**.

> **La Fase 3 arregló la cadena G14→G8 con empowerment, y el órgano que mide el empowerment sigue
> desconectado del lazo.** El concepto entró; el órgano no. Es exactamente la clase de hueco que
> un censo encuentra y una lectura del código no.

## 4. `interocepcion`, que es el que más me preocupa
Es el sentido que Diego tiene **de sí mismo** — su propiocepción. **Nadie lee lo que publica.**
Junto con el INFORME-57 —donde su brazo no alcanzaba nada— dibuja algo incómodo: **de los tres
órganos que tocan el cuerpo, uno mide un cuerpo que no llega al mundo y otro publica para nadie.**

## 5. LO QUE **NO** SE AFIRMA, y aquí importa mucho
- **NO se afirma que estos cuatro órganos deban borrarse.** Un órgano desconectado **puede estar
  esperando a que lo conecten**, y tres de estos cuatro tienen trabajo hecho detrás. El censo dice
  **qué está desconectado hoy**, no qué merece existir.
- **NO se afirma que los 11 conectados funcionen.** Estar en el lazo no es hacerlo bien: eso lo
  dice su ficha de sanidad, y **8 de los 15 ni siquiera la tienen** (INFORME-63).
- **NO se ha tocado ni borrado ningún órgano.** Este estudio **solo mide**.
- **NO se afirma que 0 duplicados signifique que no hay redundancia.** El censo compara **nombres
  de lo que se publica**, y solo dos órganos tienen contrato declarado. **Dos órganos podrían
  calcular lo mismo con nombres distintos y este censo no lo vería** — es un límite del método,
  no un resultado.
- **Nada del universo.**

## 6. LA PREGUNTA QUE ABRE (Regla 18)
> **¿Por qué se construyeron cuatro órganos que nadie llegó a conectar?** No es una pregunta
> retórica: los cuatro tienen código serio detrás. La respuesta probable es que **el proyecto
> avanzó por estudios y no por lazo** — cada prerregistro construía lo que necesitaba y nadie
> volvía a cerrar el circuito. **Si eso es cierto, el censo hay que repetirlo cada vez, no una
> sola.**

## 7. LO QUE LE TOCA AL DIRECTOR
**Una decisión por órgano, y son cuatro:**

| órgano | qué es | mi recomendación, y es solo eso |
|---|---|---|
| **`poder`** | mide empowerment | **conectarlo ya**: la Fase 3 usa su idea con números a mano |
| **`interocepcion`** | el sentido de sí mismo | **conectarlo**, junto con la decisión pendiente sobre el cuerpo |
| **`memoria`** | guarda lo vivido | conectar o archivar — no tengo medida que lo decida |
| **`curiosidad2`** | qué explorar | **esperar**: depende de la epistémica de G14, que acaba de cambiar |

**Ninguna de las cuatro la tomo yo.** Y si decide archivar alguno, se archiva **con acta**, no
borrándolo: el trabajo hecho y el motivo de retirarlo valen tanto como el código.
