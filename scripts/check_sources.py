#!/usr/bin/env python3
"""Re-check every official source and record what changed.

This is the change-monitoring job. It does three things:

1. Fetches each official URL listed in data/changelog.json.
2. Stores a SHA-256 checksum of the fetched bytes in data/snapshots.json.
3. For any URL whose checksum differs from the stored one, appends a dated
   entry to the snapshots list in data/changelog.json so the site can show it
   on the Change log page.

It deliberately does NOT scrape, copy or republish venue content, and it does
not change any tournament or hotel value. A changed source is a signal to
re-verify that source line by line against the official page; only a verified
reading may change a value.

Exit codes: 0 = no change (or dry run), 2 = one or more sources changed.

Usage:
    python3 scripts/check_sources.py            # fetch, update, report
    python3 scripts/check_sources.py --dry-run  # fetch and report, write nothing
"""
import hashlib
import json
import os
import ssl
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
CHANGELOG = os.path.join(DATA, "changelog.json")
SNAPSHOTS = os.path.join(DATA, "snapshots.json")

TIMEOUT = 60
USER_AGENT = "Poker1-source-monitor/1.0 (+https://github.com/karagemop466-tech/Poker1)"


def fetch(url):
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as resp:
        return resp.read()


def main(argv):
    dry = "--dry-run" in argv
    if not os.path.isfile(CHANGELOG):
        print("check_sources: data/changelog.json missing; run scripts/build_data.py first")
        return 1

    changelog = json.load(open(CHANGELOG, encoding="utf-8"))
    stored = {}
    if os.path.isfile(SNAPSHOTS):
        stored = json.load(open(SNAPSHOTS, encoding="utf-8")).get("snapshots", {})

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    changed, failed, unchanged = [], [], []

    for item in changelog.get("monitored", []):
        url = item["url"]
        try:
            body = fetch(url)
        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as exc:
            failed.append({"url": url, "label": item.get("label", url), "error": str(exc)})
            print("FAIL  %s (%s)" % (item.get("label", url), exc))
            continue
        digest = hashlib.sha256(body).hexdigest()
        prev = stored.get(url)
        if prev is None:
            entry = {"url": url, "label": item.get("label", url), "checksum": digest,
                     "bytes": len(body), "first_seen": now, "last_seen": now,
                     "last_changed": now}
            status = "new"
        elif prev.get("checksum") == digest:
            entry = dict(prev)
            entry["last_seen"] = now
            entry["bytes"] = len(body)
            status = "same"
        else:
            entry = dict(prev)
            entry["checksum"] = digest
            entry["bytes"] = len(body)
            entry["last_seen"] = now
            entry["last_changed"] = now
            entry["previous_checksum"] = prev.get("checksum")
            status = "changed"
        stored[url] = entry

        if status == "changed":
            changed.append(entry)
            print("CHANGED  %s" % item.get("label", url))
        elif status == "new":
            print("BASELINE %s" % item.get("label", url))
        else:
            unchanged.append(entry)
            print("same     %s" % item.get("label", url))

    if not dry:
        with open(SNAPSHOTS, "w", encoding="utf-8") as f:
            json.dump({"updated_on": now, "snapshots": stored}, f, indent=1, sort_keys=True)
            f.write("\n")
        if changed:
            for c in changed:
                changelog.setdefault("snapshots", []).append({
                    "date": now,
                    "source": c.get("label"),
                    "url": c["url"],
                    "change": ("Content checksum changed. Re-verify every row sourced from this "
                               "page line by line against the official page before changing any value."),
                    "previous_checksum": c.get("previous_checksum"),
                    "new_checksum": c.get("checksum"),
                })
            with open(CHANGELOG, "w", encoding="utf-8") as f:
                json.dump(changelog, f, indent=1)
                f.write("\n")

    print("\nchecked %d sources: %d changed, %d unchanged, %d unreachable"
          % (len(changelog.get("monitored", [])), len(changed), len(unchanged), len(failed)))
    if failed:
        print("unreachable sources:")
        for f in failed:
            print("  - %s: %s" % (f["label"], f["error"]))
    return 2 if changed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
