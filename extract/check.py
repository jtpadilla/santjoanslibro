#!/usr/bin/env python3
"""Comprueba que content/*.md y content/cataleg.yaml contienen exactamente las mismas palabras que el texto del
PDF de julio de 2010 (págs. 5-58: fuera portada, página en blanco e índice), descontando los números de página.
Compara multiconjuntos de palabras (las notas al pie cambian de sitio) y después el orden de las palabras del
cuerpo. Los pies de foto son de esta edición y no cuentan. Debe imprimir «distintas=0» y «desajustes de orden: 0».

Uso: python3 extract/check.py   (tras extract/extract.sh)."""
import difflib
import re
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
WORD = re.compile(r"[0-9A-Za-zÀ-ÿ·]+")
PAGINES = range(5, 59)
CAMPS = ["d", "m", "c", "f", "cr", "o", "lf", "ob"]
ETIQUETES = {"d": "[D.]:", "m": "[M.]:", "c": "[C.]:", "f": "[F.]:", "cr": "[Cr.]:", "o": "[O.]:", "lf": "[L.F.]:", "ob": "[Ob.]:"}
# Erratas del original que el YAML no puede reproducir (dos claves iguales): la ficha 5 etiqueta las medidas como [D.]
CORRECCIONS = {"05": {"m": "[D.]:"}}


def words(s):
    return Counter(w.lower() for w in WORD.findall(s))


def text_pdf():
    parts = []
    for i in PAGINES:
        t = (ROOT / f"extract/text/estudio/p{i:02d}.raw.txt").read_text(encoding="utf-8")
        t = re.sub(r"^\s*\d{1,2}\s*$", "", t, flags=re.M)              # número de página o de nota, solo en su línea
        t = re.sub(r"(?<=[A-Za-zÀ-ÿ”’.\]])(?<!x)(\d)\b(?!\d)", r" \1", t)  # llamada de nota pegada a la palabra (no «3x4»)
        parts.append(t)
    return "\n".join(parts)


def neteja_md(t, notes=None):
    """Markdown → texto plano comparable. Las llamadas de nota quedan como número suelto (así están en el PDF);
    las definiciones se quitan (y se guardan en `notes` si se pide)."""
    t = re.sub(r"^---.*?---", "", t, flags=re.S)                        # frontmatter
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", t)                           # figuras (pies de esta edición)
    t = re.sub(r"<[^>]+>", "", t)                                       # html (anclas, <dl> de la leyenda)
    for m in re.finditer(r"^\[\^(\d+)\]: (.*)$", t, flags=re.M):
        if notes is not None:
            notes.append(m.group(2))
    t = re.sub(r"^\[\^\d+\]: .*$", "", t, flags=re.M)                   # definiciones de nota
    t = re.sub(r"\[\^(\d+)\]", r" \1", t)                                # llamadas de nota
    return t


def text_cataleg():
    """El catálogo, ficha a ficha en el orden del libro, con las etiquetas [D.]… que sí están en el PDF."""
    out = []
    for fitxa in yaml.safe_load((ROOT / "content/cataleg.yaml").read_text(encoding="utf-8")):
        for camp in CAMPS:
            if camp in fitxa:
                etiqueta = CORRECCIONS.get(fitxa["id"], {}).get(camp, ETIQUETES[camp])
                out.append(f"{etiqueta} {fitxa[camp]}")
    return "\n".join(out)


def text_md(notes=None):
    out = []
    for f in sorted((ROOT / "content").glob("*.md")):
        out.append(neteja_md(f.read_text(encoding="utf-8"), notes))
        if f.name.startswith("03-"):
            out.append(text_cataleg())                                  # el catálogo cierra el capítulo 3
    return "\n".join(out)


notes = []
pdf_t, md_t = text_pdf(), text_md(notes)
pdf, md = words(pdf_t), words(md_t + "\n" + "\n".join(notes))   # las notas cuentan, estén donde estén
diff = {w: (pdf[w], md[w]) for w in set(pdf) | set(md) if pdf[w] != md[w]}
print(f"palabras PDF={sum(pdf.values())}  MD={sum(md.values())}  distintas={len(diff)}")
for w, (a, b) in sorted(diff.items(), key=lambda x: -abs(x[1][0] - x[1][1]))[:40]:
    print(f"  {w!r:30} pdf={a} md={b}")

# --- orden de las palabras del cuerpo (sin notas al pie, que en el Markdown van al final del capítulo) --------
md_seq = [w.lower() for w in WORD.findall(md_t)]
pdf_seq = [w.lower() for w in WORD.findall(pdf_t)]
note_words = Counter(w.lower() for n in notes for w in WORD.findall(re.sub(r"[*_\\]", "", n)))

sm = difflib.SequenceMatcher(a=pdf_seq, b=md_seq, autojunk=False)
problems = 0
for op, i1, i2, j1, j2 in sm.get_opcodes():
    if op == "equal":
        continue
    a, b = pdf_seq[i1:i2], md_seq[j1:j2]
    if op == "delete" and all(note_words[w] > 0 for w in a):
        continue  # nota al pie: esperado
    problems += 1
    if problems <= 25:
        print(f"  {op:8} pdf[{i1}]: {' '.join(a)[:70]!r}  |  md: {' '.join(b)[:70]!r}")
print(f"desajustes de orden: {problems}")
