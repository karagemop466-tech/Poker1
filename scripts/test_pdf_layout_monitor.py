#!/usr/bin/env python3
"""Position-aware PDF monitoring must not lose facts or invent a change at migration."""
import os
import sys
import types
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import check_source_facts as csf  # noqa: E402
import monitor_sources as monitor  # noqa: E402
import schedule_feed  # noqa: E402


class _Page:
    def extract_text(self, extraction_mode=None):
        if extraction_mode == "layout":
            return "DATE TIME EVENT GUARANTEE ENTRY\n1/18 11 A.M. DAY 1A $100,000 $400"
        return "DATE\nTIME\nEVENT\nENTRY\n1/18\n11 A.M.\nDAY 1A\n$400"


class _Reader:
    def __init__(self, _stream):
        self.pages = [_Page()]


class _BrokenLayoutPage:
    def extract_text(self, extraction_mode=None):
        if extraction_mode == "layout":
            raise ValueError("layout decoder failed")
        return "EVENT DAY 1A $400"


class _BrokenLayoutReader:
    def __init__(self, _stream):
        self.pages = [_BrokenLayoutPage()]


class PdfLayoutExtractionTests(unittest.TestCase):
    def test_pdf_capture_keeps_plain_and_layout_render_separate(self):
        fake_pypdf = types.SimpleNamespace(PdfReader=_Reader)
        with patch.dict(sys.modules, {"pypdf": fake_pypdf}):
            variants = csf.to_text_variants("https://official.example/schedule.pdf", b"%PDF-test")
        self.assertTrue(variants["is_pdf"])
        self.assertIn("DAY 1A", variants["plain"])
        self.assertIn("$100,000", variants["layout"])
        self.assertNotIn("$100,000", variants["plain"])
        self.assertIsNone(variants["layout_error"])

    def test_union_finds_layout_only_fact(self):
        plain = "1/18\n11 A.M.\nDAY 1A\n$400"
        layout = "1/18 | 11 A.M. | DAY 1A | GUARANTEE $100,000 | ENTRY $400"
        combined = csf.union_facts_signature(plain, layout)
        self.assertTrue(any("$100,000" in line for line in combined))
        self.assertTrue(any("DAY 1A" in line and "$100,000" in line for line in combined))

    def test_failed_layout_render_is_reported_and_not_compared(self):
        fake_pypdf = types.SimpleNamespace(PdfReader=_BrokenLayoutReader)
        with patch.dict(sys.modules, {"pypdf": fake_pypdf}):
            variants = csf.to_text_variants("https://official.example/schedule.pdf", b"%PDF-test")
        self.assertTrue(variants["plain"].strip())
        self.assertFalse(variants["layout"].strip())
        self.assertIn("layout decoder failed", variants["layout_error"])
        changed, diff, pending = csf.compare_fact_signatures(
            {"facts_signature_plain": ["EVENT DAY 1A $400"],
             "facts_signature_layout": ["DAY 1A $100,000"],
             "facts_signature_layout_available": True},
            csf.facts_signature(variants["plain"]), [], False, True)
        self.assertFalse(changed)
        self.assertEqual([], diff)
        self.assertFalse(pending)

    def test_first_layout_capture_is_pending_not_a_false_source_change(self):
        previous = {"facts_signature": ["1/18 11 A.M. DAY 1A $400"]}
        changed, diff, pending = csf.compare_fact_signatures(
            previous,
            ["1/18 11 A.M. DAY 1A $400"],
            ["1/18 11 A.M. DAY 1A $100,000 $400"],
            True,
        )
        self.assertFalse(changed)
        self.assertEqual([], diff)
        self.assertTrue(pending)

    def test_layout_changes_are_compared_after_first_capture(self):
        previous = {
            "facts_signature_plain": ["11 A.M. DAY 1A $400"],
            "facts_signature_layout": ["11 A.M. DAY 1A $100,000 $400"],
        }
        changed, diff, pending = csf.compare_fact_signatures(
            previous,
            ["11 A.M. DAY 1A $400"],
            ["11 A.M. DAY 1A $150,000 $400"],
            True,
        )
        self.assertTrue(changed)
        self.assertTrue(any("layout +" in item and "$150,000" in item for item in diff))
        self.assertTrue(any("layout -" in item and "$100,000" in item for item in diff))
        self.assertFalse(pending)

    def test_incomplete_prior_render_becomes_a_baseline_not_a_false_change(self):
        previous = {
            "facts_signature_plain": ["truncated old plain fact"],
            "facts_signature_plain_available": False,
            "facts_signature_layout": ["truncated old layout fact"],
            "facts_signature_layout_available": False,
        }
        changed, diff, pending = csf.compare_fact_signatures(
            previous,
            ["complete current plain fact"],
            ["complete current layout fact"],
            True,
            True,
        )
        self.assertFalse(changed)
        self.assertEqual([], diff)
        self.assertTrue(pending)


