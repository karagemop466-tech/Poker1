#!/usr/bin/env python3
"""Pair-level schedule check: published rows vs the archived official page text.

`scripts/verify_rows.py` proves each individual value in a row (a buy-in, a time, a
fee) appears somewhere in the official document. That cannot catch a row stored with
the *right values on the wrong schedule line* - a time that exists on the page but
belongs to a different date, or a date paired with the neighbouring row's start time.

This check therefore compares the (date, start) **pair** of every published row with
the pairs the official document actually prints, and the money tokens on the same
printed line:

  * the two Venetian event pages (HTML captured to one cell per line), and
  * the Wynn Signature Series poster (one row per line: date, day, time, event).

The WPT schedule PDF is deliberately not pair-checked: its text extracts column-wise
(all dates, then all times), so the row structure is gone and a pair match against it
would be a coin flip. Those rows are covered by `verify_rows.py` value checks instead.

Read-only: it prints a report and exits non-zero if a published row does not match a
printed line.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
SNAP = os.path.join(DATA, "snapshots")

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]
# "Tuesaday" is printed on the official page for January 5, 2027; it is matched so the
# row is still pair-checked, and the misspelling is recorded in FLAGGED.md (F2).
DATE_RE = re.compile(r"^(Monday|Tuesday|Tuesaday|Wednesday|Thursday|Friday|Saturday|Sunday),?\s+"
                     r"(" + "|".join(MONTHS) + r")\s+(\d{1,2}),?\s+(\d{4})$")
TIME_RE = re.compile(r"^(\d{1,2}):(\d{2})\s*(AM|PM)$", re.I)


def norm(s):
    return re.sub(r"\s+", " ", (s or "").replace("\u2019", "'").replace("\ufb01", "fi")).strip().lower()


def h24(hh, mm, ampm):
    return "%02d:%02d" % (int(hh) % 12 + (12 if ampm.lower() == "pm" else 0), int(mm))


def parse_event_page(path):
    """The (date, start, line-text) tuples a Venetian event page prints, in order."""
    lines = [l.strip() for l in open(path, encoding="utf-8") if l.strip()]
    out, cur = [], None
    for i, line in enumerate(lines):
        m = DATE_RE.match(line)
        if m:
            cur = "%04d-%02d-%02d" % (int(m.group(4)), MONTHS.index(m.group(2)) + 1, int(m.group(3)))
            continue
        t = TIME_RE.match(line)
        if t and cur:
            rest = " ".join(lines[i + 1:i + 4])
            out.append({"date": cur, "start": h24(t.group(1), t.group(2), t.group(3)), "rest": norm(rest)})
    return out


def parse_poster_rows(path):
    """The Wynn Signature Series poster prints one row per line: '1/11 MON 12 P.M. EVENT ...'."""
    out = []
    for line in open(path, encoding="utf-8"):
        m = re.match(r"^(\d{1,2})/(\d{1,2})\s+(?:MON|TUE|WED|THU|FRI|SAT|SUN)\s+(\d{1,2})\s*([AP])\.?M\.?"
                     r"(?:\s|$)(.*)$", line.strip(), re.I)
        if not m:
            continue
        hh = int(m.group(3)) % 12 + (12 if m.group(4).upper() == "P" else 0)
        out.append({"date": "2027-%02d-%02d" % (int(m.group(1)), int(m.group(2))),
                    "start": "%02d:00" % hh, "rest": norm(m.group(5))})
    return out


def overlap(a, b):
    """How many words the two names share - used to pick which printed line a row is."""
    wa, wb = set(a.split()), set(b.split())
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / float(len(wa | wb))


def documented(row, needle):
    """True when the row already carries a flag explaining this mismatch.

    The method here is to publish a conflict on the row rather than resolve it in
    silence, so a mismatch that the row itself explains is not a defect: it is a
    recorded disagreement between two official sources. A mismatch the row does not
    mention is a real failure, which is what this check exists to catch.
    """
    return any(needle in flag for flag in (row.get("flags") or []))


def compare(series, printed, mine, problems, documented_notes):
    """Match each published row to a line the official document prints, one line per row.

    The official pages sometimes print two events at the same time on the same day (a
    Day 2 restart and the next day's first flight), so this is a bipartite greedy match
    on (date, start) plus name similarity, not a lookup by key.
    """
    free = list(range(len(printed)))
    used_by = {}
    # pass 1: exact (date, start) + best name overlap; pass 2: the F1 year typo.
    for row_index, r in enumerate(mine):
        want = (r["date"], r["start"])
        alt = None
        if r["date"] == "2026-12-26":  # FLAGGED.md F1: the page prints 2025 for these rows
            alt = ("2025-12-26", r["start"])
        best, best_score = None, 0.0
        for i in free:
            p = printed[i]
            if (p["date"], p["start"]) != want:
                continue
            score = overlap(norm(r["name"]), p["rest"])
            if best is None or score > best_score:
                best, best_score = i, score
        if best is None and alt:
            for i in free:
                p = printed[i]
                if (p["date"], p["start"]) != alt:
                    continue
                score = overlap(norm(r["name"]), p["rest"])
                if best is None or score > best_score:
                    best, best_score = i, score
                    p["typo_year"] = True
        if best is not None:
            used_by[row_index] = best
            free.remove(best)

    orphans = [r for i, r in enumerate(mine) if i not in used_by]
    unprinted = [printed[i] for i in free]
    print("\n== %s: official document prints %d dated lines, dataset publishes %d rows"
          % (series, len(printed), len(mine)))
    for r in orphans:
        note = "%s %s: no official line at %s %s for %s" % (
            series, r["id"], r["date"], r["start"], r["name"][:44])
        if documented(r, "Two official sources disagree"):
            documented_notes.append(note + " - recorded on the row as a source conflict")
            print("   CONFLICT ON RECORD  %s %s %s - %s (the row's own flag explains it)"
                  % (r["id"], r["date"], r["start"], r["name"][:58]))
        else:
            print("   NOT PRINTED  %s %s %s - %s" % (r["id"], r["date"], r["start"], r["name"][:58]))
            problems.append(note)
    for p in unprinted:
        same_day = [r["id"] for r in mine if r["date"] == p["date"]]
        print("   UNPUBLISHED  official line %s %s: %s%s"
              % (p["date"], p["start"], p["rest"][:52],
                 "  (rows on this date: %s)" % ",".join(same_day[:4]) if same_day else ""))
        note = "%s official line %s %s has no published row" % (series, p["date"], p["start"])
        if any(documented(r, "Two official sources disagree")
               for r in mine if r["date"] == p["date"] and abs(int(r["start"][:2]) - int(p["start"][:2])) <= 1):
            documented_notes.append(note + " - it is the line the flagged row is stored against")
        else:
            problems.append(note)

    name_diffs = 0
    problems_before = len(problems)
    for row_index, i in used_by.items():
        r, p = mine[row_index], printed[i]
        if p.get("typo_year"):
            print("   YEAR TYPO (F1)  %s is published on %s rather than the printed %s"
                  % (r["id"], r["date"], p["date"]))
        if norm(r["name"])[:30] not in p["rest"] and p["rest"][:30] not in norm(r["name"]):
            name_diffs += 1
            print("   NAME WORD ORDER  %s %s | official: %s | dataset: %s"
                  % (r["id"], r["date"], p["rest"][:46], norm(r["name"])[:46]))
        money = [int(x.replace(",", "")) for x in re.findall(r"\$(\d[\d,]*)", p["rest"])]
        money = [m for m in money if m >= 100]  # ignore $10/$20 rake-discount notes
        if money and r.get("buy_in_usd") and r["buy_in_usd"] not in money:
            problems.append("%s %s: official line prints %s, dataset buy-in %s"
                            % (series, r["id"], ["$" + format(m, ",") for m in money], r["buy_in_usd"]))
        gtd = re.findall(r"\$([\d.]+)\s*(k|m)\b", p["rest"])
        for value, unit in gtd:
            want = int(float(value) * (1000 if unit.lower() == "k" else 1_000_000))
            if r.get("guarantee_usd") not in (None, want):
                problems.append("%s %s: official guarantee %s, dataset %s"
                                % (series, r["id"], want, r["guarantee_usd"]))
    if len(problems) > problems_before:
        # A money or guarantee mismatch on a row whose flag explains the same conflict
        # is on record; otherwise it is a failure.
        for r in mine:
            if documented(r, "Two official sources disagree"):
                for extra in problems[problems_before:]:
                    if r["id"] in extra:
                        problems.remove(extra)
                        documented_notes.append(extra + " - explained by the row's own flag")
    print("   matched one-for-one to a printed line: %d / %d (name word-order notes: %d)"
          % (len(used_by), len(mine), name_diffs))


def main():
    rows = json.load(open(os.path.join(DATA, "tournaments.json")))["rows"]
    problems, documented_notes = [], []
    pages = [("Venetian DeepStack Extravaganza IV", "v_dse_nov_page.txt", parse_event_page),
             ("Venetian DeepStack Extravaganza NYE", "v_dse_dec_page.txt", parse_event_page)]
    for series, snap, parser in pages:
        path = os.path.join(SNAP, snap)
        if not os.path.isfile(path):
            print("MISSING SNAPSHOT", snap)
            continue
        printed = parser(path)
        mine = [r for r in rows if r["series"] == series]
        print("\n== %s: official document prints %d dated lines, dataset publishes %d rows"
              % (series, len(printed), len(mine)))
        compare(series, printed, mine, problems, documented_notes)

    poster = os.path.join(SNAP, "wss_sched.txt")
    if os.path.isfile(poster):
        compare("Wynn Signature Series", parse_poster_rows(poster),
                [r for r in rows if r["series"] == "Wynn Signature Series"], problems, documented_notes)

    print("\n== unexplained mismatches: %d" % len(problems))
    for p in problems[:60]:
        print("  -", p)
    if not problems:
        print("  every published row matches a line printed on the official document")
    if documented_notes:
        print("\n== mismatches already recorded on the row (not defects, kept visible)")
        for n in documented_notes[:20]:
            print("  -", n)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
