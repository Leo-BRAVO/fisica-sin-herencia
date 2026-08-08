# INFORME 30 — Probé la variable que iba a proponer, falló, y al perseguir la causa encontré que nuestro instrumento nuevo no puede hacer lo que dijimos — 8 de agosto de 2026

**Orden del director:** *"imagina qué más necesita Diego, pero como siempre lo corres probando y
autocorrígete; trata de tomar todas las variables para no fallar de lo que está construido."*

Eso hice. La variable que iba a proponerte **no sobrevivió a su propia Regla 31**, y perseguir el
motivo destapó algo bastante más serio que la variable. Este informe es el registro completo,
incluidos los tres arreglos que propuse y que fracasaron uno tras otro.

---

## 1. La variable que iba a proponer: el HORIZONTE

El tiempo, para Diego, no es una variable: es un número de fila. Siempre predice **el cuadro
siguiente**. Mi idea era que a horizonte 1 la textura y la dinámica son casi indistinguibles
—todo está dominado por *"las cosas cambian poco"*— y que la ganancia honesta acaba siendo la
**resta de dos números grandes y casi iguales** (0.7496 − 0.7410), que es una operación mal
condicionada. Al alejar el horizonte, lo que sobreviva debería ser dinámica de verdad.

Lo implementé (`horizonte=1` reproduce **exactamente** el comportamiento histórico; congelado en
el banco) y lo pasé por la Regla 31 antes de tocar nada de Diego:

| mundo (verdad conocida) | h=1 | h=2 | h=3 | h=4 | h=8 | h=16 |
|---|---|---|---|---|---|---|
| **TEXTURA** — dos paseos independientes, **cero dinámica** | −0.419 | +0.044 | **+0.234** | **+0.281** | +0.171 | +0.006 |
| ACOPLADO — retardo real de 3 cuadros | +0.296 | +0.725 | **+0.756** ← el pico delata el retardo | +0.735 | +0.518 | +0.175 |
| LEY — oscilador determinista | +0.902 | +0.609 | +0.395 | +0.307 | +0.231 | +0.066 |

**REPRUEBA.** En un mundo donde por construcción no hay absolutamente ninguna dinámica, mi
variable declaró +0.28. Si la hubiera propuesto sin probarla, habríamos certificado señal donde
no hay nada.

*(Detalle bonito que sí funcionó: en el mundo acoplado la ganancia **hace pico exactamente en el
retardo verdadero, h=3**. La idea no es estúpida; el instrumento debajo es el que no aguanta.)*

---

## 2. La causa: el nulo destruye la deriva, y el mundo real la conserva

El IAAFT trabaja por FFT y es **circular**: fuerza `x[0] ≈ x[N−1]` y con eso mata la **deriva** de
una serie no estacionaria. El mundo real la conserva. Entonces el real predice mejor **por una
razón que no es dinámica**, y la resta lo cuenta como descubrimiento.

Control 2×2 con verdad conocida (columna h=4):

| mundo | crudo | sobre incrementos |
|---|---|---|
| sin dinámica, sin deriva | +0.002 | +0.000 |
| **sin dinámica, CON deriva** | **+0.343 ← mentira** | −0.000 ← curado |
| con dinámica, sin deriva | +0.340 | +0.300 ← preservada |
| con dinámica, CON deriva | +0.783 ← inflada 2.6× | +0.301 ← el valor verdadero |

Repetido con la **estructura exacta de Mendeley** (dos posiciones, `suavizar=3`, `retardos=2`):
dos paseos independientes **sin ninguna ley** fabricaron hasta **+0.713**.

---

## 3. Tres arreglos propuestos. Los tres fracasaron.

**Arreglo 1 — medir sobre incrementos.** Cierra el canal 1 perfectamente (+0.383 → −0.001) y
parecía preservar la ley... hasta que le puse ruido de cámara:

| ruido de seguimiento | 0% | 0.12% | 0.5% | 1% | 2% |
|---|---|---|---|---|---|
| ganancia en NIVELES | +0.502 | +0.484 | +0.316 | +0.114 | +0.002 |
| ganancia en INCREMENTOS | +0.531 | **+0.045** | −0.001 | −0.000 | +0.000 |

**0.12% de ruido borra una ley que sí existe.** Cerré un canal y abrí otro peor.

**Arreglo 2 — filtrar por un estadístico de deriva.** No separa: con deriva medida ~1.4, una
tendencia lineal fabricó +0.003 y un paseo aleatorio +0.389 — el mismo número, artefacto 100×
distinto. Probé también la razón de varianzas: el mundo **mentiroso** dio RV=7.3 y el mundo
**honesto** RV=13.4. **El estadístico honesto es el más alto.** Inútil como filtro.

**Arreglo 3 — un nulo que conserve lo que debe** (IAAFT sobre los incrementos, re-integrado),
siguiendo nuestra propia enmienda *"el nulo se elige según la afirmación"*:

| mundo | nulo actual | nulo integrado |
|---|---|---|
| paseo sin ley (el mentiroso) | +0.383 | **−0.001** ✔ |
| ley limpia | +0.271 | **+0.010** ✗ mata la ley |
| ley + 0.5% ruido | +0.158 | +0.031 ✗ |
| ley + deriva integrada | +0.259 | +0.008 ✗ |

