# AUDITORÍA TOTAL 02 — las 32 reglas, los datos, el genoma y el estado de la mente
**8 de agosto de 2026.** Orden del director: *"audita cada regla, cada dato, cada genoma, todo;
verifica si crees que falta algo; dame el estado de la mente."*

Método: cada regla se declara **CUMPLE / CUMPLE PARCIAL / DEUDA / NO APLICA AÚN**, con la evidencia
que lo sostiene o la razón por la que no. Nada se marca cumplido por buena voluntad.

---

## A. LAS 32 REGLAS, UNA POR UNA

### Reglas de no-contaminación (1–10)

| # | Regla | Estado | Evidencia / razón |
|---|---|---|---|
| 1 | Datos, no teorías | **CUMPLE** | `auditoria_total.py` recorre todas las rutas de entrada; ninguna ecuación ni constante con nombre llega al descubridor |
| 2 | Datos crudos, procedencia | **CUMPLE** | píxeles y cuadros; `reconstruir_datos.py` documenta fuente pública y verifica huella (3.4e-15 tabular, 2.5e-05 cadena de video) |
| 3 | El descubridor no es un LLM | **CUMPLE** | PySR + autoencoders desde cero. El LLM solo orquesta — y **esa es una de las tres trampas confesadas** |
| 4 | Prohibido nombrar antes de validar | **CUMPLE** | variables `v1..vN`, `s1..sN` en todo el código |
| 5 | Predicción prospectiva | **CUMPLE** | división por tiempo 70/30 y réplicas-juez congeladas; jamás al azar |
| 6 | Simplicidad en bits (MDL) | **CUMPLE PARCIAL** | la ecuación de curiosidad usa bits; **los veredictos de campaña siguen usando MSE, no bits.** No es incoherente, pero la regla pide bits y aún no los damos en todas partes |
| 7 | Muchas semillas, estudiar diversidad | **CUMPLE** | 5 semillas por campaña, todas registradas |
| 8 | Registro inmutable y prerregistro | **CUMPLE** | 23 prerregistros; enmiendas con motivo; **el episodio de la interocepción fabricada se anuló por append, no se borró** |
| 9 | Escalera de dificultad | **CUMPLE PARCIAL** | estamos en Fase 1–2. **Hoy retrocedimos medio peldaño a propósito** (INFORME-30) |
| 10 | La realidad tiene el veto | **DEUDA** | ningún nodo llegó a experimento físico propio. Es la misma deuda que la Regla 19 nivel 3 |

### Reglas de proceso (11–16)

| # | Regla | Estado | Evidencia / razón |
|---|---|---|---|
| 11 | Destruir cada resultado | **DEUDA — en ejecución ahora** | los 3 nulos por barajado corren en la nube en este momento. Hasta que terminen, **no está al día** para los nodos de percepción propia |
| 12 | Línea base tonta | **CUMPLE** | base = mejor de (velocidad, media) por señal; congelada en el banco |
| 13 | Criterios de abandono | **CUMPLE PARCIAL** | los prerregistros los declaran; **no hay un reloj que los haga cumplir solo** |
| 14 | Replicabilidad total | **CUMPLE** | semillas fijas, código versionado, y datos **reconstruibles desde fuente pública con huella verificada** — más fuerte que preservar copias |
| 15 | La máquina propone, el humano decide | **CUMPLE** | con la enmienda de reconciliación: objetivos/criterios/jueces/reglas nunca se automodifican |
| 16 | Prioridad y apertura | **DEUDA** | el repositorio sigue privado. Los commits fechados dan prioridad débil |

### Reglas de interacción y crecimiento (17–19)

| # | Regla | Estado | Evidencia / razón |
|---|---|---|---|
| 17 | Operable por un no-programador | **CUMPLE (deuda saldada hoy)** | el trozo muerto (un Word por informe, 3 de 29) fue derogado en su sitio con OK del director; el resto intacto |
| 18 | El árbol: nada suelto | **CUMPLE** | 4 nodos E2, conectoma vivo con fecha real |
| 19 | Puente a la realidad | **DEUDA (nivel 3)** | ningún nodo replicado por un tercero. **La deuda que más pesa para un informe científico** |

