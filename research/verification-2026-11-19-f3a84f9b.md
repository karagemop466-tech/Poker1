# Verification record — session f3a84f9b, 2026-11-19

Scope: dated official re-reads behind the claims "read every structure sheet and remove the
'unverified' label from each event that is confirmed", "keep rates as a dated log" and
"automatic re-check of each official URL". Nothing in this file was inferred; every line names
the official document and the time it was read.

## Sources re-read on 2026-11-19 (UTC)

| Official source | Read at | Result |
|---|---|---|
| [Venetian DeepStack Extravaganza IV November schedule page](https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html) | 10:53Z | Every Nov 18 – Nov 28 line printed today matches the archived capture `data/snapshots/v_dse_nov_page.txt` and the dataset rows: Wed Nov 18 Event 2 $300 $10K GTD 11:10 (sheet 5); Thu Nov 19 10:10 $200 RaceDay sheet 18; Fri/Sat Nov 20/21 same RaceDay; Sun Nov 22 11:10 $200 sheet 29; Mon Nov 23 11:10 $400 1A $75K sheet 2 + 5:10 $200 PKO $8K sheet 30; Tue Nov 24 11:10 $400 1B + 5:10 $200 Bounty $8K sheet 1; Wed Nov 25 11:00 $400 Day 2 Restart + 11:10 $400 $15K sheet 6 + 5:10 Bounty; **Thu Nov 26 11:10 Event 12 $300 $10K GTD (1Day) sheet 5 + 5:10 PM $200 Bounty $8K sheet 1**; Fri Nov 27 11:10 $600 $30K sheet 7 + 5:10 Bounty; Sat Nov 28 11:10 $600 Bounty $30K sheet 11 + 12:10 $400 PLO Bounty $15K sheet 26. No value moved, so no `last_checked` advance was made on Venetian rows from this read (the page is the *same content* re-rendered; the monitor records it as cosmetic). |
| [Structure sheet #5 (dse_nov_2026-structure_5.pdf)](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_5.pdf) | 10:56Z | Re-read in full. Prints: $300 NLH (1Day), Event numbers 02 and 12, start 11:10 AM, 40,000 chips, 30-minute levels through level 28, breaks every 4 levels, "Late Registration: 10 levels + Break (~ 4:55 PM)", Guarantee $10,000, clause 6 "$58 of the $300 Buy-In is withheld ... prize pool consists of $242 of every $300 Buy In", clause 7 "pays 12.5% of the field", clause 9 "All pre-registered stacks will be in play at the start of the event", clause 10 unanimous written agreement to modify disbursement. **Clauses 1–10 still contain no one-entry limit, no rebuy prohibition and no add-on prohibition** — the strict booking gate stays closed for r018, exactly as `research/readiness-2026-11-19.md` recorded this morning, and the Nov 26 5:10 PM bounty remains not-a-plan pairing. Row r018 verified field-by-field: buy-in $300, guarantee $10,000, start 11:10, late-reg 16:55, 40,000 chips, 30-minute levels, $58 fee — all printed; ratio 33.3 stays descriptive. |
| [Wynn Signature Series schedule PDF](https://cdn.wynnresorts.com/image/upload/v1753296112/visitwynn_pdfs_files/Poker/Wynn%20Signature%20Series/Wynn_Signature_Series_Schedule.pdf) | 10:56Z | Re-read with a table-structure renderer. **Finding (F83): the official table DOES print the multi-day main-event guarantees** — $150,000 on each Jan 11–13 $400 flight row (1A–1F), $250,000 on each Jan 14–16 $600 flight row (1A–1D), $100,000 on each Jan 18–20 $400 flight row, $300,000 on each Jan 21–23 $800 flight row. The archived line-text capture (`data/snapshots/wss_sched.txt`, produced by pypdf `extract_text` on 2026-11-16/17) drops those merged cells, which is why the rows had been published blank with a flag. The CI provenance job's own 2026-11-19T06:00:04Z fetch reports sha256 `51a19da4…54eb` with `changed=false`, so bytes-vs-bytes the file is the same document both captures were made from; the difference is the extractor, not Wynn. All other row values verified against today's render: every date, day, time, event name, buy-in, chips and level count of the 38 published rows matches (incl. $10,000 NLH Turbos on 1/15·1/17·1/18·1/19·1/20·1/24, $30,000 Sunday NLH 1/17 and Seniors 1/24, satellites 1/14·1/21·1/22 at "10 Seats", continuation Day-2 rows with no numbers). Rows whose official GUARANTEE cell is genuinely empty (PLO 1/18, TORSE 1/19, Mixed Triple Draw 1/20, TOE 1/21, Big O 1/22, PLO Bomb Pot 1/24) stay blank. The 1/18 11 a.m. render shows one shifted cell; its $100,000 is corroborated by the un-shifted sibling rows on 1/19 and 1/20 before adoption. Full capture: `data/snapshots/wss_sched_reread_20261119.txt`. |
| [Wynn Signature Series structures PDF](https://cdn.wynnresorts.com/image/upload/v1762299460/visitwynn_pdfs_files/Poker/Wynn%20Signature%20Series/Wynn_Signature_Series_Structures.pdf) | 10:52Z | **Still "LAS VEGAS POKER — COMING SOON"** — no sheet to read, so no Wynn entry-rule label could be removed today; the row notes keep "read on 2026-11-19" honestly because the placeholder itself was re-read. |
| [Wynn poker room page](https://www.wynnlasvegas.com/casino/poker) | 11:02Z | WPT World Championship Nov 27 – Dec 21 with the Super Gold Million ($400, $3,000,000 GTD) — already on the site as rows r105/r111/r113/r117 (+Day 2 continuation), matching the archived `data/snapshots/w_poker_page.txt` and `wpt_sched.txt`. Signature Series Jan 11–24, 2027 banner unchanged. No new event, no changed number; no rows advanced. |

## Dataset changes made from these reads (each cites its source)

- 17 WSS flight rows gained the guarantee printed on their own row (F83); flags and notes amended.
  `gtd_multiple` recomputed (descriptive ratio; not a forecast): 375.0 ($400→$150k), 416.7
  ($600→$250k), 250.0 ($400→$100k), 375.0 ($800→$300k).
- All 38 WSS rows: `last_checked` 2026-11-17 → 2026-11-19, because their governing source
  (schedule + structures placeholder) was actually re-read today. No other row's date moved.
- `data/row_snapshot.json` re-baselined with the documented flow
  (`monitor_sources.py --update-snapshot`) so the monitor compares against the newly verified
  values instead of crying wolf about the promotion it was given.
- Entry-rule status for every WSS row remains UNV and the single-entry strict count is unchanged
  — a guarantee is money on the page, not an entry rule, and nothing here licenses a second label.

## Verification commands run over the changed tree (all exit 0)

`build_data.py` (deterministic) · `build_site.py` · `check_links.py` (30 pages) ·
`verify_rows.py` (335 rows / 1,386 checks / 0 hard failures; r225 documented) ·
`verify_against_snapshots.py` (0 unexplained mismatches; only the two on-record r263/01-04
conflict lines) · `check_schedule.py` · `check_source_facts.py --offline` ·
`python3 -m unittest discover -s scripts` (9 modules) · `npm test` (smoke 30/30, schedule
render, rendered links, calculator, source badges).
