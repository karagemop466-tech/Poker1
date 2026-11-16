# Questions and Information Gaps

For each question: what is known now, what is missing, and how to close it. **Open** means no official source answers it yet.

## A. Decisions only you can make

| # | Question | Why it matters | Status |
|---|---|---|---|
| D1 | Should a player who busts one flight and enters a later flight count as a second entry? | 27 rows depend on it, including the $800 Event 26 ($500K) and the $2,200 Event 47 ($1M). If a bust-out re-entry is allowed, these are not single-entry events. | Open. Ask the poker room (C1). |
| D2 | Should age- or gender-limited events be ranked with open events? | 6 verified single-entry rows are limited: events 24 and 32 (50+), event 39 (LIPS Ladies, female), event 35 (tag team, female/male), and events 49 (50+, multi-flight). | Open. They are listed with a note. |
| D3 | What is your nightly budget, including resort fee and tax? | Hotel ranking and the trip-cost calculator depend on it. | Open. |
| D4 | Which nights do you plan to stay? | Only fixed dates allow a dated rate quote, a day-by-day schedule and a like-for-like hotel comparison. | Open. |
| D5 | What is your quality floor for a hotel? | You said cost and quality outrank distance. Without a floor, hotels cannot be ranked. | Open. |
| D6 | Should bounty events count as single entry? They add no second buy-in, but the guarantee includes bounties (F6), so the pool ÷ fee ratio is not comparable to a freezeout. | Changes the ranking. | Open. Kept in the ranking with a **(bounty)** label. |
| D7 | Should the WSOP Circuit or Planet Hollywood series be included? | No verified 2027 Las Vegas Circuit schedule exists in this data. | Open. |
| D8 | How late will you play? Several days have an 11:10 AM event and a 5:10 PM event; 10 of them are flagged as a tight turnaround. | Determines whether the fallback is realistic for you. | Open. |

## B. Information that is missing or unverified

| # | Question | Known now | Missing | How to close it |
|---|---|---|---|---|
| I1 | Are the 50 verified single-entry rows truly single entry? | Each official structure sheet was read and shows no re-entry, rebuy, add-on or flight clause. | A written "no re-entry" sentence, or written confirmation from the room. The sheets' silence is an absence-of-clause finding, not a written guarantee. | Ask the poker room (C1). |
| I2 | Entry rules for 51 Wynn WPT rows | 35 WPT rows are confirmed re-entry from the official structures PDF. The PDF covers only 13 of ~30 distinct WPT events (F13). | The remaining events' structure documents. | Find the remaining official WPT structure documents, or ask the Wynn poker room. |
| I3 | Entry rules for 21 Venetian NYE rows | Sheets 1 and 2 read (10 rows). Sheet 1 confirms events 1, 3, 17 as single entry; sheet 2 produced flag F5. | NYE sheets 3, 6, 8, 9, 10, 11, 12, 13, 14, 15. | Read each NYE sheet from the [NYE event page](https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-dec-2026.html). |
| I4 | Entry rules for 31 Wynn Signature Series rows (Jan 11–24, 2027) | Schedule and buy-ins are official. | A structures document. None was found on an official source. | Ask the Wynn poker room, or watch for an official structures PDF. |
| I5 | Nightly room rate for each hotel on your dates | None verified. | Every rate. | Check each official booking page for your dates and record checkout total, nightly average, resort fee, tax, parking, cancellation deadline and a timestamp (schema in `data/hotel_rates.json`). |
| I6 | Resort fee, tax, parking and cancellation for Bellagio, ARIA and Caesars Palace | Caesars: official range $45–$50 only. Bellagio and ARIA: nothing. | Property-specific figures. | Read each property's official resort-fee and parking terms. |
| I7 | Poker-suite rate mapping | Official page says "$119 and $209" for the Venetian or Palazzo, conditional on play. | Which rate belongs to which tower, and the play requirement. | Ask the Venetian poker room (C1). |
| I8 | Itemized tax-and-fee total for a given room and stay | Venetian terms state a $55 fee plus applicable tax and 13.38% Clark County Room Tax, but publish no worked example (F11). | A dated itemized quote or final folio. | Obtain an official booking quote for your exact dates. |
| I9 | WPT $1M addition and the Nevada footnote (F7) | Footnote says ClubWPT Gold is not available in Nevada. | Whether the $1M is paid to Nevada players. | Ask the Wynn poker room (C1). |
| I10 | Ladies WPT entry (F8) | Footnote gives $11,100 with a discounted ladies entry; the printed buy-in is $1,100. | What a ladies player actually pays. | Ask the Wynn poker room (C1). |
| I11 | Registration opening times | Schedules print a registration CLOSE time per event. | Opening times. | Ask the poker room (C1). |
| I12 | Event finish times | Not published anywhere official (U11). | Every finish time. | This is why the schedule overlap check uses official registration windows instead. Ask the room for typical run times. |
| I13 | 2027 Las Vegas WSOP Circuit schedule | Only leads found. | 2027 dates and buy-ins. | Check the official WSOP Circuit calendar on wsop.com. |

## C. Suggestions for discovering the missing information

1. **Contact the poker rooms.** The Wynn schedule prints (702) 770-7654 and wynnpoker.com. The Venetian poker room is at venetianpokerroom.blog. Ask about D1, D2, I1, I7, I9, I10, I11 and I12.
2. **Read the remaining structure sheets.** Venetian NYE sheets 3, 6, 8, 9, 10, 11, 12, 13, 14 and 15, plus the WPT and Signature Series structures documents if they exist. Note that satellites (DSE IV sheets 19, 24, 25) are not needed — satellites are excluded from the dataset.
3. **Record official rates on your dates.** For each candidate hotel record: check-in, check-out, nights, occupancy, nightly rate, mandatory resort fee, tax, parking, cancellation deadline, checkout total, nightly average and a timestamp. That makes stays comparable like for like, and feeds the rate log.
4. **Measure the walking routes.** Use a mapping service at walking pace for each of the 14 hotel–venue pairs. Record the result with the date and mark it as a measured estimate, not an official figure. The site applies the 30-minute limit as soon as a value exists.
5. **Let the change monitor run.** `scripts/check_sources.py` runs daily in GitHub Actions, stores a checksum per official source and opens an issue when one changes. Re-verify the rows from any changed page.
6. **Keep every value dated.** Each row carries `last_checked`; each structured rule field carries `retrieved_on` and its own source URL, so a stale value is visible.
