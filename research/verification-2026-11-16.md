# Verification log — session 40ca34e5, 2026-11-16

Line-by-line record of what was read from official sources, with links for manual review.
Every verdict below comes from text printed on the linked official document.

## 1. Method

1. The official series pages for both Venetian series were read in full (four sections for the November series, two for the NYE series). Every row on those pages carries a link to its own structure sheet, so each event was bound to the sheet the operator published for it — no sheet was guessed.
2. The official WPT schedule PDF and the official WPT structures PDF were fetched and parsed. Each schedule row was matched to the structure block that prints the same flight date and time (63 rows) or the same event name and buy-in (23 rows). 86 of 87 rows quote a re-entry rule from their own block.
3. The official Wynn Signature Series schedule PDF was read row by row. Its structures PDF is image-based (166 KB, 27 characters of text), so no entry rule could be quoted for those 31 rows.
4. Every source URL is re-fetched, hashed and snapshot-recorded by `scripts/check_source_facts.py`; the last check covered 71 URLs: 68 fetched with text, 1 marked inactive (a URL that 404s), 2 unreachable (Bellagio and ARIA time out). It recorded 9 raw page changes but 0 published-value changes, because the monitor compares the numbers, dates, times and rule words printed on each page rather than the raw bytes.

**A note on row counts.** This log was written against the schedule rows this session transcribed: 87 WPT rows and 31 Wynn Signature Series rows, counting only playable starting flights and single-day events, with milestone satellites, Day 2/Day 3 restarts and final tables excluded. The published dataset (`data/tournaments.json`) is larger — 135 WPT rows and 38 Signature Series rows — because session `baba1a15` transcribed the satellites and continuations as well. Both are readings of the same official schedule PDFs; the counts differ only in what was transcribed, not in what the PDFs print.

## 2. Venetian structure sheets, one row per sheet