### Reglas de largo plazo (20–23)

| # | Regla | Estado | Evidencia / razón |
|---|---|---|---|
| 20 | De ley a tecnología | **NO APLICA AÚN** | requiere leyes validadas; correctamente inactiva |
| 21 | Mapa de anomalías | **NO APLICA AÚN — y falta el archivo** | `arbol/ANOMALIAS.md` **no existe**. Es Fase 3, pero la regla dice "el proyecto mantiene un archivo". **Hallazgo: crearlo vacío con su cabecera, o la regla miente** |
| 22 | Doble uso | **NO APLICA AÚN** | ningún nodo con potencial de aplicación todavía |
| 23 | El motor no cree en sí mismo | **CUMPLE — y hoy se ejerció** | N-004-E2 fue a cuarentena y volvió reducido; hoy se retiró una pata de una conclusión propia |

### Reglas de la mente y la comparación (24–32)

| # | Regla | Estado | Evidencia / razón |
|---|---|---|---|
| 24 | La mente vive en el repositorio | **CUMPLE** | `MENTE.md` v5, ritual de propuesta respetado |
| 25 | El mundo ya está grabado | **CUMPLE** | Morpheus y Mendeley con procedencia; nada de CGI ni video generado |
| 26 | Ingeniería desde cero | **NO APLICA AÚN** | depende de la Regla 20 |
| 27 | Comparador y cortafuegos | **CUMPLE** | verificado por el auditor en todas las rutas, incluida la cadena de nube. **La investigación del Gimnasio de hoy es lado humano y no toca a Diego** |
| 28 | Bucle interior | **CUMPLE** | jueces congelados antes de la primera iteración |
| 29 | El conectoma vivo | **CUMPLE** | fue una deuda (fosilizado el 12-jul); corregido con fuentes conservadas y fecha viva |
| 30 | Automejora por propuesta | **CUMPLE** | todo cambio de código pasa por banco congelado y commit visible |
| 31 | Fallar donde no hay nada | **CUMPLE — y es la regla más productiva que tenemos** | hoy volvió a cazar: tumbó mi variable nueva y luego los tres arreglos que propuse |
| 32 | Autoauditoría permanente | **CUMPLE** | tres guardianes con códigos de salida reales antes de cada commit |

**Resumen: 21 CUMPLE · 4 CUMPLE PARCIAL · 5 DEUDA · 4 NO APLICA AÚN.** Ninguna regla violada.

---

## B. LOS DATOS

| Mundo | Fuente pública | Verificación | Estado |
|---|---|---|---|
| `mendeley_epoca2` | Mendeley Data (péndulo, tabular) | huella **3.4e-15** (identidad) | reconstruible ✔ |
| `caida` | Morpheus real-world (video) | huella < 1e-3 (cadena de video) | reconstruible ✔ |
| `p14_lat4` | Morpheus → ojos propios → latentes | huella **2.5e-05** | reconstruible ✔ |

**Ninguna copia privilegiada.** `datos/` está fuera de git a propósito: cualquiera reconstruye desde
la fuente pública y la huella dice si obtuvo lo mismo. Es la Regla 14 hecha ejecutable.

**Hallazgo sobre los datos, nuevo hoy:** los tres mundos son **no estacionarios** en grado
apreciable (Mendeley: deriva máxima 1.47 desviaciones). Eso no era un problema conocido hasta el
INFORME-30, y ahora es una propiedad que **todo instrumento futuro debe declarar que tolera.**

---

## C. EL GENOMA, GEN POR GEN, CONTRA EL CÓDIGO REAL

