# NOTES.md — decisiones y hallazgos

Lo que se ha decidido y lo que se ha encontrado al montar esta edición. Las tareas pendientes están en `TODO.md`.

---

## 2026-09-08 · Arranque: el boceto

### De dónde sale el proyecto

La carpeta `santjoanslibro/` apareció con solo `raw/` (hoy `source/`): el trabajo de mayo de 2010 en PDF, la invitación
de la Diputació a la presentación del libro (23/11/2012) y 14 fotos. El usuario pidió «elegir el más moderno y preparar
un boceto con la tecnología que más se le acople», y que él intentará localizar una edición real para escanearla y revisar.

- **«El más moderno»** es el PDF de **julio de 2010** (`EstudioSantjoans.pdf`, que ya estaba publicado en
  santjoans.es/proyecto/ y se ha copiado a `source/`): 58 páginas maquetadas a 17 × 24 cm, generadas por Lari Orenga
  (metadato Author «orengad») para la web del visor. El de mayo es la entrega a la UJI (47 págs., A4, «Tutora: Pilar
  Escuder Mollón · 2º ciclo»).
- **La tecnología**: el patrón de masosdemorella (Astro 7, masters Markdown, `astro:assets`, Pages), porque es el otro
  libro de la autora reconstruido desde PDF y el `site/` se reaprovecha casi entero. Lo propio de este libro es el
  **catálogo**: 29 fichas con campos fijos, que van en YAML y se pintan con un componente, no en prosa.

### Diferencias entre las dos versiones de 2010

Mismo texto con retoques: la portada de julio pierde la tutora y el «2º ciclo»; la ficha 2 del catálogo pasa de «Bou
envestint sobre illeta diagonal i fulles» (mayo) a «Vaca sobre illeta diagonal i fulles» (julio); «isleta» → «illeta»
en las fichas 13 y 19. No se ha hecho una comparación exhaustiva (T-05).

### Las imágenes

Los dos PDF llevan cada foto **troceada en bandas horizontales** (Word): la portada de julio son 10 tiras de 678 × 88;
en mayo, 10 tiras de 2784 × 361. `pdfimages` no sirve; se recortan de los renders a 300 ppp con las posiciones de
`pdftohtml -xml` (unión de las bandas con el mismo `left`/`width`). Las de mayo son ~4 veces más grandes, así que **las
imágenes salen del PDF de mayo y el texto del de julio**. El mapa de comarcas pisa 12 unidades del mapa dels Ports en
la página 7 de mayo; se recorta con un margen extra (`FIGURES` admite un quinto valor).

Tamaños obtenidos: rajoles del catálogo ~1770 × 1770 px; fachada 1697 × 1130; escudos ~700 × 1060; portada 1275 × 1645.
Son fotos de 2010 hechas para el trabajo, no las del visor (que fotografió las 434 piezas aparte).

### El catálogo en YAML

`content/cataleg.yaml`: `id` («01»…«29», el orden del libro), `nom` (título corto de esta edición, del campo [O.]),
`pagina`, `imatge` y los campos `d m c f cr o lf ob`. Se transcriben tal cual, con sus variantes de puntuación
(«1790c.», «1790 c», «20,50x20,50», «21 x21 2 cm.») y sus erratas («morró», «enValència», «acuaticos»).

- **Ficha 5**: el original etiqueta las medidas como `[D.]` en vez de `[M.]`. En YAML no puede haber dos claves `d`,
  así que va como `m` y `check.py` lo sabe (`CORRECCIONS`). Es la única corrección al texto, y «Sobre esta edició» la cuenta.
- **Ficha 6**: el campo [Ob.] termina con «Rajola quadrada de dibuix complet, sense enllaços.», que parece un resto de
  copiar y pegar del original. Se deja.
- Los `cr: 1790.` de las fichas 7, 8 y 10 van entrecomillados: YAML los leía como el número 1790.0.
- Las fichas 28 y 29 no tienen todos los campos (la de fang cuit solo [D.]).

### La comprobación

`extract/check.py` compara multiconjunto y orden de palabras entre `extract/text/estudio/p05..p58.raw.txt` y
`content/*.md` + `cataleg.yaml` (insertado tras el capítulo 3). Da **5.712 palabras, 0 distintas, 0 desajustes**.
Detalles que costaron: las llamadas de nota van pegadas a la palabra en el PDF («poble1», «Cabrera.4») y se separan con
un regex que no toca «3x4» ni «21 x2»; los números de nota y de página a solas en su línea se descartan en el PDF; los
pies de foto, que son de esta edición, se descartan en el Markdown.

### Lo que el original no tiene y esta edición añade

