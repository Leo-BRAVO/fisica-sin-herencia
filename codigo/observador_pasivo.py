# observador_pasivo.py — EL CONTROL QUE PODRIA REFUTARNOS (prerregistro-32, FIRMADO 9-ago-2026).
#
# POR QUE EXISTE (honestidad ofensiva, no defensiva): todo el proyecto apuesta a que la
# ENCARNACION —tener cuerpo, actuar, sentir las consecuencias— es lo que permite descubrir fisica
# sin heredarla. Pero en 2025 Meta publico que la fisica intuitiva (permanencia de objetos,
# consistencia de forma) EMERGE de video PASIVO, sin cuerpo y sin accion. Si eso es cierto para
# la fisica de soporte, entonces buena parte de lo que le atribuimos al cuerpo de Diego no se debe
# al cuerpo. Queremos saberlo NOSOTROS, y antes que un tercero.
#
# EL EXPERIMENTO, en una linea: mismo mundo, misma dieta sensorial, la UNICA diferencia es el
# acceso a las propias ordenes.
#   ENCARNADO      — vive sus episodios y conoce sus comandos (copia eferente disponible).
#   PASIVO-PROPIO  — ve exactamente los mismos episodios, pero sin acceso a los comandos.
#   PASIVO-AJENO   — ve episodios de OTRO agente: ni los causo ni puede tener copia eferente.
#
# Se comparan en dos capacidades de naturaleza distinta:
#   (1) FRONTERA YO/MUNDO — requiere accion por construccion. El encarnado debe ganar; si no
#       ganara ni aqui, la comparacion misma seria ciega (es nuestro control positivo).
#   (2) FISICA DE SOPORTE (escalon 2 y examen VOE del prereg-29) — aprendible mirando. Aqui es
#       donde la literatura predice que el pasivo empata. Si empata, lo escribimos.
#
# Regla 31: (a) el encarnado gana la capacidad que exige accion; (b) dos encarnados identicos
# empatan en todo (la comparacion no fabrica ventajas); (c) una ventaja PLANTADA se detecta.

import os
import sys
import json
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "codigo"))

from soporte import (escena, escalon2, examen_voe, _r2_autopredictivo, _ganancia_comando,
                     PISO_LEGALIDAD, TECHO_OBEDIENCIA, PASOS_MINIMOS)

CONDICIONES = ("encarnado", "pasivo_propio", "pasivo_ajeno")


def _dieta(semilla, pasos):
    """Los episodios que UN agente vive. Devuelve lo observable y, aparte, sus ordenes — que solo
    el encarnado podra usar."""
    c1, x1, nom, k1 = escena("cae", semilla=semilla + 1, pasos=pasos)
    c2, x2, _, k2 = escena("apoyado", semilla=semilla + 2, pasos=pasos)
    return {"comandos": [c1, c2], "canales": [x1, x2], "cortes": [k1, k2], "nombres": nom}


def frontera_yo_mundo(dieta, comandos_disponibles, semilla=32, nulos=6):
    """Capacidad 1: ¿puede separar lo suyo de lo demas? Sin comandos NO PUEDE, por construccion —
    y eso es exactamente lo que queremos medir en vez de asumir. Puntaje: cuantos canales quedan
    correctamente clasificados como suyos (obedecen sobre su nulo) usando solo lo disponible."""
    if comandos_disponibles is None:
        return {"puntaje": 0.0, "canales_mios": [],
                "nota": "sin acceso a sus ordenes no hay contingencia posible"}
    nombres = dieta["nombres"]
    mios, detalle = [], []
    rng = np.random.default_rng(semilla)
    for x, u, k in zip(dieta["canales"], comandos_disponibles, dieta["cortes"]):
        for i, n in enumerate(nombres):
            g = _ganancia_comando(x[:, i], u, cortes=k)
            g0 = float(np.mean([_ganancia_comando(x[:, i], u[rng.permutation(len(u))], cortes=k)
                                for _ in range(nulos)]))
            if g - g0 > TECHO_OBEDIENCIA:
                mios.append(n)
            detalle.append({"canal": n, "obediencia_neta": round(max(0.0, g - g0), 4)})
    mios = sorted(set(mios))
    return {"puntaje": float(len(mios)), "canales_mios": mios, "detalle": detalle}


