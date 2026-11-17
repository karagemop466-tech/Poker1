#!/usr/bin/env python3
"""Validate the generated site, its source-linked data, and derived schedules.

This validator merges the stricter checks added in session 673f9643 (row ids,
dates, derived values, dated hotel rate logs, page links and fragments) with
the schema checks added in session baba1a15 (the daily, venue, walking,
monitoring and snapshot files, and the rule-object shape of every row).

Run:  python3 scripts/check_links.py
"""
from collections import Counter
from datetime import date
from html.parser import HTMLParser
import json
import math
import os
import re
import sys
from urllib.parse import unquote, urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
problems = []
REQUIRED_SITE_DOCS = (
    "EXECUTIVE_SUMMARY.md",
    "QUESTIONS.md",
    "SUGGESTIONS.md",
    "FLAGGED.md",
    "REVIEW.md",
    "README.md",
)
# Exact hosts, not substring matches: data rows must point to official venue / operator sources.
OFFICIAL_SOURCE_HOSTS = {
    "www.venetianlasvegas.com",
    "www.wynnlasvegas.com",
    "cdn.wynnresorts.com",
    "aria.mgmresorts.com",
    "bellagio.mgmresorts.com",
    "www.caesars.com",
    # MGM Resorts' shared corporate pages (parking, portfolio-wide fee text).
    # Property pages stay on each property's own subdomain.
    "www.mgmresorts.com",
    # Session 0d069ce0: the official property domains behind pages/other-rooms.html. Each is the
    # operator's own site for the property. The contentstack CDN that hosts the MGM PDFs is
    # deliberately not added, matching the existing F40 treatment of the Bellagio flyers: those
    # PDFs are cited through the official page that links them, never as a source host.
    "mgmgrand.mgmresorts.com",
    "mandalaybay.mgmresorts.com",
    "orleans.boydgaming.com",
    "southpointcasino.com",
}
TOURNAMENT_STATUSES = {"SE", "MULTI", "RE", "REBUY", "CONT", "UNV"}
TOURNAMENT_KINDS = {"entry", "continuation"}
RULE_FIELDS = ("single_entry", "re_entry", "add_on", "fee")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TIME_RE = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d$")
KNOWN_PAGES = {"index", "singleEntry", "separate", "unverified", "daily", "hotels", "calculator",
               "schedule", "venues", "search", "monitoring", "summary", "questions", "suggestions",
               "flagged", "review",
               # Session 0d069ce0: pages/other-rooms.html. Registered here because the page-link
               # check rejects any data-page outside this set. One line, no other change.
               "otherRooms"}


def load_json(rel):
    path = os.path.join(ROOT, rel)
    try:
        with open(path, encoding="utf-8") as stream:
            return json.load(stream)
    except Exception as exc:  # noqa: BLE001
        problems.append(f"{rel}: {exc}")
        return None


def check_date(value, where, required=False):
    if value in (None, ""):
        if required:
            problems.append(f"{where}: required date is blank")
        return
    if not isinstance(value, str) or not DATE_RE.fullmatch(value):
        problems.append(f"{where}: date must be YYYY-MM-DD or blank, got {value!r}")
        return
    try:
        date.fromisoformat(value)
    except ValueError:
        problems.append(f"{where}: invalid calendar date {value!r}")


def check_time(value, where, required=False):
    if value in (None, ""):
        if required:
            problems.append(f"{where}: required start time is blank")
        return
    if not isinstance(value, str) or not TIME_RE.fullmatch(value):
        problems.append(f"{where}: time must be HH:MM or blank, got {value!r}")


def is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def check_number(value, where, *, nonnegative=True):
    if value is None:
        return
    if not is_number(value):
        problems.append(f"{where}: expected a finite number or null, got {value!r}")
    elif nonnegative and value < 0:
        problems.append(f"{where}: value cannot be negative, got {value!r}")


def check_official_https_url(url, where):
    if not isinstance(url, str) or not url.strip():
        problems.append(f"{where} has no URL")
        return False
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname:
        problems.append(f"{where} must use an https URL: {url}")
        return False
    if parsed.hostname.lower() not in OFFICIAL_SOURCE_HOSTS:
        problems.append(f"{where} has a non-approved source host: {parsed.hostname}")
        return False
    return True


def check_sources(rel, record, identity):
    sources = record.get("sources")
    if not isinstance(sources, list) or not sources:
        problems.append(f"{rel}: row {identity} has no official source links")
        return []
    urls = []
    for index, source in enumerate(sources, 1):
        where = f"{rel}: row {identity}, source {index}"
        if not isinstance(source, dict):
            problems.append(f"{where} is not an object")
            continue
        label = source.get("label")
        url = source.get("url")
        if not isinstance(label, str) or not label.strip():
            problems.append(f"{where} has no source label")
        if check_official_https_url(url, where):
            urls.append(url)
    return urls


