#!/usr/bin/env python3
"""Turn the monitoring result into a short Markdown report.

Used by .github/workflows/monitor.yml and readable on its own:
    python3 scripts/report_monitoring.py
"""
import json
import os

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
    print(f"- sources reachable: {mon['sources_ok']} / {mon['sources_total']}")
    print(f"- unreachable: {mon['sources_unreachable']}")
    print(f"- HTTP errors: {mon['sources_http_error']}")
    print(f"- rows changed: {len(ch['changed'])}, added: {len(ch['added'])}, removed: {len(ch['removed'])}")
    for row in ch["changed"][:40]:
        print(f"  - changed {row['id']} {row['name']}")
    for row in ch["added"][:40]:
        print(f"  - added {row['id']} {row['name']}")
    for row in ch["removed"][:40]:
        print(f"  - removed {row['id']} {row['name']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
