# Loop Magazin Web

Statikus HTML site + SEO/Generative AI optimalizálási eszközök a [loopmagazin.hu](https://loopmagazin.hu/) számára.

A Google hivatalos útmutatója szerint: **GEO/AEO = SEO**. Nincs szükség llms.txt-re, chunkolásra vagy AI-specifikus átírásra.

## Pillér-oldalak (generatív AI idézésre) — ÉLES

| URL | Téma |
|-----|------|
| https://loopmagazin.hu/cikk/eu-ai-act-magyar-kkv-utmutato-2026.html | EU AI Act magyar KKV-nak |
| https://loopmagazin.hu/cikk/nis2-audit-magyar-cegeknek-checklista.html | NIS2 audit checklista |
| https://loopmagazin.hu/cikk/gdpr-nis2-ai-act-egyutt.html | Integrált GDPR + NIS2 + AI Act |

Minden pillér-oldal tartalmaz: H1/H2 struktúrát, FAQ blokkot, FAQPage JSON-LD schema-t, canonical URL-t.

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

### Automatikus (GitHub Actions)

Állítsd be a repo Secrets-ben:

| Secret | Példa |
|--------|-------|
| `LOOPMAGazin_SSH_KEY` | privát SSH kulcs (PEM) |
| `LOOPMAGazin_DEPLOY_HOST` | `root@178.105.123.148` |
| `LOOPMAGazin_DEPLOY_PATH` | `/var/www/loopmagazin.hu` (opcionális) |

Majd: **Actions → Deploy loopmagazin.hu → Run workflow**, vagy push a `main`-re.

### Kézi

```bash
export LOOPMAGazin_DEPLOY_HOST=user@178.105.123.148
export LOOPMAGazin_SSH_KEY_FILE=~/.ssh/id_ed25519
export LOOPMAGazin_DEPLOY_PATH=/var/www/loopmagazin.hu
bash scripts/deploy-live.sh
```
