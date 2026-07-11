# Prerregistro 11 — Péndulo doble Morpheus: la pregunta inter-aparato con las herramientas nuevas — 11 de julio de 2026
**Aprobado por el director ("ADELANTE pero vamos a hacer 5 o 7 semillas a la vez"). Primer prerregistro que usa las cinco mejoras del taller.**

- **Pregunta del árbol (N-002 p.1 / N-003 p.1, pendiente desde INFORME-05):** en un péndulo doble de OTRO laboratorio, con oscilación grande, medido por rastreo propio de dos cuerpos en coordenadas de imagen (representación distinta a los ángulos de Michigan), ¿emerge estructura de ACOPLE entre los dos cuerpos comparable — canónicamente — a la de N-001?
- **Datos:** 10 videos reales (Morpheus, CC-BY-4.0), extracción PROPIA con el rastreador de dos cuerpos (k-means con continuidad de identidad; 10/10 videos, 0 cuadros perdidos). 4 señales neutras s1–s4 (posiciones de imagen de ambos cuerpos), ~5,213 muestras.
- **Pisos de ruido medidos ANTES de correr (mejora #2):** s1≈19, s2≈31, s3≈20, s4≈29 (medianas; dos videos con pisos altos en s1/s3 — se documenta).
- **Diseño:** entrenamiento en 7 videos; jueces los videos completos en posiciones 3, 6 y 9 (1-indexado, lista ordenada). 5 semillas EN PARALELO (mejora #4). maxsize 20 (4 señales requieren algo más de expresividad que 15), 400 iteraciones.
- **Éxito nivel A (predicción, por señal, informado por el piso):** en ≥3/5 semillas, el error de CADA señal sobre los jueces es < max(50% de su base trivial, 3× su piso mediano) — el término del piso evita exigir lo físicamente imposible (lección INFORME-08).
- **Éxito nivel B (estructura, CANÓNICO — mejora #5, lección v7):** en las semillas exitosas, las tarjetas canónicas muestran ACOPLE: el gradiente de las ecuaciones de un cuerpo tiene componentes no nulas (>0.001) respecto a las señales del OTRO cuerpo, replicado entre semillas. Se registra además si el acople pasa por DIFERENCIAS de señales (la marca de N-001) — deseable pero no exigido (representación distinta).
- **Nivel C (rodado — mejora #3):** se reporta el horizonte multi-paso en los jueces; sin umbral exigido (primer dato de referencia en este aparato).
- **Autopsia (mejora #1) obligatoria tras el veredicto, éxito o fracaso.**
- **Fracaso:** <3/5 en nivel A, o nivel A sin acople canónico replicado — se registra tal cual.
- **Firmado:** Leo, director — 11-jul-2026.
