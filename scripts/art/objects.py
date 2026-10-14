"""Sacred objects and plants: lotuses and their leaves, lamps, garlands, gold symbols."""
import math
import random

from glyphs import OM
from paint import f, mix


def _petal(w, h, pinch=0.0):
    return (f"M0 0C{f(-w * .62)} {f(-h * .12)} {f(-w * .58)} {f(-h * (.72 - pinch))} 0 {f(-h)}"
            f"C{f(w * .58)} {f(-h * (.72 - pinch))} {f(w * .62)} {f(-h * .12)} 0 0Z")


def lotus(s, cx, cy, sc=1.0, tip="#e9558f", base="#fff5ee", edge="#c23a73", glow="#ffd2e0", seed=1, bloom=1.0, lit=1.0):
    """A sacred lotus in bloom seen from the side; (cx, cy) is where the flower meets its stem.
    About 230 units across at sc=1."""
    rng = random.Random(seed)
    rows = [  # (angles, length, width, darken)
        ([-82, -58, 58, 82], 118, 54, .22),
        ([-64, -38, 38, 64], 124, 56, .12),
        ([-46, -16, 16, 46], 128, 58, .05),
    ]
    front = ([-26, 0, 26], 112, 62, 0.0)
    out = [f'<g transform="translate({f(cx)} {f(cy)}) scale({f(sc)})">']
    if glow:
        out.append(f'<ellipse cx="0" cy="-60" rx="170" ry="130" fill="{s.rad([(0, glow, .35 * lit), (1, glow, 0)])}" style="mix-blend-mode:screen"/>')

    def petals(spec, open_k):
        angles, L, Wd, dk = spec
        res = []
        for a in angles:
            a2 = a * bloom * open_k + rng.uniform(-3, 3)
            t = mix(tip, "#5a1830", dk)
            g = s.lin([(0, base, 1), (0.45, mix(base, t, .25), 1), (0.85, t, 1), (1, mix(t, "#ffffff", .1), 1)], 0, 1, 0, 0)
            L2 = L * rng.uniform(.94, 1.04)
            d = _petal(Wd, L2, rng.uniform(0, .08))
            veins = "".join(f"M{f(k * 6)} -8Q{f(k * 10)} {f(-L2 * .5)} {f(k * 4)} {f(-L2 * .9)}" for k in (-1, 0, 1))
            res.append(f'<g transform="rotate({a2:.1f})"><path d="{d}" fill="{g}" stroke="{edge}" stroke-opacity=".35" stroke-width="1.2"/>'
                       f'<path d="{veins}" stroke="{edge}" stroke-opacity=".18" stroke-width="1.1" fill="none"/>'
                       f'<path d="M{f(-Wd * .18)} {f(-L2 * .2)}Q{f(-Wd * .22)} {f(-L2 * .6)} 0 {f(-L2 * .94)}" stroke="#fff" stroke-opacity=".35" stroke-width="2" fill="none"/></g>')
        return res

    for spec in rows:
        out += petals(spec, 1.0)
    # seed pod and stamens
    out.append('<g transform="translate(0 -34)">')
    st = []
    for k in range(34):
        a = -math.pi + math.pi * (k + .5) / 34
        r = 30 + rng.uniform(-3, 4)
        st.append(f"M{f(math.cos(a) * 12)} 0Q{f(math.cos(a) * r * .6)} {f(-10 + math.sin(a) * 8)} {f(math.cos(a) * r)} {f(math.sin(a) * r * .55 - 6)}")
    out.append(f'<path d="{"".join(st)}" stroke="#f7c948" stroke-width="2" fill="none" stroke-linecap="round"/>')
    out.append(f'<path d="M-20 -4C-20 -16 20 -16 20 -4C20 4 -20 4 -20 -4Z" fill="{s.lin([(0, "#e9f0a0", 1), (1, "#b8c254", 1)], 0, 0, 0, 1)}"/>')
    out.append("".join(f'<circle cx="{x}" cy="{y}" r="2" fill="#8c9a3a"/>' for x, y in ((-10, -9), (0, -10), (10, -9), (-5, -5), (5, -5))))
    out.append('</g>')
    out += petals(front, 1.0)
    out.append('</g>')
    s.add("".join(out))


