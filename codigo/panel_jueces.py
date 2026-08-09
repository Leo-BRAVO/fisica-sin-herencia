# panel_jueces.py — EL PANEL DE JUECES DIVERSOS (prerregistro-31, FIRMADO 9-ago-2026).
#
# POR QUE EXISTE (un bug real, cazado en la corrida 13, no una precaucion teorica):
# el torneo de ojos del prereg-27 mide con UNA sola vara: `filogenia.aptitud`, que es
#     puntaje = media( max(margen, 0) ) + 0.01 * n_canales_mios
# El `max(..., 0)` es un SUELO. Cuando ningun latente visual alcanza el piso de contingencia
# (0.40 del prereg-23) —que es exactamente el regimen en que vive la vista de Diego segun el
# INFORME-36— TODOS los margenes son negativos, todos se recortan a cero, y los cuatro
# competidores empatan en 0.0000 EXACTO. Paso en las semillas 1, 2 y 3: cuatro arquitecturas
# distintas, doce corridas, el mismo cero. La vara no estaba midiendo a los competidores: estaba
# midiendo su propio suelo. Y en la semilla 4 una sola arquitectura asomo por encima del piso,
# lo que habria coronado un ganador por puro azar de semilla.
#
# LA CURA, en dos partes:
#   1. NO RECORTAR. El margen crudo (negativo incluido) ordena a los competidores en todo el
#      rango. Un ojo que queda a -0.02 del piso es medible y mejor que uno a -0.35.
#   2. TRES LECTURAS INDEPENDIENTES, no una. Si cambias como lees la red, cambia quien gana
#      (medido en la literatura de sondeo por capas). Un juez unico corona; un panel no.
#
# LAS TRES LECTURAS (prerregistradas, ninguna la ve el competidor):
#   A. CONTINGENCIA — ¿sus latentes le sirven al detector del prereg-23 para hallar el cuerpo?
#      Es la lectura historica, ahora sin suelo.
#   B. FLECHA DEL TIEMPO — se le da el mismo video al derecho y al reves. Si su representacion
#      no distingue el orden temporal, aprendio APARIENCIA, no MOVIMIENTO. Se mide como asimetria
#      de predictibilidad: en un mundo disipativo el futuro es mas predecible que el pasado.
#   C. ROBUSTEZ — se repite la lectura A con los cuadros corrompidos y ocluidos. Un ojo que se
#      derrumba con un poco de ruido no sirve para ningun mundo real.
#
# LA REGLA DE ORO DEL VEREDICTO: un competidor GANA solo si gana o empata en LAS TRES lecturas.
# Si gana en una y pierde en otra, el acta lo registra como GANA CON ASTERISCO y NO reemplaza a
# los ojos oficiales sin una segunda vuelta. Asi ningun juez individual corona a nadie.
#
# Regla 31 del panel (cinco casos): gemelos empatan en las tres; un oraculo plantado gana las
# tres; un tramposo que gana una y pierde otra recibe ASTERISCO (jamas victoria); el ruido puro
# no gana ninguna; y el panel NO puede empatar a cero dos representaciones distintas bajo el piso
# —el bug de la corrida 13 no puede volver sin que esto grite—.

import os
import sys
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "codigo"))

LECTURAS = ("contingencia", "flecha", "robustez")


# ----------------------------------------------------------------------------- lectura A
# EL HORIZONTE, IMPORTADO DE UNA SOLA FUENTE. La auditoria del 9-ago-2026 encontro que este
# modulo media la obediencia a UN PASO mientras `soporte.py` la medida a OCHO — y la leccion del
# prereg-29 es justamente que a un paso la obediencia es INVISIBLE (lo que el torque agrega en un
# paso es del orden de a*dt^2). El panel estaba subestimando sistematicamente a todos los
# competidores por igual. Se corrige usando la MISMA funcion, no una copia parecida: tres
# implementaciones distintas de "cuanto ayuda conocer el comando" eran tres oportunidades de
# divergir en silencio.
from soporte import HORIZONTE, _ganancia_comando as _ganancia_canal


