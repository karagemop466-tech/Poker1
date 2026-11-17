#!/usr/bin/env python3
"""Turn the monitoring result into a short Markdown report.

Used by .github/workflows/monitor.yml and readable on its own:
    python3 scripts/report_monitoring.py

The report answers three questions in the order a reviewer asks them: did the
official pages answer, did anything they print change, and which rows have to be
re-read as a result.
"""
import json
import os
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")


def load(name):
    path = os.path.join(DATA, name)
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main():
    mon = load("monitoring.json")
    ch = load("changes.json") or {"changed": [], "added": [], "removed": []}
    if not mon:
        print("No monitoring result is stored yet.")
        return 0
    check = mon.get("http_check") or {}
    print("- checked: %s on %s (%s)" % (mon.get("checked_at_utc") or mon["checked_at"],
                                       check.get("ran_on", "unknown host"),
                                       check.get("mode", "status-only")))
    if mon.get("sources_no_evidence"):
        print(f"- URLs cited by the data but with no fetch on record yet: {mon['sources_no_evidence']}")
    print(f"- evidence basis: {mon.get('kpi_basis', 'not recorded')}")
    print(f"- official sources reachable: {mon['sources_ok']} / {mon['sources_total']}")
    print(f"- unreachable: {mon['sources_unreachable']}")
    print(f"- HTTP errors: {mon['sources_http_error']}")
    if mon.get("routing_total"):
        print(f"- routing (OpenStreetMap) endpoints cited by the walking records: "
              f"{mon.get('routing_ok', 0)} / {mon['routing_total']}")
    statuses = Counter(v.get("content_status", "unknown") for v in (mon.get("sources") or {}).values())
    if statuses:
        print("- content verdict: " + ", ".join(f"{k} {v}" for k, v in sorted(statuses.items())))
    print(f"- pages re-rendered with no value change: "
          f"{mon.get('sources_raw_changed', 0) - mon.get('sources_facts_changed', 0)}")
    print(f"- pages whose published values changed: {mon.get('sources_facts_changed', 0)}")
    print(f"- rows marked for re-reading: {mon.get('rows_source_changed', 0)}")
    print(f"- dataset rows differing from the last verified snapshot - "
          f"changed: {len(ch['changed']) - mon.get('rows_source_changed', 0)}, "
          f"added: {len(ch['added'])}, removed: {len(ch['removed'])}")
    for row in ch["changed"][:40]:
        mark = "source changed" if row.get("source_url") else "value changed"
        print(f"  - {mark}: {row['id']} {row.get('name')} ({row.get('date', '-')})")
    for row in ch["added"][:40]:
        print(f"  - added {row['id']} {row['name']}")
    for row in ch["removed"][:40]:
        print(f"  - removed {row['id']} {row['name']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
