# Coordination

## Working rules

- Current checkout: `arena/0c0423f8-poker1` (active). The session identifier below is taken from the Arena branch name because no separate session ID is exposed in the checkout.
- No other active task claims or parallel-session work were present in the repository when this board was created. This session will stay on the current Arena branch; it will not create or switch branches.
- Claims are committed and pushed before work starts. Shared site navigation, landing page, and final combined data are reserved for the integration task after the research tasks are complete.

## Task board

| ID | Task | Status | Owner | File scope |
|---|---|---|---|---|
| T-01 | Research live Las Vegas Strip-area poker tournaments; verify official schedule, format, entry/re-entry/add-on rules, price and posted prize-pool facts; record sources and uncertainties. | Done | `0c0423f8` | `research/tournaments.md`, `data/tournaments.json`, this file for task log only |
| T-02 | Research official hotel nightly rates, dates, fees, total stay cost, and walk times to eligible venues. | Done | `0c0423f8` | `research/hotels.md`, `data/hotels.json`, this file for task log only |
| T-03 | Build the dashboard/site, categorized pages, analysis, executive summary, questions, and Flagged for Review page using only verified inputs. | Unclaimed | — | `index.html`, `pages/`, `assets/`, site configuration, `README.md` |
| T-04 | Final integration and verification: validate every populated row's official link, run build/link checks, publish GitHub Pages, and report PR/deploy outcome. | Unclaimed | — | Shared site/data files only after T-01–T-03 are complete; this file for final log |

## Verification / handoff log

- Initial review: repository contained only `README.md`; no existing site, source data, or prior claims were present.
- T-01 completed by `0c0423f8`. Source-by-source review completed on 2026-11-16 against official pages/structure documents from [The Venetian Resort](https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html), [Wynn Las Vegas](https://www.wynnlasvegas.com/casino/poker), [World Poker Tour](https://www.worldpokertour.com/event/main-tour-wpt-world-championship-at-wynn-las-vegas-season-2026), [MGM Grand](https://mgmgrand.mgmresorts.com/en/casino/poker-tables.html), [Caesars Entertainment](https://www.caesars.com/las-vegas/explore/casino/poker-tournaments-las-vegas-strip), and [ARIA](https://aria.mgmresorts.com/en/casino/poker.html). Detailed source links and event-level evidence are recorded beside every populated tournament row in `data/tournaments.json` and `research/tournaments.md`.
- T-01 verification: JSON parses; populated guarantee/buy-in ratios were mechanically checked; all schedule rows have official source links. Result: 0 confirmed strict single-entry events, 11 records with confirmed re-entry/add-on/paid-chip advantage, and 17 candidate events whose entry policy is not fully confirmed.
- T-01 irregularities flagged: Venetian event structures omit entry/re-entry/add-on rules for several events; MGM's current page links an August schedule PDF with no effective date and a time-precision mismatch, and its linked structure describes a voluntary gratuity/extra-chip option whose effect on total outlay needs confirmation; Caesars' dated article is not a current event-level calendar; ARIA does not publish detailed tournament terms on its current poker page. None of these were silently inferred.
- T-02 claim: `0c0423f8` — official hotel rates/fees/walk-time research; scope `research/hotels.md`, `data/hotels.json`, and this file for task log only. The claim was committed and pushed before research started.
- T-02 completed by `0c0423f8` on 2026-11-16. Added date-specific direct booking evidence and clearly separated quoted totals, nightly averages, illustrative tax estimates, conditional advertised poker-rate floors, and failed quote attempts. The four-night Dec 12-16, two-guest comparison remains provisional; the Dec 12-21 nine-night scenario is labeled supplemental. Walk estimates are source-linked and include the Resorts World–Venetian restricted-route warning. No hotel was booked. `data/hotels.json` parses and the room totals/tax illustrations were checked with Decimal arithmetic; `git diff --check` passed.
