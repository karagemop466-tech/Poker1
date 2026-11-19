# Live official-source re-verification — 2026-11-19 — session af414e67

Session `af414e67`, branch `arena/af414e67-poker1`. All fetches below were made on **2026-11-19
(UTC)** with the agent page-fetch tool, which reaches operator domains from this sandbox (bash
`curl` still cannot: `exit 35`, as recorded in F55). Every comparison is between the **live text
read today** and the **archived snapshot** under `data/snapshots/` (or, where no snapshot exists,
against the published dataset). No published value was changed by this pass; three new findings are
published as **F82–F84** on the Flagged for Review page.

## Method

For the two Venetian schedule pages, every table row (date, start time, event #, event name) was
transcribed from the live fetch into a file and diffed mechanically against the rows parsed from
the archived snapshot (normalisation: whitespace collapse, `<br>` split, leading bullet strip).
Zero-diff means row-for-row identity on all four fields. For PDFs and policy pages the comparison
is fact-by-fact (money, times, dates, rule sentences) against the snapshot text.

## 1. Venetian DeepStack Extravaganza IV schedule — 94/94 rows match, zero drift

- Live: https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html (4 chunks, read in full)
- Snapshot: `data/snapshots/v_dse_nov_page.txt` (archived 2026-11-16/17)
- Result: **94 live rows = 94 snapshot rows, 0 diffs** on (date, start, event #, name), including
  the printed typos that the dataset deliberately preserves (`No LImit`, event names, structure
  links pattern). Series header still prints "November 16 – December 23, 2026" and
  "More than $3.6 Million in guaranteed tournament prize pools".

## 2. Venetian DeepStack Extravaganza NYE schedule — 49/49 rows match, zero drift

- Live: https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-dec-2026.html (2 chunks, read in full)
- Snapshot: `data/snapshots/v_dse_dec_page.txt`
- Result: **49 live rows = 49 snapshot rows, 0 diffs**. The two known printed anomalies are still
  printed live and unchanged: **"Saturday, December 26, 2025"** (F1) and **"Tuesaday, January 5,
  2027"**. Header still "December 24, 2026 – January 10, 2027", "More than $1.1 Million".

## 3. Venetian hotel terms and resort fee — every published cost fact re-confirmed live

- Live: https://www.venetianlasvegas.com/legal/hotel-terms-and-conditions.html (2 chunks) and
  https://www.venetianlasvegas.com/resort/resort-fee.html
- Snapshot: `data/snapshots/v_hotel_terms.txt`
- Result, each quoted from today's live text:
  - "Daily rates do not include the applicable Clark County Room Tax of **13.38%**." ✓
  - "standard Las Vegas Resort Fee of **$55 plus applicable tax per night**" ✓ (resort-fee page:
    "daily Resort Fee of $55 plus tax per night")
  - incidental deposit "**$150 per night**" ✓; additional guest "**$50**" per day ✓;
    early check-out "**$100 plus tax**" ✓; registered-guest self-parking "**$20/day**",
    non-guest $20 M–Th / $25 F–S, valet "**$40/day**" ✓
  - check-in 3:00 p.m., check-out 11:00 a.m.; prepaid offers non-cancellable ✓
- No drift on any hotel-cost figure the calculator depends on.

## 4. Venetian structure sheet #05 (spot check) — matches; entry-rule silence re-confirmed

- Live: https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_5.pdf
- Snapshot: `data/snapshots/v_nov_struct_05.txt`
- Result: Start 11:10 AM, Starting Chips 40,000, Level Duration 30 minutes, Late Registration
  "10 levels + Break (~ 4:55 PM)", Guarantee $10,000, "$58 of the $300 Buy-In … house fees",
  "$242 of every $300", "pays 12.5% of the field" — all identical. (Snapshot line 13 prints
  "2.500-5,000" where the live text prints "2,500-5,000" — an archived-extraction artifact, not a
  live change.)
- **Rules 1–10 contain no re-entry, no add-on, no "single entry" and no "freezeout" sentence**,
  read live today. This re-confirms, from the official sheet itself, why the row stays a
  sheet-silence candidate (CAND) under the strict written-evidence policy.

## 5. Offline sweep of every archived structure sheet for affirmative freezeout language

- `grep` over all 93 files in `data/snapshots/` for
  `freeze-out / no re-entry / no rebuy / no add-on / single entry / one entry only / entries are not permitted`:
  the only hits are the **Wynn parking page** ("no re-entry" for valet re-entry privileges) and
  `w_daily_struct.txt` — **no Venetian structure sheet in the archive contains an affirmative
  single-entry sentence**. Sheets that mention entry terms at all: only the December sheets that
  print re-entry/add-on clauses (they stay out of the candidate pool accordingly).
- Verdict: the strict-policy blocker (SE = 0 rows) still rests on correctly-read evidence; nothing
  in the archive would allow promoting a row today.

## 6. Wynn Signature Series structures PDF — still "COMING SOON" (re-confirmed live)

- Live: https://cdn.wynnresorts.com/image/upload/v1762299460/visitwynn_pdfs_files/Poker/Wynn%20Signature%20Series/Wynn_Signature_Series_Structures.pdf
- Result: the PDF parses to exactly **"LAS VEGAS / POKER / COMING SOON"** (title: "Poker Tournament -
  Details Coming Soon"). F22/F76 remain open: the 38 Signature Series rows stay unverified on the
  entry rule. Checked twice on 2026-11-19.

## 7. Wynn Signature Series schedule PDF — **the four multi-day guarantees print live** (F82)

- Live (fetched twice, identical): https://cdn.wynnresorts.com/image/upload/v1753296112/visitwynn_pdfs_files/Poker/Wynn%20Signature%20Series/Wynn_Signature_Series_Schedule.pdf
- Snapshot: `data/snapshots/wss_sched.txt` — `grep` finds **none** of 150,000 / 250,000 / 100,000 /
  300,000; the multi-day rows in the snapshot carry only the entry (e.g.
  "1/11 MON 12 P.M. NO LIMIT HOLD'EM DAY 1A $400 40,000 30/40").
- Live table (header `DATE DAY TIME EVENT GUARANTEE ENTRY CHIPS LEVELS`) prints:
  - 1/11–1/13 Day 1A–1F (6 rows): **GUARANTEE $150,000**, ENTRY $400
  - 1/14–1/16 Day 1A–1D (4 rows): **GUARANTEE $250,000**, ENTRY $600
  - 1/18–1/20 Day 1A–1C (3 rows): **GUARANTEE $100,000**, ENTRY $400
    (the 1/18 row renders with one stray empty cell in the extraction; the clean 1/19 and 1/20 rows
    confirm the column reading)
  - 1/21–1/23 Day 1A–1D (5 rows): **GUARANTEE $300,000**, ENTRY $800
  - Already-published values unchanged: NLH Turbo $10,000, Sunday NLH $30,000, Seniors $30,000.
- This is exactly the set of values **F54 blanked** as "appear on no official source". As of
  today's live read they **do** appear on the official source. Whether the PDF was updated after
  the 2026-11-16/17 snapshot or the snapshot extraction dropped those cells cannot be determined
  from this sandbox (same URL, version-pinned). Recorded as **F82**: restore-candidate for the
  integration phase, each value carrying retrieved-on 2026-11-19 and this page as its source;
  until then the published blanks and flags stand.

## 8. WPT World Championship schedule PDF — extraction discrepancy (F84)

- Live: https://cdn.wynnresorts.com/image/upload/v1757097329/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Schedule.pdf (both chunks)
- Snapshot: `data/snapshots/wpt_sched.txt`
- Matches: dates Nov. 27 – Dec. 21, all buy-ins and guarantees read on the first two pages
  ($600/$400K, $800/$1M, $1,600/$1M, $1,100/$5M Prime, $400/$3M Super Gold Million,
  $10,400/$1,000,000 Added, satellites, turbos $600/$50K) — identical to snapshot lines.
- **Differs:** the live extraction prints `Ladies NIH Championship (2 Day)`,
  `Mixed Triple Draw (A-5, 2-7, BadugI)` and `World Championship 1A/8` where the snapshot prints
  `Ladies NLH Championship`, `Badugi`, `1A/B`. The published rows use the snapshot reading (NLH).
  An earlier session fetch produced the same NIH/1A/8 strings and they were judged transcription
  artifacts then (df94b75e); the snapshot contains zero `NIH`. Two independent fetches today both
  return NIH/BadugI/1A/8, so this is either a PDF text change under the same version-pinned URL or
  a difference between PDF extractors. Recorded as **F84** — no published value changes; resolving
  it needs a second extraction method (a different PDF parser in CI).

## 9. Bellagio Friday flyer, Caesars Palace daily flyer — match live

- Bellagio Friday $600 NLH (live, official contentstack asset linked from the Bellagio poker page):
  Fridays 11:00 a.m.; 30,000 starting chips (15,000 + 15,000); 30-minute levels;
  re-entry through end of level 8; $510 prize pool / $50 house fee / $40 voluntary staff gratuity;
  the $40 gratuity grants 15,000 extra chips — identical to `data/snapshots/b_fri_pdf.txt`.
  (Note: a URL I first built from a truncated manifest listing 404'd; the manifest URL with the
  `$600` filename is correct — my error, not the repo's.)
- Caesars Palace daily flyer (live): 10 AM $100 / 2 PM $160 / 6 PM $100 / 9 PM $160, $50 optional
  add-on, 20,000 chips, 20-minute levels, $1,000 guarantees, registration closes start of level 7,
  re-entry within first break, fee splits $70/$30, $115/$45, $45/$5 — identical to
  `data/snapshots/c_daily_flyer.txt` (printed "Version 6.19.2026" on both).

## 10. Wynn poker page and Venetian series page — match live

- https://www.wynnlasvegas.com/casino/poker: WPT World Championship "November 27–December 21",
  Super Gold Million "$400 buy-in featuring a $3,000,000 guarantee", Signature Series
  "January 11–24. 2027", daily formats ($200,000 weekly, $40,000 NLH Rebuy Friday, $10,000 every
  evening at 6 p.m.), suspension note, Encore room location — identical to `w_poker_page.txt`.
  The Signature Structures link still points at the v1762299460 placeholder (item 6).
- https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament.html:
  DSE IV headline guarantees match the schedule rows; NYE headline guarantees match. The page also
  lists the **DeepStack Showdown (January)** series (item 11).

## 11. Venetian DeepStack Showdown (January) 2027 — official, published, **absent from the repo** (F83)

- Live: https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dss-jan-2027.html
  — a full official schedule table, January 11 – February 14, 2027, "More than $2.2 Million in
  guaranteed tournament prize pools", with per-row structure-sheet links
  (`dse_jan`/`dss_jan_2027-structure_N.pdf`). Chunk 0 alone shows events 1–15 covering
  Jan 11–20 (daily $300/$12K and $200/$8K events, the $250/$100K multi-flight Jan 15–18, seniors,
  bounties).
- `grep -ri showdown` across `FLAGGED.md`, `QUESTIONS.md`, `SUGGESTIONS.md`,
  `EXECUTIVE_SUMMARY.md`, `REVIEW.md`, `README.md`, `data/*.json`, `scripts/build_data.py`:
  **zero hits**. `data/tournaments.json` has 0 DeepStack Showdown rows; January rows in the
  dataset are Venetian NYE (Jan 1–10) and Wynn Signature (Jan 11–24) only.
- The same announcement was already in the archived series-page snapshot, so this is not a page
  published today — it is a **coverage gap**: an entire officially-scheduled Venetian series that
  overlaps the dataset's own window (Jan 11–24) and extends to Feb 14, 2027, with no rows, no
  flag and no question recorded anywhere in the repository. Recorded as **F83** (integration-phase
  candidate: add sourced rows from this page; until then the gap is published, not hidden).

## 12. Live hotel rate capture — attempted, not possible from here (no change)

- Live: https://www.venetianlasvegas.com/booking?adults[]=2&arrival_date=2026-12-13&children[]=0&departure_date=2026-12-20&view=calendar
- Result: the engine returns the client-side loading shell ("Your Venice meets Vegas getaway is
  loading") with **no rate figures** in the static HTML — the same blocker recorded for P2/S22b.
  **No quote was captured and nothing was inferred.** The five dated quotes in `data/rates.json`
  are untouched; the like-for-like comparison continues to rest on them.

## Summary

| # | Source (official) | Live read 2026-11-19 | Result |
|---|---|---|---|
| 1 | Venetian DSE IV schedule page | 94 rows | 0 diffs vs snapshot |
| 2 | Venetian DSE NYE schedule page | 49 rows | 0 diffs vs snapshot |
| 3 | Venetian hotel terms + resort fee page | tax/fee/parking sentences | all published figures re-confirmed |
| 4 | Venetian structure sheet #05 | full sheet | matches; no entry-rule sentence |
| 5 | all 93 archived snapshots (offline) | freezeout-language sweep | no affirmative single-entry text exists |
| 6 | Wynn Signature Structures PDF | full PDF | still "COMING SOON" |
| 7 | Wynn Signature Schedule PDF (×2) | full PDF | **four multi-day guarantees print live → F82** |
| 8 | WPT World Championship Schedule PDF | 2 chunks | money/dates match; NIH/BadugI/1A-8 extraction diff → F84 |
| 9 | Bellagio Friday flyer, Caesars daily flyer | full PDFs | match |
| 10 | Wynn poker page, Venetian series page | full pages | match |
| 11 | Venetian DSS January page | chunk 0 of 4 | **official series missing from repo → F83** |
| 12 | Venetian booking engine | dated URL | no figures rendered; no quote taken |

No published value was changed, no `last_checked` date was advanced by this record alone (row-level
advancement happens only in the integration phase, for rows whose source this pass actually re-read
and whose values are regenerated with it), and every finding above carries its official link.

## Post-merge addendum (same session, after syncing `origin/main` at `8c71387`)

- **Item 7 (WSS guarantees) is resolved on `main` by an independent session.** Session `f3a84f9b`
  found the same fact from the same live PDF and published it as **F83** (their id), and PR #112
  restored the 17 multi-day flight guarantees in `data/tournaments.json`
  (150,000 x6, 250,000 x4, 100,000 x3, 300,000 x4; `verify_rows.py` and `build_data.py` cite F83).
  This session's duplicate F82 row was therefore dropped during the merge and the finding above
  stands as an independent cross-confirmation: two sessions, one live PDF, same four values.
- **Numbering after the merge:** the DSS-coverage gap is now **F85** and the WPT extraction
  discrepancy is now **F86** in `FLAGGED.md` (main had already taken F83/F84 for other findings).
