# Flagged for Review

Published so you can review the items. Flags do not block the merge. Every flag links to its source.

## A. Irregularities in the official sources

| # | Irregularity | Source |
|---|---|---|
| F1 | NYE event 5 (Dec 26) is printed as "Saturday, December 26, 2025". The series runs 2026 to 2027. | [NYE event page](https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-dec-2026.html) |
| F2 | Typos printed on official schedules: "(IDAY)" for "(1DAY)" on the DSE IV schedule; "No LImit" on the DSE IV event page; "BadugI" and "NIH" for NLH on the WPT schedule. Names are kept as printed. | [DSE IV schedule](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/dse-nov-2026-schedule.pdf), [WPT schedule](https://cdn.wynnresorts.com/image/upload/v1757097329/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Schedule.pdf) |
| F3 | Structure sheets for events 1, 7, 19 and 26 carry clause 08: "Any player who bags chips for Day 2 may not play a subsequent flight." The clause does not say whether a player who busts may enter a later flight. Sheets read: [2](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_2.pdf), [3](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_3.pdf), [9](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_9.pdf), [10](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_10.pdf), [12](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_12.pdf), [13](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_13.pdf), [14](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_14.pdf) |
| F4 | Structure sheet 8 (events 18 and 58) says "All subsequent buy-in's after the initial buy in will be $200", which may imply a second buy-in. Re-read this session: not confirmed. | [Structure 8](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_8.pdf) |
| F5 | Bounty guarantees include bounties: sheet 15 reads "Guarantee: $15,000 (prize pool + total bounties)". Each bounty pays $100 per elimination. | [Structure 15](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_15.pdf) |
| F6 | WPT footnote ***: ClubWPT Gold adds $1,000,000 and "is not available in Nevada." The headline "$1M added" is printed on the WPT Day 1 rows. Needs reconciling. | [WPT schedule](https://cdn.wynnresorts.com/image/upload/v1757097329/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Schedule.pdf) |
| F7 | WPT footnote ****: "The Tournament Entry for the Ladies Championship is $11,100. Ladies will receive a discounted entry." The printed ladies buy-in is $1,100. | [WPT schedule](https://cdn.wynnresorts.com/image/upload/v1757097329/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Schedule.pdf) |
| F8 | Caesars Palace resort fee: official disclaimer gives a general $45 to $50 plus tax. Third-party values conflict. | [Caesars disclaimer](https://www.caesars.com/corporate/disclaimer) |
| F9 | Venetian poker-suite page: rates "start as low as $119 and $209" without saying which property each applies to. | [Poker suite rates](https://www.venetianlasvegas.com/resort/casino/poker/suite-rates.html) |
| F10 | The full Venetian hotel terms state a $55 resort fee "plus applicable tax" and a 13.38% Clark County Room Tax. The current text supports that the Venetian fee is taxed; it does not provide a separate itemized calculation. The 13.38% value is not applied to other hotels without property-specific support. | [Venetian hotel terms](https://www.venetianlasvegas.com/legal/hotel-terms-and-conditions.html) |
| F11 | PDF date cells are blank for some rows (LIPS and PokerAtlas overlay rows). The official event page prints a date for each row. Event 49 was wrong in the draft and is corrected. | [DSE IV event page](https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html) |
| F12 | Event 1 (Nov 16) starts on the check date. Nov 16 and 17 have only Event 1 flights, which are multi-flight rows. | [DSE IV event page](https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html) |

## B. Items with no official value (left blank)

| # | Item | Why it is blank |
|---|---|---|
| U1 | Nightly room rate, every hotel, every date | No official rate for any stay date was retrieved. Third-party rates were not used. |
| U2 | Bellagio resort fee | No official MGM page found. Third-party values conflict ($45, $50, $55). |
| U3 | Caesars Palace resort fee | Official range only ($45 to $50). Property fee not confirmed. |
| U4 | ARIA resort fee | Official home page read; fee terms not found on it. |
| U5 | Walking time from any hotel to any venue | Not published on any official source. |
| U6 | Entry rule for 171 unverified official rows | Structure sheets not read (see QUESTIONS.md). |
| U7 | Venetian NYE entry rules | Sheets not read. All 31 NYE rows are unverified. |
| U8 | Wynn Signature Series entry rules | Sheets not read. All 31 rows are unverified. |
| U9 | Registration opening times (Venetian and Wynn) | Not printed in the schedules read. The schedules print a REG CLOSES time per event. |
| U10 | 2027 Las Vegas WSOP Circuit schedule | Not found on an official source. |

## D. Verification scope note (integration session arena/f5896c06-poker1, 2026-11-16)

This session re-verified what is verifiable from the sandbox: the site builds cleanly (`scripts/build_site.py` produces zero diff), all 11 pages pass `scripts/check_links.py` (JSON valid, every local link resolves, no external assets, every data row carries an https source), and the data cross-checks (225 rows: 33 single-entry verified, 6 re-entry, 15 possible multi-entry, 171 unverified).

The official venue sources could NOT be re-fetched from this sandbox (outbound internet is limited to github.com / api.github.com and related hosts; venetianlasvegas.com, cdn.wynnresorts.com and github.io return connection failure). Therefore no content on those official pages was re-confirmed this session. All existing rows were verified against those official sources in prior sessions and retain their official links; every unconfirmed value remains blank and flagged. Nothing was inferred or filled in.

Live site URL: https://karagemop466-tech.github.io/Poker1/ (GitHub Pages API status: `built`, source branch `main`, path `/`). The live site could not be fetched from this sandbox.

## C. Official links for manual review

- [Venetian DeepStack IV event page](https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html)
- [Venetian DeepStack NYE event page](https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-dec-2026.html)
- [Wynn poker room](https://www.wynnlasvegas.com/casino/poker) (the official schedule prints wynnpoker.com and (702) 770-7654)
- [Wynn Signature Series schedule (PDF)](https://cdn.wynnresorts.com/image/upload/v1753296112/visitwynn_pdfs_files/Poker/Wynn%20Signature%20Series/Wynn_Signature_Series_Schedule.pdf)
- [Wynn WPT structures and terms (PDF)](https://cdn.wynnresorts.com/image/upload/v1750864036/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Structures.pdf)
- [Wynn resort fee terms](https://www.wynnlasvegas.com/terms-and-conditions/848671) (prior search excerpt)
- [Venetian resort fee](https://www.venetianlasvegas.com/resort/resort-fee.html) (fetched and read)
- [Venetian hotel terms](https://www.venetianlasvegas.com/legal/hotel-terms-and-conditions.html) (full page fetched and read; 13.38% Clark County room tax and $55 resort fee plus applicable tax)
- [Caesars corporate disclaimer](https://www.caesars.com/corporate/disclaimer) (search excerpt)
- [ARIA home page](https://aria.mgmresorts.com/en.html)
