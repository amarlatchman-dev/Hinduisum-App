"""Core of the painting toolkit: a Scene collects SVG layers and raster effects.

Scenes are drawn at 1600 x 1000. Each run of SVG is rendered by Chromium (render.js) to a
transparent PNG; compose.py stacks the layers and applies the raster effects (fx.py) in
order, and finish.py grades the result. Everything is procedural and original.
"""
import math
import random

W, H = 1600, 1000


def f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def pts_d(pts, close=True):
    d = "M" + "L".join(f"{f(x)} {f(y)}" for x, y in pts)
    return d + ("Z" if close else "")


def mix(c1, c2, t):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(a, b))


def _stops(stops):
    return [s if len(s) == 3 else (s[0], s[1], 1) for s in stops]


class Scene:
    def __init__(self, seed=1):
        self.defs = []
        self.body = []
        self.ops = []
        self.rng = random.Random(seed)
        self.n = 0
        self.cache = {}

    def uid(self, p="i"):
        self.n += 1
        return f"{p}{self.n}"

    def add(self, s):
        self.body.append(s)
        return self

    # ---------- layers and raster effects ----------
    def fx(self, name, **kw):
        """Close the current SVG layer and apply a raster effect from fx.py to everything so far."""
        self._flush()
        self.ops.append(("fx", name, kw))

    def _flush(self):
        if self.body:
            self.ops.append(("svg", self.body))
            self.body = []

    def layers(self):
        self._flush()
        defs = "".join(self.defs)
        out = []
        for op in self.ops:
            if op[0] == "svg":
                out.append(("svg", f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
                                   f'<defs>{defs}</defs>{"".join(op[1])}</svg>'))
            else:
                out.append(op)
        return out

    def mark(self):
        return len(self.body)

    def wrap(self, start, gid):
        inner = "".join(self.body[start:])
        del self.body[start:]
        self.add(f'<g id="{gid}">{inner}</g>')
        return gid

    # ---------- paint servers and filters ----------
    def lin(self, stops, x1=0, y1=0, x2=0, y2=1, user=False):
        i = self.uid("g")
        units = ' gradientUnits="userSpaceOnUse"' if user else ""
        st = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in _stops(stops))
        self.defs.append(f'<linearGradient id="{i}" x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}"{units}>{st}</linearGradient>')
        return f"url(#{i})"

    def rad(self, stops, cx=0.5, cy=0.5, r=0.5, fx=None, fy=None, user=False, transform=None):
        i = self.uid("r")
        units = ' gradientUnits="userSpaceOnUse"' if user else ""
        fxy = f' fx="{f(fx)}" fy="{f(fy)}"' if fx is not None else ""
        tr = f' gradientTransform="{transform}"' if transform else ""
        st = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in _stops(stops))
        self.defs.append(f'<radialGradient id="{i}" cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}"{fxy}{units}{tr}>{st}</radialGradient>')
        return f"url(#{i})"

    def blur(self, sd):
        key = ("blur", sd)
        if key not in self.cache:
            i = self.uid("b")
            self.defs.append(f'<filter id="{i}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{sd}"/></filter>')
            self.cache[key] = f"url(#{i})"
        return self.cache[key]

    def gold_filter(self, scale=6, light="#fff4d6", az=225, el=42, spec=1.15, exp=22):
        """Embossed metal: the shape's own alpha becomes a bump map lit from one side."""
        key = ("gold", scale, az, el, spec, exp, light)
        if key not in self.cache:
            i = self.uid("au")
            self.defs.append(
                f'<filter id="{i}" x="-10%" y="-10%" width="120%" height="120%" color-interpolation-filters="sRGB">'
                f'<feGaussianBlur in="SourceAlpha" stdDeviation="{scale * .55:.1f}" result="b"/>'
                f'<feSpecularLighting in="b" surfaceScale="{scale}" specularConstant="{spec}" specularExponent="{exp}" lighting-color="{light}" result="s">'
                f'<feDistantLight azimuth="{az}" elevation="{el}"/></feSpecularLighting>'
                f'<feComposite in="s" in2="SourceAlpha" operator="in" result="s2"/>'
                f'<feDiffuseLighting in="b" surfaceScale="{scale}" diffuseConstant="1" lighting-color="#fff" result="d"><feDistantLight azimuth="{az}" elevation="{el + 8}"/></feDiffuseLighting>'
                f'<feComposite in="SourceGraphic" in2="d" operator="arithmetic" k1="1" k2="0" k3="0" k4="0" result="lit"/>'
                f'<feComposite in="lit" in2="s2" operator="arithmetic" k1="0" k2="1" k3="1" k4="0"/>'
                f'</filter>')
            self.cache[key] = f"url(#{i})"
        return self.cache[key]

    def grain(self, freq=0.8, octaves=3, opacity=0.08, seed=3, color="#fff"):
        """A noise texture filter for stone, clay or paper (apply to a filled shape)."""
        i = self.uid("t")
        r, g, b = (int(color[k:k + 2], 16) / 255 for k in (1, 3, 5))
        self.defs.append(
            f'<filter id="{i}" x="0" y="0" width="100%" height="100%">'
            f'<feTurbulence type="fractalNoise" baseFrequency="{freq}" numOctaves="{octaves}" seed="{seed}"/>'
            f'<feColorMatrix values="0 0 0 0 {r:.3f}  0 0 0 0 {g:.3f}  0 0 0 0 {b:.3f}  {opacity * 4:.2f} 0 0 0 {-opacity * 1.5:.2f}"/>'
            f'<feComposite in2="SourceGraphic" operator="in"/></filter>')
        return f"url(#{i})"

    def clip(self, d):
        i = self.uid("c")
        self.defs.append(f'<clipPath id="{i}"><path d="{d}"/></clipPath>')
        return f"url(#{i})"

    def mask_fade(self, x, y, w, h, top=1, bottom=0, horizontal=False):
        i = self.uid("m")
        g = self.lin([(0, "#fff", top), (1, "#fff", bottom)], 0, 0, 1 if horizontal else 0, 0 if horizontal else 1)
        self.defs.append(f'<mask id="{i}" maskUnits="userSpaceOnUse" x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}"><rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="{g}"/></mask>')
        return f"url(#{i})"

    def mask_radial(self, cx, cy, r, inner=0.5):
        i = self.uid("m")
        g = self.rad([(0, "#fff", 1), (inner, "#fff", 1), (1, "#fff", 0)], cx, cy, r, user=True)
        self.defs.append(f'<mask id="{i}" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="{g}"/></mask>')
        return f"url(#{i})"

    # ---------- skies and light ----------
    def sky(self, stops, y0=0, y1=H):
        self.add(f'<rect width="{W}" height="{H}" fill="{self.lin(stops, 0, y0, 0, y1, user=True)}"/>')

    def glow(self, cx, cy, r, color, a=1.0, mid=0.35, sy=1.0, blend=True):
        g = self.rad([(0, color, a), (mid, color, a * 0.42), (0.7, color, a * 0.1), (1, color, 0)], cx, cy, r, user=True,
                     transform=f"translate(0 {f(cy * (1 - sy))}) scale(1 {sy})" if sy != 1 else None)
        st = ' style="mix-blend-mode:screen"' if blend else ""
        self.add(f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(r)}" ry="{f(r * sy)}" fill="{g}"{st}/>')

    def sun(self, cx, cy, r, core="#fffaf0", rim="#ffd890", halo="#ffb066", halo_r=None, halo_a=0.6):
        self.glow(cx, cy, halo_r or r * 10, halo, halo_a, 0.16)
        self.glow(cx, cy, r * 3, rim, 0.8, 0.3)
        g = self.rad([(0, "#ffffff", 1), (0.6, core, 1), (1, rim, 1)], cx, cy, r, user=True)
        self.add(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{g}"/>')

    def moon(self, cx, cy, r, color="#f7f1e0", glow="#c9d4ff", glow_r=None, sky=None, crescent=0.0, seed=4):
        self.glow(cx, cy, glow_r or r * 7, glow, 0.4, 0.14)
        g = self.rad([(0, "#ffffff", 1), (0.65, color, 1), (1, "#d8cfb8", 1)], cx - r * .25, cy - r * .3, r * 1.35, user=True)
        self.add(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{g}"/>')
        rng = random.Random(seed)
        maria = []
        for _ in range(9):
            a = rng.uniform(0, 6.28); dd = rng.uniform(0, r * .62); cr = rng.uniform(r * .08, r * .22)
            maria.append(f'<ellipse cx="{f(cx + math.cos(a) * dd)}" cy="{f(cy + math.sin(a) * dd)}" rx="{f(cr)}" ry="{f(cr * .8)}" fill="#a9a08a" opacity=".2"/>')
        self.add(f'<g filter="{self.blur(max(1, r * .05))}">{"".join(maria)}</g>')
        if crescent and sky:
            self.add(f'<circle cx="{f(cx + r * crescent)}" cy="{f(cy - r * .12)}" r="{f(r * 1.02)}" fill="{sky}"/>')

    def stars(self, n, y0=0, y1=600, seed=None, bright=0.95, x0=0, x1=W, color="#fff8ea"):
        rng = random.Random(seed) if seed is not None else self.rng
        out = []
        for _ in range(n):
            x = rng.uniform(x0, x1); y = y0 + (rng.random() ** 1.4) * (y1 - y0)
            r = rng.choice([0.6, 0.8, 0.9, 1.1, 1.3, 1.6, 2.0])
            a = rng.uniform(0.2, bright) * (1 - (y - y0) / max(1, (y1 - y0)) * 0.7)
            out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" fill="{color}" opacity="{a:.2f}"/>')
        for _ in range(max(1, n // 50)):
            x = rng.uniform(x0 + 60, x1 - 60); y = rng.uniform(y0, y0 + (y1 - y0) * .6)
            out.append(self.sparkle(x, y, rng.uniform(7, 14)))
        self.add("".join(out))

    def sparkle(self, x, y, s, color="#fff6dc", a=0.9):
        k = 0.1
        return (f'<g opacity="{a}" style="mix-blend-mode:screen"><circle cx="{f(x)}" cy="{f(y)}" r="{f(s * .9)}" fill="{color}" opacity=".18" filter="{self.blur(max(1, s * .3))}"/>'
                f'<path d="M{f(x)} {f(y - s)}L{f(x + s * k)} {f(y - s * k)}L{f(x + s)} {f(y)}L{f(x + s * k)} {f(y + s * k)}'
                f'L{f(x)} {f(y + s)}L{f(x - s * k)} {f(y + s * k)}L{f(x - s)} {f(y)}L{f(x - s * k)} {f(y - s * k)}Z" fill="{color}"/>'
                f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(s * .16)}" fill="#fff"/></g>')

    def rays(self, cx, cy, n=14, length=1100, width=0.05, color="#ffe2a0", a=0.16, spread=(0, 360), seed=None, blur=6):
        rng = random.Random(seed) if seed is not None else self.rng
        g = self.rad([(0, color, a), (0.55, color, a * .3), (1, color, 0)], cx, cy, length, user=True)
        parts = []
        for _ in range(n):
            ang = math.radians(rng.uniform(*spread))
            w = width * rng.uniform(0.4, 1.6)
            x1, y1 = cx + math.cos(ang - w) * length, cy + math.sin(ang - w) * length
            x2, y2 = cx + math.cos(ang + w) * length, cy + math.sin(ang + w) * length
            parts.append(f'M{f(cx)} {f(cy)}L{f(x1)} {f(y1)}L{f(x2)} {f(y2)}Z')
        self.add(f'<path d="{"".join(parts)}" fill="{g}" filter="{self.blur(blur)}" style="mix-blend-mode:screen"/>')

    def bokeh(self, n, x0, x1, y0, y1, colors=("#ffd27a",), r=(4, 18), a=(0.15, 0.6), blur=2.5, seed=None, ring=False):
        rng = random.Random(seed) if seed is not None else self.rng
        out = []
        for _ in range(n):
            c = rng.choice(colors)
            cx, cy, rr, aa = rng.uniform(x0, x1), rng.uniform(y0, y1), rng.uniform(*r), rng.uniform(*a)
            out.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(rr)}" fill="{c}" opacity="{aa:.2f}"/>')
            if ring:
                out.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(rr * .92)}" fill="none" stroke="{c}" stroke-width="{f(rr * .12)}" opacity="{aa * .8:.2f}"/>')
        self.add(f'<g filter="{self.blur(blur)}" style="mix-blend-mode:screen">{"".join(out)}</g>')

    def motes(self, n, x0, x1, y0, y1, color="#ffe6a8", seed=None, size=(1.0, 2.8), glow=4):
        """Tiny glowing specks of gold dust or fireflies."""
        rng = random.Random(seed) if seed is not None else self.rng
        out, gl = [], []
        for _ in range(n):
            x, y, r = rng.uniform(x0, x1), rng.uniform(y0, y1), rng.uniform(*size)
            a = rng.uniform(.4, 1)
            out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="#fffaf0" opacity="{a:.2f}"/>')
            gl.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r * glow)}" fill="{color}" opacity="{a * .4:.2f}"/>')
        self.add(f'<g filter="{self.blur(3)}" style="mix-blend-mode:screen">{"".join(gl)}</g><g style="mix-blend-mode:screen">{"".join(out)}</g>')

    def mist(self, y, h, color="#ffffff", a=0.35, blur=30, x0=-100, x1=W + 100):
        g = self.lin([(0, color, 0), (0.5, color, a), (1, color, 0)], 0, y - h / 2, 0, y + h / 2, user=True)
        self.add(f'<rect x="{f(x0)}" y="{f(y - h / 2)}" width="{f(x1 - x0)}" height="{f(h)}" fill="{g}" filter="{self.blur(blur)}"/>')

    def wisps(self, n, x0, x1, y0, y1, color="#ffffff", a=(0.08, 0.25), length=(160, 520), thick=(4, 14), blur=10, seed=None):
        """Long thin streaks of high cloud or river mist."""
        rng = random.Random(seed) if seed is not None else self.rng
        out = []
        for _ in range(n):
            cx, cy, L = rng.uniform(x0, x1), rng.uniform(y0, y1), rng.uniform(*length)
            t = rng.uniform(*thick)
            out.append(f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(L / 2)}" ry="{f(t / 2)}" fill="{color}" opacity="{rng.uniform(*a):.2f}"/>')
        self.add(f'<g filter="{self.blur(blur)}">{"".join(out)}</g>')

    def birds(self, n, x0, x1, y0, y1, color="#2a1a14", s=(6, 12), seed=None, a=1.0):
        rng = random.Random(seed) if seed is not None else self.rng
        out = []
        for _ in range(n):
            x, y, w = rng.uniform(x0, x1), rng.uniform(y0, y1), rng.uniform(*s)
            up = rng.uniform(.25, .7)
            out.append(f'<path d="M{f(x - w)} {f(y - w * up * .5)}Q{f(x - w * .45)} {f(y - w * up)} {f(x)} {f(y)}Q{f(x + w * .45)} {f(y - w * up)} {f(x + w)} {f(y - w * up * .5)}'
                       f'Q{f(x + w * .45)} {f(y - w * up * .6)} {f(x)} {f(y + w * .12)}Q{f(x - w * .45)} {f(y - w * up * .6)} {f(x - w)} {f(y - w * up * .5)}Z" fill="{color}"/>')
        self.add(f'<g opacity="{a}">{"".join(out)}</g>')

    # ---------- fire ----------
    def flame(self, cx, cy, h, glow=True, glow_r=None, lean=0.0, glow_a=0.55, seed=None):
        """A lamp flame whose base sits at (cx, cy)."""
        w = h * 0.34
        tip = cx + lean * h
        if glow:
            self.glow(cx, cy - h * .45, glow_r or h * 5.5, "#ff9440", glow_a, 0.12)
            self.glow(cx, cy - h * .45, h * 1.5, "#ffd890", 0.85, 0.3)
        g = self.rad([(0, "#ffffff", 1), (0.3, "#fff4c8", 1), (0.62, "#ffb640", 1), (0.86, "#f06a1e", .8), (1, "#c2351a", 0)], 0.5, 0.78, 0.75)
        d = (f"M{f(tip)} {f(cy - h)}C{f(cx + w * .3 + lean * h * .5)} {f(cy - h * .68)} {f(cx + w)} {f(cy - h * .42)} {f(cx + w * .82)} {f(cy - h * .15)}"
             f"C{f(cx + w * .66)} {f(cy + h * .06)} {f(cx - w * .66)} {f(cy + h * .06)} {f(cx - w * .82)} {f(cy - h * .15)}"
             f"C{f(cx - w)} {f(cy - h * .42)} {f(cx - w * .3 + lean * h * .5)} {f(cy - h * .68)} {f(tip)} {f(cy - h)}Z")
        blue = f'<ellipse cx="{f(cx)}" cy="{f(cy - h * .06)}" rx="{f(w * .5)}" ry="{f(h * .09)}" fill="#6f8cff" opacity=".45" filter="{self.blur(max(.6, h * .02))}"/>'
        core = (f"M{f(cx + lean * h * .3)} {f(cy - h * .64)}C{f(cx + w * .3)} {f(cy - h * .42)} {f(cx + w * .4)} {f(cy - h * .18)} {f(cx)} {f(cy - h * .05)}"
                f"C{f(cx - w * .4)} {f(cy - h * .18)} {f(cx - w * .3)} {f(cy - h * .42)} {f(cx + lean * h * .3)} {f(cy - h * .64)}Z")
        self.add(f'<path d="{d}" fill="{g}" filter="{self.blur(max(.5, h * .012))}"/>{blue}<path d="{core}" fill="#fffef8" opacity=".92" filter="{self.blur(max(.8, h * .03))}"/>')

    def smoke(self, x, y, h, color="#e8dccb", a=0.22, seed=None, width=1.0, drift=0.0):
        """A thin curl of incense smoke rising from (x, y)."""
        rng = random.Random(seed) if seed is not None else self.rng
        out = []
        for strand in range(3):
            px, py = x, y
            d = f"M{f(px)} {f(py)}"
            amp = 6 * width
            ph = rng.uniform(0, 6.28)
            steps = 14
            for k in range(1, steps + 1):
                t = k / steps
                ny = y - h * t
                nx = x + math.sin(ph + t * 7 + strand) * amp * (1 + t * 5) + drift * h * t * t
                cx1 = px + (nx - px) * .5 + rng.uniform(-4, 4) * width
                d += f"Q{f(cx1)} {f((py + ny) / 2)} {f(nx)} {f(ny)}"
                px, py = nx, ny
            out.append(f'<path d="{d}" stroke="{color}" stroke-width="{f((1.2 + strand) * width)}" fill="none" opacity="{a * (1 - strand * .25):.2f}" stroke-linecap="round"/>')
        m = self.mask_fade(x - h, y - h, 2 * h, h, 0, 1)
        self.add(f'<g mask="{m}" filter="{self.blur(1.6 * width)}">{"".join(out)}</g>')
