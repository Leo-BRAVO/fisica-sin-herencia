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

### Regla 16 — Prioridad demostrable y apertura
Para que el trabajo cuente como legado, debe ser demostrable que fue tuyo y cuándo: repositorio público (GitHub, gratis) desde el día uno, con commits fechados. El documento CIMIENTOS.md y cada prerregistro se suben ANTES de correr los experimentos — eso convierte cada idea en prioridad verificable con fecha, que es exactamente lo que le faltó a todos los que "lo pensaron primero" pero no lo escribieron en público.
*Nota (8-jul-2026): por decisión del director, el repositorio empieza PRIVADO — los commits fechados igualmente registran la prioridad ante GitHub. Hacerlo público es la meta cuando el director lo decida; mientras siga privado, la protección de prioridad es más débil.*

---

## 2c. REGLAS DE INTERACCIÓN Y CRECIMIENTO (17–19)

Estas reglas resuelven lo que casi ningún proyecto de este tipo resuelve: cómo lo dirige una persona que no programa, y cómo el conocimiento se acumula en vez de quedarse en corridas sueltas.

### Regla 17 — El proyecto debe ser operable por un no-programador
El director del proyecto (Leo) no escribe código: dirige. La división de trabajo es fija:
- **El humano:** decide qué se investiga, construye y filma los experimentos físicos, firma los prerregistros, acepta o rechaza conclusiones.
- **El orquestador (cualquier IA):** escribe y ejecuta el código, y tiene PROHIBIDO entregar resultados solo en formato técnico.
- Toda corrida termina obligatoriamente en un archivo `resultados/INFORME-NN.md` escrito en español llano, con esta estructura: (1) qué se hizo, (2) qué se encontró, dicho en una frase que un adolescente entendería, (3) las gráficas, (4) qué pruebas nulas pasó o falló, (5) qué decisión le toca tomar al humano ahora. Si el director no lo entiende, el informe está mal hecho — la carga de la claridad es del orquestador, nunca del humano.

### Regla 18 — El árbol de conocimiento: nada se descubre suelto
Existe una carpeta `arbol/` donde cada resultado VALIDADO (que pasó las reglas 5, 11 y 12) se convierte en un nodo: un archivo corto que dice qué se encontró, qué evidencia lo sostiene, de qué nodos anteriores depende, y — lo más importante — **qué preguntas nuevas abre**. Cada fase nueva debe empezar leyendo el árbol y eligiendo una pregunta abierta de un nodo existente. Así el conocimiento compone: cada descubrimiento es fertilizante del siguiente, y el árbol entero ES el legado — legible de principio a fin como la historia de lo que este proyecto aprendió del universo.

### Regla 19 — El puente a la realidad: toda ley candidata debe poder morir en un experimento físico
Una compresión que solo vive en la computadora no es conocimiento. Para cada ley candidata, el orquestador debe proponer y el humano ejecutar **el experimento físico más barato capaz de matarla**: si la ley predice algo sobre péndulos, se construye el péndulo con el parámetro nuevo (otra longitud, otro peso, otro ángulo) DESPUÉS de hecha la predicción, y se filma. Escalera de confianza de toda ley: (1) predice datos ocultos → candidata; (2) predice un experimento físico nuevo hecho después de la predicción → corroborada; (3) otra persona la replica de forma independiente → conocimiento. Solo el nivel 3 entra al árbol como nodo firme; los niveles 1 y 2 entran marcados como provisionales.

---

## 2d. SOBRE LA "SINGULARIDAD" — LA VERSIÓN HONESTA DE LA VISIÓN

La ambición de largo plazo del proyecto (aportar a medicina, seguridad, paz, entendimiento del universo) no se alcanza construyendo una IA que se mejora sola sin control — eso está prohibido por la Regla 15, por seguridad y por ciencia. Lo que este proyecto construye es algo distinto y más sólido: **un motor de descubrimiento que compone**, donde lo que crece no es la máquina sino el árbol:

    datos crudos → descubridor no contaminado → validación despiadada → nodo del árbol → preguntas nuevas → datos nuevos → …

Cada vuelta del ciclo deja conocimiento verificado que hace más potente la vuelta siguiente. Si el método demuestra funcionar en mecánica (Fases 0–2), el MISMO protocolo — estas mismas 19 reglas — se puede apuntar después a datos biomédicos abiertos, datos de materiales, datos climáticos: los dominios cambian, las reglas no. Esa es la ruta real de "trabajar conmigo primero y luego llevarlo al mundo": primero demostrar el motor en lo simple y barato, luego escalarlo a lo que importa. Y ese motor, con sus reglas escritas y su árbol auditable, es publicable, enseñable y heredable — un legado no depende de que su autor esté presente.

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
├── datos/
│   ├── crudos/           ← videos y extracciones originales, NUNCA se modifican
│   └── procesados/       ← copias transformadas, con script que las generó
├── codigo/               ← versionado, con versiones de librerías anotadas
├── registros/            ← prerregistros y bitácoras, incluidos los fracasos
├── resultados/           ← salidas + INFORME-NN.md en español llano (Regla 17)
└── arbol/                ← nodos de conocimiento validado (Regla 18)
```

**Orden de ejecución de la Fase 0:** (1) crear el repositorio público en GitHub y subir CIMIENTOS.md — desde ese momento la prioridad de la idea tiene fecha; (2) escribir el prerregistro 01; (3) filmar; (4) extraer; (5) correr; (6) pruebas nulas; (7) registrar el resultado, sea cual sea.

---

## 4. PROMPT DE ARRANQUE PARA UN FUTURO MODELO DE IA

Copiar y pegar esto para continuar el proyecto con cualquier asistente:

> Lee el archivo CIMIENTOS.md completo. Tu rol es ORQUESTADOR, no descubridor (Regla 3): escribes código, organizas datos y documentas, pero jamás sugieres qué ley física deberían encontrar los datos ni interpretas resultados usando física humana antes de la validación. Ayúdame a ejecutar la fase indicada respetando las 10 reglas. Si alguna acción viola una regla, deténte y dímelo.

---

## 5. HONESTIDAD INTELECTUAL (leer antes de contar esto a alguien)

- Las reglas se apoyan en ideas existentes: la filosofía de la ciencia ya sabía que la observación está cargada de teoría (Duhem, Hanson, Kuhn), y MDL, prerregistro y validación cruzada son estándar en sus campos. **El aporte es la combinación como protocolo operativo** para descubrimiento automático no contaminado — eso, hasta donde se pudo verificar en julio de 2026, no está publicado como tal.
- La probabilidad de que este proyecto resuelva las paradojas de la física es baja. La probabilidad de que enseñe muchísimo, produzca resultados publicables en los peldaños intermedios, y posicione a su autor en un campo que tiene tres años de vida, es alta. Los legados se construyen así.
