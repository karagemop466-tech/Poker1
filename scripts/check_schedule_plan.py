#!/usr/bin/env python3
"""Read-only chronology audit of the published poker day plan.

The generator stores estimated durations in minutes but also stores a clock-only
``est_end``. Comparing clock times alone loses the day rollover (11:10 + 15h45m
is 02:55 the next day, not 02:55 the same day). This audit recomputes absolute
intervals from each row's date, start and estimated duration and compares them
with the primary/fallback and overlap records in data/schedule.json.

This tool does not change the data or certify an actual finish time. Event
finishes are estimates derived from published structure information; reported
intersections are therefore estimated overlaps requiring review, not confirmed
finish-time conflicts.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Interval:
    start: int  # absolute minute, using date.toordinal() as the day index
    end: int


def clock_minutes(value: Any) -> int | None:
    if not isinstance(value, str):
        return None
    try:
        h, m = value.split(":", 1)
        hh, mm = int(h), int(m)
    except (ValueError, TypeError):
        return None
    if not (0 <= hh <= 23 and 0 <= mm <= 59):
        return None
    return hh * 60 + mm


def absolute_start(row: dict[str, Any]) -> int | None:
    start = clock_minutes(row.get("start"))
    if start is None or not row.get("date"):
        return None
    day = date.fromisoformat(row["date"]).toordinal()
    return day * 1440 + start


def interval_for(row: dict[str, Any]) -> Interval | None:
    start = absolute_start(row)
    duration = row.get("est_duration_min")
    if start is None or not isinstance(duration, int) or duration <= 0:
        return None
    return Interval(start, start + duration)


def format_absolute(minute: int) -> str:
    day_num, minute_of_day = divmod(minute, 1440)
    d = date.fromordinal(day_num)
    hh, mm = divmod(minute_of_day, 60)
    return f"{d.isoformat()} {hh:02d}:{mm:02d}"


def official_source(row: dict[str, Any]) -> str:
    for source in row.get("sources", []):
        url = source.get("url")
        if url and ("venetianlasvegas.com" in url or "wynnresorts.com" in url):
            return url
    return ""


def pair_key(a: str, b: str) -> tuple[str, str]:
    return tuple(sorted((a, b)))


def audit(tournaments: dict[str, Any], schedule: dict[str, Any]) -> dict[str, Any]:
    rows = tournaments.get("rows", [])
    by_id = {r.get("id"): r for r in rows if r.get("id")}
    intervals = {r["id"]: interval_for(r) for r in rows if r.get("id")}
    missing_duration = [
        r for r in rows
        if r.get("kind") == "entry" and interval_for(r) is None
    ]

    bad_fallbacks: list[dict[str, Any]] = []
    uncheckable_fallbacks: list[dict[str, Any]] = []
    recorded: set[tuple[str, str]] = set()

    for day in schedule.get("days", []):
        primary_id, fallback_id = day.get("primary_id"), day.get("fallback_id")
        if primary_id and fallback_id:
            primary, fallback = by_id.get(primary_id), by_id.get(fallback_id)
            if not primary or not fallback:
                uncheckable_fallbacks.append({
                    "date": day.get("date"), "primary_id": primary_id,
                    "fallback_id": fallback_id, "reason": "row id missing from tournaments.json",
                })
            else:
                p_int = intervals.get(primary_id)
                f_start = clock_minutes(fallback.get("start"))
                if not p_int or f_start is None:
                    uncheckable_fallbacks.append({
                        "date": day.get("date"), "primary_id": primary_id,
                        "fallback_id": fallback_id,
                        "reason": "start or estimated duration is not published",
                    })
                else:
                    abs_f_start = date.fromisoformat(day["date"]).toordinal() * 1440 + f_start
                    if abs_f_start < p_int.end:
                        bad_fallbacks.append({
                            "date": day["date"], "primary": primary,
                            "fallback": fallback, "primary_interval": p_int,
                            "fallback_start": abs_f_start,
                            "source": official_source(primary),
                        })

        for conflict in day.get("conflicts", []):
            a, b = conflict.get("a"), conflict.get("b")
            if a and b:
                recorded.add(pair_key(a, b))

    known_overlaps: list[dict[str, Any]] = []
    for i, a in enumerate(rows):
        if a.get("kind") != "entry" or not a.get("id"):
            continue
        a_start = absolute_start(a)
        if a_start is None:
            continue
        for b in rows[i + 1:]:
            if b.get("kind") != "entry" or not b.get("id"):
                continue
            b_start = absolute_start(b)
            if b_start is None:
                continue

            same_start = a_start == b_start
            if a_start < b_start:
                first, second = a, b
                first_start, second_start = a_start, b_start
            elif b_start < a_start:
                first, second = b, a
                first_start, second_start = b_start, a_start
            else:
                # The start collision is certain even when neither event publishes
                # enough structure for an estimated finish. Prefer a duration-bearing
                # row first when there is one, to show the estimate as evidence.
                a_int, b_int = intervals.get(a["id"]), intervals.get(b["id"])
                if a_int:
                    first, second = a, b
                elif b_int:
                    first, second = b, a
                else:
                    first, second = a, b
                first_start = second_start = a_start

            # A later event is known to overlap if it starts before the earlier
            # event's estimated end. The later event's own finish need not be
            # known. Identical scheduled starts are also a conflict even where
            # both durations are unknown.
            first_int = intervals.get(first["id"])
            duration_overlap = bool(first_int and second_start < first_int.end)
            if same_start or duration_overlap:
                second_int = intervals.get(second["id"])
                known_overlaps.append({
                    "a": first, "b": second,
                    "start_a": first_start,
                    "end_a": first_int.end if first_int else None,
                    "start_b": second_start,
                    "end_b": second_int.end if second_int else None,
                    "same_start": same_start,
                    "duration_overlap": duration_overlap,
                    "key": pair_key(first["id"], second["id"]),
                })

    same_day_overlaps = [
        item for item in known_overlaps if item["a"]["date"] == item["b"]["date"]
    ]
    cross_day_overlaps = [
        item for item in known_overlaps if item["a"]["date"] != item["b"]["date"]
    ]
    duration_overlaps = [item for item in known_overlaps if item["duration_overlap"]]
    same_start_collisions = [item for item in known_overlaps if item["same_start"]]
    expected_same_day = {item["key"] for item in same_day_overlaps}
    expected_cross_day = {item["key"] for item in cross_day_overlaps}
    expected_all = expected_same_day | expected_cross_day
    missing_overlap_flags = expected_same_day - recorded
    missing_cross_day_flags = expected_cross_day - recorded
    recorded_not_reproduced = recorded - expected_all

    end_mismatches = []
    for row in rows:
        interval = intervals.get(row.get("id"))
        if not interval:
            continue
        expected_end = interval.end % 1440
        stored_end = clock_minutes(row.get("est_end"))
        if stored_end is not None and expected_end != stored_end:
            end_mismatches.append({
                "id": row.get("id"), "date": row.get("date"),
                "name": row.get("name"), "expected_end": expected_end,
                "stored_end": row.get("est_end"),
            })

    overlap_by_key = {item["key"]: item for item in known_overlaps}
    return {
        "rows": len(rows),
        "known_duration_rows": sum(1 for interval in intervals.values() if interval is not None),
        "missing_duration_rows": missing_duration,
        "primary_fallback_pairs": sum(
            1 for d in schedule.get("days", []) if d.get("primary_id") and d.get("fallback_id")
        ),
        "bad_fallbacks": bad_fallbacks,
        "uncheckable_fallbacks": uncheckable_fallbacks,
        "overlaps": known_overlaps,
        "duration_overlaps": duration_overlaps,
        "same_start_collisions": same_start_collisions,
        "same_day_overlaps": same_day_overlaps,
        "cross_day_overlaps": cross_day_overlaps,
        "recorded_conflicts": recorded,
        "missing_overlap_flags": [overlap_by_key[k] for k in sorted(missing_overlap_flags)],
        "missing_cross_day_flags": [overlap_by_key[k] for k in sorted(missing_cross_day_flags)],
        "recorded_not_reproduced": sorted(recorded_not_reproduced),
        "end_mismatches": end_mismatches,
    }


def self_test() -> None:
    # A 15h45m event beginning at 11:10 ends at 02:55 on the following day.
    start = clock_minutes("11:10")
    assert start is not None
    interval = Interval(date(2026, 11, 25).toordinal() * 1440 + start,
                        date(2026, 11, 25).toordinal() * 1440 + start + 945)
    assert format_absolute(interval.end) == "2026-11-26 02:55"
    fallback = date(2026, 11, 25).toordinal() * 1440 + clock_minutes("17:10")
    assert fallback < interval.end  # same-day 17:10 is before next-day 02:55

    # An event estimated to end exactly at a later start is sequential, not overlapping.
    primary_start = date(2026, 11, 25).toordinal() * 1440 + clock_minutes("11:10")
    short = Interval(primary_start, primary_start + 360)
    later_start = date(2026, 11, 25).toordinal() * 1440 + clock_minutes("17:10")
    assert short.end == later_start
    assert not (max(short.start, later_start) < min(short.end, later_start + 240))

    # Exercise the actual audit path: same-day fallback and next-day overlap.
    fixture_rows = [
        {"id": "p", "kind": "entry", "date": "2026-11-25", "start": "11:10",
         "est_duration_min": 945, "est_end": "02:55"},
        {"id": "f", "kind": "entry", "date": "2026-11-25", "start": "17:10",
         "est_duration_min": 60, "est_end": "18:10"},
        {"id": "n", "kind": "entry", "date": "2026-11-26", "start": "02:30",
         "est_duration_min": 60, "est_end": "03:30"},
        {"id": "u", "kind": "entry", "date": "2026-11-25", "start": "09:00",
         "est_duration_min": None, "est_end": None},
        {"id": "v", "kind": "entry", "date": "2026-11-25", "start": "09:00",
         "est_duration_min": None, "est_end": None},
    ]
    fixture_schedule = {"days": [
        {"date": "2026-11-25", "primary_id": "p", "fallback_id": "f", "conflicts": []},
        {"date": "2026-11-26", "primary_id": "n", "conflicts": []},
    ]}
    checked = audit({"rows": fixture_rows}, fixture_schedule)
    assert len(checked["bad_fallbacks"]) == 1
    assert len(checked["same_day_overlaps"]) == 2
    assert len(checked["duration_overlaps"]) == 2
    assert len(checked["same_start_collisions"]) == 1
    assert not checked["same_start_collisions"][0]["duration_overlap"]
    assert len(checked["cross_day_overlaps"]) == 1
    assert len(checked["missing_overlap_flags"]) == 2
    assert len(checked["missing_cross_day_flags"]) == 1
    assert not checked["recorded_not_reproduced"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="run rollover, sequence and overlap fixtures")
    parser.add_argument("--limit", type=int, default=30, help="maximum examples per finding type (default: 30)")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        print("check_schedule_plan self-test: PASS (midnight rollover, sequential boundary, same-start and cross-day cases)")
        return 0

    tournaments = json.loads((ROOT / "data/tournaments.json").read_text())
    schedule = json.loads((ROOT / "data/schedule.json").read_text())
    result = audit(tournaments, schedule)
    print("Read-only schedule chronology audit (estimated durations; not official finish times)")
    print(f"Tournament rows: {result['rows']}")
    print(f"Rows with an estimated duration: {result['known_duration_rows']}")
    print(f"Entry rows without a usable start/duration: {len(result['missing_duration_rows'])}")
    print(f"Days with a primary + fallback: {result['primary_fallback_pairs']}")
    print(f"Fallbacks starting before the primary's absolute estimated finish: {len(result['bad_fallbacks'])}")
    print(f"Scheduled conflict pairs (duration overlap or identical start): {len(result['overlaps'])}")
    print(f"  pairs supported by a stored duration estimate: {len(result['duration_overlaps'])}")
    print(f"  identical scheduled start pairs: {len(result['same_start_collisions'])}")
    print(f"  same-day pairs: {len(result['same_day_overlaps'])}")
    print(f"  cross-day pairs: {len(result['cross_day_overlaps'])}")
    print(f"Same-day pairs absent from schedule.json conflicts: {len(result['missing_overlap_flags'])}")
    print(f"Cross-day pairs absent from day-local conflict records: {len(result['missing_cross_day_flags'])}")
    print(f"Stored conflict pairs not reproduced by known durations: {len(result['recorded_not_reproduced'])}")
    print(f"Rows whose est_end disagrees with start + duration modulo one day: {len(result['end_mismatches'])}")

    for item in result["bad_fallbacks"][:max(0, args.limit)]:
        p, f = item["primary"], item["fallback"]
        print("\nINVALID FALLBACK (estimate):")
        print(f"  {item['date']} primary {p['id']} {p['start']} {p['name']}")
        print(f"  estimated finish {format_absolute(item['primary_interval'].end)}")
        print(f"  fallback {f['id']} {f['start']} {f['name']}")
        if item["source"]:
            print(f"  official schedule/structure source: {item['source']}")

    for item in result["missing_overlap_flags"][:max(0, args.limit)]:
        a, b = item["a"], item["b"]
        if item["same_start"]:
            label = ("UNFLAGGED IDENTICAL STARTS (duration unknown)" if not item["duration_overlap"]
                     else "UNFLAGGED IDENTICAL STARTS (also overlaps under estimate)")
            print(f"\n{label}:")
            print(f"  {a['date']} {a['start']} {a['id']} {a['name']}")
            print(f"  {b['date']} {b['start']} {b['id']} {b['name']}")
        else:
            print("\nUNFLAGGED SAME-DAY ESTIMATED OVERLAP:")
            print(f"  {a['date']} {a['start']} {a['id']} {a['name']}")
            print(f"    estimated interval {format_absolute(item['start_a'])} to {format_absolute(item['end_a'])}")
            print(f"  {b['date']} {b['start']} {b['id']} {b['name']}")
            b_end = format_absolute(item["end_b"]) if item["end_b"] is not None else "finish unknown"
            print(f"    begins {format_absolute(item['start_b'])}; {b_end}")
        print(f"  source: {official_source(a) or official_source(b)}")

    for item in result["cross_day_overlaps"][:max(0, args.limit)]:
        a, b = item["a"], item["b"]
        print("\nCROSS-DAY ESTIMATED OVERLAP:")
        print(f"  {a['date']} {a['start']} {a['id']} {a['name']}")
        print(f"    estimated finish {format_absolute(item['end_a'])}")
        print(f"  {b['date']} {b['start']} {b['id']} {b['name']}")
        print(f"  source: {official_source(a) or official_source(b)}")

    if result["recorded_not_reproduced"]:
        print("\nStored conflicts not reproduced by known start/duration evidence:")
        for a, b in result["recorded_not_reproduced"][:max(0, args.limit)]:
            print(f"  {a} / {b}")

    print("\nInterpretation: duration-derived conflicts are provisional because finishes are estimates; "
          "identical scheduled starts are certain start-time conflicts. Rows without a duration are "
          "indeterminate as to finish, not conflict-free.")
    # A non-zero status is intentional: an independent audit has found that the
    # checked-in day plan does not represent its own estimated timeline faithfully.
    return 1 if (result["bad_fallbacks"] or result["missing_overlap_flags"]
                or result["missing_cross_day_flags"] or result["end_mismatches"]
                or result["uncheckable_fallbacks"]) else 0


if __name__ == "__main__":
    sys.exit(main())
