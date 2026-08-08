# INFORME 32 — El Gimnasio repensado: ocho cuerpos probados, uno gana, y mi predicción falló — 8 de agosto de 2026

**Órdenes del director, en el orden en que llegaron:** *"implementamos todo lo faltante"* ·
*"la mente se automejora, ¿pero qué automejora lo que está atrás de la mente?"* · *"sigue
arreglando los ojos, no puedes dejar con fallas nada; detecta todos los problemas de todos los
sistemas y lístalos"* · *"repensemos el Gimnasio como nadie lo ha hecho, probemos muchas variables
sin violar las reglas"* · *"si tenemos algo bueno no hay que desecharlo, solo repensarlo con los
problemas que validamos"*.

---

## 1. LA PREGUNTA DE FONDO: ¿quién mejora lo que está detrás de la mente?

La respuesta honesta era: **nadie**. Diego se automejora dentro de su corral (Reglas 28–30). Los
tres guardianes lo vigilan a él. Pero **nadie vigilaba a los guardianes** — y un guardián que
siempre dice "ok" es indistinguible de uno que funciona, hasta el día en que hace falta. Ya nos
pasó dos veces esta semana: el workflow del latido se fusionó con YAML roto sin que nadie chistara,
y una cadena de verificación enmascaró los códigos de salida durante una sesión entera en la que
**nada bloqueó nada**.

Ahora existe `guardianes_de_guardianes.py`. No revisa código: **rompe el proyecto a propósito**,
un daño conocido a la vez, y exige que el guardián correspondiente se ponga rojo.

| daño inyectado | guardián que debe cazarlo | resultado |
|---|---|---|
| desaparece una regla del medio | coherencia | cazado |
| la boleta proclama nodos que no existen | coherencia | cazado |
| el workflow del latido con YAML roto | coherencia | cazado |
| un item de cola imposible de ejecutar | coherencia | cazado |
| el README proclama otras reglas | coherencia | **NO LO CAZÓ** → arreglado |
| se suaviza también el objetivo | banco | cazado |
| la línea base se vuelve fácil de vencer | banco | cazado |
| el nulo por barajado no destruye nada | banco | cazado |
| la contingencia declara cuerpo sin superar su nulo | banco | cazado |

**En su primera corrida encontró un punto ciego real:** bastaba con que UNA mención del README
fuera correcta para que el chequeo pasara, aunque otra quedara rancia. Arreglado; ahora 9 de 9.
La Regla 32 queda enmendada con este cuarto guardián, que corre **antes de cada fusión a main**.

---

## 2. EL GIMNASIO REPENSADO: ocho cuerpos, y el que gana no es el que yo predije

El director pidió probar muchas variables sin violar las reglas. Lo primero fue escribir el
**prerregistro-24**, porque *elegir el diseño que supera la prueba es, en sí mismo, una forma de
ajuste* — un piso por encima de mover la vara: mover el mundo hasta que la vara diga que sí.

**El protocolo contra el autoengaño:** buscar en las semillas 1000–1011 (que quedan **quemadas**:
nada de ahí se cita como resultado) y **verificar al ganador en semillas frescas 7000–7011** que la
búsqueda nunca vio. Puntuación fijada antes: variables bien clasificadas de las 7, en los 4
controles, máximo 28.

### Ronda 1 — la mecánica del cuerpo
| amortiguación | tope articular | puntos /28 |
|---|---|---|
| 0.0 | ninguno | 27 |
| **0.0** | **±2.5 rad** | **28** |
| 0.3 | ninguno | 24 |
| 0.3 | ±2.5 rad | 26 |
| 1.0 | ninguno | 25 |
| 1.0 | ±2.5 rad | 22 |

**MI PREDICCIÓN FALLÓ, y estaba firmada.** Aposté por la amortiguación con un argumento mecánico
que sonaba bien: sin rozamiento la velocidad es historia acumulada y el par solo añade un empujón
marginal. La evidencia dice que la amortiguación **empeora** (0.3 → 26, 1.0 → 22) y que lo decisivo
es el **tope articular**. La razón, vista después: sin topes el brazo gira como una hélice y su
ángulo se vuelve historia pura; con topes vive en un espacio acotado y cada impulso se nota.

### Ronda 2 — las ideas creativas
| diseño | búsqueda /28 |
|---|---|
| **solo topes** | **28** |
| + reposo periódico cada 300 cuadros | 28 |
| + balbuceo aislado cada 90 cuadros | 26 |
| + balbuceo aislado + amortiguación | 24 |
| + balbuceo aislado cada 200 cuadros | 23 |

