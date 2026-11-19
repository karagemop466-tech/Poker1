#!/usr/bin/env python3
"""Fetch every official source URL in data/sources.json, snapshot it, and record changes.

This is the provenance archive and cross-check for the row-level monitor in
``scripts/monitor_sources.py``: it keeps the line-rendered text of every official
document under ``data/snapshots/`` and a separate position-aware ``.layout.txt``
render for PDFs, plus the hashes and last-checked time in ``data/change_log.json``.
It decides whether a re-check found a *meaningful* change by comparing complete
line renders with prior line renders and complete layout renders with prior layout
renders, while retaining their de-duplicated union for coverage. This avoids
mistaking an extractor migration for an official-source change; operator pages
also rotate promos and cookie text on almost every fetch.

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

Nothing is inferred: the script only records what the server returned. Layout output is
comparison evidence only; it does not establish merged-cell ownership or populate a
published tournament value.

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

# The taxing authority. Clark County levies the transient lodging (room) tax that
# the hotel rows publish; it is kept apart from the operator domains so a county
# record is never reported as a casino's own page.
GOVERNMENT_HOSTS = (
    "clarkcountynv.gov",
    "www.clarkcountynv.gov",
)

# Only these hosts are treated as official operators of the data.  Any URL in the
# manifest must be on this list or on GOVERNMENT_HOSTS, otherwise this script
# refuses to run.
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
        if host not in OFFICIAL_HOSTS and host not in GOVERNMENT_HOSTS:
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


def pdf_text_variants(data):
    """Extract both linear and position-aware text from a PDF.

    The plain render remains the quote-check snapshot because existing evidence
    cites its line numbers.  pypdf's ``layout`` mode is archived separately and
    contributes a second fact signature: it preserves table-column positions
    which ordinary ``extract_text`` can flatten or omit around merged cells.
    It does not identify merged-cell ownership, so the layout text is never used
    to populate a tournament row by itself.
    """
    try:
        from pypdf import PdfReader
    except Exception:
        try:
            from PyPDF2 import PdfReader
        except Exception:
            missing = "pypdf/PyPDF2 is not installed"
            return {"plain": "", "layout": "", "plain_error": missing, "layout_error": missing}
    try:
        reader = PdfReader(io.BytesIO(data))
    except Exception as e:
        error = "%s: %s" % (type(e).__name__, e)
        return {"plain": "", "layout": "", "plain_error": error, "layout_error": error}

    plain, layout, plain_errors, layout_errors = [], [], [], []
    for page_number, page in enumerate(reader.pages, 1):
        try:
            plain.append(page.extract_text() or "")
        except Exception as e:
            plain.append("")
            plain_errors.append("page %d: %s: %s" % (page_number, type(e).__name__, e))
        try:
            layout.append(page.extract_text(extraction_mode="layout") or "")
        except Exception as e:
            layout.append("")
            layout_errors.append("page %d: %s: %s" % (page_number, type(e).__name__, e))
    plain_text, layout_text = "\n".join(plain), "\n".join(layout)
    if not plain_text.strip() and not plain_errors:
        plain_errors.append("no extractable plain text")
    if not layout_text.strip() and not layout_errors:
        layout_errors.append("no extractable layout text")
    return {"plain": plain_text, "layout": layout_text,
            "plain_error": "; ".join(plain_errors) if plain_errors else None,
            "layout_error": "; ".join(layout_errors) if layout_errors else None}


def pdf_to_text(data):
    """Compatibility wrapper: return the original, quote-checkable PDF render."""
    return pdf_text_variants(data)["plain"]


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


def is_pdf(url, data):
    return url.lower().split("?")[0].endswith(".pdf") or data[:5] == b"%PDF-"


def to_text_variants(url, data):
    """Return archived text renders without changing the legacy plain snapshot."""
    if is_pdf(url, data):
        variants = pdf_text_variants(data)
        return {"plain": variants["plain"], "layout": variants["layout"],
                "is_pdf": True, "plain_error": variants.get("plain_error"),
                "layout_error": variants.get("layout_error")}
    return {"plain": html_to_text(data), "layout": "", "is_pdf": False,
            "plain_error": None, "layout_error": None}


def to_text(url, data):
    """Return the original plain render used by row-quote evidence and older callers."""
    return to_text_variants(url, data)["plain"]


def union_facts_signature(plain_text, layout_text=""):
    """Stable, de-duplicated union of published facts in both PDF renders."""
    by_key = {}
    for text in (plain_text or "", layout_text or ""):
        for line in facts_signature(text):
            key = re.sub(r"\s+", " ", line).strip().casefold()
            by_key.setdefault(key, line)
    return [by_key[key] for key in sorted(by_key)]


def previous_signature_available(previous, render):
    """Whether a previous render is complete enough to compare without a false change."""
    previous = previous or {}
    field = "facts_signature_%s_available" % render
    if field in previous:
        return bool(previous[field])
    signature = "facts_signature_%s" % render
    if signature in previous:
        return previous[signature] is not None
    # Before the dual-render migration, facts_signature is the line/plain render.
    return render == "plain" and "facts_signature" in previous and previous.get("facts_signature") is not None


def compare_fact_signatures(previous, plain_facts, layout_facts, layout_available, plain_available=True):
    """Compare complete like renders, keeping migration and extraction failures distinct.

    Old ``change_log.json`` entries only have ``facts_signature`` (the plain
    renderer). Compare that history to the new plain signature and report the
    new layout render as baseline-pending, rather than falsely claiming the
    newly visible layout text is a source change. An incomplete current or prior
    render is not compared; the next complete capture becomes its baseline.
    """
    previous = previous or {}
    old_plain = previous.get("facts_signature_plain")
    if old_plain is None:
        old_plain = previous.get("facts_signature") or []
    differences = []

    def add_diff(old_values, new_values, label):
        old_set, new_set = set(old_values or []), set(new_values or [])
        added = sorted(new_set - old_set)
        removed = sorted(old_set - new_set)
        differences.extend(["%s+ %s" % (label, x) for x in added])
        differences.extend(["%s- %s" % (label, x) for x in removed])

    if plain_available and previous_signature_available(previous, "plain"):
        add_diff(old_plain, plain_facts, "plain ")
    old_layout = previous.get("facts_signature_layout")
    old_layout_available = previous_signature_available(previous, "layout")
    layout_pending = bool(layout_available and not old_layout_available)
    if layout_available and old_layout_available:
        add_diff(old_layout, layout_facts, "layout ")
    return bool(differences), differences[:10], layout_pending


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
                   "facts_signature_plain": prev.get("facts_signature_plain"),
                   "facts_signature_layout": prev.get("facts_signature_layout"),
                   "facts_signature_plain_available": previous_signature_available(prev, "plain"),
                   "facts_signature_layout_available": previous_signature_available(prev, "layout"),
                   "facts_signature_mode": prev.get("facts_signature_mode"),
                   "layout_snapshot": prev.get("layout_snapshot"),
                   "layout_extracted_chars": prev.get("layout_extracted_chars"),
                   "layout_status": prev.get("layout_status", "not-checked"),
                   "plain_error": prev.get("plain_error"),
                   "layout_error": prev.get("layout_error"),
                   "layout_baseline_pending": prev.get("layout_baseline_pending", False),
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
            "facts_signature": [],
            "facts_signature_plain": [],
            "facts_signature_layout": [],
            "facts_signature_plain_available": False,
            "facts_signature_layout_available": False,
            "plain_baseline_pending": False,
            "facts_signature_mode": None,
            "layout_snapshot": None,
            "layout_extracted_chars": None,
            "layout_status": "not-applicable",
            "plain_error": None,
            "layout_baseline_pending": False,
            "layout_error": None,
            "error": None,
            "snapshot": "data/snapshots/%s.txt" % sid,
        }
        if args.offline:
            path = os.path.join(SNAP, sid + ".txt")
            layout_path = os.path.join(SNAP, sid + ".layout.txt")
            if os.path.exists(path):
                with open(path, encoding="utf-8") as f:
                    plain_text = f.read()
                layout_text = ""
                if os.path.exists(layout_path):
                    with open(layout_path, encoding="utf-8") as f:
                        layout_text = f.read()
                rec["extracted_chars"] = len(plain_text)
                rec["layout_extracted_chars"] = len(layout_text) if layout_text else None
                rec["layout_snapshot"] = "data/snapshots/%s.layout.txt" % sid if layout_text else None
                rec["sha256"] = hashlib.sha256(plain_text.encode("utf-8")).hexdigest()
                if rec["sha256"] != prev.get("sha256"):
                    rec["last_changed_utc"] = rec["last_checked_utc"]
                    rec["changed"] = True
                rec["facts_signature_plain"] = facts_signature(plain_text)
                rec["facts_signature_layout"] = facts_signature(layout_text) if layout_text else []
                rec["facts_signature"] = union_facts_signature(plain_text, layout_text)
                rec["plain_error"] = prev.get("plain_error") or ("offline: no plain snapshot text" if not plain_text.strip() else None)
                rec["layout_error"] = prev.get("layout_error") or None
                pdf_source = is_pdf(s["url"], b"")
                rec["facts_signature_plain_available"] = bool(plain_text.strip() and not rec["plain_error"])
                rec["facts_signature_layout_available"] = bool(layout_text.strip() and not rec["layout_error"])
                rec["plain_baseline_pending"] = bool(rec["facts_signature_plain_available"] and
                                                       not previous_signature_available(prev, "plain"))
                rec["facts_signature_mode"] = ("plain+layout-v1" if rec["facts_signature_plain_available"] and
                                               rec["facts_signature_layout_available"] else
                                               "layout-v1" if rec["facts_signature_layout_available"] else
                                               "plain-v1" if rec["facts_signature_plain_available"] else None)
                rec["facts_checked"] = len(rec["facts_signature"])
                if pdf_source:
                    rec["layout_status"] = ("partial" if rec["plain_error"] or rec["layout_error"] else
                                             "baseline-pending" if rec["facts_signature_layout_available"] and
                                             not previous_signature_available(prev, "layout") else
                                             "comparable" if rec["facts_signature_layout_available"] else
                                             "unavailable")
                    rec["layout_baseline_pending"] = bool(rec["facts_signature_layout_available"] and
                                                           not previous_signature_available(prev, "layout"))
                    if not rec["facts_signature_layout_available"] and not rec["layout_error"]:
                        rec["layout_error"] = "offline: no position-aware snapshot text on file"
                else:
                    rec["layout_status"] = "not-applicable"
            out.append(rec)
            continue

        try:
            status, data = fetch(s["url"], args.timeout)
            rec["http_status"] = status
            rec["bytes"] = len(data)
            variants = to_text_variants(s["url"], data)
            plain_text, layout_text = variants["plain"], variants["layout"]
            rec["extracted_chars"] = len(plain_text)
            rec["facts_signature_plain"] = facts_signature(plain_text)
            rec["facts_signature_layout"] = facts_signature(layout_text) if layout_text else []
            rec["facts_signature"] = union_facts_signature(plain_text, layout_text)
            rec["layout_extracted_chars"] = len(layout_text) if layout_text else None
            rec["layout_snapshot"] = "data/snapshots/%s.layout.txt" % sid if layout_text else None
            rec["plain_error"] = variants.get("plain_error")
            rec["layout_error"] = variants.get("layout_error")
            rec["facts_signature_plain_available"] = bool(plain_text.strip() and not rec["plain_error"])
            rec["facts_signature_layout_available"] = bool(layout_text.strip() and not rec["layout_error"])
            rec["plain_baseline_pending"] = bool(rec["facts_signature_plain_available"] and
                                                   not previous_signature_available(prev, "plain"))
            rec["facts_signature_mode"] = ("plain+layout-v1" if rec["facts_signature_plain_available"] and
                                           rec["facts_signature_layout_available"] else
                                           "layout-v1" if rec["facts_signature_layout_available"] else
                                           "plain-v1" if rec["facts_signature_plain_available"] else None)
            rec["facts_checked"] = len(rec["facts_signature"])
            previous_layout_available = previous_signature_available(prev, "layout")
            if variants["is_pdf"]:
                rec["layout_status"] = ("partial" if rec["plain_error"] or rec["layout_error"] else
                                         "baseline-pending" if rec["facts_signature_layout_available"] and
                                         not previous_layout_available else
                                         "comparable" if rec["facts_signature_layout_available"] else
                                         "unavailable")
                rec["layout_baseline_pending"] = bool(rec["facts_signature_layout_available"] and
                                                       not previous_layout_available)
            else:
                rec["layout_status"] = "not-applicable"
                rec["layout_baseline_pending"] = False
            write_snapshot(sid, plain_text)
            if layout_text:
                write_snapshot(sid + ".layout", layout_text)
            else:
                stale_layout_path = os.path.join(SNAP, sid + ".layout.txt")
                if os.path.exists(stale_layout_path):
                    os.remove(stale_layout_path)
            # Hash the bytes actually served, so a changed file is detected even
            # when the extracted text happens to be identical.
            rec["sha256"] = hashlib.sha256(data).hexdigest()
            rec["error"] = None if (status == 200 and (plain_text.strip() or layout_text.strip())) else (
                "no extractable text" if status == 200 else "http %s" % status)
            if variants["is_pdf"] and not layout_text and not rec["layout_error"]:
                rec["layout_error"] = "position-aware PDF extraction returned no text"
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

        # Compare like render with like render. During the migration, the old
        # facts_signature is the plain renderer; newly visible layout lines are
        # reported as baseline-pending, never as a fabricated source change.
        if rec["http_status"] == 200 and rec.get("error") is None:
            rec["facts_changed"], rec["facts_diff"], rec["layout_baseline_pending"] = compare_fact_signatures(
                prev,
                rec["facts_signature_plain"],
                rec["facts_signature_layout"],
                rec.get("facts_signature_layout_available", False),
                rec.get("facts_signature_plain_available", False),
            )
        out.append(rec)

    log = {
        "generated_utc": now_utc(),
        "mode": "offline" if args.offline else "fetch",
        "source_count": len(out),
        "changed_ids": changed,
        "facts_changed_ids": [r["id"] for r in out if r.get("facts_changed")],
        "layout_baseline_pending_ids": [r["id"] for r in out if r.get("layout_baseline_pending")],
        "layout_unavailable_ids": [r["id"] for r in out if r.get("layout_status") in ("unavailable", "partial")],
        "error_count": len(errors),
        "note": ("Snapshot hashes let the site flag any row whose official source has changed "
                 "since the row's values were captured. PDF line and position-aware layout facts "
                 "are compared separately; first-time layout captures are marked baseline-pending, "
                 "not as source changes. Blank/absent snapshots are never guessed."),
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
    pending_layout = [r["id"] for r in out if r.get("layout_baseline_pending")]
    unavailable_layout = [r["id"] for r in out if r.get("layout_status") in ("unavailable", "partial")]
    if pending_layout:
        print("  PDF layout baseline pending for %d source(s): %s" %
              (len(pending_layout), ", ".join(pending_layout)))
    if unavailable_layout:
        print("  PDF layout extraction unavailable for %d source(s): %s" %
              (len(unavailable_layout), ", ".join(unavailable_layout)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
