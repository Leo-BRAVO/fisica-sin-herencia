# Prerregistro 02 — Corrida OFICIAL Fase 0, Trial 1 — 9 de julio de 2026
**Aprobado por el director en conversación ("sí avancemos con estas mejoras").**

- **Qué se corre:** `descubrir.py` sobre `trial1_50hz.csv`, 10 semillas (1–10). Las semillas 1–3 se reutilizan del piloto (motor determinista, mismos parámetros — resultado idéntico por construcción). Unidad estándar de error: SUMA de los MSE por señal (el piloto ya comparaba en esta unidad, de forma conservadora).
- **Vara (incluye las dos mejoras aprobadas):** éxito de una semilla = su error sobre el 30% temporal oculto cumple AMBAS condiciones: (a) menor que el 50% de la mejor base trivial (velocidad constante o media, enmienda-01), y (b) menor que el error del RIVAL LINEAL (regresión por mínimos cuadrados sobre las mismas entradas). La condición (b) es nueva y más exigente: si una recta logra lo mismo, no hay descubrimiento no lineal.
- **Éxito de la corrida:** al menos 5 de 10 semillas cumplen ambas condiciones.
- **Fracaso:** menos de 5, o cualquier prueba nula futura que supere esta misma vara.
- **Después:** replicación con Trials 2 y 3 (mismo protocolo, prerregistro aparte).
- **Firmado:** Leo, director — 9-jul-2026.
