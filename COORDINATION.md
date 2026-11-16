# COORDINATION.md

Shared task board for the Poker1 project (Las Vegas Strip poker tournament & hotel planner).
Session ID: `arena-1` (branch `arena/e3571fc8-poker1`, PR #4).

## Parallel sessions (visible on this repo)
| Session ID | PR | Status | Contribution |
|---|---|---|---|
| arena/67733ec6-poker1 | #1 MERGED | done | Evidence-first dashboard foundation: index.html, styles.css, app.js, README.md, COORDINATION.md, .github/workflows/pages.yml |
| arena/85820f64-poker1 | #2 MERGED | done | Expanded dashboard: decision.html, flagged.html, hotels.html, suggestions.html, tournaments.html, scripts/check_site.py |
| arena/85820f64-poker1 | #6 MERGED | done | Record final research and Pages deployment verification (COORDINATION.md) |
| arena/e73e692a-poker1 | #5 MERGED | done | Venetian/Wynn/Bellagio research site (T1-T7); review.html, REVIEW.md, data/*.json, pages/*.html; claimed Pages workflow run 43931551346 |
| arena-1 | #4 | merging | Full research + category-dashboard site (verified Wynn tournament + hotel data); 8 root pages + assets/style.css |

## How to use
- Claim a task by writing your session ID and file scope, then commit and push immediately.
- Never start a task another session has claimed. Keep scopes non-overlapping.
- If a task requires changing a file owned by another session, log the request here instead of editing it.
- Make small, frequent commits; run `git pull --rebase` before every push.
- On merge conflict: stop, resolve without discarding the other session's work, and log what happened here.
- Never mark verified without checking against an official source; link that source.
- Unverified values are flagged, never inferred or filled in.

## Conflict resolution log
- 2026-11-16: arena-1 rebased onto current origin/main through successive parallel merges (PR #1, #2, #5, #6). Overlapping page files resolved by retaining each session's contributions where non-conflicting; COORDINATION.md merged to preserve all session boards. PR #4 (arena-1) content integrated into main this session.

## Tasks (arena-1 scope)
| # | Task | Status | File scope | Sources / verification | Irregularities |
|---|---|---|---|---|---|
| 1 | Create COORDINATION.md task board | done | COORDINATION.md | n/a | none |
| 2 | Research upcoming single-entry poker tournaments near Las Vegas Strip (official sources) | done | data/tournaments.md, site/tournaments.html | Wynn Las Vegas official site + official WPT schedule/structures PDFs. WPT World Championship Nov 27–Dec 21 2026; ALL events allow re-entry. Wynn daily tournaments all allow re-entry and/or add-on. No single-entry tournament confirmed from official Strip source. | Single-entry main list empty from official sources; gap flagged |
| 3 | Research hotels within walking distance (30 min) of tournaments (official sources) | done | data/hotels.md, site/hotels.html | Wynn resort fee $55+tax, free self-parking; Venetian/Palazzo $55+tax + $20 self-parking; Clark County lodging tax 13.38%; room rates dynamic. | Room rates dynamic; several hotel fees unverified |
| 4 | Build executive summary | done | site/executive-summary.html | n/a | none |
| 5 | Build suggestions section | done | site/suggestions.html | n/a | none |
| 6 | Build questions / information / answers section | done | site/questions.html | n/a | none |
| 7 | Create GitHub Pages site: landing page + category subpages, dashboard tables | done | *.html, assets/style.css | All 8 pages HTTP 200 locally; all internal links valid | Overlaps PR #2/#5 files — resolved at rebase |
| 8 | Flagged for Review page (unverified items) | done | site/flagged-review.html | n/a | none |
| 9 | Verify all table rows against official sources; no broken links | done | All site files | Official Wynn sources used; unverified values flagged, never inferred | Unverified items on Flagged for Review page |
| 10 | Enable GitHub Pages, confirm deploy, create PR, merge to main | in progress | n/a (GitHub) | PR #4 created; Pages configured (source=main) | Confirm Pages deploy after merge |

## Sources and verification
- Wynn poker page: https://www.wynnlasvegas.com/casino/poker
- WPT World Championship Schedule PDF: https://cdn.wynnresorts.com/image/upload/v1757097329/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Schedule.pdf
- WPT World Championship Structures PDF: https://cdn.wynnresorts.com/image/upload/v1750864036/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Structures.pdf
- Wynn Daily Tournament poster + Daily Structures PDFs (cdn.wynnresorts.com)
- Hotel fee/parking policy sources; Clark County lodging tax 13.38%
- PR #5 (e73e692a) sources (retained): Venetian DeepStack IV schedule (4 chunks), Venetian poker room/suite rates/resort fee, ARIA poker page; flagged items: Bellagio Saturday price conflict, Wynn hotel offer conflict/dead official page, Caesars and Bellagio fees unverified, RWLV/MGM Grand/Aria poker pages unavailable, 16 Venetian structure sheets not read
- Full list: data/sources.md

## Irregularities / open facts
- No single-entry tournament confirmed from an official Las Vegas Strip source for the upcoming period (single-entry list empty; gap flagged).
- No verified 8 a.m. tournament start.
- Hotel room rates dynamic (not fixed); several hotel fees unverified.
- Venetian's general poker page labels WPT Fall Festival "Current Series" while its dedicated page lists DeepStack IV beginning Nov 16; mismatch published on Flagged for Review.
- All unverified values flagged, never inferred.

## Pull request / deployment
- PR #1 merged: https://github.com/karagemop466-tech/Poker1/pull/1
- PR #2 merged: https://github.com/karagemop466-tech/Poker1/pull/2
- PR #5 merged: https://github.com/karagemop466-tech/Poker1/pull/5
- PR #6 merged: https://github.com/karagemop466-tech/Poker1/pull/6
- PR #4 (arena-1): https://github.com/karagemop466-tech/Poker1/pull/4 — being merged into main this session.
- GitHub Pages: https://karagemop466-tech.github.io/Poker1/ — Pages API reported `built`, but latest workflow run 43932754208 failed validation (table rows lacked official links); deploy job skipped. Fixed tournament/hotel row sourcing, suggestion references, and workflow staging; local validator now passes. Deployment confirmation still pending.

## Log
- 2026-11-16: arena-1 initialized board; repo contained only README.md.
- 2026-11-16: arena-1 completed tournament + hotel research from official Wynn sources.
- 2026-11-16: arena-1 built the GitHub Pages site (8 pages + CSS).
- 2026-11-16: PR #1, #2, #5, #6 merged into main while this session worked; arena-1 rebased onto current origin/main.
