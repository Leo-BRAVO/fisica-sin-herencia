# INFORME-47 — LA FICHA DE SANIDAD APLICADA HACIA ATRÁS: los tres instrumentos que ya dieron nodos AGUANTAN
**10 de agosto de 2026.** Pedido por el director: *"utilízalo contra las pruebas ya realizadas,
veamos qué resultados nos traen"*.

**Resultado en una línea: los tres instrumentos de los que salieron nodos pasan la ficha. Los
errores que encontró están todos en la ficha misma y en módulos ya cerrados.**

---

## 1. SOPORTE (prereg-29/35) — de aquí salió el nodo **H-002**

| Comprobación | Resultado |
|---|---|
| ¿Clasifica bien qué es su cuerpo? | **3 aciertos positivos, 4 negativos, CERO falsos** |
| ¿El señuelo de ruido queda fuera? | **Sí** — aptos: solo `altura` |
| Tramoya declarada | **1.67%** de la señal, declarada y excluida |
| Cocientes con piso | sí, desde el 9-ago |

**El instrumento sabe exactamente cuáles de los siete canales son su cuerpo y cuáles no, sin que
nadie se lo diga.** El nodo H-002 se sostiene.

## 2. ESPEJO2 (prereg-30) — de aquí salió el nodo **H-001**

| Comprobación | Resultado |
|---|---|
| ¿Clasifica bien qué cuerpo es suyo? | **1 acierto positivo, 1 negativo, CERO falsos** |
| ¿Los dos cuerpos son de verdad distintos? | **Sí** |
| Margen sobre el nulo | propio **+0.227** vs nulo 0.0071; ajeno **−0.222** vs nulo 0.0061 |

**Treinta veces el nulo, en las dos direcciones.** El nodo H-001 se sostiene.

## 3. OBSERVADOR PASIVO (prereg-32/35) — el que produjo el **empate** de H-002

Aquí la ficha **gritó**, y al mirarlo resultó ser **una falsa alarma que enseñó algo**.

El detector avisó: *"encarnado y pasivo-propio observaron exactamente lo mismo"*. Y es cierto — **a
propósito**. Ese es el diseño entero del experimento: misma dieta sensorial, y la **única**
diferencia es el acceso a las propias órdenes.

Lo que verifiqué en su lugar, que es lo que de verdad importa:
- **la copia eferente ENTRA al modelo del encarnado:** sí;
- **en el examen su copia eferente es cero** (son escenas que no actuó): sí;
- **el pasivo-ajeno sí ve datos distintos:** sí.

**El empate de H-002 no era una tautología.** Lo que separaba a las dos condiciones estaba puesto y
comprobado.

### Y de aquí salió la mejora más fina de la ficha
Compartir datos entre dos condiciones **es legítimo si otra cosa las separa Y esa otra cosa está
comprobada**. La ficha ahora distingue tres situaciones que a simple vista son idénticas:

| Situación | Veredicto |
|---|---|
| comparten datos y **nada** se declara que las separe | **FALLO** — tautología (fue el prereg-37) |
| comparten datos, se declara qué las separa, **sin probarlo** | **FALLO** — una promesa no es una prueba |
| comparten datos, se declara y **está probado** | **APRUEBA** (es el prereg-32) |

---

## 4. LO QUE LA FICHA ENCONTRÓ DE VERDAD, y dónde estaba

**Cinco hallazgos, y CUATRO estaban en la ficha misma.** Eso no es una casualidad incómoda: es la
prueba de que el problema es de método y no de un módulo concreto.

| # | Dónde | Qué |
|---|---|---|
| 1 | **en la ficha** | comparaba correlaciones brutas: dos verdades correlacionadas entre sí hacían parecer contaminada una lectura perfecta *(tipo A)* |
| 2 | **en la ficha** | su correlación parcial dividía por casi cero justo en el caso bueno *(tipo D)* |
| 3 | **en la ficha** | medía **dirección** en vez de **tamaño**: una miga alineada daba 0.94 *(tipo A)* |
| 4 | **en la ficha** | `list(cortes or [])` reventaba con un array de numpy *(el mismo descuido que persigue)* |
| 5 | en `sueno.py` | un guardián calculado y tirado bajo un comentario que decía lo contrario *(tipo E)* |

Y una falsa alarma sobre `soporte.py` que **también era mía**: apliqué el estadístico de lecturas
continuas a un instrumento que **clasifica por umbral**. Con la prueba correcta —¿acierta, y por
los dos lados?— soporte pasa impecable.

**Esa es la lección que el director había anticipado: *cada experimento es distinto*.** Una ficha
que aplica el mismo estadístico a todo produce alarmas falsas, y una alarma falsa cuesta tanto como
un error: hace desconfiar de lo que funciona.

## 5. LO QUE ESTO SIGNIFICA PARA LA PREGUNTA DEL DIRECTOR
Él lo dijo así: *"parece que el culpable es Diego y no es así"*. Tenía razón, y ahora hay números:

- **Los tres instrumentos que produjeron nodos aguantan la auditoría.** Lo que Diego consiguió,
  lo consiguió de verdad.
- **Los estudios que salieron mal salieron mal por MI instrumento, no por él:** el torneo de ojos
  midió su propio suelo; las firmas conductuales tenían una vara que fallaba 3 de 5 veces sobre un
  caso conocido; la primera experimentación dirigida comparaba una condición contra sí misma.
- **Ninguno de esos tres dice nada sobre lo que Diego puede o no puede hacer.** Están correctamente
  escritos como **NO CONCLUYENTE POR INSTRUMENTO**, que es una tercera cosa y tiene su nombre.

## 6. TRAZA
- `codigo/sanidad.py` — la ficha, con su meta-prueba de nueve casos.
- `registros/METODO.md` — los seis pasos, y qué queda mecanizado y qué no.
- Corridas de esta auditoría: sobre `soporte.py`, `espejo2.py` y `observador_pasivo.py` con las
  semillas de sus corridas oficiales.