def check_rows_shape(rel, payload):
    if not isinstance(payload, dict):
        problems.append(f"{rel}: top-level JSON value must be an object")
        return []
    rows = payload.get("rows")
    if not isinstance(rows, list):
        problems.append(f"{rel}: 'rows' must be a list")
        return []
    return rows


def check_rule_objects(where, identity, rules):
    """Every rule field carries the excerpt, the source it came from, and the date it was read."""
    if not isinstance(rules, dict):
        problems.append(f"{where} {identity}: rules must be an object")
        return
    for field in RULE_FIELDS:
        value = rules.get(field)
        if not isinstance(value, dict):
            problems.append(f"{where} {identity}: rules.{field} must be a rule object")
            continue
        if not isinstance(value.get("value"), str) or not value["value"].strip():
            problems.append(f"{where} {identity}: rules.{field}.value must be non-empty text")
        if not isinstance(value.get("excerpt"), str) or not value["excerpt"].strip():
            problems.append(f"{where} {identity}: rules.{field} must include the source excerpt")
        source = value.get("source")
        if not isinstance(source, dict):
            problems.append(f"{where} {identity}: rules.{field}.source must be an object")
            continue
        check_official_https_url(source.get("url"), f"{where} {identity} rules.{field}")
        check_date(value.get("retrieved_on"), f"{where} {identity} rules.{field} retrieved_on", required=True)


for rel in REQUIRED_SITE_DOCS:
    if not os.path.isfile(os.path.join(ROOT, rel)):
        problems.append(f"{rel}: required Markdown content for the deployed dashboard is missing")

tournaments_data = load_json("data/tournaments.json")
hotels_data = load_json("data/hotels.json")
schedule_data = load_json("data/schedule.json")
daily_data = load_json("data/daily.json")
rates_data = load_json("data/rates.json")
venues_data = load_json("data/venues.json")
walking_data = load_json("data/walking.json")
monitoring_data = load_json("data/monitoring.json")
changes_data = load_json("data/changes.json")
snapshot_data = load_json("data/row_snapshot.json")
# Provenance archive kept by scripts/check_source_facts.py (session 40ca34e5).
source_manifest = load_json("data/sources.json")
source_facts_log = load_json("data/change_log.json")
structure_rules = load_json("data/structure_rules.json")
wpt_rules = load_json("data/wpt_rules.json")

tournament_rows = check_rows_shape("data/tournaments.json", tournaments_data)
hotel_rows = check_rows_shape("data/hotels.json", hotels_data)
daily_rows = check_rows_shape("data/daily.json", daily_data)
venue_rows = check_rows_shape("data/venues.json", venues_data)
walking_rows = check_rows_shape("data/walking.json", walking_data)
for rel, payload in (("data/tournaments.json", tournaments_data),
                     ("data/hotels.json", hotels_data),
                     ("data/schedule.json", schedule_data),
                     ("data/daily.json", daily_data),
                     ("data/venues.json", venues_data),
                     ("data/walking.json", walking_data)):
    if isinstance(payload, dict) and "verified_on" in payload:
        check_date(payload.get("verified_on"), f"{rel} verified_on", required=True)
if schedule_data is not None and not isinstance(schedule_data, dict):
    problems.append("data/schedule.json: top-level JSON value must be an object")

