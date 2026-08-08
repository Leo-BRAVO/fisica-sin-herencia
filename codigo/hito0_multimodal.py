# hito0_multimodal.py — LA CORRIDA OFICIAL DEL PRERREGISTRO-26 (FIRMADO): Diego se SIENTE.
#
# Vector sensorial = [latentes visuales (8)] + [propiocepción (6)] + [tacto (3)] = 17 canales.
# Sobre TODO el vector: contingencia (criterio del prereg-23 congelado). Además:
#   - el ESPEJO (intermodal.py): ¿la vista lleva dentro al cuerpo sentido?
#   - control obligatorio: sin_agencia (el brazo cae por gravedad: propiocepción SIN agencia).
#   - nivel B con el vector completo.
# Uso: python hito0_multimodal.py [--episodios 12] [--pasos 1500] [--epocas 12]

import os
import sys
import json
import argparse

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "codigo"))

from gimnasio import correr, episodio
from contingencia import medir
from ojos_gimnasio import entrenar_ojos, primer_no_yo
from intermodal import espejo
import percepcion2 as p2

N_VIS = 8


def episodios_completos(n, pasos, modo, semilla0=1000):
    coms, sens, vids, sentidos, verdad = [], [], [], [], None
    for i in range(n):
        c, s, v, cuadros, sen = episodio(semilla0 + i, pasos=pasos, modo=modo,
                                         render=True, sensores=True)
        coms.append(c); sens.append(s); vids.append(cuadros); sentidos.append(sen); verdad = v
    return coms, sens, vids, sentidos, verdad


def vector_multimodal(vids, sentidos, jidx, epocas):
    modelo = entrenar_ojos(vids, jidx, latente=N_VIS, epocas=epocas)
    lat = p2.codificar(modelo, vids, jidx)
    tren = np.vstack([s for i, s in enumerate(sentidos) if i not in jidx])
    mu, sd = tren.mean(0), tren.std(0)
    sd[sd == 0] = 1.0
    cuerpo_std = [(s - mu) / sd for s in sentidos]
    return [np.column_stack([l, c[:len(l)]]) for l, c in zip(lat, cuerpo_std)], lat, cuerpo_std


def resumen_medicion(nombre, res):
    mias = sorted(r["variable"] for r in res if r["es_mia"])
    print(f"\n--- {nombre}: canales MÍOS {mias or 'ninguno'} ---", flush=True)
    for r in res:
        etiqueta = ("visual" if r["variable"] < N_VIS
                    else "propio" if r["variable"] < N_VIS + 6 else "tacto")
        print(f"    c{r['variable']:>2} [{etiqueta:>6}]: {r['obedece_en']:.2f} "
              f"(nulo {r['nulo_techo']:.2f}){' <- MÍO' if r['es_mia'] else ''}", flush=True)
    return mias


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--episodios", type=int, default=12)
    ap.add_argument("--pasos", type=int, default=1500)
    ap.add_argument("--epocas", type=int, default=12)
    ap.add_argument("--jueces", nargs="+", type=int, default=[10, 11, 12])
    a = ap.parse_args()
    jidx = {j - 1 for j in a.jueces}
    salida = {"prerregistro": 26, "episodios": a.episodios, "pasos": a.pasos,
              "epocas": a.epocas, "jueces": a.jueces}

    print(f"=== PREREG-26 MULTIMODAL — {a.episodios} ep x {a.pasos} cuadros ===", flush=True)
    coms, sens, vids, sentidos, verdad = episodios_completos(a.episodios, a.pasos, "normal")
    vec, lat_vis, cuerpo_std = vector_multimodal(vids, sentidos, jidx, a.epocas)

    res = medir(list(zip(coms, vec)), a.jueces, nulos=10)
    mias = resumen_medicion("NIVEL A multimodal (normal)", res)
    salida["nivel_a"] = res
    salida["canales_mios"] = mias

    print("\n[control obligatorio] sin_agencia: el brazo cae por gravedad, cero agencia", flush=True)
    comsG, sensG, vidsG, sentidosG, _ = episodios_completos(a.episodios, a.pasos, "sin_agencia",
                                                            semilla0=3000)
    vecG, _, _ = vector_multimodal(vidsG, sentidosG, jidx, a.epocas)
    resG = medir(list(zip(comsG, vecG)), a.jueces, nulos=10)
    miasG = resumen_medicion("CONTROL sin agencia", resG)
    salida["control_sin_agencia"] = {"canales_mios": miasG, "detalle": resG}

    esp = espejo(lat_vis, cuerpo_std, a.jueces)
    print(f"\nEL ESPEJO: {esp['espejo']:.3f} vs nulo {esp['nulo_techo']:.3f} "
          f"→ {'SE RECONOCE' if esp['se_reconoce'] else 'la vista NO lleva al cuerpo dentro'}",
          flush=True)
    salida["espejo"] = esp

    no_mias = {r["variable"] for r in res} - set(mias)
    nb = primer_no_yo(vec, coms, no_mias, jidx)
    salida["nivel_b"] = nb
    if nb:
        print(f"NIVEL B: fuerza {nb['fuerza']:.4f} vs nulo {nb['nulo_techo']:.4f} "
              f"→ {'SUPERA' if nb['supera_al_nulo'] else 'no supera'}", flush=True)

    out = os.path.join(BASE, "resultados", "p26-hito0-multimodal")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "resumen.json"), "w", encoding="utf-8") as f:
        json.dump(salida, f, indent=2, ensure_ascii=False, default=str)
    print(f"\nguardado en {out}/resumen.json", flush=True)


if __name__ == "__main__":
    main()
