# koopman.py — EL OPERADOR DE KOOPMAN: la ruta nueva a los invariantes, tras el fracaso de F3.
# Implementado el 8-ago-2026 por orden del director ("implementa todo lo que dijiste").
#
# LA IDEA (álgebra pura, cero física): toda dinámica no lineal se vuelve LINEAL si en vez de
# mirar el estado x se miran funciones del estado Ψ(x). El operador K que avanza esas funciones
# en el tiempo (EDMD: mínimos cuadrados sobre un diccionario polinómico) tiene autofunciones; una
# autofunción con autovalor λ = 1 NO CAMBIA con el tiempo: **es una cantidad conservada**,
# encontrada sin que nadie nombre "energía".
#
# EL CRITERIO DE INVARIANTE (y es el que F3 no tenía): una función g es conservada si su varianza
# DENTRO de cada trayectoria es minúscula comparada con su varianza ENTRE trayectorias distintas.
# Constante dentro, distinta entre — eso separa un invariante real de la función constante trivial.
#
# Regla 31: en un oscilador (donde x²+v² se conserva) DEBE encontrarlo; en paseos aleatorios y en
# un sistema amortiguado (donde nada se conserva) DEBE callar.

import os
import sys
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _diccionario(X):
    """Polinomios hasta grado 2 — matemática genérica, sin nombres."""
    cols = [np.ones(len(X))]
    d = X.shape[1]
    for i in range(d):
        cols.append(X[:, i])
    for i in range(d):
        for j in range(i, d):
            cols.append(X[:, i] * X[:, j])
    return np.column_stack(cols)


# EL RESIDUO (añadido el 9-ago-2026, prerregistro-33). Está DEMOSTRADO matemáticamente que la
# discretización finita del operador de Koopman produce, además de los autovalores reales,
# FANTASMAS: autovalores espurios que son artefactos del truncamiento, no del mundo (polución
# espectral; el remedio publicado es calcular el residuo del operador infinito-dimensional).
# Para cada candidato λ con autofunción g se calcula
#       residuo^2 = ||(K − λI)g||^2 / ||g||^2
# estimado directamente de los datos. Un invariante REAL tiene residuo bajo; un fantasma no.
# Es nuestra Regla 31 con teorema incluido: la herramienta ya no solo pasa el nulo, ahora también
# certifica cuánto de fantasma tiene cada cosa que declara.
RESIDUO_MAXIMO = 0.10


def _residuo(Psi0, Psi1, v, lam):
    """||(K − λI)g|| / ||g|| estimado de los datos: g(x_t) = Psi(x_t)·v, y (Kg)(x_t) = g(x_{t+1}).
    Si g fuese autofunción exacta, g(x_{t+1}) = λ·g(x_t) y el residuo sería cero."""
    g0 = Psi0 @ v
    g1 = Psi1 @ v
    n0 = float(np.sqrt(np.mean(np.abs(g0) ** 2)))
    if n0 < 1e-12:
        return float("inf")
    return float(np.sqrt(np.mean(np.abs(g1 - lam * g0) ** 2)) / n0)


