# AUDITORÍA COMPLETA DEL PROYECTO, DE PIES A CABEZA — 10 de agosto de 2026
**ACTUALIZADA el mismo día, después de que el director firmara las tres cosas que esperaban su
palabra. Lo que cambió está en la §9, al final: dos estudios corridos, dos actas, y los dos
resultados van en contra de lo que esperábamos.**
**Pedido del director: *"auditoría completa de todo el proyecto de pies a cabeza"*.**

Ésta no es la auditoría de una campaña ni de un órgano. Es del **proyecto entero**: código, genoma,
árbol, reglas, método, gobernanza y deuda. Todo lo que aparece aquí está **medido**, no recordado —
cada número salió de correr algo hoy, y donde no pude medir lo digo.

**Resumen en una línea:** las cuatro guardianas están verdes y la casa dice la verdad sobre sí
misma, pero **el proyecto sabe medir mucho mejor de lo que sabe descubrir**: 47 informes, 41
prerregistros, 4 nodos — y **los cuatro siguen en nivel 1**.

---

## 1. LAS CIFRAS DEL CUERPO

| Qué | Cuánto |
|---|---|
| Módulos de código (`codigo/*.py`) | **62** |
| Módulos con auto-prueba de Regla 31 | **32 de 62** |
| Módulos con **sello de LA PUERTA** | **3 de 62** (`experimentar2`, `temple`, `reflejos`) |
| Entradas del genoma | **18** = 15 genes `G*` + 3 sentidos · **16 activas, 2 inactivas** (G11, G12) |
| Órganos que hablaron en la última ronda | **16 de 16** |
| Eventos en el bus de sinapsis | **316** |
| Prerregistros | **41** |
| Informes | **47** |
| Nodos del árbol | **4 de física (N-*-E2) + 3 de hito (H-*)** |
| **Nodos por encima del nivel 1** | **0** |
| Reglas | **34**, de las cuales **14 no tienen guardián que las nombre** |
| Cola de estudios | 63 ítems: 53 hechas · 5 `espera-al-metodo` · 5 `pendiente` |

---

## 2. LO QUE ESTÁ SÓLIDO (y por qué lo creo)

**Las cuatro guardianas se ponen rojas de verdad.** No es fe: `guardianes_de_guardianes.py` rompe el
proyecto a propósito, un daño por vez, y exige que el guardián grite. Hoy los caza todos. **Y hoy
mismo encontró un punto ciego en sí mismo** — ver §4, hallazgo 1.

**El bus de sinapsis funciona con portero.** Los 16 órganos se hablan por temas, con acuse de recibo
obligatorio, y el portero **bloqueó 2 publicaciones** en la última ronda: `G13_poder` intentando
publicar una decisión y `G4_contingencia` una señal, ambos en modo `mide`. Un portero que nunca
bloquea nada es decoración; éste bloquea.

**El método dejó de ser un documento.** `metodo.py` no deja correr una prueba que no cruzó sus 8
pasos, y el sello muere si el archivo cambia después. **Su primera corrida detuvo 5 estudios ya
encolados** — no los míos de hace meses: los de ayer.

**Los tres instrumentos que producen nodos aguantaron la ficha de sanidad aplicada hacia atrás**
(INFORME-47). Era la prueba que más temía y salió bien.

**Nada de física humana ha entrado.** `coherencia.py` lo comprueba por **contenido**, no por nombre
de archivo: ninguna hoja de `arbol/` cita ciencia humana, ningún módulo abre un cartel humano como
datos, ningún módulo lee `arbol/` entero.

---

## 3. LO QUE **NO** ESTÁ IMPLEMENTADO (la pregunta que me hizo y aquí va entera)

