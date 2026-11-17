# Live-site acceptance audit — 2026-11-17

Session `f2ad3bce`, branch `arena/f2ad3bce-poker1`. This audit was deliberately scoped **disjoint** from the
open parallel claims (PR #36 `arena/c0714e1a-poker1`, PR #38 `arena/160f9080-poker1`, PR #39
`arena/11c7cbe6-poker1`, PR #40 `arena/bb9a3717-poker1`): it fetches the **deployed** site and the
**deployed** JSON, checks deployment and workflow health, and walks the project's requirement list against
what is actually published. Nothing in another session's claimed file scope was edited; the four requests
produced by this audit are logged in `COORDINATION.md` for the sessions that own those files.

- Live site: https://karagemop466-tech.github.io/Poker1/
- Deployed commit: `aea688a3981d32d84b43d3c2328278709018cbd0` (= `main` HEAD at audit time).
- Method: every page and JSON file below was fetched **from the live site** (not from the repo) with a
  rendering fetcher, so the client-side tables were seen as a visitor sees them. Workflow and deployment
  state came from the GitHub API. Arithmetic in the rate log was re-computed from the deployed values.

## 1. Deployment health

| Check | Result |
|---|---|
| Pages status | `built`; latest build for commit `aea688a` (created 2026-11-17T00:57:03Z) — exactly `main` HEAD at audit time |
| Pages source | branch `main`, path `/`, URL https://karagemop466-tech.github.io/Poker1/ |
| Landing page | Renders with counts **317 rows · 80 single entry · 106 separate section · 129 unverified · 70 dates · 4/7 verified fees · 4 daily formats · 56 flagged rows** |
| Data vs repo | `data/rates.json`, `data/hotels.json` and the head of `data/tournaments.json` fetched live are **field-for-field identical** to the committed files (tournaments.json is served in 145 chunks; head rows r001–r003 compared exactly) |

The 317-row arithmetic on the landing page is internally consistent: 80 SE + 60 MULTI + 46 RE + 129 UNV + 2 continuation = 317; 60 + 46 = 106 separate-section rows.

## 2. Page-by-page results (all 21 pages fetched live)

| Page | Live result |
|---|---|
| `index.html` | OK. 15 navigation cards, all targets verified below. |
| `pages/single-entry.html` | OK. Filter bar (search, from/to date, min/max buy-in, venue, series, entry rule, single-entry toggle, labels). "80 of 80 rows". Default sort is guarantee ÷ buy-in; every row carries its rule excerpt and official sources. |
| `pages/separate-section.html` | OK. "106 of 106 rows"; MULTI and RE selectable; clause text shown. |
| `pages/unverified.html` | OK. "129 of 129 rows"; states why each rule is unknown (structures PDF publishes no sheet for those rows). |
| `pages/daily.html` | Renders, but the **weekly format map is wrong for Tuesday and Wednesday** — see §4.2. The "Published formats" table itself matches `data/daily.json`. |
| `pages/schedule.html` | OK. 70-date jump list, previous/next-day navigation, per-day primary event + conditional fallback, overlap statements, estimated ends with the estimate caveat. |
| `pages/hotels.html` | Renders fully (fees, tax, true cost, walk columns, walking records with route links, dated rate log) but has **no ≤30-minute-walk filter** — see §4.3. |
| `pages/calculator.html` | OK. Property picker, rate inputs, refusal message when the rate is unverified, and a quote-match message ("A quote for these exact dates was logged on 2026-11-16: $2,412.44 checkout total…"). |
| `pages/venues.html` | OK. Five venues: Venetian 143 rows (80 SE), Wynn 174 rows (0 SE — all Wynn rules are RE or UNV), ARIA/Bellagio/Caesars 0 dated rows with the reason printed. |
| `pages/venue-venetian.html` | OK. 143 of 143 rows; hotel and walking tables. |
| `pages/venue-wynn.html` | OK. 174 of 174 rows; WPT re-entry clause quoted per row. |
| `pages/venue-bellagio.html` | OK. 0 rows as expected (flyers carry no dates); weekly flyer irregularities summarised. |
| `pages/venue-caesars.html` | OK. 0 rows as expected (editorial article, daily add-on format). |
| `pages/venue-aria.html` | OK. 0 rows as expected (no schedule published by ARIA). |
| `pages/search.html` | OK. One search box over tournaments, hotels, venues, daily formats, walking records, rate entries and documents. |
| `pages/monitoring.html` | Renders; discloses that the last check ran from the sandbox (0/93 reachable) and explains that "unreachable" is a network fact, not a change fact. The first scheduled run has not fired yet — see §3. |
| `pages/summary.html` | Renders; two **stale counts** remain in the text — see §4.1. |
| `pages/questions.html` | OK. D1–D7, I1–I17 with open/closed status and how to close each. |
| `pages/suggestions.html` | Renders; built/open/proposed lists present, but **8 of its links are broken** — see §4.1. |
| `pages/flagged.html` | Renders; F1–F52 sections, but **1 link is broken** — see §4.1. |
| `pages/review.html` | OK. R1–R14 handling log and the source log. |

Cosmetic, already being fixed by PR #40 ("Restore the trip cost calculator: drop duplicate renderers left by
the merge"): some pages print a duplicated section heading (`# Flagged for review` twice on flagged.html,
"## Hotels here"/"## Hotels at this venue" and "## Walking records" twice on the venue pages, and the same
duplication on monitoring.html and summary.html).

