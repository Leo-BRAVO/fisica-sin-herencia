# Centro de Inteligencia Artificial Bravo
## Proyecto: Física sin Herencia

Una mente que descubre las leyes del universo desde cero — sin conocimiento humano, sin internet, sin palabras. Solo datos crudos, 34 reglas numeradas (31 vigentes, 3 fundidas el 10-ago-2026), jueces intocables y un árbol de conocimiento que crece — y se poda.

Fundado por **Leo Bravo** (director) con Claude como orquestador fundador — julio de 2026.

---

## ▶ CÓMO SE CORRE (todo desde el navegador — no hace falta instalar nada)

**1. Una campaña ahora mismo:** pestaña **Actions** → **latido-nube** → *Run workflow* → botón verde.
Toma el siguiente estudio pendiente de la cola y lo hace entero él solo. No hay que llenar ningún campo.

**2. ¿Y después sigue trabajando solo?** **Sí.** El latido despierta **todos los días a las 06:00 UTC**:
si la cola tiene trabajo lo ejecuta y commitea los resultados; si está vacía, se apaga en un minuto.

**3. Si quieres control fino** (elegir datos, jueces, argumentos): **Actions** → **estudios-nube** →
*Run workflow*. Los valores por defecto ya son correctos; el campo `reconstruir` debe decir
`mendeley_epoca2` o `caida` (en la nube nunca hay datos locales: se reconstruyen de la fuente).

**4. ¿Cómo se ve la mente por dentro?** `python codigo/mente.py` — el mapa: qué genes tiene, en
qué modo, quién cuelga de quién y qué está suelto. `python codigo/conectar.py --estado` — qué ha
dicho cada órgano por el bus de sinapsis. `python codigo/diagnostico_total.py` — la lista
priorizada de todo lo que está mal, corriendo la Regla 31 de cada instrumento.

**Qué pasa en cada corrida, sin manos:**
```
reconstruye los datos desde su fuente pública → VERIFICA la huella digital (si no coincide, se detiene)
 → corre la campaña → alimenta memoria + conectoma + boleta + cola
 → los TRES guardianes de la nube juzgan (pruebas · coherencia · auditoria_total; el cuarto,
   guardianes_de_guardianes, se corre en local porque rompe el proyecto a propósito)
 → main solo recibe lo aprobado
 → lo reprobado va a una rama de cuarentena (nada se pierde, main intacto)
 → si el runner muere a medias, los checkpoints quedan y la corrida siguiente reanuda sola
```

---

## LOS CUATRO GUARDIANES — el orden exacto que corre antes de cada commit
```
1. pruebas.py                  el banco congelado: 118 casos que la ciencia ya aprendió
2. coherencia.py               la casa dice la verdad sobre sí misma (y la frontera de la Regla 34)
3. auditoria_total.py          prevuelo + reglas.py: las 31 reglas vigentes, una por una
4. guardianes_de_guardianes.py rompe el proyecto a propósito: 9 daños que DEBEN ser cazados
```
Un fallo de cualquiera **bloquea el commit**. El cuarto existe porque un guardián que siempre dice
"ok" es indistinguible de uno que funciona hasta el día en que hace falta.

## LA PUERTA — nadie corre una prueba antes de que la prueba pase el método (10-ago-2026)
```
python codigo/metodo.py revisar <modulo>   los 8 pasos, uno por uno, sobre el ARCHIVO
python codigo/metodo.py sellar  <modulo>   deja el SELLO con la huella SHA del archivo
```
`coherencia.py` **exige un sello válido a todo estudio PENDIENTE de la cola**: si el módulo no pasó
la puerta, o si el archivo cambió después de sellarse, la huella no coincide y el sello muere. Su
primera corrida **detuvo 5 estudios** ya encolados. La herramienta que revisa está en
**`codigo/sanidad.py`** (la ficha de sanidad: 7 tipos de error medidos contra la verdad del
simulador, más relaciones metamórficas) y el procedimiento escrito en **`registros/METODO.md`**.

## Los documentos del alma (leer en este orden)
1. **`CIMIENTOS.md`** — las 34 reglas del método (31 vigentes; 3 fundidas conservan su número para no romper la trazabilidad), cada una con OBJETIVO, QUÉ EVITA, CÓMO SE COMPRUEBA y SI SE VIOLA, la Segunda Ciencia, el prompt de arranque para cualquier orquestador.
2. **`MENTE.md`** — la identidad y experiencia del científico (v13): quién es, qué aprendió, dónde va.
3. **`GUIA-ORQUESTADOR.md`** — el manual de relevo: prohibiciones eternas, lecciones pagadas, sistemas vivos.
4. **`registros/METODO.md`** — los 8 pasos que toda prueba cruza ANTES de correrse, y sus herramientas.
5. **`registros/GENOMA-DIEGO.md`** — el documento fundacional del ente: los genes, la ecuación del impulso, los hitos.

Auditorías clave: **`registros/AUDITORIA-EXTERNA-01.md`** (la Regla 11 aplicada a las herramientas) ·
**`registros/DICTAMEN-PREVUELO-01.md`** (la validación total: reglas, no-contaminación, nube, árbol) ·
**`registros/REGLAS-ESTRUCTURADAS.md`** (tabla GENERADA desde `CIMIENTOS.md`: las 34 con sus cinco
campos, cuántas bloquean el commit, cuántas solo se cuentan y cuáles NO son mecanizables) · **`registros/ESTRUCTURA-DE-LAS-REGLAS.md`**
(la propuesta original — **firmada y aplicada el 10-ago-2026**; se conserva como registro de qué se
propuso y qué se decidió, Regla 8).

