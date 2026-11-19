# Live re-read: Venetian DeepStack Extravaganza IV (session 98241f2f, 2026-11-19)

Read-only verification record. **No file under `data/`, `pages/`, `assets/`, `scripts/` or `FLAGGED.md` was changed.**
No row's `last_checked`, value, source or retrieval date was edited; that is for the integration owner, who must
re-read the sources before advancing any date.

## Sources read live (fetched 2026-11-19 UTC from this session, via the page-fetch tool)

| Source | URL | Read result |
|---|---|---|
| Official DeepStack Extravaganza IV event listing (all 4 chunks) | https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html | 94 listed entries, 16 Nov – 23 Dec 2026, each with date, time, event number, name and structure link. Transcribed verbatim to `venetian_dse_iv_listing_2026-11-19.tsv`. |
| Venetian poker room page | https://www.venetianlasvegas.com/resort/casino/poker.html | Lists the current series and room facts. States no entry, re-entry, rebuy or add-on policy for any event. |
| Structure sheet, event numbers 09, 11, 13, 15, 21, 22, 23, 25, 60, 61, 62, 64 | https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_1.pdf | Re-read in full. Contains **no** re-entry, rebuy, add-on or single-entry clause. Event numbers, 5:10 PM start, 25,000 starting chips, 30-minute levels, late registration to 9:40 PM, $8,000 guarantee, $40 fee of $200, 12.5% payout and bounty clauses all match the archived copy `data/snapshots/v_nov_struct_01.txt`. |
| Structure sheet, event 10 (Day 2 clause cited by the dataset) | https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_10.pdf | Re-read in full. Clause 08 is "Any player who bags chips for Day 2 may not play a subsequent flight." Clause 06 is the $60 fee of $300. No freezeout statement. The fields checked (Day A+C 11:10 with Day 2 at 12:00, event 01, 30,000 starting chips, 40-minute levels, late registration about 3:40 PM, $75,000 guarantee, clauses 06 and 08) match the archived `data/snapshots/v_nov_struct_10.txt`. |

## Comparison results (reproducible)

- `compare_venetian_dse_iv.py`: 94 official entries and 94 dataset rows (`series == Venetian DeepStack Extravaganza IV`).
  - Key = (date, start, event number, structure-sheet file). **94 of 94 matched. 0 missing, 0 extra.**
  - Name wording: 5 differences, all wording only (hyphen notes, "Progressive Knock-Out Bounty" vs "PKO", "Double Board Bomb Pot" placement). Not value changes.
    - 2026-11-23 17:10 event 8, 2026-11-28 17:10 event 18, 2026-11-29 12:10 event 20, 2026-12-15 11:10 event 52, 2026-12-17 12:10 event 57.
- `check_values_venetian_dse_iv.py`: buy-in, guarantee and continuation/restart kind, read from each official name.
  **94 of 94 rows checked, 0 mismatches.**

## Findings (none change a published value)

1. **Single-entry evidence is still absent.** The live event listing, the poker room page and the sheets re-read here
   contain no written whole-event one-entry, no-rebuy or no-add-on clause. The archived Venetian sheets agree.
   Current classification (0 SE) therefore stands for the Venetian DSE IV rows.
2. **Transcription note.** In the first chunk the listing is cut mid-row at Saturday 28 November; chunk 2 begins with
   the remainder of that row ("6 | 5:10 PM | 18 | …"). The date in the TSV (2026-11-28) is taken from the cut text
   "Saturday, November 28, 202", which is part of the same row. This is the only reconstructed field.
3. **Not re-read live in this session:** the other 36 November sheets, the 15 December (NYE) sheets, and the NYE listing
   page. These rely on the archived copies from 2026-11-17 and the daily monitor (`.github/workflows/monitor.yml`).
   The sandbox's bash network cannot reach the official hosts; only the page-fetch tool can.

## Limits

- Official pages only. Nothing here is a booking, rate or walking-time check.
- The fetch tool returns page text; visual layout and any gated content are not captured.
- A Google/Apple Maps walking check, a live hotel rate lookup and a Strip-wide tournament search were **not** attempted
  in this session and are not claimed.