## 3. Workflow health

| Workflow | Schedule (verified in the workflow files on `main`) | Last runs |
|---|---|---|
| `pages.yml` (Deploy static site to GitHub Pages) | PR validation + push deploy | PR-triggered runs for #39/#40 active at audit time; the merge-triggered run for `aea688a` succeeded (run `43991740818`) |
| `monitor.yml` (Monitor official sources) | `cron: "17 7 * * *"` — daily 07:17 UTC, plus `workflow_dispatch` | All runs so far are push-triggered; **the first scheduled run is still due** (audit ran ~01:30 UTC). Until it fires, `data/monitoring.json` keeps the sandbox result (0 of 93 reachable), which the monitoring page discloses. |
| `source-facts.yml` (Check official source facts) | `cron: '47 6 * * 0'` — weekly, Sundays 06:47 UTC | Last successful run on a session branch (run `43990392709`); next scheduled run 2026-11-22 |

The 93-source count in `data/monitoring.json` (row-level monitor, rows + hotels + walking + rates) versus the
74-source count in `data/change_log.json` (provenance archive in `data/sources.json`) are **two different
manifests by design**, not a conflict: the row-level monitor checks the URLs that back published rows; the
source-facts job archives the text of the underlying documents.

## 4. Defects found by this audit (logged for the owning sessions)

All four items below are inside the file scopes claimed by open PRs, so they are **requests, not edits** (the
exact requests are recorded in `COORDINATION.md`). None was silently fixed by this session.

### 4.1 Eleven broken links in three published documents (live 404s, confirmed)

The site renders `EXECUTIVE_SUMMARY.md`, `SUGGESTIONS.md` and `FLAGGED.md` inside `pages/summary.html`,
`pages/suggestions.html` and `pages/flagged.html` by fetching the markdown client-side. Those documents use
repo-root-relative links so they work on GitHub, but from a page inside `/Poker1/pages/` the browser resolves
them against the page URL, producing `/Poker1/pages/pages/…`:

| Document | Broken links | Example |
|---|---|---|
| `EXECUTIVE_SUMMARY.md` | 3 | `pages/calculator.html`, `pages/monitoring.html`, `pages/search.html` |
| `SUGGESTIONS.md` | 8 | `pages/calculator.html` ×2, `pages/monitoring.html` ×2, `pages/venues.html`, `pages/search.html`, `pages/hotels.html`, `pages/daily.html` |
| `FLAGGED.md` | 1 | `pages/monitoring.html` |