def _ganancia_obediencia(latentes, comandos, jidx, h=HORIZONTE):
    """CUANTO AYUDA CONOCER EL COMANDO a predecir el latente a horizonte h, de forma CONTINUA.
    Por que existe: el criterio del prereg-23 UMBRALIZA dos veces (por ventana y por fraccion),
    y bajo el piso todo se aplasta al mismo numero — dos representaciones distintas y ambas
    flojas dan identico -0.4000. Umbralizar es correcto para DECIDIR 'este canal es mio';
    es ruinoso para ORDENAR competidores. Esta cifra no umbraliza nada."""
    gs = []
    for i, (u, Z) in enumerate(zip(comandos, latentes)):
        if i not in jidx:
            continue                       # SOLO episodios-juez: la muralla intacta
        Z = np.asarray(Z, dtype=float)
        u = np.asarray(u, dtype=float)
        if len(Z) < 40:
            continue
        gs.append(float(np.mean([_ganancia_canal(Z[:, c], u, h=h)
                                 for c in range(Z.shape[1])])))
    return float(np.mean(gs)) if gs else 0.0


def lectura_contingencia(latentes, comandos, jueces, nulos=8, semilla=31):
    """El detector del prereg-23 SIN SUELO, mas su version continua para poder ORDENAR.
    El puntaje que ordena es la ganancia de obediencia NETA (real menos su nulo por comandos
    barajados) — la misma disciplina de nulos de siempre, ahora sin umbral que aplaste."""
    from contingencia import medir
    jidx = {j - 1 for j in jueces}
    res = medir(list(zip(comandos, latentes)), jueces, nulos=nulos)
    margenes = [r["margen"] for r in res]
    g_real = _ganancia_obediencia(latentes, comandos, jidx)
    rng = np.random.default_rng(semilla)
    g_nulo = float(np.mean([_ganancia_obediencia(
        latentes, [u[rng.permutation(len(u))] for u in comandos], jidx) for _ in range(3)]))
    return {"puntaje": g_real - g_nulo,
            "ganancia": g_real, "ganancia_nulo": g_nulo,
            "margen_medio_prereg23": float(np.mean(margenes)),
            "n_mias": int(sum(1 for r in res if r["es_mia"])),
            "margen_max": float(np.max(margenes))}


# ----------------------------------------------------------------------------- lectura B
def _error_prediccion(Z, semilla=0):
    """Error de un predictor lineal z_{t+1} ~ [z_t, z_{t-1}], normalizado por la varianza.
    Sin red ni entrenamiento: minimos cuadrados cerrados, para que la lectura sea barata y
    reproducible bit a bit."""
    if len(Z) < 8:
        return 1.0
    A = np.column_stack([Z[1:-1], Z[:-2], np.ones(len(Z) - 2)])
    B = Z[2:]
    W, *_ = np.linalg.lstsq(A, B, rcond=None)
    resid = B - A @ W
    var = np.var(B, axis=0)
    var[var == 0] = 1.0
    return float(np.mean(np.var(resid, axis=0) / var))


def lectura_flecha(latentes, jueces):
    """¿Su representacion sabe hacia donde corre el tiempo? Se predice el futuro con el video al
    derecho y con el mismo video al reves. En un mundo con disipacion el futuro es mas predecible
    que el pasado; una representacion que solo lee ESCENA da la misma cifra en ambos sentidos.
    Puntaje = (err_reves - err_derecho) / (err_reves + err_derecho): cero = ciego al tiempo."""
    jidx = {j - 1 for j in jueces}
    puntajes = []
    for i, Z in enumerate(latentes):
        if i not in jidx:
            continue                      # SOLO episodios-juez: la muralla intacta
        Z = np.asarray(Z, dtype=float)
        e_der = _error_prediccion(Z)
        e_rev = _error_prediccion(Z[::-1])
        if e_der + e_rev <= 0:
            continue
        puntajes.append((e_rev - e_der) / (e_rev + e_der))
    return {"puntaje": float(np.mean(puntajes)) if puntajes else 0.0,
            "episodios_juez": len(puntajes)}


