# Flagged for Review

Published so you can review each item. Flags do not block the merge. Every flag keeps the text of the
official source it came from, and every flagged row carries the flag in `data/tournaments.json` so the
row itself says what is odd about it.

## A. Irregularities in the official sources

| # | Irregularity | Source | Effect on the data |
|---|---|---|---|
| F1 | NYE event page prints the Dec 26 rows as "Saturday, December 26, **2025**". The series header reads "December 24, 2026 – January 10, 2027" and the printed weekday (Saturday) matches December 26, 2026. | [NYE event page](https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-dec-2026.html) | The three Dec 26 rows are stored as 2026-12-26 and carry the flag. |
| F2 | NYE event page prints "Tuesaday" for the Jan 5, 2027 rows. | Same page | The four Jan 5 rows are stored as 2027-01-05 and carry the flag. |
| F3 | WPT schedule prints one block under the heading "**Dec. 18 Wednesday**", but December 18, 2026 is a Friday and the same PDF prints a separate "Dec. 18 Friday" block. | [WPT schedule PDF](https://cdn.wynnresorts.com/image/upload/v1757097329/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Schedule.pdf) | That block is stored as **December 16, 2026**, the only reading that also fits the WPT World Championship day order (Day 1A Dec 13, 1B Dec 14, 1C Dec 15, Day 2 Dec 16). Each affected row says so. |
| F4 | WPT schedule prints the $600 NLH Turbo on December 21 at **8 p.m.**, while the $600 NLH Turbo structure sheet lists "Monday, December 21, 2026 at **6 p.m.**". | [WPT schedule PDF](https://cdn.wynnresorts.com/image/upload/v1757097329/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Schedule.pdf) and [structures PDF](https://cdn.wynnresorts.com/image/upload/v1750864036/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Structures.pdf) | Both times are kept. The schedule time is stored and the conflict is flagged on the row. |
| F5 | WPT schedule prints a buy-in in each "Day 2" / "Final Table" row that belongs to a different event than the day it names: "Dec. 3 · 1 p.m. · No Limit Hold'em Day 2" carries $1,600 but the $800 structure sheet prints that Day 2; "Dec. 5 · 11 a.m. · No Limit Hold'em Day 2" carries $1,100 but the $1,600 structure sheet prints that Day 2. | Same schedule PDF plus the structures PDF | The structure sheet is treated as authoritative for the day-to-event link; the printed value is recorded in the row flag. |
| F6 | WPT schedule prints four rows whose weekday heading does not match the date in the same block, and the block order is not chronological (the "Dec. 18 Wednesday" block sits between Dec 15 and Dec 17). | Same schedule PDF | Handled with F3. The row order in the data is chronological. |
| F7 | WPT schedule footnote \*\*\*: "ClubWPT Gold adds $1,000,000" and "ClubWPT Gold is not available in Nevada." The "$1,000,000 Added" wording is printed on the World Championship rows. | Same schedule PDF | The footnote text is stored in the row flag. Whether the addition is paid to Nevada players is still open (see QUESTIONS.md). |
| F8 | WPT schedule footnote \*\*\*\*: "The Tournament Entry for the Ladies Championship is $11,100. Ladies will receive a discounted entry." The printed ladies buy-in is $1,100. | Same schedule PDF | The footnote is stored in the row flag; the printed $1,100 is kept as the buy-in. |
| F9 | WPT schedule prints the $3,000, $10,500 and $25,800 buy-ins with a footnote that "Players registered prior to the start of the event will receive a discounted entry". | Same schedule PDF | Stored in the row flag. |
| F10 | Structure sheets for events 1, 7, 19, 26, 30, 47, 49, 56 and the NYE events 8, 20 and 27 carry clause 08: "Any player who bags chips for Day 2 may not play a subsequent flight." The clause does not say whether a player who busts may enter a later flight. | Sheets linked from the official event pages | These rows are in the separate section, not the single-entry ranking. |
| F11 | NYE structure sheet 15 (event 27) adds: "Players who cash on Day 1 but bust before making Day 2 may play another flight." | [NYE sheet 15](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_dec_2026-structure_15.pdf) | Kept in the separate section because a later flight is still a possible second entry. |
| F12 | Structure sheet 8 (events 18 and 58) says "All subsequent buy in's after the initial buy in will be $200", which may imply a second buy-in. | [Sheet 8](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_8.pdf) | Rows 18 and 58 are in the separate section. |
| F13 | Structure sheet 2 (NYE, events 2, 4, 13, 22, 26, 29, 32) mentions re-entry in clause 06 for **Event #29 only**: "The $20 discount can be applied to the initial entry or any subsequent re-entry." | [NYE sheet 2](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_dec_2026-structure_2.pdf) | Event 29 is listed as re-entry; the other events on that sheet are single entry. The sheet note says so. |
| F14 | Bounty guarantees include bounties: sheet 15 reads "Guarantee: $15,000 (prize pool + total bounties)". Each bounty pays $100 per elimination. | [Sheet 15](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_15.pdf) | A bounty guarantee is not a pure prize pool. Flagged on the bounty rows. |
| F15 | Venetian poker-suite page: rates "start as low as $119 and $209" without saying which property each applies to. | [Poker suite rates](https://www.venetianlasvegas.com/resort/casino/poker/suite-rates.html) | Not used as a room rate. |
| F16 | The Venetian hotel terms state a $55 resort fee "plus applicable tax" and a 13.38% Clark County Room Tax, but publish no itemized calculation. | [Venetian hotel terms](https://www.venetianlasvegas.com/legal/hotel-terms-and-conditions.html) | The 13.38% value is not applied to other hotels without property-specific support. |
| F17 | PDF date cells are blank for some rows (LIPS and PokerAtlas overlay rows) on the DSE IV schedule PDF. | [DSE IV schedule PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/dse-nov-2026-schedule.pdf) | The official event page prints a date on every row; the dates were taken from there. |
| F18 | Typos printed on official schedules: "No LImit" on the DSE IV event page; "BadugI" and "NIH" for NLH on the WPT schedule. | DSE IV event page, WPT schedule PDF | Names are kept as printed. |
| F19 | The WPT schedule prints several "Day 2", "Day 3", "Day 4" and "Final Table" rows with no buy-in, no guarantee, no chips and no level count, and does not name the parent event. | Same schedule PDF | Those rows are marked as continuations with no parent stated, and say so. |

| Scheduled check never ran | `.github/workflows/monitor.yml` used a `name:` key inside its `schedule:` entry. The workflow schema accepts only `cron` there, so the daily source check never fired and `data/monitoring.json` still shows a run made from a sandbox where every operator domain was unreachable (0 of 59 sources). | Fixed by removing the unsupported key. The parallel provenance job (`scripts/check_source_facts.py`, weekly) does run in GitHub Actions and reports 68 of 71 sources fetched, which is the reachability evidence the monitoring page is still missing. |

## B. Items with no official value (left blank)

| # | Item | Why it is blank |
|---|---|---|
| U1 | Nightly room rate for every hotel and every date, except the one logged quote | No official rate for any stay date was retrieved. Third-party rates were not used. |
| U2 | Bellagio resort fee and room tax | No Bellagio-specific fee or tax value is printed on an official page read in this session. Third-party values conflict. |
| U3 | Caesars Palace resort fee and room tax | No Caesars Palace-specific fee or tax value is printed on an official page read in this session. An earlier draft quoted a general corporate range; that claim was not supported by a page read here and was removed. |
| U4 | ARIA resort fee and room tax | The official ARIA pages read here publish player rates by phone or e-mail only. |
| U5 | Walking time from any hotel to any venue | Not published on any official source. A walking route link is given instead. |
| U6 | Entry rule for 129 unverified official rows | No structure sheet is published for them. See QUESTIONS.md. |
| U7 | Entry rules for the 38 Wynn Signature Series rows | The official Signature Series structures PDF contains only a "COMING SOON" placeholder. |
| U8 | Entry rules for the WPT milestone and satellite rows | The WPT structures PDF ends with the PLO Mystery Bounty and publishes no sheet for them. |
| U9 | Registration opening times for the Venetian and Wynn series | Not printed in the schedules read. The structure sheets print a registration close time per event. |
| U10 | 2027 Las Vegas WSOP Circuit schedule | Not found on an official source. |

## C. Rows carrying a flag in the dataset

55 of the 316 rows carry at least one flag. They are listed with their flag text on the
[Monitoring page](pages/monitoring.html), and the same flag text is stored in the row itself under
`flags`, so the row can never be separated from the reason it is unusual.
