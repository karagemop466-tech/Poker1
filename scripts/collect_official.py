#!/usr/bin/env python3
"""Collect facts from official operator sources and detect changes.

This script is the only component that touches the network. It runs:

  * in GitHub Actions on a daily schedule (.github/workflows/monitor.yml), and
  * manually via `python3 scripts/collect_official.py`.

It writes two files that are committed back to the repository:

  data/official_facts.json   facts extracted from official pages and PDFs, plus
                             a SHA-256 of every fetched document and its fetch
                             time. Every extracted value keeps the verbatim
                             source excerpt it came from.
  data/change_log.json       one record per fetch: unchanged / changed / new /
                             unreachable, with both hashes.

Nothing is inferred. If a value is not printed on the official document, it is
left as null. If a document cannot be fetched, the previous facts are kept and
the fetch is logged as unreachable.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
SNAP = os.path.join(DATA, "snapshots")
FACTS = os.path.join(DATA, "official_facts.json")
CHANGES = os.path.join(DATA, "change_log.json")

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0 Safari/537.36 PokerPlanResearch/1.0 (+repo fact collection)")

DSE_NOV_PAGE = ("https://www.venetianlasvegas.com/resort/casino/poker/"
                "deepstack-extravaganza-poker-tournament/dse-nov-2026.html")
DSE_NYE_PAGE = ("https://www.venetianlasvegas.com/resort/casino/poker/"
                "deepstack-extravaganza-poker-tournament/dse-dec-2026.html")
WYNN_POKER = "https://www.wynnlasvegas.com/casino/poker"
WPT_SCHEDULE = ("https://cdn.wynnresorts.com/image/upload/v1757097329/"
                "visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Schedule.pdf")
WPT_STRUCTURES = ("https://cdn.wynnresorts.com/image/upload/v1750864036/"
                  "visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Structures.pdf")
WSS_SCHEDULE = ("https://cdn.wynnresorts.com/image/upload/v1756113053/"
                "visitwynn_pdfs_files/Poker/Wynn%20Signature%20Series/"
                "Wynn_Signature_Series_Schedule.pdf")

# Non-tournament documents whose text is monitored for change (hotel fees/terms).
HOTEL_DOCS = {
    "venetian_resort_fee": "https://www.venetianlasvegas.com/resort/resort-fee.html",
    "venetian_hotel_terms": "https://www.venetianlasvegas.com/legal/hotel-terms-and-conditions.html",
    "venetian_poker_suite_rates": "https://www.venetianlasvegas.com/resort/casino/poker/suite-rates.html",
    "wynn_terms": "https://www.wynnlasvegas.com/terms-and-conditions/848671",
    "caesars_disclaimer": "https://www.caesars.com/corporate/disclaimer",
    "bellagio_home": "https://bellagio.mgmresorts.com/en.html",
    "aria_home": "https://aria.mgmresorts.com/en.html",
}

NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")


def log(*a):
    print(*a, flush=True)


def fetch(url, tries=3):
    """Fetch a URL. Returns (bytes, None) or (None, error string)."""
    last = ""
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": UA,
                "Accept": "text/html,application/pdf,*/*",
                "Accept-Language": "en-US,en;q=0.9",
            })
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read(), None
        except urllib.error.HTTPError as e:
            last = "HTTP %s" % e.code
            if e.code in (403, 404, 410):
                break
        except Exception as e:  # noqa: BLE001
            last = "%s: %s" % (type(e).__name__, e)
    return None, last


def sha(b):
    return hashlib.sha256(b).hexdigest()


def pdf_text(raw):
    """Extract text from a PDF using poppler's pdftotext -layout."""
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        f.write(raw)
        path = f.name
    out = path + ".txt"
    try:
        subprocess.run(["pdftotext", "-layout", "-enc", "UTF-8", path, out],
                       check=True, capture_output=True, timeout=120)
        with open(out, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except FileNotFoundError:
        raise SystemExit("pdftotext not found: install poppler-utils")
    except subprocess.CalledProcessError as e:
        raise SystemExit("pdftotext failed: %s" % e.stderr[:400])
    finally:
        for p in (path, out):
            try:
                os.unlink(p)
            except OSError:
                pass


# ---------------------------------------------------------------- HTML rows --
TAG = re.compile(r"<[^>]+>")


def strip_tags(h):
    h = re.sub(r"<br\s*/?>", " ", h, flags=re.I)
    return re.sub(r"\s+", " ", TAG.sub("", h)).strip()


MONTHS = {m: i for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July", "August",
     "September", "October", "November", "December"], 1)}