def bud(s, x, y, sc=1.0, stem_to=None, tip="#e9558f", base="#fff1ea", stem="#2f5a3a"):
    """A closed lotus bud on its stem; (x, y) is the base of the bud."""
    if stem_to is not None:
        s.add(f'<path d="M{f(x)} {f(y)}Q{f(x + 6 * sc)} {f((y + stem_to) / 2)} {f(x + 2 * sc)} {f(stem_to)}" stroke="{stem}" stroke-width="{f(4 * sc)}" fill="none"/>')
    g = s.lin([(0, base, 1), (0.5, mix(base, tip, .4), 1), (1, tip, 1)], 0, 1, 0, 0)
    d = f"M0 0C-26 -10 -24 -52 0 -78C24 -52 26 -10 0 0Z"
    s.add(f'<g transform="translate({f(x)} {f(y)}) scale({f(sc)})"><path d="{d}" fill="{g}" stroke="#c23a73" stroke-opacity=".3"/>'
          f'<path d="M0 0C-14 -10 -14 -44 -2 -70" stroke="#c23a73" stroke-opacity=".3" fill="none"/>'
          f'<path d="M-4 -4C-26 -14 -30 -40 -20 -56C-14 -40 -8 -20 -4 -4Z" fill="{g}" opacity=".9"/></g>')


def pad(s, cx, cy, rx, ry=None, rot=0.0, dark="#173d33", light="#3f7f5c", rim="#b6d99a", rim_a=0.5, seed=1, notch=True):
    """A floating lotus leaf in perspective, with radiating veins and a lit rim."""
    rng = random.Random(seed)
    ry = ry or rx * .28
    a0 = rng.uniform(-.3, .3) + rot
    if notch:
        x1, y1 = cx + math.cos(a0 - .12) * rx, cy + math.sin(a0 - .12) * ry
        x2, y2 = cx + math.cos(a0 + .12) * rx, cy + math.sin(a0 + .12) * ry
        d = f"M{f(cx)} {f(cy)}L{f(x1)} {f(y1)}A{f(rx)} {f(ry)} 0 1 0 {f(x2)} {f(y2)}Z"
    else:
        d = f"M{f(cx - rx)} {f(cy)}A{f(rx)} {f(ry)} 0 1 0 {f(cx + rx)} {f(cy)}A{f(rx)} {f(ry)} 0 1 0 {f(cx - rx)} {f(cy)}Z"
    g = s.rad([(0, light, 1), (0.75, mix(light, dark, .5), 1), (1, dark, 1)], cx, cy - ry * .2, rx, user=True,
              transform=f"translate(0 {f(cy * (1 - ry / rx))}) scale(1 {f(ry / rx)})")
    veins = "".join(f"M{f(cx)} {f(cy)}L{f(cx + math.cos(a) * rx * .92)} {f(cy + math.sin(a) * ry * .92)}"
                    for a in [a0 + .5 + k * .52 for k in range(11)])
    s.add(f'<ellipse cx="{f(cx)}" cy="{f(cy + ry * .25)}" rx="{f(rx * 1.02)}" ry="{f(ry * 1.05)}" fill="#05070a" opacity=".35" filter="{s.blur(max(1, ry * .15))}"/>'
          f'<path d="{d}" fill="{g}"/><path d="{veins}" stroke="{rim}" stroke-opacity=".16" stroke-width="{f(max(.8, rx * .012))}"/>'
          f'<path d="M{f(cx - rx * .95)} {f(cy - ry * .3)}A{f(rx)} {f(ry)} 0 0 1 {f(cx + rx * .95)} {f(cy - ry * .3)}" stroke="{rim}" stroke-opacity="{rim_a}" stroke-width="{f(max(1, rx * .015))}" fill="none"/>')