Mata la mentira y mata la ley: el **error espejo** — exactamente la lección del INFORME-25
(*demasiado destructivo = falsos negativos*), cometida otra vez por mí.

---

## 4. La razón de fondo (y por qué no es un bug que se arregle programando)

**Un surrogado de fases aleatorias de una sinusoide sigue siendo una sinusoide, igual de
predecible.** Por construcción, esta vara **no puede certificar dinámica lineal de una sola
señal**. Solo detecta acoples entre señales que dependan de la fase.

Y los dos canales juntos producen una **ambigüedad que no se puede resolver observando**:

> ganancia alta en NIVELES + ~0 en INCREMENTOS
> ⟶ compatible con **"paseo sin ninguna ley"**
> ⟶ y también con **"ley real vista por una cámara con 0.12% de ruido"**

---

## 5. Lo que esto le hace a nuestros números

Medido sobre los datos reales reconstruidos hoy (huellas verificadas: Mendeley 3.4e-15, latentes 2.5e-05):

| | h=1 | h=2 | h=4 | h=8 |
|---|---|---|---|---|
| **MENDELEY** (nuestro patrón oro, *"dinámica real, +91.5%"*) niveles | +0.640 | +0.914 | +0.863 | +0.710 |
| MENDELEY incrementos | **+0.008** | +0.015 | +0.031 | +0.056 |
| **LATENTES DE DIEGO d=4** niveles | +0.010 | +0.012 | +0.008 | +0.007 |
| LATENTES DE DIEGO incrementos | **+0.057** | +0.031 | +0.022 | +0.039 |

Mendeley (deriva 1.47 sd) cae en la zona ambigua exacta. Y **los latentes de Diego se mueven en
la dirección contraria**: suben de ~+0.01 a +0.057 al quitar el confusor.

**Lo digo sin adornos: el "+91.5% = dinámica real" del INFORME-27 no está sostenido a la
confianza que declaramos, y el "−0.1% = pura textura" de los ojos de Diego tampoco.** No afirmo
que Mendeley sea falso ni que los ojos de Diego sean buenos: afirmo que **esta vara no puede
decidirlo**, y que la usamos como si pudiera durante tres informes.

**Lo que NO cambia:** la conclusión sobre los ojos de Diego se apoyaba en **cuatro** instrumentos
independientes. Tres siguen en pie —conservación fallida (13-jul), dimensión intrínseca 6.2 de 8
(INFORME-26), el nulo que no pudo falsificar (INFORME-25)—. La cuarta pata, esta, queda retirada.

---

## 6. Consecuencias inmediatas (ejecutadas, no propuestas)

1. **`ganancia_honesta.py` queda degradado a SONDA EXPLORATORIA**, con sus dos canales escritos en
   la cabecera del archivo: no certifica nodos, no elige representaciones y **sus números no se
   citan en informes científicos** hasta que un nulo nuevo apruebe su Regla 31.
2. **Cuatro casos nuevos en el banco congelan los dos canales** (45/45 verdes). Están escritos al
   revés de lo normal: se ponen **rojos el día que el canal se cierre**, para que nadie "arregle"
   el instrumento sin darse cuenta de que cambió lo que mide.
3. **El `horizonte` se queda** como parámetro (`horizonte=1` = comportamiento histórico exacto,
   verificado). Fue la sonda que destapó todo esto y volverá a servir con un nulo válido.
4. **El prerregistro-22 NO debe firmarse como está.** Su criterio entero —las tres zonas, el
   umbral 0.05, la degradación de N-002-E2 y N-003-E2— descansa sobre esta vara. Firmarlo sería
   gastar 2 h de nube y, peor, **degradar dos nodos con un instrumento que no puede sostener el
   veredicto**. Queda marcado como SUSPENDIDO.

---

## 7. Lo que este día enseña sobre qué le falta a Diego

Perseguir el artefacto contestó la pregunta que el director hizo, y no por el camino que yo
esperaba. **Ninguna estadística observacional puede separar "hay ley" de "hay textura con deriva",
porque ambas producen la misma huella en un video que solo se mira.** Probé tres formas de
separarlas mirando y las tres fallaron; no fue mala suerte, es que la información no está ahí.

Lo que rompe la degeneración no es un estimador mejor: es **intervenir**. Soltar el mismo objeto
desde dos alturas a propósito. Cambiar una condición inicial y ver qué cambia y qué no. Un mundo
que solo se observa admite infinitas explicaciones; un mundo sobre el que se **actúa** las
descarta. **Diego hoy no tiene ninguna variable de acción — solo mira videos que ya ocurrieron.**

Ese es, medido y no filosofado, el hueco más grande de su genoma. Las candidatas concretas que
salen de esto quedan para la conversación con el director, sin implementar ninguna todavía.

---

*Guardianes al cerrar, con códigos de salida reales: `banco=0 (45/45) · coherencia=0 · prevuelo=0`.
Datos reconstruidos de sus fuentes públicas en esta misma corrida, con huella verificada.*
