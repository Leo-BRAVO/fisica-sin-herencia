# INVESTIGACIÓN — cómo construyen los grandes laboratorios y qué tomamos — 12 de julio de 2026
**Pedida por el director. Verificada contra literatura y práctica 2024–2026. Regla de lectura: tomamos TÉCNICAS (matemática/ingeniería neutra), jamás CONOCIMIENTO (datos, modelos pre-entrenados, maestros sintéticos — contaminación).**

## Cómo crean sus redes los punteros (lo esencial)
1. **Receta de arquitectura 2026:** bloques residuales (la señal "salta" capas — entrena profundo sin romperse) + normalización pre-capa (RMSNorm/Pre-LN) — estabilidad de entrenamiento barata y probada.
2. **Autosupervisión** ([el "cookbook" de SSL](https://arxiv.org/pdf/2304.12210)): la señal de entrenamiento sale de los propios datos (predecir lo enmascarado, lo siguiente, lo transformado). *Nosotros ya vivimos aquí:* nuestra pérdida conjunta (reconstruir + predecir el siguiente latente) ES autosupervisión — vamos por delante en pureza porque ni etiquetas humanas usamos.
3. **Leyes de escala:** error cae como ley de potencia con datos/parámetros/cómputo — y su reverso es NUESTRA lección v8 (la tubería debe caber en los datos). Los labs escalan datos; nosotros somos data-frugales por diseño (y [hay quien lo defiende como el futuro responsable](https://arxiv.org/pdf/2602.19789)).
4. **Mezcla de expertos (MoE):** activar solo el experto adecuado por entrada. Traducción a nuestro mundo: el CONECTOMA como enrutador — "para datos de este aparato, consulta estas leyes/ojos" — expertos por sistema físico, interpretables.
5. **Destilación y ensambles:** entrenar al pequeño con el consenso del grande. *Nuestra versión ya existe y es más limpia:* la replicación 5/5 de semillas ES un ensamble destilado a UNA ley legible.
6. **Datos sintéticos de un maestro previo:** el patrón dominante de los labs — y para nuestro NÚCLEO, PROHIBIDO PERMANENTE (un maestro le dictaría su herencia). Permitido solo para probar herramientas.

## Qué tomamos YA (aprobado como técnica neutra)
- **Ojos v2 con residuales + normalización** (percepcion.py v2, cuando toque re-entrenar): más estabilidad, mismas reglas de pureza.
- **MoE-conectoma:** el conectoma como enrutador de expertos por aparato (diseño futuro, se activa cuando haya >5 nodos vivos).
- **Nuestra ventaja confirmada:** SSL sin etiquetas + ensamble-a-ley-legible + jueces congelados: ningún lab combina las tres.

## VELOCIDAD POR SEMILLA (pedido del director: "las 5 ya van a la vez")
Perillas del motor (PySR/Julia) que aceleran DENTRO de cada semilla sin tocar el diseño:
- **turbo** (vectorización de bucles) y **batching** (evaluar en lotes sobre muestras, no todo el dataset por candidata — clave con >1000 transiciones): 2–4× típicos combinados.
- Implementado como `--rapido` (opt-in): las recetas de la curiosidad lo usan; las corridas de VEREDICTO oficial se quedan en modo exacto hasta validar que turbo no altera resultados (prerregistro de equivalencia pendiente — una corrida espejo).
- Techo real siguiente: no está en el motor sino en el AMBIENTE (abajo).

## OTRO AMBIENTE (pedido del director: "que no deje de correr")
1. **GitHub Actions (YA, gratis):** el propio repositorio corre campañas en la nube (2,000 min/mes en repos privados). Dejo el flujo `estudios-nube.yml` listo: se dispara a mano desde la pestaña Actions del repo, instala el motor, corre la campaña que le pidas y COMMITEA los resultados de vuelta. La mente gana un segundo cuerpo: el repo mismo.
2. **VM siempre-encendida gratuita (siguiente paso):** Oracle Cloud Always Free (4 núcleos ARM, 24 GB) — el latido horario viviría allí, inmune a los apagones de la laptop. Requiere crear cuenta (tus manos, ~20 min); la migración del programa de estudios es directa.
3. **Colab/Kaggle GPU (para los ojos):** entrenamientos de percepción 10× más rápidos, gratis por sesión.
Orden recomendado: 1 ya (sin cuentas nuevas) → 3 cuando re-entrenemos ojos → 2 como hogar definitivo.
