#!/usr/bin/env python3
"""Watch every official source URL and record when a document changes.

Fetches each URL in data/source_registry.json, hashes the response body and
compares it with the baseline stored in data/source_baseline.json. A document
whose body differs is flagged, and the flag is written to
data/source_changes.json so the site can show it.

Nothing here changes the tournament or hotel data. A change flag means a
document moved and the row that depends on it needs to be read again.

Run:  python3 scripts/monitor_sources.py [--update-baseline]
"""
import argparse
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
USER_AGENT = "Poker1SourceMonitor/1.0 (+https://github.com/karagemop466-tech/Poker1)"
TIMEOUT = 45

REGISTRY = os.path.join(DATA, "source_registry.json")
BASELINE = os.path.join(DATA, "source_baseline.json")
CHANGES = os.path.join(DATA, "source_changes.json")


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.status, r.read(), dict(r.headers)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--update-baseline", action="store_true",
                    help="record the current bodies as the new baseline and clear the change flags")
    args = ap.parse_args()

    with open(REGISTRY, encoding="utf-8") as f:
        registry = json.load(f)

    baseline = {}
    if os.path.isfile(BASELINE):
        try:
            with open(BASELINE, encoding="utf-8") as f:
                baseline = json.load(f).get("sources", {})
        except (ValueError, OSError):
            baseline = {}

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    results = []
    changed = 0
    failed = 0

    for src in registry.get("sources", []):
        key = src["key"]
        rec = {"key": key, "url": src["url"], "label": src["label"], "kind": src["kind"],
               "cadence": src["cadence"], "checked_at": now}
        try:
            status, body, headers = fetch(src["url"])
            digest = hashlib.sha256(body).hexdigest()
            rec["http_status"] = status
            rec["bytes"] = len(body)
            rec["sha256"] = digest
            rec["last_modified"] = headers.get("Last-Modified", "")
            old = baseline.get(key, {})
            old_hash = old.get("sha256")
            if old_hash is None:
                rec["status"] = "baseline"
            elif old_hash == digest:
                rec["status"] = "unchanged"
            else:
                rec["status"] = "changed"
                rec["previous_sha256"] = old_hash
                rec["previous_checked_at"] = old.get("checked_at")
                changed += 1
        except (urllib.error.URLError, urllib.error.HTTPError, OSError, ValueError) as e:
            rec["status"] = "error"
            rec["error"] = "%s: %s" % (type(e).__name__, e)
            failed += 1
        results.append(rec)
        print("%-28s %s" % (key, rec["status"]))

    if args.update_baseline:
        out = {"updated_at": now, "sources": {r["key"]: {"sha256": r.get("sha256"),
                                                         "checked_at": now,
                                                         "bytes": r.get("bytes")} for r in results}}
        with open(BASELINE, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=1)
        print("baseline updated")

    changes = {
        "checked_at": now,
        "total": len(results),
        "changed": changed,
        "failed": failed,
        "note": ("A changed document means the official source moved. The rows that depend on it need to be "
                 "read again before the values are treated as current. An error means the document could not "
                 "be fetched, which is different from a document that has not changed."),
        "results": results,
    }
    with open(CHANGES, "w", encoding="utf-8") as f:
        json.dump(changes, f, indent=1)
    print("wrote %s (%d changed, %d failed)" % (CHANGES, changed, failed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
