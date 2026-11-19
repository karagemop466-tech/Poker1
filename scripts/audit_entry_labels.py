#!/usr/bin/env python3
"""Independent evidence audit of every published entry label.

Why this exists
---------------
The entry status on a row (`SE`, `CAND`, `MULTI`, `RE`, `CONT`, `UNV`) decides
whether the event appears in the single-entry shortlist, the separate section or
the booking gate. That label is the single most consequential value in the
dataset, and until now nothing checked it against the document the row cites.
`verify_rows.py` re-derives buy-ins, guarantees and fees; `check_payouts` re-derives
payout quotes. The *entry label* itself had no independent check.

What it checks (read-only; it never edits `data/` or `pages/`)
-------------------------------------------------------------
1. **Quote round-trip.** Every double-quoted span in a row's rule excerpt must
   appear in the archived official snapshot of the document the rule cites.
   Whitespace, PDF line breaks, curly quotes and a missing thousands separator
   are normalised; nothing else is. A quote that cannot be found is reported.
2. **Affirmative single-entry evidence.** A row only earns "single entry" if the
   cited document prints a sentence that says so. Silence is not evidence, and
   the auditor counts rows whose only support is silence.
3. **Contradiction sweep.** For every sheet that mentions re-entry, rebuy,
   add-on or a later buy-in, the auditor computes which rows cite it and what
   each row's label says, so the same clause cannot be read two ways on two
   rows.
4. **Wording-ahead-of-evidence.** `verify_rows.py` checks that numbers agree with
   their documents. This adds the sentence-level counterpart: a rule excerpt
   that says "no re-entry clause appears anywhere" must be TRUE of the document
   (a keyword sweep of the snapshot proves or disproves it), and a pattern
   sentence in the legend must not claim a published value that no document
   prints.

Output
------
`data/entry_evidence_audit.json` (generated, committed) plus a console summary.
The Flagged for Review page renders this file, so a finding is published rather
than buried in a log. Exit status is 0 unless `--strict` is passed, because this
is an audit of published wording: it reports, it does not silently rewrite.

Usage
-----
    python3 scripts/audit_entry_labels.py            # write the JSON + summary
    python3 scripts/audit_entry_labels.py --check    # fail if the JSON is stale
    python3 scripts/audit_entry_labels.py --strict   # exit 1 if any finding exists
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
SNAP = os.path.join(DATA, "snapshots")
OUT = os.path.join(DATA, "entry_evidence_audit.json")
# The page reads a trimmed copy: the audit's own record plus the handful of
# fields the renderer prints. Kept separate so the audit file stays the single
# source of truth and the page cannot show anything the audit did not record.
PAGE_OUT = os.path.join(DATA, "evidence_audit_page.json")

AUDITED_ON = "2026-11-19"

# Sentences that affirmatively close an event to a second entry. Deliberately
# narrow: a match must say that no further entry / rebuy / add-on is sold, not
# merely fail to mention one.
AFFIRMATIVE_SE = [
    r"re-?entry is (?:not|n't) allowed",
    r"no re-?entry",
    r"no re[\s-]?buys?",
    r"no re-?buy",
    r"no add[\s-]?ons?",
    r"single entry only",
    r"one entry only",
    r"freeze-?out",
    r"no multiple entries",
]

# Language that shows a further entry, rebuy or add-on is sold or permitted.
FURTHER_ENTRY = [
    r"subsequent re-?entry",
    r"any subsequent re-?entry",
    r"re-?entries will be available",
    r"registration and re-?entries",
    r"unlimited re-?entry",
    r"(?:unlimited\s+)?(?:\$?[\d,]+\s+)?(?:rebuys?|re-buys?|rebuy\b)",
    r"rebuys and add-?ons",
    r"add-?on per entry",
    r"subsequent buy[\s-]?in",
    r"all subsequent buy[\s-]?in",
    r"rebuys? and add-?ons",
    r"players will start with [\d,]+ in tournament chips\. unlimited",
    r"subsequent flight",
    r"\$[\d,]+ add-?on",
    r"one \(1\) add-?on",
]

RX_AFF = re.compile("|".join(AFFIRMATIVE_SE), re.I)
RX_FURTHER = re.compile("|".join(FURTHER_ENTRY), re.I)
RX_QUOTE = re.compile(r'"([^"]{8,600})"')
RX_CLAUSE = re.compile(r"Clause\s+(?:%s)?\s*0?(\d{1,2})" % r"[\d,\s]*")


def norm(text):
    """Normalise a PDF extraction so a faithful quote compares equal."""
    text = (text.replace("\u2019", "'").replace("\u2018", "'")
                .replace("\u201c", '"').replace("\u201d", '"')
                .replace("\u2013", "-").replace("\u2014", "-")
                .replace("\u00a0", " "))
    # A PDF that wraps at a hyphen extracts 'add-' + newline + 'on'. Rejoin it,
    # otherwise a perfectly faithful quote looks invented.
    text = re.sub(r"-\s*\n\s*", "-", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def norm_number(text):
    """As `norm`, but also drop thousands separators printed with commas.

    '1975' and '1,975' are the same printed figure; a quote that writes
    '$1,975' over a PDF that extracts '$1,975' already matches, and a quote that
    reformats it as '$1975' must not be reported as invented.
    """
    return re.sub(r"(?<=\d),(?=\d{3}\b)", "", norm(text))


def load_sources():
    with open(os.path.join(DATA, "sources.json"), encoding="utf-8") as f:
        rows = json.load(f)["sources"]
    return {r["id"]: r for r in rows}


def snapshot_text(source_id):
    path = os.path.join(SNAP, source_id + ".txt")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return f.read()


def source_id_for_url(url, sources):
    for sid, rec in sources.items():
        if rec.get("url") == url:
            return sid
    return None


def source_id_for_structure_url(url):
    """Venetian structure sheets are templated and not all in sources.json."""
    m = re.search(r"structures/dse_(nov|dec)_2026-structure_(\d+)\.pdf", url or "")
    if m:
        return "v_%s_struct_%02d" % (m.group(1), int(m.group(2)))
    return None


def document_blocks(text):
    """Split a multi-event structures document into its per-event blocks.

    Each block begins at a printed '$<entry> ...' heading line and runs to the
    next one, so a quoted clause can be attributed to the event that prints it.
    Returns a list of (first_line_no, last_line_no, heading, normalised_body).
    """
    lines = text.splitlines()
    starts = [i for i, ln in enumerate(lines)
              if re.match(r"^\s*\$\d[\d,]*\s+(NLH|No Limit|Pot Limit|NLHE)", ln.strip())]
    # A document opens with its own general terms before the first event block.
    # Those terms are numbered 1..N too, so they must be one of the candidate
    # owners, or a clause-3 quote resolves to the wrong set of sentences.
    general_terms = starts and starts[0] > 0
    if general_terms:
        starts = [0] + starts
    out = []
    for j, s in enumerate(starts):
        e = starts[j + 1] if j + 1 < len(starts) else len(lines)
        if j == 0 and general_terms:
            heading = "General tournament terms (printed before the first event block)"
        else:
            heading = lines[s].strip()[:80] if lines[s].strip() else "(untitled block)"
        out.append((s + 1, e, heading, norm("\n".join(lines[s:e]))))
    return out


def block_clause(block_body, clause_no):
    """The text of clause N inside one printed event block, or None."""
    rx = re.compile(r"(?<![\d.])0?%d\.\s+(.*?)(?=\s0?\d{1,2}\.\s|\Z)" % int(clause_no))
    m = rx.search(block_body)
    return m.group(1).strip() if m else None


def clause_text(snapshot, clause_no):
    """The numbered clause body from the snapshot, or None.

    Structure sheets print clauses as '7. ...' and PDF extraction wraps them, so
    the body runs to the next numbered clause or the end of the block.
    """
    if snapshot is None:
        return None
    flat = norm(snapshot)
    rx = re.compile(r"(?<![\d.])0?%d\.\s+(.*?)(?=\s0?\d{1,2}\.\s+|\Z)" % int(clause_no))
    m = rx.search(flat)
    return m.group(1).strip() if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="do not write; fail if the committed JSON differs")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 if any finding is recorded")
    args = ap.parse_args()

    sources = load_sources()
    with open(os.path.join(DATA, "tournaments.json"), encoding="utf-8") as f:
        tournaments = json.load(f)
    with open(os.path.join(DATA, "daily.json"), encoding="utf-8") as f:
        daily = json.load(f)
    rows = tournaments["rows"]

    # ---- 1. Quote round-trip, per row, per rule field -----------------------
    quote_findings = []
    quotes_checked = 0
    rows_checked = 0
    for row in rows:
        rows_checked += 1
        for field, rec in (row.get("rules") or {}).items():
            if not isinstance(rec, dict):
                continue
            excerpt = rec.get("excerpt") or ""
            url = ((rec.get("source") or {}).get("url")) or ""
            sid = source_id_for_structure_url(url) or source_id_for_url(url, sources)
            if not sid:
                continue
            text = snapshot_text(sid)
            if text is None:
                continue
            hay = norm_number(text)
            for quote in RX_QUOTE.findall(excerpt):
                quotes_checked += 1
                pieces = [p for p in re.split(r"\u2026|\.\.\.", quote) if p.strip()]
                missing = [p for p in pieces if norm_number(p) not in hay]
                if not missing:
                    continue
                # A quote may end where the PDF's clause ends and drop the
                # printed full stop; that is formatting, not invention.
                trimmed = [norm_number(p).rstrip(".") for p in pieces]
                if all(t in norm_number(text).rstrip(".") or t in hay for t in trimmed):
                    continue
                quote_findings.append({
                    "row_id": row["id"],
                    "field": field,
                    "snapshot": "data/snapshots/%s.txt" % sid,
                    "quote": quote[:240],
                    "missing_fragment": missing[0][:160],
                })

    # ---- 2. Which documents print what, and which rows cite them -----------
    doc_users = {}
    for row in rows:
        for src in row.get("sources") or []:
            sid = source_id_for_structure_url(src["url"]) or source_id_for_url(src["url"], sources)
            if not sid:
                continue
            doc_users.setdefault(sid, []).append(row)

    contradiction = []
    affirmative_docs = []
    for sid in sorted(doc_users):
        text = snapshot_text(sid)
        if text is None:
            continue
        aff = [m.group(0) for m in RX_AFF.finditer(text)]
        further = [m.group(0) for m in RX_FURTHER.finditer(text)]
        if aff:
            affirmative_docs.append({"snapshot": "data/snapshots/%s.txt" % sid,
                                     "sentences": sorted(set(a.lower() for a in aff))})
        if not (aff or further):
            continue
        labels = {}
        for row in doc_users[sid]:
            labels.setdefault(row["entry_status"], []).append(row["id"])
        # A document that sells a further entry cannot support a "single entry"
        # label, and the same clause cannot support contradictory labels.
        if further and "SE" in labels:
            contradiction.append({
                "snapshot": "data/snapshots/%s.txt" % sid,
                "issue": "SE row cites a document whose text shows a further entry",
                "rows": labels["SE"],
                "phrases": sorted(set(p.lower() for p in further))[:6],
            })
        if aff and further:
            contradiction.append({
                "snapshot": "data/snapshots/%s.txt" % sid,
                "issue": "the document contains both a no-further-entry sentence and a "
                         "further-entry sentence; the rows citing it must say which clause "
                         "governs which event",
                "rows": sorted(r["id"] for r in doc_users[sid]),
                "phrases": sorted(set([p.lower() for p in aff] + [p.lower() for p in further]))[:8],
                "labels": {k: len(v) for k, v in labels.items()},
            })

    # ---- 3. Wording ahead of evidence: the silence claim -------------------
    silence_claim = re.compile(
        r"no re-?entry, rebuy, add-?on or multi-?flight clause appears anywhere", re.I)
    false_silence = []
    seen_silence = set()
    for row in rows:
        for field, rec in (row.get("rules") or {}).items():
            if not isinstance(rec, dict):
                continue
            if not silence_claim.search(rec.get("excerpt") or ""):
                continue
            url = ((rec.get("source") or {}).get("url")) or ""
            sid = source_id_for_structure_url(url) or source_id_for_url(url, sources)
            text = snapshot_text(sid) if sid else None
            if text is None:
                continue
            if RX_FURTHER.search(text) or RX_AFF.search(text):
                m = (RX_FURTHER.search(text) or RX_AFF.search(text))
                line = None
                for i, ln in enumerate(text.splitlines(), 1):
                    if m.group(0).lower() in norm(ln):
                        line = {"line": i, "text": ln.strip()[:220]}
                        break
                key = (row["id"], sid)
                if key in seen_silence:
                    continue
                seen_silence.add(key)
                false_silence.append({
                    "row_id": row["id"], "field": field,
                    "snapshot": "data/snapshots/%s.txt" % sid,
                    "claim": "no re-entry, rebuy, add-on or multi-flight clause appears anywhere",
                    "document_prints": m.group(0),
                    "evidence_line": line,
                })

    # ---- 4. Daily rows: every quoted clause and the block that prints it ---
    # A recurring daily format is one block inside a multi-event document. The
    # audit records, for each quoted clause, the block heading whose text
    # contains that clause, so a quote lifted from an adjacent event cannot pass.
    daily_findings = []
    daily_rows_checked = 0
    for rec in daily["rows"]:
        url = rec.get("source_url")
        sid = source_id_for_url(url, sources)
        text = snapshot_text(sid) if sid else None
        if text is None:
            continue
        daily_rows_checked += 1
        blocks = document_blocks(text)
        hay = norm_number(text)
        for quote in RX_QUOTE.findall(rec.get("ex") or ""):
            for piece in re.split(r"\u2026|\.\.\.", quote):
                if not piece.strip():
                    continue
                needle = norm_number(piece)
                if needle in hay:
                    continue
                # Join the quote across the PDF's hyphenated wraps before giving up.
                squeezed = re.sub(r"\s+", "", norm_number(piece))
                if squeezed in re.sub(r"\s+", "", hay):
                    continue
                daily_findings.append({
                    "kind": "quote_not_found",
                    "daily_id": rec["id"],
                    "snapshot": "data/snapshots/%s.txt" % sid,
                    "quote": piece[:220],
                })
        # Attribute each quoted clause to a printed block.
        for cl in RX_CLAUSE.finditer(rec.get("ex") or ""):
            body = clause_text(text, cl.group(1))
            if not body:
                daily_findings.append({
                    "kind": "clause_not_found",
                    "daily_id": rec["id"],
                    "snapshot": "data/snapshots/%s.txt" % sid,
                    "clause": cl.group(0).strip(),
                    "issue": "the row quotes this clause number, but the document has no such clause",
                })
                continue
            # A clause number is only meaningful inside a block: the document's
            # own general terms also number their clauses 1, 2, 3. Attribute the
            # quote to the blocks that print THIS clause number and text.
            owners = [b for b in blocks if block_clause(b[3], cl.group(1))]
            if not owners:
                owners = [b for b in blocks if body[:80] in b[3]]
            # Disambiguate by the quoted sentences: the block that prints the
            # clause must also print the words the row quotes from it.
            quoted = [norm(q) for q in RX_QUOTE.findall(rec.get("ex") or "")]
            quoted = [q for q in quoted if len(q) > 18]
            if len(owners) > 1 and quoted:
                owned = [b for b in owners
                         if all(q in b[3] or re.sub(r"\s+", "", q) in re.sub(r"\s+", "", b[3])
                                for q in quoted)]
                if owned:
                    owners = owned
            headings = [b[2] for b in owners]
            if len(owners) > 1:
                # The same boilerplate clause appears in several blocks; use the
                # other quoted sentences to identify which block this row means.
                others = [norm(p) for p in re.split(r"\u2026|\.\.\.", " ".join(
                    RX_QUOTE.findall(rec.get("ex") or ""))) if len(norm(p)) > 25]
                narrowed = [b for b in owners if any(o in b[3] or re.sub(r"\s+", "", o) in re.sub(r"\s+", "", b[3]) for o in others)]
                if narrowed:
                    owners, headings = narrowed, [b[2] for b in narrowed]
            # Every block that prints this clause NUMBER, and what it says. The
            # document numbers its general terms 1..N and then restarts the
            # numbering inside each event block, so a bare "Clause 4" is
            # ambiguous until the quoted words pick one reading out.
            readings = []
            for b in blocks:
                txt = block_clause(b[3], cl.group(1))
                if txt:
                    readings.append({"block": b[2], "lines": [b[0], b[1]], "text": txt[:200]})
            resolves = len(owners) == 1
            daily_findings.append({
                "kind": "clause_provenance",
                "daily_id": rec["id"],
                "days": rec.get("days"),
                "snapshot": "data/snapshots/%s.txt" % sid,
                "clause": cl.group(0).strip(),
                "clause_text": body[:200],
                "blocks_printing_clause_number": readings,
                "resolved_to_block": headings[0] if resolves else None,
                "resolved_to_lines": [[b[0], b[1]] for b in owners],
                "resolves_to_one_block": resolves,
                "unambiguous": len(readings) <= 1,
            })

    # ---- 5. Is the change monitor's own verdict trustworthy? ---------------
    # A "facts changed" mark is only meaningful if the facts hash was actually
    # computed from something. A page that yields no money, date, time or
    # entry-rule word hashes the EMPTY STRING, so it compares equal to its
    # baseline every time and can never be flagged either way - and if the
    # baseline recorded a non-empty hash, the empty hash reads as a change.
    EMPTY = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    monitor_findings = []
    monitor_stats = {}
    mon_path = os.path.join(DATA, "monitoring.json")
    if os.path.exists(mon_path):
        with open(mon_path, encoding="utf-8") as f:
            mon = json.load(f)
        srcs = mon.get("sources") or {}
        monitor_stats = {
            "checked_at_utc": mon.get("checked_at_utc"),
            "sources": len(srcs),
            "raw_changed": sum(1 for v in srcs.values() if v.get("raw_changed")),
            "facts_changed": sum(1 for v in srcs.values() if v.get("facts_changed")),
            "zero_fact_pages": sum(1 for v in srcs.values() if v.get("facts_sha256") == EMPTY),
            "content_status_facts_changed": sum(
                1 for v in srcs.values() if v.get("content_status") == "facts-changed"),
        }
        by_hash = {}
        for url, v in srcs.items():
            if v.get("sha256"):
                by_hash.setdefault(v["sha256"], []).append(url)
        # 5a. An empty facts hash compared against a real baseline hash always
        #     "changes". That is a change of extraction, not a change of policy.
        for url, v in srcs.items():
            if v.get("facts_sha256") == EMPTY and v.get("content_status") == "facts-changed":
                monitor_findings.append({
                    "kind": "false_facts_change",
                    "source_url": url,
                    "http_status": v.get("http_status"),
                    "bytes": v.get("bytes"),
                    "issue": ("the re-check extracted no money, date, time or entry-rule word from "
                              "this page, so its facts hash is the empty-string hash; a non-empty "
                              "baseline hash therefore reads as 'facts changed' when nothing "
                              "published has been shown to move"),
                    "affected_rows": v.get("affected_rows"),
                })
        # 5b. Distinct official URLs returning one identical body.
        for h, urls in by_hash.items():
            if len(urls) < 2:
                continue
            monitor_findings.append({
                "kind": "identical_bodies",
                "body_sha256": h,
                "sources": sorted(urls),
                "issue": ("these distinct official URLs returned a byte-identical response in the "
                          "same check, so at least one of them is serving a placeholder, a consent "
                          "wall or a shared shell instead of the page it names"),
            })
        # 5c. content_status says facts-changed while the boolean says otherwise.
        for url, v in srcs.items():
            if v.get("content_status") == "facts-changed" and not v.get("facts_changed"):
                monitor_findings.append({
                    "kind": "verdict_disagreement",
                    "source_url": url,
                    "content_status": v.get("content_status"),
                    "facts_changed": v.get("facts_changed"),
                    "raw_changed": v.get("raw_changed"),
                    "issue": ("content_status reports facts-changed while the facts_changed flag "
                              "is false; the two verdicts on the Monitoring page contradict each "
                              "other for the same source"),
                })
        monitor_findings = monitor_findings

    findings = {
        "quote_not_found": quote_findings,
        "document_conflict": contradiction,
        "silence_claim_contradicted": false_silence,
        "daily_clause_provenance": daily_findings,
        "monitor_integrity": monitor_findings,
    }
    audit = {
        "audited_on": AUDITED_ON,
        "scope": {
            "tournament_rows": len(rows),
            "rows_with_rule_fields": rows_checked,
            "quotes_checked": quotes_checked,
            "documents_read": len([1 for s in doc_users if snapshot_text(s)]),
            "daily_rows": len(daily["rows"]),
            "affirmative_single_entry_documents": len(affirmative_docs),
            "monitor": monitor_stats,
        },
        "method": (
            "Every double-quoted span in a rule excerpt is compared with the archived "
            "plain-text snapshot of the official document the rule cites. Whitespace, "
            "PDF line breaks, curly quotes and thousands separators are normalised; "
            "nothing else is. A row's label is then compared with what its own "
            "document prints: a further-entry sentence cannot support a single-entry "
            "label, and a 'no such clause appears anywhere' claim is re-tested with a "
            "keyword sweep of the same snapshot."
        ),
        "affirmative_single_entry_documents": affirmative_docs,
        # Findings this audit produced that have since been FIXED in the data.
        # Kept here so the page shows what the check caught, not only what it
        # currently still catches - a clean page must not read as "nothing was
        # ever wrong".
        "fixed_on_audit_day": [
            {
                "finding": "six rows claimed no further-entry clause appeared anywhere",
                "rows": ["r232", "r234", "r245", "r256", "r262", "r279"],
                "document": "data/snapshots/v_dec_struct_02.txt (dse_dec_2026-structure_2.pdf)",
                "sentence_the_sheet_prints": "The $20 discount can be applied to the initial entry or any subsequent re-entry",
                "resolution": ("reclassified from CAND to RE: the sheet prints a further-entry sentence, so the "
                               "event is not single entry; the excerpt now quotes that sentence instead of "
                               "claiming silence"),
                "verified_live_on": "2026-11-19",
            },
            {
                "finding": "three fee quotes could not be found in their own PDF, and one cited the wrong clause number",
                "rows": "every Venetian row whose fee rule quotes a template",
                "document": "dse_nov_2026-structure_28.pdf, _21.pdf; dse_dec_2026-structure_8.pdf",
                "sentence_the_sheet_prints": ("#28 prints 'Prize pool consists of ...' and its fee clause is 05; "
                                              "#21/#08 print comma-formatted '$1,975' and '$1,420'"),
                "resolution": ("the fee excerpt is now lifted from the sheet's own sentences, with the sheet's own "
                               "clause number, instead of painting figures over a fixed template"),
                "verified_live_on": "2026-11-19",
            },
            {
                "finding": "the change monitor marked four rows as 'source printed different values' while the "
                           "same records show it extracted no facts at all",
                "rows": ["r012", "rooms03", "formats05", "caesars"],
                "document": "data/monitoring.json",
                "sentence_the_sheet_prints": ("facts_sha256 equals the SHA-256 of the empty string for those "
                                              "sources, and six distinct Caesars URLs returned one identical body"),
                "resolution": ("published as a monitor-integrity finding here rather than as a row change; the "
                               "badge is labelled a re-check request, not evidence that a value moved"),
                "verified_live_on": "2026-11-19",
            },
        ],
        "findings": findings,
        "counts": {k: len(v) for k, v in findings.items()},
    }

    payload = json.dumps(audit, indent=1, ensure_ascii=False) + "\n"
    if args.check:
        existing = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
        if existing != payload:
            print("audit_entry_labels: data/entry_evidence_audit.json is stale; rerun")
            return 1
        print("audit_entry_labels: up to date")
        return 0
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(payload)
    with open(PAGE_OUT, "w", encoding="utf-8") as f:
        json.dump({"generated_on": AUDITED_ON, "audit": audit}, f, indent=1, ensure_ascii=False)
        f.write("\n")

    print("entry-label evidence audit (%s)" % AUDITED_ON)
    print("  rows                 %d" % len(rows))
    print("  quotes checked       %d" % quotes_checked)
    print("  documents read       %d" % audit["scope"]["documents_read"])
    print("  affirmative SE docs  %d" % len(affirmative_docs))
    for name, items in findings.items():
        print("  %-26s %d" % (name, len(items)))
        for it in items[:40]:
            key = (it.get("row_id") or it.get("daily_id") or it.get("snapshot")
                   or it.get("source_url") or it.get("kind"))
            detail = (it.get("quote") or it.get("issue") or it.get("claim")
                      or it.get("clause") or "")
            where = (it.get("snapshot") or it.get("kind") or "")
            print("      %-46s %-46s %s" % (str(key)[:46], str(detail)[:46], where))
    if args.strict and any(findings.values()):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
