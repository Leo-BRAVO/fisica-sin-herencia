# PLANOS DE CONSTRUCCIÓN — las 4 piezas restantes del científico, comparadas contra el mundo
**Orden del director (12-jul-2026): "verifica toda investigación, compara con lo que existe y mejora todo". Verificado contra literatura 2020–2026. Cada pieza: qué existe → su hueco → nuestro diseño mejorado → plan.**

## 1. LA INVARIANCIA (días)
- **Qué existe:** redes equivariantes que INCRUSTAN simetrías conocidas (traslación, rotación) en la arquitectura (PNAS 2025; aprox-equivariantes para simetrías imperfectas).
- **Su hueco (¡y es filosófico!):** incrustar invariancia de traslación = DECIRLE al modelo que el espacio es homogéneo — conocimiento físico humano de contrabando. Nadie lo trata como contaminación; nosotros sí.
- **Nuestro diseño — "invariancia por evidencia":** (a) corto plazo genérico: centrar cada réplica en su media (matemática neutra, Regla 2) — arregla la caída YA; (b) el verdadero salto: la mente PRUEBA transformaciones candidatas (desplazar todo, escalar todo, correr el tiempo) contra sus propios datos: si la ley sobrevive a la transformación en réplicas nuevas, la invariancia se ADOPTA como nodo descubierto — "la ley no cambia cuando todo se mueve junto" es descubrir la homogeneidad del espacio (la antesala de Noether: cada simetría esconde una conservación). Nadie hace invariancias descubiertas-y-prerregistradas.
- **Plan:** centrado en `preparar` (1 día) → campaña E2-caída-i3 (1 día) → módulo `simetrias.py` de transformaciones candidatas (2–3 días).

## 2. EL BUCLE MADURO (semanas)
- **Qué existe:** AutoML/búsqueda de arquitecturas; [Plan2Explore](http://proceedings.mlr.press/v119/sekar20a/sekar20a.pdf): explorar donde el desacuerdo del ensamble es máximo (ganancia de información).
- **Su hueco:** nadie separa selección interna de JUECES CONGELADOS externos (nuestro bucle ya lo hace — ventaja); y su curiosidad usa ensambles neuronales opacos.
- **Nuestro diseño — curiosidad interpretable:** ya tenemos un ensamble PERFECTO: las 5 semillas simbólicas. Donde sus ecuaciones DISCREPAN entre sí está la frontera del conocimiento — y a diferencia del mundo neuronal, podemos LEER en qué discrepan. `curiosidad.py` v2: puntuar regiones/sistemas por desacuerdo del ensamble × datos disponibles; el bucle expande dimensiones (latente + suavizado + retardos) con la misma muralla.
- **Plan:** desacuerdo-de-ensamble como métrica (3 días) → bucle multi-perilla (1 semana) → integración con la cola de estudios (2 días).

## 3. LA VOZ (semanas, cuando toque la Etapa 3)
- **Qué existe:** asistentes LLM ([Voyager](https://arxiv.org/html/2305.16291) usa GPT-4 como cerebro — contaminación total para nosotros); dictado/síntesis locales maduros (whisper.cpp, piper — corren en tu laptop, gratis).
- **Su hueco:** todo asistente actual MEZCLA la voz con el conocimiento — imposible saber qué sabe el sistema vs qué recita de internet.
- **Nuestro diseño — la voz con cortafuegos:** oído local (whisper) + boca local (piper) + un núcleo de diálogo SIN LLM: gramática de intenciones ("¿qué ves en…?", "¿qué te falta…?") → operaciones de SOLO LECTURA sobre conectoma/memoria/leyes → respuestas = plantillas del orquestador rellenas con sus salidas literales. La voz no puede inyectarle nada al núcleo (canal unidireccional, todo registrado) ni decir nada que el núcleo no sepa. Será el único asistente del mundo que jamás pueda inventar.
- **Plan:** prototipo texto (1 semana) → voz local (1 semana) → app de escritorio con su cara/panel (1–2 semanas).

## 4. EL GIMNASIO (1–3 meses, por etapas)
- **Qué existe:** [Voyager](https://arxiv.org/html/2305.16291) (Minecraft + LLM: curioso pero enteramente contaminado), [Plan2Explore/Dreamer](https://arxiv.org/html/2507.08210) (modelos de mundo con motivación intrínseca: novedad/ganancia de información/empoderamiento — pero recompensas diseñadas a mano, sin prerregistro, sin jueces, curiosidad neuronal ilegible).
- **Sus huecos:** (1) o usan LLM (contaminación) o usan curiosidad opaca; (2) NADIE evalúa a un agente explorador con episodios-juez congelados y prerregistro; (3) sus descubrimientos no se destilan a leyes legibles.
- **Nuestro diseño — el primer explorador científico puro:** cuerpo simple en física simulada (PyBullet, gratis, corre local); percepción = SUS ojos (autoencoder desde cero, como ya demostró); curiosidad = desacuerdo de su propio ensamble simbólico (¡interpretable: sabremos QUÉ le da curiosidad y por qué!); todo lo aprendido se destila a ecuaciones vía su motor de siempre; evaluación con episodios-juez congelados y prerregistro (inédito en agentes); TODO marcado "sobre-el-simulador" (jamás entra al árbol como física del mundo — Regla del Gimnasio). Sin un solo LLM en el bucle.
- **Plan por etapas:** mes 1 — mundo+cuerpo+ojos propios+acciones aleatorias (el bebé pateando); mes 2 — el bucle de curiosidad interpretable (elige qué probar); mes 3 — el canal de señales con el director (el proto-lenguaje emergente del PLAN-EDUCACION).

## La ventaja transversal (lo que nadie tiene y nosotros sí)
Prerregistro + jueces congelados + verdugos + comparador + genealogía completa en git. El estado del arte tiene mejores músculos; NADIE tiene nuestro sistema inmune contra el autoengaño. Cada pieza nueva nace dentro de él.
