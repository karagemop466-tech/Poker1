# Repo Review and Verification Log

Session `baba1a15` · Branch `arena/baba1a15-poker1` (base `2dc4120`, from `main`) · Checked 2026-11-16

This log records what was read, what was found, what was changed, and what is still missing. The
earlier session (`1fafb3d2`) findings are kept where they still apply.

## 1. Repository state at the start of this session

| Item | Result | Evidence |
|---|---|---|
| Branch | `arena/baba1a15-poker1`, based on `2dc4120` | `git log` |
| Published site | https://karagemop466-tech.github.io/Poker1/ | `COORDINATION.md` deployment log |
| Rows in the published dataset | 225 (33 single entry, 15 possible multi-entry, 6 re-entry, 171 unverified) | `data/tournaments.json` at `bf597a0` |
| Structure sheets read | 16 of 37 Venetian November sheets, 0 of 15 Venetian December sheets, 2 of 8 Wynn WPT structure sections | `research/structure-sheets-verification.md` |
| Hotel data | 7 hotels, no room rate verified, no dated rate log | `data/hotels.json` |
| Site | 11 pages, a text filter and a series dropdown only | `assets/app.js` |

## 2. What this session read

Every source below was opened directly and read on **2026-11-16**. The full field-by-field log is in
`research/structure-sheets-verification.md`.

| Source | Coverage |
|---|---|
| `dse_nov_2026-structure_1.pdf` … `_37.pdf` | **37 of 37** |
| `dse_dec_2026-structure_1.pdf` … `_15.pdf` | **15 of 15** |
| `dse-nov-2026.html` | read in full, four chunks |
| `dse-dec-2026.html` | read in full, two chunks |
| `WPT_World_Championship_Schedule.pdf` | read in full, Nov 27 – Dec 21, 2026 |
| `WPT_World_Championship_Structures.pdf` | read in full, eight sections |
| `Wynn_Signature_Series_Schedule.pdf` | read in full, Jan 11 – 24, 2027 |
| `Wynn_Signature_Series_Structures.pdf` | read - "COMING SOON" placeholder only |
| Wynn daily poster and daily structures | read in full |
| Venetian and Wynn hotel terms, resort fee, poker suite rates, map, booking engine, poker pages | read |

No official source used by the dataset is left unread.

## 3. Irregularities found and how each was handled

| # | Area | Irregularity | Handling |
|---|---|---|---|
| R1 | Data completeness | The draft omitted **seven** November milestone-satellite rows and **thirteen** December milestone-satellite rows, plus the NYE Ante Up flight 1B on Dec 28, because the official event pages list them in rows the earlier draft did not transcribe. | All twenty-one rows added, with their own structure sheets (19, 24, 25 in November; 4, 5, 7 in December). |
| R2 | Data completeness | The draft's Wynn WPT schedule was missing 43 printed rows: the Day 2, Day 3, Day 4 and final-table continuations, 28 milestone and satellite rows, and the December 16 block. | The WPT schedule was rebuilt row by row from the official PDF, including the published chip counts and level counts. |
| R3 | Date correctness | The draft had several Wynn rows on the wrong date. The PDF prints one block under the heading "Dec. 18 Wednesday"; December 18, 2026 is a Friday and the PDF prints a separate "Dec. 18 Friday" block. | The block is stored as **December 16, 2026**, the only reading that also fits the World Championship day order. Every affected row carries the flag and the reasoning. |
| R4 | Source conflict | The schedule PDF prints the December 21 $600 NLH Turbo at 8 p.m.; the $600 NLH Turbo structure sheet lists "Monday, December 21, 2026 at 6 p.m." | Both times kept, the schedule time stored, the conflict flagged on the row. |
| R5 | Source conflict | The schedule PDF prints a buy-in in each "Day 2" row that belongs to a different event than the day it names. | The structure sheet is treated as authoritative for the day-to-event link, the printed value is kept in the row flag. |
| R6 | Date typo | The NYE event page prints the Dec 26 rows as "Saturday, December 26, **2025**". | Stored as 2026-12-26 with the printed string and the reasoning in the row flag. |
| R7 | Date typo | The NYE event page prints "Tuesaday" for the Jan 5, 2027 rows. | Stored as 2027-01-05 with the flag. |
| R8 | Unsupported claim | The draft stated a Caesars Palace resort fee from a corporate disclaimer range that no page read in this session supports. | The claim and its source were removed. Caesars Palace fee and tax stay blank. |
| R9 | Wrong URL | The draft pointed the Wynn Signature Series structures at a URL variant that was never fetched. | The fetched URL (`v1753296112`) is restored, and the row records that the file is a "COMING SOON" placeholder. |
| R10 | Rule wording | The draft's generic "no re-entry clause" excerpt was applied to rows where the sheet says something more specific (clause 08 on the flight events, clause 07 on the PokerAtlas rows, clause 06 on NYE Event 29). | Each row now quotes its own clause. |
| R11 | Payout and stack data | The draft carried starting stacks, level lengths, breaks and payout rules only for the two WPT structures that had been read. | All eight WPT structure sections were read, so every WPT row with a published sheet now carries the fee split, stack, level length, break rule and payout note. |
| R12 | Entry status | The draft's separate section did not include the Wynn re-entry rows, so the published ranking mixed verified and unverified rows. | The separate section now holds all 105 rows that are not verified single entry. |
| R13 | Schedule schema | `assets/app.js` read `days[].options`, but the generator emits `days[].events`, so the schedule page rendered nothing. | Fixed in both places, and `scripts/check_links.py` now checks the schedule schema. |
| R14 | Missing data files | `data/daily.json`, `data/rates.json`, `data/venues.json` and `data/walking.json` were created by the earlier draft but were never validated, rendered or linked. | All four are generated, validated, rendered on their own pages and linked from the navigation. |

