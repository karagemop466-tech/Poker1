#!/usr/bin/env python3
"""Tests for the facts capture upgrade (SUGGESTIONS P14, defect F83).

F83 is not a hypothetical: the archived official documents in this repository show it.
``data/snapshots/wss_sched.txt`` is the reading-order render of the Wynn Signature
Series schedule PDF, and it does not contain the four multi-day guarantees that the same
PDF prints - ``data/snapshots/wss_sched_reread_20261119.txt``, a table render of the same
file (identical bytes, per the provenance job's own sha256), does contain them. A monitor
built on the line render alone therefore could not have seen those numbers move.

These tests pin three things:
  1. the union signature recovers a fact line the line render drops, proven against those
     two archived captures;
  2. the union never loses a fact line either render found, and is stable;
  3. a signature is only compared with a signature built by the same extractor, so the
     upgrade neither marks 109 sources as changed on its first run nor silently skips the
     comparison.

All offline: no pypdf required, no network.
"""
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import check_source_facts as csf  # noqa: E402
import monitor_sources as ms  # noqa: E402

SNAP = os.path.join(ROOT, "data", "snapshots")


def read(name):
    with open(os.path.join(SNAP, name), encoding="utf-8") as f:
        return f.read()


class FactSets(unittest.TestCase):
    def test_union_recovers_a_fact_the_line_render_drops(self):
        line = read("wss_sched.txt")
        table = read("wss_sched_reread_20261119.txt")
        line_facts = csf.facts_signature(line)
        self.assertFalse([f for f in line_facts if "$150,000" in f],
                         "the archived line render must still show the defect this test guards")
        self.assertTrue([f for f in csf.facts_signature(table) if "$150,000" in f])
        union = csf.facts_union(line, table)
        hits = [f for f in union if "$150,000" in f and "DAY 1A" in f]
        self.assertTrue(hits, "the union must carry the guarantee line of the 1/11 Day 1A row")
        self.assertGreaterEqual(len([f for f in union if "$150,000" in f]), 4,
                                "all four 1/11-1/13 flights print the same guarantee and all belong in the signature")

    def test_layout_only_count_matches(self):
        line = read("wss_sched.txt")
        table = read("wss_sched_reread_20261119.txt")
        only = csf.facts_only_in(table, line)
        self.assertTrue(only)
        self.assertTrue(any("$150,000" in f for f in only))
        line_facts = {f.lower() for f in csf.facts_signature(line)}
        self.assertFalse([f for f in only if f.lower() in line_facts],
                         "a counted 'layout only' line must be absent from the line render")

    def test_union_is_a_superset_deduped_and_sorted(self):
        a = "Guarantee: $20,000\nStart Time: 5:10 PM\nnothing here"
        b = "guarantee:   $20,000\nGuarantee: $30,000"
        union = csf.facts_union(a, b)
        in_union = {f.lower() for f in union}
        self.assertTrue(all(f.lower() in in_union for f in csf.facts_signature(a)),
                        "superset of the first render")
        self.assertTrue(all(f.lower() in in_union for f in csf.facts_signature(b)),
                        "superset of the second render")
        # Membership is case-folded for the same reason facts_signature folds case within
        # one render: the two renders of one document can capitalise a heading
        # differently, and that is not a published value moving.
        self.assertEqual(union, sorted(union))
        self.assertEqual(len(union), len(in_union), "deduplicated, case-folded")
        self.assertEqual(union, csf.facts_union(a, b, a, b), "idempotent across repeated renders")

    def test_empty_renders_are_no_fact(self):
        self.assertEqual(csf.facts_union(""), [])
        self.assertEqual(csf.facts_union("", ""), [])


