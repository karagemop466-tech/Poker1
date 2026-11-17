# Strip-wide poker-room survey, 2026-11-17 (session 88793bf4)

Scope: Strip poker rooms that the venue dataset (`data/tournaments.json`) did not yet cover. The rooms already covered (Venetian, Wynn, ARIA, Bellagio, Caesars Palace) are not re-read here.
Output: `data/strip_rooms.json`, rendered on [pages/strip-rooms.html](../pages/strip-rooms.html). Flags are S1–S10 in `FLAGGED.md` section E.

## 1. Rule applied

- Official values come only from an operator page, an operator PDF, or an operator article. Each one is stored with its excerpt and read date.
- A closure that appears only in the press is stored under `reported_changes` with `official_confirmed: false`. It is never written into an official field.
- A recurring schedule with no calendar date is not turned into dated rows.
- A format that sells extra chips for extra money goes to the separate section, because the brief says to keep those out of the single-entry ranking.
- Third-party listings are read only to find leads. No third-party value is stored.

## 2. Official reads (2026-11-17)

| # | URL | What it says (quoted or summarised) | Used for |
|---|---|---|---|
| 1 | [MGM Grand poker page](https://mgmgrand.mgmresorts.com/en/casino/poker-tables.html) | "Daily: 24 Hours"; contact (702) 891-7434; price range "$100 – No Max"; "Daily Texas Hold'em Tournaments 11:00am, 7:00pm and 11:00pm"; links the weekly schedule PDF and the full structure list PDF. | Room record; S1 |
| 2 | [MGM Grand weekly schedule (PDF)](https://assets.contentstack.io/v3/assets/bltc6ce635bc4868eb2/blt5f25277b8918da08/mgm-grand-casino-poker-tournament_schedule.pdf) | Title "MGM Grand August Tournament Schedule". Starts 11:10am, 7:10pm, 11:10pm. $120 NLH at 7:10pm and 11:10pm every day and at 11:10am Sunday–Friday, 25K chips, 15-minute levels. Saturday 11:10am: "$150 NLH - $2,000", 25K chips, 20-minute levels. Note: players with 5 entries in $120 dailies get a free Saturday $150 entry. | Formats; S1, S2, S6 |
| 3 | [MGM Grand $120 NLH structure (PDF)](https://assets.contentstack.io/v3/assets/bltc6ce635bc4868eb2/bltb2a45da7e8ee5621/mgm-grand-casino-poker-120_nlh.pdf) | 25,000 chips "including the chips for staff gratuity (15,000 + 10,000)". Levels 15 minutes. "Registration is open until Level 8." Fee: "$92 to Prize Pool, $13 House Fee and a onetime, voluntary gratuity of $11 which grants players an extra 10,000 chips. $4 will fund Tournament Promotions." Payout percentages by entry count. Printed metadata title "Max Stacks Tournament Series". No re-entry or single-entry clause. | Formats; S3 |
| 4 | [Mandalay Bay poker page](https://mandalaybay.mgmresorts.com/en/casino/poker-tables.html) | Hours "Wednesday – Monday: 10:00 AM – 4:00 AM"; "Tuesday: Closed"; price range "$60 - $1,000"; contact 702.632.7790; "Please Visit or Call Poker Room for Details". No tournament schedule printed. | Room record; S4 |
| 5 | [Caesars poker article (Caesars Palace and Horseshoe; dated 2026-07-17 on the source)](https://www.caesars.com/las-vegas/explore/casino/poker-tournaments-las-vegas-strip) | Horseshoe: "six daily No-Limit Hold'em games. The times at 9 a.m., 11 a.m., 2 p.m., 5 p.m., 8 p.m. and 11 p.m."; "A mixture of buy-ins, levels and guarantees". Sign-up "usually one hour before the scheduled start". Caesars Palace figures were already in the dataset. | Horseshoe; S5 |
| 6 | [Resorts World casino events](https://www.rwlasvegas.com/gaming/casino-events/) | Lists slot and rewards promotions (Rodeo Roundup, Mystery Point Multiplier, Genting Rewards programs). No poker event. | Closure check; S7 |
| 7 | [Resorts World gaming page](https://www.rwlasvegas.com/gaming/) | Describes table games, slots and Genting Rewards. No poker room or poker event named. | Closure check; S7 |
| 8 | [Planet Hollywood property page](https://www.caesars.com/planet-hollywood) | First of three sections read: hotel offers and packages. No poker room in the sections read. | Closure check; S8 |

### Arithmetic and internal checks

- MGM $120 fee split: 92 + 13 + 11 + 4 = 120. Matches the buy-in.
- MGM $120 starting stack: 25,000 with the gratuity, 15,000 without. 25,000 ÷ 15,000 = 1.67, so the gratuity buys a 67% larger starting stack.
- MGM start-time conflict: the page (11:00 / 7:00 / 11:00) and the PDF (11:10 / 7:10 / 11:10) differ by ten minutes at each start. The rows use the PDF, and S1 records both.
- Start-time parse check: `data/strip_rooms.json` times are all HH:MM, and `scripts/check_links.py` now validates every time, number and source host in the file.

## 3. Press reports used only as closure leads (not confirmed on official pages)

| Report | Claim | Official confirmation found |
|---|---|---|
| [Casino.org, 13 Mar 2026](https://www.casino.org/vitalvegas/resorts-world-confirms-closure-of-poker-room/) | Resorts World poker room closes 30 March 2026; a representative is quoted: "We can confirm that the poker room will close on March 30." Also lists the Strip rooms still open at that date: Aria, Bellagio, Caesars Palace, Horseshoe, Mandalay Bay, MGM Grand, Venetian, Wynn. | No. The Resorts World pages read (item 6, 7) do not mention poker. |
| [Las Vegas Review-Journal, 28 Jan 2026](https://www.reviewjournal.com/business/casinos-gaming/inside-gaming-strip-casino-to-close-poker-room-3612434/) | Planet Hollywood poker room stops after 31 January 2026; Caesars statement: "This consolidation is designed to better match current demand and enhance the player experience." | No. The Caesars property page read (item 8) does not list a poker room in the sections read. |

## 4. Third-party listings checked for leads only (not used as values)

These gave the leads that the official pages then confirmed or contradicted.

- [PokerAtlas: MGM Grand tournaments](https://www.pokeratlas.com/poker-room/mgm-grand-las-vegas/tournaments): shows 11:10am / 7:10pm / 11:10pm $120 NL. Matches the official PDF.
- [MTT DB: Mandalay Bay](https://mttdb.com/live-poker/venues/mandalay-bay-las-vegas/) and [PokerDiscover: Mandalay Bay](https://pokerdiscover.com/clubs/united-states/las-vegas/mandalay-bay): show daily $60 and $100 NLH with re-entry. Not on the official page, so not used (S4).
- [PokerAtlas: Resorts World](https://www.pokeratlas.com/poker-room/resorts-world-las-vegas/tournaments): says Resorts World "does not currently run any poker tournaments". Consistent with the closure report, but not an official source.

## 5. What is not verified

- Horseshoe's buy-ins, guarantees, structures and entry rules (S5).
- The MGM Saturday $150 event's structure and entry rule (S6).
- Whether the MGM Grand schedule shown is the current one (S2).
- Whether Resorts World and Planet Hollywood are closed on an official page (S7, S8).
- Any room not listed in section 2 (S10).
- Walking times and hotel fees for MGM Grand, Horseshoe and Mandalay Bay. These are not in `data/hotels.json` or `data/walking.json` and are not added here.

## 6. Effect on the 8 AM goal

- No Strip room in this survey starts a verified single-entry event before 9:00 AM. Horseshoe's first daily session is at 9:00 AM per the Caesars article, but no buy-in or entry rule is printed for it.
- MGM Grand's earliest daily start is 11:10 AM.
- Mandalay Bay publishes no schedule, so it cannot be used for an 8 AM plan.
