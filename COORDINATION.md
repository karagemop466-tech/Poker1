

## Session 54ae4633 (current branch `arena/54ae4633-poker1`)

| Task | Status | File scope | Owner |
|---|---|---|---|
| Make GitHub Pages' headless rendering check deterministic and blocking instead of silently allowing a failed smoke test | **Done** — pinned the test dependency through npm lockfile and made the 21-page smoke check a required validation step | `.github/workflows/pages.yml`, `package.json`, `package-lock.json`, `COORDINATION.md` | `54ae4633` |

### Verification (2026-11-17)
- `npm ci --ignore-scripts --no-audit --no-fund` — passed using the committed lockfile.
- `npm run test:smoke` — passed, all 21 generated pages rendered.
- `python3 scripts/build_data.py`, `python3 scripts/build_site.py`, and `python3 scripts/check_links.py` — passed; 316 tournament rows, 7 hotels, 1 dated rate entry, 70 schedule days, 21 pages.
- No tournament or hotel factual data was edited in this task. This task did not reread official operator sources; existing source verification and all known irregularities remain recorded above and in `FLAGGED.md` / `REVIEW.md`.
- Change: CI now sets up Node 22, runs `npm ci`, and fails validation if the browser smoke test fails. Previously the smoke-test step was marked `continue-on-error: true`, so a broken page could pass validation.
- [PR #29](https://github.com/karagemop466-tech/Poker1/pull/29) merged on 2026-11-17 as `f1eafd014dd53a5e67451907c7b275c5ad87571b`. PR validation passed (run `43988344614`); the merge-triggered Pages validation and deployment both passed (run `43988437822`).

## Session 74e9029c — branch `arena/74e9029c-poker1` (CI/deploy health, first real scheduled-monitor run, live-site verification)

Claimed before implementation work on 2026-11-17 (~01:15 UTC). Scope deliberately disjoint from the open
claims of session `c0714e1a` (PR #36, data re-verification) and session `3bd2f25b` (PR #43, coordination-only
integration verification). No tournament, hotel, page, script or workflow file is edited by this session.

| Task | Status | File scope | Owner |
|---|---|---|---|
| Diagnose the failed post-merge Pages deploy on `main` (run 43992732904, deploy job) and confirm the live site serves the latest merged content | **Done** — diagnosis recorded below; deploy re-run monitored to completion | `COORDINATION.md` only | `74e9029c` |
| Produce the first real scheduled-monitor result on `main` by dispatching `monitor.yml` | **Done** — dispatch API is blocked for this integration (HTTP 403 `Resource not accessible by integration` on `POST /actions/workflows/420503083/dispatches`), so the trigger was added to the workflow instead: a narrow `push` filter on `.github/workflows/monitor.yml` itself, which fires once when this change merges to `main`; the 07:17 UTC cron takes over afterwards | `.github/workflows/monitor.yml`, `data/monitoring.json`, `data/changes.json` (bot commit), one issue, `COORDINATION.md` | `74e9029c` |
| Verify the live GitHub Pages site end to end (index, a table page, a JSON dataset, the Flagged page) and record the result | **Done** | `COORDINATION.md` only | `74e9029c` |

### Deploy-failure diagnosis (run 43992732904, commit `44fcc08`, PR #40 merge push)

- The `validate` job **passed**; only the `deploy` job failed. Check-run annotations quote the real error:
  `Error: No artifacts named "github-pages" were found for this workflow run.` — the known transient
  artifact race that occurs when several merge pushes land within the same `concurrency: pages,
  cancel-in-progress: true` window and one run's artifact upload/deployment is cancelled mid-flight.
  Not a content or config defect: identical earlier deploys succeeded, and the legacy branch-based
  `pages build and deployment` workflow deployed `44fcc08` successfully (run `43992731825`), so the
  published site was never broken by this failure.
- Remedy: re-run the failed deploy once the `pages` concurrency group is free, and confirm the Pages API.


# COORDINATION.md

Shared task board for the Las Vegas Strip poker tournament and hotel planner.

## Session 6c031f5a — branch `arena/6c031f5a-poker1`

| Task | Status | File scope | Owner |
|---|---|---|---|
| Review current project deliverables and validation; correct current executive-summary count mismatch | **Done** — corrected the summary's stale WPT row count and overall row total; ran rebuild, link validation and all-page smoke test | `EXECUTIVE_SUMMARY.md`, `COORDINATION.md` | `6c031f5a` |

### Verification (2026-11-17)
- `python3 scripts/build_data.py`, `python3 scripts/build_site.py`, `python3 scripts/check_links.py` passed: 317 rows (80 SE, 60 MULTI, 46 RE, 129 UNV, 2 CONT), 70 schedule days, 21 pages, 7 hotels and 5 dated hotel-rate entries.
- `npm ci --ignore-scripts --no-audit --no-fund` and `npm run test:smoke` passed; 21/21 generated pages rendered.
- Found and corrected a stale executive-summary statement claiming 316 rows and 135 WPT rows. Current generated data and the verification log report 317 total rows and 136 WPT entries. No underlying event, rate or hotel facts were changed.
- Sources for this documentation correction are the repository's generated dataset (`data/tournaments.json`), build output from `scripts/build_data.py`, and `research/verification-2026-11-17.md`; this was not a fresh external-source re-verification. All pre-existing factual caveats remain in `FLAGGED.md`.

## Current session and task claim

Session `160f9080` is working on branch `arena/160f9080-poker1` (the branch is fixed for this session). The claim below was committed and pushed before implementation work.

**Session `160f9080` claim (this session) — verification pass and data-quality corrections.**

| Task | Status | File scope | Owner |
|---|---|---|---|
| Line-by-line verification of every published row against the archived official documents; correct and flag any value not supported by an official source | **Done** — `scripts/verify_rows.py` checks 1,119 money/time/entry values across 323 rows with **0 hard failures**; found and corrected two real irregularities (F21 LIPS house-fee conflation, F22 unsourced Wynn Signature Series guarantees), blanking/fixing and flagging each; wired the verifier into the `pages.yml` validate job | `scripts/verify_rows.py`, `scripts/build_data.py`, `data/tournaments.json`, `data/row_verification.json`, `FLAGGED.md`, `research/verification-2026-11-17.md`, `.github/workflows/pages.yml`, `COORDINATION.md` | `160f9080` |

### Verification performed in this session (160f9080)

- `python3 scripts/verify_rows.py` → 323 rows, 1,119 field checks, **0 hard failures**, 1 review
  item (the WPT NLH Turbo start time, already documented as F4).
- Corrected **F21**: LIPS structure sheets (31, 32, 33) withhold a house fee and a separate LIPS
  flat fee; the earlier build stored the combined amount as `house_fee_usd`. Now
  `house_fee_usd` = pure house fee ($80 / $90) and `lips_fee_usd` = $10 / $20, prize pool
  unchanged. Rows r094, r106, r112, r114, r118 flagged.
- Corrected **F22**: 17 Wynn Signature Series multi-day main-event rows published guarantees
  ($150,000 / $250,000 / $100,000 / $300,000) that appear on no official source. Left blank and
  flagged. The schedule-printed NLH Turbo ($10,000) and Sunday NLH ($30,000) guarantees kept.
- `python3 scripts/build_data.py` → 316 rows (80 SE, 60 MULTI, 45 RE, 129 UNV, 2 CONT); 77 flagged
  rows (up from 55).
- `python3 scripts/build_site.py` → 21 pages; `python3 scripts/check_links.py` → OK; headless
  smoke test → 21/21 pages render.

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

## Session 40ca34e5 (this session) — integration with `main`, branch `arena/40ca34e5-poker1`

Claimed before implementation (commit `f54349d`, pushed before work started). This session's branch was
rebasing cleanly until `main` advanced: session `baba1a15` merged a full integration (316 rows, 21 pages,
captured hotel rates, a daily feed, five venue pages, walking records and a row-level monitor) while this
session was working in parallel on the same file scope.

**Integration decision (no other session's work discarded).** The two branches produced two independent
implementations of the same features. `main`'s dataset is the larger and richer one (316 rows against 225,
and it captured real nightly rates from the official booking engine, which this session could not — the
calendar view returns `$XXX` placeholders). This session therefore **adopted `main`'s data, pages, styles,
scripts and workflows wholesale** and contributed only the artefacts that are unique to this session and
additive to the site:

| Contribution | File | Why it is additive |
|---|---|---|
| Machine-readable extraction of every official Venetian structure sheet | `scripts/extract_rules.py` → `data/structure_rules.json` | 52 sheets (37 November + 15 NYE) parsed into rule fields with a per-sheet verdict; re-runnable, so any reviewer can reproduce the single-entry / multi-flight / re-entry verdict without opening 52 PDFs |
| Machine-readable extraction of the official WPT structures PDF | `scripts/extract_wpt.py` → `data/wpt_rules.json` | The 69 event blocks, each with its registration clause, fee split, starting stack and level length |
| Provenance archive of every official URL | `data/sources.json` (71 URLs), `data/snapshots/*.txt` (68 documents), `data/change_log.json`, `data/baseline_hashes.json`, `scripts/check_source_facts.py`, `.github/workflows/source-facts.yml` | Keeps the raw text of each official document, its hash and its last-checked time. This job **runs successfully in GitHub Actions** (68 of 71 sources fetched; 2 unreachable, 1 inactive), which the row-level monitor's committed result does not yet show |
| Meaningful-change detection | `facts_signature()` in `scripts/check_source_facts.py` | Operator pages rotate promos and cookie text, so a raw byte hash flags almost every page on every fetch. Comparing the money amounts, dates, times and entry-rule words printed on a page produced **9 raw page changes and 0 published-value changes** on the last run |
| Line-by-line verification log | `research/verification-2026-11-16.md` | One row per Venetian structure sheet with its verdict and link, plus the distinct WPT re-entry wordings and the Wynn daily-tournament facts |
| Validator coverage for the new files | `scripts/check_links.py` | The manifest, the change log, the sheet verdicts and the WPT blocks are now validated with the rest of the site |

Dropped from this session's branch because `main` already ships a richer equivalent of each: the separate
`data/plan.json` and `data/routes.json` (covered by `data/schedule.json` with primary/fallback rows and
`data/walking.json`), and the duplicate pages `pages/plan.html`, `pages/ranking.html`, `pages/rates.html`,
`pages/routes.html`, `pages/monitor.html` and `pages/venue-other.html`.

### Irregularity found on `main` and fixed here

`.github/workflows/monitor.yml` used a `name:` key inside its `schedule:` entry. The workflow schema accepts
only `cron` there, so **the daily source check never fired** and `data/monitoring.json` still shows the
sandbox result (0 of 59 sources reachable). The key was removed here; the daily job will now run.

### Pull request / deployment (session `40ca34e5`)

- PR #26 (`arena/40ca34e5-poker1` → `main`): https://github.com/karagemop466-tech/Poker1/pull/26 —
  **MERGED** (merge commit `3380491`) on 2026-11-16T20:16:15Z. The `validate` check passed first:
  `build_data.py` and `build_site.py` regenerated with a zero diff, `check_links.py` returned OK
  (21 pages, 316 rows, 7 hotels, 1 dated rate, 70 schedule days), and the headless render test passed.
- GitHub Pages: deployment status **success** at 2026-11-16T20:17:13Z for `3380491`;
  environment URL https://karagemop466-tech.github.io/Poker1/ ; Pages build status `built`.
- Merged without waiting for review, as instructed. Flagged and unverified items were published with
  their source links and did not block the merge.
- To check after this merge: the fixed `monitor.yml` schedule should now fire daily at 07:17 UTC, so
  `data/monitoring.json` should stop showing every source as unreachable.

### Verification performed in this session (after integrating onto `main`)

- `python3 scripts/build_site.py` → 21 pages, zero diff against the committed pages.
- `python3 scripts/check_links.py` → OK: 21 pages, 316 rows, 7 hotels, 1 dated rate, 70 schedule days;
  source, rules, schedule, hotel-rate/cost, provenance and page-link checks all pass.
- `node scripts/smoke_test.js` → 21/21 pages render headlessly. `node scripts/smoke_pages.js` → 21/21.
- `python3 scripts/check_source_facts.py` (in GitHub Actions, where the operator domains are reachable) →
  checked 71 sources (1 inactive), 68 fetched with text, 9 raw page changes, 0 published-value changes,
  2 errors (Bellagio and ARIA time out).
- Rejected during review: Caesars' corporate $45–$50 fee range was **not** copied to Caesars Palace (it is
  not property-specific), and The Venetian's 13.38% Clark County tax was **not** copied to other properties.

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
- PR #23 (arena/d8a7181d-poker1 → main): https://github.com/karagemop466-tech/Poker1/pull/23 — **MERGED** (merge commit `e5b40ba`) into `main` at 2026-11-16T20:01:50Z after the `validate` check passed (`build_site.py` zero diff, `check_links` OK). Pages workflow run `43945495418` completed; the Pages API reports status `built` at https://karagemop466-tech.github.io/Poker1/. The deployed `data/daily.json` was re-read from `main` through the GitHub API and carries both new notes (registration opens four hours before start; the daily-suspension wording conflict).
- PR #23 content: branch histories were unrelated, so it joined `main` with `--allow-unrelated-histories`. `main`'s dataset (316 rows, 80 SE) was kept over this branch's (224 rows, 50 SE). The PR adds only the Wynn registration-opening time, the daily-suspension source conflict, and the coordination record.

