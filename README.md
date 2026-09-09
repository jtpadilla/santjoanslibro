# Paviment ceràmic de la casa Santjoans — edición digital

El estudio de **Francisca Julián Querol** sobre el pavimento cerámico zoomórfico del salón noble del Palau Santjoans
de Cinctorres: quién levantó la casa, de dónde salieron los azulejos y un catálogo de 29 piezas. Fue su trabajo de
final del segundo ciclo de la Universitat per a Majors (UJI, mayo de 2010) y la **Diputació de Castelló lo publicó en
libro en 2012** (*Paviment ceràmic de la casa Santjoans (Cinctorres)*, col. Biblioteca Popular, ISBN 978-84-15301-12-7).

**Estado: boceto** (2026-09-08). Reproduce el PDF de julio de 2010, la última versión del texto que se conserva como
texto; el libro de la Diputación aún no se ha podido consultar (ver `TODO.md`, T-01).

**https://jtpadilla.github.io/santjoanslibro/** · repositorio [github.com/jtpadilla/santjoanslibro](https://github.com/jtpadilla/santjoanslibro). Forma parte de la familia de sitios de la autora:
[franciscajulianquerol.es](https://franciscajulianquerol.es/). El visor del pavimento, nacido del mismo trabajo, es
[santjoans.es](https://santjoans.es/).

## Qué hay aquí

| | |
|---|---|
| `source/` | Los originales, intocables: el PDF de julio de 2010 (58 págs., el texto de esta edición), el PDF de mayo de 2010 (47 págs., A4, entregado en la UJI, con las fotos a más resolución), la invitación de la Diputació a la presentación y las fotos de ese acto (`Llibre diputacio/`). |
| `content/` | **Los masters recuperados**: un `.md` por capítulo, `cataleg.yaml` con las 29 fichas del catálogo y `llibre.yaml` con los metadatos. |
| `assets/images/` | Las 13 fotografías y mapas del texto; los dos mapas del capítulo 1 se han redibujado en SVG desde OpenStreetMap (`extract/mapa/`) y el croquis del capítulo 2 con Gemini; los JPEG originales se conservan. `assets/cataleg/`: las 29 rajoles del catálogo. `assets/presentacio/`: la invitación y 11 fotos de la presentación de 2012. |
| `extract/` | Cómo se ha sacado todo de los PDF: `extract.sh` (Poppler), `images.py` (recortes) y `check.py` (comprobación palabra a palabra). |
| `site/` | El sitio web (Astro 7). Se publica en GitHub Pages con cada push a `main`. |
| `CLAUDE.md` | Cómo está montado todo y las convenciones del proyecto. |
| `NOTES.md` / `TODO.md` | Decisiones tomadas, hallazgos sobre el original y tareas pendientes (`T-nn`). |

## Reproducir la extracción

```bash
bash extract/extract.sh        # texto, XML y renders a 300 ppp de los dos PDF (poppler-utils)
python3 extract/images.py      # recorta las 42 imágenes a assets/ (Pillow)
python3 extract/check.py       # debe decir «distintas=0» y «desajustes de orden: 0»
```

## El sitio

```bash
cd site
npm install
npm run dev       # http://localhost:4321/
npm run build     # genera dist/ y copia los PDF originales a dist/original/
npm run preview
```

Astro 7, sin JavaScript de cliente salvo el botón de tema. Requiere Node ≥ 22.12.

## Licencias

- **Texto y fotografías:** © Francisca Julián Querol y archivo familiar, **CC BY-NC-ND 4.0** (ver `LICENSE-CONTINGUT.md`).
- **Código** (`extract/` y `site/`): **MIT** (ver `LICENSE`).

Edición digital a cargo de **Juan Tadeo Padilla Julián**, hijo de la autora, que es también el contacto para cualquier
corrección a través de este repositorio.
