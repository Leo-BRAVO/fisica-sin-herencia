# unico_apto.py — PRERREGISTRO 42: ¿el escalon 1 debe aislar UN canal, o puede declarar varios?
#
# ORIGEN. El prereg-35 salio PARCIAL (INFORME-42): pedia `altura` como UNICO apto y en 2 de 5
# mundos `contacto` tambien paso — por 0.016 sobre un piso de 0.30. La pregunta "¿y si exigir
# unicidad era la exigencia equivocada?" se me ocurrio DESPUES de ver eso, que es la definicion de
# una racionalizacion a posteriori. Por eso espero la firma del director (la dio el 10-ago) y por
# eso este modulo NO PUEDE tocar las semillas 1..5: quedaron quemadas al generar la hipotesis.
#
# LO QUE ESTE MODULO NO HACE, y es lo mas importante: no cambia `soporte.py`. No mueve el piso, no
# toca el criterio, no reinterpreta nada. Solo CORRE el instrumento tal cual esta sobre mundos que
# nadie ha visto y cuenta lo que sale. Si tocara el instrumento, estaria eligiendo el resultado.
#
# Uso: python unico_apto.py [--regla31] [--semillas 71 73 79 83 89]

import os
import sys
import json
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "codigo"))

import soporte                                                              # noqa: E402

# ------------------------------------------------------------------ EL PRERREGISTRO, EN CODIGO
# Estas constantes son el prerregistro-42 hecho numeros. Cambiarlas despues de ver los datos es
# exactamente lo que el director prohibio, y lo unico que su enmienda de la Regla 15 nunca delego.
SEMILLAS_NUEVAS = (71, 73, 79, 83, 89)   # declaradas en el prerregistro ANTES de tocarlas
CANALES = 7                              # art0..2, altura, contacto, vel_z, ruido
LINEA_BASE_TONTA = 1.0 / CANALES         # elegir un canal al azar: 0.1429
OBJETIVO = "altura"
MARGEN_H_VARIOS = 0.10                   # 6x el 0.016 que provoco el PARCIAL
MINIMOS_H_AISLAR = 4                     # de 5
MINIMOS_H_VARIOS_MARGEN = 4              # de 5
MINIMOS_H_VARIOS_ELEGIDO = 5             # de 5, sin excepcion

METODO = {
    "prerregistro": 42,
    # UMBRAL: el instrumento decide "apto / no apto" cruzando PISO_LEGALIDAD=0.30. La cantidad
    # subyacente (autopredictibilidad) es continua, pero lo que el estudio juzga es la DECISION.
    "tipo_de_medida": "umbral",
    "que_mide": "que canal declara el escalon 1 como primer no-yo, y con cuanto margen",
    "comparten_datos": {
        "hay": True,
        "porque": "las dos hipotesis se juzgan sobre LA MISMA corrida de cada mundo, a proposito: "
                  "correr dos veces y quedarse con la corrida que favorece a una seria elegir el "
                  "resultado. Compartir datos aqui es lo correcto; lo que estaria mal es no "
                  "declararlo.",
    },
    "linea_base": ("elegir canal al azar entre 7 = 0.1429. Todo puntaje se reporta como GANANCIA "
                   "sobre ella (Regla 11, fusionada con la 12 el 10-ago-2026)"),
    # RELACIONES METAMORFICAS: no se puede saber cual es la autopredictibilidad "correcta" de un
    # canal —nadie la conoce— pero SI se sabe COMO tiene que cambiar cuando se cambia el mundo.
    "formulas": [
        {"base": {"suavizado": 4.0, "ruido": 0.05}, "parametro": "suavizado", "factor": 8.0,
         "esperado": "sube",
         "porque": "una señal mas suave es mas predecible desde su propio pasado. Se declara como "
                   "DESIGUALDAD y no como proporcion porque el R2 autopredictivo de una señal "
                   "suavizada no tiene forma cerrada: poner un factor exacto seria inventarselo"},
        {"base": {"suavizado": 4.0, "ruido": 0.05}, "parametro": "ruido", "factor": 20.0,
         "esperado": "baja",
         "porque": "mas ruido blanco encima = menos ley propia que leer: la autopredictibilidad "
                   "debe caer. Si NO cayera, el instrumento estaria midiendo la forma del canal y "
                   "no su regularidad"},
    ],
}


