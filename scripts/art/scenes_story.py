"""Story and practice paintings: people, animals and sacred stories.

Silhouettes here are drawn in local units (feet or seat at the origin, facing right) and
placed with a transform. `lit()` wraps any group in a filter that rim-lights the edges
facing a light source, so the same figure can be used by a fire, a lamp or the sun.
"""
import math
import random

import arch
import objects as ob
from land import crown, grass, hills, mountains, peak_line, pine, pines, ribbon, ridgeline, smooth_line, y_at
from paint import H, W, f, mix, pts_d
from scenes import scene


# ---------------------------------------------------------------- light on silhouettes
def rim_filter(s, ang, w=3.0, color="#ffd9a0", a=0.95, blur=0.8, w2=0.0, a2=0.0, color2=None, halo=0.0, halo_a=0.0):
    """A filter that lights the edges of a shape facing direction ang (degrees; 0 = light to the
    right, -90 = light above). w is the rim width in px; w2/a2 add a broad soft half-light that
    models the body; halo adds light bleeding around the outline (for backlit figures)."""
    key = ("rim", round(ang), round(w, 1), color, a, blur, round(w2, 1), a2, color2, halo, halo_a)
    if key in s.cache:
        return s.cache[key]
    i = s.uid("rim")
    lx, ly = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    parts = [f'<filter id="{i}" x="-30%" y="-30%" width="160%" height="160%" color-interpolation-filters="sRGB">',
             f'<feOffset in="SourceAlpha" dx="{-lx * w:.2f}" dy="{-ly * w:.2f}" result="o"/>',
             '<feComposite in="SourceAlpha" in2="o" operator="out" result="r"/>',
             f'<feGaussianBlur in="r" stdDeviation="{blur}" result="rb"/>',
             '<feComposite in="rb" in2="SourceAlpha" operator="in" result="rb2"/>',
             f'<feFlood flood-color="{color}" flood-opacity="{a}"/>',
             '<feComposite in2="rb2" operator="in" result="rim"/>']
    merge = ['<feMergeNode in="SourceGraphic"/>']
    if w2:
        parts += [f'<feOffset in="SourceAlpha" dx="{-lx * w2:.2f}" dy="{-ly * w2:.2f}" result="o2"/>',
                  '<feComposite in="SourceAlpha" in2="o2" operator="out" result="q"/>',
                  f'<feGaussianBlur in="q" stdDeviation="{w2 * .45:.2f}" result="qb"/>',
                  '<feComposite in="qb" in2="SourceAlpha" operator="in" result="qb2"/>',
                  f'<feFlood flood-color="{color2 or color}" flood-opacity="{a2}"/>',
                  '<feComposite in2="qb2" operator="in" result="half"/>']
        merge.append('<feMergeNode in="half"/>')
    if halo:
        parts += [f'<feMorphology in="SourceAlpha" operator="dilate" radius="{halo * .3:.1f}" result="d"/>',
                  f'<feGaussianBlur in="d" stdDeviation="{halo}" result="db"/>',
                  '<feComposite in="db" in2="SourceAlpha" operator="out" result="db2"/>',
                  f'<feFlood flood-color="{color}" flood-opacity="{halo_a}"/>',
                  '<feComposite in2="db2" operator="in" result="glowout"/>']
        merge.insert(0, '<feMergeNode in="glowout"/>')
    merge.append('<feMergeNode in="rim"/>')
    parts.append(f'<feMerge>{"".join(merge)}</feMerge></filter>')
    s.defs.append("".join(parts))
    s.cache[key] = f"url(#{i})"
    return s.cache[key]


def lit(s, svg, ang, **kw):
    """Wrap svg (scene units) in a rim-light filter; see rim_filter."""
    return f'<g filter="{rim_filter(s, ang, **kw)}">{svg}</g>'


def toward(x0, y0, x1, y1):
    """Angle in degrees from (x0, y0) toward (x1, y1)."""
    return math.degrees(math.atan2(y1 - y0, x1 - x0))


def place(x, y, sc, inner, flip=False, rot=0.0):
    sx = -sc if flip else sc
    r = f" rotate({f(rot)})" if rot else ""
    return f'<g transform="translate({f(x)} {f(y)}) scale({f(sx)} {f(sc)}){r}">{inner}</g>'


# ---------------------------------------------------------------- seated figures (profile)
# Seated height about 100 units, seat at the origin, facing right. Built from parts so the
# poses share one anatomy: head with a real profile, neck, torso, crossed legs, near arm.
HEAD = ("M0 -99.5C5 -99.5 8.5 -96 9 -91.5C9.3 -90 9.4 -89 9 -88.2L9 -87.6L11.6 -83"
        "C11.9 -82.4 11.4 -81.9 10.4 -82C10.9 -81.2 10.9 -80.4 10.3 -80C10.8 -79.4 10.6 -78.6 9.9 -78.3"
        "C9.9 -77.4 9.6 -76.4 8.6 -75.8C6.5 -75.2 3 -76 0 -77C-4 -78.5 -8 -80 -10 -83"
        "C-12 -87 -11.5 -95 -7 -98C-5 -99.3 -2.5 -99.6 0 -99.5Z")
NECK = "M-8.5 -84C-7.5 -78 -8 -73 -10.5 -68L5 -66C4 -70 3.6 -73 4.2 -78Z"
TORSO = ("M-10.5 -70C-14.5 -66.5 -17 -62 -17 -55C-17 -47 -15 -40 -14.5 -34C-14 -28 -16 -22 -19 -17"
         "C-24 -12 -24 -3 -20 0L14 0L12 -30C11 -36 11.5 -40 10.5 -45C9.8 -48 10.5 -52 11 -56"
         "C11.5 -61 9 -66 4.5 -68.5Z")
LAP = ("M-18 0C-18 -10 -8 -23 8 -25.5C20 -27 31 -26 39 -23.5C45.5 -21.5 48.8 -17 48.4 -11.5"
       "C48 -7.5 46.6 -5 44.6 -3.8C47 -3.3 48.8 -1.8 48 0Z")
ARMS = {
    "knee": ("M-8 -62C-8 -68 1 -69 2.5 -63C3.5 -58 4.5 -50 4.5 -44C10 -38.5 22 -33 35 -29.5"
             "C39 -29 43 -28 46 -25.5C48 -23.5 48.5 -21 47 -20C44 -20.5 40 -22.5 35.5 -23.5"
             "C22 -26 9 -30 1 -35.5C-3 -37.5 -6.5 -41 -7.5 -47C-8.5 -52 -9 -57 -8 -62Z"),
    "lap": ("M-8 -62C-8 -68 1 -69 2.5 -63C3.5 -58 4.5 -50 4.5 -44C8 -37 14 -32.5 22 -30.5"
            "C26 -30 29 -29 30 -27C29 -25 25 -24.5 21 -25C12 -26 4 -29.5 -1 -34C-5 -37.5 -7 -42 -7.5 -47"
            "C-8.5 -52 -9 -57 -8 -62Z"),
    "anjali": ("M-8 -62C-8 -68 1 -69 2.5 -63C3.5 -58 4 -52 4.5 -48C7.5 -49.5 10.5 -51.5 12.5 -53.5"
               "C13 -58 13.6 -63.5 15 -68C15.8 -70.4 17.8 -70.4 18.2 -68C19 -63.5 19.4 -58 18.6 -53.5"
               "C18 -49.5 15 -46 10.5 -43C5 -39.5 -1.5 -38.5 -5 -41.5C-8 -45 -8.6 -54 -8 -62Z"),
    "teach": ("M-8 -62C-8 -68 1 -69 2.5 -63C3.5 -58 4.5 -51 5 -46.5C8.5 -48.5 11.5 -52 13.5 -56"
              "C14 -60 14 -65 15 -68.5C15.8 -71 17.8 -71.2 18.4 -69C18.8 -66 18.8 -62.5 19.6 -59.5"
              "C21 -58.5 21.6 -57 20.6 -56C19.6 -51 16.5 -45 11 -40.5C5.5 -36.5 -1 -37 -4.5 -40"
              "C-7.5 -44 -8.5 -53 -8 -62Z"),
    "offer": ("M-8 -62C-8 -68 1 -69 2.5 -63C4 -58 6 -52 9 -48C16 -43 26 -38.5 36 -35"
              "C40 -34 44 -33.5 47 -32C49 -31 49.2 -29 47.5 -28.5C44 -28.5 40 -29.5 36 -30"
              "C25 -32 13 -36.5 4 -41C-2 -44 -7 -49 -8 -55Z"),
}
SAGE_HAIR = ("M-6.5 -97.5C-9 -102.5 -5.5 -107.5 -0.5 -107.5C4.5 -107.5 6.5 -103 4 -98.5Z"
             "M-7 -97C-12.5 -94 -13.8 -86 -12.6 -79C-12 -75 -12.8 -71 -14.4 -67.5L-9.5 -70C-8 -74 -8.5 -80 -8 -86Z")
SAGE_BEARD = ("M9.6 -79C11.2 -76 12.2 -71 12 -66C11.8 -62 10.8 -58.6 9.2 -55.8C6.5 -59.5 3 -65 -1 -70.5"
              "C-4 -74.5 -6 -78.5 -4.5 -82C0 -81 5 -80 9.6 -79Z")
YOUTH_HAIR = '<circle cx="-6.2" cy="-98.6" r="2.4"/><path d="M-7.5 -97.5C-10 -97 -12 -95 -12.8 -92.5C-11 -93.6 -9.4 -94.4 -7 -95Z"/>'


def seated_side(kind="sage", hands="knee", color="#0c0a12", extra=""):
    """A cross-legged figure in profile facing right (local units, seat at 0,0).
    kind: 'sage' (hair knot, long beard), 'youth' (shaven head with a shikha, slimmer) or
    'plain' (short hair). hands: 'knee' (resting on the knee), 'lap' (dhyana mudra),
    'anjali' (palms joined), 'teach' (hand raised in chin mudra) or 'offer' (reaching forward)."""
    body = f'<path d="{NECK}"/><path d="{TORSO}"/><path d="{LAP}"/><path d="{ARMS[hands]}"/>'
    if kind == "sage":
        inner = f'{body}<path d="{HEAD}"/><path d="{SAGE_HAIR}"/><path d="{SAGE_BEARD}"/>'
    elif kind == "youth":
        inner = (f'<g transform="scale(.9 .93)">{body}</g>'
                 f'<g transform="translate(-0.6 5.2) scale(1.03)"><path d="{HEAD}"/>{YOUTH_HAIR}</g>')
    else:
        inner = f'{body}<path d="{HEAD}"/><path d="M-8 -96C-12.5 -92 -13 -85 -11 -79.5L-8 -84Z"/>'
    return f'<g fill="{color}">{inner}{extra}</g>'


def ladle(x0, y0, x1, y1, color, w=1.6):
    """A long sacrificial ladle (sruva) from the hand at (x0, y0) to its bowl at (x1, y1)."""
    a = math.atan2(y1 - y0, x1 - x0)
    return (f'<path d="M{f(x0)} {f(y0)}L{f(x1)} {f(y1)}" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<ellipse cx="{f(x1 + math.cos(a) * 2.5)}" cy="{f(y1 + math.sin(a) * 2.5)}" rx="4" ry="2.2" fill="{color}" '
            f'transform="rotate({math.degrees(a):.0f} {f(x1 + math.cos(a) * 2.5)} {f(y1 + math.sin(a) * 2.5)})"/>')


# ---------------------------------------------------------------- shape helpers
def _hull(points):
    pts = sorted(set((round(x, 2), round(y, 2)) for x, y in points))

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def blob(*circles, n=20):
    """The convex hull of circles (x, y, r): a smooth capsule or rounded mass."""
    pts = []
    for x, y, r in circles:
        pts += [(x + math.cos(2 * math.pi * k / n) * r, y + math.sin(2 * math.pi * k / n) * r) for k in range(n)]
    return pts_d(_hull(pts))


def limb(*circles):
    """A tapered limb through joints (x, y, r): consecutive capsules."""
    return "".join(blob(a, b) for a, b in zip(circles, circles[1:]))


def _pt(p, L, ang):
    """Point at distance L from p at angle ang (degrees from straight down, + forward/right)."""
    a = math.radians(ang)
    return (p[0] + math.sin(a) * L, p[1] + math.cos(a) * L)


# ---------------------------------------------------------------- walking and standing people
def person(dress="dhoti", stride=0.0, lean=0.0, head=0.0, arm=(10, -20), arm2=None, prop=None,
           color="#0c0a12", scale_w=1.0, hair="short", age="adult"):
    """A standing or walking person in profile facing right; feet at the origin, about 100 tall.
    stride (degrees) swings the legs apart; lean tips the body forward; head bows the head;
    arm/arm2 = (upper, fore) angles from straight down for the near and far arms (+ forward).
    dress: 'dhoti' (kurta and dhoti), 'sari', 'robe' (a renunciate's robe), 'child'.
    hair: 'short', 'bun', 'shikha', 'shawl' (head covered) or 'jata'. prop: 'staff', 'books',
    'plate', 'pot' or None. Returns (svg, hand) where hand is the near hand in local units."""
    sw = scale_w
    hip = (0.0, -50.0)
    legs = []
    for sgn in (1, -1):  # near leg forward when stride > 0
        a = stride * sgn
        bend = 5 + (7 if sgn < 0 and stride else 0)
        knee = _pt(hip, 25, a)
        ankle = _pt(knee, 24, a - bend)
        legs.append((knee, ankle))
    # feet planted: shift so the lowest ankle sits at -3.5
    low = max(legs[0][1][1], legs[1][1][1])
    dy = -3.5 - low
    hip = (hip[0], hip[1] + dy)
    legs = [((k[0], k[1] + dy), (a_[0], a_[1] + dy)) for k, a_ in legs]
    top = _pt(hip, 31, 180 - lean)
    sh = _pt(hip, 27.5, 180 - lean)
    sh = (sh[0] - 1.0, sh[1])
    neck = _pt(top, 3.5, 180 - lean * 1.3 - head * .4)
    hc = _pt(neck, 7.4, 180 - lean * 1.3 - head)
    out = []
    # far arm first (behind the body)
    if arm2:
        el = _pt(sh, 16.5, arm2[0])
        wr = _pt(el, 14.5, arm2[1])
        out.append(f'<path d="{limb((sh[0], sh[1], 3.4 * sw), (el[0], el[1], 2.5 * sw), (wr[0], wr[1], 2.0 * sw))}" opacity=".92"/>')
    # legs and feet
    leg_r = (5.8, 4.0, 2.5) if dress != "dhoti" else (6.6, 5.4, 4.0)
    if age == "child":
        leg_r = (5.0, 3.6, 2.4)
    for (knee, ankle) in legs:
        out.append(f'<path d="{limb((hip[0], hip[1], leg_r[0] * sw), (knee[0], knee[1], leg_r[1] * sw), (ankle[0], ankle[1], leg_r[2] * sw))}"/>')
        out.append(f'<path d="M{f(ankle[0] - 2.6)} {f(ankle[1] - 1)}C{f(ankle[0] - 3.2)} {f(ankle[1] + 3.6)} {f(ankle[0])} {f(ankle[1] + 3.6)} {f(ankle[0] + 3)} {f(ankle[1] + 3.6)}'
                   f'L{f(ankle[0] + 7.5)} {f(ankle[1] + 3.6)}C{f(ankle[0] + 8.6)} {f(ankle[1] + 3.2)} {f(ankle[0] + 8)} {f(ankle[1] + 1.4)} {f(ankle[0] + 6)} {f(ankle[1] + 1)}'
                   f'L{f(ankle[0] + 2)} {f(ankle[1] - 1.6)}Z"/>')
    # torso: chest, waist and hips
    chest = _pt(hip, 21, 180 - lean)
    waist = _pt(hip, 11, 180 - lean)
    out.append(f'<path d="{blob((chest[0] + .8, chest[1], 6.9 * sw), (waist[0] - .3, waist[1], 5.6 * sw), (hip[0] - .8, hip[1], 6.6 * sw), (top[0] - .5, top[1] + 2.5, 5 * sw))}"/>')
    out.append(f'<path d="{limb((top[0], top[1] + 2, 3.0), (hc[0] - 1, hc[1] + 4, 2.7))}"/>')
    # clothing
    fk, bk = legs[0][1], legs[1][1]
    xs = sorted([fk[0], bk[0]])
    if dress == "sari":
        out.append(f'<path d="{blob((waist[0], waist[1], 6.2 * sw), (hip[0], hip[1] + 2, 7.6 * sw), (xs[0] - 1.5, -4.2, 3.2), (xs[1] + 2.5, -4.2, 3.4))}"/>'
                   f'<path d="M{f(xs[0] - 4)} -3.5L{f(xs[1] + 5.5)} -3.5L{f(xs[1] + 6)} -1.2L{f(xs[0] - 4.5)} -1.2Z"/>')
        # pallu: over the left shoulder and down the back
        p0 = _pt(sh, 3, 180)
        out.append(f'<path d="M{f(p0[0] + 3)} {f(p0[1] - 1)}C{f(p0[0] - 6)} {f(p0[1] - 1)} {f(p0[0] - 11)} {f(p0[1] + 10)} {f(p0[0] - 12.5)} {f(p0[1] + 30)}'
                   f'L{f(p0[0] - 6)} {f(p0[1] + 31)}C{f(p0[0] - 6)} {f(p0[1] + 18)} {f(p0[0] - 3)} {f(p0[1] + 8)} {f(p0[0] + 1)} {f(p0[1] + 3)}Z"/>')
    elif dress == "robe":
        out.append(f'<path d="{blob((chest[0] + 1, chest[1], 7.4 * sw), (hip[0], hip[1] + 4, 7.8 * sw), (xs[0] - 1, -5, 3.4), (xs[1] + 2, -5, 3.4))}"/>')
    elif dress in ("dhoti", "child"):
        kurta_y = hip[1] + (12 if dress == "dhoti" else 6)
        out.append(f'<path d="{blob((chest[0] + 1, chest[1], 7.3 * sw), (hip[0] - .5, hip[1], 7.4 * sw), (hip[0] - 3.5, kurta_y, 5.6 * sw), (hip[0] + 3.5, kurta_y, 5.6 * sw))}"/>')
    # near arm
    el = _pt(sh, 16.5, arm[0])
    wr = _pt(el, 14.5, arm[1])
    out.append(f'<path d="{limb((sh[0], sh[1], 3.7 * sw), (el[0], el[1], 2.7 * sw), (wr[0], wr[1], 2.1 * sw))}"/>')
    ha = math.radians(arm[1])
    hand = (wr[0] + math.sin(ha) * 3.5, wr[1] + math.cos(ha) * 3.5)
    out.append(f'<ellipse cx="{f(hand[0])}" cy="{f(hand[1])}" rx="2.4" ry="3.6" transform="rotate({f(-arm[1])} {f(hand[0])} {f(hand[1])})"/>')
    # head with a real profile (HEAD is 23 units tall; scale it to about 13.5)
    hs = .6 if age != "child" else .66
    tilt = lean * 1.3 + head
    hg = f'<g transform="translate({f(hc[0])} {f(hc[1])}) rotate({f(tilt)}) scale({hs}) translate(0 88)"><path d="{HEAD}"/>'
    if hair == "bun":
        hg += '<circle cx="-10.5" cy="-86" r="5.8"/><path d="M-11 -96C-13 -92 -13 -86 -11.5 -82L-8 -84Z"/>'
    elif hair == "shikha":
        hg += YOUTH_HAIR
    elif hair == "shawl":
        hg += '<path d="M2 -103C-8 -104 -14 -98 -15 -88C-16 -78 -16 -70 -18 -60L-6 -66C-6 -74 -5 -80 -4 -84C-1 -90 4 -94 9 -96C8 -100 6 -102 2 -103Z"/>'
    elif hair == "jata":
        hg += SAGE_HAIR + SAGE_BEARD
    else:
        hg += '<path d="M-8 -96C-12.5 -92 -13 -85 -11 -79.5L-8 -84Z"/>'
    hg += "</g>"
    out.append(hg)
    if prop == "staff":
        out.append(f'<path d="M{f(hand[0] + 1)} {f(hand[1] - 16)}L{f(hand[0] + 7)} -0.5" stroke="{color}" stroke-width="1.8" stroke-linecap="round"/>')
    elif prop == "books":
        out.append(f'<rect x="{f(hand[0] - 7)}" y="{f(hand[1] - 9)}" width="10" height="13" rx="1" transform="rotate(-12 {f(hand[0])} {f(hand[1])})"/>')
    elif prop == "pot":
        out.append(f'<path d="M{f(hand[0])} {f(hand[1])}V{f(hand[1] + 4)}M{f(hand[0] - 4)} {f(hand[1] + 9)}C{f(hand[0] - 5)} {f(hand[1] + 4)} {f(hand[0] + 5)} {f(hand[1] + 4)} {f(hand[0] + 4)} {f(hand[1] + 9)}'
                   f'C{f(hand[0] + 6)} {f(hand[1] + 14)} {f(hand[0] - 6)} {f(hand[1] + 14)} {f(hand[0] - 4)} {f(hand[1] + 9)}Z" stroke="{color}" stroke-width="1.2"/>')
    elif prop == "plate":
        out.append(f'<ellipse cx="{f(hand[0] + 2)}" cy="{f(hand[1] - 2)}" rx="7" ry="1.6"/>')
    return f'<g fill="{color}">{"".join(out)}</g>', hand


