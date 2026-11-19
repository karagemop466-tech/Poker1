#!/usr/bin/env python3
"""Tests for the derived spend-advantage reading (scripts/spend_advantage.py).

Two things are proven here and nowhere else:

  1. every bucket of the classifier is reachable from the wording the official
     documents actually use, and each record quotes the row's own excerpt verbatim;
  2. the reading is a pure function of that evidence - change the excerpt and the
     value moves with it, which is what stops the column from being decoration.

Run: python3 -m unittest scripts/test_spend_advantage.py  (or the CI discovery run)
"""
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import spend_advantage  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def rf(value, excerpt, url="https://www.venetianlasvegas.com/x.pdf", label="Structure sheet #99",
        retrieved="2026-11-19"):
    return {"value": value, "excerpt": excerpt, "source": {"label": label, "url": url},
            "retrieved_on": retrieved}


def row(single="not stated", reent="not mentioned", addon="not mentioned", kind="entry",
        status="CAND", s_ex=None, r_ex=None, a_ex=None):
    s_ex = s_ex or ("No re-entry, rebuy, add-on or multi-flight clause appears anywhere on this "
                    "structure sheet (every numbered clause was read on 2026-11-16).")
    r_ex = r_ex or s_ex
    a_ex = a_ex or s_ex
    return {
        "id": "t001", "kind": kind, "entry_status": status,
        "rules": {
            "single_entry": rf(single, s_ex),
            "re_entry": rf(reent, r_ex),
            "add_on": rf(addon, a_ex),
            "fee": rf("house fee $40 of the $200 buy-in; prize pool $160",
                      'Clause 06: "$40 of the $200 Buy-In is withheld for house fees."'),
        },
    }


class Buckets(unittest.TestCase):
    def test_silent_sheet_is_silence_not_permission(self):
        sa = spend_advantage.classify(row())
        self.assertEqual(sa["value"], "no-further-entry-clause")
        self.assertEqual(sa["advantage"], "not-printed")
        self.assertIn("not a written one-entry rule", sa["reading"])

    def test_priced_later_buyin_wins_over_flight_wording(self):
        r = row(reent="possible for later flights", status="MULTI",
                r_ex='Clause 07: "All subsequent buy in\'s after the initial buy in will be $200." '
                     "Later buy-ins are allowed, so the event is not single entry.")
        sa = spend_advantage.classify(r)
        self.assertEqual(sa["value"], "further-entry-priced")
        self.assertEqual(sa["advantage"], "yes")
        self.assertIn("subsequent buy in", sa["excerpt"])

    def test_reentry_terms_printed(self):
        r = row(single="not single entry", reent="allowed", addon="not mentioned on the structure sheet",
                status="RE",
                r_ex='Registration: "Unlimited re-entry will be available until the start of level 9."')
        sa = spend_advantage.classify(r)
        self.assertEqual(sa["value"], "rebuy-or-reentry-printed")
        self.assertEqual(sa["basis"], "rules.re_entry")
        self.assertIn("Unlimited re-entry", sa["excerpt"])

    def test_bag_a_flight_clause(self):
        r = row(single="not single entry", reent="possible for later flights", status="MULTI",
                r_ex='Clause 08: "Any player who bags chips for Day 2 may not play a subsequent '
                     'flight." Later entry after busting is not addressed; exclude from the strict list.')
        sa = spend_advantage.classify(r)
        self.assertEqual(sa["value"], "later-flight-printed")
        self.assertEqual(sa["advantage"], "yes")

    def test_unread_document_is_unknown(self):
        r = row(single="unknown", reent="unknown", addon="unknown", status="UNV",
                s_ex='The official Wynn Signature Series Structures PDF published by Wynn contains a '
                     '"COMING SOON" placeholder and no structure sheets (read on 2026-11-19). '
                     "Entry rule unknown.")
        sa = spend_advantage.classify(r)
        self.assertEqual(sa["value"], "no-structure-sheet")
        self.assertEqual(sa["advantage"], "unknown")

    def test_continuation_row(self):
        r = row(single="not applicable", reent="not mentioned", status="CONT", kind="continuation",
                s_ex="Day 2 restart of the event above: the sheet sells no entry on this row.")
        sa = spend_advantage.classify(r)
        self.assertEqual(sa["value"], "continuation")
        self.assertEqual(sa["advantage"], "none")

    def test_row_without_rules_has_no_reading(self):
        self.assertIsNone(spend_advantage.classify({"id": "x", "rules": {}}))

    def test_curly_apostrophe_variant_is_still_priced(self):
        r = row(reent="allowed", status="RE",
                r_ex='Clause 07: "All subsequent buy in\u2019s after the initial buy in will be $200."')
        self.assertEqual(spend_advantage.classify(r)["value"], "further-entry-priced")


