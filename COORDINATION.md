# COORDINATION.md

Shared task board for the Las Vegas Strip poker tournament and hotel planner.

## Current session and task claim

Session `f0143c13` is working on branch `arena/f0143c13-poker1` (the branch is fixed for this session). Claim commit `cc17d9e` was pushed before implementation work.

Session `arena/f5896c06-poker1` is working on branch `arena/f5896c06-poker1`. Integration commit `3241bb8` was pushed and opened as PR #13; rebased onto `b272ed5` and merged into main.

Current session `arena/673f9643-poker1` is on the fixed branch `arena/673f9643-poker1`. Claim: independent official-source re-audit of the current tournament and hotel planner, correction of source-backed errors, stronger data/build checks, and final site integration. This claim is scoped to the files listed in the task row below; no other active claims are recorded.

| Task | Status | File scope | Owner |
|---|---|---|---|
| Independent official-source re-audit; correct tournament/hotel findings, strengthen data/source validation, regenerate and integrate the dashboard, and publish verified gaps | In progress | `scripts/build_data.py`, `scripts/build_site.py`, `scripts/check_links.py`, `data/*.json`, `research/*.md`, `EXECUTIVE_SUMMARY.md`, `QUESTIONS.md`, `SUGGESTIONS.md`, `FLAGGED.md`, `REVIEW.md`, `README.md`, `assets/*`, `index.html`, `pages/*`, `.github/workflows/pages.yml`, `COORDINATION.md` | `arena/673f9643-poker1` |
| Repair GitHub Pages deployment of the Markdown-backed dashboard pages; add checks for deployed content and official source domains; correct incorrect summary metadata; record the review/deploy result | Done — [PR #11 merged](https://github.com/karagemop466-tech/Poker1/pull/11), Pages run [43935034760 succeeded](https://github.com/karagemop466-tech/Poker1/actions/runs/43935034760) | `.github/workflows/pages.yml`, `scripts/check_links.py`, `README.md`, `EXECUTIVE_SUMMARY.md`, `COORDINATION.md` | `f0143c13` |
| Final integration: repo re-review, verification, Flagged-for-Review transparency, PR #13 + merge to main, Pages deploy confirmation | Merged (PR #13) | `COORDINATION.md`, `FLAGGED.md` | `arena/f5896c06-poker1` |
| Correct the Venetian resort-tax caveat based on full official hotel terms; keep other hotel tax values blank without property-specific support; synchronize flags, research, generated data, and UI null handling | Done — [PR #15 merged](https://github.com/karagemop466-tech/Poker1/pull/15), Pages run [43936246593 succeeded](https://github.com/karagemop466-tech/Poker1/actions/runs/43936246593) | `FLAGGED.md`, `QUESTIONS.md`, `EXECUTIVE_SUMMARY.md`, `REVIEW.md`, `scripts/build_data.py`, `data/hotels.json`, `assets/app.js`, `research/hotels.md`, `research/analysis.md`, `COORDINATION.md` | `f0143c13` |

Conflict resolution: during the required rebase onto updated `origin/main`, preserved the merged arena/f5896c06-poker1 PR #13 records and both f0143c13 tasks; no concurrent work was discarded.

## Current session (c44e63df) claims — started 2026-11-16

Session `c44e63df` is working on branch `arena/c44e63df-poker1`, branched from `main` at `2dc41203c468004dec61d653192113b8e167c86d`. Outbound internet from this sandbox is limited to GitHub hosts and package registries; the official venue domains (venetianlasvegas.com, wynnlasvegas.com, cdn.wynnresorts.com) cannot be fetched here, so no new structure-sheet or hotel-rate values can be verified in this session. All unverified values therefore remain blank and flagged; nothing is inferred or filled in.

| Task | Status | File scope | Owner |
|---|---|---|---|
| Add `last_checked` date to every tournament and hotel row | Done | `scripts/build_data.py`, `data/*.json` | `c44e63df` |
| Store structured rule fields per event (single-entry, re-entry, rebuy, add-on, fee) each with source excerpt and retrieval date | Done | `scripts/build_data.py`, `data/tournaments.json` | `c44e63df` |
| Keep hotel rates as a dated log (date/rate/source/timestamp) plus checkout total, nightly average, parking, cancellation deadline | Done | `scripts/build_data.py`, `data/hotels.json` | `c44e63df` |
| Flag same-day schedule overlaps from start time + plausible duration (estimated, unverified) | Done | `scripts/build_data.py`, `scripts/build_site.py`, `assets/app.js` | `c44e63df` |
| Trip calculator page: entries × buy-ins + nights × true hotel cost | Done | `pages/trip-calculator.html`, `scripts/build_site.py`, `assets/app.js` | `c44e63df` |
| One page per venue (Venetian, Wynn, others) with its events and hotels | Done | `pages/venue-*.html`, `scripts/build_site.py`, `assets/app.js` | `c44e63df` |
| Search box across all tables; date filter on the events tables | Done | `scripts/build_site.py`, `assets/app.js` | `c44e63df` |
| Change-monitoring page + re-check script skeleton; mark rows whose source changed | Done | `pages/change-monitor.html`, `scripts/check_changes.py` | `c44e63df` |
| Rebuild site, run checks, PR to main, merge, confirm Pages deploy | Done | all site files | `c44e63df` |

No other active file claims are recorded. The current session changes only the files listed in its task scopes.


## Session c44e63df results — completed 2026-11-16

All claimed tasks are done. The work was delivered as PR #17 (arena/c44e63df-poker1 → main), merged into main as commit `f3508d1`, and deployed to GitHub Pages.

- **Pull request:** https://github.com/karagemop466-tech/Poker1/pull/17 — MERGED (merge commit `f3508d1`) into `main`.
- **CI validate:** `scripts/build_site.py` zero diff; `scripts/check_links.py` OK (16 pages; every data row carries an https source on an approved host); `node --check assets/app.js` OK. (Actions run `43938736605`.)
- **Pages deploy:** `pages build and deployment` run `43938959094` concluded **success**; Pages status `built`, live at https://karagemop466-tech.github.io/Poker1/ (source branch `main`, path `/`). The live site could not be fetched directly from this sandbox (github.io is not reachable here), consistent with the limitation noted in FLAGGED.md.
- **Data:** `scripts/build_data.py` — 225 official rows (33 single-entry verified, 6 re-entry, 15 possible multi-entry, 171 unverified), unchanged counts.

### What was delivered
- `last_checked` date on every tournament and hotel row (verification date 2026-11-16).
- Structured entry-rule fields per event (single_entry / re_entry / rebuy / add_on / flights) each with source excerpt and retrieval date, rendered as rule chips.
- Hotel rates kept as a dated log (`rates` array) plus checkout total, nightly average, parking, cancellation deadline fields — all blank/unverified until official values are retrieved.
- Same-day overlap flag field added (finish times not published, so no overlaps are asserted; flagged as unverified).
- Trip calculator page: entries × buy-ins + nights × true hotel cost per night.
- One page per venue (Venetian, Wynn, other Strip hotels), each with its events and hotels.
- Search box across all tables; date filter on the event tables to show only chosen days.
- Change-monitor page listing every official source URL with last-checked date; re-check results not populated because the sandbox cannot reach the official venue domains.

### Verification scope / irregularities
- No new structure-sheet or hotel-rate values could be verified in this session (official venue domains not reachable from the sandbox). All unverified values remain blank and flagged; nothing is inferred or filled in. See FLAGGED.md (F1–F12, U1–U10) and REVIEW.md (R1–R20).
- Ranking remains limited to the 33 Venetian single-entry events already verified; the 171 unverified official rows remain unranked.


## Existing deliverables and current data status

The repository already contains a static dashboard (`index.html`, `pages/`, `assets/`), source-linked JSON data, research notes, and separate Executive Summary, Questions, Suggestions, and Flagged for Review documents. The data build reports 225 rows: 33 marked verified single entry, 15 marked possible multi-entry, 6 marked re-entry, and 171 with entry rules unverified. Only the 33 Venetian DeepStack IV rows are presently in the verified single-entry list.

## Verification performed in this session (f0143c13 / PRs #11 and #15)

- `python3 scripts/build_data.py` — generated the committed data files; counts matched the above.
- `python3 scripts/build_site.py` — generated the landing page and 10 dashboard subpages.
- `python3 scripts/check_links.py` — passed JSON parsing, local links, required Markdown-file presence, and official-source-host validation.
- Pages staging smoke test — confirmed the static build contains `index.html`, all required subpages, the three JSON datasets, and all five Markdown documents fetched by the summary/questions/suggestions/flags/review pages.
- `git diff --check` and root Markdown local-link checks — passed.
- Hotel-data assertions passed: The Venetian retains its officially sourced 13.38% rate; other property-specific tax values are `null`; all true nightly totals remain blank because no date-specific rate is verified.
- Official Venetian and Bellagio source pages fetched and read:
  - [DeepStack Extravaganza IV schedule](https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html): series dates Nov 16–Dec 23, 2026; displayed schedule rows and structure-sheet links.
  - [DeepStack Extravaganza NYE schedule](https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-dec-2026.html): series dates Dec 24, 2026–Jan 10, 2027; source page itself prints some rows with a 2025 year, recorded in `FLAGGED.md`.
  - [Venetian poker suite rates](https://www.venetianlasvegas.com/resort/casino/poker/suite-rates.html): starting-rate language is conditional, rates are not assigned to a particular tower, availability and poker-play qualification apply, and $55/night resort fee is stated.
  - [Venetian resort fee](https://www.venetianlasvegas.com/resort/resort-fee.html): $55 plus tax per night.
  - [Venetian hotel terms](https://www.venetianlasvegas.com/legal/hotel-terms-and-conditions.html): full page confirms 13.38% Clark County room tax and $55 resort fee plus applicable tax; dates/rates remain availability-dependent.
  - [Bellagio official home page](https://bellagio.mgmresorts.com/en.html): identifies the property; no fee or tax amount is claimed from this page.
- After PR #11 merged, both Pages workflows completed successfully (including deploy run `43935034760`). The published Markdown files were fetched successfully at `https://karagemop466-tech.github.io/Poker1/EXECUTIVE_SUMMARY.md` and `https://karagemop466-tech.github.io/Poker1/FLAGGED.md`.
- PR #15's final Pages run `43936246593` passed validation and deployment. The live `data/hotels.json` was fetched after deployment and confirmed: only The Venetian has a numeric tax value (13.38%); the other six hotel tax values and all seven true-cost values are null.
- The full current session's official-source fetches are noted above; this session independently checked the source findings documented in this section, but did not reread every one of the 225 tournament rows or all 171 unverified structure sheets.

## Integration session arena/f5896c06-poker1 (PR #13)

### Verification performed
- `python3 scripts/build_site.py` regenerates `index.html` and all `pages/*.html` with **zero diff** against the committed files — the committed site exactly matches the build output.
- `python3 scripts/check_links.py`: OK — 11 pages, JSON parses, every local link resolves, no external asset references, and **every data row carries at least one https source URL**.
- `python3 scripts/build_data.py`: OK — 225 official rows total: 33 single-entry (verified), 6 re-entry, 15 possible multi-entry, 171 unverified (entry rule).
- Counts cross-check: single-entry page lists 33 Venetian DeepStack IV events (Nov 18 – Dec 23, 2026); schedule page lists 23 days with at least one verified single-entry option; earliest verified start is 10:10 AM.
- Every table row links to an official domain (venetianlasvegas.com, cdn.wynnresorts.com, wynnlasvegas.com). Blank/unverified values are left blank and flagged; nothing is inferred.

### Network-verification limitation (transparency)
- In session `arena/f5896c06-poker1`, official venue domains and `github.io` could not be reached; that session relied on prior-session source records and left unconfirmed values blank. In the later `f0143c13` session, official Venetian and Bellagio pages and the live Pages JSON/Markdown endpoints were fetched successfully; those checks are documented above. This later check did not reread all 225 tournament rows or all unverified event structures.
- Live site URL: https://karagemop466-tech.github.io/Poker1/ — Pages is configured for `main`, path `/`; the merge deployment succeeded in run `43936246593`.

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
- Hotel fee/tax source links are recorded in `data/hotels.json` and `REVIEW.md`; the 13.38% rate is now recorded only for The Venetian based on its official terms.

### Pull request / deployment
- Stale/conflicting PR #7 (head branch arena/552e97d2-poker1 not fetchable) closed; its content is already integrated on main.
- PR #13 (arena/f5896c06-poker1 → main): https://github.com/karagemop466-tech/Poker1/pull/13 — MERGED (merge commit c37d0cd) into main after the validate check (build_site.py zero diff, check_links OK) reported success.
- GitHub Pages: status `built`, live at https://karagemop466-tech.github.io/Poker1/ (source branch `main`, path `/`). Deploy triggered by the merge completed successfully.
- All integration tasks done: site builds cleanly, no broken links, every data row carries an official https source, unverified values left blank and flagged.

## Log
- 2026-11-16: PR #11 merged into main (b272ed5), advancing it past the branch base.
- 2026-11-16: arena/f5896c06-poker1 rebased onto origin/main, resolved COORDINATION.md conflict preserving both sessions' work; PR #13 created and merged; recording verification and limitation above.
- 2026-11-16: session c44e63df (branch arena/c44e63df-poker1, from main 2dc4120) claimed implementation tasks on COORDINATION.md. Outbound internet limited to GitHub hosts/package registries; official venue domains not reachable from this sandbox, so no new structure-sheet or hotel-rate values can be verified. Unverified values remain blank and flagged.
- 2026-11-16: session c44e63df completed all claimed tasks. PR #17 (arena/c44e63df-poker1 → main) merged as commit `f3508d1`; Pages deploy run `43938959094` succeeded; site live at https://karagemop466-tech.github.io/Poker1/. PR link and merge result recorded above.
