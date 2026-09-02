#!/usr/bin/env python3
"""Generate sitemap.xml from HTML files in the site root."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring


def build_sitemap(root: Path, base_url: str) -> bytes:
    urlset = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    for html in sorted(root.rglob("*.html")):
        if ".git" in html.parts or "templates" in html.parts:
            continue
        rel = html.relative_to(root).as_posix()
        if rel == "index.html":
            loc = base_url.rstrip("/") + "/"
        else:
            loc = base_url.rstrip("/") + "/" + rel
        url = SubElement(urlset, "url")
        SubElement(url, "loc").text = loc
        SubElement(url, "lastmod").text = today

    return b'<?xml version="1.0" encoding="UTF-8"?>\n' + tostring(urlset, encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default="https://loopmagazin.hu")
    ap.add_argument("--root", default=".")
    ap.add_argument("-o", "--output", default="sitemap.xml")
    args = ap.parse_args()
    out = Path(args.output)
    out.write_bytes(build_sitemap(Path(args.root), args.base_url))
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
