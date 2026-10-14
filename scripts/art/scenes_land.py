from scenes import scene

# Landscape, water and temple paintings: the lotus, rivers and the sun, the avatars of the
# ocean, the great temples and the banyan. Helpers that only these scenes need live here too,
# including two raster effects registered with fx: "sea" (a wind-driven sea) and "foliage".

import math
import random

import numpy as np
from scipy import ndimage

import arch
import fx
import objects as ob
from land import crown, grass, hills, mountains, peak_line, pines, ribbon, ridgeline, smooth_line, y_at
from paint import H, W, f, mix, pts_d


# =====================================================================================
# small geometry helpers
# =====================================================================================
def _poly(pts):
    return pts_d(pts)


def _lerp(a, b, t):
    return a + (b - a) * t


def _norm(v):
    L = math.sqrt(sum(c * c for c in v)) or 1
    return tuple(c / L for c in v)


# =====================================================================================
# a lotus modelled in 3D: petals placed around an axis and projected for the camera
# =====================================================================================
class _Cam:
    def __init__(self, cx, cy, sc, elev=18):
        self.cx, self.cy, self.sc = cx, cy, sc
        self.ce, self.se = math.cos(math.radians(elev)), math.sin(math.radians(elev))

    def p(self, x, y, z):
        """3D (y up, z towards the viewer) to screen."""
        return (self.cx + x * self.sc, self.cy + (-y * self.ce + z * self.se) * self.sc)

    def depth(self, x, y, z):
        return z * self.ce + y * self.se


