# torneo_ojos.py — EL TORNEO DE SUS OJOS (prerregistro-27): A vs B vs C vs Ranuras.
#
# La primera generación de la Regla 33 corrida de verdad: cuatro arquitecturas visuales, mismo
# mundo, mismas semillas, aptitud del lado de los jueces (filogenia.aptitud), acta con
# filogenia.torneo(). Ninguna arquitectura ve su propio puntaje ni el de las demás.
#
# Uso: python torneo_ojos.py [--episodios 12] [--pasos 1500] [--epocas 12] [--semillas 5]

import os
import sys
import json
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "codigo"))

from gimnasio import correr
from ojos_gimnasio import entrenar_ojos
import percepcion2 as p2
import ranuras as rn
from filogenia import aptitud, torneo
import panel_jueces as pj

COMPETIDORES = ["A-pixel", "B-predictivo", "C-corolario", "R-ranuras"]


def codificar_competidor(nombre, videos, jidx, epocas, semilla, comandos=None):
    if nombre == "A-pixel":
        m = entrenar_ojos(videos, jidx, latente=8, epocas=epocas, semilla=semilla)
        return p2.codificar(m, videos, jidx)
    if nombre == "B-predictivo":
        m = p2.entrenar(videos, jidx, latente=8, epocas=epocas, semilla=semilla)
        return p2.codificar(m, videos, jidx)
    if nombre == "C-corolario":
        m = p2.entrenar(videos, jidx, latente=8, epocas=epocas, semilla=semilla, comandos=comandos)
        return p2.codificar(m, videos, jidx)
    if nombre == "R-ranuras":
        m = rn.entrenar(videos, jidx, k_ranuras=4, epocas=epocas, semilla=semilla)
        return rn.codificar(m, videos, jidx)
    raise ValueError(nombre)


def una_semilla_panel(semilla, episodios, pasos, epocas, jueces):
    """SEGUNDA VUELTA (prereg-38). Misma competencia, OTRA VARA.

    La primera vuelta quedo NO CONCLUYENTE POR INSTRUMENTO (INFORME-38): la aptitud del prereg-27
    aplastaba a los cuatro competidores en 0.0000 EXACTO porque el `max(margen, 0)` es un suelo, y
    el margen mismo satura en -0.4000 cuando ningun latente alcanza el piso de contingencia. La
    vara no medía a los competidores: medía su propio suelo.

    El panel del prereg-31 no tiene suelo, y mira TRES cosas distintas en vez de una: contingencia
    (¿sirven para hallar el cuerpo?), flecha (¿llevan dentro el sentido del tiempo?) y robustez
    (¿cuanto sobrevive al mundo mal visto?). Un competidor gana solo si gana o empata en LAS TRES.
    """
    jidx = {j - 1 for j in jueces}
    eps, verdad, videos = correr(episodios, pasos, "normal", render=True,
                                 semilla0=1000 + 5000 * semilla)
    comandos = [c for c, _ in eps]
    filas = []
    for nombre in COMPETIDORES:
        def _cod(vs, _n=nombre):
            return codificar_competidor(_n, vs, jidx, epocas, semilla, comandos)
        r = pj.evaluar(nombre, _cod, videos, comandos, jueces, nulos=8)
        filas.append(r)
        print(f"  [{nombre}] semilla {semilla}: contingencia {r['puntajes']['contingencia']:+.5f}  "
              f"flecha {r['puntajes']['flecha']:+.5f}  robustez {r['puntajes']['robustez']:+.5f}",
              flush=True)
    return filas