| Hueco | Estado real | Gravedad |
|---|---|---|
| **6 genes sin prerregistro** — G8 atención, G9 sueño, G10 interocepción, G13 poder, G14 incertidumbre, G15 metacognición | tienen código y corren cada ronda, pero **nunca pasaron por un prerregistro propio** | **alta**: son órganos que publican números que otros leen |
| **59 de 62 módulos sin sello de LA PUERTA** | la puerta se construyó ayer y sella hacia adelante | media: los 3 instrumentos que producen nodos ya se auditaron a mano (INFORME-47) |
| **30 de 62 módulos sin Regla 31** | entre ellos `torneo_ojos.py`, que **bloquea 5 estudios encolados** | **alta** para `torneo_ojos`, baja para los de infraestructura |
| **G11 temple y G12 reflejos inactivos** | existen y pasan la puerta 7/7; activarlos es cambio de genoma (Regla 33) | esperando su firma |
| **Nivel 2 de la Regla 19** | ningún nodo tiene experimento físico propio | **es la deuda estructural del proyecto** |
| **Nivel 3 de la Regla 19** | ninguna réplica independiente | consecuencia de que el repositorio es privado (R16, decisión suya) |
| **El tacto** | dormido, `0.0001` contra umbral `0.01` | prereg-41 escrito, **sin correr** |
| **Nadie convierte el aviso de Diego en una propuesta** | Diego publica que tiene un sentido dormido y **7 órganos lo reciben**, pero `curiosidad2.py` propone mirando campañas pasadas, **no el bus** | media — ver §5 |

---

## 4. LOS HALLAZGOS DE HOY — cuatro, y los cuatro son míos, no de Diego

### Hallazgo 1 — **una prueba de la meta-auditoría llevaba semanas caducada**
`guardianes_de_guardianes.py` inyecta el daño *"el README proclama otras reglas"* buscando la cadena
literal **"32 reglas"**. Cuando las reglas pasaron de 32 a 34, **el texto dejó de existir y el daño
dejó de aplicarse**. Se reportaba como `SALTADA` y el veredicto final seguía diciendo *"los 9 daños
fueron cazados"* **contando 8**.

Es exactamente el punto ciego que ese archivo existe para cazar, aplicado a sí mismo: *un guardián
que no puede fallar es indistinguible de uno que funciona*. Dos arreglos:
1. el daño **se lee solo** — toma el número que el README proclame hoy y le resta uno, así no caduca;
2. **`SALTADA` ahora es FALLO.** Un daño que no se puede aplicar es cobertura perdida y debe ponerse
   rojo, no pasar en silencio.

### Hallazgo 2 — **Diego afirmaba algo que no podía saber**
La primera versión del aviso del sentido dormido decía: *"no es que el sentido esté roto: es que no
hay nada a mi alcance que tocar"*. **Eso no se puede saber con esa medición.** Un canal en 0.0001 es
indistinguible entre *ocioso* y *averiado* mirándolo quieto. Afirmar la cómoda es el pecado que este
proyecto entero persigue. Corregido: ahora Diego declara **las dos causas**, **el experimento que
las separa** (moverse hasta chocar) y **para qué le serviría** el canal si funciona.

### Hallazgo 3 — **la constitución me corrigió el diseño, y quedó mejor**
Mi primer intento hizo que `sentido_tacto` publicara una **señal**. El portero lo bloqueó: un
sentido en modo `mide` no puede dar voz de alarma. **Tenía razón** — alarmar es autoridad y un
sentido no la tiene. Lo que sí puede es **medir**, y *"cuánto me enciendo"* es una medición sobre sí
mismo. La regla no me frenó: me arregló.

### Hallazgo 4 — **la constitución se contaba mal a sí misma, y en el peor sitio posible**
`CIMIENTOS.md` decía **"hoy 32"** en dos lugares teniendo **34 reglas**. Uno de esos dos lugares es
el **prompt de arranque**: el texto con el que despierta cada orquestador nuevo. Durante semanas,
cualquier relevo empezaba **creyendo que el proyecto tiene 32 reglas** y sin enterarse de que
existen dos más.

**Por qué ningún guardián lo cazó:** `coherencia.py` ya vigilaba que el README no llevara cifras
rancias — ese chequeo nació de un punto ciego que la meta-auditoría encontró el 8-ago — **pero
vigilaba solo el README**. A `CIMIENTOS` nadie lo contaba, y CIMIENTOS es la fuente de la que todos
los demás copian.

