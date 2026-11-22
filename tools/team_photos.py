"""Fiktive Teamporträts (Demo) aus Higgsfield-Generierungen (Soul 2.0).

Die Rohbilder liegen in HF_SRC (Standard: WEBSEITE_DATEN/HIGGSFIELD/ERGEBNIS/<name>.png).
Pro Person: Ausschnitt für einheitliche Kopfgröße und Augenhöhe, sanfte Angleichung an
die Farbwelt der Praxisfotos (Haut geschützt), Ausgabe quadratisch 1000 px als WebP.

Aufruf: python3 tools/hf_portraits.py [namen]
"""
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from grade_photos import grade, split_tone, tone, vignette, finish  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.environ.get("HF_SRC", "/home/claude/hf/raw")
OUT = os.path.join(ROOT, "assets", "img")
SIZE = 800

# Ausschnitt relativ zum Rohbild: Mittelpunkt (cx, cy) und Kantenlänge (s), jeweils 0..1
CROP = {
    "evelyne": (0.5, 0.5, 1.0),
    "andreas": (0.5, 0.5, 1.0),
    "p1": (0.5, 0.5, 1.0),
    "p2": (0.5, 0.5, 1.0),
    "p3": (0.5, 0.5, 1.0),
    "p4": (0.5, 0.5, 1.0),
    "p5": (0.5, 0.5, 1.0),
}


def crop(img, cx, cy, s):
    w, h = img.size
    side = s * min(w, h)
    x0 = min(max(cx * w - side / 2, 0), w - side)
    y0 = min(max(cy * h - side / 2, 0), h - side)
    return img.crop((round(x0), round(y0), round(x0 + side), round(y0 + side)))


def look(rgb, seed):
    rgb = grade(rgb, warm_keep=0.92, other_keep=0.86, blue_boost=1.0, skin=True)
    rgb = split_tone(rgb, 0.06)
    rgb = tone(rgb, lift=0.012, contrast=0.04, roll=0.03)
    rgb = vignette(rgb, 0.08)
    return finish(rgb, grain=0.006, seed=seed)


def run(names):
    for i, k in enumerate(names):
        src = next((os.path.join(SRC, k + e) for e in (".png", ".jpg", ".jpeg", ".webp", ".PNG", ".JPG")
                    if os.path.exists(os.path.join(SRC, k + e))), "")
        if not src:
            print("fehlt", src)
            continue
        img = crop(Image.open(src).convert("RGB"), *CROP[k]).resize((SIZE, SIZE), Image.LANCZOS)
        # leichte Glättung gegen JPEG-Blöcke der Übernahme
        import cv2
        arr = cv2.fastNlMeansDenoisingColored(np.asarray(img)[:, :, ::-1].copy(), None, 2, 2, 5, 15)[:, :, ::-1]
        rgb = np.asarray(arr, dtype=np.float32) / 255.0
        out = look(rgb, seed=11 + i)
        Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8)).save(
            os.path.join(OUT, f"team-{k}.webp"), "WEBP", quality=86, method=6)
        print("ok", k)


if __name__ == "__main__":
    run(sys.argv[1:] or list(CROP))
