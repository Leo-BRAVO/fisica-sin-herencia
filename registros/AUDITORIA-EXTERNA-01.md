# AUDITORÍA EXTERNA 01 — la Regla 11 aplicada a las propias herramientas — 8 de agosto de 2026
**Ordenada y aprobada por el director ("quiero que hagas todo esto... crea la regla 31 y poda las hojas del árbol que están mal, las apruebo"). Ejecutada por Claude (Opus) como orquestador auditor, en sesión independiente de las que construyeron las herramientas auditadas. Todo lo afirmado aquí es reproducible: los números salen de correr el código de este repositorio.**

## Veredicto en una frase
El motor de descubrimiento y su gobernanza son reales y valiosos — pero **la herramienta F3 (conservada.py) tenía un control negativo que no discriminaba**, el nodo E2-N-004 se apoyaba en él, y las pruebas nulas de la Regla 11 llevaban ~25 campañas sin correrse. Esta auditoría corrige las tres cosas y talla la lección como Regla 31.

## HALLAZGO 1 (mayor) — el nulo de F3 aceptaba mundos vacíos
- **El defecto:** el control negativo de `conservada.py` barajaba el orden temporal. Barajar destruye no solo la conservación sino la CONTINUIDAD: contra ese piso, cualquier función suave de señales suaves parece "conservada".
- **La prueba (Regla 31, reproducible con `python codigo/regla31_conservada.py --nulo barajado`):** 6 réplicas sintéticas de caminatas aleatorias suavizadas, independientes entre sí — un mundo con la textura de datos reales y NADA conservado por construcción. Con el nulo viejo: **5 candidatas "serias", la mejor con score 0.0004, y jueces con ratios 0.0023–0.5 — cumplía CON MARGEN el criterio completo del prerregistro-16.** La herramienta habría parido un nodo de un mundo vacío. Peor: en el control positivo (oscilador con s1²+s2² genuinamente conservada) el nulo viejo es además CIEGO (score 0.98 — no encuentra lo que sí existe).
- **La corrección:** el nulo pasa a **surrogados IAAFT a nivel de señal** (vía `preparar(nulo="surrogado")` — conservan espectro y distribución, destruyen fases y acoples; la relación señal/cambio queda coherente). Con el nulo nuevo la herramienta **APRUEBA la Regla 31**: rechaza el mundo vacío (los jueces lo matan) y encuentra el mundo lleno (score 0.034, jueces aprueban).
- **Lección fina (tallada en el banco):** en señales NO estacionarias el score de entrenamiento (nivel A) puede sobreajustar incluso con surrogados; el verdugo DECISIVO es el nivel B — jueces fuera de muestra contra su reconstrucción surrogada. El criterio que pare nodos es A+B, nunca A solo.
- **Consecuencia sobre el árbol:** E2-N-004 pasa a **CUARENTENA** (no poda — la evidencia de Michigan puede sobrevivir al nulo corregido, y si sobrevive el nodo queda MÁS fuerte). Re-corrida encolada; requiere la máquina de los datos.

## HALLAZGO 2 — la Regla 11 llevaba ~25 campañas sin ejecutarse
`descubrir_pool.py` — la ruta de TODAS las campañas desde el prereg-08 — no tenía opción `--nulo`. Los únicos nulos en disco (`nulo-ruido`, `nulo-barajado`) son del día 1, con la tubería vieja. Ninguna campaña de la Época 2, ni percepción, ni bucle interior, tienen verdugo corrido con SU tubería.
- **Corrección:** `--nulo {barajado,ruido,surrogado}` implementado en `descubrir_pool.py`; el resumen registra el nulo; la corrida imprime su naturaleza y su veredicto. **Obligación nueva (parte de la Regla 31): toda campaña que aspire a nodo corre su nulo con su misma tubería.** Nulos de las campañas insignia (e2-mendeley-i2, p13-latente, p14-final) encolados; requieren la máquina de los datos.

## HALLAZGO 3 — la memoria de la mente estaba contaminada con sus verdugos
`MEMORIA-MENTE.jsonl` registraba `nulo-ruido` como campaña con "mejora 0.6567" — la mente "recordaba" haber mejorado un 65% prediciendo ruido puro, y `curiosidad.py` decide con esa memoria. **Corrección:** `memoria.py` marca los nulos (`"nulo": true`, sin mejora ni hueco), `curiosidad.py` y `boleta.py` los excluyen. El archivo jsonl NO se edita (append-only se respeta): el filtrado es por código.

