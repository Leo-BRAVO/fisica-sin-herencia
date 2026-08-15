# Prerregistro 50 — EL MUNDO PERSISTENTE: ¿puede Diego vivir en un lugar en vez de en escenas? — 11 de agosto de 2026
**Fase 4 del PLAN MAESTRO 01. Peldaño (Regla 9): Fase 1 — propiedad de nuestro código, no del
universo.**
**Estado: FIRMADO antes de escribir `mundo.py`.**

---

## 0. DE DÓNDE SALE ESTO
Del encargo del director: *"por qué no creamos un mundo virtual, un videojuego donde se interactúe
con Diego y realmente él pueda ver todo... cuando vea algo va a poder ver números y tratar de
entender todo, pero también va a poder moverse en el mundo que creemos, y le vamos a dar mejoras
por cada prueba que resuelva"*.

**La idea es correcta y responde a un defecto medido:** hoy **Diego no tiene mundo, tiene escenas.**
Cada estudio monta su escenita, la mide y la tira. Nada persiste. Y el INFORME-57 encontró la
consecuencia más cruda: **su brazo no alcanza nada** — la punta baja como mucho a **0.380** y los
objetos están a **0.20**. Nadie comprobó nunca que el cuerpo llegara al mundo.

## 1. LAS DOS TRAMPAS, que este prerregistro existe para cerrar

### 1.1 «Mejoras por cada prueba que resuelva» rompe la Regla 27
Si **nosotros** decidimos qué cuenta como *resuelto*, **le metemos nuestra física por la función de
recompensa.** No le decimos *F=ma*; le decimos *"te premio cuando aciertes lo que yo, que sé F=ma,
considero acertar"*. **Es herencia por la puerta de atrás, con las apariencias intactas.**

**La salida: que el verificador sea el mundo, no nosotros.** La única señal admisible es
**¿predijo bien lo que iba a pasar?** Diego declara qué observará dentro de N pasos, el mundo
ocurre, se compara. **Nadie necesita saber física para puntuar eso**, y es la misma estructura que
hizo funcionar a DeepSeek-R1-Zero: recompensa por corrección verificable, sin imponer el proceso.

### 1.2 «Va a poder ver números» depende enteramente de qué números
- **Admisible:** lecturas crudas de sus sensores, **sin nombre y sin unidad**. Un vector.
- **Prohibido:** cualquier número con etiqueta humana — *masa*, *kg*, *velocidad*, *gravedad*.
  **La etiqueta ES la herencia.** Los kilogramos son un descubrimiento humano, no un hecho del
  mundo.

## 2. LA PREGUNTA
> ¿Se puede construir un mundo que **persista**, que el cuerpo de Diego **alcance**, y cuya única
> moneda sea **la predicción de sus propias observaciones** — sin que ninguna etiqueta humana ni
> ningún criterio nuestro de "resuelto" entre en él?

## 3. LO QUE SE CONSTRUYE
1. **`mundo.py`** — un lugar con **estado que sobrevive entre rondas**, no una escena desechable.
2. **Chequeo de alcance BLOQUEANTE**: si la intersección entre el alcance medido del cuerpo y los
   objetos del mundo está vacía, **no se corre nada**. El fallo del INFORME-57 se vuelve imposible.
3. **La moneda de la predicción**: Diego declara observaciones futuras; el mundo arbitra.
4. **Dos guardianes nuevos de la Regla 27**, y son la parte que más me importa:
   - **de ETIQUETAS**: ninguna palabra humana de física puede aparecer en lo que Diego observa.
   - **de RECOMPENSA**: la señal solo puede depender de su propio error de predicción. Cualquier
     término que dependa de un criterio nuestro **BLOQUEA**.

## 4. LA LÍNEA BASE TONTA (Reglas 11 y 12)
**Predecir que nada cambia** — *"dentro de N pasos veré exactamente lo que veo ahora"*. Es la
persistencia, el predictor más tonto que existe. **Un mundo donde ese predictor puntúa igual que
uno que modela no está midiendo comprensión de nada.**

## 5. LOS CRITERIOS CONGELADOS

| | criterio | pide |
|---|---|---|
| **A** | **el cuerpo alcanza el mundo** | La intersección entre el alcance medido y la posición de los objetos **no está vacía**, y se comprueba **antes** de cualquier medida |
| **B** | **el mundo persiste de verdad** | El estado tras N pasos **depende de lo ocurrido antes**: dos historias distintas dan estados distintos. Suena obvio y es justo lo que nadie comprueba |
| **C** | **la moneda discrimina** | Un predictor que usa el estado del mundo **le gana** a la línea base tonta de persistencia, con una diferencia declarada de antemano: **≥0.10 de error relativo** |
| **D** | **nulo del mundo muerto** | En un mundo donde **las acciones no hacen nada**, la ventaja sobre la línea base tonta cae a **≤0.02**. Si un mundo muerto puntuase, la moneda no mide interacción |
| **E** | **señuelo del predictor al azar** | Un predictor **aleatorio** queda **por debajo** de la línea base tonta. Si puntuara, la moneda está rota |
| **F** | **Regla 27, etiquetas** | El vector de observación de Diego **no contiene ninguna palabra humana de física**, comprobado por guardián |
| **G** | **Regla 27, recompensa** | La señal depende **solo** del error de predicción propio. Un intento de meter un criterio nuestro **debe bloquear**, y se prueba **inyectándolo a propósito** |

## 6. REGLA 31 — sobre MI PROCEDIMIENTO, los dos lados, y no sobre el mundo
- **Control positivo (debe aprobar):** la geometría se **mide**, no se supone, y el objeto se
  coloca **dentro del alcance medido**. Si no, se detiene.
- **Señuelo / control negativo (debe fallar):** los dos guardianes de la Regla 27 se prueban
  **inyectando la violación**: una etiqueta humana en la observación y un término de recompensa
  ajeno. **Si no saltan, son decoración.**
- **Base distinta de cero** en toda relación metamórfica. Quinta vez que lo escribo este mes.
- **No se mete aquí ninguna prueba sobre lo que Diego aprenda.** Eso es resultado, no requisito de
  entrada — el error que dejó NULO al prerregistro 45.

## 7. CUÁNDO SE ABANDONA (Regla 13, con número)
- Si falla **A**, **se detiene**: un mundo que el cuerpo no alcanza no es un mundo, y ya cometimos
  ese error una vez.
- Si falla **D** o **E**, **se detiene**: la moneda no mide lo que dice medir.
- Si falla **F** o **G**, **se descarta el mundo entero**. No hay versión "casi limpia" de la
  Regla 27: **un mundo con una fuga de herencia es peor que no tener mundo.**
- Si sale **NO CONCLUYENTE**, no hay segunda versión de este estudio.

## 8. LO QUE ESTE ESTUDIO **NO** PUEDE AFIRMAR
- **Nada del universo.**
- **No afirma que Diego aprenda física en él.** Construye **un lugar donde medir**, no una
  garantía. Lo que aprenda —si aprende— va en prerregistros posteriores.
- **No implementa la dificultad autogenerada** (el currículo estilo POET). Va aparte: mezclarla
  aquí impediría saber si un fallo es del mundo o del currículo.
- **No toca el gimnasio actual** ni ninguna corrida ya hecha en él.

## 9. FIRMA
Avanza por **quórum adversarial**: los dos guardianes de la Regla 27 se prueban inyectando la
violación que deben cazar, el criterio D está escrito para que un mundo falso no pueda aprobar, y
**F y G mandan descartar el mundo entero**. Revocable con una palabra del director.
