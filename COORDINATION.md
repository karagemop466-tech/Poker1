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

## Pull request / deployment

- Prior evidence-first dashboard PR #1 merged: https://github.com/karagemop466-tech/Poker1/pull/1
- Expanded dashboard PR #2: https://github.com/karagemop466-tech/Poker1/pull/2 (created before discovering PR #1 was merged; its base advanced and integration/rechecks are underway).
- GitHub Pages status is pending a successful final merge/deploy. Do not report the site live until the workflow confirms deployment.
