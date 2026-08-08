# latido_nube.py — EL LATIDO EN LA NUBE (8-ago-2026): el corazon del proyecto ya no vive
# en ninguna laptop. El workflow latido-nube.yml (GitHub Actions, diario) llama a este
# script para ejecutar la cola de estudios sin que nadie este despierto.
# Gobernanza intacta: SOLO toma items tipo "re-analisis" con estado "pendiente"
# (aprobacion permanente del director para re-analisis; todo lo demas lo espera a el).
#
# Uso: python latido_nube.py --campo id|datos|salida|args|reconstruir   (del proximo item)
#      python latido_nube.py --completar-si-terminado <id>   (marca hecha SOLO si hay resumen)

import os
import sys
import json
import argparse

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COLA = os.path.join(BASE, "registros", "COLA-ESTUDIOS.json")


def cargar():
    return json.load(open(COLA, encoding="utf-8")) if os.path.exists(COLA) else {"items": []}


def siguiente():
    for i in cargar()["items"]:
        if i.get("tipo") == "re-analisis" and i.get("estado") == "pendiente":
            return i
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--campo", choices=["id", "datos", "salida", "args", "reconstruir"])
    ap.add_argument("--completar-si-terminado", default=None)
    a = ap.parse_args()

    if a.campo:
        item = siguiente()
        print("" if item is None else str(item.get(a.campo, "") or ""))
        return

    if a.completar_si_terminado:
        cola = cargar()
        for i in cola["items"]:
            if i["id"] == a.completar_si_terminado:
                resumen = os.path.join(BASE, i.get("salida", ""), "resumen.json")
                if os.path.exists(resumen):
                    i["estado"] = "hecha"
                    i["resultado"] = "corrida por latido-nube (Actions)"
                    print(f"COMPLETADA: {i['id']}")
                else:
                    print(f"NO completada (sin resumen — quedan checkpoints para reanudar): {i['id']}")
        with open(COLA, "w", encoding="utf-8") as f:
            json.dump(cola, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
