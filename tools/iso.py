"""Kleine Isometrie-Engine für architektonische Strichzeichnungen (SVG).

Achsen: +x läuft nach rechts unten, +y nach links unten, +z nach oben.
Sichtbar sind bei Boxen: Deckfläche, +x-Fläche (rechts) und +y-Fläche (links).
"""
import math

C30 = math.cos(math.radians(30))
S30 = 0.5

BLUE = "#0080C9"
DEEP = "#006BA8"
STONE = "#9BA2A7"
SAGE = "#9BA2A7"
INK = "#1F282D"
MIST = "#F3F6F8"

STYLE = f"""
.x-l{{stroke:{BLUE};stroke-width:1.15;stroke-linejoin:round;stroke-linecap:round}}
.x-t{{fill:#FFFFFF}}
.x-r{{fill:#EDF4F9}}
.x-f{{fill:#F7FAFC}}
.x-n{{fill:none}}
.x-w{{fill:#FFFFFF}}
.x-glass{{fill:#DCEBF5}}
.x-acc{{fill:{BLUE}}}
.x-accs{{fill:{BLUE};stroke:{BLUE}}}
.x-sage{{fill:#EEF0F1;stroke:{SAGE}}}
.x-sagef{{fill:{SAGE};stroke:{SAGE}}}
.x-g{{stroke:{STONE};stroke-width:.6;stroke-dasharray:2 4;fill:none;opacity:.8}}
.x-gs{{stroke:{STONE};stroke-width:.6;fill:none;opacity:.7}}
.x-lbl{{font-family:'Fira Sans',system-ui,sans-serif;fill:{DEEP};font-weight:500}}
.x-lbll{{font-family:'Fira Sans',system-ui,sans-serif;fill:{DEEP};font-weight:300}}
.x-mark{{fill:{BLUE};opacity:.12}}
"""


def c(cls):
    return " ".join("x-" + k for k in cls.split())


