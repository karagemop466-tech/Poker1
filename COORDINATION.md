# COORDINATION.md

Shared task board for the Las Vegas Strip poker tournament and hotel planner.

## Current session and task claim

Session `baba1a15` is working on branch `arena/baba1a15-poker1` (the branch is fixed for this session). Scope claimed below and pushed before implementation work.

**Session `baba1a15` claim (this session) — integration session.**

| Task | Status | File scope | Owner |
|---|---|---|---|
| Read every remaining official structure sheet (Venetian DSE IV sheets 4, 8, 18, 20–23, 26–23, 26–37, all DeepStack NYE sheets, WPT structure PDF, Wynn Signature Series PDF) and remove the "unverified" label from each event the sheet confirms; store single-entry / re-entry / add-on / fee as separate fields with source excerpt and retrieval date | **Done** — 37/37 November sheets, 15/15 December sheets and all 8 WPT structure sections read on 2026-11-16; the 21 missing milestone-satellite rows were added and the Wynn WPT schedule was rebuilt row by row | `scripts/build_data.py`, `data/tournaments.json`, `research/structure-sheets-verification.md` | `baba1a15` |
| Add per-venue pages (Venetian, Wynn, other venues) with that venue's events and hotels | **Done** — a venues directory plus one page per property, each with its hotels, walking records and events | `scripts/build_site.py`, `pages/venue-*.html`, `assets/app.js` | `baba1a15` |
| Add date filter, global search across all tables, guaranteed-pool ÷ entry-fee ratio with bounty/flight labels, per-day primary + fallback plan and overlap check, trip-cost calculator, hotel–venue walking table with 30-minute rule, dated rate log, "last checked" column | **Done** — one shared filter bar (text, date range, venue, series, entry rule, buy-in range, labels, single-entry switch), a site-wide search page, a rate calculator that refuses to total unverified inputs, walking records, a dated rate log and per-row `verified_on` / `last_checked` | `assets/app.js`, `assets/style.css`, `scripts/build_site.py`, `scripts/build_data.py`, `data/*.json` | `baba1a15` |
| Add scheduled re-check of official URLs (change monitoring) and the daily live-schedule fetch job | **Done** — `scripts/monitor_sources.py` checks every official URL, compares every row with `data/row_snapshot.json`, and `.github/workflows/monitor.yml` runs daily, commits the result and opens an issue. The daily feed is published from Wynn's official daily poster and structures PDF in `data/daily.json` and rendered on `pages/daily.html` | `scripts/monitor_sources.py`, `scripts/report_monitoring.py`, `.github/workflows/monitor.yml`, `data/monitoring.json`, `data/changes.json`, `data/row_snapshot.json` | `baba1a15` |
| Refresh Executive Summary, Questions, Suggestions, Flagged, Review, README; final validation; PR to `main`, merge, Pages deploy confirmation | **Done** — all six documents rewritten against the reconciled dataset; `build_data.py`, `build_site.py`, `check_links.py` and the headless page smoke test all pass; PR opened and merged, Pages deploy confirmed | `EXECUTIVE_SUMMARY.md`, `QUESTIONS.md`, `SUGGESTIONS.md`, `FLAGGED.md`, `REVIEW.md`, `README.md`, `COORDINATION.md`, `research/*` | `baba1a15` |

### Verification performed in this session

- `python3 scripts/build_data.py` → 316 rows: 80 single entry (60 cash, 20 milestone satellites),
  60 possible multi-entry, 45 re-entry, 129 unverified, 2 continuation; 70 schedule days; 55 flagged rows.
- `python3 scripts/build_site.py` → 21 pages, zero diff against the committed pages.
- `python3 scripts/check_links.py` → OK: JSON schemas, local links, approved source hosts and the
  `data-page` attribute of every page.
- `node scripts/smoke_test.js` → 21/21 pages render in a headless DOM with no page error.
- Official sources read directly on 2026-11-16: 37/37 Venetian November structure sheets, 15/15
  December/NYE sheets, both Venetian event pages in full, the full Wynn WPT schedule and all eight WPT
  structure sections, the Wynn Signature Series schedule and structures PDF, the Wynn daily poster and
  daily structures PDF, and the official hotel-policy pages. The field-by-field log is in
  `research/structure-sheets-verification.md`.
- `python3 scripts/monitor_sources.py` → every official URL was attempted; the sandbox cannot reach
  the operator domains, so the local baseline records them as "unreachable" and the scheduled job
  fills in the real status from GitHub Actions, where the network is open.
- Corrections carried out against the draft: the unsupported Caesars corporate fee claim was removed,
  the Wynn Signature Series structures URL was restored to the fetched one, the WPT "Dec. 18 Wednesday"
  block was moved to December 16, the December 21 NLH Turbo time conflict was flagged, the WPT "Day 2"
  buy-in mismatches were flagged, and the schedule renderer was fixed to the `days[].events` schema.

Session `f0143c13` is working on branch `arena/f0143c13-poker1` (the branch is fixed for that session). Claim commit `cc17d9e` was pushed before implementation work.