def _de_un_mundo(semilla, pasos=900):
    """Corre el instrumento TAL CUAL en un mundo nuevo y devuelve lo que declaro."""
    mundo = soporte.mundo_variable(semilla)
    com, can, nom, cortes = soporte.escena("cae", semilla=semilla, pasos=pasos, mundo=mundo)
    r = soporte.escalon1(com, can, nom, cortes=cortes)
    auto = {f["canal"]: f["autopredictible"] for f in r["detalle"]}
    # 10-ago-2026 — SE GUARDA TAMBIEN LA OBEDIENCIA, y el motivo es una falta mia. El INFORME-48
    # publico que `art1` tenia obediencia 0.0297 contra un techo de 0.05, y ese numero lo habia
    # medido A MANO en una sesion: no estaba en ningun archivo. `actas.py` —el auditor de actas,
    # escrito ese mismo dia— lo caza al primer intento: "1 cifra de sus tablas NO aparece en los
    # datos citados". Tenia razon. Un numero que solo existe en mi cabeza no es evidencia, por
    # cierto que sea. Ahora el detalle entero viaja al JSON y el acta puede apuntarle.
    obed = {f["canal"]: f["obediencia_neta"] for f in r["detalle"]}
    legal = {f["canal"]: bool(f["legal"]) for f in r["detalle"]}
    no_mio = {f["canal"]: bool(f["no_mio"]) for f in r["detalle"]}
    aptos = r.get("candidatos_aptos") or []
    ajenos = [a for a in aptos if a != OBJETIVO]
    margen = (auto.get(OBJETIVO, 0.0) - max([auto[a] for a in ajenos])) if ajenos else None
    return {"semilla": int(semilla), "mundo": {k: round(float(v), 3) for k, v in mundo.items()},
            "aptos": aptos, "elegido": r.get("candidato"),
            "auto_objetivo": auto.get(OBJETIVO), "auto_por_canal": auto,
            "obediencia_neta_por_canal": obed, "legal_por_canal": legal,
            "no_mio_por_canal": no_mio,
            "margen_sobre_el_mejor_ajeno": (round(margen, 4) if margen is not None else None)}


def correr(semillas=SEMILLAS_NUEVAS, pasos=900, verbose=True):
    filas = [_de_un_mundo(s, pasos=pasos) for s in semillas]
    n = len(filas)

    # H-AISLAR: exactamente un apto y que sea el objetivo
    aislar = sum(1 for f in filas if f["aptos"] == [OBJETIVO])
    gana_aislar = aislar >= MINIMOS_H_AISLAR

    # H-VARIOS: elegido siempre, y margen suficiente en la mayoria
    elegido = sum(1 for f in filas if f["elegido"] == OBJETIVO)
    # un mundo SIN ajenos aptos cuenta a favor del margen: no hay rival que descontar
    con_margen = sum(1 for f in filas
                     if f["margen_sobre_el_mejor_ajeno"] is None
                     or f["margen_sobre_el_mejor_ajeno"] >= MARGEN_H_VARIOS)
    gana_varios = (elegido >= MINIMOS_H_VARIOS_ELEGIDO
                   and con_margen >= MINIMOS_H_VARIOS_MARGEN)

    ganancia = elegido / float(n) - LINEA_BASE_TONTA

    if gana_aislar:                 # regla 3 del prerregistro: si ganan las dos, gana la vieja
        veredicto = "H-AISLAR"
    elif gana_varios:
        veredicto = "H-VARIOS"
    else:
        veredicto = "NO CONCLUYENTE"

    r = {"semillas": list(semillas), "filas": filas,
         "aciertos_de_altura": elegido, "de": n,
         "linea_base_tonta": round(LINEA_BASE_TONTA, 4),
         "ganancia_sobre_la_linea_base": round(ganancia, 4),
         "mundos_con_un_solo_apto": aislar,
         "mundos_con_margen_suficiente": con_margen,
         "gana_h_aislar": bool(gana_aislar), "gana_h_varios": bool(gana_varios),
         "veredicto": veredicto}
    if verbose:
        print(f"=== PRERREGISTRO 42 — semillas NUEVAS {list(semillas)} ===")
        print(f"{'s':>4} {'aptos':<26} {'elegido':<9} {'auto(altura)':>12} {'margen':>8}")
        for f in filas:
            m = "—" if f["margen_sobre_el_mejor_ajeno"] is None else f"{f['margen_sobre_el_mejor_ajeno']:.4f}"
            print(f"{f['semilla']:>4} {str(f['aptos']):<26} {str(f['elegido']):<9} "
                  f"{f['auto_objetivo']:>12.4f} {m:>8}")
        print(f"\naltura elegida {elegido}/{n} | linea base tonta {LINEA_BASE_TONTA:.4f} "
              f"| GANANCIA {ganancia:+.4f}")
        print(f"un solo apto: {aislar}/{n} (pide {MINIMOS_H_AISLAR})   "
              f"margen>={MARGEN_H_VARIOS}: {con_margen}/{n} (pide {MINIMOS_H_VARIOS_MARGEN})")
        print(f"VEREDICTO: {veredicto}")
    return r


