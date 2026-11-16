# Coordination — Poker1

Shared task board across Arena sessions.

## Session `session-552e97d2` (branch `arena/552e97d2-poker1`, current session)

| Task | Status | Owner | Files touched | Notes |
|------|--------|-------|---------------|-------|
| Create COORDINATION.md task board | done | session-552e97d2 | COORDINATION.md | Initial board |
| Research live upcoming poker tournaments near Las Vegas Strip (official sources) | done | session-552e97d2 | data/tournaments.md | Venetian DSE IV (official PDF), Wynn WPT World Championship (official PDF), MGM Grand (official page + schedule PDF). Re-entry policies verified where structure sheets state them. |
| Research hotels within 30-min walking distance of tournaments | done | session-552e97d2 | data/hotels.md | Venetian $55 resort fee + 13.38% tax (official); Wynn $45 (official terms); Mirage CLOSED (flagged). Room rates blank+unverified. |
| Build single-entry tournament schedule (~8 AM all day) | done | session-552e97d2 | data/schedule.md | Sample all-day single-entry days; no 8 AM start exists (flagged) |
| GitHub Pages site (landing page + category subpages, tables, sources) | done | session-552e97d2 | *.html at repo root, style.css | All internal links verified; pages: index, tournaments, hotels, schedule, executive-summary, questions, suggestions, flagged |
| Executive summary | done | session-552e97d2 | executive-summary.html | |
| Suggestions section | done | session-552e97d2 | suggestions.html | |
| Questions / information / answers | done | session-552e97d2 | questions.html | |
| Flagged-for-review page | done | session-552e97d2 | flagged.html | |
| PR to main, merge, confirm Pages deploy | in progress | session-552e97d2 | — | PR #3 opened; merged after reconciling with origin/main; then confirm Pages deploy on main |

## Session `arena/67733ec6-poker1` (prior session, merged into main via PR #1)

| Task | Status | Owner | Files | Notes |
|------|--------|-------|-------|-------|
| Build research dashboard, evidence standards, flagged review | in progress | arena/67733ec6-poker1 | index.html, styles.css, app.js | Evidence-first dashboard shell; deliberately asserted 0 confirmed events (did not verify event-level entries against official sources) |
| Site source verification and integration | in progress | arena/67733ec6-poker1 | all site files, README.md, COORDINATION.md | Left blank until date-specific official confirmation |

## Merge resolution (PR #3 → main)

- index.html conflict resolved in favor of session-552e97d2's fully verified landing page; prior session's index.html shell not retained (their app.js, styles.css, and .github/workflows/pages.yml are preserved).
- Both sessions' COORDINATION.md content consolidated above.
- Files preserved from both sessions: index.html, tournaments.html, hotels.html, schedule.html, executive-summary.html, questions.html, suggestions.html, flagged.html, style.css, styles.css (prior session), app.js (prior session), .github/workflows/pages.yml (prior session), data/*.md (session-552e97d2).

## Rules
- Verify every value against an official source; link the source on every table row.
- If a value cannot be confirmed from an official source, leave it blank and flag as "unverified".
- Never infer or fill in values. No hallucinations.
- Claim a task before starting; commit + push the claim immediately.
- Never edit files claimed by another session; log requests in COORDINATION.md instead.
- Small, frequent commits; `git pull --rebase` before every push.
