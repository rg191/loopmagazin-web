#!/usr/bin/env python3
"""Generate production-ready Loop Magazin pillar pages matching live site template."""

from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "cikk"

HEADER = """<header style="border-bottom:1px solid #000;padding:16px 24px;display:flex;align-items:center;gap:12px;flex-wrap:wrap">
  <a href="/" style="display:inline-flex;align-items:center;text-decoration:none;line-height:0" aria-label="Loop Magazin — főoldal">
    <img src="/assets/loop/nav-lockup-light.svg?v=looplogo6" alt="Loop Magazin" width="181" height="40" style="height:32px;width:auto;display:block">
  </a>
  <span style="color:#6e6e6e;margin:0 4px">·</span>
  <span style="color:#15506b;font-size:12px;font-weight:600;letter-spacing:.1em;text-transform:uppercase">{section}</span>
</header>"""

FOOTER = """<footer style="margin-top:40px;padding-top:24px;border-top:1px solid #d4d4d4;font-size:14px;display:flex;flex-direction:column;gap:10px">
  <a href="https://www.linkedin.com/sharing/share-offsite/?url={share_url}" target="_blank" rel="noopener noreferrer" style="display:inline-block;color:#0a66c2;font-weight:600;text-decoration:none;border:1px solid #0a66c2;border-radius:2px;padding:8px 16px;width:fit-content">Megosztás LinkedInen →</a>
  <a href="https://loopmagazin.hu/?article={slug}" style="color:#15506b;font-weight:600;text-decoration:none">Olvasd a Loop Magazin felületén →</a>
  <a href="/" style="color:#6e6e6e;font-size:13px;text-decoration:none">← Vissza a címlapra</a>
</footer>"""


def page(
    slug: str,
    title: str,
    description: str,
    section: str,
    keywords: str,
    image: str,
    read_mins: int,
    body_html: str,
    faq: list[tuple[str, str]],
) -> str:
    url = f"https://loopmagazin.hu/cikk/{slug}.html"
    share = url.replace(":", "%3A").replace("/", "%2F") + "%3Futm_source%3Dshare%26utm_medium%3Dlinkedin%26utm_campaign%3Darticle-share%26utm_content%3D" + slug

    news = {
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "@id": f"{url}#article",
        "headline": title,
        "description": description,
        "image": [image],
        "datePublished": "2026-09-02",
        "dateModified": "2026-09-02",
        "author": {"@type": "Person", "name": "Loop Szerkesztőség"},
        "publisher": {"@id": "https://loopmagazin.hu/#publisher"},
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "inLanguage": "hu",
        "articleSection": section,
        "keywords": keywords,
        "isAccessibleForFree": True,
    }
    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in faq
        ],
    }

    return f"""<!DOCTYPE html>
<html lang="hu">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Loop Magazin</title>
<meta name="description" content="{description.replace('"', '&quot;')}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Loop Magazin">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description.replace('"', '&quot;')}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="hu_HU">
<meta property="og:image" content="{image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/colors_and_type.css">
<link rel="stylesheet" href="/site.css">
<script type="application/ld+json">{json.dumps(news, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
</head>
<body style="margin:0;background:#fff;color:#000;font-family:Inter Tight,system-ui,sans-serif">
{HEADER.format(section=section)}
<main style="max-width:720px;margin:0 auto;padding:40px 24px 80px">
  <p style="font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#6e6e6e;margin:0 0 16px">2026-09-02 · {read_mins} perc olvasás · Loop Szerkesztőség</p>
  <h1 style="font-family:Playfair Display,Georgia,serif;font-size:clamp(32px,5vw,48px);line-height:1.1;margin:0 0 20px">{title}</h1>
  <p style="font-size:18px;line-height:1.5;color:#1a1a1a;margin:0 0 32px">{description}</p>
  <figure style="margin:0 0 32px"><img src="{image}" alt="{title}" style="width:100%;height:auto"></figure>
  <div class="md-body article-body" style="font-size:17px;line-height:1.65">{body_html}</div>
  {FOOTER.format(share_url=share, slug=slug)}
</main>
</body>
</html>
"""


