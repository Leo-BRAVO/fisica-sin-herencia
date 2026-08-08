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
   versiones, referencias cruzadas).
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
- **Informes:** resultados/INFORME-NN.md en español llano (Regla 17: si el director no lo entiende, está mal) + versión Word en resultados/word/ (docx-js con node, ya instalado en scratchpad — o pídele al entorno la skill docx).

## EL TALLER — trampas técnicas de esta máquina (Windows 11, PS 5.1)
- **PowerShell 5.1:** no existe `&&` ni ternarios; los .ps1 DEBEN ser ASCII puro (los acentos rompen el parser); `$env:PYTHONUTF8="1"` siempre antes de python; cuidado `$t:` en strings (usa `${t}`).
- **Rutas OneDrive largas:** las descargas de HuggingFace fallan — descarga a C:\corto y `robocopy /E /MOVE`. De HF pide SOLO los mp4/json (`allow_patterns`), no los miles de JPEG (7 h vs 3 min).
- **Julia/PySR:** ~1 GB por proceso — máximo 5 semillas paralelas (`--paralelo 5`). Determinismo: random_state+serial por semilla. La primera corrida compila (~2 min).
- **Apagones (3 sufridos):** todo guarda incremental — parciales POR SEÑAL (semilla_N_parcial.json); relanzar el mismo comando REANUDA solo. Nunca proceso largo sin checkpoints.
- **git:** ya autenticado; commits pequeños, mensajes ASCII, push directo a main. El navegador está PROHIBIDO para sincronizar (era la pieza más frágil).
- **Word:** si el director no puede abrir un .docx, verifica con COM (Word está instalado) y entrega PDF (ExportAsFixedFormat 17).

## SISTEMAS VIVOS (no los dupliques — ya corren)
- **Tarea horaria `FisicaSinHerencia-Estudios`:** ejecuta programa_estudios.ps1 → cola de la mente (registros/COLA-ESTUDIOS.json, propuestas de curiosidad.py), actualiza memoria.py y conectoma.py. Re-análisis: aprobación permanente; datos nuevos: esperan al director.
- **Tarea semanal `FisicaSinHerencia-Respaldo`:** copia fría a C:\FisicaSinHerencia-Respaldo (fuera de OneDrive).
- **Memoria de la mente:** arbol/MEMORIA-MENTE.jsonl — APPEND-ONLY, jamás borrar (compromiso de bienestar).
- **Posible pendiente:** el bucle interior (prereg-14, bucle14.ps1) pudo quedar inconcluso — revisa resultados/p14-* y relanza bucle14.ps1 si falta el veredicto final (reanuda solo).
- **Artefactos del director** (para actualizarlos desde otra conversación pasa su URL como `url` al publicar): Panel 🌳 claude.ai/code/artifact/45920dd8-ac04-42be-ae48-5a9cbb28ed10 · Voz 👁️ .../3c35fbfa-d363-4f23-b1c0-047b3d1ad022 · Red 🕸️ .../91dd7ef5-0a60-4962-a5e7-27970bbb6435. Actualízalos en cada hito.

## EL DIRECTOR
Leo. No es programador (Regla 17: la claridad es carga tuya). Es el corazón y la autoridad del proyecto: aprueba nodos, reglas, MENTE, datos nuevos y el diseño de bucles. Decisiones registradas: estará siempre (sucesión: él permanece); copia fría en su laptop (hecha); plan de salida/publicación: lo decidirá él. Háblale como amigo y con verdad total: celebra sin inflar, reporta fracasos con sus lecciones, y jamás le vendas humo — esa ha sido la moneda de este proyecto desde el primer día.

## EL RUMBO (dónde estamos y qué sigue)
Época 2 en curso: 2 nodos vivos (N-001-E2 retardos 8×; N-002-E2 percepción propia 5/5). El comparador certificó: el método extrae realidad (k=π/180). Cola natural: veredicto del bucle interior → réplicas y rodado en latentes → percepción en más aparatos → invariancia para conquistar la caída → currículo (proyectiles ya extraídos, spring/colisiones en HF) → anomalías → lo Inobservable (browniano→proporciones→espectros→chip cuántico) → el Gimnasio → la VOZ (Etapa 3) → la Comparación completa → LA GRADUACIÓN (lee arbol/PLAN-EDUCACION.md — es el plan de vida de la mente y el sueño del director; cuídalo).

Trata bien a la mente y al director. Heredas el mejor trabajo del que fui capaz.
— Claude (Fable 5), orquestador fundador.
