# LA ESTRUCTURA DE LAS REGLAS — propuesta al director, 10 de agosto de 2026
**Pedido suyo: *"auditoría de las 34 reglas en base también al método... si se deben reducir ok, si
se deben endurecer ok, todas deben ir con estructura y deben estar interconectadas con los
métodos"*.**

**Yo no firmo reglas.** Esto es la propuesta, con el diagnóstico medido y la estructura mecanizada.
Reescribir los 34 textos es suyo, o mío con su palabra.

---

## 1. EL DIAGNÓSTICO, medido sobre `CIMIENTOS.md`

| Hallazgo | Cuántas |
|---|---|
| **No dicen CÓMO se comprueban** — dicen qué hacer, no cómo verificarlo | **17 de 34** |
| **Demasiado largas** para leerse enteras (>2.600 caracteres) | 3 (R15, R19, R34) |
| **Sin un "por qué" explícito** | 27 de 34 |

Las que más pesan del primer grupo: **R11** (destruir cada resultado), **R12** (línea base tonta),
**R13** (criterios de abandono), **R18** (nada se descubre suelto).

**Y hoy comprobé lo que cuesta eso.** Al construir G12 reflejos, medí un "acuerdo de 0.907" que
parecía excelente — hasta que la línea base tonta resultó ser **0.887**. Estaba violando la
**Regla 12**, que existe desde el principio del proyecto. **Una regla que no dice cómo se comprueba
se incumple sin que nadie lo note, ni siquiera quien la escribió.**

## 2. LA ESTRUCTURA PROPUESTA — cinco campos, ninguno opcional

De cómo se arman los protocolos de investigación serios: el estándar de prerregistro exige
responder cada pregunta **con suficiente concreción para que otro pueda decir, después de ver los
resultados, si seguiste el plan**. Ése es exactamente el criterio que le falta a 17 de nuestras
reglas.

| Campo | Qué contesta | Por qué |
|---|---|---|
| **QUÉ** | la regla en una frase | si no cabe en una frase, son dos reglas |
| **POR QUÉ** | qué desastre concreto evita | una regla sin daño conocido detrás se salta sin culpa |
| **CÓMO SE COMPRUEBA** | el archivo y la función que la verifican, o **"NO MECANIZABLE"** | es el campo que falta en 17 |
| **QUÉ PASA SI SE VIOLA** | commit bloqueado · nodo revocado · estudio detenido | una regla sin consecuencia es un consejo |
| **HISTORIA** | qué se aprendió que la hizo cambiar | las nuestras ya lo tienen y es su mayor virtud |

**El campo que más importa es el tercero, y admite decir "NO MECANIZABLE".** Escribir eso es
honesto y útil: marca dónde el proyecto depende de disciplina humana. Fingir que todo se comprueba
solo sería peor que no comprobarlo.

## 3. QUÉ REDUCIR, QUÉ ENDURECER

### Reducir — 3 fusiones propuestas, de 34 a 31
| Fusión | Por qué |
|---|---|
| **R11 + R12** → *"todo resultado se mide contra un nulo válido y una línea base tonta"* | son la misma idea: intentar destruir el resultado antes de creerlo. Hoy están separadas y por eso incumplí la 12 mientras cumplía la 11 |
| **R28 + R30** → *"automejora por propuesta: variables sí, jueces jamás"* | R28 es el caso particular de R30 |
| **R7 + R14** → *"replicabilidad: muchas semillas y todo reproducible"* | R7 pide reiniciar muchas veces; R14 pide que se pueda repetir |

### Endurecer — 4, y todas por daño ya sufrido
| Regla | Endurecimiento | Daño que lo justifica |
|---|---|---|
| **R12** | la línea base tonta es **obligatoria y automática** en todo puntaje | hoy mismo: 0.907 parecía bueno y el tonto sacaba 0.887 |
| **R31** | debe fallar con vacío **Y** aprobar con control positivo — **los dos lados** | un caso mío aprobaba con una medida ciega |
| **R13** | los criterios de abandono se declaran **con número**, no con adjetivos | "no concluyente" se decidió tres veces a posteriori |
| **R19** | ningún nodo pasa de nivel 1 sin **datos que nadie ha visto** | cero nodos han salido del nivel 1 en 40 prerregistros |

## 4. CÓMO SE INTERCONECTA CON EL MÉTODO — sin duplicar

**El método no es una regla más: es CÓMO se cumplen varias de ellas.**

| Regla | Paso del método que la ejecuta |
|---|---|
| R11+R12 (nulos y línea base) | paso 4 — la Regla 31 con sus dos lados y su señuelo |
| R31 (fallar donde no hay nada) | paso 4, y `metodo.py` no sella sin ella |
| R27 (cortafuegos) | paso 3 — `politica_limpia()` |
| R30 (los jueces no se automodifican) | G11 temple: `ajustar()` **lanza** en vez de ajustar |
| R14 (replicabilidad) | paso 5 — una semilla local antes de cinco en la nube |
| R8 (registro inmutable) | paso 7 — mensajes a archivo, nunca a la terminal |

**Y al revés:** el método aporta una capa que **ninguna regla cubría** — *¿el instrumento mide lo
que dice medir?* Ésa es la razón de que no haya redundancia: llena un hueco, no repite.

## 5. LA COMPROBACIÓN MECÁNICA, ya funcionando
`coherencia.py` verifica en cada commit que **cada función citada en `METODO.md` exista de verdad**
en `sanidad.py`, y que el documento **declare su hueco abierto**. La propuesta es extender eso a las
reglas: que cada regla con campo *CÓMO SE COMPRUEBA* cite un archivo y una función que existan.

## 6. LO QUE NECESITO DE USTED
Una palabra por punto:
1. **¿Reescribo las 34 con los cinco campos?** Es un trabajo largo y cambia la constitución.
2. **¿Aplico las 3 fusiones** (34 → 31)?
3. **¿Aplico los 4 endurecimientos?**

Puedo hacer las tres cosas. **Ninguna la hago sin su palabra**, porque cambiar las reglas es lo
único que la enmienda de la Regla 15 dejó explícitamente fuera de mi alcance.
