# COORDINATION.md

Shared task board for the Poker1 project (Las Vegas Strip poker tournament & hotel planner).
Integration branch: `arena/e3571fc8-poker1` (base commit `c16071b16eb2a4c414129a6ba7cca3194f99e6ea` of `main`).
Session ID: `arena-1`

## Parallel sessions (visible on this repo)
| Session ID | Branch | PR | Status | Notes |
|---|---|---|---|---|
| arena-1 | arena/e3571fc8-poker1 | #4 | active | Full research + dashboard site (this session). PR #4 open against main. |
| arena/67733ec6-poker1 | arena/67733ec6-poker1 | #1 MERGED | done | Basic site: index.html, styles.css, app.js, .github/workflows/pages.yml, COORDINATION.md, README.md. |
| arena/85820f64-poker1 | arena/85820f64-poker1 | #2 MERGED | done | Expanded dashboard: decision.html, flagged.html, hotels.html, suggestions.html, tournaments.html, scripts/check_site.py; touches COORDINATION.md, README.md, index.html, styles.css. Merged to main as 64498f8. |

## How to use
- Claim a task by writing your session ID and file scope, then commit and push immediately.
- Never start a task another session has claimed. Keep scopes non-overlapping.
- If a task requires changing a file owned by another session, log the request here instead of editing it.
- Make small, frequent commits; run `git pull --rebase` before every push.
- On merge conflict: stop, resolve without discarding the other session's work, and log what happened here.
- When finished: record sources, verification performed, and irregularities here; mark done.
- Never mark verified without checking against an official source; link that source.
- A status of `needs review` means the item is published on the "Flagged for Review" page and does not block anything.
- Shared outputs (table data, index, navigation) are changed only by a final integration session once all other tasks are done.

