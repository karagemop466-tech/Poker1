#!/usr/bin/env python3
"""Derive, for every published row, whether the official document prints a way to
gain an advantage by spending more money.

Why this module exists
----------------------
The planning rule this dataset is built to serve separates events by whether a
player can buy an advantage - a rebuy, an add-on, or a second entry into the same
event - and puts those events in a separate section. The published `entry_status`
encodes that only implicitly: `RE` and `MULTI` both mean "a further entry exists"
without saying which kind, `CAND` means the sheet was read and prints no clause
either way, and `UNV` means no sheet was read at all. A reader comparing two rows
could not tell "the sheet prices later buy-ins" from "the sheet only restricts
bagging chips into another flight", although the trip consequence differs.

This module makes that reading explicit **without adding a single fact**: every
value is derived from the clause excerpt already stored on the row, and the derived
record keeps a verbatim pointer back to that excerpt, its source and the date it was
retrieved. Nothing here promotes or demotes an `entry_status`: it never says an
event is single entry, and it is not an operator statement. Where the official
document is silent, the derived value says the document is silent.

The rule is purely mechanical (see ``classify``); ``scripts/check_links.py`` re-derives
it for every row on each build and fails if a value, its excerpt, its source or its
retrieval date disagree with what is stored on the row, so the column cannot drift
away from the evidence it quotes.
"""

#: Rule fields, in the order the classifier looks for a printed clause in them.
FIELDS = ("add_on", "re_entry", "single_entry")

#: The derived values, in the order they are listed in the documentation.
VALUES = (
    "further-entry-priced",       # a later buy-in is priced on the sheet
    "rebuy-or-reentry-printed",   # further entries are sold during the event
    "later-flight-printed",       # a further starting flight is permitted (or restricted)
    "no-further-entry-clause",    # the sheet was read and prints no such clause
    "no-structure-sheet",         # no official document for this event was read
    "continuation",               # a Day 2 / final-table row: no entry is sold
)

#: How each value answers "can a player buy an advantage here?".
#:   "yes"       - the official document prints a paid route to more entries or chips
#:   "not-printed" - the document was read in full and prints no such route (silence,
#:                   which is *not* a confirmation that none exists)
#:   "unknown"   - no document for this event was read
#:   "none"      - no entry is sold on this row at all
ADVANTAGE = {
    "further-entry-priced": "yes",
    "rebuy-or-reentry-printed": "yes",
    "later-flight-printed": "yes",
    "no-further-entry-clause": "not-printed",
    "no-structure-sheet": "unknown",
    "continuation": "none",
}

#: One-line chip text per value, as the tables print it.
LABEL = {
    "further-entry-priced": "Later buy-in priced on the sheet",
    "rebuy-or-reentry-printed": "Further entries sold during the event",
    "later-flight-printed": "Another flight entry allowed unless chips bagged",
    "no-further-entry-clause": "No further-entry or add-on clause printed",
    "no-structure-sheet": "No structure sheet on file",
    "continuation": "No entry sold on this row",
}

#: The sentence printed under the chip. Each one names what the document does, never
#: what the operator intends.
READING = {
    "further-entry-priced": "The official structure sheet puts a price on a buy-in after the "
                            "first one, so paying more buys another chance in this event.",
    "rebuy-or-reentry-printed": "The official structure sheet sells further entries during the "
                                "event (re-entry or rebuy terms are printed), so paying more buys "
                                "another chance in this event.",
    "later-flight-printed": "The official structure sheet addresses a further starting flight - "
                            "it bars only a player who bagged chips for Day 2 - so a player who "
                            "busts out can buy back in at another flight.",
    "no-further-entry-clause": "Every numbered clause of the official structure sheet was read "
                               "and none of them prices a later buy-in, a rebuy or an add-on. "
                               "This is silence in the document, not a written one-entry rule.",
    "no-structure-sheet": "No official structure document exists for this event yet, so the "
                          "sheet cannot be read for a further-entry clause.",
    "continuation": "This row is a Day 2 or final-table restart; the official document sells no "
                    "entry on it, so the question does not apply. The parent event's rows carry "
                    "the reading.",
}


