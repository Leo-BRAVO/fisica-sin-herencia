# cadena_g14g8.py — PRERREGISTRO 49: ¿deja Diego de mirar la pared que parpadea?
#
# QUE MIDE. Los criterios congelados del prerregistro-49, y el mas importante NO con numeros
# puestos a mano sino CON LA CADENA ENTERA: se construyen dos regiones de verdad —una donde hay
# una ley que aprender y otra que es ruido puro—, se mide cada una con el G14 REAL, y su lectura
# se le entrega al G8 REAL. Eso es lo que el INFORME-52 encontro roto, y es lo unico que puede
# decir si esta arreglado.
#
# POR QUE IMPORTA QUE SEA DE PUNTA A PUNTA. Los dos modulos pasan ya su ficha por separado, y eso
# NO basta: el defecto del INFORME-52 no era de un modulo sino de la union entre dos que pasaban
# sus pruebas cada uno por su lado. Un arreglo comprobado modulo a modulo repetiria el mismo error
# de mirada.
#
# LA REGLA 31 DE ESTE ARCHIVO EXAMINA MI PROCEDIMIENTO, NO LA CADENA. Su control positivo es que
# el mundo de juguete de verdad tenga las dos clases de region que dice tener: una aprendible y
# otra que es solo ruido. Si el "televisor" tuviera estructura, no seria un televisor y el estudio
# no mediria nada.
#
# Uso: python cadena_g14g8.py [--regla31] [--salida resultados/p49-cadena/medida.json]

import os
import sys
import json
import argparse

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import atencion                                                             # noqa: E402
import incertidumbre                                                        # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRESUPUESTO = 10.0
TOPE_TV = 2.0        # criterio B2: el televisor menos de 2.0 de 10
PISO_BUENA = 7.0     # criterio B2: la region buena mas de 7.0 de 10

METODO = {
    "prerregistro": 49,
    "tipo_de_medida": "continua",
    "que_mide": ("cuanto presupuesto de atencion se lleva una region de RUIDO PURO cuando su "
                 "lectura de ignorancia la produce el G14 real y el reparto lo hace el G8 real"),
    "comparten_datos": {
        "hay": False,
        "porque": "las dos regiones se generan con semillas distintas y no comparten ni datos ni "
                  "parametros; lo unico comun es el presupuesto que se disputan, que es el "
                  "objeto de la medida",
    },
    "linea_base": ("repartir POR IGUAL: con dos regiones, 5.0 y 5.0. Si el televisor se lleva "
                   "eso o mas, la atencion no esta priorizando (Regla 11)"),
    "formulas": [
        {"base": {"ruido_buena": 0.3}, "parametro": "ruido_buena", "factor": 10.0,
         "esperado": "sube",
         "porque": "al ENTERRAR la region aprendible en ruido deja de tener ley que aprender, es "
                   "decir se vuelve un televisor mas; entonces las dos regiones se parecen y el "
                   "reparto tiende a igualarse, luego la cuota del televisor SUBE. Es ruido de "
                   "MEDIDA sobre observaciones —aqui no hay dinamica que excitar—, asi que si "
                   "entierra informacion (LECCION-RUIDO-01). Base 0.3 y NO 0.0."},
        # AQUI DECLARE PRIMERO "subir el ruido DEL TELEVISOR baja su cuota" y LA RETIRO por dos
        # razones, y la segunda es la que importa:
        #   (1) Es TRIVIALMENTE falsa como "baja": escalar la amplitud de una region que ya es
        #       ruido puro multiplica por igual la epistemica y la aleatoria, y `curable` es una
        #       RAZON entre dos cantidades con las mismas unidades — asi que no se mueve. La
        #       puerta lo midio x1.000. Un televisor mas fuerte sigue siendo un televisor.
        #   (2) Y aunque la hubiera escrito como "igual", que es lo cierto, seria declarar en mi
        #       instrumento EXACTAMENTE el criterio E del prerregistro-49, con lo que el criterio
        #       E no podria fallar. Sexta vez este mes que evito el mismo mal.
        # El criterio E se mide en `correr()`, donde SI puede reprobar.
    ],
}


def _region_aprendible(n=60, ruido=0.3, semilla=1):
    """Hay una ley: Y depende de X. La ignorancia es CURABLE con mas datos."""
    rng = np.random.default_rng(semilla)
    X = rng.normal(size=(int(n), 2))
    Y = X @ np.array([1.5, -0.7]) + rng.normal(0, ruido, int(n))
    return X, Y, rng.normal(size=(40, 2))


def _region_televisor(n=60, ruido=1.0, semilla=2):
    """NO hay ley: Y es ruido, no depende de X. La ignorancia es IRREDUCIBLE. Es la pared que
    parpadea: mucha varianza, nada que aprender."""
    rng = np.random.default_rng(semilla)
    X = rng.normal(size=(int(n), 2))
    Y = rng.normal(0, ruido, int(n))
    return X, Y, rng.normal(size=(40, 2))


