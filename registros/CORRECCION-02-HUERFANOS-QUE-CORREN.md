# CORRECCIÓN 02 — Dos de los «huérfanos» corren en cada latido: el censo solo miraba `import`
**17 de agosto de 2026. Corrige el INFORME-65 y el archivo de datos del prerregistro 54.**
**Va en `registros/` y no en `resultados/` a propósito: es una corrección, no un resultado.**

---

## 1. LO QUE SE PUBLICÓ
El censo de órganos del prerregistro 54 declaró huérfanos —«nadie que no sea una prueba ni un
guardián los usa»— a cuatro módulos, y el INFORME-65 lo publicó. Tras conectar `poder` quedaron
tres: **`interocepcion`, `memoria` y `curiosidad2`.**

## 2. LO QUE ES VERDAD
**Dos de los tres se ejecutan después de CADA estudio del latido.** En
`.github/workflows/latido-nube.yml`, líneas 81–82 y 126–127:

```
python3 codigo/interocepcion.py --sentir "$SALIDA" --segundos "$SEGUNDOS" || true
python3 codigo/memoria.py --retro || true
```

`memoria.py` aparece además en `estudios-nube.yml`.

> **Corren más a menudo que casi cualquier órgano del genoma.** Llamarlos desconectados es lo
> contrario de la verdad.

**`curiosidad2` es el único huérfano real de los tres:** no lo importa nadie y no lo ejecuta ningún
workflow ni la cola.

## 3. POR QUÉ FALLÓ, y el fallo es de diseño mío
`anatomia.py` construye su grafo buscando `import x` / `from x import` en `codigo/*.py`. **Este
proyecto tiene DOS formas de usar un módulo** —importarlo, y ejecutarlo desde un workflow— **y el
censo solo miraba una.**

Es el mismo error que el censo de los muertos ya había corregido para otra cosa: allí un módulo
sobrevive si un acta lo **cita**, aunque nadie lo importe. Aquí faltaba la tercera vía: que el
proyecto lo **ejecute**.

## 4. POR QUÉ NO SE EDITA `anatomia.py`
**Está sellado** (17-ago-2026, 00:22). Editarlo mataría su sello y dejaría irreproducible el
INFORME-65. La regla de esta casa es la misma de siempre: **el arreglo va en un módulo nuevo con su
prerregistro**, y el defecto se publica aquí.

## 5. QUÉ SE HIZO HOY
1. **Error nº27 en el catálogo**: «contar un módulo como desconectado mirando solo las
   importaciones», con detector **mecanizado** `d_huerfano_que_si_corre`, probado por los tres
   lados.
2. **El guardián bloquea desde hoy**: `disciplina` lee lo que el censo publicó y lo compara con lo
   que los workflows ejecutan. **Ahora mismo está en rojo por este mismo motivo, y así debe estar
   hasta que el censo corregido lo sustituya.**

## 6. LO QUE ESTO **NO** CAMBIA
- **El INFORME-65 no se retira.** Midió lo que dijo medir —conexión por importación— y su dato
  sigue siendo cierto bajo esa definición. Lo que estaba mal era **llamar a eso «desconectado»**.
- **No dice nada sobre si los tres módulos hacen falta.** Ejecutarse no es funcionar: eso lo dice
  su ficha de sanidad, y **ninguno de los tres ha pasado la puerta**.
- **Nada del universo.**
