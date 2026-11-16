# Las Vegas Strip Poker Plan

A source-verified plan for single-entry poker tournaments on the Las Vegas Strip and walkable hotels. Snapshot date: **2026-11-16**.

Live site: https://karagemop466-tech.github.io/Poker1/

## What is in the site

- `index.html`: landing page with counts and links.
- `pages/`: single entry, separate section (possible multi-entry and re-entry), unverified rows, hotels, schedule, executive summary, questions, suggestions, flagged for review, repo review and sources.
- `data/*.json`: tournament, hotel and schedule data. Generated from `scripts/build_data.py`. Do not edit the JSON by hand.
- `assets/`: shared stylesheet and client-side renderer. The site has no external CDN dependencies.
- `research/`: research notes for each task.
- `archive/prior-main/`: the earlier site and documents from other sessions, kept for reference. Not published.

## Rules used

- Only events whose official structure sheet has been read and shows no re-entry, rebuy, add-on or flight clause are listed as single entry.
- Possible multi-entry events are shown separately. The structure sheet clause only says a player who bags Day 2 chips may not play a subsequent flight.
- Hotel true cost includes resort fees. A value is blank until it is verified from an official source. Nothing is inferred.
- Every table row links to an official source.

## Rebuild and check

```
python3 scripts/build_data.py     # regenerate data/*.json
python3 scripts/build_site.py     # regenerate index.html and pages/*.html
python3 scripts/check_links.py    # JSON, local links, source links
```

The Pages workflow (`.github/workflows/pages.yml`) runs the checks on each pull request and deploys `index.html`, `pages/`, `assets/`, `data/`, and the Markdown content files used by the Executive Summary, Questions, Suggestions, Flagged for Review, and Repo Review pages after a push to `main`. `scripts/check_links.py` verifies those Markdown files are present and that every data source uses an approved official operator domain.

Coordination and open items: `COORDINATION.md`.
