from scenes import scene

# Still-life paintings of sacred objects: lamps, conches, vessels, beads, sweets and relics.
#
# The hero objects are modelled in 3D and painted by a small numpy rasteriser: each object is a
# parametric surface (a lathe profile, a tube along a path, a rounded box or a free sheet) that is
# sampled densely, shaded with a lamp, a soft ambient and a reflected environment, and splatted
# into a z-buffer. That gives true form: a highlight facing the lamp, a shadow side, cast and
# contact shadows, and reflections on polished floors. Rooms, skies, flowers and flames are
# painted with the shared SVG toolkit around them.
import math
import random

import numpy as np
from scipy import ndimage

import arch
import fx
import objects as ob
from glyphs import OM
from land import hills, mountains, peak_line, pines, ridgeline, smooth_line, y_at
from paint import H, W, f, mix


# ============================================================ numpy 3D renderer
def C(c):
    c = c.lstrip("#")
    return np.array([int(c[i:i + 2], 16) / 255 for i in (0, 2, 4)], np.float32)


def _unit(v):
    n = np.sqrt((v * v).sum(-1, keepdims=True))
    return v / np.maximum(n, 1e-12), n[..., 0]


def _sm(a, b, x):
    d = b - a
    d = np.where(np.abs(d) < 1e-9, 1e-9, d)
    t = np.clip((x - a) / d, 0, 1)
    return t * t * (3 - 2 * t)


def _hash(i, j, seed):
    x = np.sin(i * 127.1 + j * 311.7 + seed * 74.7) * 43758.5453
    return x - np.floor(x)


def vnoise(x, y, seed=0):
    xi, yi = np.floor(x), np.floor(y)
    xf, yf = x - xi, y - yi
    u, v = xf * xf * (3 - 2 * xf), yf * yf * (3 - 2 * yf)
    a, b = _hash(xi, yi, seed), _hash(xi + 1, yi, seed)
    c, d = _hash(xi, yi + 1, seed), _hash(xi + 1, yi + 1, seed)
    return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v


def fbm(x, y, octaves=4, seed=0):
    t, amp, tot = 0.0, 1.0, 0.0
    for k in range(octaves):
        t = t + amp * vnoise(x * 2 ** k, y * 2 ** k, seed + k * 13)
        tot += amp
        amp *= .5
    return t / tot


def rot(ax, deg):
    a = math.radians(deg)
    c, s_ = math.cos(a), math.sin(a)
    return {"x": np.array([[1, 0, 0], [0, c, -s_], [0, s_, c]]),
            "y": np.array([[c, 0, s_], [0, 1, 0], [-s_, 0, c]]),
            "z": np.array([[c, -s_, 0], [s_, c, 0], [0, 0, 1]])}[ax]


def rots(*pairs):
    M = np.eye(3)
    for ax, deg in pairs:
        M = rot(ax, deg) @ M
    return M


class Cam:
    """Orthographic-ish camera with a little perspective. World: X = screen x, Y = up, Z = towards
    the viewer. The world point (x0, 0, 0) appears at screen (x0, y0); elev is the downward tilt."""

    def __init__(self, elev=30, x0=800, y0=700, dist=3600):
        e = math.radians(elev)
        self.ce, self.se = math.cos(e), math.sin(e)
        self.x0, self.y0, self.D = x0, y0, dist
        self.pos = np.array([x0, dist * self.se, dist * self.ce])

    def proj(self, P):
        X, Y, Z = P[..., 0], P[..., 1], P[..., 2]
        d = Z * self.ce + Y * self.se
        k = self.D / (self.D - d)
        return self.x0 + (X - self.x0) * k, self.y0 + (Z * self.se - Y * self.ce) * k, d

    def at(self, sx, sy, Y=0.0):
        """The world point at height Y that appears at screen (sx, sy)."""
        a, D = sy - self.y0, self.D
        Z = (a * D - a * Y * self.se + Y * D * self.ce) / (D * self.se + a * self.ce)
        d = Z * self.ce + Y * self.se
        k = D / (D - d)
        return np.array([self.x0 + (sx - self.x0) / k, Y, Z])

    def scr(self, P):
        x, y, _ = self.proj(np.asarray(P, float))
        return float(x), float(y)


class Light:
    def __init__(self, pos=None, color="#ffd49a", power=1.0, falloff=900, direction=None, shadow=0.0, size=30):
        self.pos = None if pos is None else np.asarray(pos, float)
        self.dir = None if direction is None else _unit(np.asarray(direction, float))[0]
        self.col = C(color) * power
        self.falloff, self.shadow, self.size = falloff, shadow, size


class Rig:
    """Lights plus the soft surroundings: a hemisphere of ambient light and an environment that
    metals and glazes reflect, given as colour stops over the up-component of the reflection."""

    def __init__(self, lights, sky="#3a2416", ground="#1a0d07", amb=1.0, env=None):
        self.lights = lights
        self.sky, self.ground = C(sky) * amb, C(ground) * amb
        env = env or [(-1, "#2a1408"), (-.15, "#6a3818"), (0.05, "#8a5228"), (.3, "#2a160c"), (1, "#0e0806")]
        self.ey = np.array([e[0] for e in env], np.float32)
        self.ec = np.array([C(e[1]) for e in env], np.float32)

    def env(self, R):
        y = R[:, 1]
        return np.stack([np.interp(y, self.ey, self.ec[:, k]) for k in range(3)], -1)


class Mat:
    def __init__(self, color="#b08040", metal=0.0, rough=0.4, ks=0.4, wrap=0.15, kr=0.25, amb=1.0,
                 tex=None, bump=None, bump_k=1.0, emit=None, ao=None, env_k=1.0, lobe=0.5, kd_metal=0.25, spec_tint=0.5,
                 sheen=0.0, sheen_col=None, fres=1.0):
        self.color, self.metal, self.ks, self.wrap, self.kr, self.amb = color, metal, ks, wrap, kr, amb
        self.exp = max(2.0, (1 - rough) ** 3 * 420 + 3)
        self.tex, self.bump, self.bump_k, self.emit, self.ao = tex, bump, bump_k, emit, ao
        self.env_k, self.lobe, self.kd_metal, self.spec_tint = env_k, lobe, kd_metal, spec_tint
        self.sheen, self.sheen_col, self.fres = sheen, (C(sheen_col) if sheen_col else None), fres

    def albedo(self, g):
        if callable(self.color):
            a = self.color(g)
        else:
            a = np.broadcast_to(C(self.color), (len(g["u"]), 3)).copy()
        if self.tex is not None:
            t = self.tex(g)
            a = a * (t[:, None] if t.ndim == 1 else t)
        return a


def _with(m, **kw):
    import copy
    n = copy.copy(m)
    for k, v in kw.items():
        if k == "rough":
            n.exp = max(2.0, (1 - v) ** 3 * 420 + 3)
        else:
            setattr(n, k, v)
    return n


BRASS_M = dict(color="#e0a64a", metal=1, rough=.28, ks=1.1, env_k=1.25, lobe=.7, kd_metal=.32)
GOLD_M = dict(color="#f2c25a", metal=1, rough=.24, ks=1.2, env_k=1.3, lobe=.75, kd_metal=.35)
SILVER_M = dict(color="#e8e4dc", metal=1, rough=.22, ks=1.1, env_k=1.2, lobe=.7, kd_metal=.3, spec_tint=.2)
COPPER_M = dict(color="#d8784a", metal=1, rough=.3, ks=1.0, env_k=1.2, lobe=.7, kd_metal=.3)
CLAY_M = dict(color="#b4552a", rough=.8, ks=.12, wrap=.25, kr=.06)


class Surf:
    def __init__(self, pos, mat, normal=None, orient=1, extra=None, two_sided=False, cast=True, reflect=True, dens=1.0,
                 fd=False):
        self.pos, self.mat, self.normal, self.orient, self.extra = pos, mat, normal, orient, extra
        self.two_sided, self.cast, self.reflect, self.dens, self.fd = two_sided, cast, reflect, dens, fd


def _cr(pts, step=2.0):
    """Centripetal Catmull-Rom through 2D or 3D control points; a repeated point makes a corner."""
    pts = np.asarray(pts, float)
    if len(pts) < 3:
        n = max(2, int(np.linalg.norm(pts[-1] - pts[0]) / step))
        return np.linspace(pts[0], pts[-1], n)
    P = np.vstack([2 * pts[0] - pts[1], pts, 2 * pts[-1] - pts[-2]])
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        L = np.linalg.norm(p2 - p1)
        if L < 1e-9:
            continue
        t0 = 0.0
        t1 = t0 + max(np.linalg.norm(p1 - p0), 1e-4) ** .5
        t2 = t1 + max(L, 1e-4) ** .5
        t3 = t2 + max(np.linalg.norm(p3 - p2), 1e-4) ** .5
        n = max(3, int(L / step))
        t = np.linspace(t1, t2, n, endpoint=False)[:, None]
        A1 = (t1 - t) / (t1 - t0) * p0 + (t - t0) / (t1 - t0) * p1
        A2 = (t2 - t) / (t2 - t1) * p1 + (t - t1) / (t2 - t1) * p2
        A3 = (t3 - t) / (t3 - t2) * p2 + (t - t2) / (t3 - t2) * p3
        B1 = (t2 - t) / (t2 - t0) * A1 + (t - t0) / (t2 - t0) * A2
        B2 = (t3 - t) / (t3 - t1) * A2 + (t - t1) / (t3 - t1) * A3
        out.append((t2 - t) / (t2 - t1) * B1 + (t - t1) / (t2 - t1) * B2)
    out.append(pts[-1:])
    return np.vstack(out)


def _arclen(c):
    seg = np.sqrt((np.diff(c, axis=0) ** 2).sum(1))
    L = np.concatenate([[0], np.cumsum(seg)])
    return L / max(L[-1], 1e-9), L[-1]


def lathe(prof, mat, at=(0, 0, 0), M=None, mod=None, smooth=True, scale=1.0, sy=None, **kw):
    """A body of revolution. prof lists (radius, height) points traversed so the solid lies to
    the left: from the bottom centre out along the foot, up the outside, over the lip and down the
    inside. mod(u, phi, y) may return a radius multiplier (pleats, ribs, spiral whorls)."""
    pts = np.asarray(prof, float) * scale
    if sy is not None:
        pts[:, 1] *= sy
    cur = _cr(pts, 1.5) if smooth else pts
    uu, _ = _arclen(cur)
    tan = np.gradient(cur, axis=0)
    tan, _ = _unit(tan)
    n2 = np.stack([tan[:, 1], -tan[:, 0]], -1)
    M = np.eye(3) if M is None else np.asarray(M, float)
    at = np.asarray(at, float)
    ortho = np.allclose(M @ M.T, np.eye(3), atol=1e-6)

    def local(u, v):
        rho = np.interp(u, uu, cur[:, 0])
        y = np.interp(u, uu, cur[:, 1])
        phi = 2 * np.pi * v
        if mod is not None:
            rho = rho * mod(u, phi, y)
        return rho, y, phi

    def pos(u, v):
        rho, y, phi = local(u, v)
        L = np.stack([rho * np.sin(phi), y, rho * np.cos(phi)], -1)
        return L @ M.T + at

    def normal(u, v):
        nr, ny = np.interp(u, uu, n2[:, 0]), np.interp(u, uu, n2[:, 1])
        phi = 2 * np.pi * v
        N = np.stack([nr * np.sin(phi), ny, nr * np.cos(phi)], -1)
        if not ortho:
            N = N @ np.linalg.inv(M)
            return _unit(N)[0]
        return N @ M.T

    def extra(u, v):
        rho, y, phi = local(u, v)
        return {"y": y, "rho": rho, "phi": phi}

    return Surf(pos, mat, normal, orient=-1, extra=extra, fd=mod is not None, **kw)


def ellipsoid(c, r, mat, M=None, **kw):
    rx, ry, rz = (r, r, r) if np.isscalar(r) else r
    t = np.linspace(0, np.pi, 60)
    prof = np.stack([np.sin(t), -np.cos(t)], -1)
    S = np.diag([rx, ry, rz])
    MM = (np.eye(3) if M is None else np.asarray(M)) @ S
    return lathe(prof, mat, at=c, M=MM, smooth=False, **kw)


def tube(path, radius, mat, cap=True, smooth=True, twist=0.0, **kw):
    """A tube swept along a 3D path; radius is a number, a list per control point, or f(s01)."""
    path = np.asarray(path, float)
    cen = _cr(path, 1.5) if smooth else path
    uu, L = _arclen(cen)
    T = _unit(np.gradient(cen, axis=0))[0]
    a = np.array([0, 0, 1.0]) if abs(T[0, 2]) < .9 else np.array([1.0, 0, 0])
    N1 = np.zeros_like(T)
    n = _unit(np.cross(T[0], a))[0]
    for i in range(len(T)):
        n = n - (n @ T[i]) * T[i]
        n = n / max(np.linalg.norm(n), 1e-9)
        N1[i] = n
    N2 = np.cross(T, N1)
    if callable(radius):
        rf = radius
    elif np.isscalar(radius):
        rf = lambda s: np.full_like(s, float(radius))
    else:
        rk = np.asarray(radius, float)
        _, cu = None, np.linspace(0, 1, len(rk))
        ctrl_u, _ = _arclen(path)
        rf = lambda s: np.interp(s, ctrl_u, rk)

    def rad(s):
        r = rf(s)
        if cap:
            r0, r1 = float(rf(np.array([0.0]))[0]), float(rf(np.array([1.0]))[0])
            d0, d1 = s * L, (1 - s) * L
            k0 = np.sqrt(np.clip(1 - np.clip(1 - d0 / max(r0, 1e-3), 0, 1) ** 2, 0, 1))
            k1 = np.sqrt(np.clip(1 - np.clip(1 - d1 / max(r1, 1e-3), 0, 1) ** 2, 0, 1))
            r = r * np.minimum(k0, k1)
        return r

    def frame(u):
        c = np.stack([np.interp(u, uu, cen[:, k]) for k in range(3)], -1)
        n1 = _unit(np.stack([np.interp(u, uu, N1[:, k]) for k in range(3)], -1))[0]
        n2 = _unit(np.stack([np.interp(u, uu, N2[:, k]) for k in range(3)], -1))[0]
        return c, n1, n2

    def pos(u, v):
        c, n1, n2 = frame(u)
        ang = 2 * np.pi * v + twist * u
        r = rad(u)[:, None]
        return c + r * (np.cos(ang)[:, None] * n1 + np.sin(ang)[:, None] * n2)

    def normal(u, v):
        c, n1, n2 = frame(u)
        ang = 2 * np.pi * v + twist * u
        radial = np.cos(ang)[:, None] * n1 + np.sin(ang)[:, None] * n2
        du = 1e-3
        dr = (rad(np.clip(u + du, 0, 1)) - rad(np.clip(u - du, 0, 1))) / (2 * du * L)
        t = np.stack([np.interp(u, uu, T[:, k]) for k in range(3)], -1)
        return _unit(radial - dr[:, None] * t)[0]

    def extra(u, v):
        return {"s": u * L, "ang": 2 * np.pi * v}

    return Surf(pos, mat, normal, extra=extra, **kw)


def rbox(c, half, r, mat, M=None, **kw):
    """A box with rounded edges; returns six faces. extra gives the face id and local q."""
    c = np.asarray(c, float)
    h = np.asarray(half, float)
    M = np.eye(3) if M is None else np.asarray(M, float)
    inner = h - r
    faces = []
    for ax in range(3):
        for sg in (-1, 1):
            o = [k for k in range(3) if k != ax]

            def mk(ax=ax, sg=sg, o=o):
                def q_of(u, v):
                    q = np.zeros((len(u), 3))
                    q[:, ax] = sg * h[ax]
                    q[:, o[0]] = (u * 2 - 1) * h[o[0]]
                    q[:, o[1]] = (v * 2 - 1) * h[o[1]]
                    return q

                def nloc(u, v):
                    q = q_of(u, v)
                    p_in = np.clip(q, -inner, inner)
                    return p_in, _unit(q - p_in)[0]

                def pos(u, v):
                    p_in, n = nloc(u, v)
                    return (p_in + r * n) @ M.T + c

                def normal(u, v):
                    return nloc(u, v)[1] @ M.T

                def extra(u, v):
                    return {"face": (ax, sg), "q": q_of(u, v)}

                return Surf(pos, mat, normal, extra=extra, **kw)
            faces.append(mk())
    return faces


def sheet(fn, mat, two_sided=True, **kw):
    """A free surface: fn(u, v) -> (n, 3) world points."""
    return Surf(fn, mat, None, two_sided=two_sided, **kw)


# ---------- rendering ----------
def _dims(surf, cam, ss, dens):
    n = 28
    u = np.linspace(0, 1, n)
    U, V = np.meshgrid(u, u, indexing="ij")
    P = surf.pos(U.ravel(), V.ravel())
    sx, sy, _ = cam.proj(P)
    sx, sy = sx.reshape(n, n), sy.reshape(n, n)
    lu = np.hypot(np.diff(sx, axis=0), np.diff(sy, axis=0)).sum(0).max()
    lv = np.hypot(np.diff(sx, axis=1), np.diff(sy, axis=1)).sum(1).max()
    k = ss * dens * surf.dens
    return int(lu * k) + 6, int(lv * k) + 6, sx, sy


