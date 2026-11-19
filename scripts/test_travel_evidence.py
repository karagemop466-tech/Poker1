#!/usr/bin/env python3
"""Tri-state walk-threshold tests; no network or generated-file changes."""
import unittest
from travel_evidence import within_walk_limit, walk_evidence_errors


class TravelEvidenceTests(unittest.TestCase):
    def test_untimed_internal_walk_is_unknown(self):
        self.assertIsNone(within_walk_limit(None))
        self.assertEqual([], walk_evidence_errors({"status": "internal", "minutes": None, "within_30_min": None}))
        self.assertTrue(walk_evidence_errors({"status": "internal", "minutes": None, "within_30_min": True}))
        self.assertTrue(walk_evidence_errors({"status": "internal", "minutes": None, "within_30_min": False}))

    def test_inclusive_threshold_and_real_zero(self):
        self.assertIs(within_walk_limit(0), True)
        self.assertIs(within_walk_limit(29), True)
        self.assertIs(within_walk_limit(30), True)
        self.assertIs(within_walk_limit(30.01), False)
        self.assertEqual([], walk_evidence_errors({"minutes": 30, "within_30_min": True}))
        self.assertEqual([], walk_evidence_errors({"minutes": 31, "within_30_min": False}))
        self.assertTrue(walk_evidence_errors({"minutes": 31, "within_30_min": True}))

    def test_invalid_numeric_evidence_does_not_qualify(self):
        for bad in (-1, "15", True, float("nan"), float("inf"), -float("inf")):
            with self.subTest(minutes=bad):
                self.assertIsNone(within_walk_limit(bad))
                self.assertTrue(walk_evidence_errors({"minutes": bad, "within_30_min": True}))

    def test_threshold_itself_must_be_valid(self):
        for bad in (-1, "30", False, float("nan")):
            with self.subTest(limit=bad), self.assertRaises(ValueError):
                within_walk_limit(1, bad)

    def test_truthy_non_boolean_flag_is_not_valid(self):
        self.assertTrue(walk_evidence_errors({"minutes": 20, "within_30_min": 1}))
        self.assertTrue(walk_evidence_errors({"minutes": 40, "within_30_min": 0}))


if __name__ == "__main__":
    unittest.main(verbosity=2)
