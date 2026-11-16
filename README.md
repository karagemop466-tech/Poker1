# Strip Poker Planner

A dependency-free, static dashboard for official-source Las Vegas poker tournament research, entry-policy screening, conditional day planning, and resort-fee comparison.

## Open locally

Serve the repository root over HTTP (the dashboard loads `data.json` with `fetch`, so opening `index.html` directly as a `file://` URL is not supported):

```sh
python3 -m http.server 8000 --bind 0.0.0.0
```

Then open `http://localhost:8000` locally, or use the Arena preview. The site has no package install or build step. `index.html`, `styles.css`, `app.js`, and `data.json` are the deployable site files.

## Research boundaries

- Snapshot date: **November 16, 2026**. Tournament schedules, room conditions, resort fees, availability, and prices can change; verify with the venue before entering or booking.
- Tournament and hotel claims use official venue/operator pages or structure sheets linked in the dashboard. The site does not scrape schedules automatically.
- **Strict single-entry** means one paid entry total for the whole tournament. “One entry per flight,” “1Day,” or a missing rule is not equivalent. Unverified or conflicting values are left blank and clearly flagged.
- The Dec 3–7, 2026 hotel comparison is an illustrative assumption (two adults, one standard room, four nights), not a confirmed trip request or a live booking quote. Fee-only subtotals are shown separately; no full-stay total was obtained.
- Walking minutes are not inferred from “same resort” or pedestrian bridges. Venue details are operator-published signals, not independent hotel-quality rankings.
- The 8 AM itinerary begins with planning because no live 8 AM tournament start was verified. Overlapping starts are alternatives; a later session is conditional on finishing/elimination and registration still being open.

## Updating the dashboard

1. Recheck the official schedule and the event's own structure/terms.
2. Update `data.json`; keep source URLs beside the values and retain a note for every unresolved conflict or missing entry rule.
3. Run the static checks (JSON parse and JavaScript syntax) and review the responsive page in a local browser.
4. Do not call an event strict single-entry unless an official source confirms one paid entry total.

The detailed research log, unresolved issues, and integration checklist are in [`COORDINATION.md`](./COORDINATION.md).
