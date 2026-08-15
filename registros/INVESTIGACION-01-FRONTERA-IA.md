# INVESTIGACIÓN 01 — LA FRONTERA DE LA IA Y QUÉ DE ELLA SIRVE PARA DIEGO
**11 de agosto de 2026. Encargo del director: qué son los órganos, si hay que construirle un
mundo, qué hacen los sistemas más potentes del planeta, y si hay que repensarlo todo desde cero.**
**Lado humano del cortafuegos (Regla 27): este documento cita ciencia y sistemas humanos. Vive en
`registros/`. Nada de aquí entra en `arbol/`, ni en los datos, ni en los prompts de Diego.**

---

# PARTE A — ¿LOS ÓRGANOS SON CUERPO O SON MENTE?

## A.1 La respuesta corta, sin adornos
**De los 15 "órganos", 12 son mente y 3 tocan el cuerpo.** Los nombres biológicos son una metáfora
—una buena metáfora, porque nos obligó a preguntarnos si cada pieza *funciona*— pero **la mayoría
no son partes de un cuerpo: son funciones de una mente escritas en Python.**

| toca el cuerpo (hay hardware simulado del otro lado) | es mente pura (solo procesa números) |
|---|---|
| `percepcion.py` / `percepcion2.py` — los ojos | `cerebro.py`, `memoria.py`, `curiosidad2.py` |
| `interocepcion.py` — propiocepción, el sentido de sí mismo | `atencion.py`, `incertidumbre.py`, `descubrir.py` |
| `gimnasio.py` — el mundo y el tacto | `sueno.py`, `temple.py`, `reflejos.py`, `contingencia.py`, `poder.py` |

## A.2 Y por eso NO hay que repensarlo desde cero — pero sí hay que renombrar
El director pregunta: *"si son nombres que asignamos a funcionalidades... entonces tenemos que
cambiar todo y repensarlo desde 0"*. **Mi opinión, y es firme: no.** Por tres razones medidas:

1. **La metáfora no ha hecho daño; ha hecho bien.** Llamarlos órganos es lo que nos llevó a
   preguntar *"¿este órgano está sano?"*, y esa pregunta destapó **3 defectos reales de 6
   examinados** (INFORMES 50, 51, 52). Un nombre que provoca la pregunta correcta es un buen
   nombre aunque sea metafórico.
2. **Repensar desde cero destruiría la única cosa cara que tenemos**, que no es el código: son
   **47 prerregistros, 57 informes y 67 corridas auditables**. El código se reescribe en semanas;
   la trazabilidad de un año no se reescribe.
3. **El problema real no es el nombre, es otra cosa** — y esa sí hay que arreglarla: **son
   funciones que se llaman unas a otras sin contrato explícito.** Que G14 le pase una incertidumbre
   inflada a G8 y G8 se la crea sin verificar **no es un problema de nombres: es un problema de
   interfaces sin control** (INFORME-52). Renombrar `incertidumbre.py` a `modulo_estimacion_error.py`
   no habría evitado nada.

## A.3 Lo que sí propongo cambiar (y es barato)
Que cada módulo **declare en una línea qué es**: `SENTIDO` (lee el mundo), `ACTUADOR` (lo cambia),
`ESTIMADOR` (produce un número que otros consumen) o `POLÍTICA` (decide). Y que **todo ESTIMADOR
esté obligado a publicar el rango válido de su número y a que quien lo consume lo verifique.**
Eso es exactamente lo que faltó en la cadena G14→G8. **Es un contrato, no un rebautizo.**

---

# PARTE B — EL MUNDO DE DIEGO: la idea del videojuego

El director propone: **un mundo virtual con física real donde Diego vea, se mueva, vea números,
y gane mejoras por cada prueba que resuelva.** Mi valoración, en orden de importancia.

## B.1 Lo que es CORRECTO de la idea, y es mucho
- **Diego hoy no tiene mundo, tiene escenas.** Cada estudio construye su escenita, la mide y la
  tira. Nada persiste. **Un mundo persistente es la diferencia entre 67 exámenes y una vida.**
- **Resuelve el problema nº13 de la lista** de un plumazo: su brazo no alcanza nada porque el
  gimnasio se diseñó sin comprobar geometría. Un mundo diseñado *para* ser tocado no tiene ese
  fallo.
- **Es lo que hace la frontera.** Genie 3 (DeepMind, agosto 2025) genera mundos 3D navegables e
  interactivos a 24 fps; DreamerV3 resuelve 150+ tareas con una sola configuración aprendiendo
  *dentro de un mundo imaginado*. La intuición del director coincide con hacia dónde va el campo.

