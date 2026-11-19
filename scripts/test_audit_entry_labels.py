#!/usr/bin/env python3
"""Regression tests for the entry-label evidence audit.

The audit is only useful if its own normalisation and reading rules cannot be
loosened without a test failing. Each test pins one rule:

* a faithful quote is found across PDF line breaks, hyphenated wraps, curly
  quotes and a reformatted thousands separator, and an invented one is not;
* a document that prints a further-entry sentence cannot support a single-entry
  label;
* an explicit "no such clause appears anywhere" claim is contradicted when the
  same snapshot prints one;
* a clause number resolves to the block whose text contains the quoted words,
  not to whichever block happens to be numbered first;
* the published audit file is current, so a data change cannot ship with a stale
  evidence page.
"""
import json
import os
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import audit_entry_labels as audit  # noqa: E402


class NormalisationTests(unittest.TestCase):
    def test_faithful_quote_survives_pdf_formatting(self):
        pdf = "Re-entry is NOT\nallowed. The prize pool consists of $1,975 of\nevery $2,200 Buy In."
        self.assertIn(audit.norm_number("The prize pool consists of $1975 of every $2,200 Buy In."),
                      audit.norm_number(pdf))
        self.assertIn(audit.norm_number("Re-entry is NOT allowed"),
                      audit.norm_number(pdf))

    def test_hyphenated_wrap_is_joined(self):
        self.assertIn("one (1) $100 add-on", audit.norm("one (1) $100 add-\non"))

    def test_invented_number_is_not_found(self):
        self.assertNotIn(audit.norm_number("$2,400 Buy In"), audit.norm_number("$2,200 Buy In"))


class LabelRuleTests(unittest.TestCase):
    def test_further_entry_phrase_is_recognised(self):
        for text in (
            "The $20 discount can be applied to the initial entry or any subsequent re-entry",
            "All subsequent buy in's after the initial buy in will be $200.",
            "Unlimited re-entry for each starting flight will be available until the start of level 9.",
            "One (1) $100 add-on for 15,000 tournament chips is available any time.",
            "Re-entry is NOT allowed. All rebuys must be done immediately",
        ):
            self.assertTrue(audit.RX_FURTHER.search(text), text)

    def test_affirmative_single_entry_phrase_is_recognised_but_silence_is_not(self):
        for text in ("Re-entry is NOT allowed.", "No rebuys and no add-ons.",
                     "This event is single entry only.", "Freezeout format."):
            self.assertTrue(audit.RX_AFF.search(text), text)
        # Silence must never read as confirmation.
        for text in ("Players will start with 25,000 chips.",
                     "Late registration closes at 4:55 PM."):
            self.assertFalse(audit.RX_AFF.search(text), text)

    def test_every_published_single_entry_row_has_an_affirmative_document(self):
        """The strict claim the site makes: SE requires affirmative evidence."""
        with open(os.path.join(ROOT, "data", "tournaments.json"), encoding="utf-8") as f:
            rows = json.load(f)["rows"]
        se = [r for r in rows if r["entry_status"] == "SE"]
        for row in se:
            text = ""
            for field in ("single_entry", "re_entry"):
                rec = (row.get("rules") or {}).get(field) or {}
                text += " " + (rec.get("excerpt") or "")
            self.assertTrue(audit.RX_AFF.search(text),
                            "%s is labelled SE without an affirmative sentence: %r"
                            % (row["id"], text[:160]))


class ClauseAttributionTests(unittest.TestCase):
    def test_block_split_includes_the_general_terms(self):
        text = ("Wynn Daily Poker Tournaments\nGeneral Terms and Conditions\n\n"
                "1. One.\n3. Registration opens four (4) hours prior.\n\n"
                "$200 NLH\nMonday-Thursday\n\n1. This event is one day.\n"
                "3. Re-entries are available until level 9.\n")
        blocks = audit.document_blocks(text)
        self.assertEqual(2, len(blocks))
        self.assertIn("General tournament terms", blocks[0][2])
        self.assertIn("$200 NLH", blocks[1][2])
        self.assertIsNotNone(audit.block_clause(blocks[1][3], "3"))
        self.assertIn("re-entries", audit.block_clause(blocks[1][3], "3"))


class PublishedAuditTests(unittest.TestCase):
    def audit_path(self):
        return os.path.join(ROOT, "data", "entry_evidence_audit.json")

    def test_published_audit_is_current(self):
        result = subprocess.run(
            [sys.executable, os.path.join(ROOT, "scripts", "audit_entry_labels.py"), "--check"],
            cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(0, result.returncode,
                         "data/entry_evidence_audit.json is stale - rerun the auditor:\n"
                         + result.stdout + result.stderr)

    def test_page_copy_matches_the_audit(self):
        audit_file = self.audit_path()
        if not os.path.exists(audit_file):
            self.skipTest("audit not generated yet")
        with open(audit_file, encoding="utf-8") as f:
            published = json.load(f)
        page_file = os.path.join(ROOT, "data", "evidence_audit_page.json")
        self.assertTrue(os.path.exists(page_file), "the page copy is missing")
        with open(page_file, encoding="utf-8") as f:
            page = json.load(f)
        self.assertEqual(published, page["audit"],
                         "data/evidence_audit_page.json is not the published audit - rerun the auditor")

    def test_no_finding_is_silently_dropped(self):
        """Every finding category the renderer knows about must exist in the file."""
        with open(self.audit_path(), encoding="utf-8") as f:
            published = json.load(f)
        for key in ("quote_not_found", "document_conflict", "silence_claim_contradicted",
                    "daily_clause_provenance", "monitor_integrity"):
            self.assertIn(key, published["findings"], key)


if __name__ == "__main__":
    unittest.main()