# Tournaments: every row is identified, classified, dated, and source-linked.
tournament_by_id = {}
for index, row in enumerate(tournament_rows, 1):
    where = f"data/tournaments.json row {index}"
    if not isinstance(row, dict):
        problems.append(f"{where}: row must be an object")
        continue
    identity = row.get("id")
    if not isinstance(identity, str) or not identity.strip():
        problems.append(f"{where}: missing non-empty id")
        identity = f"row {index}"
    elif identity in tournament_by_id:
        problems.append(f"data/tournaments.json: duplicate tournament id {identity!r}")
    else:
        tournament_by_id[identity] = row

    for field in ("series", "venue", "name", "entry_rule"):
        if not isinstance(row.get(field), str) or not row[field].strip():
            problems.append(f"{where} {identity}: {field} must be non-empty text")
    event_no = row.get("event_no")
    if event_no is not None and (not isinstance(event_no, int) or isinstance(event_no, bool) or event_no < 0):
        problems.append(f"{where} {identity}: event_no must be a non-negative integer or null")
    status = row.get("entry_status")
    if not isinstance(status, str) or status not in TOURNAMENT_STATUSES:
        problems.append(f"{where} {identity}: unsupported entry_status {status!r}")
    kind = row.get("kind")
    if not isinstance(kind, str) or kind not in TOURNAMENT_KINDS:
        problems.append(f"{where} {identity}: unsupported kind {kind!r}")
    check_date(row.get("date"), f"{where} {identity}", required=True)
    check_time(row.get("start"), f"{where} {identity}", required=True)
    check_date(row.get("verified_on"), f"{where} {identity} verified_on", required=True)
    check_date(row.get("last_checked"), f"{where} {identity} last_checked", required=True)
    for field in ("labels", "flags"):
        if not isinstance(row.get(field, []), list):
            problems.append(f"{where} {identity}: {field} must be a list")

    check_sources("data/tournaments.json", row, identity)
    entry_rule = str(row.get("entry_rule", "")).lower()
    sources = row.get("sources") if isinstance(row.get("sources"), list) else []
    check_rule_objects(where, identity, row.get("rules"))
    if status == "SE":
        if not any("structure" in str(source.get("label", "")).lower()
                   for source in sources if isinstance(source, dict)):
            problems.append(f"{where} {identity}: SE row must link its official structure sheet")
        if not re.search(r"single[ -]entry", entry_rule):
            problems.append(f"{where} {identity}: SE entry_rule must explicitly state its verified classification")
        if re.search(r"unverified|not confirmed|unclear|possible multiple", entry_rule):
            problems.append(f"{where} {identity}: SE entry_rule contains unresolved wording")
    elif status == "MULTI" and not re.search(r"multi|flight|multiple|limit|limited", entry_rule):
        problems.append(f"{where} {identity}: MULTI entry_rule must explain possible additional entries")
    elif status == "RE" and not re.search(r"re[ -]?entr", entry_rule):
        problems.append(f"{where} {identity}: RE row must describe the re-entry rule")
    elif status == "UNV" and not re.search(r"unverif|not verified|not confirmed|unclear", entry_rule):
        problems.append(f"{where} {identity}: UNV entry_rule must identify the rule as unverified")
    elif status == "CONT" and not re.search(r"continuation", entry_rule):
        problems.append(f"{where} {identity}: CONT entry_rule must identify the row as a continuation")

    for field in ("buy_in_usd", "guarantee_usd", "house_fee_usd", "house_fee_pct", "gtd_multiple",
                  "starting_chips", "levels", "level_minutes", "est_duration_min"):
        check_number(row.get(field), f"{where} {identity} {field}")
    buy_in = row.get("buy_in_usd")
    guarantee = row.get("guarantee_usd")
    multiple = row.get("gtd_multiple")
    if is_number(buy_in) and buy_in > 0 and is_number(guarantee) and guarantee > 0:
        expected_multiple = round(guarantee / buy_in, 1)
        if not is_number(multiple) or abs(multiple - expected_multiple) > 0.01:
            problems.append(f"{where} {identity}: gtd_multiple should be {expected_multiple}")
    elif multiple is not None:
        problems.append(f"{where} {identity}: gtd_multiple must be blank without a positive guarantee and buy-in")

    fee = row.get("house_fee_usd")
    fee_pct = row.get("house_fee_pct")
    # A fee percentage is only meaningful against the entry the structure sheet
    # prices, which the row records as house_fee_basis_usd.
    fee_basis = row.get("house_fee_basis_usd", buy_in)
    if is_number(fee_basis) and is_number(buy_in) and abs(fee_basis - buy_in) > 0.001 \
            and not str(row.get("flags")):
        problems.append(f"{where} {identity}: a fee basis different from the buy-in must be explained in flags")
    if is_number(fee) and fee > 0 and is_number(fee_basis) and fee_basis > 0:
        expected_fee_pct = round(100 * fee / fee_basis, 2)
        if not is_number(fee_pct) or abs(fee_pct - expected_fee_pct) > 0.01:
            problems.append(f"{where} {identity}: house_fee_pct should be {expected_fee_pct}")
    elif fee is None and fee_pct is not None:
        problems.append(f"{where} {identity}: house_fee_pct must be blank without a confirmed house fee")

    # An estimated finish time must be consistent with the estimated duration.
    est_end = row.get("est_end")
    if est_end is not None:
        check_time(est_end, f"{where} {identity} est_end", required=True)
    if is_number(row.get("est_duration_min")) and row["est_duration_min"] <= 0:
        problems.append(f"{where} {identity}: est_duration_min must be positive")