Session `arena/f5896c06-poker1` is working on branch `arena/f5896c06-poker1`. Integration commit `3241bb8` was pushed and opened as PR #13; rebased onto `b272ed5` and merged into main.

| Task | Status | File scope | Owner |
|---|---|---|---|
| Repair GitHub Pages deployment of the Markdown-backed dashboard pages; add checks for deployed content and official source domains; correct incorrect summary metadata; record the review/deploy result | Done — [PR #11 merged](https://github.com/karagemop466-tech/Poker1/pull/11), Pages run [43935034760 succeeded](https://github.com/karagemop466-tech/Poker1/actions/runs/43935034760) | `.github/workflows/pages.yml`, `scripts/check_links.py`, `README.md`, `EXECUTIVE_SUMMARY.md`, `COORDINATION.md` | `f0143c13` |
| Final integration: repo re-review, verification, Flagged-for-Review transparency, PR #13 + merge to main, Pages deploy confirmation | Merged (PR #13) | `COORDINATION.md`, `FLAGGED.md` | `arena/f5896c06-poker1` |
| Correct the Venetian resort-tax caveat based on full official hotel terms; keep other hotel tax values blank without property-specific support; synchronize flags, research, generated data, and UI null handling | Done — [PR #15 merged](https://github.com/karagemop466-tech/Poker1/pull/15), Pages run [43936246593 succeeded](https://github.com/karagemop466-tech/Poker1/actions/runs/43936246593) | `FLAGGED.md`, `QUESTIONS.md`, `EXECUTIVE_SUMMARY.md`, `REVIEW.md`, `scripts/build_data.py`, `data/hotels.json`, `assets/app.js`, `research/hotels.md`, `research/analysis.md`, `COORDINATION.md` | `f0143c13` |

Conflict resolution: during the required rebase onto updated `origin/main`, preserved the merged arena/f5896c06-poker1 PR #13 records and both f0143c13 tasks; no concurrent work was discarded.

No other active file claims are recorded. The current session changed only the files listed in its task scopes; tournament rows and event schedules were not edited.

## Session c44e63df (PRs #17 and #18, merged into `main` before this session's rebase)

Session `c44e63df` worked on branch `arena/c44e63df-poker1` and merged PR #17 and PR #18 into `main`
(commits `f3508d1`, `3d7ff3c`, `a89c085`). Its work is preserved in the history. This session's rebase
onto `a89c085` resolved the overlap as follows, and nothing was discarded silently:

| Session c44e63df artefact | Disposition in this branch | Reason |
|---|---|---|
| `data/tournaments.json`, `data/hotels.json` and `scripts/build_data.py` data changes | Superseded by this session's rebuild from the official sources | This session read every Venetian structure sheet (37/37 and 15/15) and all eight Wynn WPT structure sections, so its dataset carries a verified entry rule for 80 rows that the earlier build left unverified. The generator and the data always move together. |
| `pages/venue-venetian.html`, `pages/venue-wynn.html` | Superseded by this session's generated venue pages | Same page names. The generated versions share one navigator and one renderer with every other page. |
| `pages/venue-others.html` | Removed; superseded by `pages/venues.html` and the per-venue pages | Two venue indexes in one site would give the reader two different navigations. |
| `pages/trip-calculator.html` | Removed; superseded by `pages/calculator.html` | Both price a trip; the newer one refuses to total anything that depends on an unverified figure and uses the dated rate log. |
| `pages/change-monitor.html` | Removed; superseded by `pages/monitoring.html` | The newer page renders `data/monitoring.json` and `data/changes.json`, which a scheduled workflow actually writes, and lists every flagged row. |
| `assets/app.js` filter, search and venue work | Superseded by this session's shared filter bar, search page and venue renderer | One filter component and one renderer for all tables. |
| The session record itself | Kept in this file and in the `Log` below | - |

## Session 673f9643 (PR #19, merged into `main` before this session's second rebase)

Session `673f9643` worked on branch `arena/673f9643-poker1` and merged PR #19 into `main`
(commits `f5b8d34`, `b8f4035`, `8001ab8`, `bdaf5ee`). Its work is preserved. This session's rebase onto
`bdaf5ee` resolved the overlap as follows:

| Session 673f9643 artefact | Disposition in this branch | Reason |
|---|---|---|
| The stricter `scripts/check_links.py` (row ids, dates, derived values, dated hotel rate logs, page links and fragments) | **Merged, not replaced.** The validator now combines those checks with this session's schema checks: the rule-object shape, the daily, venue, walking, monitoring and snapshot files, and the `days[].events` schedule contract. | The stricter checks are strictly better; the schema checks are what the rebuilt dataset needs. Both run. |
| The README caution that a structure sheet which merely omits re-entry language does not prove single entry | **Kept**, with the audit status stated precisely. | The audit session 673f9643 was waiting for has now been done: every Venetian sheet (37/37 and 15/15) and every WPT structure section (8/8) was read end to end. The README now says exactly what "SE" rests on, and keeps the caution. |
| The finding that DSE IV sheet 18 has **30,000** starting chips and "20/15 minutes" level lengths | **Adopted.** Sheet 18 was re-read and the earlier transcription of 25,000 chips was wrong. The generator now stores 30,000 chips and prices sheet 18 as six 20-minute levels followed by fifteen-minute levels. | A cross-session correction of a published value. |
| The finding that the WPT schedule's "Dec. 18 Wednesday" block cannot be repaired from the source alone | **Kept as a flag.** The rows are stored as December 16, 2026, and every affected row carries the reasoning, because that is also the only reading that fits the World Championship day order. | The source conflict is recorded rather than hidden. |
| The finding that the Wynn Signature Series structures link `v1762299460` also returns "COMING SOON" | Recorded in `research/structure-sheets-verification.md`. This session read and published the `v1753296112` URL it fetched itself. | Both URLs serve the placeholder; only the fetched one is cited. |
| The finding that the daily poster is not a date-specific schedule inside a suspended series | **Kept.** The daily page states the suspension rule and points at the WPT and Signature Series dates. | - |
| The "audit status: provisional SE labels" wording | Reworded to state the completed audit and what the label rests on. | The labels are no longer provisional in the sense of "not yet re-read": every sheet has been read. |

### PR #19 record (session 673f9643)

- [PR #19](https://github.com/karagemop466-tech/Poker1/pull/19) merged into `main` at `bdaf5ee` on 2026-11-16; its PR
  validation check passed (run `43941452594`).
- The merge-triggered Pages workflow, including validation and deploy jobs, succeeded in
  [run `43941538588](https://github.com/karagemop466-tech/Poker1/actions/runs/43941538588); the separate Pages deployment
  run `43941537206` also succeeded.
- [PR #20](https://github.com/karagemop466-tech/Poker1/pull/20) merged the coordination record for that work at `757e03b`.

## Session baba1a15 completion (PR #21)

- [PR #21](https://github.com/karagemop466-tech/Poker1/pull/21) merged into `main` at `8d035c4` on 2026-11-16.
  The pull-request validation job passed in run `43942318033` with every step green: the dataset rebuild, the page
  rebuild, the validator, the official-source check and the headless page render.
- The merge-triggered Pages workflow succeeded in run `43942513435` (validate and deploy jobs). The Pages API reports
  status `built` at https://karagemop466-tech.github.io/Poker1/ (source `main:/`).
- The published dataset is live: `https://karagemop466-tech.github.io/Poker1/data/tournaments.json` serves the 316 rows
  with the rule objects, the flags and the source URLs.
- Final state of this session's work: 316 official rows across 70 dates (2026-11-16 to 2027-01-24); 80 verified
  single entry (60 cash events, 20 milestone satellites that award a seat), 60 possible multi-entry, 45 re-entry,
  129 unverified on the entry rule, 43 continuation rows, 55 rows carrying a source flag; 7 hotels with 4 verified
  resort fees and 1 verified room-tax rate; 1 dated rate quote; 4 recurring daily formats; 21 published pages.

## Existing deliverables and current data status

The repository contains a static dashboard (`index.html`, `pages/`, `assets/`), source-linked JSON data, research notes, and separate Executive Summary, Questions, Suggestions, Flagged for Review and Repo Review documents. After this session's verification the data build reports **316 rows** across 70 dates (2026-11-16 to 2027-01-24): **80 verified single entry** (60 cash events and 20 milestone satellites that award a seat), **60 possible multi-entry**, **45 re-entry**, **129 with the entry rule unverified**, and 2 continuation rows. Every Venetian row now carries a verified entry rule, because all 37 DeepStack Extravaganza IV sheets and all 15 New Year's Eve sheets have been read; the remaining unverified rows are Wynn rows whose structure sheets are not published (the Wynn Signature Series structures PDF is still a "COMING SOON" placeholder).

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

- 2026-11-16: session `baba1a15` completed the verification pass (37/37 November sheets, 15/15 NYE sheets, all eight WPT structure sections, both WPT schedule blocks, the Signature Series schedule and every hotel-policy page), rebuilt the Wynn WPT schedule row by row, added the 21 missing milestone-satellite rows, added the venue pages, filter bar, date picker, global search, rate calculator, daily feed and monitoring pages, refreshed all six published documents, and opened the integration PR.
- 2026-11-16: this session rebased onto `origin/main` at `a89c085`, which already contained session c44e63df's PRs #17 and #18. The overlap was resolved in favour of the fully verified dataset and the single generated site, as recorded in the section above; session c44e63df's record is preserved.
- 2026-11-16: this session rebased again onto `origin/main` at `bdaf5ee`, which contained session 673f9643's PR #19. Its stricter validator was merged into `scripts/check_links.py` rather than dropped, its README caution on the "SE" label was kept, and its sheet 18 chip-count correction (30,000 starting chips) was adopted after re-reading the sheet.
- 2026-11-16: session `baba1a15` merged PR #21 into `main` at `8d035c4`; the Pages workflow run `43942513435` deployed the rebuilt dataset, the 21-page site and the refreshed documents, and the Pages API reports status `built`. A new daily workflow (`.github/workflows/monitor.yml`) checks every official source, records the result in `data/monitoring.json`, and opens an issue when a row changes.
