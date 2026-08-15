# Prerregistro 47 — ¿ARREGLA EL CORTE ADIMENSIONAL LOS DOS DEFECTOS DEL MOTOR? — 11 de agosto de 2026
**Fase 1 de la Plan Maestro 01. Peldaño (Regla 9): Fase 1 — propiedad de nuestro código, no del
universo.**
**Estado: FIRMADO antes de escribir una sola línea de `sindy4.py` que produzca datos.**

---

## 0. QUÉ SE ARREGLA Y POR QUÉ SE CREE QUE ESO ES LA CAUSA
El INFORME-55 dejó abierta la pregunta *"¿qué umbral interno del motor se apaga alrededor de
10⁻¹·⁵?"*. El `DIAGNOSTICO-MOTOR-01` la responde: **`umbral=0.05` en la línea 74 de `sindy3.py`**,
un corte por magnitud aplicado a pesos que bajo un cambio de escala **s** se multiplican por **s**
(término constante), por **1** (lineales) y por **1/s** (cuadráticos). **Un solo número comparado
contra tres escalas que se mueven en direcciones opuestas.**

**Eso es una HIPÓTESIS, no un hecho.** Este estudio existe para ponerla a prueba, incluida la
posibilidad de que sea falsa.

## 0.1 LO QUE YA VI, declarado antes de correr (y las semillas que quemo)
Dos sondas **exploratorias** del `DIAGNOSTICO-MOTOR-01`, que **no son evidencia de este estudio**:
- A escala 10⁻³, **7 de 12** pesos del ajuste crudo superan 0.05 en vez de 3, y el motor se cae.
- Sobre señal casi constante el número de condición de la matriz es **7.06 × 10⁹** frente a
  **10.5** del oscilador sano, y el motor declara 12 términos con probabilidad 1.000.

**Semillas quemadas y prohibidas aquí:** `2, 3, 5, 7, 11` (arreglo del módulo de escala),
`23, 29, 31, 37, 41` (prerregistro 46) y `7` (las sondas de arriba).
**Este estudio corre sobre cinco semillas nuevas: `47, 53, 59, 61, 67`**, declaradas aquí antes de
tocarlas.

> ### ENMIENDA 4 — la semilla 43 queda QUEMADA y se sustituye por la 67. 11-ago-2026, antes de correr
> **La lista original de este prerregistro era `43, 47, 53, 59, 61`. Miré la 43 y por eso la
> retiro.**
>
> **Qué miré y por qué:** al construir el módulo, LA PUERTA reprobó la relación metamórfica
> midiendo `×1.000`. Para saber si era la trampa de la base cero (que ya me tumbó tres relaciones
> en un día) abrí el caso concreto: **semilla 43, oscilador, escala ×1, con los dos motores.**
>
> **Qué vi, dicho entero para que se me pueda descontar:** con ruido base, `sindy3` declara
> `dx/dt = 0.993·v` y `dv/dt = −0.89·x`, y `sindy4` declara lo mismo **más el término de
> amortiguamiento** `−0.041·v`, que es el que la ley verdadera tiene en `−0.05` y **`sindy3` no
> encuentra**. Con ruido ×200, `sindy3` calla y `sindy4` declara la ley con margen fuera de
> muestra de 0.71 y 0.74.
>
> **Esas observaciones NO son evidencia de este estudio.** Salieron de diagnosticar un fallo de la
> puerta, sobre una semilla que ahora queda fuera. **La sustituye la `67`**, que no se ha tocado.
>
> **Y no se toca ningún criterio.** A, B, C y D siguen exactamente como estaban firmados.

**Y declaro mi expectativa, para que se me pueda descontar:** espero que **A y B pasen y C pase**.
Si el criterio A falla, mi diagnóstico del umbral era incorrecto y lo escribiré con esas palabras.

## 1. LA PREGUNTA
> Sustituyendo el corte por magnitud por un criterio **adimensional**, añadiendo una **guarda de
> condición** y una prueba de **poder predictivo fuera de muestra**: ¿desaparecen los agujeros de
> escala **sin perder** las leyes que el motor sí encontraba?

## 2. LOS CUATRO CAMBIOS, congelados — ni uno más
Se construye un archivo **NUEVO**, `codigo/sindy4.py`. **`sindy3.py` no se edita**: editarlo
mataría su sello y dejaría irreproducibles las 67 corridas ya hechas.

