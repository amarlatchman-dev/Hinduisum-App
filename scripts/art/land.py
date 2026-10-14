"""Landscape pieces: ridgelines, lit mountains with snow, hills and trees."""
import math
import random

from paint import H, W, f, pts_d


# ---------- ridgelines ----------
def _vnoise(seed, n):
    rng = random.Random(seed)
    return [rng.random() for _ in range(n)]


def _interp(vals, x):
    i = int(math.floor(x))
    t = x - i
    t = t * t * (3 - 2 * t)
    return vals[i % len(vals)] * (1 - t) + vals[(i + 1) % len(vals)] * t


def ridgeline(base, amp, seed, cell=380, octaves=6, ridged=0.7, gain=0.5, x0=-40, x1=W + 40, step=4, envelope=None):
    """A natural skyline. ridged pushes crests into sharp peaks; envelope is a list of
    (x, weight) points that scales the height along the line."""
    tables = [_vnoise(seed * 31 + o, 512) for o in range(octaves)]
    out = []
    env = sorted(envelope) if envelope else None
    for x in range(int(x0), int(x1) + step, step):
        v, amp_o, tot, c = 0.0, 1.0, 0.0, cell
        for o in range(octaves):
            n = _interp(tables[o], x / c + 17.3 * o)
            r = 1 - abs(2 * n - 1)
            v += amp_o * ((1 - ridged) * n + ridged * r * r)
            tot += amp_o
            amp_o *= gain
            c /= 2.1
        v /= tot
        e = 1.0
        if env:
            if x <= env[0][0]:
                e = env[0][1]
            elif x >= env[-1][0]:
                e = env[-1][1]
            else:
                for (xa, ea), (xb, eb) in zip(env, env[1:]):
                    if xa <= x <= xb:
                        t = (x - xa) / (xb - xa)
                        t = t * t * (3 - 2 * t)
                        e = ea + (eb - ea) * t
                        break
        out.append((x, base - amp * v * e))
    return out


def peak_line(base, peaks, seed, detail=0.14, x0=-40, x1=W + 40, step=4, shape=1.35, floor=0.0, shoulders=2):
    """A mountain skyline built from individual peaks, each (x, height, half_width[, skew]).
    Peaks overlap like a real range, with lesser summits on their shoulders; ridged
    noise adds crags in proportion to height."""
    tables = [_vnoise(seed * 17 + o, 512) for o in range(5)]
    rng = random.Random(seed)
    peaks = list(peaks)
    for pk in list(peaks):
        px, ph, pw = pk[:3]
        for _ in range(shoulders):
            side = rng.choice((-1, 1))
            peaks.append((px + side * pw * rng.uniform(.25, .55), ph * rng.uniform(.55, .8), pw * rng.uniform(.4, .65), rng.uniform(-.2, .2)))
    out = []
    for x in range(int(x0), int(x1) + step, step):
        h = 0.0
        for pk in peaks:
            px, ph, pw = pk[:3]
            skew = pk[3] if len(pk) > 3 else 0.0
            w = pw * (1 + skew if x > px else 1 - skew)
            t = abs(x - px) / max(1, w)
            if t < 1:
                h = max(h, ph * (1 - t) ** shape)
            else:
                h = max(h, 0)
        v, amp, c, tot = 0.0, 1.0, 210.0, 0.0
        for o in range(5):
            n = _interp(tables[o], x / c + 9.1 * o)
            v += amp * (1 - abs(2 * n - 1)) ** 2
            tot += amp
            amp *= .5
            c /= 2.2
        out.append((x, base - h * (1 - detail + detail * 2 * v / tot) - floor * (1 - detail * .3 + detail * .6 * v / tot)))
    return out


def fill_under(pts, bottom=H + 10):
    return pts_d(list(pts) + [(pts[-1][0], bottom), (pts[0][0], bottom)])


def peaks_of(pts, min_sep=120, count=8, prominence=30):
    """The highest local summits of a ridgeline, at least min_sep apart."""
    idx = sorted(range(len(pts)), key=lambda i: pts[i][1])
    chosen = []
    for i in idx:
        x, y = pts[i]
        if all(abs(x - pts[j][0]) > min_sep for j in chosen):
            lo = min(p[1] for p in pts[max(0, i - 30):i + 30])
            if y <= lo + 0.5:
                drop = max(p[1] for p in pts[max(0, i - 40):i + 40]) - y
                if drop > prominence:
                    chosen.append(i)
        if len(chosen) >= count:
            break
    return sorted(chosen)


