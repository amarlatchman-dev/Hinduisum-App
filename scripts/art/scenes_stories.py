"""Paintings for the children's stories from the Panchatantra and Hitopadesha: the animals as
silhouettes against luminous skies, in the same style as the lesson paintings."""
import math
import random

import objects as ob
from land import crown, ridgeline, hills, round_tree, grass
from paint import H, W, f, mix
from scenes import scene
from scenes_land import palm


# ======================================================================
# the animals, as SVG silhouettes; (x, y) is where they stand, sc their size
# ======================================================================
def _g(x, y, sc, inner, flip=False, rot=0):
    sx = -sc if flip else sc
    return f'<g transform="translate({f(x)} {f(y)}) rotate({f(rot)}) scale({f(sx)} {f(sc)})">{inner}</g>'


def put(s, svg_fn, x, y, sc, color="#1a1220", rim=None, flip=False, rot=0, rim_dx=2.0, **kw):
    inner = svg_fn(**kw)
    if rim:
        s.add(f'<g fill="{rim}" transform="translate({f(rim_dx)} {f(-abs(rim_dx) * .6)})">{_g(x, y, sc, inner, flip, rot)}</g>')
    s.add(f'<g fill="{color}">{_g(x, y, sc, inner, flip, rot)}</g>')


def monkey_svg(arms="hang", tail=1):
    """A monkey sitting, facing right; about 100 tall. arms: hang, reach, up."""
    a = {"hang": "M-6 -46Q8 -36 10 -18L16 -16Q14 -40 0 -52Z", "reach": "M-4 -50Q20 -60 40 -64L42 -58Q20 -50 0 -42Z",
         "up": "M0 -52Q10 -74 8 -96L14 -96Q18 -72 6 -46Z"}[arms]
    t = ("M-20 -20Q-60 -10 -58 -46Q-56 -70 -36 -66Q-48 -60 -46 -44Q-44 -24 -16 -28Z" if tail == 1
         else "M-20 -16Q-40 10 -30 40Q-26 52 -18 48Q-28 30 -12 -14Z")
    return (f'<ellipse cx="0" cy="-34" rx="20" ry="26"/><circle cx="10" cy="-70" r="15"/>'
            f'<ellipse cx="22" cy="-66" rx="9" ry="7"/><circle cx="2" cy="-80" r="5"/><circle cx="4" cy="-74" r="5"/>'
            f'<path d="{a}"/><path d="M-14 -14Q-18 0 -6 2L10 2Q4 -6 6 -14Z"/><path d="{t}"/>')


def crocodile_svg():
    """A crocodile swimming to the right, mostly under water; about 260 long. The back is at y = 0."""
    ridges = "".join(f'<path d="M{x} -6L{x + 5} -16L{x + 10} -6Z"/>' for x in range(-110, 40, 16))
    return ('<path d="M-130 2Q-60 -14 30 -10Q60 -12 92 -6Q118 -4 132 0Q118 6 90 6Q40 8 -60 8Q-110 10 -150 4Z"/>'
            '<circle cx="62" cy="-14" r="6"/><circle cx="76" cy="-12" r="5"/>' + ridges)


def _leg(x0, y0, x1, y1, w0, w1, bend=0.0):
    from scenes_festive import _taper_path
    from land import smooth_line
    mx, my = (x0 + x1) / 2 + bend, (y0 + y1) / 2
    return f'<path d="{_taper_path(smooth_line([(x0, y0), (mx, my), (x1, y1)], step=4), w0, w1)}"/><ellipse cx="{f(x1 + 3)}" cy="{f(y1 - 2)}" rx="{f(w1 * .9)}" ry="{f(w1 * .45)}"/>'


def lion_svg(roar=False):
    """A lion standing, facing right; about 130 tall: a deep chest, a great mane, a tufted tail."""
    body = ('<path d="M-84 -58C-90 -86 -60 -98 -20 -96C10 -98 40 -102 58 -94C72 -86 74 -60 66 -44C50 -34 20 -38 0 -40'
            'C-30 -38 -60 -36 -78 -42Z"/>')
    mane = "".join(f'<ellipse cx="{f(52 + math.cos(a) * 26)}" cy="{f(-92 + math.sin(a) * 30)}" rx="16" ry="11" transform="rotate({f(math.degrees(a))} {f(52 + math.cos(a) * 26)} {f(-92 + math.sin(a) * 30)})"/>'
                   for a in [k * math.pi / 7 for k in range(14)])
    face = ('<path d="M64 -108C82 -110 96 -100 100 -88C102 -80 96 -74 86 -72C80 -64 66 -66 60 -74Z"/>' if not roar else
            '<path d="M64 -110C82 -114 100 -108 106 -98L92 -92L108 -84C102 -72 88 -68 74 -70C64 -72 58 -82 60 -94Z"/>')
    legs = (_leg(-70, -50, -74, 0, 16, 10, -4) + _leg(-48, -46, -44, 0, 15, 10, 4) + _leg(40, -50, 42, 0, 16, 10, -3) + _leg(58, -50, 64, 0, 15, 10, 3))
    tail = '<path d="M-82 -72C-108 -70 -120 -48 -114 -28L-109 -28C-114 -46 -104 -62 -80 -64Z"/><ellipse cx="-111" cy="-24" rx="8" ry="11"/>'
    return body + '<circle cx="52" cy="-92" r="30"/>' + mane + face + legs + tail


