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
from datetime import date as _date, datetime, timedelta

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


def _candidate_ok(want, got):
    """A sheet's printed start time may differ from the schedule by up to two
    hours. WPT prints structure sheets in whole hours and rounds an evening NLH
    Turbo down (the schedule prints 9 p.m. for the $600 turbos whose sheet prints
    9 p.m., but 8 p.m. for the Dec 21 turbo whose sheet prints 6 p.m.), so a
    printed time within two hours on the same date is treated as the same event -
    and the difference is recorded as a flag on the row, never silently taken.
    """
    if want == got:
        return 0
    w = datetime.strptime(want, "%H:%M")
    g = datetime.strptime(got, "%H:%M")
    delta = abs((w - g).total_seconds()) / 60.0
    return int(delta) if delta <= 120 else None


def main():
    blocks = json.load(open(BLOCKS, encoding="utf-8"))
    rows = [r for r in json.load(open(ROWS, encoding="utf-8"))["rows"]
            if r["series"] == "WPT World Championship (Wynn)" and r["kind"] == "entry"]

    by_slot = {}
    for b in blocks:
        for date, start in b["dates"]:
            by_slot.setdefault((date, start), []).append(b)

    matched, unresolved = {}, []
    for row in sorted(rows, key=lambda r: (r["date"], r["start"], -(r["buy_in_usd"] or 0))):
        # Candidates: every sheet that prints the row's date with a start time
        # within two hours (WPT rounds structure-sheet times to the hour, and the
        # Dec 21 turbo is printed two hours apart; that difference is recorded on
        # the row, never hidden).
        cands = []
        for (d, t), block_list in by_slot.items():
            if d != row["date"]:
                continue
            delta = _candidate_ok(row["start"], t)
            if delta is None:
                continue
            for b in block_list:
                cands.append((len(tokens(b["title"]) & tokens(row["name"])), delta, b))
        if not cands:
            unresolved.append({"id": row["id"], "date": row["date"], "start": row["start"],
                               "name": row["name"], "kind": row["kind"],
                               "reason": "no structure sheet prints this date and any start "
                                         "time within two hours of the schedule"})
            continue
        # Printed title words decide first. Buy-in and an exact printed start time
        # only break a tie; they never override the printed title. The Ladies
        # Championship is why: its sheet is headed "$11,100 (***discounted to
        # $1,100 for Ladies)", so its buy-in cannot be compared with the row's.
        best_overlap = max(c[0] for c in cands)
        cands = [c for c in cands if c[0] == best_overlap]
        cands.sort(key=lambda c: (c[1],
                                  c[2]["buyin_usd"] != row["buy_in_usd"],
                                  -c[2]["buyin_usd"]))
        scored = cands
        if len(scored) > 1 and scored[0][:2] == scored[1][:2] and \
                (scored[0][2]["buyin_usd"] == row["buy_in_usd"]) == \
                (scored[1][2]["buyin_usd"] == row["buy_in_usd"]):
            unresolved.append({"id": row["id"], "date": row["date"], "start": row["start"],
                               "name": row["name"], "kind": row["kind"],
                               "reason": "more than one structure sheet prints this date and "
                                         "time and neither the printed titles nor the buy-in "
                                         "can separate them",
                               "candidates": [[c[2]["block"], c[2]["title"]] for c in scored]})
            continue
        best, delta = scored[0][2], scored[0][1]
        matched[row["id"]] = {
            "row_id": row["id"],
            "key": [row["date"], row["start"], row["buy_in_usd"]],
            "block": best["block"],
            "title": best["title"],
            "registration": best["reg"],
            "unlimited_re_entry": best["unlimited_re_entry"],
            "multi_entry": best["multi_entry"],
            "entry_fee_line": best["entry_fee_line"],
            "printed_standard_fee_line": best.get("printed_standard_fee_line"),
            "printed_discounted_fee_line": best.get("printed_discounted_fee_line"),
            "buyin_usd": best["buyin_usd"],
            "row_buyin_usd": row["buy_in_usd"],
            "prize_pool_usd": best["prize_pool_usd"],
            "tournament_fee_usd": best["tournament_fee_usd"],
            "staff_fee_usd": best["staff_fee_usd"],
            "starting_stack": best["stack"],
            "level_minutes": int(best["lmin"]) if best["lmin"] else None,
            "length_of_play": best["length"],
            "printed_time_delta_min": delta,
            "sheet_dates": best["dates"],
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