def fisica_de_soporte(dieta, dieta_examen, comandos=None):
    """Capacidad 2: ¿nota que el contacto detiene la caida, y que lo imposible es imposible?

    EL COMANDO ENTRA AQUI SI SE TIENE. Sin esto la comparacion seria TAUTOLOGICA: si las medidas
    de soporte no consultan las ordenes, el encarnado y el pasivo-propio ven exactamente el mismo
    numero por construccion y el "empate" no significa nada. (Hueco propio, cazado el 9-ago-2026
    al leer el primer resultado: diferencia 0.0000 EXACTA — demasiado limpia para ser una
    medicion.) El encarnado aprende su modelo del mundo con la COPIA EFERENTE incluida: predice el
    proximo estado sabiendo tambien lo que acaba de ordenar. Si esa informacion ayuda, se vera."""
    junto = np.vstack(dieta["canales"])
    e2 = escalon2(junto, dieta["nombres"])
    ent = ([np.column_stack([x, u[:len(x)]]) for x, u in zip(dieta["canales"], comandos)]
           if comandos is not None else dieta["canales"])

    def _ex(nombre):
        x = dieta_examen[nombre]
        if comandos is None:
            return x
        # en el examen el encarnado NO actua (son escenas ajenas): su copia eferente es cero.
        # Es la unica lectura honesta — no se le puede dar un comando que no emitio.
        return np.column_stack([x, np.zeros((len(x), comandos[0].shape[1]))])

    v_flota = examen_voe(ent, _ex("cae2"), _ex("flota"))
    v_atrav = examen_voe(ent, _ex("apoyado2"), _ex("atraviesa"))
    nulo = examen_voe(ent, _ex("cae2"), _ex("cae3"))
    return {"escalon2_efecto": e2.get("efecto"), "escalon2_hallado": e2.get("hallado"),
            "voe_flota": v_flota["sorpresa_relativa"],
            "voe_atraviesa": v_atrav["sorpresa_relativa"],
            "voe_nulo_natural": nulo["sorpresa_relativa"],
            "puntaje": float(min(v_flota["sorpresa_relativa"], v_atrav["sorpresa_relativa"]))}


def _examen(semilla, pasos):
    _, x_flo, _, _ = escena("flota", semilla=semilla + 3, pasos=pasos)
    _, x_atr, _, _ = escena("atraviesa", semilla=semilla + 4, pasos=pasos)
    _, x_c2, _, _ = escena("cae", semilla=semilla + 5, pasos=pasos)
    _, x_a2, _, _ = escena("apoyado", semilla=semilla + 6, pasos=pasos)
    _, x_c3, _, _ = escena("cae", semilla=semilla + 7, pasos=pasos)
    return {"flota": x_flo, "atraviesa": x_atr, "cae2": x_c2, "apoyado2": x_a2, "cae3": x_c3}


def comparar(semilla=1, pasos=PASOS_MINIMOS):
    """Las tres condiciones sobre el MISMO mundo. El pasivo-propio ve exactamente los mismos
    episodios que el encarnado: la unica diferencia es el acceso a sus ordenes."""
    dieta = _dieta(100 * semilla, pasos)
    dieta_ajena = _dieta(100 * semilla + 50, pasos)     # episodios de OTRO agente
    examen = _examen(100 * semilla, pasos)
    filas = {}
    for cond in CONDICIONES:
        d = dieta_ajena if cond == "pasivo_ajeno" else dieta
        u = d["comandos"] if cond == "encarnado" else None
        filas[cond] = {"frontera": frontera_yo_mundo(d, u),
                       "soporte": fisica_de_soporte(d, examen, comandos=u)}
    return filas


def veredicto(filas):
    """Lo que se puede afirmar y lo que no. Se escribe SIEMPRE, gane quien gane."""
    enc, pas = filas["encarnado"], filas["pasivo_propio"]
    aje = filas["pasivo_ajeno"]
    gana_frontera = enc["frontera"]["puntaje"] > pas["frontera"]["puntaje"]
    dif_soporte = enc["soporte"]["puntaje"] - pas["soporte"]["puntaje"]
    return {
        "frontera_yo_mundo": ("EL CUERPO APORTA — el pasivo no puede siquiera plantearla"
                              if gana_frontera else
                              "SIN VENTAJA MEDIDA — revisar si la capacidad estaba bien definida"),
        "fisica_de_soporte": ("EL CUERPO APORTA" if dif_soporte > 0.05 else
                              "EMPATE — la fisica de soporte se aprende MIRANDO; el cuerpo no "
                              "aporta aqui, y asi queda escrito"),
        "diferencia_soporte": round(float(dif_soporte), 4),
        "pasivo_ajeno_soporte": aje["soporte"]["puntaje"],
        "nota": "la capacidad (1) exige accion POR CONSTRUCCION: que el encarnado gane ahi no es "
                "evidencia de nada, es el control positivo de que la comparacion ve diferencias."}