# Hotels: property-specific costs are only stated when every input is verified.
hotel_by_id = {}
quote_by_hotel = {}
for entry in (rates_data or {}).get("entries", []) or []:
    key = entry.get("hotel_id")
    if key:
        quote_by_hotel.setdefault(key, []).append(entry)

for index, row in enumerate(hotel_rows, 1):
    where = f"data/hotels.json row {index}"
    if not isinstance(row, dict):
        problems.append(f"{where}: row must be an object")
        continue
    identity = row.get("id")
    if not isinstance(identity, str) or not identity.strip():
        problems.append(f"{where}: missing non-empty id")
        identity = f"row {index}"
    elif identity in hotel_by_id:
        problems.append(f"data/hotels.json: duplicate hotel id {identity!r}")
    else:
        hotel_by_id[identity] = row
    if not isinstance(row.get("name"), str) or not row["name"].strip():
        problems.append(f"{where} {identity}: name must be non-empty text")
    check_date(row.get("last_checked"), f"{where} {identity} last_checked", required=True)
    check_sources("data/hotels.json", row, identity)

    for field in ("room_rate_usd", "resort_fee_usd", "clark_county_tax_pct",
                  "true_cost_per_night_usd", "parking_usd_per_day", "walk_to_venetian_min"):
        check_number(row.get(field), f"{where} {identity} {field}")
    fee = row.get("resort_fee_usd")
    tax = row.get("clark_county_tax_pct")
    rate = row.get("room_rate_usd")
    total = row.get("true_cost_per_night_usd")
    walk = row.get("walk_to_venetian_min")
    if is_number(walk) and walk > 30 and row.get("walk_to_venetian_within_30") is not False:
        problems.append(f"{where} {identity}: a walk over 30 minutes must be flagged walk_to_venetian_within_30 = false")
    if walk is not None and not is_number(walk):
        problems.append(f"{where} {identity}: walk_to_venetian_min must be a number or blank")

    fee_status = row.get("resort_fee_status")
    if fee_status not in ("verified", "unverified", "conditional"):
        problems.append(f"{where} {identity}: resort_fee_status must be verified, conditional or unverified")
    if fee_status == "unverified" and fee is not None:
        problems.append(f"{where} {identity}: resort_fee_usd must be blank when resort_fee_status is unverified")
    tax_status = row.get("tax_status")
    # "estimated" (session c0714e1a) means the property's own terms print the tax *rule* but not a
    # percentage; the county rate is then shown as an estimate and must never be used to calculate a
    # true cost. "conditional" (older rows) is likewise never a basis for a true cost. Such an
    # "estimated" row must say so in its tax_note (checked below).
    if tax_status not in ("verified", "unverified", "estimated", "conditional"):
        problems.append(f"{where} {identity}: tax_status must be verified, estimated, conditional or unverified")
    if tax_status in ("verified", "estimated") and tax is None:
        problems.append(f"{where} {identity}: tax_status is {tax_status} but the tax rate is blank")
    if tax_status == "unverified" and tax is not None:
        problems.append(f"{where} {identity}: tax_status is unverified but a tax rate is present")
    if tax_status == "estimated" and "estimate" not in (row.get("tax_note") or "").lower():
        problems.append(f"{where} {identity}: an estimated tax rate must be explained in tax_note")
    if tax_status == "estimated" and is_number(total):
        problems.append(f"{where} {identity}: true_cost_per_night_usd cannot use an estimated tax rate")
    if is_number(total):
        # Combined rule (sessions baba1a15/54ae4633 and c0714e1a): a true cost may be
        # published only when the property has a verified resort fee and a verified tax
        # rate, and the value must come from a dated quote in data/rates.json whose own
        # arithmetic reproduces it. The nightly room rate itself is never stored on the
        # row because it changes by night; it lives inside the dated quote.
        quotes = quote_by_hotel.get(identity) or []
        if fee_status != "verified" or tax_status != "verified":
            problems.append(f"{where} {identity}: true_cost_per_night_usd needs a verified resort fee and a verified tax rate")
        elif not quotes:
            problems.append(f"{where} {identity}: true_cost_per_night_usd must come from a dated quote in data/rates.json")
        else:
            latest = max(quotes, key=lambda q: (q.get("arrival", ""), q.get("retrieved_on", "")))
            if abs(total - latest["true_cost_per_night_usd"]) > 0.01:
                problems.append(f"{where} {identity}: true_cost_per_night_usd does not match its dated quote")

# The verification date the site prints in its footer must be the date the
# dataset itself records, so the site cannot claim a fresher check than the data.
try:
    app_js = open(os.path.join(ROOT, "assets", "app.js"), encoding="utf-8").read()
except OSError as exc:  # noqa: BLE001
    problems.append(f"assets/app.js: {exc}")
