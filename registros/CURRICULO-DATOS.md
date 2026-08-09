# CURRÍCULO DE DATOS — la ruta de videos y datasets del proyecto
**Documento vivo (Regla 18): detalle concreto para los próximos pasos, principios para lo lejano. Se actualiza cada vez que el árbol gana nodos.**
Creado: 9 de julio de 2026. Toda entrada debe cumplir la Regla 25 (procedencia, sin CGI, sin narración de física, sin video generado por IA).

## Cómo se avanza (criterio de aprobación de cada peldaño)
Un peldaño se aprueba cuando: (1) la corrida oficial supera su umbral prerregistrado, (2) las pruebas nulas fracasan como deben, (3) el nodo queda escrito en el árbol con sus preguntas nuevas. Solo entonces se pasa al siguiente. Saltar peldaños está prohibido por la Regla 9.

## PELDAÑO ACTUAL — 0/1: Péndulo doble (Mendeley 7yd2ntbh3w) — EN CURSO
- Trial 1 en corrida piloto (9-jul-2026). Pendiente: corrida oficial 10 semillas, pruebas nulas, Trials 2 y 3 como replicación.
- Extra disponible: validar el rastreo de video contra el sensor encoder del mismo dataset (dos instrumentos independientes midiendo lo mismo — primera validación cruzada del proyecto).
- Pendiente del director: video propio de péndulo simple (cuerda + tuerca) para la corroboración física de la Regla 19.

## PELDAÑO 2: Caída y vuelo (lo que R-la-gravedad debería unificar)
Objetivo: ver si la regularidad del péndulo reaparece en fenómenos distintos — la primera oportunidad de que un nodo unifique dominios.
- Videos propios (costo $0, cámara fija 60 fps): objetos soltados desde reposo (3 pesos distintos), lanzamientos parabólicos (pelota), rebotes.
- Fuentes existentes verificables: grabaciones de laboratorios docentes SIN narración ni diagramas (buscar en repositorios universitarios abiertos; cada video entra al catálogo con fuente/fps/licencia/indicios de edición).

### Peldaño 2b — Fase de Percepción Pura (decisión de arquitectura anotada el 9-jul-2026, propuesta del director, mejorada por el orquestador)
Hito de desacoplamiento tecnológico, no debilidad actual: el Peldaño 1 aisló el motor simbólico usando variables pre-extraídas (validado: constante k invariante entre corridas — naturaleza pendiente del test de re-escalado; NUNCA llamarla "universal" sin evidencia inter-sistema). La transición pendiente es de señales extraídas a PÍXELES PUROS:
- **Frontera de percepción:** autoencoder (Beta-VAE o similar) que descubra variables de estado directamente de los fotogramas, eliminando el rastreo clásico. **Regla de pureza inviolable:** todo componente neuronal de percepción se entrena DESDE CERO, solo con datos del proyecto — jamás modelos pre-entrenados (sus variables latentes traen la herencia de millones de imágenes humanas). El número de variables que el autoencoder necesite es en sí un descubrimiento (precedente: Columbia/Lipson).
- **Frontera del lenguaje (el oráculo):** una red recurrente (LSTM / modelos de espacio de estados) entrenada en los mismos datos como TECHO de referencia. Si las fórmulas simbólicas no igualan a la red, NO se declara "física oculta" de inmediato — la brecha debe: (a) sostenerse en datos ocultos por tiempo, (b) sobrevivir a pruebas nulas aplicadas también a la red, y (c) persistir tras aumentar el presupuesto simbólico. Solo entonces la brecha se registra como "dinámica no capturada por expresiones cortas" — un hallazgo, no un fracaso.
- **Arquitectura resultante:** redes como ojos (píxeles → variables descubiertas), evolución simbólica como lenguaje (variables → leyes legibles), verdugos juzgando a ambos. La auditabilidad no se negocia: la ley final siempre es una fórmula legible.
- **Nota de método (fitness del Peldaño 1, para replicadores):** PySR con maxsize=25 y selección por frente de Pareto (score = mejora de error por unidad de complejidad); parsimonia interna en valor por defecto — parámetro no explorado, candidato a barrido de robustez.

