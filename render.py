#!/usr/bin/env python3
"""Draw "The World in One Day" — a one-page newspaper front page as an image.

Usage:
    python3 render.py <countries-110m.json> [output.png]

The first argument is a Natural Earth countries TopoJSON file (the 110m
resolution set). The day's news is read from stories.json, which sits next to
this script: masthead and dateline, the lead story, three column stories, a
six-story grid, a strip of one-line items, and a set of numbered map markers.

The page is composed on a 1024x1024 canvas:

    masthead  — the paper's name, tagline and dateline between rules
    lead      — kicker, headline, and the deck
    map band  — the world as a field of dots, with the day's places numbered
    columns   — three stories side by side
    grid      — six shorter stories, three across and two down
    strip     — "Also today": the remaining one-liners
    footer    — the sources line
"""

import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# Page geometry and palette
# ---------------------------------------------------------------------------

PAGE = 1024
MARGIN = 46
INK = (24, 22, 20)
PAPER = (247, 243, 236)
FADED = (96, 90, 82)
RULE = (24, 22, 20)
DOT = (120, 112, 100)
ACCENT = (146, 32, 24)

HERE = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# Fonts — try the usual serif/sans system faces, fall back to PIL's bitmap
# ---------------------------------------------------------------------------

_SERIF = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
]
_SERIF_REG = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
]
_SANS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]
_SANS_REG = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
]


def font(paths, size):
    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def wrap(draw, text, fnt, width):
    """Split text into lines that fit `width` pixels."""
    lines, current = [], ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def text_block(draw, xy, text, fnt, fill, width, leading):
    """Draw wrapped text; return the y just below it."""
    x, y = xy
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------------------
# TopoJSON decoding — just enough of the format to recover country polygons
# ---------------------------------------------------------------------------

def decode_topology(topo):
    """Return polygons; a polygon is a list of rings of (lon, lat) points,
    the first ring the outer boundary and the rest holes."""
    transform = topo.get("transform") or {"scale": [1, 1], "translate": [0, 0]}
    sx, sy = transform["scale"]
    tx, ty = transform["translate"]

    arcs = []
    for arc in topo["arcs"]:
        points, x, y = [], 0, 0
        for dx, dy in arc:  # arc coordinates are delta-encoded
            x += dx
            y += dy
            points.append((x * sx + tx, y * sy + ty))
        arcs.append(points)

    def arc_points(index):
        if index >= 0:
            return arcs[index]
        return list(reversed(arcs[~index]))  # negative index: arc backwards

    def ring(indices):
        points = []
        for i in indices:
            seg = arc_points(i)
            points.extend(seg[1:] if points else seg)
        return points

    def geometry_polygons(geom):
        if geom["type"] == "Polygon":
            return [[ring(r) for r in geom["arcs"]]]
        if geom["type"] == "MultiPolygon":
            return [[ring(r) for r in poly] for poly in geom["arcs"]]
        return []

    polygons = []
    for obj in topo["objects"].values():
        geoms = obj["geometries"] if obj["type"] == "GeometryCollection" else [obj]
        for geom in geoms:
            polygons.extend(geometry_polygons(geom))
    return polygons


# ---------------------------------------------------------------------------
# The dotted map
# ---------------------------------------------------------------------------

def project(lon, lat, box):
    """Equirectangular projection into box = (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    return (
        x0 + (lon + 180.0) / 360.0 * (x1 - x0),
        y0 + (90.0 - lat) / 180.0 * (y1 - y0),
    )


def point_in_ring(lon, lat, ring):
    inside = False
    j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i]
        xj, yj = ring[j]
        if (yi > lat) != (yj > lat):
            cross = (xj - xi) * (lat - yi) / (yj - yi) + xi
            if lon < cross:
                inside = not inside
        j = i
    return inside


def prepare_land(polygons):
    """Attach a bounding box to each polygon's outer ring for a fast reject."""
    land = []
    for polygon in polygons:
        if not polygon:
            continue
        outer = polygon[0]
        lons = [p[0] for p in outer]
        lats = [p[1] for p in outer]
        land.append(((min(lons), max(lons), min(lats), max(lats)), polygon))
    return land


def on_land(lon, lat, land):
    for (lo_x, hi_x, lo_y, hi_y), polygon in land:
        if not (lo_x <= lon <= hi_x and lo_y <= lat <= hi_y):
            continue
        if point_in_ring(lon, lat, polygon[0]):
            if not any(point_in_ring(lon, lat, hole) for hole in polygon[1:]):
                return True
    return False


def draw_map(draw, polygons, markers, box):
    x0, y0, x1, y1 = box
    land = prepare_land(polygons)
    step_px = 7
    radius = 1.6
    lat_top, lat_bottom = 84.0, -58.0
    lon_step = 360.0 * step_px / (x1 - x0)   # degrees per dot column
    lat_step = 180.0 * step_px / (y1 - y0)   # degrees per dot row
    rows = int((lat_top - lat_bottom) / lat_step)
    cols = int(360.0 / lon_step)
    for r in range(rows + 1):
        lat = lat_top - r * lat_step
        for c in range(cols + 1):
            lon = -180.0 + c * lon_step
            if on_land(lon, lat, land):
                x, y = project(lon, lat, box)
                draw.ellipse([x - radius, y - radius, x + radius, y + radius],
                             fill=DOT)

    badge_font = font(_SANS, 13)
    label_font = font(_SANS, 11)
    for m in markers:
        x, y = project(m["lon"], m["lat"], box)
        r = 9
        draw.ellipse([x - r, y - r, x + r, y + r], fill=ACCENT)
        label = str(m["n"])
        w = draw.textlength(label, font=badge_font)
        draw.text((x - w / 2, y - 7), label, font=badge_font,
                  fill=(255, 255, 255))
        lx = x + m.get("dx", 9)
        ly = y + m.get("dy", -7)
        label_w = draw.textlength(m["label"], font=label_font)
        lx = max(x0, min(lx, x1 - label_w))  # never spill past the band
        draw.text((lx, ly), m["label"], font=label_font, fill=INK)


