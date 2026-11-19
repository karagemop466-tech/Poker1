# Live re-verification — session aa1e89b0 (2026-11-19)

Scope: the official Venetian DeepStack Extravaganza IV schedule and a sample of its structure sheets,
re-read live on 2026-11-19 with the fetch tool, compared with `data/tournaments.json`.
Purpose: test whether any official source affirmatively states **single entry**, and check that the
stored date, start time, event number, name, buy-in and guarantee still match the official page.

No data row, rate, `last_checked` value or generated page was changed by this session. Nothing here
promotes an event to `SE`.

## 1. Official schedule page (read live)

Source: [Venetian DeepStack Extravaganza IV, November 16 – December 23, 2026](https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html)
(read in chunks 0, 1 and 2 of 4; the page is titled "DeepStack Extravaganza - November 16 – December 23, 2026").

| Window read | Stored rows compared | Result |
|---|---|---|
| Mon 16 Nov – Mon 30 Nov (events 1–22) | r001–r042 | Date, start, event number, buy-in and guarantee match on every row. |
| Tue 1 Dec – Sat 19 Dec (events 19–58) | r044–r207 | Date, start, event number, buy-in and guarantee match on every row. |

Wording differences only (not value differences): "Progressive Knock-Out Bounty (PKO)" vs
"Progressive Knock-Out Bounty"; "Pot Limit Omaha Double Board Bomb Pot" vs "Pot Limit Omaha … Double Board Bomb Pot";
"NLH" vs "No Limit Hold'em". The page's own typos ("No LImit") are not carried into the data.

Not re-read in this session: the page's chunk 3 (Dec 19 – Dec 23) and every structure sheet except the four below.
Those rows keep their 2026-11-17 `last_checked` value.

## 2. Structure sheets read live

| Sheet | Governs | Clause text relevant to entries | Read result |
|---|---|---|---|
| [#1 $200 NLH Bounty (1Day)](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_1.pdf) | Events 9, 11, 13, 15, 21, 22, 23, 25 and others (Nov 24 – Dec 2 bounty events) | None on re-entry, rebuy or add-on. | **Silent.** Not an SE confirmation. |
| [#3 $400 NLH 1A/1B/1C + Day 2](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_3.pdf) | Event 19 (1A/1B/1C) | Clause 8: "Any player who bags chips for Day 2 may not play a subsequent flight." | **Multi-flight clause.** Consistent with existing `MULTI`. Also states 40,000 starting chips and 5:55 PM late registration (matches row r033). |
| [#5 $300 NLH (1Day)](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_5.pdf) | Events 2 and 12 (Nov 18, Nov 26) | None on re-entry, rebuy or add-on. | **Silent.** Fee $58 / pool $242 / 40,000 chips / late reg ~4:55 PM all match rows r005 and r018. |
| [#18 $200 NLH RaceDay Stack (1Day)](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_18.pdf) | Events 3, 4, 5 (Nov 19–21) | None on re-entry, rebuy or add-on. | **Silent.** Late reg ~12:25 PM, fee $35 / pool $165, 30,000 chips all match row r007. |
| [#29 $200 NLH (1Day)](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_29.pdf) | Event 6 (Nov 22) | None on re-entry, rebuy or add-on. | **Silent.** Fee $40 / pool $160 / late reg ~3:40 PM match row r010. |

Sheets are PDFs read through the fetch tool; they are single-page for these events.

## 3. Conclusion

- No re-read sheet affirmatively states single entry, no re-entry, no rebuy or no add-on.
  Silence is not confirmation, so the `CAND` and `MULTI` statuses on these rows stay as they are.
- The one clause read that restricts entries (sheet #3, Day 2 bagging) is a multi-flight restriction,
  so the `MULTI` status on the 1A/1B/1C events stays as well.
- Stored fee, pool, starting-chip and late-registration values for the four sheets above match the
  sheets.

## 4. Irregularities (for manual review, not changed here)

1. The Venetian sheets say "TDA rules apply" but do not say whether re-entry is allowed for the
   1Day events (sheets #1, #5, #18, #29). The fix is a written answer from the Venetian Poker Room,
   not an inference.
2. Sheet #3 gives event 19 a 5:55 PM late-registration cut-off, which matches row r033; sheet #3 is
   the only sheet read here that has a Day 2 clause.
3. The event page's chunk 3 (Dec 19–23) and the other 40-odd structure sheets were not re-read here.
   They are still covered by the existing daily monitor and by the archived 2026-11-17 reads.

## 5. Sources (for manual review)

- Official event page: https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html
- Sheet #1: https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_1.pdf
- Sheet #3: https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_3.pdf
- Sheet #5: https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_5.pdf
- Sheet #18: https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_18.pdf
- Sheet #29: https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_29.pdf
