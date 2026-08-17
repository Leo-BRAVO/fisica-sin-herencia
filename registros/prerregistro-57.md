# Prerregistro 57 — EL BRAZO DELGADO: ¿es AHÍ donde la pérdida por píxel ciega a Diego? — 11 de agosto de 2026
**Continuación directa del INFORME-66. Peldaño (Regla 9): Fase 1.**
**Estado: FIRMADO antes de escribir `ojos_brazo.py`.**

---

## 0. LA PREGUNTA QUE ABRIÓ EL ACTA ANTERIOR, sin cambiarle una palabra
> *"¿Cambia todo esto con un brazo articulado en vez de un disco? La escena de juguete tiene un
> objeto compacto y brillante — el caso **fácil** para cualquier codificador. La crítica externa
> señalaba las **articulaciones delgadas**, y esta escena no las tiene."*

**El prerregistro 56 midió el caso fácil y el margen que declaré no se cumplió por 0.044 en una
semilla de cinco.** Éste mide **el caso difícil**, que es además **el que Diego tiene de verdad**:
su gimnasio es un brazo articulado, no un disco.

## 1. LA PREGUNTA
> Con un objeto **delgado y articulado** —el caso que la crítica señalaba— ¿crece la ventaja del
> cuello de botella espacial sobre la pérdida por píxel, **o no crece**?

## 2. LO QUE YA SÉ, declarado antes de correr
Del INFORME-66, sobre un **disco compacto**: softmax espacial **0.8745 a 0.9594**; píxel **0.6287
a 0.7848**; ventajas **0.1062 a 0.2693**. **Ésos son datos de otro estudio y de otra escena.**

**Mi expectativa, declarada para que se me pueda descontar:** espero que **la ventaja CREZCA**,
porque un brazo delgado ocupa aún menos píxeles y la pérdida por píxel debería ignorarlo más.
**Si no crece, diré que la hipótesis de la pérdida por píxel no explica la ceguera de Diego** — y
entonces hay que buscar la causa en otro sitio, y lo escribiré con esas palabras.

## 3. LA LÍNEA BASE TONTA (Reglas 11 y 12)
La misma y por la misma razón: **el codificador que Diego usa hoy**. No es un rival de paja.

## 4. EL DISEÑO, congelado
- **Escena:** brazo de **dos segmentos delgados** (grosor de 1 píxel) sobre fondo con textura, con
  los dos ángulos moviéndose a frecuencias distintas. **El brazo ocupa menos del 4% de los
  píxeles**, y se comprueba antes de medir.
- **La verdad:** la **posición del extremo** (x, y). Se usa **SOLO PARA EVALUAR**, jamás para
  entrenar — las dos arquitecturas se entrenan con la **misma pérdida por píxel**.
- **Cinco semillas nuevas: `251, 257, 263, 269, 271`.** Quemadas: 211, 223 (banco) y 227, 229,
  233, 239, 241 (prerregistro 56).
- **Todo lo demás idéntico al prerregistro 56**: misma medida, mismas épocas, mismo R² lineal
  fuera de muestra. **Lo único que cambia es la escena** — si cambiara algo más, la comparación
  entre los dos estudios no valdría.

## 5. LOS CRITERIOS CONGELADOS

| | criterio | pide |
|---|---|---|
| **A** | **el brazo es delgado de verdad** | ocupa **< 4%** de los píxeles. Si no, no es el caso difícil y **se detiene** |
| **B** | **la ventaja CRECE** | ventaja media **> 0.2693** — el **máximo** que dio el disco. Comparar contra la media sería regalarme el resultado |
| **C** | **la medida no se infla sola** | contra objetivo aleatorio, **R² ≤ 0.10** |
| **D** | **la medida responde** | con ruido de sensor al doble del contraste, el R² **baja** |
| **E** | **ninguno diverge** | las dos pérdidas finales son finitas |

**El criterio B es duro a propósito.** Exijo superar **el mejor caso** del disco, no su promedio.
Si la ventaja solo iguala, **no habré demostrado que el brazo delgado sea el caso crítico.**

## 6. REGLA 31 — sobre MI PROCEDIMIENTO, los dos lados
- **Control positivo:** un latente que **es** la posición del extremo da R² alto.
- **Señuelo:** ruido puro contra la posición da R² ≈ 0.
- **La escena se comprueba**: el brazo tiene que ser delgado (criterio A) y **moverse** — un brazo
  quieto no tiene posición que recuperar.
- **Base distinta de cero.** Décima vez este mes.
- **`SUJETO` declarado**, y la Regla 31 **no entrena ninguna arquitectura**: trabaja con latentes
  sintéticos. Es el error que dejó NULO al prerregistro 45.

## 7. CUÁNDO SE ABANDONA (Regla 13, con número)
- Si falla **A**, **se detiene**: sin brazo delgado no se está midiendo el caso difícil.
- Si falla **C**, **se detiene**: si el R² se infla, ninguna comparación vale.
- Si falla **B**, el veredicto es **NO ES LA CAUSA** y **no hay segunda versión de este estudio**:
  se busca la ceguera de Diego en otro sitio.

## 8. LO QUE **NO** SE AFIRMA
- **Nada del universo.**
- **NO se cambia el ojo de Diego con este resultado.** Un brazo dibujado en numpy **no es** el
  gimnasio con PyBullet: aprobar aquí autoriza el estudio sobre la escena real, nada más.
- **NO se afirma que el softmax espacial sea la mejor arquitectura posible.** Es una de dos.

## 9. FIRMA
Avanza por **quórum adversarial**: el criterio **B** me exige superar el **mejor** caso del estudio
anterior y no su media, el **A** manda detener si mi propia escena no es el caso difícil, y el
veredicto **NO ES LA CAUSA** me deja sin explicación para la pregunta que más le importa al
director. Revocable con una palabra.
