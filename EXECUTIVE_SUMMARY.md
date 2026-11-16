# Executive Summary: Las Vegas Strip Poker Plan

*Sources read 2026-11-16 · Data: `data/tournaments.json`, `data/hotels.json`, `data/schedule.json`, `data/hotel_rates.json`*

## Bottom line

- **80 single-entry tournaments are verified.** Each has its official structure sheet read, and none of
  those sheets contains a re-entry, rebuy, add-on, subsequent-buy-in or multi-flight clause. 54 are in the
  Venetian DeepStack Extravaganza IV (Nov 18 - Dec 23, 2026) and 26 in the DeepStack Extravaganza NYE
  (Dec 24, 2026 - Jan 10, 2027). Buy-ins run from $100 to $1,100.
- **22 of those 80 are plain freezeouts.** The other 58 are single entry but carry a bounty, progressive
  knockout, satellite, milestone or team format. Those formats do not let a player take a second entry, so
  they stay in the single-entry section and the Format filter sets them aside.
- **184 rows are in the separate section.** 47 allow more than one entry, 28 offer re-entry, 16 are Day 2
  continuations that take no new entry, and 93 have no confirmed entry rule. The 93 are 62 Wynn WPT rows and
  all 31 Wynn Signature Series rows.
- **The house fee is inside the buy-in, not on top of it.** Every official sheet read here withholds the fee
  from the buy-in: a $300 buy-in with $58 withheld puts $242 into the prize pool. The money a player commits
  to enter is the buy-in.
- **Hotels are confirmed on terms, not on price.** The resort fee, Clark County room tax, parking,
  cancellation, occupancy and incidental deposit are verified from each property's own official terms for
  seven hotels. **No date-specific room rate could be confirmed, so no true cost per night is stated.**
- **The 8 AM question has a clear answer.** No confirmed single-entry event starts before 9:10 AM, and that
  one is a turbo milestone satellite. The earliest confirmed single-entry *freezeout* starts at 10:10 AM.
  There is no verified 8 AM event anywhere in this dataset.

## 1. Best single-entry tournaments by guarantee per buy-in

Guarantee divided by buy-in is a descriptive ratio of two published numbers. It is not a forecast, and for a
bounty event the guarantee includes money paid out as bounties rather than as a pure prize pool. The eight
below are the top of the ranking. The Single entry page lists all 80 and sorts by any column.

| # | Date | Start | Event | Buy-in | Guarantee | GTD ÷ buy-in | House fee | Format | Source |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Dec 9, 2026 | 11:10 AM | $800 No Limit Hold'em Bounty, $75K GTD | $800 | $75,000 | 93.8× | 12.5% | Bounty | [Sheet 16](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_16.pdf) |
| 2 | Dec 16, 2026 | 11:10 AM | $600 No Limit Hold'em Bounty, $50K GTD | $600 | $50,000 | 83.3× | 15.0% | Bounty | [Sheet 11](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_11.pdf) |
| 3 | Dec 30, 2026 | 11:10 AM | $600 No Limit Hold'em, $50K GTD | $600 | $50,000 | 83.3× | 15.0% | Plain freezeout | [NYE sheet 12](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_dec_2026-structure_12.pdf) |
| 4 | Dec 15, 2026 | 11:10 AM | $1,100 No Limit Hold'em Progressive Knockout, $75K GTD | $1,100 | $75,000 | 68.2× | 11.8% | Progressive knockout | [Sheet 24](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_24.pdf) |
| 5 | Dec 6, 2026 | 11:10 AM | $600 No Limit Hold'em, $40K GTD | $600 | $40,000 | 66.7× | 15.0% | Plain freezeout | [Sheet 14](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_14.pdf) |
| 6 | Dec 2, 2026 | 10:10 AM | $600 No Limit Hold'em Seniors, $40K GTD | $600 | $40,000 | 66.7× | 15.0% | Seniors (50+) | [Sheet 10](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_10.pdf) |
| 7 | Nov 27, 2026 | 11:10 AM | $600 No Limit Hold'em, $30K GTD | $600 | $30,000 | 50.0× | 15.0% | Plain freezeout | [Sheet 6](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_6.pdf) |
| 8 | Dec 3, 2026 | 12:10 PM | $600 BIG O, $25K GTD | $600 | $25,000 | 41.7× | 15.0% | Plain freezeout | [Sheet 8](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_8.pdf) |

If the aim is a plain single-entry freezeout with the biggest published guarantee, the pick is **Dec 30,
2026, $600 No Limit Hold'em, $50,000 guaranteed**. If a bounty is acceptable, the **Dec 9 $800 bounty** has the
highest guaranteed money per dollar of buy-in.

## 2. The sequence of a trip

The schedule page gives every date a primary event and, where one exists, a conditional fallback. 45 of the 52
dates in the plan carry at least one confirmed single-entry event, and 22 carry a plain freezeout. The
workable shape of a stay:

- **Nov 18 - Nov 27:** the plain freezeouts are $300 (Nov 18), $200 RaceDay Stack (Nov 19 - 21, 10:10 AM),
  $200 (Nov 22), $400 (Nov 25), $300 (Nov 26) and $600/$30K (Nov 27). Nov 28 and Nov 29 add a $600 and a $400
  bounty and a $300 PLO double-board event.
