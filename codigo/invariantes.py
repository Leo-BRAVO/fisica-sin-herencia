# invariantes.py — EL SEGUNDO MOTOR: buscar lo que NO cambia (prerregistro-52, 11-ago-2026).
#
# POR QUE EXISTE, y NO es para sustituir a sindy4. El primer motor solo puede expresar mezclas de
# SEIS PIEZAS FIJAS. Si la ley del mundo no esta ahi, no la vera ni con el umbral perfecto — y no
# dira "no se mirar eso": dira "no vi nada". ESTE MOTOR NO COMPITE POR SER MEJOR: COMPITE POR
# FALLAR DE OTRA MANERA, y es la unica forma de detectar esa jaula desde fuera.
#
# QUE HACE, y por que es una forma DISTINTA de mirar:
#   sindy4     pregunta "¿COMO CAMBIAN las cosas?" — busca una ecuacion de movimiento.
#   este       pregunta "¿QUE NO CAMBIA?"          — busca una cantidad conservada.
# Es la idea del teorema de Noether al reves y sin heredar nada: no se parte de una simetria
# conocida, se buscan combinaciones de las lecturas cuyo valor se mantiene constante a lo largo de
# la trayectoria. Y tiene una propiedad que ninguna ecuacion de movimiento tiene: UNA CANTIDAD
# CONSERVADA SE DESCUBRE MIRANDO, SIN INTERVENIR.
#
# EL DICCIONARIO NO LLEVA TERMINO CONSTANTE, y es una decision de diseño, no un olvido: una
# constante se conserva trivialmente, asi que con el `1` dentro la respuesta vacia "la constante
# es constante" seria la ganadora siempre. SE HACE IRREPRESENTABLE quitandola del diccionario, en
# vez de prohibirla con un chequeo que alguien podria quitar despues.
#
# Y SE ADIMENSIONALIZA DESDE EL PRIMER DIA: la leccion del DIAGNOSTICO-MOTOR-01 es que un corte con
# unidades se mueve con la escala. Aqui se normaliza por las escalas de los propios datos —nunca
# unidades humanas, que serian herencia— y el criterio es una VARIACION RELATIVA, sin unidades.
#
# Uso: python invariantes.py [--regla31] [--salida resultados/p52-invariantes/medida.json]

import os
import sys
import json
import argparse

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sindy4                                                               # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NOMBRES = ["x", "v", "x2", "xv", "v2"]      # SIN el "1": ver la cabecera
FRACCION_BUSQUEDA = 0.7      # se busca en el 70% y se comprueba en el 30% que no vio
TECHO_VARIACION = 0.05       # variacion relativa maxima, fuera de muestra, para declarar
SALTO_MINIMO = 10.0          # cuanto mas quieta debe estar la mejor direccion que la siguiente
SEMILLAS = (71, 73, 79, 83, 89)     # nuevas: ninguna se ha usado en este repositorio
T = 4000
DT = 0.02

METODO = {
    "prerregistro": 52,
    "tipo_de_medida": "umbral",   # declara invariante o no lo declara: es binario por corrida
    "que_mide": ("si existe una combinacion de las lecturas cuyo valor se mantiene constante a lo "
                 "largo de la trayectoria, comprobada en el tramo que el motor NO vio"),
    "comparten_datos": {
        "hay": True,
        "porque": "la busqueda y la comprobacion salen de la MISMA trayectoria, partida por "
                  "tiempo: primero el 70%, luego el 30% final. Es una particion, no una "
                  "reutilizacion — el tramo de comprobacion no participa en la busqueda.",
    },
    "linea_base": ("declarar que CUALQUIER direccion es invariante — el tonto de la Regla 11. Se "
                   "le gana exigiendo un SALTO respecto de la siguiente direccion menos variable "
                   "y que la constancia se mantenga fuera de muestra"),
    "formulas": [
        {"base": {"ruido_medida": 0.001}, "parametro": "ruido_medida", "factor": 100.0,
         "esperado": "baja",
         "porque": "el ruido de MEDIDA se suma a la trayectoria ya ocurrida y ensucia el valor de "
                   "cualquier cantidad conservada, luego la calidad del invariante tiene que "
                   "caer. De MEDIDA y no de proceso: el de proceso excita el sistema y no "
                   "entierra nada (LECCION-RUIDO-01, que ya me costo tres modulos). Base 0.001 y "
                   "NO 0.0, porque comparar un cero con otro cero no prueba nada"},
    ],
}


