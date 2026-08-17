# latente_conservado.py — ¿EL LATENTE CONSERVA ALGO? MEDIRLO, NO IMPONERLO (prerregistro-64,
# 17-ago-2026).
#
# LO QUE PEDIA EL ITEM 27 Y POR QUE NO SE HACE ASI: la critica externa proponia regularizar el
# latente con estructura hamiltoniana. UNA PERDIDA HAMILTONIANA LE ESTA DICIENDO A DIEGO QUE EL
# MUNDO CONSERVA ALGO. Eso no es una arquitectura: es una ley de la fisica humana metida por la
# puerta de atras, y de las mas caras. Si se la regalamos y luego "descubre" que hay una cantidad
# conservada, no ha descubierto nada: ha repetido lo que le pusimos en la perdida. Regla 27.
#
#     ENTRENAR sigue siendo con perdida de pixel y nada mas, exactamente como esta publicado.
#     MEDIR si el latente admite una cantidad casi constante es cosa NUESTRA, del lado humano.
#     MEDIR NO ES ENSEÑAR: esa es la frontera entera de la Regla 27.
#
# QUE SE IMPORTA Y NO SE COPIA: de `ojos_keypoint` —sellado— la escena, las dos arquitecturas y
# `entrenar`; de `invariantes` —sellado— los tres umbrales y la medida de calidad. Lo UNICO propio
# es el diccionario: `invariantes.buscar` esta escrito para DOS variables y un latente tiene mas.
#
# LO QUE ESA GENERALIZACION CUESTA, dicho antes de medir: un diccionario mas grande encuentra
# invariantes mas facilmente POR CASUALIDAD. Por eso el nulo no es un adorno aqui, es el criterio
# que manda: si el nulo encuentra invariantes, el estudio se descarta entero.
#
# Uso: python latente_conservado.py [--regla31] [--salida resultados/p64-latente/medida.json]

import os
import sys
import json
import math
import argparse

import numpy as np
import torch

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "codigo"))

import invariantes as INV                                                   # noqa: E402
import ojos_keypoint as OK                                                  # noqa: E402

# QUE ESTUDIA ESTE MODULO: los latentes. Por eso su regla31() NO los toca — trabaja con
# trayectorias hechas a mano.
SUJETO = ("LATENTE",)

# ------------------------------------------------------------------ EL PRERREGISTRO, EN CODIGO
# NUEVAS. Ninguna quemada en el banco (101,103,211,223,251,263) ni usada en los prerregistros
# 56 (227..241) y 57 (251..271).
SEMILLAS = (277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367)
MINIMAS_A_FAVOR = 12          # P(X >= 12 | 15, 0.5) = 0.0176, calculado ANTES (error nº26)

METODO = {
    "prerregistro": 64,
    "tipo_de_medida": "mixta",   # por semilla es binario; el criterio cuenta semillas
    "que_mide": ("en cuantas semillas el latente del cuello de botella espacial admite una "
                 "cantidad casi constante fuera de muestra que el latente de pixeles no admite, "
                 "sin que ninguna perdida se lo haya pedido"),
    "comparten_datos": {
        "hay": True,
        "porque": "los dos latentes se entrenan sobre LA MISMA escena de cada semilla, a "
                  "proposito: si cada uno viera un mundo distinto, la diferencia podria venir del "
                  "mundo y no del cuello de botella. La comparacion es pareada por semilla",
    },
    "linea_base": ("el latente de PIXELES planos, entrenado sobre las mismas escenas, con las "
                   "mismas semillas y las mismas epocas. Es el rival correcto porque lo unico que "
                   "cambia entre los dos es el cuello de botella"),
    "formulas": [
        {"base": {"ruido_medida": 0.001}, "parametro": "ruido_medida", "factor": 100.0,
         "esperado": "baja",
         "porque": "el ruido de MEDIDA se suma a la trayectoria ya ocurrida y ensucia el valor de "
                   "cualquier cantidad conservada, luego la calidad del invariante tiene que "
                   "caer. De MEDIDA y no de proceso: el de proceso EXCITA el sistema y no entierra "
                   "nada (LECCION-RUIDO-01, que ya me costo tres modulos). Base 0.001 y NO 0.0, "
                   "porque comparar un cero con otro cero no prueba nada"},
    ],
}


