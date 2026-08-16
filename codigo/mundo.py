# mundo.py — EL LUGAR DONDE VIVE DIEGO (prerregistro-50, 11-ago-2026).
#
# POR QUE EXISTE. Hasta hoy Diego NO TIENE MUNDO: TIENE ESCENAS. Cada estudio monta su escenita,
# la mide y la tira, y nada persiste. El INFORME-57 encontro la consecuencia mas cruda: su brazo
# no alcanza nada — la punta baja como mucho a 0.380 y los objetos estan a 0.20. NADIE COMPROBO
# NUNCA QUE EL CUERPO LLEGARA AL MUNDO. Aqui eso pasa a ser un chequeo BLOQUEANTE.
#
# LAS DOS TRAMPAS DE LA REGLA 27, que este archivo existe para cerrar, y que son la parte que mas
# importa de todo el modulo:
#
#   1. LA RECOMPENSA. Si NOSOTROS decidimos que cuenta como "resuelto", le metemos nuestra fisica
#      por la funcion de recompensa. No le decimos F=ma: le decimos "te premio cuando aciertes lo
#      que yo, que se F=ma, considero acertar". Es herencia por la puerta de atras, con las
#      apariencias intactas. Por eso LA UNICA MONEDA ES LA PREDICCION DE SUS PROPIAS
#      OBSERVACIONES: Diego declara que observara dentro de N pasos, el mundo ocurre, se compara.
#      Nadie necesita saber fisica para puntuar eso.
#
#   2. LAS ETIQUETAS. "Ver numeros" solo vale si los numeros NO llevan nombre humano. Un vector de
#      lecturas crudas es admisible; "masa: 2 kg" es herencia, porque el kilogramo es un
#      descubrimiento humano y no un hecho del mundo. La ETIQUETA es la herencia.
#
# LOS DOS GUARDIANES DE ABAJO SE PRUEBAN INYECTANDO LA VIOLACION QUE DEBEN CAZAR. Un guardian que
# nunca se ha visto saltar es decoracion.
#
# Uso: python mundo.py [--regla31] [--salida resultados/p50-mundo/medida.json]

import os
import re
import sys
import json
import argparse

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# EL ALCANCE MEDIDO DEL CUERPO. Sale del INFORME-57, donde se midio con el brazo real en PyBullet,
# y NO se supone: si el mundo pusiera sus objetos fuera de esto, el chequeo de abajo bloquea.
ALCANCE = {"x": (-0.220, 0.657), "y": (-0.440, 0.439), "z": (0.380, 0.820),
           "medido": "10-ago-2026, INFORME-57"}

HORIZONTE = 5          # a cuantos pasos vista se le pide la prediccion
MARGEN_C = 0.10        # criterio C: cuanto debe ganarle un predictor con estado a la persistencia
TECHO_MUERTO = 0.02    # criterio D: ventaja maxima admisible en un mundo sin interaccion

# PALABRAS HUMANAS DE FISICA. Si alguna aparece en lo que Diego observa, es herencia. La lista es
# corta y a proposito: no pretende ser exhaustiva —ninguna lista lo seria— sino cazar el descuido
# tipico de ponerle nombre a una columna. Lo declara asi para que nadie confie de mas.
PROHIBIDAS = ("masa", "kg", "gramo", "velocidad", "aceleracion", "gravedad", "fuerza", "newton",
              "energia", "julio", "momento", "inercia", "peso", "metro", "segundo", "friccion",
              "rozamiento", "densidad", "presion", "pascal")

