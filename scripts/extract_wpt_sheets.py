#!/usr/bin/env python3
"""Map every WPT schedule row to the structure sheet that governs it.

The official schedules PDF prints one line per tournament, and the official
structures PDF prints one structure sheet per event. This script joins the two
so that no row is labelled "unverified" while a published sheet for it exists,
and so that every row carries the sheet's own clause text.

The join is deliberately conservative:

1. Candidates are only structure sheets that print the row's exact date and
   start time.
2. A candidate must not print a different buy-in than the row.
3. Of the remaining candidates, exactly one must win on printed title words.
   If the match is not unique the row is reported as unresolved and is left
   exactly as the schedule printed it - never guessed.

Output: ``data/wpt_row_sheets.json`` - one record per matched row with the
block number, the printed title, the registration clause, the fee breakdown and
the starting stack, plus an ``unresolved`` list for reviewer attention.

Usage:
    python3 scripts/extract_wpt_struct.py     # refresh data/wpt_struct_blocks.json
    python3 scripts/extract_wpt_sheets.py     # join rows to sheets
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOCKS = os.path.join(ROOT, "data", "wpt_struct_blocks.json")
ROWS = os.path.join(ROOT, "data", "tournaments.json")
OUT = os.path.join(ROOT, "data", "wpt_row_sheets.json")

STOP = set("""a of the and no limit holdem hold'em nlh poker tournament event day
day1a day1b day1c day1d day1e day1f 1a 1b 1c 1d 1e 1f""".split())


def tokens(s):
    s = (s or "").lower().replace("hold\u2019em", "holdem").replace("hold'em", "holdem")
    s = s.replace("$", "").replace(",", "")
    return {w for w in re.findall(r"[a-z0-9]+", s) if w not in STOP}


def main():
    blocks = json.load(open(BLOCKS, encoding="utf-8"))
    rows = [r for r in json.load(open(ROWS, encoding="utf-8"))["rows"]
            if r["series"] == "WPT World Championship (Wynn)"]

    by_slot = {}
    for b in blocks:
        for date, start in b["dates"]:
            by_slot.setdefault((date, start), []).append(b)

    matched, unresolved = {}, []
    for row in sorted(rows, key=lambda r: (r["date"], r["start"], -(r["buy_in_usd"] or 0))):
        cands = [b for b in by_slot.get((row["date"], row["start"]), [])
                 if not row["buy_in_usd"] or b["buyin_usd"] == row["buy_in_usd"]]
        if not cands:
            # Continuation rows (Day 2, Final Table) never have their own
            # structure sheet; the parent event's sheet is the source for them.
            unresolved.append({"id": row["id"], "date": row["date"], "start": row["start"],
                               "name": row["name"], "kind": row["kind"],
                               "reason": "no structure sheet prints this date and time"})
            continue
        scored = []
        for b in cands:
            scored.append((len(tokens(b["title"]) & tokens(row["name"])), b))
        scored.sort(key=lambda t: -t[0])
        if len(scored) > 1 and scored[0][0] == scored[1][0]:
            unresolved.append({"id": row["id"], "date": row["date"], "start": row["start"],
                               "name": row["name"], "kind": row["kind"],
                               "reason": "more than one structure sheet prints this date and "
                                         "time and the printed titles cannot separate them",
                               "candidates": [[b["block"], b["title"]] for _, b in scored]})
            continue
        best = scored[0][1]
        matched[row["id"]] = {
            "row_id": row["id"],
            "key": [row["date"], row["start"], row["buy_in_usd"]],
            "block": best["block"],
            "title": best["title"],
            "registration": best["reg"],
            "unlimited_re_entry": best["unlimited_re_entry"],
            "multi_entry": best["multi_entry"],
            "entry_fee_line": best["entry_fee_line"],
            "buyin_usd": best["buyin_usd"],
            "prize_pool_usd": best["prize_pool_usd"],
            "tournament_fee_usd": best["tournament_fee_usd"],
            "staff_fee_usd": best["staff_fee_usd"],
            "starting_stack": best["stack"],
            "level_minutes": int(best["lmin"]) if best["lmin"] else None,
            "length_of_play": best["length"],
        }

    out = {
        "source": "https://cdn.wynnresorts.com/image/upload/v1750864036/visitwynn_pdfs_files/"
                  "Poker/WPT/WPT_World_Championship_Structures.pdf",
        "schedule": "https://cdn.wynnresorts.com/image/upload/v1757097329/visitwynn_pdfs_files/"
                    "Poker/WPT/WPT_World_Championship_Schedule.pdf",
        "blocks_total": len(blocks),
        "rows_total": len(rows),
        "matched": matched,
        "unresolved": unresolved,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
        f.write("\n")
    print("wrote %s: %d of %d WPT rows joined to a printed structure sheet, %d unresolved"
          % (os.path.relpath(OUT, ROOT), len(matched), len(rows), len(unresolved)))
    for u in unresolved:
        print("  unresolved", u["id"], u["date"], u["start"], u["name"], "|", u["reason"])


if __name__ == "__main__":
    main()
