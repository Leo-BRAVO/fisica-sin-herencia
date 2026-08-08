# Prerregistro 25 — El segundo intento del hito 0: ojos que predicen en su propio idioma — 8 de agosto de 2026
**Estado: FIRMADO por el director el 8-ago-2026 ("esto igual aprobado, vamos con todo"). Orden adicional: construir TODOS los sistemas del plan antes de lanzar la corrida.** Responde a la pregunta *"¿qué vamos a hacer
con el hito 0 que sigue fracasando a 0.02 del piso?"* — con un plan, no con un piso rebajado.

## El diagnóstico completo (todo medido, nada supuesto)
1. El detector de contingencia acierta **4/4** sobre el estado del simulador. El detector está sano.
2. Los ojos actuales leen la **escena** (+0.66) y no el **brazo** (−0.09/+0.03/+0.21). El fallo
   está en la representación.
3. Cinco vías independientes dicen que la pérdida por reconstrucción de píxeles codifica textura y
   disposición, no dinámica.
4. **La literatura llegó a lo mismo por otro camino:** LeCun (JEPA, 2025-26) — reconstruir píxeles
   condena la representación porque obliga a codificar lo impredecible; la cura es **predecir en el
   espacio latente**, no en el espacio de píxeles. Nuestra evidencia y la suya convergen.

## Las TRES candidatas de ojos (arquitectura = legal; se declaran antes de correr)
- **A. Actuales** (reconstrucción + dinámica en píxel) — la línea base; ya sabemos su resultado.
- **B. Predictivos en latente (estilo JEPA):** la pérdida principal es predecir `z(t+1)` desde
  `z(t), z(t-1)` — la reconstrucción queda solo como regularizador débil (0.1×). Lo impredecible
  deja de costar; el movimiento pasa a ser lo único que paga.
- **C. Predictivos + comandos:** como B, pero el predictor interno también recibe los comandos
  motores. Biología directa (descarga corolaria: el cerebro le avisa a la vista lo que ordenó al
  músculo). Legal: son SUS comandos.

## Protocolo (idéntico al 19/23 salvo lo declarado)
- Cuerpo ganador del prereg-24 (topes ±2.5), 12 episodios × 1500 cuadros, jueces 10/11/12
  congelados, criterio del 23 SIN TOCAR (h=8, ventana 150, piso 0.02, fracción 0.40, ≥20 ventanas).
- Cada candidata se entrena con las MISMAS semillas y episodios. La comparación es entre ojos,
  no entre mundos.
- **Nulo adicional para C** (obligatorio): con los comandos desplazados circularmente en el
  entrenamiento de C, su ventaja debe desaparecer — si no, C aprende del reloj, no del motor.

## Predicciones comprometidas
1. B supera a A en fracción-de-ventanas del mejor latente (los actuales quedaron en 0.38).
2. C supera a B **solo si** la descarga corolaria aporta — si C=B, se registra y gana la más
   simple (B) por navaja.
3. **Éxito del hito 0** = el criterio del prereg-23 se cumple sobre los latentes de la candidata
   ganadora, replicado en ≥4/5 semillas. **Si ninguna candidata lo logra, el hito 0 se registra
   como FRACASO del aparato visual actual** y la siguiente jugada es la frontera gris de las
   ranuras vía filogenia (Regla 33, ablación medida) — no un cuarto retoque del mismo autoencoder.
- **Firmado:** Leo, director — 8-ago-2026 ("esto igual aprobado"). La candidata C (descarga
  corolaria) fue además ordenada explícitamente: "vamos a hacer esto".
