# Requirement audit — live re-read · session `dd06081b` · 2026-11-19

Branch `arena/dd06081b-poker1`, base `main` @ `f5ecde0`. Every official page below was opened in this
session with the page-fetch tool on **2026-11-19** (UTC). The sandbox's own HTTP route cannot reach
the operator domains (`curl` to `www.venetianlasvegas.com` fails at TLS, exit 35), so no value here
comes from `scripts/monitor_sources.py`; each quotes the live page it was read from.

Nothing in `data/*.json` was changed by this session. This file records what matched, what differed,
and what is missing — including two findings that change the shape of the trip decision (§6, §7).

---

## 1. Venetian DeepStack Extravaganza IV — event listing (89 rows printed)

Source: <https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html>
(read in full: chunks 0–3 + the table continuation in chunk 2/3 boundary)

* Header unchanged: **"November 16 – December 23, 2026 … More than $3.6 Million in guaranteed
  tournament prize pools"**.
* Every printed row carries the same `Structures` PDF the dataset's `sources` list cites for that
  event number. Spot-checked one-for-one against the archive:

| Printed row (live, 2026-11-19) | Structure sheet printed | Dataset row | Field comparison |
|---|---|---|---|
| Thu Nov 26 · 11:10 AM · #12 · $300 NLH $10K GTD (1Day) | `dse_nov_2026-structure_5.pdf` | `r022` | match |
| Wed Nov 25 · 11:10 AM · #10 · $400 NLH $15K GTD (1Day) | `dse_nov_2026-structure_6.pdf` | `r021` | match |
| Mon Nov 23 · 5:10 PM · #8 · $200 NLH PKO $8K GTD (1Day) | `dse_nov_2026-structure_30.pdf` | `r012` | match |

* Printed rows whose *time and event number* were cross-checked in chunk 1–3 and that the dataset
  stores identically (all present, none missing, none extra among the 89 printed entries the listing
  shows: the dataset holds 94 DSE IV rows because it also stores the restarts/continuations listed
  further down the same page).

**Sheet #5 (Event 02 and Event 12), re-read in full:**

> "$300 No Limit Hold'em (1Day) … Event Numbers: 02 and 12 · Start Time: 11:10 AM · Starting Chips:
> 40,000 · Level Duration: 30 minutes · Late Registration: 10 levels + Break (~ 4:55 PM) · Guarantee:
> $10,000 · … 6. $58 of the $300 Buy-In is withheld for house fees (Rake + Staff). The prize pool
> consists of $242 of every $300 Buy In. · 7. This event pays 12.5% of the field · 8. Ante will come
> from the Big Blind Only … · 9. All pre-registered stacks will be in play … · 10. The tournament prize
> pool disbursement … may be modified upon unanimous written agreement …"

Ten numbered clauses, **no clause limits a player to one entry and none prohibits a rebuy or add-on**.
`r022` therefore stays a **candidate**, not a confirmed freezeout — exactly as the dataset has it.

**Sheet #6 (Event 10), re-read in full:** $400, $15,000 guarantee, 40,000 chips, 30-minute levels, ten
levels + break registration close (~4:55 PM), **$65 of the $400 withheld**, "pays 12.5% of the field",
same ten numbered clauses and the same silence on entry count. `r021` stays a candidate.

**Sheet #30 (Event 08), re-read in full (the monitor marked this URL "facts-changed"):**

> "$200 No Limit Hold'em (1Day) · Progressive Knock-Out Bounty (PKO) · Event Number: 08 · Start Time:
> 5:10 PM · Starting Chips: 25,000 · Level Duration: 30 minutes · Late Registration: 8 levels + Break
> (9:40 PM) · Guarantee: $8,000 (prize pool + total bounties) · 6. $40 of the $200 Buy-In is withheld …
> 9. Players start the event as a $50 bounty … 10. A Prize Pool of $8,000 is guaranteed by the Venetian
> Poker Room which consists of the actual prize pool plus the total amount of bounty prize money …"