Confirmed live: https://karagemop466-tech.github.io/Poker1/pages/pages/calculator.html returns GitHub Pages'
404 page.

Why CI missed it: `scripts/check_links.py` validates the links of the **generated HTML**, and the markdown
documents are fetched and rendered client-side, so the rewritten URL never appears in a checked file; the
headless smoke test renders pages but does not resolve the markdown's relative link targets against the page
URL.

Fix options (owner's choice): (a) rewrite those links as bare filenames (`calculator.html`) — correct from
`/Poker1/pages/` but wrong when the markdown is read on GitHub; (b) prefix the links with the site base path in
the markdown renderer (`assets/app.js`), which keeps GitHub working; (c) teach `check_links.py` to resolve every
link inside the fetched markdown against its hosting page URL so the class of bug cannot return.

### 4.2 Daily-feed weekday map drops Tuesday and Wednesday (`assets/app.js`)

The builder at the "weekly format map" section filters with
`x.days.indexOf(d.slice(0,3)) >= 0`, i.e. it only matches when the weekday abbreviates to a **substring** of
the stored range string. `data/daily.json` stores `Monday-Thursday` for the noon $200 format and
`Monday-Sunday` for the 6 p.m. nightly, so:

- Monday and Thursday match ("Mon", "Thu" occur in the string);
- Tuesday and Wednesday match neither format, and the map prints "No daily format published for this
  weekday" — although both stored ranges include them;
- the nightly row also loses Tuesday/Wednesday.

Observed live on https://karagemop466-tech.github.io/Poker1/pages/daily.html (Monday: 12 PM + 6 PM; Tuesday:
none; Wednesday: none; Thursday: 12 PM only; Friday–Sunday as stored). The published-formats table on the same
page is correct; only the weekday map is wrong. Fix: expand each stored range to its weekday list in the
renderer (or store the weekday list in `data/daily.json` at build time).

### 4.3 Missing "≤30 min walk" filter on the hotels table (explicit project requirement)

The brief asks for "walking-distance verification … with a '≤30 min walk' filter". The verification exists
(routed OSM foot times, route links, internal walks marked, 30-minute rule applied and chips shown
"within 30"/"over 30"), but the hotels table has **no filter control** — the filter bar exists only on the
tournament pages. A reader cannot, for example, hide the hotels that fail the 30-minute rule for the Wynn
poker room (Bellagio 31, Caesars 32, ARIA 43). Fix: add a toggle or per-venue select to the hotels renderer
(only-show-within-30 for a chosen poker room). Suggestion P6 (Google/Apple Maps links next to the OSM route)
complements this and stays open.

### 4.4 Stale counts inside `EXECUTIVE_SUMMARY.md`

The document was partly updated for 317 rows but two passages still describe the 316-row build:

- Intro: "all **316** rows still match their official source today" — the dataset is **317** rows.
- Bottom line: "**105 rows** sit in the separate section … **45** Wynn rows" — the data has **106** separate-section
  rows, because the restored TORSE (2 Day) row (flag F21) is the 46th re-entry row.

The landing page and the separate-section page (both generated from the data) show the correct 106. PR #36's
current diff still carries the stale text, so the request is logged for its owner. No number in the data files
is affected.

## 5. Requirements traceability matrix

Every requirement from the project brief, mapped to what implements it on the live site, with verification
status at the deployed commit.

