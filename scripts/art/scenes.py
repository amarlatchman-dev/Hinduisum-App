"""Scene compositions for the lesson and rite paintings."""
import random

import arch
import objects as ob
import figures as fig
from glyphs import OM
from land import crown, grass, hills, round_tree, mountains, peak_line, pine, pines, ribbon, ridgeline, smooth_line, y_at
from paint import H, W, Scene, f, mix

SCENES = {}


def scene(fn):
    SCENES[fn.__name__.replace("_", "-")] = lambda: fn(Scene(seed=sum(map(ord, fn.__name__))))
    return fn


def om_gold(s, cx, cy, scale, glow=True):
    """The Om sign in burnished, glowing gold."""
    t = f"translate({f(cx)} {f(cy)}) scale({scale}) translate(-240 -152)"
    gold = s.lin([(0, "#fff6d2"), (0.35, "#f7d27a"), (0.7, "#d99a35"), (1, "#a5641d")], 0, 0, 0.3, 1)
    if glow:
        s.add(f'<g transform="{t}" filter="{s.blur(26 / scale)}" opacity=".9"><path d="{OM}" fill="#ffb347"/></g>')
        s.add(f'<g transform="{t}" filter="{s.blur(8 / scale)}" opacity=".8"><path d="{OM}" fill="#ffe2a0"/></g>')
    s.add(f'<g transform="{t}" filter="{s.gold_filter(4 / scale * 2)}"><path d="{OM}" fill="{gold}"/></g>')


