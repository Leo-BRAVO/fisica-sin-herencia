# Prerregistro 35 — La segunda ronda: que la caída varíe de verdad — 10 de agosto de 2026
**Estado: FIRMADO por el director el 10-ago-2026 ("adelante con todo").**
**Nace de un defecto que encontramos nosotros, en nuestra propia tabla, sin que nadie lo señalara.**

## Por qué (el hallazgo, no la excusa)
El INFORME-39 declaró el prereg-29 **conseguido 5/5** según su criterio firmado. Al leer la tabla
**en vertical** apareció esto:

| | s1 | s2 | s3 | s4 | s5 |
|---|---|---|---|---|---|
| escalón 1, `autopredictible` | 0.5403 | 0.5403 | 0.5403 | 0.5403 | 0.5403 |
| escalón 2, efecto | 2.544 | 2.544 | 2.544 | 2.544 | 2.544 |
| escalón 2, nulo | 0.1397 | 0.1397 | 0.1397 | 0.1397 | 0.1397 |

Idénticos hasta el último dígito. **No es una coincidencia notable: es una consecuencia del
diseño.** La semilla gobierna el **balbuceo del brazo**, y el brazo **nunca toca al objeto que
cae**. La caída es la misma caída, desde la misma altura, con la misma masa, en las cinco corridas.

**Cinco mediciones de una realización no son cinco réplicas.** Un número que aparece idéntico cinco
veces no ha sido sometido a prueba cinco veces.

Lo que sí replicó de verdad —y sigue en pie— es el **rechazo**: cinco balbuceos distintos, y en los
cinco el criterio supo decir "esto soy yo, esto no", con el señuelo de ruido rechazado por ilegal
las cinco veces. Y el **examen VOE** sí varía (0.0948 a 0.1951). Lo que no está replicado es la
**aceptación**.

## Qué se construye
El mundo deja de ser una constante y pasa a ser un sorteo por semilla:

| Parámetro | Fijo (1ª ronda) | Rango (2ª ronda) |
|---|---|---|
| altura de la mesa | 0.55 | 0.40 – 0.70 |
| altura de soltada | 1.30 | 1.05 – 1.55 |
| masa del objeto | 0.25 | 0.15 – 0.45 |
| posición de soltada (x) | 1.00 | 0.85 – 1.15 |

### Las tres restricciones que hacen honesto el sorteo
1. **Un solo mundo por corrida, compartido por las cuatro escenas.** Si el par gemelo no comparte
   decorado deja de ser gemelo, y el examen VOE mediría **la mesa** en lugar de la imposibilidad.
   Es el error que más fácil habría sido cometer al arreglar el otro.
2. **RNG propio, desplazado.** Si el mundo y el balbuceo salieran del mismo generador, cambiar uno
   cambiaría el otro y no se sabría cuál de los dos movió el resultado.
3. **El objeto sigue fuera del alcance del brazo** (base en x=0, tres eslabones de 0.22 = 0.66 de
   alcance; x ≥ 0.85). **Variar la caída NO es dejar que el brazo la toque.** Eso es otra pregunta
   —una mucho mayor, la de la manipulación— y necesita su propia firma.

## El defecto por omisión no se mueve
Sin `--variar`, la escena es **bit a bit** la de la primera ronda. Es lo que permite que el
INFORME-39, el INFORME-41 y los nodos H-002 sigan valiendo tal como están escritos, y es un caso
congelado del banco, no una promesa.

## Regla 31 declarada antes de correr (cuatro casos nuevos, sobre los siete que ya existían)
| Caso | Qué exige |
|---|---|
| **Mundo variable** | 5 semillas dan 5 valores **distintos** de cada uno de los 4 parámetros. Sin esto, la "segunda ronda" sería la primera con otro nombre |
| **El defecto no se movió** | sin `mundo`, la escena es idéntica bit a bit a la de la 1ª ronda |
| **Gemelos con mundo variable** | `apoyado` y `atraviesa` coinciden exactamente hasta el paso en que el objeto alcanza la mesa |
| **La escalera en un mundo ajeno** | el escalón 1 sigue declarando `altura` (o `vel_z`) con parámetros que no son los congelados. Si solo acertaba con mesa=0.55 y masa=0.25, no habíamos medido física: habíamos ajustado el instrumento a un decorado |

Y en `observador_pasivo.py`, un quinto: **el mundo variable no rompe la comparación** — las tres
condiciones siguen compartiendo decorado (mismo escalón 2) y el control positivo sigue ganando la
frontera. La cura del INFORME-39 podía destruir justo lo que el prereg-32 mide; se comprueba en el
dato, no en la intención.

## Qué se corre
- `p35-soporte-variable-s{1..5}` — la escalera del prereg-29 en cinco mundos distintos.
- `p35-pasivo-variable-s{1..5}` — las tres condiciones del prereg-32 en esos mismos cinco mundos.

## La predicción, comprometida ANTES de correr
**Espero que ambas repliquen igual.**
- La escalera, porque el señuelo de ruido ya demostró que el criterio discrimina por la razón
  correcta y no por el decorado.
- El empate del prereg-32, porque es una comparación **entre condiciones dentro de cada semilla**, y
  ahí ya había variación real (0.0948 a 0.1951) sin que la diferencia se acercara nunca al umbral.

**Si la escalera NO replicara**, el INFORME-39 se habría escrito a tiempo y el nodo que propuse no
escribir se habría ahorrado. Ese es exactamente el motivo de no haberlo escrito.

## Criterios (5 semillas)
- **Escalera CONSEGUIDA** si en ≥4/5 mundos: escalón 1 declara `altura`/`vel_z` como único apto,
  escalón 2 supera su nulo, y ambos exámenes VOE superan 0.05 con nulo natural < 0.05.
- **Empate CONFIRMADO** si la diferencia de física de soporte no supera 0.05 en ≥4/5 mundos.
- **Si los números vuelven a salir idénticos entre semillas**, el instrumento sigue ciego a la
  variación y esto se declara **no concluyente**, no conseguido.

## Qué NO se autoriza
- **El brazo no toca el objeto.** Ese cambio no está en este prerregistro.
- Los umbrales del prereg-29 y del prereg-32 (**piso 0.30, techo 0.05, horizonte 8, ciclo 60, 900
  pasos, umbral de diferencia 0.05**) **no se tocan**: si se movieran a la vez que el mundo, no se
  sabría qué produjo el cambio. Quedan congelados donde están.
- Los rangos de esta tabla quedan **congelados aquí**.

## Firmado
Leo, director — 10-ago-2026, aprobación en conversación ("adelante con todo").