1. **Corte adimensional**: en vez de `|W| < 0.05`, la **Presencia de Coeficiente**
   `CP = |μ(ξ)| / σ(ξ)` sobre los remuestreos del bootstrap. Es una razón **sin unidades**, así
   que **no cambia si el mundo se mide en otra escala**. Piso de CP congelado: **3.0** — un peso
   solo entra si está a **tres desviaciones o más de cero**.

   > ### ENMIENDA 1, escrita ANTES de correr y antes de que exista `sindy4.py` — 11-ago-2026
   > **La primera versión de este prerregistro escribió la fórmula como `CP = √m · μ/σ`**, copiada
   > tal cual del trabajo que la propone (STCV, arXiv 2603.05201). **Al ir a implementarla vi que
   > ese factor `√m` no aplica a nuestro estimador y la corrijo aquí, en abierto, antes de tener
   > un solo dato.**
   >
   > **La razón:** en el trabajo original, `σ` es la dispersión *de una muestra* de tamaño `m`, y
   > `√m` convierte esa dispersión en el error de la media. **En un bootstrap, la dispersión entre
   > remuestreos YA ES el error estándar** — no hay que dividirla otra vez. Con nuestros 200
   > remuestreos, `√m = 14.1`, así que dejar el factor **multiplicaría por catorce la puntuación de
   > todos los términos, incluidos los falsos**, y un piso de 3.0 dejaría pasar cualquier cosa con
   > una razón real de 0.21.
   >
   > **Qué cambia y qué no:** cambia el factor constante, **no cambia el criterio ni lo relaja** —
   > al contrario, lo endurece. Y **no cambia lo que importa: sigue siendo una razón sin unidades**,
   > que es la propiedad por la que se eligió. **Se enmienda ahora porque implementar a sabiendas
   > una fórmula que creo equivocada sería peor que enmendarla a la vista.**
2. **Adimensionalización previa**: las columnas del diccionario se normalizan por las escalas de
   **los propios datos** antes de ajustar, y los pesos se devuelven a unidades al final. **No se
   usan unidades humanas** — eso sería herencia; se usan las escalas empíricas de la serie.
   **Piso de peso adimensional congelado: `|W_s| ≥ 0.01`.**

   > ### ENMIENDA 3, escrita ANTES de correr el estudio — 11-ago-2026
   > **La puerta reprobó `sindy4` en su control positivo antes de que existiera un solo dato del
   > estudio, y el motivo obliga a declarar un número que faltaba.**
   >
   > **Lo que pasó:** sobre el oscilador **sin ruido**, CP no discrimina. La razón es que **CP mide
   > consistencia, no relevancia**: el sesgo de discretización del integrador —un término de
   > magnitud 0.0059 sobre 1.0— es diminuto pero **perfectamente consistente entre remuestreos**,
   > así que su CP sale 7·10¹², indistinguible del de un término verdadero. **Un criterio de
   > consistencia por sí solo no puede separar "pequeño y sistemático" de "grande y real".**
   >
   > **Lo que se añade:** el piso de magnitud **en el espacio adimensional**, que el cambio 2 ya
   > declaraba construir y que no llegué a usar para decidir. Como las columnas del diccionario y
   > el objetivo están normalizados a norma unidad, **`|W_s|` es la fracción de la magnitud del
   > objetivo que explica ese término — una cantidad sin unidades.** Se congela en **0.01**: *un
   > término que aporta menos del 1% no es un término de la ley.*
   >
   > **Por qué esto NO reintroduce el defecto que arreglamos:** el `0.05` de `sindy3` cortaba
   > **pesos con unidades**, y por eso se movía con la escala. Este piso corta **una fracción**, y
   > una fracción no cambia si el mundo se mide en otra escala. Es la diferencia entre *"pesa menos
   > de 50 gramos"* y *"es menos del 1% del total"*.
   >
   > **Qué vi antes de fijar el 0.01, dicho entero:** los pesos adimensionales del control positivo
   > —el juguete de `sindy3`, semilla 7, **ya quemada**— salen 1.001, 1.002 y 0.162 para los
   > términos verdaderos, 0.0059 para el sesgo de discretización y ≤0.0046 para el ruido. **El 0.01
   > es el orden de magnitud que separa esos dos grupos, y lo digo en vez de presentarlo como
   > elegido a priori.** No he mirado ni un dato del barrido de 25 escalas ni de las semillas
   > 43, 47, 53, 59, 61: el estudio no ha corrido.
   >
   > **Y esto hace el criterio A más difícil, no más fácil:** un piso de magnitud es exactamente
   > la clase de número que podría reintroducir dependencia de la escala si estuviera mal puesto.
   > Si el barrido sigue saliendo con agujeros, este piso será el primer sospechoso.