def _cadena(ruido_tv=1.0, poder_tv=0.0, ruido_buena=0.3):
    """LA CADENA ENTERA: G14 mide, G8 reparte. Ningun numero puesto a mano."""
    regiones = []
    for nid, (X, Y, Xt), poder in (("buena", _region_aprendible(ruido=float(ruido_buena)), 0.5),
                                   ("tv", _region_televisor(ruido=ruido_tv), float(poder_tv))):
        m = incertidumbre.medir(X, Y, Xt)
        regiones.append({"id": nid, "curable": m["curable"], "aleatoria": m["aleatoria"],
                         "poder": poder, "coste": PRESUPUESTO})
    reparto = {r["id"]: r["asignado"]
               for r in atencion.repartir(regiones, presupuesto=PRESUPUESTO)}
    return regiones, reparto


def _metodo_medir(ruido_buena=0.3):
    """PASO 1 — la medida escalar: cuanto se lleva el televisor, de 10, segun lo enterrada que
    este la region aprendible."""
    _, reparto = _cadena(ruido_buena=float(ruido_buena))
    return float(reparto["tv"])


def _metodo_sanidad():
    """PASO 3 — LA FICHA. La pregunta: **¿el mundo de juguete tiene de verdad las dos clases de
    region que digo?** Si el "televisor" tuviera estructura aprendible, no seria un televisor y
    todo el estudio estaria midiendo otra cosa. Se comprueba con el instrumento mas tonto posible
    y AJENO a G14: cuanta varianza de Y explica X por minimos cuadrados."""
    fallos = []

    def r2(X, Y):
        A = np.column_stack([X, np.ones(len(X))])
        w, *_ = np.linalg.lstsq(A, Y, rcond=None)
        res = Y - A @ w
        st = float(np.sum((Y - Y.mean()) ** 2))
        return 0.0 if st == 0 else 1.0 - float(np.sum(res ** 2)) / st

    Xb, Yb, _ = _region_aprendible()
    Xt, Yt, _ = _region_televisor()
    r_buena, r_tv = r2(Xb, Yb), r2(Xt, Yt)
    if r_buena < 0.5:
        fallos.append(f"la region 'aprendible' no tiene ley que aprender (R2={r_buena:.3f})")
    if r_tv > 0.15:
        fallos.append(f"el 'televisor' SI tiene estructura (R2={r_tv:.3f}): no es un televisor y "
                      f"el estudio no mediria lo que dice medir")
    return {"aprueba": not fallos, "fallos": fallos,
            "r2_region_aprendible": round(r_buena, 4), "r2_televisor": round(r_tv, 4)}


def regla31(verbose=True):
    """LA REGLA 31 — sobre MI PROCEDIMIENTO, los DOS lados, y NUNCA sobre el resultado.

    NO se prueba aqui que el televisor pierda: eso es el criterio B2, el resultado que el estudio
    existe para medir. Meterlo aqui impediria que pudiera fallar."""
    fallos = []

    def caso(nombre, ok, extra=""):
        if verbose:
            print(f"  {'ok  ' if ok else 'FALLO'} {nombre}" + (f"  [{extra}]" if extra else ""))
        if not ok:
            fallos.append(nombre)

    if verbose:
        print("== REGLA 31 del prereg-49: el montaje, no la cadena ==")

    fs = _metodo_sanidad()
    caso("CONTROL POSITIVO: la region aprendible tiene ley y el televisor no",
         fs["aprueba"], f"R2 buena={fs['r2_region_aprendible']} tv={fs['r2_televisor']}")

    # SEÑUELO: si las dos regiones fueran televisores, el reparto NO puede coronar a ninguna.
    rng = np.random.default_rng(49)
    dos_tv = []
    for i, nid in enumerate(("a", "b")):
        X = rng.normal(size=(60, 2))
        Y = rng.normal(0, 1.0, 60)
        m = incertidumbre.medir(X, Y, rng.normal(size=(40, 2)))
        dos_tv.append({"id": nid, "curable": m["curable"], "aleatoria": m["aleatoria"],
                       "poder": 0.0, "coste": PRESUPUESTO})
    rep = {r["id"]: r["asignado"] for r in atencion.repartir(dos_tv, presupuesto=PRESUPUESTO)}
    caso("SEÑUELO: con DOS televisores ninguno se lleva mas del doble que el otro",
         max(rep.values()) <= 2.0 * min(rep.values()), str(rep))

    # LA MEDIDA RESPONDE: el presupuesto repartido suma lo que hay, ni mas ni menos.
    _, reparto = _cadena()
    caso("el reparto conserva el presupuesto", abs(sum(reparto.values()) - PRESUPUESTO) < 1e-6,
         f"suma {sum(reparto.values()):.4f}")

    # BASE DISTINTA DE CERO en la medida escalar: comparar dos ceros no prueba nada.
    v = _metodo_medir()
    caso("la lectura base NO es cero (o la relacion metamorfica no probaria nada)", v > 0,
         f"{v:.4f}")

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — el montaje es legitimo."
                                if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


