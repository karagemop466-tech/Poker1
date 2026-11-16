# Executive summary

Snapshot: **2026-11-16**. Live site: https://karagemop466-tech.github.io/Poker1/

Only what an official operator document prints appears below. Every number traces to a row in the tournament
table, and every row links to its official PDF or page. Where an official document does not print a value, the
value is blank and the row is flagged.

## 1. What is verified

| Question | Answer | Basis |
|---|---|---|
| How many tournament rows are in the dataset? | **225** across four series | Official Venetian event pages and official Wynn PDFs |
| How many are **confirmed single entry**? | **54** | Each row's own official structure sheet was read by the automated collector and prints no re-entry, rebuy, add-on, multiple-entry or starting-flight clause |
| How many **offer more than one entry**? | **97** | The sheet prints unlimited re-entry (WPT terms) or cash-entry wording |
| How many are **possible multiple entries**? | **40** | The sheet prints "any player who bags chips for Day 2 may not play a subsequent flight", but is silent on a player who busts |
| How many still have **no confirmed rule**? | **34** | The official document available does not settle the rule. Left blank, never guessed |
| Date range covered | **2026-11-16 to 2027-01-24** | Four series |

| Series | Venue | Official dates | Rows | Confirmed single entry |
|---|---|---|---|---|
| DeepStack Extravaganza IV | The Venetian | Nov 16 – Dec 23, 2026 | 76 | **47** |
| DeepStack Extravaganza NYE | The Venetian | Dec 24, 2026 – Jan 10, 2027 | 31 | **7** |
| WPT World Championship | Wynn Las Vegas | Nov 27 – Dec 21, 2026 | 87 | **0** |
| Wynn Signature Series | Wynn Las Vegas | Jan 11 – 24, 2027 | 31 | **0** |

Two results deserve emphasis:

* **The WPT series has zero confirmed single-entry events.** All 61 of its event terms pages print unlimited
  re-entry, except the WPT Prime Championship, which prints "One (1) Entry and One (1) re-entry for each starting
  flight". Every WPT row belongs in the separate section.
* **The Wynn Signature Series has zero confirmed rows** because the official structures PDF linked from the Wynn
  poker page currently contains only the text "COMING SOON". There is nothing to read, so nothing is asserted.

### What changed as the sheets were read

The first pass, which trusted the sheet naming convention, found 88 single-entry rows. Reading each sheet's own
clause 8 reduced that to **54** and reclassified 40 rows. Clause 8 is decisive:

> "Any player who bags chips for Day 2 may not play a subsequent flight."

That clause is printed on the multi-flight sheets. It prohibits a *surviving* player from taking a second flight,
and says nothing about a player who busts. Those 40 rows are therefore published as **possible multiple entries**
in the separate section, not counted as single entry and not asserted to be re-entry either. Being conservative
here is the point of the exercise: a single-entry recommendation that later turns out to allow a second buy-in is
worse than no recommendation.

## 2. The single-entry shortlist

All 54 confirmed single-entry events are **single-day freezeouts**: you buy in once, play to a finish, and you are
free the next morning. None of them is a starting flight. That makes them well suited to a trip where you want to
play every day.

| Date | Start | Event | Buy-in | House fee | Guarantee | Guarantee ÷ buy-in |
|---|---|---|---|---|---|---|
| Wed Nov 18, 2026 | 11:10 AM | $300 No Limit Hold'em | $300 | printed on sheet | $10,000 | 33.33x |
| Thu Nov 19, 2026 | 10:10 AM | $200 NLH RaceDay Stack | $200 | $35 (17.5%) | not printed | — |
| Fri Nov 20, 2026 | 10:10 AM | $200 NLH RaceDay Stack | $200 | $35 (17.5%) | not printed | — |
| Sat Nov 21, 2026 | 10:10 AM | $200 NLH RaceDay Stack | $200 | $35 (17.5%) | not printed | — |
| Sun Nov 22, 2026 | 11:10 AM | $200 No Limit Hold'em | $200 | $40 (20%) | not printed | — |
| Mon Nov 23, 2026 | 5:10 PM | $200 NLH PKO Bounty | $200 | $40 (20%) | $8,000 (includes bounties) | 40x |
| Tue Nov 24, 2026 | 5:10 PM | $200 NLH Bounty | $200 | $40 (20%) | $8,000 (includes bounties) | 40x |
| Wed Dec 2, 2026 | 10:10 AM | $600 NLH Seniors (50+) | $600 | printed on sheet | $40,000 | 66.67x |
| Sun Dec 6, 2026 | 11:10 AM | $600 No Limit Hold'em | $600 | printed on sheet | $40,000 | 66.67x |
| Wed Dec 9, 2026 | 11:10 AM | $800 NLH Bounty | $800 | printed on sheet | $75,000 (includes bounties) | 93.75x |
| Tue Dec 15, 2026 | 11:10 AM | $1,100 NLH PKO Bounty | $1,100 | printed on sheet | $75,000 (includes bounties) | 68.18x |
| Wed Dec 16, 2026 | 11:10 AM | $600 NLH Bounty | $600 | printed on sheet | $50,000 (includes bounties) | 83.33x |

Buy-in range: **$200 to $1,100**. 50 of the 54 print a guarantee; 4 do not.

Guarantee ÷ buy-in is a **descriptive ratio of two printed numbers**, not a forecast. A bounty event's ratio is
not comparable with a pure prize-pool guarantee, because the printed guarantee includes the bounty money that will
be paid to whoever eliminates players. The highest non-bounty ratio in the set is **83.33x** ($600, $50,000,
Dec 30) and **66.67x** ($600, $40,000, Dec 2 / Dec 6 / Dec 8).

