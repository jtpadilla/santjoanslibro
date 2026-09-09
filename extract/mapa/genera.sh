#!/usr/bin/env bash
# Regenera los dos mapas SVG del capítulo 1 (assets/images/02-mapa-comarques-de-castello.svg y 03-mapa-els-ports.svg)
# a partir de extract/mapa/castello.osm.json (que se versiona; para volver a descargarlo: python3 descarrega.py).
# Requiere python3, node y las dependencias del sitio instaladas (cd site && npm install: aporta opentype.js).
# Con --png, exporta además una vista PNG de cada uno a extract/mapa/preview/ (requiere inkscape).
set -euo pipefail
cd "$(dirname "$0")"
[ -d ../../site/node_modules/opentype.js ] || { echo "Falta opentype.js: ejecuta 'npm install' en site/" >&2; exit 1; }
python3 mapa_comarques.py
python3 mapa_ports.py
if [ "${1:-}" = "--png" ]; then
  mkdir -p preview
  for f in ../../assets/images/0[23]-*.svg; do
    inkscape --export-type=png --export-width=1200 --export-filename="preview/$(basename "${f%.svg}").png" "$f" >/dev/null 2>&1
  done
  echo "vistas en extract/mapa/preview/"
fi
