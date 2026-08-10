# pruebas.py — EL BANCO DE PRUEBAS CONGELADO (exigido por la Regla 30; construido 12-jul-2026).
# Toda modificacion de codigo (humana o por propuesta de la mente) debe pasar este banco
# ANTES del commit. Los casos son sinteticos y FIJOS: no se tocan jamas — solo se agregan.
# Uso: python pruebas.py   (salida: OK total o el detalle del fallo; codigo de salida 0/1)

import os
import sys
import json
import tempfile

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from descubrir import preparar, dividir_por_tiempo, error_linea_base, error_rival_lineal, _mse_suma
from autopsia import evaluar, piso_de_ruido
from canonizar import tarjeta

FALLOS = []


def caso(nombre, cond, detalle=""):
    if cond:
        print(f"  ok  {nombre}")
    else:
        print(f"FALLO {nombre} {detalle}")
        FALLOS.append(nombre)


def csv_temporal(contenido):
    f = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, newline="")
    f.write(contenido); f.close()
    return f.name


print("== preparar: formas, retardos, suavizado, objetivo crudo ==")
# senal lineal s(t)=2t: cambios constantes=2; con 12 muestras
csv1 = csv_temporal("t,s1\n" + "\n".join(f"{t},{2*t}" for t in range(12)))
X, Y = preparar(csv1)
caso("forma base 1 senal", X.shape[1] == 2 and Y.shape[1] == 1, f"{X.shape}")
caso("cambio correcto", np.allclose(X[:, 1], 2.0))
caso("objetivo = siguiente", np.allclose(Y[:, 0], X[:, 0] + 2.0))
X2, Y2 = preparar(csv1, retardos=2)
caso("retardos agregan columnas", X2.shape[1] == 4, f"{X2.shape}")
caso("retardo-1 correcto", np.allclose(X2[:, 2], X2[:, 0] - 2.0))
X3, Y3 = preparar(csv1, suavizar=3)
caso("suavizado: objetivo sigue CRUDO (lineal exacto)", np.allclose(Y3[:, 0] - (X3[:, 0] + 2.0), 0.0, atol=1e-9),
     "el suavizado toco al objetivo (leccion INF-11 violada)")

print("== varas: base trivial y rival lineal ==")
rng = np.random.default_rng(7)
Xs = rng.normal(size=(200, 4)); Ys = np.column_stack([Xs[:, 0] + Xs[:, 2], Xs[:, 1] + Xs[:, 3]])
caso("base velocidad exacta cuando el mundo ES velocidad",
     error_linea_base(Xs, Ys) < 1e-20)
caso("rival lineal aprende el mapa lineal",
     error_rival_lineal(Xs[:100], Ys[:100], Xs[100:], Ys[100:]) < 1e-10)
caso("_mse_suma = suma por senal",
     abs(_mse_suma(np.zeros((5, 2)), np.ones((5, 2))) - 2.0) < 1e-12)

print("== autopsia: piso de ruido y evaluar ==")
ruido = rng.normal(0, 3.0, size=5000)
piso = piso_de_ruido(np.cumsum(rng.normal(size=5000)) + ruido)  # camino suave + ruido sigma=3
caso("piso ~ var del ruido (9.0)", 6.0 < piso < 12.5, f"piso={piso:.2f}")
caso("evaluar respeta v-indices", np.allclose(evaluar("v1 + 2*v3", np.array([[1., 0., 5., 0.]])), 11.0))

print("== surrogado IAAFT: la falsificacion perfecta ==")
from descubrir import _iaaft
rng2 = np.random.default_rng(3)
# senales de banda ancha (camino aleatorio suavizado) acopladas — caso realista;
# con ondas puras monocromaticas la decorrelacion por fases es debil por naturaleza
s1 = np.convolve(rng2.normal(size=2100), np.ones(8) / 8, mode="valid")[:2000]
s2 = 0.8 * np.roll(s1, 3) + 0.1 * rng2.normal(size=2000)  # acoplada a s1
f1 = _iaaft(s1, rng2)
esp_o = np.abs(np.fft.rfft(s1)); esp_f = np.abs(np.fft.rfft(f1))
caso("surrogado conserva el espectro",
     np.corrcoef(esp_o, esp_f)[0, 1] > 0.99, f"corr={np.corrcoef(esp_o, esp_f)[0,1]:.3f}")
caso("surrogado conserva la distribucion", np.allclose(np.sort(f1), np.sort(s1)))
f2 = _iaaft(s2, rng2)
c_orig = abs(np.corrcoef(s1, s2)[0, 1]); c_surr = abs(np.corrcoef(f1, f2)[0, 1])
caso("surrogado DESTRUYE el acople entre senales",
     c_surr < c_orig * 0.35, f"original={c_orig:.2f} surrogado={c_surr:.2f}")

print("== REGLA 31 (agregado 8-ago-2026): el criterio completo A+B de conservada ==")
# Caso congelado: replicas de ruido SUAVIZADO e independientes (nada conservado, nada
# compartido). Con el nulo viejo (barajado) el criterio completo de los prerregistros
# 16-17 ACEPTABA este mundo vacio (score 0.0004 y jueces < 0.2 — habria parido un nodo).
# Con surrogado (IAAFT) los JUECES lo rechazan. Leccion tallada aqui: en senales no
# estacionarias el score de entrenamiento (nivel A) puede sobreajustar; el verdugo
# decisivo es el nivel B con nulo surrogado.
import tempfile as _tmp, shutil as _sh
from regla31_conservada import mundo_vacio as _mv, mundo_lleno as _ml, \
    escribir_replicas as _er, correr_mundo as _cm
# Parametros IDENTICOS a la corrida oficial de regla31_conservada.py (6 replicas, T=600,
# 20 corridas nulas): miniaturizarlo hace trampas — con 2 replicas de entrenamiento y senos
# monocromaticos, el surrogado conserva una combinacion por accidente (leccion documentada).
_dir31 = _tmp.mkdtemp(prefix="p31_")
_csvs_v = _er(os.path.join(_dir31, "v"), _mv(np.random.default_rng(12345)))
_csvs_l = _er(os.path.join(_dir31, "l"), _ml(np.random.default_rng(54321)))
_sv, _nv, _jv = _cm(_csvs_v, "surrogado", 20)
caso("surrogado: el mundo vacio NO pare nodo",
     not (_nv > 0 and _jv), f"score={_sv:.4g} serias={_nv} jueces={_jv}")
_sb, _nb, _jb = _cm(_csvs_v, "barajado", 20)
caso("barajado daba 5 'serias' en el mundo vacio (defecto historico documentado)",
     _nb > 0, f"score={_sb:.4g} serias={_nb}")
_sl, _nl, _jl = _cm(_csvs_l, "surrogado", 20)
caso("surrogado: el mundo lleno SI pare nodo (s1^2+s2^2 encontrada)",
     _nl > 0 and _jl, f"score={_sl:.4g} serias={_nl} jueces={_jl}")
_sh.rmtree(_dir31, ignore_errors=True)

print("== GEN G2 (curiosidad2, metrica 18b FIRMADA): aburrimiento, frescura, records limpios ==")
# NOTA DE GOBERNANZA: estos casos REEMPLAZAN a los del prereg-18 original (8-ago-2026) porque
# prueban la metrica: la 18a fracaso su backtest (INFORME-21) y la 18b fue firmada por el
# director. El ESPIRITU del caso (Regla 31 del gen: sin progreso -> aburrimiento; jamas
# interes inventado) es identico y queda congelado aqui.
from curiosidad2 import prioridades as _prio, UMBRAL as _umb, H as _H
_prefijos = ["oficial-trial1", "peldano2-pendulo46", "dp-morpheus", "p13-latente",
             "caida-libre", "conservadas-x"]
# memoria plana LARGA: dos pasadas por todas las regiones con el MISMO g — los records de
# todas quedan viejos (mas alla del horizonte H) y nada progresa.
_mem_plana = [{"campana": p, "lo_trivial": 4.0, "mi_mejor_esfuerzo": 1.0}
              for _v in range(3) for p in _prefijos]