METODO = {
    "prerregistro": 50,
    "tipo_de_medida": "continua",
    "que_mide": ("cuanto mejor predice sus propias observaciones futuras un predictor que usa el "
                 "estado del mundo, frente a la linea base tonta de decir que nada cambia"),
    "comparten_datos": {
        "hay": True,
        "porque": "los dos predictores se evaluan sobre EXACTAMENTE la misma historia del mismo "
                  "mundo — esa es la definicion de la comparacion. Si cada uno tuviera su propia "
                  "historia, la diferencia podria ser de la historia.",
    },
    "linea_base": ("PERSISTENCIA: 'dentro de N pasos vere exactamente lo que veo ahora'. Es el "
                   "predictor mas tonto que existe (Regla 11). Un mundo donde la persistencia "
                   "puntua igual que un modelo no mide comprension de nada"),
    "formulas": [
        {"base": {"acoplamiento": 1.0}, "parametro": "acoplamiento", "factor": 0.0,
         "esperado": "baja",
         "porque": "el acoplamiento es cuanto influyen las acciones sobre el mundo. Con "
                   "acoplamiento CERO el mundo deja de responder, asi que conocer el estado ya no "
                   "ayuda a predecir y la ventaja sobre la persistencia tiene que caer. Es lo "
                   "unico que se sabe A PRIORI de esta medida. Base 1.0 y NO 0.0"},
    ],
}


# ------------------------------------------------------------------ el lugar
class Mundo:
    """UN LUGAR CON ESTADO, no una escena. Su estado sobrevive entre rondas y depende de todo lo
    que paso antes: esa es la diferencia entera con el gimnasio actual.

    La fisica es de juguete y NUESTRA — un objeto con inercia y roce dentro de una caja—, y no se
    le cuenta a Diego: el solo ve numeros sin nombre."""

    def __init__(self, semilla=50, acoplamiento=1.0):
        rng = np.random.default_rng(int(semilla))
        # el objeto nace DENTRO del alcance medido del cuerpo: es el criterio A, por construccion
        self.pos = np.array([rng.uniform(*ALCANCE["x"]), rng.uniform(*ALCANCE["y"]),
                             rng.uniform(*ALCANCE["z"])])
        self.vel = np.zeros(3)
        self.acoplamiento = float(acoplamiento)
        self.pasos = 0
        self._roce = 0.92

    def paso(self, accion):
        """Un instante. La accion empuja; el roce frena; las paredes del alcance rebotan."""
        a = np.asarray(accion, dtype=float)[:3] * self.acoplamiento
        self.vel = self.vel * self._roce + a * 0.02
        self.pos = self.pos + self.vel * 0.02
        for i, eje in enumerate(("x", "y", "z")):
            lo, hi = ALCANCE[eje]
            if self.pos[i] < lo:
                self.pos[i], self.vel[i] = lo, abs(self.vel[i]) * 0.5
            elif self.pos[i] > hi:
                self.pos[i], self.vel[i] = hi, -abs(self.vel[i]) * 0.5
        self.pasos += 1
        return self.observar()

    def observar(self):
        """LO QUE DIEGO VE: un vector de numeros SIN NOMBRE Y SIN UNIDAD. Seis columnas, y el que
        sean posicion y velocidad es asunto NUESTRO: el no se entera, y por eso no hereda nada."""
        return np.concatenate([self.pos, self.vel]).astype(float)

    def estado(self):
        return {"pos": self.pos.tolist(), "vel": self.vel.tolist(), "pasos": int(self.pasos)}


# ------------------------------------------------------------------ los dos guardianes de la R27
def guardian_de_etiquetas(observacion_con_nombres):
    """BLOQUEA si lo que Diego observa lleva una palabra humana de fisica.

    Recibe un diccionario nombre->valor, que es la forma en que la fuga ocurriria de verdad:
    alguien, por comodidad, le pone nombre a las columnas. Devuelve la lista de fugas."""
    fugas = []
    for clave in (observacion_con_nombres or {}):
        texto = str(clave).lower()
        for p in PROHIBIDAS:
            if re.search(rf"\b{p}", texto):
                fugas.append(f"la observacion trae la etiqueta humana '{clave}' (palabra '{p}')")
                break
    return fugas