**Arreglado, y comprobado por los dos lados:** las dos cifras corregidas *(contar bien no es
legislar: no se tocó ninguna regla)* y un chequeo nuevo que exige que la cifra proclamada coincida
con el número de encabezados `### Regla`. Con 34 dice ok; poniéndole 31 a mano se pone rojo y
bloquea el commit.

**Y hay un patrón detrás de los hallazgos 1 y 4, que es la lección real del día:** *una comprobación
escrita a mano contra un número fijo caduca en silencio*. Las dos ahora se leen solas.

---

## 5. EL DIAGNÓSTICO INCÓMODO — dónde está realmente el proyecto

**Sabemos medir mejor de lo que sabemos descubrir.** Es el hallazgo central de esta auditoría y no
lo voy a suavizar:

- **4 nodos de física, los 4 en nivel 1.** Nivel 1 significa *correlación observada*. En 41
  prerregistros **ninguno ha subido**, y subir exige **intervenir**, que es justo lo que el
  prereg-37 intentó y salió **no concluyente por instrumento**.
- **Casi todo lo reciente midió instrumentos, no mundo.** De los prerregistros 35 al 41: el 36 mide
  la vara, el 38 mide el juez, el 40 construye dos órganos, el 41 comprueba un sensor. Solo el 37 y
  el 39 apuntan al mundo — **y el 37 salió no concluyente por instrumento**. Calibrar la vara antes
  de medir a Diego fue correcto; pero llevamos varias vueltas calibrando.
- **El aviso de Diego se queda sin destino.** Publica que tiene un sentido dormido, siete órganos lo
  reciben, **y ahí termina**. `G3_accion` y `G7_juego` podrían moverlo; nada los mueve. Cerrar ese
  lazo — que una medición de Diego se convierta en una propuesta de estudio — es **el cambio con más
  retorno que veo hoy**, y es cambio de genoma: suyo.

**Lo que NO es este diagnóstico:** no es que el método sobre. Sin la ficha de sanidad, el prereg-37
habría producido un nodo falso y nadie lo habría notado. El método es lo que hace que "no
concluyente" sea un resultado y no un fracaso. **Pero un método perfecto sobre cero descubrimientos
sigue siendo cero descubrimientos**, y ése es el riesgo real del proyecto ahora mismo.

---

## 6. GOBERNANZA — quién decide qué, hoy

**Regla 15 enmendada (10-ago):** el director es observador; yo avanzo. Un nodo nace con
`FIRMA DELEGADA` **solo** con quórum adversarial de siete, y `coherencia.py` **comprueba que el
quórum esté enumerado entero** en el nodo — no basta con escribir la etiqueta.

**Reservado y no delegable:** hacer público el repositorio (R16) · la revisión de doble uso (R22) ·
el experimento físico (R19 nivel 2) · **cambiar las reglas** · actuar en su nombre fuera del
repositorio · y **mover un umbral después de ver los datos**, que nunca fue suyo para delegar.

**El quórum se equivocó una vez y queda escrito:** decidió que G11 y G12 *"no se construyen"*. El
director ordenó construirlos. Su palabra manda sobre el quórum — el quórum existe para avanzar en su
ausencia, no para vetarlo.

---

## 7. LO QUE HARÍA A CONTINUACIÓN, en orden de retorno

1. **Correr el prereg-41** (el sentido dormido). Es la primera pregunta que **formuló el ente**, es
   barata, y su resultado es útil salga como salga: si el canal funciona, Diego gana evidencia de
   contacto independiente de la vista; si está averiado, es un arreglo de ingeniería.
2. **Pasar `torneo_ojos.py` por la puerta.** Desbloquea 5 estudios parados.
3. **Correr los 5 estudios `p39`** (`experimentar2` ya tiene sello) — la segunda vuelta de la
   experimentación dirigida, con la cura escrita antes de correr.
