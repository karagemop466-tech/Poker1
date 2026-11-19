#!/usr/bin/env python3
"""Extract event-scoped facts and verbatim fee clauses from Venetian sheets.

These functions only read the supplied document. They do not decide that a
missing rule is a prohibition or that a blind table is a finish time. Joining a
sheet to an event must first confirm the event number printed in its heading.
"""
import re


def collapse(value):
    return " ".join(value.split())


def extract_sheet(text, event_no, *, continuation=False):
    headings = list(re.finditer(r"(?mi)^\s*Event Numbers?\s*:\s*([^\n]+)", text))
    try:
        event_no = int(event_no)
    except (TypeError, ValueError):
        raise ValueError("An event number is required to join this sheet") from None
    event_heading = next((h for h in headings if event_no in
                          {int(n) for n in re.findall(r"\b\d{1,3}\b", h.group(1))}), None)
    if not event_heading:
        raise ValueError("Event %s is not listed in the structure-sheet heading" % event_no)
    fee = re.search(r"(?m)^\s*(\d{1,2})\.\s*(\$[\d,]+\s+of\s+the\s+\$[\d,]+\s+Buy[- ]?In\b.*?)"
                    r"(?=\n\s*\d{1,2}\.\s|\Z)", text, re.I | re.S)
    if not fee:
        raise ValueError("No numbered fee clause found for event %s" % event_no)
    amounts = re.search(r"\$([\d,]+)\s+of\s+the\s+\$([\d,]+)\s+Buy[- ]?In", fee.group(2), re.I)
    stack = re.search(r"(?mi)^\s*Starting Chips\s*:\s*([\d,]+)", text)
    levels = re.findall(r"(?mi)^\s*Level Duration[^\n]*", text)
    payout = re.search(r"\bpays?\s+[\d.]+\s*%\s+of the field\b", text, re.I)
    return {
        "event_scope_excerpt": collapse(event_heading.group(0)),
        "fee_clause": fee.group(1),
        "fee_excerpt": collapse(fee.group(2)),
        "house_fee_usd": int(amounts.group(1).replace(",", "")),
        "buy_in_usd": int(amounts.group(2).replace(",", "")),
        "starting_chips": int(stack.group(1).replace(",", "")) if stack and not continuation else None,
        "starting_chips_excerpt": "Starting Chips: " + stack.group(1) if stack and not continuation else None,
        "level_duration_excerpt": "; ".join(collapse(line) for line in levels) or None,
        "payout_excerpt": collapse(payout.group(0)) if payout else None,
    }