class Evidence(unittest.TestCase):
    def test_excerpt_is_verbatim_from_the_row(self):
        for r in (row(), row(reent="allowed", status="RE"), row(single="unknown", reent="unknown")):
            sa = spend_advantage.classify(r)
            stored = [v["excerpt"] for v in r["rules"].values()]
            self.assertIn(sa["excerpt"], stored)
            field = sa["basis"].split(".")[1]
            self.assertEqual(sa["source"], r["rules"][field]["source"])
            self.assertEqual(sa["retrieved_on"], r["rules"][field]["retrieved_on"])

    def test_reading_follows_the_evidence_not_the_label(self):
        """Change only the clause text and the derived value must move with it.

        The discriminator the classifier reads for itself is the priced later buy-in:
        a row whose stored excerpt starts to quote one is no longer "no clause
        printed", even though nothing else about the row changed. That is what makes
        the column evidence-driven rather than a restatement of ``entry_status``.
        """
        before = spend_advantage.classify(row())
        tampered = row(r_ex='Clause 07: "All subsequent buy in\'s after the initial buy in will '
                            'be $200."')
        after = spend_advantage.classify(tampered)
        self.assertEqual(before["value"], "no-further-entry-clause")
        self.assertEqual(after["value"], "further-entry-priced")
        self.assertEqual(after["advantage"], "yes")

    def test_pure_and_total(self):
        rows = [row(), row(reent="allowed", status="RE"), row(kind="continuation", status="CONT"),
                row(single="unknown", reent="unknown", status="UNV")]
        first = [spend_advantage.classify(r) for r in rows]
        second = [spend_advantage.classify(r) for r in rows]
        self.assertEqual(first, second)
        self.assertTrue(all(sa and sa["value"] in spend_advantage.VALUES for sa in first))

    def test_every_bucket_documented(self):
        for v in spend_advantage.VALUES:
            self.assertTrue(spend_advantage.LABEL[v].strip())
            self.assertTrue(spend_advantage.READING[v].strip())
            self.assertIn(v, spend_advantage.ADVANTAGE)


class PublishedData(unittest.TestCase):
    """The column as it stands in the generated dataset."""

    @classmethod
    def setUpClass(cls):
        with open(os.path.join(ROOT, "data", "tournaments.json"), encoding="utf-8") as f:
            cls.rows = json.load(f)["rows"]

    def test_every_row_carries_a_reading(self):
        missing = [r["id"] for r in self.rows if not isinstance(r.get("spend_advantage"), dict)]
        self.assertEqual(missing, [], "rows without a spend_advantage record")

    def test_no_row_is_promoted_by_it(self):
        for r in self.rows:
            sa = r.get("spend_advantage") or {}
            if sa.get("advantage") == "yes":
                self.assertNotEqual(r["entry_status"], "SE",
                                    "%s prints a further-entry clause and cannot be SE" % r["id"])

    def test_silence_only_where_the_sheet_is_silent(self):
        for r in self.rows:
            sa = r.get("spend_advantage") or {}
            if sa.get("value") == "no-further-entry-clause":
                self.assertEqual(r["rules"]["re_entry"]["value"], "not mentioned")
                self.assertEqual(r["rules"]["single_entry"]["value"], "not stated")

    def test_rederived_from_the_published_excerpts(self):
        for r in self.rows:
            expect = spend_advantage.classify({"kind": r["kind"], "rules": r["rules"]})
            self.assertEqual(r["spend_advantage"]["value"], expect["value"], r["id"])
            self.assertEqual(r["spend_advantage"]["excerpt"], expect["excerpt"], r["id"])

    def test_summary_counts_every_row(self):
        s = spend_advantage.summary(self.rows)
        self.assertEqual(sum(s.values()), len(self.rows))
        self.assertEqual(set(s), set(spend_advantage.VALUES))


if __name__ == "__main__":
    unittest.main(verbosity=2)