3. **Guarda de condición**: si el número de condición de la matriz supera **10⁶**, el motor
   **calla**. Razón declarada, y es aritmética y no empírica: la doble precisión lleva ~16 cifras
   significativas, y con condición 10⁶ se conservan 10 cifras buenas.
4. **Poder predictivo fuera de muestra**: se ajusta en el 70% de las ventanas y se mide en el 30%
   restante. **Si la ley no supera a la línea base tonta en las ventanas que no vio, no se declara
   ley.**

   > ### ENMIENDA 2, escrita ANTES de correr — 11-ago-2026
   > La versión firmada decía *"supera a la línea base tonta"* **sin número**, y sin número no es
   > un criterio. Se fija aquí, antes de existir el código: **la línea base tonta es el modelo que
   > solo usa el término constante** (*"la derivada no depende de nada"*), y la ley debe superarlo
   > en **R² ≥ +0.10** en las ventanas que no vio, **en cada una de las dos ecuaciones**.
   >
   > Se elige ese rival y no la persistencia porque es el que **discrimina justo el defecto 2**:
   > sobre una señal casi constante, el modelo constante lo explica todo, así que **ninguna ley
   > puede ganarle por 0.10 y el motor se ve obligado a callar.**

**Lo que NO se cambia:** la forma débil (integrar en vez de derivar) se queda intacta, y **el
diccionario sigue teniendo las mismas seis piezas**. Un cambio a la vez, o no sabremos cuál actuó.

## 3. LA LÍNEA BASE TONTA (Regla 11 y 12)
Dos, según el criterio:
- **Para el barrido de escala:** el ideal es *"el motor ve la ley siempre que exista, sin importar
  las unidades"* — **25 de 25 escalas, en un solo tramo**. Se reporta la fracción de escalas en que
  ve y **cuántos tramos contiguos** hacen falta para describirla.
- **Para el poder predictivo dentro del motor:** la **línea base tonta** es *"el estado siguiente
  es igual al actual"* (persistencia). Una ley que no le gana a eso **no es una ley**.

## 4. EL DISEÑO, congelado
- **25 escalas:** 10^k, k de −3 a +3 en pasos de 0.25. Idéntico al prerregistro 46, para que la
  comparación sea legítima.
- **Dos sistemas:** oscilador amortiguado y caída con roce.
- **Cinco semillas nuevas:** 43, 47, 53, 59, 61.
- **Ruido RELATIVO a la escala**, para que la relación señal/ruido sea idéntica en los 25 puntos.
- **Ve en una escala** = declara ley en ≥4 de 5 semillas. **No ve** = ≤1 de 5.
- **Los cuatro criterios se corren con LOS DOS motores** sobre las mismas semillas nuevas.

## 5. LOS CRITERIOS CONGELADOS — y dos de ellos me dejan mal

| | criterio | pide |
|---|---|---|
| **A** | **se cerraron los agujeros** | **exactamente UN tramo contiguo** en los dos sistemas, cubriendo **≥5 de las 6 décadas** |
| **B** | **se acabó la alucinación** | sobre señal casi constante, **0 leyes declaradas en 25 de 25** casos. Una sola ley = fallo |
| **C** | **no se rompió lo que funcionaba** | `sindy4` recupera la ley en **todos** los casos en que `sindy3` la recuperaba a ×1 (oscilador limpio y oscilador con sensor ruidoso) **y calla** en barajado y en ruido puro |
| **D** | **el arreglo es del motor, no de las semillas** | `sindy3`, sobre **estas mismas semillas nuevas**, debe **seguir fallando** A y B |

**El criterio D es el que me deja peor si sale mal.** Si `sindy3` sale limpio con semillas nuevas,
entonces **el defecto era de las semillas y el INFORME-55 estaba equivocado** — y se escribiría
así, con esas palabras y con acta propia.

**Veredictos posibles:**
- **ARREGLADO** — pasan A, B, C y D.
- **ARREGLA UNO SOLO** — pasa A pero no B, o al revés, con C y D en pie.
- **NO ERA LA CAUSA** — falla A con C y D en pie: el umbral no era el problema.
- **EL INFORME-55 ESTABA MAL** — falla D.
- **NO CONCLUYENTE** — no encaja en ninguno.

