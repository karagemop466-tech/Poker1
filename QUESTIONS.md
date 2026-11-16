# Questions and Information Gaps

For each question: what is known, what is missing, and how to close it. "Open" means no official source answers it yet.
"Closed" means an official source now answers it and the answer is in the dataset.

## A. Decisions only you can make

| # | Question | Why it matters | Status |
|---|---|---|---|
| D1 | Should a player who busts from one flight and enters a later flight count as a second entry? | 60 multi-flight rows depend on it, including the $800 Event 26 at $500K. | Open. Ask the poker room (see C1). |
| D2 | Should age-limited events (50+ Seniors, ladies-only, tag-team) be ranked with open events? | Several verified rows are age-limited (Events 24, 32, 33, 37, 49). | Open. Currently listed with a note. |
| D3 | What is your nightly budget, including resort fee and tax? | Hotel ranking depends on it. | Open. The calculator answers it as soon as you enter a rate. |
| D4 | Which nights do you plan to stay? | Only chosen dates allow a rate check and a day-by-day schedule. | Open. The date selector on the schedule page uses the same dates. |
| D5 | Should bounty events count as single entry? They add no buy-in, but the guarantee includes bounties (F14). | Changes the ranking. | Open. Kept, with a note. |
| D6 | Should the milestone satellites count as single-entry tournaments? Their structure sheets contain no re-entry clause, so they are listed as single entry, but they award **seats, not cash**. | Twenty rows sit in the single-entry list with a seat prize instead of a dollar guarantee. | Open. They are marked with a `satellite` label and a `prize_text` value. |
| D7 | Should the WSOP Circuit or Planet Hollywood series be included? | No verified 2027 Las Vegas schedule in this data. | Open. |

## B. Information that is missing or unverified

| # | Question | Known now | Missing | How to close it |
|---|---|---|---|---|
| I1 | Are the 80 verified single-entry rows truly single entry? | Every Venetian structure sheet was read: 37 of 37 for DeepStack Extravaganza IV and 15 of 15 for the NYE series. None of them carries a re-entry, rebuy, add-on or flight clause. | Written confirmation from the poker room. | Ask the poker room (C1). |
| I2 | Entry rules for the 135 Wynn WPT rows | 14 official structure sheets read: $600 NLH, $800 NLH, $1,600 NLH, WPT Prime, PLO Mystery Bounty, $600 NLH Turbo, $400 PLO, $1,100 PLO, TORSE, Mixed Triple Draw, HORSE, Limit Omaha 8, Limit Omaha 8/Stud 8. Fee splits, stacks, level lengths, action-clock terms and payout rules are stored. | Structure sheets for the milestone and satellite rows, and for the events listed only on the schedule. | The official structures PDF publishes no sheet for the satellites; ask the Wynn poker room (C1). |
| I3 | Entry rules for the 49 Venetian NYE rows | **Closed.** All 15 NYE structure sheets were read on 2026-11-16. | Nothing for the entry rule. | - |
| I4 | Entry rules for the 38 Wynn Signature Series rows (Jan 11 – 24, 2027) | The official schedule is complete and read. | Structure sheets. The official Wynn Signature Series Structures PDF contains only a "COMING SOON" placeholder. | Re-check the official structures PDF once Wynn publishes it; the monitoring job flags the change. |
| I5 | Remaining Venetian DSE IV structure sheets | **Closed.** All 37 sheets were read on 2026-11-16. | Nothing. | - |
| I6 | Nightly room rate for each hotel on your dates | One dated quote is on file: Palazzo Luxury King, Nov 26 – 29, 2026, two adults, three nights, $2,412.44 checkout total, $284.69 taxes, $804.15 true cost per night. | Every other rate, on every other date. | Check the official booking page for the chosen dates and add the quote to `data/rates.json` with its date. |
| I7 | Resort fee at Bellagio, Caesars Palace and ARIA | Venetian, Palazzo, Wynn and Encore have a verified $55 fee. | The other three property fees. | Read each property's official resort-fee terms. The earlier general Caesars range was not supported by a page read here and was removed. |
| I8 | Poker-suite rate mapping | The official page says "$119 and $209" for the Venetian or the Palazzo, conditional on qualifying play. | Which rate belongs to which property, and the exact play requirement. | Ask the Venetian poker room (C1). |
| I9 | The exact tax-and-fee total for a given room and stay at each hotel | The Venetian terms state a $55 resort fee plus applicable tax and a 13.38% Clark County Room Tax. The calculator uses the logged quote when the dates match and otherwise leaves unverified inputs blank. | Date-specific room rates for the other properties and an itemised quote. | Obtain a dated official booking quote for each selected hotel and stay and add it to the rate log. |
| I10 | WPT $1M addition and the Nevada footnote (F7) | The footnote says ClubWPT Gold is not available in Nevada. | Whether the $1M is paid to Nevada players. | Ask the Wynn poker room (C1). |
| I11 | Ladies WPT entry (F8) | The footnote gives $11,100 with a discounted ladies entry; the printed buy-in is $1,100. | The amount a ladies player actually pays. | Ask the Wynn poker room (C1). |
| I12 | Registration opening times | The structure sheets print a registration close time per event. | Opening times. | Ask the poker room (C1). |
| I13 | 2027 Las Vegas WSOP Circuit schedule | Only leads found. | 2027 dates and buy-ins. | Check wsop.com's official Circuit calendar. |
| I14 | Which time is right for the December 21 $600 NLH Turbo: 8 p.m. or 6 p.m.? (F4) | Both official sources were read; they disagree. | A single confirmed time. | Ask the Wynn poker room (C1), or check the poker room board on the day. |
| I15 | Which Wynn WPT day is the block printed under "Dec. 18 Wednesday"? (F3) | Stored as December 16, 2026 because that is the only reading that fits the World Championship day order. | Confirmation from Wynn. | Ask the Wynn poker room (C1). |
| I16 | Which event owns each WPT "Day 2" row? (F5) | The structure sheets were used where they exist. | Confirmation for the rows with no structure sheet. | Ask the Wynn poker room (C1). |
| I17 | Do the milestone satellites end when the seats run out, or when the chip milestone is reached? | The structure sheets describe both endings: clause 09 (200,000-chip milestone) and clause 10 (play ends when the remaining seats equal the seats left to award). | Which ending a player should plan for. | Read the rules again with the poker room, or use the estimated end time as an upper bound. |

## C. Suggestions for discovering the missing information

1. **Contact the poker rooms.** The Wynn schedule prints (702) 770-7654 and wynnpoker.com. The Venetian poker room is at venetianpokerroom.blog. Ask about D1, I8, I10, I11, I12, I14, I15 and I16.
2. **Re-check the Signature Series structures PDF.** Wynn publishes it at a fixed URL; the monitoring job records its status every day, so a change from "COMING SOON" shows up automatically.
3. **Record official rates on a date.** Pick your dates, open each official booking page, and add the quote to `data/rates.json` with its date and the number of nights. The rate log keeps every quote instead of overwriting it.
4. **Measure walking routes.** Use a mapping service at walking pace for each hotel-to-venue pair, then record the value in `data/walking.json` and mark it as an estimate with the date. The 30-minute rule applies to a value only once one exists.
5. **Keep a dated change log.** Every row carries a verified date, and `scripts/monitor_sources.py` reports which rows changed since the last verified snapshot.
