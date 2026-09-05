#!/usr/bin/env python3
"""Fix common SEO issues in Loop Magazin static article HTML."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

SUFFIX = " — Loop Magazin"
MAX_TITLE = 60
BODY_MARKER = '<div class="md-body article-body"'


def shorten_title_tag(full: str) -> str:
    full = full.strip()
    if len(full) <= MAX_TITLE:
        return full

    if full.endswith(SUFFIX):
        head = full[: -len(SUFFIX)].strip()
    else:
        head = full

    budget = MAX_TITLE - len(SUFFIX)
    if budget < 10:
        return full[:MAX_TITLE]

    for sep in (" — ", ": ", " – ", " - "):
        if sep in head:
            cand = head.split(sep)[0].strip()
            if 15 <= len(cand) <= budget:
                return cand + SUFFIX

    if len(head) <= budget:
        return head + SUFFIX

    cut = head[: budget - 1].rsplit(" ", 1)[0]
    if len(cut) < 12:
        cut = head[: budget - 1]
    cut = cut.rstrip(".,;:") + "…"
    return cut + SUFFIX


def demote_body_h1(html: str) -> str:
    if BODY_MARKER not in html:
        return html
    head, tail = html.split(BODY_MARKER, 1)
    tail = re.sub(r"</h1>", "</h2>", tail, flags=re.I)
    tail = re.sub(r"<h1(\s[^>]*)?>", r"<h2\1>", tail, flags=re.I)
    return head + BODY_MARKER + tail


def fix_title_tag(html: str) -> str:
    match = re.search(r"<title>([^<]*)</title>", html, re.I)
    if not match:
        return html
    old = match.group(1)
    new = shorten_title_tag(old)
    if new == old:
        return html
    return html[: match.start(1)] + new + html[match.end(1) :]


def ensure_newsarticle(html: str) -> str:
    if "NewsArticle" in html or '"@type":"Article"' in html or '"@type": "Article"' in html:
        return html
    faq_match = re.search(
        r'<script type="application/ld\+json">(\{.*?"@type"\s*:\s*"FAQPage".*?\})</script>',
        html,
        re.S,
    )
    if not faq_match:
        return html

    title = re.search(r"<title>([^<]*)</title>", html, re.I)
    desc = re.search(r'<meta name="description" content="([^"]*)"', html, re.I)
    canonical = re.search(r'<link rel="canonical" href="([^"]*)"', html, re.I)
    og_image = re.search(r'<meta property="og:image" content="([^"]*)"', html, re.I)
    section = re.search(
        r'text-transform:uppercase">([^<]+)</span>\s*</header>',
        html,
        re.I,
    )

    if not (title and desc and canonical):
        return html

    headline = title.group(1).replace(SUFFIX, "").strip()
    news = {
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "@id": canonical.group(1) + "#article",
        "headline": headline,
        "description": desc.group(1),
        "image": [og_image.group(1)] if og_image else [],
        "datePublished": "2026-09-02",
        "dateModified": "2026-09-02",
        "author": {"@type": "Person", "name": "Loop Szerkesztőség"},
        "publisher": {"@id": "https://loopmagazin.hu/#publisher"},
        "mainEntityOfPage": {"@type": "WebPage", "@id": canonical.group(1)},
        "inLanguage": "hu",
        "articleSection": section.group(1) if section else "Compliance",
        "isAccessibleForFree": True,
    }
    import json

    block = f'<script type="application/ld+json">{json.dumps(news, ensure_ascii=False)}</script>\n'
    return html.replace(faq_match.group(0), block + faq_match.group(0), 1)


def fix_file(path: Path, *, pillar: bool = False) -> dict[str, bool]:
    html = path.read_text(encoding="utf-8")
    original = html
    h1_changed = demote_body_h1(html) != html
    html = demote_body_h1(html)
    title_changed = fix_title_tag(html) != html
    html = fix_title_tag(html)
    news_changed = False
    if pillar:
        patched = ensure_newsarticle(html)
        news_changed = patched != html
        html = patched
    changed = html != original
    if changed:
        path.write_text(html, encoding="utf-8")
    return {
        "changed": changed,
        "h1": h1_changed,
        "title": title_changed,
        "news": news_changed,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", help="Directory with cikk/*.html or HTML files")
    ap.add_argument("--pillars-only", action="store_true")
    args = ap.parse_args()
    root = Path(args.root)
    files = sorted(root.glob("*.html") if root.is_dir() else root.rglob("*.html"))

    pillar_names = {
        "eu-ai-act-magyar-kkv-utmutato-2026.html",
        "nis2-audit-magyar-cegeknek-checklista.html",
        "gdpr-nis2-ai-act-egyutt.html",
    }

    stats = {"files": 0, "changed": 0, "h1": 0, "title": 0, "news": 0}
    for f in files:
        is_pillar = f.name in pillar_names
        if args.pillars_only and not is_pillar:
            continue
        result = fix_file(f, pillar=is_pillar)
        stats["files"] += 1
        if result["changed"]:
            stats["changed"] += 1
            print(f"fixed {f.name}")
        stats["h1"] += int(result["h1"])
        stats["title"] += int(result["title"])
        stats["news"] += int(result["news"])

    print(
        f"\n{stats['files']} files, {stats['changed']} changed "
        f"(h1={stats['h1']}, title={stats['title']}, news={stats['news']})"
    )


if __name__ == "__main__":
    main()
