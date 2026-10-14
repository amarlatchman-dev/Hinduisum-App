"""Paintings of the deities, shown through their emblems, places, light and sacred animals,
and of the cosmic and calendrical themes (Sri Yantra, gunas, wheels, the moon)."""
import math
import random

import numpy as np

import arch
import fx
import objects as ob
from land import crown, grass, hills, mountains, peak_line, pines, ribbon, ridgeline, round_tree, smooth_line, y_at
from paint import H, W, f, mix, pts_d
from scenes import scene

GOLD = [(0, "#fff6d2"), (0.35, "#f7d27a"), (0.7, "#d99a35"), (1, "#a5641d")]
PALE_GOLD = [(0, "#fffbea"), (0.4, "#fbe3a4"), (0.75, "#e0ad55"), (1, "#b07a2c")]


# =====================================================================================
# raster effects
# =====================================================================================
def _nebula(img, seed=1, cell=320, colors=("#3a2a8a", "#b0407a", "#ffb070"), strength=0.7, cx=800, cy=500,
            r=900, y0=0, y1=None, cover=0.45, dark=0.0, warp=60, aniso=1.0, falloff=1.6):
    """Soft glowing gas: fbm density, coloured through a ramp, screened onto the image,
    fading with distance from (cx, cy). dark > 0 adds dusty lanes that dim what is behind."""
    Hh, Ww, _ = img.shape
    y1 = Hh if y1 is None else y1
    h = y1 - y0
    n = fx.fbm(h, Ww, cell, 6, seed, aniso, 0.55)
    wx = (fx.fbm(h, Ww, cell * .7, 3, seed + 5) - .5) * warp
    wy = (fx.fbm(h, Ww, cell * .7, 3, seed + 6) - .5) * warp
    from scipy import ndimage
    yy, xx = np.mgrid[0:h, 0:Ww].astype(np.float32)
    n = ndimage.map_coordinates(n, [np.clip(yy + wy, 0, h - 1), np.clip(xx + wx, 0, Ww - 1)], order=1, mode="reflect")
    n = fx._stretch(n)
    d = np.sqrt((xx - cx) ** 2 + (yy + y0 - cy) ** 2) / r
    env = np.clip(1 - d, 0, 1) ** falloff
    dens = fx.smooth(1 - cover, 1.0, n) * env
    c = fx.fbm(h, Ww, cell * 1.3, 3, seed + 9)
    c = fx._stretch(c)
    ramp = [fx.rgb(k) for k in colors]
    t = np.clip(c * (len(ramp) - 1), 0, len(ramp) - 1.001)
    i = t.astype(int)
    fr = (t - i)[..., None]
    R = np.stack(ramp)
    col = R[i] * (1 - fr) + R[i + 1] * fr
    col = col * (0.55 + 0.9 * dens[..., None])
    glow = np.clip(col * dens[..., None] * strength, 0, 1)
    reg = img[y0:y1]
    if dark:
        lane = fx.smooth(0.55, 0.8, fx._stretch(fx.fbm(h, Ww, cell * .5, 5, seed + 21, aniso * 1.5))) * env
        reg = reg * (1 - dark * lane[..., None])
    img[y0:y1] = 1 - (1 - reg) * (1 - glow)
    return img


def _starfield(img, n=4000, seed=1, y0=0, y1=None, cx=None, cy=None, r=None, bright=1.0, tint=0.25):
    """Thousands of fine stars, denser and brighter towards (cx, cy) when given."""
    Hh, Ww, _ = img.shape
    y1 = Hh if y1 is None else y1
    rng = np.random.default_rng(seed)
    xs = rng.uniform(0, Ww, n)
    ys = rng.uniform(y0, y1, n)
    if cx is not None:
        ang = rng.uniform(0, 2 * np.pi, n)
        rad = r * rng.random(n) ** 1.8
        k = rng.random(n) < .55
        xs = np.where(k, cx + np.cos(ang) * rad, xs)
        ys = np.where(k, cy + np.sin(ang) * rad * .8, ys)
    m = (xs >= 0) & (xs < Ww - 1) & (ys >= y0) & (ys < y1 - 1)
    xs, ys = xs[m], ys[m]
    b = rng.random(len(xs)) ** 3 * bright
    hue = rng.random(len(xs))
    col = np.where(hue[:, None] < .3, fx.rgb("#ffd9b0"), np.where(hue[:, None] > .8, fx.rgb("#bcd0ff"), fx.rgb("#fff8ee")))
    col = 1 - tint + tint * col
    layer = np.zeros_like(img)
    xi, yi = xs.astype(int), ys.astype(int)
    np.add.at(layer, (yi, xi), col * b[:, None])
    from scipy import ndimage
    layer = layer + ndimage.gaussian_filter(layer, (1.2, 1.2, 0)) * 3
    return 1 - (1 - img) * (1 - np.clip(layer, 0, 1))


def _add_glow(img, cx, cy, r, color="#ffffff", a=1.0, sy=1.0, power=2.0):
    """A true additive (screen) radial glow, unlike an SVG glow drawn over transparency."""
    Hh, Ww, _ = img.shape
    yy, xx = np.mgrid[0:Hh, 0:Ww].astype(np.float32)
    d = np.sqrt(((xx - cx) / r) ** 2 + ((yy - cy) / (r * sy)) ** 2)
    g = np.exp(-d * d * power) * a
    return 1 - (1 - img) * (1 - np.clip(g[..., None] * fx.rgb(color), 0, 1))


def _beam(img, cx, y0, y1, w=40, color="#fff4dc", a=1.0, halo=6.0, taper=0.0):
    """A vertical column of light: a hot core with a wide soft halo, screened on."""
    Hh, Ww, _ = img.shape
    yy, xx = np.mgrid[0:Hh, 0:Ww].astype(np.float32)
    t = np.clip((yy - y0) / max(1, y1 - y0), 0, 1)
    ww = w * (1 - taper * (1 - t))
    dx = np.abs(xx - cx) / ww
    core = np.exp(-dx ** 4 * 2)
    hal = np.exp(-dx / halo) * .55
    inside = ((yy >= y0) & (yy <= y1)).astype(np.float32)
    g = (core + hal) * inside * a
    return 1 - (1 - img) * (1 - np.clip(g[..., None] * fx.rgb(color), 0, 1))


fx.EFFECTS["nebula"] = _nebula
fx.EFFECTS["starfield"] = _starfield
fx.EFFECTS["addglow"] = _add_glow
fx.EFFECTS["beam"] = _beam


# =====================================================================================
# small geometry helpers
# =====================================================================================
def P(pts, close=True):
    return pts_d(pts, close)


def circle_d(cx, cy, r):
    return f"M{f(cx - r)} {f(cy)}A{f(r)} {f(r)} 0 1 0 {f(cx + r)} {f(cy)}A{f(r)} {f(r)} 0 1 0 {f(cx - r)} {f(cy)}Z"


def ellipse_d(cx, cy, rx, ry):
    return f"M{f(cx - rx)} {f(cy)}A{f(rx)} {f(ry)} 0 1 0 {f(cx + rx)} {f(cy)}A{f(rx)} {f(ry)} 0 1 0 {f(cx - rx)} {f(cy)}Z"


def petal_d(w, h, x=0, y=0, rot=0, pinch=0.0, base_w=0.0):
    """A pointed petal from (x, y) outward along angle rot (degrees, 0 = up)."""
    a = math.radians(rot)
    ca, sa = math.cos(a), math.sin(a)

    def T(px, py):
        return (x + px * ca - py * sa, y + px * sa + py * ca)
    pts = [(-base_w, 0), (-w * .62, -h * .12), (-w * .58, -h * (.72 - pinch)), (0, -h), (w * .58, -h * (.72 - pinch)), (w * .62, -h * .12), (base_w, 0)]
    q = [T(*p) for p in pts]
    return (f"M{f(q[0][0])} {f(q[0][1])}C{f(q[1][0])} {f(q[1][1])} {f(q[2][0])} {f(q[2][1])} {f(q[3][0])} {f(q[3][1])}"
            f"C{f(q[4][0])} {f(q[4][1])} {f(q[5][0])} {f(q[5][1])} {f(q[6][0])} {f(q[6][1])}Z")


def rot_pts(pts, ang, cx=0, cy=0):
    a = math.radians(ang)
    c, s_ = math.cos(a), math.sin(a)
    return [(cx + x * c - y * s_, cy + x * s_ + y * c) for x, y in pts]


# =====================================================================================
# gilding: glowing, embossed gold emblems
# =====================================================================================
def gilt(s, parts, x, y, sc=1.0, rot=0.0, glow=0.85, glow_col="#ffb347", halo_col="#ffe2a0", glow_r=26,
         emboss=7, grad=GOLD, az=225, el=42, details="", flip=False, under=None):
    """Draw emblem parts (path strings in local units, or (d, grad) pairs) as burnished,
    embossed gold at (x, y). Each part is embossed separately, back to front, so
    overlapping pieces keep their own edges. details is extra SVG drawn on top."""
    sx = -sc if flip else sc
    t = f"translate({f(x)} {f(y)}) rotate({f(rot)}) scale({f(sx)} {f(sc)})"
    ds = [p if isinstance(p, tuple) else (p, None) for p in parts]
    alld = "".join(d for d, _ in ds)
    if glow:
        s.add(f'<g transform="{t}" filter="{s.blur(glow_r / sc)}" opacity="{glow}" style="mix-blend-mode:screen"><path d="{alld}" fill="{glow_col}"/></g>')
        s.add(f'<g transform="{t}" filter="{s.blur(glow_r * .3 / sc)}" opacity="{glow * .9}" style="mix-blend-mode:screen"><path d="{alld}" fill="{halo_col}"/></g>')
    if under:
        s.add(f'<g transform="{t}">{under}</g>')
    out = []
    for d, gr in ds:
        g = s.lin(gr or grad, 0, 0, .3, 1)
        out.append(f'<path d="{d}" fill="{g}" fill-rule="evenodd" filter="{s.gold_filter(emboss / sc, az=az, el=el)}"/>')
    s.add(f'<g transform="{t}">{"".join(out)}{details}</g>')


# ---------- emblem shapes, in local units ----------
def chakra_d(R=100, teeth=24, spokes=12, swirl=0.35):
    """Sudarshana: a flaming serrated rim, a beaded band, lotus-blade spokes and a hub."""
    parts = []
    ri, ro = R * .8, R
    tooth = []
    for k in range(teeth):
        a0 = 2 * math.pi * k / teeth
        a1 = 2 * math.pi * (k + 1) / teeth
        am = (a0 + a1) / 2 + swirl * (a1 - a0)
        p0 = (math.cos(a0) * ri, math.sin(a0) * ri)
        p1 = (math.cos(a1) * ri, math.sin(a1) * ri)
        tip = (math.cos(am + swirl * .6 * (a1 - a0)) * ro, math.sin(am + swirl * .6 * (a1 - a0)) * ro)
        c0 = (math.cos(a0 + .2 * (a1 - a0)) * (ri + (ro - ri) * .75), math.sin(a0 + .2 * (a1 - a0)) * (ri + (ro - ri) * .75))
        c1 = (math.cos(a1) * (ri + (ro - ri) * .35), math.sin(a1) * (ri + (ro - ri) * .35))
        tooth.append(f"{'M' if k == 0 else 'L'}{f(p0[0])} {f(p0[1])}Q{f(c0[0])} {f(c0[1])} {f(tip[0])} {f(tip[1])}Q{f(c1[0])} {f(c1[1])} {f(p1[0])} {f(p1[1])}")
    ring_outer = "".join(tooth) + "Z"
    parts.append(ring_outer + circle_d(0, 0, R * .64))            # flaming rim with the band, hollow centre
    beads = "".join(circle_d(math.cos(2 * math.pi * k / 32) * R * .72, math.sin(2 * math.pi * k / 32) * R * .72, R * .028) for k in range(32))
    blades = []
    for k in range(spokes):
        a = 360 * k / spokes
        blades.append(petal_d(R * .14, R * .46, 0, 0, a, base_w=R * .02))
        # each blade pushed out from the hub
    sp = []
    for k in range(spokes):
        a = 360 * k / spokes
        rad = math.radians(a - 90)
        ox, oy = math.cos(rad) * R * .18, math.sin(rad) * R * .18
        sp.append(petal_d(R * .13, R * .48, ox, oy, a, base_w=R * .015))
    parts.append("".join(sp))
    parts.append(circle_d(0, 0, R * .2) + circle_d(0, 0, R * .1))
    parts.append(circle_d(0, 0, R * .055))
    return parts, beads


def trishula_d(h=420):
    """Shiva's trident with the shaft's top (the crossbar) at the origin; prongs rise to y=-210,
    the shaft runs down to y=h. Returns (prongs and blades, shaft) path strings."""
    # crescent of the side prongs, joined under the centre
    prong = ("M-64 -168C-72 -128 -86 -76 -70 -40C-56 -10 -26 4 0 6C26 4 56 -10 70 -40C86 -76 72 -128 64 -168"
             "C58 -132 54 -86 44 -60C34 -38 18 -26 0 -24C-18 -26 -34 -38 -44 -60C-54 -86 -58 -132 -64 -168Z")
    # little barbs on the outer side of each prong
    barbs = "M-77 -92L-96 -104L-79 -76ZM77 -92L96 -104L79 -76Z"
    spear = "M0 -214C9 -186 18 -150 16 -112C14 -78 9 -46 7 -22H-7C-9 -46 -14 -78 -16 -112C-18 -150 -9 -186 0 -214Z"
    collar = ellipse_d(0, 14, 20, 7) + ellipse_d(0, 30, 13, 6) + ellipse_d(0, 44, 16, 6)
    shaft = f"M-6.5 40H6.5L6 {f(h - 30)}L0 {f(h)}L-6 {f(h - 30)}Z"
    return [prong + barbs, spear, collar], shaft


def damaru_d(sc=1.0):
    """The hourglass drum, axis vertical, centred on its waist at the origin."""
    w, hh = 46 * sc, 50 * sc
    body = (f"M{f(-w)} {f(-hh)}C{f(-w * .7)} {f(-hh * .5)} {f(-w * .2)} {f(-hh * .12)} {f(-w * .16)} 0"
            f"C{f(-w * .2)} {f(hh * .12)} {f(-w * .7)} {f(hh * .5)} {f(-w)} {f(hh)}H{f(w)}"
            f"C{f(w * .7)} {f(hh * .5)} {f(w * .2)} {f(hh * .12)} {f(w * .16)} 0"
            f"C{f(w * .2)} {f(-hh * .12)} {f(w * .7)} {f(-hh * .5)} {f(w)} {f(-hh)}Z")
    bottom = f"M{f(-w)} {f(hh)}A{f(w)} {f(w * .22)} 0 0 0 {f(w)} {f(hh)}Z"
    return body + bottom, ellipse_d(0, -hh, w, w * .22), f"M{f(-w)} {f(-hh + 6 * sc)}H{f(w)}"


def shankha_d():
    """A right-turning conch held upright, spire at the top (about 230 units tall)."""
    body = ("M0 -118C10 -112 18 -100 24 -88C30 -84 36 -78 40 -68C50 -62 60 -50 66 -36"
            "C80 -24 88 -4 86 18C84 44 70 68 50 86C38 98 24 110 12 124C8 130 2 134 -2 132"
            "C-6 126 -10 114 -18 100C-36 76 -56 46 -62 14C-66 -12 -60 -38 -48 -54"
            "C-40 -66 -30 -76 -22 -84C-16 -98 -8 -110 0 -118Z")
    lip = ("M30 -40C56 -34 72 -12 72 16C72 46 54 72 30 96C22 104 14 114 8 122C10 104 14 88 16 66"
           "C20 30 22 -10 30 -40Z")
    whorls = ("M-22 -84C-6 -78 12 -80 24 -88M-40 -64C-14 -54 18 -58 40 -68M-50 -48C-20 -34 22 -38 56 -48"
              "M-58 -22C-30 -6 0 -8 24 -18")
    ridges = "M-50 10C-40 40 -24 70 -4 104M-34 0C-24 34 -12 66 2 100"
    return body, lip, whorls, ridges


def gada_d(h=360):
    """Kaumodaki, the mace: a ribbed bulbous head on a banded handle; origin at the head's centre."""
    head = ("M0 -86C26 -84 52 -66 58 -34C64 0 54 34 34 52C24 60 12 64 0 64C-12 64 -24 60 -34 52"
            "C-54 34 -64 0 -58 -34C-52 -66 -26 -84 0 -86Z")
    crown = "M-16 -84C-14 -98 -8 -104 0 -122C8 -104 14 -98 16 -84Z" + ellipse_d(0, -88, 22, 7)
    neck = ellipse_d(0, 66, 26, 8) + ellipse_d(0, 80, 18, 6)
    handle = f"M-8 82H8L9 {f(h - 40)}H-9Z"
    grip = "".join(ellipse_d(0, h - 40 - k * 16, 12, 4.5) for k in range(5))
    pommel = ellipse_d(0, h - 28, 16, 12) + f"M-5 {f(h - 18)}L0 {f(h - 2)}L5 {f(h - 18)}Z"
    ribs = "".join(f"M{f(x * .9)} -80C{f(x * 1.9)} -40 {f(x * 1.9)} 20 {f(x * 1.0)} 60" for x in (-30, -15, 0, 15, 30))
    return [handle, grip + pommel, neck, head, crown], ribs


def kamandalu_d():
    """The ascetic's water pot: round belly, narrow neck with a lip, spout and loop handle."""
    belly = ("M-70 -10C-72 -52 -40 -78 -18 -82V-98H18V-82C40 -78 72 -52 70 -10"
             "C68 34 36 58 0 58C-36 58 -68 34 -70 -10Z")
    rim = ellipse_d(0, -100, 28, 8)
    foot = "M-30 52C-26 66 26 66 30 52Z"
    spout = "M54 -40C78 -46 96 -64 110 -92C114 -96 120 -94 118 -88C108 -58 88 -30 62 -18Z"
    handle = "M-26 -104C-40 -160 40 -160 26 -104L18 -104C28 -146 -28 -146 -18 -104Z"
    return [handle, foot, belly, rim, spout]


def lotus_emblem_d(R=100):
    """A front-facing lotus emblem: three rows of petals and a little cup of stamens."""
    back = [petal_d(R * .34, R * .95, 0, 0, a) for a in (-70, -46, 46, 70)]
    mid = [petal_d(R * .36, R * 1.0, 0, 0, a) for a in (-24, 24)]
    top = [petal_d(R * .38, R * 1.05, 0, 0, 0)]
    front = [petal_d(R * .3, R * .62, 0, 0, a) for a in (-100, 100)]
    sepal = f"M{f(-R * .5)} {f(R * .05)}C{f(-R * .3)} {f(R * .28)} {f(R * .3)} {f(R * .28)} {f(R * .5)} {f(R * .05)}C{f(R * .2)} {f(R * .14)} {f(-R * .2)} {f(R * .14)} {f(-R * .5)} {f(R * .05)}Z"
    return back, mid, top, front, sepal


