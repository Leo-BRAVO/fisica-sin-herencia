# INFORME-43 — ACTA DEL PRERREGISTRO 35 (pasivo): el empate **SOBREVIVE** la réplica real, 5/5
**10 de agosto de 2026.** Corrida oficial completa: 5 semillas, las tres guardianas verdes en cada
una, commiteadas en `main` (`7bf3fcf`, `f1a0815`, `5b8c590`, `47af091`, `bb7d57f`).

El nodo **H-002** se escribió con una salvedad explícita: el empate estaba medido sobre **un solo
régimen de caída**. Esta acta cierra esa salvedad. **El empate no era un artefacto.**

---

## 1. LA TABLA COMPLETA

| s | mundo (mesa / suelta / masa) | Frontera enc. vs pas. | Encarnado | Pasivo-propio | Pasivo-ajeno | Diferencia |
|---|---|---|---|---|---|---|
| 1 | 0.507 / 1.157 / 0.232 | **3 vs 0** | 0.1095 | 0.1068 | 0.1002 | **+0.0027** |
| 2 | 0.446 / 1.284 / 0.274 | **3 vs 0** | 0.1912 | 0.1942 | 0.1631 | **−0.0030** |
| 3 | 0.644 / 1.210 / 0.293 | **3 vs 0** | 0.1290 | 0.1325 | 0.1248 | **−0.0035** |
| 4 | 0.697 / 1.468 / 0.428 | **3 vs 0** | 0.1664 | 0.1759 | 0.1730 | **−0.0095** |
| 5 | 0.526 / 1.545 / 0.277 | **3 vs 0** | 0.1260 | 0.1279 | 0.1419 | **−0.0019** |

- **Control positivo: 5/5.** El encarnado gana la frontera yo/mundo **3 canales a 0** en las cinco.
  La comparación no es ciega: cuando hay una diferencia que encontrar, la encuentra y al máximo.
- **Física de soporte: EMPATE 5/5.** Umbral prerregistrado 0.05. Mayor diferencia a favor del
  cuerpo: **+0.0027 — dieciocho veces menor**. Negativa en **4 de 5**.
- En la semilla 5 el **pasivo-ajeno** —que ni causó lo que ve— vuelve a puntuar **más alto** que el
  encarnado (0.1419 vs 0.1260).

## 2. POR QUÉ ESTA RONDA VALE MÁS QUE LA ANTERIOR

En el INFORME-41 el escalón 2 valía **2.544 en las quince mediciones**, porque la caída era siempre
la misma. Esa constante era el límite declarado del nodo H-002. Aquí el mundo cambia en las cinco
semillas y **el empate no se mueve**: sigue en el mismo orden de magnitud (±0.01) contra un umbral
de 0.05, en cinco escenarios distintos.

**La salvedad del nodo H-002 queda cerrada.** El nodo se actualiza en consecuencia.

## 3. LO QUE ESTO CONFIRMA, DICHO IGUAL QUE LA PRIMERA VEZ

**La física de soporte se aprende MIRANDO. El cuerpo no aporta aquí.** Y ahora está medido sobre
cinco mundos, no sobre uno.

**Lo que el cuerpo sí aporta es la frontera yo/mundo**, y como **hecho lógico, no como mérito**: el
pasivo no saca 0 porque le vaya mal, sino porque la pregunta no existe para él. Sin órdenes propias
no hay contingencia que detectar.

**La encarnación no se justifica como atajo para aprender física.** Se justifica porque **sin ella
no hay un "yo" respecto del cual definir nada**. Es la tesis pequeña, y es la que aguanta — ahora
con réplica real detrás.

## 4. LO QUE NO SE AFIRMA
- **No se afirma que la encarnación sea inútil.** Para **esta capacidad**, en **este mundo**, no
  aportó. Nada más y nada menos.
- **Manipulación, causalidad por contacto activo y experimentación dirigida siguen sin medirse.**
  Es donde el cuerpo debería ganar, y no tenemos derecho a suponerlo.
- **Sigue habiendo un límite, y es distinto del anterior:** el brazo **nunca toca el objeto**.
  Variar la caída no fue dejar que la tocara — eso se excluyó a propósito del prereg-35 porque es
  otra pregunta. Mientras el cuerpo no pueda **intervenir** sobre lo que observa, este experimento
  compara a un encarnado que en la práctica también está mirando. **Ese es el siguiente experimento
  de verdad, no una nota al pie.**
- Sigue siendo PyBullet, no el universo.

## 5. PROPUESTA AL DIRECTOR (Regla 15)
1. **Actualizar H-002**: quitar la salvedad de "un solo régimen de caída" (resuelta) y sustituirla
   por la que sí queda en pie (el brazo no interviene). Necesita su firma.
2. **Prerregistrar la experimentación dirigida** — la capacidad donde el pasivo **no puede
   competir**, porque no puede elegir qué mirar. Es la prueba que decidiría de verdad la discusión
   sobre el cuerpo. **Si el cuerpo tampoco aportara ahí, sería una noticia mucho mayor que ésta.**

## 6. TRAZA
- Prerregistro: `registros/prerregistro-35.md` (firmado 10-ago-2026).
- Código: `codigo/observador_pasivo.py`, 5/5 casos de Regla 31 — incluido el que exige que el mundo
  variable **no rompa** la comparación (las tres condiciones comparten decorado y el control
  positivo sigue ganando). La cura podía destruir justo lo que este módulo mide; se comprobó en el
  dato, no en la intención.
- Datos crudos: `resultados/p35-pasivo-variable-s{1..5}/resumen.json`.