PAGES = [
    {
        "slug": "eu-ai-act-kkv-utmutato-2026",
        "title": "EU AI Act magyar KKV-nak — teljes útmutató 2026",
        "description": "Az EU AI Act magyar vállalkozásoknak: kockázati kategóriák, NMHH felügyelet, konkrét lépések és határidők — Big4-zsargon nélkül.",
        "section": "Compliance",
        "keywords": "EU AI Act, mesterséges intelligencia, KKV, NMHH, megfelelés",
        "image": "https://loopmagazin.hu/assets/articles/ai-act-magas-kockazat-konzultacio.jpg",
        "read_mins": 15,
        "faq": [
            ("Ki kötelezett az EU AI Act alá Magyarországon?", "Minden szervezet, amely AI-rendszert fejleszt, telepít vagy használ üzleti folyamatban — függetlenül a székhelyétől."),
            ("Mikor lép teljes mértékben hatályba?", "2026. augusztus 2-tól a magas kockázatú AI-rendszerekre vonatkozik a teljes keret."),
            ("Ki felügyeli Magyarországon?", "Az NMHH (Nemzeti Média- és Hírközlési Hatóság)."),
        ],
        "body": """
<p class="dropcap">Ha Ön magyar KKV-vezető vagy középvezető, és AI-eszközöket használ — ChatGPT, HR-szűrés, chatbot, automatizált döntéshozatal — az EU AI Act Önt is érinti. Ez az útmutató érthető nyelven, gyakorlati lépésekkel mutatja be, mit kell tennie.</p>
<h2>Mi változott 2026-ban?</h2>
<p>2026. augusztus 2-tól a magas kockázatú AI-rendszerekre (HR-szűrés, hitelbírálat, kritikus infrastruktúra) vonatkozik a teljes megfelelési keret. Az NMHH megkezdte a felügyeletet.</p>
<h2>Kockázati kategóriák</h2>
<ul>
<li><strong>Tiltott:</strong> social scoring, manipulatív AI.</li>
<li><strong>Magas kockázat:</strong> HR-szűrés, hitelbírálat — teljes megfelelés.</li>
<li><strong>Korlátozott:</strong> chatbot — átláthatósági kötelezettség.</li>
<li><strong>Minimális:</strong> spam-szűrő, ajánlórendszer.</li>
</ul>
<h2>Konkrét lépések</h2>
<ol>
<li>AI-eszköz leltár (beleértve az árnyék-AI-t is).</li>
<li>Kockázati besorolás rendszerenként.</li>
<li>Belső AI-használati szabályzat.</li>
<li>Dokumentáció magas kockázatnál.</li>
<li>Képzés az érintett munkatársaknak.</li>
</ol>
<h2>Gyakori kérdések</h2>
<h3>Ki kötelezett?</h3>
<p>Minden szervezet, amely AI-rendszert fejleszt, telepít vagy használ.</p>
<h3>Mikor a határidő?</h3>
<p>2026. augusztus 2. — magas kockázatú rendszerek.</p>
<p>Kapcsolódó: <a href="https://loopmagazin.hu/cikk/nis2-audit-magyar-cegek.html">NIS2 audit checklista</a> · <a href="https://loopmagazin.hu/cikk/gdpr-nis2-ai-act-egyutt.html">GDPR + NIS2 + AI Act együtt</a></p>
""",
    },
    {
        "slug": "nis2-audit-magyar-cegek",
        "title": "NIS2 audit magyar cégeknek — checklista és határidők",
        "description": "NIS2 audit magyar KKV-knak: ki érintett, mit vár az SZTFH, konkrét checklista — gyakorlati útmutató.",
        "section": "Kibervédelem",
        "keywords": "NIS2, audit, SZTFH, kiberbiztonság, KKV",
        "image": "https://res.cloudinary.com/djcymhcjf/image/upload/f_auto,q_auto/v1782827962/30_yincih.png",
        "read_mins": 12,
        "faq": [
            ("Ki kötelezett NIS2 auditra Magyarországon?", "A LXIX. törvény hatálya alá tartozó szervezetek — kritikus és fontos szektorokban."),
            ("Mi történik lejárt határidő után?", "Az SZTFH ellenőrizhet; a nyilvántartás dátuma nem helyettesíti a lezárt auditot."),
        ],
        "body": """
<p class="dropcap">A NIS2 nem IT-projekt — üzleti kockázatkezelés. Ha magyar cégvezetőként a kiberbiztonsági törvény hatálya alá tartozik, az audit nem adminisztratív formalitás, hanem bizonyítható megfelelés.</p>
<h2>NIS2 audit checklista</h2>
<ol>
<li>Kockázatelemzés dokumentálva</li>
<li>Incidenskezelési terv és gyakorlat</li>
<li>Hozzáférés-kezelés</li>
<li>Biztonsági mentések és helyreállítás</li>
<li>Alkalmazottak kiberbiztonsági képzése</li>
<li>Beszállítói lánc kockázatkezelése</li>
<li>Bejelentési folyamat incidens esetén</li>
</ol>
<h2>Mit vár az SZTFH?</h2>
<p>Strukturált dokumentációt, nem sablon-dobozokat. A partner sem kérdezi meg, van-e NIS2-d — bizonyítékot kér.</p>
<p>Kapcsolódó: <a href="https://loopmagazin.hu/cikk/nis2-audit-utan-mit-bizonyits.html">Mit vár az SZTFH audit után</a> · <a href="https://loopmagazin.hu/cikk/eu-ai-act-kkv-utmutato-2026.html">EU AI Act útmutató</a></p>
""",
    },
    {
        "slug": "gdpr-nis2-ai-act-egyutt",
        "title": "GDPR + NIS2 + AI Act együtt — mit kell tudnia egy magyar vezetőnek",
        "description": "Hogyan illeszkedik össze a GDPR, NIS2 és EU AI Act egy magyar KKV-nál? Prioritások és egy havi akcióterv.",
        "section": "Compliance",
        "keywords": "GDPR, NIS2, AI Act, megfelelés, integrált",
        "image": "https://loopmagazin.hu/assets/articles/ai-act-magas-kockazat-konzultacio.jpg",
        "read_mins": 10,
        "faq": [
            ("Melyik szabályozással kezdjek?", "GDPR alapok, ha nincs naprakész adatkezelési tájékoztató; utána NIS2 ha érintett; majd AI Act ha AI-t használ döntéshozatalban."),
        ],
        "body": """
<p class="dropcap">2026-ban a GDPR, NIS2 és EU AI Act egy közös szabályozási térben működik — egymásra épülő védelmi rétegek, nem három külön projekt.</p>
<h2>A három réteg</h2>
<ul>
<li><strong>GDPR:</strong> adatok védelme</li>
<li><strong>NIS2:</strong> rendszerek védelme</li>
<li><strong>AI Act:</strong> algoritmusok felelős használata</li>
</ul>
<h2>Egy havi akcióterv</h2>
<ol>
<li><strong>1. hét:</strong> AI-eszköz leltár + GDPR adatfolyam térkép</li>
<li><strong>2. hét:</strong> NIS2 gap-analízis (ha érintett)</li>
<li><strong>3. hét:</strong> AI kockázati besorolás + belső szabályzat</li>
<li><strong>4. hét:</strong> Dokumentáció összehangolása, képzés</li>
</ol>
<p>A Google hivatalos útmutatója szerint nincs szükség külön AI-fájlokra vagy tartalom-darabolásra — a minőségi, egyedi tartalom és a jó SEO alapok elegendők.</p>
<p>Kapcsolódó pillérek: <a href="https://loopmagazin.hu/cikk/eu-ai-act-kkv-utmutato-2026.html">AI Act</a> · <a href="https://loopmagazin.hu/cikk/nis2-audit-magyar-cegek.html">NIS2</a></p>
""",
    },
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for p in PAGES:
        html = page(
            p["slug"],
            p["title"],
            p["description"],
            p["section"],
            p["keywords"],
            p["image"],
            p["read_mins"],
            p["body"],
            p["faq"],
        )
        path = OUT / f"{p['slug']}.html"
        path.write_text(html, encoding="utf-8")
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
