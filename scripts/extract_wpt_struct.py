#!/usr/bin/env python3
"""Extract every structure-sheet block from the official WPT structures PDF.

Reads ``data/snapshots/wpt_struct.txt`` (a verbatim text extraction of the
official ``WPT_World_Championship_Structures.pdf`` served from
cdn.wynnresorts.com) and writes ``data/wpt_struct_blocks.json`` with one record
per published structure sheet:

    block          1-based order of the sheet in the PDF
    title          the event title exactly as the sheet prints it
    dates          every printed date/time pair for the event
    entry_fee_line the printed entry-fee breakdown
    buyin / pool / tournament_fee / staff_fee   the parsed money values
    reg            the printed registration (re-entry) clause
    unlimited      True when the clause prints "Unlimited re-entry"
    multi_entry    True when the clause allows more than one entry per player
    stack          the printed starting stack
    lmin           the printed minutes per level for single-level schedules
    length         the printed length-of-play text

Nothing is inferred. The script only reorganises text that the official PDF
prints, so a reviewer can diff a block against the PDF page it came from.

Usage:
    python3 scripts/extract_wpt_struct.py
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "data", "snapshots", "wpt_struct.txt")
OUT = os.path.join(ROOT, "data", "wpt_struct_blocks.json")

MONTHS = {m: i + 1 for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July",
     "August", "September", "October", "November", "December"])}

DATE_RE = re.compile(
    r"(?:Day \d+[A-F]?(?:/[A-Za-z0-9]+)?\s*:\s*)?"
    r"(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),?\s+"
    r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+"
    r"(\d{1,2}),?\s+(20\d\d),?\s*(?:at|, at)?\s*(\d{1,2})(?::(\d\d))?\s*([ap])\.?\s*m\.?",
    re.I)

FEE_RE = re.compile(
    r"Entry Fee:\s*(\$[\d,]+(?:\*\*)?)\s*Buy-in\s*=\s*"
    r"\$([\d,]+)\s*\(Tournament Prize Pool\)\s*\+\s*"
    r"\$([\d, ]+?)\s*\(([^)]*)\)\s*\+\s*\$([\d, ]+?)\s*\(([^)]*)\)")


def norm(s):
    return re.sub(r"\s+", " ", s)


def money(v):
    if not v:
        return None
    digits = re.sub(r"[^\d]", "", v)
    return int(digits) if digits else None


def grab(pattern, text, flags=re.S):
    m = re.search(pattern, text, flags)
    return norm(m.group(1)).strip() if m else None


def printed_dates(chunk):
    out = []
    for m in DATE_RE.finditer(norm(chunk)):
        hour = int(m.group(5)) % 12
        if m.group(7).lower() == "p":
            hour += 12
        out.append([
            "%04d-%02d-%02d" % (int(m.group(4)), MONTHS[m.group(2).title()], int(m.group(3))),
            "%02d:%02d" % (hour, int(m.group(6) or 0)),
        ])
    return out


def main():
    with open(SRC, encoding="utf-8") as f:
        text = f.read()
    # Every structure sheet starts with its own "TERMS AND CONDITIONS" banner.
    chunks = re.split(r"(?m)^\s*TERMS AND CONDITIONS\s*$", text)[1:]
    blocks = []
    for i, chunk in enumerate(chunks, 1):
        j = norm(chunk)
        fee = FEE_RE.search(j)
        reg = grab(r"Registration:\s*(.{0,900}?)\s*Starting Stack", j)
        unlimited = bool(reg and "unlimited re-entry" in reg.lower())
        blocks.append({
            "block": i,
            "title": grab(r"This (\$[\d,]+.{0,120}?)\(the \u201cTournament\u201d\)", j),
            "dates": printed_dates(chunk),
            "entry_fee_line": grab(r"(Entry Fee:\s*.{0,240}?\(Poker Staff Service Charge\))", j),
            # A discounted entry line is printed separately (the Ladies Championship prints the
            # standard $11,100 entry and a "*Discounted Ladies Entry Fee" of $1,100). Kept apart
            # so a row is never described by the price it does not pay.
            "discounted_fee_line": grab(
                r"(\*?Discounted[^:]*Entry Fee:\s*.{0,240}?\(Poker Staff Service Charge\))", j),
            "discounted_buyin_usd": (lambda m: money(m.group(1)) if m else None)(
                re.search(r"\*?Discounted[^:]*Entry Fee:\s*\$([\d,]+)\s*Buy-in", j)),
            "buyin_usd": money(fee.group(1)) if fee else None,
            "prize_pool_usd": int(re.sub(r"[^\d]", "", fee.group(2))) if fee else None,
            "tournament_fee_usd": money(fee.group(3)) if fee else None,
            "staff_fee_usd": money(fee.group(5)) if fee else None,
            "reg": reg,
            # "Unlimited re-entry" is a printed statement, so the sheet itself
            # confirms that more than one entry may be bought.
            "unlimited_re_entry": unlimited,
            "multi_entry": bool(unlimited) or bool(
                reg and re.search(r"one \(1\) re-entry|two \(2\)|entries maximum|"
                                  r"(two|three|four|2|3|4)\s+entries", reg, re.I)),
            "stack": grab(r"Starting Stack:\s*(.{0,140}?)\s*Length of Play", j),
            "lmin": grab(r"Length of Play:\s*(\d+)\s*minutes per level", j),
            "length": grab(r"Length of Play:\s*(.{0,300}?)\s*Breaks", j),
        })
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(blocks, f, indent=1)
        f.write("\n")
    dates = sum(len(b["dates"]) for b in blocks)
    print("wrote %s: %d structure sheets, %d printed date/time pairs, %d with a fee "
          "breakdown, %d with a registration clause, %d printing unlimited re-entry"
          % (os.path.relpath(OUT, ROOT), len(blocks), dates,
             sum(1 for b in blocks if b["buyin_usd"]),
             sum(1 for b in blocks if b["reg"]),
             sum(1 for b in blocks if b["unlimited_re_entry"])))


if __name__ == "__main__":
    main()
