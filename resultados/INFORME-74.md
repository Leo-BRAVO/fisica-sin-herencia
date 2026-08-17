# INFORME-74 — ACTA DEL PRERREGISTRO 61: la curiosidad sola NO basta para buscar el contacto, y esta vez el diseño sí podía distinguirlo
**17 de agosto de 2026. 15 semillas, 20000 pasos por política, criterio con su probabilidad bajo el
azar escrita ANTES de correr.**
**Datos crudos:** `resultados/p61-contacto2/medida.json`. Módulo: `codigo/contacto2.py` (puerta
8/8).
**VEREDICTO, con las palabras del archivo de datos:** *LA CURIOSIDAD SOLA NO BASTA PARA BUSCAR EL
CONTACTO — gana en 6 de 15 y hacían falta 12. Esta vez el diseño SI tenía potencia, así que el item
queda cerrado con una respuesta.*

---

## 1. LOS NÚMEROS

| | de 15 semillas |
|---|---|
| **la intrínseca le gana al balbuceo** | **6** — hacían falta 12 |
| **el nulo (barajada) le gana al balbuceo** | **9** — por debajo de 12, así que no anula nada |
| **la intrínseca gana en el mundo sordo** | **6** — igual que en el mundo normal |
| **diferencia mediana** (informativa, sin veto) | **−0.00075** |
| **el azar pasa el criterio congelado** | **0.0176**, escrito antes de correr |

| criterio congelado | pedía | salió | |
|---|---|---|---|
| **A** el cortafuegos aguanta | sin fugas | ✔ | ✔ |
| **B** el mundo sordo no premia | < 12 de 15 | **6** | ✔ |
| **C** la intrínseca busca sola | ≥ 12 de 15 | **6** | ✘ |
| **D** el nulo no gana | < 12 de 15 | **9** | ✔ |
| **E** no se puede inventar contacto | 0.0 con radio 0 | ✔ | ✔ |

## 2. LA RESPUESTA, y por qué esta vez cuenta
El prerregistro 60 no pudo decir nada: **su nulo pasaba el criterio el 18.75% de las veces por puro
azar**. Aquí el criterio lo pasa el **1.76%**, y el nulo **no lo pasó**: ganó 9 de 15, por debajo
del umbral.

> **Con un diseño que sí distinguía, la respuesta es que no.** Una política movida únicamente por
> el desacuerdo entre sus propios modelos **no acaba más cerca del objeto que una que se mueve al
> azar** — 6 de 15, y la diferencia mediana es **−0.00075**, es decir **nada, o un pelo en contra**.

**El item 30 queda cerrado con una respuesta, no con un empate.** El canal táctil sigue ocioso, y
ahora se sabe **por qué**: no porque el sensor falle —el INFORME-57 ya mostró que funciona— sino
porque **la curiosidad, tal como está construida, no lleva la mano hasta donde hay algo que tocar.**

## 3. LO QUE NO ME GUSTA DE MI PROPIO RESULTADO, y va escrito
**Yo predije este resultado en el prerregistro** («Espero que C falle»). **Una predicción que se
cumple vale menos que una que se rompe**, y hay que decirlo: el diseño se construyó para poder
refutarme —criterio congelado, nulo, mundo sordo, control positivo— pero el resultado **no me
contradijo**, y eso baja su valor como evidencia. Lo que lo sostiene no es mi acierto: es que
**el nulo y el mundo sordo salieron donde tenían que salir**.

**Y hay algo peor, que es el dato más interesante del acta:**

> **El nulo lo hizo MEJOR que la política que se estudia: 9 de 15 contra 6 de 15.** Elegir por el
> desacuerdo de los propios modelos no solo no ayuda — **parece estorbar** frente a elegir al azar
> ese mismo desacuerdo. Con 15 semillas eso **no es concluyente** (9 y 6 caben en el ruido), pero
> apunta a que el `argmax` del desacuerdo **concentra la mano** en zonas que no llevan a ninguna
> parte, en vez de explorar.

## 4. QUÉ SE HABRÍA NECESITADO, y no se hace aquí
Lo que este estudio deja claro es que **el desacuerdo de un conjunto de modelos cuadráticos, elegido
por `argmax` a un paso**, no basta. Lo que faltaría es otra cosa —planificación a varios pasos,
progreso de aprendizaje en vez de desacuerdo puro, o empowerment— **y cada una es un prerregistro
nuevo, no una enmienda a éste.**

## 5. LO QUE **NO** SE AFIRMA
- **Nada del universo.**
- **NO se afirma que ninguna curiosidad pueda buscar el contacto.** Se afirma que **ésta**, en
  **este** mundo, con **este** presupuesto de pasos, no lo hace. Cambiar cualquiera de los tres es
  otro estudio.
- **NO se afirma que el nulo sea mejor política.** 9 contra 6 en 15 semillas **no distingue nada**,
  y decir lo contrario sería cometer con el nulo el mismo error que el prerregistro 60 cometió con
  el resultado.
- **NO se retira el INFORME-71.** Aquel dijo «este diseño no puede decidir» y tenía razón; éste
  decide.
- **NO se conecta ninguna política a nada**, ni se tocó `politica_contacto.py`, `tacto.py`,
  `mundo.py` ni `gimnasio.py`.

## 6. LO QUE LE TOCA AL DIRECTOR
**Nada urgente.** El item queda cerrado. Si algún día quiere volver sobre el tacto, la pregunta ya
no es «¿busca el contacto?» sino **«¿qué clase de motivación sí lo haría?»**, y eso empieza por un
prerregistro nuevo.