class Iso:
    def __init__(self, scale=20, ox=400, oy=120):
        self.s = scale
        self.ox = ox
        self.oy = oy
        self.out = []
        self.bb = [1e9, 1e9, -1e9, -1e9]

    def _track(self, X, Y, m=0):
        b = self.bb
        b[0] = min(b[0], X - m); b[1] = min(b[1], Y - m); b[2] = max(b[2], X + m); b[3] = max(b[3], Y + m)

    # --- Projektion ---------------------------------------------------
    def p(self, x, y, z=0):
        X, Y = (self.ox + (x - y) * C30 * self.s, self.oy + (x + y) * S30 * self.s - z * self.s)
        self._track(X, Y)
        return X, Y

    def fmt(self, pts):
        return " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)

    # --- Primitive ----------------------------------------------------
    def poly(self, pts3, cls="l t", extra=""):
        pts = [self.p(*q) for q in pts3]
        self.out.append(f'<polygon class="{c(cls)}" points="{self.fmt(pts)}" {extra}/>')

    def line(self, a, b, cls="l"):
        (x1, y1), (x2, y2) = self.p(*a), self.p(*b)
        self.out.append(f'<line class="{c(cls)}" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>')

    def path3(self, pts3, cls="l n", close=False):
        pts = [self.p(*q) for q in pts3]
        d = "M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in pts) + (" Z" if close else "")
        self.out.append(f'<path class="{c(cls)}" d="{d}"/>')

    def raw(self, s):
        self.out.append(s)

    def box(self, x, y, z, w, d, h, top="l t", right="l r", left="l f"):
        P = (x, y, z)
        self.poly([(x, y + d, z), (x + w, y + d, z), (x + w, y + d, z + h), (x, y + d, z + h)], left)
        self.poly([(x + w, y, z), (x + w, y + d, z), (x + w, y + d, z + h), (x + w, y, z + h)], right)
        self.poly([(x, y, z + h), (x + w, y, z + h), (x + w, y + d, z + h), (x, y + d, z + h)], top)
        return P

    # Rechteck auf einer Fläche
    def rect_y(self, y, x, z, w, h, cls="l glass"):
        """Rechteck in Ebene y=const (linke Fassade)."""
        self.poly([(x, y, z), (x + w, y, z), (x + w, y, z + h), (x, y, z + h)], cls)

    def rect_x(self, x, y, z, d, h, cls="l glass"):
        """Rechteck in Ebene x=const (rechte Fassade)."""
        self.poly([(x, y, z), (x, y + d, z), (x, y + d, z + h), (x, y, z + h)], cls)

    def rect_z(self, z, x, y, w, d, cls="l t"):
        self.poly([(x, y, z), (x + w, y, z), (x + w, y + d, z), (x, y + d, z)], cls)

    # Kreis in Ebene (als transformierte Ellipse)
    def circle_y(self, y, x, z, r, cls="accs"):
        X, Y = self.p(x, y, z)
        s = self.s
        self.out.append(
            f'<circle class="{c(cls)}" r="{r*s:.2f}" cx="0" cy="0" transform="matrix({C30:.4f} {S30:.4f} 0 1 {X:.1f} {Y:.1f})"/>')

    def circle_x(self, x, y, z, r, cls="l t"):
        X, Y = self.p(x, y, z)
        s = self.s
        self.out.append(
            f'<circle class="{c(cls)}" r="{r*s:.2f}" cx="0" cy="0" transform="matrix({C30:.4f} {-S30:.4f} 0 1 {X:.1f} {Y:.1f})"/>')

    def circle_z(self, z, x, y, r, cls="l t"):
        X, Y = self.p(x, y, z)
        s = self.s
        self.out.append(
            f'<circle class="{c(cls)}" r="{r*s:.2f}" cx="0" cy="0" transform="matrix({C30:.4f} {S30:.4f} {-C30:.4f} {S30:.4f} {X:.1f} {Y:.1f})"/>')

    # Text auf Flächen
    def text_y(self, y, x, z, txt, size=0.6, cls="lbl", anchor="start"):
        X, Y = self.p(x, y, z)
        self.out.append(
            f'<text class="{c(cls)}" font-size="{size*self.s:.1f}" text-anchor="{anchor}" transform="matrix({C30:.4f} {S30:.4f} 0 1 {X:.1f} {Y:.1f})">{txt}</text>')

    def text_x(self, x, y, z, txt, size=0.6, cls="lbl", anchor="start"):
        X, Y = self.p(x, y, z)
        self.out.append(
            f'<text class="{c(cls)}" font-size="{size*self.s:.1f}" text-anchor="{anchor}" transform="matrix({C30:.4f} {-S30:.4f} 0 1 {X:.1f} {Y:.1f})">{txt}</text>')

    def text_z(self, z, x, y, txt, size=0.8, cls="lbl", anchor="start", along="x"):
        X, Y = self.p(x, y, z)
        if along == "x":
            m = f"{C30:.4f} {S30:.4f} {-C30:.4f} {S30:.4f}"
        else:  # entlang -y gelesen
            m = f"{C30:.4f} {-S30:.4f} {C30:.4f} {S30:.4f}"
        self.out.append(
            f'<text class="{c(cls)}" font-size="{size*self.s:.1f}" text-anchor="{anchor}" transform="matrix({m} {X:.1f} {Y:.1f})">{txt}</text>')

    # --- Komposita ----------------------------------------------------
    def floor_grid(self, x0, y0, x1, y1, step=1, z=0, cls="g"):
        x = x0
        while x <= x1 + 1e-6:
            self.line((x, y0, z), (x, y1, z), cls)
            x += step
        y = y0
        while y <= y1 + 1e-6:
            self.line((x0, y, z), (x1, y, z), cls)
            y += step

    def person(self, x, y, z=0, h=1.75, cls="l w", walking=False, tone=None):
        """Maßstabsfigur – aufrecht im Bildraum gezeichnet (wie in Architekturplänen)."""
        X, Y = self.p(x, y, z)
        s = self.s * h / 1.75
        head = 0.12 * s * 1.75
        stroke = tone or BLUE
        body_top = Y - 1.42 * s
        hip = Y - 0.82 * s
        sh = 0.24 * s
        legs = (f'M{X-0.07*s:.1f},{hip:.1f} L{X-(0.16 if walking else 0.08)*s:.1f},{Y:.1f} '
                f'M{X+0.07*s:.1f},{hip:.1f} L{X+(0.14 if walking else 0.08)*s:.1f},{Y:.1f}')
        torso = (f'M{X-sh:.1f},{body_top+0.12*s:.1f} Q{X-sh:.1f},{body_top:.1f} {X:.1f},{body_top:.1f} '
                 f'Q{X+sh:.1f},{body_top:.1f} {X+sh:.1f},{body_top+0.12*s:.1f} L{X+0.17*s:.1f},{hip+0.02*s:.1f} '
                 f'L{X-0.17*s:.1f},{hip+0.02*s:.1f} Z')
        self._track(X, body_top - head * 2.6)
        self.out.append(f'<g style="stroke:{stroke}"><path class="x-l x-n" d="{legs}"/>'
                        f'<path class="{c(cls)}" d="{torso}"/>'
                        f'<circle class="{c(cls)}" cx="{X:.1f}" cy="{body_top-head*1.25:.1f}" r="{head:.1f}"/></g>')

    def tree(self, x, y, z=0, h=4.2, r=1.4):
        X, Y = self.p(x, y, z)
        top = self.p(x, y, z + h - r * 0.8)
        self.out.append(f'<line class="x-l" style="stroke:{SAGE}" x1="{X:.1f}" y1="{Y:.1f}" x2="{top[0]:.1f}" y2="{top[1]:.1f}"/>')
        cx, cy = self.p(x, y, z + h - r * 0.4)
        self._track(cx, cy, r * self.s + 2)
        self.out.append(f'<circle class="x-sage" stroke-width="1.15" cx="{cx:.1f}" cy="{cy:.1f}" r="{r*self.s:.1f}"/>')

    def plant(self, x, y, z=0, s=0.6):
        self.box(x - s / 2, y - s / 2, z, s, s, s * 1.1)
        cx, cy = self.p(x, y, z + s * 1.1 + s * 0.9)
        self.out.append(f'<circle class="x-sage" stroke-width="1.15" cx="{cx:.1f}" cy="{cy:.1f}" r="{s*0.95*self.s:.1f}"/>')

    def chair(self, x, y, z=0, facing="x", c="l t"):
        # Sitz + Lehne
        self.box(x, y, z + 0.45, 0.5, 0.5, 0.06, c, "l r", "l f")
        if facing == "x":   # Lehne an der -x Seite
            self.box(x, y, z + 0.51, 0.07, 0.5, 0.45, c, "l r", "l f")
        else:               # Lehne an der -y Seite
            self.box(x, y, z + 0.51, 0.5, 0.07, 0.45, c, "l r", "l f")
        self.line((x + 0.05, y + 0.45, z), (x + 0.05, y + 0.45, z + 0.45))
        self.line((x + 0.45, y + 0.45, z), (x + 0.45, y + 0.45, z + 0.45))
        self.line((x + 0.45, y + 0.05, z), (x + 0.45, y + 0.05, z + 0.45))

    def car(self, x, y, z=0, along="y"):
        # Auto in Längsrichtung y (Front zeigt nach +y)
        self.box(x, y, z + 0.2, 1.8, 4.3, 0.62)
        b, t = z + 0.82, z + 1.36
        self.poly([(x + 1.72, y + 0.8, b), (x + 1.72, y + 3.3, b), (x + 1.58, y + 2.75, t), (x + 1.58, y + 1.25, t)], "l glass")
        self.poly([(x + 0.08, y + 3.3, b), (x + 1.72, y + 3.3, b), (x + 1.58, y + 2.75, t), (x + 0.22, y + 2.75, t)], "l glass")
        self.poly([(x + 0.22, y + 1.25, t), (x + 1.58, y + 1.25, t), (x + 1.58, y + 2.75, t), (x + 0.22, y + 2.75, t)], "l t")
        self.line((x + 1.72, y + 2.05, b), (x + 1.58, y + 2.05, t))
        for yy in (0.85, 3.4):
            self.circle_x(x + 1.8, y + yy, z + 0.34, 0.34, "l w")

    def svg(self, w, h, title, extra_style="", bg=None, fit=True, pad=14):
        bgr = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
        vb = f"0 0 {w} {h}"
        if fit:
            x0, y0, x1, y1 = self.bb
            vb = f"{x0-pad:.0f} {y0-pad:.0f} {x1-x0+2*pad:.0f} {y1-y0+2*pad:.0f}"
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="{title}">'
                f'<style>{STYLE}{extra_style}</style>{bgr}'
                + "".join(self.out) + "</svg>")