- **Dec 2 - Dec 17:** the strongest stretch. Dec 2 and Dec 8 are $600 Seniors $40K; Dec 3 is $600 BIG O; Dec 6
  is $600/$40K; Dec 9 is the $800/$75K bounty; Dec 10 is the $800 LIPS Ladies $40K; Dec 15 is the $1,100
  progressive knockout; Dec 17 is $600 PLO double board. Several of these dates sit alongside the WPT World
  Championship at Wynn, a 13-minute walk from the Venetian.
- **Dec 23 - Jan 10:** the NYE series. Dec 23 $600/$30K, Dec 24 and Dec 25 $400/$15K, Dec 30 $600/$50K and
  Dec 31 $400/$15K, then Jan 6 $400/$15K and Jan 10 $400 Seniors $20K. **Dec 30 is the strongest single-entry
  freezeout in the whole plan.**
- **Dec 5 and Dec 19 have no confirmed single-entry event.** Those dates are consumed by WPT Day 1 flights and
  Venetian multi-flight Day 1s, which sit in the separate section.

## 3. What is confirmed for the hotels

| Hotel | Resort fee | Room tax | Self parking, registered guest | Cancellation | Sleeps | Source |
|---|---|---|---|---|---|---|
| The Venetian Resort | $55 + tax | 13.38% | $20/day | Offer-dependent, unverified | Not stated as a number | [Terms](https://www.venetianlasvegas.com/legal/hotel-terms-and-conditions.html) |
| The Palazzo | $55 + tax | 13.38% | $20/day | Offer-dependent, unverified | Not stated as a number | [Poker suites](https://www.venetianlasvegas.com/resort/casino/poker/poker-suites.html) |
| Wynn Las Vegas | $55 + tax | 13.38% | Included | 48 hours (offer terms) | 4 | [Terms](https://www.wynnlasvegas.com/terms-and-conditions/848671) |
| Encore at Wynn | $55 + tax | 13.38% | Included | 48 hours (offer terms) | 4 | [Terms](https://www.wynnlasvegas.com/terms-and-conditions/848671) |
| Bellagio | $55 + tax | 13.38% | $20/day | 72 hours | Not stated as a number | [Terms](https://bellagio.mgmresorts.com/en/terms-and-conditions.html) |
| ARIA | $55 + tax | 13.38% | $20/day | 72 hours | Not stated as a number | [Terms](https://aria.mgmresorts.com/en/terms-and-conditions.html) |
| Caesars Palace | $54.95 + tax *(secondary source)* | 13.38% | $20/day | Not verified | Not stated as a number | [Hotel page](https://www.caesars.com/caesars-palace/hotel-information/) |

The Venetian and the Palazzo are the only properties with a published poker-player rate: suites **from $119**
(a standard room) and **from $209** (a larger suite), conditional on playing six hours of cash poker or
entering a $300 or larger tournament for every night stayed, quoting code `EPOKR25`. That is a starting rate,
not a quote for your dates.

**Walking is the deciding factor, not the nightly rate.** The Venetian and the Palazzo are inside the same
complex as the DeepStack room, so the walk is 0 minutes. Wynn and Encore are a 13 to 15 minute walk from the
Venetian. Bellagio is a 28 minute walk (2.1 km) and ARIA is a 31 minute walk (2.3 km). If the plan is built
around the Venetian series, staying at the Venetian or the Palazzo removes the walk entirely.

## 4. What is not confirmed, and why

| Gap | Why it is still open | What would close it |
|---|---|---|
| No room rate for any hotel | Every official booking engine is a JavaScript application that returns no static rate to a plain fetch, and no property publishes a rate card. | One dated quote per property, same dates and occupancy, recorded in the Hotel rate log. |
| Caesars resort fee | Caesars' own page carries no fee table. The $54.95 figure is a secondary travel-industry source. | The Caesars resort-fee page, or a booking confirmation showing the fee. |
| 93 tournament rows with no entry rule | The Wynn WPT structure PDF extraction stops after the Dec 3 - 5 event, and the Wynn Signature Series structures document is a "COMING SOON" placeholder with no structure in it at all. | A complete WPT structures PDF, and the Signature Series structures once published. |
| Bellagio Saturday buy-in | The official sheet contradicts itself across its title, header and rule text, and refers to a September 2026 Day 2. | A corrected Bellagio Saturday sheet. |
| Venetian and Palazzo maximum occupancy | The official terms charge $50 per additional guest but do not state a maximum number. | The room-type page or the booking engine's occupancy selector. |
| No published finish time for any event | No official source prints a projected finish time. | Nothing public. The printed late-registration cutoff is used instead and labelled as such. |

## 5. How this site stays honest

- Every tournament and hotel row links to the official document it was read from.
- A blank means the document did not state it. Nothing is interpolated, averaged or carried over from a
  similar property.
- Contradictions in official documents are reproduced on the Irregularity log page rather than quietly
  resolved.
- A scheduled job re-fetches every official source, hashes it and flags any document that has moved. The
  status of each source is on the Official sources page.

*Flags do not block publication. Each one is visible, sourced, and paired with the document that would
settle it.*
