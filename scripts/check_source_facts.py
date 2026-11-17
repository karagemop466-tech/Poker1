#!/usr/bin/env python3
"""Fetch every official source URL in data/sources.json, snapshot it, and record changes.

This is the provenance archive and cross-check for the row-level monitor in
``scripts/monitor_sources.py``: it keeps the raw text of every official document
under ``data/snapshots/``, plus the hash and last-checked time in
``data/change_log.json``, and it decides whether a re-check found a *meaningful*
change by comparing the money amounts, dates, times and entry-rule words printed
on each page rather than the raw bytes (operator pages rotate promos and cookie
text on almost every fetch).

It deliberately does not touch the files owned by the row-level monitor
(``data/monitoring.json``, ``data/changes.json``, ``data/row_snapshot.json``).

This is the "live feed" for the project. Every source listed in the manifest is
fetched, hashed, and (for PDF/HTML) converted to plain text under
``data/snapshots/``.  ``data/change_log.json`` records, per source:

    first_seen_utc, last_checked_utc, last_changed_utc, sha256, previous_sha256,
    http_status, bytes, extracted_chars, changed (bool), error (or null)

A row on the site is flagged "source changed" when the sha256 of one of its
sources differs from the hash recorded when that row's values were captured
(``data/baseline_hashes.json``).

Nothing is inferred: the script only records what the server returned.

Usage
-----
    python3 scripts/check_source_facts.py            # fetch everything, write snapshots + log
    python3 scripts/check_source_facts.py --offline  # rebuild the log from existing snapshots
    python3 scripts/check_source_facts.py --id ID    # fetch a single source id
"""
import argparse
import hashlib
import html
import io
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
SNAP = os.path.join(DATA, "snapshots")
MANIFEST = os.path.join(DATA, "sources.json")
CHANGE_LOG = os.path.join(DATA, "change_log.json")
BASELINE = os.path.join(DATA, "baseline_hashes.json")

USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

# Only these hosts are treated as official operators of the data.  Any URL in the
# manifest must be on this list, otherwise this script refuses to run.
OFFICIAL_HOSTS = (
    "venetianlasvegas.com",
    "www.venetianlasvegas.com",
    "wynnlasvegas.com",
    "www.wynnlasvegas.com",
    "cdn.wynnresorts.com",
    "bellagio.mgmresorts.com",
    "aria.mgmresorts.com",
    "www.caesars.com",
    "caesars.com",
    # MGM's own asset host; only used for the Bellagio structure PDFs that the official
    # Bellagio poker page links.
    "assets.contentstack.io",
    # Clark County Department of Business License: the taxing/licensing authority whose
    # table records each Strip resort's address and room-tax class. A government record,
    # not an operator page - the site labels it as such.
    "www.clarkcountynv.gov",
    # Session 0d069ce0: official property domains behind pages/other-rooms.html.
    "mgmgrand.mgmresorts.com",
    "mandalaybay.mgmresorts.com",
    "orleans.boydgaming.com",
    "southpointcasino.com",
    # Session df94b75e: official Resorts World Las Vegas domain behind
    # pages/strip-rooms.html (data id strip_rwlv_events). Its absence made this
    # script refuse to run on main (REQUEST 2, session 206debc0).
    "www.rwlasvegas.com",
    "rwlasvegas.com",
)


def now_utc():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_manifest():
    with open(MANIFEST) as f:
        return json.load(f)


def assert_official(sources):
    from urllib.parse import urlparse
    bad = []
    for s in sources:
        host = urlparse(s["url"]).netloc
        if host not in OFFICIAL_HOSTS:
            bad.append((s["id"], host))
    if bad:
        raise SystemExit("Refusing to run: non-official host(s) in manifest: %s" % bad)


