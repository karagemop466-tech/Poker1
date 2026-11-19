#!/usr/bin/env python3
"""Value check for the official Venetian DeepStack IV listing (read 2026-11-19). Read-only."""
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LISTING = ROOT / "research/live-reread-98241f2f/venetian_dse_iv_listing_2026-11-19.tsv"
DATA = ROOT / "data/tournaments.json"


def official_values(name: str):
    head = name.split(" - ")[0]
    m = re.search(r"\$([\d,]+)(?!\s*(?:K|Mill))", head)
    buy_in = int(m.group(1).replace(",", "")) if m else None
    g = re.search(r"\$([\d,.]+)\s*(K|Mill)?\s*GTD", head)
    guarantee = None
    if g:
        amt = float(g.group(1).replace(",", ""))
        guarantee = int(amt * (1_000_000 if g.group(2) == "Mill" else 1_000 if g.group(2) == "K" else 1))
    restart = bool(re.search(r"Restart|Final Table", name))
    return buy_in, guarantee, restart


def main() -> int:
    official = list(csv.DictReader(LISTING.open(encoding="utf-8"), delimiter="\t"))
    rows = [r for r in json.loads(DATA.read_text(encoding="utf-8"))["rows"]
            if r["series"] == "Venetian DeepStack Extravaganza IV"]
    idx = {}
    for r in rows:
        k = (r["date"], r["start"], str(r["event_no"]), r["rules"]["single_entry"]["source"]["url"].split("/")[-1])
        idx.setdefault(k, []).append(r)
    bad = []
    checked = 0
    for o in official:
        k = (o["date"], o["start"], o["event_no"], o["structure_file"])
        buy, gtd, restart = official_values(o["name"])
        for r in idx.get(k, []):
            checked += 1
            if buy is not None and r.get("buy_in_usd") != buy:
                bad.append(("buy_in", o["date"], o["start"], o["event_no"], buy, r.get("buy_in_usd"), r["id"]))
            if gtd is not None and r.get("guarantee_usd") != gtd:
                bad.append(("guarantee", o["date"], o["start"], o["event_no"], gtd, r.get("guarantee_usd"), r["id"]))
            is_cont = r["kind"] == "continuation"
            if restart != is_cont:
                bad.append(("kind", o["date"], o["start"], o["event_no"], "restart" if restart else "entry", r["kind"], r["id"]))
    print(f"row-checks: {checked}  mismatches: {len(bad)}")
    for b in bad:
        print("  MISMATCH", b)
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
