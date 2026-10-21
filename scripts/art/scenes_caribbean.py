"""Indo-Caribbean paintings: jhandi flags in a yard at sunrise, Ramleela on a village field at
night, the Kartik bath in the sea at dawn and the women's Matikor procession."""
import math
import random

import objects as ob
from land import crown, ridgeline, hills, smooth_line
from paint import H, W, f, mix
from scenes import scene
from scenes_festive import person, fire, J_BOTH_UP, J_THROW_UP, joint
from scenes_land import palm


# ======================================================================
# helpers
# ======================================================================
def bamboo(s, x, base, h, lean=0.0, w=7, color="#c8a46a", shade="#7a5a32", light=None):
    """A bamboo pole with its nodes; returns the top (x, y)."""
    tx, ty = x + lean * h, base - h
    s.add(f'<path d="M{f(x - w / 2)} {f(base)}L{f(tx - w * .3)} {f(ty)}L{f(tx + w * .3)} {f(ty)}L{f(x + w / 2)} {f(base)}Z" fill="{color}"/>')
    s.add(f'<path d="M{f(x + w * .15)} {f(base)}L{f(tx + w * .12)} {f(ty)}L{f(tx + w * .3)} {f(ty)}L{f(x + w / 2)} {f(base)}Z" fill="{shade}" opacity=".55"/>')
    if light:
        s.add(f'<path d="M{f(x - w / 2)} {f(base)}L{f(tx - w * .3)} {f(ty)}" stroke="{light}" stroke-width="1.6" opacity=".7"/>')
    n = max(3, int(h / 70))
    for k in range(1, n):
        t = k / n
        nx, ny = x + (tx - x) * t, base + (ty - base) * t
        s.add(f'<path d="M{f(nx - w * .62)} {f(ny)}L{f(nx + w * .62)} {f(ny)}" stroke="{shade}" stroke-width="2.2" opacity=".8"/>')
    return tx, ty


def cloth_flag(s, x, y, w, h, color, seed=1, wave=.18, light=None, shape="rect", glow=0.0):
    """A cloth flag hanging from (x, y) on a pole and fluttering to the right."""
    rng = random.Random(seed)
    pts_top, pts_bot = [], []
    n = 10
    ph = rng.uniform(0, 6)
    for i in range(n + 1):
        t = i / n
        dy = math.sin(t * 5.2 + ph) * h * wave * t
        sag = t * t * h * .18
        pts_top.append((x + t * w, y + dy + sag))
        bh = h * (1 - t * .55) if shape == "tri" else h * (1 - t * .08)
        pts_bot.append((x + t * w * (1 - (.04 if shape == "rect" else 0)), y + dy + sag + bh))
    if shape == "tri":
        pts_bot[-1] = pts_top[-1]
    d = "M" + "L".join(f"{f(a)} {f(b)}" for a, b in pts_top) + "L" + "L".join(f"{f(a)} {f(b)}" for a, b in reversed(pts_bot)) + "Z"
    dark = mix(color, "#000000", .45)
    g = s.lin([(0, dark, 1), (.35, color, 1), (.7, mix(color, "#ffffff", .25), 1), (1, color, 1)], x, y, x + w, y, user=True)
    if glow:
        s.add(f'<path d="{d}" fill="{color}" opacity="{glow}" filter="{s.blur(14)}"/>')
    s.add(f'<path d="{d}" fill="{g}"/>')
    # folds catching the light
    folds = []
    for k in range(3):
        t = .25 + k * .25
        i = int(t * n)
        folds.append(f'<path d="M{f(pts_top[i][0])} {f(pts_top[i][1])}L{f(pts_bot[i][0])} {f(pts_bot[i][1])}" stroke="{light or "#ffffff"}" stroke-width="{f(w * .05)}" opacity=".14" filter="{s.blur(3)}"/>')
    s.add(f'<g clip-path="{s.clip(d)}">{"".join(folds)}</g>')


