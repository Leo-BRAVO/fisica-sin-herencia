# DIAGNÓSTICO DEL MOTOR SIMBÓLICO — qué es, quién falla, y el número exacto que lo rompe
**11 de agosto de 2026 · responde a la pregunta abierta del INFORME-55 §7**
**Lado humano del cortafuegos (Regla 27): este documento cita ciencia humana y por eso vive en
`registros/`. Nada de aquí entra en `arbol/` ni en los datos de Diego.**

---

## 0. ADVERTENCIA DE MÉTODO — qué vale y qué no de este documento
Las dos sondas de §3 y §4 son **exploratorias**: se corrieron para *encontrar la causa*, no para
*probar una afirmación*. **No son evidencia y no se citan como tal.** Su valor es que convierten
"el motor falla" en "falla por esta línea concreta", que es lo que permite escribir un
prerregistro con criterios. **La semilla 7 queda QUEMADA** para el estudio formal del arreglo.

---

## 1. QUÉ ES EL MOTOR SIMBÓLICO, en palabras llanas

Diego mira un mundo y anota números: dónde está algo y a qué velocidad va, miles de veces. El
motor simbólico es **la pieza que convierte esa tabla de números en una fórmula.**

Funciona así, y es más simple de lo que parece:

1. **Se le da una lista de piezas candidatas** — un "diccionario". El nuestro tiene seis
   (`codigo/sindy3.py`, línea 36): `1, x, v, x², xv, v²`. Nada más. El motor **no puede** inventar
   un seno ni una raíz: solo puede combinar esas seis.
2. **Se pregunta: ¿qué mezcla de esas seis piezas explica cómo cambian los números?** Eso es un
   sistema de ecuaciones y se resuelve con álgebra estándar (mínimos cuadrados).
3. **Se tacha lo pequeño.** La mezcla cruda usa las seis piezas con pesos diminutos. El motor
   **borra todo peso menor que un umbral** y vuelve a resolver con las que sobreviven. Repite ocho
   veces. Eso deja una fórmula **corta**, que es lo que queremos: una ley, no un ajuste.
4. **Se comprueba que no fue suerte.** Se rehace el ajuste 200 veces sobre trozos remuestreados de
   los datos y se cuenta en cuántas aparece cada pieza. Solo entra a la ley lo que aparece en el
   90% o más.

Eso es todo. El método se llama **SINDy** (identificación rala de dinámicas no lineales, Brunton,
Proctor y Kutz, 2016) y es un método humano **establecido y publicado**; la variante que usamos —
forma débil (integrar en vez de derivar, para no amplificar el ruido del sensor) más bootstrap —
también es literatura estándar (**Ensemble-SINDy**, Fasel–Kutz et al., *Proc. Royal Society A*,
2022).

**Traducción de la pregunta del director:** el motor no es "el entorno". Es **un algoritmo de
álgebra lineal, escrito por nosotros, de 229 líneas, que ocupa un archivo.** Se puede leer entero
en veinte minutos.

---

## 2. ¿FALLA EL ENTORNO O FALLAMOS NOSOTROS?

**Fallamos nosotros, y en un sitio muy concreto — pero es un fallo que la literatura mundial
también tenía, y que apenas ahora está siendo corregido en público.** Las dos cosas son ciertas a
la vez y ninguna excusa a la otra.

- **No falla PyBullet ni el simulador.** Los defectos se reproducen sobre trayectorias generadas
  con aritmética pura, sin simulador de por medio.
- **No falla Python ni NumPy.** El álgebra hace exactamente lo que se le pide.
- **No falla "el ruido".** Los dos estudios controlaron la relación señal/ruido y la midieron.
- **Falla una decisión de diseño nuestra**, tomada al escribir el módulo y heredada sin examen del
  ejemplo canónico de la literatura: **`umbral=0.05`** en la línea 74 de `codigo/sindy3.py`.

---

## 3. DEFECTO 1 — LOS AGUJEROS DE ESCALA. El número es `umbral=0.05`

### 3.1 La línea culpable
```python
def _stlsq(A, b, umbral=0.05, pasadas=8):
    ...
    chicos = np.abs(W) < umbral        # <- AQUÍ
    W[chicos] = 0.0
```
`W` son los pesos de las seis piezas. La línea dice: **"borra todo peso menor que 0.05"**.

### 3.2 Por qué eso es un error DIMENSIONAL, no un mal ajuste de parámetro
Aquí está el fondo del asunto, y es geometría, no opinión.

Si el mundo se mide en otra unidad —todo multiplicado por un factor **s**— los pesos **no cambian
todos igual**. Se puede calcular exactamente:

