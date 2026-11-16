# Coordination board

Current Arena session: `85820f64` on the fixed branch `arena/85820f64-poker1`.

| Task | Status | Owner | Scope | Result |
|---|---|---|---|---|
| Evidence-first dashboard foundation and official venue directory | done | `arena/67733ec6-poker1` | `index.html`, `styles.css`, `app.js`, `README.md`, `COORDINATION.md` | Integrated through PR #1; source directory and evidence-first policy retained. |
| Official tournament / hotel research and decision findings | done | `85820f64` | `tournaments.html`, `hotels.html`, `decision.html`, `flagged.html` | Official Venetian/Wynn facts linked; unknown values remain blank and flagged. |
| Category dashboard, executive summary and suggestions | done | `85820f64` | All HTML pages and `styles.css` | Published sourced tables, decision questions, suggestions, and review flags. |
| Integration, validation and GitHub Pages deployment | done | `85820f64` | `.github/**`, `scripts/**`, all site files | PR #2 merged; required validation passed; Pages deployment succeeded. |

## Coordination and integration history

- Initial checkout at base `c16071b` contained only a minimal `README.md` and no `COORDINATION.md`. This session claimed available scopes on its fixed Arena branch and pushed the claim. At that time no other claim was visible.
- During integration, `origin/main` had advanced through PR #1 from `arena/67733ec6-poker1`. Shared-file conflicts occurred in `README.md`, `COORDINATION.md`, `index.html`, `styles.css`, and the Pages workflow. Resolution retained PR #1's `app.js` official-source directory and source-first policy while integrating the requested multi-page dashboard; no other session's work was silently removed.
- This workspace requires all work to remain on `arena/85820f64-poker1`; a separate `session-...` or integration branch could not be created/switched to here. The fixed branch was used for final integration.

## Sources checked (2026-11-16)

