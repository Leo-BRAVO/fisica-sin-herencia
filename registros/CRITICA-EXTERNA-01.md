# CRÍTICA EXTERNA 01 — revisión punto por punto, y qué entra en la lista
**11 de agosto de 2026. El director trae un diagnóstico técnico externo y pide incorporarlo.**
**Antes de meter nada en la lista lo comprobé contra el código de hoy: meter en la lista algo ya
resuelto la envenena, y descartar algo cierto por orgullo la vacía.**

---

## VEREDICTO GENERAL
**La crítica es buena, y tres de sus puntos son mejores que nada que yo hubiera escrito.** Su punto
A —el autoencoder que optimiza el fondo— es la respuesta más probable a la pregunta que más le
importa al director: *por qué no descubre leyes con los videos*. **Lo adopto entero.**

De sus 4 puntos de deuda y 4 cuellos de botella: **5 ciertos y nuevos, 2 ciertos ya contados,
1 ya resuelto hoy, y 2 correcciones factuales.**

---

## 1. LO QUE ES CIERTO Y NUEVO — entra en la lista

### 1.1 · El autoencoder confunde el fondo con la física — **EL PUNTO MÁS VALIOSO**
**Comprobado en el código.** `ojos_gimnasio.py`, línea 54:
```python
rec = ((modelo.decodificar(zb) - xb) ** 2).mean()
```
Es **error cuadrático por píxel, promediado**. Y la crítica tiene razón en la consecuencia: si más
del 90% de los píxeles son fondo, **el óptimo de esa pérdida es reconstruir la pared**, no el brazo
delgado. Los latentes no son coordenadas: son mezclas de textura.

**Y encaja con lo que ya habíamos medido y no habíamos sabido explicar:**
- las **cuatro arquitecturas de ojo puntuaron a escala de ruido** en el torneo;
- **`percepcion2` diverge** en 3 de 4 entrenamientos (INFORME-63);
- el motor recibe series de las que **no puede sacar nada**, y calla o alucina.

**Tres hallazgos sueltos que ahora tienen una sola causa candidata.** → **NUEVO ITEM 25.**

### 1.2 · Keypoints espaciales / flujo óptico en vez de reconstrucción
La cura propuesta —**spatial softmax**, que fuerza al latente a ser un punto (x, y) de atención, y
**diferencia temporal de fotogramas** para que la red vea movimiento y no textura— es correcta,
está publicada y es directamente aplicable. → **NUEVO ITEM 26.**

### 1.3 · Regularización física del latente (Hamiltoniano / Lagrangiano)
Forzar que el latente tenga estructura de posición-momento. **Con una salvedad de la Regla 27 que
la crítica no menciona y es seria:** imponer estructura hamiltoniana **es meter física humana en
la arquitectura**. No es prohibitivo —es matemática, no una ley concreta— pero **hay que declararlo
y decidirlo**, no colarlo. → **NUEVO ITEM 27, con su aviso.**

### 1.4 · Los 9 módulos huérfanos de `mente.py`
`brazo_no_mio`, `cadena_g14g8`, `contratos`, `diag_p47`, `invariantes`, `mundo`, `sueno_motor`,
`tacto`, `unico_apto`. **Es un huerfanismo DISTINTO del que midió el INFORME-65**: aquél contaba
órganos del genoma sin consumidor; éste cuenta módulos que no cuelgan de ningún gen. **Los dos son
ciertos y se suman.** → **NUEVO ITEM 28.**

### 1.5 · El banco de experimentación rápida — **la crítica más incómoda y en parte acertada**
Dice que *"la burocracia interna ha comenzado a frenar la velocidad de experimentación"*.

**Mi respuesta, y quiero que sea honesta en las dos direcciones:**

**Donde NO tiene razón:** los guardianes se han pagado solos, y con hallazgos que una iteración
rápida no habría encontrado nunca — los dos defectos del motor, la cadena G14→G8, los cuatro
órganos desconectados, y **tres falsos positivos de mis propios detectores en un solo día**.
Quitarlos no aceleraría: nos devolvería a publicar resultados falsos más deprisa.

**Donde SÍ tiene razón, y es un fallo de diseño mío:** **no existe un carril rápido.** Hoy,
probar una tasa de aprendizaje distinta obliga a pasar por la puerta como si fuera un estudio. Eso
no protege nada —una prueba de concepto no publica— y **cuesta horas**.

**La salida no es aflojar los guardianes: es declarar dos carriles.** → **NUEVO ITEM 29, y lo
implemento primero porque desbloquea todo lo demás.**

