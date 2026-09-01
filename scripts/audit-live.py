#!/usr/bin/env python3
"""Audit live loopmagazin.hu articles (downloaded HTML or via sitemap fetch)."""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

AUDIT_SCRIPT = Path(__file__).resolve().parent / "seo-audit.py"


def fetch_sitemap_articles(base: str, out_dir: Path) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    xml = subprocess.check_output(["curl", "-sL", f"{base}/sitemap.xml"], text=True)
    urls = []
    for line in xml.splitlines():
        if "/cikk/" in line and "<loc>" in line:
            start = line.index("<loc>") + 5
            end = line.index("</loc>")
            urls.append(line[start:end])
    for url in urls:
        dest = out_dir / Path(url).name
        subprocess.run(["curl", "-sL", url, "-o", str(dest)], check=True)
    return len(urls)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true", help="Download articles from live site")
    ap.add_argument("--dir", default="cikk", help="Directory with HTML files")
    args = ap.parse_args()
    root = Path(args.dir)
    if args.fetch:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            n = fetch_sitemap_articles("https://loopmagazin.hu", tmp_path)
            print(f"Fetched {n} articles")
            return subprocess.call([sys.executable, str(AUDIT_SCRIPT), str(tmp_path)])
    return subprocess.call([sys.executable, str(AUDIT_SCRIPT), str(root)])


if __name__ == "__main__":
    sys.exit(main())
