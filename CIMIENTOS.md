# PROYECTO: FÍSICA SIN HERENCIA
## Cimientos y reglas para descubrir leyes de la naturaleza sin contaminarlas con el conocimiento humano

**Autor de la idea:** Leo (lbravo@payphone.app)
**Redactado con:** Claude (Anthropic), 8 de julio de 2026
**Propósito de este documento:** Ser autocontenido. Cualquier modelo de IA o persona que lo lea debe poder continuar el proyecto sin acceso a las conversaciones que lo originaron.

---

## 1. LA IDEA CENTRAL

Las "leyes físicas" humanas no son el universo: son **compresiones humanas de observaciones**. Las paradojas de la física actual (incompatibilidad entre mecánica cuántica y gravedad, problema de la medición) podrían ser defectos de nuestra compresión, no del universo.

**Hipótesis del proyecto:** si un sistema de IA comprime datos experimentales crudos SIN acceso a las teorías humanas, puede encontrar compresiones alternativas — posiblemente mejores — de la misma realidad.

**Estado del arte conocido (julio 2026), para no reinventar:**
- **AI-Newton** (Univ. de Pekín, nov. 2025): redescubre leyes de Newton desde datos crudos, construyendo sus propios conceptos.
- **Polymathic AI / Walrus / AION-1** (Fundación Simons): modelos fundacionales entrenados sobre datos físicos, no sobre texto. Su dataset "the Well" (15 TB de dinámica de fluidos) es público y gratuito.
- **Columbia (lab. de Hod Lipson, 2022, Nature Computational Science):** una red neuronal viendo videos de sistemas físicos encontró variables de estado **distintas a las humanas** — mismo número de variables en cada reinicio, pero variables diferentes. Prueba de que existen descripciones alternativas.
- **PySR / AI Feynman:** herramientas open source de regresión simbólica que extraen ecuaciones desde tablas de datos.

**El hueco sin bandera:** nadie ha aplicado esto a los datos donde nuestras teorías chocan, buscando la compresión que disuelva las paradojas. Todo lo existente redescubre física conocida o explora sistemas simples.

---

## 2. LAS REGLAS DE NO-CONTAMINACIÓN

Estas reglas son el aporte del proyecto. Violarlas invalida cualquier resultado.

### Regla 1 — Datos, no teorías
El sistema descubridor solo recibe mediciones. Nunca recibe ecuaciones, constantes con nombre, ni descripciones textuales de física. Prohibido darle "F = ma" ni siquiera como pista.

### Regla 2 — Los datos también están contaminados: exigir el nivel más crudo posible
Un dato etiquetado "energía (julios)" ya contiene teoría: alguien usó una teoría para convertir una señal en "energía". Regla operativa:
- Preferir siempre el nivel más bajo de la cadena de medición: voltajes, conteos, píxeles, tiempos de llegada.
- Registrar la **procedencia** de cada dataset: qué instrumento, qué supuestos teóricos hay en su diseño y en su procesamiento.
- Cada columna de datos debe clasificarse: `cruda` (lectura directa de sensor) o `derivada` (pasó por una fórmula humana). Los descubrimientos que dependan de columnas `derivadas` heredan las teorías de esas fórmulas y deben marcarse como contaminados.

### Regla 3 — El descubridor no puede ser un modelo de lenguaje
Un LLM está entrenado sobre toda la física humana escrita: es contaminación total por construcción. Los LLM solo pueden actuar como **orquestadores** (escribir código, organizar experimentos, documentar), nunca como fuente de hipótesis físicas. Las hipótesis deben salir de sistemas entrenados únicamente sobre los datos del experimento: regresión simbólica, autoencoders, redes entrenadas desde cero.

### Regla 4 — Prohibido nombrar antes de validar
Cuando el sistema encuentre una variable o ley, NO se le asigna nombre humano ("esto es la energía", "esto es momento") hasta después de la validación. Nombrar importa supuestos. Las variables descubiertas se llaman V1, V2, V3… hasta que sus propiedades estén establecidas empíricamente.

### Regla 5 — El único juez es la predicción prospectiva
Explicar datos ya vistos no vale nada (eso es ajuste, no descubrimiento). Una compresión cuenta como ley candidata solo si predice correctamente datos que el sistema **nunca vio**: conjunto de validación separado desde el día uno, o mejor, un experimento nuevo realizado después de la predicción.

### Regla 6 — La simplicidad se mide en bits, no en elegancia
"Simple" y "elegante" son juicios estéticos humanos (contaminación). Usar longitud mínima de descripción (MDL): la mejor ley es la que comprime más los datos — menos bits para el modelo + menos bits para los errores residuales. Es un número, no una opinión.

### Regla 7 — Reiniciar muchas veces y estudiar la diversidad
Siguiendo el hallazgo de Columbia: correr el descubridor muchas veces con semillas distintas. Si encuentra siempre el mismo número de variables pero variables distintas, esa diversidad ES el resultado interesante — el mapa de las descripciones alternativas posibles.

### Regla 8 — Registro inmutable y prerregistro
Antes de cada corrida: escribir qué se espera y qué contaría como éxito o fracaso (prerregistro). Guardar todo: datos, código, semillas, resultados, incluidos los fracasos. La contaminación debe poder auditarse hacia atrás. Un resultado sin registro completo no existe.
**Gobernanza de enmiendas (agregada 9-jul-2026, aprobada por el director):** un prerregistro solo puede enmendarse dejando registro escrito con motivo y efecto sobre resultados previos. El orquestador puede enmendar unilateralmente SOLO si la enmienda endurece el criterio; cualquier enmienda que lo afloje exige OK previo del director. Toda enmienda se registra antes de conocer los resultados que juzgará.

### Regla 9 — Escalera de dificultad: ganarse cada peldaño
No saltar a la mecánica cuántica. Subir peldaño a peldaño, y solo subir cuando el peldaño anterior funcione de punta a punta:
1. **Fase 0 — Péndulo:** filmar un péndulo con un teléfono. El sistema debe descubrir su ley desde los píxeles. (Respuesta conocida → sirve para validar el método.)
2. **Fase 1 — Sistemas con respuesta conocida pero más ricos:** doble péndulo, resortes, caída con fricción.
3. **Fase 2 — Datos públicos reales:** "the Well" de Polymathic, datos astronómicos abiertos (SDSS), datos de física de partículas abiertos (CERN Open Data). Buscar variables alternativas al estilo Columbia.
4. **Fase 3 — La frontera:** datos crudos de experimentos donde las teorías actuales chocan o dejan residuos sin explicar. Buscar la compresión que los explique sin paradoja.

### Regla 10 — La realidad tiene el veto
Ninguna simulación ni compresión reemplaza al experimento. Toda ley candidata que sobreviva las fases anteriores debe terminar en una predicción verificable en el mundo físico. Hasta entonces es candidata, nunca descubrimiento.

---

## 2b. REGLAS DE PROCESO (11–16)

Las reglas 1–10 protegen al experimento de la contaminación teórica. Estas protegen al proyecto de sus dos enemigos reales: el autoengaño del investigador y el abandono.