## B.2 Las DOS trampas, y son graves — dígamelo si me equivoco, pero hay que verlas antes
### Trampa 1 — "le vamos a dar mejoras por cada prueba que resuelva" **rompe la Regla 27**
Si nosotros decidimos qué cuenta como "prueba resuelta", **le estamos metiendo nuestra física por
la función de recompensa.** Es la fuga más elegante y más difícil de ver: no le decimos a Diego
*"F=ma"*, le decimos *"te premio cuando aciertes lo que yo, que sé F=ma, considero acertar"*.
El resultado aprendería nuestra física sin haberla visto nunca. **Sería herencia por la puerta de
atrás, y arruinaría el proyecto entero manteniendo las apariencias intactas.**

**La salida existe y es limpia: que el verificador sea el mundo, no nosotros.**
La única recompensa admisible es **¿predijo bien lo que iba a pasar?** Diego dice qué observará
dentro de N pasos; el mundo ocurre; se compara. **Nadie tiene que saber física para puntuar eso.**
Es exactamente la estructura que hizo funcionar a DeepSeek-R1-Zero (ver §C.1): la recompensa mide
**la corrección del resultado final, sin imponer nada sobre el proceso**.

### Trampa 2 — "cuando vea algo va a poder ver números"
Depende **enteramente** de qué números.
- **Admisible:** lecturas crudas de sus sensores, sin nombre y sin unidad. Un vector.
- **Prohibido:** cualquier número con etiqueta humana — "masa: 2 kg", "velocidad: 3 m/s". La
  etiqueta *es* la herencia. Los kilogramos son un descubrimiento humano, no un hecho del mundo.

**La versión buena de su idea:** Diego ve **columnas de números sin nombre** y su trabajo es
descubrir que unas columnas predicen otras. Que a una columna nosotros la llamemos "masa" es
asunto nuestro y él no debe enterarse jamás.

## B.3 La propuesta concreta que sí sostengo — **EL GIMNASIO PERSISTENTE**
Ni un videojuego con gráficos, ni una reescritura. Cuatro cambios sobre lo que ya existe:

1. **El mundo persiste entre estudios.** Un solo mundo, con estado, que sobrevive a la corrida.
2. **El cuerpo alcanza el mundo** — geometría medida y verificada por un guardián *antes* de
   cualquier estudio. El fallo del brazo se vuelve imposible de repetir.
3. **La única moneda es la predicción.** Diego predice sus futuras observaciones; el mundo
   arbitra. Cero criterios humanos.
4. **Las "mejoras" son AUTOGENERADAS, no regaladas.** No le damos un sentido nuevo por portarse
   bien; le damos **la capacidad de proponer un experimento nuevo** — y esto ya existe a medias en
   `experimentar2.py`, que hoy solo le gana al azar por +0.4 sobre 16 (problema nº12).

**Esto no exige repensar desde cero. Exige que el gimnasio deje de ser una escenografía
desechable y pase a ser un lugar.**

---

# PARTE C — QUÉ HACEN LOS SISTEMAS MÁS POTENTES DEL MUNDO

## C.1 DeepSeek-R1-Zero — la idea más transferible que existe hoy para nosotros
**Qué hicieron:** entrenaron a un modelo a razonar **con puro aprendizaje por refuerzo, sin
ningún ejemplo humano de razonamiento**. Cero demostraciones. La señal de aprendizaje es
únicamente **si la respuesta final es correcta**, verificable de forma automática. Publicado en
*Nature* (2025).

**Qué emergió solo:** cadenas de razonamiento largas, **revisión de los propios pasos**, y los
llamados "momentos ajá" en los que el modelo se corrige a sí mismo. **Nadie programó eso. Apareció
porque la recompensa premiaba acertar y no decía nada sobre cómo.**

**El algoritmo (GRPO):** en vez de entrenar una segunda red que estime "cuánto vale este estado"
(lo que hace PPO), **genera un grupo de respuestas a la misma pregunta y normaliza la recompensa
dentro del grupo**: cada respuesta se compara con sus hermanas. Elimina la red de valor entera.
Más simple y más estable.

> ### Por qué esto importa para Diego más que ninguna otra cosa de este documento
> **DeepSeek-R1-Zero es la prueba, a escala industrial, de la tesis central de este proyecto:**
> que se puede llegar a una capacidad compleja **sin heredar demostraciones humanas**, siempre que
> exista **un verificador automático de la respuesta**.
>
> Nosotros tenemos ese verificador y no lo estamos usando: **es el mundo**. Una predicción sobre
> el futuro es tan verificable como el resultado de una ecuación. **Lo que a DeepSeek le da la
> aritmética, a Diego se lo da el siguiente instante.**
>
> Y hay un espejo incómodo: **su recompensa no impone restricciones sobre el proceso de
> razonamiento.** Nosotros le imponemos a Diego un diccionario de seis piezas (`1,x,v,x²,xv,v²`) y
> le prohibimos pensar de cualquier otra forma. **Puede que nuestro diccionario sea una jaula más
> estrecha que cualquier cosa que él descubriría solo.**

