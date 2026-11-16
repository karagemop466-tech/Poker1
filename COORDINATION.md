# COORDINATION.md

Shared task board for the Las Vegas Strip poker tournament and hotel planner.

## Current session and task claim

Session `f0143c13` is working on branch `arena/f0143c13-poker1` (the branch is fixed for this session). Claim commit `cc17d9e` was pushed before implementation work.

| Task | Status | File scope | Owner |
|---|---|---|---|
| Repair GitHub Pages deployment of the Markdown-backed dashboard pages; add checks for deployed content and official source domains; correct incorrect summary metadata; record the review/deploy result | In progress pending PR and deploy verification | `.github/workflows/pages.yml`, `scripts/check_links.py`, `README.md`, `EXECUTIVE_SUMMARY.md`, `COORDINATION.md` | `f0143c13` |

No other active file claims are recorded. All tournament/hotel data and site generation code are outside this session's scope.

## Existing deliverables and current data status

The repository already contains a static dashboard (`index.html`, `pages/`, `assets/`), source-linked JSON data, research notes, and separate Executive Summary, Questions, Suggestions, and Flagged for Review documents. The data build reports 225 rows: 33 marked verified single entry, 15 marked possible multi-entry, 6 marked re-entry, and 171 with entry rules unverified. Only the 33 Venetian DeepStack IV rows are presently in the verified single-entry list. The full dataset and research notes have not been independently reread row by row in this current audit; the verification boundary and open items below are explicit.

## Verification performed in this session

- `python3 scripts/build_data.py` — generated the committed data files; counts matched the above.
- `python3 scripts/build_site.py` — generated the landing page and 10 dashboard subpages.
- `python3 scripts/check_links.py` — passed JSON parsing, local links, required Markdown-file presence, and official-source-host validation.
- Pages staging smoke test — confirmed the static build contains `index.html`, all required subpages, the three JSON datasets, and all five Markdown documents fetched by the summary/questions/suggestions/flags/review pages.
- `git diff --check` — passed.
- Official Venetian source pages fetched and read:
  - [DeepStack Extravaganza IV schedule](https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html): series dates Nov 16–Dec 23, 2026; displayed schedule rows and structure-sheet links.
  - [DeepStack Extravaganza NYE schedule](https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-dec-2026.html): series dates Dec 24, 2026–Jan 10, 2027; source page itself prints some rows with a 2025 year, recorded in `FLAGGED.md`.
  - [Venetian poker suite rates](https://www.venetianlasvegas.com/resort/casino/poker/suite-rates.html): starting-rate language is conditional, rates are not assigned to a particular tower, availability and poker-play qualification apply, and $55/night resort fee is stated.
  - [Venetian resort fee](https://www.venetianlasvegas.com/resort/resort-fee.html): $55 plus tax per night.
  - [Venetian hotel terms](https://www.venetianlasvegas.com/legal/hotel-terms-and-conditions.html): 13.38% Clark County room tax and $55 plus applicable tax resort fee are stated; the terms also state rates are availability/date-dependent.
- GitHub Pages is configured for `main` at `/`. The existing Pages run `43934417739` succeeded before this session's fix. Its success did not prove the Markdown-backed pages worked because the staging step omitted the Markdown files; the current fix must merge and deploy before the issue is considered closed.

## Open facts and irregularities — publish on Flagged for Review

- The initial deployed artifact staged only `index.html`, `pages/`, `assets/`, and `data/`, while dashboard pages fetch the root Markdown documents. Those Markdown pages would fail to load after deployment. The workflow now stages the five required documents, and a smoke check covers them. Actual post-merge Pages deployment remains pending.
- The audit checks that all dataset sources use known official operator hosts; it does not establish that every individual schedule/structure value has been freshly reread. Do not describe all 225 rows as independently reverified by this session.
- Research note `research/tournaments.md` says some Venetian multi-flight structure-sheet-to-event mappings were selected by reasoning and not rechecked sheet by sheet. Keep those 15 rows segregated from the single-entry ranking pending confirmation.
- 171 tournament rows still have unverified entry rules. No unsupported value should be filled in.
- No date-specific hotel nightly quote is verified. The Venetian poker offer is conditional and has not been used as a generic rate; a true total for a particular stay cannot yet be computed.
- Official-source walking times have not been verified. Therefore the 30-minute walking requirement and quality/cost hotel ranking cannot be confirmed from current data.
- No verified single-entry event starts at 8 AM. Verified single-entry entries start no earlier than 10:10 AM; the schedule page reports 11:10 AM for the first event date (Nov 18). Long enough tournament duration/late registration/overlap data are not established to guarantee all-day multi-entry scheduling.
- The official Venetian NYE schedule has year/date typos and other printed inconsistencies documented in `FLAGGED.md`.
- `EXECUTIVE_SUMMARY.md` previously contained an unsupported “Houston, TX” label; removed. No user location is asserted in the summary.

## PR and deployment record

Previous project changes are already integrated on `main` (including PRs #1, #2, #5, #6, #8, #9, and #10). PR #7 is an unrelated open historical PR. Current-session PR link, merge result, and resulting GitHub Pages deployment run will be recorded here after they are confirmed.
