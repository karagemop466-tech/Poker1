#!/usr/bin/env python3
"""Offline checks for the room survey; does not write generated site files."""
import unittest
import build_other_rooms as other


class OtherRoomsEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.dataset = other.build_dataset()

    def test_westgate_publishes_daily_tournaments_not_an_event_structure(self):
        room = next(r for r in self.dataset["rooms"] if r["id"] == "westgate")
        self.assertIn("(702) 732-5223", room["poker_room_quote"])
        self.assertEqual([], room["events"])
        self.assertIn("unverified", room["schedule_status"])
        self.assertTrue(any(s["url"] == other.WESTGATE_PAGE for s in room["sources"]))

    def test_orleans_october_named_pdf_is_not_presented_as_current(self):
        room = next(r for r in self.dataset["rooms"] if r["id"] == "orleans")
        self.assertIn("unverified", room["schedule_status"])
        self.assertIn("October", room["schedule_note"])
        for event in room["events"]:
            self.assertIn("current validity is unverified", event["status_note"])

    def test_historical_windows_are_not_ranked_as_like_for_like(self):
        html = other.windows_section()
        self.assertIn("not like-for-like", html)
        self.assertIn("not a playable itinerary", html)
        self.assertNotIn("cheapest quoted window", html.lower())
        self.assertNotIn("choice can be made like-for-like", html.lower())
        self.assertIn("Strictly confirmed entry options", html)

    def test_page_keeps_a_current_validity_warning(self):
        html = other.render_page(self.dataset)
        self.assertIn("does not establish whether the grid is current", html)
        self.assertIn("(702) 732-5223", html)
        self.assertIn("Different dates and rooms are not like-for-like", html)
        self.assertNotIn("Single entry - no clause permitting a further entry", html)


if __name__ == "__main__":
    unittest.main(verbosity=2)
