# Verification log — integration session 212b84be (2026-11-17)

Scope: merge the open session branches (PR #36 c0714e1a, PR #38 160f9080), re-verify the combined
dataset line by line, resolve the open PR #24, and publish.

## 1. Line-by-line verification of every published value

`python3 scripts/verify_rows.py` checks every published money / date / time / entry-rule value in
`data/tournaments.json`, `data/hotels.json` and `data/rates.json` against the raw official document text
archived under `data/snapshots/` (which the scheduled source-facts job refreshed on 2026-11-17).

| Check | Result |
|---|---|
| Verified rows | 324 |
| Field checks | 1,296 |
| Hard failures | **0** |
| Review items | 1 (F4: the Dec 21 NLH Turbo start time, schedule 8 p.m. vs sheet 6 p.m. — already flagged) |
| Rate arithmetic | 5 / 5 dated quotes reproduce exactly at 13.38% of room + resort fee |

Integration fix required to reach 0 failures: a WPT sheet prints the fee split ("... = $510 (Tournament
Prize Pool) + $65 (Tournament Fee) + $25 (Poker Staff Service Charge)") but never the house-fee sum. The
verifier now accepts a sum only when it equals the two printed components and both components appear in
the official text. Base rule from session 160f9080; component acceptance added here.

## 2. Ambiguous structure-sheet keys found and fixed (flag F60)

Two WPT sheets print the same date/start/buy-in key:

| Key | Candidate sheets | Correct fee (per printed title) |
|---|---|---|
| Dec 7, 11:00, $1,100 | block 14 "$1,100 HORSE" ($90 + $45) / block 11 "$1,100 WPT Prime Championship" ($90 + $40) | HORSE 135 / Prime Day 1C 130 |
| Dec 14, 12:00, $1,100 | block 62 "$1,100 Milestone Satellite to $10,400" ($85 + $40) / block 27 "$1,100 Mixed Triple Draw" ($90 + $45) | Satellite 125 / Mixed Triple Draw 135 |

`_sheet_for` in `scripts/build_data.py` returned the first candidate and mis-priced the Prime
Championship Day 1C (r081) and the Mixed Triple Draw (r148). Both are now priced from the sheet whose
printed title matches the row name — the same rule `scripts/extract_wpt_sheets.py` uses. Post-fix
classification: SE 80 / MULTI 67 / RE 107 / CONT 25 / UNV 38; every count published in
`EXECUTIVE_SUMMARY.md`, `REVIEW.md` and `research/*.md` was re-synced.

## 3. Entry-rule policy audit (the "written maximum-entry" requirement)

- All 80 single-entry rows are Venetian. Each row's `rules.single_entry` carries the exact basis:
  "No re-entry, rebuy, add-on or multi-flight clause appears anywhere on this structure sheet (every
  numbered clause was read)." A spot re-read of sheet 5 (`data/snapshots/v_nov_struct_05.txt`) confirms
  the ten numbered clauses contain no entry-count language.
- No official source in the archive prints an affirmative "single entry" / "freezeout" / "one entry"
  sentence (searched all snapshots). The label is therefore published as single entry **by absence of
  contrary terms**, with the basis on every row and a callout on the single-entry page.
- The multi-flight implication clause ("Any player who bags chips for Day 2 may not play a subsequent
  flight") keeps its 60 rows in the separate section with the reasoning printed: a busted player can
  still enter a later flight. The 7 Wynn limited-entry flights (Prime "One (1) Entry and One (1)
  re-entry"; World Championship "Four (4) Entries maximum") are also in the separate section.

## 4. Live official pages re-read today (page fetcher)

| URL | What it confirmed |
|---|---|
| Venetian DSE IV schedule page | Rows match the dataset (checked the first 17 rows and sheet links against `data/tournaments.json`); no drift. |
| Caesars Palace FAQ (Policies & Guidelines) | "Check-in at Caesars Palace begins at 4:00 PM, and check-out is at 11:00 AM." + 48-hour cancellation rule. Filled the blank `check_in_out` and completed the cancellation note. |
| Wynn booking engine (details.aspx, Nov 18–20 requested) | F37 re-confirmed: engine renders "1 Night Stay: Nov. 16 - Nov. 17"; offer averages $1,254 and $1,074 per night include the resort fee and **exclude taxes**; no tax line or checkout total exposed. Not logged as quotes. Also: "Self-parking is complimentary to registered guests" — Wynn/Encore `parking_usd_per_day` corrected to 0 for a hotel stay (the $25 non-guest rate stays in the note). |

## 5. Validation after the merge

- `build_data.py` → 317 rows, 78 flagged, 7 hotels, 5 dated rates, 70 days.
- `build_site.py` → 21 pages. `check_links.py` → OK.
- `npm run test:smoke` → 21/21 pages render headlessly.
- PR #24 closed as superseded (clause-8 policy already applied on main; stale 225-row universe);
  disposition in `FLAGGED.md` F39 and `QUESTIONS.md` Q-D5.
