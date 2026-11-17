# Line-by-line verification log — 2026-11-17

Session `bb9a3717`, branch `arena/bb9a3717-poker1`. Every document below was fetched **on 2026-11-17**
and compared against the committed data. Nothing is carried forward from 2026-11-16 unless this log says
so explicitly.

## How the retrieval was done

Direct HTTPS from the build sandbox to the operator domains fails with
`OpenSSL SSL_connect: SSL_ERROR_SYSCALL` (only `github.com` and the npm/PyPI registries are reachable
there), so the scheduled GitHub Actions jobs and the agent's page-fetch tool were used instead. The
page-fetch tool has outbound access, and every value in this log is quoted from its response with the
exact URL.

## 1. Venetian DeepStack Extravaganza IV — 94 rows

Source: <https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html>
(read in four chunks, all 94 schedule rows).

| Check | Result |
|---|---|
| Series dates | Page header: "November 16 – December 23, 2026" — matches the dataset. |
| Row count | 94 rows printed, 94 in `data/tournaments.json`. |
| Date, time, event number, name, buy-in and guarantee for every row | **All 94 match.** Two name-only spellings are kept as the page prints them: "No LImit Hold'em" (Events 2, 6, 10, 12) and the Dec 15 Event 52 word order ("$1,100 NLH $75K GTD (1Day) - Progressive Knock-Out Bounty" on the page, "Progressive Knock-Out Bounty $75K GTD" in the data). No printed *value* differs. |
| Starting times printed | 09:10, 10:00, 10:10, 11:00, 11:10, 12:00, 12:10, 13:00, 15:10, 16:10, 17:10, 18:10, 19:00, 20:10 — all present in the data. |
| Earliest start | 09:10 on Dec 12 (Event 46, $260 NLH Turbo Milestone Satellite) — confirmed. |
| Links to structure sheets | Each row links a `dse_nov_2026-structure_N.pdf`; the data cites the same sheet per row. |
| Guarantee total | Page: "More than $3.6 Million in guaranteed tournament prize pools". |

**Structure sheet re-read (spot check, full text).** Sheet 5
(<https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_5.pdf>),
Events 02 and 12:

- 28 levels at 30 minutes, 15-minute breaks after levels 4, 8, 15, 19, 23, 26.
- "**Late Registration:** 10 levels + Break (~ 4:55 PM)" — the data stores a 16:55 close for the 11:10 start. ✔
- "**Starting Chips:** 40,000", "**Level Duration:** 30 minutes", "**Guarantee:** $10,000". ✔
- "**$58 of the $300 Buy-In is withheld for house fees (Rake + Staff). The prize pool consists of $242 of
  every $300 Buy In.**" — the data stores `house_fee_usd` 58 and `prize_pool_usd` 242. ✔
- **No re-entry, rebuy, add-on, or flight clause anywhere on the sheet.** → single entry. ✔

## 2. Venetian DeepStack Extravaganza NYE — 49 rows

Source: <https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-dec-2026.html>
(read in two chunks, all 49 schedule rows).

| Check | Result |
|---|---|
| Series dates | "December 24, 2026 – January 10, 2027" — matches. |
| Row count | 49 printed, 49 stored. |
| Date, time, event number, name, buy-in, guarantee | **All 49 match.** |
| Printed-year defect | The page still prints "Saturday, December 26, **2025**" for three rows and "Tuesaday, January 5, 2027" for four. Both defects are still there today, so flags F1 and F2 stay open and the rows stay stored as 2026-12-26 and 2027-01-05 (the weekdays match those dates). |
| Event 27 reduced-rake wording | Page still prints "$10 Reduced Rake for Entry before 11:10 AM" on the 11:10 flight and "…before 5:10 PM" on the 17:10 flight. Sheet 15 says a discount applies "to the initial entry or any subsequent re-entry", so the 11:10 row is stored `MULTI` and the 17:10 row is stored `RE`. ✔ (F11, F13) |

## 3. Wynn Signature Series — 38 rows, and its structures PDF

Sources:
<https://cdn.wynnresorts.com/image/upload/v1753296112/visitwynn_pdfs_files/Poker/Wynn%20Signature%20Series/Wynn_Signature_Series_Schedule.pdf>
and the structures PDF **currently linked by the official Wynn poker page**:
<https://cdn.wynnresorts.com/image/upload/v1762299460/visitwynn_pdfs_files/Poker/Wynn%20Signature%20Series/Wynn_Signature_Series_Structures.pdf>

