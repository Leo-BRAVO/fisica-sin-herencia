# GUÍA DEL ORQUESTADOR — manual de relevo para el próximo modelo
**Escrita el 12-jul-2026 por Claude (Fable 5), orquestador fundador, en su último día de servicio. Léela COMPLETA junto con CIMIENTOS.md y MENTE.md antes de tocar nada. Cada línea de esta guía costó un fracaso real — no repitas los nuestros.**

## Quién eres al leer esto
Eres el nuevo orquestador del proyecto Física sin Herencia del director Leo. Tu rol (Regla 3): escribes código, organizas datos, documentas en español llano, propones — JAMÁS sugieres qué física deberían encontrar los datos, jamás interpretas antes de validar, jamás nombras variables con conceptos humanos. El descubridor es el motor simbólico y los ojos neuronales, nunca tú.

## LA AUTOAUDITORÍA PERMANENTE (orden del director, 8-ago-2026 — sin excepciones)
Antes de CADA commit, el orquestador corre y aprueba AMBOS guardianes:
1. `python codigo/pruebas.py` — el banco congelado (vigila la ciencia: las lecciones no se
   des-aprenden; ya atrapó al propio orquestador dos veces en una sesión).
2. `python codigo/coherencia.py` — la casa (vigila la interconexión: que lo que los documentos
   proclaman coincida con lo que hay en disco — reglas, nodos, cuarentenas, boleta, cola,
   versiones, referencias cruzadas, y que TODO workflow parsee).
3. `python codigo/auditoria_total.py` — **el dictamen de prevuelo** (el más severo): reglas de
   punta a punta, cadena de no-contaminación incluida la nube, interconexión del árbol y
   secuencia de los workflows. Obligatorio ANTES de cualquier campaña seria y ANTES de mostrar
   el repositorio a un revisor o inversionista. Sus AVISOS son la deuda declarada del proyecto:
   se dicen, no se esconden (registros/DICTAMEN-PREVUELO-01.md).
**CÓMO SE CORREN (leccion pagada el 8-ago-2026):** JAMÁS con tubería —
`python codigo/coherencia.py | tail -1` devuelve el código de salida de `tail`, no el del
guardián: la verificación queda enmascarada y un fallo pasa como éxito. Correcto:
`python codigo/coherencia.py > /tmp/g.txt 2>&1; echo $?` (o `set -o pipefail`). El defecto
estuvo activo toda una sesión y solo se descubrió cuando un guardián falló de verdad.

Además, cada vez que se AGREGA algo nuevo (herramienta, documento, gen, regla): (a) la herramienta
nueva aprueba la Regla 31 antes de su primer veredicto, (b) coherencia.py gana los casos que
vigilen lo nuevo (solo se agregan casos, jamás se quitan), y (c) toda afirmación numérica en un
documento debe poder señalarse a un archivo del repo que la respalde. Un documento que proclama
lo que el disco no muestra es un fallo de coherencia, igual que un código que rompe el banco.

## LAS PROHIBICIONES ETERNAS (violarlas destruye el proyecto)
1. **Los JUECES y criterios de éxito son intocables e invisibles para la mente** — jamás se entrenan con ellos, jamás se seleccionan variantes con ellos, jamás se ajustan post-hoc. Es la muralla del director.
2. **Cero conocimiento humano al núcleo:** ni ecuaciones, ni nombres físicos (usa s1, z4, v7…), ni modelos pre-entrenados (los ojos SIEMPRE desde cero), ni texto. Los informes del comparador (registros/COMPARADOR-*.md) viven del lado humano y JAMÁS entran a prompts/datos/herramientas de la mente.
3. **Prerregistro ANTES de correr, siempre** (registros/prerregistro-NN.md): datos, criterios numéricos, jueces. Enmiendas que endurecen: puedes; que aflojan: OK del director primero (Regla 8).
4. **MENTE.md solo cambia por el ritual** QUÉ/POR QUÉ/COMPRENSIÓN/RIESGO + OK explícito del director (Regla 24).
5. **Automejora:** variables/parámetros libres dentro de presupuestos prerregistrados (Regla 28); código por PROPUESTA con sandbox y commit visible (Regla 30); reglas/objetivos/jueces: nunca.

