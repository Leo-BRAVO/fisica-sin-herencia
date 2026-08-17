# TANTEO DEL BANCO — NO ES EVIDENCIA. Diagnostico de la pregunta que abrio el INFORME-67:
# ¿por que el softmax espacial se derrumba en la semilla 263 y no en las otras cuatro?
# Sospecha declarada en el acta: los dos puntos de atencion COLAPSAN sobre el mismo segmento.
import sys, json
import numpy as np, torch
sys.path.insert(0, "/home/user/fisica-sin-herencia/codigo")
import banco, ojos_keypoint as OK, ojos_brazo as OB

out = {}
for sem in (263, 251):                     # la que fallo y una que fue bien
    vids, verdad = OB.escena(sem)
    X = torch.tensor(vids)
    m, _ = OK.entrenar(OK.Keypoint(), X, semilla=sem)
    with torch.no_grad():
        Z = m.z(X).numpy()                 # [x0, x1, y0, y1]
    p0 = np.stack([Z[:, 0], Z[:, 2]], 1)
    p1 = np.stack([Z[:, 1], Z[:, 3]], 1)
    sep = np.linalg.norm(p0 - p1, axis=1)
    out[str(sem)] = {
        "r2": round(OK.r2_lineal(Z, verdad), 4),
        "separacion_media_entre_los_dos_puntos": round(float(sep.mean()), 4),
        "separacion_minima": round(float(sep.min()), 4),
        "recorrido_del_punto_0": round(float(p0.std(0).mean()), 4),
        "recorrido_del_punto_1": round(float(p1.std(0).mean()), 4),
    }
    print(sem, out[str(sem)])
banco.escribir("colapso/tanteo.json", out, semillas=(263, 251),
               que_se_tanteaba="si los dos keypoints colapsan sobre el mismo segmento (INFORME-67)")
