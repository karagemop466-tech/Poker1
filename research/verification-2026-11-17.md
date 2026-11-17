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
