#!/usr/bin/env python3
"""Recorta las imágenes del libro a partir de los renders a 300 ppp y las deja en assets/.

Los dos PDF llevan cada fotografía troceada en bandas horizontales (Word las exporta así), de modo que
`pdfimages` no sirve. En cambio, `pdftohtml -xml` da la posición de cada banda en la página; la unión de las
bandas de un mismo bloque es el rectángulo de la foto, que se recorta del render de la página.

Se recorta del PDF de MAYO (treball Sanjoan.pdf, A4) porque sus imágenes van a ~300 ppp reales, frente a los
~150 ppp del PDF de julio. La tabla FIGURES dice, para cada imagen del libro (página del PDF de julio), en qué
página del PDF de mayo está y cuál es su nombre de fichero. Las 29 fichas del catálogo van a assets/cataleg/.
Además recorta la invitación de 2012 (extract/render/invitacio.png) a assets/presentacio/00-invitacio.jpg.

Uso: python3 extract/images.py   (tras extract/extract.sh). Necesita Pillow.
"""
import re
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
XML = ROOT / "extract/xml/treball.xml"
RENDER = ROOT / "extract/render/treball"
ESCALA = (300 / 72) / 1.5  # unidades del XML (pt × 1,5) → píxeles a 300 ppp

# (página del PDF de julio, página del PDF de mayo, índice del bloque en esa página ordenado por `left`, fichero
#  [, recorte extra por la izquierda en unidades del XML: el mapa de comarcas pisa 12 unidades del mapa dels Ports])
FIGURES = [
    (1, 1, 0, "images/01-portada-paviment-del-salo.jpg"),
    (7, 7, 1, "images/02-mapa-comarques-de-castello.jpg", 14),
    (7, 7, 0, "images/03-mapa-els-ports.jpg"),
    (9, 8, 1, "images/04-croquis-placa-vella.jpg"),
    (10, 8, 0, "images/05-facana-casa-santjoans.jpg"),
    (11, 9, 0, "images/06-escut-polo-de-bernabe.jpg"),
    (12, 10, 0, "images/07-escut-sanjoan.jpg"),
    (14, 11, 0, "images/08-escut-penarroja.jpg"),
    (16, 12, 0, "images/09-escut-heraldic-sanjoan-i-sousa.jpg"),
    (19, 13, 0, "images/10-paviment-del-salo.jpg"),
    (21, 14, 0, "images/11-fragments-capella-de-sant-vito.jpg"),
    (22, 14, 1, "images/12-auca-mare-de-deu-del-lledo.jpg"),
    (23, 15, 0, "images/13-auca-abat-oliba.jpg"),
]
CATALEG = [
    "pavo-reial", "vaca", "tortuga", "ovella", "serp", "cuco", "sargantana", "balena", "pollastre", "cavall",
    "caragol", "galgo", "dromedari", "sardina", "lleo", "pardal", "elefant", "granota", "molto", "jaguar",
    "cabro", "llebre", "cuco-2", "cervol", "ram-amb-taronja-i-narcis", "ram-amb-taronja-i-flor-trimera",
    "ram-amb-ranuncle-margarida-i-tulipa", "imitacio-de-marbre", "rajola-de-fang-cuit",
]
for i, nom in enumerate(CATALEG):
    # catálogo: julio p27–55 ↔ mayo p18–46, una ficha por página
    FIGURES.append((27 + i, 18 + i, 0, f"cataleg/{i + 1:02d}-{nom}.jpg"))


def blocs(xml: str) -> dict[int, list[tuple[int, int, int, int]]]:
    """Por página: rectángulos (left, top, width, height) que forman las bandas de cada imagen, ordenados por left."""
    out = {}
    for num, body in re.findall(r'<page number="(\d+)"(.*?)</page>', xml, flags=re.S):
        grups: dict[tuple[int, int], list[tuple[int, int]]] = {}
        for m in re.finditer(r"<image ([^>]*)/>", body):
            a = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
            l, t, w, h = (int(a[k]) for k in ("left", "top", "width", "height"))
            grups.setdefault((l, w), []).append((t, h))
        rects = []
        for (l, w), bandes in grups.items():
            t0 = min(t for t, _ in bandes)
            t1 = max(t + h for t, h in bandes)
            if w >= 200 and t1 - t0 >= 200:  # fuera los logotipos de la portada de mayo
                rects.append((l, t0, w, t1 - t0))
        if rects:
            out[int(num)] = sorted(rects)
    return out


def main() -> int:
    if not XML.exists():
        print("Falta extract/xml/treball.xml: ejecuta extract/extract.sh", file=sys.stderr)
        return 1
    per_pagina = blocs(XML.read_text(encoding="utf-8"))
    for p_juliol, p_maig, idx, nom, *extra in FIGURES:
        rects = per_pagina.get(p_maig, [])
        if idx >= len(rects):
            print(f"p{p_maig} de mayo: esperaba el bloque {idx}, hay {len(rects)}", file=sys.stderr)
            return 1
        l, t, w, h = rects[idx]
        if extra:
            l, w = l + extra[0], w - extra[0]
        pagina = Image.open(RENDER / f"p-{p_maig:02d}.png")
        caixa = tuple(round(v * ESCALA) for v in (l, t, l + w, t + h))
        retall = pagina.crop(caixa).convert("RGB")
        desti = ROOT / "assets" / nom
        desti.parent.mkdir(parents=True, exist_ok=True)
        retall.save(desti, quality=92, optimize=True)
        print(f"p{p_juliol:02d} ← mayo p{p_maig:02d}[{idx}] {retall.size[0]}×{retall.size[1]}  {nom}")
    # La invitación de la Diputació (2012): una A4 casi en blanco; se recorta al contenido con un margen
    inv = Image.open(ROOT / "extract/render/invitacio.png").convert("RGB")
    from PIL import ImageChops, ImageOps
    caixa = ImageChops.difference(inv, Image.new("RGB", inv.size, (255, 255, 255))).convert("L").point(lambda v: 255 if v > 24 else 0).getbbox()
    marge = 60
    caixa = (max(caixa[0] - marge, 0), max(caixa[1] - marge, 0), min(caixa[2] + marge, inv.width), min(caixa[3] + marge, inv.height))
    desti = ROOT / "assets/presentacio/00-invitacio.jpg"
    inv.crop(caixa).save(desti, quality=92, optimize=True)
    print(f"invitació {caixa[2] - caixa[0]}×{caixa[3] - caixa[1]}  presentacio/00-invitacio.jpg")
    return 0


if __name__ == "__main__":
    sys.exit(main())