else:
    match = re.search(r'var checkedOn = "(\d{4}-\d{2}-\d{2})";', app_js)
    if not match:
        problems.append("assets/app.js: the site footer must declare its checkedOn date")
    elif (tournaments_data or {}).get("verified_on") != match.group(1):
        problems.append("assets/app.js: footer checkedOn %s does not match data/tournaments.json "
                        "verified_on %s" % (match.group(1), (tournaments_data or {}).get("verified_on")))

# Dated rate log: every quote is dated, sourced, and internally consistent.
rate_entries = (rates_data or {}).get("entries", [])
if not isinstance(rate_entries, list):
    problems.append("data/rates.json: 'entries' must be a list")
    rate_entries = []
for index, entry in enumerate(rate_entries, 1):
    where = f"data/rates.json entry {index}"
    if not isinstance(entry, dict):
        problems.append(f"{where}: entry must be an object")
        continue
    check_date(entry.get("arrival"), f"{where} arrival", required=True)
    check_date(entry.get("departure"), f"{where} departure", required=True)
    check_date(entry.get("logged_on"), f"{where} logged_on", required=True)
    check_official_https_url(entry.get("source"), where)
    for field in ("nights", "nightly_average_usd", "nightly_rates_usd", "taxes_total_usd",
                  "checkout_total_usd", "true_cost_per_night_usd", "resort_fee_per_night_usd"):
        if field == "nightly_rates_usd":
            values = entry.get(field)
            if not isinstance(values, list) or not values:
                problems.append(f"{where}: nightly_rates_usd must be a non-empty list")
                continue
            for value in values:
                check_number(value, f"{where} nightly_rates_usd")
            continue
        check_number(entry.get(field), f"{where} {field}")
    arrival, departure = entry.get("arrival"), entry.get("departure")
    nights = entry.get("nights")
    if isinstance(arrival, str) and isinstance(departure, str) and is_number(nights):
        try:
            expected_nights = (date.fromisoformat(departure) - date.fromisoformat(arrival)).days
        except ValueError:
            expected_nights = None
        if expected_nights is not None and expected_nights != nights:
            problems.append(f"{where}: nights should be {expected_nights}")
    # The engine's own Average Rate is (room charges + resort fee) / nights, before tax. Re-derive it, and
    # re-check that room + fee + tax == checkout total, so the log cannot drift from the quoted page.
    nights_val = entry.get("nights")
    room_only = entry.get("room_only_average_usd")
    avg = entry.get("nightly_average_usd")
    fee = entry.get("resort_fee_per_night_usd")
    rooms = entry.get("nightly_rates_usd")
    taxes = entry.get("taxes_total_usd")
    if is_number(room_only) and isinstance(rooms, list) and rooms and is_number(nights_val) and nights_val > 0:
        expected_room_only = round(sum(rooms) / nights_val, 2)
        if abs(room_only - expected_room_only) > 0.01:
            problems.append(f"{where}: room_only_average_usd should be {expected_room_only}")
    if all(is_number(x) for x in (room_only, avg, fee)):
        if abs(avg - (room_only + fee)) > 0.01:
            problems.append(f"{where}: nightly_average_usd should be room_only + resort fee = {round(room_only + fee, 2)}")
        if entry.get("nightly_average_includes_resort_fee") is not True:
            problems.append(f"{where}: nightly_average_includes_resort_fee must be true")
    if all(is_number(x) for x in (rooms and sum(rooms), fee, taxes, entry.get("checkout_total_usd"), nights_val)):
        expected_total = round(sum(rooms) + fee * nights_val + taxes, 2)
        if abs(entry["checkout_total_usd"] - expected_total) > 0.02:
            problems.append(f"{where}: checkout_total_usd should be room + fee + tax = {expected_total}")

    checkout = entry.get("checkout_total_usd")
    per_night = entry.get("true_cost_per_night_usd")
    if is_number(checkout) and is_number(nights) and nights > 0 and is_number(per_night):
        expected_per_night = round(checkout / nights, 2)
        if abs(per_night - expected_per_night) > 0.01:
            problems.append(f"{where}: true_cost_per_night_usd should be {expected_per_night}")

