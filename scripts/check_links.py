#!/usr/bin/env python3
"""Validate the generated site, its source-linked data, and derived schedules."""
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
)
# Exact hosts, not substring matches: data rows must point to official venue / operator sources.
OFFICIAL_SOURCE_HOSTS = {
    "www.venetianlasvegas.com",
    "www.wynnlasvegas.com",
    "cdn.wynnresorts.com",
    "aria.mgmresorts.com",
    "bellagio.mgmresorts.com",
    "www.caesars.com",
}
TOURNAMENT_STATUSES = {"SE", "MULTI", "RE", "UNV"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TIME_RE = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d$")


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
        if not isinstance(url, str) or not url.strip():
            problems.append(f"{where} has no URL")
            continue
        parsed = urlparse(url)
        if parsed.scheme != "https" or not parsed.hostname:
            problems.append(f"{where} must use an https URL: {url}")
            continue
        if parsed.hostname.lower() not in OFFICIAL_SOURCE_HOSTS:
            problems.append(f"{where} has a non-approved source host: {parsed.hostname}")
            continue
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


for rel in REQUIRED_SITE_DOCS:
    if not os.path.isfile(os.path.join(ROOT, rel)):
        problems.append(f"{rel}: required Markdown content for the deployed dashboard is missing")

tournaments_data = load_json("data/tournaments.json")
hotels_data = load_json("data/hotels.json")
schedule_data = load_json("data/schedule.json")
tournament_rows = check_rows_shape("data/tournaments.json", tournaments_data)
hotel_rows = check_rows_shape("data/hotels.json", hotels_data)
for rel, payload in (("data/tournaments.json", tournaments_data),
                     ("data/hotels.json", hotels_data),
                     ("data/schedule.json", schedule_data)):
    if isinstance(payload, dict) and "verified_on" in payload:
        check_date(payload.get("verified_on"), f"{rel} verified_on", required=True)
if schedule_data is not None and not isinstance(schedule_data, dict):
    problems.append("data/schedule.json: top-level JSON value must be an object")

# Tournaments: every row is identified, classified, dated where known, and source-linked.
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

    for field in ("series", "name", "entry_rule"):
        if not isinstance(row.get(field), str) or not row[field].strip():
            problems.append(f"{where} {identity}: {field} must be non-empty text")
    status = row.get("entry_status")
    if not isinstance(status, str) or status not in TOURNAMENT_STATUSES:
        problems.append(f"{where} {identity}: unsupported entry_status {status!r}")
    check_date(row.get("date"), f"{where} {identity}", required=status == "SE")
    check_time(row.get("start"), f"{where} {identity}", required=status == "SE")
    check_date(row.get("verified_on"), f"{where} {identity} verified_on", required=True)

    check_sources("data/tournaments.json", row, identity)
    entry_rule = str(row.get("entry_rule", "")).lower()
    sources = row.get("sources") if isinstance(row.get("sources"), list) else []
    if status == "SE":
        if not any("structure" in str(source.get("label", "")).lower()
                   for source in sources if isinstance(source, dict)):
            problems.append(f"{where} {identity}: SE row must link its official structure sheet")
        if not re.search(r"single[ -]entry", entry_rule):
            problems.append(f"{where} {identity}: SE entry_rule must explicitly state its verified classification")
        if re.search(r"unverified|not confirmed|unclear|possible multiple", entry_rule):
            problems.append(f"{where} {identity}: SE entry_rule contains unresolved wording")
    elif status == "MULTI" and not re.search(r"multi|flight|multiple", entry_rule):
        problems.append(f"{where} {identity}: MULTI entry_rule must explain possible additional entries")
    elif status == "RE" and not re.search(r"re[ -]?entr", entry_rule):
        problems.append(f"{where} {identity}: RE row must describe the re-entry rule")
    elif status == "UNV" and not re.search(r"unverif|not confirmed|unclear", entry_rule):
        problems.append(f"{where} {identity}: UNV entry_rule must identify the rule as unverified")

    for field in ("buy_in_usd", "guarantee_usd", "house_fee_usd", "house_fee_pct", "gtd_multiple"):
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
    if is_number(fee) and fee > 0 and is_number(buy_in) and buy_in > 0:
        expected_fee_pct = round(100 * fee / buy_in, 2)
        if not is_number(fee_pct) or abs(fee_pct - expected_fee_pct) > 0.01:
            problems.append(f"{where} {identity}: house_fee_pct should be {expected_fee_pct}")
    elif fee is None and fee_pct is not None:
        problems.append(f"{where} {identity}: house_fee_pct must be blank without a confirmed house fee")

# Hotels: total cost is allowed only when all required, property-specific inputs are present.
hotel_by_id = {}
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
    check_sources("data/hotels.json", row, identity)

    for field in ("room_rate_usd", "resort_fee_usd", "clark_county_tax_pct",
                  "true_cost_per_night_usd", "walk_to_venetian_min"):
        check_number(row.get(field), f"{where} {identity} {field}")
    room = row.get("room_rate_usd")
    fee = row.get("resort_fee_usd")
    tax = row.get("clark_county_tax_pct")
    total = row.get("true_cost_per_night_usd")
    walk = row.get("walk_to_venetian_min")
    if is_number(walk) and walk > 30:
        problems.append(f"{where} {identity}: hotel is outside the 30-minute walking limit")
    inputs_confirmed = all(is_number(value) for value in (room, fee, tax))
    if total is not None and not inputs_confirmed:
        problems.append(f"{where} {identity}: nightly total must be blank until room rate, resort fee, and tax are confirmed")
    elif inputs_confirmed:
        expected_total = round((room + fee) * (1 + tax / 100), 2)
        if not is_number(total) or abs(total - expected_total) > 0.01:
            problems.append(f"{where} {identity}: true_cost_per_night_usd should be {expected_total}")

# Schedule: every listed option must exactly correspond to a verified-SE source row.
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
        options = day.get("options")
        if not isinstance(options, list) or not options:
            problems.append(f"{where}: options must be a non-empty list")
            continue
        for option_index, event in enumerate(options, 1):
            event_where = f"{where} option {option_index}"
            if not isinstance(event, dict):
                problems.append(f"{event_where}: option must be an object")
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
            if row.get("entry_status") != "SE":
                problems.append(f"{event_where}: {identity} is not classified as verified single-entry")
            if row.get("date") != day_date:
                problems.append(f"{event_where}: date does not match tournament row {identity}")
            for field in ("start", "series", "name", "buy_in_usd", "guarantee_usd"):
                if event.get(field) != row.get(field):
                    problems.append(f"{event_where}: {field} does not match tournament row {identity}")
            row_sources = row.get("sources") if isinstance(row.get("sources"), list) else []
            valid_sources = {source.get("url") for source in row_sources if isinstance(source, dict)}
            if event.get("source") not in valid_sources:
                problems.append(f"{event_where}: source is not attached to tournament row {identity}")
            source_url = event.get("source")
            if not isinstance(source_url, str) or urlparse(source_url).hostname not in OFFICIAL_SOURCE_HOSTS:
                problems.append(f"{event_where}: source is not an approved official host")
    expected_ids = {identity for identity, row in tournament_by_id.items()
                    if row.get("entry_status") == "SE"}
    if scheduled_ids != expected_ids:
        missing = sorted(expected_ids - scheduled_ids)
        extra = sorted(scheduled_ids - expected_ids, key=str)
        if missing:
            problems.append(f"data/schedule.json: verified-SE rows missing from schedule: {missing}")
        if extra:
            problems.append(f"data/schedule.json: non-SE or unknown rows included in schedule: {extra}")

# Static page links and inline-only assets; authored pages must resolve within the staged site.
class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if attributes.get("id"):
            self.ids.append(attributes["id"])
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

if problems:
    print("\n".join(problems))
    sys.exit(1)
print(f"check_links: OK ({len(pages)} pages, {len(tournament_rows)} tournament rows, "
      f"{len(hotel_rows)} hotels; source, schedule, hotel cost/walk-limit, and local-link checks passed)")
