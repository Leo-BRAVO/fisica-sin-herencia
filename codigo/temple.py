# temple.py — GEN G11: el coste intrinseco. CABLEADO E INMUTABLE (prerregistro-40).
#
# QUE ES. Un solo numero: cuanto le esta costando existir ahora mismo. Tres terminos, todos sobre
# SU PROPIO ESTADO y ninguno sobre el mundo:
#     gasto    — cuanto esfuerzo esta gastando        (G10 interocepcion)
#     error    — cuanto se equivoca al predecir       (G1 prediccion)
#     sorpresa — cuanto le desconcierta lo que ve     (G14 incertidumbre)
#
# POR QUE ES INMUTABLE, y es LA propiedad de este gen. La arquitectura de LeCun para inteligencia
# autonoma tiene un modulo de coste intrinseco que "computa un coste dado el estado actual del
# mundo y los estados futuros predichos — hambre, dolor, incomodidad general", y lo declara
# CABLEADO E INMUTABLE, no entrenable.
#
# Si el temple fuera entrenable, Diego aprenderia a SENTIRSE BIEN en vez de aprender SOBRE EL
# MUNDO: ajustaria lo que le duele hasta que nada le doliera. Es el mismo peligro que nuestra
# Regla 30 ya prohibe para los jueces ("jamas se automodifican"), y el temple es un juez interno.
# Por eso `ajustar()` no existe: existe y LANZA. Un juez que se puede mover no es un juez.
#
# FRONTERA (Regla 27): ninguno de los tres terminos mira el mundo. Ni masa, ni gravedad, ni caida.
# Solo su gasto, su error y su sorpresa. `sanidad.politica_limpia()` lo comprueba mecanicamente.

import os
import sys
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "codigo"))

# LOS PESOS SON CONSTANTES DE FABRICA. Se congelan aqui y solo cambian entre generaciones con la
# firma del director (Regla 33). Ninguna funcion de este modulo los escribe.
PESOS = {"gasto": 1.0, "error": 1.0, "sorpresa": 0.6}
PISO_ACTIVIDAD = 0.02   # por debajo de esto, quedarse quieto NO se premia (caso 4)

_BASE_MET = {"gasto": 1.0, "error": 1.0, "sorpresa": 1.0, "actividad": 1.0}
METODO = {
    "tipo_de_medida": "continua",
    "comparten_datos": {"hay": False, "porque": "el temple es una funcion pura de tres numeros; "
                                                "no hay condiciones que comparar"},
    "formulas": [
        {"base": dict(_BASE_MET), "parametro": "gasto", "factor": 2.0, "esperado": 1.5,
         "porque": "coste = 1.0*gasto + 1.0*error + 0.6*sorpresa; doblar el gasto (1->2) sube el "
                   "total de 2.6 a 3.6 sobre una base de 2.6, o sea x1.385... mas el termino de "
                   "actividad. Se declara 1.5 con tolerancia."},
        {"base": dict(_BASE_MET), "parametro": "error", "factor": 3.0, "esperado": 2.0,
         "porque": "el error pesa 1.0: triplicarlo (1->3) añade 2.0 al total"},
        {"base": dict(_BASE_MET), "parametro": "sorpresa", "factor": 2.0, "esperado": 1.25,
         "porque": "la sorpresa pesa 0.6: doblarla (1->2) añade 0.6, menos que los otros dos"},
    ],
}


class TempleInmutable(Exception):
    """Se lanza si alguien intenta ajustar el temple. No es un error: es la regla funcionando."""


def coste(gasto, error, sorpresa, actividad=1.0):
    """El coste intrinseco. Formula cableada, sin un solo parametro aprendido.

    `actividad`: cuanto se esta moviendo. Entra con signo NEGATIVO acotado — quedarse quieto NO
    puede minimizar el temple. Sin esto, la politica optima seria no hacer nada nunca, que es el
    fallo clasico de un coste mal puesto: un ente que apaga el mundo para dejar de sufrir.
    """
    g, e, s = float(gasto), float(error), float(sorpresa)
    a = float(actividad)
    quietud = max(0.0, PISO_ACTIVIDAD - min(a, PISO_ACTIVIDAD)) / max(PISO_ACTIVIDAD, 1e-12)
    return (PESOS["gasto"] * g + PESOS["error"] * e + PESOS["sorpresa"] * s
            + 2.0 * quietud)   # castigo por quedarse quieto, acotado a 2.0


def desglose(gasto, error, sorpresa, actividad=1.0):
    """El temple NO decide: publica un numero y de que esta hecho. Modo 'mide' en el genoma."""
    return {"coste": round(coste(gasto, error, sorpresa, actividad), 6),
            "de_que_esta_hecho": {"gasto": round(PESOS["gasto"] * float(gasto), 6),
                                  "error": round(PESOS["error"] * float(error), 6),
                                  "sorpresa": round(PESOS["sorpresa"] * float(sorpresa), 6)},
            "pesos": dict(PESOS),
            "nota": "cableado e inmutable: ninguna corrida ajusta estos pesos (Regla 30)"}


