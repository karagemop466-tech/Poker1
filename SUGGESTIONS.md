# Suggestions for Site Improvement

These are options for you to choose from. **None has been implemented.** Pick the ones you want, and the next session will build only those.

## 1. Decision support

| # | Suggestion | Benefit | Cost / risk |
|---|---|---|---|
| S1 | Add a filter for "Only events I can enter in my budget" (buy-in cap). | Faster shortlist. | Needs your budget (D3). |
| S2 | Add a day planner that lets you drag events onto a day and warns on time overlaps. | Shows which events conflict. | Overlap rules depend on real run times, which are not published. |
| S3 | Add an "estimated cost of a trip" calculator: entries × buy-ins + nights × true hotel cost. | One total number. | Blank until rates are verified. |
| S4 | Show a traffic-light status on each row: verified, partially verified, unverified. | Makes gaps obvious at a glance. | None. |

## 2. Data quality

| # | Suggestion | Benefit | Cost / risk |
|---|---|---|---|
| S5 | Add an automatic re-check of each official URL on a schedule and mark rows whose source changed. | Catches schedule changes. | Needs a scheduled job. Limited by source access. |
| S6 | Read every structure sheet and remove the "unverified" label from each event that is confirmed. | Largest gain in confidence. | All remaining structure sheets (Venetian, Venetian NYE, Wynn). |
| S7 | Add a "last checked" date to each row. | Easy to see stale data. | None. |
| S8 | Keep rates as a dated log, not a single value. | Shows price patterns on your dates. | Needs repeat checks. |

## 3. Site structure

| # | Suggestion | Benefit | Cost / risk |
|---|---|---|---|
| S9 | One page per venue (Venetian, Wynn, others), each with its events and hotels. | Easier to plan by location. | Duplicates some data. |
| S10 | Keep the current category pages (single entry, separate section, hotels, schedule). | Matches your request. | None. |
| S11 | Add print-friendly views. | Useful on the trip. | Small effort. |
| S12 | Add a search box across all tables. | Faster lookup. | Small effort. |

## 4. Process

| # | Suggestion | Benefit | Cost / risk |
|---|---|---|---|
| S13 | Use one shared `COORDINATION.md` on `main` before parallel sessions start. | Avoids the split-branch claims found in this repo. | Needs agreement. |
| S14 | Put the build script in CI so the site cannot publish with a broken link or missing source. | Protects quality. | Setup effort. |
| S15 | Require a source URL on every new row (already enforced by `scripts/build_data.py`). | Keeps the "no hallucination" rule. | None. |

## Your choice

Reply with the numbers you want (for example "S1, S4, S6, S10"). Nothing changes until you choose.