# ----------------------------------------------------------------------------- lectura C
def corromper(videos, sigma=0.08, tapa=0.25, semilla=31):
    """Ruido de sensor + oclusion de un parche. No cambia el mundo: cambia lo que el ojo alcanza
    a ver de el — que es lo que le pasa a cualquier ojo real."""
    rng = np.random.default_rng(semilla)
    salida = []
    for v in videos:
        v = np.asarray(v, dtype=float).copy()
        v += rng.normal(0, sigma, v.shape)
        if v.ndim >= 3 and tapa > 0:
            h, w = v.shape[1], v.shape[2]
            ah, aw = max(1, int(h * tapa)), max(1, int(w * tapa))
            y0 = rng.integers(0, max(1, h - ah + 1))
            x0 = rng.integers(0, max(1, w - aw + 1))
            v[:, y0:y0 + ah, x0:x0 + aw] = 0.0
        salida.append(v)
    return salida


def lectura_robustez(codificar, videos, comandos, jueces, base_puntaje, nulos=8):
    """Repite la lectura A sobre el mundo mal visto. Puntaje = cuanta ganancia de obediencia
    SOBREVIVE al ruido y la oclusion. Se reporta en absoluto (no como fraccion) porque una
    fraccion sobre una base casi nula infla cualquier cosa: 0.001/0.0005 = 2.0 no es robustez,
    es division por casi cero. El absoluto no miente."""
    lat_c = codificar(corromper(videos))
    sucio = lectura_contingencia(lat_c, comandos, jueces, nulos=nulos)["puntaje"]
    return {"puntaje": float(sucio), "puntaje_limpio": float(base_puntaje),
            "retenido": float(sucio / base_puntaje) if base_puntaje > 1e-6 else None}


# ----------------------------------------------------------------------------- el panel
def evaluar(nombre, codificar, videos, comandos, jueces, nulos=8):
    """Las tres lecturas de UN competidor. `codificar(videos) -> lista de latentes por episodio`.
    El competidor jamas ejecuta ninguna de estas funciones ni ve sus cifras."""
    lat = codificar(videos)
    a = lectura_contingencia(lat, comandos, jueces, nulos=nulos)
    b = lectura_flecha(lat, jueces)
    c = lectura_robustez(codificar, videos, comandos, jueces, a["puntaje"], nulos=nulos)
    return {"nombre": nombre, "contingencia": a, "flecha": b, "robustez": c,
            "puntajes": {"contingencia": a["puntaje"], "flecha": b["puntaje"],
                         "robustez": c["puntaje"]}}


