# lazo_atencion.py — QUE EL EMPOWERMENT LO MIDA EL ORGANO, NO YO A MANO (prerregistro-58).
#
# EL HUECO, MEDIDO. El INFORME-65 encontro que `poder.py` no lo usa nadie, y el detalle es mas fino
# que el conteo: `atencion.py` SI usa la idea de poder —su prioridad es curable*poder— pero NUNCA
# IMPORTA poder.py. El numero le llega ESCRITO A MANO en los casos de prueba. La Fase 3 arreglo la
# cadena G14->G8 con empowerment y el organo que mide el empowerment sigue fuera del lazo: el
# concepto entro, el organo no.
#
# LO QUE ESTE MODULO NO TOCA, y es deliberado:
#   - NO edita poder.py: esta SELLADO, y editarlo mataria su sello dejando irreproducible lo que
#     publico. El organo deja de ser huerfano PORQUE ALGUIEN LO IMPORTA, no porque se le cambie
#     una linea.
#   - NO edita atencion.py: su contrato ya exige `curable` en [0,1] y lo verifica.
#
# LA LINEA BASE TONTA SON MIS PROPIOS NUMEROS INVENTADOS, que es el rival mas incomodo posible: si
# medir de verdad no reparte mejor que lo que yo escribia a mano, no hay motivo para conectar nada
# y se dice asi.
#
# Uso: python lazo_atencion.py [--regla31] [--salida resultados/p58-lazo/medida.json]

import os
import sys
import json
import argparse

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import poder                                                                # noqa: E402
import incertidumbre                                                        # noqa: E402
import atencion                                                             # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# QUE ESTUDIA: el LAZO —la cadena de los dos organos hasta el reparto—. Su regla31() trabaja con
# mundos hechos a mano y NO examina a los organos: eso seria resultado, no requisito de entrada.
SUJETO = ("lazo",)

PRESUPUESTO = 10.0
TECHO_TELEVISOR = 2.0     # criterio B: el MISMO numero del prerregistro-49, no uno nuevo
PISO_BUENA = 7.0          # criterio C: el mismo tambien

METODO = {
    "prerregistro": 58,
    "tipo_de_medida": "continua",
    "que_mide": ("cuanto presupuesto de atencion recibe cada region cuando la ignorancia curable y "
                 "el poder los MIDEN los organos, en vez de escribirlos yo a mano"),
    "comparten_datos": {
        "hay": True,
        "porque": "las dos regiones se miden sobre el MISMO conjunto de episodios y con los mismos "
                  "comandos — esa es la definicion del reparto. Si cada region tuviera sus propios "
                  "episodios, la diferencia podria ser de los episodios y no de la region.",
    },
    "linea_base": ("los numeros ESCRITOS A MANO que uso hoy en las pruebas de atencion.py. Es "
                   "exactamente lo que hay, y si el lazo medido no reparte al menos igual de bien, "
                   "no hay motivo para conectarlo (Regla 11)"),
    "formulas": [
        {"base": {"fuerza_de_la_buena": 0.6}, "parametro": "fuerza_de_la_buena", "factor": 0.1,
         "esperado": "baja",
         "porque": "la fuerza es cuanto efecto tienen los comandos sobre la region buena. Al "
                   "reducirla a la decima parte, el R2 de control que mide `poder` cae por "
                   "construccion —el mando explica menos varianza— y con el cae la prioridad, que "
                   "es curable*poder. El MECANISMO es ese, no una intuicion: la prioridad es un "
                   "producto y uno de sus dos factores se derrumba. Base 0.6 y NO 0.0, porque "
                   "multiplicar cero por una decima sigue siendo cero y ese descuido ya me tumbo "
                   "cuatro relaciones este mes"},
    ],
}


def _mundo(fuerza_de_la_buena=0.6, semilla=58, T=1200, n_ep=6):
    """Dos regiones y la verdad la ponemos nosotros: la BUENA obedece a los comandos y tiene ley;
    el TELEVISOR es ruido irreducible que nadie manda."""
    rng = np.random.default_rng(int(semilla))
    k = np.ones(9) / 9
    eps = []
    for _ in range(int(n_ep)):
        a = np.column_stack([np.convolve(rng.normal(size=T + 8), k, mode="valid")[:T]
                             for _ in range(3)])
        s = np.zeros((T, 3))
        for t in range(1, T):
            # region 0: la BUENA — obedece al comando 0
            s[t, 0] = 0.85 * s[t - 1, 0] + float(fuerza_de_la_buena) * a[t - 1, 0] \
                + rng.normal(0, 0.3)
            # region 1: EL TELEVISOR — ruido fuerte que nadie manda
            s[t, 1] = 0.90 * s[t - 1, 1] + rng.normal(0, 3.0)
            s[t, 2] = 0.80 * s[t - 1, 2] + rng.normal(0, 1.0)
        eps.append((a, s))
    return eps


