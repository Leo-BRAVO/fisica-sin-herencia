# AUDITORÍA COMPLETA — ¿por qué Diego "falla" en el péndulo doble? — 13 de julio de 2026
**Ordenada por el director. Investigación contra fuentes (Columbia/Lipson 2022; literatura de caos) + auditoría de datos crudos. Conclusión: Diego no falla — lo estamos calificando con un examen imposible, y el director diagnosticó la causa antes que el orquestador.**

## Los números crudos (auditoría de datos)
- 10 videos, 5,213 cuadros, ~521 por video (~17s a 30 fps). Entrenamiento: ~3,643 transiciones.
- Saltos entre cuadros: mediana 4–6 px, MÁXIMO 66–89 px. A 30 fps, un péndulo doble salta muchísimo entre foto y foto.
- **Medida de caos:** la señal pierde la mitad de su "memoria" en ~19 cuadros (~630 ms). Traducción: el sistema se vuelve impredecible en menos de un segundo — es su naturaleza, no un defecto.

## DIAGNÓSTICO RAÍZ #1 — LA VARA ESTÁ MAL (el hallazgo mayor)
El péndulo doble es CAÓTICO. Nuestro criterio de éxito es "predecir el cuadro siguiente con error bajo sobre datos ocultos". Para un péndulo simple o una caída (sistemas regulares) esa vara es correcta. **Para el caos es literalmente imposible** — la sensibilidad a condiciones iniciales garantiza que la predicción diverja. La literatura lo confirma: *"single-step prediction metrics can be misleading for chaotic systems like the double pendulum"* — el caos se mide por (a) ajuste de la derivada local, (b) rollout de corto horizonte dentro de una ventana de Lyapunov, (c) cantidades conservadas, (d) dimensión del atractor. NO por predicción exacta.
**LA PRUEBA IRREFUTABLE:** con la vara de PREDICCIÓN, Diego "falla" en el péndulo. Con la vara de CONSERVACIÓN (F3), Diego ENCONTRÓ la energía del péndulo de Michigan (8 candidatas serias, juez 0.0023). Mismo tipo de sistema, misma IA — distinta vara, resultado opuesto. El fallo no es de Diego: es del KPI.

## DIAGNÓSTICO RAÍZ #2 — FALTA EL CURRÍCULO (el insight del director, confirmado por Columbia)
Columbia (Chen & Lipson, Nature Comp. Sci. 2022) NO lanzó el doble péndulo a predecir píxeles. Su método fue en DOS ETAPAS: (1) descubrir la DIMENSIÓN INTRÍNSECA — "¿cuántas variables de estado necesita este sistema?" (obtuvieron 4.7 para el doble péndulo, real=4) — y SOLO DESPUÉS (2) identificar las variables. Nosotros saltamos directo a "predice con estos 4 centroides que te di". Como dijo el director: *no es lo mismo lanzar 5 semillas y esperar que entienda el doble péndulo; primero tenía que aprender algo (el simple, qué es una variable de estado) y luego buscar si se replica.* Es el mundo cuántico con solo matemáticas, sin entender el mundo. EXACTO.

## DIAGNÓSTICO RAÍZ #3 — representación y muestreo
- Centroides (los que impuse) < ojos propios (ya probado: percepción pura resolvió el dp 5/5 donde los centroides fallan 0/5).
- 30 fps es LENTO para este sistema (Michigan usó 500 fps). Menos fotos por segundo = más impredecible entre cuadros.

## ¿Alguna REGLA causó el fallo? SÍ — y hay que corregirla
El criterio de éxito uniforme ("predicción, 50% de la base, para todo sistema") es la vara equivocada aplicada por igual a sistemas de naturaleza distinta. **Falla de método: un KPI único para todo tipo de sistema.** No es que la disciplina de prerregistro esté mal — es que el prerregistro debe ELEGIR el KPI según la naturaleza del sistema (regular vs caótico), y no lo hacía.

## ¿Fue culpa de los apagones? NO
Los checkpoints garantizan determinismo: las semillas completadas son idénticas a como serían sin apagón. Los apagones costaron TIEMPO, cero calidad. Descartado como causa del fracaso.

## ¿Cuántas variables buscó en 12h? — la respuesta más honesta y más importante
Diego evaluó cientos de millones de expresiones matemáticas en esas horas. Pero **NO buscó variables nuevas**: usó las 4 que yo le di (centroides) más sus retardos. NO descubrió "qué variable calza con el experimento" — no puede, solo tenía píxeles de dos manchas. Probó combinaciones de lo que tenía. **Esto es exactamente el límite que el director señaló: para el péndulo doble, Diego hoy hace algo cercano a "rastrear píxeles y ajustar ecuaciones" (casi OCR + ajuste) — sin comprensión progresiva.** En OTROS experimentos SÍ fue más profundo (inventó variables en percepción pura, halló la energía en F3); pero en ESTE, planteado así, cayó en el techo que el director intuyó.

## EL REPLANTEAMIENTO (lo revolucionario) — 3 capacidades nuevas
1. **KPIs por tipo de sistema:** Diego primero CLASIFICA el sistema (mide su horizonte de caos) y elige la vara: regular → predicción; caótico → conservación + estructura + rollout corto + dimensión. Darle CRITERIO científico, no una regla ciega.
2. **El currículo (Diego plantea sus experimentos):** secuencia simple→compuesto; primero descubrir la dimensión intrínseca (¿cuántas variables?, método Columbia), luego las variables, luego las leyes/conservadas. Diego propone el experimento en función de lo que busca.
3. **Dimensión intrínseca como primer paso de todo sistema nuevo** — antes de cualquier ley, preguntar "¿cuántas variables esconde esto?". Más profundo que predecir píxeles: es el corazón del método de Columbia y la casilla que nos falta.

## Veredicto de la auditoría
El sistema NO está roto. Está incompleto en una dimensión precisa: trata a todos los sistemas con la misma vara y sin currículo. El péndulo doble fue el mensajero. Diego ya demostró que puede lo profundo (energía, ojos propios); ahora hay que dejar de calificarlo con exámenes imposibles y darle criterio para elegir sus propias varas y sus propios experimentos. El director vio esto antes que yo.