def standing_leaf(s, x, y, sc=1.0, water=None, dark="#15352b", light="#5d9a66", rim="#d5ec9e", seed=1):
    """A lotus leaf held up above the water like a shallow bowl; (x, y) is the leaf centre."""
    rng = random.Random(seed)
    if water is not None:
        s.add(f'<path d="M{f(x)} {f(y + 20 * sc)}Q{f(x + rng.uniform(-18, 18) * sc)} {f((y + water) / 2)} {f(x + rng.uniform(-6, 6) * sc)} {f(water)}" stroke="#284d38" stroke-width="{f(5 * sc)}" fill="none"/>')
    rx, ry = 120 * sc, 30 * sc
    rim_pts = []
    for k in range(73):
        a = 2 * math.pi * k / 72
        wav = 1 + .04 * math.sin(k * 1.9 + seed) + .03 * math.sin(k * .7 + seed * 2)
        rim_pts.append((x + math.cos(a) * rx * wav, y + math.sin(a) * ry * wav))
    rim_d = "M" + "L".join(f"{f(a)} {f(b)}" for a, b in rim_pts) + "Z"
    under = f"M{f(x - rx)} {f(y)}Q{f(x - rx * .6)} {f(y + ry * 2.6)} {f(x)} {f(y + ry * 2.4)}Q{f(x + rx * .6)} {f(y + ry * 2.6)} {f(x + rx)} {f(y)}Z"
    g_under = s.lin([(0, mix(dark, light, .3), 1), (1, dark, 1)], 0, 0, 0, 1)
    g_in = s.rad([(0, mix(light, dark, .45), 1), (0.7, light, 1), (1, mix(light, "#ffffff", .15), 1)], x, y, rx, user=True,
                 transform=f"translate(0 {f(y * (1 - ry / rx))}) scale(1 {f(ry / rx)})")
    veins = "".join(f"M{f(x)} {f(y)}L{f(x + math.cos(a) * rx * .9)} {f(y + math.sin(a) * ry * .9)}" for a in [k * .42 for k in range(15)])
    s.add(f'<path d="{under}" fill="{g_under}"/><path d="{rim_d}" fill="{g_in}"/>'
          f'<path d="{veins}" stroke="{dark}" stroke-opacity=".3" stroke-width="{f(1.2 * sc)}"/>'
          f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(4 * sc)}" fill="{dark}" opacity=".5"/>'
          f'<path d="{rim_d}" stroke="{rim}" stroke-opacity=".55" stroke-width="{f(1.6 * sc)}" fill="none"/>')


def om_gold(s, cx, cy, scale, glow=True, halo=None):
    """The Om sign in burnished, glowing gold, optionally inside a faint mandala halo."""
    if halo:
        rings = []
        R = 150 * scale
        for k, r in enumerate((R, R * 1.18, R * 1.42)):
            rings.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="none" stroke="{halo}" stroke-opacity="{.35 - k * .08:.2f}" stroke-width="{f(1.2 + k * .2)}"/>')
        for k in range(24):
            a = 2 * math.pi * k / 24
            px, py = cx + math.cos(a) * R * 1.3, cy + math.sin(a) * R * 1.3
            rings.append(f'<path d="{_petal(R * .16, R * .2)}" transform="translate({f(cx + math.cos(a) * R * 1.2)} {f(cy + math.sin(a) * R * 1.2)}) rotate({math.degrees(a) + 90:.1f})" fill="none" stroke="{halo}" stroke-opacity=".22" stroke-width="1.2"/>')
            rings.append(f'<circle cx="{f(px + math.cos(a) * R * .17)}" cy="{f(py + math.sin(a) * R * .17)}" r="{f(1.6 * scale)}" fill="{halo}" opacity=".5"/>')
        s.add(f'<g style="mix-blend-mode:screen">{"".join(rings)}</g>')
    t = f"translate({f(cx)} {f(cy)}) scale({scale}) translate(-240 -152)"
    gold = s.lin([(0, "#fff6d2"), (0.35, "#f7d27a"), (0.7, "#d99a35"), (1, "#a5641d")], 0, 0, 0.3, 1)
    if glow:
        s.add(f'<g transform="{t}" filter="{s.blur(26 / scale)}" opacity=".9" style="mix-blend-mode:screen"><path d="{OM}" fill="#ffb347"/></g>')
        s.add(f'<g transform="{t}" filter="{s.blur(8 / scale)}" opacity=".8" style="mix-blend-mode:screen"><path d="{OM}" fill="#ffe2a0"/></g>')
    s.add(f'<g transform="{t}" filter="{s.gold_filter(4 / scale * 2)}"><path d="{OM}" fill="{gold}"/></g>')


