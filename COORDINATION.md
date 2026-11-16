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
