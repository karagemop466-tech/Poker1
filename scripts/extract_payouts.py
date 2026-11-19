#!/usr/bin/env python3
"""Extract payout clauses from the official-document snapshots already on file.

Reads the archived text extractions in ``data/snapshots/`` (fetched from the
operators' own PDFs and pages by the scheduled GitHub Actions monitors) and
writes ``data/payouts.json`` with one record per official document:

    id / kind / snapshot / source_url / clauses[]

Each clause stores the snapshot line range it was taken from and the text
quoted from those lines.  Nothing is inferred: a clause is either a verbatim
span of the official document or it is not written.  A document whose text
matches no pattern records an empty ``clauses`` list, which the site renders
as "the sheet prints no payout rule", never as a guessed value.

Every clause is re-derived from its own line range before the file is
written, and ``scripts/check_links.py`` performs the same check on every
build, so a clause that does not appear in its snapshot fails the build.

Documents covered
    * 52 Venetian DeepStack structure sheets (v_nov_struct_*, v_dec_struct_*)
    * 69 blocks of the Wynn WPT World Championship structures/terms PDF
    * 3 Bellagio weekly structure flyers (b_fri_pdf, b_sat_pdf, b_sun_pdf)
    * the Caesars Palace daily tournament flyer (c_daily_flyer)

Usage:
    python3 scripts/extract_payouts.py
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAP = os.path.join(ROOT, "data", "snapshots")
OUT = os.path.join(ROOT, "data", "payouts.json")

# --- clause kinds -----------------------------------------------------------
# Composition kinds say where the money goes; every other kind states a payout
# rule (who gets paid, how many, or in what form).
COMPOSITION_KINDS = {"prize-pool-composition", "guarantee-composition"}

# Sentence rules: PREFIX + CORE + smart trailing period.  The trailing piece
# ends the quote at the first period that is not part of a number, or right
# before the next numbered rule (" 8. Ante ...") when the printed sentence
# has no period of its own, so "12.5" can never terminate a clause, a quote
# can never run into the following rule, and never more than 300 characters
# past its own sentence.
TRAILING = r".{0,300}?(?:(?<!\d)\.(?!\d)|(?= \d+\. ))"

SENTENCE_RULES = [
    # Placement rule: "This event pays 12.5% of the field."
    ("percent-of-field",
     r"[^.]{0,100}\bpay[s]? \d+(?:\.\d+)?% of the field"),
    # Venetian NYE header: Day 1 payouts start at 12.5%, 5% of each flight
    # advances to Day 2 (a full header line, no sentence period).
    ("day-1-payout",
     r"Day 1 Payouts Start at 12\.5% with 5% From Each Flight Advancing to Day 2",
     "line"),
    # Multi-flight rules: who is "in the money" and when a flight stops.
    ("in-the-money",
     r"[^.]{0,120}(?:being )?considered in the money"),
    ("in-the-money",
     r"[^.]{0,60}down to approximately \d+(?:\.\d+)?% of the field remaining"),
    ("in-the-money",
     r"[^.]{0,120}approximately 12\.5% of each Day 1 Field being in the money"),
    ("in-the-money",
     r"[^.]{0,60}Each Flight would play until the money \(12\.5%?\)\. "
     r"Must bag chips to make Day 2 and be in the money"),
    # Prizes paid as seats (satellites) and the seat-count conclusion rule.
    ("seat-prize",
     r"[^.]{0,60}All tournament prizes are direct entry"),
    ("seat-prize",
     r"[^.]{0,60}Winners will be awarded direct entry to Event"),
    ("seat-prize",
     r"The tournament will conclude when the number of players remaining"),
    # Milestone: the seat is awarded mid-event.
    ("milestone-seat",
     r"[^.]{0,140}will instantly receive direct entry"),
    # How much of each buy-in reaches the prize pool.
    ("prize-pool-composition",
     r"[^.]{0,80}prize pool consists of \$[\d,]+ of every \$[\d,]+"),
    ("prize-pool-composition",
     r"[^.]{0,60}The \$[\d,]+ Buy-In is allocated as follows"),
    ("prize-pool-composition",
     r"[^.]{0,60}Of the \$[\d,]+ [Bb]uy[- ]?[Ii]n"),
    ("prize-pool-composition",
     r"[^.]{0,60}Of the \$[\d,]+ add-on"),
    # What the guarantee actually covers (cash vs bounties).
    ("guarantee-composition",
     r"[^.]{0,60}A Prize Pool of \$[\d,]+ is guaranteed by"),
    ("guarantee-composition",
     r"[^.]{0,40}A total prize pool of \$[\d,]+ is guaranteed"),
    ("guarantee-composition",
     r"Guarantee: \$[\d,]+ \(prize pool \+ total bounties\)",
     "line"),
    ("guarantee-composition",
     r"[^.]{0,40}Bellagio guarantees that the total Combined Prize Pool"),
    # Bounty prize mechanics.
    ("bounty-rule",
     r"Players receive \$[\d,]+ [Bb]ounty for each player they eliminate"),
    ("bounty-rule",
     r"If the bounty cannot be divided equally into whole dollars"),
    ("bounty-payout",
     r"Once we reach the money \(posted payouts\)"),
    ("bounty-payout",
     r"[^.]{0,60}they will receive ½ of the other players bounty"),
    # Bellagio Sunday: the flyer's own payout-structure sentence.
    ("payout-structure",
     r"[^.]{0,40}Payout structure based on"),
]

# WPT structures PDF: sections whose heading itself names the payout subject.
# Captured raw (newlines preserved) between the heading line and the next
# section heading, or the end of the block.
WPT_SECTION_HEADINGS = {
    "Payouts": "payout-section",
    "Mystery Payouts": "mystery-payout-section",
    "Bounty Rules": "bounty-rules-section",
    "Progressive Bounty Rules": "bounty-rules-section",
    "Mystery Bounty Rules": "bounty-rules-section",
    "prizes": "prize-table",
}
WPT_BLOCK_SPLIT = r"(?m)^\s*TERMS AND CONDITIONS\s*$"
WPT_HEADING_RE = re.compile(r"^[ \t]*([A-Za-z][A-Za-z0-9 &/()-]*):[ \t]*$")

# Caesars Palace flyer: the printed payout matrix (places x field size).
CAESARS_TABLE_START = "Places"
CAESARS_TABLE_END = "Tournament Rules"


def read_lines(rel):
    path = os.path.join(ROOT, rel)
    with open(path, encoding="utf-8") as stream:
        return stream.read().split("\n")


def normalise(text):
    return re.sub(r"\s+", " ", text).strip()


def build_norm_map(lines):
    """Return (norm_text, line_of) where line_of[i] is the source line of
    norm_text[i].  Whitespace runs collapse to single spaces, exactly like
    normalise(), but every kept character remembers its line."""
    norm_chars = []
    line_of = []
    for lineno, raw in enumerate(lines, 1):
        for token in re.split(r"(\s+)", raw):
            if not token:
                continue
            if token.isspace():
                if norm_chars and norm_chars[-1] != " ":
                    norm_chars.append(" ")
                    line_of.append(lineno)
            else:
                for ch in token:
                    norm_chars.append(ch)
                    line_of.append(lineno)
        if norm_chars and norm_chars[-1] != " ":
            norm_chars.append(" ")
            line_of.append(lineno)
    return "".join(norm_chars), line_of


def compiled_sentence_rules():
    rules = []
    for entry in SENTENCE_RULES:
        kind, core = entry[0], entry[1]
        mode = entry[2] if len(entry) > 2 else "sentence"
        if mode == "sentence":
            rules.append((kind, re.compile(core + TRAILING), "sentence"))
        else:
            rules.append((kind, re.compile(core), "line"))
    return rules


def find_matches(norm, rules):
    found = []
    for kind, pattern, mode in rules:
        for m in pattern.finditer(norm):
            found.append([kind, m.start(), m.end(), mode])
    # Keep the earliest, longest span when patterns overlap the same sentence.
    found.sort(key=lambda item: (item[1], -(item[2] - item[1])))
    kept = []
    for item in found:
        if any(item[1] < k[2] and k[1] < item[2] for k in kept):
            continue
        kept.append(item)
    kept.sort(key=lambda item: item[1])
    return kept


def clauses_from_patterns(lines):
    norm, line_of = build_norm_map(lines)
    rules = compiled_sentence_rules()
    clauses = []
    for kind, start, end, mode in find_matches(norm, rules):
        if mode == "line":
            # Standalone header phrase: quote the rest of its source line,
            # never the sentence after it.
            begin = start
            last_line = line_of[end - 1]
            finish = end
            while finish < len(norm) and line_of[finish] == last_line:
                finish += 1
        else:
            # Extend to the sentence boundary.  The +1 keeps a ". " that
            # starts immediately before the match (the match begins on the
            # space after the period) inside the search window; without it
            # the quote reaches back past the previous sentence.
            back = norm.rfind(". ", max(0, start - 200), start + 1)
            begin = start if back == -1 else back + 2
            finish = end
        text_full = norm[begin:finish]
        lead = len(text_full) - len(text_full.lstrip())
        text = text_full.strip()
        begin += lead
        finish = begin + len(text)
        start_line = line_of[begin]
        end_line = line_of[finish - 1]
        # The quoted text must appear verbatim in the source lines.
        source = normalise("\n".join(lines[start_line - 1:end_line]))
        if text not in source:
            raise SystemExit(
                "clause does not round-trip in lines %d-%d: %r" %
                (start_line, end_line, text[:120]))
        clauses.append({
            "kind": kind,
            "line": start_line,
            "line_count": end_line - start_line + 1,
            "text": text,
        })
    return clauses


def clauses_from_wpt_sections(lines, start_index, end_index):
    """Capture every payout-named section of one WPT structure block, raw.

    ``start_index``/``end_index`` are 0-based slice bounds of the block inside
    ``lines`` (the text between two TERMS AND CONDITIONS banners; the banner
    line itself is excluded).
    """
    heading_indexes = [
        i for i in range(start_index, end_index)
        if WPT_HEADING_RE.match(lines[i])
    ]
    clauses = []
    for pos, heading_index in enumerate(heading_indexes):
        heading_text = WPT_HEADING_RE.match(lines[heading_index]).group(1)
        if heading_text not in WPT_SECTION_HEADINGS:
            continue
        body_start = heading_index + 1
        body_end = (heading_indexes[pos + 1]
                    if pos + 1 < len(heading_indexes) else end_index)
        body = lines[body_start:body_end]
        leading = 0
        while leading < len(body) and not body[leading].strip():
            leading += 1
        trailing = 0
        while trailing < len(body) - leading and not body[len(body) - 1 - trailing].strip():
            trailing += 1
        kept = body[leading:len(body) - trailing]
        if not kept:
            continue
        start_line = body_start + leading + 1  # 1-based
        clauses.append({
            "kind": WPT_SECTION_HEADINGS[heading_text],
            "heading": heading_text,
            "line": start_line,
            "line_count": len(kept),
            "text": "\n".join(kept),
            "raw": True,
        })
    return clauses


def extract_wpt_blocks():
    rel = "data/snapshots/wpt_struct.txt"
    lines = read_lines(rel)
    text = "\n".join(lines)
    starts = [m.start() for m in re.finditer(WPT_BLOCK_SPLIT, text)]
    if len(starts) != 69:
        raise SystemExit("expected 69 WPT structure blocks, found %d" % len(starts))
    records = []
    for number, start in enumerate(starts, 1):
        end = starts[number] if number < len(starts) else len(text)
        start_index = text[:start].count("\n")
        # For the last block take every remaining line; otherwise stop just
        # before the next TERMS AND CONDITIONS banner line.
        end_index = len(lines) if number == len(starts) else text[:end].count("\n")
        clauses = clauses_from_wpt_sections(lines, start_index, end_index)
        records.append({
            "id": "wpt-block-%02d" % number,
            "kind": "wynn-wpt-structure-block",
            "block": number,
            "snapshot": rel,
            "source_url": WPT_STRUCT_URL,
            "clauses": clauses,
        })
    return records


def extract_caesars_table(lines):
    """The flyer prints one payout matrix: Places header .. Tournament Rules."""
    start = None
    end = None
    for i, line in enumerate(lines):
        if start is None and line.strip() == CAESARS_TABLE_START:
            start = i
        elif start is not None and line.strip().startswith(CAESARS_TABLE_END):
            end = i
            break
    if start is None or end is None:
        raise SystemExit("Caesars payout matrix not found in c_daily_flyer")
    while end > start and not lines[end - 1].strip():
        end -= 1
    raw = "\n".join(lines[start:end])
    if not raw.split("\n")[0].strip() == CAESARS_TABLE_START:
        raise SystemExit("Caesars matrix header mismatch")
    heading_line = next(
        (i + 1 for i, line in enumerate(lines) if line.strip() == "Payouts"), 0)
    return {
        "kind": "prize-table",
        "heading": "Payouts",
        "line": start + 1,
        "line_count": end - start,
        "text": raw,
        "raw": True,
        "note": "The flyer's text extraction prints the heading \"Payouts\" "
                "after the table (line %d); the table itself starts at line "
                "%d." % (heading_line, start + 1),
    }


def source_url_by_id():
    with open(os.path.join(ROOT, "data", "sources.json"), encoding="utf-8") as stream:
        doc = json.load(stream)
    return {entry["id"]: entry["url"] for entry in doc["sources"]}


WPT_STRUCT_URL = None  # set in main() from sources.json


def main():
    global WPT_STRUCT_URL
    urls = source_url_by_id()
    WPT_STRUCT_URL = urls["wpt_struct"]
    documents = []

    # Venetian structure sheets.
    venetian = sorted(
        name for name in os.listdir(SNAP)
        if re.match(r"v_(nov|dec)_struct_\d+\.txt$", name))
    for name in venetian:
        doc_id = name[:-4]
        rel = "data/snapshots/" + name
        if doc_id not in urls:
            raise SystemExit("no official URL for %s in data/sources.json" % doc_id)
        lines = read_lines(rel)
        documents.append({
            "id": doc_id,
            "kind": "venetian-structure-sheet",
            "snapshot": rel,
            "source_url": urls[doc_id],
            "clauses": clauses_from_patterns(lines),
        })

    # Wynn WPT World Championship structures/terms PDF, block by block.
    documents.extend(extract_wpt_blocks())

    # Bellagio weekly flyers.
    for doc_id in ("b_fri_pdf", "b_sat_pdf", "b_sun_pdf"):
        rel = "data/snapshots/%s.txt" % doc_id
        lines = read_lines(rel)
        documents.append({
            "id": doc_id,
            "kind": "bellagio-structure-flyer",
            "snapshot": rel,
            "source_url": urls[doc_id],
            "clauses": clauses_from_patterns(lines),
        })

    # Caesars Palace daily flyer: sentences plus the printed payout matrix.
    rel = "data/snapshots/c_daily_flyer.txt"
    lines = read_lines(rel)
    clauses = clauses_from_patterns(lines)
    clauses.append(extract_caesars_table(lines))
    clauses.sort(key=lambda clause: clause["line"])
    documents.append({
        "id": "c_daily_flyer",
        "kind": "caesars-daily-flyer",
        "snapshot": rel,
        "source_url": urls["c_daily_flyer"],
        "clauses": clauses,
    })

    payload = {
        "note": "Payout clauses quoted verbatim from the official-document "
                "snapshots in data/snapshots/ by scripts/extract_payouts.py. "
                "Each clause stores the snapshot line range it came from; "
                "scripts/check_links.py re-derives every clause from those "
                "lines on each build and fails on a mismatch. An empty "
                "clauses list means the document was read and printed no "
                "clause matching the extraction patterns - it is never a "
                "guessed value.",
        "documents": documents,
    }
    with open(OUT, "w", encoding="utf-8") as stream:
        json.dump(payload, stream, indent=1, ensure_ascii=False)
        stream.write("\n")

    total = sum(len(doc["clauses"]) for doc in documents)
    by_kind = {}
    for doc in documents:
        for clause in doc["clauses"]:
            by_kind[clause["kind"]] = by_kind.get(clause["kind"], 0) + 1
    silent = [doc["id"] for doc in documents if not doc["clauses"]]
    print("wrote data/payouts.json: %d documents, %d clauses" %
          (len(documents), total))
    for kind in sorted(by_kind):
        print("  %-28s %d" % (kind, by_kind[kind]))
    print("documents with no clause: %d" % len(silent))
    for doc_id in silent:
        print("  -", doc_id)


if __name__ == "__main__":
    main()