def reflect_since(s, start, axis_y, opacity=0.4, blur=2.0, depth=200):
    """Mirror everything drawn since mark() below the line axis_y (for things floating on water)."""
    inner = "".join(s.body[start:])
    del s.body[start:]
    m = s.mask_fade(-200, axis_y, 2000, depth, 1, 0)
    s.add(f'<g mask="{m}" opacity="{opacity}"><g transform="translate(0 {f(2 * axis_y)}) scale(1 -1)" filter="{s.blur(blur)}">{inner}</g></g>{inner}')


# ---------- shrine still lifes ----------
BRASS = [(0, "#3a2408"), (0.18, "#7a5218"), (0.42, "#d9a440"), (0.5, "#fff0b8"), (0.58, "#e2ae4a"), (0.8, "#8a5c1c"), (1, "#2e1c06")]


def stone_wall(s, color="#3a2a26", light=(800, 600), light_color="#ff9a4a", light_r=900, blocks=True, seed=3):
    """A warm, lamp-lit temple wall of dressed stone."""
    W_, H_ = 1600, 1000
    s.add(f'<rect width="{W_}" height="{H_}" fill="{color}"/>')
    s.add(f'<rect width="{W_}" height="{H_}" fill="{color}" filter="{s.grain(0.012, 4, .5, seed, "#000000")}"/>')
    s.add(f'<rect width="{W_}" height="{H_}" fill="{color}" filter="{s.grain(0.6, 3, .18, seed + 1, "#ffffff")}"/>')
    if blocks:
        rng = random.Random(seed)
        d = []
        y = 0
        row = 0
        while y < H_:
            h = rng.uniform(90, 120)
            d.append(f"M0 {f(y)}H{W_}")
            x = rng.uniform(-150, 0) if row % 2 else rng.uniform(-60, 0)
            while x < W_:
                d.append(f"M{f(x)} {f(y)}V{f(y + h)}")
                x += rng.uniform(200, 320)
            y += h
            row += 1
        s.add(f'<path d="{"".join(d)}" stroke="#000" stroke-opacity=".35" stroke-width="3" filter="{s.blur(1)}"/>'
              f'<path d="{"".join(d)}" stroke="#ffd9b0" stroke-opacity=".05" stroke-width="1.2" transform="translate(1.5 1.5)"/>')
    lx, ly = light
    s.add(f'<rect width="{W_}" height="{H_}" fill="{s.rad([(0, light_color, .55), (0.35, light_color, .22), (1, light_color, 0)], lx, ly, light_r, user=True)}" style="mix-blend-mode:screen"/>')
    s.add(f'<rect width="{W_}" height="{H_}" fill="{s.rad([(0, "#000", 0), (0.6, "#000", .25), (1, "#000", .7)], lx, ly, light_r * 1.2, user=True)}"/>')


