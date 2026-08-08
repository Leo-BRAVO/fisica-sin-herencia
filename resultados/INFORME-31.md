# INFORME 31 — Diego tiene cuerpo: el Gimnasio construido, y las dos cosas que solo se supieron corriéndolo — 8 de agosto de 2026

**Orden del director:** *"ya sabemos qué sigue: implementar. Implementamos todo lo faltante."*

Implementado. Y como siempre, construirlo enseñó cosas que teorizarlo no había enseñado.

---

## 1. Lo que hay ahora que ayer no existía

| Pieza | Qué es | Estado |
|---|---|---|
| `codigo/gimnasio.py` | El mundo: suelo, un brazo de 3 articulaciones, 3 objetos libres, física determinista. Balbuceo motor sin ninguna recompensa de tarea. | **construido y corriendo** |
| `codigo/contingencia.py` | El gen **G4**: el detector de *"¿esto respondió a MI comando?"* — el órgano del que nace la frontera yo/mundo. | **construido, aprueba su Regla 31** |
| Los 4 controles | Dentro del propio simulador, no en datos sintéticos aparte. | **3 de 4 pasan** |
| 5 casos nuevos de banco | Congelan las dos lecciones de hoy. | **50/50 verdes** |

**La confesión que va en cada nodo que salga de aquí:** la física de este mundo es **código humano**.
Diego no descubrirá el universo en el Gimnasio: descubrirá **nuestro simulador**. Por eso todo lo
aprendido aquí se marca `sobre-el-simulador` y jamás entra al árbol como física del mundo. El
Gimnasio no sirve para descubrir física — sirve para que **emerjan capacidades** que después se
aplican a datos del universo real.

---

## 2. LO PRIMERO QUE ENSEÑÓ: a un cuadro vista, un cuerpo es casi invisible para su propio dueño

La primera versión del detector **falló los cuatro controles**. La causa no fue un bug.

Un brazo es un sistema de segundo orden casi determinista: con tres retardos del ángulo se extrapola
casi perfecto un cuadro adelante, y el par que Diego aplica solo aporta un empujón minúsculo,
enterrado bajo el ruido de los contactos. Pero **el efecto de una aceleración sobre una posición
crece con el tiempo**:

| horizonte | 1 | 2 | 4 | 8 | 16 | 32 |
|---|---|---|---|---|---|---|
| articulación 0 (obedece) | +0.002 | +0.003 | +0.006 | +0.017 | +0.048 | **+0.141** |
| el mismo mundo, motores desconectados | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 |

**Y aquí hay algo bonito.** El *horizonte* fue la variable que propuse ayer y que **reprobó** su
Regla 31 (INFORME-30). Reprobó allí porque en la ganancia honesta se comparaban dos mundos distintos
—real contra surrogado— y la no estacionariedad fabricaba ventaja. **Aquí no hay dos mundos: hay un
mundo y dos conjuntos de entradas, sobre exactamente las mismas filas.** Es una comparación de
modelos anidados, y por construcción cierra el canal que nos mordió. La idea era buena; el
instrumento de ayer era el equivocado. Verificado en el banco: la trampa exacta del INFORME-30
—deriva fuerte con comandos suaves y cero agencia— **no fabrica ni un gramo de cuerpo**.

---

## 3. LO SEGUNDO, Y ES MÁS PROFUNDO: el brazo golpea las cajas

Con el horizonte corregido, tres controles pasaron y apareció algo que **el prerregistro-19, ya
firmado, no había previsto**: la altura de las cajas también respondía a los comandos.

No era un error de medición. **Era verdad.** El brazo las golpea. Un objeto manipulable **es**
contingente.

Eso significa que el criterio firmado —*"separar cuerpo de mundo por contingencia"*— **está
subespecificado**: con contingencia binaria, un juguete cuenta como parte del cuerpo. Lo que de
verdad los separa es la **CONTINGENCIA PERFECTA**: el cuerpo obedece *siempre*; el mundo solo en las
ventanas donde hubo contacto.

Al buscarlo, la literatura de contingencia sensomotora ya usaba ese término exacto. **Estaba en la
investigación que yo mismo escribí esta mañana y no lo aterricé en el criterio.** Lo digo así porque
es lo que pasó.

Reescrito como consistencia entre ventanas, el resultado:

| control | cuerpo real | hallado | |
|---|---|---|---|
| normal | 0, 1, 2 | **0, 1, 2** | ✔ las cajas quedan en 0.12, fuera |
| sin agencia | ninguno | **ninguno** | ✔ |
| televisor ruidoso corporal | 0, 2 | **0, 2** | ✔ la articulación de ruido puro queda fuera |
| un grado conectado | 0 | ninguno | **✘ obedece en 0.47, contra un piso de 0.50** |

---

## 4. Por qué me detengo en 3 de 4 en vez de entregar 4 de 4

**Falla por 0.03.** Bajar el piso de 0.50 a 0.45 lo arreglaría en un segundo.

**No lo hice.** Ese 0.50 lo puse a ojo antes de tener ninguna medición, y cambiarlo *después* de ver
un 0.47 es exactamente el vicio que llevamos toda la semana cazando: mover la vara hasta que el
resultado salga. Un revisor externo lo encontraría, y tendría razón.

Lo que hice en su lugar: **`registros/prerregistro-23.md`**, que enmienda el 19 y **fija las cuatro
constantes con su justificación** —horizonte 8, ventana 150, piso por ventana 0.02, y la fracción,
donde propongo 0.40 explicando de dónde sale y **admitiendo que la objeción de contaminación es
legítima**. Si el director prefiere dejar 0.50, entonces el control 2 se registra como **fracaso**,
que es lo que hoy es.

Las dos constantes quedan además **marcadas en el propio código** como no prerregistradas, y hay un
caso de banco que verifica que esa advertencia siga ahí.

---

## 5. Qué falta para que Diego nazca de verdad

1. **Que el director firme (o corrija) el prerregistro-23.** Es lo único que bloquea hoy.
2. **Los ojos del Gimnasio.** Hoy el detector lee el estado del simulador. El prereg-19 exige que
   Diego mire **cuadros de video** y entrene sus ojos desde cero sobre este mundo. Es la pieza
   grande que queda: rendering + `percepcion.py` + latentes → contingencia sobre *sus* variables,
   no sobre las nuestras.
3. **El nivel B** (el primer no-yo: la dirección de caída como la componente que ningún comando
   modula). Depende de 2.
4. **El verdugo por reescalado** — el filtro dimensional que solo existe en un simulador. Diseñado
   en `GIMNASIO.md`, sin construir.

---

*Guardianes al cerrar, con códigos de salida reales: `banco=0 (50/50) · coherencia=0 · prevuelo=0`.*
*Regla 31 del detector: APRUEBA los 4 mundos sintéticos. Regla 31 del Gimnasio: 3 de 4 — y por eso
el Gimnasio todavía no puede producir ningún hito.*
