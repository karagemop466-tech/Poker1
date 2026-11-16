# Vegas Poker Planner

A source-linked static dashboard for planning Las Vegas Strip-area poker tournaments and hotel stays. Research snapshot: **November 16, 2026**.

## Current finding

Two official upcoming series are listed: The Venetian DeepStack Extravaganza IV (Nov 16–Dec 23, 2026) and Wynn's WPT World Championship (Nov 27–Dec 21, 2026). The strict single-entry result remains **zero confirmed events** because the reviewed official structures do not explicitly establish a one-entry/no-re-entry limit for the one-day candidates. Those events are shown as unverified candidates—not as single-entry recommendations. Exact hotel totals are blank because trip dates and occupancy are unknown.

The source-first rule from the initial dashboard remains in effect: an event belongs in the strict shortlist only when the official schedule/structure identifies it and its entry rules explicitly rule out re-entry, re-buy, add-on, and extra bullets. “One day” is not equivalent to “single entry.” Guarantees divided by buy-in are shown only as arithmetic screening comparisons, never as expected value.

## Dashboard pages

- `index.html` — executive summary and decision status
- `tournaments.html` — Venetian event candidates, Wynn multi-flight leads, and entry-rule caveats
- `hotels.html` — official resort fees, conditional poker rates, and blank date-dependent true nightly totals
- `decision.html` — unresolved questions and provisional path
- `suggestions.html` — site improvement options, separate from implementation
- `flagged.html` — unverified values and source irregularities

## Research limits

This is a dated, source-verified snapshot, not a reservation or entry guarantee and not a comprehensive event census of every Strip-area poker room. ARIA's official poker page directs readers to confirm whether daily tournaments are running; other rooms are retained as official source-directory links in `app.js` but are not represented as having verified future events in this snapshot. Unconfirmed event rules, prices, fees, and walking times are left blank and flagged.

Hotel comparisons require exact stay dates, occupancy, room type, live operator quotes, mandatory resort/destination fees, applicable taxes, and cancellation terms. Walk times require route evidence and actual entrances. No unsupported value is inferred. Confirm current information directly with operators before paying.

## Verification and hosting

Run `python3 scripts/check_site.py` to verify required site pages, local links, and at least one official venue/operator source on every table row. The GitHub Actions workflow in `.github/workflows/pages.yml` checks pull requests and publishes the site root to GitHub Pages after pushes to `main`. GitHub Pages must permit GitHub Actions deployments.

## Retained starter research

`app.js` retains the initial official poker/property source directory and its no-event-unless-officially-verified rule from the prior evidence-first dashboard. It is retained for later venue expansion; the current multi-page tables contain the reviewed event-specific records.
