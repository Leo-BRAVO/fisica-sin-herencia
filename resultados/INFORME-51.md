# INFORME-51 — G14 REPRUEBA: su "ignorancia curable" sube igual con pocos datos que con mucho ruido
**10 de agosto de 2026. Acta parcial del prerregistro-43. Hallazgo de ingeniería. No genera nodo.**
**Datos crudos:** `resultados/p43-g14-incertidumbre/medida.json`. Módulo: `codigo/incertidumbre.py`.
**VEREDICTO, con las mismas palabras que el archivo de datos:** *REPROBADO: la ignorancia curable
sube igual con pocos datos que con mucho ruido.*

---

## 1. EL CRITERIO QUE ESTABA ESCRITO, y cómo salió
El prerregistro-43 declaró, **antes de correr**, el lado negativo de G14:

> *"con ruido puro, la parte **curable** debe ser ~0"*

**No lo es.** La medida:

| ruido fijo 0.5, cambia el número de datos | epistémica |
|---|---|
| n = 30 | 0.1432 |
| n = 100 | 0.0955 |
| n = 400 | 0.0374 |
| n = 1600 | 0.0170 |

| n fijo 100, cambia el ruido | epistémica |
|---|---|
| ruido = 0.1 | 0.0191 |
| ruido = 0.5 | 0.0955 |
| ruido = 2.0 | 0.3820 |
| ruido = 8.0 | 1.5279 |

**Multiplicar el ruido por 5 multiplica la "ignorancia curable" por 5.** La ficha de sanidad lo
cuantificó: el ruido explica un **43.3% EXTRA** de la lectura epistémica.

## 2. QUÉ SIGNIFICA, sin adornos
La epistémica que G14 publica es, en el fondo, **σ/√n**: el error estándar del ajuste. Sube cuando
hay **pocos datos** y sube cuando hay **mucho ruido**, y **no distingue una causa de la otra**.

**Y eso importa porque G2 (curiosidad) lee este número para decidir dónde mirar.** Una región muy
ruidosa e imposible de aprender **le parece a Diego una región muy prometedora**. Es exactamente el
fallo del televisor ruidoso — el mismo que `atencion.py` tiene una prueba congelada para evitar, y
que aquí entra por otra puerta.

## 3. LO QUE **NO** SE HACE
- **No se toca `incertidumbre.py`.** El arreglo probable —reportar la epistémica **relativa** a la
  aleatoria en vez de en bruto— cambia lo que significa el número que otros órganos ya leen. Eso es
  un cambio de instrumento y va con prerregistro propio, no con una edición hoy.
- **No se sella G14.** Reprobó, y queda escrito como **reprobado**, no como pendiente.
- **No se degrada nada del pasado todavía.** Hay que medir cuánto pesó esto en las decisiones de
  curiosidad ya tomadas, y eso es otro estudio.

## 4. LO QUE SÍ SE HACE HOY
`codigo/reglas.py` lleva ahora un registro que distingue **"no examinado"** de **"examinado y
REPROBADO"**, con la causa y el acta de cada uno. Hoy hay dos reprobados: **G9** (por el motor
simbólico, INFORME-50) y **G14** (éste). Un órgano reprobado que figura como "pendiente" es una
deuda disfrazada de tarea.

## 5. LA PREGUNTA QUE ABRE (Regla 18)
> **¿Cuánto de lo que Diego ha elegido explorar lo eligió por ruido y no por ignorancia?**
> Se contesta re-corriendo las decisiones de curiosidad ya tomadas con la epistémica **relativa**
> y viendo si habría elegido otra cosa. No se hace hoy.

## 6. EL BALANCE HONESTO DE LA JORNADA
Se pasaron por la puerta **cuatro órganos** que llevaban meses publicando sin examen. **Dos
pasaron** (`contingencia`, `torneo_ojos` — este último tras arreglarle un bug que impedía correr su
tercera lectura) y **dos reprobaron** (`sueno`, `incertidumbre`). **Quedan 11 sin examinar.**

**Una tasa de reprobación del 50% en los primeros cuatro no es una buena noticia disfrazada de
diligencia: es la medida de cuánto llevábamos sin mirar.**
