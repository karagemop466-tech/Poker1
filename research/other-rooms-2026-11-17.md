# Other Las Vegas poker rooms — verification log, 2026-11-17

Session `0d069ce0`, branch `arena/0d069ce0-poker1`.

## Why this file exists

The dataset covered two poker rooms: the Venetian/Palazzo and Wynn/Encore. The brief asks for
live upcoming tournaments "near the Las Vegas Strip or around the strip area", so every other
candidate room was checked against its own website. This file records what was read, what each
official page prints, and what was left blank because no official source states it.

Rules used, identical to the rest of the site:

1. A row is published only where an official page or an official PDF prints the value.
2. A value that cannot be confirmed from an official source is left blank and flagged.
3. Third-party schedules were found for several rooms. None of them is used.
4. "No poker room published" means the property's own casino page lists none. It is weaker
   evidence than a printed statement and is worded as such everywhere.
5. Where the operator publishes a schedule as images with no text layer, nothing is
   transcribed and the gap is recorded instead.

## Retrieval method

`fetch_page` was used for every page and PDF below, because this sandbox's shell cannot reach
the operator domains. PDFs were read in full: the Orleans schedule was read across all four
chunks, and both MGM PDFs were read end to end.

---

## 1. MGM Grand — schedule and one structure sheet, both in text

| Source | URL | What it printed |
|---|---|---|
| Official poker page | https://mgmgrand.mgmresorts.com/en/casino/poker-tables.html | "Known for the deepest $1-$3 No Limit Hold 'Em action in Las Vegas, the MGM Grand Poker Room is the Strip's #1 hotspot for Texas Hold'em." · "Hours of Operation — Daily: 24 Hours" · "Contact (702) 891-7434" · "Price Range $100 – No Max" · "Daily Texas Hold'em Tournaments — 11:00am, 7:00pm and 11:00pm" · "Must be 21 or older to play. Must have an MGM Rewards card to play in the tournament. Must present valid ID to be paid." |
| Weekly schedule PDF (linked from the page, "Weekly Schedule") | https://assets.contentstack.io/v3/assets/bltc6ce635bc4868eb2/blt5f25277b8918da08/mgm-grand-casino-poker-tournament_schedule.pdf | Heading "MGM Grand August Tournament Schedule". Grid: 11:10am $120 NLH 25K chips / 15 min (Mon–Fri, Sun); 11:10am Saturday $150 NLH - $2,000, 25K chips / 20 min; 7:10pm $120 NLH 25K / 15 min daily; 11:10pm $120 NLH 25K / 15 min daily. Footnote: "Sunday through Friday - Players with 5 entries or more in $120 Daily Tournaments will receive one (1) free entry to the Saturday $150 NLH $2,000 Guarantee". |
| Structure sheet (linked from the page, "Full Structure List") | https://assets.contentstack.io/v3/assets/bltc6ce635bc4868eb2/bltb2a45da7e8ee5621/mgm-grand-casino-poker-120_nlh.pdf | $120 NLH, 22 levels, BB ante. "Players start with 25,000 tournament chips, including the chips for staff gratuity. (15,000 + 10,000)" · "All levels are 15 minutes in length. There will be a break after levels 7 and 15. Registration is open until Level 8." · "Each initial $120 buy-in is allocated as follows: $92 to Prize Pool, $13 House Fee and a one-time, voluntary gratuity of $11 which grants players an extra 10,000 chips. $4 will fund Tournament Promotions." · "***The voluntary staff gratuity will grant players an extra 10,000 chips. This is an optional gratuity paid to staff and will not be kept by the house***" · "Approximately 1 in 7 entries will be 'in the money'. Winners will be paid in casino chips." · "All Daily tournaments are governed by TDA rules." · payout table by entry count. |
| MGM Resorts poker hub (which MGM properties have poker) | https://www.mgmresorts.com/en/casino/poker.html | Lists Bellagio, ARIA, MGM Grand, Mandalay Bay, Luxor, Excalibur (plus non-Vegas properties). |

