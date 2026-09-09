# CLAUDE.md — Proyecto santjoanslibro

Punto de entrada para Claude Code en cualquier sesión y en cualquier máquina. Leer este fichero completo antes de tocar nada.

---

## Qué es este proyecto

Edición digital del estudio de **Francisca Julián Querol** («Paquita», Cinctorres, 1945) sobre el **pavimento cerámico
zoomórfico del salón noble del Palau Santjoans** de Cinctorres: *Paviment ceràmic de la casa Sanjoan i Sousa.
Cinctorres*. Fue su trabajo de final del segundo ciclo de la Universitat per a Majors (UJI, tutora Pilar Escuder
Mollón, mayo de 2010) y la **Diputació de Castelló lo publicó en libro en 2012** con el título *Paviment ceràmic de la
casa Santjoans (Cinctorres)* (col. Biblioteca Popular, 78 págs., 20 × 12 cm, ISBN 978-84-15301-12-7; presentado el
23/11/2012 en la Sala de Premsa de la Diputació).

Es el **séptimo repositorio** de la familia de la autora (ver «Proyectos hermanos»). Sigue el modelo de
**masosdemorella**: un libro reconstruido desde PDF a masters abiertos (Markdown + YAML + JPEG) y un sitio Astro que
solo es una vista de esos masters.

**Estado: BOCETO** (2026-09-08, primera sesión). Reproduce el PDF de julio de 2010. **El libro de la Diputación no se ha
podido consultar**: el usuario intentará localizar un ejemplar para escanearlo y revisar esta edición contra él (T-01).
Publicado en **https://jtpadilla.github.io/santjoanslibro/** (repositorio público `jtpadilla/santjoanslibro`, Pages con
origen GitHub Actions, desde el 2026-09-08). Falta la ficha en la portada (T-03) y decidir si tendrá dominio propio (T-02).

Idioma del libro: valenciano. UI del sitio: valenciano (como masosdemorella). Idioma de trabajo con el usuario: **castellano**.
No se modifica el contenido del libro: la reconstrucción es fiel al PDF (erratas y todo, salvo lo anotado en `NOTES.md`).

### Proyectos hermanos (clonados al lado de este, en `~/IdeaProjects/francisca/`)

| Repositorio | Qué es | Relación con este |
|---|---|---|
| franciscajulianquerol | La portada: franciscajulianquerol.es. Indexa los proyectos y cuenta sus cifras con `tools/metriques.py` | Hay que añadirle este proyecto (T-03), siguiendo su «Cómo añadir un proyecto» |
| santjoans | El visor del pavimento (santjoans.es), 434 piezas en tres tamaños | Nació del mismo trabajo; su `santjoans-web/public/proyecto/EstudioSantjoans.pdf` es el PDF de julio que aquí es `source/` |
| masosdemorella | El otro libro de la autora, reconstruido desde PDF | **El modelo de este repo**: `site/` se copió de ahí y se adaptó |
| franciscaineditos | Escritos inéditos | `md/Castelló/Paviment ceràmic/index.md` es un texto de 2009 precursor de este trabajo |
| franciscabacket | Fondo en bruto, no publicado | `markdown/drive/Copias Pendrivers/Numero 02/Sant joans/` tiene el mismo material que `source/` más la nota de prensa de la presentación |

Consultar sus `CLAUDE.md` antes de reinventar decisiones.

---

## Diagnóstico de los PDF (hecho 2026-09-08, no repetir)

- **Dos versiones del trabajo, ambas con capa de texto** (no son escaneos; no hace falta OCR):
  - `source/treball Sanjoan.pdf` — **mayo de 2010**, 47 págs., A4, Ghostscript. Portada con «Tutora: Pilar Escuder
    Mollón · 2º ciclo». **Imágenes a ~300 ppp** (las rajoles del catálogo, ~1770 px de lado).
  - `source/EstudioSantjoans.pdf` — **julio de 2010**, 58 págs., 17 × 24 cm, Acrobat Distiller, metadato Author
    «orengad» (Lari Orenga, que maquetó los documentos de santjoans.es). Mismo texto con retoques menores. Imágenes a
    ~150 ppp. **Es el texto de esta edición** («el más moderno»); las imágenes se toman del de mayo.
- **Las imágenes van troceadas en bandas horizontales** en los dos PDF (exportación de Word): `pdfimages` da decenas de
  tiras de 60-90 px de alto. Se recortan de los renders a 300 ppp con las posiciones de `pdftohtml -xml` (`extract/images.py`).
- Paginación del PDF de julio: física = impresa (la 1 es la portada sin número; la 2, en blanco; 3, índice; 5, pròleg…).
  El índice del propio PDF coincide con ella.
- Estructura: pròleg, 4 capítulos (Situació; Naixement de la casa Santjoans con 6 apartados; Paviment con 7 apartados,
  el 3.7 es el catálogo de 29 fichas a una por página, págs. 27-55; Bibliografia). 7 notas al pie, numeradas de corrido.
  Sin pies de foto en el original. ~5.700 palabras.
- Correspondencia de imágenes mayo ↔ julio: en la tabla `FIGURES` de `extract/images.py`. El orden del catálogo es el
  mismo en las dos versiones (comprobado por el campo [O.] de cada ficha).
- Título inconsistente en el original: portada «Sanjoan i Sousa», índice «Naixement de la casa Sanjoan», capítulo
  «Naixement de la casa Santjoans», 2.2 «Sanjoan»/«Santjoan». Se respeta cada sitio.

