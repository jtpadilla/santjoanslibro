#!/usr/bin/env python3
"""Descarga de OpenStreetMap (Overpass) los datos de los dos mapas del capítulo 1 y los deja en
extract/mapa/castello.osm.json, que SE VERSIONA: construir no necesita red (Overpass se satura a menudo; el script
reintenta con varios servidores). © colaboradores de OpenStreetMap, ODbL.

Contenido del JSON:
  comarques:  [{name, ways: [{ref, geometry}]}]  las 8 comarcas de la provincia de Castelló (admin_level 7)
  municipis:  [{name, comarca, ways: [{ref, geometry}]}]  municipios (admin_level 8) de la caja que envuelve la
              provincia con margen, es decir, también los vecinos de Teruel, Tarragona y València (comarca = null).
              La comarca se asigna por el punto representativo del municipio dentro del polígono de la comarca (las
              relaciones de comarca de OSM no siempre listan sus municipios). Se guarda el id de cada tramo (ref) para
              saber qué tramos separan comarcas o provincias.
  costa:      [[[lon, lat], ...], ...]  tramos de línea de costa (natural=coastline) de la misma caja.
Las coordenadas se redondean a 5 decimales (~1 m) y cada tramo se simplifica a ~20 m para que el fichero pese poco.
Uso: python3 extract/mapa/descarrega.py
"""
import json, sys, time, urllib.request
from pathlib import Path
from mapalib import rings_of, simplify

OUT = Path(__file__).resolve().parent / "castello.osm.json"
SERVERS = ["https://overpass-api.de/api/interpreter", "https://overpass.kumi.systems/api/interpreter",
           "https://overpass.private.coffee/api/interpreter"]
BBOX = "39.55,-1.05,40.95,0.70"   # sur, oeste, norte, este: la provincia de Castelló con margen
Q_COMARQUES = """[out:json][timeout:180];
area["boundary"="administrative"]["admin_level"="6"]["name"~"Castell"]->.prov;
rel(area.prov)["boundary"="administrative"]["admin_level"="7"];out geom;"""
Q_MUNICIPIS = f'[out:json][timeout:300];rel["boundary"="administrative"]["admin_level"="8"]({BBOX});out geom;'
Q_COSTA = f'[out:json][timeout:120];way["natural"="coastline"]({BBOX});out geom;'


def overpass(query):
    for attempt in range(6):
        server = SERVERS[attempt % len(SERVERS)]
        try:
            req = urllib.request.Request(server, data=query.encode(), headers={"User-Agent": "santjoanslibro/1.0"})
            with urllib.request.urlopen(req, timeout=400) as r:
                data = json.loads(r.read())
            if "elements" in data:
                return data["elements"]
        except Exception as e:                      # 429/504, JSON de error…
            print(f"  {server}: {e}", file=sys.stderr)
        time.sleep(20 * (attempt + 1))
    sys.exit("Overpass no responde; probar más tarde")


def tram(geometry):
    pts = [(round(p["lon"], 5), round(p["lat"], 5)) for p in geometry]
    return simplify(pts, 0.0002)                    # ~20 m; los tramos compartidos se simplifican igual (misma entrada)


def boundaries(elements):
    out = []
    for e in elements:
        name = e.get("tags", {}).get("name")
        if not name:
            continue
        ways = [{"ref": m["ref"], "geometry": tram(m["geometry"])}
                for m in e["members"] if m["type"] == "way" and m["role"] in ("outer", "") and "geometry" in m]
        out.append({"name": name, "ways": ways})
    return out


def inside(pt, rings):
    """Punto dentro de alguno de los anillos (ray casting)."""
    x, y = pt
    for ring in rings:
        c = False
        for (x1, y1), (x2, y2) in zip(ring, ring[1:] + ring[:1]):
            if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
                c = not c
        if c:
            return True
    return False


print("comarques…", file=sys.stderr)
comarques = boundaries(overpass(Q_COMARQUES))
print("  " + ", ".join(c["name"] for c in comarques), file=sys.stderr)

print("municipis…", file=sys.stderr)
municipis = boundaries(overpass(Q_MUNICIPIS))
com_rings = {c["name"]: rings_of({"members": [dict(role="outer", **w) for w in c["ways"]]}) for c in comarques}
for m in municipis:
    # punto representativo: media del anillo mayor (Castelló de la Plana incluye les Columbretes: la media de todo
    # caería al mar)
    ring = max(rings_of({"members": [dict(role="outer", **w) for w in m["ways"]]}), key=len)
    pt = (sum(p[0] for p in ring) / len(ring), sum(p[1] for p in ring) / len(ring))
    m["comarca"] = next((n for n, rings in com_rings.items() if inside(pt, rings)), None)
counts = {c["name"]: sum(m["comarca"] == c["name"] for m in municipis) for c in comarques}
print(f"  {len(municipis)} municipis; " + "; ".join(f"{k}: {v}" for k, v in counts.items()), file=sys.stderr)

print("costa…", file=sys.stderr)
costa = [tram(e["geometry"]) for e in overpass(Q_COSTA) if "geometry" in e]
print(f"  {len(costa)} trams", file=sys.stderr)

OUT.write_text(json.dumps({"comarques": comarques, "municipis": municipis, "costa": costa},
                          ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"{OUT.name}: {OUT.stat().st_size // 1024} KB", file=sys.stderr)
