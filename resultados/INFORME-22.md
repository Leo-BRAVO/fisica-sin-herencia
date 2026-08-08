# INFORME 22 — La cuarentena resuelta desde la nube: Michigan cae, la caída sobrevive con otra cara — 8 de agosto de 2026

## Contexto (y por qué esto es un hito operativo)
El director quedó sin su máquina personal (los datos viven allá). Solución ejecutada: **los datos
se RECONSTRUYERON desde sus fuentes públicas originales en la máquina de la nube** (Mendeley
7yd2ntbh3w para Michigan; HuggingFace physics-from-video/morpheus-real-world para la caída), con
los mismos scripts del repo (`preparar_mendeley.py`, `extraer_posiciones.py`) y verificación por
**huella digital**: la base trivial y el rival lineal recalculados sobre los datos reconstruidos
debían coincidir con los números registrados en los resúmenes históricos.
- Michigan: desviación 3.4×10⁻¹⁵ (idénticos a precisión de máquina).
- Caída: desviación **0.0 exacta** (extracción byte a byte igual).
**Esto demuestra de paso la Regla 14 (replicabilidad): cualquier persona con el repo puede
reconstruir los datos y reproducir cada número. El proyecto ya no depende de ninguna máquina.**

## Qué se corrió (los items encolados por la AUD-EXT-01, con la herramienta corregida)
Re-validación de E2-N-004 (en cuarentena): `conservada.py --nulo surrogado` (el nulo que aprueba
la Regla 31) sobre ambos mundos, con los criterios ORIGINALES de los prerregistros 16 y 17.
Más `dimension.py` (dimensión intrínseca) en ambos.

## Resultado en una frase
**El nulo honesto partió el nodo en dos: las candidatas estrella de AMBOS mundos eran artefactos
de la suavidad de las señales (jueces las rechazan con ratios ~1), PERO en la caída una candidata
DISTINTA cumple el criterio completo del prerregistro-16 — se conserva 250–300× mejor que su
falsificación en los dos jueces limpios y se rompe EXACTAMENTE en video_9, el video que la
forense ya había marcado como corrupto.**

## Los números
| Mundo | Con el nulo viejo (13-jul) | Con el nulo honesto (hoy) |
|---|---|---|
| **Michigan (ángulos)** | 8 "serias", juez 0.0023 → "éxito pleno" | 1 seria marginal (0.166) y el juez la RECHAZA (ratio 1.02) → **FRACASO — se retira del nodo** |
| **Caída (píxeles centrados)** | 3 "serias", la estrella con score 0.0002 | la vieja estrella REFUTADA (jueces 0.64–1.03); **la candidata #1 (score 0.108) VALIDA: jueces limpios 0.0041 y 0.0032, rompe solo en video_9 → criterio prereg-16 CUMPLIDO con confirmación forense cruzada** |

Traducción de los ratios: la candidata sobreviviente de la caída es ~250× más constante que su
versión falsificada en videos jamás vistos; en Michigan, la "conservación" entera se explicaba
por el espectro de las señales — era el instrumento viejo halagándose a sí mismo.

## Dimensión intrínseca (primera medición del proyecto — la casilla de Columbia)
- **Michigan (péndulo doble):** TwoNN ≈ 2.5–3.1 — el sistema visita un espacio de ~3 dimensiones
  (menos que las 4 señales observadas: hay estructura, no ruido llenando el espacio).
- **Caída:** TwoNN ≈ 2.3 con participación PCA ≈ 1.2 — dinámica esencialmente de baja dimensión.
- Reportes en `resultados/dimension-*`. (Lectura fina y comparación: lado del comparador, solo director.)

## Consecuencia sobre el árbol (aprobación de poda ya dada por el director: "poda las hojas que están mal, las apruebo")
**E2-N-004 SALE DE CUARENTENA, REDUCIDO Y MÁS FUERTE:** se retira todo lo de Michigan y la vieja
candidata estrella; queda SOLO la candidata sobreviviente de la caída, ahora validada contra el
verdugo honesto (lo que ningún resultado del nodo original podía decir). El nodo reescrito
registra ambas cosas: lo que murió y por qué, y lo que sobrevivió y contra qué.

## Lo que queda pendiente (y cómo correrlo SIN máquina personal ni PowerShell)
1. **Los 2 verdugos surrogados de PySR** (e2-mendeley-i2 y p14-final) — necesitan Julia/PySR:
   quedan para el **segundo cuerpo** (GitHub Actions): `estudios-nube.yml` ahora sabe
   RECONSTRUIR los datos públicos antes de correr (`reconstruir_datos.py`, con las mismas
   huellas de verificación). El director los dispara con un clic desde el navegador
   (pestaña Actions → estudios-nube → Run workflow).
2. **Dimensión del dp Morpheus** — requiere el rastreo de 2 cuerpos; va con la misma vía.
3. Los latentes p14 no son reconstruibles sin re-entrenar ojos (torch) — también vía Actions.
