"""A Kuwahara filter: smooths flat areas into brush-like strokes while keeping edges crisp."""
import numpy as np


def _box(ii, r, h, w):
    # Sum over (2r+1)-wide windows using an integral image padded by r on every side.
    k = r + 1
    return ii[k:k + h, k:k + w] - ii[:h, k:k + w] - ii[k:k + h, :w] + ii[:h, :w]


def kuwahara(a, r=4):
    h, w, _ = a.shape
    lum = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    pad = lambda x: np.pad(x, ((r + 1, r + 1), (r + 1, r + 1)) + ((0, 0),) * (x.ndim - 2), mode="edge")
    best_var = np.full((h, w), np.inf, np.float32)
    out = np.zeros_like(a)
    n = (r + 1) ** 2
    for dy, dx in ((0, 0), (0, r), (r, 0), (r, r)):
        # quadrant windows of size (r+1) whose top-left is offset by (dy - r, dx - r)
        sl = lambda x: pad(x)[dy:dy + h + r + 1, dx:dx + w + r + 1]
        L = sl(lum)
        C = sl(a)
        def wsum(x):
            ii = np.cumsum(np.cumsum(np.pad(x, ((1, 0), (1, 0)) + ((0, 0),) * (x.ndim - 2)), 0), 1)
            return ii[r + 1:r + 1 + h, r + 1:r + 1 + w] - ii[:h, r + 1:r + 1 + w] - ii[r + 1:r + 1 + h, :w] + ii[:h, :w]
        m = wsum(L) / n
        v = wsum(L * L) / n - m * m
        mc = wsum(C) / n
        sel = v < best_var
        best_var = np.where(sel, v, best_var)
        out = np.where(sel[..., None], mc, out)
    return out
