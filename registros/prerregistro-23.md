# Prerregistro 23 — Enmienda al 19: el criterio de la frontera yo/mundo, con sus constantes fijadas — 8 de agosto de 2026
**Estado: BORRADOR pendiente de firma del director. Enmienda el prerregistro-19 (FIRMADO) en un
punto que solo se descubrió CONSTRUYENDO el Gimnasio y corriéndolo contra sus propios controles.**

---

## Por qué existe esta enmienda

El prerregistro-19 dice, en su éxito nivel A: *"el mapa de contingencia separa las variables del
cuerpo de las del mundo con exactitud ≥ 90%"*. Al construir el mundo y correr los cuatro controles
apareció que **ese criterio está subespecificado**, por dos razones que no son fallos de código:

**1. El brazo golpea las cajas.** La altura de una caja **sí responde** a los comandos de Diego —
por contacto. Con contingencia binaria, un objeto manipulable cuenta como "cuerpo". La frontera
yo/mundo **no es contingencia sí/no**. Lo que las separa es la **CONTINGENCIA PERFECTA**: el cuerpo
obedece *siempre*; el mundo solo en las ventanas donde hubo contacto. (La literatura de contingencia
sensomotora ya usaba ese término; el prereg-19 lo pasó por alto.)

**2. A un cuadro vista, un cuerpo es casi invisible para su propio dueño.** Un brazo es un sistema
de segundo orden casi determinista: con tres retardos del ángulo se extrapola casi perfecto un
cuadro adelante, y el par solo aporta un empujón enterrado bajo los contactos. El efecto de una
aceleración sobre una posición **crece con el tiempo**. Medido en nuestro propio simulador:

| horizonte | 1 | 2 | 4 | 8 | 16 | 32 |
|---|---|---|---|---|---|---|
| contingencia de la articulación 0 | +0.002 | +0.003 | +0.006 | +0.017 | +0.048 | **+0.141** |
| mismo mundo con los motores desconectados | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 | +0.000 |

---

## Estado medido HOY, con el criterio corregido (3 de 4 controles)

| control | cuerpo real | hallado | veredicto |
|---|---|---|---|
| normal | 0, 1, 2 | **0, 1, 2** | ✔ (y las cajas, 0.12, quedan fuera) |
| sin agencia | ninguno | **ninguno** | ✔ |
| televisor ruidoso corporal | 0, 2 | **0, 2** | ✔ (la articulación de ruido puro queda fuera) |
| un grado conectado | 0 | **ninguno** | ✘ — la variable 0 obedece en 0.47 de las ventanas, contra un piso de 0.50 |

**El cuarto control falla por 0.03.** Y aquí está la razón de este documento: **no voy a bajar el
piso de 0.50 a 0.45 para que pase.** Elegir la constante después de ver el resultado es exactamente
el vicio que este proyecto lleva la semana entera cazando. Las constantes se fijan aquí, firmadas,
antes de volver a correr.

---

## Lo que esta enmienda fija (y por qué cada número)

- **Horizonte de medición: h = 8 cuadros.** Justificación *a priori*, no ajustada: es el orden de
  magnitud en que el efecto de una aceleración sobre una posición se hace comparable al ruido de
  contacto. Se declara **antes** y no se explora a posteriori.
- **Ventana: 150 cuadros** (~5 segundos de mundo). Suficiente para que un contacto ocurra dentro de
  una ventana y no la domine entera.
- **Piso por ventana: 0.02** de reducción del error. Es el umbral de "hubo respuesta" en esa ventana.
- **Fracción de ventanas para declarar CUERPO: se propone 0.40**, no 0.50.
  **Justificación explícita, y el director debe juzgarla:** 0.50 fue un número que puse a ojo antes
  de tener ninguna medición. El valor que sí tiene contenido es que **el cuerpo debe obedecer en una
  fracción mayor que cualquier variable de mundo y mayor que el techo de su nulo**. En los cuatro
  controles, las variables de mundo llegan como máximo a **0.18** y los nulos a **0.41**. Un umbral
  de 0.40 sigue por encima de todo lo que el mundo y el azar produjeron. **Si el director considera
  que elegir 0.40 después de ver 0.47 está contaminado — y es una objeción legítima — la alternativa
  honesta es dejar 0.50 y registrar el control 2 como FRACASO, que es lo que hoy es.**
- **Nulo: desplazamiento circular de los comandos.** Conserva entera la estructura temporal del
  comando y destruye solo su alineación con las señales. Barajarlos sería demasiado destructivo
  (les quitaría su autocorrelación) — el error espejo que ya cometimos en el INFORME-25.
- **Criterio de éxito del hito 0, enmendado:** una variable se declara CUERPO si obedece en una
  fracción de ventanas **mayor que el techo de su distribución nula Y mayor que el umbral fijado
  arriba**, y esa clasificación coincide con la verdad de los jueces en **≥ 90% de las variables**,
  replicado en **≥ 4 de 5 semillas**.

## Predicción comprometida
Con h=8 y fracción 0.40, espero **4 de 4 controles**. Si el control 2 sigue fallando, el problema no
es el umbral: es que un solo grado de libertad conectado en una cadena de tres eslabones produce una
señal genuinamente débil, y habría que decirlo así en vez de seguir moviendo constantes.

## Lo que esta enmienda NO cambia del prerregistro-19
Los jueces congelados, el nivel B (el primer no-yo), la marca `sobre-el-simulador` en todo lo que
salga del Gimnasio, y la prohibición de que nada de esto entre al árbol como física del mundo.

- **Firmado:** PENDIENTE — Leo, director.
