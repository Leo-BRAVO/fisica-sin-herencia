# Prerregistro 08 — Caída libre (Morpheus, peldaño 2) — 10 de julio de 2026
**Aprobado por el director ("avancemos... caída libre para expandir el peldaño 2").**

- **Pregunta:** ¿qué ley descubre el motor en cuerpos cayendo, y esa ley se replica entre experimentos independientes del mismo laboratorio?
- **Datos (Regla 25/2):** benchmark Morpheus (CC-BY-4.0, arXiv 2504.02918, github physics-from-video): 11 videos reales de laboratorio de una pelota cayendo (30 fps, condiciones iniciales variadas). Extracción PROPIA con `extraer_posiciones.py` (píxeles y cuadros — dato crudo, Regla 2; primera vez que el proyecto extrae de video directamente).
- **Diseño (lección v6 aplicada):** entrenamiento con las transiciones agrupadas de 8 videos; juicio sobre los 3 videos COMPLETOS restantes, nunca vistos (posiciones 3, 7 y 11 de la lista ordenada, fijadas aquí). Las transiciones no cruzan fronteras de video.
- **Nota técnica prerregistrada (honestidad sobre el rival lineal):** en la formulación estado→siguiente, un cuerpo con aceleración constante ES un sistema lineal con término constante. El rival lineal se REPORTA pero no se exige vencerlo — exigirlo sería exigir que la caída no sea caída. La prueba real está en el nivel B.
- **Éxito nivel A (predicción):** al menos 3/5 semillas predicen los videos juez con error < 50% de la base trivial.
- **Éxito nivel B (estructura — la firma de la aceleración):** en las semillas exitosas, la ecuación de UNA de las dos señales (y solo una) contiene un término CONSTANTE ADITIVO, replicado entre semillas con variación < 10%. Interpretación comprometida: ese término — algo que se suma igual en cada paso, siempre en la misma dirección, independiente del estado — sería la firma de una influencia constante actuando sobre el cuerpo. La otra señal no debe mostrarlo (o ~0).
- **Fracaso:** menos de 3/5 en nivel A, o constante no replicada, o constante en ambas señales por igual — se registra tal cual.
- **Firmado:** Leo, director — 10-jul-2026.
