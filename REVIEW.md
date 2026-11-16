# Repo review and source log

Snapshot **2026-11-16**. This page records what was reviewed, what was corrected, and where every fact comes from.

## 1. How the data is produced

| Stage | Script | What it does |
|---|---|---|
| Collect | `scripts/collect_official.py` | Fetches every official URL, extracts facts from official PDFs with `pdftotext`, stores a SHA-256 of each document's visible text, and writes `data/official_facts.json` plus `data/change_log.json` |
| Build | `scripts/build_data.py` | Turns the collected facts plus curated official rows into `data/tournaments.json`, `hotels.json`, `rates.json`, `schedule.json`, `changes.json` |
| Render | `scripts/build_site.py` | Writes `index.html` and every page in `pages/` with the CSS and JS inlined |
| Check | `scripts/check_links.py` | Validates JSON, every local link, every generated page, and that every data row links to an approved official operator domain |

Only the collector touches the network. It runs daily on a schedule (`.github/workflows/monitor.yml`) and commits
its result, so a change on an operator's site becomes visible on this site without any manual step.

## 2. What was reviewed line by line in this session

* **Official Venetian event pages** were parsed row by row. The DeepStack IV page yields 94 printed rows and the
  NYE page 49, including blank date cells that the operator's own event page fills in.
* **Structure sheet links were taken from the event page itself**, not guessed from a filename pattern. 52
  Venetian structure PDFs were downloaded and read; each one's title, event numbers, start time, starting chips,
  level length, late-registration line, guarantee, house fee and clause 8 were extracted verbatim.
* **Entry rules were decided only from the sheet text.** A row is single entry when its sheet prints no re-entry,
  rebuy, add-on, multiple-entry or starting-flight clause. A sheet that prints a cash-entry sentence is re-entry.
  A sheet that prints the multi-flight clause is neither.
* **The WPT structures PDF** was split page by page. 61 events were identified: 29 structure pages with a terms
  page attached, plus the satellites. Every one of them prints unlimited re-entry, so no WPT row is single entry.
* **The Wynn Signature Series structures PDF** was fetched and contains the text "COMING SOON". Those 31 rows are
  therefore unverified and the site says so.
* **Hotel documents** (Venetian resort fee, Venetian hotel terms, Venetian poker suite rates, Wynn terms, Caesars
  disclaimer) were fetched and stored. Only values printed in them are used.

## 3. Corrections made in this session

| Correction | Before | After |
|---|---|---|
| Single-entry count | 33 rows | **88 rows**, each confirmed from its own structure sheet |
| Entry-rule basis | Assumed from a filename list of "multi-flight sheets" | Derived from the sheet's own clause text, quoted on the row |
| House fee | Copied from a hand-maintained table | Read from each sheet's fee sentence; blank when absent or when the sheet covers a different event number |
| Start time per event | Taken from the schedule row only | Cross-checked against the start time printed on the structure sheet |
| "Unverified" label | Applied to whole series without reading the sheets | Removed from every row whose sheet was read and confirmed |
| Hotel data | Single undated value per property | A dated rate log with the printed text, the URL and the retrieval time |
| Walking time | A single blank note | Same-building stays confirmed from official location text; all other walks still blank |
| Sequence test | None | Uses the printed late-registration close, with a 45-minute buffer |
| Change detection | None | Daily hash of every official document, with rows tinted when their source changed |
| Site pages | 11 | 15, with search, date filters, a cost calculator, venue pages and a source monitor |

## 4. Bugs found and fixed during the review

| Bug | Effect | Fix |
|---|---|---|
| Collector's `main()` was truncated by a patch | Facts and change log were never written, so the build silently produced zero verified rows | Rewrote `main()` in one piece and added an offline test that exercises the write path |
| `pdftotext -layout` interleaved two-column rule text with the blind table | Clause 8 was reported as absent on sheets that print it, which would have mislabelled multi-flight events as single entry | Switched to `-layout -raw` and matched clause 8 by pattern, never treating a missing parse as permission |
| Signature Series rows parsed with a fixed year | Dates came out as 2028 | Year is derived from the schedule's own season |
| HTML hash included rotating markup | Every daily run reported a change on every HTML page | The hash is now taken over the visible text, not the raw markup |
| `.gitignore`-free facts file never committed | The site could not show collected facts | The workflow commits `data/official_facts.json`, `data/change_log.json` and the rebuilt pages |

## 5. Checks that ran before publication

```
python3 scripts/collect_official.py    # fetch, extract, hash  (runs in CI; needs poppler-utils)
python3 scripts/build_data.py          # regenerate data/*.json
python3 scripts/build_site.py          # regenerate index.html and pages/*.html
python3 scripts/check_links.py         # JSON, local links, generated pages, official source hosts
```

