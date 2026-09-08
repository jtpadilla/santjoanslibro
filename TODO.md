# TODO.md — tareas pendientes

Numeradas `T-nn`. Se citan en los commits al resolverlas y el resultado se anota en `NOTES.md`.

---

## Abiertas

### T-01 · Revisar contra el libro de la Diputació (2012)
El usuario intentará localizar un ejemplar y escanearlo. Cuando llegue: guardarlo en `source/`, compararlo con el texto
de julio de 2010 (título, prólogo, posibles textos añadidos, orden y número de fichas, paginación de 78 págs.) y decidir
si esta edición sigue reproduciendo el PDF de 2010 o pasa al libro. Anotar diferencias en `NOTES.md` y en «Sobre esta
edició», y quitar el aviso de «Esborrany» de esa página.

### T-02 · Publicar: Pages y dominio
El repositorio público `jtpadilla/santjoanslibro` existe y `main` está subido (2026-09-08). Falta encender Pages con
origen GitHub Actions (el workflow ya está y corre con cada push; el `deploy` falla hasta entonces) y comprobar que
las páginas responden. Decidir si va en la subruta
`jtpadilla.github.io/santjoanslibro/` (como masosdemorella) o con dominio propio; el `href()` y `astro.config.mjs` ya
lo soportan. Actualizar la URL de cita en `edicio.astro` y en `README.md`.

### T-03 · Ficha en la portada franciscajulianquerol
Seguir «Cómo añadir un proyecto» de su `CLAUDE.md`: función `santjoanslibro()` en `tools/metriques.py` (¿qué se cuenta?:
1 texto de ~5.700 palabras, 13 fotografías, 29 fichas; no sumar las rajoles a `peces`, que ya cuenta santjoans),
`content/projectes/7-santjoanslibro.yaml`, portada, tipo (¿`llibre`, como masosdemorella?) y los textos que dicen
«cinco proyectos» → seis. También el enlace de vuelta desde santjoans («Información del proyecto») y desde masosdemorella.

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

(ninguna todavía)