def hare_svg():
    """A hare sitting up, facing left; about 90 tall."""
    return ('<ellipse cx="6" cy="-26" rx="24" ry="26"/><circle cx="-12" cy="-52" r="13"/>'
            '<path d="M-14 -62Q-22 -96 -12 -100Q-4 -96 -8 -62Z"/><path d="M-6 -62Q2 -92 12 -94Q16 -88 2 -60Z"/>'
            '<ellipse cx="-12" cy="-2" rx="14" ry="4"/><circle cx="30" cy="-18" r="7"/>')


def tortoise_svg():
    return ('<path d="M-40 0Q-38 -34 0 -36Q38 -34 40 0Z"/><path d="M36 -10Q54 -14 58 -6Q56 0 40 -2Z"/>'
            '<rect x="-30" y="-4" width="10" height="10" rx="3"/><rect x="18" y="-4" width="10" height="10" rx="3"/>')


def goose_svg(phase=0.0):
    """A flying goose, facing right, wings raised; about 140 across."""
    up = math.sin(phase)
    wing = (f'<path d="M-14 -6C-20 {f(-30 - 10 * up)} -36 {f(-56 - 14 * up)} -62 {f(-66 - 16 * up)}'
            f'C-56 {f(-58 - 12 * up)} -54 {f(-50 - 10 * up)} -58 {f(-44 - 8 * up)}C-46 {f(-44 - 8 * up)} -42 {f(-36 - 6 * up)} -44 {f(-30 - 6 * up)}'
            f'C-30 {f(-30 - 4 * up)} -10 -16 12 -6Z"/>')
    return ('<path d="M-40 2C-34 -10 -10 -12 16 -8C26 -8 34 -12 40 -16C48 -22 56 -22 62 -18L72 -16L62 -12C56 -10 50 -6 42 -2C30 8 0 12 -26 8Z"/>'
            '<path d="M-38 2L-56 -2L-50 8Z"/>' + wing)


def jackal_svg(howl=False):
    """A jackal, slender with a long muzzle, big ears and a bushy tail, facing right; about 90 tall."""
    body = '<path d="M-50 -50C-52 -64 -30 -66 0 -64C24 -64 40 -62 46 -54C50 -44 44 -36 34 -36C10 -34 -20 -34 -44 -36Z"/>'
    if howl:
        head = ('<path d="M34 -60C38 -76 44 -90 52 -100L70 -116L66 -100C64 -88 58 -72 50 -58Z"/>'
                '<path d="M46 -92L40 -112L52 -100Z"/><path d="M54 -94L54 -114L62 -100Z"/>')
    else:
        head = ('<path d="M36 -58C44 -70 56 -72 64 -66L88 -58L86 -52L62 -48C52 -46 42 -48 36 -52Z"/>'
                '<path d="M50 -68L48 -90L60 -70Z"/><path d="M58 -66L62 -86L68 -66Z"/>')
    legs = _leg(-42, -40, -46, 0, 9, 5, -3) + _leg(-28, -38, -24, 0, 8, 5, 3) + _leg(28, -40, 30, 0, 9, 5, -2) + _leg(40, -42, 46, 0, 8, 5, 2)
    tail = '<path d="M-48 -54C-74 -50 -88 -30 -86 -10C-76 -16 -70 -30 -60 -36C-56 -40 -50 -42 -46 -44Z"/>'
    return body + head + legs + tail


def crow_svg(fly=False):
    if fly:
        return ('<ellipse cx="0" cy="0" rx="22" ry="8"/><path d="M18 -4L34 0L18 4Z"/><path d="M-20 0L-36 -6L-34 6Z"/>'
                '<path d="M-6 -4Q-16 -36 -40 -44Q-20 -20 8 -2Z"/><path d="M-2 2Q-10 20 -26 30Q-8 16 10 2Z"/>')
    return ('<ellipse cx="0" cy="-16" rx="14" ry="20" transform="rotate(20 0 -16)"/><circle cx="10" cy="-34" r="9"/>'
            '<path d="M16 -36L30 -32L16 -30Z"/><path d="M-10 -2L-30 14L-24 18L-4 2Z"/><path d="M0 0L-2 8M6 0L6 8" stroke="#000" stroke-width="2"/>')


