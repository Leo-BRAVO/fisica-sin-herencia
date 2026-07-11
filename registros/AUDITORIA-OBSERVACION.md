# AUDITORÍA — Qué hacen los laboratorios de IA-para-ciencia que nosotros no — 11 de julio de 2026
**Solicitada por el director ("verifica a detalle qué hacen los laboratorios y en qué estamos fallando — tal vez la manera en que está observando le falta algo"). Verificada contra literatura 2019–2026.**

## Veredicto en una frase
El motor de descubrimiento está al nivel del estado del arte (evolución simbólica + réplicas + jueces); **la tubería de OBSERVACIÓN está una generación atrás** — y los tres fracasos finos de esta semana (los "casi" del 1–18%) son exactamente los síntomas que la literatura predice para esa carencia.

## Las cinco carencias (de mayor a menor impacto)

### 1. Derivamos ruido en vez de integrarlo (la más grave)
Nuestro estado usa DIFERENCIAS entre cuadros (Δs) — y diferenciar datos ruidosos AMPLIFICA el ruido (nuestos pisos lo gritaban). Los laboratorios resolvieron esto con la **forma débil/integral** (Weak SINDy): en vez de preguntar "¿cuánto cambia en un paso?", preguntan "¿cuánto acumula en una ventana?" — la integración PROMEDIA el ruido en vez de amplificarlo, y identifica leyes con ruidos 10× mayores que los nuestros. Es matemática neutra (integración), sin física. **Mejora: objetivo de forma integral como opción del motor.**

### 2. No suavizamos nunca (por miedo justificado pero excesivo)
Alimentamos píxeles crudos con temblor. Los laboratorios aplican filtros GENÉRICOS documentados (Savitzky-Golay, splines) antes de descubrir. Nuestra Regla 2 ya lo permite ("suavizado solo con métodos genéricos, documentado") — nunca lo usamos. **Mejora: suavizado neutro opcional y documentado en la preparación.**

### 3. El estado que observa puede estar INCOMPLETO
Si la cámara no ve todo (velocidades angulares reales, la coordenada oculta), la ley no puede emerger. Los laboratorios usan **inmersión por retardos** (Takens): añadir como variables los valores PASADOS de las señales (s(t−1), s(t−2)…) — pura historia, cero física — para reconstruir el estado oculto. **Mejora: opción --retardos N en el preparador.**

### 4. Percepción y ley se aprenden JUNTAS, no en serie (el hallazgo mayor para el Peldaño 2b)
Nuestro plan de Percepción Pura era secuencial: autoencoder primero, ecuaciones después. El estado del arte (SINDy-autoencoder, Champion/Lusch/Brunton/Kutz 2019, y sus versiones bayesianas 2024+) los entrena SIMULTÁNEAMENTE: el autoencoder busca las coordenadas EN LAS QUE la ley resulta simple — la simplicidad de la ecuación guía qué variables aprender. Es la diferencia entre buscar lentes y después mirar, o ajustar los lentes MIENTRAS miras. **Mejora: rediseñar el Peldaño 2b como entrenamiento conjunto (pérdida = reconstrucción + dinámica simple en el latente).**

### 5. Nuestro rastreador es de centroides; los laboratorios usan flujo óptico subpixel
k-means de manchas en movimiento da posiciones gruesas; el flujo óptico (Lucas-Kanade) sigue rasgos con precisión subpixel. **Mejora: rastreador v2 con flujo óptico.**

## Lo que ya hacemos al nivel de los laboratorios (para no flagelarnos de más)
Réplicas y semillas múltiples (ensembles), jueces fuera de muestra por experimento completo, prerregistro (esto casi NADIE lo hace — es nuestra ventaja), pisos de ruido, canonización, rodado multi-paso, autopsias, rivales del propio árbol.

## Lo que consciente y correctamente NO copiamos
El análisis dimensional de AI-Feynman (usa unidades físicas humanas — contaminación) y los priors de teorías conocidas. Nuestra pureza es deliberada; estas cinco mejoras no la tocan: todas son matemática genérica u observación mejor.

## Orden de implementación propuesto
(1) Retardos + suavizado neutro (una tarde, y rehabilitan al péndulo doble Morpheus de inmediato); (2) forma integral; (3) flujo óptico; (4) Peldaño 2b conjunto (PyTorch ya instalado).