## 4. Corrections made to earlier drafts

| Earlier claim | What the source says | Action |
|---|---|---|
| "Every structure sheet was verified" | At the start of this session only 16 of 37 November sheets and none of the December sheets had been read. | The claim was replaced with a per-sheet log, and the reading was completed. |
| "Wynn registration opens 4 hours before start" | Not in the official text read. | Removed earlier. The schedules publish a registration close time. |
| "$197.28 per night" hotel example | Used unverified inputs. | Removed earlier. |
| "Venetian walk time 0 min" | No official source. | Blank; each walking record now carries a route link instead. |
| Hotel tax applied to every property | The Venetian terms state 13.38% for the Venetian only. | Tax kept for The Venetian only. |
| Caesars corporate fee range | Not supported by a page read here. | Removed this session. |
| Wynn WPT rows on Dec 18 for PLO 6-Max, HORSE and the $1,100 flights | Those rows are printed under "Dec. 18 Wednesday". | Moved to Dec 16 with the reasoning stored on each row. |

## 5. Verification method

1. Primary sources only (venue or operator domains). Third-party sites were used to find events and
   hotels, never as a value source.
2. Each row is copied from the official schedule or event page. Buy-in, guarantee, chips and level
   count come from those pages.
3. Single-entry status requires the official structure sheet to be read. The sheet must show no
   re-entry, rebuy, add-on or flight language.
4. Every rule field carries the clause text it came from, the source label, the source URL and the
   date the source was read.
5. Missing or conflicting values are left blank and flagged. Nothing is inferred.

## 6. Source log

| Source | URL | Read how | Used for |
|---|---|---|---|
| Venetian DSE IV event page | https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html | Chunks 0-3 of 4 | Dates, times, guarantees, structure links |
| Venetian DSE NYE event page | https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-dec-2026.html | Chunks 0-1 of 2 | Dates, times, guarantees, structure links |
| Venetian DSE IV structure sheets 1-37 | https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_{N}.pdf | Read directly | Entry rules, fee split, levels, stacks, late registration |
| Venetian DSE NYE structure sheets 1-15 | https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_dec_2026-structure_{N}.pdf | Read directly | Entry rules, fee split, levels, stacks, late registration |
| Venetian DSE IV schedule PDF | https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/dse-nov-2026-schedule.pdf | Read | Row order, footnotes |
| Venetian hotel terms | https://www.venetianlasvegas.com/legal/hotel-terms-and-conditions.html | Chunks 0-1 | 13.38% Clark County Room Tax, $55 resort fee, parking, deposit and cancellation |
| Venetian resort fee | https://www.venetianlasvegas.com/resort/resort-fee.html | Read | Fee confirmation |
| Venetian poker suite rates | https://www.venetianlasvegas.com/resort/casino/poker/suite-rates.html | Read | Conditional suite rates, $55 fee |
| Venetian poker page and map | https://www.venetianlasvegas.com/resort/casino/poker.html, https://www.venetianlasvegas.com/content/dam/vlvweb/resort/map.pdf | Read | Poker room location, 50 tables, parking benefit |
| Venetian booking engine | https://www.venetianlasvegas.com/book | Read | Dated quote, Nov 26-29 2026 |
| Wynn WPT schedule PDF | https://cdn.wynnresorts.com/image/upload/v1757097329/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Schedule.pdf | Chunks 0-1 | Every WPT row, chips, levels, footnotes |
| Wynn WPT structures PDF | https://cdn.wynnresorts.com/image/upload/v1750864036/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Structures.pdf | Chunks 0-7 of 8 | Fee splits, stacks, levels, breaks, payouts, action clock, day lists |
| Wynn Signature Series schedule PDF | https://cdn.wynnresorts.com/image/upload/v1753296112/visitwynn_pdfs_files/Poker/Wynn%20Signature%20Series/Wynn_Signature_Series_Schedule.pdf | Read | Every Signature Series row |
| Wynn Signature Series structures PDF | https://cdn.wynnresorts.com/image/upload/v1753296112/visitwynn_pdfs_files/Poker/Wynn%20Signature%20Series/Wynn_Signature_Series_Structures.pdf | Read | Confirmed "COMING SOON" placeholder |
| Wynn daily poster and structures | https://cdn.wynnresorts.com/image/upload/v1752011166/.../poker-daily-tournament-poster.pdf, https://cdn.wynnresorts.com/image/upload/v1752011191/.../Poker-All_Daily_Structures.pdf | Read in full | Daily formats, fee splits, levels, cut-offs |
| Wynn offer terms | https://www.wynnlasvegas.com/terms-and-conditions/848671 | Read | $55 plus tax resort fee, deposit and cancellation terms |
| Wynn facts page | https://www.wynnlasvegas.com/ai-information | Read | Address, resort fee, parking, check-in and check-out |
| Wynn parking | https://www.wynnlasvegas.com/about-us/parking | Read | Parking terms |
| Wynn poker page | https://www.wynnlasvegas.com/casino/poker | Read | Series links, daily suspension note |
| ARIA poker page | https://aria.mgmresorts.com/en/casino/poker.html | Read | 24 tables, player rates by phone or e-mail |
| Bellagio home page | https://bellagio.mgmresorts.com/en.html | Read | Identifies the property; no fee or tax value claimed |
| Caesars Palace page | https://www.caesars.com/caesars-palace | Read | Address only; no fee or tax value claimed |