def _clause_key(row, field):
    """Return (value, excerpt, source, retrieved_on) for one rule field, or None."""
    rules = row.get("rules") or {}
    ent = rules.get(field)
    if not isinstance(ent, dict):
        return None
    return (ent.get("value"), ent.get("excerpt"), ent.get("source") or {}, ent.get("retrieved_on"))


def _prices_later_buyin(text):
    """True when a stored excerpt puts a price on a buy-in after the first one."""
    if not text:
        return False
    low = text.lower().replace("\u2019", "'")
    return "subsequent buy in" in low or "subsequent buy-in" in low


def classify(row):
    """Derive the spend-advantage record for one published row.

    Pure function of what is already stored on the row: ``kind``, the four rule
    fields and their values/excerpts. Returns ``None`` only for a row with no rule
    fields at all, which the build never produces (and the validator rejects).
    """
    if row.get("kind") == "continuation":
        value = "continuation"
        prefer = ("single_entry", "re_entry", "add_on")
    else:
        add = _clause_key(row, "add_on")
        reent = _clause_key(row, "re_entry")
        single = _clause_key(row, "single_entry")
        excerpts = [x[1] for x in (add, reent, single) if x and x[1]]
        if any(_prices_later_buyin(x) for x in excerpts):
            value = "further-entry-priced"
        elif reent and reent[0] == "allowed":
            value = "rebuy-or-reentry-printed"
        elif reent and reent[0] == "possible for later flights":
            value = "later-flight-printed"
        elif any(x and x[0] in ("unknown", None) for x in (reent, single)):
            # A missing rule field means no official document was read for this row.
            value = "no-structure-sheet"
        elif reent and reent[0] == "not mentioned":
            value = "no-further-entry-clause"
        else:
            value = "no-structure-sheet"
        # Prefer the field whose own value drove the decision, so the printed excerpt
        # is the clause the value was read out of.
        prefer = {
            "further-entry-priced": ("re_entry", "single_entry", "add_on"),
            "rebuy-or-reentry-printed": ("re_entry",),
            "later-flight-printed": ("re_entry",),
            "no-further-entry-clause": ("re_entry", "add_on", "single_entry"),
            "no-structure-sheet": ("single_entry", "re_entry", "add_on"),
        }[value]

    basis_field, got = None, None
    for f in prefer + FIELDS:
        got = _clause_key(row, f)
        if got and got[1]:
            basis_field = f
            break
    if not got or not got[1]:
        return None
    ent_value, excerpt, source, retrieved = got
    return {
        "value": value,
        "advantage": ADVANTAGE[value],
        "label": LABEL[value],
        "reading": READING[value],
        "basis": "rules.%s" % basis_field,
        "excerpt": excerpt,
        "excerpt_rule_value": ent_value,
        "source": {"label": source.get("label"), "url": source.get("url")} if source else {},
        "retrieved_on": retrieved,
        "note": ("Derived from the clause text stored on this row. It is not an operator "
                 "statement and it does not confirm or deny a one-entry policy."),
    }


def summary(rows):
    """Counts per derived value, for the pages that print a breakdown."""
    out = {v: 0 for v in VALUES}
    for r in rows:
        sa = r.get("spend_advantage") or {}
        v = sa.get("value")
        if v in out:
            out[v] += 1
    return out


if __name__ == "__main__":  # pragma: no cover - manual inspection helper
    import json
    import os

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data = json.load(open(os.path.join(root, "data", "tournaments.json"), encoding="utf-8"))
    for v, n in sorted(summary(data["rows"]).items(), key=lambda x: -x[1]):
        print("%-28s %4d" % (v, n))
