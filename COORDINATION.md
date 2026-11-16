# Coordination

## Working rules

- Current checkout: `arena/0c0423f8-poker1` (active). The session identifier below is taken from the Arena branch name because no separate session ID is exposed in the checkout.
- No other active task claims or parallel-session work were present in the repository when this board was created. This session will stay on the current Arena branch; it will not create or switch branches.
- Claims are committed and pushed before work starts. Shared site navigation, landing page, and final combined data are reserved for the integration task after the research tasks are complete.

## Task board

| ID | Task | Status | Owner | File scope |
|---|---|---|---|---|
| T-01 | Research live Las Vegas Strip-area poker tournaments; verify official schedule, format, entry/re-entry/add-on rules, price and posted prize-pool facts; record sources and uncertainties. | In progress | `0c0423f8` | `research/tournaments.md`, `data/tournaments.json`, this file for task log only |
| T-02 | Research official hotel nightly rates, dates, fees, total stay cost, and walk times to eligible venues. | Unclaimed | — | `research/hotels.md`, `data/hotels.json`, this file for task log only |
| T-03 | Build the dashboard/site, categorized pages, analysis, executive summary, questions, and Flagged for Review page using only verified inputs. | Unclaimed | — | `index.html`, `pages/`, `assets/`, site configuration, `README.md` |
| T-04 | Final integration and verification: validate every populated row's official link, run build/link checks, publish GitHub Pages, and report PR/deploy outcome. | Unclaimed | — | Shared site/data files only after T-01–T-03 are complete; this file for final log |

## Verification / handoff log

- Initial review: repository contained only `README.md`; no existing site, source data, or prior claims were present. No verification has yet been performed.
