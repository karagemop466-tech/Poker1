# Executive Summary: Las Vegas Strip Poker Plan

## Booking decision · November 19, 2026

**Hold nonrefundable bookings.** None of the **74** rows now classified as single-entry candidates has a
written no-add-on rule in its structured evidence: every one says "not mentioned." The strict shortlist
is empty; the day plan is conditional. This does not mean those events allow add-ons.

**An independent audit now checks this claim on every build.** [`scripts/audit_entry_labels.py`](scripts/audit_entry_labels.py)
re-derives all **980** quoted spans in the dataset from the archived official document each row cites, and
prints the result on the [Evidence audit](pages/evidence-audit.html) page. Its headline finding is the
one that decides the trip: across **59** official documents, **not one prints a sentence that closes an
event to a second entry** — no "single entry only", no "no re-entry", no "no rebuy", no "no add-on". The
decision to hold is therefore not caution about missing paperwork; it is the measured state of the
published evidence.

The same audit found and fixed three defects in this dataset on 2026-11-19, all of which had passed every
earlier check because they were defects of *wording against its own source*, not of arithmetic:

1. **Six rows claimed a clause was absent while their own sheet printed it.** r232, r234, r245, r256,
   r262 and r279 said "no re-entry, rebuy, add-on or multi-flight clause appears anywhere on this
   structure sheet" while citing a sheet whose clause 6 reads *"The $20 discount can be applied to the
   initial entry or any subsequent re-entry."* They are now correctly **re-entry** rows. The candidate
   count therefore fell from 80 to 74, and the separate multi-entry/re-entry section grew by six.
2. **Three fee quotes could not be found in their own PDF**, and one cited the wrong clause number,
   because the excerpt was a template that painted figures over fixed wording. Every such quote is now
   lifted from the sheet's own sentence.
3. **The change monitor's "source changed" mark was comparing an empty hash.** Four rows were marked as
   if a published value had moved when the fetcher had extracted no money, date, time or entry-rule word
   from those pages at all; six distinct Caesars URLs returned one identical 5,871-byte body. That badge
   is now labelled a re-request to read the page, not evidence of a change.

**One upcoming candidate, not a recommendation:** The [Venetian schedule](https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html) lists event 12 on Thursday, November 26 at 11:10 AM. Its [official structure sheet](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_5.pdf), read in full on November 19, confirms a $300 total entry ($58 withheld), $10,000 guarantee, 40,000 starting chips, 30-minute levels, registration through approximately 4:55 PM and payouts to 12.5% of the field. The guarantee is 33.3 times one entry fee; that is not a return forecast. None of its ten clauses specifies one entry per person or expressly prohibits rebuys and add-ons. Obtain a written event-specific ruling before promoting it. Do not schedule the 5:10 PM bounty as a second entry on the assumption the first event finishes by then.