def arch_niche(s, cx, top, w, bottom, recess="#160d0c", carve="#8a5a3a", light=(800, 700), light_color="#ffb060", lobed=True):
    """A carved, cusped arch cut into the wall, with a dark recess and a border of lotus petals."""
    r = w / 2
    spring = top + r * 1.1
    if lobed:
        d = (f"M{f(cx - r)} {f(bottom)}V{f(spring)}"
             f"C{f(cx - r)} {f(spring - r * .5)} {f(cx - r * .7)} {f(spring - r * .62)} {f(cx - r * .62)} {f(spring - r * .72)}"
             f"C{f(cx - r * .7)} {f(spring - r * .95)} {f(cx - r * .4)} {f(top + r * .12)} {f(cx - r * .2)} {f(top + r * .14)}"
             f"C{f(cx - r * .14)} {f(top)} {f(cx)} {f(top - r * .08)} {f(cx)} {f(top - r * .2)}"
             f"C{f(cx)} {f(top - r * .08)} {f(cx + r * .14)} {f(top)} {f(cx + r * .2)} {f(top + r * .14)}"
             f"C{f(cx + r * .4)} {f(top + r * .12)} {f(cx + r * .7)} {f(spring - r * .95)} {f(cx + r * .62)} {f(spring - r * .72)}"
             f"C{f(cx + r * .7)} {f(spring - r * .62)} {f(cx + r)} {f(spring - r * .5)} {f(cx + r)} {f(spring)}V{f(bottom)}Z")
    else:
        d = f"M{f(cx - r)} {f(bottom)}V{f(spring)}A{f(r)} {f(r)} 0 0 1 {f(cx + r)} {f(spring)}V{f(bottom)}Z"
    # carved frame: offset outline drawn thick, then motifs along it
    s.add(f'<path d="{d}" fill="none" stroke="#000" stroke-opacity=".5" stroke-width="64" filter="{s.blur(6)}"/>')
    s.add(f'<path d="{d}" fill="none" stroke="{carve}" stroke-width="54" filter="{s.gold_filter(3, "#ffd8a8", 250, 38, .6, 14)}"/>')
    s.add(f'<path d="{d}" fill="none" stroke="#000" stroke-opacity=".45" stroke-width="2" stroke-dasharray="2 9" transform="translate(0 0)"/>')
    s.add(f'<path d="{d}" fill="none" stroke="{mix(carve, "#000000", .45)}" stroke-width="30" stroke-dasharray="1 13" stroke-linecap="round"/>')
    s.add(f'<path d="{d}" fill="none" stroke="{mix(carve, "#ffffff", .2)}" stroke-width="8"/>')
    g = s.rad([(0, mix(recess, light_color, .35), 1), (0.5, recess, 1), (1, mix(recess, "#000000", .5), 1)], light[0], light[1], w * 1.1, user=True)
    s.add(f'<path d="{d}" fill="{g}"/>')
    s.add(f'<g clip-path="{s.clip(d)}"><path d="{d}" fill="none" stroke="#000" stroke-opacity=".7" stroke-width="40" filter="{s.blur(14)}"/></g>')
    return d


def ledge(s, y, x0=-20, x1=1620, color="#4a3228", edge="#ffcf9a", depth=60):
    """A stone shelf: a lit front edge with its top surface receding into shadow."""
    top = s.lin([(0, mix(color, "#000000", .5), 1), (1, color, 1)], 0, y - depth, 0, y, user=True)
    front = s.lin([(0, mix(color, edge, .25), 1), (0.15, color, 1), (1, mix(color, "#000000", .6), 1)], 0, y, 0, 1000, user=True)
    s.add(f'<path d="M{x0} {f(y)}L{x0 + 30} {f(y - depth)}H{x1 - 30}L{x1} {f(y)}Z" fill="{top}"/>'
          f'<rect x="{x0}" y="{f(y)}" width="{x1 - x0}" height="{f(1000 - y)}" fill="{front}"/>'
          f'<path d="M{x0} {f(y)}H{x1}" stroke="{edge}" stroke-opacity=".45" stroke-width="2"/>')