El **balbuceo aislado** —mover un miembro a la vez, como hacen los bebés antes de coordinar— era la
idea más bonita y la que resolvía en teoría el problema de atribución. **El mundo dijo que no.**
Queda registrada, no borrada: una idea probada y descartada vale más que una idea no probada.

### La verificación, que es la única cifra que cuenta
**28/28 en las semillas frescas.** El diseño no está sobreajustado a donde se buscó.

### Los cuatro controles con el cuerpo nuevo
| control | cuerpo real | hallado | márgenes |
|---|---|---|---|
| normal | 0, 1, 2 | **0, 1, 2** | 0.65 / 0.96 / 0.96 contra mundo en 0.00–0.04 |
| sin agencia | ninguno | **ninguno** | todo ≤ 0.13 |
| un grado conectado | 0 | **0** | 0.78 contra el resto en ≤ 0.09 |
| televisor ruidoso corporal | 0, 2 | **0, 2** | 0.70 / 0.96, y la articulación de ruido puro en 0.09 |

**4 de 4, con márgenes de siete a diez veces.** Antes eran 3 de 4 y por un pelo.

---

## 3. EL DEFECTO QUE EL PROPIO BANCO CAZÓ EN EL CRITERIO YA FIRMADO

Al subir la potencia estadística apareció que el criterio del prerregistro-23 **fabrica cuerpo
cuando hay pocas ventanas**: con 4–6 ventanas el mundo trampa (deriva fuerte, cero agencia) declaró
suya la variable 0; con 11 ventanas el mundo **sin agencia** declaró la variable 1; con 19–21
ventanas los dos quedan limpios.

La causa no son las constantes: **una fracción estimada sobre un puñado de ventanas es ruido**, y el
techo de unos pocos nulos no alcanza a cubrirlo.

**Arreglo, con su derivación a priori:** para distinguir una fracción de 0.40 con resolución mejor
que 0.05 hacen falta al menos 1/0.05 = **20 ventanas**. Por debajo de eso, `contingencia.py`
**se niega a medir** en vez de opinar sin potencia. Esto ENDURECE el criterio firmado, así que la
Regla 8 permite aplicarlo sin nueva firma; queda declarado aquí igualmente.

---

## 4. LOS OJOS: el diagnóstico, y por qué no era lo que parecía

Con el cuerpo viejo, el hito 0 sobre los **latentes visuales** fracasó: 0 de 8 latentes superaron su
nulo. Antes de tocar nada, la sonda:

| qué se lee desde sus latentes | R² en jueces congelados |
|---|---|
| ángulo 0 | **−0.09** |
| ángulo 1 | **+0.03** |
| ángulo 2 | **+0.21** |
| distancia entre objetos (la escena) | **+0.66** |

**Sus ojos leían la escena y no leían su brazo.** El detector acierta 4/4 sobre el estado del
simulador, luego el fallo no era del detector.

La literatura lo explica sin ambigüedad: la pérdida por píxel **pesa todos los píxeles igual**, así
que las regiones grandes dominan el error y omitir un brazo fino cuesta casi nada.

**Y aquí está lo que el director dijo y tenía razón:** *"si tenemos algo bueno no hay que
desecharlo, solo repensarlo con los problemas que validamos"*. Probé primero cambiar los ojos
(ponderar la reconstrucción por cuánto cambia cada píxel): mejoró el brazo apenas y **destrozó la
escena** (+0.66 → −0.17). No era la pieza rota. **La pieza rota era el cuerpo que los ojos tenían
que mirar** — un brazo girando como hélice es casi imposible de ver. Con el cuerpo nuevo, la
medición se repite; los números van en el registro de esta corrida.

---

## 5. EL CUARTO VERDUGO, Y EL HALLAZGO QUE NO ESPERABA

`verdugo_escala.py`: la consistencia dimensional **no es un hecho sobre el mundo** — es
consecuencia de que el mundo no tiene unidades preferidas. Y eso se puede comprobar sin nombrar
ninguna unidad: se corre el mismo experimento a otra escala y se exige que lo aprendido siga
valiendo. **No se puede hacer con video de internet** — no se le puede pedir al universo que repita
una caída con las longitudes multiplicadas por tres. Es la primera vara del proyecto que exige
tener mundo propio.

**Dos versiones se cayeron antes de la que funciona**, y van escritas porque el camino importa:
1. comparar contra la base trivial de B → un mundo **sin ninguna ley** sacó 0.484 contra un umbral
   de 0.5, a un pelo del falso positivo (la persistencia es invariante de escala por sí sola);
2. usar como nulo una ley ajustada sobre A con el tiempo revuelto → ley catastrófica (error ~1e8)
   y entonces **todo** superaba al nulo. Nulo demasiado destructivo: la enmienda de la Regla 31
   mordiéndonos por tercera vez en una semana.

