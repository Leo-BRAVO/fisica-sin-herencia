# INFORME 28 — Los ojos que se ganan su dimensión: la vara nueva funciona, el prerregistro tenía un hueco — 8 de agosto de 2026

## Qué se corrió (prerregistro-21, FIRMADO por el director)
Cinco pares de ojos entrenados DESDE CERO (d = 2, 3, 4, 6, 8), protocolo idéntico a N-002-E2 salvo
la dimensión, jueces 3/6/9 congelados e invisibles. Cada uno medido con la **ganancia honesta**:
`reducción(datos reales) − reducción(datos surrogados)`.

## Los números
| d | Reducción real | Reducción en el mundo falso | **Ganancia honesta** |
|---|---|---|---|
| **2** | 0.4974 | 0.4010 | **+0.0964** |
| 3 | 0.7210 | 0.7039 | +0.0171 |
| **4** *(los ojos actuales de Diego)* | **0.7496** ← el mejor rendimiento | 0.7410 | **+0.0085** ← casi el peor |
| 6 | 0.3362 | 0.4213 | −0.0851 |
| 8 | 0.6386 | 0.5518 | +0.0868 |

## EL HALLAZGO PRINCIPAL: las dos varas apuntan en direcciones OPUESTAS
**Si eligiéramos por rendimiento —como hacen todos— ganaría d=4 (0.7496). Por ganancia honesta,
d=4 queda casi último.** Es la demostración directa, en nuestros propios datos, de la tesis del
INFORME-27: el error de predicción no distingue dinámica de textura, y en este régimen elige mal.
Además: **d=4 reprodujo +0.0085 aquí contra +0.010 medido de forma independiente sobre los ojos
canónicos** — dos caminos distintos, el mismo número. La vara es consistente.

## EL VEREDICTO HONESTO: **INCONCLUSO** (y por qué eso importa más que un resultado bonito)
El prerregistro-21 comprometió dos predicciones: (1) si alguna d supera **0.10** → hay dinámica
capturable; (2) si TODAS quedan bajo **0.05** → se degrada la certificación predictiva de los nodos.
**El mejor resultado fue +0.0964: por encima de 0.05 y por debajo de 0.10. Ninguna predicción aplica.**
El prerregistro que yo escribí tenía una **banda descubierta** entre 0.05 y 0.10, y el resultado cayó
justo ahí. No se declara veredicto sobre ningún nodo.

**Y hay que decir algo más incómodo:** mi propio código **auto-declaró "predicción 2"** en cuanto
nadie superó 0.10 — pero la predicción 2 exigía que TODAS estuvieran bajo 0.05, y dos no lo estaban.
El código habría degradado dos nodos con una regla que el prerregistro no autoriza. **Corregido antes
de reportar nada**, y la corrección queda escrita en el propio código y en el resumen.
Es la segunda vez hoy que un veredicto automático mío decía más de lo que la evidencia permitía.

## Lo que la evidencia SÍ sostiene y lo que NO
- **SÍ:** las dos varas discrepan, y la ganancia honesta es reproducible entre mediciones independientes.
- **SÍ:** los ojos actuales (d=4) tienen ganancia honesta casi nula — el 72–75% de reducción es textura.
- **NO:** que d=2 sea "la dimensión correcta". Con **una sola semilla por candidata**, el patrón no es
  monótono (d=8 da +0.087, d=6 da **−0.085**). Una ganancia negativa es imposible como magnitud real:
  **es ruido**, y su tamaño (~0.09) es del mismo orden que la señal que buscamos. Con esta varianza,
  ninguna d puede declararse ganadora.

## Lo que toca (y el director decide)
**Prerregistro-22:** repetir con **5 semillas por dimensión** y declarar ganadora solo si su ganancia
honesta supera a las demás **por más de la desviación entre semillas** — la misma disciplina de
replicación que el proyecto exige desde julio, aplicada ahora a la selección de representación.
Y cerrar la banda descubierta: un criterio sin huecos, con las tres zonas definidas de antemano.
Coste estimado: 25 entrenamientos (~2 h en la nube). Es barato y es lo correcto.
