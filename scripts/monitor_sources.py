#!/usr/bin/env python3
"""Re-check every official source URL and mark the rows whose source changed.

Three jobs, in the order a reviewer reads them:

1. **Availability.** Every official URL cited by the dataset is requested and its
   HTTP result recorded. A source that stops answering is the earliest warning
   that a published row may be stale.
2. **Content.** With ``--content`` the body of each answer is also read, converted
   to text and hashed - once for the raw page and once for the *published facts*
   on the page (money amounts, percentages, dates, start times and entry-rule
   words). Operator pages rotate promotions, cookie banners and cache-busting
   markup on every fetch, so the raw hash alone cries wolf; the facts hash is the
   one that means "a number or a rule printed on this page moved". The comparison
   point is ``data/source_baseline.json``.
3. **Row marking.** Any source whose facts changed is mapped back to every row
   that cites it - tournament rows (including the structure-sheet URL stored in
   each rule object), hotel rows, dated rate quotes and walking records - and the
   affected rows are written into ``data/changes.json`` as ``changed`` entries,
   which the Monitoring page renders. That is what "mark rows whose source
   changed" means here: the mark is produced by the check, not by hand.

When the machine running this script has no route to the operator domains (any
sandbox, or a CI job on a network-restricted runner), the check does not pretend
otherwise: the HTTP channel reports that, and the verdict falls back on the most
recent *real* fetch, which is the provenance job ``scripts/check_source_facts.py``
runs on GitHub Actions and records in ``data/change_log.json``. ``kpi_basis`` in
the output always names which evidence the counts come from and when it was taken,
so a reader never mistakes "this host has no network" for "these pages are down".

Usage:
    python3 scripts/monitor_sources.py                  # availability only (fast; used by PR validation)
    python3 scripts/monitor_sources.py --content        # availability + content change detection
    python3 scripts/monitor_sources.py --print          # also print a per-URL line
    python3 scripts/monitor_sources.py --update-snapshot # rewrite data/row_snapshot.json from the dataset
    python3 scripts/monitor_sources.py --accept-baseline # accept the current content as the new baseline
"""
import argparse
import hashlib
import json
import os
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import check_source_facts as csf  # noqa: E402  (reused: fetch, text extraction, facts signature)

TIMEOUT = 30
# Cap the body read. A schedule page is ~270 KB of markup and a structure sheet is
# a few hundred KB of PDF; the cap only exists so one pathological response cannot
# exhaust the runner, and a page that hits it is recorded as truncated so the
# monitor never silently compares a prefix against a full document.
BODY_CAP = 4_000_000
BASELINE = os.path.join(DATA, "source_baseline.json")
CHANGE_LOG = os.path.join(DATA, "change_log.json")
# A browser-like agent, because the operators' WAFs reject a bare script agent
# and the monitor must not report "unreachable" for what is really "blocked".
USER_AGENT = csf.USER_AGENT


def load(name):
    path = os.path.join(DATA, name)
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def sha(value):
    if value is None:
        return None
    if isinstance(value, str):
        value = value.encode("utf-8")
    return hashlib.sha256(value).hexdigest()


def fingerprint(row):
    """The published values of a row, in the shape the snapshot file stores."""
    return {
        "date": row["date"], "start": row["start"], "name": row["name"], "venue": row["venue"],
        "series": row["series"], "buy_in_usd": row["buy_in_usd"], "guarantee_usd": row["guarantee_usd"],
        "entry_status": row["entry_status"], "buy_in": row["rules"]["fee"]["value"],
        "flags": len(row.get("flags") or []),
    }


def urls_of(obj):
    """Every source URL attached to a data object, at any depth under 'sources'/'source'."""
    found = []
    srcs = obj.get("sources")
    if isinstance(srcs, list):
        for s in srcs:
            if isinstance(s, dict) and s.get("url"):
                found.append(s["url"])
    single = obj.get("source")
    if isinstance(single, dict) and single.get("url"):
        found.append(single["url"])
    elif isinstance(single, str) and single.startswith("https://"):
        found.append(single)
    rules = obj.get("rules")
    if isinstance(rules, dict):
        for rule in rules.values():
            if isinstance(rule, dict) and isinstance(rule.get("source"), dict) and rule["source"].get("url"):
                found.append(rule["source"]["url"])
    return found