No published value differs from `r012` ($200 / $8,000 / 25,000 chips / 28 levels / 9:40 PM close /
$40 withheld). **Irregularity (F87):** the monitor marks this row "facts-changed" while the sheet prints every published value unchanged and the provenance fetch records `facts_changed: false` with an empty `facts_diff`. The cause is in the baseline: hashing the stored line-render signature of 98 sources, exactly two disagree with `data/source_baseline.json` (#30 at `dd025da6…` vs `938b6bf7…`, and the series page at `032ea8e3…` vs `3f02cab0…`); the other 96 reproduce their stored hash byte for byte, and neighbouring sheet #5 reproduces `4da28f91…` exactly. `data/change_log.json` now additionally stores union-render signatures, which cannot be compared with line-render hashes, so the mark cannot distinguish "a value moved" from "the baseline was seeded wrong".

## 2. Venetian poker room and resort-fee pages

* Poker room page <https://www.venetianlasvegas.com/resort/casino/poker.html>: "LOCATION — The Palazzo,
  level 2, Grand Canal Shoppes … Open 24 Hours", 50 tables / 14,000 sq ft, "Non-registered hotel guests
  who play for three hours or more in our tournaments or cash games receive complimentary
  self-parking." **No entry, re-entry, rebuy or add-on policy is printed** — the written-freezeout gate
  has no official answer here.
* Resort fee page <https://www.venetianlasvegas.com/resort/resort-fee.html>: **"Rates include a daily
  Resort Fee of $55 plus tax per night, payable upon check-in."** This is the value `data/hotels.json`
  stores for The Venetian and The Palazzo.
* Series hub <https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament.html>:
  confirms DSE IV (Nov 16 – Dec 23, 2026) summary events — $800 NLH $500K GTD Dec 3–6, $2,200 NLH
  $1 Mill GTD Dec 12–14 (PokerAtlas Championship Title Event, final table streamed Dec 14 12pm), $1,100
  NLH Seniors $300K GTD Dec 13–15 (50+), $1,100 NLH $500K GTD Dec 17–20, $600 NLH $150K GTD Dec 20–23.
  The hub also announces a **third series this dataset does not carry** — see §7.

## 3. Wynn — poker room, Signature Series schedule, Signature Series structures

* Poker room <https://www.wynnlasvegas.com/casino/poker>: WPT World Championship "November 27–December
  21"; "New for 2026, the Super Gold Million brings a $400 buy-in featuring a $3,000,000 guarantee";
  Wynn Signature Series "January 11–24. 2027"; daily tournaments "suspended during each Wynn Signature,
  Wynn Millions, and Classic tournament series"; links to the same three PDFs the dataset cites.
* **Signature Series structures** — the URL the dataset cites,
  <https://cdn.wynnresorts.com/image/upload/v1762299460/visitwynn_pdfs_files/Poker/Wynn%20Signature%20Series/Wynn_Signature_Series_Structures.pdf>,
  still renders exactly `LAS VEGAS / POKER / COMING SOON`, title "Poker Tournament - Details Coming
  Soon". **The Wynn poker page now links a different file version for the same document**:
  <https://cdn.wynnresorts.com/image/upload/v1753296112/visitwynn_pdfs_files/Poker/Wynn%20Signature%20Series/Wynn_Signature_Series_Structures.pdf>
  (the version id the dataset already uses for the *schedule*). Read in this session: also
  `LAS VEGAS / POKER / COMING SOON`. So both versions are placeholders on 2026-11-19; the 34 Signature
  Series rows stay **UNV** (unverified entry rule). Recorded as **F88** (URL drift, no value change).
* **Signature Series schedule**, read in full with a table-structure renderer and archived verbatim at
  `research/requirements-audit-dd06081b/wss_sched_live_20261119.md`. Line-by-line check:
  `python3 research/requirements-audit-dd06081b/compare_wss_live_20261119.py` →
  **38 printed rows, 38 published rows, 38 matched, 0 mismatches** on date, start, buy-in, guarantee,
  starting chips and printed levels. Three name word-order notes (r300 TORSE, r307 TOE, r314 Seniors
  50+) are wording only — the poster prints a one-cell name column.

## 4. Caesars / Horseshoe east-side page (marked "facts-changed" by the monitor)

<https://www.caesars.com/las-vegas/explore/casino/poker-tournaments-las-vegas-strip> — printed author
"James Billington", date "July 17, 2026". It is an **editorial article**, not a schedule: no dated
tournament, no buy-in table, no structure sheet. It states the Caesars Palace room is on the Appian Way
promenade, 16 tables, open 24/7, and Horseshoe's "Hall of Fame Poker Room" is open around the clock.
The dataset already treats this page as an editorial source and publishes **no** Caesars or Horseshoe
dated rows from it. A change here cannot move a published value, so the mark is cosmetic. Confirmed
without a value change; recorded in §1 of `FLAGGED.md`'s note and in `COORDINATION.md`.

## 5. Required by the request but **not obtainable from an official source**

| Item | What the official pages show | Status |
|---|---|---|
| Written one-entry / no-rebuy / no-add-on confirmation for Venetian events | 52 Venetian structure sheets read (37 DSE IV + 15 NYE); none prints a maximum-entry, no-rebuy or no-add-on clause. Re-read today for #5, #6, #30; still silent. | **blocked** — needs the poker room's written ruling (QUESTIONS C1) |
| Written entry rules for the 136 Wynn WPT rows | structures PDF exists; entry wording is per-event and already stored; nothing affirms a whole-event freezeout | **blocked** — same |
| Wynn Signature Series entry rules | structures PDF is a "COMING SOON" placeholder in both published versions, read today | **blocked until Wynn publishes** |
| Any 8 AM tournament start | Venetian earliest printed start in the DSE IV listing is 10:10 AM (events 3–5, 24, 32, 35); Wynn daily registration opens 4 h before a 12 PM start, but that is registration, not play | **not available** — the "play from 8 AM" aim cannot be met from official schedules |
| Live hotel rate for an arbitrary date | The Venetian engine returned only a loading shell for the Dec 13–20 lookup on 2026-11-19 (already flagged); Wynn's engine renders client-side and returns no quote to a text fetch | **not obtainable without a rendering browser**; the dated log is the only priced evidence |
| Verified finish times | No sheet prints one; the site's finish is start + published levels + breaks | **estimate only, labelled as such** |

## 6. A value-level conflict worth a reviewer's attention (no change made)

The **DSE IV listing prints event 12 as `$300 No Limit Hold'em $10K GTD (1Day)` at 11:10 AM on
Thursday November 26**, while **the Wynn Signature Series schedule prints NLH Day 1A/1B/1C/1D/1E/1F on
January 11–13 at the Wynn**. The trip plan's Dec 13–20 scenario and the January 10–15 rate quote are
therefore in two different tournament universes: the December window is Venetian-only, the January
window is Venetian (NYE finale to Jan 10, Showdown from Jan 11) **plus** Wynn Signature Series. The
executive summary's "no competing property for that same stay" statement remains true for December;
for January there are now two properties running series at once, which changes the hotel comparison.
No row changes; logged for the summary and questions.

## 7. **Finding — a Venetian series the dataset does not carry**

`https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament.html`
announces, on 2026-11-19:

> "**Next Series:** DeepStack Showdown (January) — **January 11 – February 14, 2027** — More than $2.2
> Million in guaranteed tournament prize pools
> · $250 No Limit Hold'em $100K GTD Jan 15-18
> · $300 No Limit Hold'em $100K GTD Jan 21-25
> · $400 No Limit Hold'em $75K GTD Jan 25-27
> · $600 No Limit Hold'em $125K GTD Jan 28-31
> · $400 No Limit Hold'em $75K GTD Feb 1-3
> · $800 No Limit Hold'em $150K GTD Feb 4-7
> · $1,600 No Limit Hold'em $1 Mill GTD Feb 10-13 — MSPT PokerBowl XI"

The event page exists and prints a dated table with 59 event numbers:
<https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dss-jan-2027.html>
(read in full, chunks 0–3: Jan 11 2027 11:10 AM through Feb 14 2027 5:10 PM, each row linking its own
structure sheet under `/deepstack/2027/structures/dss_jan_2027-structure_NN.pdf`). Sheet #7 was read in
full as a spot check: `$300 NLH (1Day)`, "Event Numbers: 01, 05, and 10", 11:10 AM, 40,000 chips,
30-minute levels, 10 levels + break registration close (~4:55 PM), $12,000 guarantee, "**$58 of the $300
Buy-In**" withheld, "pays 12.5% of the field", same ten numbered clauses — again **silent on entry
count**.

**Why it is not added to the dataset in this session, and what would be needed:** every published row
in this repo must be verifiable against an *archived* official document, and `scripts/verify_rows.py`
maps structure sheets by the filename pattern `dse_nov_2026-structure_N.pdf` /
`dse_dec_2026-structure_N.pdf` only. Adding a third series correctly means (a) archiving the 59-row
event page and its ~26 structure sheets as snapshots through the provenance job, (b) extending
`extract_rules.py` / `verify_rows.py` to the `dss_jan_2027` pattern, (c) re-deriving entry status for
every row from its own sheet, and (d) re-running the schedule and overlap model over the new dates. That
is a full session of work with new source material, not a footnote to this one. It is therefore
**published as a flagged gap (F89) with the official links quoted above**, listed first in
`SUGGESTIONS.md` as the highest-value next task, and recorded in `QUESTIONS.md` as I18. The practical
consequence for the reader: for **11 January – 14 February 2027 this site's tournament tables are
incomplete**, and the Wynn Signature Series is not the only series running in that window.

## 8. What this session changed (and did not)

* **No official value, source URL or `last_checked` was changed.** The dataset rebuilds byte-identical.
* Added: this record, the Wynn Signature Series live capture + its re-runnable checker, `REQUIREMENTS.md`
  (requirement-by-requirement status with links), a date-filter control and an entry-plan calculator on
  the site, and flags F87–F89 with the questions they raise.
* Not attempted, with reasons in §5: Google/Apple walking verification (the site's walking times are
  OSM-routed and labelled as such — no property publishes a time), live hotel quotes for new dates
  (engines render client-side; the text fetch returns a shell), and any promotion of a candidate to a
  confirmed freezeout (no official source supports it).