**Arithmetic check.** 92 + 13 + 11 + 4 = 120. The printed fee split accounts for the whole
buy-in.

**Entry-rule verdict.** The sheet read end to end contains no re-entry, rebuy or add-on clause.
It does print a paid chip advantage, so under the brief's own rule ("tournaments where you could
gain an advantage through spending more money, keep those in a separate section") the $120
dailies are stored as `PAID_CHIPS` and kept out of the single-entry list. Flag **F62**.

---

## 2. The Orleans — a full daily schedule with a structure sheet for every event

| Source | URL | What it printed |
|---|---|---|
| Official poker room page | https://orleans.boydgaming.com/play/poker-room | "this comfortable 35-table room has been enhanced with state-of-the-art furnishings and 25 LED TV's" · "The Orleans Poker Room is open daily 24 hours and features Texas Hold'Em, Omaha Hi-Lo and 7-Card Stud." · links the "2026 Orleans Poker Daily Schedule" PDF. |
| 2026 Orleans Poker Daily Schedule (official PDF, 4 chunks) | https://orleans.boydgaming.com/-/media/project/boyd/property/lasvegas/orleans/pdf/2026_orleans_october_poker_daily_tournaments_schedule_ada.pdf?rev=6a96aa7ef9fc428bb65c06f9e4d554b0 | Weekday grid (11:05am / 4:05pm / 6:05pm) plus a structure sheet for each of the thirteen events. "$160,000 in GUARANTEED PRIZE POOLS EVERY WEEK!" · "Registration begins 1 hour prior to the start of each tournament." · "Valid I.D. and player's card are required." · "Late entries / re-entries available based on the rules and structures of each tournament." · phone 702-365-7150. |

**Every one of the thirteen structure sheets prints a re-entry clause.** The wording is
identical apart from the level number and the clock time:

- $100 AM Super Stack (Mon–Thu 11:05) — "Late entries and re-entries are available until the
  start of Level 9, approximately 2:10pm." · $23 withheld. 25,000 chips, 20-minute levels,
  $4,000 guarantee.
- $120 PM Monster Stack (Mon–Thu, Sat 18:05) — "until the start of Level 9, approximately
  9:10pm." · $24 withheld. 30,000 chips, 20-minute levels, $5,000 guarantee.
- $150 Friday Monster Stack *RING EVENT* (Fri 11:05) — "until the start of Level 12,
  approximately 5:30pm." · $30 withheld. 30,000 chips, 30-minute levels, $10,000 guarantee.
- $200 Saturday Mega Stack *RING EVENT* (Sat 11:05) — "until the start of Level 12,
  approximately 5:30pm." · $35 withheld. 40,000 chips, 30-minute levels, $15,000 guarantee.
- $200 Sunday Special *RING EVENT* (Sun 11:05) — "until the start of Level 12, approximately
  5:30pm." · $52 withheld · **and** "One-Time Add-On: $100 = 25,000 Chips", "Add-on is optional
  and may be taken before any hand and prior to the end of level 11 unless registering during
  the dinner break. The add-on then must be taken while registering. Players may only add-on
  once per entry." · "All add-ons will be added directly to the prize pool with no fees
  withheld." 25,000 chips, 30-minute levels, $50,000 guarantee.
- $150 Friday Night 20K Monster Stack *RING EVENT* (Fri 18:05) — "until the start of Level 11,
  approximately 9:50pm." · $30 withheld. 30,000 chips, 20-minute levels (30-minute in the
  money), $20,000 guarantee.
- $200 Pot-Limit Big-O (Sun 18:05) — "until the start of Level 11, approximately 9:50pm." ·
  $35 withheld. 25,000 chips, 20-minute levels, $4,000 guarantee.
