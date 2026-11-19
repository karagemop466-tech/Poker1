#!/usr/bin/env python3
"""Map every published row to the official document its payout rule comes from.

Shared by ``scripts/build_site.py`` (which renders pages/payouts.html) and
``scripts/check_links.py`` (which re-derives the same mapping on every build
and fails if the published page disagrees), so the page and the validator can
never drift apart.

Nothing here guesses a value.  A row either resolves to an archived official
document through its own printed source link (a structure-sheet URL, a
"block N" label, a unique structure-title match, or an exact document URL),
or it records why it does not:

    structure-sheet   Venetian row whose sources print the sheet URL
    block-label       Wynn row whose sources name the structure block
    matched           Wynn row matched to a block by the structure matcher
    title-label       Wynn row whose sources print the sheet title; used only
                      when exactly one block carries that normalised title
    document-url      daily row whose document_url/source_url is archived
    caesars-flyer     Caesars daily row; the archived flyer is the room's
                      own daily document (its printed URL matches)
    placeholder       Wynn structures PDF on file is a COMING SOON stub
    title-ambiguous   two blocks share the printed title; not guessed
    title-unmatched   no block carries the printed title; not guessed
    none              no structure source on the row at all

Statuses published on the page (and asserted by the validator):

    published          the document prints at least one payout rule clause
    composition-only   the document only says where the money goes
    sheet-silent       the document was read and printed no payout clause
    sheet-placeholder  the official structures PDF is a placeholder stub
    sheet-unmapped     a structure document exists but is not mapped to row
    no-sheet           the row carries no structure source
    no-snapshot        the row's official source has no archived capture
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Composition says where the money goes; every other kind states a payout rule.
COMPOSITION_KINDS = frozenset({"prize-pool-composition", "guarantee-composition"})

CLAUSE_KINDS = frozenset({
    "percent-of-field", "day-1-payout", "in-the-money", "seat-prize",
    "milestone-seat", "prize-pool-composition", "guarantee-composition",
    "bounty-rule", "bounty-payout", "payout-structure",
    "payout-section", "mystery-payout-section", "bounty-rules-section",
    "prize-table",
})

DOCUMENT_KINDS = frozenset({
    "venetian-structure-sheet", "wynn-wpt-structure-block",
    "bellagio-structure-flyer", "caesars-daily-flyer",
})

STATUSES = frozenset({
    "published", "composition-only", "sheet-silent", "sheet-placeholder",
    "sheet-unmapped", "no-sheet", "no-snapshot",
})

# Chip class per status; the classes exist in assets/style.css.
CHIP_CLASS = {
    "published": "ok",
    "composition-only": "info",
    "sheet-silent": "warn",
    "sheet-placeholder": "warn",
    "sheet-unmapped": "warn",
    "no-sheet": "warn",
    "no-snapshot": "warn",
}

STATUS_TEXT = {
    "published": "Payout rule published",
    "composition-only": "Composition only",
    "sheet-silent": "Sheet prints no payout rule",
    "sheet-placeholder": "Structures PDF is a placeholder",
    "sheet-unmapped": "Structure sheet not mapped to this row",
    "no-sheet": "No structure sheet on file",
    "no-snapshot": "Source not captured for payout extraction",
}

VENETIAN_SHEET_RE = re.compile(
    r"dse_(nov|dec)_2026-structure[_-](\d+)\.pdf", re.IGNORECASE)
WPT_BLOCK_RE = re.compile(r"\bblock (\d+)\b", re.IGNORECASE)
WPT_TITLE_RE = re.compile(r"Official structures PDF \((.*)\)\s*$")


def normalise(text):
    return re.sub(r"\s+", " ", text).strip()


def normalise_title(text):
    """Fold the title variants the schedule PDF and structure PDF print
    differently (apostrophe style, GTD vs Guaranteed) so an exact-title
    comparison can be made without inventing a match."""
    text = text.lower()
    text = text.replace("\u2019", "'").replace("\u2013", "-").replace("\u2014", "-")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\bgtd\b", "guarantee", text)
    text = re.sub(r"\bguaranteed\b", "guarantee", text)
    text = re.sub(r"[^a-z0-9$,. ]", "", text)
    return text.strip()


def load_bundle(root=None):
    """Read every file the mapping needs; one bundle keeps the two callers
    reading identical inputs."""
    root = root or ROOT
    with open(os.path.join(root, "data", "payouts.json"), encoding="utf-8") as stream:
        payouts = json.load(stream)
    with open(os.path.join(root, "data", "wpt_row_sheets.json"), encoding="utf-8") as stream:
        matched = json.load(stream)["matched"]
    with open(os.path.join(root, "data", "wpt_struct_blocks.json"), encoding="utf-8") as stream:
        blocks = json.load(stream)
    docs_by_id = {doc["id"]: doc for doc in payouts["documents"]}
    docs_by_url = {}
    for doc in payouts["documents"]:
        docs_by_url.setdefault(doc["source_url"], doc)
    titles = {block["block"]: normalise_title(block["title"]) for block in blocks}
    return {
        "payouts": payouts,
        "docs": payouts["documents"],
        "docs_by_id": docs_by_id,
        "docs_by_url": docs_by_url,
        "matched": matched,
        "block_titles": titles,
    }


def venetian_doc_id(url):
    match = VENETIAN_SHEET_RE.search(url or "")
    if not match:
        return None
    return "v_%s_struct_%02d" % (match.group(1).lower(), int(match.group(2)))


def resolve_tournament_row(row, bundle):
    """Return {'how': ..., 'doc_id': ...} for one tournament row."""
    sources = row.get("sources") or []
    labels = [str(source.get("label", "")) for source in sources]
    urls = [str(source.get("url", "")) for source in sources]

    if row.get("venue") == "The Venetian Resort":
        for url in urls:
            doc_id = venetian_doc_id(url)
            if doc_id and doc_id in bundle["docs_by_id"]:
                return {"how": "structure-sheet", "doc_id": doc_id}
        return {"how": "none", "doc_id": None}

    if row.get("venue") != "Wynn Las Vegas":
        return {"how": "none", "doc_id": None}

    if any("COMING SOON" in label for label in labels):
        return {"how": "placeholder", "doc_id": None}

    matched = bundle["matched"].get(row.get("id"))
    if matched and "wpt-block-%02d" % matched["block"] in bundle["docs_by_id"]:
        return {"how": "matched",
                "doc_id": "wpt-block-%02d" % matched["block"]}

    for label in labels:
        match = WPT_BLOCK_RE.search(label)
        if match:
            doc_id = "wpt-block-%02d" % int(match.group(1))
            if doc_id in bundle["docs_by_id"]:
                return {"how": "block-label", "doc_id": doc_id}

    for label in labels:
        match = WPT_TITLE_RE.search(label)
        if not match:
            continue
        wanted = normalise_title(match.group(1))
        hits = sorted(block for block, title in bundle["block_titles"].items()
                      if wanted and wanted in title)
        if len(hits) == 1:
            doc_id = "wpt-block-%02d" % hits[0]
            if doc_id in bundle["docs_by_id"]:
                return {"how": "title-label", "doc_id": doc_id}
        return {"how": "title-ambiguous" if len(hits) > 1 else "title-unmatched",
                "doc_id": None}

    return {"how": "none", "doc_id": None}


def resolve_daily_row(row, bundle):
    """Return {'how': ..., 'doc_id': ...} for one daily-format row.

    Exact URL equality only: the archived capture must be the very document
    the row cites (document_url, else source_url).  The Caesars flyer is the
    exception by identity, not by guess - its printed URL is the row's own
    source URL."""
    for key in ("document_url", "source_url", "source"):
        url = row.get(key)
        if not url:
            continue
        doc = bundle["docs_by_url"].get(url)
        if doc:
            return {"how": "document-url", "doc_id": doc["id"]}
    return {"how": "none", "doc_id": None}


def classify_document(doc):
    """Split a document's clauses into payout rules and composition."""
    if not doc:
        return [], []
    rules = []
    composition = []
    for clause in doc.get("clauses") or []:
        if clause.get("kind") in COMPOSITION_KINDS:
            composition.append(clause)
        else:
            rules.append(clause)
    return rules, composition