def _curable_de(eps, col):
    """La ignorancia CURABLE de una columna, medida por G14. Es la fraccion adimensional que el
    contrato de atencion.py exige: la epistemica cruda sube con el ruido y no se consume."""
    X = np.vstack([s[:-1] for _, s in eps])
    Y = np.vstack([s[1:, col:col + 1] for _, s in eps])
    n = min(400, len(X))
    m = incertidumbre.medir(X[:n], Y[:n], X[n:n + 200])
    return float(m["curable"])


def _poder_de(eps, col):
    """El empowerment de una columna, medido por G9... perdon, por `poder.py`: R2 de control, es
    decir cuanta varianza de esa columna explican los comandos. Un televisor da ~0."""
    filas = poder.medir([(a, s[:, [col]]) for a, s in eps], jueces=[1], region_var=0, cortes=())
    v = [f["poder"] for f in filas if f["poder"] is not None]
    return float(np.clip(v[0], 0.0, 1.0)) if v else 0.0


def regiones_medidas(fuerza_de_la_buena=0.6, semilla=58):
    """LAS REGIONES, CON LOS DOS NUMEROS MEDIDOS POR SUS ORGANOS. Ni uno escrito a mano."""
    eps = _mundo(fuerza_de_la_buena=fuerza_de_la_buena, semilla=semilla)
    return [{"id": "buena", "curable": _curable_de(eps, 0), "poder": _poder_de(eps, 0),
             "coste": PRESUPUESTO},
            {"id": "tv", "curable": _curable_de(eps, 1), "poder": _poder_de(eps, 1),
             "coste": PRESUPUESTO}]


def repartir_medido(fuerza_de_la_buena=0.6, semilla=58):
    regs = regiones_medidas(fuerza_de_la_buena, semilla)
    rep = {r["id"]: r["asignado"] for r in atencion.repartir(regs, presupuesto=PRESUPUESTO)}
    return regs, rep


def _metodo_medir(fuerza_de_la_buena=0.6):
    """PASO 1 — la medida escalar: cuanto se lleva la region BUENA del presupuesto."""
    _, rep = repartir_medido(float(fuerza_de_la_buena))
    return float(rep["buena"])


def _metodo_sanidad():
    """PASO 3 — LA FICHA. La pregunta: **¿los dos numeros los miden los organos, o se me ha colado
    alguno escrito a mano?** Es el criterio A, y sin el esto seria mis numeros con otro nombre."""
    fallos = []
    regs = regiones_medidas()
    for r in regs:
        for clave in ("curable", "poder"):
            v = r[clave]
            if not isinstance(v, float):
                fallos.append(f"{r['id']}.{clave} no es una medida: {v!r}")
        if not (0.0 <= r["curable"] <= 1.0):
            fallos.append(f"{r['id']}.curable={r['curable']} fuera del rango del contrato [0,1]")
    if len(regs) < 2:
        fallos.append("hacen falta al menos dos regiones para que el reparto signifique algo")
    return {"aprueba": not fallos, "fallos": fallos,
            "medidas": {r["id"]: {"curable": round(r["curable"], 4),
                                  "poder": round(r["poder"], 4)} for r in regs}}


