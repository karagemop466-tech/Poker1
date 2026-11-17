# Line-by-line verification record — session `c7a324a6`, 2026-11-17

Two independent passes were run against the official documents, then one expansion of coverage.
Nothing in this file is inferred: each statement below names the document it came from.

## 1. Printed-schedule audit, Venetian (both series, all printed rows)

Method: the official page text archived by the monitoring job (`data/snapshots/v_dse_nov_page.txt`
and `v_dse_dec_page.txt`, both fetched by GitHub Actions from the operator's own domain at
2026-11-17T00:41Z) was parsed into printed rows — `weekday, date / time / event number / event name` —
and each printed row was matched to a stored row on (date, start time, event number). For every
matched pair the check compared **all $ amounts printed on the line**, the guarantee token, the
flight/structure tokens (`1A`…`1H`, `(1Day)`, `(2Day)`) and the format words (bounty, PKO, milestone,
seniors, ladies, turbo, streamed).

| Series | Printed rows parsed | Stored rows | Matched | Result |
|---|---|---|---|---|
| DeepStack Extravaganza IV (Nov 16 – Dec 23, 2026) | 94 | 94 | 94 | exact on date, time, event number and every printed amount |
| DeepStack Extravaganza NYE (Dec 24, 2026 – Jan 10, 2027) | 49 | 49 | 48 | one start time contradicted the page (below) |

**Corrections and confirmations:**

* **One published value was wrong and is fixed.** The NYE row for the **$1,600 No Limit Hold'em MSPT
  Day 2 Restart, Monday, January 4, 2027** was stored with a start of `11:00`. The official page prints
  `11:10 AM` (re-read on 2026-11-17 at
  <https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-dec-2026.html>).
  The row is republished at **11:10** and flagged (F106). The row is a continuation row, so the correction
  changes no buy-in, guarantee or entry rule — it changes when a player must be seated.
  Session `d94b191b` reached the same correction independently on the same day; the two records agree, and
  its note that the structure sheet prints "Day 2 will resume at 11:00 AM" is the reason both readings are kept.
* The three NYE rows on Dec 26 are printed by the operator as **"Saturday, December 26, 2025"**; the
  dataset stores 2026-12-26 (already flagged as F1). Confirmed again on the live page on 2026-11-17.
* The page still prints **"Tuesaday, January 5, 2027"**. No effect on the data.
* The promotional second line the page prints under some events was checked line by line instead of trusted:
  "Show Your CES Badge - $10 RAKE DISCOUNT" appears under **three** rows only - Jan 6 event 29 (Bounty),
  Jan 7 5:10 p.m. event 30 flight 1B and Jan 8 5:10 p.m. event 30 flight 1D. It is **not** printed under
  event 30 flights 1A, 1C or 1F. The dataset carried it on **Jan 9 5:10 p.m. flight 1F** as well, so that row
  is republished without the clause (F113); its amounts were already correct and are unchanged. The three rows
  that do print it keep it, because the words sit on the same printed row as their buy-in.
* The stored name `… $1 Mill GTD …` was re-checked against the guarantee arithmetic: the printed token is
  `$1 Mill GTD` = $1,000,000, which is what the row stores.

## 2. Value-provenance audit, all four Venetian/Wynn series

Method: every **money value** published in a tournament row (`buy_in_usd`, `guarantee_usd`,
`house_fee_usd`, `prize_pool_usd`) and every starting stack was required to appear in the official
documents of that row's own venue — the two Venetian pages plus all 37 November and 15 December/NYE
structure sheets, the WPT schedule and structures PDFs, the Signature Series schedule and structures
PDFs — as a dollar token (`$300`, `$110,000`, `$75K`, `$1 Mill`) or, for stacks, as the exact number.

Result over **317 rows**: every buy-in, house fee, prize pool and starting stack is printed by an
official document of that venue. **The only unsourced money values in the dataset were 17 Wynn Signature
Series guarantees** ($150K / $250K / $100K / $300K on the multi-day main events), which no official
source prints — the Signature Series structures PDF is still a `COMING SOON` placeholder at both
published URLs. Session `160f9080` found the same 17 rows independently and blanked them (published as
F54); this pass is a second, separately written check that reached the same list, row for row.

Arithmetic re-checked rather than trusted: `house fee + prize pool = buy-in` on every row that publishes a
split, and `guarantee ÷ buy-in = published ratio` on every row that publishes one. One class of difference
was investigated and is not an error: three Venetian RaceDay rows (r007–r009) publish an estimated end
computed with the two-tier level length printed on their sheet (30/40 minutes), which the naive
single-length formula in this audit does not reproduce.

## 3. Coverage added: the other Strip rooms' own schedule documents

The morning feed previously held only Wynn's daily formats; the other rooms were described from editorial
pages. That has changed, because the rooms publish their own documents:

| Room | Official document read 2026-11-17 | What it lets the site say |
|---|---|---|
| Caesars Palace | [Daily No-Limit Hold'em tournament schedule (2026)](https://www.caesars.com/content/dam/empire/clv/casino/poker/tournament-schedule/clv-poker-daily-nlh-tournament-flyer-2026.pdf), reached from the [official casino page](https://www.caesars.com/caesars-palace/casino/poker) ("View Schedule") | Four starts a day (10 a.m. $100, 2 p.m. $160, 6 p.m. $100, 9 p.m. $160), each `$1,000` guaranteed, 20,000 chips, 20-minute levels, optional `$50` add-on at the first break, registration closes at the start of level seven, sign-ups open one hour before the start, fee splits ($70/$30 and $115/$45, add-on $45/$5), six-player minimum with refund, payout ladder printed. Every one of the four allows re-entry on elimination within the first break, so none is single entry. |
| Bellagio | The three weekly structure PDFs linked from the [official Bellagio poker page](https://bellagio.mgmresorts.com/en/casino/poker.html): [Friday $600 NLH](https://assets.contentstack.io/v3/assets/bltc6ce635bc4868eb2/blt9cf95b0e60ec253e/6af491a3a9851d75c40be840/mgm-bellagio-poker-fridays-$600-nlh.pdf), [Saturday NLH](https://assets.contentstack.io/v3/assets/bltc6ce635bc4868eb2/blt6d47974bf5a7d9b6/6af491a391a6e8e4230c9e07/mgm-bellagio-poker-saturdays-$1000-nlh.pdf), [Sunday $400 H.O.R.S.E.](https://assets.contentstack.io/v3/assets/bltc6ce635bc4868eb2/blt07fcf1244a6da661/6af491a339e2b4f6b76a86ad/mgm-bellagio-poker-sundays-$400-horse.pdf) | Friday: 11:00 a.m., $600 = $510 pool + $50 house + $40 voluntary gratuity, 30,000 chips, 30-minute levels, 12-minute break every four levels, re-entry through the end of level 8. Sunday: 11:00 a.m., $400 = $340 + $35 + $25, same chip figure, re-entry through level 8, payout about 12.5% of the field, 26-level ladder. Saturday: four flights with a combined Day 2, "at least $50,000" combined prize pool, registration open until the start of level 10 — and **three different buy-ins printed** ($1,100 heading, $1,000 page label, "$600 Buy-in" in its own rule 07), so its entry fee is left blank. |
| ARIA | [Official ARIA poker page](https://aria.mgmresorts.com/en/casino/poker.html) | A verified negative, published: 24 tables, the room's location, a phone number (702.590.7232) and `PokerRoomRates@aria.com`, and the instruction "Be sure to call the Poker Room or check out our Twitter account, @ARIAPoker, for the most recent information on whether our Daily Tournaments are running as scheduled!" **No schedule, buy-in, structure, resort fee or tax is published on the page**, so ARIA contributes no rows. The page is now in the monitored manifest, so the first day ARIA publishes a schedule the monitor notices it. |

All seven of those URLs were added to `data/sources.json`, so the daily job fetches and snapshots them and
the row-level monitor flags any printed value that moves. Two hosts were allow-listed for this, each with
the reason written in the code: `assets.contentstack.io` (MGM's own asset host, serving the PDFs that the
official Bellagio page links) and `www.clarkcountynv.gov` (a county record, labelled as such everywhere it
is used).

## 4. Tax and fee verification against the authority that sets them

Until now a room-tax percentage was published only where the property's own page printed it, which left
Wynn, Encore, Bellagio, ARIA and Caesars Palace blank (F46, F47). The rate is set by the county, so the
county's own licensing record was read:

> Clark County Department of Business License, *General Information Guide for Transient Lodging
> Establishments*, licensed-establishment table:
> `1000389.RES-001 | Venetian Resort Hotel Casino / Palazzo Resort Hotel Casino | 3325 Las Vegas Blvd S |
> Las Vegas | NV | Licensed | 13.38% | RES | 1 | Transient Lodging Tax - Resort Hotel (PGC)`
> `2000078.RES-001 | Wynn Las Vegas / Encore at Wynn Las Vegas | 3131 Las Vegas Blvd S | Las Vegas | NV |
> Licensed | 13.38% | RES | 1 | Transient Lodging Tax - Resort Hotel (PGC)`
> (read 2026-11-17, <https://www.clarkcountynv.gov/adobe/assets/urn:aaid:aem:689ef54f-ec0d-4bb6-b8ea-05a82887561f/original/as/genl-info-guide-for-tles-july-2021.pdf>)

What changed, and what did not:

* **Wynn and Encore: room tax 13.38%, `verified`.** The percentage now comes from the taxing authority,
  labelled as a county record. Wynn's own pages still print no percentage and its booking engine still
  renders its rate grid and tax line client-side, so **the nightly amount stays blank** — the rate is
  verified, the price is not. F46 is therefore narrowed, not closed: it is no longer "unknown", it is
  "known from the county, still unpriced".
* **Venetian and Palazzo: street address `3325 Las Vegas Blvd S, Las Vegas, NV`, `verified`.** No operator
  page read in any session printed the address, so it had been left blank; the county record prints it. The
  property's own map and poker page remain the source for the room being at The Palazzo, level 2 of the
  Grand Canal Shoppes.
* **Bellagio, ARIA and Caesars Palace: verified from the same record, one step later.** This session's own
  fetch of the guide returned only the W and V end of the table (the document is 12 chunks), so those three
  hotels were deliberately left blank rather than filled from a search excerpt. The monitor job then archived
  the whole PDF at `data/snapshots/clark_county_tle_guide.txt` (1,106 lines, fetched by GitHub Actions from the
  county's own URL at 2026-11-17T01:25Z), whose licensed-establishment table prints
  `1003760.RES-001 | Bellagio | 3600 Las Vegas Blvd S | 13.38% | RES | 1 | Resort Hotel (PGC)`,
  `2000035.RES-001 | Aria Resort & Casino | 3730 Las Vegas Blvd S | 13.38% | RES | 1 | Resort Hotel (PGC)` and
  `1136233.RES-001 | Caesars Palace | 3570 Las Vegas Blvd S | 13.38% | RES | 1 | Resort Hotel (PGC)`. All three
  rows now publish **13.38%, `verified`**, citing the licence number, and Bellagio (3600) and ARIA (3730) gain
  a licensed street address where they had none. Caesars Palace is the one property where the operator and the
  county agree on the address (`3570 Las Vegas Blvd South` vs `3570 Las Vegas Blvd S`), which is said on the
  row. **What did not change: the resort fee, the nightly rate and the cancellation deadline.** A county tax
  record says nothing about a hotel's own amenity fee, so those stay blank (U2-U4) - which is exactly the
  division this record was written to enforce. The published flag F109 carries the whole story, including that
  the snippet route was rejected before the document itself arrived.
* This record is a county publication dated July 2021. It is cited for the address and the tax **class**,
  and the 13.38% figure it prints for these resorts agrees with the Venetian's 2026 hotel terms and with
  both booking-engine breakdowns, each of which reproduces at exactly 13.38% of room + resort fee. Where
  the two disagree, the operator's current page governs the price; the county record is never used to fill
  a fee.

## 5. Rate log: one more attempt, recorded as a negative

The Dec 24–27 (NYE) window was requested from the official Venetian engine on 2026-11-17
(`…/booking?adults[]=2&arrival_date=2026-12-24&children[]=0&departure_date=2026-12-27&view=calendar`).
The calendar returned `$XXX` for every night, including the two nights it marks as selected, so **no quote
was added**: an unpriced grid is not a rate. The five dated quotes already logged (Nov 18–20, Nov 26–29,
Dec 13–20, Jan 1–6, Jan 10–15) are unchanged, each reproducing at 13.38% of room + resort fee. This is the
third session to hit the same wall on the calendar view; the quotes that worked came from the offer/booking
flow, not the calendar, and the difference is recorded here so the next session does not re-run the
calendar URL expecting numbers.

## 6. The daily feed is now machine-checked too (`scripts/verify_rows.py` gained a daily section)

Recurring formats have no dated row, so nothing checked them. `verify_rows.py` now verifies every row of
`data/daily.json` against the official document its own `source_url` points at, using the snapshot the monitor
job archived (`data/snapshots/<source id>.txt`), with four checks per row:

1. **money** — `buy_in_usd` and `guarantee_usd` must be printed as a number token in that document;
2. **time** — the published start (and any printed late-registration close) must appear as a time token;
3. **quote** — every text span a row prints inside double quotes must occur **verbatim** in the document, after
   whitespace and ligature normalisation. A quotation the source does not contain is a hard failure, not a review
   item;
4. **entry** — a row published as single entry fails if the document contains any re-entry, add-on, flight or
   Day 2 wording, and a re-entry / multi-entry row is reported for review if the document shows no such relief.

Running it found **five real defects in this session's own rows**, which are fixed: four Caesars rows quoted a
pipe-separated reflow of the schedule *table* as if it were a sentence from the flyer (the flyer prints
`10 AM $100 $50 20,000 20 Minutes $1,000`), and the Bellagio Saturday row carried a quotation mark pair whose
text came from the *poker page* rather than the structure PDF the row cites - that label is now described in
prose instead of quoted, since this check can only certify the cited document. Total after the fixes:
**335 rows, 1,218 field checks, 0 hard failures, 1 review item** (the pre-existing WPT Dec 21 8 p.m./6 p.m.
conflict, F4).

## 7. Commands run

- `python3 scripts/build_data.py` → 317 rows, 70 schedule days, 11 daily-feed formats (4 Wynn, 3 Bellagio,
  4 Caesars Palace), 78 flagged rows.
- `python3 scripts/build_site.py` → 21 pages.
- `python3 scripts/check_links.py` → OK (schemas, local links, approved source hosts, rule objects,
  schedule contract, dated rate log, provenance manifest, page links).
- `python3 scripts/verify_rows.py` → **335 rows (324 tournament + 11 daily feed), 1,218 field checks,
  0 hard failures, 1 review item** (the WPT Dec 21 8 p.m./6 p.m. conflict, published as F4).
- `NODE_PATH=/tmp/jsdom/node_modules node scripts/smoke_test.js` → 21/21 pages render.
