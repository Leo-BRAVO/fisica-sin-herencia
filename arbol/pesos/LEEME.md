# arbol/pesos/ — los ojos canonicos de los nodos validados
**Enmienda a la politica de datos (8-ago-2026, aprobada por el director): los pesos de redes
que sustentan un NODO APROBADO son evidencia del archivo — sin ellos, la cadena
pixeles -> variables -> ley no es replicable (Regla 14). Solo pesos canonicos; los
checkpoints exploratorios siguen fuera de git.**

## Contenido (SUBIDO Y VERIFICADO — 8-ago-2026)

| Archivo | Latente | Sustenta | sha256 (16) | Verificacion |
|---|---|---|---|---|
| `ojos_p13_lat8.pt` | 8 | [[N-002-E2]] — la percepcion propia original | `57a7ec5e80c94358` | HUELLA VERIFICADA |
| `ojos_p14_lat4.pt` | 4 | [[N-003-E2]] — los ojos que Diego se eligio solo | `648796adf498e357` | HUELLA VERIFICADA |

## Como se verificaron (la prueba que importa, reproducible)
No basta con que carguen: se comprobo que **la cadena entera reproduce la historia**. Con los
videos del dp Morpheus bajados de su fuente publica, se regeneraron los latentes con estos
pesos, se estandarizaron con las estadisticas de entrenamiento (jueces 3,6,9) y se evaluaron
**las ecuaciones descubiertas en julio** sobre ellos:

| Ojos | mse de las ecuaciones historicas sobre los latentes regenerados | mse historico registrado | desviacion |
|---|---|---|---|
| `ojos_p14_lat4.pt` | 0.166322632 | 0.166326505 | 2.3×10⁻⁵ |
| `ojos_p13_lat8.pt` | 0.290719589 | 0.290720783 | 4.1×10⁻⁶ |

**Lectura:** unos pesos distintos darian numeros completamente distintos (el latente es otro
espacio); coincidir a la 5ª cifra prueba que son EXACTAMENTE estos ojos. El residuo de ~10⁻⁵
es decodificacion de video (otra version de OpenCV/ffmpeg descomprime el mp4 con diferencias
de subpixel), no otros pesos — afecta a los dos por igual y en la misma direccion.

**Tolerancia declarada para futuras verificaciones de esta cadena: desviacion < 10⁻³.**
(La cadena pixeles->latentes NO es bit-identica entre maquinas por el decodificador; la cadena
de datos tabulares SI lo es — Mendeley dio 3×10⁻¹⁵ y la caida 0.0 exacto, INFORME-22.)

## Que habilitan
El item `aud01-nulo-p14-final` de la cola deja de esperar al director: con `ojos_p14_lat4.pt`
en el repo, la nube puede regenerar los latentes con los ojos exactos, verificar la huella
(< 10⁻³) y correr el verdugo surrogado pendiente de esa campana insignia.
