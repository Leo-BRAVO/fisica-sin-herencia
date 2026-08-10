# EL MÉTODO — las seis reglas que sigo al pie de la letra al armar una prueba
**10 de agosto de 2026. Escrito a petición del director, que diagnosticó la causa antes que yo:
*"no lees antes las cosas en las que avanzamos"*. Tenía razón, y esto es lo que hago al respecto.**

Este documento existe para poder **acusarme con él en la mano**. Si vuelvo a fallar, la primera
pregunta es cuál de estos seis pasos me salté.

---

## El diagnóstico, con los números
Catorce errores míos en seis módulos, en una sesión. No son catorce errores distintos — son **seis
tipos que repito**:

| Tipo | Veces | Qué es |
|---|---|---|
| **A** | 5 | la medida no mide lo que creo |
| **B** | 3 | la tramoya del simulador se cuela como si fuera física |
| **C** | 2 | dos condiciones que son la misma por construcción |
| **D** | 2 | cocientes con denominador casi cero |
| **E** | 1 | restos de versiones anteriores que siguen ejecutándose |
| **F** | 2 | deslices de escritura invisibles al ojo |

**Y la causa común de casi todos: edito por parche y no releo el conjunto.**

---

## Los seis pasos, en orden, sin saltarse ninguno

### 1. Leer la función ENTERA antes de tocarla
No el trozo que voy a cambiar: la función completa, y el archivo si es corto.

*De aquí salieron:* la variable pisada en `soporte.py`, la fuerza duplicada en `experimentar2.py`,
y el `guardian_ok` de `sueno.py` que llevaba semanas calculándose y tirándose bajo un comentario
que decía lo contrario.

### 2. Escribir la FÓRMULA antes que el código
Si voy a medir masa, escribo primero **v ≈ F·T/m**. Si voy a medir rozamiento, **a = μg**.

**Si no sé escribir la fórmula, no entiendo la medida y no debo programarla.**

*Los cinco errores de tipo A los habría cazado esto solo.* Es también la forma correcta de la
investigación que el director pide: se investiga **cómo se mide**, jamás **cuál es la respuesta**.
Buscar métodos de medición es metodología y vive en `registros/`. Buscar la respuesta física es
contaminación y rompe la Regla 27.

### 3. La FICHA DE SANIDAD antes de la Regla 31
`codigo/sanidad.py`, contra la verdad del simulador. Comprueba los seis tipos.

**Por qué va antes y no después:** todos mis casos de Regla 31 comprueban que el instrumento hace
**lo que yo quise**. Ninguno comprueba que lo que quise fuera **correcto**. La Regla 31 valida el
diseño contra mis propias suposiciones — si la suposición está mal, aprueba con entusiasmo.

*Probado:* aplicada a `experimentar2.py` **después** de que su Regla 31 lo aprobara 8/8, encontró
dos cosas más.

### 4. Una semilla en LOCAL antes de encolar cinco en la nube
Correr cinco semillas de un instrumento que no he mirado es gastar cinco veces el mismo error.

### 5. Nunca reutilizar un módulo como plantilla sin leer el original de punta a punta
Copiar la estructura de un módulo que funciona **no** copia sus supuestos. `experimentar2.py`
heredó de `experimentar.py` la idea de empujar con una fuerza — sin que yo comprobara que en
PyBullet **una fuerza dura un solo paso**. Cuatro de ocho objetos no se movían.

### 6. Los mensajes largos van a un ARCHIVO, nunca inline en la terminal
`git commit -F archivo`, siempre. Nada de comillas invertidas dentro de comillas dobles.

*De aquí salió:* un mensaje de commit donde bash **ejecutó** lo que había entre comillas invertidas
y borró dos nombres de variable del registro. Y `sanidad.texto_para_shell()` avisa antes.

---

## Lo que ahora es MECÁNICO y lo que sigue dependiendo de mi disciplina

**Esta distinción es la respuesta honesta a *"¿con esto mejoro todo el método?"*.**

| Tipo | ¿Lo caza una máquina? | Cómo |
|---|---|---|
| **A** — la medida no mide lo suyo | **SÍ** | `correlaciones()` contra la verdad del simulador |
| **C** — condiciones idénticas | **SÍ** | `condiciones_distintas()` compara los datos, no los resultados |
| **D** — denominador casi cero | **SÍ** | `cociente_seguro()` devuelve 0 bajo el piso |
| **E** — restos de versiones | **SÍ** | `restos_de_versiones()` sobre el AST |
| **F** — deslices de escritura | **SÍ** | `homoglifos()` y `texto_para_shell()` |
| **B** — la tramoya se cuela | **A MEDIAS** | `tramoya_declarada()` exige declararla, pero **no sabe si la declaré bien** |
| **Leer antes de escribir** | **NO** | ninguna máquina puede obligarme |
| **Escribir la fórmula primero** | **NO** | ninguna máquina sabe si la escribí antes o después |

**Cinco de seis tipos quedan mecanizados. Los dos pasos que más errores causaron —leer antes y
escribir la fórmula primero— NO son mecanizables**, y sería deshonesto decir lo contrario. Lo que
sí puedo hacer es dejarlos escritos aquí para que se me pueda exigir.

## El coste, dicho antes de que se note
**Cada prueba nueva va a tardar aproximadamente el doble.** Es el precio de los seis pasos, y el
director lo aceptó explícitamente: *"estoy de acuerdo, más lento pero ya no más errores"*.

## Cómo se comprueba que esto se cumple
- `pruebas.py` corre la meta-prueba de la ficha en cada commit, y la ficha debe **cazar los seis
  tipos** y **no gritar donde no hay nada** — un detector que siempre encuentra algo es tan inútil
  como uno que nunca encuentra nada.
- Todo módulo nuevo con `regla31()` debe aparecer también en la sección de sanidad del banco.
- Cuando falle, el acta dirá **qué paso me salté**, no "hubo un error".