class Comparability(unittest.TestCase):
    def test_only_same_extractor_is_comparable(self):
        self.assertFalse(csf.facts_comparable(None))
        self.assertFalse(csf.facts_comparable({}), "a legacy signature states no algorithm")
        self.assertFalse(csf.facts_comparable({"facts_algo": "line-only"}))
        self.assertTrue(csf.facts_comparable({"facts_algo": csf.FACTS_ALGO}))

    def test_legacy_baseline_compares_against_the_line_hash(self):
        record = {"facts_sha256": "union-hash", "facts_sha256_line": "line-hash"}
        self.assertEqual(ms.compare_facts({"facts_sha256": "old"}, record), "line-hash")
        self.assertEqual(ms.compare_facts({"facts_sha256": "old", "facts_algo": csf.FACTS_ALGO}, record),
                         "union-hash")
        self.assertIn("predates", ms.facts_basis({"facts_sha256": "old"}))
        self.assertIn("union", ms.facts_basis({"facts_algo": csf.FACTS_ALGO}))

    def test_a_record_without_the_new_field_still_compares(self):
        """An older caller (or a body the extractor refused to parse) has no line hash;
        falling back to the only hash present keeps the monitor answering, not crashing."""
        record = {"facts_sha256": "only-hash"}
        self.assertEqual(ms.compare_facts({"facts_sha256": "x"}, record), "only-hash")

    def test_extractor_change_is_not_reported_as_a_value_change(self):
        """The whole point of keeping two hashes: the content is identical as far as the
        reading-order render can tell, a merged cell has become visible in the layout
        render, and the baseline on file was written by the older extractor."""
        legacy_line_text = "Guarantee: $400"
        legacy = {"facts_sha256": ms.sha("\n".join(csf.facts_signature(legacy_line_text)))}
        # Same document as far as the line render goes; the layout render adds a cell.
        line_text = "Guarantee: $400\na sentence that is not a fact"
        layout_text = "Guarantee: $400\n| 1/11 | DAY 1A | $150,000 |"
        record = {
            "facts_sha256": ms.sha("\n".join(csf.facts_union(line_text, layout_text))),
            "facts_sha256_line": ms.sha("\n".join(csf.facts_signature(line_text))),
        }
        self.assertNotEqual(record["facts_sha256"], legacy["facts_sha256"],
                            "the union signature does move - that is the sensitivity being added")
        self.assertEqual(ms.compare_facts(legacy, record), legacy["facts_sha256"],
                         "a legacy baseline is measured with the legacy definition, so no false alarm")
        union_base = {"facts_sha256": record["facts_sha256"], "facts_algo": csf.FACTS_ALGO}
        self.assertEqual(ms.compare_facts(union_base, record), record["facts_sha256"],
                         "a union baseline is measured with the union, so the merged cell is watched")


class RenderFallback(unittest.TestCase):
    def test_html_body_uses_one_render(self):
        out = csf.body_renders("https://www.venetianlasvegas.com/x.html",
                               b"<html><body><p>Guarantee: $20,000</p></body></html>")
        self.assertEqual(out["layout"], "")
        self.assertIsNone(out["layout_error"])
        self.assertIn("Guarantee", out["line"])
        self.assertEqual(out["line"], csf.to_text("https://www.venetianlasvegas.com/x.html",
                                                  b"<html><body><p>Guarantee: $20,000</p></body></html>"),
                         "to_text must keep returning exactly what the snapshots are built from")

    def test_pdf_without_pypdf_is_an_empty_line_render_not_a_crash(self):
        try:
            import pypdf  # noqa: F401
            has_pypdf = True
        except Exception:
            has_pypdf = False
        out = csf.pdf_renders(b"%PDF-1.4\nnot really a pdf\n")
        self.assertEqual(set(out), {"line", "layout", "layout_error"})
        self.assertEqual(out["line"], "", "an unreadable PDF yields no text, as before")
        if not has_pypdf:
            self.assertEqual(out["layout_error"], "pypdf not installed")

    def test_facts_algo_tag_is_declared_once(self):
        self.assertEqual(csf.FACTS_ALGO, "line+layout-union-v1")
        self.assertEqual(csf.pdf_to_text(b"nope"), csf.pdf_renders(b"nope")["line"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
