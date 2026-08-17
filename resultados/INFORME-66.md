# INFORME-66 — ACTA DEL PRERREGISTRO 56: el latente SÍ es una coordenada, y el margen que declaré no se cumple
**11 de agosto de 2026. Cinco semillas nuevas (227, 229, 233, 239, 241), dos arquitecturas, la
misma pérdida y los mismos datos.**
**Datos crudos:** `resultados/p56-ojos/medida.json`. Módulo: `codigo/ojos_keypoint.py` (puerta 8/8).
**VEREDICTO, con las mismas palabras del archivo de datos:** *EL TANTEO ERA RUIDO — el softmax
espacial no le gana al codificador de hoy, y la causa de que los ojos puntuen a ruido sigue sin
encontrarse.*

---

## 1. LOS NÚMEROS

| semilla | 227 | 229 | 233 | 239 | 241 |
|---|---|---|---|---|---|
| **softmax espacial** | 0.891 | 0.9293 | 0.898 | 0.9594 | 0.8745 |
| **píxel (el de hoy)** | 0.7848 | 0.6894 | 0.6287 | 0.7383 | 0.7208 |
| **ventaja** | **0.1062** | 0.2399 | 0.2693 | 0.2211 | 0.1537 |

| criterio congelado | pedía | salió | |
|---|---|---|---|
| **A** el latente es coordenada | R² ≥ 0.80 en 5 de 5 | **5 de 5** | ✔ |
| **B** le gana al de hoy | ventaja ≥ 0.15 en 5 de 5 | **4 de 5** — la 227 da **0.1062** | ✘ |
| **C** la medida no se infla | ≤ 0.10 contra objetivo al azar | todas negativas: **[-0.0255, -0.0203, -0.0093, -0.0266, -0.0061]** | ✔ |
| **D** la medida responde | baja con ruido de sensor | **0.8685 → -0.0044** | ✔ |
| **E** no se rompió el codificador | no diverge | no divergió | ✔ |

## 2. EL RÓTULO DEL VEREDICTO DESCRIBE MAL LO QUE PASÓ — y no lo cambio
**El veredicto congelado es el que es y se queda.** Pero el rótulo que yo mismo escribí en el
código —*"el softmax espacial no le gana al codificador de hoy"*— **es falso como descripción**:

> **El softmax espacial gana en las CINCO semillas**, con ventajas de 0.1062 a 0.2693 y una media
> cerca de 0.20. **Lo que falló no es que no gane: es que en una de las cinco no gana POR EL MARGEN
> QUE YO DECLARÉ.**

**Y aun así el veredicto no se toca.** Mover el 0.15 después de ver que una semilla se quedó a
0.044 es **exactamente lo único que el director se reservó**, y es la razón entera de congelar los
criterios antes. **Un margen que se ajusta cuando no se cumple no es un margen.**

## 3. LO QUE **SÍ** QUEDA ESTABLECIDO — y es el criterio A, que pasó limpio
**El cuello de botella de softmax espacial produce latentes que SON coordenadas: R² ≥ 0.80 en las
cinco, con la misma pérdida por píxel y los mismos datos que el codificador de hoy.**

El codificador actual se queda entre **0.6287 y 0.7848**. La diferencia no está en el
entrenamiento: **está en dónde puede guardar la información.** En el latente plano cabe textura; en
un softmax espacial **solo caben coordenadas**.

## 4. POR QUÉ EL TANTEO EXAGERÓ, y por qué esto justifica el carril rápido entero
En el banco, con dos semillas, el codificador de hoy dio **0.475 y 0.6671**. En el estudio, con
cinco nuevas, da **0.6287 a 0.7848** — bastante mejor. **El tanteo no se equivocó sobre el
ganador: se equivocó sobre el tamaño de la diferencia**, porque sus dos semillas fueron de las
malas para el rival.

> **Esto es exactamente lo que el carril rápido existe para que pase AQUÍ y no en un acta.** El
> banco me dio en minutos la señal para escribir el prerregistro; el estudio formal, con semillas
> nuevas y criterios congelados, **impidió que una exageración se convirtiera en un hallazgo
> publicado.** Los dos carriles hicieron su trabajo el mismo día en que nacieron.

## 5. LO QUE ESTO SIGNIFICA PARA LA PREGUNTA DE FONDO
El director pregunta por qué Diego no descubre leyes con los vídeos. La hipótesis era: **la pérdida
por píxel produce latentes que no son coordenadas.**

**Queda medio confirmada, y hay que decirlo con esa mitad:**
- **La parte confirmada:** un cuello de botella espacial **sí** produce coordenadas (A, 5 de 5).
- **La parte NO confirmada:** que la ventaja sobre lo actual sea grande y consistente. **El
  codificador de hoy no es tan malo como yo creía sobre esta escena** — llega a 0.78.

**Y hay un límite del diseño que no puedo saltarme:** esta escena tiene **un objeto redondo sobre
fondo estático**. El gimnasio real tiene **un brazo articulado**, que es justo el caso donde la
crítica decía que la pérdida por píxel subpondera *"las articulaciones delgadas"*. **Puede que la
diferencia real esté ahí y esta escena no la muestre.** Ese es otro estudio, y no lo adelanto.

## 6. LO QUE **NO** SE AFIRMA
- **NO se cambia el ojo de Diego.** Estaba declarado antes de correr y se cumple: **con este
  resultado no se toca nada.**
- **NO se afirma que la pérdida por píxel sea la causa** de que los ojos puntúen a ruido. Sigue
  siendo la hipótesis mejor sostenida y **sigue sin confirmarse**.
- **NO se afirma que el softmax espacial no sirva.** Gana en 5 de 5 y su latente es coordenada:
  lo que no está establecido es el **margen**.
- **Nada del universo.**

## 7. LA PREGUNTA QUE ABRE (Regla 18)
> **¿Cambia todo esto con un brazo articulado en vez de un disco?** La escena de juguete tiene un
> objeto compacto y brillante — el caso **fácil** para cualquier codificador. La crítica externa
> señalaba las *articulaciones delgadas*, y **esta escena no las tiene**. Si la diferencia crece
> ahí, la hipótesis se confirma; si no crece, hay que buscar la causa en otro sitio. **Es el
> estudio siguiente y necesita su propio prerregistro.**

## 8. LO QUE LE TOCA AL DIRECTOR
Ninguna decisión urgente. Un aviso de método que quiero dejar dicho: **este acta es la primera del
proyecto en la que un criterio congelado me deja sin poder afirmar algo que los datos casi
sostienen.** Podía haberlo subido con una frase — *"gana en las cinco, ¿qué más da el margen?"*—
y **eso habría convertido todos los criterios anteriores en decoración.**
