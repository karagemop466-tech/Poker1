# Coordination board

The repository began this task without a `COORDINATION.md` file or any existing task claims. The current Arena session is required to work on `arena/ce95f9c0-poker1`; the branch cannot be renamed or replaced with a separate session/integration branch.

| Task | Status | Owner / session | File scope |
| --- | --- | --- | --- |
| End-to-end Las Vegas poker research, dashboard, verification, and integration | in progress | `arena/ce95f9c0-poker1` | `COORDINATION.md`, `README.md`, site source/data/assets, and GitHub Pages workflow/configuration added for this project |

## Handoff and overlap policy

No other task claims were present when this board was created. This session is handling the end-to-end work in its current branch because Arena requires all changes to stay on that branch. Any additional session should check this board first and avoid the listed scope; please log requests for changes here rather than editing files in that scope.

## Scope and verification policy

Research snapshot: **2026-11-16 (UTC)**. Only official venue/operator/series pages and their official event structures support published facts. Every event/hotel row in the dashboard links to its primary official source. A field not confirmed by an official source is blank and paired with a review flag; conflicting official values are also blank until resolved. Strict single-entry means one paid entry total for the event (not one entry per starting flight). A single-day label, one structure sheet, or a multiple-flight schedule does not prove single-entry.

## Research log

- **Venetian DeepStack Extravaganza IV:** the official schedule covers 2026-11-16 through 2026-12-23 and lists event times, buy-ins, and some guarantees. Official structure sheets were checked for representative $200/$300/$400 one-day events and the $800/$500K multi-flight event. These sheets state their formats and schedules but do not establish a strict one-entry limit; the $800 structure says a player who bags for Day 2 cannot play a later flight, but does not confirm a general re-entry policy. No such row is treated as confirmed single-entry.
  - Schedule: https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html
  - Series overview: https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament.html
  - Structures: `dse_nov_2026-structure_18.pdf`, `_29.pdf`, `_5.pdf`, `_1.pdf`, `_2.pdf`, `_3.pdf`, `_6.pdf`, and `_12.pdf` under https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/
- **Wynn WPT World Championship:** official 2026 schedule and structure sheets were checked. Confirmed examples include $600 NLH ($400K guarantee, unlimited re-entry per starting flight), $1,600 NLH ($1M guarantee, unlimited re-entry per flight), $600 HORSE (unlimited re-entry), $1,100 WPT Prime ($5M guarantee, one entry plus one re-entry per flight), $600 NLH Turbo ($50K guarantee, unlimited re-entry), and $1,600 PLO Mystery Bounty ($500K guarantee, unlimited re-entry per flight). These belong in extra-spend / re-entry, not the strict-single-entry list.
  - Schedule: https://cdn.wynnresorts.com/image/upload/v1757097329/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Schedule.pdf
  - Structures: https://cdn.wynnresorts.com/image/upload/v1750864036/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Structures.pdf
  - Wynn poker room: https://www.wynnlasvegas.com/casino/poker
- **PGT ARIA High Roller Series:** official PGT news says five daily $5,300 events on Nov. 28–Dec. 2. The official schedule page lists $5,300 and 3 PM; its linked structure lists a $5,000 buy-in plus $100 on-time/$300 late fee and 12 PM, and explicitly says all events offer unlimited re-entry. Since official schedule/structure amounts and start times conflict, those fields must remain blank and flagged; no event is single-entry. The structure says no guarantee, so leave prize-pool guarantee blank.
  - News: https://www.pgt.com/news/pgt-winter-schedule-features-boosted-points-at-aria-and-five-dream-seats-at-last-chance
  - Schedule: https://www.pgt.com/schedule
  - Structure: https://pgt.pokergomedia.com/event_pdf/053862af-PGTARIAHighRollerSeriesstructurev3.pdf
