# Prerregistro 28 — SINDy en forma débil + bootstrap: la cura del ruido de sensor — 9 de agosto de 2026
**Estado: FIRMADO por el director el 9-ago-2026 ("implementemos todo absolutamente todo... avanza
uno por uno hasta terminar todo lo solicitado"), sobre la propuesta ordenada por impacto que él
mismo pidió y aprobó en bloque.**

## Por qué (el problema medido, no supuesto)
`sindy2.py` obtiene la derivada restando posiciones consecutivas (`np.gradient`). Esa resta
**amplifica el ruido**: el error relativo de la derivada crece como σ/dt. Diego tiene sensores
encarnados — propiocepción, tacto, latentes visuales — y todo sensor real es ruidoso por
construcción. La literatura de 2024–2026 (Ensemble-SINDy, Weak-SINDy, Multi-Fidelity SINDy)
converge en que la forma débil da órdenes de magnitud más robustez, y que la estabilidad del
soporte bajo remuestreo es el mecanismo anti-ruido correcto — sin necesidad de priors físicos.
Ninguna de esas piezas importa física: son cuadratura e integración por partes.

## Qué se construye (`codigo/sindy3.py`)
1. **Forma débil.** Se elige una función de prueba φ que vale cero en los bordes de su ventana;
   entonces `∫ φ·(dx/dt) = −∫ φ'·x`. El lado derecho **no deriva los datos ni una vez**: solo pesa
   `x` contra una curva conocida. El ruido, integrado contra φ', se promedia a cero.
2. **Bootstrap con probabilidad de inclusión.** Se remuestrean las ventanas con reemplazo 200
   veces; cada término recibe la fracción de remuestreos en que sobrevive. Un término entra a la
   ley solo si supera el **piso de inclusión prerregistrado: 0.9**.
3. **Confirmación final.** El ajuste sobre todas las ventanas debe reproducir exactamente el
   soporte que votó el bootstrap; si no, se calla. Y una ley vacía jamás cuenta como replicada
   (lección congelada de `sindy2`, que se hereda intacta).

## Regla 31 declarada ANTES de correr (cuatro casos)
| Caso | Qué debe pasar |
|---|---|
| Oscilador limpio (`dx=v`, `dv=−0.4x−0.1v`) | recupera la ley rala término a término |
| **Oscilador con sensor ruidoso** | recupera la MISMA ley — el caso que justifica el módulo |
| Barajado | calla |
| Ruido puro | calla (y soporte vacío ≠ replicación) |

**Nulo elegido y por qué** (enmienda de la Regla 31): la afirmación es de **estructura dinámica**
(qué términos gobiernan la derivada), y el barajado destruye exactamente el orden temporal del que
esa afirmación depende. Corresponde barajado + ruido, no IAAFT.

## Resultado (corrido el 9-ago-2026, antes de firmar el módulo al banco)
**Regla 31: APRUEBA 4/4.** Coeficientes recuperados con ruido de sensor: `dx/dt = 0.9942·v`
(verdad 1.0), `dv/dt = −0.3972·x − 0.0944·v` (verdad −0.4, −0.1); probabilidad de inclusión 1.000
en los tres términos.

**La medida honesta de la ganancia** (`--comparar`, misma verdad, mismo ruido, los dos motores):

| Ruido del sensor | Derivada numérica (`sindy2`) | Forma débil (`sindy3`) |
|---|---|---|
| 0.0 | SÍ | SÍ |
| 0.005 | **no** | SÍ |
| 0.01 | no | SÍ |
| 0.02 | no | SÍ |
| 0.05 | no | SÍ |
| 0.1 | no | SÍ |
| 0.2 | no | **no — aquí se rompe** |

**Veinte veces más robusto, y se rompe limpiamente.** El motor viejo muere con 0.5% de ruido; el
nuevo aguanta hasta 10% y por encima de eso calla en vez de inventar (que es lo que se le exige).

## Qué NO se afirma
- `sindy2` **no se retira**: sigue en el banco como segundo motor independiente. Dos motores que
  llegan a la misma ley valen más que uno; y uno que descubre donde el otro calla es una alarma.
- Esto no descubre ninguna ley del mundo por sí solo. Es un instrumento mejor, no un resultado.
- El piso de inclusión 0.9 y las 200 repeticiones quedan **congelados aquí**: cambiarlos después
  de ver un resultado sería exactamente ajustar la vara al examen.

## Firmado
Leo, director — 9-ago-2026, aprobación en conversación ("implementa todo absolutamente todo").
