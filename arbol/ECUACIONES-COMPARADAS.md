# LAS ECUACIONES DEL IMPULSO — las de ellos, la nuestra, y la que vamos a construir
**Orden del director (8-ago-2026): "compara las ecuaciones de esas universidades con la nuestra; no vamos a usar las suyas, vamos a mejorarlas evitando dañar y prediciendo si esto va a ser lo correcto cuando se corra cada experimento". Verificado contra la literatura de motivación intrínseca (Oudeyer/INRIA, Schmidhuber/IDSIA) y su crítica formal de 2026. Fuentes al pie.**
**Nota de cortafuegos (Regla 27):** este documento compara MÉTODOS, no física. Comparar cómo decide un agente qué estudiar es territorio del orquestador; comparar QUÉ descubrió es del comparador, del lado humano. El núcleo de Diego no lee esto.

---

## 1. LAS TRES ECUACIONES QUE EXISTEN

### (A) Oudeyer — *Intelligent Adaptive Curiosity* (IAC, IEEE TEC 2007)
```
interés(región) = | error_medio(ventana vieja) − error_medio(ventana reciente) |
```
Divide el mundo en regiones, guarda el historial de errores de predicción de cada una y elige
donde el error **está bajando más rápido**. Validado en robots reales: auto-organiza un currículo
(agitar → tocar → empujar) sin que nadie lo programe.
- **Su fortaleza:** evita a la vez lo trivial (ya predicho) y lo imposible (nunca predicho).
- **Su hueco:** el error de predicción es una vara **cruda** — no distingue "aprendí una ley" de
  "memoricé ruido". Y las regiones se definen a mano.

### (B) Schmidhuber — *Compression Progress* (teoría formal de la creatividad, 1990–2010)
```
recompensa(t) = C(historia, t−1) − C(historia, t)      [primera derivada de la compresibilidad]
```
El agente maximiza la **derivada de cuánto puede comprimir su historia**. Es más profundo que
Oudeyer: el ruido no se comprime → aburrimiento automático ante el "televisor con estática".
- **Su fortaleza:** distingue regularidad aprendible de ruido incompresible, por construcción.
- **Su hueco:** la formulación es informal — no dice **sobre qué datos** medir la compresión.

### (C) La crítica de 2026 (*Signed Compression Progress on a Sealed Audit is Goodhart-Resistant*)
Demuestra que el enunciado de Schmidhuber es demasiado amplio y nombra **cuatro canales de
Goodhart** por los que un agente puede farmear recompensa sin aprender nada:
1. mejorar sobre su propio flujo elegido mientras **empeora en la distribución objetivo**;
2. **olvidar y reaprender** los mismos hechos, si la recompensa recorta el progreso negativo;
3. sobreajustar un conjunto de validación finito;
4. explotar una clase de modelos de alta capacidad.
Y nombra la cura: **progreso CON SIGNO medido sobre una AUDITORÍA SELLADA.**

---

## 2. LA NUESTRA HOY — y el defecto exacto que tiene

```
Curiosidad(e) = ΔC(e) / coste(e)
LP(región)    = max(0, récord_hoy − récord_hace_H_eventos)          ← implementado en curiosidad2.py
coste(e)      = 1  (uniforme)                                        ← confesado como falso en el código
```

**Dónde estamos por delante de ellos** (y no es autobombo, es la arquitectura que ya existe):
- Medimos en **bits** (MDL, Regla 6), no en error crudo → heredamos la ventaja de Schmidhuber.
- Nuestras "regiones" no son cajas artificiales: son **sistemas físicos reales con prerregistro**.
- Y sobre todo: **ya tenemos jueces congelados** — la infraestructura exacta que la crítica de
  2026 pide y que ni Oudeyer ni Schmidhuber tenían. Nadie más puede medir progreso sobre una
  auditoría sellada porque nadie más sella nada.

**Dónde estamos MAL — los dos defectos, dichos sin adorno:**
1. **El `max(0, ...)` es el canal de Goodhart nº2, literal.** Al recortar el progreso negativo,
   una región que *pierde* conocimiento y lo recupera farmea interés para siempre. Lo escribí sin
   saber que la literatura ya lo tenía documentado como modo de fallo.
