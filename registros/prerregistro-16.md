# Prerregistro 16 — F3: minería de cantidades conservadas en la caída — 13 de julio de 2026
**Primera campaña de la herramienta conservada.py (construida por modelo delegado bajo especificación y revisión del orquestador; banco de pruebas aprobado). Nota de gobernanza: la ejecución de construcción del obrero fue prueba de sandbox (Regla 30); esta es la corrida OFICIAL — determinista, semillas fijas, reproduce los mismos números.**

- **Pregunta:** ¿existen combinaciones de las señales de la caída (posiciones y cambios, centradas, grado 2) cuyo valor casi no cambie en el tiempo — cantidades conservadas?
- **Método:** minimización de la razón varianza-del-cambio / varianza-total sobre base de funciones (variante gobernada de análisis de rasgos lentos), resuelta exacta por autovalores. Control negativo INTEGRADO: el piso del azar = mediana de 20 corridas con orden temporal permutado; score = lambda/piso.
- **Datos:** 11 videos de caída, crudos (sin suavizar — lección INF-18), centrados; jueces: videos en posiciones 3, 7, 11 (fuera del entrenamiento).
- **Éxito nivel A:** ≥1 candidata SERIA (score < 0.2 — al menos 5× más constante que el azar).
- **Éxito nivel B:** esa candidata, evaluada en réplicas juez, muestra ratio_juez < 0.2 en AL MENOS 2 de los 3 jueces (se admite fallo en video_9, previamente diagnosticado como corrupto por la autopsia — desenfoque de movimiento; si falla EXACTAMENTE ahí, cuenta como confirmación cruzada del diagnóstico forense).
- **Fracaso:** sin candidatas serias, o serias que no validen en jueces limpios.
- **Firmado:** bajo el "Adelante" del director a F3; diseño del orquestador.