def _mirror(half):
    """A symmetric closed path from its right half [(x, y) or ('C', c1, c2, p)] listed top to bottom."""
    def seg(items, sgn):
        out = []
        for it in items:
            if it[0] == "C":
                (a, b), (c, d), (e, g) = it[1:]
                out.append(f"C{f(a * sgn)} {f(b)} {f(c * sgn)} {f(d)} {f(e * sgn)} {f(g)}")
            else:
                out.append(f"L{f(it[0] * sgn)} {f(it[1])}")
        return out
    start = half[0]
    right = seg(half[1:], 1)
    # walk back up the left side: reverse the segments
    rev = []
    pts = [start] + [it[3] if it[0] == "C" else it for it in half[1:]]
    for k in range(len(half) - 1, 0, -1):
        it = half[k]
        p0 = pts[k - 1]
        if it[0] == "C":
            rev.append(("C", it[2], it[1], p0))
        else:
            rev.append(p0)
    left = seg(rev, -1)
    return f"M{f(start[0])} {f(start[1])}" + "".join(right) + "".join(left) + "Z"


# A devotee seen from behind, hands joined in front (so the elbows stand out); 100 units tall.
BACK_MAN = _mirror([(0, -99), ("C", (4, -99), (6.6, -95.5), (6.6, -91)), ("C", (6.6, -87), (5, -84.5), (3.6, -83.2)),
                    (3.4, -81.6), ("C", (5, -80.4), (8.5, -79.8), (11, -78.6)), ("C", (13.6, -77.4), (14.6, -74.5), (14.6, -71)),
                    ("C", (14.8, -67), (15.6, -63.5), (16, -60.5)), ("C", (16.2, -58), (14.5, -56.5), (11.5, -57)),
                    ("C", (10.5, -53), (11, -49), (11.6, -45)), ("C", (12, -30), (11.5, -15), (11, 0)), (0, 0)])
BACK_WOMAN = _mirror([(0, -97), ("C", (3.8, -97), (6.2, -93.6), (6.2, -89.4)), ("C", (6.2, -85.6), (4.8, -83.2), (3.4, -82)),
                      (3.2, -80.6), ("C", (4.6, -79.6), (7.6, -79), (9.8, -78)), ("C", (12.2, -77), (13, -74.5), (13, -71)),
                      ("C", (13.2, -67), (14, -63.5), (14.4, -60.5)), ("C", (14.6, -58), (13, -56.5), (10.2, -57)),
                      ("C", (9.2, -54), (9.4, -50), (10.6, -46)), ("C", (12.5, -30), (14, -15), (15, 0)), (0, 0)])
BACK_VEILED = _mirror([(0, -100), ("C", (5, -100), (8, -96), (8.2, -90)), ("C", (8.4, -85), (8.8, -82), (10.5, -79.5)),
                       ("C", (12.8, -77), (14.2, -74), (14.4, -70)), ("C", (14.8, -66), (15.6, -63), (16, -60)),
                       ("C", (16.2, -57.5), (14.6, -56), (11.5, -56.5)), ("C", (10.5, -53), (11, -49), (12, -45)),
                       ("C", (13.5, -30), (14.5, -15), (15.5, 0)), (0, 0)])
# A meditator in lotus seen from behind: rounded head, sloping shoulders, elbows, wide knees.
BACK_SEATED = _mirror([(0, -100), ("C", (5.6, -100), (8.6, -95.5), (8.6, -89)), ("C", (8.6, -83.5), (6.6, -79.5), (5, -77.8)),
                       (5, -74.6), ("C", (8.5, -73), (14, -72), (17.6, -70)), ("C", (20.6, -68.3), (21.8, -65), (21.8, -61)),
                       ("C", (22.2, -54), (23.4, -47), (24.2, -41)), ("C", (24.8, -36), (26.6, -31), (29, -27)),
                       ("C", (33, -22), (40, -20.5), (44.5, -15)), ("C", (47.5, -11), (47, -3), (42, 0)), (0, 0)])


def back_person(kind="man", color="#0c0a12", extra=""):
    d = {"man": BACK_MAN, "woman": BACK_WOMAN, "veiled": BACK_VEILED, "seated": BACK_SEATED}[kind]
    hair = ""
    if kind == "woman":
        hair = '<path d="M-2.6 -84C-3.2 -76 -2.6 -64 -1.6 -52C-1 -50 1 -50 1.6 -52C2.6 -64 3.2 -76 2.6 -84Z"/><circle cx="0" cy="-50.5" r="1.8"/>'
    elif kind == "seated":
        hair = '<ellipse cx="0" cy="-100.5" rx="4.6" ry="3.6"/>'
    return f'<g fill="{color}"><path d="{d}"/>{hair}{extra}</g>'


# ---------------------------------------------------------------- horse (profile, facing right)
# Withers 100 units above the ground at the origin; nose about 90 units ahead of the centre.
HORSE = ("M-50 -94C-42 -100 -28 -100.5 -14 -96.5C-2 -93.5 10 -95 20 -100C28 -106 38 -120 46 -132"
         "C51 -139 56 -145 61 -148C60.5 -152 61.5 -155.5 63 -157C64.5 -154.5 65.5 -151 65.5 -148"
         "C68 -146 71 -143 73 -139C78 -130 85 -118 89.5 -110C91.5 -106.5 91 -103 88.5 -101.5"
         "C87 -100.5 85.5 -100.5 84.5 -101.5C83.5 -100.5 81.5 -100.5 80.5 -102C77 -104 73 -106.5 69.5 -109.5"
         "C65 -112 61 -114 60 -119C59 -121 58 -121.5 57 -120C53 -110 51 -97 52 -86C53 -80 52.5 -74 49.5 -69"
         "C47.5 -65 46.5 -60 46.5 -54C46.5 -46 45.5 -38 46 -32C46.5 -28 46 -23 46 -17C46 -12 47 -9 48.5 -6.5"
         "C49.5 -4.5 51 -2 51.5 0L41.5 0C41.5 -2.5 41 -4.5 40.5 -6.5C40 -9.5 39.5 -12.5 39.5 -17"
         "C39.5 -23 39 -28 39.3 -32C39.3 -40 38 -48 36.5 -55C35.5 -58.5 33 -60.5 29.5 -61"
         "C15 -58 -5 -57.5 -21 -62C-23 -56 -24 -50 -26.5 -44C-29 -38 -33 -34 -35.5 -30"
         "C-36.5 -25 -36 -19 -35.5 -15C-35 -11 -34 -8 -32.5 -6C-31.5 -4 -30.5 -2 -30 0L-39.5 0"
         "C-39.7 -2 -40 -4 -40.6 -6.2C-41.4 -9.5 -41.8 -13 -41.8 -17.5C-41.8 -23 -42.6 -27 -44.5 -31"
         "C-46.5 -35 -47.5 -44 -48.5 -54C-49.5 -64 -52 -73 -54.5 -80C-55.5 -86 -54 -91 -50 -94Z")
HORSE_FAR = (limb((33, -60, 6.5), (36, -45, 5), (37, -31, 3.9), (38, -9, 3.2)) +
             "M33.8 -9L41 -8C42 -5 43 -2 43.5 0H33.8C33.8 -3 33.7 -6 33.8 -9Z" +
             limb((-28, -62, 9), (-36, -44, 5.5), (-43, -31, 3.9), (-38, -8, 3.2)) +
             "M-42 -8L-35 -8C-34 -5 -33 -2 -32.5 0H-42C-42 -3 -42.1 -6 -42 -8Z")
HORSE_MANE = ("M61 -148C55 -144 48 -135 42 -125C36 -115 28 -106 20 -100C28 -99 35 -104 41 -111"
              "C46 -118 51 -127 55 -135C58 -140 61 -144 63.5 -147Z"
              "M65.5 -148C68.5 -145 71 -141 71.5 -136C68 -139 66 -142 64.5 -145Z")
HORSE_TAIL = "M-49 -95C-60 -95 -65 -84 -65.5 -70C-66 -55 -63 -40 -67 -24C-60 -30 -57 -45 -56.5 -60C-56 -74 -54 -86 -47 -90Z"


def horse(body="#e8e2ea", shade="#8f86a8", dark="#2a2236", s=None, harness="#b8862e", plume="#c8342a", far=None):
    """A standing horse in profile facing right. With a Scene, the body is modelled with a
    gradient from body (top) to shade (belly), otherwise it is a flat silhouette in body."""
    fill = s.lin([(0, body, 1), (.55, mix(body, shade, .45), 1), (1, shade, 1)], 0, -150, 0, 0, user=True) if s else body
    farc = far or mix(shade, dark, .45)
    out = [f'<path d="{HORSE_FAR}" fill="{farc}"/>', f'<path d="{HORSE_TAIL}" fill="{mix(body, shade, .3)}"/>',
           f'<path d="{HORSE}" fill="{fill}"/>', f'<path d="{HORSE_MANE}" fill="{mix(body, "#ffffff", .3)}"/>']
    # shadowed underside of the neck and belly, and the near legs below the knee
    if s:
        out.append(f'<g clip-path="{s.clip(HORSE)}"><ellipse cx="0" cy="-48" rx="70" ry="16" fill="{shade}" opacity=".55" filter="{s.blur(6)}"/>'
                   f'<path d="M54 -84C52 -96 53 -110 58 -120L66 -112C62 -104 60 -94 58 -84Z" fill="{shade}" opacity=".35" filter="{s.blur(3)}"/></g>')
    out.append('<ellipse cx="72.5" cy="-131.5" rx="2" ry="1.5" fill="#140e18" transform="rotate(50 72.5 -131.5)"/><ellipse cx="87" cy="-106" rx="1.6" ry="1.1" fill="#3a2a30"/>')
    if harness:
        out.append(f'<path d="M64 -142C68 -134 74 -124 80 -112M70 -129L82 -116M71 -120C76 -117 80 -112 83 -106" stroke="{harness}" stroke-width="1.6" fill="none"/>'
                   f'<path d="M51 -74C44 -68 36 -64 28 -66" stroke="{harness}" stroke-width="3" fill="none"/>'
                   f'<path d="M24 -100C26 -88 28 -76 28 -64" stroke="{harness}" stroke-width="3.2" fill="none"/>')
    if plume:
        out.append(f'<path d="M63 -150C60 -160 62 -170 68 -176C67 -168 68 -160 66 -150Z" fill="{plume}"/>')
    return "".join(out)


# ---------------------------------------------------------------- elephant (profile, facing right)
# Shoulder about 100 units high; the twin domes of the head are the highest point.
ELEPHANT = ("M-66 -86C-62 -96 -50 -106 -32 -111C-15 -115 5 -114 20 -110C28 -108 34 -107 40 -110"
            "C44 -118 52 -128 62 -129C68 -130 72 -127 75 -124C80 -128 88 -125 91 -117"
            "C95 -108 96 -98 95 -90C95 -74 98 -56 98 -40C98 -27 102 -17 108 -13C112 -10 112 -4 107 -4"
            "C101 -4 95 -9 92 -18C89 -28 87 -42 86 -56C85 -64 82 -70 78 -73C76 -71 73 -70 71 -72"
            "C69 -75 67 -76 65 -74C60 -70 57 -66 55 -58C54 -45 54 -25 55 -8C55.5 -3 57 -1 59 0L36 0"
            "C37 -3 38 -6 38 -12C38 -30 38 -46 36 -54C30 -50 10 -46 -10 -47C-20 -48 -28 -50 -34 -54"
            "C-35 -40 -36 -24 -36 -10C-36 -4 -35 -1 -33 0L-57 0C-58 -3 -58.5 -7 -58 -12"
            "C-58 -22 -59 -32 -61 -42C-63 -52 -66 -62 -67 -72C-67.5 -78 -67 -83 -66 -86Z")
ELEPHANT_EAR = ("M54 -119C46 -119 37 -112 34 -100C31 -89 34 -79 40 -73C44 -69 50 -69 54 -73"
                "C58 -79 58 -88 57 -96C56.5 -104 57 -112 54 -119Z")
ELEPHANT_FAR = ("M38 -60H56C56 -40 56 -20 57 -6C57.5 -2 58.5 0 60 0H40C40.5 -6 40 -30 38 -60Z"
                "M-50 -60H-32C-32 -40 -31 -20 -30 -6C-30 -2 -29 0 -27 0H-48C-48 -20 -49 -40 -50 -60Z")
ELEPHANT_TUSK = "M70 -75C78 -73 90 -69 100 -63C102.5 -61.6 102 -59.6 99.5 -60.2C90 -63 80 -66.5 70 -69.5Z"
ELEPHANT_TAIL = "M-66.5 -84C-69 -74 -70 -60 -70.5 -46L-68.8 -46C-68 -60 -67 -72 -64.5 -82Z"