def snake_path(pts, w0, w1):
    from scenes_festive import _taper_path
    from land import smooth_line
    return f'<path d="{_taper_path(smooth_line(pts, step=6), w0, w1)}"/>'


def mongoose_svg():
    return ('<path d="M-60 -16Q-56 -30 -10 -30Q30 -32 44 -26L60 -22L70 -16L60 -12L40 -10Q0 -6 -56 -8Z"/>'
            '<circle cx="46" cy="-28" r="3"/><rect x="-46" y="-12" width="7" height="12" rx="3"/><rect x="24" y="-12" width="7" height="12" rx="3"/>'
            '<path d="M-58 -14Q-96 -12 -116 4Q-90 -4 -56 -6Z"/>')


def heron_svg():
    """A heron standing, facing right; about 220 tall."""
    return ('<ellipse cx="0" cy="-110" rx="38" ry="20" transform="rotate(-18 0 -110)"/>'
            '<path d="M24 -122Q40 -150 30 -176Q28 -196 44 -198Q58 -196 56 -184L96 -176L56 -176Q46 -170 42 -150Q46 -130 34 -114Z"/>'
            '<path d="M-36 -104L-64 -86L-30 -96Z"/>'
            '<path d="M-2 -94L-6 0L-2 0L4 -94Z"/><path d="M8 -94L16 0L20 0L14 -94Z"/>')


def crab_svg():
    return ('<ellipse cx="0" cy="0" rx="26" ry="16"/>'
            '<path d="M-20 -8Q-40 -26 -34 -40Q-26 -36 -28 -26Q-22 -18 -14 -10Z"/><path d="M20 -8Q40 -26 34 -40Q26 -36 28 -26Q22 -18 14 -10Z"/>'
            '<path d="M-36 -42L-46 -50L-30 -46Z"/><path d="M36 -42L46 -50L30 -46Z"/>'
            + "".join(f'<path d="M{s * 22} {4 + k * 4}L{s * (40 + k * 4)} {14 + k * 6}" stroke="#000" stroke-width="3"/>' for s in (-1, 1) for k in range(3)))


def donkey_svg(bray=True):
    """A donkey, facing right; with bray its head is thrown back; about 140 tall."""
    body = '<path d="M-64 -74C-68 -94 -40 -98 -10 -96C20 -98 44 -96 52 -84C58 -72 54 -58 44 -54C20 -50 -20 -50 -58 -54C-66 -58 -66 -66 -64 -74Z"/>'
    neck = '<path d="M30 -92C40 -100 50 -100 56 -90L62 -80L44 -74Z"/>'
    if bray:
        head = ('<path d="M48 -96C52 -112 62 -124 74 -130C84 -134 92 -128 90 -120L70 -96C64 -88 54 -86 48 -90Z"/>'
                '<path d="M80 -126L98 -140L92 -128Z"/>'
                '<path d="M56 -112C50 -130 46 -146 50 -152C56 -148 60 -130 62 -114Z"/><path d="M62 -116C62 -134 64 -150 70 -152C74 -146 70 -130 68 -116Z"/>')
    else:
        head = ('<path d="M50 -92C62 -94 80 -88 90 -80C96 -74 92 -66 84 -66L58 -70C50 -72 46 -84 50 -92Z"/>'
                '<path d="M54 -92C50 -110 50 -124 54 -128C60 -122 60 -108 60 -92Z"/>')
    legs = _leg(-56, -58, -58, 0, 12, 7, -3) + _leg(-38, -56, -34, 0, 11, 7, 3) + _leg(30, -58, 32, 0, 12, 7, -2) + _leg(44, -58, 48, 0, 11, 7, 2)
    tail = '<path d="M-64 -80C-76 -70 -78 -52 -74 -40L-70 -40C-72 -54 -68 -68 -60 -76Z"/><ellipse cx="-72" cy="-36" rx="5" ry="8"/>'
    return body + neck + head + legs + tail


def dove_svg(phase=0.0):
    up = math.sin(phase)
    return (f'<ellipse cx="0" cy="0" rx="18" ry="8"/><circle cx="16" cy="-4" r="6"/><path d="M20 -4L28 -2L20 0Z"/>'
            f'<path d="M-16 0L-30 -6L-28 6Z"/>'
            f'<path d="M-4 -4Q-12 {f(-26 - 10 * up)} -30 {f(-32 - 12 * up)}Q-14 {f(-16 - 6 * up)} 8 -2Z"/>')