**Hotel comparison:** For November 26–29, two adults, the November 16 [Palazzo booking-engine observation](https://www.venetianlasvegas.com/book) was $2,412.44 at checkout ($804.15/night including resort fee and tax). One $300 tournament entry plus that stay would be $2,712.44 before parking and other spending. Do not multiply the rounded nightly average to reconstruct checkout. This is a historical quote, not today's availability. The log contains no competing property for that same stay. Capture a second refundable checkout for those dates and occupancy, including its cancellation deadline and parking, before naming a best hotel. An interior route does not establish a timed walk from the guest room.

## What the next decision costs

**Planning scenario, not a reservation or an inferred preference:** December 13–20, two adults, one private king suite, up to $350/night including mandatory charges. Require refundable terms and an evidenced walk of at most 30 minutes. This window has a matching historical room quote; it is not a claim that the room or a qualifying tournament is available.

| Decision | What the evidence supports | What would change the decision |
|---|---|---|
| Tournament | On November 25 the [Venetian schedule](https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html) lists event 10 at 11:10 AM. Its [sheet](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_6.pdf) confirms $400 total, $65 withheld, $15,000 guaranteed, 40,000 chips, 30-minute levels, about 4:55 PM registration close and payouts to 12.5% of the field. The 37.5× ratio is descriptive. | The ten rules do not affirm a whole-event freezeout. Require event-specific written confirmation before ranking it, even though its fee and pool are known. |
| Play from 8 AM | No verified 8 AM start in the series dataset. At [Wynn](https://www.wynnlasvegas.com/casino/poker), registration and play are separate. Nightly formats can allow re-entry. | Require a dated start, not opening hours. Treat an evening event as an alternative unless the prior event has ended and registration remains open. |
| Hotel for the scenario | The November 17 [Venetian checkout observation](https://www.venetianlasvegas.com/book) for seven nights was $2,369.38 total, $338.48/night. An on-property route avoids the street walk; no measured guest-room-to-seat time is published. | The [same-date booking lookup](https://www.venetianlasvegas.com/booking?arrival_date=2026-12-13&departure_date=2026-12-20&adults%5B%5D=2&children%5B%5D=0&view=calendar) returned no itemized checkout in the readable response on November 19. Do not refresh the price or assume free cancellation. |

A seven-night stay at that historical total plus one hypothetical $400 entry would be **$2,769.38 before parking and extras**. That is a sensitivity calculation, not an itinerary. Zero confirmed tournaments means there is no evidence-backed reason to buy that stay for this poker trip. A lower price on different dates or in a different room is not a competing offer.

## Re-read of 2026-11-19 and what it changed

Three Venetian structure sheets (#5, #8, #10) and the Wynn Signature Series structures PDF were opened again today,
field by field, alongside both poker-room pages. **No published value moved**: every compared buy-in, guarantee, fee
split, prize pool, starting stack, level table, registration deadline and payout clause matched, so the seven rows
citing those sheets now carry `last_checked: 2026-11-19` and a note naming what the re-read found, and the 34
Signature Series rows stay unverified because their only possible source is still the document that renders
`LAS VEGAS / POKER / COMING SOON`. Evidence log: `research/verification-2026-11-19-0f038248.md`.

Every table now also carries a **Spend advantage** column, derived from the clause text on the row: 3 rows print a
priced later buy-in, 114 sell further entries during the event, 43 permit another flight unless chips were bagged,
80 have a sheet that was read and print no such clause, 34 have no sheet on file and 43 are continuations. That is
the trip rule made explicit - and the 80 remain candidates, not confirmed freezeouts.

## What changed on November 19 (session dd06081b)

* **The date filter and the trip calculator now answer the two questions the brief asks most often.**
  Every tournament table filters by day (today, tomorrow, this weekend, next 7/30 days, or a tick list of
  the dates this dataset actually holds), and the [calculator](pages/calculator.html) prices the entry
  side from the day plan itself — one round per night at the printed buy-in of that date's published
  primary — with a night-by-night table and a source link per line. The typed entries × buy-in box is
  still there, labelled as the manual alternative.
* **A live re-read of every cited official page on November 19 changed no published value.** Event 12's
  sheet still prints $300 / $10,000 / 40,000 chips / ten clauses with no entry-count limit; Event 10's
  still prints $400 / $15,000 / $65 withheld; the Wynn Signature Series schedule matched all 38 rows on
  every field; the Signature Series *structures* file is still "COMING SOON" in both versions Wynn
  publishes. Details and links: `research/requirements-audit-dd06081b/README.md`.
* **Three irregularities are published for review (F87–F89).** The one that matters to a decision is
  **F89**: the Venetian runs a **DeepStack Showdown from January 11 to February 14, 2027** (59 events,
  $2.2M guaranteed, each row with its own structure sheet) that **this site does not carry**. So for that
  window the tournament tables are incomplete and the Wynn Signature Series is not the only series
  running. It is listed as the top open proposal from this session (P18) because it is gathering, not waiting on anyone.
* **`REQUIREMENTS.md`** now audits the brief line by line — done / partial / blocked, with the file, the
  page and the official source — and states the six things a static site cannot close at all.

## Coverage and review order

317 series rows: **74 reviewed candidates**, **166 possible multiple-entry or re-entry rows**, **43 continuations**, and **34 entry rows without a confirmed entry policy**. The conditional day model spans 70 dates and flags 170 pairs based on starts, registration and published structures. Those are planning conflicts, not verified finish times.

1. Review the [strict shortlist](pages/single-entry.html) before the [conditional schedule](pages/schedule.html).
2. Compare the [dated hotel quotes and route evidence](pages/hotels.html), then use the [trip calculator](pages/calculator.html). Do not add tax or resort fees twice.
3. Check [morning schedule excerpts](pages/daily.html), [changed sources](pages/monitoring.html) and [flagged discrepancies](pages/flagged.html) before any payment. Source availability is not confirmation of a field value.