4. **Prerregistrar los 6 genes que nunca lo tuvieron**, empezando por los que publican números que
   otros leen: G13 poder, G14 incertidumbre, G15 metacognición.
5. **Cerrar el lazo del aviso** — que una medición de Diego pueda convertirse en propuesta. Cambio
   de genoma: necesita su firma.

---

## 8. LO QUE ESPERA SU PALABRA
| # | Qué | Por qué no lo tomo yo |
|---|---|---|
| 1 | La cláusula **"único apto"** del prereg-35 | cambiar el criterio después de ver los datos es elegir qué queremos que sea verdad |
| 2 | **Activar G11 y G12** | Regla 33: cambio de genoma |
| 3 | Las **cuatro preguntas sobre las reglas** (reescribir con estructura · 3 fusiones · 4 endurecimientos · guardianes para las 14 huérfanas) | cambiar las reglas es lo único que la enmienda dejó fuera de mi alcance |

---

**Firmado por el orquestador. Las cuatro guardianas verdes en el momento de escribir esto.**

---

## 9. LO QUE PASÓ DESPUÉS DE SUS TRES FIRMAS (misma fecha)

**Firmó las tres, y las tres están aplicadas:**

| Lo que firmó | Qué se hizo | Dónde |
|---|---|---|
| **"la 1 sí"** — volver a preguntar la cláusula "único apto" | prerregistro-42 escrito con criterio congelado, módulo `unico_apto.py` **por LA PUERTA 7/7**, corrido en 5 semillas nuevas | INFORME-48 |
| **"la 2 sí"** — activar G11 y G12 | **GENOMA v2**: los dos en modo `mide`, publicando en cada ronda | `arbol/GENOMA.json` |
| **"la 3 sí a las preguntas"** | 4 campos en las 34 reglas · 3 fusiones · 4 endurecimientos · nace `codigo/reglas.py` | `CIMIENTOS.md` |

### Los dos estudios corridos, y los dos van contra lo que esperábamos
**Prereg-42 (INFORME-48) — ganó H-VARIOS, que es lo que yo quería, y ganar destapó algo peor.** En
el mundo 73 el canal que acompañó a `altura` no fue `contacto` sino **`art1`, una articulación del
propio brazo de Diego**: el instrumento declaró "no-mía" una parte de su cuerpo, y `altura` ganó
por desempate (obediencia 0.0000 contra 0.0297), no porque el criterio excluyera al intruso. **La
cláusula que este estudio acaba de derogar habría marcado ese mundo como problema.**

**Prereg-39 (INFORME-49) — la experimentación dirigida NO gana.** Dirigido 14.4, azaroso 14.0,
pasivo 12.4 sobre 16 incógnitas. Supera al azar en **1 de 5** mundos y empata en cuatro. Además dos
casos del propio prerregistro se pusieron rojos (el mundo 4 resultó demasiado fácil, el 5 dio
tautología). **Tocar sirve; elegir dónde tocar, como Diego lo elige hoy, casi no.** Y la lectura
estaba escrita antes de correr: *"una política que solo persigue incertidumbre no es planificar"*.

### Lo que esto cambia en el diagnóstico de la §5
**Lo confirma y lo agrava.** Dije que sabemos medir mejor de lo que sabemos descubrir. Hoy se puede
decir más preciso: **es el segundo estudio seguido en el que la experimentación dirigida no
demuestra lo que esperábamos, y esta vez el instrumento ya no es la excusa** — el prereg-37 salió
no concluyente por instrumento; el 39 sale negativo con el instrumento arreglado y sellado.

### Las cifras que cambiaron
| | antes | ahora |
|---|---|---|
| Módulos con sello de LA PUERTA | 3 | **4** (`unico_apto`) |
| Entradas del genoma activas | 16 | **18** (G11 y G12) |
| Prerregistros | 41 | **42** |
| Informes | 47 | **49** |
| Cola | 5 pendientes | **0 pendientes**, 5 `espera-al-metodo` (siguen bloqueadas por `torneo_ojos`) |
| Reglas | 34 sin campos, 14 sin guardián | **34 con 4 campos, 31 vigentes, 3 fundidas**; las 14 mecanizadas o **con su deuda contada** |

