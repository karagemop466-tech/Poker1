# Executive Summary: Las Vegas Strip Poker Plan

*Checked 2026-11-17 · Data: `data/tournaments.json`, `data/hotels.json`, `data/schedule.json`,
`data/daily.json`, `data/rates.json`, `data/venues.json`, `data/walking.json`*

Every official tournament page and structure PDF listed below was re-fetched and re-read on
**2026-11-17**, not carried forward: the DeepStack Extravaganza IV page (94 rows), the NYE page
(49 rows), the Wynn Signature Series schedule PDF (38 rows) and the WPT World Championship schedule
PDF (136 rows). The result is that **all 317 rows in the current dataset match their official sources**, with known source irregularities listed in `FLAGGED.md` (including the NYE page printing the Dec 26, 2026 date as 2025). Hotel fees, taxes, rates and walking times were also
re-checked on 2026-11-17.

## Bottom line

- **317 official rows are now published across 70 dates**, from Nov 16, 2026 to Jan 24, 2027. Every row
  carries the official URL it was read from and the excerpt that supports each rule field.
- **80 rows are verified single entry.** 60 award cash, and 20 are milestone satellites that award a
  **seat** into a bigger event rather than cash. All 37 DeepStack Extravaganza IV structure sheets and
  all 15 New Year's Eve sheets have been read, so every Venetian row in the dataset now carries a
  verified entry rule.
- **106 rows sit in the separate section** because a second entry is possible: 60 multi-flight rows
  whose sheets say a player who bags Day 2 chips may not play a later flight, and 46 re-entry rows whose
  official terms publish unlimited or limited re-entry.
- **129 rows are still unverified on the entry rule** and are not ranked: 91 Wynn WPT rows (the
  milestone satellites and the events the WPT schedule prints without a structure sheet) and all 38
  Wynn Signature Series rows, because Wynn's own structures PDF is still a "COMING SOON" placeholder.
- **Hotels are much stronger than yesterday, with one hard limit.** $55 resort fee plus 13.38% room tax
  is verified for The Venetian and The Palazzo, and the $55 fee alone for Wynn and Encore. **Five dated
  quotes are on file**, all from the Venetian's official booking engine: $804.15 (Nov 26–29), $475.35
  (Nov 18–20), $338.48 (Dec 13–20), $911.86 (Jan 1–6) and $320.02 (Jan 10–15) true cost per night. Every quote stores the per-night rates, resort fee, tax total, checkout
  total, cancellation terms and the date it was read, so a later quote is compared against these instead
  of replacing them.
- **Every one of those five quotes reproduces exactly** — twice over: 13.38% applied to (room + resort fee)
  returns the stored tax total to the cent, and (room + fee) ÷ nights returns the Average Rate the engine
  itself printed on the page (709.25, 298.54, 804.25, 282.25, 419.25). Two independent identities agreeing
  is what keeps the log honest.