@scene
def pilgrim(s):
    sun = (1180, 505)
    s.sky([(0, "#11163a"), (.2, "#262b5e"), (.4, "#5a4f88"), (.52, "#a9799f"), (.6, "#e9a99a"), (.68, "#ffcfa8"), (1, "#ffe6c2")])
    s.stars(50, 0, 240, seed=3, bright=.55)
    s.sun(*sun, 30, halo_r=560, halo_a=.75)
    s.fx("clouds", y0=20, y1=330, seed=4, cell=140, aniso=3, cover=.42, soft=.16, lit="#f3b3a6", body=.75, direct=.72,
         light=(0.5, 1), sun=(sun[0], sun[1], 420), opacity=.95)
    s.fx("clouds", y0=280, y1=540, seed=14, cell=100, aniso=3.5, cover=.36, soft=.18, lit="#ffd3ae", body=.8, direct=.9,
         light=(0.3, 1), sun=(sun[0], sun[1], 360), opacity=.9)
    far = peak_line(650, [(-30, 230, 240), (270, 300, 280, .15), (560, 240, 200), (830, 410, 330, -.1),
                          (1430, 300, 280, .1), (1650, 240, 220)], 21, shape=1.3, floor=70, shoulders=2)
    mountains(s, far, "#7f78b0", "#b08fb4", lit="#f2b7a8", lit_a=.8, light=1, seed=5, snow="#bdb3df",
              snow_shade="#9a8fc4", lit_snow="#fff0e6", snowline=470, snow_fingers=60, rim="#fff2dc", rim_center=sun,
              rim_r=520, haze="#efc6c0", haze_a=.45, haze_h=150, base_y=660)
    s.mist(648, 110, "#f6d4cc", .45, 30)
    mid = peak_line(780, [(80, 230, 260), (430, 180, 220, .2), (760, 120, 220), (1050, 150, 200), (1420, 230, 280, -.1)],
                    22, shape=1.15, detail=.18)
    mountains(s, mid, "#4f4580", "#7e6496", lit="#e99c92", lit_a=.75, light=1, seed=6, snow="#b5a9d3",
              snow_shade="#8c7fb6", lit_snow="#ffe1d6", snowline=640, snow_fingers=40, rim="#ffe2c6", rim_center=sun,
              rim_r=600, haze="#d9a9b4", haze_a=.45, haze_h=140, base_y=780)
    s.mist(775, 110, "#f0c8c4", .42, 28)
    near = ridgeline(880, 170, 23, cell=240, octaves=6, ridged=.35, envelope=[(0, .9), (700, .5), (1600, 1)])
    hills(s, near, "#2f2850", "#4c3a61", rim="#ffd2ac", rim_a=.9, rim_center=sun, rim_r=700, haze="#c995a6", haze_a=.35)
    pines(s, -20, W + 20, 0, 80, h=(26, 64), color="#251f40", seed=7, ground_fn=lambda x: y_at(near, x))
    s.mist(890, 100, "#e7b8b6", .35, 26)
    # the knoll with the temple, and the path climbing to it
    fg = smooth_line([(-60, 640), (160, 628), (420, 650), (640, 720), (900, 860), (1200, 930), (1660, 960)], 8)
    hills(s, fg, "#1d1832", "#0b0914", rim="#ffcf9e", rim_a=.95, rim_center=sun, rim_r=1300)
    s.glow(300, 660, 340, "#ff9a50", .22, .2, sy=.45)
    path = smooth_line([(1150, 1010), (1010, 950), (880, 905), (780, 855), (680, 790), (560, 722), (430, 676), (330, 656)], 5)
    s.add(f'<path d="{ribbon(path, 70, 10)}" fill="{s.lin([(0, "#5d4250", 1), (1, "#2a2033", 1)], 0, 640, 0, 1000, user=True)}" opacity=".8"/>')
    treads = []
    for k in range(8, len(path) - 4, 4):
        (x, y), (x2, y2) = path[k], path[k + 1]
        w = (70 + (10 - 70) * k / (len(path) - 1)) / 2 * .85
        treads.append(f"M{f(x - w)} {f(y)}L{f(x + w)} {f(y - (x2 - x) * .05)}")
    s.add(f'<path d="{"".join(treads)}" stroke="#8a6062" stroke-opacity=".35" stroke-width="1.6"/>')
    grass(s, -40, 700, lambda x: y_at(fg, x) + 2, 260, h=(6, 22), color="#1d1832", seed=3)
    grass(s, 700, 1700, lambda x: y_at(fg, x) + 2, 200, h=(8, 26), color="#1a152d", seed=4)
    s.glow(560, 760, 520, "#ff9c55", .16, .25, sy=.35)
    arch.deepastambha(s, 470, 676, .8, color="#1f1830", rim="#ffcf9e")
    arch.nagara(s, 290, 652, .9, color="#221b33", rim="#ffd9a8", light=1, shade="#000000")
    for k, t in enumerate([0.06, 0.18, 0.3, 0.42, 0.54, 0.66, 0.78, 0.9]):
        i = int(t * (len(path) - 1))
        x, y = path[i]
        side = 1 if k % 2 else -1
        sc = 0.4 + 0.6 * (1 - t)
        s.flame(x + side * 44 * sc, y + 2, 22 * sc, glow_r=110 * sc, glow_a=.5)
    s.add(fig.pilgrim(745, 832, 1.1, color="#0d0a14", rim="#ffcf9e"))
    pines(s, 1380, 1680, 1010, 7, h=(260, 440), color="#0a0812", seed=9)
    pines(s, -60, 110, 1010, 3, h=(180, 280), color="#0a0812", seed=10)
    s.birds(7, 980, 1260, 330, 400, color="#3a2a40", s=(5, 9), seed=2, a=.8)
    s.motes(36, 450, 1300, 600, 960, seed=8)
    s.fx("godrays", cx=sun[0], cy=sun[1], strength=.4, thresh=.68, decay=.972, radius=210)
    s.fx("mottle", amp=.05, cell=60)
    return s