| Sheet | Events covered | Buy-in $ | House fee $ | Chips | Level | Late registration | Verdict | Source |
|---|---|---|---|---|---|---|---|---|
| NYE sheet 1 | 01, 03, and 17 | 400 | 65 | 30,000 | 30 minutes | 8 levels + Break (~ 3:40 PM) | Single Entry | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_dec_2026-structure_1.pdf) |
| NYE sheet 2 | 02, 04, 13, 22, 26, 29, and 32 | 200 | 40 | 25,000 | 30 minutes. | 8 levels + Break (9:40 PM) | Re Entry | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_dec_2026-structure_2.pdf) |
| NYE sheet 3 | 05 | 600 | 90 | 40,000 | 30 minutes | 10 levels + Break (4:55 PM) | Single Entry | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_dec_2026-structure_3.pdf) |
| NYE sheet 4 | 06, 09, and 11 | 260 | 40 | 20,000 | 20 minutes. | 6 levels + Break (~5:25 PM or ~  | Single Entry | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_dec_2026-structure_4.pdf) |
| NYE sheet 5 | 15, 18, 21, and 24 | 200 | 35 | 20,000 | 20 minutes. | 6 levels + Break (~5:25 PM or 12 | Single Entry | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_dec_2026-structure_5.pdf) |
| NYE sheet 6 | 08 | 1100 | 140 | 40,000 | 40 minutes | 9 levels + Break (~ 5:55 PM) | Multi Flight | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_dec_2026-structure_6.pdf) |
| NYE sheet 7 | 16 and 19 | 200 | 30 | 20,000 | 15 minutes. | 6 levels + Break (~7:55 PM) | Single Entry | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_dec_2026-structure_7.pdf) |
| NYE sheet 8 | 20 | 1600 | 180 | 40,000 | 40 minutes | 9 levels + Break (~ 5:55 PM) | Multi Flight | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_dec_2026-structure_8.pdf) |
| NYE sheet 9 | 25 | 200 | 40 | 25,000 | 30 minutes. | 8 levels + Break (9:40 PM) | Re Entry | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_dec_2026-structure_9.pdf) |
| NYE sheet 10 | 31 | 400 | 65 | 40,000 | 30 minutes | 10 levels + Break (~ 3:55 PM) | Single Entry | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_dec_2026-structure_10.pdf) |
| NYE sheet 11 | 28 | 400 | 65 | 40,000 | 30 minutes | 10 levels + Break (~ 4:55 PM) | Single Entry | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_dec_2026-structure_11.pdf) |
| NYE sheet 12 | 14 | 600 | 90 | 40,000 | 30 minutes | 10 levels + Break (~ 4:55 PM) | Single Entry | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_dec_2026-structure_12.pdf) |
| NYE sheet 13 | 30 | 300 | 60 | 30,000 | 40 minutes | 6 levels + Break (~ 3:40 PM) | Multi Flight | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_dec_2026-structure_13.pdf) |
| NYE sheet 14 | 30 | 300 | 60 | 30,000 | 30 minutes | 6 levels + Break (~ 8:40 PM) | Re Entry | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_dec_2026-structure_14.pdf) |
| NYE sheet 15 | 27 | 250 | 50 | 40,000 Level Duration Day 1: 30 minutes Level Duration Day 2: 40 minutes |  | 8 levels + Break (~ 3:40 PM or ~ | Multi Flight | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_dec_2026-structure_15.pdf) |
| Nov sheet 1 | 09, 11, 13, 15, 21, 22, 23, 25, 60, 61, 62, and 64 | 200 | 40 | 25,000 | 30 minutes. | 8 levels + Break (9:40 PM) | Single Entry | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_1.pdf) |
| Nov sheet 2 | 07 | 400 | 70 | 40,000 | 40 minutes | 9 levels + Break (5:55 PM) | Multi Flight | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_2.pdf) |
| Nov sheet 3 | 19 | 400 | 70 | 40,000 | 40 minutes | 9 levels + Break (5:55 PM) | Multi Flight | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_3.pdf) |
| Nov sheet 4 | 59 | 600 | 95 | 40,000 | 40 minutes | 9 levels + Break (5:55 PM) | Multi Flight | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_4.pdf) |
| Nov sheet 5 | 02 and 12 | 300 | 58 | 40,000 | 30 minutes. | 10 levels + Break (~ 4:55 PM) | Single Entry | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_5.pdf) |
| Nov sheet 6 | 10 | 400 | 65 | 40,000 | 30 minutes. | 10 levels + Break (~ 4:55 PM) | Single Entry | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_6.pdf) |
| Nov sheet 7 | 14, 28, and 63 | 600 | 90 | 40,000 | 30 minutes. | 10 levels + Break (~ 4:55 PM) | Single Entry | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_7.pdf) |
| Nov sheet 8 | 18 and 58 | 200 | 40 | 25,000 | 30 minutes. | 8 levels + Break (9:40 PM) | Re Entry | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_8.pdf) |
| Nov sheet 9 | 01 | 300 | 60 | 30,000 | 30 minutes | 6 levels + Break (~ 8:40 PM) | Multi Flight | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_9.pdf) |
| Nov sheet 10 | 01 | 300 | 60 | 30,000 | 40 minutes | 6 levels + Break (~ 3:40 PM) | Multi Flight | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_10.pdf) |
| Nov sheet 11 | 16, 30, and 54 | 600 | 90 | 40,000 | 30 minutes | 10 levels + Break (4:55 PM) | Single Entry | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_11.pdf) |
| Nov sheet 12 | 26 | 800 | 110 | 40,000 | 40 minutes | 6 levels + Break (~ 3:40 PM) | Multi Flight | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_12.pdf) |
| Nov sheet 13 | 26 | 800 | 110 | 40,000 | 30 minutes | 6 levels + Break (~ 8:40 PM) | Multi Flight | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_13.pdf) |
| Nov sheet 14 | 26 | 800 | 110 | 40,000 | 20 minutes | 6 levels + Break (~ 7:25 PM) | Multi Flight | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_14.pdf) |
| Nov sheet 15 | 29, 31, 34, 38, 42, 50, 51, 53, and 55 | 300 | 50 | 25,000 | 30 minutes. | 8 levels + Break (9:40 PM) | Single Entry | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_15.pdf) |
| Nov sheet 16 | 36 | 800 | 100 | 40,000 | 30 minutes. | 10 levels + Break (4:55 PM) | Single Entry | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_16.pdf) |
| Nov sheet 17 | 24 and 32 | 600 | 90 | 40,000 | 30 minutes | 10 levels + Break (~ 3:55 PM) | Single Entry | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_17.pdf) |
| Nov sheet 18 | 03, 04, and 05 | 200 | 35 | 30,000 | 20/15 minutes. | 6 levels + Break (~ 12:25 PM) | Single Entry | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_18.pdf) |
| Nov sheet 19 | 33 and 37 | 100 | 20 | 20,000 | 20 minutes. | 6 levels + Break (~6:25 PM) | Single Entry | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_19.pdf) |
| Nov sheet 20 | 49 | 1100 | 140 | 40,000 | 40 minutes | 9 levels + Break (~ 4:55 PM) | Multi Flight | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_20.pdf) |
| Nov sheet 21 | 47 | 2200 | 225 | 40,000 | 40 minutes | 9 levels + Break (~ 4:55 PM) | Multi Flight | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_21.pdf) |
| Nov sheet 22 | 20 | 300 | 58 | 30,000 | 30 minutes | 8 levels + break (~ 4:40 PM) | Single Entry | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_22.pdf) |
| Nov sheet 23 | 57 | 600 | 90 | 30,000 | 30 minutes | 8 levels + break (~ 4:40 PM) | Single Entry | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_23.pdf) |
| Nov sheet 24 | 41 and 44 | 260 | 40 | 20,000 | 20 minutes. | 6 levels + Break (~6:25 PM) | Single Entry | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_24.pdf) |
| Nov sheet 25 | 45, 46, and 48 Event # 45 | 260 | 35 | 20,000 | 15 minutes. | 6 levels | Single Entry | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_25.pdf) |
| Nov sheet 26 | 17 | 400 | 60 | 30,000 | 30 minutes | 8 levels + break (~ 4:40 PM) | Single Entry | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_26.pdf) |
| Nov sheet 27 | 40 | 600 | 90 | 30,000 | 30 minutes | 8 levels + break (~ 4:40 PM) | Single Entry | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_27.pdf) |
| Nov sheet 28 | 27 | 600 | 90 | 30,000 | 30 minutes | 8 levels + break (~ 4:40 PM) | Single Entry | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_28.pdf) |
| Nov sheet 29 | 06 | 200 | 40 | 30,000 | 30 minutes. | 8 levels + Break (~ 3:40 PM) | Single Entry | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_29.pdf) |
| Nov sheet 30 | 08 | 200 | 40 | 25,000 | 30 minutes. | 8 levels + Break (9:40 PM) | Single Entry | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_30.pdf) |
| Nov sheet 31 | 35 | 600 | 80 | 40,000 | 30 minutes. | 8 levels + Break (~ 2:40 PM) | Single Entry | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_31.pdf) |
| Nov sheet 32 | 39 | 800 | 90 | 40,000 | 40 minutes | 9 levels + Break (~ 4:55 PM) | Single Entry | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_32.pdf) |
| Nov sheet 33 | 43 | 600 | 80 | 40,000 | 30 minutes. | 10 levels + Break (4:55 PM) | Single Entry | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_33.pdf) |
| Nov sheet 34 | 52 | 1100 | 130 | 40,000 | 30 minutes. | 10 levels + Break (4:55 PM) | Single Entry | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_34.pdf) |
| Nov sheet 35 | 56 | 1100 | 140 | 40,000 | 40 minutes | 9 levels + Break (~ 4:55 PM) | Multi Flight | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_35.pdf) |
| Nov sheet 36 | 56 | 1100 | 140 | 40,000 | 30 minutes | 9 levels + Break (~ 11:10 PM) | Multi Flight | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_36.pdf) |
| Nov sheet 37 | 47 | 2200 | 225 | 40,000 | 30 minutes | 9 levels + Break (~ 11:10 PM) | Multi Flight | [PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_37.pdf) |

