# Verification record — session `81c6f6bc`, 2026-11-17 (T5)

Scope: the integration-session re-verification of the combined tree (stale PRs
#64, #66, #53, #46 merged in full; #52 and #51 integrated/closed with
dispositions). Automated field checks plus live spot-checks of the official
sources through the agent page fetcher.

## 1. Automated checks (every one re-run on the final tree)

| Check | Result |
|---|---|
| `scripts/check_links.py` (conflict markers, sources, rules, schedule, hotel-rate/cost arithmetic, provenance, page links) | OK — 58 files, 23 pages, 317 tournament rows, 7 hotels, 5 dated rates, 70 schedule days |
| `scripts/verify_rows.py` (every published field vs the archived official text) | 335 rows, 1,392 field checks, **0 hard failures, 0 review items** |
| `scripts/verify_live_rows.py` (317 rows compared field by field with the documents that print them) | 317/317 checked, 0 skipped, **0 contradicted** (3 warnings: the Dec 26 "2025" rows, F109) |
| `scripts/verify_live.py --offline` (archived replay of the live parser) | 136 published rows checked, **0 missing, 0 changed, 0 discrepancies** |
| `npm run test:smoke` | 23/23 pages render |
| `npm run test:ui` | 14/14 assertions |

## 2. Live spot-checks through the agent page fetcher (2026-11-17)

### NYE official event page (Venetian, HTML) — matches the dataset

- **r263, Jan 4, 2027 MSPT Day 2 Restart = 11:10 AM** on the live page — the
  published 11:10 (F111) is confirmed live; the structure sheet's 11:00 AM
  wording stays on the row as the conflict (question E2).
- The **CES badge** lines print under Jan 6 event 29, Jan 7 (1B) and Jan 8 (1D)
  only — not under 1A/1C/1E/1F. The F118 removal on the 1F row is confirmed
  live; the three rows that do print the line keep it.
- The page still prints **"Saturday, December 26, 2025"** on the Dec 26 rows —
  F109's source-side year typo persists live.

### WPT schedule sign PDF (Cloudinary version pin `v1757097329` — the bytes are immutable, so this is the same file the snapshots captured)

A layout-aware table extraction of the same file bytes agrees with the archived
reading-order extraction on **the large majority of rows** (all Nov 27 – Dec 12
values, the Dec 17 – Dec 20 blocks, all buy-ins/guarantees/chips/levels), and
both extractors agree on real sign typos ("BadugI" on Nov 28). But they
**disagree on six tokens**:

| Row(s) | Archived extraction (published) | Layout-aware extraction |
|---|---|---|
| r154 / r165 (Dec 14/15) | "NLH Turbo" / "NLH $500 Bounty Turbo" | "NIH Turbo" / "NIH $500 Bounty Turbo" |
| r133 (Dec 13) | "Ladies NLH Championship (2 Day)" | "Ladies NIH Championship (2 Day)" |
| r173 (Dec 16) | "$25K NLH High Roller" satellite | "$25K NIH High Roller" |
| r125 / r130 (Dec 12) | "World Championship 1A/B" | "World Championship 1A/8" |
| r128 (Dec 12) | "Milestone Satellite to $1,100 Ladies NLH Championship" | "Milestone Satellite to $10,400 Ladies NLH Championship" |
| r045 (Dec 1) | "Limit Omaha 8/Stud 8" | "Limit Omaha 8/5/stud 8" |
| r166–r175 heading | "Dec. 16 / Wednesday" date list | "Dec. 18 Wednesday" block heading |
| r225 (Dec 21 turbo) | 6 p.m. | **8 p.m.** |

Notes on the two directions:

- The "Dec. 18 Wednesday" heading is what row F6 and the per-row flags on
  `r166`–`r175` already quote — the layout-aware reading **confirms the
  established flag text**; the archived date-list reads "Dec. 16" there.
- The 8 p.m. reading of the Dec 21 turbo is what the **original F4** flag
  recorded before F108 retired it as a transcription error on the basis of the
  archived extraction. The structure sheet prints 6 p.m. and the archived
  extraction reads 6 p.m.; the row keeps **18:00** and carries the alternate
  reading as a flag (nothing silently flipped).
- Session `ca6d75b1`'s F119 corrections (NIH→NLH etc.) follow the
  pypdf/archived reading; `scripts/verify_live.py` (pypdf) reproduces them.

Everything about the disagreement is published rather than resolved by
guesswork: **FLAGGED F123** lists all six tokens, each affected row carries the
alternate reading as a flag, and **question E3** asks which glyphs the rendered
sign shows. A human with the rendered PDF (or the Wynn poker room) settles it.

## 3. Integration verification summary

- Nine transcription corrections applied (F119), each confirmed against the
  archived official text and each carrying a per-row correction flag.
- Fee-line arithmetic (F120) and the Ladies dual fee lines (F121) published
  exactly as printed; both printed lines preserved in
  `data/wpt_row_sheets.json`; question I11 (fee basis) stays open.
- `verify_rows.py` and `verify_live_rows.py` no longer clobber one artefact
  (`data/row_field_checks.json` vs `data/row_verification.json`).
- Flag ids globally unique through F123; next free id **F124**.

No published value was changed in this T5 pass; the pass's output is the
disagreement record (F123, question E3) and the live confirmations above.
