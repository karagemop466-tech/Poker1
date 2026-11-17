# Structure-sheet verification and row join, 2026-11-17 (session c0714e1a)

Scope: every structure sheet published in the official WPT World Championship Structures PDF, read
sheet by sheet, and every Wynn WPT schedule row joined to the sheet that governs it. This closes the
gap that the earlier logs recorded as "no structure sheet is published for this event".

Sources read directly on **2026-11-17** (this sandbox cannot reach the operator domains from bash —
TLS is refused — so every read below was made through the page fetcher and checked against the text
snapshots already committed under `data/snapshots/`):

| Source | URL | Read |
|---|---|---|
| WPT World Championship Structures PDF | https://cdn.wynnresorts.com/image/upload/v1750864036/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Structures.pdf | 8 of 8 chunks |
| WPT World Championship Schedule PDF | https://cdn.wynnresorts.com/image/upload/v1757097329/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Schedule.pdf | 2 of 2 chunks |
| Wynn Signature Series Schedule PDF | https://cdn.wynnresorts.com/image/upload/v1753296112/visitwynn_pdfs_files/Poker/Wynn%20Signature%20Series/Wynn_Signature_Series_Schedule.pdf | 1 of 1 |
| Wynn Signature Series Structures PDF (both published URL versions) | https://cdn.wynnresorts.com/image/upload/v1753296112/.../Wynn_Signature_Series_Structures.pdf and https://cdn.wynnresorts.com/image/upload/v1762299460/.../Wynn_Signature_Series_Structures.pdf | 1 of 1 each |
| Venetian DeepStack Extravaganza IV event page | https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html | 4 of 4 |
| Venetian DeepStack Extravaganza NYE event page | https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-dec-2026.html | 2 of 2 |
| Venetian hotel terms | https://www.venetianlasvegas.com/legal/hotel-terms-and-conditions.html | 2 of 2 |
| Venetian poker suite rates and play requirements | https://www.venetianlasvegas.com/resort/casino/poker/suite-rates.html | 1 of 1 |
| Bellagio hotel reservation terms | https://bellagio.mgmresorts.com/en/terms-and-conditions.html | 2 of 2 |
| Bellagio FAQ (check-in, check-out) | https://bellagio.mgmresorts.com/en/faq.html | 1 of 3 (the "Before You Arrive" section) |
| ARIA hotel reservation terms | https://aria.mgmresorts.com/en/terms-and-conditions.html | 1 of 2 |
| MGM Resorts parking rates | https://www.mgmresorts.com/en/things-to-do/parking.html | 1 of 3 |
| Caesars Palace FAQ | https://www.caesars.com/caesars-palace/faqs | 15 of 15 |
| Caesars corporate disclaimers | https://www.caesars.com/corporate/disclaimer | 1 of 4 (the hotel disclaimer) |
| Wynn special-offer terms | https://www.wynnlasvegas.com/terms-and-conditions/848671 | 1 of 1 |
| Wynn parking information | https://www.wynnlasvegas.com/about-us/parking | 1 of 1 |

## 1. What the structures PDF actually contains

The earlier logs stated that the WPT structures PDF ends with the $1,600 PLO Mystery Bounty and
publishes no sheet for the milestone satellites (flag **U8**). That is wrong. Read end to end, the
PDF prints **69 separate structure sheets**, each introduced by its own "TERMS AND CONDITIONS" banner:

| Measure | Count |
|---|---|
| Structure sheets in the PDF | **69** |
| Sheets that print an entry-fee breakdown (`$X Buy-in = $Y Prize Pool + $Z Tournament Fee + $S Staff`) | **69** |
| Sheets that print a registration / re-entry clause | **69** |
| Sheets whose re-entry clause reads "Unlimited re-entry" | **67** |
| Printed date/time pairs across all sheets | **149** |
| Sheets with a printed starting stack | 69 |

The two sheets that do **not** print "Unlimited re-entry" are the events with a published entry cap:

- **Block 11, $1,100 WPT Prime Championship (Dec 5–12, 2026):** *"Registration: One (1) Entry and One
  (1) re-entry for each starting flight will be available until the start of level 10 (approximately
  6:45 p.m.). A player who advances to Day 2 is prohibited from entering a subsequent starting flight."*
- **Block 22, $10,400 WPT World Championship (Dec 13–20, 2026):** *"Registration: Four (4) Entries
  maximum. Players are allowed One (1) entry per starting flight + One (1) Day 2 Entry prior to the
  start of Day 2. Registration is available until the start of level nine (9)."*

Every other sheet, including all 16 milestone-satellite sheets, prints "Unlimited re-entry will be
available until the start of level N". **No sheet in the PDF prints an add-on or a re-buy.**