def parse_venetian_rows(html):
    """Parse the official event table.

    Returns rows with the printed strings kept verbatim, plus a normalised date
    and 24h time. A printed year that contradicts the series dates is kept as
    printed and recorded in `printed_year`.
    """
    rows = []
    for tr in re.findall(r"<tr[^>]*>([\s\S]*?)</tr>", html, flags=re.I):
        cells = re.findall(r"<td[^>]*>([\s\S]*?)</td>", tr, flags=re.I)
        if len(cells) < 4:
            continue
        date_raw = strip_tags(cells[0])
        time_raw = strip_tags(cells[1])
        ev_raw = strip_tags(cells[2])
        name_raw = strip_tags(cells[3])
        m = re.search(r"(January|February|March|April|May|June|July|August|"
                      r"September|October|November|December)\s+(\d{1,2}),\s*(\d{4})",
                      date_raw)
        t = re.search(r"(\d{1,2}):(\d{2})\s*([APap])\.?[Mm]\.?", time_raw)
        if not (m and t and re.fullmatch(r"\d{1,3}", ev_raw.strip() or "x") is None
                or (m and t)):
            continue
        if not (m and t):
            continue
        year = int(m.group(3))
        month = MONTHS[m.group(1)]
        day = int(m.group(2))
        hour = int(t.group(1)) % 12
        if t.group(3).lower() == "p":
            hour += 12
        struct = re.search(r'href="(https://www\.venetianlasvegas\.com/content/dam/'
                           r'[^"]+\.pdf)"', cells[4] if len(cells) > 4 else "")
        rows.append({
            "printed_date": date_raw,
            "date": "%04d-%02d-%02d" % (year, month, day),
            "printed_year": year,
            "printed_time": time_raw,
            "start": "%02d:%02d" % (hour, int(t.group(2))),
            "event_no": ev_raw.strip(),
            "printed_name": name_raw,
            "structure_url": struct.group(1) if struct else None,
        })
    return rows


# ------------------------------------------------------------ PDF fact pull --
RE_KEYWORDS = [
    r"re-?entr(?:y|ies|ed)",
    r"re-?bu(?:y|ys|ying)",
    r"add-?\s?on",
    r"double\s+buy",
    r"multiple\s+entr(?:y|ies)",
    r"subsequent\s+buy",
    r"unlimited\s+entr",
]


def excerpt(text, start, end, pad=180):
    a = max(0, start - pad)
    b = min(len(text), end + pad)
    return re.sub(r"\s+", " ", text[a:b]).strip()


def numbered_clause(text, number):
    """Return the numbered clause text, e.g. clause 08."""
    pat = re.compile(r"(?:^|\n)\s*0?%d[.)]\s+([\s\S]{0,900}?)(?=\n\s*0?\d{2}[.)]\s|\Z)"
                     % number)
    m = pat.search(text)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else None


def parse_structure(text):
    """Extract the material facts from one official Venetian structure sheet."""
    flat = re.sub(r"[ \t]+", " ", text)
    one = re.sub(r"\s+", " ", text)

    def grab(pattern, group=1):
        m = re.search(pattern, one, flags=re.I)
        return re.sub(r"\s+", " ", m.group(group)).strip() if m else None

    facts = {
        "title": grab(r"^\s*(\$[\d,]+[^|\n]{0,70}?)\s*(?:\n|Level)"),
        "event_numbers_raw": grab(r"Event Numbers?:?\s*([0-9][0-9,\s&and]*)"),
        "start_time": grab(r"Start Time:?\s*(\d{1,2}:\d{2}\s*[AP]\.?M\.?)"),
        "starting_chips": grab(r"Starting Chips:?\s*([\d,]+)"),
        "level_minutes": grab(r"Level Duration:?\s*([\d]+)\s*min"),
        "late_registration": grab(r"Late Registration:?\s*([^\n]{0,90})"),
        "guarantee": grab(r"Guarantee:?\s*(\$[\d,]+[^\n]{0,90})"),
        "house_fee_clause": grab(r"(\$[\d,]+ of the \$[\d,]+ Buy-?In[^\n]{0,400})"),
        "buy_in": None,
        "house_fee": None,
        "keywords": [],
    }
    if facts["event_numbers_raw"]:
        nums = re.findall(r"\d{1,3}", facts["event_numbers_raw"])
        facts["event_numbers"] = sorted({int(n) for n in nums})
    else:
        facts["event_numbers"] = []

    m = re.search(r"\$([\d,]+) of the \$([\d,]+) Buy-?In", one)
    if m:
        facts["house_fee"] = int(m.group(1).replace(",", ""))
        facts["buy_in"] = int(m.group(2).replace(",", ""))

    # Verbatim keyword hits, with surrounding text, for re-entry / rebuy / add-on.
    for kw in RE_KEYWORDS:
        for m in re.finditer(kw, one, flags=re.I):
            facts["keywords"].append({
                "keyword": m.group(0),
                "excerpt": excerpt(one, m.start(), m.end()),
            })
    seen = set()
    uniq = []
    for k in facts["keywords"]:
        key = k["excerpt"][:120]
        if key in seen:
            continue
        seen.add(key)
        uniq.append(k)
    facts["keywords"] = uniq

    facts["clause_08"] = numbered_clause(flat, 8)
    facts["has_flight_language"] = bool(re.search(r"\bflight", one, flags=re.I))
    facts["is_satellite"] = bool(re.search(r"satellite", one, flags=re.I))
    facts["is_tag_team"] = bool(re.search(r"tag\s*team", one, flags=re.I))
    return facts