---

## 2. LO QUE ES CIERTO Y YA ESTABA CONTADO

- **Derivadas y mal condicionamiento.** Cierto, **y ya medido con más precisión de la que la
  crítica maneja**: condición 7.06×10⁹ sobre señal casi constante (INFORME-58) y 7.33×10¹⁴ en el
  oscilador sin amortiguar (INFORME-62). Un matiz técnico: **`sindy3`/`sindy4` NO derivan
  numéricamente** — usan la forma débil, que integra en vez de derivar, precisamente por esto. El
  problema que queda es **la calidad del latente**, que es su propio punto A.
- **Tacto muerto / falta de intervención causal.** Cierto y medido: el brazo **no alcanzaba nada**
  (INFORME-57, punta a z=0.380 con objetos a z≈0.20). Ya hay mundo con alcance verificado
  (INFORME-61); **falta la política que busque el contacto.** Ya está en la lista.
- **Deuda de nivel 2.** Cierto y contado por un guardián: **0 de 4 nodos**, con estas palabras:
  *"sin nivel 2 no hay ley, solo correlación"*.

## 3. LO QUE YA ESTÁ RESUELTO — no entra en la lista, y aporto la evidencia
**La cadena incertidumbre → atención.** La crítica describe `piso_poder=0.05` y la epistémica que
escala con el ruido. **Las dos cosas se arreglaron hoy** (prerregistro 49):
- `piso_poder` **ya no existe**; el reparto es `curable · poder` con dos presupuestos.
- La epistémica cruda **ya no la consume nadie**: `atencion.py` **exige** `curable`, una fracción
  en [0,1] donde σ se cancela, y **levanta error** si le pasan otra cosa.
- Medido: el televisor pasó de **7.036 de 10 a 0.25**.

**No lo digo para defenderme: lo digo porque una lista con un problema ya resuelto hace perder
tiempo a quien la lea.**

## 4. DOS CORRECCIONES FACTUALES, dichas sin acritud
- **«Confirmado por el INFORME-45»** — no existe. Los informes van del 1 al 65 y **el 45 es un
  prerregistro**, precisamente el que quedó NULO. El dato del 0.0001 es real y viene de las
  campañas del tacto.
- **«8 módulos reprobaron por no incluir manifiestos»** — exacto, y es **mi propio hallazgo**
  (INFORME-63), donde además escribí que **2 de los 3 hallazgos de código eran falsos positivos
  míos**. Coincido con la lectura; solo señalo que salió de la misma maquinaria que se critica.

## 5. Y UNA COSA EN LA QUE ESTOY DE ACUERDO SIN MATICES
> *"Diego no es una mente biológica ni una IA sintiente. Los términos como genoma, órganos, sueño
> o mente son metáforas."*

**Cierto, y ya está medido y escrito:** **12 de los 15 «órganos» son mente y solo 3 tocan el
cuerpo**, y el problema de la cadena **no era la metáfora, era una interfaz sin contrato**.
Mantengo los nombres porque **fueron los que provocaron la pregunta correcta** —*¿este órgano está
sano?*— que destapó 3 defectos de 6 examinados. **Pero la advertencia es justa: si alguna vez la
metáfora nos hace tratar un `if` como una intuición, el nombre habrá dejado de servir.**

---

## LOS SEIS ITEMS NUEVOS DE LA LISTA
| # | qué | por qué ahí |
|---|---|---|
| **25** | La pérdida por píxel optimiza el fondo | causa candidata de tres hallazgos sueltos |
| **26** | Keypoints espaciales + flujo óptico | la cura publicada del 25 |
| **27** | Regularización física del latente | **con aviso de Regla 27: es meter estructura humana** |
| **28** | 9 módulos fuera del genoma | huerfanismo distinto del INFORME-65, y también real |
| **29** | **Banco de experimentación rápida** | desbloquea todo lo demás — **se hace primero** |
| **30** | Política que busque el contacto | ya había mundo alcanzable; falta querer tocarlo |

## LO QUE **NO** SE AFIRMA
- **No se afirma que la pérdida por píxel sea LA causa** de que los ojos puntúen a ruido. Es la
  hipótesis mejor sostenida, con mecanismo y con tres hallazgos que encajan — **y sigue siendo una
  hipótesis hasta que un estudio prerregistrado la mida contra la alternativa.**
- **No se afirma que los keypoints vayan a funcionar aquí.** Funcionan en la literatura, sobre
  otros problemas.
- **Nada del universo.**
