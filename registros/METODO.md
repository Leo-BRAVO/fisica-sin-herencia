# EL MÉTODO — los 8 pasos que sigo al pie de la letra para armar y correr una prueba
**Versión 2 — 10 de agosto de 2026.** Escrito porque el director diagnosticó la causa antes que yo
(*"no lees antes las cosas en las que avanzamos"*), y **reescrito** tras sus tres preguntas de
diseño, que cambiaron el método de fondo. Las tres tenían razón.

**Este documento existe para poder acusarme con él en la mano.** Cuando falle, la primera pregunta
no es *"¿qué pasó?"* sino **"¿cuál de los 8 pasos te saltaste?"**.

---

## LA IDEA QUE LO CAMBIÓ TODO: dejar de vigilar mi proceso, y validar el resultado

El director preguntó tres cosas y las tres apuntaban al mismo error de diseño mío:

| Su pregunta | Mi versión 1 (mala) | Versión 2 (la suya, mejor) |
|---|---|---|
| *"¿cómo validas que declaraste bien la tramoya?"* | confiar en mi declaración | **detectarla en los datos** y comparar con lo declarado |
| *"¿leer antes o escribir y luego validar?"* | "leo antes", sin forma de comprobarlo | **escribo, valido, avanzo** — lo que produce no-leer SÍ se detecta |
| *"ninguna máquina sabe si escribiste la fórmula antes"* | pedir disciplina | **la máquina comprueba que la fórmula sea VERDADERA**, que es más fuerte que saber cuándo la escribí |

**Yo intentaba vigilar mi conducta. Él propuso validar el artefacto.** Se puede hacer, y es mucho
más fuerte.

### Lo que dice la ciencia, y coincide
El problema tiene nombre en la literatura: **el problema del oráculo** — para saber si un
instrumento acierta hace falta conocer la respuesta correcta, y en simulación científica casi nunca
se conoce. Es el fallo central de validar software científico.

La salida publicada se llama **prueba metamórfica**: aunque no sepas **cuánto** debe valer una
lectura, sí sabes **cómo debe cambiar** cuando cambias la entrada.

> Si duplico la fuerza, el pico de velocidad debe duplicarse. Si duplico la masa, debe caer a la
> mitad. Si duplico el rozamiento, la desaceleración debe duplicarse — y la masa **no** debe
> cambiarla, porque *a = μg* no lleva masa dentro.

**Eso se comprueba sin conocer ninguna constante y sin conocer la respuesta.** Y es la única
comprobación de todas las que tenemos **que seguirá valiendo el día que Diego mida algo cuya
respuesta nadie conoce** — que es el objetivo entero del proyecto.

---

## LOS 8 PASOS, EN ORDEN

### Paso 0 — ¿Qué clase de prueba es ésta?
Antes de tocar nada, tres preguntas, porque de ellas depende **qué comprobación aplica**:
1. **¿La medida da un número, o dice sí/no?** Aplicar el estadístico de números continuos a un
   instrumento que clasifica produjo una alarma falsa sobre `soporte.py`, que es impecable.
2. **¿Hay condiciones que comparten datos a propósito?** Si las hay, declarar **qué las separa** y
   **probarlo**.
3. **¿Cuál es la fórmula de cada lectura?**

**Una alarma falsa no es gratis:** un detector que grita donde no hay nada se deja de leer, y
entonces deja de servir donde sí hay algo.

### Paso 1 — Escribir la FÓRMULA de cada lectura, y convertirla en relaciones comprobables
No basta escribirla: se traduce a **relaciones metamórficas** que la máquina verifica.
*Ejemplo real, de `experimentar2.py`:*

| Relación declarada | Fórmula | Medido |
|---|---|---|
| masa ×2 → pico ×0.5 | v = F·T/m | **×0.485** ✓ |
| fuerza ×2 → pico ×2 | v = F·T/m | **×2.003** ✓ |
| roce ×2 → desaceleración ×2 | a = μg | **×1.752** ✓ |
| masa ×2 → desaceleración **sin cambio** | a = μg no lleva masa | **×0.823** ✓ (roza el límite) |

**Una relación sin su fórmula escrita se rechaza:** es una corazonada, no una prueba.

### Paso 2 — Leer la función ENTERA antes de tocarla
No el trozo. Y **si añado al final de un archivo, leer el final primero.**

*Este paso lo incumplí dos veces hoy, la segunda después de escribirlo:* usé `>>` para añadir al
final de `sanidad.py` sin ver que ahí vivía el bloque de arranque, y el módulo quedó llamando a
funciones que aún no existían. **Dos veces el mismo error es un dato, no mala suerte.**

