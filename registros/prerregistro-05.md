# Prerregistro 05 — Transferencia directa entre trials (pregunta 3 de N-002) — 9 de julio de 2026
**Aprobado por el director ("luego la transferencia entre trials").**

- **Pregunta:** ¿las fórmulas descubiertas en el Trial 1 predicen los Trials 2 y 3 SIN re-entrenar? Es la prueba más dura de que una fórmula es ley del sistema y no ajuste a una corrida.
- **Qué se corre:** `codigo/archivo/transferir.py` (archivado 9-ago-2026) toma las ecuaciones de la mejor semilla oficial del Trial 1 (semilla 9, error 0.1461) tal cual están escritas — sin tocar una sola constante — y las evalúa sobre el 30% temporal oculto de los Trials 2 y 3.
- **Éxito prerregistrado:** en cada trial destino, el error de las fórmulas transferidas es menor que el umbral propio de ese trial (50% de su base trivial: 0.2801 en Trial 2, 0.2451 en Trial 3). Sin re-entrenamiento, sin ajuste, sin excepciones.
- **Fracaso:** cualquier trial destino donde no se cumpla — se registra y abre pregunta sobre qué parte de la fórmula era de la corrida y no del sistema.
- **Firmado:** Leo, director — 9-jul-2026.
