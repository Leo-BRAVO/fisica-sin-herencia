# LA PLATAFORMA BRAVO Y LOS ALGORITMOS DE FRONTERA — 13 de julio de 2026
**Orden del director: "necesitamos nuestra propia plataforma... qué algoritmos podemos mejorar nosotros... qué no se ha explorado... piensa como nadie lo ha hecho".**

# PARTE 1 — LA PLATAFORMA (el cuerpo institucional del Centro)
El mismo concepto que gobierna a la mente gobierna a su casa: separación de poderes.
```
┌─ EL LABORATORIO (donde la mente trabaja — puede automejorarse) ─────────┐
│ motor simbólico · percepción · curiosidad · memoria · conectoma        │
│ planificador (cola de deseos) · bucles de automejora                    │
├─ EL TRIBUNAL (fuera del alcance de la mente — SOLO el director) ───────┤
│ jueces retenidos · criterios · reglas · banco de pruebas congelado     │
├─ EL ARCHIVO (append-only, triple respaldo) ────────────────────────────┤
│ git (génesis) · memoria jsonl · OneDrive · copia fría                  │
└─ LA VENTANA (el director ve y firma) ──────────────────────────────────┘
  panel · voz de la mente · red del árbol · boleta · informes Word
```
**Despliegue por fases (costo → capacidad):**
- **Fase A (HOY, $0):** laptop (latido horario) + GitHub Actions (segundo cuerpo para ráfagas). Ya operativa.
- **Fase B (semanas, $0):** VM siempre-encendida (Oracle Always Free, 4 núcleos ARM/24GB) = HOGAR DEL LATIDO — inmune a apagones de laptop; la laptop pasa a ser terminal del director. Julia/PySR corren en ARM.
- **Fase C (con inversión):** mini-servidor propio del Centro (GPU modesta para percepción, 64GB RAM) + la VM como respaldo; el laboratorio escala a decenas de campañas diarias.
- **Invariante de todas las fases:** el TRIBUNAL nunca vive en la misma máquina de escritura que el laboratorio (los jueces se replican a un remoto de solo-lectura — ni un bug puede tocarlos).

# PARTE 2 — LOS CINCO ALGORITMOS DE FRONTERA (no explorados; nuestros para intentar)

## F1 — Álgebra del desacuerdo: localizar EXACTAMENTE qué no sabe
Todos usan el desacuerdo de ensambles como número (varianza). NADIE lo usa como ESTRUCTURA: nuestras 5 semillas producen árboles simbólicos comparables — se pueden ALINEAR y hacer diff, como git hace con código. El subárbol donde las cinco discrepan ES la ignorancia localizada, señalada con nombre y apellido ("no sé el término que acompaña a Δz6 cuando v4 es grande"). La curiosidad deja de ser un escalar y se vuelve un MAPA. Implementable ya: parsear ecuaciones (sympy), alinear, diff. Nadie lo ha publicado.

## F2 — La ley como detective de datos (forense inverso)
Usamos leyes para predecir; nadie las usa sistemáticamente al revés: donde las 5 semillas REPLICADAS fallan JUNTAS en los mismos cuadros, la física no cambió — el INSTRUMENTO mintió (desenfoque, oclusión, salto del rastreador). La mente cura sus propios datos usando su propio conocimiento: marca cuadros sospechosos, los excluye con registro, re-descubre. Autopsia → cirugía. Con nuestra gobernanza (exclusiones prerregistradas y auditables) esto es único: los demás limpian datos a mano y a escondidas.

## F3 — Minería directa de cantidades CONSERVADAS
En vez de preguntar "¿qué predice el futuro?", preguntar "¿qué NO CAMBIA mientras todo cambia?": buscar con el motor simbólico funciones f(s, Δs) cuya varianza temporal sea mínima comparada con su varianza en datos barajados (esa razón ES la vara, con controles negativos integrados de nacimiento). Es el tipo de ley más profundo de la física (energía, momento — Noether). Existe literatura embrionaria (AI Poincaré) pero sin prerregistro, sin nulos, sin réplicas — nuestra versión gobernada sería la primera auditada. Y conecta directo con F5.

## F4 — Percepción compartida entre aparatos (los ojos que viajan)
Un solo autoencoder entrenado sobre TODOS nuestros aparatos a la vez (péndulos, caídas, colisiones) con un adaptador mínimo por aparato: los ojos aprenden "maneras de ver movimiento" que transfieren. Es nuestro Walrus en miniatura — pero desde cero y sin etiquetas, puro. Si las variables compartidas emergen, el conectoma gana su capa neuronal: conocimiento conectado a nivel de REPRESENTACIÓN, no solo de consulta (la red que el director pidió).

## F5 — Curiosidad por COMPRESIÓN (la Regla 6 hecha deseo)
"Aprender = comprimir mejor el archivo del mundo". Medir en bits la descripción total (leyes del árbol + residuos de todos los datos); la próxima campaña elegida es LA QUE MÁS BITS AHORRARÍA. Unifica curiosidad, parsimonia y progreso en un solo número con significado matemático (MDL) — y da la respuesta definitiva a "¿cuánto sabe?": bits ahorrados frente al archivo crudo. Los laboratorios hablan de MDL; nadie gobierna un programa de investigación entero con él.

## Orden de ataque recomendado
F3 (conservación — el salto científico, días) → F2 (forense — mejora todo lo demás, días) → F1 (álgebra del desacuerdo — semanas) → F4 (ojos compartidos — semanas, pide Fase B/C) → F5 (compresión — el norte de largo plazo, se construye encima de todos).
