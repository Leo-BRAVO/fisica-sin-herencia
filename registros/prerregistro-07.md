# Prerregistro 07 — Campaña de la familia: 14 longitudes de péndulo — 10 de julio de 2026
**Aprobado por el director ("adelante" a la recomendación del orquestador).**

- **Pregunta del árbol (nueva, nacida del INFORME-05):** las constantes que el motor descubre en cada péndulo de la familia Zenodo — el factor de pérdida y cualquier otra — ¿ESCALAN con la longitud del péndulo según alguna ley? Una ley que una a la familia sería el primer nodo inter-sistema del proyecto.
- **Datos:** los 16 archivos del dataset Zenodo 15569631 (14 longitudes, 23.5–69 cm; dos con réplicas). La longitud de cada péndulo es un dato medido por los autores (procedencia del dataset) — entra como etiqueta de cada sistema, no como teoría.
- **Qué se corre (etapa 1):** `descubrir.py` sobre cada longitud, 3 semillas cada una (las corridas previas en este régimen convergen de forma idéntica entre semillas; 3 bastan para verificar esa convergencia). Vara de tres rivales de siempre, calculada por archivo.
- **Naturaleza declarada:** campaña EXPLORATORIA — el objetivo no es superar la vara (el régimen es lineal y ya sabemos que el rival lineal empata), sino MEDIR las constantes descubiertas por longitud. El "éxito de vara" se registra pero no es el criterio.
- **Etapa 2 (tras la etapa 1):** tabla (longitud → constantes descubiertas) y regresión simbólica SOBRE ESA TABLA: buscar la ley de la familia. Éxito prerregistrado de etapa 2: una expresión con complejidad ≤ 15 que prediga la constante de longitudes NO usadas en su ajuste (dejar 3 longitudes fuera, elegidas por semilla fija = las posiciones 3, 8 y 12 de la lista ordenada) con error relativo < 10%.
- **Fracaso:** sin convergencia entre semillas, o etapa 2 sin expresión que cumpla — se registra tal cual.
- **Firmado:** Leo, director — 10-jul-2026.
