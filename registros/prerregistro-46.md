# Prerregistro 46 — LA BANDA DE ESCALA DEL MOTOR, segunda versión — 10 de agosto de 2026
**El prerregistro-45 quedó NULO por su propio señuelo (INFORME-54). Éste lo rehace corrigiendo el
error de diseño que lo mató.**
**Peldaño (Regla 9): Fase 1.** Propiedad de nuestro código, no del universo.

---

## 0. POR QUÉ HAY UN SEGUNDO PRERREGISTRO, y qué se corrige
El 45 metió en la Regla 31 de su instrumento una prueba sobre el **objeto de estudio**: *"el motor
no puede dar ley sobre un sistema sin dinámica"*. **El motor la dio** —20 de 25 casos, con confianza
1.0 (INFORME-54)— y por el criterio congelado el estudio quedó **NULO**. Se cumplió sin discutirlo.

**El error no fue el señuelo: fue dónde lo puse.** La Regla 31 de un instrumento debe examinar
**mi procedimiento de medida**; el comportamiento del sujeto es **resultado**, no requisito de
entrada. Con el señuelo ahí, un defecto del motor bloquea el módulo que existe para medir defectos
del motor.

## 1. LO QUE YA VI, declarado antes de correr
**Al arreglar el módulo corrí el barrido en 7 puntos y vi esto:**

| escala | ve en |
|---|---|
| 10⁻³ | 5/5 |
| 10⁻² | 3/5 |
| **10⁻¹** | **0/5** |
| 10⁰ | 5/5 |
| 10¹ | 5/5 |
| **10²** | **1/5** |
| 10³ | 4/5 |

**No es una banda: ve, deja de ver, vuelve a ver.** Y con la relación señal/ruido **constante** en
todas las escalas, así que no es un efecto del ruido.

**Esas observaciones NO son evidencia de este estudio** — salieron de un módulo que estaba
arreglándose, sobre las semillas `2,3,5,7,11`. **Esas cinco semillas quedan quemadas.** El estudio
corre sobre **cinco nuevas**: `23, 29, 31, 37, 41`, declaradas aquí antes de tocarlas.

**Y declaro mi expectativa, para que se me pueda descontar:** espero **ERRÁTICO**. Si sale una banda
limpia, mi lectura de arriba era ruido de siete puntos y lo diré con esas palabras.

## 2. LA PREGUNTA
> ¿El motor ve dentro de **un intervalo contiguo** de escalas (banda), en **tramos separados**
> (errático), o **en todas** (y entonces el INFORME-50 se cae)?

**La diferencia importa:** una banda se rodea normalizando antes de ajustar. **Un patrón errático no
se rodea**: significa que el veredicto del motor depende de las unidades de forma impredecible.

## 3. LA LÍNEA BASE TONTA (Regla 11)
El ideal: **"el motor ve la ley siempre que exista, sin importar las unidades"** — 25 de 25 escalas.
Se reporta la **fracción de escalas en que ve** sobre el barrido declarado, y **cuántos tramos
contiguos** hacen falta para describirla. Un solo tramo = banda. Más de uno = errático.

## 4. EL DISEÑO, congelado
- **25 escalas:** 10^k, k de −3 a +3 en pasos de 0.25.
- **Dos sistemas:** oscilador amortiguado y caída con roce. Dos formas de ley distintas, para no
  confundir una propiedad del motor con una del oscilador.
- **Cinco semillas nuevas:** 23, 29, 31, 37, 41.
- **Ruido RELATIVO a la escala**, para que la relación señal/ruido sea idéntica en los 25 puntos.
  Sin esto, el estudio mediría el ruido creyendo medir la escala.
- **Ve en una escala** = declara ley en ≥4 de 5 semillas. **No ve** = ≤1 de 5.

## 5. LOS CRITERIOS
1. **BANDA** si en **los dos sistemas** hay **exactamente un** tramo contiguo, y fuera de él no ve.
2. **ERRÁTICO** si en **algún** sistema hay **más de un** tramo contiguo.
3. **CONTRADICE AL INFORME-50** si ve en las 25 escalas de los dos sistemas. **Sería mi error**, y
   se escribiría así.
4. **NO CONCLUYENTE** si no encaja en ninguno — por ejemplo, si hay zonas intermedias (2 o 3 de 5)
   que no permiten llamar ni "ve" ni "no ve".
5. **Banda ESTRECHA** (agravante) si abarca menos de 3 décadas.

## 6. REGLA 31 — sobre MI PROCEDIMIENTO, no sobre el motor
Ésta es la corrección de fondo respecto del 45:
- **Control positivo:** a escala ×1 el motor ve en 5 de 5. Si no, el barrido no tiene punto de
  anclaje y se detiene.
- **Control negativo:** sobre **ruido puro** escalado igual, no declara ley en ninguna escala.
- **La medida debe responder al ruido:** con ruido ×200 la cuenta cae. Si no cayera, la medida no
  estaría midiendo si hay ley que hallar.
- **La medida debe DISTINGUIR escalas:** si diera lo mismo en todas, no mediría nada.
- **La relación señal/ruido debe ser idéntica en todas las escalas** (se mide, no se supone).

**El comportamiento del motor sobre señal casi constante NO es criterio de entrada aquí.** Ya está
medido y publicado en el INFORME-54, y es un defecto **distinto** del que este estudio mide.

## 7. CUÁNDO SE ABANDONA (Regla 13, con número)
- Si el control positivo da **<5 de 5** a escala ×1 → **se detiene**, no hay anclaje.
- Si el control negativo declara ley en **≥1** escala → **se detiene**.
- Si sale **NO CONCLUYENTE** → **no hay tercera versión de este estudio**. Se escribe que el motor
  falla de una forma que este barrido no describe, y la pregunta pasa al arreglo directo.

## 8. LO QUE ESTE ESTUDIO **NO** PUEDE AFIRMAR
- Nada del universo.
- **No dice qué resultados nuestros están tocados.** Eso exige medir campaña por campaña.
- **No arregla el motor.** El arreglo va en su propio prerregistro, con su propia Regla 31.

## 9. FIRMA
Avanza por **quórum adversarial**: decisión sobre cómo medir, criterios congelados, semillas nuevas
declaradas, expectativa mía declarada y un veredicto posible que me deja mal. Revocable con una
palabra del director.
