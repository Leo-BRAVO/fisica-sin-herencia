# Prerregistro 10 — Réplica entre OBJETOS que caen (Morpheus: apple, marker, tape) — 10 de julio de 2026
**Continuación declarada en prereg-08 ("necesita más datos") e INFORME-08. Registrado ANTES de tocar los datos nuevos.**

- **Pregunta:** la firma de la caída — término constante aditivo, solo en la señal vertical — ¿se replica en OBJETOS distintos (manzana, marcador, cinta) del mismo laboratorio?
- **Datos:** experimentos falling_apple, falling_marker y falling_tape de Morpheus (CC-BY-4.0), extracción propia con `extraer_posiciones.py`. Pocos videos por objeto: el último video (orden alfabético) de cada objeto queda como juez; el resto entrena.
- **Qué se corre:** `descubrir_pool.py` por objeto, 5 semillas (1–5), maxsize 15, 400 iteraciones.
- **Éxito (por replicación estructural, no por umbral):** en cada objeto, ≥3/5 semillas producen ecuación de v2 con término CONSTANTE ADITIVO (magnitud entre 5 y 40), y las ecuaciones de v1 no lo muestran. Predicción adicional comprometida: si la escala de cámara es compartida entre experimentos, la constante será ≈15.3 (±10%); si difiere, la PRESENCIA (no el valor) es el criterio.
- **Éxito global:** los 3 objetos muestran la firma → nace nodo por replicación estructural (caída de Michigan-bola + manzana + marcador + cinta = 4 objetos independientes). 2/3 = parcial, se registra. ≤1/3 = fracaso de la hipótesis de universalidad, se registra tal cual.
- **Los MSE por señal se REPORTAN (transparencia) pero no gobiernan el veredicto — motivo en INFORME-08: la ley es lineal-con-constante y el piso de ruido coincide con el umbral del 50%.**
- **Firmado:** Leo, director — 10-jul-2026 (flujo aprobado con su "adelante" y el OK al re-planteo).
