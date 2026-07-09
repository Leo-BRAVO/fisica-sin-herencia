# Prerregistro 04 — Test de re-escalado (pregunta 2 de N-002) — 9 de julio de 2026
**Aprobado por el director en conversación ("vamos como tú sugieras: el test de re-escalado y luego la transferencia").**

- **Pregunta:** ¿la constante k ≈ 0.01746 depende de las unidades de los datos o es intrínseca al sistema?
- **Qué se corre:** los datos del Trial 1 multiplicados por 100 (s1×100, s2×100 — transformación matemática neutra y documentada), `descubrir.py`, 3 semillas, misma vara de tres rivales (calculada sobre los datos re-escalados).
- **Predicciones prerregistradas (una debe cumplirse):**
  - **Resultado A (k es del lenguaje de medición):** la estructura sin(...) persiste y la constante aparece re-escalada inversamente, k' ≈ k/100 ∈ [0.000170, 0.000185] (o equivalente como división).
  - **Resultado B (k es intrínseca):** la constante aparece SIN re-escalar, en [0.0170, 0.0185].
  - **Resultado C (fracaso informativo):** la estructura no se replica en datos re-escalados — abriría pregunta sobre sensibilidad del motor a la escala.
- **Interpretación comprometida de antemano:** A implica que k pertenece al sistema de unidades en que el instrumento reportó los datos (sigue siendo un descubrimiento sobre el LENGUAJE de los datos, no sobre la dinámica); B la elevaría a candidata a constante dinámica del sistema. Ninguno de los dos invalida N-001/N-002 — precisan su significado.
- **Firmado:** Leo, director — 9-jul-2026.