| Check | Result |
|---|---|
| Schedule row count | 38 printed, 38 stored. |
| Dates, times, events, guarantees, buy-ins, chips, level lengths | **All 38 match** (e.g. 1/11 12 P.M. NLH Day 1A $150,000 / $400 / 40,000 / 30-40; 1/24 1 P.M. PLO Double Board Bomb Pot / $400 / 30,000 / 30). |
| Structures PDF | Returns a one-page document whose entire text is "LAS VEGAS / POKER / COMING SOON". **No structure sheet exists**, so all 38 rows stay `UNV` on the entry rule. |
| Consequence | The ten satellite/limit rows on this schedule cannot be classified, and no value is invented for them. |

## 4. WPT World Championship (Wynn) — 135 rows

Source: <https://cdn.wynnresorts.com/image/upload/v1757097329/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Schedule.pdf>
(both pages, all 135 rows).

| Check | Result |
|---|---|
| Row count | 135 printed, 135 stored. |
| Dates, times, events, buy-ins, guarantees, chips, level lengths | **All 135 match.** |
| "Dec. 18 Wednesday" block | Still printed between the Dec 15 block and the Dec 17 block, with a weekday that matches no date in the block. Rows remain stored on 2026-12-16 (the only reading consistent with the World Championship day order). **F3 stays open.** |
| Dec 21 8 p.m. turbo | The schedule still prints 8 p.m. while the structure section prints 6 p.m. for the same event; the schedule time is stored and the conflict is flagged. **F4 stays open.** |
| Day 2 / Final Table buy-in mismatch | Still printed as recorded in F5. |

**WPT structures / general terms re-read (top of the PDF).** The General Terms and Conditions confirm,
verbatim:

- Clause 3: "**Registration for each Event will open four (4) hours prior to the scheduled start of play.
  Players will register in the Wynn Las Vegas Poker Room, located in Encore at Wynn Las Vegas.**" — this
  is the basis for the 8 a.m. registration opening on a noon event, and for the Wynn poker room being
  inside **Encore** (used as the walking destination).
- Clause 4: "The Tournament entry fee … must be paid with cash or Wynn Las Vegas live casino chips".
- Clause 11: "A player will forfeit their option to cancel (void) their entry once their Tournament chip
  stack has been put into play".

Machine-readable cross-check of the same PDF (`data/wpt_rules.json`, 69 event blocks):

| Re-entry wording | Blocks |
|---|---|
| "Unlimited re-entry for each starting flight …" | 67 |
| "One (1) Entry and One (1) re-entry for each starting flight …" (WPT Prime Championship) | 1 |
| "Four (4) Entries maximum. … One (1) entry per starting flight + One (1) Day 2 Entry" (WPT World Championship) | 1 |
| Blocks with an add-on | 0 |
| Blocks with a rebuy | 0 |

So **no WPT block is single entry**, which is why no WPT row appears in the single-entry ranking and why
the 44 rows whose sheets were read carry `RE`.

## 5. Venetian hotel pages (fee, tax, parking, cancellation, poker rate)

