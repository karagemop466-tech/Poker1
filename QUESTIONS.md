# Questions and Information Gaps

For each question: what is known, what is missing, and how to close it. "Open" means no official source answers it yet.
"Closed" means an official source now answers it and the answer is in the dataset.

## A. Decisions only you can make

| # | Question | Why it matters | Status |
|---|---|---|---|
| D1 | Should a player who busts from one flight and enters a later flight count as a second entry? | 60 multi-flight rows depend on it, including the $800 Event 26 at $500K. | Open. Ask the poker room (see C1). |
| D2 | Should age-limited events (50+ Seniors, ladies-only, tag-team) be ranked with open events? | Several verified rows are age-limited (Events 24, 32, 33, 37, 49). | Open. Currently listed with a note. |
| D3 | What is your nightly budget, including resort fee and tax? | Hotel ranking depends on it. | Open. Five dated quotes bracket the range: **$320.02 to $911.86 true cost per night**, and the same tower swings $338.48 (Dec 13–20) to $911.86 (Jan 1–6), so dates matter more than the property. |
| D4 | Which nights do you plan to stay? | Only chosen dates allow a rate check and a day-by-day schedule. | Open. The rate log covers Nov 26–29, Dec 13–20, Jan 1–6 and Jan 10–15; any other date needs a fresh quote. |
| D5 | Should bounty events count as single entry? They add no buy-in, but the guarantee includes bounties (F14). | Changes the ranking. | Open. Kept, with a note. |
| D6 | Should the milestone satellites count as single-entry tournaments? Their structure sheets contain no re-entry clause, so they are listed as single entry, but they award **seats, not cash**. | Twenty rows sit in the single-entry list with a seat prize instead of a dollar guarantee. | Open. They are marked with a `satellite` label and a `prize_text` value. |
| D7 | Should the WSOP Circuit or Planet Hollywood series be included? | No verified 2027 Las Vegas schedule in this data. | Open. |

## B. Information that is missing or unverified

| # | Question | Known now | Missing | How to close it |
|---|---|---|---|---|
| I1 | Are the 80 verified single-entry rows truly single entry? | Every Venetian structure sheet was read: 37 of 37 for DeepStack Extravaganza IV and 15 of 15 for the NYE series. None of them carries a re-entry, rebuy, add-on or flight clause. | Written confirmation from the poker room. | Ask the poker room (C1). |
| I2 | Entry rules for the 136 Wynn WPT rows | 14 official structure sheets read: $600 NLH, $800 NLH, $1,600 NLH, WPT Prime, PLO Mystery Bounty, $600 NLH Turbo, $400 PLO, $1,100 PLO, TORSE, Mixed Triple Draw, HORSE, Limit Omaha 8, Limit Omaha 8/Stud 8. Fee splits, stacks, level lengths, action-clock terms and payout rules are stored. | Structure sheets for the milestone and satellite rows, and for the events listed only on the schedule. | The official structures PDF publishes no sheet for the satellites; ask the Wynn poker room (C1). |
| I3 | Entry rules for the 49 Venetian NYE rows | **Closed.** All 15 NYE structure sheets were read on 2026-11-16. | Nothing for the entry rule. | - |
| I4 | Entry rules for the 38 Wynn Signature Series rows (Jan 11 – 24, 2027) | The official schedule is complete and read. | Structure sheets. The official Wynn Signature Series Structures PDF contains only a "COMING SOON" placeholder. | Re-check the official structures PDF once Wynn publishes it; the monitoring job flags the change. |
| I5 | Remaining Venetian DSE IV structure sheets | **Closed.** All 37 sheets were read on 2026-11-16. | Nothing. | - |
| I6 | Nightly room rate for each hotel on your dates | **Five dated quotes on file**, all from the Venetian's official engine: Nov 18–20 ($475.35/night), Nov 26–29 ($804.15), Dec 13–20 ($338.48), Jan 1–6 ($911.86), Jan 10–15 ($320.02). Each reproduces exactly at 13.38% of room + resort fee. | Any other date, and **every** Wynn/Encore rate: its engine renders the grid client-side and returns no quote to a text fetch. | Open each official booking engine for the chosen dates and add the quote to `data/rates.json` with its timestamp; the log keeps every quote instead of replacing one. |
| I7 | Resort fee and room tax at Bellagio, Caesars Palace, ARIA and Wynn's tax | Venetian and Palazzo: $55 fee and 13.38% tax, both verified. Wynn and Encore: $55 fee verified, tax blank. Bellagio, Caesars and ARIA: both blank. | The three properties' fees and taxes, and Wynn's tax rate. Twelve candidate official URLs were tried on 2026-11-17 and none published a value (F47, F46). | Read each property's official resort-fee or policies page — the URLs tried are listed in FLAGGED.md so the next attempt does not repeat them — or capture a booking-engine breakdown that prints the tax line. |
| I8 | Poker-suite rate mapping | The official page says "$119 and $209" for the Venetian or the Palazzo, conditional on qualifying play. | Which rate belongs to which property, and the exact play requirement. | Ask the Venetian poker room (C1). |
| I9 | The exact tax-and-fee total for a given room and stay | **Closed for every logged quote.** Both engines print an itemised breakdown (nightly rates, resort fee, taxes, total), which is stored per quote. The Jan 10–15 stay is identical at both properties: $1,600.08 total, $188.83 tax, $320.02 per night. | Other dates. | Add a quote for the dates you pick. |
| I9b | Does the Venetian's free-cancellation deadline match Wynn's 48 hours? | Wynn publishes 48 hours plus a one-night deposit. The Venetian publishes only that prepaid offers are non-cancellable. | The Venetian's deadline for a general rate. | Ask the Venetian reservation line (866.255.8936) or read the rate's own terms in the booking flow. |
| I10 | WPT $1M addition and the Nevada footnote (F7) | The footnote says ClubWPT Gold is not available in Nevada. | Whether the $1M is paid to Nevada players. | Ask the Wynn poker room (C1). |
| I11 | Ladies WPT entry (F8) | The footnote gives $11,100 with a discounted ladies entry; the printed buy-in is $1,100. | The amount a ladies player actually pays. | Ask the Wynn poker room (C1). |
| I12 | Registration opening times | **Partly answered for Wynn.** The official Wynn daily tournament terms state: *"Registration for each Event will open four (4) hours prior to the scheduled start of play"*, so the 12 p.m. daily events open registration at 8 a.m. | Venetian opening times, and Wynn opening times for WPT and Signature Series events (those PDFs print a close time only). | Ask the Venetian poker room; watch the WPT and Signature Series structures documents. |
| I13 | 2027 Las Vegas WSOP Circuit schedule | Only leads found. | 2027 dates and buy-ins. | Check wsop.com's official Circuit calendar. |
| I14 | Which time is right for the December 21 $600 NLH Turbo: 8 p.m. or 6 p.m.? (F4) | Both official sources were read; they disagree. | A single confirmed time. | Ask the Wynn poker room (C1), or check the poker room board on the day. |
| I15 | Which Wynn WPT day is the block printed under "Dec. 18 Wednesday"? (F3) | Stored as December 16, 2026 because that is the only reading that fits the World Championship day order. | Confirmation from Wynn. | Ask the Wynn poker room (C1). |
| I16 | Which event owns each WPT "Day 2" row? (F5) | The structure sheets were used where they exist. | Confirmation for the rows with no structure sheet. | Ask the Wynn poker room (C1). |
| I17 | Do the milestone satellites end when the seats run out, or when the chip milestone is reached? | The structure sheets describe both endings: clause 09 (200,000-chip milestone) and clause 10 (play ends when the remaining seats equal the seats left to award). | Which ending a player should plan for. | Read the rules again with the poker room, or use the estimated end time as an upper bound. |

