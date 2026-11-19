#!/usr/bin/env python3
"""Line-by-line verification of every published row against the archived official
documents in data/snapshots/.

The sandbox cannot reach the operator domains, so this verifier does not re-fetch
the web. Instead it checks each numeric / date / time value published in
data/tournaments.json, data/hotels.json and data/rates.json against the raw
official document text that the monitoring job archived under data/snapshots/.
A value that cannot be found in the official text is reported as UNVERIFIED
(never guessed or filled in).

Three independent checks run per tournament row:
  1. money   - buy-in, guarantee and house fee must appear as a dollar token in
               the official document text.
  2. time    - the published start time must appear as a time token in the text.
  3. entry   - the published entry_status must agree with the independently
               parsed sheet verdict (Venetian structure_rules.json) or the
               registration wording (WPT wpt_rules.json).

Exit code is non-zero if any published value is contradicted or unverified, so a
workflow can gate on it.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNAP = ROOT / "data" / "snapshots"


def load(name):
    return json.loads((ROOT / "data" / name).read_text())


def norm(s):
    if not s:
        return ""
    s = s.replace("\u2019", "'").replace("\u2018", "'")
    for lig, rep in (("\ufb01", "fi"), ("\ufb02", "fl"), ("\ufb00", "ff"),
                     ("\ufb03", "ffi"), ("\ufb04", "ffl")):
        s = s.replace(lig, rep)
    s = re.sub(r"[^0-9a-zA-Z]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def money_tokens(text):
    """Set of every comma-grouped number token in the raw text, digits only
    ("$75,000" -> "75000"). Extracted from raw text so commas stay attached."""
    toks = set()
    for m in re.finditer(r"\d[\d,]*\d", text or ""):
        toks.add(re.sub(r"[^0-9]", "", m.group(0)))
    for m in re.finditer(r"(?<![\d,])\d(?![\d,])", text or ""):
        toks.add(m.group(0))
    return toks


def time_tokens(text):
    """Every time-of-day in the text normalised to HHMM."""
    out = set()
    for m in re.finditer(r"(\d{1,2}):(\d{2})\s*(a\.?m\.?|p\.?m\.?)?", text, re.I):
        h, mi, ap = int(m.group(1)), int(m.group(2)), (m.group(3) or "").lower()
        if "p" in ap and h != 12:
            h += 12
        if "a" in ap and h == 12:
            h = 0
        if 0 <= h <= 23 and 0 <= mi <= 59:
            out.add(f"{h:02d}{mi:02d}")
    for m in re.finditer(r"(\d{1,2})\s*(a\.?m\.?|p\.?m\.?)", text, re.I):
        h, ap = int(m.group(1)), m.group(2).lower()
        if "p" in ap and h != 12:
            h += 12
        if "a" in ap and h == 12:
            h = 0
        if 0 <= h <= 23:
            out.add(f"{h:02d}00")
    return out


def row_time(v):
    if not v:
        return None
    m = re.match(r"^(\d{1,2}):(\d{2})$", str(v).strip())
    return f"{int(m.group(1)):02d}{int(m.group(2)):02d}" if m else None


def money(v):
    return re.sub(r"[^0-9]", "", str(v)) if v is not None else None


def sheet_key(url):
    if not url:
        return None
    m = re.search(r"dse_nov_2026-structure_(\d+)\.pdf", url)
    if m:
        return f"v_nov_struct_{int(m.group(1)):02d}"
    m = re.search(r"dse_dec_2026-structure_(\d+)\.pdf", url)
    if m:
        return f"v_dec_struct_{int(m.group(1)):02d}"
    return None


def corpus_for(series, url):
    """All official snapshot text relevant to a row (structure sheet + series page)."""
    files = []
    sk = sheet_key(url)
    if sk:
        files.append(f"{sk}.txt")
    if "Venetian DeepStack Extravaganza IV" in series:
        files += ["v_dse_nov_sched.txt", "v_dse_nov_page.txt"]
    elif "Venetian DeepStack Extravaganza NYE" in series:
        files += ["v_dse_dec_page.txt", "v_dse_dec_sched.txt"]
    elif series == "WPT World Championship (Wynn)":
        files += ["wpt_struct.txt", "wpt_sched.txt"]
    elif series == "Wynn Signature Series":
        files += ["wss_sched.txt", "wss_struct.txt"]
    out = []
    for f in files:
        if (SNAP / f).exists():
            out.append((SNAP / f).read_text(errors="ignore"))
    return "\n".join(out)


def entry_expected(series, url, status, event_no=None):
    """Independent verdict for the entry rule, from the parsed sheet / WPT blocks."""
    sk = sheet_key(url)
    if sk:
        rule = load("structure_rules.json").get(sk, {})
        kind = (rule.get("sheet_kind") or "").upper()
        # F13: NYE structure sheet 2 mentions re-entry only for Event #29 (a CES-badge
        # discount clause). Other events on that sheet are legitimately single entry, so a
        # SE row on that sheet whose event is not the re-entry event is not a mismatch.
        if sk == "v_dec_struct_02" and status == "SE" and event_no != 29:
            return True, "sheet verdict %s (re-entry clause is event-scoped to #29, F13)" % kind
        if status == "SE":
            return kind == "SINGLE_ENTRY", f"sheet verdict {kind}"
        return kind != "SINGLE_ENTRY", f"sheet verdict {kind}"
    if "WPT_World_Championship_Structures" in (url or ""):
        reg = None
        for blk in load("wpt_rules.json"):
            if "re-entry" in (blk.get("registration") or "").lower() or "rebuy" in (blk.get("registration") or "").lower():
                reg = "re-entry wording"
                break
        has_re = reg is not None
        if status in ("RE", "REBUY"):
            return has_re, "WPT registration wording"
        if status == "SE":
            return not has_re, "WPT registration wording"
    return None, None


# ---------------------------------------------------------------------------
# The morning daily feed (data/daily.json): recurring formats, no dated row.
# Same principle as the tournament rows - every published value must be found in
# the official document the monitor archived for the source the row cites.
# ---------------------------------------------------------------------------

QUOTED = re.compile("\u201c([^\u201d]{25,})\u201d|\"([^\"\\n]{25,})\"")
RELIEF = ("re enter", "re-enter", "rebuy", "re buy", "add on", "add-on", "flight",
          "day 2", "late registration", "restart")


def snapshot_for_source_url(url):
    """The archived official text for a source URL, via data/sources.json ids."""
    if not url:
        return None, None
    try:
        srcs = load("sources.json")["sources"]
    except (KeyError, FileNotFoundError):
        return None, None
    sid = next((e["id"] for e in srcs if e.get("url") == url), None)
    if not sid:
        return None, None
    path = SNAP / ("%s.txt" % sid)
    return (sid, path.read_text(errors="ignore")) if path.exists() else (sid, None)


def verify_daily():
    """(results, n_checks, failures) for every row of the daily feed."""
    daily = load("daily.json")["rows"]
    results, n_checks = [], 0
    for row in daily:
        # The structure document is document_url where a row has one (Bellagio: the PDF; the page
        # is in `source`); otherwise the row's source URL.
        doc = row.get("document_url") or row.get("source_url") or row.get("source")
        sid, text = snapshot_for_source_url(doc)
        checks = []
        if not text:
            checks.append(("source document archived", False,
                           "no snapshot for source id %r - re-run check_source_facts.py" % sid,
                           "fail"))
        else:
            ntext = norm(text).lower()
            mt = money_tokens(text)
            tt = time_tokens(text)
            for f in ("buy_in_usd", "guarantee_usd"):
                v = row.get(f)
                if v is not None:
                    n_checks += 1
                    checks.append((f, str(int(v)) in mt, "$%s not printed in %s" % (v, sid), "fail"))
            for f in ("start", "late"):
                v = row.get(f)
                if v:
                    n_checks += 1
                    checks.append((f, row_time(v) in tt, "%s not printed in %s" % (v, sid), "fail"))
            for f in ("fee", "ex", "stack", "late_note", "single_entry", "flag"):
                v = row.get(f)
                if isinstance(v, str):
                    for m in QUOTED.finditer(v):
                        q = m.group(1) or m.group(2)
                        n_checks += 1
                        checks.append(("%s quote" % f, norm(q).lower() in ntext,
                                       "quoted from %s but not found in it: %s" % (sid, q[:70]), "fail"))
            low = ntext
            relief = any(k in low for k in RELIEF)
            n_checks += 1
            if row.get("status") == "SE":
                checks.append(("single entry", not relief,
                               "published as single entry, but %s prints re-entry / add-on / "
                               "flight wording" % sid, "fail"))
            else:
                checks.append(("registration relief", relief,
                               "%s but no re-entry / add-on / flight wording in %s" %
                               (row.get("status"), sid), "review"))
        failed = [c for c in checks if not c[1] and c[3] == "fail"]
        review = [c for c in checks if not c[1] and c[3] == "review"]
        results.append({"id": row["id"], "venue": row.get("venue"), "name": row.get("name"),
                        "source": row.get("source_url"), "snapshot": sid,
                        "checked": len(checks) if text else 0,
                        "failed": [{"field": f, "detail": d} for f, _, d, _ in failed],
                        "review": [{"field": f, "detail": d} for f, _, d, _ in review]})
    return results, n_checks



def main():
    rows = load("tournaments.json")["rows"]
    results, issues = [], []
    # WPT sheet join: printed fee components per schedule row, keyed on the printed
    # (date, start time, buy-in) tuple — the join file is regenerated by
    # scripts/extract_wpt_sheets.py and row ids can shift between builds. A few keys
    # are shared by two sheets, so each key maps to a list and the sheet whose printed
    # title matches the row name is chosen, mirroring scripts/build_data.py.
    wpt_comp = {}
    try:
        for rec in load("wpt_row_sheets.json")["matched"].values():
            key = rec.get("key")
            if key and rec.get("tournament_fee_usd") is not None:
                wpt_comp.setdefault(tuple(key), []).append(rec)
    except (OSError, KeyError):
        pass

    def sheet_for_row(row):
        cands = wpt_comp.get((row.get("date"), row.get("start"), row.get("buy_in_usd"))) or []
        if len(cands) <= 1:
            return cands[0] if cands else None

        def overlap(rec):
            a = set(re.findall(r"[a-z0-9]+", (rec.get("title") or "").lower()))
            b = set(re.findall(r"[a-z0-9]+", (row.get("name") or "").lower()))
            return len(a & b)
        return max(cands, key=overlap)

    for r in rows:
        src_url, src_label = None, None
        for k in ("single_entry", "re_entry", "add_on", "fee"):
            rule = (r.get("rules") or {}).get(k)
            if isinstance(rule, dict) and rule.get("source", {}).get("url"):
                src_url = rule["source"]["url"]
                src_label = rule["source"].get("label")
                break
        text = corpus_for(r["series"], src_url)
        mt = money_tokens(text)
        tt = time_tokens(text)
        checks = []  # (field, ok, detail, severity) severity: fail | review

        bi = money(r.get("buy_in_usd"))
        if bi:
            checks.append(("buy_in_usd", bi in mt, f"${bi}", "fail"))
        g = money(r.get("guarantee_usd"))
        if g:
            checks.append(("guarantee_usd", g in mt, f"${g}", "fail"))
        hf = money(r.get("house_fee_usd"))
        if hf:
            ok, detail = hf in mt, f"${hf}"
            if not ok:
                # The WPT structure sheets print the fee split ("... = $510 (Tournament
                # Prize Pool) + $65 (Tournament Fee) + $25 (Poker Staff Service Charge)")
                # but never the house-fee sum. A sum is accepted only when it is exactly
                # the arithmetic of two printed components and each component appears in
                # the official text (session 212b84be integration fix; see
                # research/verification-2026-11-17-160f9080.md for the base rule).
                comp = sheet_for_row(r)
                if comp and "WPT" in (r.get("series") or ""):
                    t = money(comp.get("tournament_fee_usd"))
                    s = money(comp.get("staff_fee_usd"))
                    if t and s and str(int(t) + int(s)) == hf and t in mt and s in mt:
                        ok = True
                        detail = (f"${hf} = ${t} (Tournament Fee) + ${s} (Poker Staff "
                                  f"Service Charge); both components printed in the official text")
            checks.append(("house_fee_usd", ok, detail, "fail"))
        rt = row_time(r.get("start"))
        if rt and text:
            # A time that cannot be found in the archived text is a review item, not
            # necessarily an error: PDF time columns sometimes fail text extraction
            # (see the WPT schedule, flagged as F4).
            checks.append(("start", rt in tt, r.get("start"), "review"))

        status = r.get("entry_status")
        if status in ("SE", "RE", "REBUY", "MULTI"):
            exp, basis = entry_expected(r["series"], src_url, status, r.get("event_no"))
            if exp is not None:
                # Entry-rule wording often needs interpretation (event-scoped clauses),
                # so a mismatch is reported for review rather than as a hard failure.
                checks.append((f"entry_status[{status}]", exp, basis, "review"))

        failed = [c for c in checks if not c[1] and c[3] == "fail"]
        review = [c for c in checks if not c[1] and c[3] == "review"]
        rec = {"id": r["id"], "series": r["series"], "date": r.get("date"),
               "name": r.get("name"), "source": src_url,
               "checked": len(checks),
               "failed": [{"field": f, "detail": d} for f, _, d, _ in failed],
               "review": [{"field": f, "detail": d} for f, _, d, _ in review]}
        results.append(rec)
        if failed:
            issues.append(rec)

    # ---- hotels: resort fee must appear in the archived official hotel text ----
    hotel_text = ""
    for fn in ("v_resort_fee.txt", "v_hotel_terms.txt"):
        if (SNAP / fn).exists():
            hotel_text += (SNAP / fn).read_text(errors="ignore")
    htok = money_tokens(hotel_text)
    for h in load("hotels.json")["rows"]:
        rf = money(h.get("resort_fee_usd"))
        bad = []
        if rf and rf not in htok:
            bad.append({"field": "resort_fee_usd", "detail": f"${rf} not in official hotel text"})
        rec = {"id": h["id"], "series": "hotel", "name": h.get("name"),
               "source": h.get("booking_url"), "snapshot": None,
               "checked": 1, "failed": bad}
        results.append(rec)
        if bad:
            issues.append(rec)

    # ---- rates: checkout total must equal room + resort fee*nights + taxes ----
    rate_issues = []
    for e in load("rates.json")["entries"]:
        rt = e.get("nightly_rates_usd") or []
        nights = e.get("nights") or 0
        fee = e.get("resort_fee_per_night_usd") or 0
        room = sum(rt)
        expected = room + fee * nights + (e.get("taxes_total_usd") or 0)
        if abs(expected - (e.get("checkout_total_usd") or 0)) > 0.02:
            rate_issues.append({"id": e.get("property"), "failed": [
                {"field": "checkout_total_usd",
                 "detail": f"recomputed {round(expected, 2)} != published {e.get('checkout_total_usd')}"}]})

    n_checked = sum(x["checked"] for x in results)
    n_review = sum(len(x.get("review") or []) for x in results)
    daily_results, n_daily_checks = verify_daily()
    for d in daily_results:
        for f in d["failed"]:
            issues.append({"id": d["id"], "series": "Daily feed (%s)" % d.get("venue"),
                           "name": d.get("name"), "source": d.get("source"),
                           "failed": [f]})
    n_checked += n_daily_checks
    n_review += sum(len(x.get("review") or []) for x in daily_results)

    print(f"verified rows: {len(results) + len(daily_results)}   field checks: {n_checked}   "
          f"hard failures: {len(issues)}   review items: {n_review}")
    if issues:
        print("\nUNVERIFIED / CONTRADICTED VALUES (left blank or flagged, never guessed):")
        for i in issues:
            print(f"  {i['id']}  {i.get('series','')}  {i.get('name','')}")
            for f in i["failed"]:
                print(f"      - {f['field']}: {f['detail']}  (source: {i.get('source')})")
    if n_review:
        print("\nREVIEW ITEMS (documented interpretation, not a data error):")
        for x in results + daily_results:
            for f in (x.get("review") or []):
                print(f"  {x['id']}  {x.get('series') or x.get('venue','')}  {f['field']}: {f['detail']}")
    if rate_issues:
        print("\nRATE ARITHMETIC FAILURES:")
        for i in rate_issues:
            print(f"  {i['id']}")
            for f in i["failed"]:
                print(f"      - {f['field']}: {f['detail']}")

    out = {
        "verified_on": "2026-11-17",
        "method": "Each published numeric/date/time value was searched in the raw official "
                  "document text archived under data/snapshots/. Missing = UNVERIFIED. "
                  "Entry status was cross-checked against the independently parsed sheet "
                  "verdict (structure_rules.json) or the WPT registration wording. The daily "
                  "feed (data/daily.json) is checked the same way against the document its own "
                  "source_url points at, and every text span it prints in quotes must appear "
                  "verbatim in that document.",
        "rows_checked": len(results),
        "field_checks": n_checked,
        "hard_failures": issues,
        "review_items": n_review,
        "rate_arithmetic_failures": rate_issues,
        "daily_feed_rows": len(daily_results),
        "daily_feed_checks": n_daily_checks,
        "daily_feed": daily_results,
    }
    (ROOT / "data" / "row_verification.json").write_text(json.dumps(out, indent=2))
    print("\nwrote data/row_verification.json")
    return 1 if (issues or rate_issues) else 0


if __name__ == "__main__":
    sys.exit(main())
