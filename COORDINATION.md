# COORDINATION.md — Shared Task Board

Repo: `karagemop466-tech/Poker1` · Live site (GitHub Pages, served from `main` `/`): https://karagemop466-tech.github.io/Poker1/

Status values: `unclaimed` · `in progress` · `done` · `needs review`
(`needs review` = published on the Flagged for Review page; does not block anything.)

## Protocol notes

- Session branch note: the session protocol asks for `session-<id>/<task>` branches. This session is pinned to a single branch, `arena/e73e692a-poker1` (base `c16071b`, from `main`). All work for every task below is committed to that branch. No other branches are created or pushed.
- Session ID for this board: `e73e692a`.
- Only one session is active in this repo right now (confirmed: no other claims existed when this file was created). Tasks are still recorded per-task so any parallel session can see what is claimed.
- Shared outputs (table data, site index/navigation) are owned by the final integration task (T7).

## Task board

| ID | Task | Status | Owner (session) | Files / scope |
|----|------|--------|-----------------|---------------|
| T1 | Repo review: line-by-line check, irregularities, source links | in progress | e73e692a | `REVIEW.md`, `data/repo_review.json` |
| T2 | Find live upcoming single-entry poker tournaments near the Las Vegas Strip (verified) | in progress | e73e692a | `data/tournaments.json`, `research/tournaments/` |
| T3 | Hotels within walking distance: nightly rate, resort fees, true cost (verified) | in progress | e73e692a | `data/hotels.json`, `research/hotels/` |
| T4 | Schedule builder (8 AM all-day plan), executive summary, analysis | in progress | e73e692a | `data/schedule.json`, `EXECUTIVE_SUMMARY.md`, `research/analysis.md` |
| T5 | Suggestions for site improvement + Questions / Info-gap register | in progress | e73e692a | `SUGGESTIONS.md`, `QUESTIONS.md` |
| T6 | Static site: landing page, category subpages, Flagged for Review page | in progress | e73e692a | `index.html`, `pages/*.html`, `assets/*` |
| T7 | Final integration: merge, re-verify combined data, build/link check, PR, merge, Pages deploy check | unclaimed | — | all shared outputs |

## Task log

### 2026-11-16 · session e73e692a
- Created this board. Claimed T1–T6 for session `e73e692a` on branch `arena/e73e692a-poker1`. T7 is reserved for this same session's final step.
- Repo at claim time: only `README.md` (`# Poker1`), one commit `c16071b Initial commit`, no existing claims, Pages already enabled (legacy, `main` `/`).