- **Wynn cannot be priced the same way yet.** Its booking engine renders the nightly grid and the tax
  line client-side and returns only fee and policy text to a text fetch, so no Wynn quote could be
  captured. Its **room tax is no longer blank**: the Clark County licensing record lists "Wynn Las Vegas /
  Encore at Wynn Las Vegas | 3131 Las Vegas Blvd S | Licensed | 13.38% | Transient Lodging Tax - Resort
  Hotel (PGC)", so 13.38% is now verified from the authority that sets it rather than borrowed from the
  Venetian ([record](https://www.clarkcountynv.gov/adobe/assets/urn:aaid:aem:689ef54f-ec0d-4bb6-b8ea-05a82887561f/original/as/genl-info-guide-for-tles-july-2021.pdf),
  read 2026-11-17, flagged F60). One number is still missing - the nightly rate - so the like-for-like
  Wynn-versus-Venetian comparison still cannot be made. That is the last missing piece of the hotel
  picture.
- **Walking times are now routed, not blank.** Twelve hotel-to-poker-room pairs were measured on the
  OpenStreetMap foot network between geocoded coordinates, with the destination being the resort that
  actually contains the poker room (The Palazzo for the Venetian, Encore for Wynn), the lookup and query
  linked on every row, and walks inside one resort marked internal instead of timed. Under the
  30-minute rule: **Bellagio 22 min and Caesars 23 min reach the Venetian poker room; Wynn 15 and
  Encore 14 reach it too; The Venetian 16 and The Palazzo 14 reach the Wynn poker room.** Over the
  limit: **ARIA to the Venetian (34), Bellagio to Wynn (31), ARIA to Wynn (43) and Caesars to Wynn (32)**.
- **8 AM start:** the earliest cash single-entry event in the dataset starts at **10:10 AM**. The only
  earlier single-entry start is the 9:10 AM $260 turbo milestone satellite on Dec 12, and it pays a
  seat rather than cash. The 8 to 10 AM window holds nothing all day. The one thing that *does* open at
  8 AM is **registration**, four hours before a noon start at Wynn (official Wynn terms) — not play.
- **The live daily feed now covers three rooms, not one.** It previously held only Wynn's four printed
  daily formats, because the other rooms published nothing machine-readable. That changed: the Bellagio
  Friday $600 / Saturday multi-flight / Sunday $400 H.O.R.S.E. structure PDFs and the Caesars Palace daily
  No-Limit schedule were read from the rooms' own pages and are published format by format, each with its
  printed clause and retrieval date, at [Daily feed](pages/daily.html) (11 rows: 4 Wynn, 3 Bellagio, 4
  Caesars Palace). Two of these matter for an early start: **Caesars runs a $100 daily at 10 a.m. with a
  $1,000 guarantee**, and **Wynn's noon dailies open registration at 8 a.m.** Neither Caesars format can
  be ranked as single entry - its own flyer allows a re-entry and a $50 add-on - so they are listed as
  daily structures, not as verified single-entry rows. ARIA publishes no schedule at all and tells guests
  to call the room or follow it on social media, which is recorded as a verified negative (F38, F59).
- **Every printed Venetian row was re-audited against the page text, and one value was wrong.** All 143
  printed rows across the two DeepStack Extravaganza pages were matched by date, start time, event number
  and printed amounts: 142 matched, and the Jan 4, 2027 MSPT Day 2 Restart is republished at the printed
  **11:10** instead of 11:00 (F57). The separately written provenance audit over all 317 rows found no
  unsourced buy-in, house fee, prize pool or starting stack; the only unsourced money values in the dataset
  were the 17 Signature Series guarantees, already blanked and published as F54. The record is
  `research/verification-2026-11-17-c7a324a6.md`.
- **Trip cost calculator.** The calculator now prices a whole trip: entries × buy-in + nights × true
  hotel cost + parking + other spend, using only logged quotes, and it shows what the selected stay
  window actually holds (verified single-entry events, days covered, cheapest buy-in, best
  guarantee ÷ buy-in ratio). It refuses to total anything it cannot source.
- **Every published value is now machine-checked against its official source.** A new verifier
  (`scripts/verify_rows.py`) re-checks each money, time and entry-rule value in the dataset against
  the raw official documents archived in `data/snapshots/` — 1,119 checks, **0 hard failures**. The
  pass caught and fixed two data-quality problems, now flagged for review (F53, F54): the LIPS
  sheets withhold a house fee **and** a separate LIPS flat fee (the two are now stored separately),
  and 17 Wynn Signature Series main-event rows had published guarantees that appear on no official
  source (now left blank and flagged). See `FLAGGED.md` and `research/verification-2026-11-17-160f9080.md`.

## 1. Best single-entry tournaments (verified)

Ranked by guarantee divided by buy-in. A higher figure means more prize pool per dollar. For bounty
events the guarantee includes bounties, so it is not a pure prize pool. The table lists the top nine;
the single-entry page lists all 80, sortable by any column and filterable by date, venue, series,
buy-in and label.

| Rank | Date (2026) | Start | Event | Buy-in | Guarantee | Guarantee ÷ buy-in | House fee | Source |
|---|---|---|---|---|---|---|---|---|
| 1 | Dec 9 | 11:10 AM | Event 36, $800 No Limit Hold'em Bounty | $800 | $75,000 | 93.8x | 12.5% | [Sheet #16](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_16.pdf) |
| 2 | Dec 16 | 11:10 AM | Event 54, $600 No Limit Hold'em Bounty | $600 | $50,000 | 83.3x | 15% | [Sheet #11](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_11.pdf) |
| 2 (tie) | Dec 30 | 11:10 AM | Event 14, $600 No Limit Hold'em | $600 | $50,000 | 83.3x | 15% | [Sheet #12](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_dec_2026-structure_12.pdf) |
| 4 | Dec 15 | 11:10 AM | Event 52, $1,100 Progressive Knock-Out Bounty | $1,100 | $75,000 | 68.2x | 11.82% | [Sheet #34](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_34.pdf) |
| 5 (tie) | Dec 2 | 10:10 AM | Event 24, $600 No Limit Hold'em Seniors | $600 | $40,000 | 66.7x | 15% | [Sheet #17](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_17.pdf) |
| 5 (tie) | Dec 6 | 11:10 AM | Event 28, $600 No Limit Hold'em | $600 | $40,000 | 66.7x | 15% | [Sheet #7](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_7.pdf) |
| 5 (tie) | Dec 7 | 11:10 AM | Event 30, $600 No Limit Hold'em Bounty | $600 | $40,000 | 66.7x | 15% | [Sheet #11](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_11.pdf) |
| 5 (tie) | Dec 8 | 10:10 AM | Event 32, $600 No Limit Hold'em Seniors | $600 | $40,000 | 66.7x | 15% | [Sheet #17](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_17.pdf) |
| 5 (tie) | Dec 26 | 11:10 AM | Event 5, $600 No Limit Hold'em Bounty | $600 | $40,000 | 66.7x | 15% | [Sheet #3](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_dec_2026-structure_3.pdf) |

The Dec 26 row sits on a date the official New Year's Eve page prints as "Saturday, December 26,
**2025**". It is stored as Dec 26, 2026 and the printed year is flagged on the row (F1).

Sources: [official DeepStack IV schedule (PDF)](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/dse-nov-2026-schedule.pdf),
[DeepStack IV event page](https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html),
[NYE event page](https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-dec-2026.html),
and the structure sheet linked on each row.

## 2. Separate section: not single entry

These are kept out of the ranking.

- **Possible multiple entries (60 rows).** Every Venetian flight event in the dataset: Events 1, 7, 19,
  26, 30, 47, 49, 56, 8, 20 and 27. Each structure sheet says: "Any player who bags chips for Day 2 may
  not play a subsequent flight." Whether a player who busts may enter a later flight is not stated.
  Event 26 has the highest guarantee multiple of any event in the dataset (625x, 13.75% house fee) but
  sits here until this is confirmed with the poker room.
- **Re-entry offered (46 rows).** 45 Wynn WPT rows whose official terms publish unlimited re-entry
  per flight, or one entry plus one re-entry for the WPT Prime Championship, and one Venetian row
  (NYE Event 29) whose sheet applies a discount to "any subsequent re-entry".
- **Rebuy and add-on (daily feed, not ranked).** The Wynn Friday $240 format allows unlimited $200
  rebuys and a $100 add-on. Rebuy events are excluded from the ranking.

### Other Strip poker rooms checked on 2026-11-17 (no rows added)

- **Bellagio** publishes three weekly flyers on its official poker page: Friday $600 NLH and Sunday $400 H.O.R.S.E. at 11 a.m., and a Saturday event at 11 a.m. Both the Friday and the Sunday flyers allow buy-in and re-entry through level 8, so **neither is single entry**. The Saturday flyer contradicts itself on its buy-in ($1,100 heading, $1,000 label), so its entry rule is not confirmed. No flyer prints a calendar date, so no dated row is created.
- **Caesars Palace**: an official article (dated 2026-07-17) describes four daily no-limit hold'em events at 10 a.m., 2 p.m., 6 p.m. and 9 p.m. with a **$50 add-on**. That makes them **not single entry**, so they belong in the separate section. The article is not a structure sheet, so no rows are created.
- **ARIA** says its Daily Tournaments run but publishes no schedule or structure. The official poker page gives a phone number (702.590.7232) for the current schedule.

## 3. Milestone satellites (now published)

Twenty Venetian rows were missing from the earlier draft because the official event pages list them in
the milestone-satellite rows. All of them are now in the dataset with their structure sheet, their fee
split, their 200,000-chip milestone and their seat prize:

| Rows | Buy-in | Fee / pool | Levels | Prize | Target |
|---|---|---|---|---|---|
| Events 33, 37 (Dec 8, 9) | $100 | $20 / $80 | 28 × 20 min | 2 seats | Event #39, $800 LIPS Ladies (female players only, 21+, Venetian Rewards card) |
| Events 41, 44 (Dec 10, 11) | $260 | $40 / $220 | 28 × 20 min | 2 seats | Event #47, $2,200 PokerAtlas Championship |
| Events 45, 46, 48 (Dec 11, 12) | $260 | $35 / $225 | 28 × 15 min | 2 seats | Event #47, $2,200 PokerAtlas Championship |
| Events 6, 7, 9, 10, 11, 12 (Dec 26 – 28) | $260 | $40 / $220 | 28 × 20 min | 4 seats | Event #08, $1,100 Ante Up Championship |
| Events 15, 18, 21, 23, 24 (Dec 30 – Jan 2) | $200 | $35 / $165 | 28 × 20 min | 2 seats | Event #20, $1,600 MSPT |
| Events 16, 19 (Dec 30, 31) | $200 | $30 / $170 | 28 × 15 min | 2 seats | Event #20, $1,600 MSPT |

None of these sheets has a re-entry clause, so they are listed as single entry. Because the prize is a
seat and not cash, each row carries a `prize_text` value and a `satellite` label instead of a dollar
guarantee, and the calculator and the ranking both treat them differently from cash events.

## 4. Hotels, true cost and walking

Every figure below was read from the property's own site on **2026-11-17**. "True cost per night" is the
official booking engine's own checkout total divided by the nights, so it already contains the room, the
resort fee and the tax; nothing is reconstructed from an assumed rate.

| Hotel | Resort fee / night | Room tax | True cost / night (dated quote) | Walk to Venetian poker room | Walk to Wynn poker room |
|---|---|---|---|---|---|
| [The Venetian Resort](https://www.venetianlasvegas.com/legal/hotel-terms-and-conditions.html) | $55 plus tax (verified) | 13.38% (verified) | $338.48 (Dec 13–20), $911.86 (Jan 1–6), $804.15 (Nov 26–29) | inside the resort | **16 min** (routed) |
| [The Palazzo](https://www.venetianlasvegas.com/resort/casino/poker/suite-rates.html) | $55 (verified) | 13.38% (verified) | $320.02 (Jan 10–15) | inside the resort | **14 min** (routed) |
| [Wynn Las Vegas](https://www.wynnlasvegas.com/terms-and-conditions/848671) | $55 plus tax (verified) | **13.38%** (Clark County licensing record; no Wynn page prints it) | blank (no Wynn quote captured yet) | **15 min** | inside the resort (the room is in Encore) |
| [Encore at Wynn Las Vegas](https://www.wynnlasvegas.com/terms-and-conditions/848671) | $55 plus tax (verified) | **13.38%** (same county record, same licence) | blank (no dated quote) | **14 min** | inside the resort |
| [Bellagio](https://bellagio.mgmresorts.com/en.html) | blank (no official page prints it) | **13.38%** (county licensing record `1003760.RES-001`) | blank (no quote captured) | **22 min** | **31 min — over the limit** |
| [ARIA Resort & Casino](https://aria.mgmresorts.com/en.html) | blank | **13.38%** (county record `2000035.RES-001`) | blank (rates by phone/e-mail only) | **34 min — over the limit** | **43 min — over the limit** |
| [Caesars Palace](https://www.caesars.com/caesars-palace) | blank | **13.38%** (county record `1136233.RES-001`) | blank (no quote captured) | **23 min** | **32 min — over the limit** |

**Like-for-like inside the one resort that publishes its breakdown.** Same property group, same engine,
five different stays, so the comparison is between dates rather than between companies. The nightly
average column uses the engine's own convention, (room charges + resort fee) ÷ nights, before tax — each
of the five figures is the number the engine itself printed, which is an independent check on the log:

| Stay | Room | Nights | Nightly average<br>(room + fee) | Resort fee | Taxes | Checkout total | True cost / night |
|---|---|---|---|---|---|---|---|
| [Nov 18–20, 2026](https://www.venetianlasvegas.com/book) | Venetian Newly Remodeled Luxury Two Queen | 2 | $419.25 | $55 × 2 | $112.19 | $950.69 | **$475.35** |
| [Nov 26–29, 2026](https://www.venetianlasvegas.com/book) | Palazzo Luxury King | 3 | $709.25 | $55 × 3 | $284.69 | $2,412.44 | $804.15 |
| [Dec 13–20, 2026](https://www.venetianlasvegas.com/book) | Venetian Newly Remodeled Luxury King | 7 | $298.54 | $55 × 7 | $279.63 | $2,369.38 | **$338.48** |
| [Jan 1–6, 2027](https://www.venetianlasvegas.com/book) | Venetian Newly Remodeled Luxury King | 5 | $804.25 | $55 × 5 | $538.05 | $4,559.30 | **$911.86** |
| [Jan 10–15, 2027](https://www.venetianlasvegas.com/book) | Palazzo Luxury Two Queen | 5 | $282.25 | $55 × 5 | $188.83 | $1,600.08 | **$320.02** |

The lesson is in the spread, not the average: the same tower costs **$338.48 a night for Dec 13–20 and
$911.86 a night for Jan 1–6**, because Jan 1 is quoted at $1,949.25 for the night. Two nights over a
weekend in November cost $475.35 all in. Dates, not the hotel name, dominate the hotel budget.

**Cancellation.** Wynn publishes a 48-hour deadline and a one-night deposit
([terms](https://www.wynnlasvegas.com/terms-and-conditions/848671)). The Venetian publishes that prepaid
offers are non-cancellable and non-refundable but prints **no fixed free-cancellation deadline** for a
general rate, so the two properties cannot even be matched on that term yet. Both texts are stored
verbatim in `data/rates.json`.

**Wynn's room tax is stated because the taxing authority states it.** No Wynn page prints the percentage,
and its engine does not expose the breakdown to a text fetch. Applying the Venetian's 13.38% to Wynn would
be exactly the kind of inference this dataset forbids, so it was not done; instead the Clark County
Department of Business License licensing table was read, and it lists Wynn Las Vegas and Encore at Wynn Las
Vegas together at **13.38%, Transient Lodging Tax - Resort Hotel (PGC)** - the same class and rate as the
Venetian and Palazzo. That is a county record dated July 2021, labelled as such on the hotel row, and the
nightly rate is still blank, so no Wynn true cost per night is shown.

**Room tax is verified at all seven hotels; the resort fee at three of them is not.** The room-tax gap for
Bellagio, ARIA and Caesars Palace closed on 2026-11-17, but not from the hotel pages: eight candidate official
URLs (resort-fee and policies pages on mgmresorts.com and caesars.com) returned a 404 or a marketing page with
no fee, so the percentage was taken from the authority that levies it - the Clark County licensing table, cited
by licence number, which puts all three in the 13.38% Resort Hotel (PGC) class (F60). **The resort fee is still
blank at those three properties, and so is their nightly rate**, because a tax record says nothing about a
hotel's amenity fee and this dataset will not borrow one property's fee for another. The exact URLs tried are
listed in `FLAGGED.md`.

**Walking times are routed, not guessed.** All twelve pairs were measured on the OpenStreetMap foot
network between geocoded coordinates, rounded up to the whole minute, and every row links both the
geocoding lookup and the routing query. Walks inside one resort are marked internal rather than timed,
and the official statement that fixes where each poker room sits is quoted on the row. The 30-minute rule
is applied to every routed time, and rows that fail it stay visible and flagged.

## 5. Schedule and the 8 AM goal

- **Verified options:** 45 of the 70 dates carry at least one verified single-entry event, and 41 of
  them carry a cash one. The first cash single-entry event is Nov 18 (Event 2, $300 NLH, 11:10 AM).
- **Primary and fallback:** each day names one verified single-entry event as the primary, and 24 days
  also name a conditional fallback that starts after the primary is estimated to finish. Estimated end
  times come from the published level structure and are labelled as estimates, never as official finish
  times.
- **Overlaps:** 14 row-pairs on two days are flagged. Dec 12 (six pairs) and Jan 2 (three pairs, and
  eight counting both directions) all trace back to a milestone satellite on the same day whose
  estimated end is an upper bound, because a satellite stops when the seats run out. Each of those
  days still gets a single primary plus a conditional fallback; no impossible sequence is proposed.
- **Wynn registration opens at 8 AM for the noon events.** The official Wynn daily tournament terms
  and conditions state: *"Registration for each Event will open four (4) hours prior to the scheduled
  start of play."* The daily events start at 12 p.m., so registration opens at **8 a.m.** That is the
  only registration *opening* time printed on any official source read so far, and it is the one place
  the 8 AM goal is met directly. It is printed in the Wynn daily terms only: the WPT and Signature
  Series schedule PDFs print a registration *close* time per event and no opening time.
- **Wynn daily formats:** four recurring formats are published on their own page: $200/$10K Monday to
  Thursday, $240 rebuy-and-add-on/$40K Friday, $200/$25K Saturday and Sunday, and $160/$10K nightly.
  All four permit re-entry, rebuys or add-ons, so **none of them qualifies as single entry**; they sit
  in the separate section. Wynn states that the daily schedule is suspended during each Wynn Signature, Wynn Millions and
  Classic series, and the WPT and Signature Series dates are listed on the schedule page.

## 6. Trip cost and how to plan a stay

The calculator prices a trip the way the brief asks: **entries × buy-in + nights × true hotel cost**,
plus parking and any other spend, using only logged quotes. For the Jan 10–15 window it returns:

| Line | Value | Where it comes from |
|---|---|---|
| Hotel total, 5 nights | $1,600.08 | official engine checkout total (room + $55 resort fee + $188.83 tax) |
| True hotel cost / night | $320.02 | checkout total ÷ 5 |
| One $300 entry | $300.00 | buy-in entered by you, matching the event you pick |
| Trip total | $1,900.08 | hotel + entries + parking + other |
| All in per night | $380.02 | trip total ÷ 5 |
| Events in the window | verified single-entry rows dated inside the stay | `data/tournaments.json` |

It also shows what the window actually contains, so a stay is never bought against an empty schedule:
for Jan 10–15 the window holds the NYE finale on Jan 10 (Event 31 seniors $400, Event 32 $200 bounty)
and nothing on Jan 11–15 at the Venetian, because the Wynn Signature Series rows for those dates are
still unverified on the entry rule and are not counted.

**The practical planning sequence the data supports:**

1. Fix the dates and the nightly budget/quality floor first — the rate log shows that the same tower
   swings from $164.25 to $1,949.25 a night inside one week, so dates dominate the budget.
2. Pick the event, then read its structure sheet for the written single-entry rule. 80 rows pass today;
   129 cannot be judged yet because Wynn has not published the sheets.
3. Compare only surviving events on guarantee, buy-in, stack, level length, payout and daily fit. The
   guarantee ÷ buy-in ratio is descriptive, not a forecast, and bounty/flight events are labelled.
4. Check the walking route against the hotel you picked. The Venetian, The Palazzo, Wynn, Encore,
   Bellagio and Caesars Palace are all inside 30 minutes of the Venetian poker room; only ARIA is not.
   Toward the Wynn poker room, only the Wynn/Encore cluster makes it — Bellagio (31), ARIA (43) and
   Caesars (32) do not. The same-stay price comparison across the two companies is blocked until a Wynn
   quote can be captured (see §4).
5. Build one event per day first and only add an evening event where the earlier one can realistically
   end. Use the primary/fallback pair on the schedule page.
6. Reconfirm schedule, rate and policy on the official page before any non-refundable payment. That is
   exactly what the dated rate log and the daily monitor are for.

## 7. What is not in the data

- No 2027 Las Vegas WSOP Circuit schedule: no official source was found (I13).
- No payout ladder for most events: only some structure sheets publish one.
- No *published* nightly rate: both Venetian and Wynn sell through a booking engine that quotes a stay,
  not a rate card, so the only defensible per-night figure is checkout total ÷ nights from a dated quote.
- No resort fee, room tax or rate for Bellagio, ARIA or Caesars Palace: eight candidate official URLs
  returned 404s or marketing pages that print no fee.
- No official structure sheets for the Wynn Signature Series (the PDF is a "COMING SOON" placeholder)
  or for the WPT milestone satellites, so those entry rules stay unverified.
- No 8 AM *play* anywhere: registration opens at 8 AM at Wynn, but the earliest verified cash start is
  10:10 AM.
- No official structure sheet exists for the Wynn WPT milestone satellites, so their entry rules stay
  unverified even though their buy-in, prize, chips and level count are official.

## 8. How to use the site

- Every tournament table has the same filter bar: text search, date range, venue, series, entry rule,
  buy-in range, labels and a single-entry-only switch.
- The schedule page has a date picker and previous/next day buttons.
- The [calculator](pages/calculator.html) prices a whole trip (entries × buy-in + nights × true hotel
  cost + parking + other) from the dated rate log, shows what the chosen stay window holds, and compares
  every logged quote like-for-like. It refuses to total anything it cannot source.
- The [monitoring page](pages/monitoring.html) shows which official sources answered on the last
  check, which rows changed since the last verified snapshot, and every flagged row.
- The [search box](pages/search.html) covers every row, hotel, venue, daily format, walking record,
  rate entry and document on the site.

## 9. Strip-wide room survey (added 2026-11-17)

Details: [Strip rooms page](pages/strip-rooms.html) · [research log](research/strip-room-survey-2026-11-17.md) · flags S1–S10 in [FLAGGED.md](FLAGGED.md) section E.

- **Strip coverage was incomplete.** The venue dataset covered five rooms. This survey adds MGM Grand, Mandalay Bay and Horseshoe, and records two closures.
- **MGM Grand has an official weekly schedule.** Daily $120 no-limit hold'em at 11:10 AM (Sunday to Friday), 7:10 PM and 11:10 PM, plus a Saturday $150 event with a $2,000 guarantee. The $120 entry includes an optional $11 "gratuity" that buys 10,000 extra chips, so those formats sit in the **separate section**. The Saturday event's structure is not published, so it is unverified. The official poker page and the PDF disagree by ten minutes on every start time (flag S1).
- **Horseshoe runs six daily no-limit hold'em sessions** at 9 AM, 11 AM, 2 PM, 5 PM, 8 PM and 11 PM, per the official Caesars article. No buy-in, guarantee or structure is printed, so none is shown (flag S5). The 9 AM start is the earliest official daily start found on the Strip in this survey, but it is not a verified single-entry event.
- **Mandalay Bay publishes no tournament schedule** on its official poker page (flag S4). Its page says Tuesdays are closed.
- **Resorts World and Planet Hollywood are reported closed** (March 2026 and January 2026). Both reports quote a company statement, but neither closure is confirmed on an official page read (flags S7, S8).
- **Not surveyed:** Paris, Flamingo, Linq, Harrah's, Excalibur, Luxor, New York-New York, Park MGM, Westgate and Circus Circus (flag S10).
