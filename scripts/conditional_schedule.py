#!/usr/bin/env python3
"""Build honest day plans: event duration and finish are not blind-table bounds.

This independent module does not write generated files. The owning integration
session can call it from build_data once shared-file handoff has occurred.
"""
from entry_evidence import load_archives, strict_single_entry_errors


def build_schedule(rows, verified_on, archives=None):
    """Build all-date starts, strict recommendations and conditional warnings.

    A fallback is possible only after ending or busting the first tournament,
    travelling, and registering in time; it is never a guaranteed sequence. All
    unordered same-day pairs are surfaced because neither actual finish is known.
    """
    days = {}
    continuations = {}
    for row in rows:
        if row.get("kind") == "entry":
            days.setdefault(row["date"], []).append(row)
        elif row.get("kind") == "continuation":
            # A restart is useful information, not another entry or a primary.
            days.setdefault(row["date"], [])
            continuations.setdefault(row["date"], []).append(row)
    if any(r.get("entry_status") == "SE" for events in days.values() for r in events):
        archives = load_archives() if archives is None else archives
        for events in days.values():
            for row in events:
                if row.get("entry_status") == "SE":
                    errors = strict_single_entry_errors(row, archives)
                    if errors:
                        raise ValueError("Unsupported SE event %s: %s" % (row.get("id"), "; ".join(errors)))
    plan = []
    for day_date in sorted(days):
        events = sorted(days[day_date], key=lambda e: (e["start"], e["name"], e["id"]))
        confirmed = [e for e in events if e.get("entry_status") == "SE"]
        primary = confirmed[0] if confirmed else None
        fallback = next((e for e in confirmed[1:] if e["start"] > primary["start"]), None) if primary else None
        alternatives = [{
            "id": e["id"], "start": e["start"], "name": e["name"],
            "buy_in_usd": e.get("buy_in_usd"), "guarantee_usd": e.get("guarantee_usd"),
            "entry_closes": e.get("late_reg_close"), "late_reg_published": bool(e.get("late_reg_close")),
            "note": "An alternative to the primary. Confirm registration and travel time; simultaneous play is not assumed.",
        } for e in confirmed[1:] if e is not fallback]
        conflicts = []
        for index, first in enumerate(events):
            for second in events[index + 1:]:
                simultaneous = first["start"] == second["start"]
                close = second.get("late_reg_close")
                deadline = ("late registration is printed through %s" % close if close else
                            "late-registration deadline not published")
                detail = ("%s starts %s; %s starts %s (%s). The first event's finish is unknown. "
                          "%sPlay the second only if the first has finished or you are eliminated, "
                          "and you can travel and register before the deadline." % (
                              first["name"], first["start"], second["name"], second["start"], deadline,
                              "Both cannot be started simultaneously. " if simultaneous else ""))
                conflicts.append({"a": first["id"], "b": second["id"],
                                  "kind": "simultaneous_start" if simultaneous else "potential_overlap",
                                  "a_start": first["start"], "b_start": second["start"],
                                  "b_late_reg_close": close, "a_end": None, "detail": detail})
        if not primary:
            note = "No strictly confirmed single-entry event on this date; no primary or fallback is recommended."
        elif not fallback:
            note = ("No later confirmed event is available as a conditional fallback. The primary's "
                    "finish is unknown; do not assume it fits another event or the next morning.")
        else:
            deadline = ("late registration %s" % fallback["late_reg_close"] if fallback.get("late_reg_close")
                        else "the start %s (late-registration deadline unverified)" % fallback["start"])
            note = ("Conditional fallback only: enter %s after the primary ends or you are eliminated, "
                    "and only if you can travel and register before %s. Actual finish, capacity and transfer "
                    "time are not known." % (fallback["name"], deadline))
        plan.append({
            "date": day_date,
            "events": [{
                "id": e["id"], "start": e["start"], "name": e["name"], "series": e.get("series"),
                "venue": e.get("venue"), "buy_in_usd": e.get("buy_in_usd"),
                "guarantee_usd": e.get("guarantee_usd"), "prize_text": e.get("prize_text"),
                "entry_status": e.get("entry_status"), "labels": e.get("labels", []),
                "late_reg_close": e.get("late_reg_close"),
                "est_end": None, "est_duration_min": None, "est_end_next_day": False, "duration_basis": None,
                "source": (e.get("sources") or [{}])[-1].get("url"),
            } for e in events],
            "continuations": [{
                "id": e["id"], "start": e["start"], "name": e["name"],
                "series": e.get("series"), "venue": e.get("venue"),
                "entry_status": e.get("entry_status"), "note": e.get("note"),
                "source": (e.get("sources") or [{}])[-1].get("url"),
            } for e in sorted(continuations.get(day_date, []),
                              key=lambda e: (e["start"], e["name"], e["id"]))],
            "continuation_note": ("Restarts are not new entry opportunities. If you qualified for a restart, "
                                  "it may overlap another event; the finish is unknown."
                                  if continuations.get(day_date) else None),
            "primary_id": primary["id"] if primary else None,
            "fallback_id": fallback["id"] if fallback else None,
            "fallback_kind": "conditional" if fallback else None,
            "fallback_note": note,
            "conflicts": conflicts,
            "conflicts_simultaneous_start": sum(c["kind"] == "simultaneous_start" for c in conflicts),
            "conflicts_potential_overlap": sum(c["kind"] == "potential_overlap" for c in conflicts),
            "alternatives": alternatives,
            "cross_day_warning": "Finishes are unknown. A previous day's event may continue into this date; check it before entering another tournament.",
        })
    starts = sorted(r["start"] for events in days.values() for r in events)
    return {"verified_on": verified_on, "days": plan,
            "earliest_listed_start": starts[0] if starts else None,
            "overlap_pairs": sum(len(day["conflicts"]) for day in plan),
            "note": "Primaries and fallbacks require affirmative official confirmation of every strict entry rule. "
                    "Finish times are unknown: a printed blind table is not a finish time or a hard upper bound. "
                    "Overlap warnings are conditional, not proof that two events can or cannot be played. "
                    "Allow for elimination or completion, travel, registration and previous-day events."}