_pp = _prio(_mem_plana)
caso("memoria sin progreso -> aburrimiento universal (todas <= umbral)",
     all(p <= _umb for p in _pp.values()), f"{_pp}")
_mem_viva = list(_mem_plana) + [{"campana": "oficial-trial1", "lo_trivial": 4.0, "mi_mejor_esfuerzo": 0.25}]
_pv = _prio(_mem_viva)
caso("record que mejora -> progreso positivo SOLO en su region",
     _pv["mendeley"] > _umb and all(_pv[r] <= _umb for r in _pv if r != "mendeley"), f"{_pv}")
# frescura: un record ganado hace mas de H eventos ya no cuenta como progreso
_mem_rancia = list(_mem_viva) + [{"campana": p, "lo_trivial": 4.0, "mi_mejor_esfuerzo": 1.0}
                                 for p in _prefijos[:1] * _H]
_pr = _prio(_mem_rancia)
caso("frescura 18b: el record viejo deja de contar como progreso",
     _pr["mendeley"] <= _umb, f"mendeley={_pr['mendeley']}")
# records limpios: una corrida interna (-inner-) con g gigante NO mueve el record
_mem_inner = list(_mem_plana) + [{"campana": "p14-inner-d4", "lo_trivial": 100.0, "mi_mejor_esfuerzo": 0.001}]
_pi = _prio(_mem_inner)
caso("records limpios 18b: las corridas internas no mueven records",
     _pi["dp-latentes-propios"] <= _umb, f"dp-latentes={_pi['dp-latentes-propios']}")

print("== GEN G10 (interocepcion) + el defecto de Goodhart de G2 ==")
# Regla 31 del gen G10: el coste sentido debe CRECER con el esfuerzo y con el territorio,
# y jamas ser constante (un coste plano es el denominador falso que veniamos arrastrando).
from interocepcion import trabajo_del_motor as _tm
caso("G10: mas semillas -> mas coste", _tm(10, 400, 20) > _tm(5, 400, 20))
caso("G10: mas iteraciones -> mas coste", _tm(5, 800, 20) > _tm(5, 400, 20))
caso("G10: la campana unidad vale 1.0", abs(_tm(5, 400, 20) - 1.0) < 1e-9)
caso("G10: el coste NO es constante (el denominador dejo de ser falso)",
     len({_tm(2, 400, 12), _tm(5, 400, 20), _tm(5, 800, 25)}) == 3)

# EL CANAL DE GOODHART Nº2, demostrado en NUESTROS PROPIOS DATOS (ECUACIONES-COMPARADAS §4.2):
# una region que OLVIDA y REAPRENDE farmea interes para siempre si el progreso se recorta con
# max(0,...). Con progreso CON SIGNO, el ciclo se cancela. Caso congelado: es la razon por la
# que la ecuacion de G2 debe corregirse (prerregistro-20).
def _lp_recortado(serie, H):
    return max(0.0, serie[-1] - (serie[-1 - H] if len(serie) > H else 0.0))
def _lp_con_signo(serie, H):
    return serie[-1] - (serie[-1 - H] if len(serie) > H else 0.0)
_oscila = [0.0, 0.5, 0.9, 0.4, 0.9, 0.4, 0.9]      # aprende, olvida, reaprende...
caso("G2/Goodhart nº2: el recorte max(0,.) PREMIA olvidar-y-reaprender",
     _lp_recortado(_oscila, 1) > 0.4, f"lp={_lp_recortado(_oscila,1):.3f}")
caso("G2/Goodhart nº2: el progreso CON SIGNO cancela el ciclo (sobre la vuelta completa)",
     abs(_lp_con_signo(_oscila, 2)) < 1e-9, f"lp={_lp_con_signo(_oscila,2):.3f}")

print("== GANANCIA HONESTA: el instrumento que separa dinamica de textura ==")
# Nace de convertir un fracaso en medidor (INFORME-27). Casos congelados: debe dar ~0 donde
# solo hay textura y >0 donde hay acople real. Si deja de distinguirlos, no puede opinar
# sobre ninguna representacion y el banco lo grita.
from ganancia_honesta import regla31 as _gh31, reduccion as _red
caso("ganancia honesta: reduccion bien definida", abs(_red(1.0, 0.25) - 0.75) < 1e-12)
caso("ganancia honesta: APRUEBA su Regla 31 (separa textura de dinamica)", _gh31() == 0)
# MEDIDO el 8-ago-2026: un solo sorteo de surrogado varia +-0.015 — reportar uno es elegir el
# que salio. La medicion DEBE traer su desviacion o no es medicion.
import inspect as _insp
from ganancia_honesta import medir as _gm
caso("ganancia honesta: promedia N surrogados (no un solo sorteo)",
     _insp.signature(_gm).parameters["surrogados"].default >= 5)
caso("ganancia honesta: reporta su DESVIACION junto al numero",
     "ganancia_honesta_desv" in _insp.getsource(_gm))
# G10: una sensacion anulada o sin tiempo fiable no puede alimentar decisiones
from interocepcion import coste_de as _cd
caso("G10: sin tiempo fiable, coste_de devuelve None (no inventa)",
     _cd("p14-final") is None)

print("== dimension intrinseca: TwoNN y participacion ==")
from dimension import twonn, participacion
_rngD = np.random.default_rng(4)
# curva 1-D (circulo) embebida en 4 dimensiones: TwoNN debe decir ~1, participacion ~2
_t = _rngD.uniform(0, 2 * np.pi, 800)
_C = np.column_stack([np.cos(_t), np.sin(_t), 0.5 * np.cos(_t), -0.2 * np.sin(_t)])
_d1 = twonn(_C + _rngD.normal(0, 1e-4, _C.shape))
caso("TwoNN ~1 en una curva embebida en 4D", _d1 is not None and 0.7 < _d1 < 1.5, f"d={_d1}")
# nube llena en 3D: TwoNN ~3
_N3 = _rngD.normal(size=(800, 3))
_d3 = twonn(_N3)
caso("TwoNN ~3 en nube llena 3D", _d3 is not None and 2.4 < _d3 < 3.7, f"d={_d3}")
caso("participacion ~3 en nube llena 3D", 2.5 < participacion(_N3) <= 3.05, f"pr={participacion(_N3):.2f}")

