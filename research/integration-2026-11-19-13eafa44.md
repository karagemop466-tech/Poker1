# Integration record — 2026-11-19 (session 13eafa44-poker1)

**Branch:** `arena/13eafa44-poker1` (from `a1361aa` = `origin/main`, post-#85)
**PR:** #98 (open → merged; see `COORDINATION.md` for the merge record)
**Scope claimed in COORDINATION.md:** takeover of the stale final-integration PRs #79, #81, #82 after `main` moved through #85.
**Live site:** https://karagemop466-tech.github.io/Poker1/ (deploy confirmation recorded in COORDINATION.md after merge)

## What this session did, in order

1. Read `COORDINATION.md`, claimed the stale-integration takeover, pushed the claim immediately (`60cfff2`).
2. Fetched and diffed all three open PRs against `main`. All three were DIRTY/CONFLICTING; none was merged wholesale. #82 predates main through ~#80 — a wholesale apply would have deleted main-only files and regressed `assets/app.js` (which carries `endFmt`, `toMinJS`, `mdHref`, the pipe-escape, the "Estimated finish" column — all kept). #79 predates the same fixes. #81's substantive fixes (absolute-minute comparisons, "(next day)" labels, `mdHref()`, doubled `<h1>`, provenance `pipefail`) are all already on `main`.
3. Copied the six official-source snapshots from the PR branches into `data/snapshots/` (byte-identical between #79 and #82 where both carried them), renamed/kept as-is. Nothing was fetched live: this sandbox has no route to operator hosts (F55) — an accidental fetch run of `check_source_facts.py` was reverted with `git checkout -- data/change_log.json` before any commit, leaving the 2026-11-17 provenance log intact.
4. Ported data/script changes with re-verification:
   - WPT/NLH renames + Ladies-satellite `$10,400 → $1,100` buy-in fix + 1F CES-suffix drop + Ladies/NIH correction notes. Zero `NIH` remains anywhere in `data/tournaments.json`.
   - `BELLAGIO_DAILY` (Friday $600 NLH, Saturday $1,000 NLH, Sunday $400 H.O.R.S.E.) and `CAESARS_DAILY` (4 daily formats) — rule numbers and level counts re-read line by line against `bellagio_*.txt` and `caesars_daily_flyer.txt` (FRI 28 levels, fee Rule 5, re-entry Rule 3; SAT 28 levels, fee Rule 7 + gratuity Rule 9, registration level 10; SUN 26 levels, fee Rule 1; Caesars flyer Version 6.19.2026: $100→$70/$30, $160→$115/$45, $50 add-on→$45/$5; close at start of level 7; 20-minute levels; $1,000 GTD). Bellagio Saturday keeps its printed contradictions (F79) and is unranked.
   - `CLARK_COUNTY_TAX` + `cc_tax_note()`: all seven strip-hotel rows now publish 13.38% verified (Resort Hotel, Stadium District & PGC, Appendix III components, effective 3-1-17, Clark County Code 4.08.010), with the licence numbers from the county guide's "As of April 2021" licensed-establishment table. The `1000389.RES-001` transposition in #82's flag text was corrected to `1003089.RES-001` (F81); the DBA column is quoted as printed, including the truncated "Casin".
   - `data/sources.json`: `caesars_poker_article` marked `active: false` (404 on 2026-11-17); `caesars_casino`, `caesars_daily_flyer`, `cc_tle_guide` added; `bellagio_poker` note records the content-host flyer policy (F40/S9 pattern). `check_source_facts.py --offline` confirmed the log is left unchanged — the weekly provenance workflow (`source-facts.yml`) re-fetches on merge because it triggers on `data/sources.json`.
   - `monitor.yml`: added cron `17 15 * * *` (7:17 a.m. PST trip window) next to `17 7 * * *`; added the missing `set -o pipefail` on the tee'd check step.
   - `check_links.py`/`check_source_facts.py`/`monitor_sources.py`: `clarkcountynv.gov` (+`www.`) accepted as an official government source host; daily rows may carry `late_reg_level`+`late_reg_text` instead of a printed clock time.
   - `data/walking.json`: rows now carry `hotel_name` and `destination` (derived from stored ids; labels say so).
5. Ported the site changes (app.js, NOT #82's older app.js): trip diary on the single-entry page (one line per playable day, estimated finish labelled "table maximum, estimate", deep link `pages/schedule.html#day-<date>`), `Daily feed` Room/Registration-closes/Source-document columns with level-based late registration, `Hotels` date pickers that build the official booking-engine URL for the picked dates (Venetian/Palazzo pattern only — the only date-parameter pattern read on an official page in the rate log; the other properties link their booking pages with no invented parameters), walking table prints property names and poker-room destinations, per-day "running after midnight, so no later event can be played on this date" note on the schedule page (this makes `check_schedule_render.js` pass — it was red on clean `main`).
6. FLAGGED.md: F18 amended with a dated correction (the WPT schedule never printed "NIH"); new section G records F77–F82 (county tax verification incl. the #82 transposition; Caesars article 404; Bellagio Saturday flyer contradictions; 1F CES suffix; SS# 02 Event #29 $10-vs-$20 conflict) and lists deliberately-not-ported material (#81's P1–P6, #79's colliding flag numbering, #82's wholesale reverts).
7. Rebuilt and verified (see below). `data/*.json` regenerated only via `scripts/build_data.py`; pages regenerated only via `scripts/build_site.py`.

## Verification results (2026-11-19)

| Check | Result |
|---|---|
| `python3 scripts/check_links.py` | OK — 23 pages, 317 tournament rows, 7 hotels, 5 dated rates, 70 schedule days, 20 markdown links, no conflict markers |
| `python3 scripts/verify_rows.py` | 1,296 field checks, **0 hard failures**, 1 documented review item (r225 WPT start 20:00 — interpretation, not a data error) |
| `npm test` | smoke **23/23** pages; `check_schedule_render: OK` (`(next day)` labels = 89); `check_rendered_links: 23 pages, 576 rendered local references, 0 broken` |
| Trip-diary render (jsdom) | 45 diary lines; no `undefined`/`NaN` leaked; links deep-link into the schedule page anchors |
| FRI/SAT/SUN level tables | re-read line by line: FRI 28 levels (through "28th Level 125,000"), SAT 28 levels, SUN 26 levels (through "26TH LEVEL 100,000") |
| County licence rows | all five licence numbers match the archived county table exactly, including the truncated DBA |
| `check_source_facts.py --offline` | change_log.json left unchanged (correct behaviour); no fetch was run from the sandbox |

## Known limitations and deliberate decisions

- Nightly rates/resort fees for Wynn, Encore, Bellagio, ARIA, Caesars Palace remain blank unless printed and quoted; the county tax record settles only tax class and rate.
- Bellagio Saturday and both Bellagio/Caesars daily rows are published but **not ranked**; none carries a single-entry claim.
- The Bellagio flyer PDFs are `document_url` only — cited through the official property page, never fetched as a source host (F40/S9; same treatment as MGM PDFs).
- The monitor/provenance jobs that re-fetch official sources could not be run from this sandbox (F55); they run in GitHub Actions (`monitor.yml` daily, twice; `source-facts.yml` weekly and on `data/sources.json` push). Their result is data recorded by CI, not by this session.
- `data/row_snapshot.json` shows 18 changed rows — all WPT/NLH renames plus the re-verification of the renamed rows; every change was matched by a full `verify_rows.py` pass.
- PR #81 and PR #79 are closed as superseded by #98; PR #82 likewise. Their content is catalogued in FLAGGED.md section G and in the #98 description.
