#!/usr/bin/env python3
"""Scrape the official daily Strip poker-room schedules into data/daily_feed.json.

Every row names the official document it was read from and the moment it was
retrieved. Fields that the document does not state are left null and flagged:
nothing is inferred here either.

This runs in two places:
  * locally, with network access, to refresh the feed;
  * on a schedule in CI, which publishes the refreshed feed to the `live`
    branch so the site can pick up the newest copy without touching `main`.

Run:  python3 scripts/scrape_daily.py [--out data/daily_feed.json]
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
VERIFIED_ON = "2026-11-16"
USER_AGENT = "Poker1DailyFeed/1.0 (+https://github.com/karagemop466-tech/Poker1)"

SOURCES = [
    {"key": "wynn_daily_poster", "kind": "pdf", "venue": "wynn",
     "venue_name": "Wynn Las Vegas / Encore Poker Room",
     "name": "Wynn daily tournament poster",
     "url": "https://cdn.wynnresorts.com/image/upload/v1752011166/visitwynn_pdfs_files/Poker/Daily%20Tournaments/poker-daily-tournament-poster.pdf"},
    {"key": "wynn_daily_struct", "kind": "pdf", "venue": "wynn",
     "venue_name": "Wynn Las Vegas / Encore Poker Room",
     "name": "Wynn daily tournament structures",
     "url": "https://cdn.wynnresorts.com/image/upload/v1752011191/visitwynn_pdfs_files/Poker/Daily%20Tournaments/Poker-All_Daily_Structures.pdf"},
    {"key": "wynn_poker", "kind": "html", "venue": "wynn",
     "venue_name": "Wynn Las Vegas / Encore Poker Room",
     "name": "Wynn poker room",
     "url": "https://www.wynnlasvegas.com/casino/poker"},
    {"key": "bellagio_poker", "kind": "html", "venue": "bellagio",
     "venue_name": "Bellagio Poker Room",
     "name": "Bellagio poker room",
     "url": "https://bellagio.mgmresorts.com/en/casino/poker.html"},
    {"key": "bellagio_fri", "kind": "pdf", "venue": "bellagio",
     "venue_name": "Bellagio Poker Room",
     "name": "Bellagio Friday $600 No Limit Hold'em",
     "url": "https://assets.contentstack.io/v3/assets/bltc6ce635bc4868eb2/blt9cf95b0e60ec253e/6af491a3a9851d75c40be840/mgm-bellagio-poker-fridays-$600-nlh.pdf"},
    {"key": "bellagio_sat", "kind": "pdf", "venue": "bellagio",
     "venue_name": "Bellagio Poker Room",
     "name": "Bellagio Saturday No Limit Hold'em",
     "url": "https://assets.contentstack.io/v3/assets/bltc6ce635bc4868eb2/blt6d47974bf5a7d9b6/6af491a391a6e8e4230c9e07/mgm-bellagio-poker-saturdays-$1000-nlh.pdf"},
    {"key": "bellagio_sun", "kind": "pdf", "venue": "bellagio",
     "venue_name": "Bellagio Poker Room",
     "name": "Bellagio Sunday $400 H.O.R.S.E.",
     "url": "https://assets.contentstack.io/v3/assets/bltc6ce635bc4868eb2/blt07fcf1244a6da661/6af491a339e2b4f6b76a86ad/mgm-bellagio-poker-sundays-$400-horse.pdf"},
    {"key": "aria_poker", "kind": "html", "venue": "aria",
     "venue_name": "ARIA Poker Room",
     "name": "ARIA poker room",
     "url": "https://aria.mgmresorts.com/en/casino/poker.html"},
    {"key": "venetian_poker", "kind": "html", "venue": "venetian",
     "venue_name": "The Venetian Resort Las Vegas (DeepStack Poker Room)",
     "name": "Venetian poker room",
     "url": "https://www.venetianlasvegas.com/resort/casino/poker.html"},
]

# Lines that look like a scheduled tournament in the source text.
ROW_RE = re.compile(
    r"(?P<when>Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|Weekdays?|Weekends?|Nightly|Every\s+\w+)"
    r"[^\n]{0,80}?\$"
    r"(?P<buy>\d[\d,]*)"
    r"[^\n]{0,90}",
    re.IGNORECASE)

MONEY_RE = re.compile(r"\$\s?(\d[\d,]*)")
GTD_RE = re.compile(r"\$([\d,]+)\s*(?:k\b|GTD|guarantee)", re.IGNORECASE)
STACK_RE = re.compile(r"start(?:ing)? with\s+([\d,]+)\s+(?:in\s+)?tournament chips", re.IGNORECASE)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.status, r.read(), r.headers.get("Last-Modified", "")


def html_to_text(body):
    text = body.decode("utf-8", "replace")
    text = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", text)
    links = re.findall(r'(?is)<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', text)
    keep = []
    for href, label in links:
        label = re.sub(r"(?s)<[^>]+>", " ", label)
        label = re.sub(r"\s+", " ", label).strip()
        if label and ("$" in label or re.search(r"(?i)nlh|horse|plo|turbo|bounty|poker|tournament", label)):
            keep.append(label)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"\s+", " ", text)
    return text, keep


def pdf_to_text(body):
    """Best-effort PDF text extraction. Returns (text, available)."""
    tmp = os.path.join(DATA, ".scrape_tmp.pdf")
    try:
        os.makedirs(DATA, exist_ok=True)
        with open(tmp, "wb") as f:
            f.write(body)
        try:
            out = subprocess.run(["pdftotext", "-layout", tmp, "-"],
                                 capture_output=True, timeout=60)
            if out.returncode == 0 and out.stdout.strip():
                return out.stdout.decode("utf-8", "replace"), True
        except (OSError, subprocess.SubprocessError):
            pass
        for mod in ("pypdf", "PyPDF2"):
            try:
                m = __import__(mod)
                reader = m.PdfReader(tmp)
                text = "\n".join((p.extract_text() or "") for p in reader.pages)
                if text.strip():
                    return text, True
            except Exception:  # noqa: BLE001 - optional dependency
                continue
        return "", False
    finally:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except OSError:
                pass


def parse_buy_in(text):
    m = MONEY_RE.search(text)
    if not m:
        return None
    return int(m.group(1).replace(",", ""))


def parse_gtd(text):
    m = GTD_RE.search(text)
    if not m:
        return None
    v = m.group(1).replace(",", "")
    if m.group(0).lower().strip().endswith("k") or re.search(r"\$" + re.escape(m.group(1)) + r"\s*k\b", text, re.I):
        try:
            return int(float(v) * 1000)
        except ValueError:
            return None
    try:
        return int(v)
    except ValueError:
        return None


def parse_entry_rule(text):
    low = text.lower()
    if "re-entry" in low or "re-entry" in low or "rebuy" in low or "rebuy" in low:
        return "Re-entry or rebuy language present in the source text; see the source document for the exact rule."
    if "add-on" in low or "add on" in low:
        return "Add-on language present in the source text."
    return None


def rows_from_text(text, source):
    rows = []
    seen = set()
    for line in text.split("\n"):
        line = line.strip()
        if not line or len(line) > 220:
            continue
        if not re.search(r"(?i)\$\s?\d", line):
            continue
        if not re.search(r"(?i)nlh|no limit|hold'em|hold’em|horse|pl[oa]o|pot limit|triple draw|big o|turbo|bounty|satellite|ante up|mspt", line):
            continue
        when = None
        m = re.search(r"(?i)\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday|weekdays?|weekends?|nightly)\b", line)
        if m:
            when = m.group(1).title()
        buy = parse_buy_in(line)
        gtd = parse_gtd(line)
        key = (when, line[:90])
        if key in seen:
            continue
        seen.add(key)
        rows.append({
            "venue": source["venue"],
            "venue_name": source["venue_name"],
            "when": when,
            "name": line[:180],
            "format": source["name"],
            "buy_in_usd": buy,
            "guarantee_usd": gtd,
            "stack_chips": None,
            "entry_rule": parse_entry_rule(line),
            "source": source["url"],
            "source_label": source["name"],
            "retrieved_at": source["_now"],
            "notes": ("Extracted verbatim from the official document by the daily scraper. Fields the document "
                      "does not state on this line are left blank rather than filled in."),
        })
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(DATA, "daily_feed.json"))
    args = ap.parse_args()

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    rows = []
    docs = []
    errors = []

    # Rows that were read directly from an official document are preserved.
    # The automated extraction is a supplement, not a replacement.
    seed_path = os.path.join(DATA, "daily_feed.json")
    seed_rows = []
    if os.path.isfile(seed_path):
        try:
            with open(seed_path, encoding="utf-8") as f:
                seed_rows = json.load(f).get("rows", [])
        except (ValueError, OSError):
            seed_rows = []
    kept = [r for r in seed_rows if r.get("origin") == "read from the official document"]

    for src in SOURCES:
        src = dict(src)
        src["_now"] = now
        rec = {"key": src["key"], "name": src["name"], "url": src["url"],
               "venue": src["venue"], "venue_name": src["venue_name"]}
        try:
            status, body, last_mod = fetch(src["url"])
            rec["http_status"] = status
            rec["bytes"] = len(body)
            rec["sha256"] = hashlib.sha256(body).hexdigest()
            rec["last_modified"] = last_mod
            rec["retrieved_at"] = now
            rec["status"] = "fetched"
            if src["kind"] == "html":
                text, anchors = html_to_text(body)
                rec["extraction"] = "html"
                got = rows_from_text(text, src)
                for a in anchors:
                    if "$" in a and len(a) < 120:
                        key = (None, a[:90])
                        if any(r["name"] == a for r in got):
                            continue
                        got.append({
                            "venue": src["venue"], "venue_name": src["venue_name"],
                            "when": None, "name": a, "format": src["name"],
                            "buy_in_usd": parse_buy_in(a), "guarantee_usd": parse_gtd(a),
                            "stack_chips": None, "entry_rule": parse_entry_rule(a),
                            "source": src["url"], "source_label": src["name"],
                            "retrieved_at": now,
                            "notes": "Link text taken from the official page.",
                        })
            else:
                text, ok = pdf_to_text(body)
                rec["extraction"] = "pdf-text" if ok else "pdf-unreadable"
                got = rows_from_text(text, src) if ok else []
                if not ok:
                    rec["status"] = "fetched"
                    rec["note"] = ("The document was fetched successfully but its text could not be extracted in "
                                   "this environment, so no rows were parsed from it. The document link is "
                                   "included so the schedule can be read directly.")
                m = STACK_RE.search(text)
                if m:
                    rec["stack_chips_mentioned"] = int(m.group(1).replace(",", ""))
            rows.extend(got)
            rec["row_count"] = len(got)
            rec["seed_rows_kept"] = sum(1 for r in kept if r.get("source") == src["url"])
            rows_found = len(got)
        except (urllib.error.URLError, urllib.error.HTTPError, OSError, ValueError) as e:
            rec["status"] = "error"
            rec["error"] = "%s: %s" % (type(e).__name__, e)
            errors.append("%s - %s" % (src["name"], e))
            rows_found = 0
        docs.append(rec)
        print("%-22s %-10s rows=%d" % (src["key"], rec["status"], rows_found))

    for r in kept:
        if not any(x.get("name") == r.get("name") and x.get("source") == r.get("source") for x in rows):
            rows.append(r)

    feed = {
        "generated_at": now,
        "verified_on": VERIFIED_ON,
        "note": ("Live feed of the official daily Strip poker-room schedules. Each row names the official "
                 "document it was read from and the moment it was retrieved. Rows that were read directly "
                 "from an official document are kept even when the automated extraction cannot parse the "
                 "same document, so a failed parse never drops a verified row. Fields the documents do not "
                 "state are left blank."),
        "sources": [{"label": d["name"], "url": d["url"], "status": d["status"],
                     "sha256": d.get("sha256"), "retrieved_at": d.get("retrieved_at")} for d in docs],
        "documents": docs,
        "errors": errors,
        "rows": rows,
    }
    out = args.out if os.path.isabs(args.out) else os.path.join(ROOT, args.out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(feed, f, indent=1)
    print("wrote %s (%d rows, %d errors)" % (out, len(rows), len(errors)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