def _chunks(nu, nv, maxn=400000):
    rows = max(1, maxn // nv)
    v = (np.arange(nv) + .5) / nv
    for i0 in range(0, nu, rows):
        u = (np.arange(i0, min(nu, i0 + rows)) + .5) / nu
        U, V = np.meshgrid(u, v, indexing="ij")
        yield U.ravel(), V.ravel()


def _geom(surf, u, v, du, dv):
    P = surf.pos(u, v)
    need_fd = surf.normal is None or surf.fd or surf.mat.bump is not None
    Pu = Pv = None
    if need_fd:
        hu, hv = du * .5, dv * .5
        Pu = surf.pos(u + hu, v) - surf.pos(u - hu, v)
        Pv = surf.pos(u, v + hv) - surf.pos(u, v - hv)
    if surf.normal is not None and not surf.fd:
        N = surf.normal(u, v)
    else:
        N, ln = _unit(np.cross(Pu, Pv) * surf.orient)
        bad = ln < 1e-9
        if bad.any():
            N[bad] = surf.normal(u[bad], v[bad]) if surf.normal is not None else np.array([0, 1.0, 0])
    if surf.mat.bump is not None:
        b = surf.mat.bump
        hu, hv = du * .5, dv * .5
        lu = np.maximum(np.sqrt((Pu * Pu).sum(1)), 1e-6)
        lv = np.maximum(np.sqrt((Pv * Pv).sum(1)), 1e-6)
        gu = (b(u + hu, v) - b(u - hu, v)) / lu
        gv = (b(u, v + hv) - b(u, v - hv)) / lv
        Tu, Tv = Pu / lu[:, None], Pv / lv[:, None]
        N = _unit(N - surf.mat.bump_k * (gu[:, None] * Tu + gv[:, None] * Tv))[0]
    return P, N


def _shade(surf, P, N, V, u, v, rig):
    m = surf.mat
    g = {"u": u, "v": v, "P": P, "N": N, "V": V}
    if surf.extra is not None:
        g.update(surf.extra(u, v))
    g.setdefault("s", u * 300)
    g.setdefault("ang", v * 2 * np.pi)
    alb = m.albedo(g)
    NdV = np.clip((N * V).sum(1), 1e-4, 1)
    R = 2 * NdV[:, None] * N - V
    hemi = (N[:, 1] * .5 + .5)[:, None]
    amb = rig.ground * (1 - hemi) + rig.sky * hemi
    diff = np.zeros_like(P)
    spec = np.zeros_like(P)
    lobe = np.zeros_like(P)
    e = m.exp
    for L in rig.lights:
        if L.pos is not None:
            Ld, dist = _unit(L.pos - P)
            att = (1 / (1 + (dist / L.falloff) ** 2))[:, None]
        else:
            Ld = np.broadcast_to(L.dir, P.shape)
            att = 1.0
        ndl = (N * Ld).sum(1)
        df = np.clip((ndl + m.wrap) / (1 + m.wrap), 0, 1)
        Hh = _unit(Ld + V)[0]
        ndh = np.clip((N * Hh).sum(1), 0, 1)
        sp = ndh ** e * _sm(-.1, .15, ndl)
        rl = np.clip((R * Ld).sum(1), 0, 1) ** max(2.0, e * .1)
        diff += df[:, None] * att * L.col
        spec += sp[:, None] * att * L.col
        lobe += rl[:, None] * att * L.col
    envc = rig.env(R)
    fres = (1 - NdV) ** 5
    col = np.zeros_like(P)
    if m.metal < 1:
        cd = alb * (amb * m.amb + diff) + spec * m.ks + envc * (m.kr * (.04 + .96 * fres * m.fres))[:, None]
        if m.sheen:
            sc = m.sheen_col if m.sheen_col is not None else np.ones(3)
            cd = cd + (m.sheen * (1 - NdV) ** 2)[:, None] * sc * (diff * .6 + amb * .4)
        col += cd * (1 - m.metal)
    if m.metal > 0:
        tint = alb * (1 - m.spec_tint) + m.spec_tint
        cm = alb * (envc * m.env_k + diff * m.kd_metal + lobe * m.lobe + amb * .15) + spec * m.ks * tint
        col += cm * m.metal
    if m.emit is not None:
        col = col + (m.emit(g) if callable(m.emit) else C(m.emit))
    if m.ao is not None:
        col = col * m.ao(g)[:, None]
    return col


def _splat(zb, cb, idx, d, col_fn):
    o = np.argsort(-d, kind="stable")
    uq, first = np.unique(idx[o], return_index=True)
    sel = o[first]
    better = d[sel] > zb[uq]
    uq, sel = uq[better], sel[better]
    if len(sel) == 0:
        return
    zb[uq] = d[sel]
    cb[uq] = col_fn(sel)


def _fill_holes(zb, cb, h, w):
    filled = np.isfinite(zb).reshape(h, w)
    c3 = cb.reshape(h, w, 3)
    k = np.ones((3, 3), np.float32)
    for _ in range(3):
        cnt = ndimage.convolve(filled.astype(np.float32), k, mode="constant") - filled
        hole = (~filled) & (cnt >= 5)
        if not hole.any():
            break
        acc = np.stack([ndimage.convolve(c3[..., i] * filled, k, mode="constant") for i in range(3)], -1)
        c3[hole] = acc[hole] / cnt[hole][:, None]
        filled |= hole
    return filled


def _bbox(surfs, cam, pad=6):
    xs, ys = [], []
    for s_ in surfs:
        _, _, sx, sy = _dims(s_, cam, 1, 1)
        xs += [sx.min(), sx.max()]
        ys += [sy.min(), sy.max()]
    x0, x1 = max(0, int(min(xs)) - pad), min(W, int(max(xs)) + pad + 1)
    y0, y1 = max(0, int(min(ys)) - pad), min(H, int(max(ys)) + pad + 1)
    return x0, y0, x1, y1


def _raster(surfs, cam, rig, ss, mirror=None, box=None, dens=1.3):
    """Render surfaces into a supersampled z-buffer. mirror=floorY renders their reflection."""
    x0, y0, x1, y1 = box
    w, h = (x1 - x0) * ss, (y1 - y0) * ss
    zb = np.full(w * h, -np.inf, np.float32)
    cb = np.zeros((w * h, 3), np.float32)
    hb = np.zeros(w * h, np.float32) if mirror is not None else None
    for surf in surfs:
        if mirror is not None and not surf.reflect:
            continue
        nu, nv, _, _ = _dims(surf, cam, ss, dens)
        for u, v in _chunks(nu, nv):
            P, N = _geom(surf, u, v, 1 / nu, 1 / nv)
            V = _unit(cam.pos - P)[0]
            nd = (N * V).sum(1)
            if surf.two_sided:
                N = np.where(nd[:, None] < 0, -N, N)
                nd = np.abs(nd)
            keep = nd > -0.02
            if mirror is not None:
                Pm = P.copy()
                Pm[:, 1] = 2 * mirror - P[:, 1]
                sx, sy, d = cam.proj(Pm)
            else:
                sx, sy, d = cam.proj(P)
            ix = ((sx - x0) * ss).astype(np.int64)
            iy = ((sy - y0) * ss).astype(np.int64)
            keep &= (ix >= 0) & (ix < w) & (iy >= 0) & (iy < h)
            if not keep.any():
                continue
            P, N, V, u_, v_, d = P[keep], N[keep], V[keep], u[keep], v[keep], d[keep]
            idx = iy[keep] * w + ix[keep]
            _splat(zb, cb, idx, d, lambda sel: _shade(surf, P[sel], N[sel], V[sel], u_[sel], v_[sel], rig))
            if hb is not None:
                o = np.isfinite(zb[idx])
                hb[idx] = P[:, 1] - mirror
    filled = _fill_holes(zb, cb, h, w)
    a = filled.reshape(h // ss, ss, w // ss, ss).mean((1, 3))
    c = (cb.reshape(h, w, 3) * filled[..., None]).reshape(h // ss, ss, w // ss, ss, 3).mean((1, 3))
    hh = None
    if hb is not None:
        hh = hb.reshape(h // ss, ss, w // ss, ss).mean((1, 3))
    return a, c, hh


def _shadows(img, surfs, cam, lights, floor, wall_z, box_all, ao=0.55, ao_h=26, ao_blur=7, tint="#000000"):
    Hh, Ww, _ = img.shape
    for L in [l for l in lights if l.shadow > 0] + [None]:
        masks = [np.zeros((Hh, Ww), np.float32) for _ in range(3)]
        for surf in surfs:
            if not surf.cast:
                continue
            nu, nv, _, _ = _dims(surf, cam, 1, .7)
            for u, v in _chunks(nu, nv):
                P = surf.pos(u, v)
                if L is None:
                    S = P.copy()
                    S[:, 1] = floor
                    wgt = np.exp(-np.maximum(P[:, 1] - floor, 0) / ao_h)
                    sx, sy, _ = cam.proj(S)
                    ix, iy = sx.astype(int), sy.astype(int)
                    ok = (ix >= 0) & (ix < Ww) & (iy >= 0) & (iy < Hh)
                    np.maximum.at(masks[0], (iy[ok], ix[ok]), wgt[ok])
                    continue
                if L.pos is None:
                    dv = L.dir
                    S = P - dv[None, :] * ((P[:, 1] - floor) / max(dv[1], 1e-3))[:, None]
                    pen = L.size * .02 * np.maximum(P[:, 1] - floor, 0) / max(dv[1], .05)
                    sx, sy, _ = cam.proj(S)
                    ix, iy = sx.astype(int), sy.astype(int)
                    ok = (ix >= 0) & (ix < Ww) & (iy >= 0) & (iy < Hh)
                    b = np.digitize(pen, [6, 18])
                    for k in range(3):
                        sel = ok & (b == k)
                        masks[k][iy[sel], ix[sel]] = 1
                    continue
                lp = L.pos
                dy = lp[1] - P[:, 1]
                ok = dy > 1
                t = (lp[1] - floor) / np.maximum(dy, 1e-3)
                S = lp + (P - lp) * t[:, None]
                if wall_z is not None:
                    onwall = S[:, 2] < wall_z
                    dz = P[:, 2] - lp[2]
                    tw = (wall_z - lp[2]) / np.where(np.abs(dz) < 1e-3, -1e-3, dz)
                    Sw = lp + (P - lp) * tw[:, None]
                    S = np.where(onwall[:, None], Sw, S)
                    ok |= onwall & (tw > 0)
                dist_o = np.sqrt(((S - P) ** 2).sum(1))
                dist_l = np.sqrt(((P - lp) ** 2).sum(1))
                pen = L.size * dist_o / np.maximum(dist_l, 1)
                sx, sy, _ = cam.proj(S)
                ix, iy = sx.astype(int), sy.astype(int)
                ok &= (ix >= 0) & (ix < Ww) & (iy >= 0) & (iy < Hh)
                b = np.digitize(pen, [6, 18])
                for k in range(3):
                    sel = ok & (b == k)
                    masks[k][iy[sel], ix[sel]] = 1
        if L is None:
            m = ndimage.gaussian_filter(masks[0], ao_blur) * ao
            m = np.clip(m * 1.6, 0, ao)
        else:
            m = np.zeros((Hh, Ww), np.float32)
            for k, sd in enumerate((3, 9, 22)):
                if masks[k].any():
                    mk = ndimage.binary_closing(masks[k] > 0, iterations=2).astype(np.float32)
                    m = np.maximum(m, ndimage.gaussian_filter(mk, sd))
            m = np.clip(m * 1.15, 0, 1) * L.shadow
        img = img * (1 - m[..., None] * (1 - C(tint)))
    return img


def render(img, surfs, cam, rig, ss=3, shadow=None, reflect=None, blur=0, opacity=1.0, dens=1.3):
    """Shadows, then the floor reflection, then the objects themselves."""
    surfs = [x for x in surfs if x is not None]
    box = _bbox(surfs, cam)
    if shadow:
        sh = dict(shadow)
        img = _shadows(img, surfs, cam, rig.lights, sh.pop("floor", 0), sh.pop("wall_z", None), box, **sh)
    if reflect:
        fl = reflect.get("floor", 0)
        x0, y0, x1, y1 = box
        mb = (x0, y0, x1, min(H, y1 + (y1 - y0)))
        a, c, hh = _raster(surfs, cam, rig, 1, mirror=fl, box=mb, dens=1.0)
        fade = np.exp(-hh / reflect.get("fade", 160))
        k = reflect.get("k", .35)
        bl = reflect.get("blur", 2.5)
        a2 = ndimage.gaussian_filter(a * fade, bl)
        c2 = np.stack([ndimage.gaussian_filter(c[..., i] * fade, bl) for i in range(3)], -1)
        tint = C(reflect.get("tint", "#000000"))
        reg = img[mb[1]:mb[3], mb[0]:mb[2]]
        img[mb[1]:mb[3], mb[0]:mb[2]] = reg * (1 - a2[..., None] * k) + (c2 * (1 - .3) + tint * .3 * a2[..., None]) * k
    a, c, _ = _raster(surfs, cam, rig, ss, box=box, dens=dens)
    if blur:
        a = ndimage.gaussian_filter(a, blur)
        c = np.stack([ndimage.gaussian_filter(c[..., i], blur) for i in range(3)], -1)
    x0, y0, x1, y1 = box
    reg = img[y0:y1, x0:x1]
    img[y0:y1, x0:x1] = reg * (1 - a[..., None] * opacity) + np.clip(c, 0, 1.4) * opacity
    return img


def _run(img, job):
    out = job(img)
    return img if out is None else out


fx.EFFECTS["still3d"] = _run


def stage(s, surfs, cam, rig, **kw):
    """Queue a 3D render after the SVG painted so far; later SVG goes on top."""
    s.fx("still3d", job=lambda img: render(img, surfs, cam, rig, **kw))


def raster(s, fn):
    s.fx("still3d", job=fn)


# ============================================================ object builders
def angd(a, b):
    return (a - b + np.pi) % (2 * np.pi) - np.pi


def band_tex(bands, base=1.0):
    """Engraved rings on metal: bands = [(y, width, depth)] in local height."""
    def t(g):
        y = g["y"] if "y" in g else g.get("s", g["u"] * 0 - 1e4)
        out = np.full_like(y, base)
        for yy, wd, dp in bands:
            out *= 1 - dp * np.exp(-((y - yy) / wd) ** 2)
        return out
    return t


def hammered(scale=.08, amp=.6, seed=1):
    def b(u, v):
        return amp * fbm(u * 60 * scale * 10, v * 160 * scale * 10, 2, seed)
    return b


def kalash(at, sc=1.0, mat=None, M=None):
    """A brass kalasha: foot, round belly, narrow neck and a flared lip."""
    prof = [(0, 0), (46, 0), (52, 3), (50, 9), (44, 14), (62, 26), (98, 52), (118, 92), (112, 136), (88, 170),
            (60, 190), (52, 200), (56, 210), (70, 218), (78, 223), (76, 228), (66, 226), (54, 218), (46, 206), (40, 194)]
    m = mat or Mat(**BRASS_M, tex=band_tex([(92, 2.2, .45), (98, 1.2, .3), (136, 1.6, .35), (24, 1.5, .4), (200, 1.6, .4)]))
    return [lathe(prof, m, at=at, scale=sc, M=M)]


def coconut(at, sc=1.0, seed=1):
    def col(g):
        y, phi = g["y"], g["phi"]
        n = fbm(phi * 9, y * 0.06 / sc, 3, seed)
        fib = vnoise(phi * 140, y * .02 / sc, seed + 3)
        base = np.stack([.42 + .18 * n, .25 + .1 * n, .12 + .05 * n], -1)
        return base * (.8 + .35 * fib)[:, None]
    m = Mat(color=col, rough=.7, ks=.12, wrap=.2, kr=.05, bump=lambda u, v: 1.2 * vnoise(v * 260, u * 30, seed + 7), bump_k=1.0)
    t = np.linspace(0, np.pi, 50)
    prof = np.stack([np.sin(t) * 62 * (1 + .08 * np.sin(t)), -np.cos(t) * 76 + 76 + 8 * np.sin(t * 2) * 0], -1)
    prof[-1] = [0, prof[-1, 1]]
    tip = np.array([[6, 150], [3, 162], [0, 168]])
    prof = np.vstack([prof[:-2], tip])
    return lathe(prof, m, at=at, scale=sc, smooth=True)


def leaf(base, direction, length, width, mat, droop=.25, fold=.25, twist=0.0, curl=0.0, shape="mango", seed=1, side_up=None):
    """A leaf as a two-sided sheet growing from base along direction, sagging under gravity."""
    base = np.asarray(base, float)
    d = _unit(np.asarray(direction, float))[0]
    up = np.array([0, 1.0, 0]) if side_up is None else _unit(np.asarray(side_up, float))[0]
    sd = np.cross(d, up)
    if np.linalg.norm(sd) < 1e-6:
        sd = np.array([1.0, 0, 0])
    sd = _unit(sd)[0]
    nn = np.cross(sd, d)
    rng = random.Random(seed)
    asym = rng.uniform(-.08, .08)

    def wfun(u):
        if shape == "mango":
            return width * 2.2 * (u ** .55) * (1 - u) ** .9
        if shape == "banana":
            return width * np.clip(np.sqrt(np.clip(u * 30, 0, 1)) * np.clip((1 - u) * 6, 0, 1) ** .5, 0, 1)
        if shape == "peepal":
            return width * 1.7 * np.sin(np.pi * np.clip(u, 0, 1) ** .75) * (1 - u) ** .25
        if shape == "blade":
            return width * (1 - u) ** .8 * np.clip(u * 40, 0, 1)
        return width * np.sin(np.pi * u)

    def pos(u, v):
        s = u[:, None] * length
        cen = base + d * s - np.array([0, 1.0, 0]) * droop * length * u[:, None] ** 2
        cen = cen + nn * curl * length * (u[:, None] ** 2)
        wv = (v * 2 - 1)
        w = wfun(u) * (1 + asym * wv)
        ang = twist * u
        sdir = sd * np.cos(ang)[:, None] + nn * np.sin(ang)[:, None]
        ndir = nn * np.cos(ang)[:, None] - sd * np.sin(ang)[:, None]
        return cen + sdir * (wv * w)[:, None] + ndir * (fold * np.abs(wv) * w)[:, None]

    return sheet(pos, mat)


def leaf_mat(dark="#1e4a1c", light="#5f9a3a", vein="#b9d48a", seed=1, gloss=.5, spacing=.06, mid=.06):
    def col(g):
        u, v = g["u"], g["v"]
        wv = v * 2 - 1
        t = fbm(u * 6, v * 3, 3, seed)
        c = C(dark) * (1 - t[:, None]) + C(light) * t[:, None]
        vn = np.abs(np.sin((u - np.abs(wv) * .35) / spacing * np.pi))
        vein_m = _sm(.92, 1.0, vn) * .25 + np.exp(-(wv / mid) ** 2) * .55
        c = c * (1 - vein_m[:, None]) + C(vein) * vein_m[:, None]
        edge = _sm(.8, 1.0, np.abs(wv))
        return c * (1 - .25 * edge[:, None])
    return Mat(color=col, rough=1 - gloss * .6, ks=.25 + gloss * .35, wrap=.4, kr=.12, sheen=.2, sheen_col="#e8ffd0")


def bell(at, sc=1.0, M=None, mat=None):
    """A temple hand bell (ghanta): flared skirt, ringed handle and a lotus-bud finial."""
    m = mat or Mat(**BRASS_M, tex=band_tex([(8, 1.5, .4), (40, 1.2, .35), (96, 1.5, .35)]))
    body = [(0, 112), (30, 108), (44, 88), (52, 50), (60, 18), (70, 4), (76, 0), (78, 4), (74, 10), (64, 22),
            (58, 50), (52, 92), (38, 114), (16, 122), (0, 124)]
    handle = [(0, 120), (16, 124), (18, 130), (10, 136), (9, 150), (16, 156), (16, 162), (9, 168), (9, 186), (14, 192), (20, 198),
              (14, 205), (8, 208), (10, 218), (12, 226), (8, 236), (3, 246), (0, 250)]
    return [lathe(body, m, at=at, scale=sc, M=M), lathe(handle, m, at=at, scale=sc, M=M)]


def shankha(at, sc=1.0, M=None, gold=True, ap=np.pi / 2):
    """A sacred shankha (Turbinella pyrum): a long tapering canal, a broad shouldered body whorl
    with an opening on one side (local phi = ap) and a flared outer lip, and a short spire of
    whorls. Gold caps the spire and the canal and edges the lip. Local axis +Y runs to the spire."""
    Lc = 300.0

    def env(y):
        return np.interp(y, [0, 20, 60, 100, 140, 170, 192, 205, 222, 240, 258, 276, 290, 300],
                         [7, 11, 20, 34, 52, 64, 66, 60, 50, 39, 27, 15, 6, 0])

    def apw(y):
        return 1.05 * np.clip(np.sin(np.pi * np.clip((y - 40) / 160, 0, 1)), 0, 1) ** .55

    def rho(u, phi):
        y = u * Lc
        r = env(y)
        t = (y - 196) / 19 + phi / (2 * np.pi)
        ridge = .86 + .14 * np.sin(np.pi * (t - np.floor(t))) ** .5
        r = np.where(y > 196, r * ridge, r)
        r = r * (1 + .004 * np.sin(y * .5 + phi))
        a = np.abs(angd(phi, ap))
        w = apw(y)
        inside = _sm(w * 1.02, w * .7, a) * (w > .05)
        return r * (1 - .42 * inside), y, inside

    M = np.eye(3) if M is None else np.asarray(M, float)
    at = np.asarray(at, float)

    def pos(u, v):
        phi = 2 * np.pi * v
        r, y, _ = rho(u, phi)
        L = np.stack([r * np.sin(phi), y, r * np.cos(phi)], -1) * sc
        return L @ M.T + at

    def col(g):
        y = g["u"] * Lc
        phi = 2 * np.pi * g["v"]
        n = fbm(y * .05, phi * 2, 3, 5)
        c = np.stack([.98 - .03 * n, .95 - .05 * n, .89 - .08 * n], -1)
        streak = _sm(.6, .95, vnoise(y * .035 + phi * .4, phi * 2.5, 9)) * .16
        c = c * (1 - streak[:, None] * np.array([0, .3, .7]))
        _, _, ins = rho(g["u"], phi)
        deep = np.clip(ins, 0, 1)
        inner = np.stack([.98 - .1 * deep, .74 - .25 * deep, .62 - .28 * deep], -1)
        c = c * (1 - deep[:, None]) + inner * deep[:, None]
        if gold:
            gm = ((y > 268) | (y < 26)).astype(np.float32)
            gm = np.maximum(gm, np.exp(-((y - 262) / 3) ** 2))
            c = c * (1 - gm[:, None]) + C("#f0b94c") * gm[:, None]
        return c

    def ao(g):
        _, _, ins = rho(g["u"], 2 * np.pi * g["v"])
        return 1 - .35 * np.clip(ins, 0, 1) ** 2

    shell = Mat(color=col, rough=.32, ks=.6, wrap=.4, kr=.25, sheen=.18, sheen_col="#ffe8d0", ao=ao)
    surfs = [Surf(pos, shell, None, orient=-1, fd=True, dens=1.2)]

    # the flared outer lip, rising from one edge of the opening
    def lip(u, v):
        y = 46 + u * 150
        w = apw(y)
        phi = ap - w * 1.0
        r = env(y) * .99
        flare = 22 * np.sin(np.pi * u) ** .8 * v
        curl = 10 * np.sin(np.pi * u) * v * v
        rr = r + flare
        pl = phi - curl / np.maximum(r, 1) * .6
        L = np.stack([rr * np.sin(pl), y - 6 * v * np.sin(np.pi * u), rr * np.cos(pl)], -1) * sc
        return L @ M.T + at

    def lipcol(g):
        v = g["v"]
        c = np.broadcast_to(C("#f8eee0"), (len(v), 3)).copy()
        if gold:
            gm = _sm(.72, .82, v)
            c = c * (1 - gm[:, None]) + C("#f0b94c") * gm[:, None]
        return c
    surfs.append(sheet(lip, Mat(color=lipcol, rough=.3, ks=.6, wrap=.4, kr=.25), dens=1.2))
    if gold:
        tex = band_tex([(282, 1.2, .5), (290, 1, .5), (274, 1.2, .5), (10, 1.2, .5), (18, 1.2, .5)])
        gm = Mat(**GOLD_M, tex=tex)

        def gpos(lo, hi, grow):
            def p(u, v):
                phi = 2 * np.pi * v
                uu = lo + u * (hi - lo)
                r, y, _ = rho(uu, phi)
                r = np.maximum(r, env(y))
                L = np.stack([(r + grow) * np.sin(phi), y, (r + grow) * np.cos(phi)], -1) * sc
                return L @ M.T + at
            return p

        def gext(lo, hi):
            return lambda u, v: {"y": (lo + u * (hi - lo)) * Lc}
        surfs.append(Surf(gpos(268 / Lc, 1, 1.8), gm, None, orient=-1, fd=True, extra=gext(268 / Lc, 1)))
        surfs.append(Surf(gpos(0, 26 / Lc, 1.8), gm, None, orient=-1, fd=True, extra=gext(0, 26 / Lc)))
    return surfs


def samai(at, sc=1.0, wicks=5, M=None):
    """A standing brass oil lamp: domed foot, ringed stem, a lobed oil dish and a bud finial.
    Returns (surfaces, wick points in world space)."""
    m = Mat(**BRASS_M, tex=band_tex([(30, 1.5, .4), (120, 1.5, .35), (200, 1.5, .35)]))
    stem = [(0, 0), (86, 0), (90, 6), (84, 14), (58, 24), (40, 34), (26, 44), (22, 52), (28, 60), (24, 66), (12, 72),
            (10, 110), (22, 118), (24, 124), (12, 130), (9, 180), (18, 188), (18, 194), (8, 200), (7, 226), (0, 228)]
    k = wicks

    def lobes(u, phi, y):
        return 1 + .16 * np.clip(np.cos(phi * k), 0, 1) ** 3 * _sm(226, 246, y)
    dish = [(0, 222), (14, 224), (50, 228), (86, 236), (98, 244), (98, 248), (92, 248), (80, 242), (40, 238), (0, 236)]
    fin = [(0, 236), (10, 238), (8, 252), (14, 262), (16, 272), (10, 286), (4, 298), (0, 304)]
    if k == 1:
        dish = [(0, 222), (14, 224), (40, 228), (62, 236), (70, 244), (70, 248), (64, 248), (54, 242), (30, 238), (0, 236)]
        lobes = lambda u, phi, y: 1 + .45 * np.exp(-(angd(phi, 0) / .3) ** 2) * _sm(.3, .6, u)
    surfs = [lathe(stem, m, at=at, scale=sc, M=M), lathe(dish, m, at=at, scale=sc, M=M, mod=lobes), lathe(fin, m, at=at, scale=sc, M=M)]
    Mm = np.eye(3) if M is None else M
    tips = []
    for j in range(k):
        phi = 2 * np.pi * j / k
        r = (98 * 1.16 if k > 1 else 70 * 1.4) * sc
        tips.append(np.asarray(at) + Mm @ np.array([r * math.sin(phi), 250 * sc, r * math.cos(phi)]))
    oil = Mat(color="#6a3a10", rough=.1, ks=1.2, kr=.6, wrap=0)
    surfs.append(lathe([(0, 241), (84 if k > 1 else 58, 241), (0, 241.01)], oil, at=at, scale=sc, M=M, smooth=False, cast=False))
    return surfs, tips


def diya3d(at, sc=1.0, spout=0.0, clay="#b04a1e", painted=True, M=None):
    """A terracotta oil lamp with a pinched spout pointing at angle spout (radians, 0 = towards
    the viewer, +pi/2 = right). Returns (surfaces, wick tip in world space)."""
    def mod(u, phi, y):
        a = np.exp(-(angd(phi, spout) / .42) ** 2)
        return 1 + .55 * a * _sm(10, 38, y)

    def col(g):
        y, phi = g["y"], g["phi"]
        base = C(clay) * (.9 + .2 * fbm(phi * 8, y * .1, 3, 4))[:, None]
        if painted:
            dots = (np.cos(phi * 24) > .7) & (np.abs(y - 26) < 3)
            line = np.abs(y - 18) < 1.6
            base = np.where(dots[:, None], C("#f3e2b8"), base)
            base = np.where(line[:, None], C("#e8b13a"), base)
        return base
    prof = [(0, 0), (34, 0), (38, 3), (34, 6), (56, 14), (80, 28), (90, 36), (92, 40), (86, 41), (74, 34), (40, 22), (0, 18)]
    m = Mat(color=col, rough=.75, ks=.15, wrap=.3, kr=.08)
    oil = Mat(color="#4a2408", rough=.08, ks=1.4, kr=.7, wrap=0)
    surfs = [lathe(prof, m, at=at, scale=sc, M=M, mod=mod),
             lathe([(0, 27), (70, 27), (0, 27.01)], oil, at=at, scale=sc, M=M, smooth=False, cast=False, mod=lambda u, p, y: 1 + .4 * np.exp(-(angd(p, spout) / .4) ** 2))]
    r = 92 * 1.55 * sc
    tip = np.asarray(at) + np.array([r * math.sin(spout) * .97, 42 * sc, r * math.cos(spout) * .97])
    wick = tube([tip + np.array([-math.sin(spout), -.4, -math.cos(spout)]) * 34 * sc, tip], 4.5 * sc,
                Mat(color="#f2e6cc", rough=.9, ks=.05, wrap=.5), cast=False)
    surfs.append(wick)
    return surfs, tip


def bokeh_lamps(s, rows, cx=800, gap=150, seed=3, color="#ffb45a"):
    rng = random.Random(seed)
    out = []
    for y, n, r, a in rows:
        for k in range(n):
            x = (k + rng.uniform(.2, .8)) * 1600 / n
            if abs(x - cx) > gap:
                out.append(f'<circle cx="{f(x)}" cy="{f(y + rng.uniform(-10, 10))}" r="{r}" fill="{color}" opacity="{a}"/>')
    s.add(f'<g filter="{s.blur(4)}" style="mix-blend-mode:screen">{"".join(out)}</g>')


def flame_at(s, cam, P, h, **kw):
    x, y = cam.scr(P)
    s.flame(x, y + h * .06, h, **kw)
    return x, y


def folds(seed=1, amp=10, n=6, scale=260, dirn=None):
    """A height field of soft cloth folds."""
    rng = random.Random(seed)
    waves = []
    for _ in range(n):
        a = rng.uniform(0, math.pi) if dirn is None else dirn + rng.uniform(-.45, .45)
        waves.append((math.cos(a), math.sin(a), rng.uniform(.5, 1.5) * scale, rng.uniform(.3, 1) * amp, rng.uniform(0, 6.28)))

    def h(X, Z):
        out = np.zeros_like(X)
        for ca, sa, L, A, ph in waves:
            t = (X * ca + Z * sa) / L * 2 * np.pi + ph
            out += A * np.sin(t + .7 * np.sin(t * .5 + ph))
        return out + amp * .8 * (fbm(X / scale * 1.4, Z / scale * 1.4, 3, seed) - .5)
    return h


def cloth(x0, x1, z0, z1, hfn, mat, y0=0.0, **kw):
    def pos(u, v):
        X = x0 + u * (x1 - x0)
        Z = z0 + v * (z1 - z0)
        return np.stack([X, y0 + hfn(X, Z), Z], -1)

    def extra(u, v):
        return {"X": x0 + u * (x1 - x0), "Z": z0 + v * (z1 - z0)}
    kw.setdefault("cast", False)
    kw.setdefault("reflect", False)
    return Surf(pos, mat, None, orient=-1, fd=True, extra=extra, **kw)


def silk_mat(color, dark, border=None, gold="#e8b04a", weave=1.6, sheen=.55, rough=.5, ks=.35, seed=3):
    """Silk: a fine weave, a soft colour drift and a sheen; border(X, Z) -> 0..1 marks zari bands."""
    def col(g):
        X, Z = g["X"], g["Z"]
        n = fbm(X * .003, Z * .003, 3, seed)
        c = C(dark) * (1 - n[:, None]) + C(color) * n[:, None]
        wv = .95 + .05 * np.sin(X * weave) * np.sin(Z * weave * 1.1)
        c = c * wv[:, None]
        if border is not None:
            b = border(X, Z)
            patt = .75 + .25 * (np.sin(X * .35) * np.sin(Z * .35) > 0)
            c = c * (1 - b[:, None]) + (C(gold) * patt[:, None]) * b[:, None]
        return c
    return Mat(color=col, rough=rough, ks=ks, wrap=.3, kr=.12, sheen=sheen, sheen_col=color)


def align_y(a):
    """Rotation taking +Y to the direction a."""
    a = _unit(np.asarray(a, float))[0]
    y = np.array([0, 1.0, 0])
    v = np.cross(y, a)
    s_ = np.linalg.norm(v)
    c = y @ a
    if s_ < 1e-8:
        return np.eye(3) if c > 0 else np.diag([1, -1, -1.0])
    vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return np.eye(3) + vx + vx @ vx * ((1 - c) / s_ ** 2)


def rudraksha(c, r, axis, seed=1, mat=None):
    """A five-faced rudraksha bead: furrowed, warty, drilled along axis."""
    rng = random.Random(seed)
    ph0 = rng.uniform(0, 6.28)

    def mod(u, phi, y):
        gro = np.exp(-(np.sin((phi + ph0) * 2.5) ** 2) / .025)
        return 1 - .1 * gro * np.sin(np.pi * u) ** .5

    def bump(u, v):
        return 2.2 * vnoise(u * 22, v * 40, seed) + 1.0 * vnoise(u * 55, v * 100, seed + 1)
    tone = rng.uniform(-.06, .06)
    m = mat or Mat(color=lambda g: np.broadcast_to(np.array([.42 + tone, .2 + tone * .5, .11]), (len(g["u"]), 3)) *
                   (.75 + .45 * vnoise(g["u"] * 22, g["v"] * 40, seed))[:, None],
                   rough=.45, ks=.35, wrap=.25, kr=.1, bump=bump, bump_k=.06 * r)
    t = np.linspace(0, np.pi, 40)
    prof = np.stack([np.sin(t) * r, -np.cos(t) * r * .92], -1)
    prof[0, 0] = prof[-1, 0] = 0
    return lathe(prof, m, at=c, M=align_y(axis), mod=mod, smooth=False)


def katori(at, sc=1.0, mat=None, fill=None, fill_h=24, fill_dome=10, M=None):
    """A small brass bowl, optionally heaped with powder or paste (fill = Mat)."""
    m = mat or Mat(**BRASS_M, tex=band_tex([(30, 1.2, .4)]))
    prof = [(0, 0), (28, 0), (32, 2), (30, 5), (40, 12), (52, 26), (58, 36), (59, 39), (55, 40), (50, 34), (38, 20), (0, 15)]
    out = [lathe(prof, m, at=at, scale=sc, M=M)]
    if fill is not None:
        t = np.linspace(0, 1, 20)
        dome = np.stack([52 * (1 - t), fill_h + fill_dome * np.sin(np.pi / 2 * t) ** 1.5], -1)
        out.append(lathe(np.vstack([[[54, fill_h - 2]], dome]), fill, at=at, scale=sc, M=M, cast=False))
    return out


def powder(color, seed=1, rough=.95):
    def col(g):
        n = fbm(g["u"] * 18, g["v"] * 40, 3, seed)
        return np.broadcast_to(C(color), (len(n), 3)) * (.8 + .35 * n)[:, None]
    return Mat(color=col, rough=rough, ks=.03, wrap=.35, kr=.02, bump=lambda u, v: 1.5 * vnoise(u * 60, v * 160, seed), bump_k=.5)


def rice_grains(s, pts, sc=1.0, seed=1, color="#f6efdc", shade="#b9a07a", light=(-1, -1)):
    """Grains of raw rice at the given screen points (each lit from the light direction)."""
    rng = random.Random(seed)
    lx, ly = light
    out_s, out_b, out_h = [], [], []
    for x, y in pts:
        a = rng.uniform(0, 180)
        L, Wd = rng.uniform(6.5, 8.5) * sc, rng.uniform(2.4, 3.0) * sc
        out_s.append(f'<ellipse cx="{f(x - lx * 1.2 * sc)}" cy="{f(y - ly * 1.2 * sc)}" rx="{f(L / 2)}" ry="{f(Wd / 2)}" transform="rotate({a:.0f} {f(x - lx * 1.2 * sc)} {f(y - ly * 1.2 * sc)})"/>')
        out_b.append(f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(L / 2)}" ry="{f(Wd / 2)}" transform="rotate({a:.0f} {f(x)} {f(y)})"/>')
        out_h.append(f'<ellipse cx="{f(x + lx * .5 * sc)}" cy="{f(y + ly * .5 * sc)}" rx="{f(L * .32)}" ry="{f(Wd * .22)}" transform="rotate({a:.0f} {f(x)} {f(y)})"/>')
    s.add(f'<g fill="#1a0c04" opacity=".45" filter="{s.blur(1.2 * sc)}">{"".join(out_s)}</g>'
          f'<g fill="{shade}">{"".join(out_b)}</g>'
          f'<g fill="{color}" transform="translate({f(lx * .6 * sc)} {f(ly * .6 * sc)})">{"".join(out_b)}</g>'
          f'<g fill="#ffffff" opacity=".8">{"".join(out_h)}</g>')


def dof(img, y_focus, k=0.012, max_sd=10, x_focus=None, steps=5):
    """Shallow depth of field: blur grows with distance from the focal row."""
    Hh, Ww, _ = img.shape
    yy = np.arange(Hh, dtype=np.float32)[:, None]
    dist = np.abs(yy - y_focus) * np.ones((1, Ww), np.float32)
    if x_focus is not None:
        xx = np.arange(Ww, dtype=np.float32)[None, :]
        dist = np.maximum(dist, np.abs(xx - x_focus[0]) - x_focus[1])
    sd = np.clip(dist * k, 0, max_sd)
    levels = np.linspace(0, max_sd, steps)
    blurred = [img] + [np.stack([ndimage.gaussian_filter(img[..., c], l) for c in range(3)], -1) for l in levels[1:]]
    pos = sd / max_sd * (steps - 1)
    i0 = np.clip(np.floor(pos).astype(int), 0, steps - 2)
    t = (pos - i0)[..., None]
    out = np.zeros_like(img)
    for i in range(steps - 1):
        m = (i0 == i)[..., None]
        out = np.where(m, blurred[i] * (1 - t) + blurred[i + 1] * t, out)
    return out


def trails(s, center, rx, ry, a0, sweep, offsets, color="#ffd890", width=3.2, seed=1, laps=1):
    """Long-exposure light trails: each flame (offset from the lamp) traced along an ellipse
    that ends at angle a0 after sweeping `sweep` degrees."""
    cx, cy = center
    segs, glow = [], []
    n = 140
    for (ox, oy) in offsets:
        for lap in range(laps):
            for k in range(n):
                t0, t1 = k / n, (k + 1) / n
                a_0 = math.radians(a0 - sweep * (1 - t0) - lap * 360)
                a_1 = math.radians(a0 - sweep * (1 - t1) - lap * 360)
                x0, y0 = cx + rx * math.cos(a_0) + ox, cy + ry * math.sin(a_0) + oy
                x1, y1 = cx + rx * math.cos(a_1) + ox, cy + ry * math.sin(a_1) + oy
                op = t1 ** 1.6 * (.35 if lap else 1)
                segs.append(f'<path d="M{f(x0)} {f(y0)}L{f(x1)} {f(y1)}" stroke-opacity="{op:.3f}" stroke-width="{f(width * (.5 + .7 * t1))}"/>')
                glow.append(f'<path d="M{f(x0)} {f(y0)}L{f(x1)} {f(y1)}" stroke-opacity="{op * .6:.3f}" stroke-width="{f(width * 5 * (.5 + .7 * t1))}"/>')
    s.add(f'<g stroke="#ff9a40" fill="none" stroke-linecap="round" filter="{s.blur(9)}" style="mix-blend-mode:screen">{"".join(glow)}</g>'
          f'<g stroke="{color}" fill="none" stroke-linecap="round" filter="{s.blur(1.2)}" style="mix-blend-mode:screen">{"".join(segs)}</g>')


def sanctum(s, cx=800, cy=420, warm="#4a1e0a"):
    """A dark sanctum: warm air around the lamp, an out-of-focus golden arch and hanging bells."""
    s.add(f'<rect width="1600" height="1000" fill="#0b0503"/>')
    s.add(f'<rect width="1600" height="1000" fill="{s.rad([(0, warm, 1), (.5, mix(warm, "#0b0503", .6), 1), (1, "#0b0503", 1)], cx, cy, 1000, user=True)}"/>')


# ============================================================ scenes
def warm_room(s, hz, light=(800, 420), warm="#5a2812", floor_top="#3a1c0e", floor_glow="#ff9a50", glow_x=None, r=1100):
    ob.dark_room(s, light=light, warm=warm, r=r, horizon=hz, floor="#170a06")
    gx = light[0] if glow_x is None else glow_x
    s.add(f'<rect y="{hz}" width="1600" height="{1000 - hz}" fill="{s.lin([(0, floor_top, 1), (1, "#0e0503", 1)], 0, hz, 0, 1000, user=True)}"/>')
    s.add(f'<rect y="{hz}" width="1600" height="{1000 - hz}" fill="{s.rad([(0, floor_glow, .35), (1, floor_glow, 0)], gx, hz + 40, 700, user=True, transform=f"translate(0 {(hz + 40) * .7:.0f}) scale(1 .3)")}" style="mix-blend-mode:screen"/>')
    s.add(f'<path d="M0 {hz}H1600" stroke="#ffb070" stroke-opacity=".22" stroke-width="2"/>')


def kalava(center, r, y, mat=None):
    m = mat or Mat(color=lambda g: np.where((np.sin(g["s"] * .9 + g["ang"] * 3) > 0)[:, None], C("#c81e1e"), C("#e8c040")),
                   rough=.8, ks=.1, wrap=.4)
    t = np.linspace(0, 2 * np.pi, 49)
    path = [(center[0] + r * math.sin(a), y + 1.5 * math.sin(3 * a), center[2] + r * math.cos(a)) for a in t]
    return tube(path, 3.2, m, cap=False, cast=False)


@scene
def puja_items(s):
    hz = 640
    warm_room(s, hz, light=(1150, 420), warm="#5e2a12", glow_x=1150)
    ob.arch_niche(s, 800, 110, 580, hz, recess="#140b09", carve="#6e4630", light=(950, 520))
    bokeh_lamps(s, ((300, 14, 6, .35),))
    s.bokeh(7, 0, 1600, 40, 560, colors=("#ff8a2a", "#ffb43a"), r=(26, 60), a=(.06, .16), blur=4, seed=6, ring=True)
    cam = Cam(elev=22, x0=800, y0=hz + 150, dist=3800)
    wall_z = cam.at(800, hz)[2]
    # a red silk runner under the kalash
    run = silk_mat("#b0182a", "#5a0814", border=lambda X, Z: _sm(8, 2, np.abs(np.abs(X - 800) - 205)), seed=4)
    stage(s, [cloth(590, 1010, wall_z, 900, folds(3, 2.5, 5, 160, dirn=1.5), run, y0=1)], cam,
          Rig([Light(cam.at(1170, 720) + np.array([0, 330, 0]), "#ffcf8a", 2.0, 700)], sky="#3a2414", ground="#1a0a05", amb=.8), ss=1)
    k_at = cam.at(800, 800)
    surfs = kalash(k_at, 1.25)
    surfs.append(kalava(k_at, 66, k_at[1] + 196 * 1.25))
    lamp_at = cam.at(1180, 720)
    sm, tips = samai(lamp_at, 1.05)
    surfs += sm
    surfs += bell(cam.at(500, 830), 1.25)
    surfs += shankha(cam.at(1010, 900) + np.array([0, 50, 0]), 1.05, M=rots(("z", -96), ("x", 34), ("y", -14)), ap=-np.pi / 2)
    k_top = k_at + np.array([0, 228 * 1.25, 0])
    rig = Rig([Light(np.mean(tips, 0) + np.array([0, 50, 0]), "#ffcf8a", 2.3, 700, shadow=.7, size=40),
               Light(direction=(-.4, .5, .6), color="#5a4870", power=.35),
               Light(cam.at(700, 980) + np.array([0, 260, 300]), "#ffb070", .9, 500)],
              sky="#3a2414", ground="#1a0a05", amb=.9)
    stage(s, surfs, cam, rig, ss=3, shadow=dict(floor=0, ao=.6, ao_h=20, ao_blur=6, wall_z=wall_z),
          reflect=dict(floor=0, k=.3, fade=120, blur=2))
    lm = leaf_mat(seed=2, dark="#163e14", light="#4f8a2c")
    leaves = []
    for j, a in enumerate(np.linspace(0, 2 * np.pi, 7, endpoint=False)):
        dirv = (math.sin(a + .3), .7, math.cos(a + .3))
        leaves.append(leaf(k_top + np.array([0, -10, 0]), dirv, 250, 46, lm, droop=.62, fold=.22, seed=j))
    leaves.append(coconut(k_top + np.array([0, -2, 0]), 1.0))
    stage(s, leaves, cam, rig, ss=3)
    for t in tips:
        flame_at(s, cam, t, 46, glow_r=260, glow_a=.5)
    s.glow(1180, 380, 520, "#ff8a3a", .22, .2)
    s.add("".join(ob.marigold(x, y, r, c, k) for k, (x, y, r, c) in enumerate(
        [(330, 905, 26, "#f39a1c"), (372, 925, 22, "#f7c02a"), (640, 950, 24, "#e8562a"), (1290, 850, 24, "#f39a1c"), (1330, 872, 20, "#f7c02a")])))
    ob.petals_scatter(s, 260, 1400, hz + 150, hz + 340, 34, seed=5, size=(5, 9))
    s.add(f'<g filter="{s.blur(12)}">' + ob.marigold(130, 960, 84, "#f39a1c", 4) + ob.marigold(1500, 965, 70, "#e8562a", 5) + '</g>')
    s.motes(30, 900, 1400, 160, 520, seed=7, size=(.8, 1.8))
    s.fx("mottle", amp=.035, cell=50)
    return s


def aarti_geom(center, M, sc=1.0):
    """A five-cup brass aarti lamp on a handle, plus a raised centre cup. Returns (surfs, wick points)."""
    m = Mat(**BRASS_M, tex=band_tex([(8, 1.2, .4), (14, 1.0, .3)]))
    center = np.asarray(center, float)

    def lob(u, phi, y):
        return 1 + .18 * np.clip(np.cos(phi * 5), 0, 1) ** 4 * _sm(.3, .55, u)
    tray = [(0, 0), (40, -2), (78, 2), (100, 10), (110, 16), (108, 20), (100, 16), (74, 8), (0, 6)]
    surfs = [lathe(tray, m, at=center, M=M, scale=sc, mod=lob)]
    cup = [(0, 0), (8, 0), (15, 4), (22, 12), (25, 19), (23, 21), (19, 17), (0, 13)]
    wicks = []
    for k in range(5):
        a = 2 * np.pi * k / 5
        p = np.array([118 * math.sin(a), 12, 118 * math.cos(a)]) * sc
        surfs.append(lathe(cup, m, at=center + M @ p, M=M, scale=sc * 1.05))
        wicks.append(center + M @ (p + np.array([0, 21, 0]) * sc))
    col = [(0, 4), (16, 6), (10, 14), (8, 40), (14, 48), (10, 56), (14, 62), (24, 72), (30, 80), (28, 84), (22, 80), (0, 76)]
    surfs.append(lathe(col, m, at=center, M=M, scale=sc))
    wicks.append(center + M @ (np.array([0, 84, 0]) * sc))
    neck = [(0, -46), (12, -44), (16, -36), (10, -28), (12, -12), (24, -4), (30, 0), (0, 1)]
    surfs.append(lathe(neck, m, at=center, M=M, scale=sc))
    hp = [np.array(p) * sc for p in [(0, -40, 0), (10, -90, 20), (50, -150, 60), (120, -200, 120), (230, -250, 220)]]
    surfs.append(tube([center + M @ p for p in hp], lambda t: 11 * sc + 3 * sc * t, m, cap=False))
    surfs.append(lathe([(0, -60), (16, -58), (20, -50), (14, -44), (0, -42)], m, at=center, M=M, scale=sc))
    oil = Mat(color="#5a3008", rough=.1, ks=1.2, kr=.6, wrap=0)
    for k in range(5):
        a = 2 * np.pi * k / 5
        p = np.array([118 * math.sin(a), 12 + 16 * 1.05, 118 * math.cos(a)]) * sc
        surfs.append(lathe([(0, 0), (19, 0), (0, .01)], oil, at=center + M @ p, M=M, scale=sc, smooth=False))
    return surfs, wicks


@scene
def aarti_lamp(s):
    sanctum(s, 760, 420, warm="#3e1806")
    # the shrine behind, out of focus: a golden arch with jewels, garlands and hanging bells
    arch_d = "M420 1000V520C420 300 560 170 800 130C1040 170 1180 300 1180 520V1000"
    s.add(f'<path d="{arch_d}" fill="none" stroke="#c8862a" stroke-width="34" opacity=".28" filter="{s.blur(10)}"/>')
    s.add(f'<path d="{arch_d}" fill="none" stroke="#ffd890" stroke-width="6" opacity=".2" filter="{s.blur(6)}"/>')
    rng = random.Random(4)
    jew = []
    for k in range(40):
        t = k / 39
        a = math.pi * (1 - t)
        x = 800 + math.cos(a) * 380
        y = 520 - math.sin(a) * 390 if t > 0 else 520
        jew.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{rng.uniform(5, 12):.1f}" fill="#ffcf7a" opacity="{rng.uniform(.15, .45):.2f}"/>')
    s.add(f'<g filter="{s.blur(5)}" style="mix-blend-mode:screen">{"".join(jew)}</g>')
    ob.bells(s, [170, 300, 1300, 1440], -20, blur=9, sc=1.3)
    s.bokeh(10, 0, 1600, 60, 900, colors=("#ff8a2a", "#ffb43a"), r=(20, 60), a=(.06, .18), blur=5, seed=6, ring=True)
    cam = Cam(elev=14, x0=800, y0=600, dist=3600)
    c = cam.at(770, 500)
    M = rots(("x", 34), ("z", -12), ("y", 14))
    surfs, wicks = aarti_geom(c, M, 1.75)
    # trails first, under the lamp
    pts = [cam.scr(w) for w in wicks]
    cx, cy = np.mean(pts, 0)
    trails(s, (cx - 40, cy - 120), 360, 170, 72, 230, [(x - cx, y - cy) for x, y in pts[:5]], width=2.4, laps=1)
    rig = Rig([Light(np.mean(wicks, 0) + np.array([0, 80, 40]), "#ffcf8a", 2.6, 420),
               Light(direction=(-.6, .3, -.5), color="#7a5a8a", power=.25)],
              sky="#2a160a", ground="#0e0603", amb=.7,
              env=[(-1, "#120804"), (-.2, "#3a1c08"), (0.1, "#a8622a"), (.35, "#3a1c0a"), (1, "#0a0503")])
    stage(s, surfs, cam, rig, ss=3)
    for k, w in enumerate(wicks):
        flame_at(s, cam, w, 78 if k < 5 else 92, glow_r=320, glow_a=.4, lean=-.2)
    s.glow(cx, cy - 40, 420, "#ff9a40", .3, .2)
    s.motes(50, 300, 1300, 120, 760, seed=9, size=(.8, 2.2))
    s.fx("mottle", amp=.035, cell=50)
    s.look = {"bloom": 1.15, "vignette": .4}
    return s


def battlefield(s, hz, seed=3):
    """Two hosts far across the plain at dawn: a dark crowd bristling with spears, banners on
    tall poles and chariots with flags, half lost in golden dust."""
    rng = random.Random(seed)
    for side, (x0, x1) in enumerate(((-20, 690), (910, 1620))):
        for row, (dy, sc, col, a) in enumerate(((0, .45, "#8a6078", .5), (10, .7, "#6a4462", .65), (24, 1.0, "#4a2e4a", .8))):
            y = hz + dy
            crowd, spears, flags, carts = [], [], [], []
            pts = [(x0, y + 4)]
            x = x0
            while x < x1:
                x += rng.uniform(3, 7) * sc
                pts.append((x, y - rng.uniform(5, 11) * sc))
            pts.append((x1, y + 4))
            crowd.append("M" + "L".join(f"{f(px)} {f(py)}" for px, py in pts) + "Z")
            for _ in range(int((x1 - x0) / 9)):
                sx = rng.uniform(x0 + 10, x1 - 10)
                h = rng.uniform(26, 44) * sc
                lean = rng.uniform(-.08, .08) * h
                spears.append(f"M{f(sx)} {f(y - 4 * sc)}L{f(sx + lean)} {f(y - h)}")
            for _ in range(int((x1 - x0) / 70)):
                fx_ = rng.uniform(x0 + 20, x1 - 20)
                h = rng.uniform(60, 110) * sc
                spears.append(f"M{f(fx_)} {f(y - 4 * sc)}V{f(y - h)}")
                flags.append(arch.flag(fx_, y - h, rng.uniform(18, 30) * sc, rng.uniform(9, 14) * sc,
                                       rng.choice(["#d0703a", "#c04a3a", "#e0a040", "#b8603a"]), seed=rng.randint(0, 999)))
            if row == 2:
                for _ in range(3):
                    cx = rng.uniform(x0 + 60, x1 - 60)
                    w = 46
                    carts.append(f'<path d="M{f(cx - w / 2)} {f(y - 8)}h{f(w)}l-6 -22h{f(-w + 12)}Z"/>'
                                 f'<circle cx="{f(cx - 6)}" cy="{f(y - 6)}" r="11" fill="none" stroke="{col}" stroke-width="2.6"/>'
                                 f'<path d="M{f(cx - 14)} {f(y - 30)}q14 -14 28 0z"/><path d="M{f(cx)} {f(y - 36)}V{f(y - 130)}" stroke="{col}" stroke-width="2.4"/>')
                    carts.append(arch.flag(cx, y - 130, 40, 20, rng.choice(["#e07a2a", "#d04a2a"]), seed=int(cx)))
            s.add(f'<g opacity="{a}"><path d="{"".join(crowd)}" fill="{col}"/><path d="{"".join(spears)}" stroke="{col}" stroke-width="{f(1.1 * sc + .3)}"/>'
                  f'<g fill="{col}">{"".join(carts)}</g>{"".join(flags)}</g>')
        s.mist(hz + 8, 46, "#ffc89a", .4, 12, x0=x0 - 80, x1=x1 + 80)


@scene
def conch(s):
    hz = 640
    sun = (1000, 606)
    s.sky([(0, "#1a1d4a"), (.22, "#38326e"), (.42, "#7a4f86"), (.53, "#c47088"), (.6, "#f09a7a"), (.64, "#ffc88e"), (.7, "#ffe2b0")])
    s.stars(40, 0, 200, seed=3, bright=.5)
    s.sun(*sun, 32, halo_r=620, halo_a=.85)
    s.fx("clouds", y0=40, y1=330, seed=41, cell=150, aniso=3.4, cover=.42, soft=.16, lit="#ffb79a", body=.72, direct=.78,
         light=(0.2, 1), sun=(sun[0], sun[1], 400), opacity=.92)
    s.fx("clouds", y0=330, y1=560, seed=42, cell=90, aniso=5, cover=.33, soft=.2, lit="#ffd8a8", body=.85, direct=.9,
         light=(0, 1), sun=(sun[0], sun[1], 320), opacity=.85)
    far = ridgeline(hz - 4, 26, 51, cell=300, octaves=5, ridged=.3)
    hills(s, far, "#a07090", "#c890a0", haze="#ffcaa8", haze_a=.55, haze_h=40)
    s.add(f'<rect y="{hz}" width="1600" height="{1000 - hz}" fill="{s.lin([(0, "#d8a088", 1), (.2, "#a07068", 1), (.5, "#5a3a40", 1), (1, "#2a1a20", 1)], 0, hz, 0, 1000, user=True)}"/>')
    s.add(f'<rect y="{hz}" width="1600" height="{1000 - hz}" fill="#000" filter="{s.grain(.012, 4, .3, 12, "#000000")}" opacity=".35"/>')
    battlefield(s, hz + 6)
    s.fx("clouds", y0=hz - 70, y1=hz + 60, seed=44, cell=70, aniso=4, cover=.5, soft=.25, lit="#ffd2a2", body=.95, direct=.9,
         light=(.6, .4), sun=(sun[0], sun[1], 300), opacity=.7, top_fade=.4, bottom_fade=.5)
    s.mist(hz + 10, 80, "#ffd2a6", .5, 20)
    s.glow(sun[0], hz + 10, 560, "#ffb070", .4, .2, sy=.25)
    s.birds(6, 1100, 1350, 380, 450, color="#4a2a40", s=(5, 9), seed=4, a=.7)
    s.fx("godrays", cx=sun[0], cy=sun[1], strength=.35, thresh=.72, decay=.97, radius=260)
    # a low knoll in the foreground, rim-lit by the dawn
    knoll = smooth_line([(-40, 830), (300, 790), (620, 768), (900, 766), (1200, 780), (1640, 820)], 8)
    hills(s, knoll, "#2e1e2a", "#0c080c", rim="#ffc8a0", rim_a=.9, rim_center=sun, rim_r=900)
    from land import grass
    grass(s, -40, 1640, lambda x: y_at(knoll, x) + 3, 260, h=(8, 28), color="#1c121a", seed=5)
    cam = Cam(elev=14, x0=800, y0=810, dist=3600)
    cloth_y = 0
    run = silk_mat("#c8501a", "#6a1e08", border=lambda X, Z: _sm(6, 2, np.abs(np.abs(X - 800) - 225)) * .9, seed=9, sheen=.5)
    rig = Rig([Light(direction=(.5, .35, -.8), color="#ffc890", power=1.6),
               Light(direction=(-.35, .6, .72), color="#e0cce0", power=1.0, shadow=.55, size=60)],
              sky="#9a8aa8", ground="#4a3038", amb=.55,
              env=[(-1, "#2a1c24"), (-.1, "#7a5a68"), (0.05, "#ffc8a0"), (.2, "#c88a98"), (.6, "#5a4a80"), (1, "#2a2a5a")])
    cs = shankha(cam.at(800, 800) + np.array([-262, 54, 0]), 1.75, M=rots(("z", -97), ("x", 30), ("y", -10)), ap=-np.pi / 2)
    stage(s, cs, cam, rig, ss=3, shadow=dict(floor=0, ao=.6, ao_h=22, ao_blur=8))
    s.motes(30, 300, 1300, 420, 760, seed=8, color="#ffd8a8")
    s.fx("mottle", amp=.04, cell=60)
    return s


@scene
def thali(s):
    cam = Cam(elev=76, x0=800, y0=520, dist=4200)
    s.add('<rect width="1600" height="1000" fill="#1a0806"/>')
    border = lambda X, Z: (_sm(4, 1, np.abs(np.abs((X * .55 + Z * .83) + 700) - 46)) + _sm(30, 26, np.abs((X * .55 + Z * .83) + 700)) * .85
                           + _sm(3, 1, np.abs(np.abs((X * .55 + Z * .83) + 700) - 36)) * .0)
    silk = silk_mat("#9a1424", "#3a050c", border=lambda X, Z: np.clip(border(X - 800, Z), 0, 1), seed=5)
    diya_at = cam.at(980, 360, 6)
    ds, tip = diya3d(diya_at, .74, spout=math.radians(200))
    lamp = Light(tip + np.array([0, 40, 0]), "#ffc070", 1.7, 520, shadow=0, size=24)
    key = Light(direction=(-.45, .8, -.4), color="#ffe2c0", power=.75, shadow=.35, size=40)
    rig = Rig([lamp, key], sky="#4a2a20", ground="#1a0a06", amb=.6,
              env=[(-1, "#1a0a06"), (0, "#5a2a14"), (.4, "#b0703a"), (.8, "#3a2010"), (1, "#20100a")])
    stage(s, [cloth(-200, 1800, -700, 700, folds(8, 7, 4, 560, dirn=.7), silk)], cam, rig, ss=1)
    pc = cam.at(800, 520)
    plate = [(0, 0), (300, 0), (318, 4), (332, 16), (340, 24), (336, 28), (326, 22), (304, 9), (0, 7)]

    def plate_tex(g):
        rho, phi = g["rho"], g["phi"]
        t = np.ones_like(rho)
        for rr, d in ((60, .4), (64, .25), (150, .35), (154, .25), (250, .3), (290, .35)):
            t *= 1 - d * np.exp(-((rho - rr) / 1.3) ** 2)
        pet = np.abs(np.sin(phi * 8)) ** .5 * 40 + 70
        t *= 1 - .3 * np.exp(-((rho - pet) / 1.5) ** 2) * (rho < 112)
        pet2 = np.abs(np.sin(phi * 16 + .2)) ** .6 * 34 + 160
        t *= 1 - .25 * np.exp(-((rho - pet2) / 1.4) ** 2) * (rho > 150)
        return t
    surfs = [lathe(plate, Mat(**dict(BRASS_M, rough=.3), tex=plate_tex), at=pc)]
    surfs += ds
    surfs += katori(cam.at(640, 400, 7), 1.0, fill=powder("#c4102a", 2), fill_h=28, fill_dome=14)
    surfs += katori(cam.at(700, 640, 7), .9, fill=powder("#f0b21a", 3), fill_h=28, fill_dome=12)
    rice_c = cam.at(905, 615, 7)
    surfs += katori(rice_c, 1.05, fill=powder("#efe6cf", 4, rough=.7), fill_h=30, fill_dome=10)
    # paan leaves with areca nuts
    lm = leaf_mat(dark="#2a5a18", light="#7ab040", vein="#c8e090", seed=7, gloss=.8, spacing=.12)
    p0 = cam.at(560, 610, 9)
    surfs.append(leaf(p0, (-.2, .02, .9), 150, 70, lm, droop=.02, fold=.1, shape="peepal", seed=3))
    surfs.append(leaf(p0 + np.array([10, 2, 0]), (.35, .02, .9), 140, 64, lm, droop=.02, fold=.1, shape="peepal", seed=4))
    nut = Mat(color=lambda g: np.array([.5, .28, .14]) * (.7 + .5 * fbm(g["u"] * 9, g["v"] * 20, 3, 6))[:, None], rough=.5, ks=.25, wrap=.2,
              bump=lambda u, v: 2 * fbm(u * 8, v * 16, 3, 6), bump_k=.4)
    for k, (x, y) in enumerate(((566, 672), (596, 690), (574, 710))):
        surfs.append(ellipsoid(cam.at(x, y, 20), (15, 12, 15), nut))
    # incense sticks resting in a little holder
    hold = cam.at(1030, 640, 7)
    surfs.append(ellipsoid(hold + np.array([0, 6, 0]), (26, 12, 18), Mat(**BRASS_M)))
    stick = Mat(color="#3a1a10", rough=.9, ks=.05, wrap=.3)
    ends = []
    for k, ang in enumerate((-.25, 0, .25)):
        d = np.array([math.sin(-2.2 + ang), .55, math.cos(-2.2 + ang)])
        a_ = hold + np.array([0, 14, 0])
        e = a_ + _unit(d)[0] * 260
        surfs.append(tube([a_, e], 2.4, stick))
        ends.append(e)
    stage(s, surfs, cam, rig, ss=3, shadow=dict(floor=0, ao=.35, ao_h=5, ao_blur=4))
    # rice grains heaped in their bowl and scattered as akshata
    rng = random.Random(5)
    rx, ry = cam.scr(rice_c + np.array([0, 40, 0]))
    pts = []
    for _ in range(220):
        a, r = rng.uniform(0, 6.28), 48 * math.sqrt(rng.random())
        pts.append((rx + math.cos(a) * r, ry + math.sin(a) * r * .95))
    for _ in range(40):
        pts.append((rng.uniform(820, 1010), rng.uniform(690, 760)))
    rice_grains(s, pts, 1.0, seed=6, light=(-.7, -.7))
    # flowers on the plate
    fl = [(700, 300, 34, "#f39a1c"), (746, 268, 28, "#f7c02a"), (650, 300, 26, "#e8562a"), (1080, 470, 30, "#f39a1c"),
          (1110, 510, 24, "#f7c02a"), (880, 750, 26, "#e8562a")]
    s.add(f'<g filter="{s.blur(3)}" opacity=".6" transform="translate(8 10)">' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#1a0604"/>' for x, y, r, c in fl) + '</g>')
    s.add("".join(ob.marigold(x, y, r, c, k, light=(.6, .6)) for k, (x, y, r, c) in enumerate(fl)))
    ob.petals_scatter(s, 520, 1120, 260, 780, 36, colors=("#c91e3a", "#e8562a", "#a8102a"), seed=9, size=(6, 11))
    for e in ends:
        x, y = cam.scr(e)
        s.glow(x, y, 16, "#ff6a1a", .9, .3)
        s.add(f'<circle cx="{f(x)}" cy="{f(y)}" r="2.6" fill="#ffd080"/>')
    x, y = cam.scr(ends[1])
    s.smoke(x, y, 420, color="#f3e6d6", a=.4, seed=4, width=1.6, drift=-.2)
    flame_at(s, cam, tip, 92, glow_r=460, glow_a=.5)
    s.fx("mottle", amp=.035, cell=50)
    s.look = {"vignette": .42}
    return s


def mala_path(cx, cz, n=108, r0=300, r1=180, turns=1.7, start=np.pi / 2):
    t = np.linspace(0, 1, 800)
    th = start + t * turns * 2 * np.pi
    r = r0 + (r1 - r0) * t
    spiral = np.stack([cx + r * np.cos(th), cz + r * np.sin(th) * 1.0], -1)
    back = np.linspace(spiral[-1], spiral[0], 120)[1:]
    path = np.vstack([spiral, back])
    seg = np.sqrt((np.diff(path, axis=0) ** 2).sum(1))
    L = np.concatenate([[0], np.cumsum(seg)])
    st = np.linspace(0, L[-1], n + 1)[:-1]
    xs = np.interp(st, L, path[:, 0])
    zs = np.interp(st, L, path[:, 1])
    return np.stack([xs, zs], -1)


@scene
def mala(s):
    cam = Cam(elev=52, x0=800, y0=560, dist=3400)
    s.add('<rect width="1600" height="1000" fill="#3a1606"/>')
    hf = folds(11, 7, 4, 520, dirn=.5)
    silk = silk_mat("#c8601a", "#6a2408", seed=8, sheen=.35, ks=.25)
    key = Light(direction=(-.6, .62, -.45), color="#fff0d8", power=1.15, shadow=.6, size=40)
    rig = Rig([key, Light(direction=(.6, .3, .5), color="#ffb070", power=.25)], sky="#8a7a80", ground="#4a2a14", amb=.5,
              env=[(-1, "#3a1a08"), (0, "#8a5a30"), (.3, "#f0d8b0"), (.7, "#8a8090"), (1, "#5a5a70")])
    stage(s, [cloth(-500, 2100, -1300, 700, hf, silk)], cam, rig, ss=1)
    c0 = cam.at(800, 520)
    pts = mala_path(c0[0], c0[2] - 10, 108, 300, 196, 2.0)
    beads, Y = [], []
    rb = 13
    for k, (x, z) in enumerate(pts):
        y = float(hf(np.array([x]), np.array([z]))[0]) + rb * .9
        for j in range(k - 3):
            if np.hypot(*(pts[j] - pts[k])) < rb * 2.1:
                y = max(y, Y[j] + rb * 1.7)
        Y.append(y)
    P = np.stack([pts[:, 0], np.array(Y), pts[:, 1]], -1)
    surfs = []
    thread = Mat(color="#b8141c", rough=.7, ks=.15, wrap=.4)
    surfs.append(tube(np.vstack([P, P[:1]]), 2.0, thread, cap=False))
    for k in range(108):
        ax = P[(k + 1) % 108] - P[k - 1]
        surfs.append(rudraksha(P[k], rb * (1 + .06 * math.sin(k * 2.7)), ax, seed=k))
    # the guru bead and the tassel, where the loop closes
    g0 = (P[0] + P[-1]) / 2 + np.array([0, 5, 30])
    surfs.append(rudraksha(g0, rb * 1.45, (0, 0, 1), seed=200))
    knot = g0 + np.array([0, -4, 30])
    surfs.append(ellipsoid(knot, (9, 8, 10), thread))
    rng = random.Random(3)
    tas = Mat(color=lambda g: np.array([.86, .3, .08]) * (.85 + .3 * vnoise(g["u"] * 3, g["v"] * 3, 2))[:, None], rough=.8, ks=.08, wrap=.5, sheen=.4, sheen_col="#ffb070")
    for k in range(34):
        a = rng.uniform(-.5, .5)
        L = rng.uniform(150, 190)
        e = knot + np.array([math.sin(a) * L, 0, math.cos(a) * L * .9])
        mid = (knot + e) / 2 + np.array([rng.uniform(-6, 6), 0, 0])
        for p in (mid, e):
            p[1] = float(hf(np.array([p[0]]), np.array([p[2]]))[0]) + 2
        surfs.append(tube([knot, mid, e], 1.7, tas, cap=True))
    surfs.append(ellipsoid(knot + np.array([0, -1, 18]), (8, 7, 16), thread))
    stage(s, surfs, cam, rig, ss=3, shadow=dict(floor=0, ao=.6, ao_h=10, ao_blur=4))
    raster(s, lambda img: dof(img, 520, k=.011, max_sd=8))
    ob.petals_scatter(s, 260, 560, 640, 900, 14, colors=("#f39a1c", "#f7c02a", "#c91e3a"), seed=4, size=(6, 11))
    ob.petals_scatter(s, 1080, 1360, 300, 520, 10, colors=("#f39a1c", "#f7c02a", "#c91e3a"), seed=5, size=(6, 11))
    s.add(f'<rect width="1600" height="1000" fill="{s.rad([(0, "#fff0d0", .22), (1, "#fff0d0", 0)], 200, 0, 1100, user=True)}" style="mix-blend-mode:screen"/>')
    s.fx("mottle", amp=.03, cell=60)
    s.look = {"vignette": .38, "vibrance": .05}
    return s


# ---------- sweets, butter and the little mouse
def modak_sweet(at, sc=1.0, seed=1, tone="#fff8ec"):
    rng = random.Random(seed)
    tw = rng.uniform(-.0004, .0004)
    ph = rng.uniform(0, 6.28)

    def mod(u, phi, y):
        rib = np.abs(np.cos((phi + ph + tw * y * 40 / sc) * 6))
        env = _sm(6 * sc, 26 * sc, y) * (1 - _sm(66 * sc, 90 * sc, y))
        return 1 + .085 * (rib ** 2.5 - .35) * env
    prof = [(0, 0), (34, 0), (41, 3), (46, 13), (46, 25), (41, 40), (31, 56), (19, 70), (9, 81), (4, 88), (1.5, 94), (0, 96)]

    def col(g):
        n = fbm(g["phi"] * 3, g["y"] * .05, 3, seed)
        return np.broadcast_to(C(tone), (len(n), 3)) * (.93 + .1 * n)[:, None]
    m = Mat(color=col, rough=.42, ks=.3, wrap=.6, kr=.12, sheen=.35, sheen_col="#fff4e0", amb=1.4)
    return lathe(prof, m, at=at, scale=sc, mod=mod)


def banana_round(c, r, y, seed=1, mat=None):
    """A round piece of banana leaf laid flat, its midrib running left to right."""
    def col(g):
        X, Z = g["P"][:, 0] - c[0], g["P"][:, 2] - c[2]
        n = fbm(X * .01, Z * .01, 3, seed)
        base = C("#1e5a1a") * (1 - n[:, None]) + C("#4e9a30") * n[:, None]
        vein = .5 + .5 * np.sin((X + Z * .08) * .55)
        base = base * (.9 + .12 * vein)[:, None]
        mid = np.exp(-(Z / 6) ** 2) * .7
        base = base * (1 - mid[:, None]) + C("#8aa848") * mid[:, None]
        edge = _sm(r * .9, r, np.hypot(X, Z))
        return base * (1 - .3 * edge)[:, None]

    def pos(u, v):
        rr = u * r * (1 + .03 * np.sin(v * 2 * np.pi * 5 + seed))
        a = v * 2 * np.pi
        X, Z = c[0] + rr * np.cos(a), c[2] + rr * np.sin(a)
        return np.stack([X, y + 2 * np.sin(rr * .03) * u, Z], -1)
    m = mat or Mat(color=col, rough=.35, ks=.5, wrap=.3, kr=.2)
    return Surf(pos, m, None, two_sided=True, cast=False, reflect=False)


def mouse(at, heading=0.0, sc=1.0):
    """Mushika, Ganesha's little mouse, as soft fur-shaded ellipsoids; heading in degrees (0 = towards the viewer)."""
    at = np.asarray(at, float)
    R = rot("y", heading)

    def furc(g):
        n = fbm(g["u"] * 8, g["v"] * 16, 3, 3)
        return np.broadcast_to(C("#8c7a6a"), (len(n), 3)) * (.82 + .3 * n)[:, None]
    fur = Mat(color=furc, rough=.85, ks=.08, wrap=.45, kr=.05, sheen=.7, sheen_col="#e8dccb",
              bump=lambda u, v: .8 * vnoise(u * 60, v * 140, 5), bump_k=.25)
    pink = Mat(color="#d8908a", rough=.5, ks=.25, wrap=.5, sheen=.3, sheen_col="#ffd8d0")
    eye = Mat(color="#0a0606", rough=.08, ks=1.6, kr=.5, wrap=0)
    P = lambda x, y, z: at + R @ (np.array([x, y, z]) * sc)
    out = [ellipsoid(P(0, 27, -4), (27, 25, 42), fur, M=R @ rot("x", -6)),
           ellipsoid(P(0, 36, 40), (17, 16, 27), fur, M=R @ rot("x", 18)),
           ellipsoid(P(0, 28.5, 64), (3.6, 3.4, 3.6), pink),
           ellipsoid(P(-9.5, 42, 52), (3.6, 3.8, 3.4), eye), ellipsoid(P(9.5, 42, 52), (3.6, 3.8, 3.4), eye)]
    for sx in (-1, 1):
        out.append(ellipsoid(P(sx * 15, 55, 34), (11, 13, 3.2), pink, M=R @ rot("y", sx * 22) @ rot("z", -sx * 20)))
        out.append(ellipsoid(P(sx * 10, 6, 30), (5, 4, 8), pink))
        out.append(ellipsoid(P(sx * 16, 6, -26), (6, 4, 10), pink))
    tail = [P(0, 14, -42), P(6, 6, -72), P(30, 2, -104), P(70, 2, -118), P(110, 2, -104)]
    out.append(tube(tail, lambda t: (4.4 - 3 * t) * sc, pink))
    return out, P(0, 28.5, 66)


def whiskers(s, x, y, sc=1.0, color="#f0e6d6"):
    d = []
    for sx in (-1, 1):
        for k, a in enumerate((-12, 2, 16)):
            L = 46 * sc
            r = math.radians(a)
            d.append(f"M{f(x + sx * 3 * sc)} {f(y)}Q{f(x + sx * L * .5)} {f(y + math.sin(r) * L * .3 - 4 * sc)} {f(x + sx * L * math.cos(r))} {f(y + math.sin(r) * L)}")
    s.add(f'<path d="{"".join(d)}" stroke="{color}" stroke-width="{f(.9 * sc)}" stroke-opacity=".7" fill="none"/>')


@scene
def modak(s):
    hz = 600
    warm_room(s, hz, light=(800, 420), warm="#5a2610", glow_x=800)
    bokeh_lamps(s, ((250, 18, 7, .45), (330, 13, 11, .3)), gap=0, seed=5)
    s.bokeh(10, 0, 1600, 20, 560, colors=("#ff8a2a", "#ffb43a", "#ff5a6a"), r=(24, 70), a=(.08, .2), blur=5, seed=8, ring=True)
    s.add(f'<g filter="{s.blur(3.5)}" opacity=".85">')
    ob.garland(s, -40, -20, 820, -20, 60, r=24, seed=4, tassel=False)
    ob.garland(s, 780, -20, 1640, -20, 60, r=24, seed=5, tassel=False)
    s.add('</g>')
    cam = Cam(elev=30, x0=800, y0=740, dist=3800)
    pc = cam.at(800, 760)
    lamps = []
    surfs = []
    for (x, y, sp) in ((420, 650, .4), (1190, 650, -.4), (1330, 905, -.9)):
        d, tip = diya3d(cam.at(x, y), .62 if y < 800 else .75, spout=sp)
        surfs += d
        lamps.append(tip)
    plate = [(0, 0), (250, 0), (272, 6), (286, 18), (292, 26), (288, 30), (278, 24), (258, 10), (0, 8)]
    surfs.append(lathe(plate, Mat(**BRASS_M, tex=band_tex([(18, 1.2, .4)])), at=pc))
    rig = Rig([Light(cam.at(800, 600) + np.array([0, 420, -120]), "#ffd09a", 1.4, 900, shadow=.55, size=60)] +
              [Light(t + np.array([0, 40, 0]), "#ffb060", .8, 380) for t in lamps] +
              [Light(direction=(-.2, .5, .85), color="#ffd8b0", power=.45)],
              sky="#4a2a18", ground="#1a0a06", amb=.75)
    stage(s, surfs, cam, rig, ss=3, shadow=dict(floor=0, ao=.6, ao_h=16, ao_blur=6), reflect=dict(floor=0, k=.3, fade=90, blur=2))
    items = [banana_round(pc, 236, 9, seed=2)]
    ring = [(np.cos(a) * 128, np.sin(a) * 118) for a in np.linspace(0, 2 * np.pi, 7, endpoint=False) + .3]
    for k, (dx, dz) in enumerate(ring):
        items.append(modak_sweet(pc + np.array([dx, 10, dz]), 1.0, seed=k))
    for k, a in enumerate(np.linspace(0, 2 * np.pi, 3, endpoint=False) + .9):
        items.append(modak_sweet(pc + np.array([np.cos(a) * 46, 46, np.sin(a) * 46]), 1.0, seed=10 + k))
    items.append(modak_sweet(pc + np.array([0, 98, 0]), 1.0, seed=20))
    ms, nose = mouse(pc + np.array([226, 10, 166]), heading=-126, sc=1.55)
    items += ms
    stage(s, items, cam, rig, ss=3, shadow=dict(floor=9, ao=.55, ao_h=12, ao_blur=5))
    nx, ny = cam.scr(nose)
    whiskers(s, nx, ny, 1.0)
    for t in lamps:
        flame_at(s, cam, t, 64 if cam.scr(t)[1] < 800 else 80, glow_r=320, glow_a=.5)
    ob.petals_scatter(s, 200, 1400, 820, 960, 30, seed=5, size=(5, 10))
    s.add("".join(ob.marigold(x, y, r, c, k) for k, (x, y, r, c) in enumerate(
        [(300, 880, 28, "#f39a1c"), (350, 905, 24, "#f7c02a"), (1080, 930, 26, "#e8562a"), (520, 960, 22, "#f7c02a")])))
    s.motes(30, 300, 1300, 140, 520, seed=7, size=(.8, 1.8))
    s.fx("mottle", amp=.035, cell=50)
    return s


def peacock_feather(s, x0, y0, x1, y1, w=70, seed=1):
    """A peacock feather from its quill at (x0, y0) to its eye near (x1, y1)."""
    rng = random.Random(seed)
    L = math.hypot(x1 - x0, y1 - y0)
    ang = math.degrees(math.atan2(x1 - x0, -(y1 - y0)))
    out = [f'<g transform="translate({f(x0)} {f(y0)}) rotate({ang:.1f})">']
    barbs = []
    for k in range(260):
        t = .1 + .9 * k / 260
        y = -L * t
        reach = w * (.35 + .65 * min(1, t * 1.2)) * (1.1 if t > .75 else 1)
        for sd in (-1, 1):
            l2 = reach * rng.uniform(.75, 1.05)
            c = rng.choice(["#6a9a3a", "#3a8a5a", "#b8a03a", "#4a7a3a", "#9a8a30", "#2a8a7a"])
            barbs.append(f'<path d="M0 {f(y)}Q{f(sd * l2 * .5)} {f(y - l2 * .25)} {f(sd * l2)} {f(y - l2 * .55)}" stroke="{c}" stroke-opacity="{rng.uniform(.45, .9):.2f}"/>')
    out.append(f'<g fill="none" stroke-width="1.6" filter="{s.blur(.6)}">{"".join(barbs)}</g>')
    out.append(f'<path d="M-2 0Q0 {f(-L * .5)} 0 {f(-L * 1.02)}L1.5 {f(-L * .5)}L2 0Z" fill="#e8dcb0"/>')
    ey = -L + w * .1
    eye = [(1.0, 1.15, "#6a7a26", .9), (.82, .95, "#c89a38", 1), (.68, .8, "#2a8a5a", 1), (.54, .64, "#1aa0a0", 1),
           (.4, .48, "#7a5a2a", 1), (.33, .4, "#163a9a", 1), (.18, .2, "#0a1a5a", 1)]
    for rx, ry, c, a in eye:
        out.append(f'<ellipse cx="0" cy="{f(ey + (1 - ry) * w * .12)}" rx="{f(rx * w * .5)}" ry="{f(ry * w * .5)}" fill="{c}" opacity="{a}"/>')
    lines = "".join(f'<path d="M0 {f(ey + w * .4)}L{f(math.sin(a) * w * .62)} {f(ey + w * .1 - math.cos(a) * w * .66)}"/>' for a in np.linspace(-2.6, 2.6, 40))
    out.append(f'<g stroke="#0a1a20" stroke-opacity=".18" stroke-width="1">{lines}</g>')
    out.append(f'<ellipse cx="{f(-w * .12)}" cy="{f(ey - w * .12)}" rx="{f(w * .1)}" ry="{f(w * .16)}" fill="#ffffff" opacity=".18" filter="{s.blur(3)}"/>')
    out.append('</g>')
    s.add("".join(out))


def rope_mat(color="#b08a54", dark="#5a3a18"):
    def col(g):
        st = .5 + .5 * np.sin(g["s"] * .9 + g["ang"] * 2)
        return C(dark) * (1 - st[:, None]) + C(color) * st[:, None]
    return Mat(color=col, rough=.85, ks=.08, wrap=.4, bump=lambda u, v: 0 * u, bump_k=0)


def clay_pot(at, sc=1.0, seed=2, color="#b25a2c", M=None):
    prof = [(0, 0), (40, 0), (70, 6), (112, 28), (142, 70), (150, 118), (140, 168), (112, 206), (78, 226), (66, 236),
            (68, 246), (78, 252), (80, 258), (74, 262), (64, 256), (56, 246), (52, 236)]

    def potc(g):
        y, phi = g["y"] / sc, g["phi"]
        n = fbm(phi * 6, y * .03, 3, seed)
        c = C(color) * (.8 + .32 * n)[:, None]
        band = np.exp(-((y - 196) / 4) ** 2) + np.exp(-((y - 186) / 2) ** 2) + np.exp(-((y - 140) / 2.5) ** 2) * .6
        c = c * (1 - .45 * band[:, None]) + C("#f0e2c0") * (.45 * band)[:, None]
        soot = _sm(60, 0, y) * .4
        return c * (1 - soot[:, None])
    return lathe(prof, Mat(color=potc, rough=.82, ks=.1, wrap=.3, kr=.05,
                           bump=lambda u, v: 1.2 * fbm(u * 40, v * 90, 2, 4), bump_k=.5), at=at, scale=sc, M=M)


@scene
def butter_pot(s):
    # a village room, backlit by a barred window pouring in the morning
    s.add(f'<rect width="1600" height="1000" fill="{s.lin([(0, "#4a3424", 1), (.6, "#5a4030", 1), (.84, "#3a2618", 1)], 0, 0, 0, 1000, user=True)}"/>')
    s.add(f'<rect width="1600" height="1000" fill="#000" filter="{s.grain(.006, 3, .25, 9, "#000000")}" opacity=".35"/>')
    wx0, wy0, wx1, wy1 = 170, 200, 450, 560
    s.add(f'<rect width="1600" height="1000" fill="{s.rad([(0, "#ffe0a8", .35), (1, "#ffe0a8", 0)], 310, 380, 700, user=True)}" style="mix-blend-mode:screen"/>')
    s.add(f'<rect y="840" width="1600" height="160" fill="{s.lin([(0, "#3a2818", 1), (1, "#160c06", 1)], 0, 840, 0, 1000, user=True)}"/>')
    s.add('<path d="M0 840H1600" stroke="#1a0e06" stroke-width="5" opacity=".6"/>')
    s.add(f'<rect x="{wx0 - 28}" y="{wy0 - 28}" width="{wx1 - wx0 + 56}" height="{wy1 - wy0 + 56}" fill="#2a1a0e"/>')
    s.add(f'<rect x="{wx0}" y="{wy0}" width="{wx1 - wx0}" height="{wy1 - wy0}" fill="{s.lin([(0, "#fffcf0", 1), (.6, "#fff4d0", 1), (1, "#eef2c8", 1)], 0, wy0, 0, wy1, user=True)}"/>')
    s.add(f'<g filter="{s.blur(7)}" opacity=".5">' + "".join(
        f'<circle cx="{wx0 + 30 + k * 60}" cy="{wy1 - 20 - (k % 2) * 50}" r="{48 + (k % 3) * 14}" fill="#b8d08a"/>' for k in range(5)) + '</g>')
    s.add("".join(f'<rect x="{wx0 + k * (wx1 - wx0) / 4 - 7:.0f}" y="{wy0}" width="14" height="{wy1 - wy0}" fill="#2a1a0e"/>' for k in (1, 2, 3)))
    s.add(f'<rect x="{wx0 - 44}" y="{wy1 + 28}" width="{wx1 - wx0 + 88}" height="20" fill="#3a2414"/>')
    # sun on the floor, and the shaft through the dusty air
    s.add(f'<path d="M560 860L980 860L1180 1000L640 1000Z" fill="#ffe2a8" opacity=".5" filter="{s.blur(18)}" style="mix-blend-mode:screen"/>')
    s.add(f'<path d="M{wx0} {wy0}L{wx1} {wy0}L1180 1000L640 1000Z" fill="{s.lin([(0, "#fff0c8", .3), (1, "#ffd890", .08)], 0, 0, 1, 1)}" filter="{s.blur(36)}" style="mix-blend-mode:screen"/>')
    s.add(f'<rect x="0" y="0" width="1600" height="70" fill="#1a0e06"/><rect x="0" y="66" width="1600" height="8" fill="#3a2410"/>')
    cam = Cam(elev=6, x0=800, y0=800, dist=3600)
    base = cam.at(860, 700, 0)
    sc = 1.45
    pot = clay_pot(base, sc)
    bm = Mat(color=lambda g: np.broadcast_to(C("#fbf4e2"), (len(g["u"]), 3)) * (.92 + .1 * fbm(g["u"] * 8, g["v"] * 18, 3, 6))[:, None],
             rough=.4, ks=.35, wrap=.6, kr=.12, sheen=.25, sheen_col="#fff8e8",
             bump=lambda u, v: 6 * fbm(u * 5, v * 12, 3, 8), bump_k=.6)
    t = np.linspace(0, 1, 26)
    dome = np.stack([62 * (1 - t ** 1.6), 244 + 50 * np.sin(np.pi / 2 * t) ** .9], -1)
    butter = lathe(np.vstack([[[64, 240]], dome]), bm, at=base, scale=sc, mod=lambda u, p, y: 1 + .08 * np.sin(p * 3 + 1) * u + .05 * np.sin(p * 7) * u)
    drip = [ellipsoid(base + np.array([62 * math.sin(a), 238 - k * 10, 62 * math.cos(a)]) * np.array([sc, 1, sc]) + np.array([0, 238 * (sc - 1), 0]),
                      (11, 20 + k * 6, 11), bm) for k, a in enumerate((.35, -.5))]
    hook = base + np.array([0, 820, -10])
    rm = rope_mat()
    ropes = []
    for k in range(4):
        a = math.pi / 4 + k * math.pi / 2
        pts = [hook, base + np.array([math.sin(a) * 50, 560, math.cos(a) * 50]),
               base + np.array([math.sin(a) * 92, 222, math.cos(a) * 92]) * np.array([sc, sc, sc]),
               base + np.array([math.sin(a) * 154, 118, math.cos(a) * 154]) * np.array([sc, sc, sc]),
               base + np.array([math.sin(a) * 118, 26, math.cos(a) * 118]) * np.array([sc, sc, sc]),
               base + np.array([math.sin(a) * 40, -6, math.cos(a) * 40]) * np.array([sc, sc, sc])]
        pts[2:] = [base + (p - base) for p in pts[2:]]
        ropes.append(tube(pts, 5, rm, cap=False))
    ring_pts = [base + np.array([math.sin(a) * 42 * sc, -6 * sc, math.cos(a) * 42 * sc]) for a in np.linspace(0, 2 * np.pi, 25)]
    ropes.append(tube(ring_pts, 6, rm, cap=False))
    ropes.append(tube([hook + np.array([0, -10, 0]), hook + np.array([0, 300, 0])], 6, rm))
    # a churning pot on the floor with its wooden churn
    fpos = cam.at(1330, 930)
    churn = [clay_pot(fpos, .9, seed=5, color="#9a4a24")]
    wood = Mat(color=lambda g: C("#7a4a24") * (.8 + .3 * fbm(g["u"] * 3, g["v"] * 6, 3, 2))[:, None], rough=.55, ks=.2, wrap=.3)
    churn.append(tube([fpos + np.array([0, 150, 0]), fpos + np.array([-60, 560, -60])], 7, wood))
    churn.append(lathe([(0, 0), (14, 2), (16, 20), (10, 30), (0, 32)], wood, at=fpos + np.array([-60, 560, -60]), M=align_y((-.14, 1, -.14))))
    rig = Rig([Light(direction=(-.72, .4, -.5), color="#fff0d0", power=1.6),
               Light(direction=(.45, .25, .85), color="#d8905a", power=.55)],
              sky="#8a6a50", ground="#3a2414", amb=.55,
              env=[(-1, "#2a1a0e"), (0, "#6a4a30"), (.4, "#fff0c8"), (1, "#4a3020")])
    stage(s, churn, cam, rig, ss=2, shadow=dict(floor=0, ao=.6, ao_h=20, ao_blur=8))
    stage(s, [pot, butter] + drip + ropes, cam, rig, ss=3)
    s.fx("godrays", cx=(wx0 + wx1) / 2, cy=(wy0 + wy1) / 2, strength=.5, thresh=.85, decay=.975, radius=300, region=(wy0, 1000))
    px, py = cam.scr(base + np.array([150, 300, 140]))
    peacock_feather(s, px - 70, py + 120, px + 170, py - 300, w=92, seed=3)
    s.motes(70, 300, 1200, 150, 860, color="#fff0c8", seed=5, size=(.8, 2.0), glow=3)
    s.fx("mottle", amp=.035, cell=60)
    s.look = {"vignette": .38}
    return s


# ---------- marks of devotion
def peepal(base, L, Wd, mat, direction=(0, 0, -1), seed=1, curl=.0):
    base = np.asarray(base, float)
    d = _unit(np.asarray(direction, float))[0]
    sd = _unit(np.cross(d, [0, 1, 0]))[0]

    def wfun(u):
        body = np.sin(np.pi * np.clip(u / .84, 0, 1)) ** .62 * (1 - .18 * u)
        tip = .09 * np.clip((1 - u) / .3, 0, 1) ** 1.2 * (u > .6)
        return Wd * np.maximum(body, tip)

    def pos(u, v):
        wv = v * 2 - 1
        w = wfun(u)
        along = u * L - .16 * L * np.abs(wv) ** 1.6 * np.clip(1 - u / .32, 0, 1) ** 1.3
        lift = curl * (np.abs(wv) * w) ** 2 / Wd + 3 * np.sin(np.pi * u) + 6 * u ** 4
        return base + d * along[:, None] + sd * (wv * w)[:, None] + np.array([0, 1.0, 0]) * lift[:, None]
    return sheet(pos, mat)


def mark_mat(base, kind, d, sd, L):
    """Peepal leaf material with one of the three sacred marks painted on it."""
    lm = leaf_mat(dark="#2a5a18", light="#6aa83a", vein="#c8e098", seed=11, gloss=.75, spacing=.075)
    base = np.asarray(base, float)

    def col(g):
        c = lm.color(g)
        rel = g["P"] - base
        a = rel @ d
        x = rel @ sd
        rng_n = fbm(a * .08, x * .08, 3, 3)
        if kind == "namam":
            arm = np.where(a > 92, np.abs(np.abs(x) - 20), np.abs(np.hypot(x, a - 92) - 20))
            arm = np.where((a > 92) & (a > 190), 99, arm)
            white = _sm(6.5, 4.5, arm)
            red = _sm(4.2, 2.6, np.abs(x)) * _sm(98, 104, a) * _sm(192, 186, a)
            c = c * (1 - white[:, None]) + C("#fbf8f0") * white[:, None]
            c = c * (1 - red[:, None]) + C("#d81a1a") * red[:, None]
        elif kind == "tripundra":
            ash = np.zeros_like(a)
            for yy in (118, 140, 162):
                ash = np.maximum(ash, _sm(5.5, 3.5, np.abs(a - yy)) * _sm(58, 52, np.abs(x)))
            ash = ash * (.75 + .3 * rng_n)
            dot = _sm(8.5, 6.5, np.hypot(x, a - 140))
            c = c * (1 - ash[:, None]) + C("#e8e4dc") * ash[:, None]
            c = c * (1 - dot[:, None]) + C("#c8102a") * dot[:, None]
        else:
            ring = _sm(22, 20, np.hypot(x, a - 140)) * .9
            dot = _sm(15, 13, np.hypot(x, a - 140))
            c = c * (1 - ring[:, None]) + C("#f0c868") * ring[:, None]
            c = c * (1 - dot[:, None]) + C("#c40e26") * (.9 + .15 * rng_n)[:, None] * dot[:, None]
        return c
    return Mat(color=col, rough=.35, ks=.45, wrap=.4, kr=.15, sheen=.2, sheen_col="#e8ffd0")


@scene
def tilak(s):
    hz = 380
    warm_room(s, hz, light=(1150, 300), warm="#4a2410", glow_x=1150, floor_top="#2a1a14", floor_glow="#ff9a50")
    bokeh_lamps(s, ((200, 14, 6, .3),), gap=0, seed=2)
    s.bokeh(6, 0, 1600, 20, 440, colors=("#ff8a2a", "#ffb43a"), r=(26, 60), a=(.06, .14), blur=5, seed=6, ring=True)
    # polished black stone
    s.add(f'<rect y="{hz}" width="1600" height="{1000 - hz}" fill="{s.lin([(0, "#1c1412", 1), (1, "#070504", 1)], 0, hz, 0, 1000, user=True)}"/>')
    s.add(f'<rect y="{hz}" width="1600" height="{1000 - hz}" fill="{s.rad([(0, "#ff9a50", .25), (1, "#ff9a50", 0)], 1100, hz + 30, 700, user=True, transform=f"translate(0 {(hz + 30) * .7:.0f}) scale(1 .3)")}" style="mix-blend-mode:screen"/>')
    cam = Cam(elev=44, x0=800, y0=600, dist=3400)
    surfs = []
    d_, tip = diya3d(cam.at(1260, 430), .8, spout=-.6)
    surfs += d_
    surfs += katori(cam.at(540, 470), 1.45, fill=powder("#ead2a0", 3, rough=.55), fill_h=30, fill_dome=8)
    surfs += katori(cam.at(800, 450), 1.45, fill=powder("#c8102a", 2), fill_h=30, fill_dome=16)
    surfs += katori(cam.at(1060, 470), 1.45, fill=powder("#dcd8d0", 5), fill_h=30, fill_dome=14)
    d = np.array([0, 0, -1.0])
    sd = _unit(np.cross(d, [0, 1, 0]))[0]
    for k, (x, kind, dx) in enumerate(((500, "namam", -.12), (800, "tripundra", 0), (1100, "bindi", .12))):
        b = cam.at(x, 915 if k != 1 else 930, 1)
        dd = _unit(np.array([dx, 0, -1.0]))[0]
        sdd = _unit(np.cross(dd, [0, 1, 0]))[0]
        surfs.append(peepal(b, 330, 118, mark_mat(b, kind, dd, sdd, 330), direction=dd, seed=k, curl=.0))
    rig = Rig([Light(tip + np.array([0, 60, 0]), "#ffc070", 1.5, 650, shadow=.55, size=30),
               Light(direction=(-.3, .75, .35), color="#fff0dc", power=.55)],
              sky="#4a3020", ground="#140a06", amb=.7,
              env=[(-1, "#0a0604"), (0, "#4a2a18"), (.35, "#c88a50"), (.7, "#3a2418"), (1, "#140c08")])
    stage(s, surfs, cam, rig, ss=3, shadow=dict(floor=0, ao=.6, ao_h=12, ao_blur=5), reflect=dict(floor=0, k=.35, fade=70, blur=1.5))
    flame_at(s, cam, tip, 70, glow_r=360, glow_a=.5)
    s.add("".join(ob.marigold(x, y, r, c, k) for k, (x, y, r, c) in enumerate(
        [(300, 640, 26, "#f39a1c"), (1330, 720, 26, "#f7c02a"), (1372, 748, 22, "#e8562a"), (250, 680, 20, "#f7c02a")])))
    ob.petals_scatter(s, 260, 1340, 560, 990, 22, seed=3, size=(5, 9))
    s.fx("mottle", amp=.035, cell=50)
    return s


# ---------- the scales of dharma
@scene
def scales(s):
    hz = 640
    s.sky([(0, "#141a44"), (.25, "#2e2c66"), (.45, "#6a4a86"), (.56, "#b8668a"), (.62, "#ee8e78"), (.66, "#ffb88a"), (.7, "#ffd8a8")])
    s.stars(70, 0, 300, seed=11, bright=.7)
    s.moon(300, 150, 16, glow_r=150)
    s.fx("clouds", y0=200, y1=520, seed=61, cell=110, aniso=4.5, cover=.36, soft=.18, lit="#ffb898", body=.75, direct=.85,
         light=(0, 1), sun=(800, 640, 380), opacity=.85)
    s.glow(800, 650, 700, "#ffb070", .45, .18, sy=.4)
    arch.nagara(s, 1290, hz + 4, 1.25, color="#3a2440", rim="#ffbf98", light=-1, door="#ffb45c")
    arch.nagara(s, 330, hz + 4, .8, color="#43294a", rim="#ffbf98", light=1, door="#ffb45c")
    arch.deepastambha(s, 120, hz + 40, 1.1, color="#2a1a30", rim="#ffbf98")
    arch.deepastambha(s, 1520, hz + 40, 1.0, color="#2a1a30", rim="#ffbf98")
    s.add(f'<rect y="{hz}" width="1600" height="{1000 - hz}" fill="{s.lin([(0, "#6a4a5e", 1), (.35, "#3a2636", 1), (1, "#140c14", 1)], 0, hz, 0, 1000, user=True)}"/>')
    lines = "".join(f"M0 {f(hz + (1000 - hz) * (k / 9) ** 1.8)}H1600" for k in range(1, 10))
    lines += "".join(f"M{f(800 + (x - 800) * .25)} {hz}L{f(x)} 1000" for x in range(-1600, 3300, 260))
    s.add(f'<path d="{lines}" stroke="#000" stroke-opacity=".25" stroke-width="2"/>')
    s.fx("reflect", y0=hz, strength=.45, tint="#1a0f1e", tint_near=.6, tint_far=.2, amp=1.2, blur=2.5)
    cam = Cam(elev=13, x0=800, y0=940, dist=3600)
    b = cam.at(800, 915)
    m = Mat(**BRASS_M, tex=band_tex([(30, 1.4, .4), (150, 1.4, .35), (300, 1.4, .35), (410, 1.4, .35)]))
    stand = [(0, 0), (130, 0), (134, 8), (120, 16), (96, 26), (72, 40), (58, 52), (50, 62), (62, 72), (52, 80), (26, 92),
             (18, 110), (16, 150), (26, 158), (26, 166), (16, 174), (14, 300), (22, 308), (22, 316), (14, 324), (12, 420),
             (20, 430), (24, 440), (14, 452), (0, 454)]
    fin = [(0, 470), (12, 474), (16, 484), (12, 496), (18, 510), (14, 524), (6, 536), (0, 544)]
    surfs = [lathe(stand, m, at=b), lathe(fin, m, at=b)]
    span = 350
    beam = [b + np.array([x, 452 + 8 * (abs(x) / span) ** 3, 0]) for x in np.linspace(-span, span, 9)]
    surfs.append(tube(beam, lambda t: 8 - 3 * np.abs(t - .5), m, cap=True))
    surfs.append(lathe([(0, -12), (16, -10), (20, 0), (16, 10), (0, 12)], m, at=b + np.array([0, 456, 0]), M=rot("x", 90)))
    lamp_tip = None
    for sx in (-1, 1):
        top = b + np.array([sx * span, 462, 0])
        surfs.append(ellipsoid(top + np.array([0, 4, 0]), 9, m))
        surfs.append(lathe([(0, 0), (6, 2), (4, 10), (8, 20), (0, 28)], m, at=top + np.array([0, 8, 0])))
        pc = b + np.array([sx * span, 170, 0])
        pan = [(0, 0), (50, 0), (88, 10), (112, 26), (116, 32), (110, 32), (88, 18), (0, 8)]
        surfs.append(lathe(pan, m, at=pc))
        for a in (0, 2 * math.pi / 3, 4 * math.pi / 3):
            rim = pc + np.array([112 * math.sin(a + .5), 32, 112 * math.cos(a + .5)])
            surfs.append(tube([top + np.array([0, -4, 0]), rim], 1.6, Mat(**dict(BRASS_M, rough=.45)), cap=False,
                              ))
        if sx < 0:
            d_, lamp_tip = diya3d(pc + np.array([0, 8, 0]), .66, spout=.6)
            surfs += d_
        else:
            lotus_at = pc + np.array([0, 10, 0])
    rig = Rig([Light(direction=(0, .25, -.9), color="#ffb890", power=1.0),
               Light(lamp_tip + np.array([0, 40, 0]), "#ffc070", 1.6, 420),
               Light(direction=(-.2, .6, .7), color="#a888b8", power=.55)],
              sky="#6a4a78", ground="#2a1820", amb=.6,
              env=[(-1, "#1a0f1e"), (-.1, "#5a3a50"), (0, "#ffb890"), (.15, "#c8708a"), (.5, "#4a3a7a"), (1, "#1a1a44")])
    stage(s, surfs, cam, rig, ss=3, shadow=dict(floor=0, ao=.5, ao_h=26, ao_blur=8), reflect=dict(floor=0, k=.3, fade=260, blur=2.5))
    flame_at(s, cam, lamp_tip, 64, glow_r=320, glow_a=.55)
    lx, ly = cam.scr(lotus_at)
    s.add(f'<path d="M{f(lx - 60)} {f(ly - 4)}Q{f(lx)} {f(ly + 14)} {f(lx + 60)} {f(ly - 4)}" stroke="#2c5a3a" stroke-width="10" fill="none"/>')
    ob.lotus(s, lx, ly - 2, .58, seed=4, lit=.8)
    s.motes(40, 300, 1300, 200, 800, seed=4, size=(.8, 2.0))
    s.fx("mottle", amp=.04, cell=60)
    return s


# ---------- the palm-leaf manuscript
def palm_leaf(c, L, Wd, R, seed=1, bend=6, ruled=True):
    """One loose palm leaf: a long, faintly bent strip with string holes and ruled lines."""
    c = np.asarray(c, float)

    def pos(u, v):
        x = (u - .5) * L
        z = (v - .5) * Wd
        y = bend * np.sin(np.pi * u) + 2 * np.sin(np.pi * v) - 1
        return np.stack([x, y, z], -1) @ R.T + c

    def col(g):
        u, v = g["u"], g["v"]
        cc = C("#e4c084") * (.84 + .2 * fbm(u * 30, v * 4, 3, seed))[:, None]
        rule = ruled & (np.abs(np.sin(v * np.pi * 5)) < .07) & (u > .06) & (u < .94)
        cc = np.where(rule[:, None] if ruled else (u < 0)[:, None], cc * .8, cc)
        hole = np.hypot((np.abs(u - .5) - .22) * L, (v - .5) * Wd) < 4.5
        edge = _sm(.0, .06, np.minimum(u, 1 - u)) * _sm(0, .12, np.minimum(v, 1 - v))
        cc = cc * (.75 + .25 * edge)[:, None]
        return np.where(hole[:, None], C("#2a160a"), cc)
    return sheet(pos, Mat(color=col, rough=.55, ks=.25, wrap=.35, kr=.1))


@scene
def manuscript(s):
    hz = 470
    warm_room(s, hz, light=(380, 300), warm="#5a2810", glow_x=380, floor_top="#3a1e10")
    bokeh_lamps(s, ((200, 12, 6, .25),), gap=0, seed=9)
    s.bokeh(6, 600, 1600, 20, 420, colors=("#ff8a2a", "#ffb43a"), r=(26, 70), a=(.05, .12), blur=5, seed=3, ring=True)
    cam = Cam(elev=38, x0=800, y0=700, dist=3400)
    lamp_at = cam.at(300, 520)
    sm, tips = samai(lamp_at, .95, wicks=1)
    surfs = list(sm)
    c = cam.at(830, 640)
    R = rot("y", -6)

    def wood(g):
        q = g["q"]
        n = fbm(q[:, 0] * .02, q[:, 2] * .2 + q[:, 1] * .2, 4, 3)
        grain = .5 + .5 * np.sin(q[:, 0] * .08 + n * 9)
        cc = C("#5a1e10") * (1 - grain[:, None] * .4) + C("#8a3a1a") * (grain[:, None] * .4)
        top = g["face"] == (1, 1)
        bx = np.minimum(330 - np.abs(q[:, 0]), 52 - np.abs(q[:, 2]))
        band = top & (bx > 6) & (bx < 17)
        dots = top & (bx > 9) & (bx < 14) & (np.sin(q[:, 0] * .5) > .55)
        lotus = top & (np.hypot(q[:, 0] / 1.6, q[:, 2]) < 26) & (np.cos(np.arctan2(q[:, 2], q[:, 0] / 1.6) * 8) > -.2) & (np.hypot(q[:, 0] / 1.6, q[:, 2]) > 8)
        cc = np.where(band[:, None], C("#d0922e"), cc)
        cc = np.where(dots[:, None], C("#2a6a3a"), cc)
        cc = np.where(lotus[:, None], C("#d0922e"), cc)
        return cc
    wm = Mat(color=wood, rough=.3, ks=.55, wrap=.2, kr=.25)

    def leaves(g):
        q = g["q"]
        side = np.full(len(q), g["face"][0] != 1)
        st = .55 + .45 * np.abs(np.sin(q[:, 1] * 1.9))
        base = C("#e0b670") * (.85 + .2 * fbm(q[:, 0] * .01, q[:, 1] * .3, 3, 7))[:, None]
        return np.where(side[:, None], base * st[:, None], base)
    lm = Mat(color=leaves, rough=.6, ks=.2, wrap=.4, kr=.1)
    surfs += rbox(c + R @ np.array([0, 11, 0]), (340, 11, 54), 4, wm, M=R)
    surfs += rbox(c + R @ np.array([0, 46, 0]), (328, 25, 48), 2, lm, M=R)
    surfs += rbox(c + R @ np.array([0, 82, 0]), (340, 11, 54), 4, wm, M=R)
    cord = Mat(color=lambda g: np.where((np.sin(g["s"] * .8 + g["ang"] * 2) > 0)[:, None], C("#b8241a"), C("#7a120e")), rough=.7, ks=.15, wrap=.4)
    for x in (-150, 150):
        loop = [c + R @ np.array([x + 2 * math.sin(a), 47 + 52 * math.sin(a), 63 * math.cos(a)]) for a in np.linspace(0, 2 * np.pi, 41)]
        surfs.append(tube(loop, 3, cord, cap=False))
    tail = [c + R @ np.array([150, 99, 20]), c + R @ np.array([190, 92, 60]), c + R @ np.array([230, 40, 110]),
            c + R @ np.array([260, 3, 150]), c + R @ np.array([330, 3, 190]), c + R @ np.array([400, 3, 170])]
    surfs.append(tube(tail, 3, cord))
    surfs.append(ellipsoid(tail[-1] + np.array([10, 5, 0]), (10, 9, 10), Mat(**BRASS_M)))
    # three loose leaves fanned in front, and the stylus resting on them
    for k, (dx, dz, ang) in enumerate(((-40, 170, 4), (-10, 205, 9), (30, 240, 14))):
        surfs.append(palm_leaf(c + np.array([dx, 3 + k * 2.5, dz]), 600, 50, rot("y", ang), seed=k))
    a0, a1 = c + np.array([-260, 12, 330]), c + np.array([260, 14, 250])
    iron = Mat(color="#8a8680", metal=1, rough=.3, ks=1.0, env_k=1.1, lobe=.6, kd_metal=.35, spec_tint=.2)
    mid = a0 + (a1 - a0) * .6
    surfs.append(tube([a0, mid], lambda t: 5 * np.clip(t * 5, 0, 1) ** .7 + .4, iron, cap=True))
    surfs.append(tube([mid, a1], lambda t: 8 - 2.5 * t, Mat(**BRASS_M, tex=band_tex([(14, 3, .5), (50, 3, .5), (120, 3, .5)]))))
    rig = Rig([Light(tips[0] + np.array([0, 50, 0]), "#ffc47a", 2.3, 900, shadow=.6, size=26),
               Light(direction=(.3, .5, .8), color="#ffb880", power=.45),
               Light(direction=(.6, .4, -.6), color="#4a3a5a", power=.3)],
              sky="#3a2414", ground="#140804", amb=.75)
    stage(s, surfs, cam, rig, ss=3, shadow=dict(floor=0, ao=.6, ao_h=14, ao_blur=5), reflect=dict(floor=0, k=.2, fade=80, blur=2))
    flame_at(s, cam, tips[0], 66, glow_r=400, glow_a=.55)
    s.glow(300, 260, 480, "#ff8a3a", .25, .2)
    ob.petals_scatter(s, 260, 1360, 860, 990, 16, seed=8, size=(5, 9))
    s.add(ob.marigold(1250, 560, 24, "#f39a1c", 3) + ob.marigold(1290, 582, 19, "#f7c02a", 4))
    s.motes(26, 150, 800, 100, 460, seed=5, size=(.8, 1.8))
    s.fx("mottle", amp=.035, cell=50)
    return s


# ---------- reading by lamplight
def page_half(spine, right, up, out, W_, H_, lift, sign, mat, stack=8):
    """One half of an open book: a page surface curving up from the gutter."""
    def pos(u, v):
        t = u
        z = lift * (np.sqrt(t) * (1 - .45 * t)) + stack
        return spine + right * (sign * t * W_)[:, None] + up * ((v - .5) * H_)[:, None] + out * z[:, None]
    return Surf(pos, mat, None, two_sided=True, extra=lambda u, v: {"pu": u, "pv": v})


def page_mat(seed=1):
    def col(g):
        u, v = g["pu"], g["pv"]
        c = C("#f2e6c8") * (.92 + .08 * fbm(u * 6, v * 8, 3, seed))[:, None]
        rows = (np.abs(np.sin(v * np.pi * 34)) > .55) & (u > .12) & (u < .88) & (v > .1) & (v < .9)
        broken = vnoise(u * 40, v * 34 * 2, seed) > .35
        ink = rows & broken
        c = np.where(ink[:, None], c * .78, c)
        edge = _sm(.0, .12, u)
        return c * (.75 + .25 * edge)[:, None]
    return Mat(color=col, rough=.8, ks=.05, wrap=.45, kr=.03)


@scene
def lamp_book(s):
    hz = 600
    s.add(f'<rect width="1600" height="1000" fill="{s.lin([(0, "#1a1020", 1), (.6, "#24141a", 1), (1, "#0e0806", 1)], 0, 0, 0, 1000, user=True)}"/>')
    s.add(f'<rect width="1600" height="1000" fill="{s.rad([(0, "#7a3a14", .9), (.45, "#3a1a0c", .5), (1, "#000", 0)], 520, 470, 900, user=True)}"/>')
    # an arched window with the full moon
    wx, wy, ww, wh = 1130, 120, 300, 420
    win = f"M{wx} {wy + wh}V{wy + ww / 2}A{ww / 2} {ww / 2} 0 0 1 {wx + ww} {wy + ww / 2}V{wy + wh}Z"
    s.add(f'<path d="{win}" fill="none" stroke="#1a0e0a" stroke-width="44"/>')
    s.add(f'<g clip-path="{s.clip(win)}"><rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="{s.lin([(0, "#0c1640", 1), (.6, "#1e3070", 1), (1, "#3a4a8a", 1)], 0, wy, 0, wy + wh, user=True)}"/>')
    s.stars(40, wy, wy + wh, seed=4, bright=.8, x0=wx, x1=wx + ww)
    s.moon(wx + 190, wy + 120, 38, glow_r=230)
    s.add(f'<path d="M{wx} {wy + wh - 40}Q{wx + 80} {wy + wh - 90} {wx + 160} {wy + wh - 60}T{wx + ww} {wy + wh - 70}V{wy + wh}H{wx}Z" fill="#0a0e20"/>')
    s.add('</g>')
    s.add(f'<path d="M{wx + ww / 2} {wy}V{wy + wh}M{wx} {wy + wh * .55}H{wx + ww}" stroke="#1a0e0a" stroke-width="10"/>')
    s.add(f'<rect x="{wx - 40}" y="{wy + wh + 18}" width="{ww + 80}" height="22" fill="#2a160e"/>')
    # moonlight on the floor
    s.add(f'<rect y="{hz}" width="1600" height="{1000 - hz}" fill="{s.lin([(0, "#2a1810", 1), (1, "#0c0604", 1)], 0, hz, 0, 1000, user=True)}"/>')
    s.add(f'<path d="M1120 {hz + 20}L1440 {hz + 20}L1300 1000L760 1000Z" fill="#8aa0e0" opacity=".12" filter="{s.blur(24)}" style="mix-blend-mode:screen"/>')
    s.add(f'<rect y="{hz}" width="1600" height="{1000 - hz}" fill="{s.rad([(0, "#ff9a50", .35), (1, "#ff9a50", 0)], 470, hz + 60, 700, user=True, transform=f"translate(0 {(hz + 60) * .7:.0f}) scale(1 .3)")}" style="mix-blend-mode:screen"/>')
    s.add(f'<path d="M0 {hz}H1600" stroke="#ffb070" stroke-opacity=".15" stroke-width="2"/>')
    cam = Cam(elev=20, x0=800, y0=760, dist=3600)
    lamp_at = cam.at(450, 700)
    sm, tips = samai(lamp_at, 1.15, wicks=5)
    c = cam.at(860, 800)
    # the rehal: two carved boards crossing in an X
    def wood(g):
        q = g["q"]
        n = fbm(q[:, 0] * .01, q[:, 1] * .05 + q[:, 2] * .05, 4, 3)
        gr = .5 + .5 * np.sin(q[:, 1] * .09 + n * 8)
        return C("#6a3418") * (.75 + .35 * gr)[:, None]
    wm = Mat(color=wood, rough=.4, ks=.35, wrap=.25, kr=.18)
    surfs = list(sm)
    Rb = rot("x", -38)
    surfs += rbox(c + np.array([0, 130, -40]), (230, 150, 7), 4, wm, M=Rb)
    surfs += rbox(c + np.array([0, 22, 50]), (232, 8, 26), 3, wm)
    surfs += rbox(c + np.array([0, 38, 70]), (232, 10, 5), 2, wm)
    for sx in (-1, 1):
        surfs += rbox(c + np.array([sx * 220, 60, -60]), (8, 60, 100), 3, wm, M=rot("x", 0))
    # the open book resting in the V
    tilt = math.radians(52)
    spine0 = c + np.array([0, 130, -40]) + Rb @ np.array([0, 0, 9])
    up = np.array([0, math.sin(tilt), -math.cos(tilt)])
    out = np.array([0, math.cos(tilt), math.sin(tilt)])
    right = np.array([1.0, 0, 0])
    spine = spine0 + out * 8
    pm = page_mat(2)
    for sgn in (-1, 1):
        surfs.append(page_half(spine, right, up, out, 200, 270, 34, sgn, pm, stack=10))
        surfs += rbox(spine + right * sgn * 100 + out * 4, (100, 136, 5), 3, Mat(color="#e8dcc0", rough=.8, ks=.05, wrap=.4), M=np.stack([right, up, out], 1))
    cover = Mat(color="#7a1418", rough=.5, ks=.3, wrap=.3, kr=.15)
    surfs += rbox(spine + out * -2, (212, 142, 3), 2, cover, M=np.stack([right, up, out], 1))
    rig = Rig([Light(np.mean(tips, 0) + np.array([0, 60, 0]), "#ffc47a", 2.4, 800, shadow=.6, size=40),
               Light(direction=(.7, .35, -.6), color="#8aa0e8", power=.55)],
              sky="#2a1a20", ground="#140804", amb=.75,
              env=[(-1, "#140a06"), (-.1, "#4a2a18"), (.1, "#b0703a"), (.4, "#2a2440"), (1, "#141430")])
    stage(s, surfs, cam, rig, ss=3, shadow=dict(floor=0, ao=.6, ao_h=18, ao_blur=6), reflect=dict(floor=0, k=.18, fade=90, blur=2.5))
    for t in tips:
        flame_at(s, cam, t, 50, glow_r=280, glow_a=.45)
    s.glow(450, 300, 520, "#ff8a3a", .22, .2)
    s.add(ob.marigold(1080, 900, 26, "#f39a1c", 1) + ob.marigold(1122, 918, 21, "#f7c02a", 2))
    ob.petals_scatter(s, 600, 1200, 860, 980, 12, seed=4, size=(5, 9))
    s.motes(30, 250, 800, 140, 560, seed=6, size=(.8, 1.8))
    s.fx("mottle", amp=.035, cell=50)
    return s


# ---------- Rama's sandals on the throne
def paduka(at, sc=1.0, heading=0.0, mat=None, mirror=False):
    """A wooden sandal with a toe-knob, covered in gold. Sole points along +Z (toe towards the viewer)."""
    m = mat or Mat(**GOLD_M, tex=lambda g: 1 - .35 * np.exp(-((g["d"] - g["R"] + 9) / 1.6) ** 2))
    at = np.asarray(at, float)
    Rm = rot("y", heading)
    T, q = 20.0, 7.0
    mx = -1 if mirror else 1

    def Rad(a):
        # footprint outline radius in direction a (0 = toe, +Z)
        z = np.cos(a)
        x = np.sin(a) * mx
        rr = 52 + 70 * np.abs(z) ** 2.2 - 8 * np.exp(-((np.abs(a) - 1.4) / .35) ** 2)
        rr = rr + 10 * np.clip(z, 0, 1) ** 3 + 6 * x * np.clip(z, 0, 1)
        return rr

    def geo(u, v):
        a = 2 * np.pi * v
        R = Rad(a)
        d = np.where(u < .7, u / .7 * (R - q), 0)
        y = np.full_like(u, T)
        e = (u >= .7) & (u < .85)
        th = (u - .7) / .15 * np.pi / 2
        d = np.where(e, R - q + q * np.sin(th), d)
        y = np.where(e, T - q + q * np.cos(th), y)
        sd = u >= .85
        d = np.where(sd, R, d)
        y = np.where(sd, (T - q) * (1 - (u - .85) / .15), y)
        return a, R, d, y

    def pos(u, v):
        a, R, d, y = geo(u, v)
        L = np.stack([np.sin(a) * d * mx, y, np.cos(a) * d + 10], -1) * sc
        return L @ Rm.T + at

    def extra(u, v):
        a, R, d, y = geo(u, v)
        return {"d": d, "R": R}
    out = [Surf(pos, m, None, orient=mx, fd=True, extra=extra)]
    knob = [(0, 0), (6, 0), (5, 16), (4, 30), (10, 38), (12, 44), (8, 50), (0, 53)]
    out.append(lathe(knob, Mat(**GOLD_M), at=at + Rm @ (np.array([8 * mx, T, 110]) * sc), scale=sc))
    return out


@scene
def sandals(s):
    hz = 760
    s.add('<rect width="1600" height="1000" fill="#120604"/>')
    s.add(f'<rect width="1600" height="1000" fill="{s.rad([(0, "#6a2a10", 1), (.5, "#2a0e06", 1), (1, "#0a0302", 1)], 800, 420, 950, user=True)}"/>')
    bokeh_lamps(s, ((240, 16, 6, .35), (130, 12, 9, .22)), gap=330, seed=12)
    # the royal parasol
    s.add(f'<path d="M800 40V330" stroke="#c8902e" stroke-width="10"/>')
    can = "M520 160C580 60 700 20 800 20C900 20 1020 60 1080 160Q1050 172 1020 162Q990 176 960 164Q930 178 900 166Q870 180 840 168Q820 182 800 168Q780 182 760 168Q730 180 700 166Q670 178 640 164Q610 176 580 162Q550 172 520 160Z"
    s.add(f'<path d="{can}" fill="{s.lin([(0, "#fffaf0", 1), (.7, "#f0e2c8", 1), (1, "#c8b090", 1)], 0, 0, 1, 0)}"/>')
    s.add(f'<path d="{can}" fill="{s.lin([(0, "#000", 0), (.6, "#000", .05), (1, "#000", .35)], 0, 0, 0, 1)}"/>')
    s.add(f'<path d="M520 160Q800 120 1080 160" stroke="#e8b04a" stroke-width="8" fill="none" filter="{s.gold_filter(3)}"/>')
    s.add("".join(f'<path d="M{x} {154 + 10 * (1 - ((x - 800) / 280) ** 2) * -1 + 8}v{22 + (k % 2) * 8}" stroke="#e8b04a" stroke-width="3"/><circle cx="{x}" cy="{154 + 10 * (1 - ((x - 800) / 280) ** 2) * -1 + 34 + (k % 2) * 8}" r="4" fill="#ffd27a"/>'
                  for k, x in enumerate(range(530, 1080, 22))))
    s.add('<circle cx="800" cy="16" r="12" fill="#e8b04a"/>')
    # throne back: a carved golden arch around red velvet
    back = "M560 640V360C560 250 660 196 800 180C940 196 1040 250 1040 360V640Z"
    inner = "M610 640V380C610 290 690 246 800 234C910 246 990 290 990 380V640Z"
    s.add(f'<path d="{back}" fill="#000" opacity=".6" filter="{s.blur(14)}" transform="translate(0 10)"/>')
    s.add(f'<path d="{back}" fill="{s.lin([(0, "#ffe6a0", 1), (.4, "#d89a3a", 1), (1, "#7a4a12", 1)], 0, 0, 1, 1)}" filter="{s.gold_filter(5, "#fff4d6", 235, 40)}"/>')
    s.add(f'<path d="{back}" fill="none" stroke="#5a3008" stroke-width="3" stroke-dasharray="2 10"/>')
    s.add(f'<path d="{inner}" fill="{s.rad([(0, "#c8203a", 1), (.6, "#7a0c1e", 1), (1, "#3a040c", 1)], 800, 380, 320, user=True)}"/>')
    s.add(f'<path d="{inner}" fill="#000" filter="{s.grain(.9, 2, .15, 3, "#000000")}" opacity=".5"/>')
    s.add(f'<g clip-path="{s.clip(inner)}"><path d="{inner}" fill="none" stroke="#000" stroke-opacity=".6" stroke-width="40" filter="{s.blur(14)}"/></g>')
    rays = "".join(f'<path d="M{f(800 + math.cos(a - .05) * 62)} {f(410 + math.sin(a - .05) * 62)}L{f(800 + math.cos(a) * (112 if k % 2 else 92))} {f(410 + math.sin(a) * (112 if k % 2 else 92))}L{f(800 + math.cos(a + .05) * 62)} {f(410 + math.sin(a + .05) * 62)}Z"/>'
                   for k, a in enumerate(np.linspace(0, 2 * np.pi, 24, endpoint=False)))
    s.add(f'<g fill="#e8b04a" opacity=".9" filter="{s.gold_filter(3)}">{rays}<circle cx="800" cy="410" r="56"/></g>')
    s.add(f'<circle cx="800" cy="410" r="40" fill="none" stroke="#8a5a14" stroke-width="3" opacity=".6"/>')
    s.add(f'<path d="M760 560V520Q800 490 840 520V560Z" fill="#e8b04a" opacity=".0"/>')
    # seat and its front panel
    seat = "M500 640H1100L1080 700H520Z"
    s.add(f'<path d="{seat}" fill="{s.lin([(0, "#ffe6a0", 1), (.5, "#c8862a", 1), (1, "#6a3a0a", 1)], 0, 0, 0, 1)}" filter="{s.gold_filter(4, "#fff4d6", 235, 40)}"/>')
    s.add(f'<path d="M520 700H1080V840H520Z" fill="{s.lin([(0, "#8a1424", 1), (1, "#3a0610", 1)], 0, 0, 0, 1)}"/>')
    s.add(f'<path d="M520 700H1080V840H520Z" fill="none" stroke="#e8b04a" stroke-width="14" filter="{s.gold_filter(3)}"/>')
    s.add("".join(f'<circle cx="{x}" cy="770" r="16" fill="none" stroke="#e8b04a" stroke-width="5" filter="{s.gold_filter(2)}"/><circle cx="{x}" cy="770" r="5" fill="#ffd27a"/>' for x in range(580, 1060, 80)))
    for x in (520, 1080):
        s.add(f'<path d="M{x - 30} 840h60l-10 80h-40Z" fill="#d89a3a" filter="{s.gold_filter(4)}"/>')
    s.add(f'<rect y="{hz + 160}" width="1600" height="100" fill="#0a0403"/>')
    garl = s.mark()
    ob.garland(s, 570, 330, 1030, 330, 150, r=17, seed=7, tassel=True)
    cam = Cam(elev=16, x0=800, y0=650, dist=3600)
    surfs = []
    cush = cam.at(800, 655)
    surfs += rbox(cush + np.array([0, 16, -10]), (230, 16, 70), 14, silk_mat("#b0182a", "#4a0410", seed=6, sheen=.6), M=None)
    for f_ in surfs:
        f_.extra = (lambda e: (lambda u, v: dict(e(u, v), X=(e(u, v)["q"][:, 0]), Z=e(u, v)["q"][:, 2])))(f_.extra)
    surfs += paduka(cush + np.array([-92, 30, -46]), 1.18, heading=-5, mirror=True)
    surfs += paduka(cush + np.array([92, 30, -46]), 1.18, heading=5)
    lamps = []
    for x in (330, 1270):
        sm, tips = samai(cam.at(x, 900), 1.0)
        surfs += sm
        lamps += tips
    rig = Rig([Light(cam.at(800, 600) + np.array([0, 520, 520]), "#ffe2b0", 1.7, 1200, shadow=.5, size=60)] +
              [Light(np.mean(lamps[:5], 0) + np.array([0, 60, 0]), "#ffb060", 1.2, 700),
               Light(np.mean(lamps[5:], 0) + np.array([0, 60, 0]), "#ffb060", 1.2, 700)],
              sky="#4a2a18", ground="#1a0806", amb=.7)
    stage(s, surfs, cam, rig, ss=3, shadow=dict(floor=cam.at(800, 655)[1] + 32, ao=.5, ao_h=10, ao_blur=4))
    for t in lamps:
        flame_at(s, cam, t, 46, glow_r=240, glow_a=.45)
    ob.petals_scatter(s, 200, 1400, 905, 990, 30, seed=11, size=(5, 9))
    s.motes(40, 400, 1200, 60, 600, seed=8, size=(.8, 2))
    s.fx("mottle", amp=.035, cell=50)
    return s


# ---------- the game of dice
def pasa(c, sc, heading, counts=(1, 2, 5, 6), roll=0, seed=1):
    """A long four-sided ivory die marked with ring-and-dot pips."""
    R = rot("y", heading) @ rot("x", roll)
    hx, hy = 62 * sc, 14 * sc
    faces = {(1, 1): counts[0], (2, 1): counts[1], (1, -1): counts[3], (2, -1): counts[2]}

    def col(g):
        q = g["q"]
        n = fbm(q[:, 0] * .04, q[:, 1] * .2 + q[:, 2] * .2, 3, seed)
        c_ = C("#efe2c4") * (.88 + .14 * n)[:, None]
        k = faces.get(g["face"], 0)
        if k:
            ax = g["face"][0]
            other = 2 if ax == 1 else 1
            xs = (np.arange(k) - (k - 1) / 2) * (hx * 1.5 / max(k, 2))
            dmin = np.full(len(q), 1e9)
            for x0 in xs:
                dmin = np.minimum(dmin, np.hypot(q[:, 0] - x0, q[:, other]))
            ring = _sm(1.2 * sc, .4 * sc, np.abs(dmin - 6 * sc))
            dot = _sm(2.6 * sc, 1.8 * sc, dmin)
            c_ = c_ * (1 - .7 * np.maximum(ring, dot))[:, None] + C("#3a1a0a") * (.7 * np.maximum(ring, dot))[:, None]
        return c_
    m = Mat(color=col, rough=.35, ks=.5, wrap=.35, kr=.2, sheen=.2, sheen_col="#fff4e0")
    return rbox(np.asarray(c, float) + np.array([0, hy, 0]), (hx, hy, hy), 4 * sc, m, M=R)


def board_svg(s, cam, cx, cz, sq=46, y=1):
    """A cross-shaped chaupar cloth seen through the camera, with its squares embroidered in gold."""
    def P(x, z):
        return cam.scr((cx + x, y, cz + z))
    out_cloth, out_lines, out_x = [], [], []
    arms = []
    for ang in range(4):
        for i in range(3):
            for j in range(8):
                x0, z0 = (i - 1.5) * sq, 1.5 * sq + j * sq
                arms.append((ang, x0, z0))
    def rotp(ang, x, z):
        for _ in range(ang):
            x, z = -z, x
        return x, z
    cloth_d = []
    for ang in range(4):
        pts = [rotp(ang, x, z) for x, z in ((-1.5 * sq, 1.5 * sq), (1.5 * sq, 1.5 * sq), (1.5 * sq, 9.5 * sq), (-1.5 * sq, 9.5 * sq))]
        cloth_d.append("M" + "L".join(f"{f(a)} {f(b)}" for a, b in (P(*p) for p in pts)) + "Z")
    ctr = [P(*p) for p in ((-1.5 * sq, -1.5 * sq), (1.5 * sq, -1.5 * sq), (1.5 * sq, 1.5 * sq), (-1.5 * sq, 1.5 * sq))]
    cloth_d.append("M" + "L".join(f"{f(a)} {f(b)}" for a, b in ctr) + "Z")
    for ang, x0, z0 in arms:
        pts = [rotp(ang, x, z) for x, z in ((x0, z0), (x0 + sq, z0), (x0 + sq, z0 + sq), (x0, z0 + sq))]
        sp = [P(*p) for p in pts]
        out_lines.append("M" + "L".join(f"{f(a)} {f(b)}" for a, b in sp) + "Z")
        j = int(round((z0 - 1.5 * sq) / sq))
        i = int(round(x0 / sq + 1.5))
        if (j == 3 and i in (0, 2)) or (j == 7 and i == 1):
            out_x.append(f"M{f(sp[0][0])} {f(sp[0][1])}L{f(sp[2][0])} {f(sp[2][1])}M{f(sp[1][0])} {f(sp[1][1])}L{f(sp[3][0])} {f(sp[3][1])}")
    d = "".join(cloth_d)
    s.add(f'<path d="{d}" fill="#000" opacity=".55" filter="{s.blur(8)}" transform="translate(6 8)"/>')
    s.add(f'<path d="{d}" fill="{s.rad([(0, "#a8162a", 1), (.6, "#6a0a18", 1), (1, "#2a0408", 1)], *cam.scr((cx + 160, 0, cz - 60)), 700, user=True)}"/>')
    s.add(f'<path d="{d}" fill="#000" filter="{s.grain(.7, 2, .2, 5, "#000000")}" opacity=".5"/>')
    s.add(f'<path d="{"".join(out_lines)}" fill="none" stroke="#e8b04a" stroke-width="2.2" stroke-opacity=".75"/>')
    s.add(f'<path d="{"".join(out_x)}" fill="none" stroke="#e8b04a" stroke-width="2.6" stroke-opacity=".8"/>')
    s.add(f'<path d="{d}" fill="none" stroke="#e8b04a" stroke-width="5"/>')
    c0 = P(0, 0)
    s.add(f'<ellipse cx="{f(c0[0])}" cy="{f(c0[1])}" rx="{f(sq * 1.1)}" ry="{f(sq * 1.1 * cam.se)}" fill="none" stroke="#e8b04a" stroke-width="3"/>')


@scene
def dice(s):
    hz = 470
    s.add('<rect width="1600" height="1000" fill="#0a0504"/>')
    s.add(f'<rect width="1600" height="1000" fill="{s.rad([(0, "#5a2410", 1), (.5, "#22100a", 1), (1, "#070303", 1)], 1150, 440, 1000, user=True)}"/>')
    # columns of a palace hall, lit from the one lamp
    for x, w in ((140, 90), (430, 70), (1430, 100)):
        s.add(f'<rect x="{x - w / 2}" y="0" width="{w}" height="{hz + 10}" fill="{s.lin([(0, "#1a0c08", 1), (.6, "#3a1c10", 1), (1, "#120806", 1)], 0, 0, 1, 0)}"/>')
        s.add(f'<rect x="{x - w / 2 - 14}" y="{hz - 24}" width="{w + 28}" height="34" fill="#2a140c"/>')
    s.add(f'<path d="M0 0H1600V60Q1400 140 1200 70Q1000 150 800 70Q600 150 400 70Q200 140 0 60Z" fill="#3a0a12" opacity=".8"/>')
    s.add(f'<rect y="{hz}" width="1600" height="{1000 - hz}" fill="{s.lin([(0, "#2a160e", 1), (1, "#080403", 1)], 0, hz, 0, 1000, user=True)}"/>')
    s.add(f'<rect y="{hz}" width="1600" height="{1000 - hz}" fill="{s.rad([(0, "#ff9a50", .3), (1, "#ff9a50", 0)], 1150, hz + 80, 800, user=True, transform=f"translate(0 {(hz + 80) * .6:.0f}) scale(1 .4)")}" style="mix-blend-mode:screen"/>')
    cam = Cam(elev=40, x0=800, y0=640, dist=3400)
    c = cam.at(760, 660)
    board_svg(s, cam, c[0], c[2], sq=44)
    lamp_at = cam.at(1240, 520)
    sm, tips = samai(lamp_at, 1.0, wicks=1)
    surfs = list(sm)
    surfs += pasa(c + np.array([-40, 0, 130]), 1.45, 18, seed=1)
    surfs += pasa(c + np.array([140, 0, 190]), 1.45, -24, roll=90, counts=(3, 4, 1, 6), seed=2)
    surfs += pasa(c + np.array([30, 0, 290]), 1.45, 70, roll=180, seed=3)
    for k, (x, z, colr) in enumerate(((-90, -40, "#b8141a"), (-60, 10, "#b8141a"), (90, -60, "#1a6a2a"), (40, -110, "#d8a020"), (130, 20, "#1a1a1a"))):
        piece = [(0, 0), (16, 0), (18, 4), (14, 10), (10, 24), (7, 34), (9, 38), (5, 44), (0, 46)]
        surfs.append(lathe(piece, Mat(color=colr, rough=.25, ks=.7, wrap=.2, kr=.3), at=c + np.array([x, 1, z]), scale=1.1))
    rig = Rig([Light(tips[0] + np.array([0, 40, 0]), "#ffc070", 2.6, 900, shadow=.8, size=10),
               Light(direction=(-.5, .5, .6), color="#3a2a4a", power=.3)],
              sky="#2a160c", ground="#0a0403", amb=.6)
    stage(s, surfs, cam, rig, ss=3, shadow=dict(floor=0, ao=.6, ao_h=10, ao_blur=4))
    flame_at(s, cam, tips[0], 62, glow_r=420, glow_a=.55)
    s.glow(1240, 300, 560, "#ff8a3a", .22, .2)
    s.motes(20, 900, 1500, 100, 480, seed=3, size=(.8, 1.6))
    s.fx("mottle", amp=.035, cell=50)
    s.look = {"vignette": .45, "contrast": 1.1}
    return s


# ---------- Rama's bow
@scene
def bow(s):
    hz = 640
    sun = (800, 640)
    s.sky([(0, "#1a2050"), (.2, "#34397a"), (.4, "#7a5a92"), (.52, "#d87a7a"), (.6, "#ffaa6e"), (.66, "#ffd48e"), (.7, "#fff0c8")])
    s.stars(30, 0, 180, seed=21, bright=.5)
    s.sun(*sun, 44, halo_r=700, halo_a=.9)
    s.fx("clouds", y0=40, y1=320, seed=71, cell=160, aniso=3.5, cover=.42, soft=.16, lit="#ffbc94", body=.72, direct=.8,
         light=(0, 1), sun=(sun[0], sun[1], 420), opacity=.92)
    s.fx("clouds", y0=320, y1=580, seed=72, cell=90, aniso=5, cover=.33, soft=.2, lit="#ffdcae", body=.85, direct=.95,
         light=(0, 1), sun=(sun[0], sun[1], 340), opacity=.85)
    far = peak_line(hz, [(-20, 120, 200), (300, 190, 240), (620, 90, 200), (1000, 110, 220), (1300, 200, 260), (1640, 130, 200)], 31, shape=1.2, floor=30)
    mountains(s, far, "#8a6a9a", "#b88aa8", lit="#ffb8a0", lit_a=.6, light=1, seed=5, rim="#ffe2c0", rim_center=sun, rim_r=500,
              haze="#ffc8b0", haze_a=.5, haze_h=120, base_y=hz + 20)
    s.mist(hz, 90, "#ffd0b0", .5, 24)
    near = ridgeline(hz + 70, 50, 33, cell=260, octaves=5, ridged=.3)
    hills(s, near, "#4a3460", "#2a1c3a", rim="#ffd0a8", rim_a=.8, rim_center=sun, rim_r=700, haze="#c890a8", haze_a=.3)
    s.mist(hz + 80, 70, "#e8b0b0", .35, 20)
    # stone terrace in front
    s.add(f'<rect y="790" width="1600" height="210" fill="{s.lin([(0, "#3a2a3a", 1), (.1, "#2a1e2c", 1), (1, "#0e0a10", 1)], 0, 790, 0, 1000, user=True)}"/>')
    s.add('<path d="M0 790H1600" stroke="#ffc8a0" stroke-opacity=".7" stroke-width="3"/>')
    s.add(f'<path d="M0 806H1600" stroke="#000" stroke-opacity=".4" stroke-width="2"/>')
    s.fx("godrays", cx=sun[0], cy=sun[1], strength=.4, thresh=.72, decay=.972, radius=300)
    cam = Cam(elev=8, x0=800, y0=870, dist=3600)
    base = cam.at(800, 860)
    gm = Mat(**GOLD_M)

    def bow_col(g):
        s_ = g["s"]
        L = 1180.0
        mid = np.abs(s_ - L / 2)
        c_ = np.broadcast_to(C("#f2c25a"), (len(s_), 3)).copy()
        bands = np.zeros_like(s_)
        for k in range(1, 9):
            bands = np.maximum(bands, np.exp(-((mid - 70 - k * 58) / 2.2) ** 2))
        c_ = c_ * (1 - .45 * bands[:, None])
        wrap_ = (mid < 62)
        stripe = .5 + .5 * np.sign(np.sin(s_ * .5 + g["ang"] * 1.0))
        red = C("#9a1020") * (.7 + .3 * stripe)[:, None]
        return np.where(wrap_[:, None], red, c_)

    def bow_metal(g):
        return 1
    half = [(0, 0), (130, -6), (270, -30), (380, -66), (460, -108), (510, -146), (530, -176), (548, -194), (574, -196), (594, -186)]
    pts = [(-x, y) for x, y in half[::-1]] + half[1:]
    lift = 420
    path = [base + np.array([x, lift + y, 0]) for x, y in pts]
    rad = lambda t: 22 - 13 * np.abs(t - .5) * 2 + 4 * np.exp(-((t - .5) / .05) ** 2)
    bow_m = Mat(color=bow_col, metal=1, rough=.24, ks=1.2, env_k=1.3, lobe=.75, kd_metal=.35)
    surfs = [tube(path, rad, bow_m, cap=True)]
    bc = _cr(np.array(path), 2.0)
    bu, bL = _arclen(bc)
    for k in range(1, 9):
        for sgn in (-1, 1):
            t = .5 + sgn * (70 + k * 58) / bL
            p = np.array([np.interp(t, bu, bc[:, j]) for j in range(3)])
            rr = float(rad(np.array([t]))[0])
            surfs.append(ellipsoid(p, (rr * .55, rr * 1.12, rr * 1.12), gm, M=align_y(np.gradient(bc, axis=0)[min(len(bc) - 1, int(t * len(bc)))]) @ rot("z", 90)))
    for sx in (-1, 1):
        tip = base + np.array([sx * 594, lift - 186, 0])
        surfs.append(ellipsoid(tip, (10, 10, 10), gm))
        surfs.append(lathe([(0, 0), (8, 4), (5, 14), (9, 24), (0, 34)], gm, at=tip + np.array([0, 4, 0]), M=rot("z", -sx * 30)))
    # the carved stand: two forked posts on a plinth
    wood = Mat(**dict(GOLD_M, color="#c8862a", rough=.35))
    post = [(0, 0), (40, 0), (44, 8), (34, 16), (24, 24), (18, 40), (14, 200), (22, 210), (22, 218), (14, 226), (12, 300), (18, 306), (0, 308)]
    for sx in (-1, 1):
        pb = base + np.array([sx * 300, 0, 0])
        surfs.append(lathe(post, wood, at=pb, scale=1.0))
        for k in (-1, 1):
            surfs.append(tube([pb + np.array([0, 300, 0]), pb + np.array([k * 6, 330, k * 14]), pb + np.array([k * 6, 360, k * 30])], 5, wood))
    surfs += rbox(base + np.array([0, -10, 0]), (420, 10, 70), 4, Mat(color=lambda g: C("#4a3448") * (.8 + .3 * fbm(g["q"][:, 0] * .01, g["q"][:, 2] * .03, 3, 2))[:, None], rough=.6, ks=.15, wrap=.3))
    rig = Rig([Light(direction=(0, .12, -1), color="#ffc890", power=1.4),
               Light(direction=(-.3, .6, .75), color="#c8a0c0", power=.7, shadow=.5, size=50)],
              sky="#9a7aa0", ground="#3a2434", amb=.6,
              env=[(-1, "#1a1018"), (-.1, "#5a3a50"), (0, "#ffd0a0"), (.12, "#ff9a7a"), (.4, "#8a5a8a"), (1, "#2a2a5a")])
    stage(s, surfs, cam, rig, ss=3, shadow=dict(floor=0, ao=.5, ao_h=14, ao_blur=6))
    l, r = cam.scr(base + np.array([-594, lift - 186, 0])), cam.scr(base + np.array([594, lift - 186, 0]))
    s.add(f'<path d="M{f(l[0])} {f(l[1])}L{f(r[0])} {f(r[1])}" stroke="#fff0d0" stroke-width="2.2" stroke-opacity=".9"/>')
    s.add(f'<path d="M{f(l[0])} {f(l[1])}L{f(r[0])} {f(r[1])}" stroke="#ffd890" stroke-width="7" stroke-opacity=".25" filter="{s.blur(3)}"/>')
    gx, gy = cam.scr(base + np.array([0, lift - 60, 0]))
    s.glow(gx, gy, 520, "#ffd890", .22, .2, sy=.45)
    s.birds(7, 1000, 1300, 330, 420, color="#3a2238", s=(5, 10), seed=8, a=.8)
    s.motes(30, 300, 1300, 300, 760, seed=9, color="#ffe0a8")
    s.fx("mottle", amp=.04, cell=60)
    return s


# ---------- Hanuman's mace and the mountain of herbs
def flying_mountain(s, cx, cy, sc=1.0, seed=5):
    rng = random.Random(seed)
    # a trail of light where it has passed
    trail = f"M{f(cx - 40 * sc)} {f(cy + 20 * sc)}Q{f(cx - 500 * sc)} {f(cy + 40 * sc)} {f(cx - 1100 * sc)} {f(cy - 60 * sc)}"
    s.add(f'<path d="{trail}" stroke="#bff0a0" stroke-width="{f(70 * sc)}" stroke-opacity=".1" fill="none" filter="{s.blur(30)}" style="mix-blend-mode:screen"/>')
    s.add(f'<path d="{trail}" stroke="#fff4c0" stroke-width="{f(5 * sc)}" stroke-opacity=".3" fill="none" filter="{s.blur(5)}" style="mix-blend-mode:screen"/>')
    s.glow(cx, cy - 10 * sc, 320 * sc, "#9af08a", .35, .2)
    top = [(-150, 10), (-120, -30), (-90, -40), (-60, -90), (-30, -120), (0, -150), (25, -115), (50, -100), (80, -70), (110, -60), (150, 0)]
    bottom = [(150, 0), (120, 40), (80, 60), (50, 110), (20, 140), (0, 190), (-25, 150), (-60, 110), (-100, 70), (-130, 40)]
    pts = [(cx + x * sc, cy + y * sc) for x, y in top + bottom]
    d = "M" + "L".join(f"{f(x)} {f(y)}" for x, y in pts) + "Z"
    s.add(f'<path d="{d}" fill="{s.lin([(0, "#3a4a3a", 1), (.5, "#22281e", 1), (1, "#0e100c", 1)], 0, 0, 0, 1)}"/>')
    s.add(f'<path d="{d}" fill="#000" filter="{s.grain(.03, 4, .3, 4, "#000000")}" opacity=".6"/>')
    tp = "M" + "L".join(f"{f(cx + x * sc)} {f(cy + y * sc)}" for x, y in top)
    s.add(f'<path d="{tp}" stroke="#d8ffb0" stroke-width="{f(2.5 * sc)}" fill="none" opacity=".8"/>')
    from land import crown
    trees = "".join(crown(cx + x * sc, cy + y * sc - rng.uniform(8, 18) * sc, rng.uniform(9, 16) * sc, seed=k) for k, (x, y) in enumerate(top[1:-1]))
    s.add(f'<path d="{trees}" fill="#1a2a1a"/>')
    s.motes(70, cx - 140 * sc, cx + 140 * sc, cy - 160 * sc, cy + 60 * sc, color="#a8ff90", seed=seed, size=(1, 3), glow=5)
    s.motes(30, cx - 700 * sc, cx - 60 * sc, cy - 60 * sc, cy + 60 * sc, color="#d8ffb0", seed=seed + 1, size=(.6, 1.6), glow=4)


@scene
def mace(s):
    s.sky([(0, "#060a20"), (.4, "#0e1a40"), (.75, "#1e2c5a"), (1, "#2a3060")])
    s.stars(260, 0, 700, seed=31, bright=1.0)
    s.add(f'<rect width="1600" height="1000" fill="{s.lin([(0, "#8a9aff", 0), (.5, "#8a9aff", .08), (1, "#8a9aff", 0)], 0, 0, 1, 1)}" style="mix-blend-mode:screen"/>')
    s.moon(260, 150, 34, glow_r=260)
    s.fx("clouds", y0=480, y1=760, seed=81, cell=110, aniso=5, cover=.32, soft=.2, lit="#8a9ad0", body=.7, direct=.7,
         light=(-.5, -1), opacity=.7)
    flying_mountain(s, 1290, 190, .78)
    far = ridgeline(760, 60, 41, cell=300, octaves=5, ridged=.5)
    hills(s, far, "#1a2448", "#121a34", rim="#8aa0e0", rim_a=.5, rim_center=(260, 150), rim_r=900)
    s.mist(770, 80, "#4a5a90", .4, 20)
    rock = "M-20 1010V880C80 860 180 820 300 800C420 780 520 790 640 760C720 744 820 750 900 790C1000 830 1140 850 1300 870C1440 886 1540 900 1620 910V1010Z"
    s.add(f'<path d="{rock}" fill="{s.lin([(0, "#1e2236", 1), (1, "#06070c", 1)], 0, 750, 0, 1000, user=True)}"/>')
    s.add(f'<path d="{rock}" fill="#000" filter="{s.grain(.02, 4, .35, 3, "#000000")}" opacity=".6"/>')
    s.add('<path d="M-20 880C80 860 180 820 300 800C420 780 520 790 640 760C720 744 820 750 900 790C1000 830 1140 850 1300 870C1440 886 1540 900 1620 910" stroke="#a8b8f0" stroke-opacity=".5" stroke-width="2.4" fill="none"/>')
    boulder = "M700 905L712 760L752 640L800 572L880 520L990 500L1080 528L1150 600L1196 720L1210 905Z"
    s.add(f'<path d="{boulder}" fill="#000" opacity=".5" filter="{s.blur(16)}" transform="translate(-10 10)"/>')
    s.add(f'<path d="{boulder}" fill="{s.lin([(0, "#2e3654", 1), (.6, "#141a2c", 1), (1, "#080a12", 1)], 0, 0, 1, 1)}"/>')
    s.add('<path d="M712 760L752 640L800 572L880 520L900 600L850 700L790 790Z" fill="#3a4466" opacity=".7"/>'
          '<path d="M880 520L990 500L1080 528L1010 590L900 600Z" fill="#3a4a5a" opacity=".55"/>'
          '<path d="M1080 528L1150 600L1196 720L1110 700L1010 590Z" fill="#101626" opacity=".6"/>')
    s.add(f'<path d="{boulder}" fill="#000" filter="{s.grain(.03, 4, .4, 6, "#000000")}" opacity=".55"/>')
    s.add('<path d="M712 760L752 640L800 572L880 520L990 500" stroke="#b8c8ff" stroke-opacity=".55" stroke-width="2.4" fill="none"/>'
          '<path d="M990 500L1080 528L1150 600L1196 720" stroke="#c8ffb0" stroke-opacity=".5" stroke-width="2.4" fill="none"/>'
          '<path d="M850 700L900 600M1010 590L1110 700" stroke="#000" stroke-opacity=".35" stroke-width="2"/>')
    cam = Cam(elev=12, x0=800, y0=900, dist=3600)
    gm = Mat(**GOLD_M, tex=band_tex([(0, 1, 0)]))
    base = cam.at(560, 915, 0)
    ax = _unit(np.array([.36, 1, .3]))[0]
    M = align_y(ax)

    def ribs(u, phi, y):
        return 1 + .07 * np.abs(np.cos(phi * 6)) ** .6 * _sm(10, 40, y) * (1 - _sm(150, 185, y))
    head = [(0, 0), (40, 2), (78, 18), (104, 50), (114, 96), (104, 142), (78, 174), (44, 190), (30, 194), (34, 202), (24, 212),
            (16, 222), (22, 232), (12, 246), (5, 262), (0, 270)]
    hb = base + M @ np.array([0, 560, 0])
    surfs = [lathe(head, Mat(**GOLD_M, tex=band_tex([(96, 2.5, .5), (60, 1.5, .35), (132, 1.5, .35), (8, 2, .4)])), at=hb, M=M, mod=ribs)]
    shaft = [(0, -560), (26, -556), (30, -546), (22, -536), (16, -520), (18, -380), (24, -372), (24, -362), (18, -354), (16, -200),
             (24, -192), (24, -182), (18, -174), (18, -40), (28, -30), (34, -14), (28, 0), (0, 4)]
    surfs.append(lathe(shaft, Mat(**GOLD_M, tex=band_tex([(-450, 3, .4), (-300, 3, .4), (-100, 3, .4)])), at=hb, M=M))
    rig = Rig([Light(direction=(.7, .55, -.2), color="#d8ffb0", power=.6),
               Light(direction=(-.75, .5, -.3), color="#c8d0ff", power=1.0, shadow=.5, size=40),
               Light(direction=(.2, .4, .9), color="#ffd8a0", power=.75)],
              sky="#3a4a7a", ground="#0a0c18", amb=.55,
              env=[(-1, "#05060c"), (-.1, "#2a2030"), (0, "#8a7a90"), (.3, "#4a4a7a"), (.7, "#c8d0a0"), (1, "#2a2a48")])
    stage(s, surfs, cam, rig, ss=3, shadow=dict(floor=0, ao=.55, ao_h=20, ao_blur=8))
    s.motes(26, 500, 1100, 300, 800, color="#c8ffb0", seed=12, size=(.6, 1.6))
    s.fx("mottle", amp=.04, cell=60)
    s.look = {"vibrance": .1}
    return s


# ---------- rites of childhood
def torus(c, R, r, mat, M=None, mod=None):
    t = np.linspace(0, 2 * np.pi, 64)
    prof = np.stack([R + r * np.cos(t + np.pi), r * np.sin(t + np.pi)], -1)
    return lathe(prof, mat, at=c, M=M, smooth=False, mod=mod)


def banana_leaf(base, direction, length, width, seed=1, droop=.0):
    """A long banana leaf with its pale midrib and fine parallel veins, laid nearly flat."""
    def col(g):
        u, v = g["u"], g["v"]
        wv = v * 2 - 1
        n = fbm(u * 4, v * 2.5, 4, seed)
        c = C("#123a10") * (1 - n[:, None]) + C("#3e8226") * n[:, None]
        vein = .5 + .5 * np.sin((u * length + np.abs(wv) * width * .45) * .42)
        c = c * (.86 + .2 * vein ** 3)[:, None]
        mid = np.exp(-(wv * width / 9) ** 2)
        c = c * (1 - mid[:, None]) + C("#b8cc78") * mid[:, None]
        edge = _sm(.85, 1, np.abs(wv))
        return c * (1 - .25 * edge[:, None])
    m = Mat(color=col, rough=.3, ks=.4, wrap=.3, kr=.18, sheen=.06, sheen_col="#e8ffd0", amb=.8)
    return leaf(base, direction, length, width, m, droop=droop, fold=.04, shape="banana", seed=seed)


@scene
def earrings(s):
    cam = Cam(elev=58, x0=800, y0=520, dist=3000)
    s.add('<rect width="1600" height="1000" fill="#3a2414"/>')

    def planks(g):
        X, Z = g["X"], g["Z"]
        n = fbm(X * .0015, Z * .03, 4, 3)
        gr = .5 + .5 * np.sin(Z * .09 + n * 10)
        seam = _sm(2.5, .5, np.abs(((Z + 40) % 170) - 85) - 83)
        tone = .85 + .2 * vnoise(np.floor((Z + 40) / 170), 0 * X, 5)
        return C("#7a4a2a") * ((.78 + .22 * gr) * tone * (1 - .5 * seam))[:, None]
    stone = Mat(color=planks, rough=.4, ks=.3, wrap=.3, kr=.2)
    key = Light(direction=(-.55, .7, -.45), color="#ffeed4", power=.95, shadow=.55, size=40)
    rig = Rig([key, Light(direction=(.6, .4, .6), color="#ffd0a0", power=.3)], sky="#a89a98", ground="#6a5040", amb=.45,
              env=[(-1, "#4a3020"), (0, "#a08868"), (.35, "#fff2dc"), (.7, "#b8a898"), (1, "#8a8090")])
    stage(s, [cloth(-600, 2200, -1500, 900, lambda X, Z: 0 * X, stone)], cam, rig, ss=1)
    c = cam.at(800, 540)
    plate = [(0, 0), (330, 0), (348, 6), (362, 18), (368, 26), (364, 30), (354, 24), (334, 10), (0, 8)]
    surfs = [lathe(plate, Mat(**BRASS_M, tex=band_tex([(18, 1.2, .4)])), at=c + np.array([0, 0, 20])),
             banana_round(c + np.array([0, 0, 20]), 320, 9, seed=3)]
    gold = Mat(**GOLD_M)
    e1 = c + np.array([-90, 18, 20])
    e2 = c + np.array([90, 18, 50])
    surfs.append(torus(e1, 74, 10, gold, M=rot("x", 6)))
    surfs.append(torus(e2, 74, 10, gold, M=rot("z", 10) @ rot("x", -8)))
    for e, a in ((e1, 1.2), (e2, 2.0)):
        p = e + np.array([74 * math.cos(a), 4, 74 * math.sin(a)])
        surfs.append(ellipsoid(p, 13, gold))
        surfs.append(ellipsoid(p + np.array([0, 10, 0]), 6.5, Mat(color="#c81830", rough=.08, ks=1.4, kr=.5)))
    surfs += katori(cam.at(640, 340, 10), 1.25, fill=powder("#e8a010", 4, rough=.5), fill_h=20, fill_dome=8)
    root = Mat(color=lambda g: C("#b06a2a") * (.8 + .3 * fbm(g["s"] * .05, g["ang"], 3, 5))[:, None], rough=.7, ks=.12, wrap=.3,
               bump=lambda u, v: 3 * np.sin(u * 40) ** 8, bump_k=.5)
    r0 = cam.at(860, 700, 14)
    surfs.append(tube([r0, r0 + np.array([80, 2, 26]), r0 + np.array([170, 4, 8]), r0 + np.array([240, 2, 50])], lambda t: 22 - 6 * t, root))
    surfs.append(tube([r0 + np.array([80, 2, 26]), r0 + np.array([120, 2, 90]), r0 + np.array([128, 2, 140])], lambda t: 14 - 5 * t, root))
    surfs.append(tube([r0 + np.array([170, 4, 8]), r0 + np.array([210, 3, -50])], lambda t: 12 - 4 * t, root))
    d_, tip = diya3d(cam.at(1250, 300, 2), .9, spout=-.5)
    surfs += d_
    stage(s, surfs, cam, rig, ss=3, shadow=dict(floor=0, ao=.5, ao_h=8, ao_blur=4))
    raster(s, lambda img: dof(img, 560, k=.014, max_sd=9))
    flame_at(s, cam, tip, 72, glow_r=260, glow_a=.4)
    fl = [(560, 600, 32, "#f39a1c"), (606, 640, 26, "#f7c02a"), (1010, 420, 30, "#f39a1c"), (968, 452, 24, "#e8562a"), (300, 860, 34, "#f7c02a"), (1330, 760, 30, "#e8562a")]
    s.add(f'<g filter="{s.blur(4)}" opacity=".35" transform="translate(10 12)">' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#1a2a10"/>' for x, y, r, c_ in fl) + '</g>')
    s.add("".join(ob.marigold(x, y, r, c_, k, light=(.6, .7)) for k, (x, y, r, c_) in enumerate(fl)))
    s.add(f'<rect width="1600" height="1000" fill="{s.rad([(0, "#fff0d0", .4), (1, "#fff0d0", 0)], 100, -100, 1200, user=True)}" style="mix-blend-mode:screen"/>')
    s.fx("mottle", amp=.025, cell=60)
    s.look = {"vignette": .36, "contrast": 1.05}
    return s


def glass_mat(color, glow=.5, flecks=False, seed=1):
    base = C(color)

    def col(g):
        c = np.broadcast_to(base, (len(g["u"]), 3)).copy()
        if flecks:
            fl = _sm(.75, .8, vnoise(g["u"] * 60, g["v"] * 300, seed))
            c = c * (1 - fl[:, None]) + C("#ffd27a") * fl[:, None]
        return c

    def emit(g):
        nd = np.clip((g["N"] * g["V"]).sum(1), 0, 1)
        return base[None, :] * (glow * (.25 + .9 * (1 - nd) ** 2))[:, None]
    return Mat(color=col, rough=.06, ks=1.6, kr=.55, wrap=.2, emit=emit, amb=.6)


@scene
def bangles(s):
    hz = 560
    warm_room(s, hz, light=(420, 360), warm="#5a2410", glow_x=420)
    bokeh_lamps(s, ((240, 16, 7, .4), (330, 12, 11, .25)), gap=0, seed=21)
    s.bokeh(8, 0, 1600, 20, 520, colors=("#ff8a2a", "#ffb43a", "#ff4a6a", "#4aff8a"), r=(24, 64), a=(.06, .16), blur=5, seed=18, ring=True)
    cam = Cam(elev=28, x0=800, y0=740, dist=3000)
    silk = silk_mat("#a01428", "#3a040c", seed=7, sheen=.5)
    lamp_at = cam.at(400, 640)
    d_, tip = diya3d(lamp_at, .9, spout=.5)
    rig = Rig([Light(tip + np.array([0, 50, 0]), "#ffc070", 2.2, 700, shadow=.55, size=24),
               Light(direction=(.5, .5, .6), color="#ffd0b0", power=.4)],
              sky="#3a2016", ground="#140806", amb=.75,
              env=[(-1, "#1a0806"), (-.1, "#5a2a14"), (.1, "#ffb070"), (.35, "#4a2010"), (1, "#100604")])
    stage(s, [cloth(-400, 2000, -2600, 600, folds(6, 6, 4, 420, dirn=.3), silk)], cam, rig, ss=1)
    c = cam.at(820, 760)
    surfs = list(d_)
    reds = [glass_mat("#e0182e", .95), glass_mat("#c00c22", .95, flecks=True, seed=2), glass_mat("#f0303e", .95)]
    greens = [glass_mat("#18b040", .9), glass_mat("#0a8a2e", .9, flecks=True, seed=3), glass_mat("#28c050", .9)]
    goldm = Mat(**GOLD_M)
    for k in range(9):
        m = reds[k % 3] if k % 4 != 3 else goldm
        surfs.append(torus(c + np.array([-140, 8 + k * 14, 0]), 82, 6.5, m, M=rot("z", 1.5 * math.sin(k))))
    for k in range(7):
        m = greens[k % 3] if k % 3 != 2 else goldm
        surfs.append(torus(c + np.array([140, 8 + k * 14, -40]), 82, 6.5, m, M=rot("x", 1.2 * math.sin(k))))
    surfs.append(torus(c + np.array([10, 74, 150]), 82, 6.5, reds[0], M=rot("x", 64) @ rot("z", 8)))
    surfs.append(torus(c + np.array([-270, 8, 190]), 82, 6.5, greens[1], M=rot("x", 4)))
    surfs.append(torus(c + np.array([-254, 22, 196]), 82, 6.5, reds[1], M=rot("x", -6)))
    # laddoos on a small brass plate
    pc = cam.at(1180, 820)
    surfs.append(lathe([(0, 0), (90, 0), (104, 8), (108, 12), (104, 13), (0, 6)], Mat(**BRASS_M), at=pc))
    lad = Mat(color=lambda g: C("#f0a020") * (.8 + .35 * vnoise(g["u"] * 40, g["v"] * 80, 7))[:, None], rough=.6, ks=.25, wrap=.4,
              bump=lambda u, v: 2.2 * vnoise(u * 40, v * 80, 7), bump_k=.6)
    for k, (dx, dz, dy) in enumerate(((-36, 10, 0), (34, 14, 0), (0, -30, 0), (0, 0, 46))):
        surfs.append(ellipsoid(pc + np.array([dx, 30 + dy, dz]), 30, lad))
    stage(s, surfs, cam, rig, ss=3, shadow=dict(floor=0, ao=.55, ao_h=10, ao_blur=5))
    raster(s, lambda img: dof(img, 700, k=.02, max_sd=8))
    flame_at(s, cam, tip, 76, glow_r=380, glow_a=.55)
    # a string of jasmine and some marigolds
    jas = []
    rng = random.Random(9)
    for k in range(40):
        t = k / 39
        x, y = 470 + 700 * t, 935 - 60 * math.sin(t * math.pi) + 10 * math.sin(t * 20)
        a = 40 + 60 * math.sin(t * 7)
        jas.append(f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="12" ry="6.5" transform="rotate({a:.0f} {f(x)} {f(y)})" fill="url(#jasB)"/>')
    s.defs.append('<radialGradient id="jasB" cx=".35" cy=".35" r=".7"><stop offset="0" stop-color="#ffffff"/><stop offset=".6" stop-color="#f6efe0"/><stop offset="1" stop-color="#b8a080"/></radialGradient>')
    s.add(f'<path d="M470 935Q820 860 1170 935" stroke="#3a6a2a" stroke-width="2" fill="none"/>' + "".join(jas))
    s.add("".join(ob.marigold(x, y, r, c_, k) for k, (x, y, r, c_) in enumerate(
        [(300, 860, 30, "#f39a1c"), (352, 890, 24, "#f7c02a"), (1380, 700, 26, "#e8562a")])))
    ob.petals_scatter(s, 260, 1400, 780, 990, 24, seed=7, size=(5, 9))
    s.motes(30, 300, 1300, 140, 560, seed=7, size=(.8, 1.8))
    s.fx("mottle", amp=.035, cell=50)
    s.look = {"bloom": 1.1}
    return s


@scene
def rice_bowl(s):
    cam = Cam(elev=50, x0=800, y0=540, dist=3000)
    s.add('<rect width="1600" height="1000" fill="#d8c8b0"/>')

    def planks(g):
        X, Z = g["X"], g["Z"]
        n = fbm(X * .0015, Z * .03, 4, 3)
        gr = .5 + .5 * np.sin(Z * .09 + n * 10)
        seam = _sm(2.5, .5, np.abs(((Z + 40) % 170) - 85) - 83)
        tone = .85 + .2 * vnoise(np.floor((Z + 40) / 170), 0 * X, 5)
        return C("#9a6a40") * ((.78 + .22 * gr) * tone * (1 - .5 * seam))[:, None]
    wood = Mat(color=planks, rough=.45, ks=.3, wrap=.3, kr=.2)
    key = Light(direction=(-.5, .75, -.45), color="#ffeed8", power=1.0, shadow=.5, size=50)
    rig = Rig([key, Light(direction=(.6, .4, .6), color="#ffd0a0", power=.3)], sky="#a8a0a0", ground="#5a4030", amb=.45,
              env=[(-1, "#2a1a10"), (-.2, "#5a4030"), (0, "#8a7058"), (.25, "#f8f0e4"), (.5, "#7a7880"), (1, "#3a3a44")])
    stage(s, [cloth(-600, 2200, -1500, 700, lambda X, Z: 0 * X, wood)], cam, rig, ss=1)
    c = cam.at(800, 610)
    surfs = [banana_round(c + np.array([0, 0, 30]), 380, 2, seed=6)]
    silver = Mat(**SILVER_M, tex=band_tex([(14, 1.4, .35), (60, 1.6, .4), (66, 1, .3), (92, 1.2, .3)]))
    bowl = [(0, 0), (52, 0), (58, 3), (54, 8), (70, 18), (98, 42), (118, 72), (126, 96), (128, 102), (124, 104), (118, 98),
            (110, 74), (92, 48), (64, 26), (0, 20)]
    b = c + np.array([-30, 4, 10])
    surfs.append(lathe(bowl, silver, at=b, scale=1.55))

    def kheer(g):
        rho = g["rho"]
        n = fbm(g["P"][:, 0] * .02, g["P"][:, 2] * .02, 4, 5)
        c_ = C("#ecd09a") * (.88 + .18 * n)[:, None]
        return c_ * (1 - .12 * _sm(150, 190, rho))[:, None]
    surfs.append(lathe([(0, 86), (126, 86), (0, 86.01)], Mat(color=kheer, rough=.3, ks=.4, wrap=.5, kr=.15,
                                                          bump=lambda u, v: 4 * fbm(u * 6, v * 20, 3, 2), bump_k=.4), at=b, scale=1.55, smooth=False))
    spoon_m = Mat(**SILVER_M)
    sp0 = c + np.array([290, 4, 150])
    Rs = rot("y", 35)
    surfs.append(lathe([(0, 0), (22, 1), (34, 6), (38, 12), (36, 14), (22, 9), (0, 8)], spoon_m, at=sp0, M=Rs @ np.diag([1, 1, 1.5])))
    hs = [sp0 + Rs @ np.array([0, 10, -52]), sp0 + Rs @ np.array([0, 18, -110]), sp0 + Rs @ np.array([0, 22, -230])]
    surfs.append(tube(hs, lambda t: 7 + 3 * t, spoon_m))
    surfs.append(ellipsoid(hs[-1] + Rs @ np.array([0, 0, -8]), (12, 6, 14), spoon_m))
    stage(s, surfs, cam, rig, ss=3, shadow=dict(floor=0, ao=.5, ao_h=10, ao_blur=5))
    raster(s, lambda img: dof(img, 560, k=.014, max_sd=9))
    # saffron strands, pistachio and almond slivers on the kheer
    kx, ky = cam.scr(b + np.array([0, 133, 0]))
    rng = random.Random(3)
    bits = []
    for _ in range(34):
        a, r = rng.uniform(0, 6.28), 150 * math.sqrt(rng.random())
        x, y = kx + math.cos(a) * r, ky + math.sin(a) * r * cam.se
        L = rng.uniform(8, 16)
        t = rng.uniform(0, 6.28)
        bits.append(f'<path d="M{f(x)} {f(y)}q{f(math.cos(t) * L * .5)} {f(math.sin(t) * L * .5 - 3)} {f(math.cos(t) * L)} {f(math.sin(t) * L)}" stroke="#d8401a" stroke-width="1.8" fill="none" stroke-linecap="round"/>')
    for k in range(22):
        a, r = rng.uniform(0, 6.28), 140 * math.sqrt(rng.random())
        x, y = kx + math.cos(a) * r, ky + math.sin(a) * r * cam.se
        colr = "#8ab83a" if k % 2 else "#f0e2c4"
        bits.append(f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="6" ry="2.6" transform="rotate({rng.uniform(0, 180):.0f} {f(x)} {f(y)})" fill="{colr}" stroke="#6a5a3a" stroke-opacity=".3"/>')
    s.add("".join(bits))
    fl = [(380, 420, 34, "#f39a1c"), (440, 452, 27, "#f7c02a"), (1200, 360, 32, "#e8562a"), (1246, 400, 25, "#f39a1c")]
    s.add(f'<g filter="{s.blur(4)}" opacity=".3" transform="translate(10 12)">' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#3a2a10"/>' for x, y, r, c_ in fl) + '</g>')
    s.add("".join(ob.marigold(x, y, r, c_, k, light=(.6, .7)) for k, (x, y, r, c_) in enumerate(fl)))
    ob.petals_scatter(s, 380, 1250, 700, 900, 18, colors=("#c91e3a", "#e8562a", "#f7c02a"), seed=2, size=(6, 11))
    s.add(f'<rect width="1600" height="1000" fill="{s.rad([(0, "#fff6e4", .5), (1, "#fff6e4", 0)], 120, -120, 1200, user=True)}" style="mix-blend-mode:screen"/>')
    s.fx("mottle", amp=.025, cell=60)
    s.look = {"vignette": .3, "contrast": 1.04}
    return s


def _om_polys(scale=1.0):
    """The Om outline as polygons in glyph units, centred on (0, 0)."""
    import re
    toks = re.findall(r"[MLQZ]|-?\d+\.?\d*", OM)
    polys, cur, i = [], [], 0
    pos = (0.0, 0.0)
    cmd = None
    while i < len(toks):
        t = toks[i]
        if t in "MLQZ":
            cmd = t
            i += 1
            if t == "Z":
                if cur:
                    polys.append(cur)
                cur = []
            continue
        if cmd == "M":
            if cur:
                polys.append(cur)
            pos = (float(toks[i]), float(toks[i + 1]))
            cur = [pos]
            i += 2
            cmd = "L"
        elif cmd == "L":
            pos = (float(toks[i]), float(toks[i + 1]))
            cur.append(pos)
            i += 2
        elif cmd == "Q":
            cx_, cy_, x, y = map(float, toks[i:i + 4])
            for k in range(1, 7):
                t_ = k / 6
                cur.append(((1 - t_) ** 2 * pos[0] + 2 * (1 - t_) * t_ * cx_ + t_ * t_ * x, (1 - t_) ** 2 * pos[1] + 2 * (1 - t_) * t_ * cy_ + t_ * t_ * y))
            pos = (x, y)
            i += 4
    if cur:
        polys.append(cur)
    return [[((x - 240) * scale, (y - 152) * scale) for x, y in p] for p in polys]


def rice_om_fx(img, cam, center, R, y_top, om_scale, seed=3, light=(-.55, -.65)):
    """A plate heaped with raw rice in which the Om has been traced with a finger:
    grains are stamped into a height field, the groove is pressed out, and the whole is lit."""
    from PIL import Image, ImageDraw
    Hh, Ww, _ = img.shape
    ss = 2
    cx, cy = cam.scr(center + np.array([0, y_top, 0]))
    rx, ry = R * 1.0, R * cam.se
    x0, x1 = int(cx - rx - 10), int(cx + rx + 10)
    y0, y1 = int(cy - ry - 10), int(cy + ry + 10)
    w, h = (x1 - x0) * ss, (y1 - y0) * ss
    # Om mask in screen space (traced on the rice plane)
    mask = Image.new("L", (w, h), 0)
    for poly in _om_polys(om_scale):
        pts = [cam.scr(center + np.array([px, y_top, py])) for px, py in poly]
        layer = Image.new("L", (w, h), 0)
        ImageDraw.Draw(layer).polygon([((px - x0) * ss, (py - y0) * ss) for px, py in pts], fill=255)
        mask = Image.fromarray(np.bitwise_xor(np.asarray(mask), np.asarray(layer)))
    m = np.asarray(mask, np.float32) / 255
    m = ndimage.gaussian_filter(m, 2.2 * ss)
    groove = _sm(.25, .7, m)
    ridge = np.clip(ndimage.gaussian_filter(m, 6 * ss) - m, 0, 1)
    # stamp grains
    rng = np.random.default_rng(seed)
    hgt = np.zeros((h, w), np.float32)
    tone = np.zeros((h, w), np.float32)
    k = 9 * ss
    yy, xx = np.mgrid[-k:k + 1, -k:k + 1].astype(np.float32)
    kernels = []
    for a in np.linspace(0, np.pi, 12, endpoint=False):
        u = (xx * np.cos(a) + yy * np.sin(a) * (1 / max(cam.se, .3))) / (4.0 * ss)
        v = (-xx * np.sin(a) + yy * np.cos(a) * (1 / max(cam.se, .3))) / (1.6 * ss)
        kernels.append(np.sqrt(np.clip(1 - u * u - v * v, 0, 1)))
    n = int(w * h / (ss * ss) / 9)
    px = rng.integers(k, w - k, n)
    py = rng.integers(k, h - k, n)
    ks = rng.integers(0, 12, n)
    lift = rng.uniform(0, .5, n).astype(np.float32)
    keep = groove[py, px] < rng.uniform(.2, 1, n)
    for x_, y_, kk, l_ in zip(px[keep], py[keep], ks[keep], lift[keep]):
        sl = (slice(y_ - k, y_ + k + 1), slice(x_ - k, x_ + k + 1))
        kv = kernels[kk] * 3 + l_
        np.maximum(hgt[sl], np.where(kernels[kk] > 0, kv, 0), out=hgt[sl])
        tone[sl] = np.where(kernels[kk] > 0, l_, tone[sl])
    yy2, xx2 = np.mgrid[0:h, 0:w].astype(np.float32)
    ell = ((xx2 / ss + x0 - cx) / rx) ** 2 + ((yy2 / ss + y0 - cy) / ry) ** 2
    inside = _sm(1.0, .96, ell)
    base_h = 6 * (1 - ell).clip(0, 1) ** .5
    H_ = hgt * (1 - groove * .95) + base_h + ridge * 8 - groove * 6
    gy, gx = np.gradient(H_)
    lx, ly = light
    nrm = 1 / np.sqrt(gx * gx + gy * gy + 1)
    lam = np.clip((-gx * lx - gy * ly + .8) * nrm, 0, 1.4)
    rice = np.array([.97, .93, .84], np.float32)
    col = rice[None, None, :] * (.45 + .55 * lam)[..., None] * (.9 + .15 * tone)[..., None]
    spec = np.clip((-gx * lx - gy * ly) * nrm, 0, 1) ** 8 * .5
    col = col + spec[..., None]
    occ = 1 - .5 * _sm(.0, .5, groove) * (hgt < .5)
    reg = img[y0:y1, x0:x1]
    up = np.repeat(np.repeat(reg, ss, 0), ss, 1)
    floor_vis = (hgt < .2) & (groove > .3)
    out = np.where(floor_vis[..., None], up * (.55 + .2 * lam[..., None]), col * occ[..., None])
    a = inside * (1 - floor_vis * 0)
    res = up * (1 - a[..., None]) + out * a[..., None]
    img[y0:y1, x0:x1] = res.reshape(h // ss, ss, w // ss, ss, 3).mean((1, 3))
    return img


@scene
def rice_om(s):
    hz = 330
    warm_room(s, hz, light=(1180, 300), warm="#5a2812", glow_x=1150, floor_top="#3a2214")
    bokeh_lamps(s, ((180, 14, 6, .3),), gap=0, seed=31)
    cam = Cam(elev=60, x0=800, y0=600, dist=3600)
    c = cam.at(780, 610)
    plate = [(0, 0), (300, 0), (318, 4), (332, 16), (340, 30), (336, 34), (326, 28), (304, 12), (0, 10)]
    surfs = [lathe(plate, Mat(**BRASS_M), at=c)]
    d_, tip = diya3d(cam.at(1260, 380), .8, spout=-.6)
    surfs += d_
    slate_c = cam.at(330, 560)
    frame = Mat(color=lambda g: C("#7a4a24") * (.8 + .3 * fbm(g["q"][:, 0] * .01, g["q"][:, 2] * .05, 3, 2))[:, None], rough=.5, ks=.25, wrap=.3)
    slate = Mat(color=lambda g: C("#2a2e30") * (.85 + .2 * fbm(g["q"][:, 0] * .02, g["q"][:, 2] * .02, 4, 5))[:, None], rough=.7, ks=.15, wrap=.2)
    R = rot("y", 14)
    surfs += rbox(slate_c + np.array([0, 6, 0]), (130, 6, 170), 3, frame, M=R)
    surfs += rbox(slate_c + np.array([0, 8, 0]), (112, 6, 150), 2, slate, M=R)
    surfs.append(tube([slate_c + R @ np.array([-60, 15, 120]), slate_c + R @ np.array([30, 15, 60])], 3.2, Mat(color="#e8e4dc", rough=.8, ks=.05, wrap=.4)))
    rig = Rig([Light(tip + np.array([0, 60, 0]), "#ffc070", 1.8, 800, shadow=.55, size=24),
               Light(direction=(-.4, .75, .4), color="#fff0dc", power=.55)],
              sky="#4a3020", ground="#140a06", amb=.7)
    stage(s, surfs, cam, rig, ss=3, shadow=dict(floor=0, ao=.55, ao_h=12, ao_blur=5))
    raster(s, lambda img: rice_om_fx(img, cam, c, 300, 18, 1.55))
    flame_at(s, cam, tip, 70, glow_r=380, glow_a=.5)
    s.add("".join(ob.marigold(x, y, r, c_, k) for k, (x, y, r, c_) in enumerate(
        [(1180, 780, 28, "#f39a1c"), (1228, 806, 22, "#f7c02a"), (300, 850, 24, "#e8562a")])))
    ob.petals_scatter(s, 260, 1340, 820, 990, 18, seed=3, size=(5, 9))
    s.fx("mottle", amp=.03, cell=50)
    return s


def homa_kunda(s, cx, cy, w, h, color="#7a3a22"):
    """A stepped square fire altar of brick, seen from the front."""
    for k in range(3):
        ww, hh = w - k * w * .16, h * .3
        y = cy - k * hh
        s.add(f'<path d="M{f(cx - ww / 2)} {f(y)}H{f(cx + ww / 2)}V{f(y - hh)}H{f(cx - ww / 2)}Z" fill="{s.lin([(0, mix(color, "#ffb070", .25), 1), (1, mix(color, "#000000", .55), 1)], 0, 0, 0, 1)}"/>')
        bricks = "".join(f"M{f(cx - ww / 2)} {f(y - hh * j / 3)}H{f(cx + ww / 2)}" for j in (1, 2))
        s.add(f'<path d="{bricks}" stroke="#2a0e06" stroke-opacity=".5" stroke-width="2"/>')
        s.add(f'<path d="M{f(cx - ww / 2)} {f(y - hh)}H{f(cx + ww / 2)}" stroke="#ffc080" stroke-opacity=".6" stroke-width="2.5"/>')


def fire(s, cx, cy, w, h, seed=1):
    """A sacred fire: tongues of flame of many sizes, licking and leaning, over glowing embers."""
    rng = random.Random(seed)
    s.glow(cx, cy - h * .4, h * 3.6, "#ff6a1a", .55, .15)
    s.glow(cx, cy - h * .3, h * 1.4, "#ffa040", .6, .3)
    s.add(f'<ellipse cx="{f(cx)}" cy="{f(cy + 4)}" rx="{f(w * .5)}" ry="{f(h * .1)}" fill="#ff7a20" filter="{s.blur(6)}"/>')
    tongues = []
    for k in range(26):
        t = rng.random()
        x = cx + (t - .5) * w * .9
        fh = h * (1 - abs(t - .5) * 1.3) * rng.uniform(.45, 1.1)
        tongues.append((fh, x, rng.uniform(-.25, .25)))
    for fh, x, ln in sorted(tongues, reverse=True):
        s.flame(x, cy + 6, fh, glow=False, lean=ln)
    s.add(f'<g filter="{s.blur(14)}" style="mix-blend-mode:screen"><ellipse cx="{f(cx)}" cy="{f(cy - h * .35)}" rx="{f(w * .4)}" ry="{f(h * .45)}" fill="#ffd080" opacity=".35"/></g>')
    s.motes(60, cx - w * .6, cx + w * .6, cy - h * 2.6, cy - h * .5, color="#ffa040", size=(.8, 2.4), glow=4)
    s.smoke(cx - 30, cy - h * 1.1, h * 2.2, color="#c8b8a8", a=.25, seed=seed, width=3, drift=.15)


@scene
def sacred_thread(s):
    hz = 470
    warm_room(s, hz, light=(560, 360), warm="#6a2a0e", glow_x=560, floor_top="#3a1c0e")
    homa_kunda(s, 560, hz + 20, 520, 160)
    fire(s, 560, hz - 76, 420, 250, seed=3)
    s.add(f'<rect y="{hz + 20}" width="1600" height="{980 - hz}" fill="{s.lin([(0, "#3a1c0e", 1), (1, "#0e0604", 1)], 0, hz + 20, 0, 1000, user=True)}"/>')
    s.add(f'<rect y="{hz + 20}" width="1600" height="{980 - hz}" fill="{s.rad([(0, "#ff8a3a", .4), (1, "#ff8a3a", 0)], 560, hz + 40, 800, user=True, transform=f"translate(0 {(hz + 40) * .6:.0f}) scale(1 .4)")}" style="mix-blend-mode:screen"/>')
    cam = Cam(elev=44, x0=800, y0=690, dist=3000)
    fire_pos = cam.at(560, hz + 20) + np.array([0, 200, 0])
    rig = Rig([Light(fire_pos, "#ffb070", 2.6, 900, shadow=.55, size=90),
               Light(direction=(.4, .6, .7), color="#ffd8b0", power=.45),
               Light(direction=(.6, .5, .6), color="#5a4060", power=.3)],
              sky="#5a3018", ground="#140804", amb=.7)
    c = cam.at(900, 770)
    surfs = [banana_round(c, 300, 2, seed=9)]
    # the thread: three white strands coiled in loose loops, with the brahma knot
    thr = Mat(color=lambda g: C("#fffaf0") * (.85 + .18 * (.5 + .5 * np.sin(g["s"] * 1.1 + g["ang"] * 3)))[:, None],
              rough=.7, ks=.2, wrap=.6, sheen=.6, sheen_col="#ffffff", amb=1.6)
    rng = random.Random(5)
    path = []
    turns = 3
    for k in range(turns * 64 + 1):
        a = 2 * np.pi * k / 64
        r = 170 + 22 * math.sin(a * .5 + 1) + 8 * k / 64 + rng.uniform(-2, 2)
        path.append(c + np.array([r * math.cos(a) * 1.15, 7 + 4 * (k / 64), r * math.sin(a) * .95]))
    for j in range(3):
        off = np.array([math.cos(j * 2.1) * 4.5, j * 1.6, math.sin(j * 2.1) * 4.5])
        surfs.append(tube([p + off for p in path], 3.6, thr, cap=False, dens=1.2))
    knot = c + np.array([178 * 1.15, 24, 0])
    surfs.append(ellipsoid(knot, (24, 17, 20), Mat(color="#fbf6ea", rough=.8, ks=.1, wrap=.55, sheen=.4, sheen_col="#fff0d8",
                                                  bump=lambda u, v: 2 * np.sin(u * 30 + v * 40) ** 2, bump_k=.5)))
    # kusha grass laid alongside
    km = leaf_mat(dark="#4a6a1a", light="#a8b040", vein="#d8d880", seed=3, gloss=.5, spacing=.5, mid=.15)
    for k in range(11):
        a = rng.uniform(-.05, .05)
        b0 = c + np.array([-560 + k * 7, 3 + k * .8, 250 + k * 11])
        surfs.append(leaf(b0, (math.cos(a), .0, -.62 + math.sin(a)), 640 + rng.uniform(-60, 40), 16, km, droop=.0, fold=.35, shape="blade", seed=k))
    stage(s, surfs, cam, rig, ss=3, shadow=dict(floor=0, ao=.55, ao_h=8, ao_blur=4))
    s.add("".join(ob.marigold(x, y, r, c_, k) for k, (x, y, r, c_) in enumerate(
        [(1260, 690, 26, "#f39a1c"), (1300, 714, 21, "#f7c02a")])))
    ob.petals_scatter(s, 300, 1400, 860, 990, 16, seed=12, size=(5, 9))
    s.motes(40, 300, 900, 100, 400, color="#ffb050", seed=13, size=(.8, 2))
    s.fx("mottle", amp=.035, cell=50)
    s.look = {"bloom": 1.1}
    return s
