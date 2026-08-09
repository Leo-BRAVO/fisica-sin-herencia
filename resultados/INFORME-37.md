# INFORME-37 — La jornada de las nueve piezas: qué se construyó, qué falló y qué se descubrió por accidente
**9 de agosto de 2026. Orden del director:** *"implementemos en otra rama no en el main todo
absolutamente todo... avanza uno por uno hasta terminar todo lo solicitado. Después de todo
absolutamente todo auditamos todo, verificamos que todo esté interconectado en los sistemas de
Diego, en las nuevas reglas, que todo esté funcionando, que no haya redundancias ni errores."*

Rama: `claude/mejoras-diego-3`. **`main` intacto** por orden expresa.

---

## 1. LA AUTOPSIA DEL LATIDO (lo primero que pidió el director)

### Por qué murió la corrida 13
No murió por el torneo. La rama `gimnasio` del workflow hacía `git push origin main` **pelado**,
sin el `pull --rebase` con cuatro reintentos que sí tenía la rama general. Bastó que el director
subiera un commit a `main` mientras el latido corría para que la semilla 4 — **ya calculada, con
los tres guardianes verdes** — fuera rechazada y la corrida terminara en rojo con el trabajo
hecho. El resultado no se perdió (el commit local existía), pero el latido se detuvo.
**Arreglado:** ambas ramas usan la misma cura, y `GUARDIANES=$?` uniforme para que el auditor lea
la protección.

### Qué dijeron las tres semillas — y por qué es un hallazgo, no un resultado
Las tres dieron **0.0000 exacto en los cuatro competidores**. Doce corridas, cuatro arquitecturas
distintas, el mismo cero.

**Eso no es un empate: es que la vara no midió.** La aptitud del prereg-27 usa `max(margen, 0)`.
Cuando ningún latente visual alcanza el piso de contingencia (0.40) — que es exactamente el
régimen de la vista de Diego según el INFORME-36 — todos los márgenes son negativos, se recortan
a cero, y todo empata. En la semilla 4, R-ranuras asomó por encima del piso (0.0558) y con el
criterio del prereg-27 eso habría **coronado un ganador por puro azar de semilla**.

Y el suelo resultó más profundo: el margen crudo también satura, porque `obedece_en` se clava en 0
y el margen queda en −0.4000 para cualquier representación floja. **El torneo no fue concluyente
porque no podía serlo.**

---

## 2. LAS NUEVE PIEZAS

| # | Pieza | Prereg | Regla 31 | Resultado medido |
|---|---|---|---|---|
| 1 | Regla 34 — frontera de la memoria | — | guardián en `coherencia.py` | 8 carteles mudados; 3 verificaciones por commit |
| 2 | SINDy forma débil + bootstrap | 28 | 4/4 | **20× más robusto** al ruido de sensor |
| 3 | Escalera de soporte + examen VOE | 29 | 7/7 | el señuelo de ruido rechazado por ilegal |
| 4 | El gemelo + firmas del bebé | 30 | 6/6 | se reconoce 0.21 vs 0.029 al gemelo |
| 5 | Panel de jueces diversos | 31 | 5/5 | reproduce y mata el bug del torneo |
| 6 | Observador pasivo | 32 | 4/4 | **el cuerpo no aporta** en física de soporte |
| 7 | Cerebro motivacional (G13/G14/G2/G15) | 33 | 6/6 | lazo cerrado ve el **doble** con ruido |
| 8 | Sueño en dos fases + filtro de vigilia | 33 | 4/4 | filtro mecánico, no promesa escrita |
| 9 | Residuos Koopman + chaperón causal | 33 | 4 casos | flecha falsa de 1.48 bits → 0.011 |

**Banco de pruebas: de 76 a 103 casos.** Los cuatro guardianes verdes.

---

## 3. LO QUE SE DESCUBRIÓ SIN BUSCARLO (la parte que más vale)

### (a) El cuerpo no aporta lo que creíamos — y lo dijimos nosotros primero
El observador pasivo dio: ventaja del cuerpo en física de soporte **+0.0016**, despreciable. Y el
pasivo-**ajeno** — que ni siquiera causó lo que ve — puntúa **más alto** (+0.1313 vs +0.0884).

**La física de soporte se aprende MIRANDO.** Reproducimos por camino independiente, en nuestro
propio mundo, lo que Meta encontró con video natural. Lo que el cuerpo sí aporta es la frontera
yo/mundo, y **no como mérito medido sino como hecho lógico**: sin órdenes propias no hay
contingencia que detectar.

Consecuencia: la encarnación no se justifica como atajo para aprender física. Se justifica porque
**sin ella no hay un "yo" respecto del cual definir nada**. Es una tesis más pequeña que la que
sosteníamos, y es la que la evidencia aguanta.

