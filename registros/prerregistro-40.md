# Prerregistro 40 — G11 TEMPLE y G12 REFLEJOS: los dos genes que estaban prometidos y no existían — 10 de agosto de 2026
**Estado: AVANZA POR QUÓRUM (Regla 15 enmendada). Revocable con una palabra del director al leerlo.**
**Pedido explícito suyo: *"quiero que implementes temple y reflejos detalladamente con investigación
que respalde... mira qué puedes tomar de LeCun"*.**

## Por qué existen y por qué llevaban un mes vacíos
La auditoría del 10-ago (INFORME-45) encontró que `G11_temple` y `G12_reflejos` estaban **en el
genoma sin una línea de código**. El genoma prometía dos órganos que no había. Quedaron marcados
como *diseño no implementado*; ahora se construyen.

## LA INVESTIGACIÓN QUE LOS RESPALDA
La arquitectura de LeCun para inteligencia autónoma tiene **exactamente estas dos piezas**, con
nombres distintos y con una propiedad cada una que nos importa mucho:

### TEMPLE ← el **módulo de coste intrínseco**
En esa arquitectura, el coste intrínseco *"computa un coste dado el estado actual del mundo y los
estados futuros predichos — puede imaginarse como hambre, dolor o incomodidad general"*. Y lo
decisivo:

> **el coste intrínseco está cableado y es INMUTABLE — no entrenable.**

**Por qué eso nos importa más que a nadie:** si el temple fuera entrenable, Diego aprendería a
**sentirse bien** en lugar de aprender **sobre el mundo**. Ajustaría lo que le duele hasta que nada
le duela. Eso tiene nombre y es un modo de fallo conocido, y encaja exactamente con lo que nuestra
**Regla 30** ya prohíbe: *los jueces jamás se automodifican*. El temple es un juez interno, así que
hereda esa prohibición entera.

### REFLEJOS ← el **Modo-1, la política reactiva**
*"Un módulo de política que computa una acción a partir del estado. Actúa rápido y produce
decisiones simples. No involucra razonamiento ni planificación complejos."* Y la parte que convierte
esto en algo construible y no en un adorno:

> **el agente puede entrenar la política para aproximar las acciones óptimas que salen del
> razonamiento de Modo-2. Así adquiere destrezas que quedan compiladas en una política reactiva.**

**Un reflejo no es una regla que le metemos: es una deliberación destilada.** Eso da criterios
comprobables — un reflejo debe ser **más rápido** que la deliberación que lo originó, **coincidir**
con ella donde ella opinaba, y **callar** donde ella no actuaría.

## LA FRONTERA, y aquí está el riesgo real de estos dos genes
**Un reflejo es la puerta trasera perfecta para meter física humana.** Si yo escribo "si el objeto
cae, retira la mano", le estoy enseñando gravedad disfrazada de instinto. Por eso:

- **Ningún reflejo se escribe a mano. Todos se DESTILAN** de decisiones que Diego ya tomó.
- **`sanidad.politica_limpia()`** comprueba mecánicamente que ninguno nombre masa, gravedad, caída,
  peso ni nada del mundo.
- El temple mide **su propio estado** (gasto, error, sorpresa), **jamás** propiedades del mundo.

## QUÉ SE CONSTRUYE

### `codigo/temple.py` — G11, modo `mide`
Un coste intrínseco **cableado e inmutable** con tres términos, todos sobre **su propio estado**:
| Término | Qué mide | De dónde sale |
|---|---|---|
| **gasto** | cuánto le está costando | G10 interocepción, que ya existe |
| **error** | cuánto se está equivocando al predecir | G1 predicción |
| **sorpresa** | cuánto le desconcierta lo que ve | G14 incertidumbre |

**El temple no decide nada.** Publica un número y su desglose. Modo `mide`: el portero de
`sinapsis.py` le impide publicar decisiones, y eso ya se comprueba en producción cada ronda.

### `codigo/reflejos.py` — G12, modo `mide`
Destila una política rápida a partir de decisiones que Diego ya tomó despacio. **No inventa
ninguna.** Y trae su propio freno: un reflejo solo se adopta si **supera las cuatro pruebas** de
abajo.

## REGLA 31 — ocho casos declarados ANTES de correr

**Temple (4):**
1. **INMUTABLE:** intentar entrenar el temple debe **fallar**, no ajustarse. Es la Regla 30 hecha
   código: un juez que se puede mover no es un juez.
2. **Sube con el gasto:** más esfuerzo → más coste. Si no, no mide lo que dice (tipo A).
3. **Sube con el error:** equivocarse más → más coste.
4. **NO se puede bajar sin hacer nada:** una política que se queda quieta **no** puede minimizar el
   temple. Sin esto, lo óptimo sería no hacer nada nunca — el fallo clásico del coste mal puesto.

**Reflejos (4):**
5. **MÁS RÁPIDO** que la deliberación que destiló. Si no lo es, no es un reflejo: es una copia lenta.
6. **COINCIDE** con ella por encima del azar donde ella opinaba.
7. **CALLA** donde la deliberación no actuaría — un reflejo que dispara siempre no es un reflejo.
8. **SEÑUELO:** una deliberación de **puro ruido** no puede producir un reflejo aprobado. Es el
   hermano de los cuatro señuelos que ya cazaron fallos reales en su primera corrida.

## LA PUERTA (`metodo.py`)
Los dos módulos **no se encolan hasta pasar los 8 pasos**: manifiesto declarado, fórmulas
comprobadas con relaciones metamórficas, arranque al final, sin nombres pisados, ficha de sanidad,
Regla 31, escritura limpia.

## QUÉ NO SE AUTORIZA
- **Ninguno de los dos entra al genoma como activo por esta corrida.** Se construyen y se miden;
  activarlos es cambio de genoma y exige generación nueva (Regla 33).
- **El temple no puede subir de modo.** Si un día decidiera, sería un ente que actúa para sentirse
  bien, y eso es exactamente lo que la investigación advierte que no se debe permitir.
- **Ningún reflejo escrito a mano.** Nunca.

## LA PREDICCIÓN, comprometida ANTES de correr
- **Espero que el temple pase sus cuatro casos**: es aritmética sobre su propio estado y no tiene
  dónde esconderse.
- **NO tengo confianza en el caso 6** (que el reflejo coincida con la deliberación). Diego decide
  hoy con muy pocas señales, y destilar de pocas decisiones da una política pobre. **Si falla, la
  lectura honesta será que aún no hay bastante deliberación que destilar** — y la cura será
  esperar, no bajar el umbral.

## Firmado
Avanza por quórum. Investigación citada en `registros/INVESTIGACION-TEMPLE-REFLEJOS.md`.