| # | Requirement | Where it lives | Live status |
|---|---|---|---|
| R1 | Find live upcoming tournaments near the Strip; rank by cost vs prize pool; single entry focus | `pages/single-entry.html` (80 verified rows, ranked by guarantee ÷ buy-in), `pages/summary.html` §1 top-9 table | ✅ Live |
| R2 | Separate section for events where money buys advantage (re-entry, rebuy, add-on) | `pages/separate-section.html` (106 rows: 60 multi-flight + 46 re-entry), Caesars daily add-on and Wynn Friday rebuy formats noted on venue/daily pages | ✅ Live |
| R3 | Hotels within walking distance; distance vs cost/quality trade-off; true cost per night | `pages/hotels.html` (7 properties; fees, tax, true cost from dated engine quotes), `data/walking.json` + walking records on venue pages | ✅ Live; ✗ the ≤30-min **filter** is missing (§4.3) |
| R4 | Resort fees factored into true cost | Verified $55 + 13.38% tax for Venetian/Palazzo; $55 fee for Wynn/Encore; blanks elsewhere, never inferred | ✅ Live |
| R5 | Play-all-day 8 AM schedule ambition | `pages/schedule.html` (70 days, primary + conditional fallback, overlap logic); `pages/summary.html` answers the 8 AM question (earliest cash SE start 10:10 AM; 9:10 AM satellite on Dec 12; Wynn registration opens 8 AM) | ✅ Live; earliest verified starts re-checked against the data in this audit |
| R6 | Executive summary | `EXECUTIVE_SUMMARY.md` → `pages/summary.html` | ✅ Live; two stale counts (§4.4) |
| R7 | Suggestions section for review-before-implementation | `SUGGESTIONS.md` → `pages/suggestions.html` (built S1–S15, open S16–S23, proposals P1–P6) | ✅ Live; 8 broken links (§4.1) |
| R8 | Clear list of questions/info/answers needed before deciding | `QUESTIONS.md` → `pages/questions.html` (D1–D7 decisions, I1–I17 information gaps, C section: how to discover each) | ✅ Live |
| R9 | No manual input; work autonomously; verify from official sources; no hallucinations | Every row/hotel/rate carries official source URLs and retrieval dates; blanks stay blank; flags publish every irregularity | ✅ Enforced by generator + validator; spot-verified live in this audit |
| R10 | Repo review, line by line, with links; flag irregularities | `REVIEW.md` (R1–R14) → `pages/review.html`; `FLAGGED.md` F1–F52 → `pages/flagged.html` | ✅ Live; 1 broken link on flagged page (§4.1) |
| R11 | GitHub Pages live site, clean landing page, category subpages, dashboard-style tables | 21 pages, shared stylesheet, no external CDN | ✅ Live (all 21 fetched successfully) |
| R12 | Verification discipline: source link on every row; blank + flagged when unconfirmed | `data/tournaments.json` rows each carry `sources[]`; unverified page lists 129 rows with reasons; `check_links.py` enforces approved official hosts | ✅ Verified live in head rows and on every page fetched |
| R13 | Parallel-session coordination via COORDINATION.md | Board with claims, scopes, handoffs, conflict log | ✅ Maintained (this audit is filed under its own claim) |
| R14 | Trip cost calculator: entries × buy-in + nights × true hotel cost | `pages/calculator.html` (verified-quote driven; refuses unverified inputs; shows stay-window contents and like-for-like comparison) | ✅ Live |
| R15 | Scheduled automatic re-check of official URLs; mark changed rows | `scripts/monitor_sources.py` + `monitor.yml` (daily 07:17 UTC) + `data/monitoring.json`/`row_snapshot.json` → `pages/monitoring.html`; weekly provenance re-fetch via `source-facts.yml` | ✅ Configured; first scheduled run still due at audit time (§3) |
| R16 | Read structure sheets; remove "unverified" where confirmed | 37/37 DSE IV + 15/15 NYE sheets and 8/8 WPT structure sections read; per-sheet log in `research/structure-sheets-verification.md`; 129 rows honestly remain UNV | ✅ Live |
| R17 | "Last checked" date per row | `last_checked`/`verified_on` on rows, hotels, rates | ✅ Verified in live JSON |
| R18 | Rates as a dated log, not a single value | `data/rates.json` (5 quotes) + rate-log table on hotels page + calculator matching | ✅ Live; arithmetic re-verified in §6 |
| R19 | One page per venue with its events and hotels | `pages/venues.html` + 5 venue pages | ✅ Live |
| R20 | Search box across all tables | Filter-bar search on every table + `pages/search.html` global search | ✅ Live |
| R21 | Like-for-like hotel comparison: checkout total, nightly average, mandatory fee, tax, parking, cancellation deadline, timestamp | Every quote stores all seven fields; parking rates stored per property (Venetian/Palazzo $20/day verified) | ✅ Verified in live `rates.json`/`hotels.json` |
| R22 | Overlap check via start time, late-registration cutoff, plausible duration; primary + fallback per day | `pages/schedule.html` primary/fallback rows with estimated ends and the estimate caveat | ✅ Live |
| R23 | Ratio (guaranteed pool ÷ entry fee) as descriptive value, not forecast; bounty/flight events labelled | Ratio column labelled "Descriptive ratio only, not a forecast"; bounty and satellite labels on rows | ✅ Live |
| R24 | Date selector showing only chosen days | From/to date inputs in the filter bar + schedule day picker | ✅ Live |
| R25 | Structured rule fields (single-entry, re-entry, add-on, fee) with excerpt + retrieval date | `rules{}` object per row, each field with excerpt, source label+URL, `retrieved_on`, clause number | ✅ Verified in live JSON head |
| R26 | Walking-route check with 30-minute limit | 12 routed pairs, route links, internal marking, over-30 chips | ✅ Live; filter missing (§4.3) |
| R27 | Change monitoring of values | Row snapshot comparison; monitoring page lists changed rows and flag rows | ✅ Configured (§3) |
| R28 | Daily live-schedule feed per morning | `data/daily.json` from Wynn's official daily poster + structures; rendered on `pages/daily.html` | ✅ Live; weekday map bug (§4.2) |
| R29 | "Single-entry / freezeout confirmed" toggle filter | "Single entry only" checkbox in the shared filter bar | ✅ Live |
| R30 | Live hotel rate lookup + auto true-cost calculation (rate + fee + 13.38% tax) | Booking-engine quotes logged with itemised breakdowns; calculator and hotels page compute and re-verify the identity | ✅ Live for the five logged windows; Wynn engine blocked (flagged F45/F47) |
| R31 | PR + merge without waiting; publish flags on a "Flagged for Review" page; do not merge a broken site | `pages/flagged.html` publishes all flags with sources; CI builds and smoke-tests before deploy | ✅ Followed across sessions; this audit adds its own PR under the same rules |