def walker(stride, arm=0.0, head=0.0):
    """Joints (feet at y = 0, facing right) for a walking figure; stride -1..1, arm swing."""
    return dict(head=(2 + head, -92), neck=(1, -84), ls=(-8, -80), rs=(8, -80), lh=(-6, -50), rh=(6, -50),
                le=(-10 - 6 * arm, -66), lw=(-12 - 10 * arm, -52), re=(10 + 6 * arm, -66), rw=(13 + 10 * arm, -52),
                lk=(-4 - 7 * stride, -25), lf=(-8 - 12 * stride, 0), rk=(5 + 7 * stride, -25), rf=(9 + 12 * stride, 0))


J_CARRY = dict(head=(1, -92), neck=(0, -84), ls=(-8, -80), rs=(8, -80), lh=(-6, -50), rh=(6, -50),
               le=(-14, -96), lw=(-6, -106), re=(15, -95), rw=(7, -106),
               lk=(-5, -25), lf=(-11, 0), rk=(6, -25), rf=(11, 0))
J_LAMP = dict(head=(3, -92), neck=(1, -84), ls=(-8, -80), rs=(8, -80), lh=(-6, -50), rh=(6, -50),
              le=(-8, -64), lw=(4, -60), re=(18, -68), rw=(26, -66),
              lk=(-6, -25), lf=(-13, 0), rk=(6, -25), rf=(12, 0))
J_DRUM = dict(head=(2, -92), neck=(1, -84), ls=(-9, -80), rs=(9, -80), lh=(-7, -50), rh=(7, -50),
              le=(-18, -70), lw=(-8, -62), re=(20, -76), rw=(16, -88),
              lk=(-7, -25), lf=(-12, 0), rk=(7, -25), rf=(12, 0))
J_ARGHYA = dict(head=(2, -93), neck=(1, -85), ls=(-8, -81), rs=(8, -81), lh=(-6, -50), rh=(6, -50),
                le=(2, -96), lw=(12, -108), re=(16, -96), rw=(16, -110),
                lk=(-5, -25), lf=(-8, 0), rk=(5, -25), rf=(8, 0))
J_FOLDED = dict(head=(1, -92), neck=(0, -84), ls=(-8, -80), rs=(8, -80), lh=(-6, -50), rh=(6, -50),
                le=(-9, -64), lw=(1, -76), re=(10, -64), rw=(2, -76),
                lk=(-5, -25), lf=(-8, 0), rk=(5, -25), rf=(8, 0))