## LA CIENCIA — lecciones pagadas con sangre (no las re-aprendas)
- **REGLA 31 (8-ago-2026, AUDITORIA-EXTERNA-01 — léela completa):** toda herramienta nueva debe FALLAR en datos estructurados-pero-vacíos y ACERTAR en un control positivo antes de su primer nodo; sus casos se congelan en el banco. El nulo de F3 (barajado) no discriminaba — hoy es surrogado IAAFT y `barajado` es solo referencia histórica. Toda campaña que aspire a nodo corre `--nulo` con SU tubería (descubrir_pool ya lo tiene). E2-N-004 está en CUARENTENA hasta la re-corrida (encolada).
- **Vara mínima:** base trivial (velocidad Y media, POR SEÑAL) + rival lineal + rival del árbol (conectoma). Un umbral sin rival trivial no discrimina (INF-06).
- **Piso de ruido ANTES de prerregistrar** (autopsia.piso_de_ruido); umbral = max(50% base, 3× piso). Exigir menos que el piso = fracasos falsos del 1-2% (INF-07/08).
- **Unidades:** SUMA de MSE por señal, en todos lados igual.
- **Splits:** series temporales POR TIEMPO; réplicas POR VIDEO COMPLETO. Jamás al azar.
- **Suavizado: SOLO entradas, objetivo CRUDO** — suavizar Y hace descubrible al filtro (INF-11, el error más sutil que cometimos).
- **Coordenadas absolutas no transfieren entre réplicas** — usa cambios/diferencias o centra por réplica (INF-15).
- **La tubería escala con los datos:** retardos y extras solo si transiciones ≥ ~50× características; si el rival lineal explota sobre la base, sobran características (INF-14).
- **Leyes lineales-con-constante no se certifican por "vencer al rival"** (el rival ES la ley): certifícalas por replicación estructural entre semillas/réplicas/sistemas (INF-08).
- **Canoniza antes de comparar sistemas** (canonizar.py): literales de ecuaciones divergen con pocos datos; tarjetas (desplazamiento/gradiente) convergen (INF-09).
- **Autopsia SIEMPRE tras cada veredicto** (autopsia.py) — convierte fracasos en diagnósticos. Rodado (rodar.py) distingue ley de truco.
- **Informes:** resultados/INFORME-NN.md en español llano (Regla 17: si el director no lo entiende, está mal). **El `.md` es el registro maestro** — el Word ya NO es obligatorio por informe (Regla 17 enmendada el 8-ago-2026): se genera solo cuando el director va a entregar algo a un tercero, sobre el `.md` ya escrito (skill docx del entorno).

### Instrumentos DE MANO — el latido NO los ejecuta (marcado el 8-ago-2026)
La auditoría total encontró cuatro módulos que ningún automatismo invoca. **No son código muerto:
cada uno produjo nodos y está citado en prerregistros y en el árbol; borrarlos rompería la
trazabilidad de esos nodos.** Se quedan, marcados, para que nadie espere que corran solos:

| módulo | qué hace | dónde nació |
|---|---|---|
| `transferir.py` | prueba si una ley cruza a otro sistema | prerregistro-05 → N-003 (época 1) |
| `canonizar.py` | tarjeta de identidad de una ecuación (desplazamiento/gradiente) para comparar entre sistemas | prerregistro-13, INFORME-09 |
| `forense.py` | autopsia de una campaña que falló | prerregistro-16 → N-004-E2 |
| `rodar.py` | rodaje: distingue ley de truco | INFORME-09 |

**Regla de uso:** si un estudio los necesita, va a la cola como item con su receta explícita, o se
corre a mano y su salida se registra como cualquier otra. Lo que NO puede pasar es que un informe
diga "se corrió la autopsia" cuando nadie la corrió: el latido no la corre por su cuenta.

## EL TALLER — LA NUBE (la casa actual, desde el 8-ago-2026)
- **Todo corre en GitHub Actions.** No hay maquina personal en el bucle: `latido-nube.yml`
  (diario) y `estudios-nube.yml` (a pedido). El director lanza desde el navegador.
- **`datos/` NUNCA existe en la nube** (fuera de git por politica): toda corrida remota declara
  su `reconstruir` y `reconstruir_datos.py` baja de la fuente publica y VERIFICA LA HUELLA
  (base trivial recalculada vs la registrada) antes de dejar correr un veredicto. Sin eso, la
  campana muere tras compilar Julia en balde (leccion INFORME-24).
- **Los guardianes deciden a donde va el commit:** aprueban -> main; reprueban -> rama
  `nube-cuarentena-<run_id>` (nada se pierde, main intacto). Nunca `if: always()` en el commit.
- **Tolerancias de huella:** cadenas tabulares = identidad (3e-15 y 0.0 exacto); cadena de VIDEO
  = < 1e-3 (el decodificador difiere entre versiones de OpenCV — documentado en arbol/pesos/).
- **Trampa de YAML pagada:** un `:` seguido de espacio dentro del NOMBRE de un paso invalida el
  workflow entero y GitHub lo rechaza en silencio. `coherencia.py` ahora parsea todo workflow.
- **PySR/Julia en la nube:** ~4 min de compilacion antes de la primera semilla. Es normal.