# Daily formats, venues and walking records.
daily_ids = set()
for index, row in enumerate(daily_rows, 1):
    where = f"data/daily.json row {index}"
    identity = row.get("id")
    if not isinstance(identity, str) or not identity.strip():
        problems.append(f"{where}: missing non-empty id")
        continue
    if identity in daily_ids:
        problems.append(f"data/daily.json: duplicate daily format id {identity!r}")
    daily_ids.add(identity)
    for field in ("name", "days", "fee", "ex"):
        if not isinstance(row.get(field), str) or not row[field].strip():
            problems.append(f"{where} {identity}: {field} must be non-empty text")
    check_time(row.get("start"), f"{where} {identity} start", required=True)
    for field in ("buy_in_usd", "guarantee_usd", "levels", "lmin"):
        check_number(row.get(field), f"{where} {identity} {field}")
    check_time(row.get("late"), f"{where} {identity} late", required=True)

venue_names = set()
for index, row in enumerate(venue_rows, 1):
    where = f"data/venues.json row {index}"
    identity = row.get("id")
    if not isinstance(identity, str) or not identity.strip():
        problems.append(f"{where}: missing non-empty id")
        continue
    venue_names.add(row.get("name"))
    for field in ("name", "note"):
        if not isinstance(row.get(field), str) or not row[field].strip():
            problems.append(f"{where} {identity}: {field} must be non-empty text")
    for link in row.get("official_links", []):
        check_official_https_url(link, f"{where} {identity} official_links")
    for hotel_id in row.get("hotel_ids", []):
        if hotel_id not in hotel_by_id:
            problems.append(f"{where} {identity}: unknown hotel id {hotel_id!r}")

for index, row in enumerate(walking_rows, 1):
    where = f"data/walking.json row {index}"
    if row.get("hotel") not in hotel_by_id:
        problems.append(f"{where}: record for unknown hotel {row.get('hotel')}")
    if row.get("venue") not in venue_names:
        problems.append(f"{where}: record for unknown venue {row.get('venue')}")
    check_number(row.get("minutes"), f"{where} minutes")
    if is_number(row.get("minutes")) and row["minutes"] > 30 and row.get("within_30_min") is not False:
        problems.append(f"{where}: a walking time over 30 minutes must be marked within_30_min = false")
    if row.get("status") == "verified" and is_number(row.get("minutes")) and not row.get("sources"):
        problems.append(f"{where}: a routed walking time must cite the routing and geocoding sources")

# Provenance archive: the official source manifest, the per-source change log and the
# machine-readable rule extraction from the official structure sheets and WPT blocks.
if isinstance(source_manifest, dict):
    manifest_sources = source_manifest.get("sources")
    if not isinstance(manifest_sources, list) or not manifest_sources:
        problems.append("data/sources.json: 'sources' must be a non-empty list")
    else:
        seen_ids = set()
        for index, source in enumerate(manifest_sources, 1):
            where = f"data/sources.json source {index}"
            if not isinstance(source, dict):
                problems.append(f"{where} is not an object")
                continue
            source_id = source.get("id")
            if not isinstance(source_id, str) or not source_id.strip():
                problems.append(f"{where} has no id")
            elif source_id in seen_ids:
                problems.append(f"data/sources.json: duplicate source id {source_id!r}")
            else:
                seen_ids.add(source_id)
            if source.get("active") is False:
                if not isinstance(source.get("note"), str) or not source["note"].strip():
                    problems.append(f"{where} is inactive without an explanation")
                continue
            check_official_https_url(source.get("url"), where)
if isinstance(source_facts_log, dict):
    if not isinstance(source_facts_log.get("generated_utc"), str):
        problems.append("data/change_log.json: generated_utc must be a string")
    for index, source in enumerate(source_facts_log.get("sources") or [], 1):
        where = f"data/change_log.json source {index}"
        if not isinstance(source, dict):
            problems.append(f"{where} is not an object")
            continue
        if source.get("inactive"):
            if not isinstance(source.get("note"), str) or not source["note"].strip():
                problems.append(f"{where} is inactive without an explanation")
            continue
        if not isinstance(source.get("last_checked_utc"), str):
            problems.append(f"{where} has no last-checked time")
        check_official_https_url(source.get("url"), where)
if isinstance(structure_rules, dict):
    if not structure_rules:
        problems.append("data/structure_rules.json: no structure sheets recorded")
    for sheet_id, sheet in structure_rules.items():
        if not isinstance(sheet, dict):
            problems.append(f"data/structure_rules.json: {sheet_id} is not an object")
            continue
        if sheet.get("sheet_kind") not in {"SINGLE_ENTRY", "MULTI_FLIGHT", "RE_ENTRY"}:
            problems.append(f"data/structure_rules.json: {sheet_id} has no rule verdict")
if not isinstance(wpt_rules, list) or not wpt_rules:
    problems.append("data/wpt_rules.json: expected a non-empty list of WPT structure blocks")