def _petal3d(cam, phi, tilt0, tilt1, L, Wd, r0=6, cup=0.45, droop=0.0, n=18):
    """Outline (screen points), midline and frame of one cupped, spoon-shaped petal.
    tilt0 is the angle from vertical at the base, tilt1 at the tip (smaller = curls in)."""
    cp, sp = math.cos(phi), math.sin(phi)
    T = (-sp, 0.0, cp)
    left, right, mid = [], [], []
    x, y, z = r0 * cp, 0.0, r0 * sp
    centre = []
    for k in range(n + 1):
        s = k / n
        centre.append((x, y, z, s))
        th = math.radians(_lerp(tilt0, tilt1, s ** 1.2) + droop * s * s)
        D = (math.sin(th) * cp, math.cos(th), math.sin(th) * sp)
        x, y, z = x + D[0] * L / n, y + D[1] * L / n, z + D[2] * L / n
    for (x, y, z, s) in centre:
        th = math.radians(_lerp(tilt0, tilt1, s ** 1.2) + droop * s * s)
        N = (math.cos(th) * cp, -math.sin(th), math.cos(th) * sp)  # outward normal
        # broad obovate petal: narrow claw, widest past the middle, rounded tip with a small point
        if s < .6:
            w = (s / .6) ** .55
        else:
            w = math.sqrt(max(0.0, 1 - ((s - .6) / .42) ** 2))
        w = Wd / 2 * w * (.25 + .75 * min(1, s * 4) if s < .25 else 1)
        e = w * cup
        lp = (x + T[0] * w - N[0] * e, y + T[1] * w - N[1] * e, z + T[2] * w - N[2] * e)
        rp = (x - T[0] * w - N[0] * e, y - T[1] * w - N[1] * e, z - T[2] * w - N[2] * e)
        left.append(cam.p(*lp))
        right.append(cam.p(*rp))
        mid.append(cam.p(x, y, z))
    tip = mid[-1]
    outline = left + [tip] + right[::-1]
    cmid = centre[len(centre) // 2]
    th = math.radians(_lerp(tilt0, tilt1, .5))
    normal = (math.cos(th) * cp, -math.sin(th), math.cos(th) * sp)
    return outline, mid, left, right, cam.depth(cmid[0], cmid[1], cmid[2]), normal


def lotus3d(s, cx, cy, sc=1.0, elev=16, seed=1, tip="#de3f7c", mid_c="#f4a3c2", base="#fff8f2", sun_x=1.0,
            rim="#fff3dc", rim_a=0.7, shadow="#6e1442", veins=True, glow="#ffd6e4", glow_a=0.4, pod=True, open_=1.0):
    """A sacred lotus in full bloom, modelled in 3D; (cx, cy) is where the flower sits on its
    stem. sc=1 gives a flower about 320 px across. sun_x > 0 lights it from the right."""
    rng = random.Random(seed)
    cam = _Cam(cx, cy, sc, elev)
    # rows from outermost to innermost: (count, tilt0, tilt1, length, width, cup, droop, offset)
    rows = [
        (6, 96, 84, 128, 86, .32, 12, .2),
        (7, 74, 56, 134, 90, .42, 2, .65),
        (7, 54, 32, 132, 88, .52, 0, .15),
        (6, 34, 14, 120, 80, .6, -4, .5),
        (5, 18, 2, 100, 66, .66, -6, .85),
    ]
    petals = []
    for ri, (n, t0, t1, L, Wd, cup, dr, off) in enumerate(rows):
        for k in range(n):
            phi = 2 * math.pi * (k + off) / n + rng.uniform(-.1, .1)
            o, m, le, rt, dep, nrm = _petal3d(cam, phi, (t0 + rng.uniform(-4, 4)) * open_, (t1 + rng.uniform(-4, 4)) * open_,
                                               L * rng.uniform(.94, 1.05), Wd * rng.uniform(.92, 1.06), r0=14 - ri * 1.5,
                                               cup=cup, droop=dr)
            petals.append((dep, ri, phi, o, m, le, rt, nrm))
    petals.sort(key=lambda p: p[0])
    out = ['<g>']
    if glow:
        gx, gy = cam.p(0, 60, 0)
        out.append(f'<ellipse cx="{f(gx)}" cy="{f(gy)}" rx="{f(280 * sc)}" ry="{f(210 * sc)}" fill="{s.rad([(0, glow, glow_a), (.5, glow, glow_a * .4), (1, glow, 0)])}" style="mix-blend-mode:screen"/>')
    rim_g = s.lin([(0, rim, rim_a * .25), (.5, rim, rim_a * .5), (1, rim, rim_a)], cx - 200 * sc * sun_x, 0, cx + 200 * sc * sun_x, 0, user=True)
    pod_drawn = False

    def pod_svg():
        res = []
        top_y = 40
        st, st2 = [], []
        for k in range(90):
            a = 2 * math.pi * k / 90 + rng.uniform(-.03, .03)
            r1, r2 = 18, 33 + rng.uniform(-4, 7)
            h1, h2 = top_y - 4, top_y - 16 + rng.uniform(-5, 7)
            p1 = cam.p(math.cos(a) * r1, h1, math.sin(a) * r1)
            p2 = cam.p(math.cos(a) * r2, h2, math.sin(a) * r2)
            (st if math.sin(a) < 0 else st2).append((p1, p2))

        def strokes(lst):
            return "".join(f"M{f(a[0])} {f(a[1])}L{f(b[0])} {f(b[1])}" for a, b in lst)

        def tips(lst):
            return "".join(f'<ellipse cx="{f(b[0])}" cy="{f(b[1])}" rx="{f(1.6 * sc)}" ry="{f(2.6 * sc)}"/>' for a, b in lst)
        res.append(f'<path d="{strokes(st)}" stroke="#d99a2a" stroke-width="{f(1.8 * sc)}" stroke-linecap="round"/>'
                   f'<g fill="#ffe89a">{tips(st)}</g>')
        c = cam.p(0, top_y, 0)
        rx, ry = 21 * sc, 21 * sc * cam.se * 1.2
        bx, by = cam.p(0, 14, 0)
        side = s.lin([(0, "#a8b048", 1), (.55, "#e2e690", 1), (1, "#7c8a2a", 1)], 0, 0, 1, 0)
        res.append(f'<path d="M{f(c[0] - rx)} {f(c[1])}L{f(bx - 8 * sc)} {f(by)}Q{f(bx)} {f(by + 5 * sc)} {f(bx + 8 * sc)} {f(by)}L{f(c[0] + rx)} {f(c[1])}Z" fill="{side}"/>')
        topg = s.rad([(0, "#f7f6c0", 1), (.7, "#dbe080", 1), (1, "#a9b04a", 1)], .55, .4, .7)
        res.append(f'<ellipse cx="{f(c[0])}" cy="{f(c[1])}" rx="{f(rx)}" ry="{f(ry)}" fill="{topg}"/>')
        holes = []
        for k in range(15):
            if k < 9:
                a, r = 2 * math.pi * k / 9, 13
            elif k < 14:
                a, r = 2 * math.pi * k / 5 + .3, 6
            else:
                a, r = 0, 0
            hx, hy = c[0] + math.cos(a) * r * sc, c[1] + math.sin(a) * r * sc * cam.se * 1.2
            holes.append(f'<ellipse cx="{f(hx)}" cy="{f(hy)}" rx="{f(2.4 * sc)}" ry="{f(2.4 * sc * cam.se * 1.6)}"/>')
        res.append(f'<g fill="#6d7a22" opacity=".7">{"".join(holes)}</g>')
        res.append(f'<path d="{strokes(st2)}" stroke="#eab040" stroke-width="{f(1.8 * sc)}" stroke-linecap="round"/>'
                   f'<g fill="#fff4b8">{tips(st2)}</g>')
        res.append(f'<ellipse cx="{f(c[0])}" cy="{f(c[1] - 4 * sc)}" rx="{f(46 * sc)}" ry="{f(26 * sc)}" fill="{s.rad([(0, "#ffe9a0", .5), (1, "#ffe9a0", 0)])}" style="mix-blend-mode:screen"/>')
        return "".join(res)

    for dep, ri, phi, o, m, le, rt, nrm in petals:
        if pod and not pod_drawn and dep > 0 and ri >= 3:
            out.append(pod_svg())
            pod_drawn = True
        facing = nrm[2] * cam.ce + nrm[1] * cam.se  # >0: we see the outside of the petal
        inner = facing < 0
        b, t = m[0], m[-1]
        d = _poly(o)
        # contact shadow on whatever lies behind
        out.append(f'<path d="{d}" fill="{shadow}" opacity=".22" filter="{s.blur(3.5 * sc)}" transform="translate({f(-2 * sc * sun_x)} {f(2 * sc)})"/>')
        if inner:   # inside of the cup, lit through the petals: pale and glowing
            stops = [(0, "#fff3d0", 1), (.3, base, 1), (.62, mix(mid_c, base, .45), 1), (.9, mix(tip, mid_c, .35), 1), (1, mix(tip, "#ffffff", .2), 1)]
        else:       # outside, turned from the sun: richer colour
            stops = [(0, mix(base, "#d9e0a0", .35), 1), (.25, base, 1), (.6, mid_c, 1), (.88, tip, 1), (1, mix(tip, "#ffffff", .12), 1)]
        g = s.lin(stops, b[0], b[1], t[0], t[1], user=True)
        out.append(f'<path d="{d}" fill="{g}"/>')
        # shading across the petal: the edge turned from the sun is darker
        a1, a2 = le[len(le) // 2], rt[len(rt) // 2]
        if sun_x * (a2[0] - a1[0]) < 0:
            a1, a2 = a2, a1
        sa = .32 if not inner else .16
        cg = s.lin([(0, shadow, sa), (.5, shadow, sa * .25), (.8, shadow, 0), (1, rim, .25)], a1[0], a1[1], a2[0], a2[1], user=True)
        out.append(f'<path d="{d}" fill="{cg}"/>')
        bg = s.lin([(0, shadow, .3 if ri <= 2 else .18), (.22, shadow, 0)], b[0], b[1], t[0], t[1], user=True)
        out.append(f'<path d="{d}" fill="{bg}"/>')
        if veins:
            vs = []
            nv = 9
            for j in range(nv):
                q = (j + .5) / nv
                pts = [(_lerp(l[0], r[0], q), _lerp(l[1], r[1], q)) for l, r in zip(le[1:-1], rt[1:-1])]
                vs.append("M" + "L".join(f"{f(x)} {f(y)}" for x, y in pts))
            out.append(f'<path d="{"".join(vs)}" stroke="{mix(tip, shadow, .25)}" stroke-opacity="{.13 if not inner else .08}" stroke-width="{f(1.0 * sc)}" fill="none"/>')
        # keel or groove along the middle of the petal
        ml = "M" + "L".join(f"{f(x)} {f(y)}" for x, y in m[2:-2])
        out.append(f'<path d="{ml}" stroke="{"#ffffff" if not inner else shadow}" stroke-opacity="{.22 if not inner else .1}" stroke-width="{f(2.2 * sc)}" fill="none" filter="{s.blur(1.2 * sc)}"/>')
        out.append(f'<path d="{d}" fill="none" stroke="{rim_g}" stroke-width="{f(1.5 * sc)}" stroke-linejoin="round"/>')
    if pod and not pod_drawn:
        out.append(pod_svg())
    out.append('</g>')
    s.add("".join(out))


def bud3d(s, x, y, sc=1.0, lean=0.0, tip="#d93d78", base="#fbeef0", seed=1, rim="#fff1d8", shadow="#6a1a40"):
    """A closed lotus bud on top of its stem at (x, y); about 150 units tall at sc=1."""
    rng = random.Random(seed)
    out = []
    h, w = 150 * sc, 60 * sc
    tx = x + lean * h
    for k, (dx, ww, hh, a) in enumerate(((-.5, .8, .82, .9), (.55, .8, .85, .9), (0, 1, 1, 1))):
        bx = x + dx * w * .35
        L = h * hh
        W_ = w * ww
        ttx = tx + dx * w * .1
        d = (f"M{f(bx)} {f(y)}C{f(bx - W_ * .75)} {f(y - L * .12)} {f(bx - W_ * .62)} {f(y - L * .62)} {f(ttx)} {f(y - L)}"
             f"C{f(bx + W_ * .62)} {f(y - L * .62)} {f(bx + W_ * .75)} {f(y - L * .12)} {f(bx)} {f(y)}Z")
        g = s.lin([(0, mix(base, "#d8e0a0", .2), 1), (.35, base, 1), (.75, mix(base, tip, .6), 1), (1, tip, 1)], bx, y, ttx, y - L, user=True)
        cg = s.lin([(0, shadow, .35), (.5, shadow, .05), (.8, "#fff", 0), (1, rim, .25)], bx - W_ * .6, 0, bx + W_ * .6, 0, user=True)
        out.append(f'<path d="{d}" fill="{g}"/><path d="{d}" fill="{cg}"/>')
        vs = "".join(f"M{f(bx + o * W_ * .3)} {f(y - 4 * sc)}Q{f(bx + o * W_ * .55)} {f(y - L * .5)} {f(ttx + o * 2)} {f(y - L * .96)}" for o in (-1, -.5, 0, .5, 1))
        out.append(f'<path d="{vs}" stroke="{shadow}" stroke-opacity=".12" stroke-width="{f(1 * sc)}" fill="none"/>')
        out.append(f'<path d="M{f(bx)} {f(y)}C{f(bx + W_ * .75)} {f(y - L * .12)} {f(bx + W_ * .62)} {f(y - L * .62)} {f(ttx)} {f(y - L)}" stroke="{rim}" stroke-opacity=".6" stroke-width="{f(1.6 * sc)}" fill="none"/>')
    # sepals
    out.append(f'<path d="M{f(x - 14 * sc)} {f(y + 2 * sc)}Q{f(x - 22 * sc)} {f(y - 18 * sc)} {f(x - 10 * sc)} {f(y - 30 * sc)}Q{f(x - 4 * sc)} {f(y - 10 * sc)} {f(x)} {f(y + 4 * sc)}Z'
               f'M{f(x + 14 * sc)} {f(y + 2 * sc)}Q{f(x + 22 * sc)} {f(y - 18 * sc)} {f(x + 10 * sc)} {f(y - 30 * sc)}Q{f(x + 4 * sc)} {f(y - 10 * sc)} {f(x)} {f(y + 4 * sc)}Z" fill="#4f7a3e" opacity=".9"/>')
    s.add("".join(out))


def stem(s, x0, y0, x1, y1, w=6, color="#3d6a3c", rim="#d8e8a0", bend=0.0, rim_a=.5):
    """A lotus stem from (x0, y0) (top) down to (x1, y1)."""
    mx = (x0 + x1) / 2 + bend
    s.add(f'<path d="M{f(x0)} {f(y0)}Q{f(mx)} {f((y0 + y1) / 2)} {f(x1)} {f(y1)}" stroke="{color}" stroke-width="{f(w)}" fill="none" stroke-linecap="round"/>'
          f'<path d="M{f(x0 + w * .3)} {f(y0)}Q{f(mx + w * .3)} {f((y0 + y1) / 2)} {f(x1 + w * .3)} {f(y1)}" stroke="{rim}" stroke-opacity="{rim_a}" stroke-width="{f(max(1, w * .22))}" fill="none"/>')


def dew(s, pts, color="#ffffff", r=(2.5, 6), seed=1, a=0.9):
    """Dew drops: a dark lower rim, a bright refracted crescent and a sharp highlight."""
    rng = random.Random(seed)
    out = []
    for x, y in pts:
        rr = rng.uniform(*r)
        g = s.rad([(0, "#ffffff", .05), (.65, "#ffffff", .12), (.85, "#3a1028", .3), (1, "#3a1028", 0)], .5, .4, .55)
        out.append(f'<ellipse cx="{f(x + rr * .2)}" cy="{f(y + rr * .35)}" rx="{f(rr * 1.05)}" ry="{f(rr * .8)}" fill="#000" opacity=".12"/>'
                   f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(rr)}" fill="{g}"/>'
                   f'<path d="M{f(x - rr * .7)} {f(y + rr * .3)}A{f(rr * .8)} {f(rr * .8)} 0 0 0 {f(x + rr * .7)} {f(y + rr * .3)}" stroke="{color}" stroke-opacity=".55" stroke-width="{f(rr * .25)}" fill="none"/>'
                   f'<circle cx="{f(x - rr * .35)}" cy="{f(y - rr * .4)}" r="{f(rr * .26)}" fill="#fff" opacity="{a}"/>')
    s.add(f'<g>{"".join(out)}</g>')


def lily_pad(s, cx, cy, rx, ry=None, rot=0.0, dark="#173d33", light="#3f7f5c", rim="#d6e79a", rim_a=0.5, seed=1,
             sheen=None, drops=0, blur=0, sky="#f3b8a8"):
    """A floating lotus leaf: round and peltate (no notch), veins radiating from the centre,
    a wavy margin, a waxy sheen that mirrors the sky, and water beading on it."""
    rng = random.Random(seed)
    ry = ry or rx * .26
    pts = []
    n = 120
    ph = [rng.uniform(0, 6.28) for _ in range(3)]
    for k in range(n):
        a = 2 * math.pi * k / n
        wob = 1 + .022 * math.sin(a * 9 + ph[0]) + .014 * math.sin(a * 17 + ph[1]) + .03 * math.sin(a * 2 + ph[2])
        pts.append((cx + math.cos(a) * rx * wob, cy + math.sin(a) * ry * wob))
    d = _poly(pts)
    sq = f"translate(0 {f(cy * (1 - ry / rx))}) scale(1 {f(ry / rx)})"
    g = s.rad([(0, mix(light, "#e8f0b0", .12), 1), (.12, light, 1), (.7, mix(light, dark, .45), 1), (1, dark, 1)], cx, cy, rx, user=True, transform=sq)
    ox, oy = cx + rng.uniform(-.06, .06) * rx, cy + rng.uniform(-.1, .1) * ry
    veins = []
    for k in range(17):
        a = 2 * math.pi * k / 17 + rng.uniform(-.08, .08)
        ex, ey = cx + math.cos(a) * rx * .96, cy + math.sin(a) * ry * .96
        mx, my = ox + (ex - ox) * .5 + math.cos(a + 1.57) * rx * .03, oy + (ey - oy) * .5 + math.sin(a + 1.57) * ry * .03
        veins.append(f"M{f(ox)} {f(oy)}Q{f(mx)} {f(my)} {f(ex)} {f(ey)}")
        # fork near the margin
        fx_, fy_ = ox + (ex - ox) * .72, oy + (ey - oy) * .72
        for sgn in (-1, 1):
            veins.append(f"M{f(fx_)} {f(fy_)}L{f(cx + math.cos(a + sgn * .09) * rx * .97)} {f(cy + math.sin(a + sgn * .09) * ry * .97)}")
    flt = f' filter="{s.blur(blur)}"' if blur else ""
    out = [f'<g{flt}>',
           f'<ellipse cx="{f(cx)}" cy="{f(cy + ry * .12)}" rx="{f(rx * 1.04)}" ry="{f(ry * 1.1)}" fill="#05060c" opacity=".4" filter="{s.blur(max(1, ry * .15))}"/>',
           f'<path d="{d}" fill="{g}"/>',
           f'<path d="{d}" fill="{dark}" filter="{s.grain(0.9 / max(1, rx / 120), 3, .35, seed, "#000000")}" opacity=".5"/>',
           f'<path d="{"".join(veins)}" stroke="{mix(light, "#f4f0c0", .35)}" stroke-opacity=".2" stroke-width="{f(max(.7, rx * .006))}" fill="none"/>']
    # waxy sheen mirroring the bright sky, strongest on the far half
    sx, sy = sheen if sheen else (cx + rx * .2, cy - ry * .4)
    out.append(f'<path d="{d}" fill="{s.rad([(0, sky, .42), (.6, sky, .12), (1, sky, 0)], sx, sy, rx * .8, user=True, transform=f"translate(0 {f(sy * (1 - ry / rx))}) scale(1 {f(ry / rx)})")}" style="mix-blend-mode:screen"/>')
    # the margin: lit far edge, dark near edge
    far = "M" + "L".join(f"{f(x)} {f(y)}" for x, y in pts[n // 2:] + pts[:1])
    near = "M" + "L".join(f"{f(x)} {f(y)}" for x, y in pts[:n // 2 + 1])
    out.append(f'<path d="{far}" stroke="{rim}" stroke-opacity="{rim_a}" stroke-width="{f(max(1.2, rx * .01))}" fill="none" filter="{s.blur(max(.5, rx * .003))}"/>')
    out.append(f'<path d="{near}" stroke="#08130f" stroke-opacity=".55" stroke-width="{f(max(1.4, rx * .014))}" fill="none"/>')
    out.append(f'<circle cx="{f(ox)}" cy="{f(oy)}" r="{f(max(1.5, rx * .012))}" fill="{mix(light, "#f4f0c0", .4)}" opacity=".5"/>')
    out.append('</g>')
    s.add("".join(out))
    if drops:
        dpts = []
        for _ in range(drops):
            a, r = rng.uniform(0, 6.28), rng.uniform(.15, .75)
            dpts.append((cx + math.cos(a) * rx * r, cy + math.sin(a) * ry * r))
        beads(s, dpts, r=(max(2, rx * .012), max(4, rx * .035)), seed=seed, flat=ry / rx)


def beads(s, pts, r=(3, 9), seed=1, flat=0.5, sky="#ffe2c8"):
    """Beads of water on a lotus leaf: rounded silver drops that never wet it."""
    rng = random.Random(seed)
    out = []
    for x, y in pts:
        rr = rng.uniform(*r)
        ry = rr * (.7 + flat * .5)
        g = s.rad([(0, "#ffffff", .1), (.55, sky, .22), (.85, "#1a2a24", .35), (1, "#1a2a24", .1)], .45, .35, .6)
        out.append(f'<ellipse cx="{f(x + rr * .3)}" cy="{f(y + ry * .5)}" rx="{f(rr * 1.1)}" ry="{f(ry * .7)}" fill="#020806" opacity=".35" filter="{s.blur(max(.6, rr * .2))}"/>'
                   f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(rr)}" ry="{f(ry)}" fill="{g}"/>'
                   f'<path d="M{f(x - rr * .7)} {f(y + ry * .25)}A{f(rr * .75)} {f(ry * .75)} 0 0 0 {f(x + rr * .7)} {f(y + ry * .25)}" stroke="{sky}" stroke-opacity=".65" stroke-width="{f(max(.6, rr * .2))}" fill="none"/>'
                   f'<ellipse cx="{f(x - rr * .35)}" cy="{f(y - ry * .4)}" rx="{f(rr * .26)}" ry="{f(ry * .22)}" fill="#fff"/>')
    s.add("".join(out))


# =====================================================================================
# 1. the lotus
# =====================================================================================
@scene
def lotus(s):
    sun = (1150, 418)
    wl = 470
    s.sky([(0, "#22234c"), (.15, "#3c376a"), (.28, "#71548a"), (.38, "#c47f9c"), (.44, "#f2a99c"), (.47, "#ffd6ae")])
    s.stars(40, 0, 200, seed=2, bright=.45)
    s.sun(*sun, 30, halo_r=620, halo_a=.85)
    s.fx("clouds", y0=20, y1=280, seed=57, cell=170, aniso=4.5, cover=.36, soft=.22, lit="#ffbea8", body=.75, direct=.8,
         light=(0.4, 1), sun=(sun[0], sun[1], 460), opacity=.8)
    s.fx("clouds", y0=280, y1=440, seed=52, cell=90, aniso=7, cover=.3, soft=.24, lit="#ffe0b8", body=.85, direct=.95,
         light=(0.2, 1), sun=(sun[0], sun[1], 360), opacity=.7)
    far = ridgeline(wl, 26, 53, cell=240, octaves=5, ridged=.3)
    hills(s, far, "#a76f8c", "#c99198", haze="#ffcaa8", haze_a=.5, haze_h=26)
    rng = random.Random(5)
    crowns = "".join(crown(x, wl - rng.uniform(2, 10), rng.uniform(7, 16), seed=int(x)) for x in range(-20, 1640, 12) if rng.random() < .7)
    s.add(f'<path d="{crowns}" fill="#8a5f80" opacity=".8" filter="{s.blur(2)}"/>')
    s.mist(wl - 6, 46, "#ffd8bc", .75, 12)
    s.fx("reflect", y0=wl, strength=.9, tint="#2a1838", tint_near=.6, tint_far=.05, amp=2)
    s.fx("glints", y0=wl, cx=sun[0], color="#fff0c8", width=40, strength=.9, scatter=.03, density=.4)
    s.wisps(16, 0, W, wl + 4, wl + 60, "#ffdcc8", a=(.12, .28), length=(300, 800), thick=(8, 20), blur=12, seed=6)
    s.glow(sun[0], wl + 10, 520, "#ffb070", .3, .2, sy=.25)
    # middle distance
    leaf = dict(dark="#1f3438", light="#4a6460", rim="#ffd0a0", rim_a=.45, sky="#f3b2a2")
    for (x, y, r, sd) in ((300, 520, 64, 11), (1360, 512, 46, 12), (1520, 548, 80, 13), (90, 575, 110, 14), (620, 540, 50, 15), (980, 528, 40, 16)):
        lily_pad(s, x, y, r, r * .17, seed=sd, **leaf)
    stem(s, 236, 438, 232, 520, w=3.2, color="#3c4f44", rim="#ffd0a0")
    bud3d(s, 236, 440, .36, lean=.06, seed=2)
    ob.standing_leaf(s, 1390, 470, .62, water=525, seed=3, dark="#16302c", light="#4e6e5c", rim="#ffd6a8")
    s.fx("mottle", amp=.03, cell=40, y0=wl, y1=H)
    # the flower and its leaves
    big = dict(dark="#122a24", light="#3e6a50", rim="#ffd6a0", rim_a=.6, sky="#f7c0a8")
    lily_pad(s, 1130, 760, 320, 70, seed=21, sheen=(1180, 730), drops=6, **big)
    lily_pad(s, 430, 680, 230, 46, seed=22, sheen=(500, 665), drops=4, **big)
    stem(s, 1255, 430, 1246, 742, w=6, rim="#ffe0b0", bend=14)
    bud3d(s, 1255, 434, .9, lean=.07, seed=3)
    m = s.mark()
    stem(s, 795, 600, 806, 730, w=11, rim="#ffe0b0")
    lotus3d(s, 795, 604, 2.25, elev=15, seed=7)
    ob.reflect_since(s, m, 730, .3, 3, 230)
    beads(s, [(1040, 772), (1100, 790), (1180, 748), (420, 694), (470, 676)], r=(5, 10), seed=4)
    m2 = s.mark()
    lily_pad(s, 120, 960, 380, 82, seed=31, dark="#0d201c", light="#2e5242", rim="#ffcf9a", rim_a=.5)
    lily_pad(s, 1540, 975, 330, 72, seed=32, dark="#0d201c", light="#2e5242", rim="#ffcf9a", rim_a=.5)
    inner = "".join(s.body[m2:])
    del s.body[m2:]
    s.add(f'<g filter="{s.blur(7)}">{inner}</g>')
    s.motes(36, 300, 1400, 150, 620, seed=9, size=(.8, 2.0))
    s.fx("godrays", cx=sun[0], cy=sun[1], strength=.35, thresh=.72, decay=.97, radius=240)
    s.fx("mottle", amp=.04, cell=60)
    s.look = {"vibrance": .1}
    return s


# =====================================================================================
# shared pieces for the river scenes
# =====================================================================================
def mound(s, cx, base, w, h, top, bottom, seed=1, rim=None, rim_a=.6, fade=80, ridged=.3, cell=200, lit=None, lit_side=1):
    """A free-standing hill whose foot melts into the ground plane, so rivers can wind behind it."""
    pts = ridgeline(base, h, seed, cell=cell, octaves=5, ridged=ridged, x0=cx - w, x1=cx + w, step=4,
                    envelope=[(cx - w, 0), (cx - w * .55, .8), (cx, 1), (cx + w * .55, .8), (cx + w, 0)])
    pts = [(x, min(y, base)) for x, y in pts]
    ymin = min(y for _, y in pts)
    d = pts_d(pts + [(cx + w, base + fade), (cx - w, base + fade)])
    g = s.lin([(0, top, 1), (1, bottom, 1)], 0, ymin, 0, base + fade, user=True)
    mk = s.mark()
    s.add(f'<path d="{d}" fill="{g}"/>')
    if lit:
        lg = s.lin([(0, lit, 0), (.6, lit, 0), (1, lit, .35)] if lit_side > 0 else [(0, lit, .35), (.4, lit, 0), (1, lit, 0)], cx - w, 0, cx + w, 0, user=True)
        s.add(f'<path d="{d}" fill="{lg}"/>')
    if rim:
        line = "M" + "L".join(f"{f(x)} {f(y)}" for x, y in pts)
        s.add(f'<g clip-path="{s.clip(d)}"><path d="{line}" stroke="{rim}" stroke-opacity="{rim_a}" stroke-width="3" fill="none" filter="{s.blur(1)}"/></g>')
    inner = "".join(s.body[mk:])
    del s.body[mk:]
    i = s.uid("m")
    g2 = s.lin([(0, "#fff", 1), ((base - ymin) / (base + fade - ymin), "#fff", 1), (1, "#fff", 0)], 0, ymin, 0, base + fade, user=True)
    s.defs.append(f'<mask id="{i}" maskUnits="userSpaceOnUse" x="{f(cx - w - 10)}" y="{f(ymin - 10)}" width="{f(2 * w + 20)}" height="{f(base + fade - ymin + 20)}">'
                  f'<rect x="{f(cx - w - 10)}" y="{f(ymin - 10)}" width="{f(2 * w + 20)}" height="{f(base + fade - ymin + 20)}" fill="{g2}"/></mask>')
    s.add(f'<g mask="url(#{i})">{inner}</g>')
    return pts


def dona_lamp(s, cx, cy, sc=1.0, seed=1, reflect=True):
    """A floating leaf-bowl lamp (dona): sal leaves pinned into a bowl, heaped with marigolds,
    a small clay diya burning in the middle. (cx, cy) is the waterline centre; ~130 wide at sc=1."""
    rng = random.Random(seed)
    s.glow(cx, cy + 2 * sc, 330 * sc, "#ff9840", .32, .22, sy=.32)
    m = s.mark()
    w, lip = 64 * sc, cy - 16 * sc
    out = []
    # leaves around the bowl, tips poking above the lip
    leaves = []
    for k in range(9):
        t = (k + .5) / 9
        a = math.pi * (1 - t)
        bx = cx + math.cos(a) * w * .92
        by = lip + 4 * sc + math.sin(a) * 9 * sc
        lean = math.cos(a) * 18 * sc
        L = rng.uniform(22, 32) * sc
        lw = 14 * sc
        tipx, tipy = bx + lean, by - L
        col = mix("#3f4a22", "#7a6a2a", rng.random() * .5)
        d = (f"M{f(bx - lw)} {f(by + 14 * sc)}Q{f(bx - lw * 1.1)} {f(by - L * .4)} {f(tipx)} {f(tipy)}"
             f"Q{f(bx + lw * 1.1)} {f(by - L * .4)} {f(bx + lw)} {f(by + 14 * sc)}Z")
        leaves.append((d, col, tipx, tipy, bx))
    body = (f"M{f(cx - w)} {f(lip)}C{f(cx - w * .95)} {f(cy + 6 * sc)} {f(cx - w * .5)} {f(cy + 12 * sc)} {f(cx)} {f(cy + 12 * sc)}"
            f"C{f(cx + w * .5)} {f(cy + 12 * sc)} {f(cx + w * .95)} {f(cy + 6 * sc)} {f(cx + w)} {f(lip)}Z")
    bg = s.lin([(0, "#2a2a12", 1), (.6, "#4a4418", 1), (1, "#a0702a", 1)], 0, 0, 1, 0)
    out.append(f'<path d="{body}" fill="{bg}"/>')
    # back leaves (behind the flowers)
    for d, col, tx, ty, bx in leaves:
        out.append(f'<path d="{d}" fill="{col}"/><path d="M{f(bx)} {f(lip + 10 * sc)}L{f(tx)} {f(ty + 3 * sc)}" stroke="#d8b860" stroke-opacity=".35" stroke-width="{f(.9 * sc)}"/>')
    out.append(f'<ellipse cx="{f(cx)}" cy="{f(lip)}" rx="{f(w * .94)}" ry="{f(11 * sc)}" fill="#2a1a08"/>')
    # marigolds heaped inside
    heads = []
    for k in range(14):
        a = rng.uniform(0, 2 * math.pi)
        r = rng.uniform(0, .85)
        hx = cx + math.cos(a) * w * .8 * r
        hy = lip - 3 * sc + math.sin(a) * 8 * sc * r
        if abs(hx - cx) < 16 * sc and hy < lip + 2 * sc:
            continue
        heads.append((hy, hx))
    for hy, hx in sorted(heads):
        out.append(ob.marigold(hx, hy, rng.uniform(7, 10) * sc, rng.choice(["#f59a1b", "#f7b52a", "#ee7a1a", "#e8562a"]), rng.randint(0, 999)))
    for k in range(6):
        px, py = cx + rng.uniform(-w * .7, w * .7), lip + rng.uniform(-6, 2) * sc
        out.append(f'<ellipse cx="{f(px)}" cy="{f(py)}" rx="{f(5 * sc)}" ry="{f(2.4 * sc)}" fill="#c91e3a" transform="rotate({rng.randint(0, 180)} {f(px)} {f(py)})"/>')
    # the clay diya
    dy_ = lip - 8 * sc
    out.append(f'<path d="M{f(cx - 17 * sc)} {f(dy_)}Q{f(cx - 15 * sc)} {f(dy_ + 12 * sc)} {f(cx)} {f(dy_ + 12 * sc)}Q{f(cx + 15 * sc)} {f(dy_ + 12 * sc)} {f(cx + 17 * sc)} {f(dy_)}Z" fill="#8a3a14"/>'
               f'<ellipse cx="{f(cx)}" cy="{f(dy_)}" rx="{f(17 * sc)}" ry="{f(4.5 * sc)}" fill="#c8682a"/>'
               f'<ellipse cx="{f(cx)}" cy="{f(dy_ + .6 * sc)}" rx="{f(13 * sc)}" ry="{f(3 * sc)}" fill="#e0a040"/>')
    # front leaves, lit by the flame along their tops
    front = body
    lg = s.lin([(0, "#ffcf7a", .55), (.4, "#ffcf7a", 0)], 0, lip, 0, cy + 12 * sc, user=True)
    out.append(f'<path d="{front}" fill="{s.lin([(0, "#53501e", 1), (1, "#1e1c0a", 1)], 0, 0, 0, 1)}"/>'
               f'<path d="{front}" fill="{lg}"/>')
    ribs = "".join(f"M{f(cx + o * w * .9)} {f(lip + 2 * sc)}Q{f(cx + o * w * .75)} {f(cy + 6 * sc)} {f(cx + o * w * .45)} {f(cy + 10 * sc)}" for o in (-.8, -.45, -.1, .25, .6))
    out.append(f'<path d="{ribs}" stroke="#0e0c04" stroke-opacity=".45" stroke-width="{f(1.2 * sc)}" fill="none"/>')
    out.append(f'<path d="M{f(cx - w)} {f(lip)}Q{f(cx)} {f(lip + 13 * sc)} {f(cx + w)} {f(lip)}" stroke="#ffd890" stroke-opacity=".6" stroke-width="{f(1.4 * sc)}" fill="none"/>')
    s.add("".join(out))
    s.flame(cx, dy_ - 1 * sc, 30 * sc, glow_r=200 * sc, glow_a=.55)
    if reflect:
        ob.reflect_since(s, m, cy + 10 * sc, .45, 2.5 * sc, 120 * sc)


def wake(s, cx, cy, sc=1.0, color="#ffcf8a", n=6, a=.4, seed=1):
    """Rings spreading behind a lamp drifting away from us: each older ring is wider and
    centred a little nearer the viewer; only the near half catches the light."""
    rng = random.Random(seed)
    out = []
    for k in range(1, n + 1):
        t = k / n
        rx = (60 + 52 * k ** 1.15) * sc
        ry = rx * (.16 + .02 * k)
        yc = cy + 8 * sc * k ** 1.3
        x0, x1 = cx - rx, cx + rx
        op = a * (1 - t * .75) * rng.uniform(.8, 1)
        out.append(f'<path d="M{f(x0)} {f(yc)}A{f(rx)} {f(ry)} 0 0 0 {f(x1)} {f(yc)}" stroke="{color}" stroke-opacity="{op:.2f}" stroke-width="{f((1.2 + k * .35) * sc)}" fill="none" stroke-dasharray="{f(rx * .5)} {f(rx * .08)} {f(rx * .9)} {f(rx * .1)}"/>')
    s.add(f'<g filter="{s.blur(1.4 * sc)}">{"".join(out)}</g>')


def floating_petals(s, x0, x1, y0, y1, n, seed=1, colors=("#f39a1c", "#f7b52a", "#e8562a", "#c91e3a"), size=(5, 11), a=.9):
    rng = random.Random(seed)
    out = []
    for _ in range(n):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        t = (y - y0) / max(1, y1 - y0)
        r = rng.uniform(*size) * (.4 + .9 * t)
        c = rng.choice(colors)
        rot = rng.uniform(-25, 25)
        out.append(f'<g transform="translate({f(x)} {f(y)}) rotate({rot:.0f})"><ellipse cx="0" cy="{f(r * .25)}" rx="{f(r * 1.1)}" ry="{f(r * .3)}" fill="#000" opacity=".25"/>'
                   f'<ellipse rx="{f(r)}" ry="{f(r * .34)}" fill="{c}"/><ellipse cx="{f(-r * .2)}" cy="{f(-r * .08)}" rx="{f(r * .5)}" ry="{f(r * .12)}" fill="#fff4c0" opacity=".35"/></g>')
    s.add(f'<g opacity="{a}">{"".join(out)}</g>')


# =====================================================================================
# 2. a leaf lamp floating away (antyeshti)
# =====================================================================================
@scene
def lamp_river(s):
    wl = 500
    glow_c = (800, 498)
    s.sky([(0, "#141838"), (.2, "#24285a"), (.34, "#4a3f78"), (.43, "#93608c"), (.48, "#d98a86"), (.5, "#ffc38e")])
    s.stars(70, 0, 260, seed=11, bright=.6)
    s.add(s.sparkle(1120, 150, 12, "#fff6e0", .9))
    s.glow(glow_c[0], glow_c[1], 760, "#ff9a6a", .5, .18, sy=.42)
    s.glow(glow_c[0], glow_c[1], 260, "#ffd8a0", .7, .25, sy=.3)
    s.fx("clouds", y0=40, y1=320, seed=64, cell=200, aniso=5, cover=.38, soft=.24, lit="#b87894", body=.72, direct=.55,
         light=(0, 1), sun=(glow_c[0], glow_c[1], 520), opacity=.8)
    s.fx("clouds", y0=330, y1=480, seed=62, cell=90, aniso=8, cover=.3, soft=.24, lit="#ffbfa0", body=.8, direct=.85,
         light=(0, 1), sun=(glow_c[0], glow_c[1], 420), opacity=.7)
    # far bank: low trees, a few ghat steps and a small temple far away to the left
    far = ridgeline(wl, 14, 63, cell=200, octaves=4, ridged=.2)
    hills(s, far, "#6a4a6e", "#7e5674")
    rng = random.Random(8)
    cr = "".join(crown(x, wl - rng.uniform(2, 8), rng.uniform(6, 14), seed=int(x)) for x in list(range(-20, 520, 11)) + list(range(1080, 1640, 11)) if rng.random() < .8)
    s.add(f'<path d="{cr}" fill="#5e4266" filter="{s.blur(1.2)}"/>')
    arch.shikhara_front(s, 300, wl - 6, .16, color="#5a3e64", rim="#ffb890", door=None)
    arch.chhatri(s, 360, wl - 6, .26, color="#5a3e64")
    for k, x in enumerate((230, 330, 420, 1180, 1300)):
        s.glow(x, wl - 5, 14, "#ffb060", .8, .3)
    s.mist(wl - 4, 50, "#e6a6a0", .7, 12)
    s.fx("reflect", y0=wl, strength=.92, tint="#1a1630", tint_near=.6, tint_far=.04, amp=2.2)
    s.fx("glints", y0=wl, cx=glow_c[0], color="#ffd8a8", width=34, strength=.8, scatter=.03, density=.4, spread=1.6)
    s.wisps(22, -100, W + 100, wl + 4, wl + 120, "#f2c0b8", a=(.1, .26), length=(300, 900), thick=(8, 24), blur=14, seed=13)
    s.mist(wl + 60, 120, "#c89aa8", .25, 30)
    # the lamp, its trail of light, its wake
    lx, ly = 800, 690
    s.glow(lx, (ly + wl) / 2, 300, "#ffb070", .25, .2, sy=.8)
    wake(s, lx, ly + 12, 1.5, n=5, a=.34)
    dona_lamp(s, lx, ly, 1.75, seed=3)
    s.glow(lx, ly + 150, 150, "#ff9a40", .32, .2, sy=1.8)
    floating_petals(s, 0, 1600, 820, 990, 22, seed=5, size=(6, 12), a=.8)
    floating_petals(s, 500, 1100, 720, 800, 8, seed=6, size=(4, 7), a=.8)
    s.birds(2, 960, 1040, 330, 360, color="#2a1a30", s=(7, 10), seed=8, a=.85)
    s.motes(18, 500, 1100, 480, 720, seed=4, size=(.6, 1.6))
    s.fx("godrays", cx=glow_c[0], cy=glow_c[1], strength=.25, thresh=.75, decay=.97, radius=260)
    s.fx("mottle", amp=.04, cell=60)
    return s


# =====================================================================================
# 3. three rivers, one ocean
# =====================================================================================
def river(s, ctrl, w0, w1, near="#4a3c70", far="#fff0c8", y_near=1000, y_far=470, bank="#120d1e", rim="#ffd0a0",
          sparkle=0, seed=1, glint_x=800, glint_w=260, mid="#e89a90"):
    """A river seen from above, mirroring the sky: gold where it nears the sun's road, rose in the
    middle distance and deep violet close by, with dark banks, a lit far edge and fine sparkle."""
    rng = random.Random(seed)
    pts = smooth_line(ctrl, 5)
    d = ribbon(pts, w0, w1)
    bank_d = ribbon(pts, w0 * 1.3 + 6, w1 * 1.3 + 2)
    g = s.lin([(0, far, 1), (.1, mix(far, mid, .5), 1), (.26, mid, 1), (.5, mix(mid, near, .65), 1), (.75, near, 1), (1, mix(near, "#000000", .2), 1)], 0, y_far, 0, y_near, user=True)
    out = [f'<path d="{bank_d}" fill="{bank}" opacity=".6" filter="{s.blur(3)}"/>', f'<path d="{d}" fill="{g}"/>']
    # sky streaks along the current
    for k in range(3):
        off = rng.uniform(-.3, .3)
        sub = [(x + off * (w0 + (w1 - w0) * i / len(pts)) * .5, y) for i, (x, y) in enumerate(pts)]
        out.append(f'<path d="{ribbon(sub, w0 * .12, w1 * .1)}" fill="#ffe8d0" opacity=".12" filter="{s.blur(2)}"/>')
    # near bank in shadow, far bank catching light
    out.append(f'<path d="{d}" fill="none" stroke="#000" stroke-opacity=".14" stroke-width="3" filter="{s.blur(2)}"/>')
    sp = []
    n = len(pts)
    for _ in range(sparkle):
        i = n - 1 - int(rng.random() ** 1.4 * (n - 1))
        x, y = pts[i]
        t = i / (n - 1)
        wloc = (w0 + (w1 - w0) * t)
        x += rng.uniform(-.4, .4) * wloc
        near_g = math.exp(-((x - glint_x) / glint_w) ** 2) * (.3 + .7 * t)
        if rng.random() > near_g:
            continue
        L = rng.uniform(.8, 2.4) * (1 + (1 - t))
        sp.append(f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(L)}" ry="{f(max(.5, L * .3))}" fill="#fff8e0" opacity="{rng.uniform(.4, .9):.2f}"/>')
    out.append(f'<g style="mix-blend-mode:screen">{"".join(sp)}</g>')
    s.add("".join(out))
    return pts


def hill(s, cx, base, h, hw, top, bottom, seed=1, lit=None, light=1, rim=None, rim_center=None, rim_r=900, foot=40,
         haze=None, haze_a=.4, snow=None, rim_a=.8):
    """A single lit hill whose foot fades into the ground, so whatever lies beyond it is hidden
    while the plain in front stays visible."""
    pts = peak_line(base, [(cx, h, hw, .1 * light)], seed, detail=.24, x0=cx - hw * 1.5, x1=cx + hw * 1.5, step=3, shape=1.3, shoulders=3)
    pts = [(x, min(y, base)) for x, y in pts]
    ymin = min(y for _, y in pts)
    mk = s.mark()
    mountains(s, pts, top, bottom, lit=lit, lit_a=.6, light=light, seed=seed, rim=rim, rim_a=rim_a, rim_center=rim_center, rim_r=rim_r,
              rim_w=1.4, gullies=True, haze=haze, haze_a=haze_a, haze_h=h * .7, base_y=base)
    inner = "".join(s.body[mk:])
    del s.body[mk:]
    i = s.uid("m")
    y0 = base - foot
    g2 = s.lin([(0, "#fff", 1), (max(0, (y0 - ymin) / (base + 3 - ymin)), "#fff", 1), (1, "#fff", 0)], 0, ymin, 0, base + 3, user=True)
    s.defs.append(f'<mask id="{i}" maskUnits="userSpaceOnUse" x="-100" y="{f(ymin - 10)}" width="1800" height="{f(base + 3 - ymin + 10)}">'
                  f'<rect x="-100" y="{f(ymin - 10)}" width="1800" height="{f(base + 3 - ymin + 10)}" fill="{g2}"/></mask>')
    s.add(f'<g mask="url(#{i})">{inner}</g>')
    return pts


@scene
def rivers_ocean(s):
    sun = (800, 318)
    hz = 340
    s.sky([(0, "#1a1d48"), (.12, "#34336a"), (.21, "#7a5486"), (.28, "#e08c88"), (.32, "#ffc898"), (.34, "#fff0d0")])
    s.sun(*sun, 28, halo_r=680, halo_a=.85)
    s.fx("clouds", y0=10, y1=210, seed=73, cell=170, aniso=4, cover=.42, soft=.2, lit="#ffb8a0", body=.72, direct=.8,
         light=(0, 1), sun=(sun[0], sun[1], 460), opacity=.9)
    s.fx("clouds", y0=190, y1=320, seed=72, cell=80, aniso=7, cover=.3, soft=.22, lit="#ffe0b0", body=.85, direct=.95,
         light=(0, 1), sun=(sun[0], sun[1], 380), opacity=.7)
    s.fx("reflect", y0=hz, strength=.95, tint="#3a2a50", tint_near=.3, tint_far=.02, amp=1.6, y_end=440)
    s.fx("glints", y0=hz, cx=sun[0], color="#fff2cc", width=50, strength=1.2, scatter=.1, density=.55, y_end=440, spread=3)

    # ground plane: y = hz + 6000 / Z, x = 800 + 600 X / Z
    def P(X, Z):
        return (800 + 600 * X / Z, hz + 6000 / Z)
    Zc = 64  # the coast
    coast = ridgeline(P(0, Zc)[1], 4, 90, cell=180, octaves=3, ridged=.1)
    land = s.lin([(0, "#c88c9c", 1), (.08, "#9a6a8e", 1), (.3, "#5a3e6e", 1), (1, "#1c1430", 1)], 0, P(0, Zc)[1], 0, 1000, user=True)
    s.add(f'<path d="{pts_d(coast + [(1640, 1010), (-40, 1010)])}" fill="{land}"/>')
    s.add(f'<path d="{pts_d(coast + [(1640, 1010), (-40, 1010)])}" fill="#000" filter="{s.grain(.02, 4, .3, 9, "#000000")}" opacity=".5"/>')
    rng0 = random.Random(2)
    woods = []
    for _ in range(260):
        X, Z = rng0.uniform(-40, 40), 9 * (Zc / 9) ** rng0.random()
        x, y = P(X, Z)
        r = 900 / Z * rng0.uniform(.4, 1.2)
        woods.append(f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(r * 1.6)}" ry="{f(r * .5)}"/>')
    s.add(f'<g fill="#140e22" opacity=".28" filter="{s.blur(2)}">{"".join(woods)}</g>')
    s.add(f'<path d="M{"L".join(f"{f(x)} {f(y)}" for x, y in coast)}" stroke="#fff0d8" stroke-opacity=".85" stroke-width="2.2" fill="none" filter="{s.blur(.8)}"/>')
    # three rivers meandering across the plain to one mouth
    rng = random.Random(4)
    rv = dict(near="#c88aa0", far="#fff6dc", mid="#ffc8a4", y_near=1000, y_far=P(0, Zc)[1], glint_x=800, glint_w=170, bank="#140e22")
    for k, (X0, ph, amp) in enumerate(((-13, .5, 4.6), (1.5, 2.2, 3.8), (14, 4.1, 4.8))):
        ctrl = []
        Z = 8.6
        while Z < Zc:
            t = (Z - 8.6) / (Zc - 8.6)
            X = X0 * (1 - t) ** 1.25 + (k - 1) * .5 * t + (amp * math.sin(Z * .42 + ph) + amp * .35 * math.sin(Z * 1.3 + ph * 2)) * (1 - t) ** .6
            ctrl.append(P(X, Z))
            Z *= 1.12
        ctrl.append(P((k - 1) * .5, Zc))
        pts = smooth_line(ctrl, 5)
        widths = [600 * .95 / ((6000 / max(1, y - hz))) for x, y in pts]
        rp = river(s, ctrl, widths[0] * .62, 5, sparkle=320, seed=k + 1, **rv)
        s.add(f'<path d="{ribbon(rp, widths[0] * 1.5, 14)}" fill="#ffc090" opacity=".38" filter="{s.blur(12)}" style="mix-blend-mode:screen"/>')
    mx, my = P(0, Zc)
    s.glow(mx, my, 160, "#fff0c8", .7, .25, sy=.25)
    s.mist(my + 6, 24, "#ffd8c0", .45, 6)
    # hills, far to near, set beside the rivers so they hide them at the bends
    sunrim = dict(rim="#ffd8b0", rim_center=sun, rim_r=1000)
    hills_spec = [  # X, Z, height, half width, light
        (-34, 58, 64, 260, 1), (34, 60, 70, 280, -1), (-21, 46, 70, 170, 1), (22, 44, 76, 190, -1),
        (-11, 34, 46, 110, 1), (13, 31, 52, 120, -1), (-22, 25, 140, 240, 1), (24, 23, 160, 280, -1),
    ]
    for X, Z, h, hw, li in hills_spec:
        x, y = P(X, Z)
        d = min(1, (Z - 20) / 40)
        top = mix("#3a2a56", "#b07896", d)
        bot = mix("#2a1e40", "#946a8c", d)
        plain = mix("#5a3e6e", "#b07a96", d)
        hill(s, x, y + h * .12, h, hw, top, bot, seed=int(X * 7 + Z), lit=mix(top, "#ffc0a0", .55), light=li, foot=h * .3,
             haze=plain, haze_a=.85, rim_a=.85, **sunrim)
        s.mist(y + 2, 24 + 30 * (1 - d), "#f0b8c0", .2 + .2 * d, 8 + 6 * (1 - d), x0=x - hw * 1.4, x1=x + hw * 1.4)
    for my_, x0_, x1_, a_ in ((520, -100, 700, .35), (600, 900, 1700, .3), (700, 200, 1100, .28), (820, -100, 600, .25), (860, 1000, 1700, .25)):
        s.mist(my_, 70, "#e8b8c4", a_, 22, x0=x0_, x1=x1_)
    fg = ridgeline(1000, 190, 95, cell=340, octaves=6, ridged=.45, envelope=[(0, 1.2), (360, .5), (620, .06), (980, .06), (1240, .5), (1600, 1.2)])
    mountains(s, fg, "#20182e", "#0e0a18", lit="#6a4a6a", lit_a=.4, light=1, seed=96, rim="#ffc898", rim_a=.9, rim_center=sun, rim_r=1100, gullies=False)
    pines(s, -20, 330, 0, 14, h=(60, 160), color="#0c0916", seed=4, ground_fn=lambda x: y_at(fg, x))
    pines(s, 1270, 1640, 0, 14, h=(60, 170), color="#0c0916", seed=5, ground_fn=lambda x: y_at(fg, x))
    s.birds(6, 860, 1060, 230, 290, color="#3a2440", s=(5, 9), seed=7, a=.8)
    s.fx("godrays", cx=sun[0], cy=sun[1], strength=.4, thresh=.72, decay=.972, radius=240)
    s.fx("mottle", amp=.045, cell=60)
    return s


# =====================================================================================
# 4. one sun, many reflections
# =====================================================================================
def matka(s, cx, base, sc=1.0, clay="#b4532a", rim="#ffd29a", sun_dx=0.0, water_sky=("#ffd9a0", "#6a3a40"), seed=1,
          paint=True, light=1, wide=1.0, tall=1.0):
    """A round clay water pot (matka) filled to the brim; the water holds a small sun.
    (cx, base) is where it stands; about 200 tall at sc=1."""
    rng = random.Random(seed)
    def P(x, y):
        return f"{f(cx + x * sc * (wide if abs(x) > 50 else 1))} {f(base + y * sc * tall)}"
    body = (f"M{P(-46, -186)}C{P(-44, -176)} {P(-40, -170)} {P(-42, -164)}"
            f"C{P(-70, -152)} {P(-100, -130)} {P(-100, -92)}C{P(-100, -46)} {P(-70, -10)} {P(-32, -2)}"
            f"Q{P(0, 3)} {P(32, -2)}C{P(70, -10)} {P(100, -46)} {P(100, -92)}C{P(100, -130)} {P(70, -152)} {P(42, -164)}"
            f"C{P(40, -170)} {P(44, -176)} {P(46, -186)}Z")
    out = []
    out.append(f'<ellipse cx="{f(cx + 14 * sc * -light)}" cy="{f(base + 2 * sc)}" rx="{f(118 * sc)}" ry="{f(14 * sc)}" fill="#0a0406" opacity=".6" filter="{s.blur(6 * sc)}"/>')
    g = s.lin([(0, mix(clay, "#000000", .7), 1), (.35, mix(clay, "#000000", .35), 1), (.7, clay, 1), (.9, mix(clay, "#ffc890", .35), 1), (1, mix(clay, "#000000", .3), 1)] if light > 0 else
              [(0, mix(clay, "#000000", .3), 1), (.1, mix(clay, "#ffc890", .35), 1), (.3, clay, 1), (.65, mix(clay, "#000000", .35), 1), (1, mix(clay, "#000000", .7), 1)],
              cx - 100 * sc, 0, cx + 100 * sc, 0, user=True)
    out.append(f'<path d="{body}" fill="{g}"/>')
    vg = s.lin([(0, "#000", .1), (.45, "#000", 0), (.8, "#000", .25), (1, "#000", .55)], 0, base - 186 * sc, 0, base, user=True)
    out.append(f'<path d="{body}" fill="{vg}"/>')
    out.append(f'<path d="{body}" fill="{clay}" filter="{s.grain(.7, 3, .25, seed, "#000000")}" opacity=".6"/>')
    if paint:
        # painted bands round the shoulder: white dots and a wavy line, following the curve
        dots, wave = [], []
        for k in range(26):
            t = (k + .5) / 26
            a = math.pi * t
            x = -math.cos(a) * 88
            y = -128 + math.sin(a) * 16
            sh = .35 + .65 * (math.sin(a) ** .5) * (1 if light * x > -30 else .6)
            dots.append(f'<circle cx="{f(cx + x * sc)}" cy="{f(base + y * sc)}" r="{f(2.6 * sc)}" fill="#f2e2c4" opacity="{.55 * sh:.2f}"/>')
        pts = []
        for k in range(61):
            a = math.pi * k / 60
            x = -math.cos(a) * 96
            y = -104 + math.sin(a) * 18 + math.sin(k * 1.1) * 4
            pts.append((cx + x * sc, base + y * sc))
        wave = "M" + "L".join(f"{f(x)} {f(y)}" for x, y in pts)
        band = "M" + "L".join(f"{f(cx - math.cos(math.pi * k / 40) * 99 * sc)} {f(base + (-90 + math.sin(math.pi * k / 40) * 19) * sc)}" for k in range(41))
        out.append("".join(dots) + f'<path d="{wave}" stroke="#f2e2c4" stroke-opacity=".38" stroke-width="{f(2.2 * sc)}" fill="none"/>'
                   f'<path d="{band}" stroke="#2a0e06" stroke-opacity=".35" stroke-width="{f(5 * sc)}" fill="none"/>')
    # rim light on the side towards the sun, and a wet sheen
    edge = (f"M{P(42 * light, -164)}C{P(70 * light, -152)} {P(100 * light, -130)} {P(100 * light, -92)}C{P(100 * light, -46)} {P(70 * light, -10)} {P(32 * light, -2)}")
    out.append(f'<g clip-path="{s.clip(body)}"><path d="{edge}" stroke="{rim}" stroke-opacity=".7" stroke-width="{f(7 * sc)}" fill="none" filter="{s.blur(3 * sc)}"/></g>')
    out.append(f'<ellipse cx="{f(cx + 58 * sc * light)}" cy="{f(base - 118 * sc)}" rx="{f(10 * sc)}" ry="{f(26 * sc)}" fill="#fff0d0" opacity=".22" filter="{s.blur(5 * sc)}" transform="rotate({-25 * light} {f(cx + 58 * sc * light)} {f(base - 118 * sc)})"/>')
    # the lip and the water inside
    ly = base - 186 * sc * tall
    out.append(f'<ellipse cx="{f(cx)}" cy="{f(ly)}" rx="{f(55 * sc)}" ry="{f(15 * sc)}" fill="{mix(clay, "#ffb080", .25)}"/>'
               f'<ellipse cx="{f(cx)}" cy="{f(ly + 1.5 * sc)}" rx="{f(55 * sc)}" ry="{f(15 * sc)}" fill="none" stroke="#000" stroke-opacity=".35" stroke-width="{f(2 * sc)}"/>')
    wg = s.lin([(0, water_sky[0], 1), (.6, mix(water_sky[0], water_sky[1], .6), 1), (1, water_sky[1], 1)], 0, ly - 12 * sc, 0, ly + 12 * sc, user=True)
    out.append(f'<ellipse cx="{f(cx)}" cy="{f(ly + 1 * sc)}" rx="{f(46 * sc)}" ry="{f(11.5 * sc)}" fill="{wg}"/>')
    sx, sy = cx + sun_dx * sc, ly - 4 * sc
    clipw = s.clip(f"M{f(cx - 46 * sc)} {f(ly + 1 * sc)}A{f(46 * sc)} {f(11.5 * sc)} 0 1 0 {f(cx + 46 * sc)} {f(ly + 1 * sc)}A{f(46 * sc)} {f(11.5 * sc)} 0 1 0 {f(cx - 46 * sc)} {f(ly + 1 * sc)}Z")
    out.append(f'<g clip-path="{clipw}"><ellipse cx="{f(sx)}" cy="{f(sy)}" rx="{f(34 * sc)}" ry="{f(10 * sc)}" fill="{s.rad([(0, "#fff6d8", 1), (.3, "#ffd890", .7), (1, "#ff9a50", 0)])}"/>'
               f'<ellipse cx="{f(sx)}" cy="{f(sy)}" rx="{f(9 * sc)}" ry="{f(5 * sc)}" fill="#ffffff"/>'
               f'<path d="M{f(sx - 18 * sc)} {f(sy + 5 * sc)}H{f(sx + 18 * sc)}M{f(sx - 12 * sc)} {f(sy + 8 * sc)}H{f(sx + 10 * sc)}" stroke="#fff0c0" stroke-opacity=".5" stroke-width="{f(1.2 * sc)}"/></g>')
    out.append(f'<path d="M{f(cx - 55 * sc)} {f(ly)}A{f(55 * sc)} {f(15 * sc)} 0 0 1 {f(cx + 55 * sc)} {f(ly)}" stroke="{rim}" stroke-opacity=".7" stroke-width="{f(2 * sc)}" fill="none"/>')
    s.add("".join(out))
    s.glow(sx, sy, 60 * sc, "#ffe0a0", .55, .25, sy=.4)


@scene
def sun_pots(s):
    sun = (800, 214)
    wl = 470
    s.sky([(0, "#2a2a5a"), (.12, "#4a3e74"), (.25, "#a46a8a"), (.36, "#f0a888"), (.44, "#ffd8a8"), (.47, "#ffe8c4")])
    s.sun(*sun, 40, halo_r=760, halo_a=.85)
    s.fx("clouds", y0=10, y1=170, seed=94, cell=170, aniso=4, cover=.36, soft=.2, lit="#ffc8a8", body=.75, direct=.85,
         light=(0, -1), sun=(sun[0], sun[1], 420), opacity=.85)
    s.fx("clouds", y0=260, y1=450, seed=92, cell=90, aniso=6, cover=.32, soft=.22, lit="#ffe2b8", body=.85, direct=.95,
         light=(0, -1), sun=(sun[0], sun[1], 380), opacity=.7)
    # far bank with a ghat town in haze
    arch.skyline(s, -20, 1640, wl - 4, h=(20, 56), color="#b08094", seed=93, windows=0, parapet=False,
                 temples=[(330, .34), (1180, .4)], chhatris=[(720, .34)])
    s.mist(wl - 6, 50, "#ffd0b0", .7, 12)
    s.fx("reflect", y0=wl, strength=.9, tint="#3a2440", tint_near=.45, tint_far=.04, amp=2.5)
    s.fx("glints", y0=wl, cx=sun[0], color="#fff2cc", width=50, strength=1.3, scatter=.06, density=.55, spread=2.2)
    s.wisps(14, -100, W + 100, wl + 4, wl + 80, "#ffd8c0", a=(.08, .2), length=(300, 800), thick=(6, 18), blur=12, seed=93)
    arch.boat(s, 1330, 560, .55, color="#3a2238", rim="#ffd0a0", people=1)
    # the stone ledge of a ghat
    top = 800
    ob.ledge(s, top, color="#5a3a34", edge="#ffd8a8", depth=90)
    s.add(f'<rect x="-20" y="{top - 90}" width="1640" height="{1000 - top + 90}" fill="#5a3a34" filter="{s.grain(.03, 3, .25, 5, "#000000")}" opacity=".6"/>')
    s.add(f'<path d="M-20 {top + 70}H1640M-20 {top + 150}H1640" stroke="#000" stroke-opacity=".3" stroke-width="3"/>')
    s.glow(800, top - 40, 700, "#ffb070", .25, .2, sy=.18)
    # the pots, each holding the one sun
    rng = random.Random(4)
    clays = ["#a8482a", "#b65a2e", "#9a3e26", "#b04e2c", "#a44a2a"]
    xs = [330, 565, 800, 1035, 1270]
    for k, x in enumerate(xs):
        sc = [.98, 1.04, 1.1, 1.02, .96][k]
        b = top - 30 + [6, -4, 0, -2, 8][k]
        matka(s, x, b, sc, clay=clays[k], sun_dx=(sun[0] - x) * .02, seed=k + 3, wide=[1, .92, 1.06, .96, 1.02][k], tall=[1, 1.08, .96, 1.04, .94][k], light=1 if x < 800 else -1 if x > 800 else 1,
              water_sky=("#a86a78", "#2a1830"))
    floating_petals(s, 100, 1500, top - 40, top + 40, 14, seed=9, size=(4, 7), a=.85)
    s.add(ob.marigold(700, top - 20, 13, "#f39a1c", 3) + ob.marigold(920, top - 24, 11, "#f7c02a", 4))
    s.birds(5, 880, 1100, 300, 360, color="#4a2a40", s=(5, 8), seed=5, a=.75)
    s.motes(26, 200, 1400, 260, 700, seed=8, size=(.7, 1.8))
    s.fx("godrays", cx=sun[0], cy=sun[1], strength=.4, thresh=.72, decay=.972, radius=260)
    s.fx("mottle", amp=.04, cell=60)
    return s


# =====================================================================================
# 5. offering water to the rising sun (surya arghya)
# =====================================================================================
def arghya_figure(x, y, sc=1.0, color="#100a16", rim=None):
    """A man standing waist-deep, facing right, raising a copper lota with both hands to pour
    water towards the sun. (x, y) is his waist at the waterline. Returns (svg, spout_x, spout_y)."""
    body = (
        f'<g fill="{color}" stroke="{color}" stroke-linecap="round" stroke-linejoin="round">'
        # torso: broad shoulders tapering to the waist, chest towards the sun
        f'<path d="M-19 8C-19 -14 -20 -34 -24 -56C-30 -84 -34 -104 -30 -116C-25 -124 -12 -127 0 -127'
        f'C12 -127 24 -124 28 -118C31 -110 30 -96 27 -84C23 -68 18 -46 18 -28C18 -14 18 0 19 8Z" stroke="none"/>'
        f'<path d="M-6 -124L-4 -138H10L12 -124Z" stroke="none"/>'
        # head in profile with the hair tied in a knot at the back
        f'<path d="M-11 -152C-11 -168 -1 -177 10 -176C20 -175 25 -168 24 -160L27 -154L24 -152L25 -148L23 -145C23 -140 18 -137 10 -138C2 -138 -9 -142 -11 -152Z" stroke="none"/>'
        f'<ellipse cx="-11" cy="-166" rx="7" ry="6" stroke="none"/>'
        # far arm, then near arm, raised from the shoulders
        f'<path d="M-14 -118Q6 -146 34 -168L50 -190" stroke-width="10" fill="none"/>'
        f'<path d="M18 -118Q30 -144 46 -160L60 -186" stroke-width="12" fill="none"/>'
        f'</g>')
    lota = (f'<g transform="translate(62 -198) rotate(32)">'
            f'<ellipse cx="0" cy="0" rx="16" ry="14" fill="#4a1e0c"/>'
            f'<path d="M-8 -11H8L10 -17H-10Z" fill="#4a1e0c"/>'
            f'<ellipse cx="0" cy="-18" rx="12" ry="3" fill="#5a2810"/>'
            f'<path d="M5 -10C13 -6 16 4 11 11" stroke="#ffb870" stroke-width="2.6" fill="none" opacity=".9"/>'
            f'<path d="M9 -17Q12 -10 14 -5" stroke="#ffd8a0" stroke-width="1.6" fill="none" opacity=".8"/>'
            f'</g>')
    rimsvg = ""
    if rim:
        rimsvg = (f'<path d="M28 -118C31 -110 30 -96 27 -84C23 -68 18 -46 18 -28C18 -14 18 0 19 8" stroke="{rim}" stroke-width="2.6" fill="none" opacity=".85"/>'
                  f'<path d="M24 -160L27 -154L24 -152L25 -148L23 -145C23 -140 18 -137 10 -138" stroke="{rim}" stroke-width="2" fill="none" opacity=".8"/>'
                  f'<path d="M10 -176C20 -175 25 -168 24 -160" stroke="{rim}" stroke-width="2" fill="none" opacity=".8"/>'
                  f'<path d="M24 -122Q36 -146 52 -162L64 -186" stroke="{rim}" stroke-width="2" fill="none" opacity=".75"/>')
    svg = f'<g transform="translate({f(x)} {f(y)}) scale({f(sc)})">{body}{lota}{rimsvg}</g>'
    ang = math.radians(32 - 90)
    sx, sy = 62 + math.cos(ang) * 18 + 9, -198 + math.sin(ang) * 18 + 3
    return svg, x + sx * sc, y + sy * sc


def water_stream(s, x0, y0, x1, y1, sc=1.0, seed=1, color="#fff2d0", glow="#ffd090"):
    """A stream of poured water: a slim falling arc that breaks into drops, lit from behind."""
    rng = random.Random(seed)
    pts = []
    n = 40
    for k in range(n + 1):
        t = k / n
        # parabola: out and then down
        x = x0 + (x1 - x0) * (1 - (1 - t) ** 2.2)
        y = y0 + (y1 - y0) * t ** 1.6
        pts.append((x, y))
    out = [f'<path d="{ribbon(pts, 9 * sc, 3 * sc)}" fill="{glow}" opacity=".5" filter="{s.blur(6 * sc)}" style="mix-blend-mode:screen"/>',
           f'<path d="{ribbon(pts[:int(n * .8)], 6 * sc, 2.6 * sc)}" fill="{color}" opacity=".85"/>',
           f'<path d="{ribbon(pts[:int(n * .8)], 2 * sc, 1 * sc)}" fill="#ffffff" opacity=".9"/>']
    for k in range(34):
        t = rng.uniform(.45, 1)
        i = int(t * n)
        x, y = pts[i]
        x += rng.gauss(0, 4 * sc * t)
        r = rng.uniform(.8, 2.4) * sc
        out.append(f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(r * .8)}" ry="{f(r * 1.5)}" fill="#fff8e8" opacity="{rng.uniform(.5, 1):.2f}"/>')
    # splash where it meets the river
    for k in range(14):
        a = rng.uniform(-2.8, -.3)
        L = rng.uniform(6, 22) * sc
        out.append(f'<path d="M{f(x1)} {f(y1)}l{f(math.cos(a) * L)} {f(math.sin(a) * L)}" stroke="#fff4dc" stroke-width="{f(1.2 * sc)}" opacity=".7" stroke-linecap="round"/>')
    s.add(f'<g style="mix-blend-mode:screen">{"".join(out)}</g>')
    s.glow(x1, y1, 50 * sc, "#ffe0a0", .7, .3, sy=.4)


def ripples(s, cx, cy, rx0, ry0, n=5, gap=1.6, color="#ffd8a0", a=.4, w=1.6):
    out = []
    for k in range(n):
        rx, ry = rx0 * gap ** k, ry0 * gap ** k
        out.append(f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(rx)}" ry="{f(ry)}" fill="none" stroke="{color}" stroke-opacity="{a * (1 - k / n):.2f}" stroke-width="{f(w * (1 + k * .3))}"/>')
    s.add(f'<g filter="{s.blur(1)}">{"".join(out)}</g>')


@scene
def sun_arc(s):
    sun = (912, 572)
    wl = 640
    s.sky([(0, "#1c1f4c"), (.18, "#3a356c"), (.36, "#86598a"), (.48, "#e48c84"), (.56, "#ffbc84"), (.62, "#ffe2b0"), (.64, "#fff2d8")])
    s.stars(30, 0, 180, seed=21, bright=.4)
    s.sun(*sun, 46, halo_r=780, halo_a=.9)
    s.fx("clouds", y0=20, y1=330, seed=101, cell=170, aniso=4, cover=.42, soft=.2, lit="#ffb8a0", body=.72, direct=.8,
         light=(0.2, 1), sun=(sun[0], sun[1], 480), opacity=.9)
    s.fx("clouds", y0=360, y1=560, seed=102, cell=90, aniso=7, cover=.3, soft=.22, lit="#ffe0b0", body=.85, direct=.95,
         light=(0, 1), sun=(sun[0], sun[1], 400), opacity=.7)
    far = ridgeline(wl, 22, 103, cell=220, octaves=5, ridged=.2)
    hills(s, far, "#9a6684", "#b07a8a")
    rng = random.Random(3)
    cr = "".join(crown(x, wl - rng.uniform(2, 10), rng.uniform(7, 16), seed=int(x)) for x in range(-20, 1640, 12) if rng.random() < .6)
    s.add(f'<path d="{cr}" fill="#8a5a7c" filter="{s.blur(1.2)}"/>')
    arch.shikhara_front(s, 330, wl - 8, .22, color="#7a4e72", rim="#ffc8a0", door=None)
    s.mist(wl - 4, 46, "#ffd0b0", .75, 12)
    s.fx("reflect", y0=wl, strength=.92, tint="#2a1a38", tint_near=.5, tint_far=.04, amp=3)
    s.fx("glints", y0=wl, cx=sun[0], color="#fff0c8", width=56, strength=1.3, scatter=.06, density=.55, spread=2.4)
    s.wisps(14, -100, W + 100, wl + 4, wl + 80, "#ffd8c0", a=(.08, .2), length=(300, 800), thick=(6, 18), blur=12, seed=4)
    # the devotee
    fx_, fy = 676, wl + 4
    svg, sx, sy = arghya_figure(fx_, fy, 1.75, color="#120b18", rim="#ffd29a")
    m = s.mark()
    s.add(svg)
    ob.reflect_since(s, m, wl + 4, .35, 3, 260)
    ripples(s, fx_, wl + 6, 70, 9, n=5, gap=1.45, a=.45)
    ripples(s, sx + 64, wl + 10, 18, 3, n=4, gap=1.7, a=.5, color="#fff0c8")
    s.birds(5, 1020, 1240, 380, 450, color="#4a2a44", s=(5, 9), seed=6, a=.8)
    s.motes(22, 600, 1200, 300, 640, seed=5, size=(.7, 1.8))
    s.fx("godrays", cx=sun[0], cy=sun[1], strength=.45, thresh=.7, decay=.972, radius=260)
    water_stream(s, sx, sy, sx + 64, wl + 8, sc=1.6, seed=3)
    s.fx("mottle", amp=.04, cell=60)
    return s


# =====================================================================================
# 6. the pot of nectar above the sangam
# =====================================================================================
def kalash(s, cx, cy, sc=1.0, glow=True):
    """A golden purna kalash: round pot, mango leaves fanned at the mouth and a coconut on top.
    (cx, cy) is the centre of the pot's belly; about 260 tall at sc=1."""
    def P(x, y):
        return f"{f(cx + x * sc)} {f(cy + y * sc)}"
    if glow:
        s.glow(cx, cy - 40 * sc, 520 * sc, "#ffb040", .55, .16)
        s.glow(cx, cy - 30 * sc, 190 * sc, "#ffe6a0", .7, .3)
    gold = s.lin([(0, "#fff6d2"), (.3, "#f7d27a"), (.62, "#d99a35"), (1, "#8a5418")], 0, 0, .35, 1)
    pot = (f"M{P(-30, -62)}C{P(-34, -56)} {P(-36, -52)} {P(-34, -48)}C{P(-70, -40)} {P(-84, -12)} {P(-84, 10)}"
           f"C{P(-84, 48)} {P(-48, 74)} {P(0, 76)}C{P(48, 74)} {P(84, 48)} {P(84, 10)}C{P(84, -12)} {P(70, -40)} {P(34, -48)}"
           f"C{P(36, -52)} {P(34, -56)} {P(30, -62)}Z"
           f"M{P(-40, -70)}L{P(40, -70)}L{P(36, -60)}L{P(-36, -60)}Z"
           f"M{P(-26, 74)}L{P(26, 74)}L{P(32, 88)}L{P(-32, 88)}Z")
    leaves = []
    for k, a in enumerate((-62, -40, -18, 0, 18, 40, 62)):
        L = 92 if abs(a) < 30 else 80
        leaves.append(f'<path transform="translate({f(cx)} {f(cy - 64 * sc)}) rotate({a}) scale({f(sc)})" d="M0 0C-16 -18 -14 -{L * .7} 0 -{L}C14 -{L * .7} 16 -18 0 0Z"/>')
    leaf_g = s.lin([(0, "#2e5a22", 1), (1, "#7aa83a", 1)], 0, 1, 0, 0)
    veins = "".join(f'<path transform="translate({f(cx)} {f(cy - 64 * sc)}) rotate({a}) scale({f(sc)})" d="M0 -4V-{(92 if abs(a) < 30 else 80) * .92}" stroke="#d8e890" stroke-opacity=".5" stroke-width="1.4"/>'
                    for a in (-62, -40, -18, 0, 18, 40, 62))
    s.add(f'<g fill="{leaf_g}">{"".join(leaves)}</g>{veins}')
    s.add(f'<g filter="{s.gold_filter(5 * sc)}"><path d="{pot}" fill="{gold}"/></g>')
    # embossed bands
    s.add(f'<path d="M{P(-80, -6)}Q{P(0, 14)} {P(80, -6)}M{P(-82, 22)}Q{P(0, 42)} {P(82, 22)}" stroke="#7a4410" stroke-opacity=".5" stroke-width="{f(3 * sc)}" fill="none"/>'
          f'<path d="M{P(-80, -3)}Q{P(0, 17)} {P(80, -3)}M{P(-82, 25)}Q{P(0, 45)} {P(82, 25)}" stroke="#fff2c0" stroke-opacity=".55" stroke-width="{f(1.6 * sc)}" fill="none"/>')
    dots = "".join(f'<circle cx="{f(cx + x * sc)}" cy="{f(cy + (12 + 10 * (1 - (x / 80) ** 2)) * sc)}" r="{f(2.6 * sc)}" fill="#fff0b0" opacity=".8"/>' for x in range(-70, 71, 14))
    s.add(dots)
    # coconut
    cg = s.rad([(0, "#c88a4a", 1), (.7, "#7a4a22", 1), (1, "#3a2010", 1)], .4, .35, .7)
    s.add(f'<path d="M{P(-30, -72)}C{P(-34, -100)} {P(-14, -126)} {P(0, -132)}C{P(14, -126)} {P(34, -100)} {P(30, -72)}Z" fill="{cg}"/>'
          f'<path d="M{P(-6, -128)}C{P(-10, -138)} {P(-2, -146)} {P(0, -150)}C{P(2, -146)} {P(10, -138)} {P(6, -128)}Z" fill="#6a3e1a"/>'
          f'<path d="M{P(-20, -80)}Q{P(-18, -108)} {P(-4, -126)}M{P(-6, -78)}Q{P(-4, -110)} {P(2, -128)}M{P(10, -78)}Q{P(10, -106)} {P(6, -126)}" stroke="#2a1608" stroke-opacity=".4" stroke-width="{f(1.4 * sc)}" fill="none"/>'
          f'<path d="M{P(-32, -74)}Q{P(0, -64)} {P(32, -74)}" stroke="#c0202a" stroke-width="{f(5 * sc)}" fill="none"/>')


@scene
def kumbh(s):
    hz = 418
    sun = (800, 410)
    s.sky([(0, "#1a1c48"), (.16, "#33336a"), (.28, "#6e4e84"), (.36, "#c87e92"), (.4, "#f6ae94"), (.418, "#ffdcb0")])
    s.stars(40, 0, 200, seed=31, bright=.5)
    s.glow(sun[0], sun[1], 720, "#ff9e6a", .55, .18, sy=.5)
    s.glow(sun[0], sun[1] + 4, 200, "#fff0c8", .8, .3, sy=.35)
    s.fx("clouds", y0=230, y1=400, seed=111, cell=90, aniso=7, cover=.32, soft=.22, lit="#ffd6b0", body=.82, direct=.95,
         light=(0, 1), sun=(sun[0], sun[1], 400), opacity=.75)
    # far shore and camps
    far = ridgeline(hz, 10, 113, cell=200, octaves=4, ridged=.2)
    hills(s, far, "#9a6a8a", "#a87a8c")
    s.mist(hz - 2, 30, "#ffd0b0", .7, 8)
    s.fx("reflect", y0=hz, strength=.92, tint="#2a2040", tint_near=.45, tint_far=.04, amp=2.6)
    # the two waters: Ganga pale and silty, Yamuna deep blue-green
    seam = smooth_line([(800, 520), (790, 600), (760, 700), (720, 820), (680, 1010)], 6)
    seam_d = "L".join(f"{f(x)} {f(y)}" for x, y in seam)
    gan = f"M-40 {hz + 30}L770 {hz + 60}L{seam_d}L-40 1010Z"
    yam = f"M1640 {hz + 30}L830 {hz + 60}L800 520L{seam_d}L1640 1010Z"
    s.add(f'<path d="{gan}" fill="#e0c098" opacity=".2" style="mix-blend-mode:screen"/>'
          f'<path d="{yam}" fill="#3a5a68" opacity=".32" style="mix-blend-mode:multiply"/>'
          f'<path d="{yam}" fill="#3a7a78" opacity=".08" style="mix-blend-mode:screen"/>')
    s.add(f'<path d="M800 520L{seam_d}" stroke="#ffe8c8" stroke-opacity=".28" stroke-width="5" fill="none" filter="{s.blur(3)}"/>')
    s.fx("glints", y0=hz, cx=sun[0], color="#fff0c8", width=44, strength=1.0, scatter=.05, density=.5, spread=2.4)
    # sand flats: the spit between the rivers, and the near banks
    sand = s.lin([(0, "#d8a890", 1), (1, "#a87878", 1)], 0, hz, 0, 560, user=True)
    spit = smooth_line([(420, hz + 8), (600, hz + 24), (700, hz + 50), (780, 500), (800, 522), (830, 500), (920, hz + 44), (1100, hz + 18), (1300, hz + 8)], 5)
    s.add(f'<path d="{pts_d(spit)}" fill="{sand}"/>')
    s.add(f'<path d="M{"L".join(f"{f(x)} {f(y)}" for x, y in spit)}" stroke="#ffe6c8" stroke-opacity=".5" stroke-width="2" fill="none"/>')
    # tents and flags of the mela on the spit
    rng = random.Random(7)
    tents = []
    for k in range(70):
        x = rng.uniform(470, 1260)
        top_y = y_at(sorted(spit), x)
        if top_y - hz < 6:
            continue
        y = rng.uniform(hz + 4, top_y - 4)
        w = rng.uniform(5, 11) * (1 + (y - hz) / 80)
        c = rng.choice(["#f4e6d8", "#e8c8b0", "#f0a060", "#d87a50", "#fff0e0"])
        tents.append(f'<path d="M{f(x - w)} {f(y)}L{f(x)} {f(y - w * .8)}L{f(x + w)} {f(y)}Z" fill="{c}" opacity=".8"/>')
    for k in range(12):
        x = rng.uniform(500, 1200)
        y = hz + rng.uniform(6, 20)
        tents.append(f'<path d="M{f(x)} {f(y)}V{f(y - 26)}" stroke="#5a3a40" stroke-width="1.2"/><path d="M{f(x)} {f(y - 26)}l12 4l-12 4Z" fill="#f07a1e"/>')
    s.add("".join(tents))
    for k in range(14):
        s.glow(rng.uniform(480, 1250), hz + rng.uniform(8, 30), 10, "#ffb060", .8, .3)
    # pilgrims bathing at the meeting point
    for k in range(26):
        x = 800 + rng.uniform(-90, 90)
        y = 522 + rng.uniform(-6, 14)
        h = rng.uniform(7, 10)
        s.add(f'<path d="M{f(x - 2)} {f(y)}V{f(y - h)}H{f(x + 2)}V{f(y)}Z" fill="#2a1a2a"/><circle cx="{f(x)}" cy="{f(y - h - 2)}" r="2.2" fill="#2a1a2a"/>')
    near_l = smooth_line([(-40, 800), (100, 820), (230, 880), (320, 950), (360, 1010)], 6)
    near_r = smooth_line([(1640, 760), (1480, 790), (1360, 860), (1270, 940), (1240, 1010)], 6)
    bank = s.lin([(0, "#8a6070", 1), (.3, "#5a3c50", 1), (1, "#22141e", 1)], 0, 760, 0, 1000, user=True)
    for nb, edge_x in ((near_l, -40), (near_r, 1640)):
        d = pts_d(nb + [(edge_x, 1010)])
        s.add(f'<path d="{d}" fill="{bank}"/><path d="{d}" fill="#000" filter="{s.grain(.05, 3, .25, 3, "#000000")}" opacity=".5"/>')
        s.add(f'<path d="M{"L".join(f"{f(x)} {f(y)}" for x, y in nb)}" stroke="#ffd8b0" stroke-opacity=".6" stroke-width="2.4" fill="none"/>')
        s.add(f'<path d="{ribbon(nb, 30, 30)}" fill="#ffe8d0" opacity=".12" filter="{s.blur(6)}"/>')
    rng2 = random.Random(12)
    figs = []
    for k in range(18):
        side = rng2.random() < .5
        nb = near_l if side else near_r
        i = rng2.randint(2, len(nb) - 6)
        x, y = nb[i]
        x += (-1 if side else 1) * rng2.uniform(10, 120)
        y += rng2.uniform(14, 60)
        h = 26 + (y - 760) * .12
        c = "#1a0e18"
        figs.append(f'<path d="M{f(x - h * .14)} {f(y)}L{f(x - h * .1)} {f(y - h * .7)}Q{f(x)} {f(y - h * .8)} {f(x + h * .1)} {f(y - h * .7)}L{f(x + h * .14)} {f(y)}Z" fill="{c}"/>'
                    f'<circle cx="{f(x)}" cy="{f(y - h * .86)}" r="{f(h * .1)}" fill="{c}"/>')
        if rng2.random() < .3:
            figs.append(f'<path d="M{f(x + h * .3)} {f(y)}V{f(y - h * 1.8)}" stroke="{c}" stroke-width="1.6"/>' + arch.flag(x + h * .3, y - h * 1.8, h * .7, h * .36, "#f07a1e", seed=k))
    s.add("".join(figs))
    # boats gathered near the sangam
    for (x, y, sc, fl, ppl) in ((640, 560, .42, False, 3), (960, 575, .46, True, 3), (560, 640, .6, False, 4), (1060, 690, .7, True, 4), (880, 640, .52, True, 2)):
        m = s.mark()
        arch.boat(s, x, y, sc, color="#1c1220", rim="#ffc890", people=ppl, flip=fl)
        s.add(f'<path d="M{f(x - 40 * sc * (-1 if fl else 1))} {f(y - 6 * sc)}V{f(y - 90 * sc)}" stroke="#1c1220" stroke-width="{f(2.4 * sc)}"/>'
              + arch.flag(x - 40 * sc * (-1 if fl else 1), y - 90 * sc, 34 * sc, 18 * sc, "#f07a1e", seed=k))
        ob.reflect_since(s, m, y + 6 * sc, .3, 2, 60)
    s.birds(9, 560, 1050, 300, 380, color="#3a2440", s=(5, 9), seed=6, a=.8)
    # the kalash of amrita in the sky
    s.add(f'<g style="mix-blend-mode:screen" opacity=".5"><circle cx="800" cy="180" r="150" fill="none" stroke="#ffe0a0" stroke-opacity=".35" stroke-width="1.4"/>'
          f'<circle cx="800" cy="180" r="176" fill="none" stroke="#ffe0a0" stroke-opacity=".2" stroke-width="1"/></g>')
    s.rays(800, 180, n=22, length=420, width=.03, color="#ffe2a0", a=.22, seed=4, blur=5)
    kalash(s, 800, 190, .82)
    for k, (dx, dy, r) in enumerate(((-6, 300, 5), (10, 336, 4), (-2, 372, 3.2))):
        s.glow(800 + dx, dy, 26, "#ffe6a0", .8, .3)
        s.add(f'<path d="M{f(800 + dx)} {f(dy - r * 2.2)}C{f(800 + dx + r)} {f(dy - r * .4)} {f(800 + dx + r)} {f(dy + r)} {f(800 + dx)} {f(dy + r)}C{f(800 + dx - r)} {f(dy + r)} {f(800 + dx - r)} {f(dy - r * .4)} {f(800 + dx)} {f(dy - r * 2.2)}Z" fill="#fff6d8"/>')
    s.motes(40, 500, 1100, 60, 420, seed=8, size=(.7, 2))
    s.fx("godrays", cx=800, cy=200, strength=.3, thresh=.75, decay=.97, radius=220)
    s.fx("mottle", amp=.04, cell=60)
    return s


# =====================================================================================
# a raster sea: a perspective height field shaded by the sky, with foam and a warm light
# =====================================================================================
def _sea(img, y0, deep="#08101c", sky="#6a6a84", crest="#9aa4b0", foam="#eef2f0", seed=1, cell=16, aniso=4.0, chop=1.0,
         foam_amt=.5, light=None, light_c="#ffb050", light_r=300, light_a=.8, opacity=1.0, x0=0, x1=None, top_fade=0,
         y_end=None, sky_far="#a07a80", gloss=1.0):
    """Paint a wind-driven sea below the horizon y0. The waves are fbm noise laid out on the
    water plane (small and dense far off, large close by); faces turned towards the horizon
    mirror the sky, faces turned to us stay dark, high crests break into foam."""
    H_, W_, _ = img.shape
    x1 = W_ if x1 is None else x1
    y_end = H_ if y_end is None else y_end
    rows = y_end - y0
    d = np.arange(rows, dtype=np.float32)
    p = (d + 2) / (H_ - y0)
    v = np.log1p(d / 2.5) * 34
    nh = int(v.max()) + 10
    big = fx.fbm(nh, W_ + 200, cell * 3, 4, seed, aniso=aniso * 1.3)
    small = fx.fbm(nh, W_ + 200, cell, 5, seed + 7, aniso=aniso)
    yy = np.repeat(v[:, None], W_, 1)
    xx = np.tile(np.arange(W_, dtype=np.float32), (rows, 1))
    scale = (0.2 + 2.2 * p)[:, None]
    u = (xx - W_ / 2) / scale + W_ / 2 + 100
    hb = ndimage.map_coordinates(big, [yy, u], order=1, mode="reflect")
    hs = ndimage.map_coordinates(small, [yy, u], order=1, mode="reflect")
    h = hb * .6 + hs * .4 * chop
    h = (h - h.mean()) / (h.std() + 1e-6)
    # sharpen crests (trochoid-like): peaks narrow, troughs broad
    hc = np.tanh(h * .9)
    gy = np.gradient(hc, axis=0) * (1.5 / (0.15 + 2.5 * p[:, None]))
    gx = np.gradient(hc, axis=1) * (1.5 / (0.15 + 2.5 * p[:, None]))
    refl = np.clip(.5 - gy * 6, 0, 1) ** 1.4 * gloss  # faces towards the horizon mirror the sky
    tsky = np.clip(p[:, None] * 1.6, 0, 1)
    skyc = fx.rgb(sky_far) * (1 - tsky[..., None]) + fx.rgb(sky) * tsky[..., None]
    col = fx.rgb(deep) * (1 - refl[..., None]) + skyc * refl[..., None]
    col = col + (fx.rgb(crest) - col) * (np.clip(hc - .55, 0, 1) * .6)[..., None]
    # far water melts into the horizon haze
    hz_t = np.exp(-d / 26)[:, None, None]
    col = col * (1 - hz_t) + fx.rgb(sky_far) * hz_t
    # foam on the breaking crests, broken up by fine noise
    if foam_amt:
        fn = fx.fbm(nh, W_ + 200, max(2, cell * .3), 3, seed + 3, aniso=2)
        fz = ndimage.map_coordinates(fn, [yy, u], order=1, mode="reflect")
        fm = np.clip((hc - (1 - foam_amt * .55)) * 4, 0, 1) * fx.smooth(.45, .7, fz)
        fm = ndimage.gaussian_filter(fm, (.6, 1.2))
        col = col + (fx.rgb(foam) - col) * (fm * .85)[..., None]
    if light:
        lx, ly = light
        Y = (y0 + d)[:, None]
        dist2 = ((xx - lx) / 1.0) ** 2 + ((Y - ly) / .6) ** 2
        g = np.exp(-dist2 / (2 * light_r ** 2)) * light_a
        col = col + fx.rgb(light_c) * (g * (.35 + refl * .9 + np.clip(hc, 0, 1) * .4))[..., None]
    col = np.clip(col, 0, 1)
    a = np.ones((rows, W_), np.float32) * opacity
    if top_fade:
        a *= fx.smooth(0, top_fade, d)[:, None]
    if x0 > 0 or x1 < W_:
        xm = np.zeros(W_, np.float32)
        xm[int(x0):int(x1)] = 1
        xm = ndimage.gaussian_filter1d(xm, 30)
        a *= xm[None, :]
    reg = img[y0:y_end]
    img[y0:y_end] = reg * (1 - a[..., None]) + col * a[..., None]
    return img


fx.EFFECTS["sea"] = _sea


# =====================================================================================
# the ocean avatars: a sea of waves, the golden fish, the boat of the sages
# =====================================================================================
def wave_rows(s, hz, rows, seed=1, deep="#0c1a2a", crest="#2c4a5a", foam="#e8f0ec", foam_a=.5, y_end=1060, amp=(2, 70),
              light=None, light_r=500, light_c="#ffb050", light_a=.5, power=1.9, x_skip=None):
    """Rows of storm waves from the horizon to the viewer: each row's crest is lit, its trough
    dark, with broken foam along the top. light=(x, y) adds a warm glow cast on nearby water."""
    rng = random.Random(seed)
    for k in range(rows):
        t = (k + 1) / rows
        base = hz + (y_end - hz) * t ** power
        A = amp[0] + (amp[1] - amp[0]) * t ** 1.5
        lam = 40 + 520 * t ** 1.4
        ph = [rng.uniform(0, 6.28) for _ in range(4)]
        pts = []
        for x in range(-40, W + 44, 4):
            c = math.sin(x / lam * 6.28 + ph[0])
            c2 = math.sin(x / (lam * .43) * 6.28 + ph[1])
            c3 = math.sin(x / (lam * 2.3) * 6.28 + ph[2])
            v = ((c + 1) / 2) ** 2.2 * .7 + ((c2 + 1) / 2) ** 2 * .22 + (c3 + 1) / 2 * .25
            pts.append((x, base - A * v))
        d = pts_d(pts + [(W + 44, base + A + 400), (-40, base + A + 400)])
        g = s.lin([(0, crest, 1), (.35, mix(crest, deep, .6), 1), (1, deep, 1)], 0, base - A, 0, base + A * 1.6 + 30, user=True)
        out = [f'<path d="{d}" fill="{g}"/>']
        if light:
            lx, ly = light
            lg = s.rad([(0, light_c, light_a), (.5, light_c, light_a * .35), (1, light_c, 0)], lx, ly, light_r, user=True)
            out.append(f'<path d="{d}" fill="{lg}" style="mix-blend-mode:screen"/>')
        crestline = "M" + "L".join(f"{f(x)} {f(y)}" for x, y in pts)
        fw = 1 + 5 * t
        out.append(f'<path d="{crestline}" stroke="{foam}" stroke-opacity="{foam_a * (.4 + .6 * t):.2f}" stroke-width="{f(fw)}" fill="none" '
                   f'stroke-dasharray="{f(lam * .18)} {f(lam * .12)} {f(lam * .3)} {f(lam * .2)}" filter="{s.blur(.6 + t * 1.6)}"/>')
        # spray on the highest crests
        spray = []
        for i in range(2, len(pts) - 2):
            x, y = pts[i]
            if pts[i][1] < pts[i - 1][1] and pts[i][1] <= pts[i + 1][1] and (base - y) > A * .75 and rng.random() < .8:
                for _ in range(int(3 + 10 * t)):
                    sx_, sy_ = x + rng.gauss(0, 10 * t + 2), y - abs(rng.gauss(0, 10 * t + 2))
                    spray.append(f'<circle cx="{f(sx_)}" cy="{f(sy_)}" r="{f(rng.uniform(.5, 1.6) * (1 + t))}"/>')
        out.append(f'<g fill="{foam}" opacity="{foam_a * .8:.2f}" filter="{s.blur(.8 + t)}">{"".join(spray)}</g>')
        # lacy foam streaks on the back of the wave
        lace = []
        for _ in range(int(6 + 18 * t)):
            x = rng.uniform(-40, W + 40)
            y = y_at(pts, x) + rng.uniform(.2, 1.4) * A
            L = rng.uniform(.1, .35) * lam
            lace.append(f'<path d="M{f(x)} {f(y)}q{f(L * .5)} {f(-A * .08)} {f(L)} {f(A * .04)}"/>')
        out.append(f'<g stroke="{foam}" stroke-opacity="{foam_a * .35:.2f}" stroke-width="{f(.8 + t * 2)}" fill="none" filter="{s.blur(.5 + t)}">{"".join(lace)}</g>')
        s.add("".join(out))
    return


FISH_BODY = ("M300 0C300 -40 270 -80 200 -96C120 -114 20 -112 -60 -92C-140 -72 -210 -42 -262 -18L-270 -14L-270 14"
             "C-210 36 -140 62 -60 78C20 94 140 94 210 72C262 56 300 30 300 0Z")
FISH_TAIL = "M-258 -12C-300 -40 -342 -104 -376 -150C-352 -84 -346 -32 -330 0C-346 32 -352 84 -378 134C-338 92 -300 40 -258 12Z"
FISH_DORSAL = "M126 -104C90 -176 26 -206 -44 -196C-62 -160 -74 -124 -86 -84Z"
FISH_PECT = "M168 40C150 86 112 118 64 132C96 98 120 64 138 30Z"
FISH_ANAL = "M-118 66C-140 104 -172 128 -206 132C-184 100 -164 72 -150 54Z"
FISH_HORN = "M226 -84C232 -140 252 -190 292 -232C276 -186 262 -134 254 -86Z"


def golden_fish(s, x, y, sc=1.0, rot=-6, flip=False):
    """Matsya: a vast, luminous golden fish with a single horn. (x, y) is the middle of the body."""
    t = f"translate({f(x)} {f(y)}) rotate({rot}) scale({f(-sc if flip else sc)} {f(sc)})"
    s.glow(x, y - 30 * sc, 700 * sc, "#ffb040", .55, .18)
    s.glow(x + 120 * sc, y - 60 * sc, 260 * sc, "#ffe0a0", .55, .3)
    gold = s.lin([(0, "#fff4c8"), (.3, "#ffd06a"), (.65, "#e09a2a"), (1, "#9a5410")], 0, 0, .15, 1)
    fin = s.lin([(0, "#ffe6a0", .95), (1, "#ff9a3a", .55)], 0, 0, 0, 1)
    cid = s.clip(FISH_BODY)
    scales = []
    for row in range(-6, 8):
        for col in range(-14, 16):
            cx_ = col * 22 + (11 if row % 2 else 0)
            cy_ = row * 16
            scales.append(f"M{cx_ - 11} {cy_}A11 11 0 0 0 {cx_ + 11} {cy_}")
    inner = (f'<path d="{FISH_TAIL}" fill="{fin}"/>'
             f'<path d="{FISH_DORSAL}" fill="{fin}"/>'
             f'<path d="{FISH_ANAL}" fill="{fin}"/>'
             f'<g filter="{s.gold_filter(7)}"><path d="{FISH_BODY}" fill="{gold}"/></g>'
             f'<g clip-path="{cid}"><path d="{"".join(scales)}" stroke="#8a4a10" stroke-opacity=".35" stroke-width="2" fill="none"/>'
             f'<path d="{"".join(scales)}" stroke="#fff4c8" stroke-opacity=".25" stroke-width="1.2" fill="none" transform="translate(0 -2)"/>'
             f'<rect x="-280" y="-120" width="600" height="80" fill="{s.lin([(0, "#fffbe8", .55), (1, "#fffbe8", 0)], 0, 0, 0, 1)}"/>'
             f'<rect x="-280" y="30" width="600" height="80" fill="{s.lin([(0, "#7a3a08", 0), (1, "#7a3a08", .5)], 0, 0, 0, 1)}"/></g>'
             f'<path d="M172 -82C146 -34 146 30 174 74" stroke="#8a4a10" stroke-opacity=".6" stroke-width="4" fill="none"/>'
             f'<path d="M176 -82C150 -34 150 30 178 74" stroke="#fff0c0" stroke-opacity=".5" stroke-width="1.6" fill="none"/>'
             f'<path d="{FISH_PECT}" fill="{fin}"/>'
             f'<g stroke="#b86a18" stroke-opacity=".5" stroke-width="1.6" fill="none">'
             f'<path d="M-268 0L-360 -130M-268 0L-344 -60M-268 0L-338 0M-268 0L-344 60M-268 0L-362 118"/>'
             f'<path d="M110 -104L40 -186M80 -104L0 -194M50 -100L-30 -192M20 -96L-56 -170"/></g>'
             f'<path d="M298 8L262 12" stroke="#6a3008" stroke-width="2.6" fill="none" stroke-linecap="round"/>'
             f'<path d="M278 16C250 40 200 52 140 50" stroke="#ffe0a0" stroke-width="2.6" fill="none" stroke-linecap="round" opacity=".75"/>'
             f'<circle cx="240" cy="-32" r="9" fill="#5a2a08"/><circle cx="240" cy="-32" r="6" fill="#0c0602"/><circle cx="237.5" cy="-34.5" r="2.2" fill="#fff"/>'
             f'<g filter="{s.gold_filter(4)}"><path d="{FISH_HORN}" fill="{s.lin([(0, "#fff8e0"), (1, "#e8b050")], 0, 1, 0, 0)}"/></g>')
    s.add(f'<g transform="{t}">{inner}</g>')
    # horn tip in scene coordinates
    a = math.radians(rot)
    hx, hy = 286 * (-1 if flip else 1), -226
    return (x + (hx * math.cos(a) - hy * math.sin(a)) * sc, y + (hx * math.sin(a) + hy * math.cos(a)) * sc)


def ark(s, x, y, sc=1.0, color="#120e18", rim="#ffc890", lamp=True, flip=False):
    """Manu's boat: a high-prowed hull with a thatched shelter and the sages seated aboard.
    (x, y) is the waterline centre; returns the prow tip (where the rope is tied)."""
    hull = "M-130 -30C-110 -8 -60 4 0 4C60 4 112 -4 150 -44L158 -64L146 -48C120 -24 70 -14 0 -14C-60 -14 -100 -20 -124 -36Z"
    hull2 = "M-130 -30C-110 -8 -60 4 0 4C60 4 112 -4 150 -44C130 -10 70 12 0 14C-70 14 -114 2 -130 -30Z"
    hut = "M-70 -16C-72 -44 -50 -66 -20 -70C10 -66 30 -44 32 -16Z"
    sages = "".join(f'<circle cx="{px}" cy="-30" r="5.5"/><path d="M{px - 9} -14C{px - 10} -24 {px - 6} -26 {px} -26C{px + 6} -26 {px + 10} -24 {px + 9} -14Z"/>'
                    for px in (48, 66, 84, 102))
    inner = (f'<g fill="{color}"><path d="{hull2}"/><path d="{hull}"/><path d="{hut}"/>{sages}'
             f'<circle cx="-92" cy="-40" r="5.5"/><path d="M-100 -16C-101 -30 -97 -34 -92 -34C-87 -34 -83 -30 -84 -16Z"/></g>'
             f'<path d="M-68 -18C-70 -44 -48 -64 -20 -68M-50 -56L-60 -20M-30 -64L-36 -18M-8 -64L-6 -18M12 -54L18 -18" stroke="#3a2a28" stroke-width="1.6" fill="none"/>'
             f'<path d="M-130 -30C-110 -8 -60 4 0 4C60 4 112 -4 150 -44L158 -64" stroke="{rim}" stroke-width="2" fill="none" opacity=".75"/>'
             f'<path d="M-20 -70C10 -66 30 -44 32 -16" stroke="{rim}" stroke-width="1.6" fill="none" opacity=".6"/>')
    if lamp:
        inner += f'<ellipse cx="-20" cy="-26" rx="16" ry="9" fill="#ffb050" opacity=".9"/>'
    s.add(f'<g transform="translate({f(x)} {f(y)}) scale({f(-sc if flip else sc)} {f(sc)})">{inner}</g>')
    if lamp:
        s.glow(x - 20 * sc * (-1 if flip else 1), y - 26 * sc, 60 * sc, "#ff9a40", .6, .3)
    return (x + 156 * sc * (-1 if flip else 1), y - 62 * sc)


def choppy(s, y0, y1, n, seed=1, crest="#4a5a6a", foam="#eef2f0", shade="#060c16", light=None, light_c="#ffc060", light_r=500,
           size=(10, 160), foam_a=.7, x0=-60, x1=W + 60):
    """A choppy sea as many separate wave crests, small at the horizon and big close by.
    Each crest has a lit face, a dark trough below and a lace of foam on top."""
    rng = random.Random(seed)
    items = []
    for _ in range(n):
        t = rng.random() ** 1.6
        y = y0 + (y1 - y0) * t
        w = size[0] + (size[1] - size[0]) * t
        items.append((y, rng.uniform(x0, x1), w * rng.uniform(.6, 1.4), t))
    items.sort()
    out = []
    for y, x, w, t in items:
        h = w * rng.uniform(.16, .3)
        k = rng.uniform(-.25, .25)
        d = (f"M{f(x - w)} {f(y)}C{f(x - w * .5)} {f(y - h * .2)} {f(x - w * .25 + k * w)} {f(y - h)} {f(x + k * w)} {f(y - h * 1.04)}"
             f"C{f(x + w * .3 + k * w)} {f(y - h * .95)} {f(x + w * .55)} {f(y - h * .2)} {f(x + w)} {f(y)}Z")
        lit = 0.0
        if light:
            lx, ly = light
            lit = math.exp(-(((x - lx) ** 2 + (y - ly) ** 2) / (2 * light_r ** 2)))
        c = mix(crest, light_c, lit * .55)
        g = s.lin([(0, c, 1), (1, mix(c, shade, .7), 1)], 0, y - h, 0, y, user=True)
        out.append(f'<path d="M{f(x - w * 1.05)} {f(y + h * .1)}Q{f(x)} {f(y + h * .7)} {f(x + w * 1.05)} {f(y + h * .1)}" stroke="{shade}" stroke-opacity=".35" stroke-width="{f(h * .5)}" fill="none" filter="{s.blur(max(1, h * .25))}"/>')
        out.append(f'<path d="{d}" fill="{g}"/>')
        fa = foam_a * rng.uniform(.4, 1) * (.5 + .5 * t)
        out.append(f'<path d="M{f(x - w * .35 + k * w)} {f(y - h * .8)}Q{f(x + k * w)} {f(y - h * 1.1)} {f(x + w * .4 + k * w)} {f(y - h * .6)}" stroke="{mix(foam, light_c, lit * .5)}" stroke-opacity="{fa:.2f}" stroke-width="{f(1 + h * .12)}" fill="none" stroke-linecap="round"/>')
        if t > .35 and rng.random() < .5:
            spr = "".join(f'<circle cx="{f(x + k * w + rng.gauss(0, w * .15))}" cy="{f(y - h - abs(rng.gauss(0, h * .4)))}" r="{f(rng.uniform(.6, 1.8) * (1 + t))}"/>' for _ in range(int(4 + 8 * t)))
            out.append(f'<g fill="{foam}" opacity="{fa * .8:.2f}">{spr}</g>')
    s.add("".join(out))


def rain(s, n, seed=1, angle=12, a=.18, color="#c8d4e0", y0=0, y1=1000, length=(30, 90)):
    rng = random.Random(seed)
    dx = math.tan(math.radians(angle))
    out = []
    for _ in range(n):
        x, y, L = rng.uniform(-100, W + 100), rng.uniform(y0, y1), rng.uniform(*length)
        out.append(f"M{f(x)} {f(y)}l{f(-dx * L)} {f(L)}")
    s.add(f'<path d="{"".join(out)}" stroke="{color}" stroke-opacity="{a}" stroke-width="1.2" filter="{s.blur(.6)}"/>')


@scene
def matsya(s):
    hz = 470
    rift = (1240, 440)
    s.sky([(0, "#080c18"), (.2, "#141a2c"), (.36, "#262a40"), (.43, "#5a4a5e"), (.47, "#b07a74")])
    s.glow(rift[0], rift[1], 600, "#ff9a6a", .42, .2, sy=.3)
    s.glow(rift[0], rift[1] + 20, 240, "#ffd0a0", .55, .3, sy=.22)
    s.fx("clouds", y0=0, y1=455, seed=121, cell=210, aniso=2.6, cover=.8, soft=.16, lit="#6a6a84", shade="#10141f", body=.55,
         direct=.65, light=(.5, 1), sun=(rift[0], rift[1], 380), rim="#ffc8a0", rim_a=.85, opacity=1, top_fade=0, bottom_fade=.25)
    s.fx("clouds", y0=20, y1=330, seed=124, cell=120, aniso=3, cover=.45, soft=.18, lit="#4a4a62", shade="#0c101c", body=.5,
         direct=.55, light=(.4, 1), opacity=.85)
    s.add(f'<path d="M250 110L272 180L256 186L292 276L276 282L312 372" stroke="#e8eeff" stroke-width="2.4" fill="none" filter="{s.blur(1)}"/>'
          f'<path d="M272 180L240 220M276 282L254 320" stroke="#e8eeff" stroke-width="1.2" fill="none" opacity=".7"/>')
    s.glow(280, 240, 280, "#a8b8ff", .28, .2)
    fish_c = (880, 640)
    sea = dict(y0=hz, deep="#060c18", sky="#4a5068", sky_far="#8a6a74", crest="#6a7888", foam="#dfe6e8", seed=7, cell=14, aniso=3.2,
               chop=1.2, foam_amt=.55, light=(fish_c[0], fish_c[1] - 20), light_c="#ffa840", light_r=260, light_a=.7)
    s.fx("sea", **sea)
    # the boat behind, on its long rope
    bx, by = 420, 600
    m = s.mark()
    prow = ark(s, bx, by, .9, rim="#ffc890")
    ob.reflect_since(s, m, by + 4, .2, 2, 40)
    horn = golden_fish(s, fish_c[0], fish_c[1], 1.28, rot=-9)
    # the sea closes over the fish's flanks; it glows up through the water
    surf = 608
    s.fx("sea", **dict(sea, y0=surf, opacity=.72, top_fade=26, light_a=.9))
    s.glow(fish_c[0] + 40, fish_c[1] + 30, 440, "#ffb040", .38, .25, sy=.38)
    s.add(f'<path d="M{fish_c[0] - 380} {surf + 6}Q{fish_c[0]} {surf - 6} {fish_c[0] + 420} {surf - 34}" stroke="#fff4dc" stroke-width="6" stroke-opacity=".5" fill="none" filter="{s.blur(4)}"/>')
    s.motes(60, fish_c[0] + 220, fish_c[0] + 480, surf - 120, surf, color="#fff0d0", seed=11, size=(.8, 2.2))
    s.add(f'<path d="M{f(prow[0])} {f(prow[1])}Q{f((prow[0] + horn[0]) / 2)} {f(min(prow[1], horn[1]) + 40)} {f(horn[0])} {f(horn[1])}" stroke="#1a1008" stroke-width="3.4" fill="none"/>'
          f'<path d="M{f(prow[0])} {f(prow[1])}Q{f((prow[0] + horn[0]) / 2)} {f(min(prow[1], horn[1]) + 40)} {f(horn[0])} {f(horn[1])}" stroke="#ffd890" stroke-width="1.2" fill="none" opacity=".6" transform="translate(0 -1.5)"/>')
    rain(s, 300, seed=4, angle=14, a=.1)
    s.fx("mottle", amp=.05, cell=60)
    s.look = {"vibrance": .08, "contrast": 1.08}
    return s


# =====================================================================================
# 8. Kurma and the churning of the ocean of milk
# =====================================================================================
def _chevrons(pts, w, color):
    """Overlapping scale marks along a serpent's back, pointing back along the body."""
    out = []
    acc, step = 0.0, w * .34
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        L = math.hypot(xb - xa, yb - ya)
        if L == 0:
            continue
        ux, uy = (xb - xa) / L, (yb - ya) / L
        nx, ny = -uy, ux
        t = step - acc
        while t <= L:
            cx_, cy_ = xa + ux * t, ya + uy * t - w * .08
            for side in (-1, 1):
                ex, ey = cx_ - ux * w * .16 + nx * side * w * .3, cy_ - uy * w * .16 + ny * side * w * .3
                out.append(f"M{f(cx_)} {f(cy_)}L{f(ex)} {f(ey)}")
            t += step
        acc = (acc + L) % step
    return f'<path d="{"".join(out)}" stroke="{color}" stroke-width="{f(w * .07)}" stroke-opacity=".5" fill="none" stroke-linecap="round"/>'


def serpent_stroke(s, pts, w, body="#163c3c", mid="#2e6a62", belly="#e6c47a", hi="#b8f0d8", scale_c="#071a18", rim=None, rim_a=.7,
                   taper=None):
    """A serpent's body along a polyline: dark iridescent back, a cream-gold belly showing
    underneath, fine scales and a glossy highlight; taper narrows the last part."""
    if len(pts) < 2:
        return
    def dd(p):
        return "M" + "L".join(f"{f(x)} {f(y)}" for x, y in p)
    out = []
    pieces = [(pts, w)]
    if taper:
        n = len(pts)
        cut = int(n * (1 - taper))
        pieces = [(pts[:cut + 1], w)] + [(pts[cut + k:cut + k + 2], w * (1 - k / (n - cut)) + 2) for k in range(n - cut - 1)]
    for p_, ww in pieces:
        d = dd(p_)
        out.append(f'<path d="{d}" stroke="#040a0a" stroke-opacity=".55" stroke-width="{f(ww * 1.14)}" fill="none" stroke-linecap="round" stroke-linejoin="round" transform="translate(0 {f(ww * .14)})" filter="{s.blur(ww * .1)}"/>')
    for p_, ww in pieces:
        d = dd(p_)
        out.append(f'<path d="{d}" stroke="{body}" stroke-width="{f(ww)}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    for p_, ww in pieces:
        d = dd(p_)
        out.append(f'<path d="{d}" stroke="{belly}" stroke-width="{f(ww * .26)}" fill="none" stroke-linecap="round" transform="translate(0 {f(ww * .33)})" opacity=".85"/>'
                   f'<path d="{d}" stroke="{mid}" stroke-width="{f(ww * .5)}" fill="none" stroke-linecap="round" transform="translate(0 {f(-ww * .12)})" filter="{s.blur(ww * .08)}"/>'
                   + _chevrons(p_, ww, scale_c) +
                   f'<path d="{d}" stroke="{hi}" stroke-width="{f(ww * .12)}" fill="none" stroke-linecap="round" opacity=".45" transform="translate(0 {f(-ww * .26)})" filter="{s.blur(ww * .05)}"/>')
        if rim:
            out.append(f'<path d="{d}" stroke="{rim}" stroke-width="{f(ww * .07)}" fill="none" opacity="{rim_a}" transform="translate(0 {f(-ww * .44)})" filter="{s.blur(ww * .04)}"/>')
    s.add("".join(out))


@scene
def kurma(s):
    hz = 640
    glow_c = (800, 260)
    s.sky([(0, "#0e0e2c"), (.2, "#22205a"), (.4, "#4a3a7e"), (.54, "#a06a9a"), (.61, "#f0b0a0"), (.64, "#ffe0c0")])
    s.stars(90, 0, 360, seed=41, bright=.75)
    s.glow(glow_c[0], glow_c[1], 800, "#ffb070", .55, .2)
    s.glow(glow_c[0], glow_c[1] - 30, 280, "#fff0c8", .75, .3)
    s.rays(glow_c[0], glow_c[1] - 40, n=30, length=1000, width=.03, color="#ffe2a8", a=.2, seed=3, blur=8)
    s.fx("clouds", y0=300, y1=620, seed=141, cell=120, aniso=5, cover=.42, soft=.2, lit="#ffc8a8", body=.75, direct=.9,
         light=(0, -1), sun=(glow_c[0], glow_c[1], 480), opacity=.85)
    s.fx("clouds", y0=10, y1=230, seed=145, cell=170, aniso=3.5, cover=.38, soft=.2, lit="#b88ab0", body=.7, direct=.7,
         light=(0, 1), sun=(glow_c[0], glow_c[1], 500), opacity=.75)
    # the ocean of milk: pearly, opalescent
    s.fx("sea", y0=hz, deep="#3e3c6c", sky="#b8a8cc", sky_far="#f4cfc4", crest="#ece4f0", foam="#fbf6f4", seed=23, cell=34,
         aniso=2.0, chop=.6, foam_amt=.22, light=(800, hz + 30), light_c="#ffc890", light_r=260, light_a=.35, gloss=.85)
    s.fx("glints", y0=hz, cx=800, color="#fff0d0", width=70, strength=1.0, scatter=.08, density=.5, spread=2.4)
    # Kurma's shell rising from the milk
    sx, sy, srx, sry = 800, 668, 440, 128
    dome = f"M{sx - srx} {sy}C{sx - srx} {sy - sry * 1.05} {sx - srx * .5} {sy - sry * 1.25} {sx} {sy - sry * 1.25}C{sx + srx * .5} {sy - sry * 1.25} {sx + srx} {sy - sry * 1.05} {sx + srx} {sy}Z"
    s.add(f'<path d="{dome}" fill="{s.rad([(0, "#8a8262", 1), (.45, "#4e4a3a", 1), (1, "#1c1a1e", 1)], .5, .05, .9)}"/>')
    top_y = sy - sry * 1.25
    scutes = []
    for j in range(-3, 4):
        x_top = sx + j * srx * .2
        x_bot = sx + j * srx * .34
        scutes.append(f"M{f(x_top)} {f(top_y - 4)}Q{f((x_top + x_bot) / 2 + j * 10)} {f(sy - sry * .55)} {f(x_bot)} {f(sy + 4)}")
    for t in (.42, .72):
        yy = top_y + (sy - top_y) * t
        scutes.append(f"M{f(sx - srx)} {f(yy + sry * .5)}Q{sx} {f(yy - sry * .25)} {f(sx + srx)} {f(yy + sry * .5)}")
    sd = "".join(scutes)
    s.add(f'<g clip-path="{s.clip(dome)}"><path d="{sd}" stroke="#14120e" stroke-opacity=".55" stroke-width="7" fill="none" filter="{s.blur(2.5)}"/>'
          f'<path d="{sd}" stroke="#d8c890" stroke-opacity=".22" stroke-width="2" fill="none" transform="translate(3 -3)"/>'
          f'<ellipse cx="{sx}" cy="{sy - sry}" rx="{srx * .7}" ry="{sry * .3}" fill="#fff0c8" opacity=".18" filter="{s.blur(18)}"/></g>')
    s.add(f'<path d="M{sx - srx} {sy}C{sx - srx} {sy - sry * 1.05} {sx - srx * .5} {sy - sry * 1.25} {sx} {sy - sry * 1.25}C{sx + srx * .5} {sy - sry * 1.25} {sx + srx} {sy - sry * 1.05} {sx + srx} {sy}" stroke="#ffe8b8" stroke-opacity=".55" stroke-width="3" fill="none" filter="{s.blur(1.4)}"/>')
    # Mandara, resting on the shell
    base = sy - sry * 1.08
    pk = peak_line(base, [(800, 330, 230, 0), (690, 210, 150, 0), (915, 230, 160, 0)], 143, detail=.26, x0=520, x1=1080, step=3,
                   shape=1.25, shoulders=2)
    pk = [(x, min(y, base)) for x, y in pk]
    def half_w(y):
        xs = [x for x, yy in pk if yy <= y]
        return (max(xs) - min(xs)) / 2 if xs else 0
    coil = []
    turns = 2.25
    y_lo, y_hi = base - 18, 300
    N = 600
    for k in range(N + 1):
        t = k / N
        th = math.pi + 2 * math.pi * turns * t
        yc = y_lo + (y_hi - y_lo) * t
        R = half_w(yc) + 14
        coil.append((800 + R * math.cos(th), yc + R * .22 * math.sin(th), math.sin(th)))
    def segs(front):
        out, cur = [], []
        for x, y, sn in coil:
            if (sn > -.02) == front:
                cur.append((x, y))
            elif cur:
                out.append(cur); cur = []
        if cur:
            out.append(cur)
        return out
    snake = dict(rim="#ffe6b8", rim_a=.8, body="#10202c", mid="#1c3a48", belly="#5a5038", hi="#8ac8d0", scale_c="#4a7a80")
    tw = 32
    for sg in segs(False):
        serpent_stroke(s, sg, tw * .9, body="#0c1822", mid="#142a36", belly="#3a3428", hi="#4a7a80", scale_c="#2a4a50", rim=None)
    mk = s.mark()
    mountains(s, pk, "#4a3e68", "#2c2446", lit="#f2b4a4", lit_a=.75, light=1, seed=144, rim="#fff0c8", rim_a=.95, rim_center=glow_c,
              rim_r=600, rim_w=2.2, base_y=base, haze="#c8a0b8", haze_a=.4, haze_h=80)
    pines(s, 560, 1040, 0, 60, h=(10, 24), color="#1a1630", seed=8, ground_fn=lambda x: y_at(pk, x) + 30 + abs(x - 800) * .04)
    inner = "".join(s.body[mk:])
    del s.body[mk:]
    s.add(f'<g clip-path="{s.clip(f"M0 0H1600V{f(base + 2)}H0Z")}">{inner}</g>')
    s.mist(base + 4, 30, "#ffe8d8", .55, 8, x0=560, x1=1040)
    for sg in segs(True):
        serpent_stroke(s, sg, tw, **snake)
    # both ends drawn taut towards the two horizons, where the gods and the asuras pull
    x0_, y0_, _ = coil[0]
    left = [(x0_ + (150 - x0_) * t, y0_ + (560 - y0_) * t + 20 * math.sin(math.pi * t)) for t in [k / 40 for k in range(41)]]
    left += smooth_line([(150, 560), (110, 548), (92, 500), (104, 448)], 4)[1:]
    x1_, y1_, _ = coil[-1]
    right = [(x1_ + (1700 - x1_) * t, y1_ + (470 - y1_) * t + 30 * math.sin(math.pi * t)) for t in [k / 40 for k in range(41)]]
    serpent_stroke(s, left, tw, **snake)
    hood = ("M104 470C96 450 74 420 64 384C56 352 58 322 76 306C86 298 96 296 104 296C112 296 122 298 132 306C150 322 152 352 144 384C134 420 112 450 104 470Z"
            "M90 300C88 284 96 274 104 274C112 274 120 284 118 300C114 308 94 308 90 300Z")
    s.add(f'<path d="{hood}" fill="#0e1a24" transform="translate(-3 2)" opacity="0"/>'
          f'<g transform="translate(-2.5 -2)"><path d="{hood}" fill="#ffe6b8" opacity=".85"/></g><path d="{hood}" fill="#10202c"/>'
          f'<path d="M104 452C90 436 78 410 76 380C76 352 88 330 104 322C120 330 132 352 132 380C130 410 118 436 104 452Z" fill="#1c3a48" opacity=".55"/>'
          f'<circle cx="98" cy="286" r="2.4" fill="#ffd070"/><circle cx="110" cy="286" r="2.4" fill="#ffd070"/>')
    serpent_stroke(s, right, tw * .9, **snake)
    # Kurma's head and a flipper breaking the milk
    head = "M110 0C80 -30 30 -44 -20 -46C-46 -48 -72 -42 -88 -30C-100 -20 -100 -6 -90 2L-72 6C-50 12 -20 10 20 14C60 18 90 16 110 12Z"
    s.add(f'<g transform="translate(372 672) scale(1.6)"><g transform="translate(-2 -1.5)"><path d="{head}" fill="#ffe6b8" opacity=".8"/></g>'
          f'<path d="{head}" fill="{s.lin([(0, "#6a6650", 1), (1, "#22201e", 1)], 0, 0, 0, 1)}"/>'
          f'<path d="M-24 -44C-18 -32 0 -24 24 -26M8 -40C14 -30 30 -24 50 -26" stroke="#3a3c3a" stroke-width="2" fill="none"/>'
          f'<path d="M-98 -10L-76 -6" stroke="#3a3c3a" stroke-width="2" fill="none"/>'
          f'<circle cx="-58" cy="-26" r="3.4" fill="#ffd890"/></g>')
    s.add(f'<path d="M1210 690C1270 664 1350 672 1400 706C1350 704 1290 708 1230 714Z" fill="#1a1c20"/>'
          f'<path d="M1210 690C1270 664 1350 672 1400 706" stroke="#ffe6b8" stroke-opacity=".7" stroke-width="2" fill="none"/>')
    rng = random.Random(9)
    churn = []
    for j in range(5):
        rx, ry = srx + 40 + j * 90, sry * .45 + 10 + j * 26
        churn.append(f'<ellipse cx="{sx}" cy="{f(sy + 6 + j * 6)}" rx="{f(rx)}" ry="{f(ry)}" fill="none" stroke="#ffffff" stroke-opacity="{.38 - j * .06:.2f}" stroke-width="{6 + j * 3}"/>')
    s.add(f'<g filter="{s.blur(7)}">{"".join(churn)}</g>')
    spray = "".join(f'<circle cx="{f(sx + rng.uniform(-1, 1) * (srx + 60))}" cy="{f(sy + rng.uniform(-30, 16))}" r="{f(rng.uniform(1, 3))}"/>' for _ in range(160))
    s.add(f'<g fill="#fffaf4" opacity=".7" filter="{s.blur(.8)}">{spray}</g>')
    s.add(f'<ellipse cx="{sx}" cy="{sy + 2}" rx="{srx + 30}" ry="20" fill="#ffffff" opacity=".6" filter="{s.blur(9)}"/>')
    s.motes(50, 400, 1200, 100, 600, seed=4, size=(.8, 2))
    s.fx("godrays", cx=glow_c[0], cy=glow_c[1] - 30, strength=.35, thresh=.75, decay=.97, radius=300)
    s.fx("mottle", amp=.045, cell=60)
    return s


# =====================================================================================
# 9. Hanuman's leap
# =====================================================================================
def hanuman(x, y, sc=1.0, color="#120a10", rim=None, rim_off=(-3, 2), rot=-12):
    """Hanuman in flight, as a respectful silhouette: a powerful body stretched out heading
    right, the near fist thrust forward, the mace held over the shoulder, legs trailing and the
    tail curling up behind. (x, y) is the middle of the body; about 500 wide at sc=1."""
    def body(c, e=0.0):
        return (
            f'<g fill="{c}" stroke="{c}" stroke-linecap="round" stroke-linejoin="round">'
            f'<path d="M-26 -24C-70 -60 -104 -116 -104 -164C-104 -204 -74 -222 -50 -210C-32 -200 -36 -178 -54 -176" stroke-width="{12 + e}" fill="none"/>'
            f'<path d="M-12 -2L-108 4L-196 -2" stroke-width="{30 + e}" fill="none"/>'
            f'<path d="M-196 -2L-226 -10" stroke-width="{15 + e}" fill="none"/>'
            f'<path d="M-12 10L-86 38L-150 -4" stroke-width="{28 + e}" fill="none"/>'
            f'<path d="M-150 -4L-170 -24" stroke-width="{15 + e}" fill="none"/>'
            f'<path d="M14 -34C-30 -36 -74 -34 -110 -18C-124 -26 -140 -40 -160 -40C-146 -20 -132 0 -118 14C-90 34 -50 40 -16 36C4 34 14 28 16 20Z" stroke-width="{e}"/>'
            f'<path d="M136 -40C110 -46 70 -44 30 -36C6 -32 -14 -30 -26 -26L-26 24C0 24 26 22 52 28C84 34 112 32 128 18C140 6 144 -18 136 -40Z" stroke-width="{e}"/>'
            f'<path d="M124 -42C90 -66 50 -58 10 -80C-30 -102 -70 -96 -110 -118C-96 -86 -60 -70 -20 -60C30 -48 74 -36 116 -28Z" stroke-width="{e}"/>'
            f'<path d="M126 -24L148 -32" stroke-width="{24 + e}"/>'
            f'<circle cx="152" cy="-36" r="{21 + e / 2}" stroke="none"/>'
            f'<ellipse cx="172" cy="-26" rx="{17 + e / 2}" ry="{12 + e / 2}" stroke="none"/>'
            f'<path d="M134 -50L170 -54L168 -62L136 -58Z" stroke-width="{2 + e}"/>'
            f'<path d="M138 -58C136 -76 144 -92 154 -100C162 -92 168 -76 166 -62Z" stroke-width="{e}"/>'
            f'<path d="M153 -100L154 -112" stroke-width="{3 + e}"/>'
            f'<path d="M118 4L186 12L248 -2" stroke-width="{22 + e}" fill="none"/>'
            f'<circle cx="262" cy="-4" r="{15 + e / 2}" stroke="none"/>'
            f'<path d="M104 -34L92 -88L126 -118" stroke-width="{20 + e}" fill="none"/>'
            f'<path d="M144 -104L44 -192" stroke-width="{9 + e}" fill="none"/>'
            f'<circle cx="150" cy="-99" r="{6 + e / 2}" stroke="none"/>'
            f'<circle cx="26" cy="-208" r="{36 + e / 2}" stroke="none"/>'
            f'<path d="M4 -234L-8 -258L16 -244Z" stroke-width="{3 + e}"/>'
            f'<circle cx="126" cy="-118" r="{12 + e / 2}" stroke="none"/>'
            f'</g>')
    inner = ""
    if rim:
        inner += f'<g transform="translate({rim_off[0]} {rim_off[1]})">{body(rim, 0)}</g>'
    inner += body(color)
    inner += (f'<path d="M-8 -214Q26 -198 60 -214M-6 -200Q26 -184 58 -200" stroke="#ffcf8a" stroke-opacity=".3" stroke-width="2.4" fill="none"/>'
              f'<circle cx="12" cy="-222" r="10" fill="#ffd8a0" opacity=".16"/>')
    return f'<g transform="translate({f(x)} {f(y)}) rotate({rot}) scale({f(sc)})">{inner}</g>'


def lanka(s, cx, base, sc=1.0, seed=1):
    """The golden city on Trikuta hill: towers, domes and spires catching the dawn."""
    rng = random.Random(seed)
    hillp = peak_line(base, [(cx, 110 * sc, 300 * sc), (cx - 160 * sc, 60 * sc, 160 * sc), (cx + 170 * sc, 70 * sc, 170 * sc)], seed,
                      detail=.1, x0=cx - 460 * sc, x1=cx + 460 * sc, step=3, shape=1.2, shoulders=1)
    s.add(f'<path d="{pts_d(hillp + [(cx + 460 * sc, base + 6), (cx - 460 * sc, base + 6)])}" fill="{s.lin([(0, "#8a5a5a", 1), (1, "#5a3a4a", 1)], 0, base - 110 * sc, 0, base, user=True)}"/>')
    gold = s.lin([(0, "#fff2c0", 1), (.5, "#ffc860", 1), (1, "#c8782a", 1)], 0, base - 260 * sc, 0, base, user=True)
    d = []
    for k in range(26):
        x = cx + rng.gauss(0, 150 * sc)
        g = y_at(hillp, x)
        h = rng.uniform(30, 90) * sc * (1.4 if abs(x - cx) < 80 * sc else 1)
        w = rng.uniform(8, 18) * sc
        kind = rng.random()
        if kind < .45:   # spire
            d.append(f"M{f(x - w)} {f(g + 4)}V{f(g - h * .5)}C{f(x - w)} {f(g - h * .8)} {f(x - w * .3)} {f(g - h)} {f(x)} {f(g - h * 1.15)}C{f(x + w * .3)} {f(g - h)} {f(x + w)} {f(g - h * .8)} {f(x + w)} {f(g - h * .5)}V{f(g + 4)}Z")
        elif kind < .8:  # domed tower
            d.append(f"M{f(x - w)} {f(g + 4)}V{f(g - h * .7)}H{f(x + w)}V{f(g + 4)}Z")
            d.append(f"M{f(x - w * 1.1)} {f(g - h * .7)}C{f(x - w * 1.1)} {f(g - h * 1.05)} {f(x + w * 1.1)} {f(g - h * 1.05)} {f(x + w * 1.1)} {f(g - h * .7)}Z")
            d.append(f"M{f(x - 1)} {f(g - h * .98)}V{f(g - h * 1.12)}H{f(x + 1)}V{f(g - h * .98)}Z")
        else:            # wall block
            d.append(f"M{f(x - w * 2)} {f(g + 4)}V{f(g - h * .35)}H{f(x + w * 2)}V{f(g + 4)}Z")
    s.add(f'<path d="{"".join(d)}" fill="{gold}"/>')
    s.add(f'<path d="{"".join(d)}" fill="#7a3a20" opacity=".25" transform="translate(3 0)" clip-path="{s.clip("".join(d))}"/>')
    s.glow(cx, base - 60 * sc, 360 * sc, "#ffc060", .5, .25, sy=.5)


@scene
def leap(s):
    hz = 640
    sun = (330, 600)
    s.sky([(0, "#1a1e4c"), (.2, "#33346c"), (.38, "#7a5a8e"), (.5, "#e08e8a"), (.6, "#ffc090"), (.64, "#ffe6c0")])
    s.stars(30, 0, 160, seed=51, bright=.4)
    s.sun(*sun, 40, halo_r=760, halo_a=.85)
    s.fx("clouds", y0=40, y1=360, seed=151, cell=170, aniso=3.6, cover=.42, soft=.2, lit="#ffbca0", body=.72, direct=.85,
         light=(-.6, 1), sun=(sun[0], sun[1], 520), opacity=.9)
    s.fx("clouds", y0=430, y1=620, seed=152, cell=90, aniso=6, cover=.36, soft=.22, lit="#ffe0b8", body=.85, direct=.95,
         light=(-.4, 1), sun=(sun[0], sun[1], 440), opacity=.85)
    lanka(s, 1330, hz, .8, seed=5)
    s.mist(hz - 4, 30, "#ffd0b0", .5, 8)
    s.fx("sea", y0=hz, deep="#2a1e3e", sky="#7a5a8a", sky_far="#ffc8a8", crest="#c89aa8", foam="#ffeede", seed=19, cell=14,
         aniso=4.5, chop=.8, foam_amt=.25, light=(sun[0], hz + 40), light_c="#ffc070", light_r=220, light_a=.6, gloss=1.1)
    s.fx("glints", y0=hz, cx=sun[0], color="#fff0c8", width=60, strength=1.2, scatter=.05, density=.5, spread=2.6)
    # the cliff of Mahendra mountain he leapt from
    cliff = smooth_line([(-60, 560), (40, 548), (120, 570), (170, 640), (200, 760), (230, 860), (300, 1010)], 6)
    s.add(f'<path d="{pts_d(cliff + [(-60, 1010)])}" fill="#120c18"/>')
    s.add(f'<path d="M{"L".join(f"{f(x)} {f(y)}" for x, y in cliff)}" stroke="#ffbf90" stroke-opacity=".7" stroke-width="2.4" fill="none"/>')
    pines(s, -40, 130, 0, 6, h=(40, 90), color="#120c18", seed=3, ground_fn=lambda x: y_at(cliff, x))
    s.birds(7, 1000, 1250, 470, 540, color="#4a2a44", s=(5, 9), seed=6, a=.8)
    # Hanuman in mid-leap, high over the sea
    s.glow(800, 340, 420, "#ffd8a0", .22, .2)
    s.add(hanuman(790, 370, 1.22, color="#140c14", rim="#ffd8a0", rim_off=(-4, 3), rot=-12))
    s.wisps(8, 300, 760, 360, 470, "#fff0e0", a=(.08, .18), length=(200, 420), thick=(3, 8), blur=4, seed=8)
    s.motes(30, 500, 1200, 200, 600, seed=4, size=(.7, 1.8))
    s.fx("godrays", cx=sun[0], cy=sun[1], strength=.4, thresh=.7, decay=.972, radius=280)
    s.fx("mottle", amp=.045, cell=60)
    return s


# =====================================================================================
# 10. many paths up one mountain
# =====================================================================================
@scene
def mountain_paths(s):
    sun = (240, 500)
    summit = (812, 168)
    s.sky([(0, "#161a44"), (.2, "#2e2e64"), (.38, "#6a4e86"), (.5, "#d08a8c"), (.58, "#ffb88c"), (.62, "#ffe0b0")])
    s.stars(50, 0, 220, seed=61, bright=.5)
    s.sun(*sun, 34, halo_r=640, halo_a=.8)
    s.fx("clouds", y0=20, y1=300, seed=161, cell=170, aniso=3.6, cover=.42, soft=.2, lit="#ffb8a0", body=.72, direct=.8,
         light=(-.6, 1), sun=(sun[0], sun[1], 480), opacity=.85)
    s.fx("clouds", y0=380, y1=560, seed=162, cell=90, aniso=6, cover=.3, soft=.22, lit="#ffd8b0", body=.85, direct=.95,
         light=(-.4, 1), sun=(sun[0], sun[1], 420), opacity=.75)
    far = peak_line(640, [(150, 160, 260), (420, 120, 220), (1250, 150, 260), (1520, 190, 240)], 162, shape=1.3, floor=40)
    mountains(s, far, "#8a6a9e", "#a888aa", lit="#ffc0a8", lit_a=.6, light=-1, seed=163, snow="#c8b8dc", snow_shade="#a898c4",
              lit_snow="#fff0e6", snowline=560, snow_fingers=40, rim="#fff0d8", rim_center=sun, rim_r=700, haze="#efc6c0", haze_a=.5,
              haze_h=120, base_y=660)
    s.mist(640, 90, "#f0c0b8", .5, 22)
    # the great mountain
    mt = peak_line(900, [(812, 732, 640, -.05), (560, 380, 300), (1080, 400, 320)], 164, detail=.12, x0=-40, x1=1640, step=3, shape=1.25, shoulders=1)
    mountains(s, mt, "#4e3e78", "#2a2246", lit="#ff b0a0".replace(" ", ""), lit_a=.6, light=-1, seed=165, snow="#c8bcdc",
              snow_shade="#8a7cb0", lit_snow="#ffe4dc", snowline=330, snow_fingers=70, rim="#fff0d8", rim_center=sun, rim_r=1100,
              rim_w=2, haze="#c890a8", haze_a=.4, haze_h=260, base_y=920)
    s.mist(760, 140, "#d8a0b0", .3, 30)
    # lamp-lit paths winding up the faces, all meeting at the summit
    rng = random.Random(7)
    paths = [
        [(140, 1010), (300, 880), (240, 800), (400, 690), (360, 600), (520, 500), (500, 420), (640, 330), (720, 250), summit],
        [(620, 1010), (700, 900), (600, 800), (720, 700), (640, 600), (760, 500), (700, 400), (790, 300), summit],
        [(1060, 1010), (960, 900), (1060, 800), (930, 700), (1000, 600), (880, 480), (920, 380), (840, 280), summit],
        [(1500, 1010), (1340, 900), (1420, 820), (1240, 720), (1300, 640), (1080, 520), (1060, 420), (920, 320), summit],
    ]
    for k, ctrl in enumerate(paths):
        pts = smooth_line(ctrl, 4)
        n = len(pts)
        trail = ribbon(pts, 14, 2)
        s.add(f'<path d="{trail}" fill="#ffd8b0" opacity=".2" filter="{s.blur(1.5)}"/>')
        lamps = []
        step = 1.0
        i = 0.0
        while i < n - 1:
            x, y = pts[int(i)]
            t = (y - summit[1]) / (1010 - summit[1])
            r = 1.1 + 3.2 * t
            lamps.append((x + rng.uniform(-2, 2) * t, y, r))
            i += 5 + 11 * t
        for x, y, r in lamps:
            s.add(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r * 5)}" fill="#ffa040" opacity=".45" filter="{s.blur(r * 2.4)}"/>'
                  f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="#fff0c0"/>')
    # the shrine at the summit
    s.glow(summit[0], summit[1], 420, "#ffb060", .45, .18)
    s.glow(summit[0], summit[1] - 20, 90, "#fff0c8", .6, .3)
    arch.shikhara_front(s, summit[0], summit[1] + 6, .3, color="#2a1e36", rim="#fff0d0", door="#ffd890")
    s.rays(summit[0], summit[1] - 40, n=18, length=520, width=.03, color="#ffe8b8", a=.2, seed=5, blur=6)
    # foreground pilgrims setting out at the foot
    from figures import pilgrim
    s.add(pilgrim(230, 990, 1.0, color="#0c0812", rim="#ffcf9e", flip=True) + pilgrim(1420, 996, .9, color="#0c0812", rim="#ffcf9e"))
    fg = ridgeline(1000, 60, 166, cell=260, octaves=5, ridged=.3)
    hills(s, fg, "#120c1c", "#0a0812", rim="#ffbf90", rim_a=.7, rim_center=sun, rim_r=900)
    s.motes(40, 300, 1300, 150, 900, seed=6, size=(.7, 1.8))
    s.fx("godrays", cx=summit[0], cy=summit[1], strength=.3, thresh=.75, decay=.97, radius=200)
    s.fx("mottle", amp=.045, cell=60)
    return s


# =====================================================================================
# temple architecture in front elevation, lit from one side
# =====================================================================================
def _side_lit(s, x0, x1, dark, mid, lit, light=1, rim=None):
    """Horizontal gradient for a form spanning x0..x1, light coming from the right (light=1) or left."""
    st = [(0, dark, 1), (.45, mid, 1), (.82, lit, 1), (1, rim or lit, 1)]
    if light < 0:
        st = [(1 - o, c, a) for o, c, a in st][::-1]
    return s.lin(st, x0, 0, x1, 0, user=True)


def _curve_spire(cx, base, top, w0, w1, bulge=.18, n=24):
    """Points of one side (right) of a curvilinear spire, base to top."""
    pts = []
    for k in range(n + 1):
        t = k / n
        w = w0 + (w1 - w0) * t ** 1.7 + w0 * bulge * math.sin(math.pi * t) * (1 - t)
        pts.append((cx + w, base + (top - base) * t))
    return pts


def _spire_path(cx, base, top, w0, w1, bulge=.18):
    r = _curve_spire(cx, base, top, w0, w1, bulge)
    l = [(2 * cx - x, y) for x, y in r]
    return pts_d(r + l[::-1]), r


def amalaka(cx, y, rx, ry, ribs=14):
    """A ribbed amalaka disc: returns (outline path, rib path)."""
    d = f"M{f(cx - rx)} {f(y)}C{f(cx - rx)} {f(y - ry * 1.3)} {f(cx + rx)} {f(y - ry * 1.3)} {f(cx + rx)} {f(y)}C{f(cx + rx)} {f(y + ry * 1.3)} {f(cx - rx)} {f(y + ry * 1.3)} {f(cx - rx)} {f(y)}Z"
    ribs_d = "".join(f"M{f(cx + rx * math.sin(a))} {f(y - ry * .95)}Q{f(cx + rx * 1.08 * math.sin(a))} {f(y)} {f(cx + rx * math.sin(a))} {f(y + ry * .95)}"
                     for a in [-math.pi / 2 + math.pi * (k + .5) / ribs for k in range(ribs)])
    return d, ribs_d


def kalasha_top(cx, y, sc):
    """Pot finial on a short neck, with a spike: path above y."""
    return (f"M{f(cx - 7 * sc)} {f(y)}H{f(cx + 7 * sc)}V{f(y - 6 * sc)}H{f(cx - 7 * sc)}Z"
            f"M{f(cx - 10 * sc)} {f(y - 6 * sc)}C{f(cx - 14 * sc)} {f(y - 18 * sc)} {f(cx - 4 * sc)} {f(y - 24 * sc)} {f(cx)} {f(y - 24 * sc)}"
            f"C{f(cx + 4 * sc)} {f(y - 24 * sc)} {f(cx + 14 * sc)} {f(y - 18 * sc)} {f(cx + 10 * sc)} {f(y - 6 * sc)}Z"
            f"M{f(cx - 2 * sc)} {f(y - 23 * sc)}L{f(cx)} {f(y - 34 * sc)}L{f(cx + 2 * sc)} {f(y - 23 * sc)}Z")


def nagara_grand(s, cx, base, sc=1.0, dark="#3a2430", mid="#8a5a48", lit="#f0b888", rim="#fff0d0", light=1,
                 door="#ffb050", flag_c="#f07a1e", mandapa=True, spires=2, line="#2a1418", white=False):
    """A grand Nagara (north Indian) temple seen from the front: a curvilinear shikhara clustered
    with smaller spires (urushringas), crowned by a ribbed amalaka and kalasha with a flag, a
    pillared hall with a stepped pyramidal roof in front, all on a high moulded platform.
    About 600 tall and 520 wide at sc=1; (cx, base) is the foot of the platform's steps."""
    S = sc
    def X(v):
        return cx + v * S
    def Y(v):
        return base - v * S
    out = []
    shade_a = .45 if not white else .3
    # -- the main shikhara and its clustered spires (back to front)
    wall_top = 170
    spire_top = 560
    layers = []
    if spires >= 2:
        for side in (-1, 1):
            layers.append((side * 168, wall_top, 340, 46, 16))
    for side in (-1, 1):
        layers.append((side * 112, wall_top, 430, 60, 20))
    layers.append((0, wall_top, spire_top, 124, 40))
    bands = []
    for (ox, b0, t0, w0, w1) in layers:
        d, r = _spire_path(X(ox), Y(b0), Y(t0), w0 * S, w1 * S)
        g = _side_lit(s, X(ox) - w0 * S, X(ox) + w0 * S, dark, mid, lit, light, rim)
        out.append(f'<path d="{d}" fill="{g}"/>')
        # ratha offsets: vertical bands that run up the spire
        cl = s.clip(d)
        ribs = []
        for q in (-.62, -.3, .3, .62):
            pts = [(X(ox) + (x - X(ox)) * q, y) for x, y in r]
            ribs.append("M" + "L".join(f"{f(x)} {f(y)}" for x, y in pts))
        hb = []
        nb = int((t0 - b0) / 22)
        for k in range(1, nb):
            yy = Y(b0) + (Y(t0) - Y(b0)) * k / nb
            hb.append(f"M{f(X(ox) - w0 * S * 1.2)} {f(yy)}H{f(X(ox) + w0 * S * 1.2)}")
        out.append(f'<g clip-path="{cl}"><path d="{"".join(hb)}" stroke="{line}" stroke-opacity=".35" stroke-width="{f(2.4 * S)}"/>'
                   f'<path d="{"".join(hb)}" stroke="{rim}" stroke-opacity=".14" stroke-width="{f(1.2 * S)}" transform="translate(0 {f(-2 * S)})"/>'
                   f'<path d="{"".join(ribs)}" stroke="{line}" stroke-opacity=".3" stroke-width="{f(3 * S)}" fill="none"/>'
                   f'<path d="{"".join(ribs)}" stroke="{rim}" stroke-opacity=".12" stroke-width="{f(1.4 * S)}" fill="none" transform="translate({f(2 * S * light)} 0)"/></g>')
        # little amalakas at the corners every few storeys (bhumi-amalakas)
        bam = []
        for k in range(4, nb, 5):
            yy = Y(b0) + (Y(t0) - Y(b0)) * k / nb
            ww = [x for x, y in r if y <= yy + .5]
            wx = (ww[0] if ww else r[-1][0]) - X(ox)
            for sd in (-1, 1):
                bam.append(f'<ellipse cx="{f(X(ox) + sd * wx * .97)}" cy="{f(yy)}" rx="{f(9 * S)}" ry="{f(5 * S)}"/>')
        out.append(f'<g fill="{mid}">{"".join(bam)}</g>')
        # amalaka and finial on each spire
        ad, ar = amalaka(X(ox), Y(t0) - 6 * S, w1 * 1.35 * S, 7 * S if ox else 11 * S)
        out.append(f'<path d="{ad}" fill="{_side_lit(s, X(ox) - w1 * 1.4 * S, X(ox) + w1 * 1.4 * S, dark, mid, lit, light, rim)}"/>'
                   f'<path d="{ar}" stroke="{line}" stroke-opacity=".4" stroke-width="{f(1.2 * S)}" fill="none"/>')
        if ox == 0:
            out.append(f'<path d="{kalasha_top(X(0), Y(t0) - 16 * S, 1.6 * S)}" fill="{"#f4d080" if not white else "#f6d890"}"/>')
            fy = Y(t0) - 54 * S
            out.append(f'<path d="M{f(X(0))} {f(fy)}V{f(fy - 46 * S)}" stroke="{line}" stroke-width="{f(2.4 * S)}"/>' +
                       arch.flag(X(0), fy - 46 * S, 56 * S, 26 * S, flag_c, seed=3))
        else:
            out.append(f'<path d="{kalasha_top(X(ox), Y(t0) - 12 * S, .9 * S)}" fill="{mid}"/>')
    # -- sanctum walls with pilasters and niches
    wall = f"M{f(X(-200))} {f(Y(46))}V{f(Y(wall_top))}H{f(X(200))}V{f(Y(46))}Z"
    out.append(f'<path d="{wall}" fill="{_side_lit(s, X(-200), X(200), dark, mid, lit, light, rim)}"/>')
    pil = "".join(f"M{f(X(v))} {f(Y(50))}V{f(Y(wall_top - 6))}" for v in range(-190, 200, 26))
    out.append(f'<path d="{pil}" stroke="{line}" stroke-opacity=".3" stroke-width="{f(3 * S)}"/>')
    out.append(f'<path d="M{f(X(-206))} {f(Y(wall_top))}H{f(X(206))}M{f(X(-206))} {f(Y(110))}H{f(X(206))}" stroke="{line}" stroke-opacity=".4" stroke-width="{f(5 * S)}"/>')
    # -- the mandapa: pillared porch with a stepped pyramidal roof and bell finial
    if mandapa:
        roof_b, roof_t = 150, 300
        tiers = []
        nt = 7
        for k in range(nt):
            y0, y1 = roof_b + (roof_t - roof_b) * k / nt, roof_b + (roof_t - roof_b) * (k + 1) / nt
            w0 = 150 - 100 * k / nt
            w1 = w0 - 6
            tiers.append(f"M{f(X(-w0 - 8))} {f(Y(y0))}L{f(X(-w1))} {f(Y(y1 - 4))}H{f(X(w1))}L{f(X(w0 + 8))} {f(Y(y0))}Z")
        rd = "".join(tiers)
        out.append(f'<path d="{rd}" fill="{_side_lit(s, X(-160), X(160), dark, mid, lit, light, rim)}"/>')
        out.append(f'<path d="{rd}" fill="none" stroke="{line}" stroke-opacity=".45" stroke-width="{f(2 * S)}"/>')
        bell = (f"M{f(X(-30))} {f(Y(roof_t - 4))}C{f(X(-34))} {f(Y(roof_t + 30))} {f(X(-12))} {f(Y(roof_t + 40))} {f(X(0))} {f(Y(roof_t + 42))}"
                f"C{f(X(12))} {f(Y(roof_t + 40))} {f(X(34))} {f(Y(roof_t + 30))} {f(X(30))} {f(Y(roof_t - 4))}Z")
        out.append(f'<path d="{bell}" fill="{_side_lit(s, X(-34), X(34), dark, mid, lit, light, rim)}"/>')
        out.append(f'<path d="{kalasha_top(X(0), Y(roof_t + 42), 1.1 * S)}" fill="{"#f4d080"}"/>')
        porch = f"M{f(X(-130))} {f(Y(46))}V{f(Y(roof_b))}H{f(X(130))}V{f(Y(46))}Z"
        out.append(f'<path d="{porch}" fill="{_side_lit(s, X(-130), X(130), dark, mid, lit, light, rim)}"/>')
        out.append(f'<path d="M{f(X(-136))} {f(Y(roof_b))}H{f(X(136))}" stroke="{line}" stroke-opacity=".5" stroke-width="{f(6 * S)}"/>')
        # pillars, with the lamp-lit interior between them
        inner_g = s.lin([(0, door, .9), (1, mix(door, "#5a1a08", .6), .9)], 0, Y(roof_b), 0, Y(46), user=True)
        out.append(f'<path d="M{f(X(-110))} {f(Y(52))}V{f(Y(roof_b - 12))}H{f(X(110))}V{f(Y(52))}Z" fill="{inner_g}" opacity=".85"/>')
        pills = "".join(f'<path d="M{f(X(v - 8))} {f(Y(52))}V{f(Y(roof_b - 12))}H{f(X(v + 8))}V{f(Y(52))}Z"/>' for v in (-102, -60, 60, 102))
        out.append(f'<g fill="{mix(dark, mid, .4)}">{pills}</g>')
        out.append(f'<path d="M{f(X(-22))} {f(Y(52))}V{f(Y(110))}C{f(X(-22))} {f(Y(126))} {f(X(22))} {f(Y(126))} {f(X(22))} {f(Y(110))}V{f(Y(52))}Z" fill="#fff0c0" opacity=".9"/>')
    # -- the moulded platform (jagati) and its central steps
    plat = f"M{f(X(-270))} {f(Y(0))}V{f(Y(46))}H{f(X(270))}V{f(Y(0))}Z"
    out.append(f'<path d="{plat}" fill="{_side_lit(s, X(-270), X(270), dark, mid, lit, light, rim)}"/>')
    out.append(f'<path d="M{f(X(-276))} {f(Y(46))}H{f(X(276))}M{f(X(-272))} {f(Y(30))}H{f(X(272))}M{f(X(-270))} {f(Y(14))}H{f(X(270))}" stroke="{line}" stroke-opacity=".45" stroke-width="{f(3 * S)}"/>')
    stp = "".join(f'<path d="M{f(X(-50 - k * 4))} {f(Y(46 - k * 8))}H{f(X(50 + k * 4))}" stroke="{rim}" stroke-opacity=".35" stroke-width="{f(1.6 * S)}"/>' for k in range(6))
    out.append(f'<path d="M{f(X(-50))} {f(Y(46))}H{f(X(50))}L{f(X(74))} {f(Y(0))}H{f(X(-74))}Z" fill="{mix(mid, dark, .3)}"/>{stp}')
    s.add("".join(out))
    if door:
        s.glow(X(0), Y(90), 160 * S, door, .4, .25, sy=.7)


def gopuram(s, cx, base, sc=1.0, dark="#3a2430", mid="#9a6248", lit="#f4c090", rim="#fff0d0", light=1, line="#2a1418",
            tiers=7, door="#ffb050", finials=7):
    """A Dravida gopuram: a towering gateway of diminishing storeys, each crowded with little
    pavilions, crowned by a barrel-vaulted roof with a row of kalasha finials and horned gable
    ends. About 620 tall at sc=1; (cx, base) is the foot of the gateway."""
    S = sc
    def X(v):
        return cx + v * S
    def Y(v):
        return base - v * S
    out = []
    # granite base storeys
    bw, bh = 160, 150
    basep = f"M{f(X(-bw))} {f(Y(0))}V{f(Y(bh))}H{f(X(bw))}V{f(Y(0))}Z"
    out.append(f'<path d="{basep}" fill="{_side_lit(s, X(-bw), X(bw), dark, mid, lit, light, rim)}"/>')
    out.append(f'<path d="{"".join(f"M{f(X(v))} {f(Y(4))}V{f(Y(bh - 8))}" for v in range(-150, 151, 20))}" stroke="{line}" stroke-opacity=".3" stroke-width="{f(3 * S)}"/>'
               f'<path d="M{f(X(-bw - 6))} {f(Y(bh))}H{f(X(bw + 6))}M{f(X(-bw - 4))} {f(Y(70))}H{f(X(bw + 4))}" stroke="{line}" stroke-opacity=".5" stroke-width="{f(6 * S)}"/>')
    dg = s.lin([(0, "#fff0c0", 1), (.4, door, 1), (1, mix(door, "#4a1a08", .6), 1)], 0, Y(118), 0, Y(0), user=True)
    out.append(f'<path d="M{f(X(-34))} {f(Y(0))}V{f(Y(118))}H{f(X(34))}V{f(Y(0))}Z" fill="{dg}"/>'
               f'<path d="M{f(X(-42))} {f(Y(0))}V{f(Y(124))}H{f(X(42))}V{f(Y(0))}" stroke="{mix(dark, mid, .3)}" stroke-width="{f(8 * S)}" fill="none"/>')
    # the storeys
    y = bh
    w = bw - 6
    th = 52
    for k in range(tiers):
        w2 = w - 13
        tier = f"M{f(X(-w))} {f(Y(y))}L{f(X(-w2))} {f(Y(y + th))}H{f(X(w2))}L{f(X(w))} {f(Y(y))}Z"
        out.append(f'<path d="{tier}" fill="{_side_lit(s, X(-w), X(w), dark, mid, lit, light, rim)}"/>')
        # cornice and the row of little pavilions on it
        cy = y + th
        out.append(f'<path d="M{f(X(-w2 - 6))} {f(Y(cy))}H{f(X(w2 + 6))}" stroke="{line}" stroke-opacity=".55" stroke-width="{f(5 * S)}"/>')
        n = max(3, int(w2 / 22))
        kudus = []
        for j in range(n + 1):
            px = -w2 + 2 * w2 * j / n
            if j in (0, n):    # kutas: square domed pavilions at the corners
                kudus.append(f"M{f(X(px - 9))} {f(Y(cy))}V{f(Y(cy + 10))}C{f(X(px - 9))} {f(Y(cy + 20))} {f(X(px + 9))} {f(Y(cy + 20))} {f(X(px + 9))} {f(Y(cy + 10))}V{f(Y(cy))}Z")
            elif j % 2:        # shalas: little barrel roofs
                kudus.append(f"M{f(X(px - 11))} {f(Y(cy))}V{f(Y(cy + 8))}Q{f(X(px))} {f(Y(cy + 20))} {f(X(px + 11))} {f(Y(cy + 8))}V{f(Y(cy))}Z")
            else:              # kudu arches
                kudus.append(f"M{f(X(px - 6))} {f(Y(cy))}C{f(X(px - 7))} {f(Y(cy + 12))} {f(X(px + 7))} {f(Y(cy + 12))} {f(X(px + 6))} {f(Y(cy))}Z")
        out.append(f'<path d="{"".join(kudus)}" fill="{_side_lit(s, X(-w2), X(w2), dark, mid, lit, light, rim)}"/>')
        # figures in niches: a rhythm of light and dark
        nn = []
        for j in range(n):
            px = -w2 + 2 * w2 * (j + .5) / n
            nn.append(f"M{f(X(px - 4))} {f(Y(y + 6))}V{f(Y(y + th - 12))}H{f(X(px + 4))}V{f(Y(y + 6))}Z")
        out.append(f'<path d="{"".join(nn)}" fill="{line}" opacity=".35"/>')
        y += th
        th *= .93
        w = w2 - 3
    # barrel-vault crown with horned gables and kalasha finials
    vw = w + 16
    vh = 58
    vault = (f"M{f(X(-vw))} {f(Y(y))}V{f(Y(y + vh * .45))}C{f(X(-vw))} {f(Y(y + vh * 1.05))} {f(X(-vw * .6))} {f(Y(y + vh * 1.1))} {f(X(0))} {f(Y(y + vh * 1.1))}"
             f"C{f(X(vw * .6))} {f(Y(y + vh * 1.1))} {f(X(vw))} {f(Y(y + vh * 1.05))} {f(X(vw))} {f(Y(y + vh * .45))}V{f(Y(y))}Z")
    horns = (f"M{f(X(-vw))} {f(Y(y + vh * .5))}C{f(X(-vw - 22))} {f(Y(y + vh * .6))} {f(X(-vw - 26))} {f(Y(y + vh * 1.2))} {f(X(-vw - 12))} {f(Y(y + vh * 1.35))}"
             f"C{f(X(-vw - 14))} {f(Y(y + vh * 1.0))} {f(X(-vw - 8))} {f(Y(y + vh * .85))} {f(X(-vw + 4))} {f(Y(y + vh * .8))}Z"
             f"M{f(X(vw))} {f(Y(y + vh * .5))}C{f(X(vw + 22))} {f(Y(y + vh * .6))} {f(X(vw + 26))} {f(Y(y + vh * 1.2))} {f(X(vw + 12))} {f(Y(y + vh * 1.35))}"
             f"C{f(X(vw + 14))} {f(Y(y + vh * 1.0))} {f(X(vw + 8))} {f(Y(y + vh * .85))} {f(X(vw - 4))} {f(Y(y + vh * .8))}Z")
    out.append(f'<path d="{vault}{horns}" fill="{_side_lit(s, X(-vw - 26), X(vw + 26), dark, mid, lit, light, rim)}"/>')
    out.append(f'<path d="M{f(X(-vw * .55))} {f(Y(y + 6))}V{f(Y(y + vh * .8))}M{f(X(vw * .55))} {f(Y(y + 6))}V{f(Y(y + vh * .8))}" stroke="{line}" stroke-opacity=".3" stroke-width="{f(3 * S)}"/>'
               f'<ellipse cx="{f(X(0))}" cy="{f(Y(y + vh * .45))}" rx="{f(16 * S)}" ry="{f(20 * S)}" fill="{line}" opacity=".45"/>')
    fin = "".join(kalasha_top(X(-vw * .8 + 1.6 * vw * j / (finials - 1)), Y(y + vh * 1.06 - 3), 1.0 * S) for j in range(finials))
    out.append(f'<path d="{fin}" fill="#f4d080"/>')
    s.add("".join(out))
    s.glow(X(0), Y(50), 120 * S, door, .4, .25, sy=.9)


def vimana(s, cx, base, sc=1.0, dark="#3a2430", mid="#9a6248", lit="#f4c090", rim="#fff0d0", light=1, line="#2a1418", tiers=5):
    """A Dravida vimana: a square sanctum under a stepped pyramid of storeys ringed with miniature
    shrines, then a neck and an octagonal domed cupola with one kalasha. ~460 tall at sc=1."""
    S = sc
    def X(v):
        return cx + v * S
    def Y(v):
        return base - v * S
    out = []
    plat = f"M{f(X(-150))} {f(Y(0))}V{f(Y(30))}H{f(X(150))}V{f(Y(0))}Z"
    wall = f"M{f(X(-120))} {f(Y(30))}V{f(Y(150))}H{f(X(120))}V{f(Y(30))}Z"
    out.append(f'<path d="{plat}{wall}" fill="{_side_lit(s, X(-150), X(150), dark, mid, lit, light, rim)}"/>')
    out.append(f'<path d="{"".join(f"M{f(X(v))} {f(Y(36))}V{f(Y(144))}" for v in range(-110, 111, 22))}" stroke="{line}" stroke-opacity=".3" stroke-width="{f(3 * S)}"/>'
               f'<path d="M{f(X(-126))} {f(Y(150))}H{f(X(126))}M{f(X(-152))} {f(Y(30))}H{f(X(152))}" stroke="{line}" stroke-opacity=".5" stroke-width="{f(6 * S)}"/>')
    niches = "".join(f"M{f(X(v - 9))} {f(Y(50))}V{f(Y(118))}Q{f(X(v))} {f(Y(130))} {f(X(v + 9))} {f(Y(118))}V{f(Y(50))}Z" for v in (-77, 0, 77))
    out.append(f'<path d="{niches}" fill="{line}" opacity=".45"/>')
    y, w, th = 150, 116, 42
    for k in range(tiers):
        w2 = w - 8
        tier = f"M{f(X(-w))} {f(Y(y))}V{f(Y(y + th * .7))}L{f(X(-w2))} {f(Y(y + th))}H{f(X(w2))}L{f(X(w))} {f(Y(y + th * .7))}V{f(Y(y))}Z"
        out.append(f'<path d="{tier}" fill="{_side_lit(s, X(-w), X(w), dark, mid, lit, light, rim)}"/>')
        cy = y + th
        n = max(2, int(w2 / 26))
        sh = []
        for j in range(n + 1):
            px = -w2 + 2 * w2 * j / n
            if j in (0, n):
                sh.append(f"M{f(X(px - 10))} {f(Y(cy))}V{f(Y(cy + 10))}C{f(X(px - 10))} {f(Y(cy + 22))} {f(X(px + 10))} {f(Y(cy + 22))} {f(X(px + 10))} {f(Y(cy + 10))}V{f(Y(cy))}Z")
            else:
                sh.append(f"M{f(X(px - 13))} {f(Y(cy))}V{f(Y(cy + 9))}Q{f(X(px))} {f(Y(cy + 22))} {f(X(px + 13))} {f(Y(cy + 9))}V{f(Y(cy))}Z")
        out.append(f'<path d="{"".join(sh)}" fill="{_side_lit(s, X(-w2), X(w2), dark, mid, lit, light, rim)}"/>')
        out.append(f'<path d="M{f(X(-w - 4))} {f(Y(y + th * .7))}H{f(X(w + 4))}" stroke="{line}" stroke-opacity=".5" stroke-width="{f(4 * S)}"/>'
                   f'<path d="{"".join(f"M{f(X(v))} {f(Y(y + 4))}V{f(Y(y + th * .66))}" for v in range(int(-w) + 10, int(w), 18))}" stroke="{line}" stroke-opacity=".25" stroke-width="{f(2.4 * S)}"/>')
        y += th + 8
        w = w2 - 14
        th *= .9
    neck = f"M{f(X(-30))} {f(Y(y))}V{f(Y(y + 22))}H{f(X(30))}V{f(Y(y))}Z"
    dome = (f"M{f(X(-56))} {f(Y(y + 22))}C{f(X(-60))} {f(Y(y + 60))} {f(X(-30))} {f(Y(y + 82))} {f(X(0))} {f(Y(y + 84))}"
            f"C{f(X(30))} {f(Y(y + 82))} {f(X(60))} {f(Y(y + 60))} {f(X(56))} {f(Y(y + 22))}Z")
    out.append(f'<path d="{neck}{dome}" fill="{_side_lit(s, X(-60), X(60), dark, mid, lit, light, rim)}"/>')
    out.append(f'<path d="M{f(X(-28))} {f(Y(y + 26))}Q{f(X(-34))} {f(Y(y + 64))} {f(X(0))} {f(Y(y + 82))}M{f(X(28))} {f(Y(y + 26))}Q{f(X(34))} {f(Y(y + 64))} {f(X(0))} {f(Y(y + 82))}M{f(X(0))} {f(Y(y + 24))}V{f(Y(y + 82))}" stroke="{line}" stroke-opacity=".35" stroke-width="{f(2.4 * S)}" fill="none"/>')
    out.append(f'<path d="{kalasha_top(X(0), Y(y + 82), 1.5 * S)}" fill="#f4d080"/>')
    s.add("".join(out))


def rekha_deula(s, cx, base, sc=1.0, dark="#2a1a28", mid="#6a4a50", lit="#e8a888", rim="#fff0d0", light=1, line="#1a0e14", chakra=True):
    """A Kalinga temple as at Puri: a tall rib-banded curvilinear tower (rekha deula) topped by an
    amalaka, the Nila Chakra wheel and a flag, with the stepped pidha roof of the porch before it."""
    S = sc
    def X(v):
        return cx + v * S
    def Y(v):
        return base - v * S
    out = []
    d, r = _spire_path(X(0), Y(0), Y(420), 92 * S, 34 * S, bulge=.05)
    out.append(f'<path d="{d}" fill="{_side_lit(s, X(-92), X(92), dark, mid, lit, light, rim)}"/>')
    ribs = []
    for q in (-.75, -.45, -.15, .15, .45, .75):
        ribs.append("M" + "L".join(f"{f(X(0) + (x - X(0)) * q)} {f(y)}" for x, y in r))
    out.append(f'<g clip-path="{s.clip(d)}"><path d="{"".join(ribs)}" stroke="{line}" stroke-opacity=".35" stroke-width="{f(3 * S)}" fill="none"/></g>')
    ad, ar = amalaka(X(0), Y(430), 46 * S, 10 * S)
    out.append(f'<path d="{ad}" fill="{_side_lit(s, X(-46), X(46), dark, mid, lit, light, rim)}"/><path d="{ar}" stroke="{line}" stroke-opacity=".4" stroke-width="{f(1.2 * S)}" fill="none"/>')
    out.append(f'<path d="{kalasha_top(X(0), Y(440), 1.4 * S)}" fill="#f4d080"/>')
    if chakra:
        cy = Y(500)
        out.append(f'<path d="M{f(X(0))} {f(Y(474))}V{f(Y(560))}" stroke="{line}" stroke-width="{f(2.4 * S)}"/>'
                   f'<circle cx="{f(X(0))}" cy="{f(cy)}" r="{f(18 * S)}" fill="none" stroke="#f4d080" stroke-width="{f(3 * S)}"/>'
                   + "".join(f'<path d="M{f(X(0))} {f(cy)}L{f(X(0) + 18 * S * math.cos(a))} {f(cy + 18 * S * math.sin(a))}" stroke="#f4d080" stroke-width="{f(1.4 * S)}"/>' for a in [k * math.pi / 4 for k in range(8)])
                   + arch.flag(X(0), Y(560), 54 * S, 24 * S, "#f07a1e", seed=4))
    # porch with the pidha roof: stacked horizontal tiers
    py0 = 40
    porch = f"M{f(X(-150))} {f(Y(0))}V{f(Y(110))}H{f(X(150))}V{f(Y(0))}Z"
    tiers = "".join(f"M{f(X(-140 + k * 14))} {f(Y(110 + k * 22))}L{f(X(-132 + k * 14))} {f(Y(126 + k * 22))}H{f(X(132 - k * 14))}L{f(X(140 - k * 14))} {f(Y(110 + k * 22))}Z" for k in range(7))
    bell = f"M{f(X(-34))} {f(Y(268))}C{f(X(-34))} {f(Y(296))} {f(X(34))} {f(Y(296))} {f(X(34))} {f(Y(268))}Z"
    out.append(f'<path d="{porch}{tiers}{bell}" fill="{_side_lit(s, X(-150), X(150), dark, mid, lit, light, rim)}"/>')
    out.append(f'<path d="{kalasha_top(X(0), Y(294), 1.1 * S)}" fill="#f4d080"/>')
    out.append(f'<path d="M{f(X(-18))} {f(Y(0))}V{f(Y(60))}Q{f(X(0))} {f(Y(76))} {f(X(18))} {f(Y(60))}V{f(Y(0))}Z" fill="#ffd890"/>')
    s.add("".join(out))


def palm(x, base, h, seed=1, lean=0.0, color="#120c14"):
    """A coconut palm silhouette (SVG string): a slender curving trunk and a crown of arching fronds."""
    rng = random.Random(seed)
    tx, ty = x + lean * h, base - h
    out = [f'<path d="M{f(x - h * .022)} {f(base)}Q{f(x + lean * h * .2)} {f(base - h * .5)} {f(tx - h * .01)} {f(ty)}L{f(tx + h * .012)} {f(ty)}Q{f(x + lean * h * .2 + h * .02)} {f(base - h * .5)} {f(x + h * .022)} {f(base)}Z"/>']
    for k in range(11):
        a = -math.pi / 2 + (k - 5) * .32 + rng.uniform(-.1, .1)
        L = h * rng.uniform(.32, .46)
        ex, ey = tx + math.cos(a) * L, ty + math.sin(a) * L * .5 + L * .35 * abs(math.cos(a))
        mx, my = tx + math.cos(a) * L * .5, ty + math.sin(a) * L * .55 - L * .05
        w = L * .07
        out.append(f'<path d="M{f(tx)} {f(ty)}Q{f(mx)} {f(my - w)} {f(ex)} {f(ey)}Q{f(mx)} {f(my + w)} {f(tx)} {f(ty + 2)}Z"/>')
    return f'<g fill="{color}">{"".join(out)}</g>'


# =====================================================================================
# 12. the temple as a sacred mountain
# =====================================================================================
@scene
def temple(s):
    sun = (1290, 470)
    s.sky([(0, "#1a1e4c"), (.18, "#33346c"), (.34, "#7a5a8e"), (.44, "#d8889a"), (.5, "#ffb890"), (.54, "#ffe2b8")])
    s.stars(40, 0, 200, seed=71, bright=.5)
    s.sun(*sun, 34, halo_r=700, halo_a=.85)
    s.fx("clouds", y0=20, y1=300, seed=171, cell=170, aniso=3.8, cover=.42, soft=.2, lit="#ffbca8", body=.72, direct=.8,
         light=(.6, 1), sun=(sun[0], sun[1], 480), opacity=.85)
    s.fx("clouds", y0=330, y1=520, seed=172, cell=90, aniso=6, cover=.3, soft=.22, lit="#ffe0b8", body=.85, direct=.95,
         light=(.4, 1), sun=(sun[0], sun[1], 420), opacity=.7)
    far = peak_line(600, [(800, 470, 330, 0), (420, 300, 260), (1160, 330, 280), (120, 220, 220), (1500, 250, 240)], 173,
                    shape=1.25, floor=60, shoulders=2)
    mountains(s, far, "#8a74aa", "#ae8aae", lit="#ffc2a8", lit_a=.75, light=1, seed=174, snow="#c4b6de", snow_shade="#9c8ec4",
              lit_snow="#fff0e4", snowline=380, snow_fingers=60, rim="#fff2dc", rim_center=sun, rim_r=800, haze="#efc6c0",
              haze_a=.5, haze_h=180, base_y=640)
    s.mist(620, 110, "#f6d0c4", .5, 26)
    mid = ridgeline(780, 120, 175, cell=260, octaves=6, ridged=.4, envelope=[(0, 1), (600, .4), (800, .2), (1000, .4), (1600, 1)])
    hills(s, mid, "#4e3e70", "#5e4672", rim="#ffd2ac", rim_a=.8, rim_center=sun, rim_r=900, haze="#c98fa6", haze_a=.4)
    pines(s, -20, 1640, 0, 60, h=(24, 60), color="#3a2c56", seed=7, ground_fn=lambda x: y_at(mid, x))
    s.mist(800, 100, "#e8b0b4", .4, 24)
    # courtyard
    s.add(f'<rect x="-20" y="860" width="1640" height="160" fill="{s.lin([(0, "#6a4650", 1), (1, "#2a1a24", 1)], 0, 860, 0, 1000, user=True)}"/>'
          f'<path d="M-20 860H1640" stroke="#ffd8b0" stroke-opacity=".4" stroke-width="2"/>')
    s.add(f'<path d="{"".join(f"M{x} 860L{800 + (x - 800) * 2.2} 1000" for x in range(-400, 2001, 80))}{"".join(f"M-20 {y}H1640" for y in (880, 908, 944, 990))}" stroke="#1a0e14" stroke-opacity=".3" stroke-width="2"/>')
    s.glow(800, 820, 600, "#ffb070", .3, .2, sy=.3)
    nagara_grand(s, 800, 872, 1.02, dark="#2e1a2a", mid="#7a4a4a", lit="#f4b48a", rim="#fff0d8", light=1, line="#1e0e18")
    arch.deepastambha(s, 330, 880, 1.15, color="#3a2432", rim="#ffd8b0")
    arch.deepastambha(s, 1270, 880, 1.15, color="#3a2432", rim="#ffd8b0")
    from figures import pilgrim
    s.add(pilgrim(640, 960, .9, color="#140a12", rim="#ffcf9e", flip=True) + pilgrim(1010, 972, .95, color="#140a12", rim="#ffcf9e"))
    pines(s, -60, 200, 905, 5, h=(260, 420), color="#120a12", seed=9)
    pines(s, 1420, 1680, 905, 5, h=(280, 440), color="#120a12", seed=10)
    s.birds(7, 980, 1220, 300, 380, color="#4a2a44", s=(5, 9), seed=6, a=.8)
    s.motes(30, 300, 1300, 300, 860, seed=4, size=(.7, 1.8))
    s.fx("godrays", cx=sun[0], cy=sun[1], strength=.4, thresh=.72, decay=.972, radius=260)
    s.fx("mottle", amp=.045, cell=60)
    return s


# =====================================================================================
# 13. Nagara and Dravida side by side
# =====================================================================================
@scene
def temple_styles(s):
    sun = (190, 560)
    s.sky([(0, "#2a2858"), (.2, "#4a3e74"), (.38, "#a0688a"), (.5, "#f0a080"), (.58, "#ffc890"), (.64, "#ffe6bc")])
    s.sun(*sun, 38, halo_r=720, halo_a=.85)
    s.fx("clouds", y0=20, y1=320, seed=181, cell=170, aniso=3.8, cover=.4, soft=.2, lit="#ffc0a0", body=.74, direct=.85,
         light=(-.6, 1), sun=(sun[0], sun[1], 520), opacity=.85)
    s.fx("clouds", y0=360, y1=560, seed=182, cell=90, aniso=6, cover=.3, soft=.22, lit="#ffe0b0", body=.85, direct=.95,
         light=(-.5, 1), sun=(sun[0], sun[1], 440), opacity=.7)
    far = ridgeline(700, 60, 183, cell=260, octaves=5, ridged=.3)
    hills(s, far, "#a07490", "#b88a98", rim="#ffe0c0", rim_a=.6, rim_center=sun, rim_r=900, haze="#f0c0b0", haze_a=.5)
    rng = random.Random(4)
    s.add("".join(palm(x, y_at(far, x) + 30, rng.uniform(90, 150), seed=int(x), lean=rng.uniform(-.08, .08), color="#7a5470") for x in range(-20, 1640, 70) if rng.random() < .6))
    s.mist(720, 90, "#ffd0b8", .55, 20)
    s.add(f'<rect x="-20" y="880" width="1640" height="140" fill="{s.lin([(0, "#8a5a50", 1), (1, "#2a1a20", 1)], 0, 880, 0, 1000, user=True)}"/>'
          f'<path d="M-20 880H1640" stroke="#ffe0b8" stroke-opacity=".45" stroke-width="2"/>')
    s.glow(sun[0], 880, 900, "#ffb070", .3, .2, sy=.2)
    stone = dict(dark="#2e1a26", mid="#82504a", lit="#f8bc8a", rim="#fff2d8", light=-1, line="#1e0e18")
    nagara_grand(s, 470, 892, .78, **stone)
    vimana(s, 980, 892, .86, **stone)
    gopuram(s, 1290, 900, .9, **stone)
    s.add(palm(80, 930, 380, seed=7, lean=.06) + palm(1560, 940, 340, seed=8, lean=-.05) + palm(1490, 950, 260, seed=9, lean=.04))
    s.birds(8, 640, 900, 240, 330, color="#4a2a44", s=(5, 9), seed=6, a=.8)
    s.motes(30, 300, 1300, 300, 880, seed=4, size=(.7, 1.8))
    s.fx("godrays", cx=sun[0], cy=sun[1], strength=.4, thresh=.72, decay=.972, radius=280)
    s.fx("mottle", amp=.045, cell=60)
    return s


# =====================================================================================
# 14. a temple among the towers
# =====================================================================================
def towers(s, x0, x1, base, h=(200, 560), seed=1, glass=("#1a2a4e", "#3a5a8a"), win=("#ffd8a0", "#bfe0ff", "#fff4e0"), win_p=.35,
           haze=None, haze_a=.3, rim="#ffb8c8", spires=.3):
    """Modern glass towers with lit window grids, crowns and spires."""
    rng = random.Random(seed)
    x = x0
    while x < x1:
        w = rng.uniform(60, 150)
        hh = rng.uniform(*h)
        top = base - hh
        g = s.lin([(0, glass[1], 1), (.5, glass[0], 1), (1, mix(glass[0], "#000000", .3), 1)], x, 0, x + w, 0, user=True)
        kind = rng.random()
        if kind < .2:     # slanted crown
            d = f"M{f(x)} {f(base)}V{f(top + 40)}L{f(x + w)} {f(top)}V{f(base)}Z"
        elif kind < .35:  # stepped
            d = f"M{f(x)} {f(base)}V{f(top + 60)}H{f(x + w * .2)}V{f(top + 20)}H{f(x + w * .8)}V{f(top + 60)}H{f(x + w)}V{f(base)}Z"
        else:
            d = f"M{f(x)} {f(base)}V{f(top)}H{f(x + w)}V{f(base)}Z"
        out = [f'<path d="{d}" fill="{g}"/>']
        if rng.random() < spires:
            out.append(f'<path d="M{f(x + w / 2)} {f(top)}V{f(top - rng.uniform(40, 110))}" stroke="{glass[0]}" stroke-width="3"/>')
            out.append(f'<circle cx="{f(x + w / 2)}" cy="{f(top - 4)}" r="0" fill="none"/>')
        lit, dark = [], []
        fh, fw = 14, 10
        cols = max(2, int(w / 16))
        for r_ in range(int((hh - 30) / fh)):
            yy = base - 12 - r_ * fh
            band = rng.random() < .7
            for c in range(cols):
                xx = x + 6 + c * (w - 12) / cols
                if band and rng.random() < win_p:
                    lit.append(f'<rect x="{f(xx)}" y="{f(yy - 8)}" width="{f(fw * .7)}" height="7" fill="{rng.choice(win)}" opacity="{rng.uniform(.5, 1):.2f}"/>')
        out.append(f'<g clip-path="{s.clip(d)}">{"".join(lit)}'
                   f'<path d="{"".join(f"M{f(x + 6 + c * (w - 12) / cols - 3)} {f(top)}V{f(base)}" for c in range(cols + 1))}" stroke="#000" stroke-opacity=".2" stroke-width="2"/></g>')
        out.append(f'<path d="M{f(x + w)} {f(base)}V{f(top)}" stroke="{rim}" stroke-opacity=".35" stroke-width="2"/>')
        if rng.random() < .4:
            out.append(f'<circle cx="{f(x + w / 2)}" cy="{f(top - 6)}" r="2.6" fill="#ff4a4a"/>')
        s.add("".join(out))
        x += w + rng.uniform(-10, 30)
    if haze:
        s.add(f'<rect x="{x0}" y="{base - h[1] - 120}" width="{x1 - x0}" height="{h[1] + 120}" fill="{s.lin([(0, haze, 0), (1, haze, haze_a)], 0, base - h[1], 0, base, user=True)}"/>')


@scene
def skyline(s):
    wl = 870
    s.sky([(0, "#0e1434"), (.25, "#1e2a5a"), (.48, "#4a4a82"), (.62, "#a06a92"), (.72, "#ee9a8e"), (.8, "#ffc89a")])
    s.stars(40, 0, 220, seed=81, bright=.5)
    s.fx("clouds", y0=40, y1=360, seed=191, cell=170, aniso=4, cover=.36, soft=.2, lit="#c88aa8", body=.75, direct=.7,
         light=(0, 1), opacity=.75)
    s.glow(800, 760, 900, "#ff9a80", .3, .2, sy=.4)
    towers(s, -40, 1660, 740, h=(220, 520), seed=3, glass=("#2a2e5e", "#4a4a80"), win_p=.22, haze="#8a6a9a", haze_a=.55, spires=.2)
    towers(s, -60, 1680, 800, h=(140, 420), seed=5, glass=("#16204a", "#34487a"), win_p=.38, haze="#5a4a7a", haze_a=.35, spires=.35)
    s.mist(780, 80, "#c890a8", .4, 20)
    # temple precinct: wall, lawns, then the temple itself, floodlit
    s.add(f'<rect x="-20" y="800" width="1640" height="80" fill="{s.lin([(0, "#2a2448", 1), (1, "#16122a", 1)], 0, 800, 0, 880, user=True)}"/>')
    s.add("".join(palm(x, 820, 120 + (k % 3) * 20, seed=k, color="#100c1e") for k, x in enumerate(range(-10, 1640, 120)) if abs(x - 800) > 330))
    s.glow(800, 640, 560, "#ffd8a0", .32, .22, sy=.8)
    marble = dict(dark="#a08c98", mid="#efe2da", lit="#fffaf2", rim="#ffffff", light=1, line="#7a6874", door="#ffc060", flag_c="#f08a2a", white=True)
    for side in (-1, 1):
        arch.shikhara_front(s, 800 + side * 300, 812, .62, color="#e6d8d2", rim="#fff8f0", door=None, flag_color="#f08a2a")
        arch.chhatri(s, 800 + side * 410, 812, .9, color="#e0d2cc", rim="#fff8f0")
    nagara_grand(s, 800, 830, .78, **marble)
    s.add(f'<rect x="-20" y="830" width="1640" height="{wl - 830}" fill="{s.lin([(0, "#3a304a", 1), (1, "#241e36", 1)], 0, 830, 0, wl, user=True)}"/>'
          f'<path d="M-20 830H1640" stroke="#ffe8c8" stroke-opacity=".4" stroke-width="2"/>')
    for x in range(120, 1600, 160):
        s.glow(x, 846, 14, "#ffc070", .9, .3)
    s.fx("reflect", y0=wl, strength=.85, tint="#100c22", tint_near=.5, tint_far=.1, amp=2.4)
    s.wisps(10, -100, W + 100, wl + 6, wl + 50, "#d8a8c0", a=(.06, .14), length=(300, 800), thick=(4, 10), blur=8, seed=4)
    s.motes(26, 400, 1200, 300, 800, seed=5, size=(.6, 1.6))
    s.fx("mottle", amp=.04, cell=60)
    s.look = {"vibrance": .1}
    return s


# =====================================================================================
# 11. the four abodes
# =====================================================================================
def small_badrinath(s, cx, base, sc=1.0):
    """Badrinath's bright painted facade: an arched gateway, flanking bays and a small gilded roof."""
    S = sc
    out = (f'<path d="M{f(cx - 60 * S)} {f(base)}V{f(base - 50 * S)}H{f(cx + 60 * S)}V{f(base)}Z" fill="#c8a080"/>'
           f'<path d="M{f(cx - 28 * S)} {f(base)}V{f(base - 74 * S)}Q{f(cx)} {f(base - 100 * S)} {f(cx + 28 * S)} {f(base - 74 * S)}V{f(base)}Z" fill="#d84a3a"/>'
           f'<path d="M{f(cx - 16 * S)} {f(base)}V{f(base - 56 * S)}Q{f(cx)} {f(base - 72 * S)} {f(cx + 16 * S)} {f(base - 56 * S)}V{f(base)}Z" fill="#ffd890"/>'
           f'<path d="M{f(cx - 60 * S)} {f(base - 50 * S)}H{f(cx + 60 * S)}" stroke="#3a6ab0" stroke-width="{f(5 * S)}"/>'
           f'<path d="M{f(cx - 20 * S)} {f(base - 92 * S)}C{f(cx - 22 * S)} {f(base - 118 * S)} {f(cx + 22 * S)} {f(base - 118 * S)} {f(cx + 20 * S)} {f(base - 92 * S)}Z" fill="#f4c860"/>'
           f'<path d="M{f(cx)} {f(base - 116 * S)}V{f(base - 140 * S)}" stroke="#3a2a28" stroke-width="{f(1.6 * S)}"/>' + arch.flag(cx, base - 140 * S, 26 * S, 12 * S, "#f07a1e"))
    s.add(out)


@scene
def char_dham(s):
    hz = 330
    sun = (1440, 318)
    s.sky([(0, "#1a1e4c"), (.12, "#34346c"), (.22, "#8a5a8a"), (.29, "#f0a08a"), (.33, "#ffe0b8")])
    s.stars(40, 0, 150, seed=91, bright=.5)
    s.sun(*sun, 30, halo_r=640, halo_a=.85)
    s.fx("clouds", y0=10, y1=220, seed=201, cell=160, aniso=4, cover=.4, soft=.2, lit="#ffbca8", body=.72, direct=.8,
         light=(.8, 1), sun=(sun[0], sun[1], 500), opacity=.85)
    # the seas: western on the left, eastern on the right (sunrise), southern in front
    s.fx("reflect", y0=hz, strength=.92, tint="#2a1e48", tint_near=.45, tint_far=.04, amp=2)
    s.fx("glints", y0=hz, cx=sun[0], color="#fff0c8", width=50, strength=1.1, scatter=.05, density=.5, spread=2.6)
    # the land: wide in the north, narrowing to the southern tip near us
    def coast(ctrl, seed, amp=10):
        pts = smooth_line(ctrl, 5)
        rr = random.Random(seed)
        ph = [rr.uniform(0, 6) for _ in range(3)]
        out = []
        for i, (x, y) in enumerate(pts):
            k = (y - 372) / 580
            out.append((x + (math.sin(i * .21 + ph[0]) * 1.0 + math.sin(i * .07 + ph[1]) * 1.6) * amp * (.3 + k), y))
        return out
    lc = coast([(150, 372), (250, 420), (330, 500), (420, 600), (520, 700), (610, 800), (700, 890), (770, 940)], 1)
    rc = coast([(1460, 372), (1340, 430), (1250, 520), (1150, 640), (1040, 760), (930, 860), (840, 930)], 2)
    land_d = pts_d(lc + rc[::-1])
    land = s.lin([(0, "#7a6478", 1), (.2, "#4e4660", 1), (.6, "#2e3044", 1), (1, "#1e2032", 1)], 0, 372, 0, 950, user=True)
    s.add(f'<path d="{land_d}" fill="{land}"/>')
    rng = random.Random(3)
    woods = "".join(f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(4 + (y - 360) * .05)}" ry="{f(1.5 + (y - 360) * .02)}"/>'
                    for x, y in [(rng.uniform(150, 1460), rng.uniform(380, 940)) for _ in range(800)])
    lit_side = s.lin([(0, "#ffb890", 0), (.7, "#ffb890", .0), (1, "#ffc8a0", .35)], 150, 0, 1460, 0, user=True)
    s.add(f'<g clip-path="{s.clip(land_d)}"><rect width="1600" height="1000" fill="{lit_side}"/>'
          f'<g fill="#0e1018" opacity=".22" filter="{s.blur(3)}">{woods}</g>'
          f'<path d="M{"L".join(f"{f(x + 30 + (y - 372) * .06)} {f(y)}" for x, y in lc)}" stroke="#141422" stroke-opacity=".6" stroke-width="40" fill="none" filter="{s.blur(14)}"/>'
          f'<path d="M{"L".join(f"{f(x + 24)} {f(y)}" for x, y in lc)}" stroke="#ffd0a8" stroke-opacity=".25" stroke-width="6" fill="none" filter="{s.blur(6)}"/>'
          f'<path d="M{"L".join(f"{f(x)} {f(y)}" for x, y in rc)}" stroke="#fff0d0" stroke-opacity=".7" stroke-width="10" fill="none" filter="{s.blur(5)}"/></g>')
    s.add(f'<path d="M{"L".join(f"{f(x)} {f(y)}" for x, y in lc)}" stroke="#ffe0c0" stroke-opacity=".7" stroke-width="2" fill="none"/>'
          f'<path d="M{"L".join(f"{f(x)} {f(y)}" for x, y in rc)}" stroke="#fff4e0" stroke-opacity=".9" stroke-width="2.4" fill="none"/>')
    s.add(f'<ellipse cx="800" cy="958" rx="46" ry="8" fill="#2a2438"/><path d="M754 958Q800 948 846 958" stroke="#fff0d0" stroke-opacity=".7" stroke-width="2" fill="none"/>')
    # the Ganga, from the mountains to the eastern sea
    river(s, [(780, 400), (840, 430), (930, 450), (1040, 470), (1140, 500), (1250, 530)], 4, 12, near="#c08aa0", far="#fff0c8",
          mid="#ffd0a8", y_near=560, y_far=400, sparkle=60, seed=4, glint_x=1300, glint_w=300)
    # the Himalaya across the north, Badrinath beneath its peaks
    him = peak_line(400, [(800, 150, 200), (560, 110, 160), (1040, 120, 170), (360, 70, 140), (1250, 80, 150)], 202,
                    x0=180, x1=1430, step=3, shape=1.25, shoulders=2)
    him = [(x, min(y, 400)) for x, y in him]
    mk = s.mark()
    mountains(s, him, "#8c7ab0", "#9a7aa0", lit="#ffcab0", lit_a=.8, light=1, seed=203, snow="#ccc0e4", snow_shade="#a294c8",
              lit_snow="#fff2e8", snowline=330, snow_fingers=40, rim="#fff2dc", rim_center=sun, rim_r=900, haze="#e8b8b8",
              haze_a=.5, haze_h=60, base_y=400)
    inner = "".join(s.body[mk:])
    del s.body[mk:]
    s.add(f'<g clip-path="{s.clip("M0 0H1600V403H0Z")}">{inner}</g>')
    s.mist(400, 30, "#f0c0b8", .6, 8, x0=180, x1=1430)
    halo = lambda x, y, r: s.glow(x, y, r, "#ffd090", .7, .25)
    halo(800, 380, 110)
    small_badrinath(s, 800, 402, .42)
    halo(430, 560, 140)
    nagara_grand(s, 430, 590, .28, dark="#4a2c3a", mid="#a87060", lit="#ffd0a0", rim="#fff0d8", light=1, flag_c="#f05a1e")
    halo(1175, 560, 150)
    rekha_deula(s, 1175, 610, .3, dark="#3a2432", mid="#8a5a58", lit="#ffd8b0", rim="#fff2dc", light=1)
    halo(800, 830, 170)
    gopuram(s, 800, 948, .36, dark="#4a2c34", mid="#a8705a", lit="#ffcc98", rim="#fff2d8", light=1, line="#2a1420")
    # a faint ring of lamps: the pilgrimage that joins the four
    ring = []
    for k in range(64):
        a = 2 * math.pi * k / 64
        x, y = 800 + math.cos(a) * 375, 670 + math.sin(a) * 270
        ring.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="2" fill="#fff0c0"/><circle cx="{f(x)}" cy="{f(y)}" r="7" fill="#ffb050" opacity=".3"/>')
    s.add(f'<g style="mix-blend-mode:screen" opacity=".55">{"".join(ring)}</g>')
    s.wisps(10, -100, W + 100, hz + 6, hz + 60, "#ffd8c8", a=(.06, .16), length=(300, 800), thick=(4, 12), blur=8, seed=5)
    s.birds(6, 1180, 1380, 220, 280, color="#4a2a44", s=(5, 9), seed=6, a=.8)
    s.fx("godrays", cx=sun[0], cy=sun[1], strength=.4, thresh=.72, decay=.972, radius=260)
    s.fx("mottle", amp=.045, cell=60)
    return s


# =====================================================================================
# 15. the banyan
# =====================================================================================
def _foliage(img, blobs, seed=1, dark="#14180e", mid="#3a4a22", lit="#c8b05a", rim="#ffe0a0", sun=(300, 500), light=(-.7, -.5),
             cell=46, holes=.35, edge=.6):
    """A dense tree canopy painted in raster: soft blob masses broken by leafy noise, lit from the
    sun's side and from above, dark beneath, with sky showing through small gaps and glowing
    edges where the light comes through."""
    H_, W_, _ = img.shape
    xs0 = int(max(0, min(b[0] - b[2] for b in blobs) - 60)); xs1 = int(min(W_, max(b[0] + b[2] for b in blobs) + 60))
    ys0 = int(max(0, min(b[1] - b[3] for b in blobs) - 60)); ys1 = int(min(H_, max(b[1] + b[3] for b in blobs) + 60))
    h, w = ys1 - ys0, xs1 - xs0
    yy, xx = np.mgrid[ys0:ys1, xs0:xs1].astype(np.float32)
    m = np.zeros((h, w), np.float32)
    for cx, cy, rx, ry in blobs:
        m = np.maximum(m, 1 - ((xx - cx) / rx) ** 2 - ((yy - cy) / ry) ** 2)
    clump = fx.fbm(h, w, cell, 5, seed, aniso=1.4)
    leaf = fx.fbm(h, w, max(3, cell * .12), 3, seed + 5, aniso=1.0)
    dens = m * 1.5 + (clump - .5) * 1.3 + (leaf - .5) * edge
    a = fx.smooth(.3, .42, dens) * fx.smooth(-.05, .2, m)
    gap = fx.smooth(.62, .7, fx.fbm(h, w, cell * .5, 4, seed + 9)) * fx.smooth(.2, .6, m) * holes
    a = np.clip(a - gap * fx.smooth(.4, .6, leaf), 0, 1)
    bump = ndimage.gaussian_filter(clump * 1.0 + leaf * .25, 2)
    gy, gx = np.gradient(bump)
    lx, ly = light
    shade = np.clip(.5 + (gx * lx + gy * ly) * 26, 0, 1)
    top = np.clip(1 - (yy - ys0) / max(1, h), 0, 1)
    tone = np.clip(shade * .55 + top * .3 - .22 + (clump - .5) * .4, 0, 1)
    col = fx.rgb(dark) + (fx.rgb(mid) - fx.rgb(dark)) * np.clip(tone * 1.6, 0, 1)[..., None]
    col = col + (fx.rgb(lit) - col) * (np.clip(tone - .62, 0, 1) * 2.2)[..., None]
    sx, sy = sun
    near = np.exp(-(((xx - sx) ** 2 + (yy - sy) ** 2) / (2 * 420 ** 2)))
    edge_m = np.clip(a * (1 - fx.smooth(.42, .7, dens)) * 3, 0, 1)
    col = col + (fx.rgb(rim) - col) * (edge_m * near * .9)[..., None]
    reg = img[ys0:ys1, xs0:xs1]
    img[ys0:ys1, xs0:xs1] = reg * (1 - a[..., None]) + col * a[..., None]
    return img


fx.EFFECTS["foliage"] = _foliage


def limb(pts, w0, w1):
    return ribbon(smooth_line(pts, 4), w0, w1)


@scene
def banyan(s):
    sun = (300, 560)
    ground = 830
    s.sky([(0, "#2a2a5a"), (.2, "#4a3e74"), (.4, "#a86e88"), (.52, "#f4a47e"), (.6, "#ffd094"), (.66, "#ffeec4")])
    s.sun(*sun, 40, halo_r=760, halo_a=.9)
    s.fx("clouds", y0=20, y1=280, seed=211, cell=170, aniso=3.8, cover=.38, soft=.2, lit="#ffc0a0", body=.74, direct=.85,
         light=(-.6, 1), sun=(sun[0], sun[1], 520), opacity=.8)
    far = ridgeline(700, 40, 212, cell=240, octaves=5, ridged=.3)
    hills(s, far, "#b08098", "#c8949a", haze="#ffd0b0", haze_a=.5)
    rng = random.Random(6)
    s.add(f'<path d="{"".join(crown(x, y_at(far, x) - rng.uniform(4, 10), rng.uniform(8, 18), seed=int(x)) for x in range(-20, 1640, 16) if rng.random() < .6)}" fill="#9a6a86" filter="{s.blur(1.4)}"/>')
    s.mist(720, 90, "#ffd8b8", .6, 20)
    fld = s.lin([(0, "#b07a6a", 1), (.3, "#6a4a40", 1), (1, "#22161c", 1)], 0, 740, 0, 1000, user=True)
    s.add(f'<rect x="-20" y="740" width="1640" height="280" fill="{fld}"/>')
    s.glow(sun[0], 760, 800, "#ffb070", .4, .2, sy=.25)
    bark = s.lin([(0, "#2e1e1c", 1), (.35, "#181012", 1), (1, "#0e0a0c", 1)], 640, 0, 1000, 0, user=True)
    # trunk, great limbs and pillar roots (behind the leaves)
    trunk = (f"M700 {ground + 6}C730 760 740 700 742 620C744 560 720 520 690 480L760 470C790 520 806 560 820 560"
             f"C836 560 850 520 880 470L950 480C914 530 896 580 896 640C898 720 910 770 950 {ground + 6}Z")
    limbs = [limb([(760, 520), (620, 470), (460, 450), (300, 460), (170, 490)], 60, 16),
             limb([(880, 520), (1020, 470), (1180, 450), (1340, 460), (1480, 500)], 60, 16),
             limb([(800, 540), (760, 420), (700, 330), (640, 260)], 50, 14),
             limb([(840, 540), (900, 420), (980, 330), (1060, 280)], 50, 14),
             limb([(560, 462), (520, 380), (450, 320)], 24, 8), limb([(1260, 456), (1300, 380), (1380, 330)], 24, 8)]
    s.add(f'<path d="{trunk}{"".join(limbs)}" fill="{bark}"/>')
    pillars = [(260, 470, 26), (420, 456, 32), (1140, 455, 30), (1300, 460, 36), (1440, 484, 22)]
    strands = []
    for x, y, w_ in pillars:
        for j in range(4):
            o = (j - 1.5) / 1.5
            xb = x + o * w_ * .35 + rng.uniform(-4, 4)
            sw = w_ * rng.uniform(.25, .4)
            strands.append(f'<path d="M{f(x + o * w_ * .2)} {f(y)}C{f(x + o * w_ * .3 + rng.uniform(-8, 8))} {f(y + 140)} {f(xb + rng.uniform(-10, 10))} {f(ground - 120)} {f(xb + o * w_ * .4)} {f(ground + 6)}" '
                           f'stroke="{"#1a1012" if j % 2 else "#2a1c18"}" stroke-width="{f(sw)}" fill="none" stroke-linecap="round"/>')
        strands.append(f'<path d="M{f(x - w_ * .3)} {f(y)}C{f(x - w_ * .4)} {f(y + 140)} {f(x - w_ * .9)} {f(ground - 120)} {f(x - w_ * 1.1)} {f(ground + 6)}" stroke="#ffc890" stroke-opacity=".3" stroke-width="1.6" fill="none"/>')
    s.add("".join(strands))
    tr = []
    for j in range(22):
        x0_ = 712 + j * 10 + rng.uniform(-4, 4)
        tr.append(f"M{f(x0_)} {f(ground + 4)}C{f(x0_ + rng.uniform(-10, 10))} {f(720)} {f(x0_ + rng.uniform(-14, 14))} {f(600)} {f(790 + (x0_ - 820) * .5)} {f(500)}")
    s.add(f'<path d="{"".join(tr)}" stroke="#0e0a0a" stroke-opacity=".55" stroke-width="3" fill="none"/>'
          f'<path d="{"".join(tr[:5])}" stroke="#c89068" stroke-opacity=".25" stroke-width="1.6" fill="none" transform="translate(-3 0)"/>')
    blobs = [(800, 300, 330, 190), (520, 380, 300, 130), (1100, 370, 320, 140), (300, 440, 220, 90), (1340, 440, 240, 95),
             (680, 220, 200, 110), (960, 230, 220, 120), (150, 480, 140, 60), (1480, 485, 150, 60), (800, 430, 560, 110)]
    s.fx("foliage", blobs=blobs, seed=13, dark="#0e0f0c", mid="#2a3020", lit="#b09850", rim="#ffdc98", sun=sun, light=(-.75, -.55), cell=50)
    # hanging aerial roots in front of the leaves' lower edge
    roots = []
    for k in range(120):
        x = rng.uniform(150, 1480)
        y0 = 470 + rng.uniform(-20, 30) - 40 * math.exp(-((x - 800) / 300) ** 2)
        L = rng.uniform(40, 300) if rng.random() < .8 else ground - y0
        sway = rng.uniform(-6, 6)
        roots.append(f"M{f(x)} {f(y0)}Q{f(x + sway)} {f(y0 + L * .5)} {f(x + sway * .4)} {f(y0 + L)}")
    s.add(f'<path d="{"".join(roots)}" stroke="#2a1c18" stroke-width="1.8" fill="none" opacity=".8"/>'
          f'<path d="{"".join(roots[:40])}" stroke="#ffc890" stroke-width="1" fill="none" opacity=".25" transform="translate(-1.2 0)"/>')
    # the stone platform round the trunk, red threads, a small shrine and its lamp
    s.add(f'<path d="M560 {ground + 10}L590 {ground - 20}H1060L1090 {ground + 10}Z" fill="{s.lin([(0, "#8a6050", 1), (1, "#3a2420", 1)], 0, ground - 20, 0, ground + 10, user=True)}"/>'
          f'<path d="M590 {ground - 20}H1060" stroke="#ffd8b0" stroke-opacity=".6" stroke-width="2"/>')
    s.add(f'<path d="M712 690Q820 712 920 690M716 702Q820 724 922 702M720 714Q820 736 924 714" stroke="#d8302a" stroke-width="2.4" fill="none" opacity=".9"/>'
          f'<path d="M714 696Q820 718 920 696" stroke="#f0c040" stroke-width="1.6" fill="none" opacity=".8"/>')
    arch.shikhara_front(s, 980, ground - 18, .34, color="#5a3a34", rim="#ffd8b0", door="#ffc060", flag_color="#f07a1e")
    s.add(f'<ellipse cx="860" cy="{ground - 24}" rx="18" ry="5" fill="#8a3a14"/>')
    s.flame(860, ground - 28, 26, glow_r=200, glow_a=.6)
    s.glow(860, ground - 30, 160, "#ffb050", .35, .25)
    s.add(ob.marigold(810, ground - 24, 8, "#f39a1c", 2) + ob.marigold(900, ground - 22, 7, "#f7c02a", 3))
    grass(s, -20, 1640, lambda x: 960 + 30 * math.sin(x / 200), 260, h=(10, 40), color="#1a1014", seed=4)
    s.birds(9, 860, 1300, 140, 260, color="#3a2430", s=(6, 11), seed=8, a=.85)
    s.motes(40, 200, 1400, 300, 800, seed=4, size=(.7, 1.8))
    s.fx("godrays", cx=sun[0], cy=sun[1], strength=.55, thresh=.7, decay=.975, radius=380)
    s.fx("mottle", amp=.045, cell=60)
    return s