## HALLAZGO 4 — la boleta tenía notas escritas a mano
`"leyes_humanas_redescubiertas": 3` y `"automejoras_validadas": 1` estaban hardcodeadas. Además "3 leyes redescubiertas" era generoso: π/180 es una CONVERSIÓN DE UNIDADES (valiosa, pero no una ley de la naturaleza), y la caída es coincidencia estructural con reserva del propio comparador. **Corrección:** la boleta solo contiene lo contable desde disco; los juicios de valor viven en los informes y el comparador, firmados por el director.

## HALLAZGO 5 — la comparación insignia de la automejora no era comparable
El "71.9% vs 65%" de N-003-E2 compara reducciones **contra bases distintas, en espacios latentes distintos (4 vs 8 señales)**. El INFORME-16 ya lo advertía; el titular lo perdió. El nodo se mantiene (su 5/5 contra su propio umbral prerregistrado es real) con el reclamo corregido en el propio nodo.

## HALLAZGO 6 — dos fugas confesadas, ahora por escrito
1. **El orquestador es la fuga del cortafuegos:** un LLM lleno de física humana elige tubería, operadores, jueces y KPIs. Caso concreto: la AUDITORIA-PENDULO-DOBLE usó literatura de caos para rediseñar la vara del sistema investigado. No es eliminable; queda CONFESADA (como la gota de los operadores, Sección 5 de CIMIENTOS) y debe ir en el paper.
2. **`--centrar` usa la media de la réplica completa** (incluida la parte juzgada). Fuga leve (usa solo las entradas, práctica estándar), documentada; corregirla rompería la comparabilidad con campañas pasadas — decisión: se documenta, no se re-escribe la historia.

## SOBRE LAS REGLAS (decisión de consolidación, aprobada por el director)
**No se borra ninguna regla.** Las Reglas 1–19 son el corazón y están sanas; las 20–23 son horizonte inofensivo; borrar reglas con historia crearía más confusión que limpieza. La suciedad real era: (a) la Regla 15 contradicha en la práctica por las 28–30 sin enmienda formal, (b) los conteos inconsistentes ("26 reglas", "27 reglas", "30 reglas" en el mismo documento), (c) la casilla ausente que esta auditoría talló. Correcciones: **enmienda de reconciliación a la Regla 15**, conteos unificados, y la **REGLA 31** (texto en CIMIENTOS.md):

> **Regla 31 — Toda herramienta debe fallar donde no hay nada.** Antes de que una herramienta de descubrimiento produzca su primer nodo — y tras todo cambio de su lógica de veredicto — se corre sobre datos sintéticos que POR CONSTRUCCIÓN carecen del fenómeno que busca, con la textura de los datos reales (no solo ruido blanco: datos estructurados pero vacíos), y sobre un control positivo que sí lo contiene. Si encuentra algo en el vacío o no encuentra lo que existe, la herramienta no puede producir nodos. Además, toda campaña que aspire a nodo corre sus pruebas nulas (Regla 11) con SU MISMA tubería. Los casos de la Regla 31 se congelan en el banco de pruebas.

## LO QUE ESTA AUDITORÍA NO PUDO CORRER AQUÍ (encolado, requiere la máquina de los datos)
1. Re-corrida F3 **caída** y **Michigan** con `--nulo surrogado` (decide la cuarentena de E2-N-004).
2. Nulos surrogados de las campañas insignia (e2-mendeley-i2, p13-latente, p14-final).
3. `dimension.py` sobre dp Morpheus, caída y Mendeley — la dimensión intrínseca como primer paso (replanteo de la AUDITORIA-PENDULO-DOBLE, ya implementado y con banco).

## CONGELAMIENTO (orden del director, punto 6)
**Una semana sin construcción nueva** (voz, gimnasio, plataforma B/C, F4, F5): solo re-verificación, nulos pendientes y dimensión intrínseca. El proyecto no necesita más órganos; necesita que los que tiene digan la verdad.

## Registro de verificación de esta auditoría
- Banco congelado: 24/24 OK tras todos los cambios (7 casos nuevos agregados, ninguno viejo tocado).
- `regla31_conservada.py --nulo surrogado`: APRUEBA (vacío rechazado, lleno encontrado).
- `regla31_conservada.py --nulo barajado`: REPRUEBA (5 falsos positivos en el vacío + ciega en el lleno).
- Todo determinista (semillas fijas), sin datos del proyecto: cualquiera puede reproducirlo con solo el repo.