def temple_elephant(s, body="#5a5262", shade="#221d2a", cloth="#9e1f2a", gold="#e2b04a"):
    """An adorned temple elephant in profile facing right: a gold forehead plate (nettipattam),
    a caparison with a gold border and tassels, a rope of bells and belled anklets."""
    fill = s.lin([(0, body, 1), (.6, mix(body, shade, .5), 1), (1, shade, 1)], 0, -130, 0, 0, user=True)
    gg = s.lin([(0, "#fff0b8", 1), (.35, gold, 1), (.7, "#a86e1c", 1), (1, "#5a3608", 1)], 0, 0, 1, 1)
    out = [f'<path d="{ELEPHANT_FAR}" fill="{mix(shade, "#000000", .35)}"/>',
           f'<path d="{ELEPHANT_TAIL}" fill="{shade}"/><path d="M-71.5 -48L-67.5 -48L-68 -38L-70.5 -37Z" fill="{shade}"/>',
           f'<path d="{ELEPHANT}" fill="{fill}"/>']
    clip = s.clip(ELEPHANT)
    # skin: belly shadow, trunk wrinkles, leg creases, a little texture
    wr = "".join(f"M{f(86.5 + k * .25)} {f(-80 + k * 5)}Q{f(91 + k * .3)} {f(-78.5 + k * 5)} {f(96 + k * .2)} {f(-80 + k * 5)}" for k in range(12))
    legs = "".join(f"M{f(x0)} {f(y)}Q{f(x0 + 9)} {f(y + 1.6)} {f(x0 + 18)} {f(y)}" for x0 in (37, -57) for y in (-26, -21, -16))
    out.append(f'<g clip-path="{clip}"><ellipse cx="0" cy="-40" rx="80" ry="16" fill="{shade}" opacity=".6" filter="{s.blur(6)}"/>'
               f'<path d="{wr}{legs}" stroke="{shade}" stroke-opacity=".55" stroke-width=".9" fill="none"/>'
               f'<rect x="-80" y="-140" width="190" height="150" fill="{body}" filter="{s.grain(.35, 3, .2, 5, "#000000")}" opacity=".25"/></g>')
    # bell rope round the neck (behind the ear)
    out.append(f'<path d="M41 -110C38 -96 40 -80 50 -66" stroke="#6a3a1a" stroke-width="2.4" fill="none"/>')
    out.append(f'<path d="{ELEPHANT_EAR}" fill="{mix(body, shade, .25)}"/>'
               f'<path d="M54 -119C46 -119 37 -112 34 -100C31 -89 34 -79 40 -73" stroke="{mix(body, "#ffffff", .12)}" stroke-width="1.2" fill="none" opacity=".7"/>'
               f'<path d="M50 -110C45 -104 43 -94 45 -84" stroke="{shade}" stroke-opacity=".5" stroke-width="1" fill="none"/>')
    # caparison over the back, scalloped hem with tassels
    hem = []
    x = 31.0
    while x > -46:
        hem.append(f"Q{f(x - 3.6)} {f(-71.5)} {f(x - 7.2)} {f(-76)}")
        x -= 7.2
    cl = f"M-46 -104C-32 -112.5 -14 -116.5 5 -115.5C16 -115 25 -112.5 31 -110L31 -76{''.join(hem)}L-46 -104Z"
    cg = s.lin([(0, mix(cloth, "#ff8060", .25), 1), (1, mix(cloth, "#200008", .45), 1)], 0, -116, 0, -72, user=True)
    out.append(f'<path d="{cl}" fill="{cg}"/>')
    out.append(f'<g clip-path="{s.clip(cl)}"><path d="M-50 -82H35M27 -112V-70" stroke="{gold}" stroke-width="4" fill="none"/>'
               f'<path d="M-50 -88H35" stroke="{gold}" stroke-width="1" stroke-dasharray="2 3" fill="none"/>'
               + "".join(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="2.2" fill="{gold}" opacity=".85"/>' for cx in range(-34, 26, 12) for cy in (-102, -94) if cy > -112 + abs(cx) * .0)
               + '</g>')
    tass = "".join(f'<path d="M{f(31 - 7.2 * k)} -76V-69" stroke="{gold}" stroke-width="1"/><circle cx="{f(31 - 7.2 * k)}" cy="-68" r="1.6" fill="{gold}"/>' for k in range(11))
    out.append(tass)
    # girth chain with small bells
    out.append(f'<path d="M24 -112C26 -96 28 -80 30 -52" stroke="{gold}" stroke-width="1.6" stroke-dasharray="2.4 1.4" fill="none"/>')
    # forehead plate (nettipattam) along the brow and trunk, with bosses and drops
    nt = ("M82 -127C88 -128 92.5 -124 94 -117C97.5 -108 98 -98 97 -90C96 -78 94.6 -66 95 -56"
          "L91 -48C88 -58 87 -73 87 -87C87 -100 86 -112 82 -127Z")
    out.append(f'<path d="{nt}" fill="{gg}"/>'
               + "".join(f'<circle cx="{f(91.5 + (k % 2) * .6)}" cy="{f(-120 + k * 8)}" r="{f(2.4 - k * .1)}" fill="#fff4c8" opacity=".8"/>' for k in range(9))
               + "".join(f'<path d="M{f(87.6 - k * .05)} {f(-112 + k * 7)}l-2 2.6l1 2.4z" fill="{gold}"/>' for k in range(9)))
    # eye, mouth, tusk
    out.append('<path d="M77 -105C78.5 -106.8 81 -106.8 82 -105C80.5 -103.8 78.5 -103.8 77 -105Z" fill="#100a0c"/>'
               f'<path d="M76.5 -107.5C78.5 -109.5 81.5 -109.5 83 -107.5" stroke="{shade}" stroke-width=".8" fill="none"/>')
    out.append(f'<path d="{ELEPHANT_TUSK}" fill="{s.lin([(0, "#fff8e8", 1), (1, "#c8b08a", 1)], 0, 0, 0, 1)}"/>')
    # neck bells, anklets
    for bx, by, bs in ((51, -64, 1.0), (45, -74, .7)):
        out.append(f'<path d="M{f(bx - 4.5 * bs)} {f(by + 9 * bs)}C{f(bx - 4.5 * bs)} {f(by + 2 * bs)} {f(bx - 3 * bs)} {f(by)} {f(bx)} {f(by)}'
                   f'C{f(bx + 3 * bs)} {f(by)} {f(bx + 4.5 * bs)} {f(by + 2 * bs)} {f(bx + 4.5 * bs)} {f(by + 9 * bs)}Z" fill="{gg}"/>'
                   f'<circle cx="{f(bx)}" cy="{f(by + 9.6 * bs)}" r="{f(1.3 * bs)}" fill="#5a3608"/>')
    for x0, x1 in ((36.5, 55.5), (-57.5, -35.5)):
        out.append(f'<path d="M{f(x0)} -11Q{f((x0 + x1) / 2)} -8.5 {f(x1)} -11" stroke="{gold}" stroke-width="2.6" fill="none"/>'
                   + "".join(f'<circle cx="{f(x0 + (x1 - x0) * t)}" cy="{f(-7.2 - 2.2 * (1 - abs(t - .5) * 2) * .5)}" r="1.4" fill="{gold}"/>' for t in (.15, .38, .62, .85)))
    return "".join(out)


# ---------------------------------------------------------------- trees
def branches(x, y, ang, length, width, depth, rng, segs, tips, spread=30, shrink=0.74, bend=8, kids=(2, 3)):
    """Grow a tapering branch system; segs collects limb paths, tips the twig ends."""
    a2 = ang + rng.uniform(-bend, bend)
    xm, ym = x + math.sin(math.radians(ang)) * length * .5, y - math.cos(math.radians(ang)) * length * .5
    x2, y2 = xm + math.sin(math.radians(a2)) * length * .5, ym - math.cos(math.radians(a2)) * length * .5
    segs.append(limb((x, y, width / 2), (xm, ym, width * .44), (x2, y2, width * .36)))
    if depth == 0 or width < 1.4:
        tips.append((x2, y2, length))
        return
    n = rng.randint(*kids)
    for k in range(n):
        off = spread * (k - (n - 1) / 2) / max(1, (n - 1) / 2) if n > 1 else 0
        branches(x2, y2, a2 + off + rng.uniform(-8, 8), length * rng.uniform(shrink - .08, shrink + .06),
                 width * rng.uniform(.6, .74), depth - 1, rng, segs, tips, spread, shrink, bend, kids)


def canopy(tips, r=(30, 60), seed=1, k=2, squash=0.8):
    rng = random.Random(seed)
    d = []
    for (x, y, L) in tips:
        for _ in range(k):
            d.append(crown(x + rng.uniform(-20, 20), y + rng.uniform(-14, 10), rng.uniform(*r), seed=rng.randint(0, 999), lobes=rng.randint(7, 11), bump=.22))
    return "".join(d)


def foliage(blobs, seed=1, fine=14, fr=(9, 20)):
    """Leafy masses: each blob (x, y, r) is a broad crown whose edge is broken up by small
    leaf clusters, so the canopy reads as leaves rather than cloud."""
    rng = random.Random(seed)
    d = []
    for x, y, r in blobs:
        d.append(crown(x, y, r * .82, seed=rng.randint(0, 999), lobes=9, bump=.12))
        for _ in range(fine):
            a = rng.uniform(0, 2 * math.pi)
            rr = r * rng.uniform(.7, .98)
            d.append(crown(x + math.cos(a) * rr, y + math.sin(a) * rr * .82, rng.uniform(*fr) * r / 80, seed=rng.randint(0, 999), lobes=7, bump=.3))
    return "".join(d)


# ---------------------------------------------------------------- peacock feather and flute
def peacock_feather(s, L=420, seed=3):
    """A peacock tail feather lying along +x from the quill (0, 0); the eye is near x = L - 50."""
    rng = random.Random(seed)
    ex = L - 52
    out = []
    # vane: fine bronze-green barbs, longest just below the eye
    barbs = {"#6f8a34": [], "#3d6e3e": [], "#a8913c": []}
    for k in range(150):
        t = k / 149
        x = 40 + t * (ex - 70)
        reach = 10 + 46 * math.sin(min(1, t * 1.1) * math.pi * .55) ** 1.3
        for side in (-1, 1):
            ang = math.radians(rng.uniform(38, 58))
            l = reach * rng.uniform(.75, 1.05)
            x2 = x + math.cos(ang) * l * .9
            y2 = side * math.sin(ang) * l
            c = rng.choice(list(barbs))
            barbs[c].append(f"M{f(x)} 0Q{f(x + l * .25)} {f(y2 * .55)} {f(x2)} {f(y2 + side * rng.uniform(0, 4))}")
    for c, ds in barbs.items():
        out.append(f'<path d="{"".join(ds)}" stroke="{c}" stroke-width=".9" fill="none" opacity=".75"/>')
    # filaments radiating round the eye
    fil = []
    for k in range(70):
        a = math.radians(-150 + 300 * k / 69 + rng.uniform(-2, 2))
        r0, r1 = 30, rng.uniform(52, 66)
        fil.append(f"M{f(ex + math.cos(a) * r0)} {f(math.sin(a) * r0 * .8)}Q{f(ex + math.cos(a) * r1 * .8)} {f(math.sin(a) * r1 * .7)} {f(ex + math.cos(a) * r1)} {f(math.sin(a) * r1 * .78)}")
    out.append(f'<path d="{"".join(fil)}" stroke="#8fa63c" stroke-width="1" fill="none" opacity=".7"/>')
    # the eye: nested rings, inner ones drawn toward the quill
    rings = [(0, 44, 34, "#c7a63c"), (-3, 38, 29, "#5aa86a"), (-6, 31, 24, "#2f7f6a"), (-8, 26, 19.5, "#8a5a28"),
             (-10, 21, 16, "#2fb3b8")]
    for dx, rx, ry, c in rings:
        out.append(f'<ellipse cx="{f(ex + dx)}" cy="0" rx="{rx}" ry="{ry}" fill="{c}"/>')
    heart = (f"M{f(ex - 26)} 0C{f(ex - 24)} -10 {f(ex - 14)} -14 {f(ex - 6)} -12C{f(ex + 2)} -10 {f(ex + 4)} -4 {f(ex + 1)} 0"
             f"C{f(ex + 4)} 4 {f(ex + 2)} 10 {f(ex - 6)} 12C{f(ex - 14)} 14 {f(ex - 24)} 10 {f(ex - 26)} 0Z")
    hg = s.rad([(0, "#3a5ad8", 1), (.6, "#1a2a90", 1), (1, "#0a124a", 1)], .4, .4, .7)
    out.append(f'<path d="{heart}" fill="{hg}"/>')
    out.append(f'<ellipse cx="{f(ex - 14)}" cy="-4" rx="5" ry="2.6" fill="#8ab0ff" opacity=".45"/>')
    # iridescent sheen and the quill
    out.append(f'<ellipse cx="{f(ex - 2)}" cy="-14" rx="26" ry="8" fill="#e8ffd8" opacity=".18" filter="{s.blur(3)}"/>')
    out.append(f'<path d="M20 0Q{f(L * .5)} -2 {f(ex - 26)} 0" stroke="#b8a888" stroke-width="2" fill="none" stroke-linecap="round" opacity=".85"/>'
               f'<path d="M0 .6Q10 .6 20 0" stroke="#d8ccb0" stroke-width="2.6" stroke-linecap="round" fill="none"/>')
    return "".join(out)


def bansuri(s, L=520, r=9.5, tassel=True):
    """A bamboo flute (bansuri) along +x from (0, 0), lit from above, with silk bindings."""
    g = s.lin([(0, "#fff2c8", 1), (.18, "#e6bd6a", 1), (.5, "#b98238", 1), (.85, "#5a3612", 1), (1, "#2a1606", 1)], 0, 0, 0, 1)
    out = [f'<rect x="0" y="{-r}" width="{L}" height="{2 * r}" rx="{r * .9}" fill="{g}"/>']
    for x in (150, 330):
        out.append(f'<path d="M{x} {-r}V{r}" stroke="#4a2a0c" stroke-width="2" opacity=".55"/><path d="M{x + 2} {-r}V{r * .2}" stroke="#fff0c0" stroke-width="1" opacity=".5"/>')
    for x0, x1 in ((14, 36), (118, 132), (470, 498)):
        band = s.lin([(0, "#ff7a5a", 1), (.4, "#c0242a", 1), (1, "#4a0610", 1)], 0, 0, 0, 1)
        out.append(f'<rect x="{x0}" y="{-r - .5}" width="{x1 - x0}" height="{2 * r + 1}" fill="{band}"/>'
                   + "".join(f'<path d="M{x} {-r - .5}V{r + .5}" stroke="#ffd36a" stroke-width="1.2"/>' for x in range(x0 + 2, x1, 5)))
    holes = [70] + [250 + k * 30 for k in range(6)]
    for k, x in enumerate(holes):
        out.append(f'<ellipse cx="{x}" cy="{-r * .25}" rx="{4.6 if k else 5.4}" ry="3.4" fill="#1a0c04"/><ellipse cx="{x + .6}" cy="{-r * .25 + 1.6}" rx="3.4" ry="1.2" fill="#8a5a24" opacity=".6"/>')
    out.append(f'<rect x="4" y="{-r * .78}" width="{L - 8}" height="{r * .28}" rx="2" fill="#fffbe8" opacity=".55"/>')
    if tassel:
        out.append(f'<path d="M496 {r * .6}C506 {r + 14} 512 {r + 40} 508 {r + 62}" stroke="#d8a838" stroke-width="2" fill="none"/>'
                   f'<path d="M499 {r * .5}C514 {r + 10} 522 {r + 36} 522 {r + 58}" stroke="#c0242a" stroke-width="2" fill="none"/>'
                   f'<circle cx="515" cy="{r + 60}" r="5" fill="#d8a838"/>'
                   + "".join(f'<path d="M515 {r + 62}Q{515 + k * 1.2} {r + 74} {515 + k * 2.2} {r + 86}" stroke="{"#c0242a" if k % 2 else "#e04a3a"}" stroke-width="1.3" fill="none"/>' for k in range(-4, 5)))
    return "".join(out)


def crag(s, ctrl, seed=1, color="#1a1426", jitter=10, step=5):
    """A rocky outcrop through control points (closed along the bottom), with ragged edges and ledges."""
    rng = random.Random(seed)
    pts = smooth_line(ctrl, step)
    tab = [rng.uniform(-1, 1) for _ in range(len(pts) + 3)]
    out = []
    for k, (x, y) in enumerate(pts):
        n = tab[k] * .5 + tab[k // 3] * .35 + tab[k // 7] * .6
        out.append((x + n * jitter * .3, y + n * jitter * (0.4 if k % 9 else 1.2)))
    return out


# ================================================================ the paintings
@scene
def flute(s):
    moon = (1210, 190)
    wl = 560
    s.sky([(0, "#070b22"), (.3, "#111a40"), (.5, "#1e2d5c"), (.56, "#33456f")], 0, wl)
    s.stars(150, 0, 470, seed=11, bright=.85)
    s.moon(*moon, 44, glow_r=420)
    s.glow(*moon, 260, "#dfe8ff", .25, .2)
    s.fx("clouds", y0=230, y1=420, seed=7, cell=90, aniso=5, cover=.3, soft=.2, lit="#c8d4f0", body=.85, direct=.7,
         light=(.8, -.3), sun=(moon[0], moon[1], 300), rim="#f4f6ff", opacity=.6, x0=500, x1=1600)
    # far bank of Vrindavan: groves and a small shrine with a lamp
    far = ridgeline(wl - 2, 26, 51, cell=160, octaves=5, ridged=.2)
    s.add(f'<path d="{pts_d(far + [(1640, wl + 4), (-40, wl + 4)])}" fill="#1a2446"/>')
    rng = random.Random(4)
    cr = "".join(crown(x, wl - rng.uniform(14, 34), rng.uniform(14, 30), seed=x) for x in range(-20, 1640, 22))
    s.add(f'<path d="{cr}" fill="#141c3a"/>')
    arch.nagara(s, 1010, wl - 18, .26, color="#121a34", rim="#9aa8d8", light=1, door="#ffb45c", mandapa=True, bands=False)
    s.glow(987, wl - 24, 40, "#ffb060", .5, .25)
    s.mist(wl - 6, 30, "#8c9ccc", .45, 8)
    s.fx("reflect", y0=wl, strength=.88, tint="#060a1c", tint_near=.5, tint_far=.1, amp=3.5, y_end=H)
    s.fx("glints", y0=wl, cx=moon[0], color="#e8eeff", width=40, strength=1.0, scatter=.05, density=.45)
    s.glow(987, wl + 26, 36, "#ffb060", .35, .2, sy=2)
    s.wisps(12, 0, W, wl + 10, wl + 90, "#9fb0dd", a=(.06, .16), length=(240, 700), thick=(6, 16), blur=9, seed=3)
    # near bank
    bank = smooth_line([(-60, 700), (300, 690), (700, 712), (1100, 706), (1660, 690)], 8)
    s.add(f'<path d="{pts_d(bank + [(1660, 1010), (-60, 1010)])}" fill="{s.lin([(0, "#121a2c", 1), (1, "#05070e", 1)], 0, 690, 0, 1000, user=True)}"/>')
    s.add(f'<path d="M-60 700C300 688 700 712 1100 704S1500 690 1660 690" stroke="#8fa2d8" stroke-opacity=".35" stroke-width="2" fill="none" filter="{s.blur(1)}"/>')
    grass(s, -40, 1640, lambda x: y_at(bank, x) + 3, 300, h=(10, 34), color="#0a1020", seed=5)
    # kadamba tree on the left: a heavy trunk and limbs under a broad dome of leaves
    trng = random.Random(9)
    limbs = (limb((150, 1010, 46), (190, 780, 32), (230, 560, 26)) + limb((230, 560, 24), (150, 380, 15), (60, 230, 8)) +
             limb((230, 560, 22), (330, 360, 13), (330, 170, 7)) + limb((236, 570, 20), (420, 420, 12), (560, 260, 6)) +
             limb((420, 420, 9), (590, 360, 6), (690, 330, 3)) + limb((330, 360, 8), (460, 300, 4.5)) + limb((150, 380, 8), (40, 330, 4)))
    blobs = [(-30, 160, 120), (70, 90, 110), (190, 60, 110), (320, 80, 104), (440, 120, 96), (540, 170, 86), (630, 230, 72),
             (700, 300, 56), (740, 356, 40), (90, 250, 86), (250, 210, 92), (410, 240, 76), (560, 270, 58), (-20, 300, 70)]
    leaves = foliage(blobs, seed=3, fine=16)
    s.add(lit(s, f'<path d="{limbs}" fill="#0a0e1a"/><path d="{leaves}" fill="#0d1728"/>', toward(400, 260, *moon), w=3, color="#8fa6e0", a=.8, w2=18, a2=.2))
    tips = []
    for x, y, r in blobs:
        for _ in range(int(r / 14)):
            ang = trng.uniform(0, 2 * math.pi)
            rr = r * trng.uniform(.1, .95)
            tips.append((x + math.cos(ang) * rr, y + math.sin(ang) * rr * .8, 0))
    # kadamba blossoms: golden balls with pale filament tips, lit by the moon
    fl = []
    frng = random.Random(12)
    for (x, y, L) in tips:
        for _ in range(1):
            fx_, fy = x, y
            r = frng.uniform(3.8, 6.6)
            fl.append(f'<circle cx="{f(fx_)}" cy="{f(fy)}" r="{f(r)}" fill="url(#kad)"/>'
                      f'<circle cx="{f(fx_ + r * .3)}" cy="{f(fy - r * .3)}" r="{f(r * .45)}" fill="#fff6d0" opacity=".55"/>')
    s.defs.append('<radialGradient id="kad" cx=".62" cy=".35" r=".7"><stop offset="0" stop-color="#ffe9a0"/><stop offset=".55" stop-color="#f0a83a"/><stop offset="1" stop-color="#9a5a1a"/></radialGradient>')
    s.add(f'<g filter="{s.blur(.5)}" opacity=".9">{"".join(fl)}</g>')
    s.add(f'<g opacity=".35" style="mix-blend-mode:screen" filter="{s.blur(5)}">{"".join(fl)}</g>')
    # the stone by the water
    m0 = s.mark()
    stone = ("M520 905C505 870 520 800 560 776C620 748 760 742 900 744C1010 745 1110 752 1160 778"
             "C1200 800 1206 860 1188 905Z")
    top = "M560 776C620 748 760 742 900 744C1010 745 1110 752 1160 778C1100 792 980 798 860 798C740 798 620 794 560 776Z"
    s.add(f'<ellipse cx="860" cy="912" rx="380" ry="26" fill="#000" opacity=".55" filter="{s.blur(14)}"/>')
    s.add(f'<path d="{stone}" fill="{s.lin([(0, "#2a3450", 1), (.3, "#1a2236", 1), (1, "#0a0e18", 1)], 0, 740, 0, 905, user=True)}"/>')
    s.add(f'<path d="{stone}" fill="#fff" filter="{s.grain(.05, 4, .35, 8, "#000000")}" opacity=".5"/>')
    s.add(f'<path d="{top}" fill="{s.lin([(0, "#3e4c70", 1), (1, "#5a6a94", 1)], 500, 0, 1200, 0, user=True)}"/>')
    s.add(f'<path d="{top}" fill="#fff" filter="{s.grain(.4, 3, .25, 9, "#000000")}" opacity=".6"/>')
    s.add(f'<path d="M900 744C1010 745 1110 752 1160 778C1196 798 1204 850 1190 900" stroke="#c8d6ff" stroke-opacity=".5" stroke-width="3" fill="none" filter="{s.blur(1.5)}"/>')
    # a soft radiance over the offering
    s.glow(860, 740, 420, "#ffd8a0", .22, .2, sy=.6)
    # flute and feather resting on the stone
    s.add(f'<g transform="translate(600 784) rotate(-4)" ><rect x="10" y="6" width="520" height="16" rx="8" fill="#000" opacity=".5" filter="{s.blur(5)}"/></g>')
    s.add(f'<g transform="translate(600 784) rotate(-4)">{bansuri(s)}</g>')
    s.add(f'<g transform="translate(640 800) rotate(-14) scale(1.32 1.2)"><path d="M40 6Q200 10 330 4" stroke="#000" stroke-width="16" opacity=".35" filter="{s.blur(6)}" fill="none"/>'
          f'<g filter="{s.blur(.3)}">{peacock_feather(s)}</g></g>')
    s.add("".join(f'<circle cx="{x}" cy="{y}" r="7" fill="url(#kad)"/>' for x, y in ((640, 772), (1090, 768), (1010, 784))))
    inner = "".join(s.body[m0:])
    del s.body[m0:]
    s.add(f'<g transform="translate(860 840) scale(1.16) translate(-860 -840)">{inner}</g>')
    s.add("".join(f'<circle cx="{x}" cy="{y}" r="7" fill="url(#kad)"/>' for x, y in ((420, 742), (300, 760), (1300, 720))))
    s.motes(46, 100, 1500, 380, 940, color="#d8ff7a", seed=5, size=(1.2, 2.6), glow=5)
    s.motes(18, 500, 1200, 560, 760, color="#ffe8a0", seed=6, size=(.8, 1.6), glow=4)
    s.fx("mottle", amp=.04, cell=60)
    s.look = {"vibrance": .1}
    return s


def fire(s, cx, cy, h, n=5, seed=1, spread=0.5):
    """A small open fire of several tongues whose base sits on (cx, cy)."""
    rng = random.Random(seed)
    s.glow(cx, cy - h * .3, h * 7, "#ff8a3a", .5, .12)
    s.glow(cx, cy - h * .3, h * 2.2, "#ffc070", .7, .3)
    for k in range(n):
        t = (k - (n - 1) / 2) / max(1, (n - 1) / 2)
        hh = h * (1 - abs(t) * .45) * rng.uniform(.8, 1.1)
        s.flame(cx + t * h * spread, cy + abs(t) * h * .04, hh, glow=False, lean=rng.uniform(-.12, .12) - t * .08)


def sparks(s, cx, cy, n, h, w, seed=1, color="#ffcf70"):
    rng = random.Random(seed)
    out = []
    for _ in range(n):
        t = rng.random() ** 1.3
        x = cx + rng.uniform(-w, w) * (.3 + t) + math.sin(t * 9 + rng.random() * 6) * 18 * t
        y = cy - t * h
        L = rng.uniform(3, 9)
        a = rng.uniform(.4, 1) * (1 - t * .7)
        out.append(f'<path d="M{f(x)} {f(y)}l{f(rng.uniform(-1.5, 1.5))} {f(-L)}" stroke="#fff3c8" stroke-width="{f(rng.uniform(1, 2))}" stroke-linecap="round" opacity="{a:.2f}"/>')
    s.add(f'<g style="mix-blend-mode:screen"><g filter="{s.blur(2.5)}" opacity=".8">{"".join(out).replace("#fff3c8", color)}</g>{"".join(out)}</g>')


def bonfire(s, cx, cy, h, w, n=16, seed=1):
    """A big sacrificial fire: many tongues of different heights and leans, darker red outer
    tongues behind brighter inner ones, a white-hot core and a broad glow."""
    rng = random.Random(seed)
    s.glow(cx, cy - h * .35, h * 4.2, "#ff6a20", .55, .12)
    s.glow(cx, cy - h * .4, h * 1.4, "#ffc070", .75, .3)
    tongues = []
    for k in range(n):
        t = rng.uniform(-1, 1)
        hh = h * (1 - abs(t) ** 1.6 * .7) * rng.uniform(.55, 1.05)
        tongues.append((abs(t), cx + t * w * .5, hh, rng.uniform(-.18, .18) - t * .12))
    for _, x, hh, ln in sorted(tongues, reverse=True):
        m = s.mark()
        s.flame(0, 0, hh, glow=False, lean=ln)
        inner = "".join(s.body[m:])
        del s.body[m:]
        s.add(f'<g transform="translate({f(x)} {f(cy + rng.uniform(-4, 6))}) scale({rng.uniform(.42, .62):.2f} 1)">{inner}</g>')
    s.add(f'<ellipse cx="{f(cx)}" cy="{f(cy - h * .12)}" rx="{f(w * .32)}" ry="{f(h * .16)}" fill="#fffbe8" opacity=".85" filter="{s.blur(h * .05)}"/>')


def palm(x, base, h, seed=1, lean=0.1):
    """A coconut palm silhouette (path)."""
    rng = random.Random(seed)
    tx, ty = x + lean * h, base - h
    d = [ribbon(smooth_line([(x, base), (x + lean * h * .3, base - h * .5), (tx, ty)], 10), h * .05, h * .025)]
    for k in range(9):
        a = math.radians(-160 + 140 * k / 8 + rng.uniform(-8, 8))
        L = h * rng.uniform(.32, .45)
        ex, ey = tx + math.cos(a) * L, ty + math.sin(a) * L * .55 + L * .35
        mx, my = tx + math.cos(a) * L * .5, ty + math.sin(a) * L * .5 - L * .12
        line = smooth_line([(tx, ty), (mx, my), (ex, ey)], 4)
        n = len(line)
        left, right = [], []
        for i, (px, py) in enumerate(line):
            qx, qy = line[min(n - 1, i + 1)]
            ox, oy = line[max(0, i - 1)]
            dx, dy = qx - ox, qy - oy
            Ln = math.hypot(dx, dy) or 1
            wv = h * .045 * math.sin(math.pi * min(1, (i + .5) / n * 1.05)) * (1 + .18 * ((i % 2) * 2 - 1) * (i > 2))
            left.append((px - dy / Ln * wv, py + dx / Ln * wv))
            right.append((px + dy / Ln * wv * .5, py - dx / Ln * wv * .5))
        d.append(pts_d(left + right[::-1]))
    return "".join(d)


def beams(s, x0, y0, specs, color="#fff0c0", blur=18):
    """Hand-painted shafts of light from (x0, y0): specs are (angle_deg, width_deg, length, alpha)."""
    out = []
    for ang, wd, L, a in specs:
        a1, a2 = math.radians(ang - wd / 2), math.radians(ang + wd / 2)
        g = s.lin([(0, color, a), (.7, color, a * .5), (1, color, 0)], x0, y0, x0 + math.sin(math.radians(ang)) * L, y0 + math.cos(math.radians(ang)) * L, user=True)
        out.append(f'<path d="M{f(x0)} {f(y0)}L{f(x0 + math.sin(a1) * L)} {f(y0 + math.cos(a1) * L)}L{f(x0 + math.sin(a2) * L)} {f(y0 + math.cos(a2) * L)}Z" fill="{g}"/>')
    s.add(f'<g filter="{s.blur(blur)}" style="mix-blend-mode:screen">{"".join(out)}</g>')


@scene
def guru(s):
    sun = (1010, 40)
    # forest air: warm light behind the clearing, cool green at the edges
    s.sky([(0, "#f6efc8"), (.35, "#c9cf9a"), (.65, "#6d8a6a"), (1, "#2a3a30")])
    s.add(f'<rect width="{W}" height="{H}" fill="{s.rad([(0, "#fff6d8", .85), (.5, "#e8dca0", .3), (1, "#e8dca0", 0)], 960, 420, 700, user=True)}"/>')
    rng = random.Random(5)
    # three depths of tree trunks fading into the haze
    for depth, (col, n, wr, a) in enumerate((("#b8bf98", 18, (6, 14), .7), ("#7f9274", 14, (10, 22), .85), ("#3f5244", 9, (18, 34), 1))):
        d = []
        for _ in range(n):
            x = rng.uniform(-40, 1640)
            if 560 < x < 1240 and depth == 2:
                continue
            w = rng.uniform(*wr)
            base = 760 + depth * 40
            d.append(f"M{f(x - w / 2)} {base}C{f(x - w * .4)} 500 {f(x - w * .35)} 200 {f(x - w * .3)} -10H{f(x + w * .3)}C{f(x + w * .35)} 200 {f(x + w * .4)} 500 {f(x + w / 2)} {base}Z")
        s.add(f'<path d="{"".join(d)}" fill="{col}" opacity="{a}"/>')
        s.add(f'<path d="{canopy([(rng.uniform(-50, 1650), rng.uniform(-40, 120 + depth * 40), 0) for _ in range(14)], r=(60, 120), seed=depth + 3, k=2)}" fill="{col}" opacity="{a}"/>')
        s.mist(560 + depth * 90, 300, "#f0ead0", .35, 40)
    # ground of the clearing
    g = smooth_line([(-60, 800), (400, 812), (800, 826), (1200, 812), (1660, 798)], 8)
    s.add(f'<path d="{pts_d(g + [(1660, 1010), (-60, 1010)])}" fill="{s.lin([(0, "#8a8a50", 1), (.25, "#5a6236", 1), (1, "#1c2414", 1)], 0, 800, 0, 1000, user=True)}"/>')
    s.add(f'<ellipse cx="830" cy="880" rx="520" ry="70" fill="#ffe8a0" opacity=".35" filter="{s.blur(30)}" style="mix-blend-mode:screen"/>')
    grass(s, -40, 1640, lambda x: y_at(g, x) + 4, 260, h=(8, 26), color="#3a4424", seed=2)
    # the great banyan: trunk, aerial roots and a canopy roofing the clearing
    trng = random.Random(21)
    segs, tips = [], []
    branches(330, 840, 6, 260, 120, 4, trng, segs, tips, spread=40, shrink=.74, bend=12)
    roots = []
    for _ in range(16):
        x = trng.uniform(140, 720)
        y0 = trng.uniform(120, 300)
        y1 = trng.uniform(500, 840) if trng.random() < .5 else trng.uniform(380, 560)
        w = trng.uniform(2, 7)
        roots.append(ribbon(smooth_line([(x, y0), (x + trng.uniform(-8, 8), (y0 + y1) / 2), (x + trng.uniform(-5, 5), y1)], 10), w * .6, w))
    leaves = foliage([(x + trng.uniform(-20, 20), y, trng.uniform(50, 80)) for x, y, _ in tips], seed=8, fine=12) + \
        foliage([(x, trng.uniform(-50, 50), trng.uniform(80, 120)) for x in range(-80, 1700, 110)], seed=9, fine=14)
    tree = (f'<path d="{"".join(segs)}" fill="#1e2318"/>'
            f'<path d="{"".join(roots)}" fill="#262c1e"/>'
            f'<path d="{leaves}" fill="#18241a"/>')
    s.add(lit(s, tree, toward(330, 600, *sun), w=3, color="#ffe6a0", a=.85, w2=18, a2=.22))
    # gaps of bright sky in the canopy feed the light shafts
    s.add("".join(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="#fffbe8" opacity=".9" filter="{s.blur(3)}"/>'
                  for x, y, r in ((990, 64, 13), (1040, 96, 7), (930, 40, 9), (1120, 52, 6), (1220, 128, 5))))
    beams(s, 1010, 60, [(-28, 7, 980, .32), (-18, 5, 950, .26), (-38, 4, 1000, .2), (-8, 4, 900, .18), (-48, 3, 1000, .14)], blur=14)
    s.fx("godrays", cx=1010, cy=70, strength=.5, thresh=.75, decay=.975, radius=220)
    # the teacher and the student, a small fire between them
    fx_, base = 818, 868
    s.add(f'<ellipse cx="600" cy="{base + 2}" rx="120" ry="14" fill="#3a2a18"/><ellipse cx="1020" cy="{base + 2}" rx="106" ry="12" fill="#3a2a18"/>')
    s.add(f'<path d="M500 {base + 4}C520 {base - 8} 690 {base - 10} 722 {base + 2}C700 {base + 14} 520 {base + 16} 500 {base + 4}Z" fill="#8a6a44"/>')  # antelope skin
    sage = place(600, base, 2.8, seated_side("sage", "teach", "#16120e"))
    s.add(lit(s, sage, 0, w=5, color="#ffc074", a=1, w2=26, a2=.42))
    s.add(lit(s, sage, -60, w=2.5, color="#fff0c0", a=.6))
    pupil = place(1030, base, 2.5, seated_side("youth", "anjali", "#16120e"), flip=True)
    s.add(lit(s, pupil, 180, w=5, color="#ffc074", a=1, w2=24, a2=.42))
    s.add(lit(s, pupil, -110, w=2.5, color="#fff0c0", a=.55))
    # kamandalu and palm-leaf books
    s.add(f'<path d="M456 {base}C442 {base - 2} 440 {base - 26} 454 {base - 32}C450 {base - 38} 454 {base - 44} 462 {base - 44}C470 {base - 44} 474 {base - 38} 470 {base - 32}C484 {base - 26} 482 {base - 2} 468 {base}Z" fill="#3a2414"/>'
          f'<path d="M470 {base - 36}C480 {base - 50} 492 {base - 50} 494 {base - 42}" stroke="#3a2414" stroke-width="3" fill="none"/>')
    s.add(f'<g transform="translate(1150 {base - 4}) rotate(-3)"><rect x="-36" y="-8" width="72" height="9" rx="2" fill="#c8a462"/><rect x="-38" y="-14" width="76" height="7" rx="2" fill="#b08a4a"/>'
          f'<path d="M-30 -14V1M30 -14V1" stroke="#6a3a1a" stroke-width="2"/></g>')
    s.add(f'<ellipse cx="{fx_}" cy="{base + 4}" rx="44" ry="9" fill="#2a1a10"/>')
    s.add("".join(f'<path d="M{fx_ - 30 + k * 12} {base + 2}L{fx_ + 22 - k * 9} {base - 8}" stroke="#4a2a14" stroke-width="5" stroke-linecap="round"/>' for k in range(4)))
    fire(s, fx_, base - 4, 46, n=5, seed=3, spread=.45)
    s.smoke(fx_ + 4, base - 50, 420, color="#f6ecd8", a=.4, seed=6, width=2.4, drift=.25)
    s.motes(60, 500, 1300, 250, 820, color="#fff0b0", seed=4, size=(.8, 2.0))
    # foreground ferns
    fern = []
    frng = random.Random(3)
    for cx, cy, n in ((60, 1010, 9), (1560, 1010, 9), (260, 1010, 6), (1380, 1010, 5)):
        for k in range(n):
            a = math.radians(-70 + 140 * k / max(1, n - 1) + frng.uniform(-6, 6))
            L = frng.uniform(140, 240)
            ex, ey = cx + math.sin(a) * L, cy - math.cos(a) * L * .8
            fern.append(ribbon(smooth_line([(cx, cy), ((cx + ex) / 2 + math.sin(a) * 20, (cy + ey) / 2 - 20), (ex, ey)], 6), 16, 1))
    s.add(f'<path d="{"".join(fern)}" fill="#0e140c"/>')
    s.fx("mottle", amp=.045, cell=60)
    s.look = {"vibrance": .12}
    return s


@scene
def meditator(s):
    sun = (800, 560)
    s.sky([(0, "#1a1a48"), (.22, "#3a3170"), (.4, "#7d4f86"), (.5, "#c9718a"), (.56, "#f2a280"), (.6, "#ffd3a0")], 0, 640)
    s.stars(50, 0, 220, seed=8, bright=.5)
    s.sun(*sun, 58, halo_r=660, halo_a=.85)
    s.fx("clouds", y0=40, y1=320, seed=17, cell=150, aniso=3.4, cover=.4, soft=.18, lit="#ffb8a0", body=.72, direct=.75,
         light=(0, 1), sun=(sun[0], sun[1], 420), opacity=.9)
    s.fx("clouds", y0=330, y1=500, seed=18, cell=80, aniso=6, cover=.3, soft=.22, lit="#ffd8b0", body=.85, direct=.9,
         light=(0, 1), sun=(sun[0], sun[1], 360), opacity=.75)
    far = peak_line(600, [(130, 190, 220), (420, 120, 170), (1220, 210, 230, .1), (1500, 140, 180)], 31, shape=1.25, floor=0, shoulders=2)
    mountains(s, far, "#7a6aa2", "#c49ab4", lit="#ffc0a0", lit_a=.75, light=-1, seed=4, snow="#c8bce0", snow_shade="#a898c8",
              lit_snow="#fff0e0", snowline=480, snow_fingers=40, rim="#ffe8cc", rim_center=sun, rim_r=700, haze="#f2c2b8", haze_a=.6, haze_h=120)
    # a sea of cloud below the summits
    s.add(f'<rect y="560" width="{W}" height="440" fill="{s.lin([(0, "#e9b0a8", 1), (.4, "#b98aa8", 1), (1, "#5a4a7a", 1)], 0, 560, 0, 1000, user=True)}"/>')
    s.fx("clouds", y0=540, y1=820, seed=19, cell=120, aniso=2.6, cover=.62, soft=.22, lit="#ffe2c8", body=.8, direct=1.0,
         light=(0, -1), sun=(sun[0], sun[1], 520), rim="#fff4e0", opacity=1, top_fade=.15, bottom_fade=.1, bump=1.6)
    s.fx("clouds", y0=700, y1=1000, seed=20, cell=150, aniso=2.4, cover=.6, soft=.24, lit="#f8c8c0", body=.75, direct=.9,
         light=(0, -1), sun=(sun[0], sun[1], 600), opacity=1, top_fade=.2, bottom_fade=0, bump=1.4)
    s.glow(800, 640, 600, "#ffcf9a", .35, .2, sy=.4)
    # the rock, with a few windswept pines
    s.add(f'<circle cx="{sun[0]}" cy="{sun[1]}" r="96" fill="none" stroke="#fff2d8" stroke-opacity=".3" stroke-width="2" filter="{s.blur(1.5)}"/>')
    s.add(f'<circle cx="{sun[0]}" cy="{sun[1]}" r="150" fill="none" stroke="#fff2d8" stroke-opacity=".14" stroke-width="1.5" filter="{s.blur(2)}"/>')
    man = place(800, 778, 2.35, back_person("seated", "#120e1c"))
    s.add(lit(s, man, -90, w=3, color="#ffe6bc", a=1, blur=1.2, halo=8, halo_a=.45))
    rock = crag(s, [(330, 1010), (380, 960), (452, 930), (500, 880), (560, 858), (600, 822), (660, 800), (700, 776), (740, 770), (800, 768), (860, 770),
                    (900, 778), (940, 800), (1010, 818), (1060, 852), (1120, 870), (1180, 930), (1240, 960), (1300, 1010)], seed=4, jitter=8)
    s.add(lit(s, f'<path d="{pts_d(rock)}" fill="#1a1426"/>', -90, w=3, color="#ffcf9e", a=.9, w2=14, a2=.2))
    s.add(f'<path d="{pts_d(rock)}" fill="#fff" filter="{s.grain(.03, 4, .3, 5, "#000000")}" opacity=".35"/>')
    s.add(f'<path d="M560 858Q600 880 700 872M940 800Q980 836 1080 846" stroke="#ffcf9e" stroke-opacity=".08" stroke-width="3" fill="none" filter="{s.blur(2)}"/>')
    s.birds(5, 1000, 1240, 380, 450, color="#4a2a48", s=(5, 9), seed=3, a=.75)
    s.fx("godrays", cx=sun[0], cy=sun[1], strength=.45, thresh=.72, decay=.972, radius=260)
    s.fx("mottle", amp=.04, cell=60)
    return s


@scene
def breath(s):
    wl = 540
    glow_x = 1080
    s.sky([(0, "#5d6f98"), (.35, "#93a3c4"), (.7, "#d6c6d0"), (.92, "#f6d6c8"), (1, "#ffe2c8")], 0, wl)
    s.glow(glow_x, wl, 520, "#ffe0c0", .55, .2, sy=.5)
    s.fx("clouds", y0=120, y1=360, seed=27, cell=120, aniso=6, cover=.26, soft=.24, lit="#fff0e6", body=.92, direct=.7,
         light=(.3, 1), opacity=.55)
    far = ridgeline(wl, 34, 61, cell=300, octaves=5, ridged=.25, envelope=[(0, 1), (700, .6), (1600, .9)])
    hills(s, far, "#a6a8c4", "#c6bccc", haze="#efd8d4", haze_a=.6, haze_h=40)
    near = ridgeline(wl + 1, 12, 62, cell=160, octaves=4, ridged=.2, envelope=[(0, 1), (600, .4), (1600, .2)])
    hills(s, near, "#8a8cac", "#a4a0bc")
    s.mist(wl - 2, 40, "#fff0ea", .5, 10)
    s.fx("reflect", y0=wl, strength=.92, tint="#3a3c60", tint_near=.32, tint_far=.04, amp=1.2, ripple=.5, blur=1.0)
    # the low bank and rock where the figure sits, mirrored in the still water
    edge = 668
    m = s.mark()
    bank = f"M-60 {edge}L-60 610C60 616 200 630 300 640C380 618 470 606 540 612C590 618 618 640 630 {edge}Z"
    s.add(f'<path d="{bank}" fill="#2a2840"/>')
    s.add(f'<path d="M300 640C380 618 470 606 540 612C590 618 618 640 630 {edge}" stroke="#ffe0c8" stroke-opacity=".45" stroke-width="2" fill="none"/>')
    rr = random.Random(3)
    reeds = []
    for _ in range(26):
        x = rr.uniform(10, 260)
        b = 640 + (x / 260) * 4
        h = rr.uniform(50, 150)
        lean = rr.uniform(-.1, .35) * h
        reeds.append(ribbon(smooth_line([(x, b), (x + lean * .3, b - h * .55), (x + lean, b - h)], 8), 3.2, .4))
    s.add(f'<path d="{"".join(reeds)}" fill="#2a2840"/>')
    grass(s, -40, 300, lambda x: 612 + x * .1, 70, h=(10, 30), color="#2a2840", seed=7, lean=.2)
    fig = place(452, 612, 1.75, seated_side("plain", "knee", "#262338"))
    s.add(lit(s, fig, toward(452, 560, glow_x, wl), w=2.4, color="#ffe8d8", a=.85, w2=10, a2=.2))
    ob.reflect_since(s, m, edge, .55, 2.5, 260)
    # concentric ripples spreading over the still water
    cx, cy = 900, 740
    rings = []
    for k in range(9):
        rx = 40 + k * 46
        ry = rx * .16
        a = .55 * (1 - k / 9) ** 1.2
        rings.append(f'<ellipse cx="{cx}" cy="{f(cy + k * 1.5)}" rx="{rx}" ry="{f(ry)}" fill="none" stroke="#fff4ec" stroke-opacity="{a:.2f}" stroke-width="{f(2.2 - k * .12)}"/>'
                     f'<ellipse cx="{cx}" cy="{f(cy + k * 1.5 + ry * .22)}" rx="{rx}" ry="{f(ry)}" fill="none" stroke="#2a2c4a" stroke-opacity="{a * .6:.2f}" stroke-width="{f(1.6 - k * .08)}"/>')
    s.add(f'<g filter="{s.blur(.8)}">{"".join(rings)}</g>')
    s.wisps(14, 720, 1600, wl + 4, wl + 120, "#fff2ee", a=(.08, .22), length=(200, 600), thick=(8, 22), blur=12, seed=4)
    s.add(f'<g opacity=".45">' + "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#fff4f0" filter="{s.blur(16)}"/>'
                                          for x, y, rx, ry in ((900, 600, 240, 22), (1250, 620, 300, 26), (1000, 560, 200, 14))) + '</g>')
    s.birds(3, 1080, 1220, 300, 340, color="#4a4a6a", s=(5, 8), seed=5, a=.6)
    s.fx("mottle", amp=.03, cell=70)
    s.look = {"contrast": 1.02, "vignette": .26}
    return s


# ---------------------------------------------------------------- ritual objects
def kalash(s, x, y, sc=1.0, metal="brass"):
    """A brass or copper water pot crowned with mango leaves and a coconut; (x, y) is its base."""
    g = s.lin(ob.BRASS if metal == "brass" else [(0, "#3a1408"), (.3, "#a04a22"), (.5, "#ffc09a"), (.62, "#c2602a"), (1, "#3a1408")], 0, 0, 1, 0)
    leaves = "".join(f'<path d="M0 -62C{f(k * 9)} -70 {f(k * 22)} -74 {f(k * 34)} {f(-68 + abs(k) * 6)}C{f(k * 22)} -64 {f(k * 10)} -62 0 -60Z" fill="#2f6a2a"/>'
                     for k in (-1.2, -.6, .6, 1.2))
    body = ("M-14 0C-30 -4 -36 -24 -32 -38C-28 -50 -18 -54 -12 -56L-12 -62H12L12 -56C18 -54 28 -50 32 -38"
            "C36 -24 30 -4 14 0Z")
    return place(x, y, sc, f'<ellipse cx="0" cy="1" rx="30" ry="5" fill="#000" opacity=".4"/>{leaves}<path d="{body}" fill="{g}"/>'
                 f'<path d="M-31 -30C-10 -24 10 -24 31 -30" stroke="#c0242a" stroke-width="3" fill="none"/>'
                 f'<ellipse cx="0" cy="-72" rx="13" ry="15" fill="#8a5a2a"/><path d="M-6 -86C-2 -92 2 -92 6 -86" stroke="#c8a060" stroke-width="3" fill="none"/>'
                 f'<path d="M-13 -66H13" stroke="#c0242a" stroke-width="2.4"/>')


def persp(X, Y, Z=0, vx=800, horizon=430, ground=370, fl=900):
    """Project a point on (or Z above) the ground, Y metres away from the front plane."""
    k = fl / (fl + Y)
    return vx + X * k, horizon + (ground - Z) * k, k


@scene
def yajna(s):
    fire_x, fire_y = 800, 690
    s.sky([(0, "#05040e"), (.4, "#120a1e"), (.62, "#2a1424"), (.75, "#3a1a1a")])
    s.stars(80, 0, 300, seed=4, bright=.6)
    # trees and a pavilion roof in the dark, warmed by the fire
    rng = random.Random(8)
    s.add(f'<rect y="300" width="{W}" height="240" fill="{s.lin([(0, "#3a1814", 0), (1, "#5a2414", .8)], 0, 300, 0, 540, user=True)}"/>')
    trees = foliage([(x, rng.uniform(420, 470), rng.uniform(50, 90)) for x in range(-40, 1700, 80)], seed=5, fine=10)
    s.add(f'<path d="{trees}M-50 470H1650V560H-50Z" fill="#1c0e12"/>')
    s.glow(fire_x, 520, 900, "#ff7a2a", .35, .15)
    # ground of beaten earth, lit in a pool around the altar
    s.add(f'<rect y="500" width="{W}" height="500" fill="{s.lin([(0, "#1a0c0a", 1), (1, "#2a140c", 1)], 0, 500, 0, 1000, user=True)}"/>')
    s.add(f'<ellipse cx="{fire_x}" cy="780" rx="760" ry="230" fill="{s.rad([(0, "#c8622a", .7), (.45, "#7a3214", .35), (1, "#2a1008", 0)])}" style="mix-blend-mode:screen"/>')
    s.mist(505, 90, "#7a3420", .6, 20)
    # the havan kund: three stepped brick tiers around a square pit
    tiers = [(150, 0, 20), (124, 20, 38), (100, 38, 54)]
    clr = ["#8a3a1c", "#9a4422", "#aa4e28"]
    for k, (a, z0, z1) in enumerate(tiers):
        fl_ = [persp(X, Y, z1) for X, Y in ((-a, -a), (a, -a), (a, a), (-a, a))]
        front = [persp(-a, -a, z0), persp(a, -a, z0), persp(a, -a, z1), persp(-a, -a, z1)]
        top_g = s.lin([(0, mix(clr[k], "#ffb070", .35), 1), (1, mix(clr[k], "#ffd0a0", .55), 1)], 0, fl_[2][1], 0, fl_[0][1], user=True)
        s.add(f'<path d="{pts_d([(p[0], p[1]) for p in fl_])}" fill="{top_g}"/>')
        fg = s.lin([(0, mix(clr[k], "#ff9a50", .3), 1), (1, mix(clr[k], "#200804", .55), 1)], 0, front[2][1], 0, front[0][1], user=True)
        s.add(f'<path d="{pts_d([(p[0], p[1]) for p in front])}" fill="{fg}"/>')
        # brick courses
        y0, y1 = front[2][1], front[0][1]
        s.add(f'<path d="M{f(front[0][0])} {f((y0 + y1) / 2)}H{f(front[1][0])}" stroke="#3a1206" stroke-opacity=".45" stroke-width="1.4"/>'
              + "".join(f'<path d="M{f(front[0][0] + (front[1][0] - front[0][0]) * t)} {f(y0 + (k2 % 2) * (y1 - y0) / 2)}v{f((y1 - y0) / 2)}" stroke="#3a1206" stroke-opacity=".35" stroke-width="1.2"/>'
                        for k2 in range(2) for t in [i / 9 + (k2 * .055) for i in range(1, 9)]))
        s.add(f'<path d="M{f(front[3][0])} {f(front[3][1])}H{f(front[2][0])}" stroke="#ffd09a" stroke-opacity=".7" stroke-width="2"/>')
    pit = [persp(X, Y, 54) for X, Y in ((-70, -70), (70, -70), (70, 70), (-70, 70))]
    s.add(f'<path d="{pts_d([(p[0], p[1]) for p in pit])}" fill="#3a0c04"/>')
    # rangoli of turmeric and kumkum round the base
    for a_, col, wd in ((172, "#f2b632", 5), (190, "#c8241e", 4), (206, "#f6efe0", 2.5)):
        rg = [persp(X, Y, 0) for X, Y in ((-a_, -a_), (a_, -a_), (a_, a_), (-a_, a_))]
        s.add(f'<path d="{pts_d([(p[0], p[1]) for p in rg])}" fill="none" stroke="{col}" stroke-width="{wd}" opacity=".75" filter="{s.blur(.8)}"/>')
    for X, Y in ((-190, -190), (190, -190), (0, -190), (-190, 0), (190, 0)):
        x, y, k = persp(X, Y, 0)
        s.add("".join(f'<ellipse cx="{f(x + math.cos(a) * 9 * k)}" cy="{f(y + math.sin(a) * 3.2 * k)}" rx="{f(6 * k)}" ry="{f(2.4 * k)}" fill="#f2b632" opacity=".85" transform="rotate({f(math.degrees(a))} {f(x + math.cos(a) * 9 * k)} {f(y + math.sin(a) * 3.2 * k)})"/>' for a in [i * math.pi / 4 for i in range(8)])
              + f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(4 * k)}" fill="#c8241e"/>')
    # priests seated round the fire: two behind (facing us), two at the sides
    for X, Y, kind in ((-250, 210, "back"), (250, 210, "back")):
        x, y, k = persp(X, Y)
        s.add(lit(s, place(x, y, 1.15 * k * 1.6, back_person("seated", "#1a0c0a")), -90, w=2.5, color="#ffb060", a=.8))
    # flames, sparks and smoke rising from the pit
    bonfire(s, fire_x, fire_y + 2, 280, 170, n=22, seed=5)
    sparks(s, fire_x, fire_y - 120, 140, 560, 120, seed=3)
    s.smoke(fire_x + 10, fire_y - 260, 420, color="#e8c8a8", a=.28, seed=3, width=4, drift=.15)
    for side, X in ((-1, -330), (1, 330)):
        x, y, k = persp(X, -40)
        figsvg = seated_side("sage" if side < 0 else "youth", "offer" if side < 0 else "anjali", "#120806",
                             extra=ladle(46, -30, 92, -52, "#120806", 2.2) if side < 0 else "")
        sc = 2.25 * k
        s.add(lit(s, place(x, y, sc, figsvg, flip=side > 0), 0 if side < 0 else 180, w=4, color="#ffb868", a=1, w2=22, a2=.42))
        s.add(lit(s, place(x, y, sc, figsvg, flip=side > 0), -90, w=2, color="#ff9a50", a=.5))
    # ghee bowl, kalash and a stack of samidh sticks
    s.add(kalash(s, 470, 862, .95))
    s.add(f'<ellipse cx="610" cy="864" rx="26" ry="8" fill="{s.lin(ob.BRASS, 0, 0, 1, 0)}"/><ellipse cx="610" cy="861" rx="20" ry="4" fill="#f2c860"/>')
    s.add("".join(f'<path d="M{1040 + k * 3} {876 - k * 5}L{1160 + k * 2} {866 - k * 5}" stroke="#5a3418" stroke-width="7" stroke-linecap="round"/>' for k in range(5)))
    ob.petals_scatter(s, 520, 1120, 850, 900, 30, seed=4)
    # the yajnashala: two posts and a beam hung with mango leaves and marigolds
    post = "M120 1010V100H162V1010ZM1438 1010V100H1480V1010ZM60 70H1540V112H60Z"
    s.add(lit(s, f'<path d="{post}" fill="#140806"/>', -90, w=3, color="#ffa050", a=.8, w2=14, a2=.25))
    s.add(f'<path d="M40 74C400 40 1200 40 1560 74V0H40Z" fill="#0e0604"/>')
    s.add("".join(f'<path d="M{x} 112C{x - 8} 132 {x - 5} 150 {x} 158C{x + 5} 150 {x + 8} 132 {x} 112Z" fill="{"#2a4a1e" if (x // 26) % 2 else "#3a5a24"}"/>' for x in range(180, 1430, 26)))
    ob.garland(s, 170, 118, 1430, 118, 40, r=9, seed=6, tassel=False)
    s.motes(40, 500, 1100, 120, 600, color="#ffb050", seed=9, size=(.8, 1.8))
    s.fx("mottle", amp=.04, cell=60)
    s.look = {"vibrance": .1, "bloom": 1.1}
    return s


def pillar(s, x, y0, y1, w, color="#2a1a12", rim="#ffb860", side=1, rim_a=0.8):
    """A carved temple pillar standing on y0 and carrying the beam at y1: square base, banded
    shaft with a lotus-bell section, and a bracket capital. side = which edge faces the light."""
    h = y0 - y1
    d = [f"M{f(x - w * .62)} {f(y0)}V{f(y0 - h * .1)}H{f(x + w * .62)}V{f(y0)}Z",
         f"M{f(x - w * .5)} {f(y0 - h * .1)}V{f(y1 + h * .14)}H{f(x + w * .5)}V{f(y0 - h * .1)}Z",
         f"M{f(x - w * .62)} {f(y0 - h * .38)}h{f(w * 1.24)}v{f(h * .05)}h{f(-w * 1.24)}Z",
         f"M{f(x - w * .58)} {f(y0 - h * .64)}h{f(w * 1.16)}v{f(h * .04)}h{f(-w * 1.16)}Z",
         f"M{f(x - w * .5)} {f(y1 + h * .14)}C{f(x - w * .7)} {f(y1 + h * .1)} {f(x - w * .9)} {f(y1 + h * .06)} {f(x - w * 1.1)} {f(y1 + h * .04)}"
         f"V{f(y1)}H{f(x + w * 1.1)}V{f(y1 + h * .04)}C{f(x + w * .9)} {f(y1 + h * .06)} {f(x + w * .7)} {f(y1 + h * .1)} {f(x + w * .5)} {f(y1 + h * .14)}Z"]
    lg = s.lin([(0, color, 1), (.6, color, 1), (1, mix(color, rim, .35), 1)] if side > 0 else [(0, mix(color, rim, .35), 1), (.4, color, 1), (1, color, 1)],
               x - w * 1.1, 0, x + w * 1.1, 0, user=True)
    out = f'<path d="{"".join(d)}" fill="{lg}"/>'
    out += (f'<path d="M{f(x - w * .5)} {f(y0 - h * .2)}H{f(x + w * .5)}M{f(x - w * .5)} {f(y0 - h * .5)}H{f(x + w * .5)}M{f(x - w * .5)} {f(y0 - h * .8)}H{f(x + w * .5)}"'
            f' stroke="#000" stroke-opacity=".35" stroke-width="{f(max(1, w * .05))}"/>')
    ex = x + side * w * .5
    out += (f'<path d="M{f(ex)} {f(y0 - h * .1)}V{f(y1 + h * .14)}" stroke="{rim}" stroke-opacity="{rim_a}" stroke-width="{f(max(1.2, w * .07))}"/>'
            f'<path d="M{f(x + side * w * .62)} {f(y0)}V{f(y0 - h * .1)}M{f(x + side * w * 1.1)} {f(y1)}V{f(y1 + h * .04)}" stroke="{rim}" stroke-opacity="{rim_a * .7}" stroke-width="{f(max(1, w * .05))}"/>')
    return out


@scene
def darshan(s):
    vx, vy = 800, 470
    ob.dark_room(s, light=(vx, vy), base="#0c0604", warm="#5a2a10", r=1000, horizon=640, floor="#140a06")
    # the hall: ceiling beams and pillars receding to the sanctum
    depths = [0.16, 0.24, 0.34, 0.48, 0.68, 1.0]
    s.add(f'<path d="M0 0H1600L{vx + 180} {vy - 170}H{vx - 180}Z" fill="#0a0503"/>')
    for k in depths:
        yb = vy + 470 * k   # floor line
        yt = vy - 300 * k - 30 * k  # beam underside
        s.add(f'<path d="M{f(vx - 1300 * k)} {f(yt)}H{f(vx + 1300 * k)}V{f(yt - 40 * k)}H{f(vx - 1300 * k)}Z" fill="#1a0d06"/>'
              f'<path d="M{f(vx - 1300 * k)} {f(yt)}H{f(vx + 1300 * k)}" stroke="#ffb050" stroke-opacity="{.35 - k * .2:.2f}" stroke-width="{f(1 + 2 * k)}"/>')
    # sanctum doorway glowing with tiers of lamps
    dx0, dx1, dy0, dy1 = vx - 86, vx + 86, vy - 150, vy + 76
    s.add(f'<rect x="{dx0 - 26}" y="{dy0 - 30}" width="{dx1 - dx0 + 52}" height="{dy1 - dy0 + 30}" fill="#3a1e0c"/>')
    s.add(f'<rect x="{dx0}" y="{dy0}" width="{dx1 - dx0}" height="{dy1 - dy0}" fill="{s.rad([(0, "#fff4c8", 1), (.35, "#ffbf5a", 1), (.75, "#c8601a", 1), (1, "#5a2008", 1)], .5, .55, .7)}"/>')
    # an arched prabhavali frame inside, dark against the glow, lamps in rows before it
    s.add(f'<path d="M{vx - 54} {dy1 - 10}V{vy - 50}C{vx - 54} {vy - 120} {vx + 54} {vy - 120} {vx + 54} {vy - 50}V{dy1 - 10}" stroke="#6a2a08" stroke-width="10" fill="none" opacity=".75"/>')
    s.add(f'<path d="M{vx - 28} {dy1 - 10}V{vy - 40}C{vx - 28} {vy - 76} {vx + 28} {vy - 76} {vx + 28} {vy - 40}V{dy1 - 10}Z" fill="#5a2208" opacity=".6"/>')
    for row, (y, n, h) in enumerate(((dy1 - 18, 9, 13), (dy1 - 44, 7, 11), (vy - 70, 11, 8), (vy - 110, 9, 7))):
        for i in range(n):
            t = (i - (n - 1) / 2) / max(1, (n - 1) / 2)
            yy = y + (abs(t) ** 2 * 18 if row >= 2 else 0)
            s.flame(vx + t * (74 if row < 2 else 60), yy, h, glow_r=h * 4, glow_a=.35)
    s.glow(vx, vy - 20, 260, "#ffd890", .7, .3)
    # garlands framing the door
    ob.garland(s, dx0 - 10, dy0 - 18, dx1 + 10, dy0 - 18, 22, r=6, seed=4, tassel=False)
    # floor: polished stone carrying the light toward us
    s.add(f'<path d="M{vx - 90} {dy1}L{vx + 90} {dy1}L{vx + 520} 1000H{vx - 520}Z" fill="{s.lin([(0, "#ffb050", .35), (1, "#ffb050", 0)], 0, dy1, 0, 1000, user=True)}" style="mix-blend-mode:screen"/>')
    s.add(f'<path d="M{vx - 30} {dy1}L{vx + 30} {dy1}L{vx + 120} 1000H{vx - 120}Z" fill="{s.lin([(0, "#fff0c0", .5), (1, "#fff0c0", 0)], 0, dy1, 0, 1000, user=True)}" filter="{s.blur(10)}" style="mix-blend-mode:screen"/>')
    lines = "".join(f"M{f(vx + t * 90)} {dy1}L{f(vx + t * 1400)} 1000" for t in (-1, -.6, -.2, .2, .6, 1))
    lines += "".join(f"M0 {f(vy + 470 * k)}H1600" for k in depths)
    s.add(f'<path d="{lines}" stroke="#000" stroke-opacity=".3" stroke-width="1.5"/>')
    # brass lamp stands down the aisle, near ones larger
    for k in (0.34, 0.48, 0.68):
        for side in (-1, 1):
            x = vx + side * 230 * k
            ob.brass_lamp(s, x, vy + 470 * k, .38 * k, flames=5, flame_h=26 * k)
    # pillars, back to front
    for k in depths:
        for side in (-1, 1):
            x = vx + side * 330 * k
            yb = vy + 470 * k
            yt = vy - 330 * k
            s.add(pillar(s, x, yb, yt, 64 * k, color=mix("#2a160a", "#120804", k), rim="#ffb860", side=-side, rim_a=.5 + .4 * (1 - k)))
    # hanging bells in the nearer bays
    for k, xs in ((0.48, (-120, 120)), (0.68, (-170, 170))):
        for dx in xs:
            x, top = vx + dx * k * 1.6, vy - 330 * k
            b = 30 * k
            s.add(f'<path d="M{f(x)} {f(top)}V{f(top + 160 * k)}" stroke="#8a5a20" stroke-width="{f(2 * k + .5)}"/>'
                  f'<path d="M{f(x - b * .5)} {f(top + 160 * k + b)}C{f(x - b * .5)} {f(top + 160 * k + b * .2)} {f(x - b * .3)} {f(top + 160 * k)} {f(x)} {f(top + 160 * k)}'
                  f'C{f(x + b * .3)} {f(top + 160 * k)} {f(x + b * .5)} {f(top + 160 * k + b * .2)} {f(x + b * .5)} {f(top + 160 * k + b)}Z" fill="{s.lin(ob.BRASS, 0, 0, 1, 0)}"/>')
    s.add(f'<rect width="{W}" height="{H}" fill="#2a1406" opacity=".15" filter="{s.grain(.5, 2, .2, 3, "#000000")}"/>')
    s.add(f'<g opacity=".55" style="mix-blend-mode:screen">' + "".join(
        f'<path d="M{vx - 40 + i * 20} {dy0}L{vx - 260 + i * 130} 1000L{vx - 200 + i * 130} 1000Z" fill="#ffd8a0" opacity=".06" filter="{s.blur(20)}"/>' for i in range(5)) + '</g>')
    # devotees in the foreground, seen from behind with hands joined
    rim = dict(w=4, color="#ffc070", a=1, blur=1.2, halo=10, halo_a=.25)
    for k in depths[1:5]:
        for side in (-1, 1):
            x = vx + side * 520 * k
            y = vy + 40 * k
            s.add(f'<path d="M{f(x - 22 * k)} {f(y)}h{f(44 * k)}v{f(6 * k)}h{f(-44 * k)}Z" fill="#3a1e0c"/>')
            s.flame(x, y, 18 * k, glow_r=120 * k, glow_a=.45)
    for x, y, sc, kind in ((430, 1190, 4.4, "man"), (590, 1150, 4.0, "veiled"), (1020, 1160, 4.1, "woman"), (1190, 1200, 4.6, "man")):
        s.add(lit(s, place(x, y, sc, back_person(kind, "#0a0503")), toward(x, y - 400, vx, vy), **rim))
    s.motes(30, 500, 1100, 200, 640, color="#ffc070", seed=4, size=(.7, 1.6))
    s.fx("mottle", amp=.035, cell=50)
    s.look = {"vibrance": .08, "bloom": 1.1}
    return s


@scene
def pradakshina(s):
    sun = (1240, 560)
    s.sky([(0, "#161a44"), (.25, "#33306a"), (.45, "#6e4a84"), (.58, "#c06a80"), (.66, "#f29a7a"), (.72, "#ffc896")], 0, 760)
    s.stars(50, 0, 260, seed=2, bright=.55)
    s.sun(*sun, 24, halo_r=520, halo_a=.6)
    s.fx("clouds", y0=60, y1=360, seed=41, cell=140, aniso=3.4, cover=.4, soft=.18, lit="#ffae96", body=.72, direct=.75,
         light=(.4, 1), sun=(sun[0], sun[1], 420), opacity=.9)
    far = ridgeline(600, 40, 71, cell=260, octaves=5, ridged=.3)
    hills(s, far, "#7a5a8a", "#a8708a", haze="#f0b0a0", haze_a=.5, haze_h=40)
    rng = random.Random(6)
    s.add(f'<path d="{"".join(crown(x, 596 - rng.uniform(0, 20), rng.uniform(16, 34), seed=x) for x in range(-30, 1640, 30))}" fill="#4a3460"/>')
    s.mist(600, 50, "#ffc8b0", .5, 12)
    # courtyard
    s.add(f'<rect y="600" width="{W}" height="400" fill="{s.lin([(0, "#3a2a48", 1), (.4, "#2a1c34", 1), (1, "#120c18", 1)], 0, 600, 0, 1000, user=True)}"/>')
    # a sacred peepal behind the shrine
    trng = random.Random(14)
    segs, tips = [], []
    branches(1000, 690, -4, 150, 46, 4, trng, segs, tips, spread=34, shrink=.74)
    leaves = foliage([(x, y, trng.uniform(40, 64)) for x, y, _ in tips], seed=5, fine=12)
    s.add(lit(s, f'<path d="{"".join(segs)}" fill="#1e1428"/><path d="{leaves}" fill="#22162e"/>', toward(1000, 400, *sun), w=3, color="#ffc8a0", a=.8, w2=14, a2=.18))
    # the circle of lamps round a paved path, far half first
    cx, cy, rx, ry = 800, 760, 470, 120
    s.add(f'<ellipse cx="{cx}" cy="{cy + 4}" rx="{rx + 40}" ry="{ry + 22}" fill="{s.rad([(0, "#5a4258", 1), (.7, "#4a3448", 1), (1, "#3a2a40", 1)])}"/>')
    flag = []
    for k in range(48):
        a = 2 * math.pi * k / 48
        flag.append(f"M{f(cx + math.cos(a) * (rx - 120))} {f(cy + math.sin(a) * (ry - 30))}L{f(cx + math.cos(a) * (rx + 40))} {f(cy + 4 + math.sin(a) * (ry + 22))}")
    s.add(f'<path d="{"".join(flag)}" stroke="#2a1c30" stroke-opacity=".5" stroke-width="1.4"/>'
          f'<ellipse cx="{cx}" cy="{cy}" rx="{rx - 120}" ry="{ry - 30}" fill="none" stroke="#2a1c30" stroke-opacity=".5" stroke-width="1.4"/>')
    ring = [(cx + math.cos(a) * rx, cy + math.sin(a) * ry, a) for a in [2 * math.pi * k / 60 for k in range(60)]]
    s.add(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx + 20}" ry="{ry + 12}" fill="none" stroke="#ffb060" stroke-opacity=".15" stroke-width="40" filter="{s.blur(20)}"/>')
    def lamps(pred):
        for x, y, a in ring:
            if pred(y):
                k = .6 + .5 * (y - (cy - ry)) / (2 * ry)
                s.add(f'<ellipse cx="{f(x)}" cy="{f(y + 6 * k)}" rx="{f(30 * k)}" ry="{f(8 * k)}" fill="#ffa050" opacity=".25" filter="{s.blur(6)}" style="mix-blend-mode:screen"/>'
                      f'<ellipse cx="{f(x)}" cy="{f(y + 3 * k)}" rx="{f(9 * k)}" ry="{f(3.6 * k)}" fill="#6a2a10"/>')
                s.flame(x, y, 15 * k, glow_r=60 * k, glow_a=.35)
    lamps(lambda y: y < cy)
    # walkers on the far side, moving right behind the shrine
    walk = dict(w=3, color="#ffb070", a=.95, w2=12, a2=.25)
    for x, y, sc, sp in ((520, 690, 1.05, dict(dress="sari", stride=12, arm=(25, 160), arm2=(25, 160), hair="bun")),
                         (1080, 692, 1.0, dict(dress="dhoti", stride=14, arm=(25, 160), arm2=(25, 160), hair="shikha"))):
        svg, _ = person(color="#160e1c", **sp)
        s.add(lit(s, place(x, y, sc, svg), 180 if x > cx else 0, **walk))
    # the shrine on its plinth
    s.add(f'<path d="M640 712L960 712L990 736H610Z" fill="#3a2a40"/><path d="M610 736H990V752H610Z" fill="#241a2c"/>'
          f'<path d="M610 736H990" stroke="#ffc890" stroke-opacity=".6" stroke-width="2"/>')
    arch.nagara(s, 836, 714, 1.15, color="#3a2c44", rim="#ffcf9e", light=1, shade="#000000", door="#ffb45c", flag_color="#ef7a22")
    s.glow(735, 690, 120, "#ffb050", .5, .25)
    lamps(lambda y: y >= cy)
    # walkers on the near side, moving left with the shrine on their right
    for x, y, sc, sp in ((560, 872, 1.6, dict(dress="sari", stride=14, arm=(30, 105), arm2=(20, 120), hair="bun", prop="plate")),
                         (900, 884, 1.66, dict(dress="dhoti", stride=16, arm=(25, 160), arm2=(25, 160), hair="short")),
                         (1150, 868, 1.55, dict(dress="sari", stride=12, arm=(25, 160), arm2=(25, 160), hair="shawl"))):
        svg, hand = person(color="#140c18", **sp)
        s.add(lit(s, place(x, y, sc, svg, flip=True), toward(x, y - 80, cx, 700), **walk))
        if sp.get("prop") == "plate":
            s.flame(x - (hand[0] + 2) * sc, y + (hand[1] - 3) * sc, 12, glow_r=60, glow_a=.5)
    s.birds(6, 1060, 1300, 380, 440, color="#3a2040", s=(5, 9), seed=7, a=.8)
    s.fx("godrays", cx=sun[0], cy=sun[1], strength=.3, thresh=.72, decay=.97, radius=200)
    s.fx("mottle", amp=.045, cell=60)
    return s


@scene
def family(s):
    # dusk outside a home; the door stands open on lamplight
    s.sky([(0, "#141838"), (.4, "#2e2a5a"), (.7, "#7a4a74"), (.85, "#c86a6a"), (1, "#f0a070")], 0, 760)
    s.stars(40, 1000, 360, seed=9, bright=.6, x0=1000, x1=1600)
    s.moon(1400, 170, 22, glow_r=200, sky="#1c1e44", crescent=.55)
    far = ridgeline(760, 40, 81, cell=200, octaves=5, ridged=.3)
    rng = random.Random(5)
    s.add(f'<path d="{foliage([(x, 750 - rng.uniform(0, 30), rng.uniform(30, 50)) for x in range(980, 1680, 60)], seed=4, fine=8)}" fill="#2a1e3a"/>')
    # ground: a swept courtyard
    s.add(f'<rect y="760" width="{W}" height="240" fill="{s.lin([(0, "#3a2630", 1), (1, "#160e14", 1)], 0, 760, 0, 1000, user=True)}"/>')
    # the house wall, door frame and lit interior
    wall = s.lin([(0, "#5a3a3a", 1), (1, "#3a2430", 1)], 0, 0, 1, 0)
    s.add(f'<path d="M-20 60H1020V790H-20Z" fill="{wall}"/>')
    s.add(f'<path d="M-20 60H1020V790H-20Z" fill="#fff" filter="{s.grain(.02, 4, .25, 3, "#000000")}" opacity=".35"/>')
    s.add(f'<path d="M-30 40H1050L1030 70H-30Z" fill="#2a1820"/><path d="M1020 60V790" stroke="#000" stroke-opacity=".3" stroke-width="6"/>')
    s.add(f'<rect x="-20" y="700" width="1040" height="90" fill="#6a2a22"/><path d="M-20 700H1020" stroke="#f0d8b0" stroke-opacity=".5" stroke-width="5" stroke-dasharray="2 10"/>')
    s.add(f'<rect x="110" y="300" width="160" height="170" fill="#2a1408"/><rect x="122" y="312" width="136" height="146" fill="{s.rad([(0, "#ffd890", 1), (1, "#b04a14", 1)], .5, .6, .7)}"/>'
          + "".join(f'<rect x="{x}" y="312" width="7" height="146" fill="#3a1a0a"/>' for x in range(136, 258, 22)) +
          f'<path d="M100 300H280L270 286H110Z" fill="#3a1a0a"/>')
    s.glow(190, 390, 200, "#ffb050", .35, .25)
    dx0, dx1, dy0, dy1 = 420, 640, 250, 780
    s.add(f'<path d="M{dx0 - 40} {dy1 + 8}V{dy0 - 50}H{dx1 + 40}V{dy1 + 8}Z" fill="#3a1e12"/>')
    s.add(f'<path d="M{dx0 - 40} {dy1 + 8}V{dy0 - 50}H{dx1 + 40}V{dy1 + 8}Z" fill="none" stroke="#6a3a1c" stroke-width="10"/>')
    s.add(f'<path d="M{dx0 - 28} {dy1}V{dy0 - 38}H{dx1 + 28}V{dy1}" fill="none" stroke="#c88a40" stroke-opacity=".45" stroke-width="3" stroke-dasharray="3 5"/>')
    s.add(f'<rect x="{dx0}" y="{dy0}" width="{dx1 - dx0}" height="{dy1 - dy0}" fill="{s.rad([(0, "#fff2c0", 1), (.45, "#ffb24a", 1), (1, "#a8441a", 1)], .5, .7, .8)}"/>')
    # inside: an open door leaf and a lamp niche
    s.add(f'<path d="M{dx0} {dy0}L{dx0 + 46} {dy0 + 26}V{dy1 - 14}L{dx0} {dy1}Z" fill="#5a2a10"/>')
    s.add(f'<path d="M{dx1} {dy0}L{dx1 - 40} {dy0 + 24}V{dy1 - 12}L{dx1} {dy1}Z" fill="#6a3214"/>')
    s.add(f'<path d="M{dx0 + 60} {dy0 + 90}h100v120h-100Z" fill="#c8682a" opacity=".5"/><path d="M{dx0 + 70} {dy0 + 100}h80v100h-80Z" fill="#7a2a0c" opacity=".55"/>')
    s.flame(530, dy0 + 196, 16, glow_r=80, glow_a=.5)
    ob.brass_lamp(s, 530, 768, .5, flames=5, flame_h=24)
    s.glow(530, 640, 300, "#ffc060", .5, .25)
    # torana of mango leaves and marigolds above the door
    leaves = "".join(f'<path d="M{x} {dy0 - 50}C{x - 7} {dy0 - 30} {x - 4} {dy0 - 14} {x} {dy0 - 6}C{x + 4} {dy0 - 14} {x + 7} {dy0 - 30} {x} {dy0 - 50}Z" fill="{"#2f6a2a" if (x // 20) % 2 else "#3f7a30"}"/>' for x in range(dx0 - 30, dx1 + 40, 20))
    s.add(leaves)
    ob.garland(s, dx0 - 36, dy0 - 52, dx1 + 36, dy0 - 52, 8, r=8, seed=3, tassel=False)
    # threshold, rangoli and diyas
    s.add(f'<path d="M{dx0 - 60} {dy1 + 8}H{dx1 + 60}V{dy1 + 22}H{dx0 - 60}Z" fill="#5a3a2a"/>')
    rc, ry_ = 530, 880
    rang = []
    for k in range(16):
        a = 2 * math.pi * k / 16
        rang.append(f'<ellipse cx="{f(rc + math.cos(a) * 70)}" cy="{f(ry_ + math.sin(a) * 18)}" rx="18" ry="6" fill="{["#f2b632", "#e8562a", "#f6efe0", "#c8241e"][k % 4]}" opacity=".85" transform="rotate({f(math.degrees(a) * .25)} {f(rc + math.cos(a) * 70)} {f(ry_ + math.sin(a) * 18)})"/>')
    s.add(f'<ellipse cx="{rc}" cy="{ry_}" rx="110" ry="30" fill="none" stroke="#f6efe0" stroke-width="3" opacity=".7"/>{"".join(rang)}'
          f'<ellipse cx="{rc}" cy="{ry_}" rx="30" ry="8" fill="#e8562a" opacity=".9"/><ellipse cx="{rc}" cy="{ry_}" rx="14" ry="4" fill="#f2b632"/>')
    for x in (dx0 - 40, dx1 + 40, 400, 660):
        ob.clay_diya(s, x, dy1 + 6 if x in (dx0 - 40, dx1 + 40) else 920, .18, flame_h=24, dots=False)
    # a tulsi pedestal in the courtyard
    s.add(f'<path d="{palm(1120, 770, 320, seed=2, lean=.12)}{palm(1480, 760, 380, seed=3, lean=-.08)}{palm(1560, 780, 260, seed=4, lean=.1)}" fill="#1e1428"/>')
    tg = s.lin([(0, "#c87a4a", 1), (.5, "#9a4a2a", 1), (1, "#4a2018", 1)], 0, 0, 1, 0)
    s.add(f'<path d="M1180 820H1300L1290 700H1190Z" fill="{tg}"/><path d="M1172 700H1308V684H1172ZM1170 820H1310V832H1170Z" fill="#d89a6a"/>'
          f'<path d="M1222 790V740C1222 728 1258 728 1258 740V790Z" fill="#2a0c06"/><path d="M1190 712H1290" stroke="#f6efe0" stroke-width="3" stroke-dasharray="4 6"/>')
    s.flame(1240, 786, 16, glow_r=70, glow_a=.5)
    tb = "".join(f'<path d="M1240 684Q{1240 + dx * .3} {684 - h * .6} {1240 + dx} {684 - h}" stroke="#2a4a2a" stroke-width="3" fill="none"/>' for dx, h in ((-30, 80), (-12, 100), (8, 104), (26, 84), (0, 70)))
    tl = "".join(crown(1240 + dx, 684 - h, 14, seed=int(h)) for dx, h in ((-30, 80), (-12, 100), (8, 104), (26, 84)))
    s.add(tb + f'<path d="{tl}" fill="#2a5a2a"/>')
    ob.clay_diya(s, 1225, 690, .15, flame_h=20, dots=False)
    # host and guest greet each other with namaste
    host, _ = person(dress="sari", stride=0, head=4, arm=(22, 158), arm2=(22, 158), hair="bun", color="#120a10")
    guest, _ = person(dress="dhoti", stride=0, head=10, lean=3, arm=(22, 158), arm2=(22, 158), hair="short", color="#120a10")
    s.add(lit(s, place(706, 808, 4.2, host), 180, w=4, color="#ffc070", a=1, w2=26, a2=.45))
    s.add(f'<ellipse cx="760" cy="812" rx="260" ry="40" fill="#ffb060" opacity=".25" filter="{s.blur(20)}" style="mix-blend-mode:screen"/>')
    s.add(lit(s, place(930, 812, 4.4, guest, flip=True), 180, w=4, color="#ffc070", a=1, w2=34, a2=.55))
    s.add(lit(s, place(930, 812, 4.4, guest, flip=True), 0, w=2, color="#8a7ab8", a=.6))
    s.motes(26, 300, 1100, 200, 760, color="#ffc070", seed=3, size=(.7, 1.6))
    s.fx("mottle", amp=.04, cell=60)
    return s


# ---------------------------------------------------------------- hands
def _finger(bx, by, ang, L, w0, w1, curl=4.0):
    """A finger from its base (bx, by) pointing up at ang degrees (+ = outward), as joint circles."""
    a = math.radians(ang)
    ux, uy = math.sin(a), -math.cos(a)
    px, py = -uy, ux
    pts = []
    for t, w in ((0, w0), (.38, (w0 * .6 + w1 * .4) * .98), (.7, (w0 * .3 + w1 * .7) * .96), (1, w1)):
        c = curl * math.sin(t * math.pi * .9)
        pts.append((bx + ux * L * t + px * c, by + uy * L * t + py * c, w / 2))
    return pts


def open_hand(light=(-70, -110), skin="#9a5c3a", shade="#1e0e08", s=None):
    """The viewer's right one of two open hands held up together, palm toward us, in its own
    upright frame: wrist centre at the origin, fingers up. Real proportions: palm 108, middle
    finger 82, thumb from the thenar mound; returns SVG."""
    g = s.rad([(0, mix(skin, "#ffd0a0", .45), 1), (.3, skin, 1), (.7, mix(skin, shade, .5), 1), (1, shade, 1)], light[0], light[1], 260, user=True)
    dk = mix(shade, "#000000", .3)
    fingers = [(-30, -100, -9, 58, 15.5, 12.5), (-11, -107, -3, 73, 17.5, 13.5), (9, -109, 2, 81, 18, 14), (28, -103, 8, 73, 18, 14)]
    out = []
    # forearm, widening toward the elbow
    out.append(f'<path d="M-25 -6C-27 60 -30 150 -34 300H38C36 150 32 60 27 -6Z" fill="{s.lin([(0, mix(skin, shade, .55), 1), (.3, shade, 1), (1, "#0e0705", 1)], 0, -10, 0, 130, user=True)}"/>')
    # palm with the hypothenar and thenar mounds
    palm = ("M-28 4C-35 -24 -43 -62 -41 -98C-40 -106 -32 -110 -24 -110L36 -108C42 -104 44 -96 42 -86"
            "C40 -74 41 -64 44 -56C40 -36 34 -14 28 4Z")
    out.append(f'<path d="{palm}" fill="{g}"/>')
    thumb = _finger(36, -46, 30, 68, 25, 15, curl=-6)
    out.append(f'<path d="{limb(*thumb)}" fill="{g}"/>')
    # soft dark edges under all the fingers first, so neighbours separate without rings
    edges = "".join(limb(*_finger(bx, by, ang, L, w0 + 2.4, w1 + 2.4)) for bx, by, ang, L, w0, w1 in fingers)
    out.append(f'<path d="{edges}" fill="{shade}" opacity=".5" filter="{s.blur(.8)}"/>')
    out.append(f'<path d="{"".join(limb(*_finger(bx, by, ang, L, w0, w1)) for bx, by, ang, L, w0, w1 in fingers)}" fill="{g}"/>')
    # separations between fingers, joints and palm lines
    seps = []
    for (bx, by, ang, L, w0, w1) in fingers:
        pts = _finger(bx, by, ang, L, w0, w1)
        for (x, y, r), (x2, y2, r2) in ((pts[1], pts[1]), (pts[2], pts[2])):
            a = math.radians(ang)
            seps.append(f"M{f(x - math.cos(a) * r * .7)} {f(y - math.sin(a) * r * .7)}L{f(x + math.cos(a) * r * .7)} {f(y + math.sin(a) * r * .7)}")
    out.append(f'<path d="M-38 -76C-18 -82 6 -84 30 -96M-36 -58C-16 -60 6 -64 22 -74M18 -100C14 -70 14 -40 22 -10" stroke="{shade}" stroke-opacity=".18" stroke-width="1.6" fill="none" filter="{s.blur(.6)}"/>')
    tips = "".join(f'<circle cx="{f(p[-1][0])}" cy="{f(p[-1][1] - p[-1][2] * .3)}" r="{f(p[-1][2] * .7)}"/>' for p in
                   [_finger(bx, by, ang, L, w0, w1) for bx, by, ang, L, w0, w1 in fingers])
    out.append(f'<g fill="#ffe2b8" opacity=".22" filter="{s.blur(2)}">{tips}</g>')
    return "".join(out)


def cupped_hands(s, cx, cy, sc=1.0, tilt=17, gap=46):
    """A pair of open hands held up side by side, palms toward the viewer."""
    one = open_hand(s=s)
    return (f'<g transform="translate({f(cx)} {f(cy)}) scale({f(sc)})">'
            f'<g transform="translate({gap} 0) rotate({tilt})">{one}</g>'
            f'<g transform="scale(-1 1) translate({gap} 0) rotate({tilt})">{one}</g></g>')


def cupped_side(s, cx, cy, sc=1.0, skin="#2c170e", far="#1a0c07", rim="#ffc884"):
    """Two hands cupped together, seen from the side, holding something up; (cx, cy) is the
    middle of the cup's opening. Returns SVG."""
    from land import smooth_line
    near = [(-560, 330), (-330, 170), (-215, 78), (-130, 44), (-20, 34), (80, 18), (140, -8), (178, -46), (198, -84),
            (194, -108), (178, -112), (164, -92), (138, -64), (100, -46), (40, -40), (-40, -42), (-82, -58), (-96, -96),
            (-104, -128), (-118, -136), (-134, -122), (-146, -84), (-160, -48), (-190, -26), (-300, 60), (-470, 190), (-600, 260)]
    farh = [(x + 34, y - 26) for x, y in near[6:15]] + [(110, -52), (40, -50)]

    def path(pts, closed=True):
        sm = smooth_line(pts, 5)
        return "M" + "L".join(f"{f(cx + x * sc)} {f(cy + y * sc)}" for x, y in sm) + ("Z" if closed else "")
    body = s.lin([(0, "#5a3020", 1), (0.35, skin, 1), (1, "#0c0604", 1)], 0, cy - 120 * sc, 0, cy + 200 * sc, user=True)
    fingers = "".join(path([(186 - k * 9, -100 + k * 14), (176 - k * 12, -70 + k * 16), (150 - k * 14, -34 + k * 14)], False) for k in range(3))
    rim_top = path(near[10:17], False)
    rim_tip = path(near[7:11], False)
    rim_thumb = path(near[16:23], False)
    return (f'<path d="{path(farh)}" fill="{far}"/>'
            f'<path d="{path(farh[1:7], False)}" stroke="{rim}" stroke-width="{f(2.4 * sc)}" fill="none" opacity=".7"/>'
            f'<path d="{path(near)}" fill="{body}"/>'
            f'<path d="{fingers}" stroke="#000" stroke-opacity=".28" stroke-width="{f(5 * sc)}" fill="none" filter="{s.blur(2 * sc)}"/>'
            f'<g filter="{s.blur(1.2 * sc)}"><path d="{rim_top}" stroke="{rim}" stroke-width="{f(3.4 * sc)}" fill="none" opacity=".9"/>'
            f'<path d="{rim_tip}" stroke="{rim}" stroke-width="{f(2.6 * sc)}" fill="none" opacity=".7"/>'
            f'<path d="{rim_thumb}" stroke="{rim}" stroke-width="{f(2.6 * sc)}" fill="none" opacity=".75"/></g>')


@scene
def hands_offering(s):
    ob.dark_room(s, light=(800, 420), base="#0e0705", warm="#4a2410", r=1000, horizon=1000, floor="#0e0705")
    s.bokeh(14, 0, 1600, 40, 900, colors=("#ff9a3a", "#ffc060", "#e86a3a"), r=(30, 90), a=(.06, .18), blur=6, seed=4, ring=True)
    s.bokeh(40, 0, 1600, 0, 1000, colors=("#ffb050",), r=(4, 12), a=(.15, .4), blur=3, seed=5)
    s.glow(820, 470, 720, "#ff9a40", .32, .2)
    hx, hy, sc = 830, 640, 1.55
    # the lamp sits in the cup of the hands; the hands are drawn over its lower half
    ob.clay_diya(s, hx - 150, hy - 118, .86, flame_h=190, dots=True)
    s.add(cupped_side(s, hx, hy, sc))
    s.glow(hx - 20, hy - 40, 260, "#ff9a40", .25, .3, sy=.5)
    rng = random.Random(3)
    pet = []
    for _ in range(9):
        x = hx + rng.uniform(-60, 240)
        y = hy - rng.uniform(50, 80)
        r = rng.uniform(8, 14)
        c = rng.choice(["#f39a1c", "#f7b52a", "#e8562a", "#c91e3a", "#f39a1c"])
        a = rng.uniform(0, 180)
        pet.append(f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(r)}" ry="{f(r * .5)}" fill="{c}" transform="rotate({a:.0f} {f(x)} {f(y)})"/>'
                   f'<ellipse cx="{f(x)}" cy="{f(y - r * .12)}" rx="{f(r * .5)}" ry="{f(r * .18)}" fill="#fff2c0" opacity=".35" transform="rotate({a:.0f} {f(x)} {f(y)})"/>')
    s.add("".join(pet))
    s.add(ob.marigold(hx + 70, hy - 52, 17, "#f39a1c", 3) + ob.marigold(hx + 110, hy - 60, 14, "#f7c02a", 4))
    s.motes(40, 560, 1100, 120, 480, color="#ffd080", seed=7, size=(.8, 1.8))
    s.fx("mottle", amp=.035, cell=50)
    s.look = {"bloom": 1.1}
    return s


