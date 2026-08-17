# CORRECCIÓN 01 — mi sospecha sobre la semilla 263 era falsa, y el diagnóstico encontró un defecto peor en mi propio código
**11 de agosto de 2026. Nota de corrección al INFORME-67, §6.**
**VIVE EN `registros/` Y NO EN `resultados/`, y el auditor de actas me obligó a moverla: la puse
donde viven los RESULTADOS y sus números salen de un TANTEO, que por construcción no puede probar
nada. Era un error de categoría mío — poner algo en `resultados/` es afirmar que es un resultado.**
**Origen:** tanteo del banco (`banco/colapso/tanteo.json`), semillas 263 y 251 **quemadas**.
**Esto NO es un estudio y sus números NO son evidencia.** Es un diagnóstico que **retira una
sospecha publicada** y **declara un defecto de método**.

---

## 1. LA SOSPECHA QUE RETIRO
El INFORME-67 cerró con esta pregunta:
> *"La sospecha más simple es que **los dos puntos de atención colapsen sobre el mismo sitio**."*

**Es falsa, y por el lado contrario al que esperaba.** En el tanteo, la separación media entre los
dos puntos fue **1.489 en la semilla 263** —la que se derrumbó— y **0.2603 en la 251**, que fue
bien. **Los puntos de la semilla mala están CINCO VECES MÁS SEPARADOS, no colapsados.**

## 2. Y AL COMPROBARLO APARECIÓ ALGO PEOR, que es mío
**Al reproducir la semilla 263 sola, el R² salió 0.6148. En el estudio había salido -0.0205.**

**La misma semilla, el mismo código, dos números completamente distintos.** La causa está en mi
propio código, en `ojos_keypoint.py`:

```python
for nombre, M in (("pixel_mse", Pixel()), ("keypoint_softmax", Keypoint())):
    m, perdida = entrenar(M, X, semilla=semilla)   # ← la semilla se fija AQUÍ DENTRO
```

**Los dos modelos se CONSTRUYEN antes de que `entrenar` fije la semilla.** Sus pesos iniciales
salen del estado global que hubiera en ese momento — **que depende de todo lo que corrió antes**.

> **La semilla que declaré en el prerregistro no controlaba la inicialización de los pesos.**
> Controlaba la escena y el orden de los lotes, no el punto de partida del entrenamiento.

## 3. QUÉ INVALIDA Y QUÉ NO — con precisión, sin refugiarme ni exagerar

**NO invalida el hallazgo principal del INFORME-67.** El derrumbe del codificador de hoy con brazos
delgados —de 0.6287–0.7848 a 0.1838–0.3852— es **consistente en las cinco semillas** y las dos
arquitecturas recibieron **el mismo trato dentro de cada corrida**. Ese resultado se sostiene.

**NO invalida la reproducibilidad del estudio completo.** Volver a correr el script entero, desde
el principio, da la misma secuencia y los mismos números.

**SÍ invalida la lectura por semilla.** El **-0.3277** de la 263 **no es atribuible a esa semilla**:
es el resultado de una inicialización que nadie controló. **Y por tanto la frase del INFORME-67
—"el candidato falla 1 de cada 5 veces"— no está sostenida.** Lo que está sostenido es que
**hay variabilidad grande que la semilla declarada no explica**, que es una afirmación más débil y
más incómoda.

**Y toca algo que este proyecto sí promete:** *"todo debe poder ser auditado y replicado"*. **Una
semilla que no aísla su corrida rompe la mitad de esa promesa.**

## 4. LO QUE NO HAGO, y por qué
**No edito `ojos_keypoint.py` ni `ojos_brazo.py`.** Los dos pasaron la puerta y están sellados;
editarlos **mataría su sello** y dejaría irreproducibles los estudios que ya produjeron —
exactamente el motivo por el que `sindy3` sigue intacto. **El arreglo va en un módulo nuevo, con su
prerregistro**, y el estudio se vuelve a correr con semillas nuevas.

**Tampoco corrijo el INFORME-67.** Se queda como está, y esta nota lo corrige desde fuera. **La
historia del error se conserva; ésa es la regla y no la toco por comodidad.**

## 5. LO QUE ENTRA EN EL CATÁLOGO
`disciplina.py` recibe el **error nº16: "la semilla declarada no controla toda la aleatoriedad"**,
con este incidente y sus dos números. **Y es mecanizable**: se puede comprobar que un módulo que
declara semillas fije la del marco **antes** de construir cualquier modelo.

## 6. LO QUE **NO** SE AFIRMA
- **NO se afirma que el softmax espacial sea estable.** Se afirma que **no sabemos** si el
  derrumbe era del método o de una inicialización sin control. **Es menos de lo que dije ayer.**
- **NO se afirma que los demás estudios estén afectados.** Solo estos dos usan PyTorch; el resto
  usa NumPy con generadores locales, que sí aíslan. **Comprobarlo módulo a módulo está pendiente.**
- **Nada del universo.**

## 7. LO QUE LE TOCA AL DIRECTOR
Ninguna decisión. Un apunte que prefiero decir yo: **el tanteo que hice para confirmar una
sospecha mía terminó desmintiéndola y encontrando un fallo peor en mi propio código.** Es el mejor
argumento que tengo a favor del carril rápido — **y también el recordatorio de que un guardián no
sustituye a mirar el resultado con desconfianza.**