def is_official(url):
    """True for the operator domains whose pages publish the prices and rules."""
    from urllib.parse import urlparse
    host = (urlparse(url).netloc or "").lower()
    return host in csf.OFFICIAL_HOSTS


def collect_dataset():
    """Return (urls -> list of row references, rows_by_id) for everything the site publishes."""
    doc_refs = {}

    def add(url, kind, ident, label, extra):
        if not url or not url.startswith("http"):
            return
        doc_refs.setdefault(url, []).append({"kind": kind, "id": ident, "label": label, **extra})

    tournaments = load("tournaments.json") or {"rows": []}
    for row in tournaments["rows"]:
        for url in urls_of(row):
            add(url, "tournament", row["id"], row["name"], {"date": row["date"]})
    hotels = load("hotels.json") or {"rows": []}
    for row in hotels["rows"]:
        for url in urls_of(row):
            add(url, "hotel", row["id"], row["name"], {})
    rates = load("rates.json") or {"entries": []}
    for index, entry in enumerate(rates["entries"], 1):
        url = entry.get("source")
        add(url, "rate", "rate%02d" % index, "%s %s to %s" % (
            entry.get("property"), entry.get("arrival"), entry.get("departure")), {})
    walking = load("walking.json") or {"rows": []}
    for index, row in enumerate(walking["rows"], 1):
        for url in urls_of(row):
            add(url, "walking", "w%02d" % index, "%s -> %s" % (row.get("from"), row.get("to")), {})
        add(row.get("route_link"), "walking", "w%02d" % index,
            "%s -> %s" % (row.get("from"), row.get("to")), {})
    # The Strip-room survey (MGM Grand, Mandalay Bay, Horseshoe, closure checks) is monitored the
    # same way: a fee or a schedule that moves there is a published value that moved.
    strips = load("strip_rooms.json") or {}
    for group in ("rooms", "formats"):
        for index, item in enumerate(strips.get(group, []), 1):
            for src in (item.get("sources") or []):
                add(src.get("url"), "strip-room", "%s%02d" % (group, index), item.get("name") or item.get("property"), {})
    # The other-rooms survey (pages/other-rooms.html) publishes an event row per recurring format
    # and a finding per room, each with its own official citations. Neither was monitored, so a
    # room's "$120 buy-in" or its "no poker room published" claim could go stale unseen.
    others = load("other_rooms.json") or {}
    for group, prefix in (("events", "or-ev"), ("rooms", "or-rm")):
        for index, item in enumerate(others.get(group, []), 1):
            ident = item.get("id") or "%s%02d" % (prefix, index)
            for src in (item.get("sources") or []):
                add(src.get("url"), "other-room", ident, item.get("name") or ident, {})
            add(item.get("source"), "other-room", ident, item.get("name") or ident, {})
    daily = load("daily.json") or {"rows": []}
    for index, row in enumerate(daily["rows"], 1):
        for url in urls_of(row):
            add(url, "daily", "d%02d" % index, row.get("name"), {})
    for row in (load("venues.json") or {"rows": []})["rows"]:
        for url in urls_of(row):
            add(url, "venue", row.get("id"), row.get("name"), {})
    return doc_refs, tournaments["rows"]


