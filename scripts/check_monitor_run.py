#!/usr/bin/env python3
"""Decide whether a monitoring run is actually worth reading, and say so out loud.

Why this exists
---------------
The scheduled monitor has two quiet failure modes, both of which have happened here:

  * the weekly provenance job refuses to run (a host in ``data/sources.json`` is not on
    its allowlist), writes the refusal into ``data/monitor_last_run.txt``, and - before
    ``pipefail`` was added - left the job green while nothing had been checked; and
  * a run reaches none of the operator domains at all, so every verdict in
    ``data/monitoring.json`` is inherited from the last real fetch. That is the right
    fallback, but a reader of the site cannot tell it apart from a fresh check unless
    somebody says so.

This script turns both into a non-zero exit with a one-line reason, plus a warning when
the comparison is still running against a baseline written by the older, line-only
extractor (F83: that baseline cannot see a merged table cell move).

It reads the reports; it never writes them, so it is safe to run from a pull request.

Run:  python3 scripts/check_monitor_run.py [--json] [--max-age-days N]
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
REFUSAL = "Refusing to run"


def _load(name):
    path = os.path.join(DATA, name)
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _day(value):
    """Parse the date part of an ISO timestamp; None when it is missing or unusable."""
    if not value:
        return None
    try:
        return datetime.strptime(str(value)[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def age_days(value, today=None):
    """Whole days between a stored timestamp and today (UTC); None if unparseable."""
    d = _day(value)
    if d is None:
        return None
    return ((today or datetime.now(timezone.utc).date()) - d).days


def findings(mon=None, last_run_text=None, prov=None, today=None, max_age_days=7,
             stale_error_days=7):
    """Every verdict about this run, as (level, code, message), errors first.

    Kept as a pure function of the three inputs so the rules can be tested offline
    without touching the network or the committed reports.
    """
    out = []
    if mon is None:
        return [("error", "no-report",
                 "data/monitoring.json is missing: the monitor wrote no report, so nothing "
                 "here has been re-checked")]

    # 1. A refused provenance run. The refusal may be preceded by extractor noise, so the
    #    whole file is scanned rather than only the first line.
    if last_run_text and any(line.startswith(REFUSAL) for line in last_run_text.splitlines()):
        line = next(l for l in last_run_text.splitlines() if l.startswith(REFUSAL))
        out.append(("error", "provenance-refused",
                    "the official-source provenance run refused to run, so no snapshot behind "
                    "these rows was refreshed: %s" % line[:200]))

    total = mon.get("sources_total") or 0
    ok = mon.get("sources_ok") or 0
    prov_age = age_days((prov or {}).get("generated_utc"), today)
    if total and ok == 0:
        # Nothing was reached from this machine. That is allowed - the fallback exists -
        # but only while the fetch it falls back on is itself recent.
        if prov_age is None:
            out.append(("error", "no-evidence",
                        "this run reached 0 of %d official sources and no dated provenance fetch "
                        "is on file to fall back on" % total))
        elif prov_age > stale_error_days:
            out.append(("error", "no-evidence",
                        "this run reached 0 of %d official sources and the last real fetch is %d "
                        "days old; re-check before trusting any row" % (total, prov_age)))
        else:
            out.append(("warn", "fell-back",
                        "this run reached 0 of %d official sources; every verdict is inherited from "
                        "the provenance fetch of %s (%d day(s) old)"
                        % (total, str((prov or {}).get("generated_utc"))[:10], prov_age)))
    elif total and ok / total < 0.5:
        out.append(("warn", "mostly-unreachable",
                    "only %d of %d official sources answered this run; rows citing the rest carry "
                    "no fresh verdict" % (ok, total)))

    # 2. The report itself must not be older than the schedule it claims to keep.
    report_age = age_days(mon.get("checked_at_utc"), today)
    if report_age is not None and report_age > max_age_days:
        out.append(("error", "stale-report",
                    "data/monitoring.json is %d days old (checked %s): the scheduled re-check is "
                    "not running, or its result was never published"
                    % (report_age, str(mon.get("checked_at_utc"))[:10])))

    # 3. Comparison running on the pre-union baseline: honest, but not yet watching
    #    merged table cells, which is the defect class F83 came from.
    legacy = mon.get("sources_facts_legacy_baseline") or 0
    if legacy:
        out.append(("warn", "legacy-baseline",
                    "%d source(s) are still compared against a baseline written by the reading-order "
                    "extractor, so a value that only the layout render can see cannot move their "
                    "verdict yet; re-run with --accept-baseline after the flagged rows have been "
                    "read by hand" % legacy))

    errors = (prov or {}).get("error_count")
    if isinstance(errors, int) and total and errors > total / 2:
        out.append(("warn", "provenance-errors",
                    "the last provenance fetch reported an error for %d of %d official sources"
                    % (errors, total)))

    order = {"error": 0, "warn": 1}
    return sorted(out, key=lambda f: order.get(f[0], 9))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true", help="print the findings as JSON")
    ap.add_argument("--max-age-days", type=int, default=7,
                    help="how old data/monitoring.json may be before the run is an error (default 7)")
    ap.add_argument("--stale-error-days", type=int, default=7,
                    help="how old the fallback provenance fetch may be when this host reached nothing")
    args = ap.parse_args(argv)

    mon = _load("monitoring.json")
    prov = _load("change_log.json")
    last_run_path = os.path.join(DATA, "monitor_last_run.txt")
    last_run_text = None
    if os.path.isfile(last_run_path):
        with open(last_run_path, encoding="utf-8", errors="ignore") as f:
            last_run_text = f.read()

    out = findings(mon=mon, last_run_text=last_run_text, prov=prov,
                   today=datetime.now(timezone.utc).date(),
                   max_age_days=args.max_age_days, stale_error_days=args.stale_error_days)
    if args.json:
        print(json.dumps([{"level": l, "code": c, "message": m} for l, c, m in out], indent=1))
    else:
        if not out:
            print("check_monitor_run: OK - the run reported a fresh result and the provenance "
                  "archive did not refuse")
        for level, code, msg in out:
            print("check_monitor_run %s [%s]: %s" % (level.upper(), code, msg))
    return 1 if any(level == "error" for level, _, _ in out) else 0


if __name__ == "__main__":
    sys.exit(main())
