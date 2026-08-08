# EL GIMNASIO — el mundo donde Diego tendrá manos
**Documento de teoría e investigación. 8 de agosto de 2026. Rama de trabajo, NO main hasta que el
director lo apruebe.** Prerregistro asociado: **19 (FIRMADO)**. Este documento es la investigación
extensa que el director pidió ANTES de construir nada.

---

## 0. Por qué el Gimnasio existe (y por qué no es un capricho)

El 8-ago-2026 medí tres formas distintas de separar *"aquí hay una ley"* de *"aquí solo hay textura
con deriva"* **mirando datos ya grabados**. Las tres fallaron (INFORME-30). No fue mala suerte de
implementación: **la información no estaba en los datos.**

Ese día yo creía haber tropezado con un defecto nuestro. Buscando la literatura resulta que
tropecé con un **teorema conocido**:

> Con datos puramente observacionales, la estructura causal solo es identificable **hasta su clase
> de equivalencia de Markov**. Para desambiguarla hacen falta **intervenciones**. En aprendizaje de
> representaciones causales se demuestra además que hace falta **al menos una intervención por
> variable latente** para identificarlas.

Es decir: **ningún estimador, por bueno que sea, puede sacar de un video lo que el video no
contiene.** Diego lleva toda su vida en el escalón 1 de la escalera de Pearl (VER). El Gimnasio es
el escalón 2 (HACER). No es una mejora incremental: es la única puerta de salida del callejón, y
ahora tenemos **evidencia propia y teorema ajeno** apuntando a la misma puerta.

**Lo que esto le da al proyecto que no tiene:** hasta hoy, cada nodo del árbol es una afirmación
sobre correlaciones en grabaciones de terceros. El primer nodo nacido en el Gimnasio será la
primera afirmación **causal** del proyecto — y estará sostenida por intervenciones que Diego
eligió, no por datos que alguien más grabó.

---

## 1. LA INVESTIGACIÓN — qué hay ahí fuera y qué nos falta

Revisión hecha el 8-ago-2026. Para cada línea: **qué dicen**, **qué tomamos**, **qué NO tomamos**,
y **en qué somos distintos**. (Regla 27: esto es trabajo del COMPARADOR y del orquestador — nada de
esto entra jamás como dato, pista ni contexto al lado de Diego.)

### 1.1 Aprendizaje de representaciones CAUSALES desde intervenciones — *lo más importante que no estábamos usando*
Un campo entero (von Kügelgen, Squires, Buchholz y otros) demuestra **garantías de identificabilidad**
cuando hay intervenciones, incluso con mezcla no lineal y objetivos de intervención desconocidos —
y **imposibilidad** en varios casos puramente observacionales.

- **Qué tomamos:** el criterio de éxito. No basta con que Diego "prediga mejor". El estándar del
  campo es **identificar las variables latentes**, y eso es exactamente lo que el prereg-19 pide:
  separar cuerpo de mundo con ≥90% en jueces congelados.
- **Qué NO tomamos:** sus supuestos (mezcla lineal, ruido gaussiano, grafo conocido) — son la
  biblioteca, y además Diego no puede recibirlos.
- **En qué somos distintos, y es real:** **ellos asumen que las intervenciones les son dadas.**
  Un experimentador decide qué nodo intervenir. **Diego tiene que descubrir que él mismo es el
  interventor**, con qué comandos y sobre qué variables. Nadie en ese campo hace que el agente
  *derive* su propio conjunto de intervenciones desde balbuceo, bajo gobernanza con jueces
  sellados. Ahí hay algo que aportar.

### 1.2 Contingencia sensomotora y la frontera yo/mundo — *el paradigma que ya adoptamos, ahora con su literatura*
El vínculo acción→consecuencia es un motor central del desarrollo infantil; en robótica, la
distinción cuerpo/entorno se ha logrado por correlación entre movimientos voluntarios y cambios
sensoriales, invarianza multimodal (visión + propiocepción), modelos internos predictivos y
contingencias temporales.