print("== LOS DOS CANALES DE MENTIRA DE LA GANANCIA HONESTA (medidos el 8-ago-2026) ==")
# Estos casos NO celebran el instrumento: congelan sus LIMITES, medidos con mundos de verdad
# conocida. Nacen de tres arreglos propuestos que fracasaron uno tras otro (INFORME-30).
import tempfile as _tf, shutil as _sh
from ganancia_honesta import medir as _medir
_tmpd = _tf.mkdtemp(prefix="lim_banco_")
try:
    def _mundo(nombre, reps):
        c = os.path.join(_tmpd, nombre); os.makedirs(c, exist_ok=True)
        for i, (a, b) in enumerate(reps, 1):
            with open(os.path.join(c, f"r{i}.csv"), "w") as f:
                f.write("t,x_px,y_px\n")
                for t_ in range(len(a)):
                    f.write(f"{t_},{a[t_]:.6f},{b[t_]:.6f}\n")
        return c
    _n = 900
    _k9 = np.ones(9) / 9
    _rg = np.random.default_rng(5)
    _t = np.arange(_n)
    # CANAL 1 — FALSO POSITIVO: dos paseos aleatorios INDEPENDIENTES (cero ley) fabrican
    # ganancia honesta porque el IAAFT es circular y destruye la deriva que el real conserva.
    _paseo = [(np.convolve(np.cumsum(_rg.normal(size=_n + 8)), _k9, mode="valid")[:_n],
               np.convolve(np.cumsum(_rg.normal(size=_n + 8)), _k9, mode="valid")[:_n])
              for _ in range(6)]
    _g_falso = _medir(_mundo("paseo", _paseo), [3], surrogados=4, suavizar=3, retardos=2)
    caso("ganancia honesta MIENTE con señales integradas sin ley (canal conocido)",
         _g_falso["ganancia_honesta"] > 0.05,
         f"si este caso se pone rojo el canal se cerro: revisar INFORME-30 (dio {_g_falso['ganancia_honesta']:+.3f})")
    # CANAL 2 — FALSO NEGATIVO: una ley determinista vista con 0.5% de ruido de seguimiento
    # pierde casi toda su ganancia. El instrumento no puede certificar datos de camara real.
    def _osc(ruido):
        r = []
        for j in range(6):
            w = 0.06 + 0.004 * j
            x = 40 * np.cos(w * _t + _rg.uniform(0, 6.3)) + _rg.normal(0, ruido, _n)
            y = 40 * np.sin(1.9 * w * _t + _rg.uniform(0, 6.3)) + _rg.normal(0, ruido, _n)
            r.append((x, y))
        return r
    _limpio = _medir(_mundo("limpio", _osc(0.0)), [3], surrogados=4, suavizar=3, retardos=2)
    _sucio = _medir(_mundo("sucio", _osc(0.4)), [3], surrogados=4, suavizar=3, retardos=2)
    caso("ganancia honesta ve la ley cuando NO hay ruido",
         _limpio["ganancia_honesta"] > 0.10, f"{_limpio['ganancia_honesta']:+.3f}")
    caso("ganancia honesta PIERDE la misma ley con 1% de ruido (canal conocido)",
         _sucio["ganancia_honesta"] < _limpio["ganancia_honesta"] / 2,
         f"limpio {_limpio['ganancia_honesta']:+.3f} vs sucio {_sucio['ganancia_honesta']:+.3f}")
    # LA CONSECUENCIA: los dos canales juntos hacen que (niveles alto, incrementos ~0) sea
    # AMBIGUO — compatible con 'paseo sin ley' Y con 'ley a traves de camara ruidosa'.
    caso("el par (niveles, incrementos) NO desambigua: queda registrado como limite",
         "AMBIGUO" in open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        "ganancia_honesta.py"), encoding="utf-8").read())
finally:
    _sh.rmtree(_tmpd, ignore_errors=True)

print("== horizonte: retrocompatibilidad exacta ==")
from descubrir import preparar as _prep
_csvh = os.path.join(_tmpd, "x")  # ruta ya borrada: se usa un csv sintetico en memoria
import tempfile as _tf2
_fd = _tf2.mkdtemp(prefix="hz_")
_p = os.path.join(_fd, "a.csv")
with open(_p, "w") as _f:
    _f.write("t,s1,s2\n")
    for _i in range(300):
        _f.write(f"{_i},{np.sin(_i*0.1):.6f},{np.cos(_i*0.07):.6f}\n")
_X1, _Y1 = _prep(_p, suavizar=3, retardos=2)
_X2, _Y2 = _prep(_p, suavizar=3, retardos=2, horizonte=1)
caso("horizonte=1 reproduce EXACTAMENTE el comportamiento historico",
     np.array_equal(_X1, _X2) and np.array_equal(_Y1, _Y2))
_X4, _Y4 = _prep(_p, suavizar=3, retardos=2, horizonte=4)
caso("horizonte=4 predice 4 cuadros al futuro (Y desplazada, no recortada al azar)",
     len(_Y4) == len(_Y1) - 3 and abs(_Y4[0, 0] - _Y1[3, 0]) < 1e-12)
_sh.rmtree(_fd, ignore_errors=True)

print("== contingencia (G4): el detector de la frontera yo/mundo ==")
# Congela las DOS lecciones que costaron una tarde de corridas contra el simulador:
# (1) a un cuadro vista un cuerpo es casi invisible -> el horizonte importa;
# (2) un objeto manipulable TAMBIEN es contingente -> lo que separa es la CONSISTENCIA.
from contingencia import medir as _cmedir, _mundos_regla31 as _cmundos
_cm = _cmundos(n_ep=14, T=1600, semilla=3)
_cjueces = [13, 14]
_sin_ag = _cm["1 SIN AGENCIA (motores desconectados)"][0]
_pos = _cm["2 CONTROL POSITIVO (solo la var 0 obedece)"][0]
_trampa = _cm["4 DERIVA FUERTE, CERO AGENCIA (la trampa del INF-30)"][0]
_r_sin = _cmedir(_sin_ag, _cjueces, nulos=5, horizonte=8, ventana=150)
_r_pos = _cmedir(_pos, _cjueces, nulos=5, horizonte=8, ventana=150)
_r_tra = _cmedir(_trampa, _cjueces, nulos=5, horizonte=8, ventana=150)
caso("contingencia: NO inventa cuerpo donde los motores estan desconectados",
     not any(r["es_mia"] for r in _r_sin),
     str([r["variable"] for r in _r_sin if r["es_mia"]]))
caso("contingencia: encuentra EXACTAMENTE el grado de libertad conectado",
     [r["variable"] for r in _r_pos if r["es_mia"]] == [0],
     str([(r["variable"], r["obedece_en"]) for r in _r_pos]))
caso("contingencia: la deriva fuerte con comandos suaves NO fabrica cuerpo (trampa INF-30)",
     not any(r["es_mia"] for r in _r_tra),
     str([r["variable"] for r in _r_tra if r["es_mia"]]))
caso("contingencia: el nulo es DESPLAZAMIENTO circular, no barajado (regla 31 enmendada)",
     "roll" in _insp.getsource(__import__("contingencia")._desplazar))
# HUECO CAZADO POR EL PROPIO BANCO (8-ago-2026): con pocas ventanas el criterio firmado
# fabrica cuerpo donde no lo hay. Ahora la medicion se NIEGA a opinar bajo el minimo.
try:
    _cmedir(_cmundos(n_ep=6, T=300, semilla=3)["1 SIN AGENCIA (motores desconectados)"][0],
            [5, 6], nulos=2, horizonte=8, ventana=150)
    _rechaza = False
except SystemExit:
    _rechaza = True
caso("contingencia: se NIEGA a medir con menos ventanas del minimo (no opina sin potencia)",
     _rechaza)
caso("contingencia: sus constantes las fija el prerregistro-23, no el codigo",
     "PRERREGISTRO-23" in _insp.getsource(_cmedir) and "SIN AJUSTAR" in _insp.getsource(_cmedir))

print("== verdugo por reescalado: le importa la escala o no ==")
# Congela las DOS versiones que se cayeron antes de la que sirve (INFORME-32):
# comparar contra la base trivial dejaba un mundo SIN LEY a 0.484 de un umbral de 0.5, y un nulo
# con el tiempo revuelto era tan destructivo que TODO lo superaba.
from verdugo_escala import sensibilidad_de_escala as _sens, regla31 as _ve31
_tt = np.arange(400)
_caida = lambda k: [np.column_stack([k * (5.0 - 0.5 * 0.004 * (_tt + f) ** 2) for f in (0, 7, 13)])
                    for _ in range(6)]
_rngE = np.random.default_rng(11)
_paseo = lambda k: [np.column_stack([k * np.cumsum(_rngE.normal(size=400)) for _ in range(3)])
                    for _ in range(6)]
_con = _sens(_caida(1.0), _caida(3.0), 3.0, 1.0)
_sin = _sens(_paseo(1.0), _paseo(3.0), 3.0, 1.0)
caso("verdugo escala: un mundo CON ley es sensible a la escala",
     _con["sensibilidad"] > 0.5 and _con["sobrevive"], f"{_con['sensibilidad']:+.3f}")
caso("verdugo escala: un mundo SIN ley NO es sensible a la escala",
     abs(_sin["sensibilidad"]) < 0.05 and not _sin["sobrevive"], f"{_sin['sensibilidad']:+.4f}")
caso("verdugo escala: la persistencia sola YA transfiere (por eso la vara vieja no servia)",
     0.3 < _sin["transferencia_escala_deshecha"] < 0.7,
     f"{_sin['transferencia_escala_deshecha']:.3f} — si esto baja de 0.3 revisar INFORME-32")