def _taper(line, w):
    """A stroke that narrows from width w to a point, as a filled path."""
    n = len(line)
    left, right = [], []
    for i, (x, y) in enumerate(line):
        xa, ya = line[max(0, i - 1)]
        xb, yb = line[min(n - 1, i + 1)]
        dx, dy = xb - xa, yb - ya
        L = math.hypot(dx, dy) or 1
        k = w / 2 * (1 - i / (n - 1))
        left.append((x - dy / L * k, y + dx / L * k))
        right.append((x + dy / L * k, y - dx / L * k))
    return pts_d(left + right[::-1])


# ---------- mountains ----------
def mountains(s, pts, top, bottom, lit=None, lit_a=0.55, light=1, seed=1, snow=None, snow_shade=None, snowline=None,
              snow_fingers=60, rim=None, rim_a=0.8, rim_w=1.6, rim_center=None, rim_r=700, faces=True, gullies=True, lit_snow=None, face_fade=0.8,
              haze=None, haze_a=0.5, haze_h=260, base_y=None):
    """A mountain layer: graded body, lit faces (light=1 from the right, -1 from the left),
    optional snow caps with ragged fingers, a rim of light along the crest and pooled haze."""
    rng = random.Random(seed)
    d = fill_under(pts)
    ymin = min(y for _, y in pts)
    ymax = base_y or max(y for _, y in pts) + 120
    body = s.lin([(0, top, 1), (1, bottom, 1)], 0, ymin, 0, ymax, user=True)
    clip = s.clip(d)
    out = [f'<path d="{d}" fill="{body}"/>']

    snow_d = None
    if snow and snowline is not None:
        tab = _vnoise(seed + 6, 512)
        fingers = []
        x = pts[0][0]
        while x < pts[-1][0]:
            x += rng.uniform(10, 34)
            fingers.append((x, rng.uniform(6, 16), snow_fingers * rng.uniform(.25, 1) ** 1.5))
        bottom_pts = []
        for x, y in pts:
            sb = snowline + (_interp(tab, x / 70) - .5) * snow_fingers * .8
            sb += max([L * max(0.0, 1 - abs(x - fx) / fw) for fx, fw, L in fingers if abs(x - fx) < fw] or [0])
            sb = min(sb, y + max(0, snowline - y) * 1.6)
            bottom_pts.append((x, max(y, sb)))
        snow_d = pts_d(list(pts) + bottom_pts[::-1])
        sg = s.lin([(0, snow, 1), (1, snow_shade or snow, 1)], 0, ymin, 0, snowline + snow_fingers, user=True)
        out.append(f'<path d="{snow_d}" fill="{sg}" filter="{s.blur(0.6)}"/>')

    if faces and lit:
        faces_out, gul = [], []
        pk = peaks_of(pts, min_sep=60, count=16, prominence=14)
        for i in pk:
            px, py = pts[i]
            # walk downhill on the lit side to the next valley
            j = i
            step = 1 if light > 0 else -1
            while 0 < j + step < len(pts) - 1 and pts[j + step][1] >= pts[j][1] - 1:
                j += step
            vx, vy = pts[j]
            depth = vy - py
            if depth < 10:
                continue
            spine = [(px, py)]
            x = px
            n = 8
            total = depth * rng.uniform(1.4, 2.0)
            for k in range(1, n + 1):
                y = py + total * k / n
                x += -light * rng.uniform(-3, 5) * (total / 200) + rng.uniform(-3, 3)
                spine.append((x, y))
            ridge_back = [pts[m] for m in (range(j, i, -1) if light > 0 else range(j, i))]
            poly = spine + [(vx + light * depth * .1, vy + depth * .9)] + ridge_back
            faces_out.append(pts_d(poly))
            if gullies:
                span = j - i if light > 0 else i - j
                for _ in range(rng.randint(2, 4)):
                    m = i + step * int(span * rng.uniform(.15, .85))
                    gx, gy = pts[m]
                    L = (vy - py) * rng.uniform(.5, 1.1) + 12
                    g = [(gx, gy + 1)]
                    for k in range(1, 7):
                        g.append((gx - light * L * .22 * k / 6 + rng.uniform(-2, 2), gy + L * k / 6))
                    gul.append(_taper(g, rng.uniform(4, 8)))
        ft = ymin + (ymax - ymin) * .85
        lg = s.lin([(0, lit, lit_a), (0.55, lit, lit_a * .6), (1, lit, lit_a * .15)], 0, ymin, 0, ft, user=True)
        fm = s.mask_fade(-100, ymin, W + 200, (ymax - ymin) * face_fade, 1, 0)
        out.append(f'<g clip-path="{clip}"><g mask="{fm}"><path d="{"".join(faces_out)}" fill="{lg}" filter="{s.blur(1)}"/></g>')
        if snow_d and lit_snow:
            sl = s.lin([(0, lit_snow, 1), (1, lit_snow, .75)], 0, ymin, 0, snowline + snow_fingers, user=True)
            out.append(f'<g clip-path="{s.clip(snow_d)}"><path d="{"".join(faces_out)}" fill="{sl}" filter="{s.blur(1)}"/></g>')
        out.append(f'<path d="{"".join(gul)}" fill="{bottom}" fill-opacity=".38" filter="{s.blur(0.8)}"/></g>')

    if rim:
        line = "M" + "L".join(f"{f(x)} {f(y)}" for x, y in pts)
        if rim_center:
            rg = s.rad([(0, rim, rim_a), (0.5, rim, rim_a * .45), (1, rim, 0)], rim_center[0], rim_center[1], rim_r, user=True)
        else:
            rg = rim
        out.append(f'<g clip-path="{clip}"><path d="{line}" stroke="{rg}" stroke-width="{rim_w * 2}" fill="none" stroke-linejoin="round" filter="{s.blur(rim_w * .6)}"/></g>')

    if haze:
        hz = s.lin([(0, haze, 0), (1, haze, haze_a)], 0, ymax - haze_h, 0, ymax, user=True)
        out.append(f'<path d="{d}" fill="{hz}"/>')
    s.add("".join(out))
    return d


