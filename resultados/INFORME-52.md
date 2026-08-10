# INFORME-52 — LA CADENA COMPLETA: el defecto de G14 llega hasta dónde mira Diego, y el televisor gana
**10 de agosto de 2026. Acta parcial del prerregistro-43. Hallazgo de ingeniería. No genera nodo.**
**Datos crudos:** `resultados/p43-g8-atencion/medida.json`. Módulo: `codigo/atencion.py`.
**VEREDICTO, con las mismas palabras que el archivo de datos:** *REPROBADO: el contagio SI ocurre.
Con la epistemica del televisor inflada x20 se lleva 7.036 de 10 y la region buena 2.964.*

---

## 1. YO PREDIJE QUE NO PASARÍA, Y LA MEDIDA DICE QUE SÍ
Al escribir la ficha de G8 declaré, **antes de correr**, esta relación:

> *"Inflar la epistémica del televisor ×20 **NO puede cambiar el reparto**, porque su poder es cero
> y el producto sigue siendo cero. Si cambiara, el defecto de G14 se convertiría en conducta."*

**La puerta la midió y me reprobó:** la lectura no se quedó igual, se fue a **×0.068**.

## 2. LA MEDIDA
Un **televisor** (mucha "ignorancia", cero control) contra una **región buena**, presupuesto 10:

| epistémica del televisor | se lleva el TV | se lleva la BUENA | ventaja de la buena |
|---|---|---|---|
| 1 | 1.306 | 8.694 | **6.659** |
| 2 | 2.150 | 7.850 | 3.651 |
| 5 | 3.904 | 6.096 | 1.562 |
| **20** | **7.036** | **2.964** | **0.421** ← el televisor gana |
| 100 | 9.046 | 0.954 | 0.105 |
| 1000 | 9.675 | 0.325 | 0.034 |

## 3. POR QUÉ PASA — la causa exacta, en una línea de código
El reparto usa `prioridad = epistemica * max(poder, piso_poder)` con **`piso_poder = 0.05`**.

Ese suelo existe por una buena razón —**que ninguna región quede ciega del todo**— pero tiene un
efecto que nadie había medido: **una región con poder CERO no puntúa cero, puntúa 0.05.** Y con un
suelo distinto de cero, **la epistémica inflada sí compra atención.**

## 4. LA CADENA ENTERA, que es lo que hace grave esto
1. **G14** entrega una ignorancia "curable" que es σ/√n: **una región más ruidosa llega con la
   epistémica multiplicada** (INFORME-51 — noise ×5 → epistémica ×5).
2. **G8** multiplica esa epistémica por `max(poder, 0.05)`, y el suelo **deja pasar la inflación**.
3. **Resultado: Diego reparte su atención hacia la región que no puede aprender.**

**Ninguno de los dos órganos falla solo.** G14 mide lo que un ajuste lineal permite medir; G8 tiene
un suelo defendible. **El defecto vive en la unión**, y por eso no lo habría encontrado nunca
examinando módulos por separado — apareció porque la ficha de G8 preguntó por la cadena.

## 5. POR QUÉ LA PRUEBA ANTI-TELEVISOR QUE YA TENÍAMOS NO LO CAZÓ
`pruebas.py` congela desde agosto un caso llamado *"la varianza pura NO compra fóvea"*, y **pasa**.
Pero usa un televisor con **epistémica fija en 0.05** — un televisor que ya viene declarado como
poco informativo. **Nunca probó un televisor cuya epistémica llegue inflada**, que es justo lo que
G14 produce en el mundo real.

**La lección:** una prueba anti-fallo que fija ella misma la entrada del atacante no prueba nada
sobre el atacante que de verdad aparece.

## 6. LO QUE **NO** SE HACE
- **No se toca `piso_poder`.** Bajarlo a cero dejaría regiones completamente ciegas, que es el
  problema que ese suelo resuelve. El arreglo correcto probablemente sea **normalizar la epistémica
  por la aleatoria antes de multiplicar** — pero eso cambia lo que significan los números que dos
  órganos ya intercambian, y va con prerregistro propio.
- **No se sella G8.** Reprobó. Queda registrado como **reprobado**, con causa y acta.
- **No se re-interpreta mi predicción fallida.** Está arriba, escrita antes de medir, y falló.

## 7. LA PREGUNTA QUE ABRE (Regla 18)
> **¿Cuánta de la atención que Diego ya repartió se fue a televisores?** Se contesta re-corriendo
> los repartos registrados con la epistémica normalizada y comparando. No se hace hoy.

## 8. EL BALANCE ACTUALIZADO DE LA CAMPAÑA DE LA PUERTA
**Seis órganos examinados: tres pasaron** (`contingencia`, `torneo_ojos`, `poder`) **y tres
reprobaron** (`sueno`, `incertidumbre`, `atencion`). **Quedan 9 sin examinar.**

Y el patrón de los tres fallos vale más que los tres por separado: **ninguno es un error de
programación.** Son tres decisiones razonables —un umbral, un estimador estándar, un suelo de
seguridad— que **sólo fallan cuando se miran juntas o fuera de su rango**. Eso no se encuentra
leyendo código. Se encuentra midiendo.