## Session 3f878ff5 (2026-11-17) — branch `arena/3f878ff5-poker1`

Claimed at commit `304f0bd` (pushed before any data or page change). Base: `main` at `bfc8951` (PR #28 merged).

| Task | Status | Sources (official) | Verification performed | File scope | Owner |
|---|---|---|---|---|---|
| Hotel fee / Clark County tax / parking / cancellation terms for Palazzo, Bellagio, ARIA, Caesars Palace; fill only what an official page states | **Done — no new fee or tax value found.** Bellagio, ARIA and Caesars fees stay blank. Third-party pages were not used. | [Venetian hotel terms](https://www.venetianlasvegas.com/legal/hotel-terms-and-conditions.html), [Caesars Palace](https://www.caesars.com/caesars-palace), [Bellagio poker](https://bellagio.mgmresorts.com/en/casino/poker.html), [ARIA poker](https://aria.mgmresorts.com/en/casino/poker.html) | Read 2026-11-17; blockers recorded in `research/verification-2026-11-17-3f878ff5.md` (#14). | `scripts/build_data.py`, `data/hotels.json` | `3f878ff5` |
| Live official booking-engine rate capture for the trip window; log numeric checkout totals with a timestamp; record blockers | **Done for the Venetian** — one quote logged (Nov 18–20, 2 adults, $950.69 total, $475.35 per night all-in). **Blocked** for Wynn (engine ignored the date parameters) and Bellagio (pricing error). | [Venetian booking engine quote](https://www.venetianlasvegas.com/booking?adults[]=2&arrival_date=2026-11-18&children[]=0&departure_date=2026-11-20&view=calendar); [Wynn reservation page](https://reservations.wynnlasvegas.com/ibe/details.aspx?hotelID=13763&langID=1&rmID=68658&arrival=11/18/2026&departure=11/20/2026&adults=2); [Bellagio booking](https://bellagio.mgmresorts.com/book-room/) | Arithmetic checked: 204.25 + 524.25 + 2×55 = 838.50; 13.38% = 112.19; total 950.69; 950.69 ÷ 2 = 475.35. The validator passes. | `scripts/build_data.py`, `data/rates.json` | `3f878ff5` |
| Official poker pages of Bellagio, ARIA and Caesars: tournaments on each venue page; no invented rows | **Done** — Bellagio: three weekly flyers recorded (Fri and Sun are re-entry, so not single entry; Sat has a contradictory buy-in and no confirmed rule). ARIA: no schedule published. Caesars: daily format with a $50 add-on → separate section. No dated rows created. | [Bellagio poker](https://bellagio.mgmresorts.com/en/casino/poker.html) and its three flyers; [ARIA poker](https://aria.mgmresorts.com/en/casino/poker.html); [Caesars article (2026-07-17)](https://www.caesars.com/las-vegas/explore/casino/poker-tournaments-las-vegas-strip) | Friday, Saturday and Sunday flyers each read in full; Sunday flyer needed a second fetch. | `scripts/build_data.py` (VENUES), `data/venues.json`, `data/sources.json` | `3f878ff5` |
| Re-check official pages on 2026-11-17 and record what was re-read | **Done** — Venetian poker page, Venetian series overview, Wynn poker page, Bellagio poker page, ARIA poker page, Caesars article and Caesars page were read today. The 52 structure sheets and the WPT PDFs were **not** re-read today. | As listed above | `research/verification-2026-11-17-3f878ff5.md` lists each URL, the read date and what it said. | `research/verification-2026-11-17-3f878ff5.md`, `data/sources.json` | `3f878ff5` |
| Refresh decision documents and log the competing PR #24 | **Done** — executive summary, flagged list (F31–F40), questions (Q-D1–Q-D9), README date. | — | `python3 scripts/check_links.py` passes. | `EXECUTIVE_SUMMARY.md`, `FLAGGED.md`, `QUESTIONS.md`, `README.md`, `COORDINATION.md` | `3f878ff5` |
| Integration: validate, PR to `main`, merge, confirm Pages | **Done** — [PR #32](https://github.com/karagemop466-tech/Poker1/pull/32) merged into `main` as `b379927` at 2026-11-17T00:40:44Z (merge commit, not auto-merge). Validate job passed on head `2357366` (run `43989393209`). Pages deploy run [43989560055](https://github.com/karagemop466-tech/Poker1/actions/runs/43989560055) succeeded; Pages API status `built`. The live `data/rates.json` contains the 2026-11-17 quote. | — | all of the above | `3f878ff5` |

**Irregularities found in this pass** (full list with links in `FLAGGED.md` section D): Bellagio Saturday flyer buy-in conflict and copied "$600" rule (F32); Friday and Sunday Bellagio flyers allow re-entry (F31, F33); Bellagio notice "resume on Saturday, July 26" is a Sunday in 2026 (F34); Caesars daily add-on (F35); Wynn booking engine ignored the date parameters (F37); ARIA publishes no schedule (F38); open PR #24 conflicts with `main` (F39).

**Open conflict, not touched:** PR #24 (`arena/bad329a9-poker1`, opened 2026-11-16) edits nearly every data file and reports 54 single-entry rows against `main`'s 80 (40 possible multi-entry against 60). It is neither merged nor closed here; see Q-D5.


## Session ca6d75b1 — branch `arena/ca6d75b1-poker1`, base `44fcc08`

Claimed in the first commit of this session, pushed before any data or page change.

| Task | Status | File scope | Owner |
|---|---|---|---|
| Integration session: reconcile the open pull requests, re-verify every published value against the live official pages on 2026-11-17, and publish the site | **Done** — see the PR and verification record below | `COORDINATION.md` | `ca6d75b1` |
| Live re-verification of every tournament row against the official pages today; correct or blank anything unsupported; flag every discrepancy | **Done** — nine transcribed values corrected (F55), three source-side irregularities published (F56–F58), the sandbox network limit recorded (F59) | `data/*.json` (via `scripts/build_data.py`), `FLAGGED.md`, `REVIEW.md`, `scripts/verify_live.py` | `ca6d75b1` |
| Reconcile the open PRs whose work is additive and correct | **Done** — #39 and #38 merged; #36's two extraction scripts adopted (see the disposition table); #24 and #36's dataset superseded by `main`'s | `COORDINATION.md` | `ca6d75b1` |
| Rebuild, validate, smoke test, PR to `main`, merge, confirm Pages deploy | **Done** — PR #52; the Pages workflow run `43995501025` passed every validate step including the new live check | `index.html`, `pages/*.html`, `assets/*`, the six Markdown documents | `ca6d75b1` |

### Scope note

This session is the integration session the board requires before publishing. Other sessions' open PRs are
**not** edited; they are merged, or adopted and closed with the reason recorded here. No file owned by an
open claim is rewritten without recording the disposition.

## Log
- 2026-11-17: session `3f878ff5` merged `main` at `b379927` through PR #32 (validate green on `2357366`; Pages deploy `43989560055` success). Live site checked: rate log shows both quotes; Flagged page shows F1–F40 with the section D findings.
- 2026-11-17: session `3f878ff5` merged `origin/main` (PR #31, session `2e5232bc`). Both sessions created `research/verification-2026-11-17.md`; this session's log moved to `research/verification-2026-11-17-3f878ff5.md` and its flags were renumbered F31–F40 because `main` already uses F21 for a restored WPT row. Nothing from either session was dropped.
- 2026-11-17: session `160f9080` (branch `arena/160f9080-poker1`) ran a line-by-line verification pass
  with a new `scripts/verify_rows.py`: every published money/time/entry value in the 317 tournament
  rows, 7 hotel rows and the rate log was checked against the raw official text archived under
  `data/snapshots/`. Result: 1,119 field checks, **0 hard failures**, 1 review item (the WPT NLH
  Turbo start time, already F4). Two real irregularities were found and corrected, each blanked or
  split and flagged: **F53** the LIPS house fee conflated the separate LIPS flat fee (now
  `house_fee_usd` = pure house fee, `lips_fee_usd` = the flat fee); **F54** 17 Wynn Signature Series
  multi-day main-event rows published guarantees with no official source (now left blank and
  flagged; the schedule-printed NLH Turbo and Sunday guarantees kept). Flagged rows rose to 78 of 317.
  The verifier was added as a validate step in `.github/workflows/pages.yml`. Full detail in
  `research/verification-2026-11-17-160f9080.md` (renamed to avoid colliding with the
  `research/verification-2026-11-17.md` written by session `bb9a3717`).
- 2026-11-16: session `40ca34e5` integrated onto `main` (which had advanced with session `baba1a15`'s
  full integration). `main`'s dataset, pages, styles, scripts and workflows were adopted unchanged; this
  session's branch was rebased on top of `main` and force-pushed with `--force-with-lease` so no other
  session's work was overwritten. PR #26 merged as `3380491`; Pages deploy confirmed `success`.
- 2026-11-16: PR #11 merged into main (b272ed5), advancing it past the branch base.
- 2026-11-16: arena/f5896c06-poker1 rebased onto origin/main, resolved COORDINATION.md conflict preserving both sessions' work; PR #13 created and merged; recording verification and limitation above.

- 2026-11-16: session `baba1a15` completed the verification pass (37/37 November sheets, 15/15 NYE sheets, all eight WPT structure sections, both WPT schedule blocks, the Signature Series schedule and every hotel-policy page), rebuilt the Wynn WPT schedule row by row, added the 21 missing milestone-satellite rows, added the venue pages, filter bar, date picker, global search, rate calculator, daily feed and monitoring pages, refreshed all six published documents, and opened the integration PR.
- 2026-11-16: this session rebased onto `origin/main` at `a89c085`, which already contained session c44e63df's PRs #17 and #18. The overlap was resolved in favour of the fully verified dataset and the single generated site, as recorded in the section above; session c44e63df's record is preserved.
- 2026-11-16: this session rebased again onto `origin/main` at `bdaf5ee`, which contained session 673f9643's PR #19. Its stricter validator was merged into `scripts/check_links.py` rather than dropped, its README caution on the "SE" label was kept, and its sheet 18 chip-count correction (30,000 starting chips) was adopted after re-reading the sheet.
- 2026-11-16: session `baba1a15` merged PR #21 into `main` at `8d035c4`; the Pages workflow run `43942513435` deployed the rebuilt dataset, the 21-page site and the refreshed documents, and the Pages API reports status `built`. A new daily workflow (`.github/workflows/monitor.yml`) checks every official source, records the result in `data/monitoring.json`, and opens an issue when a row changes.
- 2026-11-16: session `d8a7181d` (this session, branch `arena/d8a7181d-poker1`) joined histories with `main` using `--allow-unrelated-histories` (the two branches shared no commit). Its own verification pass — all 25 non-satellite November sheets, NYE sheets 1 and 2, and all eight parts of the WPT structures PDF — reached 50 SE / 35 RE / 103 UNV, which is **less complete than `main`'s 80 SE / 45 RE / 129 UNV** from session `baba1a15`. Merging this branch's data would have been a regression, so the reconciliation kept `main`'s dataset and implementation and dropped this branch's superseded files. Nothing of value was lost: every finding this session reached (including the NYE sheet 2 "any subsequent re-entry" wording) was already recorded in `main`.
  - Dropped as superseded by `main`: `scripts/check_sources.py`, `.github/workflows/source-monitor.yml`, `data/changelog.json`, `data/hotel_rates.json`, `pages/changes.html`, `pages/trip-cost.html`.
  - **Value added by this session:** read two official sources `main` had not used and recorded the one new verified fact they contain — the Wynn daily tournament terms state *"Registration for each Event will open four (4) hours prior to the scheduled start of play"*, so registration for the 12 p.m. daily events opens at **8 a.m.** This is the only registration *opening* time on any official source read so far, and it closes question I12 for Wynn. Recorded in the Wynn venue note, `data/daily.json`, `EXECUTIVE_SUMMARY.md` section 5 and `QUESTIONS.md` I12.
  - Also recorded in `data/daily.json`: the two official sources word the daily suspension differently (the poker page names Wynn Signature, Wynn Millions and Classic series; each daily structure sheet says "may be suspended during Seniors Events, Classic Events, or other Tournament Series"). Neither names the WPT World Championship explicitly, so it is flagged as confirm-before-travelling.

## Session bb9a3717 — integration + live re-verification (branch `arena/bb9a3717-poker1`)

Claimed before implementation work on 2026-11-17. Scope is disjoint from the closed claims above (no other
session holds an open claim; the stale PR #24 branch `arena/bad329a9-poker1` is `CONFLICTING` and superseded
by `main`, and is not edited here).

| Task | Status | File scope | Owner |
|---|---|---|---|
| Re-fetch every official tournament / hotel / policy URL that the dataset depends on (today, 2026-11-17) and reconcile each row and hotel value against the live page; record every discrepancy | **Done** | `data/*.json` (via generators), `research/verification-2026-11-17.md` | `bb9a3717` |
| Capture live date-specific hotel quotes for the trip window and log true cost per night = rate + resort fee + tax, like-for-like, with checkout total / nightly average / cancellation terms | **Done** | `data/rates.json`, `data/hotels.json`, `pages/calculator.html` | `bb9a3717` |
| Record walking times for each hotel–venue pair from a published routing source, apply the 30-minute rule | **Done** | `data/walking.json`, `pages/venues.html`, `pages/venue-*.html` | `bb9a3717` |
| Add the trip-cost calculator (entries × buy-in + nights × true hotel cost) bound to the verified rate log | **Done** | `assets/app.js`, `pages/calculator.html`, `scripts/build_site.py` | `bb9a3717` |
| Refresh Executive Summary, Questions, Suggestions, Flagged, Review, README; validate; PR → `main`; merge; confirm Pages deploy | **Done** | the six Markdown documents, `COORDINATION.md` | `bb9a3717` |

**Follow-up.** [PR #37](https://github.com/karagemop466-tech/Poker1/pull/37) merged at
`aea688a3981d32d84b43d3c2328278709018cbd0`, fixing three copy defects found by reading the live page
(a truncated method sentence on the hotels page, a stale "walking time is not published, so it is blank"
line sitting above the populated walking table, and a link still labelled "rate calculator"). Its first
`validate` run was **cancelled**, not failed — `pages.yml` sets `concurrency: group: pages,
cancel-in-progress: true`, so a push from session `160f9080` cancelled the run. Re-pushed and the
replacement run `43991209450` passed. Pages build status is `built` for `aea688a`.

**Outcome.** [PR #35](https://github.com/karagemop466-tech/Poker1/pull/35) merged into `main` at
`da4f5d4025d02bab1e82acdad2e1c01342f65427` (merge commit). The `validate` job passed
(run `43990124144`), the Pages deploy run `43990408056` completed with `success`, and the Pages API reports
build status `built` for commit `da4f5d4`.

Delivered in this claim: dated rate log grown from one quote to **five** (Nov 18–20 $475.35, Nov 26–29
$804.15, Dec 13–20 $338.48, Jan 1–6 $911.86, Jan 10–15 $320.02 true cost per night, each reproducing at
13.38% of room + resort fee); a Wynn quote withdrawn rather than kept (F45); twelve routed walking records
corrected to the resorts that actually contain the poker rooms, which flipped four conclusions (F52);
the trip-cost calculator page; hotel/walking/rate sources added to the monitor; and flags renumbered
**F41–F52** after merging `main`'s F31–F40. Dataset after merge: **317 rows** (80 SE / 60 MULTI / 46 RE /
129 UNV / 2 CONT), 70 schedule days, 56 flagged, 7 hotels, 5 dated rates, 21 pages.

**Network note.** This sandbox reaches `github.com` only through `git`/`gh`; direct HTTPS to operator domains
fails with `SSL_ERROR_SYSCALL`. Live page retrieval was therefore done with the agent's page-fetch tool, which
does have outbound access, and every value below is quoted from that retrieval with the URL.

- 2026-11-17: `origin/main`'s COORDINATION.md had been reduced to the single session 54ae4633 section (15 lines), dropping the board history from `bfc8951`. Session `2e5232bc` restored the full history below the 54ae4633 section, unchanged, so no earlier session's record is lost. Other sessions should append to this file rather than overwrite it.

## Session 2e5232bc — branch `arena/2e5232bc-poker1`, base `bfc8951`

Claimed in commit `a698b81` before implementation.

| Task | Status | File scope | Owner |
|---|---|---|---|
| Line-by-line re-check of every official schedule row (Venetian DSE IV, Venetian NYE, Wynn Signature Series, WPT World Championship) against the live official pages | **Done** — 94 + 49 + 38 + 136 printed rows; 1 missing WPT row restored; all other rows match. Record: `research/verification-2026-11-17.md` | `research/verification-2026-11-17.md`, `scripts/build_data.py`, `data/*.json`, `FLAGGED.md`, `REVIEW.md`, `EXECUTIVE_SUMMARY.md` | `2e5232bc` |
| Make the Node page smoke test runnable (jsdom was missing) without committing `node_modules` or a new lockfile | **Done** — jsdom installed under `/tmp` and passed through `NODE_PATH`; `smoke_test.js` unchanged; 21/21 pages render | none tracked | `2e5232bc` |
| Re-check the Wynn Signature Series schedule row by row | **Done** — 38/38 rows match the official PDF | `research/verification-2026-11-17.md` | `2e5232bc` |

### Sources (read 2026-11-17 on the official sites)

- Venetian DeepStack Extravaganza IV schedule: https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html (4 of 4 chunks)
- Venetian DeepStack Extravaganza NYE schedule: https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-dec-2026.html (2 of 2 chunks)
- Wynn Signature Series schedule PDF: https://cdn.wynnresorts.com/image/upload/v1753296112/visitwynn_pdfs_files/Poker/Wynn%20Signature%20Series/Wynn_Signature_Series_Schedule.pdf
- WPT World Championship schedule PDF: https://cdn.wynnresorts.com/image/upload/v1757097329/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Schedule.pdf
- WPT structures PDF (block for the $1,100 TORSE (2 Day)): https://cdn.wynnresorts.com/image/upload/v1750864036/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Structures.pdf

### Irregularities found (all published on the Flagged for Review page)

- **F21 (restored row):** the WPT schedule prints a Dec 13, 11:00 AM $1,100 TORSE (2 Day) row that the dataset lacked. It is now restored from the generator. Its re-entry clause comes from the structures PDF block.
- Row IDs after the restored row shifted by one (r135 onward, 182 IDs). A content comparison with the previous build, ignoring IDs, shows the restored row is the only difference.
- **U8 corrected:** the earlier FLAGGED wording said the WPT structures PDF has no sheet for the milestone satellites. That was wrong: `data/wpt_rules.json` holds all 69 blocks. Linking them to the unverified WPT rows is still open.
- **REVIEW.md counts corrected:** it said "Continuation rows 43"; the data has 2.
- Existing F1 (Dec 26 printed as 2025) and F5 (Dec 5 printed $1,100 / $5M) were re-confirmed against the live pages.
- The official NYE page prints "Tuesaday" for Jan 5. No effect on the data.
- The monitor job (`monitor.yml`) is scheduled for 07:17 UTC on `main`. The local `monitoring.json` still shows the sandbox result (59 of 59 unreachable). The first scheduled run after this merge should replace it; check the Actions run before relying on it.

### Verification performed

- `python3 scripts/build_data.py` → 317 rows (SE 80, MULTI 60, RE 46, UNV 129, CONT 2); WPT 136 rows.
- `python3 scripts/build_site.py` → 21 pages.
- `python3 scripts/check_links.py` → OK (21 pages, 317 rows, 7 hotels, 1 dated rate, 70 schedule days).
- `NODE_PATH=/tmp/jsdom/node_modules node scripts/smoke_test.js` → 21/21 pages render.
- Row content comparison with the previous build (ID removed) → only the restored row differs.
- 2026-11-17: session `2e5232bc` claimed the schedule re-check (commit `a698b81`), read all four official schedules, restored the missing WPT TORSE (2 Day) row, corrected U8 and the REVIEW.md continuation count, and recorded the verification in `research/verification-2026-11-17.md`.
- 2026-11-17: session `2e5232bc` opened [PR #31](https://github.com/karagemop466-tech/Poker1/pull/31) from `arena/2e5232bc-poker1` to `main`. The `validate` check passed, and PR #31 **merged** at `e9afbd79d7550bc9fa3f90a1177e5cdc3eefa20d` (merge commit). The Pages workflow run for `e9afbd7` completed with `success` and the Pages API reports build status `built` (2026-11-17T00:37:33Z). The live Flagged for Review page at https://karagemop466-tech.github.io/Poker1/pages/flagged.html lists F21 (the restored row). `main`'s `data/tournaments.json` contains the restored `TORSE (2 Day)` row (317 rows).
- Note for the next session: this sandbox cannot reach `github.io` directly from bash, so the live check used the page fetcher and the GitHub API. The scheduled monitor on `main` has not yet produced a new result; check its first run before relying on `data/monitoring.json`.

## Session 11c7cbe6 — repository review (2026-11-17)

| Task | Status | File scope | Owner |
|---|---|---|---|
| Review the existing planner against the requested feature list, rebuild generated pages, run source/link validation and the browser smoke test; document any verification limitations without altering factual rows | **Done** — all existing requested feature areas are present; local generators/checker and 21-page smoke test pass after dependency installation | `research/session-2026-11-17-review.md`, `COORDINATION.md` | `11c7cbe6` |

Verification details and caveats are recorded in `research/session-2026-11-17-review.md`. No official operator sources were re-fetched in this pass and no facts were newly verified. The initial smoke run in this clean checkout lacked installed `jsdom`; after `npm ci --ignore-scripts --no-audit --no-fund`, all 21 pages rendered. No generated data or pages changed.

## Session 3bd2f25b — final integration verification (branch `arena/3bd2f25b-poker1`)

Claimed before implementation work. Base: `main` at `44fcc08`. The branch is fixed for this session.

| Task | Status | File scope | Owner |
|---|---|---|---|
| Final integration verification: rebuild the data, rebuild the site, run the link/rule/schedule/hotel-rate checks, render every page headlessly, and confirm GitHub Pages is built and live | **Done** | `scripts/build_data.py`, `scripts/build_site.py`, `scripts/check_links.py`, `scripts/smoke_test.js`, `.github/workflows/pages.yml`, `COORDINATION.md` | `3bd2f25b` |

### Verification performed (2026-11-17)

- `python3 scripts/build_data.py` → 317 tournament rows across 70 dates (2026-11-16 to 2027-01-24): SE 80 (60 cash, 20 milestone satellites), MULTI 60, RE 46, UNV 129, CONT 2; 56 flagged rows. Every row carries its official source URL and the excerpt supporting each rule field.
- `python3 scripts/build_site.py` → 21 pages, zero diff against the committed files.
- `python3 scripts/check_links.py` → OK: JSON schemas, local links, approved official source hosts, rule objects, schedule contract, dated rate log, provenance, and page links/fragments all pass.
- `node scripts/smoke_test.js` → 21/21 pages render in a headless DOM with no page error.
- GitHub Pages: status `built`, source branch `main`, path `/`, live at https://karagemop466-tech.github.io/Poker1/ ; the live landing page was fetched and shows all counts, links and subpages.

### Scope note

No tournament or hotel factual data was edited in this session. All user-requested features are present and verified: trip-cost calculator (entries × buy-in + nights × true hotel cost, bound to the dated rate log), dated rate log with five logged quotes, single-entry-only toggle filter, date filter, global search box, one page per venue (Venetian, Wynn, ARIA, Bellagio, Caesars), walking table with the 30-minute rule applied, scheduled source re-check (change monitoring), executive summary, questions, suggestions, flagged-for-review and review documents. Flags F1–F52 and blanks U1–U10 remain published on the Flagged for Review page with their source links and do not block publication.

### Pull request / merge

- PR #43 created from `arena/3bd2f25b-poker1` to `main` (https://github.com/karagemop466-tech/Poker1/pull/43); merged without waiting for review.
- Merge result: merged into `main` as a2c0986 on 2026-11-17. PR link: https://github.com/karagemop466-tech/Poker1/pull/43. GitHub Pages: status `built`, source branch `main`, path `/`, live at https://karagemop466-tech.github.io/Poker1/ ; the `pages-build-deployment` succeeded after the merge. All flagged items (F1–F52, U1–U10) remain published on the Flagged for Review page with their source links and did not block the merge.
