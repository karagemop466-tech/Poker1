# Irregularity log

Typos, contradictions and gaps found in the official documents that this planner is built from.
Each one is recorded here rather than silently corrected, because a correction that is not
published should be visible to the reader.

Every row names the official document it came from and what was done about it.

## Official tournament documents

| # | Document | What is wrong | How it was handled |
|---|---|---|---|
| 1 | Venetian DSE IV December schedule (`dse-dec-2026.html`) | Events 5, 6 and 7 are printed with a 2025 date instead of 2026. | The dates were taken from the official structure sheets, which print 2026, and the 2025 typo was ignored. The schedule row is dated Dec 26, 2026. |
| 2 | Venetian NYE structure sheet 12 (event 29) | The sheet says a discounted subsequent re-entry costs `$20` off for a `$180` total. The event page says the discount is `$10`. | Neither figure was published as the re-entry price. The row records that a discounted subsequent re-entry is permitted and lists the discrepancy. |
| 3 | Wynn WPT World Championship schedule PDF | The extracted date and column order is shifted on several rows, so a printed date does not always line up with the printed event name. | Dates were taken from the event names and the structure PDF rather than from the shifted schedule columns. The affected rows are flagged as date-uncertain in the data. |
| 4 | Wynn Signature Series schedule PDF | The extracted columns are shifted on several rows. | The Series dates were taken from the official Wynn poker hub page, which confirms Jan 11-24, 2027. The shifted fields were not ingested. |
| 5 | Wynn Signature Series structures PDF | The document is a placeholder: it contains only the words "LAS VEGAS POKER - COMING SOON" and no structure at all. | No Signature row is presented as a confirmed single-entry event. All 31 Signature rows are marked unverified, and the placeholder is linked from every one of them. |
| 6 | Bellagio Saturday No Limit Hold'em PDF | The title, the header and the rule text disagree about the buy-in. It also refers to a Day 2 in September 2026, which cannot be a forward-looking reference from a current poster. | The disputed fields are not confirmed. The row is marked unverified and the contradiction is reproduced in the row's note. |
| 7 | Venetian DSE IV schedule | Events 12, 18, 19, 26, 47, 49, 56, 58 and 59 are printed with a fee or entry rule that does not match the generic "one entry" wording used elsewhere. | Each of these was read on its own structure sheet and placed in the separate-formats section with the reason stated, rather than being counted as single entry. |

## Official hotel documents

| # | Document | What is wrong | How it was handled |
|---|---|---|---|
| 8 | Clark County transient lodging licence list | The list is dated July 2021 and records the Venetian and Palazzo at 3325 Las Vegas Blvd S. The current Venetian branding uses 3355. | The list was used only to corroborate the 13.38% Primary Gaming Corridor rate and the property classifications. The addresses come from the properties' own official pages. |
| 9 | Caesars Palace hotel page | The official page carries no resort-fee table and no dated rate. | The $54.95 fee comes from a secondary travel-industry source, not from Caesars. It is labelled as secondary everywhere it appears and the official Caesars link is given alongside it. |
| 10 | Venetian and Caesars booking engines | Both booking pages return only a JavaScript loading shell to a plain fetch, so no dated room inventory or rate can be read. | A blank server-rendered result was not treated as "no availability". The room rate stays blank and the reason is recorded. |
| 11 | Venetian parking page | `venetianlasvegas.com/resort/parking.html` returns HTTP 404. | The parking figures are taken from the official hotel terms and conditions page, which still publishes them. |
| 12 | Visit Las Vegas and Venetian "getting here" pages | Both return HTTP 404. | Neither is linked from the site. Walking directions come from Google Maps and Apple Maps links instead. |

## Handling rule

Where an official document contradicts itself, the planner does not pick a side silently.
The contradiction is reproduced in the row's note, the row is placed in the separate-formats
section or marked unverified, and the two readings are both recorded here.
