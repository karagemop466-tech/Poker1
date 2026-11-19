#!/usr/bin/env python3
"""Tests for scripts/check_monitor_run.py - the step that decides whether a
monitoring run is worth reading, and fails the job when it is not.

Each case is one quiet failure mode this repository has actually had: a provenance
run that refused, a machine with no route to the operators leaning on a stale
fallback, a report so old the schedule is not running, and a comparison still being
made against a pre-union baseline.
"""
import datetime
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import check_monitor_run as cmr  # noqa: E402

TODAY = datetime.date(2026, 11, 19)


def mon(**kw):
    base = {"checked_at_utc": "2026-11-19T16:45:28Z", "sources_total": 109, "sources_ok": 99,
            "sources_raw_changed": 22, "sources_facts_changed": 0, "rows_source_changed": 0}
    base.update(kw)
    return base


def codes(findings):
    return [c for _, c, _ in findings]


class Rules(unittest.TestCase):
    def test_a_good_run_says_nothing(self):
        self.assertEqual(cmr.findings(mon=mon(), last_run_text="checked 109 sources\n",
                                      prov={"generated_utc": "2026-11-19T11:37:11Z"},
                                      today=TODAY), [])

    def test_missing_report_is_an_error(self):
        out = cmr.findings(mon=None, today=TODAY)
        self.assertEqual(codes(out), ["no-report"])
        self.assertTrue(all(l == "error" for l, _, _ in out))

    def test_refusal_anywhere_in_the_log_is_an_error(self):
        # The refusal is preceded by extractor warnings, so scanning only the first
        # line would have missed it - which is how the green run happened before.
        text = "fontTools is required to fully parse...\nIgnoring wrong pointing object 8 0\n" \
               "Refusing to run: non-official host(s) in manifest: [('x', 'evil.example')]\n"
        out = cmr.findings(mon=mon(), last_run_text=text,
                           prov={"generated_utc": "2026-11-19T11:37:11Z"}, today=TODAY)
        self.assertIn("provenance-refused", codes(out))
        self.assertIn("evil.example", out[0][2])

    def test_no_route_with_a_fresh_fallback_is_a_warning_only(self):
        out = cmr.findings(mon=mon(sources_ok=0, network_unavailable=True),
                           prov={"generated_utc": "2026-11-18T06:47:00Z"}, today=TODAY)
        self.assertEqual(codes(out), ["fell-back"])
        self.assertEqual(out[0][0], "warn")

    def test_no_route_with_a_stale_fallback_is_an_error(self):
        out = cmr.findings(mon=mon(sources_ok=0), prov={"generated_utc": "2026-10-30T06:47:00Z"},
                           today=TODAY)
        self.assertIn("no-evidence", codes(out))
        self.assertTrue(any(l == "error" and c == "no-evidence" for l, c, _ in out))

    def test_no_route_and_no_dated_fallback_is_an_error(self):
        out = cmr.findings(mon=mon(sources_ok=0), prov=None, today=TODAY)
        self.assertEqual(codes(out), ["no-evidence"])

    def test_unparseable_fallback_date_is_treated_as_no_evidence(self):
        out = cmr.findings(mon=mon(sources_ok=0), prov={"generated_utc": "yesterday-ish"},
                           today=TODAY)
        self.assertEqual(codes(out), ["no-evidence"])

    def test_stale_report_is_an_error(self):
        out = cmr.findings(mon=mon(checked_at_utc="2026-11-01T03:00:00Z"),
                          prov={"generated_utc": "2026-11-19T06:47:00Z"}, today=TODAY,
                          max_age_days=7)
        self.assertIn("stale-report", codes(out))

    def test_minority_of_sources_reachable_is_a_warning(self):
        out = cmr.findings(mon=mon(sources_ok=40), prov={"generated_utc": "2026-11-19T06:47:00Z"},
                           today=TODAY)
        self.assertEqual(codes(out), ["mostly-unreachable"])
        self.assertEqual(out[0][0], "warn")

    def test_legacy_baseline_is_advertised_not_assumed(self):
        out = cmr.findings(mon=mon(sources_facts_legacy_baseline=74),
                           prov={"generated_utc": "2026-11-19T06:47:00Z"}, today=TODAY)
        self.assertEqual(codes(out), ["legacy-baseline"])
        self.assertIn("74 source", out[0][2])
        self.assertEqual(out[0][0], "warn", "a legacy baseline is a weaker check, not a failed run")

    def test_many_provenance_errors_is_a_warning(self):
        out = cmr.findings(mon=mon(), prov={"generated_utc": "2026-11-19T06:47:00Z",
                                            "error_count": 60}, today=TODAY)
        self.assertEqual(codes(out), ["provenance-errors"])

    def test_errors_sort_first_and_exit_code_follows_them(self):
        out = cmr.findings(mon=mon(sources_ok=0, checked_at_utc="2026-01-01T00:00:00Z"),
                           prov={"generated_utc": "2026-01-01T00:00:00Z"}, today=TODAY)
        self.assertTrue(out)
        self.assertEqual(out[0][0], "error", "a reader sees the blocking finding first")

    def test_no_zero_division_on_an_empty_run(self):
        # sources_total 0 must not raise, and must not invent a verdict.
        out = cmr.findings(mon=mon(sources_total=0, sources_ok=0), today=TODAY)
        self.assertEqual(codes(out), [])


class Helpers(unittest.TestCase):
    def test_age_days(self):
        self.assertEqual(cmr.age_days("2026-11-19T16:45:28Z", TODAY), 0)
        self.assertEqual(cmr.age_days("2026-11-17", TODAY), 2)
        self.assertIsNone(cmr.age_days(None, TODAY))
        self.assertIsNone(cmr.age_days("not a date", TODAY))

    def test_date_only_values_parse(self):
        self.assertEqual(cmr.age_days(datetime.date(2026, 11, 1), TODAY), 18)


if __name__ == "__main__":
    unittest.main(verbosity=2)
