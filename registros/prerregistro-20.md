# Prerregistro 20 — BORRADOR — G2 corregido: progreso CON SIGNO sobre auditoría SELLADA, con coste real (G10) — 8 de agosto de 2026
**Estado: FIRMADO — 8-ago-2026, con UNA CORRECCION del orquestador antes de firmar (abajo). Nace de `arbol/ECUACIONES-COMPARADAS.md`: la crítica formal de 2026 a la teoría de Schmidhuber nombra cuatro canales de Goodhart, y nuestra ecuación tenía DOS de ellos abiertos. G10 (interocepción) ya está construido y MIDE; este prerregistro decide si puede DECIDIR.**

- **Qué cambia (tres correcciones, ninguna cosmética):**
  1. **Progreso CON SIGNO:** desaparece el `max(0, ·)`. Cierra el canal nº2 (olvidar-y-reaprender),
     ya demostrado en nuestro propio banco: con recorte, una región que oscila farmea interés
     para siempre; con signo, el ciclo se cancela.
  2. **Medido sobre la AUDITORÍA SELLADA:** los bits de progreso se calculan SOLO sobre los jueces
     congelados de cada región, nunca sobre los datos que la campaña eligió. Cierra los canales
     nº1 (mejorar en el propio flujo) y nº3 (sobreajustar la validación).
  3. **Denominador real:** `coste_sentido` de G10 sustituye al `coste = 1` uniforme. Cierra el
     canal nº4 (perseguir ganancias diminutas a costo infinito).
- **CORRECCION ANTES DE FIRMAR (del orquestador, 8-ago):** el criterio A que yo mismo habia
  escrito era CONFIRMATORIO — pedia que la ecuacion nueva "mantenga el veredicto" de la vieja.
  Eso no es una prueba, es un chequeo de consistencia: una metrica no se valida pidiendole que
  este de acuerdo con la que reemplaza. **El criterio correcto es ADVERSARIAL: la ecuacion nueva
  debe SOBREVIVIR un ataque que MATA a la vieja.**
- **Éxito nivel A (ADVERSARIAL, criterio corregido):** se construye de antemano un ataque de
  Goodhart —una region que oscila (aprende, olvida, reaprende)— y se exige:
  (a) la ecuacion VIEJA le asigna interes alto y sostenido (cae en la trampa);
  (b) la ecuacion NUEVA le asigna progreso ~0 (resiste).
  **Ya demostrado y congelado en el banco.** Ademas, sobre las dos decisiones historicas del
  prereg-18b, la nueva no debe elegir la region esteril (se conserva como criterio secundario,
  no como validacion).
- **Éxito nivel B (Regla 31 del gen, obligatorio antes de cualquier decisión real):**
  1. memoria plana → aburrimiento universal (ya congelado en el banco);
  2. memoria que OSCILA → progreso ≈ 0 con signo, y > 0 con recorte (la demostración del defecto);
  3. el coste sentido correlaciona con el tiempo real de reloj (r > 0.7 sobre ≥ 5 campañas con
     `tiempo_fiable = true`). **Hoy no hay ninguna: el tiempo deducido del disco es falso en un
     clon de git, y así queda marcado en cada registro.** El latido ya mide el reloj de verdad;
     este criterio se evalúa cuando existan las 5.
- **Prohibición explícita mientras no se firme:** `interocepcion.py` MIDE y REGISTRA, pero su
  `coste_de()` NO entra al denominador de `curiosidad2.py`. Un órgano nuevo se enciende después
  de saber que no miente, no antes.
- **Fracaso:** se registra tal cual; abriría la pregunta de si el corpus histórico (27 campañas,
  ninguna con tiempo fiable aún) alcanza para calibrar un coste, o si eso debe esperar al Gimnasio.
- **Firmado:** PENDIENTE — Leo, director.