caso("verdugo escala: APRUEBA su Regla 31", _ve31(verbose=False) == 0)

print("== G13 (poder) y G14 (incertidumbre): activados por el director, congelados aqui ==")
from poder import regla31 as _p31, medir as _pmedir
from incertidumbre import regla31 as _i31, medir as _imedir
caso("G13 poder: APRUEBA su Regla 31 (control real, no varianza ni casualidad)", _p31(verbose=False) == 0)
# (corregido en el acto: la primera version de este caso terminaba en "or True" — un caso que
# no puede fallar es decoracion, no vigilancia)
_src_poder = _insp.getsource(__import__("poder"))
caso("G13 poder: es MEDIDOR — no importa curiosidad2 ni escribe en la cola de estudios",
     "import curiosidad2" not in _src_poder and "COLA-ESTUDIOS" not in _src_poder)
caso("G14 incertidumbre: APRUEBA su Regla 31 (separa 'es azar' de 'aun no aprendo')", _i31(verbose=False) == 0)
# la firma falsable de G14, congelada como numero: doblar datos reduce la epistemica
_rngU = np.random.default_rng(9)
_XU = _rngU.normal(size=(12, 2)); _YU = 2 * _XU[:, 0] - _XU[:, 1] + _rngU.normal(0, 0.5, 12)
_XU2 = _rngU.normal(size=(48, 2)); _YU2 = 2 * _XU2[:, 0] - _XU2[:, 1] + _rngU.normal(0, 0.5, 48)
_XtU = _rngU.normal(size=(200, 2))
_eA = _imedir(_XU, _YU, _XtU); _eB = _imedir(_XU2, _YU2, _XtU)
caso("G14: la ignorancia curable CAE al doblar los datos (su firma falsable)",
     _eB["epistemica"] < 0.7 * _eA["epistemica"],
     f"{_eA['epistemica']:.3f} -> {_eB['epistemica']:.3f}")

print("== los sistemas del plan biologico: sueño, atencion, filogenia (Reglas 31 rapidas) ==")
from sueno import regla31 as _s31
from atencion import regla31 as _a31, repartir as _rep
from filogenia import regla31 as _f31, torneo as _torneo
caso("G9 sueño: APRUEBA su Regla 31 (sueña donde hay algo, calla donde no)", _s31(verbose=False) == 0)
caso("G8 atencion: APRUEBA su Regla 31 (la fovea huye del televisor)", _a31(verbose=False) == 0)
caso("Regla 33 filogenia: el estadio empata gemelos y corona oraculos", _f31(verbose=False) == 0)
# la propiedad anti-Goodhart de la atencion, congelada como numero:
_regs = [{"id": "tv", "epistemica": 0.05, "aleatoria": 5.0, "poder": 0.0, "coste": 10},
         {"id": "buena", "epistemica": 0.8, "aleatoria": 0.1, "poder": 0.5, "coste": 10}]
_r = {x["id"]: x["asignado"] for x in _rep(_regs, presupuesto=10)}
caso("atencion: la varianza pura NO compra fovea (anti-televisor por construccion)",
     _r["buena"] > 4 * _r["tv"], str(_r))
caso("filogenia: dos puntajes a 0.001 EMPATAN (no se fabrican linajes)",
     _torneo([{"nombre": "a", "puntaje": 0.500}, {"nombre": "b", "puntaje": 0.501}])["veredicto"] == "EMPATE")

print("== la sinapsis: el genoma es portero, no comentario ==")
from sinapsis import regla31 as _sin31, publicar as _pub, SinapsisBloqueada as _SB
caso("sinapsis: APRUEBA su Regla 31 (bloqueos mecanicos de modo)", _sin31(verbose=False) == 0)
import tempfile as _tf3
_tmp3 = _tf3.mktemp(suffix=".jsonl")
try:
    _pub("G14_incertidumbre", "decision", {}, _ruta=_tmp3); _blq = False
except _SB:
    _blq = True
caso("sinapsis: G14 (medidor) no puede decidir ni queriendo", _blq)
import json as _js
_gj = _js.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "arbol", "GENOMA.json"), encoding="utf-8"))
caso("GENOMA.json: todo gen en modo 'decide' tiene prerregistro anotado",
     all(g.get("prerregistro") for g in _gj["genes"].values() if g["modo"] == "decide"))
caso("GENOMA.json: los genes nuevos del dia nacen como MEDIDORES (cuarentena de activacion)",
     all(_gj["genes"][k]["modo"] == "mide" for k in
         ("G13_poder", "G14_incertidumbre", "G8_atencion", "G9_sueno", "G4_contingencia")))

print("== las cinco ecuaciones nuevas (orden del director: implementa todo) ==")
from koopman import regla31 as _k31
from sindy2 import regla31 as _sy31, descubrir as _sydesc
from entropia_transferencia import regla31 as _te31
from energia_libre import regla31 as _el31
from intermodal import regla31 as _im31
caso("Koopman: APRUEBA (halla lo conservado, calla ante lo que decae o vaga)", _k31(verbose=False) == 0)
caso("SINDy: APRUEBA (segundo motor; sin replicacion no hay ley)", _sy31(verbose=False) == 0)
caso("entropia de transferencia: APRUEBA (ve el flujo no lineal que el lineal no ve)", _te31(verbose=False) == 0)
caso("energia libre: APRUEBA (una moneda debajo de todos los impulsos)", _el31(verbose=False) == 0)
caso("espejo intermodal: APRUEBA (refleja al que se mueve, no al que se parece)", _im31(verbose=False) == 0)
caso("SINDy: una ley vacia no es una ley replicada (hueco cazado y congelado)",
     "no es vacío" in _insp.getsource(_sydesc) or "sop_a.sum() == 0" in _insp.getsource(_sydesc))

print("== ranuras: entra al torneo (frontera gris), no al genoma ==")
from ranuras import regla31 as _rn31
caso("ranuras: APRUEBA su Regla 31 (una ranura por cosa, o nada)", _rn31(epocas=3, verbose=False) == 0)
# Se pregunta a la HOJA MECANICA, no al cartel en prosa. Antes esto leia GENOMA-DIEGO.md, que
# desde el 10-ago-2026 vive en registros/ por ser un documento humano — y ademas la prosa no es la
# fuente de verdad: el genoma que se ejecuta es GENOMA.json. Si alguien activara las ranuras de
# verdad, lo haria ahi, no en un parrafo.
import json as _json
_gj = _json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                                   "arbol", "GENOMA.json"), encoding="utf-8"))
caso("ranuras: el genoma EJECUTABLE sigue sin activarlas como gen (solo torneo)",
     "ranuras" not in _json.dumps(_gj, ensure_ascii=False).lower())

print("== SINDy en forma debil + bootstrap (prereg-28): la cura del ruido de sensor ==")
import sindy3 as _s3
caso("sindy3: APRUEBA su Regla 31 (4/4, incluido el oscilador con sensor ruidoso)",
     _s3.regla31(verbose=False) == 0)
# LA LECCION QUE JUSTIFICA EL MODULO, CONGELADA: la derivada numerica muere con 0.5% de ruido de
# sensor; la forma debil sobrevive. Si alguien "simplifica" sindy3 volviendo a derivar, esto grita.
_Xr, _dtr = _s3._oscilador(ruido=0.02)
caso("sindy3: recupera la ley con ruido de sensor donde la derivada numerica ya fracasa",
     _s3._es_la_ley(_s3.descubrir(_Xr, dt=_dtr)) and not (
         lambda l: l is not None and [n for n, _ in l["dx/dt"]] == ["v"]
     )(_sydesc(_Xr, dt=_dtr)))
caso("sindy3: una ley vacia jamas cuenta como replicada (bootstrap sobre ruido puro calla)",
     _s3.descubrir(__import__("numpy").random.default_rng(3).normal(size=(4000, 2)), dt=0.02) is None)