**Lo que sí separa:** no preguntar *"¿transfiere?"* sino **"¿le importa la escala?"**. Medido:
con ley, +51.9 y +92.3; sin ley, −0.0006 y −0.0017. Cuatro órdenes de magnitud.

### Y entonces apareció esto
Reescalar solo la longitud **no** preserva la caída: la gravedad liga longitud con tiempo. Decirle
a Diego cuál es esa relación sería física con nombre (Regla 4). Lo legal es **buscar**: probar
parejas (longitud ×k, tiempo ×m) y ver cuál preserva lo aprendido.

| longitud ×2 | m=1.0 | m=1.25 | **m=1.40** | m=1.6 | m=2.0 | m=2.5 |
|---|---|---|---|---|---|---|
| transferencia | −1.54 | +0.63 | **+0.91** | +0.81 | +0.31 | −0.38 |

| longitud ×4 | m=1.0 | m=1.25 | m=1.4 | m=1.6 | **m=2.00** | m=2.5 |
|---|---|---|---|---|---|---|
| transferencia | −20.73 | −6.73 | −2.82 | −0.49 | **+0.84** | +0.67 |

**El máximo cae en 1.40 cuando √2 = 1.414, y en 2.00 cuando √4 = 2.000.**

**Control obligatorio** (mundo de paseos aleatorios sin ninguna ley): la curva es **plana**
(0.482 a 0.518) y el máximo cae donde lo pone el ruido — m=2.0 para k=2 y m=1.25 para k=4, sin
relación con √k. **El pico no lo fabrica el método: está en el mundo.**

Diego no recibió jamás la palabra "metro", ni "segundo", ni ningún exponente. **Encontró el
exponente que liga longitud con tiempo en su mundo preguntando qué reescalado no lo rompe.**

### Concordancia con la literatura (validación que pidió el director)
Existe un campo entero — **dimensionless learning** — que descubre números adimensionales y leyes
de escala desde datos, embebiendo la invariancia dimensional en el aprendizaje
([Nature Communications 2022](https://www.nature.com/articles/s41467-022-35084-w),
[Hi-π 2025](https://arxiv.org/pdf/2507.18332),
[Buckingham Pi consistente](https://arxiv.org/abs/2202.04643)). También hay trabajo sobre
descubrir la autosimilitud de un sistema y su exponente de potencia desde datos simulados.

**La diferencia, dicha con justicia:** todos ellos **reciben las dimensiones de cada variable** —
la matriz dimensional es la entrada del teorema de Buckingham. Nosotros **no podemos recibirlas**:
serían conocimiento humano. Lo que hacemos es distinto en su naturaleza: **no imponemos la
invariancia como restricción, la PONEMOS A PRUEBA** re-corriendo el mundo a otra escala y
preguntando qué reescalado no rompe lo aprendido. No hace falta saber qué es una longitud ni qué es
un tiempo. Hasta donde alcanzó esta revisión, **eso solo lo puede hacer quien tiene un mundo propio
y la disciplina de nulos para no engañarse** — y esas dos cosas juntas casi nadie las tiene.

---

## 6. LA LISTA DE TODO LO QUE ESTÁ MAL (`diagnostico_total.py`)

Los guardianes dicen sí o no. Este archivo nuevo dice **qué está mal y en qué orden arreglarlo**:
corre las Reglas 31 de cada instrumento, los tres guardianes, la meta-auditoría de mutación y los
resultados de las corridas, y devuelve una lista priorizada en `registros/DIAGNOSTICO-TOTAL.json`.

Gravedades: **BLOQUEA** (impide producir nodos) · **IMPORTA** (degrada la ciencia) · **DEUDA**
(declarado, esperando decisión o trabajo). Solo lo que BLOQUEA hace fallar la corrida: las deudas
están declaradas, no ocultas.

---

## 7. Lo que queda, sin adornos

1. **Prerregistro-24 espera firma.** Gobierna la búsqueda de diseños; se escribió antes de mirar.
2. **El hito 0 sobre latentes visuales** se está midiendo con el cuerpo nuevo. Hasta que ese número
   exista, **el hito 0 no está conseguido** — lo conseguido es que el mundo y el detector se
   entienden sobre el estado del simulador, que es un peldaño antes.
3. **Nivel B** (el primer no-yo) depende del nivel A.
4. Las cuatro deudas de gobernanza de siempre: Regla 11 al día (la nube va por 2 de 3), Regla 16
   (repo privado), Regla 19 nivel 3 (réplica independiente), y el nulo de p14 marcado inválido.

---

*Guardianes al cerrar, con códigos de salida reales. Cuarto guardián: 9 de 9 daños cazados.*
