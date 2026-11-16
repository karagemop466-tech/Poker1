#!/usr/bin/env python3
"""Small dependency-free validator for the static GitHub Pages dashboard."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import sys

ROOT = Path(__file__).resolve().parents[1]
PAGES = ["index.html", "tournaments.html", "hotels.html", "decision.html", "suggestions.html", "flagged.html"]
OFFICIAL_HOSTS = {
    "venetianlasvegas.com",
    "www.venetianlasvegas.com",
    "cdn.wynnresorts.com",
    "www.wynnlasvegas.com",
    "reservations.wynnlasvegas.com",
    "aria.mgmresorts.com",
}

class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.tbody_row_depth = 0
        self.rows = []
        self.current_row = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag == "tr" and self.tbody_row_depth:
            self.current_row = []
        if tag == "a" and self.current_row is not None and attrs.get("href"):
            self.current_row.append(attrs["href"])
        if tag == "tbody":
            self.tbody_row_depth += 1

    def handle_endtag(self, tag):
        if tag == "tr" and self.current_row is not None:
            self.rows.append(self.current_row)
            self.current_row = None
        if tag == "tbody" and self.tbody_row_depth:
            self.tbody_row_depth -= 1


def is_official(href):
    try:
        host = (urlparse(href).hostname or "").lower()
        return any(host == allowed or host.endswith("." + allowed) for allowed in OFFICIAL_HOSTS)
    except ValueError:
        return False


def main():
    errors = []
    parsed_pages = {}
    for page in PAGES:
        path = ROOT / page
        if not path.is_file():
            errors.append(f"Missing required page: {page}")
            continue
        parser = SiteParser()
        parser.feed(path.read_text(encoding="utf-8"))
        parsed_pages[page] = parser
        if not parser.links:
            errors.append(f"No links found in {page}")
        for href in parser.links:
            if href.startswith(("http://", "https://", "mailto:", "tel:", "#")):
                continue
            local = (path.parent / href.split("#", 1)[0].split("?", 1)[0]).resolve()
            if not local.exists():
                errors.append(f"Broken local link in {page}: {href}")
        for row_number, row_links in enumerate(parser.rows, 1):
            if not any(is_official(href) for href in row_links):
                errors.append(f"Table body row {row_number} in {page} has no official venue/operator source link")
    if errors:
        print("Site validation FAILED:")
        print("\n".join(f"- {e}" for e in errors))
        return 1
    row_count = sum(len(p.rows) for p in parsed_pages.values())
    print(f"Site validation passed: {len(parsed_pages)} pages, {row_count} sourced table rows, local links resolve.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
