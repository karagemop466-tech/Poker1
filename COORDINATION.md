# COORDINATION.md — Shared Task Board

Repo: `karagemop466-tech/Poker1` · Live site (GitHub Pages, served from `main` `/`): https://karagemop466-tech.github.io/Poker1/

Status values: `unclaimed` · `in progress` · `done` · `needs review`
(`needs review` = published on the Flagged for Review page; does not block anything.)

## Protocol notes

- **Branch pinned by the workspace:** this session works only on `arena/1fafb3d2-poker1` (base `c16071b`, from `main`). Work is not pushed to any other branch. The `session-<id>/<task>` naming in the protocol cannot be used in this workspace.
- **Session ID for this board:** `1fafb3d2`.
- **Overlapping sessions found at claim time (read-only check of remote branches):**
  - `arena/85820f64-poker1` — claimed research, dashboard, integration (commit `a1cb63d`).
  - `arena/ce95f9c0-poker1` — claimed end-to-end work (commit `8fadf66`).
  - `arena/e73e692a-poker1` — claimed T1–T7 (commit `d31f2f2`).
  None of these claims are on `main`. This session did **not** edit any file on those branches. Because the same scope is claimed in several places, the final merge to `main` may conflict with other sessions' pushes. This is logged as an open coordination risk (see Task log).
- Shared outputs (table data, site index/navigation) are owned by the final integration task (T7), which this session runs at the end.

## Task board

| ID | Task | Status | Owner (session) | Files / scope |
|----|------|--------|-----------------|---------------|
| T1 | Repo review: line-by-line check, irregularities, source links | in progress | 1fafb3d2 | `REVIEW.md` |
| T2 | Live upcoming single-entry tournaments near the Las Vegas Strip (verified) | in progress | 1fafb3d2 | `data/tournaments.json`, `research/tournaments.md` |
| T3 | Hotels within walking distance: rate, resort fee, true cost (verified) | in progress | 1fafb3d2 | `data/hotels.json`, `research/hotels.md` |
| T4 | Schedule builder (8 AM all-day plan), executive summary, analysis | in progress | 1fafb3d2 | `data/schedule.json`, `EXECUTIVE_SUMMARY.md`, `research/analysis.md` |
| T5 | Suggestions for site improvement + Questions / information-gap register | in progress | 1fafb3d2 | `SUGGESTIONS.md`, `QUESTIONS.md` |
| T6 | Static site: landing page, category pages, Flagged for Review page | in progress | 1fafb3d2 | `index.html`, `pages/*.html`, `assets/*` |
| T7 | Final integration: build/link check, PR to `main`, merge, Pages deploy check | unclaimed | — | all shared outputs |

## Task log

### 2026-11-16 · session 1fafb3d2
- Read `main` (only `README.md`, `c16071b`). `COORDINATION.md` did not exist on `main`. Pages is enabled (legacy, `main` `/`).
- Found the three overlapping claims listed above on their own branches. Did not edit them.
- Claimed T1–T6 on `arena/1fafb3d2-poker1`. T7 is reserved for this session's final step.
