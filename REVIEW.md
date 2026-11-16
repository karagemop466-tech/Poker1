# Repo Review and Verification Log (T1)

Session `1fafb3d2` · Branch `arena/1fafb3d2-poker1` (base `c16071b`, from `main`) · Checked 2026-11-16

## 1. Repository state

| Item | Result | Evidence |
|---|---|---|
| Files on `main` | Only `README.md` (`# Poker1`) | `git ls-tree -r main` |
| Commits on `main` | One commit, `c16071b` | `git log` |
| `COORDINATION.md` | Not on `main`. Created on this branch (`bc212f8`). | `git show origin/main:COORDINATION.md` returns nothing |
| GitHub Pages | Enabled. Legacy build, source `main` `/`, status `built`. | `gh api repos/karagemop466-tech/Poker1/pages` |
| Other session branches | `arena/85820f64-poker1`, `arena/ce95f9c0-poker1`, `arena/e73e692a-poker1` each claim overlapping scope. | `git ls-remote origin`; their `COORDINATION.md` files, read only |

## 2. Irregularities found

| # | Area | Irregularity | Source | Impact / status |
|---|---|---|---|---|
| R1 | Coordination | Three other branches claim the same scope, so the task board is split across branches. | Their `COORDINATION.md` files | Possible merge conflicts. This session did not edit them. |
| R2 | Coordination | The workspace pins one branch, so the `session-<id>/<task>` branch naming in the protocol cannot be followed. | `COORDINATION.md` protocol notes | Process only. Noted on the board. |
| R3 | Venetian NYE page | Event 5 (Dec 26) is printed as "Saturday, December 26, 2025". The series runs 2026 to 2027. | [NYE event page](https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-dec-2026.html) | Year flagged. Row kept with a flag. |
| R4 | Venetian NYE page | Typo "Tuesaday" (Jan 5, 2027). | Same page | Cosmetic |
| R5 | Venetian DSE IV schedule | "(IDAY)" printed where "(1DAY)" is meant, on many rows. | [DSE IV schedule PDF](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/dse-nov-2026-schedule.pdf) | Cosmetic. Event names are kept as printed in the source. |
| R6 | Venetian DSE IV event page | "No LImit Hold'em" on events 2, 6, 10, 12. | [DSE IV event page](https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html) | Cosmetic |
| R7 | Wynn WPT schedule | "BadugI" for Badugi, and "NIH" printed where NLH is meant (for example "NIH Turbo", "Ladies NIH Championship"). | [WPT schedule PDF](https://cdn.wynnresorts.com/image/upload/v1757097329/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Schedule.pdf) | Cosmetic. Names are kept as printed. |
| R8 | Venetian PDF date cells | Some rows have a blank date cell (LIPS and PokerAtlas overlay rows: events 17, 18, 32, 36, 39, 40, 43-49, 58). | DSE IV schedule PDF | The official event page prints a date on every row. The dates were taken from that page. Event 49 was wrong in the draft (Dec 12/13) and is corrected to Dec 13/14. |
| R9 | Venetian flight events | Structure sheets for events 1, 7, 19 and 26 (sheets 2, 3, 9, 10, 12, 13, 14) carry clause 08: "Any player who bags chips for Day 2 may not play a subsequent flight." The clause does not say whether a player who busts may enter a later flight. | Sheets listed in FLAGGED.md | 15 rows moved from single entry to the separate section. |
| R10 | Venetian structure sheet 8 | Wording on the PokerAtlas discount reads "all subsequent buy in's ... $200", which may imply a second buy-in. | [Structure 8](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_8.pdf) (from session log; not re-read this session) | Rows 18 and 58 kept as unverified. |
| R11 | Venetian bounty sheets | Sheet 15: "Guarantee: $15,000 (prize pool + total bounties)." Each bounty pays $100 per elimination. | [Structure 15](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_15.pdf) | A bounty guarantee is not a pure prize pool. Flagged on the bounty rows. |
| R12 | Wynn WPT footnotes | Footnote *** says ClubWPT Gold adds $1,000,000 and "is not available in Nevada." Footnote **** gives a $11,100 ladies tournament entry with a discounted ladies entry. | [WPT schedule PDF](https://cdn.wynnresorts.com/image/upload/v1757097329/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Schedule.pdf) | Printed as-is and flagged. Confirmation needed. |
| R13 | Wynn WPT $600 NLH $400K | Unlimited re-entry for each starting flight until level 9. | [WPT structures PDF](https://cdn.wynnresorts.com/image/upload/v1750864036/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Structures.pdf) (pages 1-2 read) | Moved to the separate section. |
| R14 | Caesars Palace fee | Official corporate disclaimer gives a general "$45-$50 plus tax" range. Third-party values conflict. | [Caesars disclaimer](https://www.caesars.com/corporate/disclaimer) | Left blank. |
| R15 | Bellagio fee | No official MGM page found. Third-party values conflict ($45, $50, $55). | Third-party only | Left blank. |
| R16 | ARIA fee | Official home page fetched. No resort-fee terms found on it. | [ARIA home page](https://aria.mgmresorts.com/en.html) | Left blank. Row added. |
| R17 | Venetian room tax | 13.38% Clark County room tax comes from a search excerpt of the Venetian hotel terms. The terms do not say whether it applies to the resort fee. | [Venetian hotel terms](https://www.venetianlasvegas.com/legal/hotel-terms-and-conditions.html) (excerpt) | Tax-on-fee assumption flagged (F10). |
| R18 | Venetian poker suite page | "Start as low as $119 and $209" for the Venetian or Palazzo, conditional on play. It does not say which rate belongs to which property. | [Poker suite rates](https://www.venetianlasvegas.com/resort/casino/poker/suite-rates.html) | Not used as a room rate. |
| R19 | Time-sensitive | The first verified single-entry Venetian event is Nov 18, 11:10 AM. The Nov 16 and 17 events are multi-flight rows. | DSE IV event page | Confirm before travel. |
| R20 | Coverage | No verified 2027 Las Vegas WSOP Circuit schedule. Search returned leads only. | Search only | Gap. See QUESTIONS.md. |

## 3. Corrections made during this review

Claims in the earlier drafts were checked against the official text. These were removed or corrected:

| Earlier claim | What the source says | Action |
|---|---|---|
| Wynn registration opens 4 hours before start | Not found in any official text read. | Removed. The schedule prints a REG CLOSES time per event. |
| Venetian event 58 date "Dec 19 from row position" | Event page prints Sat Dec 19, 5:10 PM. | Confirmed. |
| Event 49 Seniors 1A on Dec 12 | Event page prints Sun Dec 13 (1A) and Mon Dec 14 (1B). | Corrected. |
| Two WPT rows missing from the draft | Schedule prints HORSE $800 and PLO 6-Max $10,500 on Dec 18 at 1 PM. | Added. |
| Typos "No LImit" on DSE IV schedule | Printed on the event page, not on the schedule PDF. | Re-attributed (R6). |
| "$197.28 per night" example | Used unverified inputs. | Removed. |
| "Venetian walk time 0 min" | No official source. | Set to blank. |
| Palazzo "connected at casino level" | Not in any source read. | Removed. |
| Venetian "payable at check-in" | Not in any source read. | Removed. |
| WSOP "March and July 2026" | Not checked against a source. | Replaced by R20. |
| Hotel "true cost" formula taxing the fee | Assumption. The official source does not confirm it. | Labelled as an assumption (F10). |

## 4. Verification method

1. Primary sources only (venue or operator domains). Third-party sites were used to find events and hotels, never as a value source.
2. Each row is copied from the official schedule or event page. Buy-in and guarantee come from those pages.
3. Single-entry status requires the official structure sheet to be read. The sheet must show no re-entry, rebuy or add-on language and no flight clause.
4. Hotel resort fees come from official pages or official excerpts. Where only an excerpt was read, it is labelled "search excerpt".
5. Missing or conflicting values are left blank and flagged. Nothing is inferred.

## 5. Source log

| Source | URL | Read how | Used for |
|---|---|---|---|
| Venetian DSE IV schedule (PDF) | https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/dse-nov-2026-schedule.pdf | Chunks 0-1 | All DSE IV rows |
| Venetian DSE IV event page | https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html | Chunks 0-2 of 4 (chunk 3 not read) | Explicit dates and structure links |
| Venetian DSE NYE event page | https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-dec-2026.html | Chunks 0-1 | NYE rows |
| Venetian DSE IV structure sheets: 1, 2, 3, 5-17 | https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_{N}.pdf | Read (earlier session) | Single-entry checks, house fee |
| Structure sheets 2, 3, 9, 10, 12, 13, 14, 15 | same pattern | Read this session | Clause 08 check; house fee for sheet 15 |
| Venetian DeepStack home | https://venetianpokerroom.blog/ | Read | Navigation only |
| Wynn WPT World Championship schedule (PDF) | https://cdn.wynnresorts.com/image/upload/v1757097329/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Schedule.pdf | Chunks 0-1 | WPT rows, footnotes, phone and website |
| Wynn WPT structures (PDF) | https://cdn.wynnresorts.com/image/upload/v1750864036/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Structures.pdf | Chunks 0-1 of 8 | $600 NLH re-entry terms |
| Wynn Signature Series schedule (PDF) | https://cdn.wynnresorts.com/image/upload/v1753296112/visitwynn_pdfs_files/Poker/Wynn%20Signature%20Series/Wynn_Signature_Series_Schedule.pdf | Read | Signature Series rows |
| Wynn poker page | https://www.wynnlasvegas.com/casino/poker | Read (earlier session) | Series dates |
| Wynn terms (resort fee) | https://www.wynnlasvegas.com/terms-and-conditions/848671 | Search excerpt | Fee $55 plus tax |
| Venetian resort fee | https://www.venetianlasvegas.com/resort/resort-fee.html | Search excerpt | Fee $55 plus tax |
| Venetian hotel terms | https://www.venetianlasvegas.com/legal/hotel-terms-and-conditions.html | Search excerpt | 13.38% room tax |
| Venetian poker suite rates | https://www.venetianlasvegas.com/resort/casino/poker/suite-rates.html | Read (earlier session) | Conditional suite rates; $55 fee |
| Caesars disclaimer | https://www.caesars.com/corporate/disclaimer | Search excerpt | General fee range |
| ARIA home page | https://aria.mgmresorts.com/en.html | Read | Official domain; no fee terms found |

Third-party sites (vegaspokercalendar.com, pokernews.com, pokerfuse.com, mttdb.com, pokeratlas.com, pokerscout.com and others) were used to locate events and hotels only. They are not cited on any row.

## 6. Build and data checks

- `scripts/build_data.py` regenerates `data/tournaments.json`, `data/hotels.json` and `data/schedule.json` from the rows in the script.
- `scripts/check_links.py` checks that the site's local links and JSON files resolve.
- Current counts: 225 official rows. Single entry 33 (Venetian DSE IV). Separate section 21 (15 possible multi-entry, 6 re-entry). Unverified 171.
- Unique row IDs: checked (`r001`-`r225`).