def fetch(url, timeout=60):
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/pdf,application/xhtml+xml,*/*",
        "Accept-Language": "en-US,en;q=0.9",
    })
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, resp.read()


def pdf_to_text(data):
    try:
        from pypdf import PdfReader
    except Exception:
        try:
            from PyPDF2 import PdfReader
        except Exception:
            return ""
    try:
        reader = PdfReader(io.BytesIO(data))
    except Exception:
        return ""
    out = []
    for page in reader.pages:
        try:
            out.append(page.extract_text() or "")
        except Exception:
            out.append("")
    return "\n".join(out)


def html_to_text(data):
    try:
        txt = data.decode("utf-8", "replace")
    except Exception:
        return ""
    txt = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", txt)
    txt = re.sub(r"(?s)<[^>]+>", "\n", txt)
    txt = html.unescape(txt)
    txt = re.sub(r"[ \t\r\f\v]+", " ", txt)
    txt = re.sub(r"\n\s*\n+", "\n", txt)
    return txt.strip()


FACT_RE = re.compile(
    r"(?:\$[\d,]+(?:\.\d{2})?|\b\d{1,2}:\d{2}\s*(?:AM|PM)\b|\b\d{1,3}(?:\.\d{1,2})?\s?%\b"
    r"|\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s*\d{4}\)"
    r"|(?:no\s+)?re-?entry|re-?buy|add-?on|freeze[- ]?out|single\s+entry)",
    re.I)


def facts_signature(text):
    """The published numbers and rule words on a page, normalised.

    HTML pages carry rotating promos and cookie text that change on every fetch
    even when no tournament or hotel value has changed, so the raw hash alone
    produces false alarms.  This signature keeps only lines that state a money
    amount, a percentage, a date, a start time or an entry-rule word, and is
    compared against the previous check to decide whether a human should look.
    """
    if not text:
        return []
    seen, out = set(), []
    for line in text.split("\n"):
        line = re.sub(r"\s+", " ", line).strip()
        if not line or not FACT_RE.search(line):
            continue
        key = line.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(line)
    return sorted(out)


def to_text(url, data):
    if url.lower().split("?")[0].endswith(".pdf") or data[:5] == b"%PDF-":
        return pdf_to_text(data)
    return html_to_text(data)


def write_snapshot(sid, text):
    os.makedirs(SNAP, exist_ok=True)
    path = os.path.join(SNAP, sid + ".txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path) as f:
                return json.load(f)
        except Exception:
            return default
    return default


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true", help="rebuild the log from existing snapshots")
    ap.add_argument("--id", action="append", help="limit to this source id (repeatable)")
    ap.add_argument("--timeout", type=int, default=60)
    args = ap.parse_args()

    manifest = load_manifest()
    sources = manifest["sources"]
    assert_official(sources)

    prev_log = {s["id"]: s for s in load_json(CHANGE_LOG, {"sources": []}).get("sources", [])}
    # PR #66 (session 1ebc7e08): the file is {"note", "captured_utc", "hashes": {id: sha256}};
    # reading the wrapper made every lookup miss, so changed_vs_baseline was false for every
    # source forever (the "dead baseline lookup").
    baseline_doc = load_json(BASELINE, {})
    baseline = baseline_doc.get("hashes", baseline_doc) if isinstance(baseline_doc, dict) else {}
    baseline_captured = baseline_doc.get("captured_utc") if isinstance(baseline_doc, dict) else None
    ids = set(args.id) if args.id else None

    out = []
    changed = []
    errors = []
    for s in sources:
        sid = s["id"]
        if ids and sid not in ids:
            continue
        if s.get("active") is False and not ids:
            # Recorded for completeness (for example a URL that 404s) but not checked.
            prev = prev_log.get(sid, {})
            rec = {"id": sid, "label": s.get("label", sid), "kind": s.get("kind", "other"),
                   "venue": s.get("venue", ""), "url": s["url"],
                   "first_seen_utc": prev.get("first_seen_utc") or now_utc(),
                   "last_checked_utc": None, "last_changed_utc": prev.get("last_changed_utc"),
                   "sha256": prev.get("sha256"), "previous_sha256": prev.get("sha256"),
                   "http_status": prev.get("http_status"), "bytes": None, "extracted_chars": None,
                   "changed": False, "changed_vs_baseline": False, "facts_changed": False,
                   "facts_diff": [], "facts_checked": prev.get("facts_checked"),
                   "facts_signature": prev.get("facts_signature"),
                   "inactive": True, "note": s.get("note", ""),
                   "error": "not checked (source marked inactive)",
                   "snapshot": "data/snapshots/%s.txt" % sid}
            out.append(rec)
            continue
        prev = prev_log.get(sid, {})
        rec = {
            "id": sid,
            "label": s.get("label", sid),
            "kind": s.get("kind", "other"),
            "venue": s.get("venue", ""),
            "url": s["url"],
            "first_seen_utc": prev.get("first_seen_utc") or now_utc(),
            "last_checked_utc": now_utc(),
            "last_changed_utc": prev.get("last_changed_utc"),
            "sha256": prev.get("sha256"),
            "previous_sha256": prev.get("sha256"),
            "http_status": None,
            "bytes": None,
            "extracted_chars": None,
            "changed": False,
            "changed_vs_baseline": False,
            "facts_changed": False,
            "facts_diff": [],
            "facts_checked": None,
            "error": None,
            "snapshot": "data/snapshots/%s.txt" % sid,
        }
        if args.offline:
            path = os.path.join(SNAP, sid + ".txt")
            if os.path.exists(path):
                with open(path, encoding="utf-8") as f:
                    text = f.read()
                rec["extracted_chars"] = len(text)
                rec["sha256"] = hashlib.sha256(text.encode("utf-8")).hexdigest()
                if rec["sha256"] != prev.get("sha256"):
                    rec["last_changed_utc"] = rec["last_checked_utc"]
                    rec["changed"] = True
                rec["facts_checked"] = len(facts_signature(text))
                rec["facts_signature"] = facts_signature(text)
            out.append(rec)
            continue

        try:
            status, data = fetch(s["url"], args.timeout)
            rec["http_status"] = status
            rec["bytes"] = len(data)
            text = to_text(s["url"], data)
            rec["extracted_chars"] = len(text)
            write_snapshot(sid, text)
            # Hash the bytes actually served, so a changed file is detected even
            # when the extracted text happens to be identical.
            rec["sha256"] = hashlib.sha256(data).hexdigest()
            rec["error"] = None if (status == 200 and text.strip()) else (
                "no extractable text" if status == 200 else "http %s" % status)
        except urllib.error.HTTPError as e:
            rec["http_status"] = int(e.code)
            rec["error"] = "http %s" % e.code
            errors.append((sid, rec["error"]))
        except Exception as e:  # network/DNS/TLS
            rec["error"] = "%s: %s" % (type(e).__name__, e)
            errors.append((sid, rec["error"]))

        if rec["sha256"] and prev.get("sha256") and rec["sha256"] != prev["sha256"]:
            rec["changed"] = True
            rec["last_changed_utc"] = rec["last_checked_utc"]
            changed.append(sid)
        if rec["sha256"] and baseline.get(sid):
            rec["baseline_sha256"] = baseline[sid]
            rec["baseline_captured_utc"] = baseline_captured
            if rec["sha256"] != baseline[sid]:
                rec["changed_vs_baseline"] = True

        # Meaningful change: did any published number, date, time or rule word move?
        rec["facts_signature"] = facts_signature(text) if rec.get("extracted_chars") else []
        rec["facts_checked"] = len(rec["facts_signature"])
        if prev.get("facts_signature") is not None and rec["facts_signature"]:
            old_facts = set(prev["facts_signature"])
            new_facts = set(rec["facts_signature"])
            added = sorted(new_facts - old_facts)[:8]
            removed = sorted(old_facts - new_facts)[:8]
            if added or removed:
                rec["facts_changed"] = True
                rec["facts_diff"] = (["+ " + a for a in added] + ["- " + r for r in removed])[:10]
        out.append(rec)

    log = {
        "generated_utc": now_utc(),
        "mode": "offline" if args.offline else "fetch",
        "source_count": len(out),
        "changed_ids": changed,
        "facts_changed_ids": [r["id"] for r in out if r.get("facts_changed")],
        "error_count": len(errors),
        "note": ("Snapshot hashes let the site flag any row whose official source has changed "
                 "since the row's values were captured. Blank/absent snapshots are never guessed."),
        "sources": out,
    }
    os.makedirs(DATA, exist_ok=True)
    if args.offline:
        # Offline mode only reports on the snapshots already on disk; it must not
        # overwrite the log written by a real fetch.
        print("offline: change_log.json left unchanged")
        return 0
    with open(CHANGE_LOG, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=1)

    # First clean run: record the hashes the rows were captured from, so later checks
    # can flag a row whose official source has changed since then.
    if not args.offline and not os.path.exists(BASELINE):
        with open(BASELINE, "w", encoding="utf-8") as f:
            json.dump({"note": ("Baseline hashes: the SHA-256 of what each official server returned when the "
                                "values in data/*.json were captured. Rows are flagged 'source changed' when a "
                                "later check differs from this baseline."),
                       "captured_utc": now_utc(),
                       "hashes": {r["id"]: r["sha256"] for r in out if r.get("sha256")}}, f, indent=1)
        print("wrote", BASELINE)

    inactive = sum(1 for r in out if r.get("inactive"))
    ok = sum(1 for r in out if r["http_status"] == 200 and r["extracted_chars"])
    fact_changes = [r["id"] for r in out if r.get("facts_changed")]
    print("checked %d sources (%d inactive) | %d fetched with text | %d changed | %d published values changed | %d errors"
          % (len(out), inactive, ok, len(changed), len(fact_changes), len(errors)))
    for sid in fact_changes:
        print("  FACTS CHANGED %s" % sid)
        for line in next(r for r in out if r["id"] == sid)["facts_diff"]:
            print("    " + line[:160])
    for sid, err in errors:
        print("  ERROR %s: %s" % (sid, err))
    return 0


if __name__ == "__main__":
    sys.exit(main())
