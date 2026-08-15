# PLAN MAESTRO 01 — APLICARLO TODO: motor, ecuaciones, mundo y revalidación completa
**11 de agosto de 2026. Encargo del director: aplicar todo lo que soluciona las cosas — el mundo,
las ecuaciones nuevas, lo que encontramos de los modelos — y decir de antemano cada paso y cada
validación.**
**Este documento es un PLAN. No contiene ni un solo resultado. Ningún número de aquí es evidencia
de nada.**

---

## 0. LO QUE ACEPTO Y LA ÚNICA CONDICIÓN QUE PONGO

**Acepto el alcance entero: todo.** Las seis fases de abajo cubren los 24 problemas de la lista,
las cinco ecuaciones de la investigación y el mundo persistente. No dejo nada fuera.

**Y pongo una sola condición, que es de método y no de gusto: EL ORDEN NO ES NEGOCIABLE.**

La razón es concreta, no burocrática: **cada fase se valida con los instrumentos de la fase
anterior.** Si construimos el mundo antes de arreglar el motor, mediremos un mundo nuevo con un
instrumento que sabemos roto, y dentro de dos semanas no sabremos si lo que falla es el mundo o
la vara. **Hacerlo todo a la vez es exactamente el mecanismo que produjo los 24 problemas: cosas
que llevaban meses corriendo sin examen.**

**Aplicarlo todo, sí. Aplicarlo todo el mismo día, no.**

---

## 1. LA REGLA QUE PROTEGE EL PASADO — `sindy3.py` NO SE TOCA

**Decisión de diseño, y es la más importante del plan.** El motor arreglado será un **archivo
nuevo, `sindy4.py`**. `sindy3.py` se queda intacto para siempre.

