# Enmienda 01 al prerregistro 01 — 9 de julio de 2026

**Qué se cambia:** la línea base del umbral pasa de "predictor de velocidad constante" a "el mejor de dos predictores triviales: velocidad constante y media del entrenamiento". El umbral sigue siendo 50% del error de esa línea base.

**Por qué:** la primera semilla de la prueba nula de ruido reveló que la base de velocidad constante es patológicamente mala en datos sin estructura (error 4,540,404 en ruido) — tan mala que una ecuación sin habilidad real (error 1,573,272, dos veces peor que predecir la media) la "superaba". La vara vieja habría hecho gritar falsa alarma a la Regla 11.

**Efecto sobre los resultados ya obtenidos (verificado con números):**
- Datos reales: la base combinada no cambia (min(0.3036, 664,760) = 0.3036) → el veredicto del piloto (2/3 semillas superan) queda EXACTAMENTE igual. Además, las ecuaciones del piloto superan a la base de la media por un factor de ~4.5 millones.
- Nulo de ruido: con la vara nueva (umbral = 0.5 × 764,798 = 382,399), la semilla 1 (error 1,573,272) FRACASA correctamente.
- Nulo barajado: se evaluará con la vara nueva cuando termine.

**Naturaleza de la enmienda:** endurece la vara (nunca la afloja) y se registra ANTES de conocer el resultado del nulo barajado. La detectó el propio protocolo (Regla 11 haciendo su trabajo: los verdugos también auditan la vara).

**Decisión:** aplicada por el orquestador como corrección de defecto evidente, reportada al director en conversación en el momento.
