# INFORME-44 — ACTA DEL PRERREGISTRO 36: la vara de las firmas **NO SIRVE A NINGUNA DURACIÓN**, y mi hipótesis era falsa
**10 de agosto de 2026.** Corrida oficial completa, tres guardianas verdes, commiteada en `main`
(`7f452aa`).

El prereg-36 no medía a Diego: medía **el instrumento**. El instrumento reprobó, y de paso reprobó
**mi explicación de por qué reprobaba**.

---

## 1. LA TABLA COMPLETA

| pasos/fase | control positivo | balbuceo ciego | señuelo agitado (específico) | dispersión de la ciega | separación de medias |
|---|---|---|---|---|---|
| 400 | **0.4** | 0.0 | **0.2** | 0.1032 | 5.33σ |
| 800 | **0.2** | **0.2** ⚠ | 0.0 | 0.2724 | 1.10σ |
| 1600 | **0.6** | 0.0 | **0.2** | 0.1110 | 3.46σ |
| 3200 | **0.6** | 0.0 | 0.0 | 0.1165 | 4.28σ |

Razones del control positivo, semilla a semilla:
- 400: 1.212, 1.138, 1.481, 2.351, 2.199
- 800: 1.837, 1.067, 1.146, 1.367, 1.398
- 1600: 1.616, 1.279, 1.558, 1.529, 1.492
- 3200: 1.885, 1.197, 1.203, 1.696, 1.575

**VEREDICTO: la vara NO es usable a ninguna duración probada.**

Tres fallos distintos, no uno:
1. **El control positivo nunca llega a 5/5.** Su mejor marca es 3 de 5.
2. **A 800 pasos el balbuceo ciego disparó el criterio.** Un falso positivo del control negativo:
   el instrumento vio la firma donde con certeza no la hay.
3. **El señuelo agitado fue coronado como específico 1 de 5 veces**, a 400 y a 1600. Se mueve más y
   de forma desigual **sin ninguna contingencia detrás**, y aun así pasó. Ese señuelo se construyó
   en este mismo prerregistro y **cazó lo que venía a cazar a la primera**.

## 2. MI HIPÓTESIS REGISTRADA ERA FALSA

En el prereg-36 escribí, antes de correr:

> *"Si la dispersión de la línea base es del orden del efecto buscado, la vara no puede ver ese
> efecto por mucho que insistamos. Ésa es la sospecha que registro antes de correr; la medición
> dirá."*

La medición dijo **que no**:
- La dispersión **no baja** al alargar las fases: 0.103 → 0.272 → 0.111 → 0.117. Ocho veces más
  muestras y la misma dispersión.
- La tasa de acierto **no es monótona**: 0.4 → 0.2 → 0.6 → 0.6. Más samples no cura nada.

**Alargar las fases no era la cura, y lo dije mal.** Queda escrito porque el registro de una
predicción fallida vale exactamente lo mismo que el de una acertada — si no, prerregistrar no
sirve para nada.

## 3. LO QUE LOS DATOS SÍ SEÑALAN (y lo que NO voy a hacer con ello)

La **separación de medias es de 4 a 5 sigmas** en tres de las cuatro duraciones. El efecto medio de
la política contingente **existe y es grande**. Lo que falla es exigir **1.5× semilla por semilla**:
las razones individuales van de 1.07 a 2.35, y el umbral cae justo en medio de esa nube.

Diagnóstico honesto: **el problema es el criterio por-semilla, no el fenómeno.**

**Y no voy a tocar el umbral.** El prereg-36 lo prohíbe con todas las letras: *"mover el umbral
hasta que el control positivo pase sería fabricar el resultado: la vara se declararía buena por
construcción."* Escribí esa frase sin saber que iba a necesitarla, y ahora la necesito. Un criterio
distinto es **un instrumento distinto** y va en un prerregistro nuevo, con su predicción por
delante.

## 4. LA CONSECUENCIA, QUE SE ACEPTÓ POR ESCRITO ANTES DE CONOCERLA

El prereg-36 firmó los dos desenlaces por adelantado. Se cumplió el malo:

> *"Si NINGUNA lo logra: se escribe como resultado que las firmas conductuales no son medibles con
> este diseño, y el prereg-30 B queda cerrado en no concluyente de forma permanente hasta que
> alguien proponga otro instrumento."*

**Así queda.** El prereg-30 B está cerrado. No se vuelve a preguntar a Diego con esta vara.

Y conviene decir qué significa eso para lo que ya sabíamos: **"Diego no exhibe las firmas
conductuales" sigue sin poder afirmarse.** Probablemente sea cierto —no tiene política contingente
alguna— pero probablemente-cierto no es medido, y en este árbol solo entra lo medido.

## 5. EL ERROR DE DISEÑO ORIGINAL, PARA QUE NO VUELVA

El banco del prereg-30 aprobaba el control positivo con **una sola semilla** — la 2, que resulta ser
de las que funcionan a esa duración. **Un control positivo de una muestra no es un control
positivo: es una anécdota que aprueba.**

Ya no puede repetirse: el caso está congelado en el banco, **no simula nada**, y exige que con el
positivo en 2/5 la vara se declare NO usable. Si alguien vuelve a leer "una semilla pasó" como "el
instrumento funciona", el guardián grita.

## 6. PROPUESTA AL DIRECTOR (Regla 15)
1. **Cerrar formalmente el prereg-30 B** como no concluyente permanente. Ya está escrito así en el
   nodo H-001; esta acta lo sella.
2. **No prerregistrar todavía un instrumento nuevo.** Antes hay que responder a una pregunta que
   este acta deja servida y que no cuesta una corrida: *¿qué firma conductual tiene sentido medir
   en un cuerpo de tres articulaciones acopladas?* El criterio del 1.5× viene de un experimento con
   otro cuerpo y otra tarea. Copiarlo fue nuestra decisión, no un dato.
3. **Mantener el señuelo agitado en el banco.** Cazó un fallo real a la primera corrida y es barato.

## 7. TRAZA
- Prerregistro: `registros/prerregistro-36.md` (firmado 10-ago-2026, umbrales congelados allí).
- Código: `codigo/espejo2.py`, 9/9 casos de Regla 31.
- Datos crudos: `resultados/p36-calibracion-firmas/resumen.json`.
