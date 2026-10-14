"""Architecture: temples, shrines, pavilions, river ghats and boats, mostly as
rim-lit silhouettes. Shapes are drawn in local units and placed with a transform."""
import math
import random

from paint import f, mix, pts_d


def _g(x, y, sc, inner, flip=False):
    sx = -sc if flip else sc
    return f'<g transform="translate({f(x)} {f(y)}) scale({f(sx)} {f(sc)})">{inner}</g>'


def flag(x, y, w, h, color="#f07a1e", wave=0.25, seed=1):
    """A triangular temple pennant flying to the right from a pole top at (x, y)."""
    rng = random.Random(seed)
    k = wave * h
    return (f'<path d="M{f(x)} {f(y)}C{f(x + w * .3)} {f(y - k)} {f(x + w * .6)} {f(y + k * rng.uniform(.4, 1))} {f(x + w)} {f(y + h * .35)}'
            f'C{f(x + w * .62)} {f(y + h * .5 + k * .4)} {f(x + w * .3)} {f(y + h * .62)} {f(x)} {f(y + h)}Z" fill="{color}"/>')


def nagara(s, x, base, sc=1.0, color="#1a1626", rim=None, light=1, door="#ffb45c", flag_color="#ef7a22",
           shade=None, bands=True, mandapa=True, glow=True):
    """A North Indian (Nagara) stone temple in side elevation: a curving shikhara tower over
    the sanctum, smaller attached spires, an amalaka and kalasha, a pillared hall with a
    stepped pyramid roof, and a flag. light=1 lights the right-hand edges."""
    tower = "M-48 -62C-50 -128 -34 -198 -12 -226H12C34 -198 50 -128 48 -62Z"
    mini_l = "M-62 -62C-63 -102 -52 -134 -41 -146H-33C-24 -134 -17 -108 -15 -62Z"
    mini_r = "M62 -62C63 -102 52 -134 41 -146H33C24 -134 17 -108 15 -62Z"
    mini_amalaka = '<ellipse cx="-37" cy="-149" rx="10" ry="3.6"/><ellipse cx="37" cy="-149" rx="10" ry="3.6"/>'
    top = ('<ellipse cx="0" cy="-232" rx="21" ry="7"/><rect x="-7" y="-241" width="14" height="6"/>'
           '<path d="M-8 -243C-10 -251 -5 -256 0 -256C5 -256 10 -251 8 -243Z"/><path d="M-2 -256L0 -266L2 -256Z"/>')
    sanctum = "M-54 0V-62H54V0Z"
    plinth = "M-138 0V-8H86V0ZM-130 -8V-16H80V-8Z"
    hall = ""
    if mandapa:
        tiers = []
        for k in range(6):
            y0 = -58 - k * 11
            hw = 44 - k * 6.5
            tiers.append(f"M{f(-88 - hw - 3)} {f(y0)}L{f(-88 - hw + 2)} {f(y0 - 9)}H{f(-88 + hw - 2)}L{f(-88 + hw + 3)} {f(y0)}Z")
        hall = ("M-126 -16V-54H-50V-16Z" + "".join(tiers) +
                "M-96 -124C-97 -130 -92 -134 -88 -134C-84 -134 -79 -130 -80 -124Z")
    shape = tower + mini_l + mini_r + sanctum + plinth + hall
    inner = [f'<g fill="{color}"><path d="{shape}"/>{mini_amalaka}{top}</g>']
    inner.append(f'<path d="M0 -266V-312" stroke="{color}" stroke-width="2.2"/>')
    inner.append(flag(0, -312, 46, 22, flag_color, seed=3))

    clip_d = tower + mini_l + mini_r + sanctum + hall
    cid = s.clip(clip_d)
    if shade:
        sg = s.lin([(0, shade, 0), (0.5, shade, 0.0), (1, shade, 0.55)], -140, 0, 70, 0, user=True) if light > 0 else \
            s.lin([(0, shade, 0.55), (0.5, shade, 0.0), (1, shade, 0)], -140, 0, 70, 0, user=True)
        inner.append(f'<g clip-path="{cid}"><rect x="-140" y="-270" width="210" height="270" fill="{sg}"/></g>')
    if bands:
        lines = "".join(f"M-70 {y}H70" for y in range(-74, -222, -11))
        inner.append(f'<g clip-path="{s.clip(tower + mini_l + mini_r)}"><path d="{lines}" stroke="#000" stroke-opacity=".28" stroke-width="2.2"/>'
                     f'<path d="M0 -70V-226" stroke="#000" stroke-opacity=".18" stroke-width="10"/></g>')
    if rim:
        if light > 0:
            edges = "M48 -62C50 -128 34 -198 12 -226M62 -62C63 -102 52 -134 41 -146M54 0V-62M86 -8V0"
            if mandapa:
                edges += "M-50 -16V-54" + "".join(f"M{f(-88 + 44 - k * 6.5 - 2)} {f(-58 - k * 11 - 9)}L{f(-88 + 44 - k * 6.5 + 3)} {f(-58 - k * 11)}" for k in range(6))
        else:
            edges = "M-48 -62C-50 -128 -34 -198 -12 -226M-62 -62C-63 -102 -52 -134 -41 -146M-54 0V-62"
            if mandapa:
                edges += "M-126 -16V-54" + "".join(f"M{f(-88 - 44 + k * 6.5 + 2)} {f(-58 - k * 11 - 9)}L{f(-88 - 44 + k * 6.5 - 3)} {f(-58 - k * 11)}" for k in range(6))
        inner.append(f'<path d="{edges}" stroke="{rim}" stroke-width="2.4" fill="none" opacity=".85" stroke-linecap="round"/>'
                     f'<ellipse cx="{8 * light}" cy="-234" rx="12" ry="3" fill="{rim}" opacity=".7"/>')
    if door:
        dg = s.lin([(0, "#fff1c4", 1), (0.5, door, 1), (1, "#b2441c", 1)], 0, -48, 0, -16, user=True)
        inner.append(f'<path d="M-97 -16V-38C-97 -46 -79 -46 -79 -38V-16Z" fill="{dg}"/>' if mandapa else
                     f'<path d="M-10 -8V-40C-10 -50 10 -50 10 -40V-8Z" fill="{dg}"/>')
        if glow:
            gx = -88 if mandapa else 0
            inner.append(f'<ellipse cx="{gx}" cy="-24" rx="70" ry="40" fill="{s.rad([(0, door, .45), (1, door, 0)])}" style="mix-blend-mode:screen"/>')
    s.add(_g(x, base, sc, "".join(inner)))