def _diccionario(X):
    x, v = X[:, 0], X[:, 1]
    return np.column_stack([x, v, x * x, x * v, v * v])


def _calidad(q):
    """Cuanto se mueve una cantidad, SIN UNIDADES: su desviacion dividida por su escala tipica.
    Se usa la escala de la propia cantidad para que multiplicar el mundo por mil no cambie nada."""
    escala = float(np.mean(np.abs(q)))
    if escala <= 0:
        return np.inf
    return float(np.std(q) / escala)


def buscar(X, techo=TECHO_VARIACION, salto=SALTO_MINIMO, fraccion=FRACCION_BUSQUEDA):
    """Devuelve el invariante o None. La direccion de MINIMA variacion se busca en el primer
    tramo y se juzga en el que no vio."""
    if len(X) < 200:
        return None
    Theta = _diccionario(np.asarray(X, dtype=float))
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
    mejor, siguiente = vecs[:, orden[0]], vecs[:, orden[1]]

    # EL JUICIO ES FUERA DE MUESTRA: la cantidad hallada en A tiene que seguir quieta en B.
    q_mejor = B @ mejor
    q_sig = B @ siguiente
    var_mejor, var_sig = _calidad(q_mejor), _calidad(q_sig)
    if not np.isfinite(var_mejor) or var_mejor > techo:
        return None                            # no esta quieta donde no miro: no hay invariante
    # EL SALTO: si la siguiente direccion esta igual de quieta, no hay UN invariante — hay ruido
    # con muchas direcciones parecidas, y coronar a la primera seria el error del panel de jueces.
    if not np.isfinite(var_sig) or var_sig < var_mejor * salto:
        return None
    c = mejor / (np.abs(mejor).max() or 1.0)
    return {"combinacion": {NOMBRES[i]: round(float(c[i] / escalas[i]
                                                    * escalas[int(np.argmax(np.abs(mejor)))]), 4)
                            for i in range(len(NOMBRES)) if abs(c[i]) > 0.05},
            "variacion_relativa_fuera_de_muestra": round(var_mejor, 5),
            "variacion_de_la_siguiente": round(var_sig, 5),
            "salto": round(float(var_sig / var_mejor), 2)}


# ------------------------------------------------------------------ los mundos
def _mundo(amortiguamiento=0.0, semilla=71, escala=1.0, ruido_medida=0.0):
    """Oscilador con o sin amortiguamiento. SIN amortiguar tiene una cantidad exactamente
    conservada; amortiguado NO la tiene, porque se disipa. La verdad la ponemos nosotros."""
    rng = np.random.default_rng(int(semilla))
    x, v = 1.0 + 0.1 * rng.normal(), 0.0
    tray = []
    for _ in range(T):
        tray.append([x, v])
        ax = -0.9 * x - float(amortiguamiento) * v
        v = v + ax * DT
        x = x + v * DT
    Z = np.array(tray) * float(escala)
    if ruido_medida:
        Z = Z + rng.normal(0, float(ruido_medida) * float(escala), Z.shape)
    return Z


def _metodo_medir(ruido_medida=0.001):
    """PASO 1 — la medida escalar: la CALIDAD del invariante hallado (cuanto mas alto, mas quieto).
    Se devuelve el salto respecto de la siguiente direccion, que es lo que distingue un invariante
    de un ruido con muchas direcciones parecidas. Si no hay invariante, 0."""
    inv = buscar(_mundo(amortiguamiento=0.0, semilla=71, ruido_medida=float(ruido_medida)))
    return float(inv["salto"]) if inv else 0.0


def _metodo_sanidad():
    """PASO 3 — LA FICHA. La pregunta: **¿el motor distingue un mundo con cantidad conservada de
    uno donde se disipa?** Si declarara invariante en el amortiguado, estaria viendo lo que quiere
    ver — que es el defecto que mato a sindy3 sobre señal constante."""
    fallos = []
    sin_amort = sum(1 for s in SEMILLAS if buscar(_mundo(0.0, s)) is not None)
    con_amort = sum(1 for s in SEMILLAS if buscar(_mundo(0.35, s)) is not None)
    if sin_amort < 5:
        fallos.append(f"no encuentra el invariante que SI existe: {sin_amort}/5")
    if con_amort > 0:
        fallos.append(f"declara invariante donde la cantidad se DISIPA: {con_amort}/5")
    return {"aprueba": not fallos, "fallos": fallos,
            "sin_amortiguar": sin_amort, "amortiguado": con_amort}