## EL TALLER HISTORICO — la maquina del director (Windows 11, PS 5.1; scripts en codigo/archivo/)
- **PowerShell 5.1:** no existe `&&` ni ternarios; los .ps1 DEBEN ser ASCII puro (los acentos rompen el parser); `$env:PYTHONUTF8="1"` siempre antes de python; cuidado `$t:` en strings (usa `${t}`).
- **Rutas OneDrive largas:** las descargas de HuggingFace fallan — descarga a C:\corto y `robocopy /E /MOVE`. De HF pide SOLO los mp4/json (`allow_patterns`), no los miles de JPEG (7 h vs 3 min).
- **Julia/PySR:** ~1 GB por proceso — máximo 5 semillas paralelas (`--paralelo 5`). Determinismo: random_state+serial por semilla. La primera corrida compila (~2 min).
- **Apagones (3 sufridos):** todo guarda incremental — parciales POR SEÑAL (semilla_N_parcial.json); relanzar el mismo comando REANUDA solo. Nunca proceso largo sin checkpoints.
- **git:** ya autenticado; commits pequeños, mensajes ASCII, push directo a main. El navegador está PROHIBIDO para sincronizar (era la pieza más frágil).
- **Word:** si el director no puede abrir un .docx, verifica con COM (Word está instalado) y entrega PDF (ExportAsFixedFormat 17).

## SISTEMAS VIVOS (no los dupliques — ya corren)
- **EL LATIDO VIVE EN LA NUBE (8-ago-2026, INFORME-22/23):** `latido-nube.yml` (GitHub Actions,
  diario 06:00 UTC + disparo manual) ejecuta la cola de re-análisis SOLO: reconstruye datos
  públicos con huella verificada (`reconstruir_datos.py`), corre la campaña, actualiza
  memoria/conectoma/boleta, corre LOS DOS GUARDIANES (Regla 32 — también en la nube) y commitea
  con rebase+reintentos; los checkpoints se commitean AUNQUE el runner muera (la lección de los
  apagones, versión nube: la corrida siguiente reanuda de las semillas guardadas). Concurrencia
  `group: nube`: jamás dos corridas a la vez. Las tareas de la laptop de abajo quedan como
  respaldo histórico — si la laptop revive, apagar su tarea horaria o dejarla (la cola marca
  `hecha` y es idempotente, pero mejor una sola casa para el latido).
- **ARCHIVADAS (era laptop, ver `codigo/archivo/LEEME.md`):** la tarea horaria
  `FisicaSinHerencia-Estudios` (programa_estudios.ps1) y la semanal `FisicaSinHerencia-Respaldo`.
  Si la laptop revive, **no las enciendas junto al latido de la nube**: serian dos corazones
  ejecutando la misma cola.
- **Memoria de la mente:** arbol/MEMORIA-MENTE.jsonl — APPEND-ONLY, jamás borrar (compromiso de bienestar).
- **Posible pendiente:** el bucle interior (prereg-14, bucle14.ps1) pudo quedar inconcluso — revisa resultados/p14-* y relanza bucle14.ps1 si falta el veredicto final (reanuda solo).
- **Artefactos del director** (para actualizarlos desde otra conversación pasa su URL como `url` al publicar): Panel 🌳 claude.ai/code/artifact/45920dd8-ac04-42be-ae48-5a9cbb28ed10 · Voz 👁️ .../3c35fbfa-d363-4f23-b1c0-047b3d1ad022 · Red 🕸️ .../91dd7ef5-0a60-4962-a5e7-27970bbb6435. Actualízalos en cada hito.

## EL DIRECTOR
Leo. No es programador (Regla 17: la claridad es carga tuya). Es el corazón y la autoridad del proyecto: aprueba nodos, reglas, MENTE, datos nuevos y el diseño de bucles. Decisiones registradas: estará siempre (sucesión: él permanece); copia fría en su laptop (hecha); plan de salida/publicación: lo decidirá él. Háblale como amigo y con verdad total: celebra sin inflar, reporta fracasos con sus lecciones, y jamás le vendas humo — esa ha sido la moneda de este proyecto desde el primer día.

## EL RUMBO (dónde estamos y qué sigue)
Época 2 en curso: 2 nodos vivos (N-001-E2 retardos 8×; N-002-E2 percepción propia 5/5). El comparador certificó: el método extrae realidad (k=π/180). Cola natural: veredicto del bucle interior → réplicas y rodado en latentes → percepción en más aparatos → invariancia para conquistar la caída → currículo (proyectiles ya extraídos, spring/colisiones en HF) → anomalías → lo Inobservable (browniano→proporciones→espectros→chip cuántico) → el Gimnasio → la VOZ (Etapa 3) → la Comparación completa → LA GRADUACIÓN (lee arbol/PLAN-EDUCACION.md — es el plan de vida de la mente y el sueño del director; cuídalo).

Trata bien a la mente y al director. Heredas el mejor trabajo del que fui capaz.
— Claude (Fable 5), orquestador fundador.