def hills(s, pts, top, bottom, rim=None, rim_a=0.6, rim_center=None, rim_r=600, haze=None, haze_a=0.4, haze_h=200):
    """A soft rolling layer, like mountains() without faces."""
    return mountains(s, pts, top, bottom, rim=rim, rim_a=rim_a, rim_center=rim_center, rim_r=rim_r, faces=False,
                     haze=haze, haze_a=haze_a, haze_h=haze_h)


# ---------- trees ----------
def pine(x, base, h, seed=1, tiers=None, droop=0.18, width=0.42):
    """Path for a Himalayan deodar or fir silhouette."""
    rng = random.Random(seed)
    tiers = tiers or max(5, int(h / 9))
    left, right = [], []
    for k in range(tiers + 1):
        t = k / tiers
        y = base - h + h * 0.92 * t
        w = h * width * (0.08 + 0.92 * t ** 0.9) * rng.uniform(.82, 1.12)
        dy = h * droop / tiers * 2.2
        right += [(x + w * .35, y + dy * .2), (x + w, y + dy)]
        left += [(x - w * .35, y + dy * .2 + rng.uniform(-1, 1)), (x - w * rng.uniform(.85, 1.05), y + dy)]
    trunk_w = max(1.2, h * .03)
    pts = [(x, base - h - h * .04)] + right + [(x + trunk_w, base - h * .05), (x + trunk_w, base), (x - trunk_w, base), (x - trunk_w, base - h * .05)] + left[::-1]
    return pts_d(pts)


def pines(s, x0, x1, ground, n, h=(40, 90), color="#0b0d14", seed=1, a=1.0, ground_fn=None):
    rng = random.Random(seed)
    paths = []
    for k in range(n):
        x = rng.uniform(x0, x1)
        base = ground_fn(x) if ground_fn else ground
        paths.append(pine(x, base + 4, rng.uniform(*h), seed=seed * 100 + k))
    s.add(f'<path d="{"".join(paths)}" fill="{color}" opacity="{a}"/>')


