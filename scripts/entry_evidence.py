#!/usr/bin/env python3
"""Conservative, independently testable gate for strict single-entry claims.

Silence is never evidence of a prohibition. Each qualifying row must cite an
archived official source that identifies the event and affirmatively specifies:
  * one entry per player for the whole event;
  * no re-entry, no rebuy, no add-on, and no purchasable playing advantage.

The narrow patterns intentionally fail closed. They are not a general-purpose
natural-language parser: a human must still read the complete source for scope,
conditions, exceptions and conflicting official documents before recommending
an event. This module can be integrated into a generator or validator after the
ongoing parallel-session handoff; currently it changes no generated data.
"""
import json
import re
import unicodedata
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
OFFICIAL_HOSTS = frozenset({
    "www.venetianlasvegas.com", "www.wynnlasvegas.com", "cdn.wynnresorts.com",
    "aria.mgmresorts.com", "bellagio.mgmresorts.com", "www.caesars.com",
    "www.mgmresorts.com", "mgmgrand.mgmresorts.com", "mandalaybay.mgmresorts.com",
    "orleans.boydgaming.com", "southpointcasino.com", "www.rwlasvegas.com",
    "www.westgateresorts.com",
})


def normalized(value):
    value = unicodedata.normalize("NFKC", str(value or "")).lower()
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def load_archives(root=ROOT):
    """Load only active manifest URLs with an archived, readable text snapshot."""
    manifest = json.loads((root / "data/sources.json").read_text(encoding="utf-8"))
    result = {}
    for src in manifest.get("sources", []):
        if src.get("active") is False or not src.get("url") or not src.get("id"):
            continue
        if not is_official_url(src["url"]):
            continue
        path = root / "data/snapshots" / (src["id"] + ".txt")
        if path.is_file():
            result[src["url"]] = path.read_text(encoding="utf-8", errors="replace")
    return result


def is_official_url(url):
    if not isinstance(url, str):
        return False
    parsed = urlparse(url)
    return parsed.scheme == "https" and (parsed.hostname or "").lower() in OFFICIAL_HOSTS


# Narrower than general natural-language interpretation. In particular, "one
# entry per flight" and "no re-entry after level 9" are not event-wide limits.
AFFIRMATIVE = {
    "single_entry": re.compile(
        r"\b(?:one|1)\s+(?:(?:\(\s*1\s*\)|\(\s*one\s*\))\s*)?entry\s+per\s+(?:player|person)\b"
        r"|\b(?:each\s+player|players?)\s+(?:may|can)\s+(?:enter|register)\s+(?:only\s+)?(?:once|one\s+time)\b"
        r"|\b(?:single[ -]entry|freeze[ -]?out)\s+(?:event|tournament|format)\b", re.I),
    "re_entry": re.compile(r"\b(?:no\s+re[ -]?entr(?:y|ies)|re[ -]?entr(?:y|ies)\s+(?:is|are)\s+(?:not\s+allowed|not\s+permitted|prohibited))\b", re.I),
    "rebuy": re.compile(r"\b(?:no\s+re[ -]?buys?|re[ -]?buys?\s+(?:are|is)\s+(?:not\s+allowed|not\s+permitted|prohibited))\b", re.I),
    "add_on": re.compile(r"\b(?:no\s+add[ -]?ons?|add[ -]?ons?\s+(?:are|is)\s+(?:not\s+allowed|not\s+permitted|prohibited))\b", re.I),
    "spending_advantage": re.compile(
        r"\b(?:no\s+(?:paid|purchasable|optional)\s+(?:playing|competitive|tournament)\s+advantages?"
        r"|(?:playing|competitive|tournament)\s+advantages?\s+(?:may\s+not|cannot|can\s+not)\s+be\s+(?:purchased|bought))\b", re.I),
}
QUALIFIERS = re.compile(
    r"\b(?:after|before|until|except|unless|subject\s+to|per\s+flight|each\s+flight|for\s+event\s*#?\s*\d+\s+only)\b", re.I)
NEGATION_OF_CLAIM = re.compile(
    r"\b(?:not|never|without)\s+(?:a\s+|an\s+|any\s+)?(?:no\s+|one\s+entry|single[ -]entry|freeze[ -]?out)\b"
    r"|\bno\s+(?:re[ -]?entr(?:y|ies)|re[ -]?buys?|add[ -]?ons?)\s+(?:is|are)\s+not\b", re.I)
