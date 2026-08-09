# Prerregistro 31 — El panel de jueces diversos: ningún juez individual corona a nadie — 9 de agosto de 2026
**Estado: FIRMADO por el director el 9-ago-2026 ("implementemos todo absolutamente todo").**

## Por qué (un bug real, cazado en la corrida 13 — no una precaución teórica)
El torneo de ojos (prereg-27) mide con una sola vara, `filogenia.aptitud`:

```
puntaje = media( max(margen, 0) ) + 0.01 * n_canales_mios
```

El `max(·, 0)` es un **suelo**. Cuando ningún latente visual alcanza el piso de contingencia del
prereg-23 (0.40) — que es **exactamente el régimen en que vive la vista de Diego** según el
INFORME-36 — todos los márgenes son negativos, todos se recortan a cero, y los cuatro
competidores empatan en **0.0000 exacto**. Ocurrió: semillas 1, 2 y 3, cuatro arquitecturas,
doce corridas, el mismo cero. La vara no medía a los competidores: medía su propio suelo.
En la semilla 4 una sola arquitectura asomó por encima del piso — y con el criterio del prereg-27
eso habría coronado un ganador por puro azar de semilla.

**Y el suelo es más profundo de lo que parecía.** Al construir este panel se descubrió que el
margen crudo TAMBIÉN satura: `margen = obedece_en − max(techo, 0.40)`, y cuando `obedece_en` cae
a 0 el margen se clava en −0.4000 para cualquier representación floja. Umbralizar es correcto
para **decidir** "este canal es mío"; es ruinoso para **ordenar** competidores.

## Qué se construye (`codigo/panel_jueces.py`)
**Tres lecturas independientes y prerregistradas de cada competidor. Ninguna la ve el competidor.**

| Lectura | Qué pregunta | Cómo se mide |
|---|---|---|
| **A — contingencia** | ¿sus latentes sirven para hallar el cuerpo? | ganancia de obediencia CONTINUA (cuánto ayuda conocer el comando a predecir el próximo latente) menos su nulo por comandos barajados. Sin umbral que aplaste. |
| **B — flecha del tiempo** | ¿aprendió movimiento o solo apariencia? | mismo video al derecho y al revés; asimetría de predictibilidad. En un mundo disipativo el futuro es más predecible que el pasado; una representación ciega al tiempo da cero. |
| **C — robustez** | ¿aguanta un mundo mal visto? | se repite A con ruido de sensor (σ=0.08) y oclusión de un parche (25%). Reportado en **absoluto**, no como fracción: una fracción sobre base casi nula infla cualquier cosa. |

Las tres se calculan **solo sobre episodios-juez** — la muralla intacta.

## La regla de oro del veredicto
- **GANA** quien gana o empata en **las tres** lecturas.
- **EMPATE TÉCNICO** si varios lo logran → decide la parsimonia declarada (navaja, no evidencia).
- **GANA CON ASTERISCO** quien gana en una lectura y pierde en otra: se registra, **no reemplaza
  los ojos oficiales sin una segunda vuelta**.
- **NINGUNO SIRVE** si nadie gana ni empata en lectura alguna.

## Regla 31 del panel, declarada antes de correr (cinco casos)
1. **Gemelos** (dos codificadores idénticos) → empatan en las tres.
2. **Oráculo plantado** (lee la verdad del simulador; trampa a propósito, jamás competidor) → gana las tres.
3. **Tramposo parcial** (gana la flecha, pierde la contingencia) → jamás recibe victoria limpia.
4. **Ruido puro** → no le gana al oráculo en ninguna lectura.
5. **SIN EFECTO SUELO** — dos representaciones distintas que el criterio viejo aplasta al mismo
   −0.4000 deben quedar **distinguibles** por el panel. Es el bug de la corrida 13 convertido en
   prueba permanente: no puede volver sin que el banco grite.

## Resultado (corrido el 9-ago-2026)
**APRUEBA 5/5.** El caso 5 con números: dos representaciones flojas que el prereg-23 aplasta al
mismo −0.4000 exacto, el panel las separa en −0.00004 vs −0.00021.

## Qué pasa con el torneo que corre ahora
- **El prereg-27 NO se toca a mitad de carrera.** Su acta se escribirá con su propio criterio, y
  ahora sabemos leerla: los ceros de las semillas 1-3 no dicen "empate", dicen "la vara no midió".
- El panel se aplica **del siguiente torneo en adelante**, y como **segunda vuelta** del prereg-27
  si su resultado sale apretado o dominado por el efecto suelo (que es lo que ya parece).

## Qué NO se afirma
- El panel no descubre nada del mundo. Es una vara mejor, no un resultado.
- Los parámetros (σ=0.08, tapa=25%, margen de empate 5% del rango) quedan **congelados aquí**.

## Firmado
Leo, director — 9-ago-2026, aprobación en conversación.