# ---------------------------------------------------------------------------
# Page sections
# ---------------------------------------------------------------------------

def draw_masthead(draw, data, y):
    name_font = font(_SERIF, 64)
    name = data["masthead"]
    w = draw.textlength(name, font=name_font)
    draw.text(((PAGE - w) / 2, y), name, font=name_font, fill=INK)
    y += 82

    tag_font = font(_SANS, 17)
    tag = data["tagline"]
    w = draw.textlength(tag, font=tag_font)
    draw.text(((PAGE - w) / 2, y), tag, font=tag_font, fill=FADED)
    y += 30

    draw.line([MARGIN, y, PAGE - MARGIN, y], fill=RULE, width=3)
    y += 8
    date_font = font(_SANS_REG, 15)
    date = data["dateline"]
    w = draw.textlength(date, font=date_font)
    draw.text(((PAGE - w) / 2, y), date, font=date_font, fill=INK)
    y += 26
    draw.line([MARGIN, y, PAGE - MARGIN, y], fill=RULE, width=1)
    return y + 16


def draw_lead(draw, lead, y):
    kicker_font = font(_SANS, 15)
    draw.text((MARGIN, y), lead["kicker"], font=kicker_font, fill=ACCENT)
    y += 24
    head_font = font(_SERIF, 44)
    y = text_block(draw, (MARGIN, y), lead["headline"], head_font, INK,
                   PAGE - 2 * MARGIN, 50)
    y += 4
    deck_font = font(_SERIF_REG, 19)
    y = text_block(draw, (MARGIN, y), lead["deck"], deck_font, FADED,
                   PAGE - 2 * MARGIN, 25)
    return y + 14


def draw_story(draw, story, x, y, width, head_size=21, deck_size=14):
    kicker_font = font(_SANS, 12)
    draw.text((x, y), story["kicker"], font=kicker_font, fill=ACCENT)
    y += 17
    head_font = font(_SERIF, head_size)
    y = text_block(draw, (x, y), story["headline"], head_font, INK, width,
                   int(head_size * 1.18))
    deck_font = font(_SANS_REG, deck_size)
    y = text_block(draw, (x, y + 2), story["deck"], deck_font, FADED, width,
                   int(deck_size * 1.3))
    return y


def draw_columns(draw, stories, y):
    gap = 26
    width = (PAGE - 2 * MARGIN - 2 * gap) / 3
    bottom = y
    for i, story in enumerate(stories):
        x = MARGIN + i * (width + gap)
        bottom = max(bottom, draw_story(draw, story, x, y, width))
    for i in range(1, len(stories)):
        x = MARGIN + i * (width + gap) - gap / 2
        draw.line([x, y, x, bottom], fill=RULE, width=1)
    return bottom + 16


def draw_grid(draw, stories, y):
    gap = 26
    width = (PAGE - 2 * MARGIN - 2 * gap) / 3
    row_height = 128
    for i, story in enumerate(stories):
        x = MARGIN + (i % 3) * (width + gap)
        yy = y + (i // 3) * row_height
        draw_story(draw, story, x, yy, width, head_size=18, deck_size=13)
    return y + 2 * row_height + 8


def draw_also(draw, items, y):
    draw.line([MARGIN, y, PAGE - MARGIN, y], fill=RULE, width=1)
    y += 10
    head_font = font(_SANS, 14)
    draw.text((MARGIN, y), "ALSO TODAY", font=head_font, fill=INK)
    y += 22
    item_font = font(_SANS_REG, 13)
    joined = "  ·  ".join(items)
    y = text_block(draw, (MARGIN, y), joined, item_font, FADED,
                   PAGE - 2 * MARGIN, 18)
    return y + 10


def draw_footer(draw, footer, y):
    draw.line([MARGIN, y, PAGE - MARGIN, y], fill=RULE, width=3)
    y += 10
    foot_font = font(_SANS_REG, 12)
    w = draw.textlength(footer, font=foot_font)
    draw.text(((PAGE - w) / 2, y), footer, font=foot_font, fill=FADED)
    return y + 20


# ---------------------------------------------------------------------------
# Compose the page
# ---------------------------------------------------------------------------

def render(topo_path, out_path):
    data = json.loads((HERE / "stories.json").read_text(encoding="utf-8"))
    topo = json.loads(Path(topo_path).read_text(encoding="utf-8"))
    polygons = decode_topology(topo)

    img = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(img)

    y = draw_masthead(draw, data, 30)
    y = draw_lead(draw, data["lead"], y)

    map_top = y
    map_bottom = y + 268
    draw_map(draw, polygons, data["markers"],
             (MARGIN, map_top, PAGE - MARGIN, map_bottom))
    y = map_bottom + 18

    y = draw_columns(draw, data["column"], y)
    draw.line([MARGIN, y - 6, PAGE - MARGIN, y - 6], fill=RULE, width=1)
    y = draw_grid(draw, data["grid"], y)
    y = draw_also(draw, data["also"], y)
    draw_footer(draw, data["footer"], y)

    img.save(out_path)
    return out_path


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    topo_path = argv[1]
    out_path = argv[2] if len(argv) > 2 else str(HERE / "front-page.png")
    render(topo_path, out_path)
    print(f"wrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