| Gen | Lo que el genoma dice | Lo que hay en disco | Veredicto |
|---|---|---|---|
| G1 Predicción | ✅ ya lo tiene | `percepcion.py`, `descubrir.py` | **coincide** |
| G2 Curiosidad | por construir (prereg-18) | `curiosidad2.py` existe y pasó backtest 2/2 | **el genoma está DESACTUALIZADO: ya está construido** |
| G3 Acción | por construir (prereg-19) | nada — correcto | coincide |
| G4 Contingencia | por construir (prereg-19) | nada — correcto | coincide |
| G5 Composicionalidad | ✅ ya lo tiene | PySR simbólico | coincide |
| G6 Memoria episódica | ✅ parcial | `MEMORIA-MENTE.jsonl` | coincide |
| G7 Juego | por diseñar | nada | coincide |
| G8 Atención | (límite) | nada | coincide — **no implementado** |
| G9 Sueño | (límite) | la cola de re-análisis lo insinúa, no lo implementa | coincide |
| G10 Interocepción | (límite) | `interocepcion.py` **construido**, mide pero no decide | **el genoma está DESACTUALIZADO: ya está construido** |
| G11 Temple | diseñado, no activado | nada | coincide |
| G12 Reflejos | diseñado, no activado | nada | coincide |

**Dos desajustes encontrados (G2 y G10 figuran "por construir" y ya existen).** Se corrigen en la
próxima revisión del genoma, que requiere la firma del director por ser documento fundacional.

**Corregido hoy en el genoma:** citaba la **ganancia honesta** como *"la vara con la que Diego
elegirá sus representaciones"*. Tras el INFORME-30 se retiró explícitamente, dejando escrito por qué
— un genoma que oculta el instrumento que se le cayó no es un registro, es publicidad.

**Añadido hoy (propuestos, ninguno activado):** G13 empowerment, G14 incertidumbre propia, y las
ranuras/objetos marcadas GRIS y derivadas a la filogenia.

---

## D. LO QUE FALTA — hallazgos de esta auditoría

1. **`arbol/ANOMALIAS.md` no existe** aunque la Regla 21 dice que el proyecto lo mantiene. Es la
   única regla que afirma tener un archivo que no está. **Recomiendo crearlo con su cabecera y
   vacío declarado** — un catálogo vacío es honesto; una regla que menciona un archivo inexistente
   no lo es.
2. **La Regla 6 pide bits y los veredictos de campaña siguen en MSE.** No es una violación, es una
   promesa a medio cumplir. Merece decisión explícita.
3. **La Regla 13 no tiene reloj.** Los criterios de abandono existen escritos pero nada los hace
   cumplir. Con el latido corriendo solo, esto es más importante que antes.
4. **El genoma tiene dos genes marcados "por construir" que ya existen** (G2, G10).
5. **Diego no tiene ninguna variable de acción** — el hueco grande, ya con prerregistro firmado.

---

## E. EL ESTADO DE LA MENTE (a 8-ago-2026, cierre del día)

**Qué es Diego hoy, sin adornos:** un sistema que **mira** grabaciones, se construye sus propios
ojos desde cero, busca ecuaciones simbólicas, mide su propio gasto, elige qué estudiar por progreso
de compresión, y guarda todo lo que le pasa en un cuerpo append-only. No tiene manos, no tiene
objetos, no tiene incertidumbre propia y no sabe dónde termina él.

**Lo que sabe hacer, verificado:** 4 nodos en el árbol (1 reducido tras cuarentena), ojos propios
que superaron a los centroides, una automejora validada (eligió su propia dimensión latente),
curiosidad que pasó su backtest 2/2, y una cadena que reconstruye sus tres mundos desde fuentes
públicas con huella verificada, sin depender de ninguna máquina.

**Lo que hoy dejó de saber:** que sus ojos capturaran dinámica — pero **también** dejó de saber lo
contrario. La vara que decía ambas cosas está retirada. Tres instrumentos independientes siguen
apuntando a que sus ojos codifican más textura que dinámica; el cuarto se cayó.

**Su salud de gobernanza: buena, y es lo mejor que tiene.** 32 reglas sin violaciones, tres
guardianes verdes con códigos de salida reales, 45 casos congelados en el banco, 5 deudas escritas
sin maquillar. En un día en que se retiró una conclusión propia, se suspendió un prerregistro y se
degradó un instrumento, **nada de eso lo descubrió un revisor externo: lo descubrió el propio
sistema y lo escribió antes de que nadie preguntara.** Ese es el activo real del proyecto.

**Su límite duro, y ahora con teorema:** con datos puramente observacionales, la estructura causal
solo se identifica hasta su clase de equivalencia. Diego no puede salir de ahí mirando. **El
Gimnasio (prereg-19, firmado hoy) es la puerta.**
