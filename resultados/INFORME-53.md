# INFORME-53 — EL TORNEO DE LOS OJOS CORRIÓ POR FIN, y corona a un ganador a escala de ruido
**10 de agosto de 2026. Acta parcial del prerregistro-38 (4 de 5 semillas; la 5ª en curso).**
**Datos crudos:** `resultados/p38-torneo-panel-s2/resumen.json`,
`resultados/p38-torneo-panel-s3/resumen.json`, `resultados/p38-torneo-panel-s4/resumen.json`,
`resultados/p38-torneo-panel-s5/resumen.json`, y el agregado con la calibración de la vara en
`resultados/p38-veredicto/veredicto.json`. Módulo sellado: `codigo/torneo_ojos.py`.

---

## 1. PRIMERO, LO QUE COSTÓ LLEGAR AQUÍ
Estos 5 estudios llevaban días **parados por LA PUERTA**: `torneo_ojos.py` no tenía manifiesto, ni
fórmulas comprobables, ni ficha de sanidad, ni Regla 31 propia. Al construírselos y correrlo,
apareció **un bug que lo tenía roto**: `corromper()` convertía los vídeos a `float64` y los
codificadores son `float32`, así que **la lectura de ROBUSTEZ —una de las tres del veredicto— nunca
había podido correr con vídeo de verdad.** Arreglado, y añadido como caso congelado.

**La puerta no retrasó este estudio: impidió que se corriera roto por segunda vez.**

## 2. LOS NÚMEROS (4 semillas)

| competidor | contingencia | flecha | robustez |
|---|---|---|---|
| A-pixel | +0.00541 | −0.02057 | −0.00046 |
| B-predictivo | +0.00168 | −0.01378 | +0.00081 |
| C-corolario | +0.00161 | −0.01262 | +0.00146 |
| **R-ranuras** | **+0.00710** | **−0.01098** | +0.00002 |

**Veredicto formal de la regla de oro del panel, aplicada tal como está congelada:**
> *GANA CON ASTERISCO R-ranuras — gana en contingencia y flecha, pierde en robustez; NO reemplaza
> los ojos oficiales sin segunda vuelta.*

## 3. Y AHORA LO QUE DE VERDAD DICE ESA TABLA
La vara tiene calibración propia, medida en su Regla 31 el mismo día:

| qué se le da a la vara | contingencia que devuelve |
|---|---|
| latentes que **sí obedecen** a los comandos | **+0.412** |
| latentes de **puro ruido** | **−0.0002** |
| **los cuatro competidores reales** | **entre −0.002 y +0.014** |

**Los cuatro están en el rango del ruido, no en el de la señal.** El "ganador" gana por
**+0.00710 contra +0.00541**, con un margen automático de **0.00027**. Y el signo de las lecturas
**cambia de semilla a semilla** (A-pixel va de +0.0132 en la 2 a −0.0014 en la 4).

**Lectura honesta: ninguna de las cuatro arquitecturas produce latentes que sirvan para hallar el
cuerpo.** No es que una gane: es que ninguna despega.

## 4. EL DEFECTO QUE ESTO DESTAPA EN LA REGLA DE ORO — y es del panel, no de los competidores
`panel_jueces.veredicto()` usa, cuando no se le dan márgenes, **el 5% del rango observado** en cada
lectura. Es una regla **sin escala absoluta**: si todos los competidores están en el ruido, el rango
también es ruido, el margen se encoge con él, **y el panel corona igualmente a alguien.**

> **Una regla de veredicto que siempre produce un ganador no puede distinguir "el mejor" de
> "ninguno sirve".** Es el mismo mal que ya cazamos hoy tres veces: un criterio que no puede
> devolver "nada".

**No se toca hoy.** El arreglo probable —exigir que el ganador supere un **piso absoluto** calibrado
contra la propia Regla 31 de la vara (que sabe cuánto vale el ruido: −0.0002, y cuánto la señal:
+0.412)— cambia cómo se decide un torneo, y eso va con prerregistro propio. Cambiarlo ahora, con
este resultado delante, sería mover el criterio después de ver los datos.

## 5. QUÉ SE AFIRMA Y QUÉ NO
**Se afirma:**
- El torneo **por fin corre entero**, con sus tres lecturas, incluida la robustez que nunca había
  funcionado.
- **Los cuatro competidores puntúan a escala de ruido** en las tres lecturas, con la calibración de
  la propia vara como referencia.
- El veredicto formal, tal cual salió, corona a R-ranuras **con asterisco**.

**NO se afirma:**
- **Que R-ranuras sea mejor.** Ganar dentro del ruido no es ganar.
- **Que los ojos de Diego no sirvan para nada.** Sirven para reconstruir la escena (sus pérdidas de
  entrenamiento bajan). Lo que esta medida dice es que **no codifican el cuerpo de forma que la
  contingencia lo encuentre** — que es lo mismo que el INFORME-38 sospechaba, pero entonces se
  atribuyó al instrumento y **ahora el instrumento está validado**.
- **Ningún nodo.** Esto es sobre arquitecturas nuestras, no sobre el universo.
- **Ningún cambio de genoma.** R-ranuras no reemplaza a nadie (Regla 33: eso exige firma, y además
  aquí no hay evidencia que lo sostenga).

## 6. LA PREGUNTA QUE ABRE (Regla 18)
> **Si ninguna de las cuatro arquitecturas codifica el cuerpo, ¿el problema es la arquitectura o es
> que el cuerpo no se ve desde donde mira la cámara?** Es una pregunta distinta de la que este
> torneo hacía, y se contesta comparando contra un control que SÍ tenga el cuerpo dentro (por
> ejemplo, propiocepción directa) para saber si el techo es del ojo o de la escena.

## 7. LA DECISIÓN QUE LE TOCA AL DIRECTOR
Ninguna urgente. Pero conviene que sepa que **el prereg-27 quedó "no concluyente por instrumento",
se construyó un panel nuevo para arreglarlo, y la segunda vuelta dice que el problema no era del
todo el instrumento**: la vara nueva funciona y mide, y lo que mide es que ninguna de las cuatro
opciones despega. Eso es un resultado, aunque no sea el que buscábamos.