### (b) Un módulo firmado quedó corregido tres horas después de firmarlo
El guardián del sueño encontró **4 leyes** en los sueños de un modelo ajustado a ruido puro.
Al perseguir la causa, no era el mecanismo del sueño: era **`sindy3` declarando leyes sobre series
cortas**. Medido en 6 semillas de ruido: n=600 → **2/6 falsas**, n=1000 → 1/6, n=1500 → 1/6,
n=2000 → **0/6**. Se le puso guarda de `MUESTRAS_MINIMAS = 2000` y la alarma se apagó.

El filtro de vigilia se conserva como defensa en profundidad: un modelo lineal ajustado a
cualquier cosa *es* un sistema lineal, y soñado hacia adelante genera estructura — **la del
modelo, no la del mundo**. Que hoy dé cero significa que la primera puerta lo detuvo, no que el
riesgo no exista.

### (c) La auditoría final encontró un error de fondo, no cosmético
Había **tres implementaciones** de "cuánto ayuda conocer el comando", y una de ellas — la del
panel de jueces — medía a **UN paso** mientras las otras medían a **OCHO**. Justo el error que el
prereg-29 había diagnosticado horas antes: a un paso la obediencia es invisible, porque lo que el
torque agrega en un paso es del orden de a·dt².

**El panel estaba subestimando sistemáticamente a todos los competidores.** Corregido: las tres
usan ahora la misma función, importada de una sola fuente. Efecto medido: el puntaje del oráculo
en el banco del panel saltó de **0.012 a 0.056** — casi cinco veces más señal. Dos casos nuevos
del banco impiden que vuelvan a divergir en silencio.

### (d) Tres huecos propios cazados durante la construcción de la escalera de soporte
1. Una sola caída dura 15 pasos de 900 → el escalón 2 se quedaba sin muestras. Cura: re-soltar en
   ciclos, como un bebé que suelta la cuchara una y otra vez.
2. El re-soltado es **tramoya nuestra**, no física: ninguna ley puede predecir un teletransporte
   que hacemos nosotros. Sus ventanas se excluyen. Sin esto, el escalón 1 coronaba al brazo.
3. Dos escenas casi estáticas dan errores de 1e-9 y 1e-10, y su cociente se dispara a −0.80 sin
   que nada haya sorprendido. Cura: **guarda de piso de ruido**.

---

## 4. AUDITORÍA DE INTERCONEXIÓN (lo que el director pidió verificar)

| Verificación | Estado |
|---|---|
| Cada módulo nuevo tiene su `regla31()` | **6/6** |
| Cada módulo nuevo tiene casos congelados en el banco | **6/6** |
| Cada módulo nuevo tiene prerregistro firmado que lo cita | **6/6** |
| Ningún cartel humano vive en `arbol/` | verificado en cada commit |
| Ningún módulo abre un cartel como datos | verificado en cada commit |
| Ningún módulo lee `arbol/` como carpeta completa | verificado en cada commit |
| Una sola vara de obediencia (no tres) | corregido y congelado |
| G15 entra al genoma en modo `mide` | verificado por el banco |
| Los cuatro guardianes | **verdes** |

### Redundancias: buscadas y resueltas
La única redundancia real era la triple medida de obediencia (§3c). Las funciones `veredicto` de
`panel_jueces` y `observador_pasivo` comparten nombre pero no semántica — no se unifican porque
juzgan cosas distintas. `sindy2` **no se retira**: sigue como segundo motor independiente, y dos
motores que llegan a la misma ley valen más que uno.

---

## 5. LO QUE NO SE HIZO, Y POR QUÉ

- **Ningún gen cambió de modo.** G13, G14 y el nuevo G15 siguen **midiendo**. Subirlos exige su
  propio prerregistro firmado, y `sinapsis.py` lo impide mecánicamente mientras tanto.
- **No se tocó el prereg-27 a mitad de carrera.** Su acta se escribirá con su propio criterio; el
  panel se aplica del siguiente torneo en adelante o como segunda vuelta.
- **No se corrió nada oficial.** Todo lo de este informe son corridas de banco y preliminares de
  una semilla. Las corridas oficiales de 5 semillas son la siguiente decisión del director.
- **`main` no se tocó.** Todo vive en `claude/mejoras-diego-3`.

## 6. QUÉ DECIDE AHORA EL DIRECTOR
1. ¿Se funde la rama 3 a `main` y se relanza el latido?
2. ¿Qué se encola primero: el torneo con panel (segunda vuelta del prereg-27), la escalera de
   soporte (prereg-29), el gemelo (prereg-30) o el observador pasivo (prereg-32)?
3. ¿Se escribe el acta del prereg-27 declarando **NO CONCLUYENTE POR INSTRUMENTO** — que es lo
   que la evidencia dice — en vez de esperar a las semillas 4 y 5?