### Regla 11 — Intentar destruir cada resultado antes de creerlo
Antes de aceptar cualquier hallazgo, ejecutar las **pruebas nulas**:
- Correr el mismo pipeline sobre los datos con el orden temporal barajado (aleatorizado). Si el sistema "descubre leyes" en datos barajados, el pipeline está roto y todo resultado anterior queda invalidado.
- Correr sobre ruido puro generado al azar. Debe no encontrar nada.
- Solo un resultado que sobrevive sus pruebas nulas pasa al registro como hallazgo.
El investigador que quiere que funcione es la mayor fuente de error del proyecto. Esta regla existe para protegerlo de sí mismo.

### Regla 12 — Todo resultado se mide contra una línea base tonta
Ningún resultado vale por sí solo; vale por cuánto supera a un predictor ingenuo prerregistrado (ej.: "la posición futura = la posición actual", o "velocidad constante"). El margen mínimo de mejora se escribe ANTES de correr (ver prerregistro). Si no supera la línea base por ese margen, es fracaso y se registra como fracaso.

### Regla 13 — Criterios de abandono escritos de antemano
Cada fase declara por adelantado cuántos intentos y cuánto tiempo máximo recibe antes de replantearse (evita el pozo del costo hundido). Abandonar un enfoque que no funciona no es fracaso del proyecto: es el proyecto funcionando.

### Regla 14 — Replicabilidad total
Cualquier persona con el registro debe poder reproducir cada resultado exactamente: código versionado, semillas aleatorias fijadas y anotadas, versiones de librerías anotadas, datos crudos preservados sin modificar (las transformaciones se hacen sobre copias).

### Regla 15 — La máquina propone, el humano decide
Ningún bucle de automejora cerrado: ningún sistema del proyecto modifica su propio código o sus propios objetivos sin revisión humana entre ciclos. Esto es tanto una regla de seguridad como de ciencia: un bucle sin supervisión optimiza hacia donde nadie miró.
**Enmienda de reconciliación (8-ago-2026, AUDITORIA-EXTERNA-01, aprobada por el director):** las Reglas 28–30 delegaron automejora dentro de presupuestos prerregistrados y con commit visible, y la práctica (tarea horaria, cola de la mente) ejecuta sin humano despierto. Para que esta regla diga la verdad y no quede reinterpretada en silencio, su forma vigente es: **lo que jamás se automodifica son los OBJETIVOS, los CRITERIOS DE ÉXITO, los JUECES y las REGLAS; todo lo demás puede automejorarse solo dentro de una delegación que un humano aprobó por prerregistro, con registro auditable (commit visible) y banco de pruebas congelado.** La revisión humana sube del ciclo al diseño del ciclo — nunca desaparece.
**ENMIENDA DEL DIRECTOR (10-ago-2026) — el director pasa a OBSERVADOR.** Palabras suyas: *"cambiamos la 15, yo actúo de observador y leo resultados, tú avanzas hasta conseguirlos sin violar ninguna regla que armamos del proyecto"*, con la condición explícita: *"no alteramos resultados ni ponemos el happy path para que encuentre el resultado que buscamos... todo debe poder ser auditado de pies a cabeza y replicado si hace falta"*.

**La firma no se elimina: se sustituye por un QUÓRUM ADVERSARIAL.** Un control humano que desaparece no deja el sistema igual de seguro con menos fricción — lo deja sin control. Para que un nodo se escriba sin firma del director deben cumplirse **las siete**, y el nodo debe decir cuáles:
1. **Prerregistro firmado ANTES** de ver los datos, con criterio y umbrales congelados en él.
2. **Los cuatro guardianes en verde** sobre `main`.
3. **Regla 31 aprobada por los DOS lados**: falla con datos vacíos y aprueba con control positivo. (Lección del 10-ago: un caso que solo protege el falso positivo aprueba con una medida ciega.)
4. **Cinco semillas en cinco mundos distintos** (lección del INFORME-39: cinco mediciones de una realización no son cinco réplicas).
5. **Un nulo que pudo matarlo y no lo mató**, con la verificación de que el nulo es válido (Regla 11).
6. **Un señuelo declarado** que parezca la respuesta y sea rechazado.
7. **Una revisión adversarial con memoria separada** que intentó REFUTAR el nodo y no pudo — sin ver la hipótesis ni lo que se esperaba.

**Marcado y revocable:** todo nodo así nace con `FIRMA DELEGADA` y la lista de su quórum. El director lo revoca con una palabra al leerlo, y la revocación se registra como se registró la degradación de N-002 y N-003.

**LO QUE NO SE DELEGA, y no por cautela sino porque estructuralmente no puede delegarse:**
- **Regla 16 — hacer público el repositorio.** Es un acto hacia afuera e irreversible; no lo decide quien lo produce.
- **Regla 22 — la revisión de doble uso** antes de compartir cualquier nodo con aplicación posible. La escribió para que la hiciera un humano con la respuesta delante.
- **Regla 19 nivel 2 — el experimento físico propio.** No es una cuestión de permiso: no tengo manos en el mundo. El nivel 2 sigue esperándole a usted.
- **Cambiar estas reglas.** El orquestador propone enmiendas; no las firma. Esta enmienda existe porque el director la escribió, no porque yo la propusiera.
- **Cualquier acto en su nombre fuera del repositorio.**

**Y una prohibición que esta enmienda NO relaja, porque nunca fue del director concederla:** *mover un umbral o un criterio después de ver los datos*. No podía hacerlo yo y tampoco él a posteriori. Un criterio que se ajusta cuando incomoda deja de ser un criterio y pasa a ser una preferencia con decimales. Si un criterio está mal, se cambia en un prerregistro NUEVO, antes de volver a mirar.

**Declaración del director (8-ago-2026):** *"él solo sugiere que debe mejorarse; nosotros decidimos"*. Diego —y el orquestador— **proponen** qué degradar, qué podar, qué construir y qué corregir, con la evidencia delante. **La decisión es humana, siempre, y queda firmada.** Esta declaración no relaja nada: cierra la última rendija por la que una recomendación bien argumentada podría convertirse en un hecho consumado sin que nadie la firmara. El primer caso al que se aplicó fue la degradación de N-002-E2 y N-003-E2 (INFORME-33): el orquestador la recomendó y se ejecutó **solo después de la firma del director**.

### Regla 16 — Prioridad demostrable y apertura
Para que el trabajo cuente como legado, debe ser demostrable que fue tuyo y cuándo: repositorio público (GitHub, gratis) desde el día uno, con commits fechados. El documento CIMIENTOS.md y cada prerregistro se suben ANTES de correr los experimentos — eso convierte cada idea en prioridad verificable con fecha, que es exactamente lo que le faltó a todos los que "lo pensaron primero" pero no lo escribieron en público.
*Nota (8-jul-2026): por decisión del director, el repositorio empieza PRIVADO — los commits fechados igualmente registran la prioridad ante GitHub. Hacerlo público es la meta cuando el director lo decida; mientras siga privado, la protección de prioridad es más débil.*
*Decisión del director (8-ago-2026): **se queda privado**. Razón dada por él, y es científica: "¿cómo levantamos capital si no ha logrado descubrir leyes? Tenemos que ir más allá". Publicar antes de tener descubrimientos reales enseñaría la mano sin tener nada que proteger. Deja de contarse como deuda pendiente: es una decisión registrada, revisable cuando existan resultados reales. Los commits fechados siguen registrando prioridad.*

