# Prerregistro 38 — Segunda vuelta del torneo de los ojos, con la vara que sí mide — 10 de agosto de 2026
**Estado: FIRMADO por el director el 10-ago-2026 ("incluso el tema de la firma de torneo ojos").**
**Cierra la deuda abierta desde el INFORME-38: `p27-torneo-ojos-s5` llevaba desde el 9-ago en
`espera-al-director`.**

## Por qué la primera vuelta no valió
El prereg-27 dio **0.0000 exacto en las cuatro arquitecturas, en tres semillas seguidas**. No fue
un empate: **la vara no midió**. La aptitud era

```
puntaje = media( max(margen, 0) ) + 0.01 · n_canales_mios
```

y el `max(·, 0)` es **un suelo**. El margen que entra ahí ya trae otro suelo (`obedece_en − max(techo_nulo, 0.40)`).
Cuando ningún latente alcanza el piso de 0.40 —que es **el régimen documentado de la vista de
Diego**, la visión-que-se-une no replicó (1/5)— todos los márgenes son negativos, el `max` los
aplasta a cero, y los cuatro empatan. **La vara medía su propio suelo.**

Y el agravante: al construir el panel se comprobó que **el margen crudo también satura** en −0.4000,
idéntico para cualquier representación floja, por distintas que sean. Dos representaciones
deliberadamente diferentes daban el mismo −0.4000; el panel las separa en −0.00014 vs −0.00051.

## Qué cambia, y qué NO
**Cambia SOLO la vara.** Los cuatro competidores, el mundo, los jueces, las épocas y las semillas
son **exactamente los mismos**. Si cambiáramos las dos cosas a la vez no sabríamos cuál produjo el
resultado — la misma disciplina que el prereg-35 aplicó al mundo variable.

**La vara vieja no se toca ni se borra.** `torneo_ojos.py` conserva su camino del prereg-27 intacto;
la segunda vuelta entra por `--panel`. El INFORME-38 sigue siendo el acta de la primera vuelta.

## La vara nueva: el panel de tres lecturas (prereg-31, ya con su Regla 31 aprobada 5/5)
| Lectura | Qué pregunta | Por qué no tiene suelo |
|---|---|---|
| **contingencia** | ¿sus latentes sirven para hallar el cuerpo? | ganancia de obediencia **continua**, sin umbral que aplaste |
| **flecha** | ¿llevan dentro el sentido del tiempo? | error de predicción hacia adelante vs hacia atrás |
| **robustez** | ¿cuánto sobrevive al mundo mal visto (ruido y oclusión)? | se reporta en **absoluto**, no como fracción — una fracción sobre una base casi nula infla cualquier cosa: 0.001/0.0005 = 2.0 no es robustez, es división por casi cero |

## La regla de oro (congelada aquí)
**Gana quien gana o empata en LAS TRES lecturas.** Y las tres salidas posibles están declaradas
antes de correr:
- **GANA X** — único que gana o empata en las tres.
- **EMPATE TÉCNICO** — más de uno lo logra: desempata la **parsimonia** (navaja, no evidencia), y
  se escribe con esas palabras para que nadie lo lea como que ganó por mérito.
- **GANA CON ASTERISCO** — gana en unas y pierde en otras: **NO reemplaza los ojos oficiales**.
- **NINGUNO SIRVE** — ninguno gana ni empata en lectura alguna. Es un desenlace legítimo y se
  publicaría igual.

## Lo que este prerregistro NO autoriza
- **R-ranuras NO puede entrar al genoma**, gane lo que gane. La constitución lo prohíbe; compite
  solo como **ablación medida**, y esto no lo cambia.
- **El ganador no reemplaza los ojos canónicos por ganar.** Eso es un cambio de genoma y exige
  generación nueva y firma aparte (Regla 33).
- **Ninguna semilla se mira suelta.** El veredicto exige las cinco juntas: mirar antes de tiempo es
  exactamente el vicio que el prereg-27 nos cazó.

## La predicción, comprometida ANTES de correr
**Espero que salga GANA CON ASTERISCO o NINGUNO SIRVE, no un ganador limpio.** Motivo: la vista de
Diego lleva sin sostenerse desde el hito 0 (visión-que-se-une 1/5), y el gemelo (H-001) volvió a
medir que **la propiocepción distingue y la visión no**. Sería raro que cuatro arquitecturas
entrenadas sobre esa misma vista produjeran de pronto un campeón limpio.

**Si sale un ganador limpio, sospecharé de la vara antes que celebrarlo** — y el primer sitio a
mirar será la lectura de robustez, que es la más joven de las tres.

## Qué se corre
`p38-torneo-panel-s{1..5}` — las cinco semillas, una por estudio encolado.

## Firmado
Leo, director — 10-ago-2026, aprobación en conversación.