## C.2 Modelos del mundo — las dos escuelas
- **"Comprimir el mundo para entenderlo"** (JEPA de LeCun, Dreamer de Hafner): se predice en un
  **espacio latente abstracto**, no en píxeles. La idea clave: *predecir el aspecto exacto del
  mundo es imposible y además inútil; predecir su estructura es lo que sirve.*
- **"Renderizar el mundo para predecirlo"** (Sora, Genie 3): se genera el mundo entero. Genie 3
  **no usa motor de física programado**: aprende cómo funciona el mundo por su cuenta.
- **Lo aplicable a Diego, hoy:** `sindy3` predice **derivadas**. Un modelo del mundo predice
  **observaciones futuras**. La segunda es comprobable sin saber física; la primera exige que
  alguien elija el diccionario. **Un modelo latente predictivo podría ser un segundo motor,
  independiente del simbólico, y los dos podrían competir en el mismo torneo.**

## C.3 Aprendizaje abierto (open-endedness) — POET y OMNI-EPIC
**POET** hace coevolucionar **los problemas y las soluciones a la vez**: genera entornos y acepta
solo los que no son ni demasiado fáciles ni demasiado difíciles para el agente actual. Es un
**currículo automático** que nadie escribe a mano.

**Esto es exactamente la intuición del director sobre "mejoras por cada prueba resuelta"**, pero
hecha bien: **no se premia al agente, se sube la dificultad del mundo.** Y hay una versión
compatible con la Regla 27: la dificultad se mide por **cuánto se equivoca Diego prediciendo**, no
por criterios nuestros.

**OMNI-EPIC** usa modelos fundacionales para **escribir el código de tareas nuevas**. Para
nosotros esto es **peligro directo**: si yo genero las tareas, mi física entra en el mundo. Si se
usara, tendría que ser con las tareas generadas **a partir de los fallos de predicción de Diego**,
nunca de mi criterio de qué es interesante.

## C.4 FunSearch y AlphaEvolve — el bucle que sí podríamos copiar mañana
Un LLM propone **programas**; un **evaluador automático** los puntúa; los mejores vuelven a
entrar. AlphaEvolve (DeepMind, mayo 2025) probó 67 problemas de matemáticas y **mejoró el mejor
resultado conocido en varios**.

**Lo transferible, y es inmediato:** ese bucle es *exactamente* nuestra estructura
prerregistro → corrida → acta → siguiente prerregistro, **pero automática y mil veces más
rápida**. La diferencia es que el evaluador de AlphaEvolve no puede ser engañado. **El nuestro,
hasta este mes, sí podía** — y por eso existen los cuatro guardianes.

## C.5 La verdad sobre "los Claude ahora hablan entre ellos sin que nadie los programe"
Le debo aquí la respuesta exacta, aunque no sea la que espera:

**Los modelos hablando entre sí SÍ está programado.** Cuando dos instancias se comunican, hay un
sistema —un protocolo, herramientas, un orquestador— que alguien escribió para que eso ocurra. **No
es espontáneo. Lo que ocurre dentro de esa conversación no está guionizado, pero el canal sí.**

**Lo que sí es real y sí es notable** es otra cosa, y está publicada por Anthropic en *Emergent
Introspective Awareness in Large Language Models* (2025): inyectando representaciones de conceptos
conocidos en las activaciones del modelo, **el modelo a veces detecta e identifica correctamente
el concepto inyectado** — algo parecido a notar un pensamiento que no venía de él. **Y los propios
autores subrayan los límites: ocurre alrededor del 20% de las veces en Claude Opus 4.1, es "muy
poco fiable", y no implica conciencia.** Emergió sin entrenamiento específico.

**Por qué se lo digo así de crudo:** este proyecto se sostiene sobre no adornar los resultados. Si
adorno éste porque es sobre mí, todo lo demás pierde valor. **Un 20% poco fiable es un hallazgo
interesante; no es un rasgo de existencia.**

