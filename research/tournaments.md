# T2: Tournament research log

Session `baba1a15` · Checked 2026-11-16 · Output: `data/tournaments.json` (316 rows), built by `scripts/build_data.py`.
The field-by-field structure-sheet log is in `research/structure-sheets-verification.md`.

## Scope
- Live, upcoming, Las Vegas Strip events from official schedules only: The Venetian (DeepStack Extravaganza IV,
  DeepStack Extravaganza NYE) and Wynn Las Vegas (WPT World Championship, Wynn Signature Series).
- Single entry is confirmed only when the structure sheet has been read and shows no re-entry, rebuy, add-on or
  flight clause.

## Method
1. Schedule rows copied from the official event pages and schedule PDFs. Where a PDF date cell is blank, the
   official event page supplies the date.
2. **Every** Venetian structure sheet was read directly on 2026-11-16: 37 of 37 for DeepStack Extravaganza IV and
   15 of 15 for the New Year's Eve series. The sheet-to-event mapping is taken from the sheet header, not from
   position in a list.
3. All eight sections of the Wynn WPT structures PDF were read, which covers the $600 NLH, $800 NLH, $1,600 NLH,
   WPT Prime, PLO Mystery Bounty, $600 NLH Turbo, $400 PLO, $1,100 PLO, TORSE, Mixed Triple Draw, HORSE,
   Limit Omaha 8 and Limit Omaha 8/Stud 8 structures. The PDF publishes no sheet for the milestone and satellite
   events, so those rows stay unverified on the entry rule.
4. The Wynn WPT schedule was rebuilt row by row from the official PDF for Nov 27 – Dec 21, 2026, including the
   Day 2 / Day 3 / Day 4 / final-table continuation rows and the published chip counts and level counts.
5. The Wynn Signature Series schedule was transcribed in full for Jan 11 – 24, 2027. The official structures PDF
   is a "COMING SOON" placeholder, so those rows stay unverified.
6. Where two official sources disagree, both values are kept and the row carries the conflict as a flag.

## Counts
| Series | SE | Possible multi-entry | RE | Unverified | Continuation | Total |
|---|---|---|---|---|---|---|
| Venetian DeepStack IV | 54 | 38 | 0 | 0 | 2 | 94 |
| Venetian DeepStack NYE | 26 | 22 | 1 | 0 | 0 | 49 |
| Wynn WPT World Championship | 0 | 0 | 44 | 91 | 0 | 135 |
| Wynn Signature Series | 0 | 0 | 0 | 38 | 0 | 38 |
| **Total** | **80** | **60** | **45** | **129** | **2** | **316** |

Of the 80 verified single-entry rows, 60 award cash and 20 are milestone satellites that award a seat into a
bigger event. Those 20 rows carry a `prize_text` value and a `satellite` label instead of a dollar guarantee.

## Still open (see QUESTIONS.md)
- Entry-rule confirmation for the 129 unverified rows: 91 Wynn WPT rows (no structure sheet is published for the
  milestone satellites and the remaining events) and 38 Wynn Signature Series rows (the official structures PDF is
  still a placeholder).
- Whether a player who busts from one flight may enter a later flight. 60 rows depend on the answer.
- Whether the WPT $1M ClubWPT addition is paid to Nevada players, and what a ladies player actually pays for the
  $11,100 ladies championship entry.
- The December 21 $600 NLH Turbo start time: the schedule PDF prints 8 p.m. and the structure sheet prints 6 p.m.