# --------------------------------------------------------------- el buscador, generalizado
def hay_objetivo_propio(ruta=None):
    """¿Este modulo define una funcion de perdida propia? Se comprueba con AST y NO buscando una
    cadena en el texto: mi primera version buscaba la cadena "def perdida" en el propio archivo y
    se marcaba a si misma, porque esa cadena estaba en el chequeo. Es la TERCERA vez que un
    detector mio confunde una cadena con codigo, y esta en el catalogo. Y la SEGUNDA version
    tambien se marcaba a si misma: se llamaba `define_alguna_perdida` y su propio nombre contenia
    la palabra que buscaba. De ahi que esta se llame como se llama."""
    import ast
    fuente = open(ruta or __file__, encoding="utf-8").read()
    for nodo in ast.walk(ast.parse(fuente)):
        if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if any(p in nodo.name.lower() for p in ("perdida", "loss", "energia", "hamilton")):
                return True
    return False


def diccionario(X):
    """TODOS los terminos lineales y cuadraticos de las columnas. SIN termino constante: con un
    '1' en el diccionario la respuesta trivial —la constante— seria representable y ganaria
    siempre. Es la misma decision que tomo `invariantes` y por la misma razon."""
    X = np.asarray(X, dtype=float)
    cols = [X[:, i] for i in range(X.shape[1])]
    for i in range(X.shape[1]):
        for j in range(i, X.shape[1]):
            cols.append(X[:, i] * X[:, j])
    return np.column_stack(cols)


def buscar(X, techo=INV.TECHO_VARIACION, salto=INV.SALTO_MINIMO, fraccion=INV.FRACCION_BUSQUEDA):
    """La direccion de MINIMA variacion se busca en el primer tramo y SE JUZGA EN EL QUE NO VIO.
    Mismos umbrales que `invariantes`, importados y no copiados; lo unico distinto es que el
    diccionario admite cualquier numero de columnas."""
    X = np.asarray(X, dtype=float)
    if len(X) < 200:
        return None
    Theta = diccionario(X)
    escalas = np.linalg.norm(Theta, axis=0)
    escalas[escalas == 0] = 1.0
    Th = Theta / escalas                      # adimensionalizacion con las escalas propias
    corte = int(len(Th) * fraccion)
    A, B = Th[:corte], Th[corte:]
    if len(B) < 50:
        return None
    C = np.cov((A - A.mean(axis=0)).T)
    vals, vecs = np.linalg.eigh(C)
    orden = np.argsort(vals)
    q_mejor = B @ vecs[:, orden[0]]
    q_sig = B @ vecs[:, orden[1]]
    var_mejor, var_sig = INV._calidad(q_mejor), INV._calidad(q_sig)
    if not np.isfinite(var_mejor) or var_mejor > techo:
        return None                           # no esta quieta donde no miro: no hay invariante
    # EL SALTO: si la siguiente direccion esta igual de quieta, no hay UN invariante — hay ruido
    # con muchas direcciones parecidas, y coronar a la primera seria el error del panel de jueces.
    if not np.isfinite(var_sig) or var_sig < var_mejor * salto:
        return None
    return {"variacion_relativa_fuera_de_muestra": round(var_mejor, 5),
            "variacion_de_la_siguiente": round(var_sig, 5),
            "salto": round(float(var_sig / var_mejor), 2),
            "terminos": int(Theta.shape[1])}


def nulo_por_columnas(X, semilla=0):
    """EL NULO del prerregistro-52 (ENMIENDA 1): barajar CADA COLUMNA por separado. Destruye la
    relacion entre columnas —que es donde vive un invariante— y conserva la distribucion de cada
    una. Barajar FILAS no serviria: una cantidad conservada vale lo mismo en cualquier orden, y
    ese fue el error nº8 del catalogo."""
    rng = np.random.default_rng(int(semilla))
    Y = np.array(X, dtype=float, copy=True)
    for j in range(Y.shape[1]):
        Y[:, j] = rng.permutation(Y[:, j])
    return Y


def probabilidad_del_azar(k=MINIMAS_A_FAVOR, n=len(SEMILLAS)):
    """P(X >= k | n, p=0.5): lo que una moneda justa saca bajo este criterio de conteo."""
    return sum(math.comb(n, i) for i in range(int(k), int(n) + 1)) / float(2 ** int(n))


