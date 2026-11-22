"""Erzeugt alle Praxisfotos der Website aus WEBSEITE_DATEN/PRAXIS (Farbangleichung, Zuschnitt)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from grade_photos import process

SRC = os.environ.get("PRAXIS_SRC", "/home/claude/neu/PRAXIS")
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "img")
JOBS = [
    # Datei, Quelle, Zielgröße (B, H), Ausschnitt relativ oder None
    ("foto-hero.webp", "IMG_8285.jpeg", (1200, 1500), None),
    ("foto-empfang.webp", "IMG_0687.jpeg", (1200, 1600), None),
    ("foto-anmeldung.webp", "IMG_0689.jpeg", (1050, 1400), None),
    ("foto-raum.webp", "IMG_4830.jpeg", (1050, 1400), None),
    ("foto-raum-2.webp", "IMG_4720.jpeg", (1050, 1400), None),
    ("foto-sitz.webp", "IMG_8239.jpeg", (1050, 1400), None),
    ("foto-g.webp", "IMG_8261.jpeg", (1050, 1400), None),
    ("foto-strasse.webp", "IMG_5510.jpeg", (1050, 1400), None),
    ("foto-abend.webp", "IMG_8282.jpeg", (1050, 1400), None),
    ("foto-vordach.webp", "IMG_8258.jpeg", (1050, 1400), None),
    ("foto-tuer.webp", "IMG_8246.jpeg", (1050, 1400), None),
    ("insta-g.webp", "IMG_8282.jpeg", (900, 900), (0.0, 0.18, 1.0, 0.93)),
    ("insta-empfang.webp", "IMG_0687.jpeg", (900, 900), (0.0, 0.25, 1.0, 1.0)),
]
for name, src, size, crop in JOBS:
    print(name, process(os.path.join(SRC, src), os.path.join(OUT, name), crop=crop, size=size))
