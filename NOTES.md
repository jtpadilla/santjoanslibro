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