## 6. Rate-log arithmetic re-verified (from the deployed `data/rates.json`)

| Stay | Room rates sum | + resort fees | ×13.38% tax | Engine total | ÷ nights = true cost | Check |
|---|---|---|---|---|---|---|
| Nov 18–20 (2n) | $728.50 | $110.00 | $112.19 | $950.69 | $475.35 | ✅ |
| Nov 26–29 (3n) | $1,962.75 | $165.00 | $284.69 | $2,412.44 | $804.15 | ✅ |
| Dec 13–20 (7n) | $1,704.75 | $385.00 | $279.63 (engine) | $2,369.38 | $338.48 | ✅ |
| Jan 1–6 (5n) | $3,746.25 | $275.00 | $538.05 (engine) | $4,559.30 | $911.86 | ✅ |
| Jan 10–15 (5n) | $1,136.25 | $275.00 | $188.83 (engine) | $1,600.08 | $320.02 | ✅ |

(Where the engine's tax line differs from a raw 13.38% computation by a cent, the engine's own printed total is
used — the stored identity checks compare against the engine figure, which is the like-for-like requirement.)

## 7. Data spot-checks re-verified from the deployed JSON

- Landing counts: 317 = 80 SE + 60 MULTI + 46 RE + 129 UNV + 2 CONT; 106 separate-section. ✅
- Earliest start in the dataset: **9:10 AM** on Dec 12, 2026 — row r120, $260 NLH Turbo Milestone Satellite,
  prize "2 seats to Event #47", entry rule SE with `satellite`/`milestone-satellite` labels. ✅ (matches the
  summary's 8 AM answer)
- Earliest **cash** single-entry start: **10:10 AM** (RaceDay Stack rows, Nov 19–21). ✅
- Venue row counts: Venetian 143 (80 SE) + Wynn 174 (0 SE) = 317. ✅
- Hotels: 4 of 7 verified resort fees ($55 Venetian/Palazzo/Wynn/Encore); room tax numeric only for
  Venetian/Palazzo (13.38%); true cost filled only where a dated quote exists ($911.86 Venetian, $320.02
  Palazzo). ✅

## 8. Conclusion

The deployed site at `aea688a` is a faithful render of the committed dataset: all 21 pages load, every count
cross-checks, the rate log reproduces to the cent, and the verification discipline (source links, blanks, flags)
is visible on every row. Four actionable defects were found and are logged in `COORDINATION.md` for the
sessions that own the affected files: broken markdown-derived links (11), the daily-feed weekday map bug, the
missing ≤30-minute-walk filter, and two stale counts in the executive summary. None of them blocks the site;
all are published transparency items consistent with the project's "flag, don't hide" rule.

## 9. Post-audit `main` movement (re-checked before this record was pushed)

While this audit was in progress, PRs #38, #39, #41 and #42 merged into `main` (new head `e9ca3d6`), including
a commit that corrects the executive-summary totals. Every finding above was therefore re-verified against
`e9ca3d6` before publication:

| Finding | Status on `main` at `e9ca3d6` |
|---|---|
| §4.1 Eleven broken markdown-derived links | **Still open.** `EXECUTIVE_SUMMARY.md` 3, `SUGGESTIONS.md` 8, `FLAGGED.md` 1 relative `pages/…` links remain (the earlier count for SUGGESTIONS.md is unchanged — 8 link matches, 7 lines). |
| §4.2 Weekday map drops Tuesday/Wednesday | **Still open.** `assets/app.js` line 531 is unchanged. |
| §4.3 Missing ≤30-min-walk filter | **Still open.** No walk filter exists in `assets/app.js` on `main`. |
| §4.4 Stale executive-summary counts | **Half fixed.** The intro now reads "all **317** rows in the current dataset match their official sources". The bottom-line bullet still says "**105 rows** sit in the separate section … **45** Wynn rows"; the data has 106 / 46, and §2 of the same document correctly says "Re-entry offered (46 rows)". |

The §4 requests logged in `COORDINATION.md` were updated to this state before this session's PR was opened.
Note for readers: the deployment, page and data results in §1–§3 and §6–§7 describe the deployed site at
`aea688a`, which was the live commit during the audit; the Pages deployment of `e9ca3d6` had not completed at
the time of the re-check.

## 10. CI defect found and fixed by this session: global concurrency group cancelled every validation

While merging this audit, PR #47's `validate` check was cancelled within seconds of creation. The cause is in
`.github/workflows/pages.yml`: a single global concurrency group (`pages`) with `cancel-in-progress: true`
meant **every new run anywhere in the repository cancelled the run in flight** — including validations of other
sessions' PRs and, worse, a push-to-main deployment could be cancelled by any PR validation starting. Runs
cancelled by this in the audit window alone: PRs #38, #39, #41 and #47 (verified in the Actions list).

`.github/workflows/pages.yml` was unclaimed by any open PR, so session `f2ad3bce` claimed and fixed it (the
claim is recorded in `COORDINATION.md`). The fix keeps the protection that matters and removes the collision:

| Stream | Old group | New group |
|---|---|---|
| Push to `main` (the deploy stream) | `pages` (shared with everything) | `pages-deploy` — serialized; a newer main push still cancels an older deploy, so the site always reflects the latest merged state |
| `pull_request` validation | `pages` (shared with everything) | `pages-validate-pr<PR number>` — a new push to the same PR supersedes its older run; other PRs are never affected |
| `workflow_dispatch` | `pages` | `pages-manual-<run id>` — unique per run, never cancelled |

This change is included in PR #47 so the PR's own validation runs under the repaired configuration.
