#!/usr/bin/env python3
"""Regression tests for source-monitor scheduling and publication failures."""
import os
import subprocess
import tempfile
import textwrap
import unittest
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
MONITOR = ROOT / ".github/workflows/monitor.yml"
SOURCE_FACTS = ROOT / ".github/workflows/source-facts.yml"


class MonitorGuardTests(unittest.TestCase):
    def test_daily_monitor_is_a_vegas_morning_and_follows_feed(self):
        text = MONITOR.read_text()
        self.assertIn('cron: "17 15 * * *"', text)
        for month, expected_hour in ((1, 7), (7, 8)):
            dt = datetime(2027, month, 1, 15, 17, tzinfo=timezone.utc)
            self.assertEqual(expected_hour, dt.astimezone(ZoneInfo("America/Los_Angeles")).hour)
        self.assertIn("cron: '17 14 * * *'", (ROOT / ".github/workflows/schedule-feed.yml").read_text())

    def test_piped_monitor_failure_is_not_hidden(self):
        text = MONITOR.read_text()
        section = text.split("- name: Check every official source", 1)[1].split("- name:", 1)[0]
        self.assertIn("set -euo pipefail", section)
        self.assertIn("scripts/monitor_sources.py $args | tee monitor.txt", section)
        result = subprocess.run(["bash", "-c", "set -o pipefail; (exit 23) | tee /dev/null"])
        self.assertEqual(23, result.returncode)

    def test_no_change_summary_does_not_claim_failed_sources_are_unchanged(self):
        text = MONITOR.read_text()
        section = text.split("- name: Comment on the run when nothing moved", 1)[1]
        self.assertIn("not proof", section)
        self.assertIn("unreachable, unreadable, or un-baselined", section)
        self.assertNotIn("Every official source was re-checked", section)
        self.assertNotIn('git pull --rebase origin "$GITHUB_REF_NAME" || git rebase --abort', text)

    def run_publication_block(self, fail_rebase=False, fail_push=False):
        text = SOURCE_FACTS.read_text()
        # Exercise the actual workflow shell block with stubbed git/sleep; the
        # last line in the file is the surrounding workflow step's outer `fi`.
        tail = text.split("            published=false\n", 1)[1].splitlines()
        self.assertEqual("          fi", tail[-1])
        block = "published=false\n" + textwrap.dedent("\n".join(tail[:-1]))
        with tempfile.TemporaryDirectory() as d:
            calls = Path(d) / "calls"
            env = dict(os.environ, CALLS=str(calls), GITHUB_REF_NAME="main",
                       FAIL_REBASE="1" if fail_rebase else "0", FAIL_PUSH="1" if fail_push else "0")
            program = """set -euo pipefail
git() {
  echo "$1" >> "$CALLS"
  case "$1" in
    pull) [ "$FAIL_REBASE" = 0 ] ;;
    push) [ "$FAIL_PUSH" = 0 ] ;;
    *) return 0 ;;
  esac
}
sleep() { :; }
""" + block
            result = subprocess.run(["bash", "-c", program], cwd=d, env=env, capture_output=True, text=True)
            return result, calls.read_text().splitlines() if calls.exists() else []

    def test_snapshot_retry_succeeds_only_after_a_push(self):
        result, calls = self.run_publication_block()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(["pull", "push"], calls)

    def test_snapshot_failed_pushes_propagate(self):
        result, calls = self.run_publication_block(fail_push=True)
        self.assertNotEqual(0, result.returncode)
        self.assertEqual(["pull", "push"] * 3, calls)
        self.assertIn("All snapshot publication attempts failed", result.stderr)

    def test_snapshot_rebase_failure_does_not_try_to_push(self):
        result, calls = self.run_publication_block(fail_rebase=True)
        self.assertNotEqual(0, result.returncode)
        self.assertEqual(["pull"], calls)
        self.assertIn("Rebase failed", result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