print("== panel de jueces diversos (prereg-31): ningun juez unico corona ==")
import panel_jueces as _pj
caso("panel: APRUEBA su Regla 31 (5/5: gemelos, oraculo, asterisco, ruido, sin suelo)",
     _pj.regla31(verbose=False) == 0)
# EL BUG DE LA CORRIDA 13, CONGELADO: la aptitud vieja recorta el margen a cero con max(.,0),
# asi que CUALQUIER par de representaciones bajo el piso empata en 0.0000 exacto. Si alguien
# vuelve a poner un suelo en el ordenamiento del panel, esto grita.
_cero = _pj.veredicto([{"nombre": "a", "puntajes": {"contingencia": 0.0, "flecha": 0.0,
                                                    "robustez": 0.0}},
                       {"nombre": "b", "puntajes": {"contingencia": 0.0, "flecha": 0.0,
                                                    "robustez": 0.0}}])
caso("panel: cuatro ceros identicos JAMAS producen un ganador (el torneo viejo si lo hacia)",
     "ganador" not in _cero or "EMPATE" in _cero["fallo"])
caso("panel: gana con ASTERISCO quien gana una lectura y pierde otra (no reemplaza los ojos)",
     "ASTERISCO" in _pj.veredicto(
         [{"nombre": "x", "puntajes": {"contingencia": 1.0, "flecha": 0.0, "robustez": 0.0}},
          {"nombre": "y", "puntajes": {"contingencia": 0.0, "flecha": 1.0, "robustez": 1.0}}]
     )["fallo"] or "GANA y" in _pj.veredicto(
         [{"nombre": "x", "puntajes": {"contingencia": 1.0, "flecha": 0.0, "robustez": 0.0}},
          {"nombre": "y", "puntajes": {"contingencia": 0.0, "flecha": 1.0, "robustez": 1.0}}]
     )["fallo"])

print("== la escalera de soporte (prereg-29): el primer no-yo por definicion POSITIVA ==")
import soporte as _sop
caso("soporte: APRUEBA su Regla 31 (11/11: escalones, senuelo, sin gravedad, VOE, nulos, "
     "y el mundo variable del prereg-35)",
     _sop.regla31(verbose=False) == 0)
# EL HALLAZGO DEL INFORME-39, CONGELADO: las 5 semillas de la primera ronda daban cifras IDENTICAS
# porque la semilla movia el balbuceo y no la caida. Estos dos casos exigen que la cura exista Y
# que no haya movido el defecto: lo publicado tiene que seguir valiendo bit a bit.
caso("soporte: el mundo VARIA de verdad por semilla (5 valores distintos de cada parametro)",
     all(len({_sop.mundo_variable(_s)[_k] for _s in range(1, 6)}) == 5
         for _k in _sop.RANGOS_MUNDO))
caso("soporte: sin --variar la escena es la de la primera ronda (nada publicado se movio)",
     _sop.mundo_variable(1) != _sop.MUNDO_FIJO
     and np.array_equal(_sop.escena("cae", semilla=1, pasos=_sop.PASOS_MINIMOS)[1],
                        _sop.escena("cae", semilla=1, pasos=_sop.PASOS_MINIMOS,
                                    mundo=_sop.MUNDO_FIJO)[1]))
# LA LECCION DEL NIVEL B FRACASADO, CONGELADA: definir el no-yo solo como "no me obedece" deja
# entrar al ruido puro. El senuelo de ruido debe ser rechazado por ILEGAL (impredecible), no por
# obediente. Si alguien quita el requisito de legalidad, esto grita.
_c, _x, _n, _k = _sop.escena("cae", semilla=1, pasos=_sop.PASOS_MINIMOS)
_e1 = _sop.escalon1(_c, _x, _n, cortes=_k)
caso("soporte: el ruido puro NO puede ser el primer no-yo (legalidad exigida, no solo ausencia)",
     "ruido" not in (_e1.get("candidatos_aptos") or []) and _e1["candidato"] == "altura")
caso("soporte: sin potencia estadistica no hay veredicto (guarda de pasos minimos)",
     _sop.PASOS_MINIMOS >= 900)

print("== el gemelo y las firmas del bebe (prereg-30): el control de oro del espejo ==")
import espejo2 as _e2
caso("espejo2: APRUEBA su Regla 31 (9/9: gemelo, apariencia, firmas, y el calibrador del "
     "prereg-36)",
     _e2.regla31(verbose=False) == 0)
# LA LECCION DEL INFORME-40, CONGELADA Y SIN SIMULAR NADA: el control positivo del prereg-30
# disparo 2 de 5 en la nube y aun asi el banco lo aprobaba, porque probaba UNA semilla. Un control
# positivo de una sola muestra no es un control positivo. Si alguien vuelve a leer "2/5" como
# instrumento sano, esto grita.
caso("espejo2: con el control positivo en 2/5 la vara se declara NO USABLE (prereg-36)",
     not _e2._veredicto_calibracion(
         [{"pasos_fase": 500, "tasa_control_positivo": 0.4, "tasa_ciega": 0.0,
           "tasa_agitada_especifica": 0.0}])["vara_usable"])
# CONGELADO: el cuerpo del GEMELO jamas puede declararse propio. Si alguien afloja el criterio
# del espejo hasta que la apariencia baste, esto grita.
_up, _ua, _sp, _sa, _ = _e2.escena_gemelo(semilla=1, pasos=1200)
caso("espejo2: el cuerpo del gemelo NO se declara mio (apariencia no basta)",
     not _e2.prueba_gemelo(_sa, _up, _ua)["se_reconoce"]
     and _e2.prueba_gemelo(_sp, _up, _ua)["se_reconoce"])
# CONGELADO: el balbuceo ciego de HOY no puede exhibir la firma conductual. Un instrumento que
# la ve donde no la hay esta midiendo su propio ruido.
caso("espejo2: el balbuceo ciego NO alcanza el criterio 1.5x (control negativo vivo)",
     not _e2.firmas(_e2.paradigma_movil(semilla=2, pasos_fase=400,
                                        politica="ciega"))["criterio_clasico_1.5x"])

print("== la experimentacion dirigida (prereg-37): la primera intervencion de Diego ==")
import experimentar as _ex
caso("experimentar: APRUEBA su Regla 31 (7/7: duda real por los dos lados, tocar la resuelve, "
     "señuelo agitador, mundo sin duda, guarda de potencia)",
     _ex.regla31(verbose=False) == 0)
# CONGELADO: el señuelo del agitador. Tocar MUCHO y sin criterio no puede ganarle a elegir. Sin
# esto, cualquier ventaja de intervenir se confundiria con "actuar informa mas que mirar", que es
# trivial y no dice nada sobre pensar. Sus dos hermanos (el ruido de la escalera, el agitado del
# prereg-36) cazaron fallos reales en su primera corrida.
caso("experimentar: el agitador (toca sin criterio) NO le gana al dirigido",
     _ex.correr("agitador", semilla=1)["puntaje"]
     <= _ex.correr("dirigido", semilla=1)["puntaje"])
# CONGELADO: la medida de "¿se ve la diferencia?" no puede ser ciega. En reposo debe dar ~0 Y con
# una diferencia plantada debe verla. Cazado el 10-ago: agrupar los tres ejes en un solo std medía
# la geometria del montaje (y=+0.16 vs y=-0.16) y daba 0.21 con los objetos perfectamente quietos.
caso("experimentar: la duda es real por los DOS lados (ciega en reposo, no ciega al plantarle algo)",
     _ex._mirando_sin_tocar(_ex._mundo(1)) < 0.05
     and _ex._mirando_sin_tocar(_ex._mundo(1), mover_uno=True) > 0.50)

print("== G11 TEMPLE y G12 REFLEJOS (prereg-40): los dos genes que estaban prometidos y no existian ==")
import temple as _tp, reflejos as _rf
caso("temple: APRUEBA su Regla 31 (4/4: inmutable, sube con gasto y error, la quietud no gana)",
     _tp.regla31(verbose=False) == 0)
