"""Festival and home paintings: Diwali, rangoli, Holi, Garba, Sankranti kites and the
household rites (griha pravesh, vivaha, namkaran, mundan), the offering of Gita 9.26,
the home shrine and the six darshanas."""
from scenes import scene

import math
import random

import numpy as np
from scipy import ndimage

import fx
import objects as ob
from land import crown, smooth_line, y_at
from paint import H, W, f, mix, pts_d


# ======================================================================
# small geometry helpers
# ======================================================================
def _hull(pts):
    pts = sorted(set((round(x, 2), round(y, 2)) for x, y in pts))
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(hi) >= 2 and cross(hi[-2], hi[-1], p) <= 0:
            hi.pop()
        hi.append(p)
    return lo[:-1] + hi[:-1]


def _petal(w, h, pinch=0.0):
    """A pointed petal from the origin up to (0, -h)."""
    return (f"M0 0C{f(-w * .62)} {f(-h * .12)} {f(-w * .58)} {f(-h * (.72 - pinch))} 0 {f(-h)}"
            f"C{f(w * .58)} {f(-h * (.72 - pinch))} {f(w * .62)} {f(-h * .12)} 0 0Z")


def _round_petal(w, h):
    """A rounded petal (tip is a curve) from the origin up to (0, -h)."""
    return (f"M0 0C{f(-w * .7)} {f(-h * .15)} {f(-w * .62)} {f(-h * .95)} 0 {f(-h)}"
            f"C{f(w * .62)} {f(-h * .95)} {f(w * .7)} {f(-h * .15)} 0 0Z")


def _leaf(w, L):
    """A lanceolate (mango) leaf hanging from the origin down to (0, L)."""
    return (f"M0 0C{f(w * .62)} {f(L * .18)} {f(w * .58)} {f(L * .66)} 0 {f(L)}"
            f"C{f(-w * .58)} {f(L * .66)} {f(-w * .62)} {f(L * .18)} 0 0Z")


def powder_filter(s, scale=3.0, freq=0.9, seed=2, speck=0.18):
    """Coloured-powder texture: ragged, grainy edges and a speckled surface."""
    i = s.uid("pw")
    s.defs.append(
        f'<filter id="{i}" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">'
        f'<feTurbulence type="fractalNoise" baseFrequency="{freq}" numOctaves="2" seed="{seed}" result="n"/>'
        f'<feDisplacementMap in="SourceGraphic" in2="n" scale="{scale}" xChannelSelector="R" yChannelSelector="G" result="d"/>'
        f'<feTurbulence type="fractalNoise" baseFrequency="1.7" numOctaves="1" seed="{seed + 5}" result="g"/>'
        f'<feColorMatrix in="g" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  {speck * 5:.2f} 0 0 0 {-speck * 2.4:.2f}" result="ga"/>'
        f'<feComposite in="ga" in2="d" operator="in" result="gw"/>'
        f'<feTurbulence type="fractalNoise" baseFrequency="1.3" numOctaves="1" seed="{seed + 9}" result="h"/>'
        f'<feColorMatrix in="h" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  {speck * 5:.2f} 0 0 0 {-speck * 2.6:.2f}" result="ha"/>'
        f'<feComposite in="ha" in2="d" operator="in" result="hd"/>'
        f'<feMerge><feMergeNode in="d"/><feMergeNode in="gw"/><feMergeNode in="hd"/></feMerge></filter>')
    return f"url(#{i})"


# ======================================================================
# lamps
# ======================================================================
def diya(s, x, y, sc=1.0, k=0.36, lip=90, flame_h=None, clay="#a8441c", glow_a=0.5, glow_r=None, dots=True,
         lit=1.0, flame=True, shadow=True, seed=1):
    """A small clay diya seen from above at an angle; (x, y) is the centre of the rim.
    k is the foreshortening of the rim (0 side-on .. 1 straight down); lip is the
    direction of the pinched spout in the floor plane (90 points at the viewer).
    About 64 * sc wide.  Returns the flame base."""
    r = 26 * sc
    a0 = math.radians(lip)
    rim = []
    for t in range(0, 360, 6):
        a = math.radians(t)
        c = max(0.0, math.cos(a - a0))
        rr = r * (1 + .42 * c ** 7)
        rim.append((x + math.cos(a) * rr, y + math.sin(a) * rr * k))
    depth = 17 * sc * math.sqrt(max(0.05, 1 - k * k))
    bot = [(x + (px - x) * .56, y + (py - y) * .56 + depth) for px, py in rim]
    body = _hull(rim + bot)
    lip_x = x + math.cos(a0) * r * 1.3
    lip_y = y + math.sin(a0) * r * 1.3 * k
    if shadow:
        s.add(f'<ellipse cx="{f(x)}" cy="{f(y + depth + 2 * sc)}" rx="{f(r * 1.25)}" ry="{f(r * (k * .9 + .12))}" fill="#000" opacity=".5" filter="{s.blur(max(1, 4 * sc))}"/>')
    g = s.lin([(0, mix(clay, "#ffc890", .35 * lit), 1), (0.45, clay, 1), (1, mix(clay, "#100400", .78), 1)], 0, y - r * k, 0, y + depth, user=True)
    sh = s.lin([(0, "#000", .45), (0.35, "#000", 0), (0.7, "#000", 0), (1, "#000", .35)], x - r * 1.3, 0, x + r * 1.3, 0, user=True)
    out = [f'<path d="{pts_d(body)}" fill="{g}"/><path d="{pts_d(body)}" fill="{sh}"/>']
    if dots and k < .8:
        rng = random.Random(seed)
        dd = []
        for j in range(11):
            t = math.pi * (j + .5) / 11
            px = x - math.cos(t) * r * .92
            py = y + math.sin(t) * r * k * .92 + depth * .45
            dd.append(f'<circle cx="{f(px)}" cy="{f(py)}" r="{f(1.7 * sc)}" fill="{"#fbe7b8" if j % 2 else "#f2b232"}" opacity="{.5 + .4 * math.sin(t):.2f}"/>')
        out.append("".join(dd))
    rim_g = s.lin([(0, mix(clay, "#ffd8a8", .55 * lit), 1), (1, mix(clay, "#2a0a02", .35), 1)], 0, y - r * k, 0, y + r * k, user=True)
    out.append(f'<path d="{pts_d(rim)}" fill="{rim_g}"/>')
    inner = [(x + (px - x) * .8, y + (py - y) * .8 + 1.2 * sc * (1 - k)) for px, py in rim]
    out.append(f'<path d="{pts_d(inner)}" fill="#2a1004"/>')
    oil = [(x + (px - x) * .7, y + (py - y) * .7 + 2 * sc * (1 - k)) for px, py in rim]
    og = s.rad([(0, "#ffe7a0", .95), (0.35, "#e2a03a", .9), (1, "#6a2c08", .9)], lip_x, lip_y, r * 1.4, user=True)
    out.append(f'<path d="{pts_d(oil)}" fill="{og}"/>')
    out.append(f'<path d="M{f(x + (lip_x - x) * .2)} {f(y + (lip_y - y) * .2)}L{f(lip_x)} {f(lip_y - 1.5 * sc)}" stroke="#f6e8cc" stroke-width="{f(2.6 * sc)}" stroke-linecap="round"/>')
    s.add("".join(out))
    if flame:
        fh = flame_h or 34 * sc
        s.flame(lip_x, lip_y - 1.5 * sc, fh, glow_r=glow_r or fh * 5, glow_a=glow_a)
    return lip_x, lip_y


