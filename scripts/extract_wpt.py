#!/usr/bin/env python3
"""Parse the official WPT World Championship structures PDF into per-event rules.

Reads data/snapshots/wpt_struct.txt (a verbatim text extraction of the official
WPT World Championship Structures PDF) and writes data/wpt_rules.json with one
record per event block:

    name, guarantee, dates, flights (day/time lines as printed), entry fee
    breakdown, registration text, starting stack, length of play, and any
    add-on / re-buy text found in the block.

Nothing is inferred: only text printed in the official PDF is captured.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "data", "snapshots", "wpt_struct.txt")
OUT = os.path.join(ROOT, "data", "wpt_rules.json")

FIELD = re.compile(r"^(Entry Fee|Registration|Starting Stack|Length of Play|Breaks|"
                   r"Players Per Table|Level|Day \d+[A-F]?)\s*:?\s*(.*)$")


def clean(s):
    return re.sub(r"\s+", " ", s).strip()


def main():
    with open(SRC, encoding="utf-8") as f:
        lines = [l.rstrip() for l in f]

    # A block starts a few lines above the "TERMS AND CONDITIONS" banner.
    starts = [i for i, l in enumerate(lines) if clean(l) == "TERMS AND CONDITIONS"]
    blocks = []
    for n, i in enumerate(starts):
        end = starts[n + 1] - 12 if n + 1 < len(starts) else len(lines)
        chunk = lines[max(0, i - 6):min(len(lines), i + 400)]
        # stop at the next block's header (blank run followed by a title line)
        text = "\n".join(chunk)
        head = [clean(x) for x in lines[max(0, i - 6):i] if clean(x)]
        name = ""
        gtd = ""
        for h in reversed(head):
            if not name and "GUARANTEE" not in h.upper() and "TERMS" not in h.upper():
                name = h
            if "GUARANTEE" in h.upper():
                gtd = h
        body = "\n".join(lines[i:end])
        joined = clean(body)

        def grab(label, stop):
            m = re.search(label + r"\s*:?\s*(.{0,900}?)(?=" + stop + r"|$)", joined)
            return clean(m.group(1)) if m else None

        entry = grab("Entry Fee", "Registration")
        reg = grab("Registration", "Starting Stack")
        stack = grab("Starting Stack", "Length of Play")
        length = grab("Length of Play", "Breaks")
        dates = clean(lines[i + 1]) if i + 1 < len(lines) else ""
        flights = [clean(x) for x in lines[i + 2:i + 20]
                   if re.match(r"^Day\s", clean(x))]
        blocks.append({
            "name": name, "guarantee_line": gtd, "dates_line": dates,
            "flights": flights, "entry_fee": entry, "registration": reg,
            "starting_stack": stack, "length_of_play": length,
            "has_addon": bool(re.search(r"add-?on", joined, re.I)),
            "has_rebuy": bool(re.search(r"re-?buy", joined, re.I)),
        })

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(blocks, f, indent=1)

    for b in blocks:
        print("NAME : %s | %s | %s" % (b["name"], b["guarantee_line"], b["dates_line"]))
        print("  FLIGHTS: %s" % ("; ".join(b["flights"]) or "-"))
        print("  FEE  : %s" % (b["entry_fee"] or "-")[:150])
        print("  REG  : %s" % (b["registration"] or "-")[:320])
        print("  STACK: %s | LENGTH: %s" % ((b["starting_stack"] or "-")[:60], (b["length_of_play"] or "-")[:110]))
        if b["has_addon"] or b["has_rebuy"]:
            print("  *** add-on/rebuy text present in block")
        print()
    print("wrote", OUT, "with", len(blocks), "blocks")


if __name__ == "__main__":
    main()
