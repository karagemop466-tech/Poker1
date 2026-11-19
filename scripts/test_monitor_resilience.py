#!/usr/bin/env python3
"""The scheduled monitor must finish even when one source misbehaves.

Context: run 44468765019 (2026-11-19T05:58Z) failed the step "Check every
official source, including its content" - one source whose response raised
inside the fetch loop aborted the whole re-check, so the remaining sources got
no check at all that morning and data/monitoring.json stayed at its 2026-11-17
fallback state. These tests pin the containment: a refused connection, an
exception raised mid-response, and an extractor that blow up must all be
*recorded*, never propagated, and a row without the full rules shape must not
crash the fingerprint step that compares data/row_snapshot.json.
"""
import http.client
import io
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import monitor_sources as ms  # noqa: E402


class FingerprintTests(unittest.TestCase):
    FULL = {
        "id": "r1", "date": "2026-11-26", "start": "11:10", "name": "Event 12",
        "venue": "The Venetian", "series": "DSE IV", "buy_in_usd": 300,
        "guarantee_usd": 10000, "entry_status": "CAND",
        "rules": {"fee": {"value": "$242 + $58"}}, "flags": ["f1"],
    }

    def test_complete_row_fingerprint_is_unchanged(self):
        # Byte-for-byte the shape data/row_snapshot.json stores: the guard must
        # not silently move any comparison and mark every row as "changed".
        self.assertEqual(ms.fingerprint(self.FULL), {
            "date": "2026-11-26", "start": "11:10", "name": "Event 12",
            "venue": "The Venetian", "series": "DSE IV", "buy_in_usd": 300,
            "guarantee_usd": 10000, "entry_status": "CAND",
            "buy_in": "$242 + $58", "flags": 1,
        })

    def test_incomplete_row_does_not_raise(self):
        for partial in ({}, {"id": "r2"}, {"name": "x", "rules": {}},
                        {"rules": {"fee": None}}, {"rules": []}):
            fp = ms.fingerprint(partial)  # used to be a KeyError
            self.assertIsInstance(fp, dict)
            self.assertIsNone(fp.get("buy_in"))

    def test_real_dataset_still_matches_the_stored_snapshot(self):
        rows = ms.load("tournaments.json")["rows"]
        snapshot = ms.load("row_snapshot.json")
        if not snapshot:  # never generated in a fresh checkout
            self.skipTest("no row_snapshot.json to compare against")
        for row in rows:
            self.assertEqual(snapshot["rows"][row["id"]], ms.fingerprint(row),
                             "fingerprint moved for %s - the guard changed published comparisons" % row["id"])


class _Resp:
    def __init__(self, body=b"<html>ok</html>", status=200):
        self._body = io.BytesIO(body)
        self.status = status

    def read(self, n=-1):
        return self._body.read(n)

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class CheckUrlGuardTests(unittest.TestCase):
    def test_connection_refused_is_recorded_not_raised(self):
        rec = ms.check_url("http://127.0.0.1:9/x.html", False)
        self.assertEqual(rec["status"], "unreachable")
        self.assertIn("error", rec)

    def test_mid_response_http_exception_is_contained(self):
        def boom(req, timeout=None):
            raise http.client.IncompleteRead(b"partial")
        orig, ms.urlopen = ms.urlopen, boom
        try:
            rec = ms.check_url("https://operator.example/page.html", True)
        finally:
            ms.urlopen = orig
        self.assertEqual(rec["status"], "http-error")
        self.assertTrue(rec.get("unexpected"))
        self.assertIn("IncompleteRead", rec["error"])

    def test_extractor_exception_is_contained(self):
        orig_open, orig_text = ms.urlopen, ms.csf.to_text
        ms.urlopen = lambda req, timeout=None: _Resp()

        def explode(url, data):
            raise RuntimeError("decoder blew up")
        ms.csf.to_text = explode
        try:
            rec = ms.check_url("https://operator.example/page.html", True)
        finally:
            ms.urlopen, ms.csf.to_text = orig_open, orig_text
        self.assertEqual(rec["status"], "http-error")
        self.assertTrue(rec.get("unexpected"))
        self.assertIn("decoder blew up", rec["error"])

    def test_clean_fetch_still_hashes(self):
        orig_open, orig_text = ms.urlopen, ms.csf.to_text
        ms.urlopen = lambda req, timeout=None: _Resp(b"<html>Guarantee $10,000 at 11:10 AM</html>")
        ms.csf.to_text = lambda url, data: "Guarantee $10,000 at 11:10 AM"
        try:
            rec = ms.check_url("https://operator.example/page.html", True)
        finally:
            ms.urlopen, ms.csf.to_text = orig_open, orig_text
        self.assertEqual(rec["status"], "ok")
        self.assertIsNotNone(rec["sha256"])
        self.assertFalse(rec.get("unexpected"))
        self.assertEqual(rec["facts_count"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
