# Verification — 2026-11-19 (session cebd4457)

Branch `arena/cebd4457-poker1`. Scope (claimed in `COORDINATION.md`, commit `f10d4b2`): the
2026-11-19 live re-reads, the monitor "source changed" re-check, the P3 flag, the disposition of
stale PR #113, and the final integration.

## 1. Live re-verification of every official source (2026-11-19)

All reads were live reads of the official URLs in `scripts/build_data.py SRC` on 2026-11-19.

| Source | Result |
|---|---|
| Venetian DSE IV listing page (`dse-nov-2026.html`, 4 chunks) | 94/94 stored rows match every printed value. Five name diffs are wording-only re-renders ("1 Day $400 Bounty NLH Event #18" vs stored "Event 18 - $400 NLH 1 Day Bounty", etc.); stored names kept (dated capture of the sheet wording). |
| Venetian DSE NYE listing page (`dse-dec-2026.html`, 2 chunks) | 49/49 stored rows match. Official typos unchanged: "Saturday, December 26, 2025" (DATE_TYPO_DEC26), "Tuesaday, January 5, 2027" (DATE_TYPO_TUESDAY), MSPT Day 2 11:10 listing vs 11:00 sheet #8 (MSPT_DAY2_START_CONFLICT). Nothing new. |
| WPT World Championship schedule PDF | 136/136 rows match every published value (incl. the "25 Prizes"/"50 Seats" columns). The known Dec 3/Dec 5 Day 2 column misprints and "Dec. 18 Wednesday" are unchanged. Footnotes unchanged (Ladies $11,100→$1,100 discount, ClubWPT Gold +$1M, "**" = direct entry). |
| WPT World Championship structures PDF (all 8 sections) | 8/8 blocks match verbatim: fee splits, registration clauses (Prime "One entry plus one re-entry per flight to Level 10", WC "Four (4) Entries maximum"), starting stacks, level counts, action clock, mystery bounty terms. |
| Venetian structure sheets #1, #5, #10, #29 | Re-read in full; every published value of the 18 rows they source matches. |
| Venetian structure sheet #30 (`dse_nov_2026-structure_30.pdf`) | Re-read in full as the r012 source-change re-check: identical to `data/snapshots/v_nov_struct_30.txt` on every published value (Event 08 PKO, $200/$40/$160, 5:10 PM, 25,000, late reg 8 levels + break ~9:40 PM, $8,000 gtd incl. bounties, clause 06 $40/$200→$160 = 12.5%, $50 bounty). |
| Venetian Resort Fee page | "$55 plus tax per night" + the five inclusions unchanged. |
| Venetian Hotel Terms & Conditions | All figures unchanged: $150 deposit, $50 additional guest, $100+tax early checkout, $55+tax resort fee, 13.38% tax, $20 self / $25 valet / $40 peaks parking, prepaid non-refundable. |
| Wynn parking page | $25 self (first 3 hours complimentary) / $40 valet, comps for Resort/Tower Suite guests, "Complimentary self-parking is extended to Wynn Poker Room guests (please visit the Poker Room for details)" unchanged. |
| Caesars poker-tournaments article | rooms03/formats05 excerpts unchanged verbatim (Horseshoe six daily NLH 9/11/2/5/8/11 a.m., "mixture of buy-ins"; Caesars Palace four daily 10/2/6/9 p.m., $100 buy-in / 20,000 / $1,000 gtd / 20-min blinds / $50 add-on +15,000). The article's "$100" vs the flyer's "$160" (Q-D4/F78) is unchanged. |
| Caesars corporate disclaimer | **Changed.** The Hotel Disclaimer now prints "Room reservations are subject to a daily resort fee between **$45-$60** plus applicable tax" where the 2026-11-17 read recorded "**$45-$50**". See §2. |

## 2. The four monitor "source changed - re-check" marks

`data/changes.json` (key `changed`, checked_at 2026-11-19) carries four rows marked
"source changed - re-check". Each was re-checked live today:

