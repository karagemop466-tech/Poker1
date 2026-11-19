#!/usr/bin/env python3
"""Unit tests for the fail-closed single-entry evidence gate. No network needed."""
import copy
import json
import unittest
from pathlib import Path

from entry_evidence import load_archives, strict_single_entry_errors

URL = "https://www.venetianlasvegas.com/example.pdf"
DOC = """Event Numbers: 02, 12
This is a single-entry tournament.
No re-entry.
No rebuys.
No add-ons.
No paid competitive advantages.
"""


def evidence(text, value=None, url=URL):
    obj = {"excerpt": text, "source": {"url": url}, "retrieved_on": "2026-11-19"}
    if value is not None:
        obj["value"] = value
    return obj


def confirmed_fixture():
    return {
        "kind": "entry", "event_no": 12, "sources": [{"url": URL}],
        "event_scope": evidence("Event Numbers: 02, 12"),
        "rules": {
            "single_entry": evidence("single-entry tournament", "confirmed"),
            "re_entry": evidence("No re-entry", "prohibited"),
            "rebuy": evidence("No rebuys", "prohibited"),
            "add_on": evidence("No add-ons", "prohibited"),
            "spending_advantage": evidence("No paid competitive advantages", "prohibited"),
        },
    }


class EvidenceGateTests(unittest.TestCase):
    def setUp(self):
        self.row = confirmed_fixture()
        self.archives = {URL: DOC}

    def assert_rejected(self, msg=None):
        self.assertTrue(strict_single_entry_errors(self.row, self.archives), msg)

    def test_all_affirmative_excerpts_in_one_scoped_archive_pass(self):
        self.assertEqual([], strict_single_entry_errors(self.row, self.archives))

    def test_no_add_on_language_is_not_no_add_on_evidence(self):
        del self.row["rules"]["add_on"]
        self.assert_rejected()

    def test_all_five_distinct_rules_are_required(self):
        for key in self.row["rules"]:
            with self.subTest(key=key):
                row = copy.deepcopy(self.row)
                del row["rules"][key]
                self.assertTrue(strict_single_entry_errors(row, self.archives))

    def test_absence_unsupported_claim_and_fabricated_quote_fail(self):
        self.row["rules"]["add_on"]["excerpt"] = "No add-ons or rebuys are mentioned"
        self.assert_rejected()

    def test_registration_deadline_does_not_prove_an_event_wide_ban(self):
        text = "No re-entry after level 8"
        self.archives[URL] += text
        self.row["rules"]["re_entry"]["excerpt"] = text
        self.assert_rejected()

    def test_one_entry_per_flight_is_not_one_per_event(self):
        text = "One entry per flight"
        self.archives[URL] += text
        self.row["rules"]["single_entry"]["excerpt"] = text
        self.assert_rejected()

    def test_negated_freezeout_is_rejected(self):
        text = "This is not a single-entry tournament"
        self.archives[URL] += text
        self.row["rules"]["single_entry"]["excerpt"] = text
        self.assert_rejected()

    def test_exception_and_inconsistent_source_are_rejected(self):
        text = "No rebuys except during the first break"
        self.archives[URL] += text
        self.row["rules"]["rebuy"]["excerpt"] = text
        self.assert_rejected()
        self.row = confirmed_fixture()
        self.archives[URL] += "\nRe-entry is allowed."
        self.assert_rejected()

    def test_event_number_and_continuation_must_match(self):
        self.row["event_no"] = 29
        self.assert_rejected()
        self.row = confirmed_fixture()
        self.row["kind"] = "continuation"
        self.assert_rejected()

    def test_rule_and_scope_cannot_be_joined_from_unscoped_sources(self):
        other = "https://www.venetianlasvegas.com/different.pdf"
        self.archives[other] = DOC
        self.row["sources"].append({"url": other})
        self.row["rules"]["add_on"]["source"]["url"] = other
        self.assert_rejected()

    def test_unlinked_unofficial_and_unarchived_sources_are_rejected(self):
        del self.row["sources"][:]
        self.assert_rejected()
        self.row = confirmed_fixture()
        other = "https://example.com/fake.pdf"
        self.archives[other] = DOC
        self.row["sources"] = [{"url": other}]
        self.row["event_scope"]["source"]["url"] = other
        for obj in self.row["rules"].values():
            obj["source"]["url"] = other
        self.assert_rejected()
        self.row = confirmed_fixture()
        self.archives.clear()
        self.assert_rejected()

    def test_retrieval_date_and_source_quote_required(self):
        self.row["rules"]["re_entry"]["retrieved_on"] = "2026-02-30"
        self.assert_rejected()
        self.row = confirmed_fixture()
        self.row["event_scope"]["excerpt"] = "Event Number: 12 (never printed here)"
        self.assert_rejected()

    def test_scope_does_not_match_a_buy_in_or_date(self):
        for wrong_heading in ("Event #2 — $12 entry", "Event 2 on 12 January"):
            with self.subTest(heading=wrong_heading):
                self.archives[URL] += "\n" + wrong_heading
                self.row["event_scope"]["excerpt"] = wrong_heading
                self.assert_rejected()

    def test_scope_does_not_treat_next_numbered_rule_as_an_event(self):
        heading = "Event Numbers: 02, 12\n1. TDA rules apply"
        self.archives[URL] += "\n" + heading
        self.row["event_scope"]["excerpt"] = heading
        self.row["event_no"] = 1
        self.assert_rejected()

    def test_conflicting_clause_elsewhere_in_same_document_fails_closed(self):
        for contradiction in ("This is not a single-entry tournament.",
                              "No re-entry after level 8.",
                              "One entry per player per flight.",
                              "Players may re-enter.",
                              "Re-entry will be permitted.",
                              "Multiple entries are available.",
                              "An optional purchase provides additional chips."):
            with self.subTest(clause=contradiction):
                self.archives[URL] = DOC + "\n" + contradiction
                self.assert_rejected()

    def test_current_production_se_labels_must_pass(self):
        root = Path(__file__).resolve().parent.parent
        rows = json.loads((root / "data/tournaments.json").read_text())["rows"]
        archives = load_archives(root)
        for row in rows:
            if row.get("entry_status") == "SE":
                self.assertEqual([], strict_single_entry_errors(row, archives), row.get("id"))

    def test_actual_silent_venetian_sheet_is_not_a_confirmed_freezeout(self):
        root = Path(__file__).resolve().parent.parent
        rows = json.loads((root / "data/tournaments.json").read_text())["rows"]
        row = next(r for r in rows if r["id"] == "r096")
        self.assertTrue(strict_single_entry_errors(row, load_archives(root)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