@scene
def ghats(s):
    sun = (960, 492)
    wl = 690
    s.sky([(0, "#141c46"), (.18, "#2c2d68"), (.36, "#6a4580"), (.48, "#c0607a"), (.56, "#f28a68"), (.62, "#ffb56c"), (.7, "#ffd796")])
    s.sun(*sun, 36, halo_r=620, halo_a=.8)
    s.fx("clouds", y0=10, y1=300, seed=21, cell=150, aniso=3.4, cover=.45, soft=.16, lit="#ffb592", body=.62, direct=.9,
         light=(0.1, 1), sun=(sun[0], sun[1], 380), opacity=.95)
    s.fx("clouds", y0=250, y1=470, seed=22, cell=90, aniso=5, cover=.34, soft=.2, lit="#ffd6a0", body=.85, direct=.9,
         light=(0, 1), sun=(sun[0], sun[1], 300), opacity=.85)
    # far bank of the city, then the near ghats
    arch.skyline(s, -20, 1640, 600, h=(30, 80), color="#9a6a84", seed=31, windows=0, parapet=False,
                 temples=[(260, .45), (1240, .5)], chhatris=[(700, .5)])
    s.mist(600, 80, "#ffc9a2", .55, 18)
    arch.skyline(s, -30, 1660, 628, h=(60, 170), color="#4a2f52", rim="#ffbe8a", light=1, seed=32, windows=.16,
                 temples=[(330, 1.0), (1130, 1.15), (1460, .8)], chhatris=[(120, .8), (620, .7), (1320, .7)], storey=26)
    s.glow(sun[0], 610, 520, "#ffb070", .35, .2, sy=.3)
    arch.steps(s, -20, 1620, 628, wl, 9, color="#2a1b30", edge="#a86a62", edge_a=.35)
    for k, x in enumerate([90, 300, 1250, 1500]):
        arch.umbrella(s, x, 648 + (k % 2) * 14, .9, color="#1d1324", rim="#ffbe8a")
    lamps = []
    for k, x in enumerate([470, 590, 710, 830, 950, 1070]):
        s.add(f'<rect x="{x - 44}" y="664" width="88" height="10" fill="#1a1020"/>')
        svg, lx, ly = fig.priest_aarti(x, 664, .62, color="#140c18", flip=k % 2 == 1)
        s.add(svg)
        lamps.append((lx, ly))
    for lx, ly in lamps:
        s.glow(lx, 670, 150, "#ff9a4a", .35, .25, sy=.45)
        for dx, dy in ((-8, 2), (0, -4), (8, 2), (-4, 8), (4, 8)):
            s.flame(lx + dx, ly + dy + 4, 15, glow_r=110, glow_a=.45)
    rng = random.Random(4)
    for _ in range(14):
        x = rng.uniform(380, 1180)
        s.add(fig.sitter(x, wl - rng.choice([2, 10, 18]), .34, color="#150d19", flip=rng.random() < .5))
    s.mist(wl, 40, "#ffb98a", .35, 10)
    s.fx("reflect", y0=wl, strength=.85, tint="#1a0f26", tint_near=.5, tint_far=.1, amp=5)
    s.fx("glints", y0=wl, cx=sun[0], color="#ffe0a8", width=60, strength=1.1, scatter=.06, density=.5)
    for lx, ly in lamps:
        s.glow(lx, wl + (wl - ly) * .9, 80, "#ff9a4a", .3, .2, sy=1.8)
    s.wisps(14, 0, W, wl + 10, wl + 70, "#ffc8a8", a=(.06, .16), length=(200, 600), thick=(6, 16), blur=8, seed=3)
    for k in range(26):
        t = k / 25
        x = 700 + (rng.random() - .5) * (160 + 900 * t * t) + t * 120
        y = wl + 12 + (H - wl - 40) * t ** 1.6
        arch.leaf_lamp(s, x, y, .35 + 1.3 * t * t, seed=k)
    arch.boat(s, 1230, 760, .9, color="#120b16", rim="#ffb98a", people=2)
    arch.boat(s, 300, 735, .65, color="#150d1a", rim="#ffb98a", people=3, flip=True)
    arch.boat(s, 120, 1000, 2.2, color="#08050a", rim="#ff9a60", people=0, rower=False)
    s.birds(9, 800, 1150, 300, 400, color="#3a2030", s=(5, 10), seed=6, a=.85)
    s.fx("godrays", cx=sun[0], cy=sun[1], strength=.45, thresh=.7, decay=.97, radius=240)
    s.fx("mottle", amp=.045, cell=60)
    return s