2. **El récord se mide sobre el resultado de la campaña, no sobre una auditoría sellada.** Es el
   canal nº1 y nº3: el progreso podría venir de ajustarse mejor a sus propios datos elegidos.
   Y `coste = 1` hace que el denominador no exista: hoy la ecuación no tiene freno.

---

## 3. LA QUE VAMOS A CONSTRUIR (no la de ellos: la nuestra, corregida por su crítica)

```
Curiosidad(e) = LP_sellado(región) / coste_sentido(e)

LP_sellado(r) = bits_jueces(r, hoy) − bits_jueces(r, hace H eventos)      ← CON SIGNO, sin recortar
bits_jueces   = bits ahorrados medidos SOLO sobre los JUECES CONGELADOS de esa región
                (la auditoría sellada que la crítica pide — y que ya teníamos)
coste_sentido = gasto real medido por INTEROCEPCIÓN (G10): tiempo + cómputo + esfuerzo
```

Las tres mejoras, y qué daño previene cada una:

| Mejora | Canal de Goodhart que cierra | Qué habría pasado sin ella |
|---|---|---|
| **Progreso CON SIGNO** (sin `max(0,·)`) | olvidar-y-reaprender (nº2) | una región podría oscilar y farmear interés eternamente |
| **Medido sobre JUECES CONGELADOS** | auto-flujo (nº1) y sobreajuste de validación (nº3) | "progresar" ajustándose mejor a sus propios datos, sin aprender nada real |
| **Coste SENTIDO (G10)** | explotar capacidad (nº4) | perseguir ganancias diminutas a costo infinito |

**Respuesta directa a la pregunta del director — "¿qué pasará cuando le demos más videos?"**
Con la ecuación de hoy: **peligro real.** Más datos = más regiones = más superficie para farmear
progreso ilusorio (canal nº1: mejora en lo que él elige, empeora en el resto). Con la ecuación
corregida: más videos **fortalecen** el sistema, porque el progreso solo cuenta si aparece en
jueces que el agente nunca tocó. Es la diferencia entre una vara que crece con los datos y una
que se corrompe con ellos.

---

## 4. LA PREDICCIÓN COMPROMETIDA (lo que el director pidió: predecir si esto será correcto)
Antes de correr nada, se comprometen estas expectativas falsables:
1. En una memoria sintética donde **nada progresa**, la ecuación corregida debe declarar
   aburrimiento universal (ya congelado en el banco desde 18b).
2. En una memoria donde una región **oscila** (pierde y recupera), la versión con signo debe dar
   progreso ≈ 0 y la versión vieja `max(0,·)` debe dar progreso positivo — **la demostración
   directa del canal nº2 en nuestros propios datos.**
3. El coste sentido debe correlacionar con el tiempo real de cómputo (verificable contra el reloj).
Si (2) no se reproduce, el defecto no era real y se registra tal cual.

---

## 5. LO QUE NO COPIAMOS (y por qué)
Ni las regiones artificiales de IAC (las nuestras son sistemas con prerregistro), ni el
reforzamiento profundo de Plan2Explore (curiosidad neuronal ilegible: no se puede auditar qué le
dio curiosidad). Nuestra curiosidad debe poder **leerse** — es la condición para que un director
no programador la gobierne.

## Fuentes (validadas 8-ago-2026)
- Oudeyer, Kaplan & Hafner, *Intrinsic Motivation Systems for Autonomous Mental Development* (IEEE TEC 2007) — IAC y la ventana de errores por región.
- Baranes & Oudeyer, *R-IAC* — regiones robustas. Flowers/INRIA, *Curiosity, intrinsic motivation and information seeking in cognitive development*.
- Schmidhuber, *Driven by Compression Progress* y *Formal Theory of Creativity, Fun and Intrinsic Motivation (1990–2010)* — la derivada de la compresibilidad.
- *Signed Compression Progress on a Sealed Audit is Goodhart-Resistant* (arXiv 2606.11417, 2026) — los cuatro canales de Goodhart y la cura por auditoría sellada.