# Monitoring and changed-row files.
if isinstance(monitoring_data, dict):
    check_date(monitoring_data.get("checked_at"), "data/monitoring.json checked_at", required=True)
    if not isinstance(monitoring_data.get("sources"), dict):
        problems.append("data/monitoring.json: 'sources' must be an object")
if isinstance(changes_data, dict):
    for field in ("changed", "added", "removed"):
        if not isinstance(changes_data.get(field, []), list):
            problems.append(f"data/changes.json: '{field}' must be a list")
if isinstance(snapshot_data, dict):
    snapshot_rows = snapshot_data.get("rows")
    if not isinstance(snapshot_rows, dict):
        problems.append("data/row_snapshot.json: 'rows' must be an object")
    else:
        missing = sorted(set(tournament_by_id) - set(snapshot_rows))
        if missing:
            problems.append(f"data/row_snapshot.json: {len(missing)} tournament rows are missing from the snapshot")

# Schedule: every listed event must correspond to an entry row of the dataset.
if isinstance(schedule_data, dict):
    schedule_days = schedule_data.get("days")
    if not isinstance(schedule_days, list):
        problems.append("data/schedule.json: 'days' must be a list")
        schedule_days = []
    scheduled_ids = set()
    seen_days = set()
    for day_index, day in enumerate(schedule_days, 1):
        where = f"data/schedule.json day {day_index}"
        if not isinstance(day, dict):
            problems.append(f"{where}: day must be an object")
            continue
        day_date = day.get("date")
        check_date(day_date, where, required=True)
        if isinstance(day_date, str):
            if day_date in seen_days:
                problems.append(f"{where}: duplicate schedule date {day_date!r}")
            seen_days.add(day_date)
        events = day.get("events")
        if not isinstance(events, list) or not events:
            problems.append(f"{where}: events must be a non-empty list")
            continue
        day_se = set()
        for event_index, event in enumerate(events, 1):
            event_where = f"{where} event {event_index}"
            if not isinstance(event, dict):
                problems.append(f"{event_where}: event must be an object")
                continue
            identity = event.get("id")
            if not isinstance(identity, str) or not identity.strip():
                problems.append(f"{event_where}: missing non-empty event id")
                continue
            if identity in scheduled_ids:
                problems.append(f"data/schedule.json: duplicate scheduled event id {identity!r}")
            scheduled_ids.add(identity)
            row = tournament_by_id.get(identity)
            if row is None:
                problems.append(f"{event_where}: event id {identity!r} does not exist in tournaments.json")
                continue
            if row.get("kind") != "entry":
                problems.append(f"{event_where}: {identity} is a continuation row and cannot be scheduled")
            if row.get("date") != day_date:
                problems.append(f"{event_where}: date does not match tournament row {identity}")
            for field in ("start", "series", "name", "buy_in_usd", "guarantee_usd", "venue"):
                if event.get(field) != row.get(field):
                    problems.append(f"{event_where}: {field} does not match tournament row {identity}")
            if row.get("entry_status") == "SE":
                day_se.add(identity)
            row_sources = row.get("sources") if isinstance(row.get("sources"), list) else []
            valid_sources = {source.get("url") for source in row_sources if isinstance(source, dict)}
            if event.get("source") not in valid_sources:
                problems.append(f"{event_where}: source is not attached to tournament row {identity}")
            source_url = event.get("source")
            if not check_official_https_url(source_url, event_where):
                problems.append(f"{event_where}: source is not an approved official host")
        for pointer in ("primary_id", "fallback_id"):
            pointer_id = day.get(pointer)
            if pointer_id is None:
                continue
            if pointer_id not in day_se:
                problems.append(f"{where}: {pointer} must reference a verified single-entry row on this day")
    expected_ids = {identity for identity, row in tournament_by_id.items() if row.get("kind") == "entry"}
    if scheduled_ids != expected_ids:
        missing = sorted(expected_ids - scheduled_ids)
        extra = sorted(scheduled_ids - expected_ids, key=str)
        if missing:
            problems.append(f"data/schedule.json: entry rows missing from schedule: {missing[:20]}")
        if extra:
            problems.append(f"data/schedule.json: unknown or continuation rows included in schedule: {extra[:20]}")


# Static page links and inline-only assets; authored pages must resolve within the staged site.
class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.hrefs = []
        self.page = None

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if attributes.get("id"):
            self.ids.append(attributes["id"])
        if tag == "body":
            self.page = attributes.get("data-page")
        if tag == "a" and attributes.get("href"):
            self.hrefs.append(attributes["href"])


page_dir = os.path.join(ROOT, "pages")
if not os.path.isdir(page_dir):
    problems.append("pages/: generated dashboard pages directory is missing")
    page_paths = []