def shikhara_front(s, x, base, sc=1.0, color="#1a1626", rim=None, light=1, flag_color="#ef7a22", tiers=True, door=None):
    """A temple tower seen from the front, as in a Varanasi skyline."""
    tower = "M-40 -50C-42 -112 -28 -176 -10 -200H10C28 -176 42 -112 40 -50Z"
    sides = "M-56 -50C-57 -86 -48 -114 -38 -124H-30C-22 -112 -16 -90 -15 -50ZM56 -50C57 -86 48 -114 38 -124H30C22 -112 16 -90 15 -50Z"
    top = ('<ellipse cx="0" cy="-205" rx="18" ry="6"/><rect x="-6" y="-213" width="12" height="6"/>'
           '<path d="M-7 -214C-9 -221 -4 -226 0 -226C4 -226 9 -221 7 -214Z"/><path d="M-2 -226L0 -234L2 -226Z"/>'
           '<ellipse cx="-34" cy="-127" rx="8" ry="3"/><ellipse cx="34" cy="-127" rx="8" ry="3"/>')
    body = "M-62 0V-50H62V0ZM-68 -50H68L64 -56H-64Z"
    inner = [f'<g fill="{color}"><path d="{tower + sides + body}"/>{top}</g>',
             f'<path d="M0 -234V-270" stroke="{color}" stroke-width="2"/>', flag(0, -270, 40, 18, flag_color, seed=5)]
    if tiers:
        lines = "".join(f"M-60 {y}H60" for y in range(-60, -198, -10))
        inner.append(f'<g clip-path="{s.clip(tower + sides)}"><path d="{lines}" stroke="#000" stroke-opacity=".25" stroke-width="2"/></g>')
    if rim:
        e = "M40 -50C42 -112 28 -176 10 -200M56 -50C57 -86 48 -114 38 -124M62 0V-50" if light > 0 else \
            "M-40 -50C-42 -112 -28 -176 -10 -200M-56 -50C-57 -86 -48 -114 -38 -124M-62 0V-50"
        inner.append(f'<path d="{e}" stroke="{rim}" stroke-width="2.2" fill="none" opacity=".85"/>')
    if door:
        inner.append(f'<path d="M-9 0V-28C-9 -36 9 -36 9 -28V0Z" fill="{door}"/>')
    s.add(_g(x, base, sc, "".join(inner)))


