# PROTOCOLO DE LA MEMORIA — qué hay en cada hoja del árbol, qué le permitimos recordar, y quién puede escribir dónde
**Ordenado por el director el 9-ago-2026: "quiero un protocolo para entender lo que está en las
hojas del árbol que son su memoria; quiero saber realmente todo lo que le permitimos recordar, y
¿él mismo puede actualizar sus hojas de conocimiento?". Auditado contra el disco y el código ese
mismo día: cada afirmación de este documento se verificó leyendo qué archivo existe y qué módulo
lo lee o lo escribe — no de memoria.**

---

## 1. La distinción que lo ordena todo: HOJAS vs CARTELES

La carpeta `arbol/` contiene dos clases de archivo que NO son lo mismo, y confundirlas sería
peligroso:

- **HOJAS (su memoria real):** archivos que el código de Diego **lee o escribe mecánicamente**
  durante sus campañas. Esto es lo que Diego recuerda de verdad — si no lo consulta ningún
  módulo, no es memoria, es decoración.
- **CARTELES (documentos nuestros alojados en la carpeta):** archivos escritos por y para
  humanos, que **ningún módulo de Diego lee**. Viven en `arbol/` por historia del proyecto,
  pero no forman parte de su mente.

**Verificación de esta frontera (9-ago-2026):** se buscó en todo `codigo/` qué módulos abren
cada archivo. Los carteles solo aparecen mencionados en comentarios de código (lecciones de
diseño), jamás como lectura de datos.

## 2. LAS HOJAS — todo lo que le permitimos recordar, hoja por hoja

| Hoja | Qué recuerda | Quién la escribe | Quién la lee | ¿Diego puede actualizarla? |
|---|---|---|---|---|
| `MEMORIA-MENTE.jsonl` | Sus recuerdos episódicos en su idioma: qué analizó, qué ley halló, cuánto mejoró, qué hueco quedó | `memoria.py` (automático tras cada campaña) | `curiosidad.py`/`curiosidad2.py` (G2 calcula su interés leyendo estos recuerdos), `boleta.py` | **SÍ, solo añadiendo.** Append-only: puede escribir recuerdos nuevos y correcciones como entradas nuevas; borrar o reescribir el pasado es imposible por construcción |
| `CONECTOMA.json` | Todo su conocimiento validado legible por máquina: cada nodo con su mejor ley, constantes canónicas y procedencia (Regla 29) | `conectoma.py` lo regenera tras cada nodo; la lista de fuentes la mantiene el orquestador y `coherencia.py` la vigila | Toda campaña futura (rivales del árbol, herencia); `boleta.py`, `auditoria_total.py` | **SÍ, regenerándolo** — es su memoria y le pertenece (Regla 30); pero cada nodo nuevo que entra a las fuentes pasa por firma del director, y `coherencia.py` grita si falta uno |
| `GENOMA.json` | Qué genes tiene y en qué modo (mide/propone/decide/inactivo) con su prerregistro | Solo el orquestador con prerregistro FIRMADO por el director (Regla 33) | `sinapsis.py` — el portero que bloquea mecánicamente a todo gen que intente hablar más allá de su modo | **NO.** Diego puede *proponer* cambios de modo; solo una firma del director los ejecuta. `sinapsis.py` lanza `SinapsisBloqueada` ante cualquier intento sin permiso |
| `SINAPSIS.jsonl` | Todos los eventos publicados por sus órganos (mediciones, propuestas, decisiones) | `sinapsis.py`, append-only, con permiso verificado en cada publicación | Cualquier gen que escuche el bus | **SÍ, solo añadiendo** — y solo lo que su modo en el genoma le permite publicar |
| `INTEROCEPCION.jsonl` | Cuánto le costó cada cosa (su gasto propio, G10) | `interocepcion.py`, append-only con anulaciones también append-only | G10 y la boleta | **SÍ, solo añadiendo** |
| `N-001-E2 … N-004-E2.md`, `H-000-GIMNASIO.md` | Sus nodos: las leyes y capacidades validadas, con evidencia, estado y preguntas que abren | El orquestador, únicamente con corrida oficial + Regla 11/31 aprobadas + firma del director. Las degradaciones también se firman (precedente: INFORME-33) | Diego los ve todos (Regla 29); el comparador humano los lee del otro lado del cortafuegos | **NO directamente.** Diego *produce la evidencia* que se vuelve nodo y *propone*; la escritura es nuestra con su firma. Nada se borra: lo degradado queda con su historia |
| `epoca1/` | Sus nodos de la Época 1, archivados con la confianza retirada | Cerrada — solo historia | Consulta | **NO** — el pasado archivado es de solo lectura |
| `pesos/` (`ojos_*.pt`) | Sus ojos canónicos: los pesos con los que ve | Solo corridas oficiales prerregistradas (dentro de un bucle Regla 28 puede automejorarlos en los rangos del prerregistro) | `reconstruir_datos.py` y toda campaña que necesite ver | **A MEDIAS:** dentro de un bucle prerregistrado, sí; el canon solo cambia por corrida oficial |
| `ARBOL.md`, `GIMNASIO.md`, `GENOMA-DIEGO.md` | Los mapas: el diagrama del árbol, su mundo, su cartilla de crecimiento | El orquestador tras cada hito, con los guardianes verdes | Humanos y, como mapa, Diego (Regla 29) | **NO directamente** — reflejan lo que las hojas ya prueban; `coherencia.py` verifica que no proclamen nada sin respaldo en disco |