@scene
def four_goals(s):
    top = (800, 210)
    cx, cy, rx, ry = 800, 770, 500, 150
    s.sky([(0, "#04061a"), (.4, "#0c1236"), (.7, "#1a1a44"), (1, "#100c22")])
    s.stars(220, 0, 640, seed=13, bright=.9)
    s.add(f'<rect width="{W}" height="{H}" fill="{s.rad([(0, "#5a4aa0", .35), (.5, "#3a2a70", .12), (1, "#000", 0)], 800, 300, 700, user=True)}"/>')
    # a dark stone floor, the lotus mandala painted on it
    s.add(f'<rect y="560" width="{W}" height="440" fill="{s.lin([(0, "#14122a", 1), (1, "#06050e", 1)], 0, 560, 0, 1000, user=True)}"/>')
    s.mist(565, 70, "#4a4a8a", .45, 16)
    def ell(r, n=96, rot=0.0, wob=0.0, k=0):
        return [(cx + math.cos(a) * r * rx / 500 * (1 + wob * math.cos(k * a)), cy + math.sin(a) * r * ry / 500 * (1 + wob * math.cos(k * a)))
                for a in [rot + 2 * math.pi * i / n for i in range(n)]]
    mand = []
    for r, col, wd in ((520, "#d4a84a", 3), (500, "#d4a84a", 1.4), (300, "#d4a84a", 2), (120, "#d4a84a", 2)):
        mand.append(f'<path d="{pts_d(ell(r))}" fill="none" stroke="{col}" stroke-width="{wd}"/>')
    for n, r0, r1, col in ((16, 300, 480, "#ff5a7a"), (8, 120, 290, "#ffc84a")):
        for i in range(n):
            a = 2 * math.pi * (i + .5) / n
            a1, a2 = a - math.pi / n * .9, a + math.pi / n * .9
            P = lambda r, ang: (cx + math.cos(ang) * r * rx / 500, cy + math.sin(ang) * r * ry / 500)
            p0, pl, pr, pt = P(r0, a1), P(r0 + (r1 - r0) * .55, a - math.pi / n * .75), P(r0 + (r1 - r0) * .55, a + math.pi / n * .75), P(r1, a)
            p0b = P(r0, a2)
            mand.append(f'<path d="M{f(p0[0])} {f(p0[1])}Q{f(pl[0])} {f(pl[1])} {f(pt[0])} {f(pt[1])}Q{f(pr[0])} {f(pr[1])} {f(p0b[0])} {f(p0b[1])}Z" fill="{col}" fill-opacity=".38" stroke="#ffd890" stroke-width="1.8"/>')
    mand.append(f'<path d="{pts_d(ell(60))}" fill="#e8c070" fill-opacity=".5"/>')
    s.add(f'<g opacity=".9">{"".join(mand)}</g>')
    s.add(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx * 1.1}" ry="{ry * 1.1}" fill="{s.rad([(0, "#ffe0a0", .25), (1, "#ffe0a0", 0)])}" style="mix-blend-mode:screen"/>')
    # four lamps at the cardinal points: dharma, artha, kama, moksha
    lamps = [((cx, cy - ry - 10), "#fff4d0", "#e8d8b0", .95), ((cx - rx - 20, cy), "#7ae0a8", "#2a8a5a", 1.25),
             ((cx + rx + 20, cy), "#ff7aa0", "#b0284a", 1.25), ((cx, cy + ry + 20), "#8ab0ff", "#3a4ab0", 1.5)]
    # beams of their light rising to meet at one point
    beam = []
    for (x, y), glow_c, body, k in lamps:
        g = s.lin([(0, glow_c, .55), (.6, glow_c, .25), (1, "#ffffff", .5)], x, y, top[0], top[1], user=True)
        w0 = 34 * k
        beam.append(f'<path d="M{f(x - w0)} {f(y - 20 * k)}L{f(top[0] - 3)} {f(top[1])}L{f(top[0] + 3)} {f(top[1])}L{f(x + w0)} {f(y - 20 * k)}Z" fill="{g}"/>')
    s.add(f'<g filter="{s.blur(12)}" style="mix-blend-mode:screen">{"".join(beam)}</g>')
    s.add(f'<g filter="{s.blur(3)}" style="mix-blend-mode:screen" opacity=".6">{"".join(beam).replace("34", "10")}</g>')
    for (x, y), glow_c, body, k in sorted(lamps, key=lambda l: l[0][1]):
        s.glow(x, y - 20 * k, 220 * k, glow_c, .45, .2)
        cl = s.lin([(0, mix(body, "#ffffff", .35), 1), (.5, body, 1), (1, mix(body, "#000000", .6), 1)], 0, 0, 0, 1)
        s.add(f'<ellipse cx="{f(x)}" cy="{f(y + 16 * k)}" rx="{f(60 * k)}" ry="{f(12 * k)}" fill="#000" opacity=".5" filter="{s.blur(6)}"/>'
              f'<path d="M{f(x - 46 * k)} {f(y)}C{f(x - 42 * k)} {f(y + 22 * k)} {f(x - 20 * k)} {f(y + 28 * k)} {f(x)} {f(y + 28 * k)}C{f(x + 20 * k)} {f(y + 28 * k)} {f(x + 42 * k)} {f(y + 22 * k)} {f(x + 46 * k)} {f(y)}Z" fill="{cl}"/>'
              f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(46 * k)}" ry="{f(8 * k)}" fill="{mix(body, "#ffffff", .3)}"/><ellipse cx="{f(x)}" cy="{f(y + 1)}" rx="{f(38 * k)}" ry="{f(5 * k)}" fill="#3a2008"/>'
              f'<path d="M{f(x - 44 * k)} {f(y + 8 * k)}C{f(x - 20 * k)} {f(y + 16 * k)} {f(x + 20 * k)} {f(y + 16 * k)} {f(x + 44 * k)} {f(y + 8 * k)}" stroke="#ffd870" stroke-width="{f(2 * k)}" fill="none" opacity=".8"/>')
        s.flame(x, y - 2, 46 * k, glow_r=120 * k, glow_a=.5)
    # where the four lights meet
    s.glow(*top, 240, "#ffffff", .35, .2)
    s.glow(*top, 60, "#fff8e0", .9, .3)
    s.add(s.sparkle(top[0], top[1], 46, "#ffffff", 1))
    s.add(f'<circle cx="{top[0]}" cy="{top[1]}" r="8" fill="#fff"/>')
    s.motes(60, 300, 1300, 160, 760, color="#e8e0ff", seed=8, size=(.7, 1.6))
    s.fx("godrays", cx=top[0], cy=top[1], strength=.35, thresh=.78, decay=.97, radius=200)
    s.fx("mottle", amp=.035, cell=60)
    return s