# --------------------------------------------------------------------------- los latentes
def latentes(semilla):
    """Entrena las DOS arquitecturas publicadas sobre LA MISMA escena y devuelve sus latentes.
    La perdida es la de `ojos_keypoint.entrenar` — este modulo no define ninguna."""
    vids, _ = OK.escena(semilla)
    X = torch.tensor(vids)
    salida = {}
    for nombre, M in (("pixel", OK.Pixel()), ("keypoint", OK.Keypoint())):
        m, _p = OK.entrenar(M, X, semilla=semilla)
        with torch.no_grad():
            salida[nombre] = m.z(X).numpy()
    return salida


# ---------------------------------------------------------------- la ficha y las autopruebas
def _oscilador(n=600, ruido_medida=0.0, semilla=71):
    """Trayectoria HECHA A MANO con invariante conocido: x2+v2 se queda quieto. Es el andamio del
    control positivo, no un resultado."""
    rng = np.random.default_rng(int(semilla))
    t = np.linspace(0, 30, n)
    x, v = np.cos(t), -np.sin(t)
    X = np.column_stack([x, v])
    return X + rng.normal(0, ruido_medida, X.shape)


def _metodo_medir(ruido_medida=0.001):
    """La medida que la relacion metamorfica mueve: la CALIDAD del invariante hallado sobre el
    oscilador hecho a mano. Menos calidad = numero mas grande, asi que se devuelve invertido para
    que 'baja' signifique lo que dice."""
    r = buscar(_oscilador(ruido_medida=float(ruido_medida)), techo=np.inf, salto=1.0)
    if not r:
        return 0.0
    return float(1.0 / (r["variacion_relativa_fuera_de_muestra"] + 1e-12))


def _metodo_sanidad():
    """PASO 3 — LA FICHA. La pregunta: **¿el buscador generalizado encuentra lo que hay y NO lo que
    no hay?** Con un diccionario grande la segunda mitad es la que importa: mas terminos hacen mas
    facil encontrar un invariante por casualidad."""
    fallos = []
    if buscar(_oscilador()) is None:
        fallos.append("no encuentra el invariante de un oscilador limpio: el buscador esta roto")
    rng = np.random.default_rng(5)
    if buscar(rng.normal(size=(600, 2))) is not None:
        fallos.append("encuentra un invariante en RUIDO PURO: se lo esta inventando")
    if buscar(nulo_por_columnas(_oscilador(), semilla=3)) is not None:
        fallos.append("el nulo por columnas sigue dando invariante: no destruye lo que debe")
    if not SEMILLAS:
        fallos.append("no hay ni una semilla que correr: el estudio aprobaria sobre nada")
    if probabilidad_del_azar() > 0.05:
        fallos.append(f"el criterio de conteo lo pasa el azar el {probabilidad_del_azar():.1%}")
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
        print("REGLA 31 de latente_conservado — sobre MI PROCEDIMIENTO, con trayectorias a mano\n")

    r = buscar(_oscilador())
    caso("control positivo: encuentra el invariante de un oscilador limpio", r is not None,
         f"variacion {r['variacion_relativa_fuera_de_muestra'] if r else '-'}")

    rng = np.random.default_rng(5)
    caso("señuelo: NO encuentra invariante en ruido puro",
         buscar(rng.normal(size=(600, 2))) is None)
    caso("señuelo: NO encuentra invariante en ruido puro de MUCHAS columnas — el caso que importa "
         "con un diccionario grande",
         buscar(rng.normal(size=(600, 6))) is None)

    caso("el nulo por columnas DESTRUYE el invariante que si existia",
         buscar(nulo_por_columnas(_oscilador(), semilla=3)) is None)
    caso("y baraja las columnas, NO las filas: barajar filas dejaria el invariante intacto",
         buscar(_oscilador()[np.random.default_rng(3).permutation(600)]) is not None)

    f = METODO["formulas"][0]
    base = f["base"]["ruido_medida"]
    antes, despues = _metodo_medir(base), _metodo_medir(base * f["factor"])
    caso(f"metamorfica: mas ruido de MEDIDA = peor invariante (base {base}, x{f['factor']})",
         despues < antes, f"{antes:.1f} -> {despues:.1f}")

    p = probabilidad_del_azar()
    caso("el azar NO pasa el criterio de conteo congelado", p <= 0.05, f"P={p:.4f}")

    caso("este modulo NO define ninguna perdida propia: entrena con la publicada",
         not hay_objetivo_propio())

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — encuentra lo que hay y no lo que no hay"
                                if not fallos else f"REPRUEBA en {len(fallos)}: {fallos}"))
    return 0 if not fallos else 1


