# Verification 2026-11-17 — the source check, from measurement to merged code

Session `1ebc7e08`, branch `arena/1ebc7e08-poker1`, **PR #66**. Base: `main`, rebased twice while the work
was in progress; the numbers below were measured against `main` as of the second rebase (23 pages, 317
tournament rows, 91 manifest sources).

The requirement was *"an automatic re-check of each official URL on a schedule, marking the rows whose
source changed"*. While this work was in flight, `main` gained a monitor implementation for the same
requirement (session `8a12503e`, with `data/source_baseline.json`, `--content`, `kpi_basis` and a
`--write-report` gate that stops a validation run from publishing). That implementation is kept — this
branch no longer replaces it. What remains here is what `main` still could not do, each item measured first.

## 1. Official pages re-read on 2026-11-17

| Source | Read | Result |
|---|---|---|
| [Wynn Signature Series structures PDF](https://cdn.wynnresorts.com/image/upload/v1753296112/visitwynn_pdfs_files/Poker/Wynn%20Signature%20Series/Wynn_Signature_Series_Structures.pdf) | whole document | still a placeholder: the served page is titled "Poker Tournament - Details Coming Soon" and prints only "LAS VEGAS POKER COMING SOON", so the 38 Signature Series rows keep their unverified entry rule |
| [WPT World Championship structures PDF](https://cdn.wynnresorts.com/image/upload/v1750864036/visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Structures.pdf) | live text against `data/snapshots/wpt_struct.txt` | same title, same range "November 27 – December 21, 2026", same clause 3 ("Registration for each Event will open four (4) hours prior to the scheduled start of play"); hash equals the capture baseline, so no WPT row needs re-reading |
| The 52 Venetian structure sheets | each sheet's recorded hash | no printed amount, date, time or rule word differs from the archived text, which is what the single-entry verdicts rest on |
| Bellagio, ARIA pages | attempted by the scheduled job | `TimeoutError` from GitHub Actions as well as from this sandbox; recorded as not checked, never as unchanged |
| 7 sources listed in F100 | byte hash vs the capture hash of 2026-11-16T19:21:15Z | **the bytes moved, the printed values did not** (`facts_changed` empty) - rotating offer text, not a schedule edit |

Network fact, stated for the record: this sandbox reaches `github.com` through `git`/`gh` only; a direct
HTTPS request to an operator domain fails with `TLS/SSL connection has been closed (EOF)` in ~31 ms. Live
page reading was done with the agent's page fetcher; hash evidence comes from the collector job's own run,
stored in `data/change_log.json` (`generated_utc 2026-11-17T01:36:07Z`).

## 2. The four fixes, and how each was measured

1. **`changed_vs_baseline` was dead** (`scripts/check_source_facts.py`, F100). The baseline file is
   `{"note", "captured_utc", "hashes": {id: sha256}}`; the code looked each id up on the wrapper. Measured
   before/after on the committed data: **0 → 7** sources flagged, `facts_changed_ids` still empty, so the
   correct conclusion is "page churn, values intact" and no dataset value was edited.
2. **The provenance job refused to run** (F101). `assert_official()` exits with
   `non-official host(s) in manifest: [('strip_rwlv_events', 'www.rwlasvegas.com')]`: the Strip-survey
   session registered that domain in `check_links.py`'s `OFFICIAL_SOURCE_HOSTS` but not in the collector's
   `OFFICIAL_HOSTS`, so every scheduled snapshot run failed. Reproduced on pristine `main` before the fix,
   and `python3 scripts/check_source_facts.py --offline` now completes. The duplicate allow-list is the root
   cause; this registers the missing property host and says so in a comment rather than silently diverging.
   The MGM `assets.contentstack.io` CDN stays un-approved in both lists, matching F40.
3. **31 published rows were outside the monitor** (F102). `collect_dataset()` did not read
   `data/other_rooms.json`. After the change it collects 60 citations from those events and room findings,
   and monitored URLs go **89 → 117**; `--print` reports the same verdicts for them (`0` rows marked).
4. **Four official URLs cited by hotel rows were in no manifest** (F103). Added (91 → 95), so the collector
   will hash the ARIA and Bellagio booking pages, the Caesars room calendar and the Wynn rooms page too.

## 3. What was measured and then dropped, so it does not look like an unexplained loss

An earlier revision of this branch replaced `scripts/monitor_sources.py` with a different design: printed-fact
comparison against `data/capture_facts.json`, a run-to-run baseline in `data/monitor_baseline.json`, a
per-row verdict file `data/source_changes.json`, row stamping into the data files, and a self-test. `main`'s
version already covers items 1-3 of that design (facts signature comparison, its own baseline file, the
provenance fallback with `kpi_basis`, and `--write-report` so a validation run cannot publish), so
replacing it was no longer the right change and was dropped. Two parts are genuinely missing there and are
filed instead of forced: **row-level marking** and **a self-test** — see F104 and S27. The worked version,
including its test evidence, stays on this branch's history:

- `--self-test` ran 18 checks with no network and no data file written: every verdict state, an empty
  reference still catching a value appearing, a flag not changing the dataset fingerprint, idempotent and
  reversible stamping, the URL named once, the row's own flag surviving.
- End-to-end fixture (a copy of the repository in `/tmp`, no published file touched): one printed line of
  the reference for the Venetian November schedule changed `$300` → `$375`; the monitor with `--stamp`
  marked **94 rows** with a dated flag and refreshed `last_checked`, listed all 94 in `data/changes.json`,
  and a clean re-check cleared every flag while keeping the rows' own flags and leaving the dataset diff 0.
- Two consecutive runs were byte-identical (idempotent), and an offline run never rewrote a bytes hash with
  a text hash — the defect that had made every offline re-check look changed.

## 4. Validation of this branch

- `python3 scripts/build_data.py` → 317 rows (SE 80 / MULTI 60 / RE 46 / UNV 129 / CONT 2), 70 schedule
  days, 79 flagged rows; **zero diff** in `data/`, so no published value moved.
- `python3 scripts/build_site.py` → 23 pages; zero diff against the committed pages.
- `python3 scripts/check_links.py` → OK. `python3 scripts/verify_rows.py` → 324 rows, 1122 field checks,
  0 hard failures, 1 review item (the 20:00 start on `r225`, already recorded as a source conflict).
- `python3 scripts/monitor_sources.py --print` → 117 URLs, `0` rows marked, and it writes nothing: the
  report says *"reports not written (run with --write-report to publish)"*.
- `python3 scripts/check_source_facts.py --offline` → completes, `change_log.json left unchanged`.
- `npm run test:smoke` and `node scripts/smoke_pages.js` → 23/23 pages render, no script errors.

## 5. Still open after this branch

- The two official-host allow-lists should become one constant; until then a new property domain has to be
  registered twice, which is how F101 happened.
- Row-level marking and the self-test (F104, S27).
- **35 of the 117 cited URLs are not in `data/sources.json`**, so nothing archives them (measured by
  comparing `collect_dataset()` with the manifest). 21 are the OpenStreetMap geocoding and routing queries the
  walking rows record as method rather than as a source, and 14 are the surveyed rooms' own pages: three
  `caesars.com` subpages, two MGM `assets.contentstack.io` PDFs, and one page each on
  `excalibur.mgmresorts.com`, `luxor.mgmresorts.com`, `southpointcasino.com`, `thestrat.com`,
  `www.rwlasvegas.com`, `www.mgmresorts.com`, `www.hardrockvegas.com`, `www.fontainebleaulasvegas.com` and
  `www.saharalasvegas.com`. Twelve of those fourteen hosts are not in either allow-list, so the collector
  would refuse to run with them: whether they count as official is the row owner's call, not a monitoring
  fix. `southpointcasino.com` is approved but was never registered, and `www.rwlasvegas.com` is the case
  where the row owner had already decided and only the collector had not been told (F101).
- `sources_ok` and friends are still only as good as the machine that ran the job: this branch could not
  probe an operator domain, so the live counts stay whatever the last scheduled run measured.
