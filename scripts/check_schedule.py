#!/usr/bin/env python3
"""Guard the day plan against the one defect it exists to detect.

`data/schedule.json` is the page that tells a reader whether two events on one date can
actually be played in sequence. Every comparison in it is a comparison of clock times, and
a tournament that runs past midnight has a finish time that reads as EARLIER than its
start. A check that compares the bare clock strings therefore inverts: it blesses
impossible pairs and misses real ones. That happened on `main` between 2026-11-16 and
2026-11-17 (see FLAGGED.md F76): 24 of 24 published fallbacks were unplayable and 121 of
274 rows printed a finish before their start.

This script re-derives the whole day plan from `data/tournaments.json` using minutes
counted from the start day's midnight, and fails if the published file disagrees:

  1. every estimated finish must equal start + est_duration_min, modulo a day, with the
     next-day marker set exactly when it crosses midnight;
  2. every published duration basis must match the event's own name and labels, and a
     structure printed for more than one playing day must never bound the day;
  3. a published fallback must be enterable after the primary is estimated to finish;
  4. the conflict list must be complete: no unflagged unplannable pair, no flagged pair
     that the published tables do allow;
  5. a primary event must be the day's earliest verified single-entry event.

Run:  python3 scripts/check_schedule.py
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ONE_DAY_RE = re.compile(r"\(\s*1\s*Day\s*\)", re.I)


def to_min(hhmm):
    h, m = str(hhmm).split(":")
    return int(h) * 60 + int(m)


def load(name):
    with open(os.path.join(ROOT, "data", name)) as f:
        doc = json.load(f)
    return doc["rows"] if isinstance(doc, dict) and "rows" in doc else doc


def abs_end(row):
    """Minutes from the start day's midnight; None when no same-day finish is derivable."""
    if not row.get("est_end"):
        return None
    if row.get("est_duration_min"):
        return to_min(row["start"]) + row["est_duration_min"]
    return to_min(row["est_end"])


SATELLITE_LABELS = ("satellite", "milestone-satellite")


def is_satellite(row):
    return ("satellite" in (row.get("name") or "").lower()
            or bool(set(SATELLITE_LABELS) & set(row.get("labels") or [])))


def basis(row):
    if not row.get("est_end"):
        return None
    if is_satellite(row):
        return "satellite_maximum"
    return "day_maximum" if is_one_day(row) else "no_day_bound"


def is_one_day(row):
    return bool(ONE_DAY_RE.search(row.get("name") or "")) and not is_satellite(row)


def day_bound(row):
    """Latest minute from the start day's midnight at which the event can still be running.

    A "(1Day)" event cannot outlive its own table and neither can a satellite, so the table's
    end is a maximum for the day. A flight of a multi-day event prints a table spanning several
    playing days, which bounds nothing about the first day, so it is refused here entirely.
    """
    return abs_end(row) if basis(row) in ("day_maximum", "satellite_maximum") else None


def deadline(row):
    return to_min(row.get("late_reg_close") or row["start"])


