# Prerregistro 56 — ¿ES LA PÉRDIDA POR PÍXEL LO QUE CIEGA A DIEGO? — 11 de agosto de 2026
**Items 25 y 26 de la lista. Peldaño (Regla 9): Fase 1 — propiedad de nuestro código, no del
universo.**
**Estado: FIRMADO antes de escribir `ojos_keypoint.py`.**

---

## 0. DE DÓNDE SALE
De una crítica externa que el director trajo, y **su punto era mejor que nada que yo hubiera
escrito**. `ojos_gimnasio.py`, línea 54:
```python
rec = ((modelo.decodificar(zb) - xb) ** 2).mean()
```
**Error cuadrático por píxel.** Si más del 90% de los píxeles son fondo, **el óptimo de esa pérdida
es reconstruir la pared**, no el objeto pequeño que se mueve.

**Y ata tres hallazgos que teníamos sueltos:** las cuatro arquitecturas de ojo puntuaron **a escala
de ruido** en el torneo · `percepcion2` **diverge** en 3 de 4 entrenamientos (INFORME-63) · el motor
recibe series de las que no puede sacar nada, y calla o alucina.

## 1. LO QUE YA VI EN EL BANCO, declarado antes de correr
**El carril rápido (`banco.py`) se estrenó con esto.** Sobre una escena con fondo texturizado y un
objeto de ~13 píxeles de 1024, **misma pérdida, mismos datos, mismas épocas, solo cambia el cuello
de botella**:

| | R² fuera de muestra de la posición verdadera |
|---|---|
| pérdida por píxel | **0.475 · 0.6671** |
| softmax espacial | **0.9036 · 0.9103** |

**Eso es un TANTEO y NO es evidencia de este estudio.** Las semillas **211 y 223 quedan quemadas**
y están anotadas en la bitácora del banco. **Este estudio corre sobre cinco nuevas: `227, 229,
233, 239, 241`.**

**Declaro mi expectativa, para que se me pueda descontar:** espero que el softmax espacial gane.
**Si no gana, diré que el tanteo fue ruido de dos semillas y que la pérdida por píxel no era la
causa** — y entonces la causa de que los ojos puntúen a ruido sigue sin encontrarse.

## 2. LA PREGUNTA
> ¿Produce el cuello de botella de **softmax espacial** latentes que **son coordenadas**, donde la
> pérdida por píxel produce mezclas de textura — **con la misma pérdida y los mismos datos**?

## 3. LA LÍNEA BASE TONTA (Reglas 11 y 12)
**El propio codificador de hoy**, `pixel_mse`. No es un rival de paja: es **exactamente lo que
Diego usa ahora**. Si el nuevo no le gana por un margen declarado, no hay motivo para cambiarlo.

## 4. EL DISEÑO, congelado
- **Escena:** fondo con textura estática + un objeto pequeño en trayectoria conocida. **La verdad
  la ponemos nosotros y SOLO SE USA PARA EVALUAR.** Entrenar contra ella sería darle la respuesta,
  y además no mediría nada: **las dos arquitecturas se entrenan con la MISMA pérdida por píxel.**
- **Cinco semillas nuevas:** 227, 229, 233, 239, 241.
- **La medida:** R² **fuera de muestra** (70/30 por tiempo) de la posición verdadera recuperada
  **linealmente** del latente. Lineal a propósito: si hiciera falta una red para sacar la posición
  del latente, el latente **no es** una coordenada.

## 5. LOS CRITERIOS CONGELADOS

| | criterio | pide |
|---|---|---|
| **A** | **el latente ES una coordenada** | softmax espacial: **R² ≥ 0.80** en **5 de 5** semillas |
| **B** | **le gana al de hoy** | ventaja **≥ 0.15** de R² sobre `pixel_mse` en **5 de 5** |
| **C** | **la medida no se infla sola** | contra un objetivo **aleatorio** sin relación con el vídeo, **R² ≤ 0.10** — si no, el R² lo produce el ajuste y no el latente |
| **D** | **la medida responde** | al añadir ruido de sensor creciente a los fotogramas, el R² **baja** en las dos arquitecturas |
| **E** | **no se rompió el codificador** | el softmax espacial **sigue reconstruyendo**: su pérdida final es finita y no diverge |

