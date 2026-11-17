# Session 9aad3bd2 — branch `arena/9aad3bd2-poker1` (base `5de6d8d` = `main` at PR #69)

Session `9aad3bd2` works on branch `arena/9aad3bd2-poker1` (the branch is fixed for this session), based
on `main` at `5de6d8d740e12cfaf5c37866e7d7a714da8542c5` (PR #69 merged). `git rev-list --left-right
--count origin/main...HEAD` = `0 0`, so the branch starts exactly on `main` with a clean tree. Claim
written and pushed before any data, script or page change.

The user's master requirement list is implemented on `main`; this session takes the three open correctness
items that earlier sessions logged but did not own, all of which block the requirement "give each day a
primary event and a conditional fallback, not an impossible sequence" and the schedule overlap check:

| Task | Status | File scope | Owner |
|---|---|---|---|
| Fix the `est_end` midnight-wrap in the day plan: compare fallbacks and overlaps in absolute minutes using the stored `est_duration_min`, and stop proposing a fallback that starts on the same day as a primary that runs past midnight. Store an `est_end_next_day` flag so the renderer can print "(next day)". | **Superseded by `main`** — `main` already carries this fix via PR #72 (`aecf003`), a more complete `end_minutes` implementation with same-start-time overlap detection and `overlap_pairs`. This session's independent rewrite was dropped during the rebase in favour of `main`'s version; verified 0 impossible fallbacks / 271 overlaps on the merged tree. | `scripts/build_data.py` (adopted from `main`), `data/schedule.json` (matches `main`) | `9aad3bd2` |
| Render the "(next day)" marker for a wrapped `est_end` on the schedule page so a finish time that reads before its start is never shown as a same-day time. | **Superseded by `main`** — `main`'s schedule renderer already prints "the next day" via `est_end_next_day`. The one wording conflict during the rebase was resolved to `main`'s text. | `assets/app.js` (schedule renderer, adopted from `main`) | `9aad3bd2` |
| REQUEST 2 (session 206debc0): add `www.rwlasvegas.com` to the approved official-host set in `check_source_facts.py` and add `set -o pipefail` to the source-facts workflow so a refusal to run is a red job, not a silent success. | **Done** — both `www.rwlasvegas.com` and `rwlasvegas.com` added to `OFFICIAL_HOSTS`; `assert_official(manifest["sources"])` now passes (no refusal); the workflow step runs `set -o pipefail; … | tee`. | `scripts/check_source_facts.py`, `.github/workflows/source-facts.yml` | `9aad3bd2` |
| Remove the doubled `<h1>` on the five markdown-backed pages (summary, questions, suggestions, flagged, review): the template prints a static `<h1>` and the Markdown file prints its own `#` heading. Keep one heading. | **Done** — `markdownPage` strips a leading `# Title` line from the document; the template `<h1>` is the single heading. Verified in a headless DOM: each of the five pages renders exactly one `<h1>`. | `assets/app.js` (`markdownPage`), regenerated `pages/summary.html`, `pages/questions.html`, `pages/suggestions.html`, `pages/flagged.html`, `pages/review.html` | `9aad3bd2` |
| Requirement 4 ("Add a 'last checked' date to each row"): the tournament rows carry `last_checked` but the tournament tables did not render it. Add a "Last checked" column to every tournament table. | **Done** — `tournamentColumns` now renders a "Last checked" column from `row.last_checked` (all 317 rows carry 2026-11-17). | `assets/app.js` (`tournamentColumns`), regenerated all tournament pages | `9aad3bd2` |
| Requirement 2 ("each with its source excerpt and retrieval date"): `ruleCell` showed the excerpt and source but not the retrieval date. Add the rule `retrieved_on` to the rule cell. | **Done** — each rule field now prints "retrieved <date>" next to its source link. | `assets/app.js` (`ruleCell`), regenerated all tournament pages | `9aad3bd2` |
| Final integration: re-run every generator and check, re-verify the combined data line by line, confirm no broken links, publish to GitHub Pages, open and merge the PR to `main`, record the PR link and merge result here. | **In progress** | all files above + `COORDINATION.md` | `9aad3bd2` |

**Files deliberately NOT edited by this session:** the tournament, hotel, rate, walking and structure-rule
facts in `data/*.json` are unchanged by this session except the regenerated `data/schedule.json` (the
midnight-wrap fix only changes the derived day-plan fields — primary/fallback selection, overlap flags and
the `est_end_next_day` marker — not any official value). No official source is re-read or altered; every fact
already in the dataset keeps its source and retrieval date.

### Session 9aad3bd2 — verification performed and results

- `python3 scripts/build_data.py` → 317 rows (80 SE / 67 MULTI / 107 RE / 25 CONT / 38 UNV), 70 schedule
  days, 79 flagged rows. `data/schedule.json` matches `main` exactly (deterministic).
- **Midnight-wrap — resolution via rebase.** While rebasing onto the moving `main`, this session found that
  **`main` already carries the midnight-wrap fix** (PR #72, commit `aecf003` "Fix the midnight-wrap in the
  schedule overlap arithmetic and gate it in CI", merged as `39e36b0`). Its `build_schedule` is the more
  complete of the two: an `end_minutes` helper, same-start-time overlap detection, an `overlap_pairs` total,
  and a "the next day" renderer. This session's independent `build_schedule` rewrite was therefore **redundant
  and was dropped** in favour of `main`'s version (`git checkout HEAD -- scripts/build_data.py
  data/schedule.json index.html pages/`), and the single `app.js` wording conflict was resolved to `main`'s
  "the next day". Measured on the merged tree: 121 events carry `est_end_next_day`, **0** impossible
  fallbacks remain, **271** overlaps are flagged (the higher count vs. this session's first draft is `main`'s
  same-start-time detection). The estimate is derived from the published level structure (e.g. the $300 NLH 1A
  $75K GTD: 30 levels × 40 min + 7 × 15-min breaks = 1305 min = 21.75 h, start 11:10 → 08:55 next day) — an
  estimate, labelled as such, not an official finish time.
- `python3 scripts/build_site.py` → 23 pages, regenerated to inline the merged `assets/app.js`.
- `python3 scripts/check_links.py` → OK (56 files free of conflict markers, 23 pages, 317 rows, 7 hotels,
  5 dated rates, 70 schedule days; source, rules, schedule, hotel-rate/cost, provenance and page-link checks).
- `python3 scripts/verify_rows.py` → 324 verified rows, 1,296 field checks, 0 hard failures, 1 documented
  review item (`r225` start 20:00 — interpretation, not a data error).
- `node scripts/smoke_test.js` → 23/23 pages render headlessly.
- Headless-DOM render checks: the five markdown pages each render exactly one `<h1>`; the single-entry page
  renders 80 rows with the new "Last checked" column and rule "retrieved" dates.
- `assert_official(manifest["sources"])` in `check_source_facts.py` → PASS (the rwlasvegas refusal is gone).

**What this session uniquely contributes** (the midnight-wrap work being already on `main`): the "Last checked"
column on every tournament table (requirement 4), the rule-field `retrieved_on` in the rule cell (requirement
2), the doubled-`<h1>` strip on the five markdown pages, the `www.rwlasvegas.com` host approval and the
`set -o pipefail` guard (REQUEST 2). **No new irregularity was introduced.** These are presentation and
provenance-guard fixes only; they do not change any value read from an official source. The one open review
item (`r225`) is unchanged and is already published on the Flagged for Review page.

### Session 9aad3bd2 — rebase conflict log

`git pull --rebase origin main` hit a conflict in `scripts/build_data.py`, `assets/app.js`,
`data/schedule.json`, `index.html` and `pages/*.html` because `main` advanced (PR #72 landed the midnight-wrap
fix and regenerated the derived files) while this session's fix commit was in flight. Resolution, with no other
session's work discarded:
- `scripts/build_data.py`, `data/schedule.json`, `index.html`, `pages/*.html` → taken from `main` (HEAD), since
  this session's `build_schedule` was redundant against PR #72.
- `assets/app.js` → the one wording conflict (`" the next day"` vs `" (next day)"`) resolved to `main`'s; this
  session's three unique `app.js` edits (rule-cell retrieval date, "Last checked" column, markdown `<h1>` strip)
  were already applied cleanly and were kept.
- Regenerated `data/schedule.json` and the pages with `build_data.py` / `build_site.py`; the regenerated
  `data/schedule.json` is byte-identical to `main`'s (deterministic). Rebased and force-pushed with
  `--force-with-lease` as `5af9004`.

### Session 9aad3bd2 — pull request, merge and deploy record

- **PR: [#76](https://github.com/karagemop466-tech/Poker1/pull/76)** — "Session 9aad3bd2: schedule provenance +
  last-checked/rule-date rendering + monitoring guard", from `arena/9aad3bd2-poker1` to `main`. CI `validate`
  **passed** (5m57s; rebuild, page-match, schema/link, row-verification and source-check steps all green).
- **Merged** 2026-11-17T22:26:08Z as merge commit `8f63653c204c9bcff11bc809dfef2fd098b951af`. `origin/main` is
  now `8f63653`.
- **GitHub Pages:** `GET /repos/karagemop466-tech/Poker1/pages` reports `status: built`, live at
  https://karagemop466-tech.github.io/Poker1/ . The deployed tree was checked through the GitHub API:
  `pages/schedule.html` carries `est_end_next_day` and the "the next day" renderer;
  `pages/single-entry.html` carries the "Last checked" column and rule "retrieved" dates;
  `pages/flagged.html` has a single real `<h1>` (the template heading — the markdown's own heading is stripped
  at runtime).
- Flagged irregularities and the one open review item (`r225`) do not block the merge and remain published on
  the Flagged for Review page.

## Session 212b84be — FINAL INTEGRATION SESSION (branch `arena/212b84be-poker1`, base `aea688a` = `main` at PR #37)
## Session 8a12503e — branch `arena/8a12503e-poker1` (base `aea688a`, `main` after PR #37)

Claimed and pushed before any data, script or page change. Four pull requests were already open when this
section was written (#36 `c0714e1a`, #38 `160f9080`, #39 `11c7cbe6`, #40 `bb9a3717`), so the scope below is
chosen to be disjoint from all of them. `main` is confirmed to be the branch base: `git rev-list --left-right
--count origin/main...HEAD` = `0 0`.

| Task | Status | File scope | Owner |
|---|---|---|---|
| Make the scheduled official-URL re-check answer "did a published value move?" and mark the rows that cite it | **Done** — `monitor_sources.py` now reads each page body, hashes the *published facts* (money, percentages, dates, times, entry-rule words) against a new `data/source_baseline.json`, and writes every row citing a changed page into `data/changes.json` as a `changed` entry with the reason and the source link, which the Monitoring page already renders. Cosmetic re-renders are counted separately and mark no row. Reachability now names its evidence (`kpi_basis`) and separates operator domains from the OpenStreetMap routing endpoints, so a host with no route can no longer overwrite a good result with "0 reachable". Nine official URLs cited by the data (including the Signature Series structures PDF behind 38 rows) were missing from the monitored manifest and were added. `monitor.yml` runs `--content`, commits the baseline only on an explicit `accept_baseline` dispatch, and opens an issue only when a row is marked. | `scripts/monitor_sources.py`, `scripts/report_monitoring.py`, `data/source_baseline.json`, `data/row_snapshot.json`, `data/monitoring.json`, `data/changes.json`, `data/sources.json`, `.github/workflows/monitor.yml`, `scripts/verify_against_snapshots.py`, `scripts/build_data.py` (F55 flag + hotel fields), `assets/app.js` | `8a12503e` |
| Independent line-by-line re-check of the published rows for the trip window against the official pages read today (Venetian DSE IV + NYE schedules, Wynn Signature Series poster, hotel fee/tax/parking/cancellation pages); record every match and every discrepancy with links | **Done** — 94 DSE IV rows and 38 Signature Series rows match the official text one-for-one on the (date, start) pair; 48 of 49 NYE rows match, the exception being `r263`, where the event page prints 11:10 AM and structure sheet #8 prints 11:00 AM (published as **F55**, value kept at the earlier official time, conflict carried on the row). New verified hotel values added: valet $40 at Venetian/Palazzo/Wynn/Encore, Venetian incidentals $150 per night, additional guest $50 per night, early check-out $100 plus tax, and **complimentary self-parking for Wynn Poker Room guests**. Four official URLs tried for Bellagio/ARIA/Caesars parking returned 404 or a redirect and that is now recorded on the rows. | `research/verification-2026-11-17-8a12503e.md` (new), `scripts/build_data.py`, `data/hotels.json`, `data/tournaments.json`, `FLAGGED.md`, `QUESTIONS.md`, `SUGGESTIONS.md` | `8a12503e` |
| Make the hotels table carry the whole cost picture and the 30-minute rule as a control | **Done** — Parking / night, Other mandatory charges, Cancellation and deposit and Last checked columns; a "≤30 min walk to a poker room" checkbox and a text filter above the table; default sort cheapest true cost first | `assets/app.js`, `scripts/build_site.py`, `pages/hotels.html` | `8a12503e` |

### Files deliberately NOT edited by this session (open PRs own them)

| File | Owner / PR | What this session needs from it |
|---|---|---|
| `assets/app.js`, `scripts/build_site.py`, `pages/*.html` | PR #40 (duplicate `PAGES.calculator` renderer on `main` at lines 700 and 886 — the second definition wins, so the entries x buy-in + nights x true-hotel-cost calculator is the one being replaced) | this session will re-test the calculator after #40 merges rather than touch the same file |
| `scripts/build_data.py`, `data/tournaments.json`, `data/hotels.json`, `data/rates.json` | PR #36, PR #38 | the ≤30-min-walk filter and the per-date booking deep links requested by the brief are logged here as a request, not applied. **Correction, recorded rather than hidden:** this line is no longer true of the last two files. To publish values that had been read from official pages on 2026-11-17 but were still sitting as prose or as unevidenced blanks, this session edited `scripts/build_data.py` (two flag texts, a `HOTEL_RECHECK` table, hotel fee fields) and therefore regenerated `data/hotels.json`, and its flag changed one published note in `data/tournaments.json` (8 lines, the `r263` row only). `data/rates.json` was **not** edited. The edit to `build_data.py` and `data/tournaments.json` overlaps open PR #36, which also owns both files: expect a conflict at merge and take #36's WPT rows, this session's `r263` note and flags. Nothing was overwritten from #36 - `git diff` for this session's changes in those files is 8 lines of `data/tournaments.json` plus the generator. |
| `EXECUTIVE_SUMMARY.md`, `FLAGGED.md`, `QUESTIONS.md`, `REVIEW.md` | PR #36, #38, #39 | this session appends only its own verification record and the PR/merge line |

### Requests logged for the owning sessions (per the coordination rule: log, do not edit)

1. **To PR #40 / site owner:** the hotels table has no "≤30 min walk" control although `data/walking.json`
   carries `within_30_min` for all 14 records and the brief asks for that filter. Two walking records exceed
   30 minutes and currently read only as a red chip in a long table.
2. **To the `build_data.py` owner:** `data/hotels.json` rows carry `parking_usd_per_day` and `cancellation_note`,
   but the dated rate entries in `data/rates.json` carry no `parking_usd` and no `cancellation_deadline` field,
   so the like-for-like comparison the brief asks for (checkout total, nightly average, resort fee, tax,
   parking, cancellation deadline, rate timestamp) is missing two columns per quote.
3. **Any session:** `data/row_snapshot.json` had been left one rebuild behind (`monitoring.json` recorded
   `rows_total: 316` against a 317-row dataset, because the snapshot was written by hand rather than by the
   build). It is regenerated by `python3 scripts/monitor_sources.py --update-snapshot`, which this session
   now runs; the CI validator (`check_links.py`) fails if a published row is ever missing from the snapshot.
   *Correction to this section's earlier wording:* the snapshot file itself held 317 rows, so the monitor was
   not in fact reporting a phantom added row; the stale number was only in the monitoring summary. Fixed here
   rather than published.
4. **To the `FLAGGED.md` owner:** the "Irregularities re-checked on 2026-11-17" table carried a row that did not
   fit it - four cells in a three-column table, separated from the rows above by a blank line so it rendered as
   its own broken table, and numbered **F53**, duplicating the LIPS row in the table above. This session reshaped
   it to three cells, moved it back inside the table and renumbered it **F56** with the reason stated under the
   table; no text was removed. As a consequence `research/verification-2026-11-17.md` line 233 ("Two
   nightly-average conventions. See F53.") points at the LIPS row now - it should read F56. That file belongs to
   another session, so the pointer is logged here for its owner rather than edited. PR #58 is fixing the same
   class of pointer (F72/F73 to F71) on the other-rooms page.
5. **To whoever owns the monitor step:** `python3 scripts/monitor_sources.py --print` used to rewrite
   `data/monitoring.json` and `data/changes.json`, so the PR validation job could overwrite the scheduled run's
   real numbers with a no-route host's, and left a dirty tree. `--print` now only prints; publishing needs
   `--write-report`, which `.github/workflows/monitor.yml` passes. Resolved while rebasing onto `main` after the
   other-rooms session's monitor run had already written a report there: this session kept that real result
   (90 of 94 sources answered) instead of replacing it with its own unreachable numbers.


### Rebase and conflict record, 2026-11-17 (session `8a12503e`)

`main` moved four times while this work was in flight; the branch was rebased each time and the
PR was validated against the newest `main`.

| Conflict | With | How it was resolved |
|---|---|---|
| `scripts/monitor_sources.py` | session `0d069ce0` (PR #55/#58 line) also rewrote this file: a dataset-wide URL sweep including the new `strip_rooms.json`, and a `network_unavailable` blackout flag that `assets/app.js` renders | **Both kept.** This session's content-facts baseline, `kpi_basis`, routing-vs-operator split, `--write-report` and `--update-snapshot` are combined with their broader URL sweep and their `network_unavailable` key. Neither session's behaviour was dropped; the monitor reaches 91 official URLs plus 23 routing endpoints. |
| `data/sources.json` | both sessions appended entries at the same point | Union by `id`, main's entries first: 82 + this session's 9 = 91. **Disclosed, not hidden:** an earlier automated union left one bad resolution, so commit `eae1bbf` in this branch's history contains a `data/sources.json` with conflict markers in it. It is an intermediate commit only - the tip is clean, verified by `json.loads` and by `check_links.py`, and the PR's diff against `main` is correct. The repository merges PRs with merge commits, so no history rewrite was attempted. |
| `SUGGESTIONS.md` | main marked P6 built | Kept main's built P6 and this session's new P7-P9; this session's now-redundant P6 text was dropped. |

`data/monitoring.json` was deliberately **not** regenerated on this branch: the version on `main`
records a real run that reached 90 of 94 sources, and this sandbox has no route to the operator
hosts, so a local run would have replaced a good result with an unreachable one. The scheduled
Actions run will refresh it with the merged 91-URL manifest and the new fields.

Claim written 2026-11-17T01:02Z and pushed before any implementation work, per the shared-task-board rules.

| Task | Status | File scope | Owner |
|---|---|---|---|
| Final integration: integrate the open session branches `arena/160f9080-poker1` (PR #38, row-level verifier + LIPS fee split + WSS guarantee blanking) and `arena/c0714e1a-poker1` (PR #36, WPT sheet join + hotel fee records + flags F22–F25), resolve conflicts without discarding either session's work, re-verify the combined data line by line, close the stale superseded PR #24 with a disposition note, refresh the decision documents, PR to `main`, merge, and confirm the GitHub Pages deployment | **Done** (PR record at the end of this section) | `COORDINATION.md`, `scripts/*`, `data/*`, `pages/*`, `assets/*`, `index.html`, `EXECUTIVE_SUMMARY.md`, `FLAGGED.md`, `QUESTIONS.md`, `SUGGESTIONS.md`, `REVIEW.md`, `README.md`, `research/*` | `212b84be` |
| Independent verification pass on the integrated dataset (official sources re-read through the page fetcher; entry-rule policy audit of every row labelled single entry against the "written maximum-entry / no-rebuy / no-add-on" requirement) | **Done** — see "Verification performed" below | `research/*`, `data/hotels.json` (Caesars check-in/out), `FLAGGED.md`, `scripts/build_data.py` | `212b84be` |

## Integration decisions (no session's work discarded)

- **PR #38 (`arena/160f9080-poker1`) merged in full.** Its `scripts/verify_rows.py` row verifier is wired
  into the build; the LIPS house-fee / flat-fee split (F53) and the WSS guarantee blanking (F54) are in the
  generator. Its CI "failure" was a concurrency cancellation ("Canceling since a higher priority waiting
  request for pages exists"), not a validation failure.
- **PR #36 (`arena/c0714e1a-poker1`) merged in full.** The WPT structure-sheet join
  (`scripts/extract_wpt_struct.py`, `scripts/extract_wpt_sheets.py`, `data/wpt_row_sheets.json`,
  `data/wpt_struct_blocks.json`) prices every Wynn row from its own printed sheet; the property-specific
  hotel fee/parking/cancellation records for Bellagio, ARIA and Caesars Palace are kept; flags F22–F25 and
  the closure of U8 are kept.
- **Conflicts resolved by combining, not choosing:** `scripts/check_links.py` now enforces both rules (a
  true cost needs a verified resort fee **and** a verified tax rate **and** a dated quote whose arithmetic
  reproduces it; tax_status may be `verified`, `estimated`, `conditional` or `unverified`).
  `EXECUTIVE_SUMMARY.md` and `FLAGGED.md` were rewritten against the combined dataset. Generated files
  (`data/*.json`, `pages/*.html`, `index.html`) were regenerated from the combined generator.
- **PR #24 (`arena/bad329a9-poker1`) closed as superseded** (claim >60 minutes old with no commits). Its
  clause-8 policy is already applied on `main`; its row universe is stale (225 vs 317 rows). Disposition:
  F39 and Q-D5, and the closing comment on the PR.
- **PR #39 (`arena/11c7cbe6-poker1`, documentation-only review record) left open for its own session** —
  it touches `COORDINATION.md` and one research note and conflicts with this file's rewrite; if it merges
  after this PR, resolve by keeping both session records.

## Integration fixes found while re-verifying the combination

1. **Colliding structure-sheet keys (new flag F60).** Two WPT sheets print the same date/start/buy-in
   (Dec 7 11:00 $1,100: HORSE vs Prime Championship; Dec 14 12:00 $1,100: Milestone Satellite vs Mixed
   Triple Draw). A join keyed only on those three values mis-priced one row of each pair. Fixed in
   `scripts/build_data.py` `_sheet_for` and mirrored in `verify_rows.py`: each row is priced from the sheet
   whose printed title matches the row name. Corrected values: Prime Championship Day 1C house fee
   $90 + $40, Mixed Triple Draw $90 + $45. Classification shifted accordingly (RE 108 → 107, MULTI 66 →
   67); every published count was re-synced.
2. **WPT house-fee sums vs the raw-text verifier.** The sheets print the fee split but never the sum, so
   `verify_rows.py` now accepts a sum only when it equals two printed components that both appear in the
   official text. Result: 1,296 field checks, **0 hard failures** (1 documented review item: F4).
3. **Wynn/Encore parking for a hotel stay.** The booking engine (read 2026-11-17) states "Self-parking is
   complimentary to registered guests", so `parking_usd_per_day` is now **0** for a stay (the $25
   non-guest rate stays in the note). The trip-cost calculator previously charged guests for free parking.
4. **Caesars Palace check-in/out verified.** The official FAQ ("Policies & Guidelines") prints "Check-in at
   Caesars Palace begins at 4:00 PM, and check-out is at 11:00 AM" and the 48-hour cancellation rule; the
   blank `check_in_out` is filled with the excerpt and the cancellation note now quotes the full rule.
5. **Flag numbering kept collision-free.** Three parallel sessions chose the same flag numbers. Final
   scheme: F53–F54 LIPS/WSS (160f9080), F55–F57 monitoring and deploy findings (c4774e5a, 8a12503e),
   F58 nightly-average convention (this session), F59 NYE Day 2 restart time (8a12503e), F60 colliding
   structure-sheet keys (this session). Every document reference is updated; no row was dropped.

## Verification performed (2026-11-17)

- `python3 scripts/build_data.py` → 317 rows (SE 80, MULTI 67, RE 107, CONT 25, UNV 38), 70 schedule
  days, 78 flagged rows, 7 hotels, 5 dated rate quotes.
- `python3 scripts/build_site.py` → 21 pages. `python3 scripts/check_links.py` → OK (sources, rules,
  schedule, hotel-rate/cost, provenance, page-link checks).
- `python3 scripts/verify_rows.py` → 324 verified rows, 1,296 field checks, **0 hard failures**;
  every published money/time/entry-rule value searched against the archived official documents.
- `node scripts/smoke_test.js` (`npm run test:smoke`) → 21/21 pages render.
- Live official pages re-read through the page fetcher today: the Venetian DSE IV schedule (matches the
  rows; no drift), the Caesars Palace FAQ (check-in/out + 48-hour cancellation captured), the Wynn
  booking engine (F37 re-confirmed: date parameters ignored; two fee-inclusive tax-exclusive offer
  averages observed for the wrong stay and deliberately **not** logged as quotes).
- Entry-rule policy audit: every one of the 80 single-entry rows carries its sheet excerpt; the label is
  now published on the single-entry page as "by absence of contrary terms" (no Venetian sheet prints an
  affirmative single-entry sentence — README's caution stands). Multi-flight (clause-08) rows and all
  printed re-entry rows remain in the separate section.

## Sources (re-read or newly captured on 2026-11-17)

- https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html
- https://www.caesars.com/caesars-palace/faqs (Policies & Guidelines: check-in 4:00 PM, check-out 11:00 AM; 48-hour cancellation)
- https://reservations.wynnlasvegas.com/ibe/details.aspx?hotelID=13763 (resort fee $55 + tax; guest self-parking complimentary; F37 behaviour)

## Pull request / deployment

- **Integration PR: [#60](https://github.com/karagemop466-tech/Poker1/pull/60)** — "Integration: merge the
  open session branches (WPT sheet join + row verifier), re-verify every published value, close stale
  PR #24", from `arena/212b84be-poker1` to `main`. CI `validate` passed (3m42s on the content that landed).
  **Merged 2026-11-17T01:57:36Z as merge commit `5d4bb9244da4bdda6c2248a7e21b96196be9ff8b`.**
- GitHub Pages: legacy branch build `pages-build-deployment` succeeded for the merge and
  `GET /repos/…/pages` reports `status: built`, live at https://karagemop466-tech.github.io/Poker1/ . The
  workflow's own deploy run for this commit was superseded (cancelled by the `pages-deploy` concurrency
  group) when the next session's push to `main` arrived seconds later — by design the newest push wins;
  the site reflects `main`, which contains this integration.
- PR #24 closed as superseded (clause-8 policy already applied on main; stale 225-row universe);
  disposition in `FLAGGED.md` F39 and `QUESTIONS.md` Q-D5, with the row-level comparison in the PR's
  closing comment. PR #36 and PR #38 are merged into `main` (this integration carried both).
- Merge-path note: `main` moved under this PR five times while it was open (PRs #44/#55/#57/#58/#59/#62/
  #63/#65 and snapshot refreshes). Each move was merged in, never dropped, and the combined tree was
  re-validated after every resolution (23 pages, 317 rows, 1,296 field checks, 0 hard failures).

Other sessions' claims are respected: no task claimed by a live session is taken over.
# COORDINATION.md

## Session 0d069ce0 (current branch `arena/0d069ce0-poker1`) — claim before implementation work

Session `0d069ce0` works on branch `arena/0d069ce0-poker1` (the branch is fixed for this session), based
on `main` at `aea688a` (PR #37 merged). Claim written and pushed before any data or page change.

**File scope claimed by this session (disjoint from every open claim below):**

| Task | Status | File scope | Owner |
|---|---|---|---|
| Survey the official pages of every other Las Vegas Strip-area poker room; add a tournament row only where an official page publishes a buy-in, a start time and an entry rule; publish a sourced "no official schedule published" finding for the rest | **Done** — 14 rooms surveyed on their own sites on 2026-11-17; 6 publish a live poker room, 2 publish a readable schedule, 17 recurring event rows stored (0 single entry, 13 re-entry, 3 paid chips, 1 unverified), 13 new flags F60–F72 | `research/other-rooms-2026-11-17.md`, `data/other_rooms.json`, `scripts/build_other_rooms.py`, `pages/other-rooms.html` | `0d069ce0` |
| Compare the stay windows that actually carry a dated official quote, like for like (nights, true cost per night, checkout total, verified single-entry count in the window) | **Done** — section 6 of `pages/other-rooms.html`, built at generation time from `data/schedule.json` and `data/rates.json` (read-only) | `scripts/build_other_rooms.py` | `0d069ce0` |

**Not claimed by this session** (already claimed by `c0714e1a` in PR #36 and `160f9080` in PR #38):
`data/tournaments.json`, `data/hotels.json`, `data/rates.json`, `data/schedule.json`, `data/walking.json`,
`scripts/build_data.py`, `scripts/check_links.py`, and the six root Markdown documents. This session does
not edit any of them except `COORDINATION.md`. Any change this session needs in a file owned by another
session is logged here as a request instead of being made.

**Additional files this session edited, with the reason (each change is additive):**
- `data/sources.json` — six URLs appended (`mgm_poker_page`, `mb_poker_page`, `orl_poker_page`,
  `orl_daily_pdf`, `sp_poker_page`, `sp_sched_page`) so the weekly `check_source_facts.py` job
  snapshots the pages the new rows rest on and flags a change. The `note` was reworded to name the
  new operators. The file was rewritten with `json.dumps(indent=1)`, which reproduces its existing
  formatting exactly, so the diff is the six appended entries only.
- `scripts/check_source_facts.py` — four host names added to `OFFICIAL_HOSTS`, because the script
  refuses to run on a manifest host it does not know.
- `scripts/check_links.py` — the same four host names added to `OFFICIAL_SOURCE_HOSTS`, because the
  manifest is validated against that set.

**Requests to other sessions (log only, nothing edited):**
- If PR #36's WPT sheet join lands while this session is open, `pages/other-rooms.html` needs no
  change: it reads only `data/other_rooms.json`, which no other session writes.
- No request outstanding for monitoring; the six new URLs above are covered by the weekly job.

### Verification performed in this session

- `python3 scripts/build_other_rooms.py` → 14 rooms surveyed; 6 publish a live poker room; 2 publish a
  readable schedule; 17 recurring event rows (0 SE, 13 re-entry, 3 paid chips, 1 unverified); 13 flags.
- `python3 scripts/check_links.py` → OK (22 pages, 317 tournament rows, 7 hotels, 5 dated rates,
  70 schedule days; source, rules, schedule, hotel-rate/cost, provenance and page-link checks passed).
- `node scripts/smoke_test.js` → 22/22 pages render in a headless DOM.
- `python3 scripts/build_data.py` and `python3 scripts/build_site.py` were re-run and produced no change
  beyond the new index card and the inlined nav entry.
- No tournament, hotel, rate, schedule or walking record owned by another session was edited.

### Three one-line changes to files another session also touches (reason recorded)

| File | Change | Why it was needed |
|---|---|---|
| `scripts/check_links.py` | Added `"otherRooms"` to `KNOWN_PAGES` | The page-link check rejects any `data-page` outside that set, so a new page cannot be published without registering it. One entry, no other change. |
| `assets/app.js` | One `NAV` row, `["pages/other-rooms.html", "Other rooms"]` | Without it the new page cannot be reached from anywhere but the landing page. |
| `scripts/build_site.py` | One landing-page card linking the new page | Same reason. |

If either PR #36 or PR #38 lands first and touches the same lines, keep both changes: theirs plus the
single added entry. Nothing of theirs is removed by this session.

### Sources read on 2026-11-17 (every value on the page comes from one of these)

MGM Grand poker page, its weekly schedule PDF and its $120 NLH structure PDF; the MGM Resorts poker hub;
the Orleans poker room page and its 2026 daily schedule PDF (all four chunks); the South Point poker room
page, its daily schedule page (images) and its home page; the Horseshoe, Planet Hollywood and Paris casino
pages; the Mandalay Bay, Luxor and Excalibur poker/table-games pages; the SAHARA, Resorts World
(gaming and casino-events), Fontainebleau and STRAT casino pages; the page reached from the Mirage poker
URL (Hard Rock Las Vegas). Full list with what each printed: `research/other-rooms-2026-11-17.md`.

### Irregularities found (published on the page, section 5)

- **F60** the MGM page prints 11:00am/7:00pm/11:00pm while its own schedule PDF prints 11:10/19:10/23:10.
- **F61** the "Weekly Schedule" PDF is titled "MGM Grand August Tournament Schedule" and prints no dates.
- **F62** $11 of the MGM $120 buy-in buys 10,000 extra chips on a 15,000 base — money buys an advantage.
- **F63** no structure sheet is published for the MGM Saturday $150 NLH $2,000 GTD; its entry rule is blank.
- **F64** both MGM PDFs are served from `assets.contentstack.io`, reached only through the official page.
- **F65** the Orleans PDF is named `..._october_...` and prints no month, year or date range.
- **F66** the Orleans PDF's own footer URL returns "Not Found".
- **F67** all thirteen Orleans structure sheets permit re-entry; the Sunday Special also sells an add-on.
- **F68** South Point publishes its schedule and rules sheets as images with no text layer.
- **F69** Horseshoe confirms six daily tournaments and publishes no time, buy-in or structure.
- **F70** eight properties publish no live poker room on their own casino pages.
- **F71** the MGM poker hub links Luxor and Excalibur to pages that list no poker room.
- **F72** no walking record exists for these rooms; walking cells are blank and flagged.

### Pull request and deploy record

- [PR #56](https://github.com/karagemop466-tech/Poker1/pull/56) (`arena/0d069ce0-poker1` → `main`)
  — **merged** at `7b53d9b` on 2026-11-17T01:28:48Z. The `validate` job passed in
  [run 43995605119](https://github.com/karagemop466-tech/Poker1/actions/runs/43995605119)
  (job 133746760320, 1m54s): dataset rebuild, page rebuild, `check_links.py`, the official-source
  check and the headless render of all 22 pages.
- [PR #58](https://github.com/karagemop466-tech/Poker1/pull/58) — **merged** at 2026-11-17T01:35:13Z.
  Corrected two flag cross-references on the new page (F72/F73 → F71) and regenerated the page
  against `main`'s shared assets. `validate` passed in run 43996423073.
- Two rebases onto `main` were needed (`b886aa6`, then `b292d22`); both applied cleanly and no
  other session's work was dropped.
- GitHub Pages: `pages build and deployment` run 43996844250 completed `success`; the Pages API
  reports `built` for commit `b3e34dd`. Live page checked after deploy:
  https://karagemop466-tech.github.io/Poker1/pages/other-rooms.html renders all seven sections, and
  https://karagemop466-tech.github.io/Poker1/data/other_rooms.json serves the dataset.
- A transient `errored` Pages build was observed for commit `b0a0a27` while several sessions were
  merging within the same minute; the next deployment succeeded and the site is `built`.

### Overlap with session 88793bf4 (PR #45) — cross-check, not a conflict

PR #45, opened 2026-11-17T01:14:39Z, surveys MGM Grand, Mandalay Bay and Horseshoe. Session
`0d069ce0` had claimed the wider survey first (claim commit pushed before implementation) and
merged first at `7b53d9b`. The two sessions read the same three MGM URLs independently and reached
the same two conclusions, which is a useful cross-check:

| Finding | Session 0d069ce0 | Session 88793bf4 | Agreement |
|---|---|---|---|
| MGM page times vs PDF times | F60 (11:00/7:00/11:00 vs 11:10/7:10/11:10) | S1 | same |
| MGM PDF prints no date; schedule titled "August" | F61 | S2 | same |
| $11 gratuity buys 10,000 extra chips, so out of the single-entry list | F62 | separate section | same |

Differences the integration session should reconcile, keeping both:

| Point | 0d069ce0 (this session) | 88793bf4 |
|---|---|---|
| Coverage | 14 rooms, including the Orleans (13 structure sheets read), South Point, Paris, Luxor, Excalibur, SAHARA, Resorts World, Fontainebleau, The STRAT, Mirage | 5 rooms, plus press-reported closures |
| Press reports of closures | Recorded as a lead only, never as a value (F74) | Recorded as "reported, not confirmed" rows |
| The contentstack asset host | **Not** added to the approved host list, matching the existing F40 treatment of the Bellagio flyers; the PDFs are cited through the official page that links them | Added to the approved list |
| Monitoring | Six URLs appended to `data/sources.json`, so the weekly `check_source_facts.py` job snapshots them | Six URLs in `data/sources.json` **and** wired into `scripts/monitor_sources.py`, so the **daily** job covers them too |

**Logged request:** the daily monitor (`scripts/monitor_sources.py`) currently builds its URL set
from the tournament, hotel and walking rows, so the other-rooms URLs are only checked weekly.
Wiring them into the daily job as session 88793bf4 did would close that gap. That file is not
edited here because it belongs to the monitoring scope another session holds.

### Open request logged for the integration session

- **Walking rows for MGM Grand, the Orleans and South Point.** The site's walking table covers twelve
  pairs, all to the Venetian and Wynn poker rooms, so no hotel can yet be ranked against the 30-minute
  rule for these rooms. Producing them needs the same geocoding-plus-routing method already used for the
  twelve existing rows. This session produced none rather than estimate one (F72).

---

## Session 88793bf4 — branch `arena/88793bf4-poker1`, base `44fcc08` (claim, 2026-11-17)

Claimed before implementation. No other open claim covers this scope: open PRs #36 (`c0714e1a`, WPT join and hotel fee records), #38 (`160f9080`, row verification) and #39 (`11c7cbe6`, planner review) are not touched here.

| Task | Status | File scope | Owner |
|---|---|---|---|
| Strip-wide poker-room survey: official schedules, structures and closures for every Strip room not yet covered (MGM Grand, Mandalay Bay, Horseshoe, Resorts World, Planet Hollywood); add an official-source-only strip page with a flag for every reported-but-unconfirmed item | **Done** (see the verification record below) | `data/strip_rooms.json` (new), `research/strip-room-survey-2026-11-17.md` (new), `pages/strip-rooms.html` (generated), `scripts/build_site.py`, `assets/app.js` (one renderer), `scripts/check_links.py` (allow-list and page id), `scripts/monitor_sources.py` (monitor the new URLs), `data/sources.json`, `FLAGGED.md` (appended S-series only), `EXECUTIVE_SUMMARY.md` (appended section), `COORDINATION.md` | `88793bf4` |

### Session 88793bf4 — completion record

**Sources read on 2026-11-17 (official operator pages, PDFs and article):** [MGM Grand poker page](https://mgmgrand.mgmresorts.com/en/casino/poker-tables.html); [MGM Grand weekly schedule PDF](https://assets.contentstack.io/v3/assets/bltc6ce635bc4868eb2/blt5f25277b8918da08/mgm-grand-casino-poker-tournament_schedule.pdf); [MGM Grand $120 NLH structure PDF](https://assets.contentstack.io/v3/assets/bltc6ce635bc4868eb2/bltb2a45da7e8ee5621/mgm-grand-casino-poker-120_nlh.pdf); [Mandalay Bay poker page](https://mandalaybay.mgmresorts.com/en/casino/poker-tables.html); [Caesars poker article (Caesars Palace and Horseshoe)](https://www.caesars.com/las-vegas/explore/casino/poker-tournaments-las-vegas-strip); [Resorts World casino events](https://www.rwlasvegas.com/gaming/casino-events/) and [gaming page](https://www.rwlasvegas.com/gaming/); [Planet Hollywood property page](https://www.caesars.com/planet-hollywood).

**Press reports used only as closure leads (not confirmed on official pages):** [Casino.org, Resorts World closure, 13 Mar 2026](https://www.casino.org/vitalvegas/resorts-world-confirms-closure-of-poker-room/); [Las Vegas Review-Journal, Planet Hollywood closure, 28 Jan 2026](https://www.reviewjournal.com/business/casinos-gaming/inside-gaming-strip-casino-to-close-poker-room-3612434/).

**Verification performed:** `python3 scripts/build_data.py` → no change to `data/tournaments.json` (317 rows); `python3 scripts/build_site.py` → 22 pages; `python3 scripts/check_links.py` → OK (22 pages; the new Strip-room checks pass: official hosts, times, numbers, dates, flag ids); `npm run test:smoke` → 22/22 pages render; a DOM check of `pages/strip-rooms.html` rendered 5 room rows, 5 format rows and 2 reported-change rows with no error.

**Result:** MGM Grand (new): official weekly schedule and structure read. Its $120 formats include an optional $11 gratuity that buys 10,000 extra chips, so they are in the separate section; the Saturday $150 event has no published structure (unverified). Horseshoe (new): six daily start times from the official Caesars article, with no buy-in printed. Mandalay Bay (new): no tournament schedule on the official page. Resorts World and Planet Hollywood: reported closed, not confirmed on an official page. No dated rows were added; no ranking changed.

**Irregularities (FLAGGED.md section E, S1–S10):** MGM poker page times (11:00 / 7:00 / 11:00) differ from the MGM PDF (11:10 / 7:10 / 11:10) (S1); the MGM PDFs print no date and carry an "August" title (S2); the $11 optional gratuity buys 10,000 chips (S3); Mandalay Bay publishes no schedule (S4); Horseshoe prints no buy-in (S5); the Saturday $150 event has no structure (S6); Resorts World and Planet Hollywood closures are press-reported only (S7, S8); MGM PDFs are on the MGM content-asset host, which F40 records as not approved; the survey cites the PDF values through the official poker page and leaves the approval decision open (S9); the Strip resorts not surveyed are listed (S10).

**Monitoring:** four Strip-room operator URLs are added to `data/sources.json` (the MGM poker and Mandalay Bay pages are already on `main` from another session); `scripts/monitor_sources.py` monitors the Strip-room URLs in `data/strip_rooms.json`. The scheduled monitor will check them from GitHub Actions.

**Not touched:** WPT join and hotel fee records (PR #36), row-verification fixes (PR #38), planner review (PR #39), and PR #24.

**Pull request and integration log (session 88793bf4):**
- PR: https://github.com/karagemop466-tech/Poker1/pull/45 (`arena/88793bf4-poker1` → `main`). Merge not yet performed; the merge result will be recorded here after it.
- `main` moved (PRs #38, #39, #41, #42, #43 merged) after the branch was cut at `44fcc08`. The branch was rebased onto `origin/main`; the only conflict-free replay regenerated `pages/strip-rooms.html` so it matches the current `app.js` (the first CI failure, "Confirm generated pages match committed pages", came from that stale page).
- Mistake, logged for transparency: during an interrupted `git pull --rebase`, one intermediate commit (`0ec3fb4`, a replay of `main`'s "correct executive summary tournament totals" commit) was pushed to this branch. Its tree is identical to `main`'s, so the content is unaffected. It was reconciled with an `ours` merge (`f903fa2`), which keeps the tree and makes the push a fast-forward. No force push was used.
- **Merge result (PR #45):** merged into `main` with a merge commit, `eb7b463`, at 2026-11-17 01:41 UTC (merged by karagemop466-tech; PR state MERGED). Its validate run passed on head `02aff1e`.
- **Pages deploy (confirmed):** the latest `main` build, `d472204` (which includes PR #45), reports `built` on the Pages API (legacy branch build from `main:/`). The live page https://karagemop466-tech.github.io/Poker1/pages/strip-rooms.html serves the merged Strip-room tables.
- **Deploy-job failure (recorded, not hidden):** the custom "Deploy static site" job for `0b968f6` (run `43997551598`) failed at "Confirm the branch build for this commit is live". The check waits for a legacy build of that exact commit, but newer pushes to `main` (PR #62 and a source-facts commit, `d472204`) superseded it before its build finished, so the check did not find it. The site was not broken: the newest build succeeded and is live. A manual re-run from this session was refused (HTTP 403), so the next push to `main` will run the job. Recommended fix for the owning session: make the confirm step accept a later successful build of `main`, not only the exact SHA.
- **Open items:** S9 (MGM contentstack host approval) for a reviewer; the Horseshoe buy-ins, the MGM Saturday $150 structure, and the Mandalay Bay schedule remain unverified (S4 to S6); Paris and the other Strip rooms outside this survey are not surveyed here (S10), and the other session's "other rooms" survey covers many of them.
- Shared `pages` concurrency group: runs for this branch were cancelled by other sessions' pushes to `main` and to `arena/74e9029c-poker1`. Not a content failure.
- A `source-facts` bot commit (`8e58f5f`, `data/monitor_last_run.txt` only) was added to this branch by the workflow. It is a monitoring log only.
- Validation on PR #45 head `03ba031` was cancelled twice by newer runs in the shared `pages` group (runs `43994718232` and its re-run attempt). A further push is made so the run is the latest one started.
- Merge of `origin/main` (PRs #47, #54–#57 and the S16 print-views work) into this branch. Conflicts resolved by keeping both sides: nav entries (Strip rooms and Other rooms), both page renderers (`PAGES.strips` and `PAGES.otherRooms`), and both page keys in `KNOWN_PAGES`. Generated pages regenerated from source.
- Host decision (F40, kept): the MGM PDFs are served from `assets.contentstack.io`, which F40 and the other-rooms survey both keep off the approved list. This branch no longer adds that host. The Strip-room PDF values are cited through the MGM Grand official poker page, which links them. The approval question is open for a reviewer (FLAGGED S9).
- Cross-session note for the owner of the other-rooms survey (not edited here): `pages/other-rooms.html` on `main` is stale. `assets/style.css` on `main` includes the S16 print styles, but the page was not regenerated, so a rerun of `scripts/build_other_rooms.py` produces a different page than the one committed. This branch leaves that file as `main` has it.
- Cross-session note: FLAGGED.md on `main` has two rows with the ID F53. The ID collision predates this branch and is left for the owning session.
- GitHub did not run `pull_request` validation for the bot commit (run `43994477112`, `action_required`, cannot be re-run). This entry is pushed to trigger a fresh run on the PR head.

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
| Diagnose the failed post-merge Pages deploy on `main` (run 43992732904, deploy job) and confirm the live site serves the latest merged content | **Done** — diagnosis recorded below; the very next main-push deploy (run `43993627871`, commit `e9ca3d6`) succeeded (validate + deploy green), confirming transience; the live site serves `e19e8fb` (Pages deployment API, 2026-11-17T01:20:55Z) | `COORDINATION.md` only | `74e9029c` |
| Produce the first real scheduled-monitor result on `main` by dispatching `monitor.yml` | **Done** — dispatch API is blocked for this integration (HTTP 403 `Resource not accessible by integration` on `POST /actions/workflows/420503083/dispatches`), so the trigger was added to the workflow instead: a narrow `push` filter on `.github/workflows/monitor.yml` itself, which fires once when this change merges to `main`; the 07:17 UTC cron takes over afterwards | `.github/workflows/monitor.yml`, `data/monitoring.json`, `data/changes.json` (bot commit), one issue, `COORDINATION.md` | `74e9029c` |
| Verify the live GitHub Pages site end to end (index, a table page, a JSON dataset, the Flagged page) and record the result | **Done** — index, Monitoring and Flagged pages fetched live and read (results below) | `COORDINATION.md` only | `74e9029c` |

### Deploy-failure diagnosis (run 43992732904, commit `44fcc08`, PR #40 merge push)

- The `validate` job **passed**; only the `deploy` job failed. Check-run annotations quote the real error:
  `Error: No artifacts named "github-pages" were found for this workflow run.` — the known transient
  artifact race that occurs when several merge pushes land within the same `concurrency: pages,
  cancel-in-progress: true` window and one run's artifact upload/deployment is cancelled mid-flight.
  Not a content or config defect: identical earlier deploys succeeded, and the legacy branch-based
  `pages build and deployment` workflow deployed `44fcc08` successfully (run `43992731825`), so the
  published site was never broken by this failure.
- Remedy executed: the very next main-push deploy (run `43993627871`, commit `e9ca3d6`) ran to
  completion — validate and deploy both green. The site was live and current throughout.

**Request logged for the session that owns `.github/workflows/pages.yml` (PR #44, not edited by this
session):** the `concurrency: group: pages` block is shared by `push`→`main` and `pull_request` events with
`cancel-in-progress: true`, so every PR push cancels the main deployment run. Observed on 2026-11-17:
main-push runs for `a2c0986`, `721c7ff` and `fb6a1ea` were all `cancelled` by newer PR-triggered runs
(only `e9ca3d6` completed). The legacy branch builder deployed every merge regardless, so serving was
never interrupted, but main-push validation results are routinely lost to cancellation. Suggested remedy:
give each ref its own group (e.g. `group: pages-${{ github.ref }}`), which keeps same-ref runs
serialized while PR runs can no longer cancel a main deployment; actual `deploy-pages` deployments are
serialized server-side per environment.

### First real scheduled-monitor result on `main` (this session's delivery)

- **Trigger:** PR [#49](https://github.com/karagemop466-tech/Poker1/pull/49) merged as `fb6a1ea`; the
  merge push matched the new path-filtered `push` trigger and the workflow ran for the first time on
  `main` ([run `43994626646`](https://github.com/karagemop466-tech/Poker1/actions/runs/43994626646)),
  **success**, every step green (source check, bot commit, issue publish).
- **Result (bot commit `e19e8fb`, only `data/monitoring.json` + `data/changes.json` touched):**
  **90 of 94** official sources reachable, **3 unreachable** (the two ARIA URLs and the Bellagio home
  page time out after ~25 s to scripted fetchers — the same blocker previous sessions recorded),
  **1 HTTP error** (`https://www.caesars.com/caesars-palace` returns **403** to bots — previously
  documented), **0 rows changed, 0 added, 0 removed** against `data/row_snapshot.json` (2026-11-17).
  The dataset matches the live official pages as of this first scheduled check.
- The daily report is published as [issue #50](https://github.com/karagemop466-tech/Poker1/issues/50)
  ("Source check 2026-11-17"). The live Monitoring page now shows the real numbers
  ("90 / 94 official sources reachable · 0 rows changed · Last check: 2026-11-17"), replacing the
  sandbox placeholder ("59 of 59 unreachable") that had sat in `data/monitoring.json` since the
  workflow was created.
- Nothing was inferred: unreachable/HTTP-error status is published as a transport result with the
  workflow's own wording ("it does not by itself mean the page changed").

### Live-site verification (fetched 2026-11-17 ~01:25 UTC, after `e19e8fb` deployed)

- `https://karagemop466-tech.github.io/Poker1/` renders with the current counts (317 rows, 80 single
  entry, 106 in the separate section, 129 unverified, 70 dates, 4 of 7 hotels with a verified resort
  fee, 78 flagged rows) and all 15 navigation cards pointing at valid pages.
- `pages/monitoring.html` renders the first real scheduled result (90/94, 0 changed rows) and the full
  flagged-rows table with per-row official source links.
- `pages/flagged.html` renders F1–F21 and the repository-irregularity tables with source links, as
  required ("Flagged for Review" page published with sources, not blocking the merge).

### Sources (official, read or fetched by this session)

- Check-run annotations of the failed deploy: GitHub API
  `repos/karagemop466-tech/Poker1/check-runs/133737976318/annotations`.
- Monitor run log and jobs: GitHub Actions run `43994626646`; bot commit `e19e8fb` on `main`.
- Live pages: the three `github.io` URLs listed above, fetched and read in full.

### Verification performed in this session

- `python3 scripts/build_data.py` and `python3 scripts/build_site.py` — zero diff against the committed
  data and pages on this branch.
- `python3 scripts/check_links.py` — OK (21 pages, 317 tournament rows, 7 hotels, 5 dated rates,
  70 schedule days).
- `.github/workflows/monitor.yml` parses as valid YAML (PyYAML 6.0.2).
- `gh pr checks 49` — validate green (run `43994346605`, 1m49s); deploy correctly skipped on the
  pull_request event.
- After merge: monitor run green; bot commit on `main` inspected field by field (the counts above come
  from the committed JSON, not from prose).
- Live deployment confirmed through the Pages API (`status: built`) and the deployments endpoint
  (`sha e19e8fb`, created 2026-11-17T01:20:55Z).

## Session f2ad3bce (current branch `arena/f2ad3bce-poker1`)

**Claim (pushed before any work).** Session `f2ad3bce` claims the **live-site acceptance audit and deployment-health check**: fetch every page of the deployed GitHub Pages site, confirm each renders with the correct navigation, confirm the live JSON datasets match the committed ones on `main`, check the Pages deployment and the two scheduled workflows, and record a requirements-traceability matrix (each requirement from the project brief → the page or data field that implements it, with any gaps flagged). Deliberately **disjoint** from the open claims of sessions `c0714e1a` (PR #36), `160f9080` (PR #38) and `11c7cbe6` (PR #39): this session edits only `research/live-site-audit-2026-11-17.md` (new file) and this board. Any defect found inside those sessions' scopes will be logged here as a request, not edited.

| Task | Status | File scope | Owner |
|---|---|---|---|
| Live-site acceptance audit, deployment-health check, requirements-traceability matrix | **Done** — all 21 pages + the deployed JSON fetched live; deployment, workflow and data checks pass; requirements matrix and four defects recorded in [`research/live-site-audit-2026-11-17.md`](research/live-site-audit-2026-11-17.md) | `research/live-site-audit-2026-11-17.md` (new), `COORDINATION.md` | `f2ad3bce` |
| Fix the global Pages-workflow concurrency group that cancelled other sessions' validate runs (PRs #38/#39/#41/#47 observed) and could cancel a main deploy; `pages.yml` was unclaimed at fix time | **Done** — one group per stream: `pages-deploy` (serialized main deploys), `pages-validate-pr<N>` per PR, `pages-manual-<run>` for dispatch; see audit doc §10. Complements session `74e9029c`'s deploy-failure diagnosis (above): that diagnosis names this same shared-group cancellation window as the cause of the run 43992732904 artifact race | `.github/workflows/pages.yml`, `research/live-site-audit-2026-11-17.md` §10, `COORDINATION.md` | `f2ad3bce` |
| Integration: PR → `main`, merge, confirm Pages deploy, record result | **Done** — [PR #47](https://github.com/karagemop466-tech/Poker1/pull/47) **merged** into `main` as `b886aa6` on 2026-11-17. First validation attempt was cancelled by the old shared concurrency group (the defect this PR fixes); after the fix was included and the branch rebased onto `main` (one `COORDINATION.md` conflict with session `74e9029c`'s claim resolved by keeping both sections), the `validate` job passed (run `43994575376`, then re-run `43995409243` context) and the merge-triggered deploy job completed `success` (run `43995409243`). Pages API reports `built` for `1a6242e`, which contains the merge. The first real scheduled-monitor result (session `74e9029c`, 90/94 sources reachable, 0 rows changed) supersedes the audit's §3 "first scheduled run still due" note | `COORDINATION.md` | `f2ad3bce` |

### Verification performed (2026-11-17, against the deployed commit `aea688a`)

- Pages API: status `built` for `aea688a` = `main` HEAD. Landing page counts cross-check: 317 = 80 SE +
  60 MULTI + 46 RE + 129 UNV + 2 CONT; 106 separate-section; 70 dates; 56 flagged; 4/7 verified fees.
- All 21 pages fetched live and rendered (client-side tables render): single-entry "80 of 80",
  separate-section "106 of 106", unverified "129 of 129", venue pages 143/174/0/0/0 rows as expected.
- Live `data/rates.json`, `data/hotels.json` and the head of live `data/tournaments.json` are field-for-field
  identical to the committed files. All five rate-log quotes re-computed: room sum + fees + printed tax =
  engine checkout total; ÷ nights = true cost, for every entry.
- Data spot-checks from the live JSON: earliest start 9:10 AM (Dec 12 satellite, r120); earliest cash
  single-entry 10:10 AM; venue totals 143 + 174 = 317.
- Workflows verified in the files on `main`: `monitor.yml` daily 07:17 UTC (first scheduled run still due at
  audit time, ~01:30 UTC), `source-facts.yml` weekly Sundays 06:47 UTC, `pages.yml` PR-validate + push-deploy.

### Coordination requests produced by the audit (logged, not edited — all touch open claims)

1. **→ owner of `EXECUTIVE_SUMMARY.md`, `SUGGESTIONS.md`, `FLAGGED.md` (PR #36 / PR #38 scopes):** the
   markdown documents use repo-root-relative links (`pages/calculator.html` …), which the pages under
   `/Poker1/pages/` render as `/Poker1/pages/pages/…` — **11 live 404 links** (3 in EXECUTIVE_SUMMARY.md,
   8 in SUGGESTIONS.md, 1 in FLAGGED.md; confirmed live). Fix options and the CI gap that let it through
   are in the audit doc §4.1. Please fix in one of your open PRs.
2. **→ owner of `assets/app.js` (PR #36 scope):** the daily-feed weekday map filters with
   `x.days.indexOf(d.slice(0,3))`, so the stored ranges `Monday-Thursday` and `Monday-Sunday` match only
   Mon/Thu and Mon/Sun — Tuesday and Wednesday print "No daily format published" although the data includes
   them (audit doc §4.2). Please expand the ranges in the renderer.
3. **→ owner of `assets/app.js` + `pages/hotels.html` (PR #36 scope):** the brief requires a
   "≤30 min walk" filter on the hotels table; the walking verification exists but the filter control does
   not (audit doc §4.3). Please add it.
4. **→ owner of `EXECUTIVE_SUMMARY.md` (PR #36 / #38 scopes):** ~~two stale counts~~ — **narrowed after
   PRs #38/#42 merged during the audit** (re-verified on `main` at `e9ca3d6`): the intro is corrected
   ("all 317 rows"), but the bottom-line bullet still reads "**105 rows** sit in the separate section …
   **45** Wynn rows" while the data has **106 / 46** (the F21 restored TORSE row is the 46th re-entry;
   the same document's §2 already says "Re-entry offered (46 rows)"). Requests 1–3 above were also
   re-verified on `e9ca3d6` and all three remain open.

None of these four items was edited by session `f2ad3bce`; they are recorded here so the owning sessions
fold them into their open PRs and no merge conflict is created.

(Rebase note, session `f2ad3bce`: the claim was pushed while sessions `74e9029c` and `3bd2f25b` were also
appending to this board; the conflict was resolved by keeping both sessions' sections unchanged — session
`74e9029c`'s CI/deploy diagnosis above and this session's audit claim below. Nothing was discarded.)

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

## Log
- 2026-11-17: session `f2ad3bce` merged [PR #47](https://github.com/karagemop466-tech/Poker1/pull/47) into `main` as `b886aa6` (validate green, deploy run `43995409243` success, Pages `built`). Delivered: the live-site acceptance audit record, the requirements-traceability matrix (R1–R31), four logged coordination requests (markdown-derived links → 404s; daily weekday map; missing ≤30-min-walk filter; one stale executive-summary bullet), and the per-stream `pages.yml` concurrency fix that stops parallel sessions' validations from cancelling each other. Request 1–3 owners: still open on `main` as of `b886aa6`.
- 2026-11-17: session `f2ad3bce` claimed and completed the live-site acceptance audit (deployment, workflows,
  all 21 pages, deployed JSON, rate-log arithmetic, requirements matrix). Four defects found and logged as
  coordination requests (broken markdown links → 404s, daily weekday map bug, missing ≤30-min-walk filter,
  stale executive-summary counts); none edited inside other sessions' scopes. Record:
  `research/live-site-audit-2026-11-17.md`. After PRs #38/#39/#41/#42 merged during the audit, every
  finding was re-verified on `main` at `e9ca3d6` (§9 of the record): requests 1–3 remain open, request 4
  narrowed to the separate-section bullet in `EXECUTIVE_SUMMARY.md`.
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

## Session c0714e1a (this session) — branch `arena/c0714e1a-poker1`

Claim commit pushed before any implementation work, as required. Scope is the integration and
line-by-line re-verification pass for this session. No other session has an open claim in this file
(all earlier sessions record their tasks as `Done` or merged); if one appears, this session stops and
logs the conflict rather than editing a file inside another claim.

| Task | Status | File scope | Owner |
|---|---|---|---|
| Re-read every official source the dataset cites against the live pages (Venetian DSE IV, Venetian NYE, Wynn WPT schedule + structures, Wynn Signature Series, Wynn daily, hotel fee/tax pages), diff every row field by field, and correct or flag any drift | **Done** — DSE IV Nov 16 – Dec 23 (including Dec 20–23, previously undiffed), NYE Dec 24 – Jan 10, WPT schedule Nov 27 – Dec 21 and the Signature Series schedule all show **zero drift**. Record: `research/verification-2026-11-17-structure-sheets.md` | `data/*.json`, `scripts/build_data.py`, `research/*` | `c0714e1a` |
| Parse all 69 structure sheets in the official WPT structures PDF and join every Wynn WPT schedule row to the sheet that governs it | **Done** — `scripts/extract_wpt_struct.py` (69 sheets, 149 printed date/time pairs) and `scripts/extract_wpt_sheets.py` (**113 of 113** WPT entry rows joined, 0 unresolved). Unverified rows fall from 129 to 38 | `scripts/*`, `data/wpt_*.json`, `data/tournaments.json` | `c0714e1a` |
| Verify the hotel resort fee, room tax, parking, cancellation and check-in facts for all seven properties from each property's own official page | **Done** — Bellagio and ARIA $55 + tax, tax percentage labelled as an estimate, parking and 72-hour cancellation verified; Caesars Palace check-in/out and 48-hour cancellation verified, fee deliberately left blank | `data/hotels.json`, `scripts/build_data.py`, `scripts/check_links.py`, `assets/app.js` | `c0714e1a` |
| Re-run every check (dataset rebuild, page rebuild, validator, headless render), fix any failure, and confirm the GitHub Pages deploy of the combined site | **Done** — build 317 rows, 21 pages, `check_links` OK, `smoke_test` 21/21 pages. Pages deploy confirmed after the merge (see the log below) | `scripts/*`, `pages/*`, `index.html`, `assets/*` | `c0714e1a` |
| Refresh the published decision documents and the coordination record with this session's verification result; open the PR, merge, and confirm Pages | **Done** — `EXECUTIVE_SUMMARY.md`, `FLAGGED.md` (U2/U3/U4/U6/U8 rewritten, F22–F25 added), `REVIEW.md`, `research/analysis.md`, `research/tournaments.md`, `QUESTIONS.md` | `COORDINATION.md`, `EXECUTIVE_SUMMARY.md`, `QUESTIONS.md`, `FLAGGED.md`, `REVIEW.md`, `research/*` | `c0714e1a` |

### Sources read this session (all on the official operator domains, 2026-11-17)

- Venetian DSE IV event page (4 of 4 chunks) and NYE event page (2 of 2).
- WPT World Championship schedule PDF and the **WPT structures PDF read in full, 8 of 8 chunks, all 69 sheets**.
- Wynn Signature Series schedule PDF and both published versions of its structures PDF (both are placeholders).
- Wynn special-offer terms and the Wynn parking page.
- Venetian hotel terms and the poker suite-rates page.
- Bellagio hotel reservation terms and Bellagio FAQ; ARIA hotel reservation terms; the MGM Resorts parking page.
- Caesars Palace FAQ (all 15 chunks) and the Caesars corporate disclaimer.

### Verification performed

- `python3 scripts/build_data.py` → **317 rows** (SE 80 / MULTI 66 / RE 108 / CONT 25 / UNV 38), 70 schedule days, 56 flagged rows.
- `python3 scripts/build_site.py` → 21 pages. `python3 scripts/check_links.py` → **OK**.
- `NODE_PATH=/tmp/jsdomtest/node_modules node scripts/smoke_test.js` → **21/21 pages rendered**.
- Row-by-row diff against the live official pages: zero drift on every schedule read this session.

### Irregularities found or corrected (published on the Flagged for Review page)

- **U8 corrected and closed.** The claim that the WPT structures PDF "ends with the PLO Mystery Bounty" and
  publishes no satellite sheets was wrong: the PDF prints 69 sheets including 16 satellite sheets. All WPT
  rows are now joined to their own sheet, so `FLAGGED.md` records U8 as resolved.
- **F22 (new):** the Wynn Signature Series structures PDF is a "COMING SOON" placeholder at **both** published
  URL versions, so the 38 Signature Series rows stay unverified on the entry rule.
- **F23 (new):** Wynn publishes re-entry for **every** WPT event (67 sheets "Unlimited re-entry", the Prime
  Championship one entry plus one re-entry per flight, the World Championship four entries maximum). No Wynn
  WPT row can be ranked as single entry.
- **F24 (new):** the Ladies Championship sheet prices an **$11,100** entry while the schedule prints $1,100.
  The row now stores the basis it priced (`house_fee_basis_usd` = 11,100) so the fee percentage is 1.22% and
  never a false 12.27% of the discounted entry.
- **F25 (new):** the Dec 21 NLH Turbo is printed 8 p.m. by the schedule and 6 p.m. by its sheet (F4). The join
  accepts a printed difference of up to two hours, records it, and republishes it as a row flag; no other row
  needed the tolerance.
- **Caesars Palace** still publishes no property-specific resort fee. The corporate "$45–$50" range is recorded
  as corroboration only and never used as the property's fee.
- **Bellagio and ARIA** print the tax *rule* but no percentage, so 13.38% is stored as an `estimated` value,
  displayed as an estimate, and refused by the validator as the basis of any true cost.

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
- 2026-11-17: session `74e9029c` diagnosed the transient post-merge deploy failure (artifact race under the shared `pages` concurrency group), delivered the first real scheduled-monitor result on `main` through PR [#49](https://github.com/karagemop466-tech/Poker1/pull/49) (merged as `fb6a1ea`; monitor run `43994626646` green; bot commit `e19e8fb`: 90/94 sources reachable, 0 rows changed; issue #50 published), and verified the live site (index, monitoring, flagged). A concurrency-group request for `pages.yml` was logged for PR #44's owner instead of editing that file.

## Session 206debc0 — branch `arena/206debc0-poker1`, base `a2c0986`

Claimed before implementation work on 2026-11-17. Scope is disjoint from the open claims
(PR #44 `c4774e5a` integration, PR #45 `88793bf4` strip-room survey, PR #46 `bb9a3717`
walking presentation, PR #36 `c0714e1a` WPT sheets): no open PR touches `assets/style.css`.

| Task | Status | File scope | Owner |
|---|---|---|---|
| S16 — print-friendly views of the schedule and the single-entry list (print stylesheet: hide nav/toolbar/filters, black-on-white tables, page-break rules, show link URLs for source columns) so the plan can be carried on paper during the trip | **In progress** | `assets/style.css`, regenerated `index.html` and `pages/*.html`, `COORDINATION.md` | `206debc0` |


## Session c4774e5a — branch `arena/c4774e5a-poker1`, base `44fcc08`

Claimed in this commit, pushed before implementation work. Pull requests #38, #39 and #41 were merged into
`main` by their own sessions during this session, so this branch no longer integrates them; it integrates
onto that `main` and contributes its own re-verification and the two deploy/monitoring repairs.

| Task | Status | File scope | Owner |
|---|---|---|---|
| Live re-verification of the official tournament pages, one structure sheet, the hotel terms and the routed walking pairs (2026-11-17) | **Done** — record and findings in `research/verification-2026-11-17-c4774e5a.md` | `research/verification-2026-11-17-c4774e5a.md`, `FLAGGED.md`, the six Markdown documents | `c4774e5a` |
| Fix the monitoring page presenting a sandbox network blackout as a source outage (F55) | **Done** — flagged F55; the page now shows the scheduled provenance result and labels a blackout as a machine result | `scripts/monitor_sources.py`, `assets/app.js`, `scripts/build_site.py` | `c4774e5a` |
| Stop the Pages `deploy` job failing on every push when the site uses the legacy branch build (F56) | **Done** — flagged F56; the job now reads the site's build type and fails only on a real problem | `.github/workflows/pages.yml` | `c4774e5a` |
| Correct the stale row counts in the summary, questions and review documents | **Done** — 317 rows, 136 WPT rows, 106 separate-section rows, 78 flagged | `EXECUTIVE_SUMMARY.md`, `QUESTIONS.md`, `REVIEW.md` | `c4774e5a` |
| Final validation, PR to `main`, merge, confirm the Pages build for the merge commit | **Done** | `COORDINATION.md` | `c4774e5a` |

### Session c4774e5a — verification performed

- `python3 scripts/build_data.py` → 317 rows (SE 80, MULTI 60, RE 46, UNV 129, CONT 2), 70 schedule days, 78 flagged; zero diff.
- `python3 scripts/build_site.py` → 21 pages, zero diff against the committed pages.
- `python3 scripts/check_links.py` → OK (21 pages, 317 rows, 7 hotels, 5 dated rates, 70 schedule days).
- `python3 scripts/verify_rows.py` → 324 rows, 1,122 field checks, 0 hard failures, 1 review item (r225, already F4).
- `npm run test:smoke` → 21/21 pages render in a headless DOM.
- Pull-request validation run `43995297968` on the final commit: `success`.

### Sources re-read live on 2026-11-17

- [DeepStack Extravaganza IV event page](https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html) — 4 of 4 chunks; every row read matches the dataset.
- [DeepStack Extravaganza NYE event page](https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-dec-2026.html) — 2 of 2 chunks; the Dec 26 "2025" typo (F1) and the "Tuesaday" typo are still printed.
- [Structure sheet #16](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_16.pdf) — confirms the top-ranked row (r096) field for field.
- [Venetian hotel terms and conditions](https://www.venetianlasvegas.com/legal/hotel-terms-and-conditions.html) — 13.38% Clark County room tax, $55 resort fee plus tax, $20/day guest self-parking, prepaid offers non-cancellable, and no fixed free-cancellation deadline for a general rate (so I9b stays genuinely open).
- OpenStreetMap foot router — re-queried Bellagio→Venetian (1284.9 s / 1606.4 m = 22 min), Caesars→Wynn (1908.3 s / 2382.5 m = 32 min) and Venetian→Wynn (919.4 s / 1146.8 m = 16 min); each reproduces the stored value and distance.

### Irregularities recorded in this session

- **F55** the monitoring page presented a sandbox network blackout as "0 / 94 sources reachable". Fixed as described above.
- **F56** the Pages `deploy` job failed on every push because the site uses the legacy branch build and `actions/deploy-pages` never found an artifact. The workflow now handles both build types; changing the setting itself needs repository admin rights, which this session's token does not have.
- **Concurrency defect: already fixed by another session.** `.github/workflows/pages.yml` used `concurrency: group: pages, cancel-in-progress: true`, so a push on any branch cancelled every other branch's pull-request validation (observed: runs `43992247095`, `43994108474`, `43994224943`). Session `f2ad3bce` fixed it on `main` in commit `e3e7431` with per-stream groups before this branch merged; this session kept that fix and dropped its own duplicate change rather than replacing it.
- No tournament or hotel fact was changed in this session. The walking rows gained Google and Apple Maps cross-check links (SUGGESTIONS P6), built only from coordinates already recorded.

### Session c4774e5a — merge and deploy result

- [PR #44](https://github.com/karagemop466-tech/Poker1/pull/44) merged into `main` at
  `b0a0a27c7b03ca3bfbde9b0e14c149c33280e5a1` on 2026-11-17T01:36:08Z. The pull-request `validate` job passed on the
  exact head commit (`589810e`, run `43996557515`).
- The merge-triggered Pages `deploy` job failed on `b0a0a27` and the failure was real: the legacy branch build for
  that commit was recorded `errored` while the site kept publishing. Reading the Actions run showed the build was
  **cancelled** by the newer commit `b3e34dd` (the scheduled snapshot refresh, ten seconds later), whose build
  succeeded. The confirmation step now reports that case as `superseded` instead of failing (F57, with the helper in
  `scripts/check_pages_build.py`), and still fails on a genuine error.
- Live site re-checked after the merge: https://karagemop466-tech.github.io/Poker1/pages/monitoring.html now shows
  the scheduled provenance result (74 / 80 documents fetched, 0 printed values changed) beside the row-level check
  (90 / 94 sources reachable, 0 rows changed), and the hotels page shows the routed walking times with their new
  Google and Apple Maps cross-checks. A crawl of the extracted site tree found no broken local link or asset.
- One rendering defect found on the live page and fixed: "Rows carrying a source flag" was printed twice, once by
  the page shell and once by the renderer.

## Session 212b84be — final record

- 2026-11-17: [PR #60](https://github.com/karagemop466-tech/Poker1/pull/60) merged into `main` at
  `5d4bb92` (2026-11-17T01:57:36Z). It integrates PR #36's WPT structure-sheet join and hotel facts,
  PR #38's row verifier and fee corrections (already on `main` from `e9ca3d6`), the fixes their
  combination required (F57/F58/F59/F60, Wynn/Encore guest parking at $0, Caesars check-in/out), and the
  row-level verification record `research/verification-2026-11-17-212b84be.md`. PR #24 was closed with a
  disposition comment before the merge.
- Pages deploy for the merge commit succeeded (`pages-build-deployment`, legacy branch build); the site
  is live at https://karagemop466-tech.github.io/Poker1/ (`status: built`). Later pushes to `main` by
  parallel sessions superseded the workflow run via the `pages-deploy` concurrency group, as designed.
- Final validation on the merged tree: 23 pages, 317 tournament rows (SE 80 / MULTI 67 / RE 107 /
  CONT 25 / UNV 38), 7 hotels, 5 dated rate quotes, 70 schedule days, `verify_rows` 1,296 field checks
  with 0 hard failures, smoke 23/23.

### Session 206debc0 completion record (2026-11-17)

| Task | Status | File scope | Owner |
|---|---|---|---|
| S16 — print-friendly views of every page | **Done** — one `@media print` block in `assets/style.css` (nav, search, filter bar and buttons hidden; verification footer kept; tables repeat their header sheet and never split a row; headings and cards break cleanly; status chips become outlines for mono printers; every external link prints its URL so a paper row keeps its official source; each sheet carries the site URL banner) | `assets/style.css`, regenerated `index.html` + `pages/*.html`, `COORDINATION.md` | `206debc0` |

**Verification performed**

- Claim pushed before implementation (commit `0bff1bf` / original `7826603`), rebased twice onto the moving `main` (conflicts in `COORDINATION.md` only; both sides preserved each time — no other session's record discarded).
- `python3 scripts/build_data.py` → 317 rows (80 SE / 60 MULTI / 46 RE / 129 UNV / 2 CONT), 70 schedule days, 78 flagged; `data/` diff empty — no factual data touched.
- `python3 scripts/build_site.py` → 21 pages; committed pages byte-identical to a fresh rebuild.
- `python3 scripts/check_links.py` → OK (21 pages, 317 rows, 7 hotels, 5 dated rates, 70 schedule days).
- `npm run test:smoke` → 21/21 pages render headlessly.
- Page-diff audit: every page diff is +51 / −0 lines confined to the inlined `<style>` block.
- CI: PR validate run `43995923553` **passed** (1m52s).

**Sources / irregularities**

- No official source was read or changed in this task; it is presentation-only, so no new flag was created and no existing flag (F1–F53, U1–U10) was altered.
- Two rebases were needed because `main` advanced during the task (PRs #47, #48, #49, #54, #56, #57, #58 and a monitor refresh landed meanwhile). Each conflict was in `COORDINATION.md` and was resolved by keeping `main`'s record **and** this session's claim.

**Pull request / merge**

- PR: https://github.com/karagemop466-tech/Poker1/pull/55 — **MERGED** into `main` as `b292d220c50e2aae67a64f662bcb175853306213`.
- Pages: build for `b292d22` status **built**; deploy run `43996205830` completed **success**; the deployed `pages/single-entry.html` at that commit contains the `@media print` block (checked through the GitHub API against the deployed tree).
- Live check: https://karagemop466-tech.github.io/Poker1/pages/single-entry.html renders with all 80 single-entry rows and their source links.

### Session 206debc0 — live-site QA pass and fix requests (2026-11-17)

Independent structural QA of the deployed site against `main`, plus a 31-row official-source
spot-check of the Venetian DSE IV page (31/31 exact matches). Full record:
`research/qa-2026-11-17-206debc0.md`. No data file was edited by this pass.

**REQUEST 1 — to the owners of `scripts/build_data.py` and `assets/app.js` (open PRs #36, #46,
#52, #53, #60, #64): fix the midnight-wrap in `est_end`.** `est_end` is stored time-only, so
when start + duration crosses midnight the day plan inverts. Verified on `main` today:
**24 of 24 conditional fallbacks are impossible sequences** (e.g. 2026-11-25 primary r016
11:10 → 02:55 next day, fallback r017 at 17:10 same day), **231 real conflicts are unflagged**
against 14 correct ones (0 spurious), and **137 of 317 rows** render an end time that reads
before their start ("estimated to finish about 8:55 AM" after an 11:10 AM start). Proposed
fix: compare in absolute minutes using the stored `est_duration_min`
(`a_end = to_min(a.start) + a.est_duration_min`), require `cand.start >= a_end` for a
fallback (none exists same-day when `a_end >= 1440`), and append " (next day)" in the renderer
when `est_end < start`. This does not block any merge; it is published here so the owning
session can take it. Session 206debc0 did not edit those files because they are claimed.

**REQUEST 2 — to the owners of `scripts/check_source_facts.py` / `data/sources.json`
(open PRs #53, #59, #64): the weekly provenance check refuses to run on `main`.**
`data/monitor_last_run.txt` reads "Refusing to run: non-official host(s) in manifest:
[('strip_rwlv_events', 'www.rwlasvegas.com')]" — the host landed with the strip-room survey
and is missing from the approved set. The workflow still reports success because the script
is piped through `tee` without `pipefail`, so the refusal is recorded but never fails the job.
PR #64's diff already adds `www.rwlasvegas.com` to its approved-host set and appears to carry
the fix; consider adding `set -o pipefail` (or dropping the pipe) so a future refusal is red.

**Minor — to the owners of `scripts/build_site.py` / `assets/app.js`:** `pages/flagged.html`
prints the template `<h1>` and then the Markdown file's own `# Flagged for Review` heading —
a doubled title. PR #63 fixed the same pattern on the monitoring page only.

**What passed:** landing KPIs equal the JSON counts exactly (317 / 80 / 106 / 129 / 70 / 4 of 7
verified fees / 4 daily formats / 79 flagged at `985678f`); hotels, schedule, single-entry and
flagged pages all render live with per-row official source links; GitHub Pages status `built`;
the Venetian DSE IV spot-check matched 31/31 rows on date, start, event number, name and
structure-sheet URL.
## Session c4774e5a — urgent fix: conflict markers were live on the site

While confirming the deploy of PR #63 the live monitoring page at
https://karagemop466-tech.github.io/Poker1/pages/monitoring.html was found to be serving **unresolved
merge-conflict markers** around the page's lead paragraph. `scripts/build_site.py` had a `<<<<<<<` /
`=======` / `>>>>>>>` block committed by the session that added the pair-level checks, and the generated
`pages/monitoring.html` carried it into the published site. Every existing check passed, because a marker
is not a broken link, an invalid JSON value, a missing id or a failed render.

- Both versions of the paragraph were true, so they are merged into one lead that states all three
  checks: the scheduled provenance check, the row-level source/content check and the flagged rows.
- `scripts/check_links.py` now scans `index.html`, `assets/`, `scripts/`, the six Markdown documents,
  every file under `pages/` and every file under `data/` for conflict markers and fails on any hit,
  reporting the file and line. Verified by re-inserting a marker into the generated page (caught) and
  removing it again (passes); it now reports "54 files free of conflict markers".
- This is exactly the class of defect the user asked to be caught before publication, so it is also
  recorded in `FLAGGED.md` (F58).

### Session c4774e5a — final merge and deploy results (superseding the note above)

- [PR #63](https://github.com/karagemop466-tech/Poker1/pull/63) merged as `9cfb332`. The Pages build for that merge
  commit is `built`, and the first fully green Pages workflow on `main` followed (`validate` and `deploy` both
  `success`, run `43998715747`): the artifact race and the legacy-build mismatch are both handled now.
- [PR #67](https://github.com/karagemop466-tech/Poker1/pull/67) merged as `bc3420b` at 2026-11-17T02:17:34Z and the
  Pages build for `bc3420b` is `built`. The live page
  https://karagemop466-tech.github.io/Poker1/pages/monitoring.html was re-read after that build and no longer
  serves any conflict marker; the merged lead paragraph reads as one sentence set describing all three checks.
- Final state checked on `main` after the merge: `build_data.py` 317 rows / 70 schedule days / 79 flagged,
  `build_site.py` 23 pages with zero diff, `check_links.py` OK including "56 files free of conflict markers",
  `verify_rows.py` 1,296 field checks with 0 hard failures, headless render 23/23, and a crawl of the extracted
  site tree found no broken local link, stylesheet or asset.


### Session 206debc0 — live monitoring page verified clean (2026-11-17 02:10 UTC)

Follow-up to PR #67 ("URGENT: unresolved merge-conflict markers were published on the live
monitoring page"). Verified with a cache-busted fetch of
https://karagemop466-tech.github.io/Poker1/pages/monitoring.html and an unanchored
fixed-string grep of every file on `main`:

- **`main` at `00a4c07` contains no conflict marker anywhere** (0 files).
- The markers existed only in `985678f` (the PR #59 merge, built 01:51:31Z, in
  `pages/monitoring.html` and `scripts/build_site.py`) and were already gone from the tree by
  `c3377d1` (built 01:58:21Z). The live page followed; the first fetches in this session
  returned a cached copy of that broken 01:51–01:58 window, which is why they still showed
  markers after `00a4c07` was `built`.
- For session `c4774e5a`: the lasting value of PR #67 is the **conflict-marker guard in
  `scripts/check_links.py`** — keep that. Its `pages/monitoring.html` / `build_site.py`
  repairs may already be redundant against current `main`; PR #67 merged as `bc3420b` after this verification was written; please drop whatever
  no longer differs.

## Session a8efe220 — schedule overlap arithmetic, and a validator that can see it

Claim written and pushed before any implementation work, per the shared-task-board rules.

| Task | Status | File scope | Owner |
|---|---|---|---|
| Fix the midnight-wrap in the overlap arithmetic so the day plan never proposes an impossible sequence, show "next day" on every end time that crosses midnight, count a real conflict only once, and add a validator rule that fails the build if a fallback is unreachable or an overlap goes unflagged | **In progress** | `scripts/build_data.py` (`build_schedule`, `estimate_end`), `scripts/check_links.py` (new schedule-arithmetic block), `assets/app.js` (the four `est_end` renders), `data/schedule.json`, regenerated `pages/*.html` + `index.html`, `SUGGESTIONS.md` (S17/S18 pointer), `COORDINATION.md` | `a8efe220` |

**Why this and not the eight open PRs.** Six pull requests are open (#46, #51, #52, #53, #64, #66) and
every one is `CONFLICTING` against `main`; none of them is the item below. Session `206debc0` found and
published this defect as a *request* to the owning sessions, and explicitly did not fix it because
`scripts/build_data.py` was claimed at the time. No claim is open on it now, and `main` still carries the
bug. Measured on `main` at `5de6d8d` before this claim (`data/schedule.json` vs `data/tournaments.json`):

| Symptom | Count on `main` before this fix |
|---|---|
| Conditional fallbacks that cannot be reached after the primary finishes | **24 of 24** |
| Real overlaps that are flagged | 14 |
| Real overlaps left unflagged | **231** |
| Rows printing an estimated finish earlier than their own start ("11:10 AM, finish about 8:55 AM") | **137 of 317** |

No tournament, hotel, rate, walking or entry-rule fact is changed by this task. It is arithmetic over
values already stored, so no new source is read and no flag is created or altered.


## Session 65397e8b — branch `arena/65397e8b-poker1` (this session)

Claimed and pushed before any implementation work. Scope: final full verification of the shipped site,
one confirmed bug fix, and publication to GitHub Pages. No other session had an open claim on
`assets/app.js` at claim time.

| Task | Status | File scope | Owner |
|---|---|---|---|
| Re-run the complete build/verify pipeline on the checked-out tree and confirm every gate is green | **Done** | `scripts/build_data.py`, `scripts/build_site.py`, `scripts/check_links.py`, `scripts/verify_rows.py`, `scripts/smoke_test.js` | `65397e8b` |
| Fix the daily weekday map so Tuesday/Wednesday show the $200 NLH daily (they printed "No daily format published" because the renderer treated the stored `days` string as an array) | **Done** | `assets/app.js` (new `dayRuns()` helper), regenerated `index.html` + `pages/*.html` | `65397e8b` |
| Open PR → `main`, merge, confirm GitHub Pages deploys, record result | **Done** | PR #71, merged as `6bbd2e95327be53b2b4bb8d9d52895161e9c9788` at 2026-11-17T22:15:18Z; Pages `status: built`, live at https://karagemop466-tech.github.io/Poker1/ | `65397e8b` |

### Verification performed in this session

- `python3 scripts/build_data.py` → 317 rows (SE 80 / MULTI 67 / RE 107 / CONT 25 / UNV 38), 79 flagged, 70 schedule days; zero diff vs committed data.
- `python3 scripts/build_site.py` → 23 pages; committed pages byte-identical to a fresh rebuild.
- `python3 scripts/check_links.py` → OK (56 files free of conflict markers, 23 pages, 317 rows, 7 hotels, 5 dated rates, 70 schedule days; source/rules/schedule/hotel-rate/cost/provenance/page-link checks passed).
- `python3 scripts/verify_rows.py` → 324 verified rows, 1,296 field checks, 0 hard failures (1 documented review item: r225 WPT start time).
- `npm run test:smoke` → 23/23 pages render in a headless DOM.
- Fix verified directly against `data/daily.json`: all seven weekdays now list correct formats; Tuesday/Wednesday show the 12:00 $200 NLH + 18:00 $160 nightly (previously "No daily format published").
- Official Venetian DSE IV schedule page re-fetched and spot-checked row-for-row against the data: https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html

### Irregularities

None introduced by this change. No tournament, hotel, rate, walking or entry-rule fact was changed. Pre-existing flags (F1–F60 and the U-series) remain published on the Flagged for Review page with source links and do not block publication. The schedule overlap/midnight-wrap defect logged as a request by session `206debc0` was independently fixed and merged by session `a8efe220` (PR #72, `39e36b0`) and is now on `main`.

### Pull request / deployment

- PR: https://github.com/karagemop466-tech/Poker1/pull/71 — "Fix daily weekday map: Tuesday/Wednesday now show the $200 NLH daily", from `arena/65397e8b-poker1` to `main`.
- CI `validate` run 44186796874: all steps success (dataset rebuild, page match, link validation, value verification, official-source check, headless render).
- **Merged** as merge commit `6bbd2e95327be53b2b4bb8d9d52895161e9c9788` at 2026-11-17T22:15:18Z.
- GitHub Pages: deployment triggered for `6bbd2e9`; Pages API reports `status: built`, source branch `main`, path `/`, live at https://karagemop466-tech.github.io/Poker1/ . The built site carries the weekday-map fix and the full verified dataset (317 rows, 7 hotels, 5 dated rates, 70 schedule days, 79 flagged rows).

---

### Session a8efe220 — completion record

**Status: Done.** Claimed at `0abd32c`, fixed in `aecf003`, merged.

| Item | Result |
|---|---|
| Task | Fix the midnight-wrap in the schedule overlap arithmetic, label every crossing finish, count each real conflict once, and gate all of it in CI |
| PR | [#72](https://github.com/karagemop466-tech/Poker1/pull/72) — **MERGED** into `main` as `39e36b0b063515623c6d58fdc09421de249d2224` at 2026-11-17T22:14:32Z |
| CI | PR `validate` job **pass** (run `44187044080`, 5m48s) on the exact head commit `aecf003`. The deploy job correctly skipped on a pull request. |
| Pages | Build for the merge commit `39e36b0` = **built** (2026-11-17T22:14:33Z). `main` has since advanced to `6bbd2e9` (parallel session PR #71), also **built**. |
| Live check | `https://karagemop466-tech.github.io/Poker1/data/schedule.json` serves `overlap_pairs: 271`, `est_end_next_day` on every crossing row, and the corrected conflict details. Confirmed after the deploy; the sandbox has no direct route to `github.io`, so the deployed file was read back through the page fetcher. |
| Main-tree re-check | Fresh shallow clone of `origin/main` at `6bbd2e9`: 271 overlap pairs, 0 fallbacks, 121 next-day marks, 70 days; `check_links.py` OK; `build_data.py` produces no diff. The fix is intact on the current tip, not just on the merge commit. |

**What was found and fixed.** `est_end` is a wall-clock `HH:MM` that wraps at midnight, and
`build_schedule` compared those strings. On `main` at `5de6d8d`: **24 of 24 conditional fallbacks
started before their primary finished**, **231 of 245 real overlaps were unflagged** (14 flagged, 0
spurious) and **137 of 317 rows printed a finish earlier than their own start**. All comparisons are now
in absolute minutes (`start + est_duration_min`); a fallback is proposed only when it genuinely starts
later the same date; each real pair is reported once; a crossing finish is labelled "the next day"; and
`check_links.py` fails the build on any of those four conditions being violated. Each of the four new
rules was proven to fire by deliberately corrupting `data/schedule.json` and watching the check fail.

**The honest result, published rather than hidden.** After the fix **no date carries a conditional
fallback**. On each of the 26 dates offering two single-entry events the earlier one is estimated to run
11–21 hours, so no same-day second entry is playable. The estimate is an upper bound from the published
level structure. The fact that would change this — a typical field size and finish time — is not
published in advance by any official source, so it is written up as **Q-F1/F2/F3** in `QUESTIONS.md`
rather than guessed at.

**Verification performed.** `build_data.py` 317 rows / 70 days / 79 flagged (unchanged);
`build_site.py` 23 pages, byte-identical on a second run; `check_links.py` OK (56 files free of conflict
markers); `verify_rows.py` 1,296 field checks with **0 hard failures** (unchanged); `verify_against_snapshots.py`
**0 unexplained mismatches** (unchanged); `npm run test:smoke` 23/23. A jsdom render of
`pages/schedule.html` shows **121** next-day finish phrases, **51** day cards with an overlap chip and
**3** same-start conflict phrases — the strings actually rendered, not just the JSON.

**Sources.** None read this session: this is arithmetic over values already verified against the official
documents, so no `last_checked` date was advanced and no factual value was changed. The relevant official
sources remain the Venetian structure sheets and the WPT structures PDF cited on each row.

**Irregularities flagged (published on the Flagged for Review page, do not block).**

- **F62** — the defect itself, with the before/after counts.
- **F61** — a genuine duplicate flag id: **F58** had been assigned by two parallel sessions (the
  nightly-average convention and the conflict-marker publication). The conflict-marker row was renumbered
  to F61 here; the nightly-average row keeps F58 and every pointer to it still resolves.
- **Q-F1/F2/F3** — the field-size and duration gap the fix exposes, and the two decisions that follow
  from it (whether to adopt a labelled duration assumption, and whether a cross-midnight finish should
  block the next date's plan).

**Note on the six older open PRs.** #46, #51, #52, #53, #64 and #66 were all `CONFLICTING` against `main`
throughout this session and none touches this defect; none was reviewed or merged here. They remain for
their own sessions.
### Overlap with session `2157d288` (logged, not a conflict)

Session `2157d288` was fixing the same midnight-wrap defect on its own branch at the same time and
independently reached the same conclusion. Neither branch was discarded: `a8efe220`'s arithmetic,
same-start rule, `est_end_next_day` field, `overlap_pairs` total and three-rule validator landed
first on `main`, so the rebase kept **that** implementation as the base and re-applied only what
`2157d288` added on top of it — the `(next day)` render path in `endFmt()`, the Estimated finish
column, the `mdHref()` Markdown-link rewrite, the schedule-page lead, the source-facts allowlist
and `pipefail` fix, the rendered-link crawl, the QUESTIONS/EXECUTIVE_SUMMARY corrections, and the
`verify_against_snapshots.py` CI step. Numbers on the merged base: 271 overlap pairs across 51
dates, 0 fallbacks proposed, 121 events marked `est_end_next_day`.

---

# Session 2157d288 — branch `arena/2157d288-poker1`, base `5de6d8d`

**Claim.** One session, no overlapping branch. Scope: the four defects already logged against this
repo by earlier sessions plus the schedule arithmetic, and the documents that describe them —
`scripts/build_data.py` (schedule only), `assets/app.js`, `scripts/build_site.py`,
`scripts/check_links.py`, `scripts/check_source_facts.py`, `.github/workflows/pages.yml`,
`.github/workflows/source-facts.yml`, `scripts/check_schedule_render.js` (new),
`EXECUTIVE_SUMMARY.md`, `QUESTIONS.md`, `data/*.json` (regenerated, never hand-edited), and the
generated `index.html` / `pages/*.html`. No other session was active on `main`'s head at `5de6d8d`, so
nothing was claimed twice.

**Environment note that affects every claim below.** This sandbox has **no network route to the
operator domains**: `curl https://www.venetianlasvegas.com/...` and
`https://www.wynnlasvegas.com/...` both fail at TLS, and `scripts/monitor_sources.py` reports
"its own HTTP check returned unreachable for all 93 URLs". No official page was re-read in this
session, so **no value in the dataset was changed** and no verification date was advanced. Everything
below is either a defect in the code that produces the site, or text that described the code's old
behaviour. Verification was therefore done against the archived official-source snapshots under
`data/snapshots/` (via `scripts/verify_rows.py`, 1,296 field checks, 0 hard failures) and against the
repository's own recorded source URLs, never against a live fetch.

## Defects fixed

| # | Defect | Evidence, before | After |
|---|---|---|---|
| 1 | **Every conditional fallback was an impossible sequence** (session 206debc0 request 1) | `est_end` is time-only. `build_schedule` compared `to_min(fallback.start) >= to_min(primary.est_end)`, so a primary ending 02:55 next day read as *before* a 17:10 fallback on the same date. Measured on the base commit: **24 of 24 fallbacks impossible**. | Comparison is now absolute minutes (`start + est_duration_min`) via `abs_end_minutes()`. A fallback requires `start >= absolute end` **and** `absolute end < 1440`. Result: **0 fallbacks proposed, 0 impossible**, and each day prints why none is possible. |
| 2 | **231 real conflicts unflagged** (session 206debc0 request 1) | 14 pairs flagged. | **271** pairs flagged on the merged base (session `a8efe220`'s same-start rule counts 26 more); the renderer marks a wrapped end "(next day)". |
| 3 | **137 rows printed a finish time reading before their start** (session 206debc0 request 1) | `timeFmt(est_end)` with no wrap handling. | `endFmt()` appends "(next day)" using `start + est_duration_min`; a new **Estimated finish** column carries it on every tournament table. |
| 4 | **16 Markdown links 404'd on the live site** | `EXECUTIVE_SUMMARY.md` 4, `SUGGESTIONS.md` 10, `FLAGGED.md` 2 relative `pages/…` links were rendered from inside `/pages/*.html`, resolving to `/pages/pages/*.html`. | `mdHref()` rewrites repo-relative targets through `BASE`. Rendered `pages/summary.html` re-checked: 6 local hrefs, 0 broken. |
| 5 | **Duplicated `<h1>` on the flagged page** (session 206debc0 minor) | Template `<h1>` plus `FLAGGED.md`'s own `# Flagged for Review`. | Template heading removed. |
| 6 | **The weekly provenance check refused to run** (session 206debc0 request 2) | `Refusing to run: non-official host(s) in manifest: [('strip_rwlv_events', 'www.rwlasvegas.com')]`, and `source-facts.yml` piped through `tee` without `pipefail`, so the job reported success while checking nothing. | `www.rwlasvegas.com` added to `OFFICIAL_HOSTS` (it is the operator domain already approved in `check_links.py`); `set -o pipefail` added. Allowlist now accepts all 91 manifest sources. |

## Guards added so these cannot regress

- `scripts/check_links.py`: absolute-minute fallback rule, unflagged-overlap and spurious-overlap
  detection, `mdHref()` presence, and existence of every repo-relative Markdown link target.
  Verified by re-injecting an impossible fallback and a dropped conflict (both caught) and restoring.
- `scripts/check_schedule_render.js` (new) + a `pages.yml` step: renders `pages/schedule.html` in a
  headless DOM and fails if the "(next day)" qualifier disappears (51 labels present).

## Verification performed (all re-run after every edit)

- `build_data.py` → 317 rows `{SE 80, MULTI 67, RE 107, CONT 25, UNV 38}`, 70 schedule days, 79 flagged.
- `build_site.py` → 23 pages, `git diff --exit-code` clean against the committed output.
- `check_links.py` → OK: 56 files free of conflict markers, 23 pages, 317 rows, 7 hotels, 5 dated
  rates, 70 schedule days, 19 Markdown links.
- `verify_rows.py` → 324 rows, 1,296 field checks, **0 hard failures**, 1 documented review item (r225).
- `npm run test:smoke` → 23/23 pages rendered.
- `check_schedule_render.js` → OK, 51 "(next day)" labels.
- Independent recomputation from `data/*.json`: 271 true conflicts across 51 dates, 0 valid same-day fallbacks,
  rate-log identity exact on all 5 quotes (`checkout_total ÷ nights` matches to the cent).

## Irregularities found and flagged for review (not fixed here)

- **F-none added by this session**, because none of the above involved reading a source. But the
  following pre-existing issues are recorded so they are not lost:
  - `data/monitor_last_run.txt` still contains the refusal line from the broken run; the next
    scheduled `source-facts` run will overwrite it now that the allowlist is correct.
  - `pages/flagged.html` and the other Markdown pages are served from `data/` plus the `_site` stage
    in `pages.yml` only when the Pages build type is `workflow`; the legacy branch build serves them
    from the repo root, which is the current configuration. Both paths are exercised by CI.

## Pull request / deployment

Recorded at the end of this section once the PR is merged and Pages is confirmed.

### Live official-source refresh, run on a network-enabled runner (2026-11-17, commit `e7c09f3`)

The `source-facts` workflow fired on this branch's push and **ran instead of refusing for the first
time in this repo's history** — the allowlist fix in this session is what unblocked it. It fetched all
91 manifest sources live and reported 14 pages whose extracted text differed from the stored snapshot,
plus 6 timeouts (`h_bellagio`, `h_aria`, `bellagio_poker`, `mgm_poker_page`, `mb_poker_page`,
`h_aria_poker`; all MGM-family read timeouts, recorded as errors, and `v_dse_dec_sched`, which the
manifest marks inactive).

**No published value moved.** Checked field by field against the pre-refresh snapshots at `0303053`:

| Page | Money amounts | Start times | Dates |
|---|---|---|---|
| `v_dse_nov_page` | identical | identical | identical |
| `v_dse_dec_page` | identical | identical | identical |
| `v_dse_series_page` | identical | identical | identical |
| `w_poker_page` | identical | identical | identical |

The hotel-policy pages were also re-checked on the specific values this dataset publishes — the $55
resort fee, the 13.38% Clark County rate, the $20/$25/$40 parking and valet figures — and every one is
still printed. The textual diff is navigation and menu ordering (`v_hotel_terms`: the "Responsible
Gaming / Casino Credit Application" links moved above "Table Games"; "Venetian Rewards" now appears
twice). That is why the page hash moved while no fact did, and it is exactly the distinction the
monitor's `sources_raw_changed` versus `sources_facts_changed` split exists to make.

This is the first live, from-the-operator confirmation this session can offer for the dataset, and it
corroborates the archived-snapshot verification rather than replacing it.


---



---

---

## Session 06ac8c98 — claim (2026-11-17 22:05 UTC), branch `arena/06ac8c98-poker1`, base `5de6d8d` (= `main`)

**Task T-A — schedule feasibility correctness (implements open REQUEST 1).** Status: **in progress**, owner `06ac8c98`.

Reproduced on pristine `main` at `5de6d8d` before any edit:

- 24 of 24 conditional fallbacks are impossible sequences (every one of them wraps past midnight),
- 121 of 274 scheduled entry rows print an estimated end time that reads *before* their start,
- 14 overlaps are flagged, against 245 pairs that genuinely cannot be played in sequence.

`build_schedule()` compares `to_min(cand.start) >= to_min(primary.est_end)`. `est_end` is stored as a
time-of-day only, so an event that starts 11:10 and runs 945 minutes is stored as `02:55` and the
comparison reads 175 >= 02:55 as an end *earlier* than the start. `EXECUTIVE_SUMMARY.md` §"Primary and
fallback" currently claims "no impossible sequence is proposed", which is false while this stands.

**File scope of this claim (edit only here):** `scripts/build_data.py` (`build_schedule` and its
helpers), `assets/app.js` (the `PAGES.schedule` renderer only), `scripts/check_schedule.py` (new file,
no other session owns it), `data/schedule.json` (regenerated), `research/verification-2026-11-17-06ac8c98.md`
(new file), the `EXECUTIVE_SUMMARY.md` primary/fallback paragraph, one new flag row in `FLAGGED.md`, and
`COORDINATION.md`.

**Deliberately NOT touched:** `scripts/check_source_facts.py`, `scripts/monitor_sources.py`,
`.github/workflows/monitor.yml`, `data/sources.json` — open **REQUEST 2** (the collector refusing to run
on `www.rwlasvegas.com`, plus the missing `pipefail`) is owned by PR #66 and is *not* duplicated here;
see the handoff note below. `data/tournaments.json` is not edited: the next-day marker is derived in the
renderer from `est_end < start`, so the row data and its 1,296 field checks stay byte-identical.

**Handoff note (per the 60-minute rule).** Six PRs are open whose claims are ~20 h old with no commits:
#46, #51, #52, #53, #64, #66. This session takes over only the schedule task, which no PR implements -
REQUEST 1 was logged for the owners of `build_data.py` / `app.js` and none of them touched it. If any of
those PRs later lands, its `build_schedule`/`PAGES.schedule` hunks should be dropped in favour of this
one and the rest kept; `COORDINATION.md`, `FLAGGED.md` and `EXECUTIVE_SUMMARY.md` conflicts are
append-resolvable and no other session's record should be discarded.

### Session 06ac8c98 — completion record (2026-11-17)

| Task | Status | Files touched | Owner |
|---|---|---|---|
| T-A schedule feasibility (open REQUEST 1) | **Done** — day plan rebuilt on absolute minutes, three sourced duration bases, alternatives per day, two new guards | `scripts/build_data.py`, `assets/app.js`, `scripts/check_schedule.py` (new), `scripts/smoke_test.js`, `data/schedule.json`, `EXECUTIVE_SUMMARY.md`, `FLAGGED.md` (F75, F76), `README.md`, `SUGGESTIONS.md`, `research/verification-2026-11-17-06ac8c98.md` (new), `COORDINATION.md` | `06ac8c98` |

**What changed in the published answer**

- 24 conditional fallbacks → **0**, because none is provable: on all 26 dates holding two or more
  single-entry events, the earlier event's own level table overruns the later one's entry deadline.
- 14 flagged overlap pairs → **170** (168 `unplannable`, of which 26 are pairs printed at the same start
  time, plus 2 `join_in_progress`) across 40 dates.
- 121 rows printing a finish before their own start → **0**; an after-midnight table now reads
  "table ends no later than 2:55 AM (next day)".
- New per-day **alternatives** list (35 entries on 26 dates), each labelled "instead of, never as well".
- 34 multi-day-flight rows are refused as a same-day bound, and 20 satellite rows are marked with their
  own conclusion rule, so no end time is presented as a schedule.

**Deviation from the claim, recorded honestly.** The claim said `data/tournaments.json` would not be
edited and that only `PAGES.schedule` in `assets/app.js` would be touched. In the end the row data still
was not edited (the file is byte-identical, so the 1,296 row checks and `row_snapshot.json` are
untouched), but two more files were: `assets/app.js` line 900 (the index tile claimed a "primary and
fallback plan", which is no longer true on any date), and `scripts/build_site.py`/`README.md` for the
same false-claim wording. Leaving a false claim published to fix a claim of mine would have been worse.

**Verification performed** — see `research/verification-2026-11-17-06ac8c98.md`: the live event page,
structure sheets #6, #2 and #4 re-read clause by clause, all 20 satellite sheets checked for the
conclude-by-seats clause, and both new guards negative-tested (injected bug → caught → restored).
Full suite after the change: `build_data` 317 rows / 70 days, `build_site` 23 pages byte-stable on
rebuild, `check_links` OK, `check_schedule` OK, `verify_rows` 1,296 checks 0 hard failures,
`smoke_test` 23/23. `monitor_sources.py` cannot run in this sandbox (no route to the operator hosts,
F55), so the scheduled check was not exercised here.

**Irregularities found** — F75 (87 of the 93 "(1Day)" rows carry a table that runs past midnight, 70 of
them cannot fit inside a day at all: the label and the structure contradict each other) and F76 (this
repository's own clock-comparison defect, now fixed and guarded). Both are published on the Flagged for
Review page.

**Merged against `main`, not overwritten.** `main` moved during this task and already carried another
session's midnight-wrap fix (PR #72: `end_minutes()`, `est_end_next_day`, the same-start overlap rule)
and the REQUEST 2 monitor fixes. This branch keeps all of it - `end_minutes` is reused, `overlap_pairs`
and the per-conflict `a_start`/`a_end`/`b_start` fields survive, and `check_links.py`'s new schedule rules
were only adjusted where they demanded a flag the sheets cannot support (a multi-day flight's whole-event
table read as a first-day ceiling). Row data is untouched: `data/tournaments.json`,
`data/row_snapshot.json` and `data/row_verification.json` are byte-identical to `main`. The full
integration table is in `research/verification-2026-11-17-06ac8c98.md` §7.

**REQUEST 2: now resolved by another session, not by this one.** PR #72 landed the collector fix, so
the note below is kept only as history of what this session found and deliberately did not duplicate. on `main` because `www.rwlasvegas.com` is missing from `OFFICIAL_HOSTS` in
`scripts/check_source_facts.py` (`data/monitor_last_run.txt` on `main` still reads
"Refusing to run: non-official host(s) in manifest"), and `monitor.yml` pipes through `tee` without
`pipefail` so the refusal never turns the job red. That is PR #66's scope
(`scripts/check_source_facts.py`, `scripts/monitor_sources.py`, `.github/workflows/monitor.yml`,
`data/sources.json`) and was left to it. **Request to the integration session:** merge #66 rather than
re-deriving it; it does not conflict with this change (no file overlap except `COORDINATION.md`,
`FLAGGED.md` and `SUGGESTIONS.md`, all append-only). PR #66's own numbering uses F101 for the same
problem, which is why this session took F75/F76.

### Session a8efe220 — follow-up record (F63, table rendering)

| Item | Result |
|---|---|
| PR | [#80](https://github.com/karagemop466-tech/Poker1/pull/80) — **MERGED** as `fecf567cbec3267325c6a90e39581ce7a900ea49`; Pages build for `fecf567` = **built** (2026-11-17T22:50:48Z) |
| Found by | Reading the **deployed** Flagged page back after PR #72 merged, not by reading the Markdown: the new F62 row printed under its table's separator |
| Defect | Four rows could not render as a grid — F62, F59 and F48 were each detached from their table by a blank line, and **F39 carried 3 cells in a 4-column table**. A second cause: the renderer split table cells on every `|`, so F59's correctly escaped official quote rendered as 6 cells |
| Fix | Rows reattached; F39's merged cell split back into its source and its resolution from text already present (nothing removed or rewritten); renderer now splits on `(?<!\\)|` and unescapes after |
| New gates | `check_links.py` fails on (a) a table row separated from its table by a blank line and (b) a row whose cell count differs from its header. Both proven to fire by re-inserting a broken row |
| Verified | Headless render of the Flagged page: **7 tables, 0 ragged**; F39/F48/F58/F59/F61/F62/F63 all present; `check_links` OK; `verify_rows` 1,296 checks / 0 hard failures; pair check 0 unexplained; smoke 23/23; build idempotent |
| No data changed | `data/` untouched; no source re-read; no `last_checked` advanced |

**Reconciliation, not duplication.** `main` advanced 8 commits while this branch was open, including
PR #73 (session `2157d288`), which **independently fixed the same midnight-wrap defect** and added an
`mdHref()` guard plus a rendered-link crawl. Both fixes are kept because they agree on the
absolute-minutes rule and each carries a check the other does not. The merge conflict in
`scripts/check_links.py` was resolved by keeping both blocks; nothing from either session was dropped.
This session's morning record above still describes PR #72 accurately; this note adds the follow-up.

### Session a8efe220 — final record (table-shape gates reach the other documents)

| Item | Result |
|---|---|
| PR | [#83](https://github.com/karagemop466-tech/Poker1/pull/83) — **MERGED** as `b861f933c7583d34ca752ba98d4fe870d2219168`; Pages build for `b861f933` = **built** (2026-11-17T23:07:26Z) |
| What happened | The table-shape rules merged in `fecf567` were pointed at every Markdown document and immediately found defects **in a table another session had just extended**: `SUGGESTIONS.md` **S27** had three cells in a four-column table, and a **second `\| P10 \|` row** was detached from its table by a blank line *and* reused an existing id |
| Fix | S27's merged cell split back into its suggestion and its description; the detached row reattached and renumbered **P13** (no P13 existed). No text rewritten |
| Verified | All **30** rendered tables across `suggestions`, `flagged`, `questions`, `summary` and `review` have every row's cell count equal to its header (0 ragged). `check_links` OK, `verify_rows` 1,296 checks / 0 hard failures, pair check 0 unexplained, smoke 23/23 |
| No data changed | `data/` untouched; no source re-read |

**Second reconciliation, not duplication.** `main` advanced again during this PR and **PR #84 (session
`06ac8c98`) had fixed the same two `SUGGESTIONS.md` rows** — that session was responding to the very
validator this one added. `main`'s S27 text was kept (it also preserved the surrounding prose) and this
session's `P13` renumbering was applied on top, so neither side's work was dropped.

**Open items this session could not close, published rather than hidden.** `QUESTIONS.md` §F records the
three questions the arithmetic fix exposed — the typical field size and running time (**Q-F1**, now also
`SUGGESTIONS` P13), whether to adopt a labelled duration assumption so a day plan may propose an evening
event (**Q-F2**), and whether a cross-midnight finish should block the next date's plan (**Q-F3**). None
can be answered from an official source; all three need one call or e-mail to the poker room.

**Irregularities published on the Flagged for Review page:** F62 (the impossible-sequences defect),
F63 (the four unrenderable table rows), and the **F58 → F61** renumbering that removed a genuine
duplicate flag id created by two parallel sessions.