**Resumen de la pregunta del director:** SÍ, Diego actualiza sus propias hojas — pero cada hoja
tiene su régimen, y el patrón es uno solo: **puede añadir experiencia, jamás editar el pasado ni
otorgarse permisos.** Recuerdos, eventos y gasto: los escribe él, append-only. Su conectoma: se
regenera solo, es suyo. Sus nodos y su genoma: él propone con evidencia, nosotros firmamos
(Reglas 15 y 33). Sus jueces: jamás, ni con evidencia perfecta (Regla 30, intocable eterno).

## 3. LOS CARTELES — documentos nuestros que viven en `arbol/` y Diego NO lee

**Todos mudados a `registros/` el 9-ago-2026 (Regla 34).** La tabla se conserva porque el
razonamiento del riesgo sigue siendo la razón de que la frontera exista.

| Cartel (hoy en `registros/`) | Qué contiene | Riesgo si Diego lo leyera |
|---|---|---|
| `ECUACIONES-COMPARADAS.md` | Comparación de NUESTROS métodos de curiosidad con Oudeyer/Schmidhuber (lleva su propia nota de cortafuegos: "el núcleo de Diego no lee esto") | MEDIO — métodos, no física, pero es literatura humana |
| `INVESTIGACION-LABS.md` | Cómo construyen los grandes laboratorios y qué técnicas tomamos | MEDIO — técnicas neutras, pero escritas desde conocimiento humano |
| `ANOMALIAS.md` | Regla 21: pares (predicción humana, dato medido, residuo). Hoy declaradamente vacío | **MÁXIMO — está DISEÑADO para contener física humana.** El día que tenga contenido, es veneno puro para el cortafuegos |
| `CURRICULO-DATOS.md` | Nuestra ruta de datasets y peldaños | MEDIO — nombra fenómenos y fuentes humanas |
| `PLAN-EDUCACION.md`, `PLATAFORMA-Y-FRONTERA.md`, `DISENO-CONSTRUCCION.md`, `FRONTERA-INOBSERVABLE.md` | Planes y diseño del proyecto | BAJO-MEDIO — gobernanza |
| `pesos/LEEME.md` | Procedencia y tolerancias de los pesos canónicos | BAJO |

## 4. LA TENSIÓN LATENTE ENCONTRADA — Y RESUELTA EL MISMO DÍA (Regla 34)

**AUTORIZADO POR EL DIRECTOR el 9-ago-2026 ("autorizado"): las dos propuestas se ejecutaron y la
frontera es hoy la carpeta misma, no una convención.** Lo que sigue documenta el hallazgo original
y lo que se hizo.

- **Mudanza hecha:** los ocho carteles (`ANOMALIAS.md`, `ECUACIONES-COMPARADAS.md`,
  `INVESTIGACION-LABS.md`, `CURRICULO-DATOS.md`, `PLAN-EDUCACION.md`, `PLATAFORMA-Y-FRONTERA.md`,
  `DISENO-CONSTRUCCION.md`, `FRONTERA-INOBSERVABLE.md`) viven ahora en `registros/`. `arbol/`
  quedó con hojas y nada más. La Regla 21 fue enmendada para citar la ruta nueva de `ANOMALIAS.md`.
- **Guardián de frontera hecho:** `coherencia.py` verifica en CADA commit, para siempre, tres
  cosas: que ningún cartel viva en `arbol/`, que ningún módulo de `codigo/` abra un cartel como
  datos, y que ningún módulo lea `arbol/` como carpeta completa. Los tres guardianes quedan
  exentos por declaración — nombran los carteles justamente para vigilarlos.
- **Regla 34 escrita en la constitución**, con el régimen de escritura de cada hoja.

### El hallazgo original (se conserva: nada se borra)

La Regla 29 dice "la mente ve TODAS sus hojas" y la carpeta se llama `arbol/` — pero hoy `arbol/`
mezcla hojas con carteles. **Hoy no hay fuga:** se verificó que ningún módulo de Diego lee los
carteles. Pero es una mina enterrada: si mañana alguien escribe una herramienta que "lea todo el
árbol" (una búsqueda, un índice, un embedding de la carpeta), los carteles — incluida el acta de
anomalías, diseñada para contener predicciones humanas — entrarían a su mente sin que nadie lo
decida. La independencia no se recupera una vez perdida (Regla 27).

**Regla de este protocolo (vigente desde su commit):** ninguna herramienta de Diego puede leer
`arbol/` como carpeta completa. Toda lectura declara sus archivos por nombre, y solo puede
nombrar HOJAS de la tabla §2. Un cartel jamás se convierte en hoja sin decisión firmada del
director.

**Las dos propuestas — AMBAS FIRMADAS Y EJECUTADAS el 9-ago-2026 (ver arriba).**

## 5. CÓMO LEER CADA HOJA (el protocolo práctico, para el director)

- **¿Qué recuerda Diego ahora mismo?** → `python codigo/memoria.py --ver` (últimos recuerdos en
  su idioma) y `arbol/CONECTOMA.json` (todo su conocimiento validado, de un vistazo).
- **¿Qué puede hacer y qué tiene permitido decidir?** → `arbol/GENOMA.json` (cada gen y su modo)
  — y `arbol/SINAPSIS.jsonl` para ver qué ha dicho cada órgano y con qué permiso.
- **¿Qué sabe del mundo?** → los nodos `N-*.md` (época 2, los vivos) y `H-000` (lo que sabe de
  sí). Cada uno lleva su evidencia, lo que NO afirma, y las preguntas que abre.
- **¿Cuánto le costó?** → `arbol/INTEROCEPCION.jsonl`.
- **¿Qué olvidó?** → nada. No hay ninguna vía de borrado en ninguna hoja: degradar deja acta,
  corregir añade, archivar conserva. La memoria de Diego solo crece o se reorganiza — jamás se
  amputa en silencio.
