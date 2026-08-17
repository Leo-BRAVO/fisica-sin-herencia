# contacto2.py — EL CONTACTO OTRA VEZ, CON POTENCIA (prerregistro-61, 17-ago-2026).
#
# POR QUE HAY UN SEGUNDO INTENTO: el prerregistro-60 no fallo por la politica, fallo por MI
# CRITERIO. Congele "gana en 4 de 5" y el azar pasa eso el 18.75% de las veces; el nulo lo paso y
# anulo el estudio entero (INFORME-71, error nº26 del catalogo).
#
# ESTO NO ES SUBIR LAS SEMILLAS HASTA QUE SALGA. El estudio 60 esta publicado y no se toca. Lo que
# cambia es el DISEÑO, y el numero sale de una binomial escrita ANTES:
#     n=5  k=4  -> 18.8%   (el del 60)      n=10 k=8  -> 5.5%   (no basta)
#     n=5  k=5  ->  3.1%                    n=10 k=9  -> 1.1%
#     n=15 k=12 ->  1.8%   <- el elegido
# Se elige 12 de 15 y no 9 de 10 porque con 15 semillas hay mas capacidad de ver un efecto REAL, y
# exigir 9 de 10 castiga a un efecto moderado tanto como al azar.
#
# QUE SE IMPORTA Y NO SE COPIA: TODO —el mundo, las tres politicas, el medidor y los dos guardianes
# de la Regla 27— viene de `politica_contacto`, que esta SELLADO. Aqui solo cambian las semillas y
# el criterio de conteo. Editar aquel modulo mataria su sello y dejaria irreproducible el
# INFORME-71.
#
# Uso: python contacto2.py [--regla31] [--salida resultados/p61-contacto2/medida.json]

import os
import sys
import json
import math
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "codigo"))

import mundo                                                                # noqa: E402
import politica_contacto as PC                                              # noqa: E402

# El sujeto sigue siendo la politica intrinseca, heredado del prerregistro-60. La Regla 31 de este
# modulo examina LO UNICO QUE ES SUYO: el criterio de conteo.
SUJETO = ("POLITICA",)

# ------------------------------------------------------------------ EL PRERREGISTRO, EN CODIGO
SEMILLAS = tuple(range(1, 16))     # 15, derivadas de la binomial y no de mi gusto
MINIMAS_A_FAVOR = 12               # P(X >= 12 | 15, 0.5) = 0.0176
TECHO_DEL_AZAR = 0.05              # por encima de esto un criterio de conteo no esta listo

METODO = {
    "prerregistro": 61,
    "tipo_de_medida": "mixta",   # la fraccion es continua; el criterio cuenta semillas por umbral
    "que_mide": ("en cuantas semillas la politica movida por su propio error de prediccion acaba "
                 "mas cerca del objeto que el balbuceo, con un criterio de conteo cuya "
                 "probabilidad bajo el azar esta calculada y escrita antes de correr"),
    "comparten_datos": {
        "hay": False,
        "porque": "cada semilla corre su propio mundo de principio a fin; nada se reutiliza entre "
                  "semillas ni entre politicas",
    },
    "linea_base": ("el balbuceo: elegir al azar entre los mismos candidatos, heredado del "
                   "prerregistro-60. Y ADEMAS, sobre el criterio mismo, la moneda justa: un "
                   "criterio de conteo que una moneda pasa mas del 5% de las veces no esta listo "
                   "para congelarse, y esa es la leccion que costo el estudio anterior"),
    "formulas": [
        {"base": {"exigidas": 8.0}, "parametro": "exigidas", "factor": 1.5, "esperado": "baja",
         "porque": "la probabilidad de que el azar pase un criterio de 'k de n' es la cola de una "
                   "binomial: subir k con n fijo solo puede BAJARLA, porque se suman menos "
                   "terminos de la misma suma. Es aritmetica exacta, no intuicion. Base 8.0 y NO "
                   "0.0: multiplicar cero por uno y medio sigue siendo cero"},
    ],
}


def probabilidad_del_azar(k=MINIMAS_A_FAVOR, n=len(SEMILLAS)):
    """P(X >= k | n, p=0.5): lo que una moneda justa saca bajo este criterio."""
    return sum(math.comb(n, i) for i in range(int(k), int(n) + 1)) / float(2 ** int(n))


def _cuenta(filas, cual):
    """En cuantas semillas `cual` supera al balbuceo."""
    return sum(1 for f in filas if f[cual] > f["balbuceo"])


def aprueba_el_conteo(victorias, exigidas=MINIMAS_A_FAVOR):
    """LO UNICO QUE ES PROPIO DE ESTE MODULO: la regla de conteo. Se examina por los dos lados."""
    return int(victorias) >= int(exigidas)


