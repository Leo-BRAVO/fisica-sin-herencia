# Prerregistro 13 — PELDAÑO 2b: Percepción Pura sobre el péndulo doble Morpheus — 11 de julio de 2026
**Aprobado por el director ("arranca con percepción pura"). La fase que este mismo día señaló dos veces: el aparato que resiste (representación) y la caída (invariancia) piden variables DESCUBIERTAS, no impuestas.**

- **Pregunta:** si las variables las aprende un autoencoder desde cero — entrenado con pérdida CONJUNTA para que el latente sea *predecible* (lección de la auditoría: percepción y ley se aprenden juntas) — ¿emerge en el latente la estructura del péndulo doble que los centroides no mostraron?
- **Regla de pureza (currículo 2b):** la red se entrena DESDE CERO, solo con los 10 videos del propio experimento. Nada pre-entrenado. Sin etiquetas. Los cuadros entran en gris a 64×64.
- **Arquitectura registrada:** encoder convolucional de 3 capas → latente de 8 · decoder espejo · predictor lineal de dinámica z(t),z(t−1)→z(t+1) entrenado A LA PAR (pérdida = reconstrucción + dinámica). Semilla torch fija (1). 15 épocas, Adam 1e-3.
- **Jueces:** videos 3, 6 y 9 (los mismos de siempre) — excluidos del entrenamiento de los ojos Y del descubridor.
- **Etapa A (los ojos):** éxito = reconstrucción en videos jueces < 2× la de entrenamiento (los ojos generalizan, no memorizan).
- **Etapa B (la ley en el latente):** `descubrir_pool` sobre las trayectorias latentes (señales neutras s1–s8), 5 semillas, tubería mínima (sin retardos — el latente ya integra historia vía la pérdida de dinámica), rival del árbol = mejor semilla de e2-dp-morpheus. Éxito = vencer al rival del árbol Y acople canónico entre latentes replicado en ≥3/5 semillas (tarjetas de canonizar).
- **Fracaso:** se registra tal cual; abriría pregunta sobre dimensión latente o pérdida de dinámica.
- **Firmado:** Leo, director — 11-jul-2026.