- The Venetian's dedicated DeepStack Extravaganza IV schedule and official structure PDFs for events #2, #6, #10, #12, #14, #24, #28, and #32; official poker-room location, poker suite-rate terms, resort fee, and contact page.
- Wynn's official poker / WPT festival page, WPT schedule PDF, date-dependent hotel booking details, and contact/address page.
- ARIA's official poker page checked; it directs players to verify whether its daily tournaments are running, so no specific ARIA event is claimed as scheduled.
- Links: [Venetian DeepStack IV schedule](https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html), [Venetian poker room](https://www.venetianlasvegas.com/resort/casino/poker.html), [Venetian poker suite rates](https://www.venetianlasvegas.com/resort/casino/poker/suite-rates.html), [Venetian resort fee](https://www.venetianlasvegas.com/resort/resort-fee.html), [Wynn poker / WPT page](https://www.wynnlasvegas.com/casino/poker), [Wynn WPT schedule PDF](https://cdn.wynnresorts.com/image/upload/v1757097329/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Schedule.pdf), [Wynn booking details](https://reservations.wynnlasvegas.com/ibe/details.aspx?propertyid=13763&rate=WEBONLY&nono=1), [ARIA poker page](https://aria.mgmresorts.com/en/casino/poker.html).

## Verification and irregularities

- `python3 scripts/check_site.py` passed: six pages, 31 table-body rows each with an official venue/operator link, and all local links resolve. `git diff --check` passed. The PR validation job also succeeded.
- Single-entry policy: reviewed event structures do not explicitly set a one-entry/no-re-entry limit for the one-day candidates. Strict confirmed single-entry count is zero; these are candidates only.
- Hotel totals and walking-minute route values remain unverified because dates, occupancy, live quote, and route evidence are absent. Room prices/totals are blank.
- Venetian general poker page still labels WPT Fall Festival (Oct 28–Nov 15) “Current Series” on the Nov 16 snapshot while the dedicated DeepStack IV page starts Nov 16. Dedicated schedule used; mismatch is published on Flagged for Review.
- Wynn WPT includes multiple-flight, satellite, and bounty formats; these are kept separate from the strict shortlist.
- Workflow run `43931316013` initially failed at Pages artifact upload on a pull-request event; workflow was corrected so PRs validate only and the artifact is created in the main-branch deployment job. Subsequent PR validation and deployment both succeeded.

## Pull request and deployment result

- PR #1 (evidence-first dashboard): https://github.com/karagemop466-tech/Poker1/pull/1 — merged.
- PR #2 (expanded research dashboard): https://github.com/karagemop466-tech/Poker1/pull/2 — merged at `64498f883a2d619d7023ab7b14e402ec2f315510` on 2026-11-16.
- Successful Pages workflow run: https://github.com/karagemop466-tech/Poker1/actions/runs/43931551346
- Published site: https://karagemop466-tech.github.io/Poker1/

---

## Session e73e692a board (Venetian / Wynn / Bellagio research site)

Branch `arena/e73e692a-poker1`. Tasks T1–T7 are claimed and tracked here; shared outputs (index, nav, table data) are integrated in T7.

### Task board (e73e692a)

| ID | Task | Status | Owner (session) | Files / scope |
|----|------|--------|-----------------|---------------|
| T1 | Repo review: line-by-line check, irregularities, source links | done | e73e692a | `REVIEW.md`, `data/repo_review.json`, `review.html` |
| T2 | Find live upcoming single-entry poker tournaments near the Las Vegas Strip (verified) | done | e73e692a | `data/tournaments.json`, `research/tournaments/`, `tournaments.html`, `pages/excluded.html` |
| T3 | Hotels within walking distance: nightly rate, resort fees, true cost (verified) | done | e73e692a | `data/hotels.json`, `research/hotels/`, `pages/hotels.html` |
| T4 | Schedule builder (8 AM all-day plan), executive summary, analysis | done | e73e692a | `data/schedule.json`, `EXECUTIVE_SUMMARY.md`, `research/analysis.md`, `pages/schedule.html` |
| T5 | Suggestions for site improvement + Questions / Info-gap register | done | e73e692a | `SUGGESTIONS.md`, `QUESTIONS.md` |
| T6 | Static site: landing page, category subpages, Flagged for Review page | done | e73e692a | `assets/style.css`, `pages/*.html` (index and nav reserved for T7) |
| T7 | Final integration: merge, re-verify combined data, build/link check, PR, merge, Pages deploy check | done | e73e692a | all shared outputs (`index.html`, nav, merged table data, `.github/workflows/pages.yml`) |

## Task log

### 2026-11-16 · session e73e692a
- Created this board. Claimed T1–T6 for session `e73e692a` on branch `arena/e73e692a-poker1`. T7 is reserved for this same session's final step.
- Repo at claim time: only `README.md` (`# Poker1`), one commit `c16071b Initial commit`, no existing claims, Pages already enabled (legacy, `main` `/`).
- T1–T6 completed on `arena/e73e692a-poker1`. Data rows were re-verified against the official Venetian schedule on 2026-11-16 (all 4 chunks). Flagged items (not blocking) are on `flagged.html`: Bellagio Saturday price conflict (IR-1), Wynn hotel offer conflict and dead official page, Caesars and Bellagio fees unverified, RWLV / MGM Grand / Aria poker pages unavailable, 16 Venetian structure sheets not read (events unranked).
- T7 claimed for session `e73e692a`. Integration will build `index.html` and nav, run link and JSON checks, open a PR into `main`, merge it, and record the PR link and merge result below.

### Integration record (e73e692a, T7)

- Integration merged `origin/main` (PR #1, #2 and claim PR #6 from other sessions) into `arena/e73e692a-poker1`. Conflicts resolved: `index.html` replaced by the new dashboard index; `scripts/check_site.py` kept as the other session's validator (allowed hosts extended for Bellagio, Caesars, RWLV and MGM Grand official pages); our checker is `scripts/check_site_integration.py`; `COORDINATION.md` combined (both boards kept). Other session's `decision.html`, `suggestions.html`, `styles.css`, `app.js` kept and linked from our nav.
- Pages now serves a flat root site: `index.html`, `tournaments.html`, `excluded.html`, `hotels.html`, `schedule.html`, `flagged.html`, `review.html`, plus `assets/` and `data/`. Workflow staging updated to copy these.
- Both validators passed before merge: `python3 scripts/check_site.py` (6 pages, 74 sourced table rows) and `python3 scripts/check_site_integration.py` (7 generated pages, 47 candidate, 16 excluded, 136 unranked rows, all with official links).
- Pull request: https://github.com/karagemop466-tech/Poker1/pull/5 (`arena/e73e692a-poker1` into `main`).
- Merge result: MERGED at 2026-11-16T18:45:55Z, merge commit `529570fb900a7e0a082713d4089db0f569541fd9`, merged with a merge commit (no approval wait; no `--auto`).
- Pages deploy: run 43932265271 on `main` at 529570f: validate success, deploy success. Live check: https://karagemop466-tech.github.io/Poker1/tournaments.html returns the new single-entry candidates page.
- This record is committed on `arena/e73e692a-poker1` after the merge, so it is not on `main`. Record-only change; no site content depends on it.
- Open flags (non-blocking, see `flagged.html`): explicit single-entry wording not found on structure sheets (strict count 0); Bellagio Saturday price conflict; Wynn hotel fee conflict; Caesars and Bellagio fees unverified; walking times unverified; 16 Venetian structure sheets not read.

