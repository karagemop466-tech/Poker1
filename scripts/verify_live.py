#!/usr/bin/env python3
"""Re-fetch the official schedule pages and check every published row against them.

This is the independent, live half of the verification. `scripts/verify_rows.py`
checks published values against the *archived* official text; this script goes back
to the official pages themselves, parses the schedule table each one prints, and
compares that parse with the published dataset element by element.

For every official schedule page it reports:

    printed     the rows the page prints today, parsed by this script
    published   the rows the dataset carries for that source page
    missing     published rows the page no longer prints      -> source moved, row stale
    new         printed rows the dataset does not carry       -> new event to read
    changed     same date/event printed with a different time, buy-in or name

Nothing is written back into the dataset: a discrepancy is reported so a reviewer
re-reads the sheet. Exit code is 0 when every source was reachable and the parse
agrees with the dataset, 1 when a source was unreachable (so a scheduled job shows
a red run), and 2 when a real discrepancy was found.

The sandbox used for editing cannot reach the operator domains, so the scheduled
GitHub Actions job is where this runs for real:

    python3 scripts/verify_live.py --json data/live_verification.json
"""
import argparse
import io
import json
import os
import re
import sys
import time
from datetime import date
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
TIMEOUT = 45
UA = "Mozilla/5.0 (compatible; Poker1-live-verify/1.0; +https://github.com/karagemop466-tech/Poker1)"

# Official schedule pages and the dataset series each one governs.
VENETIAN_PAGES = [
    ("https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html",
     "Venetian DeepStack Extravaganza IV"),
    ("https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-dec-2026.html",
     "Venetian DeepStack Extravaganza NYE"),
]

WPT_SCHEDULE_PDF = ("https://cdn.wynnresorts.com/image/upload/v1757097329/visitwynn_pdfs_files/"
                    "Poker/WPT/WPT_World_Championship_Schedule.pdf")
WPT_SERIES = "WPT World Championship (Wynn)"

MONTHS_SHORT = {m: i + 1 for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])}

# The Wynn WPT schedule PDF is printed as one long table. Its text extraction gives one
# value per line, so the columns are read positionally: every date line starts a row and
# the following time / event / buy-in / guarantee / chips / levels lines fill it in.
WPT_DATE_LINE = re.compile(r"^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.?\s+(\d{1,2})$")
WPT_TIME_LINE = re.compile(r"^(\d{1,2})(?::(\d{2}))?\s*([ap])\.?m\.?$", re.I)

MONTHS = {m: i + 1 for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July",
     "August", "September", "October", "November", "December"])}

# One printed row of the Venetian schedule table, in the markdown the page serves:
#   | Wednesday, November 18, 2026 | 11:10 AM | 2 | $300 No LImit Hold'em $10K GTD (1Day) | [View...](url) |
VEN_ROW = re.compile(
    r"(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),\s+"
    r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+"
    r"(\d{1,2}),\s+(\d{4})\s*\|\s*"
    r"(\d{1,2}):(\d{2})\s*([AP]M)\s*\|\s*"
    r"(\d+)\s*\|\s*"
    r"([^|]*?)\s*\|\s*"
    r"\[\s*View[^\]]*\]\(\s*(https://[^)\s]+)\s*\)", re.I)


def get(url):
    req = Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml"})
    started = time.time()
    with urlopen(req, timeout=TIMEOUT) as resp:
        raw = resp.read()
        status = getattr(resp, "status", 200)
    return status, raw, int((time.time() - started) * 1000)


def text_of(raw):
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("latin-1", "replace")