- **Daily rooms and extra-spend terms:** Caesars' current official article confirms Caesars Palace daily $100 NLH events at 10 AM, 2 PM, 6 PM and 9 PM, each with a $1,000 guarantee and a $50 optional add-on for 15,000 chips. It does not state re-entry/single-entry rules. The same article confirms Horseshoe times (9 AM, 11 AM, 2 PM, 5 PM, 8 PM and 11 PM), but not buy-ins, guarantees, or entry rules. MGM Grand's current poker page confirms daily tournament times (11 AM, 7 PM, 11 PM); its linked $120 structure says an optional $11 gratuity adds 10,000 chips, but re-entry policy and schedule validity for a particular date are not established. Bellagio's Friday $600 NLH and Sunday $400 HORSE sheets explicitly allow re-entry through level 8 and optional gratuities that add chips. The Bellagio Saturday structure is internally inconsistent ($1,000 title vs $1,100 heading vs $600 buy-in allocation) and is excluded pending venue correction.
  - Caesars article: https://www.caesars.com/las-vegas/explore/casino/poker-tournaments-las-vegas-strip
  - Horseshoe room: https://caesars.com/horseshoe-las-vegas/casino
  - MGM Grand room: https://mgmgrand.mgmresorts.com/en/casino/poker-tables.html
  - MGM $120 structure: https://assets.contentstack.io/v3/assets/bltc6ce635bc4868eb2/bltb2a45da7e8ee5621/mgm-grand-casino-poker-120_nlh.pdf
  - Bellagio room: https://bellagio.mgmresorts.com/en/casino/poker.html
  - Bellagio Friday/Sunday/Saturday structure sheets are linked from the Bellagio poker page; Saturday is marked for review, not published as a usable row.
- **Hotel fee and rate verification:** official pages confirm posted resort fees: Venetian $55 + tax/night; Wynn $55 + tax/night; Bellagio $55 + tax/night; ARIA $55 + tax/night; MGM Grand $50 + tax/night; Horseshoe $49.95 + $6.68 tax/night ($56.63); Caesars Palace $54.95 + $7.35 tax/night ($62.30); Treasure Island $49.95 + tax/night. A date-specific official booking search for Dec. 3–7, 2026 (two adults, one room) did not return a usable stay quote; full stay totals therefore remain blank. Venetian's poker-player rates are conditional on availability and qualifying play and are not a date-specific quote. Same-resort hotel candidates have official venue/property links; exact room-to-room walking minutes are not published and must be flagged rather than invented.
  - Venetian fees: https://www.venetianlasvegas.com/resort/resort-fee.html
  - Venetian poker rates: https://www.venetianlasvegas.com/resort/casino/poker/suite-rates.html
  - Wynn fees: https://www.wynnlasvegas.com/about-us/resort-information
  - Bellagio fees: https://bellagio.mgmresorts.com/en/terms-and-conditions.html
  - ARIA fees: https://aria.mgmresorts.com/en/terms-and-conditions.html
  - MGM Grand fees: https://mgmgrand.mgmresorts.com/en/terms-and-conditions.html
  - Caesars booking policy/fees (Horseshoe/Caesars Palace): https://www.caesars.com/book/hotel-calendar?dateSearchFormat=flexible-dates&flexibleMonth=December&propCode=blv and https://www.caesars.com/book/hotel-calendar?dateSearchFormat=flexible-dates&flexibleMonth=December&propCode=clv
  - Treasure Island: https://treasureisland.com/hotel/luxury-suite
- **Schedule planning:** no confirmed 8 AM live tournament start was found. The dashboard must begin its itinerary at 8 AM with a planning/check-in step, distinguish competing starts, and show later starts only as conditional pivots after elimination or finish and while registration remains open. It must not promise that multiple overlapping entries can be played.

## Known irregularities and unresolved facts

- No upcoming event in the reviewed official sources is yet confirmed as strict single-entry (one paid entry total); the primary table should show an honest empty state and relevant candidates should appear in a separate review list.
- PGT ARIA structure vs schedule/news conflicts on buy-in/fee and start time; blanks + review flags required.
- Bellagio Saturday buy-in is contradictory; exclude from quantified tournament tables.
- Venetian event structures often omit any re-entry rule; do not assume freezeout or re-entry from a one-day label.
- Exact hotel room prices and full stay totals (including tax and resort fee) were not obtained for the selected comparison dates; leave total blank. Resort-fee-only amounts are not full-stay prices.
- Exact walk durations inside same-resort properties were not published in the official material reviewed; mark as on-property candidate with exact minutes unverified.

## Remaining work

1. Build the static dashboard, mobile/desktop styling, source-linked data, executive analysis, known/missing/questions, an 8 AM conditional itinerary, and a dedicated suggestions section.
2. Update README with project use and verification limitations. Run local static validation and review the live preview.
3. Add GitHub Pages Actions deployment, push only to `arena/ce95f9c0-poker1`, open a PR from this branch, inspect checks, merge via `gh pr merge`, and verify the deployed Pages URL.
4. Record PR/merge/deployment and final verification results here after success; never mark complete if the site is not live or broken.