# ------------------------------------------------------------------ REGLA 31, LOS DOS LADOS
def regla31(verbose=True):
    """Los dos lados declarados en el prerregistro, mas el señuelo que puede anular el estudio."""
    fallos = []

    def caso(nombre, ok, extra=""):
        print(f"  {'ok  ' if ok else 'FALLO'} {nombre} {extra}")
        if not ok:
            fallos.append(nombre)

    if verbose:
        print("== REGLA 31 del prereg-42: debe fallar donde no hay nada Y aprobar donde si ==")

    s = 71
    mundo = soporte.mundo_variable(s)
    com, can, nom, cortes = soporte.escena("cae", semilla=s, pasos=600, mundo=mundo)

    # LADO NEGATIVO — canales barajados EN EL TIEMPO: ningun canal conserva su ley propia, asi que
    # ninguno puede ser "legal". Si aun asi aparece un apto, el instrumento inventa no-yos.
    rng = np.random.default_rng(1234)
    revuelto = can.copy()
    for j in range(revuelto.shape[1]):
        revuelto[:, j] = revuelto[rng.permutation(revuelto.shape[0]), j]
    r_neg = soporte.escalon1(com, revuelto, nom, cortes=cortes)
    caso("con los canales barajados en el tiempo NO aparece ningun apto",
         not (r_neg.get("candidatos_aptos") or []), str(r_neg.get("candidatos_aptos")))

    # LADO POSITIVO — el mundo tal cual: el objetivo DEBE aparecer entre los aptos.
    r_pos = soporte.escalon1(com, can, nom, cortes=cortes)
    caso("en el mundo real el objetivo aparece entre los aptos",
         OBJETIVO in (r_pos.get("candidatos_aptos") or []), str(r_pos.get("candidatos_aptos")))

    # EL SEÑUELO — el canal de ruido puro NUNCA puede ser el elegido. Si lo fuera, el criterio
    # premia "no me obedece" a secas y el estudio entero se declara NULO, gane quien gane.
    caso("el canal de RUIDO nunca es el elegido (si lo fuera, el estudio es NULO)",
         r_pos.get("candidato") != "ruido", str(r_pos.get("candidato")))

    # LA LINEA BASE NO SE PUEDE MOVER: 7 canales, 1/7. Congelada aqui para que un cambio de
    # canales en soporte.py no deje la linea base rancia sin que nadie lo note.
    caso("la linea base tonta coincide con los canales que el instrumento mira de verdad",
         len(nom) == CANALES, f"{len(nom)} canales, la linea base supone {CANALES}")

    if verbose:
        print("REGLA 31: " + ("APRUEBA" if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


def _senal_sintetica(n=600, suavizado=4.0, ruido=0.05, semilla=5):
    """Una señal con regularidad CONTROLADA por nosotros. Sirve para los pasos 1 y 3 de LA PUERTA
    sin pagar el simulador: lo que se examina ahi es la MEDIDA, no el mundo."""
    rng = np.random.default_rng(int(semilla))
    x = rng.normal(size=int(n))
    k = max(1, int(round(suavizado)))
    nucleo = np.ones(k) / k
    x = np.convolve(x, nucleo, mode="same")            # mas suavizado = mas predecible
    return x + rng.normal(0.0, float(ruido), size=int(n))


def _metodo_medir(suavizado=4.0, ruido=0.05):
    """PASO 1 — la medida escalar sobre la que se comprueban las relaciones metamorficas: la
    autopredictibilidad que el instrumento asigna a una señal cuya regularidad controlamos."""
    return float(soporte._r2_autopredictivo(_senal_sintetica(suavizado=suavizado, ruido=ruido)))


def _metodo_sanidad():
    """PASO 3 — LA FICHA. La pregunta que contesta es la unica que importa de un instrumento que
    compara canales: **¿la lectura de cada canal sigue a ESE canal, y no a su vecino?**

    Se fabrican 10 mundos de juguete con 3 canales cada uno, y en cada mundo el suavizado de los
    tres se sortea POR SEPARADO. La verdad conocida es ese suavizado; la lectura es lo que el
    instrumento mide. Si la lectura del canal A subiera cuando lo que cambio fue el canal B, el
    instrumento estaria confundiendo canales — y todo el estudio, que consiste en comparar un
    canal contra otro, quedaria sin sentido. Es el tipo de error que la ficha llama CRUCE.
    """
    import sanidad as S
    rng = np.random.default_rng(3)
    verdad = {"a": [], "b": [], "c": []}
    lect = {"a": [], "b": [], "c": []}
    for i in range(10):
        for nombre in ("a", "b", "c"):
            s = float(rng.uniform(2.0, 20.0))
            verdad[nombre].append(s)
            lect[nombre].append(float(soporte._r2_autopredictivo(
                _senal_sintetica(suavizado=s, ruido=0.05, semilla=100 + i * 7 + ord(nombre)))))
    r = S.correlaciones(lect, verdad)
    return {"aprueba": not r["fallos"], "fallos": r["fallos"]}


def main():
    ap = argparse.ArgumentParser(description="Prerregistro 42 — la clausula 'unico apto'")
    ap.add_argument("--regla31", action="store_true")
    ap.add_argument("--semillas", type=int, nargs="*", default=list(SEMILLAS_NUEVAS))
    ap.add_argument("--pasos", type=int, default=900)
    ap.add_argument("--salida", default=None)
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    if any(s <= 10 for s in a.semillas):
        print("NEGADO: las semillas 1..10 son las QUEMADAS del prereg-35. La hipotesis nacio "
              "mirandolas; volver a usarlas seria examinar con las respuestas delante.")
        sys.exit(2)
    r = correr(a.semillas, pasos=a.pasos)
    if a.salida:
        os.makedirs(os.path.dirname(a.salida) or ".", exist_ok=True)
        json.dump(r, open(a.salida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"escrito: {a.salida}")


if __name__ == "__main__":
    main()