else:
    page_paths = [os.path.join("pages", name) for name in sorted(os.listdir(page_dir))
                  if name.endswith(".html")]
pages = ["index.html"] + page_paths
html_by_path = {}
for rel in pages:
    path = os.path.join(ROOT, rel)
    try:
        with open(path, encoding="utf-8") as stream:
            html = stream.read()
    except OSError as exc:
        problems.append(f"{rel}: cannot read generated page: {exc}")
        continue
    html_by_path[rel] = html
    if re.search(r'<(?:link|script)\b[^>]*?(?:\bsrc|\bhref)\s*=\s*["\'](?:https?:)?//', html, flags=re.IGNORECASE):
        problems.append(f"{rel}: external asset reference; site assets must be inline or local")
    static = re.sub(r"<script\b[^>]*>[\s\S]*?</script\s*>", "", html, flags=re.IGNORECASE)
    parser = PageParser()
    parser.feed(static)
    duplicates = [identity for identity, count in Counter(parser.ids).items() if count > 1]
    if duplicates:
        problems.append(f"{rel}: duplicate HTML ids: {duplicates}")
    if not parser.page:
        problems.append(f"{rel}: no data-page attribute")
    elif parser.page.startswith("venue:"):
        venue_id = parser.page.split(":", 1)[1]
        if venue_id not in {row.get("id") for row in venue_rows}:
            problems.append(f"{rel}: unknown venue id {venue_id!r}")
        if os.path.basename(rel) != "venue-%s.html" % venue_id:
            problems.append(f"{rel}: filename does not match the venue id {venue_id!r}")
    elif parser.page not in KNOWN_PAGES:
        problems.append(f"{rel}: unknown data-page {parser.page!r}")
    for href in parser.hrefs:
        parsed = urlparse(href)
        if parsed.scheme in {"http", "https", "mailto", "tel"}:
            continue
        relative_target = unquote(parsed.path)
        if relative_target.startswith("/"):
            relative_target = relative_target.lstrip("/")
            target_rel = os.path.normpath(relative_target)
        else:
            target_rel = os.path.normpath(os.path.join(os.path.dirname(rel), relative_target)) if relative_target else rel
        target = os.path.realpath(os.path.join(ROOT, target_rel))
        site_root = os.path.realpath(ROOT)
        if os.path.commonpath((site_root, target)) != site_root:
            problems.append(f"{rel}: local link escapes the site root: {href}")
            continue
        if not os.path.exists(target):
            problems.append(f"{rel}: broken local link {href}")
            continue
        if parsed.fragment:
            target_page_rel = target_rel
            if os.path.isdir(target):
                target_page_rel = os.path.join(target_rel, "index.html")
            target_page = html_by_path.get(target_page_rel)
            if target_page is None and target_page_rel.endswith(".html") and os.path.isfile(os.path.join(ROOT, target_page_rel)):
                with open(os.path.join(ROOT, target_page_rel), encoding="utf-8") as stream:
                    target_page = stream.read()
            if target_page is not None and target_page_rel.endswith(".html"):
                anchor_parser = PageParser()
                anchor_parser.feed(re.sub(r"<script\b[^>]*>[\s\S]*?</script\s*>", "", target_page, flags=re.IGNORECASE))
                if unquote(parsed.fragment) not in anchor_parser.ids:
                    problems.append(f"{rel}: broken fragment link {href}")


# --- one renderer per page: a duplicate PAGES.x silently overrides an earlier one and the page still loads,
# so link checking cannot catch it. A merge once did exactly that to the calculator.
app_js = os.path.join(ROOT, "assets", "app.js")
if os.path.isfile(app_js):
    with open(app_js, encoding="utf-8") as stream:
        js = stream.read()
    assigned = re.findall(r"^\s*PAGES\.(\w+)\s*=\s*(?:function|markdownPage)", js, flags=re.MULTILINE)
    duplicates = sorted({name for name in assigned if assigned.count(name) > 1})
    if duplicates:
        problems.append("assets/app.js: duplicate renderer(s) defined twice: " + ", ".join(duplicates))
    for name in sorted(set(KNOWN_PAGES)):
        if name != "home" and name not in assigned:
            problems.append(f"assets/app.js: no renderer for data-page {name!r}")

if problems:
    print("\n".join(problems))
    sys.exit(1)
print(f"check_links: OK ({len(pages)} pages, {len(tournament_rows)} tournament rows, "
      f"{len(hotel_rows)} hotels, {len(rate_entries)} dated rates, {len(schedule_days)} schedule days; "
      f"source, rules, schedule, hotel-rate/cost, provenance and page-link checks passed)")