# ======================================================================
# 1. Jhandi: prayer flags raised in the yard at sunrise
# ======================================================================
@scene
def jhandi(s):
    sun = (1060, 470)
    s.sky([(0, "#2c4f8e"), (.22, "#5d7fbc"), (.42, "#b9a7c8"), (.55, "#f6c49a"), (.62, "#ffe2b4")], 0, 1000)
    s.sun(*sun, 40, core="#fffdf4", rim="#fff0c8", halo="#ffd29a", halo_r=700, halo_a=.75)
    s.fx("clouds", y0=40, y1=430, seed=71, cell=160, aniso=3.2, cover=.4, soft=.18, lit="#ffe6c8", body=.8, direct=1.0,
         light=(.2, 1), sun=(sun[0], sun[1], 420), rim="#fff4e0", opacity=.85)
    hz = 640
    far = ridgeline(hz, 22, 33, cell=220, octaves=5, ridged=.2)
    hills(s, far, "#8a7fa0", "#a898b4")
    rng = random.Random(7)
    cr = "".join(crown(x, hz - rng.uniform(4, 16), rng.uniform(10, 22), seed=x) for x in range(-20, 1640, 24))
    s.add(f'<path d="{cr}" fill="#6f6688"/>')
    s.mist(hz - 4, 50, "#ffe6cc", .55, 16)
    # palms and a house on stilts, against the light
    s.add(palm(170, hz + 40, 430, seed=3, lean=.12, color="#3a2a3a"))
    s.add(palm(260, hz + 60, 330, seed=5, lean=-.08, color="#33243a"))
    s.add(palm(1460, hz + 50, 470, seed=9, lean=-.14, color="#3a2a3a"))
    hx, hy = 1180, hz + 24
    house = (f'<g fill="#3c2c3e"><path d="M{hx - 150} {hy - 150}L{hx} {hy - 230}L{hx + 160} {hy - 150}L{hx + 160} {hy - 60}L{hx - 150} {hy - 60}Z"/>'
             + "".join(f'<rect x="{hx - 140 + k * 70}" y="{hy - 60}" width="9" height="62"/>' for k in range(5)) + '</g>'
             f'<rect x="{hx - 100}" y="{hy - 132}" width="38" height="40" fill="#ffd28a" opacity=".85"/>'
             f'<rect x="{hx + 60}" y="{hy - 132}" width="38" height="40" fill="#ffc87a" opacity=".7"/>')
    s.add(house)
    s.mist(hz + 30, 60, "#ffe0c0", .3, 20)
    gg = s.lin([(0, "#7a8a4a", 1), (.3, "#5a6a32", 1), (1, "#2a3218", 1)], 0, hz + 40, 0, 1000, user=True)
    s.add(f'<path d="M0 {hz + 50}Q800 {hz + 20} 1600 {hz + 46}V1000H0Z" fill="{gg}"/>')
    s.add(f'<path d="M0 {hz + 50}Q800 {hz + 20} 1600 {hz + 46}V1000H0Z" fill="#4a5a2a" filter="{s.grain(.05, 3, .2, 4, "#1a2208")}"/>')
    # the jhandis: bamboo poles with flags, the newest red one for Hanuman in front
    flags = [  # x, base, height, lean, colour, flag w, h, shape
        (520, 880, 610, .03, "#f2efe4", 120, 82, "rect"),
        (610, 860, 520, -.02, "#f2c21c", 110, 74, "rect"),
        (700, 900, 700, .0, "#d81e1e", 150, 104, "tri"),
        (790, 870, 560, .04, "#e86a14", 120, 80, "rect"),
        (880, 885, 640, -.03, "#2a5ad8", 120, 82, "rect"),
        (450, 905, 470, -.05, "#d81e1e", 100, 70, "rect"),
        (965, 895, 520, .06, "#f2efe4", 110, 74, "tri"),
    ]
    for i, (x, base, h, lean, col, fw, fh, shp) in enumerate(flags):
        tx, ty = bamboo(s, x, base, h, lean, w=8 + h / 160, light="#ffe2b0")
        cloth_flag(s, tx, ty + 6, fw, fh, col, seed=i + 3, light="#fff4d8", shape=shp, glow=.25)
    # marigolds and a small diya at the foot of the poles
    for x in (560, 680, 760, 860):
        s.add(ob.marigold(x, 902 + (x % 3) * 4, 13, seed=x))
    ob.clay_diya(s, 720, 930, sc=.42)
    ob.petals_scatter(s, 420, 1020, 900, 960, 40, seed=5, size=(3, 6))
    s.fx("godrays", cx=sun[0], cy=sun[1], strength=.35, thresh=.8, decay=.97, radius=260)
    s.fx("mottle", amp=.035, cell=60)
    s.look = {"vibrance": .12, "vignette": .28}
    return s


