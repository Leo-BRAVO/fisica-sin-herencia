# Prerregistro 09 — Caída libre, criterio POR SEÑAL — 10 de julio de 2026
**Aprobado por el director con OK explícito ("SÍ... Y ADELANTE"), conforme a la gobernanza de la Regla 8 (re-planteo de criterio requiere OK previo). La Regla 8 no se modifica — funcionó como diseñada.**

- **Datos y diseño:** idénticos al prereg-08 — 11 videos reales de caída (Morpheus, extracción propia), entrenamiento en 8, juicio sobre los videos completos 3, 7 y 11 de la lista ordenada. Semillas NUEVAS: 11–15, maxsize 15, 400 iteraciones.
- **Éxito nivel A (POR SEÑAL):** en al menos 3/5 semillas, el error de la SEÑAL VERTICAL (v2) sobre los videos jueces es menor que el 50% de la base trivial de esa señal (la mejor entre velocidad-constante y media, calculadas solo sobre v2). La señal horizontal (v1) se reporta sin exigencia — diagnóstico del INFORME-07: es ruido de rastreo sin dinámica.
- **Éxito nivel B (sin cambios respecto a prereg-08):** en las semillas exitosas, la ecuación de v2 contiene un término CONSTANTE ADITIVO replicado entre semillas (variación < 10%), y v1 no lo muestra. Interpretación comprometida: firma de una influencia constante actuando sobre el cuerpo en un solo eje.
- **Fracaso:** menos de 3/5 en nivel A por señal, o constante no replicada — se registra tal cual y la pregunta pasa a "necesita más datos" (hay 3 experimentos de caída más en Morpheus: apple, marker, tape).
- **Firmado:** Leo, director — 10-jul-2026.
