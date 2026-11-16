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

## Dashboard implementation and verification

- Built the static, responsive dashboard in `index.html`, `styles.css`, and `app.js`; factual content and source IDs are in `data.json`. The page includes a strict-entry empty state, separately classified re-entry/extra-spend events, candidate review table with search/sort, daily-room watch, guarantee-to-buy-in comparison, Dec. 5 conditional day plan beginning at 8 AM, hotel fee comparison, known/missing/questions, suggestions/decision paths, and grouped official source links.
- Current data counts: **0 confirmed strict-entry events**, **8** re-entry/extra-spend rows, **16** entry-cap candidates, **8** hotel rows, and **39** official links. The 0 strict-entry count is intentional; unknown and re-entry terms are never promoted to freezeout status.
- Expanded official Venetian schedule review through Dec. 23. Examples now shown include #2 ($300/$10K, Nov. 18), #3 RaceDay Stack ($200, Nov. 19), #7 ($400/$75K, Nov. 23–25), #14 ($600/$30K, Nov. 27), #26 ($800/$500K multi-flight, Dec. 3–6), #28 ($600/$40K, Dec. 6), #47 ($2,200/$1M, Dec. 12–14), #56 ($1,100/$500K, Dec. 17–20), and #59 ($600/$150K, Dec. 20–23). Reviewed structure sheets do not establish a strict one-entry cap; one-day labels remain candidates only.
- Added Wynn WPT examples with the structure-confirmed terms: $600 NLH ($400K), $800 NLH ($1M), $1,600 NLH ($1M), $600 HORSE, $1,100 WPT Prime ($5M; one entry plus one re-entry per starting flight), $600 NLH Turbo ($50K), and $1,600 PLO Mystery Bounty ($500K). The $400 Super Gold Mystery Bounty / $3M schedule listing appears as a candidate because its entry cap was not confirmed in the reviewed structure material. PGT ARIA's unlimited re-entry is clear, but the official time/cost conflict remains displayed as unresolved blanks.
- The Dec. 5 planner makes the 11 AM Wynn WPT Prime and 11:10 AM Venetian event #26 alternatives, not concurrent registrations; a 9 PM Wynn Turbo is only a conditional pivot after the earlier session is over and if registration is still open. The first 8 AM step is planning/checking, not a fabricated live tournament.
- Hotel table uses the Dec. 3–7, 2026 / two-adult / one-room four-night comparison assumption. It shows operator-posted resort fees and separately marked **fee-only** arithmetic; all full stay quotes remain blank. Exact walking minutes are blank/flagged; on-property or pedestrian-bridge connections are not presented as timed routes. No independent hotel-quality ranking is claimed. Venetian's conditional poker rate is noted as not a dated quote.
- Daily-room watch captures Caesars Palace ($100, $1K guarantee, optional $50 add-on), Horseshoe start times, MGM Grand daily starts and its unconfirmed $120 sheet, and Bellagio's re-entry/add-on structures with date validity flagged. Bellagio Saturday is excluded due to conflicting buy-in figures.
- Updated `README.md` with run instructions, methodology, and limitations. Added `.github/workflows/pages.yml` to validate JSON/JavaScript/HTML anchors on PRs, package the four static files, and deploy on pushes to `main` (or an explicit main-branch dispatch) through GitHub Pages Actions.
- Static checks passed: `python3 -m json.tool data.json`, `node --check app.js`, duplicate/broken HTML-anchor audit, source-ID/data integrity audit, and a Node mock-DOM render smoke test (counts, dynamic sections, search, empty state). A local HTTP smoke test returned 200 for `/`, `index.html`, `styles.css`, `app.js`, and `data.json`. No headless browser binary is installed in the workspace; the Arena live preview is running on port 8000 as process `poker-planner-dashboard-6d1b2bb3` for visual review.

## Remaining work

1. Review the live preview for visual/usability issues and make final edits; rerun static checks and `git diff --check`.
2. Commit the dashboard on `arena/ce95f9c0-poker1`, push only that branch, open a PR to `main`, and inspect its checks.
3. Merge with `gh pr merge <explicit-number> --merge` only after the PR and workflow are ready; verify the GitHub Pages Actions run and the live deployment URL.
4. Record the actual PR number, merge commit, workflow result, and verified live URL here. Do not mark the task complete until the live dashboard loads correctly.