def invariantes(trayectorias, umbral_ratio=0.05, umbral_entre=0.2,
                residuo_maximo=RESIDUO_MAXIMO):
    """trayectorias: lista de arrays (T, d) — réplicas con condiciones iniciales distintas.
    Devuelve candidatos a cantidad conservada: autofunciones de K con |λ|≈1 cuya varianza
    dentro-de-trayectoria / entre-trayectorias sea < umbral_ratio Y cuyo RESIDUO sea bajo."""
    Psi0 = np.vstack([_diccionario(t[:-1]) for t in trayectorias])
    Psi1 = np.vstack([_diccionario(t[1:]) for t in trayectorias])
    K, *_ = np.linalg.lstsq(Psi0, Psi1, rcond=None)
    lam, V = np.linalg.eig(K.T)
    out = []
    for k in range(len(lam)):
        if abs(abs(lam[k]) - 1.0) > 0.02:
            continue
        v = np.real(V[:, k])
        valores = [_diccionario(t) @ v for t in trayectorias]
        dentro = float(np.mean([np.var(x) for x in valores]))
        medias = np.array([np.mean(x) for x in valores])
        entre = float(np.var(medias))
        escala = float(np.var(np.concatenate(valores))) + 1e-12
        # constante DENTRO, distinta ENTRE — si no distingue trayectorias, es la constante trivial
        if entre / escala > umbral_entre and dentro / (entre + 1e-12) < umbral_ratio:
            res = _residuo(Psi0, Psi1, v, lam[k])
            if res > residuo_maximo:
                continue          # FANTASMA: artefacto del truncamiento, no del mundo
            # DEDUPLICACION POR SUBESPACIO. HALLAZGO DEL 9-ago-2026, cazado por el banco al
            # correr EN LA NUBE lo que aqui pasaba: con una perturbacion del orden de 1e-12 —es
            # decir, con otra version de BLAS— la descomposicion devuelve DOS autovectores que
            # generan el MISMO observable, y el modulo los reportaba como dos invariantes.
            # No son dos: es uno visto dos veces. Contarlos por separado inflaria cualquier
            # recuento futuro de "cuantas cantidades conserva este mundo", que es justo la clase
            # de cifra sobre la que se construyen nodos.
            # Se comparan los OBSERVABLES (no los coeficientes): dos autovectores distintos
            # pueden dar la misma funcion sobre los datos.
            obs = np.concatenate(valores)
            obs = obs - obs.mean()
            n_obs = np.linalg.norm(obs)
            repetido = False
            for y in out:
                d = y["_obs"]
                if n_obs > 1e-12 and np.linalg.norm(d) > 1e-12:
                    coseno = abs(float(obs @ d) / (n_obs * np.linalg.norm(d)))
                    if coseno > 0.99:      # mismo observable salvo escala y signo
                        repetido = True
                        break
            if repetido:
                continue
            out.append({"lambda": complex(lam[k]), "coefs": np.round(v, 4),
                        "ratio_dentro_entre": round(dentro / (entre + 1e-12), 5),
                        "residuo": round(res, 5), "_obs": obs})
    for y in out:
        y.pop("_obs", None)
    return out


def regla31(verbose=True):
    rng = np.random.default_rng(13)
    fallos = []

    def oscilador(E, T=400, w=0.15):
        th = rng.uniform(0, 2 * np.pi)
        t = np.arange(T)
        x = np.sqrt(E) * np.cos(w * t + th)
        v = -np.sqrt(E) * np.sin(w * t + th)
        return np.column_stack([x, v])

    # 1) oscilador con energías distintas: DEBE hallar el invariante (x²+v² en el diccionario)
    tr = [oscilador(E) for E in (1.0, 2.5, 4.0, 6.0)]
    inv = invariantes(tr)
    c1 = len(inv) >= 1
    if verbose:
        print(f"  {'ok  ' if c1 else 'FALLO'} OSCILADOR: encuentra {len(inv)} invariante(s) "
              f"(ratio dentro/entre {inv[0]['ratio_dentro_entre'] if inv else '-'})")
    if not c1:
        fallos.append("oscilador")

    # 2) paseos aleatorios: nada se conserva -> debe callar
    tr2 = [np.column_stack([np.cumsum(rng.normal(size=400)),
                            np.cumsum(rng.normal(size=400))]) for _ in range(4)]
    inv2 = invariantes(tr2)
    c2 = len(inv2) == 0
    if verbose:
        print(f"  {'ok  ' if c2 else 'FALLO'} PASEOS: calla ({len(inv2)} falsos invariantes)")
    if not c2:
        fallos.append("paseos")

    # 3) oscilador AMORTIGUADO: la 'energía' decae -> no es invariante, debe callar
    def amortiguado(E, T=400, w=0.15, g=0.01):
        th = rng.uniform(0, 2 * np.pi)
        t = np.arange(T)
        a = np.sqrt(E) * np.exp(-g * t)
        return np.column_stack([a * np.cos(w * t + th), -a * np.sin(w * t + th)])
    inv3 = invariantes([amortiguado(E) for E in (1.0, 2.5, 4.0, 6.0)])
    c3 = len(inv3) == 0
    if verbose:
        print(f"  {'ok  ' if c3 else 'FALLO'} AMORTIGUADO: calla ({len(inv3)} falsos invariantes) "
              f"— lo que decae no se conserva")
    if not c3:
        fallos.append("amortiguado")

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — halla lo conservado y calla ante lo que decae o vaga."
                                if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Koopman/EDMD: invariantes sin nombrar la energía")
    ap.add_argument("--regla31", action="store_true")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    print("uso: --regla31 (su uso sobre datos reales exige prerregistro)")
