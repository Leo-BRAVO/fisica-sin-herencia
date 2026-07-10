# INFORME 06 — Campaña de la familia, etapa 2 (prerregistro-07) — 10 de julio de 2026

## Resultado en una frase
**El candado prerregistrado se cumplió formalmente (3 jueces < 10%), pero la auditoría lo destruyó: la media trivial predice a los jueces MEJOR que la ley descubierta — el candado estaba mal calibrado y la "ley senoidal" es ajuste al ruido. NO nace nodo de familia.**

## Los hechos
- Etapa 1 completa: 16 sistemas, 3 semillas cada uno, 48 evoluciones. Tabla de constantes (linealización local del mapa descubierto, definición neutra documentada en `etapa2_familia.py`).
- La tendencia global es real y ordenada: el factor de pérdida sube de 0.954 (23.5 cm) a 0.984 (69 cm) — 13 de 14 longitudes en orden monotónico.
- Etapa 2: la regresión simbólica sobre la tabla eligió `constante = sin(L×1.272)×0.0128 + 0.9731`, que pasó el candado (errores 2.28%, 0.23%, 1.51% en los jueces L=31.2, 44.2, 57.3).
- **Auditoría post-veredicto:** el rival trivial (media = 0.97085) obtiene 0.83%, 0.05%, 0.96% en los mismos jueces — MEJOR que la ley. El candado no discriminaba: la constante de la familia varía tan poco (~3%) que un umbral absoluto del 10% lo pasa cualquier cosa.

## Por qué la "ley senoidal" no se cree
- Un seno de período ~5 cm en L no tiene estructura creíble con 13 puntos de entrenamiento: es flexibilidad sobrando.
- La réplica del 63.3 cm delata la varianza de medición: v1 dio 0.936 y v2 dio 0.982 — ¡5% de diferencia entre réplicas del MISMO péndulo, mayor que el rango entero de la familia! Con esa varianza, ninguna ley fina es resoluble con estos datos.

## Lo que SÍ sobrevive
1. La tendencia monotónica global (más longitud → menos pérdida por paso) — 13/14 en orden; observación robusta, sin forma funcional certificada.
2. Candidata simple para el futuro (complejidad 5 del frente de Pareto): `constante = 0.986 − 0.637/L` — se registra como hipótesis, NO como nodo; necesita datos con réplicas múltiples por longitud.
3. Una lección de método de primer orden (para MENTE): **todo candado prerregistrado debe incluir vencer al rival trivial** — la misma lección de la enmienda-01, ahora a nivel de los candados. Un umbral absoluto sin rival no discrimina.

## Veredicto
FRACASO INFORMATIVO de la etapa 2 en su lectura honesta (la formal queda registrada como cumplida, con su refutación al lado). No nace N-004. Pregunta abierta actualizada: la ley de la familia requiere datos con menor varianza entre réplicas (múltiples corridas por longitud) o rango mayor de longitudes.

## Qué decisión le toca al director
1. Aceptar este veredicto doble (formal: cumplido / honesto: no discriminante).
2. Aprobar la lección de candados para MENTE v6.
3. Siguiente movimiento sugerido: cerrar la campaña Zenodo definitivamente y volver al currículo — cacería de datos de oscilación grande (pregunta inter-aparato) y/o caída libre (peldaño 2 original).
