# Lesson paintings

The illustrations in `img/learn/*.webp` are painted entirely by code. Nothing is
traced or downloaded, and every scene is original.

Each scene is a Python function. It draws SVG layers, which Chromium renders, and
between the layers it applies raster effects with numpy: clouds, water reflections,
sun glitter and light shafts. A finishing pass adds bloom, a gentle grade, a vignette
and fine grain, then writes a 1200 x 750 WebP.

```
python3 build.py <workDir> <outDir> [id ...]
```

With no ids it builds every painting. To refresh the app's images, point `outDir` at `img/learn`.

Needs Python 3 with numpy, scipy and Pillow, plus Node with Playwright. Point
`PLAYWRIGHT` at the playwright module and `CHROME` at a Chromium binary if they are
not on the default paths.

## Files

| File | What it holds |
| --- | --- |
| `paint.py` | `Scene`: gradients, filters, masks, glows, sun, moon, stars, flames, smoke, mist, birds, bokeh. `s.fx(name, **kw)` closes the current SVG layer and queues a raster effect. |
| `fx.py` | Raster effects: `clouds`, `reflect`, `glints`, `godrays`, `haze`, `mottle`. A scene module can register its own with `fx.EFFECTS["name"] = fn`, where `fn(img, **kw)` takes and returns a float RGB array. |
| `land.py` | Ridgelines (`ridgeline`, `peak_line`), lit snowy `mountains`, `hills`, `pines`, round trees, grass, plus curve helpers (`smooth_line`, `ribbon`, `y_at`). |
| `arch.py` | Temples (`nagara`, `shikhara_front`), `chhatri`, riverside buildings and `skyline`, ghat `steps`, `umbrella`, `boat`, lamp pillar, rocks, floating `leaf_lamp`. |
| `objects.py` | Lotus flowers, buds and leaves, the gold Om, still-life pieces (`dark_room`, `stone_wall`, `arch_niche`, `ledge`), `marigold` and `garland`, petals, `clay_diya`, `brass_lamp`, `bells`, and `reflect_since` for things floating on water. |
| `figures.py` | Human silhouettes: pilgrim, seated meditator, priest raising an aarti lamp, sitter, rower. |
| `scenes.py` | The `@scene` registry and four reference paintings: `om`, `ghats`, `pilgrim` and `flame`. The id is the function name with `_` changed to `-`. |
| `scenes_land.py` | Landscapes, rivers and seas, temples and the avatar stories set on water. Adds the `sea` and `foliage` effects. |
| `scenes_divine.py` | The gods through their emblems, sacred geometry and the cosmos. Adds the `nebula`, `starfield`, `addglow` and `beam` effects. |
| `scenes_still.py` | Still lifes of sacred objects. A small numpy 3D renderer (the `still3d` effect) shades the hero objects, so these are the slowest to build, at about a minute each. |
| `scenes_festive.py` | Festivals, home rituals and the rites of passage. Adds the `powder` effect for Holi colour. |
| `scenes_stories.py` | The children's stories: the Panchatantra animals as silhouettes (monkey, crocodile, lion, hare, geese, jackal, crows, mongoose, heron, crab, donkey, doves). |
| `scenes_story.py` | People, animals and stories: sages, devotees, the temple elephant, the chariot. |
| `compose.py`, `finish.py`, `render.js`, `build.py` | The pipeline. |

## Style

These are devotional paintings. They should be quiet, luminous and reverent, not
diagrams.

- **Light first.** Every scene has one clear light source: sun, moon, lamp or fire.
  Rim light falls on the edges that face it, and the air glows around it.
- **Depth through air.** Layers lighten and cool with distance, and mist gathers in
  valleys and over water.
- **Composition.** The canvas is 1600 x 1000. Lists show a square centre crop
  (x 300 to 1300), so the subject must sit there and read at 70 px.
- **Gods are shown through their emblems and places, not their bodies.** For example,
  Shiva is shown through Kailash, the crescent, the trident and the Ganga, and
  Vishnu through the cosmic ocean, Shesha's hoods and the four emblems. The one
  exception is a respectful silhouette where the story needs it, such as Hanuman's
  leap.
- **Palette.** Dawn and dusk use indigo, violet, rose and gold. Night uses deep
  blue with silver and warm lamps. Interiors use dark umber with amber light.
- **Finish.** End most scenes with `s.fx("mottle", amp=.04, cell=60)`. To tune the
  grade, set `s.look = {"vibrance": .15}`; `contrast`, `vignette` and `bloom` can
  be set the same way.
