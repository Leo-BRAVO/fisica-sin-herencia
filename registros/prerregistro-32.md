# Prerregistro 32 — El observador pasivo: el control que podría refutarnos — 9 de agosto de 2026
**Estado: FIRMADO por el director el 9-ago-2026 ("implementemos todo absolutamente todo").**

## Por qué (honestidad ofensiva, no defensiva)
Todo el proyecto apuesta a que la **encarnación** — tener cuerpo, actuar, sentir las consecuencias
— es lo que permite descubrir física sin heredarla. Pero en 2025 Meta publicó que la física
intuitiva (permanencia de objetos, consistencia de forma) **emerge de video pasivo**, sin cuerpo y
sin acción. Si eso vale también para la física de soporte, entonces buena parte de lo que le
atribuimos al cuerpo de Diego **no se debe al cuerpo**.

Queremos saberlo nosotros, y antes que un tercero. Este prerregistro se firma **sabiendo que puede
refutar una parte de nuestra tesis**, y comprometiendo por escrito que el resultado se publica
salga como salga.

## Qué se construye
`codigo/observador_pasivo.py` — las tres condiciones, sus dos capacidades y el veredicto que se
escribe gane quien gane.

## El experimento, en una línea
Mismo mundo, misma dieta sensorial; la única diferencia es el acceso a las propias órdenes.

| Condición | Qué ve | Copia eferente |
|---|---|---|
| **ENCARNADO** | sus propios episodios | **sí** |
| **PASIVO-PROPIO** | exactamente los mismos episodios | no |
| **PASIVO-AJENO** | episodios de **otro** agente | no (ni podría) |

Y se comparan en **dos capacidades de naturaleza distinta**:
1. **Frontera yo/mundo** — exige acción *por construcción*. Que el encarnado gane aquí **no es
   evidencia de nada**: es el control positivo de que la comparación ve diferencias.
2. **Física de soporte** (escalón 2 + examen VOE del prereg-29) — aprendible mirando. **Aquí está
   la pregunta honesta.**

## Regla 31 declarada antes de correr (cuatro casos)
1. **Control positivo:** el encarnado gana la frontera yo/mundo. Si ni ahí ganara, la comparación
   sería ciega y ningún empate posterior significaría nada.
2. **Gemelos:** dos medidas de la misma dieta dan lo mismo — no se fabrican ventajas del ruido.
3. **Ventaja plantada:** con un examen trivializado (lo "imposible" ya no lo es) el puntaje debe
   bajar — la vara reacciona a lo que mide.
4. **Pasivo-ajeno** no puede plantear la frontera: sin copia eferente no hay contingencia posible.

**APRUEBA 4/4.**

## Un hueco propio grave, cazado al leer el primer resultado
La primera corrida dio **diferencia 0.0000 exacta** entre encarnado y pasivo-propio. Demasiado
limpia para ser una medición — y lo era: **las medidas de soporte no consultaban los comandos**,
así que ambas condiciones veían el mismo número por construcción. El "empate" no significaba nada.
**Cura:** el modelo del mundo del encarnado se aprende **con la copia eferente incluida** — predice
el próximo estado sabiendo también lo que acaba de ordenar. En el examen su copia eferente es cero
(son escenas que él no actuó): es la única lectura honesta, no se le puede dar un comando que no
emitió. Congelado en el banco: si alguien vuelve a quitar los comandos del modelo, el banco grita.

## Resultado de la corrida preliminar (semilla 1, 9-ago-2026 — NO oficial)
| Condición | Frontera yo/mundo | VOE flota | VOE atraviesa | Nulo natural | Puntaje soporte |
|---|---|---|---|---|---|
| **Encarnado** | **2 canales suyos** | +0.9999 | +0.0884 | +0.0358 | **+0.0884** |
| **Pasivo-propio** | 0 (imposible) | +0.9999 | +0.0868 | +0.0355 | +0.0868 |
| **Pasivo-ajeno** | 0 (imposible) | +0.9999 | **+0.1313** | +0.0348 | **+0.1313** |

**Ventaja del cuerpo en física de soporte: +0.0016 — despreciable.** Y el pasivo-ajeno, que ni
siquiera causó lo que ve, puntúa **más alto**.

## Lo que esto dice, escrito sin suavizar
- **La física de soporte se aprende MIRANDO.** El cuerpo no aporta aquí. Reproducimos por camino
  independiente, en nuestro propio mundo, lo que Meta encontró con video natural.
- **Lo que el cuerpo sí aporta es la frontera yo/mundo** — y no como mérito medido, sino como
  hecho lógico: sin órdenes propias no hay contingencia que detectar. Un observador pasivo no
  puede plantearse la pregunta "¿cuál de estas cosas soy yo?".
- **Consecuencia para el proyecto:** la encarnación no se justifica como atajo para aprender
  física. Se justifica porque **sin ella no hay un "yo" respecto del cual definir nada** — ni el
  no-yo, ni la agencia, ni los hitos que vengan. Es una tesis más pequeña que la que sosteníamos,
  y es la que la evidencia aguanta.

## Criterio de la corrida oficial (5 semillas)
- **EL CUERPO APORTA** si la diferencia en física de soporte supera 0.05 en ≥4/5 semillas.
- **EMPATE** en caso contrario — y se escribe en el árbol como resultado, no como nota al pie.
- La preliminar apunta claramente al empate. Se registra la predicción **antes** de la oficial.

## Qué NO se afirma
- No se afirma que la encarnación sea inútil: se afirma que **para esta capacidad concreta**, en
  **este mundo**, no aportó. Otras capacidades (manipulación, causalidad por contacto activo,
  experimentación dirigida) no están medidas aquí.
- Umbrales (0.05 de diferencia, 900 pasos mínimos) **congelados aquí**.

## Firmado
Leo, director — 9-ago-2026, aprobación en conversación.
