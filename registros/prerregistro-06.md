# Prerregistro 06 — Peldaño 2: primer aparato distinto (péndulo simple Zenodo) — 10 de julio de 2026
**Aprobado por el director ("después de probar todo eso vamos al salto al peldaño 2" + solicitud de obtener los datos de internet, 10-jul-2026).**

- **Pregunta del árbol (N-002 p.1 y N-003 p.1):** ¿la estructura descubierta en el sistema Mendeley-DP (valor + cambio + corrección senoidal con constante pequeña) reaparece en un APARATO físicamente distinto, medido por otro equipo humano con otro método?
- **Datos (Regla 25/2):** dataset Zenodo 15569631 (CC-BY-4.0, publicado con el paper arXiv 2506.07301): mediciones de péndulos simples REALES con la app Pendulum Tracker (cámara de teléfono), 14 longitudes distintas (23.5–69 cm). Clasificación: `derivada` (ángulo extraído por rastreo de la app; la columna omega se descarta y los cambios se recalculan). Primera corrida: archivo `dados-quarto-esfera-46.6cm` (1,885 muestras, una sola señal s1).
- **Limitación documentada:** el muestreo es irregular (paso 0.013–0.088 s, medio 0.034 s). La formulación estado→estado siguiente asume paso casi uniforme; la irregularidad actúa como ruido. Se corre igual — los datos reales son así.
- **Qué se corre:** `descubrir.py` (adaptado a una señal), 5 semillas, vara de tres rivales del prerregistro-02.
- **Éxito nivel A:** al menos 3/5 semillas cumplen ambas condiciones de la vara.
- **Éxito nivel B (estructura):** en las semillas exitosas, la mejor ecuación contiene un término trigonométrico (sin o cos) aplicado a la señal — la firma estructural de N-001. NOTA prerregistrada: la constante interna NO tiene por qué ser 0.01746 (el INFORME-04 sugiere que k depende de las unidades y este aparato/medición usa otras); lo que se prueba es la ESTRUCTURA, no el número.
- **Fracaso:** menos de 3/5 en nivel A, o nivel A sin estructura trigonométrica — se registra tal cual.
- **Firmado:** Leo, director — 10-jul-2026.
