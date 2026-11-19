#!/usr/bin/env python3
"""Inspect quoted rule text against the archived source linked by that rule.

This is a review aid rather than a full language parser. It checks quoted spans
only, preserves punctuation and digits, normalizes Unicode and whitespace, and
reports mismatches or missing source archives; it does not infer rules from a
missing quotation. `--strict` returns nonzero when any review items exist.
"""
import argparse
import json
import re
import unicodedata
from pathlib import Path

from entry_evidence import load_archives

ROOT = Path(__file__).resolve().parent.parent
QUOTED = re.compile(r'"([^"\n]+)"')


def normalize(text):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text)).strip().lower()


def audit_rule_quotes(rows, archives):
    reviews = []
    for row in rows:
        row_id = row.get("id", "?")
        linked = {s.get("url") for s in row.get("sources", []) if isinstance(s, dict)}
        for field, value in (row.get("rules") or {}).items():
            if not isinstance(value, dict):
                continue
            source = value.get("source") or {}
            url = source.get("url") if isinstance(source, dict) else None
            quotes = QUOTED.findall(value.get("excerpt") or "")
            if not quotes:
                continue
            if not url or url not in linked:
                reviews.append({"id": row_id, "field": field, "source": url, "reason": "rule source is not linked to row"})
            if url not in archives:
                reviews.append({"id": row_id, "field": field, "source": url, "reason": "no archived source available"})
                continue
            source_text = normalize(archives[url])
            for quote in quotes:
                if normalize(quote) not in source_text:
                    reviews.append({"id": row_id, "field": field, "source": url,
                                    "reason": "quoted text not found in this archive", "quote": quote})
    return reviews


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="exit nonzero if any quotation needs review")
    args = parser.parse_args()
    rows = json.loads((ROOT / "data/tournaments.json").read_text(encoding="utf-8"))["rows"]
    reviews = audit_rule_quotes(rows, load_archives())
    print("quoted rule checks: %d review item(s) across %d row(s)" %
          (len(reviews), len({x["id"] for x in reviews})))
    for item in reviews[:30]:
        print("  %s %s: %s [%s]" % (item["id"], item["field"], item["reason"], item.get("source")))
    if len(reviews) > 30:
        print("  ... %d further item(s)" % (len(reviews) - 30))
    return int(args.strict and bool(reviews))


if __name__ == "__main__":
    raise SystemExit(main())