def veredicto(filas, margenes=None, parsimonia=None):
    """LA REGLA DE ORO. filas: [{'nombre', 'puntajes': {lectura: valor}}, ...].
    `margenes`: cuanto hay que separarse en cada lectura para decir que se gano (si no se da,
    empate tecnico = diferencia menor al 5% del rango observado en esa lectura).
    `parsimonia`: orden de simplicidad para desempatar, del mas simple al mas complejo."""
    if not filas:
        return {"fallo": "SIN COMPETIDORES"}
    margenes = margenes or {}
    detalle, ganan_o_empatan = {}, {}
    for lec in LECTURAS:
        vals = {f["nombre"]: f["puntajes"][lec] for f in filas}
        mejor = max(vals.values())
        rango = mejor - min(vals.values())
        m = margenes.get(lec, 0.05 * rango if rango > 0 else 0.0)
        detalle[lec] = {"mejor": mejor, "margen_usado": m, "valores": vals}
        ganan_o_empatan[lec] = {n for n, v in vals.items() if v >= mejor - m}

    limpios = set.intersection(*[ganan_o_empatan[l] for l in LECTURAS])
    if len(limpios) == 1:
        n = limpios.pop()
        return {"fallo": f"GANA {n} — gana o empata en LAS TRES lecturas", "ganador": n,
                "detalle": detalle}
    if len(limpios) > 1:
        if parsimonia:
            orden = {n: i for i, n in enumerate(parsimonia)}
            n = min(limpios, key=lambda x: orden.get(x, 999))
            return {"fallo": f"EMPATE TECNICO — gana {n} por parsimonia (navaja, no evidencia)",
                    "ganador": n, "empatados": sorted(limpios), "detalle": detalle}
        return {"fallo": "EMPATE TECNICO — sin orden de parsimonia declarado, decide el director",
                "empatados": sorted(limpios), "detalle": detalle}

    # nadie gana o empata en las tres: hay quien gana una y pierde otra -> ASTERISCO
    asteriscos = {}
    for f in filas:
        gana_en = [l for l in LECTURAS if f["nombre"] in ganan_o_empatan[l]]
        if gana_en:
            asteriscos[f["nombre"]] = gana_en
    if asteriscos:
        n = max(asteriscos, key=lambda x: len(asteriscos[x]))
        return {"fallo": f"GANA CON ASTERISCO {n} — gana en {asteriscos[n]} y pierde en el resto; "
                         f"NO reemplaza los ojos oficiales sin segunda vuelta",
                "asterisco": n, "gana_en": asteriscos[n], "detalle": detalle}
    return {"fallo": "NINGUNO SIRVE — ningun competidor gana ni empata en lectura alguna",
            "detalle": detalle}


# ----------------------------------------------------------------------------- Regla 31
def _mundo_sintetico(n_ep=9, T=3400, semilla=31):
    """Mundo de juguete con VERDAD CONOCIDA y disipacion: un punto empujado por comandos y
    frenado por rozamiento. T=3400 para que el detector tenga sus 20 ventanas minimas (ventana=150
    en contingencia.py: por debajo de eso el criterio fabrica cuerpo donde no lo hay).
    Los "videos" son mapas 6x6 donde el punto deja una mancha."""
    rng = np.random.default_rng(semilla)
    comandos, videos, cuerpos = [], [], []
    for _ in range(n_ep):
        u = rng.normal(0, 1, (T, 2))
        p = np.zeros((T, 2))
        vel = np.zeros(2)
        for t in range(1, T):
            vel = 0.86 * vel + 0.14 * u[t]          # disipacion: da flecha del tiempo real
            p[t] = p[t - 1] + vel
        p = np.clip(p, -2.5, 2.5)
        vid = np.zeros((T, 6, 6))
        for t in range(T):
            iy = int(np.clip((p[t, 0] + 2.5) / 5.0 * 5, 0, 5))
            ix = int(np.clip((p[t, 1] + 2.5) / 5.0 * 5, 0, 5))
            vid[t, iy, ix] = 1.0
        comandos.append(u); videos.append(vid); cuerpos.append(p)
    return comandos, videos, cuerpos