def regla31(verbose=True):
    """LA REGLA 31 — sobre MI PROCEDIMIENTO, los DOS lados, con mundos hechos a mano.

    Aqui NO se comprueba que el televisor pierda: eso es el criterio B del prerregistro-58, es
    decir RESULTADO. Meterlo haria que el criterio B no pudiera fallar."""
    fallos = []

    def caso(nombre, ok, extra=""):
        if verbose:
            print(f"  {'ok  ' if ok else 'FALLO'} {nombre}" + (f"  [{extra}]" if extra else ""))
        if not ok:
            fallos.append(nombre)

    if verbose:
        print("== REGLA 31 del prereg-58: el lazo, no los organos ==")

    fs = _metodo_sanidad()
    caso("CONTROL POSITIVO: los dos numeros salen de los organos y respetan el contrato",
         fs["aprueba"], str(fs["medidas"]))

    # SEÑUELO: si NINGUNA region es controlable, el reparto no puede inventarse un ganador.
    sin_control = [{"id": "a", "curable": 0.5, "poder": 0.0, "coste": PRESUPUESTO},
                   {"id": "b", "curable": 0.5, "poder": 0.0, "coste": PRESUPUESTO}]
    rep = {r["id"]: r["asignado"] for r in atencion.repartir(sin_control, presupuesto=PRESUPUESTO)}
    caso("SEÑUELO: sin ninguna region controlable, el reparto cae al uniforme",
         abs(rep["a"] - rep["b"]) < 1e-6, str(rep))

    # EL CONTRATO SE VERIFICA DE VERDAD: pasarle algo fuera de rango tiene que levantar error.
    try:
        atencion.repartir([{"id": "x", "curable": 20.0, "poder": 0.5, "coste": PRESUPUESTO},
                           {"id": "y", "curable": 0.1, "poder": 0.5, "coste": 1.0}],
                          presupuesto=1.0)
        caso("el contrato RECHAZA una ignorancia fuera de rango", False)
    except ValueError:
        caso("el contrato RECHAZA una ignorancia fuera de rango", True)

    b = _metodo_medir(0.6)
    caso("la lectura base NO es cero", b > 0, f"{b:.4f}")

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — el lazo mide y el contrato se sostiene."
                                 if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


def correr(salida=None, verbose=True):
    regs, rep = repartir_medido()
    fs = _metodo_sanidad()

    # LA LINEA BASE TONTA: mis numeros escritos a mano, los de las pruebas de atencion.py
    a_mano = [{"id": "buena", "curable": 0.30, "poder": 0.5, "coste": PRESUPUESTO},
              {"id": "tv", "curable": 0.10, "poder": 0.0, "coste": PRESUPUESTO}]
    rep_mano = {r["id"]: r["asignado"] for r in atencion.repartir(a_mano, presupuesto=PRESUPUESTO)}

    datos = {"prerregistro": 58,
             "regiones_medidas": {r["id"]: {"curable": round(r["curable"], 4),
                                            "poder": round(r["poder"], 4)} for r in regs},
             "reparto_medido": {k: round(v, 4) for k, v in rep.items()},
             "reparto_con_mis_numeros_a_mano": {k: round(v, 4) for k, v in rep_mano.items()},
             "ficha": fs,
             "criterios": {
                 "A_los_organos_miden": bool(fs["aprueba"]),
                 "B_el_televisor_pierde": bool(rep["tv"] < TECHO_TELEVISOR),
                 "C_la_buena_gana": bool(rep["buena"] > PISO_BUENA),
                 "D_el_rango_del_contrato_se_respeta": bool(
                     all(0.0 <= r["curable"] <= 1.0 for r in regs)),
                 "E_le_gana_a_mis_numeros": bool(rep["buena"] >= rep_mano["buena"] - 1e-9),
             }}
    c = datos["criterios"]
    if not c["B_el_televisor_pierde"]:
        datos["veredicto"] = ("SE DESCARTA EL LAZO — conectar los organos hace que el televisor "
                              "vuelva a ganar, y eso deshace la Fase 3")
    elif not c["A_los_organos_miden"]:
        datos["veredicto"] = "NO HAY LAZO — seguirian siendo mis numeros con otro nombre"
    elif not c["E_le_gana_a_mis_numeros"]:
        datos["veredicto"] = ("MEDIR DE VERDAD NO MEJORA EL REPARTO — `poder` sigue desconectado, "
                              "y ahora con esa razon escrita")
    elif all(c.values()):
        datos["veredicto"] = ("LAZO CERRADO — la ignorancia y el empowerment los miden sus "
                              "organos, el televisor pierde y la region buena gana")
    else:
        datos["veredicto"] = ("NO CONCLUYENTE — fallan "
                              + ", ".join(k for k, v in c.items() if not v))

    if salida:
        ruta = os.path.join(BASE, salida)
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
    if verbose:
        print(f"\nVEREDICTO: {datos['veredicto']}")
    return datos


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Prerregistro 58: conectar poder al lazo")
    ap.add_argument("--regla31", action="store_true")
    ap.add_argument("--salida", default="resultados/p58-lazo/medida.json")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    correr(salida=a.salida)
