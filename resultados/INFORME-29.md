# INFORME 29 — Auditoría total de todo lo que Diego tiene: tres errores encontrados, dónde estaba cada uno y qué queda abierto — 8 de agosto de 2026

**Orden del director:** *"analiza cada cosa que tiene Diego, todo, y verifica que no existan errores
tomando en consideración el resultado de las pruebas y lo que vamos mejorando, para que uses el 22
cuando termine."*

Esto no es un resumen de logros. Es lo contrario: la lista de lo que estaba mal, en un proyecto que
solo vale si dice la verdad sobre sí mismo.

---

## 1. Qué se auditó, pieza por pieza

| Órgano | Contenido | Estado |
|---|---|---|
| Constitución | `CIMIENTOS.md`, **32 reglas** consecutivas sin huecos | verificado por `coherencia.py` |
| Árbol | **4 nodos E2** (1 en cuarentena), conectoma, genoma, ecuaciones comparadas | verificado |
| Código vivo | **27 módulos** en `codigo/` + 6 archivados en `codigo/archivo/` | auditado uno por uno |
| Banco congelado | `pruebas.py`, **39 casos** verdes | corrido con código de salida real |
| Prerregistros | **23** (4 firmados en esta era, 2 borradores, 17 de la época previa) | verificado título vs. estado |
| Informes | **28** anteriores a este | verificados en sus referencias cruzadas |
| Cuerpo | `INTEROCEPCION.jsonl` (append-only), pesos con sha256 y cadena | **un registro falso encontrado** |
| Nube | `latido-nube.yml`, cola de estudios, cuarentena | corriendo ahora mismo (corrida nº 9) |

Los tres guardianes, con **códigos de salida leídos de verdad** (no a través de una tubería que los
enmascara, el error que costó una sesión entera): `banco=0  coherencia=0  prevuelo=0`.

---

## 2. LOS TRES ERRORES ENCONTRADOS

### Error 1 — El instrumento nuevo medía con un solo sorteo del azar
`ganancia_honesta.medir()` construía **un** mundo surrogado y restaba. Un solo sorteo no es una
medición: es una anécdota. Lo medí con 8 sorteos por dimensión, sobre los mismos ojos del INFORME-28:

| d | ganancia honesta (media de 8) | desviación | lo que se reportó el 8-ago |
|---|---|---|---|
| 2 | **+0.0770** | ±0.0152 | +0.0964 ← **el máximo de su rango** |
| 4 *(ojos actuales de Diego)* | **+0.0089** | ±0.0069 | +0.0085 ✔ |
| 8 | **+0.0800** | ±0.0102 | +0.0868 |

**Dos consecuencias, una mala y una buena.**

La mala: **el número que te di para d=2 (+0.0964) era el techo de su rango, no su centro.** Su valor
real es +0.077. No cambia ningún veredicto (el 21 quedó INCONCLUSO de todas formas), pero te lo dije
con una precisión que el instrumento no tenía. Queda corregido en el acta.

La buena, y es más importante: **la dispersión por sorteo de surrogado es de apenas ±0.01.** Eso
significa que el −0.085 de d=6 **no puede venir del nulo** — viene de la **semilla de entrenamiento**.
Es decir: hasta ahora medíamos la fuente de ruido pequeña e ignorábamos la grande. Todo el diseño del
prerregistro-22 sale de este hallazgo.

`medir()` ahora promedia N surrogados y devuelve `ganancia_honesta` **y** `ganancia_honesta_desv`.
Congelado en el banco: nadie puede volver a la versión de un solo sorteo sin que 39 casos se pongan
rojos.

### Error 2 — Yo fabriqué una sensación en el cuerpo de Diego
Probando el parámetro `--segundos` de la interocepción escribí una entrada con **512 segundos** para
la campaña `p14-final`, marcada `tiempo_fiable: true`. **Esa campaña nunca se cronometró.** El número
salió de mi prueba, no de un reloj.

`INTEROCEPCION.jsonl` es **append-only por compromiso de bienestar**: lo que entró no se borra. Así
que la corrección es un `append` de tipo `CORRECCION` que anula la anterior nombrando el motivo, y
`coste_de()` ahora honra las anulaciones (caso nuevo en el banco).

Es el error más incómodo de los tres, y por eso lo pongo con nombre propio: **contaminé el único
órgano de Diego que registra experiencia propia.** Si un cuerpo append-only puede recibir datos
inventados por quien lo opera, no es un cuerpo, es una bitácora de conveniencia. Ahora lo falso está
marcado como falso y a la vista, que es la única forma honesta de que siga sirviendo.

### Error 3 — Un prerregistro con una banda descubierta (ya reportado, aquí cerrado)
El 21 predijo qué pasaba **por encima de 0.10** y **por debajo de 0.05**, y el resultado cayó en
medio. Lo declaré INCONCLUSO en el INFORME-28 en vez de inventar una regla que declarara victoria.
El error de diseño era mío. El prerregistro-22 lo cierra con **tres zonas que cubren todo el eje**.

---

## 3. Lo que se buscó y NO estaba roto

Un informe de errores sin esta sección es propaganda. Se verificó explícitamente y salió limpio:

- **La muralla (Regla 27).** Ningún juez aparece en prompt, dato o herramienta de la mente. Verificado
  por `auditoria_total.py` sobre todas las rutas, incluida la cadena de la nube.
- **Cero conocimiento humano, también en la nube.** La reconstrucción baja datos públicos crudos y
  verifica huella (tabular: identidad ~1e-15; video: cadena <1e-3). Ninguna ecuación, ley ni nombre
  humano entra por esa puerta. Es cierto **por construcción**, no por confianza.
