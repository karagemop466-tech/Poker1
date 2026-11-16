# Flagged for review

Every blank and every disputed value in the dataset, with the document it came from and the reason it is
blank. Flags do not block publication. Each one is here so it can be reviewed rather than assumed.

Generated from `data/tournaments.json` and `data/hotels.json` on the most recent build.

## Tournament blanks

| Field | Blank rows | Which rows | Why |
|---|---|---|---|
| House fee | 100 of 264 | 93 unverified Wynn rows (62 WPT, 31 Signature) plus 7 Bellagio and WPT rows whose fee split is not printed | The Wynn WPT structure PDF's extraction stops after the Dec 3 - 5 event, and the Signature Series structures document is a "COMING SOON" placeholder containing no structure at all. The Bellagio Saturday sheet contradicts itself on the split. |
| Guarantee | 57 of 264 | Mostly WPT side events and Signature Series rows | The document states no guarantee for those events. A blank guarantee is not a zero guarantee. |
| Starting stack | 99 of 264 | Wynn WPT and Signature rows whose structure has not been read | The stack is printed on the structure sheet, not on the schedule. With no readable sheet there is nothing to transcribe. |
| Level length | 99 of 264 | Same rows as starting stack | Same reason. |
| Late-registration cutoff | 140 of 264 | Rows whose structure sheet has not been read, plus recurring Bellagio weeklies which state "end of level 8 (including break)" relative to a level, not a clock time | The cutoff is printed as a level number in some documents and as a clock time in others. Only the clock time can be turned into an overlap test, so the level-number form stays blank rather than being converted from an assumed level length. |
| Prize pool | 100 of 264 | Same rows as house fee | The pool is the buy-in minus the fee. With no fee there is no pool figure. |
| Projected finish time | 264 of 264 (not a field) | Every event | No official document publishes one. The printed late-registration cutoff is used as the practical substitute and is labelled as derived. |

## Hotel blanks

| Field | Blank | Which hotels | Why |
|---|---|---|---|
| Date-specific room rate | 7 of 7 | All | Every official booking engine returns only a JavaScript loading shell to a plain fetch, and no property publishes a rate card. |
| True cost per night | 7 of 7 | All | It cannot be computed without a room rate. The resort fee and tax component *is* computed: $55 plus 13.38% tax comes to $62.36 per night for the five properties at that fee. |
| Resort fee | 1 of 7 | Caesars Palace | Caesars' own hotel page carries no fee table. A secondary reseller source states $54.95 plus tax, reported as $62.30 with tax. It is labelled secondary everywhere it appears. |
| Self parking, registered guest | 1 of 7 | Caesars Palace | Not confirmed from an official Caesars page. |
| Cancellation deadline | 2 of 7 | Venetian, Palazzo | The official terms bill a deposit at confirmation but set the cancellation deadline per offer rather than as a single property-wide rule. |
| Maximum occupancy | 5 of 7 | Venetian, Palazzo, Bellagio, ARIA, Caesars | Only Wynn and Encore state a maximum number (4). The others charge for additional guests without stating a cap. |
| Poker-player rate | 5 of 7 | All except Venetian and Palazzo | Only the Venetian publishes a poker-suite rate: from $119 and from $209, conditional on six hours of cash play or a $300+ tournament entry per night. |
| Check-in and check-out times | 4 of 7 | Wynn, Encore, Bellagio, ARIA | Not stated in the official terms pages that were read. |

## Disputed values, set aside rather than resolved

| Item | The conflict | Handling |
|---|---|---|
| Bellagio Saturday buy-in | Rule text says $600 ($510 pool / $50 admin / $40 optional gratuity); the heading says "NLH $1100 BUY-IN"; the file name says $1000 NLH. The sheet also refers to a Day 2 in September 2026. | Buy-in left blank. The row is marked unverified and the contradiction is reproduced in its note. |
| Venetian NYE event 29 re-entry price | The structure sheet says a discounted subsequent re-entry is $20 off, making it $180 total. The event page says the discount is $10. | Neither price is published as fact. The row records that a discounted subsequent re-entry is permitted and lists both readings. |
| Wynn WPT schedule dates | The extracted date and column order is shifted on several rows, so a printed date does not always line up with a printed event name. | Dates were taken from the structure PDF and the event names instead of the shifted columns. |
| Wynn Signature Series schedule | The extracted columns are shifted on several rows. | Series dates taken from the Wynn poker hub, which confirms Jan 11 - 24, 2027. Shifted fields not ingested. |
| Venetian DSE IV event 5 - 7 dates | The NYE schedule page prints "Saturday, December 26, 2025" for events that fall in a series running December 2026 to January 2027. | Treated as a publication typo. 2026 is used and the row is flagged. |
| Clark County licence list | Dated July 2021 and lists the Venetian and Palazzo at 3325 Las Vegas Blvd S, while current branding uses 3355. | Used only to corroborate the 13.38% Primary Gaming Corridor rate. Addresses come from the properties' own pages. |
| Caesars resort fee | $54.95 is from a secondary travel-industry source, not from Caesars. | Labelled secondary. The official Caesars link sits beside it. |

## Source documents that could not be read

| Document | Problem | Effect |
|---|---|---|
| Wynn WPT World Championship structures PDF | Text extraction stops after the Dec 3 - 5 event despite the PDF containing later events. | 62 WPT rows unranked. |
| Wynn Signature Series structures PDF | Contains only "LAS VEGAS POKER - COMING SOON". | All 31 Signature rows unranked. |
| Venetian and Caesars booking engines | Return a JavaScript loading shell only. | No room rate for either property. A blank was **not** read as "no availability". |
| Venetian parking page | Returns HTTP 404. | Parking figures come from the official hotel terms page instead. |
| Visit Las Vegas and Venetian "getting here" pages | Return HTTP 404. | Neither is linked from the site. Walk times come from Google Maps and Apple Maps links. |
