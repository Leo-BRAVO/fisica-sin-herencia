# Prerregistro 27 — El torneo de sus ojos: A vs B vs C vs Ranuras, con acta de la Regla 33 — 9 de agosto de 2026
**Estado: FIRMADO por el director el 9-ago-2026 ("adelante con todo") — aprobación en la
conversación donde pidió el plan para arreglar los ojos y dio luz verde a ejecutarlo completo.**

## Por qué (el problema medido, no supuesto)
El hito 0 quedó conseguido por su cuerpo (INFORME-36), pero **la visión no se une de forma
estable**: 1 de 5 semillas fuerte, el resto débil o nula. Es la misma cojera de los INFORMES
30–33: sus ojos leen escena, no movimiento. Ya construimos cuatro arquitecturas candidatas y cada
una aprobó su propia Regla 31 por separado. Lo que falta es hacerlas competir **entre sí, sobre el
mismo mundo**, con un acta — que es exactamente para lo que existe la Regla 33 (filogenia).

## Los cuatro competidores (ninguno nuevo; hoy se enfrentan)
- **A — píxel** (`ojos_gimnasio.py`): reconstrucción de imagen. La línea base histórica.
- **B — predictivo** (`percepcion2.py`): predice el latente siguiente, estilo JEPA.
- **C — descarga corolaria** (`percepcion2.py` con comandos): B + copia eferente de sus órdenes.
- **R — ranuras** (`ranuras.py`): K mapas de atención espacial. **Frontera gris**: no entra al
  genoma pase lo que pase hoy; solo se mide cuánto vale el prior "hay cosas separadas".

## Diseño
- **Mismo mundo, mismas semillas, mismos jueces** para los cuatro: 12 episodios × 1500 cuadros,
  modo `normal`, jueces [10,11,12] — igual que el hito 0 oficial, para que el resultado sea
  comparable línea a línea con el INFORME-36.
- **Aptitud (prerregistrada, del lado de los jueces, `filogenia.aptitud`):** margen medio de
  contingencia sobre el nulo + bono por número de canales propios hallados. Ningún competidor la
  ve ni la calcula sobre sí mismo.
- **5 semillas de repetición** (como el hito 0): el ganador debe repetir, no solo ganar una vez.
- **Regla 31 del estadio ya aprobada** (`filogenia.py`): gemelos empatan, oráculo arrasa.

## Criterio de victoria (sin huecos, las tres zonas)
Sea `p*` el mejor puntaje medio (5 semillas) y `p₂` el segundo:
- **GANA** un competidor si `p* > 0` (control positivo real, no solo mejor que los demás) y
  `p* − p₂ >` la suma de sus desviaciones entre semillas (separación real).
- **EMPATE TÉCNICO** si `p* > 0` pero no se separa así → gana por parsimonia el más simple
  (orden: A < B < C < R, por número de parámetros y de supuestos), registrando que fue navaja.
- **NINGUNO SIRVE** si ni el mejor supera 0 con margen → se registra fracaso del torneo visual
  completo; la vista de Diego sigue certificada solo `estructural`, nunca predictiva de su cuerpo.

## Qué pasa con el ganador
Reemplaza a los ojos actuales (A) como línea oficial del Gimnasio en el próximo hito (nivel B
rediseñado, futuros hitos de la cartilla). **R, si gana, NO entra al genoma** — entra como
ablación registrada: el genoma sigue sin asumir que "hay objetos"; el torneo solo mide cuánto
costó no asumirlo.

## Predicción comprometida
Espero que **C gane o empate técnico con B**, y que **A quede último** — es la predicción que ya
sostienen los INFORMES 30–32. Sobre R no tengo predicción firme: nunca compitió contra C en el
mundo real del Gimnasio, solo en el mundo sintético de su propia Regla 31.

- **Firmado:** Leo, director — 9-ago-2026, aprobación en conversación ("adelante con todo").
