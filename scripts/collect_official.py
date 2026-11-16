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
WSS_SCHEDULE = ("https://cdn.wynnresorts.com/image/upload/v1753296112/"
                "visitwynn_pdfs_files/Poker/Wynn%20Signature%20Series/"
                "Wynn_Signature_Series_Schedule.pdf")
WSS_STRUCTURES = ("https://cdn.wynnresorts.com/image/upload/v1762299460/"
                  "visitwynn_pdfs_files/Poker/Wynn%20Signature%20Series/"
                  "Wynn_Signature_Series_Structures.pdf")

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
        subprocess.run(["pdftotext", "-layout", "-raw", "-enc", "UTF-8", path, out],
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


# --------------------------------------------------- Wynn / WPT structure PDF --
def parse_wynn_structures(text):
    """Split a Wynn structures PDF into per-event records.

    The document alternates a structure page (title, entry fee, guarantee, blind
    levels) with a terms page (entry-fee breakdown, registration and re-entry
    rule, day listing). Pages are classified, then each terms page is paired with
    the nearest preceding unpaired structure page.
    """
    pages = text.split("\f")
    struct_pages, terms_pages = [], []
    for i, page in enumerate(pages):
        flat = re.sub(r"[ \t]+", " ", page)
        is_terms = ("TERMS AND CONDITIONS" in page.upper()
                    and re.search(r"Registration|Entry Fee:", page))
        has_levels = bool(re.search(r"Level\s+Small Blind|Level\s+Ante|Level\s+Blind", page)) or \
                     bool(re.search(r"^\s*1\s+[\d,]+\s+[\d,]+", page, flags=re.M))
        has_fee = bool(re.search(r"\$[\d,]+\s*\*{0,3}\s*Entry Fee", page))
        if is_terms:
            terms_pages.append(i)
        elif has_fee and has_levels:
            struct_pages.append(i)

    events = []
    used = set()
    for t in terms_pages:
        # nearest unpaired structure page before this terms page, skipping
        # terms pages already consumed (a terms page is never a structure page)
        prior = [x for x in struct_pages if x < t and x not in used]
        if not prior:
            continue
        sp = prior[-1]
        # skip any structure page that is itself the front of an already-paired event
        used.add(sp)
        spage, tpage = pages[sp], pages[t]
        one_struct = re.sub(r"\s+", " ", spage)
        one_terms = re.sub(r"\s+", " ", tpage)
        first = [l.strip() for l in spage.split("\n") if l.strip()]
        fee = re.search(r"\$([\d,]+)\s*\*{0,3}\s*Entry Fee", spage)
        gtd = re.search(r"\$([\d,]+)\s*\*{0,3}\s*(?:Guarantee|Guaranteed)", spage, flags=re.I)
        levels = [int(x) for x in re.findall(r"^\s*(\d{1,2})\s+[\d,]+\s+[\d,]+", spage, flags=re.M)]
        facts = {
            "index": len(events),
            "page_structure": sp,
            "page_terms": t,
            "structure_title": re.sub(r"\s+", " ", " ".join(first[:3]))[:160],
            "structure_entry_fee_usd": int(fee.group(1).replace(",", "")) if fee else None,
            "structure_guarantee_usd": int(gtd.group(1).replace(",", "")) if gtd else None,
            "levels_printed": max(levels) if levels else None,
            "entry_fee_breakdown": None,
            "registration_rule": None,
            "single_entry": None,
            "re_entry": None,
            "rebuy": None,
            "add_on": None,
            "starting_stack": None,
            "level_minutes": None,
            "day_listing": [],
            "terms_excerpt": one_terms[:1600],
        }
        m = re.search(r"(Entry Fee:?\s*\$[\d,]+[^.]{0,170})", one_terms)
        if m:
            facts["entry_fee_breakdown"] = m.group(1).strip()
        m = re.search(r"Registration:\s*(.{0,900})", one_terms)
        if m:
            seg = m.group(1)
            cut = re.search(r"(Starting Stack|Length of Play:|Breaks:|Payouts:|Action Clock)", seg)
            if cut:
                seg = seg[:cut.start()]
            facts["registration_rule"] = seg.strip()
        m = re.search(r"Players will start with ([\d,]+) in tournament chips", one_terms)
        if m:
            facts["starting_stack"] = int(m.group(1).replace(",", ""))
        m = re.search(r"(\d+ minutes? per level[^.]{0,90})", one_terms)
        if m:
            facts["level_minutes"] = m.group(1).strip()
        # The terms page prints every calendar day this structure applies to,
        # with the start time. This is the only reliable discriminator between
        # two events that share an entry fee.
        facts["day_listing"] = parse_day_listing(one_terms)
        facts["event_dates"] = [d["date"] for d in facts["day_listing"]]
        facts["event_starts"] = sorted({d["start"] for d in facts["day_listing"]})
        reg = facts["registration_rule"] or ""
        joined = one_struct + " " + one_terms
        if re.search(r"re-?entr|rebu|add-?\s?on", reg, flags=re.I):
            facts["re_entry"] = True
            facts["single_entry"] = False
        elif re.search(r"no re-?entr|single entr|freeze-?out|one \(1\) entr|only one entr",
                       joined, flags=re.I):
            facts["re_entry"] = False
            facts["single_entry"] = True
        if re.search(r"add-?\s?on", reg, flags=re.I):
            facts["add_on"] = True
        if re.search(r"rebu", reg, flags=re.I):
            facts["rebuy"] = True
        events.append(facts)
    return events


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
        cell_html = cells[4] if len(cells) > 4 else ""
        struct = None
        m2 = re.search(r'href="([^"]*?/content/dam/[^"]+?\.pdf)"', cell_html, flags=re.I)
        if m2:
            href = m2.group(1)
            if href.startswith("//"):
                href = "https:" + href
            elif href.startswith("/"):
                href = "https://www.venetianlasvegas.com" + href
            struct = href
        rows.append({
            "printed_date": date_raw,
            "date": "%04d-%02d-%02d" % (year, month, day),
            "printed_year": year,
            "printed_time": time_raw,
            "start": "%02d:%02d" % (hour, int(t.group(2))),
            "event_no": ev_raw.strip(),
            "printed_name": name_raw,
            "structure_url": struct,
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
    """Return clause <number> from a sheet whose columns are interleaved.

    Returns None when the sheet prints no numbered rules at all. When the sheet
    does print numbered rules but the clause cannot be isolated, returns the
    string 'PRESENT-BUT-UNPARSED' so the caller never treats it as absent.
    """
    has_rules = re.search(r"0?1[.)]\s+TDA rules", text)
    if not has_rules:
        return None
    pat = re.compile(r"0?%d[.)]\s*([\s\S]{0,600}?)(?=0?\d{1,2}[.)]\s+[A-Z]|\Z)" % number)
    m = pat.search(text)
    if not m:
        return "PRESENT-BUT-UNPARSED" if has_rules else None
    return re.sub(r"\s+", " ", m.group(1)).strip()


MONTHS = {m: i for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july", "august",
     "september", "october", "november", "december"], start=1)}


def parse_day_listing(one):
    """Parse the 'This event will be held on the following day(s):' bullets.

    The WPT terms pages print the exact calendar day and start time each
    structure applies to, which is the only reliable way to tell two events
    with the same fee apart.
    """
    out = []
    seg = one
    m = re.search(r"held on the following day\(s\)\s*:?(.{0,1200})", one, flags=re.I)
    if m:
        seg = m.group(1)
    for dm in re.finditer(
            r"(January|February|March|April|May|June|July|August|September|October|"
            r"November|December)\s+(\d{1,2}),?\s*(\d{4})[^.]{0,40}?(\d{1,2})(?::(\d{2}))?\s*"
            r"([ap])\.?\s*m", seg, flags=re.I):
        mon = MONTHS[dm.group(1).lower()]
        day = int(dm.group(2))
        year = int(dm.group(3))
        hh = int(dm.group(4)) % 12
        if dm.group(6).lower() == "p":
            hh += 12
        mm = dm.group(5) or "00"
        out.append({"date": "%04d-%02d-%02d" % (year, mon, day),
                    "start": "%02d:%s" % (hh, mm)})
    return out


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
        "start_time": (grab(r"Start Time:?\s*(\d{1,2}:\d{2}\s*[AP]\.?M\.?)")
                       or grab(r"@\s*(\d{1,2}:\d{2}\s*[AP]\.?M\.?)")
                       or grab(r"(\d{1,2}:\d{2}\s*[AP]\.?M\.?)\s+with", )),
        "starting_chips": grab(r"Starting Chips:?\s*([\d,]+)"),
        "level_minutes": grab(r"Level Duration:?\s*([\d]+)\s*min"),
        "late_registration": grab(r"Late Registration:?\s*(\d+\s+levels?[^\n]{0,80})"),
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
    m8 = re.search(r"(?:0?8[.)]\s*)?(Any player who bags chips[^.]*\.)", one)
    facts["clause_08_sentence"] = m8.group(1).strip() if m8 else None
    facts["mentions_players_may_not_play_subsequent_flight"] = bool(
        re.search(r"may not play a subsequent flight", one, flags=re.I))
    facts["mentions_starting_flight"] = bool(re.search(r"starting flight|flight 1[ABCDEF]",
                                                       one, flags=re.I))
    facts["has_flight_language"] = bool(re.search(r"\bflight", one, flags=re.I))
    # number of blind levels printed (first column of the level table)
    lv = re.findall(r"(?:^|\n)\s*(\d{1,2})\s+\d{1,3}\s+[\d,]+\s+[\d,]+-", flat)
    facts["levels_printed"] = max((int(x) for x in lv), default=None)
    facts["is_satellite"] = bool(re.search(r"satellite", one, flags=re.I))
    facts["is_tag_team"] = bool(re.search(r"tag\s*team", one, flags=re.I))
    # The terms page prints the exact day(s) and start time this structure applies to.
    facts["event_dates"] = parse_day_listing(one)
    return facts


def parse_wynn_schedule(text, default_year):
    """Parse the Wynn Signature Series schedule PDF by column position.

    Columns are located from the printed header line, because long event names
    run into the guarantee column. Returns rows that keep the printed strings.
    """
    lines = text.split("\n")
    hdr = None
    for l in lines:
        if "EVENT" in l and "ENTRY" in l and "GUARANTEE" in l:
            hdr = l
            break
    if hdr is None:
        return []
    cols = {k: hdr.find(k) for k in ("EVENT", "GUARANTEE", "ENTRY", "CHIPS", "LEVELS")}
    rows = []
    for line in lines:
        m = re.match(r"\s*(\d{1,2})/(\d{1,2})\s+([A-Z]{3})\s+"
                     r"(\d{1,2}(?::\d{2})?\s*[AP]\.M\.)", line)
        if not m:
            continue
        name = line[cols["EVENT"]:cols["GUARANTEE"]].strip()
        gtd = line[cols["GUARANTEE"]:cols["ENTRY"]].strip()
        entry = line[cols["ENTRY"]:cols["CHIPS"]].strip()
        chips = line[cols["CHIPS"]:cols["LEVELS"]].strip()
        levels = line[cols["LEVELS"]:].strip()
        if not entry and not levels:
            continue            # Day 2 rows print no entry and no levels
        hh, mm = None, 0
        tm = re.match(r"(\d{1,2})(?::(\d{2}))?\s*([AP])\.M\.", m.group(4))
        if tm:
            hh = int(tm.group(1)) % 12
            mm = int(tm.group(2) or 0)
            if tm.group(3) == "P":
                hh += 12
        season = default_year
        if int(m.group(1)) == 1:      # a January row belongs to the following year
            season = default_year + 1
        rows.append({
            "month": int(m.group(1)), "day": int(m.group(2)),
            "date": "%04d-%02d-%02d" % (season, int(m.group(1)), int(m.group(2))),
            "weekday_printed": m.group(3),
            "printed_time": m.group(4),
            "start": "%02d:%02d" % (hh, mm) if hh is not None else None,
            "name_printed": name,
            "guarantee_printed": gtd or None,
            "entry_printed": entry or None,
            "chips_printed": chips or None,
            "levels_printed": levels or None,
        })
    return rows


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
    prev_series = prev.get("series", {})
    prev_structs = prev.get("structures", {})
    changes = []
    if os.path.exists(CHANGES):
        try:
            changes = json.load(open(CHANGES, encoding="utf-8")).get("records", [])
        except Exception:  # noqa: BLE001
            changes = []

    documents, structures, series = {}, {}, {}

    def canonical(raw, kind):
        """Hash-able form of a document: HTML is reduced to its visible text so a
        change in markup or a rotating token is not reported as a source change."""
        if kind == "pdf":
            return raw
        text = raw.decode("utf-8", "replace")
        text = re.sub(r"<script[\s\S]*?</script>", " ", text, flags=re.I)
        text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
        text = TAG.sub(" ", text)
        return re.sub(r"\s+", " ", text).strip().encode("utf-8")

    def record(slug, url, raw, kind):
        h = sha(canonical(raw, kind))
        raw_sha = sha(raw)
        old = prev_docs.get(url, {})
        prev_h = old.get("sha256")
        status = "new" if prev_h is None else ("unchanged" if prev_h == h else "changed")
        documents[url] = {
            "slug": slug, "kind": kind, "sha256": h, "bytes": len(raw),
            "fetched_utc": NOW, "status": status,
            "first_seen_utc": old.get("first_seen_utc", NOW),
            "previous_sha256": prev_h,
            "changed_since_first_seen": bool(prev_h and prev_h != h)
                                        or bool(old.get("changed_since_first_seen")),
        }
        changes.append({"checked_utc": NOW, "slug": slug, "url": url, "kind": kind,
                        "status": status, "sha256": h, "previous_sha256": prev_h})
        return documents[url]

    def unreachable(slug, url, err, kind):
        log("UNREACHABLE", slug, err)
        documents[url] = {"slug": slug, "kind": kind, "fetched_utc": NOW,
                          "status": "unreachable", "error": err,
                          "sha256": prev_docs.get(url, {}).get("sha256")}
        changes.append({"checked_utc": NOW, "slug": slug, "url": url, "kind": kind,
                        "status": "unreachable", "sha256": None,
                        "previous_sha256": prev_docs.get(url, {}).get("sha256"),
                        "error": err})

    # ---- Venetian series pages ----
    for slug, url, series_name in (
            ("dse_nov_2026_page", DSE_NOV_PAGE, "Venetian DeepStack Extravaganza IV"),
            ("dse_dec_2026_page", DSE_NYE_PAGE, "Venetian DeepStack Extravaganza NYE")):
        raw, err = fetch(url)
        if raw is None:
            unreachable(slug, url, err, "html")
            series[slug] = prev_series.get(slug, {})
            continue
        doc = record(slug, url, raw, "html")
        html = raw.decode("utf-8", "replace")
        rows = parse_venetian_rows(html)
        with open(os.path.join(SNAP, slug + ".rows.txt"), "w", encoding="utf-8") as f:
            for r in rows:
                f.write("%s %s ev%s %s | %s\n" % (r["date"], r["start"], r["event_no"],
                                                  r["printed_name"], r["structure_url"]))
        h1 = re.search(r"<h1[^>]*>([\s\S]*?)</h1>", html)
        daterange = re.search(
            r"<strong>\s*((?:January|February|March|April|May|June|July|August|September|"
            r"October|November|December)[^<]{0,80}?\d{4})\s*</strong>", html)
        blurb = re.search(r"More than \$[\d.,]+ [^<]+", html)
        series[slug] = {
            "name": series_name, "url": url, "sha256": doc["sha256"],
            "fetched_utc": NOW,
            "page_title": strip_tags(h1.group(1)) if h1 else None,
            "printed_date_range": strip_tags(daterange.group(1)) if daterange else None,
            "printed_guarantee_blurb": strip_tags(blurb.group(0)) if blurb else None,
            "rows": rows, "rows_count": len(rows),
        }
        log("rows", slug, len(rows))

    # ---- Venetian structure sheets ----
    struct_urls = {}
    for slug, s in series.items():
        for r in s.get("rows", []):
            if r.get("structure_url"):
                struct_urls.setdefault(r["structure_url"], (slug, r["event_no"]))
    for url in sorted(struct_urls):
        slug, ev = struct_urls[url]
        key = os.path.basename(url)
        raw, err = fetch(url)
        if raw is None:
            unreachable(key, url, err, "pdf")
            if key in prev_structs:
                structures[key] = prev_structs[key]
            continue
        doc = record(key, url, raw, "pdf")
        text = pdf_text(raw)
        with open(os.path.join(SNAP, key + ".txt"), "w", encoding="utf-8") as f:
            f.write(text)
        facts = parse_structure(text)
        facts.update({"url": url, "fetched_utc": NOW, "series_page": slug,
                      "referenced_by_event_no": ev, "sha256": doc["sha256"],
                      "raw_text_chars": len(text)})
        structures[key] = facts
        log("structure", key, "->", facts.get("event_numbers"),
            "kw", len(facts.get("keywords") or []))

    # ---- Wynn / WPT documents ----
    for slug, url in (("wpt_schedule", WPT_SCHEDULE),
                      ("wpt_structures", WPT_STRUCTURES),
                      ("wynn_signature_schedule", WSS_SCHEDULE),
                      ("wynn_signature_structures", WSS_STRUCTURES),
                      ("wynn_poker_page", WYNN_POKER)):
        raw, err = fetch(url)
        if raw is None:
            unreachable(slug, url, err, "pdf")
            series[slug] = prev_series.get(slug, {})
            continue
        kind = "pdf" if url.lower().endswith(".pdf") or raw[:4] == b"%PDF" else "html"
        doc = record(slug, url, raw, kind)
        entry = {"url": url, "kind": kind, "sha256": doc["sha256"], "fetched_utc": NOW}
        if kind == "pdf":
            text = pdf_text(raw)
            with open(os.path.join(SNAP, slug + ".txt"), "w", encoding="utf-8") as f:
                f.write(text)
            one = re.sub(r"\s+", " ", text)
            hits = []
            for kw in RE_KEYWORDS:
                for m in re.finditer(kw, one, flags=re.I):
                    hits.append({"keyword": m.group(0),
                                 "excerpt": excerpt(one, m.start(), m.end(), 140)})
            entry.update({"chars": len(text), "re_entry_hits": hits[:60]})
            if slug == "wynn_signature_schedule":
                entry["rows"] = parse_wynn_schedule(text, 2026)
                entry["rows_count"] = len(entry["rows"])
                log("wynn signature schedule rows", entry["rows_count"])
            if slug in ("wpt_structures", "wynn_signature_structures"):
                entry["events"] = parse_wynn_structures(text)
                log("wynn structures", slug, len(entry["events"]), "events parsed")
        else:
            entry["chars"] = len(raw)
        series[slug] = entry

    # ---- hotel / fee documents (hashed and monitored, not parsed into numbers) ----
    for slug, url in HOTEL_DOCS.items():
        raw, err = fetch(url)
        if raw is None:
            unreachable(slug, url, err, "html")
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
        "note": ("Facts are copied verbatim from the official documents listed here. Null "
                 "means the document does not print the value. Every document is hashed so "
                 "a later run can detect a change."),
        "documents": documents,
        "series": series,
        "structures": structures,
    }
    with open(FACTS, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    changes = changes[-4000:]
    with open(CHANGES, "w", encoding="utf-8") as f:
        json.dump({"updated_utc": NOW, "records": changes}, f, indent=1)

    ok = sum(1 for d in documents.values() if d.get("status") != "unreachable")
    bad = [d for d in documents.values() if d.get("status") == "unreachable"]
    log("done: %d documents fetched, %d unreachable, %d structures"
        % (ok, len(bad), len(structures)))
    for k in ("wpt_structures", "wynn_signature_structures"):
        log("  %s events: %d" % (k, len(series.get(k, {}).get("events", []))))
    log("  signature schedule rows: %d"
        % series.get("wynn_signature_schedule", {}).get("rows_count", 0))
    for u, d in documents.items():
        if d.get("status") == "unreachable":
            log("  unreachable:", u, d.get("error"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
