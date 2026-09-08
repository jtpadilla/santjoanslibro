#!/usr/bin/env bash
# Extracción reproducible de los dos PDF del trabajo. Requiere poppler-utils (pdftotext, pdftohtml, pdftoppm, pdfinfo).
#
#   source/EstudioSantjoans.pdf   julio de 2010, 58 págs., maquetado 17×24: EL TEXTO que reproduce la edición
#   source/treball Sanjoan.pdf    mayo de 2010, 47 págs., A4: la versión entregada en la UJI; SUS IMÁGENES son
#                                 unas 4 veces más grandes que las del PDF de julio (ver NOTES.md), y de aquí
#                                 se recortan (extract/images.py).
# Salida (ignorada en git salvo *.txt de metadatos):
#   extract/text/estudio/pNN.txt, pNN.raw.txt   texto por página (con y sin -layout)
#   extract/xml/{estudio,treball}.xml           pdftohtml -xml: posición de cada fragmento de texto e imagen
#   extract/render/{estudio,treball}/p-NN.png   cada página a 300 ppp (de aquí se recortan las imágenes)
set -euo pipefail
cd "$(dirname "$0")"
ESTUDIO=../source/EstudioSantjoans.pdf
TREBALL="../source/treball Sanjoan.pdf"

rm -rf text xml render; mkdir -p text/estudio xml render/estudio render/treball
{ pdfinfo "$ESTUDIO"; echo; pdffonts "$ESTUDIO"; echo; pdfimages -list "$ESTUDIO"; } > pdfinfo-estudio.txt
{ pdfinfo "$TREBALL"; echo; pdffonts "$TREBALL"; echo; pdfimages -list "$TREBALL"; } > pdfinfo-treball.txt

N=$(pdfinfo "$ESTUDIO" | awk '/^Pages:/{print $2}')
for i in $(seq 1 "$N"); do
  p=$(printf 'p%02d' "$i")
  pdftotext -layout -f "$i" -l "$i" "$ESTUDIO" "text/estudio/$p.txt"
  pdftotext         -f "$i" -l "$i" "$ESTUDIO" "text/estudio/$p.raw.txt"
done

pdftohtml -xml -q "$ESTUDIO" xml/estudio >/dev/null
pdftohtml -xml -q "$TREBALL" xml/treball >/dev/null
rm -f xml/*.jpg xml/*.png   # pdftohtml deja las imágenes troceadas al lado del XML; no sirven
pdftoppm -r 300 -png "$ESTUDIO" render/estudio/p
pdftoppm -r 300 -png "$TREBALL" render/treball/p
pdftoppm -r 200 -png -singlefile "../source/incitaciónpavimentceràmic.pdf" render/invitacio   # images.py le quita el blanco

echo "Páginas del estudio: $N"; echo "Renders: $(ls render/estudio render/treball | grep -c png)"
