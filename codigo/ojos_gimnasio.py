# ojos_gimnasio.py — EL HITO 0 DE VERDAD: Diego mira su propio mundo y descubre dónde termina él.
#
# Hasta aquí, el detector de contingencia leía el ESTADO del simulador — ángulos y alturas que
# nosotros elegimos. Eso no es el hito 0: es hacer trampa con nuestras variables. El prerregistro-19
# exige que Diego mire CUADROS DE CÁMARA, se construya sus ojos DESDE CERO sobre este mundo, y que
# la frontera yo/mundo emerja sobre SUS PROPIAS variables latentes, que nadie diseñó.
#
#   1. balbucea y graba          -> comandos + video (lo único que él ve)
#   2. ojos desde cero           -> percepcion.Ojos, entrenados SOLO con episodios de entrenamiento
#   3. contingencia (G4)         -> qué latentes suyos obedecen a sus comandos = SU CUERPO
#   4. nivel B: el primer no-yo  -> la dirección que NINGÚN comando modula y que siempre empuja
#
# Los jueces (episodios apartados + la verdad cuerpo/mundo del simulador) NUNCA entran al
# entrenamiento ni a la selección: solo dicen, al final, si acertó.
#
# Uso: python ojos_gimnasio.py [--episodios 12] [--pasos 500] [--latente 8] [--epocas 8]
#      python ojos_gimnasio.py --control-nivel-b     (el mismo experimento SIN gravedad)

import os
import sys
import json
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "codigo"))

from gimnasio import correr
from contingencia import medir, _desplazar


def entrenar_ojos(videos, jidx, latente=8, epocas=8, semilla=1, lote=64):
    """Ojos DESDE CERO (percepcion.py, el mismo protocolo de N-002-E2). Nada preentrenado, y los
    episodios-juez no participan ni de una época."""
    import torch
    from percepcion import Ojos
    torch.manual_seed(semilla)
    rng = np.random.default_rng(semilla)

    tren = [torch.tensor(v) for i, v in enumerate(videos) if i not in jidx]
    tripletas = [(i, t) for i, v in enumerate(tren) for t in range(1, len(v) - 1)]
    modelo = Ojos(latente)
    opt = torch.optim.Adam(modelo.parameters(), lr=1e-3)
    for ep in range(epocas):
        perm = rng.permutation(len(tripletas))
        tot = n = 0
        for a in range(0, len(perm), lote):
            idx = perm[a:a + lote]
            xa = torch.stack([tren[tripletas[i][0]][tripletas[i][1] - 1] for i in idx])
            xb = torch.stack([tren[tripletas[i][0]][tripletas[i][1]] for i in idx])
            xc = torch.stack([tren[tripletas[i][0]][tripletas[i][1] + 1] for i in idx])
            za, zb, zc = modelo.codificar(xa), modelo.codificar(xb), modelo.codificar(xc)
            rec = ((modelo.decodificar(zb) - xb) ** 2).mean()
            din = ((modelo.dinamica(torch.cat([zb, za], dim=1)) - zc) ** 2).mean()
            p = rec + din
            opt.zero_grad(); p.backward(); opt.step()
            tot += float(p) * len(idx); n += len(idx)
        print(f"   época {ep + 1}/{epocas} pérdida {tot / n:.5f}", flush=True)
    return modelo


def codificar(modelo, videos, jidx):
    """Latentes estandarizados con estadísticas SOLO de entrenamiento (como siempre en la casa)."""
    import torch
    with torch.no_grad():
        zs = [modelo.codificar(torch.tensor(v)).numpy() for v in videos]
    tren = np.vstack([z for i, z in enumerate(zs) if i not in jidx])
    mu, sd = tren.mean(0), tren.std(0)
    sd[sd == 0] = 1.0
    return [(z - mu) / sd for z in zs]


# ============================ NIVEL B — EL PRIMER NO-YO ============================

def primer_no_yo(latentes, comandos, no_mias, jidx, retardos=2, nulos=12, semilla=0):
    """La dirección de su espacio latente que NINGÚN comando modula y que SIEMPRE empuja igual.

    Se ajusta la dinámica de sus propios latentes:   z[t+1] ≈ A·z[t] + B·z[t-1] + C·u[t] + d
    El vector `d` es el término constante: la parte de lo que ocurre que **no depende ni de lo que
    él hace ni de dónde está**. Es, literalmente, "lo que pasa igual haga lo que haga".

    Se mide SOLO sobre las variables que la contingencia declaró NO SUYAS (si se midiera sobre su
    cuerpo, la gravedad sobre su propio brazo lo contaminaría), y se compara contra el nulo de
    comandos desplazados. Su tamaño se declara en unidades de la desviación del propio latente.
    """
    rng = np.random.default_rng(semilla)
    cols = sorted(no_mias)
    if len(cols) < 2:
        return None

    def ajuste(rot):
        X, Y = [], []
        for z, u in zip(latentes, comandos):
            zz = z[:, cols]
            T = len(zz)
            uu = _desplazar(u, rng) if rot else u
            ini, fin = retardos, T - 1
            X.append(np.column_stack([zz[ini:fin], zz[ini - 1:fin - 1], uu[ini:fin],
                                      np.ones(fin - ini)]))
            Y.append(zz[ini + 1:fin + 1])
        X, Y = np.vstack(X), np.vstack(Y)
        w, *_ = np.linalg.lstsq(X, Y, rcond=None)
        return w[-1]                                     # el término constante: el vector d

    tren = [i for i in range(len(latentes)) if i not in jidx]
    lat_tr = [latentes[i] for i in tren]
    com_tr = [comandos[i] for i in tren]
    latentes, comandos = lat_tr, com_tr

    d = ajuste(False)
    nulo = np.array([np.linalg.norm(ajuste(True)) for _ in range(nulos)])
    fuerza = float(np.linalg.norm(d))
    return {"columnas": cols,
            "direccion": [round(float(x), 4) for x in (d / max(fuerza, 1e-12))],
            "fuerza": round(fuerza, 5),
            "nulo_media": round(float(nulo.mean()), 5),
            "nulo_techo": round(float(nulo.max()), 5),
            "supera_al_nulo": bool(fuerza > nulo.max())}


