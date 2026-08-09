# Prerregistro 29 — La escalera de soporte: el primer no-yo por definición POSITIVA — 9 de agosto de 2026
**Estado: FIRMADO por el director el 9-ago-2026 ("implementemos todo absolutamente todo").**
**Sustituye el método del nivel B del prereg-26, que fracasó limpio 0/5 (INFORME-36).**

## Por qué fracasó el nivel B (diagnóstico, no excusa)
Buscábamos la gravedad como **"lo que NO obedece mis órdenes"** — una definición por ausencia, la
más débil que existe: **el ruido tampoco obedece**. La revisión de la línea Baillargeon (2024)
sobre el paradigma de violación de expectativa dice algo distinto y comprobable: los bebés no
detectan "la gravedad" como fuerza abstracta. Aprenden una **escalera de expectativas de soporte**
— qué pasa cuando sueltas algo, siempre ligada al **contacto**, refinándose por etapas (a los 5.5
meses esperan que caiga si se suelta; a los 6.5, si solo el 15% de la base está apoyada; a los 8,
según el centro de la base). En los bebés, gravedad y causalidad por contacto **son el mismo
sistema**. Nosotros los teníamos como dos hitos separados. Este prerregistro los fusiona.

**Frontera de contaminación, explícita:** la escalera infantil nos dice **qué medir**, jamás qué
responder. Programar "cae si <15% apoyado" sería inyectar el resultado esperado como input. Aquí
solo se construye el mundo donde eso ocurre y se pregunta si Diego lo notó.

## Qué se construye (`codigo/soporte.py`)
Cuatro escenas gemelas en el Gimnasio, dos posibles y dos imposibles:

| Escena | Qué pasa | |
|---|---|---|
| `cae` | el objeto se suelta en el aire y cae al suelo | POSIBLE |
| `apoyado` | el objeto descansa sobre una mesa y no cae | POSIBLE |
| `flota` | el objeto se queda quieto en el aire, sin nada debajo | **IMPOSIBLE** |
| `atraviesa` | el objeto cae y pasa a través de la mesa sólida | **IMPOSIBLE** |

El brazo **balbucea siempre** en las cuatro: es lo que permite preguntar si la caída obedece o no
a sus órdenes. El objeto **se re-suelta cada 60 pasos** — como un bebé que suelta la cuchara una y
otra vez; cada ciclo es una repetición del mismo experimento.

### Escalón 1 — "lo que suelto, cae, siempre igual"
El primer no-yo exige **dos condiciones, no una**:
- **(A) LEGALIDAD** — el canal debe ser predecible desde su propio pasado por encima de un piso
  (0.30). Es la parte **positiva**, la que faltaba: sin ella el ruido puro sería el primer no-yo.
- **(B) NO-MÍO** — conocer los comandos no debe ayudar a predecirlo (≤0.05 sobre su nulo barajado).

Se mide a **horizonte 8 pasos**, no a un paso: con comandos suaves, tres retardos del ángulo
extrapolan casi perfecto y lo que el torque agrega en un paso es del orden de a·dt² — invisible.
La obediencia se ve cuando el efecto se acumula. (Es también la pregunta honesta: nadie siente
que manda su brazo por un paso de simulación.)

### Escalón 2 — "no cae si algo lo sostiene"
La dinámica vertical debe **cambiar según el contacto**. Nulo: barajar la señal de contacto —
destruye exactamente la ligadura afirmada, ni más ni menos (enmienda de la Regla 31).

### Escalón 3 — el examen de sorpresa (VOE)
Un predictor aprendido **solo con escenas posibles** recibe pares **gemelos**: mismo montaje,
única diferencia la (im)posibilidad. Si se sorprende más ante lo imposible, sabe física de soporte.
**Nulo natural de fábrica:** dos escenas posibles del mismo tipo deben dar sorpresa ≈0.

## Regla 31 declarada antes de correr (siete casos)
1. Escalón 1 halla la caída en el mundo normal.
2. **SEÑUELO DE RUIDO** — un canal de ruido puro que tampoco obedece debe ser **rechazado por
   ilegal**. Es la prueba de que el criterio dejó de ser una definición por ausencia.
3. Mundo **sin gravedad** → el escalón 1 no halla caída alguna.
4. Escalón 2 halla la ligadura contacto→no-caída.
5. Examen: flotar y atravesar sorprenden más que sus gemelos posibles.
6. Nulo natural: dos posibles gemelas no sorprenden.
7. Contacto barajado → el escalón 2 calla.

## Resultado (corrido el 9-ago-2026)
**APRUEBA 7/7.** Escalón 1: el único canal a la vez legal y no-mío es `altura`
(autopredictible 0.5429, obediencia neta 0.0000). El señuelo de ruido: rechazado por ilegal
(autopredictible 0.0035 < piso 0.30) **aunque su obediencia también sea 0** — exactamente el
agujero que hundía al nivel B viejo. Escalón 2: efecto 2.544 vs nulo 0.0406. Examen: flotar
+1.000, atravesar +0.149. Nulo natural: +0.033 y −0.030.

## Tres huecos que su propia Regla 31 cazó, y quedan congelados
1. **Una sola caída dura 15 pasos de 900** → el régimen "sin contacto" quedaba sin muestras y el
   escalón 2 no podía medirse. Cura: re-soltar cada 60 pasos.
2. **El re-soltado es tramoya nuestra**, no física: ninguna ley puede predecir un teletransporte
   que hacemos nosotros. Las ventanas que lo cruzan se **excluyen** de toda medición. Sin esto la
   caída parecía caótica y el escalón 1 coronaba al brazo.
3. **Dos escenas casi estáticas** dan errores de 1e-9 y 1e-10, y su cociente relativo se dispara
   a −0.80 sin que nada haya sorprendido. Cura: **guarda de piso de ruido** — por debajo del propio
   error del modelo sobre lo que ya vio, la sorpresa es cero por construcción.

**Guarda de potencia (como el mínimo de 20 ventanas del detector de contingencia):** por debajo de
**900 pasos** (15 sueltas) el módulo **se niega a dar veredicto**. Medido: con 600 pasos el nulo
natural reprueba por falta de muestras, no porque el mundo sorprenda.

## Criterio del hito (5 semillas, como el hito 0)
- **CONSEGUIDO** si en ≥4/5 semillas: escalón 1 declara `altura` (o `vel_z`) como único apto,
  escalón 2 supera su nulo, y ambos exámenes VOE dan sorpresa > 0.05 con nulo natural < 0.05.
- **PARCIAL** si los escalones 1 y 2 replican pero el examen no.
- **FRACASO LIMPIO** si el escalón 1 no replica — y se registra como se registró el anterior.

## Qué NO se afirma
- Esto no es física del universo: es PyBullet haciendo de mundo. El nodo será `sobre-el-simulador`.
- No se afirma que Diego "entienda la gravedad": se mide si distingue lo posible de lo imposible
  en su propio mundo, que es una afirmación mucho más pequeña y mucho más comprobable.
- Los umbrales (piso 0.30, techo 0.05, horizonte 8, ciclo 60, 900 pasos) quedan **congelados aquí**.

## Firmado
Leo, director — 9-ago-2026, aprobación en conversación.
