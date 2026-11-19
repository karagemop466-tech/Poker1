#!/usr/bin/env python3
"""Compare the published Wynn Signature Series rows with the live official schedule.

Read-only. Run from the repo root:

    python3 research/requirements-audit-dd06081b/compare_wss_live_20261119.py

Input is the live capture this session made on 2026-11-19 with the page-fetch tool,
saved verbatim beside this script as ``wss_sched_live_20261119.md`` (a Markdown
table render of
https://cdn.wynnresorts.com/image/upload/v1753296112/visitwynn_pdfs_files/Poker/Wynn%20Signature%20Series/Wynn_Signature_Series_Schedule.pdf,
linked from https://www.wynnlasvegas.com/casino/poker).

The check is field by field, one row at a time: date, 24h start time, buy-in,
guarantee, starting chips and the printed level string. A value the official row
prints empty stays ``None`` and is compared as "blank vs blank". Nothing is
inferred: a row that cannot be matched prints MISSING, a printed row with no
published row prints EXTRA.

Why the capture is not parsed as the PDF: the archived line render of this same
file (``data/snapshots/wss_sched.txt``) shifts whole cells on five rows
(FLAGGED.md F83). The capture beside this script was taken with a table-structure
renderer, so its columns can be read as columns.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CAPTURE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wss_sched_live_20261119.md")
YEAR = "2027"

TIME_RE = re.compile(r"^(\d{1,2})\s*([AP])\.?M\.?$", re.I)


def to_24h(cell):
    m = TIME_RE.match(cell.strip().replace(" ", ""))
    if not m:
        return None
    hour = int(m.group(1)) % 12
    if m.group(2).upper() == "P":
        hour += 12
    return "%02d:00" % hour


def money(cell):
    cell = (cell or "").strip()
    if not cell:
        return None
    m = re.search(r"\$?\s*([\d,]+)", cell)
    return int(m.group(1).replace(",", "")) if m else None


def digits(cell):
    cell = (cell or "").strip()
    if not cell:
        return None
    m = re.search(r"([\d,]+)", cell)
    return int(m.group(1).replace(",", "")) if m else None


def parse_capture(path):
    """One dict per printed schedule row. Only lines starting with a date cell."""
    out = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not cells or not re.match(r"^\d{1,2}/\d{1,2}$", cells[0]):
            continue
        if len(cells) < 8:
            continue
        date_m, date_d = cells[0].split("/")
        out.append({
            "date": "%s-%02d-%02d" % (YEAR, int(date_m), int(date_d)),
            "day": cells[1],
            "time_text": cells[2],
            "start": to_24h(cells[2]),
            "name": cells[3],
            "guarantee": money(cells[4]) if not cells[4].lower().startswith(("10 seats",)) else None,
            "entry": money(cells[5]),
            "chips": digits(cells[6]),
            "levels": (cells[7] or "").strip() or None,
        })
    return out


def main():
    rows = [r for r in json.load(open(os.path.join(ROOT, "data/tournaments.json"), encoding="utf-8"))["rows"]
            if r["series"] == "Wynn Signature Series"]
    printed = parse_capture(CAPTURE)

    problems, notes = [], []
    if len(printed) != len(rows):
        problems.append("printed rows %d != published rows %d" % (len(printed), len(rows)))

    # A printed row is matched on (date, start) because those are the only two cells
    # that are never blank in the official poster.
    index = {}
    for r in rows:
        index.setdefault((r["date"], r["start"]), []).append(r)

    used = set()
    for p in printed:
        key = (p["date"], p["start"])
        bucket = [r for r in index.get(key, []) if r["id"] not in used]
        if not bucket:
            problems.append("MISSING published row for printed %s %s %s" % (p["date"], p["time_text"], p["name"]))
            continue
        row = bucket[0]
        used.add(row["id"])
        checks = [("date", row["date"], p["date"]), ("start", row["start"], p["start"]),
                  ("buy_in_usd", row["buy_in_usd"], p["entry"]),
                  ("guarantee_usd", row["guarantee_usd"], p["guarantee"]),
                  ("starting_chips", row["starting_chips"], p["chips"])]
        for field, got, want in checks:
            if got != want:
                problems.append("%s %s: %s published %r, official row prints %r"
                                % (row["id"], p["name"], field, got, want))
        if p["levels"] and row.get("levels_published") != p["levels"]:
            problems.append("%s %s: levels_published published %r, official row prints %r"
                            % (row["id"], p["name"], row.get("levels_published"), p["levels"]))

    for r in rows:
        if r["id"] not in used:
            problems.append("EXTRA published row with no printed line: %s %s %s" % (r["id"], r["date"], r["name"]))

    # The three name word-order notes are recorded, not defects: the poster prints
    # "TORSE $400 35,000 30" in the name column order that the archived line render
    # flattened. They are listed so a reviewer sees the wording, not so a value changes.
    for r in rows:
        if r["name"] in ("Mixed Game (TORSE)", "Mixed Game (TOE)", "Seniors No Limit Hold'em 50+"):
            notes.append("%s name published as %r - wording only" % (r["id"], r["name"]))

    print("== Wynn Signature Series: live capture vs published rows")
    print("   printed rows: %d | published rows: %d | matched: %d" % (len(printed), len(rows), len(used)))
    for n in notes:
        print("   NOTE", n)
    print("== mismatches: %d" % len(problems))
    for p in problems:
        print("  -", p)
    if not problems:
        print("  every published value matches the row the official schedule prints")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
