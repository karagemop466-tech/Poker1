# Suggestions

Proposed improvements to this project, so you can review them and choose which to implement. **None of these is
implemented unless you pick it.** Each entry states the decision it would unlock, what it needs, and its cost or
risk. They are ordered by the value they add to a booking decision.

## Already implemented in this session

Listed so you can see what is no longer a suggestion.

| Suggestion | Status |
|---|---|
| Search box across all tables | **done** — one search field filters every column on every table page |
| Date filter | **done** — From/To date pickers on the tournament tables and the day plan |
| Single-entry toggle filter | **done** — the tournaments page separates single entry, multi-entry and unverified; a "flights only" toggle isolates starting flights |
| Structured rule fields per event | **done** — single-entry, re-entry, rebuy, add-on, entries allowed, plus the verbatim sheet excerpt and retrieval time |
| "Last checked" date on every row | **done** |
| Rates as a dated log | **done** — `data/rates.json`, with the printed text and retrieval time per entry |
| Trip cost calculator | **done** — entries × buy-in + nights × true nightly cost |
| Scheduled re-check of official URLs | **done** — a daily GitHub Actions workflow re-fetches every official document, hashes the visible text, and tints rows whose source changed |
| Read every structure sheet and drop the "unverified" label where confirmed | **done for 88 rows** — 52 Venetian structure sheets read automatically |
| One page per venue | **done** — the Venues page |
| Schedule overlap flagging | **done** — the day plan flags events that cannot follow the primary, using the printed late-registration close |
| Executive summary | **done** |
| Suggestions section | this page |

## 1. Highest value: a dated official hotel quote

**Decision it unlocks:** the trip budget, and with it whether the trip is affordable at all.

**What it needs:** one official Venetian/Palazzo poker-suite quote for the exact stay dates. The booking channel is
printed on the official page (866.255.8936, code EPOKR25). The rate is date-dependent, capacity-dependent, and
capped at 150 days out, so it cannot be obtained by scraping a static page.

**Why it cannot be automated:** the quote is produced by a reservation agent for specific dates. No public
official endpoint returns it for an arbitrary date without a booking session.

**Cost:** one phone call. **Risk:** none.

**Recommendation: do this first.** Until it exists, the trip-cost calculator can never show a hotel number.

## 2. High value: settle the multi-flight re-entry question

**Decision it unlocks:** whether the biggest events are usable in a single-entry plan.

Six official sheets print "any player who bags chips for Day 2 may not play a subsequent flight". That clause
prohibits a player who *survives* from re-entering, but it does not say whether a player who *busts* may buy in
again. If a busted player can re-enter, those events are exactly the kind of "spend more to gain an advantage"
event your rules put in the separate section.

**What it needs:** a written answer from the Venetian poker room (702.414.7657, printed on the official page).

**Recommendation:** ask when you call about the hotel rate. One call answers suggestions 1 and 2.

## 3. Medium value: real finish times from published results

**Decision it unlocks:** how many events actually fit in one day.

The operator publishes results PDFs per event. Those give the field size and sometimes the finishing time. Real
finish times would replace the current *estimate* (levels × level length) with observed data, letting more days
pair a primary and a fallback.

**What it needs:** a collector for the results PDFs, which the operator publishes on the same event pages.

**Risk:** results pages are published after the event, so they help plan the *next* trip, not the current one.
Historical finish times also depend on field size, so a small field finishes faster.

**Recommendation:** worth doing for a repeat trip, not for a first booking.

## 4. Medium value: walking times from a non-official map source

**Decision it unlocks:** whether Bellagio, ARIA or Caesars Palace can be tested against the 30-minute rule.

No operator publishes a walking time. The honest options are:

* (a) leave walking times blank, which is what the site does now, and accept that only same-building stays are
  confirmed;
* (b) use a named map provider's walking estimate and label it clearly as a non-official, third-party number with
  its own retrieval date.

**Recommendation:** option (b) if you want a wider hotel choice, but keep the label. The site should never present
a map estimate as an official operator fact.

## 5. Medium value: monitor the Wynn Signature Series structures

**Decision it unlocks:** up to 31 Wynn rows.

The structures PDF currently says "COMING SOON". The daily monitor already fetches it, so the moment Wynn
publishes the file the rows can be classified without any further code change.

**What it needs:** nothing, unless the published file has a different layout, in which case the parser needs a
look.

**Recommendation:** no action. It is already wired up.

## 6. Lower value: extend the dataset to the Wynn daily tournaments

**Decision it unlocks:** more playable days, especially the dates with no verified single-entry event (Dec 19 and
Jan 1–3).

Wynn runs a daily tournament programme (official poster: Monday–Thursday $200 NLH 12 PM, Friday $240 NLH Rebuy
12 PM, Saturday and Sunday $200 NLH 12 PM, plus a nightly $160 NLH $10,000 guarantee at 6 PM). Those are official
and they fill gaps.

**Risk:** the official poster says the daily schedule is **suspended** during each Signature, Millions and Classic
series. The WPT World Championship runs Nov 27 – Dec 21 and the Signature Series runs Jan 11 – 24, so the daily
events may not run during the trip window at all. Also, the Friday event is explicitly a **rebuy** tournament, so
it belongs in the separate section.

**Recommendation:** confirm with the Wynn poker room whether the daily schedule runs on the specific dates before
adding rows, otherwise the dataset will contain events that do not exist.

## 7. Lower value: add the DeepStack Showdown (January 2027)

The official DeepStack page lists a DeepStack Showdown from Jan 11 to Feb 14, 2027, with buy-ins from $250 to
$1,600 and guarantees up to $1M. That extends the trip window past Jan 10.

**What it needs:** the Showdown event page and its structure sheets, read the same way as the other two series.

**Recommendation:** only if the trip may run into late January.

## 8. Presentation improvements, in priority order

| Idea | Why it helps | Effort |
|---|---|---|
| A sticky "my plan" bar showing the chosen events and their total cost | keeps the plan visible while browsing | medium |
| CSV export of the filtered table | lets you work with the data in a spreadsheet | small |
| A per-event detail panel showing the whole official excerpt set | one click from a row to the exact words on the sheet | medium |
| A "no guarantee printed" filter | separates events with a real posted guarantee from those without | small |
| Printing stylesheet for the day plan | a one-page printable plan | small |

## 9. Things this project should **not** do

* **Do not** fill a blank with a third-party value, an average, or a "typical" figure. A blank is information: it
  says the operator does not publish the number.
* **Do not** turn guarantee ÷ buy-in into a predicted return. It is a ratio of two printed values.
* **Do not** merge bounty and non-bounty events into one ranking. A bounty guarantee includes money paid out to
  eliminators, so its ratio is not comparable to a pure prize-pool guarantee.
* **Do not** assert a walking time the site cannot source.
* **Do not** assert that two events can be played back to back without the operator's printed times to support it.