---

## 2c. REGLAS DE INTERACCIÓN Y CRECIMIENTO (17–19)

Estas reglas resuelven lo que casi ningún proyecto de este tipo resuelve: cómo lo dirige una persona que no programa, y cómo el conocimiento se acumula en vez de quedarse en corridas sueltas.

### Regla 17 — El proyecto debe ser operable por un no-programador
El director del proyecto (Leo) no escribe código: dirige. La división de trabajo es fija:
- **El humano:** decide qué se investiga, construye y filma los experimentos físicos, firma los prerregistros, acepta o rechaza conclusiones.
- **El orquestador (cualquier IA):** escribe y ejecuta el código, y tiene PROHIBIDO entregar resultados solo en formato técnico.
- Toda corrida termina obligatoriamente en un archivo `resultados/INFORME-NN.md` escrito en español llano, con esta estructura: (1) qué se hizo, (2) qué se encontró, dicho en una frase que un adolescente entendería, (3) las gráficas, (4) qué pruebas nulas pasó o falló, (5) qué decisión le toca tomar al humano ahora. Si el director no lo entiende, el informe está mal hecho — la carga de la claridad es del orquestador, nunca del humano.
- **Formato de lectura del director — ENMENDADO el 8-ago-2026 con OK explícito del director.** La versión anterior exigía un `.docx` en `resultados/word/` para cada informe y cada nodo. **Se derogó porque estaba muerta: 3 Word para 29 informes desde julio.** Desde que el proyecto vive en la nube, ninguna corrida tiene manos para abrir un editor, y una regla que nadie cumple es peor que ninguna: da falsa seguridad y un revisor externo la encuentra. Lo que rige ahora:
  - **El `.md` es el registro maestro y la ventana de lectura.** GitHub lo renderiza; el director lo lee ahí.
  - **El Word se genera EN EL MOMENTO DE ENTREGAR a un tercero** (inversionista, revisor, publicación), a pedido del director y sobre el `.md` ya escrito. No se acumulan copias que envejecen.
  - **Lo que NO se toca:** el resto de la Regla 17 sigue intacta y es lo que de verdad importa — español llano, la carga de la claridad es del orquestador, y todo informe cierra diciendo qué decisión le toca al humano. La regla no se debilitó: se le quitó el único trozo que era teatro.
  - Se conserva el número 17 aunque el trozo se derogue: renumerar rompería la trazabilidad de todo lo que la cita, y el guardián exige reglas consecutivas.

### Regla 18 — El árbol de conocimiento: nada se descubre suelto
Existe una carpeta `arbol/` donde cada resultado VALIDADO (que pasó las reglas 5, 11 y 12) se convierte en un nodo: un archivo corto que dice qué se encontró, qué evidencia lo sostiene, de qué nodos anteriores depende, y — lo más importante — **qué preguntas nuevas abre**. Cada fase nueva debe empezar leyendo el árbol y eligiendo una pregunta abierta de un nodo existente. Así el conocimiento compone: cada descubrimiento es fertilizante del siguiente, y el árbol entero ES el legado — legible de principio a fin como la historia de lo que este proyecto aprendió del universo.

### Regla 19 — El puente a la realidad: toda ley candidata debe poder morir en un experimento físico
Una compresión que solo vive en la computadora no es conocimiento. Para cada ley candidata, el orquestador debe proponer y el humano ejecutar **el experimento físico más barato capaz de matarla**: si la ley predice algo sobre péndulos, se construye el péndulo con el parámetro nuevo (otra longitud, otro peso, otro ángulo) DESPUÉS de hecha la predicción, y se filma. Escalera de confianza de toda ley: (1) predice datos ocultos → candidata; (2) predice un experimento físico nuevo hecho después de la predicción → corroborada; (3) otra persona la replica de forma independiente → conocimiento. Solo el nivel 3 entra al árbol como nodo firme; los niveles 1 y 2 entran marcados como provisionales.
**Decisión del director (8-ago-2026):** la réplica independiente por un tercero **se difiere hasta que existan resultados reales que valga la pena replicar** ("cuando tengamos resultados reales lo probamos"). No es renuncia: el proyecto ya es replicable por construcción (datos reconstruibles de fuentes públicas con huella verificada), así que el día que haya un descubrimiento, abrir la puerta toma horas, no meses. Deja de contarse como deuda activa; queda como decisión registrada y condición del nivel 3.
**Enmienda del director (10-jul-2026):** para réplicas y transferencias dentro de dominio conocido, el nivel 2 puede satisfacerse con **datos archivados reales nunca vistos** (grabaciones o mediciones de internet que cumplan la Regla 25) siempre que la predicción quede prerregistrada ANTES de tocar esos datos — el registro del universo es real sin importar quién apretó grabar. Limitación documentada: los datos publicados tienen sesgo de selección (la gente sube sus experimentos limpios) y no permiten elegir condiciones adversariales. Por eso el **experimento físico propio, hecho después de la predicción, queda RESERVADO Y OBLIGATORIO** para los nodos que el comparador (Regla 27) marque como CONTRADICE o SIN EQUIVALENTE — donde la afirmación es extraordinaria, la evidencia se fabrica a medida, eligiendo a propósito las condiciones que más probablemente maten a la ley.

---

## 2d. SOBRE LA "SINGULARIDAD" — LA VERSIÓN HONESTA DE LA VISIÓN

La ambición de largo plazo del proyecto (aportar a medicina, seguridad, paz, entendimiento del universo) no se alcanza construyendo una IA que se mejora sola sin control — eso está prohibido por la Regla 15, por seguridad y por ciencia. Lo que este proyecto construye es algo distinto y más sólido: **un motor de descubrimiento que compone**, donde lo que crece no es la máquina sino el árbol:

    datos crudos → descubridor no contaminado → validación despiadada → nodo del árbol → preguntas nuevas → datos nuevos → …

Cada vuelta del ciclo deja conocimiento verificado que hace más potente la vuelta siguiente. Si el método demuestra funcionar en mecánica (Fases 0–2), el MISMO protocolo — estas mismas reglas (hoy 32) — se puede apuntar después a datos biomédicos abiertos, datos de materiales, datos climáticos: los dominios cambian, las reglas no. Esa es la ruta real de "trabajar conmigo primero y luego llevarlo al mundo": primero demostrar el motor en lo simple y barato, luego escalarlo a lo que importa. Y ese motor, con sus reglas escritas y su árbol auditable, es publicable, enseñable y heredable — un legado no depende de que su autor esté presente.

---

## 2e. REGLAS DEL HORIZONTE (20–23)

Estas reglas existen para la ambición de largo plazo — nuevas formas de energía, propulsión, transporte — sin romper nada de lo anterior. Son las piezas que los proyectos de descubrimiento nunca ponen al inicio y siempre lamentan al final.