def veredicto_de_los_jueces(latentes, senales, no_mias, direccion, cols, jidx):
    """LADO HUMANO. Diego jamás ejecuta esto: comprueba si la dirección que él encontró
    corresponde a la caída real, usando la verdad del simulador (alturas de los objetos)."""
    proy, altura = [], []
    for i in jidx:
        z = latentes[i][:, cols]
        proy.append(z @ np.array(direccion))
        altura.append(senales[i][:, 3:6].mean(axis=1))     # altura media real de los objetos
    proy = np.concatenate(proy); altura = np.concatenate(altura)
    if proy.std() < 1e-9 or altura.std() < 1e-9:
        return 0.0
    return float(abs(np.corrcoef(proy, altura)[0, 1]))


def main():
    ap = argparse.ArgumentParser(description="Hito 0 completo: ojos propios sobre el Gimnasio")
    ap.add_argument("--episodios", type=int, default=12)
    ap.add_argument("--pasos", type=int, default=500)
    ap.add_argument("--latente", type=int, default=8)
    ap.add_argument("--epocas", type=int, default=8)
    ap.add_argument("--jueces", nargs="+", type=int, default=[10, 11, 12])
    ap.add_argument("--modo", default="normal")
    ap.add_argument("--control-nivel-b", action="store_true",
                    help="repite el experimento SIN gravedad: el primer no-yo debe DESAPARECER")
    a = ap.parse_args()

    modo = "sin_gravedad" if a.control_nivel_b else a.modo
    jidx = {j - 1 for j in a.jueces}
    print(f"=== HITO 0 — modo {modo} | {a.episodios} episodios x {a.pasos} cuadros | "
          f"latente {a.latente} | jueces {a.jueces} (congelados) ===", flush=True)

    eps, verdad, videos = correr(a.episodios, a.pasos, modo, render=True)
    comandos = [c for c, _ in eps]
    senales = [s for _, s in eps]
    print(f"grabado: video {videos[0].shape} por episodio", flush=True)

    modelo = entrenar_ojos(videos, jidx, a.latente, a.epocas)
    latentes = codificar(modelo, videos, jidx)
    print(f"latentes: {latentes[0].shape} — SUS variables, que nadie diseñó", flush=True)

    res = medir(list(zip(comandos, latentes)), a.jueces, nulos=10)
    mias = {r["variable"] for r in res if r["es_mia"]}
    no_mias = {r["variable"] for r in res} - mias
    print("\n--- NIVEL A: ¿qué parte de lo que veo soy YO? ---")
    for r in res:
        print(f"  z{r['variable']}: obedece en {r['obedece_en']:.2f} de las ventanas "
              f"(techo del nulo {r['nulo_techo']:.2f}) {'<- MÍA' if r['es_mia'] else ''}")
    print(f"  cuerpo hallado: {sorted(mias) or 'ninguno'} de {a.latente} latentes")

    nb = primer_no_yo(latentes, comandos, no_mias, jidx)
    print("\n--- NIVEL B: el primer no-yo ---")
    salida = {"modo": modo, "nivel_a": res, "cuerpo": sorted(mias), "nivel_b": nb,
              "verdad_de_los_jueces": sorted(verdad)}
    if nb is None:
        print("  no hay suficientes variables no-mías para buscarlo")
    else:
        print(f"  fuerza del empuje constante: {nb['fuerza']:.4f} "
              f"(techo del nulo {nb['nulo_techo']:.4f}) "
              f"-> {'SUPERA AL NULO' if nb['supera_al_nulo'] else 'no supera al nulo'}")
        corr = veredicto_de_los_jueces(latentes, senales, no_mias, nb["direccion"],
                                       nb["columnas"], jidx)
        salida["correlacion_con_la_caida_real"] = round(corr, 4)
        print(f"  [LADO HUMANO — los jueces] correlación de esa dirección con la altura real "
              f"de los objetos: {corr:.3f}")

    out = os.path.join(BASE, "resultados", f"p19-hito0-{modo}")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "resumen.json"), "w", encoding="utf-8") as f:
        json.dump(salida, f, indent=2, ensure_ascii=False)
    print(f"\nguardado en {out}/resumen.json")


if __name__ == "__main__":
    main()