Sheets classified **Single Entry** print no re-entry, re-buy, add-on or multiple-entry clause.
Sheets classified **Multi Flight** print a "starting flight" clause plus "Any player who bags chips for Day 2 may not play a subsequent flight".
Sheets classified **Re Entry** print wording that contemplates a further entry ("subsequent re-entry", or "All subsequent buy in's after the initial buy in will be $200").
Satellite sheets (Nov 19, 24, 25; NYE 4, 5, 7) are listed for completeness; their events are not rows in the dataset.

## 3. WPT World Championship: the re-entry rule quoted per event

Every one of the 86 matched rows quotes a re-entry rule from its own block in the official
[WPT structures PDF](https://cdn.wynnresorts.com/image/upload/v1750864036/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Structures.pdf).
The distinct wordings, and how many rows quote each:

| Rows | Official wording (start of the Registration clause) |
|---|---|
| 16 | Unlimited re-entry for each starting flight will be available until the start of level 9. A player who advances to Day 2 |
| 16 | Unlimited re-entry will be available until the start of level 9. |
| 9 | Unlimited re-entry will be available until the start of level 9 (approximately 5:30 p.m.). |
| 8 | Unlimited re-entry for each starting flight will be available until the start of level 10. A player who advances to Day  |
| 5 | Unlimited re-entry will be available until the start of level 9 (approximately 4:30 p.m.). |
| 5 | One (1) Entry and One (1) re-entry for each starting flight will be available until the start of level 10 (approximately |
| 4 | Unlimited re-entry will be available until the start of level 10 (approximately 7:30 p.m.). |
| 4 | Unlimited re-entry will be available until the start of level 7 (approximately 4:30 p.m.). |
| 4 | Unlimited re-entry for will be available until the start of level 10. |
| 3 | Unlimited re-entry will be available until the start of level 9 |
| 3 | Four (4) Entries maximum. Players are allowed One (1) entry per starting flight + One (1) Day 2 Entry prior to the start |
| 3 | Unlimited re-entry will be available until the start of level 10 (approximately 6:30 p.m.). |
| 1 | Unlimited re-entry for each starting flight will be available until the start of level 10. |
| 1 | Unlimited re-entry will be available until the start of level 9 (approximately 2:30 p.m.). |
| 1 | Unlimited re-entry will be available until the start of level 9 (approximately 4:30 p.m.) |
| 1 | Unlimited re-entry will be available until the start of level 10 (approximately 8:30 p.m.) |
| 1 | Unlimited re-entry will be available until the start of level 11 (approximately 1:15 p.m. on Day 2). |
| 1 | Unlimited re-entry will be available until the start of level 9 (approximately 9 p.m.). |

One event (the $1,100 WPT Prime Championship) allows **One (1) Entry and One (1) re-entry** per starting flight; the $10,400 Championship allows **Four (4) entries maximum**. No block in the document prints a prohibition on re-entry.

## 4. Wynn Signature Series

The [official schedule PDF](https://cdn.wynnresorts.com/image/upload/v1753296112/visitwynn_pdfs_files/Poker/Wynn%20Signature%20Series/Wynn_Signature_Series_Schedule.pdf) prints the series dates as **January 11-24, 2027** and was read row by row: 31 playable rows (satellites and Day 2 restarts excluded), each with date, day, time, event, guarantee, entry, chips and levels. The [official structures PDF](https://cdn.wynnresorts.com/image/upload/v1762299460/visitwynn_pdfs_files/Poker/Wynn%20Signature%20Series/Wynn_Signature_Series_Structures.pdf) returns 27 characters of text, so the entry rule for every one of these rows is blank and flagged (F6).

## 5. Wynn daily tournaments (official poster and structures)

| Official fact | Source |
|---|---|
| $10,000 guarantee, Monday-Thursday, $200 NLH, 12 p.m. | [daily poster](https://cdn.wynnresorts.com/image/upload/v1752011166/visitwynn_pdfs_files/Poker/Daily%20Tournaments/poker-daily-tournament-poster.pdf) |
| $25,000 guarantee Saturday, $25,000 Sunday, $200 NLH, 12 p.m. | same |
| $40,000 guarantee Friday, $240 NLH **Rebuy**, 12 p.m. | same |
| Nightly $10,000 guarantee, $160 NLH, 6 p.m. | same |
| $200/$160 events: "Registration and re-entries will be available until the start of level 9"; one $100 add-on per entry | [daily structures](https://cdn.wynnresorts.com/image/upload/v1752011191/visitwynn_pdfs_files/Poker/Daily%20Tournaments/Poker-All_Daily_Structures.pdf) |
| Friday $240: "Registration, rebuys and add-ons will be available until the start of level 9... **Re-entry is NOT allowed.**" | same |
| The daily schedule is suspended during each Wynn Signature, Wynn Millions and Classic series | [Wynn poker room](https://www.wynnlasvegas.com/casino/poker) |

None of the dailies is single entry, so none is in the single-entry list or the day plan.

## 6. Hotel facts, each with the page it was read from

See the line-by-line hotel table in `REVIEW.md`. The rate-capture attempt and its result (`$XXX` placeholders) are recorded in `FLAGGED.md` as F8.

## 7. What a reviewer should spot-check first

1. Flag F13 — the single-entry classification rests on the absence of a clause.
2. Flag F4 — the same $200 Bounty event is worded differently in the two Venetian series.
3. Flag F8 — no nightly rate could be captured, so every true-cost cell is blank.
4. Flag F6 — 31 Wynn Signature Series rows are unverified because the official structures PDF is images.
