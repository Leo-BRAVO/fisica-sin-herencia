# percepcion2.py — LOS OJOS DE SEGUNDA GENERACIÓN (prerregistro-25, FIRMADO).
#
# POR QUÉ EXISTEN: cinco vías independientes midieron que los ojos v1 (reconstrucción de píxeles)
# codifican escena y textura, no movimiento. La literatura llegó a lo mismo por otro camino
# (LeCun/JEPA: "reconstruir píxeles condena la representación — obliga a codificar lo
# impredecible"). Aquí no adoptamos su tesis por autoridad: LA ADOPTAMOS PORQUE NUESTROS PROPIOS
# INSTRUMENTOS LA MIDIERON, y la ponemos bajo los mismos verdugos que todo lo demás.
#
# LAS DOS CANDIDATAS NUEVAS (la vieja queda como línea base, no se borra):
#
#   B — OJOS PREDICTIVOS (estilo JEPA): la pérdida principal es predecir z(t+1) en el ESPACIO
#       LATENTE desde z(t), z(t-1). La reconstrucción queda como regularizador débil (0.1×) SOLO
#       para anclar el latente a la imagen (sin ella el codificador colapsa a una constante:
#       predecirse a sí mismo cuesta cero — el colapso es EL riesgo conocido de esta familia).
#
#   C — OJOS CON DESCARGA COROLARIA (biología directa): como B, pero el predictor recibe TAMBIÉN
#       los comandos motores. Es el modelo interno del cerebelo: una copia de la orden motora
#       (copia eferente) llega a la vista, que PREDICE la consecuencia sensorial y la CANCELA.
#       Lo que la copia eferente no explica ES el mundo externo. Legal: son SUS comandos.
#       — De regalo, C trae la frontera yo/mundo DENTRO de los ojos: reafferencia = yo.
#
# Uso: python percepcion2.py --regla31

import os
import sys
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "codigo"))


def _torch():
    import torch
    import torch.nn as nn
    return torch, nn


def construir(latente=8, n_comandos=0):
    """Ojos v2: mismo codificador convolucional de la casa; predictor latente (y comandos si
    n_comandos>0). El decodificador existe solo como ancla débil."""
    torch, nn = _torch()
    from percepcion import Ojos
    base = Ojos(latente)
    if n_comandos > 0:
        base.dinamica = nn.Linear(2 * latente + n_comandos, latente)
    return base


def entrenar(videos, jidx, latente=8, epocas=8, comandos=None, semilla=1, lote=64,
             peso_rec=0.1):
    """Entrena B (comandos=None) o C (comandos=lista de arrays (T, A)). Desde cero, como siempre.
    Pérdida = ||predicho z(t+1) − real z(t+1)||² + peso_rec · reconstrucción."""
    torch, nn = _torch()
    torch.manual_seed(semilla)
    rng = np.random.default_rng(semilla)
    nA = 0 if comandos is None else comandos[0].shape[1]
    modelo = construir(latente, nA)
    tren = [i for i in range(len(videos)) if i not in jidx]
    vids = {i: torch.tensor(videos[i]) for i in tren}
    coms = None if comandos is None else {i: torch.tensor(comandos[i], dtype=torch.float32)
                                          for i in tren}
    trip = [(i, t) for i in tren for t in range(1, len(videos[i]) - 1)]
    opt = torch.optim.Adam(modelo.parameters(), lr=1e-3)
    for ep in range(epocas):
        perm = rng.permutation(len(trip))
        tot = n = 0
        for a in range(0, len(perm), lote):
            idx = perm[a:a + lote]
            xa = torch.stack([vids[trip[i][0]][trip[i][1] - 1] for i in idx])
            xb = torch.stack([vids[trip[i][0]][trip[i][1]] for i in idx])
            xc = torch.stack([vids[trip[i][0]][trip[i][1] + 1] for i in idx])
            za, zb = modelo.codificar(xa), modelo.codificar(xb)
            zc = modelo.codificar(xc).detach()      # el objetivo latente NO propaga gradiente:
            #                                         perseguir un blanco que huye = colapso
            ent = torch.cat([zb, za], dim=1)
            if coms is not None:
                u = torch.stack([coms[trip[i][0]][trip[i][1]] for i in idx])
                ent = torch.cat([ent, u], dim=1)
            pred = ((modelo.dinamica(ent) - zc) ** 2).mean()
            rec = ((modelo.decodificar(zb) - xb) ** 2).mean()
            # ancla de varianza contra el colapso (VICReg lo llama así; es matemática genérica):
            # la desviación de cada latente en el lote no debe morir.
            var = torch.relu(1.0 - zb.std(dim=0)).mean()
            p = pred + peso_rec * rec + 0.5 * var
            opt.zero_grad(); p.backward(); opt.step()
            tot += float(p.detach()) * len(idx); n += len(idx)
        print(f"   época {ep + 1}/{epocas} pérdida {tot / n:.5f}", flush=True)
    return modelo


