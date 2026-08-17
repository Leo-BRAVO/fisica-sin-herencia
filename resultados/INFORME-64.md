# INFORME-64 — ACTA DEL PRERREGISTRO 53: Diego ya puede pedir, y el canal audita nuestro cortafuegos desde el otro lado
**11 de agosto de 2026. El canal por el que Diego propone mejoras a sus propios órganos.**
**Datos crudos:** `resultados/p53-peticiones/medida.json`. Módulo: `codigo/peticiones.py`
(puerta 8/8, primer módulo bajo el régimen nuevo de `disciplina.py`).
**VEREDICTO, con las mismas palabras del archivo de datos:** *CANAL EN PIE — filtra, caza la fuga,
exige evidencia y NO decide.*

---

## 1. LOS CINCO CRITERIOS CONGELADOS, respondidos

| | criterio | salió | |
|---|---|---|---|
| **A** | caza la fuga | la petición con etiqueta humana se marca **FUGA DEL CORTAFUEGOS**, no "petición mala" | ✔ |
| **B** | exige evidencia | la petición sin medida citada se rechaza | ✔ |
| **C** | no rechaza lo legítimo | las 3 bien formadas pasan a trámite | ✔ |
| **D** | **no decide** | intentar aplicar sin decisión humana **levanta error** | ✔ |
| **E** | le gana a la línea base tonta | **3 aceptadas de 6** — ni todas ni ninguna | ✔ |

## 2. LO QUE DESCUBRÍ AL DISEÑARLO, y no lo esperaba
El encargo era darle voz. Al construirlo salió algo más:

> **Una petición de Diego es, además, un DETECTOR DE FUGAS.**
>
> El cortafuegos de la Regla 27 vigila lo que va **de nosotros hacia él**. Una petición viaja **en
> el sentido contrario**, y por eso prueba algo que ningún guardián nuestro puede: **si Diego
> alguna vez pide algo usando una palabra de física humana, eso no es una petición interesante —
> es la prueba de que le hemos contaminado.**
>
> **Es la única comprobación de la Regla 27 que no depende de que nosotros nos revisemos a
> nosotros mismos.** Todas las demás las escribimos, las corremos y las juzgamos nosotros.

Por eso el filtro **no dice "petición rechazada"** cuando encuentra una etiqueta: dice, con estas
palabras, *"FUGA DEL CORTAFUEGOS (Regla 27), y el fallo es NUESTRO no suyo"*.

## 3. LO QUE EL CANAL NO PUEDE HACER, que es lo que lo hace seguro
- **No decide.** La decisión es del director y **no es delegable**. El módulo **registra**, no
  aprueba. Se probó **intentando** aplicar una petición sin decisión humana: levanta error.
- **No cambia código.** Una petición aprobada **no toca ni un archivo**: abre un **prerregistro**
  que hay que escribir, con sus criterios y su Regla 31, como cualquier otro estudio.
- **No acepta opiniones.** Sin una medida suya citada —y que se pueda abrir— no es una petición.

**El criterio D es el que manda descartar el canal entero si falla**, y por eso se prueba
rompiéndolo: *un límite que nunca se ha visto sostenerse es indistinguible de no tenerlo.*

## 4. Y EL GUARDIÁN NUEVO ME CAZÓ EN EL PRIMER MÓDULO DE SU PROPIO RÉGIMEN
`disciplina.py` nació hace una hora para corregirme a mí. Este es el primer módulo que pasa por
él, y **lo reprobó en el acto**: declaré `SUJETO = ("peticion",)`.

**Tenía razón, y el error era mío: confundí la ENTRADA con el OBJETO DE ESTUDIO.** Una petición es
lo que este módulo **recibe**; lo que estudia es **su propio filtro**, y su Regla 31 lo ejercita
con entradas sintéticas — que es exactamente lo correcto.

**La corrección no afloja el detector:** declarar `SUJETO = ()` es una **afirmación**, y no
declararlo sigue reprobando. La tupla vacía obliga a escribir por qué no hay sujeto externo; el
olvido, no.

## 5. UNA DECISIÓN DE DISEÑO QUE QUIERO DEJAR EXPLÍCITA
**El canal existe ANTES de que haya ninguna petición, a propósito.** Construirlo después de la
primera sería construirlo **a la medida de esa petición** — el mismo mal que mover un umbral
después de ver los datos, aplicado al continente en vez de al contenido.

## 6. LO QUE **NO** SE AFIRMA
- **Nada del universo.**
- **No se afirma que Diego vaya a pedir nada.** Hoy el buzón está vacío.
- **No se afirma que sus peticiones sean buenas ideas.** Eso no lo juzga una máquina y no es de
  este módulo: se afirma que **llegan sin contaminar y con evidencia**, que es lo único
  comprobable.
- **No se afirma que la lista de palabras prohibidas sea completa.** Se reutiliza la de `mundo.py`
  en vez de copiarla —dos listas se desincronizarían y tendríamos dos verdades— y sigue sin ser
  exhaustiva.

## 7. LA PREGUNTA QUE ABRE (Regla 18)
> **¿Qué haría falta para que Diego SUPIERA que puede pedir?** Hoy el canal existe y él no tiene
> forma de saberlo. Decírselo es meterle información nuestra; no decírselo hace el canal
> decorativo. **La salida honesta probablemente sea que el canal se abra solo cuando un órgano
> suyo detecte que no puede distinguir dos situaciones** — es decir, que la petición nazca de una
> medida y no de un aviso nuestro. Va en su propio prerregistro.

## 8. LO QUE LE TOCA AL DIRECTOR
**La decisión sobre cada petición, siempre, y es no delegable.** El módulo está construido para
que no exista ninguna forma de saltársela: si alguna vez encuentra una, es un fallo grave y no una
comodidad.