@scene
def om(s):
    sun = (800, 606)
    wl = 612
    s.sky([(0, "#161c48"), (.22, "#3b3474"), (.4, "#8a5c92"), (.5, "#da8a8c"), (.56, "#ffbb94"), (.61, "#ffe2bc")])
    s.stars(60, 0, 260, seed=5, bright=.6)
    s.sun(*sun, 54, halo_r=700, halo_a=.8)
    s.fx("clouds", y0=40, y1=330, seed=31, cell=150, aniso=3.6, cover=.4, soft=.18, lit="#ffbfa0", body=.72, direct=.8,
         light=(0, 1), sun=(sun[0], sun[1], 420), opacity=.9)
    s.fx("clouds", y0=360, y1=560, seed=32, cell=80, aniso=6, cover=.3, soft=.22, lit="#ffe0b8", body=.85, direct=.95,
         light=(0, 1), sun=(sun[0], sun[1], 360), opacity=.8)
    far = ridgeline(wl, 46, 41, cell=260, octaves=5, ridged=.3)
    hills(s, far, "#9a6283", "#c98a8e", haze="#ffc9a8", haze_a=.5, haze_h=40)
    rng = random.Random(3)
    crowns = "".join(crown(x, wl - rng.uniform(4, 16), rng.uniform(10, 22), seed=int(x)) for x in range(-20, 560, 14))
    crowns += "".join(crown(x, wl - rng.uniform(4, 16), rng.uniform(10, 22), seed=int(x)) for x in range(1040, 1640, 14))
    s.add(f'<path d="{crowns}" fill="#6a4466"/>')
    arch.nagara(s, 360, wl - 6, .3, color="#5e3c60", rim="#ffc9a0", light=1, door=None, bands=False)
    near = ridgeline(wl + 2, 14, 42, cell=120, octaves=5, ridged=.2, envelope=[(0, 1), (560, .6), (800, .1), (1040, .6), (1600, 1)])
    hills(s, near, "#4e3254", "#5e3c60")
    s.mist(wl - 4, 40, "#ffd6b6", .6, 10)
    s.fx("reflect", y0=wl, strength=.9, tint="#2a1838", tint_near=.5, tint_far=.05, amp=3)
    s.fx("glints", y0=wl, cx=sun[0], color="#fff0c8", width=50, strength=1.2, scatter=.05, density=.5)
    s.wisps(12, 0, W, wl + 6, wl + 60, "#ffd9c0", a=(.08, .2), length=(260, 700), thick=(6, 18), blur=10, seed=5)
    ob.om_gold(s, 800, 300, 1.25, halo="#ffe2a8")
    leaf = dict(dark="#10221f", light="#2c4a40", rim="#ffc79a", rim_a=.7)
    ob.pad(s, 1050, 690, 70, seed=1, **leaf)
    ob.pad(s, 560, 676, 50, seed=2, **leaf)
    m = s.mark()
    s.add('<path d="M1064 688Q1060 660 1066 640" stroke="#2c4d3a" stroke-width="3" fill="none"/>')
    ob.lotus(s, 1066, 642, .32, seed=3)
    ob.reflect_since(s, m, 690, .35, 2, 60)
    ob.standing_leaf(s, 170, 650, .8, water=760, seed=2, dark="#0e1f1b", light="#2f5244", rim="#ffc79a")
    ob.standing_leaf(s, 1470, 672, .95, water=800, seed=4, dark="#0e1f1b", light="#2f5244", rim="#ffc79a")
    ob.pad(s, 1280, 880, 220, seed=4, **leaf)
    ob.pad(s, 320, 830, 180, seed=5, **leaf)
    ob.pad(s, 760, 960, 160, seed=6, **leaf)
    ob.pad(s, 1560, 980, 150, seed=7, **leaf)
    ob.bud(s, 520, 780, .8, stem_to=850)
    ob.bud(s, 1500, 800, .7, stem_to=880)
    s.add('<path d="M330 820Q322 790 330 766M1274 870Q1290 840 1278 812" stroke="#24402f" stroke-width="6" fill="none"/>')
    ob.lotus(s, 330, 770, .95, seed=1)
    ob.lotus(s, 1278, 816, 1.15, seed=2)
    s.motes(50, 200, 1400, 100, 700, seed=7)
    s.birds(5, 960, 1180, 420, 480, color="#5a3048", s=(5, 8), seed=4, a=.7)
    s.fx("godrays", cx=sun[0], cy=sun[1], strength=.35, thresh=.72, decay=.97, radius=260)
    s.fx("mottle", amp=.04, cell=60)
    return s


