# INFORME-73 — ACTA DEL PRERREGISTRO 63: no eran tres huérfanos, era uno — los otros dos corren en cada latido
**17 de agosto de 2026. El censo de órganos con las DOS vías: lo que se importa y lo que el
proyecto ejecuta.**
**Datos crudos:** `resultados/p63-anatomia2/medida.json`. Módulo: `codigo/anatomia2.py` (puerta
8/8). Defecto de origen publicado en `registros/CORRECCION-02-HUERFANOS-QUE-CORREN.md`.
**VEREDICTO, con las palabras del archivo de datos:** *1 ORGANO(S) DESCONECTADO(S) de 15, y NO 3:
interocepcion, memoria no los importa nadie pero el proyecto SI los ejecuta.*

---

## 1. LOS NÚMEROS

| censo | huérfanos |
|---|---|
| **viejo** (solo `import`) | `curiosidad2`, `interocepcion`, `memoria` — **3** |
| **con las dos vías** | `curiosidad2` — **1** |
| **rescatados por ejecutarse** | `interocepcion`, `memoria` |

| criterio congelado | pedía | |
|---|---|---|
| **A** cuenta las dos vías | ejecutado por un workflow ⇒ conectado | ✔ |
| **B** no inventa conexiones | ni importado ni ejecutado ⇒ huérfano | ✔ |
| **C** le gana al censo viejo | cambia al menos un veredicto | ✔ **cambia dos** |
| **D** no acusa por no estar sellado | sello y conexión son cosas distintas | ✔ |

## 2. LA PRUEBA, con archivo y línea
`.github/workflows/latido-nube.yml`, líneas 81–82 y 126–127 — **después de cada estudio**:

```
python3 codigo/interocepcion.py --sentir "$SALIDA" --segundos "$SEGUNDOS" || true
python3 codigo/memoria.py --retro || true
```

**Corren más a menudo que casi cualquier órgano del genoma.** El INFORME-65 los llamó
desconectados, y era **lo contrario de la verdad**.

## 3. POR QUÉ FALLÓ EL CENSO VIEJO
`anatomia.py` busca `import x` en `codigo/*.py`. **Este proyecto usa los módulos de dos formas
—importándolos y ejecutándolos— y el censo miraba una.**

Es el mismo hueco que el censo de los muertos ya había tapado para otra cosa: allí un módulo
sobrevive si un acta lo **cita**. Aquí faltaba que el proyecto lo **ejecute**. **Dos veces el mismo
descuido con dos caras distintas.**

## 4. LO QUE ESTO CAMBIA EN LA MESA DEL DIRECTOR
La decisión que estaba pendiente sobre **tres** módulos ahora es sobre **uno**:

- **`interocepcion` y `memoria`**: **no hay nada que decidir.** Están en el lazo del latido y llevan
  ahí desde antes de esta conversación. Lo que les falta es **otra cosa**: ninguno ha pasado la
  puerta, así que **corren sin ficha de sanidad**. Eso es deuda contada, no orfandad.
- **`curiosidad2`**: **el único huérfano real.** No lo importa nadie, no lo ejecuta nada, y cuelga
  del gen `G2_curiosidad` del genoma — **con un `curiosidad.py` hermano que sí existe**. Esa
  decisión sigue siendo suya, y **no la tomo yo**: archivar un órgano del genoma no es lo mismo que
  archivar una herramienta.

## 5. LO QUE SE ARREGLÓ HOY, en el mismo commit
1. **Error nº27 del catálogo**: «contar un módulo como desconectado mirando solo las
   importaciones», con **detector mecanizado** `d_huerfano_que_si_corre`, probado por los tres
   lados.
2. **El guardián estuvo en rojo hasta que el censo se arregló.** No se le puso una excepción: leyó
   el censo viejo, gritó, y ahora lee el corregido y calla. **Si algún día vuelve a publicarse un
   censo que solo mire una vía, vuelve a gritar.**
3. **`CORRECCIÓN-02`** publicada en `registros/`, no en `resultados/`: es una corrección, no un
   resultado.

## 6. LO QUE **NO** SE AFIRMA
- **Nada del universo.**
- **NO se retira el INFORME-65.** Midió conexión **por importación** y ese dato es cierto bajo esa
  definición. Lo que estaba mal era **llamar «desconectado» a eso**.
- **NO se afirma que los dos rescatados funcionen.** **Ejecutarse no es funcionar**: ninguno de los
  tres ha pasado la puerta, y una ficha de sanidad es lo único que dice si un órgano mide bien.
- **NO se archiva ni se conecta nada.** El censo mide; el director decide.
- **NO se editó `anatomia.py`.** Está sellado y su acta debe seguir siendo reproducible.

## 7. LA PREGUNTA QUE ABRE (Regla 18)
> **¿Qué otras terceras vías hay?** Hoy aparecieron dos formas de usar un módulo y el censo
> conocía una. ¿Hay una tercera —un `subprocess`, un `importlib` por cadena, una llamada desde un
> `.ps1` archivado— que siga sin contarse? **`anatomia2` mira workflows y cola. No mira nada más, y
> no lo he comprobado.**
