# LAS 34 REGLAS, CON ESTRUCTURA — versión estructurada, 10 de agosto de 2026
**Pedido del director: *"cada regla debería tener estructura: la regla, el porqué, qué evita y su
objetivo... pero debe existir investigación científica que nos ayude a redactarlas mejor"*.**

**Esto NO reemplaza a `CIMIENTOS.md`.** Es su índice estructurado: la misma constitución, ordenada
para poder auditarla de un vistazo. El texto completo, con su historia, sigue donde estaba.

---

## LOS TRES PRINCIPIOS QUE LA INVESTIGACIÓN APORTA
La literatura sobre diseño de reglas y cumplimiento da tres, y los tres nos cambian algo:

**1. La RAZÓN importa más que el enunciado.** *La gente cumple de forma más consistente las reglas
que ENTIENDE que las reglas que solo CONOCE, y una regla que incluye su razón produce cumplimiento
más robusto y generalizable a situaciones nuevas.*
→ Es exactamente lo que el director propuso por su cuenta. **27 de nuestras 34 no dicen su razón.**

**2. FORMULAR EN POSITIVO.** *Las reglas que dicen qué SÍ hacer producen cumplimiento más fiable
que las que solo dicen qué no hacer.*
→ Casi todas las nuestras están en negativo ("prohibido", "jamás", "ningún"). Por eso esta tabla
añade una columna **OBJETIVO** en positivo, que antes no existía en ninguna.

**3. ESPECIFICIDAD CON HOLGURA.** *Suficientemente específicas para aplicarse de forma
determinista dentro de su alcance, suficientemente generales para cubrir casos no previstos.*
→ Es el equilibrio que nos falta: 17 reglas no dicen **cómo** se comprueban, así que no se aplican
de forma determinista — se aplican como uno se acuerde.

**Y hoy pagué esa factura.** Al construir G12 reflejos medí un acuerdo de 0.907 que parecía
excelente; la línea base tonta sacaba 0.887. **Incumplí la Regla 12 sin darme cuenta**, porque la
Regla 12 dice *qué* hacer y no *cómo se comprueba que lo hice*.

---

## LA TABLA

| # | LA REGLA | OBJETIVO (en positivo) | QUÉ EVITA | CÓMO SE COMPRUEBA |
|---|---|---|---|---|
| **1** | Datos, no teorías | usar solo lo que se midió | que una teoría heredada decida qué se busca | **NO MECANIZADA** |
| **2** | Los datos también están contaminados: exigir el nivel más crudo posible | partir del dato más crudo disponible | que el preprocesado de otro traiga sus supuestos dentro | auditoria_total.py |
| **3** | El descubridor no puede ser un modelo de lenguaje | descubrir con sistemas entrenados solo en los datos del experimento | importar toda la física humana por la puerta del lenguaje | auditoria_total.py |
| **4** | Prohibido nombrar antes de validar | nombrar solo lo ya validado | que un nombre familiar haga creer que ya entendemos | auditoria_total.py |
| **5** | El único juez es la predicción prospectiva | juzgar por predicción de datos ocultos | aprobar por ajuste bonito sobre lo ya visto | **NO MECANIZADA** |
| **6** | La simplicidad se mide en bits, no en elegancia | medir la simplicidad en bits | confundir elegancia con verdad | **NO MECANIZADA** |
| **7** | Reiniciar muchas veces y estudiar la diversidad | correr muchas semillas y estudiar su diversidad | tomar una corrida afortunada por un hallazgo | **NO MECANIZADA** |
| **8** | Registro inmutable y prerregistro | dejar registro inmutable y prerregistro previo | decidir el criterio después de ver el resultado | auditoria_total.py |
| **9** | Escalera de dificultad: ganarse cada peldaño | declarar cada supuesto del montaje | que un supuesto invisible sostenga la conclusión | **NO MECANIZADA** |
| **10** | La realidad tiene el veto | mantener separados los datos de entrenamiento y de juicio | juzgarse con lo que ya se estudió | **NO MECANIZADA** |
| **11** | Intentar destruir cada resultado antes de creerlo | intentar destruir cada resultado antes de creerlo | creer un patrón que también aparece en el ruido | auditoria_total.py, guardianes_de_guardianes.py |
| **12** | Todo resultado se mide contra una línea base tonta | medir contra una línea base tonta | celebrar un acierto que un tonto también consigue | pruebas.py |
| **13** | Criterios de abandono escritos de antemano | escribir de antemano cuándo se abandona | perseguir una idea muerta por no haber dicho cuándo parar | **NO MECANIZADA** |
| **14** | Replicabilidad total | hacer todo reproducible por otro | un resultado que solo existe en una máquina | **NO MECANIZADA** |
| **15** | La máquina propone, el humano decide | proponer con evidencia y decidir con firma | que una recomendación se vuelva hecho consumado | auditoria_total.py, coherencia.py |
| **16** | Prioridad demostrable y apertura | registrar prioridad con commits fechados | perder la autoría de lo que se pensó primero | auditoria_total.py |
| **17** | El proyecto debe ser operable por un no-programador | mantener el proyecto operable por un no-programador | que el director dependa de mí para entender su propio proyecto | auditoria_total.py |
| **18** | El árbol de conocimiento: nada se descubre suelto | hacer nacer cada corrida de una pregunta abierta | acumular resultados sueltos que no responden nada | **NO MECANIZADA** |
| **19** | El puente a la realidad: toda ley candidata debe poder morir en un experimento físico | subir la escalera de confianza hasta el experimento físico | llamar conocimiento a una compresión que solo vive en la computadora | auditoria_total.py |
| **20** | El camino inverso: de ley a tecnología | diseñar tecnología solo con leyes del árbol | colar intuición de ingeniería humana como si fuera nuestra | **NO MECANIZADA** |
| **21** | El mapa de anomalías: dónde cavar para contradecir | cavar donde la teoría humana deja residuos | buscar contradicciones opinando en vez de midiendo | guardianes_de_guardianes.py |
| **22** | Doble uso: el descubrimiento también se audita moralmente | revisar el doble uso antes de compartir | publicar algo peligroso sin haberlo pensado | guardianes_de_guardianes.py |
| **23** | El motor tampoco cree en sí mismo | someter los nodos viejos a las varas nuevas | un árbol que solo crece y nunca se poda | **NO MECANIZADA** |
| **24** | El científico del proyecto vive en el repositorio, no en un modelo | mantener al científico en el repositorio, no en un modelo | que el conocimiento viva en un sitio que no se puede auditar | **NO MECANIZADA** |
| **25** | El mundo ya está grabado: datos de video existentes | usar grabaciones reales con procedencia clara | datos de origen dudoso sosteniendo un nodo | auditoria_total.py |
| **26** | Ingeniería desde cero: los documentos que no existen | escribir los documentos que faltan antes de construir | construir sin saber qué se está construyendo | **NO MECANIZADA** |
| **27** | El comparador y el cortafuegos: cómo se corrige el conocimiento humano | mantener el cortafuegos del comparador | que la física humana entre por la puerta de atrás | auditoria_total.py, coherencia.py, metodo.py, pruebas.py, sanidad.py, temple.py |
| **28** | El bucle interior: automejora de las VARIABLES, jamás de los JUECES | automejorar las variables, jamás los jueces | que el ente ajuste su propia vara hasta aprobar | **NO MECANIZADA** |
| **29** | El conectoma: la mente ve TODAS sus hojas | dejar que la mente vea todas sus hojas | una mente ciega a su propia memoria | auditoria_total.py, coherencia.py |
| **30** | Automejora total POR PROPUESTA: código, conectoma y entendimiento | automejorar por propuesta con commit visible | código que se edita a sí mismo en silencio | pruebas.py, temple.py |
| **31** | Toda herramienta debe fallar donde no hay nada | hacer que toda herramienta falle donde no hay nada | una herramienta que encuentra algo hasta en un mundo vacío | auditoria_total.py, guardianes_de_guardianes.py, metodo.py, pruebas.py, sanidad.py |
| **32** | La autoauditoría permanente: todo interconectado, salvo lo que la mente no ve | autoauditar la casa en cada commit | que los documentos digan una cosa y el disco otra | auditoria_total.py, coherencia.py |
| **33** | La filogenia: el genoma solo cambia entre generaciones, jamás dentro de una vida | cambiar el genoma solo entre generaciones | que el ente se modifique a mitad de una vida y nada sea comparable | pruebas.py, sinapsis.py, temple.py |
| **34** | La frontera de la memoria: `arbol/` son sus HOJAS; los carteles humanos viven fuera | guardar en arbol/ solo las hojas del ente | que un cartel humano acabe donde el ente lo puede leer | coherencia.py |