## C. Suggestions for discovering the missing information

1. **Contact the poker rooms.** The Wynn schedule prints (702) 770-7654 and wynnpoker.com. The Venetian poker room is at venetianpokerroom.blog. Ask about D1, I8, I10, I11, I12, I14, I15 and I16.
2. **Re-check the Signature Series structures PDF.** Wynn publishes it at a fixed URL; the monitoring job records its status every day, so a change from "COMING SOON" shows up automatically.
3. **Record official rates on a date.** Pick your dates, open each official booking page, and add the quote to `data/rates.json` with its date and the number of nights. The rate log keeps every quote instead of overwriting it.
4. **Measure walking routes.** *Done on 2026-11-17:* all twelve hotel-to-poker-room pairs are now routed on the OpenStreetMap foot network from geocoded coordinates, with the geocoding lookup and routing query linked on every row. The remaining gap is that these are routed times, not a property's own published time — none exists (F49).
5. **Keep a dated change log.** Every row carries a verified date, and `scripts/monitor_sources.py` reports which rows changed since the last verified snapshot.

## D. Added 2026-11-17 (open after the official re-read)

| # | Question | What is known | What is missing | How to close it |
|---|---|---|---|---|
| Q-D1 | What is the Saturday Bellagio buy-in: $1,000 or $1,100? | The flyer heading says $1,100 and the page label says $1,000; rule 7 refers to $600 (F32). | One official figure, with its structure. | Call the Bellagio poker host printed on the official poker page (702.693.7291) or write to the e-mail printed there. |
| Q-D2 | Is the Bellagio flyer schedule current? The page notice says "resume on Saturday, July 26" (F34). | The notice does not match the calendar (July 26, 2026 is a Sunday). | Whether the weekly events still run and on which dates. | Same poker host contact (Q-D1). |
| Q-D3 | Should Bellagio's weekly events, which allow re-entry, be shown in the separate section? | They are described on the venue page, but no dated rows exist. | A decision on whether undated recurring formats belong in the tables. | Your decision. The site currently keeps them on the venue page only. |
| Q-D4 | What are the current Caesars Palace daily buy-in, guarantee and add-on? | The official article (2026-07-17) gives $100, $1,000 guarantee and a $50 add-on. | A structure sheet or current official schedule. | Ask the room (the article gives only the hotel number, 866-227-5938) and look for a structure sheet on caesars.com. |
| Q-D5 | Which of the two competing datasets should be kept: `main` (80 single-entry rows) or open PR #24 (54)? | Both are from official sources; their counts do not reconcile (F39). | A decision after row-level comparison. | Integration decision. This session did not merge or close PR #24. |
| Q-D6 | Can the Wynn rate be captured for Nov 18–20? | The reservation page ignored the date parameters (F37). | A priced quote for the requested dates. | Use the Wynn calendar on wynnlasvegas.com, or call 855.788.6775 (printed on the Wynn booking page). |
| Q-D7 | Which day-by-day schedule should the trip follow if Bellagio and ARIA are added? | Only Venetian and Wynn have verified structures. | Bellagio and ARIA structures or dates. | Depends on Q-D1 and Q-D2, plus the ARIA call (702.590.7232). |
| Q-D8 | Are Google Maps or Apple Maps walking times acceptable as a labelled, non-official reference? | The 30-minute walking limit cannot be checked from an official source. Walking times were not checked on Google or Apple Maps in this session. | A decision on whether map routing counts as a reference. | Your decision. If yes, the site will show route times labelled as "map estimate, not official". |
| Q-D9 | Should Horseshoe Las Vegas (Caesars, on the Strip) be added as a venue? | The official Caesars article describes six daily games there. | A structure sheet and a fee schedule. | Your decision, then an official read of its schedule. |
