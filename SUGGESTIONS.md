# Suggestions for Site Improvement

The list is split into what has been built and what is still open. Everything under "Built" is live on
the site; everything under "Still open" is a proposal that has **not** been implemented.

## 1. Built in this session

| # | Suggestion | What was built | Where |
|---|---|---|---|
| S1 | Filter for "only events I can enter in my budget". | Buy-in range filter on every tournament table. | Filter bar on the single-entry, separate, unverified and venue pages |
| S3 | An "estimated cost of a trip" calculator. | Rate calculator: nights, room rate, resort fee, room tax, parking, tournament entries. It refuses to total anything that depends on an unverified figure and says which value is missing. | [Calculator](pages/calculator.html) |
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
| S20 | Verify walking times and store them. | Makes the 30-minute walk rule usable. | Needs a measured source per hotel-to-venue pair; the records are already in place and stay blank until then. |
| S21 | A per-property true cost for the MGM and Caesars properties. | Completes the hotel comparison. | Blocked on I7: the fee pages have not been read. |
| S22 | Track several quoted rates for the same property on different dates. | Shows price movement for the dates you care about. | Needs repeat checks; the rate log already stores every entry, so this is only a reporting view. |
| S23 | A weekly calendar of the daily formats across a whole trip. | See at a glance which nights have a format. | The daily page already shows the weekday map. A date-based version needs the trip dates. |

## Your choice

Reply with the numbers you want from the "Still open" list. Nothing on that list changes until you choose.
