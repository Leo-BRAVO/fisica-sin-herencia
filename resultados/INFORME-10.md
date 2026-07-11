# INFORME 10 — Péndulo doble Morpheus (prerregistro-11) — 11 de julio de 2026

## Resultado en una frase
**FRACASO (0/5 en nivel A por señal; sin acople canónico): en coordenadas de imagen a 30 fps, la mente encontró una ley de suavizado por coordenada — replicada en las 20 ecuaciones — pero NO el acople entre cuerpos; la autopsia dice por qué y señala el camino.**

## Los hechos
- Nivel A: 0/5 — todas las semillas tropezaron con la señal s4 (110 vs umbral 93; margen 18%) y varias con s1. Las señales s2 y s3 pasaron en todas.
- Estructura descubierta (20/20 ecuaciones, 5 semillas): `siguiente = valor + A·sin(cambio × k)` por coordenada — un integrador de velocidad con saturación senoidal. Constantes A y k replicadas entre semillas (p.ej. 8.54 y 0.1213 hasta la 4ª cifra), otra vez por rutas algebraicas distintas (multiplicación y división).
- Nivel B: ninguna ecuación depende de las señales del otro cuerpo. El acople físico del péndulo doble NO emergió en esta representación.
- Rodado: horizonte de 5 pasos (contra 101 del sistema Michigan en ángulos) — las fórmulas por coordenada no ruedan: leyes débiles.

## Lo que dijo la autopsia (mejora #1 en su primer uso obligatorio)
- Las fórmulas están a 2.6–4× del piso de ruido: HAY estructura sin explotar en los datos — no es límite físico, es límite del modelo.
- El error correlaciona con la magnitud del cambio (+0.3 a +0.5) y se concentra AL INICIO de los videos (cuando el movimiento es violento): la falla vive exactamente donde el acople entre cuerpos importa más.
- Traducción: la mente capturó el suavizado dominante y se quedó ciega al acople — y la ceguera es de la REPRESENTACIÓN: centroides de píxeles de dos manchas a 30 fps diluyen la geometría que conecta los cuerpos (Michigan, con ángulos a 500 Hz, la mostraba de inmediato).

## Qué señala el camino (dos rutas, ambas en el currículo)
1. **Datos mejores en la misma representación:** video de péndulo doble a alta velocidad (Michigan tenía 500 Hz; Morpheus da 30 fps). Sin candidato inmediato con licencia limpia — queda en cacería.
2. **La ruta profunda — Peldaño 2b (Percepción Pura):** este fracaso es la motivación EXACTA de esa fase: en vez de que el orquestador elija las variables (centroides k-means), un autoencoder entrenado desde cero descubriría las variables correctas del sistema — como hizo Columbia. El proyecto acaba de toparse, con datos propios, con la razón de ser de su siguiente frontera.

## Estado de la pregunta inter-aparato
Sigue ABIERTA — dos intentos (Zenodo: amplitud insuficiente; Morpheus: representación insuficiente), dos fronteras mapeadas. La pregunta no está fallando: está enseñándonos qué necesita.
