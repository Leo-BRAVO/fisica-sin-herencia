# Prerregistro 37 — La experimentación dirigida: que Diego INTERVENGA, y la primera afirmación causal del proyecto — 10 de agosto de 2026
**Estado: FIRMADO por el director el 10-ago-2026 ("vamos a hacer todo absolutamente todo lo que
dijiste... avanzamos con el siguiente experimento").**

**Este es el prerregistro más importante que hemos escrito, y conviene decir por qué antes de
describir nada:** hasta hoy, **cada nodo del árbol es una afirmación sobre correlaciones en
grabaciones**. Ninguna es causal. Para separar causa de correlación hacen falta **intervenciones**,
y Diego nunca ha intervenido sobre nada — en el Gimnasio su brazo balbucea, pero **jamás toca el
objeto que cae**. Esto lo cambia.

---

## 1. Por qué (la evidencia propia que lo obliga)

El nodo **H-002** midió que en física de soporte el **observador pasivo empata** con el encarnado:
5/5 en el prereg-32 y otra vez 5/5 en cinco mundos distintos (prereg-35). Diferencias de +0.0027 a
−0.0095 contra un umbral de 0.05.

Ese empate **recortó nuestra tesis** y la dejó en su forma pequeña: el cuerpo no es un atajo para
aprender física; se justifica porque sin él no hay un "yo" respecto del cual definir nada.

**Pero el empate se midió en la única condición donde el cuerpo no podía ganar.** Nuestro
"encarnado" observa episodios exactamente igual que el pasivo — solo se distingue en que conoce sus
propias órdenes. **Nadie le dio nunca la posibilidad de cambiar lo que ocurre.** Comparar a un
encarnado que en la práctica mira contra un pasivo que mira **y llamarle empate del cuerpo es
injusto con la hipótesis, en nuestra contra**.

La experimentación dirigida es la capacidad donde **el pasivo no puede competir por construcción**:
no puede elegir qué mirar. Si el cuerpo no aportara ni aquí, sería una noticia **mucho mayor** que
el empate, y la publicaríamos igual.

## 2. Qué se construye (`codigo/experimentar.py`)

Un mundo con **una duda plantada**: dos objetos de aspecto **idéntico** —mismo tamaño, misma
forma, mismo color, misma posición de reposo— que difieren en **una sola propiedad oculta** que
**no se puede ver sin tocar**: uno es pesado y otro ligero (o uno está anclado y el otro suelto).

- **Mirando, la duda no se resuelve.** Quietos son indistinguibles: esa es la condición que hace
  del experimento un experimento y no una prueba de agudeza visual. Se verifica midiendo que un
  observador entrenado **no supera el azar** con solo mirar la escena en reposo.
- **Tocando, sí.** Un empujón revela la diferencia inmediatamente.

Y **tres condiciones**, que se diferencian **solo en quién decide qué hacer**:

| Condición | Qué puede hacer | Qué mide |
|---|---|---|
| **DIRIGIDO** | elige a cuál de los dos empujar y cuándo, según su propia incertidumbre | la capacidad completa |
| **AZAROSO** | actúa el mismo número de veces, con la misma fuerza, pero **elige al azar** | **el control que separa ACTUAR de ELEGIR** |
| **PASIVO** | mira los episodios del dirigido, sin actuar | el que empata en H-002 |

**La condición AZAROSO es el corazón de este prerregistro.** Sin ella, cualquier ventaja del
dirigido podría ser simplemente "tocar da más información que mirar", que es trivial y no dice nada
sobre inteligencia. Lo que queremos saber es si **elegir bien qué tocar** vale más que tocar al
azar. Esa es la diferencia entre agitar el mundo y hacerle una pregunta.

## 3. La frontera de contaminación, explícita
- **A Diego no se le dice que hay dos objetos, ni que difieren, ni en qué.** Se le da un mundo y una
  medida de su propia incertidumbre (el gen G14 ya existe y ya está medido). Que "reducir la
  incertidumbre" lleve a tocar lo dudoso **tiene que emerger, no programarse**.
- **Nada de física humana en la política.** La regla de elección puede usar únicamente cantidades
  que Diego ya calcula sobre sus propios datos. Ninguna función puede mencionar masa, peso, anclaje
  ni ninguna propiedad del mundo por su nombre.
- **Nada de LLM en el bucle.** Como siempre.

## 4. Lo que este prerregistro hace posible y ningún otro hacía
Con intervención elegida, y **solo con ella**, se puede preguntar: *¿el efecto que Diego predice
ocurre cuando ÉL lo provoca, y no ocurre cuando no lo provoca?* Eso es una **afirmación causal**, no
una correlación. Sería **la primera del proyecto**.

Se registra desde ya el límite: seguiría siendo causalidad **sobre el simulador**. La gravedad de
PyBullet es una ecuación que escribimos nosotros. El nodo llevaría `sobre-el-simulador` de por vida,
como H-000, H-001 y H-002.

## 5. Regla 31 declarada antes de correr (siete casos)
| # | Caso | Qué exige |
|---|---|---|
| 1 | **La duda es real** | mirando la escena en reposo, la propiedad oculta **no** se distingue por encima del azar. Si se distinguiera, no habría duda que resolver |
| 2 | **Tocar la resuelve** | un solo empujón separa los dos objetos muy por encima de su nulo |
| 3 | **Control positivo: el dirigido gana al pasivo** | si el que puede intervenir no supera al que solo mira, la comparación es ciega y nada de lo que siga significa algo |
| 4 | **EL CASO QUE DECIDE: dirigido vs azaroso** | con el **mismo número de toques y la misma fuerza**, elegir debe superar a no elegir. Es el único resultado que habla de inteligencia y no de mera acción |
| 5 | **SEÑUELO — el agitador** | una política que toca **mucho y sin criterio** no puede ganar. Es el hermano del señuelo de ruido de la escalera y del agitado del prereg-36, que ya cazaron fallos reales |
| 6 | **Mundo sin duda** | si los dos objetos son idénticos también por dentro, la ventaja del dirigido debe **desaparecer**. Un instrumento que premia la intervención donde no hay nada que averiguar mide su propio entusiasmo |
| 7 | **Guarda de potencia** | por debajo de N toques el módulo **se niega a dar veredicto**, como el mínimo de 20 ventanas del detector de contingencia y los 900 pasos de la escalera |

## 6. Criterios del hito (5 semillas, cinco mundos distintos como manda el prereg-35)
- **EL CUERPO APORTA CUANDO ELIGE** si el dirigido supera al **azaroso** por encima del umbral en
  ≥4/5 semillas. **El umbral se congela aquí antes de mirar nada** (ver §8).
- **ACTUAR SÍ, ELEGIR NO** si el dirigido supera al pasivo pero **empata con el azaroso**. Sería un
  resultado importante y decepcionante: el cuerpo sirve, la cabeza todavía no.
- **EMPATE TOTAL** si el dirigido no supera al pasivo. Refutaría lo poco que le quedaba en pie a la
  tesis de la encarnación, y **se publicaría igual** — con el mismo peso que H-002.

## 7. La predicción, comprometida ANTES de correr
- **Espero que el dirigido gane al pasivo con holgura.** Sería raro que no: puede obtener
  información que el otro no tiene acceso a producir.
- **NO tengo confianza en que gane al azaroso.** Con dos objetos y una sola propiedad, el espacio de
  preguntas es minúsculo, y tocar al azar acierta la mitad de las veces. Si sale empate, la lectura
  honesta será *"el mundo era demasiado simple para que elegir importara"*, y la cura es **más
  objetos y más propiedades**, no un umbral más bajo.
- **Espero que el señuelo agitador sea rechazado**, porque sus dos hermanos ya cazaron fallos
  reales a la primera corrida.

## 8. Qué NO se autoriza
- **El umbral no se mueve después de ver los datos.** Es la regla que el prereg-36 me hizo cumplir
  cuando dolía, y aquí va a doler más.
- **La política de elección no entra al genoma** por esta corrida. Es un instrumento; el genoma solo
  cambia entre generaciones y con firma (Regla 33).
- **Ningún nodo nace de aquí sin réplica en cinco mundos**, por la lección del INFORME-39: cinco
  mediciones de una realización no son cinco réplicas.
- **No se toca la escalera de soporte ni el prereg-32.** Si se movieran a la vez que esto, no se
  sabría qué produjo el cambio.

## Firmado
Leo, director — 10-ago-2026, aprobación en conversación.