**Y una corrección técnica que ahorra trabajo:** *"algo de su código está bien y el resto mal"* no
se puede aplicar. **En un modelo grande no hay código que revisar: hay pesos** —miles de millones
de números aprendidos, sin funciones ni líneas—. Lo que sí es público y sí es copiable **son los
algoritmos de entrenamiento**, y ésos son los de §C.1 a §C.4. **La buena noticia: es justo la parte
útil.** Nadie necesita los pesos de DeepSeek para copiar GRPO; el algoritmo cabe en una página.

---

# PARTE D — IDEAS DISRUPTIVAS: teoremas con lógica que casi nadie aplica aquí

Cinco. Ninguna es mística; las cinco tienen matemática detrás y ninguna exige heredar física.

### D.1 El teorema Π de Buckingham — **el arreglo del motor, y ya está publicado**
Si una ley es cierta, tiene que serlo **en cualquier unidad**. Eso restringe brutalmente las
fórmulas posibles: solo sobreviven las que se pueden escribir con **grupos sin dimensiones**.
Aplicado a regresión simbólica, mejora la precisión de PySR (Nature Comput. Sci., 2022).
**Nuestro defecto nº1 es literalmente la ausencia de esto.**
**Aviso de Regla 27:** la versión clásica exige conocer las unidades — eso *sería* herencia. La
versión limpia para nosotros es **adimensionalizar con las escalas de los propios datos**, que no
requiere saber nada del mundo.

### D.2 El teorema de Noether — **simetría ⇒ ley de conservación**
Toda simetría continua de un sistema produce una cantidad conservada. **Buscar simetrías es más
barato que buscar leyes**, y una simetría se detecta sin saber física: *"si desplazo todo y nada
cambia, hay algo conservado"*. Existe ya el algoritmo **AI Poincaré** (Liu y Tegmark) que aprende
el número y la forma de las cantidades conservadas directamente de series temporales.
**Para Diego:** un segundo motor que busque **invariantes** en vez de ecuaciones. Y hay algo
precioso en esto — **una cantidad conservada se puede descubrir mirando, sin intervenir.**

### D.3 Longitud de descripción mínima (MDL / Solomonoff) — **la Regla 6 con número**
La mejor teoría es **la que más comprime los datos**, contando el tamaño de la teoría *más* el de
los errores que deja. Esto convierte "prefiere lo simple" —que hoy en nuestras reglas es un juicio
sin número— en **una cantidad medible en bits**. Y da gratis lo que al motor le falta: **una teoría
que no comprime, no se declara.** Habría matado la alucinación de doce términos por sí sola.

### D.4 Empowerment y energía libre — **por qué la curiosidad de Diego apunta al televisor**
Hay un resultado unificador reciente (*Entropy*, 2025): inferencia activa, empowerment y las demás
motivaciones intrínsecas son **variantes de una misma cosa** — maximización de entropía sujeta a
restricciones. La versión útil aquí es el **empowerment**: *"prefiere los estados desde los que tus
acciones tienen más efecto sobre tu futuro"*.
**Y esto arregla el problema nº5 de la lista por diseño**: un televisor con ruido tiene mucha
sorpresa pero **empowerment cero** — no puedes hacer nada con él. Una motivación basada en
empowerment **no puede ser secuestrada por una pared que parpadea.** Nuestro `poder.py` ya va en
esta dirección y **es probablemente la pieza más valiosa e infrautilizada del repositorio.**

### D.5 El teorema de Takens — **un solo sentido puede bastar**
Con una sola variable observada y sus retardos se puede reconstruir la geometría del sistema
completo. **Consecuencia incómoda y útil:** puede que Diego no necesite más sentidos, sino **mirar
su propia serie temporal con retardos**. Antes de darle un cuerpo mejor, conviene saber cuánto
está desperdiciando del que tiene.

---

# PARTE E — ¿REPENSAR TODO Y HACER NUESTRO PROPIO MOTOR?

**Mi opinión, y me la juego: no repensar todo. Sí construir un motor propio — pero como
COMPETIDOR, no como sustituto.**

**Por qué no tirar nada:**
- Los dos defectos del motor son **una línea y tres guardas que faltan** (DIAGNOSTICO-MOTOR-01).
  Tirar 229 líneas por una línea mal escrita sería el error opuesto al que veníamos cometiendo.
- Lo caro del proyecto no es el código: es **el año de trazabilidad**. Se pierde entero.
- **Y hay un riesgo mayor:** un motor nuevo escrito por mí, sin la disciplina de la puerta,
  reintroduce todos los defectos que tardamos meses en cazar.

