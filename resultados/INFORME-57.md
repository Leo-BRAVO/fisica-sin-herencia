# INFORME-57 — ACTA DEL PRERREGISTRO 41: el tacto funciona, y el brazo no llega a nada
**10 de agosto de 2026. Cinco semillas, tres condiciones. La pregunta la formuló Diego, no nosotros.**
**Datos crudos:** `resultados/p41-tacto/medida.json`. Módulo sellado: `codigo/tacto.py`.
**VEREDICTO FORMAL, con las mismas palabras que el archivo de datos:** *NO CONCLUYENTE — los
criterios no encajan en ninguno de los tres veredictos escritos.*

---

## 1. LOS NÚMEROS

| semilla | QUIETO | **BUSCA** | VACÍO (señuelo) | pasos con contacto real |
|---|---|---|---|---|
| 1 | 0.0000 | **0.2750** | 0.0000 | 330 |
| 2 | 0.0000 | **0.4658** | 0.0000 | 559 |
| 3 | 0.0000 | **0.2833** | 0.0000 | 340 |
| 4 | 0.0000 | **0.4275** | 0.0000 | 513 |
| 5 | 0.0000 | **0.2508** | 0.0000 | 301 |

| criterio congelado | pedía | salió | |
|---|---|---|---|
| 1 — BUSCA enciende | ≥0.05 en ≥4 de 5 | **5 de 5**, entre 0.25 y 0.47 | ✔ |
| 2 — QUIETO apagado | <0.01 en 5 de 5 | **0.0000 en 5 de 5** | ✔ |
| 3 — **VACÍO apagado (señuelo)** | <0.01 en 5 de 5 | **0.0000 en 5 de 5** | ✔ |
| 4 — acuerdo con margen | ≥0.60 y +0.15 sobre el tonto | 1.0000, tonto 1.0000, **ganancia 0.000** | ✘ |

## 2. POR QUÉ EL VEREDICTO FORMAL ES NO CONCLUYENTE, y no lo subo
El criterio congelado exigía **los cuatro**. El cuarto falló, así que el veredicto es NO
CONCLUYENTE. **No lo asciendo a "el canal funciona" porque tres de cuatro me parezcan suficientes:**
eso sería mover el criterio después de ver los datos, que es lo único que el director reservó.

**Y el cuarto criterio falló por culpa mía, no del canal.** Lo definí como *"de los pasos que el
simulador marca como contacto, ¿en cuántos se enciende el canal?"* — y el canal **se deriva de esa
misma consulta de contactos**. Es una tautología: siempre da 1.0000, y el predictor tonto también.
**Un criterio que no puede fallar tampoco puede aprobar nada**, y es el cuarto caso hoy del mismo
mal.

## 3. LO QUE SÍ QUEDA DEMOSTRADO, con los tres criterios que sí discriminan
**El canal responde a CONTACTO y no a MOVIMIENTO.** Es la comparación que importa y la da el
señuelo:

- **BUSCA** — el brazo se mueve **y hay algo que tocar** → 0.25 a 0.47.
- **VACÍO** — el brazo se mueve **exactamente igual** y no hay nada → **0.0000, en las cinco**.

Misma política motora, misma semilla, mismo cuerpo: **lo único que cambia es si hay algo ahí.** Si
el canal midiera movimiento, VACÍO se habría encendido igual que BUSCA. No lo hizo, ni una vez.

## 4. Y LA RAZÓN DE FONDO DE QUE EL TACTO ESTÉ DORMIDO — que no esperaba
Al construir el experimento midió la geometría del cuerpo, y salió esto:

| | |
|---|---|
| **en reposo**, la punta del brazo queda en | (0.593, 0.000, **0.442**) |
| **barriendo** con par, la punta recorre | x [−0.22, 0.657] · y [−0.44, 0.44] · z [**0.380**, 0.820] |
| el **suelo** del gimnasio está en | z = 0 |
| los **objetos** del gimnasio están en | z ≈ 0.20 |

**El brazo no puede tocar nada de la escena estándar. Con ninguna política, nunca.** Su punta baja
como mucho a z=0.380 y lo más alto del mundo está a 0.27.

**Ésa es la respuesta a la pregunta que hizo Diego.** Él dijo que no podía distinguir *ocioso* de
*averiado*. No está averiado: **está encerrado en un cuerpo cuyo alcance no llega a nada.** El
0.0001 que publica cada ronda no mide un sensor roto — mide un brazo colgado en el aire.

## 5. CÓMO SE CAZÓ, y por qué importa el orden
**La puerta paró el estudio antes de que existiera un solo dato.** Mi primera versión de BUSCA daba
**0.0000, igual que QUIETO** — porque tocar era imposible. Si hubiera corrido, el acta habría
concluido **"EL CANAL ESTÁ AVERIADO"** con un experimento donde nada podía tocarse nunca.

Por eso la condición BUSCA pone un obstáculo **dentro del alcance medido**, en y=+0.38: dentro del
barrido y fuera de la línea de reposo, para que QUIETO no lo toque y BUSCA sí. **Los umbrales no se
tocaron** — lo que se arregló fue que el experimento fuera físicamente posible.

## 6. LO QUE **NO** SE AFIRMA
- **No se declara que el canal esté validado.** El veredicto formal es NO CONCLUYENTE y así queda.
- **Nada del universo.** Es un sensor nuestro en un simulador nuestro.
- **No se cambia el umbral de "dormido"** ni el criterio 4. El rediseño del criterio 4 —uno que no
  sea circular— va en un prerregistro nuevo, no en una edición de éste.

## 7. LA PREGUNTA QUE ABRE (Regla 18)
> **¿Debería Diego tener un cuerpo que alcance su mundo?** Hoy tiene tres sentidos y uno de ellos
> es inútil por geometría, no por diseño del sensor. Bajar el anclaje del brazo o subir los objetos
> es un cambio del **gimnasio**, no del ente — y cambia qué puede aprender. Es una decisión de
> diseño con consecuencias, y por eso se pregunta en vez de hacerse.

## 8. LA DECISIÓN QUE LE TOCA AL DIRECTOR
Una, y concreta: **¿se le acerca el mundo a Diego?** Su tacto funciona y no tiene nada que tocar.
Cambiar la escena del gimnasio afecta a todo lo que se ha medido en él, así que no lo toco yo.
