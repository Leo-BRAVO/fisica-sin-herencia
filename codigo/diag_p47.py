# diag_p47.py — DIAGNOSTICO de por que sindy4 calla en la caida con roce (INFORME-58 §5).
#
# ESTO NO ES UN ESTUDIO Y NO PRODUCE EVIDENCIA DE NINGUN CRITERIO. El prerregistro-47 ya corrio,
# sus cuatro criterios ya estan respondidos en resultados/p47-arreglo/medida.json, y nada de aqui
# los toca. Esto existe por una razon distinta: el INFORME-58 explicaba el fallo con cifras
# —condiciones de matriz, recorrido de la coordenada, margenes fuera de muestra— y EL AUDITOR DE
# ACTAS lo reprobo porque esas cifras no estaban en ningun archivo. Tenia razon: es exactamente el
# mal del INFORME-48, publicar numeros medidos a mano que solo existen en mi cabeza. Aqui se
# calculan, se guardan y quedan auditables.
#
# No pasa por LA PUERTA a proposito: la puerta sella los modulos que producen datos de estudio, y
# esto no lo es. Lo que si hace es correr sobre el modulo YA SELLADO sin tocarlo.
#
# Uso: python diag_p47.py [--salida resultados/p47-arreglo/diagnostico.json]

import os
import sys
import json
import argparse

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sindy3                                                               # noqa: E402
import sindy4                                                               # noqa: E402
import escala                                                               # noqa: E402
import arreglo_motor                                                        # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEMILLA = arreglo_motor.SEMILLAS[0]          # la primera del estudio, a escala x1


def diagnosticar():
    out = {"que_es": ("diagnostico del INFORME-58 §5, NO evidencia de ningun criterio del "
                      "prerregistro-47"),
           "semilla": int(SEMILLA), "escala": 1.0, "sistemas": {}}
    for sis in ("oscilador", "caida_con_roce"):
        x = escala.SISTEMAS[sis](semilla=SEMILLA)
        ventana = max(20, len(x) // 25)
        A, b = sindy3._sistema_debil(x, escala.DT, ventana, max(1, ventana // 4))
        ea, eb = sindy4._escalas(A, b)
        A_s, b_s = A / ea, b / eb
        cp = sindy4._cp(A_s, b_s, 200, 28)
        W_s = sindy4._ols(A_s, b_s)
        soporte = (cp >= sindy4.PISO_CP) & (np.abs(W_s) >= sindy4.PISO_PESO)
        corte = max(3, int(len(A) * sindy4.FRACCION_AJUSTE))
        gana, margenes = sindy4._gana_a_la_linea_base(A, b, soporte, corte)
        out["sistemas"][sis] = {
            "condicion_matriz": round(float(np.linalg.cond(A)), 1),
            "recorrido_x": [round(float(x[:, 0].min()), 2), round(float(x[:, 0].max()), 2)],
            "recorrido_v": [round(float(x[:, 1].min()), 2), round(float(x[:, 1].max()), 2)],
            "soporte": {f"d{v}/dt": [sindy3.NOMBRES[i] for i in range(len(sindy3.NOMBRES))
                                     if soporte[i, j]] for j, v in enumerate(["x", "v"])},
            "cp": {f"d{v}/dt": {sindy3.NOMBRES[i]: round(float(cp[i, j]), 1)
                                for i in range(len(sindy3.NOMBRES))}
                   for j, v in enumerate(["x", "v"])},
            "margen_fuera_de_muestra": margenes,
            "gana_a_la_linea_base": bool(gana),
            "con_tope_1e12_declara_ley": sindy4.descubrir(x, dt=escala.DT,
                                                          tope_condicion=1e12) is not None,
            "declara_ley": sindy4.descubrir(x, dt=escala.DT) is not None,
        }
    out["tope_condicion_del_motor"] = sindy4.TOPE_CONDICION
    out["piso_cp_del_motor"] = sindy4.PISO_CP
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Diagnostico del INFORME-58 (no es un estudio)")
    ap.add_argument("--salida", default="resultados/p47-arreglo/diagnostico.json")
    a = ap.parse_args()
    d = diagnosticar()
    ruta = os.path.join(BASE, a.salida)
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
    print(json.dumps(d["sistemas"], ensure_ascii=False, indent=1))
