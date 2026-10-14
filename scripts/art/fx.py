"""Raster effects applied between SVG layers: soft clouds, water reflections, sun glitter
and light shafts. Images are float32 arrays in 0..1, shape (H, W, 3)."""
import numpy as np
from PIL import Image
from scipy import ndimage


def rgb(c):
    c = c.lstrip("#")
    return np.array([int(c[i:i + 2], 16) / 255 for i in (0, 2, 4)], np.float32)


def smooth(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def fbm(h, w, cell, octaves=5, seed=0, aniso=1.0, gain=0.5, aniso_decay=1.0):
    """Fractal value noise in 0..1. cell is the largest feature size in pixels;
    aniso > 1 stretches features horizontally (aniso_decay < 1 relaxes it for finer octaves)."""
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w), np.float32)
    amp, tot = 1.0, 0.0
    cy = float(cell)
    for o in range(octaves):
        cx = cy * (1 + (aniso - 1) * aniso_decay ** o)
        if cy < 1.5:
            break
        gh, gw = int(h / cy) + 4, int(w / cx) + 4
        g = rng.random((gh, gw)).astype(np.float32)
        z = ndimage.zoom(g, (cy, cx), order=3, mode="reflect", grid_mode=True)
        oy, ox = int(rng.integers(0, int(cy) + 1)), int(rng.integers(0, int(cx) + 1))
        out += amp * z[oy:oy + h, ox:ox + w]
        tot += amp
        amp *= gain
        cy = cy / 2
    return np.clip(out / tot, 0, 1)


def _stretch(n):
    lo, hi = np.percentile(n, 1), np.percentile(n, 99)
    return np.clip((n - lo) / max(1e-6, hi - lo), 0, 1)


def clouds(img, y0, y1, seed=1, cell=160, aniso=3.0, cover=0.5, soft=0.14, lit="#fff1e0", shade=None,
           light=(0.0, 1.0), absorb=2.4, opacity=1.0, sun=None, rim="#fff6e0", rim_a=0.9, x0=0, x1=None,
           top_fade=0.3, bottom_fade=0.3, warp=14, octaves=7, gain=0.56, bump=1.2, body=0.82, direct=1.0):
    """Soft, self-shadowed clouds painted into the band y0..y1. The unlit body takes its
    colour from the sky behind (or shade); light is the direction (dx, dy) towards the
    light; sun=(x, y, radius) adds silver linings near it."""
    H, W, _ = img.shape
    x1 = W if x1 is None else x1
    h, w = int(y1 - y0), int(x1 - x0)
    n = fbm(h + 2 * warp, w + 2 * warp, cell, octaves, seed, aniso, gain, aniso_decay=0.55)
    if warp:
        wx = (fbm(h, w, cell * .5, 3, seed + 11) - .5) * 2 * warp
        wy = (fbm(h, w, cell * .5, 3, seed + 12) - .5) * 2 * warp
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        n = ndimage.map_coordinates(n, [yy + warp + wy, xx + warp + wx], order=1, mode="reflect")
    else:
        n = n[:h, :w]
    n = _stretch(n)
    t = np.linspace(0, 1, h, dtype=np.float32)[:, None]
    prof = (smooth(0, top_fade, t) if top_fade else 1) * (smooth(0, bottom_fade, 1 - t) if bottom_fade else 1)
    d = n * prof
    thr = 1 - cover
    a = smooth(thr, thr + soft, d)
    dens = np.clip((d - thr) / max(1e-6, 1 - thr), 0, 1)
    lx, ly = light
    ln = max(1e-6, (lx * lx + ly * ly) ** .5)
    lx, ly = lx / ln, ly / ln
    # self-shadowing: cloud between this point and the light
    od = np.zeros_like(dens)
    st = cell * 0.07
    for k in range(1, 6):
        od += ndimage.shift(dens, (-ly * k * st, -lx * k * st), order=1, mode="nearest")
    shadow = np.exp(-absorb * od / 5)
    # billows: treat density as height and light its slopes
    db = ndimage.gaussian_filter(dens, max(1.0, cell * 0.025))
    gy, gx = np.gradient(db)
    slope = np.clip(0.5 - bump * cell * 0.35 * (gx * lx + gy * ly), 0, 1)
    lightness = np.clip(shadow * (0.35 + slope) * direct, 0, 1)
    region = img[y0:y0 + h, x0:x0 + w]
    base = region * body if shade is None else region * (1 - body) * 0 + rgb(shade) * 0.6 + region * 0.4
    col = base + (rgb(lit) - base) * lightness[..., None]
    if sun is not None:
        sx, sy, sr = sun
        yy, xx = np.mgrid[y0:y0 + h, x0:x0 + w].astype(np.float32)
        near = np.exp(-(((xx - sx) ** 2 + (yy - sy) ** 2) / (2 * sr * sr)))
        edge = np.clip(a * (1 - dens) * 2.5, 0, 1)
        col = col + (rgb(rim) - col) * np.clip(edge * near * rim_a, 0, 1)[..., None]
    a = (a * opacity)[..., None]
    img[y0:y0 + h, x0:x0 + w] = region * (1 - a) + col * a
    return img


