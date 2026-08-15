# INFORME-58 — ACTA DEL PRERREGISTRO 47: la alucinación está muerta, y el arreglo abrió una puerta y cerró otra
**11 de agosto de 2026. 25 escalas × 5 semillas nuevas × 2 sistemas × 2 motores, más 25 casos de
señal casi constante. Semillas: 47, 53, 59, 61, 67.**
**Datos crudos:** `resultados/p47-arreglo/medida.json` y, para el diagnóstico de la §5,
`resultados/p47-arreglo/diagnostico.json`. Módulos: `codigo/sindy4.py`, `codigo/arreglo_motor.py`
(sellado, puerta 7/7) y `codigo/diag_p47.py`.
**VEREDICTO, con las mismas palabras del archivo de datos:** *ARREGLA UNO SOLO — deja de alucinar
pero siguen los agujeros.*

---

## 1. LOS CUATRO CRITERIOS CONGELADOS, respondidos

| | criterio | pedía | salió | |
|---|---|---|---|---|
| **A** | agujeros cerrados | **un tramo** en los **dos** sistemas, ≥5 décadas | oscilador **1 tramo / 5.5 décadas** ✔ · caída con roce **0 tramos** ✘ | ✘ |
| **B** | alucinación muerta | **0 leyes en 25 de 25** | **0 de 25** | ✔ |
| **C** | no se rompió nada | `sindy4` conserva los 4 casos de `sindy3` | **4 de 4** | ✔ |
| **D** | el defecto es del motor | `sindy3` sigue fallando con las semillas nuevas | **3 tramos en los dos sistemas y 24 alucinaciones de 25** | ✔ |

## 2. LA ALUCINACIÓN ESTÁ MUERTA, y el número es limpio
Sobre señal casi constante —donde **no hay ninguna ley que hallar**:

| motor | leyes declaradas |
|---|---|
| `sindy3` | **24 de 25** |
| `sindy4` | **0 de 25** |

**El INFORME-54 queda replicado con semillas nuevas** (declaraba 20 de 25; con estas cinco son 24)
**y el defecto queda eliminado.** La guarda que lo mata no es la de condición sino la **línea base
tonta fuera de muestra**: sobre una señal plana, el modelo que solo usa el término constante lo
explica todo, así que ninguna ley puede ganarle por 0.10 y el motor **queda obligado a callar**.
Es la Regla 12 —la que le exigimos a cada prerregistro— aplicada por fin al corazón del proyecto.

## 3. EL CRITERIO D: el INFORME-55 queda confirmado, no desmentido
Este criterio existía para dejarme mal. `sindy3`, sobre **semillas que nunca había visto**, vuelve
a dar **tres tramos separados en los dos sistemas**. **El defecto era del motor y no de las
semillas.** Se declaró antes de correr que si `sindy3` salía limpio, la conclusión sería *"el
INFORME-55 estaba equivocado"*. No hizo falta.

## 4. LO QUE DE VERDAD PASÓ CON LOS AGUJEROS — y por qué el rótulo del veredicto se queda corto
**El veredicto congelado es el que es y no lo toco.** Pero el rótulo que yo mismo escribí en el
código —*"siguen los agujeros"*— **describe mal lo ocurrido**, y el acta tiene que decirlo:

**Oscilador amortiguado**
```
sindy3  [5,5,5,5,2,0,0,0,0,1,3,5,5,5,5,5,5,5,3,2,2,1,3,4,5]   3 tramos, 1.5 décadas
sindy4  [0,0,4,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5]   1 tramo, 5.5 décadas
```
**En el oscilador los agujeros no siguen: se cerraron, y de forma espectacular.** De tres tramos
que cubrían 1.5 décadas a **un solo tramo continuo de 5.5 décadas**. La zona muerta de 10⁻¹·⁵ que
el INFORME-55 encontró **ha desaparecido**. **El corte adimensional hizo exactamente lo que el
DIAGNOSTICO-MOTOR-01 predijo que haría.**

**Caída con roce**
```
sindy3  [2,4,4,4,3,3,2,1,2,2,5,5,5,3,3,2,3,4,5,5,5,5,5,5,5]   3 tramos, 1.75 décadas
sindy4  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]   CALLA EN LAS 25
```
**Aquí no hay agujeros: hay silencio total.** `sindy4` no ve ese sistema en ninguna escala.
**El criterio A falla por esto, no por lo otro**, y las dos cosas no son el mismo defecto.

## 5. POR QUÉ CALLA — medido, no supuesto
Diagnóstico sobre la semilla 47, escala ×1 (`diagnostico.json`):

| | oscilador | caída con roce |
|---|---|---|
| **condición de la matriz** | 10.6 | **1434996.3** (por encima del tope de 1000000.0) |
| **recorrido de x** | [-0.96, 1.0] | **[-0.01, 220.6]** |
| **recorrido de v** | [-0.92, 0.86] | [0.0, 2.9] |