- **Qué tomamos:** la validación de que el paradigma funciona; y una idea concreta que **nos falta**:
  la **invarianza multimodal** (una variable que responde igual a mi comando en dos sentidos
  distintos es más "mía" que una que solo responde en uno).
- **Qué NO tomamos:** las arquitecturas específicas ni los "modelos internos" preprogramados.
- **En qué somos distintos:** en esa literatura la frontera yo/mundo se evalúa con métricas que el
  experimentador define **después** de ver los resultados. Nosotros la **prerregistramos con
  jueces congelados y nulos** (prereg-19). Es la misma pregunta, con una gobernanza que ellos no
  aplican.

### 1.3 Empowerment (poder de control) — *un motor que NO tenemos y que encaja perfecto*
El *empowerment* mide, en bits, **cuánto control tiene el agente sobre sus estados futuros**
(información mutua entre sus acciones y sus observaciones futuras). Maximizarlo empuja a explorar
sin ninguna recompensa de tarea, y trabajo reciente lo usa como señal de pre-entrenamiento y lo
extiende a *empowerment descontado* para balancear control a corto y largo plazo.

- **Por qué encaja como un guante:** nuestra ecuación de curiosidad (G2) mide **bits ahorrados**;
  el empowerment mide **bits controlados**. Son la misma moneda — el proyecto ya decidió por la
  Regla 6 que la unidad son los bits. Y donde la curiosidad se apaga (una región ya comprendida),
  el empowerment sigue empujando hacia donde el cuerpo puede *hacer* más.
- **Y hay algo más profundo:** el empowerment **es** una medida de contingencia. Información mutua
  entre acción y futuro = exactamente lo que G4 quiere detectar. **Un solo estadístico puede servir
  de motor (qué hacer) y de detector (qué es mío).** Eso sería una economía conceptual que la
  literatura tiene partida en dos campos que casi no se citan.
- **Riesgo, dicho ahora:** el empowerment tiene su propio Goodhart (un agente puede maximizar
  control sobre variables triviales). Entra como **G13 propuesto, NO activado**, y solo después de
  pasar su Regla 31.

### 1.4 El problema del televisor ruidoso — *nuestra ecuación ya lo esquiva, pero hay un aviso nuevo*
La literatura 2025–2026 insiste: el error de predicción como proxy de progreso **sigue siendo
ambiguo**, y hay agentes que caen en transiciones estocásticas incluso usando modelos inversos
pensados para evitarlo. Las curas propuestas van hacia **monitorizar la mejora del modelo** en vez
del error crudo.

- **Dónde estamos:** bien — nuestra ecuación mide **progreso de compresión con signo sobre auditoría
  sellada**, que es la forma fuerte de esa cura (ECUACIONES-COMPARADAS §4).
- **El aviso que sí nos toca:** en el Gimnasio, el agente **genera su propia estocasticidad** al
  moverse. Un motor con juego mecánico o un contacto caótico es un televisor ruidoso **construido
  por su propio cuerpo**. La Regla 31 del prereg-19 (motores desconectados) no lo cubre. **Hay que
  añadir un control: un grado de libertad que responde a los comandos con RUIDO PURO** — debe
  clasificarse como "mundo", no como "yo", y no debe atraer curiosidad.

### 1.5 Objetos y ranuras (*slot attention*) — *lo que Diego no tiene y sabemos que le falta*
El paradigma de ranuras descompone una escena en un conjunto de latentes, cada uno un objeto
persistente, sin anotaciones. Hay trabajo 2026 sobre desacoplar **apariencia** de **identidad** en
video y sobre ranuras adaptativas en número.

- **El diagnóstico que encaja:** la dimensión intrínseca de los latentes de Diego es **~6.2 de 8**
  (INFORME-26) — su espacio de estados casi no se comprime. Una representación **sin noción de
  objeto** tiene que gastar dimensiones codificando textura y posición mezcladas. Es coherente con
  todo lo demás que medimos.
