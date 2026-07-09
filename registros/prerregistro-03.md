# Prerregistro 03 — Réplica en Trials 2 y 3 (pregunta 2 de N-001) — 9 de julio de 2026

- **Pregunta del árbol que responde:** ¿la regularidad de N-001 — su estructura y sus constantes k1 ≈ 0.01747 y k2 ≈ 0.0180 — reaparece en corridas físicas distintas del mismo sistema (Trials 2 y 3, condiciones iniciales diferentes)?
- **Qué se corre:** `descubrir.py` sobre `trial2_50hz.csv` y `trial3_50hz.csv` (mismo procesamiento que Trial 1: submuestreo genérico a 50 Hz, 3,883 muestras cada uno). **5 semillas por trial** (presupuesto de cómputo; la replicación de estructura requiere menos semillas que el descubrimiento inicial — la unanimidad 10/10 del Trial 1 ya está establecida). Misma vara de tres rivales del prerregistro-02, calculada sobre los datos de cada trial.
- **Éxito de réplica (dos niveles, prerregistrados):**
  - **Nivel A (predicción):** al menos 3 de 5 semillas de cada trial cumplen ambas condiciones de la vara.
  - **Nivel B (estructura):** en las semillas exitosas, las mejores ecuaciones contienen términos `sin(...)` cuyo argumento incluye una constante multiplicativa en el rango [0.0170, 0.0185] (o su equivalente como división). Se verifica por inspección de las ecuaciones guardadas, no por ajuste posterior.
- **Fracaso:** cualquier trial que no alcance nivel A, o que alcanzándolo no muestre nivel B — se registra tal cual y N-001 gana una pregunta nueva en vez de confirmación.
- **Firmado:** Leo, director — aprobación de avance dada en conversación (9-jul-2026); esta réplica es el "siguiente paso" declarado en INFORME-02.