Third-party sites were used to locate events and hotels only. They are not cited on any row.

## 7. Build and data checks

- `scripts/build_data.py` regenerates every file in `data/` from the verified rows and the structure
  sheets. It also writes `data/row_snapshot.json`, the fingerprint used for changed-row detection.
- `scripts/build_site.py` regenerates `index.html` and every page in `pages/`.
- `scripts/check_links.py` validates the JSON schemas, every local link, every source host, and the
  `data-page` attribute of every generated page.
- `scripts/monitor_sources.py` checks every official URL and reports the rows that changed.
- `scripts/smoke_test.js` renders every generated page in a headless DOM and fails on any page error.
- Current counts (2026-11-17): **317 rows**. Single entry 80 (60 cash, 20 milestone satellites). Separate section
  106 (60 possible multi-entry, 46 re-entry). Unverified 129. Continuation rows 2.
- Row IDs are unique and assigned after the chronological sort (`r001` to `r317`). Restoring a row that sorts into the middle of the WPT block shifts every later ID by one; no row content changed (see `research/verification-2026-11-17.md`).

## 8. Cross-check from the parallel session `40ca34e5`

Session `40ca34e5` worked in parallel on the same file scope. Its branch was integrated here rather than
merged over this one: this session's dataset is larger (316 rows against 225), and it captured a real
nightly rate from the official booking engine, which `40ca34e5` could not — that session's attempt used
the calendar view, which returns `$XXX` placeholders. Nothing from this session was discarded.

What `40ca34e5` contributed, and how it cross-checks this session's work:

| Contribution | Cross-check result |
|---|---|
| `scripts/extract_rules.py` → `data/structure_rules.json`: every official Venetian structure sheet parsed into rule fields with a per-sheet verdict | 52 sheets (37 November + 15 NYE). **Agrees with this session's row-level verdicts**: the sheets that print a starting-flight clause are exactly the ones this session classifies as possible multi-entry; the two Valuetown sheets and the CES-discount sheets are the only ones printing wording about a further entry. |
| `scripts/extract_wpt.py` → `data/wpt_rules.json`: the 69 event blocks of the official WPT structures PDF | Confirms this session's reading that **no WPT block prints a prohibition on re-entry**; every block states a re-entry rule. It also confirms the Signature Series structures file is a placeholder: 166 KB fetched, **27 characters** of extractable text. |
| `scripts/check_source_facts.py` + `data/sources.json` (71 URLs) + `data/snapshots/` + `data/change_log.json` + `data/baseline_hashes.json`, run weekly by `.github/workflows/source-facts.yml` | Runs successfully in GitHub Actions, where the operator domains are reachable: **68 of 71 sources fetched with text, 1 inactive, 2 unreachable** (Bellagio and ARIA time out). This is the reachability evidence that `data/monitoring.json` cannot yet show, because that file still holds a sandbox run in which every domain was unreachable. |
| Meaningful-change detection (`facts_signature`) | On a live re-check it recorded **9 raw page changes and 0 published-value changes**. Operator pages rotate promos and cookie text, so a raw byte hash flags almost every page on every fetch; comparing the money amounts, dates, times and entry-rule words printed on the page avoids that false alarm. |
| `research/verification-2026-11-16.md` | One row per Venetian structure sheet with its verdict and link, the distinct WPT re-entry wordings with a count of the rows quoting each, and the Wynn daily-tournament facts. |

Irregularity found in this repository during that integration: `.github/workflows/monitor.yml` used a
`name:` key inside its `schedule:` entry. The workflow schema accepts only `cron` there, so **the daily
source check had never fired**. The key was removed; the daily job will now run on its schedule.
