# Prerregistro 21 — Los ojos que se GANAN su dimensión: selección por ganancia honesta — 8 de agosto de 2026
**Estado: FIRMADO — Leo, director, 8-ago-2026 ("firmado el 21"). Nace del INFORME-27 y del instrumento `ganancia_honesta.py` (aprobado por la Regla 31). Responde a la evidencia triangulada de que los ojos actuales de Diego cargan estructura que no es física.**

## La pregunta
Los laboratorios eligen la dimensión de una representación por **error de reconstrucción** o por
**error de predicción**. Nuestra evidencia dice que la textura satisface ambos: los ojos de Diego
predicen al 72% y su **ganancia honesta es ≈ 0%** — todo su poder era espectro. La pregunta:
**¿existe una dimensión latente cuyo poder predictivo SÍ sea dinámica, y no textura?**

## El criterio nuevo (lo que nadie usa)
La dimensión no se elige: **se gana**. Para cada candidata d, se mide sobre los JUECES CONGELADOS:
```
GANANCIA_HONESTA(d) = reducción(datos reales) − reducción(datos surrogados)
```
Ganan las dimensiones cuyo poder la textura NO puede explicar.

## Diseño
- **Candidatas:** d ∈ {2, 3, 4, 6, 8}. Ojos entrenados DESDE CERO por candidata (misma semilla,
  mismas épocas, misma pérdida conjunta que N-002-E2 — solo cambia d).
- **Jueces:** videos 3, 6, 9 — los mismos de siempre, congelados, invisibles al entrenamiento.
- **Sonda rápida:** la ganancia honesta se calcula con el rival lineal (no gasta el motor
  simbólico). **La ganadora, y solo ella, corre la campaña completa** contra los jueces.
- **Selección interna vs veredicto externo:** la elección de d es del bucle interior (Regla 28);
  el veredicto final lo dan los jueces congelados una sola vez, al final.

## Predicciones comprometidas ANTES de correr (las tres son informativas)
1. **Si alguna d tiene ganancia honesta > 0.10:** existe dinámica capturable; esa d es la
   representación legítima y la campaña completa debe confirmarlo. Nace nodo candidato.
2. **Si TODAS las d dan ganancia honesta < 0.05:** hallazgo mayor y honesto — *ninguna*
   representación autoencoder de este aparato a 30 fps captura dinámica más allá de la textura, y
   la certificación predictiva de N-002-E2 y N-003-E2 queda formalmente **degradada a estructural**
   (que es lo único que esos nodos afirmaban con rigor). Se registra tal cual, sin maquillaje.
3. **Si la d ganadora coincide con la dimensión intrínseca medida (~4 menos las ~2 de basura ≈ 2–3):**
   convergencia entre dos instrumentos independientes — la señal más fuerte posible.

## Regla 31 (ya cumplida por el instrumento)
`ganancia_honesta.py` aprueba: da ≈0 en un mundo de textura pura y +0.28 en uno con acople real.
Casos congelados en el banco.

## Fracaso
Se registra tal cual. Un fracaso aquí no es del método: es el mapa de lo que 30 fps y un
autoencoder pueden y no pueden ver.

- **Nota de ejecución (concurrencia, 8-ago):** se implementa y corre en la RAMA mientras el
  latido vacía la cola de nulos en la nube. Razón: el latido hace `git pull --rebase origin main`
  antes de cada push, así que código nuevo en main entraría en su directorio a mitad de corrida;
  si algo rompiera el banco, su siguiente guardián lo mandaría a cuarentena y los nulos quedarían
  a medias. La rama aísla por completo. Se fusiona cuando los nulos aterricen.
- **Firmado:** Leo, director — 8-ago-2026.
