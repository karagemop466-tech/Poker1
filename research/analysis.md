# T4: Analysis notes

Session `1fafb3d2` · Checked 2026-11-16 · Inputs: `data/tournaments.json`, `data/hotels.json`, `data/schedule.json`.

## Ranking method
- Single-entry events are ranked by guarantee ÷ buy-in. A higher figure means more prize pool per dollar entered.
- Bounty events carry a guarantee that includes bounties (sheet 15: "prize pool + total bounties"), so their ratio is not directly comparable to a pure prize pool. The ranking is shown with a note on each row.
- Ties are shown as ties. Ranks 3 to 6 are tied at 66.7x; ranks 7 to 9 are tied at 50x.

## Schedule method
- Each day lists only verified single-entry events, sorted by start time.
- 23 days have at least one verified event. The earliest verified event is Nov 18 at 11:10 AM. The earliest start in the dataset is 10:00 AM (Wynn, Dec 10 and 11), with an unverified entry rule.
- No verified single-entry event starts before 10:10 AM, so the 8 to 10 AM window is free time.

## Hotel cost method
- Only verified values are used. Nothing is inferred.
- Fees are verified for four hotels. No room rate is verified for any hotel, so no true cost per night is stated.

## Risks to the analysis
- Multi-flight events (15 rows) could allow a second entry, which would change the value ranking. They are kept out of the ranking until the poker room confirms.
- The room-tax-on-fee assumption affects only the true-cost column, which is blank.