- **Cuidado con la contaminación:** "hay objetos separados y persistentes" es un **hecho sobre el
  mundo** (biblioteca), y el GENOMA declara explícitamente que la permanencia de objeto **no se le
  da**: debe emerger como hito. **Una arquitectura de ranuras es una frontera GRIS** — no dice
  cuántos objetos hay ni cuáles, pero sí impone *que el mundo se descompone en cosas*.
  **Recomendación honesta: no entra al genoma. Entra como candidata de la filogenia (Regla 33) y
  se mide por ablación** — si Diego con ranuras aprende mucho mejor que Diego sin ranuras, ese
  número es un resultado científico sobre cuánto vale ese prior, y es publicable.

### 1.6 Descubrimiento de leyes de conservación y simetrías — *donde ya fallamos una vez*
Hay una familia entera de métodos: redes que meta-aprenden cantidades conservadas, ConservNet
(invariantes desde datos agrupados con pérdida de varianza-ruido), redes convolucionales de álgebra
de Lie para descubrir simetrías, AI Poincaré, y regresión simbólica para simetrías de EDOs.

- **Por qué importa ahora:** nuestra prueba de conservación (F3) **falló** el 13-jul y su nulo
  aceptaba mundos vacíos (origen de la Regla 31). Estos métodos no nos dan la respuesta —
  **nos dan la vara**: cómo se plantea una pérdida que busque invariantes sin decir cuál.
- **Qué tomamos:** la idea de que buscar un invariante **cualquiera** es legal (es matemática, no
  física), y la pérdida de varianza como forma de pedirlo. En el Gimnasio esto es potente:
  **la gravedad será el invariante que ningún comando modula.**

### 1.7 Análisis dimensional automático (Buckingham Pi) — *el filtro gratis que estamos tirando a la basura*
Hay métodos que **descubren los grupos adimensionales** desde datos (optimización con restricciones,
BuckiNet, SINDy adimensional) y que mejoran la regresión simbólica al forzar consistencia dimensional.

- **El problema nuestro, concreto:** `estandarizar` convierte todo a z-scores. **Eso destruye la
  información de escala**, y con ella la posibilidad de descubrir consistencia dimensional. Nos
  estamos amputando el filtro más potente que existe **y que no cuesta ni una pizca de conocimiento
  humano** — la consistencia dimensional es consecuencia de que el mundo no tiene unidades
  preferidas, no de que alguien nos contara qué es un metro.
- **Cómo se hace legal para Diego:** él no puede recibir "esto son metros". Pero **sí puede recibir
  el mismo mundo a dos escalas** (el Gimnasio puede reescalar longitud y tiempo a voluntad — un
  video de internet no). Una ley que sobreviva el reescalado capturó una relación; una que no,
  estaba ajustando unidades arbitrarias. **Es un verdugo nuevo, gratis, y el Gimnasio es el único
  sitio donde se puede aplicar.** Precedente propio: la carpeta `resultados/reescalado-x100`.

---

## 2. LO QUE SALE DE LA INVESTIGACIÓN: cinco cosas que Diego no tiene

Ordenadas por **(valor × cuán legal es) ÷ coste**. Ninguna se implementa antes de su Regla 31 y de
la firma del director.

| # | Qué | Por qué | Legalidad | Coste |
|---|---|---|---|---|
| **1** | **Acción** (G3) + **contingencia** (G4) | el teorema: sin intervenir no hay identificabilidad | limpia — es un cuerpo, no un hecho | prereg-19, ya firmado |
| **2** | **Verdugo por reescalado** | el único filtro dimensional legal, y solo existe en el Gimnasio | **totalmente limpia** — es matemática de invariancia | bajo |
| **3** | **Empowerment (G13)** | motor de acción Y detector de contingencia con un solo estadístico, en bits | limpia — mide su control, no el mundo | medio |
| **4** | **Incertidumbre propia** | sin ella la curiosidad no distingue "es azar" de "aún no aprendo"; crítico con un cuerpo ruidoso | limpia — mide su propio estado | medio |
| **5** | **Ranuras / objetos** | explicaría la dimensión 6.2 de 8 | **GRIS — no entra al genoma**; candidata de filogenia, medida por ablación | alto |