def reflect(img, y0, strength=0.85, tint="#0b0a18", tint_near=0.45, tint_far=0.12, amp=4.0, seed=3,
            squash=1.0, blur=1.6, fade=None, ripple=1.0, y_end=None):
    """Mirror everything above the waterline y0 into the water below it, broken by
    perspective ripples. tint darkens the water, more so close to the viewer."""
    H, W, _ = img.shape
    y_end = H if y_end is None else y_end
    rows = y_end - y0
    d = np.arange(rows, dtype=np.float32)
    p = (d + 2) / rows                      # 0 at the horizon, 1 at the bottom
    # Ripple noise in water-plane coordinates: compressed near the horizon.
    v = np.log1p(d / 3.0) * 30              # rows -> plane depth index
    nh = int(v.max()) + 8
    noise_x = fbm(nh, W + 64, 18, 4, seed, aniso=6.0) - .5
    noise_y = fbm(nh, W + 64, 14, 3, seed + 1, aniso=5.0) - .5
    yy = np.repeat(v[:, None], W, 1)
    xx = np.tile(np.arange(W, dtype=np.float32), (rows, 1))
    scale = (0.25 + 1.6 * p)[:, None]
    nx = ndimage.map_coordinates(noise_x, [yy, xx / scale + 16], order=1, mode="reflect")
    ny = ndimage.map_coordinates(noise_y, [yy, xx / scale + 16], order=1, mode="reflect")
    dx = nx * amp * ripple * (0.5 + 3.2 * p[:, None]) * 2
    dy = ny * amp * ripple * (0.15 + 1.1 * p[:, None])
    src_y = (y0 - 1 - d[:, None] * squash) + dy
    src_y = np.clip(src_y, 0, y0 - 1)
    src_x = np.clip(xx + dx, 0, W - 1)
    out = np.empty((rows, W, 3), np.float32)
    for c in range(3):
        out[..., c] = ndimage.map_coordinates(img[..., c], [src_y, src_x], order=1, mode="nearest")
    if blur:
        bl = ndimage.gaussian_filter(out, (blur * 3, blur, 0))
        m = np.clip(p * 1.3, 0, 1)[:, None, None]
        out = out * (1 - m) + bl * m
    fres = (strength * (1 - 0.35 * p))[:, None, None]
    ta = (tint_far + (tint_near - tint_far) * p)[:, None, None]
    water = out * fres
    water = water * (1 - ta) + rgb(tint) * ta
    if fade is not None:
        f = smooth(0, fade, d / rows)[:, None, None]
        water = img[y0:y_end] * (1 - f) + water * f
    img[y0:y_end] = water
    return img