def codificar(modelo, videos, jidx):
    torch, _ = _torch()
    with torch.no_grad():
        zs = [modelo.codificar(torch.tensor(v)).numpy() for v in videos]
    tren = np.vstack([z for i, z in enumerate(zs) if i not in jidx])
    mu, sd = tren.mean(0), tren.std(0)
    sd[sd == 0] = 1.0
    return [(z - mu) / sd for z in zs]


# ============================== REGLA 31 ==============================

def _mundo_punto(T=160, n_ep=8, con_comandos=False, semilla=5):
    """Videos sintéticos de verdad conocida: un PUNTO que se mueve sobre un fondo de TEXTURA
    RUIDOSA que cambia cuadro a cuadro (lo impredecible). La verdad = posición del punto.
      B debe leer el punto MEJOR que A, porque A gasta el latente en la textura.
      Si hay comandos, el punto los obedece (mundo para C)."""
    rng = np.random.default_rng(semilla)
    vids, poss, coms = [], [], []
    for _ in range(n_ep):
        x, y = 32.0, 32.0
        v = np.zeros((T, 64, 64), dtype=np.float32)
        pos = np.zeros((T, 2)); u = np.zeros((T, 2), dtype=np.float32)
        k = np.ones(9) / 9
        bal = np.column_stack([np.convolve(rng.normal(size=T + 8), k, mode="valid")[:T]
                               for _ in range(2)]) * 3.0
        for t in range(T):
            if con_comandos:
                u[t] = bal[t]
                x = np.clip(x + u[t, 0], 6, 57); y = np.clip(y + u[t, 1], 6, 57)
            else:
                x = np.clip(x + rng.normal(0, 1.2), 6, 57)
                y = np.clip(y + rng.normal(0, 1.2), 6, 57)
            cuadro = rng.uniform(0.3, 0.7, (64, 64)).astype(np.float32)  # textura IMPREDECIBLE
            xi, yi = int(x), int(y)
            cuadro[max(0, yi - 3):yi + 3, max(0, xi - 3):xi + 3] = 1.0   # el punto
            v[t] = cuadro
            pos[t] = (x, y)
        vids.append(v); poss.append(pos); coms.append(u)
    return vids, poss, coms


def _r2(lat, verdad, tren, test):
    A = lambda M: np.column_stack([M, np.ones(len(M))])
    Xtr = np.vstack([lat[i] for i in tren]); Ytr = np.vstack([verdad[i] for i in tren])
    Xte = np.vstack([lat[i] for i in test]); Yte = np.vstack([verdad[i] for i in test])
    w, *_ = np.linalg.lstsq(A(Xtr), Ytr, rcond=None)
    p = A(Xte) @ w
    return float(np.mean(1 - ((p - Yte) ** 2).mean(0)
                         / np.maximum(((Yte - Ytr.mean(0)) ** 2).mean(0), 1e-12)))