# ---------------------------------------------------------------- la ficha y las autopruebas
def _metodo_medir(exigidas=8.0):
    """La medida que la relacion metamorfica mueve: la probabilidad del azar bajo el criterio."""
    return float(probabilidad_del_azar(k=int(round(exigidas)), n=len(SEMILLAS)))


def _metodo_sanidad():
    """PASO 3 — LA FICHA. La pregunta: **¿el criterio que congelo aguanta a una moneda?** Es
    exactamente la pregunta que no me hice en el prerregistro-60 y que costo el estudio entero."""
    fallos = []
    if probabilidad_del_azar() > TECHO_DEL_AZAR:
        fallos.append(f"el criterio congelado lo pasa el azar el {probabilidad_del_azar():.1%} de "
                      f"las veces: por encima del techo, no esta listo")
    if probabilidad_del_azar(k=4, n=5) <= TECHO_DEL_AZAR:
        fallos.append("la cuenta del azar dice que '4 de 5' era aceptable: la aritmetica esta mal")
    if not SEMILLAS:
        fallos.append("no hay ni una semilla que correr: el estudio aprobaria sobre nada")
    if MINIMAS_A_FAVOR > len(SEMILLAS):
        fallos.append("se exigen mas victorias que semillas: el criterio no puede aprobar nunca")
    return {"aprueba": not fallos, "fallos": fallos,
            "probabilidad_del_azar": probabilidad_del_azar(), "semillas": len(SEMILLAS)}


def regla31(verbose=True):
    fallos = []

    def caso(nombre, ok, extra=""):
        if verbose:
            print(f"  {'ok   ' if ok else 'FALLO'} {nombre}{('  -> ' + extra) if extra else ''}")
        if not ok:
            fallos.append(nombre)

    if verbose:
        print("REGLA 31 de contacto2 — sobre LO UNICO QUE ES MIO: el criterio de conteo\n")

    caso("el criterio APRUEBA con las victorias justas", aprueba_el_conteo(MINIMAS_A_FAVOR))
    caso("el criterio REPRUEBA con una victoria menos",
         not aprueba_el_conteo(MINIMAS_A_FAVOR - 1))

    p = probabilidad_del_azar()
    caso("el azar NO pasa el criterio congelado", p <= TECHO_DEL_AZAR, f"P={p:.4f}")
    caso("el azar SI pasaba el criterio del prerregistro-60",
         probabilidad_del_azar(k=4, n=5) > TECHO_DEL_AZAR,
         f"P={probabilidad_del_azar(k=4, n=5):.4f}")

    f = METODO["formulas"][0]
    base = f["base"]["exigidas"]
    antes, despues = _metodo_medir(base), _metodo_medir(base * f["factor"])
    caso(f"metamorfica: exigir mas victorias BAJA la probabilidad del azar (base {base}, x{f['factor']})",
         despues < antes, f"{antes:.4f} -> {despues:.4f}")

    caso("el conteo mira al balbuceo y no a otra cosa",
         _cuenta([{"balbuceo": 0.1, "x": 0.2}, {"balbuceo": 0.3, "x": 0.2}], "x") == 1)

    caso("el cortafuegos heredado: la señal declarada pasa el guardian",
         mundo.guardian_de_recompensa(list(PC.TERMINOS_DE_LA_SEÑAL)) == [])
    caso("el cortafuegos heredado: una señal que pagara por tocar SERIA RECHAZADA",
         len(mundo.guardian_de_recompensa(["error_de_prediccion_propio", "hubo_contacto"])) == 1)

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — el criterio distingue y el azar no lo pasa"
                                if not fallos else f"REPRUEBA en {len(fallos)}: {fallos}"))
    return 0 if not fallos else 1