def una_semilla(semilla, episodios, pasos, epocas, jueces):
    jidx = {j - 1 for j in jueces}
    eps, verdad, videos = correr(episodios, pasos, "normal", render=True, semilla0=1000 + 5000 * semilla)
    comandos = [c for c, _ in eps]
    fila = {}
    for nombre in COMPETIDORES:
        lat = codificar_competidor(nombre, videos, jidx, epocas, semilla, comandos)
        r = aptitud(lat, comandos, jueces, verdad, nulos=8)
        fila[nombre] = r
        print(f"  [{nombre}] semilla {semilla}: puntaje {r['puntaje']:.4f} "
              f"(mías {r['n_mias']}, margen {r['margen_medio']:.4f})", flush=True)
    return fila


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--episodios", type=int, default=12)
    ap.add_argument("--pasos", type=int, default=1500)
    ap.add_argument("--epocas", type=int, default=12)
    ap.add_argument("--semilla", type=int, default=None,
                    help="si se da, corre SOLO esta semilla (para encolar por partes en el latido)")
    ap.add_argument("--semillas", type=int, default=5,
                    help="usado solo si --semilla no se da: cuenta semillas 1..N en una sola corrida")
    ap.add_argument("--jueces", nargs="+", type=int, default=[10, 11, 12])
    ap.add_argument("--panel", action="store_true",
                    help="prereg-38: SEGUNDA VUELTA con el panel de tres lecturas del prereg-31, "
                         "en lugar de la aptitud del prereg-27 que quedo no concluyente por "
                         "instrumento (INFORME-38). La vara vieja NO se toca.")
    a = ap.parse_args()

    rango = [a.semilla] if a.semilla is not None else list(range(1, a.semillas + 1))

    if a.panel:
        if a.semilla is None:
            raise SystemExit("la segunda vuelta se encola semilla por semilla: usa --semilla N")
        filas = una_semilla_panel(a.semilla, a.episodios, a.pasos, a.epocas, a.jueces)
        out = os.path.join(BASE, "resultados", f"p38-torneo-panel-s{a.semilla}")
        os.makedirs(out, exist_ok=True)
        with open(os.path.join(out, "resumen.json"), "w", encoding="utf-8") as f:
            json.dump({"prerregistro": 38, "semilla": a.semilla, "episodios": a.episodios,
                       "pasos": a.pasos, "epocas": a.epocas, "lecturas": list(pj.LECTURAS),
                       "resultados": filas,
                       "nota": "SIN veredicto: el veredicto exige las 5 semillas juntas, y mirarlas "
                               "antes de tiempo es exactamente el vicio que el prereg-27 cazo"},
                      f, indent=2, ensure_ascii=False)
        print(f"guardado en {out}/resumen.json (parcial — el veredicto se calcula con las 5)")
        return
    print(f"=== TORNEO DE OJOS (prereg-27) — semillas {rango} x "
          f"{a.episodios} ep x {a.pasos} cuadros ===", flush=True)
    por_semilla = []
    for s in rango:
        print(f"\n--- semilla {s} ---", flush=True)
        por_semilla.append(una_semilla(s, a.episodios, a.pasos, a.epocas, a.jueces))

    if a.semilla is not None:
        # UNA SOLA SEMILLA: se guarda sin veredicto (el veredicto exige verlas todas juntas,
        # y verlas juntas antes de tiempo seria exactamente el vicio que cazamos toda la semana).
        out = os.path.join(BASE, "resultados", f"p27-torneo-ojos-s{a.semilla}")
        os.makedirs(out, exist_ok=True)
        with open(os.path.join(out, "resumen.json"), "w", encoding="utf-8") as f:
            json.dump({"prerregistro": 27, "semilla": a.semilla, "episodios": a.episodios,
                       "pasos": a.pasos, "epocas": a.epocas, "resultados": por_semilla[0]},
                      f, indent=2, ensure_ascii=False)
        print(f"guardado en {out}/resumen.json (parcial — el veredicto se calcula con las 5)")
        return

    variantes = []
    for nombre in COMPETIDORES:
        puntajes = [f[nombre]["puntaje"] for f in por_semilla]
        variantes.append({"nombre": nombre, "puntaje": float(np.mean(puntajes)),
                          "puntaje_desv": float(np.std(puntajes)),
                          "puntajes_por_semilla": puntajes})

    veredicto = torneo(variantes, empate=0.0)  # el margen real lo aplica el criterio del prereg-27
    p1 = sorted(variantes, key=lambda v: -v["puntaje"])
    p_star, p_2 = p1[0], p1[1]
    separado = (p_star["puntaje"] - p_2["puntaje"]) > (p_star["puntaje_desv"] + p_2["puntaje_desv"])
    if p_star["puntaje"] <= 0:
        fallo = "NINGUNO SIRVE — ni el mejor supera 0 con margen"
    elif separado:
        fallo = f"GANA {p_star['nombre']} — separación real"
    else:
        orden_parsimonia = {"A-pixel": 0, "B-predictivo": 1, "C-corolario": 2, "R-ranuras": 3}
        empatados = [v for v in p1 if v["puntaje"] > 0
                    and p_star["puntaje"] - v["puntaje"] <= p_star["puntaje_desv"] + v["puntaje_desv"]]
        ganador_navaja = min(empatados, key=lambda v: orden_parsimonia[v["nombre"]])
        fallo = f"EMPATE TÉCNICO — gana {ganador_navaja['nombre']} por parsimonia (navaja, no evidencia)"

    print("\n" + "=" * 70)
    print("TABLA FINAL (media ± desviación entre semillas):")
    for v in sorted(variantes, key=lambda x: -x["puntaje"]):
        print(f"  {v['nombre']:<14} {v['puntaje']:+.4f} ± {v['puntaje_desv']:.4f}   "
              f"{v['puntajes_por_semilla']}")
    print(f"\nVEREDICTO DEL PRERREG-27: {fallo}")
    print("=" * 70)

    out = os.path.join(BASE, "resultados", "p27-torneo-ojos")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "resumen.json"), "w", encoding="utf-8") as f:
        json.dump({"prerregistro": 27, "semillas": a.semillas, "episodios": a.episodios,
                   "pasos": a.pasos, "epocas": a.epocas, "variantes": variantes,
                   "veredicto_estadio": veredicto, "veredicto_prereg27": fallo},
                  f, indent=2, ensure_ascii=False)
    print(f"guardado en {out}/resumen.json")


if __name__ == "__main__":
    main()
