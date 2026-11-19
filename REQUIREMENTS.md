# Requirement coverage audit

Every line of the brief, one row each, with the file that satisfies it, the page where a reader can see
it, and — for anything that carries a value — the official source. Status is one of:

* **Done** — the requirement is implemented and the evidence is on the site.
* **Partial** — implemented, but a documented limit stops it from being complete.
* **Blocked** — no official source answers it; the site says so and names the question that would close it.
* **Out of reach for this repo** — needs something a static site cannot have.

Read 2026-11-19 (session `dd06081b`). Sources for this audit: the whole repository at `main` @ `f5ecde0`,
every gate re-run (see `COORDINATION.md`), and the live re-read of the cited official pages recorded in
`research/requirements-audit-dd06081b/README.md`.

## 1. Planning logic — trip, entry rules, comparison, hotel, day plan

| # | Requirement | Status | Where it lives | Evidence / limit |
|---|---|---|---|---|
| 1.1 | Fix trip dates, nightly budget and a quality floor | **Partial** | `EXECUTIVE_SUMMARY.md` "What the next decision costs"; `QUESTIONS.md` D3/D4; `data/rates.json` | A planning scenario is stated as an assumption, not a preference: Dec 13–20, two adults, private king suite, ≤ $350/night inclusive, refundable, ≤ 30-minute evidenced walk. Five dated quotes bracket $320.02–$911.86 true cost/night. **No input is required from you**, so the scenario is labelled a scenario everywhere. |
| 1.2 | Get the structure sheet and the written maximum-entry / no-rebuy / no-add-on rules; drop anything that is not single entry | **Blocked** | `data/structure_rules.json` (52 sheets), `data/tournaments.json` → `rules.{single_entry,re_entry,add_on,fee}`; [Flagged](pages/flagged.html) K | All 37 DSE IV and 15 NYE sheets read; every one quotes its own clause. **None prints a maximum-entry, no-rebuy or no-add-on clause** — re-read today for #5, #6 and #30. So 80 rows are candidates, 0 are confirmed freezeouts, and the strict shortlist is empty. Asking the poker room is the only path (`QUESTIONS.md` C1). |
| 1.3 | Compare only surviving events on guaranteed pool, buy-in, stack, blind duration, payout structure, schedule fit | **Done** | [Freezeout shortlist](pages/single-entry.html), [Payout rules](pages/payouts.html), [Schedule](pages/schedule.html) | Because 1.2 survives zero events, the comparison runs over candidates and says so: guarantee, buy-in, starting stack, level minutes, printed payout rule and same-day fit, each with its own official link. Guarantee ÷ entry fee is shown as a **descriptive ratio**, never a forecast. Bounty, satellite and flight rows carry their own labels and are not ranked with cash-pool events. |
| 1.4 | Itemised hotel totals for the same stay; walking route under 30 minutes | **Partial** | [Hotels](pages/hotels.html), [Calculator](pages/calculator.html); `data/rates.json`, `data/walking.json` | Five itemised engine quotes (nightly rates, resort fee, tax total, checkout total, cancellation, rate timestamp). Walks are **routed on the OSM foot network**, not published — no property publishes a time (F49); four pairs fail 30 minutes and stay listed and flagged. Live quotes for arbitrary dates are **not obtainable**: Wynn's engine renders client-side and Venice returned a loading shell on the Dec 13–20 lookup. |
| 1.5 | One event per day first; evening events only where the player can realistically exit the earlier event | **Done** | [Schedule](pages/schedule.html) (`primary_id`, `fallback_id`, `second_entry_id`), `data/schedule.json`, `scripts/check_schedule.py` | 70 dates, 274 entry rows, 170 overlap pairs. Finish = start + published levels + breaks in **absolute minutes**, so an after-midnight finish cannot read as finished. 0 publishable impossible fallbacks; every fallback is checked for reachability against the earlier event's own estimate and the later event's registration close. |
| 1.6 | Reconfirm schedules, rates and policies before nonrefundable payment | **Done** | [Executive summary](pages/summary.html) booking hold; [Monitoring](pages/monitoring.html) | The published decision is **hold** until a written freezeout ruling exists, and the monitor re-fetches every official URL daily. |

## 2. The numbered asks

