#!/usr/bin/env python3
"""Genera assets/images/02-mapa-comarques-de-castello.svg: versión nueva del mapa de las comarcas de Castelló del
libro (un mapa comercial ilegible en el PDF), con los límites reales de OpenStreetMap (extract/mapa/castello.osm.json)
y el estilo de los mapas de masosdemorella (tinta sobre papel, rótulos en EB Garamond como trazados).

Contenido: las ocho comarcas rotuladas, els Ports destacada, Cinctorres, Morella y Castelló de la Plana, las
provincias vecinas y el mar. Vilafranca va en l'Alt Maestrat, como en el libro (castello.py).
Uso: python3 extract/mapa/mapa_comarques.py [dir node_modules con opentype.js; por defecto site/node_modules]
"""
import sys
from mapalib import FILL, FILL_HI, INK, INK_SOFT, ROOT, Projection, glyph_defs, label, labels_open, svg_open, text_paths
from castello import COMARQUES, DATA, costa, rings, trams

OUT_NAME = "02-mapa-comarques-de-castello.svg"
NODE_MODULES = sys.argv[1] if len(sys.argv) > 1 else None
SEA = "#e4e9ea"
W, H, MARGIN = 900, 980, 60

# Rótulos de comarca (texto del libro en valenciano) y punto (lat, lon) donde va cada uno.
ROTULS = {
    "els Ports":        (["ELS PORTS"],       (40.700, -0.130)),
    "l'Alt Maestrat":   (["L'ALT MAESTRAT"],  (40.400, -0.180)),
    "el Baix Maestrat": (["EL BAIX MAESTRAT"], (40.470, 0.230)),
    "l'Alcalatén":      (["L'ALCALATÉN"],     (40.170, -0.330)),
    "la Plana Alta":    (["LA PLANA ALTA"],   (40.140, 0.070)),
    "la Plana Baixa":   (["LA PLANA BAIXA"],  (39.875, -0.200)),
    "El Alto Mijares":  (["L'ALT MILLARS"],   (40.070, -0.560)),
    "l'Alt Palància":   (["L'ALT PALÀNCIA"],  (39.860, -0.600)),
}
POBLES = [  # nombre, (lat, lon), (dx, dy, anclaje), destacado
    ("Cinctorres",           (40.5826, -0.2161), (-9, 4, "end"), True),
    ("Morella",              (40.6188, -0.0998), (9, 4, "start"), False),
    ("Castelló de la Plana", (39.9864, -0.0513), (9, 4, "start"), False),
]
VEINS = [("TEROL", (40.35, -0.86)), ("TARRAGONA", (40.83, 0.32)), ("VALÈNCIA", (39.66, -0.62)),
         ("MAR MEDITERRÀNIA", (40.02, 0.42)), ("ILLES COLUMBRETES", (39.83, 0.50))]

prov = [m for m in DATA["municipis"] if m["comarca"]]
frame_pts = [p for m in prov for r in rings(m) for p in r if p[0] < 0.6]     # sin les Columbretes
lons = [p[0] for p in frame_pts]; lats = [p[1] for p in frame_pts]
pad = 0.10
proj = Projection([(min(lons) - pad, min(lats) - pad), (max(lons) + pad, max(lats) + pad)], W, H, MARGIN)
km = proj.scale / 111.2

req = [{"id": f"c|{c}", "text": t, "size": 14.5, "weight": 600, "tracking": 2.6} for c, (ls, _) in ROTULS.items() for t in ls]
req += [{"id": f"p|{n}", "text": n, "size": 15 if hi else 12, "weight": 600 if hi else 500, "tracking": 0.6} for n, _, _, hi in POBLES]
req += [{"id": f"v|{n}", "text": n, "size": 9 if "COLUMBRETES" in n else 13, "weight": 500, "tracking": 4} for n, _ in VEINS]
req += [{"id": "escala", "text": "20 km", "size": 10.5, "weight": 400, "tracking": 0.2}]
G = text_paths(req, *(NODE_MODULES,) if NODE_MODULES else ())

svg = svg_open(W, H, "Mapa de les comarques de Castelló",
               "Mapa de la província de Castelló amb les huit comarques, els Ports destacada i Cinctorres, Morella i Castelló de la Plana")
svg.append(glyph_defs())

# mar: la costa de sur a norte, cerrada por fuera del dibujo
line = [proj(*p) for p in costa()]
d = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in line) + f"L{W + 200} {line[-1][1]:.1f}L{W + 200} {line[0][1]:.1f}Z"
svg.append(f'<path d="{d}" fill="{SEA}" stroke="{INK_SOFT}" stroke-width="0.8"/>')

# rellenos por comarca
svg.append('<g stroke="none">')
for m in prov:
    svg.append(f'<path d="{proj.path(rings(m))}" fill="{FILL_HI if m["comarca"] == "els Ports" else FILL}"/>')
svg.append('</g>')

# límites: municipales muy finos, comarcales medios, provincia y costa gruesos
T = trams(lambda m: m["comarca"])
def strokes(geoms, color, width, opacity=1):
    """Tramos como un solo <path>; los que quedan del todo fuera del dibujo se omiten (pesan y no se ven)."""
    inside = lambda pts: any(-60 < x < W + 60 and -60 < y < H + 60 for x, y in pts)
    d = "".join("M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
                for pts in ([proj(*p) for p in g] for g in geoms) if inside(pts))
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-opacity="{opacity}" stroke-linejoin="round" stroke-linecap="round"/>'
svg.append(strokes(T["intern"], INK_SOFT, 0.5, 0.55))
svg.append(strokes(T["entre"], INK, 1.5))
svg.append(strokes(T["vora"], INK, 3))

# rótulos
svg.append(labels_open())
for c, (ls, (lat, lon)) in ROTULS.items():
    x, y = proj(lon, lat)
    for i, t in enumerate(ls):
        svg.append(label(G[f"c|{c}"], x, y + i * 18))
for n, (lat, lon), (dx, dy, anchor), hi in POBLES:
    x, y = proj(lon, lat)
    if n == "Castelló de la Plana":
        svg.append(f'<rect x="{x - 4:.1f}" y="{y - 4:.1f}" width="8" height="8" stroke="none"/>')
    else:
        svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{4.6 if hi else 3.2}" stroke="none"/>')
    svg.append(label(G[f"p|{n}"], x + dx, y + dy, anchor))
svg.append('</g>')
svg.append(f'<g fill="{INK_SOFT}">')
for n, (lat, lon) in VEINS:
    x, y = proj(lon, lat)
    svg.append(label(G[f"v|{n}"], x, y))
svg.append('</g>')

# escala
x, y = MARGIN + 10, H - MARGIN + 10
svg.append(f'<g stroke="{INK}" stroke-width="1.4"><path d="M{x} {y}h{20 * km:.1f}M{x} {y - 5}v10M{x + 20 * km:.1f} {y - 5}v10"/></g>')
svg.append(f'<g fill="{INK}">{label(G["escala"], x + 10 * km, y - 8)}</g>')
svg.append('</svg>')

OUT = ROOT / "assets/images" / OUT_NAME
OUT.write_text("\n".join(svg), encoding="utf-8")
print(f"{OUT.relative_to(ROOT)}: {OUT.stat().st_size // 1024} KB")
