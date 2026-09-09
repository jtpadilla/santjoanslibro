"""Datos comunes de los dos mapas del capítulo 1: lee extract/mapa/castello.osm.json (descarrega.py), aplica la
división comarcal DEL LIBRO y clasifica los tramos de límite (municipal, comarcal, exterior) para dibujarlos con el
grosor que toca. Los dos mapas del original ponen Vilafranca en l'Alt Maestrat (OSM, siguiendo la demarcación oficial,
la pone en els Ports): se sigue al libro, como hizo masosdemorella."""
import json
from mapalib import ROOT, rings_of

DATA = json.load(open(ROOT / "extract/mapa/castello.osm.json", encoding="utf-8"))
LLIBRE = {"Vilafranca / Villafranca del Cid": "l'Alt Maestrat"}     # municipio → comarca según el libro
for _m in DATA["municipis"]:
    _m["comarca"] = LLIBRE.get(_m["name"], _m["comarca"])
MUNICIPIS = {m["name"]: m for m in DATA["municipis"]}
COMARQUES = [c["name"] for c in DATA["comarques"]]


def rings(m):
    """Anillos (lon, lat) de un municipio del JSON."""
    return rings_of({"members": [{"role": "outer", "geometry": w["geometry"]} for w in m["ways"]]})


def trams(group_of):
    """Clasifica los tramos de límite según los grupos a los que pertenecen los municipios de cada lado.
    group_of(municipio) → clave de grupo (o None = fuera de lo que interesa).
    Devuelve {clase: [geometrías]} con clases: "intern" (mismo grupo a ambos lados), "entre" (dos grupos distintos),
    "vora" (un grupo y el exterior, o un solo municipio: costa) y "fora" (todo exterior)."""
    sides = {}
    for m in DATA["municipis"]:
        for w in m["ways"]:
            sides.setdefault(w["ref"], (w["geometry"], []))[1].append(group_of(m))
    out = {"intern": [], "entre": [], "vora": [], "fora": []}
    for geom, groups in sides.values():
        real = set(groups) - {None}
        if not real:
            cls = "fora"
        elif None in groups or len(groups) == 1:        # el otro lado es exterior, o no hay otro lado (costa)
            cls = "vora"
        elif len(real) == 1:
            cls = "intern"
        else:
            cls = "entre"
        out[cls].append(geom)
    return out


def costa():
    """Encadena los tramos de costa en una polilínea de sur a norte (OSM las orienta con la tierra a la izquierda)."""
    segs = [list(map(tuple, s)) for s in DATA["costa"]]
    lines = []
    while segs:
        line = segs.pop(0)
        grown = True
        while grown:
            grown = False
            for i, s in enumerate(segs):
                if s[0] == line[-1]:
                    line += s[1:]; segs.pop(i); grown = True; break
                if s[-1] == line[0]:
                    line = s[:-1] + line; segs.pop(i); grown = True; break
        lines.append(line)
    line = max(lines, key=len)                       # la costa continental; el resto son islas (les Columbretes)
    return line if line[0][1] < line[-1][1] else line[::-1]