def mouse_svg():
    return ('<ellipse cx="0" cy="-10" rx="16" ry="10"/><path d="M12 -16L26 -10L12 -4Z"/><circle cx="8" cy="-20" r="5"/>'
            '<path d="M-14 -8Q-30 -2 -40 -12" stroke="#000" stroke-width="2" fill="none"/>')


def sky_and_ground(s, top, mid, low, hz, ground, ground2, sun=None, sun_r=40, seed=1, clouds=True, moon=None, stars=0):
    s.sky([(0, top), (.45, mid), (hz / H, low)], 0, H)
    if stars:
        s.stars(stars, 0, hz - 200, seed=seed, bright=.8)
    if moon:
        s.moon(*moon, 34, glow_r=280)
    if sun:
        s.sun(*sun, sun_r, core="#fffbee", rim="#ffe8c0", halo="#ffc890", halo_r=640, halo_a=.7)
    if clouds:
        s.fx("clouds", y0=60, y1=hz - 120, seed=seed + 10, cell=160, aniso=3.4, cover=.34, soft=.2,
             lit="#fff0dc", body=.8, direct=.9, light=(0, 1), sun=(sun or (800, 200))[:2] + (420,), rim="#fff8ee", opacity=.8)
    gg = s.lin([(0, ground, 1), (1, ground2, 1)], 0, hz, 0, H, user=True)
    s.add(f'<rect y="{hz}" width="{W}" height="{H - hz}" fill="{gg}"/>')


def tree_line(s, hz, color, seed=1, amp=(20, 60), r=(30, 56)):
    rng = random.Random(seed)
    s.add(f'<path d="{"".join(crown(x, hz - rng.uniform(*amp), rng.uniform(*r), seed=x) for x in range(-40, 1680, 50))}" fill="{color}"/>')


def water(s, y0, sun_x=None, deep="#2e3c64", sky="#a8b4d0", far="#f4d8c0", light=None):
    s.fx("sea", y0=y0, deep=deep, sky=sky, sky_far=far, crest="#e8e0e8", foam="#fbf6f4", seed=11, cell=20,
         aniso=2.4, chop=.45, foam_amt=.06, light=light or (sun_x or 800, y0 + 20), light_c="#ffd8a0", light_r=220, light_a=.35, gloss=.8)
    if sun_x:
        s.fx("glints", y0=y0, cx=sun_x, color="#fff0d0", width=70, strength=.9, scatter=.1, density=.5, spread=2.2)


def big_tree(s, x, base, h, color, seed=1, lean=0.0):
    """A broad tree with a trunk and a rounded canopy (rose-apple, banyan)."""
    rng = random.Random(seed)
    s.add(f'<path d="M{f(x - h * .05)} {f(base)}Q{f(x - h * .02 + lean * h)} {f(base - h * .45)} {f(x - h * .03 + lean * h)} {f(base - h * .62)}'
          f'L{f(x + h * .05 + lean * h)} {f(base - h * .62)}Q{f(x + h * .04 + lean * h)} {f(base - h * .45)} {f(x + h * .06)} {f(base)}Z" fill="{color}"/>')
    blobs = "".join(crown(x + lean * h + rng.uniform(-h * .42, h * .42), base - h * rng.uniform(.6, .95), h * rng.uniform(.14, .22), seed=seed + k)
                    for k in range(14))
    s.add(f'<path d="{blobs}" fill="{color}"/>')
    return x + lean * h, base - h * .62


# ======================================================================
# the scenes
# ======================================================================
@scene
def story_monkey_crocodile(s):
    sun = (1180, 420)
    hz = 600
    sky_and_ground(s, "#3a4a8a", "#e0a090", "#ffd8a8", hz, "#2c3c5c", "#1c2438", sun=sun, seed=3)
    tree_line(s, hz, "#5a5070", seed=4, amp=(10, 30), r=(20, 34))
    water(s, hz, sun[0], deep="#2a3458", sky="#b090a8", far="#ffd0a8")
    # the far bank with the rose-apple tree, and the monkey on the crocodile's back
    s.add(f'<path d="M-20 {hz + 8}Q200 {hz - 40} 420 {hz + 6}L420 {hz + 30}L-20 {hz + 30}Z" fill="#1c1626"/>')
    big_tree(s, 190, hz + 10, 420, "#1c1626", seed=7, lean=.03)
    for k in range(18):
        rng = random.Random(k)
        s.add(f'<circle cx="{f(100 + rng.uniform(0, 200))}" cy="{f(hz - 260 + rng.uniform(0, 140))}" r="6" fill="#6a2a6a" opacity=".9"/>')
    y = 760
    put(s, crocodile_svg, 820, y, 3.1, color="#1c1a22", rim="#ffd0a0")
    put(s, monkey_svg, 740, y - 18, 2.2, color="#2a1c22", rim="#ffd8a8", arms="reach")
    s.add(f'<ellipse cx="820" cy="{y + 14}" rx="320" ry="16" fill="#ffe8c8" opacity=".25" filter="{s.blur(6)}"/>')
    s.fx("godrays", cx=sun[0], cy=sun[1], strength=.25, thresh=.85, decay=.97, radius=220)
    s.fx("mottle", amp=.03, cell=60)
    s.look = {"vibrance": .14, "vignette": .26}
    return s


