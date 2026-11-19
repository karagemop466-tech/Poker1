#!/usr/bin/env python3
"""Extract the structured rule fields printed on each official structure sheet.

Reads the plain-text snapshots produced by scripts/monitor_sources.py (which are
byte-for-byte extractions of the official PDFs) and prints, per sheet:

    title, sheet id, effective date, event numbers, start time, starting chips,
    level duration, late registration, guarantee, house fee / buy-in, payout %,
    and every line that mentions re-entry, re-buy, add-on, bounty, flight or
    multiple entries.

It writes data/structure_rules.json. Sheet-kind labels are evidence clues, not
event eligibility decisions; a human must check event scope and all other terms.
Silence is never proof that re-entry, rebuys or add-ons are prohibited.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAP = os.path.join(ROOT, "data", "snapshots")
OUT = os.path.join(ROOT, "data", "structure_rules.json")

KEYWORDS = re.compile(
    r"(re-?enter|re-?entry|re-?buy|rebuy|add-?on|addon|multiple entr|subsequent "
    r"buy-?in|bount|flight|single entry|freeze|one entry|per entr)", re.I)

STOP = (r"(?=Event Numbers?\s*:|Start Times?\s*:|Starting Chips\s*:|Level Duration\s*:|"
        r"Late Registration\s*:|Guarantee\s*:|\d+\.\s+TDA|$)")
FIELDS = {
    "event_no": re.compile(r"Event Numbers?\s*:\s*(.+?)" + STOP, re.I),
    "start_time": re.compile(r"Start Times?\s*:\s*(.+?)" + STOP, re.I),
    "chips": re.compile(r"Starting Chips\s*:\s*(.+?)" + STOP, re.I),
    "levels": re.compile(r"Level Duration\s*:\s*(.+?)" + STOP, re.I),
    "late_reg": re.compile(r"Late Registration\s*:\s*(.+?)" + STOP, re.I),
    "guarantee": re.compile(r"Guarantee\s*:\s*(.+?)" + STOP, re.I),
    "fee": re.compile(r"\$\s*([\d,]+)\s*of the \$\s*([\d,]+)\s*Buy-?In", re.I),
    "payout": re.compile(r"pays?\s+([\d.]+)\s*%\s*of the field", re.I),
}
SS = re.compile(r"SS#\s*(\d+)\s+Effective Date\s*([\d./]+)")


def clean(s):
    return re.sub(r"\s+", " ", s).strip()


def entry_evidence(text):
    """Extract numbered clauses and conservative event/flight scope clues.

    The word "re-entry" can occur in a promotion valid for one specific event
    or flight. Its presence alone does not apply that rule to every event on the
    sheet, and a bagged-player restriction is not affirmative proof that every
    other player may buy another entry.
    """
    joined = re.sub(r"\s+", " ", text)
    clauses = re.findall(r"(?ms)^\s*\d{1,2}\.\s+(.*?)(?=^\s*\d{1,2}\.\s+|\Z)", text)
    re_rx = re.compile(r"subsequent re-?entry|subsequent buy in.{0,60}after the initial buy in", re.I)
    clause = next((clean(c) for c in clauses if re_rx.search(c)), None)
    flight = re.search(r"(.{0,60})(Each starting flight will play until|Any player who bags chips for Day 2 may not play a subsequent flight)(.{0,400})", joined, re.I)
    addon = re.search(r"(.{0,120})(add-?on)(.{0,160})", joined, re.I)
    rebuy = re.search(r"(.{0,120})(re-?buy)(.{0,160})", joined, re.I)
    scope = re.search(r"\bfor\s+event\s*#?\s*(\d+)\b(.{0,100}?)\bonly\b", clause or "", re.I)
    event_scope = [int(scope.group(1))] if scope else []
    flights = re.findall(r"\b1[A-Z]\b", scope.group(2), re.I) if scope else []
    kind = ("EVENT_SPECIFIC_RE_ENTRY" if scope else "RE_ENTRY" if clause else
            "MULTI_FLIGHT" if flight else "NO_ENTRY_POLICY_FOUND")
    return {
        "re_entry_excerpt": clause,
        "re_entry_event_scope": event_scope,
        "re_entry_flight_scope": [v.upper() for v in flights],
        "multi_flight_excerpt": clean(flight.group(0)) if flight else None,
        "add_on_excerpt": clean(addon.group(0)) if addon else None,
        "re_buy_excerpt": clean(rebuy.group(0)) if rebuy else None,
        "sheet_kind": kind,
    }


def main():
    out = {}
    for name in sorted(os.listdir(SNAP)):
        if not (name.startswith("v_nov_struct_") or name.startswith("v_dec_struct_")):
            continue
        with open(os.path.join(SNAP, name), encoding="utf-8") as f:
            lines = [l.rstrip() for l in f]
        text = "\n".join(lines)
        joined = re.sub(r"\s+", " ", text)
        sid = name[:-4]
        title = next((clean(l) for l in lines if clean(l) and not l.startswith(" ")), "")
        rec = {"sheet": sid, "title": title, "snapshot": "data/snapshots/%s" % name}
        m = SS.search(joined)
        if m:
            rec["sheet_no"] = m.group(1)
            rec["effective_date"] = m.group(2)
        for key, rx in FIELDS.items():
            m = rx.search(joined)
            if not m:
                rec[key] = None
                continue
            if key == "fee":
                rec["house_fee_usd"] = int(m.group(1).replace(",", ""))
                rec["buy_in_usd"] = int(m.group(2).replace(",", ""))
                rec["fee_excerpt"] = clean(m.group(0))
            elif key == "payout":
                rec["payout_pct"] = float(m.group(1))
                rec["payout_excerpt"] = clean(m.group(0))
            else:
                rec[key] = clean(m.group(1))
        hits = []
        for i, l in enumerate(lines):
            if KEYWORDS.search(l):
                hits.append({"line": i + 1, "text": clean(l)})
        rec["keyword_lines"] = hits

        # An event-scoped clause stays scoped; missing language stays unknown.
        rec.update(entry_evidence(text))
        rules = re.findall(r"(?m)^\s*(\d{1,2})\.\s+\S", text)
        rec["rule_count"] = len({int(x) for x in rules})
        out[sid] = rec

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)

    for sid, r in out.items():
        print("%-18s | %-42s | ev %-18s | start %-9s | chips %-7s | lvl %-12s | latereg %-32s | gtd %-12s | fee %s" % (
            sid, (r["title"] or "")[:42], (r.get("event_no") or "")[:18], r.get("start_time") or "",
            r.get("chips") or "", r.get("levels") or "", (r.get("late_reg") or "")[:32],
            (r.get("guarantee") or ""), r.get("fee_excerpt") or ""))
        for h in r["keyword_lines"]:
            print("      L%-4d %s" % (h["line"], h["text"][:150]))
    print("\nwrote", OUT, "with", len(out), "sheets")


if __name__ == "__main__":
    main()
