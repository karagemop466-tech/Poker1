#!/usr/bin/env python3
"""Check the official source URLs and report which rows changed.

Two jobs:

1. Source monitoring - every official URL used by the dataset is requested and
   the HTTP status is recorded. A source that stops answering is the earliest
   warning that a published row may be stale.
2. Changed-row detection - each row in data/tournaments.json is fingerprinted
   and compared with data/row_snapshot.json. Added, removed and edited rows are
   listed so a reviewer sees exactly what moved since the last verified build.

The script never fails the build on a network problem: unreachable hosts are
reported as "unreachable", not as an error, because the sandbox and any
rate-limited network can be offline. Run:

    python3 scripts/monitor_sources.py            # write data/monitoring.json
    python3 scripts/monitor_sources.py --print    # also print a summary
"""
import json
import os
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
TIMEOUT = 25


def load(name):
    path = os.path.join(DATA, name)
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def fingerprint(row):
    return {
        "date": row["date"], "start": row["start"], "name": row["name"], "venue": row["venue"],
        "series": row["series"], "buy_in_usd": row["buy_in_usd"], "guarantee_usd": row["guarantee_usd"],
        "entry_status": row["entry_status"], "buy_in": row["rules"]["fee"]["value"],
        "flags": len(row.get("flags") or []),
    }


def check_url(url):
    started = time.time()
    try:
        req = Request(url, method="GET", headers={"User-Agent": "Poker1-source-monitor/1.0"})
        with urlopen(req, timeout=TIMEOUT) as resp:
            code = getattr(resp, "status", 200)
            resp.read(2048)
        return {"status": "ok" if 200 <= code < 400 else "http-error", "http_status": code,
                "elapsed_ms": int((time.time() - started) * 1000), "error": None}
    except HTTPError as e:
        return {"status": "http-error", "http_status": e.code,
                "elapsed_ms": int((time.time() - started) * 1000), "error": str(e)}
    except (URLError, OSError, ValueError) as e:  # noqa: BLE001 - network conditions vary
        return {"status": "unreachable", "http_status": None,
                "elapsed_ms": int((time.time() - started) * 1000), "error": str(e)}


def main():
    as_print = "--print" in sys.argv
    tournaments = load("tournaments.json")
    if not tournaments:
        print("monitor: data/tournaments.json is missing; run scripts/build_data.py first", file=sys.stderr)
        return 1

    urls = {s["url"] for r in tournaments["rows"] for s in (r.get("sources") or [])}
    # The hotel and walking sources answer the "did a fee, a tax, a route or a rate change?" question for the
    # non-tournament half of the site, so they are monitored on the same schedule.
    for name in ("hotels.json", "walking.json"):
        doc = load(name)
        for row in (doc or {}).get("rows", []):
            for src in (row.get("sources") or []):
                if src.get("url"):
                    urls.add(src["url"])
            if row.get("route_link"):
                urls.add(row["route_link"])
    for entry in (load("rates.json") or {}).get("entries", []):
        if entry.get("source"):
            urls.add(entry["source"])
    urls = sorted(urls)
    checked = {}
    for url in urls:
        checked[url] = check_url(url)
        if as_print:
            print("  %-9s %s" % (checked[url]["status"], url))

    snapshot = load("row_snapshot.json")
    changes = {"added": [], "removed": [], "changed": []}
    current = {r["id"]: fingerprint(r) for r in tournaments["rows"]}
    if snapshot:
        old = snapshot.get("rows", {})
        for rid, fp in current.items():
            if rid not in old:
                changes["added"].append({"id": rid, "name": fp["name"], "date": fp["date"]})
            elif old[rid] != fp:
                diff = {k: [old[rid].get(k), fp.get(k)] for k in fp if old[rid].get(k) != fp.get(k)}
                changes["changed"].append({"id": rid, "name": fp["name"], "date": fp["date"], "diff": diff})
        for rid, fp in old.items():
            if rid not in current:
                changes["removed"].append({"id": rid, "name": fp.get("name"), "date": fp.get("date")})

    checked_at = time.strftime("%Y-%m-%d", time.gmtime())
    ok = sum(1 for v in checked.values() if v["status"] == "ok")
    # A check that reaches nothing at all is a statement about the machine that ran it, not about the
    # official pages. Mark it so the site never presents a network blackout as "every source is down".
    blackout = bool(checked) and ok == 0 and all(
        v["status"] == "unreachable" and (v.get("error") or "").startswith("<urlopen error")
        for v in checked.values())
    result = {
        "checked_at": checked_at,
        "sources_total": len(checked),
        "sources_ok": ok,
        "sources_unreachable": sum(1 for v in checked.values() if v["status"] == "unreachable"),
        "sources_http_error": sum(1 for v in checked.values() if v["status"] == "http-error"),
        "rows_total": len(current),
        "rows_changed": len(changes["changed"]),
        "rows_added": len(changes["added"]),
        "rows_removed": len(changes["removed"]),
        "sources": checked,
        "network_unavailable": blackout,
        "note": "Status is the HTTP result of fetching each official URL on the date shown. "
                "'unreachable' means the host did not answer from the machine that ran the check; it does "
                "not by itself mean the page changed."
                + ("" if not blackout else
                   " This run reached none of the official hosts at all (every attempt failed at the TLS"
                   " or DNS layer), so it is a statement about the network of the machine that ran the"
                   " check and not about the sources. The scheduled GitHub Actions job reaches the"
                   " operator domains; its provenance result is in data/change_log.json."),
    }
    with open(os.path.join(DATA, "monitoring.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, indent=1)

    with open(os.path.join(DATA, "changes.json"), "w", encoding="utf-8") as f:
        json.dump({"checked_at": checked_at, **changes}, f, indent=1)

    if as_print:
        print("monitor: %d/%d sources ok, %d rows changed, %d added, %d removed"
              % (ok, len(checked), len(changes["changed"]), len(changes["added"]), len(changes["removed"])))
    else:
        print("monitor: %d/%d sources ok; wrote data/monitoring.json and data/changes.json"
              % (ok, len(checked)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
