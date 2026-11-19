#!/usr/bin/env python3
"""Archived-sheet and synthetic tests for event-scoped entry language."""
import unittest
from pathlib import Path
from extract_rules import entry_evidence

SNAP = Path(__file__).resolve().parent.parent / "data/snapshots"


class ScopeTests(unittest.TestCase):
    def sheet(self, name):
        return entry_evidence((SNAP / (name + ".txt")).read_text(encoding="utf-8"))

    def test_omission_is_not_single_entry(self):
        evidence = self.sheet("v_nov_struct_16")
        self.assertEqual("NO_ENTRY_POLICY_FOUND", evidence["sheet_kind"])
        self.assertIsNone(evidence["re_entry_excerpt"])

    def test_december_sheet_two_scopes_reference_to_event_29(self):
        evidence = self.sheet("v_dec_struct_02")
        self.assertEqual("EVENT_SPECIFIC_RE_ENTRY", evidence["sheet_kind"])
        self.assertEqual([29], evidence["re_entry_event_scope"])
        self.assertEqual([], evidence["re_entry_flight_scope"])
        self.assertIn("For Event #29 only", evidence["re_entry_excerpt"])
        self.assertIn("subsequent re-entry", evidence["re_entry_excerpt"])

    def test_december_sheet_14_scope_is_30_flights_1b_and_1d(self):
        evidence = self.sheet("v_dec_struct_14")
        self.assertEqual("EVENT_SPECIFIC_RE_ENTRY", evidence["sheet_kind"])
        self.assertEqual([30], evidence["re_entry_event_scope"])
        self.assertEqual(["1B", "1D"], evidence["re_entry_flight_scope"])
        self.assertNotIn("1F", evidence["re_entry_flight_scope"])
        self.assertIn("For Event #30 Day 1B and 1D only", evidence["re_entry_excerpt"])

    def test_bagged_player_rule_is_only_a_flight_clue(self):
        evidence = self.sheet("v_nov_struct_04")
        self.assertEqual("MULTI_FLIGHT", evidence["sheet_kind"])
        self.assertIsNone(evidence["re_entry_excerpt"])

    def test_general_subsequent_buy_in_is_not_qualified(self):
        text = "Event Number: 1\n1. TDA rules apply.\n2. All subsequent buy ins after the initial buy in will be $200.\n3. Test.\n"
        evidence = entry_evidence(text)
        self.assertEqual("RE_ENTRY", evidence["sheet_kind"])
        self.assertEqual([], evidence["re_entry_event_scope"])

    def test_unrelated_only_clause_does_not_scope_a_different_rule(self):
        text = "1. For Event #29 only a discount applies.\n2. All subsequent buy ins after the initial buy in will be $200.\n"
        evidence = entry_evidence(text)
        self.assertEqual("RE_ENTRY", evidence["sheet_kind"])
        self.assertEqual([], evidence["re_entry_event_scope"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