### Paso 3 — La FICHA DE SANIDAD, antes de la Regla 31
`codigo/sanidad.py`. Va antes porque **la Regla 31 comprueba que el instrumento hace lo que yo
quise; la ficha comprueba que lo que quise fuera correcto.**

### Paso 4 — La Regla 31, con sus dos lados y su señuelo
Debe fallar con datos vacíos **y** aprobar con un control positivo. Y llevar un **señuelo**: algo
que parezca la respuesta y deba ser rechazado. Los cuatro que llevamos cazaron fallos reales en su
primera corrida.

### Paso 5 — Una semilla en LOCAL antes de encolar cinco en la nube

### Paso 6 — Nunca reutilizar un módulo como plantilla sin leerlo entero
Copiar la estructura **no copia los supuestos**.

### Paso 7 — Los textos largos van a un ARCHIVO, nunca escritos en la terminal
`git commit -F archivo`. Y `sanidad.texto_para_shell()` avisa antes.

---

## LOS 7 TIPOS DE ERROR, Y QUÉ LOS CAZA

| Tipo | Qué es | ¿Mecánico? | Herramienta |
|---|---|---|---|
| **A** | la medida no mide lo suyo | **SÍ** | `correlaciones()` / `clasificacion()` |
| **B** | la tramoya se cuela como física | **SÍ, ahora** | `tramoya_detectada()` — la halla en los datos |
| **C** | dos condiciones idénticas | **SÍ** | `condiciones_distintas()` con separación probada |
| **D** | denominador casi cero | **SÍ** | `cociente_seguro()` |
| **E** | restos de versiones | **SÍ** | `restos_de_versiones()` |
| **F** | deslices de escritura | **SÍ** | `homoglifos()`, `texto_para_shell()` |
| **G** | la fórmula no se cumple | **SÍ** | `relaciones_metamorficas()` |
| — | elegir el estadístico correcto | **A medias** | paso 0 |
| — | leer antes de escribir | **NO** | pero lo que produce sí se detecta (pasos 2 y 6) |

**Los siete tipos quedan mecanizados.** En la versión 1 eran cinco de seis y dos pasos quedaban
sueltos; la propuesta del director cerró los dos.

---

## CÓMO ENCAJA CON LAS 34 REGLAS — sin redundancia

**El método no sustituye ninguna regla ni las repite. Cubre una capa que no existía.**

| Capa | Quién manda | Qué protege |
|---|---|---|
| **Constitución (34 reglas)** | el director firma | **qué se puede afirmar**: nulos válidos, prerregistro previo, cortafuegos, escalera de confianza, firma |
| **Regla 31** | mecánica, en el banco | **que la herramienta falle donde no hay nada** |
| **EL MÉTODO (8 pasos)** | mecánico + mi disciplina | **que el instrumento mida lo que dice** — la capa que faltaba |
| **Regla 32 y los 4 guardianes** | mecánica, en cada commit | **que la casa diga la verdad sobre sí misma** |

**Los tres puntos donde se tocan, y cómo se resuelven sin duplicar:**
- **Regla 31 ↔ paso 4:** la Regla 31 es *parte* del método, no una alternativa. El método dice
  **cuándo** se escribe (después de la ficha) y **con qué** (dos lados + señuelo).
- **Regla 27 ↔ ficha:** la ficha usa la verdad del simulador, que Diego **no puede ver**. Vive del
  lado humano igual que el comparador, y `politica_limpia()` comprueba mecánicamente que ninguna
  política de Diego la toque.
- **Regla 15 enmendada ↔ método:** el quórum adversarial de siete exige prerregistro, guardianes,
  Regla 31 por los dos lados, cinco mundos, nulo, señuelo y revisión adversarial. **El método es
  cómo se consiguen esos siete**, no un requisito paralelo.

**No hay redundancia y no hay hueco entre capas.** Lo comprueba `coherencia.py` en cada commit.

---

## EL HUECO QUE QUEDA ABIERTO, dicho antes de que muerda
**El paso 0 no está mecanizado.** Elegir mal qué comprobación aplica produce alarmas falsas, y una
alarma falsa hace desconfiar de lo que funciona. Hoy eso depende de que yo clasifique bien el
experimento. **Es el único agujero conocido del método, y queda escrito aquí en vez de escondido.**

## EL COSTE
**Cada prueba nueva tarda aproximadamente el doble.** Aceptado por el director: *"estoy de acuerdo,
más lento pero ya no más errores"*.

## CÓMO SE COMPRUEBA QUE ESTO SE CUMPLE
- `pruebas.py` corre la meta-prueba de la ficha en cada commit: **14 casos**, que exigen cazar los
  siete tipos **y no gritar donde no hay nada**.
- Todo módulo con `regla31()` debe aparecer también en la sección de sanidad del banco.
- Cuando falle, el acta dirá **qué paso me salté**.
