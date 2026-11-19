#!/usr/bin/env python3
"""Offline schedule tests for unknown finishes and conditional options."""
import copy
import unittest

from conditional_schedule import build_schedule
from test_entry_evidence import URL, DOC, confirmed_fixture


def event(identity, start, status="CAND", day="2026-11-26", late=None):
    row = confirmed_fixture()
    row.update({"id": identity, "date": day, "start": start, "name": identity,
                "series": "test", "venue": "test", "entry_status": status,
                "labels": [], "late_reg_close": late, "est_end": "02:55",
                "est_duration_min": 945, "buy_in_usd": 300, "guarantee_usd": 10000})
    return row


class ConditionalScheduleTests(unittest.TestCase):
    def setUp(self):
        self.archives = {URL: DOC}

    def build(self, rows):
        return build_schedule(rows, "2026-11-19", self.archives)

    def test_no_confirmed_events_means_no_suggested_primary(self):
        result = self.build([event("early", "11:10"), event("late", "17:10", late="21:40")])
        day = result["days"][0]
        self.assertIsNone(day["primary_id"])
        self.assertIsNone(day["fallback_id"])
        self.assertIn("No strictly confirmed", day["fallback_note"])
        self.assertEqual(1, result["overlap_pairs"])
        self.assertIn("finish is unknown", day["conflicts"][0]["detail"])
        self.assertEqual("21:40", day["conflicts"][0]["b_late_reg_close"])

    def test_confirmed_later_event_is_conditional_not_a_proven_sequence(self):
        rows = [event("A", "11:10", "SE"), event("B", "17:10", "SE", late="21:40")]
        day = self.build(rows)["days"][0]
        self.assertEqual("A", day["primary_id"])
        self.assertEqual("B", day["fallback_id"])
        self.assertEqual("conditional", day["fallback_kind"])
        self.assertIn("eliminated", day["fallback_note"])
        self.assertIn("travel", day["fallback_note"])
        self.assertIn("21:40", day["fallback_note"])
        self.assertTrue(all(e["est_end"] is None and e["est_duration_min"] is None for e in day["events"]))

    def test_simultaneous_start_is_an_alternative_not_a_fallback(self):
        day = self.build([event("A", "11:00", "SE"), event("B", "11:00", "SE")])["days"][0]
        self.assertIsNone(day["fallback_id"])
        self.assertEqual(["B"], [a["id"] for a in day["alternatives"]])
        self.assertEqual("simultaneous_start", day["conflicts"][0]["kind"])
        self.assertIn("cannot be started simultaneously", day["conflicts"][0]["detail"])

    def test_every_pair_and_cross_day_risk_is_recorded(self):
        rows = [event("A", "09:00"), event("B", "11:00"), event("C", "11:00"), event("D", "17:00"),
                event("E", "09:00", day="2026-11-27")]
        result = self.build(rows)
        day = result["days"][0]
        self.assertEqual(6, len(day["conflicts"]))
        self.assertEqual(1, day["conflicts_simultaneous_start"])
        self.assertEqual(5, day["conflicts_potential_overlap"])
        self.assertIn("previous day's event", result["days"][1]["cross_day_warning"])

    def test_missing_deadline_is_never_invented(self):
        day = self.build([event("A", "11:00", "SE"), event("B", "17:00", "SE")])["days"][0]
        self.assertIn("late-registration deadline unverified", day["fallback_note"])
        self.assertIn("deadline not published", day["conflicts"][0]["detail"])

    def test_unsupported_se_status_refuses_to_build(self):
        row = event("A", "11:00", "SE")
        del row["rules"]["add_on"]
        with self.assertRaisesRegex(ValueError, "Unsupported SE"):
            self.build([row])

    def test_continuations_not_mislabelled_as_new_entries(self):
        row = event("restart", "11:00", "CONT")
        row["kind"] = "continuation"
        result = self.build([row, event("entry", "12:00")])
        day = result["days"][0]
        self.assertEqual(["entry"], [r["id"] for r in day["events"]])
        self.assertEqual(["restart"], [r["id"] for r in day["continuations"]])
        self.assertIn("not new entry", day["continuation_note"])
        self.assertIn("previous day's event", day["cross_day_warning"])
        self.assertIsNone(day["primary_id"])
        self.assertEqual([], day["conflicts"])

    def test_date_with_only_a_continuation_is_preserved(self):
        restart = event("restart", "11:00", "CONT")
        restart["kind"] = "continuation"
        day = self.build([restart])["days"][0]
        self.assertEqual("2026-11-26", day["date"])
        self.assertEqual([], day["events"])
        self.assertEqual(["restart"], [r["id"] for r in day["continuations"]])
        self.assertIsNone(day["primary_id"])

    def test_deterministic_and_preserves_input(self):
        rows = [event("B", "17:00"), event("A", "11:00")]
        old = copy.deepcopy(rows)
        self.assertEqual(self.build(rows), self.build(list(reversed(rows))))
        self.assertEqual(old, rows)


if __name__ == "__main__":
    unittest.main(verbosity=2)
