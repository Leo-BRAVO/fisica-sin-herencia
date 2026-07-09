# extraer_posiciones.py — Fase 0, proyecto Física sin herencia
# Extrae la posición (x, y) en píxeles del objeto más móvil/contrastado de un video.
# Salida: CSV con columnas cuadro, x, y — DATO CRUDO según la Regla 2 (píxeles y cuadros, sin unidades físicas).
# Uso:  python extraer_posiciones.py <video> <salida.csv> [--metodo color|movimiento] [--hsv H_MIN H_MAX]
#
# Regla 2: este script NO aplica ningún modelo físico. Solo localiza un punto brillante/móvil por cuadro.
# Suavizado: NINGUNO aquí. Si se necesita, se hace en un paso aparte, documentado, sobre una copia.

import sys
import csv
import argparse

import cv2
import numpy as np


def centroide_por_color(frame_bgr, h_min, h_max, s_min=80, v_min=80):
    """Centroide de la mancha de color dentro del rango HSV dado. None si no hay mancha."""
    hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (h_min, s_min, v_min), (h_max, 255, 255))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    M = cv2.moments(mask)
    if M["m00"] < 50:  # mancha demasiado pequeña → sin detección este cuadro
        return None
    return (M["m10"] / M["m00"], M["m01"] / M["m00"])


def centroide_por_movimiento(frame_gray, fondo_gray):
    """Centroide de la región que más difiere del fondo (mediana temporal). None si no hay movimiento."""
    diff = cv2.absdiff(frame_gray, fondo_gray)
    _, mask = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    M = cv2.moments(mask)
    if M["m00"] < 50:
        return None
    return (M["m10"] / M["m00"], M["m01"] / M["m00"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("salida_csv")
    ap.add_argument("--metodo", choices=["color", "movimiento"], default="movimiento")
    ap.add_argument("--hsv", nargs=2, type=int, default=[0, 15],
                    help="Rango de tono HSV del marcador (solo --metodo color)")
    args = ap.parse_args()

    cap = cv2.VideoCapture(args.video)
    if not cap.isOpened():
        sys.exit(f"No se pudo abrir el video: {args.video}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    n_total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Video: {args.video} | fps reportado: {fps:.2f} | cuadros: {n_total}")

    fondo = None
    if args.metodo == "movimiento":
        # Fondo = mediana de 25 cuadros muestreados a lo largo del video (operación genérica, no física)
        idxs = np.linspace(0, max(n_total - 1, 0), 25).astype(int)
        muestras = []
        for i in idxs:
            cap.set(cv2.CAP_PROP_POS_FRAMES, int(i))
            ok, f = cap.read()
            if ok:
                muestras.append(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY))
        fondo = np.median(np.stack(muestras), axis=0).astype(np.uint8)
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    filas, perdidos = [], 0
    cuadro = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if args.metodo == "color":
            c = centroide_por_color(frame, args.hsv[0], args.hsv[1])
        else:
            c = centroide_por_movimiento(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), fondo)
        if c is None:
            perdidos += 1
        else:
            filas.append((cuadro, round(c[0], 3), round(c[1], 3)))
        cuadro += 1
    cap.release()

    with open(args.salida_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["cuadro", "x_px", "y_px"])
        w.writerows(filas)

    print(f"Detecciones: {len(filas)}/{cuadro} cuadros ({perdidos} sin detección)")
    print(f"CSV escrito: {args.salida_csv}")
    if cuadro > 0 and perdidos / cuadro > 0.10:
        print("ADVERTENCIA: más del 10% de cuadros sin detección — revisar video o método antes de usar estos datos.")


if __name__ == "__main__":
    main()
