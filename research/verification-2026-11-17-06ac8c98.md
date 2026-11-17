# Session 06ac8c98 — schedule-feasibility re-verification (2026-11-17)

Task: the day plan required by the brief ("use start time, late-registration cutoff and plausible event
duration to flag overlapping entries; give each day a primary event and a conditional fallback, not an
impossible sequence" and "once finish times are verified, flag any two events that cannot be played in
sequence"). This page records what was reproduced, what was read from official sources, and what changed.

## 1. Defect reproduced on pristine `main` (`5de6d8d`), before any edit

Recomputed from the committed `data/tournaments.json` against the committed `data/schedule.json`:

| Measure | On `main` | Expected |
|---|---|---|
| Conditional fallbacks published | 24 | 0 provable |
| …of which unplayable (primary still running when the fallback's entry closes) | **24 of 24** | 0 |
| Scheduled rows printing a finish **earlier** than their own start | **121 of 274** | 0 |
| Overlap pairs flagged | 14 | 144 |

Cause, line by line, in `scripts/build_data.py`:

```python
if to_min(cand["start"]) >= to_min(primary["est_end"]):      # old
```

`est_end` is stored as a time of day (`to_hhmm` applies `% 1440`). An event starting 11:10 with a
945-minute structure is stored as `02:55`, so the test read `175 >= 1615` inverted: it approved the
impossible pairs and rejected the possible ones. `EXECUTIVE_SUMMARY.md` repeated "no impossible sequence
is proposed" while all 24 were impossible.

## 2. Official sources read for this task (all fetched live, 2026-11-17)

| Source | What was checked | Result |
|---|---|---|
| [DeepStack Extravaganza IV event page](https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html) | Nov 25 rows: Event 10 at 11:10 AM, Event 11 at 5:10 PM, Event 7 Day 2 Restart at 11:00 AM; the "(1Day)" labels; the structure links | Matches `r016`, `r017` and the continuation row exactly. Continuations stay out of the day plan. |
| [Structure sheet #6](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_6.pdf) | Event 10 level table, start 11:10 AM, "Late Registration: 10 levels + Break (~ 4:55 PM)", clause 7 | 28 levels × 30 min with breaks after 4, 8, 10, 14, 18, 22, 26 = 945 min. The generator reproduces the printed 4:55 PM clock exactly (10 × 30 + 3 × 15), so the break model is right. Clause 7: "This event pays 12.5% of the field". **No end time is printed.** |
| [Structure sheet #2](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_2.pdf) | Event 7 (flights 1A/1B): level table, clause 3, clause 8 | Title prints "Day A+B @ 11:10 AM with Day 2 @ 11:00 AM"; clause 3: "Each starting flight will play until we are down to approximately 12.5% of the field remaining. Day 2 will resume at 11:00 AM … the clock will revert to the earliest stoppage time of Day 1"; clause 8: "Any player who bags chips for Day 2 may not play a subsequent flight." 30 levels × 40 min therefore spans **two** playing days. |
| [Structure sheet #4 (Dec series)](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_dec_2026-structure_4.pdf) | Milestone satellite conclusion rule | Clause 10: "The tournament will conclude when the number of players remaining is equal to the remaining number of … direct entry seats to be awarded, less the number of Milestone … seats already awarded previously." Clause 9 lets a player reach the Milestone and stop even earlier. |
| Archived snapshots `data/snapshots/v_nov_struct_*.txt`, `v_dec_struct_*.txt` | Every one of the 20 satellite rows with a structure end time | **20 of 20** sheets print the "will conclude when the number of players remaining" clause, so the satellite treatment is sourced for the whole set, not inferred from one. |

No value in the dataset was changed by this task: `data/tournaments.json` is byte-identical after the
rebuild, and `data/row_snapshot.json` / `data/row_verification.json` are unchanged (317 rows, 1,296
field checks, 0 hard failures, 1 documented review item).

## 3. The rule now applied, and why

A printed level table bounds an event from **above**. It never proves a clock. So:

| Basis (stored per scheduled event) | Applied to | Reason in the source |
|---|---|---|
| `day_maximum` | 73 rows | Name says "(1Day)", so the table is that day's table; ends when 12.5% of the field is paid, which no source times. |
| `satellite_maximum` | 20 rows | Clause 10 concludes the field when the seats are awarded; the table is a ceiling only. |
| `no_day_bound` | 34 rows | Clause 3: the flight ends at ~12.5% of the field and "Day 2 will resume" the next day, so the table spans more than one day. Refused as a same-day bound. |
| *(no `est_end`)* | 147 rows | No structure sheet was published for the row. Nothing is estimated. |

Consequences published on the schedule page:

- a fallback is named only when the primary's table ends before the second event's entry closes
  (labelled "from the start", or "join in progress" when it lands inside the late-registration window);
- a pair is flagged `unplannable` when the earlier event's table runs past the later event's entry
  deadline, and `join_in_progress` when it passes that start but not the deadline;
- 142 `unplannable` + 2 `join_in_progress` pairs on 39 dates; 0 publishable fallbacks; 26 dates carry 35
  alternatives, each labelled as a choice to play **instead of** the primary and never as well;
- 45 of 70 dates have a primary; 25 have no verified single-entry event at all.

## 4. Irregularities raised

- **F75** — 70 of the 73 "(1Day)" rows carry a table that cannot fit inside a day (e.g. a 17:10 start with
  28 × 30-minute levels plus seven 15-minute breaks ends at 08:55 next morning). The label and the table
  contradict each other, which is what forces "maximum" wording everywhere. Published in `FLAGGED.md`.
- **F76** — the generator defect in §1, its measured effect, and the fix. Published in `FLAGGED.md`.

## 5. Guards added, with negative tests

`scripts/check_schedule.py` re-derives the plan from `data/tournaments.json` with its own implementation
and fails on: a clock that disagrees with its duration, a wrong next-day marker, a duration basis that
disagrees with the row's own name and labels, an unenterable fallback, a missing primary, a missing
alternatives entry, a non-single-entry alternative, an `entry_closes` that does not match the row, an
unflagged playable-or-unplayable pair, and a wrong per-day count.

`scripts/smoke_test.js` additionally reads the **rendered** schedule page and fails if any event line shows
a finish before its start with no next-day marker, or if the alternatives block or the phrase "no published
schedule" is missing.

Negative tests run against the generated page:

| Injection | Result |
|---|---|
| Flip one `est_end_next_day` to `false` in `data/schedule.json` | `check_schedule` → 1 problem, exit 1 |
| Attach a fallback to a day whose primary ends after midnight, and wipe that day's conflicts | `check_schedule` → 3 problems (unenterable fallback, unflagged pair, wrong count), exit 1 |
| Remove the " (next day)" branch from the rendered page | `smoke_test` → FAIL: "17 rendered event line(s) show a finish before their start with no next-day marker" |
| Restore each | all green again |

## 6. Full check suite after the change

```
python3 scripts/build_data.py      317 rows (SE 80 / MULTI 67 / RE 107 / UNV 38 / CONT 25), 274 entry
                                   rows over 70 dates, 70 schedule days, 79 flagged rows
python3 scripts/build_site.py      23 pages; committed pages identical to a fresh rebuild
python3 scripts/check_links.py     OK (56 files free of conflict markers, sources, rules, schedule, rates, links)
python3 scripts/check_schedule.py  OK (70 days, 274 entry rows, 144 overlap pair(s))
python3 scripts/verify_rows.py     324 rows, 1,296 field checks, 0 hard failures
python3 scripts/monitor_sources.py not run here: the sandbox has no route to the operator hosts (see F55).
node   scripts/smoke_test.js       23/23 pages rendered
```
