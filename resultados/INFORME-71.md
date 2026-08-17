# INFORME-71 — ACTA DEL PRERREGISTRO 60: el estudio se anuló a sí mismo, y el culpable es mi criterio, no la política
**17 de agosto de 2026. Tres políticas, 5 semillas, 20000 pasos cada una, en un mundo donde
empujar solo funciona si la mano está cerca.**
**Datos crudos:** `resultados/p60-politica-contacto/medida.json`. Módulo:
`codigo/politica_contacto.py` (puerta 8/8).
**VEREDICTO, con las palabras del archivo de datos:** *ANULADO POR EL NULO — la política barajada
también le gana al balbuceo, así que lo que se mide no es la información sino la forma de elegir.*

---

## 1. LOS NÚMEROS, tal cual salieron

| semilla | balbuceo | intrínseca | barajada (el nulo) |
|---|---|---|---|
| 1 | 0.0085 | 0.0078 | 0.0097 |
| 2 | 0.0074 | **0.0155** | **0.0167** |
| 3 | **0.0216** | 0.0114 | 0.0030 |
| 4 | 0.0078 | 0.0071 | **0.0109** |
| 5 | 0.0132 | **0.0188** | **0.0222** |

| criterio congelado | pedía | salió | |
|---|---|---|---|
| **A** el cortafuegos aguanta | sin fugas en los dos guardianes | ✔ | ✔ |
| **B** el mundo sordo no premia | la intrínseca gana en <4 de 5 | **3 de 5** | ✔ |
| **C** la intrínseca busca sola | ≥4 de 5 | **2 de 5** | ✘ |
| **D** el nulo no gana | la barajada gana en <4 de 5 | **4 de 5** | ✘ |
| **E** no se puede inventar contacto | 0.0 con radio 0 | ✔ | ✔ |

## 2. LO QUE FALLÓ, y no es lo que parece
**La política intrínseca no buscó el contacto: ganó en 2 de 5.** Pero **eso no es lo que decide
este acta**, porque **el nulo ganó en 4 de 5** — y el nulo es una política que elige **al azar**:
su puntaje son los mismos números desordenados.

> **Un nulo que "gana" es un nulo que dice que el criterio no distingue nada.** Y aquí el fallo es
> de aritmética mía, no de la política: **con 5 semillas, una moneda justa saca 4 o más caras el
> 18.75% de las veces** (6 de 32). **Congelé un criterio de «4 de 5» sin calcular nunca qué hace el
> azar bajo ese criterio.** Casi una de cada cinco veces, el azar lo pasa.

**Así que este estudio no dice que la curiosidad no busque el contacto. Dice que mi diseño no tenía
potencia para distinguirlo**, y el nulo lo demostró antes que nadie. Es exactamente para lo que
estaba puesto.

## 3. LO QUE SÍ QUEDA EN PIE
- **El cortafuegos aguantó.** La señal declara **solo** `error_de_prediccion_propio`, y una señal
  que pagara por tocar **fue rechazada** por el guardián en la prueba de los dos lados. **El
  contacto se midió, nunca se pagó.**
- **El medidor mide.** Una política escrita a mano que va derecha al objeto marca **0.937**; con
  radio 0 marca **exactamente 0.0** para todas. No se inventa contacto.
- **El mundo sordo funciona como control** y ahí la intrínseca tampoco destacó (3 de 5).
- **El mundo es el correcto para la pregunta:** a diferencia de `mundo.py` —donde el empuje
  funciona desde cualquier sitio— aquí **tocar y no tocar son cosas distintas**, que es la
  condición mínima para que «buscar el contacto» signifique algo.

## 4. LA ENMIENDA 1, y por qué no fue una comodidad
Antes de correr nada cambié el criterio B: de «el balbuceo sigue a la geometría» a «en el mundo
sordo la intrínseca no busca». Lo declaré entonces y lo repito ahora con el dato delante:

> **La geometría predecía 0.02134 y el balbuceo dio 0.00850 — un factor 2.5.** El criterio B viejo
> pedía factor 2. **Habría fallado.** Y aun así el estudio **falló igual**, por otro lado. Cambiar
> B no me salvó de nada: cambió un criterio que examinaba **mi aritmética** por uno que examina
> **el estudio**, y el nuevo tampoco me regaló el resultado.

## 5. LO QUE **NO** SE AFIRMA
- **Nada del universo.**
- **NO se afirma que la curiosidad no produzca búsqueda de contacto.** Se afirma que **este diseño
  no puede decirlo**: su nulo lo pasa el 18.75% de las veces por puro azar.
- **NO se arregla el número de semillas y se vuelve a correr.** Subir semillas después de ver que
  el criterio no discrimina es mover el umbral con los datos delante — **lo único que este
  proyecto no perdona**. El diseño con potencia calculada es **un prerregistro nuevo**.
- **NO se conecta esta política a nada**, ni se toca `tacto.py`, `mundo.py` ni `gimnasio.py`.
- **NO se afirma que la base cuadrática sea suficiente.** Se eligió para que la dependencia del
  contacto fuera **representable** —con una base lineal el estudio habría estado amañado en contra
  desde la primera línea— pero que sea representable no es que sea aprendible en 20000 pasos.

## 6. LO QUE SE APRENDIÓ SOBRE MI MÉTODO, y va al catálogo
**Error nº26: congelar un criterio de conteo sin calcular qué hace el azar bajo ese criterio.**
«4 de 5» suena exigente y no lo es: el azar lo pasa casi una de cada cinco veces. **La regla nueva
es aritmética y barata:** antes de congelar un criterio de «k de n», se calcula
`P(X ≥ k | n, p=0.5)` y se escribe en el prerregistro. Si pasa de 0.05, **el criterio no está
listo**.

Esto **no se aplica hacia atrás por decreto**: los criterios «5 de 5» que este proyecto usa en
otros sitios dan 0.031 y aguantan; los «4 de 5» que haya hay que mirarlos uno a uno, y **no lo he
hecho**.

## 7. LA PREGUNTA QUE ABRE (Regla 18)
> **¿Cuántos criterios congelados de este proyecto los pasaría una moneda?** Hoy encontré uno.
> Contarlos es mecánico —basta la binomial— y **está sin hacer**.

## 8. LO QUE LE TOCA AL DIRECTOR
Una decisión concreta: **¿se rehace el estudio con la potencia calculada de antemano?** Sería un
prerregistro nuevo con `n` derivado de la binomial y no de mi gusto — probablemente **10 semillas
con «8 de 10»** (azar: 0.055) o **«9 de 10»** (0.011). Es una corrida de unos ocho minutos.

**Si no lo autoriza, el item 30 queda cerrado con esta respuesta:** el tacto sigue ocioso y el
barrido sigue siendo mío, **pero no porque la curiosidad haya fallado — porque mi criterio no
podía distinguirlo.** Y eso, escrito, vale más que un resultado que no se sostiene.