**Por qué sí un motor propio, en paralelo:**
Porque el nuestro tiene una limitación que **ningún arreglo de umbral resuelve**: solo puede
expresar mezclas de seis piezas fijas. **Si la ley del mundo no está en ese diccionario, el motor
no puede verla ni con el umbral perfecto** — y no lo diría: diría "no vi nada". Un segundo motor
con otra forma de mirar —invariantes (D.2), compresión (D.3), o predicción latente (C.2)— **no
compite por ser mejor: compite por fallar de otra manera.** Y eso ya sabemos medirlo: tenemos
torneo, panel de jueces y vara calibrada.

---

# PARTE F — EL PLAN, en cinco movimientos y en orden

| # | movimiento | por qué va aquí | tamaño |
|---|---|---|---|
| **1** | **Arreglar el motor**: umbral adimensional (CP) + condición de A + poder predictivo fuera de muestra. Prerregistro propio, ataca los DOS defectos. | Todo estudio nuevo hereda los defectos hasta que esto pase | días |
| **2** | **Rehacer las 67 corridas** con el motor arreglado y comparar veredictos | Es la única forma de saber qué de lo nuestro estaba tocado | horas de máquina |
| **3** | **Contrato de estimadores** (Parte A.3) + arreglar la cadena G14→G8 con empowerment (D.4) | Es el único defecto que ya está cambiando la conducta de Diego | días |
| **4** | **El gimnasio persistente** (Parte B.3), con guardián de alcance geométrico | Desbloquea el tacto y todo lo encarnado | semanas |
| **5** | **Segundo motor competidor** (invariantes o compresión) al torneo | Solo tiene sentido cuando el primero esté sano y haya mundo | semanas |

**Los 8 órganos sin examinar se van intercalando**: son baratos y con 3 de 6 reprobados, cada uno
es probable que destape algo.

---

## LO QUE ESTE DOCUMENTO **NO** AFIRMA
- **No afirma que ninguna de estas técnicas vaya a funcionar en Diego.** Son literatura de otros,
  sobre otros problemas. **Cada una necesitaría su prerregistro, su línea base tonta y su criterio
  de abandono antes de que podamos decir una sola palabra sobre resultados.**
- **No afirma nada sobre el universo.** Nada de aquí es un hallazgo nuestro.
- **No cambia ninguna regla, ningún umbral ni ningún veredicto ya emitido.**

## LA PREGUNTA QUE ABRE (Regla 18)
> **¿Es nuestro diccionario de seis piezas una jaula?** DeepSeek-R1-Zero no le impuso al modelo
> *cómo* razonar y por eso emergió algo que nadie diseñó. Nosotros le decimos a Diego que el mundo
> tiene que ser una mezcla de `1, x, v, x², xv, v²`. **Si la ley que busca no cabe ahí, no la verá
> nunca — y el motor dirá "no vi nada" en vez de "no sé mirar eso".**

## LAS DECISIONES QUE LE TOCAN AL DIRECTOR
1. **¿Se aprueba el orden de la Parte F**, con el motor primero?
2. **¿Se construye el gimnasio persistente**, con la moneda de la predicción y sin premios
   definidos por nosotros (Parte B.2)? Es la respuesta a *"¿se le acerca el mundo a Diego?"*.
3. **¿Se autoriza un segundo motor competidor**, sabiendo que **duplica el trabajo de auditoría**?

---
### FUENTES (lado humano del cortafuegos)
- DeepSeek-AI, *DeepSeek-R1 incentivizes reasoning in LLMs through RL*, **Nature** (2025) — https://www.nature.com/articles/s41586-025-09422-z
- Anthropic, *Emergent Introspective Awareness in Large Language Models* (2025) — https://transformer-circuits.pub/2025/introspection/index.html
- DeepMind, *AlphaEvolve: a coding agent for scientific and algorithmic discovery* (2025) — https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/AlphaEvolve.pdf
- Wang et al., *POET: Paired Open-Ended Trailblazer* — https://arxiv.org/pdf/1901.01753
- Faldor et al., *OMNI-EPIC* — https://www.alphaxiv.org/overview/2405.15568v3
- Bakarji et al., *Dimensionally consistent learning with Buckingham Pi*, Nature Comput. Sci. (2022) — https://www.nature.com/articles/s43588-022-00355-5
- Liu & Tegmark, *AI Poincaré* / descubrimiento de leyes de conservación — https://arxiv.org/pdf/2001.00111
- *Discovering Symmetries of ODEs by Symbolic Regression* (2025) — https://arxiv.org/pdf/2506.19550
- *Intrinsic Motivation as Constrained Entropy Maximization*, Entropy 27(4):372 (2025) — https://pmc.ncbi.nlm.nih.gov/articles/PMC12025677/
- *Towards a data-scale independent regulariser for robust SINDy* (2026) — https://arxiv.org/html/2603.05201