# ======================================================================
# 2. Ramleela: Ravan burns on the village field
# ======================================================================
def ravan(s, cx, base, h, color="#1c1220", rim="#ff9a4a"):
    """The effigy: a tall robed figure, arms out, ten crowned heads in a row."""
    w = h * .26
    body = (f"M{f(cx - w * .55)} {f(base)}L{f(cx - w * .32)} {f(base - h * .55)}L{f(cx - w * .7)} {f(base - h * .62)}"
            f"L{f(cx - w * .72)} {f(base - h * .68)}L{f(cx - w * .2)} {f(base - h * .74)}L{f(cx + w * .2)} {f(base - h * .74)}"
            f"L{f(cx + w * .72)} {f(base - h * .68)}L{f(cx + w * .7)} {f(base - h * .62)}L{f(cx + w * .32)} {f(base - h * .55)}"
            f"L{f(cx + w * .55)} {f(base)}Z")
    heads = []
    hy = base - h * .82
    for k in range(10):
        t = k - 4.5
        x = cx + t * w * .19
        y = hy - (1 - (t / 5) ** 2) * h * .04
        r = w * .09
        heads.append(f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(r)}" ry="{f(r * 1.25)}"/>'
                     f'<path d="M{f(x - r)} {f(y - r * .9)}L{f(x - r * .6)} {f(y - r * 2.1)}L{f(x)} {f(y - r * 1.4)}L{f(x + r * .6)} {f(y - r * 2.1)}L{f(x + r)} {f(y - r * .9)}Z"/>')
    neck = f'<rect x="{f(cx - w * .14)}" y="{f(base - h * .78)}" width="{f(w * .28)}" height="{f(h * .06)}"/>'
    sword = f'<path d="M{f(cx + w * .72)} {f(base - h * .66)}L{f(cx + w * .95)} {f(base - h * .98)}L{f(cx + w * .99)} {f(base - h * .97)}L{f(cx + w * .76)} {f(base - h * .65)}Z"/>'
    shape = f'<path d="{body}"/>{neck}{"".join(heads)}{sword}'
    s.add(f'<g fill="{rim}" transform="translate(3 -2)" opacity=".8">{shape}</g>')
    s.add(f'<g fill="{color}">{shape}</g>')
    # painted trim on the robe
    s.add(f'<path d="M{f(cx - w * .4)} {f(base - h * .3)}L{f(cx + w * .4)} {f(base - h * .3)}M{f(cx - w * .36)} {f(base - h * .45)}L{f(cx + w * .36)} {f(base - h * .45)}" '
          f'stroke="#c8902e" stroke-width="5" opacity=".6"/>')


@scene
def ramleela(s):
    s.sky([(0, "#070a1e"), (.3, "#15183a"), (.55, "#2a2250"), (.7, "#4a2a4a"), (.78, "#7a3a3a")], 0, 1000)
    s.stars(160, 0, 520, seed=12, bright=.8)
    s.moon(300, 170, 34, crescent=.0, glow_r=260)
    hz = 720
    rng = random.Random(3)
    tree_line = "".join(crown(x, hz - rng.uniform(20, 60), rng.uniform(26, 46), seed=x) for x in range(-30, 1660, 40))
    s.add(f'<path d="{tree_line}" fill="#120c1a"/>')
    s.add(palm(120, hz + 10, 380, seed=4, lean=.1, color="#0e0a14"))
    s.add(palm(1500, hz + 10, 420, seed=8, lean=-.12, color="#0e0a14"))
    s.add(f'<rect y="{hz - 10}" width="{W}" height="{H - hz + 10}" fill="#1a1016"/>')
    # the effigy, and the fire taking hold of it
    cx, base = 800, 760
    s.glow(cx, base - 200, 900, "#ff6a1a", .55, .2)
    ravan(s, cx, base, 560)
    fire(s, cx, base + 6, 300, 260, n=18, seed=5)
    fire(s, cx - 40, base - 200, 120, 140, n=9, seed=8, smoke=False)
    fire(s, cx + 70, base - 300, 90, 110, n=7, seed=11, smoke=False)
    s.smoke(cx, base - 520, 380, color="#c8a898", a=.25, seed=3, width=3.2, drift=.25)
    # the flaming arrow that lit it
    path = smooth_line([(160, 620), (420, 420), (700, 380)], step=8)
    d = "M" + "L".join(f"{f(x)} {f(y)}" for x, y in path)
    s.add(f'<path d="{d}" stroke="#ffcf7a" stroke-width="3" fill="none" opacity=".55" filter="{s.blur(2)}"/>')
    s.add(f'<path d="{d}" stroke="#fff0c8" stroke-width="1.2" fill="none" opacity=".8"/>')
    s.flame(702, 380, 26, lean=.6, glow_r=90)
    # lit stage at the side
    # a string of bulbs over the field
    bulbs = smooth_line([(980, hz - 150), (1200, hz - 110), (1480, hz - 160)], step=24)
    s.add(f'<path d="M{" L".join(f"{f(a)} {f(b)}" for a, b in bulbs)}" stroke="#3a2a2a" stroke-width="2" fill="none"/>')
    s.add("".join(f'<circle cx="{f(a)}" cy="{f(b + 6)}" r="5" fill="#ffe0a0"/>' for a, b in bulbs))
    s.add(f'<g filter="{s.blur(8)}">' + "".join(f'<circle cx="{f(a)}" cy="{f(b + 6)}" r="14" fill="#ffb060" opacity=".5"/>' for a, b in bulbs) + "</g>")
    s.fx("haze", y0=hz - 200, y1=hz + 40, color="#ff8a4a", a0=0, a1=.18)
    # the crowd watching, lit from the fire
    crowd = []
    for i in range(16):
        x = 140 + i * 88 + rng.uniform(-20, 20)
        if 640 < x < 960:
            continue
        crowd.append((x, 1000 + rng.uniform(-30, 10), rng.uniform(2.6, 3.2)))
    for i, (x, y, sc) in enumerate(crowd):
        J = J_BOTH_UP if i % 5 == 2 else walker(0, 0)
        flip = x > cx
        person(s, x, y, sc, J, "#0c0810", "#ff8a3a", rim_dx=-1.4 if flip else 1.4, flip=flip,
               skirt=(-20, 20, 0, 3) if i % 2 else None, kurta=None if i % 2 else (-14, 14, -28, 1), hair="bun" if i % 2 else None)
    s.fx("mottle", amp=.03, cell=60)
    s.look = {"vibrance": .1, "vignette": .34, "bloom": .5}
    return s