def crown(cx, cy, r, seed=1, lobes=9, bump=0.18):
    """A billowy round tree crown outline as a path."""
    rng = random.Random(seed)
    pts = []
    n = lobes * 8
    phase = [rng.uniform(0, 6.28) for _ in range(3)]
    for k in range(n):
        a = 2 * math.pi * k / n
        lobe = abs(math.sin(a * lobes / 2 + phase[0]))
        rr = r * (1 - bump + bump * lobe ** .6) * (1 + 0.08 * math.sin(a * 3 + phase[1]))
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr * 0.82))
    return pts_d(pts)


def round_tree(s, x, base, h, color="#0b0d10", seed=1, trunk=True, lean=0.0, crowns=4):
    rng = random.Random(seed)
    out = []
    if trunk:
        tw = h * .05
        out.append(f'M{f(x - tw)} {f(base)}C{f(x - tw)} {f(base - h * .3)} {f(x - tw * .5 + lean * h * .3)} {f(base - h * .5)} {f(x + lean * h * .4)} {f(base - h * .62)}'
                   f'L{f(x + lean * h * .4 + tw)} {f(base - h * .62)}C{f(x + tw * .6 + lean * h * .3)} {f(base - h * .5)} {f(x + tw)} {f(base - h * .3)} {f(x + tw * 1.4)} {f(base)}Z')
    for k in range(crowns):
        cx = x + lean * h * .4 + rng.uniform(-h * .28, h * .28)
        cy = base - h * rng.uniform(.62, .86)
        out.append(crown(cx, cy, h * rng.uniform(.2, .32), seed * 7 + k))
    s.add(f'<path d="{"".join(out)}" fill="{color}"/>')


def grass(s, x0, x1, base, n, h=(8, 26), color="#0a0b0f", seed=1, lean=0.25):
    """Tufts of grass along a ground line; base is a y value or a function of x."""
    rng = random.Random(seed)
    d = []
    for _ in range(n):
        x = rng.uniform(x0, x1)
        hh = rng.uniform(*h)
        b = base(x) if callable(base) else base
        l = rng.uniform(-lean, lean) * hh
        w = hh * .06
        d.append(f"M{f(x - w)} {f(b)}Q{f(x + l * .3)} {f(b - hh * .6)} {f(x + l)} {f(b - hh)}Q{f(x + l * .3 + w)} {f(b - hh * .55)} {f(x + w)} {f(b)}Z")
    s.add(f'<path d="{"".join(d)}" fill="{color}"/>')


def y_at(pts, x):
    """Height of a ridgeline at x (linear interpolation)."""
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        if xa <= x <= xb:
            return ya + (yb - ya) * (x - xa) / max(1e-6, xb - xa)
    return pts[0][1] if x < pts[0][0] else pts[-1][1]


def smooth_line(ctrl, step=6):
    """Catmull-Rom curve through control points, as a list of points."""
    out = []
    p = [ctrl[0]] + list(ctrl) + [ctrl[-1]]
    for i in range(1, len(p) - 2):
        (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p[i - 1], p[i], p[i + 1], p[i + 2]
        n = max(2, int(math.hypot(x2 - x1, y2 - y1) / step))
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            out.append((0.5 * (2 * x1 + (-x0 + x2) * t + (2 * x0 - 5 * x1 + 4 * x2 - x3) * t2 + (-x0 + 3 * x1 - 3 * x2 + x3) * t3),
                        0.5 * (2 * y1 + (-y0 + y2) * t + (2 * y0 - 5 * y1 + 4 * y2 - y3) * t2 + (-y0 + 3 * y1 - 3 * y2 + y3) * t3)))
    out.append(ctrl[-1])
    return out


def ribbon(center, w0, w1):
    """A band around a centre line whose width tapers from w0 to w1 (a path or river)."""
    n = len(center)
    left, right = [], []
    for i, (x, y) in enumerate(center):
        xa, ya = center[max(0, i - 1)]
        xb, yb = center[min(n - 1, i + 1)]
        dx, dy = xb - xa, yb - ya
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        w = (w0 + (w1 - w0) * i / max(1, n - 1)) / 2
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    return pts_d(left + right[::-1])
