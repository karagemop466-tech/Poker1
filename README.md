# Vegas Poker Planner

Static, evidence-first dashboard for planning Las Vegas Strip-area poker tournament trips. The public-facing dashboard is `index.html`; it can be hosted as a GitHub Pages static site from the repository root.

## Research status (November 16, 2026)
No tournament entries, hotel rates, resort-fee amounts, walking times, or all-in nightly prices are asserted as verified. The available search results did not provide event-specific confirmation from an official venue source. The dashboard therefore displays no confirmed events and leaves quote-dependent values blank rather than repeating third-party claims. Official venue/poker and property pages are linked in the dashboard as research starting points; source links alone do not establish a tournament schedule or fee.

## Method
- A confirmed event needs an official, current schedule or structure page that identifies the future event and date/time, buy-in, guarantee/prize information, and all entry mechanics.
- A strict single-entry candidate must have explicit official evidence that re-entry, re-buy, add-on, and extra bullets are not permitted. If terms are absent or ambiguous, classify as unverified and do not recommend it.
- Compare field guarantees and buy-in only as disclosed by the same event source. Guarantee-per-buy-in is not expected value, and a guarantee is not a predicted payout.
- Hotel totals require the user's exact dates and occupancy plus an official, bookable checkout quote. Compare room charges, mandatory resort/destination fees, applicable taxes, and mandatory charges, divided by nights. Report optional charges separately.
- Walking time is not populated without a verified route and venue entrance. The desired maximum is 30 minutes.
- Never schedule overlapping tournaments. Confirm late registration, start times, duration, breaks, and realistic transitions before proposing an all-day sequence.

## Files
- `index.html`: Dashboard sections: executive summary, tournament finder, day plan, hotel cost comparison, flagged questions, official source directory.
- `app.js`: Venue directory and empty event dataset. Rows are intentionally absent until official event-specific evidence is confirmed.
- `styles.css`: Responsive presentation.
- `COORDINATION.md`: Session work log, scope, evidence status, and deployment limitations.

## Hosting
Enable GitHub Pages for the `main` branch, repository root (`/(root)`). This is a static site with no build step. The repository's current branch workflow and Pages configuration need maintainer-level GitHub settings; no deployment is claimed by this deliverable.