def glints(img, y0, cx, color="#fff2d0", width=70, strength=1.0, scatter=0.12, seed=5, density=0.5, y_end=None,
           spread=2.6):
    """Sun or moon glitter on rippled water, widest close to the viewer."""
    H, W, _ = img.shape
    y_end = H if y_end is None else y_end
    rows = y_end - y0
    d = np.arange(rows, dtype=np.float32)
    p = (d + 2) / rows
    v = np.log1p(d / 2.0) * 60
    nh = int(v.max()) + 8
    nz = fbm(nh, W + 64, 3.5, 2, seed, aniso=6.0)
    yy = np.repeat(v[:, None], W, 1)
    xx = np.tile(np.arange(W, dtype=np.float32), (rows, 1))
    scale = (0.3 + 1.1 * p)[:, None]
    n = ndimage.map_coordinates(nz, [yy, xx / scale + 16], order=1, mode="reflect")
    n = _stretch(n)
    t = 1 - density * .5
    spark = smooth(t, t + 0.12, n)
    wpath = width * (0.25 + spread * p)[:, None]
    path = np.exp(-((xx - cx) / wpath) ** 2)
    g = spark * (path * strength + scatter * (0.3 + p[:, None]))
    g = ndimage.gaussian_filter(g, (0.5, 1.2))
    col = rgb(color)
    region = img[y0:y_end]
    img[y0:y_end] = 1 - (1 - region) * (1 - np.clip(g[..., None] * col, 0, 1))
    return img


def godrays(img, cx, cy, strength=0.45, decay=0.965, samples=64, density=0.85, thresh=0.72, color=None,
            region=None, radius=320):
    """Light shafts streaming from (cx, cy), cast by bright sky between silhouettes."""
    H, W, _ = img.shape
    sw, sh = W // 2, H // 2
    lum = 0.2126 * img[..., 0] + 0.7152 * img[..., 1] + 0.0722 * img[..., 2]
    m = smooth(thresh, 1.0, lum)[..., None] * img
    if radius:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        m = m * np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * radius * radius))[..., None]
    if region is not None:
        y0, y1 = region
        mask = np.zeros((H, 1, 1), np.float32)
        mask[y0:y1] = 1
        m = m * mask
    if color is not None:
        m = m * 0.4 + smooth(thresh, 1.0, lum)[..., None] * rgb(color) * 0.6
    src = Image.fromarray((np.clip(m, 0, 1) * 255).astype(np.uint8)).resize((sw, sh), Image.BILINEAR)
    acc = np.zeros((sh, sw, 3), np.float32)
    wsum, wgt = 0.0, 1.0
    lx, ly = cx / 2, cy / 2
    for i in range(samples):
        s = 1 - density * i / samples
        # sample point = light + (p - light) * s
        a, b, c = s, 0, lx - lx * s
        d_, e, f_ = 0, s, ly - ly * s
        t = src.transform((sw, sh), Image.AFFINE, (a, b, c, d_, e, f_), resample=Image.BILINEAR)
        acc += np.asarray(t, np.float32) / 255 * wgt
        wsum += wgt
        wgt *= decay
    acc /= wsum
    rays = np.asarray(Image.fromarray((np.clip(acc * 2.5, 0, 1) * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR), np.float32) / 255
    rays = rays * strength
    return 1 - (1 - img) * (1 - np.clip(rays, 0, 1))


def haze(img, y0, y1, color="#ffffff", a0=0.0, a1=0.4):
    """A flat atmospheric wash between y0 and y1."""
    t = np.zeros((img.shape[0], 1, 1), np.float32)
    t[y0:y1, 0, 0] = np.linspace(a0, a1, y1 - y0)
    t[y1:, 0, 0] = a1
    return img * (1 - t) + rgb(color) * t


def mottle(img, amp=0.05, cell=70, aniso=1.8, seed=9, y0=0, y1=None, warm=0.015):
    """Painterly unevenness: soft patches of slightly lighter and warmer paint."""
    H, W, _ = img.shape
    y1 = H if y1 is None else y1
    n = fbm(y1 - y0, W, cell, 5, seed, aniso) - .5
    m = fbm(y1 - y0, W, cell * 1.7, 3, seed + 3, aniso) - .5
    reg = img[y0:y1] * (1 + amp * 2 * n)[..., None]
    reg = reg + (m * warm * 2)[..., None] * np.array([1, .3, -1], np.float32)
    img[y0:y1] = np.clip(reg, 0, 1)
    return img


EFFECTS = {"mottle": mottle, "clouds": clouds, "reflect": reflect, "glints": glints, "godrays": godrays, "haze": haze}


def apply(img, name, kw):
    out = EFFECTS[name](img, **kw)
    return img if out is None else out