# ======================================================================
# 3. Kartik nahan: the dawn bath in the sea
# ======================================================================
@scene
def kartik_snan(s):
    sun = (860, 548)
    hz = 560
    s.sky([(0, "#2a2a5e"), (.2, "#5a4a86"), (.36, "#b07a9a"), (.48, "#f4a888"), (.56, "#ffd8a8")], 0, hz)
    s.sun(*sun, 46, core="#fffbee", rim="#ffe0b0", halo="#ffb07a", halo_r=620, halo_a=.8)
    s.fx("clouds", y0=60, y1=470, seed=91, cell=150, aniso=4, cover=.36, soft=.2, lit="#ffc8a8", body=.75, direct=.9,
         light=(0, 1), sun=(sun[0], sun[1], 400), rim="#fff0e0", opacity=.85)
    s.fx("sea", y0=hz, deep="#2e2a54", sky="#9a7aa8", sky_far="#ffcfae", crest="#e8c8c8", foam="#fff4ec", seed=37, cell=26,
         aniso=2.2, chop=.7, foam_amt=.18, light=(sun[0], hz + 20), light_c="#ffc890", light_r=240, light_a=.45, gloss=.85)
    s.fx("glints", y0=hz, cx=sun[0], color="#fff0d0", width=80, strength=1.1, scatter=.1, density=.55, spread=2.2)
    # floating diyas
    for i, (x, y) in enumerate([(560, 742), (650, 790), (1040, 760), (1120, 812), (480, 830), (940, 856)]):
        ob.clay_diya(s, x, y, sc=.2 + (y - 700) / 900)
    # bathers standing in the water: waist-deep figures, the near one offering water to the sun
    water = 700
    bathers = [(700, 4.4, J_ARGHYA, False, True), (1010, 3.9, J_FOLDED, True, False), (430, 3.4, J_FOLDED, False, False),
               (1250, 3.2, J_ARGHYA, True, False)]
    for x, sc, J, flip, lota in bathers:
        wl = water + (sc - 3.2) * 60
        y = wl - J["lh"][1] * sc + 2 * sc        # the hips at the waterline
        clipd = f"M0 0H{W}V{f(wl)}H0Z"
        g0 = s.mark()
        person(s, x, y, sc, J, "#2a1a2e", "#ffd8a8", rim_dx=1.6 if x < sun[0] else -1.6, flip=flip,
               hair="bun" if J is J_FOLDED else None, dupatta=None)
        if lota:
            hx, hy = joint(x, y, sc, J, "lw", flip)
            s.add(f'<ellipse cx="{f(hx + 4)}" cy="{f(hy - 8)}" rx="16" ry="13" fill="#c87a3a"/><rect x="{f(hx - 6)}" y="{f(hy - 24)}" width="20" height="8" rx="3" fill="#e8a05a"/>')
            stream = smooth_line([(hx + 14, hy - 4), (hx + 30, hy + 30), (hx + 34, wl)], step=6)
            sd = "M" + "L".join(f"{f(a)} {f(b)}" for a, b in stream)
            s.add(f'<path d="{sd}" stroke="#fff2d8" stroke-width="4" fill="none" opacity=".85" filter="{s.blur(1)}"/>')
        inner = "".join(s.body[g0:])
        del s.body[g0:]
        s.add(f'<g clip-path="{s.clip(clipd)}">{inner}</g>')
        s.add(f'<ellipse cx="{f(x)}" cy="{f(wl)}" rx="{f(16 * sc)}" ry="{f(2.6 * sc)}" fill="none" stroke="#ffe8c8" stroke-width="2" opacity=".55" filter="{s.blur(1)}"/>')
    # the shore, with jhandi flags planted after the puja
    beach = s.lin([(0, "#d8b08a", 1), (1, "#8a6244", 1)], 0, 900, 0, 1000, user=True)
    s.add(f'<path d="M0 880Q500 910 900 940T1600 930V1000H0Z" fill="{beach}"/>')
    s.add(f'<path d="M0 880Q500 910 900 940T1600 930" stroke="#fff6ec" stroke-width="5" fill="none" opacity=".6" filter="{s.blur(2)}"/>')
    for i, (x, base, h, col) in enumerate([(150, 960, 420, "#d81e1e"), (215, 955, 360, "#f2efe4"), (270, 965, 300, "#f2c21c")]):
        tx, ty = bamboo(s, x, base, h, .02 * (i - 1), w=7, light="#ffd8b0")
        cloth_flag(s, tx, ty + 4, 90, 60, col, seed=20 + i, light="#fff4d8")
    s.fx("godrays", cx=sun[0], cy=sun[1], strength=.3, thresh=.85, decay=.97, radius=240)
    s.fx("mottle", amp=.03, cell=60)
    s.look = {"vibrance": .12, "vignette": .26}
    return s