> ### ENMIENDA 5 — la relación metamórfica que declaré era FALSA. 11-ago-2026, antes de correr
> **La primera versión declaraba:** *"subir el ruido ×200 baja la cuenta, porque con la señal
> enterrada en ruido no hay ley que hallar"*. **Es falsa, y la puerta lo cazó.**
>
> **Por qué es falsa:** el ruido de `escala.py` se añade **dentro** de la integración. **No
> entierra la señal: la conduce.** La desviación de la trayectoria sube de 0.404 a 6.369 al subir
> el ruido, y la ley determinista **sigue estando ahí** — es un oscilador forzado por ruido, no un
> oscilador borrado por ruido. **`sindy4` la encuentra, con margen fuera de muestra de 0.71.**
>
> **La relación correcta, que sí se sabe a priori:** lo que destruye una ley no es el ruido del
> proceso sino **el ruido de MEDIDA** — el que se suma a la trayectoria ya ocurrida, como el de un
> sensor. Eso sí entierra la señal y sí tiene que bajar la cuenta. La relación pasa a declararse
> sobre `ruido_medida`, **con base 0.01 y no 0.0.**
>
> **Y un hallazgo sobre nuestro propio pasado, que no puedo callarme:** el prerregistro-46 declaró
> **esta misma relación falsa** y su Regla 31 la dio por buena. **Aprobó por el motivo equivocado:**
> `sindy3` pierde la ley al subir el ruido del proceso, pero **por fragilidad suya, no porque no
> hubiera ley que hallar.** El chequeo *"la medida responde al ruido"* del prerregistro-46 estaba
> midiendo un defecto del motor y creyendo medir la física del problema. **Esto no invalida el
> INFORME-55** —su barrido no dependía de esa relación— pero queda escrito, y es la **tercera vez**
> que declaro una relación metamórfica sin saberla de verdad a priori.

## 6. REGLA 31 — sobre MI PROCEDIMIENTO, **los dos lados**, y no sobre el motor
Lo escribo explícito porque este mismo error mató al prerregistro 45 y casi al 44, **el mismo
día**: la Regla 31 examina **cómo mido**, nunca lo que hace el objeto de estudio. El
comportamiento de `sindy4` es **resultado**, jamás requisito de entrada.

- **Control positivo (debe aprobar):** a escala ×1, el barrido encuentra la ley con `sindy3` en
  5 de 5. Si no, no hay anclaje y **se detiene**.
- **Señuelo / control negativo (debe fallar):** sobre **ruido puro** escalado igual, la medida no
  declara ley en ninguna de las 25 escalas.
- **La medida responde al ruido:** con ruido ×200 la cuenta cae. Si no cayera, no estaría midiendo
  si hay ley que hallar.
- **La medida distingue escalas:** si diera lo mismo en las 25, no mediría nada.
- **La relación señal/ruido es idéntica en las 25 escalas** — se mide, no se supone.
- **Relaciones metamórficas con base DISTINTA DE CERO.** Este error me mordió **tres veces en un
  día**: multiplicar 0 por 2 da 0 y la puerta mide "×1.000" sin haber probado nada. Ninguna
  relación parte de una cuenta nula.
- **Ninguna relación que no se sepa a priori.** Me mordió dos veces; una era directamente falsa.

## 7. CUÁNDO SE ABANDONA (Regla 13, con número)
- Si falla el **criterio C**, `sindy4` **se descarta entero**. **No hay segunda versión parcheada
  para pasar**: un motor que arregla la escala y deja de ver leyes es peor que el que teníamos.
- Si el **control positivo** da **<5 de 5** a escala ×1, **se detiene**: no hay anclaje.
- Si el **señuelo de ruido puro** declara ley en **≥1** escala, **se detiene**: la medida está rota.
- Si sale **NO CONCLUYENTE**, **no hay tercera versión de este estudio**. Se escribe que el motor
  falla de una forma que este diseño no describe.

## 8. LO QUE ESTE ESTUDIO **NO** PUEDE AFIRMAR
- **Nada del universo.** Es una propiedad de nuestro código.
- **No dice qué resultados nuestros quedan tocados.** Eso es la Fase 2 y exige medir campaña por
  campaña.
- **No dice que `sindy4` sea un buen motor** — solo si estos dos defectos concretos siguen ahí.
- **No toca el diccionario de seis piezas**, así que **no dice nada sobre la jaula** que ese
  diccionario pueda ser.

## 9. FIRMA
Avanza por **quórum adversarial**: criterios congelados antes de correr, semillas nuevas
declaradas, expectativa mía declarada, dos veredictos posibles que me dejan mal (**NO ERA LA
CAUSA** y **EL INFORME-55 ESTABA MAL**) y un criterio de abandono que tira el trabajo entero.
Revocable con una palabra del director.
