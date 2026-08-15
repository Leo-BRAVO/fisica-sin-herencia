# INVENTARIO 01 — ¿qué corridas nuestras usan de verdad el motor defectuoso?
**11 de agosto de 2026. Fase 2 del PLAN MAESTRO 01, paso 0 — el inventario mecánico que iba
antes de prometer nada.**
**Este documento CORRIGE una afirmación mía del propio plan. Es su primer resultado.**

---

## 1. LO QUE YO ESCRIBÍ EN EL PLAN, y era falso
El PLAN MAESTRO 01 dice, en su Fase 2: *"rehacer cada una de las 67 corridas con `sindy4` y
comparar veredictos"*, con un paso 0 mecánico *"porque no son las 67; hay que contarlo antes de
prometer nada"*.

**Se contó. Y el número no es "menos de 67": es DOS.**

## 2. EL INVENTARIO, medido sobre el código
Búsqueda de todas las llamadas reales al motor en `codigo/`:

| dónde | qué es | ¿produce resultados publicados? |
|---|---|---|
| `escala.py` | el estudio del prerregistro 46 → INFORME-55 | **sí** — es un estudio *del motor*, no *con* el motor |
| `sueno.py` | **el órgano G9**, la fase de minería del sueño | **sí — es el único órgano que usa el motor** |
| `pruebas.py` | autopruebas de los guardianes | no |
| `arreglo_motor.py`, `diag_p47.py` | el estudio de ayer y su diagnóstico | sí, y ya están hechos con los dos motores |

## 3. Y LAS 67 CORRIDAS DE LA COLA **NO USAN `sindy3` EN ABSOLUTO**
La cola tiene 67 elementos, todos en estado `hecha`: 55 de tipo `gimnasio`, 8 de `re-analisis`,
3 de `re-analisis-herramienta` y 1 de `analisis`. **Ninguno pasa por `sindy3`.** Corren por
`descubrir.py`, que usa **PySR** — un motor distinto, de la Fase 0 del proyecto.

**Los dos defectos medidos en los INFORMES 54 y 55 no tocan esas 67 corridas.** No porque las
hayamos protegido, sino porque nunca pasaron por ahí.

## 4. LA IRONÍA, y no es un adorno: **el motor VIEJO era más disciplinado que el nuevo**
`descubrir.py` declara en su cabecera, escrito hace meses:

> *"División 70/30 POR TIEMPO (sección 3b): jamás al azar. **Regla 12: línea base = velocidad
> constante; éxito = error < 50% del error base en el 30% oculto.** Regla 11: `--nulo barajado` y
> `--nulo ruido` deben FALLAR el umbral."*

**Es decir: el descubridor de la Fase 0 YA TENÍA partición fuera de muestra, línea base tonta con
número y nulos obligatorios.** Y `sindy3` —escrito después, con más matemática y mejor
justificación teórica— **no tenía ninguna de las tres.** La guarda que ayer mató la alucinación
(`INFORME-58`) es exactamente la que el motor viejo llevaba desde el principio.

**La lección, y es incómoda:** al construir `sindy3` mejoramos la *matemática* (forma débil,
bootstrap) y **perdimos la disciplina por el camino**. Un módulo mejor por dentro puede ser peor
como instrumento si se le olvida lo que el anterior ya había aprendido.

## 5. QUÉ QUEDA REALMENTE POR REVISAR — la Fase 2 corregida
| # | qué | por qué |
|---|---|---|
| **1** | **`sueno.py` (G9)** con `sindy4` | Es el único órgano afectado, **y ya está REPROBADO** por culpa de este motor: el INFORME-50 midió que con el mundo ×10 sobrevivían 0 leyes en vez de 3. Es el candidato natural a recuperarse. |
| **2** | **Los `no concluyente` del INFORME-55** | Su barrido se hizo con `sindy3`. Lo que cambia no es el hallazgo —queda confirmado por el criterio D del prerregistro 47— sino cuánta de nuestra ceguera era del umbral. |

**Y nada más.** La Fase 2 pasa de *"rehacer 67 corridas"* a **"rehacer un órgano"**.

## 6. LO QUE ESTO **NO** SIGNIFICA
- **No significa que las 67 corridas estén sanas.** Significa que **no las tocan estos dos
  defectos concretos.** `descubrir.py`/PySR **nunca ha pasado por LA PUERTA ni por la ficha de
  sanidad**, y nadie ha medido si tiene su propia banda de escala. **Es un hueco nuevo, y se
  anota como tal: no se hereda tranquilidad de un examen que no se ha hecho.**
- **No significa que la Fase 2 sea gratis.** Rehacer `sueno.py` exige su propio prerregistro,
  porque puede cambiar el veredicto de un órgano.
- **No cambia ningún resultado ya publicado.**

## 7. LA PREGUNTA QUE ABRE (Regla 18)
> **¿Tiene PySR su propia banda de escala?** Es el motor que produjo **55 de nuestras 67
> corridas** y jamás ha sido examinado como examinamos a `sindy3`. El barrido que destapó los
> agujeros son 25 escalas × 5 semillas × 2 sistemas; **aplicárselo a PySR es exactamente el mismo
> trabajo, sobre el motor que más resultados nuestros ha producido.**

## 8. LO QUE LE TOCA AL DIRECTOR
Nada que firmar. Un aviso de honestidad: **corregí a la baja una promesa que yo mismo había
escrito hace unas horas.** El plan prometía revisar 67 corridas y la revisión real son dos cosas.
**Prefiero que quede escrito que me pasé de ambicioso, a que el número grande siga en pie sin que
nadie lo compruebe.**
