# Suggestions for Site Improvement

Two sections. **Section 1 is already built** in this session. **Section 2 is awaiting your choice** — nothing in Section 2 has been implemented, and nothing will be until you pick it.

---

## 1. Built this session (2026-11-16)

These came from your request list and are live on the site.

| # | Item | Where it lives | Benefit | Cost / risk |
|---|---|---|---|---|
| B1 | **Date selector** — filter any table to the days you choose. | Every tournament table, and the Schedule page | Shows only the events on your days. | None. Uses official dates only. |
| B2 | **Search box** across every table (event, series, note, source). | Every data table | Fast lookup in 224 rows. | None. |
| B3 | **"Single-entry / freezeout confirmed" toggle** on the tournaments table. | Single entry page | Hides everything that is not a confirmed freezeout. | Relies on absence-of-clause verdicts (I1). |
| B4 | **Structured rule fields** — single entry, re-entry, add-on and fee stored separately, each with its verbatim source excerpt, source URL and retrieval date. | Every row; rule columns on the tables | You can read the rule yourself without opening the PDF. | None. |
| B5 | **"Last checked" date** on every row. | Every row | Stale data is obvious. | None. |
| B6 | **Schedule with one primary event per day plus a conditional fallback**, and overlaps flagged. | Schedule page | No impossible sequences. | Finish times are not published (U11), so the check uses official registration windows. |
| B7 | **Walking-route check** — every hotel–venue pair with both official addresses and a ≤30-minute filter. | Hotels page | Applies your distance rule the moment a time is measured. | No official walking time exists yet, so all 14 pairs are blank and the filter returns nothing. |
| B8 | **Estimated cost of a trip calculator** — entries × buy-ins + nights × true cost per night. | Trip cost page | One total number for the trip. | The hotel half is blank until a rate is verified; values you type are labelled as yours. |
| B9 | **Hotel itemization fields** — checkout total, nightly average, mandatory resort fee, tax, parking, cancellation deadline and rate timestamp. | Hotels page; schema in `data/hotel_rates.json` | Lets you compare stays like for like. | All blank until a dated quote is captured. |
| B10 | **Rates kept as a dated log**, not a single value. | `data/hotel_rates.json`, described on the Hotels page | Shows price movement across your stay window. | Empty until quotes are captured. |
| B11 | **One page per venue** (Venetian, Wynn), each with its series, row counts and hotels. | Venues page | Easier to plan by location. | Duplicates a little data. |
| B12 | **Automatic re-check of every official URL on a schedule**, flagging what changed. | `.github/workflows/source-monitor.yml`, `scripts/check_sources.py`, Change log page | Catches schedule changes without you watching. | Detects change; it does not re-verify values. A changed source means a human re-reads it. |
| B13 | **Read every structure sheet** to remove the "unverified" label where confirmed. | All rows | Verified single-entry events went from **33 to 50**. | Venetian DSE IV is complete (25 of 25 non-satellite sheets). NYE and Wynn are partial — see Section 2, N1. |
| B14 | **Ranking discipline** — rank only after confirming the total entry fee and the guarantee; show pool ÷ fee as a descriptive ratio, not a forecast; label bounty and multi-flight events separately. | Single entry page, Executive summary | Stops the ratio being read as a prediction. | None. |
| B15 | **Shared `COORDINATION.md` on `main`** before parallel sessions start. | `COORDINATION.md` | Avoids two sessions editing the same file. | Needs each session to claim before it edits. |

### Two things you asked for that were built differently, on purpose

- **"Live hotel rate lookup."** No Strip hotel publishes a public rate API, and capturing rates automatically from a booking engine means scraping a third party and re-publishing it, which would put unverified numbers on a site whose rule is that only official values appear. Instead the site stores the *official* booking link per hotel and a **dated rate log** with the exact fields you asked for (B9, B10). Fill that log from the official page for your dates and the true-cost figure appears automatically.
- **"A live feed or scraper that pulls each room's daily schedule."** Built as **change detection** (B12): the job fetches each official page daily, checksums it, and opens an issue when something changes — but it does not copy or republish venue content. When a change is flagged, the rows sourced from that page are re-read line by line against the official page. That keeps the no-hallucination rule intact.

---

## 2. Awaiting your choice — nothing here is built

Reply with the numbers you want (for example "N1, N3, N6"). Nothing changes until you choose.

### Decision support

| # | Suggestion | Benefit | Cost / risk |
|---|---|---|---|
| N1 | **Finish the structure-sheet reading**: Venetian NYE sheets 3, 6, 8, 9, 10, 11, 12, 13, 14, 15; find the Wynn Signature Series structures; find the missing WPT event structures. | Would clear most of the remaining 103 unverified rows; the single largest gain in confidence. | Needs the documents to exist and be reachable. 51 WPT rows have no official per-event structures document that could be found (F13). |
| N2 | **Buy-in cap / budget filter** ("only events inside my budget"). | Faster shortlist. | Needs your budget (D3). |
| N3 | **Day planner** — pick a primary and a fallback per day and see the resulting itinerary, with overlaps marked. | Turns the schedule into a plan you can print. | Depends on real run times, which are not published (U11). |
| N4 | **Traffic-light status per row** (verified / partially verified / unverified). | Gaps obvious at a glance. | Small effort. Status chips already exist but are not a single traffic light. |
| N5 | **Hotel ranking once you fix dates and a quality floor.** | Answers "which hotel" directly. | Needs D4 and D5, and at least one dated rate per hotel. |
| N6 | **Print-friendly views** of the schedule and the trip cost. | Useful on the trip. | Small effort. |
| N7 | **Export to CSV / ICS calendar** for the events you selected. | Put the plan in your phone. | Small effort. |

### Data quality

| # | Suggestion | Benefit | Cost / risk |
|---|---|---|---|
| N8 | **Capture dated official hotel quotes** for your stay window and fill the rate log. | Unblocks the true-cost figure and the hotel ranking. | Needs your dates (D4). Must be done by hand against the official booking pages. |
| N9 | **Measure and record the 14 walking routes.** | Activates the 30-minute filter and the distance ranking. | Measured estimates, not official figures; must be labelled and dated. |
| N10 | **Ask the poker rooms the open questions** and record the answers as a dated, attributed note (D1, D2, I1, I7, I9, I10, I11, I12). | Would resolve the 27 multi-flight rows and the "is silence a guarantee" question. | Needs a phone call; answers are not official documents. |
| N11 | **Add the WSOP Circuit and Planet Hollywood series** if official schedules appear. | Wider coverage. | No verified 2027 Las Vegas Circuit schedule exists yet (U12). |

### Process

| # | Suggestion | Benefit | Cost / risk |
|---|---|---|---|
| N12 | **Run the build in CI and block merges when committed pages differ from generated pages.** | Stops a hand-edited page being published. | Already partly in place: the Pages workflow fails if `build_site.py` output differs. Extend it to block the merge, not just warn. |
| N13 | **Require a "changed because" note on any row whose value is edited.** | Traceability for every number. | Small effort. |
| N14 | **Archive superseded snapshots** of the official PDFs so a later dispute can be checked against what the page said on a given date. | Strong audit trail. | Storage; PDFs are large. |