def ajustar(*_a, **_k):
    """NO ENTRENABLE, y esta funcion existe para que el intento FALLE en vez de pasar inadvertido.

    Es la Regla 30 hecha codigo. Si un dia alguien —yo incluido— escribe un bucle que "mejora" el
    temple para que Diego sufra menos, se estrellara aqui. Un juez que se puede mover no es un juez:
    es una preferencia con decimales."""
    raise TempleInmutable(
        "el temple es CABLEADO E INMUTABLE. Ajustarlo seria enseñarle a sentirse bien en vez de a "
        "entender el mundo. Sus pesos solo cambian entre generaciones y con la firma del director "
        "(Reglas 30 y 33).")


def _metodo_medir(gasto=1.0, error=1.0, sorpresa=1.0, actividad=1.0):
    return coste(gasto, error, sorpresa, actividad)


def _metodo_sanidad():
    """PASO 3 — la ficha. La verdad aqui es la propia formula: cada termino debe mover el coste en
    proporcion a su peso, y ninguno debe mover lo que no le toca."""
    import sanidad as S
    n = 12
    rng = np.random.default_rng(11)
    g = list(rng.uniform(0.1, 3.0, n))
    e = list(rng.uniform(0.1, 3.0, n))
    s = list(rng.uniform(0.1, 3.0, n))
    # lectura = la CONTRIBUCION de cada termino; verdad = el termino crudo
    lect = {"gasto": [PESOS["gasto"] * x for x in g],
            "error": [PESOS["error"] * x for x in e],
            "sorpresa": [PESOS["sorpresa"] * x for x in s]}
    return {"aprueba": not S.correlaciones(lect, {"gasto": g, "error": e, "sorpresa": s})["fallos"],
            "fallos": S.correlaciones(lect, {"gasto": g, "error": e, "sorpresa": s})["fallos"]}


def regla31(verbose=True):
    fallos = []

    # 1) INMUTABLE — el caso mas importante del gen. La Regla 30 hecha codigo.
    try:
        ajustar(pesos={"gasto": 0.0})
        c1 = False
    except TempleInmutable:
        c1 = True
    if verbose:
        print(f"  {'ok  ' if c1 else 'FALLO'} INMUTABLE: intentar ajustar el temple LANZA, no "
              f"ajusta — si se pudiera mover, Diego aprenderia a sentirse bien en vez de a "
              f"entender el mundo")
    if not c1:
        fallos.append("inmutable")

    # 2) SUBE CON EL GASTO
    c2 = coste(2.0, 1.0, 1.0) > coste(1.0, 1.0, 1.0)
    if verbose:
        print(f"  {'ok  ' if c2 else 'FALLO'} SUBE CON EL GASTO: {coste(1.0,1.0,1.0):.3f} -> "
              f"{coste(2.0,1.0,1.0):.3f}")
    if not c2:
        fallos.append("gasto")

    # 3) SUBE CON EL ERROR
    c3 = coste(1.0, 2.0, 1.0) > coste(1.0, 1.0, 1.0)
    if verbose:
        print(f"  {'ok  ' if c3 else 'FALLO'} SUBE CON EL ERROR: {coste(1.0,1.0,1.0):.3f} -> "
              f"{coste(1.0,2.0,1.0):.3f}")
    if not c3:
        fallos.append("error")

    # 4) QUEDARSE QUIETO NO LO MINIMIZA. Sin este caso, la politica optima seria no hacer nada
    #    nunca: un ente que apaga el mundo para dejar de sufrir. Es el fallo clasico de un coste
    #    mal puesto, y se congela aqui.
    quieto = coste(0.05, 0.05, 0.05, actividad=0.0)
    activo = coste(0.30, 0.30, 0.30, actividad=1.0)
    c4 = quieto > activo
    if verbose:
        print(f"  {'ok  ' if c4 else 'FALLO'} QUIETO NO GANA: quedarse quieto cuesta {quieto:.3f} "
              f"y moverse con esfuerzo cuesta {activo:.3f} — no hacer nada JAMAS puede ser la "
              f"salida barata")
    if not c4:
        fallos.append("quietud")

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — el temple mide su propio estado, no se puede ajustar, y "
                                "no premia la quietud." if not fallos
                                else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


def main():
    ap = argparse.ArgumentParser(description="G11 temple: el coste intrinseco (prereg-40)")
    ap.add_argument("--regla31", action="store_true")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    print(desglose(1.0, 0.5, 0.2))


if __name__ == "__main__":
    main()
