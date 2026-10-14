"""Build the lesson paintings.  Usage: build.py <workDir> <outDir> [id ...]
Writes each scene's SVG layers to <workDir>/svg, renders them with render.js, stacks the
layers with the raster effects (compose.py) and finishes WebPs into <outDir>."""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import glob  # noqa: E402
import importlib  # noqa: E402

from compose import compose  # noqa: E402
from finish import finish  # noqa: E402
from scenes import SCENES  # noqa: E402

for mod in sorted(glob.glob(os.path.join(HERE, "scenes_*.py"))):
    try:
        importlib.import_module(os.path.basename(mod)[:-3])
    except Exception as e:  # one broken module should not stop the others
        print("skipping", os.path.basename(mod), "-", e, file=sys.stderr)

work, out, *ids = sys.argv[1:]
ids = ids or sorted(SCENES)
missing = [i for i in ids if i not in SCENES]
if missing:
    sys.exit("unknown scenes: " + " ".join(missing))
svg_dir, png_dir = os.path.join(work, "svg"), os.path.join(work, "png")
for d in (svg_dir, png_dir, out):
    os.makedirs(d, exist_ok=True)
plans, names, looks = {}, [], {}
for i in ids:
    ops = []
    sc = SCENES[i]()
    looks[i] = getattr(sc, "look", {})
    for k, op in enumerate(sc.layers()):
        if op[0] == "svg":
            name = f"{i}.{k}"
            with open(os.path.join(svg_dir, name + ".svg"), "w") as fh:
                fh.write(op[1])
            names.append(name)
            ops.append(("svg", name))
        else:
            ops.append(op)
    plans[i] = ops
subprocess.run(["node", os.path.join(HERE, "render.js"), svg_dir, png_dir, *names], check=True)
for k, i in enumerate(ids):
    img = compose(plans[i], lambda n: os.path.join(png_dir, n + ".png"))
    dst = os.path.join(out, i + ".webp")
    finish(img, dst, seed=k, **looks[i])
    print(i, os.path.getsize(dst) // 1024, "KB")
