#!/usr/bin/env python3
"""Compare the official Venetian DeepStack IV listing (live read 2026-11-19) with data/tournaments.json.

Read-only: nothing in data/ is changed. Matching key is (date, start, event_no, structure file).
Name differences are reported separately because official names contain typos and wording variants.
"""
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LISTING = ROOT / "research/live-reread-98241f2f/venetian_dse_iv_listing_2026-11-19.tsv"
DATA = ROOT / "data/tournaments.json"


def norm_name(s: str) -> str:
    s = s.lower()
    s = s.replace("\u2019", "'")
    s = re.sub(r"\s*-\s.*$", "", s)  # drop official sub-notes after " - "
    s = re.sub(r"\(.*?\)", " ", s)  # drop parenthetical notes
    s = re.sub(r"[^a-z0-9$ ]+", " ", s)
    s = s.replace("limit", "limit").replace("nlh", "no limit hold em").replace("hold em", "holdem")
    s = s.replace("no limit holdem", "no limit holdem")
    return " ".join(s.split())


def main() -> int:
    official = list(csv.DictReader(LISTING.open(encoding="utf-8"), delimiter="\t"))
    rows = [r for r in json.loads(DATA.read_text(encoding="utf-8"))["rows"]
            if r["series"] == "Venetian DeepStack Extravaganza IV"]

    def key_repo(r):
        return (r["date"], r["start"], str(r["event_no"]), r["rules"]["single_entry"]["source"]["url"].split("/")[-1])

    def key_off(o):
        return (o["date"], o["start"], o["event_no"], o["structure_file"])

    repo_keys = Counter(key_repo(r) for r in rows)
    off_keys = Counter(key_off(o) for o in official)
    missing_in_repo = sorted(k for k in off_keys if k not in repo_keys)
    extra_in_repo = sorted(k for k in repo_keys if k not in off_keys)

    name_diff = []
    repo_by_key = {}
    for r in rows:
        repo_by_key.setdefault(key_repo(r), []).append(r)
    for o in official:
        for r in repo_by_key.get(key_off(o), []):
            if norm_name(o["name"]) and norm_name(o["name"]) != norm_name(r["name"]):
                name_diff.append((o["date"], o["start"], o["event_no"], o["name"], r["name"]))
                break

    print(f"official entries: {len(official)}  repo DSE IV rows: {len(rows)}")
    print(f"official keys matched exactly: {len(official) - len(missing_in_repo)}")
    print(f"official keys with no repo row: {len(missing_in_repo)}")
    for k in missing_in_repo:
        print("  MISSING", k)
    print(f"repo keys with no official listing row: {len(extra_in_repo)}")
    for k in extra_in_repo:
        print("  EXTRA", k)
    print(f"name differences (normalised, first 60 shown): {len(name_diff)}")
    for d in name_diff[:60]:
        print("  NAME", d)
    return 0 if not missing_in_repo and not extra_in_repo else 1


if __name__ == "__main__":
    sys.exit(main())
