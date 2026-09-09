# TODO.md — tareas pendientes

Numeradas `T-nn`. Se citan en los commits al resolverlas y el resultado se anota en `NOTES.md`.

---

## Abiertas

### T-01 · Revisar contra el libro de la Diputació (2012)
El usuario intentará localizar un ejemplar y escanearlo. Cuando llegue: guardarlo en `source/`, compararlo con el texto
de julio de 2010 (título, prólogo, posibles textos añadidos, orden y número de fichas, paginación de 78 págs.) y decidir
si esta edición sigue reproduciendo el PDF de 2010 o pasa al libro. Anotar diferencias en `NOTES.md` y en «Sobre esta
edició», y quitar el aviso de «Esborrany» de esa página.

### T-02 · ¿Dominio propio?
Publicado en la subruta `jtpadilla.github.io/santjoanslibro/` (ver «Resueltas», T-09). Queda decidir si, como
santjoans.es o franciscajulianquerol.es, tendrá dominio propio; `href()` y `astro.config.mjs` ya lo soportan
(`SITE_URL`, `BASE_PATH`, `public/CNAME`). Si cambia, actualizar la URL de cita en `edicio.astro` y en `README.md`.

### T-04 · Confirmar quién sale en las fotos de la presentación
Los pies de `llibre.astro` describen lo que se ve (la taula, los diputados, el público). Preguntar al usuario los
nombres y si las tres fotos apartadas (comida de 2013, Alcañiz y Caspe, IMG_2048) tienen que ver con el libro.

### T-05 · Comparación exhaustiva mayo ↔ julio 2010
Se han visto retoques sueltos (tutora en portada, «bou» → «vaca», «isleta» → «illeta»). Un `diff` palabra a palabra de
los dos PDF diría si hay más, y valdría para «Sobre esta edició».

### T-06 · Enlazar cada ficha del catálogo con su pieza en el visor santjoans.es
Las 29 rajoles catalogadas están entre las 434 del visor (`santjoans-web/public/piezes/piezes.json`, con posiciones).
Identificarlas (a ojo, o por similitud de imagen contra `public/piezes/550/`) y añadir a `cataleg.yaml` un campo
`peca` con el id del visor, para que `Fitxa.astro` enlace a la pieza. Es la razón de que el catálogo sea YAML.

### T-07 · Revisión visual página a página
Cotejar cada capítulo con `extract/render/estudio/p-NN.png`: cursivas, saltos de párrafo, sangrías de las listas del
apartado 3.5 y de la bibliografía. `check.py` garantiza las palabras, no el formato.

### T-08 · Fotos pequeñas de la presentación
Siete de las once fotos del acto (`DSCF*`) son de 480 × 360 px, copias reducidas. Preguntar si existen los originales
(la nota de prensa del backet solo trae miniaturas) y, si aparecen, sustituirlas en `assets/presentacio/`.

---

## Resueltas

### T-03 · Ficha en la portada franciscajulianquerol · 2026-09-09
La ficha la hizo la portada el 2026-09-08 (su T-11): función `santjoanslibro()` en su `tools/metriques.py` (1 texto,
13 fotografías, 29 fichas; las rajoles no se suman), ficha `3-santjoanslibro.yaml` en tercer lugar, tipo `llibre`.
Hoy, los enlaces de vuelta (su T-12): el pie de cada página de este sitio enlaza a la portada, como masosdemorella;
santjoans tiene un botón «Leer el estudio» en su presentación, en los cuatro idiomas; masosdemorella enlaza al libro en
el pie y en «L'autora».

### T-11 · Croquis de la plaça Vella redibujado · 2026-09-09
El usuario generó con Gemini una versión del croquis a mano del capítulo 2 (mismos edificios y rótulos, sobre pergamino,
con rosa de los vientos añadida). Publicada como `assets/images/04-croquis-placa-vella-redibuixat.jpg`; el original del
PDF se conserva. Anotado en el pie, en «Sobre esta edició» y en `LICENSE-CONTINGUT.md`.

### T-10 · Redibujar los dos mapas del capítulo 1 en SVG · 2026-09-09
Los mapas del PDF (un póster comercial de las comarcas y un mapa de Wikimedia dels Ports) eran ilegibles. Se han
sustituido por `assets/images/02-mapa-comarques-de-castello.svg` y `03-mapa-els-ports.svg`, generados en `extract/mapa/`
desde OpenStreetMap con la librería de masosdemorella, siguiendo al libro en poner Vilafranca en l'Alt Maestrat. Los
JPEG originales se conservan. Detalles en `NOTES.md`.

### T-09 · Publicar el repositorio y encender Pages · 2026-09-08
Repositorio público `jtpadilla/santjoanslibro` (primer commit del usuario), Pages con origen **GitHub Actions**
(`build_type=workflow`) y HTTPS forzado. El primer `deploy` falló hasta encender Pages, como en la portada; relanzado
el workflow, las diez páginas responden 200, `/no-existe/` da 404 y los PDF originales se sirven en `/original/`.
**https://jtpadilla.github.io/santjoanslibro/**
