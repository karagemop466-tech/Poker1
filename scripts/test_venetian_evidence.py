#!/usr/bin/env python3
"""Verify source-specific chip, fee, payout and event-scope extraction."""
import json
import re
import unittest
from pathlib import Path
from venetian_evidence import extract_sheet, collapse

ROOT = Path(__file__).resolve().parent.parent
SNAP = ROOT / "data/snapshots"


class VenetianEvidenceTests(unittest.TestCase):
    def sheet(self, name, event_no, continuation=False):
        text = (SNAP / (name + ".txt")).read_text(encoding="utf-8")
        return extract_sheet(text, event_no, continuation=continuation), text

    def test_three_previously_wrong_stacks_are_40000(self):
        for sheet, no in (("v_nov_struct_04", 59), ("v_nov_struct_05", 12), ("v_nov_struct_07", 28)):
            with self.subTest(sheet=sheet):
                data, _ = self.sheet(sheet, no)
                self.assertEqual(40000, data["starting_chips"])
                self.assertEqual("Starting Chips: 40,000", data["starting_chips_excerpt"])

    def test_event29_fee_excerpt_includes_actual_discount_clause(self):
        data, text = self.sheet("v_dec_struct_02", 29)
        self.assertEqual("6", data["fee_clause"])
        self.assertEqual(40, data["house_fee_usd"])
        self.assertIn("For Event #29 only", data["fee_excerpt"])
        self.assertIn("$20 discount", data["fee_excerpt"])
        self.assertIn(data["fee_excerpt"], collapse(text))

    def test_fee_excerpt_uses_sheet_wording_not_a_template(self):
        data, text = self.sheet("v_nov_struct_28", 27)
        self.assertIn("Prize pool consists", data["fee_excerpt"])
        self.assertNotIn("The prize pool consists", data["fee_excerpt"])
        self.assertIn(data["fee_excerpt"], collapse(text))
        data, text = self.sheet("v_nov_struct_21", 47)
        self.assertIn("$1,975", data["fee_excerpt"])
        self.assertIn(data["fee_excerpt"], collapse(text))

    def test_rejects_a_sheet_for_a_different_event(self):
        with self.assertRaisesRegex(ValueError, "not listed"):
            self.sheet("v_dec_struct_02", 3)

    def test_restart_has_no_new_starting_stack(self):
        data, _ = self.sheet("v_dec_struct_08", 20, continuation=True)
        self.assertIsNone(data["starting_chips"])
        self.assertIsNone(data["starting_chips_excerpt"])

    def test_all_published_venetian_joins_and_entry_stacks(self):
        rows = json.loads((ROOT / "data/tournaments.json").read_text())["rows"]
        count = 0
        for row in rows:
            fee_url = ((row.get("rules") or {}).get("fee") or {}).get("source", {}).get("url", "")
            match = re.search(r"dse_(nov|dec)_2026-structure_(\d+)\.pdf", fee_url)
            if not match:
                continue
            name = "v_%s_struct_%02d" % (match.group(1), int(match.group(2)))
            data, _ = self.sheet(name, row["event_no"], continuation=row["kind"] == "continuation")
            if row["kind"] == "entry":
                self.assertEqual(data["starting_chips"], row.get("starting_chips"), row["id"])
            self.assertEqual(data["house_fee_usd"], row.get("house_fee_usd"), row["id"])
            count += 1
        self.assertGreater(count, 100)


if __name__ == "__main__":
    unittest.main(verbosity=2)