| pieza del diccionario | grado | su peso se multiplica por |
|---|---|---|
| `1` | 0 | **s** |
| `x`, `v` | 1 | **1** (no cambia) |
| `x²`, `xv`, `v²` | 2 | **1/s** |

**Los pesos viven en tres escalas distintas que se mueven en direcciones opuestas.** Y `umbral`
es **un solo número** que se compara contra los tres. Es exactamente igual que preguntar *"¿es
0.05 mucho?"* sin decir si hablamos de kilos, de segundos o de metros por segundo al cuadrado.

**Consecuencia mecánica, sin misterio:**
- Si el mundo se mide **pequeño** (s chico), `1/s` es grande → **los pesos basura de las piezas
  cuadradas se inflan y sobreviven al corte** → la ley sale con términos falsos → el bootstrap y
  el ajuste completo no coinciden → el motor devuelve `None`. **Pierde una ley que sí estaba.**
- Si el mundo se mide **grande**, se infla el peso del término constante `1` y se apagan las
  piezas cuadradas verdaderas.

Entre esas dos zonas hay una franja donde el corte cae bien. **Fuera de ella, hay agujeros.**
Eso es precisamente lo que midió el INFORME-55: **tres tramos separados en cada sistema, y la zona
muerta en el MISMO sitio en dos sistemas independientes.** Tenía que estar en el mismo sitio: no
es una propiedad de los sistemas, es una propiedad del corte.

### 3.3 La sonda (exploratoria, semilla 7 quemada)
Barrido de 13 escalas contando cuántos de los 12 pesos del ajuste crudo superan 0.05:

| escala | pesos sobre el umbral | ¿ve la ley? |
|---|---|---|
| 10⁻³ | **7 de 12** | **no** |
| 10⁻²·⁵ a 10³ | 3 de 12 (los tres verdaderos) | sí |

**A escala 10⁻³ aparecen cuatro pesos falsos por encima del corte, y el motor se cae.** Es el
mecanismo predicho por la tabla de §3.2, observado.

### 3.4 Esto ya está resuelto en la literatura — y muy recientemente
No hay que inventar nada. El problema tiene nombre y cura publicada:

- **El diagnóstico exacto está publicado en 2026**: *"la normalización de los datos actúa como un
  hiperparámetro implícito y no controlado que puede alterar catastróficamente el resultado del
  descubrimiento"*. En el sistema de Lorenz con datos normalizados y ruido, **STLSQ —nuestro
  algoritmo— obtiene 0% de aciertos en todo el rango de parámetros probado.** No somos un caso
  raro: es el comportamiento conocido del método que copiamos.
- **La cura publicada (STCV):** sustituir el corte por magnitud por un **criterio adimensional**.
  En vez de preguntar *"¿es el peso mayor que 0.05?"* se pregunta *"¿es este peso **consistente**
  entre remuestreos?"*, con la **Presencia de Coeficiente**:

  > **CP = √m · μ(ξ) / σ(ξ)**

  la media del peso dividida por su desviación entre ajustes. **Esa razón no tiene unidades**, así
  que **no cambia si el mundo se mide en otra escala.** Un término verdadero mantiene poca
  varianza entre realizaciones ruidosas; uno espurio varía de forma errática.
- **La cura alternativa (adimensionalización, teorema Π de Buckingham):** convertir las variables
  en grupos sin unidades antes de ajustar. Publicado en *Nature Computational Science* (2022) y
  demostrado que mejora la precisión de PySR.

### 3.5 Lo bueno: ya teníamos media cura y no la estábamos usando
`sindy3` **ya calcula** la probabilidad de inclusión por bootstrap (`prob`, línea 115) — que es
casi la mitad de CP. Lo que hace después es **tirarla** y volver a cortar por magnitud (línea 119).
**El arreglo no es reescribir el motor: es dejar de tomar la decisión con el número equivocado.**

---

## 4. DEFECTO 2 — LA ALUCINACIÓN. El motor no tiene ninguna prueba de que la ley SIRVA

### 4.1 La sonda, en una línea (exploratoria, semilla 7 quemada)
Señal casi constante (lo que mató al prerregistro-45), medida junto al oscilador sano:

| | número de condición de la matriz A | qué declara el motor |
|---|---|---|
| oscilador sano | **10.5** | la ley correcta, 3 términos |
| señal casi constante | **7.06 × 10⁹** | **12 términos, probabilidad 1.000 en los doce** |

**Nueve órdenes de magnitud de diferencia**, y el motor no mira ese número ni una vez.

### 4.2 Qué significa, en llano
Cuando la señal es casi plana, las seis piezas del diccionario **se parecen entre sí** (todas son
casi constantes). El sistema de ecuaciones se vuelve **casi indeterminado**: hay infinitas mezclas
que ajustan igual de bien, y el álgebra devuelve una cualquiera, con pesos enormes y arbitrarios.
Esos pesos enormes **superan el umbral sin esfuerzo**, así que ninguna pieza se borra.

