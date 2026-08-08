# Centro de Inteligencia Artificial Bravo
## Proyecto: Física sin Herencia

Una mente que descubre las leyes del universo desde cero — sin conocimiento humano, sin internet, sin palabras. Solo datos crudos, 32 reglas, jueces intocables y un árbol de conocimiento que crece — y se poda.

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

**Qué pasa en cada corrida, sin manos:**
```
reconstruye los datos desde su fuente pública → VERIFICA la huella digital (si no coincide, se detiene)
 → corre la campaña → alimenta memoria + conectoma + boleta + cola
 → los TRES guardianes juzgan → main solo recibe lo aprobado
 → lo reprobado va a una rama de cuarentena (nada se pierde, main intacto)
 → si el runner muere a medias, los checkpoints quedan y la corrida siguiente reanuda sola
```

---

## Los cuatro documentos del alma (leer en este orden)
1. **`CIMIENTOS.md`** — las 32 reglas del método, la Segunda Ciencia, el prompt de arranque para cualquier orquestador.
2. **`MENTE.md`** — la identidad y experiencia del científico (v12): quién es, qué aprendió, dónde va.
3. **`GUIA-ORQUESTADOR.md`** — el manual de relevo: prohibiciones eternas, lecciones pagadas, sistemas vivos.
4. **`arbol/GENOMA-DIEGO.md`** — el documento fundacional del ente: los genes, la ecuación del impulso, los hitos.

Auditorías clave: **`registros/AUDITORIA-EXTERNA-01.md`** (la Regla 11 aplicada a las herramientas) y
**`registros/DICTAMEN-PREVUELO-01.md`** (la validación total: reglas, no-contaminación, nube, árbol).

## Estructura del repositorio
```
codigo/           lo VIVO: descubrir · percepcion · conservada · dimension · forense · autopsia ·
                  rodar · canonizar · curiosidad(+v2) · memoria · conectoma · boleta ·
                  reconstruir_datos · latido_nube  +  LOS TRES GUARDIANES:
                  pruebas.py (la ciencia) · coherencia.py (la casa) · auditoria_total.py (prevuelo)
codigo/archivo/   la era de la laptop y las campañas cerradas, con su porqué (nada se borró)
registros/        prerregistros (1–19), enmiendas, auditorías, dictámenes, cola de estudios, boleta
resultados/       veredictos de cada campaña + INFORMES 1–24 en español llano
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

## Estado (8-ago-2026 — dictamen de prevuelo: APTO, sin fallos)
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