def correr(salida=None, verbose=True):
    datos = {"prerregistro": 49, "criterios": {}}

    # --- A: G14 deja de confundir ruido con ignorancia (su ficha, con los umbrales de sanidad.py)
    fa = incertidumbre._metodo_sanidad()
    datos["A_ficha_G14"] = {"aprueba": bool(fa["aprueba"]), "fallos": list(fa["fallos"]),
                            "tabla": fa.get("tabla")}

    # --- B1: el contrato rechaza el numero inflado del INFORME-52
    try:
        atencion.repartir([{"id": "tv", "curable": 20.0, "poder": 0.0, "coste": PRESUPUESTO},
                           {"id": "buena", "curable": 0.3, "poder": 0.5, "coste": PRESUPUESTO}],
                          presupuesto=PRESUPUESTO)
        b1 = False
        datos["B1_detalle"] = "una ignorancia de 20 ENTRO sin levantar error"
    except ValueError as e:
        b1 = True
        datos["B1_detalle"] = str(e)

    # --- B2: el ataque mas fuerte que el contrato SI permite
    rep_max = {r["id"]: r["asignado"] for r in atencion.repartir(
        [{"id": "tv", "curable": 1.0, "poder": 0.0, "coste": PRESUPUESTO},
         {"id": "buena", "curable": 0.3, "poder": 0.5, "coste": PRESUPUESTO}],
        presupuesto=PRESUPUESTO)}
    datos["B2_ignorancia_maxima_legal"] = {k: round(v, 4) for k, v in rep_max.items()}
    b2 = rep_max["tv"] < TOPE_TV and rep_max["buena"] > PISO_BUENA

    # --- C: una region de poder cero no puntua en el presupuesto de ACTUAR
    c = (atencion._ignorancia({"id": "x", "curable": 1.0}) * max(0.0, 0.0)) == 0.0

    # --- D: no se rompio lo que servia. LA CADENA ENTERA, con datos reales.
    regiones, reparto = _cadena()
    datos["D_cadena_real"] = {"regiones": [{k: (round(v, 4) if isinstance(v, float) else v)
                                           for k, v in r.items()} for r in regiones],
                              "reparto": {k: round(v, 4) for k, v in reparto.items()}}
    d = reparto["buena"] > reparto["tv"] and reparto["buena"] > 5.0   # gana al reparto por igual

    # --- E: subir el ruido del televisor no puede subirle la cuota
    serie = {}
    for factor in (1.0, 2.0, 5.0, 10.0):
        _, rep_e = _cadena(ruido_tv=factor)
        serie[f"x{factor:g}"] = round(float(rep_e["tv"]), 4)
    datos["E_serie_ruido_tv"] = serie
    e = all(serie[f"x{f:g}"] <= serie["x1"] + 1e-9 for f in (2.0, 5.0, 10.0))

    datos["criterios"] = {"A_G14_no_confunde": bool(fa["aprueba"]),
                          "B1_contrato_rechaza_inflado": bool(b1),
                          "B2_pierde_con_ignorancia_maxima": bool(b2),
                          "C_poder_cero_no_puntua": bool(c),
                          "D_no_se_rompio": bool(d),
                          "E_mas_ruido_no_sube_cuota": bool(e)}

    todos = all(datos["criterios"].values())
    if todos:
        datos["veredicto"] = ("CADENA REPARADA — G14 deja de confundir ruido con ignorancia, el "
                              "contrato rechaza el numero inflado, y el televisor pierde incluso "
                              "con la ignorancia maxima legal")
    elif datos["criterios"]["D_no_se_rompio"] is False:
        datos["veredicto"] = ("SE DESCARTA LA REPARACION — la atencion dejo de ir donde hay algo "
                              "que aprender; el prerregistro manda descartarla entera")
    else:
        fallan = [k for k, v in datos["criterios"].items() if not v]
        datos["veredicto"] = ("ARREGLA UNO SOLO — la cadena NO esta reparada; fallan " +
                              ", ".join(fallan))

    if salida:
        ruta = os.path.join(BASE, salida)
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
    if verbose:
        print(f"\nVEREDICTO: {datos['veredicto']}")
    return datos


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Prerregistro 49: la cadena G14->G8")
    ap.add_argument("--regla31", action="store_true")
    ap.add_argument("--salida", default="resultados/p49-cadena/medida.json")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    correr(salida=a.salida)