def classify_tournament_row(row, bundle):
    resolved = resolve_tournament_row(row, bundle)
    return _status_for(resolved, bundle, none_status="no-sheet")


def classify_daily_row(row, bundle):
    # A daily row without an archived capture of its own source is
    # "no-snapshot": the document exists, it simply was not captured for
    # payout extraction.  Only a tournament row lacking a structure source
    # entirely is "no-sheet".
    resolved = resolve_daily_row(row, bundle)
    return _status_for(resolved, bundle, none_status="no-snapshot")


def _status_for(resolved, bundle, none_status):
    how = resolved["how"]
    doc_id = resolved["doc_id"]
    if how == "placeholder":
        status = "sheet-placeholder"
    elif how in ("title-ambiguous", "title-unmatched"):
        status = "sheet-unmapped"
    elif how == "none":
        status = none_status
    else:
        doc = bundle["docs_by_id"][doc_id]
        rules, composition = classify_document(doc)
        if rules:
            status = "published"
        elif composition:
            status = "composition-only"
        else:
            status = "sheet-silent"
    doc = bundle["docs_by_id"].get(doc_id) if doc_id else None
    rules, composition = classify_document(doc)
    return {
        "status": status,
        "how": how,
        "doc": doc,
        "doc_id": doc_id,
        "rules": rules,
        "composition": composition,
    }