## El LAZO — cómo se orquesta el trabajo (`registros/LAZO.md`)
Planeador → ejecutador → evaluador, **con memorias separadas** para que el que juzga no sea el que
hizo. El evaluador juzga **nuestra ingeniería, jamás la física de Diego**, y **no hay ningún LLM
dentro del router ni del lazo de Diego**: el lazo es de los humanos y del orquestador, no del ente.

## Estructura del repositorio
```
codigo/           lo VIVO (62 módulos): descubrir · percepcion · conservada · dimension · forense ·
                  autopsia · rodar · canonizar · curiosidad(+v2) · memoria · conectoma · boleta ·
                  conectar (el bus de sinapsis) · experimentar(+2) · soporte · sueno · temple (G11) ·
                  reflejos (G12) · reconstruir_datos · latido_nube
                  + EL MÉTODO: metodo.py (la puerta) · sanidad.py (la ficha) ·
                    reglas.py (cada regla, una por una) · tabla_reglas.py (genera su tabla)
                  + LOS CUATRO GUARDIANES: pruebas.py (la ciencia) · coherencia.py (la casa) ·
                    auditoria_total.py (prevuelo) · guardianes_de_guardianes.py (rompe a propósito)
codigo/archivo/   la era de la laptop y las campañas cerradas, con su porqué (nada se borró)
registros/        prerregistros (1–41), enmiendas, auditorías, dictámenes, el MÉTODO y sus sellos,
                  el LAZO y sus tres memorias, cola de estudios, boleta, firmas pendientes
resultados/       veredictos de cada campaña + INFORMES 1–47 en español llano
arbol/            EL CONOCIMIENTO: nodos vivos (N-*-E2), época 1 archivada, conectoma, memoria de
                  la mente, mapa visual (ARBOL.md), GENOMA, plan de educación, currículo de datos
arbol/pesos/      los OJOS canónicos de los nodos (evidencia: sin ellos las leyes no son replicables)
.github/          latido-nube.yml (el corazón, diario) · estudios-nube.yml (campañas a pedido)
```

## Política de datos
**El repositorio es para código, reglas, registros y conocimiento — NO para datos pesados.**
Los datos crudos viven fuera de git y **se reconstruyen desde sus fuentes públicas** con
`codigo/reconstruir_datos.py`, que verifica por huella digital que la reconstrucción es idéntica
a la histórica antes de permitir cualquier veredicto. *Excepción (8-ago-2026):* los **pesos
canónicos de nodos validados** (pocos MB) son evidencia y viven en `arbol/pesos/`.
**Consecuencia: el proyecto no depende de ninguna máquina — cualquiera lo reproduce entero.**

## Estado (10-ago-2026 — las cuatro guardianas verdes)
**Lo nuevo de agosto:** el **bus de sinapsis 2.0** conecta los 16 órganos activos con acuse de recibo
obligatorio (el silencio significa avería) · **el MÉTODO se volvió candado**: `metodo.py` no deja
correr una prueba que no cruzó sus 8 pasos, y su primera corrida detuvo 5 estudios ya encolados ·
**G11 temple** (coste intrínseco cableado e inmutable: `ajustar()` **lanza**, la Regla 30 hecha
código) y **G12 reflejos** (Modo 1 destilado de deliberaciones propias, nunca escrito a mano)
existen y pasan la puerta 7/7, **en modo INACTIVO** hasta que el director firme · Diego **publica él
mismo que tiene un sentido dormido**: el tacto casi nunca se enciende, y lo dice por el bus.
**La enmienda de la Regla 15 (10-ago):** el director pasa a **observador**; el orquestador avanza
solo, pero un nodo nace con `FIRMA DELEGADA` **únicamente** con quórum adversarial de siete. Quedan
**reservados y no delegables**: hacer público el repositorio, la revisión de doble uso, el
experimento físico, cambiar las reglas — y mover un umbral prerregistrado después de ver los datos,
que nunca fue suyo para delegar.

## Estado anterior (8-ago-2026 — dictamen de prevuelo: APTO, sin fallos)
**Lo sólido:** el motor extrae estructura real y replicable (semillas independientes convergen a la
5ª–7ª cifra) · la cadena píxeles → variables autoinventadas → ley legible se cerró (E2-N-002) ·
la cuarentena de E2-N-004 se resolvió con el nulo honesto: Michigan refutado, la caída sobrevive
con una candidata validada contra el verdugo que aprueba la Regla 31 · GENOMA v1.0 firmado y el
gen G2 (curiosidad por compresión) pasó su backtest 2/2 · dimensión intrínseca medida ·
**7 errores de método autocazados** y tallados como reglas · el latido vive en la nube y se
autoaudita antes de cada commit.
**La deuda declarada (escrita, no escondida):** los verdugos de las 3 campañas insignia están
**0 de 3** corridos (encolados) · el repositorio sigue privado (Regla 16) · ningún nodo alcanzó el
nivel 3 de la Regla 19 (réplica independiente) · **la `ganancia_honesta` quedó degradada a sonda
exploratoria el 8-ago-2026** tras medírsele dos canales de mentira (INFORME-30): sus números no
certifican nodos ni se citan como evidencia. *(Deuda saldada ese mismo día: la Regla 17 exigía un
Word por informe y llevaba 3 de 29; el director la enmendó — el `.md` es el registro maestro y el
Word se genera al entregar a un tercero.)*

## Cómo continuar el proyecto
Pega el **prompt de arranque** (CIMIENTOS.md, sección 4) en cualquier sesión de Claude u otro
modelo. El científico despierta con toda su experiencia. Las decisiones siempre son del director.