Reproduce this with `python3 scripts/extract_wpt_struct.py`, which writes
`data/wpt_struct_blocks.json` (one record per sheet) from the committed text snapshot
`data/snapshots/wpt_struct.txt` of the PDF.

## 2. Row-to-sheet join

`python3 scripts/extract_wpt_sheets.py` joins each schedule row to the sheet that prints the same
date, the same start time and the same buy-in, and only then on printed title words. It refuses to
guess: a row with more than one equally good candidate is reported instead of assigned.

| Measure | Result |
|---|---|
| Wynn WPT entry rows in the dataset | **113** |
| Entry rows joined to their printed sheet | **112** |
| Entry rows with no sheet printing that date/time/buy-in | **1** |
| Continuation rows (Day 2, Day 3, final table), which never sell a new entry | 23 |
| WPT rows still unverified on the entry rule | **1** (the row below) |

The one unresolved row is **r225, Dec 21, 8 p.m. "NLH Turbo", $600, $50,000 GTD**. The $600 NLH Turbo
sheet (block 12) prints eight dates for that event, and Dec 21 is not one of them — the sheet prints
**6 p.m.** on Dec 21, while the schedule prints **8 p.m.** This is already recorded as flag **F4**;
the dataset keeps the schedule's 8 p.m. time and the row stays unverified rather than borrow another
row's clause. Manual check: block 12 of the structures PDF against the Dec 21 line of the schedule PDF.

Continuation rows keep their own status: a Day 2 row does not sell a new entry, so it is labelled
`CONT` whatever the parent event allows, and its note points at the parent event's Day 1 rows.

## 3. Effect on the published dataset

| Classification | Before this session | After this session |
|---|---|---|
| Verified single entry (`SE`) | 80 | **80** |
| Possible multiple entries (`MULTI`) | 60 | **66** |
| Re-entry confirmed (`RE`) | 46 | **108** |
| Continuation (`CONT`) | 2 | **25** |
| Entry rule unverified (`UNV`) | 129 | **38** |

The 38 remaining unverified rows are **all Wynn Signature Series rows**. Both published versions of
the Signature Series structures PDF (the `v1753296112` and the `v1762299460` URLs) return a single
page that reads **"LAS VEGAS / POKER / COMING SOON"** and prints no sheet, so no entry rule can be
quoted for those rows. That matches the earlier record and is unchanged.

**The user-facing consequence is important and is not what the previous documents said:** no Wynn WPT
event — not the $10,400 World Championship, not the $3,300 WPT Prime flights, not the milestone
satellites — is eligible for the single-entry list. Wynn publishes re-entry for all of them, 67 sheets
without limit and 2 with a printed cap. The 80 verified single-entry rows all belong to The Venetian
(54 DeepStack Extravaganza IV, 26 New Year's Eve).

## 4. Other field corrections found while joining

- The **$1,600 Milestone Satellite to Prime and World Championship** sheet prints
  *"$1,600 Buy-in = $1,440 (Tournament Prize Pool) + $115 (Tournament Fee) + $45 (Poker Staff Service
  Charge)"*, so $160 of the $1,600 is withheld (10.0%). The dataset stores that printed split rather
  than a percentage, and the site shows the operator's own numbers.
- The **$10,400 World Championship** sheet prints a $400 tournament fee plus a $200 staff charge on a
  $10,400 buy-in (5.77%), and the **Ladies Championship** sheet is headed
  *"$11,100 (***discounted to $1,100 for Ladies)"*, which confirms flag F8 from the sheet itself.
- The **$400 Double Play Milestone Satellite** sheet defines its milestone in its own words:
  *"A Player who accumulates 140,000 in tournament chips (\"The Milestone\") or more will instantly be
  awarded one (1) Tournament Prize"*. Because that is a different mechanism from the Venetian
  satellites, no milestone figure is carried across to the Wynn rows.
- Wynn parking (official Wynn parking page): *"The daily parking fee for non-registered guests is $25
  per day with the first three (3) hours complimentary"*, self-parking is complimentary for registered
  Resort and Tower Suite guests and for Wynn Poker Room guests. Wynn resort fee (official offer terms):
  *"A daily resort fee of $55 plus tax will be added to your room account for each room night"*, with
  a 48-hour cancellation window on the offer terms read.

## 5. Hotel fee, tax, parking and cancellation facts verified this session