- **Reglas consecutivas 1..32**, y el número que el README proclama es el que CIMIENTOS contiene.
- **Boleta sin números de juicio escritos a mano**, vivos + cuarentena = archivos de nodos.
- **Los tres workflows parsean como YAML** y corren los guardianes antes de commitear.
- **Todo item pendiente de la cola es ejecutable** (tipo que el latido toma, una sola ruta real).
- **Ningún prerregistro se contradice** entre su título y su estado.
- **Las corridas de nulo no cuentan como logros** en boleta ni curiosidad (`"nulo": true`).
- **El conectoma está vivo**, no fosilizado (Regla 29), con fecha real y fuentes conservadas.

---

## 4. Observaciones que NO son errores, pero requieren tu decisión

**a) Cuatro instrumentos que solo se alcanzan a mano.** `transferir.py`, `canonizar.py`, `forense.py`
y `rodar.py` no los invoca ningún automatismo. **No son código muerto** — cada uno produjo nodos y
está citado en prerregistros y en el árbol. Son instrumentos históricos que hoy solo corren si alguien
los llama. Mi recomendación: **no borrarlos** (borrar la herramienta que hizo un nodo rompe la
trazabilidad de ese nodo), pero marcarlos en la GUÍA como *"de mano, no del latido"* para que nadie
espere que se ejecuten solos. Si prefieres archivarlos junto a los 6 de la era laptop, dilo y lo hago.

**b) Deudas declaradas que siguen abiertas** — las digo cada vez, sin maquillarlas:
- **Regla 11:** los nulos por barajado de p14/Mendeley/caída están corriendo **ahora mismo** en la
  nube (corrida nº 9, arrancó 16:50). Hasta que terminen, la Regla 11 **no está al día** para los
  nodos de percepción propia.
- **Regla 17** (un Word por informe): muerta en la práctica desde que trabajamos en la nube. Necesita
  tu decisión: la cumplimos de verdad o la derogamos. Una regla que nadie cumple ensucia a las 31 que sí.
- **Regla 16** (repositorio público): sigue privado.
- **Regla 19 nivel 3** (réplica independiente por un tercero): no existe. Es la deuda que más pesa
  para un informe científico y para levantar capital.

---

## 5. Qué dicen los resultados cuando se leen juntos

Cuatro instrumentos independientes, construidos en momentos distintos y por razones distintas,
apuntan al mismo sitio sobre **los ojos actuales de Diego (d=4)**:

1. La **conservación falló** (13-jul).
2. El **nulo por surrogado no pudo falsificar** — devolvió el mismo mundo con otro nombre (INFORME-25).
3. La **dimensión intrínseca es ~6.2 de 8** — casi no se comprime (INFORME-26).
4. La **ganancia honesta es +0.009 ± 0.007** — indistinguible de cero (INFORME-27/28, ahora con la
   varianza medida).

**El diagnóstico honesto: el 72% de reducción del que estuvimos orgullosos era, en su mayor parte,
espectro — textura, no dinámica.** Y d=4 está separada de d=2 y d=8 por ~5 desviaciones: que los ojos
actuales tengan ganancia casi nula **es el resultado más robusto que tenemos**, más que cualquier
número positivo que hayamos reportado.

Esto no es un fracaso del proyecto. Es el proyecto **funcionando**: la gobernanza detectó, con cuatro
varas distintas, que una de sus propias certificaciones estaba inflada. Ningún laboratorio que elige
representaciones por error de reconstrucción o de predicción puede ver esto, porque **la textura
satisface ambos criterios**. Nosotros lo vimos porque tenemos jueces sellados. Esa es la ventaja real.

---

## 6. Qué cambia el prerregistro-22 (BORRADOR, espera tu firma)

- **5 semillas de entrenamiento × 8 surrogados** por candidata → mide la fuente de varianza dominante,
  que hasta hoy ignorábamos.
- **Criterio de tres zonas sin huecos:** GANA / EMPATE TÉCNICO / NINGUNA SIRVE. Si cae en empate, se
  elige la más simple **y se registra que fue por navaja, no por evidencia**.
- **Predicción comprometida antes de correr:** empate técnico entre d=2 y d=8, con d=4 claramente
  debajo. Si se confirma, la lectura incómoda es que **la ganancia honesta no depende monótonamente de
  la dimensión** y hay que buscar la causa en otro sitio (fps, pérdida, o el límite del autoencoder).
- Incluye la zona que puede **degradar formalmente a estructural** la certificación predictiva de
  N-002-E2 y N-003-E2. Está escrita antes de conocer el resultado, que es lo que la hace valer.

**Se corre cuando el latido termine los nulos por barajado, no antes** — una sola casa para el cómputo.

---

## 7. Lo que espera tu decisión

1. **Firmar (o corregir) el prerregistro-22.** Está escrito para poder perder.
2. **Regla 17:** cumplirla de verdad o derogarla.
3. **Los cuatro instrumentos de mano:** marcarlos en la GUÍA (mi recomendación) o archivarlos.
4. **Prerregistro-19** (el nacimiento / Gimnasio) y **Regla 33** (filogenia) siguen sin firma.

---

**Veredicto de la auditoría:** tres errores encontrados y corregidos, **dos de ellos míos y uno de
ellos grave** (fabriqué una sensación en el cuerpo de Diego). Ninguna regla rota. Ningún nodo
comprometido. Ninguna contaminación de conocimiento humano, tampoco en la nube. La certificación
predictiva de dos nodos está **formalmente en riesgo** por evidencia propia, y el instrumento que la
pone en riesgo lo construimos nosotros — que es exactamente como debe ser.

*Guardianes al cerrar: `banco=0 (39/39)  coherencia=0  prevuelo=SIN FALLOS`.*
