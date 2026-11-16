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

- The ranking is reserved for events whose official terms confirm one paid entry total. A structure sheet that merely omits re-entry, rebuy, add-on, or flight language does not prove single-entry.
- Events with re-entry, rebuy, add-ons, multiple flights, or unresolved entry terms stay outside the strict ranking and are shown separately or flagged. A source clause that bars players who bag Day 2 from later flights does not resolve whether players who bust may re-enter.
- Hotel true cost includes resort fees and tax when both are confirmed for the property. A total stays blank until the dated room rate, fee, and property-specific tax are verified. Walking time stays blank unless supported; a listed hotel must be within 30 minutes on foot. Nothing is inferred.
- Every table row links to an official source.

## Rebuild and check

```
python3 scripts/build_data.py     # regenerate data/*.json
python3 scripts/build_site.py     # regenerate index.html and pages/*.html
python3 scripts/check_links.py    # data schema, official hosts, SE schedule, hotel totals, local links
```

The Pages workflow (`.github/workflows/pages.yml`) rebuilds and checks generated pages on each pull request, then deploys `index.html`, `pages/`, `assets/`, `data/`, and the Markdown content files used by the Executive Summary, Questions, Suggestions, Flagged for Review, and Repo Review pages after a push to `main`. `scripts/check_links.py` verifies that Markdown files are present, each data row has an HTTPS source on an approved official host, IDs and derived fields are consistent, the day schedule contains exactly the verified single-entry rows, hotel totals use confirmed rate/fee/tax inputs, and static page links resolve. Automated checks do not substitute for reading and verifying the official source documents.

Coordination and open items: `COORDINATION.md`.