# ======================================================================
# 4. Matikor: the women go out to bless the earth before the wedding
# ======================================================================
@scene
def matikor(s):
    s.sky([(0, "#0c0c26"), (.3, "#1e1a44"), (.5, "#3a2a5a"), (.62, "#6a3a5a")], 0, 1000)
    s.stars(120, 0, 420, seed=22, bright=.7)
    s.moon(1320, 160, 30, glow_r=220)
    hz = 640
    rng = random.Random(9)
    s.add(f'<path d="{"".join(crown(x, hz - rng.uniform(30, 80), rng.uniform(40, 70), seed=x) for x in range(-40, 1680, 60))}" fill="#140e1e"/>')
    s.add(palm(1480, hz + 20, 440, seed=2, lean=-.1, color="#100a18"))
    s.add(palm(90, hz + 30, 380, seed=6, lean=.12, color="#100a18"))
    s.add(f'<rect y="{hz - 6}" width="{W}" height="{H - hz + 6}" fill="#1e1418"/>')
    s.add(f'<rect y="{hz - 6}" width="{W}" height="{H - hz + 6}" fill="#2a1a16" filter="{s.grain(.04, 3, .25, 8, "#4a2a18")}"/>')
    # lamplight from the procession
    lamp = (600, 760)
    s.glow(lamp[0] + 80, lamp[1], 900, "#ff9a3a", .5, .18)
    s.glow(lamp[0], lamp[1], 300, "#ffd28a", .6, .3)
    # the women, walking left to right: lamp-bearer, the bride's mother with the basket on her head,
    # then the others singing, and a tassa drummer behind
    col, rim = "#140c16", "#ffb46a"
    people = [
        (1040, 905, 2.7, J_LAMP, dict(skirt=(-24, 24, 0, 3), hair="bun", dupatta=[(-6, -82), (-16, -60), (-20, -30)])),
        (860, 915, 2.9, J_CARRY, dict(skirt=(-26, 26, 0, 4), hair=None, dupatta=[(-4, -90), (-14, -66), (-18, -36)])),
        (700, 908, 2.75, walker(.5, .4), dict(skirt=(-25, 24, 0, 3), hair="bun", dupatta=[(-6, -84), (-16, -58), (-20, -28)])),
        (560, 900, 2.6, walker(-.4, -.3), dict(skirt=(-24, 22, 0, 3), hair="bun")),
        (420, 896, 2.5, walker(.3, .5), dict(skirt=(-23, 22, 0, 3), hair="bun", dupatta=[(-6, -84), (-14, -60), (-18, -30)])),
        (260, 902, 2.7, J_DRUM, dict(kurta=(-15, 15, -30, 1), hair=None, sticks=[("rw", -150, 22), ("lw", -40, 22)])),
    ]
    for x, y, sc, J, kw in people:
        person(s, x, y, sc, J, col, rim, rim_dx=1.5, shadow=(.25, .25), **kw)
    # the lamp in the lead woman's hand
    lx, ly = joint(1040, 905, 2.7, J_LAMP, "rw")
    ob.clay_diya(s, lx + 6, ly - 4, sc=.28)
    # the flat basket (soop) with earth, flowers and a lamp, on the mother's head
    bx, by = joint(860, 915, 2.9, J_CARRY, "lw")
    s.add(f'<ellipse cx="{f(bx + 4)}" cy="{f(by - 6)}" rx="58" ry="12" fill="#a87a3a"/><ellipse cx="{f(bx + 4)}" cy="{f(by - 10)}" rx="48" ry="8" fill="#6a4a2a"/>')
    for k in range(5):
        s.add(ob.marigold(bx - 30 + k * 15, by - 16 - (k % 2) * 4, 8, seed=40 + k))
    ob.clay_diya(s, bx + 8, by - 22, sc=.22)
    # the tassa drum slung at the drummer's waist
    dx, dy = joint(260, 902, 2.7, J_DRUM, "rh")
    dx, dy = dx + 30, dy - 40
    s.add(f'<path d="M{f(dx - 34)} {f(dy - 30)}L{f(dx - 34)} {f(dy + 30)}Q{f(dx)} {f(dy + 44)} {f(dx + 34)} {f(dy + 30)}L{f(dx + 34)} {f(dy - 30)}Z" fill="#7a4a24"/>'
          f'<ellipse cx="{f(dx)}" cy="{f(dy - 30)}" rx="34" ry="11" fill="#e8d0a0"/>'
          f'<path d="M{f(dx - 34)} {f(dy - 30)}L{f(dx + 34)} {f(dy + 30)}M{f(dx + 34)} {f(dy - 30)}L{f(dx - 34)} {f(dy + 30)}" stroke="#d8b06a" stroke-width="2" opacity=".7"/>')
    # the patch of earth dug for the puja, with the first lamp and sindoor
    ex, ey = 1240, 930
    s.add(f'<ellipse cx="{ex}" cy="{ey}" rx="120" ry="26" fill="#5a3418"/><ellipse cx="{ex}" cy="{ey - 4}" rx="90" ry="16" fill="#3a1e0e"/>')
    s.add(f'<path d="M{ex - 150} {ey + 8}Q{ex - 120} {ey - 30} {ex - 80} {ey - 6}Z" fill="#7a4a24"/>')
    ob.clay_diya(s, ex + 70, ey - 12, sc=.34)
    s.add(f'<circle cx="{ex - 20}" cy="{ey - 8}" r="9" fill="#e8201e"/><circle cx="{ex + 10}" cy="{ey - 6}" r="9" fill="#f2b81a"/>')
    ob.petals_scatter(s, 1120, 1360, 900, 960, 30, seed=7, size=(3, 6))
    s.motes(60, 300, 1300, 600, 900, color="#ffd8a0", seed=4)
    s.fx("mottle", amp=.03, cell=60)
    s.look = {"vibrance": .1, "vignette": .3, "bloom": .4}
    return s