def swan_d():
    """A hamsa on the water facing left, wings softly arched; waterline at y=0 (about 300 wide)."""
    body = ("M-112 -34C-114 -18 -108 -6 -96 -2C-40 4 40 4 92 -2C112 -6 128 -22 140 -50"
            "C120 -40 104 -40 96 -44C60 -54 0 -56 -60 -54C-72 -56 -80 -60 -84 -68"
            "C-88 -88 -86 -108 -92 -126C-98 -144 -112 -154 -128 -154C-140 -154 -148 -148 -152 -142"
            "L-180 -132L-150 -128C-144 -132 -136 -134 -128 -130C-118 -124 -114 -110 -112 -92"
            "C-110 -72 -110 -52 -112 -34Z")
    wing = ("M-76 -50C-70 -82 -40 -110 6 -118C46 -124 92 -112 122 -94C138 -84 148 -72 152 -62"
            "C138 -66 124 -64 114 -58C130 -54 140 -46 144 -38C126 -40 110 -36 100 -30"
            "C112 -24 118 -16 120 -10C80 -6 30 -8 -10 -14C-44 -20 -66 -32 -76 -50Z")
    beak = "M-152 -142L-180 -132L-150 -128C-147 -132 -148 -138 -152 -142Z"
    knob = ellipse_d(-150, -141, 6, 5)
    eye = circle_d(-138, -140, 2.4)
    return body, wing, beak, knob, eye


def elephant_d():
    """An Indian elephant side-on facing right, trunk raised high; feet on y=0 (about 330 wide)."""
    near = ("M-140 -196C-110 -232 -60 -248 -20 -246C10 -244 30 -236 46 -240"
            "C60 -262 86 -272 108 -268C130 -264 146 -248 150 -226C154 -212 154 -200 152 -190"
            "C164 -204 178 -226 184 -256C190 -284 184 -312 170 -330C164 -338 170 -346 178 -342"
            "C200 -326 210 -294 206 -258C202 -222 186 -192 168 -170C160 -160 150 -152 140 -148"
            "C134 -144 128 -142 120 -142C118 -130 116 -120 114 -110C116 -72 118 -36 120 0H82"
            "C80 -30 78 -62 74 -92C40 -88 0 -88 -40 -92C-56 -94 -70 -96 -82 -100"
            "C-84 -66 -86 -32 -86 0H-124C-124 -34 -128 -68 -134 -98C-146 -116 -154 -140 -154 -160"
            "C-154 -174 -148 -186 -140 -196Z")
    far = ("M66 -96C64 -64 62 -30 60 -4H36C36 -34 38 -66 40 -94Z"
           "M-100 -100C-104 -66 -108 -32 -110 -4H-134C-134 -36 -132 -68 -128 -100Z")
    ear = "M70 -238C46 -230 34 -204 38 -172C42 -146 58 -128 80 -126C90 -146 96 -180 92 -214C88 -228 80 -236 70 -238Z"
    tusk = "M126 -150C142 -146 162 -146 182 -156C174 -140 150 -134 124 -140Z"
    tail = "M-150 -172C-162 -150 -166 -122 -162 -96L-157 -96C-159 -122 -155 -148 -145 -168Z"
    return near, far, ear, tusk, tail


def _ragged(pts, amp, seed, step=10):
    """Roughen a polyline with alternating tufts, for manes and grass edges."""
    rng = random.Random(seed)
    out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        L = math.hypot(x1 - x0, y1 - y0)
        n = max(1, int(L / step))
        nx, ny = -(y1 - y0) / (L or 1), (x1 - x0) / (L or 1)
        for k in range(n):
            t = k / n
            a = amp * (1 if k % 2 else -.3) * rng.uniform(.4, 1)
            out.append((x0 + (x1 - x0) * t + nx * a, y0 + (y1 - y0) * t + ny * a))
    out.append(pts[-1])
    return out


def lion_d():
    """A lion standing side-on facing right, full mane; feet on y=0 (about 440 wide)."""
    body = [(222, -226), (214, -240), (196, -258), (172, -272), (120, -262), (40, -228), (0, -222), (-60, -212), (-120, -214),
            (-170, -206), (-196, -196), (-212, -176), (-216, -150), (-206, -118), (-190, -74), (-186, -40), (-182, -14), (-190, 0),
            (-150, 0), (-150, -8), (-158, -40), (-162, -74), (-150, -112), (-134, -128), (-90, -124), (-40, -118), (0, -122),
            (40, -128), (52, -110), (60, -70), (62, -30), (58, -10), (54, 0), (100, 0), (100, -8), (92, -14), (88, -40), (90, -80),
            (96, -120), (120, -150), (150, -176), (190, -204), (210, -212)]
    far = [[(64, -118), (58, -70), (54, -30), (52, -10), (48, 0), (14, 0), (14, -8), (22, -14), (28, -40), (30, -80), (28, -118)],
           [(-80, -124), (-92, -80), (-104, -40), (-106, -12), (-102, 0), (-136, 0), (-136, -8), (-130, -14), (-128, -40), (-122, -80), (-110, -124)]]
    mane_pts = [(176, -280), (160, -300), (124, -312), (84, -300), (52, -276), (34, -244), (28, -206), (36, -172), (56, -148),
                (86, -132), (118, -130), (144, -142), (164, -160), (178, -182), (186, -206), (190, -236), (186, -262), (176, -280)]
    mane = P(_ragged(smooth_line(mane_pts, 5), 12, 4, 8))
    tail = ("M-196 -190C-224 -180 -240 -150 -248 -118C-254 -94 -256 -70 -266 -56C-272 -48 -280 -46 -286 -48"
            "C-280 -56 -274 -66 -270 -80C-262 -106 -254 -138 -240 -160C-228 -176 -212 -186 -198 -196Z")
    tuft = P(_ragged([(-268, -58), (-292, -36), (-300, -62), (-280, -74), (-268, -58)], 5, 9, 6))
    ear = ellipse_d(166, -284, 8, 10)
    return P(smooth_line(body, 4)) + ear, tail + tuft + "".join(P(smooth_line(l, 4)) for l in far), mane


# =====================================================================================
# shared scene pieces
# =====================================================================================
STEEL = [(0, "#f4f6ff"), (0.35, "#b8c2e4"), (0.7, "#5a6690"), (1, "#262b46")]
WOOD = [(0, "#c98a52"), (0.45, "#7a4422"), (1, "#2a140a")]


def halo_rings(s, cx, cy, r, color="#ffe2a8", a=0.3, n=3, gap=0.12, width=1.6, dots=0):
    out = []
    for k in range(n):
        rr = r * (1 + gap * k)
        out.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(rr)}" fill="none" stroke="{color}" stroke-opacity="{a * (1 - k * .28):.2f}" stroke-width="{width}"/>')
    for k in range(dots):
        ang = 2 * math.pi * k / dots
        out.append(f'<circle cx="{f(cx + math.cos(ang) * r * (1 + gap * n))}" cy="{f(cy + math.sin(ang) * r * (1 + gap * n))}" r="1.8" fill="{color}" opacity="{a * 1.2:.2f}"/>')
    s.add(f'<g style="mix-blend-mode:screen">{"".join(out)}</g>')


def trishula(s, x, y, sc=1.0, h=420, grad=GOLD, glow=0.8, glow_col="#ffb347", halo_col="#ffe2a0", az=225, el=42, cloth=None, damaru=True):
    """Shiva's trident with its damaru and an optional cloth; (x, y) is the crossbar."""
    tp, shaft = trishula_d(h)
    gilt(s, [shaft] + tp, x, y, sc, glow=glow, glow_col=glow_col, halo_col=halo_col, grad=grad, az=az, el=el, emboss=7)
    if cloth:
        c1, c2 = cloth
        t = f"translate({f(x)} {f(y)}) scale({f(sc)})"
        d = ("M-6 58C-30 52 -60 60 -92 78C-120 94 -146 96 -170 88C-150 106 -122 112 -96 104C-110 120 -132 130 -150 132"
             "C-120 140 -86 130 -60 108C-40 92 -20 80 -6 76Z")
        knot = ellipse_d(0, 66, 12, 10)
        g = s.lin([(0, c1, 1), (1, c2, 1)], 0, 0, 1, 0)
        s.add(f'<g transform="{t}"><path d="{d}" fill="{g}"/><path d="{d}" fill="none" stroke="#000" stroke-opacity=".25" stroke-width="2"/>'
              f'<path d="M-30 70C-60 74 -90 88 -120 100M-20 80C-50 92 -80 110 -110 120" stroke="#000" stroke-opacity=".18" stroke-width="3" fill="none"/>'
              f'<path d="{knot}" fill="{c1}"/></g>')
    if damaru:
        db, dt, dbm = damaru_d(.8)
        dx, dy = x + 8 * sc, y + 130 * sc
        cord = f'<path d="M{f(x - 6 * sc)} {f(y + 70 * sc)}Q{f(x - 20 * sc)} {f(y + 96 * sc)} {f(dx)} {f(dy)}M{f(x + 6 * sc)} {f(y + 70 * sc)}Q{f(x + 26 * sc)} {f(y + 90 * sc)} {f(dx)} {f(dy)}" stroke="#d8b070" stroke-width="{f(2.2 * sc)}" fill="none"/>'
        s.add(cord)
        gilt(s, [(db, WOOD), (dt, [(0, "#fffaf0"), (1, "#d8c4a0")])], dx, dy, sc, rot=-6,
             glow=0, emboss=5, az=az, el=el,
             details=f'<path d="M-30 -36L4 0L-30 36M30 -36L-4 0L30 36" stroke="#f0d8a0" stroke-opacity=".55" stroke-width="1.6" fill="none"/>'
                     f'<path d="{dbm}" stroke="#3a1a08" stroke-opacity=".4" stroke-width="2"/>')
        # the two beads on their strings
        for side in (-1, 1):
            bx, by = dx + side * 52 * sc, dy + 18 * sc
            s.add(f'<path d="M{f(dx)} {f(dy)}Q{f(dx + side * 30 * sc)} {f(dy + 18 * sc)} {f(bx)} {f(by)}" stroke="#c8a070" stroke-width="{f(1.4 * sc)}" fill="none"/>'
                  f'<circle cx="{f(bx)}" cy="{f(by)}" r="{f(5 * sc)}" fill="#e8c890"/>')


def chakra(s, x, y, R=100, glow=0.9, rot=0.0, az=225, **kw):
    parts, beads = chakra_d(100)
    gilt(s, parts, x, y, R / 100, rot=rot, glow=glow, az=az, details=f'<path d="{beads}" fill="#fff3c0" opacity=".85"/>', **kw)


def shankha(s, x, y, sc=1.0, rot=0.0, glow=0.85, az=225, **kw):
    body, lip, whorls, ridges = shankha_d()
    gilt(s, [(body, [(0, "#fffaf0"), (0.4, "#fbe6b8"), (0.8, "#e2b060"), (1, "#a8702a")]), (lip, [(0, "#ffe8d0"), (0.6, "#f0b48a"), (1, "#a0602a")])],
         x, y, sc, rot=rot, glow=glow, az=az, details=f'<path d="{whorls + ridges}" stroke="#8a5a20" stroke-opacity=".45" stroke-width="2.4" fill="none"/>', **kw)


def gada(s, x, y, sc=1.0, rot=0.0, glow=0.85, h=330, az=225, **kw):
    gp, ribs = gada_d(h)
    gilt(s, gp, x, y, sc, rot=rot, glow=glow, az=az, details=f'<path d="{ribs}" stroke="#7a4a14" stroke-opacity=".45" stroke-width="3" fill="none"/>', **kw)


def padma(s, x, y, R=100, glow=0.85, az=225, **kw):
    back, mid, top, front, sep = lotus_emblem_d(100)
    parts = [(d, GOLD) for d in back] + [(d, PALE_GOLD) for d in mid] + [(top[0], PALE_GOLD)] + [(d, GOLD) for d in front] + [(sep, GOLD)]
    gilt(s, parts, x, y, R / 100, glow=glow, az=az, **kw)


# =====================================================================================
# 11. Sri Yantra
# =====================================================================================
# (base, apex) as divisions of the vertical diameter (48 from top), base half-width (None:
# a chord to the circle). Four upward and five downward triangles, each apex resting on the
# base of the next; it divides into the 43 triangles with the bindu in the central one.
SY = [(6, 48, None), (12, 42, None), (42, 0, None), (36, 6, None),
      (17, 36, .511), (30, 12, .667), (20, 30, .709), (27, 17, .404), (23, 27, .223)]


def sy_triangles(cx, cy, R):
    out = []
    for b, a, hw in SY:
        yb, ya = 1 - b / 24, 1 - a / 24
        if hw is None:
            hw = math.sqrt(1 - yb * yb)
        out.append([(cx, cy - ya * R), (cx + hw * R, cy - yb * R), (cx - hw * R, cy - yb * R)])
    return out


def bhupura_d(cx, cy, h, gate, depth):
    """The square enclosure with a T-shaped gate on each side."""
    g2, d2 = gate * 1.55, depth * .55
    side = [(-h, -h), (-gate, -h), (-gate, -h - depth + d2), (-g2, -h - depth + d2), (-g2, -h - depth), (g2, -h - depth),
            (g2, -h - depth + d2), (gate, -h - depth + d2), (gate, -h)]
    pts = []
    for k in range(4):
        pts += rot_pts(side, 90 * k)
    pts = [(cx + x, cy + y) for x, y in pts]
    return P(pts)


def ring_petals_d(cx, cy, n, r1, r2, off=0.0, width=1.0, inner=False):
    """A ring of pointed lotus petals between radii r1 and r2 (inner=True: the inner outline)."""
    out = []
    for i in range(n):
        a = 2 * math.pi * i / n + off - math.pi / 2
        da = math.pi / n * width * (.62 if inner else 1)
        rr2 = r1 + (r2 - r1) * (.8 if inner else 1)

        def pt(r, ang):
            return f"{f(cx + math.cos(ang) * r)} {f(cy + math.sin(ang) * r)}"
        out.append(f"M{pt(r1, a - da)}C{pt(r1 + (rr2 - r1) * .55, a - da * 1.08)} {pt(r1 + (rr2 - r1) * .88, a - da * .42)} {pt(rr2, a)}"
                   f"C{pt(r1 + (rr2 - r1) * .88, a + da * .42)} {pt(r1 + (rr2 - r1) * .55, a + da * 1.08)} {pt(r1, a + da)}")
    return "".join(out)


