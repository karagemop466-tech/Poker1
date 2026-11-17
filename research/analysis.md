# T4: Analysis notes

Session `baba1a15` · Checked 2026-11-16 · Inputs: `data/tournaments.json`, `data/hotels.json`,
`data/schedule.json`, `data/daily.json`, `data/rates.json`.

## Ranking method
- Single-entry events are ranked by guarantee ÷ buy-in. A higher figure means more prize pool per dollar entered.
- Bounty events carry a guarantee that includes bounties (sheet 15: "prize pool + total bounties"), so their ratio
  is not directly comparable to a pure prize pool. The ranking is shown with a note on each row.
- Milestone satellites have no dollar guarantee. Their prize is a seat, so they are listed with a `prize_text`
  value and a `satellite` label, and they are excluded from the cash ranking.
- The current top of the list is 93.8x (Event 36, $800 bounty, $75K GTD), then 83.3x twice (Event 54 and the
  NYE Event 14), then 68.2x (Event 52, $1,100 PKO), then five rows tied at 66.7x.

## Schedule method
- Each day names one verified single-entry event as the primary and, where possible, a conditional fallback that
  starts after the primary is estimated to finish. 45 of the 70 dates carry a primary; 24 also carry a fallback.
- Estimated end times come from the published level structure (levels × level length plus the published breaks).
  They are labelled as estimates and are never presented as official finish times.
- 45 of the 70 dates carry at least one verified single-entry event; 41 carry a cash one. The first cash
  single-entry event is Nov 18 at 11:10 AM. No verified cash single-entry event starts before 10:10 AM, so the
  8 to 10 AM window is free time. The only earlier single-entry start in the dataset is the 9:10 AM $260 turbo
  milestone satellite on Dec 12, and it pays a seat rather than cash.
- Two days carry an overlap flag: Dec 12 and Jan 2. Both involve a satellite whose estimated end is an upper
  bound, because the tournament ends when the seats run out.

## Hotel cost method
- Only verified values are used. Nothing is inferred.
- Fees are verified for six hotels; the room tax percentage is verified for one and shown as a labelled estimate
  for two. Only one dated quote is on file, so the per-hotel
  true cost stays blank and the calculator asks for a rate instead of assuming one.

## Risks to the analysis
- Multi-flight events (66 rows) could allow a second entry, which would change the value ranking. They are kept
  out of the ranking until the poker room confirms.
- 108 rows carry a printed re-entry clause from their own structure sheet and are in the separate section.
- The 38 unverified rows (all Wynn Signature Series) are listed but never ranked. No Wynn World Championship
  row is unverified any more: all 113 WPT entry rows are joined to their printed sheet.
- The full Venetian terms state a $55 resort fee plus applicable tax and a 13.38% Clark County room tax. The
  other hotels' property-specific tax values and all date-specific room rates remain unverified, so true-cost
  cells are blank.
- Two official Wynn sources disagree about the December 21 $600 NLH Turbo start time, and the WPT schedule
  prints one block under a weekday heading that does not match its date. Both are recorded as flags on the rows
  that they affect rather than being silently corrected.