def cottage(s, x, base, sc=1.0, wall="#8a5a3a", roof="#6a4a2a", door="#ffb24a"):
    """A village home: mud walls, a thatched roof and a lamp-lit doorway."""
    inner = (f'<path d="M-60 0V-46H60V0Z" fill="{wall}"/>'
             f'<path d="M-74 -42C-50 -60 -20 -84 0 -92C20 -84 50 -60 74 -42C40 -46 -40 -46 -74 -42Z" fill="{roof}"/>'
             f'<path d="M-70 -44C-40 -48 40 -48 70 -44" stroke="#3a2412" stroke-width="3" fill="none"/>'
             f'<path d="M-12 0V-30C-12 -36 12 -36 12 -30V0Z" fill="{door}"/>'
             f'<rect x="28" y="-34" width="16" height="14" fill="{door}" opacity=".85"/>'
             f'<path d="M-60 -2H60" stroke="#f0d8b0" stroke-opacity=".5" stroke-width="2" stroke-dasharray="2 5"/>')
    return place(x, base, sc, inner)


@scene
def ashramas(s):
    sun = (930, 470)
    # one sky across four seasons: fresh spring morning, golden summer, amber autumn, cold winter
    s.add(f'<rect width="{W}" height="{H}" fill="{s.lin([(0, "#bcd8e8"), (.28, "#f6dca0"), (.55, "#f6a878"), (.78, "#9a8ab8"), (1, "#4a5a90")], 0, 0, 1600, 0, user=True)}"/>')
    s.add(f'<rect width="{W}" height="{H}" fill="{s.lin([(0, "#1a2050", .75), (.45, "#1a2050", .1), (.6, "#1a2050", 0)], 0, 0, 0, 1000, user=True)}"/>')
    s.sun(*sun, 26, halo_r=520, halo_a=.55)
    s.stars(40, 0, 300, seed=6, bright=.7, x0=1250, x1=1600)
    s.moon(1480, 130, 16, glow_r=140, sky="#36447a", crescent=.5)
    s.fx("clouds", y0=80, y1=380, seed=51, cell=130, aniso=3.6, cover=.36, soft=.2, lit="#fff0e0", body=.85, direct=.8,
         light=(0, 1), sun=(sun[0], sun[1], 400), opacity=.7)
    # mountains rising toward winter
    far = peak_line(640, [(150, 60, 220), (520, 80, 260), (900, 120, 260), (1250, 300, 230, .1), (1480, 360, 240), (1660, 280, 200)], 61, shape=1.25, floor=20)
    mountains(s, far, "#8a7aa0", "#c0a0ac", lit="#ffd8c0", lit_a=.7, light=-1, seed=8, snow="#d0d6ea", snow_shade="#a0aad0",
              lit_snow="#fff6ec", snowline=520, snow_fingers=50, rim="#fff0e0", rim_center=sun, rim_r=700, haze="#f8d8c8", haze_a=.5, haze_h=140)
    s.mist(640, 90, "#fff0e8", .45, 24)
    # the ground, its colour turning with the seasons
    g = smooth_line([(-60, 760), (200, 740), (420, 770), (640, 756), (880, 780), (1100, 760), (1320, 740), (1660, 720)], 8)
    gg = s.lin([(0, "#6aa860"), (.27, "#c8b048"), (.5, "#c8782e"), (.66, "#a8785e"), (.76, "#c8c4d0"), (.84, "#dce4f2"), (1, "#c8d4ec")], 0, 0, 1600, 0, user=True)
    s.add(f'<path d="{pts_d(g + [(1660, 1010), (-60, 1010)])}" fill="{gg}"/>')
    s.add(f'<path d="{pts_d(g + [(1660, 1010), (-60, 1010)])}" fill="{s.lin([(0, "#000", 0), (1, "#0a0820", .7)], 0, 740, 0, 1000, user=True)}"/>')
    s.add(f'<path d="M{" L".join(f"{f(x)} {f(y)}" for x, y in g)}" stroke="#fff4e0" stroke-opacity=".35" stroke-width="2" fill="none"/>')
    # a path winding through all four seasons
    path = smooth_line([(-40, 900), (300, 860), (600, 880), (900, 840), (1200, 820), (1500, 770), (1660, 750)], 6)
    s.add(f'<path d="{ribbon(path, 40, 14)}" fill="#f6e8c8" opacity=".35"/>')
    rng = random.Random(7)
    # spring: blossoming trees
    for x, h in ((80, 210), (250, 170), (360, 140)):
        b = y_at(g, x) + 6
        segs, tips = [], []
        branches(x, b, 0, h * .4, h * .08, 3, rng, segs, tips, spread=34, shrink=.72)
        s.add(f'<path d="{"".join(segs)}" fill="#4a3030"/><path d="{foliage([(tx, ty, h * .14) for tx, ty, _ in tips], seed=x, fine=8)}" fill="#e8a0b4"/>')
        s.add("".join(f'<circle cx="{f(tx + rng.uniform(-20, 20))}" cy="{f(ty + rng.uniform(-16, 16))}" r="{f(rng.uniform(2, 4))}" fill="#fff0f4" opacity=".8"/>' for tx, ty, _ in tips for _ in range(4)))
    grass(s, -40, 420, lambda x: y_at(g, x) + 3, 120, h=(6, 18), color="#3a6a3a", seed=3)
    # summer: the householders' cottage under a great green tree
    segs, tips = [], []
    branches(640, y_at(g, 640) + 6, 2, 90, 22, 3, rng, segs, tips, spread=32, shrink=.74)
    s.add(f'<path d="{"".join(segs)}" fill="#3a2a1a"/><path d="{foliage([(tx, ty, 46) for tx, ty, _ in tips], seed=2, fine=10)}" fill="#3a6a2a"/>')
    s.add(cottage(s, 530, y_at(g, 530) + 4, 1.1))
    s.glow(530, y_at(g, 530) - 20, 90, "#ffb050", .4, .25)
    # autumn: the forest edge in flame colours, leaves falling
    for k in range(9):
        x = 900 + k * 34 + rng.uniform(-10, 10)
        b = y_at(g, x) + 6
        h = rng.uniform(150, 230)
        segs, tips = [], []
        branches(x, b, rng.uniform(-4, 4), h * .38, h * .07, 3, rng, segs, tips, spread=30, shrink=.72)
        col = rng.choice(["#c8501e", "#e07a26", "#b8361e", "#d89a30"])
        s.add(f'<path d="{"".join(segs)}" fill="#3a1e14"/><path d="{foliage([(tx, ty, h * .12) for tx, ty, _ in tips], seed=x, fine=7)}" fill="{col}"/>')
    for _ in range(40):
        lx, ly = rng.uniform(860, 1240), rng.uniform(620, 860)
        s.add(f'<ellipse cx="{f(lx)}" cy="{f(ly)}" rx="4.5" ry="2" fill="{rng.choice(["#e07a26", "#c8501e", "#f2b632"])}" transform="rotate({rng.randint(0, 180)} {f(lx)} {f(ly)})" opacity=".85"/>')
    # winter: snow, bare trees and dark pines below the peaks
    for x in (1290, 1340, 1530):
        segs, tips = [], []
        branches(x, y_at(g, x) + 6, rng.uniform(-6, 6), 60, 9, 4, rng, segs, tips, spread=30, shrink=.72)
        s.add(f'<path d="{"".join(segs)}" fill="#4a4258"/>')
    pines(s, 1380, 1620, 0, 9, h=(60, 120), color="#2a3048", seed=4, ground_fn=lambda x: y_at(g, x))
    s.add(f'<path d="{"".join(f"M{f(x)} {f(y_at(g, x) + 2)}c6 -3 14 -3 20 0" for x in range(1260, 1600, 26))}" stroke="#ffffff" stroke-opacity=".6" stroke-width="3" fill="none"/>')
    s.motes(60, 1240, 1600, 80, 900, color="#ffffff", seed=5, size=(1, 2.2), glow=2)
    # the four stages of life
    walk = dict(w=2.2, color="#fff0d0", a=.9, w2=8, a2=.25)
    child, _ = person(dress="child", stride=16, arm=(30, 130), prop="books", hair="shikha", age="child", color="#1e1824")
    s.add(lit(s, place(300, y_at(path, 300) + 2, .82, child), toward(300, 800, *sun), **walk))
    man, _ = person(dress="dhoti", stride=0, arm=(10, 20), arm2=(20, 40), hair="short", color="#1e1824")
    wife, _ = person(dress="sari", stride=0, arm=(20, 60), hair="bun", color="#1e1824")
    s.add(lit(s, place(612, y_at(g, 612) + 30, .98, man, flip=True), toward(612, 760, *sun), **walk))
    s.add(lit(s, place(650, y_at(g, 650) + 32, .92, wife, flip=True), toward(650, 760, *sun), **walk))
    old1, _ = person(dress="dhoti", stride=10, lean=12, head=4, arm=(30, 14), prop="staff", hair="short", color="#1e1824")
    old2, _ = person(dress="sari", stride=8, lean=10, head=4, arm=(30, 16), prop="staff", hair="shawl", color="#1e1824")
    s.add(lit(s, place(1036, y_at(path, 1036) + 4, .9, old1), toward(1036, 820, *sun), **walk))
    s.add(lit(s, place(990, y_at(path, 990) + 6, .86, old2), toward(990, 820, *sun), **walk))
    monk, _ = person(dress="robe", stride=14, lean=3, arm=(35, 25), arm2=(-10, -20), prop="staff", hair="jata", color="#1e1824")
    s.add(lit(s, place(1420, y_at(path, 1420) + 2, .92, monk), toward(1420, 780, *sun), **walk))
    s.birds(7, 700, 1000, 300, 380, color="#4a3040", s=(5, 9), seed=3, a=.75)
    s.fx("godrays", cx=sun[0], cy=sun[1], strength=.3, thresh=.75, decay=.97, radius=220)
    s.fx("mottle", amp=.04, cell=60)
    s.look = {"vibrance": .1}
    return s