def regla31(verbose=True):
    """LA REGLA 31 — sobre MI PROCEDIMIENTO, los DOS lados, y NUNCA sobre sindy4.

    La comparacion entre motores es el criterio E del prerregistro-52, es decir RESULTADO. Meterla
    aqui haria que el criterio E no pudiera fallar, y seria el septimo criterio tautologico del
    mes."""
    fallos = []

    def caso(nombre, ok, extra=""):
        if verbose:
            print(f"  {'ok  ' if ok else 'FALLO'} {nombre}" + (f"  [{extra}]" if extra else ""))
        if not ok:
            fallos.append(nombre)

    if verbose:
        print("== REGLA 31 del prereg-52: el buscador de invariantes ==")

    # CONTROL POSITIVO SOBRE UNA VERDAD QUE PONGO YO: una cantidad EXACTAMENTE conservada,
    # construida a mano, que no depende de ningun simulador.
    rng = np.random.default_rng(52)
    t = np.linspace(0, 40, T)
    xx = np.cos(t) + 0.001 * rng.normal(size=T)
    vv = -np.sin(t) + 0.001 * rng.normal(size=T)
    inv = buscar(np.column_stack([xx, vv]))
    caso("CONTROL POSITIVO: encuentra una cantidad que YO puse exactamente conservada",
         inv is not None, str(inv and inv["combinacion"]))

    # SEÑUELO: ruido puro. Si declarase algo, estaria viendo lo que quiere ver.
    caso("SEÑUELO: sobre ruido puro no declara invariante",
         buscar(rng.normal(size=(T, 2))) is None)

    # EL NULO CORRECTO PARA ESTE MOTOR: barajar CADA COLUMNA POR SEPARADO.
    # AQUI PUSE PRIMERO EL BARAJADO DE FILAS —el nulo de sindy3— Y LA PUERTA ME REPROBO, con
    # razon: sobre filas barajadas este motor SI encuentra el invariante, y hace bien. Barajar el
    # orden temporal destruye una ecuacion diferencial, porque las derivadas necesitan el orden;
    # pero NO TOCA UNA CANTIDAD CONSERVADA: x2+v2 vale lo mismo visites los puntos en el orden que
    # los visites. Copie el nulo de otro motor sin preguntarme si aplicaba al mio.
    # UN NULO TIENE QUE DESTRUIR LA ESTRUCTURA QUE EL MOTOR BUSCA, y cada motor busca otra.
    # Barajar cada columna por separado rompe la relacion entre x y v —la superficie donde vive el
    # invariante— conservando la distribucion de cada una. Ahi si no debe declarar nada.
    Z = _mundo(0.0, 71)
    Zc = np.column_stack([rng.permutation(Z[:, 0]), rng.permutation(Z[:, 1])])
    caso("NULO: con las columnas barajadas por separado no declara invariante",
         buscar(Zc) is None)

    # Y SE CONSERVA EL BARAJADO DE FILAS, pero como lo que es: la comprobacion de que este motor
    # NO depende del orden temporal, que es la propiedad que lo hace distinto del primero.
    caso("con las FILAS barajadas SI lo encuentra (no depende del orden temporal, y debe ser asi)",
         buscar(Z[rng.permutation(len(Z))]) is not None)

    # LA RESPUESTA TRIVIAL ES IRREPRESENTABLE: el diccionario no lleva el termino constante.
    caso("el diccionario NO contiene el termino constante (la respuesta trivial no cabe)",
         "1" not in NOMBRES)

    # NO DEPENDE DE LAS UNIDADES: el mismo mundo x1000 da el mismo veredicto. Es la leccion del
    # DIAGNOSTICO-MOTOR-01, aplicada desde el primer dia en vez de despues de dos informes.
    caso("el veredicto no cambia al multiplicar el mundo por mil",
         (buscar(_mundo(0.0, 71)) is not None) == (buscar(_mundo(0.0, 71, escala=1000.0))
                                                   is not None))

    # LA MEDIDA RESPONDE, y con base distinta de cero. Sexta vez que lo escribo este mes.
    limpio, sucio = _metodo_medir(0.001), _metodo_medir(0.1)
    caso("la medida RESPONDE al ruido de sensor (y la base no es cero)",
         limpio > 0 and sucio < limpio, f"{limpio:.1f} -> {sucio:.1f}")

    # LA FICHA
    fs = _metodo_sanidad()
    caso("distingue conservado de disipado", fs["aprueba"], str(fs))

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — busca lo que no cambia sin inventarselo."
                                if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


