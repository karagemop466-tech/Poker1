# Verification log, 2026-11-17 (session 3f878ff5)

Scope of this pass: the official pages and booking engines that bear on the open items in
`QUESTIONS.md` and `FLAGGED.md`. The 37 DeepStack Extravaganza IV sheets, the 15 NYE sheets and
the WPT structures were **not** re-read in this pass; their verification stays as recorded on
2026-11-16 in `research/structure-sheets-verification.md`.

Clock used for "retrieved": the sandbox clock, about 00:30–00:40 UTC on 2026-11-17. Official pages
do not print a time stamp, so the date and approximate time of each fetch are recorded here.

## Official pages read

| # | Official URL | Read on | What it says (quoted or summarised) | Used in the dataset? |
|---|---|---|---|---|
| 1 | [Venetian poker room](https://www.venetianlasvegas.com/resort/casino/poker.html) | 2026-11-17 | "Open 24 Hours"; 50 tables; the page lists the WPT Fall Festival (Oct 28 – Nov 15, 2026) as the current series. Free self-parking for players who play three hours or more. | Confirms the venue facts already on the Venetian page. |
| 2 | [Venetian DeepStack series overview](https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament.html) | 2026-11-17 | Current series WPT Fall Festival (ended Nov 15). Next series "DeepStack Extravaganza IV, November 16 – December 23, 2026", with headline events Dec 3–6 ($800 NLH, $500K GTD), Dec 12–14 ($2,200 NLH, $1M GTD), Dec 13–15 (Seniors $1,100, $300K GTD), Dec 17–20 ($1,100, $500K GTD), Dec 20–23 ($600, $150K GTD). Next: NYE Dec 24 – Jan 10, 2027; DeepStack Showdown Jan 11 – Feb 14, 2027. | Added to `data/sources.json` for monitoring. The per-event rows come from the 2026-11-16 structure reads. |
| 3 | [Wynn poker room](https://www.wynnlasvegas.com/casino/poker) | 2026-11-17 | WPT World Championship Nov 27 – Dec 21; WYNN SIGNATURE SERIES Jan 11–24, 2027; daily tournaments; the daily schedule is suspended during each Wynn Signature, Wynn Millions and Classic series. | Consistent with the existing rows. No change. |
| 4 | [Bellagio poker room](https://bellagio.mgmresorts.com/en/casino/poker.html) | 2026-11-17 | Northside of casino, next to the Sportsbook. Three weekly flyers: Friday $600 NLH, Saturday (label $1,000), Sunday $400 H.O.R.S.E. Notice: "Tournament play will resume on Saturday, July 26" (a Sunday in 2026). Poker host phone 702.693.7291. | Venue note only. No dated rows. See F21–F24. |
| 5 | Bellagio Friday flyer (linked from #4; host assets.contentstack.io, not on the approved list) | 2026-11-17 | $600 NLH, 11:00 a.m.; $510 prize pool, $50 house fee, $40 optional gratuity (+15,000 chips); players "may buy-in and re-enter through the end of level 8". | Re-entry → not single entry. |
| 6 | Bellagio Saturday flyer (linked from #4) | 2026-11-17 | Heading "NLH $1100 BUY-IN"; label and file name $1,000; rule 7 refers to a "$600 Buy-in"; blind cell "200-4300"; flights, each to the money; Day 2 on 9/13/26 printed. | Entry rule not confirmed. Flagged F22. |
| 7 | Bellagio Sunday flyer (linked from #4) | 2026-11-17 (second attempt; first attempt failed) | $400 H.O.R.S.E., 11:00 a.m.; $340 prize pool, $35 house fee, $25 optional gratuity (+15,000 chips); "buy-in and re-enter through the end of level 8". | Re-entry → not single entry. |
| 8 | [ARIA poker room](https://aria.mgmresorts.com/en/casino/poker.html) | 2026-11-17 | 24 tables, next to main valet pick-up; exclusive room rates for qualifying poker players by phone 702.590.7232 or PokerRoomRates@aria.com; Daily Tournaments mentioned but no schedule published. | Venue note only. |
| 9 | [Caesars article "Poker Tournaments in Las Vegas" (dated July 17, 2026)](https://www.caesars.com/las-vegas/explore/casino/poker-tournaments-las-vegas-strip) | 2026-11-17 | Caesars Palace: 16 tables; open 24/7; four NLH tournaments daily at 10 a.m., 2 p.m., 6 p.m., 9 p.m.; $100 buy-in; 20,000 starting chips; $1,000 guarantee; $50 add-on at the first break for 15,000 chips. Horseshoe Las Vegas: six daily NLH games at 9 a.m., 11 a.m., 2 p.m., 5 p.m., 8 p.m., 11 p.m. | Caesars venue note. Add-on → separate section. No rows (editorial). F25. |
| 10 | [Caesars Palace official page](https://www.caesars.com/caesars-palace) | 2026-11-17 | Address 3570 Las Vegas Blvd South, Las Vegas, NV 89109; phone 866-227-5938; no resort fee or room-tax figure on the page read. | Address already verified. Fee stays blank. |
| 11 | [Venetian booking engine, Nov 18–20, 2026, 2 adults](https://www.venetianlasvegas.com/booking?adults[]=2&arrival_date=2026-11-18&children[]=0&departure_date=2026-11-20&view=calendar) | 2026-11-17 | Best available rate, Venetian Newly Remodeled Luxury Two Queen, "Book Direct: Up to 25% Off": Nov 18 room $204.25; Nov 19 room $524.25; resort fee $55.00 on each night; taxes $112.19; total $950.69. The page also prints "Average Rate $419.25". | **Rate log entry added** (`data/rates.json`). |
| 12 | [Wynn reservation page](https://reservations.wynnlasvegas.com/ibe/details.aspx?hotelID=13763&langID=1&rmID=68658&arrival=11/18/2026&departure=11/20/2026&adults=2) | 2026-11-17 | The page ignored the requested dates and priced "1 Night Stay: Nov. 16 – Nov. 17, 2026" ("Flexible Getaway Rate", $1254 avg/night, includes resort fee, excludes taxes). The "Resort Fee Information" block says $55 plus tax per room night. | Not used (wrong dates). Fee already verified. F27. |
| 13 | [Bellagio booking calendar](https://bellagio.mgmresorts.com/book-room/) | 2026-11-17 | "Sorry, there was an error loading calendar dates pricing." | No quote. F27. |
| 14 | [Hotel terms, Venetian](https://www.venetianlasvegas.com/legal/hotel-terms-and-conditions.html) | Read 2026-11-16 (not re-read today) | 13.38% Clark County Room Tax and $55 resort fee. | Unchanged. |

## Checks on the new rate entry (arithmetic)

- Room charges: 204.25 + 524.25 = 728.50.
- Resort fee: 2 nights × 55.00 = 110.00.
- Taxable base: 728.50 + 110.00 = 838.50.
- Tax: 838.50 × 13.38% = 112.19 (matches the page's taxes line).
- Total: 838.50 + 112.19 = 950.69 (matches the page's total).
- Per night, all-in: 950.69 ÷ 2 = 475.345, which rounds to **475.35**.
- "Average Rate" $419.25 = 838.50 ÷ 2, so the printed average includes the resort fee.

## Blocked or not done

- **Bellagio, ARIA and Caesars resort fees and room tax:** not printed on any official page read today. Third-party aggregator pages were found in search results and were **not used**. An MGM "FAQ" page was read in part; it did not state a Bellagio or ARIA fee. A guessed "hotel-policies" path on the MGM properties returned "page not found".
- **Google Maps / Apple Maps walking times:** not checked in this pass (see Q-D8).
- **Wynn and Bellagio rates for the requested dates:** not captured (F27).
- **Structure sheets:** not re-read today.

## Data changes made in this pass

- `scripts/build_data.py`: new `SRC` keys (venetian_dse_series, venetian_quote_1118, bellagio_poker, caesars_poker_article), one new `RATES` entry, updated Venetian hotel room-rate note, updated venue notes for Bellagio, ARIA and Caesars.
- `data/sources.json`: three official pages added to the monitored list (Venetian series overview, Bellagio poker page, Caesars article). Venue label "Other" for the last two.
- Generated: `data/rates.json`, `data/hotels.json`, `data/venues.json`, `data/tournaments.json` (the `sources` block only).
- Documents: `FLAGGED.md` (F21–F30), `QUESTIONS.md` (Q-D1–Q-D9, and I6 updated), `EXECUTIVE_SUMMARY.md`, `README.md`, `COORDINATION.md`.
