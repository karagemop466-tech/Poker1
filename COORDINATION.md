# Coordination board

Current Arena session: `85820f64` on `arena/85820f64-poker1` (the workspace fixes the branch name).

| Task | Status | Owner | File scope | Notes |
|---|---|---|---|---|
| Evidence-first dashboard foundation and official venue directory | done | `arena/67733ec6-poker1` | `index.html`, `styles.css`, `app.js`, `README.md`, `COORDINATION.md` | Merged to `main` in PR #1; prior entry policy and source-directory work retained. |
| Official tournament / hotel research and decision findings | done | `85820f64` | `tournaments.html`, `hotels.html`, `decision.html`, `flagged.html` | Venetian and Wynn sources checked; unverified rules, dates and room totals remain blank/flagged. |
| Category dashboard and proposed site improvements | done | `85820f64` | `index.html`, `tournaments.html`, `hotels.html`, `decision.html`, `suggestions.html`, `flagged.html`, `styles.css` | Added executive summary, sourced tables, decision questions, suggestions and review flags. |
| Final integration, verification and GitHub Pages deployment | in progress | `85820f64` | `.github/**`, `scripts/**`, all site files | Rebased onto the previously merged PR; final checks, PR integration and deploy remain. |

## Coordination history and integration note

- Initial checkout at base commit `c16071b` contained a minimal `README.md` and no coordination board. This session claimed scopes on its fixed Arena branch and pushed the claim commit; at that moment no other claim was visible.
- During integration, fetched `origin/main` and found PR #1 from `arena/67733ec6-poker1` had merged after this branch's base. Its files overlapped `README.md`, `COORDINATION.md`, `index.html`, `styles.css`, and `.github/workflows/pages.yml`. Rebase conflicts occurred in these shared files. Resolution keeps the prior `app.js` official-source directory and evidence-first standards, combines both activity logs, and replaces the minimal one-page shell with the expanded requested category dashboard. The prior work remains in commit history and its reusable venue directory remains in `app.js`.
- Workspace constraint: work must remain on `arena/85820f64-poker1`; a separate `session-...` or integration branch cannot be created/switched to here. The fixed branch is used for integration.

## Sources and verification log

- 2026-11-16: Verified The Venetian's dedicated DeepStack Extravaganza IV schedule and linked official structure sheets for events #2, #6, #10, #12, #14, #24, #28, and #32; also checked its official poker room page, location, suite-rate terms, resort fee, and hotel contact page.
- 2026-11-16: Verified Wynn's official poker / WPT festival page, WPT schedule PDF, hotel booking details, and contact/address page. Checked ARIA's official poker page; it says to confirm whether daily tournaments are running, so no ARIA event is represented as scheduled in this snapshot.
- Key sources: [Venetian DeepStack IV schedule](https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html), [Venetian poker room](https://www.venetianlasvegas.com/resort/casino/poker.html), [Venetian poker suite rates](https://www.venetianlasvegas.com/resort/casino/poker/suite-rates.html), [Venetian resort fee](https://www.venetianlasvegas.com/resort/resort-fee.html), [Wynn official poker page](https://www.wynnlasvegas.com/casino/poker), [Wynn official WPT schedule PDF](https://cdn.wynnresorts.com/image/upload/v1757097329/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Schedule.pdf), [Wynn booking details](https://reservations.wynnlasvegas.com/ibe/details.aspx?propertyid=13763&rate=WEBONLY&nono=1), [ARIA poker page](https://aria.mgmresorts.com/en/casino/poker.html).
- Irregularities/open facts: (1) Venetian's general poker page still labels WPT Fall Festival (Oct 28–Nov 15) “Current Series” on the Nov 16 snapshot, while its dedicated series page lists DeepStack IV beginning Nov 16; dedicated schedule used, mismatch published on Flagged for Review. (2) reviewed structures do not explicitly establish a one-entry/no-re-entry limit for one-day candidates; strict confirmed single-entry count is zero. (3) exact hotel totals and walk-minute routes cannot be confirmed without stay dates, booking quotes, and route evidence. (4) Wynn WPT includes multiple flights, satellites and bounty formats; kept outside the strict candidates.
- Before final integration: `python3 scripts/check_site.py` passed (6 pages, 31 sourced table rows, local links resolve); `git diff --check` passed. Local preview started on port 4173.
- PR workflow run `43931316013` initially failed at the Pages artifact-upload step on the pull_request event, after the validator passed. Updated the workflow so PRs run validation only; the Pages artifact is staged/uploaded only in the main-branch deploy job. Re-run validation before merging and verify the actual Pages deploy afterward.

## Pull request / deployment

- Prior evidence-first dashboard PR #1 merged: https://github.com/karagemop466-tech/Poker1/pull/1
- Expanded dashboard PR #2: https://github.com/karagemop466-tech/Poker1/pull/2 (created before discovering PR #1 was merged; its base advanced and integration/rechecks are underway).
- GitHub Pages status is pending a successful final merge/deploy. Do not report the site live until the workflow confirms deployment.

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
| T7 | Final integration: merge, re-verify combined data, build/link check, PR, merge, Pages deploy check | in progress | e73e692a | all shared outputs (`index.html`, nav, merged table data) |

## Task log

### 2026-11-16 · session e73e692a
- Created this board. Claimed T1–T6 for session `e73e692a` on branch `arena/e73e692a-poker1`. T7 is reserved for this same session's final step.
- Repo at claim time: only `README.md` (`# Poker1`), one commit `c16071b Initial commit`, no existing claims, Pages already enabled (legacy, `main` `/`).
- T1–T6 completed on `arena/e73e692a-poker1`. Data rows were re-verified against the official Venetian schedule on 2026-11-16 (all 4 chunks). Flagged items (not blocking) are on `flagged.html`: Bellagio Saturday price conflict (IR-1), Wynn hotel offer conflict and dead official page, Caesars and Bellagio fees unverified, RWLV / MGM Grand / Aria poker pages unavailable, 16 Venetian structure sheets not read (events unranked).
- T7 claimed for session `e73e692a`. Integration will build `index.html` and nav, run link and JSON checks, open a PR into `main`, merge it, and record the PR link and merge result below.
