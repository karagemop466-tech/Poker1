# COORDINATION.md

Shared task board for the Las Vegas Strip poker tournament and hotel planner.

## Current session and task claim

Session `f0143c13` is working on branch `arena/f0143c13-poker1` (the branch is fixed for this session). Claim commit `cc17d9e` was pushed before implementation work.

Session `arena/f5896c06-poker1` is working on branch `arena/f5896c06-poker1`. Integration commit `3241bb8` was pushed and opened as PR #13; rebased onto `b272ed5` and merged into main.

| Task | Status | File scope | Owner |
|---|---|---|---|
| Repair GitHub Pages deployment of the Markdown-backed dashboard pages; add checks for deployed content and official source domains; correct incorrect summary metadata; record the review/deploy result | Merged (PR #11) | `.github/workflows/pages.yml`, `scripts/check_links.py`, `README.md`, `EXECUTIVE_SUMMARY.md`, `COORDINATION.md` | `f0143c13` |
| Final integration: repo re-review, verification, Flagged-for-Review transparency, PR #13 + merge to main, Pages deploy confirmation | Merged (PR #13) | COORDINATION.md, FLAGGED.md | `arena/f5896c06-poker1` |

No other active file claims are recorded. All tournament/hotel data and site generation code are outside this session's scope.

## Existing deliverables and current data status

The repository already contains a static dashboard (`index.html`, `pages/`, `assets/`), source-linked JSON data, research notes, and separate Executive Summary, Questions, Suggestions, and Flagged for Review documents. The data build reports 225 rows: 33 marked verified single entry, 15 marked possible multi-entry, 6 marked re-entry, and 171 with entry rules unverified. Only the 33 Venetian DeepStack IV rows are presently in the verified single-entry list.

## Verification performed in this session (f0143c13 / PR #11)

- `python3 scripts/build_data.py` — generated the committed data files; counts matched the above.
- `python3 scripts/build_site.py` — generated the landing page and 10 dashboard subpages.
- `python3 scripts/check_links.py` — passed JSON parsing, local links, required Markdown-file presence, and official-source-host validation.
- Pages staging smoke test — confirmed the static build contains `index.html`, all required subpages, the three JSON datasets, and all five Markdown documents fetched by the summary/questions/suggestions/flags/review pages.
- `git diff --check` — passed.
- Official Venetian source pages fetched and read:
  - [DeepStack Extravaganza IV schedule](https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html): series dates Nov 16–Dec 23, 2026; displayed schedule rows and structure-sheet links.
  - [DeepStack Extravaganza NYE schedule](https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-dec-2026.html): series dates Dec 24, 2026–Jan 10, 2027; source page itself prints some rows with a 2025 year, recorded in `FLAGGED.md`.
  - [Venetian poker suite rates](https://www.venetianlasvegas.com/resort/casino/poker/suite-rates.html): starting-rate language is conditional, rates are not assigned to a particular tower, availability and poker-play qualification apply, and $55/night resort fee is stated.
  - [Venetian resort fee](https://www.venetianlasvegas.com/resort/resort-fee.html): $55 plus tax per night.
  - [Venetian hotel terms](https://www.venetianlasvegas.com/legal/hotel-terms-and-conditions.html): 13.38% Clark County room tax and $55 plus applicable tax resort fee are stated; the terms also state rates are availability/date-dependent.

## Integration session arena/f5896c06-poker1 (PR #13)

### Verification performed
- `python3 scripts/build_site.py` regenerates `index.html` and all `pages/*.html` with **zero diff** against the committed files — the committed site exactly matches the build output.
- `python3 scripts/check_links.py`: OK — 11 pages, JSON parses, every local link resolves, no external asset references, and **every data row carries at least one https source URL**.
- `python3 scripts/build_data.py`: OK — 225 official rows total: 33 single-entry (verified), 6 re-entry, 15 possible multi-entry, 171 unverified (entry rule).
- Counts cross-check: single-entry page lists 33 Venetian DeepStack IV events (Nov 18 – Dec 23, 2026); schedule page lists 23 days with at least one verified single-entry option; earliest verified start is 10:10 AM.
- Every table row links to an official domain (venetianlasvegas.com, cdn.wynnresorts.com, wynnlasvegas.com). Blank/unverified values are left blank and flagged; nothing is inferred.

### Network-verification limitation (transparency)
- From this sandbox, outbound internet is limited to github.com / api.github.com and related hosts. The official venue domains **venetianlasvegas.com** and **cdn.wynnresorts.com** (and github.io) could not be reached (HTTP 000 / connection refused), so official venue content could not be re-fetched this session. Prior-session source links are retained; all unconfirmed values remain blank and flagged. Nothing was inferred or filled in.
- Live site URL: https://karagemop466-tech.github.io/Poker1/ — GitHub Pages API reports status `built`, source branch `main`, path `/`. The live site itself could not be fetched from this sandbox (github.io is outside the allowed hosts), so deploy status is taken from the Pages API.

### Irregularities / open facts retained
- No single-entry tournament confirmed before Nov 18, 2026 (Nov 16–17 are multi-flight Event 1 rows). First verified single-entry event: Nov 18, 11:10 AM, Venetian Event 2 ($300 NLH, $10K GTD).
- No verified 8 AM start. The 8–10 AM window has no verified event; earliest verified start is 10:10 AM (events 24/32, age 50+). Earliest start anywhere in the dataset is 10:00 AM (Wynn Super Gold Million, Dec 10, entry rule unverified).
- Hotel room rates are unverified for every hotel and date, so **no true cost per night can be stated**. Resort fee $55+tax is verified for Venetian, Palazzo, Wynn, Encore; Bellagio, Caesars, ARIA fees are blank.
- Walking times are not published on any official source; left blank.
- 171 official rows are unverified for entry rule (81 WPT, 31 Wynn Signature Series, 31 Venetian NYE, 28 Venetian DSE IV); structure sheets not read.
- Full irregularity list: see `FLAGGED.md` (F1–F12, U1–U10) and `REVIEW.md` (R1–R20).

### Sources (official domains, retained from prior sessions)
- Wynn poker page: https://www.wynnlasvegas.com/casino/poker
- WPT World Championship Schedule PDF: https://cdn.wynnresorts.com/image/upload/v1757097329/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Schedule.pdf
- WPT World Championship Structures PDF: https://cdn.wynnresorts.com/image/upload/v1750864036/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Structures.pdf
- Hotel fee/parking policy sources; Clark County lodging tax 13.38%
- Full list: data/sources.md

### Pull request / deployment
- Stale/conflicting PR #7 (head branch arena/552e97d2-poker1 not fetchable) closed; its content is already integrated on main.
- PR #13 (arena/f5896c06-poker1 → main) merged; confirmed via GitHub Pages API.

## Log
- 2026-11-16: PR #11 merged into main (b272ed5), advancing it past the branch base.
- 2026-11-16: arena/f5896c06-poker1 rebased onto origin/main, resolved COORDINATION.md conflict preserving both sessions' work; PR #13 created and merged; recording verification and limitation above.
