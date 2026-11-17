# Live re-verification — 2026-11-17 (session c4774e5a)

Branch `arena/c4774e5a-poker1`, base `44fcc08`. Every value below was read from the official page
or PDF on 2026-11-17 with a live page fetch. This sandbox cannot open an HTTPS connection to the
operator domains from `bash` (`SSL_ERROR_SYSCALL`), so the fetches were made with the agent's page
tool, which does have outbound access. Nothing here is carried forward from an earlier session
without the live check being repeated.

## What was re-read, and what it confirmed

| # | Official document | What the live document says | Effect on the dataset |
|---|---|---|---|
| 1 | [DeepStack Extravaganza IV event page](https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html) (4 of 4 chunks) | Heading "November 16 – December 23, 2026"; "More than $3.6 Million in guaranteed tournament prize pools"; the dated rows and structure-sheet links match the dataset row for row in every chunk read, including the 9:10 AM Dec 12 turbo satellite, the 10:10 AM Dec 12 $2,200 Title Event 1A, the 12:10 PM Dec 12 turbo satellite and the 6:10 PM Dec 12 1B. | No change. 94 rows stand. |
| 2 | [DeepStack Extravaganza NYE event page](https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-dec-2026.html) (2 of 2 chunks) | Heading "December 24, 2026 – January 10, 2027"; "More than $1.1 Million". The page still prints the Dec 26 rows as "Saturday, December 26, **2025**" (F1) and Jan 5 as "Tuesaday" (cosmetic, no data effect). | No change. 49 rows stand. |
| 3 | [Structure sheet #16](https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_16.pdf) — Event 36, $800 NLH Bounty, Dec 9 | Event 36, 11:10 AM, 40,000 starting chips, 30-minute levels, late registration "10 levels + Break (4:55 PM)", guarantee "$75,000 (prize pool + total bounties)", clause 6: "$100 of the $800 Buy-In is withheld for house fees", clause 7: "$200 Bounty … $500 Bounty in the money", clause 8: "pays 12.5% of the field". | Confirms the **top-ranked row** (r096) on every published field: buy-in $800, guarantee $75,000, house fee $100 (12.5%), 40,000 chips, 30-minute levels, late registration 16:55, 28 levels. |
| 4 | [Venetian hotel terms and conditions](https://www.venetianlasvegas.com/legal/hotel-terms-and-conditions.html) (2 of 2 chunks) | "Daily rates do not include the applicable Clark County Room Tax of **13.38%**." "The Venetian Resort has a standard Las Vegas Resort Fee of **$55 plus applicable tax per night**." Parking: "The daily fee for registered hotel guests is **$20/day**, seven days a week. For non-hotel guests, the fee is $20, Monday – Thursday, and $25/day Friday – Sunday. Valet parking is $40/day." Cancellation: a deposit is billed on confirmation and "for prepaid offers … bookings are non-cancellable and non-refundable"; no fixed free-cancellation deadline is printed for a general rate. Check-in 3:00–11:59 p.m., check-out 11:00 a.m.; early check-out costs $100 plus tax. | Confirms the Venetian tax rate, resort fee and parking figure already stored. Confirms that the missing Venetian cancellation deadline is genuinely absent from the official page, not merely unread (I9b stays open). |
| 5 | Ten routed walking pairs, re-queried on the OpenStreetMap foot router | Bellagio → Venetian poker room `duration 1284.9 s / 1606.4 m` = **22 min**; Caesars Palace → Wynn poker room `1908.3 s / 2382.5 m` = **32 min**; Venetian → Wynn poker room `919.4 s / 1146.8 m` = **16 min**. | Every re-queried routed time reproduces the stored value and distance to the metre, so `data/walking.json` is confirmed as published. |

The walking routes are routed estimates from a public routing source, not a property's own published
walking time; no property publishes one (F49).

## Irreproducible-but-not-yet-checkable items

- **Wynn Signature Series structures PDF.** Still a "COMING SOON" placeholder at the URL the official
  poker page links (F44), so all 38 rows remain unverified on the entry rule. Re-checked live: unchanged.
- **Wynn hotel rate.** `reservations.wynnlasvegas.com` renders the nightly grid and tax line client-side
  (F46/F37), so no like-for-like Wynn quote with a tax figure can be captured from a text fetch.

## Defects found in the published pages and documents (corrected in this session)

| # | Defect | Handling |
|---|---|---|
| P1 | The monitoring page rendered the sandbox's own network blackout as "0 / 94 official sources reachable", which reads as a source outage. | `monitor_sources.py` now sets `network_unavailable` when every attempt fails at the TLS/DNS layer; the page states that in words and renders the GitHub Actions provenance result (`data/change_log.json`: 70/74 documents fetched, 0 printed values changed, 3 timeouts) as the real source status. |
| P2 | `pages.yml` marked `deploy` failed on every run: the repository's Pages site is configured `source: main:/` with the **legacy** branch build, so `actions/deploy-pages` never found a `github-pages` artifact. The site itself kept building. | The deploy job now reads the site's real build type. With `workflow` it publishes the artifact as before; with `legacy` it fails unless the branch build for the exact commit reaches `built`. |
| P3 | `EXECUTIVE_SUMMARY.md` still said "all 316 rows", "135 rows" for WPT and "105 rows" in the separate section, and `QUESTIONS.md` said "135 Wynn WPT rows", after the restored TORSE row and the reclassification took the dataset to 317 / 136 / 106. | Corrected to the counts the build actually produces: 317 rows, 136 WPT rows, 106 in the separate section (60 multi-flight + 46 re-entry), 129 unverified (91 WPT + 38 Signature Series). |
| P4 | `REVIEW.md`'s build note said "56 flagged". | Corrected to 78, the number `build_data.py` prints. |

## Verification run in this session

```
python3 scripts/build_data.py    # 317 rows (SE 80, MULTI 60, RE 46, UNV 129, CONT 2); 70 days; 78 flagged
python3 scripts/build_site.py    # 21 pages, zero diff against the committed pages
python3 scripts/check_links.py   # OK (21 pages, 317 rows, 7 hotels, 5 dated rates, 70 schedule days)
python3 scripts/verify_rows.py   # 324 rows, 1,122 field checks, 0 hard failures, 1 review item (r225, F4)
npm run test:smoke               # 21/21 pages render in a headless DOM
```

## Still open (unchanged, published on the Flagged for Review page)

The 38 Wynn Signature Series entry rules (I4/F44), the Wynn room-tax rate and any Wynn rate quote
(I6/I7/F46), the Bellagio/Caesars/ARIA resort fees and taxes (I7/F47), the Venetian free-cancellation
deadline for a general rate (I9b), the printed date and time conflicts F1, F3, F4, F5, and the
poker-room confirmations listed in `QUESTIONS.md` section C. None of these block publication and none
is guessed at anywhere in the dataset.