## PELDAÑO 3: Resortes, colisiones y rotación
- Masa-resorte filmado propio; colisiones de bolas sobre mesa (video cenital); trompos y ruedas.
- Aquí se prueba si el motor descubre cantidades CONSERVADAS (cosas que no cambian antes/después del choque) — el tipo de ley más profundo que existe.

## PELDAÑO 4 (= Fase 2 del mapa): Datos científicos públicos masivos
- **the Well** (Polymathic AI, 15 TB, gratuito): dinámica de fluidos — descargar solo escenarios elegidos por preguntas del árbol, jamás todo.
- **SDSS / datos astronómicos abiertos:** posiciones y espectros crudos.
- **CERN Open Data:** conteos de detectores al nivel más crudo disponible.
- Requisito de entrada: que MENTE.md registre método maduro (extracción, nulas y árbol funcionando sin sorpresas en peldaños 1–3).

## PELDAÑO 5 (= Fase 3): Anomalías — se define cuando lleguemos
No se mapea todavía (sería fingir conocimiento). Se construirá el catálogo `ANOMALIAS.md` (Regla 21) con los residuos documentados entre teoría humana y medición, y el árbol decidirá por dónde cavar. Principio de selección: anomalías con datos públicos crudos disponibles y efecto medible grande primero.

## PELDAÑO FUTURO (idea del director, 11-jul-2026): el chip cuántico como APARATO
No como procesador (para nuestro cómputo las computadoras cuánticas actuales son inservibles: carga de datos lenta, lectura destructiva, ruido — el motor clásico evalúa 150k fórmulas/seg), sino como INSTRUMENTO: los chips cuánticos reales accesibles por nube (IBM Quantum, minutos gratuitos) devuelven conteos de medición crudos de un sistema genuinamente cuántico. Experimento futuro: darle esos conteos a la mente — sin decirle qué son — y ver si descubre las regularidades estadísticas de la mecánica cuántica desde cero. Requisitos de entrada: método maduro en mecánica clásica (peldaños 1–3 completos), lección de canonización operativa, y prerregistro con especial cuidado en el piso de ruido del chip. Nota Fase 5: la simulación molecular con hardware cuántico será relevante cuando el proyecto llegue a materiales/medicina.

## FASE FUTURA — EL GIMNASIO (idea del director, 11-jul-2026): entorno virtual encarnado
Un mundo simulado (tierra, agua, árboles, gravedad programada) donde la mente EXPLORA con cuerpo: salta y siente que algo la ata al suelo, empuja, prueba, y gradualmente se comunica con el director. **Para qué SÍ:** entrenar la AGENCIA — la carencia mayor de la mente actual (hoy es espectadora de datos; el gimnasio le enseña a hacer preguntas al mundo con las manos: diseñar experimentos, intervenir, medir). Esa habilidad transfiere al mundo real. **Para qué NO:** las leyes descubiertas dentro del gimnasio son conocimiento sobre NUESTRO CÓDIGO (la gravedad del simulador es la ecuación que programamos) — jamás entran al árbol como física; se marcan "sobre el simulador" y se desechan al graduarse. **Reglas de pureza:** el agente arranca sin conocimiento ni lenguaje (nada de LLM interno — sería inyectarle la cultura humana entera); la comunicación con el director emerge o se media por el orquestador; el gimnasio se construye DESPUÉS del Peldaño 2b (percepción conjunta), que es su prerequisito técnico. Herramientas candidatas: motores de física ligeros (PyBullet/MuJoCo) corren en la laptop del director.

## Principios permanentes de selección de datos (para cualquier peldaño futuro)
1. El árbol pregunta, los datos responden — nunca descargar sin pregunta abierta que lo motive (anti-"tragarlo todo").
2. Preferir siempre: instrumento más crudo, procedencia más clara, licencia más limpia.
3. Cada dominio nuevo necesita su experimento propio barato de corroboración (Regla 19) — si no se puede corroborar físicamente, se marca provisional para siempre.
4. Replicar antes de avanzar: mínimo 2 fuentes independientes por regularidad.