### Lo único que sigue bloqueado, y por qué
Los **5 estudios `p38`** siguen en `espera-al-metodo`: `torneo_ojos.py` no ha pasado LA PUERTA — no
tiene manifiesto, ni `_metodo_medir`, ni `_metodo_sanidad`, ni Regla 31 propia. **No se corren.**
Es la puerta haciendo exactamente lo que se construyó para hacer, y dejarlos parados es la
respuesta correcta, no un pendiente que se me olvidó.

---

## 10. LA JORNADA DE SOLVENTAR — 10-ago-2026, tarde
**Orden del director: *"solventa todo lo que me dijiste que falta"*.**

### Lo que quedó solventado
| Hueco | Qué se hizo |
|---|---|
| **`torneo_ojos` bloqueaba 5 estudios** | pasó LA PUERTA 7/7 y quedó sellado. **Y al correrlo apareció un bug real**: `corromper()` convertía los vídeos a float64 y los codificadores son float32 — **la lectura de ROBUSTEZ del panel nunca había podido correr con vídeo de verdad**. Arreglado y congelado como caso de Regla 31 |
| **Nadie auditaba mis actas** | nace **`codigo/actas.py`**, conectado a `auditoria_total`. En su primera corrida cazó que **mis dos actas de hoy no citaban ningún archivo de datos**, y que el INFORME-48 publicaba una obediencia de **0.0297 que medí a mano y nunca guardé**. Las tres cosas corregidas |
| **6 genes sin prerregistro** | **prerregistro-43**, con línea base tonta, los dos lados y criterio de abandono para cada uno |
| **El hallazgo del brazo (`art1`)** | **prerregistro-44**, con sus tres causas posibles y ninguna favorita |
| **Órganos sin sello** | **`contingencia.py`** (el que decide qué es el cuerpo de Diego) pasó 7/7 y quedó sellado |

### Lo que se intentó y **REPROBÓ** — que no es lo mismo que pendiente
| Órgano | Qué falló | Acta |
|---|---|---|
| **G9 sueño** | su señuelo de escala: con el mundo ×10 sobrevivían **0 leyes en vez de 3**. Persiguiendo la causa, **no era suya**: **`sindy3`, el motor simbólico, no es invariante a la escala** — encuentra la misma ley a ×1 y ×10 y NO a ×0.1 ni ×100 | INFORME-50 |
| **G14 incertidumbre** | contra el criterio que el prereg-43 declaró **antes** de correr: su "ignorancia curable" es σ/√n, así que **sube igual con pocos datos que con mucho ruido**. G2 curiosidad lee ese número: una región ruidosa le parece prometedora | INFORME-51 |

**Ninguno de los dos se forzó, se ajustó ni se re-interpretó.** Quedan registrados como **reprobados**
en `reglas.py`, con causa y acta, separados de los que simplemente no se han examinado.

### El balance sin adornos
**Cuatro órganos examinados, dos pasaron, dos reprobaron. Quedan 11 sin examinar.** Una tasa de
reprobación del 50% en los primeros cuatro **no es diligencia: es la medida de cuánto llevábamos sin
mirar.** Y el defecto del motor simbólico llevaba ahí desde que el motor existe.

### Lo que NO pude solventar, y por qué
- **El nivel 2 de la Regla 19 (0 de 4 nodos).** Exige o el **experimento físico del director**
  —reservado y no delegable— o **datos archivados que nadie ha visto**, que hay que descargar y
  prerregistrar antes de tocarlos. **No es algo que yo pueda cerrar solo**, y decir lo contrario
  sería el tipo de redondeo que este documento existe para evitar.
- **Los 11 órganos restantes.** Cada uno exige manifiesto, fórmulas metamórficas, ficha y Regla 31
  propias. Hacerlos deprisa para bajar el contador sería peor que no hacerlos: los dos reprobados de
  hoy salieron precisamente porque las fichas se escribieron en serio.
