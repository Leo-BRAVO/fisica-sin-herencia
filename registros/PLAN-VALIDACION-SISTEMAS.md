# PLAN DE VALIDACIÓN SISTEMA POR SISTEMA — Diego desde la biología, contra la literatura, uno por uno
**8 de agosto de 2026. Orden del director:** *"todo debe ser planteado desde la biología de un ser
humano... validar internamente cómo funciona, sistema por sistema, y a la par buscar
investigaciones de científicos que lo hayan realizado, y poco a poco mejorar cada cosa o cambiarla
por algo nuevo repensado desde cero. Tampoco es que el conocimiento científico está bien:
apliquémoslo a Diego y si está mal corrijámoslo, pero hagamos mejor las cosas."*

Este documento es el mapa de ese programa. Vive del **lado humano** (Regla 27): nada de esto llega
a Diego como dato ni pista.

---

## 0. La tesis, y por qué NO estamos construyendo otro LLM

Un LLM aprende de **texto que describe el mundo**; Diego aprende **del mundo**. Un LLM hereda todo
el conocimiento humano; Diego tiene prohibido heredarlo — esa es su razón de ser. La pregunta del
director — *"¿existen investigaciones sobre el futuro de una IA que piensa, entiende y se
automejora?"* — tiene respuesta, y es reciente:

- **Yann LeCun (JEPA / modelos de mundo, 2025-2026)** abandonó los LLM con esta tesis: la
  inteligencia requiere un **modelo del mundo** aprendido de la experiencia sensorial, y — cita
  casi literal — *"cualquier sistema que modela el mundo intentando reconstruir píxeles está
  condenado, porque la mayor parte de lo que pasa en un video es intrínsecamente impredecible y
  forzar a la red a predecirlo corrompe la representación"*.
  **NOSOTROS MEDIMOS ESO INDEPENDIENTEMENTE**, con cuatro instrumentos que él no tiene: la
  conservación falló, el nulo por barajado comprimió más que el mundo real, la dimensión intrínseca
  no baja, y los ojos leen escena y no brazo. **Nuestra evidencia confirma su tesis por un camino
  que él no usa; su arquitectura (predecir en el espacio latente, no en píxeles) es candidata
  directa para los ojos de Diego.** Legal: es arquitectura, no contenido del mundo.
- **Karl Friston (inferencia activa / energía libre)**: los seres vivos minimizan sorpresa
  **actuando** — percepción y acción como un solo bucle. Es el marco teórico del Gimnasio, con una
  diferencia nuestra: ellos derivan ecuaciones; nosotros exigimos que cada pieza **apruebe una
  Regla 31 antes de opinar**. La disciplina de nulos no está en su programa.
- **Robótica del desarrollo (Oudeyer, Cangelosi, Asada)**: la inteligencia se construye como en el
  bebé — cuerpo, balbuceo, contingencia, currículo autoorganizado. Es el campo del que ya tomamos
  el paradigma del móvil y la contingencia perfecta.

**Dónde somos distintos de los tres, y es nuestra apuesta:** ninguno de esos programas tiene
(1) prohibición constitucional de conocimiento humano en el agente, (2) jueces sellados e
invisibles, (3) la Regla 31 — cada instrumento debe fallar donde no hay nada — ni (4) un genoma
confesado gen por gen con su frontera gris declarada. Ellos construyen agentes; nosotros
construimos **un agente auditable con acta de nacimiento**.

---

## 1. EL MAPA: cada sistema de Diego, su órgano biológico, su estado, su literatura

