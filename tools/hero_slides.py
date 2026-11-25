"""Zusätzliches Hero-Bild (Demo, KI): das Ehepaar als Teambild.

Erzeugt mit Higgsfield (Nano Banana 2.1, 2K, 4:5) aus den Porträts team-andreas/team-evelyne
und dem Empfangsfoto als Vorlage. Die Rohbilder liegen in HF_SRC (Standard: /home/claude/hf):
  team-original.png  ->  assets/img/foto-aerzte-ehepaar.webp    (Original 1856 x 2304, von Martin)
(Das Bild „Ärzte im Gespräch“ am Tisch – meeting-1200.png – ist seit 25.11.2026 auf Wunsch
aus dem Hero entfernt; an seiner Stelle steht das Empfangsfoto, siehe make_photos.py.)
Zuschnitt mittig auf 4:5, Farbangleichung wie bei den Teamporträts (team_photos.look),
Ausgabe 1200 x 1500 WebP.

Aufruf: python3 tools/hero_slides.py
"""
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from team_photos import look  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.environ.get("HF_SRC", "/home/claude/hf")
OUT = os.path.join(ROOT, "assets", "img")
SIZE = (1200, 1500)
FILES = {
    # Quelle: (Ziel, Zufallswert der Körnung – fest, damit das Bild bei erneutem Lauf gleich bleibt)
    "team-original.png": ("foto-aerzte-ehepaar.webp", 32),
}


def run():
    for src, (dst, seed) in FILES.items():
        path = os.path.join(SRC, src)
        if not os.path.exists(path):
            print("fehlt", path)
            continue
        img = Image.open(path).convert("RGB")
        w, h = img.size
        if abs(w / h - 0.8) > 0.001:  # mittig auf 4:5 zuschneiden
            if w / h > 0.8:
                nw = round(h * 0.8); img = img.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
            else:
                nh = round(w / 0.8); img = img.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
        if img.size != SIZE:
            img = img.resize(SIZE, Image.LANCZOS)
        rgb = np.asarray(img, dtype=np.float32) / 255.0
        out = look(rgb, seed=seed)
        Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8)).save(
            os.path.join(OUT, dst), "WEBP", quality=84, method=6)
        print("ok", dst)


if __name__ == "__main__":
    run()