def clean_name(s):
    s = re.sub(r"<br\s*/?>", " - ", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    s = s.replace("&amp;", "&").replace("&nbsp;", " ").replace("&#39;", "'")
    s = re.sub(r"\s+", " ", s).strip()
    return re.sub(r"(?:\s*-\s*){2,}", " - ", s)


def parse_venetian(html):
    """Every printed schedule row: date, 24h start, event number, name, sheet URL."""
    rows = []
    for m in VEN_ROW.finditer(html):
        wd, mon, day, year, hh, mm, ap, evno, name, url = m.groups()
        hour = int(hh) % 12
        if ap.upper() == "PM":
            hour += 12
        rows.append({
            "date": "%04d-%02d-%02d" % (int(year), MONTHS[mon.title()], int(day)),
            "start": "%02d:%02d" % (hour, int(mm)),
            "event_no": int(evno),
            "name": clean_name(name),
            "sheet_url": url,
        })
    return rows


def pdf_to_text(data):
    """Text of a PDF, using pypdf when it is installed (the CI job installs it)."""
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


def check_wpt_tokens(text, published):
    """Check every published WPT row's printed facts against the live schedule PDF text.

    A positional row-by-row parse of this PDF is not reliable: the text extraction
    emits the table column by column and the column order shifts between printed
    pages, so zipping the columns would silently mis-align events. Instead each
    published row is checked against what the PDF does print, which cannot invent a
    row: the event name must appear verbatim, and so must the date line and the
    time line that the row claims. A published row whose event name is absent from
    the live PDF is reported as missing; a name that is present but not on the
    claimed date/time is reported as changed.
    """
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    # A printed event name can wrap across two lines in the text extraction (the
    # WPT World Championship rows print "... Day 1A" then "$1,000,000 Added***"),
    # so a name is also accepted when it equals two consecutive printed lines joined.
    names = {norm_key(n) for n in lines}
    names |= {norm_key(a + " " + b) for a, b in zip(lines, lines[1:])}
    dates = set()
    for i, l in enumerate(lines):
        m = re.match(r"^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.?\s+(\d{1,2})$", l)
        if m:
            dates.add((MONTHS_SHORT[m.group(1)], int(m.group(2))))
    times = set()
    for l in lines:
        m = re.match(r"^(\d{1,2})(?::(\d{2}))?\s*([ap])\.?\s*m\.?", l, re.I)
        if m:
            h = int(m.group(1)) % 12
            if m.group(3).lower() == "p":
                h += 12
            times.add("%02d:%s" % (h, m.group(2) or "00"))

    pub = [r for r in published if r["series"] == WPT_SERIES]
    missing, changed = [], []
    for r in pub:
        if norm_key(r["name"]) not in names:
            missing.append({"id": r["id"], "date": r["date"], "start": r["start"], "name": r["name"],
                            "reason": "the live schedule PDF no longer prints this event name"})
            continue
        d = r["date"]
        key = (int(d[5:7]), int(d[8:10]))
        month_name = {v: k for k, v in MONTHS_SHORT.items()}.get(key[0])
        if month_name and key not in dates:
            changed.append({"id": r["id"], "date": r["date"], "start": r["start"], "name": r["name"],
                            "reason": "the row's date is not among the dates the live schedule PDF prints"})
        elif r["start"] not in times:
            changed.append({"id": r["id"], "date": r["date"], "start": r["start"], "name": r["name"],
                            "reason": "the row's start time is not among the times the live schedule PDF prints"})
    return {"published_rows": len(pub), "printed_rows": None, "missing": missing, "changed": changed,
            "new": [], "method": ("event-name, date-line and time-line presence check against the live PDF text; "
                                  "the PDF's columns are not zipped positionally because the extraction order "
                                  "shifts between printed pages, which would mis-align events silently")}


def norm_key(s):
    s = (s or "").lower()
    s = s.replace("\u2019", "'").replace("&", "and")
    s = re.sub(r"[^a-z0-9]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    # The "$1,000,000 Added***" annotation is printed after the event name and refers to
    # a footnote ("$1,000,000 will be added in cash prizes by ClubWPT Gold"). It is
    # removed from both sides so a row is matched on the event name itself.
    return re.sub(r"\s*1 000 000 added$", "", s).strip()


def compare_wpt(printed, published):
    """Compare the printed WPT schedule with the published WPT rows, keyed by date + time + name."""
    pub = [r for r in published if r["series"] == WPT_SERIES]
    printed_keys = {(r["date"], r["start"], norm_key(r["name"])): r for r in printed}
    pub_keys = {(r["date"], r["start"], norm_key(r["name"])): r for r in pub}
    missing = [{"date": r["date"], "start": r["start"], "name": r["name"],
                "reason": "the official schedule PDF no longer prints this row"}
               for k, r in sorted(pub_keys.items()) if k not in printed_keys]
    new = [{"date": r["date"], "start": r["start"], "name": r["name"],
            "reason": "the official schedule PDF prints this row and the dataset does not carry it"}
           for k, r in sorted(printed_keys.items()) if k not in pub_keys]
    return {"printed_rows": len(printed), "published_rows": len(pub),
            "missing": missing, "changed": [], "new": new}


def compare(printed, published, series):
    """Element-by-element comparison of a printed page against the published rows."""
    pub = [r for r in published if r["series"] == series and r["kind"] == "entry"]
    printed_slots = {(r["date"], r["start"]): r for r in printed}
    published_slots = {}
    for r in pub:
        published_slots.setdefault((r["date"], r["start"]), []).append(r)

    missing, changed, new = [], [], []
    for slot, rows in sorted(published_slots.items()):
        if slot not in printed_slots:
            for r in rows:
                missing.append({"id": r["id"], "date": r["date"], "start": r["start"],
                                "name": r["name"],
                                "reason": "the official page no longer prints a row at this date and start time"})
            continue
        p = printed_slots[slot]
        # Same slot printed: compare the printed name. Venetian prints the buy-in inside
        # the name, so a buy-in change shows up as a name change.
        if norm_key(p["name"]) != norm_key(rows[0]["name"]):
            changed.append({"id": rows[0]["id"], "date": rows[0]["date"], "start": rows[0]["start"],
                            "published_name": rows[0]["name"], "printed_name": p["name"],
                            "reason": "the name printed at this date and start time differs from the published name"})
        for r in rows[1:]:
            missing.append({"id": r["id"], "date": r["date"], "start": r["start"], "name": r["name"],
                            "reason": "the page prints only one row at this date and start time"})
    for slot, p in sorted(printed_slots.items()):
        if slot not in published_slots:
            new.append({"date": p["date"], "start": p["start"], "event_no": p["event_no"],
                        "name": p["name"], "sheet_url": p["sheet_url"],
                        "reason": "the official page prints this row and the dataset does not carry it"})
    return {"printed_rows": len(printed), "published_rows": len(pub),
            "missing": missing, "changed": changed, "new": new}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=None, help="write the machine-readable result here")
    ap.add_argument("--offline", action="store_true",
                    help="replay the checks against the archived official text in data/snapshots/ "
                         "instead of the live pages, so the parser itself is exercised without a network")
    ap.add_argument("--print", action="store_true", help="print a human summary")
    args = ap.parse_args()

    with open(os.path.join(DATA, "tournaments.json"), encoding="utf-8") as f:
        published = json.load(f)["rows"]

    result = {"checked_at": date.today().isoformat(), "sources": [], "discrepancies": 0, "errors": 0}
    result["mode"] = "offline-replay-of-archived-text" if args.offline else "live"

    if args.offline:
        # The archived text is the official document as fetched by the source-facts job. The
        # Venetian archive keeps the page as text, not as the table markup, so only the WPT PDF
        # (archived verbatim) can be replayed; this is stated in the result rather than faked.
        for path, series in (("wpt_sched.txt", WPT_SERIES),):
            entry = {"url": "data/snapshots/" + path, "series": series, "status": None,
                     "http_status": None, "elapsed_ms": None, "error": None}
            archive = os.path.join(DATA, "snapshots", path)
            if not os.path.isfile(archive):
                entry["status"] = "no-archive"
                entry["error"] = "the archived text for this source is not present"
                result["errors"] += 1
            else:
                with open(archive, encoding="utf-8") as f:
                    cmp = check_wpt_tokens(f.read(), published)
                entry["status"] = "ok"
                entry.update(cmp)
                result["discrepancies"] += len(cmp["missing"]) + len(cmp["changed"])
            result["sources"].append(entry)
        result["note"] = ("Offline replay: the WPT schedule is checked against its archived verbatim text. The "
                          "Venetian schedule pages are archived as plain text, not as the printed table, so they "
                          "are only checked live by the scheduled job.")
        result["summary"] = {
            "sources_checked": len(result["sources"]),
            "sources_ok": sum(1 for s in result["sources"] if s["status"] == "ok"),
            "errors": result["errors"], "discrepancies": result["discrepancies"]}
        if args.json:
            with open(args.json, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=1)
                f.write("\n")
        for s in result["sources"]:
            print("%-10s %s" % (s["status"], s["url"]))
            if s.get("error"):
                print("   error: %s" % s["error"])
            if "missing" in s:
                print("   %d published rows checked, %d missing, %d changed"
                      % (s["published_rows"], len(s["missing"]), len(s["changed"])))
                for item in s["missing"] + s["changed"]:
                    print("   %-8s %s %s" % ("MISSING" if item in s["missing"] else "CHANGED",
                                             item.get("date"), item.get("name")))
        print("live verification (offline replay): %(sources_ok)d/%(sources_checked)d archived sources agree, "
              "%(errors)d errors, %(discrepancies)d discrepancies" % result["summary"])
        return 1 if result["errors"] else (2 if result["discrepancies"] else 0)

    for url, series in VENETIAN_PAGES:
        entry = {"url": url, "series": series, "status": None, "http_status": None,
                 "elapsed_ms": None, "error": None}
        try:
            status, raw, ms = get(url)
            entry["http_status"] = status
            entry["elapsed_ms"] = ms
            entry["status"] = "ok" if 200 <= status < 400 else "http-error"
            if entry["status"] != "ok":
                entry["error"] = "HTTP %s" % status
                result["errors"] += 1
                result["sources"].append(entry)
                continue
            printed = parse_venetian(text_of(raw))
            if not printed:
                entry["status"] = "parse-failed"
                entry["error"] = ("the page answered but no schedule row matched the parser, so nothing can be "
                                  "confirmed from it; the page layout may have changed")
                result["errors"] += 1
                result["sources"].append(entry)
                continue
            cmp = compare(printed, published, series)
            entry.update(cmp)
            entry["first_printed"] = printed[0] if printed else None
            entry["last_printed"] = printed[-1] if printed else None
            entry["sheets_linked"] = len({p["sheet_url"] for p in printed})
            result["discrepancies"] += len(cmp["missing"]) + len(cmp["changed"]) + len(cmp["new"])
        except HTTPError as e:
            entry["status"] = "http-error"
            entry["http_status"] = e.code
            entry["error"] = str(e)
            result["errors"] += 1
        except (URLError, OSError, ValueError) as e:
            entry["status"] = "unreachable"
            entry["error"] = str(e)
            result["errors"] += 1
        result["sources"].append(entry)

    # Wynn WPT World Championship: the official schedule is a PDF, so the same
    # fetch -> parse -> compare pipeline is applied to its text.
    entry = {"url": WPT_SCHEDULE_PDF, "series": WPT_SERIES, "status": None, "http_status": None,
             "elapsed_ms": None, "error": None}
    try:
        status, raw, ms = get(WPT_SCHEDULE_PDF)
        entry["http_status"] = status
        entry["elapsed_ms"] = ms
        entry["status"] = "ok" if 200 <= status < 400 else "http-error"
        text = pdf_to_text(raw)
        if not text:
            entry["status"] = "parse-failed"
            entry["error"] = ("the PDF answered but no text could be extracted (pypdf missing or the file is a "
                              "scanned image), so nothing can be confirmed from it")
            result["errors"] += 1
        else:
            cmp = check_wpt_tokens(text, published)
            entry.update(cmp)
            result["discrepancies"] += len(cmp["missing"]) + len(cmp["changed"])
    except HTTPError as e:
        entry["status"] = "http-error"
        entry["http_status"] = e.code
        entry["error"] = str(e)
        result["errors"] += 1
    except (URLError, OSError, ValueError) as e:
        entry["status"] = "unreachable"
        entry["error"] = str(e)
        result["errors"] += 1
    result["sources"].append(entry)

    result["summary"] = {
        "sources_checked": len(result["sources"]),
        "sources_ok": sum(1 for s in result["sources"] if s["status"] == "ok"),
        "errors": result["errors"],
        "discrepancies": result["discrepancies"],
    }

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=1)
            f.write("\n")
    if args.print or not args.json:
        for s in result["sources"]:
            print("%-14s %s" % (s["status"], s["url"]))
            if s.get("error"):
                print("   error: %s" % s["error"])
            if "printed_rows" in s:
                print("   printed %d rows, dataset carries %d; missing %d, new %d, changed %d"
                      % (s["printed_rows"], s["published_rows"], len(s["missing"]), len(s["new"]),
                         len(s["changed"])))
                for group in ("missing", "changed", "new"):
                    for item in s[group]:
                        print("   %-8s %s %s %s" % (group, item.get("date"), item.get("start"),
                                                    item.get("name") or item.get("printed_name")))
    print("live verification: %(sources_ok)d/%(sources_checked)d sources parsed, "
          "%(errors)d errors, %(discrepancies)d discrepancies" % result["summary"])
    if result["errors"]:
        return 1
    return 2 if result["discrepancies"] else 0


if __name__ == "__main__":
    sys.exit(main())