def regla31(verbose=True, pasos=PASOS_MINIMOS):
    fallos = []
    filas = comparar(semilla=1, pasos=pasos)

    # 1) CONTROL POSITIVO: en la capacidad que exige accion, el encarnado debe ganar. Si ni ahi
    #    ganara, la comparacion seria ciega y ningun empate posterior significaria nada.
    c1 = (filas["encarnado"]["frontera"]["puntaje"]
          > filas["pasivo_propio"]["frontera"]["puntaje"])
    if verbose:
        print(f"  {'ok  ' if c1 else 'FALLO'} CONTROL POSITIVO (frontera yo/mundo): encarnado "
              f"{filas['encarnado']['frontera']['puntaje']} vs pasivo "
              f"{filas['pasivo_propio']['frontera']['puntaje']} — la comparacion SI ve diferencias")
    if not c1:
        fallos.append("control-positivo")

    # 2) DOS ENCARNADOS IDENTICOS EMPATAN: la comparacion no fabrica ventajas del ruido.
    d = _dieta(777, pasos)
    ex = _examen(777, pasos)
    a = fisica_de_soporte(d, ex)["puntaje"]
    b = fisica_de_soporte(d, ex)["puntaje"]
    c2 = abs(a - b) < 1e-9
    if verbose:
        print(f"  {'ok  ' if c2 else 'FALLO'} GEMELOS: dos medidas de la misma dieta dan lo mismo "
              f"({a} vs {b}) — no se fabrican ventajas")
    if not c2:
        fallos.append("gemelos")

    # 3) VENTAJA PLANTADA: si a una condicion se le da una dieta con MAS informacion, la
    #    comparacion tiene que notarlo. (Trampa a proposito: el examen contra un mundo trivial.)
    ex_trivial = dict(ex)
    ex_trivial["flota"] = ex["cae2"]        # lo "imposible" ya no lo es: debe caer el puntaje
    peor = fisica_de_soporte(d, ex_trivial)["puntaje"]
    c3 = peor < a
    if verbose:
        print(f"  {'ok  ' if c3 else 'FALLO'} VENTAJA PLANTADA: con un examen trivial el puntaje "
              f"baja ({peor} < {a}) — la vara reacciona a lo que mide")
    if not c3:
        fallos.append("ventaja-plantada")

    # 4) EL PASIVO-AJENO no puede plantear la frontera: no tiene ordenes que comparar.
    c4 = filas["pasivo_ajeno"]["frontera"]["puntaje"] == 0.0
    if verbose:
        print(f"  {'ok  ' if c4 else 'FALLO'} PASIVO-AJENO: no puede plantear la frontera "
              f"(puntaje {filas['pasivo_ajeno']['frontera']['puntaje']}) — sin copia eferente")
    if not c4:
        fallos.append("pasivo-ajeno")

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — la comparacion ve diferencias reales y no inventa."
                                if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


def main():
    ap = argparse.ArgumentParser(description="El control del observador pasivo (prereg-32)")
    ap.add_argument("--regla31", action="store_true")
    ap.add_argument("--semilla", type=int, default=None)
    ap.add_argument("--pasos", type=int, default=PASOS_MINIMOS)
    a = ap.parse_args()
    if a.pasos < PASOS_MINIMOS:
        raise SystemExit(f"MEDICION INVALIDA: {a.pasos} pasos (minimo {PASOS_MINIMOS}).")
    if a.regla31:
        sys.exit(regla31(pasos=a.pasos))
    if a.semilla is None:
        print("uso: --regla31 | --semilla N")
        return
    filas = comparar(semilla=a.semilla, pasos=a.pasos)
    salida = {"prerregistro": 32, "semilla": a.semilla, "pasos": a.pasos,
              "condiciones": filas, "veredicto": veredicto(filas)}
    out = os.path.join(BASE, "resultados", f"p32-observador-pasivo-s{a.semilla}")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "resumen.json"), "w", encoding="utf-8") as f:
        json.dump(salida, f, indent=2, ensure_ascii=False, default=str)
    print(f"guardado en {out}/resumen.json (parcial — el veredicto exige las 5 semillas juntas)")


if __name__ == "__main__":
    main()