# CONGELADO, y es la Regla 30 hecha codigo: si alguien escribe un bucle que "mejora" el temple para
# que Diego sufra menos, se estrella aqui. Un juez que se puede mover no es un juez.
try:
    _tp.ajustar(pesos={"gasto": 0.0})
    _inmutable = False
except _tp.TempleInmutable:
    _inmutable = True
caso("temple: intentar ajustarlo LANZA (Regla 30 mecanizada: los jueces no se automodifican)",
     _inmutable)
# CONGELADO: quedarse quieto JAMAS puede ser la salida barata. Sin esto, la politica optima seria
# no hacer nada nunca — el fallo clasico de un coste mal puesto.
caso("temple: quedarse quieto cuesta MAS que moverse con esfuerzo",
     _tp.coste(0.05, 0.05, 0.05, actividad=0.0) > _tp.coste(0.30, 0.30, 0.30, actividad=1.0))
caso("reflejos: APRUEBA su Regla 31 (5/5: mas rapido, coincide, calla, señuelo, potencia)",
     _rf.regla31(verbose=False) == 0)
# CONGELADO (Regla 12, y me la cazo el metodo el 10-ago): el acuerdo se mide como GANANCIA sobre la
# linea base tonta. Con la deliberacion disparando el 2%, un reflejo que dijera siempre "no"
# acertaba el 88.7% y el mio el 90.7%. Llamar a eso "acuerdo 0.907" era un numero sin significado.
_xr, _yr = _rf._mundo_de_prueba(n=400, senal=0.02)
caso("reflejos: sin señal que destilar, la ganancia sobre la linea base tonta es CERO",
     _rf.examinar(_rf.destilar(_xr, _yr), _xr, _yr)["acuerdo_con_la_deliberacion"] < 0.05)

print("== LA FICHA DE SANIDAD (10-ago-2026): los cinco tipos de error que repito al armar pruebas ==")
import sanidad as _san
caso("sanidad: APRUEBA su meta-prueba (caza los 5 tipos y no grita donde no hay nada)",
     _san.regla31(verbose=False) == 0)
# CONGELADO: la ficha se aplica al modulo mas reciente. Cazo dos cosas que su Regla 31 aprobo 8/8:
# una lectura de roce que seguia leyendo masa, y tres variables muertas. La Regla 31 comprueba que
# el instrumento hace lo que YO QUISE; la ficha comprueba que lo que quise fuera correcto.
caso("sanidad: experimentar2 no tiene restos de versiones anteriores",
     _san.restos_de_versiones(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                           "experimentar2.py"))["aprueba"])
# CONGELADO (TIPO F, pedido del director): ningun nombre del codigo puede llevar una letra que
# PAREZCA latina y no lo sea. Una 'a' cirilica en `azа1` hizo que la Regla 31 del prereg-37 nunca
# probara la condicion que decidia el estudio, y ninguna busqueda por texto la encontraba.
import glob as _glob
_homo = [x for _f in sorted(_glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                    "*.py")))
         for x in _san.homoglifos(_f)["fallos"]]
caso("sanidad: ningun nombre del codigo lleva letras que parecen latinas y no lo son", not _homo,
     str(_homo[:3]))
caso("sanidad: la politica de experimentar2 NO ve la verdad del mundo (Regla 27 mecanizada)",
     _san.politica_limpia(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                       "experimentar2.py"))["aprueba"])

print("== experimentacion dirigida 2a vuelta (prereg-39): un mundo donde elegir cueste ==")
import experimentar2 as _e2b
caso("experimentar2: APRUEBA su Regla 31 (8/8: duda real por los dos lados, presupuesto que no "
     "alcanza, NO tautologia, señuelo, mundo sin duda, medida sin techo)",
     _e2b.regla31(verbose=False) == 0)
# CONGELADO, y es la leccion literal del INFORME-46: dirigido y pasivo NO pueden compartir
# episodios. Ayer el pasivo heredaba los del dirigido y la diferencia salio 0.0000 EXACTA en 5/5.
# Una advertencia sobre una condicion debe ser un FALLO, no una nota.
_w39 = _e2b.mundo(1)
caso("experimentar2: el pasivo NO es una copia del dirigido (no hay tautologia)",
     _e2b.correr("dirigido", semilla=1, w=_w39)["reparto"]
     != _e2b.correr("pasivo", semilla=1, w=_w39)["reparto"])
# CONGELADO: en un mundo sin nada que averiguar, el dirigido no puede lucirse. Un instrumento que
# premia intervenir donde no hay pregunta esta midiendo su propio entusiasmo.
caso("experimentar2: en un mundo sin duda el dirigido cae al azar (no se luce sin pregunta)",
     _e2b.correr("dirigido", semilla=1, con_duda=False)["puntaje"] <= 12)

print("== el observador pasivo (prereg-32): el control que podria refutarnos ==")
import observador_pasivo as _op
caso("observador pasivo: APRUEBA su Regla 31 (5/5: control positivo, gemelos, ventaja plantada, "
     "y el mundo variable no rompe la comparacion)",
     _op.regla31(verbose=False) == 0)
# CONGELADO: la comparacion NO puede ser tautologica. Si las medidas de soporte dejan de
# consultar los comandos, encarnado y pasivo dan el MISMO numero por construccion y el "empate"
# no significa nada. Este caso exige que la copia eferente entre de verdad al modelo del mundo.
import inspect as _insp
caso("observador pasivo: la copia eferente ENTRA al modelo del encarnado (no es empate trivial)",
     "comandos" in _insp.signature(_op.fisica_de_soporte).parameters
     and "comandos=u" in _insp.getsource(_op.comparar))

print("== residuos en Koopman y chaperon causal (prereg-33) ==")
import koopman as _kp


def _osc(E, T=400, w=0.15):
    _t = np.arange(T)
    return np.column_stack([np.sqrt(E) * np.cos(w * _t + 0.3 * E),
                            -np.sqrt(E) * np.sin(w * _t + 0.3 * E)])


_tr = [_osc(E) for E in (0.5, 1.0, 1.5, 2.0, 2.5, 3.0)]
_inv = _kp.invariantes(_tr)
caso("koopman: el invariante REAL tiene residuo ~0 (no es fantasma del truncamiento)",
     len(_inv) == 1 and _inv[0]["residuo"] < 0.01)
_P0 = np.vstack([_kp._diccionario(x[:-1]) for x in _tr])
_P1 = np.vstack([_kp._diccionario(x[1:]) for x in _tr])
_rr = np.random.default_rng(3)
# LA LECCION QUE COSTO UNA CORRIDA EN ROJO (9-ago-2026): este caso pasaba en local y FALLABA
# en la nube. No era un test fragil: era un bug real. Con una perturbacion del orden de 1e-12
# —otra version de BLAS— la descomposicion devolvia DOS autovectores del MISMO observable y el
# modulo los contaba como dos invariantes. Uno visto dos veces no son dos. Ahora se deduplica
# por subespacio, y este caso lo verifica BAJO PERTURBACION, no solo en el caso limpio.
_rk = np.random.default_rng(1)
for _eps in (1e-12, 1e-9, 1e-7):
    _trp = [x + _eps * _rk.normal(size=x.shape) for x in _tr]
    caso(f"koopman: sigue hallando UN solo invariante con perturbacion {_eps:g} (dedup por subespacio)",
         len(_kp.invariantes(_trp)) == 1)
caso("koopman: un vector cualquiera NO pasa el filtro de residuo (asi se matan los fantasmas)",
     all(_kp._residuo(_P0, _P1, _rr.normal(size=_P0.shape[1]), 1.0) > _kp.RESIDUO_MAXIMO
         for _ in range(5)))

import entropia_transferencia as _et
_r2 = np.random.default_rng(11)
_n = 6000
_a = _r2.normal(0, 1, _n)
_b = 0.98 * _a + 0.02 * _r2.normal(0, 1, _n)
_c = np.zeros(_n)
for _i in range(1, _n):
    _c[_i] = 0.98 * _b[_i - 1] + 0.02 * _r2.normal()