class LayoutBaselineTests(unittest.TestCase):
    def test_seed_adds_only_missing_layout_hash_and_preserves_plain_baseline(self):
        url = "https://official.example/schedule.pdf"
        log = {"sources": [{"id": "s1", "url": url, "http_status": 200,
                            "facts_signature_layout": ["DAY 1A $100,000"],
                            "layout_status": "baseline-pending", "layout_extracted_chars": 48,
                            "last_checked_utc": "2026-11-19T16:00:00Z"}]}
        baseline = {"sources": {url: {"facts_sha256": "original-plain-hash",
                                       "checked_at_utc": "2026-11-17T00:00:00Z"}}}
        updated, seeded = monitor.seed_layout_baseline(log, baseline)
        self.assertEqual(["s1"], seeded)
        entry = updated["sources"][url]
        self.assertEqual("original-plain-hash", entry["facts_sha256"])
        self.assertEqual("2026-11-19T16:00:00Z", entry["layout_checked_at_utc"])
        self.assertEqual(1, entry["layout_facts_count"])
        changed, again = monitor.seed_layout_baseline(log, updated)
        self.assertEqual([], again)
        self.assertEqual(entry["layout_facts_sha256"], changed["sources"][url]["layout_facts_sha256"])

        partial_log = {"sources": [{"id": "s2", "url": "https://official.example/partial.pdf",
                                    "http_status": 200, "facts_signature_layout": ["valid layout facts"],
                                    "layout_status": "partial", "layout_extracted_chars": 30,
                                    "plain_error": "plain renderer failed", "layout_error": None,
                                    "last_checked_utc": "2026-11-19T16:00:00Z"}]}
        partial_base = {"sources": {"https://official.example/partial.pdf": {"facts_sha256": "plain"}}}
        seeded_partial, ids = monitor.seed_layout_baseline(partial_log, partial_base)
        self.assertEqual(["s2"], ids, "a complete layout render can seed even if plain rendering failed")
        broken_log = {"sources": [dict(partial_log["sources"][0], layout_error="layout renderer failed")]}
        untouched, ids = monitor.seed_layout_baseline(broken_log, partial_base)
        self.assertEqual([], ids, "a partial layout render must not seed its own comparison baseline")
        self.assertNotIn("layout_facts_sha256", untouched["sources"]["https://official.example/partial.pdf"])

        new_url = "https://official.example/new-schedule.pdf"
        new_log = {"sources": [{"id": "s3", "url": new_url, "http_status": 200,
                               "sha256": "served-bytes", "facts_signature_plain": ["$400 entry"],
                               "facts_signature_plain_available": True,
                               "facts_signature_layout": ["$100,000 guarantee"],
                               "facts_signature_layout_available": True,
                               "facts_signature": ["$100,000 guarantee", "$400 entry"],
                               "facts_checked": 2, "layout_status": "baseline-pending",
                               "layout_extracted_chars": 55, "last_checked_utc": "2026-11-19T16:00:00Z"}]}
        new_base, ids = monitor.seed_layout_baseline(new_log, {"sources": {}})
        self.assertEqual(["s3"], ids, "a successful new source gets a first comparison baseline")
        entry = new_base["sources"][new_url]
        self.assertIsNone(entry["sha256"], "provenance bytes are not comparable to the monitor's text hash")
        self.assertEqual("served-bytes", entry["provenance_sha256"])
        self.assertEqual(1, entry["layout_facts_count"])
        self.assertEqual(2, entry["facts_count"])

    def test_layout_review_maps_pending_and_partial_sources_to_published_rows(self):
        url = "https://official.example/table.pdf"
        refs = {url: [{"kind": "tournament", "id": "r1", "label": "Event A", "date": "2027-01-18"}]}
        pending = monitor.build_layout_review({url: {
            "content_status": "facts-changed", "layout_status": "captured",
            "layout_baseline_pending": True, "provenance_checked_at": "2026-11-19T16:00:00Z",
        }}, refs)
        self.assertEqual(1, len(pending), "layout review remains visible alongside a separate source-change mark")
        self.assertEqual("layout-baseline-pending", pending[0]["status"])
        self.assertEqual("r1", pending[0]["id"])
        self.assertEqual(url, pending[0]["source_url"])

        partial = monitor.build_layout_review({url: {
            "content_status": "facts-changed", "layout_status": "partial",
            "layout_error": "page 2 decoder failed",
        }}, refs)
        self.assertEqual("layout-unavailable", partial[0]["status"])
        self.assertIn("incomplete", partial[0]["reason"])

    def test_content_verdict_distinguishes_pending_changed_and_unavailable(self):
        record = {"status": "ok", "is_pdf": True, "layout_status": "captured",
                  "facts_sha256": "plain", "plain_facts_sha256": "plain",
                  "layout_facts_sha256": "layout-a", "sha256": "raw"}
        status, pending = monitor.content_verdict(record, {"facts_sha256": "plain"})
        self.assertEqual("layout-baseline-pending", status)
        self.assertTrue(pending)

        status, pending = monitor.content_verdict(record, {
            "facts_sha256": "plain", "layout_facts_sha256": "layout-a"})
        self.assertEqual("unchanged", status)
        self.assertFalse(pending)

        new_source_base = {"facts_sha256": "plain", "layout_facts_sha256": "layout-a", "sha256": None}
        status, pending = monitor.content_verdict(record, new_source_base)
        self.assertEqual("unchanged", status, "fresh provenance hashes do not masquerade as monitor text hashes")
        self.assertFalse(pending)

        changed = dict(record, layout_facts_sha256="layout-b")
        status, _ = monitor.content_verdict(changed, {
            "facts_sha256": "plain", "layout_facts_sha256": "layout-a"})
        self.assertEqual("facts-changed", status)

        unavailable = dict(record, layout_status="unavailable", layout_facts_sha256=None)
        status, _ = monitor.content_verdict(unavailable, {"facts_sha256": "plain"})
        self.assertEqual("layout-unavailable", status)

        partial = dict(record, layout_status="partial", plain_error="line render failed",
                       plain_facts_sha256="different", layout_facts_sha256="layout-a")
        status, _ = monitor.content_verdict(partial, {
            "facts_sha256": "plain", "layout_facts_sha256": "layout-a"})
        self.assertEqual("layout-unavailable", status,
                         "a failed render cannot make an incomplete signature look like a source change")

        truncated = dict(record, truncated=True, layout_error="truncated PDF response",
                         layout_status="partial")
        status, pending = monitor.content_verdict(truncated, {"facts_sha256": "plain"})
        self.assertEqual("not-comparable", status)
        self.assertFalse(pending)
        self.assertEqual("layout-unavailable", monitor.build_layout_review(
            {"https://official.example/table.pdf": truncated},
            {"https://official.example/table.pdf": [{"kind": "tournament", "id": "r1", "label": "Event A"}]}
        )[0]["status"])

    def test_archived_wynn_table_capture_yields_schedule_excerpts(self):
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(root, "data", "snapshots", "wss_sched_reread_20261119.txt")
        with open(path, encoding="utf-8") as f:
            layout = f.read()
        state = schedule_feed.capture_state({}, "", layout, True)
        self.assertGreater(state["layout_excerpts_count"], 0)
        self.assertTrue(state["layout_baseline_pending"])
        self.assertTrue(any("$150,000" in excerpt for excerpt in state["excerpts"]))
        self.assertTrue(any("$100,000" in excerpt for excerpt in state["excerpts"]))

    def test_schedule_feed_migrates_plain_hash_without_claiming_change(self):
        plain = "11 A.M.\nNo Limit Hold'em Day 1A\n$400"
        old_rows = schedule_feed.excerpts(plain)
        old_digest = schedule_feed._digest(old_rows)
        layout = "| 1/18 | MON | 11 A.M. | No Limit Hold'em Day 1A | $100,000 | $400 |"
        first = schedule_feed.capture_state({"digest": old_digest}, plain, layout, True)
        self.assertFalse(first["changed"])
        self.assertTrue(first["layout_baseline_pending"])
        self.assertTrue(any("$100,000" in excerpt for excerpt in first["excerpts"]))

        changed_layout = layout.replace("$100,000", "$150,000")
        second = schedule_feed.capture_state(first, plain, changed_layout, True)
        self.assertTrue(second["changed"])
        self.assertFalse(second["layout_baseline_pending"])
        self.assertNotEqual(first["layout_digest"], second["layout_digest"])

    def test_incomplete_schedule_render_is_not_mistaken_for_source_change(self):
        plain = "11 A.M.\nNo Limit Hold'em Day 1A\n$400"
        layout = "| 1/18 | MON | 11 A.M. | No Limit Hold'em Day 1A | $100,000 | $400 |"
        previous = schedule_feed.capture_state({}, plain, layout, True)
        broken = schedule_feed.capture_state(
            previous,
            plain.replace("$400", "$500"),
            layout.replace("$100,000", "$200,000"),
            True,
            layout_error="page 1 layout decoder failed",
            plain_error="page 1 plain decoder failed",
        )
        self.assertFalse(broken["changed"])
        self.assertEqual("partial", broken["layout_status"])
        self.assertIn("layout decoder failed", broken["layout_error"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
