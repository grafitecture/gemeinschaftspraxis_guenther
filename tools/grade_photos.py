"""Farbangleichung der Praxisfotos an die Hausfarben #0080C9 (Blau) und #9BA2A7 (Grau).
Der fotografische Stil bleibt; nur Weißabgleich, Farbstimmung und Tonwerte werden vereinheitlicht:
- neutrale, leicht kühle Weißtöne
- Blau des Logos bleibt kräftig und wird zum Hausblau gezogen
- warme Töne (Holzboden, Blumen, Licht) werden zurückgenommen, nicht entfernt
- Schatten leicht ins Schiefergrau, Schwarz minimal angehoben (weicher, ruhiger Look)
"""
import cv2
import numpy as np
from PIL import Image, ImageOps

BLUE_HUE = 202.0          # Farbton von #0080C9 in Grad
SHADOW = np.array([86, 93, 98]) / 255.0     # #565d62 – Schattentönung
HIGHLIGHT = np.array([246, 248, 250]) / 255.0


def load(path, long_edge=1800):
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    im.thumbnail((long_edge, long_edge), Image.LANCZOS)
    return np.asarray(im).astype(np.float32) / 255.0


def white_balance(rgb, strength=0.85):
    """Gleicht anhand heller, wenig gesättigter Flächen auf neutral ab – mit leichtem Kühlstich."""
    mx, mn = rgb.max(2), rgb.min(2)
    sat = (mx - mn) / (mx + 1e-6)
    m = (mx > 0.55) & (mx < 0.97) & (sat < 0.18)
    if m.sum() < 500:
        m = mx > np.percentile(mx, 80)
    ref = rgb[m].mean(0)
    target = ref.mean() * np.array([0.985, 1.0, 1.02])
    gain = 1 + strength * (target / ref - 1)
    return np.clip(rgb * gain, 0, 1).astype(np.float32)


def hue_dist(h, center):
    d = np.abs(h - center)
    return np.minimum(d, 360 - d)


def grade(rgb, warm_keep=0.55, other_keep=0.7, blue_boost=1.08, skin=False):
    hsv = cv2.cvtColor(np.ascontiguousarray(rgb, dtype=np.float32), cv2.COLOR_RGB2HSV)  # H 0..360, S 0..1, V 0..1
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    blue_w = np.clip(1 - hue_dist(h, 205) / 28, 0, 1)    # Blautöne 177–233°
    warm_w = np.clip(1 - hue_dist(h, 35) / 40, 0, 1)     # Gelb/Orange/Holz
    if skin:  # Hauttöne in Porträts weitgehend schützen
        warm_keep = max(warm_keep, 0.86)
    factor = np.full_like(s, other_keep)
    factor = factor * (1 - warm_w) + warm_keep * warm_w
    factor = factor * (1 - blue_w) + blue_boost * blue_w
    s2 = np.clip(s * factor, 0, 1)
    # Blau zum Hausblau ziehen
    h2 = h + (BLUE_HUE - h) * 0.45 * blue_w
    hsv2 = np.stack([h2 % 360, s2, v], -1)
    out = cv2.cvtColor(hsv2.astype(np.float32), cv2.COLOR_HSV2RGB)
    return out


def tone(rgb, lift=0.035, contrast=0.12, roll=0.04):
    """Sanfte S-Kurve, leicht angehobenes Schwarz, weich abfallende Lichter."""
    x = rgb
    x = x + contrast * (x - 0.5) * (1 - np.abs(2 * x - 1))      # S-Kurve in den Mitten
    x = lift + (1 - lift - roll) * x + roll * (1 - (1 - x) ** 2)
    return np.clip(x, 0, 1)


def split_tone(rgb, amount=0.13):
    lum = (0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2])[..., None]
    sh = np.clip(1 - lum * 2, 0, 1) ** 1.5
    hi = np.clip(lum * 2 - 1, 0, 1) ** 1.5
    out = rgb + amount * sh * (SHADOW - rgb) * 0.9 + amount * 0.6 * hi * (HIGHLIGHT - rgb)
    return np.clip(out, 0, 1)


def vignette(rgb, amount=0.10):
    hgt, wid = rgb.shape[:2]
    y, x = np.ogrid[:hgt, :wid]
    r = np.sqrt(((x - wid / 2) / (wid / 2)) ** 2 + ((y - hgt / 2) / (hgt / 2)) ** 2) / np.sqrt(2)
    return np.clip(rgb * (1 - amount * r[..., None] ** 2.2), 0, 1)


def finish(rgb, grain=0.0, seed=1):
    """Feines Korn, wie bei Mittelformat-Abzügen – kaschiert auch Hochskalierung."""
    if grain:
        rng = np.random.default_rng(seed)
        n = cv2.GaussianBlur(rng.normal(0, grain, rgb.shape[:2]).astype(np.float32), (0, 0), 0.7)
        rgb = np.clip(rgb + n[..., None], 0, 1)
    return rgb


def process(src, dst, crop=None, size=None, wb=0.85, quality=82, **kw):
    rgb = load(src)
    if crop:  # relative (x0, y0, x1, y1)
        H, W = rgb.shape[:2]
        x0, y0, x1, y1 = crop
        rgb = rgb[int(y0 * H):int(y1 * H), int(x0 * W):int(x1 * W)]
    rgb = white_balance(rgb, wb)
    rgb = grade(rgb, **kw)
    rgb = split_tone(rgb)
    rgb = tone(rgb)
    rgb = vignette(rgb)
    im = Image.fromarray((rgb * 255 + 0.5).astype(np.uint8))
    if size:
        im = ImageOps.fit(im, size, Image.LANCZOS)
    im.save(dst, "WEBP", quality=quality, method=6)
    return im.size