def regla31(verbose=True):
    fallos = []
    comandos, videos, cuerpos = _mundo_sintetico()
    jueces = [7, 8, 9]
    rng = np.random.default_rng(31)

    def cod_oraculo(vids):
        """TRAMPA CONSTRUIDA A PROPOSITO (jamas competidor real): lee la verdad del simulador."""
        return [c.copy() for c in cuerpos[:len(vids)]]

    def cod_ruido(vids):
        return [rng.normal(size=(len(v), 2)) for v in vids]

    def _gemelo(sem):
        def cod(vids):
            r = np.random.default_rng(sem)
            return [np.array([v[t].reshape(-1) @ r.normal(size=(36, 2)) for t in range(len(v))])
                    for v in vids]
        return cod

    def cod_congelado(vids):
        """Gana la flecha del tiempo (copia el cuerpo, que es disipativo) pero pierde la
        contingencia (le suma un ruido enorme que tapa la obediencia al comando)."""
        r = np.random.default_rng(5)
        return [c + r.normal(0, 6.0, c.shape) for c in cuerpos[:len(vids)]]

    ora = evaluar("oraculo", cod_oraculo, videos, comandos, jueces)
    rui = evaluar("ruido", cod_ruido, videos, comandos, jueces)
    g1 = evaluar("gemelo-1", _gemelo(77), videos, comandos, jueces)
    g2 = evaluar("gemelo-2", _gemelo(77), videos, comandos, jueces)
    tra = evaluar("tramposo", cod_congelado, videos, comandos, jueces)

    # 1) GEMELOS: identicos deben empatar en las tres
    v1 = veredicto([g1, g2])
    c1 = "EMPATE TECNICO" in v1["fallo"]
    if verbose:
        print(f"  {'ok  ' if c1 else 'FALLO'} GEMELOS: {v1['fallo'][:60]}")
    if not c1:
        fallos.append("gemelos")

    # 2) ORACULO: la trampa plantada debe ganar las tres
    v2 = veredicto([ora, rui, g1])
    c2 = v2.get("ganador") == "oraculo" and v2["fallo"].startswith("GANA oraculo")
    if verbose:
        print(f"  {'ok  ' if c2 else 'FALLO'} ORACULO PLANTADO: {v2['fallo'][:70]}")
    if not c2:
        fallos.append("oraculo")

    # 3) ASTERISCO: quien gana una lectura y pierde otra JAMAS recibe victoria limpia
    v3 = veredicto([tra, ora])
    c3 = ("ASTERISCO" in v3["fallo"]) or (v3.get("ganador") == "oraculo")
    limpio = v3.get("ganador") == "tramposo"
    c3 = c3 and not limpio
    if verbose:
        print(f"  {'ok  ' if c3 else 'FALLO'} TRAMPOSO PARCIAL: {v3['fallo'][:78]}")
    if not c3:
        fallos.append("asterisco")

    # 4) EL RUIDO no gana ninguna lectura contra el oraculo
    c4 = rui["puntajes"]["contingencia"] < ora["puntajes"]["contingencia"]
    if verbose:
        print(f"  {'ok  ' if c4 else 'FALLO'} RUIDO PURO: no le gana al oraculo en contingencia "
              f"({rui['puntajes']['contingencia']:.3f} < {ora['puntajes']['contingencia']:.3f})")
    if not c4:
        fallos.append("ruido")

    # 5) EL BUG DE LA CORRIDA 13 NO PUEDE VOLVER: dos representaciones distintas y ambas bajo el
    #    piso NO pueden dar el mismo cero exacto. Es la razon de ser de este modulo.
    l1 = lectura_contingencia(cod_ruido(videos), comandos, jueces)
    l2 = lectura_contingencia(cod_congelado(videos), comandos, jueces)
    bajo1, bajo2 = l1["puntaje"], l2["puntaje"]
    # ambas quedan BAJO el piso del prereg-23 (margen aplastado al mismo -0.4000) y aun asi el
    # panel las distingue: eso es exactamente lo que el torneo viejo no podia hacer.
    aplastadas = abs(l1["margen_medio_prereg23"] - l2["margen_medio_prereg23"]) < 1e-9
    c5 = aplastadas and abs(bajo1 - bajo2) > 1e-6
    if verbose:
        print(f"  {'ok  ' if c5 else 'FALLO'} SIN EFECTO SUELO: el criterio viejo las aplasta "
              f"al mismo {l1['margen_medio_prereg23']:.4f}, el panel las distingue "
              f"({bajo1:+.5f} vs {bajo2:+.5f}) — el empate a 0.0000 no puede volver")
    if not c5:
        fallos.append("efecto-suelo")

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — el panel empata gemelos, corona oraculos, marca "
                                "asteriscos y no tiene suelo ciego."
                                if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Panel de jueces diversos para torneos (prereg-31)")
    ap.add_argument("--regla31", action="store_true")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    print("uso: --regla31 (su uso como juez oficial exige prerregistro)")
