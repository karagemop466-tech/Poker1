# T2: Tournament research log

Session `1fafb3d2` · Checked 2026-11-16 · Output: `data/tournaments.json` (225 rows), built by `scripts/build_data.py`.

## Scope
- Live, upcoming, Las Vegas Strip events from official schedules only: The Venetian (DeepStack Extravaganza IV, DeepStack NYE) and Wynn Las Vegas (WPT World Championship, Wynn Signature Series).
- Single entry is confirmed only when the structure sheet has been read and shows no re-entry, rebuy, add-on or flight clause.

## Method
1. Schedule rows copied from the official PDFs and event pages. Where a PDF date cell is blank, the official event page supplies the date. Event 49 was corrected to Dec 13/14 this way.
2. Structure sheets read for single-entry checks: Venetian DSE IV sheets 1, 2, 3, 5 to 17 (earlier session), plus 2, 3, 9, 10, 12, 13, 14, 15 (this session).
3. Clause 08 ("Any player who bags chips for Day 2 may not play a subsequent flight") found on sheets 2, 3, 9, 10, 12, 13, 14. Those events go to the separate section.
4. WPT rows checked against the official schedule text (chunks 0 and 1). Two rows were missing and were added (Dec 18 HORSE $800, PLO 6-Max $10,500).

## Counts
| Series | SE | Possible multi-entry | RE | Unverified | Total |
|---|---|---|---|---|---|
| Venetian DeepStack IV | 33 | 15 | 0 | 28 | 76 |
| Venetian DeepStack NYE | 0 | 0 | 0 | 31 | 31 |
| Wynn WPT World Championship | 0 | 0 | 6 | 81 | 87 |
| Wynn Signature Series | 0 | 0 | 0 | 31 | 31 |
| **Total** | **33** | **15** | **6** | **171** | **225** |

## Not yet done (see QUESTIONS.md)
- Structure sheets for the NYE series, the Signature Series, the WPT events other than the $600 NLH $400K flight, and DSE IV sheets 4 and 18 to 37.
- Entry-rule confirmation for the 171 unverified rows.
