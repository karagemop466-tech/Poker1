# Improvement suggestions for review

Each item names what it would change, why it is worth doing, and how much work it is. Nothing here has been
applied without a decision. Items already built into this version are marked **done**, so the list doubles as a
record of what changed.

## Built in this version

**1. Section the tournaments by the entry rule alone.** **Done.**
An earlier version mixed two criteria: it moved bounty, satellite and team formats out of the single-entry
section, which meant a single-entry satellite was excluded from a section whose name describes exactly what it
is. The section now turns on one question only: does the structure sheet allow more than one entry? Prize
structure became a filter instead of a section.

**2. Stop adding the house fee to the buy-in.** **Done.**
The earlier version computed a "total fee" as buy-in plus house fee, which double-counted. Every official sheet
read here withholds the fee from the buy-in. Two Bellagio prize pools were also derived as buy-in minus fee when
the official sheet prints the pool explicitly, which produced $550 instead of $510 and $365 instead of $340.
Both are now the printed figures.

**3. Give every schedule day a conditional fallback.** **Done.**
44 of 52 dates now carry a fallback rather than only 16. A fallback is only offered when its start falls outside
the primary's registration window, using the printed late-registration cutoff as the overlap test. Where no
non-overlapping alternative exists, the page says so rather than silently showing a single option.

**4. Compute the walking times instead of leaving them blank.** **Done.**
All 42 hotel-to-venue pairs are computed from the official street addresses with one OpenStreetMap pedestrian
routing request, and each pair carries Google Maps and Apple Maps walking links. The figures are labelled
computed, not quoted, because no resort publishes a walking time.

**5. Add a hotel rate log with like-for-like rules.** **Done.**
An append-only log, one row per observation of one stay, with a flag on every field. The comparison rule is
stated on the page: same dates, same occupancy, same room type, same fee and tax treatment.

**6. Add a trip cost calculator.** **Done.**
Entries times buy-ins plus nights times the true nightly cost. The hotel component stays visibly blank until a
dated rate exists, instead of being estimated from a rate the site cannot confirm.

**7. Add a live daily feed.** **Done.**
The official daily posters and structure sheets are parsed by a scheduled job. The eight rows read directly
from those documents are pinned in the seed feed so a failed extraction never drops a verified row.

**8. Add a source watchdog.** **Done.**
Every official URL is fetched, hashed and compared with a stored baseline. A document that moves is flagged on
the Official sources page. A fetch failure is reported as a failure, never as "unchanged".

**9. Add an irregularity log.** **Done.**
Contradictions and typos found in official documents are recorded with the document, the specific problem, and
how it was handled.

**10. Split the Markdown review material into its own pages.** **Done.**
The executive summary, questions, suggestions, flagged items, irregularities, sources and repo review each have
their own page instead of one long document.

## Suggested next, in order of value

**11. Capture one dated rate per property.** *Medium work, highest value.*
The single biggest gap. Seven dated quotes for the same six nights and two adults would turn every blank stay
total on the site into a real number, and would make cross-property comparison possible for the first time. The
log is already built to receive them.

**12. Read the rendered WPT and Signature Series PDFs page by page.** *Medium work, high value.*
93 rows, the majority of the Wynn inventory, sit unranked because the text extraction stops partway through the
WPT document and the Signature structures are a placeholder. A rendered read would either confirm those rows or
confirm that they genuinely cannot be confirmed yet.

**13. Add the Venetian and Palazzo room-type pages.** *Small work, moderate value.*
Maximum occupancy and the difference between the from-$119 and from-$209 tiers would both come from the same
set of pages.

**14. Add a printable one-page trip card.** *Small work, moderate value.*
The chosen dates, the primary and fallback per day, the buy-ins, the hotel, and the walk times, on one page that
prints cleanly to A4. Useful in a pocket, which a 17-page site is not.

**15. Add a calendar export.** *Small work, moderate value.*
An `.ics` file for the primary events on the chosen dates, so the plan lands in a phone calendar with the venue
address attached.

**16. Add a per-venue guarantee distribution.** *Medium work, low value.*
A small histogram per venue showing how guarantees are spread, so "the Venetian's typical guarantee is $10K but
its ceiling is $75K" is visible at a glance rather than inferred from a table.

**17. Add structured data for search engines.** *Small work, low value.*
Schema.org event markup for the tournament rows so a search result can surface a date and a venue. Worth doing
only if the site is meant to be found by people other than you.

**18. Add a change history per tournament row.** *Medium work, low value.*
Store each generated data file's previous version and diff it, so a guarantee that moves from $50K to $75K is
visible as a change rather than silently replacing the old value. The source watchdog already detects that a
document changed; this would show what changed inside it.