def marigold(cx, cy, r, color="#f39a1c", seed=1, light=(0, -1)):
    """A ruffled marigold head (SVG string)."""
    rng = random.Random(seed)
    dark = mix(color, "#7a2c00", .45)
    hi = mix(color, "#fff0a0", .45)
    out = [f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="{dark}"/>']
    for ring, rr, cnt in ((0, r * .8, 14), (1, r * .52, 10), (2, r * .26, 6)):
        for k in range(cnt):
            a = 2 * math.pi * k / cnt + rng.uniform(-.2, .2) + ring
            px, py = cx + math.cos(a) * rr, cy + math.sin(a) * rr * .9
            lit = max(0, -(math.cos(a) * light[0] + math.sin(a) * light[1]))
            c = mix(color, hi, lit * .7) if ring < 2 else hi
            out.append(f'<circle cx="{f(px)}" cy="{f(py)}" r="{f(r * (.34 - ring * .06))}" fill="{c}"/>')
    return "".join(out)


def garland(s, x0, y0, x1, y1, sag, r=14, colors=("#f39a1c", "#f7c02a"), seed=1, tassel=True):
    """A marigold garland hanging in a catenary between two points."""
    rng = random.Random(seed)
    L = math.hypot(x1 - x0, y1 - y0)
    n = int(L / (r * 1.25))
    out = [f'<path d="M{f(x0)} {f(y0)}Q{f((x0 + x1) / 2)} {f((y0 + y1) / 2 + sag * 2)} {f(x1)} {f(y1)}" stroke="#2a1006" stroke-width="{f(r * 1.6)}" fill="none" opacity=".5" filter="{s.blur(r * .5)}" transform="translate(4 {f(r * .6)})"/>']
    for k in range(n + 1):
        t = k / n
        x = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * (x0 + x1) / 2 + t * t * x1
        y = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * ((y0 + y1) / 2 + sag * 2) + t * t * y1
        c = colors[(k // 3) % len(colors)]
        out.append(marigold(x, y, r * rng.uniform(.92, 1.08), c, seed * 100 + k))
    s.add("".join(out))
    if tassel:
        for (x, y) in ((x0, y0), (x1, y1)):
            s.add("".join(marigold(x, y + 12 + k * r * 1.3, r * .85, colors[k % 2], seed + k) for k in range(5)))


def petals_scatter(s, x0, x1, y0, y1, n, colors=("#f39a1c", "#e8562a", "#f7c02a", "#c91e3a"), seed=1, size=(5, 10)):
    rng = random.Random(seed)
    out = []
    for _ in range(n):
        x, y, r = rng.uniform(x0, x1), rng.uniform(y0, y1), rng.uniform(*size)
        a = rng.uniform(0, 180)
        c = rng.choice(colors)
        out.append(f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(r)}" ry="{f(r * .45)}" fill="{c}" transform="rotate({a:.0f} {f(x)} {f(y)})"/>'
                   f'<ellipse cx="{f(x)}" cy="{f(y - r * .1)}" rx="{f(r * .5)}" ry="{f(r * .18)}" fill="#fff4c0" opacity=".3" transform="rotate({a:.0f} {f(x)} {f(y)})"/>')
    s.add("".join(out))


def clay_diya(s, cx, cy, sc=1.0, flame_h=None, glow=True, clay="#b0481e", dots=True):
    """A terracotta oil lamp, painted with dots and lit by its own flame; (cx, cy) is the rim centre."""
    w = 110 * sc
    body = s.lin([(0, mix(clay, "#ffb070", .3), 1), (0.4, clay, 1), (1, mix(clay, "#000000", .75), 1)], 0, 0, 0, 1)
    side = s.lin([(0, "#000", .65), (0.3, "#000", .2), (0.62, "#000", 0), (0.82, "#ffcf80", .25), (1, "#000", .3)], 0, 0, 1, 0)
    s.add(f'<ellipse cx="{f(cx)}" cy="{f(cy + 66 * sc)}" rx="{f(w * 1.2)}" ry="{f(12 * sc)}" fill="#000" opacity=".55" filter="{s.blur(8 * sc)}"/>')
    bowl = (f"M{f(cx - w)} {f(cy)}C{f(cx - w * .92)} {f(cy + 50 * sc)} {f(cx - w * .5)} {f(cy + 64 * sc)} {f(cx)} {f(cy + 64 * sc)}"
            f"C{f(cx + w * .5)} {f(cy + 64 * sc)} {f(cx + w * .92)} {f(cy + 50 * sc)} {f(cx + w)} {f(cy)}Z")
    spout = f"M{f(cx + w * .62)} {f(cy - 2 * sc)}C{f(cx + w * .9)} {f(cy - 8 * sc)} {f(cx + w * 1.2)} {f(cy - 22 * sc)} {f(cx + w * 1.34)} {f(cy - 26 * sc)}C{f(cx + w * 1.24)} {f(cy - 6 * sc)} {f(cx + w * 1.04)} {f(cy + 14 * sc)} {f(cx + w * .8)} {f(cy + 20 * sc)}Z"
    s.add(f'<path d="{spout}" fill="{body}"/><path d="{bowl}" fill="{body}"/><path d="{bowl}" fill="{side}"/>')
    if dots:
        rng = random.Random(7)
        band = []
        for k in range(23):
            t = (k + .5) / 23
            a = math.pi * t
            x = cx - math.cos(a) * w * .9
            y = cy + 18 * sc + math.sin(a) * 6 * sc
            band.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(3.2 * sc)}" fill="{"#f6e7c8" if k % 2 else "#f2b232"}" opacity="{.35 + .55 * t:.2f}"/>')
            if k % 2 == 0:
                band.append(f'<circle cx="{f(x)}" cy="{f(y + 11 * sc)}" r="{f(2 * sc)}" fill="#f6e7c8" opacity="{.3 + .5 * t:.2f}"/>')
        s.add("".join(band))
    s.add(f'<ellipse cx="{f(cx)}" cy="{f(cy)}" rx="{f(w)}" ry="{f(18 * sc)}" fill="{s.lin([(0, mix(clay, "#ffd0a0", .5), 1), (1, mix(clay, "#3a1408", .3), 1)], 0, 0, 1, 0)}"/>'
          f'<ellipse cx="{f(cx)}" cy="{f(cy + 2 * sc)}" rx="{f(w * .88)}" ry="{f(13 * sc)}" fill="#2a1206"/>'
          f'<ellipse cx="{f(cx + 4 * sc)}" cy="{f(cy + 4 * sc)}" rx="{f(w * .78)}" ry="{f(9 * sc)}" fill="{s.lin([(0, "#e8a63a", .9), (1, "#7a3a10", .9)], 0, 0, 1, 0)}"/>'
          f'<ellipse cx="{f(cx + w * .3)}" cy="{f(cy + 3 * sc)}" rx="{f(w * .2)}" ry="{f(3 * sc)}" fill="#fff2c0" opacity=".6"/>'
          f'<path d="M{f(cx + w * .2)} {f(cy + 2 * sc)}Q{f(cx + w * .8)} {f(cy - 6 * sc)} {f(cx + w * 1.22)} {f(cy - 20 * sc)}" stroke="#f3e6c8" stroke-width="{f(4 * sc)}" fill="none" stroke-linecap="round"/>'
          f'<path d="M{f(cx + w * 1.18)} {f(cy - 20 * sc)}l{f(8 * sc)} {f(-4 * sc)}" stroke="#2a1206" stroke-width="{f(4 * sc)}" stroke-linecap="round"/>')
    fh = flame_h or 120 * sc
    s.flame(cx + w * 1.26, cy - 22 * sc, fh, glow=glow, glow_r=fh * 6)
    return (cx + w * 1.26, cy - 22 * sc - fh * .45)


def brass_lamp(s, cx, base, sc=1.0, flames=5, flame_h=None):
    """A standing brass oil lamp (samai) with one or five wicks; base is where it stands."""
    g = s.lin(BRASS, 0, 0, 1, 0)
    sh = s.lin([(0, "#000", 0), (0.7, "#000", 0), (1, "#000", .5)], 0, 0, 0, 1)
    t = f"translate({f(cx)} {f(base)}) scale({f(sc)})"
    parts = ("M-90 0C-90 -14 -60 -22 0 -22C60 -22 90 -14 90 0Z"
             "M-50 -20C-50 -34 -20 -40 0 -40C20 -40 50 -34 50 -20Z"
             "M-12 -38H12L9 -120H-9Z"
             "M-26 -120C-26 -132 26 -132 26 -120C26 -110 -26 -110 -26 -120Z"
             "M-8 -130H8L7 -200H-7Z"
             "M-20 -200C-20 -212 20 -212 20 -200C20 -190 -20 -190 -20 -200Z"
             "M-8 -208H8L7 -232H-7Z"
             "M-96 -236C-96 -262 96 -262 96 -236C82 -214 -82 -214 -96 -236Z")
    s.add(f'<ellipse cx="{f(cx)}" cy="{f(base + 4 * sc)}" rx="{f(130 * sc)}" ry="{f(14 * sc)}" fill="#000" opacity=".6" filter="{s.blur(8 * sc)}"/>')
    s.add(f'<g transform="{t}"><path d="{parts}" fill="{g}"/><path d="{parts}" fill="{sh}"/>'
          f'<ellipse cx="0" cy="-246" rx="92" ry="11" fill="#3a2408"/><ellipse cx="0" cy="-244" rx="84" ry="7" fill="#c8862a" opacity=".7"/>'
          f'<path d="M-90 -238C-40 -232 40 -232 90 -238" stroke="#fff3c4" stroke-opacity=".6" stroke-width="2" fill="none"/>'
          f'<path d="M-4 -258C-6 -274 6 -274 4 -258Z M0 -276C-10 -290 0 -310 0 -320C0 -310 10 -290 0 -276Z" fill="{g}"/></g>')
    fh = flame_h or 70 * sc
    pos = [(0, -250)] if flames == 1 else [(-80, -246), (-40, -250), (40, -250), (80, -246), (0, -252)]
    for k, (fx_, fy) in enumerate(pos):
        s.add(f'<path d="M{f(cx + fx_ * sc - 6 * sc)} {f(base + fy * sc + 2 * sc)}l{f(6 * sc)} {f(-8 * sc)}l{f(6 * sc)} {f(8 * sc)}Z" fill="#3a2408"/>')
        s.flame(cx + fx_ * sc, base + (fy - 6) * sc, fh, glow_r=fh * 4.5, glow_a=.45 if flames > 1 else .55)


def dark_room(s, light=(800, 560), base="#120906", warm="#5a2a12", r=1100, horizon=720, floor="#1a0d08"):
    """A dim, warm interior for close-up still lifes: lamp-lit air above a polished floor."""
    s.add(f'<rect width="1600" height="1000" fill="{base}"/>')
    s.add(f'<rect width="1600" height="1000" fill="{s.rad([(0, warm, 1), (0.45, mix(warm, base, .6), 1), (1, base, 1)], light[0], light[1], r, user=True)}"/>')
    s.add(f'<rect y="{horizon}" width="1600" height="{1000 - horizon}" fill="{s.lin([(0, mix(floor, warm, .5), 1), (1, floor, 1)], 0, horizon, 0, 1000, user=True)}"/>')


def bells(s, xs, y0, color="#c8902e", blur=7, sc=1.0, seed=1):
    """Out-of-focus temple bells hanging from chains in the background."""
    rng = random.Random(seed)
    out = []
    for x in xs:
        L = rng.uniform(120, 260) * sc
        y = y0 + L
        b = 34 * sc * rng.uniform(.8, 1.2)
        out.append(f'<path d="M{f(x)} {f(y0)}V{f(y - b)}" stroke="{color}" stroke-width="{f(3 * sc)}" stroke-dasharray="{f(6 * sc)} {f(3 * sc)}"/>'
                   f'<path d="M{f(x - b * .2)} {f(y - b)}C{f(x - b * .5)} {f(y - b * .8)} {f(x - b * .55)} {f(y - b * .2)} {f(x - b * .8)} {f(y)}H{f(x + b * .8)}'
                   f'C{f(x + b * .55)} {f(y - b * .2)} {f(x + b * .5)} {f(y - b * .8)} {f(x + b * .2)} {f(y - b)}Z" fill="{s.lin(BRASS, 0, 0, 1, 0)}"/>')
    s.add(f'<g filter="{s.blur(blur)}" opacity=".75">{"".join(out)}</g>')