| Property | Fact | Official text | Source |
|---|---|---|---|
| Bellagio | Daily resort fee **$55.00 plus applicable tax** | "Daily Resort Fee. A daily resort fee of $55.00 plus applicable tax will be applied to all reservations." | [Bellagio terms](https://bellagio.mgmresorts.com/en/terms-and-conditions.html) |
| Bellagio | Tax rule, no percentage printed | "Lodging taxes apply to the basic room rate, any resort fee, additional per occupant charges, upgrades, as well as any other charges as required by applicable law." | same page |
| Bellagio | 72-hour free cancellation | "The first night's deposit is fully refundable provided a timely notice of cancellation is received ... at least 72 hours prior to the arrival date" | same page |
| Bellagio | Check-in 3:00 PM, check-out 11:00 AM | FAQ, "What time is check-in? What time is check-out?" | [Bellagio FAQ](https://bellagio.mgmresorts.com/en/faq.html) |
| ARIA | Daily resort fee **$55.00 plus applicable tax** | "Daily Resort Fee. A daily resort fee of $55.00 plus applicable tax will be applied to all reservations." | [ARIA terms](https://aria.mgmresorts.com/en/terms-and-conditions.html) |
| ARIA | Check-in 3:00 pm, check-out 11:00 am | "Check in time is 3:00 pm and check out time is 11:00 am." | same page |
| Bellagio and ARIA | Self-parking **$20** per 24 h for a registered hotel guest, valet **$40** per day | Parking rates table, "Registered Hotel Guest: $20 | $20" | [MGM parking](https://www.mgmresorts.com/en/things-to-do/parking.html) |
| Caesars Palace | Check-in **4:00 PM**, check-out **11:00 AM** | "Check-in at Caesars Palace begins at 4:00 PM, and check-out is at 11:00 AM." | [Caesars Palace FAQ](https://www.caesars.com/caesars-palace/faqs) |
| Caesars Palace | 48-hour cancellation for most direct bookings | "For most hotel reservations made directly with Caesars Palace, cancellations are generally allowed up to 48 hours prior to the scheduled arrival date." | same page |
| Caesars Palace | Resort fee **not published for this property** | The property pages and FAQ print no fee amount. The corporate disclaimer prints only a portfolio range: "Room reservations are subject to a daily resort fee between $45-$50 plus applicable tax." | [Caesars disclaimers](https://www.caesars.com/corporate/disclaimer) |
| Caesars Palace | Street address 3570 Las Vegas Blvd South, Las Vegas, NV 89109 | Property page footer | [Caesars Palace](https://www.caesars.com/caesars-palace) |
| The Venetian | 13.38% Clark County Room Tax, $55 resort fee plus tax | "Daily rates do not include the applicable Clark County Room Tax of 13.38%." / "The Venetian Resort has a standard Las Vegas Resort Fee of $55 plus applicable tax per night" | [Venetian hotel terms](https://www.venetianlasvegas.com/legal/hotel-terms-and-conditions.html) |
| The Venetian | Poker suite rate qualification | "you will be required to play six hours of active live cash gameplay or buy in to a $300 or higher tournament for each night stayed" | [Venetian poker suite rates](https://www.venetianlasvegas.com/resort/casino/poker/suite-rates.html) |

**Deliberately not used.** Third-party pages quote $45, $54.95, $55 and $62.30 for the Caesars Palace
resort fee, and the Caesars corporate disclaimer quotes a $45–$50 portfolio range. None of those names
Caesars Palace on an official page read here, so the property's `resort_fee_usd` stays blank:
it is better to leave the field empty than to publish a fee the operator has not printed for that
property. The Bellagio and ARIA tax percentages are the same problem in a milder form: their own terms
print the tax rule but no percentage, so 13.38% is stored with status `estimated`, is shown on the
site as an estimate, and is **excluded** from every true-cost calculation by
`scripts/check_links.py`.

## 6. Irregularities recorded (new or re-confirmed)

| # | Item | Handling |
|---|---|---|
| U8 (corrected) | The earlier text said the WPT structures PDF publishes no satellite sheet. In fact it publishes 16 satellite sheets. | Corrected here and in FLAGGED.md; the rows now carry the printed clause. |
| F4 (re-confirmed) | The Dec 21 NLH Turbo is printed at 8 p.m. by the schedule and 6 p.m. by its structure sheet. | The row keeps the schedule time and stays unverified. |
| F22 (new) | The Wynn Signature Series structures PDF is a "COMING SOON" placeholder at **both** published URL versions. | The 38 Signature Series rows stay unverified on the entry rule. |
| F23 (new) | Wynn's printed terms allow re-entry for every WPT event: 67 sheets say "Unlimited re-entry", the Prime Championship allows one entry plus one re-entry per flight, and the World Championship allows four entries maximum. | No Wynn WPT row can be ranked in the single-entry list. Published on the Flagged page. |
| F24 (new) | The $400 Double Play and other Wynn milestone satellites award a prize on reaching a printed chip milestone rather than paying a conventional prize pool, so a guarantee ÷ buy-in ratio would misdescribe them. | Those rows are labelled separately on the site and are excluded from the ranking. |