# ------------------------------------------------------------------------------- la corrida
def correr(salida=None, verbose=True):
    filas, sordas = [], []
    for s in SEMILLAS:
        fila = {"semilla": int(s)}
        for pol in ("balbuceo", "intrinseca", "barajada"):
            fila[pol] = PC.corrida(s, politica=pol)["fraccion_de_contacto"]
        filas.append(fila)
        sordas.append({"semilla": int(s),
                       "balbuceo": PC.corrida(s, "balbuceo", sordo=True)["fraccion_de_contacto"],
                       "intrinseca": PC.corrida(s, "intrinseca", sordo=True)["fraccion_de_contacto"]})
        if verbose:
            print(f"  semilla {s:2d}: balbuceo {fila['balbuceo']:.4f} · intrinseca "
                  f"{fila['intrinseca']:.4f} · barajada {fila['barajada']:.4f}")

    gana_intrinseca = _cuenta(filas, "intrinseca")
    gana_barajada = _cuenta(filas, "barajada")
    gana_sorda = _cuenta(sordas, "intrinseca")
    diferencia = float(np.median([f["intrinseca"] - f["balbuceo"] for f in filas]))

    a = (mundo.guardian_de_recompensa(list(PC.TERMINOS_DE_LA_SEÑAL)) == []
         and mundo.guardian_de_etiquetas({f"c{i}": 0.0 for i in range(9)}) == [])
    e = all(PC.corrida(s, politica=pol, pasos=150, radio=0.0)["fraccion_de_contacto"] == 0.0
            for s in SEMILLAS[:2] for pol in ("balbuceo", "intrinseca", "barajada"))

    datos = {
        "prerregistro": 61,
        "semillas": len(SEMILLAS),
        "exigidas": MINIMAS_A_FAVOR,
        "probabilidad_del_azar": probabilidad_del_azar(),
        "semillas_en_que_gana_la_intrinseca": gana_intrinseca,
        "semillas_en_que_gana_la_barajada": gana_barajada,
        "semillas_en_que_gana_la_intrinseca_en_el_mundo_sordo": gana_sorda,
        "diferencia_mediana_informativa": diferencia,
        "filas": filas,
        "mundo_sordo": sordas,
        "criterios": {
            "A_el_cortafuegos_aguanta": bool(a),
            "B_en_el_mundo_sordo_la_intrinseca_no_busca": not aprueba_el_conteo(gana_sorda),
            "C_la_intrinseca_busca_sola": aprueba_el_conteo(gana_intrinseca),
            "D_el_nulo_no_gana": not aprueba_el_conteo(gana_barajada),
            "E_no_se_puede_inventar_contacto": bool(e),
        },
    }
    c = datos["criterios"]
    if not c["A_el_cortafuegos_aguanta"]:
        datos["veredicto"] = ("SE DESCARTA EL ESTUDIO — el cortafuegos de la Regla 27 tiene una "
                              "fuga, y el fallo es NUESTRO no suyo")
    elif not c["E_no_se_puede_inventar_contacto"]:
        datos["veredicto"] = "SE DESCARTA EL MEDIDOR — marca contacto donde no puede haberlo"
    elif not c["B_en_el_mundo_sordo_la_intrinseca_no_busca"]:
        datos["veredicto"] = ("ANULADO POR EL MUNDO SORDO — la intrinseca tambien se acerca donde "
                              "el contacto NO HACE NADA")
    elif not c["D_el_nulo_no_gana"]:
        datos["veredicto"] = ("ANULADO POR EL NULO — la barajada tambien le gana al balbuceo, y "
                              "esta vez con un criterio que el azar solo pasa el "
                              f"{probabilidad_del_azar():.1%} de las veces: el problema no es la "
                              "potencia sino el nulo")
    elif c["C_la_intrinseca_busca_sola"]:
        datos["veredicto"] = (f"LA CURIOSIDAD SOLA BASTA PARA BUSCAR EL CONTACTO — gana en "
                              f"{gana_intrinseca} de {len(SEMILLAS)} sin que nadie le pague por "
                              f"tocar, con un criterio que el azar pasa el "
                              f"{probabilidad_del_azar():.1%} de las veces")
    else:
        datos["veredicto"] = (f"LA CURIOSIDAD SOLA NO BASTA PARA BUSCAR EL CONTACTO — gana en "
                              f"{gana_intrinseca} de {len(SEMILLAS)} y hacian falta "
                              f"{MINIMAS_A_FAVOR}. Esta vez el diseño SI tenia potencia, asi que "
                              f"el item queda cerrado con una respuesta")

    if salida:
        ruta = os.path.join(BASE, salida)
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
    if verbose:
        print(f"\nintrinseca gana {gana_intrinseca}/{len(SEMILLAS)} · barajada "
              f"{gana_barajada}/{len(SEMILLAS)} · mundo sordo {gana_sorda}/{len(SEMILLAS)}")
        print(f"diferencia mediana (informativa): {diferencia:+.5f} · el azar pasa el criterio el "
              f"{probabilidad_del_azar():.2%}")
        for k, v in c.items():
            print(f"  {'ok   ' if v else 'FALLO'} {k}")
        print(f"\nVEREDICTO: {datos['veredicto']}")
    return datos


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Prerregistro 61: el contacto con potencia calculada")
    ap.add_argument("--regla31", action="store_true")
    ap.add_argument("--salida", default="resultados/p61-contacto2/medida.json")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    correr(salida=a.salida)
