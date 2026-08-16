# Prerregistro 51 — EL SUELO ABSOLUTO DE LA REGLA DE ORO — 11 de agosto de 2026
**Fase 5 del PLAN MAESTRO 01, requisito previo. Peldaño (Regla 9): Fase 1 — propiedad de nuestro
código, no del universo.**
**Estado: FIRMADO antes de tocar `panel_jueces.py`.**

---

## 0. EL DEFECTO, y por qué va ANTES del segundo motor
`veredicto()` compara a los competidores **solo entre sí**: toma el mejor de cada lectura y corona
a quien gana o empata en las tres. **No hay ningún suelo absoluto en ninguna parte.**

**Consecuencia medida:** en el torneo de ojos, **las cuatro arquitecturas puntuaron a escala de
ruido** —la vara calibrada da **+0.412** con latentes obedientes y **−0.0002** con ruido puro— y
aun así el panel tenía que nombrar a alguien. **Un torneo siempre da campeón, exista o no mérito.**

**Por eso va antes que el segundo motor:** meter un competidor nuevo a un torneo que corona pase lo
que pase produciría un ganador sin significado, y encima parecería un resultado.

## 1. LA PREGUNTA
> ¿Puede el panel **negarse a coronar** cuando nadie supera un suelo declarado de antemano — y
> negarse también cuando **nadie ha declarado el suelo**?

## 2. LO QUE SE CAMBIA
`veredicto()` acepta **`pisos`**: el valor mínimo, **por lectura**, que un competidor debe superar
para considerarse que compite. Y:

1. **Si nadie supera el piso en una lectura**, esa lectura **no corona a nadie**.
2. **Si nadie supera el piso en ninguna lectura**, el veredicto es **NINGUNO SUPERA EL SUELO**.
3. **Si no se declara ningún piso**, el panel **no corona**: el veredicto pasa a decir que se
   compitió **sin suelo declarado**, y eso **no es una victoria**.

**El punto 3 es el que de verdad importa**, y es incómodo a propósito: **obliga a que alguien
escriba el número antes de correr el torneo.** Un suelo que se elige después de ver los puntajes
no es un suelo.

## 3. DE DÓNDE SALEN LOS PISOS — y por qué no los invento aquí
**No se fija ningún número en este prerregistro para los torneos futuros.** El piso lo declara cada
torneo en su propio prerregistro, con su calibración. Lo que sí queda es **de dónde tiene que
salir**: de una **vara calibrada con los dos extremos medidos** — qué marca algo que sí obedece y
qué marca ruido puro. La del torneo de ojos ya existe: **+0.412 contra −0.0002**.

## 4. LA LÍNEA BASE TONTA (Reglas 11 y 12)
**Coronar siempre al primero de la lista.** Un panel que no le gana a eso no está juzgando: está
ordenando alfabéticamente. La forma de ganarle es **negarse a coronar cuando no hay mérito**, que
es justo lo que el panel no sabe hacer hoy.

## 5. LOS CRITERIOS CONGELADOS

| | criterio | pide |
|---|---|---|
| **A** | **el mérito real sigue ganando** | Con competidores por encima del piso, el panel corona **al mismo** que coronaba antes. Si cambiara algún veredicto ya emitido, **el arreglo rompe el pasado y se descarta** |
| **B** | **nadie sobre el suelo ⇒ nadie gana** | Con todos los competidores por debajo del piso declarado, el veredicto es **NINGUNO SUPERA EL SUELO** y **no hay ganador** |
| **C** | **sin suelo declarado ⇒ no se corona** | Sin `pisos`, el veredicto **no** contiene un ganador |
| **D** | **el suelo no borra a los buenos** | Con un competidor sobre el piso y otros debajo, gana el de arriba — el suelo **excluye**, no **empata** |

## 6. REGLA 31 — sobre MI PROCEDIMIENTO, los dos lados
- **Control positivo (debe aprobar):** un panel con un competidor claramente bueno y un piso
  razonable **corona a ese**.
- **Señuelo / control negativo (debe fallar):** con **todos** los competidores debajo del piso, el
  panel **no puede** producir ganador. Se prueba inyectando ese caso.
- **Y el caso que motivó todo:** competidores **a escala de ruido** con el piso de la vara
  calibrada → sin ganador.
- **No se prueba aquí nada sobre qué arquitectura es mejor.** Eso es resultado de un torneo, no
  requisito de entrada de la regla de oro.

## 7. CUÁNDO SE ABANDONA (Regla 13, con número)
- Si falla **A**, el arreglo **se descarta entero**: un cambio en la regla de oro que altere un
  veredicto ya emitido reescribe el pasado, y eso no se hace.
- Si fallan **B** o **C**, el arreglo no sirve para lo que se hizo.

## 8. LO QUE **NO** SE AFIRMA
- **Nada del universo.**
- **No se re-juzga ningún torneo pasado.** El INFORME del torneo de ojos se queda como está; si
  alguna vez se re-corre, será con su propio prerregistro.
- **No se fija el piso de ningún torneo futuro.** Eso es de cada torneo.

## 9. FIRMA
Avanza por **quórum adversarial**: el criterio A manda descartar el arreglo si toca el pasado, y el
punto 3 del §2 se pone a sí mismo la traba —sin suelo declarado no hay corona— que hace el trabajo
más incómodo. Revocable con una palabra del director.