_red = _et.reduccion_por_chaperon(_a, _c, _b, nulos=6)
# LA LECCION CONGELADA: la bivariada declara una flecha a->c que NO EXISTE (a no toca a c).
# El chaperon debe derrumbarla al menos un 90%. No se exige que la anule: no puede, y decirlo
# es parte del instrumento.
caso("entropia: el chaperon derrumba >=90% una arista indirecta que la bivariada declaraba",
     _red["arista_indirecta"] and _red["bivariada"] > 0.5)
caso("entropia: sin muestras suficientes la TE condicional se NIEGA a opinar (bins^4 celdas)",
     _et.medir_condicional(_a[:200], _c[:200], _b[:200])["medicion_invalida"] is not None)

print("== el cerebro motivacional (prereg-33): G13 lazo, G14 conductual, G2 blindada, G15 meta ==")
import cerebro as _cb
caso("cerebro: APRUEBA su Regla 31 (6/6: lazo, examen doble, curiosidad blindada, meta y su nulo)",
     _cb.regla31(verbose=False) == 0)
# CONGELADO: el lazo abierto SUBESTIMA el poder cuando el efecto depende del estado. Medido:
# con ruido 0.6 el lazo cerrado ve el doble. Si alguien "simplifica" quitando las interacciones,
# esto grita.
_dg = _cb.diagnostico_g13()
caso("cerebro: el lazo abierto subestima el poder en TODOS los niveles de ruido probados",
     all(f["subestima"] >= 0 for f in _dg) and _dg[-1]["lazo_cerrado"] > _dg[-1]["lazo_abierto"])
# CONGELADO: la metacognicion con confianza BARAJADA no puede superar su nulo. Es el nulo
# natural del gen nuevo: sin conocimiento, sin credito.
_rr3 = np.random.default_rng(77)
_ac = _rr3.uniform(size=400) > 0.5
caso("cerebro: metacognicion con confianza ciega NO supera su nulo (sin credito gratis)",
     not _cb.meta_con_nulo(_ac, _rr3.normal(size=400))["supera_al_nulo"])
_gen = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                                   "arbol", "GENOMA.json"), encoding="utf-8"))
caso("cerebro: G15 metacognicion entra al genoma en modo 'mide' (no decide sin firma)",
     _gen["genes"]["G15_metacognicion"]["modo"] == "mide")

print("== el sueño en DOS FASES con guardian (prereg-33) ==")
import sueno as _su
caso("sueño 2 fases: APRUEBA su Regla 31 (conservadora, guardian, generativa, mundo de ruido)",
     _su.regla31_dos_fases(verbose=False) == 0)
# CONGELADO: una ley soñada JAMAS pasa sin coincidir en soporte con una ley de vigilia. El filtro
# es mecanico, no una promesa escrita: si alguien lo quita, esto grita.
caso("sueño 2 fases: el filtro de vigilia es MECANICO (una ley soñada no pasa sola)",
     "soportes_vigilia" in _insp.getsource(_su.dormir))
# CONGELADO: la guarda de muestras de sindy3, hallada persiguiendo la alarma del guardian.
caso("sindy3: guarda de muestras minimas viva (ruido corto ya no produce leyes falsas)",
     _s3.MUESTRAS_MINIMAS >= 2000
     and _s3.descubrir(np.random.default_rng(4).normal(size=(600, 2)), dt=0.02) is None)

print("== auditoria de interconexion: UNA sola vara de obediencia, no tres ==")
# HALLAZGO DE LA AUDITORIA FINAL DEL 9-ago-2026: habia TRES implementaciones de "cuanto ayuda
# conocer el comando", y una de ellas (el panel) medía a UN paso mientras las otras medían a OCHO
# — justo el error que el prereg-29 habia diagnosticado. El panel subestimaba a todos los
# competidores por igual. Ahora las tres usan la MISMA funcion. Este caso impide que vuelvan a
# divergir en silencio.
caso("interconexion: panel, espejo y soporte usan el MISMO horizonte de obediencia",
     _pj.HORIZONTE == _sop.HORIZONTE == _e2.HORIZONTE)
caso("interconexion: panel y espejo NO reimplementan la medida, la importan de soporte",
     "_ganancia_canal" in _insp.getsource(_pj._ganancia_obediencia)
     and "_ganancia_canal" in _insp.getsource(_e2._obediencia))

print("== EL GIMNASIO: su mundo, su cuerpo y sus sentidos (G3, G7, propiocepcion, tacto) ==")
# HALLAZGO DEL MAPA DE LA MENTE (mente.py, 9-ago-2026): el Gimnasio —el mundo donde Diego vive,
# el cuerpo que tiene y los sentidos que se le dieron a priori— NO TENIA UN SOLO CASO en el banco
# congelado. Cuatro genes activos (G3 accion, G7 juego, propiocepcion, tacto) descansaban sobre
# codigo que nadie protegia. Los guardianes no lo veian porque miran lo que hay, no lo que falta.
import gimnasio as _gim
caso("gimnasio: el diseno del cuerpo es el GANADOR del torneo del prereg-24 (tope 2.5, sin amortiguacion)",
     _gim.DISENO["limite"] == 2.5 and _gim.DISENO["amortiguacion"] == 0.0)
caso("gimnasio: los cuatro controles de la Regla 31 siguen existiendo en el mundo",
     all(m in _gim.MODOS for m in ("sin_agencia", "un_grado", "tv_ruidoso", "sin_gravedad")))
_c31, _s31g, _v31 = _gim.episodio(1000, pasos=200, modo="normal")
caso("gimnasio: un episodio normal declara las 3 articulaciones como cuerpo (verdad de los jueces)",
     _v31 == {0, 1, 2} and _s31g.shape[1] == 7)
_cA, _sA, _vA = _gim.episodio(1000, pasos=200, modo="sin_agencia")
caso("gimnasio: el control sin_agencia declara CERO cuerpo (el brazo cae, pero no obedece)",
     _vA == set())
_cU, _sU, _vU = _gim.episodio(1000, pasos=200, modo="un_grado")
caso("gimnasio: el control un_grado declara SOLO la articulacion 0", _vU == {0})
_cT, _sT, _vT = _gim.episodio(1000, pasos=200, modo="tv_ruidoso")
caso("gimnasio: el televisor ruidoso NO cuenta como agencia (la articulacion 1 queda fuera)",
     _vT == {0, 2})
_c9, _s9, _v9, _sen9 = _gim.episodio(1000, pasos=200, modo="normal", sensores=True)
caso("sentidos: propiocepcion y tacto entregan 9 canales (3 angulos + 3 velocidades + 3 contactos)",
     _sen9.shape[1] == 9)
caso("sentidos: el tacto es binario y la propiocepcion no (son sentidos distintos, no copias)",
     set(np.unique(_sen9[:, 6:9])) <= {0.0, 1.0} and len(np.unique(_sen9[:, 0:3])) > 2)

print("== sentido_vision: los ojos, el gen que mas veces nos ha fallado ==")
# HALLAZGO DEL MAPA DE LA MENTE: sentido_vision esta en modo 'decide' —el modo mas alto— y no
# tenia UN SOLO caso en el banco. Es el gen con el historial mas accidentado del proyecto
# (INFORMES 27, 30-33, 36 y el acta del prereg-27), y era el menos protegido.
import percepcion2 as _p2
import ojos_gimnasio as _og
caso("vision: percepcion2 ofrece las dos arquitecturas del torneo (predictiva y con corolario)",
     "comandos" in _insp.signature(_p2.entrenar).parameters)
caso("vision: el codificador entrega un latente por episodio, no uno global",
     "def codificar" in _insp.getsource(_p2))
# EL LIMITE CONFESADO, congelado como caso: la vista NO esta certificada como predictiva del
# cuerpo. Si alguien lo proclama en el arbol sin corrida oficial nueva, esto grita.
_gd2 = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                         "resultados", "INFORME-38.md"), encoding="utf-8").read()
caso("vision: el acta del prereg-27 sigue declarandolo NO CONCLUYENTE POR INSTRUMENTO",
     "NO CONCLUYENTE POR INSTRUMENTO" in _gd2)