def correr(salida=None, verbose=True):
    rng = np.random.default_rng(52)
    datos = {"prerregistro": 52, "semillas": list(SEMILLAS), "mundos": {}}

    for nombre, hacer in (("sin_amortiguar", lambda s: _mundo(0.0, s)),
                          ("amortiguado", lambda s: _mundo(0.35, s)),
                          ("filas_barajadas", lambda s: _mundo(0.0, s)[rng.permutation(T)]),
                          ("columnas_barajadas",
                           lambda s: np.column_stack([
                               np.random.default_rng(s).permutation(_mundo(0.0, s)[:, 0]),
                               np.random.default_rng(s + 1).permutation(_mundo(0.0, s)[:, 1])])),
                          ("ruido_puro", lambda s: np.random.default_rng(s).normal(size=(T, 2)))):
        declara_inv, declara_sindy = 0, 0
        for s in SEMILLAS:
            Z = hacer(s)
            if buscar(Z) is not None:
                declara_inv += 1
            if sindy4.descubrir(Z, dt=DT) is not None:
                declara_sindy += 1
        datos["mundos"][nombre] = {"invariantes": declara_inv, "sindy4": declara_sindy,
                                   "de": len(SEMILLAS)}

    datos["D_escala"] = {"x1": sum(1 for s in SEMILLAS if buscar(_mundo(0.0, s)) is not None),
                         "x1000": sum(1 for s in SEMILLAS
                                      if buscar(_mundo(0.0, s, escala=1000.0)) is not None)}

    m = datos["mundos"]
    crit = {
        "A_encuentra_lo_que_hay": m["sin_amortiguar"]["invariantes"] == 5,
        "B_calla_donde_se_disipa": m["amortiguado"]["invariantes"] == 0,
        # El barajado de FILAS no cuenta como nulo para este motor: ver enmienda 1 del
        # prerregistro-52. Los nulos son las columnas barajadas y el ruido puro.
        "C_nulos": (m["columnas_barajadas"]["invariantes"] == 0
                    and m["ruido_puro"]["invariantes"] == 0),
        "D_no_depende_de_las_unidades": datos["D_escala"]["x1"] == datos["D_escala"]["x1000"],
        # E NO puede sostenerse solo sobre las filas barajadas: alli la discrepancia es una
        # consecuencia trivial de la definicion —uno necesita el orden temporal y el otro no— y no
        # un aporte. Se exige discrepancia en algun mundo QUE NO SEA ese.
        "E_los_dos_motores_discrepan": any(v["invariantes"] != v["sindy4"]
                                           for k, v in m.items() if k != "filas_barajadas"),
        "E_ademas_discrepan_en_filas_barajadas":
            m["filas_barajadas"]["invariantes"] != m["filas_barajadas"]["sindy4"],
    }
    datos["criterios"] = {k: bool(v) for k, v in crit.items()}

    if not crit["A_encuentra_lo_que_hay"]:
        datos["veredicto"] = ("SE DESCARTA — no encuentra un invariante que existe y es exacto")
    elif not (crit["B_calla_donde_se_disipa"] and crit["C_nulos"]):
        datos["veredicto"] = ("SE DESCARTA — declara invariantes donde no los hay, que es el "
                              "defecto de sindy3 con otro nombre")
    elif not crit["E_los_dos_motores_discrepan"]:
        datos["veredicto"] = ("FUNCIONA PERO NO APORTA — coincide siempre con sindy4, luego "
                              "duplicar la auditoria no esta justificado")
    elif all(crit.values()):
        datos["veredicto"] = ("SEGUNDO MOTOR EN PIE — encuentra lo que hay, calla donde no lo hay, "
                              "no depende de las unidades y DISCREPA de sindy4")
    else:
        datos["veredicto"] = ("NO CONCLUYENTE — fallan "
                              + ", ".join(k for k, v in crit.items() if not v))

    if salida:
        ruta = os.path.join(BASE, salida)
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
    if verbose:
        print(f"\nVEREDICTO: {datos['veredicto']}")
    return datos


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Prerregistro 52: el motor de invariantes")
    ap.add_argument("--regla31", action="store_true")
    ap.add_argument("--salida", default="resultados/p52-invariantes/medida.json")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    correr(salida=a.salida)