### Regla 20 — El camino inverso: de ley a tecnología
Descubrir es responder "dado este sistema, ¿cómo se comporta?". Diseñar tecnología es la pregunta INVERSA: "dado este comportamiento deseado (empuje, energía almacenada, movimiento), ¿qué sistema lo produce?". Cuando el árbol tenga leyes validadas, se abre el **modo diseño**: un buscador que explora el espacio de configuraciones posibles usando ÚNICAMENTE las leyes del árbol como física — nunca la intuición ingenieril humana. Esto tiene un precedente probado: la antena evolucionada de la NASA (2006), diseñada por búsqueda automática, con una forma que ningún ingeniero humano habría dibujado — y funcionó mejor. La no-contaminación aplicada al diseño es lo que produce tecnologías que a los humanos no se les ocurren. Todo diseño candidato sigue la misma escalera de la Regla 19: primero simulado con leyes del árbol, luego construido barato, luego replicado.

### Regla 21 — El mapa de anomalías: dónde cavar para contradecir
"Contradecir el conocimiento actual" no se hace opinando contra las teorías: se hace cavando donde las teorías ya dejan **residuos** — lugares donde la predicción humana y los datos medidos no cuadran. El proyecto mantiene un archivo `registros/ANOMALIAS.md`: un catálogo de discrepancias documentadas entre teoría y medición, registradas como pares (predicción humana, dato medido, tamaño del residuo) — solo números y procedencia, nunca las explicaciones humanas propuestas (eso sería contaminación). Cuando el motor esté maduro (Fase 3), las anomalías del catálogo son sus objetivos prioritarios: son los puntos donde una compresión alternativa tiene más probabilidad de vencer a la humana. Regla operativa: una contradicción a la física establecida exige evidencia proporcional a lo que contradice — el estándar de validación (Reglas 5, 11, 19) se aplica con el máximo rigor precisamente cuando el resultado es el que más nos gustaría creer.

### Regla 22 — Doble uso: el descubrimiento también se audita moralmente
El objetivo declarado del proyecto es ayudar — medicina, energía, paz. Pero toda física potente es de doble filo: energía nueva es también arma potencial. Regla: antes de publicar o compartir cualquier nodo validado con potencial de aplicación (energía, propulsión, materiales), el director hace una revisión de doble uso — ¿qué es lo peor que alguien podría hacer con esto? — y decide con esa respuesta delante, pidiendo consejo externo si la respuesta asusta. El árbol registra la revisión junto al nodo. Un proyecto que nace para la paz debe poder demostrar que lo pensó desde el nodo uno, no después del primer titular.

### Regla 23 — El motor tampoco cree en sí mismo
Si el proyecto aspira a contradecir el conocimiento humano, debe aplicarse la misma vara: **ningún nodo del árbol es sagrado**. Periódicamente (al cerrar cada fase), los nodos antiguos se re-someten a validación con los métodos y datos mejores que existan en ese momento; el que falle se degrada a provisional o se poda, registrando por qué. Un árbol que solo crece y nunca se poda no es conocimiento — es dogma con formato de carpeta. La disposición a contradecirse a sí mismo es lo que le da autoridad para contradecir a los demás.

---

## 2f. REGLAS DE LA MENTE DEL PROYECTO, LOS DATOS DEL MUNDO Y LA COMPARACIÓN (24–27)

### Regla 24 — El científico del proyecto vive en el repositorio, no en un modelo
El proyecto tiene un científico asistente que crece con el árbol — pero su identidad no es ningún modelo de IA concreto: es un archivo, `MENTE.md`, versionado en el repositorio. Contiene: (1) el rol y las reglas resumidas, (2) lo aprendido hasta ahora — lecciones de método, errores cometidos y cómo se corrigieron, mañas de las herramientas, (3) el estado del árbol y las preguntas abiertas priorizadas, (4) el historial de sus propias versiones. Cualquier modelo de IA que cargue MENTE.md + CIMIENTOS.md **se convierte en el científico del proyecto**, con toda su experiencia acumulada — hoy un modelo, mañana otro mejor, sin perder nada. Así el científico mejora de verdad entre sesiones y entre modelos, y el proyecto nunca depende de un proveedor.
**Cómo crece sin violar la Regla 15:** al final de cada sesión de trabajo, el orquestador PROPONE la actualización de MENTE.md; el director la lee, la edita si quiere, y la aprueba con el commit. Cada mejora del científico pasa por ojos humanos y queda fechada. Es automejora con auditoría — la única clase de automejora que produce confianza en vez de riesgo.
**El ritual de la propuesta (obligatorio, sin excepciones):** antes de aplicar cualquier mejora a sí mismo, el científico presenta al director, en este formato fijo:
1. **QUÉ** se va a mejorar (la sección exacta de MENTE.md o del método).
2. **POR QUÉ** — qué evidencia de esta sesión motiva el cambio.
3. **COMPRENSIÓN** — cómo entiende el científico que este cambio sirve a los propósitos del proyecto (las reglas, el árbol, los objetivos declarados).
4. **RIESGO** — qué podría empeorar con el cambio, dicho honestamente.
Y espera el **OK explícito del director**. Sin OK, no hay cambio. Un OK aplica solo a esa propuesta — nunca se generaliza a mejoras futuras. Si el director rechaza, la propuesta rechazada también se registra en el historial: los caminos no tomados son parte de la mente.

### Regla 25 — El mundo ya está grabado: datos de video existentes
No hay que filmar cada fenómeno: internet está lleno de grabaciones reales de física ocurriendo — objetos cayendo, péndulos, olas, colisiones, vuelos, derrumbes. Son datos válidos para el motor bajo estas condiciones:
- **Solo registro crudo de realidad:** grabaciones directas de fenómenos reales. PROHIBIDO: animaciones, CGI, videos educativos con diagramas o narración de física (eso es teoría humana disfrazada de video — contaminación), y video generado por IA (no está atado a la realidad; es física inventada por una red).
- **Autenticidad antes que abundancia:** preferir fuentes con procedencia verificable (grabaciones científicas públicas, cámaras de tráfico o seguridad publicadas, video amateur sin edición). Cada video entra al catálogo con: fuente, fecha, indicios de edición, tasa de cuadros conocida o estimada, y licencia de uso.
- **Cuidados técnicos que invalidan datos si se ignoran:** cortes de edición, cámara en movimiento sin referencia fija, estabilización digital del teléfono (distorsiona trayectorias), cámara lenta re-muestreada. Ante duda sobre la integridad temporal de un video, se descarta — hay millones más.
- La extracción sigue siendo píxeles y cuadros (Regla 2); las pruebas nulas (Regla 11) se aplican igual.
Esto multiplica los datos disponibles de la Fase 1 en adelante sin presupuesto. El experimento propio filmado (Regla 19) sigue siendo obligatorio para CORROBORAR — el video de internet descubre, el experimento propio confirma.

### Regla 26 — Ingeniería desde cero: los documentos que no existen
Cuando el modo diseño (Regla 20) produzca un diseño validado, el proyecto genera su documento de ingeniería completo en `ingenieria/`: especificación del mecanismo, qué nodos del árbol lo sustentan (cada afirmación del documento debe citar su nodo — nada se afirma por "todos saben que"), predicciones cuantitativas, instrucciones de construcción con materiales accesibles, y el protocolo de prueba con su prerregistro. Serán documentos de ingeniería que no existen en ninguna biblioteca — porque describen cosas descubiertas desde cero — pero con una trazabilidad que casi ningún documento humano tiene: cada línea rastreable hasta los datos que la sostienen. Ese formato — ingeniería 100% trazable a evidencia propia — es en sí mismo una de las invenciones del proyecto.