| # | Requirement | Status | Where it lives | Evidence / limit |
|---|---|---|---|---|
| 2.1 | Date filter that shows only events on chosen days | **Done (added this session)** | Filter bar on every tournament table + the schedule page: quick presets (today, this weekend, next 7 / next 30 days, all dates) and a per-date chip picker built from the dataset's own dates | `assets/app.js` `Filters()`; headless test `scripts/check_date_filter.js` wired into `npm test`. |
| 2.2 | Store single-entry, re-entry, add-on and fee values separately, each with its source excerpt and retrieval date | **Done** | `data/tournaments.json` → `rules.single_entry`, `rules.re_entry`, `rules.add_on`, `rules.fee`, each `{value, excerpt, source{label,url}, retrieved_on, clause}` | `scripts/check_links.py` fails the build if any field loses its excerpt, source or date. |
| 2.3 | Flag two events that cannot be played in sequence | **Done** | `data/schedule.json` `conflicts`, `conflicts_unplannable`, `conflicts_join_in_progress`; [Schedule](pages/schedule.html) | 170 flagged pairs. A pair is only called *impossible* when both sheets publish a level count; a sheet with a level length and no count is recorded as **undecidable**, never as a conflict. |
| 2.4 | Official-address walking times per hotel–venue pair, 30-minute limit applied | **Partial** | `data/walking.json` (12 pairs), [Hotels](pages/hotels.html) | Times exist, are reproducible (geocoding + routing links on each row) and the limit is applied, but they are **OSM-routed, not official**, because no property publishes one. Google/Apple can only be read by a human or a rendering browser; the site links maps for cross-checking instead of claiming a Google measurement. |
| 2.5 | Re-check official pages on a schedule and flag any value that changed | **Done** | `.github/workflows/monitor.yml` (daily 07:17 / 15:17 UTC), `scripts/monitor_sources.py`, `data/monitoring.json`, `data/changes.json`; per-row "Source changed" badge in every table | Facts-level hashing (money, %, dates, times, rule words), not raw HTML. One known false mark is published as F85 rather than hidden. |
| 2.6 | Live-data feed / scraper pulling each Strip room's official daily schedule each morning | **Partial** | `.github/workflows/schedule-feed.yml`, `data/schedule_feed.json`; [Daily feed](pages/daily.html) | Runs each morning before 8 AM Las Vegas time. First production check reached 12 of 20 operator URLs; failures are shown with attempt time and the last readable capture, and **a failed fetch is not reported as a closure**. No room publishes a machine-readable daily schedule, so the feed stores official excerpts, not parsed rows. |
| 2.7 | "Single-entry / freezeout confirmed" toggle filter | **Done** | Filter bar, "Written freezeout confirmed" checkbox on every tournament table | Honest about the result: the toggle currently matches **zero** rows, because no sheet affirms a freezeout (2.1 above). |
| 2.8 | Live hotel rate lookup by date + auto true cost/night = rate + resort fee + 13.38% tax | **Partial** | [Calculator](pages/calculator.html), `data/rates.json` | True cost per night is the engine's **own checkout total ÷ nights**, and the 13.38% rate (Clark County TLE guide) reproduces every logged quote exactly. A *live* lookup for new dates is not possible from a static site or a text fetch; the log keeps every dated quote instead of overwriting one. Tax is only applied where an official authority prints it. |
| 2.9 | Walking-distance verification from each hotel to the Venetian poker room with a "≤30 min walk" filter | **Partial** | `data/walking.json`, [Hotels](pages/hotels.html) filter "≤30 min walk to a poker room" | The filter works and the destination is the room's real building (Palazzo level 2 — the poker page's own wording), not the resort's street address. The timing method remains OSM routing (2.4). |

## 3. Site and verification asks

| # | Requirement | Status | Where it lives | Evidence / limit |
|---|---|---|---|---|
| 3.1 | GitHub Pages site, clean landing page, subpages by category, dashboard feel | **Done** | <https://karagemop466-tech.github.io/Poker1/> — `index.html` + 31 pages in `pages/` | No CDN, no framework, inlined CSS/JS, `data-page` renderers, print stylesheet. |
| 3.2 | All entries and findings in simple tables | **Done** | Every tournament page, [Payout rules](pages/payouts.html), [Strip rooms](pages/strip-rooms.html), [Payout/daily formats](pages/daily.html) | Sortable, filterable, blank cells printed as `blank` — never as 0 or an estimate. |
| 3.3 | Every row links to an official source; unconfirmed values blank and flagged | **Done** | `scripts/check_links.py` (approved official hosts + HTTPS on every row), `scripts/verify_rows.py` (1,386 field checks, 0 hard failures), `scripts/verify_against_snapshots.py` (0 unexplained mismatches) | 335 rows verified against archived official text; a value not found there is a failure, not a blank guess. |
| 3.4 | Executive summary | **Done** | [Summary](pages/summary.html) / `EXECUTIVE_SUMMARY.md` | Decision, what would change it, cost of the next decision, coverage. |
| 3.5 | Suggestions section so a path can be chosen before implementing | **Done** | [Suggestions](pages/suggestions.html) / `SUGGESTIONS.md` | Implemented register, open items S16–S23, and a ranked "next" list with effort and decision value. |
| 3.6 | A clear list of questions, information and answers that must be answered before a decision | **Done** | [Questions](pages/questions.html) / `QUESTIONS.md` | Decisions D1–D7, gaps I1–I18 with known/missing/how-to-close, and who to ask. |
| 3.7 | Flagged-for-review page with source links | **Done** | [Flagged](pages/flagged.html) / `FLAGGED.md` (F1–F87) | Every flag quotes the official text, links it and states the effect on the data. |
| 3.8 | No manual input required from you | **Done** | This audit + `COORDINATION.md` session record | The scenario, the hold decision and every gate run were produced without asking you to type anything. |
| 3.9 | Parallel-session coordination, PR, merge, deploy | **Done** | `COORDINATION.md` | Claim committed before any change; integration record with PR link, merge commit and Pages build result. |

## 4. What genuinely cannot be closed from here

1. **Written one-entry / no-rebuy / no-add-on rules.** No Venetian, Wynn, Caesars, MGM or independent
   room publishes them for the events in scope. Until a poker room answers in writing, the strict
   shortlist is empty by design. This is the single most important open item, and it is why the site
   says *hold* instead of *book*.
2. **Live prices and live availability.** Both large operators' booking engines render client-side. A
   static site can store dated quotes and link the official engines; it cannot query them.
3. **Official walking times.** None exist. Google/Apple require a human or a rendering browser.
4. **Published finish times.** None exist. The schedule's finish is an arithmetic bound from the printed
   level structure, labelled as an estimate on every row.
5. **The DeepStack Showdown (Jan 11 – Feb 14, 2027)** — see F89. Everything needed to add it is public;
   it is a data-gathering session, not a missing source.
6. **8 AM starts.** The earliest printed Venetian start in this window is 10:10 AM; Wynn's 4-hours-before
   figure is a *registration* opening, not play. An all-day 8 AM itinerary cannot be built from the
   official schedules as they stand.