- $160 mixed games at 16:05 — T.O.E. (Mon, $3,000), T.O.R.S.E. (Tue, $3,000), Drama Mix
  (Wed, $4,000), 5 Game Draw (Thu, $3,000), O/E (Fri, $4,000), Triple-Triple Draw (Sat,
  $3,000) — each "until the start of Level 11, approximately 7:50pm." · $31 withheld. 25,000
  chips, 20-minute levels.

**Entry-rule verdict.** Thirteen of thirteen events permit re-entry, and one of them also sells
an add-on. No Orleans daily event is single entry. Flag **F67**.

**Note on the file name.** The PDF is named `..._october_...` while the page links it as the
"2026 Orleans Poker Daily Schedule", and nothing inside it prints a month, a year or a date
range. The grid is therefore stored as a recurring weekday schedule with no dates. Flag
**F65**. The PDF's own footer points at
`https://www.orleanscasino.com/play/casino-games/poker-room`, which returns "Not Found" on
2026-11-17. Flag **F66**.

---

## 3. South Point — schedule published as images only

| Source | URL | What it printed |
|---|---|---|
| Official poker room page | https://southpointcasino.com/casino/poker-room | "South Point Hotel and Casino has a 24-hour non-smoking poker room." · "We feature tournaments daily with aggressive guarantees at 10:10 am, 2:10 pm, 6:10 pm and 10:10 pm with buy-ins of $120 and $300." · "Room rates are available with 4 hours of cash play for our out-of-town guests and parking is always free!" |
| Official daily schedule page | https://southpointcasino.com/casino/poker-room/daily-tournament-schedule | One schedule image plus sixteen rules-sheet images with no text layer: `01_120-No-Limit-Holdem`, `02_120-No-Limit-Holdem-Chip-Chop`, `03_120-Omaha-8-or-Better`, `04_120-Crazy-Pineapple-Turbo`, `05_120-No-Limit-Holdem-Turbo-Mega-Stack`, `06_200-No-Limit-Holdem-Bounty`, `07_200-Deep-Stack`, `08_120-No-Limit-Holdem-Turbo-Bounty` (all marked Oct2026), each split into two pages. |
| Official home page | https://southpointcasino.com/ | "nestled in the southwest valley, just a short drive from the iconic Las Vegas Strip!" |

**No row is built.** The page's text gives four start times and two buy-in levels without
saying which buy-in belongs to which time, and the entry rules exist only inside images. A row
needs a buy-in and an entry rule attached to a time; neither can be read here. Flags **F68**
(image-only schedule) and the mismatch noted on the page: the eight rules sheets are $120 and
$200 events while the room page advertises "$120 and $300".

---

## 4. Horseshoe — six daily tournaments confirmed, nothing else published

| Source | URL | What it printed |
|---|---|---|
| Official casino page | https://www.caesars.com/horseshoe-las-vegas/casino | "The Hall of Fame Poker Room at Horseshoe Las Vegas features 20 tables and offers many exciting varieties of live poker suited for the recreational poker player or the seasoned veteran. You are sure to find your favorite with games such as No-Limit Hold'em, Limit Hold'em, Pot Limit Omaha and Omaha Eight or Better. Test your luck with 6 exciting tournament times daily." |

`/casino/poker-room.html` and `/casino/poker` both resolve to the same casino page, which
carries no schedule, buy-in, guarantee or structure, and no schedule PDF was found on
caesars.com. Third-party sites publish times ($9am/11am/2pm/5pm/8pm/11pm) and buy-ins
($100/$160) for these events; they are not official and are not used. Flag **F69**.

---

## 5. Rooms with a poker room on the official page but no tournament schedule

| Room | Source | What the official page prints |
|---|---|---|
| Planet Hollywood | https://www.caesars.com/planet-hollywood/casino | "23 Live Poker Tables"; "Planet Hollywood Casino takes up a notch with an exciting gaming floor, new live action poker room and poolside blackjack." No schedule, buy-in or structure. |
| Mandalay Bay | https://mandalaybay.mgmresorts.com/en/casino/poker-tables.html | Hours "Wednesday – Monday: 10:00 AM – 4:00 AM", "Tuesday: Closed"; "Price Range $60 - $1,000"; "For reservations 702.632.7790"; "To set up a Poker Tournament as a group, please contact 702.632.7790." No recurring tournament schedule. |