def guardian_de_recompensa(terminos):
    """BLOQUEA si la señal que Diego recibe depende de algo que no sea su propio error de
    prediccion.

    Recibe la lista de nombres de los terminos que componen la señal. El unico admisible es el
    error de prediccion propio. Cualquier otro —'ley_correcta', 'se_parece_a_newton', 'objetivo
    cumplido'— es un criterio NUESTRO, y meterlo seria enseñarle nuestra fisica sin decirsela."""
    fugas = []
    for t in (terminos or []):
        if str(t) != "error_de_prediccion_propio":
            fugas.append(f"la recompensa incluye el termino ajeno '{t}': depende de un criterio "
                         f"nuestro y no de si el mundo le dio la razon")
    if not terminos:
        fugas.append("la recompensa no declara ningun termino: no se puede comprobar de que "
                     "depende, y una señal que no se puede auditar no vale")
    return fugas


# ------------------------------------------------------------------ la moneda
def _historia(mundo, pasos=400, semilla=7):
    """Una vida: acciones al azar, y lo que el mundo hizo con ellas."""
    rng = np.random.default_rng(int(semilla))
    obs, acc = [mundo.observar()], []
    for _ in range(pasos):
        a = rng.normal(0, 1.0, 3)
        acc.append(a)
        obs.append(mundo.paso(a))
    return np.array(obs), np.array(acc)


def _error_persistencia(obs, h=HORIZONTE):
    """LA LINEA BASE TONTA: 'dentro de h pasos vere lo que veo ahora'."""
    return float(np.mean((obs[h:] - obs[:-h]) ** 2))


def _error_con_estado(obs, acc, h=HORIZONTE):
    """Un predictor que SI usa el estado del mundo y las acciones: ajuste lineal de la observacion
    futura sobre la actual mas las acciones. No es listo — es lo minimo por encima de tonto."""
    n = len(obs) - h
    A = np.column_stack([obs[:n], acc[:n], np.ones(n)])
    Y = obs[h:h + n]
    corte = int(n * 0.7)
    w, *_ = np.linalg.lstsq(A[:corte], Y[:corte], rcond=None)
    return float(np.mean((A[corte:] @ w - Y[corte:]) ** 2))


def ventaja(acoplamiento=1.0, semilla=50, pasos=400):
    """Cuanto le gana el predictor con estado a la persistencia, en error relativo. Fuera de
    muestra: se ajusta en el 70% de la historia y se mide en el 30% que no vio."""
    m = Mundo(semilla=semilla, acoplamiento=acoplamiento)
    obs, acc = _historia(m, pasos=pasos, semilla=semilla + 1)
    e_tonto = _error_persistencia(obs)
    e_listo = _error_con_estado(obs, acc)
    if e_tonto <= 0:
        return 0.0
    return float(max(0.0, 1.0 - e_listo / e_tonto))


def _metodo_medir(acoplamiento=1.0):
    """PASO 1 — la medida escalar: la ventaja sobre la linea base tonta."""
    return float(ventaja(acoplamiento=float(acoplamiento)))


def _metodo_sanidad():
    """PASO 3 — LA FICHA. La pregunta: **¿el cuerpo alcanza este mundo?** Es el chequeo que faltaba
    el 10-ago y por el que el tacto de Diego llevaba meses apagado sin que nadie lo supiera."""
    fallos = []
    m = Mundo()
    dentro = all(ALCANCE[e][0] <= m.pos[i] <= ALCANCE[e][1]
                 for i, e in enumerate(("x", "y", "z")))
    if not dentro:
        fallos.append(f"EL CUERPO NO ALCANZA EL MUNDO: el objeto nace en {m.pos.tolist()} y el "
                      f"alcance medido es {ALCANCE}")
    # y que el objeto se quede dentro tambien despues de moverse
    obs, _ = _historia(Mundo(), pasos=200)
    for i, e in enumerate(("x", "y", "z")):
        lo, hi = ALCANCE[e]
        if obs[:, i].min() < lo - 1e-9 or obs[:, i].max() > hi + 1e-9:
            fallos.append(f"el objeto sale del alcance en el eje {e}: "
                          f"[{obs[:, i].min():.3f}, {obs[:, i].max():.3f}] fuera de {(lo, hi)}")
    return {"aprueba": not fallos, "fallos": fallos,
            "posicion_inicial": [round(float(v), 4) for v in m.pos],
            "alcance_medido": {k: v for k, v in ALCANCE.items() if k != "medido"}}


