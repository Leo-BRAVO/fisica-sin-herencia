# Prerregistro 19 — HITO 0: el nacimiento (la frontera yo/mundo por contingencia) — 8 de agosto de 2026
**Estado: FIRMADO por el director el 8-ago-2026. Es la campaña prioritaria del proyecto.**
**Por qué ascendió (y es evidencia, no entusiasmo):** el INFORME-30 probó tres formas distintas de
separar "hay ley" de "hay textura con deriva" MIRANDO datos ya grabados, y las tres fallaron. No fue
mala suerte: en un mundo que solo se observa, esa información no está. Lo que rompe la degeneración
es **intervenir** — cambiar una condición a propósito y ver qué cambia y qué no. Este prerregistro
construye justamente el órgano que le falta a Diego: la ACCIÓN. Se ejecuta después del prereg-18 y
del levantamiento del congelamiento. Genes G3 (acción), G4 (contingencia), G7 (juego) del GENOMA-DIEGO. Primera campaña del Gimnasio. TODO lo aprendido aquí queda marcado "sobre-el-simulador" — jamás entra al árbol como física del mundo (regla del Gimnasio).**

- **Pregunta:** con balbuceo motor puro y un detector de contingencia genérico, ¿EMERGE la
  frontera yo/mundo — sin que nadie se la programe? (El paradigma del móvil de la literatura
  infantil, llevado a un cuerpo simulado con gobernanza.)
- **El mundo:** PyBullet (local, gratuito). Escena mínima: suelo, 2–3 objetos móviles libres, un
  cuerpo articulado simple (3–5 grados de libertad con efector). Sin recompensas de tarea. Física
  del simulador estándar — es NUESTRO código, no el universo, y así se registra.
- **El ente en este hito:** ojos desde cero (la percepción conjunta ya validada en N-002-E2,
  re-entrenada SOLO con cuadros de este mundo — nada preentrenado; épocas 15, Adam 1e-3, semilla
  fija, latente inicial 8); comandos motores aleatorios (balbuceo, G7) con presupuesto
  prerregistrado de **20,000 pasos de simulación por semilla**; un modelo de contingencia genérico
  que estima, por cada variable latente, cuánta de su dinámica es explicada por los comandos
  motores recientes vs. nada (matemática neutra: comparación de predictores con/sin el comando
  como entrada, misma vara de rivales de siempre).
- **Éxito nivel A (la frontera emerge):** el mapa de contingencia separa las variables del cuerpo
  de las del mundo con exactitud ≥ 90% en episodios-juez CONGELADOS (episodios grabados con
  semillas apartadas antes del entrenamiento, donde la pertenencia cuerpo/mundo se conoce por
  construcción del simulador y el ente jamás la ve), replicado en ≥ 4/5 semillas — Y ADEMÁS la
  exactitud debe superar el máximo de la distribución nula (los dos controles de la Regla 31 de
  abajo): un umbral absoluto sin nulo no discrimina (lección INF-06, elevada por la AUD-EXT-01).
  El 90% es constante prerregistrada; si el nulo lo supera, manda el nulo.
- **Éxito nivel B (el primer no-yo):** entre las variables clasificadas como "mundo", la dirección
  de caída aparece como la componente de dinámica QUE NINGÚN comando motor modula (contingencia
  ≈ 0 en todas las acciones), replicada entre semillas. Interpretación comprometida de antemano:
  el primer invariante externo del ente — el límite de su agencia. (Solo-simulador; el nombre
  humano de eso no se le dice a nadie del lado del ente.)
- **Regla 31 (doble control, obligatorio antes del veredicto):**
  1. **Mundo sin agencia:** misma corrida con los motores DESCONECTADOS (los comandos se emiten
     pero no actúan): el detector NO debe encontrar un "yo" (ninguna variable con contingencia
     significativa). Si lo encuentra, el detector miente.
  2. **Control positivo:** corrida con un solo grado de libertad conectado: debe encontrar
     exactamente ese.
  Ambos casos se congelan en el banco de pruebas.
- **Verdugos clásicos (Regla 11) con la tubería propia:** episodios barajados y surrogados deben
  fracasar el nivel A.
- **Fracaso:** se registra tal cual; abriría preguntas sobre presupuesto de balbuceo, dimensión
  latente u ojos (el bucle interior de la Regla 28 puede explorar esas perillas dentro de rangos
  que este prerregistro fija: latente ∈ {4, 8, 12}, balbuceo ∈ {N, 2N}).
- **LECCIÓN DEL INFORME-30 INCORPORADA (añadida el 8-ago-2026, antes de firmar).** El detector de
  contingencia tiene **exactamente la misma forma matemática** que la ganancia honesta: una RESTA
  DE DOS PODERES PREDICTIVOS (con el comando motor como entrada vs. sin él). Por lo tanto hereda
  sus dos canales de mentira, ya medidos, y no se firma sin blindarlos:
  1. **Falso positivo por señales integradas.** Si una variable latente se comporta como paseo
     aleatorio, la resta fabrica contingencia donde no hay ninguna (medido: hasta +0.71 en un mundo
     sin ninguna ley). **Obligatorio antes del veredicto:** reportar, por cada variable latente, si
     es integrada, y correr el control 1 (motores desconectados) sobre las MISMAS variables. Si el
     control 1 da contingencia > 0 en cualquier variable, el veredicto queda anulado — no se
     "corrige", se anula.
  2. **Falso negativo por ruido.** Un 0.12% de ruido de observación borró una ley determinista real.
     El simulador no tiene ruido de cámara, así que aquí el canal está cerrado por construcción —
     **pero eso deja de ser cierto en cuanto el Gimnasio pase a video o a un cuerpo físico**, y se
     escribe aquí para que nadie lo olvide en el hito siguiente.
  3. **El nulo se elige según la afirmación** (enmienda de la Regla 31). La afirmación aquí es
     "este comando modula esta variable": el nulo correcto es **barajar los comandos manteniendo
     las series intactas**, no barajar las series. Barajar las series destruye la no estacionariedad
     y volvería a abrir el canal 1.
- **Nota de gobernanza:** este prerregistro NO habilita la filogenia (**Regla 33**, que sigue siendo
  propuesta sin firma; la Regla 32 sí está vigente y es la autoauditoría permanente) ni hitos
  posteriores: solo el hito 0.
- **Firmado:** Leo, director — 8-ago-2026, aprobación en conversación ("firmalo"), tras leer
  el ascenso a prioridad y el blindaje con la lección del INFORME-30.
