# Loop Magazin Web

Statikus HTML site + SEO/Generative AI optimalizálási eszközök a [loopmagazin.hu](https://loopmagazin.hu/) számára.

A Google hivatalos útmutatója szerint: **GEO/AEO = SEO**. Nincs szükség llms.txt-re, chunkolásra vagy AI-specifikus átírásra.

## Pillér-oldalak (generatív AI idézésre)

| Fájl | Téma |
|------|------|
| `cikk/eu-ai-act-kkv-utmutato-2026.html` | EU AI Act magyar KKV-nak |
| `cikk/nis2-audit-magyar-cegek.html` | NIS2 audit checklista |
| `cikk/gdpr-nis2-ai-act-egyutt.html` | Integrált GDPR + NIS2 + AI Act |

Minden pillér-oldal tartalmaz: H1/H2 struktúrát, FAQ blokkot, Article + FAQPage JSON-LD schema-t, canonical URL-t.

## Eszközök

```bash
# SEO audit meglévő HTML fájlokon
python3 scripts/seo-audit.py .

# Sitemap generálás
python3 scripts/generate-sitemap.py --base-url https://loopmagazin.hu
```

## Cloud Agent környezet

A `.cursor/environment.json` beállítja a `loopmagazin.hu` egress hozzáférést.

## Deploy

A meglévő deploy folyamatba illeszd be az új `cikk/*.html` fájlokat és frissítsd a `sitemap.xml`-t.