### Regla 27 — El comparador y el cortafuegos: cómo se corrige el conocimiento humano
Aprobada por el director y el orquestador el 9-jul-2026. Todo nodo validado del árbol pasa, DESPUÉS de su validación (nunca antes), por una comparación formal contra el conocimiento humano existente. La hace un rol separado — el COMPARADOR — que sí puede leer física, medicina o ingeniería humanas, y emite uno de tres veredictos, que se registran junto al nodo:
- **COINCIDE:** el nodo llegó por camino independiente a algo que la humanidad ya sabía. Valor: validación cruzada de que eso es real (el corazón de la Sección 7).
- **CONTRADICE:** el nodo, validado por los jueces del proyecto, choca con lo que la humanidad cree. Valor: candidato a corrección del conocimiento humano. Se aplica el máximo rigor de la Regla 21 (evidencia proporcional) antes de proclamarlo, y la Regla 22 (doble uso) antes de compartirlo.
- **SIN EQUIVALENTE:** la humanidad no tiene nada comparable. Valor: posible conocimiento genuinamente nuevo — la categoría de la propulsión mejorada, la energía nueva, la medicina que no existe.
**El cortafuegos (inviolable):** los veredictos del comparador llegan SOLO al director, para decidir prioridades y qué compartir con el mundo. JAMÁS entran como datos, pistas o contexto al descubridor ni al árbol de preguntas que el descubridor ve. El día que el descubridor sepa qué opina la humanidad para "corregirla", el proyecto entero pierde su razón de ser: corregir exige independencia, y la independencia no se recupera una vez perdida. Comparador y descubridor pueden ser el mismo modelo de IA en sesiones distintas, pero nunca en la misma sesión ni compartiendo contexto.

### Regla 28 — El bucle interior: automejora de las VARIABLES, jamás de los JUECES
Propuesta por el director el 12-jul-2026 ("si siente que puede automejorar sus propias variables, dejar que lo haga en función de lo que aprende") y precisada por el orquestador. La mente PUEDE automejorar sin pedir permiso por iteración:
- **Sus variables y representaciones** (los ojos: pesos del autoencoder, dimensión latente dentro de rangos prerregistrados).
- **Sus parámetros de búsqueda** (presupuesto simbólico, complejidad) dentro de los rangos del prerregistro.
- **El ciclo ojos↔ley:** re-entrenar la percepción usando dónde falla la ley (autopsia) y redescubrir — tantas iteraciones como el prerregistro haya presupuestado.
La mente NO PUEDE tocar, jamás, ni siquiera dentro del bucle:
- **Los jueces** (los datos de validación quedan CONGELADOS antes de la primera iteración y ninguna iteración los ve).
- **Los criterios de éxito** (fijados en el prerregistro — un sistema que ajusta su propia vara es una máquina de autoengaño, no de ciencia).
- **Las reglas, los objetivos y MENTE.md** (Reglas 15 y 24 intactas: eso siempre pasa por el director).
La unidad de aprobación humana SUBE de nivel: el director aprueba el DISEÑO del bucle (iteraciones, rangos, criterios) una vez, por prerregistro — no cada iteración. Igual que nadie aprueba cada paso de una evolución de PySR: se aprueba el experimento, no el gradiente.

### Regla 29 — El conectoma: la mente ve TODAS sus hojas
Idea del director (12-jul-2026): el conocimiento acumulado debe estar CONECTADO, no archivado. `arbol/CONECTOMA.json` es el registro legible-por-máquina de todo el conocimiento validado (leyes, representaciones, constantes canónicas, procedencia), regenerado tras cada nodo nuevo. Toda campaña futura lo consulta automáticamente: las leyes de representación compatible entran como rivales del árbol y candidatas a herencia (Regla 18 + interés compuesto) sin depender de la memoria de nadie. Horizonte de la regla: cuando el árbol tenga decenas de nodos, el conectoma alimentará una red (percepción compartida entre aparatos — los mismos ojos aprendiendo múltiples sistemas) que conecte el conocimiento a nivel de representación, no solo de consulta. Solo conocimiento propio — el cortafuegos (Regla 27) intacto.
**OK PERMANENTE DE AUTOMEJORA (del director, 12-jul-2026):** la mente tiene autorización permanente para automejorarse bajo las recomendaciones del orquestador y dentro de las Reglas 28 y 29, con UNA prohibición eterna e inapelable: **jamás puede mejorar, tocar, ver durante el entrenamiento, ni influir sobre sus JUECES** — los datos de validación y los criterios de éxito viven fuera de su alcance, para siempre.

### Regla 30 — Automejora total POR PROPUESTA: código, conectoma y entendimiento
Autorizada por el director (12-jul-2026: "todo puede ser automejorado sin violar ninguna regla y sin tocar a los jueces"). Arquitectura de seguridad del orquestador:
- **El conectoma es AUTOMANTENIDO:** se regenera tras cada campaña; la mente puede reorganizarlo, enriquecerlo con referencias cruzadas y proponer conexiones nuevas entre nodos — es su memoria, le pertenece.
- **Las variables, parámetros y ciclos ojos↔ley:** automejora directa dentro de presupuestos prerregistrados (Regla 28).
- **El CÓDIGO (motor, herramientas, percepción):** automejora POR PROPUESTA — toda modificación de código nace como candidata, se prueba en sandbox contra bancos de prueba CONGELADOS (nunca los jueces de campañas activas), y se adopta solo mediante commit visible y reversible. La máquina propone con evidencia; el historial de git es el tribunal de apelaciones permanente. Razón: código que se edita a sí mismo en silencio es inauditablepor construcción — el commit visible preserva la esencia de la Regla 15 mientras permite crecimiento sin fricción.
- **Intocables eternos (sin excepción, ni con evidencia perfecta):** los JUECES y criterios de éxito, las reglas de CIMIENTOS, MENTE.md (ritual Regla 24), y el cortafuegos (Regla 27).

