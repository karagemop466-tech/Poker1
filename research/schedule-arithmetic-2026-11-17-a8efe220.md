# Schedule overlap arithmetic — fix and verification record

Session `a8efe220` · Branch `arena/a8efe220-poker1` (base `5de6d8d` = `main` at PR #69) · 2026-11-17

## 1. What was wrong, measured on `main` before the fix

`est_end` is stored on every tournament row as a wall-clock `HH:MM` (`scripts/build_data.py`,
`estimate_end` → `to_hhmm`). `to_hhmm` takes the result modulo 24 hours, so an event that starts at
11:10 AM and is estimated to run 15 hours stores `02:25` — a time that reads **earlier** than its own
start. `build_schedule` then compared those stored strings as minutes-since-midnight.

Reproduced on `main` at `5de6d8d` by recomputing each day from `data/tournaments.json`
(`start + est_duration_min`) and comparing against the published `data/schedule.json`:

| Check | Result on `main` |
|---|---|
| Conditional fallbacks proposed | 24 |
| …of which the fallback starts **before** the primary's estimated finish | **24 of 24** |
| Days with 2+ verified single-entry events | 26 |
| Real overlapping row-pairs (absolute minutes) | 245 |
| …flagged in `data/schedule.json` | **14** |
| …left unflagged | **231** |
| Rows whose printed `est_end` reads before their own `start` | **137 of 317** |

This defect had already been published on the site as a *request* to the owning sessions by session
`206debc0` (recorded in `COORDINATION.md`, "REQUEST 1"). No session had fixed it; the generator was
claimed at the time. It was still live on `main` when this session started, so it was claimed and fixed
here.

No new source was read and no tournament, hotel, rate, walking or entry-rule value was changed. This is
arithmetic over values already stored and already verified against the official documents by
`scripts/verify_rows.py` (1,296 field checks) and `scripts/verify_against_snapshots.py` (0 unexplained
mismatches). Both were re-run after the change and are unchanged.

## 2. What changed

1. **`scripts/build_data.py` — `end_minutes(row)` (new).** Returns `to_min(start) + est_duration_min`, an
   absolute count of minutes from midnight of the row's own date, or `None` when no duration is stored.
   An unknown duration is never treated as a known one.
2. **`scripts/build_data.py` — `build_schedule`.** Every comparison now uses `end_minutes`. A conditional
   fallback is proposed only when the primary's finish is known, does **not** cross midnight, and the
   candidate starts on the same date at or after that finish. Overlaps are detected with the same rule
   the validator uses: two events printed with the same start time overlap by definition, otherwise the
   pair overlaps when the earlier event's known finish reaches past the later event's start. Each pair is
   reported once. The finish is rendered as `"HH:MM the next day"` when it crosses midnight.
3. **`data/schedule.json`.** Each scheduled event gains `est_end_next_day` (boolean, `true` exactly when
   the absolute finish is 1,440 minutes or more) and each conflict gains `a_start`, `a_end` and `b_start`
   so a reader can check the arithmetic without leaving the row. The file gains a top-level
   `overlap_pairs` count. `fallback_note` now says "later on this date", because a next-day start is not
   proposed.
4. **`assets/app.js`.** The one place that prints an estimated finish now appends "the next day" when
   `est_end_next_day` is true, so 121 rows stop reading as if they finish before they start.
5. **`scripts/check_links.py`.** New schedule-arithmetic block with four rules, each of which fails the
   build with the date and event ids:
   - a fallback that starts before the primary's estimated finish, or is proposed at all while the
     primary's finish is unknown or falls on the next day;
   - a real overlap that is not published;
   - a published overlap that is not real, or the same pair published twice;
   - an event whose `est_end_next_day` disagrees with its absolute finish.
6. **Documents.** `EXECUTIVE_SUMMARY.md` §5 (the "24 days also name a conditional fallback" and "14
   row-pairs on two days" claims were both false as a result of this bug and are now corrected with the
   reason), `SUGGESTIONS.md` S17, `README.md`, `QUESTIONS.md` (new section F, three questions),
   `FLAGGED.md` (new **F62**), and a duplicate flag id (**F58** had been used by two parallel sessions;
   the conflict-marker row is now **F61**).

## 3. Verification performed

| Check | Result |
|---|---|
| `python3 scripts/build_data.py` | 317 rows (SE 80 / MULTI 67 / RE 107 / CONT 25 / UNV 38), 70 schedule days, 79 flagged rows — unchanged |
| Fallbacks that cannot be reached | **0** (was 24 of 24) |
| Real overlaps vs published overlaps | **271 published, 271 real** — every real pair flagged, none invented |
| Events marked `est_end_next_day` | 121 (matches the independent count of absolute finishes ≥ 1,440) |
| `python3 scripts/build_site.py` | 23 pages, byte-identical on a second run (idempotent) |
| `python3 scripts/check_links.py` | OK — 56 files free of conflict markers, 23 pages, 317 rows, 7 hotels, 5 dated rates, 70 schedule days |
| `python3 scripts/verify_rows.py` | 1,296 field checks, **0 hard failures**, 1 documented review item (unchanged) |
| `python3 scripts/verify_against_snapshots.py` | **0 unexplained mismatches** (unchanged) |
| `npm run test:smoke` | 23 of 23 pages rendered headlessly |

**The four new validator rules were each proven to fire** by deliberately corrupting
`data/schedule.json` and re-running the check, then restoring it:

| Corruption | Message produced |
|---|---|
| Invented a fallback on a day whose primary has no stored duration | `fallback 'r025' is proposed but the primary 'r020' has no stored duration` |
| Deleted one conflict from a day that had four | `unflagged overlap between ['r021', 'r025']` |
| Cleared `est_end_next_day` on `r001` (absolute finish 1,975 min) | `event 'r001' est_end_next_day must be True (estimated finish at minute 1975)` |
| Left as published | `check_links: OK` |

## 4. The honest result: no fallback survives

After the fix **no date carries a conditional fallback**, on all 70 dates. This is a finding, not a
regression. On each of the 26 dates that offer two verified single-entry events, the earlier one is
estimated to run 11 to 21 hours, because the Venetian and WPT structures print 15-, 16- or 21-hour
sessions and the estimate assumes the event plays to its scheduled length. Examples:

| Date | Primary | Est. finish | Second single-entry event | Its start |
|---|---|---|---|---|
| 2026-11-25 | r016, 11:10 | 02:55 the next day | r017 | 17:10 |
| 2026-11-28 | r027, 11:10 | 02:55 the next day | r029 | 12:10 |
| 2026-12-11 | r114, 11:10 | 02:55 the next day | r116 | 16:10 |

The estimate is an **upper bound** — it assumes the event runs to its scheduled length, which small
fields do not. That is why the previous version could show a plausible-looking fallback and this version
shows none: the fallback was only ever reachable because the arithmetic had wrapped. See `QUESTIONS.md`
Q-F1 and Q-F2: the missing fact that would let the site publish a realistic evening option is a typical
field size and finish time, which no official source publishes in advance.

## 5. What is still open (published, not hidden)

- **Q-F1/Q-F2/Q-F3** in `QUESTIONS.md`: field size and actual duration, whether to adopt a labelled
  duration assumption, and whether a cross-midnight finish should block the following date's plan. The
  site checks overlaps **within** a date only; chaining a next-day finish into the next date is a
  deliberate non-goal while the finish is an upper bound, because it would block days on a guess.
- The six open pull requests (#46, #51, #52, #53, #64, #66) are all `CONFLICTING` against `main` and none
  of them touches this defect. They are not reviewed or merged here.
- No source was re-read this session, so no `last_checked` value was advanced and no flag was created or
  altered apart from the F58→F61 renumbering and the new F62.