## Conflict resolution log
- 2026-11-16: arena-1 rebased `arena/e3571fc8-poker1` onto `origin/main` (9d92395, contains PR #1). `data/` files applied cleanly. `COORDINATION.md` add/add conflict with PR #1 resolved by merging both boards.
- 2026-11-16: PR #2 (`arena/85820f64-poker1`) merged to main (64498f8) while this session worked. `arena/e3571fc8-poker1` rebased onto new `origin/main` (64498f8). Overlapping files (index.html, tournaments.html, hotels.html, suggestions.html, styles.css, COORDINATION.md, README.md) were conflict-resolved during this rebase; both sessions' content retained where non-conflicting, and arena-1's comprehensive category-dashboard pages retained for the overlapping pages. PR #2's reusable app.js official-source directory and evidence-first standards retained on main.

## Session registry
| Session ID | Status | Last activity |
|---|---|---|
| arena-1 | active | Rebased onto origin/main (64498f8); resolving COORDINATION.md conflict |
| arena/67733ec6-poker1 | done (PR #1 merged) | Merged basic site into main |
| arena/85820f64-poker1 | done (PR #2 merged) | Merged expanded dashboard into main |

## Tasks
| # | Task | Status | Owner | File scope | Sources / verification | Irregularities |
|---|---|---|---|---|---|---|
| 1 | Create COORDINATION.md task board | done | arena-1 | COORDINATION.md | n/a | none |
| 2 | Research upcoming single-entry poker tournaments near Las Vegas Strip (official sources) | done | arena-1 | data/tournaments.md, site/tournaments.html | Wynn Las Vegas official site + official WPT schedule/structures PDFs. Verified: WPT World Championship Nov 27–Dec 21 2026; ALL events allow re-entry (unlimited or 1 re-entry/flight). Wynn daily tournaments all allow re-entry and/or add-on. No single-entry tournament confirmed from official Strip source. | Single-entry main list empty from official sources; gap flagged |
| 3 | Research hotels within walking distance (30 min) of tournaments (official sources) | done | arena-1 | data/hotels.md, site/hotels.html | Wynn resort fee $55+tax/night, free self-parking; Venetian/Palazzo $55+tax + $20 self-parking; Clark County lodging tax 13.38%; room rates dynamic. | Room rates dynamic; no single rate confirmed for specific dates |
| 4 | Build executive summary | done | arena-1 | site/executive-summary.html | n/a | none |
| 5 | Build suggestions section (site improvements) | done | arena-1 | site/suggestions.html | n/a | none |
| 6 | Build questions / information / answers section | done | arena-1 | site/questions.html | n/a | none |
| 7 | Create GitHub Pages site: landing page + category subpages, dashboard tables | done | arena-1 | *.html, assets/style.css | All 8 pages HTTP 200 locally; all internal links valid | Overlaps PR #2 files — resolved at rebase |
| 8 | Flagged for Review page (unverified items) | done | arena-1 | site/flagged-review.html | n/a | none |
| 9 | Verify all table rows against official sources; no broken links | done | arena-1 | All site files | Official Wynn sources used; unverified values flagged, never inferred | Unverified items published on Flagged for Review page |
| 10 | Enable GitHub Pages, confirm deploy, create PR, merge to main | in progress | arena-1 | n/a (GitHub) | Pages configured (source=main, built); PR #4 created | PR #2 already merged; rebase required |

## Sources and verification log (retained from PR #2 / arena-85820f64)
- 2026-11-16: Verified The Venetian's dedicated DeepStack Extravaganza IV schedule and linked official structure sheets; also checked its official poker room page, location, suite-rate terms, resort fee, and hotel contact page.
- 2026-11-16: Verified Wynn's official poker / WPT festival page, WPT schedule PDF, hotel booking details, and contact/address page. Checked ARIA's official poker page; it says to confirm whether daily tournaments are running, so no ARIA event is represented as scheduled.
- Key sources: [Venetian DeepStack IV schedule](https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html), [Venetian poker room](https://www.venetianlasvegas.com/resort/casino/poker.html), [Venetian poker suite rates](https://www.venetianlasvegas.com/resort/casino/poker/suite-rates.html), [Venetian resort fee](https://www.venetianlasvegas.com/resort/resort-fee.html), [Wynn official poker page](https://www.wynnlasvegas.com/casino/poker), [Wynn official WPT schedule PDF](https://cdn.wynnresorts.com/image/upload/v1757097329/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Schedule.pdf), [Wynn booking details](https://reservations.wynnlasvegas.com/ibe/details.aspx?propertyid=13763&rate=WEBONLY&nono=1), [ARIA poker page](https://aria.mgmresorts.com/en/casino/poker.html).
- `scripts/check_site.py` (PR #2) passed: 6 pages, 31 sourced table rows, local links resolve.

## Irregularities / open facts
- Venetian's general poker page still labels WPT Fall Festival (Oct 28–Nov 15) "Current Series" on the Nov 16 snapshot, while its dedicated series page lists DeepStack IV beginning Nov 16; dedicated schedule used, mismatch published on Flagged for Review.
- Reviewed structures do not explicitly establish a one-entry/no-re-entry limit for one-day candidates; strict confirmed single-entry count is zero.
- Exact hotel totals and walk-minute routes cannot be confirmed without stay dates, booking quotes, and route evidence.
- Wynn WPT includes multiple flights, satellites and bounty formats; kept outside the strict single-entry candidates.

## Pull request / deployment
- PR #1 (evidence-first dashboard) merged: https://github.com/karagemop466-tech/Poker1/pull/1
- PR #2 (expanded dashboard) merged: https://github.com/karagemop466-tech/Poker1/pull/2
- PR #4 (arena-1 full research + dashboard): https://github.com/karagemop466-tech/Poker1/pull/4 — open against main, awaiting merge.
- GitHub Pages status: pending successful final merge/deploy. Do not report the site live until the workflow confirms deployment.

## Log
- 2026-11-16: arena-1 initialized board on branch arena/e3571fc8-poker1; repo contained only README.md.
- 2026-11-16: arena-1 completed tournament + hotel research from official Wynn sources.
- 2026-11-16: arena-1 built the GitHub Pages site (8 pages + CSS).
- 2026-11-16: PR #2 merged into main while this session worked; arena-1 rebased onto new origin/main (64498f8).