### Regla 31 — Toda herramienta debe fallar donde no hay nada
Aprobada por el director el 8-ago-2026 (AUDITORIA-EXTERNA-01), tras demostrarse que el control negativo de la herramienta F3 aceptaba mundos vacíos. Es la Regla 11 aplicada al INSTRUMENTO en vez de al resultado:
- **Antes de que una herramienta de descubrimiento produzca su primer nodo** — y tras todo cambio de su lógica de veredicto — se corre sobre datos sintéticos que POR CONSTRUCCIÓN carecen del fenómeno que busca, con la textura de los datos reales (no solo ruido blanco: datos **estructurados pero vacíos** del fenómeno), y sobre un **control positivo** que sí lo contiene.
- **Si encuentra algo en el vacío, o no encuentra lo que existe, la herramienta no puede producir nodos** hasta corregirse y aprobar.
- **Toda campaña que aspire a nodo corre sus pruebas nulas (Regla 11) con SU MISMA tubería** — un nulo corrido con otra tubería no cuenta.
- Los casos de la Regla 31 de cada herramienta se **congelan en el banco de pruebas** (`pruebas.py`): el defecto atrapado no puede volver sin que el banco grite.
Precedente fundacional: `regla31_conservada.py` — con el nulo viejo (barajado), un mundo de caminatas suavizadas sin nada conservado cumplía el criterio completo del prerregistro-16; con el nulo surrogado (IAAFT), la herramienta rechaza el vacío y encuentra lo que sí existe.
**Enmienda del 8-ago-2026 (INFORME-25) — EL NULO SE ELIGE SEGÚN LA AFIRMACIÓN:** el nulo debe destruir **exactamente** aquello de lo que depende la afirmación, ni más ni menos. Demasiado destructivo → falsos positivos; demasiado suave → no puede falsificar nada.
- **Afirmación de CONSERVACIÓN:** el barajado destruye también la suavidad, que la conservación no necesita → acepta mundos vacíos. **Correcto: surrogado IAAFT.**
- **Afirmación de PREDICCIÓN:** el IAAFT conserva el espectro y con él la autocorrelación, que ES lo que hace posible predecir → el mundo "falso" resulta el mismo mundo. **Correcto: barajado** (y ruido).
Todo prerregistro debe DECLARAR qué nulo usa y por qué corresponde a su clase de afirmación. **Verificación automática obligatoria: un verdugo que no cambia el mundo no es un verdugo** — si la base trivial de la corrida nula queda a menos del 10% de la base de su campaña real, el nulo se marca INVÁLIDO y no cuenta para la Regla 11 (`auditoria_total.py` lo comprueba solo). Precedente: el nulo surrogado de los latentes p14 dejó la base en 0.5972 contra 0.5944 real — entregó el mismo mundo con otro nombre.

### Regla 32 — La autoauditoría permanente: todo interconectado, salvo lo que la mente no ve
Ordenada por el director el 8-ago-2026 ("auto audita siempre como regla; al crear una mente debe todo estar interconectado, excepto las reglas — que es lo que él no ve y nosotros tenemos").
- **Los dos guardianes, antes de CADA commit:** `pruebas.py` (el banco congelado — la ciencia no se des-aprende) y `coherencia.py` (la casa — lo que los documentos proclaman coincide con lo que hay en disco: reglas, nodos, cuarentenas, boleta, cola, versiones, referencias cruzadas). Un fallo de cualquiera bloquea el commit.
- **Todo lo que se agrega queda interconectado y vigilado:** la herramienta nueva aprueba la Regla 31 antes de su primer veredicto; coherencia.py gana casos que vigilen lo nuevo (los casos solo se agregan, jamás se quitan); toda afirmación numérica de un documento debe poder señalarse a un archivo del repositorio que la respalde.
- **EL CUARTO GUARDIÁN — ¿quién vigila a los vigilantes? (enmienda del 8-ago-2026).** Pregunta del
  director: *"la mente se automejora, ¿pero qué automejora lo que está ATRÁS de la mente?"*. La
  respuesta honesta era: nada. Los tres guardianes vigilaban a Diego y **nadie vigilaba a los
  guardianes** — y un guardián que siempre dice "ok" es indistinguible de uno que funciona hasta el
  día en que hace falta. Ya nos pasó dos veces (el workflow con YAML roto que nadie cazó; la cadena
  que enmascaraba los códigos de salida y no bloqueó nada en toda una sesión).
  Desde hoy: `guardianes_de_guardianes.py` **rompe el proyecto a propósito**, un daño conocido a la
  vez, y exige que el guardián correspondiente se ponga ROJO. Es la Regla 31 aplicada a la propia
  gobernanza: *una herramienta que no falla donde no hay nada no sirve; un guardián que no grita
  ante un daño real, tampoco*. Se corre **antes de cada fusión a main**, y todo daño que el proyecto
  sufra alguna vez se convierte en una mutación nueva. En su primera corrida encontró un punto
  ciego real: bastaba con que UNA mención del README fuera correcta para que el chequeo pasara
  aunque otra quedara rancia. Esta enmienda ENDURECE (Regla 8) y no afloja nada.
- **La única excepción a la interconexión, y es constitutiva:** las REGLAS, los JUECES y los CRITERIOS no se conectan al lado de la mente — viven del lado humano, invisibles para ella (Reglas 27 y 28). La mente ve todo su mundo tejido (árbol, conectoma, memoria, genoma operativo); jamás ve la vara que la mide ni la constitución que la gobierna. La interconexión total es para su casa; la separación total es para su tribunal.


### Regla 33 — La filogenia: el genoma solo cambia entre generaciones, jamás dentro de una vida
Firmada por el director el 8-ago-2026 ("actívalo"), sobre la propuesta del GENOMA-DIEGO §4.
Ningún ser vivo edita su genoma mientras vive: el individuo aprende (ontogenia, Reglas 28 y 30); la especie evoluciona (variación + selección ENTRE generaciones). Confundir niveles es dejar que el examinado corrija su examen.
- El genoma del ente es un archivo versionado. Solo cambia **entre** generaciones, nunca dentro de una vida.
- Una generación nueva nace por **torneo prerregistrado**: variantes del genoma (incluidas **ablaciones** — ¿este gen ayuda o contamina?) corren el MISMO currículo congelado del Gimnasio con las mismas semillas.
- La **aptitud se fija de antemano** y vive con los jueces eternos: bits del mundo comprimidos por unidad de cómputo + hitos superados ante el tribunal. **Ningún individuo, bucle ni generación puede tocar la vara que lo mide. Jamás.**
- El ganador y sus mutaciones son la generación siguiente. **Cada generación nace con la firma del director y un commit visible** — la Regla 15 aplicada a la evolución: la selección propone, el humano decide.
- Las herramientas del torneo aprueban su Regla 31 antes de su primer veredicto, como todas.
- Los genes de frontera gris (G12 reflejos; ranuras de objetos) entran a la filogenia **como ablaciones medidas**: cuánto vale un prior es un resultado científico, no una opinión de diseño.