---

## LO QUE ESTA TABLA DEJA A LA VISTA

**14 de 34 reglas no tienen ningún guardián que las nombre.** No significa que se incumplan:
significa que **si se incumplieran, nada avisaría**. Son las que dependen enteramente de mi
disciplina, y ahora se sabe cuáles son:

> **1, 5, 6, 7, 9, 10, 13, 14, 18, 20, 23, 24, 26, 28**

Entre ellas hay tres que me preocupan de verdad, y digo por qué:
- **R13 — criterios de abandono escritos de antemano.** Llevamos **tres** veredictos de *"no
  concluyente"* decididos después de ver los datos. Ninguno fue deshonesto, pero ninguno estaba
  escrito antes.
- **R18 — cada corrida nace de una pregunta abierta.** Hoy encolo estudios porque se me ocurren.
- **R23 — los nodos viejos se re-someten a las varas nuevas.** Lo hicimos una vez, en agosto, y
  porque el director lo pidió.

## LAS TRES FUSIONES PROPUESTAS (34 → 31)
| Fusión | Por qué |
|---|---|
| **R11 + R12** | son la misma idea —intentar destruir el resultado antes de creerlo— y separarlas hizo que cumpliera una mientras incumplía la otra |
| **R28 + R30** | R28 es el caso particular de R30 |
| **R7 + R14** | reiniciar muchas veces y ser reproducible son la misma exigencia |

## LOS CUATRO ENDURECIMIENTOS PROPUESTOS, todos por daño ya sufrido
| Regla | Endurecimiento | Daño |
|---|---|---|
| **R12** | línea base tonta **obligatoria y automática** en todo puntaje | 0.907 parecía bueno; el tonto sacaba 0.887 |
| **R31** | fallar con vacío **Y** aprobar con control positivo | un caso mío aprobaba con una medida ciega |
| **R13** | criterios de abandono **con número**, no con adjetivos | tres "no concluyente" decididos a posteriori |
| **R19** | ningún nodo pasa de nivel 1 sin **datos que nadie ha visto** | 40 prerregistros, cero nodos fuera del nivel 1 |

## LO QUE NECESITO DEL DIRECTOR
**No toco `CIMIENTOS.md` sin su palabra** — cambiar las reglas es lo único que la enmienda de la
Regla 15 dejó explícitamente fuera de mi alcance. Con una palabra por punto:
1. **¿Aplico la estructura de cuatro campos al texto de las 34?**
2. **¿Aplico las 3 fusiones?**
3. **¿Aplico los 4 endurecimientos?**
4. **¿Construyo guardián para las 14 sin mecanizar**, o las marcamos como *"depende de la
   disciplina del orquestador"* y se acepta?