---

## 6. Rooms where the official casino page publishes no live poker room

Each page below was read on 2026-11-17. Paris lists "Poker Derivative Table Games" (Pai Gow,
Ultimate Texas Hold'Em, Let It Ride, Three Card Poker, Mississippi Stud, I Luv Suits, Crazy 4)
and no live poker room; Luxor's table-games page lists only pit and derivative games; Excalibur's
casino page lists slots, blackjack, table games and the sportsbook; SAHARA lists slots, table
games and the sportsbook; Resorts World's gaming page and casino-events page list slots, table
games, high limit and free-play promotions; Fontainebleau's casino page lists table games, a
high-limit area with "poker machines" (electronic) and the race and sports book; The STRAT's
casino page lists slots, table games and the William Hill sports book
(`thestrat.com/casino/poker` returns the official 404 page).

| Room | Page read |
|---|---|
| Paris Las Vegas | https://www.caesars.com/paris-las-vegas/casino |
| Luxor | https://luxor.mgmresorts.com/en/casino/table-games.html |
| Excalibur | https://excalibur.mgmresorts.com/en/casino.html |
| SAHARA Las Vegas | https://www.saharalasvegas.com/casino |
| Resorts World Las Vegas | https://www.rwlasvegas.com/gaming/ and https://www.rwlasvegas.com/gaming/casino-events/ |
| Fontainebleau Las Vegas | https://www.fontainebleaulasvegas.com/casino/ |
| The STRAT | https://thestrat.com/casino |
| The Mirage (rebranding) | https://mirage.mgmresorts.com/en/casino/poker-tables.html resolves to https://www.hardrockvegas.com/ — "Coming Soon to the Las Vegas Strip" |

Flag **F70** records that absence from an official page is not proof that a room does not exist.
Flag **F71** records that the MGM Resorts poker hub links two of these properties — Luxor to
`/en/casino/table-games.html` and Excalibur to `/en/casino/poker-room.html`, which redirects to
`/en/casino.html` — to pages that publish no poker room.

---

## 7. What is still blank

| Item | Why it is blank |
|---|---|
| Walking time from any hotel to MGM Grand, the Orleans or South Point | No routed walking record was produced in this session. The site's walking table covers twelve pairs, all of them to the Venetian and Wynn poker rooms. Nothing is estimated here. Flag **F72**, logged as a request in `COORDINATION.md`. |
| MGM Grand Saturday $150 NLH entry rule, fee split and late-registration close | No structure sheet for that event is published on the official poker page, which links one sheet only (the $120 NLH). Flag **F63**. |
| MGM Grand guarantee for the $120 dailies | Neither the page nor the schedule PDF prints a guarantee for them; only the Saturday $150 carries one ($2,000). |
| South Point times-to-buy-ins mapping and every South Point entry rule | The schedule and rules sheets are images. Flag **F68**. |
| Horseshoe times, buy-ins, guarantees and structures | Not published on the official page; third-party values deliberately not used. Flag **F69**. |
| The period the Orleans grid covers | The PDF prints no month, year or date range. Flag **F65**. |
| Hotel rates for stays built around these rooms | The dated rate log holds five Venetian/Palazzo quotes only. No quote was captured for a stay built around MGM Grand, the Orleans or South Point in this session. |

## 8. Checks run

- `python3 scripts/build_other_rooms.py` → 14 rooms surveyed, 6 publishing a poker room, 2
  publishing a readable schedule, 17 recurring event rows (0 single entry, 13 re-entry, 3 paid
  chips, 1 unverified), 13 flags.
- `python3 scripts/check_links.py` → OK (22 pages, 317 tournament rows, 7 hotels, 5 dated
  rates, 70 schedule days).
- `node scripts/smoke_test.js` → 22/22 pages render in a headless DOM.