print("== EL NERVIO (conectar.py): la sinapsis conduce de verdad, no solo existe ==")
# EL BUG DE DISENO MAS GRAVE HALLADO (mapa de la mente, 9-ago-2026): `sinapsis.py` —el bus de
# comunicacion de la mente, con su portero, su Regla 31 aprobada y sus casos aqui mismo— NUNCA
# HABIA SIDO USADO POR NINGUN ORGANO. arbol/SINAPSIS.jsonl no existia: cero eventos en toda la
# vida del proyecto. Un sistema nervioso perfecto y desconectado. Los guardianes no lo veian
# porque miran lo que HAY, no lo que FALTA. Estos casos exigen que SIGA conectado.
import conectar as _con
import sinapsis as _sinapsis


def _tema_invalido():
    try:
        _sinapsis.publicar("G4_contingencia", "medicion", {}, tema="inventado",
                           _ruta=os.devnull)
        return False
    except _sinapsis.SinapsisBloqueada:
        return True

_sin_ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "arbol",
                         "SINAPSIS.jsonl")
caso("nervio: la sinapsis TIENE eventos (no basta con que el bus exista; tiene que conducir)",
     os.path.exists(_sin_ruta) and len(_sinapsis.leer()) > 0)
_ev = _sinapsis.leer()
caso("nervio: han hablado al menos 6 organos distintos por el bus",
     len({e["gen"] for e in _ev}) >= 6)
caso("nervio: NINGUN evento del bus es de tipo 'decision' publicado por un gen que solo MIDE",
     all(not (e["tipo"] == "decision"
              and _gen["genes"].get(e["gen"], {}).get("modo") == "mide") for e in _ev))
caso("nervio: el latido incluye la prueba viva del portero (un 'mide' intentando decidir)",
     "LA PRUEBA VIVA DEL PORTERO" in _insp.getsource(_con.latir))

print("== SINAPSIS 2.0: el protocolo unico, y la autopsia de cada prueba ==")
import trazar as _tz
caso("sinapsis 2.0: los cinco campos del pasaporte (id, tema, a, causa, traza)",
     all(k in _sinapsis.publicar.__doc__ for k in ("tema", "causa", "traza")))
caso("sinapsis 2.0: un tema inventado se rechaza (nervio a ninguna parte)",
     (lambda: [_sinapsis.publicar("G4_contingencia", "medicion", {}, tema="inventado")
               for _ in [0]] and False).__call__() if False else _tema_invalido())
caso("sinapsis 2.0: la suscripcion vive en el GENOMA, no en el codigo",
     all("escucha" in v for v in _gen["genes"].values()))
caso("sinapsis 2.0: NINGUN tema queda sin oyentes (no hay temas muertos)",
     all(_sinapsis.escuchan(t) for t in _sinapsis.TEMAS))
caso("trazador: APRUEBA su Regla 31 (huerfana, sin respuesta, ciclo, senal sin oyente)",
     _tz.regla31(verbose=False) == 0)
# LA LECCION CONGELADA: el acuse de recibo obligatorio. Sin el, el silencio de un organo es
# ambiguo — no distingue "nada que aportar" de "roto". Con el, el silencio significa averia.
caso("nervio: el acuse de recibo obligatorio sigue vivo (el silencio debe significar averia)",
     "ACUSE DE RECIBO OBLIGATORIO" in _insp.getsource(_con.latir))
_ult = _tz.reconstruir()
_f = _tz.revisar(_ult)
caso("nervio: la ultima ronda de vida no dejo NINGUN fallo de coordinacion",
     not any(_f.values()), str({k: v[:1] for k, v in _f.items() if v}))
# LOS DOS CAMPOS QUE CASI NADIE PONE, y sin los cuales la deteccion de fallos es imposible.
caso("sinapsis 2.0: el BUS escribe 'entrega' (distingue 'nadie oia' de 'oyeron y callaron')",
     all("entrega" in e for e in _ult["eventos"]))
# LA LECCION MAS FINA, cazada por el propio trazador: 'causa' (que me hizo hablar) NO es
# 'deriva_de' (de quien son los datos que use). Confundirlos hacia que ocho organos contestando
# la misma pregunta parecieran un consenso de un solo testigo. La genealogia viaja SOLO por
# deriva_de. Si alguien vuelve a mezclarlos, esto grita.
caso("sinapsis 2.0: la genealogia viaja por 'deriva_de' (evidencia), no por 'causa' (conversacion)",
     "deriva_de" in _sinapsis.publicar.__doc__ and "evidencial" in _sinapsis.publicar.__doc__)
caso("sinapsis 2.0: un organo que mide lo suyo cuenta como testigo INDEPENDIENTE",
     _sinapsis.testigos_independientes(
         [{"id": 1, "genealogia": [1]}, {"id": 2, "genealogia": [2]}]) == 2
     and _sinapsis.testigos_independientes(
         [{"id": 1, "genealogia": [9]}, {"id": 2, "genealogia": [9]}]) == 1)
# EL CASO QUE NACE DE UN ERROR MIO (9-ago-2026): dije "anadidos los enlaces" cuando solo habia
# anadido el CAMPO, vacio en los 33 eventos. El campo sin mecanismo no sirve de nada. Estos casos
# exigen el mecanismo, no la declaracion.
_sint = [e for e in _ult["eventos"] if e.get("enlaces")]
caso("sinapsis 2.0: la sintesis ENLAZA a todos sus contribuyentes (el campo no puede ir vacio)",
     len(_sint) >= 1 and len(_sint[0]["enlaces"]) >= 10)
caso("sinapsis 2.0: los enlaces aparecen como conexiones reales en la autopsia",
     len(_tz.conexiones(_ult)) > 2 * len([e for e in _ult["eventos"] if e.get("causa")]) // 3)
# LA SINTESIS NO PUEDE SER UN BLANQUEADOR DE EVIDENCIA: tiene que llevar lo que NO afirma.
caso("sintesis: declara explicitamente lo que NO se puede afirmar",
     any("lo_que_NO_se_afirma" in (e.get("contenido") or {}) for e in _ult["eventos"]
         if isinstance(e.get("contenido"), dict)))
caso("sintesis: cuenta TESTIGOS independientes, no voces",
     any("testigos_independientes" in (e.get("contenido") or {}) for e in _ult["eventos"]
         if isinstance(e.get("contenido"), dict)))
# CONVOCATORIA POR NECESIDAD (prereg-34): acotada duro y por competencia FUNCIONAL.
caso("convocatoria: Diego elige por competencia funcional, no por dominio fisico",
     _sinapsis.convocar_por_necesidad(["consolidar", "reminar"])[0][:1] == ["G9_sueno"])
caso("convocatoria: JAMAS puede convocar a todos (techo duro del canal global)",
     len(_sinapsis.convocar_por_necesidad(["percibir", "actuar", "modelar"], k=99)[0])
     <= _sinapsis.K_MAXIMO < 18)
caso("nervio: en la ultima ronda hablaron los 16 organos activos",
     len({e["gen"] for e in _ult["eventos"]}) >= 16)

print("== canonizar: tarjeta de identidad ==")
t = tarjeta("(v1 + v2) * 0.5 + 3.0", 4)
caso("desplazamiento = f(0)", abs(t["desplazamiento"] - 3.0) < 1e-6)
caso("gradiente correcto", abs(t["gradiente"][0] - 0.5) < 1e-4 and abs(t["gradiente"][2]) < 1e-6)
caso("estable marcada estable", not t["explota_con_entradas_grandes"])
t2 = tarjeta("exp(exp(v1))", 2)
caso("explosiva marcada fragil", t2.get("explota_con_entradas_grandes", False) or "error" in t2)

print()
if FALLOS:
    print(f"BANCO: {len(FALLOS)} FALLOS -> NO COMMITEAR: {FALLOS}")
    sys.exit(1)
print("BANCO: TODO OK — el codigo respeta las lecciones congeladas")
