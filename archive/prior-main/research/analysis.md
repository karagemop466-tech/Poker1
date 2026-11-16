# Analysis — Las Vegas Strip poker research, 2026-11-16

Data: `data/tournaments.json`, `data/hotels.json`, `data/schedule.json`. Every figure below comes from those files, and each file row carries an official source URL.

## 1. Tournament list

### 1.1 Single-entry field (47 events, Venetian)

- **Buy-in:** $200 (min) to $1,100 (max). Count by buy-in: $200 (19), $300 (12), $400 (2), $600 (12), $800 (1), $1,100 (1). Total 47.
- **Prize pool vs. house fee:** Fee = buy-in − printed prize pool. Examples: $200 → $160 pool (fee $40); $600 → $510 pool (fee $90); $1,100 PKO → $970 pool (fee $130). Fees are consistent across the structure sheets read.
- **Guarantees:** Largest in the single-entry list is $75,000 (events 36 and 52; the $1,100 PKO is event 52). Several are "guarantee includes bounties", so the cash pool is smaller than the guarantee. Sheets 1, 11, 15, 16, 30, 33 and 34 state this.
- **Bounty share:** 32 of 47 are bounty/PKO formats. This is the single biggest judgement in the list. Bounties are prize money (no chips), so they stay in the main list; see SUGGESTIONS.md.
- **Start-time clusters:** 5:10 PM (24 events), 11:10 AM (13), 10:10 AM (5), 12:10 PM (5).

### 1.2 Excluded (16 rows)

- **Venetian multi-flight (8):** events 1, 7, 19, 26, 47, 49, 56, 59. Re-entry is available across flights; Day 2 bagging rules restrict this.
- **Wynn daily (4):** Mon–Thu, Fri rebuy, Sat/Sun, and nightly. All allow re-entry, rebuy or add-on.
- **Bellagio (3):** Fri $600, Sat (price conflict), Sun $400 H.O.R.S.E. The optional staff gratuity buys chips.
- **Wynn WPT $600 NLH (1):** unlimited re-entry per flight, per structure PDF.

### 1.3 Unverified (136 rows, not ranked)

- **Venetian (9):** satellites (direct entry to events 39 and 47), the tag-team event (35), and the two-day event (39). Structure sheets not read.
- **Wynn WPT (127):** schedule rows only. The re-entry, add-on and bounty rules for most are unverified.

## 2. Hotels

| Hotel | Rate from (official, conditional) | Resort fee | True cost/night from | Position vs. venue |
|---|---|---|---|---|
| The Venetian | $119 | $55 | **$197.28** | Same resort as DSE events |
| The Palazzo | $209 | $55 | **$299.32** | Same resort; poker room on Palazzo side |
| Wynn | not verified | not verified | blank | Encore at Wynn per Wynn T&C (irregular) |
| Bellagio | not verified | not verified | blank | Venue for Bellagio events |
| Caesars Palace | not verified | not verified | blank | No verified tournament |

**Formula:** (rate + resort fee) × (1 + 13.38%). Room tax rate verified from The Venetian's official hotel terms. The rate is a floor for qualifying poker players, not a published nightly price.

**Walking requirement.** The brief asks for hotels at least 30 minutes' walk from the venue. No official source gives walking times, so no hotel is confirmed to meet this. The Venetian and Palazzo are the venue itself. Their figures are reference costs only. Cost and quality rank above distance, as instructed; quality ratings are not verified from any official source.

## 3. Schedule

- **First verified single-entry start:** 10:10 AM. There is no 8:00 AM event.
- **Plan logic:** arrive by 8:00 AM for check-in; then the day's single-entry starts in time order. The schedule lists official starts and late-registration windows only.
- **Stacking is not confirmed.** Event durations are not published, so no per-day chain of events is claimed.
- **Wynn dailies:** official page says they are suspended during the WPT series (Nov 27 – Dec 21). Resume date not stated, so they are excluded.

## 4. Irregularities affecting the plan

See REVIEW.md (IR-1 through IR-10). The most material for planning are the Bellagio Saturday price conflict (IR-1), the Wynn hotel offer conflict (IR-4/5), and the Wynn daily suspension (IR-7).

## 5. Limits of this analysis

- About a third of the Venetian structure sheets were not read.
- No official walking times, Wynn/Bellagio/Caesars rates or fees, or RWLV/MGM/Aria poker schedules were retrieved.
- No quality ratings were taken from an official source.
