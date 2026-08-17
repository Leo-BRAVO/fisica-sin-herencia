# INFORME-70 — ACTA DEL PRERREGISTRO 59: el censo de los muertos encontró UNO, y de rebote destapó un sello muerto que llevaba dos días
**17 de agosto de 2026. 55 módulos examinados, ninguno movido.**
**Datos crudos:** `resultados/p59-censo-muertos/medida.json`. Módulo: `codigo/censo_muertos.py`
(puerta 8/8).
**VEREDICTO, con las palabras del archivo de datos:** *1 MODULO(S) MUERTO(S) de 55: 1
archivable(s) y 0 inmovible(s) por sello vigente.*

---

## 1. LOS NÚMEROS

| | |
|---|---|
| candidatos (ni órganos del genoma ni guardianes) | **55** |
| muertos (nadie los importa y ninguna acta los cita) | **1** — `estandarizar` |
| archivables (muertos y sin sello vigente) | **1** |
| inmovibles por sello vigente | **0** |
| línea base tonta (`grep` del nombre pelado) | **0** |
| discrepancias que el censo tuvo que justificar | **1** |

| criterio congelado | pedía | salió | |
|---|---|---|---|
| **A** encuentra lo plantado | exactamente los plantados | ✔ | ✔ |
| **B** no acusa a quien tiene cita | vivo si un acta lo cita | ✔ | ✔ |
| **C** le gana a la línea base | discrepancias con archivo y línea | **1, justificada** | ✔ |
| **D** ni un sellado entre los archivables | **cero** | **0** | ✔ |
| **E** no toca nada | solo escribe su JSON | ✔ | ✔ |

## 2. LO QUE ESTO LE HACE A LA CRÍTICA EXTERNA
El item 28 hablaba de **9 módulos huérfanos**. **Medido: 54 de 55 están vivos.** De los nueve de
aquella lista, `contratos.py` es hoy un guardián de la puerta y `invariantes.py` y `mundo.py` son
estudios de esta semana; los demás están citados por sus actas. **La lista estaba vieja, y actuar
sobre ella habría sido archivar lo que acababa de conectarse.**

> Y hay que decir qué significa «vivo» aquí, porque no es lo que parece: **significa «no se puede
> mover sin romper algo», no «se usa hoy».** Casi todos los estudios de este repositorio son
> puntos de entrada que **nadie importa jamás**; lo que los sostiene es la **cita de su acta**. Si
> el censo hubiera mirado solo el grafo de importaciones, los habría matado a todos de golpe.

## 3. EL ÚNICO MUERTO, y por qué el `grep` no lo veía
`estandarizar.py` — z-score por dimensión. El `grep` del nombre pelado lo daba por vivo porque la
palabra aparece en cuatro sitios. **Los cuatro comprobados a mano:**

| dónde | qué es realmente |
|---|---|
| `conservada.py:190` | un **comentario** que usa el verbo: «estandarizar con media/desvío…» |
| `reconstruir_datos.py:152` | un comentario: «idéntico a `estandarizar.py`» — **la lógica está copiada, no importada** |
| `mente.py:36` | una **lista escrita a mano** de módulos del lado humano |
| `registros/GIMNASIO.md:163` | prosa que **critica** la operación |

**Ninguno lo importa. Ninguna acta lo cita.** Y la única discrepancia del criterio C queda
justificada con archivo y línea, que es exactamente lo que el criterio pedía.

*(La fila de `mente.py` desapareció al archivarlo: quitarlo de `LADO_HUMANO` era parte del
archivado. Por eso el archivo de datos reconstruido lista tres sitios y esta tabla cuatro.)*

**Y hay algo mejor que «no lo usa nadie»:** el `registros/GIMNASIO.md` dice que
`estandarizar` **convierte todo a z-scores y con eso destruye la información de escala** — la
misma información de la que viven `escala.py` y `verdugo_escala.py`. No es solo peso muerto: es
una operación que este proyecto decidió no querer.

## 4. LO QUE EL CENSO DESTAPÓ SIN BUSCARLO, y es lo más grave del día
Para separar **muerto** de **archivable**, el censo preguntó por los sellos. Y al contarlos salió
esto:

> **`incertidumbre.py` selló el 15-ago-2026 a las 20:32 y la Enmienda 3 lo editó a las 20:36. El
> sello lleva DOS DÍAS muerto y nadie se enteró.**

**Por qué nadie se enteró:** `coherencia` exige sello vigente **a los estudios en cola**. Un módulo
ya integrado **y en uso** no está en la cola, así que su sello podía morir en silencio.

**Y al volver a pasar la puerta, la puerta se negó a sellarlo** — con razón:

```
FALLO paso 3 ficha de sanidad
   -> escasez: la propiedad ajena 'ruido' explica un 20.7% EXTRA de la lectura
```

**Ese 20.7% no es nuevo: es el del INFORME-60**, donde el criterio A pedía ≤15% y salió 20.7%.
**El defecto estaba publicado; lo que no estaba era la consecuencia**: G14 lleva dos días midiendo
sin sello, y la puerta hace bien en negárselo.