---

## 3. DISEÑO DEL GIMNASIO (v0, para discutir — nada construido)

### 3.1 El mundo
PyBullet (gratis, determinista con semilla, reescalable). Escena mínima: suelo, 2–3 objetos libres,
un cuerpo articulado de 3–5 grados de libertad con efector. **Sin recompensas de tarea.**

**La confesión obligatoria, y va en cada nodo que salga de aquí:** la física del simulador **es
código humano**. Diego no descubrirá el universo en el Gimnasio: descubrirá **nuestro simulador**.
Por eso la regla del Gimnasio es absoluta — **todo lo aprendido aquí se marca `sobre-el-simulador`
y JAMÁS entra al árbol como física del mundo.** El Gimnasio no sirve para descubrir física: sirve
para que **emerjan capacidades** (la frontera yo/mundo, la noción de intervención, la de invariante)
que después se aplican a datos del universo real.

### 3.2 Lo que se mide y con qué se compara
- **Contingencia por variable latente:** cuánto de su dinámica explican los comandos motores
  recientes, contra no explicarla. Es una **resta de dos poderes predictivos** — la misma forma
  que la ganancia honesta, **y por eso hereda sus dos canales de mentira**. Ya está blindado en el
  prereg-19; se repite aquí para que nadie lo pierda de vista.
- **Jueces:** episodios grabados con semillas apartadas **antes** del entrenamiento, donde la
  pertenencia cuerpo/mundo se conoce por construcción del simulador y Diego **jamás la ve**.

### 3.3 Los controles (Regla 31) — con el que la investigación nos obligó a añadir
1. **Mundo sin agencia:** motores desconectados. No debe encontrar ningún "yo".
2. **Control positivo:** un solo grado de libertad conectado. Debe encontrar exactamente ese.
3. **NUEVO — el televisor ruidoso corporal (§1.4):** un grado de libertad que responde a los
   comandos con **ruido puro**. Debe clasificarse **mundo**, no **yo**, y no debe atraer curiosidad.
   Sin este control, el cuerpo de Diego puede convertirse en su propio distractor y no lo veríamos.
4. **NUEVO — el mundo reescalado (§1.7):** el mismo episodio con longitud ×k y tiempo ×m. Lo que
   Diego aprenda debe transferir; lo que no transfiera, estaba ajustando unidades arbitrarias.

### 3.4 Los hitos (cartilla, con criterio numérico ANTES)
- **Hito 0 — el nacimiento:** emerge la frontera yo/mundo. *(prereg-19, firmado.)*
- **Hito 0b — el primer no-yo:** la dirección de caída aparece como la componente que **ningún**
  comando modula. *(prereg-19, nivel B.)*
- **Hito 1 — permanencia:** ¿predice un objeto que dejó de ver? *(sin prerregistro aún.)*
- **Hito 2 — contacto:** ¿emerge que el cambio de trayectoria ajeno requiere proximidad?
  *(sin prerregistro aún.)*

**Ninguno de los hitos 1–2 se prerregistra todavía.** Un hito escrito antes de saber si el hito 0
funciona es una promesa, no un experimento.

---

## 4. CÓMO SE CONECTA CON TODO LO YA CONSTRUIDO (el director pidió correlación, no un anexo)