@scene
def elephant(s):
    sun = (330, 470)
    s.sky([(0, "#2a3052"), (.3, "#6a6488"), (.55, "#c89ca4"), (.72, "#f2c4a8"), (.85, "#fadcc0")], 0, 800)
    s.sun(*sun, 34, halo_r=640, halo_a=.7)
    rng = random.Random(3)
    # a dawn glade: hazy hills, a gopuram far off, a soft tree line, two great trees framing it
    hl = ridgeline(700, 120, 91, cell=320, octaves=5, ridged=.3, envelope=[(0, .6), (800, 1), (1600, .7)])
    hills(s, hl, "#a890a8", "#d8b0b0", haze="#f8d8c0", haze_a=.6, haze_h=120)
    s.add(f'<path d="M1180 700V560L1194 560L1204 506H1286L1296 560L1310 560V700Z" fill="#b898a8" opacity=".7"/>'
          f'<path d="M1204 506L1212 478H1278L1286 506ZM1216 478L1224 452H1266L1274 478ZM1228 452L1236 432H1254L1262 452Z" fill="#b898a8" opacity=".7"/>')
    s.mist(690, 120, "#ffe8d8", .55, 26)
    s.add(f'<path d="{foliage([(x, 760 - rng.uniform(0, 40), rng.uniform(40, 70)) for x in range(-40, 1680, 70)], seed=12, fine=10)}" fill="#8a7488" opacity=".9"/>')
    s.mist(770, 110, "#f8dcc8", .5, 24)
    for tx, lean, sgn in ((70, 4, 1), (1520, -5, -1)):
        segs, tips = [], []
        branches(tx, 1010, lean, 330, 90, 4, random.Random(tx), segs, tips, spread=36, shrink=.72, bend=10)
        leaves = foliage([(x, y, rng.uniform(56, 86)) for x, y, _ in tips] + [(tx + sgn * k * 120, rng.uniform(-30, 60), 100) for k in range(5)], seed=tx, fine=16)
        s.add(lit(s, f'<path d="{"".join(segs)}" fill="#1e1a22"/><path d="{leaves}" fill="#232a26"/>', toward(tx, 400, *sun), w=3, color="#ffd0a0", a=.75, w2=16, a2=.15))
    beams(s, sun[0], sun[1], [(62, 5, 1500, .2), (70, 4, 1500, .16), (78, 6, 1500, .12), (86, 3, 1500, .1)], color="#fff0d0", blur=16)
    # ground and a forest track
    g = smooth_line([(-60, 820), (400, 840), (800, 860), (1200, 846), (1660, 830)], 8)
    s.add(f'<path d="{pts_d(g + [(1660, 1010), (-60, 1010)])}" fill="{s.lin([(0, "#6a5a50", 1), (.3, "#4a3c38", 1), (1, "#1a1418", 1)], 0, 820, 0, 1000, user=True)}"/>')
    s.add(f'<ellipse cx="760" cy="900" rx="700" ry="50" fill="#ffd8a8" opacity=".25" filter="{s.blur(30)}" style="mix-blend-mode:screen"/>')
    grass(s, -40, 1640, lambda x: y_at(g, x) + 4, 260, h=(8, 30), color="#3a3030", seed=6)
    # the elephant, facing the morning light
    base = 892
    s.add(f'<ellipse cx="820" cy="{base + 4}" rx="300" ry="20" fill="#120c10" opacity=".55" filter="{s.blur(10)}"/>')
    el = place(820, base, 3.35, temple_elephant(s, body="#6a5e6c", shade="#241c28"), flip=True)
    s.add(lit(s, el, 180 + 20, w=5, color="#ffdcb0", a=1, blur=1.2, w2=70, a2=.42, color2="#ffb880"))
    s.motes(50, 200, 1500, 200, 860, color="#fff0c0", seed=9, size=(.8, 2.0))
    # foreground leaves
    fl = []
    for cx, cy, n, sgn in ((-20, 1010, 8, 1), (1620, 1010, 8, -1)):
        for k in range(n):
            a = math.radians(sgn * (10 + 60 * k / n) + rng.uniform(-6, 6))
            L = rng.uniform(160, 280)
            fl.append(ribbon(smooth_line([(cx, cy), (cx + math.sin(a) * L * .5, cy - L * .6), (cx + math.sin(a) * L, cy - L * .85)], 6), 22, 1))
    s.add(f'<path d="{"".join(fl)}" fill="#141016"/>')
    s.fx("godrays", cx=sun[0], cy=sun[1], strength=.4, thresh=.72, decay=.975, radius=240)
    s.fx("mottle", amp=.04, cell=60)
    s.look = {"vibrance": .1}
    return s