@scene
def sri_yantra(s):
    cx, cy, R = 800, 500, 205
    s.add(f'<rect width="{W}" height="{H}" fill="{s.rad([(0, "#5c1430", 1), (0.38, "#2c0f34", 1), (0.75, "#120a2c", 1), (1, "#07061a", 1)], cx, cy, 980, user=True)}"/>')
    s.fx("nebula", seed=7, cell=260, colors=("#3a1260", "#8a1840", "#c8502a", "#5a1a6a"), strength=.45, cx=cx, cy=cy, r=950, cover=.55, dark=.25, falloff=.8)
    s.fx("starfield", n=1800, seed=3, bright=.7, cx=cx, cy=cy, r=900)
    s.rays(cx, cy, n=40, length=900, width=.02, color="#ffb070", a=.12, seed=3, blur=5)
    s.glow(cx, cy, 620, "#ff7a3a", .3, .25)
    s.glow(cx, cy, 300, "#ffb060", .16, .3)
    gold = s.lin([(0, "#fff2c8", 1), (0.4, "#f2c76a", 1), (0.75, "#d0902e", 1), (1, "#9a5a1a", 1)], cx - 450, cy - 450, cx + 450, cy + 450, user=True)
    fil = s.gold_filter(3.2, az=225, el=48)
    # the square, three lines with four gates
    hq = R * 2.0
    bh = "".join(bhupura_d(cx, cy, hq - k * 13, 46 - k * 6, 48) for k in range(3))
    s.add(f'<path d="{bhupura_d(cx, cy, hq, 46, 48)}" fill="#3a0c22" fill-opacity=".35"/>')
    # three circles and the lotus rings
    r16a, r16b = R * 1.36, R * 1.68
    r8a, r8b = R * 1.04, R * 1.34
    petal_fill = s.rad([(0, "#ff9a6a", .0), (0.55, "#c8304a", .32), (0.8, "#e85a5a", .45), (1, "#ffb080", .5)], cx, cy, r16b, user=True)
    s.add(f'<path d="{ring_petals_d(cx, cy, 16, r16a, r16b, math.pi / 16)}" fill="{petal_fill}"/>')
    s.add(f'<path d="{ring_petals_d(cx, cy, 8, r8a, r8b)}" fill="{petal_fill}"/>')
    T = sy_triangles(cx, cy, R)
    tri_fill = s.rad([(0, "#ffb070", .4), (0.3, "#ff6a40", .26), (0.7, "#c8203e", .2), (1, "#8a1032", .16)], cx, cy, R, user=True)
    s.add(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#2a0618" fill-opacity=".55"/>')
    s.add("".join(f'<path d="{P(t)}" fill="{tri_fill}"/>' for t in T))
    lines = (bh + circle_d(cx, cy, R * 1.73) + circle_d(cx, cy, R * 1.78) + circle_d(cx, cy, R * 1.83)
             + ring_petals_d(cx, cy, 16, r16a, r16b, math.pi / 16) + circle_d(cx, cy, r16a)
             + ring_petals_d(cx, cy, 8, r8a, r8b) + circle_d(cx, cy, r8a) + circle_d(cx, cy, R))
    fine = ring_petals_d(cx, cy, 16, r16a, r16b, math.pi / 16, inner=True) + ring_petals_d(cx, cy, 8, r8a, r8b, inner=True)
    tri = "".join(P(t) for t in T)
    s.add(f'<g filter="{s.blur(6)}" opacity=".7" style="mix-blend-mode:screen"><path d="{lines + tri}" stroke="#ff9a40" stroke-width="7" fill="none"/></g>')
    s.add(f'<g filter="{fil}"><path d="{lines}" stroke="{gold}" stroke-width="4.2" fill="none" stroke-linejoin="round"/>'
          f'<path d="{tri}" stroke="{gold}" stroke-width="3.6" fill="none" stroke-linejoin="miter"/>'
          f'<path d="{fine}" stroke="{gold}" stroke-width="2" fill="none" opacity=".75"/></g>')
    # the bindu
    by = cy - R * (2 * (1 - 23 / 24) + (1 - 27 / 24)) / 3
    s.glow(cx, by, 60, "#fff0c8", .8, .2)
    s.add(f'<circle cx="{cx}" cy="{f(by)}" r="6" fill="#fffef6"/>')
    s.motes(40, cx - 480, cx + 480, cy - 460, cy + 460, seed=9, size=(.8, 2))
    s.fx("addglow", cx=cx, cy=by, r=26, color="#fff2d0", a=.7)
    s.fx("mottle", amp=.04, cell=60)
    s.look = {"vignette": .45, "bloom": .6}
    return s


def crescent(s, cx, cy, r, off=(-.42, -.62), color="#fbf4dc", glow="#cdd8ff", glow_r=None, glow_a=.45, shine=.08):
    """A crescent moon: a lit disc masked by an offset dark disc, with a faint earthshine."""
    s.glow(cx, cy, glow_r or r * 7, glow, glow_a, .14)
    m = s.uid("m")
    s.defs.append(f'<mask id="{m}" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="#fff"/>'
                  f'<circle cx="{f(cx + off[0] * r)}" cy="{f(cy + off[1] * r)}" r="{f(r * 1.02)}" fill="#000" filter="{s.blur(max(.6, r * .02))}"/></mask>')
    g = s.rad([(0, "#ffffff", 1), (0.6, color, 1), (1, mix(color, "#c8b890", .4), 1)], cx - off[0] * r * .6, cy - off[1] * r * .6, r * 1.3, user=True)
    s.add(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="#c8d0ff" opacity="{shine}"/>')
    s.add(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{g}" mask="url(#{m})"/>')


def kailash(s, cx, base, height, hw, moon, seed=51):
    """Mount Kailash: a great domed snow peak with banded strata and the vertical gash on its
    south face, between lesser shoulders, lit by the moon from the right."""
    pts = peak_line(base, [(cx, height, hw, 0.0), (cx - hw * .95, height * .5, hw * .6, .2), (cx + hw * .95, height * .55, hw * .65, -.2)],
                    seed, detail=.06, shape=.78, shoulders=0)
    mountains(s, pts, "#7c88c0", "#262e60", lit="#ffffff", lit_a=.95, light=1, seed=seed, snow="#9aa6d8", snow_shade="#4c5894",
              lit_snow="#ffffff", snowline=base + 60, snow_fingers=30, rim="#ffffff", rim_a=.9, rim_center=moon, rim_r=1000,
              haze="#4a5694", haze_a=.75, haze_h=220, base_y=base + 40)
    top = base - height
    clip = s.clip(P(pts + [(pts[-1][0], H), (pts[0][0], H)]))
    bands = []
    for k, t in enumerate((.14, .22, .3, .38, .47, .56, .66)):
        y = top + height * t
        half = hw * (.18 + t * .8)
        bands.append(f'<path d="M{f(cx - half)} {f(y + height * .05)}Q{f(cx)} {f(y - height * .015)} {f(cx + half)} {f(y + height * .05)}" stroke="#1c2350" stroke-width="{f(5 + t * 10)}" fill="none" opacity="{.3 - t * .2:.2f}"/>')
    gash = P([(cx - 4, top + height * .1), (cx + 4, top + height * .1), (cx + 10, top + height * .45), (cx + 16, top + height * .7),
              (cx + 4, top + height * .7), (cx - 2, top + height * .45)])
    s.add(f'<g clip-path="{clip}"><g filter="{s.blur(3)}">{"".join(bands)}</g><path d="{gash}" fill="#1a1f48" opacity=".45" filter="{s.blur(2.5)}"/></g>')
    return pts


@scene
def shiva(s):
    moon = (1220, 150)
    s.sky([(0, "#050922"), (.35, "#0d1844"), (.6, "#1f2e66"), (.75, "#34437e"), (1, "#4a5590")])
    s.stars(180, 0, 520, seed=11, bright=.9)
    crescent(s, *moon, 42, glow_r=440, glow_a=.55)
    s.fx("clouds", y0=30, y1=250, seed=12, cell=120, aniso=4.5, cover=.26, soft=.2, lit="#c8d2f4", body=.85, direct=.7,
         light=(.6, -.4), sun=(moon[0], moon[1], 300), rim="#f2f4ff", opacity=.6)
    far = peak_line(660, [(60, 260, 230), (330, 200, 200, .1), (1330, 230, 230), (1580, 270, 200)], 41, shape=1.25, shoulders=2)
    mountains(s, far, "#56649e", "#262e62", lit="#c4cff4", lit_a=.55, light=1, seed=42, snow="#9eaad8", snow_shade="#606ca6",
              lit_snow="#e6ecff", snowline=520, snow_fingers=50, rim="#f4f6ff", rim_center=moon, rim_r=900, haze="#5a66a0", haze_a=.55, haze_h=140, base_y=680)
    s.mist(640, 120, "#8a96cc", .3, 30)
    kailash(s, 840, 700, 480, 300, moon)
    s.mist(700, 140, "#7d8ac4", .55, 30)
    # the Ganga, pouring from the heavens onto the summit and falling down the shadowed face
    heaven = smooth_line([(930, -20), (900, 80), (870, 160), (848, 224)], 6)
    hm = s.mask_fade(700, -20, 400, 260, 0, 1)
    s.add(f'<g mask="{hm}"><path d="{ribbon(heaven, 170, 40)}" fill="#a8c0ff" opacity=".3" filter="{s.blur(30)}"/>'
          f'<path d="{ribbon(heaven, 50, 14)}" fill="#dfe8ff" opacity=".4" filter="{s.blur(12)}"/>'
          f'<path d="{ribbon(heaven, 14, 6)}" fill="#ffffff" opacity=".35" filter="{s.blur(6)}"/></g>')
    falls = smooth_line([(846, 228), (830, 300), (808, 380), (800, 450), (786, 530), (782, 610), (780, 700)], 5)
    s.add(f'<path d="{ribbon(falls, 60, 110)}" fill="#a8c4ff" opacity=".28" filter="{s.blur(20)}" style="mix-blend-mode:screen"/>')
    for k, (w0, w1, dx, a) in enumerate(((10, 22, 0, .45), (2, 5, -4, .8), (2, 4, 5, .7), (1.5, 3, 0, .9))):
        fl = [(x + dx * math.sin(y / 40 + k * 2), y) for x, y in falls]
        s.add(f'<path d="{ribbon(fl, w0, w1)}" fill="#f4f8ff" opacity="{a}" filter="{s.blur(1.4 + (k == 0) * 4)}"/>')
    s.glow(780, 700, 140, "#cfe0ff", .5, .3, sy=.45)
    s.motes(50, 760, 870, 230, 700, color="#cfe0ff", seed=4, size=(.6, 1.6))
    mid = ridgeline(775, 70, 43, cell=300, octaves=5, ridged=.4, envelope=[(0, 1.2), (650, .4), (1000, .3), (1600, 1)])
    hills(s, mid, "#1c2048", "#0c0e26", rim="#b8c4f0", rim_a=.6, rim_center=moon, rim_r=1100, haze="#4a5590", haze_a=.45, haze_h=60)
    s.mist(770, 80, "#7a88c8", .45, 22)
    river = smooth_line([(780, 712), (800, 760), (860, 820), (920, 890), (960, 1010)], 6)
    s.add(f'<path d="{ribbon(river, 26, 200)}" fill="{s.lin([(0, "#5a6cb0", 1), (1, "#141a40", 1)], 0, 700, 0, 1000, user=True)}" filter="{s.blur(1.5)}"/>')
    s.add(f'<path d="{ribbon([(x - 4, y) for x, y in river], 8, 50)}" fill="#e8f0ff" opacity=".55" filter="{s.blur(6)}"/>')
    s.add(f'<path d="{ribbon([(x - 4, y) for x, y in river], 2, 10)}" fill="#ffffff" opacity=".6" filter="{s.blur(1.5)}"/>')
    near = ridgeline(905, 50, 44, cell=240, octaves=5, ridged=.3, envelope=[(0, 1), (900, .3), (1600, 1.4)])
    near = [(x, y + (60 * math.sin((x - 760) / 380 * math.pi) if 760 < x < 1140 else 0)) for x, y in near]
    s.add(f'<path d="{P(near + [(1640, 1010), (-40, 1010)])}" fill="{s.lin([(0, "#14163a", 1), (1, "#05060c", 1)], 0, 840, 0, 1000, user=True)}"/>')
    s.add(f'<path d="{"M" + "L".join(f"{f(x)} {f(y)}" for x, y in near if x > 1000)}" stroke="#b8c8ff" stroke-opacity=".45" stroke-width="2" fill="none"/>')
    pines(s, 1120, 1640, 0, 14, h=(60, 150), color="#070916", seed=12, ground_fn=lambda x: y_at(near, x))
    grass(s, 1000, 1640, lambda x: y_at(near, x) + 3, 80, h=(8, 26), color="#05060c", seed=6)
    # the rock where the trident stands
    rk = random.Random(5)
    rock = [(x + rk.uniform(-3, 3), y + rk.uniform(-3, 3)) for x, y in smooth_line([(130, 1010), (220, 930), (330, 880), (450, 862), (570, 872), (670, 914), (760, 1010)], 6)]
    s.add(f'<path d="{P(rock)}" fill="{s.lin([(0, "#1c1e3a", 1), (1, "#05060c", 1)], 0, 860, 0, 1000, user=True)}"/>')
    s.add(f'<path d="{"M" + "L".join(f"{f(x)} {f(y)}" for x, y in rock if x > 400)}" stroke="#c8d4ff" stroke-opacity=".55" stroke-width="2.4" fill="none" filter="{s.blur(1)}"/>')
    grass(s, 180, 760, lambda x: y_at(rock, x) + 3, 70, h=(8, 22), color="#05060c", seed=5)
    s.glow(470, 320, 300, "#9fb4ff", .22, .2)
    trishula(s, 470, 390, 1.08, h=450, grad=STEEL, glow=.45, glow_col="#9fb6ff", halo_col="#dfe8ff", az=315, el=40,
             cloth=("#ff8a2a", "#c2361a"))
    s.motes(26, 300, 1300, 300, 900, color="#cfe0ff", seed=8, size=(.8, 2))
    s.fx("godrays", cx=moon[0], cy=moon[1], strength=.25, thresh=.75, decay=.97, radius=220)
    s.fx("mottle", amp=.04, cell=60)
    s.look = {"vignette": .4}
    return s


# =====================================================================================
# 4. Vishnu: the ocean of milk, Shesha's hoods and the four emblems
# =====================================================================================
def tube(s, stamps, light="#7aa0d0", mid="#1d3352", dark="#060c18", band="#0a1424", every=5, rim=None):
    """A thick serpent body stamped as shaded discs along a path. stamps are (x, y, r, depth);
    discs are drawn far to near so loops pass properly in front of and behind each other."""
    g1 = s.rad([(0, light, 1), (0.45, mid, 1), (1, dark, 1)], .42, .3, .72)
    g2 = s.rad([(0, mix(light, band, .35), 1), (0.45, mix(mid, band, .4), 1), (1, dark, 1)], .42, .3, .72)
    out = []
    for k, (x, y, r, d) in sorted(enumerate(stamps), key=lambda e: e[1][3]):
        out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{g2 if (k // every) % 2 else g1}"/>')
    s.add("".join(out))


def coil_stamps(cx, cy, R0=270, turns=2.3, r_body=30, lift=34, squash=.2, rise_to=None):
    """A serpent coiled on the water: an inward spiral that climbs as it stacks, ending at
    the back where the body rises (to rise_to = (x, y)); the tail tapers away at the front."""
    st = []
    n = 900
    for i in range(n):
        t = i / (n - 1)
        th = math.pi * .35 + t * turns * 2 * math.pi
        R = R0 * (1 - .5 * t)
        x = cx + math.cos(th) * R
        y = cy + math.sin(th) * R * squash - lift * t * turns
        r = r_body * (.25 + .75 * min(1, t * 6))
        st.append((x, y, r, math.sin(th) * R * squash - lift * t * turns * .2))
    if rise_to:
        x0, y0, _, _ = st[-1]
        for i in range(1, 160):
            t = i / 159
            x = x0 + (rise_to[0] - x0) * t
            y = y0 + (rise_to[1] - y0) * t
            st.append((x + math.sin(t * 3) * 10, y, r_body * (1 + .25 * t), -999 + t))
    return st


def shesha(s, cx, cy, n=7, spread=15, body="#1d3352", rim="#e8eeff", gold="#ffd890"):
    """The many-hooded serpent's canopy: overlapping cobra hoods fanned from the top of the
    rising body at (cx, cy), their pale undersides lit gold from below."""
    hood = ("M-20 0C-36 -30 -70 -80 -72 -132C-74 -180 -46 -214 -16 -226C-12 -244 12 -244 16 -226"
            "C46 -214 74 -180 72 -132C70 -80 36 -30 20 0Z")
    belly_d = "M-12 -8C-24 -40 -48 -88 -48 -132C-48 -170 -26 -198 0 -206C26 -198 48 -170 48 -132C48 -88 24 -40 12 -8Z"
    scales = "".join(f"M{f(-44 + k * 1.4)} {f(-54 - k * 15)}Q0 {f(-40 - k * 15)} {f(44 - k * 1.4)} {f(-54 - k * 15)}" for k in range(10))
    spect = "M-22 -152C-22 -166 -8 -170 0 -160C8 -170 22 -166 22 -152C22 -140 8 -138 0 -148C-8 -138 -22 -140 -22 -152Z"
    hg = s.lin([(0, "#4a6e98", 1), (0.5, body, 1), (1, "#081020", 1)], 0, 0, 1, 1)
    bg = s.lin([(0, "#fff0c8", 1), (0.45, "#e6b870", 1), (1, "#4a4a6a", 1)], 0, 1, 0, 0)
    ng = s.lin([(0, "#0a1424", 1), (0.4, "#2c4a72", 1), (0.7, body, 1), (1, "#081020", 1)], 0, 0, 1, 0)
    # the hooded neck flaring up from the body into the canopy
    s.add(f'<path d="M{f(cx - 40)} {f(cy + 70)}C{f(cx - 44)} {f(cy + 20)} {f(cx - 120)} {f(cy - 20)} {f(cx - 150)} {f(cy - 60)}'
          f'L{f(cx + 150)} {f(cy - 60)}C{f(cx + 120)} {f(cy - 20)} {f(cx + 44)} {f(cy + 20)} {f(cx + 40)} {f(cy + 70)}Z" fill="{ng}"/>')
    order = sorted(range(n), key=lambda k: -abs(k - (n - 1) / 2))
    halo = []
    for k in order:
        off = k - (n - 1) / 2
        a = off * spread
        ra = math.radians(a)
        sc = 1.08 - abs(off) * .06
        bx, by = cx + math.sin(ra) * 88, cy - math.cos(ra) * 40 + abs(off) ** 1.4 * 9
        halo.append(f'<path d="{hood}" transform="translate({f(bx)} {f(by)}) rotate({f(a)}) scale({f(sc * 1.02)})"/>')
    s.add(f'<g fill="{rim}" opacity=".9" filter="{s.blur(5)}">{"".join(halo)}</g>')
    for k in order:
        off = k - (n - 1) / 2
        a = off * spread
        ra = math.radians(a)
        sc = 1.08 - abs(off) * .06
        L = 40
        bx, by = cx + math.sin(ra) * L * 2.2, cy - math.cos(ra) * L + abs(off) ** 1.4 * 9
        t = f"translate({f(bx)} {f(by)}) rotate({f(a)}) scale({f(sc)})"
        s.add(f'<g transform="{t}"><path d="{hood}" fill="#000" opacity=".3" transform="translate(0 8)" filter="{s.blur(6)}"/><path d="{hood}" fill="{hg}"/>'
              f'<g transform="scale(1.28 1.04)"><path d="{belly_d}" fill="{bg}"/>'
              f'<path d="{scales}" stroke="#6a4020" stroke-opacity=".35" stroke-width="2" fill="none" clip-path="{s.clip(belly_d)}"/>'
              f'<path d="{spect}" fill="none" stroke="#6a4020" stroke-opacity=".45" stroke-width="3"/></g>'
              f'<path d="M-22 -218C-28 -244 -14 -266 0 -266C14 -266 28 -244 22 -218C14 -208 -14 -208 -22 -218Z" fill="{hg}"/>'
              f'<path d="M-22 -218C-28 -244 -14 -266 0 -266C14 -266 28 -244 22 -218" fill="none" stroke="{rim}" stroke-opacity=".5" stroke-width="2"/>'
              f'<path d="M-10 -248C-6 -256 6 -256 10 -248" stroke="#6a8ab8" stroke-opacity=".6" stroke-width="2" fill="none"/>'
              f'<circle cx="-10" cy="-232" r="3.6" fill="{gold}"/><circle cx="10" cy="-232" r="3.6" fill="{gold}"/>'
              f'<path d="M0 -212V-200L-4 -194M0 -200L4 -194" stroke="#d04040" stroke-width="1.6" fill="none"/>'
              f'<path d="M0 -114L9 -100L0 -86L-9 -100Z" fill="{gold}" opacity=".9"/></g>')


@scene
def vishnu(s):
    wl, moon = 650, (800, 372)
    s.sky([(0, "#070b2a"), (.25, "#14205a"), (.48, "#33468a"), (.6, "#7486c0"), (.66, "#c4cdea"), (1, "#e8ecf8")])
    s.stars(140, 0, 420, seed=21, bright=.9)
    s.glow(*moon, 640, "#b8c8ff", .5, .16)
    s.moon(*moon, 172, color="#fbf6e8", glow="#dfe6ff", glow_r=520)
    s.fx("clouds", y0=30, y1=250, seed=22, cell=140, aniso=4, cover=.32, soft=.2, lit="#dfe6ff", body=.85, direct=.75,
         light=(0, 1), sun=(moon[0], moon[1], 380), rim="#ffffff", opacity=.75)
    s.fx("clouds", y0=520, y1=648, seed=23, cell=70, aniso=6, cover=.34, soft=.2, lit="#f2f4ff", body=.92, direct=.9,
         light=(0, -1), opacity=.8, bottom_fade=.1)
    s.glow(800, 560, 380, "#ffc870", .45, .25, sy=.8)
    rise = (800, 520)
    st = coil_stamps(800, wl + 92, rise_to=rise, r_body=36)
    st = [(x, y, r * (1 + .5 * max(0, (wl + 60 - y) / 200)) if d > -1000 and d < -998 else r, d) for x, y, r, d in st]
    tube(s, [p for p in st if p[3] < -40], light="#6a90c0")
    shesha(s, 800, 500)
    s.glow(800, 600, 220, "#ffe2a0", .55, .3, sy=.6)
    gada(s, 455, 380, .72, rot=-14)
    chakra(s, 588, 175, 80)
    shankha(s, 1012, 180, .62, rot=8)
    padma(s, 1148, 372, 84)
    s.motes(50, 350, 1250, 80, 620, seed=5)
    s.fx("reflect", y0=wl, strength=.75, tint="#cdd4ec", tint_near=.42, tint_far=.22, amp=4, squash=1.0)
    s.fx("glints", y0=wl, cx=800, color="#ffffff", width=70, strength=1.0, scatter=.12, density=.55)
    s.wisps(26, 0, W, wl + 8, H, "#ffffff", a=(.15, .4), length=(120, 520), thick=(2, 6), blur=2, seed=7)
    s.glow(800, wl + 40, 300, "#ffd890", .35, .3, sy=.35)
    tube(s, [p for p in st if p[3] >= -40], light="#8ab0dc")
    s.glow(800, wl + 10, 200, "#ffe2a0", .3, .3, sy=.4)
    s.fx("godrays", cx=moon[0], cy=moon[1], strength=.25, thresh=.8, decay=.97, radius=260)
    s.fx("mottle", amp=.04, cell=60)
    return s


# =====================================================================================
# 6. Trimurti: lotus, discus and trident over the dawn ocean
# =====================================================================================
@scene
def trimurti(s):
    wl, sun = 660, (800, 652)
    s.sky([(0, "#0e1140"), (.22, "#2a2a6a"), (.42, "#6a4a8c"), (.54, "#c06a8c"), (.62, "#f39a7a"), (.68, "#ffd09a")])
    s.stars(70, 0, 260, seed=31, bright=.6)
    for x, c in ((430, "#ff9ab0"), (800, "#ffe2a0"), (1170, "#a8b8ff")):
        s.add(f'<rect x="{x - 150}" y="0" width="300" height="{wl}" fill="{s.lin([(0, c, 0), (.6, c, .16), (1, c, .3)], 0, 0, 0, wl, user=True)}" filter="{s.blur(40)}"/>')
    s.sun(*sun, 40, halo_r=700, halo_a=.8)
    s.fx("clouds", y0=40, y1=300, seed=32, cell=140, aniso=4, cover=.36, soft=.18, lit="#ffbfa8", body=.75, direct=.8,
         light=(0, 1), sun=(sun[0], sun[1], 500), opacity=.85)
    s.fx("clouds", y0=480, y1=640, seed=33, cell=80, aniso=6, cover=.3, soft=.2, lit="#ffe0b8", body=.85, direct=.95,
         light=(0, 1), sun=(sun[0], sun[1], 360), opacity=.8)
    s.rays(800, 652, n=22, length=900, width=.03, color="#ffe2a0", a=.14, spread=(190, 350), seed=4)
    for x, y, r in ((430, 420, 170), (800, 340, 190), (1170, 420, 170)):
        s.glow(x, y, r * 1.6, "#ffd890", .35, .25)
        halo_rings(s, x, y, r, a=.32, n=2, gap=.08, dots=24)
    padma(s, 430, 482, 150)
    chakra(s, 800, 340, 132)
    trishula(s, 1170, 400, .9, h=230, damaru=False)
    s.motes(50, 300, 1300, 120, 640, seed=6)
    s.fx("reflect", y0=wl, strength=.85, tint="#24183c", tint_near=.45, tint_far=.1, amp=4)
    s.fx("glints", y0=wl, cx=sun[0], color="#fff0c8", width=60, strength=1.2, scatter=.06, density=.5)
    s.wisps(14, 0, W, wl + 8, wl + 80, "#ffd0b8", a=(.06, .16), length=(240, 700), thick=(6, 16), blur=10, seed=3)
    s.birds(5, 960, 1120, 560, 610, color="#4a2a40", s=(5, 8), seed=3, a=.7)
    s.fx("godrays", cx=sun[0], cy=sun[1], strength=.4, thresh=.72, decay=.97, radius=260)
    s.fx("mottle", amp=.04, cell=60)
    return s


# =====================================================================================
# still-life pieces: palm-leaf book, veena, golden lotus seat, gold coins
# =====================================================================================
def pothi(s, x, y, L=300, depth=40, th=30, rot=0.0, sc=1.0, cover="#8a2414", trim="#e8b860", leaves="#efe0bc", seed=1):
    """A palm-leaf manuscript lying flat, seen from the front and a little above: lacquered
    wooden covers, the edges of the leaves, and a cord wound round and knotted."""
    h2, d = L / 2, depth / 2
    r = depth * .5
    t = f"translate({f(x)} {f(y)}) rotate({f(rot)}) scale({f(sc)})"
    top = f"M{f(-h2 + r)} {f(-d)}H{f(h2 - r)}A{f(r)} {f(d)} 0 0 1 {f(h2 - r)} {f(d)}H{f(-h2 + r)}A{f(r)} {f(d)} 0 0 1 {f(-h2 + r)} {f(-d)}Z"
    side = f"M{f(-h2 + r * .2)} {f(0)}V{f(th)}A{f(r)} {f(d)} 0 0 0 {f(-h2 + r)} {f(d + th)}H{f(h2 - r)}A{f(r)} {f(d)} 0 0 0 {f(h2 - r * .2)} {f(th)}V0Z"
    lines = "".join(f"M{f(-h2 + r * .6)} {f(d + k)}H{f(h2 - r * .6)}" for k in range(7, th - 4, 3))
    cw = s.lin([(0, mix(cover, "#ffffff", .25), 1), (1, mix(cover, "#000000", .4), 1)], 0, 0, 0, 1)
    lg = s.lin([(0, leaves, 1), (1, mix(leaves, "#8a6a3a", .5), 1)], 0, 0, 1, 0)
    cords = "".join(f'<path d="M{f(cx_)} {f(-d - 2)}V{f(d + th + 2)}" stroke="#6a3a14" stroke-width="3"/>' for cx_ in (-L * .2, L * .2))
    knot = (f'<circle cx="{f(L * .2)}" cy="{f(d * .2)}" r="5" fill="#7a4418"/>'
            f'<path d="M{f(L * .2)} {f(d * .2)}C{f(L * .24)} {f(d + th)} {f(L * .3)} {f(d + th + 16)} {f(L * .27)} {f(d + th + 34)}" stroke="#7a4418" stroke-width="2.4" fill="none"/>'
            f'<path d="M{f(L * .27 - 5)} {f(d + th + 32)}h10l-2 16h-6Z" fill="{trim}"/>')
    s.add(f'<g transform="{t}"><ellipse cx="0" cy="{f(d + th)}" rx="{f(h2 * 1.04)}" ry="{f(d * .9)}" fill="#000" opacity=".35" filter="{s.blur(8)}"/>'
          f'<path d="{side}" fill="{lg}"/><path d="{lines}" stroke="#8a6a3a" stroke-opacity=".45" stroke-width="1"/>'
          f'<path d="M{f(-h2 + r * .4)} {f(d + th - 5)}H{f(h2 - r * .4)}V{f(d + th)}H{f(-h2 + r * .4)}Z" fill="{mix(cover, "#000000", .3)}"/>'
          f'<path d="{top}" fill="{cw}"/><path d="{top}" fill="none" stroke="{trim}" stroke-width="2" transform="scale(.94 .8)"/>'
          f'<path d="M{f(-h2 + r * .3)} {f(d)}V{f(d + 5)}H{f(h2 - r * .3)}V{f(d)}Z" fill="{mix(cover, "#000000", .2)}"/>'
          f'<ellipse cx="0" cy="0" rx="{f(depth * .45)}" ry="{f(d * .5)}" fill="none" stroke="{trim}" stroke-width="1.6"/>'
          f'{cords}{knot}</g>')


def veena(s, x, y, sc=1.0, rot=0.0, wood="#6e2410", gold="#e8b860"):
    """A Saraswati veena lying on its side: the great round kudam, the long fretted neck,
    the second gourd beneath and the curling yali head, strung with silver."""
    t = f"translate({f(x)} {f(y)}) rotate({f(rot)}) scale({f(sc)})"
    wg = s.rad([(0, mix(wood, "#ffb080", .35), 1), (0.55, wood, 1), (1, mix(wood, "#000000", .7), 1)], .35, .3, .75)
    ng = s.lin([(0, mix(wood, "#ffb080", .3), 1), (0.5, wood, 1), (1, mix(wood, "#000000", .6), 1)], 0, 0, 0, 1)
    gourd = s.rad([(0, "#d8a060", 1), (0.6, "#8a4a1c", 1), (1, "#2a1006", 1)], .35, .3, .75)
    plate = s.rad([(0, "#f0c890", 1), (0.7, "#b8783a", 1), (1, "#7a4418", 1)], .4, .4, .7)
    frets = "".join(f"M{f(xx)} -19V-11" for xx in [-200 + 300 * (1 - .93 ** k) / (1 - .93 ** 22) for k in range(23)])
    yali = ("M-246 -18C-262 -22 -282 -30 -292 -48C-300 -64 -296 -82 -282 -88C-268 -94 -254 -86 -254 -72"
            "C-254 -62 -262 -58 -270 -60C-262 -66 -264 -76 -274 -74C-284 -70 -284 -54 -274 -44C-266 -36 -254 -32 -244 -30Z")
    out = [f'<g transform="{t}">',
           f'<ellipse cx="20" cy="104" rx="300" ry="16" fill="#000" opacity=".3" filter="{s.blur(10)}"/>',
           f'<circle cx="-170" cy="46" r="50" fill="{gourd}"/>',
           f'<path d="M-180 -4V8H-160V-4Z" fill="{gold}"/>',
           f'<path d="M-250 -20L110 -24V22L-250 16Z" fill="{ng}"/>',
           f'<path d="M-250 -20L110 -24V-14L-250 -11Z" fill="#2a0e06"/>',
           f'<path d="{frets}" stroke="{gold}" stroke-width="2.6"/>',
           f'<path d="M-250 -2H110M-250 10H110" stroke="{gold}" stroke-width="1.6" opacity=".7"/>',
           f'<circle cx="200" cy="18" r="98" fill="{wg}"/>',
           f'<ellipse cx="196" cy="-2" rx="84" ry="88" fill="{plate}" transform="rotate(8 196 -2)"/>',
           f'<ellipse cx="196" cy="-2" rx="84" ry="88" fill="none" stroke="{gold}" stroke-width="3" transform="rotate(8 196 -2)"/>',
           f'<circle cx="196" cy="-2" r="20" fill="none" stroke="{gold}" stroke-width="2" opacity=".8"/>',
           f'<path d="M110 -24C120 -40 140 -40 150 -30" stroke="{gold}" stroke-width="3" fill="none"/>',
           f'<path d="{yali}" fill="{gold}"/><circle cx="-276" cy="-64" r="3" fill="#2a0e06"/>',
           f'<path d="M206 -10H222V4H206Z" fill="#f4e4c0"/>',
           f'<path d="M214 -8L-246 -17M214 -5L-246 -15M214 -2L-246 -13M214 1L-246 -11" stroke="#f4f6ff" stroke-width=".9" opacity=".85"/>',
           "".join(f'<circle cx="{-238 + k * 14}" cy="-24" r="4" fill="{gold}"/>' for k in range(4)),
           '</g>']
    s.add("".join(out))


def lotus_seat_back(s, cx, cy, R=280, glow=True):
    """The back of a vast golden lotus: tall petals rising behind its broad flat seat."""
    if glow:
        s.glow(cx, cy - R * .3, R * 2.4, "#ffb050", .5, .2)
        s.glow(cx, cy - R * .2, R * 1.2, "#ffe2a0", .45, .3)
    order = sorted(range(11), key=lambda k: -abs(k - 5))
    for k in order:
        th = -82 + k * 16.4
        L = R * (.95 - .28 * abs(th) / 90)
        bx, by = cx + R * .52 * math.sin(math.radians(th)), cy + R * .08
        gilt(s, [(petal_d(R * .3, L, bx, by, th * .95, pinch=.04), PALE_GOLD if abs(th) < 40 else GOLD)], 0, 0, 1, glow=0, emboss=6)
    top = ellipse_d(cx, cy, R * .62, R * .15)
    band = f"M{f(cx - R * .62)} {f(cy)}V{f(cy + R * .07)}A{f(R * .62)} {f(R * .15)} 0 0 0 {f(cx + R * .62)} {f(cy + R * .07)}V{f(cy)}Z"
    holes = "".join(ellipse_d(cx + R * .45 * rr * math.cos(a), cy + R * .11 * rr * math.sin(a), R * .018, R * .007)
                    for rr in (.35, .7, .95) for a in [k * 2 * math.pi / int(6 + rr * 14) for k in range(int(6 + rr * 14))])
    gilt(s, [(band, GOLD), (top, [(0, "#fff4cc"), (0.6, "#f2cf7a"), (1, "#c88a30")])], 0, 0, 1, glow=0, emboss=4,
         details=f'<path d="{holes}" fill="#9a6a20" opacity=".5"/>')


def lotus_seat_front(s, cx, cy, R=280):
    """The front of the lotus: a ring of petals cupping the seat, and a lower row turned down."""
    low = []
    for k in range(9):
        th = -80 + k * 20
        bx, by = cx + R * .6 * math.sin(math.radians(th)), cy + R * .34
        low.append((petal_d(R * .22, R * .3, bx, by, 180 - th * .9), GOLD))
    gilt(s, low, 0, 0, 1, glow=0, emboss=5)
    order = sorted(range(9), key=lambda k: abs(k - 4))
    for k in order[::-1]:
        th = -80 + k * 20
        bx, by = cx + R * .64 * math.sin(math.radians(th)), cy + R * .4 - R * .05 * math.cos(math.radians(th))
        gilt(s, [(petal_d(R * .22, R * .27, bx, by, th * .8, pinch=.04), PALE_GOLD if abs(th) < 30 else GOLD)], 0, 0, 1, glow=0, emboss=5)


def coins(s, n, x0, x1, y0, y1, seed=1, size=(6, 13), trail=60, a=1.0):
    """Gold coins tumbling down through the air, each with a faint streak of light above it."""
    rng = random.Random(seed)
    g = s.rad([(0, "#fffbe0", 1), (0.5, "#f6cf62", 1), (1, "#a86a1c", 1)], .4, .35, .7)
    out, tr = [], []
    for _ in range(n):
        x, y, r = rng.uniform(x0, x1), rng.uniform(y0, y1), rng.uniform(*size)
        tilt = rng.uniform(.25, 1)
        ang = rng.uniform(0, 180)
        aa = rng.uniform(.6, 1) * a
        tl = trail * rng.uniform(.4, 1.2) * r / 10
        tr.append(f'<path d="M{f(x - r * .3)} {f(y - tl)}L{f(x + r * .3)} {f(y - tl)}L{f(x + r * .6)} {f(y)}L{f(x - r * .6)} {f(y)}Z" opacity="{aa * .5:.2f}"/>')
        out.append(f'<g transform="translate({f(x)} {f(y)}) rotate({ang:.0f})" opacity="{aa:.2f}"><ellipse rx="{f(r)}" ry="{f(r * tilt)}" fill="{g}"/>'
                   f'<ellipse rx="{f(r * .72)}" ry="{f(r * tilt * .72)}" fill="none" stroke="#a86a1c" stroke-opacity=".6" stroke-width="{f(max(.8, r * .1))}"/>'
                   f'<ellipse cx="{f(-r * .3)}" cy="{f(-r * tilt * .3)}" rx="{f(r * .25)}" ry="{f(r * tilt * .15)}" fill="#fff" opacity=".8"/></g>')
    fill = s.lin([(0, "#ffd890", 0), (1, "#ffe8b0", 1)], 0, 0, 0, 1)
    s.add(f'<g fill="{fill}" filter="{s.blur(2)}" style="mix-blend-mode:screen">{"".join(tr)}</g>{"".join(out)}')


def silhouette(s, d, x, y, sc=1.0, flip=False, color="#140c24", rim="#ffcf80", light=(800, 400), rim_r=700, rim_w=5, rim_a=1.0, extra=""):
    """A dark shape with an inner rim of light on the edges facing the light."""
    import re
    sx = -sc if flip else sc
    t = f"translate({f(x)} {f(y)}) scale({f(sx)} {f(sc)})"
    rg = s.rad([(0, rim, rim_a), (0.5, rim, rim_a * .4), (1, rim, 0)], light[0], light[1], rim_r, user=True)
    subs = re.findall(r"M[^M]*", d)
    cid = s.uid("c")
    s.defs.append(f'<clipPath id="{cid}">{"".join(f"<path d='{q}' transform='{t}'/>" for q in subs)}</clipPath>')
    s.add(f'<g transform="{t}" fill="{color}">{"".join(f"<path d='{q}'/>" for q in subs)}{extra}</g>'
          f'<g clip-path="url(#{cid})"><path d="{d}" transform="{t}" fill="none" stroke="{rg}" stroke-width="{f(rim_w * 2 / sc)}" filter="{s.blur(rim_w * .5)}"/></g>')


def kalasha_d():
    """A small round water pot with a flared mouth; origin at the mouth."""
    return ("M-10 0H10C10 6 6 8 8 12C22 16 30 28 30 42C30 60 16 70 0 70C-16 70 -30 60 -30 42"
            "C-30 28 -22 16 -8 12C-6 8 -10 6 -10 0Z") + ellipse_d(0, 0, 13, 4)


# =====================================================================================
# 1. Lakshmi
# =====================================================================================
@scene
def lakshmi(s):
    wl, aura = 668, (800, 470)
    s.sky([(0, "#0a0724"), (.3, "#1c1248"), (.5, "#3e2266"), (.6, "#6a3070"), (.67, "#9a4a72")])
    s.stars(120, 0, 380, seed=41, bright=.8)
    s.glow(*aura, 760, "#ff9a40", .5, .18)
    s.glow(*aura, 320, "#ffd890", .45, .3)
    s.fx("clouds", y0=20, y1=280, seed=42, cell=130, aniso=4, cover=.32, soft=.2, lit="#ffb878", body=.8, direct=.7,
         light=(0, 1), sun=(aura[0], aura[1], 420), opacity=.8)
    s.rays(aura[0], aura[1], n=34, length=950, width=.025, color="#ffd890", a=.16, spread=(195, 345), seed=5)
    # golden rain of light
    rng = random.Random(4)
    streaks = "".join(f'<rect x="{f(x)}" y="0" width="{f(rng.uniform(1, 3))}" height="{f(rng.uniform(300, 620))}" opacity="{rng.uniform(.15, .5):.2f}"/>'
                      for x in [rng.gauss(800, 260) for _ in range(46)])
    s.add(f'<g fill="{s.lin([(0, "#ffd890", 0), (0.6, "#ffd890", .8), (1, "#ffd890", 0)], 0, 0, 0, 1)}" filter="{s.blur(1.4)}" style="mix-blend-mode:screen">{streaks}</g>')
    far = ridgeline(wl, 40, 45, cell=260, octaves=5, ridged=.3)
    hills(s, far, "#3a1e4e", "#2a1640", haze="#8a4a6a", haze_a=.5, haze_h=40)
    rr = random.Random(6)
    cr = "".join(crown(x, wl - rr.uniform(6, 18), rr.uniform(12, 24), seed=int(x)) for x in list(range(-20, 520, 15)) + list(range(1090, 1640, 15)))
    s.add(f'<path d="{cr}" fill="#26143a"/>')
    s.mist(wl - 6, 40, "#c07a8a", .45, 10)
    # the two elephants, standing in the water and raising pots to the lotus
    el = elephant_d()
    for x, flip in ((300, False), (1300, True)):
        silhouette(s, el[1], x, wl + 34, 1.28, flip, color="#0e0818", rim="#ffcf80", light=aura, rim_r=600, rim_w=3, rim_a=.6)
        silhouette(s, el[0] + el[4], x, wl + 34, 1.28, flip, color="#170e28", rim="#ffd890", light=aura, rim_r=760, rim_w=5)
        sx = -1 if flip else 1
        t = f"translate({f(x)} {f(wl + 34)}) scale({f(sx * 1.28)} 1.28)"
        s.add(f'<g transform="{t}"><path d="{el[2]}" fill="#1e1430"/><path d="{el[2]}" fill="none" stroke="#ffcf80" stroke-opacity=".35" stroke-width="2"/>'
              f'<path d="{el[3]}" fill="#f4e6cc"/></g>')
        # pot held at the trunk's tip, tipped towards the lotus
        px, py = x + sx * 176 * 1.28, wl + 34 - 336 * 1.28
        gilt(s, [kalasha_d()], px, py + 6, 1.0, rot=sx * 38, glow=.6, emboss=4)
        mx, my = px + sx * 26, py - 6
        arc = [(mx + (800 - sx * 60 - mx) * t, my - 120 * math.sin(math.pi * t) * (1 - t * .3) + (aura[1] - 40 - my) * t * t) for t in [k / 30 for k in range(31)]]
        s.add(f'<path d="{ribbon(arc, 4, 22)}" fill="#ffe8b0" opacity=".25" filter="{s.blur(8)}" style="mix-blend-mode:screen"/>')
        s.add(f'<path d="{ribbon(arc, 2.5, 7)}" fill="#fff6dc" opacity=".55" filter="{s.blur(1.6)}"/>')
        s.motes(26, min(mx, 800), max(mx, 800), my - 120, aura[1], color="#ffe8b0", seed=int(x), size=(.6, 1.6))
    s.glow(800, wl - 120, 360, "#ffc070", .5, .25)
    ob.lotus(s, 800, wl - 4, 2.15, seed=7, glow="#ffd8c0")
    s.fx("reflect", y0=wl, strength=.85, tint="#140a22", tint_near=.5, tint_far=.1, amp=4)
    s.fx("glints", y0=wl, cx=800, color="#ffd890", width=80, strength=1.2, scatter=.12, density=.55)
    s.wisps(16, 0, W, wl + 8, wl + 90, "#ffb8a0", a=(.06, .16), length=(240, 700), thick=(6, 16), blur=10, seed=4)
    leaf = dict(dark="#0c1a1a", light="#24443a", rim="#ffcf90", rim_a=.7)
    ob.pad(s, 520, 712, 64, seed=2, **leaf)
    ob.pad(s, 1090, 718, 72, seed=3, **leaf)
    ob.pad(s, 250, 880, 210, seed=4, **leaf)
    ob.pad(s, 1370, 900, 230, seed=5, **leaf)
    ob.pad(s, 820, 975, 170, seed=6, **leaf)
    ob.bud(s, 1120, 712, .7, stem_to=730)
    ob.bud(s, 560, 704, .6, stem_to=716)
    ob.lotus(s, 1340, 870, .6, seed=8)
    ob.lotus(s, 280, 858, .55, seed=9)
    coins(s, 70, 380, 1220, 30, 640, seed=3)
    coins(s, 12, 600, 1000, 690, 760, seed=4, trail=0, size=(5, 8), a=.8)
    s.motes(60, 300, 1300, 60, 700, seed=9)
    s.fx("godrays", cx=aura[0], cy=aura[1], strength=.35, thresh=.72, decay=.97, radius=260)
    s.fx("mottle", amp=.04, cell=60)
    s.look = {"vibrance": .12}
    return s


# =====================================================================================
# 5. Brahma
# =====================================================================================
@scene
def brahma(s):
    wl = 650
    s.sky([(0, "#080a2a"), (.25, "#1c1e56"), (.45, "#4a3a7c"), (.56, "#9a5a86"), (.63, "#f0907a"), (.66, "#ffc890")])
    s.fx("nebula", seed=51, cell=300, colors=("#2a2a7a", "#6a3a9a", "#c0608a"), strength=.35, cx=800, cy=120, r=900, cover=.5, y0=0, y1=500)
    s.stars(150, 0, 420, seed=52, bright=.85)
    s.sun(800, 652, 34, halo_r=760, halo_a=.85)
    s.fx("clouds", y0=360, y1=630, seed=53, cell=90, aniso=6, cover=.3, soft=.2, lit="#ffd6a8", body=.85, direct=.9,
         light=(0, 1), sun=(800, 652, 420), opacity=.85)
    s.rays(800, 600, n=30, length=1000, width=.03, color="#ffe2a0", a=.16, spread=(190, 350), seed=7)
    s.fx("reflect", y0=wl, strength=.85, tint="#1a1236", tint_near=.5, tint_far=.1, amp=4)
    s.fx("glints", y0=wl, cx=800, color="#fff0c8", width=60, strength=1.1, scatter=.08, density=.5)
    s.wisps(14, 0, W, wl + 6, wl + 70, "#ffd0b8", a=(.06, .16), length=(240, 700), thick=(6, 16), blur=10, seed=5)
    m = s.mark()
    cy, R = 452, 290
    lotus_seat_back(s, 800, cy, R)
    # the four Vedas and the water pot, resting on the seat
    for k, (dx, dy, rr) in enumerate(((-86, -2, -2), (-80, -20, 2), (-90, -38, -1), (-82, -56, 3))):
        pothi(s, 800 + dx, cy + dy, L=170, depth=28, th=15, rot=rr, cover=("#8a2414", "#6a1c40", "#7a3a14", "#24305a")[k], seed=k)
    gilt(s, kamandalu_d(), 930, cy - 44, .72, glow=.5, emboss=4)
    lotus_seat_front(s, 800, cy, R)
    ob.reflect_since(s, m, wl + 2, .35, 3, 300)
    # the swan gliding towards the lotus
    sw = swan_d()
    sg = s.lin([(0, "#ffffff", 1), (0.6, "#f2ece6", 1), (1, "#b8aec8", 1)], 0, 0, 0, 1)
    m = s.mark()
    s.add(f'<g transform="translate(1250 752) scale(.9)"><path d="{sw[0]}" fill="{sg}"/><path d="{sw[1]}" fill="{sg}" stroke="#c8b8d0" stroke-width="1.4"/>'
          f'<path d="{sw[0]}" fill="none" stroke="#ffd8a0" stroke-opacity=".8" stroke-width="2.4"/>'
          f'<path d="{sw[2]}" fill="#f08a2a"/><path d="{sw[3]}" fill="#2a1a14"/><path d="{sw[4]}" fill="#1a0e0a"/></g>')
    ob.reflect_since(s, m, 754, .4, 2, 120)
    s.add(f'<path d="M1090 758Q1170 770 1230 758" stroke="#ffe0c0" stroke-opacity=".3" stroke-width="2" fill="none"/>')
    leaf = dict(dark="#10221f", light="#2c4a40", rim="#ffc79a", rim_a=.7)
    ob.pad(s, 330, 760, 120, seed=11, **leaf)
    ob.pad(s, 1460, 900, 200, seed=12, **leaf)
    ob.pad(s, 200, 950, 220, seed=13, **leaf)
    ob.bud(s, 360, 750, .8, stem_to=772)
    s.motes(50, 300, 1300, 100, 640, seed=9)
    s.fx("godrays", cx=800, cy=600, strength=.35, thresh=.75, decay=.97, radius=300)
    s.fx("mottle", amp=.04, cell=60)
    return s


# =====================================================================================
# 2. Saraswati
# =====================================================================================
def marble_steps(s, x0, x1, ys, color="#f2eee8", shade="#8a82a4", edge="#fff8ea"):
    """White marble steps descending towards the viewer: each a lit tread and a shadowed riser."""
    out = []
    for k, (yt, yr) in enumerate(ys):
        x_end = x1 - (len(ys) - 1 - k) * 0
        tread = s.lin([(0, mix(color, shade, .25), 1), (1, color, 1)], 0, yt, 0, yr, user=True)
        riser = s.lin([(0, mix(color, shade, .6), 1), (1, mix(shade, "#5a5070", .3), 1)], 0, yr, 0, yr + 40, user=True)
        out.append(f'<path d="M{f(x0)} {f(yt)}H{f(x_end)}L{f(x_end + 20)} {f(yr)}H{f(x0)}Z" fill="{tread}"/>')
        nxt = ys[k + 1][0] if k + 1 < len(ys) else 1010
        out.append(f'<path d="M{f(x0)} {f(yr)}H{f(x_end + 20)}V{f(nxt)}H{f(x0)}Z" fill="{riser}"/>')
        out.append(f'<path d="M{f(x0)} {f(yr)}H{f(x_end + 20)}" stroke="{edge}" stroke-width="2" opacity=".9"/>')
    s.add("".join(out))
    rng = random.Random(3)
    veins = "".join(f"M{f(rng.uniform(x0, x1))} {f(rng.uniform(ys[0][0], 1000))}q{f(rng.uniform(20, 60))} {f(rng.uniform(-10, 10))} {f(rng.uniform(60, 140))} {f(rng.uniform(-6, 18))}" for _ in range(26))
    s.add(f'<path d="{veins}" stroke="#a8a0b8" stroke-opacity=".25" stroke-width="1.2" fill="none" filter="{s.blur(.6)}"/>')


@scene
def saraswati(s):
    wl, sun = 590, (1090, 452)
    s.sky([(0, "#3e4886"), (.22, "#7a80b4"), (.42, "#c4b8d4"), (.53, "#f4d8c8"), (.59, "#ffe8cc")])
    s.sun(*sun, 30, core="#fffcf4", rim="#fff0d0", halo="#ffe0c0", halo_r=600, halo_a=.6)
    s.fx("clouds", y0=40, y1=330, seed=61, cell=150, aniso=3.5, cover=.38, soft=.2, lit="#fff6ec", body=.9, direct=.7,
         light=(.4, 1), sun=(sun[0], sun[1], 400), rim="#fffaf0", opacity=.85)
    far = ridgeline(wl - 2, 70, 61, cell=320, octaves=5, ridged=.3, envelope=[(0, 1), (700, .5), (1600, .8)])
    hills(s, far, "#b0aecc", "#c8c0d4", haze="#f0e4e0", haze_a=.6, haze_h=60)
    arch.nagara(s, 360, wl - 30, .34, color="#c4bed4", rim="#fff4e4", light=1, door="#ffe8c0", bands=False, glow=False, flag_color="#f0d8a0")
    near = ridgeline(wl, 26, 62, cell=180, octaves=5, ridged=.2, envelope=[(0, 1), (600, .4), (900, .1), (1600, .6)])
    hills(s, near, "#a6a0c0", "#b0aac6")
    s.mist(wl - 6, 70, "#fff8f0", .7, 14)
    s.fx("reflect", y0=wl, strength=.8, tint="#4e5288", tint_near=.45, tint_far=.1, amp=3)
    s.fx("glints", y0=wl, cx=sun[0], color="#fffaf0", width=60, strength=1.0, scatter=.08, density=.5)
    s.mist(wl + 20, 60, "#ffffff", .45, 20)
    s.wisps(16, 0, W, wl + 10, wl + 140, "#ffffff", a=(.1, .26), length=(260, 700), thick=(8, 22), blur=12, seed=6)
    # white lotuses on the water
    leaf = dict(dark="#2c4a48", light="#6a8a80", rim="#fff4e0", rim_a=.8)
    white = dict(tip="#f4f0f8", base="#ffffff", edge="#b8b0cc", glow="#ffffff")
    ob.pad(s, 1290, 712, 80, seed=21, **leaf)
    ob.pad(s, 960, 660, 50, seed=22, **leaf)
    ob.pad(s, 1460, 820, 130, seed=23, **leaf)
    m = s.mark()
    ob.lotus(s, 1300, 704, .45, seed=24, **white)
    ob.lotus(s, 1470, 806, .62, seed=25, **white)
    ob.reflect_since(s, m, 712, .3, 2, 80)
    ob.bud(s, 980, 656, .5, stem_to=668, tip="#e8e4f0", base="#ffffff")
    # the swan
    sw = swan_d()
    sg = s.lin([(0, "#fbf8f4", 1), (0.5, "#e8e2e6", 1), (1, "#9a92b4", 1)], 0, 0, 0, 1)
    m = s.mark()
    s.add(f'<g transform="translate(1100 762) scale(1.3)"><path d="{sw[0]}" fill="{sg}"/><path d="{sw[1]}" fill="{sg}" stroke="#bcb2cc" stroke-width="1.4"/>'
          f'<path d="{sw[1]}" fill="none" stroke="#ffe0a8" stroke-opacity=".8" stroke-width="2"/>'
          f'<path d="M-60 -40C-20 -60 40 -64 100 -56" stroke="#c8c0d6" stroke-width="1.2" fill="none" opacity=".7"/>'
          f'<path d="{sw[2]}" fill="#f08a2a"/><path d="{sw[3]}" fill="#2a1a14"/><path d="{sw[4]}" fill="#1a0e0a"/></g>')
    ob.reflect_since(s, m, 765, .45, 2, 160)
    s.add(f'<path d="M880 772Q990 786 1080 772M860 786Q980 806 1080 788" stroke="#ffffff" stroke-opacity=".45" stroke-width="2" fill="none"/>')
    # marble steps with the veena and the book
    marble_steps(s, -40, 860, [(690, 712), (770, 796), (868, 900)])
    s.add(f'<path d="M860 690L880 712V1010H860Z" fill="#6a6488" opacity=".6"/>')
    veena(s, 500, 776, 1.12, rot=-5)
    cloth = "M30 916C70 904 250 902 320 908L350 936C280 942 100 944 10 938Z"
    s.add(f'<path d="{cloth}" fill="#fffaf0"/><path d="M18 936C100 942 280 940 348 934" stroke="#e0b860" stroke-width="3" fill="none"/>')
    pothi(s, 175, 902, L=250, depth=34, th=24, rot=-2, cover="#a8303a", seed=3)
    rng = random.Random(8)
    jas = "".join(f'<g transform="translate({f(rng.uniform(80, 760))} {f(rng.choice([700, 780, 878]) + rng.uniform(0, 8))})">' +
                  "".join(f'<ellipse cx="{f(math.cos(a) * 3.2)}" cy="{f(math.sin(a) * 1.6)}" rx="3" ry="1.6" fill="#ffffff" transform="rotate({math.degrees(a):.0f} {f(math.cos(a) * 3.2)} {f(math.sin(a) * 1.6)})"/>' for a in [k * 1.257 for k in range(5)]) +
                  '<circle r="1.2" fill="#f4d890"/></g>' for _ in range(22))
    s.add(jas)
    s.motes(40, 300, 1400, 200, 700, color="#fff4dc", seed=6, size=(.8, 2))
    s.birds(4, 760, 900, 300, 360, color="#8a809e", s=(6, 9), seed=3, a=.7)
    s.fx("godrays", cx=sun[0], cy=sun[1], strength=.3, thresh=.82, decay=.97, radius=240)
    s.fx("mottle", amp=.03, cell=60)
    s.look = {"contrast": 1.08, "vignette": .32, "bloom": .6}
    return s


# =====================================================================================
# weapons and gifts, flowers and other shapes
# =====================================================================================
def khadga_d():
    """A broad curved sword, hilt at the origin and the blade along +x (about 560 long)."""
    blade = "M0 -9C80 -14 180 -20 280 -22C350 -24 412 -30 452 -48C444 -14 422 10 382 28C330 46 260 40 180 26C110 16 50 12 0 10Z"
    guard = "M-4 -30C2 -16 2 16 -4 30H8C12 16 12 -16 8 -30ZM-4 -30C-14 -34 -20 -28 -18 -20L-10 -24ZM-4 30C-14 34 -20 28 -18 20L-10 24Z"
    grip = "M-4 -7H-84V7H-4Z"
    pommel = ellipse_d(-94, 0, 13, 15) + "M-106 -4L-124 0L-106 4Z"
    fuller = "M24 -1C120 -5 260 -10 390 -20"
    return blade, guard + grip + pommel, fuller


def bow_d():
    """A recurved bow with an arrow nocked, arrow pointing up (-y); about 300 wide."""
    left = smooth_line([(0, -58), (-50, -50), (-100, -28), (-136, 0), (-152, 4)], 4)
    right = [(-x, y) for x, y in left]
    limbs = ribbon(left, 16, 4) + ribbon(right, 16, 4)
    grip = "M-12 -66H12V-46H-12Z"
    string = "M-150 4L0 30L150 4"
    arrow = "M-2.5 30H2.5V-150H-2.5Z"
    head = "M0 -186L12 -150H-12Z"
    fletch = "M0 24L-12 40V18L0 6ZM0 24L12 40V18L0 6Z"
    return limbs + grip, string, arrow + head + fletch


def bell_d():
    """A temple bell (ghanta) with its handle towards +y, mouth towards -y."""
    body = "M-48 -128C-46 -108 -38 -62 -28 -42C-22 -32 -12 -28 0 -28C12 -28 22 -32 28 -42C38 -62 46 -108 48 -128Z"
    lip = ellipse_d(0, -128, 50, 9)
    handle = "M-6 -30H6V40H-6Z" + ellipse_d(0, -6, 12, 6) + ellipse_d(0, 44, 10, 10) + "M0 54L-10 74L0 90L10 74Z"
    return body, lip, handle


def hibiscus(s, cx, cy, R=100, rot=-12, tilt=.78, seed=1, glow=True):
    """A red hibiscus seen a little from above: five ruffled petals, dark crimson heart,
    and the long staminal column with gold pollen and red stigma pads."""
    rng = random.Random(seed)
    t = f"translate({f(cx)} {f(cy)}) rotate({f(rot)}) scale(1 {f(tilt)})"
    pg = s.rad([(0, "#3a0010", 1), (0.16, "#7a0618", 1), (0.42, "#d0142a", 1), (0.8, "#ff3436", 1), (1, "#ff6a56", 1)], 0, 0, R * 1.08, user=True)
    if glow:
        s.glow(cx, cy, R * 3.2, "#ff2a3a", .35, .2)
    out = [f'<g transform="{t}">']
    for k in range(5):
        a = k * 72 + rng.uniform(-6, 6)
        pts = [(-R * .12, 0), (-R * .3, -R * .3), (-R * .56, -R * .66)]
        n = 14
        for i in range(n + 1):
            u = i / n
            pts.append((-R * .64 + R * 1.28 * u, -R * .84 - R * .2 * math.sin(math.pi * u) + R * .03 * math.sin(u * 4 * math.pi + k * 1.7)))
        pts += [(R * .56, -R * .66), (R * .3, -R * .3), (R * .12, 0)]
        sm = smooth_line(pts, 3)
        d = P(rot_pts(sm, a))
        veins = "".join(f'M{f(0)} {f(0)}Q{f(math.sin(math.radians(a + v * 9)) * R * .5)} {f(-math.cos(math.radians(a + v * 9)) * R * .5)} {f(math.sin(math.radians(a + v * 13)) * R * .92)} {f(-math.cos(math.radians(a + v * 13)) * R * .92)}' for v in (-2, -1, 0, 1, 2))
        out.append(f'<path d="{d}" fill="#000" opacity=".35" filter="{s.blur(R * .04)}" transform="translate({f(R * .02)} {f(R * .03)})"/>'
                   f'<path d="{d}" fill="{pg}"/><path d="{d}" fill="{s.lin([(0, "#ffffff", .22), (0.5, "#ffffff", 0), (1, "#000000", .25)], 0, 0, 1, 0)}"/>'
                   f'<path d="{veins}" stroke="#5a0010" stroke-opacity=".3" stroke-width="{f(R * .01)}" fill="none" clip-path="{s.clip(d)}"/>'
                   f'<path d="{d}" fill="none" stroke="#ff9a8a" stroke-opacity=".35" stroke-width="{f(R * .012)}"/>')
    out.append(f'<circle r="{f(R * .14)}" fill="#2a0008"/></g>')
    s.add("".join(out))
    # the staminal column rising out of the flower
    col = smooth_line([(cx, cy), (cx + R * .3, cy - R * .5), (cx + R * .52, cy - R * 1.0), (cx + R * .62, cy - R * 1.32)], 4)
    s.add(f'<path d="{ribbon(col, R * .07, R * .04)}" fill="{s.lin([(0, "#a8102a", 1), (1, "#ff5a6a", 1)], 0, 0, 1, 0)}"/>'
          f'<path d="{ribbon([(x - R * .015, y) for x, y in col], R * .02, R * .01)}" fill="#ffb0b0" opacity=".6"/>')
    tip = col[-1]
    dots = []
    for i in range(30):
        u = rng.uniform(.55, .95)
        x, y = col[int(u * (len(col) - 1))]
        dots.append(f'<circle cx="{f(x + rng.uniform(-R * .08, R * .08))}" cy="{f(y + rng.uniform(-R * .05, R * .05))}" r="{f(R * rng.uniform(.012, .022))}" fill="{rng.choice(["#ffd040", "#ffe880", "#f0a020"])}"/>')
    for k in range(5):
        a = math.radians(-90 + (k - 2) * 28)
        dots.append(f'<circle cx="{f(tip[0] + math.cos(a) * R * .07)}" cy="{f(tip[1] + math.sin(a) * R * .07)}" r="{f(R * .028)}" fill="#c8102a"/>')
    s.add("".join(dots))


def hib_leaf(s, x, y, L=160, rot=0, dark="#0c2016", light="#2e5a3a", rim="#c8d4ff"):
    pts = []
    for i in range(25):
        u = i / 24
        w = L * .32 * math.sin(math.pi * u) ** .8 * (1 + .06 * (i % 2))
        pts.append((w, -L * u))
    side = pts + [(-px, py) for px, py in pts[::-1]]
    d = P(rot_pts(side, rot, x, y))
    g = s.lin([(0, light, 1), (1, dark, 1)], 0, 0, 1, 1)
    vein = rot_pts([(0, 0), (0, -L * .95)], rot, x, y)
    s.add(f'<path d="{d}" fill="{g}"/><path d="M{f(vein[0][0])} {f(vein[0][1])}L{f(vein[1][0])} {f(vein[1][1])}" stroke="{rim}" stroke-opacity=".25" stroke-width="1.5"/>'
          f'<path d="{d}" fill="none" stroke="{rim}" stroke-opacity=".3" stroke-width="1.2"/>')


def galaxy(s, x, y, r, rot=0.0, tilt=.45, color="#c8b8ff", core="#fff4e0", a=1.0, seed=1):
    """A small spiral galaxy: a bright core and two dusty arms."""
    rng = random.Random(seed)
    arms = []
    for arm in range(2):
        pts = []
        th = 0.0
        while True:
            rr = r * .12 * math.exp(.32 * th)
            if rr > r:
                break
            ang = th + arm * math.pi
            pts.append((math.cos(ang) * rr, math.sin(ang) * rr))
            th += .1
        arms.append("M" + "L".join(f"{f(px)} {f(py)}" for px, py in pts))
    dots = "".join(f'<circle cx="{f(rng.gauss(0, r * .45))}" cy="{f(rng.gauss(0, r * .45))}" r="{f(rng.uniform(.4, 1.1))}" fill="#fff" opacity="{rng.uniform(.3, .9):.2f}"/>' for _ in range(int(r)))
    s.add(f'<g transform="translate({f(x)} {f(y)}) rotate({f(rot)}) scale(1 {f(tilt)})" opacity="{a}" style="mix-blend-mode:screen">'
          f'<circle r="{f(r * 1.1)}" fill="{s.rad([(0, color, .45), (1, color, 0)])}"/>'
          f'<g filter="{s.blur(r * .08)}"><path d="{"".join(arms)}" stroke="{color}" stroke-width="{f(r * .22)}" fill="none" opacity=".45"/>'
          f'<path d="{"".join(arms)}" stroke="#ffffff" stroke-width="{f(r * .05)}" fill="none" opacity=".6"/></g>'
          f'{dots}<circle r="{f(r * .3)}" fill="{s.rad([(0, "#ffffff", 1), (.4, core, .8), (1, core, 0)])}"/></g>')


# =====================================================================================
# 7. Durga
# =====================================================================================
@scene
def durga(s):
    sun = (800, 372)
    s.sky([(0, "#1a0a28"), (.2, "#4a1230"), (.42, "#a02a2a"), (.56, "#e8602a"), (.66, "#ffa040"), (1, "#ffd890")])
    s.sun(*sun, 46, core="#fffaf0", rim="#ffe0a0", halo="#ff8a30", halo_r=760, halo_a=.85)
    s.fx("clouds", y0=40, y1=300, seed=71, cell=140, aniso=4, cover=.36, soft=.18, lit="#ffb070", body=.7, direct=.8,
         light=(0, 1), sun=(sun[0], sun[1], 460), rim="#fff0c0", opacity=.85)
    s.rays(*sun, n=48, length=1000, width=.02, color="#ffe0a0", a=.2, seed=8)
    halo_rings(s, *sun, 140, color="#ffe8b0", a=.5, n=2, gap=.06, width=2.2, dots=36)
    halo_rings(s, *sun, 350, color="#ffe8b0", a=.3, n=1, width=1.6)
    # the eight gifts of the gods, held out like the rays of the sun
    R = 238
    items = ["trishula", "chakra", "shankha", "khadga", "bow", "padma", "ghanta", "gada"]
    angles = [-122, -87, -52, -17, 17, 52, 87, 122]
    for name, a in zip(items, angles):
        ra = math.radians(a)
        x, y = sun[0] + math.sin(ra) * R, sun[1] - math.cos(ra) * R
        if name == "trishula":
            ox, oy = math.sin(ra) * 30, -math.cos(ra) * 30
            tp, shaft = trishula_d(120)
            gilt(s, [shaft] + tp, x + ox, y + oy, .6, rot=a, glow=.7)
        elif name == "chakra":
            chakra(s, x, y, 56, glow=.8)
        elif name == "shankha":
            shankha(s, x, y, .5, rot=a, glow=.8)
        elif name == "khadga":
            bl, hilt, fuller = khadga_d()
            gilt(s, [(bl, [(0, "#ffffff"), (0.4, "#f4e8d0"), (0.8, "#d8b070"), (1, "#a8702a")]), hilt], x - math.sin(ra) * 60, y + math.cos(ra) * 60, .34, rot=a - 90,
                 glow=.8, details=f'<path d="{fuller}" stroke="#8a6020" stroke-opacity=".4" stroke-width="3" fill="none"/>', under="")
        elif name == "bow":
            limbs, string, arrow = bow_d()
            x, y = x - math.sin(ra) * 10, y + math.cos(ra) * 10
            s.add(f'<path d="{string}" transform="translate({f(x)} {f(y)}) rotate({f(a)}) scale(.5)" stroke="#fff0c8" stroke-width="2.4" fill="none"/>')
            gilt(s, [limbs, arrow], x, y, .5, rot=a, glow=.8)
        elif name == "padma":
            padma(s, x, y + 10, 58, glow=.8)
        elif name == "ghanta":
            body, lip, handle = bell_d()
            gilt(s, [handle, body, lip], x + math.sin(ra) * 20, y - math.cos(ra) * 20, .5, rot=a, glow=.8)
        elif name == "gada":
            gada(s, x + math.sin(ra) * 20, y - math.cos(ra) * 20, .46, rot=a, h=200, glow=.8)
    s.motes(60, 300, 1300, 60, 700, seed=7)
    # crags and the lion
    far = ridgeline(780, 120, 72, cell=320, octaves=5, ridged=.5, envelope=[(0, 1), (600, .5), (1000, .5), (1600, 1)])
    hills(s, far, "#8a2a3a", "#5a1a30", haze="#ff9a60", haze_a=.55, haze_h=140)
    s.mist(770, 100, "#ffa070", .45, 26)
    crag = smooth_line([(380, 1010), (470, 900), (560, 830), (640, 790), (720, 772), (860, 768), (930, 786), (1000, 830), (1090, 900), (1200, 1010)], 5)
    rk = random.Random(3)
    crag = [(x + rk.uniform(-4, 4), y + rk.uniform(-3, 3)) for x, y in crag]
    s.add(f'<path d="{P(crag)}" fill="{s.lin([(0, "#2a0e18", 1), (1, "#0a0408", 1)], 0, 770, 0, 1000, user=True)}"/>')
    s.add(f'<path d="{"M" + "L".join(f"{f(x)} {f(y)}" for x, y in crag[3:-3])}" stroke="#ffc070" stroke-opacity=".7" stroke-width="2.6" fill="none" filter="{s.blur(1.2)}"/>')
    near = ridgeline(930, 60, 73, cell=200, octaves=5, ridged=.4, envelope=[(0, 1.4), (500, .4), (1100, .4), (1600, 1.4)])
    s.add(f'<path d="{P(near + [(1640, 1010), (-40, 1010)])}" fill="#0c0508"/>')
    body, tail, mane = lion_d()
    silhouette(s, tail, 770, 776, .78, color="#0e0408", rim="#ffd080", light=sun, rim_r=700, rim_w=3, rim_a=.6)
    silhouette(s, body, 770, 776, .78, color="#14070c", rim="#ffd080", light=sun, rim_r=700, rim_w=4)
    silhouette(s, mane, 770, 776, .78, color="#1a090e", rim="#ffe0a0", light=sun, rim_r=700, rim_w=5)
    grass(s, 380, 1200, lambda x: y_at(crag, x) + 3, 90, h=(6, 18), color="#0a0408", seed=4)
    s.birds(5, 1050, 1250, 560, 620, color="#3a1018", s=(5, 9), seed=7, a=.8)
    s.fx("godrays", cx=sun[0], cy=sun[1], strength=.45, thresh=.72, decay=.97, radius=280)
    s.fx("mottle", amp=.04, cell=60)
    s.look = {"vibrance": .1}
    return s


# =====================================================================================
# 8. Kali
# =====================================================================================
@scene
def kali(s):
    moon = (360, 170)
    s.sky([(0, "#04051a"), (.4, "#0c0f36"), (.62, "#1c1f52"), (.7, "#2c2a5e"), (1, "#14143a")])
    s.stars(200, 0, 560, seed=81, bright=.9)
    crescent(s, *moon, 50, off=(.42, -.62), glow_r=480, glow_a=.5)
    s.fx("clouds", y0=60, y1=300, seed=82, cell=120, aniso=4.5, cover=.26, soft=.2, lit="#b8c4f0", body=.85, direct=.7,
         light=(-.6, -.4), sun=(moon[0], moon[1], 300), opacity=.55)
    wl = 600
    far = ridgeline(wl, 30, 83, cell=260, octaves=5, ridged=.3)
    hills(s, far, "#161a40", "#10122e")
    # a river temple with nine spires, far across the water
    for x, sc in ((1060, .5), (1010, .3), (1110, .3), (970, .24), (1150, .24)):
        arch.shikhara_front(s, x, wl - 26, sc, color="#0e1028", rim="#8a96d0", light=-1, door="#ffb45c" if sc == .5 else None)
    s.add(f'<rect x="930" y="{wl - 28}" width="260" height="28" fill="#0e1028"/>')
    for x in range(948, 1180, 26):
        s.flame(x, wl - 30, 7, glow_r=40, glow_a=.4)
    s.mist(wl - 4, 30, "#4a5090", .4, 8)
    s.fx("reflect", y0=wl, strength=.8, tint="#06071a", tint_near=.5, tint_far=.1, amp=3, y_end=760)
    s.fx("glints", y0=wl, cx=moon[0], color="#cfd8ff", width=40, strength=.8, scatter=.05, density=.45, y_end=760)
    # the stone altar in the foreground
    s.add(f'<path d="M-20 740L80 708H1520L1620 740V1010H-20Z" fill="{s.lin([(0, "#2a2a48", 1), (0.12, "#1a1a32", 1), (1, "#06060e", 1)], 0, 708, 0, 1000, user=True)}"/>')
    s.add(f'<path d="M-20 740L80 708H1520L1620 740" stroke="#9aa6e0" stroke-opacity=".45" stroke-width="2" fill="none"/>')
    s.add(f'<rect y="740" width="1600" height="270" fill="#000" opacity=".25" filter="{s.grain(.5, 3, .2, 4, "#ffffff")}"/>')
    s.glow(780, 700, 520, "#ff3040", .28, .2, sy=.6)
    # the sword resting across the stone
    bl, hilt, fuller = khadga_d()
    steel = [(0, "#ffffff"), (0.3, "#d8def8"), (0.65, "#7a84b0"), (1, "#2a2e4a")]
    s.add(f'<ellipse cx="1080" cy="830" rx="360" ry="24" fill="#000" opacity=".45" filter="{s.blur(12)}" transform="rotate(-10 1080 830)"/>')
    gilt(s, [(bl, steel)], 820, 838, 1.15, rot=-14, glow=.3, glow_col="#a8b8ff", halo_col="#dfe6ff", az=235, el=40,
         details=f'<path d="{fuller}" stroke="#3a4060" stroke-opacity=".5" stroke-width="3" fill="none"/>'
                 f'<path d="M30 -7C140 -12 280 -18 420 -36" stroke="#ffffff" stroke-opacity=".7" stroke-width="2" fill="none"/>')
    gilt(s, [hilt], 820, 838, 1.15, rot=-14, glow=.4, emboss=5)
    # hibiscus, leaves and buds
    hib_leaf(s, 520, 760, 190, rot=-62)
    hib_leaf(s, 600, 720, 170, rot=-20)
    hib_leaf(s, 840, 770, 160, rot=58)
    hibiscus(s, 700, 680, 175, rot=-10, seed=2)
    hibiscus(s, 420, 790, 70, rot=20, tilt=.7, seed=3, glow=False)
    bud = "M0 0C-16 -20 -14 -60 0 -84C14 -60 16 -20 0 0Z"
    s.add(f'<g transform="translate(930 760) rotate(40)"><path d="{bud}" fill="{s.lin([(0, "#ff4a4a", 1), (1, "#8a0618", 1)], 0, 0, 1, 0)}"/>'
          f'<path d="M-12 -4C-6 -20 6 -20 12 -4L0 6Z" fill="#2e5a3a"/></g>')
    ob.petals_scatter(s, 300, 1000, 760, 830, 16, colors=("#e81a2a", "#b80a20", "#ff4a40"), seed=5, size=(6, 11))
    ob.clay_diya(s, 220, 760, .55, flame_h=60)
    s.motes(26, 200, 1300, 300, 760, color="#ffb0a0", seed=8, size=(.6, 1.6))
    s.fx("godrays", cx=moon[0], cy=moon[1], strength=.2, thresh=.8, decay=.97, radius=200)
    s.fx("mottle", amp=.04, cell=60)
    s.look = {"vibrance": .1, "vignette": .42}
    return s


# =====================================================================================
# 9. Jyotirlinga
# =====================================================================================
def lingam_stone(s, cx, base, sc=1.0, stone="#2a2a36", rim="#fff0c8"):
    """A stone Shiva lingam on its yoni pedestal, with the tripundra and a kumkum dot."""
    t = f"translate({f(cx)} {f(base)}) scale({f(sc)})"
    sg = s.lin([(0, "#6a6a80", 1), (0.35, stone, 1), (1, "#0a0a10", 1)], 0, 0, 1, 0)
    top = s.lin([(0, "#8a8aa0", 1), (1, "#3a3a4a", 1)], 0, 0, 0, 1)
    s.add(f'<g transform="{t}">'
          f'<ellipse cx="0" cy="4" rx="150" ry="20" fill="#000" opacity=".5" filter="{s.blur(8)}"/>'
          f'<path d="M-110 -40V-8C-110 6 110 6 110 -8V-40Z" fill="{sg}"/>'
          f'<path d="M96 -46L190 -40C200 -38 200 -26 190 -24L100 -20Z" fill="{sg}"/>'
          f'<ellipse cx="0" cy="-40" rx="110" ry="24" fill="{top}"/>'
          f'<ellipse cx="0" cy="-42" rx="92" ry="17" fill="#1a1a24"/>'
          f'<path d="M-40 -42V-130C-40 -166 40 -166 40 -130V-42C40 -34 -40 -34 -40 -42Z" fill="{sg}"/>'
          f'<path d="M24 -150C34 -140 36 -110 36 -60" stroke="{rim}" stroke-opacity=".7" stroke-width="3" fill="none"/>'
          f'<path d="M-30 -112Q0 -106 30 -112M-31 -100Q0 -94 31 -100M-31 -88Q0 -82 31 -88" stroke="#f0ece4" stroke-width="4" fill="none" opacity=".9"/>'
          f'<circle cx="0" cy="-100" r="4.5" fill="#d02020"/>'
          f'<path d="M-110 -40C-60 -20 60 -20 110 -40" stroke="{rim}" stroke-opacity=".4" stroke-width="2" fill="none"/></g>')


@scene
def lingam(s):
    cx, wl = 800, 760
    s.sky([(0, "#03041a"), (.3, "#0a0c34"), (.55, "#1a1c52"), (.7, "#2a2a62"), (1, "#3a3470")])
    s.fx("nebula", seed=91, cell=300, colors=("#1a2a7a", "#4a2a8a", "#8a4aa0"), strength=.3, cx=800, cy=300, r=900, cover=.5)
    s.stars(200, 0, 600, seed=92, bright=.9)
    s.fx("clouds", y0=130, y1=420, seed=93, cell=150, aniso=4, cover=.42, soft=.2, lit="#c8c8ff", body=.8, direct=.8,
         light=(1, 0), sun=(cx, 300, 260), rim="#fff4dc", rim_a=1.0, opacity=.85)
    s.fx("beam", cx=cx, y0=0, y1=690, w=26, color="#fff2d6", a=1.0, halo=5)
    s.fx("addglow", cx=cx, cy=600, r=300, color="#ffc878", a=.5, sy=.6)
    s.fx("clouds", y0=430, y1=600, seed=94, cell=100, aniso=5, cover=.3, soft=.2, lit="#ffe8c0", body=.85, direct=.9,
         light=(1, 0), sun=(cx, 520, 320), rim="#fff8e8", opacity=.7)
    s.fx("beam", cx=cx, y0=420, y1=690, w=18, color="#fff8e8", a=.6, halo=3)
    # a tiny swan flying up beside the pillar, searching for its end
    s.birds(1, 840, 841, 150, 151, color="#fff8ec", s=(9, 9), seed=2, a=.9)
    far = ridgeline(wl - 50, 90, 95, cell=300, octaves=5, ridged=.45, envelope=[(0, 1.2), (650, .6), (950, .6), (1600, 1.2)])
    hills(s, far, "#1a1840", "#100e2a", rim="#ffd8a0", rim_a=.7, rim_center=(cx, 600), rim_r=700, haze="#5a4a7a", haze_a=.5, haze_h=60)
    s.mist(wl - 40, 80, "#8a7ab0", .4, 20)
    # the bank: a stone platform by the river
    bank = smooth_line([(-40, wl - 30), (300, wl - 26), (560, wl - 22), (700, wl - 20), (900, wl - 20), (1100, wl - 24), (1640, wl - 34)], 8)
    s.add(f'<path d="{P(bank + [(1640, wl + 4), (-40, wl + 4)])}" fill="#0c0a1c"/>')
    s.add(f'<path d="M640 {wl - 22}H960L980 {wl}H620Z" fill="{s.lin([(0, "#6a5a6a", 1), (1, "#2a2232", 1)], 0, wl - 22, 0, wl, user=True)}"/>')
    s.add(f'<path d="M640 {wl - 22}H960" stroke="#ffd8a0" stroke-opacity=".6" stroke-width="2"/>')
    s.glow(cx, wl - 60, 300, "#ffb860", .55, .25, sy=.6)
    lingam_stone(s, cx - 20, wl - 22, .9)
    for k, dx in enumerate((-150, -110, 110, 150)):
        ob.clay_diya(s, cx + dx, wl - 30, .16, flame_h=18, dots=False)
    s.add(ob.marigold(cx - 70, wl - 26, 9, "#f39a1c", 1) + ob.marigold(cx + 60, wl - 25, 8, "#f7c02a", 2) + ob.marigold(cx - 50, wl - 22, 7, "#e8562a", 3))
    s.fx("addglow", cx=cx, cy=wl - 170, r=60, color="#ffffff", a=.9)
    s.fx("reflect", y0=wl, strength=.85, tint="#0a0818", tint_near=.5, tint_far=.1, amp=4)
    s.fx("glints", y0=wl, cx=cx, color="#ffe8c0", width=50, strength=1.2, scatter=.06, density=.5)
    s.wisps(14, 0, W, wl + 8, wl + 70, "#c8b0d8", a=(.05, .14), length=(240, 700), thick=(6, 16), blur=10, seed=4)
    near = smooth_line([(-40, 900), (200, 930), (420, 1010)], 6)
    s.add(f'<path d="{P(near + [(-40, 1010)])}" fill="#05040c"/>')
    s.add(f'<path d="{P([(1640, 880), (1400, 930), (1200, 1010), (1640, 1010)])}" fill="#05040c"/>')
    grass(s, -40, 400, lambda x: y_at(near, x) + 2, 60, h=(10, 30), color="#05040c", seed=5)
    s.motes(40, 600, 1000, 100, 740, seed=6)
    s.fx("godrays", cx=cx, cy=500, strength=.3, thresh=.8, decay=.975, radius=320)
    s.fx("mottle", amp=.04, cell=60)
    return s


# =====================================================================================
# 10. The universal form
# =====================================================================================
@scene
def cosmos(s):
    c = (800, 500)
    s.add(f'<rect width="{W}" height="{H}" fill="{s.rad([(0, "#2a1a4a", 1), (0.4, "#120c30", 1), (1, "#03030c", 1)], c[0], c[1], 1000, user=True)}"/>')
    s.fx("nebula", seed=101, cell=360, colors=("#1a2a8a", "#5a2a9a", "#c0407a", "#ff9a50"), strength=.8, cx=c[0], cy=c[1], r=1000, cover=.55, dark=.35, falloff=1.1)
    s.fx("nebula", seed=102, cell=180, colors=("#2a6aa0", "#8a5ac0", "#ffd0a0"), strength=.5, cx=c[0], cy=c[1], r=800, cover=.4, warp=90, falloff=1.4)
    s.fx("starfield", n=9000, seed=103, cx=c[0], cy=c[1], r=900, bright=1.0)
    s.rays(*c, n=70, length=1100, width=.012, color="#fff0d0", a=.22, seed=9, blur=3)
    for k, (r, n, tilt) in enumerate(((180, 18, .42), (300, 26, .42), (440, 36, .42))):
        s.add(f'<ellipse cx="{c[0]}" cy="{c[1]}" rx="{r}" ry="{f(r * tilt)}" fill="none" stroke="#ffe8c0" stroke-opacity="{.22 - k * .05:.2f}" stroke-width="1.4" transform="rotate(-14 {c[0]} {c[1]})" style="mix-blend-mode:screen"/>')
        rng = random.Random(k)
        for i in range(n):
            a = 2 * math.pi * i / n + rng.uniform(-.05, .05)
            x, y = math.cos(a) * r, math.sin(a) * r * tilt
            x, y = rot_pts([(x, y)], -14, *c)[0]
            sz = rng.uniform(5, 11) * (1.1 if math.sin(a) > 0 else .8)
            s.glow(x, y, sz * 5, rng.choice(["#ffd890", "#ffe8c0", "#c8d8ff", "#ffb080"]), .5, .25)
            s.add(s.sparkle(x, y, sz, a=.9))
    for x, y, r, rot, col, sd in ((230, 190, 70, 30, "#b0c0ff", 1), (1380, 230, 90, -20, "#ffc8a0", 2), (1300, 800, 60, 60, "#d0b0ff", 3),
                                  (260, 790, 80, -40, "#ffd8b0", 4), (560, 120, 36, 10, "#c0d0ff", 5), (1080, 900, 40, -10, "#ffc0d0", 6)):
        galaxy(s, x, y, r, rot, .42, col, seed=sd)
    s.glow(*c, 520, "#ffb860", .55, .2)
    s.glow(*c, 200, "#fff0d0", .8, .3)
    s.add(f'<circle cx="{c[0]}" cy="{c[1]}" r="34" fill="#fffef8"/>')
    s.fx("addglow", cx=c[0], cy=c[1], r=140, color="#fff6e0", a=1.0)
    s.motes(80, 200, 1400, 60, 940, seed=11, size=(.6, 1.6))
    s.fx("godrays", cx=c[0], cy=c[1], strength=.4, thresh=.6, decay=.975, radius=360)
    s.fx("mottle", amp=.03, cell=60)
    s.look = {"vibrance": .1, "vignette": .4}
    return s


# =====================================================================================
# 12. The three gunas
# =====================================================================================
@scene
def three_strands(s):
    s.add(f'<rect width="{W}" height="{H}" fill="{s.rad([(0, "#1a1440", 1), (0.5, "#0c0a24", 1), (1, "#030310", 1)], 800, 500, 1000, user=True)}"/>')
    s.fx("nebula", seed=121, cell=320, colors=("#1a2a6a", "#4a2a7a", "#7a2a5a"), strength=.45, cx=800, cy=500, r=1000, cover=.5, dark=.3, falloff=1.0)
    s.fx("starfield", n=3500, seed=122, bright=.8)
    cy, A, wl = 500, 120, 2 * math.pi / 760
    strands = [  # (name, edge colour, face colour, glow)
        ("sattva", "#fff4d6", "#ffffff", "#ffe2a0"),
        ("rajas", "#ff4a2a", "#ff9a6a", "#ff3a20"),
        ("tamas", "#141a40", "#3a4a8a", "#3a50c0"),
    ]
    stamps = []
    for k, (_, c_edge, c_face, glow) in enumerate(strands):
        ph = 2 * math.pi * k / 3
        pts = []
        for i in range(700):
            x = -120 + i * 2.6
            t = x * wl + ph
            y = cy + A * math.sin(t) + 30 * math.sin(x / 400)
            z = math.sin(2 * t)
            pts.append((x, y, z, t))
        for i in range(1, len(pts) - 1):
            x, y, z, t = pts[i]
            dx = pts[i + 1][0] - pts[i - 1][0]
            dy = pts[i + 1][1] - pts[i - 1][1]
            L = math.hypot(dx, dy)
            nx, ny = -dy / L, dx / L
            twist = math.cos(t * 1.5 + k)
            w = 34 * (.35 + .65 * abs(twist))
            stamps.append((z, k, x, y, nx, ny, w, abs(twist)))
        line = "M" + "L".join(f"{f(x)} {f(y)}" for x, y, _, _ in pts)
        s.add(f'<path d="{line}" stroke="{glow}" stroke-width="{90 if k < 2 else 70}" fill="none" opacity="{.16 if k < 2 else .22}" filter="{s.blur(30)}" style="mix-blend-mode:screen"/>')
    stamps.sort(key=lambda e: e[0])
    out = []
    for z, k, x, y, nx, ny, w, lit in stamps:
        _, c_edge, c_face, _ = strands[k]
        col = mix(c_edge, c_face, lit * .8)
        if k == 2:
            col = mix("#0a0c22", "#4a5aa8", lit * .7)
        shade = .55 + .45 * (z + 1) / 2
        col = mix("#000000", col, shade)
        out.append(f'<path d="M{f(x - nx * w)} {f(y - ny * w)}L{f(x + nx * w)} {f(y + ny * w)}" stroke="{col}" stroke-width="3.4"/>')
    s.add(f'<g stroke-linecap="round">{"".join(out)}</g>')
    edge = []
    for z, k, x, y, nx, ny, w, lit in stamps[::3]:
        if k == 2:
            edge.append(f'<circle cx="{f(x + nx * w)}" cy="{f(y + ny * w)}" r="1.2" fill="#8aa0ff" opacity="{.25 + .4 * (z + 1) / 2:.2f}"/>')
    s.add("".join(edge))
    s.motes(60, 0, W, 300, 700, seed=12, size=(.6, 1.8))
    s.fx("mottle", amp=.03, cell=60)
    s.look = {"vibrance": .1, "vignette": .45}
    return s



# =====================================================================================
# 13. The wheel of samsara and the seed of action
# =====================================================================================
def light_wheel(s, cx, cy, R, spokes=12, color="#fff0d0", glow="#ffc870", rot=0.0):
    """A great wheel made of light, with trails that show it turning."""
    parts = [circle_d(cx, cy, R), circle_d(cx, cy, R * .93), circle_d(cx, cy, R * .3), circle_d(cx, cy, R * .12)]
    sp = []
    for k in range(spokes):
        a = math.radians(rot + 360 * k / spokes)
        x0, y0 = cx + math.cos(a) * R * .12, cy + math.sin(a) * R * .12
        x1, y1 = cx + math.cos(a) * R * .93, cy + math.sin(a) * R * .93
        sp.append(f"M{f(x0)} {f(y0)}L{f(x1)} {f(y1)}")
    beads = "".join(circle_d(cx + math.cos(math.radians(rot + 7.5 + 15 * k)) * R * .965, cy + math.sin(math.radians(rot + 7.5 + 15 * k)) * R * .965, 4) for k in range(24))
    d = "".join(parts) + "".join(sp)
    trails = []
    for k in range(spokes):
        a0 = rot + 360 * k / spokes
        for j in range(6):
            a = math.radians(a0 - j * 2.2)
            x1, y1 = cx + math.cos(a) * R * .93, cy + math.sin(a) * R * .93
            trails.append(f'<path d="M{f(cx)} {f(cy)}L{f(x1)} {f(y1)}" stroke="{color}" stroke-width="3" opacity="{.12 * (1 - j / 6):.2f}"/>')
    arcs = []
    for k in range(3):
        r = R * (1.04 + k * .04)
        a0, a1 = math.radians(-60 + k * 100), math.radians(20 + k * 100)
        arcs.append(f'<path d="M{f(cx + math.cos(a0) * r)} {f(cy + math.sin(a0) * r)}A{f(r)} {f(r)} 0 0 1 {f(cx + math.cos(a1) * r)} {f(cy + math.sin(a1) * r)}" stroke="{color}" stroke-width="2" fill="none" opacity="{.35 - k * .08:.2f}"/>')
    s.add(f'<g style="mix-blend-mode:screen"><g filter="{s.blur(14)}"><path d="{d}" stroke="{glow}" stroke-width="16" fill="none" opacity=".55"/></g>'
          f'<g filter="{s.blur(2)}">{"".join(trails)}{"".join(arcs)}</g>'
          f'<path d="{d}" stroke="{color}" stroke-width="4" fill="none"/><path d="{beads}" fill="#ffffff"/></g>')


@scene
def wheel(s):
    c, R, hz = (800, 330), 255, 660
    s.sky([(0, "#0c0e34"), (.25, "#24245e"), (.45, "#5a3c7c"), (.58, "#b0607c"), (.64, "#f09a7a"), (.67, "#ffd09a")])
    s.stars(90, 0, 300, seed=131, bright=.7)
    s.glow(*c, 700, "#ffb870", .45, .2)
    s.fx("clouds", y0=420, y1=640, seed=132, cell=90, aniso=6, cover=.3, soft=.2, lit="#ffd8b0", body=.85, direct=.9,
         light=(0, -1), sun=(c[0], c[1], 500), opacity=.85)
    s.rays(*c, n=36, length=900, width=.025, color="#ffe2a0", a=.15, seed=3)
    light_wheel(s, *c, R, rot=8)
    s.fx("addglow", cx=c[0], cy=c[1], r=90, color="#fff4dc", a=.9)
    far = ridgeline(hz, 50, 133, cell=280, octaves=5, ridged=.3)
    hills(s, far, "#7a4a7a", "#a06080", haze="#ffc0a0", haze_a=.5, haze_h=40)
    s.mist(hz - 4, 50, "#ffd0b0", .55, 12)
    mid = ridgeline(760, 60, 134, cell=320, octaves=5, ridged=.2, envelope=[(0, 1), (800, .4), (1600, 1)])
    hills(s, mid, "#4a2c52", "#2a1a34", rim="#ffd0a0", rim_a=.7, rim_center=c, rim_r=900, haze="#c08090", haze_a=.35, haze_h=60)
    # field rows on the middle ground
    rows = "".join(f'<path d="M{f(-40)} {f(770 + k * k * 3)}Q800 {f(756 + k * k * 3)} 1640 {f(770 + k * k * 3)}" stroke="#ffd0a0" stroke-opacity="{.05 + k * .01:.2f}" stroke-width="2" fill="none"/>' for k in range(1, 9))
    s.add(rows)
    round_tree(s, 1260, 790, 230, color="#1e1428", seed=4, crowns=5)
    rng = random.Random(5)
    fruit = "".join(f'<circle cx="{f(rng.uniform(1180, 1350))}" cy="{f(rng.uniform(600, 700))}" r="{f(rng.uniform(5, 8))}" fill="#f4b030" opacity=".9"/>' for _ in range(14))
    s.add(fruit)
    round_tree(s, 300, 780, 160, color="#20152a", seed=6, crowns=4)
    s.mist(800, 80, "#a07090", .3, 22)
    # the earth in the foreground, and the seedling
    mound = smooth_line([(-40, 1010), (200, 930), (500, 890), (800, 876), (1100, 890), (1400, 930), (1640, 1010)], 6)
    s.add(f'<path d="{P(mound)}" fill="{s.lin([(0, "#3a2420", 1), (1, "#120a0a", 1)], 0, 870, 0, 1000, user=True)}"/>')
    s.add(f'<path d="{P(mound)}" fill="#000" opacity=".3" filter="{s.grain(.35, 3, .3, 5, "#ffffff")}"/>')
    s.add(f'<path d="{"M" + "L".join(f"{f(x)} {f(y)}" for x, y in mound)}" stroke="#ffc890" stroke-opacity=".45" stroke-width="2.4" fill="none"/>')
    s.glow(800, 880, 220, "#ffd090", .45, .3, sy=.5)
    sx, sy0 = 800, 880
    stem = f"M{sx - 3} {sy0}C{sx - 8} {sy0 - 40} {sx + 10} {sy0 - 70} {sx + 2} {sy0 - 112}L{sx + 8} {sy0 - 112}C{sx + 18} {sy0 - 70} {sx} {sy0 - 40} {sx + 4} {sy0}Z"
    leaf = "M0 0C20 -26 62 -36 96 -22C70 2 30 10 0 0Z"
    lg = s.lin([(0, "#c8f080", 1), (0.5, "#6ab040", 1), (1, "#2a6a2a", 1)], 0, 0, 1, 1)
    s.add(f'<path d="{stem}" fill="#7ab048"/>'
          f'<g transform="translate({sx + 5} {sy0 - 110}) rotate(-28)"><path d="{leaf}" fill="{lg}"/><path d="M4 -2C30 -14 60 -20 90 -22" stroke="#e8ffc0" stroke-opacity=".6" stroke-width="1.6" fill="none"/></g>'
          f'<g transform="translate({sx + 5} {sy0 - 110}) scale(-1 1) rotate(-34)"><path d="{leaf}" fill="{lg}"/><path d="M4 -2C30 -14 60 -20 90 -22" stroke="#e8ffc0" stroke-opacity=".6" stroke-width="1.6" fill="none"/></g>'
          f'<path d="M{sx + 5} {sy0 - 112}C{sx} {sy0 - 130} {sx + 6} {sy0 - 146} {sx + 14} {sy0 - 150}C{sx + 16} {sy0 - 134} {sx + 12} {sy0 - 120} {sx + 5} {sy0 - 112}Z" fill="#a8e070"/>'
          f'<path d="M{sx - 34} {sy0 + 2}C{sx - 30} {sy0 - 14} {sx - 10} {sy0 - 16} {sx - 6} {sy0 - 2}Z" fill="#8a5a2a"/>'
          f'<path d="M{sx + 16} {sy0 + 2}C{sx + 22} {sy0 - 12} {sx + 40} {sy0 - 10} {sx + 42} {sy0 + 2}Z" fill="#6a4020"/>')
    s.add(s.sparkle(sx + 92, sy0 - 136, 8))
    grass(s, -40, 1640, lambda x: y_at(mound, x) + 3, 160, h=(6, 22), color="#120a0a", seed=8)
    s.motes(40, 300, 1300, 100, 880, seed=9)
    s.fx("godrays", cx=c[0], cy=c[1], strength=.35, thresh=.72, decay=.97, radius=280)
    s.fx("mottle", amp=.04, cell=60)
    return s


# =====================================================================================
# 14. The circle of the Hindu year
# =====================================================================================
@scene
def calendar_wheel(s):
    c, R = (800, 500), 360
    s.add(f'<rect width="{W}" height="{H}" fill="{s.rad([(0, "#24204e", 1), (0.5, "#0e0c2c", 1), (1, "#04040e", 1)], c[0], c[1], 1000, user=True)}"/>')
    s.fx("nebula", seed=141, cell=300, colors=("#1a2a7a", "#4a2a8a", "#a04a7a", "#e0905a"), strength=.45, cx=c[0], cy=c[1], r=1000, cover=.5, dark=.3, falloff=.9)
    s.fx("starfield", n=4000, seed=142, bright=.85)
    s.glow(*c, 640, "#ffb060", .35, .2)
    gold = s.lin([(0, "#fff2c8", 1), (0.4, "#f2c76a", 1), (0.75, "#d0902e", 1), (1, "#9a5a1a", 1)], c[0] - 400, c[1] - 400, c[0] + 400, c[1] + 400, user=True)
    fil = s.gold_filter(3.4, az=225, el=48)
    rings = "".join(circle_d(*c, R * k) for k in (1, .935, .8, .745, .47, .42))
    s.add(f'<path d="{circle_d(*c, R) + circle_d(*c, R * .42)}" fill="#1a0e20" fill-opacity=".55" fill-rule="evenodd"/>')
    # twelve months as twelve lotus petals, divided by radial lines
    divs = "".join(f"M{f(c[0] + math.cos(math.radians(30 * k - 90)) * R * .47)} {f(c[1] + math.sin(math.radians(30 * k - 90)) * R * .47)}"
                   f"L{f(c[0] + math.cos(math.radians(30 * k - 90)) * R * .745)} {f(c[1] + math.sin(math.radians(30 * k - 90)) * R * .745)}" for k in range(12))
    petals = ring_petals_d(*c, 12, R * .48, R * .73, math.pi / 12, width=.78)
    inner = ring_petals_d(*c, 12, R * .48, R * .73, math.pi / 12, width=.78, inner=True)
    # twenty-seven nakshatras: a star in each mansion of the moon's path, with ticks
    ticks = "".join(f"M{f(c[0] + math.cos(a) * R * .8)} {f(c[1] + math.sin(a) * R * .8)}L{f(c[0] + math.cos(a) * R * .935)} {f(c[1] + math.sin(a) * R * .935)}"
                    for a in [math.radians(-90 + 360 * k / 27) for k in range(27)])
    # sixty beads for the sixty years of the cycle
    beads = "".join(circle_d(c[0] + math.cos(a) * R * .968, c[1] + math.sin(a) * R * .968, 5.2) for a in [math.radians(-90 + 6 * k) for k in range(60)])
    s.add(f'<g filter="{s.blur(6)}" opacity=".6" style="mix-blend-mode:screen"><path d="{rings + divs + ticks}" stroke="#ff9a40" stroke-width="7" fill="none"/></g>')
    s.add(f'<path d="{petals}" fill="{s.rad([(0, "#ff9a6a", 0), (0.6, "#c8504a", .25), (1, "#ffb080", .45)], c[0], c[1], R * .75, user=True)}"/>')
    s.add(f'<g filter="{fil}"><path d="{rings + divs + ticks}" stroke="{gold}" stroke-width="4" fill="none"/>'
          f'<path d="{petals}" stroke="{gold}" stroke-width="3" fill="none"/><path d="{inner}" stroke="{gold}" stroke-width="1.6" fill="none" opacity=".7"/>'
          f'<path d="{beads}" fill="{gold}"/></g>')
    for k in range(27):
        a = math.radians(-90 + 360 * (k + .5) / 27)
        s.add(s.sparkle(c[0] + math.cos(a) * R * .868, c[1] + math.sin(a) * R * .868, 7, a=.95))
    # the sun at the centre, the moon set into the ring of months
    s.glow(*c, 260, "#ffb050", .6, .25)
    flames = "".join(petal_d(10, 34, c[0] + math.cos(math.radians(a)) * 108, c[1] + math.sin(math.radians(a)) * 108, a + 90) for a in range(0, 360, 15))
    gilt(s, [flames], 0, 0, 1, glow=.8, emboss=4)
    s.sun(*c, 96, core="#fff6dc", rim="#ffc860", halo="#ffa040", halo_r=280, halo_a=.5)
    mx, my = c[0] + math.cos(math.radians(-50)) * R * .605, c[1] + math.sin(math.radians(-50)) * R * .605
    s.add(f'<circle cx="{f(mx)}" cy="{f(my)}" r="42" fill="#0c0a24"/><circle cx="{f(mx)}" cy="{f(my)}" r="42" fill="none" stroke="{gold}" stroke-width="4" filter="{fil}"/>')
    crescent(s, mx, my, 32, off=(-.45, -.25), glow_r=170, glow_a=.55)
    s.motes(40, 300, 1300, 80, 920, seed=14)
    s.fx("addglow", cx=c[0], cy=c[1], r=110, color="#fff2d0", a=.7)
    s.fx("mottle", amp=.03, cell=60)
    s.look = {"vignette": .42}
    return s


# =====================================================================================
# 15. The phases of the moon
# =====================================================================================
def moon_phase(s, cx, cy, r, frac, waxing=True, seed=1):
    """The moon at a given illuminated fraction (0 new, 1 full); waxing is lit on the right."""
    k = 1 - 2 * frac
    sgn = 1 if waxing else -1
    top, bot = (cx, cy - r), (cx, cy + r)
    s.add(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="#1e2448" opacity=".9"/>'
          f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="none" stroke="#8a96d0" stroke-opacity=".25" stroke-width="1.2"/>')
    if frac <= .01:
        return
    outer_sweep = 1 if waxing else 0
    term_sweep = (0 if k > 0 else 1) if waxing else (1 if k > 0 else 0)
    d = (f"M{f(top[0])} {f(top[1])}A{f(r)} {f(r)} 0 0 {outer_sweep} {f(bot[0])} {f(bot[1])}"
         f"A{f(max(.01, abs(k) * r))} {f(r)} 0 0 {term_sweep} {f(top[0])} {f(top[1])}Z")
    s.glow(cx + sgn * r * (1 - frac) * .5, cy, r * (2.5 + 3 * frac), "#c8d4ff", .25 + .3 * frac, .14)
    g = s.rad([(0, "#ffffff", 1), (0.6, "#f6f0dc", 1), (1, "#d0c8b0", 1)], cx - r * .25, cy - r * .3, r * 1.35, user=True)
    rng = random.Random(seed)
    maria = "".join(f'<ellipse cx="{f(cx + math.cos(a) * dd)}" cy="{f(cy + math.sin(a) * dd)}" rx="{f(cr)}" ry="{f(cr * .8)}" fill="#a9a08a" opacity=".22"/>'
                    for a, dd, cr in [(rng.uniform(0, 6.28), rng.uniform(0, r * .6), rng.uniform(r * .08, r * .22)) for _ in range(9)])
    cid = s.clip(d)
    s.add(f'<g clip-path="{cid}"><circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{g}"/><g filter="{s.blur(max(1, r * .05))}">{maria}</g></g>')


@scene
def moon_phases(s):
    wl = 760
    s.sky([(0, "#03051c"), (.35, "#0a1040"), (.6, "#1a2460"), (.72, "#2c3672"), (.76, "#3a4280")])
    s.stars(220, 0, 700, seed=151, bright=.9)
    s.add(f'<path d="M150 590C200 120 1400 120 1450 590" stroke="#c8d4ff" stroke-width="40" fill="none" opacity=".08" filter="{s.blur(20)}"/>')
    n = 9
    for k in range(n):
        th = math.pi * (1 - k / (n - 1))
        x, y = 800 + 650 * math.cos(th), 600 - 410 * math.sin(th)
        frac = (1 - math.cos(2 * math.pi * k / (n - 1))) / 2
        r = 30 + 30 * math.sin(th)
        moon_phase(s, x, y, r, frac, waxing=k < (n - 1) / 2, seed=k)
    s.fx("clouds", y0=500, y1=700, seed=152, cell=90, aniso=6, cover=.26, soft=.2, lit="#b8c4f0", body=.85, direct=.7,
         light=(0, -1), sun=(800, 190, 500), opacity=.6)
    far = ridgeline(wl, 34, 153, cell=260, octaves=5, ridged=.3)
    hills(s, far, "#141a44", "#0e1232")
    rr = random.Random(4)
    cr = "".join(crown(x, wl - rr.uniform(6, 18), rr.uniform(12, 24), seed=int(x)) for x in list(range(-20, 900, 14)) + list(range(1300, 1640, 14)))
    s.add(f'<path d="{cr}" fill="#0c1028"/>')
    arch.nagara(s, 1120, wl - 4, .62, color="#0c1028", rim="#c8d4ff", light=-1, shade="#000000")
    arch.chhatri(s, 960, wl - 4, .7, color="#0c1028", rim="#c8d4ff", light=-1)
    for x in (900, 1000, 1180, 1240):
        s.flame(x, wl - 6, 8, glow_r=50, glow_a=.45)
    s.mist(wl - 4, 30, "#4a5490", .4, 8)
    s.fx("reflect", y0=wl, strength=.85, tint="#04061a", tint_near=.5, tint_far=.1, amp=3)
    s.fx("glints", y0=wl, cx=800, color="#d8e0ff", width=50, strength=.9, scatter=.06, density=.45)
    s.wisps(12, 0, W, wl + 8, wl + 60, "#8a96d0", a=(.05, .12), length=(240, 700), thick=(6, 16), blur=10, seed=4)
    for k in range(9):
        t = k / 8
        arch.leaf_lamp(s, 520 + 600 * t + random.Random(k).uniform(-60, 60), wl + 40 + 180 * t * t, .4 + .9 * t * t, seed=k)
    reeds = smooth_line([(-40, 960), (160, 940), (320, 1010)], 6)
    s.add(f'<path d="{P(reeds + [(-40, 1010)])}" fill="#03040c"/>')
    grass(s, -40, 340, lambda x: y_at(reeds, x) + 2, 60, h=(30, 90), color="#03040c", seed=6, lean=.15)
    s.motes(20, 300, 1300, 200, 740, color="#c8d4ff", seed=7, size=(.6, 1.4))
    s.fx("mottle", amp=.04, cell=60)
    return s


# =====================================================================================
# 16. Sun and moon: a baby's first outing
# =====================================================================================
def mother_d():
    """A mother in a sari, the pallu over her head, side-on facing right and holding her
    baby up towards the sky; feet at y=0 (about 300 tall)."""
    body = [(22, -282), (30, -274), (37, -266), (31, -262), (33, -256), (28, -248), (20, -240), (26, -226), (30, -200), (30, -160),
            (32, -130), (40, -80), (48, -20), (56, 0), (-46, 0), (-40, -50), (-32, -110), (-28, -150), (-22, -180), (-26, -210),
            (-22, -234), (-18, -254), (-14, -272), (0, -292), (14, -294)]
    pallu = [(-14, -268), (-30, -240), (-44, -200), (-54, -150), (-50, -116), (-38, -140), (-28, -180), (-18, -226)]
    arms = [(20, -232), (34, -204), (64, -198), (80, -206), (76, -214), (56, -212), (38, -214), (28, -224)]
    baby = "".join(P(rot_pts([(math.cos(a) * 26, math.sin(a) * 15) for a in [k * math.pi / 18 for k in range(36)]], -24, 62, -220)) for _ in [0])
    head = ellipse_d(86, -236, 10, 10)
    pleats = "M10 -120L16 -4M22 -110L32 -6M-2 -118L-4 -4"
    return P(smooth_line(body, 3)) + P(smooth_line(pallu, 3)) + P(arms) + baby + head, pleats


@scene
def sun_moon(s):
    sun, moon, hz = (360, 600), (1260, 250), 650
    s.sky([(0, "#141a4a"), (.25, "#2a2c6a"), (.45, "#6a4c8a"), (.58, "#c8708a"), (.64, "#f8a070"), (.66, "#ffc890")])
    s.add(f'<rect width="{W}" height="{H}" fill="{s.lin([(0, "#ff9a50", .35), (.45, "#ff9a50", 0), (.6, "#3a4aa0", 0), (1, "#3a4aa0", .35)], 0, 0, W, 0, user=True)}"/>')
    s.stars(70, 0, 380, seed=161, bright=.7, x0=820, x1=1600)
    s.sun(*sun, 40, halo_r=640, halo_a=.85)
    s.moon(*moon, 46, glow="#d8e0ff", glow_r=420)
    s.fx("clouds", y0=60, y1=330, seed=162, cell=140, aniso=4, cover=.34, soft=.18, lit="#ffb8a0", body=.75, direct=.8,
         light=(-1, .6), sun=(sun[0], sun[1], 500), opacity=.85)
    s.fx("clouds", y0=480, y1=630, seed=163, cell=80, aniso=6, cover=.3, soft=.2, lit="#ffd8b0", body=.85, direct=.95,
         light=(-1, .3), sun=(sun[0], sun[1], 360), opacity=.8)
    far = ridgeline(hz, 60, 164, cell=300, octaves=5, ridged=.35)
    hills(s, far, "#8a5a8a", "#6a4a7a", haze="#ffc0a0", haze_a=.5, haze_h=50)
    s.mist(hz - 6, 50, "#ffc8b0", .55, 12)
    mid = ridgeline(740, 50, 165, cell=280, octaves=5, ridged=.25)
    hills(s, mid, "#4a3060", "#2c1e40", rim="#ffc890", rim_a=.7, rim_center=sun, rim_r=900, haze="#c08090", haze_a=.35, haze_h=60)
    arch.nagara(s, 1260, 742, .42, color="#2c1e40", rim="#ffc890", light=-1)
    rng = random.Random(6)
    for _ in range(18):
        x = rng.uniform(900, 1500)
        s.flame(x, rng.uniform(744, 790), 5, glow_r=30, glow_a=.4)
    s.mist(780, 70, "#c08aa0", .35, 20)
    # the terrace: floor, low parapet with lamps, and a tulsi planter
    floor = s.lin([(0, "#3a2434", 1), (1, "#0e0810", 1)], 0, 880, 0, 1000, user=True)
    s.add(f'<rect y="880" width="1600" height="130" fill="{floor}"/>')
    wall = s.lin([(0, "#4a2e40", 1), (1, "#1a1020", 1)], 0, 780, 0, 880, user=True)
    for x0, x1 in ((-20, 560), (1040, 1620)):
        s.add(f'<rect x="{x0}" y="790" width="{x1 - x0}" height="90" fill="{wall}"/><rect x="{x0}" y="780" width="{x1 - x0}" height="14" fill="#5a3a4a"/>'
              f'<path d="M{x0} 781H{x1}" stroke="#ffc890" stroke-opacity=".7" stroke-width="2"/>')
        bal = "".join(f'<path d="M{x - 9} 800H{x + 9}L{x + 6} 812C{x + 12} 830 {x + 12} 850 {x + 6} 866H{x - 6}C{x - 12} 850 {x - 12} 830 {x - 6} 812Z" fill="#160c18"/>' for x in range(x0 + 30, x1 - 10, 44))
        s.add(bal)
    s.add(f'<path d="M1100 780L1112 700H1188L1200 780Z" fill="#5a3442"/><rect x="1104" y="690" width="92" height="12" fill="#6a4050"/>'
          f'<path d="M1150 690C1150 640 1140 620 1150 590M1150 660C1130 640 1120 640 1112 628M1150 650C1168 632 1180 630 1190 620" stroke="#2a4a2a" stroke-width="4" fill="none"/>')
    rng = random.Random(8)
    s.add("".join(f'<ellipse cx="{f(1150 + rng.uniform(-40, 40))}" cy="{f(rng.uniform(590, 680))}" rx="7" ry="3.5" fill="#3a6a3a" transform="rotate({rng.uniform(-40, 40):.0f} 1150 640)"/>' for _ in range(26)))
    ob.clay_diya(s, 470, 778, .22, flame_h=26, dots=False)
    ob.clay_diya(s, 1080, 778, .22, flame_h=26, dots=False)
    # mother and child
    sil, pleats = mother_d()
    s.glow(820, 560, 360, "#ffd8b0", .25, .25)
    silhouette(s, sil, 780, 884, 1.5, color="#160c1a", rim="#ffd090", light=sun, rim_r=900, rim_w=4,
               extra=f'<path d="{pleats}" stroke="#ffd090" stroke-opacity=".12" stroke-width="2"/>')
    s.add(f'<ellipse cx="790" cy="886" rx="120" ry="10" fill="#000" opacity=".5" filter="{s.blur(6)}"/>')
    s.birds(6, 600, 820, 380, 440, color="#3a2040", s=(5, 9), seed=3, a=.8)
    s.motes(30, 300, 1300, 300, 860, seed=9)
    s.fx("godrays", cx=sun[0], cy=sun[1], strength=.4, thresh=.72, decay=.97, radius=260)
    s.fx("mottle", amp=.04, cell=60)
    return s


# =====================================================================================
# 17. Vamana's three strides
# =====================================================================================
def foot_d(left=False):
    """A footprint, toes up, about 200 long, heel at +y."""
    sole = ("M0 100C-34 100 -42 62 -38 22C-36 -8 -50 -38 -46 -64C-42 -88 -10 -84 10 -86C40 -88 58 -72 54 -46"
            "C50 -12 36 20 34 52C32 86 24 100 0 100Z")
    toes = ellipse_d(-26, -106, 17, 20) + ellipse_d(4, -114, 11, 13) + ellipse_d(25, -108, 10, 12) + ellipse_d(42, -95, 9, 10) + ellipse_d(54, -78, 7, 8)
    return sole + toes, -1 if left else 1


def footprint(s, x, y, sc=1.0, rot=0.0, squash=1.0, left=False, a=1.0):
    d, _ = foot_d(left)
    sx = -sc if left else sc
    t = f"translate({f(x)} {f(y)}) scale(1 {f(squash)}) rotate({f(rot)}) scale({f(sx)} {f(sc)})"
    parts, beads = chakra_d(100)
    s.add(f'<g transform="{t}" opacity="{a}"><path d="{d}" fill="#ffb050" opacity=".8" filter="{s.blur(22 / sc)}" style="mix-blend-mode:screen"/>'
          f'<path d="{d}" fill="#ffe8b0" opacity=".9" filter="{s.blur(6 / sc)}"/>'
          f'<path d="{d}" fill="{s.rad([(0, "#ffffff", 1), (0.6, "#fff0c8", 1), (1, "#ffc860", 1)], .5, .45, .6)}"/>'
          f'<g transform="translate(2 -10) scale(.2)" opacity=".55"><path d="{"".join(parts)}" fill="#e09030" fill-rule="evenodd"/></g>'
          f'<path d="M-10 60C-6 70 6 70 10 60" stroke="#e09030" stroke-opacity=".5" stroke-width="3" fill="none"/></g>')


def chhatra(s, x, y, sc=1.0, rot=0.0):
    """A small palm-leaf parasol; (x, y) is the foot of its handle."""
    t = f"translate({f(x)} {f(y)}) rotate({f(rot)}) scale({f(sc)})"
    canopy = "M-96 -196C-70 -246 70 -246 96 -196C84 -190 72 -198 60 -192C46 -186 34 -194 20 -188C8 -184 -8 -184 -20 -188C-34 -194 -46 -186 -60 -192C-72 -198 -84 -190 -96 -196Z"
    ribs = "".join(f"M0 -238L{f(k)} -192" for k in range(-90, 100, 22))
    cg = s.lin([(0, "#ffe8a8", 1), (0.5, "#e0a850", 1), (1, "#8a5420", 1)], 0, 0, 0, 1)
    s.add(f'<g transform="{t}"><path d="M-3 0V-236H3V0Z" fill="#6a3c18"/><path d="{canopy}" fill="{cg}"/>'
          f'<path d="{ribs}" stroke="#7a4a1c" stroke-opacity=".5" stroke-width="1.6"/>'
          f'<path d="M-96 -196C-70 -246 70 -246 96 -196" stroke="#fff4d0" stroke-opacity=".7" stroke-width="2" fill="none"/>'
          f'<circle cx="0" cy="-240" r="6" fill="#e8b860"/><circle cx="0" cy="-4" r="5" fill="#4a2a10"/></g>')


@scene
def vamana(s):
    wl, sun = 720, (420, 660)
    s.sky([(0, "#05071e"), (.22, "#141850"), (.42, "#3a3478"), (.56, "#9a5a8a"), (.64, "#f0907a"), (.7, "#ffc890")])
    s.stars(160, 0, 360, seed=171, bright=.9)
    s.sun(*sun, 34, halo_r=620, halo_a=.8)
    s.fx("clouds", y0=320, y1=560, seed=172, cell=130, aniso=4, cover=.4, soft=.18, lit="#ffd0b0", body=.8, direct=.9,
         light=(-.6, 1), sun=(sun[0], sun[1], 600), rim="#fff0d0", opacity=.95)
    far = ridgeline(668, 60, 173, cell=300, octaves=5, ridged=.35)
    hills(s, far, "#8a5a8a", "#5a3c6a", haze="#ffc0a0", haze_a=.5, haze_h=40)
    s.mist(664, 40, "#ffc8b0", .5, 10)
    meadow = smooth_line([(-40, 700), (400, 690), (800, 684), (1200, 690), (1640, 700)], 10)
    s.add(f'<path d="{P(meadow + [(1640, wl + 4), (-40, wl + 4)])}" fill="{s.lin([(0, "#5a3a5a", 1), (1, "#3a2440", 1)], 0, 680, 0, wl, user=True)}"/>')
    # the three strides: earth, cloud and sky
    trail = smooth_line([(660, 694), (780, 560), (900, 440), (1010, 300), (1120, 170)], 6)
    s.add(f'<path d="{"M" + "L".join(f"{f(x)} {f(y)}" for x, y in trail)}" stroke="#ffe0a0" stroke-width="3" stroke-dasharray="2 14" stroke-linecap="round" fill="none" opacity=".55"/>')
    footprint(s, 660, 698, .8, rot=24, squash=.42)
    footprint(s, 900, 440, 1.0, rot=22, squash=.6, left=True)
    footprint(s, 1130, 160, 1.15, rot=18, squash=.9, a=.85)
    s.fx("addglow", cx=660, cy=698, r=140, color="#ffd090", a=.5, sy=.4)
    s.fx("addglow", cx=1130, cy=160, r=220, color="#ffd8a0", a=.35)
    s.fx("reflect", y0=wl, strength=.85, tint="#1a1030", tint_near=.5, tint_far=.1, amp=4)
    s.fx("glints", y0=wl, cx=sun[0], color="#ffe8c0", width=50, strength=1.1, scatter=.06, density=.5)
    s.wisps(12, 0, W, wl + 8, wl + 70, "#ffd0b8", a=(.06, .16), length=(240, 700), thick=(6, 16), blur=10, seed=6)
    # the near bank with the parasol and the water pot
    bank = smooth_line([(-40, 820), (200, 816), (420, 830), (600, 860), (760, 920), (860, 1010)], 6)
    s.add(f'<path d="{P(bank + [(-40, 1010)])}" fill="{s.lin([(0, "#2a1a2c", 1), (1, "#0c0810", 1)], 0, 810, 0, 1000, user=True)}"/>')
    s.add(f'<path d="{"M" + "L".join(f"{f(x)} {f(y)}" for x, y in bank)}" stroke="#ffc890" stroke-opacity=".6" stroke-width="2.4" fill="none"/>')
    s.glow(380, 820, 220, "#ffc080", .3, .3, sy=.5)
    chhatra(s, 380, 846, .8, rot=-12)
    s.add(f'<ellipse cx="500" cy="840" rx="44" ry="6" fill="#000" opacity=".45" filter="{s.blur(3)}"/>')
    gilt(s, kamandalu_d(), 500, 804, .5, glow=.4, emboss=4)
    grass(s, -40, 860, lambda x: y_at(bank, x) + 3, 90, h=(8, 26), color="#0c0810", seed=7)
    s.motes(50, 600, 1400, 80, 720, seed=8)
    s.fx("godrays", cx=sun[0], cy=sun[1], strength=.35, thresh=.72, decay=.97, radius=260)
    s.fx("mottle", amp=.04, cell=60)
    return s