---

## Tecnología

**Astro 7** + Markdown/YAML + `astro:assets` + GitHub Actions → Pages, igual que masosdemorella (misma versión, mismo
`global.css` con tokens claro/oscuro, mismo `rehype-book.mjs` para las figuras). Diferencias con masosdemorella:
- **El catálogo es datos, no prosa**: `content/cataleg.yaml`, una entrada por rajola con los campos `d m c f cr o lf ob`
  (las letras del propio libro). El sitio lo pinta con `site/src/components/Fitxa.astro` al final del capítulo 3 y como
  galería en `/cataleg/`. Esto es lo que permitirá, más adelante, enlazar cada ficha con su pieza en el visor (T-06).
- **Los dos mapas del capítulo 1 son SVG generados** (`extract/mapa/`, T-10), como el mapa dels Ports de masosdemorella,
  del que se copió la librería. Los originales del PDF eran un mapa comercial y uno de Wikimedia, ilegibles.
- **Sin Pagefind** (5.700 palabras no lo justifican) y **sin EPUB/PDF generado** (`scripts/llibre.mjs` no se copió). Si
  algún día se quieren, copiarlos de masosdemorella.
- Página **«El llibre»** (`/llibre/`): la edición de la Diputación, la invitación y las fotos de la presentación de 2012.

---

## Estructura del repositorio

```
source/                     originales (intocables): los dos PDF, la invitación (PDF) y Llibre diputacio/ (14 fotos)
extract/extract.sh          texto por página, XML de posiciones y renders a 300 ppp de los dos PDF → extract/{text,xml,render}/ (ignorados)
extract/images.py           recorta las 13 fotos del texto y las 29 rajoles a assets/ (tabla FIGURES; toma el PDF de mayo)
extract/check.py            comprueba palabra a palabra content/ + cataleg.yaml contra el PDF de julio. DEBE dar 0 y 0.
extract/mapa/               los dos mapas SVG del capítulo 1: descarrega.py (Overpass → castello.osm.json, VERSIONADO, ~1 MB),
                            castello.py (división comarcal del libro: Vilafranca en l'Alt Maestrat; clasifica los tramos),
                            mapa_comarques.py y mapa_ports.py, mapalib.py + text2path.mjs (copiados de masosdemorella).
                            `extract/mapa/genera.sh [--png]` (o `npm run mapes` en site/) los regenera; opentype.js viene con `npm install`.
content/NN-slug.md          MASTERS: un .md por capítulo. Frontmatter title/order/pages; anclas <a id="pNN" class="pag" data-p="NN">;
                            figuras ![pie de esta edición](../assets/images/NN-x.jpg); notas [^n] al final; la leyenda del 3.7 es un <dl>.
content/cataleg.yaml        las 29 fichas (id "01".."29", nom de esta edición, pagina, imatge, d m c f cr o lf ob)
content/llibre.yaml         metadatos: título, autora, fechas, contexto, edicio_impresa (datos de la Diputación)
assets/images/              13 fotos/mapas del texto, NN-descripcion.jpg (orden de aparición); 02 y 03 se publican como .svg
                            (generados) y 04 como 04-croquis-placa-vella-redibuixat.jpg (Gemini, T-11); los .jpg del PDF se
                            conservan sin usar (images.py los sigue regenerando)
assets/cataleg/             29 rajoles, NN-nom.jpg (orden del catálogo)
assets/presentacio/         00-invitacio.jpg (render del PDF) + 11 fotos del acto de 2012 (las 3 restantes de source/ no son del acto)
site/                       Astro 7. src/pages: index, [slug], cataleg, llibre, edicio, autora, robots.txt, imatges/[file] (sirve los SVG
                            a tamaño completo). src/components/Fitxa.astro.
                            src/lib/llibre.ts (capitols, cataleg, figures, href). content.config.ts: colecciones llibre, cataleg, meta.
.github/workflows/deploy.yml  build + Pages en cada push a main (copiado de masosdemorella)
```

Convención de este repo: **el texto se transcribió a mano** desde `extract/text/estudio/*.txt` (5.700 palabras no
justifican un `to_markdown.py` como el de masosdemorella) y `check.py` garantiza la fidelidad. Cualquier corrección al
texto se hace en `content/` **y** se anota en `NOTES.md`; si `check.py` deja de dar 0, o es un error o hay que
enseñarle la excepción (como `CORRECCIONS`).

---

## Flujo de trabajo

```bash
bash extract/extract.sh && python3 extract/images.py && python3 extract/check.py   # reproducir todo desde source/
cd site && npm install && npm run build        # dist/ + dist/original/*.pdf
npm run dev                                    # http://localhost:4321/
```

Capturas de comprobación: `google-chrome --headless=new --screenshot=x.png --window-size=1280,3000 URL` contra `npx astro preview`.

---

## Convenciones

- Commits y ficheros en castellano; contenido del libro en el valenciano original, sin normalizar ortografía.
- Todo hallazgo o decisión va a `NOTES.md`; las tareas, a `TODO.md` numeradas `T-nn`, y se citan en los commits al resolverlas.
- Nada derivado (`dist/`, `node_modules/`, `extract/{text,xml,render}/`) al repositorio.
- Los pies de foto y los `nom` de las fichas son de esta edición, y así lo dice «Sobre esta edició». No inventar nada más.