def chariot_svg(s, color="#1a1220", gold="#c8902e", banner="#e8781e"):
    """Arjuna's war chariot in profile facing right (wheel radius 48, ground at 0): a spoked wheel,
    a railed car under a domed canopy, the great bow standing in it, and a tall staff whose
    pennant bears a small leaping monkey for Hanuman. Returns (svg, yoke_point)."""
    out = []
    out.append(f'<path d="M66 -62C110 -64 150 -72 190 -92" stroke="{color}" stroke-width="7" fill="none" stroke-linecap="round"/>')
    car = ("M-70 -58H80L86 -66H-74Z"
           "M-70 -66V-108H-62V-66ZM48 -66V-110H56V-66Z"
           "M-74 -108H58L64 -114H-78Z"
           "M56 -66C76 -70 90 -92 92 -122C93 -136 88 -148 80 -154C84 -134 80 -110 64 -102Z"
           # canopy posts, dome and finial
           "M-68 -114V-206H-63V-114ZM50 -114V-206H55V-114Z"
           "M-80 -204H66L58 -212H-72Z"
           "M-70 -212C-66 -246 -36 -262 -6 -264C24 -262 52 -246 56 -212Z"
           "M-12 -264C-12 -272 0 -276 0 -276C0 -276 12 -272 12 -264ZM-2 -276L0 -286L2 -276Z")
    out.append(f'<path d="{car}" fill="{color}"/>')
    out.append(f'<path d="M-70 -88H50M-70 -98H50" stroke="{gold}" stroke-width="2" stroke-dasharray="3 4" opacity=".8"/>'
               f'<path d="M64 -102C80 -110 84 -132 80 -154M-80 -204H66M-66 -222C-50 -246 30 -252 50 -222" stroke="{gold}" stroke-width="2.2" fill="none" opacity=".85"/>'
               + "".join(f'<path d="M{x} -204v8" stroke="{gold}" stroke-width="1.6"/><circle cx="{x}" cy="-194" r="2" fill="{gold}"/>' for x in range(-74, 66, 10)))
    spokes = "".join(f"M0 -50L{f(math.cos(2 * math.pi * k / 12) * 46)} {f(-50 + math.sin(2 * math.pi * k / 12) * 46)}" for k in range(12))
    out.append(f'<circle cx="-6" cy="-50" r="48" fill="none" stroke="{color}" stroke-width="7"/>'
               f'<circle cx="-6" cy="-50" r="43" fill="none" stroke="{gold}" stroke-width="1.6" opacity=".7"/>'
               f'<path d="{spokes}" transform="translate(-6 0)" stroke="{color}" stroke-width="3.2"/><circle cx="-6" cy="-50" r="9" fill="{color}"/><circle cx="-6" cy="-50" r="4" fill="{gold}"/>')
    # the bow, standing in the car under the canopy
    out.append(f'<path d="M24 -64C40 -100 40 -160 24 -196" stroke="{color}" stroke-width="4.5" fill="none" stroke-linecap="round"/>'
               f'<path d="M24 -64L24 -196" stroke="{gold}" stroke-width=".9" opacity=".8"/>')
    # banner staff from the canopy, pennant with the monkey emblem
    out.append(f'<path d="M-6 -284V-420" stroke="{color}" stroke-width="4.5"/><circle cx="-6" cy="-424" r="5" fill="{gold}"/>')
    flag = "M-4 -416C-36 -420 -70 -406 -112 -412C-96 -394 -88 -382 -84 -368C-60 -378 -30 -370 -4 -374Z"
    out.append(f'<path d="{flag}" fill="{s.lin([(0, mix(banner, "#ffd890", .3), 1), (1, mix(banner, "#601008", .4), 1)], 0, 0, 1, 0)}"/>'
               f'<g transform="translate(-44 -394) scale(.62)"><path d="M6 6C2 -2 6 -10 12 -8C16 -16 22 -16 24 -10C28 -8 28 -2 24 0L30 8L26 10L20 4'
               f'C18 8 14 12 10 12L2 18L0 14L6 8C2 8 -4 10 -8 6C-12 2 -10 -4 -6 -4C-4 2 0 4 6 6Z" fill="{gold}"/>'
               f'<path d="M-8 6C-18 2 -22 -8 -18 -16" stroke="{gold}" stroke-width="2" fill="none"/></g>')
    return "".join(out), (190, -92)


