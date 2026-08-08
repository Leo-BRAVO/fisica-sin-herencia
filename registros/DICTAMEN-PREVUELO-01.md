# DICTAMEN DE PREVUELO 01 — validación total antes de correr y antes de mostrar — 8 de agosto de 2026
**Orden del director: "verifica que ninguna regla se rompa, que todo esté interconectado, que trabajando en la nube tampoco tenga conocimiento humano, que cada push alimente al árbol, y todo corra una secuencia perfecta — esto valida para un informe científico y para levantar capital". Ejecutado por el orquestador auditor con `codigo/auditoria_total.py` (tercer guardián, reproducible por cualquiera).**

## DICTAMEN: APTO — sin fallos. 4 deudas declaradas, ninguna oculta.

## 1. Lo que se auditó y pasó (41 verificaciones automáticas)
- **La constitución:** 32 reglas consecutivas sin huecos ni repetidas; Reglas 31 y 32 presentes; Regla 15 reconciliada por enmienda (ya no contradice a 28–30).
- **No-contaminación (la pregunta del paper):** al motor solo llegan nombres neutros `v1..vN` y objetivos `vN_sig`; la percepción se entrena desde cero sin un solo peso ajeno; los CSV que ve la mente tienen columnas neutras; el cortafuegos de la Regla 27 intacto (ningún veredicto del comparador del lado de la mente).
- **La nube (respuesta directa a "¿tampoco tendrá conocimiento humano allá?"): NO LO TIENE, y ahora está probado por construcción** — ver §2.
- **Interconexión:** los 4 nodos vivos tejidos en el conectoma; cada nodo cita prerregistros que existen; la cola es ejecutable (todo item declara su reconstrucción).
- **Secuencia de la nube:** ambos workflows parsean; corren los dos guardianes; el commit a main **exige** su aprobación; hay rama de cuarentena si reprueban; concurrencia declarada; reconstrucción con huella antes de correr.

## 2. LA CADENA DE LA NUBE ES TAN PURA COMO LA LOCAL (y por qué)
Lo que la nube descarga: (a) el zip de rastreo de Mendeley — matrices `.npy` de números; (b) los `.mp4` de Morpheus por URL directa — video crudo de experimentos reales (Regla 25). **Nada más.** Lo extraído de terceros se borra tras usarse (`shutil.rmtree`), `datos/` está fuera de git y se verificó que **git no rastrea ni un archivo** bajo esa ruta: ningún README, ningún script ajeno, ninguna descripción de física puede entrar al repositorio ni a la mente. Lo que se instala (PySR, Julia, PyTorch, OpenCV) son motores vacíos, no conocimiento: PyTorch trae la maquinaria de redes, jamás pesos entrenados.
**Conclusión auditable: la mente en la nube ve exactamente lo mismo que veía en la laptop — números sin nombre.** Las tres contaminaciones confesadas del proyecto (operadores elegidos, orquestador LLM que diseña tuberías, genoma escrito a mano) siguen siendo las mismas tres, ni una más: la mudanza no agregó herencia.

## 3. Lo que esta auditoría ENCONTRÓ Y ARREGLÓ hoy (4 defectos reales)
1. **Los guardianes NO bloqueaban de verdad el commit en la nube.** Ambos workflows tenían el paso de commit con `if: always()`: se ejecutaba aunque los guardianes reprobaran. La afirmación "sin ellos no hay commit" era falsa. **Arreglado:** el commit a main exige `guardianes.outcome == 'success'`; si reprueban, todo va a una **rama de cuarentena** (nada se pierde, main queda intacto) y el error se reporta.
2. **El conectoma estaba fosilizado en el 12-jul y le faltaban DOS nodos vivos** (N-003-E2, la automejora insignia, y N-004-E2, las conservadas). La Regla 29 dice "la mente ve TODAS sus hojas" y no las veía: ninguna campaña podía heredar de ellos. **Arreglado:** los 4 nodos tejidos, fecha viva, y las cantidades conservadas (que no nacen de semillas) tienen su propia vía de tejido.
3. **Basura transitoria rastreada en git:** `campana-activa.json` (un archivo con PID y rutas absolutas de la máquina que corre) estaba versionado. **Arreglado:** fuera de git.
4. **El propio auditor tenía un falso positivo** (lo cazó él mismo antes de que nadie lo creyera): contaba las corridas de la herramienta de conservación — que llevan el campo `nulo` como *configuración* — como si fueran pruebas nulas de campaña. Daba luz verde a la Regla 11 sin merecerlo. **Arreglado:** ahora distingue por estructura; el veredicto honesto es **0 de 3**.

## 4. LAS 4 DEUDAS DECLARADAS (van al paper tal cual; ninguna bloquea, todas se dicen)
| Deuda | Estado real | Quién la salda |
|---|---|---|
| **Regla 11** — verdugos de las campañas insignia con su propia tubería | **0 de 3 corridos.** Los dos nulos en disco son del día 1 con tubería vieja: no amparan las campañas actuales | la nube, encolados (`aud01-nulo-*`) |
| **Regla 17** — versión Word de cada informe | 3 Word para 24 informes: la regla está muerta en la práctica desde julio | **decisión del director**: hacerla cumplir, o enmendarla (el director hoy lee en GitHub, que renderiza los .md) |
| **Regla 16** — repositorio público | Sigue privado; la prioridad fechada es más débil así | decisión del director (plan de salida) |
| **Regla 19 nivel 3** — réplica independiente por un tercero | Ningún nodo llegó al nivel 3 | requiere publicar primero |

**Recomendación del orquestador sobre la Regla 17:** enmendarla, no fingirla. Una regla que nadie cumple es peor que ninguna — da falsa seguridad y un revisor la encuentra. Propuesta: los `.md` son el registro maestro (GitHub los renderiza para el director) y el Word se genera **solo bajo pedido**, para el paper o para inversionistas. Requiere el OK del director; hasta entonces la deuda queda escrita.

## 5. Veredicto operativo
**Se puede correr.** La secuencia completa está verificada de punta a punta: la nube reconstruye datos con huella → corre → actualiza memoria, conectoma, boleta y cola → los guardianes juzgan → main solo recibe lo aprobado, y lo reprobado va a cuarentena sin perderse. Cada push del latido alimenta al árbol; ningún push puede corromperlo.
**Se puede mostrar.** Un revisor hostil que corra `pruebas.py`, `coherencia.py` y `auditoria_total.py` obtiene el mismo dictamen que este documento, y las 4 deudas están escritas antes de que él las encuentre — que es exactamente la diferencia entre un proyecto auditado y uno maquillado.