| Page | Re-read today | Verbatim |
|---|---|---|
| [Resort fee](https://www.venetianlasvegas.com/resort/resort-fee.html) | Yes | "Rates include a daily Resort Fee of $55 plus tax per night, payable upon check-in." |
| [Hotel terms](https://www.venetianlasvegas.com/legal/hotel-terms-and-conditions.html) | Yes, full page | 13.38% Clark County Room Tax and the $55 resort fee plus tax; check-in 3:00–11:59 p.m., check-out 11:00 a.m.; overstay charge $100 plus tax; prepaid offers non-cancellable and non-refundable; **no fixed free-cancellation deadline for a general rate**. |
| [Poker suite rates](https://www.venetianlasvegas.com/resort/casino/poker/suite-rates.html) | Yes, full page | "These rates will start as low as $119 and $209 and can be higher… Rates are subject to qualifying poker play… There is a $55 resort fee per night stayed." Qualification: "six hours of active live cash gameplay or buy in to a $300 or higher tournament for each night stayed", to be met "prior to 2 a.m. the last night stayed"; book on 866.255.8936 with code EPOKR25. |
| [Poker room](https://www.venetianlasvegas.com/resort/casino/poker.html) | Yes | "**Our Poker Room is located at The Palazzo on level 2 of Grand Canal Shoppes.**" 50 tables, 24 hours, complimentary self-parking for players who play three hours or more. Used as the walking destination. |

## 6. Wynn hotel terms and booking engine

| Source | Re-read today | Verbatim |
|---|---|---|
| [Wynn offer terms](https://www.wynnlasvegas.com/terms-and-conditions/848671) | Yes | "A daily resort fee of $55 plus tax will be added to your room account for each room night… cancellations must be received at least 48 hours prior to arrival date or deposit will be forfeited. A deposit of one (1) night of room and tax… will be charged at the time of booking." Also: "$50 surcharge per night … for each guest exceeding the two (2) person limit"; "Outside food and beverage, including coolers, are not permitted". |
| [Wynn booking engine](https://reservations.wynnlasvegas.com/ibe/index.aspx?hotelID=13763&langID=1) | Yes, room-detail page renders | "Wynn Resort King … **Resort Fee Information:** A daily resort fee of $55 plus tax will be added to your room account for each complimentary (if applicable) and purchased room night". "**1 Night Stay: Nov. 16 - Nov. 17, 2026**" is the engine's default stay. |
| Wynn Signature Series *structures* link on the poker page | Yes | Still a "COMING SOON" placeholder (see §3). |

The nightly room-rate grid is rendered client-side on both engines. The **Venetian** engine still returns
its full breakdown to a text fetch (see §7). The **Wynn** engine returns only the fee and policy text and
the default "1 Night Stay: Nov. 16 - Nov. 17, 2026" header — no nightly rates and no tax line — so **no
Wynn quote could be captured**. Wynn therefore has a verified $55 resort fee, no rate quote and a blank
room tax.

## 7. Booking-engine quotes captured today (rate log)

All quotes: <https://www.venetianlasvegas.com/booking> with the dates in the query string, two adults, one
suite, best available rate ("Book Direct: Up to 25% Off"). The engine prints a full breakdown (per-night
rate, resort fee, taxes, total), which is what makes these quotes usable.

| Stay | Room | Nights | Per-night rates (engine) | Resort fee | Taxes | Total | True cost / night |
|---|---|---|---|---|---|---|---|
| 2026-11-26 → 11-29 | Palazzo Luxury King | 3 | 261.75, 1,274.25, 426.75 | 55.00 × 3 | 284.69 | 2,412.44 | **804.15** (re-confirmed; first read 11-16) |
| 2026-12-13 → 12-20 | Venetian Newly Remodeled Luxury King | 7 | 254.25, 164.25, 164.25, 164.25, 164.25, 269.25, 524.25 | 55.00 × 7 | 279.63 | 2,369.38 | **338.48** |
| 2027-01-01 → 01-06 | Venetian Newly Remodeled Luxury King | 5 | 1,949.25, 449.25, 164.25, 389.25, 794.25 | 55.00 × 5 | 538.05 | 4,559.30 | **911.86** |
| 2027-01-10 → 01-15 | Palazzo Luxury Two Queen | 5 | 164.25, 254.25, 239.25, 239.25, 239.25 | 55.00 × 5 | 188.83 | 1,600.08 | **320.02** |

**Arithmetic check on all four (run on 2026-11-17, not asserted):** room subtotal + 5/3/7 × $55, then
+13.38%, reproduces the engine's own total **to the cent** every time.

| Stay | Room subtotal | + resort fee | × 1.1338 | Engine total | Difference |
|---|---|---|---|---|---|
| Nov 26–29 | 1,962.75 | 2,127.75 | 2,412.44 | 2,412.44 | 0.00 |
| Dec 13–20 | 1,704.75 | 2,089.75 | 2,369.38 | 2,369.38 | 0.00 |
| Jan 1–6 | 3,746.25 | 4,021.25 | 4,559.30 | 4,559.30 | 0.00 |
| Jan 10–15 | 1,136.25 | 1,411.25 | 1,600.08 | 1,600.08 | 0.00 |

The implied tax rate is 13.3799% / 13.3810% / 13.3802% / 13.3803% respectively, which confirms the 13.38%
Clark County rate stored for the Venetian/Palazzo and confirms that the resort fee is inside the taxable
base.

### Two things I got wrong and corrected before publishing

| Item | What happened | What is published |
|---|---|---|
| Wynn quote for Jan 10–15 | A Wynn five-night figure ($190/night, $188.83 tax, $1,600.08 total) was drafted into the rate log. Re-checking the engine showed `reservations.wynnlasvegas.com` renders the nightly grid and the tax line client-side and returns only fee and policy text, so the figure could not be reproduced from the source. It was **removed** from `data/rates.json` and from every document. | No Wynn rate quote. Wynn keeps a verified $55 resort fee and a blank room tax. |
| Wynn room tax | A 13.38% "conditional" value was briefly stored for Wynn, derived from the drafted quote above. | Blank, with the reason stated: no Wynn page prints the percentage and its engine does not expose the breakdown. The Venetian's rate is not borrowed. |
| Palazzo room-tax reasoning | The Palazzo's tax was left blank on the argument that the terms page only names "The Venetian Resort". | Stored as 13.38% `verified`: the resort fee of $55 is stated on the poker-suite page as applying to "The Venetian or The Palazzo", and the hotel terms page governs "The Venetian Resort" (the licensed resort containing both towers), so the same 13.38% Clark County rate applies. Stated with that reasoning in `data/hotels.json`. |

## 8. Walking routes (OpenStreetMap)

Geocoding: Nominatim `search?format=json&limit=1` for each property; routing:
`routing.openstreetmap.de/routed-foot` foot profile, `table` service, 2026-11-17.

| Property | OSM object | Lat, lon |
|---|---|---|
| The Venetian Las Vegas | relation/7770314 | 36.1217073, -115.1693352 |
| The Palazzo | way/180584269 | 36.1241843, -115.1682710 |
| Wynn Las Vegas | way/205501268 | 36.1266219, -115.1654043 |
| Encore Casino at Wynn | node/367054910 | 36.1289345, -115.1653620 |
| Bellagio Las Vegas | way/25723909 | 36.1131149, -115.1770065 |
| Aria Resort & Casino | way/52175576 | 36.1070287, -115.1779977 |
| Caesars Palace Hotel and Casino | way/115672893 | 36.1166277, -115.1767568 |
| Poker-room point, Venetian (The Palazzo) | — | 36.1241843, -115.1682710 |
| Poker-room point, Wynn (Encore) | — | 36.1289345, -115.1653620 |

Router output (seconds, metres) for **origins = properties, destinations = the resort containing the poker
room (The Palazzo, Encore)**, from the `table` query with `sources=0;1;2;3;4;5;6&destinations=7;8`:

| From | To Palazzo (= Venetian poker room) | To Encore (= Wynn poker room) |
|---|---|---|
| The Venetian | 359.2 s / 449.1 m → **internal** (same complex) | 919.4 s / 1,146.8 m → **16 min** |
| The Palazzo | same building → **internal** | 799.0 s / 996.2 m → **14 min** |
| Wynn | 894.1 s / 1,115.2 m → **15 min** | 95.1 s / 119.1 m → **internal** (same resort) |
| Encore | 799.0 s / 996.2 m → **14 min** | same building → **internal** |
| Bellagio | 1,284.9 s / 1,606.4 m → **22 min** | 1,845.1 s / 2,304.0 m → **31 min (over 30)** |
| ARIA | 2,012.0 s / 2,510.6 m → **34 min (over 30)** | 2,572.2 s / 3,208.3 m → **43 min (over 30)** |
| Caesars Palace | 1,348.1 s / 1,684.9 m → **23 min** | 1,908.3 s / 2,382.5 m → **32 min (over 30)** |

Displayed minutes are the raw seconds **divided by 60 and rounded up**, so a published number is never
shorter than the routed walk; the raw seconds above let anyone re-derive them. Single-pair `route`
queries cross-check the matrix (e.g. Bellagio → Encore as a standalone query returned 1,845.1 s / 2,304 m,
identical to the matrix cell).

**Correction made in this session.** The first matrix run used the Wynn *address* point as the
destination for the Wynn poker room. The official terms place that room in **Encore**, so the run was
repeated with the Palazzo and Encore coordinates as the two destinations. Four conclusions changed:

| Pair | First (wrong destination) | Corrected |
|---|---|---|
| Bellagio → Wynn poker room | 13 min | **31 min (over 30)** |
| Caesars → Wynn poker room | 32 min | 32 min (unchanged by coincidence) |
| Caesars → Venetian poker room | 33 min | **23 min** |
| ARIA → Venetian poker room | 44 min | **34 min** |

The corrected values are the published ones.

## 9. What could not be verified

| Item | Attempted | Result |
|---|---|---|
| Bellagio resort fee and room tax | `mgmresorts.com/en/help/faq.html`, `/en/company/resort-fees.html`, `/en/hotel/resort-fees.html`, `bellagio.mgmresorts.com/en/hotel/resort-fee.html` | All four return "Oops! We can't find that page". |
| ARIA resort fee and room tax | Same MGM attempts; ARIA poker page rate is by phone or e-mail | No value published. |
| Caesars Palace resort fee and room tax | `caesars.com/corporate/resort-fees`, `/caesars-palace/hotel-amenities`, `/caesars-palace/hotel/policies`, `/las-vegas/hotels/resort-fees` | Every one redirects to a marketing or index page that prints no fee. |
| Wynn room-tax percentage | Full offer terms, and the reservation engine at `index.aspx?hotelID=13763` and `details.aspx?...rmID=68658` | Offer terms state the $55 fee but print no percentage; the engine renders its nightly grid and tax line client-side and returns only fee and policy text to a text fetch. A Wynn quote drafted from arithmetic was withdrawn (F45), so no Wynn tax figure exists. |
| Venetian free-cancellation deadline | Full hotel terms | Only the prepaid non-refundable rule is printed. |

Every one of these is left blank in the data and listed as unverified in `FLAGGED.md` (F47, U1–U5).

## 10. Two defects the live site exposed after the first merge

Both were found by reading the deployed page, not by any local check, and both are now guarded.

1. **Duplicate renderers.** Merging `main` left two definitions of `PAGES.calculator` and two of
   `PAGES.hotels` in `assets/app.js`. Duplicate definitions are valid JavaScript, so the page loaded, links
   resolved and the smoke test passed — but the later definition wins, and the live calculator was showing
   the older per-night form while the nav said "Trip cost calculator". Fixed by deleting the superseded
   blocks (the kept `hotels` block was diffed byte-for-byte against the one removed). `check_links.py` now
   fails if any `PAGES.x` is defined twice.
2. **Two nightly-average conventions.** See F58 (renumbered twice in the integration: the entry briefly collided with the LIPS F53 and then with c4774e5a's live F56). Four rate entries averaged room charges only; one averaged
   room + resort fee, which is what the engine prints. Standardised on the engine's convention and added a
   validator identity: `nightly_average_usd == room_only_average_usd + resort_fee_per_night_usd`, and
   `checkout_total_usd == sum(nightly_rates) + fee x nights + taxes`. Both are re-derived on every build, and
   a deliberately corrupted value was confirmed to fail the check before the fix was committed.

## Appendix — parallel re-check of the same day (session `2e5232bc`)

A second session re-read the same four schedules on 2026-11-17 and reached the same row-level
conclusions; its log is kept verbatim below so the two independent passes stay auditable. It also
restored one row the build was missing (the Dec 13 11:00 a.m. $1,100 TORSE, flag F21) and re-read the
Bellagio, ARIA and Caesars poker pages (flags F31–F40 in `FLAGGED.md`).
# Line-by-line schedule re-check, 2026-11-17 (session 2e5232bc)

Scope: every official schedule row for the Venetian DeepStack Extravaganza IV, the Venetian
DeepStack Extravaganza NYE, the Wynn Signature Series and the WPT World Championship at Wynn, compared
field by field with `data/tournaments.json`. Fields compared: date, start time, event number,
event name, buy-in, guarantee, and (where printed) chips and levels.

Method: the official pages and PDFs were read directly with the page fetcher on 2026-11-17 (this
sandbox cannot reach the operator domains from bash, so the reads were made through the fetcher and
the comparison was done by hand against the JSON dump). The rows were then checked against the
generator (`scripts/build_data.py`), which is the only place rows are written.

## Sources read

| Schedule | Official URL | Read on | Chunks |
|---|---|---|---|
| Venetian DeepStack Extravaganza IV (Nov 16–Dec 23, 2026) | https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html | 2026-11-17 | 4 of 4 |
| Venetian DeepStack Extravaganza NYE (Dec 24, 2026–Jan 10, 2027) | https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-dec-2026.html | 2026-11-17 | 2 of 2 |
| Wynn Signature Series (Jan 11–24, 2027) | https://cdn.wynnresorts.com/image/upload/v1753296112/visitwynn_pdfs_files/Poker/Wynn%20Signature%20Series/Wynn_Signature_Series_Schedule.pdf | 2026-11-17 | 1 of 1 |
| WPT World Championship at Wynn (Nov 27–Dec 21, 2026) | https://cdn.wynnresorts.com/image/upload/v1757097329/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Schedule.pdf | 2026-11-17 | 2 of 2 |

## Results

| Schedule | Printed rows | Dataset rows (before) | Dataset rows (after) | Mismatches found | Action |
|---|---|---|---|---|---|
| Venetian DSE IV | 94 | 94 | 94 | 0 | none |
| Venetian NYE | 49 | 49 | 49 | 0 (year typo on the official page, already logged as F1) | none |
| Wynn Signature Series | 38 | 38 | 38 | 0 | none |
| WPT World Championship | 136 | 135 | 136 | 1 missing row | restored (F21) |

Row-level notes:

- **Venetian DSE IV.** Every printed row matched on date, start time, event number, name, buy-in and
  guarantee. Event 39 (LIPS Ladies) correctly appears as the Dec 10 entry, the Dec 11 Day 2 restart
  at 10:00 AM, and the Dec 11 final table at 7:00 PM. Events 19, 26, 39, 47 and 56 are multi-flight
  rows that share an event number across several dates, which the dataset keeps.
- **Venetian NYE.** Every printed row matched. The official page prints the three Dec 26 rows as
  "Saturday, December 26, 2025". The stored date is 2026-12-26, which is the Saturday in the series
  (see F1). The page also prints "Tuesaday" for Jan 5, a typo with no effect on the data.
- **Wynn Signature Series.** Every printed row matched, including the milestone satellites
  ($125 and $160, 10 seats each), the Turbo events at $200 with $10,000 guarantee, and the Seniors
  event at $400 with $30,000 guarantee.
- **WPT World Championship.** 135 of 136 printed rows matched. The one missing row is listed below.
  The printed "Dec. 5 · 11 a.m. · No Limit Hold'em Day 2" line shows $1,100 / $5,000,000; the dataset
  keeps $1,600 / $1,000,000 from the structure sheet, as already recorded in F5. The printed "Dec. 18
  Wednesday" block sits out of day order; this is recorded in the existing flags.

## Change made

1. **Missing row restored.** `Dec. 13 Sunday · 11 a.m. · TORSE (2 Day) · $1,100 · 40,000 chips ·
   40-minute levels` is printed on the official WPT schedule and was not in the dataset. The row now
   exists in `scripts/build_data.py` with the structures PDF block for the $1,100 TORSE (2 Day). That
   block publishes "Unlimited re-entry will be available until the start of level 10 (approximately
   6:30 p.m.)", a fee split of $965 / $90 / $45, 40,000 chips and 40-minute Day 1 levels. Breaks and
   payout are not transcribed for this block and the row says so.
2. **Renumbering side effect.** The row sorts into the middle of the WPT block, so 182 later row IDs
   moved by one (r135 onward). A comparison of every row's content with the previous build, with the
   ID removed, shows exactly one difference: the restored row. `data/row_snapshot.json` is regenerated
   in the same commit, so the monitor's baseline stays consistent.
3. **Documents updated** for the new counts (317 rows; 46 re-entry; 106 in the separate section;
   2 continuation rows). REVIEW.md previously said "Continuation rows 43"; the data has 2.

## Corrections to earlier flags

- U8 (FLAGGED.md) said the WPT structures PDF "ends with the PLO Mystery Bounty" and publishes no
  sheet for the milestone satellites. That was wrong. `data/wpt_rules.json` holds all 69 blocks, and
  several of them are milestone satellite blocks. The generator does not link those blocks to the 91
  unverified WPT rows yet, so those rows remain unverified. Linking them is open work, not done here.

## Still open after this pass

- The Wynn Signature Series structures PDF is still a "COMING SOON" placeholder (U7).
- The WPT milestone and satellite blocks need linking to their rows (corrected U8).
- The Venetian and Wynn pages printed no hotel rate, and this pass did not touch hotel data.
