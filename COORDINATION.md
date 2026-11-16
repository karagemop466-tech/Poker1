# Coordination board

Current Arena session: `85820f64` on `arena/85820f64-poker1` (branch name is fixed by the workspace).

| Task | Status | Owner | File scope | Notes |
|---|---|---|---|---|
| Evidence-first dashboard foundation and source directory | done | `arena/67733ec6-poker1` | `index.html`, `styles.css`, `app.js`, `README.md`, `COORDINATION.md` | Merged to `main` in PR #1. Original strict evidence policy and venue directory are retained; `app.js` remains in the repository. |
| Official tournament / hotel research and source-backed planning findings | done | `85820f64` | `tournaments.html`, `hotels.html`, `decision.html`, `flagged.html` | Venetian and Wynn sources checked; unverified rules, dates, and room totals remain flagged/blank. |
| Multi-page category dashboard and suggestions | done | `85820f64` | `index.html`, `tournaments.html`, `hotels.html`, `decision.html`, `suggestions.html`, `flagged.html`, `styles.css` | Subpages, executive summary, decision questions, suggestion backlog and flagged-review section completed. |
| Integration, source/link verification, GitHub Pages deployment | in progress | `85820f64` | `.github/**`, `scripts/**`, all site files | Rebased to include PR #1 work; run checks, resolve PR state, deploy after merge. |

## Coordination history and integration note

- Initial checkout at base commit `c16071b` contained only a minimal `README.md` and no coordination board. Current session claimed the available scopes and pushed the claim commit to the fixed Arena branch. At that time no other session claim was visible in this checkout.
- During integration, fetched `origin/main` and found PR #1 from `arena/67733ec6-poker1` had merged after this branch's base. Its dashboard and coordination files overlapped `README.md`, `COORDINATION.md`, `index.html`, `styles.css`, and `.github/workflows/pages.yml`. Rebase produced an add/add conflict in `COORDINATION.md`; resolution combines both session histories, preserves the prior evidence policy and `app.js`, and documents the expanded official research rather than discarding the other session's work.
- Branch workflow limitation: this workspace requires all work to remain on `arena/85820f64-poker1`; separate `session-...` branches and an independent integration branch cannot be created/switched to here. This branch is used as the integration/final delivery branch.

## Sources and verification log

- 2026-11-16: Verified the Venetian dedicated DeepStack Extravaganza IV schedule and linked official structure sheets for events #2, #6, #10, #12, #14, #24, #28, and #32; also checked its official poker room page, location, suite-rate conditions, resort fee, and hotel contacts.
- 2026-11-16: Verified Wynn's official poker / WPT festival page, official WPT schedule PDF, hotel booking details, and contact/address page. Checked ARIA's official poker page; it says to confirm whether daily tournaments are running, so no ARIA event is presented as scheduled/verified here.
- Verified key sources: [Venetian DeepStack IV schedule](https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html), [Venetian poker room](https://www.venetianlasvegas.com/resort/casino/poker.html), [Venetian poker suite rates](https://www.venetianlasvegas.com/resort/casino/poker/suite-rates.html), [Venetian resort fee](https://www.venetianlasvegas.com/resort/resort-fee.html), [Wynn official poker page](https://www.wynnlasvegas.com/casino/poker), [Wynn official WPT schedule PDF](https://cdn.wynnresorts.com/image/upload/v1757097329/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Schedule.pdf), [Wynn booking details](https://reservations.wynnlasvegas.com/ibe/details.aspx?propertyid=13763&rate=WEBONLY&nono=1), [ARIA poker page](https://aria.mgmresorts.com/en/casino/poker.html).
- Irregularities/open facts: (1) Venetian's general poker page still labels WPT Fall Festival (Oct 28–Nov 15) “Current Series” on the Nov 16 snapshot, while the dedicated series page lists DeepStack IV starting Nov 16; the dedicated schedule is used and the mismatch is on Flagged for Review. (2) reviewed structures do not explicitly establish a one-entry/no-re-entry limit for one-day events; confirmed strict single-entry count remains zero. (3) exact hotel totals and walking minutes cannot be confirmed without stay dates, actual booking quotes, and route evidence. (4) Wynn WPT includes multi-flight, satellite, and bounty formats, kept outside the strict candidate list.
- Local verification before integration: `python3 scripts/check_site.py` passed (six pages, 31 table body rows with official venue/operator source links, local links resolve); `git diff --check` passed. Local preview was started on port 4173.

## Pull request / deployment

- PR #1 from the prior session is merged: https://github.com/karagemop466-tech/Poker1/pull/1
- Current expanded dashboard PR #2: https://github.com/karagemop466-tech/Poker1/pull/2 (opened before detecting PR #1 had merged; branch now needs integration/rebase and checks).
- GitHub Pages deployment status: pending successful integration and merge; do not report live until deployment is verified.