- **Pies de foto**: el trabajo no los pone. Se han escrito 13 descripciones cortas (`![...]` en el Markdown).
- **Nombres cortos** de las fichas para navegar («Pavó reial», «Cuco (segona rajola)»…).
- Las dos auques fotografiadas en 3.4 son publicaciones actuales ajenas (*Auca de la Mare de Déu del Lledó*, *Auca de
  l'abat Oliba*), que el trabajo pone como ejemplo de auca; no son las auques de Laborda del siglo XVIII que cita.

### El libro de la Diputació (2012)

No está en `source/`. Datos de la ficha de librerías (todostuslibros.com, 8/9/2026): *Paviment ceràmic de la casa
Santjoans (Cinctorres)*, Servicio de Publicaciones Diputación de Castellón, col. Biblioteca Popular, 30/07/2012, 78 págs.,
20 × 12 cm, rústica, 8 €, ISBN 978-84-15301-12-7, «no disponible». 78 páginas a 20 × 12 frente a 58 a 17 × 24 sugiere otra
maqueta y quizá algún añadido. Presentado el 23/11/2012 a las 11.30 en la Sala de Premsa de la Diputació por los
diputados Héctor Folgado (Cultura) y Vicent Sales (Promoció Econòmica) con el alcalde Andreu Blesa, según la nota de
prensa que guarda `franciscabacket` («presentacion Diputacion fot periodico.docx»); en el acto se presentó también el
visor. Las citas de la nota de prensa que usa `/llibre/` salen de ahí.

### Las fotos de `source/Llibre diputacio/`

14 ficheros; 11 son del acto en la Diputació (fechas de fichero 23/11 y 12/2012; las `DSCF*` son de 480 × 360, muy
pequeñas, y las `Diputacio 0xx` de 2816 × 2112) y van a `assets/presentacio/` con nombre descriptivo. Las otras tres
**no son del acto** y se quedan solo en `source/`: `20131209_155948.jpg` (una comida, 9/12/2013), `ALCAÑIZ Y CASPE CON
LA UJI 040.JPG` (excursión de la UJI, 2013) e `IMG_2048.JPG` (un grupo en un patio de piedra, 2014, sin identificar).
Ninguna tiene EXIF. Los pies de `llibre.astro` describen lo que se ve; quién es cada persona queda por confirmar con
el usuario (T-04).

### Material relacionado en otros repositorios

- `santjoans/santjoans-web/public/proyecto/`: el mismo PDF de julio, dos presentaciones de 2010 en PDF, los diagramas
  del modelo y la página «Información del proyecto» con la historia (presentación en el Antic Escorxador el 11/8/2010).
- `franciscaineditos/md/Castelló/Paviment ceràmic/index.md`: texto de octubre de 2009, precursor del apartado 3.
- `franciscabacket/markdown/drive/Copias Pendrivers/Numero 02/Sant joans/`: los mismos PDF, la invitación y la nota de prensa.

---

## 2026-09-08 · Publicación

El usuario creó `jtpadilla/santjoanslibro` y subió el primer commit (111 ficheros) la misma noche del boceto. Pages se
encendió con `gh api -X POST repos/jtpadilla/santjoanslibro/pages -f build_type=workflow`; el `deploy` de los dos
primeros runs había fallado por no estar encendido, y el tercero, lanzado a mano con `gh workflow run`, publicó el
sitio en https://jtpadilla.github.io/santjoanslibro/ (subruta, sin dominio propio de momento: T-02). El `build` del
workflow no necesita nada fuera del repositorio: los masters, las imágenes y los PDF van dentro.

---

## 2026-09-09 · Los dos mapas del capítulo 1, redibujados (T-10)

### Por qué
Los dos mapas del apartado 1 no son de la autora: `02-mapa-comarques-de-castello.jpg` es un póster comercial
(«Castellón/Castelló, comarcas y municipios», con leyenda por población e inset de España) y `03-mapa-els-ports.jpg`
es un mapa de Wikimedia con nota «2005 CC-BY-SA», los dos borrosos ya en el PDF de mayo (1100 × 1025 y 900 × 809 px).
masosdemorella había redibujado su «Mapa dels Ports» en SVG desde OpenStreetMap (`extract/mapa/`), y su mapa tenía
**exactamente los mismos 13 municipios y rótulos** que el de este libro (los dos omiten Vilafranca). Se ha copiado esa
librería (`mapalib.py`, `text2path.mjs`) y se han escrito dos generadores.

### Datos: `extract/mapa/castello.osm.json` (versionado, ~1 MB)
`descarrega.py` pide a Overpass (reintentando en tres servidores: se satura a menudo) las ocho comarcas de la provincia
(relaciones `admin_level=7`: 1110951 els Ports, 1690971 l'Alt Maestrat, 1690974 el Baix Maestrat, 1111146 l'Alcalatén,
1690975 la Plana Alta, 1690976 la Plana Baixa, 1690973 l'Alt Palància, 1690972 El Alto Mijares), los municipios
(`admin_level=8`) de la caja que envuelve la provincia con margen (368, incluidos los vecinos de Teruel, Tarragona y
València) y la línea de costa. Coordenadas a 5 decimales y tramos simplificados a ~20 m. Descarga del 9/9/2026,
© colaboradores de OpenStreetMap, ODbL.
- Las relaciones de comarca de OSM no siempre listan sus municipios (tres tenían cero), así que cada municipio se
  asigna por su punto representativo dentro del polígono de la comarca. El punto es la media del **anillo mayor**: con
  la media de todos los puntos, Castelló de la Plana caía al mar, porque les Columbretes son suyas.
- Se guarda el id de cada tramo (`ref`) porque OSM comparte el mismo tramo entre los dos municipios que separa: con eso
  `castello.py` clasifica cada tramo como municipal, comarcal o exterior (provincia/costa) sin unir polígonos (no hay
  shapely; todo es biblioteca estándar).

### Decisión: Vilafranca en l'Alt Maestrat, como el libro
OSM sigue la demarcación oficial y pone Vilafranca en els Ports. Los dos mapas del libro la ponen en l'Alt Maestrat
(en el póster está en el color de esa comarca; el mapa dels Ports no la dibuja). Se sigue al libro (`LLIBRE` en
`castello.py`), como hizo masosdemorella, y «Sobre esta edició» lo dice.

### Contenido de cada mapa
- **02, comarcas**: las ocho comarcas rotuladas en valenciano (el póster iba en bilingüe: «Alt Millars/Alto Mijares»),
  els Ports destacada, Cinctorres (destacada), Morella y Castelló de la Plana, Terol/Tarragona/València, el mar con la
  costa real y les Columbretes, escala de 20 km. Sin la leyenda por población ni los 135 nombres de municipio, que
  en el original eran ilegibles. Límites municipales muy finos, comarcales medios, provincia y costa gruesos.
- **03, els Ports**: adaptación de `mapa_ports.py` de masosdemorella: los mismos 13 municipios y rótulos, Cinctorres
  destacada en vez de Morella, y los vecinos en trazo tenue con «Alt Maestrat» y «Baix Maestrat» rotulados, como el
  original. Escala de 5 km. Los tramos que quedan fuera del encuadre se omiten (el SVG pasaba de 300 a 124 KB).

### En el sitio
`rehype-book.mjs` ya venía preparado para SVG (ancho real del viewBox, enlace a tamaño completo), pero faltaban el
endpoint `src/pages/imatges/[file].ts` y `opentype.js` en `devDependencies`; se han copiado de masosdemorella.
`cataleg.astro` incluye ahora los `.svg` en la galería de fotografías del texto y marca «redibuixat per a esta edició».
Pies de figura con la atribución a OpenStreetMap (la ODbL obliga a citarla donde se muestre), y párrafo en «Sobre esta
edició» y en `LICENSE-CONTINGUT.md`. `check.py` sigue dando 0 y 0 (los pies no cuentan). Los JPEG originales siguen en
`assets/images/` y `images.py` los sigue extrayendo; no se usan en el sitio.

---

## 2026-09-09 · Croquis de la plaça Vella redibujado con Gemini (T-11)

El croquis del capítulo 2 (`04-croquis-placa-vella.jpg`, 1111 × 792, foto de un dibujo a mano) lo ha redibujado el
usuario con Gemini a partir de esa imagen: pergamino con los mismos edificios y rótulos (Ajuntament, L'Hostal, Torre del
Quartillo, Casa Sanjoans, Plaça Vella, Sala Vella de la Vila, Carrer Sol de la Vila). La imagen llegó como JPEG de
2424 × 1728 y se guarda reducida a 2000 px y calidad 88 (`04-croquis-placa-vella-redibuixat.jpg`, ~0,5 MB); el sufijo
`-redibuixat` es lo que `cataleg.astro` usa para marcarla en la galería (junto con los `.svg`). El original del PDF sigue
en `assets/images/` y `images.py` lo sigue extrayendo. Se ha comprobado a ojo que la versión nueva no cambia ni añade
nada al dibujo salvo la **rosa de los vientos**, que sitúa el norte arriba: el croquis original no tiene orientación,
aunque el texto dice que el carrer Sol de la Vila «està orientat direcció est i sud-est», lo que es compatible con ella.
Se dice en «Sobre esta edició».

---

## 2026-09-09 · Enlaces de vuelta con la familia (T-03)

La portada franciscajulianquerol.es ya tenía la ficha de este libro desde el 08/09. Se cierran los enlaces en sentido
contrario: el pie de `Base.astro` lleva la misma línea que masosdemorella («Tota l'obra de l'autora…») hacia
`franciscajulianquerol.es/ca/`; el visor santjoans.es tiene un tercer botón en su presentación, «Leer el estudio», que
apunta aquí; y masosdemorella enlaza a este libro en el pie y en «L'autora». La dirección enlazada es la de GitHub
Pages: si algún día hay dominio propio (T-02), hay que cambiarla en los tres sitios y en la ficha de la portada.
