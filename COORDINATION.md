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
| T1 | Repo review: line-by-line check, irregularities, source links | done | e73e692a | `REVIEW.md`, `data/repo_review.json`, `pages/review.html` |
| T2 | Find live upcoming single-entry poker tournaments near the Las Vegas Strip (verified) | done | e73e692a | `data/tournaments.json`, `research/tournaments/`, `pages/tournaments.html`, `pages/excluded.html` |
| T3 | Hotels within walking distance: nightly rate, resort fees, true cost (verified) | done | e73e692a | `data/hotels.json`, `research/hotels/`, `pages/hotels.html` |
| T4 | Schedule builder (8 AM all-day plan), executive summary, analysis | done | e73e692a | `data/schedule.json`, `EXECUTIVE_SUMMARY.md`, `research/analysis.md`, `pages/schedule.html` |
| T5 | Suggestions for site improvement + Questions / Info-gap register | done | e73e692a | `SUGGESTIONS.md`, `QUESTIONS.md` |
| T6 | Static site: landing page, category subpages, Flagged for Review page | done | e73e692a | `assets/style.css`, `pages/*.html` (index and nav reserved for T7) |
| T7 | Final integration: merge, re-verify combined data, build/link check, PR, merge, Pages deploy check | in progress | e73e692a | all shared outputs (`index.html`, nav, merged table data) |

## Task log

### 2026-11-16 · session e73e692a
- Created this board. Claimed T1–T6 for session `e73e692a` on branch `arena/e73e692a-poker1`. T7 is reserved for this same session's final step.
- Repo at claim time: only `README.md` (`# Poker1`), one commit `c16071b Initial commit`, no existing claims, Pages already enabled (legacy, `main` `/`).
- T1–T6 completed on `arena/e73e692a-poker1`. Data rows were re-verified against the official Venetian schedule on 2026-11-16 (all 4 chunks). Flagged items (not blocking) are on `pages/flagged.html`: Bellagio Saturday price conflict (IR-1), Wynn hotel offer conflict and dead official page, Caesars and Bellagio fees unverified, RWLV / MGM Grand / Aria poker pages unavailable, 16 Venetian structure sheets not read (events unranked).
- T7 claimed for session `e73e692a`. Integration will build `index.html` and nav, run link and JSON checks, open a PR into `main`, merge it, and record the PR link and merge result below.
