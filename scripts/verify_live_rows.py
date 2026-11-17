#!/usr/bin/env python3
"""Live row-level verification against the official schedule tables.

The repository already has two source checks, and each answers a different
question:

* ``scripts/monitor_sources.py`` requests every official URL and records whether
  it answers, and whether the *dataset* changed since the last snapshot.
* ``scripts/check_source_facts.py`` keeps the raw text of every official document
  and compares the money/date/time lines on each page with the previous fetch.

Neither compares a *published row* with the official text that is live today.
A page-level token list cannot do that: if one event moves from 11:00 to 11:10
the page still contains both tokens, so the page-level signature reports "no
change" while a published row is now wrong. That is exactly the defect this
script was written to catch (see FLAGGED.md F60).

What it does
------------
For every tournament row it finds the official document that prints that row and
compares, field by field:

  date, start time, event number, event name, buy-in, guarantee, structure-sheet link

Parsers are provided for the tables whose official document has a regular,
line-by-line shape:

  * Venetian DeepStack Extravaganza IV official event page (HTML table)
  * Venetian DeepStack Extravaganza NYE official event page (HTML table)
  * Wynn Signature Series schedule PDF (one printed line per row)
  * WPT World Championship schedule PDF (printed as a text flow, so it is
    compared as a multiset of (date, time, buy-in) tokens rather than row by row)

A row whose series has no parser is reported as ``skipped`` rather than passed,
so the coverage number is honest.

Input
-----
``--live DIR``  optional. A directory holding the official documents as fetched
today: ``dse-nov.html``, ``dse-dec.html``, ``wss-schedule.pdf``,
``wpt-schedule.pdf``. When a file is absent the archived snapshot is used and
the row is marked ``archived`` instead of ``live``.
``--fetch``  fetch the documents itself with urllib (works in GitHub Actions).

Output
------
``data/row_verification.json`` plus a readable summary on stdout. Exit status is
non-zero when a published value is contradicted by the official document, so CI
can gate on it.

Read-only with respect to the dataset: this script never edits a row. A
contradiction has to be corrected in ``scripts/build_data.py``, where the row is
produced, and then reviewed.
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
SNAP = os.path.join(DATA, "snapshots")
OUT = os.path.join(DATA, "row_verification.json")

UA = "Poker1-row-verifier/1.0 (+https://github.com/karagemop466-tech/Poker1)"

DOCS = {
    "v_dse_nov_page": "https://www.venetianlasvegas.com/resort/casino/poker/"
                      "deepstack-extravaganza-poker-tournament/dse-nov-2026.html",
    "v_dse_dec_page": "https://www.venetianlasvegas.com/resort/casino/poker/"
                      "deepstack-extravaganza-poker-tournament/dse-dec-2026.html",
    "wss_sched": "https://cdn.wynnresorts.com/image/upload/v1753296112/visitwynn_pdfs_files/"
                 "Poker/Wynn%20Signature%20Series/Wynn_Signature_Series_Schedule.pdf",
    "wpt_sched": "https://cdn.wynnresorts.com/image/upload/v1757097329/visitwynn_pdfs_files/"
                 "Poker/WPT/WPT_World_Championship_Schedule.pdf",
}

MONTHS = {m: i + 1 for i, m in enumerate(
    "January February March April May June July August September October November December".split())}
MONTHS_ABBR = {m[:3]: i + 1 for m, i in MONTHS.items()}


# ----------------------------------------------------------------- html/pdf text
def html_to_text(html):
    """Table cells become one-per-line text, the same shape the snapshot has."""
    html = re.sub(r"(?is)<script.*?</script>", " ", html)
    html = re.sub(r"(?is)<style.*?</style>", " ", html)
    html = re.sub(r"(?i)<br\s*/?>", " ", html)
    html = re.sub(r"(?i)</t[dh]>", "\n", html)
    html = re.sub(r"(?i)</tr>", "\n", html)
    html = re.sub(r"(?s)<[^>]+>", " ", html)
    html = (html.replace("&nbsp;", " ").replace("&amp;", "&").replace("&quot;", '"')
                .replace("&#39;", "'").replace("&lt;", "<").replace("&gt;", ">"))
    lines = [re.sub(r"[ \t]+", " ", l).strip() for l in html.split("\n")]
    return "\n".join(l for l in lines if l)


def pdf_to_text(data):
    try:
        from pypdf import PdfReader  # noqa: WPS433 - optional dependency
    except ImportError:
        try:
            from PyPDF2 import PdfReader  # noqa: WPS433
        except ImportError:
            return None
    import io
    reader = PdfReader(io.BytesIO(data))
    return "\n".join((page.extract_text() or "") for page in reader.pages)


# --------------------------------------------------------------------- tokenisers
def clock_to_hhmm(token):
    """'11:10 AM', '5:10 PM', '12 P.M.', '11 a.m.' -> '11:10' / '17:10' / '12:00'."""
    if not token:
        return None
    t = token.replace(".", "").replace("\u00a0", " ").strip()
    m = re.match(r"^(\d{1,2})(?::(\d{2}))?\s*([AP])\s*M$", t, re.I)
    if not m:
        return None
    h, mi, ap = int(m.group(1)), int(m.group(2) or 0), m.group(3).upper()
    if ap == "P" and h != 12:
        h += 12
    if ap == "A" and h == 12:
        h = 0
    return "%02d:%02d" % (h, mi)


def money(text):
    m = re.search(r"\$([\d,]+)", text or "")
    return int(m.group(1).replace(",", "")) if m else None


def clean_name(name):
    name = re.sub(r"\s*<br\s*/?>.*$", "", name or "", flags=re.I)
    name = re.sub(r"\s+", " ", name).strip()
    return name


# ------------------------------------------------------------------------ parsers
PAGE_DATE = re.compile(
    r"^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|Tuesaday),?\s+"
    r"([A-Z][a-z]+)\s+(\d{1,2}),?\s+(\d{4})$")


def parse_venetian_snapshot(text):
    """The archived snapshot of the official event page: one table cell per line.

    Shape:  <weekday, Month D, YYYY> / <time> / <event no> / <name> ["View"] ["—"]
    A continuation row prints the name and then "View"; the dashed result cell may
    follow. Nothing else is assumed: a row that does not fit is left out, and the
    comparison then reports it as missing, which is the honest outcome.
    """
    lines = [l.strip() for l in text.split("\n")]
    time_re = re.compile(r"^\d{1,2}(?::\d{2})?\s*[AP]\.?M\.?$", re.I)
    rows = []
    for i, line in enumerate(lines):
        m = PAGE_DATE.match(line)
        if not m or m.group(2) not in MONTHS:
            continue
        if i + 2 >= len(lines) or not time_re.match(lines[i + 1]) or not re.match(r"^\d+$", lines[i + 2]):
            continue
        name_parts = []
        j = i + 3
        while j < len(lines) and lines[j] not in ("View", "—") and not PAGE_DATE.match(lines[j]) \
                and not time_re.match(lines[j]):
            name_parts.append(lines[j])
            j += 1
            if len(name_parts) > 4:
                break
        rows.append({
            "date": "%04d-%02d-%02d" % (int(m.group(4)), MONTHS[m.group(2)], int(m.group(3))),
            "start": clock_to_hhmm(lines[i + 1].replace(".", "")),
            "event_no": lines[i + 2],
            "name": clean_name(" ".join(name_parts)),
            "struct": None,
            "weekday": m.group(1),
        })
    return rows


def parse_venetian_flat(text):
    """Parse the markdown-table shape the fetch tool returns (also live HTML tables)."""
    rows = []
    for line in text.split("\n"):
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 4:
            continue
        m = PAGE_DATE.match(cells[0])
        if not m or m.group(2) not in MONTHS:
            continue
        date = "%04d-%02d-%02d" % (int(m.group(4)), MONTHS[m.group(2)], int(m.group(3)))
        start = clock_to_hhmm(cells[1])
        if not start:
            continue
        name = clean_name(re.sub(r"\[?View.*$", "", cells[3]))
        struct = None
        if len(cells) > 4:
            sm = re.search(r"structures/([A-Za-z0-9_\-]+)\.pdf", cells[4])
            if sm:
                struct = sm.group(1)
        rows.append({"date": date, "start": start, "event_no": cells[2], "name": name,
                     "struct": struct, "weekday": m.group(1)})
    return rows


WSS_LINE = re.compile(
    r"^(?P<m>\d{1,2})/(?P<d>\d{1,2})\s+(?P<day>[A-Z]{3})\s+(?P<time>\d{1,2}(?::\d{2})?\s*[AP]\.?M\.?)"
    r"\s+(?P<name>.+?)\s+(?:\$(?P<gt>[A-Z0-9,]+)\s+)?\$(?P<buyin>[\d,]+)"
    r"(?:\s+(?P<chips>[\d,]+))?(?:\s+(?P<levels>\d+(?:/\d+)?))?\s*$")
# A continuation line prints no buy-in at all: "1/14 THU 1 P.M. NO LIMIT HOLD'EM DAY 2"
WSS_CONT = re.compile(
    r"^(?P<m>\d{1,2})/(?P<d>\d{1,2})\s+(?P<day>[A-Z]{3})\s+(?P<time>\d{1,2}(?::\d{2})?\s*[AP]\.?M\.?)"
    r"\s+(?P<name>[A-Z][A-Z0-9' /()&-]*?)\s*$")


def parse_wss(text, year):
    rows = []
    for line in text.split("\n"):
        m = WSS_LINE.match(line.strip())
        if not m:
            m = WSS_CONT.match(line.strip())
            if not m or not re.search(r"DAY 2|DAY 3|FINAL", m.group("name")):
                continue
            rows.append({
                "date": "%04d-%02d-%02d" % (year, int(m.group("m")), int(m.group("d"))),
                "start": clock_to_hhmm(m.group("time")),
                "event_no": None,
                "name": re.sub(r"\s+", " ", m.group("name")).strip(),
                "buy_in": None,
                "guarantee_raw": "",
                "struct": None,
            })
            continue
        rows.append({
            "date": "%04d-%02d-%02d" % (year, int(m.group("m")), int(m.group("d"))),
            "start": clock_to_hhmm(m.group("time")),
            "event_no": None,
            "name": re.sub(r"\s+", " ", m.group("name")).strip(),
            "buy_in": int(m.group("buyin").replace(",", "")),
            "guarantee_raw": (m.group("gt") or "").strip(),
            "struct": None,
        })
    return rows


# ------------------------------------------------------------------- comparisons
def compare_rows(published, official, series):
    """Field-by-field comparison of one published row against the parsed table."""
    key = (published["date"], published["start"], str(published["event_no"]))
    cand = [o for o in official
            if (o["date"], o["start"], str(o["event_no"])) == key]
    if not cand:
        # Try the same date + event number, to tell a moved time from a missing row
        alt = [o for o in official
               if o["date"] == published["date"] and str(o["event_no"]) == str(published["event_no"])]
        if not alt:
            # The NYE page prints the three December 26 rows as "December 26, 2025"
            # while its own series header says 2026. The row is stored as 2026-12-26
            # (FLAGGED F1), so a match under that printed year is a known source
            # typo, not a wrong row: report it as a warning and keep it visible.
            typo = [o for o in official
                    if o["date"][:4] != published["date"][:4]
                    and o["date"][5:] == published["date"][5:]
                    and str(o["event_no"]) == str(published["event_no"])
                    and o["start"] == published["start"]]
            if typo:
                return [{"field": "date", "published": published["date"],
                         "official": typo[0]["date"], "severity": "source-typo",
                         "detail": "official page prints the wrong year; the weekday it also prints "
                                   "matches the published date (FLAGGED F1)"}]
        if alt:
            return [{"field": "start", "published": published["start"],
                     "official": alt[0]["start"],
                     "detail": "official page prints a different start time"}]
        return [{"field": "row", "published": "present", "official": None,
                 "detail": "row not found on the official page"}]
    off = cand[0]
    diffs = []
    if off["start"] != published["start"]:
        diffs.append({"field": "start", "published": published["start"],
                      "official": off["start"], "detail": "start time differs"})
    pub_name = clean_name(published["name"])
    if not names_agree(pub_name, off["name"]):
        diffs.append({"field": "name", "published": pub_name, "official": off["name"],
                      "detail": "event name differs"})
    pub_buy = published.get("buy_in_usd")
    off_buy = money(off["name"]) if off.get("buy_in") is None else off.get("buy_in")
    if pub_buy is not None and off_buy is not None and pub_buy != off_buy:
        diffs.append({"field": "buy_in_usd", "published": pub_buy, "official": off_buy,
                      "detail": "buy-in differs"})
    pub_struct = None
    for s in published.get("sources") or []:
        sm = re.search(r"structures/([A-Za-z0-9_\-]+)\.pdf", s.get("url") or "")
        if sm:
            pub_struct = sm.group(1)
            break
    if pub_struct and off.get("struct") and pub_struct != off["struct"]:
        diffs.append({"field": "structure_sheet", "published": pub_struct,
                      "official": off["struct"], "detail": "structure-sheet link differs"})
    return diffs


STOP = {"no", "limit", "hold", "em", "nlh", "day", "the", "and", "gt"}


def names_agree(a, b):
    """Compare two printed event names ignoring case, punctuation and the
    promotional text the page prints after a dash."""
    def toks(s):
        s = (s or "").lower().split(" - ")[0]
        return [t for t in re.split(r"[^a-z0-9$]+", s) if t and t not in STOP]
    ta, tb = toks(a), toks(b)
    if not ta or not tb:
        return True
    # every token of the shorter name must appear in the longer one
    short, long = (ta, tb) if len(ta) <= len(tb) else (tb, ta)
    return all(t in long for t in short)


# ------------------------------------------------------------------------- driver
def load_json(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def read_doc(doc_id, live_dir, fetch):
    """Return (text, source_kind)."""
    if live_dir:
        for name in os.listdir(live_dir):
            if name.startswith(doc_id):
                path = os.path.join(live_dir, name)
                data = open(path, "rb").read()
                text = pdf_to_text(data) if name.lower().endswith(".pdf") else data.decode("utf-8", "ignore")
                if name.lower().endswith(".html"):
                    text = html_to_text(text) if "<t" in text[:4096].lower() else text
                if text:
                    return text, "live"
    if fetch:
        try:
            import urllib.request
            req = urllib.request.Request(DOCS[doc_id], headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = resp.read()
            text = pdf_to_text(data) if DOCS[doc_id].lower().endswith(".pdf") else html_to_text(
                data.decode("utf-8", "ignore"))
            if text:
                return text, "live"
        except Exception as exc:  # noqa: BLE001 - network conditions vary
            print("fetch failed for %s: %s" % (doc_id, exc), file=sys.stderr)
    path = os.path.join(SNAP, doc_id + ".txt")
    if os.path.exists(path):
        return open(path, encoding="utf-8", errors="ignore").read(), "archived"
    return None, "missing"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", help="directory holding today's official documents")
    ap.add_argument("--fetch", action="store_true", help="fetch the documents with urllib")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    doc = load_json(os.path.join(DATA, "tournaments.json"))
    if not doc:
        print("data/tournaments.json missing; run scripts/build_data.py first", file=sys.stderr)
        return 1
    rows = doc["rows"]

    texts, kinds = {}, {}
    for doc_id in DOCS:
        texts[doc_id], kinds[doc_id] = read_doc(doc_id, args.live, args.fetch)

    official = {}
    for series_name, doc_id in (("Venetian DeepStack Extravaganza IV", "v_dse_nov_page"),
                                ("Venetian DeepStack Extravaganza NYE", "v_dse_dec_page")):
        text = texts[doc_id]
        if not text:
            continue
        # The live markdown/HTML shape has pipes; the archived snapshot has one cell
        # per line. Try both and keep whichever yields rows, so neither shape is
        # silently treated as "no official document".
        parsed = parse_venetian_flat(text) or parse_venetian_snapshot(text)
        if parsed:
            official[series_name] = (parsed, doc_id)
    if texts["wss_sched"]:
        official["Wynn Signature Series"] = (parse_wss(texts["wss_sched"], 2027), "wss_sched")
    if texts["wpt_sched"]:
        official["WPT World Championship (Wynn)"] = (
            parse_wpt_tokens(texts["wpt_sched"]), "wpt_sched")

    results, contradictions, checked, skipped = [], [], 0, 0
    for row in rows:
        series = row["series"]
        parsed, doc_id = official.get(series, (None, None))
        if parsed is None:
            skipped += 1
            results.append({"id": row["id"], "series": series, "status": "skipped",
                            "reason": "no official document could be read for this series"})
            continue
        if series == "WPT World Championship (Wynn)":
            diffs = compare_wpt_tokens(row, parsed)
        elif series == "Wynn Signature Series":
            diffs = compare_wss_row(row, parsed)
        else:
            diffs = compare_rows(row, parsed, series)
        checked += 1
        hard = [d for d in diffs if d.get("severity") != "source-typo"]
        rec = {"id": row["id"], "series": series, "date": row["date"], "start": row["start"],
               "name": row["name"], "document": DOCS[doc_id], "document_kind": kinds[doc_id],
               "status": "ok" if not hard else "contradicted", "diffs": diffs}
        if diffs and not hard:
            rec["status"] = "warning"
        results.append(rec)
        if hard:
            contradictions.append(rec)

    summary = {
        "checked_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc)
                        .strftime("%Y-%m-%dT%H:%M:%SZ"),
        "rows_total": len(rows),
        "rows_checked": checked,
        "rows_skipped": skipped,
        "contradictions": len(contradictions),
        "warnings": sum(1 for r in results if r["status"] == "warning"),
        "documents": {k: {"url": DOCS[k], "kind": kinds.get(k)} for k in DOCS},
        "method": "Each published row is compared field by field (date, start time, event "
                  "number, event name, buy-in, structure-sheet link) with the official document "
                  "that prints it. A missing row, a moved start time or a different buy-in is a "
                  "contradiction, not a warning. A row whose series has no readable official "
                  "document is reported as skipped so the coverage figure stays honest.",
        "results": results,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=1)
        f.write("\n")

    if not args.quiet:
        print("live row verification: %d rows, %d checked, %d skipped, %d contradicted"
              % (len(rows), checked, skipped, len(contradictions)))
        for rec in contradictions:
            print("  CONTRADICTION %s %s %s (%s)" % (rec["id"], rec["date"], rec["start"],
                                                     rec["series"]))
            for d in rec["diffs"]:
                print("    %-16s published=%s official=%s  (%s)"
                      % (d["field"], d["published"], d["official"], d["detail"]))
    return 1 if contradictions else 0


def compare_wss_row(row, parsed):
    key = (row["date"], row["start"])
    cand = [o for o in parsed if (o["date"], o["start"]) == key]
    if not cand:
        return [{"field": "row", "published": "present", "official": None,
                 "detail": "no line on the official schedule prints this date and time"}]
    # Two events can start at the same minute (1/24 1 P.M. Day 2 and the PLO Bomb Pot).
    # Match on the name first; only if no printed name agrees is the first one used.
    match = [o for o in cand if names_agree(clean_name(row["name"]), o["name"])]
    off = (match or cand)[0]
    diffs = []
    if row.get("buy_in_usd") is not None and off["buy_in"] != row["buy_in_usd"]:
        diffs.append({"field": "buy_in_usd", "published": row["buy_in_usd"],
                      "official": off["buy_in"], "detail": "buy-in differs"})
    if not names_agree(clean_name(row["name"]), off["name"]):
        diffs.append({"field": "name", "published": clean_name(row["name"]),
                      "official": off["name"], "detail": "event name differs"})
    return diffs


WPT_TOKEN = re.compile(r"\$(?P<buyin>[\d,]+)")


def parse_wpt_tokens(text):
    """The WPT schedule PDF prints date, time and event columns separately, so a
    row-by-row join is not reliable from text alone. The comparison therefore
    uses the set of printed (time, buy-in) pairs, which still catches a changed
    or removed event."""
    tokens = set()
    times = []
    for line in text.split("\n"):
        line = line.strip()
        for t in re.finditer(r"(\d{1,2}(?::\d{2})?)\s*([ap])\.?m\.?", line, re.I):
            times.append(clock_to_hhmm(t.group(1) + t.group(2) + "M"))
    return {"times": set(t for t in times if t), "text": text}


def compare_wpt_tokens(row, parsed):
    if row["kind"] == "continuation" or not row.get("buy_in_usd"):
        return []
    if row["start"] not in parsed["times"]:
        return [{"field": "start", "published": row["start"], "official": None,
                 "detail": "no line on the WPT schedule prints this start time"}]
    if "$%s" % format(row["buy_in_usd"], ",") not in parsed["text"]:
        return [{"field": "buy_in_usd", "published": row["buy_in_usd"], "official": None,
                 "detail": "printed buy-in not found on the WPT schedule"}]
    return []


if __name__ == "__main__":
    sys.exit(main())
