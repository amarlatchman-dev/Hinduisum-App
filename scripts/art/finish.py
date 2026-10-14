"""Finish rendered scenes like a photograph of a painting: bloom, gentle grading,
vignette and fine grain, then save a web-sized WebP.  Usage: finish.py <pngDir> <outDir> [id ...]"""
import os
import sys

import numpy as np
from PIL import Image, ImageFilter

from kuwahara import kuwahara

OUT_W, OUT_H = 1200, 750


def finish(src, dst, seed=0, vibrance=0.0, contrast=1.06, vignette=0.34, bloom=1.0):
    """src is a PNG path or a float RGB array in 0..1. A scene can tune the look by setting
    scene.look = {"vibrance": .15, "contrast": 1.1, "vignette": .3, "bloom": .8}."""
    if isinstance(src, str):
        a = np.asarray(Image.open(src).convert("RGB")).astype(np.float32) / 255.0
    else:
        a = src.astype(np.float32)
    h, w, _ = a.shape
    rng = np.random.default_rng(seed)

    # Painterly pass: a little canvas noise, then a Kuwahara filter turns it into brush strokes.
    if os.environ.get("PAINTERLY", "0") == "1":
        canvas = rng.normal(0, 0.03, (h, w, 1)).astype(np.float32)
        a = np.clip(0.72 * kuwahara(np.clip(a + canvas, 0, 1), 3) + 0.28 * a, 0, 1)
        soft = np.asarray(Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))).astype(np.float32) / 255
        a = np.clip(a + (a - soft) * 0.6, 0, 1)
    lum = (0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2])[..., None]

    # Bloom: blur the brightest light and add it back as a soft glow.
    bright = np.clip((lum - 0.66) / 0.34, 0, 1) * a
    small = Image.fromarray((bright * 255).astype(np.uint8)).resize((w // 4, h // 4), Image.BILINEAR)
    glow = np.zeros_like(a)
    for radius, weight in ((4, 0.4), (12, 0.35), (30, 0.3)):
        g = small.filter(ImageFilter.GaussianBlur(radius)).resize((w, h), Image.BILINEAR)
        glow += np.asarray(g).astype(np.float32) / 255.0 * weight * bloom
    a = 1 - (1 - a) * (1 - np.clip(glow, 0, 1))

    # Grade: warm the highlights, deepen the shadows toward indigo.
    lum = (0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2])[..., None]
    a = a + (lum ** 2) * np.array([0.03, 0.012, -0.02]) + ((1 - lum) ** 3) * np.array([-0.012, -0.004, 0.02])
    a = np.clip((a - 0.5) * contrast + 0.5, 0, 1)
    if vibrance:
        grey = (0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2])[..., None]
        sat = a.max(-1, keepdims=True) - a.min(-1, keepdims=True)
        a = np.clip(grey + (a - grey) * (1 + vibrance * (1 - sat)), 0, 1)

    # Vignette.
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2) / 1.414
    a *= (1 - vignette * np.clip(r, 0, 1) ** 2.2)[..., None]

    # Fine film grain, a little stronger in the shadows.
    noise = rng.normal(0, 0.016, (h, w, 1)).astype(np.float32)
    a = np.clip(a + noise * (0.55 + 0.45 * (1 - lum)), 0, 1)

    out = Image.fromarray((a * 255 + 0.5).astype(np.uint8)).resize((OUT_W, OUT_H), Image.LANCZOS)
    out.save(dst, "WEBP", quality=80, method=6)


if __name__ == "__main__":
    src_dir, out_dir, *ids = sys.argv[1:]
    os.makedirs(out_dir, exist_ok=True)
    ids = ids or sorted(f[:-4] for f in os.listdir(src_dir) if f.endswith(".png"))
    for k, i in enumerate(ids):
        finish(os.path.join(src_dir, i + ".png"), os.path.join(out_dir, i + ".webp"), seed=k)
        print(i, os.path.getsize(os.path.join(out_dir, i + ".webp")) // 1024, "KB")