@scene
def flame(s):
    hz = 690
    ob.dark_room(s, light=(800, 470), warm="#5e2a12", r=1000, horizon=hz, floor="#160a06")
    rng = random.Random(3)
    lamps = []
    for row, (y, n, r, a) in enumerate(((330, 16, 7, .5), (420, 12, 12, .35))):
        for k in range(n):
            x = (k + rng.uniform(.2, .8)) * 1600 / n
            if abs(x - 800) > 160:
                lamps.append(f'<circle cx="{f(x)}" cy="{f(y + rng.uniform(-10, 10))}" r="{r}" fill="#ffb45a" opacity="{a}"/>')
    s.add(f'<g filter="{s.blur(4)}" style="mix-blend-mode:screen">{"".join(lamps)}</g>')
    s.bokeh(9, 0, 1600, 40, 600, colors=("#ff8a2a", "#ffb43a"), r=(26, 70), a=(.08, .2), blur=4, seed=6, ring=True)
    s.glow(800, 480, 760, "#ff8a3a", .22, .2)
    floor_glow = s.rad([(0, "#c8662a", .55), (0.4, "#8a3a14", .25), (1, "#3a1608", 0)], 800, hz + 40, 700, user=True,
                       transform=f"translate(0 {f((hz + 40) * .75)}) scale(1 .25)")
    s.add(f'<rect y="{hz}" width="1600" height="{1000 - hz}" fill="{floor_glow}" style="mix-blend-mode:screen"/>')
    s.add(f'<path d="M0 {hz}H1600" stroke="#ffb070" stroke-opacity=".18" stroke-width="2"/>')
    s.add(f'<path d="M1210 {hz + 6}L1228 360" stroke="#4a2810" stroke-width="3.4"/><circle cx="1228" cy="360" r="4" fill="#ff8a3a"/>'
          f'<ellipse cx="1210" cy="{hz + 8}" rx="26" ry="7" fill="#3a2010"/>')
    s.glow(1228, 360, 26, "#ff9a4a", .9, .3)
    s.smoke(1228, 356, 360, color="#f3e6d6", a=.45, seed=4, width=1.4)
    m = s.mark()
    ob.clay_diya(s, 600, 612, 1.75, flame_h=230)
    s.add(ob.marigold(300, hz + 4, 30, "#f39a1c", 1) + ob.marigold(360, hz + 16, 24, "#f7c02a", 2) + ob.marigold(1080, hz + 10, 26, "#e8562a", 3))
    ob.petals_scatter(s, 220, 1380, hz - 2, hz + 30, 26, seed=5, size=(5, 9))
    ob.reflect_since(s, m, hz + 32, .28, 3, 220)
    s.glow(800, hz + 150, 120, "#ffb060", .35, .3, sy=1.8)
    s.add(f'<g filter="{s.blur(10)}">' + ob.marigold(170, 940, 80, "#f39a1c", 4) + ob.marigold(1470, 970, 66, "#e8562a", 5) + '</g>')
    s.motes(30, 560, 1100, 160, 560, seed=7, size=(.8, 1.8))
    s.fx("mottle", amp=.035, cell=50)
    return s
