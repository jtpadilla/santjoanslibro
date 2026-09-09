#!/usr/bin/env python3
"""Genera assets/images/03-mapa-els-ports.svg: versión nueva del mapa de la comarca dels Ports del libro (una imagen
de Wikimedia borrosa en el PDF), con los límites municipales reales de OpenStreetMap (extract/mapa/castello.osm.json)
y el estilo del mapa dels Ports de masosdemorella, del que este script es una adaptación.

Reproduce los 13 municipios que dibujaba el mapa original (omite Vilafranca, como aquel y como el mapa de comarcas del
libro) con sus rótulos, Cinctorres destacada, y las comarcas vecinas Alt Maestrat y Baix Maestrat rotuladas.
Uso: python3 extract/mapa/mapa_ports.py [dir node_modules con opentype.js; por defecto site/node_modules]
"""
import sys
from mapalib import FILL, FILL_HI, INK, INK_SOFT, PAPER, ROOT, Projection, glyph_defs, label, labels_open, svg_open, text_paths
from castello import DATA, MUNICIPIS, rings, trams

OUT = ROOT / "assets/images/03-mapa-els-ports.svg"
NODE_MODULES = sys.argv[1] if len(sys.argv) > 1 else None

# Municipios del mapa original → nombre OSM, rótulo (como en el original) y núcleo urbano (lat, lon).
MUNIS = [
    ("Zorita del Maestrazgo", ["ZORITA"],            (40.7275, -0.1672)),
    ("Palanques",             ["PALANQUES"],         (40.7174, -0.1791)),
    ("Herbers",               ["HERBERS"],           (40.7207, -0.0044)),
    ("Villores",              ["VILLORES"],          (40.6763, -0.2007)),
    ("Forcall",               ["EL FORCALL"],        (40.6461, -0.1996)),
    ("Todolella",             ["LA", "TODOLELLA"],   (40.6470, -0.2468)),
    ("Olocau del Rey",        ["OLOCAU", "DEL REY"], (40.6376, -0.3399)),
    ("la Mata de Morella",    ["LA MATA"],           (40.6164, -0.2795)),
    ("Morella",               ["MORELLA"],           (40.6188, -0.0998)),
    ("Vallibona",             ["VALLIBONA"],         (40.6031, 0.0466)),
    ("Cinctorres",            ["CINCTORRES"],        (40.5826, -0.2161)),
    ("Portell de Morella",    ["PORTELL DE", "MORELLA"], (40.5328, -0.2622)),
    ("Castellfort",           ["CASTELLFORT"],       (40.5022, -0.1911)),
]
# Colocación del rótulo respecto al punto del núcleo: (dx, dy, anclaje)
PLACE = {
    "Zorita del Maestrazgo": (0, -12, "middle"),
    "Palanques":             (0, 20, "middle"),
    "Herbers":               (0, 22, "middle"),
    "Villores":              (0, -11, "middle"),
    "Forcall":               (10, 5, "start"),
    "Todolella":             (-9, -4, "end"),
    "Olocau del Rey":        (0, 22, "middle"),
    "la Mata de Morella":    (-10, 5, "end"),
    "Morella":               (0, 22, "middle"),
    "Vallibona":             (12, 6, "start"),
    "Cinctorres":            (0, 30, "middle"),
    "Portell de Morella":    (-10, -2, "end"),
    "Castellfort":           (0, 22, "middle"),
}
VEINS = [("ALT MAESTRAT", (40.455, -0.235)), ("BAIX MAESTRAT", (40.515, 0.115))]
HI = "Cinctorres"
W, H, MARGIN = 1000, 900, 40

ports = {n: rings(MUNICIPIS[n]) for n, _, _ in MUNIS}
proj = Projection([p for r in ports.values() for ring in r for p in ring], W, H, MARGIN)
km = proj.scale / 111.2

req = [{"id": f"{n}|{i}", "text": line, "size": 19 if n == HI else 12.5,
        "weight": 600 if n == HI else 500, "tracking": 2.2 if n == HI else 1.3}
       for n, lines, _ in MUNIS for i, line in enumerate(lines)]
req += [{"id": f"v|{n}", "text": n, "size": 14, "weight": 500, "tracking": 3.5} for n, _ in VEINS]
req += [{"id": "escala", "text": "5 km", "size": 10.5, "weight": 400, "tracking": 0.2}]
G = text_paths(req, *(NODE_MODULES,) if NODE_MODULES else ())

svg = svg_open(W, H, "Mapa dels Ports", "Mapa dels Ports: els municipis de la comarca, amb Cinctorres destacada, i les comarques veïnes")
svg.append(glyph_defs())

# rellenos: los 13 municipios (Cinctorres destacada); los vecinos quedan del color del papel
svg.append('<g stroke="none">')
for n, r in ports.items():
    svg.append(f'<path d="{proj.path(r)}" fill="{FILL_HI if n == HI else FILL}"/>')
svg.append('</g>')

# límites: dentro de la comarca finos; contorno de la comarca grueso; los vecinos, muy tenues
def strokes(geoms, color, width, opacity=1):
    """Tramos como un solo <path>; los que quedan del todo fuera del dibujo se omiten (pesan y no se ven)."""
    inside = lambda pts: any(-60 < x < W + 60 and -60 < y < H + 60 for x, y in pts)
    d = "".join("M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
                for pts in ([proj(*p) for p in g] for g in geoms) if inside(pts))
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-opacity="{opacity}" stroke-linejoin="round" stroke-linecap="round"/>'
T = trams(lambda m: "ports" if m["name"] in ports else None)
V = trams(lambda m: None if m["name"] in ports else (m["comarca"] or "fora"))
svg.append(strokes(V["intern"], INK_SOFT, 0.6, 0.45))
svg.append(strokes(V["entre"], INK_SOFT, 1.1, 0.7))
svg.append(strokes(T["intern"], INK_SOFT, 0.9))
svg.append(strokes(T["vora"], INK, 4))

# rótulos
svg.append(labels_open())
for name, lines, (lat, lon) in MUNIS:
    x, y = proj(lon, lat)
    svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{4.2 if name == HI else 3.2}" stroke="none"/>')
    dx, dy, anchor = PLACE[name]
    lh = 23 if name == HI else 15
    for i, line in enumerate(lines):
        svg.append(label(G[f"{name}|{i}"], x + dx, y + dy + i * lh, anchor))
svg.append('</g>')
svg.append(f'<g fill="{INK_SOFT}">')
for n, (lat, lon) in VEINS:
    x, y = proj(lon, lat)
    svg.append(label(G[f"v|{n}"], x, y))
svg.append('</g>')

# escala
x, y = MARGIN + 20, H - MARGIN - 12
svg.append(f'<g stroke="{INK}" stroke-width="1.4"><path d="M{x} {y}h{5 * km:.1f}M{x} {y - 5}v10M{x + 5 * km:.1f} {y - 5}v10"/></g>')
svg.append(f'<g fill="{INK}">{label(G["escala"], x + 5 * km / 2, y - 8)}</g>')
svg.append('</svg>')
OUT.write_text("\n".join(svg), encoding="utf-8")
print(f"{OUT.relative_to(ROOT)}: {OUT.stat().st_size // 1024} KB")
