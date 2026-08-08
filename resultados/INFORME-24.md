# INFORME 24 — La primera campaña en la nube falló, y al buscar el porqué apareció algo peor — 8 de agosto de 2026

## El error que reportó el director
`estudios-nube.yml` → job `campana` → **Failure, exit code 1, a los 4m 26s.**

## Causa raíz (reproducida, no adivinada)
El campo `reconstruir` quedó en `no` (era el valor por defecto que dejó el orquestador), así que
la nube no reconstruyó los datos — y `datos/` está fuera de git **a propósito** (política de
datos). El motor tardó ~4 min en compilar Julia y después murió en un segundo al no encontrar
réplicas. Reproducido en local: mismo mensaje, mismo `exit 1`.
**El culpable fue el diseño del formulario, no la campaña:** en la nube, `reconstruir: no` es un
fracaso garantizado siempre que los datos no vengan en el repo. Era una trampa esperando a que
alguien la pisara, y el director la pisó a los diez minutos.

## Y al auditar el arreglo apareció el hueco GRANDE
`latido-nube.yml` — el corazón que ayer anuncié como "el proyecto ya no depende de ninguna
máquina" — **se fusionó a main con el YAML ROTO.** El nombre de un paso contenía `reanudacion:`
(dos puntos + espacio), lo que hace que YAML lo interprete como un mapa anidado; el archivo entero
queda inválido. GitHub lo habría rechazado en silencio: **el latido nunca habría latido.** El
orquestador lo anunció funcionando sin haberlo parseado jamás. Es el mismo pecado que la Regla 31
castiga en los instrumentos, cometido en la infraestructura.

## Los tres arreglos
1. **`reconstruir` por defecto = `mendeley_epoca2`** (lo que la nube necesita casi siempre) y una
   **guarda que falla en segundos** con mensaje humano si se pide una carpeta inexistente sin
   reconstruir — en vez de gastar 4 minutos compilando Julia para morir después.
2. **YAML de `latido-nube.yml` corregido** (nombre entrecomillado) — el corazón ya puede latir.
3. **`coherencia.py` gana el guardián que faltaba:** ningún workflow entra al repositorio sin
   parsearse, y además se exige que corra los dos guardianes antes de commitear (Regla 32).
   Verificado rompiendo un YAML a propósito: el guardián lo bloqueó.
   Extra: acciones actualizadas (checkout v5 / setup-python v6) — el aviso de Node.js 20
   deprecado que también salía en la corrida.

## La lección (para MENTE, y es incómoda)
**Lo que no se parsea, no existe.** Un archivo de configuración anunciado como "vivo" sin haberse
validado es exactamente lo mismo que una herramienta que nunca corrió su prueba nula: una promesa
sin evidencia. La Regla 31 vale para los instrumentos científicos Y para la infraestructura que
los ejecuta. Desde hoy el guardián lo hace cumplir por nosotros.

## Qué hace el director ahora
Actions → **estudios-nube** → Run workflow. Los valores por defecto ya son los correctos: el
campo `reconstruir` dirá `mendeley_epoca2` — solo presiona el botón verde. (O `latido-nube`, que
ahora sí es un workflow válido y toma el siguiente item de la cola solo.)
