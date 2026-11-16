# Repository review

A line-by-line review of what was in this repository, what was wrong, and what changed. The review is kept
because the corrections are as much a part of the deliverable as the data.

## What the repository looked like before this pass

| File | State found | Problem |
|---|---|---|
| `data/tournaments.json` | 225 rows | Only the November Venetian sheets had been read. 171 rows were unverified, and the NYE series was absent entirely. |
| `data/hotels.json` | 7 hotels | Resort fees were blank for Bellagio, ARIA and Caesars. No tax computation, no parking, no cancellation terms, no occupancy. |
| `data/schedule.json` | 23 days | Ran only through early December. Each day had one event with no fallback. |
| `data/walking.json` | Absent | The Hotels page had a line stating walking times are blank because no official source publishes one. |
| `data/hotel_rates.json` | Absent | No rate log existed, so no dated comparison was possible even in principle. |
| `data/venues.json` | Absent | Venues had no pages of their own. |
| `data/source_registry.json` | Absent | Source URLs were scattered through the code with no machine-readable register. |
| `data/daily_feed.json` | Absent | No daily inventory at all. |
| `scripts/build_site.py` | 11 pages | No venue pages, no cost calculator, no rate log, no source page, no irregularity page. |
| `assets/app.js` | Tables and Markdown | No date filter, no format filter, no walk filter, no interactive cost model. |

## Corrections made

**1. The house fee was being double-counted.**
`brief()` computed `total_fee_usd` as `buy_in_usd + house_fee_usd`. That is wrong. Every official structure sheet
read here withholds the fee from the buy-in. The Venetian prints it explicitly: "$58 of the $300 Buy-In is
withheld for house fees (Rake + Staff). The prize pool consists of $242 of every $300 Buy In." Adding the fee to
the buy-in overstated the cost of every event by 8% to 20%. The field is now the buy-in, and a
`fee_component_of_buy_in` flag records why.

**2. Two Bellagio prize pools were derived instead of read.**
`prize_pool_usd` was computed as `buy - fee`. For Bellagio Friday that gave $550 against the $510 the official
sheet prints, and for Sunday it gave $365 against the printed $340. The difference is the voluntary staff
gratuity, which is neither pool nor house fee. The `BELLAGIO` table now carries the printed pool as its own
column and the derivation is gone.

**3. The section boundary used the wrong criterion.**
An earlier version put bounty, satellite, milestone and team formats in the separate section. That is a
different question from the one the section asks. A $260 milestone satellite takes exactly one entry, and
excluding it from a section titled "single entry" was a category error. The section now turns only on whether
the structure sheet allows more than one entry. Prize structure became a filter, and the 80 single-entry rows
split 22 plain freezeouts and 58 bounty, satellite or team formats.

**4. The schedule covered 23 days with no fallback.**
It now covers all 52 dates in the plan, 44 with a conditional fallback. The overlap test uses the printed
late-registration cutoff — the last moment a second entry can be taken — rather than a guessed finish time.
Where a date genuinely has no non-overlapping alternative, the page says so instead of implying one exists.

**5. The Hotels page said walking times were unknowable.**
That was true of official sources and false as a statement about the world. All 42 hotel-to-venue pairs are now
computed with one OpenStreetMap pedestrian routing request over the official addresses, each with Google Maps
and Apple Maps links attached. The figures are labelled computed rather than quoted, because that is what they
are.

**6. Caesars' fee was implied by an empty cell.**
A blank resort fee read as "no fee" rather than "not verified". It is now explicitly `$54.95, secondary source`
with the official Caesars page linked beside it, so the provenance of the number is visible wherever it appears.

**7. The daily poker-room inventory was missing entirely.**
The eight daily formats across Wynn and Bellagio are now published with their exact fee allocations, stack
sizes, registration cutoffs and — importantly — the Wynn language that each daily "may be suspended during
Seniors Events, Classic Events, or other Tournament Series."

**8. Nothing watched the sources.**
An official document could change without the site noticing. `scripts/monitor_sources.py` now fetches all 76
registered URLs, hashes each body and compares it with a baseline. A changed document is flagged. A fetch
failure is reported as a failure, never as unchanged.

## Verification

The build does not rely on trust:

- `scripts/check_links.py` fails the build if a JSON file is missing, if a row lacks an https source, if a
  source host is not on the approved list, if a row in the single-entry section is not actually single entry, if
  a single-entry row lacks a confirmed total fee, if a schedule day has no primary, or if any hotel-to-venue
  walking pair is missing. It also checks every local link and rejects external asset references.
- The Pages workflow regenerates the site and runs `git diff --exit-code` against the committed pages, so a
  generated page that does not match its generator fails CI.
- The refresh workflow re-runs the daily scrape and the source watch every morning at 05:10 UTC and commits only
  when something changed.

## What is still not right, and is not hidden

| Item | Why it remains |
|---|---|
| 93 unverified Wynn rows | The WPT structures PDF truncates and the Signature structures are a placeholder. |
| No room rate anywhere | Every booking engine is a JavaScript application. |
| Six unresolved contradictions | Reproduced on the Irregularity log rather than silently resolved. |
| No projected finish times | No official source publishes one, for any event, anywhere. |

## Reading order for a reviewer

1. **Executive summary** — the findings and the recommended trip shape.
2. **Flagged for review** — every blank, with the reason.
3. **Irregularity log** — the contradictions in the official documents themselves.
4. **Official sources** — every URL the plan depends on, with a change status.
5. **Questions** — what is answered, what is open, and what only you can decide.