| Pieza existente | Cómo la usa el Gimnasio |
|---|---|
| **Reglas 1–4** (nada de física humana) | el simulador no le dice nunca qué es un objeto ni qué es gravedad; solo píxeles y su propio estado |
| **Regla 5** (predicción prospectiva) | episodios-juez congelados desde antes del entrenamiento |
| **Regla 11** (verdugos) | barajar **los comandos**, no las series — el nulo según la afirmación |
| **Regla 27** (cortafuegos) | toda esta investigación es del lado humano; ni una línea llega a Diego |
| **Regla 31** (fallar en el vacío) | los 4 controles de §3.3, congelados en el banco antes del primer veredicto |
| **Regla 32** (autoauditoría) | `coherencia.py` gana casos que vigilen lo nuevo; nada entra sin guardianes verdes |
| **`percepcion.py` (ojos)** | se reentrenan **desde cero** solo con cuadros del Gimnasio — nada preentrenado |
| **`ganancia_honesta.py`** | **degradado a sonda (INFORME-30)**: no certifica nada aquí tampoco |
| **`interocepcion.py` (G10)** | el coste de cada episodio pasa a ser sensación suya, no número nuestro |
| **`curiosidad2.py` (G2)** | elige qué explorar; el empowerment (si se aprueba) sería su hermano de acción |
| **CONECTOMA** | los nodos del Gimnasio entran marcados `sobre-el-simulador` — conectados pero segregados |
| **Latido de la nube** | los episodios son items de cola como cualquier otro, cronometrados y auditados |

---

## 5. LO QUE ESTE DOCUMENTO **NO** AUTORIZA

No autoriza construir nada. No activa G11, G12 ni el propuesto G13. No prerregistra los hitos 1–2.
No mueve el prereg-19 de su diseño firmado. Es lo que el director pidió: **la investigación extensa
primero.** Lo que sigue, cuando él lo diga, es un prerregistro de ingeniería del mundo (semillas,
versiones, determinismo, coste) antes de la primera línea de simulador.

---

## Fuentes consultadas (8-ago-2026, lado humano — Regla 27)
- Identificabilidad causal desde intervenciones: [von Kügelgen et al.](https://arxiv.org/pdf/2409.02772) · [identificabilidad general](https://arxiv.org/pdf/2310.15450) · [intervenciones suaves](https://arxiv.org/pdf/2307.06250) · [múltiples distribuciones](https://arxiv.org/pdf/2402.05052)
- Contingencia sensomotora y self: [Sensorimotor Contingencies as a Key Drive of Development](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6904889/) · [Science Robotics — sense of self](https://www.science.org/doi/10.1126/scirobotics.adn2733) · [robot en el espejo](https://arxiv.org/pdf/2011.04485)
- Empowerment: [pre-entrenamiento con empowerment](https://arxiv.org/abs/2510.05996) · [empowerment y exploración](https://arxiv.org/pdf/2107.07031) · [process empowerment](https://iopscience.iop.org/article/10.1088/2632-072X/adf2ec)
- Televisor ruidoso y progreso: [Beyond Noisy-TVs (LPM)](https://arxiv.org/pdf/2509.25438) · [gradient-momentum coupling](https://arxiv.org/pdf/2605.05856) · [incertidumbre aleatoria](https://arxiv.org/pdf/2102.04399)
- Objetos y ranuras: [dual-state slot attention](https://arxiv.org/pdf/2606.12601) · [repensar OCR para dinámica de video](https://arxiv.org/html/2606.23436) · [QASA](https://arxiv.org/pdf/2601.12936)
- Conservación y simetrías: [Noether Networks](https://dylandoblar.github.io/noether-networks/noether_networks_neurips_ml4phys_2021_CR.pdf) · [conservación agnóstica al modelo](https://arxiv.org/pdf/2301.07503) · [simetrías de EDOs por regresión simbólica](https://arxiv.org/pdf/2506.19550)
- Análisis dimensional: [Dimensionally Consistent Learning with Buckingham Pi](https://arxiv.org/abs/2202.04643) · [regresión simbólica con análisis dimensional](https://arxiv.org/pdf/2411.15919) · [análisis dimensional automático para EDPs](https://arxiv.org/pdf/2601.06535)