### 4.3 Y aquí está la parte que más me importa que quede escrita
**El bootstrap dio 1.000 en las doce piezas. Y eso NO fue un fallo del bootstrap: fue el bootstrap
diciendo la verdad sobre la pregunta equivocada.**

El bootstrap mide **estabilidad**, no **verdad**. Remuestrear un sistema degenerado da, cada vez,
un sistema degenerado. **Una degeneración es establemente degenerada.** Por eso la confianza 1.0
que publicó el INFORME-54 no era evidencia de una ley: era evidencia de que las 200 remuestras del
sistema roto estaban rotas de la misma manera.

**Es la lección de método más transferible del proyecto entero:** *un número de confianza alto
solo significa algo si la pregunta que responde puede tener respuesta negativa.* Es el mismo mal
que el criterio 4 tautológico del prerregistro-41 y que los chequeos que aprueban sobre listas
vacías. **Tercera aparición del mismo error, en tres sitios distintos.**

### 4.4 Lo que falta, y es barato
El motor **nunca comprueba que la ley prediga**. No hay ni una línea que pregunte *"¿esta fórmula
explica los datos mejor que decir 'todo es constante'?"*. Faltan tres guardas, todas de una línea:

1. **Condición de A** — si supera un tope prerregistrado, **el motor calla**. (Habría matado la
   alucinación de golpe: 7×10⁹ contra 10.5.)
2. **Poder predictivo fuera de muestra** — ajustar en unas ventanas, medir en otras que no vio, y
   exigir que gane a la línea base tonta (**Regla 12**, que el motor **no cumple hoy** aunque la
   exijamos a cada prerregistro).
3. **Rango de variación mínimo** — si la señal no se mueve, no hay dinámica que hallar.

---

## 5. EL BALANCE HONESTO
- **No hay que tirar el motor.** Los dos defectos son **una línea de decisión mal escrita** y
  **tres guardas que nunca se escribieron**. La forma débil (integrar en vez de derivar) sigue
  siendo correcta y sigue siendo la razón de existir del módulo.
- **Sí hay que dejar de heredar sin examinar.** Los dos defectos entraron **copiando la receta
  canónica de la literatura sin someterla a nuestra propia Regla 31.** Es incómodo y es exacto:
  el proyecto se llama *física sin herencia* y el corazón del proyecto heredó un umbral.
- **Y el motor no cumple nuestras propias reglas.** Le exigimos línea base tonta (R12) y criterio
  de abandono (R13) a cada prerregistro; el motor no tiene ninguna de las dos.

---

## 6. LO QUE **NO** SE AFIRMA
- **No se afirma que arreglar el umbral arregle los agujeros.** Es la hipótesis mejor sostenida
  que tenemos, con mecanismo, con tabla dimensional y con literatura — **y sigue siendo una
  hipótesis hasta que un estudio prerregistrado la mida.**
- **No se afirma qué resultados nuestros están tocados.** Sigue exigiendo revisión campaña por
  campaña, y sigue sin hacerse.
- **No se toca ningún umbral de ningún estudio ya corrido.**

## 7. LA PREGUNTA QUE ABRE (Regla 18)
> **¿Cuántas de nuestras 67 corridas dieron "no concluyente" por este umbral y no por el mundo?**
> Un motor con agujeros produce falsos negativos: los "no vio nada" son los sospechosos, no los
> hallazgos. La revisión es mecánica —rehacer cada corrida con el motor arreglado y comparar
> veredictos— y es **el primer trabajo que el motor nuevo debería hacer.**

## 8. LO QUE LE TOCA AL DIRECTOR
Nada urgente que firmar. Una sola decisión de orden: **el arreglo del motor va antes que todo lo
demás de la lista de problemas**, porque cada estudio nuevo que corramos hasta entonces hereda los
dos defectos.

---
### FUENTES (lado humano del cortafuegos)
- Fasel, Kutz et al., *Ensemble-SINDy*, Proc. R. Soc. A 478:20210904 (2022) — https://arxiv.org/pdf/2111.10992
- *Towards a data-scale independent regulariser for robust SINDy* (STCV, Presencia de Coeficiente), 2026 — https://arxiv.org/html/2603.05201
- Bakarji et al., *Dimensionally consistent learning with Buckingham Pi*, Nature Comput. Sci. (2022) — https://www.nature.com/articles/s43588-022-00355-5
- *Enhancing Symbolic Regression with Dimensional Analysis* (2024) — https://arxiv.org/pdf/2411.15919
- *Discovering equations from data: symbolic regression in dynamical systems* (2025) — https://arxiv.org/html/2508.20257v1