# ------------------------------------------------------------------------------- la corrida
def correr(salida=None, verbose=True):
    filas = []
    for s in SEMILLAS:
        Z = latentes(s)
        fila = {"semilla": int(s)}
        for nombre in ("pixel", "keypoint"):
            fila[nombre] = buscar(Z[nombre]) is not None
            fila[f"nulo_{nombre}"] = buscar(nulo_por_columnas(Z[nombre], semilla=s)) is not None
        filas.append(fila)
        if verbose:
            print(f"  semilla {s}: keypoint {'SI' if fila['keypoint'] else 'no'} · "
                  f"pixel {'SI' if fila['pixel'] else 'no'} · nulos "
                  f"{'SI' if (fila['nulo_keypoint'] or fila['nulo_pixel']) else 'no'}")

    gana_keypoint = sum(1 for f in filas if f["keypoint"] and not f["pixel"])
    gana_pixel = sum(1 for f in filas if f["pixel"] and not f["keypoint"])
    nulos = sum(1 for f in filas if f["nulo_keypoint"] or f["nulo_pixel"])

    datos = {
        "prerregistro": 64,
        "semillas": len(SEMILLAS),
        "exigidas": MINIMAS_A_FAVOR,
        "probabilidad_del_azar": probabilidad_del_azar(),
        "con_invariante_keypoint": sum(1 for f in filas if f["keypoint"]),
        "con_invariante_pixel": sum(1 for f in filas if f["pixel"]),
        "semillas_donde_solo_el_keypoint_conserva": gana_keypoint,
        "semillas_donde_solo_el_pixel_conserva": gana_pixel,
        "semillas_con_invariante_en_el_NULO": nulos,
        "filas": filas,
        "criterios": {
            "A_no_se_impone_nada": not hay_objetivo_propio(),
            "B_el_nulo_no_encuentra_nada": nulos == 0,
            "C_el_keypoint_conserva_mas": gana_keypoint >= MINIMAS_A_FAVOR,
            "D_el_juicio_es_fuera_de_muestra": INV.FRACCION_BUSQUEDA < 1.0,
        },
    }
    c = datos["criterios"]
    if not c["A_no_se_impone_nada"]:
        datos["veredicto"] = ("SE DESCARTA — este modulo define una perdida propia, o sea le esta "
                              "enseñando fisica humana a Diego")
    elif not c["B_el_nulo_no_encuentra_nada"]:
        datos["veredicto"] = (f"SE DESCARTA EL ESTUDIO ENTERO — el nulo encontro invariantes en "
                              f"{nulos} semillas: el diccionario grande los esta fabricando")
    elif c["C_el_keypoint_conserva_mas"]:
        datos["veredicto"] = (f"LA ESTRUCTURA APARECE SOLA — el cuello de botella espacial admite "
                              f"una cantidad conservada donde el de pixeles no, en {gana_keypoint} "
                              f"de {len(SEMILLAS)} semillas y SIN que ninguna perdida se lo pidiera")
    else:
        datos["veredicto"] = (f"EL CUELLO DE BOTELLA ESPACIAL NO PRODUCE ESTRUCTURA CONSERVADA — "
                              f"solo el keypoint conserva en {gana_keypoint} de {len(SEMILLAS)} y "
                              f"hacian falta {MINIMAS_A_FAVOR}. La mejora del INFORME-67 es de "
                              f"precision, no de fisica")

    if salida:
        ruta = os.path.join(BASE, salida)
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
    if verbose:
        print(f"\ncon invariante: keypoint {datos['con_invariante_keypoint']}/{len(SEMILLAS)} · "
              f"pixel {datos['con_invariante_pixel']}/{len(SEMILLAS)}")
        print(f"solo el keypoint: {gana_keypoint} · solo el pixel: {gana_pixel} · "
              f"invariantes en el NULO: {nulos}")
        for k, v in c.items():
            print(f"  {'ok   ' if v else 'FALLO'} {k}")
        print(f"\nVEREDICTO: {datos['veredicto']}")
    return datos


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Prerregistro 64: ¿el latente conserva algo?")
    ap.add_argument("--regla31", action="store_true")
    ap.add_argument("--salida", default="resultados/p64-latente/medida.json")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    correr(salida=a.salida)