@scene
def story_lion_hare(s):
    s.sky([(0, "#1a2a4a"), (.4, "#4a4a7a"), (.62, "#d89a7a"), (.7, "#f4c89a")], 0, 1000)
    s.fx("clouds", y0=60, y1=440, seed=21, cell=170, aniso=3, cover=.36, soft=.2, lit="#ffd8b8", body=.75, direct=.9,
         light=(0, 1), sun=(400, 640, 420), opacity=.8)
    hz = 680
    tree_line(s, hz, "#2a2234", seed=5)
    gg = s.lin([(0, "#6a5a3a", 1), (1, "#2a2018", 1)], 0, hz, 0, H, user=True)
    s.add(f'<rect y="{hz - 4}" width="{W}" height="{H - hz + 4}" fill="{gg}"/>')
    # the well: a stone ring, and in its water the lion's reflection
    cx, cy = 980, 860
    s.add(f'<ellipse cx="{cx}" cy="{cy}" rx="200" ry="56" fill="#7a6a58"/><ellipse cx="{cx}" cy="{cy - 6}" rx="170" ry="42" fill="#3a3040"/>')
    s.add(f'<ellipse cx="{cx}" cy="{cy - 4}" rx="160" ry="36" fill="#6a7aa8" opacity=".6"/>')
    put(s, lion_svg, cx - 10, cy - 30, .55, color="#2a2238", flip=False, rot=180, roar=True)
    s.add(f'<ellipse cx="{cx}" cy="{cy - 6}" rx="170" ry="42" fill="none" stroke="#c8b898" stroke-width="10"/>')
    # the lion roaring over the well, and the hare watching
    put(s, lion_svg, 860, 812, 2.3, color="#2a1a14", rim="#ffc890", roar=True)
    put(s, hare_svg, 420, 900, 2.2, color="#2a1a14", rim="#ffd8a8", flip=False)
    grass(s, 0, 1600, 1000, 160, h=(10, 30), color="#1a140e", seed=4)
    s.fx("mottle", amp=.03, cell=60)
    s.look = {"vibrance": .12, "vignette": .3}
    return s


@scene
def story_tortoise_geese(s):
    sun = (1250, 640)
    hz = 760
    sky_and_ground(s, "#3a7ac8", "#9ac4e8", "#f4e4cc", hz, "#a89a6a", "#6a5a3a", sun=sun, seed=7)
    far = ridgeline(hz, 20, 9, cell=220, octaves=5, ridged=.2)
    hills(s, far, "#8aa0b8", "#a8b8c8")
    fields = s.lin([(0, "#b8a870", 1), (.5, "#8a9a52", 1), (1, "#5a6a32", 1)], 0, hz, 0, H, user=True)
    s.add(f'<rect y="{hz}" width="{W}" height="{H - hz}" fill="{fields}"/>')
    rng = random.Random(3)
    for k in range(9):
        x = 100 + k * 170 + rng.uniform(-30, 30)
        s.add(f'<rect x="{f(x)}" y="{hz - 26}" width="46" height="26" fill="#7a7a8a"/><path d="M{f(x - 6)} {hz - 26}L{f(x + 23)} {hz - 46}L{f(x + 52)} {hz - 26}Z" fill="#6a6a7a"/>')
    # the two geese with the stick, the tortoise holding on in the middle
    sx0, sx1, sy = 520, 1020, 400
    put(s, goose_svg, sx0, sy, 2.4, color="#d8d4cc", rim="#ffffff", phase=.8)
    put(s, goose_svg, sx1, sy, 2.4, color="#d8d4cc", rim="#ffffff", phase=2.2)
    stick_y = sy - 38
    s.add(f'<path d="M{sx0 + 168} {stick_y}L{sx1 + 172} {stick_y}" stroke="#6a4a2a" stroke-width="7" stroke-linecap="round"/>')
    # the tortoise hangs from the middle of the stick by its mouth
    put(s, tortoise_svg, 948, stick_y + 128, 2.2, color="#3a4a2a", rim="#e8f0c8", rot=-90)
    for gx, gy in ((sx0, sy), (sx1, sy)):
        s.add(f'<ellipse cx="{gx}" cy="{gy}" rx="70" ry="22" fill="#000" opacity=".08" filter="{s.blur(6)}"/>')
    # people below, pointing up
    from scenes_festive import person, J_BOTH_UP
    for x, sc in ((300, 1.6), (380, 1.4), (1350, 1.6)):
        person(s, x, 940, sc, J_BOTH_UP, "#3a2a1a", "#ffe8c8")
    s.fx("mottle", amp=.03, cell=60)
    s.look = {"vibrance": .12, "vignette": .22}
    return s


