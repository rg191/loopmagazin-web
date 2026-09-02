#!/usr/bin/env python3
"""Audit static HTML files for Google generative AI / SEO best practices."""

from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


class HeadingParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.headings: list[tuple[str, str]] = []
        self.title = ""
        self.meta_description = ""
        self.has_json_ld = False
        self.has_faq = False
        self.in_title = False
        self.in_script_ld = False
        self.script_buffer = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        if tag in ("h1", "h2", "h3"):
            self._current_heading = (tag, "")
        elif tag == "title":
            self.in_title = True
        elif tag == "meta" and attr.get("name", "").lower() == "description":
            self.meta_description = attr.get("content") or ""
        elif tag == "script" and attr.get("type") == "application/ld+json":
            self.in_script_ld = True
            self.script_buffer = ""
        elif tag in ("details",) or (tag == "div" and "faq" in (attr.get("class") or "").lower()):
            self.has_faq = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False
        elif tag == "script" and self.in_script_ld:
            self.in_script_ld = False
            if "FAQPage" in self.script_buffer or "Question" in self.script_buffer:
                self.has_faq = True
            if "@type" in self.script_buffer and (
                "Article" in self.script_buffer
                or "NewsArticle" in self.script_buffer
                or "BlogPosting" in self.script_buffer
            ):
                self.has_json_ld = True
        elif tag in ("h1", "h2", "h3") and hasattr(self, "_current_heading"):
            self.headings.append(self._current_heading)
            del self._current_heading

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data.strip()
        elif self.in_script_ld:
            self.script_buffer += data
        elif hasattr(self, "_current_heading"):
            level, text = self._current_heading
            self._current_heading = (level, (text + data).strip())


def audit_file(path: Path) -> list[str]:
    issues: list[str] = []
    html = path.read_text(encoding="utf-8", errors="replace")
    parser = HeadingParser()
    parser.feed(html)

    if not parser.title:
        issues.append("missing <title>")
    if len(parser.title) > 60:
        issues.append(f"title too long ({len(parser.title)} chars)")
    if not parser.meta_description:
        issues.append("missing meta description")
    h1s = [h for h in parser.headings if h[0] == "h1"]
    if len(h1s) == 0:
        issues.append("missing H1")
    elif len(h1s) > 1:
        issues.append(f"multiple H1 ({len(h1s)})")
    if not parser.has_json_ld:
        issues.append("no JSON-LD schema")
    if "llms.txt" in html.lower():
        issues.append("references llms.txt (not needed per Google)")
    if re.search(r"chunk(?:ing|ed)", html, re.I) and "FAQ" not in html:
        issues.append("possible AI-chunking pattern detected")

    return issues


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit Loop Magazin HTML for SEO/AI readiness")
    ap.add_argument("root", nargs="?", default=".", help="Site root directory")
    args = ap.parse_args()
    root = Path(args.root)
    files = sorted(root.rglob("*.html"))
    if not files:
        print("No HTML files found.", file=sys.stderr)
        return 1

    total_issues = 0
    for f in files:
        if ".git" in f.parts:
            continue
        issues = audit_file(f)
        rel = f.relative_to(root)
        if issues:
            total_issues += len(issues)
            print(f"\n{rel}:")
            for i in issues:
                print(f"  - {i}")
        else:
            print(f"OK  {rel}")

    print(f"\n{len(files)} files, {total_issues} issues")
    return 0 if total_issues == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