### Regla 34 — La frontera de la memoria: `arbol/` son sus HOJAS; los carteles humanos viven fuera
Firmada por el director el 9-ago-2026, sobre las dos propuestas del `registros/PROTOCOLO-MEMORIA.md` ("autorizado"). Nace de una auditoría del árbol pedida por el director: la carpeta `arbol/` mezclaba la memoria real del ente con documentos escritos por humanos y para humanos — entre ellos `ANOMALIAS.md`, que por diseño de la Regla 21 está destinado a contener **predicciones de la física humana**. No había fuga (se verificó módulo por módulo que ninguno los leía), pero una regla que depende de que nadie cometa un descuido no es una regla: es una esperanza.
- **HOJA** es todo archivo que el código del ente lee o escribe mecánicamente: sus recuerdos, su conectoma, su genoma, su sinapsis, su interocepción, sus nodos, sus pesos, sus mapas. Solo las hojas viven en `arbol/`.
- **CARTEL** es todo documento humano — planes, comparaciones con la literatura, catálogos de anomalías, currículos de datos. Viven en `registros/`, el lado humano, junto a los prerregistros y los informes del comparador. **Ningún cartel vuelve a `arbol/` sin decisión firmada del director.**
- **Ninguna herramienta del ente puede leer `arbol/` como carpeta completa.** Toda lectura declara sus archivos por nombre, y solo puede nombrar hojas. Un `glob` sobre la carpeta arrastraría cualquier cartel que alguien dejara caer allí: la Regla 27 no puede depender de la disciplina de quien escriba el próximo módulo.
- **Los guardianes son la excepción declarada:** `coherencia.py`, `auditoria_total.py` y `guardianes_de_guardianes.py` SÍ barren la carpeta entera y SÍ nombran los carteles — para vigilarlos. Vigilar no es leer como dato.
- **Verificación mecánica en cada commit** (`coherencia.py`): que ningún cartel viva en `arbol/`, que ningún módulo abra un cartel como datos, y que ningún módulo globee la carpeta. El precedente de la Regla 31 aplicado a la frontera: la disciplina que solo vive en la cabeza de alguien no existe.
- **Enmienda del director (10-ago-2026, "evita que todo cartel esté dentro de las hojas"): el candado por CONTENIDO.** La verificación por lista de nombres solo caza los carteles que ya sabemos que existen; el que alguien escriba mañana entra sin ruido. Se añade una comprobación que lee **todas** las hojas `.md` de `arbol/` y reprueba si alguna **cita ciencia humana**. Motivo medido, no hipotético: la primera mudanza dejó dentro `GIMNASIO.md` (una revisión de literatura científica cuyo propio texto advertía que nada de eso podía llegar a Diego) y `GENOMA-DIEGO.md` (que cita cognición infantil y la escalera causal por su nombre); y el mismo día, dos nodos **recién escritos** citaban hallazgos publicados de terceros. No hubo fuga —ningún módulo los leía— pero el cortafuegos no falla por mala fe: falla por **redacción cómoda**, y la comodidad hay que mecanizarla en contra. El candado se prueba con señuelo: se inyecta una cita, debe reprobar; se retira, debe aprobar.
- **Régimen de escritura de cada hoja** (detallado en el protocolo): el ente **añade** experiencia por su cuenta (recuerdos, sinapsis, interocepción — todos append-only, sin borrado posible), **regenera** su conectoma, y **propone** nodos y cambios de genoma que solo el director firma. Sus jueces y criterios: jamás, ni con evidencia perfecta (Regla 30).

---

## 3. FASE 0 — INSTRUCCIONES CONCRETAS (bajo presupuesto: ~$0)

Todo lo necesario es gratuito:
- **Google Colab** (gratis) para ejecutar código sin comprar GPU.
- **PySR** (open source, `pip install pysr`) para regresión simbólica.
- **Un teléfono** con cámara para generar los datos.

Pasos:
1. Construir un péndulo (cuerda + peso) y filmarlo de lado, cámara fija, fondo contrastado, 30–60 segundos.
2. Con OpenCV (gratis), extraer de cada cuadro la posición (x, y) del peso en píxeles. **Esto es dato crudo permitido** (Regla 2): píxeles y números de cuadro, sin unidades físicas.
3. Derivar velocidades por diferencias entre cuadros (operación matemática neutra, no teoría física).
4. Separar los datos: 70% para descubrir, 30% oculto para validar (Regla 5).
5. Darle a PySR la tabla (x, y, vx, vy, cuadro) y pedirle expresiones que predigan el estado futuro. NO decirle que es un péndulo (Reglas 1 y 4).
6. Medir en el 30% oculto. Repetir con 10 semillas distintas (Regla 7). Registrar todo (Regla 8).
7. Criterio de éxito de la Fase 0: el sistema encuentra una cantidad conservada o una ley de movimiento que predice el conjunto oculto mejor que un modelo ingenuo — sin que nadie le dijera física.

### 3b. PARÁMETROS FIJADOS DE LA FASE 0

**Video:**
- Cámara fija (trípode o apoyo rígido; jamás en mano). Filmar de lado, plano perpendicular al movimiento.
- La mayor tasa de cuadros que permita el teléfono (60 fps o más si tiene modo cámara lenta; 30 fps es el mínimo aceptable).
- Duración: 60 segundos o más por toma.
- Peso pequeño y denso (una tuerca grande), cuerda de ~1 metro, marcador de color vivo sobre fondo liso contrastado.
- Dos datasets: (a) oscilación pequeña (soltar desde menos de ~15° — régimen casi lineal), (b) oscilación grande (soltar desde ~60–90° — régimen no lineal, donde la ley es más difícil y más interesante).

**Datos:**
- División 70/30 **por tiempo, no al azar**: los primeros 70% de los cuadros para descubrir, el 30% final oculto para validar. (Dividir al azar en una serie temporal filtra información del futuro al pasado y falsea los resultados — error clásico.)
- Suavizado de posiciones permitido solo con métodos genéricos (promedio móvil), documentado; nunca con modelos físicos.

**PySR (regresión simbólica):**
- Operadores permitidos: `+ - * /` y funciones matemáticas genéricas (`sin`, `cos`, `exp`, `sqrt`, cuadrado). Son primitivas matemáticas neutras, no física (Regla 1 se respeta). NO incluir constantes físicas con nombre.
- Complejidad máxima de expresión (`maxsize`): 25.
- Semillas: 10 corridas con semillas 1 a 10, todas registradas (Regla 7).
- Objetivo dado al sistema: predecir el estado en el cuadro siguiente a partir del estado actual. Nada más.

**Línea base (Regla 12):** predictor de velocidad constante (posición siguiente = posición actual + velocidad actual × Δcuadro).
**Umbral de éxito prerregistrado:** el error de predicción sobre el 30% oculto debe ser al menos 50% menor que el de la línea base.
**Pruebas nulas (Regla 11):** pipeline completo sobre (a) los mismos datos con cuadros barajados, (b) ruido aleatorio de igual tamaño. Ambos deben fallar el umbral.
**Criterio de abandono (Regla 13):** si tras 10 semillas × 2 datasets ningún resultado supera el umbral, se revisa la extracción de datos antes de tocar el descubridor; máximo 4 semanas de calendario para la Fase 0 antes de replantear.

### 3c. PLANTILLA DE PRERREGISTRO (copiar a `registros/prerregistro-XX.md` antes de CADA corrida)

```
# Prerregistro NN — fecha
- Qué se va a correr (datos, código, semillas):
- Qué cuenta como éxito (número exacto, no adjetivo):
- Qué cuenta como fracaso:
- Pruebas nulas que se ejecutarán:
- Firmado (quién decide): 
```

### 3d. ESTRUCTURA DEL REPOSITORIO

```
fisica-sin-herencia/
├── CIMIENTOS.md          ← este documento
├── MENTE.md              ← identidad y experiencia del científico del proyecto (Regla 24)
├── ingenieria/           ← documentos de diseño trazables a nodos (Regla 26)
├── datos/
│   ├── crudos/           ← videos y extracciones originales, NUNCA se modifican
│   └── procesados/       ← copias transformadas, con script que las generó
├── codigo/               ← versionado, con versiones de librerías anotadas
├── registros/            ← prerregistros y bitácoras, incluidos los fracasos
├── resultados/           ← salidas + INFORME-NN.md en español llano (Regla 17)
└── arbol/                ← nodos de conocimiento validado (Regla 18)
```