CONTRADICTION = re.compile(
    r"\b(?:unlimited|permitted|allowed)\s+(?:re[ -]?entr(?:y|ies)|re[ -]?buys?|add[ -]?ons?)\b"
    r"|\b(?:re[ -]?entr(?:y|ies)|re[ -]?buys?|add[ -]?ons?)\s+(?:is|are)\s+(?:allowed|permitted)\b"
    r"|\bsubsequent\s+re[ -]?entr(?:y|ies)\b"
    r"|\bnot\s+(?:a\s+)?(?:single[ -]entry|freeze[ -]?out)\s+(?:event|tournament|format)\b"
    r"|\b(?:one|1)\s+entry\s+per\s+(?:player|person)\s+(?:per|each)\s+flight\b"
    r"|\bno\s+(?:re[ -]?entr(?:y|ies)|re[ -]?buys?|add[ -]?ons?)\s+(?:after|before|until|unless|except)\b"
    r"|\b(?:optional|voluntary)\s+.{0,100}\b(?:chips|stack)\b", re.I | re.S)


def scoped_event_numbers(quote):
    """Read event numbers, not unrelated dates or amounts later in a heading."""
    multiple = re.search(r"\bevent\s+numbers?\s*:\s*((?:(?:\d{1,3}|,|/|&|\band\b|\s)+))", quote, re.I)
    if multiple:
        return {int(n) for n in re.findall(r"\b\d{1,3}\b", multiple.group(1))}
    single = re.search(r"\bevent\s*(?:no\.?|#)?\s*(\d{1,3})\b", quote, re.I)
    return {int(single.group(1))} if single else set()


def strict_single_entry_errors(row, archives=None):
    """Return reasons a claimed SE row fails the evidence gate.

    `event_scope` and each of five rule objects have `excerpt`, `source.url`,
    and `retrieved_on`. Quotes must appear in a single archived operator source
    linked to the row. A same-source scope requirement intentionally refuses
    uncertain joins between documents. An empty list means only that this narrow
    machine check passed; human review is always required.
    """
    archives = load_archives() if archives is None else archives
    errors = []
    if row.get("kind") != "entry":
        errors.append("not an entry row")
    sources = {s.get("url") for s in row.get("sources", []) if isinstance(s, dict)}

    def excerpt_from_archive(field, obj):
        if not isinstance(obj, dict):
            errors.append(f"{field}: missing evidence object")
            return "", None
        src = obj.get("source") or {}
        url = src.get("url") if isinstance(src, dict) else None
        quote = obj.get("excerpt") or ""
        if not is_official_url(url) or url not in sources:
            errors.append(f"{field}: official evidence source is not linked on this row")
        if not isinstance(quote, str) or not normalized(quote):
            errors.append(f"{field}: missing verbatim quotation")
            return "", url
        if len(quote) > 500:
            errors.append(f"{field}: quotation exceeds the short-evidence limit")
        snapshot = archives.get(url)
        if not snapshot or normalized(quote) not in normalized(snapshot):
            errors.append(f"{field}: quotation not found in the archived official source")
        try:
            date.fromisoformat(obj.get("retrieved_on", ""))
        except (TypeError, ValueError):
            errors.append(f"{field}: missing or invalid retrieval date")
        return quote, url

    scope_quote, scope_url = excerpt_from_archive("event_scope", row.get("event_scope"))
    try:
        event_no = int(row.get("event_no"))
    except (ValueError, TypeError):
        event_no = None
    scope_numbers = scoped_event_numbers(scope_quote)
    if event_no is None or event_no not in scope_numbers:
        errors.append("event_scope: quotation does not identify this event number")
    rules = row.get("rules") or {}
    for field, pattern in AFFIRMATIVE.items():
        obj = rules.get(field)
        quote, url = excerpt_from_archive(field, obj)
        expected = "confirmed" if field == "single_entry" else "prohibited"
        if not isinstance(obj, dict) or obj.get("value") != expected:
            errors.append(f"{field}: expected value {expected!r}")
        if url != scope_url:
            errors.append(f"{field}: rule and event scope must come from the same archived source")
        if not pattern.search(quote):
            errors.append(f"{field}: no affirmative event-wide prohibition/limit")
        if QUALIFIERS.search(quote):
            errors.append(f"{field}: qualified clause needs event-specific manual review")
        if NEGATION_OF_CLAIM.search(quote):
            errors.append(f"{field}: quotation negates or reverses the claim")
    if scope_url in archives and CONTRADICTION.search(archives[scope_url]):
        errors.append("source contains a conflicting permission; human review required")
    return errors