@scene
def story_blue_jackal(s):
    hz = 700
    sky_and_ground(s, "#08081e", "#1a1a44", "#3a2a5a", hz, "#1a1424", "#0c0a12", seed=9, clouds=False, moon=(1180, 220), stars=180)
    tree_line(s, hz, "#0e0c18", seed=8, amp=(40, 120), r=(40, 80))
    s.glow(1180, 220, 600, "#a8b8ff", .3, .2)
    # the blue jackal howling at the moon on a rock, the other animals below
    s.add(f'<path d="M480 {H}L520 760Q620 640 760 650Q900 660 980 760L1040 {H}Z" fill="#1c1828"/>')
    s.add(f'<path d="M560 700Q700 640 860 668" stroke="#5a5a98" stroke-width="4" fill="none" opacity=".6"/>')
    s.glow(760, 560, 220, "#4a7aff", .28, .3)
    put(s, jackal_svg, 740, 664, 3.0, color="#2a5ad8", rim="#c8dcff", howl=True)
    put(s, lion_svg, 260, 930, 1.6, color="#0a0810", rim="#7a88c8")
    put(s, jackal_svg, 1300, 900, 1.2, color="#0a0810", rim="#7a88c8", flip=True)
    put(s, jackal_svg, 1440, 910, 1.1, color="#0a0810", rim="#7a88c8", flip=True, howl=True)
    s.mist(hz + 20, 80, "#6a6aa8", .25, 24)
    s.fx("mottle", amp=.03, cell=60)
    s.look = {"vibrance": .12, "vignette": .34}
    return s


@scene
def story_crows_serpent(s):
    sun = (1300, 300)
    hz = 760
    sky_and_ground(s, "#4a8ac8", "#a8d0ec", "#f6ecd8", hz, "#7a8a4a", "#3a4a22", sun=sun, seed=11)
    tree_line(s, hz, "#5a7a5a", seed=6, amp=(10, 40))
    # the banyan with hanging roots, the nest, the snake below
    tx, ty = big_tree(s, 520, hz + 60, 640, "#1e2a1a", seed=12)
    roots = "".join(f'<path d="M{f(300 + k * 30)} {f(ty - 30 + (k % 3) * 10)}L{f(302 + k * 30)} {hz + 50}" stroke="#1e2a1a" stroke-width="3"/>' for k in range(14))
    s.add(roots)
    s.add(f'<ellipse cx="610" cy="{f(ty - 70)}" rx="40" ry="14" fill="#4a3a2a"/>')
    put(s, crow_svg, 600, ty - 80, 1.5, color="#14101a", rim="#d8e8ff")
    s.add(f'<ellipse cx="520" cy="{hz + 62}" rx="50" ry="16" fill="#0e0a08"/>')
    s.add(f'<g fill="#1a1a14">{snake_path([(470, hz + 64), (430, hz + 40), (470, hz + 10), (440, hz - 30)], 18, 4)}</g>')
    # the mother crow flying with the golden necklace, the guards running behind
    put(s, crow_svg, 1020, 420, 2.2, color="#14101a", rim="#fff0d8", fly=True)
    s.add(f'<path d="M1060 432Q1080 470 1100 432" stroke="#ffd25a" stroke-width="5" fill="none"/><circle cx="1080" cy="452" r="6" fill="#ff5a5a"/>')
    s.glow(1080, 440, 50, "#ffe08a", .6, .3)
    from scenes_festive import person
    from scenes_caribbean import walker
    for x in (1240, 1360):
        person(s, x, 940, 1.8, walker(.6, .5), "#2a2018", "#fff0d8", kurta=(-14, 14, -28, 1), hair=None, sticks=[("rw", -70, 30)])
    s.fx("mottle", amp=.03, cell=60)
    s.look = {"vibrance": .12, "vignette": .24}
    return s


