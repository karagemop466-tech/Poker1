# Suggestions for Site Improvement

The list is split into what has been built and what is still open. Everything under "Built" is live on
the site; everything under "Still open" is a proposal that has **not** been implemented.

## 1. Built in this session

| # | Suggestion | What was built | Where |
|---|---|---|---|
| S1 | Filter for "only events I can enter in my budget". | Buy-in range filter on every tournament table. | Filter bar on the single-entry, separate, unverified and venue pages |
| S3 | An "estimated cost of a trip" calculator. | **Trip cost = entries × buy-in + nights × true hotel cost**, plus parking and other spend, driven only by dated engine quotes. It also shows what the chosen stay window holds (verified single-entry events, days covered, cheapest buy-in, best guarantee ÷ buy-in), compares every logged quote like-for-like, and refuses to total anything it cannot source. | [Calculator](pages/calculator.html) |
| S4 | A status on each row. | Entry-rule chip on every row: single entry, possible multiple entries, re-entry, continuation, unverified. | All tournament tables |
| S5 | An automatic re-check of each official URL on a schedule. | `scripts/monitor_sources.py` checks every official URL daily, writes `data/monitoring.json`, compares every row with `data/row_snapshot.json`, and the workflow posts the result as an issue. | [Monitoring](pages/monitoring.html) and `.github/workflows/monitor.yml` |
| S6 | Read every structure sheet and remove the "unverified" label where the source allows. | All 37 DeepStack Extravaganza IV sheets and all 15 NYE sheets read, plus all eight Wynn WPT structure sections. The 20 milestone satellites that were missing are now published, and the Wynn WPT schedule is complete for Nov 27 – Dec 21. | `data/tournaments.json` |
| S7 | A "last checked" date on each row. | `verified_on` and `last_checked` on every row, hotel and rate entry. | All data files |
| S8 | Keep rates as a dated log, not a single value. | `data/rates.json` keeps each quote with its date, nights, nightly rates, taxes and true cost. The calculator uses the matching quote when the dates line up. | [Hotels](pages/hotels.html) and [Calculator](pages/calculator.html) |
| S9 | One page per venue. | A venues directory and a page per property, each with its hotels, walking records and events. | [Venues](pages/venues.html) |
| S10 | Keep the category pages. | Single entry, separate section and unverified pages are unchanged in purpose and now share one filter bar. | Navigation |
| S12 | A search box across all tables. | One search box over every tournament, hotel, venue, daily format, walking record, rate entry and document. | [Search](pages/search.html) |
| S14 | Put the build script in CI so the site cannot publish with a broken link or missing source. | The workflow rebuilds the data and the pages, fails on any diff, runs the schema and link checks, checks every official source, and renders every page in a headless DOM. | `.github/workflows/pages.yml` |
| S15 | Require a source URL on every new row. | Enforced by the generator and re-checked by `scripts/check_links.py`. | `scripts/build_data.py`, `scripts/check_links.py` |

New pages added with these: [Daily feed](pages/daily.html) for the recurring Wynn formats, and
[Monitoring](pages/monitoring.html) for source health and changed rows.

## 2. Still open

| # | Suggestion | Benefit | Cost / risk |
|---|---|---|---|
| S16 | Print-friendly views of the schedule and the single-entry list. | Useful on the trip without a phone. | Small effort; needs a print stylesheet and a page-break rule. |
| S17 | A drag-and-drop day planner. | Shows which events conflict on one day. | Overlap rules depend on real run times, which are not published. The schedule page already lists the overlaps it can detect. |
| S18 | Show the payout table for each event, not just the guarantee. | A guarantee is not the same as a payout ladder. | The structure sheets publish full ladders only for some events; the rest would stay blank. |
| S19 | Track the prize pool actually reached once an event finishes. | Shows how close a guarantee was. | Needs results, which the official pages publish as links only. |
| S20 | Verify walking times and store them. | **Done 2026-11-17** for all twelve pairs, from OpenStreetMap foot routing between geocoded coordinates, with the 30-minute rule applied and four pairs flagged as over it. | The open part is official confirmation: no property publishes its own walking time, so these remain routed, not published. |
| S21 | A per-property true cost for the MGM and Caesars properties. | Completes the hotel comparison. | Blocked on I7: eight candidate official URLs returned 404s or marketing pages with no fee (F47). Needs either a working fee page or a booking-engine breakdown for a specific stay. |
| S22 | Track several quoted rates for the same property on different dates. | **Partly done:** five dated quotes are logged and the calculator sorts them by true cost per night. | The reporting view is live; what is missing is repeat quotes on the *same* dates to show movement. |
| S23 | A weekly calendar of the daily formats across a whole trip. | See at a glance which nights have a format. | The daily page already shows the weekday map. A date-based version needs the trip dates. |

## 3. Proposed next, ranked by decision value

These are *not* implemented. Each one closes a specific gap in a decision you still have to make.

| # | Proposal | Gap it closes | Effort |
|---|---|---|---|
| P1 | Write one clear question list to the two poker rooms and the two reservation lines (walk-in single-entry policy, satellite end condition, registration opening, Venetian cancellation deadline). | D1, I1, I8, I10, I12, I14–I17, I9b — the largest remaining block is "only the operator can answer". | One email or call each; the draft questions are already written in `QUESTIONS.md`. |
| P2 | Add a booking-engine capture step for any stay date Wynn or the Venetian quotes, so a quote is never retyped. | Turns I6/I9 from one-off work into a repeatable dated log. | Medium: the engines render client-side, so it needs the same fetch-with-render path used on 2026-11-17. |
| P3 | Add an "effectively single entry" flag for multi-flight events whose structure sheet prices the second flight at the same amount and imposes no penalty. | D1 currently removes 60 rows from the ranking on an unanswered policy question. | Low: the clause text is already stored on every row. |
| P4 | Print the payout ladder where the sheet publishes one, and say "not published" explicitly where it does not. | S18 — a guarantee is not a payout ladder. | Low for the ~20 sheets that carry a ladder; nothing to do for the rest. |
| P5 | Publish an event-duration confidence column next to the estimated end time. | The overlap check rests on an estimate; a confidence label stops the estimate reading as fact. | Low: the inputs (levels × level length + breaks) are already parsed. |
| P6 | Publish the routed walking times as Google and Apple Maps links next to the OSM route, so the route can be checked in the app you would actually use. | Cross-checks the OSM route against the routing the user trusts. | Very low. |

## Your choice

Reply with the numbers you want from the "Still open" list. Nothing on that list changes until you choose.