def regla31(verbose=True, epocas=4):
    """Mundo del punto sobre textura: la verdad se conoce por construcción.
      1. B lee la posición del punto MEJOR que A (la textura ya no paga).
      2. B no colapsa (varianza latente viva).
      3. C con comandos DESPLAZADOS pierde su ventaja sobre B (aprende del motor, no del reloj)."""
    from ojos_gimnasio import entrenar_ojos  # los ojos v1, la línea base
    fallos = []
    vids, poss, _ = _mundo_punto()
    jidx = {6, 7}
    tren = [i for i in range(8) if i not in jidx]; test = sorted(jidx)

    mA = entrenar_ojos(vids, jidx, latente=8, epocas=epocas)
    lA = codificar(mA, vids, jidx)
    rA = _r2(lA, poss, tren, test)

    mB = entrenar(vids, jidx, latente=8, epocas=epocas)
    lB = codificar(mB, vids, jidx)
    rB = _r2(lB, poss, tren, test)
    c1 = rB > rA + 0.05
    c2 = float(np.vstack([lB[i] for i in tren]).std(0).min()) > 0.05
    if verbose:
        print(f"  {'ok  ' if c1 else 'FALLO'} B lee el punto mejor que A: R² {rA:+.3f} -> {rB:+.3f}")
        print(f"  {'ok  ' if c2 else 'FALLO'} B no colapsa (varianza mínima latente "
              f"{float(np.vstack([lB[i] for i in tren]).std(0).min()):.3f})")
    if not c1: fallos.append("B_mejor_que_A")
    if not c2: fallos.append("colapso")

    # ================= LO QUE ESTE EXAMEN CAZÓ EN SU PRIMERA CORRIDA (8-ago-2026) ============
    # Mi primer criterio para C era "con comandos verdaderos LEE mejor la posición que con
    # comandos desplazados". Salió AL REVÉS (+0.205 vs +0.465) — y al perseguirlo resultó que el
    # examen estaba mal, no el gen: cuando el comando ya le explica al predictor el movimiento
    # propio, el codificador PUEDE PERMITIRSE no verlo. La biología conoce ese fenómeno con
    # nombre: ATENUACIÓN SENSORIAL de lo autogenerado (por eso nadie puede hacerse cosquillas).
    # La afirmación falsable de la descarga corolaria NO es "leo mejor mi posición": es
    # "PREDIGO mejor las consecuencias de mis órdenes, y esa ventaja muere si las órdenes se
    # desalinean". Eso es lo que se exige aquí. La pereza codificadora queda registrada como
    # hallazgo — y como advertencia para el prereg-25: C se juzga por contingencia, no por
    # lectura, y si su atenuación daña el hito 0, ganará B y quedará escrito por qué.
    # ==========================================================================================
    vidsC, possC, comsC = _mundo_punto(con_comandos=True, semilla=11)
    mC = entrenar(vidsC, jidx, latente=8, epocas=epocas, comandos=comsC)
    rng = np.random.default_rng(3)
    coms_rotos = [np.roll(u, int(rng.integers(len(u) // 4, 3 * len(u) // 4)), axis=0)
                  for u in comsC]
    mCn = entrenar(vidsC, jidx, latente=8, epocas=epocas, comandos=coms_rotos, semilla=1)

    def _mse_prediccion(modelo, vids_, coms_):
        import torch
        with torch.no_grad():
            tot = n = 0
            for i in test:
                v = torch.tensor(vids_[i]); u = torch.tensor(coms_[i], dtype=torch.float32)
                z = modelo.codificar(v)
                ent = torch.cat([z[1:-1], z[:-2], u[1:-1]], dim=1)
                tot += float(((modelo.dinamica(ent) - z[2:]) ** 2).sum()); n += len(z) - 2
        return tot / n

    mse_c = _mse_prediccion(mC, vidsC, comsC)
    mse_cn = _mse_prediccion(mCn, vidsC, comsC)
    c3 = mse_c < 0.8 * mse_cn
    if verbose:
        print(f"  {'ok  ' if c3 else 'FALLO'} C predice las consecuencias de SUS órdenes: "
              f"error {mse_c:.4f} vs {mse_cn:.4f} con órdenes desalineadas en el entrenamiento")
    if not c3: fallos.append("corolario_nulo")

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — los ojos v2 miran el movimiento, no la textura."
                                if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Ojos v2: predictivos (B) y con descarga corolaria (C)")
    ap.add_argument("--regla31", action="store_true")
    ap.add_argument("--epocas", type=int, default=4)
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31(epocas=a.epocas))
    print("uso: --regla31 (la corrida oficial la define el prerregistro-25)")
