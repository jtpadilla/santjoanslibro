import { getCollection, getEntry, render, type CollectionEntry } from 'astro:content';

export type Capitol = CollectionEntry<'llibre'>;
export type Fitxa = CollectionEntry<'cataleg'>;

export const llibre = (await getEntry('meta', 'llibre'))!.data;

/** Enllaç intern respectant `base` (el lloc pot viure a /repositori/). */
export function href(path: string): string {
  const base = import.meta.env.BASE_URL.replace(/\/$/, '');
  return `${base}/${path.replace(/^\//, '')}`;
}

/** "03-paviment" → "paviment" */
export function slugOf(entry: Capitol): string {
  return entry.id.replace(/^\d+-/, '');
}

/** Títol del capítol tal com apareix a l'original (majúscules), i una forma més llegible per a la navegació. */
export function titolCurt(title: string): string {
  const t = title.replace(/^\d+\.\s*/, '');
  if (t !== t.toUpperCase()) return t;
  const propis = ['Santjoans', 'Sanjoan', 'Cinctorres'];
  let curt = t.charAt(0) + t.slice(1).toLowerCase();
  for (const p of propis) curt = curt.replace(new RegExp(`\\b${p.toLowerCase()}\\b`, 'g'), p);
  return curt;
}

export function numeroCapitol(title: string): string | null {
  const m = title.match(/^(\d+)\./);
  return m ? m[1] : null;
}

export async function capitols(): Promise<Capitol[]> {
  const all = await getCollection('llibre');
  return all.sort((a, b) => a.data.order - b.data.order);
}

/** Les fitxes del catàleg en l'ordre del llibre (l'id és el número amb dos dígits). */
export async function cataleg(): Promise<Fitxa[]> {
  const all = await getCollection('cataleg');
  return all.sort((a, b) => a.id.localeCompare(b.id));
}

/** Etiquetes del catàleg, tal com les usa el llibre. */
export const campsFitxa: [keyof Fitxa['data'], string][] = [
  ['d', '[D.]'], ['m', '[M.]'], ['c', '[C.]'], ['f', '[F.]'], ['cr', '[Cr.]'], ['o', '[O.]'], ['lf', '[L.F.]'], ['ob', '[Ob.]'],
];

export interface Figura {
  n: number;            // ordre dins del text
  caption: string;
  file: string;
  capitol: Capitol;
}

/** Fotografies del text (no del catàleg), en ordre d'aparició, extretes del propi Markdown. */
export async function figures(): Promise<Figura[]> {
  const out: Figura[] = [];
  const re = /!\[(.*?)\]\(\.\.\/assets\/images\/(.*?)\)/g;
  for (const capitol of await capitols()) {
    for (const m of capitol.body!.matchAll(re)) {
      out.push({ n: out.length + 1, caption: m[1], file: m[2], capitol });
    }
  }
  return out;
}

export { render };
