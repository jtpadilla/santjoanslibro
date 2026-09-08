import { defineCollection, z } from 'astro:content';
import { file, glob } from 'astro/loaders';

// Els masters recuperats viuen a ../content (arrel del repositori), fora del projecte Astro.
export const collections = {
  // Un fitxer Markdown per capítol
  llibre: defineCollection({
    loader: glob({ pattern: '*.md', base: '../content' }),
    schema: z.object({
      title: z.string(),
      order: z.number(),
      pages: z.tuple([z.number(), z.number()]), // primera i última pàgina del PDF de juliol de 2010
    }),
  }),
  // Les 29 fitxes del catàleg (apartat 3.7), una entrada per rajola
  cataleg: defineCollection({
    loader: file('../content/cataleg.yaml'),
    schema: z.object({
      nom: z.string(),
      pagina: z.number(),
      imatge: z.string(),
      d: z.string(),
      m: z.string().optional(),
      c: z.string().optional(),
      f: z.string().optional(),
      cr: z.string().optional(),
      o: z.string().optional(),
      lf: z.string().optional(),
      ob: z.string().optional(),
    }),
  }),
  // Metadades de portada (entrada única "llibre")
  meta: defineCollection({
    loader: file('../content/llibre.yaml'),
    schema: z.object({
      titol: z.string(),
      subtitol: z.string(),
      autora: z.string(),
      llengua: z.string(),
      data_text: z.coerce.date(),
      data_pdf: z.coerce.date(),
      context: z.string(),
      portada_imatge: z.string(),
      edicio_impresa: z.object({
        titol: z.string(), autoria: z.string(), editorial: z.string(), lloc: z.string(), any: z.number(), data: z.string(),
        colleccio: z.string(), isbn13: z.string(), pagines: z.number(), dimensions: z.string(), enquadernacio: z.string(),
        preu: z.string(), estat: z.string(), url: z.string(), presentacio: z.string(), presentacio_lloc: z.string(),
      }),
    }),
  }),
};