**Lo que esto le hace al INFORME-69:** las dos ignorancias que allí se midieron —0.0827 y
0.0776— **salieron de un instrumento contaminado en un 20.7%**. El acta 69 ya concluía en contra
de conectar `poder`, así que **el veredicto no cambia**; pero **el número sí queda marcado**, y a
partir de hoy toda acta que use G14 lo dirá.

## 5. LO QUE SE ARREGLÓ HOY, en el mismo commit
1. **`disciplina.py` mecaniza el fallo**: `d_sello_muerto_en_uso` — un sello muerto en un módulo
   que alguien importa es un **fallo del proyecto**, no un detalle. Probado por los **tres** lados:
   marca el sello muerto en uso, no marca el vigente, no marca el muerto que nadie usa.
2. **Error nº24 del catálogo**: «enmendar un módulo sellado y no volver a pasar la puerta». Al
   crecer el catálogo, **todas las lecturas previas caducaron** — el mecanismo funcionando.
3. **`incertidumbre` entra en `CON_DEFECTO_PUBLICADO`** con su acta: pasa a **deuda contada**, no a
   bloqueo mudo. Su sello **sigue muerto a propósito** y así se queda hasta que la ficha apruebe.
4. **Daño nº16 en la meta-auditoría**: se enmienda `poder.py` —sellado y en uso— en la copia, y se
   exige que `disciplina` se ponga rojo.
5. **Error nº25 y daño nº17**: «correr un instrumento con su salida por defecto y pisar los datos
   de un acta» — cometido dos veces hoy (sección 6). El daño reescribe un dato ya publicado y exige
   que `actas.py` se ponga rojo. **Los 17 daños fueron cazados.**

## 6. DOS COSAS QUE PASARON MIENTRAS SE ESCRIBÍA ESTA ACTA, y las dos van escritas

**(a) Cometí el error nº25 dos veces en una hora, y la segunda fue contra esta acta.** Corrí
`python censo_muertos.py` a secas para comprobar el archivado, y su `--salida` por defecto
**reescribió los datos de este informe**. `actas.py` lo cazó al instante — la misma frase que había
cazado el caso de `anatomia.py` veinte minutos antes. **El catálogo no me impidió repetirlo; el
guardián sí lo destapó.** Queda con `veces: 2`, que es el número honesto.

**(b) Al reconstruir la medida apareció algo que el prerregistro no previó: este censo se
invalida al publicarse.** Para regenerar los datos hubo que devolver `estandarizar.py` a `codigo/`
**y sacar este informe de `resultados/`** — porque el propio informe **cita `estandarizar.py` con
extensión**, y bajo la regla de citas eso lo declararía **vivo**.

> **Un acta que declara muerto a un módulo lo resucita con solo nombrarlo.** No es un fallo del
> detector: es la regla de citas funcionando exactamente como está escrita. Pero significa que
> **el veredicto de este censo no es re-ejecutable en sitio**: se reproduce desde el estado
> declarado —módulo en `codigo/`, acta fuera de `resultados/`— y así se reprodujo, dando otra vez
> `1 MODULO(S) MUERTO(S) de 55`. **Lo dejo escrito porque el que venga detrás va a correr el
> módulo, va a ver `0 muertos` y va a pensar que el acta mentía.**

## 7. LO QUE **NO** SE AFIRMA
- **Nada del universo.**
- **NO se afirma que los 54 vivos hagan falta.** Vivo aquí es **no se puede mover**, no **sirve**.
- **El archivado NO es parte de la medida.** `estandarizar.py` se movió a `codigo/archivo/` en el
  mismo commit, bajo la orden permanente de «limpieza de código redundante», con su nota en
  `codigo/archivo/LEEME.md` y quitándolo de `LADO_HUMANO` en `mente.py`. **Es un acto, no un
  resultado**, y se deshace con una palabra del director.
- **NO se toca `incertidumbre.py`.** Su arreglo necesita su propio prerregistro; editarlo aquí
  sería tapar el 20.7% en vez de medirlo.

## 8. LA PREGUNTA QUE ABRE (Regla 18)
> **¿Cuántas listas escritas a mano tiene este proyecto que digan lo mismo dos veces?** Hoy
> aparecieron dos: `mente.LADO_HUMANO` y `anatomia.NO_CUENTAN` describen la misma frontera —código
> del lado humano contra órganos de Diego— **y no se hablan.** Dos verdades sobre lo mismo es una
> de más, y el censo no las compara. **No lo he medido.**

## 9. LO QUE LE TOCA AL DIRECTOR
**Nada bloqueante.** El archivado de `estandarizar.py` se hizo bajo su orden permanente de limpieza
—no tenía sello que romper y no lo importa nadie— y **se revierte con una palabra**.

Lo que sí queda esperándole es lo de siempre, y hoy con un motivo más:
- **`incertidumbre` mide sin sello** y su ficha reprueba por el 20.7% del INFORME-60. Arreglarlo
  necesita **un prerregistro nuevo**, no una edición. **Mientras no lo autorice, G14 sigue midiendo
  y cada acta que lo use lo dirá.**