def regla31(verbose=True):
    """LA REGLA 31 — sobre MI PROCEDIMIENTO, los DOS lados, y NUNCA sobre lo que Diego aprenda.

    Los dos guardianes de la Regla 27 se prueban INYECTANDO LA VIOLACION QUE DEBEN CAZAR, porque
    un guardian que nunca se ha visto saltar es decoracion."""
    fallos = []

    def caso(nombre, ok, extra=""):
        if verbose:
            print(f"  {'ok  ' if ok else 'FALLO'} {nombre}" + (f"  [{extra}]" if extra else ""))
        if not ok:
            fallos.append(nombre)

    if verbose:
        print("== REGLA 31 del prereg-50: el mundo como instrumento ==")

    fs = _metodo_sanidad()
    caso("CONTROL POSITIVO: el cuerpo alcanza el mundo (medido, no supuesto)",
         fs["aprueba"], str(fs["posicion_inicial"]))

    # EL MUNDO PERSISTE: dos historias distintas dejan estados distintos.
    a, b = Mundo(semilla=50), Mundo(semilla=50)
    _historia(a, pasos=100, semilla=1)
    _historia(b, pasos=100, semilla=2)
    caso("el mundo PERSISTE: dos historias distintas dan estados distintos",
         not np.allclose(a.pos, b.pos), f"{a.pos.round(3).tolist()} vs {b.pos.round(3).tolist()}")

    # GUARDIAN DE ETIQUETAS, los dos lados
    limpio = guardian_de_etiquetas({"c0": 1.0, "c1": 2.0})
    sucio = guardian_de_etiquetas({"c0": 1.0, "masa_del_objeto": 2.0})
    caso("GUARDIAN DE ETIQUETAS: no marca un vector sin nombres", limpio == [])
    caso("GUARDIAN DE ETIQUETAS: SI marca una etiqueta humana inyectada a proposito",
         len(sucio) == 1, str(sucio))

    # GUARDIAN DE RECOMPENSA, los dos lados
    ok_r = guardian_de_recompensa(["error_de_prediccion_propio"])
    mal_r = guardian_de_recompensa(["error_de_prediccion_propio", "se_parece_a_newton"])
    vacio_r = guardian_de_recompensa([])
    caso("GUARDIAN DE RECOMPENSA: no marca la señal legitima", ok_r == [])
    caso("GUARDIAN DE RECOMPENSA: SI marca un criterio nuestro inyectado a proposito",
         len(mal_r) == 1, str(mal_r))
    caso("GUARDIAN DE RECOMPENSA: marca una recompensa que no declara sus terminos",
         len(vacio_r) == 1)

    # BASE DISTINTA DE CERO: comparar dos ceros no prueba nada. Quinta vez que lo escribo.
    v = _metodo_medir()
    caso("la lectura base NO es cero", v > 0, f"{v:.4f}")

    if verbose:
        print("\nREGLA 31: " + ("APRUEBA — el mundo es un instrumento legitimo."
                                if not fallos else f"REPRUEBA en {fallos}"))
    return 0 if not fallos else 1


