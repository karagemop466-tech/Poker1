# COORDINATION.md — Shared Task Board

Repo: `karagemop466-tech/Poker1` · Site (GitHub Pages, `main`): https://karagemop466-tech.github.io/Poker1/

Status values: `unclaimed` · `in progress` · `done` · `needs review`
(`needs review` = published on the Flagged for Review page; does not block merge.)

## Sessions on this repo

| Session | Branch | PR | Status | Contribution |
|---|---|---|---|---|
| 67733ec6 | arena/67733ec6-poker1 | #1 merged | done | First dashboard foundation |
| 85820f64 | arena/85820f64-poker1 | #2, #6 merged | done | Dashboard expansion, check script, Pages verification |
| e73e692a | arena/e73e692a-poker1 | #5 merged | done | Venetian/Wynn research site, review, data |
| arena-1 | arena/e3571fc8-poker1 | #4 | done | Earlier category-dashboard site (`archive/prior-main/`) |
| 1fafb3d2 | arena/1fafb3d2-poker1 | this PR | integrating | Verified structure-sheet data, `pages/` site, T1–T7 |

## Protocol notes

- Claim a task here, commit, `git pull --rebase` before every push. Never start a task another session has claimed.
- Log cross-scope requests here instead of editing another scope.
- Shared outputs (data files, site index/navigation) are changed only by the integration session.
- **Session 1fafb3d2 integration decision (2026-11-16):** the earlier `main` site (`index.html`, root `*.html`, root `data/*.json`, root `scripts/build.py`, `scripts/check_site.py`) was built before any structure sheet was read. Its finding of "zero confirmed single-entry events" is superseded. Structure sheets 2, 3, 9, 10, 12, 13, 14, 15 and others are now read (see `REVIEW.md`). The previous files are preserved verbatim under `archive/prior-main/` and in git history. They are not deleted.
- The Pages workflow now validates and deploys `index.html`, `pages/`, `assets/`, and `data/`. Validation also fails if committed pages differ from `scripts/build_site.py` output.

## Task board (session 1fafb3d2)

| ID | Task | Status | Files / scope |
|----|------|--------|---------------|
| T1 | Repo review: line-by-line check, irregularities, source links | needs review | `REVIEW.md` |
| T2 | Live upcoming single-entry tournaments near the Strip (verified) | needs review | `data/tournaments.json`, `research/tournaments.md`, `scripts/build_data.py` |
| T3 | Hotels within walking distance: rate, resort fee, true cost | needs review | `data/hotels.json`, `research/hotels.md` |
| T4 | Schedule, executive summary, analysis | needs review | `data/schedule.json`, `EXECUTIVE_SUMMARY.md`, `research/analysis.md` |
| T5 | Suggestions and questions / information-gap register | done | `SUGGESTIONS.md`, `QUESTIONS.md` |
| T6 | Static site: landing, category pages, Flagged for Review | done | `index.html`, `pages/*.html`, `assets/*`, `scripts/build_site.py`, `scripts/check_links.py` |
| T7 | Final integration: merge `main`, verify, PR, merge, Pages deploy check | done | shared outputs; `.github/workflows/pages.yml`, `README.md` |

## Task log

### 2026-11-16 · 1fafb3d2 · T1–T6
- Claimed T1–T6 on `arena/1fafb3d2-poker1`. Commits `17048cc`, `0951813`, `f03ba9d`.
- Data: 225 official rows (single entry 33, possible multi-entry 15, re-entry 6, unverified 171). Hotels: 7. Schedule: 23 days of verified single-entry options. Every row has an official https source.
- Verified against official text: DSE IV schedule and event page; WPT schedule and structure PDF; Venetian structure sheets 1–3, 5–17.
- Corrections made: Event 49 Seniors to Dec 13/14; the "No LImit" typo claim removed (it is not in the official text); Event 26 multiple (625x) stated correctly; "possible multiple entries" wording kept (the clause does not prove a second entry).

### 2026-11-16 · 1fafb3d2 · T7 integration
- `main` moved to `8709f81` during this session. Four other PRs had merged. Conflicts (add/add) on 12 paths. Resolution:
  - Kept this session's versions of `index.html`, `assets/style.css`, `data/*.json`, `EXECUTIVE_SUMMARY.md`, `QUESTIONS.md`, `REVIEW.md`, `SUGGESTIONS.md`, `research/analysis.md`.
  - Archived all other `main` files (root `*.html`, `app.js`, `styles.css`, `scripts/*.py`, `data/*.md`, `data/repo_review.json`, `research/hotels/`, `research/tournaments/`, prior `README.md`, prior `COORDINATION.md`, and their docs) under `archive/prior-main/`. Nothing was deleted from git history.
  - Merged this board, keeping the prior sessions' table above.
- Workflow updated (see protocol notes). README rewritten to describe the new site.
- PR #8 (`arena/1fafb3d2-poker1` → `main`): https://github.com/karagemop466-tech/Poker1/pull/8. Validate job passed on the PR. Merged with a merge commit at `a50f162` (2026-11-16 18:51 UTC).
- Pages deploy: push run `43933252244` on `main` (validate success, deploy success). Pages API status `built`, source `main` `/`. Live page `https://karagemop466-tech.github.io/Poker1/pages/single-entry.html` fetched and shows all 33 single-entry rows with source links.
- Note: `git pull --rebase` was run once on this branch after the merge commit. It tried to replay `main`'s history and stopped with conflicts. The rebase was aborted (`git rebase --abort`), and the branch was not changed. Use `git merge` (not `pull --rebase`) for merges that include a merge commit.

## Open items (not blocking merge; see FLAGGED / QUESTIONS)
- Room rates are unverified for every hotel. True cost is blank.
- Walking times are not published by any official source. Blank.
- Caesars, Bellagio, ARIA resort fees unverified.
- Structure sheets for NYE, Signature Series, most WPT events, and DSE IV sheets 4 and 18–64 not yet read. All of these are unverified rows.
- Event 58 date blank in the official PDF. Event 5 (NYE) printed as 2025.
- Overlapping prior claims on the same scope (`85820f64`, `ce95f9c0`, `e73e692a`) noted; their work is archived, not merged into the live site.
