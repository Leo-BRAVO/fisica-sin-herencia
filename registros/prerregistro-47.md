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
**Este estudio corre sobre cinco semillas nuevas: `43, 47, 53, 59, 61`**, declaradas aquí antes de
tocarlas.

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
   `CP = √m · μ(ξ) / σ(ξ)` sobre los remuestreos del bootstrap. Es una razón **sin unidades**, así
   que **no cambia si el mundo se mide en otra escala**. Piso de CP congelado: **3.0**.
2. **Adimensionalización previa**: las columnas del diccionario se normalizan por las escalas de
   **los propios datos** antes de ajustar, y los pesos se devuelven a unidades al final. **No se
   usan unidades humanas** — eso sería herencia; se usan las escalas empíricas de la serie.
3. **Guarda de condición**: si el número de condición de la matriz supera **10⁶**, el motor
   **calla**. Razón declarada, y es aritmética y no empírica: la doble precisión lleva ~16 cifras
   significativas, y con condición 10⁶ se conservan 10 cifras buenas.
4. **Poder predictivo fuera de muestra**: se ajusta en el 70% de las ventanas y se mide en el 30%
   restante. **Si la ley no supera a la línea base tonta en las ventanas que no vio, no se declara
   ley.**

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