def chhatri(s, x, base, sc=1.0, color="#1a1626", rim=None, light=1, open_=True):
    """A domed pavilion on four pillars; the gaps between pillars stay open to the sky."""
    pillars = "M-30 -8V-46H-24V-8ZM-12 -8V-46H-6V-8ZM6 -8V-46H12V-8ZM24 -8V-46H30V-8Z" if open_ else "M-30 -8V-46H30V-8Z"
    shape = ("M-38 0V-8H38V0Z" + pillars + "M-38 -46H38L34 -54H-34Z"
             "M-28 -54C-30 -74 -14 -86 0 -88C14 -86 30 -74 28 -54Z"
             "M-3 -88L0 -100L3 -88Z")
    inner = [f'<path d="{shape}" fill="{color}"/>', f'<circle cx="0" cy="-90" r="3" fill="{color}"/>']
    if rim:
        e = "M28 -54C30 -74 14 -86 0 -88M38 -46L34 -54" if light > 0 else "M-28 -54C-30 -74 -14 -86 0 -88M-38 -46L-34 -54"
        inner.append(f'<path d="{e}" stroke="{rim}" stroke-width="2" fill="none" opacity=".85"/>')
    s.add(_g(x, base, sc, "".join(inner)))


def building(s, x, base, w, h, color="#1a1626", rim=None, light=1, windows=None, seed=1, parapet=True, domes=0,
             balcony=True, win_color="#ffc070", win_a=0.9, storey=30, tone=0.0):
    """A riverside house or palace face: storeys of arched windows (some lit), cornices,
    a setback upper floor, a jharokha balcony and rooftop domes or pavilions."""
    rng = random.Random(seed)
    if tone:
        color = mix(color, "#ffffff" if tone > 0 else "#000000", abs(tone))
    d = [f"M{f(x)} {f(base)}V{f(base - h)}H{f(x + w)}V{f(base)}Z"]
    top = base - h
    upper = None
    if h > storey * 2.5 and rng.random() < .55:
        uw = w * rng.uniform(.45, .75)
        ux = x + rng.uniform(0, w - uw)
        uh = storey * rng.choice([1, 1, 2])
        d.append(f"M{f(ux)} {f(top)}V{f(top - uh)}H{f(ux + uw)}V{f(top)}Z")
        upper = (ux, uw, top - uh)
    roof_x, roof_w, roof_y = upper or (x, w, top)
    if parapet:
        d.append(f"M{f(roof_x - 2)} {f(roof_y)}V{f(roof_y - 4)}H{f(roof_x + roof_w + 2)}V{f(roof_y)}Z")
    for _ in range(domes):
        cx = roof_x + rng.choice([0.15, 0.85, 0.5]) * roof_w
        r = min(roof_w * .16, 15)
        if rng.random() < .5:
            d.append(f"M{f(cx - r)} {f(roof_y)}C{f(cx - r)} {f(roof_y - r * 1.3)} {f(cx)} {f(roof_y - r * 1.5)} {f(cx)} {f(roof_y - r * 1.9)}"
                     f"C{f(cx)} {f(roof_y - r * 1.5)} {f(cx + r)} {f(roof_y - r * 1.3)} {f(cx + r)} {f(roof_y)}Z")
        else:
            d.append(f"M{f(cx - r)} {f(roof_y)}V{f(roof_y - r * 1.2)}H{f(cx - r * .7)}V{f(roof_y)}ZM{f(cx + r * .7)} {f(roof_y)}V{f(roof_y - r * 1.2)}H{f(cx + r)}V{f(roof_y)}Z"
                     f"M{f(cx - r * 1.2)} {f(roof_y - r * 1.2)}H{f(cx + r * 1.2)}L{f(cx + r)} {f(roof_y - r * 1.45)}H{f(cx - r)}Z"
                     f"M{f(cx - r * .9)} {f(roof_y - r * 1.45)}C{f(cx - r * .9)} {f(roof_y - r * 2.3)} {f(cx + r * .9)} {f(roof_y - r * 2.3)} {f(cx + r * .9)} {f(roof_y - r * 1.45)}Z")
    if balcony and w > 46 and h > storey * 2:
        bx = x + w * rng.uniform(.3, .7)
        by = base - storey * rng.randint(1, max(1, int(h / storey) - 1))
        d.append(f"M{f(bx - 15)} {f(by)}H{f(bx + 15)}L{f(bx + 10)} {f(by + 7)}H{f(bx - 10)}Z"
                 f"M{f(bx - 13)} {f(by)}V{f(by - 19)}H{f(bx + 13)}V{f(by)}Z"
                 f"M{f(bx - 16)} {f(by - 19)}C{f(bx - 12)} {f(by - 31)} {f(bx + 12)} {f(by - 31)} {f(bx + 16)} {f(by - 19)}Z")
    out = [f'<path d="{"".join(d)}" fill="{color}"/>']
    dark, wins, lines = [], [], []
    rows = max(1, int(h // storey))
    cols = max(1, int(w // 18))
    for r in range(rows):
        wy = base - (r + 1) * storey + 8
        lines.append(f"M{f(x)} {f(base - r * storey - storey + 1)}H{f(x + w)}")
        for c in range(cols):
            wx = x + (c + .5) * w / cols
            ww, wh = 5, storey * .42
            p = f"M{f(wx - ww / 2)} {f(wy + wh)}V{f(wy + 2)}Q{f(wx)} {f(wy - 3)} {f(wx + ww / 2)} {f(wy + 2)}V{f(wy + wh)}Z"
            if rng.random() < (windows if windows is not None else 0.2):
                wins.append(f'<path d="{p}" fill="{win_color}" opacity="{rng.uniform(.5, 1) * win_a:.2f}"/>')
            else:
                dark.append(p)
    if dark:
        out.append(f'<path d="{"".join(dark)}" fill="#000" opacity=".22"/>')
    out.append(f'<path d="{"".join(lines)}" stroke="#000" stroke-opacity=".18" stroke-width="1.5"/>')
    if wins:
        out.append("".join(wins))
    if rim:
        ex = x + w if light > 0 else x
        out.append(f'<path d="M{f(ex)} {f(base)}V{f(base - h)}" stroke="{rim}" stroke-width="1.6" opacity=".6"/>'
                   f'<path d="M{f(roof_x - 2)} {f(roof_y - 4)}H{f(roof_x + roof_w + 2)}" stroke="{rim}" stroke-width="1.2" opacity=".5"/>')
    s.add("".join(out))


def steps(s, x0, x1, y_top, y_bottom, n, color="#1d1726", edge="#6b4c52", edge_a=0.5):
    """A flight of ghat steps descending to the water."""
    out = [f'<rect x="{f(x0)}" y="{f(y_top)}" width="{f(x1 - x0)}" height="{f(y_bottom - y_top)}" fill="{color}"/>']
    lines = "".join(f"M{f(x0)} {f(y_top + (y_bottom - y_top) * k / n)}H{f(x1)}" for k in range(n + 1))
    out.append(f'<path d="{lines}" stroke="{edge}" stroke-opacity="{edge_a}" stroke-width="1.4"/>')
    s.add("".join(out))


def umbrella(s, x, base, sc=1.0, color="#16121c", rim=None):
    """The bamboo parasol and wooden platform of a Varanasi ghat."""
    canopy = "M-46 -78C-30 -92 30 -92 46 -78L44 -76C36 -74 32 -78 28 -75C20 -73 14 -77 8 -74C0 -72 -6 -76 -12 -74C-20 -72 -26 -77 -32 -75C-38 -73 -42 -77 -46 -78Z"
    inner = [f'<path d="M-1 -90V-12M-26 -12H26V-6H-26ZM-22 -6V0M22 -6V0" stroke="{color}" stroke-width="2.4" fill="{color}"/>',
             f'<path d="{canopy}" fill="{color}"/><circle cx="0" cy="-92" r="2.4" fill="{color}"/>']
    if rim:
        inner.append(f'<path d="M0 -90C14 -90 34 -86 46 -78" stroke="{rim}" stroke-width="1.6" fill="none" opacity=".75"/>')
    s.add(_g(x, base, sc, "".join(inner)))


def boat(s, x, y, sc=1.0, color="#120e16", rim=None, flip=False, people=0, rower=True):
    """A wooden river boat with upswept ends; (x, y) is the waterline centre."""
    hull = "M-120 -18C-100 -6 -60 0 0 0C60 0 100 -6 126 -22L118 -10C96 6 60 12 0 12C-60 12 -96 6 -114 -6Z"
    inner = [f'<path d="{hull}" fill="{color}"/>', f'<path d="M-90 -6H96" stroke="{color}" stroke-width="5"/>']
    for k in range(people):
        px = -60 + k * 34
        inner.append(f'<g fill="{color}"><circle cx="{px}" cy="-30" r="5.4"/><path d="M{px - 9} -2C{px - 10} -14 {px - 7} -24 {px} -24C{px + 7} -24 {px + 10} -14 {px + 9} -2Z"/></g>')
    if rower:
        inner.append(f'<g fill="{color}" stroke="{color}" stroke-linecap="round"><circle cx="86" cy="-64" r="5"/>'
                     f'<path d="M80 -58H92L93 -30L90 -4H82L79 -30Z" stroke="none"/>'
                     f'<path d="M91 -54L102 -44M81 -54L96 -40" stroke-width="3.2"/><path d="M110 -68L80 26" stroke-width="2.2"/></g>')
    if rim:
        inner.append(f'<path d="M-120 -18C-100 -6 -60 0 0 0C60 0 100 -6 126 -22" stroke="{rim}" stroke-width="1.6" fill="none" opacity=".7"/>')
    s.add(_g(x, y, sc, "".join(inner), flip))


def deepastambha(s, x, base, sc=1.0, color="#1a1626", lamps=True, rim=None):
    """A stone lamp pillar with rings of small flames."""
    shaft = "M-9 0V-150H9V0ZM-18 0V-10H18V0ZM-14 -10V-16H14V-10Z"
    arms = "".join(f"M-{22 - k * 2.5} {-30 - k * 26}H{22 - k * 2.5}V{-26 - k * 26}H-{22 - k * 2.5}Z" for k in range(5))
    top = "M-6 -150L0 -164L6 -150Z"
    s.add(_g(x, base, sc, f'<path d="{shaft + arms + top}" fill="{color}"/>' +
             (f'<path d="M9 0V-150" stroke="{rim}" stroke-width="1.6" opacity=".7"/>' if rim else "")))
    if lamps:
        for k in range(5):
            half = 22 - k * 2.5
            for t in (-1, -.5, 0, .5, 1):
                fx_ = x + t * half * sc
                fy = base + (-30 - k * 26) * sc
                s.flame(fx_, fy, 9 * sc, glow_r=40 * sc, glow_a=.35)


def rocks(s, x0, x1, ground_fn, n, size=(10, 40), color="#120f1c", rim=None, seed=1, light=1):
    """Scattered boulders sitting on a ground line."""
    rng = random.Random(seed)
    out, rims = [], []
    for _ in range(n):
        x = rng.uniform(x0, x1)
        g = ground_fn(x)
        w = rng.uniform(*size)
        h = w * rng.uniform(.45, .8)
        k = rng.uniform(-.2, .2)
        out.append(f"M{f(x - w)} {f(g + 4)}C{f(x - w)} {f(g - h * .7)} {f(x - w * .4 + k * w)} {f(g - h)} {f(x + k * w)} {f(g - h)}"
                   f"C{f(x + w * .5)} {f(g - h)} {f(x + w)} {f(g - h * .5)} {f(x + w)} {f(g + 4)}Z")
        if rim:
            rims.append(f"M{f(x + k * w)} {f(g - h)}C{f(x + w * .5)} {f(g - h)} {f(x + w)} {f(g - h * .5)} {f(x + w)} {f(g)}" if light > 0 else
                        f"M{f(x + k * w)} {f(g - h)}C{f(x - w * .4 + k * w)} {f(g - h)} {f(x - w)} {f(g - h * .7)} {f(x - w)} {f(g)}")
    s.add(f'<path d="{"".join(out)}" fill="{color}"/>' + (f'<path d="{"".join(rims)}" stroke="{rim}" stroke-width="1.5" fill="none" opacity=".7"/>' if rims else ""))


def skyline(s, x0, x1, base, h=(60, 160), color="#2a1d33", rim=None, light=1, seed=1, windows=0.2, temples=(),
            chhatris=(), win_color="#ffc070", gap=(0, 6), parapet=True, storey=30):
    """A packed riverside skyline of houses and palaces, with temple towers (x, scale)
    and pavilions (x, scale) rising among them."""
    rng = random.Random(seed)
    x = x0
    while x < x1:
        w = rng.uniform(40, 120)
        hh = rng.uniform(*h)
        building(s, x, base, w, hh, color, rim, light, windows, seed=rng.randint(0, 9999), parapet=parapet,
                 domes=rng.choice([0, 0, 1, 2]), balcony=rng.random() < .5, win_color=win_color,
                 tone=rng.uniform(-.12, .1), storey=storey)
        x += w + rng.uniform(*gap)
    for tx, sc in temples:
        shikhara_front(s, tx, base - rng.uniform(20, 50) * sc, sc, color, rim, light, tiers=True)
    for cx, sc in chhatris:
        chhatri(s, cx, base - h[1] * rng.uniform(.5, .9), sc, color, rim, light)


def leaf_lamp(s, cx, cy, sc=1.0, seed=1):
    """A leaf-bowl lamp with marigolds floating on the river."""
    rng = random.Random(seed)
    s.add(f'<ellipse cx="{f(cx)}" cy="{f(cy + 3 * sc)}" rx="{f(30 * sc)}" ry="{f(5 * sc)}" fill="#ffb060" opacity=".35" filter="{s.blur(max(1, 3 * sc))}" style="mix-blend-mode:screen"/>')
    s.add(f'<path d="M{f(cx - 22 * sc)} {f(cy - 2 * sc)}C{f(cx - 16 * sc)} {f(cy + 8 * sc)} {f(cx + 16 * sc)} {f(cy + 8 * sc)} {f(cx + 22 * sc)} {f(cy - 2 * sc)}'
          f'C{f(cx + 10 * sc)} {f(cy + 1 * sc)} {f(cx - 10 * sc)} {f(cy + 1 * sc)} {f(cx - 22 * sc)} {f(cy - 2 * sc)}Z" fill="#3a2a18"/>')
    for k in range(4):
        px = cx + (k - 1.5) * 9 * sc + rng.uniform(-2, 2) * sc
        col = rng.choice(["#f59a1b", "#f7b52a", "#e8562a"])
        s.add(f'<circle cx="{f(px)}" cy="{f(cy - 2 * sc)}" r="{f(3.6 * sc)}" fill="{col}"/>')
    s.flame(cx + rng.uniform(-3, 3) * sc, cy - 4 * sc, 18 * sc, glow_r=70 * sc, glow_a=.5)
