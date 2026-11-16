# Repo review — line-by-line verification log

Generated 2026-11-16. Machine-readable copy: `data/repo_review.json`. Rendered page: `review.html`.
Verification standard: every value must come from an official source (venue or MGM/Wynn/Caesars domain). Aggregators are never used as values. Unconfirmed values are left blank and flagged.

## Scope checked

| Area | What was checked | Result |
|---|---|---|
| Venetian DSE IV schedule | All 4 chunks of the official page, every row (date, time, event #, name, structure link) | **Verified.** Data matches the page. Rows verified: 64 events. |
| Venetian single-day structure sheets | Fee, prize pool, guarantee, late reg, re-entry/add-on wording | **Partial.** Read: sheets 1, 2, 5, 6, 7, 8, 10, 11, 15, 16, 17, 18, 22, 23, 26, 27, 28, 29, 30, 33, 34. Not read: 3, 4, 9, 12–14, 19–21, 24, 25, 31, 32, 35–37. Affected events are not ranked. |
| Venetian hotel terms | Resort fee, room tax, guest surcharge, parking | **Verified.** $55 resort fee + 13.38% room tax per night. |
| Venetian poker suite rates | Rate basis and play requirement | **Verified** (rate is conditional on play each night). |
| Bellagio poker page + PDFs | Event rules, fees, gratuity | **Irregular.** Saturday PDF conflicts ($1,000 / $1,100 / $600). Stale July 26 notice on page. |
| Wynn daily poster + structures PDF | Rules, fees, re-entry | **Verified rules**, all re-entry or add-on: excluded from single-entry list. Location text conflict ("Encore at Wynn"). |
| Wynn WPT schedule + structures PDF | Dates, buy-ins, re-entry | **Irregular.** Out-of-order rows (Dec 18 before Dec 17); $11,100 footnote. $600 NLH verified as unlimited re-entry. |
| Wynn hotel | Base rate, resort fee | **Unverified.** Official hotel page is dead. Offers conflict ($45 undated vs $55 expired Aug 31, 2026). |
| Caesars Palace hotel | Resort fee | **Unverified.** Chunks 0–1 read: no fee shown. |
| Bellagio hotel | Resort fee, nightly rate | **Unverified.** Only aggregator figures found. |
| RWLV, MGM Grand, Aria, Planet Hollywood | Poker pages | **Unverified.** Official URLs returned email blast, 404, or an unrelated domain. |

## Corrections made during this review

1. Venetian data rows were re-checked against the official schedule. Two multi-flight event rows that had been written from memory were confirmed (event 1 flights 1A–1D; event 19 flights 1A–1C).
2. Removed unsourced details from the data: late-registration times not printed on read sheets, "8-handed" formats, a $100 bounty amount, a $50 bounty amount (event 18/58), a Venetian non-guest parking rate, a Wynn re-entry fee, and several Bellagio rule details.
3. Wynn hotel entry changed from $99/$45 (as if current) to blank, because the offers are undated or expired.
4. Wynn WPT $600 NLH moved from "single-entry" to the excluded list, because its structure states unlimited re-entry.

## Irregularities found

- **IR-1 Bellagio Saturday price.** File name and page: $1,000. PDF header: $1,100. Fee breakdown ($510 + $50 + $40) totals $600. Not resolved; left unverified.
- **IR-2 Wynn WPT schedule order.** Dec 18 rows appear before Dec 17 rows, and a footnote mentions an $11,100 Ladies entry.
- **IR-3 Wynn registration location.** Daily T&C say registration is in Encore at Wynn. Confirm the poker room location.
- **IR-4 Wynn hotel offer dates.** Offer 850225 is expired (travel window ended Aug 31, 2026). Offer 848654 is undated.
- **IR-5 Wynn resort fee conflict.** $45 (848654, undated) vs $55 (850225, expired).
- **IR-6 Bellagio stale notice.** Official poker page carries a tournament-resumption notice dated July 26.
- **IR-7 Wynn daily suspension.** Official poker page says daily tournaments are suspended during the WPT series (Nov 27 – Dec 21).
- **IR-8 Venetian typos.** The schedule prints "No LImit Hold'em" for events 2, 6, 10, 12. Cosmetic; the event data is consistent.
- **IR-9 Venetian multi-flight rake discounts.** Schedule notes $40 (events 56) and $20 (event 59) discounts for early entries. The structure sheets for those events were not read, so the amounts are unverified.
- **IR-10 Venetian structure sheet 9.** Linked for event 1 flights 1B and 1D, not read.

## Open verification gaps

See `QUESTIONS.md` and the Flagged for Review page. Summary: 136 unranked rows, 16 excluded rows, no verified walking times, no verified Wynn, Bellagio or Caesars hotel rates or fees.