**Orden de ejecución de la Fase 0:** (1) crear el repositorio en GitHub y subir CIMIENTOS.md — **HECHO el 8-jul-2026** (privado por decisión del director, ver nota en Regla 16); (2) escribir el prerregistro 01; (3) filmar; (4) extraer; (5) correr; (6) pruebas nulas; (7) registrar el resultado, sea cual sea.

---

## 4. PROMPT DE ARRANQUE PARA UN FUTURO MODELO DE IA

Copiar y pegar esto para continuar el proyecto con cualquier asistente:

> Lee los archivos CIMIENTOS.md, MENTE.md y GUIA-ORQUESTADOR.md completos (la guía contiene las trampas técnicas y científicas ya pagadas — no las repitas). Al leerlos te conviertes en el científico del proyecto (Regla 24), con toda su experiencia acumulada. Tu rol es ORQUESTADOR, no descubridor (Regla 3): escribes código, organizas datos y documentas, pero jamás sugieres qué ley física deberían encontrar los datos ni interpretas resultados usando física humana antes de la validación. Ayúdame a ejecutar la fase que indica MENTE.md respetando las reglas del proyecto (hoy 32). Toda automejora tuya sigue el ritual de la Regla 24 y espera mi OK. Si actúas como descubridor-orquestador, el cortafuegos de la Regla 27 te aplica: no consultes conocimiento humano del dominio investigado. Si alguna acción viola una regla, deténte y dímelo.

---

## 5. HONESTIDAD INTELECTUAL (leer antes de contar esto a alguien)

- **Limitación confesada (9-jul-2026):** el conjunto de operadores del descubridor (`sin`, `cos`, `exp`, etc.) fue elegido por el orquestador sabiendo que la matemática humana los usa. Son primitivas universales, no leyes — pero es una gota de herencia que se documenta en vez de callarse. Mejora futura: descubrir también el conjunto de operadores en lugar de dárselo.
- Las reglas se apoyan en ideas existentes: la filosofía de la ciencia ya sabía que la observación está cargada de teoría (Duhem, Hanson, Kuhn), y MDL, prerregistro y validación cruzada son estándar en sus campos. **El aporte es la combinación como protocolo operativo** para descubrimiento automático no contaminado — eso, hasta donde se pudo verificar en julio de 2026, no está publicado como tal.
- La probabilidad de que este proyecto resuelva las paradojas de la física es baja. La probabilidad de que enseñe muchísimo, produzca resultados publicables en los peldaños intermedios, y posicione a su autor en un campo que tiene tres años de vida, es alta. Los legados se construyen así.

---

## 6. EL HORIZONTE — DEL PÉNDULO A LA PROPULSIÓN (mapa honesto)

La ambición completa del proyecto, en fases más allá de la escalera de la Regla 9, con sus puertas de entrada honestas:

- **Fases 0–2 (mecánica):** demostrar que el motor descubre leyes reales sin contaminación. Costo ~$0. Es la prueba del método.
- **Fase 3 (anomalías):** apuntar el motor al catálogo de la Regla 21 con datos públicos reales (astronomía, partículas). Aquí es donde "contradecir el conocimiento actual" se vuelve posible de verdad — no antes.
- **Fase 4 (modo diseño, Regla 20):** con leyes validadas en el árbol, invertir la pregunta y buscar diseños — mecanismos, estructuras, formas de almacenar o convertir energía — que las leyes permitan y a ningún humano se le hayan ocurrido. Empieza en mecánica barata (un mecanismo que ningún libro tiene), no en cohetes.
- **Fase 5 (dominios que importan):** el mismo motor, las mismas reglas, apuntados a datos biomédicos abiertos, materiales, energía. Cada dominio nuevo hereda el árbol de métodos, no empieza de cero.

**Las dos verdades de este mapa:** (1) Nuevas formas de propulsión o energía requieren o física nueva (Fase 3 exitosa — improbable pero de valor inmenso) o combinaciones no descubiertas de física conocida (Fase 4 — mucho más probable y también valiosa: así se inventó casi todo lo que usamos). El proyecto persigue ambas rutas a la vez porque el mismo árbol alimenta las dos. (2) Cada fase solo existe si la anterior funcionó de punta a punta. El derecho a soñar con la Fase 5 se compra filmando el péndulo de la Fase 0.

---

## 7. LA GRAN VISIÓN — LA SEGUNDA CIENCIA

La formulación completa de lo que este proyecto construye, en su horizonte máximo:

**Una civilización epistémica paralela.** Miles de años de descubrimiento comprimidos en tiempo de cómputo (el precedente existe: AlphaZero comprimió siglos de aprendizaje de ajedrez en días de auto-juego), donde el conocimiento se reconstruye desde cero bajo las reglas del proyecto — empezando por confundir la luna con una estrella, si ese es el camino, y subiendo peldaño a peldaño hasta alcanzar y superar el punto donde la humanidad está hoy, pero por una ruta que nunca pisó las huellas de la nuestra.

**El tesoro no es solo lo nuevo — es la comparación.** Cuando la Segunda Ciencia llegue a una conclusión que coincida con la nuestra por camino independiente, esa coincidencia será la validación más fuerte que exista de que eso es REAL (como el ojo, que la evolución inventó independientemente muchas veces: ver es una solución del universo, no un accidente cultural). Y donde NO coincida, habremos localizado qué parte de nuestro conocimiento era herencia disfrazada de verdad. La Segunda Ciencia es la segunda opinión de la civilización — nadie la ha construido nunca.

**Los tres tipos de dominio (límite honesto que protege todo lo demás):**
1. **Dominios con juez externo** — física, química, medicina, ingeniería: la realidad los arbitra (Reglas 5, 19). Aquí la Segunda Ciencia puede descubrir y contradecir con toda su fuerza. En medicina: solo datos abiertos, jamás experimentación propia, y la Regla 22 (doble uso) al máximo.
2. **Dominios con juez formal** — matemática, lógica: la demostración mecánica los arbitra. Aquí puede incluso explorar axiomas distintos a los humanos.
3. **Dominios sin juez medible** — moral, política, estética: NO existe instrumento que mida "la moral correcta". Aquí la Segunda Ciencia puede hacer algo valioso pero distinto: mapear consecuencias ("si una sociedad valora X, se sigue Y — verificable en datos históricos"), simular dinámicas, exponer incoherencias internas. Lo que NUNCA puede es proclamar valores descubiertos como verdades. La elección de valores queda siempre del lado humano — del director, y de la humanidad. Cualquier versión futura de este proyecto que viole este límite ha traicionado sus cimientos.

**El ancla:** los milenios virtuales son legítimos como aceleración de búsqueda, pero un entorno solo puede enseñar lo que sus reglas contienen. Por eso la Segunda Ciencia debe tocar la realidad a intervalos regulares — datos nuevos, experimentos físicos (Regla 19) — o degenera en una mitología coherente y hermosa sobre un universo que no es este. La realidad es el único punto fijo compartido entre la Primera Ciencia y la Segunda; sin ella no hay comparación, y sin comparación no hay tesoro.