def main():
    os.makedirs(DATA, exist_ok=True)
    os.makedirs(SNAP, exist_ok=True)
    prev = {}
    if os.path.exists(FACTS):
        try:
            prev = json.load(open(FACTS, encoding="utf-8"))
        except Exception:  # noqa: BLE001
            prev = {}
    prev_docs = prev.get("documents", {})
    changes = []
    if os.path.exists(CHANGES):
        try:
            changes = json.load(open(CHANGES, encoding="utf-8")).get("records", [])
        except Exception:  # noqa: BLE001
            changes = []

    documents = {}
    structures = {}
    series = {}

    def record(slug, url, raw, kind):
        h = sha(raw)
        prev_h = prev_docs.get(url, {}).get("sha256")
        old = prev_docs.get(url, {})
        status = "new" if prev_h is None else ("unchanged" if prev_h == h else "changed")
        documents[url] = {
            "slug": slug,
            "kind": kind,
            "sha256": h,
            "bytes": len(raw),
            "fetched_utc": NOW,
            "status": status,
            "first_seen_utc": old.get("first_seen_utc", NOW),
            "previous_sha256": prev_h,
            "changed_since_first_seen": bool(prev_h and prev_h != h) or
                                        bool(old.get("changed_since_first_seen")),
        }
        changes.append({
            "checked_utc": NOW, "slug": slug, "url": url, "kind": kind,
            "status": status, "sha256": h, "previous_sha256": prev_h,
        })
        return h

    # ---- Venetian series pages ----
    for slug, url, series_name in (
            ("dse_nov_2026_page", DSE_NOV_PAGE, "Venetian DeepStack Extravaganza IV"),
            ("dse_dec_2026_page", DSE_NYE_PAGE, "Venetian DeepStack Extravaganza NYE")):
        raw, err = fetch(url)
        if raw is None:
            log("UNREACHABLE", slug, err)
            documents[url] = {"slug": slug, "kind": "html", "fetched_utc": NOW,
                              "status": "unreachable", "error": err,
                              "sha256": prev_docs.get(url, {}).get("sha256")}
            series[slug] = prev.get("series", {}).get(slug, {})
            continue
        record(slug, url, raw, "html")
        html = raw.decode("utf-8", "replace")
        rows = parse_venetian_rows(html)
        with open(os.path.join(SNAP, slug + ".rows.txt"), "w", encoding="utf-8") as f:
            for r in rows:
                f.write("%s %s ev%s %s | %s\n" % (r["date"], r["start"],
                        r["event_no"], r["printed_name"], r["structure_url"]))
        header = re.search(r"<h1[^>]*>([\s\S]*?)</h1>", html)
        dates = re.search(r"</h1>\s*<p>\s*<strong>([^<]+)</strong>", html)
        blurb = re.search(r"More than \$[\d.,]+ [^<]+", html)
        series[slug] = {
            "name": series_name,
            "url": url,
            "page_title": strip_tags(header.group(1)) if header else None,
            "printed_date_range": strip_tags(dates.group(1)) if dates else None,
            "printed_guarantee_blurb": strip_tags(blurb.group(0)) if blurb else None,
            "rows": rows,
            "rows_count": len(rows),
            "fetched_utc": NOW,
        }
        log("rows", slug, len(rows))

    # ---- Venetian structure sheets ----
    struct_urls = {}
    for slug, s in series.items():
        for r in s.get("rows", []):
            if r.get("structure_url"):
                struct_urls[r["structure_url"]] = (slug, r["event_no"])
    for url in sorted(struct_urls):
        slug, ev = struct_urls[url]
        raw, err = fetch(url)
        key = os.path.basename(url)
        if raw is None:
            log("UNREACHABLE structure", key, err)
            documents[url] = {"slug": key, "kind": "pdf", "fetched_utc": NOW,
                              "status": "unreachable", "error": err,
                              "sha256": prev_docs.get(url, {}).get("sha256")}
            if key in prev.get("structures", {}):
                structures[key] = prev["structures"][key]
            continue
        record(key, url, raw, "pdf")
        text = pdf_text(raw)
        with open(os.path.join(SNAP, key + ".txt"), "w", encoding="utf-8") as f:
            f.write(text)
        facts = parse_structure(text)
        facts.update({"url": url, "fetched_utc": NOW, "series_page": slug,
                      "referenced_by_event_no": ev,
                      "sha256": documents[url]["sha256"],
                      "raw_text_chars": len(text)})
        structures[key] = facts
        log("structure", key, "->", facts.get("event_numbers"),
            "kw", len(facts["keywords"]))

    # ---- Wynn / WPT documents ----
    for slug, url in (("wpt_schedule", WPT_SCHEDULE),
                      ("wpt_structures", WPT_STRUCTURES),
                      ("wynn_signature_schedule", WSS_SCHEDULE),
                      ("wynn_poker_page", WYNN_POKER)):
        raw, err = fetch(url)
        if raw is None:
            log("UNREACHABLE", slug, err)
            documents[url] = {"slug": slug, "kind": "pdf" if url.endswith(".pdf") else "html",
                              "fetched_utc": NOW, "status": "unreachable", "error": err,
                              "sha256": prev_docs.get(url, {}).get("sha256")}
            if slug in prev.get("wynn", {}):
                series[slug] = prev["wynn"][slug]
            continue
        kind = "pdf" if url.lower().endswith(".pdf") or raw[:4] == b"%PDF" else "html"
        record(slug, url, raw, kind)
        if kind == "pdf":
            text = pdf_text(raw)
            with open(os.path.join(SNAP, slug + ".txt"), "w", encoding="utf-8") as f:
                f.write(text)
            hits = []
            one = re.sub(r"\s+", " ", text)
            for kw in RE_KEYWORDS:
                for m in re.finditer(kw, one, flags=re.I):
                    hits.append({"keyword": m.group(0),
                                 "excerpt": excerpt(one, m.start(), m.end(), 140)})
            series[slug] = {"url": url, "kind": "pdf", "chars": len(text),
                            "re_entry_hits": hits[:40],
                            "fetched_utc": NOW}
        else:
            series[slug] = {"url": url, "kind": "html", "fetched_utc": NOW,
                            "chars": len(raw)}

    # ---- hotel / fee documents (monitored, not parsed into numbers) ----
    for slug, url in HOTEL_DOCS.items():
        raw, err = fetch(url)
        if raw is None:
            log("UNREACHABLE", slug, err)
            documents[url] = {"slug": slug, "kind": "html", "fetched_utc": NOW,
                              "status": "unreachable", "error": err,
                              "sha256": prev_docs.get(url, {}).get("sha256")}
            continue
        record(slug, url, raw, "html")
        if slug in ("venetian_resort_fee", "venetian_hotel_terms",
                    "venetian_poker_suite_rates", "wynn_terms", "caesars_disclaimer"):
            txt = strip_tags(raw.decode("utf-8", "replace"))
            with open(os.path.join(SNAP, slug + ".txt"), "w", encoding="utf-8") as f:
                f.write(txt[:400000])

    out = {
        "generated_utc": NOW,
        "generated_date": TODAY,
        "author": "scripts/collect_official.py",
        "note": ("Facts are copied verbatim from the official documents listed here. "
                 "Null means the document does not print the value. Every document is "
                 "hashed so a later run can detect a change."),
        "documents": documents,
        "series": series,
        "structures": structures,
    }
    with open(FACTS, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    # keep the log bounded but useful: newest 4000 records
    changes = changes[-4000:]
    with open(CHANGES, "w", encoding="utf-8") as f:
        json.dump({"updated_utc": NOW, "records": changes}, f, indent=1)
    ok = sum(1 for d in documents.values() if d.get("status") != "unreachable")
    bad = [d for d in documents.values() if d.get("status") == "unreachable"]
    log("done: %d documents fetched, %d unreachable, %d structures"
        % (ok, len(bad), len(structures)))
    for u, d in documents.items():
        if d.get("status") == "unreachable":
            log("  unreachable:", u, d.get("error"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