> ### ENMIENDA 1 — el factor del ruido lo elegí a ojo. 11-ago-2026, antes de correr el estudio
> **LA PUERTA reprobó la relación metamórfica: con ruido de sensor ×10 el R² no baja (×1.020).**
>
> **Y el fallo es mío, pero no de la relación: del factor.** *"Suficiente ruido de sensor entierra
> el objeto y baja el R²"* **es cierto a priori**. Lo que elegí a ojo fue el **×10**, que lleva la
> desviación del ruido de 0.02 a **0.20** — y el objeto tiene un **contraste de 0.5** sobre un
> fondo de desviación 0.15. **Con σ=0.20 el objeto sigue siendo el borrón más brillante de la
> escena**, así que el softmax espacial lo encuentra igual. La relación no falló: **mi número era
> demasiado pequeño para lo que la relación afirma.**
>
> **El factor pasa a derivarse del mecanismo, no de mi intuición: ×50**, que lleva σ a **1.0**,
> es decir **el doble del contraste del objeto**. Ese número **lo conozco a priori porque yo
> construí la escena** — no lo he sacado de mirar ningún resultado.
>
> **Y esto puede seguir fallando.** Si con σ al doble del contraste el R² tampoco baja, entonces
> **la relación es falsa** y lo escribiré con esas palabras, como ya hice tres veces este mes.

## 6. REGLA 31 — sobre MI PROCEDIMIENTO, los dos lados
- **Control positivo:** sobre un latente que **es** la posición verdadera más un poco de ruido, la
  medida da R² alto. Si no, la medida no mide lo que dice.
- **Señuelo (criterio C):** contra un objetivo aleatorio, R² ≈ 0. **Es el nulo correcto para ESTA
  medida** — y no barajar los fotogramas, porque la posición es **por fotograma** y barajar el
  tiempo no destruye nada. *(Esa lección me costó el prerregistro 52.)*
- **Base distinta de cero** en la relación metamórfica. Novena vez este mes.
- **`SUJETO` declarado**: el sujeto son **las dos arquitecturas**, y mi Regla 31 **no las examina**
  — trabaja con latentes sintéticos.

## 7. CUÁNDO SE ABANDONA (Regla 13, con número)
- Si falla **C**, **se detiene**: si el R² se infla solo, ninguna comparación vale.
- Si falla **A** pero pasa **B**, el veredicto es **MEJORA SIN RESOLVER**: gana al de hoy y aun así
  el latente no es una coordenada. **No se cambia nada de Diego con ese resultado.**
- Si falla **B**, se escribe **EL TANTEO ERA RUIDO** y la causa sigue sin encontrarse.
- Si sale **NO CONCLUYENTE**, no hay segunda versión de este estudio.

## 8. LO QUE **NO** SE AFIRMA
- **Nada del universo.**
- **NO se afirma que esto arregle el torneo de ojos.** Que un latente sea coordenada **sobre una
  escena de juguete** no dice que lo sea sobre el gimnasio con un brazo articulado. Ese estudio es
  otro.
- **NO se cambia el ojo de Diego con este resultado.** Aprobar aquí solo autoriza **escribir el
  estudio siguiente**, sobre la escena real.
- **NO se afirma que la posición verdadera sea legítima como señal de entrenamiento.** Se usa
  **solo para evaluar**, y meterla en el entrenamiento sería herencia por la puerta de atrás.

## 9. FIRMA
Avanza por **quórum adversarial**: el criterio **C** manda detenerse si mi propia medida se infla,
el **B** puede dejar el tanteo en ruido y dejarme sin causa, y la línea base tonta **es el
codificador que Diego usa hoy**, no un rival de paja. Revocable con una palabra del director.
