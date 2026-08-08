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

print("== GEN G2 (curiosidad2, prereg-18): aburrimiento y progreso ==")
# Regla 31 del gen: una memoria donde NADA progresa (mismo g en todos los intentos de todas
# las regiones) debe producir ABURRIMIENTO universal (prioridad 0 en toda region visitada),
# jamas interes inventado. Y una region cuyo record MEJORA debe puntuar positivo.
from curiosidad2 import prioridades as _prio, UMBRAL as _umb
_mem_plana = []
for _reg, _pref in [("mendeley", "oficial-trial1"), ("zenodo", "peldano2-pendulo46"),
                    ("dp-centroides", "dp-morpheus"), ("dp-latentes-propios", "p13-latente"),
                    ("caida", "caida-libre"), ("conservadas", "conservadas-x")]:
    for _k in range(3):
        _mem_plana.append({"campana": _pref, "lo_trivial": 4.0, "mi_mejor_esfuerzo": 1.0})
_pp = _prio(_mem_plana)
caso("memoria sin progreso -> aburrimiento universal (todas las prioridades <= umbral)",
     all(p <= _umb for p in _pp.values()), f"{_pp}")
_mem_viva = list(_mem_plana) + [{"campana": "oficial-trial1", "lo_trivial": 4.0, "mi_mejor_esfuerzo": 0.25}]
_pv = _prio(_mem_viva)
caso("record que mejora -> progreso positivo en su region",
     _pv["mendeley"] > _umb and all(_pv[r] <= _umb for r in _pv if r != "mendeley"),
     f"{_pv}")

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
