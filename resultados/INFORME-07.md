# INFORME 07 — Caída libre, intentos 1 y 2 (prerregistro-08) — 10 de julio de 2026

## Resultado en una frase
**Ambos intentos FRACASAN el nivel A por margen mínimo (la mejor semilla quedó a 2% del umbral), pero la firma comprometida apareció en las 10 semillas: un término constante aditivo, SOLO en la señal vertical — no reclamable bajo el prerregistro, imposible de ignorar como observación.**

## Los hechos
- Intento 1 (semillas 1–5, maxsize 25): 0/5. Tres semillas explotaron sobre los jueces (sobreajuste con ~300 transiciones).
- Intento 2 (semillas 6–10, maxsize 15, 400 iteraciones): 0/5, pero sin explosiones y todas MEJORES que la base trivial (1251–1708 contra 2449). La semilla 8 quedó en 1251 contra umbral de 1224 — a 2.2%.
- **La firma en la señal vertical, en las 10 semillas de ambos intentos:** términos constantes aditivos 15.276 (semillas 6 y 9, idénticas a la MILLONÉSIMA), 15.52 (semillas 2 y 3 del intento 1, idénticas a la milésima), 22.12 (7 y 10), 17.30 (8), 13.9 (4). Siempre sumando, siempre en la misma dirección, siempre SOLO en v2. La señal horizontal jamás lo mostró — exactamente la asimetría comprometida en el prerregistro.

## Diagnóstico del fracaso del nivel A
El criterio exige reducir a la mitad el error TOTAL (suma de ambas señales). Pero la señal horizontal de una pelota cayendo es esencialmente ruido de rastreo sin dinámica — tiene un piso de error irreducible que ninguna fórmula puede bajar. Ese piso consume el presupuesto del criterio: aunque la señal vertical mejore enormemente, el total no puede llegar a la mitad. **El criterio estaba mal planteado para sistemas donde una señal es ruido puro: debe ser POR SEÑAL.**

## Propuesta al director (requiere su OK — la gobernanza de la Regla 8 lo exige, pues re-plantea el criterio)
Prerregistro-09: mismos datos, mismos jueces, mismas semillas nuevas (11–15), criterio POR SEÑAL: éxito nivel A = la señal vertical (v2) reduce su error a la mitad de SU base trivial en los videos jueces; la horizontal se reporta sin exigencia (es ruido). Nivel B idéntico al de prereg-08. Esto no afloja la vara — la enfoca donde hay dinámica que predecir.

## Veredicto
FRACASO formal de prereg-08 en sus dos intentos, registrado. Observación estructural extraordinaria pendiente de un test bien planteado.
