#!/usr/bin/env python3
"""Test that a rule quotation follows its own archived source, not another URL."""
import copy
import unittest
from quote_provenance import audit_rule_quotes

URL = "https://example.test/structure.pdf"
SCHEDULE = "https://example.test/schedule.pdf"


def row():
    return {"id": "r1", "sources": [{"url": URL}, {"url": SCHEDULE}],
            "rules": {"fee": {"source": {"url": URL},
                              "excerpt": 'Clause 6: "$225 of the $2,200 Buy-In is withheld."'}}}


class QuoteProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.row = row()
        self.archives = {URL: "$225 of the $2,200\nBuy-In is withheld.", SCHEDULE: "COMING SOON"}

    def test_line_wrapping_does_not_break_a_verbatim_quote(self):
        self.assertEqual([], audit_rule_quotes([self.row], self.archives))

    def test_wrong_link_does_not_borrow_quote_from_another_archive(self):
        self.row["rules"]["fee"]["source"]["url"] = SCHEDULE
        result = audit_rule_quotes([self.row], self.archives)
        self.assertEqual(1, len(result))
        self.assertIn("not found", result[0]["reason"])

    def test_changed_numbers_or_punctuation_are_not_verbatim(self):
        self.row["rules"]["fee"]["excerpt"] = '"$225 of the $2200 Buy-In is withheld."'
        self.assertTrue(audit_rule_quotes([self.row], self.archives))

    def test_missing_archive_and_unlinked_url_are_review_items(self):
        self.row["rules"]["fee"]["source"]["url"] = "https://example.test/unknown"
        self.assertEqual(2, len(audit_rule_quotes([self.row], self.archives)))

    def test_commentary_without_quotes_is_not_treated_as_a_quote(self):
        self.row["rules"]["fee"]["excerpt"] = "The fee is unverified."
        self.assertEqual([], audit_rule_quotes([self.row], self.archives))

    def test_input_is_not_mutated(self):
        original = copy.deepcopy(self.row)
        audit_rule_quotes([self.row], self.archives)
        self.assertEqual(original, self.row)


if __name__ == "__main__":
    unittest.main(verbosity=2)