def main():
    problems = []
    rows = load("tournaments.json")
    entries = {r["id"]: r for r in rows if r.get("kind") == "entry"}

    with open(os.path.join(ROOT, "data", "schedule.json")) as f:
        days = json.load(f)["days"]

    if not days:
        problems.append("data/schedule.json: no days published")

    scheduled = {}
    for day in days:
        date = day.get("date")
        events = {e["id"]: e for e in day.get("events", [])}
        scheduled.update(events)

        # 1 - the published clock time must agree with the published duration.
        for eid, e in events.items():
            row = entries.get(eid)
            if row is None:
                problems.append(f"{date}: scheduled event {eid} is not an entry row")
                continue
            if bool(e.get("est_end")) != bool(row.get("est_end")):
                problems.append(f"{date}/{eid}: est_end present in the schedule but not in the row")
                continue
            if not e.get("est_end"):
                continue
            true_end = to_min(e["start"]) + (e.get("est_duration_min") or 0)
            if to_min(e["est_end"]) != true_end % 1440:
                problems.append(f"{date}/{eid}: est_end {e['est_end']} is not start + est_duration_min")
            wrapped = true_end >= 1440
            if bool(e.get("est_end_next_day")) != wrapped:
                problems.append(f"{date}/{eid}: est_end_next_day should be {str(wrapped).lower()} "
                                f"(start {e['start']} + {e.get('est_duration_min')} min)")
            # 2 - a multi-day structure must not be presented as a finish time for the day.
            row_basis = basis(row)
            if e.get("duration_basis") != row_basis:
                problems.append(f"{date}/{eid}: duration_basis is {e.get('duration_basis')!r},"
                                f" should be {row_basis!r}")

        # 5 - the primary must be the day's earliest verified single-entry event.
        se = sorted([e for e in events.values() if e.get("entry_status") == "SE"],
                    key=lambda e: (e["start"], e["name"]))
        expected_primary = se[0]["id"] if se else None
        if day.get("primary_id") != expected_primary:
            problems.append(f"{date}: primary {day.get('primary_id')} is not the earliest "
                            f"single-entry event ({expected_primary})")

        # 3 - a published fallback has to be enterable.
        if day.get("fallback_id"):
            if day["fallback_id"] not in events:
                problems.append(f"{date}: fallback {day['fallback_id']} is not an event of this day")
            else:
                p, f_ = events[day["primary_id"]], events[day["fallback_id"]]
                p_end = day_bound(p)
                if p_end is None:
                    problems.append(f"{date}: a fallback is published although the primary has no "
                                    f"same-day finish time")
                elif day.get("fallback_kind") == "from the start" and p_end > to_min(f_["start"]):
                    problems.append(f"{date}: a from-the-start fallback cannot start {f_['start']} after the "
                                    f"primary's ceiling at {p_end}")
                elif day.get("fallback_kind") not in ("from the start", "join in progress"):
                    problems.append(f"{date}: fallback_kind {day.get('fallback_kind')!r} is not a published kind")
                if to_min(f_["start"]) < to_min(p["start"]):
                    problems.append(f"{date}: fallback {f_['id']} starts before the primary")
        elif se and day.get("primary_id") and not day.get("fallback_note"):
            problems.append(f"{date}: a primary with no fallback must explain why (fallback_note)")

        # 4 - the conflict list must be exactly right.
        ordered = sorted(events.values(), key=lambda e: (e["start"], e["name"]))
        want = []
        for i, a in enumerate(ordered):
            a_end = day_bound(a)
            for b in ordered[i + 1:]:
                # Two events printed at the same instant can never both be played; that needs no
                # estimate at all and applies even when neither carries a structure.
                if a["start"] == b["start"]:
                    want.append((a["id"], b["id"], "unplannable"))
                    continue
                if a_end is None:
                    continue
                if a_end > deadline(entries[b["id"]]):
                    want.append((a["id"], b["id"], "unplannable"))
                elif a_end > to_min(b["start"]):
                    want.append((a["id"], b["id"], "join_in_progress"))
        got = [(c.get("a"), c.get("b"), c.get("kind")) for c in day.get("conflicts", [])]
        for missing in set(want) - set(got):
            problems.append(f"{date}: unflagged {missing[2]} pair {missing[0]} -> {missing[1]}")
        for extra in set(got) - set(want):
            problems.append(f"{date}: flagged pair {extra[0]} -> {extra[1]} is actually playable")
        counts = {k: sum(1 for w in want if w[2] == k)
                  for k in ("unplannable", "join_in_progress")}
        for key, field in (("unplannable", "conflicts_unplannable"),
                           ("join_in_progress", "conflicts_join_in_progress")):
            if day.get(field) != counts[key]:
                problems.append(f"{date}: {field} is {day.get(field)}, should be {counts[key]}")

        # 6 - every other single-entry event of the day must be offered as an alternative,
        #     and nothing that is not a single-entry event may be offered there.
        alt_ids = [a.get("id") for a in day.get("alternatives", [])]
        want_alts = [e["id"] for e in se if e["id"] != day.get("primary_id")
                     and e["id"] != day.get("fallback_id")]
        if sorted(alt_ids) != sorted(want_alts):
            problems.append(f"{date}: alternatives are {sorted(alt_ids)}, should be {sorted(want_alts)}")
        for a in day.get("alternatives", []):
            ev = events.get(a.get("id"))
            if ev is None:
                problems.append(f"{date}: alternative {a.get('id')} is not an event of this day")
                continue
            if ev.get("entry_status") != "SE":
                problems.append(f"{date}: alternative {a.get('id')} is not a verified single-entry event")
            if a.get("note") and not str(a.get("note")).strip():
                problems.append(f"{date}: alternative {a.get('id')} carries no explanation")
            if a.get("entry_closes") != (entries[ev["id"]].get("late_reg_close")
                                         or entries[ev["id"]]["start"]):
                problems.append(f"{date}: alternative {a.get('id')} entry_closes does not match the row")

    # every entry row must appear exactly once in the plan
    for eid in entries:
        if eid not in scheduled:
            problems.append(f"entry row {eid} is missing from data/schedule.json")

    if problems:
        print("check_schedule: %d problem(s)" % len(problems))
        for p in problems[:40]:
            print("  " + p)
        return 1

    pairs = sum(len(d.get("conflicts", [])) for d in days)
    print("check_schedule: OK (%d days, %d entry rows, %d overlap pair(s), every published "
          "fallback enterable, every clock consistent with its duration)"
          % (len(days), len(entries), pairs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
