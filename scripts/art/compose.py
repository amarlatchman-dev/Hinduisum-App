"""Stack a scene's rendered SVG layers and apply its raster effects in order."""
import numpy as np
from PIL import Image

import fx


def compose(ops, png_path):
    """ops: the scene's layer list with each SVG replaced by its layer name."""
    img = None
    for op in ops:
        if op[0] == "svg":
            layer = np.asarray(Image.open(png_path(op[1])).convert("RGBA"), np.float32) / 255
            rgb, a = layer[..., :3], layer[..., 3:4]
            img = rgb * a if img is None else rgb * a + img * (1 - a)
        else:
            img = fx.apply(img, op[1], op[2])
    return np.clip(img, 0, 1)
