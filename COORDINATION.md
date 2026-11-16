# Coordination — Poker1 (branch arena/552e97d2-poker1)

Shared task board. Session ID: `session-552e97d2` (single session; branch `arena/552e97d2-poker1`).

## Tasks

| Task | Status | Owner | Files touched | Notes |
|------|--------|-------|---------------|-------|
| Create COORDINATION.md task board | done | session-552e97d2 | COORDINATION.md | |
| Research live upcoming poker tournaments near Las Vegas Strip (official sources) | done | session-552e97d2 | data/tournaments.md | Venetian DSE IV (official PDF), Wynn WPT World Championship (official PDF), MGM Grand (official page + schedule PDF). Re-entry policies verified where structure sheets state them. |
| Research hotels within 30-min walking distance of tournaments | done | session-552e97d2 | data/hotels.md | Venetian $55 resort fee + 13.38% tax (official); Wynn $45 (official terms); Mirage CLOSED (flagged). Room rates blank+unverified (no live booking data). |
| Build single-entry tournament schedule (~8 AM all day) | done | session-552e97d2 | data/schedule.md | Sample all-day single-entry days built from Venetian 1Day events; no 8 AM start exists (flagged). |
| GitHub Pages site (landing page + category subpages, tables, sources) | done | session-552e97d2 | *.html at repo root, style.css | All internal links verified; pages: index, tournaments, hotels, schedule, executive-summary, questions, suggestions, flagged. Repo root layout required because Pages is configured on main at path "/". |
| Executive summary | done | session-552e97d2 | site/executive-summary.html | |
| Suggestions section (site improvements + missing info) | done | session-552e97d2 | site/suggestions.html | |
| Questions / information / answers (pre-decision checklist) | done | session-552e97d2 | site/questions.html | |
| Flagged-for-review page (unverified items + irregularities) | done | session-552e97d2 | site/flagged.html | |
| PR to main, merge, confirm Pages deploy | in progress | session-552e97d2 | — | Verify build/deploy from current branch first, then PR to main, merge, reconfigure Pages on main, confirm live. |

## Rules
- Verify every value against an official source; link the source on every table row.
- If a value cannot be confirmed from an official source, leave it blank and flag as "unverified".
- Never infer or fill in values. No hallucinations.
- Claim a task before starting; commit + push the claim immediately.
- Never edit files claimed by another session; log requests in COORDINATION.md instead.
- Small, frequent commits; `git pull --rebase` before every push.