## 3. The day-by-day plan

The planner found **38 days** with at least one verified single-entry option between Nov 18, 2026 and Jan 10, 2027.

* **3 days** have a primary plus a *conditional fallback* the player can realistically reach: the fallback starts
  at least 45 minutes after the primary's **published late-registration close**.
* **12 days** have a later event that **cannot** follow the primary, because the primary's late registration is
  still open when the later event starts. Those days are shown as alternatives, never as a sequence.
* **24 days** have only one verified single-entry option, so there is nothing to sequence.

The sequence test uses the late-registration close printed on the official structure sheet, because that is a time
the operator actually prints. Finish times are **not** printed anywhere. The site shows an estimated finish
(levels × level length), labels it an estimate, and never uses it to claim that a sequence is possible.

### The 8 AM question

**No official schedule in this dataset starts at 8:00 AM.** The earliest verified single-entry start is
**10:10 AM**, on Nov 19, 20, 21, Dec 2, 8, 9, 10 and Jan 10. The earliest start anywhere in the dataset is
**10:00 AM** (Wynn Super Gold Million Mystery Bounty, Dec 10, re-entry rules apply to it).

Wynn's official terms state that "registration for each Event will open four (4) hours prior to the scheduled
start of play", which for a 10:10 AM event would put registration opening at about 6:10 AM. That is a registration
opening time, not a tournament start, and the site does not label it as one.

So an 8 AM start is achievable only as an **arrival and registration** time. The first cards are dealt at 10:10 AM
at the earliest, on the official documents available.

## 4. Hotels: verified, and deliberately blank

| Hotel | Mandatory resort fee / night | Room rate / night | Room tax | True cost / night |
|---|---|---|---|---|
| The Venetian | $55 plus applicable tax | no dated rate published | 13.38% Clark County | **blank** |
| The Palazzo | $55 | no dated rate published | not confirmed separately | **blank** |
| Wynn Las Vegas | $55 plus tax | no dated rate published | not confirmed | **blank** |
| Encore at Wynn | $55 plus tax | no dated rate published | not confirmed | **blank** |
| Bellagio | not confirmed | no dated rate published | not confirmed | **blank** |
| ARIA | not confirmed | no dated rate published | not confirmed | **blank** |
| Caesars Palace | official range only, $45–$50 plus tax | no dated rate published | not confirmed | **blank** |

The true nightly cost is blank **for all seven hotels**. The official Venetian poker-suite page prints rates "as
low as $119 and $209 and can be higher" for a Luxury King Suite, for The Venetian or The Palazzo, conditional on
qualifying play and availability, with blackout dates possibly applying and future rates published at most 150
days out. It attaches **no calendar date** to either figure and does not say which figure belongs to which
property. Computing a nightly total from an undated "from" price would be a guess, so the site does not do it.

The published poker rate is **conditional**, and this matters more than it first appears:

> Six hours of active live cash gameplay **or** a $300 or higher tournament buy-in, per night stayed, completed
> before 2 AM of the last night stayed, or the nightly rate is adjusted to the prevailing rate.

The $300+ threshold means the $200 events in the shortlist **do not** on their own qualify for the poker rate.
A trip built on $200 events would need either six hours of cash play per day or at least one $300+ entry each day
to keep the rate. That is a real budget risk and it is recorded on the hotel and rate rows.

## 5. Walking distance: confirmed only for the host buildings

No operator publishes a walking time, so no walking minutes are entered. Two stays are confirmed from official
location text:

* The poker room is **inside The Palazzo**, level 2 of the Grand Canal Shoppes (official Venetian poker page), so
  **The Venetian and The Palazzo are same-building stays**.
* The poker room is **inside Encore at Wynn Las Vegas** (official WPT terms), so **Wynn and Encore are
  same-resort stays**.

That leaves the **30-minute walking test unverified for Bellagio, ARIA and Caesars Palace**. They are the nearest
non-host candidates, but the site will not assert a walk time it cannot source from an official document.

## 6. Bottom line

1. **The only trip the official data supports today is a Venetian DeepStack trip between Nov 18, 2026 and
   Jan 10, 2027.** It is the only venue with confirmed single-entry events, and The Venetian/Palazzo are the only
   same-building stays.
2. **The earliest cards are dealt at 10:10 AM.** No official 8 AM start exists. An 8 AM arrival is plausible for
   registration and breakfast, not for play.
3. **54 single-day single-entry events, $200 to $1,100.** That is enough for a continuous run of playing days
   without ever touching a multi-flight event.
4. **The best non-bounty guarantee ratios are 83.33x ($600 / $50,000, Dec 30) and 66.67x ($600 / $40,000, Dec 2,
   6 and 8).** The best bounty ratio, 93.75x, is not comparable because its guarantee includes the bounties.
5. **No hotel cost can be quoted yet.** The one published poker rate is undated and conditional. The single most
   valuable missing fact is a dated official quote for the actual stay dates.
6. **Do not book a $200-only trip against the poker rate.** The rate requires six hours of cash play or a $300+
   tournament buy-in per night.

## 7. What would change this summary

* A **dated official hotel quote** for the stay dates. That fills the true nightly cost and makes the trip-cost
  calculator produce a real number.
* A written answer from the poker room on whether a **busted** multi-flight player may buy in again. That decides
  whether 40 rows move into the single-entry set or are confirmed as multi-entry.
* The **Wynn Signature Series structures PDF** being published. That could convert up to 31 unverified rows.
* An **official walking-time source**. That would let Bellagio, ARIA and Caesars Palace be tested against the
  30-minute limit.

Open questions are on the Questions page. Every flagged irregularity is on the Flagged for Review page. Every
source link is on the Sources and review page.
