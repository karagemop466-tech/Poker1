# Las Vegas Strip Poker Plan

A source-verified plan for single-entry poker tournaments on the Las Vegas Strip and walkable hotels.
Snapshot date: **2026-11-16**.

Live site: https://karagemop466-tech.github.io/Poker1/

## What is in the site

| Page | Contents |
|---|---|
| `index.html` | Landing dashboard with counts and links. |
| `pages/single-entry.html` | The 50 verified single-entry events. Date filter, search, freezeout toggle, sortable columns. |
| `pages/separate-section.html` | 71 rows kept out of the ranking: multi-flight, re-entry and second-buy-in-implied events. |
| `pages/unverified.html` | 103 official rows whose entry rule is not yet confirmed. |
| `pages/venues.html` | One section per venue (Venetian, Wynn), with its series and row counts. |
| `pages/hotels.html` | Resort fee, room rate, tax, parking, cancellation, true cost, and the hotel→venue walking pairs with the 30-minute test. |
| `pages/schedule.html` | One primary event per day plus a conditional fallback, with overlaps flagged. |
| `pages/trip-cost.html` | Estimated trip cost: entries × buy-ins + nights × true cost per night. |
| `pages/changes.html` | Monitored official sources and any recorded change. |
| `pages/summary.html` | Executive summary. |
| `pages/questions.html` | Open decisions and information gaps, with how to close each. |
| `pages/suggestions.html` | Built improvements vs suggestions awaiting your choice. |
| `pages/flagged.html` | Irregularities and blank values, with source links. |
| `pages/review.html` | Line-by-line repo review, corrections, and the source log. |

## Data

`data/*.json` is generated. **Do not edit the JSON by hand.**

| File | Contents |
|---|---|
| `data/tournaments.json` | 224 rows: 50 single entry, 27 possible multi-entry, 35 re-entry, 9 second-buy-in implied, 103 unverified. |
| `data/hotels.json` | 7 hotels with resort fee, rate, tax, parking and cancellation status. |
| `data/schedule.json` | 34 days with a primary event, a conditional fallback where one exists, and overlap flags. |
| `data/walking.json` | 14 hotel→venue pairs with official addresses and the 30-minute limit. |
| `data/hotel_rates.json` | Dated rate log (schema documented; empty until a quote is captured). |
| `data/changelog.json` | 10 monitored official URLs and recorded changes. |

## Rules used

- **Only official sources.** Venue or operator domains only. Third-party sites are used to find events, never as a value source.
- **Nothing is inferred.** A value is recorded only when it is printed on an official source that was fetched and read. Otherwise the cell is blank and the item is flagged.
- **Single entry requires the structure sheet to be read**, and the sheet must show no re-entry, rebuy, add-on or flight clause. The Venetian sheets do not print an explicit "no re-entry" sentence, so the verdict is an absence-of-clause finding, recorded as question I1.
- **Multi-flight events are not single entry.** Their sheets restrict only players who bag chips for Day 2, so a bust-out re-entry stays possible.
- **Pool ÷ entry fee is descriptive, not a forecast.** It is a ratio of two published numbers. Bounty events are labelled, because their guarantee includes bounties.
- **True nightly cost** = `(room rate + resort fee) × (1 + tax%)`. It is computed only when a dated rate, a resort fee and a property-specific tax rate are all verified. The Venetian's 13.38% Clark County Room Tax is applied only to The Venetian.
- **Every row links to an official source**, and every structured rule field carries its own excerpt, URL and retrieval date.

## Rebuild and check

```
python3 scripts/build_data.py     # regenerate data/*.json
python3 scripts/build_site.py     # regenerate index.html and pages/*.html
python3 scripts/check_links.py    # JSON, local links, source hosts, rule fields
python3 scripts/check_sources.py  # re-check official sources and record changes
```

The Pages workflow (`.github/workflows/pages.yml`) runs the checks on every pull
request and after a push to `main`, and deploys `index.html`, `pages/`, `assets/`,
`data/` and the Markdown content files. It fails if the committed pages differ
from generated output.

`scripts/check_sources.py` runs daily from `.github/workflows/source-monitor.yml`
(07:00 UTC). It fetches each official URL, stores a checksum and opens an issue
when one changes. It never edits a value: a changed source is a signal to
re-verify that page line by line.

## Coordination

Parallel sessions: read `COORDINATION.md` **before** starting. Claim a task with
your session ID and file scope, commit and push the claim, and never start a task
another session has claimed.

**Note on branch history.** The repository's `main` branch and this session's
branch grew from unrelated histories (no common commit), so the two were joined
with `git merge --allow-unrelated-histories`. Where the two overlapped, this
session kept the more-verified dataset and adopted `main`'s stronger validator
(`scripts/check_links.py`). Five pages that `main` had added
(`venue-venetian.html`, `venue-wynn.html`, `venue-others.html`,
`trip-calculator.html`, `change-monitor.html`) were removed, because
`scripts/build_site.py` is the single generator: `venues.html`, `trip-cost.html`
and `changes.html` replace them, and leaving them would have shipped pages
carrying another session's inline script against a different data schema.

Documents: `EXECUTIVE_SUMMARY.md`, `QUESTIONS.md`, `SUGGESTIONS.md`, `FLAGGED.md`,
`REVIEW.md`, `COORDINATION.md`.

`archive/prior-main/` holds an earlier site from other sessions, kept for
reference. It is not published.