@scene
def chariot(s):
    sun = (930, 640)
    hz = 650
    s.sky([(0, "#141a44"), (.25, "#2e2c66"), (.45, "#6a4a80"), (.6, "#c46a7a"), (.7, "#f49a74"), (.78, "#ffc888"), (.84, "#ffe6b8")], 0, hz)
    s.stars(40, 0, 220, seed=12, bright=.5)
    s.sun(*sun, 40, halo_r=760, halo_a=.85)
    s.fx("clouds", y0=40, y1=330, seed=61, cell=150, aniso=3.6, cover=.4, soft=.18, lit="#ffb898", body=.72, direct=.75,
         light=(0, 1), sun=(sun[0], sun[1], 460), opacity=.9)
    s.fx("clouds", y0=360, y1=560, seed=62, cell=90, aniso=6, cover=.28, soft=.22, lit="#ffd8b0", body=.85, direct=.9,
         light=(0, 1), sun=(sun[0], sun[1], 380), opacity=.75)
    # two armies along the horizon: spears, banners, parasols and elephants in the haze
    rng = random.Random(5)
    for x0, x1, col, fl_dir in ((-20, 600, "#5a3e66", 1), (1000, 1620, "#5a3e66", -1)):
        d, flags = [], []
        # a dense mass of soldiers with a ragged top of heads and shields
        mass = [(x0, hz + 2)]
        x = x0
        while x < x1:
            mass.append((x, hz - rng.uniform(9, 15)))
            x += rng.uniform(2.5, 5)
        mass.append((x1, hz + 2))
        d.append(pts_d(mass))
        x = x0
        while x < x1:
            if rng.random() < .55:
                L = rng.uniform(16, 34)
                a = math.radians(rng.uniform(-8, 8))
                d.append(f"M{f(x)} {hz - 10}l{f(math.sin(a) * L)} {f(-L)}l1.2 0l{f(-math.sin(a) * L)} {f(L)}Z")
            if rng.random() < .05:
                fh = rng.uniform(46, 84)
                d.append(f"M{f(x)} {hz}V{f(hz - fh)}h1.8V{hz}Z")
                flags.append(f"M{f(x + 1.8)} {f(hz - fh)}c{f(fl_dir * 8)} -3 {f(fl_dir * 14)} 4 {f(fl_dir * 22)} 2l{f(-fl_dir * 4)} 6c{f(-fl_dir * 8)} 2 {f(-fl_dir * 12)} -3 {f(-fl_dir * 18)} 2Z")
            if rng.random() < .025:
                ex = x
                d.append(f"M{f(ex - 18)} {hz - 6}C{f(ex - 18)} {hz - 30} {f(ex - 6)} {hz - 36} {f(ex + 8)} {hz - 34}C{f(ex + 18)} {hz - 32} {f(ex + 22)} {hz - 22} {f(ex + 20)} {hz - 8}Z"
                         f"M{f(ex - 8)} {hz - 34}h16v-10h-16Z M{f(ex - 10)} {hz - 46}C{f(ex - 10)} {hz - 54} {f(ex + 10)} {hz - 54} {f(ex + 10)} {hz - 46}Z")
            x += rng.uniform(5, 10)
        s.add(f'<path d="{"".join(d)}" fill="{col}" opacity=".9"/><path d="{"".join(flags)}" fill="#a8504a" opacity=".85"/>')
    s.mist(hz - 6, 50, "#ffc0a0", .6, 12)
    # the plain
    s.add(f'<rect y="{hz}" width="{W}" height="{H - hz}" fill="{s.lin([(0, "#c88a7a", 1), (.15, "#7a5068", 1), (.5, "#3a2840", 1), (1, "#140e1c", 1)], 0, hz, 0, 1000, user=True)}"/>')
    s.add(f'<ellipse cx="{sun[0]}" cy="{hz + 30}" rx="620" ry="70" fill="#ffc890" opacity=".35" filter="{s.blur(30)}" style="mix-blend-mode:screen"/>')
    s.wisps(14, 0, W, hz + 10, hz + 120, "#ffc8a8", a=(.06, .18), length=(200, 600), thick=(6, 18), blur=10, seed=4)
    grass(s, -40, 1640, lambda x: 940 + math.sin(x / 90) * 8, 160, h=(8, 26), color="#120c18", seed=8)
    # the chariot and its four white horses, between the armies
    gx, gy, sc = 400, 900, 1.82
    rim = dict(w=3.5, color="#fff0d0", a=1, blur=1.0, halo=6, halo_a=.3)
    s.add(f'<ellipse cx="{gx + 360}" cy="{gy + 4}" rx="480" ry="16" fill="#0a0610" opacity=".6" filter="{s.blur(8)}"/>')
    car, yoke = chariot_svg(s)
    horses = []
    for k, (dx, dy, hsc, tone) in enumerate(((150, -40, 1.08, .55), (104, -27, 1.14, .38), (52, -13, 1.2, .2), (0, 0, 1.25, 0))):
        # backlit by the low sun: the white horses read as warm silhouettes with bright rims
        body = mix("#4a3a52", "#8a6a80", tone)
        shade = mix("#1c1422", "#4a3448", tone)
        hs = horse(body=body, shade=shade, s=s, plume="#d8342a" if k % 2 else "#f2b632")
        x = gx + (190 + 64) * sc + dx
        horses.append(place(x, gy + dy, sc * hsc, hs))
    s.add(lit(s, "".join(horses), toward(gx + 500, gy - 150, *sun), **rim))
    s.add(f'<path d="M{f(gx + 90 * sc)} {f(gy - 132 * sc)}C{f(gx + 200 * sc)} {f(gy - 170 * sc)} {f(gx + 300 * sc)} {f(gy - 175 * sc)} {f(gx + 352 * sc)} {f(gy - 140 * sc)}" stroke="#2a1a24" stroke-width="2" fill="none"/>')
    s.add(lit(s, place(gx, gy, sc, car), toward(gx, gy - 200, *sun), **rim))
    s.birds(5, 1080, 1300, 420, 480, color="#3a2040", s=(5, 9), seed=2, a=.7)
    s.motes(40, 300, 1400, 500, 900, color="#ffd8a0", seed=6, size=(.8, 2))
    s.fx("godrays", cx=sun[0], cy=sun[1], strength=.45, thresh=.7, decay=.972, radius=260)
    s.fx("mottle", amp=.045, cell=60)
    return s