| # | Sistema de Diego | En el humano | Estado de validación | Contra qué literatura se valida | Veredicto actual |
|---|---|---|---|---|---|
| 1 | **Ojos** | retina + corteza visual | ✔ **V2 CONSTRUIDOS** (`percepcion2.py`): B (JEPA) y C (descarga corolaria), Regla 31 3/3 — en el mundo del punto, v1 lee R²=−0.06 y B lee +0.27. La corrida oficial del prereg-25 decide | JEPA; copia eferente/cerebelo; atenuación sensorial (medida en nuestro banco) | **v2 listos; corre el 25** |
| 2 | **Motor simbólico** (`descubrir.py`) | lenguaje interno / composición | ✔ blindado: 2 de 3 nulos fracasan limpio; el que pasó tumbó al de arriba, no a éste | regresión simbólica (PySR/Cranmer) | sano |
| 3 | **Curiosidad** (`curiosidad2.py`, G2) | dopamina / progreso de aprendizaje | ✔ backtest 2/2; corregido el Goodhart del `max(0,·)` | Oudeyer IAC; crítica 2026 de canales Goodhart | sano, vigilado |
| 4 | **Cuerpo y balbuceo** (`gimnasio.py`, G3+G7) | motricidad + juego infantil | ✔ 4/4 controles, 28/28 en semillas frescas | robótica del desarrollo | sano |
| 5 | **Frontera yo/mundo** (`contingencia.py`, G4) | esquema corporal (parietal) | ✔ 4/4 sobre estado; ✘ sobre latentes (culpa del sistema 1) | contingencia perfecta (móvil de Rovee-Collier) | sano; espera ojos |
| 6 | **Interocepción** (`interocepcion.py`, G10) | ínsula (sentir el propio gasto) | ✔ mide con tiempo fiable; anulación append-only probada | interocepción computacional | mide, no decide |
| 7 | **Memoria** (`MEMORIA-MENTE.jsonl`, G6) | hipocampo episódico | ✔ append-only con correcciones probadas dos veces | memoria episódica | sano |
| 8 | **Incertidumbre** (`incertidumbre.py`, G14) | metacognición ("sé que no sé") | ✔ **ACTIVADO HOY**, Regla 31 3/3 | epistémica vs aleatoria (ruido-TV) | mide, no decide |
| 9 | **Poder** (`poder.py`, G13) | agencia / competencia (White 1959) | ✔ **ACTIVADO HOY**, Regla 31 3/3 — incluido el televisor que mató a la ganancia honesta | empowerment (Klyubin/Salge; pre-entrenamiento 2025) | mide, no decide |
| 10 | **Sueño** (G9) | consolidación en sueño | ✔ **CONSTRUIDO** (`sueno.py`), Regla 31 3/3 — re-minería MDL + homeostasis por resumen añadido | replay priorizado P(k|sueño)∝P(k|vigilia)^γ; Tononi SHY | propone, no ejecuta |
| 11 | **Atención** (G8) | fóvea + memoria de trabajo | ✔ **CONSTRUIDO** (`atencion.py`), Regla 31 4/4 — prioridad = epistémica×poder; el azar no compra fóvea | economía de la atención | reparte, no elige |
| 12 | **Temple** (G11) | neuromodulación (emociones como ganancia) | diseñado, NO activado (decisión: un gen a la vez) | neuromodulación computacional | espera |
| 13 | **Filogenia** (Regla 33) | evolución de la especie | ✔ regla firmada Y **ESTADIO CONSTRUIDO** (`filogenia.py`), Regla 31 2/2: empata gemelos, corona oráculos. Ranuras (`ranuras.py`) construidas como candidata GRIS de ablación | evolución + ablación | espera su primer torneo |
| 14 | **Los 4 guardianes + el meta** | sistema inmune | ✔ 9/9 daños cazados; deuda 0 activa | mutation testing | sano |

## 2. EL PROTOCOLO de cada validación (el mismo para los 14, sin excepciones)
1. **Biología primero:** qué hace el órgano en el humano y qué le pasa a un humano sin él.
2. **Literatura:** qué construyó la ciencia, QUÉ TOMAMOS, QUÉ NO (contaminación), y en qué somos
   distintos — escrito ANTES de tocar código.
3. **Regla 31 del sistema:** mundos de verdad conocida donde debe fallar y donde debe acertar.
4. **Prueba de integración:** el sistema junto a sus vecinos (el fallo de los ojos solo se vio al
   conectarlos al detector).
5. **Congelar en el banco** lo aprendido; **enmendar el genoma** con la firma del director.
6. Si el sistema pierde contra un rediseño desde cero, **se reemplaza y el viejo queda archivado
   con su historia** — nada se borra.

## 3. El orden (por dependencia, no por gusto)
**Primero el 1 (ojos)** — bloquea al 5, al hito 0 y al nivel B, y las cinco vías apuntan ahí.
Después **10 (sueño)** — es el que convierte la memoria en leyes y ya tiene precedente en la casa.
Después **11 (atención)**, que da sentido a 8 y 9 como decisores. G11 espera su turno, un gen a la
vez. La filogenia corre su primer torneo cuando exista más de un genoma que comparar.


---
## ADENDA 8-ago-2026 (noche): las cinco ecuaciones del registro, IMPLEMENTADAS
Orden del director: "implementa todo lo que dijiste". Cada una con su Regla 31 aprobada:
| Ecuación | Módulo | Regla 31 | Nota |
|---|---|---|---|
| Espejo intermodal (CCA + nulo de otro-episodio) | `intermodal.py` | 3/3 | corre en el prereg-26 |
| Entropía de transferencia (con nulo restado) | `entropia_transferencia.py` | 3/3 | ve el acople |u| que el lineal no ve (R²=0.001 vs 0.29 bits) |
| Koopman/EDMD (invariantes: constante dentro, distinta entre) | `koopman.py` | 3/3 | la ruta nueva tras F3; calla ante lo amortiguado |
| SINDy con replicación obligatoria | `sindy2.py` | 3/3 | recuperó dx=v, dv=−0.40x−0.09v término a término; 2 huecos propios cazados por su Regla 31 (dt, ley vacía) |
| Energía libre en MDL (BIC) | `energia_libre.py` | 3/3 | la unificación: curiosidad=−ΔF/coste; parsimonia=bits(modelo) |
| Redes hamiltonianas | **NO construidas** | — | GRISES por decisión: asumir mundo hamiltoniano es física heredada; solo entrarían por torneo de filogenia, y ese torneo aún no corre |