| Row | Source | Disposition |
|---|---|---|
| `r012` | `venetian-sheet-30` (Nov 23 PKO $200/$8K) | **False alarm.** Sheet #30 re-read live: identical to the archived snapshot on every published value. The change log records byte-level re-renders at 05:39Z with an empty facts diff — cosmetic. Row values confirmed; and the sheet is now fully re-read, so the row is stamped 2026-11-19. |
| `rooms03` | `rooms03` (Horseshoe strip-room entry) | **False alarm.** The Caesars article was re-read: the stored excerpt is verbatim identical. Cosmetic re-render only. |
| `formats05` | `formats05` (Caesars/Horseshoe daily-format entry) | **False alarm.** Same page, same excerpt, verbatim identical. |
| `caesars` | `h_caesars` (Caesars corporate disclaimer) | **Real change — confirmed and recorded.** The Hotel Disclaimer's portfolio resort-fee range moved from "$45-$50" (read 2026-11-17) to "$45-$60" (read 2026-11-19). Both readings are now quoted with their dates in the hotel row's `resort_fee_note`, the source label, FLAGGED U3 and this file. The Caesars Palace resort fee itself stays blank: the range is portfolio-wide and names no property, so it is never used as this property's fee. |

Mechanics recorded for future readers: marks are CI output (`monitor_sources.py --write-report`
comparing fact signatures against `data/source_baseline.json`); they must never be hand-edited, and
a baseline is only re-accepted through `monitor_sources.py --accept-baseline` after a real fetched
run — never offline. The 2026-11-17 research file keeps its then-readings; a changed quote is
recorded as a new dated reading, never as a silent edit.

## 3. Stamping rule applied (strict)

`last_checked = 2026-11-19` only where **every** source cited by the row was re-read in full that
day. `verified_on` and every rule-clause `retrieved_on` keep 2026-11-17 (they date the original
clause capture; the clauses were re-confirmed but not re-captured).

| Set | Rows | Stamped |
|---|---|---|
| Wynn Signature Series (schedule + structures PDFs re-read) | 38 | 2026-11-19 |
| WPT World Championship (schedule + structures PDFs re-read) | 136 | 2026-11-19 |
| Venetian Nov rows on sheets #1/#5/#10/#29 (listing + own sheet re-read) | 18 | 2026-11-19 |
| `r012` (sheet #30 re-read in full today) | 1 | 2026-11-19 |
| All other Venetian rows (listing re-read 94/94 + 49/49; sheets fact-hash checked by the monitor, not fully re-read) | 124 | stays 2026-11-17, each with a dated `recheck` record on the row |

Totals: 193 rows at 2026-11-19, 124 at 2026-11-17. The rebuild changed date stamps, added the
per-row `recheck` records and the P3 field — no published value changed (verified by field-diff
against the previous `data/tournaments.json`).

## 4. Hotel re-checks (P9, `data/hotels.json` `recheck`)

venetian / palazzo: resort-fee + hotel-terms pages re-read 2026-11-19, all figures unchanged.
wynn / encore: parking page re-read 2026-11-19, all figures and the poker-room parking comp
unchanged. caesars: the disclaimer re-read 2026-11-19 with the range change recorded (above);
the parking-page claims of 2026-11-17 were **not** re-read and say so. bellagio / aria keep their
2026-11-17 recheck records (not re-read today). Hotel `last_checked` stays 2026-11-17 (rates are
not re-quoted; rate dates move and only the booking engine can re-quote).

## 5. P3 built: "effectively single entry" descriptive flag

43 MULTI rows / 12 multi-flight events carry `flight_pricing` (clause-08 excerpt, uniform flight
price, explicit silence note, source + retrieval date) plus an "effectively single entry" label
chip. Never a reclassification: rows keep `entry_status` MULTI, stay out of the single-entry
shortlist and the ranking, and `check_links.py` asserts flagged rows are MULTI and keep the
multi-flight label. Excluded by construction: the three PokerAtlas Valuetown bounty rows (sheets
explicitly price later buy-ins: "All subsequent buy in's after the initial buy in will be $200")
and the seven WPT MULTI rows (sheets print entry caps). See SUGGESTIONS.md P3.

## 6. Gates (all green at integration)

- `build_data.py` → 317 rows (80 CAND / 53 MULTI / 107 RE / 43 CONT / 34 UNV), 70 schedule days.
- `check_links.py` OK — incl. the new flight_pricing/recheck validators.
- `verify_rows.py` — 335 rows, 1386 checks, 0 hard failures, 1 review item (r225).
- `verify_against_snapshots.py` OK — 0 unexplained mismatches (r263 MSPT conflict recorded on the row).
- `check_schedule.py` OK (170 overlap pairs, every fallback enterable).
- `build_site.py` 31 pages; `npm test` 5/5 (rendered links 1662 refs, 0 broken; calculator; source badges);
  9 × `test_*.py` OK.

r225 re-confirmed on the live PDFs: the Dec 21 NLH Turbo prints 8 p.m. on the schedule PDF and
6 p.m. on the structures PDF (published conflict, unchanged, recorded on the row).