All four pass. `check_links.py` also fails the build if a generated page is missing or a stale page is left behind,
so the published site cannot drift from its generator.

## 6. Source log

| Source | Domain | Used for | Retrieved |
|---|---|---|---|
| [DeepStack IV event page](https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html) | venetianlasvegas.com | 76 rows, dates, times, buy-ins, guarantees, structure links | 2026-11-16 |
| [DeepStack NYE event page](https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-dec-2026.html) | venetianlasvegas.com | 31 rows and structure links | 2026-11-16 |
| [DeepStack series overview](https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament.html) | venetianlasvegas.com | series date ranges and headline guarantees | 2026-11-16 |
| Venetian structure sheets 1–37 (IV) and 1–15 (NYE) | venetianlasvegas.com | entry rules, house fees, level data, late-registration times | 2026-11-16 |
| [Venetian poker room](https://www.venetianlasvegas.com/resort/casino/poker.html) | venetianlasvegas.com | poker room location (The Palazzo, level 2), parking | 2026-11-16 |
| [Venetian poker suite rates](https://www.venetianlasvegas.com/resort/casino/poker/suite-rates.html) | venetianlasvegas.com | $119/$209 range, $55 resort fee, play requirement, booking code | 2026-11-16 |
| [Venetian resort fee](https://www.venetianlasvegas.com/resort/resort-fee.html) | venetianlasvegas.com | $55 per night plus tax | 2026-11-16 |
| [Venetian hotel terms](https://www.venetianlasvegas.com/legal/hotel-terms-and-conditions.html) | venetianlasvegas.com | 13.38% Clark County room tax, taxed resort fee | 2026-11-16 |
| [Wynn poker room](https://www.wynnlasvegas.com/casino/poker) | wynnlasvegas.com | series dates, links to the official PDFs | 2026-11-16 |
| [WPT schedule](https://cdn.wynnresorts.com/image/upload/v1757097329/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Schedule.pdf) | cdn.wynnresorts.com | 87 WPT rows | 2026-11-16 |
| [WPT structures and terms](https://cdn.wynnresorts.com/image/upload/v1750864036/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Structures.pdf) | cdn.wynnresorts.com | 61 event terms pages, re-entry rules, fee breakdowns | 2026-11-16 |
| [Wynn Signature Series schedule](https://cdn.wynnresorts.com/image/upload/v1753296112/visitwynn_pdfs_files/Poker/Wynn%20Signature%20Series/Wynn_Signature_Series_Schedule.pdf) | cdn.wynnresorts.com | 34 printed rows, 31 of which are events | 2026-11-16 |
| [Wynn Signature Series structures](https://cdn.wynnresorts.com/image/upload/v1762299460/visitwynn_pdfs_files/Poker/Wynn%20Signature%20Series/Wynn_Signature_Series_Structures.pdf) | cdn.wynnresorts.com | fetched; contains only "COMING SOON" | 2026-11-16 |
| [Wynn daily tournament poster](https://cdn.wynnresorts.com/image/upload/v1752011166/visitwynn_pdfs_files/Poker/Daily%20Tournaments/poker-daily-tournament-poster.pdf) | cdn.wynnresorts.com | daily event types and the suspension note | 2026-11-16 |
| [Wynn terms and conditions](https://www.wynnlasvegas.com/terms-and-conditions/848671) | wynnlasvegas.com | $55 daily resort fee plus tax | 2026-11-16 |
| [Caesars corporate disclaimer](https://www.caesars.com/corporate/disclaimer) | caesars.com | resort-fee range only ($45–$50) | 2026-11-16 |
| [Bellagio](https://bellagio.mgmresorts.com/en.html) | bellagio.mgmresorts.com | property identification only; no fee value | not retrieved (timeout) |
| [ARIA](https://aria.mgmresorts.com/en.html) | aria.mgmresorts.com | property identification only; no fee value | not retrieved (timeout) |

## 7. Known limits of this review

* The WPT structure sheets are grouped: one terms page is shared by many rows of the same event (for example the
  Turbo sheet lists eight separate dates). Re-entry is printed per event, not per date, and the site classifies at
  event level.
* Venetian structure sheets frequently cover several event numbers at once (sheet 1 covers twelve). The fee is
  applied only when the sheet's printed buy-in matches the row's buy-in.
* Money values are taken as printed. Where a sheet prints a rake discount for early entry, the base fee is
  recorded and the discount is kept in the note rather than folded into the fee.
* Finish times are estimates from level count and level length. The operator prints none.
* No third-party price, rating, walk time or schedule is used anywhere in the data.
