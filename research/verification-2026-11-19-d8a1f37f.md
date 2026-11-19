# Live re-read, 2026-11-19 — session d8a1f37f

Every document below was fetched live from its official host with this session's page-fetch
tool on **2026-11-19** (UTC evening). The purpose is not to re-verify numbers — `verify_rows.py`
does that against the archived snapshots — but to test two things the archive could not answer
on its own:

1. whether the official documents still say what the snapshots say, and
2. whether the *labels and quotations* derived from them are supported by their own sentences.

| Document | Live URL | What was read | Result |
|---|---|---|---|
| Venetian DeepStack IV event listing (4 chunks) | https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html | dates, start times, event numbers, structure-sheet links | Matches `dse-nov-2026.html` rows; 94 listed entries, 16 Nov – 23 Dec 2026 |
| Venetian poker room page | https://www.venetianlasvegas.com/resort/casino/poker.html | room location, hours, parking, promotion text | Matches `v_poker_page.txt`; **publishes no entry, re-entry, rebuy or add-on rule** |
| Structure sheet #30 (Nov) | https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_30.pdf | all numbered clauses | Matches `v_nov_struct_30.txt`; **no re-entry / rebuy / add-on clause** |
| Structure sheet #21 (Nov) | https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_21.pdf | all numbered clauses | Matches `v_nov_struct_21.txt`; clause 07 prints `$1,975` |
| Structure sheet #02 (Dec) | https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_dec_2026-structure_2.pdf | all numbered clauses | Matches `v_dec_struct_02.txt`; clause 6 prints `subsequent re-entry` |
| Structure sheet #08 (Nov) | https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_8.pdf | all numbered clauses | Matches `v_nov_struct_08.txt`; clause 07 prints `All subsequent buy in's after the initial buy in will be $200` |
| Wynn Signature Series Structures | https://cdn.wynnresorts.com/image/upload/v1762299460/visitwynn_pdfs_files/Poker/Wynn%20Signature%20Series/Wynn_Signature_Series_Structures.pdf | whole document | **Still only `LAS VEGAS / POKER / COMING SOON`** in this fetch. No sheet is published, so every Signature Series row stays `UNV`. This is the third dated read of the same placeholder (2026-11-17, 2026-11-17 via PR #112, 2026-11-19 here) |
| Wynn poker room page | https://www.wynnlasvegas.com/casino/poker | series dates, daily-tournament status | Matches; the page again prints *"the Daily Tournament schedule will be suspended during each Wynn Signature, Wynn Millions, and Classic tournament series"*, which matters for any trip that spans 11–24 January 2027 |
| Wynn daily tournament structures | archived `data/snapshots/w_daily_struct.txt` | four event blocks plus general terms | Read from the archived extraction; the monitor's 2026-11-19 fetch of the same URL returned 200 and the facts hash did not change |

## Findings that change published wording (fixed in this session)

**1. Six rows claimed a clause was absent while their own sheet printed it.**
`data/tournaments.json` r232, r234, r245, r256, r262 and r279 (Venetian NYE, $200 NLH Bounty $8K
GTD, 24 Dec – 10 Jan) each carried the excerpt *"No re-entry, rebuy, add-on or multi-flight
clause appears anywhere on this structure sheet (every numbered clause was read on 2026-11-16)"*
while citing `dse_dec_2026-structure_2.pdf`, whose clause 6 prints:

> "$40 of the $200 Buy-In is withheld for house fees (Rake + Staff). ... The $20 discount can be
> applied to the initial entry or any **subsequent re-entry**"

The same sheet is the `RE` evidence for r270 (Event #29), where the data correctly reads
*Clause 06: "The $20 discount can be applied to the initial entry or any subsequent re-entry."*
So one document was read two ways on seven rows. The auditor now flags the six rows that cite a
further-entry sentence while claiming silence; the published excerpts are to be rewritten as a
follow-up integration (see `COORDINATION.md`).

**2. Three fee quotes could not be found in their own PDF, and one cited the wrong clause.**
The fee excerpt was a template that painted the figures over one fixed sentence. Sheet #28
prints *"... Buy-In for house fees (Rake + Staff). **Prize pool consists of** $510 of every $600
Buy In."* — not the templated wording — and sheets #21, #37 and #08 print comma-formatted
`$1,975` and `$1,420` where the template wrote `$1975` and `$1420`. In addition, sheet #28's fee
clause is number **05**, not 06, because that sheet prints a separate tax clause. All 143 Venetian
rows now quote their sheet's own sentences and their own clause number. `scripts/audit_entry_labels.py`
verifies every quoted span against the snapshot on every build.

**3. The change monitor's "facts changed" mark was comparing an empty hash.**
`data/changes.json` lists four rows marked *"official source page printed different values on its
last re-check"*. In `data/monitoring.json` the same four sources show
`facts_sha256 = e3b0c442…b855`, which is the SHA-256 of the empty string: the fetcher extracted no
money, date, time or entry-rule word from those pages, and a non-empty baseline hash therefore
read as a change. Nothing printed on those pages has been shown to move. The same file shows six
distinct Caesars URLs returning one byte-identical 5,871-byte body — the pages are serving a
consent wall or a shared shell, not the page each URL names. Both are now reported as monitor
integrity findings rather than published as row changes.

## Findings that change nothing

- The Wynn daily structures document nests **two** numbering systems: general terms numbered 1–N,
  then each event block restarting at 1. A citation reading only "Clause 4" is ambiguous; the
  auditor resolves every row's clause to the block that prints the quoted words and the daily
  rows all resolve correctly (`data/entry_evidence_audit.json` →
  `findings.daily_clause_provenance`).
- `QUESTIONS.md` I12's quoted sentence *"Registration for each Event will open four (4) hours
  prior to the scheduled start of play"* **is** present verbatim in `w_daily_struct.txt` line 11 and
  the same line in `wpt_struct.txt`.
- The Wynn **$240 Friday Rebuy & Add-on** is correctly kept out of every single-entry list: its
  clause 4 prints `Re-entry is NOT allowed`, but clause 5 prints `Unlimited $200 rebuys` and
  `One (1) $100 add-on`. Re-entry and rebuy are not the same thing, and the audit treats them
  separately. The **$200 weekend** and **$160 nightly** formats each sell one $100 add-on per
  entry, which the user's policy excludes from the single-entry section.

## What was not possible

- No automated Stripe-wide daily-schedule scraper was added; the Wynn and Caesars dailies are
  recurring formats without calendar dates, and only the Venetian, Wynn, Bellagio and Caesars
  Palace publish machine-readable rules. A scraper for the remaining rooms is proposed in
  `SUGGESTIONS.md`.
- No Google or Apple Maps walking time was measured: both require an API key or a browser session
  that this session does not have. Every walking row keeps its routed OpenStreetMap time, its
  Google and Apple cross-check links, and its status (`internal` or `routed`), and nothing is
  presented as published by the property.
- No live hotel quote was taken: the booking engines render client-side and return no rate to a
  text fetch. The five dated quotes in `data/rates.json` remain the only rate evidence, each with
  its own stay dates and timestamp.