**Por qué:**
- **El sello de LA PUERTA muere si el archivo cambia** (`metodo.py`, línea 218: *"pasó la puerta
  el ... pero el archivo CAMBIÓ"*). Editar `sindy3` mataría su sello y el de todo lo que depende
  de él.
- **Las 67 corridas ya hechas se hicieron con `sindy3`.** Si lo editamos, **dejan de ser
  reproducibles** y perdemos el año de trazabilidad — que es lo único caro que tenemos.
- **Y la comparación exige los dos.** La Fase 2 consiste precisamente en correr lo mismo con los
  dos motores y comparar. Con uno solo no hay comparación posible.

**Consecuencia:** al terminar tendremos dos motores vivos y **la obligación de decir con cuál se
midió cada cosa.** Un guardián nuevo lo vigilará.

---

# FASE 1 — EL MOTOR. `sindy4.py` y el prerregistro 47

## 1.1 Qué se construye — cuatro cambios, ni uno más
| # | cambio | qué defecto ataca | de dónde sale |
|---|---|---|---|
| 1 | **Corte ADIMENSIONAL**: se sustituye `\|W\| < 0.05` por la **Presencia de Coeficiente** `CP = √m·μ(ξ)/σ(ξ)` — media del peso entre remuestreos dividida por su dispersión. Sin unidades ⇒ **no cambia con la escala**. | agujeros de escala (falsos negativos) | STCV, arXiv 2603.05201 (2026) |
| 2 | **Adimensionalización previa**: las columnas del diccionario se normalizan por **las escalas de los propios datos** antes de ajustar, y los pesos se devuelven a unidades al final. | agujeros de escala | Buckingham Π, Nature Comput. Sci. 2022 |
| 3 | **Guarda de condición**: si el número de condición de la matriz supera el tope, **el motor calla**. | alucinación (falsos positivos) | numérica estándar |
| 4 | **Poder predictivo fuera de muestra (Regla 12 para el motor)**: se ajusta en unas ventanas y se mide en otras que no vio; si la ley no gana a la línea base tonta, **no se declara ley**. | alucinación | nuestra propia Regla 12 |

**El tope de condición se declara AQUÍ, antes de correr, y con su razón:** `10⁶`. La aritmética de
doble precisión lleva ~16 cifras significativas; con condición 10⁶ se conservan 10 cifras buenas.
**Declaro también lo que ya vi** (sonda exploratoria del DIAGNOSTICO-MOTOR-01): el oscilador sano
da 10.5 y la señal degenerada 7·10⁹. **Esas dos observaciones no son evidencia de este estudio** y
la semilla 7 queda quemada.

**Lo que NO se cambia:** la forma débil (integrar en vez de derivar) se queda como está — es
correcta y es la razón de existir del módulo. **No se amplía el diccionario en esta fase.** Un
cambio a la vez, o no sabremos cuál funcionó.

## 1.2 Cómo se valida que los errores YA NO EXISTEN — **prerregistro 47, congelado antes de correr**

**Semillas nuevas: `43, 47, 53, 59, 61`.** Quedan quemadas todas las anteriores (2,3,5,7,11 del
arreglo del módulo; 23,29,31,37,41 del prereg-46; 7 de la sonda).

| criterio congelado | pide | si falla |
|---|---|---|
| **A — se cerraron los agujeros** | Barrido idéntico al prereg-46 (25 escalas × 5 semillas × 2 sistemas): **exactamente UN tramo contiguo en los dos sistemas**, cubriendo **≥5 de las 6 décadas**. | El arreglo del umbral **no era la causa**, y se escribe con esas palabras. |
| **B — se acabó la alucinación** | Sobre señal casi constante: **0 leyes declaradas en 25 de 25 casos**. Una sola ley = fallo. | La guarda de condición no basta; hace falta el criterio de compresión (Fase 5). |
| **C — NO ROMPIMOS LO QUE FUNCIONABA** | `sindy4` recupera la ley en **todos** los casos en que `sindy3` la recuperaba a escala ×1: oscilador limpio, oscilador con sensor ruidoso, y **calla** en barajado y ruido puro. | **`sindy4` se descarta entero.** Un motor que arregla la escala y deja de ver leyes es peor que el que teníamos. |
| **D — el arreglo es del motor, no del barrido** | Los mismos criterios A y B, corridos con `sindy3` sobre **las mismas semillas nuevas**, deben reproducir los defectos viejos. | Si `sindy3` sale limpio con semillas nuevas, **el defecto era de las semillas y no del motor** — y el INFORME-55 estaría mal. Se escribiría así. |

**El criterio D es el que más me interesa y es el que me deja peor si sale mal.** Sin él, un
arreglo que no arregla nada podría aprobar solo porque las semillas nuevas son más fáciles.

**Cuándo se abandona (Regla 13, con número):** si falla **C**, `sindy4` se descarta y no hay
segunda versión parcheada para pasar. Si falla **A** pero pasan B y C, se publica que el umbral no
era la causa y la fase 1 queda abierta.

## 1.3 La Regla 31 del instrumento — y el error que NO vuelvo a cometer
La Regla 31 examina **mi procedimiento de medida**, nunca al motor. Lo escribo aquí porque lo hice
mal **dos veces el mismo día** (prereg-45 y prereg-44):
- **Prohibido** meter en la Regla 31 pruebas sobre el comportamiento del motor. Eso es el
  **resultado** del estudio.
- **Control positivo, control negativo, respuesta al ruido, y que la medida distinga escalas.**
- **Relaciones metamórficas con base distinta de cero.** Me mordió tres veces: multiplicar 0 por 2
  da 0 y la puerta mide "×1.000" sin probar nada.
- **Ninguna relación que no se sepa a priori.** Me mordió dos veces.

## 1.4 La puerta y el sello
`sindy4.py` pasa **los siete pasos** de `metodo.py` (0 manifiesto · 1 fórmulas · 2 arranque al
final · 2 sin pisar nombres · 3 ficha de sanidad · 4 regla 31 · 7 escritura limpia) y queda
**sellado con el hash del archivo**. Desde ese momento cualquier edición mata el sello.

---

# FASE 2 — LA REVISIÓN DE LAS 67 CORRIDAS. Prerregistro 48

## 2.1 Qué se hace
**Paso 0, mecánico:** inventario de qué corridas llaman de verdad al motor. No son las 67; hay que
contarlo antes de prometer nada.

**Paso 1:** rehacer cada una de esas corridas con `sindy4` y comparar veredictos, uno a uno.

## 2.2 Qué se congela ANTES de mirar, y por qué esto es delicado
Este estudio **puede tumbar hallazgos nuestros**. Por eso lo que se congela no es un umbral: es
**una obligación de publicación.**

| lo que puede pasar | qué se hace, decidido antes |
|---|---|
| Un **"no concluyente"** pasa a **hallazgo** | Se publica. Es lo esperado: los agujeros producen falsos negativos. |
| Un **hallazgo** pasa a **"no concluyente"** | **Se publica igual de fuerte, y con un acta propia.** Es el caso que nos deja mal y es el más importante de todos. |
| Un hallazgo **cambia de contenido** | Se publica el antes y el después, sin borrar el anterior. |
| Nada cambia | Se publica que nada cambió — y entonces los agujeros **no tocaron nuestros resultados**, que es información valiosa. |

**Ningún acta antigua se edita ni se borra.** Se añade un acta nueva que la corrige. La historia
del error se conserva; ésa es la Regla del proyecto y no la toco.

---

# FASE 3 — LA MENTE: contrato de estimadores y la cadena G14→G8. Prerregistro 49

## 3.1 El contrato (responde a "¿son órganos o funciones?")
Cada módulo declara **qué es**: `SENTIDO` · `ACTUADOR` · `ESTIMADOR` · `POLÍTICA`. Y:

> **Todo ESTIMADOR publica el rango válido de su número, y quien lo consume está obligado a
> verificarlo.**

Eso es exactamente lo que faltó cuando G14 le entregó a G8 una incertidumbre inflada y G8 se la
creyó. **Guardián nuevo `contratos.py`: BLOQUEA si un estimador no declara rango o si un consumidor
no lo verifica.**

## 3.2 Las dos reparaciones, con ecuación nueva
- **G14 `incertidumbre.py`** — hoy su ignorancia "curable" es `σ/√n`, que sube igual con pocos
  datos que con mucho ruido. Se separa en dos números distintos: **ignorancia por falta de datos**
  e **irreducible por ruido**, que es lo que confundía.
- **G8 `atencion.py` + G2 `curiosidad2.py`** — entra el **EMPOWERMENT** (idea D.4 de la
  investigación): *prefiere los estados desde los que tus acciones tienen más efecto sobre tu
  futuro*. Y se quita el `piso_poder=0.05` que hacía puntuar 0.05 a una región de poder cero.

**Por qué esto arregla el televisor por diseño y no por parche:** un televisor con ruido tiene
mucha sorpresa pero **empowerment exactamente cero** — no puedes hacer nada con él. **Una
motivación construida sobre empowerment no puede ser secuestrada por una pared que parpadea.**
`poder.py` ya va en esta dirección y está sellado.

## 3.3 Validación — criterios congelados antes de tocar nada
1. **La prueba del televisor**, la misma que reprobó: con la epistémica del televisor ×20, **el
   televisor se lleva menos de 2 de 10 y la región buena más de 7**. (Hoy: 7.036 el televisor.)
2. **Relación metamórfica, sabida a priori:** *subir el ruido del televisor NO puede subir su
   puntuación de atención.* Hoy la sube; ésa es la definición del defecto.
3. **Señuelo:** una región con **poder cero** debe puntuar **cero**, no 0.05.
4. **No romper lo que servía:** con una región de verdad prometedora, la atención debe seguir
   yendo allí.
5. **Ficha de sanidad + puerta + sello** para los tres módulos tocados.

---

# FASE 4 — EL MUNDO PERSISTENTE. `mundo.py` y prerregistro 50

## 4.1 Qué se construye
1. **El mundo persiste** entre estudios: un solo lugar con estado, no una escena desechable.
2. **El cuerpo alcanza el mundo** — y esto se convierte en **chequeo BLOQUEANTE antes de cualquier
   estudio encarnado**: si la intersección entre el alcance medido del cuerpo y los objetos del
   mundo está vacía, **no se corre nada**. El fallo del brazo (punta a z=0.380, objetos a z≈0.20)
   se vuelve imposible de repetir.
3. **La única moneda es la predicción**: Diego declara qué observará dentro de N pasos, el mundo
   ocurre, se compara. **El verificador es el mundo, no nosotros.**
4. **La dificultad sube sola**, estilo POET: sube cuando Diego predice bien, baja cuando falla —
   medido con **su error de predicción**, nunca con criterios nuestros.

## 4.2 Las dos trampas de la Regla 27, convertidas en guardián
Esto es lo que más me preocupa de toda la fase, así que se mecaniza:

- **Guardián de etiquetas:** el vector de observación de Diego **no puede contener ningún nombre
  humano** — ni "masa", ni "kg", ni "velocidad". Columnas sin nombre y sin unidad. **La etiqueta
  es la herencia.** BLOQUEA.
- **Guardián de recompensa:** la única señal admisible es **error de predicción de sus propias
  observaciones futuras**. Cualquier recompensa que dependa de un criterio nuestro sobre qué es
  "resolver" **BLOQUEA**. Es la fuga más elegante y más difícil de ver: no le decimos *F=ma*, le
  decimos *"te premio cuando aciertes lo que yo, que sé F=ma, considero acertar"*.

## 4.3 Validación
1. **Geometría medida**, no supuesta: se mide el alcance del cuerpo y los objetos, y se comprueba
   que se cruzan. Es el chequeo que faltó en el gimnasio viejo.
2. **Nulo del mundo muerto:** en un mundo donde las acciones no hacen nada, la puntuación debe ser
   **cero**. Si un mundo muerto puntúa, la medida no mide interacción.
3. **Señuelo del predictor al azar:** un Diego que predice aleatorio debe quedar **a nivel de
   ruido**. Si puntúa, la moneda está rota.
4. **El mundo persiste de verdad:** el estado tras N pasos debe depender de lo que pasó antes.
   Suena obvio; es exactamente el tipo de cosa que nadie comprueba y luego falla.
5. **Metamorfismo con base no nula:** más pasos de interacción ⇒ más contacto con el mundo.

---

# FASE 5 — EL SEGUNDO MOTOR. Prerregistros 51 y 52

## 5.1 Requisito previo, y va primero — **arreglar la regla de oro del panel**
El panel de jueces **corona un ganador aunque todos compitan a nivel de ruido** (problema nº9). Si
metemos un segundo motor al torneo antes de arreglar eso, **el torneo dará campeón pase lo que
pase.** Se le pone un **piso absoluto**: si nadie supera la vara calibrada (obediencia a latentes
+0.412 frente a ruido puro −0.0002), **el veredicto es "ninguno", no "el mejor de los malos".**

## 5.2 El motor nuevo
No compite por ser mejor: **compite por fallar de otra manera.** Dos candidatos, y se elige uno:
- **Invariantes (Noether, idea D.2):** buscar **cantidades conservadas** en vez de ecuaciones. Más
  barato, detectable sin saber física, y **descubrible mirando, sin intervenir**.
- **Compresión (MDL, idea D.3):** la mejor teoría es la que **más comprime** los datos, contando
  el tamaño de la teoría más el de sus errores. Convierte nuestra Regla 6 —"prefiere lo simple",
  hoy un juicio sin número— en **bits medibles**, y habría matado la alucinación de doce términos
  por sí sola.

## 5.3 Y la pregunta de fondo que esta fase abre — la jaula del diccionario
`sindy4` seguirá pudiendo expresar solo mezclas de `1, x, v, x², xv, v²`. **Si la ley del mundo no
está ahí, no la verá ni con el umbral perfecto — y dirá "no vi nada" en vez de "no sé mirar eso".**
El segundo motor es la única forma de detectar esa jaula desde fuera: **si encuentra estructura
donde `sindy4` no ve nada, la jaula existe y está medida.**

## 5.4 Validación
Torneo con **vara calibrada, panel con piso absoluto y semillas nuevas**. Y el criterio que
importa: **no "cuál gana", sino en qué casos discrepan.** Dos motores que siempre coinciden no
aportan nada; el valor está en el desacuerdo.

---

# FASE 6 — REVALIDAR TODO EL CÓDIGO, de pies a cabeza

## 6.1 Los 8 órganos sin examinar
`cerebro`, `curiosidad2`, `descubrir`, `gimnasio`, `interocepcion`, `memoria`, `percepcion`,
`percepcion2` — ficha de sanidad + los siete pasos de la puerta + sello.
**Expectativa declarada, para que se me pueda descontar: de 6 examinados reprobaron 3. Espero que
de estos 8 reprueben entre 2 y 5.** Si aprueban los 8, diré que la muestra anterior fue mala
suerte y lo escribiré con esas palabras.

## 6.2 Los guardianes de los guardianes nuevos
**Todo guardián nuevo (`contratos.py`, el de etiquetas, el de recompensa, el de geometría) necesita
su prueba de daño** en `guardianes_de_guardianes.py`: se rompe el repositorio a propósito de esa
forma concreta y se comprueba que el guardián lo caza. **Un guardián sin prueba de daño es
decoración**, y ya nos pasó con una prueba que buscaba el literal "32 reglas" y se saltaba sola.

## 6.3 La limpieza pendiente
- **`BOLETA.json` está rancia** (dice 49 informes y 43 prerregistros; hay 57 y 47) y **ningún
  guardián vigila esos campos**. Se regenera y se le añade el chequeo de frescura, igual que se
  hizo con la tabla de reglas.
- **Rediseñar el criterio 4 del prerregistro-41**, que era tautológico. Va en prerregistro nuevo,
  no en una edición del viejo.
- **Volver a llenar la cola** para que el latido de la nube tenga trabajo (hoy: 67 hechas, 0
  pendientes, latiendo en vacío).

## 6.4 El cierre
Los **cuatro guardianes** + la **meta-auditoría** (los 9 daños) + el **auditor de actas** sobre
todas las actas nuevas, en rama y en main, con todo empujado a GitHub.

---

# LAS TRES CAPAS DE VALIDACIÓN, que es lo que el director pidió explícitamente

**Capa 1 — ¿los errores viejos ya no existen?**
Criterios congelados **antes** de correr, **semillas nuevas**, y un **criterio D** que exige que el
motor viejo siga fallando con esas mismas semillas. Sin eso, un arreglo que no arregla nada puede
aprobar por suerte.

**Capa 2 — ¿lo nuevo funciona de verdad?**
Cada pieza nueva pasa: **control positivo** (¿encuentra lo que está?), **control negativo** (¿calla
cuando no hay nada?), **señuelo** (¿se deja engañar por algo que parece pero no es?), **relación
metamórfica con base no nula** (¿cambia como debe al cambiar el mundo?), **fuera de muestra**
(¿funciona en datos que no vio?) y **línea base tonta** (¿le gana a lo trivial?).

**Capa 3 — ¿todo el código sigue siendo correcto?**
Los cuatro guardianes + la meta-auditoría con daño real + la ficha de sanidad sobre los 15 órganos
+ el auditor de actas. **Y la prueba de daño obligatoria para cada guardián nuevo.**

---

# LO QUE **NO** PROMETO
- **No prometo que ninguna de las seis fases salga bien.** Cuatro de los criterios de arriba están
  escritos para dejarme mal si el arreglo no funciona, y ésa es su función.
- **No prometo plazos cortos.** La Fase 1 son días; las Fases 4 y 5 son semanas. Prometer un fin
  de semana sería la primera mentira del plan.
- **No prometo que el mundo nuevo enseñe física.** Es un lugar donde medir, no una garantía.
- **No se toca ninguna regla, ningún umbral ya congelado ni ningún veredicto ya emitido.**

# LO QUE SIGUE RESERVADO AL DIRECTOR, y este plan no toca
1. **Regla 16** — el repositorio sigue privado.
2. **Regla 22** — la revisión de doble uso (0 de 7 nodos). No es mecanizable ni delegable.
3. **Regla 19 nivel 2** — el experimento físico propio. **Es la deuda estructural del proyecto**
   (0 de 4 nodos) y ninguna fase de este plan la salda: todo esto sigue ocurriendo dentro de
   nuestro código.
4. **Cambiar las reglas** y **mover un umbral después de ver los datos.**

# LA PREGUNTA QUE ABRE (Regla 18)
> **Si las seis fases salen bien, ¿qué sabremos del universo?** Nada. Sabremos que nuestros
> instrumentos son honestos y que nuestro ente aprende en nuestro simulador. **El salto al nivel 2
> no es una fase más: es un cambio de naturaleza**, y sigue esperando.