def firework(s, cx, cy, r, color="#ffd27a", core="#fffbe8", n=72, seed=1, droop=0.22, a=1.0, width=1.6, trail=True,
             crackle=True, ring=None):
    """A chrysanthemum shell bursting far off: drooping streaks of sparks around a hot centre."""
    rng = random.Random(seed)
    sg = s.rad([(0, color, 0), (0.3, color, .12 * a), (0.75, core, .9 * a), (0.92, color, .9 * a), (1, color, .2 * a)], cx, cy + droop * r * .5, r * 1.08, user=True)
    d, tips = [], []
    for i in range(n):
        ang = 2 * math.pi * i / n + rng.uniform(-.06, .06)
        L = r * rng.uniform(.72, 1.0)
        pts = []
        for j in range(9):
            t = .18 + .82 * j / 8
            pts.append((cx + math.cos(ang) * L * t, cy + math.sin(ang) * L * t + droop * r * t * t))
        d.append(pts_d(pts, close=False))
        tips.append(pts[-1])
    dd = "".join(d)
    s.glow(cx, cy, r * 1.9, color, .22 * a, .25)
    s.add(f'<g style="mix-blend-mode:screen"><path d="{dd}" stroke="{sg}" stroke-width="{f(width * 3.5)}" fill="none" stroke-linecap="round" filter="{s.blur(width * 2.2)}" opacity=".8"/>'
          f'<path d="{dd}" stroke="{sg}" stroke-width="{f(width)}" fill="none" stroke-linecap="round"/></g>')
    sp = []
    for (x, y) in tips:
        if rng.random() < .7:
            sp.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(width * rng.uniform(.8, 1.6))}" fill="{core}" opacity="{a * rng.uniform(.6, 1):.2f}"/>')
        if crackle and rng.random() < .5:
            x2, y2 = x + rng.uniform(-.08, .08) * r, y + rng.uniform(.04, .2) * r
            sp.append(f'<circle cx="{f(x2)}" cy="{f(y2)}" r="{f(width * .7)}" fill="{color}" opacity="{a * rng.uniform(.3, .7):.2f}"/>')
    if ring:
        for i in range(n // 2):
            ang = 2 * math.pi * i / (n // 2)
            x, y = cx + math.cos(ang) * r * .45, cy + math.sin(ang) * r * .45 + droop * r * .2
            sp.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(width * 1.2)}" fill="{ring}" opacity="{a * .9:.2f}"/>')
    s.add(f'<g style="mix-blend-mode:screen">{"".join(sp)}</g>')
    s.glow(cx, cy + r * .05, r * .32, core, .55 * a, .3)
    if trail:
        tr = [(cx + math.sin(j * .9 + seed) * 2.5, cy + r * .2 + j * r * .09) for j in range(14)]
        tg = s.lin([(0, color, .7 * a), (1, color, 0)], 0, cy, 0, cy + r * 1.4, user=True)
        s.add(f'<path d="{pts_d(tr, False)}" stroke="{tg}" stroke-width="{f(width * 1.2)}" fill="none" filter="{s.blur(.8)}" style="mix-blend-mode:screen"/>')


# ======================================================================
# garlands and leaves
# ======================================================================
def mango_leaf(x, y, L, w, rot=0.0, dark="#1f4a1e", light="#5f9a3a", rim=None, s=None):
    """A hanging mango leaf (SVG string) whose stalk is at (x, y)."""
    g = s.lin([(0, light, 1), (0.6, mix(light, dark, .5), 1), (1, dark, 1)], 0, 0, 1, 1) if s else light
    out = (f'<g transform="translate({f(x)} {f(y)}) rotate({rot:.1f})"><path d="{_leaf(w, L)}" fill="{g}"/>'
           f'<path d="M0 0Q{f(w * .06)} {f(L * .5)} 0 {f(L * .96)}" stroke="#d8e8a0" stroke-opacity=".45" stroke-width="{f(max(.8, w * .06))}" fill="none"/>')
    if rim:
        out += f'<path d="M0 0C{f(-w * .62)} {f(L * .18)} {f(-w * .58)} {f(L * .66)} 0 {f(L)}" stroke="{rim}" stroke-opacity=".5" stroke-width="{f(max(.8, w * .07))}" fill="none"/>'
    return out + "</g>"


def toran(s, x0, x1, y, sag=10, leaf=60, n=None, marigold_r=8, strands=True, seed=1, rim=None, colors=("#f39a1c", "#f7c02a", "#e8562a"),
          dark="#1f4a1e", light="#5f9a3a", strand_len=4):
    """A doorway toran: a cord of marigolds with mango leaves and marigold strands hanging from it."""
    rng = random.Random(seed)
    n = n or max(5, int((x1 - x0) / (leaf * .34)))

    def cy(t):
        return y + sag * 4 * t * (1 - t)
    out = []
    # leaves and strands hang behind the cord
    for i in range(n):
        t = (i + .5) / n
        x = x0 + (x1 - x0) * t
        yy = cy(t)
        if strands and i % 3 == 1:
            for j in range(strand_len):
                out.append(ob.marigold(x + rng.uniform(-1, 1), yy + marigold_r * (1.1 + j * 1.55), marigold_r * (1 - j * .06),
                                       colors[(i + j) % len(colors)], seed * 50 + i * 7 + j))
        else:
            out.append(mango_leaf(x, yy, leaf * rng.uniform(.88, 1.08), leaf * .3, rng.uniform(-9, 9), dark, light, rim, s))
    # the cord of small marigolds along the top
    m = int((x1 - x0) / (marigold_r * 1.3))
    for j in range(m + 1):
        t = j / m
        out.append(ob.marigold(x0 + (x1 - x0) * t, cy(t), marigold_r * 1.05, colors[(j // 2) % len(colors)], seed * 900 + j))
    s.add(f'<path d="M{f(x0)} {f(y + 8)}Q{f((x0 + x1) / 2)} {f(y + sag * 2 + 8)} {f(x1)} {f(y + 8)}" stroke="#000" stroke-opacity=".35" stroke-width="{f(marigold_r * 2.4)}" fill="none" filter="{s.blur(6)}"/>')
    s.add("".join(out))


# ======================================================================
# rangoli
# ======================================================================
RANGOLI = dict(white="#fbf3e2", magenta="#d6246e", pink="#f472a8", saffron="#f7861c", yellow="#ffc928",
               green="#2f9a4a", leaf="#7cc243", blue="#1e6fd0", teal="#1aa6a6", purple="#7a3cc0", red="#d8302a")


def rangoli_svg(s, R, seed=1, pal=None, rings=None):
    """A symmetric powder rangoli centred at the origin, radius R (SVG string, unfiltered)."""
    p = dict(RANGOLI, **(pal or {}))
    wh = p["white"]
    out = []

    def ring_of(n, r, shape, fill, stroke=None, sw=1.5, rot0=0.0, scale=1.0):
        parts = []
        for i in range(n):
            a = 360 * i / n + rot0
            parts.append(f'<path d="{shape}" transform="rotate({a:.2f}) translate(0 {f(-r)}) scale({scale})"/>')
        st = f' stroke="{stroke}" stroke-width="{f(sw)}" stroke-linejoin="round"' if stroke else ""
        return f'<g fill="{fill}"{st}>{"".join(parts)}</g>'

    def dots(n, r, rad, fill, rot0=0.0):
        return "".join(f'<circle cx="{f(math.cos(math.radians(360 * i / n + rot0)) * r)}" cy="{f(math.sin(math.radians(360 * i / n + rot0)) * r)}" r="{f(rad)}" fill="{fill}"/>' for i in range(n))

    # outer scalloped border of 24 lobes
    out.append(f'<circle r="{f(R * .985)}" fill="{p["purple"]}"/>')
    out.append(ring_of(24, R * .80, _round_petal(R * .23, R * .2), p["magenta"], wh, R * .008))
    out.append(dots(24, R * .955, R * .017, wh, 7.5))
    out.append(f'<circle r="{f(R * .80)}" fill="{p["yellow"]}"/>')
    # ring of 16 pointed saffron petals with inner yellow tongues
    out.append(ring_of(16, R * .54, _petal(R * .2, R * .27), p["saffron"], wh, R * .007))
    out.append(ring_of(16, R * .54, _petal(R * .09, R * .17), p["red"]))
    out.append(ring_of(16, R * .56, _petal(R * .14, R * .21), p["leaf"], wh, R * .006, 11.25))
    out.append(ring_of(16, R * .56, _petal(R * .055, R * .13), p["green"], None, 0, 11.25))
    out.append(dots(16, R * .77, R * .016, wh, 11.25))
    # blue band with white dots
    out.append(f'<circle r="{f(R * .56)}" fill="{p["blue"]}" stroke="{wh}" stroke-width="{f(R * .01)}"/>')
    out.append(f'<circle r="{f(R * .48)}" fill="{p["teal"]}" stroke="{wh}" stroke-width="{f(R * .007)}"/>')
    out.append(dots(32, R * .52, R * .012, wh))
    # eight big lotus petals
    out.append(ring_of(8, 0, _petal(R * .3, R * .46), p["pink"], wh, R * .009, 22.5))
    out.append(ring_of(8, 0, _petal(R * .18, R * .34), p["magenta"], None, 0, 22.5))
    out.append(ring_of(8, 0, _petal(R * .28, R * .44), p["white"], None, 0, 0, 1))
    out.append(ring_of(8, 0, _petal(R * .22, R * .39), p["yellow"], None, 0, 0))
    out.append(ring_of(8, 0, _petal(R * .12, R * .3), p["saffron"], None, 0, 0))
    # centre
    out.append(f'<circle r="{f(R * .15)}" fill="{p["green"]}" stroke="{wh}" stroke-width="{f(R * .008)}"/>')
    out.append(f'<circle r="{f(R * .1)}" fill="{p["yellow"]}"/>')
    out.append(f'<circle r="{f(R * .055)}" fill="{p["red"]}"/>')
    out.append(dots(8, R * .125, R * .012, wh, 22.5))
    out.append(f'<circle r="{f(R * .018)}" fill="{wh}"/>')
    return "".join(out)


def lay_rangoli(s, cx, cy, R, k=1.0, seed=1, pal=None, light=None, shade=0.0, rough=3.0, opacity=1.0):
    """Lay a powder rangoli on the floor at (cx, cy), foreshortened by k, optionally
    lit by a warm pool of light (lx, ly, radius)."""
    inner = rangoli_svg(s, R, seed, pal)
    pf = powder_filter(s, scale=rough, seed=seed)
    s.add(f'<g transform="translate({f(cx)} {f(cy)}) scale(1 {f(k)})" opacity="{opacity}"><g filter="{pf}">{inner}</g></g>')
    if shade:
        g = s.rad([(0, "#000", 0), (0.55, "#000", shade * .3), (1, "#000", shade)], cx, cy, R * 1.05, user=True,
                  transform=f"translate(0 {f(cy * (1 - k))}) scale(1 {f(k)})")
        s.add(f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(R)}" ry="{f(R * k)}" fill="{g}"/>')


# ======================================================================
# 1. Diwali doorway
# ======================================================================
def _house_wall(s, x0, x1, y0, y1, color, seed=3):
    s.add(f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(x1 - x0)}" height="{f(y1 - y0)}" fill="{color}"/>')
    s.add(f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(x1 - x0)}" height="{f(y1 - y0)}" fill="{color}" filter="{s.grain(0.008, 4, .45, seed, "#000000")}"/>')
    s.add(f'<rect x="{f(x0)}" y="{f(y0)}" width="{f(x1 - x0)}" height="{f(y1 - y0)}" fill="{color}" filter="{s.grain(0.5, 3, .14, seed + 1, "#ffe0c0")}"/>')


def _arch_d(x0, x1, top, bottom, cusp=True):
    """A cusped (multifoil) arch opening from x0 to x1, apex at top."""
    cx = (x0 + x1) / 2
    r = (x1 - x0) / 2
    spring = top + r * .95
    if not cusp:
        return f"M{f(x0)} {f(bottom)}V{f(spring)}A{f(r)} {f(r * .95)} 0 0 1 {f(x1)} {f(spring)}V{f(bottom)}Z"
    pts = []
    n = 5
    for i in range(n):
        a0 = math.pi + math.pi * i / n
        a1 = math.pi + math.pi * (i + 1) / n
        pts.append((a0, a1))
    d = f"M{f(x0)} {f(bottom)}V{f(spring)}"
    for a0, a1 in pts:
        xa, ya = cx + math.cos(a1) * r, spring + math.sin(a1) * r * .95
        d += f"A{f(r * .26)} {f(r * .26)} 0 0 1 {f(xa)} {f(ya)}"
    return d + f"V{f(bottom)}Z"


@scene
def diyas(s):
    s.sky([(0, "#05081c"), (.25, "#0b1238"), (.5, "#1a1a4c"), (.62, "#2e2250")], 0, 620)
    s.stars(70, 0, 300, seed=11, bright=.5)
    # far-off fireworks over the town (Diwali falls on the new moon: no moon tonight)
    firework(s, 300, 140, 100, "#ffc35a", seed=1, n=84, a=.8, width=1.3)
    firework(s, 1290, 112, 82, "#ff7ab4", core="#fff0f6", seed=2, n=70, a=.75, ring="#ffe6a0", width=1.2)
    firework(s, 1060, 205, 44, "#9fe8c8", core="#f4fff8", seed=3, n=44, a=.55, width=1.0)
    firework(s, 505, 228, 34, "#ffd890", seed=4, n=36, a=.45, width=.9, trail=False)
    s.fx("clouds", y0=0, y1=330, seed=7, cell=170, aniso=3.2, cover=.34, soft=.25, lit="#6a4a7a", body=.9, direct=.5,
         light=(0, -1), opacity=.45, top_fade=.2, bottom_fade=.4)
    # neighbours' houses beyond, their parapets lined with lamps
    rng = random.Random(5)
    for x0, x1, top in ((-40, 236, 410), (1364, 1640, 392)):
        s.add(f'<rect x="{x0}" y="{top}" width="{x1 - x0}" height="{1000 - top}" fill="#130e24"/>'
              f'<rect x="{x0 - 6}" y="{top - 6}" width="{x1 - x0 + 12}" height="10" fill="#1c1532"/>')
        wx = x0 + (x1 - x0) * .42
        d = _arch_d(wx - 34, wx + 34, top + 90, top + 210, cusp=False)
        s.add(f'<path d="{d}" fill="{s.rad([(0, "#ffd890", .9), (1, "#c86a28", .8)], wx, top + 190, 120, user=True)}"/>'
              f'<path d="M{f(wx - 11)} {top + 110}V{top + 210}M{f(wx + 11)} {top + 110}V{top + 210}" stroke="#1a0e14" stroke-width="4"/>'
              f'<rect x="{f(wx - 50)}" y="{top + 210}" width="100" height="8" fill="#241a36"/>')
        s.glow(wx, top + 170, 150, "#ff9a4a", .3, .3)
        for x in range(x0 + 12, x1, 27):
            s.flame(x + rng.uniform(-3, 3), top - 7, 8, glow_r=34, glow_a=.32)
        for j in range(3):
            s.flame(wx - 30 + j * 30, top + 212, 9, glow_r=40, glow_a=.35)

    # ---- the house ----
    x0, x1 = 250, 1350
    roof = 286
    dl, dr, dt, sill = 706, 894, 430, 754
    wall = "#40252a"
    s.add(f'<rect x="{x0}" y="{roof}" width="{x1 - x0}" height="{1000 - roof}" fill="{wall}"/>')
    s.add(f'<rect x="{x0}" y="{roof}" width="{x1 - x0}" height="{1000 - roof}" fill="{wall}" filter="{s.grain(0.01, 3, .12, 3, "#000000")}"/>')
    s.add(f'<rect x="{x0}" y="{roof}" width="{x1 - x0}" height="{1000 - roof}" fill="{wall}" filter="{s.grain(0.9, 2, .05, 4, "#ffd8b0")}"/>')
    # parapet with arched jaali cut-outs, and a cornice
    s.add(f'<rect x="{x0 - 14}" y="{roof - 40}" width="{x1 - x0 + 28}" height="40" fill="#3a2230"/>')
    jaali = "".join(f'<path d="M{x - 9} {roof - 8}V{roof - 22}A9 9 0 0 1 {x + 9} {roof - 22}V{roof - 8}Z"/>' for x in range(x0 + 20, x1 - 10, 34))
    s.add(f'<g fill="#120b1c">{jaali}</g>')
    s.add(f'<rect x="{x0 - 22}" y="{roof - 48}" width="{x1 - x0 + 44}" height="10" fill="#54323a"/>'
          f'<rect x="{x0 - 22}" y="{roof}" width="{x1 - x0 + 44}" height="14" fill="#5a3640"/>'
          f'<rect x="{x0 - 22}" y="{roof + 14}" width="{x1 - x0 + 44}" height="10" fill="#000" opacity=".4" filter="{s.blur(5)}"/>')
    for px in (x0 + 8, x1 - 44):
        s.add(f'<rect x="{px}" y="{roof + 14}" width="36" height="{760 - roof - 14}" fill="#4a2c36"/>'
              f'<rect x="{px + 30}" y="{roof + 14}" width="6" height="{760 - roof - 14}" fill="#000" opacity=".25"/>')
    # windows with open shutters, lit from inside
    for wx in (452, 1148):
        wl, wr, wt, wb = wx - 66, wx + 66, 440, 620
        d = _arch_d(wl, wr, wt, wb)
        s.add(f'<path d="{d}" fill="#000" opacity=".55" transform="translate(0 8)" filter="{s.blur(9)}"/>')
        s.add(f'<path d="{d}" fill="none" stroke="#6a3e40" stroke-width="20"/><path d="{d}" fill="none" stroke="#2a1416" stroke-width="3" transform="translate(0 0)"/>')
        ig = s.rad([(0, "#fff0c0", 1), (0.4, "#ffbe64", 1), (1, "#b2501c", 1)], wx, wb - 30, 170, user=True)
        s.add(f'<path d="{d}" fill="{ig}"/>')
        bars = "".join(f"M{f(wl + (wr - wl) * t / 5)} {wt}V{wb}" for t in range(1, 5))
        s.add(f'<g clip-path="{s.clip(d)}"><path d="{bars}" stroke="#2a1410" stroke-width="4"/><path d="M{wl} {wt + 66}H{wr}" stroke="#2a1410" stroke-width="4"/></g>')
        for side in (-1, 1):
            sx = wl - 10 if side < 0 else wr + 10
            s.add(f'<path d="M{sx} {wt + 40}L{sx + side * 46} {wt + 50}V{wb + 4}L{sx} {wb}Z" fill="#4a2318"/>'
                  f'<path d="M{sx + side * 9} {wt + 58}L{sx + side * 37} {wt + 64}V{wb - 10}L{sx + side * 9} {wb - 13}Z" fill="none" stroke="#8a4a26" stroke-width="2"/>'
                  f'<path d="M{sx} {wt + 40}L{sx + side * 46} {wt + 50}" stroke="#ffb870" stroke-opacity=".35" stroke-width="2"/>')
        s.add(f'<rect x="{wl - 22}" y="{wb}" width="{wr - wl + 44}" height="14" fill="#64404a"/>'
              f'<rect x="{wl - 22}" y="{wb}" width="{wr - wl + 44}" height="3" fill="#ffd0a0" opacity=".55"/>'
              f'<rect x="{wl - 22}" y="{wb + 14}" width="{wr - wl + 44}" height="8" fill="#000" opacity=".35" filter="{s.blur(3)}"/>')
        s.glow(wx, wb - 70, 250, "#ff9a4a", .26, .3)
    # ---- the doorway: carved frame, lintel and a little arched pediment ----
    fr = 40
    s.add(f'<rect x="{dl - fr - 8}" y="{dt - fr - 12}" width="{dr - dl + 2 * fr + 16}" height="{sill - dt + fr + 12}" fill="#000" opacity=".55" filter="{s.blur(14)}" transform="translate(0 10)"/>')
    wood = s.lin([(0, "#7a4226"), (0.5, "#5c2c18"), (1, "#3c1a0c")], 0, 0, 1, 0)
    s.add(f'<rect x="{dl - fr}" y="{dt - fr}" width="{dr - dl + 2 * fr}" height="{sill - dt + fr}" fill="{wood}"/>')
    for k, inset in enumerate((6, 15, 26)):
        s.add(f'<path d="M{dl - fr + inset} {sill}V{dt - fr + inset}H{dr + fr - inset}V{sill}" fill="none" stroke="{"#c88a3c" if k != 1 else "#2a1008"}" stroke-opacity="{.55 if k != 1 else .5}" stroke-width="{2.2 if k != 1 else 3}"/>')
    beads = "".join(f'<circle cx="{x}" cy="{y}" r="2.2"/>' for x in (dl - fr + 20.5, dr + fr - 20.5) for y in range(dt - 10, sill - 6, 13))
    beads += "".join(f'<circle cx="{x}" cy="{dt - fr + 20.5}" r="2.2"/>' for x in range(dl - fr + 34, dr + fr - 26, 13))
    s.add(f'<g fill="#e0a85a" opacity=".7">{beads}</g>')
    # lintel and pediment
    s.add(f'<rect x="{dl - fr - 20}" y="{dt - fr - 22}" width="{dr - dl + 2 * fr + 40}" height="22" fill="#6a3820"/>'
          f'<rect x="{dl - fr - 20}" y="{dt - fr - 22}" width="{dr - dl + 2 * fr + 40}" height="3" fill="#ffc880" opacity=".45"/>'
          f'<rect x="{dl - fr - 26}" y="{dt - fr - 30}" width="{dr - dl + 2 * fr + 52}" height="9" fill="#4e2814"/>')
    ped = f"M{800 - 92} {dt - fr - 30}C{800 - 80} {dt - fr - 92} {800 + 80} {dt - fr - 92} {800 + 92} {dt - fr - 30}Z"
    s.add(f'<path d="{ped}" fill="#5c2e18"/><path d="M{800 - 70} {dt - fr - 30}C{800 - 60} {dt - fr - 76} {800 + 60} {dt - fr - 76} {800 + 70} {dt - fr - 30}" fill="none" stroke="#d39a48" stroke-opacity=".6" stroke-width="2.4"/>')
    # carved lotus rosette in the pediment
    lot = "".join(f'<path d="{_petal(9, 20)}" transform="translate(800 {dt - fr - 38}) rotate({a})"/>' for a in range(-80, 81, 32))
    s.add(f'<g fill="#e3a852" opacity=".8">{lot}</g><circle cx="800" cy="{dt - fr - 40}" r="4" fill="#fff0c0" opacity=".8"/>')
    # inside the open doors: warm light, a floor running back, the leaves swung inward
    ig = s.rad([(0, "#fffbe8", 1), (0.22, "#ffe2a0", 1), (0.6, "#f4a048", 1), (1, "#9a4618", 1)], 800, 640, 320, user=True)
    s.add(f'<rect x="{dl}" y="{dt}" width="{dr - dl}" height="{sill - dt}" fill="{ig}"/>')
    s.add(f'<path d="M{dl} {sill}L{dl + 40} {sill - 46}H{dr - 40}L{dr} {sill}Z" fill="#e0782e" opacity=".45"/>'
          f'<path d="M{dl + 40} {sill - 46}H{dr - 40}" stroke="#a04818" stroke-opacity=".5" stroke-width="2"/>')
    studs = []
    for side in (-1, 1):
        ex = dl if side < 0 else dr
        ix = ex - side * 46
        s.add(f'<path d="M{ex} {dt}L{ix} {dt + 26}V{sill - 40}L{ex} {sill}Z" fill="#5a2610"/>'
              f'<path d="M{ex} {dt}L{ix} {dt + 26}V{sill - 40}L{ex} {sill}Z" fill="{s.lin([(0, "#000", .5), (1, "#ffb060", .25)], ex, 0, ix, 0, user=True)}"/>'
              f'<path d="M{ix} {dt + 26}V{sill - 40}" stroke="#ffd08a" stroke-opacity=".6" stroke-width="2"/>')
        for y in range(dt + 40, sill - 50, 26):
            t = (y - dt) / (sill - dt)
            studs.append(f'<circle cx="{f(ex - side * 23)}" cy="{f(y + 13 * (1 - 2 * t) * .0)}" r="2.6"/>')
    s.add(f'<g fill="#ffd27a" opacity=".85">{"".join(studs)}</g>')
    s.glow(800, 600, 420, "#ffb060", .5, .25)
    # a little lamp burning on the floor within
    diya(s, 800, sill - 52, .42, k=.3, flame_h=26, glow_a=.6, dots=False)
    # threshold and stone steps (treads seen from just above)
    s.add(f'<rect x="{dl - fr - 8}" y="{sill}" width="{dr - dl + 2 * fr + 16}" height="10" fill="#7a4a32"/>'
          f'<rect x="{dl - fr - 8}" y="{sill}" width="{dr - dl + 2 * fr + 16}" height="2.5" fill="#ffe0b0" opacity=".7"/>')
    steps = [(764, 800, 586, 1014), (800, 838, 548, 1052), (838, 878, 508, 1092)]
    for top, bot, sl, sr in steps:
        tread = 12
        s.add(f'<rect x="{sl}" y="{top}" width="{sr - sl}" height="{tread}" fill="{s.lin([(0, "#6e4c4a", 1), (1, "#8a5e52", 1)], 0, top, 0, top + tread, user=True)}"/>'
              f'<rect x="{sl}" y="{top + tread}" width="{sr - sl}" height="{bot - top - tread}" fill="{s.lin([(0, "#4a2e34", 1), (1, "#2c1a22", 1)], 0, top + tread, 0, bot, user=True)}"/>'
              f'<rect x="{sl}" y="{top + tread}" width="{sr - sl}" height="2" fill="#ffc890" opacity=".5"/>')
    s.add(f'<rect x="{x0}" y="760" width="{586 - x0}" height="118" fill="#2e1b24"/><rect x="1014" y="760" width="{x1 - 1014}" height="118" fill="#2e1b24"/>'
          f'<rect x="{x0}" y="760" width="{x1 - x0}" height="4" fill="#704650"/>')
    # courtyard floor of old stone
    fg = s.lin([(0, "#4a2e30", 1), (1, "#1a0f16", 1)], 0, 878, 0, 1000, user=True)
    s.add(f'<rect x="-10" y="878" width="1620" height="130" fill="{fg}"/>')
    joints = "".join(f"M{f(800 + (x - 800) * .55)} 878L{f(x + (x - 800) * .6)} 1000" for x in range(-400, 2100, 150))
    joints += "".join(f"M-10 {y}H1620" for y in (900, 930, 968))
    s.add(f'<path d="{joints}" stroke="#000" stroke-opacity=".22" stroke-width="2"/>')
    # toran over the door
    toran(s, dl - fr - 14, dr + fr + 14, dt - fr + 4, sag=12, leaf=58, marigold_r=8.5, seed=3, rim="#ffd8a0")
    # the warm air of the house front, lit from below; night above
    s.add(f'<rect x="{x0}" y="{roof - 50}" width="{x1 - x0}" height="{880 - roof + 50}" fill="{s.rad([(0, "#ff8a3a", .42), (0.45, "#c8501e", .16), (1, "#000", 0)], 800, 860, 760, user=True)}" style="mix-blend-mode:screen"/>')
    s.add(f'<rect x="{x0 - 30}" y="{roof - 50}" width="{x1 - x0 + 60}" height="{760 - roof + 50}" fill="{s.lin([(0, "#05030c", .5), (0.55, "#05030c", 0)], 0, roof - 50, 0, 760, user=True)}"/>')
    # rangoli at the threshold
    lay_rangoli(s, 800, 936, 200, k=.27, seed=4, shade=.12)
    # ---- the lamps ----
    for x in range(x0 + 6, x1, 46):
        diya(s, x, roof - 52, .36, k=.3, flame_h=13, glow_a=.4, dots=False)
    for wx in (452, 1148):
        for j in range(5):
            diya(s, wx - 72 + j * 36, 614, .4, k=.3, flame_h=15, glow_a=.45, dots=False)
    for (top, bot, sl, sr), sc in zip(steps, (.48, .54, .6)):
        for side in (-1, 1):
            for j in range(2):
                x = 800 + side * ((sr - sl) / 2 - 26 - j * 50)
                diya(s, x, top + 6, sc, k=.34, flame_h=30 * sc, glow_a=.5, seed=j)
    for i in range(9):
        a = math.radians(196 + 148 * i / 8)
        diya(s, 800 + math.cos(a) * 252, 936 + math.sin(a) * 252 * .27 - 6, .6, k=.34, flame_h=20, glow_a=.45, seed=i)
    for x in range(290, 560, 56):
        diya(s, x, 892 + (x % 3) * 4, .55, k=.34, flame_h=18, glow_a=.4, seed=x)
    for x in range(1070, 1340, 56):
        diya(s, x, 892 + (x % 3) * 4, .55, k=.34, flame_h=18, glow_a=.4, seed=x)
    s.motes(26, 300, 1300, 380, 900, seed=4, size=(.8, 1.8))
    # out-of-focus lamps very close to the viewer
    s.add(f'<g filter="{s.blur(9)}" opacity=".9">' + ob.marigold(120, 960, 54, "#f39a1c", 4) + ob.marigold(1500, 975, 46, "#e8562a", 5) + '</g>')
    s.glow(180, 930, 220, "#ff9a40", .35, .25)
    s.glow(1440, 940, 200, "#ff9a40", .3, .25)
    s.bokeh(5, 40, 260, 860, 1000, colors=("#ffb050", "#ffd890"), r=(20, 40), a=(.25, .5), blur=5, seed=3)
    s.bokeh(4, 1340, 1580, 860, 1000, colors=("#ffb050", "#ffd890"), r=(20, 40), a=(.25, .5), blur=5, seed=4)
    s.fx("mottle", amp=.045, cell=60)
    s.look = {"vibrance": .1}
    return s


# ======================================================================
# 2. rangoli at the door (seen from above)
# ======================================================================
PAISLEY = "M0 0C-20 -2 -24 -30 -8 -44C0 -51 10 -52 12 -45C6 -45 2 -40 6 -35C14 -24 14 -6 0 0Z"


def rangoli_rich_svg(R, pal=None):
    """A larger, more intricate rangoli: lotus border, leaf garland, a ring of paisleys and a
    sixteen-petal lotus round an eight-petal heart (SVG string, centred at the origin)."""
    p = dict(RANGOLI, **(pal or {}))
    wh = p["white"]
    o = []

    def ring(n, r, shape, fill, stroke=None, sw=1.5, rot0=0.0, sc=1.0, flip=False):
        st = f' stroke="{stroke}" stroke-width="{f(sw)}" stroke-linejoin="round"' if stroke else ""
        parts = "".join(f'<path d="{shape}" transform="rotate({360 * i / n + rot0:.2f}) translate(0 {f(-r)}) scale({f(-sc if flip else sc)} {f(sc)})"/>' for i in range(n))
        return f'<g fill="{fill}"{st}>{parts}</g>'

    def dots(n, r, rad, fill, rot0=0.0):
        return "".join(f'<circle cx="{f(math.cos(math.radians(360 * i / n + rot0)) * r)}" cy="{f(math.sin(math.radians(360 * i / n + rot0)) * r)}" r="{f(rad)}" fill="{fill}"/>' for i in range(n))

    # lotus border of twelve lobes
    o.append(ring(12, R * .70, _round_petal(R * .40, R * .29), p["magenta"], wh, R * .008))
    o.append(ring(12, R * .70, _round_petal(R * .27, R * .21), p["pink"]))
    o.append(ring(12, R * .70, _round_petal(R * .13, R * .13), p["yellow"]))
    o.append(dots(12, R * .9, R * .016, wh))
    o.append(ring(12, R * .78, _petal(R * .09, R * .16), p["saffron"], wh, R * .005, 15))
    o.append(dots(48, R * 1.0, R * .009, wh))
    o.append(dots(12, R * .96, R * .014, p["yellow"], 15))
    # green garland band
    o.append(f'<circle r="{f(R * .76)}" fill="{p["green"]}" stroke="{wh}" stroke-width="{f(R * .009)}"/>')
    o.append(ring(40, R * .67, _petal(R * .035, R * .085), p["leaf"], None, 0, 0))
    o.append(dots(40, R * .725, R * .008, wh, 4.5))
    # ring of paisleys on yellow
    o.append(f'<circle r="{f(R * .665)}" fill="{p["yellow"]}" stroke="{wh}" stroke-width="{f(R * .008)}"/>')
    o.append(ring(12, R * .44, PAISLEY, p["blue"], wh, 2.2, 15, R * .0042))
    o.append(ring(12, R * .465, PAISLEY, p["teal"], None, 0, 15, R * .0026))
    o.append(dots(12, R * .53, R * .011, wh, 15.6))
    o.append(ring(12, R * .56, _petal(R * .05, R * .09), p["red"], None, 0, 0))
    o.append(dots(12, R * .645, R * .012, p["magenta"], 0))
    # sixteen-petal lotus
    o.append(f'<circle r="{f(R * .44)}" fill="{p["purple"]}" stroke="{wh}" stroke-width="{f(R * .009)}"/>')
    o.append(ring(16, R * .2, _petal(R * .12, R * .22), p["saffron"], wh, R * .005))
    o.append(ring(16, R * .2, _petal(R * .055, R * .14), p["yellow"]))
    o.append(ring(16, R * .21, _petal(R * .08, R * .17), p["red"], wh, R * .004, 11.25))
    o.append(dots(16, R * .41, R * .01, wh, 11.25))
    # the heart: white ground, pink lotus, yellow and red centre where a lamp will stand
    o.append(f'<circle r="{f(R * .2)}" fill="{wh}"/>')
    o.append(ring(8, R * .04, _petal(R * .09, R * .15), p["pink"], p["magenta"], R * .004))
    o.append(ring(8, R * .04, _petal(R * .07, R * .12), p["pink"], None, 0, 22.5))
    o.append(f'<circle r="{f(R * .075)}" fill="{p["yellow"]}"/><circle r="{f(R * .05)}" fill="{p["red"]}"/>')
    return "".join(o)


def floor_mandala(s, cx, cy, svg, k, rough=3.0, seed=1, opacity=1.0):
    pf = powder_filter(s, scale=rough, seed=seed)
    s.add(f'<g transform="translate({f(cx)} {f(cy)}) scale(1 {f(k)})" opacity="{opacity}"><g filter="{pf}">{svg}</g></g>')


def stone_floor(s, cx, cy, k, base="#2c2426", seed=5, slab=330, y0=0):
    """Large stone slabs on the floor plane, centred on (cx, cy) and foreshortened by k."""
    s.add(f'<rect y="{y0}" width="{W}" height="{H - y0}" fill="{base}"/>')
    s.add(f'<rect y="{y0}" width="{W}" height="{H - y0}" fill="{base}" filter="{s.grain(0.006, 4, .22, seed, "#000000")}"/>')
    s.add(f'<rect y="{y0}" width="{W}" height="{H - y0}" fill="{base}" filter="{s.grain(0.7, 2, .06, seed + 1, "#fff0e0")}"/>')
    rng = random.Random(seed)
    d = []
    for j in range(-4, 5):
        y = cy + (j + .5) * slab * k
        d.append(f"M0 {f(y)}H{W}")
        off = rng.uniform(0, slab)
        for i in range(-4, 5):
            x = cx + (i * slab * 1.3) + off
            d.append(f"M{f(x)} {f(y)}V{f(y + slab * k)}")
    s.add(f'<path d="{"".join(d)}" stroke="#000" stroke-opacity=".45" stroke-width="3" filter="{s.blur(1)}"/>'
          f'<path d="{"".join(d)}" stroke="#ffd8b0" stroke-opacity=".06" stroke-width="1.2" transform="translate(0 2)"/>')


@scene
def rangoli(s):
    cx, cy, R, k = 800, 548, 318, .78
    stone_floor(s, cx, cy, k, base="#30282a", slab=360)
    # the threshold of the house at the top, with light spilling out across the floor
    s.add(f'<rect y="0" width="{W}" height="86" fill="{s.lin([(0, "#3a1a0c", 1), (1, "#a8521e", 1)], 0, 0, 0, 86, user=True)}"/>')
    s.add(f'<rect y="0" width="{W}" height="86" fill="{s.rad([(0, "#ffd890", .9), (1, "#ff9a40", 0)], 800, 90, 520, user=True)}" style="mix-blend-mode:screen"/>')
    for x in (130, 1470):
        s.add(f'<rect x="{x - 60}" y="0" width="120" height="96" fill="{s.lin([(0, "#2a1206"), (0.5, "#6a3a1e"), (1, "#2a1206")], 0, 0, 1, 0)}"/>')
    s.add(f'<path d="M420 0H1180L1500 1000H100Z" fill="{s.lin([(0, "#ffb060", .4), (0.6, "#ff9a40", .08), (1, "#ff9a40", 0)], 0, 80, 0, 900, user=True)}" filter="{s.blur(40)}" style="mix-blend-mode:screen"/>')
    s.add(f'<rect y="86" width="{W}" height="54" fill="{s.lin([(0, "#6a3a1e", 1), (0.3, "#4a2410", 1), (1, "#2a1206", 1)], 0, 86, 0, 140, user=True)}"/>'
          f'<rect y="86" width="{W}" height="3" fill="#ffd8a0" opacity=".7"/><rect y="118" width="{W}" height="22" fill="#e0a830" opacity=".55"/>'
          f'<rect y="138" width="{W}" height="14" fill="#000" opacity=".5" filter="{s.blur(6)}"/>')
    s.add("".join(f'<circle cx="{x}" cy="112" r="4" fill="#e8b45a"/><circle cx="{x - 1}" cy="111" r="1.5" fill="#fff4c8"/>' for x in range(60, 1600, 120)))
    # kumkum and turmeric marks on the threshold
    s.add("".join(f'<circle cx="{x}" cy="129" r="7" fill="#c8202a" opacity=".9"/>' for x in range(80, 1600, 80)))
    # shadow where the rangoli meets the floor, then the rangoli
    floor_mandala(s, cx, cy, rangoli_rich_svg(R), k, rough=3.2, seed=3)
    # lamplight pooled over the powder
    s.add(f'<ellipse cx="{cx}" cy="{cy}" rx="{R * 1.6}" ry="{R * 1.6 * k}" fill="{s.rad([(0, "#ffb060", .3), (0.4, "#ff8a3a", .1), (1, "#ff8a3a", 0)], cx, cy, R * 1.6, user=True, transform=f"translate(0 {f(cy * (1 - k))}) scale(1 {k})")}" style="mix-blend-mode:screen"/>')
    s.add(f'<rect width="{W}" height="{H}" fill="{s.rad([(0, "#000", 0), (0.5, "#000", .05), (1, "#000", .55)], cx, cy, 980, user=True)}"/>')
    # petals and flower heads strewn round it
    ob.petals_scatter(s, 300, 1300, 170, 980, 70, seed=4, size=(5, 10))
    flowers = []
    rng = random.Random(8)
    for i in range(12):
        a = math.radians(360 * (i + .5) / 12 + 90)
        rr = R * 1.18
        x, y = cx + math.cos(a) * rr, cy + math.sin(a) * rr * k
        flowers.append(ob.marigold(x, y, 15, ("#f39a1c", "#f7c02a", "#e8562a")[i % 3], i))
        for j in range(3):
            b = a + rng.uniform(-.12, .12)
            r2 = rr + rng.uniform(-14, 30)
            flowers.append(f'<circle cx="{f(cx + math.cos(b) * r2)}" cy="{f(cy + math.sin(b) * r2 * k)}" r="4" fill="#fff6e8"/>')
    s.add("".join(flowers))
    # the ring of lamps, back ones first, and the lamp at the heart
    ring = []
    for i in range(12):
        a = math.radians(360 * i / 12 + 90)
        ring.append((math.sin(a), a))
    for _, a in sorted(ring):
        rr = R * 1.06
        diya(s, cx + math.cos(a) * rr, cy + math.sin(a) * rr * k, .78, k=.7, lip=math.degrees(a), flame_h=34, glow_a=.5, seed=int(a * 10))
    diya(s, cx, cy, 1.0, k=.72, lip=90, flame_h=52, glow_a=.6, glow_r=300)
    s.motes(30, 400, 1200, 150, 900, seed=6, size=(.8, 1.6))
    s.fx("mottle", amp=.04, cell=60)
    s.look = {"vibrance": .12}
    return s


# ======================================================================
# 12. six lamps round one light (the six darshanas)
# ======================================================================
def kolam_svg(R, color="#f4ead8"):
    """A delicate six-fold rice-flour kolam (strokes only), centred at the origin."""
    o = []
    sw = R * .008

    def circ(r, w=sw, a=1.0):
        o.append(f'<circle r="{f(r)}" fill="none" stroke="{color}" stroke-width="{f(w)}" opacity="{a}"/>')
    circ(R * .16)
    circ(R * .19, sw * .7)
    # six vesica petals, double-lined, a dot in each
    for i in range(6):
        a = 60 * i
        L, w = R * .5, R * .17
        d = f"M0 {f(-R * .2)}Q{f(w)} {f(-R * .2 - L * .5)} 0 {f(-R * .2 - L)}Q{f(-w)} {f(-R * .2 - L * .5)} 0 {f(-R * .2)}Z"
        d2 = f"M0 {f(-R * .25)}Q{f(w * .62)} {f(-R * .2 - L * .5)} 0 {f(-R * .2 - L * .88)}Q{f(-w * .62)} {f(-R * .2 - L * .5)} 0 {f(-R * .25)}Z"
        o.append(f'<g transform="rotate({a})"><path d="{d}" fill="none" stroke="{color}" stroke-width="{f(sw)}"/>'
                 f'<path d="{d2}" fill="none" stroke="{color}" stroke-width="{f(sw * .7)}" opacity=".8"/>'
                 f'<circle cy="{f(-R * .2 - L * .45)}" r="{f(R * .012)}" fill="{color}"/></g>')
        # interlaced loop between petals
        b = math.radians(a + 30 - 90)
        lx, ly = math.cos(b) * R * .42, math.sin(b) * R * .42
        o.append(f'<circle cx="{f(lx)}" cy="{f(ly)}" r="{f(R * .1)}" fill="none" stroke="{color}" stroke-width="{f(sw * .8)}"/>'
                 f'<circle cx="{f(lx)}" cy="{f(ly)}" r="{f(R * .012)}" fill="{color}"/>')
    # chain of interlocking rings
    for i in range(24):
        b = math.radians(15 * i)
        o.append(f'<circle cx="{f(math.cos(b) * R * .8)}" cy="{f(math.sin(b) * R * .8)}" r="{f(R * .1)}" fill="none" stroke="{color}" stroke-width="{f(sw * .75)}" opacity=".9"/>')
    for i in range(24):
        b = math.radians(15 * i + 7.5)
        o.append(f'<circle cx="{f(math.cos(b) * R * .8)}" cy="{f(math.sin(b) * R * .8)}" r="{f(R * .011)}" fill="{color}"/>')
    # a wave border with dots in its hollows
    pts = []
    for t in range(0, 721):
        b = math.radians(t * .5)
        r = R * (.98 + .035 * math.sin(b * 30))
        pts.append((math.cos(b) * r, math.sin(b) * r))
    o.append(f'<path d="{pts_d(pts)}" fill="none" stroke="{color}" stroke-width="{f(sw * .8)}"/>')
    for i in range(30):
        b = math.radians(12 * i + 9)
        o.append(f'<circle cx="{f(math.cos(b) * R * 1.05)}" cy="{f(math.sin(b) * R * 1.05)}" r="{f(R * .01)}" fill="{color}"/>')
        b2 = math.radians(12 * i + 3)
        o.append(f'<circle cx="{f(math.cos(b2) * R * .91)}" cy="{f(math.sin(b2) * R * .91)}" r="{f(R * .008)}" fill="{color}" opacity=".8"/>')
    circ(R * .64, sw * .6, .7)
    circ(R * 1.12, sw * .6, .55)
    for i in range(36):
        b = 10 * i
        o.append(f'<path d="{_petal(R * .035, R * .07)}" transform="rotate({b}) translate(0 {f(-R * 1.13)})" fill="none" stroke="{color}" stroke-width="{f(sw * .6)}" opacity=".6"/>')
    return "".join(o)


@scene
def darshanas(s):
    cx, cy, R, k = 800, 520, 400, .7
    s.add(f'<rect width="{W}" height="{H}" fill="#120806"/>')
    s.add(f'<rect width="{W}" height="{H}" fill="{s.rad([(0, "#4a2010", 1), (0.45, "#2a1008", 1), (1, "#0c0504", 1)], cx, cy, 900, user=True, transform=f"translate(0 {f(cy * (1 - k))}) scale(1 {k})")}"/>')
    s.add(f'<rect width="{W}" height="{H}" fill="#2a1008" filter="{s.grain(0.006, 4, .35, 7, "#000000")}" opacity=".7"/>')
    # polished floor sheen under the light
    s.add(f'<ellipse cx="{cx}" cy="{cy}" rx="420" ry="{420 * k}" fill="{s.rad([(0, "#ff9a4a", .35), (1, "#ff9a4a", 0)], .5, .5, .5)}" style="mix-blend-mode:screen"/>')
    floor_mandala(s, cx, cy, kolam_svg(R), k, rough=1.6, seed=5, opacity=.92)
    s.add(f'<g transform="translate({cx} {cy}) scale(1 {k})" filter="{s.blur(5)}" opacity=".25" style="mix-blend-mode:screen">{kolam_svg(R, "#ffd8a8")}</g>')
    # light fading into the dark beyond
    s.add(f'<rect width="{W}" height="{H}" fill="{s.rad([(0, "#000", 0), (0.45, "#000", .1), (1, "#000", .8)], cx, cy, 980, user=True, transform=f"translate(0 {f(cy * (1 - k))}) scale(1 {k})")}"/>')
    ob.petals_scatter(s, 500, 1100, 360, 700, 18, seed=9, size=(4, 7), colors=("#f39a1c", "#e8562a", "#f7c02a"))
    # six lamps (back ones first), one light at the heart
    ring = sorted((math.sin(math.radians(60 * i + 90)), math.radians(60 * i + 90)) for i in range(6))
    for _, a in ring:
        rr = R * .7
        diya(s, cx + math.cos(a) * rr, cy + math.sin(a) * rr * k, 1.3, k=.66, lip=math.degrees(a) + 180, flame_h=66, glow_a=.6, glow_r=280, seed=int(a * 10))
    s.glow(cx, cy - 60, 260, "#ffd890", .35, .3)
    diya(s, cx, cy + 4, 1.6, k=.66, lip=90, flame_h=118, glow_a=.75, glow_r=560, clay="#b07a2a", dots=False)
    s.motes(24, 500, 1100, 120, 500, seed=6, size=(.7, 1.4))
    s.fx("mottle", amp=.035, cell=60)
    s.look = {"vibrance": .08}
    return s


# ======================================================================
# people: silhouettes posed from a few joints (local units, ~100 tall, feet at 0)
# ======================================================================
def _pt(p):
    return f"{f(p[0])} {f(p[1])}"


def _taper_path(pts, w0, w1):
    """A filled stroke along pts whose width runs from w0 to w1."""
    n = len(pts)
    L, R_ = [], []
    for i, (x, y) in enumerate(pts):
        xa, ya = pts[max(0, i - 1)]
        xb, yb = pts[min(n - 1, i + 1)]
        dx, dy = xb - xa, yb - ya
        ln = math.hypot(dx, dy) or 1
        w = (w0 + (w1 - w0) * i / max(1, n - 1)) / 2
        L.append((x - dy / ln * w, y + dx / ln * w))
        R_.append((x + dy / ln * w, y - dx / ln * w))
    return pts_d(L + R_[::-1])


def _curve(ctrl, n=14):
    return smooth_line(ctrl, step=max(2, math.dist(ctrl[0], ctrl[-1]) / n))


def body_svg(J, skirt=None, kurta=None, hair="bun", dupatta=None, sticks=None, legs=True, limb=1.0, waist=3.0):
    """SVG for a figure from joints J: head, neck, ls, rs, lh, rh, le, lw, re, rw, lk, lf, rk, rf
    (each part its own path, so overlaps never cut holes). skirt / kurta = (hem_left, hem_right,
    hem_y, swirl); hair = "bun", None or a list of braid points; dupatta = list of points;
    sticks = list of (hand_key, angle_deg, length)."""
    d = []
    hx, hy = J["head"]
    nx, ny = J["neck"]
    tilt = math.degrees(math.atan2(hx - nx, ny - hy))
    d.append(f'<ellipse cx="{f(hx)}" cy="{f(hy)}" rx="6.1" ry="7.4" transform="rotate({f(tilt)} {f(hx)} {f(hy)})"/>')
    d.append(f'<path d="{_taper_path([(hx * .7 + nx * .3, hy + 5), (nx, ny + 1)], 4.6, 5.6)}"/>')
    ls, rs, lh, rh = J["ls"], J["rs"], J["lh"], J["rh"]
    wy = ls[1] + (lh[1] - ls[1]) * .62
    wl = (ls[0] + (lh[0] - ls[0]) * .62 + waist, wy)
    wr = (rs[0] + (rh[0] - rs[0]) * .62 - waist, wy)
    for q in (ls, rs):
        d.append(f'<circle cx="{f(q[0] + (1.2 if q is ls else -1.2))}" cy="{f(q[1] + 2.6)}" r="3.6"/>')
    d.append(f'<path d="M{_pt(ls)}Q{f((ls[0] + rs[0]) / 2)} {f(min(ls[1], rs[1]) - 3)} {_pt(rs)}C{f(rs[0] + 1)} {f(rs[1] + 8)} {f(wr[0])} {f(wr[1] - 6)} {_pt(wr)}'
             f'C{f(wr[0])} {f(wr[1] + 5)} {f(rh[0] + 1)} {f(rh[1] - 4)} {_pt(rh)}Q{f((lh[0] + rh[0]) / 2)} {f(lh[1] + 3)} {_pt(lh)}'
             f'C{f(lh[0] - 1)} {f(lh[1] - 4)} {f(wl[0])} {f(wl[1] + 5)} {_pt(wl)}C{f(wl[0])} {f(wl[1] - 6)} {f(ls[0] - 1)} {f(ls[1] + 8)} {_pt(ls)}Z"/>')
    for s_, e_, w_ in (("ls", "le", "lw"), ("rs", "re", "rw")):
        a, b, c = J[s_], J[e_], J[w_]
        a2 = (a[0] + (b[0] - a[0]) * .08, a[1] + (b[1] - a[1]) * .08)
        d.append(f'<path d="{_taper_path(_curve([a2, b, c], 10), 5.6 * limb, 2.8 * limb)}"/>')
        ux, uy = c[0] - b[0], c[1] - b[1]
        un = math.hypot(ux, uy) or 1
        d.append(f'<ellipse cx="{f(c[0] + ux / un * 2.6)}" cy="{f(c[1] + uy / un * 2.6)}" rx="2.2" ry="3.6" transform="rotate({f(math.degrees(math.atan2(uy, ux)) - 90)} {f(c[0] + ux / un * 2.6)} {f(c[1] + uy / un * 2.6)})"/>')
    if legs:
        for h_, k_, f_ in (("lh", "lk", "lf"), ("rh", "rk", "rf")):
            a, b, c = J[h_], J[k_], J[f_]
            d.append(f'<path d="{_taper_path(_curve([a, b, c], 10), 8.0 * limb, 3.4 * limb)}"/>')
            fw = 6.5 if J["head"][0] >= J["neck"][0] - 1 else -6.5
            d.append(f'<path d="{_taper_path([(c[0] - fw * .25, c[1] - 1.8), (c[0] + fw, c[1] + .2)], 4.2, 2.2)}"/>')
    for spec, is_kurta in ((skirt, False), (kurta, True)):
        if not spec:
            continue
        hl, hr, hem, swirl = spec
        if is_kurta:
            tl = (wl[0], wl[1])
            tr = (wr[0], wr[1])
        else:
            tl = (wl[0], wl[1])
            tr = (wr[0], wr[1])
        nn = 6
        hem_d = ""
        for i in range(nn):
            t0, t1 = i / nn, (i + 1) / nn
            xa = hr + (hl - hr) * t1
            ya = hem - swirl * math.sin(t1 * math.pi)
            xm = hr + (hl - hr) * (t0 + t1) / 2
            ym = hem - swirl * math.sin((t0 + t1) / 2 * math.pi) + (2.2 if i % 2 else -1.0)
            hem_d += f"Q{f(xm)} {f(ym)} {f(xa)} {f(ya)}"
        my = (tl[1] + hem) / 2
        bulge = .55 if not is_kurta else .3
        hR = (rh[0] + 2.4, rh[1])
        hL = (lh[0] - 2.4, lh[1])
        d.append(f'<path d="M{_pt(tl)}L{_pt(tr)}C{_pt(hR)} {f(hr - (hr - hR[0]) * (1 - bulge) * .3)} {f(hem - (hem - hR[1]) * .3)} {f(hr)} {f(hem)}'
                 + hem_d
                 + f'C{f(hl - (hl - hL[0]) * (1 - bulge) * .3)} {f(hem - (hem - hL[1]) * .3)} {_pt(hL)} {_pt(tl)}Z"/>')
    if hair == "bun":
        bx, by = hx - 5.2 if hx >= nx else hx + 5.2, hy - 1
        d.append(f'<circle cx="{f(bx)}" cy="{f(by)}" r="4"/>')
    elif isinstance(hair, list):
        d.append(f'<path d="{_taper_path(_curve([(hx, hy - 3)] + hair, 12), 7.5, 1.6)}"/>')
    if dupatta:
        d.append(f'<path d="{_taper_path(_curve(dupatta, 18), 6.5, 2.6)}"/>')
    if sticks:
        for hand, ang, L in sticks:
            c = J[hand]
            a = math.radians(ang)
            d.append(f'<path d="{_taper_path([(c[0] - math.cos(a) * 4, c[1] - math.sin(a) * 4), (c[0] + math.cos(a) * L, c[1] + math.sin(a) * L)], 2.4, 2.0)}"/>')
    return "".join(d)


def person(s, x, y, sc, J, color="#2a1a2a", rim=None, rim_dx=1.6, flip=False, shadow=None, **kw):
    """Place a silhouette; rim light is a lit copy offset towards the light (rim_dx, in local units)."""
    d = body_svg(J, **kw)
    sx = -sc if flip else sc
    t = f"translate({f(x)} {f(y)}) scale({f(sx)} {f(sc)})"
    if shadow:
        sa, sk = shadow
        s.add(f'<g transform="translate({f(x)} {f(y)}) scale({f(sx)} {f(-sc * sk)})" opacity="{sa}" filter="{s.blur(3)}" fill="#000">{d}</g>')
    if rim:
        s.add(f'<g transform="{t}"><g fill="{rim}" transform="translate({f(rim_dx)} {f(-abs(rim_dx) * .5)})">{d}</g></g>')
    s.add(f'<g transform="{t}" fill="{color}">{d}</g>')


# ======================================================================
# coloured powder (gulal) clouds as a raster effect
# ======================================================================
def powder_fx(img, bursts, light=(0.3, -1.0), backlit=None, seed=1, bump=.8):
    """Billowing clouds of gulal. Each burst is (x, y, angle_deg, length, r0, r1, color, opacity):
    a plume of puffs thrown from (x, y), growing from radius r0 to r1 along its path. Lit from the
    light direction with soft self-shadowing, glowing at its thin edges when backlit = (sx, sy, radius)."""
    Hh, Ww, _ = img.shape
    lx, ly = light
    ln = math.hypot(lx, ly)
    lx, ly = lx / ln, ly / ln
    for i, b in enumerate(bursts):
        x, y, ang, L, r0, r1, color, op = b[:8]
        rng = np.random.default_rng(seed * 101 + i)
        a = math.radians(ang)
        nb = 10
        blobs = []
        for j in range(nb):
            t = j / (nb - 1)
            r = (r0 + (r1 - r0) * t ** .8) * rng.uniform(.75, 1.2)
            px = x + math.cos(a) * L * t + rng.normal() * r * .35
            py = y + math.sin(a) * L * t + rng.normal() * r * .35
            blobs.append((px, py, r))
        x0 = int(max(0, min(p[0] - p[2] * 2.2 for p in blobs)))
        x1 = int(min(Ww, max(p[0] + p[2] * 2.2 for p in blobs)))
        y0 = int(max(0, min(p[1] - p[2] * 2.2 for p in blobs)))
        y1 = int(min(Hh, max(p[1] + p[2] * 2.2 for p in blobs)))
        if x1 <= x0 or y1 <= y0:
            continue
        h, w = y1 - y0, x1 - x0
        yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
        field = np.zeros((h, w), np.float32)
        for px, py, r in blobs:
            field = np.maximum(field, np.exp(-(((xx - px) ** 2 + (yy - py) ** 2) / (2 * r * r))))
        n = fx.fbm(h, w, r1 * 1.1, 5, seed * 31 + i, 1.0, .5)
        n = (n - n.min()) / max(1e-6, n.max() - n.min())
        dens = field * (.5 + 1.0 * n)
        alpha = fx.smooth(.18, .75, dens)
        db = ndimage.gaussian_filter(dens, max(1.0, r1 * .1))
        gy, gx = np.gradient(db)
        slope = np.clip(.5 - bump * r1 * .6 * (gx * lx + gy * ly), 0, 1)
        thick = np.clip((dens - .25) / .8, 0, 1)
        shade = (.74 + .36 * slope) * (1 - .16 * thick)
        col = fx.rgb(color)[None, None, :] * shade[..., None]
        col = col + (1 - col) * (slope ** 3 * .35)[..., None]
        if backlit:
            sx, sy, sr = backlit
            near = np.exp(-(((xx - sx) ** 2 + (yy - sy) ** 2) / (2 * sr * sr)))
            edge = np.clip(1 - thick * 2.2, 0, 1)
            col = col + (np.array([1, .96, .86], np.float32) - col) * (near * edge * .85)[..., None]
        al = (alpha * op * (.55 + .45 * np.clip(thick * 1.6, 0, 1)))[..., None]
        reg = img[y0:y1, x0:x1]
        img[y0:y1, x0:x1] = reg * (1 - al) + np.clip(col, 0, 1) * al
    return img


fx.EFFECTS["powder"] = powder_fx


# ======================================================================
# 3. Holi
# ======================================================================
def branches(x, y, ang, L, w, depth, rng, tips, spread=34, shrink=.72):
    """Recursive tapering branches (path data); collects the twig tips."""
    ex, ey = x + math.cos(math.radians(ang)) * L, y + math.sin(math.radians(ang)) * L
    mx, my = (x + ex) / 2 + rng.uniform(-.12, .12) * L, (y + ey) / 2 + rng.uniform(-.08, .08) * L
    d = _taper_path(smooth_line([(x, y), (mx, my), (ex, ey)], 4), w, w * shrink)
    if depth == 0:
        tips.append((ex, ey))
        return d
    for k in range(rng.choice([2, 2, 3])):
        na = ang + rng.uniform(-spread, spread) + (k - .5) * spread * .6
        na = max(-170, min(-10, na))
        d += branches(ex, ey, na, L * rng.uniform(.62, .8), w * shrink, depth - 1, rng, tips, spread, shrink)
    return d


def palash(s, x, base, h, seed=1, color="#3a2a22", bloom=("#ff5a14", "#ff7a1a", "#ffa02a", "#e8400e"), haze=None, a=1.0):
    """A flame-of-the-forest tree in spring: bare dark branches crowded with orange flowers."""
    rng = random.Random(seed)
    tips = []
    d = branches(x, base, -90 + rng.uniform(-6, 6), h * .36, h * .06, 4, rng, tips)
    s.add(f'<path d="{d}" fill="{color}" opacity="{a}"/>')
    dots = []
    for px, py in tips:
        for _ in range(16):
            ang, r = rng.uniform(0, 6.28), h * .055 * rng.random() ** .5
            dots.append(f'<circle cx="{f(px + math.cos(ang) * r)}" cy="{f(py + math.sin(ang) * r * .8)}" r="{f(rng.uniform(.006, .013) * h)}" fill="{rng.choice(bloom)}"/>')
    s.add(f'<g opacity="{a}">{"".join(dots)}</g>')


# joints for the Holi figures (facing right, feet at y = 0)
J_THROW_UP = dict(head=(3, -92), neck=(1, -84), ls=(-8, -80), rs=(9, -80), lh=(-7, -50), rh=(7, -50),
                  le=(-17, -68), lw=(-24, -57), re=(16, -97), rw=(21, -115),
                  lk=(-5, -26), lf=(-9, 0), rk=(5, -26), rf=(10, 0))
J_BOTH_UP = dict(head=(0, -93), neck=(0, -85), ls=(-10, -81), rs=(10, -81), lh=(-7, -49), rh=(7, -49),
                 le=(-19, -97), lw=(-23, -116), re=(19, -98), rw=(25, -115),
                 lk=(-11, -25), lf=(-17, 0), rk=(12, -25), rf=(19, 0))
J_FLING = dict(head=(6, -90), neck=(4, -82), ls=(-6, -79), rs=(11, -78), lh=(-6, -49), rh=(8, -49),
               le=(-19, -84), lw=(-32, -90), re=(24, -80), rw=(38, -88),
               lk=(-9, -24), lf=(-18, 0), rk=(12, -25), rf=(16, 0))
J_CHILD = dict(head=(2, -90), neck=(1, -82), ls=(-9, -78), rs=(9, -78), lh=(-7, -48), rh=(7, -48),
               le=(-18, -88), lw=(-20, -104), re=(19, -72), rw=(30, -66),
               lk=(-12, -24), lf=(-20, -2), rk=(9, -26), rf=(14, 0))
J_DANCE = dict(head=(-2, -92), neck=(-1, -84), ls=(-10, -80), rs=(8, -80), lh=(-7, -50), rh=(7, -50),
               le=(-24, -86), lw=(-36, -98), re=(20, -90), rw=(30, -106),
               lk=(-6, -26), lf=(-8, 0), rk=(6, -26), rf=(8, 0))


def joint(x, y, sc, J, k, flip=False):
    return x + J[k][0] * sc * (-1 if flip else 1), y + J[k][1] * sc


@scene
def holi(s):
    sun = (800, 205)
    s.sky([(0, "#3f7cc4"), (.3, "#7eb0e2"), (.55, "#c6ddef"), (.66, "#f6e8d4"), (.7, "#ffe2bc")], 0, 1000)
    s.sun(*sun, 42, core="#fffdf6", rim="#fff2d0", halo="#fff0d0", halo_r=640, halo_a=.7)
    s.fx("clouds", y0=10, y1=300, seed=41, cell=170, aniso=2.6, cover=.38, soft=.16, lit="#ffffff", body=.9, direct=1.0,
         light=(0.2, 1), sun=(sun[0], sun[1], 380), rim="#fffaf0", opacity=.9)
    hz = 680
    from land import ridgeline, hills
    import arch
    far = ridgeline(hz, 26, 51, cell=200, octaves=5, ridged=.2)
    hills(s, far, "#b2bfd4", "#ccd3de")
    rng = random.Random(4)
    cr = "".join(crown(x, hz - rng.uniform(6, 18), rng.uniform(12, 24), seed=x) for x in range(-20, 1640, 22))
    s.add(f'<path d="{cr}" fill="#a3b2c8"/>')
    arch.nagara(s, 1210, hz - 6, .46, color="#97a6bf", door=None, bands=False, flag_color="#f08a3a")
    arch.shikhara_front(s, 360, hz - 4, .32, color="#9aaac2", flag_color="#f08a3a", tiers=False)
    s.mist(hz - 6, 50, "#f6efe6", .6, 14)
    palash(s, 150, hz + 50, 440, seed=3, color="#6a5a62", a=.85)
    palash(s, 1440, hz + 46, 470, seed=8, color="#6a5a62", a=.85)
    s.mist(hz + 10, 90, "#f4e6d8", .35, 20)
    gg = s.lin([(0, "#ead2b0", 1), (0.35, "#d8b088", 1), (1, "#9c6a48", 1)], 0, hz, 0, 1000, user=True)
    s.add(f'<rect y="{hz}" width="{W}" height="{H - hz}" fill="{gg}"/>')
    s.add(f'<rect y="{hz}" width="{W}" height="{H - hz}" fill="#c89870" filter="{s.grain(0.03, 3, .16, 6, "#5a3018")}"/>')
    stains = []
    for i in range(22):
        x, y = rng.uniform(150, 1450), rng.uniform(hz + 120, 990)
        c = rng.choice(["#ff3d8b", "#ffd21f", "#2fbf5a", "#2f7fff", "#a24ad8"])
        r = rng.uniform(30, 80) * (y - hz) / 300
        stains.append(f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(r)}" ry="{f(r * .2)}" fill="{c}" opacity=".3"/>')
    s.add(f'<g filter="{s.blur(6)}">{"".join(stains)}</g>')
    ob.petals_scatter(s, 0, 300, hz + 40, hz + 140, 30, colors=("#ff6a1a", "#ff8c2a"), seed=3, size=(3, 5))
    ob.petals_scatter(s, 1320, 1600, hz + 40, hz + 140, 30, colors=("#ff6a1a", "#ff8c2a"), seed=4, size=(3, 5))
    # the revellers and the colour they throw
    people = [  # x, y, scale, joints, flip, garment
        (470, 900, 2.9, J_THROW_UP, False, dict(skirt=(-26, 26, 0, 3), hair="bun", waist=3.6)),
        (668, 918, 3.0, J_FLING, False, dict(kurta=(-15, 17, -30, 1), hair=None, waist=1.2)),
        (826, 930, 2.1, J_CHILD, False, dict(skirt=(-16, 16, -18, 2), hair="bun", waist=2.0)),
        (990, 912, 3.0, J_BOTH_UP, True, dict(kurta=(-15, 15, -30, 1), hair=None, waist=1.2)),
        (1170, 896, 2.85, J_DANCE, True, dict(skirt=(-30, 28, 0, 4), hair="bun", waist=3.6)),
    ]
    hand = lambda i, k: joint(people[i][0], people[i][1], people[i][2], people[i][3], k, people[i][4])
    PINK, YEL, GRN, BLU, PUR, ORA = "#ff3d8b", "#ffcf1f", "#27b856", "#2f7fff", "#a24ad8", "#ff7a1a"
    back = [
        (*hand(0, "rw"), -105, 260, 30, 115, PINK, .9),
        (*hand(1, "lw"), -150, 200, 26, 100, YEL, .85),
        (*hand(1, "rw"), -62, 180, 24, 86, ORA, .8),
        (*hand(3, "rw"), -122, 220, 30, 108, GRN, .85),
        (*hand(3, "lw"), -68, 240, 28, 105, BLU, .85),
        (*hand(4, "lw"), -40, 220, 28, 100, PUR, .8),
        (*hand(2, "lw"), -95, 150, 18, 70, YEL, .75),
    ]
    s.fx("powder", bursts=back, light=(.25, -1), backlit=(sun[0], sun[1], 330), seed=2)
    col, rim = "#3c2440", "#fff0d6"
    for x, y, sc, J, fl, kw in people:
        person(s, x, y, sc, J, col, rim, flip=fl, shadow=(.2, .3), **kw)
    front = [
        (*hand(0, "rw"), -100, 90, 14, 46, PINK, .7),
        (*hand(1, "lw"), -150, 80, 12, 40, YEL, .65),
        (*hand(1, "rw"), -60, 80, 12, 40, ORA, .6),
        (*hand(3, "rw"), -120, 90, 14, 44, GRN, .65),
        (*hand(3, "lw"), -70, 90, 14, 44, BLU, .65),
        (*hand(4, "lw"), -40, 80, 12, 40, PUR, .6),
        (*hand(4, "rw"), -80, 70, 10, 36, PINK, .5),
    ]
    s.fx("powder", bursts=front, light=(.25, -1), backlit=(sun[0], sun[1], 300), seed=9)
    specks = []
    for i in range(320):
        b = rng.choice(back)
        a, r = math.radians(b[2] + rng.uniform(-50, 50)), rng.uniform(.2, 1.3) * b[3]
        c = rng.choice([b[6], b[6], "#ffffff"])
        specks.append(f'<circle cx="{f(b[0] + math.cos(a) * r)}" cy="{f(b[1] + math.sin(a) * r)}" r="{f(rng.uniform(.8, 2.4))}" fill="{c}" opacity="{rng.uniform(.4, .9):.2f}"/>')
    s.add(f'<g filter="{s.blur(.5)}">{"".join(specks)}</g>')
    s.fx("godrays", cx=sun[0], cy=sun[1], strength=.32, thresh=.82, decay=.97, radius=240)
    s.fx("mottle", amp=.03, cell=60)
    s.look = {"vibrance": .1, "vignette": .26}
    return s


# ======================================================================
# 5. kites at Makar Sankranti
# ======================================================================
KITE_STYLES = ["solid", "halves", "cap", "moon", "stripe"]


def patang(s, x, y, size, rot=0.0, c1="#e8246e", c2="#ffd23a", style="solid", glow=0.0, string_to=None, sag=0.12,
         string_color="#fff1dc", string_a=0.55, frame="#4a2a1a"):
    """An Indian fighter kite (patang): a diamond of paper on a bamboo spine and arched bow,
    with a small tail. glow (0..1) is how much the low sun shines through it."""
    t = f"translate({f(x)} {f(y)}) rotate({f(rot)}) scale({f(size)})"
    body = "M0 -1L.96 0L0 1L-.96 0Z"
    tail = "M0 .96L-.24 1.3Q0 1.22 .24 1.3Z"
    lit = mix(c1, "#fff6e0", glow * .45)
    lit2 = mix(c2, "#fff6e0", glow * .45)
    out = [f'<g transform="{t}">']
    out.append(f'<path d="{body}" fill="{s.rad([(0, mix(lit, "#ffffff", .25), 1), (1, lit, 1)], .45, .35, .8)}"/>')
    if style == "halves":
        out.append(f'<path d="M0 -1L.96 0L0 1Z" fill="{lit2}"/>')
    elif style == "cap":
        out.append(f'<path d="M0 -1L.5 -.48Q0 -.36 -.5 -.48Z" fill="{lit2}"/>')
    elif style == "moon":
        out.append(f'<circle cx="0" cy=".08" r=".4" fill="{lit2}"/><circle cx="0" cy=".08" r=".22" fill="{lit}"/><circle cx="0" cy=".08" r=".08" fill="{lit2}"/>')
    elif style == "stripe":
        out.append(f'<path d="M-.24 -.75L.24 -.75L.24 .75L-.24 .75Z" fill="{lit2}" clip-path="{s.clip(body)}"/>')
    sh = s.lin([(0, "#fff", .25 * glow), (0.5, "#fff", 0), (1, "#000", .25)], 0, 0, 1, 1)
    out.append(f'<path d="{body}" fill="{sh}"/>')
    out.append(f'<path d="{tail}" fill="{lit2 if style != "solid" else mix(lit, "#000000", .15)}"/>')
    sw = max(.012, 1.1 / size)
    out.append(f'<path d="{body}" fill="none" stroke="{frame}" stroke-opacity=".5" stroke-width="{f(sw)}"/>'
               f'<path d="M0 -1V1M-.96 0Q0 -.62 .96 0" fill="none" stroke="{frame}" stroke-opacity=".75" stroke-width="{f(sw * 1.5)}"/>')
    out.append('</g>')
    if glow > .3:
        s.glow(x, y, size * 1.6, mix(c1, "#ffffff", .4), .18 * glow, .3)
    s.add("".join(out))
    if string_to:
        a = math.radians(rot)
        bx, by = x - math.sin(a) * size * .25, y + math.cos(a) * size * .25
        tx, ty = string_to
        mx, my = (bx + tx) / 2 + (ty - by) * sag, (by + ty) / 2 + abs(tx - bx) * sag * .5
        s.add(f'<path d="M{f(bx)} {f(by)}Q{f(mx)} {f(my)} {f(tx)} {f(ty)}" stroke="{string_color}" stroke-opacity="{string_a}" stroke-width=".9" fill="none"/>')


J_KITE = dict(head=(1, -92), neck=(0, -84), ls=(-8, -80), rs=(8, -80), lh=(-6, -50), rh=(6, -50),
              le=(-6, -66), lw=(4, -62), re=(16, -96), rw=(22, -112),
              lk=(-6, -26), lf=(-9, 0), rk=(6, -26), rf=(9, 0))


@scene
def kite(s):
    sun = (560, 640)
    s.sky([(0, "#4f6fae"), (.25, "#7f98c8"), (.45, "#bdb9d4"), (.58, "#f0c8b8"), (.66, "#ffd29c"), (.72, "#ffe2b0")], 0, 1000)
    s.sun(*sun, 38, core="#fffaf0", rim="#ffe0a0", halo="#ffc070", halo_r=640, halo_a=.75)
    s.fx("clouds", y0=480, y1=640, seed=61, cell=90, aniso=6, cover=.3, soft=.22, lit="#ffd8b0", body=.85, direct=.9,
         light=(-.2, 1), sun=(sun[0], sun[1], 320), opacity=.75, top_fade=.4)
    import arch
    # far city in the haze, then nearer rooftops
    arch.skyline(s, -20, 1640, 690, h=(30, 70), color="#b88a98", seed=71, windows=0, parapet=True, temples=[(1180, .5)], chhatris=[(300, .45), (900, .4)])
    s.mist(690, 70, "#ffd6b0", .6, 16)
    arch.skyline(s, -30, 1660, 770, h=(60, 150), color="#7a5470", rim="#ffcf9a", light=-1, seed=72, windows=.05,
                 temples=[(1380, .8)], chhatris=[(180, .6), (760, .55)], storey=28, win_color="#ffd9a0")
    s.add(f'<rect x="-10" y="768" width="1620" height="240" fill="#7a5470"/>')
    s.mist(780, 90, "#f2b8a0", .45, 20)
    # the roof terraces nearest us
    rng = random.Random(9)
    roofs = [(-30, 880, 360), (330, 840, 300), (630, 900, 260), (890, 860, 330), (1220, 820, 420)]
    for x0, top, w in roofs:
        g = s.lin([(0, "#4a2c40", 1), (1, "#22131e", 1)], 0, top, 0, 1000, user=True)
        s.add(f'<rect x="{x0}" y="{top}" width="{w}" height="{1000 - top}" fill="{g}"/>'
              f'<rect x="{x0 - 6}" y="{top - 22}" width="{w + 12}" height="22" fill="#3a2234"/>'
              f'<rect x="{x0 - 6}" y="{top - 22}" width="{w + 12}" height="3" fill="#ffc890" opacity=".55"/>')
        cut = "".join(f'<rect x="{xx}" y="{top - 16}" width="10" height="11" rx="5"/>' for xx in range(x0 + 14, x0 + w - 10, 24))
        s.add(f'<g fill="#e8a888" opacity=".35">{cut}</g>')
        if rng.random() < .6:
            tx = x0 + w * rng.uniform(.6, .85)
            s.add(f'<rect x="{f(tx)}" y="{top - 70}" width="46" height="48" fill="#2e1a28"/><rect x="{f(tx - 4)}" y="{top - 74}" width="54" height="6" fill="#3a2234"/>')
    # people flying kites from the terraces
    fliers = [(150, 858, .9, False), (470, 818, .85, True), (760, 878, .95, False), (1040, 838, .9, True), (1400, 798, 1.0, False)]
    hands = []
    for x, y, sc, fl in fliers:
        person(s, x, y, sc, J_KITE, "#1e1018", "#ffc890", flip=fl, kurta=(-13, 13, -30, 1), hair=None, waist=1.5)
        hands.append(joint(x, y, sc, J_KITE, "rw", fl))
    # the kites, far and small first
    kites = []
    palette = [("#e8246e", "#ffd23a"), ("#ff8a1a", "#2a6ad8"), ("#2fb35a", "#ffffff"), ("#ffd23a", "#d8202a"),
               ("#1fa6c8", "#ff5aa0"), ("#8a3ad0", "#ffd23a"), ("#d8202a", "#ffffff"), ("#ff5a1a", "#1f9a4a")]
    for i in range(16):
        x, y = rng.uniform(60, 1540), rng.uniform(300, 560)
        kites.append((x, y, rng.uniform(9, 18), rng.uniform(-25, 25), i))
    for i in range(7):
        x, y = rng.uniform(120, 1480), rng.uniform(150, 420)
        kites.append((x, y, rng.uniform(22, 38), rng.uniform(-25, 25), 20 + i))
    kites.sort(key=lambda k: k[2])
    for x, y, sz, rot, i in kites:
        c1, c2 = palette[i % len(palette)]
        d = math.hypot(x - sun[0], y - sun[1])
        g = max(0.0, 1 - d / 700)
        tx = x + rng.uniform(-200, 200)
        patang(s, x, y, sz, rot, c1, c2, KITE_STYLES[i % 5], glow=g, string_to=(tx, 1010) if i % 2 else None, sag=.1, string_a=.12 + .15 * g)
    # the big kites near us, tied to the fliers' hands
    big = [(380, 210, 70, -14, ("#ff7a1a", "#2fb35a"), "moon", 0), (690, 330, 52, 10, ("#ffd23a", "#d8202a"), "cap", 2),
           (1020, 170, 84, 16, ("#e8246e", "#ffd23a"), "stripe", 3), (1290, 330, 58, -8, ("#ff8a1a", "#2a6ad8"), "halves", 4),
           (180, 420, 46, 18, ("#1fa6c8", "#ff5aa0"), "halves", 0)]
    for x, y, sz, rot, (c1, c2), st, hi in big:
        d = math.hypot(x - sun[0], y - sun[1])
        patang(s, x, y, sz, rot, c1, c2, st, glow=max(0.0, 1 - d / 800), string_to=hands[hi], sag=.14, string_a=.6)
    s.birds(12, 700, 1200, 420, 560, color="#4a3048", s=(5, 9), seed=5, a=.75)
    s.fx("godrays", cx=sun[0], cy=sun[1], strength=.4, thresh=.72, decay=.97, radius=260)
    s.fx("mottle", amp=.035, cell=60)
    s.look = {"vibrance": .12}
    return s


# ======================================================================
# 4. Garba: the garbo pot and the dandiya sticks
# ======================================================================
def garbo(s, cx, base, sc=1.0, seed=1):
    """A pierced clay garbo pot with a lamp burning inside; light escapes through its holes.
    base is where it stands. About 230 * sc tall."""
    rng = random.Random(seed)
    r = 118 * sc
    top = base - 228 * sc
    neck_y = base - 200 * sc
    pot = (f"M{f(cx - 34 * sc)} {f(top)}H{f(cx + 34 * sc)}L{f(cx + 30 * sc)} {f(neck_y)}"
           f"C{f(cx + r * 1.05)} {f(neck_y + 30 * sc)} {f(cx + r * 1.08)} {f(base - 60 * sc)} {f(cx + 52 * sc)} {f(base - 8 * sc)}"
           f"Q{f(cx)} {f(base + 4 * sc)} {f(cx - 52 * sc)} {f(base - 8 * sc)}"
           f"C{f(cx - r * 1.08)} {f(base - 60 * sc)} {f(cx - r * 1.05)} {f(neck_y + 30 * sc)} {f(cx - 30 * sc)} {f(neck_y)}Z")
    s.glow(cx, base - 110 * sc, 520 * sc, "#ff8a2a", .4, .2)
    s.add(f'<ellipse cx="{f(cx)}" cy="{f(base)}" rx="{f(r * 1.3)}" ry="{f(18 * sc)}" fill="#000" opacity=".5" filter="{s.blur(10 * sc)}"/>')
    body = s.rad([(0, "#c8602a", 1), (0.5, "#9a3c18", 1), (1, "#3a1206", 1)], cx - 30 * sc, base - 140 * sc, r * 1.3, user=True)
    s.add(f'<path d="{pot}" fill="{body}"/>')
    # painted bands of white and yellow dots
    bands = []
    for yy, rr, col in ((neck_y + 22 * sc, .62, "#fbe7b8"), (base - 150 * sc, .9, "#f2b232"), (base - 52 * sc, .78, "#fbe7b8")):
        for k in range(15):
            t = (k + .5) / 15
            px = cx - math.cos(math.pi * t) * r * rr
            bands.append(f'<circle cx="{f(px)}" cy="{f(yy + math.sin(math.pi * t) * 8 * sc)}" r="{f(2.6 * sc)}" fill="{col}" opacity="{.4 + .5 * math.sin(math.pi * t):.2f}"/>')
    s.add("".join(bands))
    # the holes: rows of round and leaf-shaped piercings, glowing
    holes, glows = [], []
    rows = [(base - 175 * sc, .55, 7, "o"), (base - 140 * sc, .78, 9, "v"), (base - 104 * sc, .86, 10, "o"), (base - 72 * sc, .78, 9, "v")]
    for yy, rr, n, kind in rows:
        for k in range(n):
            t = (k + .5) / n
            px = cx - math.cos(math.pi * t) * r * rr
            foreshort = math.sin(math.pi * t)
            py = yy + foreshort * 10 * sc
            w = 6.5 * sc * foreshort
            if kind == "o":
                holes.append(f'<ellipse cx="{f(px)}" cy="{f(py)}" rx="{f(w)}" ry="{f(6.5 * sc)}"/>')
            else:
                holes.append(f'<path d="M{f(px)} {f(py - 11 * sc)}Q{f(px + w * 1.2)} {f(py)} {f(px)} {f(py + 11 * sc)}Q{f(px - w * 1.2)} {f(py)} {f(px)} {f(py - 11 * sc)}Z"/>')
            glows.append((px, py, foreshort))
    s.add(f'<g fill="#ffe8a8">{"".join(holes)}</g>')
    s.add(f'<g fill="#fffbe8" opacity=".85" transform="translate(0 0)">{"".join(holes)}</g>')
    for px, py, fs in glows:
        s.glow(px, py, 30 * sc * (.5 + fs), "#ffb050", .55 * fs, .3)
    # light beams through the holes, faint
    beams = []
    for px, py, fs in glows:
        ang = math.atan2(py - (base - 120 * sc), px - cx)
        L = 220 * sc
        beams.append(f"M{f(px)} {f(py)}L{f(px + math.cos(ang - .04) * L)} {f(py + math.sin(ang - .04) * L)}L{f(px + math.cos(ang + .04) * L)} {f(py + math.sin(ang + .04) * L)}Z")
    bg = s.rad([(0, "#ffc070", .22), (1, "#ffc070", 0)], cx, base - 120 * sc, 330 * sc, user=True)
    s.add(f'<path d="{"".join(beams)}" fill="{bg}" filter="{s.blur(3)}" style="mix-blend-mode:screen"/>')
    # rim, and the flame showing at the mouth
    s.add(f'<ellipse cx="{f(cx)}" cy="{f(top)}" rx="{f(34 * sc)}" ry="{f(8 * sc)}" fill="#ffb050"/><ellipse cx="{f(cx)}" cy="{f(top + 1 * sc)}" rx="{f(28 * sc)}" ry="{f(5.5 * sc)}" fill="#fff0c0"/>')
    s.flame(cx, top - 2 * sc, 58 * sc, glow_r=300 * sc, glow_a=.5)
    sh = s.lin([(0, "#000", .35), (0.35, "#000", 0), (0.75, "#000", 0), (1, "#000", .45)], cx - r, 0, cx + r, 0, user=True)
    s.add(f'<path d="{pot}" fill="{sh}"/>')


def dandiya(s, x0, y0, x1, y1, w=11, colors=("#d8202a", "#ffd23a", "#2fa04a", "#1f6fd0"), seed=1):
    """A lacquered dandiya stick wound with coloured bands, mirror-work glints and a tassel at each end."""
    rng = random.Random(seed)
    L = math.hypot(x1 - x0, y1 - y0)
    a = math.degrees(math.atan2(y1 - y0, x1 - x0))
    out = [f'<g transform="translate({f(x0)} {f(y0)}) rotate({f(a)})">']
    out.append(f'<rect x="0" y="{f(-w / 2)}" width="{f(L)}" height="{f(w)}" rx="{f(w / 2)}" fill="#8a4a1a"/>')
    n = 14
    for k in range(n):
        c = colors[k % len(colors)]
        out.append(f'<rect x="{f(L * k / n)}" y="{f(-w / 2)}" width="{f(L / n * .62)}" height="{f(w)}" fill="{c}"/>')
        out.append(f'<circle cx="{f(L * (k + .8) / n)}" cy="0" r="{f(w * .22)}" fill="#fff6dc"/>')
    out.append(f'<rect x="0" y="{f(-w / 2)}" width="{f(L)}" height="{f(w)}" rx="{f(w / 2)}" fill="{s.lin([(0, "#fff", .45), (0.35, "#fff", 0), (0.7, "#000", .1), (1, "#000", .5)], 0, 0, 0, 1)}"/>')
    for ex in (0, L):
        out.append(f'<circle cx="{f(ex)}" cy="0" r="{f(w * .7)}" fill="#e8b84a"/>')
        for j in range(5):
            dy = (j - 2) * w * .3
            out.append(f'<path d="M{f(ex)} {f(dy * .3)}Q{f(ex + (w if ex else -w) * .6)} {f(dy + w)} {f(ex + (w * .2 if ex else -w * .2))} {f(dy * 1.4 + w * 2.6)}" stroke="{colors[j % len(colors)]}" stroke-width="{f(w * .28)}" fill="none" stroke-linecap="round"/>')
    out.append('</g>')
    s.add("".join(out))


J_GARBA_UP = dict(head=(2, -92), neck=(0, -84), ls=(-8, -80), rs=(8, -80), lh=(-6, -51), rh=(7, -51),
                  le=(-14, -96), lw=(-6, -110), re=(16, -94), rw=(10, -110),
                  lk=(-6, -26), lf=(-9, 0), rk=(8, -26), rf=(14, -4))
J_GARBA_LOW = dict(head=(10, -86), neck=(6, -79), ls=(-3, -76), rs=(12, -73), lh=(-4, -48), rh=(9, -47),
                   le=(-14, -64), lw=(-6, -54), re=(24, -66), rw=(30, -56),
                   lk=(-4, -24), lf=(-10, 0), rk=(12, -24), rf=(16, 0))
J_GARBA_TURN = dict(head=(-3, -92), neck=(-1, -84), ls=(-9, -80), rs=(8, -80), lh=(-7, -51), rh=(6, -51),
                    le=(-24, -88), lw=(-34, -100), re=(18, -72), rw=(26, -62),
                    lk=(-6, -26), lf=(-8, 0), rk=(6, -26), rf=(9, 0))


@scene
def garba(s):
    s.sky([(0, "#0a0a2a"), (.3, "#1c1446"), (.55, "#3a1a52"), (.7, "#5a2048")], 0, 720)
    s.stars(40, 0, 220, seed=21, bright=.45)
    # strings of festive lights criss-crossing overhead
    rng = random.Random(3)
    bulbs = []
    for k, (x0, y0, x1, y1, sag) in enumerate([(-40, 120, 1640, 160, 90), (-40, 260, 900, 140, 60), (700, 150, 1640, 280, 70), (-40, 380, 1640, 360, 60)]):
        pts = []
        for i in range(60):
            t = i / 59
            x = x0 + (x1 - x0) * t
            y = y0 + (y1 - y0) * t + sag * 4 * t * (1 - t)
            pts.append((x, y))
        s.add(f'<path d="{pts_d(pts, False)}" stroke="#0a0614" stroke-width="1.6" fill="none" opacity=".8"/>')
        for i in range(0, 60, 2):
            x, y = pts[i]
            c = ["#ffcf5a", "#ff6a9a", "#7ad8ff", "#9aff8a", "#ffa040"][(i // 2 + k) % 5]
            bulbs.append((x, y + 6, c))
    s.add(f'<g style="mix-blend-mode:screen" filter="{s.blur(4)}">' + "".join(f'<circle cx="{f(x)}" cy="{f(y)}" r="9" fill="{c}" opacity=".55"/>' for x, y, c in bulbs) + '</g>')
    s.add("".join(f'<circle cx="{f(x)}" cy="{f(y)}" r="3.4" fill="{mix(c, "#ffffff", .6)}"/>' for x, y, c in bulbs))
    s.bokeh(14, 0, 1600, 60, 520, colors=("#ff6a9a", "#ffcf5a", "#7ad8ff", "#ffa040"), r=(14, 40), a=(.06, .16), blur=8, seed=4)
    # the ground of the courtyard, lit warm from the centre
    gy = 700
    s.add(f'<rect y="{gy}" width="{W}" height="{H - gy}" fill="{s.lin([(0, "#3a1830", 1), (1, "#12060e", 1)], 0, gy, 0, 1000, user=True)}"/>')
    s.add(f'<ellipse cx="800" cy="{gy + 120}" rx="900" ry="200" fill="{s.rad([(0, "#ff8a3a", .45), (1, "#ff8a3a", 0)], .5, .5, .5)}" style="mix-blend-mode:screen"/>')
    s.mist(gy, 90, "#a04a80", .35, 24)
    # the circle of dancers, swirling round the lamp (motion-blurred)
    dancers = [(240, 742, 2.1, J_GARBA_TURN, False, 6), (430, 724, 1.9, J_GARBA_UP, True, -5), (600, 712, 1.75, J_GARBA_LOW, False, 4),
               (1000, 712, 1.75, J_GARBA_UP, False, -4), (1170, 724, 1.9, J_GARBA_LOW, True, 5), (1360, 742, 2.1, J_GARBA_TURN, True, -6)]
    for x, y, sc, J, fl, sw in dancers:
        ghost = f'<g opacity=".35" filter="{s.blur(6)}" transform="translate({-14 if fl else 14} 0)">'
        s.add(ghost)
        person(s, x, y, sc, J, "#1a0a20", None, flip=fl, skirt=(-34, 34, 0, sw), hair="bun", waist=3.4,
               sticks=[("lw", -60, 26), ("rw", -120, 26)])
        s.add('</g>')
        person(s, x, y, sc, J, "#1a0a20", "#ff9a5a", rim_dx=.7, flip=fl, skirt=(-34, 34, 0, sw), hair="bun", waist=3.4,
               sticks=[("lw", -60, 26), ("rw", -120, 26)],
               dupatta=[(-8, -80), (-26, -70), (-42, -78), (-56, -64)] if J is J_GARBA_TURN else None)
    # bajot stool with a red cloth, the garbo upon it
    cx = 800
    s.add(f'<path d="M640 900L660 862H940L960 900Z" fill="#5a2a14"/><rect x="636" y="900" width="328" height="22" fill="#3a1608"/>'
          f'<path d="M650 922V990M950 922V990" stroke="#2a1006" stroke-width="16"/>')
    s.add(f'<path d="M652 870H948L966 908Q800 930 634 908Z" fill="#b0141e"/><path d="M634 908Q800 930 966 908" stroke="#ffcf5a" stroke-width="5" fill="none"/>')
    s.add("".join(f'<circle cx="{f(640 + k * 13.6)}" cy="{f(912 + math.sin(k / 24 * math.pi) * 9)}" r="2.6" fill="#fff0b0"/>' for k in range(25)))
    garbo(s, cx, 874, 1.0, seed=2)
    s.add(ob.marigold(672, 868, 16, "#f39a1c", 1) + ob.marigold(700, 874, 13, "#f7c02a", 2) + ob.marigold(930, 870, 15, "#e8562a", 3) + ob.marigold(902, 876, 12, "#f39a1c", 4))
    # the dandiya sticks, crossed against the stool
    dandiya(s, 990, 980, 1150, 760, 12, seed=1)
    dandiya(s, 1170, 990, 1010, 770, 12, colors=("#ff3d8b", "#ffd23a", "#1aa6a6", "#7a3cc0"), seed=2)
    dandiya(s, 590, 992, 440, 800, 12, colors=("#ffd23a", "#d8202a", "#1f6fd0", "#2fa04a"), seed=3)
    dandiya(s, 622, 996, 478, 806, 12, colors=("#ffd23a", "#d8202a", "#1f6fd0", "#2fa04a"), seed=4)
    s.motes(30, 500, 1100, 300, 800, seed=9, size=(.8, 1.8))
    s.fx("mottle", amp=.04, cell=60)
    s.look = {"vibrance": .1}
    return s


# ======================================================================
# vessels and fire
# ======================================================================
COPPER = [(0, "#3a1408"), (0.16, "#7a3214"), (0.38, "#d07a3a"), (0.48, "#ffd8a8"), (0.56, "#e08a48"), (0.8, "#8a3a18"), (1, "#2a0e06")]


def kalash(s, cx, base, sc=1.0, metal=COPPER, coconut=True, leaves=7, cloth=None, seed=1):
    """A kalash: a copper pot of water with mango leaves at its mouth and a coconut
    wrapped in red cloth on top, mauli thread tied round its neck. base is where it stands;
    about 330 * sc tall with the coconut."""
    rng = random.Random(seed)
    g = s.lin(metal, cx - 100 * sc, 0, cx + 100 * sc, 0, user=True)
    s.add(f'<ellipse cx="{f(cx)}" cy="{f(base)}" rx="{f(110 * sc)}" ry="{f(14 * sc)}" fill="#000" opacity=".45" filter="{s.blur(8 * sc)}"/>')
    belly = (f"M{f(cx - 30 * sc)} {f(base - 150 * sc)}C{f(cx - 120 * sc)} {f(base - 140 * sc)} {f(cx - 110 * sc)} {f(base - 10 * sc)} {f(cx - 40 * sc)} {f(base - 2 * sc)}"
             f"H{f(cx + 40 * sc)}C{f(cx + 110 * sc)} {f(base - 10 * sc)} {f(cx + 120 * sc)} {f(base - 140 * sc)} {f(cx + 30 * sc)} {f(base - 150 * sc)}Z")
    neck = f"M{f(cx - 34 * sc)} {f(base - 146 * sc)}L{f(cx - 28 * sc)} {f(base - 178 * sc)}H{f(cx + 28 * sc)}L{f(cx + 34 * sc)} {f(base - 146 * sc)}Z"
    rim = f"M{f(cx - 52 * sc)} {f(base - 186 * sc)}Q{f(cx)} {f(base - 176 * sc)} {f(cx + 52 * sc)} {f(base - 186 * sc)}L{f(cx + 44 * sc)} {f(base - 174 * sc)}Q{f(cx)} {f(base - 168 * sc)} {f(cx - 44 * sc)} {f(base - 174 * sc)}Z"
    s.add(f'<path d="{belly}" fill="{g}"/><path d="{neck}" fill="{g}"/>')
    # reflections of the room and soft shading on the belly
    s.add(f'<path d="{belly}" fill="{s.lin([(0, "#fff", 0), (0.6, "#000", 0), (1, "#000", .45)], 0, base - 150 * sc, 0, base, user=True)}"/>')
    s.add(f'<ellipse cx="{f(cx - 38 * sc)}" cy="{f(base - 92 * sc)}" rx="{f(9 * sc)}" ry="{f(34 * sc)}" fill="#fff4dc" opacity=".55" filter="{s.blur(4 * sc)}"/>')
    # kumkum and haldi marks
    s.add("".join(f'<circle cx="{f(cx + dx * sc)}" cy="{f(base - 96 * sc + dy * sc)}" r="{f(5 * sc)}" fill="{c}"/>'
                  for dx, dy, c in ((-14, 0, "#c0141e"), (0, -6, "#f2b232"), (14, 0, "#c0141e"), (0, 10, "#c0141e"))))
    # mauli thread wound round the neck
    s.add("".join(f'<path d="M{f(cx - 32 * sc)} {f(base - (150 + k * 4) * sc)}Q{f(cx)} {f(base - (144 + k * 4) * sc)} {f(cx + 32 * sc)} {f(base - (150 + k * 4) * sc)}" stroke="{("#d0141e", "#f2b232")[k % 2]}" stroke-width="{f(2.6 * sc)}" fill="none"/>' for k in range(6)))
    s.add(f'<path d="M{f(cx + 30 * sc)} {f(base - 156 * sc)}q{f(10 * sc)} {f(20 * sc)} {f(4 * sc)} {f(40 * sc)}M{f(cx + 30 * sc)} {f(base - 156 * sc)}q{f(16 * sc)} {f(16 * sc)} {f(14 * sc)} {f(36 * sc)}" stroke="#d0141e" stroke-width="{f(2.4 * sc)}" fill="none"/>')
    # mango leaves fanned out from the mouth
    lv = []
    for k in range(leaves):
        a = -172 + 164 * k / (leaves - 1) + rng.uniform(-5, 5)
        L = 132 * sc * (1 - abs(k - (leaves - 1) / 2) * .06)
        lv.append(mango_leaf(cx + math.cos(math.radians(a)) * 26 * sc, base - 184 * sc, L, L * .28, a - 90 + (14 if a < -90 else -14), "#1f4a1e", "#6aa03a", "#d8f0a0", s))
    s.add("".join(lv))
    s.add(f'<path d="{rim}" fill="{g}"/>')
    if coconut:
        cy = base - 218 * sc
        s.add(f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(40 * sc)}" ry="{f(48 * sc)}" fill="{s.rad([(0, "#c08a4a", 1), (0.6, "#7a4a22", 1), (1, "#3a1e0a", 1)], .38, .32, .75)}"/>')
        s.add("".join(f'<path d="M{f(cx - 38 * sc)} {f(cy + (8 + k * 5) * sc)}Q{f(cx)} {f(cy + (20 + k * 5) * sc)} {f(cx + 38 * sc)} {f(cy + (8 + k * 5) * sc)}" stroke="{("#d0141e", "#f2b232")[k % 2]}" stroke-width="{f(2.4 * sc)}" fill="none"/>' for k in range(3)))
        s.add(f'<path d="M{f(cx - 9 * sc)} {f(cy - 44 * sc)}Q{f(cx - 6 * sc)} {f(cy - 70 * sc)} {f(cx + 3 * sc)} {f(cy - 78 * sc)}Q{f(cx + 4 * sc)} {f(cy - 62 * sc)} {f(cx + 11 * sc)} {f(cy - 44 * sc)}Z" fill="#7a4a22"/>'
              f'<circle cx="{f(cx)}" cy="{f(cy + 2 * sc)}" r="{f(6 * sc)}" fill="#c0141e"/>')
        fib = "".join(f"M{f(cx + rng.uniform(-26, 26) * sc)} {f(cy - rng.uniform(10, 44) * sc)}q{f(rng.uniform(-6, 6) * sc)} {f(rng.uniform(8, 20) * sc)} {f(rng.uniform(-4, 4) * sc)} {f(rng.uniform(20, 34) * sc)}" for _ in range(30))
        s.add(f'<path d="{fib}" stroke="#d8a868" stroke-opacity=".35" stroke-width="{f(1.2 * sc)}" fill="none"/>')
        if cloth:
            wrap = (f"M{f(cx - 50 * sc)} {f(cy + 4 * sc)}Q{f(cx)} {f(cy - 14 * sc)} {f(cx + 50 * sc)} {f(cy + 4 * sc)}"
                    f"L{f(cx + 60 * sc)} {f(cy + 50 * sc)}Q{f(cx)} {f(cy + 64 * sc)} {f(cx - 60 * sc)} {f(cy + 50 * sc)}Z")
            s.add(f'<path d="{wrap}" fill="{s.lin([(0, mix(cloth, "#ff8080", .3), 1), (0.5, cloth, 1), (1, mix(cloth, "#000000", .5), 1)], 0, 0, 1, 0)}"/>'
                  f'<path d="M{f(cx - 50 * sc)} {f(cy + 4 * sc)}Q{f(cx)} {f(cy - 14 * sc)} {f(cx + 50 * sc)} {f(cy + 4 * sc)}" stroke="#f2c04a" stroke-width="{f(4 * sc)}" fill="none"/>'
                  + "".join(f'<circle cx="{f(cx + (k - 4) * 12 * sc)}" cy="{f(cy + 30 * sc + abs(k - 4) * 1.5 * sc)}" r="{f(2.2 * sc)}" fill="#f2c04a"/>' for k in range(9)))
    return base - 300 * sc


def tongue(s, x, y, w, h, lean=0.0, seed=1, a=1.0):
    """One licking tongue of fire: a slim S-curved flame whose base is at (x, y)."""
    rng = random.Random(seed)
    tx = x + lean * h
    k = rng.uniform(-.25, .25) * w
    d = (f"M{f(x - w)} {f(y)}C{f(x - w * 1.1)} {f(y - h * .35)} {f(x - w * .2 + k + lean * h * .4)} {f(y - h * .55)} {f(x - w * .25 + lean * h * .6)} {f(y - h * .75)}"
         f"C{f(x - w * .3 + lean * h * .8)} {f(y - h * .85)} {f(tx - w * .1)} {f(y - h * .93)} {f(tx)} {f(y - h)}"
         f"C{f(tx + w * .1)} {f(y - h * .8)} {f(x + w * .5 + k + lean * h * .5)} {f(y - h * .6)} {f(x + w * .7 + lean * h * .3)} {f(y - h * .4)}"
         f"C{f(x + w * 1.1)} {f(y - h * .2)} {f(x + w)} {f(y - h * .05)} {f(x + w)} {f(y)}Z")
    g = s.lin([(0, "#fffbe0", 1), (0.25, "#ffe08a", 1), (0.55, "#ffa040", .95), (0.85, "#e8501e", .7), (1, "#a02010", 0)], 0, y, 0, y - h, user=True)
    s.add(f'<path d="{d}" fill="{g}" opacity="{a}" filter="{s.blur(max(.6, w * .06))}" style="mix-blend-mode:screen"/>')


def fire(s, cx, cy, w, h, n=13, seed=1, smoke=True):
    """Sacred fire: tongues of flame rising from a bed of embers at (cx, cy)."""
    rng = random.Random(seed)
    s.glow(cx, cy - h * .4, h * 6, "#ff7a2a", .55, .16)
    s.glow(cx, cy - h * .3, h * 2.2, "#ffb04a", .5, .3)
    for k in range(n):
        t = (k + .5) / n
        x = cx + (t - .5) * w * .9 + rng.uniform(-6, 6)
        hh = h * (1 - abs(t - .5) * 1.2) * rng.uniform(.55, 1.15)
        tongue(s, x, cy, w * rng.uniform(.06, .1), hh, (t - .5) * .3 + rng.uniform(-.12, .12), seed * 50 + k, .85)
    for k in range(5):
        t = (k + .5) / 5
        tongue(s, cx + (t - .5) * w * .5, cy, w * .14, h * .45 * rng.uniform(.8, 1.1), rng.uniform(-.1, .1), seed * 90 + k, 1)
    s.add(f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(w * .55)}" ry="{f(h * .07)}" fill="#ffe8a0" opacity=".9" filter="{s.blur(4)}"/>')
    sp = []
    for _ in range(46):
        x = cx + rng.uniform(-w, w) * .7
        y = cy - rng.uniform(.4, 2.8) * h
        sp.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(rng.uniform(.8, 2))}" fill="#ffd890" opacity="{rng.uniform(.4, 1):.2f}"/>')
    s.add(f'<g style="mix-blend-mode:screen">{"".join(sp)}</g>')
    if smoke:
        for k in range(3):
            s.smoke(cx + (k - 1) * w * .2, cy - h * .9, h * 3.2, color="#e8d8c8", a=.2, seed=seed + k, width=2.4, drift=.1)


# ======================================================================
# 6. Griha pravesh: the threshold of a new home
# ======================================================================
@scene
def threshold(s):
    dl, dr, dt, sill = 560, 1040, 150, 690
    # pale lime-washed wall of the new house in cool morning shade
    wall = "#d8c4ae"
    s.add(f'<rect width="{W}" height="{H}" fill="{wall}"/>')
    s.add(f'<rect width="{W}" height="{H}" fill="{wall}" filter="{s.grain(0.01, 3, .1, 5, "#6a4a3a")}"/>')
    s.add(f'<rect width="{W}" height="{H}" fill="{s.lin([(0, "#fff0d8", .3), (0.35, "#fff0d8", 0), (0.7, "#7a6a8a", .12), (1, "#4a4a7a", .35)], 0, 0, 1, 0)}"/>')
    # morning sunlight slanting across the wall from the left
    s.add(f'<path d="M-100 -40L420 -40L180 700L-100 760Z" fill="#fff4dc" opacity=".55" filter="{s.blur(36)}" style="mix-blend-mode:screen"/>')
    # the door frame, carved and oiled new teak, with the doors open onto a lit room
    fr = 70
    s.add(f'<rect x="{dl - fr - 10}" y="{dt - fr - 10}" width="{dr - dl + 2 * fr + 20}" height="{sill - dt + fr + 30}" fill="#000" opacity=".35" filter="{s.blur(16)}" transform="translate(8 10)"/>')
    wood = s.lin([(0, "#8a4a22"), (0.4, "#6a3214"), (1, "#3a1608")], 0, 0, 1, 0)
    s.add(f'<rect x="{dl - fr}" y="{dt - fr}" width="{dr - dl + 2 * fr}" height="{sill - dt + fr}" fill="{wood}"/>')
    for k, inset in enumerate((8, 22, 38, 52)):
        s.add(f'<path d="M{dl - fr + inset} {sill}V{dt - fr + inset}H{dr + fr - inset}V{sill}" fill="none" stroke="{"#e0a050" if k % 2 == 0 else "#2a1004"}" stroke-opacity="{.55 if k % 2 == 0 else .55}" stroke-width="{2.4 if k % 2 == 0 else 4}"/>')
    lotus_row = "".join(f'<g transform="translate({x} {dt - fr + 30})">' + "".join(f'<path d="{_petal(5, 11)}" transform="rotate({a})"/>' for a in (-60, -30, 0, 30, 60)) + '</g>' for x in range(dl - fr + 50, dr + fr - 40, 36))
    s.add(f'<g fill="#e8b060" opacity=".75">{lotus_row}</g>')
    beads = "".join(f'<circle cx="{x}" cy="{y}" r="3"/>' for x in (dl - fr + 30, dr + fr - 30) for y in range(dt - 20, sill - 6, 18))
    s.add(f'<g fill="#f0c070" opacity=".7">{beads}</g>')
    # the room within: warm light, a floor running back, a brass lamp glowing far inside
    ig = s.rad([(0, "#fffbe8", 1), (0.3, "#ffe2a0", 1), (0.7, "#f0a048", 1), (1, "#a04a18", 1)], 800, 520, 420, user=True)
    s.add(f'<rect x="{dl}" y="{dt}" width="{dr - dl}" height="{sill - dt}" fill="{ig}"/>')
    s.add(f'<path d="M{dl} {sill}L{dl + 70} {sill - 120}H{dr - 70}L{dr} {sill}Z" fill="#e8883a" opacity=".4"/>')
    s.add(f'<path d="M{dl + 70} {sill - 120}H{dr - 70}" stroke="#b05a20" stroke-opacity=".35" stroke-width="2"/>')
    ob.bells(s, [650, 950], dt, color="#c8902e", blur=4, sc=.8, seed=4)
    for side in (-1, 1):
        ex = dl if side < 0 else dr
        ix = ex - side * 80
        s.add(f'<path d="M{ex} {dt}L{ix} {dt + 40}V{sill - 70}L{ex} {sill}Z" fill="#6a3214"/>'
              f'<path d="M{ex} {dt}L{ix} {dt + 40}V{sill - 70}L{ex} {sill}Z" fill="{s.lin([(0, "#000", .45), (1, "#ffb060", .3)], ex, 0, ix, 0, user=True)}"/>'
              f'<path d="M{ix} {dt + 40}V{sill - 70}" stroke="#ffd890" stroke-opacity=".7" stroke-width="3"/>')
        studs = "".join(f'<circle cx="{f(ex - side * (20 + 40 * t))}" cy="{f(dt + 30 + (sill - dt - 70) * j / 8 + 40 * t * (1 - j / 4))}" r="3"/>' for j in range(1, 8) for t in (.3, .7))
        s.add(f'<g fill="#ffd27a" opacity=".8">{studs}</g>')
    s.glow(800, 470, 520, "#ffc070", .45, .25)
    # light spilling out over the threshold onto the floor
    floor_top = sill + 40
    s.add(f'<rect y="{floor_top}" width="{W}" height="{H - floor_top}" fill="{s.lin([(0, "#a8907c", 1), (1, "#6a5448", 1)], 0, floor_top, 0, 1000, user=True)}"/>')
    s.add(f'<rect y="{floor_top}" width="{W}" height="{H - floor_top}" fill="#8a7464" filter="{s.grain(0.02, 3, .08, 8, "#000000")}"/>')
    s.add(f'<path d="{"".join(f"M{f(800 + (x - 800) * .5)} {floor_top}L{f(x + (x - 800) * .5)} 1000" for x in range(-600, 2300, 220))}M0 {floor_top + 50}H1600M0 {floor_top + 130}H1600" stroke="#3a2a22" stroke-opacity=".18" stroke-width="2"/>')
    s.add(f'<path d="M{dl} {floor_top}H{dr}L{dr + 260} 1000H{dl - 260}Z" fill="{s.lin([(0, "#ffc070", .55), (1, "#ffa050", .1)], 0, floor_top, 0, 1000, user=True)}" filter="{s.blur(24)}" style="mix-blend-mode:screen"/>')
    # the raised threshold, smeared with turmeric and dotted with kumkum
    s.add(f'<rect x="{dl - fr - 20}" y="{sill}" width="{dr - dl + 2 * fr + 40}" height="40" fill="{s.lin([(0, "#e8b040", 1), (1, "#a8701a", 1)], 0, sill, 0, sill + 40, user=True)}"/>'
          f'<rect x="{dl - fr - 20}" y="{sill}" width="{dr - dl + 2 * fr + 40}" height="4" fill="#fff0c0" opacity=".7"/>'
          f'<rect x="{dl - fr - 20}" y="{sill + 40}" width="{dr - dl + 2 * fr + 40}" height="12" fill="#000" opacity=".35" filter="{s.blur(5)}"/>')
    s.add("".join(f'<circle cx="{x}" cy="{sill + 22}" r="7" fill="#c0141e"/>' for x in range(dl - fr, dr + fr + 10, 52)))
    # rangoli on the floor before the door
    lay_rangoli(s, 800, 905, 300, k=.24, seed=6, shade=.1)
    # the kalash on the threshold, lamps either side
    kalash(s, 800, sill + 26, 1.12, seed=3)
    for x in (622, 978):
        diya(s, x, sill + 18, .8, k=.3, flame_h=34, glow_a=.5, seed=x)
    for x in (380, 1220):
        ob.brass_lamp(s, x, 960, .7, flames=5, flame_h=34)
    # rice and petals scattered for the welcome
    rng = random.Random(5)
    s.add("".join(f'<ellipse cx="{f(rng.uniform(560, 1040))}" cy="{f(rng.uniform(744, 800))}" rx="2.4" ry="1.2" fill="#fff8e8" opacity=".9"/>' for _ in range(80)))
    ob.petals_scatter(s, 480, 1120, 740, 990, 40, seed=7, size=(5, 9))
    # mango-leaf toran with marigolds across the top
    toran(s, dl - fr - 30, dr + fr + 30, dt - fr - 6, sag=18, leaf=78, marigold_r=10, seed=5, rim="#e8f4b0", strand_len=5)
    s.motes(24, 560, 1040, 200, 680, seed=3, size=(.8, 1.8))
    s.fx("mottle", amp=.035, cell=60)
    s.look = {"vibrance": .1, "vignette": .3}
    return s


# ======================================================================
# 7. Vivaha: the wedding mandap at night
# ======================================================================
def drape(s, x0, x1, y, depth, n, color="#b0141e", border="#f2c04a", seed=1):
    """Swags of fabric hanging between x0 and x1 from the line y."""
    w = (x1 - x0) / n
    out = []
    for k in range(n):
        a, b = x0 + k * w, x0 + (k + 1) * w
        m = (a + b) / 2
        d = f"M{f(a)} {f(y)}Q{f(m)} {f(y + depth * 2)} {f(b)} {f(y)}Q{f(m)} {f(y + depth * .9)} {f(a)} {f(y)}Z"
        g = s.lin([(0, mix(color, "#ff9a9a", .25), 1), (0.6, color, 1), (1, mix(color, "#000000", .5), 1)], 0, y, 0, y + depth * 1.1, user=True)
        out.append(f'<path d="{d}" fill="{g}"/><path d="M{f(a)} {f(y)}Q{f(m)} {f(y + depth * 2)} {f(b)} {f(y)}" stroke="{border}" stroke-width="3" fill="none"/>')
        folds = "".join(f'M{f(a + (b - a) * t)} {f(y)}Q{f(m)} {f(y + depth * (1.2 + .6 * (1 - abs(t - .5) * 2)))} {f(b - (b - a) * t)} {f(y)}' for t in (.15, .3))
        out.append(f'<path d="{folds}" stroke="#000" stroke-opacity=".2" stroke-width="2" fill="none"/>')
        out.append(ob.marigold(a, y + 4, 12, "#f39a1c", k + seed))
    out.append(ob.marigold(x1, y + 4, 12, "#f39a1c", n + seed))
    s.add("".join(out))


def pillar(s, x, top, base, w, color="#efe2c8", shade="#8a7058", garland=True, seed=1, light_dir=1):
    """A slender mandap pillar wound with marigold strands."""
    g = s.lin([(0, shade, 1), (0.5, color, 1), (1, mix(shade, "#000000", .3), 1)] if light_dir > 0 else
              [(0, mix(shade, "#000000", .3), 1), (0.5, color, 1), (1, shade, 1)], x - w / 2, 0, x + w / 2, 0, user=True)
    s.add(f'<rect x="{f(x - w * .8)}" y="{f(base - w * .6)}" width="{f(w * 1.6)}" height="{f(w * .6)}" fill="{g}"/>'
          f'<rect x="{f(x - w / 2)}" y="{f(top)}" width="{f(w)}" height="{f(base - top)}" fill="{g}"/>'
          f'<rect x="{f(x - w * .75)}" y="{f(top - w * .3)}" width="{f(w * 1.5)}" height="{f(w * .4)}" fill="{g}"/>')
    if garland:
        rng = random.Random(seed)
        out = []
        n = int((base - top) / (w * .55))
        for k in range(n):
            t = k / n
            y = top + (base - top) * t
            ph = k * .9
            x2 = x + math.sin(ph) * w * .42
            c = ("#f39a1c", "#f7c02a", "#e8562a")[(k // 2) % 3]
            if math.cos(ph) > -.2:
                out.append(ob.marigold(x2, y, w * .26, c, seed * 100 + k))
        s.add("".join(out))


@scene
def mandap(s):
    s.sky([(0, "#05081a"), (.35, "#0e1434"), (.62, "#1e1a40"), (.75, "#2a1a3a")], 0, 760)
    s.stars(60, 0, 300, seed=31, bright=.45)
    # garden trees, and curtains of tiny lights behind the mandap
    rng = random.Random(7)
    trees = "".join(crown(x, 560 + rng.uniform(-40, 40), rng.uniform(90, 150), seed=x) for x in range(-60, 1700, 170))
    s.add(f'<path d="{trees}" fill="#0a0c18"/><rect y="600" width="{W}" height="400" fill="#0a0c18"/>')
    fairy = []
    for x in range(30, 1600, 34):
        top = 120 + 30 * math.sin(x * .01)
        for y in range(int(top), 640, 20):
            if rng.random() < .75:
                fairy.append((x + rng.uniform(-2, 2), y + rng.uniform(-3, 3)))
    s.add(f'<g style="mix-blend-mode:screen" filter="{s.blur(3)}">' + "".join(f'<circle cx="{f(x)}" cy="{f(y)}" r="4" fill="#ffc870" opacity=".35"/>' for x, y in fairy) + '</g>')
    s.add("".join(f'<circle cx="{f(x)}" cy="{f(y)}" r="1.5" fill="#fff0c8" opacity=".8"/>' for x, y in fairy))
    s.add(f'<rect width="{W}" height="{H}" fill="{s.lin([(0, "#05081a", .6), (0.25, "#05081a", 0)], 0, 0, 0, 640, user=True)}"/>')
    s.bokeh(18, 0, 1600, 100, 650, colors=("#ffc870", "#ff9a5a", "#ffe0a0"), r=(12, 36), a=(.08, .2), blur=6, seed=8)
    # the ground and the raised platform of the mandap
    s.add(f'<rect y="760" width="{W}" height="240" fill="{s.lin([(0, "#1a1020", 1), (1, "#0a0610", 1)], 0, 760, 0, 1000, user=True)}"/>')
    plat = "M420 760H1180L1300 900H300Z"
    s.add(f'<path d="{plat}" fill="{s.lin([(0, "#8a6a58", 1), (1, "#c8a888", 1)], 0, 760, 0, 900, user=True)}"/>'
          f'<path d="M300 900H1300V936H300Z" fill="#5a3a30"/><path d="M300 900H1300" stroke="#ffd8a8" stroke-opacity=".6" stroke-width="2"/>'
          f'<path d="M270 936H1330V968H270Z" fill="#3a2422"/><path d="M270 936H1330" stroke="#ffc890" stroke-opacity=".4" stroke-width="2"/>')
    lay_rangoli(s, 800, 842, 270, k=.2, seed=9, shade=.1, opacity=.8)
    # back pillars and the drapes behind
    pillar(s, 560, 330, 768, 24, light_dir=1, seed=2)
    pillar(s, 1040, 330, 768, 24, light_dir=-1, seed=3)
    drape(s, 560, 1040, 334, 40, 4, color="#8a1018", seed=4)
    # the havan kund and its fire
    kund = "M720 800H880L860 832H740Z"
    s.add(f'<path d="M700 790H900L880 806H720Z" fill="#c87a3a"/><path d="{kund}" fill="{s.lin(COPPER, 720, 0, 880, 0, user=True)}"/>'
          f'<path d="M740 832H860L846 852H754Z" fill="{s.lin(COPPER, 740, 0, 860, 0, user=True)}"/>'
          f'<path d="M700 790H900" stroke="#ffe0b0" stroke-width="2" opacity=".8"/>')
    fire(s, 800, 794, 150, 170, seed=5)
    # kalash at the corners and two low seats for the couple
    for x, y, sc in ((470, 790, .26), (1130, 790, .26)):
        kalash(s, x, y, sc, seed=int(x))
    for x in (640, 960):
        s.add(f'<path d="M{x - 52} 850H{x + 52}L{x + 46} 866H{x - 46}Z" fill="#8a1018"/><path d="M{x - 52} 850H{x + 52}" stroke="#f2c04a" stroke-width="3"/>')
    # front pillars, the front drape and canopy
    pillar(s, 360, 230, 912, 34, light_dir=1, seed=5)
    pillar(s, 1240, 230, 912, 34, light_dir=-1, seed=6)
    s.add(f'<path d="M330 214H1270V236H330Z" fill="#e8d8b8"/><path d="M330 214H1270" stroke="#fff4d8" stroke-width="2"/>')
    canopy = "M380 214C520 120 660 70 800 60C940 70 1080 120 1220 214Z"
    s.add(f'<path d="{canopy}" fill="{s.lin([(0, "#e8c890", 1), (0.6, "#b0141e", 1), (1, "#6a0a10", 1)], 0, 60, 0, 214, user=True)}"/>')
    ribs = "".join(f"M800 62Q{f(800 + (x - 800) * .4)} {f(110)} {f(x)} 214" for x in range(380, 1230, 70))
    s.add(f'<path d="{ribs}" stroke="#f2c04a" stroke-opacity=".55" stroke-width="2" fill="none"/>')
    s.add(f'<path d="M790 62L800 20L810 62Z" fill="#f2c04a"/><circle cx="800" cy="42" r="9" fill="#e0a840"/>')
    for side in (-1, 1):
        px = 800 + side * 440
        sheer = (f"M{800 + side * 470} 236C{800 + side * 380} 300 {800 + side * 330} 420 {px + side * 10} 520"
                 f"C{px + side * 40} 600 {px + side * 70} 720 {px + side * 60} 900L{px + side * 90} 900C{px + side * 110} 720 {px + side * 70} 520 {px + side * 30} 480"
                 f"C{800 + side * 470} 380 {800 + side * 480} 300 {800 + side * 470} 236Z")
        s.add(f'<path d="{sheer}" fill="#f6e2c0" opacity=".35"/><path d="{sheer}" fill="none" stroke="#f2c04a" stroke-opacity=".5" stroke-width="2"/>')
        s.add(ob.marigold(px + side * 22, 500, 16, "#f39a1c", 70 + side) + ob.marigold(px + side * 22, 524, 13, "#f7c02a", 72 + side))
    drape(s, 330, 1270, 236, 54, 6, color="#b0141e", seed=7)
    # marigold garlands looping between the front pillars
    ob.garland(s, 360, 300, 800, 300, 40, r=11, seed=3, tassel=False)
    ob.garland(s, 800, 300, 1240, 300, 40, r=11, seed=4, tassel=False)
    s.add("".join(ob.marigold(800, 310 + k * 16, 11, ("#f39a1c", "#f7c02a")[k % 2], 40 + k) for k in range(6)))
    # firelight on everything
    s.add(f'<rect width="{W}" height="{H}" fill="{s.rad([(0, "#ff8a3a", .35), (0.4, "#ff6a2a", .12), (1, "#000", 0)], 800, 720, 700, user=True)}" style="mix-blend-mode:screen"/>')
    s.motes(40, 600, 1000, 380, 760, seed=4, size=(.8, 2))
    s.fx("mottle", amp=.04, cell=60)
    s.look = {"vibrance": .1}
    return s


# ======================================================================
# 8. Namkaran: the cradle in morning light
# ======================================================================
def turned_post(s, x, top, base, w, wood):
    """A lathe-turned wooden post with rings and bulbs."""
    d = [f"M{f(x - w / 2)} {f(top)}H{f(x + w / 2)}V{f(base)}H{f(x - w / 2)}Z"]
    y = top + 40
    while y < base - 60:
        d.append(f"M{f(x - w * .95)} {f(y)}H{f(x + w * .95)}V{f(y + 10)}H{f(x - w * .95)}Z")
        d.append(f"M{f(x)} {f(y + 16)}m{f(-w * .85)} 18a{f(w * .85)} 20 0 1 0 {f(w * 1.7)} 0a{f(w * .85)} 20 0 1 0 {f(-w * 1.7)} 0Z")
        y += 150
    d.append(f"M{f(x - w * 1.5)} {f(base - 20)}H{f(x + w * 1.5)}V{f(base)}H{f(x - w * 1.5)}Z")
    s.add(f'<path d="{"".join(d)}" fill="{wood}"/>')


@scene
def cradle(s):
    # a quiet room: warm plaster wall, a window on the left pouring in morning light
    s.add(f'<rect width="{W}" height="{H}" fill="#d0a47a"/>')
    s.add(f'<rect width="{W}" height="{H}" fill="#d0a47a" filter="{s.grain(0.008, 3, .1, 4, "#5a3a2a")}"/>')
    s.add(f'<rect width="{W}" height="{H}" fill="{s.lin([(0, "#fff0d0", .2), (0.45, "#000", 0), (1, "#3a1a1a", .5)], 0, 0, 1, 0)}"/>')
    s.add(f'<rect width="{W}" height="{H}" fill="{s.lin([(0, "#2a1408", .35), (0.4, "#000", 0)], 0, 0, 0, 800, user=True)}"/>')
    wx0, wx1, wy0, wy1 = 90, 330, 150, 560
    s.add(f'<rect x="{wx0 - 26}" y="{wy0 - 26}" width="{wx1 - wx0 + 52}" height="{wy1 - wy0 + 52}" fill="#5a3418"/>')
    s.add(f'<rect x="{wx0}" y="{wy0}" width="{wx1 - wx0}" height="{wy1 - wy0}" fill="{s.lin([(0, "#ffffff", 1), (0.6, "#fff4d0", 1), (1, "#ffe0a0", 1)], 0, wy0, 0, wy1, user=True)}"/>')
    s.add(f'<path d="M{wx0} {wy0 + 280}Q{wx0 + 60} {wy0 + 200} {wx0 + 140} {wy0 + 250}Q{wx0 + 200} {wy0 + 210} {wx1} {wy0 + 260}V{wy1}H{wx0}Z" fill="#b8d8a0" opacity=".6"/>')
    bars = "".join(f"M{f(wx0 + (wx1 - wx0) * k / 6)} {wy0}V{wy1}" for k in range(1, 6))
    s.add(f'<path d="{bars}" stroke="#3a2010" stroke-width="7"/><path d="M{wx0} {(wy0 + wy1) / 2}H{wx1}" stroke="#3a2010" stroke-width="10"/>')
    s.add(f'<rect x="{wx0 - 40}" y="{wy1 + 26}" width="{wx1 - wx0 + 80}" height="18" fill="#6a4020"/>')
    # floor of polished red oxide
    fy = 780
    s.add(f'<rect y="{fy}" width="{W}" height="{H - fy}" fill="{s.lin([(0, "#7a3a2a", 1), (1, "#3a1810", 1)], 0, fy, 0, 1000, user=True)}"/>')
    s.add(f'<rect y="{fy}" width="{W}" height="6" fill="#4a2418"/>')
    # sunlight on the floor and the far wall
    beam = s.lin([(0, "#fff2d0", .5), (1, "#ffd890", .12)], wx0, wy0, 1100, 1000, user=True)
    s.add(f'<path d="M{wx0} {wy0}L{wx1} {wy0}L1240 {fy + 40}L1180 1000H700L{wx0} {wy1}Z" fill="{beam}" filter="{s.blur(22)}" style="mix-blend-mode:screen"/>')
    s.add(f'<path d="M{wx0 + 470} {fy + 20}L{wx1 + 520} {fy + 10}L{wx1 + 900} 1000H{wx0 + 760}Z" fill="#ffe2b0" opacity=".5" filter="{s.blur(12)}" style="mix-blend-mode:screen"/>')
    # a little kolam under the cradle
    floor_mandala(s, 800, 880, kolam_svg(170, "#f8eedc"), .22, rough=1.2, seed=4, opacity=.7)
    # the stand: two turned posts and a carved crossbar
    wood = s.lin([(0, "#3a1806"), (0.35, "#c0602a"), (0.55, "#e89a50"), (1, "#5a2408")], 0, 0, 1, 0)
    for x in (470, 1130):
        s.add(f'<ellipse cx="{x}" cy="{fy + 112}" rx="70" ry="10" fill="#000" opacity=".4" filter="{s.blur(6)}"/>')
        turned_post(s, x, 250, fy + 110, 30, wood)
    s.add(f'<rect x="420" y="226" width="760" height="34" rx="6" fill="{s.lin([(0, "#e89a50"), (0.4, "#b0501e"), (1, "#4a1c06")], 0, 0, 0, 1)}"/>'
          f'<path d="M430 236H1170" stroke="#ffd890" stroke-opacity=".6" stroke-width="2"/>')
    s.add("".join(f'<circle cx="{x}" cy="243" r="5" fill="#f2c04a"/>' for x in range(450, 1160, 40)))
    s.add(f'<path d="M440 226C520 190 620 200 640 226ZM1160 226C1080 190 980 200 960 226Z" fill="#b0501e"/>')
    # chains down to the cradle
    for x0, x1 in ((640, 600), (960, 1000)):
        s.add(f'<path d="M{x0} 260L{x1} 560" stroke="#c8902e" stroke-width="4" stroke-dasharray="9 4"/>')
    # jasmine and marigold hanging from the crossbar
    rng = random.Random(4)
    strands = []
    for x in range(480, 1130, 38):
        L = rng.randint(3, 6) if abs(x - 800) > 120 else 2
        for j in range(L):
            if j % 2:
                strands.append(ob.marigold(x, 270 + j * 16, 8, ("#f39a1c", "#f7c02a")[j % 2], x + j))
            else:
                strands.append(f'<circle cx="{x}" cy="{270 + j * 16}" r="5.5" fill="#fffaf0"/><circle cx="{x}" cy="{270 + j * 16}" r="2" fill="#f2e6b8"/>')
    s.add("".join(strands))
    ob.garland(s, 470, 300, 1130, 300, 26, r=9, seed=6, tassel=False, colors=("#f39a1c", "#f7c02a"))
    for x in (470, 1130):
        s.add("".join(ob.marigold(x, 320 + k * 20, 11, ("#f39a1c", "#e8562a", "#f7c02a")[k % 3], 9 + k) for k in range(18)))
    # the cradle: a lacquered boat of wood with turned rails and curved ends
    cx, cy = 800, 640
    body = (f"M{cx - 250} {cy - 70}C{cx - 260} {cy - 20} {cx - 230} {cy + 60} {cx - 170} {cy + 70}H{cx + 170}"
            f"C{cx + 230} {cy + 60} {cx + 260} {cy - 20} {cx + 250} {cy - 70}L{cx + 210} {cy - 30}H{cx - 210}Z")
    lac = s.lin([(0, "#ff9a3a", 1), (0.4, "#d8501a", 1), (1, "#6a1a08", 1)], 0, cy - 70, 0, cy + 70, user=True)
    s.add(f'<ellipse cx="{cx}" cy="{fy + 70}" rx="300" ry="26" fill="#000" opacity=".3" filter="{s.blur(16)}"/>')
    # soft bedding inside, seen over the rail
    s.add(f'<path d="M{cx - 205} {cy - 34}Q{cx} {cy - 70} {cx + 205} {cy - 34}V{cy - 10}H{cx - 205}Z" fill="#fff6ea"/>'
          f'<path d="M{cx - 120} {cy - 44}Q{cx - 40} {cy - 78} {cx + 60} {cy - 52}Q{cx + 30} {cy - 34} {cx - 120} {cy - 34}Z" fill="#c0141e"/>'
          f'<path d="M{cx - 120} {cy - 44}Q{cx - 40} {cy - 78} {cx + 60} {cy - 52}" stroke="#f2c04a" stroke-width="3" fill="none"/>')
    s.add(f'<path d="{body}" fill="{lac}"/>')
    rail = "".join(f'<rect x="{f(x - 5)}" y="{cy - 30}" width="10" height="56" rx="5"/>' for x in range(cx - 190, cx + 200, 26))
    s.add(f'<g fill="#3a0e04" opacity=".55">{rail}</g>')
    s.add("".join(f'<ellipse cx="{x}" cy="{cy - 2}" rx="4" ry="9" fill="#f2b84a" opacity=".85"/>' for x in range(cx - 190, cx + 200, 26)))
    s.add(f'<path d="M{cx - 212} {cy - 34}H{cx + 212}" stroke="#f2c04a" stroke-width="5"/><path d="M{cx - 172} {cy + 44}H{cx + 172}" stroke="#f2c04a" stroke-width="4"/>'
          f'<path d="M{cx - 160} {cy + 56}H{cx + 160}" stroke="#2a0a02" stroke-opacity=".5" stroke-width="3"/>')
    motif = "".join(f'<g transform="translate({x} {cy + 26})">' + "".join(f'<path d="{_petal(4, 9)}" transform="rotate({a})"/>' for a in range(0, 360, 60)) + '</g>' for x in range(cx - 150, cx + 160, 50))
    s.add(f'<g fill="#ffd27a" opacity=".8">{motif}</g>')
    for side in (-1, 1):
        ex = cx + side * 250
        s.add(f'<circle cx="{ex}" cy="{cy - 76}" r="16" fill="#f2c04a"/><circle cx="{ex}" cy="{cy - 76}" r="8" fill="#c0501e"/>')
    # a garland swagged along the cradle
    ob.garland(s, cx - 230, cy - 40, cx + 230, cy - 40, 30, r=10, seed=8, tassel=False, colors=("#fffaf0", "#f39a1c"))
    # brass lamp on the floor, petals scattered
    ob.brass_lamp(s, 1330, 950, .62, flames=1, flame_h=38)
    ob.petals_scatter(s, 500, 1150, 830, 990, 34, seed=8, size=(4, 8))
    s.fx("godrays", cx=wx0 + 80, cy=wy0 + 120, strength=.6, thresh=.8, decay=.978, radius=420)
    s.motes(60, 300, 1100, 200, 760, seed=5, size=(.7, 1.6), color="#fff2d0")
    s.fx("mottle", amp=.035, cell=60)
    s.look = {"vibrance": .06, "vignette": .32}
    return s


# ======================================================================
# 9. Mundan: a lock of hair offered on the river at dawn
# ======================================================================
def hair_lock(s, cx, cy, R, seed=1):
    """A child's first hair, gathered into a soft coiled curl with one loose end, bound with red thread."""
    rng = random.Random(seed)
    strands = []
    for k in range(120):
        r = R * (.25 + .75 * rng.random() ** .7)
        a0 = rng.uniform(0, 6.28)
        sweep = rng.uniform(1.6, 3.4)
        pts = []
        for j in range(22):
            a = a0 + sweep * j / 21
            rr = r * (1 + .06 * math.sin(j * .9 + k))
            pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr * .55 - (R - rr) * .25))
        strands.append(pts_d(pts, False))
    # the loose end of the lock curling away to the side
    tail = []
    for k in range(26):
        off = rng.uniform(-1, 1) * R * .12
        pts = []
        for j in range(16):
            u = j / 15
            x = cx + R * .7 + u * R * 1.1
            y = cy + off * (1 - u * .4) + math.sin(u * 3.5 + .5) * R * .22 - u * R * .1
            pts.append((x, y))
        ex, ey = pts[-1]
        for j in range(1, 6):
            a = j * .7
            pts.append((ex + math.sin(a) * R * .16, ey - (1 - math.cos(a)) * R * .16))
        tail.append(pts_d(pts, False))
    tail = [t for i, t in enumerate(tail) if i % 3 == 0][:0]
    d = "".join(strands + tail)
    s.add(f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(R * .9)}" ry="{f(R * .45)}" fill="#0c0604"/>')
    s.add(f'<path d="{d}" stroke="#0c0604" stroke-width="2" fill="none" stroke-linecap="round"/>')
    s.add(f'<path d="{"".join((strands + tail)[::3])}" stroke="#6a4428" stroke-width=".9" fill="none" opacity=".6" transform="translate(0 -1.4)"/>')
    s.add(f'<path d="{"".join(strands[::7])}" stroke="#ffcf9a" stroke-width=".8" fill="none" opacity=".5" transform="translate(-1 -2.4)"/>')
    # red mauli thread bound round it
    for k in range(3):
        x = cx + R * (.55 + k * .09)
        s.add(f'<path d="M{f(x - R * .1)} {f(cy - R * .42)}Q{f(x + R * .08)} {f(cy)} {f(x - R * .02)} {f(cy + R * .4)}" stroke="#d0141e" stroke-width="3.4" fill="none" stroke-linecap="round"/>')
    s.add(f'<path d="M{f(cx + R * .7)} {f(cy + R * .36)}q8 20 28 26M{f(cx + R * .7)} {f(cy + R * .36)}q-6 24 4 36" stroke="#d0141e" stroke-width="2.4" fill="none" stroke-linecap="round"/>')


def leaf_boat(s, cx, cy, w, seed=1):
    """A boat folded from a banana leaf, its upturned ends pinned with slivers of stick."""
    h = w * .2
    outer = (f"M{f(cx - w / 2)} {f(cy - h * 1.3)}C{f(cx - w * .4)} {f(cy + h * .5)} {f(cx - w * .2)} {f(cy + h * .9)} {f(cx)} {f(cy + h * .9)}"
             f"C{f(cx + w * .2)} {f(cy + h * .9)} {f(cx + w * .4)} {f(cy + h * .5)} {f(cx + w / 2)} {f(cy - h * 1.3)}"
             f"C{f(cx + w * .3)} {f(cy - h * .2)} {f(cx - w * .3)} {f(cy - h * .2)} {f(cx - w / 2)} {f(cy - h * 1.3)}Z")
    inner = (f"M{f(cx - w * .44)} {f(cy - h * .95)}C{f(cx - w * .25)} {f(cy - h * .55)} {f(cx + w * .25)} {f(cy - h * .55)} {f(cx + w * .44)} {f(cy - h * .95)}"
             f"C{f(cx + w * .28)} {f(cy - h * .05)} {f(cx - w * .28)} {f(cy - h * .05)} {f(cx - w * .44)} {f(cy - h * .95)}Z")
    g = s.lin([(0, "#4a5a2a", 1), (0.45, "#24361a", 1), (1, "#0a120a", 1)], 0, cy - h, 0, cy + h, user=True)
    s.add(f'<path d="{outer}" fill="{g}"/>')
    veins = "".join(f"M{f(cx + (t - .5) * w * .9)} {f(cy - h * .2)}Q{f(cx + (t - .5) * w * .85)} {f(cy + h * .4)} {f(cx + (t - .5) * w * .7)} {f(cy + h * .8)}" for t in [k / 14 for k in range(1, 14)])
    s.add(f'<g clip-path="{s.clip(outer)}"><path d="{veins}" stroke="#c8d890" stroke-opacity=".14" stroke-width="1.4" fill="none"/></g>')
    s.add(f'<path d="{inner}" fill="{s.lin([(0, "#8a9058", 1), (1, "#3e4a26", 1)], 0, 0, 0, 1)}"/>')
    s.add(f'<path d="M{f(cx - w / 2)} {f(cy - h * 1.3)}C{f(cx - w * .4)} {f(cy + h * .5)} {f(cx - w * .2)} {f(cy + h * .9)} {f(cx)} {f(cy + h * .9)}" stroke="#ffc890" stroke-opacity=".7" stroke-width="2.6" fill="none"/>')
    for side in (-1, 1):
        x = cx + side * w * .43
        s.add(f'<path d="M{f(x - 10)} {f(cy - h * 1.1)}L{f(x + 10)} {f(cy - h * .7)}" stroke="#c8a870" stroke-width="2.4"/>')
    return inner


@scene
def hair_offering(s):
    sun = (560, 548)
    wl = 560
    s.sky([(0, "#1a1e4a"), (.18, "#3a3470"), (.34, "#8a5a8a"), (.44, "#e08a88"), (.5, "#ffb890"), (.56, "#ffe0b8")], 0, 1000)
    s.stars(30, 0, 160, seed=9, bright=.4)
    s.sun(*sun, 30, halo_r=560, halo_a=.8)
    s.fx("clouds", y0=40, y1=300, seed=81, cell=150, aniso=3.4, cover=.4, soft=.18, lit="#ffb8a0", body=.75, direct=.8,
         light=(-.2, 1), sun=(sun[0], sun[1], 420), opacity=.9)
    s.fx("clouds", y0=320, y1=500, seed=82, cell=80, aniso=6, cover=.3, soft=.22, lit="#ffd8b0", body=.85, direct=.95,
         light=(0, 1), sun=(sun[0], sun[1], 340), opacity=.8)
    import arch
    arch.skyline(s, 760, 1680, wl - 2, h=(24, 60), color="#8a5a78", seed=91, windows=0, temples=[(1000, .5), (1400, .42)], chhatris=[(1180, .4)], storey=18)
    arch.steps(s, 760, 1680, wl - 8, wl, 3, color="#7a4a68", edge="#ffb890", edge_a=.4)
    from land import ridgeline, hills
    far = ridgeline(wl, 18, 92, cell=200, octaves=4, ridged=.2, x1=800)
    hills(s, far, "#9a6a88", "#9a6a88")
    s.mist(wl - 4, 40, "#ffd0b0", .6, 10)
    s.fx("reflect", y0=wl, strength=.88, tint="#2a1838", tint_near=.45, tint_far=.06, amp=3)
    s.fx("glints", y0=wl, cx=sun[0], color="#fff0c8", width=46, strength=1.15, scatter=.05, density=.5)
    s.wisps(14, 0, W, wl + 6, wl + 80, "#ffd9c0", a=(.08, .22), length=(260, 700), thick=(6, 18), blur=10, seed=5)
    # distant leaf lamps drifting
    for k, (x, y, sc) in enumerate(((330, 600, .4), (1180, 620, .5), (1420, 680, .7), (220, 700, .8))):
        arch.leaf_lamp(s, x, y, sc, seed=k)
    # ripples spreading round the offering
    cx, cy = 800, 812
    rings = "".join(f'<ellipse cx="{cx + k * 6}" cy="{cy + 22 + k * 3}" rx="{r}" ry="{r * .16}" fill="none" stroke="#ffe0c0" stroke-opacity="{.2 - k * .04:.2f}" stroke-width="{3 - k * .5}"/>' for k, r in enumerate((260, 340, 440)))
    s.add(f'<g filter="{s.blur(2.2)}">{rings}</g>')
    s.add(f'<ellipse cx="{cx}" cy="{cy + 40}" rx="300" ry="40" fill="#000" opacity=".25" filter="{s.blur(14)}"/>')
    m = s.mark()
    leaf_boat(s, cx, cy, 500, seed=2)
    # marigolds, rose petals, the tied lock of hair and a little lamp
    s.add(ob.marigold(cx - 140, cy - 44, 22, "#f39a1c", 1) + ob.marigold(cx - 104, cy - 32, 18, "#f7c02a", 2) + ob.marigold(cx + 160, cy - 42, 20, "#e8562a", 3))
    ob.petals_scatter(s, cx - 150, cx + 150, cy - 56, cy - 30, 26, colors=("#c91e3a", "#e8304a", "#f39a1c"), seed=4, size=(5, 9))
    hair_lock(s, cx - 30, cy - 62, 74, seed=3)
    diya(s, cx + 120, cy - 56, .46, k=.36, flame_h=30, glow_a=.55, seed=2)
    s.add(f'<path d="M{cx - 220} {cy - 58}C{cx - 160} {cy - 30} {cx + 160} {cy - 30} {cx + 220} {cy - 58}" stroke="#ffc890" stroke-opacity=".4" stroke-width="2" fill="none"/>')
    ob.reflect_since(s, m, cy + 30, .3, 3, 180)
    ob.petals_scatter(s, 420, 1200, 880, 980, 9, colors=("#c91e3a", "#f39a1c", "#f7c02a"), seed=6, size=(7, 11))
    s.birds(6, 300, 700, 380, 450, color="#5a3048", s=(5, 9), seed=4, a=.75)
    s.motes(30, 300, 1300, 400, 760, seed=2)
    s.fx("godrays", cx=sun[0], cy=sun[1], strength=.38, thresh=.72, decay=.97, radius=240)
    s.fx("mottle", amp=.04, cell=60)
    return s


# ======================================================================
# 10. Patram, pushpam, phalam, toyam (Gita 9.26)
# ======================================================================
def hibiscus(s, cx, cy, r, tilt=.62, rot=0.0, seed=1, color="#d8102a"):
    """A red hibiscus seen from above at an angle: five broad ruffled petals, a dark eye and the
    long staminal column with its pollen and stigma."""
    rng = random.Random(seed)
    out = [f'<g transform="translate({f(cx)} {f(cy)}) scale(1 {f(tilt)}) rotate({f(rot)})">']
    dark = mix(color, "#3a0008", .55)
    for k in range(5):
        a = 72 * k + rng.uniform(-6, 6)
        w, L = r * .9, r * rng.uniform(.95, 1.05)
        pts = []
        for j in range(25):
            t = j / 24
            ang = math.pi * t
            rr = 1 + .06 * math.sin(t * 22 + k)
            pts.append((math.cos(ang) * w * .55 * rr, -L * .35 - math.sin(ang) * L * .65 * rr))
        d = f"M0 0L{f(pts[0][0])} {f(pts[0][1])}" + "".join(f"L{f(x)} {f(y)}" for x, y in pts[1:]) + "Z"
        g = s.lin([(0, dark, 1), (0.28, color, 1), (0.8, mix(color, "#ff6a6a", .25), 1), (1, mix(color, "#ff9a8a", .3), 1)], 0, 0, 0, -L, user=True)
        out.append(f'<g transform="rotate({f(a)})"><path d="{d}" fill="{g}" stroke="{dark}" stroke-opacity=".35" stroke-width="1"/>'
                   + "".join(f'<path d="M0 {f(-r * .1)}Q{f(dx * r * .2)} {f(-L * .5)} {f(dx * r * .3)} {f(-L * .9)}" stroke="{dark}" stroke-opacity=".25" stroke-width="1" fill="none"/>' for dx in (-1, -.4, .4, 1))
                   + '</g>')
    out.append(f'<circle r="{f(r * .22)}" fill="{dark}" opacity=".9" filter="{s.blur(r * .06)}"/>')
    out.append('</g>')
    s.add("".join(out))
    # the staminal column standing up out of the flower
    a = math.radians(rot - 60)
    tx, ty = cx + math.cos(a) * r * .55, cy - r * .62
    s.add(f'<path d="M{f(cx)} {f(cy)}Q{f(cx + (tx - cx) * .4)} {f(cy - r * .4)} {f(tx)} {f(ty)}" stroke="{mix(color, "#ff8a8a", .2)}" stroke-width="{f(r * .05)}" fill="none" stroke-linecap="round"/>')
    pol = "".join(f'<circle cx="{f(cx + (tx - cx) * t + rng.uniform(-6, 6) * r / 80)}" cy="{f(cy + (ty - cy) * t + rng.uniform(-4, 4) * r / 80)}" r="{f(r * .025)}" fill="#ffd23a"/>' for t in [.55 + .4 * rng.random() for _ in range(22)])
    s.add(pol + "".join(f'<circle cx="{f(tx + math.cos(b) * r * .05)}" cy="{f(ty - r * .04 + math.sin(b) * r * .03)}" r="{f(r * .03)}" fill="#a0001a"/>' for b in (0, 1.25, 2.5, 3.75, 5)))


def mango(s, cx, cy, sc=1.0, rot=-10):
    """A ripe mango with a red blush where the light falls, and its stalk."""
    t = f"translate({f(cx)} {f(cy)}) rotate({f(rot)}) scale({f(sc)})"
    body = "M-62 6C-64 -34 -22 -50 14 -46C52 -42 70 -16 64 12C58 40 20 50 -14 46C-44 42 -60 30 -62 6Z"
    g = s.rad([(0, "#ffe27a", 1), (0.45, "#ffb02a", 1), (0.85, "#d8641a", 1), (1, "#8a3a0a", 1)], .38, .32, .75)
    blush = s.rad([(0, "#e8302a", .75), (1, "#e8302a", 0)], .25, .3, .45)
    s.add(f'<g transform="{t}"><ellipse cx="10" cy="52" rx="64" ry="10" fill="#000" opacity=".3" filter="{s.blur(6)}"/>'
          f'<path d="{body}" fill="{g}"/><path d="{body}" fill="{blush}"/>'
          f'<path d="{body}" fill="{s.lin([(0, "#fff", 0), (0.6, "#000", 0), (1, "#000", .35)], 0, 0, .3, 1)}"/>'
          f'<ellipse cx="-26" cy="-22" rx="14" ry="7" fill="#fff8d8" opacity=".55" transform="rotate(-25 -26 -22)" filter="{s.blur(3)}"/>'
          f'<path d="M14 -46Q18 -60 26 -66" stroke="#4a3010" stroke-width="5" fill="none" stroke-linecap="round"/>'
          f'<path d="M24 -64C40 -86 80 -84 96 -70C76 -60 44 -56 24 -64Z" fill="{s.lin([(0, "#3a7a2a", 1), (1, "#1a3a14", 1)], 0, 0, 1, 1)}"/>'
          f'<path d="M24 -64C50 -70 76 -72 96 -70" stroke="#a8d080" stroke-opacity=".5" stroke-width="1.4" fill="none"/></g>')


def lota(s, cx, base, sc=1.0, metal=COPPER, water=True):
    """A small round copper pot (lota) of water."""
    g = s.lin(metal, cx - 70 * sc, 0, cx + 70 * sc, 0, user=True)
    belly = (f"M{f(cx - 26 * sc)} {f(base - 92 * sc)}C{f(cx - 84 * sc)} {f(base - 84 * sc)} {f(cx - 84 * sc)} {f(base - 4 * sc)} {f(cx - 30 * sc)} {f(base)}"
             f"H{f(cx + 30 * sc)}C{f(cx + 84 * sc)} {f(base - 4 * sc)} {f(cx + 84 * sc)} {f(base - 84 * sc)} {f(cx + 26 * sc)} {f(base - 92 * sc)}Z")
    neck = f"M{f(cx - 26 * sc)} {f(base - 90 * sc)}L{f(cx - 22 * sc)} {f(base - 112 * sc)}H{f(cx + 22 * sc)}L{f(cx + 26 * sc)} {f(base - 90 * sc)}Z"
    rim = f"M{f(cx - 40 * sc)} {f(base - 122 * sc)}Q{f(cx)} {f(base - 112 * sc)} {f(cx + 40 * sc)} {f(base - 122 * sc)}L{f(cx + 30 * sc)} {f(base - 110 * sc)}Q{f(cx)} {f(base - 104 * sc)} {f(cx - 30 * sc)} {f(base - 110 * sc)}Z"
    s.add(f'<path d="{belly}" fill="{g}"/><path d="{neck}" fill="{g}"/>'
          f'<path d="{belly}" fill="{s.lin([(0, "#fff", 0), (0.55, "#000", 0), (1, "#000", .45)], 0, base - 92 * sc, 0, base, user=True)}"/>'
          f'<path d="M{f(cx - 64 * sc)} {f(base - 46 * sc)}Q{f(cx)} {f(base - 32 * sc)} {f(cx + 64 * sc)} {f(base - 46 * sc)}" stroke="#ffd8a8" stroke-opacity=".35" stroke-width="{f(2 * sc)}" fill="none"/>'
          f'<path d="{rim}" fill="{g}"/>'
          f'<ellipse cx="{f(cx)}" cy="{f(base - 119 * sc)}" rx="{f(34 * sc)}" ry="{f(7 * sc)}" fill="#3a1408"/>')
    if water:
        s.add(f'<ellipse cx="{f(cx)}" cy="{f(base - 118 * sc)}" rx="{f(28 * sc)}" ry="{f(5 * sc)}" fill="{s.lin([(0, "#ffe8c8", .9), (1, "#7a5a50", .9)], 0, 0, 1, 0)}"/>'
              f'<ellipse cx="{f(cx - 8 * sc)}" cy="{f(base - 119 * sc)}" rx="{f(8 * sc)}" ry="{f(1.6 * sc)}" fill="#ffffff" opacity=".8"/>')


@scene
def leaf_flower_fruit(s):
    light = (150, 40)
    # a temple courtyard behind, softly out of focus, morning sun from the upper left
    s.add(f'<rect width="{W}" height="{H}" fill="{s.lin([(0, "#e8c89a", 1), (0.5, "#b08a6a", 1), (1, "#5a4038", 1)], 0, 0, 1, .7)}"/>')
    m = s.mark()
    s.add(f'<rect x="0" y="0" width="{W}" height="640" fill="{s.lin([(0, "#f4dcb0", 1), (1, "#a07a5a", 1)], 0, 0, 1, .3)}"/>')
    s.add(f'<rect x="40" y="0" width="300" height="200" fill="#fffaf0"/>')
    for x, w in ((560, 90), (980, 90), (1400, 110)):
        s.add(f'<rect x="{x}" y="0" width="{w}" height="640" fill="{s.lin([(0, "#6a4a3a", 1), (0.4, "#c8a07a", 1), (1, "#4a3028", 1)], 0, 0, 1, 0)}"/>'
              f'<rect x="{x - 14}" y="120" width="{w + 28}" height="26" fill="#5a3a2a"/><rect x="{x - 14}" y="520" width="{w + 28}" height="30" fill="#5a3a2a"/>')
    s.add(f'<path d="M1100 640V300C1100 230 1290 230 1290 300V640Z" fill="#2a160e"/>'
          f'<path d="M1130 640V320C1130 270 1260 270 1260 320V640Z" fill="{s.rad([(0, "#ffd890", 1), (0.5, "#e88a3a", 1), (1, "#4a1a0a", 1)], 1195, 520, 160, user=True)}"/>')
    for x in (1170, 1220):
        s.add(f'<circle cx="{x}" cy="520" r="10" fill="#fff4c0"/>')
    s.add(f'<rect x="0" y="0" width="{W}" height="140" fill="#4a3022" opacity=".6"/>')
    s.add(ob.marigold(200, 470, 40, "#f39a1c", 3) + ob.marigold(260, 520, 34, "#f7c02a", 4))
    s.wrap(m, s.uid("bg"))
    s.body[-1] = s.body[-1].replace('<g id=', f'<g filter="{s.blur(9)}" id=', 1)
    s.bokeh(10, 900, 1600, 200, 560, colors=("#ffd890", "#ffb060"), r=(18, 40), a=(.15, .35), blur=4, seed=5)
    # the step: lit top, dark riser
    top, edge = 520, 880
    s.add(f'<path d="M-20 {top}H1620V{edge}H-20Z" fill="{s.lin([(0, "#7a6458", 1), (1, "#c8aa94", 1)], 0, top, 0, edge, user=True)}"/>'
          f'<path d="M-20 {top}H1620V{edge}H-20Z" fill="#a08070" filter="{s.grain(0.03, 3, .14, 4, "#2a1a14")}"/>'
          f'<rect x="-20" y="{edge}" width="1640" height="{H - edge}" fill="{s.lin([(0, "#5a443c", 1), (1, "#22160f", 1)], 0, edge, 0, 1000, user=True)}"/>'
          f'<path d="M-20 {edge}H1620" stroke="#ffe8c8" stroke-opacity=".7" stroke-width="3"/>')
    s.add(f'<path d="M-20 {top}H1620V{edge}H-20Z" fill="{s.rad([(0, "#fff0d0", .55), (1, "#fff0d0", 0)], 380, 600, 900, user=True)}" style="mix-blend-mode:screen"/>')
    s.add(f'<path d="M-20 {top}H1620V{top + 40}H-20Z" fill="#2a1a12" opacity=".35" filter="{s.blur(14)}"/>')
    # the banana leaf, laid along the step
    ctr = [(230, 716), (520, 706), (820, 698), (1120, 694), (1400, 690)]
    spine = smooth_line(ctr, 8)
    up, dn = [], []
    n = len(spine)
    for i, (x, y) in enumerate(spine):
        t = i / (n - 1)
        hw = 118 * (math.sin(min(1, t * 2.2 + .04) * math.pi / 2) ** .5)
        up.append((x, y - hw * .8))
        dn.append((x, y + hw * .9))
    leaf_d = pts_d(up + dn[::-1])
    s.add(f'<path d="{pts_d([(x + 40, y + 26) for x, y in up + dn[::-1]])}" fill="#1a0e08" opacity=".5" filter="{s.blur(14)}"/>')
    s.add(f'<path d="{leaf_d}" fill="{s.lin([(0, "#86b84a", 1), (0.5, "#3e7e28", 1), (1, "#1a4416", 1)], 0, 600, 0, 810, user=True)}"/>')
    veins = []
    for i in range(3, n - 1, 2):
        x, y = spine[i]
        veins.append(f"M{f(x)} {f(y)}L{f(x + 46)} {f(up[i][1] + 2)}M{f(x)} {f(y)}L{f(x + 40)} {f(dn[i][1] - 2)}")
    s.add(f'<g clip-path="{s.clip(leaf_d)}"><path d="{"".join(veins)}" stroke="#c8e890" stroke-opacity=".2" stroke-width="1.4"/>'
          f'<path d="{pts_d(spine, False)}" stroke="#e0f4b0" stroke-opacity=".7" stroke-width="8" fill="none"/>'
          f'<path d="{pts_d([(x, y - 50) for x, y in spine], False)}" stroke="#ffffff" stroke-opacity=".2" stroke-width="26" fill="none" filter="{s.blur(10)}"/>'
          f'<path d="{pts_d(dn, False)}" stroke="#0a2008" stroke-opacity=".5" stroke-width="10" fill="none" filter="{s.blur(4)}"/></g>')
    s.add("".join(f'<path d="M{f(up[i][0])} {f(up[i][1] - 1)}L{f(up[i][0] + 34)} {f(up[i][1] + 30)}" stroke="#9a7c68" stroke-width="3"/>' for i in (34, 80, 132)))
    # the offering: flower, fruit and water
    ob.petals_scatter(s, 300, 1150, 650, 760, 12, colors=("#fff6e8",), seed=3, size=(5, 8))
    tul = "".join(mango_leaf(x, y, 40, 20, a, "#1f4a1e", "#4a8a3a", None, s) for x, y, a in ((360, 700, -60), (378, 708, 20), (402, 702, 70)))
    s.add(tul)
    s.add(f'<ellipse cx="640" cy="760" rx="150" ry="22" fill="#0a1a08" opacity=".45" filter="{s.blur(10)}" transform="translate(30 0)"/>')
    hibiscus(s, 600, 700, 148, tilt=.6, rot=12, seed=4)
    mango(s, 940, 680, 2.0, rot=-8)
    s.add(f'<ellipse cx="1290" cy="{top + 260}" rx="150" ry="22" fill="#1a0e08" opacity=".5" filter="{s.blur(12)}" transform="translate(50 6)"/>')
    lota(s, 1270, top + 262, 1.9)
    s.add("".join(f'<ellipse cx="{x}" cy="{y}" rx="7" ry="4" fill="#e8f8f0" opacity=".55"/><ellipse cx="{x - 2}" cy="{y - 1.4}" rx="2.4" ry="1.3" fill="#fff"/>' for x, y in ((1110, 700), (1140, 722), (800, 744), (1180, 690), (420, 730))))
    s.fx("godrays", cx=light[0], cy=light[1], strength=.5, thresh=.74, decay=.975, radius=520)
    s.motes(30, 200, 1100, 100, 600, seed=4, size=(.7, 1.6), color="#fff0d0")
    s.fx("mottle", amp=.035, cell=60)
    s.look = {"vibrance": .1, "vignette": .3}
    return s


# ======================================================================
# 11. The home shrine
# ======================================================================
@scene
def shrine(s):
    ob.dark_room(s, light=(800, 520), base="#0e0705", warm="#4a220e", r=1000, horizon=820, floor="#140906")
    s.bokeh(10, 0, 1600, 80, 700, colors=("#ff9a3a", "#ffc070"), r=(24, 60), a=(.06, .16), blur=6, seed=3)
    s.glow(800, 520, 700, "#ff8a3a", .25, .2)
    ob.ledge(s, 820, color="#3a2418", edge="#ffc890", depth=70)
    wood = s.lin([(0, "#2a1004"), (0.2, "#6a3410"), (0.5, "#a8602a"), (0.8, "#6a3410"), (1, "#2a1004")], 0, 0, 1, 0)
    dark = "#3a1806"
    x0, x1 = 548, 1052
    # base with carved drawer panels
    s.add(f'<rect x="{x0 - 30}" y="704" width="{x1 - x0 + 60}" height="104" fill="{wood}"/>'
          f'<rect x="{x0 - 40}" y="694" width="{x1 - x0 + 80}" height="16" fill="#8a4a1a"/><rect x="{x0 - 40}" y="694" width="{x1 - x0 + 80}" height="3" fill="#ffd090" opacity=".6"/>'
          f'<rect x="{x0 - 40}" y="800" width="{x1 - x0 + 80}" height="14" fill="#5a2a0c"/>')
    for k in range(3):
        px = x0 + 6 + k * (x1 - x0 - 12) / 3
        pw = (x1 - x0 - 12) / 3 - 14
        s.add(f'<rect x="{f(px + 7)}" y="722" width="{f(pw)}" height="64" fill="none" stroke="#e0a050" stroke-opacity=".5" stroke-width="2"/>'
              f'<circle cx="{f(px + 7 + pw / 2)}" cy="754" r="6" fill="#f2c04a"/>')
    # the sanctum: a deep glowing recess, a draped cloth behind
    top, bot = 360, 694
    s.add(f'<rect x="{x0}" y="{top}" width="{x1 - x0}" height="{bot - top}" fill="{dark}"/>')
    inner = _arch_d(x0 + 50, x1 - 50, top + 30, bot)
    glow = s.rad([(0, "#fff2c8", 1), (0.3, "#ffc070", 1), (0.7, "#c0501a", 1), (1, "#4a1806", 1)], 800, 560, 300, user=True)
    s.add(f'<path d="{inner}" fill="{glow}"/>')
    cid = s.clip(inner)
    folds = "".join(f'<path d="M{x} {top}Q{x + 10} {(top + bot) / 2} {x - 6} {bot}" stroke="#7a0a10" stroke-opacity=".35" stroke-width="10" fill="none"/>' for x in range(x0 + 70, x1 - 50, 34))
    s.add(f'<g clip-path="{cid}"><rect x="{x0}" y="{top}" width="{x1 - x0}" height="{bot - top}" fill="#c0201e" opacity=".55" style="mix-blend-mode:multiply"/>{folds}'
          f'<path d="M{x0} {top + 40}Q800 {top + 150} {x1} {top + 40}V{top}H{x0}Z" fill="#a0141a"/>'
          f'<path d="M{x0} {top + 40}Q800 {top + 150} {x1} {top + 40}" stroke="#f2c04a" stroke-width="4" fill="none"/>'
          f'<ellipse cx="800" cy="560" rx="200" ry="170" fill="{s.rad([(0, "#fff8e0", .85), (1, "#ffd890", 0)], .5, .5, .5)}" style="mix-blend-mode:screen"/></g>')
    # a low seat strewn with flowers, a lamp burning before it
    s.add(f'<path d="M700 664H900L884 694H716Z" fill="#7a3a12"/><path d="M690 652H910V666H690Z" fill="#c8862a"/><path d="M690 652H910" stroke="#fff0b0" stroke-width="2" opacity=".7"/>')
    flowers = "".join(ob.marigold(720 + k * 20, 646 - (k % 2) * 5, 11, ("#f39a1c", "#f7c02a", "#e8562a")[k % 3], k) for k in range(9))
    s.add(flowers)
    s.add(ob.marigold(780, 630, 12, "#f7c02a", 31) + ob.marigold(820, 630, 12, "#f39a1c", 32) + ob.marigold(800, 616, 12, "#e8562a", 33))
    ob.bells(s, [660, 940], top + 40, color="#e0a840", blur=1.2, sc=.55, seed=2)
    # pillars and the carved arch frame
    for px in (x0 + 22, x1 - 22):
        s.add(f'<rect x="{px - 16}" y="{top}" width="32" height="{bot - top}" fill="{s.lin([(0, "#3a1804"), (0.5, "#c07a3a"), (1, "#3a1804")], 0, 0, 1, 0)}"/>'
              + "".join(f'<rect x="{px - 20}" y="{y}" width="40" height="10" rx="4" fill="#d89a4a"/>' for y in (top + 40, top + 150, bot - 60)))
    s.add(f'<path d="{inner}" fill="none" stroke="#e0a050" stroke-width="6"/><path d="{inner}" fill="none" stroke="#3a1404" stroke-width="2" transform="translate(0 6)" opacity=".5"/>')
    # cornice, the dome and its finial, corner domes
    s.add(f'<rect x="{x0 - 30}" y="{top - 30}" width="{x1 - x0 + 60}" height="34" fill="{wood}"/>'
          f'<rect x="{x0 - 40}" y="{top - 42}" width="{x1 - x0 + 80}" height="14" fill="#8a4a1a"/><rect x="{x0 - 40}" y="{top - 42}" width="{x1 - x0 + 80}" height="3" fill="#ffd090" opacity=".55"/>')
    s.add("".join(f'<rect x="{x}" y="{top - 26}" width="8" height="20" fill="#2a1004" opacity=".45"/>' for x in range(x0 - 20, x1 + 30, 22)))
    dome = f"M{x0 + 40} {top - 42}C{x0 + 60} {top - 200} {740} {top - 250} 800 {top - 300}C{860} {top - 250} {x1 - 60} {top - 200} {x1 - 40} {top - 42}Z"
    s.add(f'<path d="{dome}" fill="{s.lin([(0, "#2a1004"), (0.35, "#8a4a1a"), (0.55, "#c8803a"), (1, "#2a1004")], 0, 0, 1, 0)}"/>')
    ribs = "".join(f'<path d="M{f(800 + (x - 800) * .05)} {top - 296}Q{f(800 + (x - 800) * .9)} {top - 200} {x} {top - 44}" stroke="#2a1004" stroke-opacity=".45" stroke-width="3" fill="none"/>' for x in range(x0 + 70, x1 - 40, 46))
    s.add(ribs)
    s.add(f'<ellipse cx="800" cy="{top - 304}" rx="30" ry="9" fill="#c8862a"/><path d="M786 {top - 310}C784 {top - 340} 816 {top - 340} 814 {top - 310}Z" fill="#e0a840"/>'
          f'<path d="M796 {top - 336}L800 {top - 360}L804 {top - 336}Z" fill="#f2c04a"/>')
    for cxd in (x0 + 4, x1 - 4):
        s.add(f'<path d="M{cxd - 34} {top - 42}C{cxd - 34} {top - 100} {cxd} {top - 110} {cxd} {top - 128}C{cxd} {top - 110} {cxd + 34} {top - 100} {cxd + 34} {top - 42}Z" fill="{s.lin([(0, "#3a1804"), (0.5, "#b0682a"), (1, "#3a1804")], 0, 0, 1, 0)}"/>')
    # garland swagged across the opening and hanging down the pillars
    ob.garland(s, x0 + 24, top + 30, x1 - 24, top + 30, 34, r=10, seed=5, tassel=False)
    for px in (x0 + 22, x1 - 22):
        s.add("".join(ob.marigold(px, top + 40 + k * 18, 10, ("#f39a1c", "#f7c02a", "#e8562a")[k % 3], 50 + k) for k in range(16)))
    # on the ledge: a brass lamp, a bell, incense smoke and petals
    s.add(f'<rect width="{W}" height="{H}" fill="{s.rad([(0, "#ffb060", .2), (1, "#000", 0)], 800, 600, 500, user=True)}" style="mix-blend-mode:screen"/>')
    diya(s, 800, 790, .8, k=.3, clay="#b88a2a", flame_h=48, glow_a=.6, dots=False)
    bx, by = 420, 800
    s.add(f'<g transform="translate({bx} {by})"><ellipse cx="0" cy="4" rx="46" ry="8" fill="#000" opacity=".5" filter="{s.blur(5)}"/>'
          f'<path d="M-40 0C-36 -40 -22 -70 0 -72C22 -70 36 -40 40 0Z" fill="{s.lin(ob.BRASS, -40, 0, 40, 0, user=True)}"/>'
          f'<path d="M-6 -72V-118H6V-72Z" fill="{s.lin(ob.BRASS, -6, 0, 6, 0, user=True)}"/>'
          f'<path d="M0 -118C-12 -128 -14 -146 0 -160C14 -146 12 -128 0 -118Z" fill="{s.lin(ob.BRASS, -14, 0, 14, 0, user=True)}"/>'
          f'<ellipse cx="0" cy="0" rx="40" ry="6" fill="#5a3a10"/></g>')
    s.add(f'<path d="M1176 800L1196 560" stroke="#3a1a0a" stroke-width="3"/><ellipse cx="1176" cy="802" rx="24" ry="6" fill="#4a2a10"/>'
          f'<path d="M1176 800L1196 560" stroke="#7a4a2a" stroke-width="1.2"/><circle cx="1196" cy="560" r="3.4" fill="#ff8a3a"/>')
    s.glow(1196, 560, 22, "#ff9a4a", .9, .3)
    s.smoke(1196, 556, 420, color="#f3e6d6", a=.45, seed=6, width=1.5, drift=-.15)
    ob.petals_scatter(s, 500, 1100, 790, 812, 24, seed=6, size=(4, 8))
    s.add(f'<g filter="{s.blur(10)}">' + ob.marigold(150, 950, 70, "#f39a1c", 4) + ob.marigold(1480, 960, 60, "#e8562a", 5) + '</g>')
    s.motes(26, 560, 1040, 200, 680, seed=5, size=(.7, 1.6))
    s.fx("mottle", amp=.035, cell=50)
    s.look = {"vibrance": .08}
    return s