@scene
def story_mongoose(s):
    # inside a village house, lamplit: the cradle, the safe baby, the mongoose, the snake
    s.sky([(0, "#1a0e0a"), (1, "#2a160e")], 0, 1000)
    s.glow(1100, 380, 900, "#ff9a3a", .4, .2)
    s.add('<rect x="1000" y="220" width="220" height="300" rx="6" fill="#ffb86a" opacity=".55"/>'
          '<rect x="1004" y="224" width="212" height="292" fill="none" stroke="#5a3418" stroke-width="10"/>'
          '<path d="M1110 224V516M1004 370H1216" stroke="#5a3418" stroke-width="8"/>')
    s.add('<rect y="760" width="1600" height="240" fill="#3a2214"/>')
    s.add(f'<rect y="760" width="1600" height="240" fill="#4a2a18" filter="{s.grain(.05, 3, .2, 5, "#2a160a")}"/>')
    # the cradle
    s.add('<path d="M560 520Q700 640 840 520" stroke="#6a3a1a" stroke-width="10" fill="none"/>'
          '<path d="M580 560Q700 690 820 560L820 600Q700 720 580 600Z" fill="#8a4a22"/>'
          '<path d="M600 140L700 220L800 140" stroke="#4a2a14" stroke-width="5" fill="none"/>'
          '<path d="M700 220V520" stroke="#4a2a14" stroke-width="4"/>')
    s.add('<ellipse cx="700" cy="590" rx="80" ry="22" fill="#f4e4c8"/><circle cx="650" cy="578" r="18" fill="#e8c8a0"/>')
    ob.clay_diya(s, 1180, 740, sc=.4)
    put(s, mongoose_svg, 920, 900, 2.6, color="#5a3a22", rim="#ffd8a0", flip=False)
    s.add(f'<g fill="#1a1410">{snake_path([(260, 940), (360, 900), (460, 950), (560, 910)], 26, 5)}</g>')
    s.motes(40, 400, 1300, 200, 800, color="#ffd8a0", seed=3)
    s.fx("mottle", amp=.03, cell=60)
    s.look = {"vibrance": .1, "vignette": .36, "bloom": .4}
    return s


@scene
def story_heron_crab(s):
    sun = (420, 420)
    hz = 620
    sky_and_ground(s, "#4a5a9a", "#d8a8b0", "#ffe0b8", hz, "#3a4a6a", "#2a3048", sun=sun, seed=13)
    tree_line(s, hz, "#6a5a7a", seed=9, amp=(8, 24), r=(18, 30))
    water(s, hz, sun[0], deep="#344670", sky="#c0a8c0", far="#ffd8b8")
    for k in range(9):
        x = 120 + k * 60
        s.add(f'<path d="M{x} 1000Q{x + 6} 800 {x + 20} 720" stroke="#1a2016" stroke-width="5" fill="none"/>')
    put(s, heron_svg, 980, 900, 2.6, color="#1c1824", rim="#ffe0c0")
    put(s, crab_svg, 1250, 760, 1.4, color="#c8502a", rim="#ffd8a8", rot=-10)
    s.add(f'<path d="M1140 690Q1200 720 1230 720" stroke="#1c1824" stroke-width="3" fill="none" opacity=".0"/>')
    for k in range(6):
        rng = random.Random(k)
        s.add(f'<ellipse cx="{f(700 + rng.uniform(0, 500))}" cy="{f(800 + rng.uniform(0, 120))}" rx="18" ry="6" fill="#ffd8a8" opacity=".25"/>')
    s.fx("mottle", amp=.03, cell=60)
    s.look = {"vibrance": .12, "vignette": .26}
    return s


@scene
def story_donkey(s):
    hz = 700
    sky_and_ground(s, "#0a0c24", "#1e2050", "#3a3466", hz, "#1e2a1a", "#0c120a", seed=17, clouds=False, moon=(380, 200), stars=150)
    tree_line(s, hz, "#0e1410", seed=4)
    # a fence, the cucumber field, the braying donkey, the jackal slipping away, the farmer's hut
    s.add(''.join(f'<rect x="{x}" y="{hz - 20}" width="8" height="60" fill="#2a2014"/>' for x in range(0, 1600, 70)))
    s.add(f'<path d="M0 {hz}H1600M0 {hz + 20}H1600" stroke="#2a2014" stroke-width="4"/>')
    for k in range(60):
        rng = random.Random(k)
        x, y = rng.uniform(0, 1600), rng.uniform(hz + 60, 1000)
        s.add(f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(14 + (y - hz) / 20)}" ry="{f(5 + (y - hz) / 50)}" fill="#2a4a22"/>')
    s.add(f'<path d="M1200 {hz - 30}L1300 {hz - 110}L1400 {hz - 30}Z" fill="#1a140e"/><rect x="1220" y="{hz - 30}" width="160" height="70" fill="#1a140e"/>'
          f'<rect x="1286" y="{hz - 10}" width="30" height="40" fill="#ffc87a"/>')
    s.glow(1300, hz + 10, 140, "#ffb060", .4, .3)
    put(s, donkey_svg, 740, 920, 3.0, color="#1a1620", rim="#c8d0ff", bray=True)
    for k, (x, y) in enumerate([(1000, 470), (1060, 410), (1120, 350)]):
        s.add(f'<text x="{x}" y="{y}" font-size="{40 + k * 10}" fill="#e8e8ff" opacity=".8" font-family="serif">♪</text>')
    put(s, jackal_svg, 220, 790, 1.4, color="#100c10", rim="#8a90c8", flip=True)
    s.fx("mottle", amp=.03, cell=60)
    s.look = {"vibrance": .1, "vignette": .32}
    return s


