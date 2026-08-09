# codigo/archivo/ — la era de la laptop y las campañas cerradas
**Limpieza del 8-ago-2026 (orden del director: "borrar las cosas que no sirven"). Nada se borró:
se archivó. Git conserva todo el historial; esta carpeta mantiene el código legible y explicado
para quien audite el proyecto — el `codigo/` de arriba solo contiene lo VIVO.**

## Por qué ya no se usan
| Archivo | Qué era | Por qué está aquí |
|---|---|---|
| `programa_estudios.ps1` | la tarea horaria de Windows que ejecutaba la cola | **reemplazado por `latido-nube.yml`**: el latido vive en la nube y no depende de ninguna laptop (INFORME-23) |
| `vigilante.ps1` | alarma que detectaba cuelgues de Julia y reiniciaba | la nube tiene su propio manejo: checkpoints commiteados + reanudación automática |
| `vigia.ps1` | vigía de UNA campaña concreta (E2-Mendeley) | esa campaña cerró en julio |
| `respaldo.ps1` | copia fría semanal a `C:\FisicaSinHerencia-Respaldo` | atado a la máquina del director; el respaldo real hoy es GitHub + la reconstrucción desde fuentes públicas |
| `bucle14.ps1` · `selector14.py` | el primer bucle interior (prerregistro-14) | campaña histórica cumplida (N-003-E2); su lección vive en el nodo |
| `veredicto_p09.py` · `veredicto_p11.py` | evaluadores de UN prerregistro cada uno | veredictos ya emitidos (INFORMES 08 y 10) |
| `campana_familia.py` · `etapa2_familia.py` · `preparar_zenodo.py` | la campaña Zenodo (familia de 14 péndulos) | **cerrada definitivamente por orden del director** (10-jul-2026): ese dataset no resuelve leyes finas |

## Si la laptop revive
Los `.ps1` siguen siendo válidos para Windows, pero **no los enciendas junto con el latido de la
nube**: habría dos corazones ejecutando la misma cola. Una sola casa para el latido.

## Archivados el 9-ago-2026 por el mapa de la mente (`mente.py`)
El mapa los declaro **huerfanos**: ni cuelgan de un gen, ni los importa nadie, ni los ejecuta la
cola. No estan rotos ni desmentidos — son herramientas de prerregistros ya cerrados que dejaron de
usarse. Se archivan **sin borrarse** (nada se borra en esta casa) para que `codigo/` contenga solo
lo que esta vivo:
- `ojos_ganados.py` — prerregistro-21, los ojos que se ganan su dimension.
- `transferir.py` — prerregistro-05, prueba de transferencia entre trials.
Si algun prerregistro futuro los necesita, vuelven a `codigo/` con su firma.