def correr(salida=None, verbose=True):
    datos = {"prerregistro": 50, "alcance_medido": {k: v for k, v in ALCANCE.items()
                                                    if k != "medido"}}
    fs = _metodo_sanidad()
    datos["A_cuerpo_alcanza"] = fs

    a, b = Mundo(semilla=50), Mundo(semilla=50)
    _historia(a, pasos=100, semilla=1)
    _historia(b, pasos=100, semilla=2)
    datos["B_persistencia"] = {"estado_historia_1": a.estado(), "estado_historia_2": b.estado(),
                              "distintos": bool(not np.allclose(a.pos, b.pos))}

    v_vivo = ventaja(acoplamiento=1.0)
    v_muerto = ventaja(acoplamiento=0.0)
    rng = np.random.default_rng(500)
    m = Mundo()
    obs, acc = _historia(m, pasos=400, semilla=51)
    e_tonto = _error_persistencia(obs)
    e_azar = float(np.mean((rng.normal(0, float(np.std(obs)), obs[HORIZONTE:].shape)
                            - obs[HORIZONTE:]) ** 2))
    datos["C_ventaja_mundo_vivo"] = round(v_vivo, 4)
    datos["D_ventaja_mundo_muerto"] = round(v_muerto, 4)
    datos["E_predictor_al_azar"] = {"error_azar": round(e_azar, 4),
                                    "error_linea_base_tonta": round(e_tonto, 4),
                                    "el_azar_pierde": bool(e_azar > e_tonto)}

    datos["F_etiquetas"] = {"limpio": guardian_de_etiquetas({"c0": 1.0, "c1": 2.0}),
                            "con_violacion_inyectada":
                                guardian_de_etiquetas({"masa_del_objeto": 2.0})}
    datos["G_recompensa"] = {"legitima": guardian_de_recompensa(["error_de_prediccion_propio"]),
                             "con_violacion_inyectada":
                                 guardian_de_recompensa(["se_parece_a_newton"])}

    datos["criterios"] = {
        "A_cuerpo_alcanza_el_mundo": bool(fs["aprueba"]),
        "B_el_mundo_persiste": bool(datos["B_persistencia"]["distintos"]),
        "C_la_moneda_discrimina": bool(v_vivo >= MARGEN_C),
        "D_nulo_mundo_muerto": bool(v_muerto <= TECHO_MUERTO),
        "E_el_azar_pierde": bool(e_azar > e_tonto),
        "F_regla27_etiquetas": bool(not datos["F_etiquetas"]["limpio"]
                                    and datos["F_etiquetas"]["con_violacion_inyectada"]),
        "G_regla27_recompensa": bool(not datos["G_recompensa"]["legitima"]
                                     and datos["G_recompensa"]["con_violacion_inyectada"]),
    }

    if not (datos["criterios"]["F_regla27_etiquetas"]
            and datos["criterios"]["G_regla27_recompensa"]):
        datos["veredicto"] = ("SE DESCARTA EL MUNDO — la Regla 27 no queda cerrada, y no hay "
                              "version casi limpia de la Regla 27")
    elif not datos["criterios"]["A_cuerpo_alcanza_el_mundo"]:
        datos["veredicto"] = ("SE DETIENE — el cuerpo no alcanza el mundo, que es el error del "
                              "INFORME-57 repetido")
    elif all(datos["criterios"].values()):
        datos["veredicto"] = ("MUNDO EN PIE — persiste, el cuerpo lo alcanza, la moneda "
                              "discrimina y la Regla 27 queda cerrada por dos guardianes")
    else:
        fallan = [k for k, v in datos["criterios"].items() if not v]
        datos["veredicto"] = "NO CONCLUYENTE — fallan " + ", ".join(fallan)

    if salida:
        ruta = os.path.join(BASE, salida)
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
    if verbose:
        print(f"\nVEREDICTO: {datos['veredicto']}")
    return datos


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Prerregistro 50: el mundo persistente")
    ap.add_argument("--regla31", action="store_true")
    ap.add_argument("--salida", default="resultados/p50-mundo/medida.json")
    a = ap.parse_args()
    if a.regla31:
        sys.exit(regla31())
    _d = correr(salida=a.salida)
    # SALE CON ERROR SI ALGUN CRITERIO FALLA, y muy en particular los dos de la Regla 27. Sin
    # esto, la meta-auditoria podria dañar los guardianes de etiquetas o de recompensa y el modulo
    # seguiria diciendo "todo bien" con codigo 0 — que es la definicion de guardian decorativo.
    sys.exit(0 if all(_d["criterios"].values()) else 1)
