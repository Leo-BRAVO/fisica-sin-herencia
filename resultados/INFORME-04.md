# INFORME 04 — Test de re-escalado ×100 (prerregistro-04) — 9 de julio de 2026

## Resultado en una frase
**Resultado C (fracaso informativo) con evidencia parcial del A: a escala ×100 el motor no replicó el descubrimiento (0/3 semillas), pero la única semilla que encontró estructura mostró k dividida exactamente por 100 — señal de que k pertenece al lenguaje de medición, no a la dinámica.**

## Detalle
- 0/3 semillas superan el umbral; dos degeneraron a fórmulas triviales (v1+v3, v2+v4).
- Semilla 1, señal 2: `sin(v2 × 0.0001745) × (−254)` — k/100 con amplitud compensada ×254. Traza del Resultado A.
- Interpretación comprometida en prereg-04: A implica que k es del sistema de unidades del instrumento. La traza apunta a A, pero con 1 sola aparición no se declara — se registra como evidencia parcial.

## Lección de método (para MENTE, pendiente de ritual)
El motor es sensible a la escala: términos que requieren constante diminuta dentro de sin() + amplitud grande afuera exceden el presupuesto de búsqueda estándar. Mitigaciones futuras: normalizar señales a rango ~[−1,1] antes de descubrir (transformación documentada), o aumentar presupuesto cuando cambie la escala.

## Estado de la pregunta Q1 del árbol
Parcialmente respondida (evidencia hacia "k es de las unidades"). Se cierra del todo si la transferencia y/o una corrida normalizada la confirman.
