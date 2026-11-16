# Executive Summary: Las Vegas Strip Poker Plan

*Checked 2026-11-16 · Data: `data/tournaments.json`, `data/hotels.json`, `data/schedule.json`,
`data/daily.json`, `data/rates.json`, `data/venues.json`, `data/walking.json`*

## Bottom line

- **316 official rows are now published across 70 dates**, from Nov 16, 2026 to Jan 24, 2027. Every row
  carries the official URL it was read from and the excerpt that supports each rule field.
- **80 rows are verified single entry.** 60 award cash, and 20 are milestone satellites that award a
  **seat** into a bigger event rather than cash. All 37 DeepStack Extravaganza IV structure sheets and
  all 15 New Year's Eve sheets have been read, so every Venetian row in the dataset now carries a
  verified entry rule.
- **105 rows sit in the separate section** because a second entry is possible: 60 multi-flight rows
  whose sheets say a player who bags Day 2 chips may not play a later flight, and 45 Wynn rows whose
  official terms publish unlimited or limited re-entry.
- **129 rows are still unverified on the entry rule** and are not ranked: 91 Wynn WPT rows (the
  milestone satellites and the events the WPT schedule prints without a structure sheet) and all 38
  Wynn Signature Series rows, because Wynn's own structures PDF is still a "COMING SOON" placeholder.
- **Hotels are still the weakest part of the data.** The $55 resort fee is verified for The Venetian,
  The Palazzo, Wynn and Encore, and the 13.38% Clark County Room Tax is verified for The Venetian only.
  Bellagio, Caesars Palace and ARIA have no verified fee or tax. **One dated quote is on file**: a
  Palazzo Luxury King for Nov 26 – 29, 2026, two adults, three nights, $2,412.44 at checkout,
  $804.15 true cost per night. No generic nightly rate is published, so the per-hotel true cost stays
  blank and the calculator asks for a rate rather than inventing one.
- **8 AM start:** the earliest cash single-entry event in the dataset starts at **10:10 AM**. The only
  earlier single-entry start is the 9:10 AM $260 turbo milestone satellite on Dec 12, and it pays a
  seat rather than cash. The 8 to 10 AM window still holds nothing.

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
- **Re-entry offered (45 rows).** 44 Wynn WPT rows whose official terms publish unlimited re-entry
  per flight, or one entry plus one re-entry for the WPT Prime Championship, and one Venetian row
  (NYE Event 29) whose sheet applies a discount to "any subsequent re-entry".
- **Rebuy and add-on (daily feed, not ranked).** The Wynn Friday $240 format allows unlimited $200
  rebuys and a $100 add-on. Rebuy events are excluded from the ranking.

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

## 4. Hotels

| Hotel | Resort fee per night | Room rate | True cost per night | Walk to Venetian poker room | Source |
|---|---|---|---|---|---|
| The Venetian Resort | $55 plus tax (verified) | Blank (one dated quote in the rate log) | Blank (rate unverified) | Host property | [Hotel terms (official)](https://www.venetianlasvegas.com/legal/hotel-terms-and-conditions.html) |
| The Palazzo | $55 (verified; tax not stated) | Blank | Blank | Host property | [Poker suite rates incl. $55 resort fee (official)](https://www.venetianlasvegas.com/resort/casino/poker/suite-rates.html) |
| Wynn Las Vegas | $55 plus tax (verified) | Blank | Blank | Not published | [Resort fee terms (official)](https://www.wynnlasvegas.com/terms-and-conditions/848671) |
| Encore at Wynn Las Vegas | $55 plus tax (verified) | Blank | Blank | Not published | [Resort fee terms (official)](https://www.wynnlasvegas.com/terms-and-conditions/848671) |
| Bellagio | Blank | Blank | Blank | Not published | [Bellagio official home page](https://bellagio.mgmresorts.com/en.html); no Bellagio-specific fee or tax confirmed. |
| ARIA Resort & Casino | Blank | Blank | Blank | Not published | [ARIA official home page](https://aria.mgmresorts.com/en.html) and [ARIA poker page](https://aria.mgmresorts.com/en/casino/poker.html) |
| Caesars Palace | Blank | Blank | Blank | Not published | [Caesars Palace official page](https://www.caesars.com/caesars-palace); no property fee confirmed. |

The Venetian's official hotel terms state a 13.38% Clark County Room Tax and a $55 resort fee plus
applicable tax. That tax rate is not applied to the other hotels without property-specific
confirmation. Walking times are not on any official source, so they stay blank and each record carries
a walking-route link instead.

## 5. Schedule and the 8 AM goal

- **Verified options:** 45 of the 70 dates carry at least one verified single-entry event, and 41 of
  them carry a cash one. The first cash single-entry event is Nov 18 (Event 2, $300 NLH, 11:10 AM).
- **Primary and fallback:** each day names one verified single-entry event as the primary, and 24 days
  also name a conditional fallback that starts after the primary is estimated to finish. Estimated end
  times come from the published level structure and are labelled as estimates, never as official finish
  times.
- **Overlaps:** two days are flagged. Dec 12 (the $2,200 PokerAtlas flight 1A at 10:10 AM against the
  9:10 AM milestone satellite) and Jan 2 (the $1,600 MSPT 1B at 11:10 AM against the 10:10 AM
  satellite). Both involve a satellite whose end time is an upper bound, because the tournament ends
  when the seats run out.
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

## 6. What is not in the data

- No 2027 Las Vegas WSOP Circuit schedule: no official source was found (I13).
- No payout ladder for most events: only some structure sheets publish one.
- No walking times, and no nightly rate for any hotel other than the single logged quote.
- No official structure sheet exists for the Wynn WPT milestone satellites, so their entry rules stay
  unverified even though their buy-in, prize, chips and level count are official.

## 7. How to use the site

- Every tournament table has the same filter bar: text search, date range, venue, series, entry rule,
  buy-in range, labels and a single-entry-only switch.
- The schedule page has a date picker and previous/next day buttons.
- The [calculator](pages/calculator.html) prices a stay from the verified fee, tax and a rate you enter,
  and refuses to total anything that depends on an unverified figure.
- The [monitoring page](pages/monitoring.html) shows which official sources answered on the last
  check, which rows changed since the last verified snapshot, and every flagged row.
- The [search box](pages/search.html) covers every row, hotel, venue, daily format, walking record,
  rate entry and document on the site.