**Estas cifras las cazó el auditor de actas antes que nadie.** La primera versión de este informe
las publicaba medidas a mano, sin archivo detrás — **el mal exacto del INFORME-48**. El auditor lo
marcó, y por eso existe `diag_p47.py`: para que estén en disco y se puedan volver a calcular.

Y subiendo el tope a 10¹² **sigue callando**, así que la guarda de condición no es la única causa.
El soporte que encuentra es `dx/dt = v` **(correcto)** y `dv/dt = 1 + x + xv` **(la ley verdadera
es `1 − 0.35·v`)**: acierta el término constante, mete dos términos falsos y **pierde el
amortiguamiento**, cuyo CP se queda en 2.5, justo por debajo del piso de 3.0.

**Lo que lo detiene es la línea base tonta fuera de muestra:** los márgenes salen **+33.66** en la
primera ecuación y **−62.44** en la segunda. La segunda ecuación **predice mucho peor que decir
"la derivada no depende de nada"**, y el motor se niega a declararla.

> **`sindy4` no está ciego: sabe que su respuesta es mala y se calla.** Eso es un fallo **seguro**
> —prefiere no decir nada antes que decir algo falso— y es preferible a lo que hacía `sindy3`,
> que sobre este mismo sistema declaraba leyes en 3 tramos sin comprobar jamás si predecían. Pero
> **sigue siendo un fallo, y el criterio A lo cuenta como fallo.**

**La causa de fondo, y es honesta:** en este sistema **x crece sin límite hasta 220** mientras `v`
se satura cerca de su velocidad terminal. Normalizar cada columna por su norma **no basta cuando
una coordenada es una rampa**: la columna queda dominada por los tiempos finales. **La
adimensionalización que arregla el oscilador no arregla un sistema con una coordenada no acotada.**

## 6. EL AGUJERO DE MI PROPIO CRITERIO C — que no me protegió
**El criterio C pasó 4 de 4 y aun así no vio venir esto.** La razón es mía: **sus cuatro casos son
todos de la familia del oscilador** (limpio, ruidoso, barajado y ruido puro). Un criterio de "no
rompimos nada" construido solo con casos parecidos entre sí **no puede detectar que rompimos algo
en una familia distinta.**

Es el mismo mal, en su quinta aparición este mes: el criterio 4 tautológico del prerregistro-41,
los chequeos que aprueban sobre listas vacías, la confianza 1.0 sobre un sistema degenerado, la
relación metamórfica falsa del prerregistro-46 — **y ahora un control de regresión que no cubre lo
que dice cubrir.** **No lo arreglo aquí:** cambiar el criterio C después de ver los datos es
exactamente lo único que el director se reservó. Va en el prerregistro siguiente.

## 7. LO QUE **NO** SE AFIRMA
- **Nada del universo.** Es una propiedad de nuestro código.
- **No se declara arreglado el motor.** Un defecto de dos murió; el otro cambió de forma.
- **No se dice qué resultados nuestros quedan tocados.** Es la Fase 2 y exige medir campaña por
  campaña. **Y ahora hay una razón más para hacerla:** `sindy4` calla donde `sindy3` hablaba, así
  que la revisión puede quitar hallazgos además de añadirlos.
- **No se toca ningún criterio, ni el rótulo del veredicto, ni ningún umbral.**
- **No se afirma que el piso de CP de 3.0 sea correcto.** Con 2.5, el amortiguamiento verdadero se
  queda fuera por poco. Cambiarlo ahora sería moverlo después de ver los datos.

## 8. LAS PREGUNTAS QUE ABRE (Regla 18)
> **¿Cómo se adimensionaliza un sistema con una coordenada no acotada?** Normalizar por la norma de
> la columna funciona cuando la señal es estacionaria y falla cuando es una rampa. Hay respuestas
> conocidas —trabajar con incrementos, con ventanas locales, o normalizar por ventana en vez de por
> serie— y cada una es un estudio con su propia Regla 31.
>
> **¿Y cuánto vale un motor que calla?** `sindy4` cambió falsos positivos por silencio. Para un
> proyecto cuya regla primera es no afirmar de más, **puede que sea el intercambio correcto** — pero
> es una decisión, no un hecho, y se toma con números delante.

## 9. LO QUE LE TOCA AL DIRECTOR
Ninguna decisión urgente. Un aviso: **la Fase 2 (revisar las 67 corridas) ya no es solo una
oportunidad de recuperar hallazgos perdidos. Con este motor también puede quitarlos**, porque
`sindy4` se niega a declarar leyes que no predicen fuera de muestra. Se publicará igual, como se
congeló antes de mirar.