@scene
def story_doves(s):
    sun = (800, 820)
    hz = 820
    sky_and_ground(s, "#3a6ac0", "#88b8e4", "#ffe4c0", hz, "#4a5a2a", "#22300f", sun=sun, sun_r=60, seed=19)
    tree_line(s, hz, "#4a5a3a", seed=11, amp=(30, 90), r=(36, 60))
    # the doves rising together with the net
    rng = random.Random(5)
    doves = [(560 + (k % 6) * 90 + rng.uniform(-20, 20), 260 + (k // 6) * 60 + rng.uniform(-14, 14)) for k in range(12)]
    net_top = 300
    for x, y in doves:
        put(s, dove_svg, x, y, 1.6, color="#ffffff", rim=None, phase=rng.uniform(0, 6))
    xs = [x for x, _ in doves]
    x0, x1 = min(xs) - 40, max(xs) + 40
    lines = "".join(f'<path d="M{f(x0 + t * (x1 - x0))} {net_top - 30}Q{f(x0 + t * (x1 - x0) + 10)} {net_top + 120} {f(x0 + t * (x1 - x0) + 20)} {net_top + 200}"/>' for t in [i / 10 for i in range(11)])
    lines += "".join(f'<path d="M{f(x0)} {net_top - 30 + k * 26}Q{f((x0 + x1) / 2)} {net_top - 20 + k * 30} {f(x1 + 20)} {net_top - 30 + k * 26}"/>' for k in range(9))
    s.add(f'<g stroke="#5a4a3a" stroke-width="2.4" fill="none" opacity=".75">{lines}</g>')
    # the hunter far below, and the mouse's tree
    from scenes_festive import person, J_THROW_UP
    person(s, 300, 960, 1.5, J_THROW_UP, "#1a1a12", "#ffe8c8", kurta=(-14, 14, -28, 1), hair=None)
    big_tree(s, 1340, hz + 60, 380, "#1a2412", seed=21)
    put(s, mouse_svg, 1300, hz + 90, 1.6, color="#1a140e", rim="#ffe0b8")
    s.fx("godrays", cx=sun[0], cy=sun[1], strength=.3, thresh=.85, decay=.97, radius=240)
    s.fx("mottle", amp=.03, cell=60)
    s.look = {"vibrance": .12, "vignette": .24}
    return s


@scene
def story_monkey_wedge(s):
    sun = (1260, 300)
    hz = 720
    sky_and_ground(s, "#4a8ac8", "#a8d0ec", "#f8ecd4", hz, "#b89a6a", "#7a5a3a", sun=sun, seed=23)
    tree_line(s, hz, "#4a6a4a", seed=13)
    # the half-built temple behind
    s.add(f'<path d="M1080 {hz}L1080 {hz - 220}L1180 {hz - 320}L1280 {hz - 220}L1280 {hz}Z" fill="#c8a880" opacity=".8"/>'
          + "".join(f'<path d="M{1060 + k * 40} {hz}V{hz - 260}" stroke="#8a6a4a" stroke-width="5"/>' for k in range(7)))
    # the half-split log on its trestles, the wedge, the monkey
    s.add('<rect x="380" y="760" width="16" height="140" fill="#5a3a1a"/><rect x="1000" y="760" width="16" height="140" fill="#5a3a1a"/>')
    s.add('<path d="M300 700H1100V770H300Z" fill="#a8743a"/><path d="M300 700Q300 690 310 690H1090Q1100 690 1100 700Z" fill="#c8945a"/>'
          '<path d="M700 735L1100 712L1100 745Z" fill="#3a2410"/>'
          + "".join(f'<path d="M300 {706 + k * 10}H1100" stroke="#8a5a2a" stroke-width="1.5" opacity=".6"/>' for k in range(6)))
    s.add('<path d="M690 740L730 690L742 692L712 744Z" fill="#7a4a1a"/>')
    put(s, monkey_svg, 760, 700, 1.7, color="#3a2414", rim="#ffe8c0", arms="reach", tail=2, flip=True)
    s.add('<path d="M120 900L200 860L240 900Z" fill="#6a4a2a"/><path d="M180 880L260 820" stroke="#3a2a1a" stroke-width="6"/>')
    s.fx("mottle", amp=.03, cell=60)
    s.look = {"vibrance": .12, "vignette": .24}
    return s