def check_url(url, want_body):
    started = time.time()
    record = {"status": "unreachable", "http_status": None, "elapsed_ms": None,
              "error": None, "bytes": None, "sha256": None, "facts_sha256": None, "facts_count": None}
    try:
        req = Request(url, method="GET", headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/pdf,application/xhtml+xml,*/*",
            "Accept-Language": "en-US,en;q=0.9",
        })
        with urlopen(req, timeout=TIMEOUT) as resp:
            code = getattr(resp, "status", 200)
            body = resp.read(BODY_CAP if want_body else 2048)
        record["status"] = "ok" if 200 <= code < 400 else "http-error"
        record["http_status"] = code
        record["elapsed_ms"] = int((time.time() - started) * 1000)
        if want_body and 200 <= code < 400:
            record["truncated"] = len(body) >= BODY_CAP
            text = csf.to_text(url, body)
            facts = csf.facts_signature(text)
            record["bytes"] = len(body)
            record["sha256"] = sha(text)
            record["facts_sha256"] = sha("\n".join(facts))
            record["facts_count"] = len(facts)
    except HTTPError as e:
        record["status"] = "http-error"
        record["http_status"] = e.code
        record["elapsed_ms"] = int((time.time() - started) * 1000)
        record["error"] = str(e)
    except (URLError, OSError, ValueError) as e:  # noqa: BLE001 - network conditions vary
        record["status"] = "unreachable"
        record["elapsed_ms"] = int((time.time() - started) * 1000)
        record["error"] = "%s: %s" % (type(e).__name__, e)
    return record


def provenance_findings():
    """Fold the last real fetch (scripts/check_source_facts.py on Actions) into url-keyed findings."""
    log = load("change_log.json")
    if not isinstance(log, dict):
        return {}, None
    out = {}
    for src in log.get("sources", []):
        url = src.get("url")
        if not url:
            continue
        out[url] = {
            "source_id": src.get("id"),
            "label": src.get("label"),
            "provenance_checked_at": src.get("last_checked_utc"),
            "provenance_http_status": src.get("http_status"),
            "provenance_error": src.get("error"),
            "provenance_sha256": src.get("sha256"),
            "raw_changed": bool(src.get("changed")),
            "facts_changed": bool(src.get("facts_changed")),
            "facts_checked": src.get("facts_checked"),
        }
    return out, log.get("generated_utc")


def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--print", dest="as_print", action="store_true")
    ap.add_argument("--write-report", dest="write_report", action="store_true",
                    help="publish data/monitoring.json and data/changes.json (the scheduled job); "
                         "without it the run only reports, so a validation run cannot overwrite a "
                         "real result or dirty the tree")
    ap.add_argument("--content", action="store_true",
                    help="fetch and hash each page body, not just its HTTP status")
    ap.add_argument("--update-snapshot", action="store_true",
                    help="rewrite data/row_snapshot.json from the current dataset")
    ap.add_argument("--accept-baseline", action="store_true",
                    help="record the content seen on this run as the new comparison baseline")
    ap.add_argument("--seed-baseline", action="store_true",
                    help="build the comparison baseline from data/change_log.json's stored facts "
                         "signatures (the last real fetch) instead of a new HTTP round-trip")
    args = ap.parse_args()

    if args.seed_baseline:
        log = load("change_log.json")
        if not isinstance(log, dict):
            print("monitor: data/change_log.json is missing; cannot seed a baseline", file=sys.stderr)
            return 1
        seeded = {"generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                  "note": "Facts baseline seeded from the last provenance fetch "
                          "(data/change_log.json, generated " + str(log.get("generated_utc")) + "). "
                          "Only the published-facts hash is stored, because the provenance job "
                          "sometimes hashes the raw body and sometimes the extracted text; comparing "
                          "facts is what decides whether a published value moved. "
                          "scripts/monitor_sources.py --content --accept-baseline replaces this file "
                          "with hashes of both.",
                  "sources": {}}
        for src in log.get("sources", []):
            url = src.get("url")
            if not url:
                continue
            facts = src.get("facts_signature") or []
            seeded["sources"][url] = {
                "sha256": None,
                "facts_sha256": sha("\n".join(facts)) if facts else None,
                "facts_count": len(facts),
                "checked_at_utc": src.get("last_checked_utc"),
                "source_id": src.get("id"),
            }
        with open(BASELINE, "w", encoding="utf-8") as f:
            json.dump(seeded, f, indent=1)
            f.write("\n")
        print("monitor: baseline seeded with %d facts hashes from %s"
              % (len(seeded["sources"]), log.get("generated_utc")))
        return 0

    tournaments = load("tournaments.json")
    if not tournaments:
        print("monitor: data/tournaments.json is missing; run scripts/build_data.py first", file=sys.stderr)
        return 1

    doc_refs, rows = collect_dataset()
    # Also re-check every URL listed in the provenance manifest, even one no row
    # cites today (a page a row stops citing is exactly the page a reviewer wants
    # to know has gone away).
    for source in (load("sources.json") or {}).get("sources", []):
        if source.get("url") and source.get("active") is not False:
            doc_refs.setdefault(source["url"], [])
    urls = sorted(doc_refs)

    # The snapshot of row values, which is what makes "this row moved" a fact
    # rather than a recollection. It must be rebuilt whenever the dataset is.
    if args.update_snapshot:
        snapshot = {"generated_on": time.strftime("%Y-%m-%d", time.gmtime()),
                    "row_count": len(rows),
                    "note": "Fingerprints of data/tournaments.json at the last verified build. "
                            "Regenerate with `python3 scripts/monitor_sources.py --update-snapshot` "
                            "after scripts/build_data.py is re-run.",
                    "rows": {r["id"]: fingerprint(r) for r in rows}}
        with open(os.path.join(DATA, "row_snapshot.json"), "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=1)
            f.write("\n")
        print("monitor: data/row_snapshot.json rewritten with %d rows" % len(rows))

    baseline = load("source_baseline.json") or {"sources": {}}
    checked = {}
    for url in urls:
        checked[url] = check_url(url, args.content)
        if args.as_print:
            print("  %-12s %s" % (checked[url]["status"], url))
    http_reachable = sum(1 for v in checked.values() if v["status"] != "unreachable")

    prov, prov_at = provenance_findings()
    for url, record in checked.items():
        p = prov.get(url)
        if p:
            record.update(p)
        base = (baseline.get("sources") or {}).get(url)
        # Decide the content verdict. A fetch taken now beats the provenance job's
        # last run; with no network the provenance job is the newest real fetch.
        record["content_status"] = "unknown"
        if args.content and record["status"] == "ok" and record.get("sha256"):
            if not base:
                record["content_status"] = "first-seen"
            elif record.get("truncated"):
                # Comparing a prefix against a full capture would look like a change.
                record["content_status"] = "not-comparable"
            elif base.get("facts_sha256") and base["facts_sha256"] != record["facts_sha256"]:
                record["content_status"] = "facts-changed"
            elif base.get("sha256") and base["sha256"] != record["sha256"]:
                record["content_status"] = "cosmetic-changed"
            elif not base.get("facts_sha256"):
                record["content_status"] = "no-baseline-facts"
            else:
                record["content_status"] = "unchanged"
        elif p:
            if p["facts_changed"]:
                record["content_status"] = "facts-changed"
            elif p["raw_changed"]:
                record["content_status"] = "cosmetic-changed"
            elif p["provenance_error"]:
                record["content_status"] = "provenance-error"
            else:
                record["content_status"] = "unchanged"
        record["affected_rows"] = len(doc_refs.get(url, []))

    # Row marking: every row whose source page shows a changed published fact.
    marked, marked_ids = [], set()
    for url, record in checked.items():
        if record["content_status"] != "facts-changed":
            continue
        for ref in doc_refs.get(url, []):
            key = (ref["kind"], ref["id"])
            if key in marked_ids:
                continue
            marked_ids.add(key)
            base = (baseline.get("sources") or {}).get(url) or {}
            when = record.get("provenance_checked_at") or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            marked.append({
                "id": ref["id"], "kind": ref["kind"], "name": ref.get("label"),
                "date": ref.get("date"),
                "reason": "official source page printed different values on its last re-check",
                "source_url": url,
                "source_changed_at": when,
                "diff": {"official source verified against": [
                    base.get("checked_at_utc") or "no baseline recorded",
                    "%s (%s)" % (when, url)]},
            })

    # Row-value diffing against the last verified snapshot.
    snapshot = load("row_snapshot.json") or {"rows": {}}
    changes = {"added": [], "removed": [], "changed": []}
    current = {r["id"]: fingerprint(r) for r in rows}
    old = snapshot.get("rows", {})
    for rid, fp in current.items():
        if rid not in old:
            changes["added"].append({"id": rid, "name": fp["name"], "date": fp["date"],
                                     "kind": "tournament", "reason": "row not present in the last verified snapshot"})
        elif old[rid] != fp:
            diff = {k: [old[rid].get(k), fp.get(k)] for k in fp if old[rid].get(k) != fp.get(k)}
            changes["changed"].append({"id": rid, "name": fp["name"], "date": fp["date"],
                                        "kind": "tournament",
                                        "reason": "dataset value differs from the last verified snapshot",
                                        "diff": diff})
    for rid, fp in old.items():
        if rid not in current:
            changes["removed"].append({"id": rid, "name": fp.get("name"), "date": fp.get("date"),
                                       "kind": "tournament", "reason": "row no longer published by the dataset"})
    changes["changed"].extend(marked)

    checked_at = time.strftime("%Y-%m-%d", time.gmtime())
    # Only operator domains count as "official sources": the OpenStreetMap geocoder
    # and foot-router cited by the walking records are a routing service, not the
    # publisher of a price or an entry rule, so they are counted separately.
    official = {u: v for u, v in checked.items() if is_official(u)}
    routing = {u: v for u, v in checked.items() if not is_official(u)}
    raw_changed = sum(1 for v in official.values()
                      if v.get("content_status") in ("cosmetic-changed", "facts-changed"))
    facts_changed = sum(1 for v in official.values() if v.get("content_status") == "facts-changed")
    # Reachability KPI: report the newest real fetch, whatever machine produced it.
    unreachable = no_evidence = 0
    if any(v["status"] != "unreachable" for v in official.values()):
        ok = sum(1 for v in official.values() if v["status"] == "ok")
        bad = sum(1 for v in official.values() if v["status"] == "http-error")
        unreachable = sum(1 for v in official.values() if v["status"] == "unreachable")
        no_evidence = sum(1 for u in official if u not in prov)
        kpi_basis = "HTTP check run by this script on %s" % checked_at
    elif any(u in prov for u in official):
        ok = sum(1 for u in official if (prov.get(u) or {}).get("provenance_http_status") == 200)
        bad = sum(1 for u in official if (prov.get(u) or {}).get("provenance_error"))
        no_evidence = len(official) - ok - bad
        kpi_basis = ("this host has no route to the operator domains (its own HTTP check returned "
                     "unreachable for all %d URLs), so the counts below are the last real fetch, made by "
                     "scripts/check_source_facts.py on %s" % (len(official), prov_at or "an earlier run"))
    else:
        ok = bad = 0
        no_evidence = len(official)
        kpi_basis = "no fetch evidence available for the official sources"
    # A check that reaches nothing at all is a statement about the machine that ran it, not about the
    # official pages. Mark it so the site never presents a network blackout as "every source is down".
    blackout = bool(official) and all(
        v["status"] == "unreachable" and (v.get("error") or "").startswith("<urlopen error")
        for v in official.values())

    result = {
        "checked_at": checked_at,
        "checked_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "sources_total": len(official),
        "sources_ok": ok,
        "sources_unreachable": unreachable,
        "sources_http_error": bad,
        "sources_no_evidence": no_evidence,
        "routing_total": len(routing),
        "routing_ok": sum(1 for v in routing.values() if v["status"] == "ok"),
        "kpi_basis": kpi_basis,
        "content_mode": "fetched and hashed here" if args.content and http_reachable else (
            "last provenance fetch (data/change_log.json)" if prov else "not checked"),
        "sources_raw_changed": raw_changed,
        "sources_facts_changed": facts_changed,
        "rows_source_changed": len(marked),
        "rows_total": len(current),
        "rows_changed": len(changes["changed"]),
        "rows_added": len(changes["added"]),
        "rows_removed": len(changes["removed"]),
        "http_check": {
            "attempted": len(urls),
            "reachable": http_reachable,
            "ran_on": "GitHub Actions run %s" % os.environ["GITHUB_RUN_ID"] if os.environ.get("GITHUB_RUN_ID") else "local sandbox",
            "mode": "content" if args.content else "status-only",
        },
        "sources": checked,
        "network_unavailable": blackout,
        "note": "sources lists every official URL the dataset cites. 'status' is the HTTP result of "
                "this host; 'provenance_*' and 'content_status' come from the most recent real fetch. "
                "'facts-changed' means a money amount, date, time or entry-rule word printed on that "
                "page differs from the last verified capture, and every row citing it is listed in "
                "data/changes.json. A page that merely re-renders (cosmetic-changed) is recorded but "
                "marks no row. 'unreachable' means the host did not answer from the machine that ran the "
                "check; it does not by itself mean the page changed."
                + ("" if not blackout else
                   " This run reached none of the official hosts at all (every attempt failed at the TLS"
                   " or DNS layer), so it is a statement about the network of the machine that ran the"
                   " check and not about the sources. The scheduled GitHub Actions job reaches the"
                   " operator domains; its provenance result is in data/change_log.json."),
    }
    # Only `--write-report` publishes. `pages.yml` runs `--print` on every pull request, and a
    # validation run must not rewrite the reports - otherwise a host with no route to the operators
    # would overwrite the scheduled run's real numbers (and leave a dirty tree behind it).
    if args.write_report:
        with open(os.path.join(DATA, "monitoring.json"), "w", encoding="utf-8") as f:
            json.dump(result, f, indent=1)
            f.write("\n")
        with open(os.path.join(DATA, "changes.json"), "w", encoding="utf-8") as f:
            json.dump({"checked_at": checked_at, "sources_facts_changed": facts_changed,
                       "sources_raw_changed": raw_changed, **changes}, f, indent=1)
            f.write("\n")

    else:
        print("monitor: reports not written (run with --write-report to publish)")

    if args.accept_baseline:
        new_base = {"generated_at_utc": result["checked_at_utc"],
                    "note": "Content of every official URL as last verified. Written by "
                            "`python3 scripts/monitor_sources.py --content --accept-baseline`. "
                            "A row whose source hash differs here is marked in data/changes.json.",
                    "sources": {}}
        for url, record in checked.items():
            if record.get("sha256"):
                new_base["sources"][url] = {"sha256": record["sha256"],
                                           "facts_sha256": record["facts_sha256"],
                                           "facts_count": record["facts_count"],
                                           "checked_at_utc": result["checked_at_utc"]}
            elif (baseline.get("sources") or {}).get(url):
                new_base["sources"][url] = baseline["sources"][url]
        with open(BASELINE, "w", encoding="utf-8") as f:
            json.dump(new_base, f, indent=1)
            f.write("\n")
        print("monitor: baseline accepted with %d source hashes" % len(new_base["sources"]))

    print("monitor: official sources %d/%d reachable (basis: %s)" % (ok, len(official), kpi_basis))
    print("monitor: %d official page(s) re-rendered without a value change, %d with a changed published value, "
          "%d row(s) marked for re-reading" % (raw_changed - facts_changed, facts_changed, len(marked)))
    print("monitor: dataset rows - %d changed, %d added, %d removed against the last verified snapshot"
          % (len(changes["changed"]) - len(marked), len(changes["added"]), len(changes["removed"])))
    print("monitor: routing sources %d/%d reachable" % (
        sum(1 for v in routing.values() if v["status"] == "ok"), len(routing)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
