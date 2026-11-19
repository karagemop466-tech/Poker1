#!/usr/bin/env python3
"""Build the "other Las Vegas poker rooms" dataset and page.

Scope of session 0d069ce0. This script owns three files and nothing else:

    data/other_rooms.json          the dataset
    pages/other-rooms.html         the generated page
    (research/other-rooms-2026-11-17.md is written by hand, not by this script)

Every value below was transcribed on 2026-11-17 from the official page or PDF named on
the row. Nothing is inferred, and nothing comes from a third-party site. Where an
official source publishes a schedule only as an image, no row is invented: the finding
is recorded as a finding with the source that produced it.

Recurring events are stored with `weekdays`, not `date`, because none of these rooms
prints calendar dates for its daily events. They are deliberately kept out of
data/tournaments.json, whose rows are dated and owned by another session.
"""
import html
import json
import os
from collections import OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERIFIED_ON = "2026-11-17"

# --------------------------------------------------------------------------------------
# Official sources read on 2026-11-17
# --------------------------------------------------------------------------------------
MGM_PAGE = "https://mgmgrand.mgmresorts.com/en/casino/poker-tables.html"
MGM_SCHED = ("https://assets.contentstack.io/v3/assets/bltc6ce635bc4868eb2/"
             "blt5f25277b8918da08/mgm-grand-casino-poker-tournament_schedule.pdf")
MGM_STRUCT = ("https://assets.contentstack.io/v3/assets/bltc6ce635bc4868eb2/"
              "bltb2a45da7e8ee5621/mgm-grand-casino-poker-120_nlh.pdf")
MGM_HUB = "https://www.mgmresorts.com/en/casino/poker.html"

ORL_PAGE = "https://orleans.boydgaming.com/play/poker-room"
ORL_SCHED = ("https://orleans.boydgaming.com/-/media/project/boyd/property/lasvegas/orleans/"
             "pdf/2026_orleans_october_poker_daily_tournaments_schedule_ada.pdf"
             "?rev=6a96aa7ef9fc428bb65c06f9e4d554b0")

SP_PAGE = "https://southpointcasino.com/casino/poker-room"
SP_SCHED = "https://southpointcasino.com/casino/poker-room/daily-tournament-schedule"
SP_HOME = "https://southpointcasino.com/"

HORSESHOE_PAGE = "https://www.caesars.com/horseshoe-las-vegas/casino"
PH_PAGE = "https://www.caesars.com/planet-hollywood/casino"
PARIS_PAGE = "https://www.caesars.com/paris-las-vegas/casino"
MB_PAGE = "https://mandalaybay.mgmresorts.com/en/casino/poker-tables.html"
LUXOR_PAGE = "https://luxor.mgmresorts.com/en/casino/table-games.html"
EXCAL_PAGE = "https://excalibur.mgmresorts.com/en/casino.html"
SAHARA_PAGE = "https://www.saharalasvegas.com/casino"
RW_PAGE = "https://www.rwlasvegas.com/gaming/"
FB_PAGE = "https://www.fontainebleaulasvegas.com/casino/"
WESTGATE_PAGE = "https://www.westgateresorts.com/hotels/nevada/las-vegas/westgate-las-vegas-resort-casino/casino/poker/"
# Session 957764d3: the room links its own "Poker Events" page. Read 2026-11-19: it lists
# cash-game promotions only (Game Starter Special, Instant High Hand Special, Weekly
# Loyalty) and publishes no tournament time, buy-in, guarantee or entry terms.
WESTGATE_EVENTS_PAGE = "https://www.westgateresorts.com/hotels/nevada/las-vegas/westgate-las-vegas-resort-casino/casino/poker/events/"
STRAT_PAGE = "https://thestrat.com/casino"
MIRAGE_PAGE = "https://www.hardrockvegas.com/"


def src(label, url):
    return {"label": label, "url": url}


def rule(value, excerpt, label, url):
    return {"value": value, "excerpt": excerpt,
            "source": src(label, url), "retrieved_on": VERIFIED_ON}


def evt(**kw):
    row = OrderedDict()
    for key in ("id", "room_id", "name", "weekdays", "start", "buy_in_usd", "guarantee_usd",
                "starting_chips", "level_minutes", "late_reg_close", "registration_opens",
                "fee_split", "entry_status", "status_note", "rules", "labels",
                "flags", "sources", "verified_on", "last_checked"):
        row[key] = kw.get(key)
    return row


# --------------------------------------------------------------------------------------
# MGM Grand - the only one of these rooms that publishes a structure sheet in text
# --------------------------------------------------------------------------------------
MGM_120_RULES = {
    "single_entry": rule(
        "no clause permitting a further entry, but extra chips are sold",
        "The structure sheet prints no re-entry, rebuy or add-on clause. It does print a "
        "paid chip advantage: \"Each initial $120 buy-in is allocated as follows: $92 to "
        "Prize Pool, $13 House Fee and a one-time, voluntary gratuity of $11 which grants "
        "players an extra 10,000 chips. $4 will fund Tournament Promotions.\" and \"Players "
        "start with 25,000 tournament chips, including the chips for staff gratuity. "
        "(15,000 + 10,000)\".",
        "MGM Grand $120 NLH structure sheet (linked from the official poker page)", MGM_STRUCT),
    "re_entry": rule(
        "not mentioned",
        "The sheet prints a late-registration clause only: \"All levels are 15 minutes in "
        "length. There will be a break after levels 7 and 15. Registration is open until "
        "Level 8.\" No re-entry clause appears anywhere in the sheet.",
        "MGM Grand $120 NLH structure sheet (linked from the official poker page)", MGM_STRUCT),
    "add_on": rule(
        "not mentioned as an add-on; a paid extra-chip gratuity is printed",
        "\"a one-time, voluntary gratuity of $11 which grants players an extra 10,000 chips\" "
        "and \"***The voluntary staff gratuity will grant players an extra 10,000 chips. This "
        "is an optional gratuity paid to staff and will not be kept by the house***\". The "
        "sheet prints no add-on or rebuy clause.",
        "MGM Grand $120 NLH structure sheet (linked from the official poker page)", MGM_STRUCT),
    "fee": rule(
        "$92 prize pool / $13 house fee / $11 voluntary gratuity / $4 promotions of $120",
        "\"Each initial $120 buy-in is allocated as follows: $92 to Prize Pool, $13 House Fee "
        "and a one-time, voluntary gratuity of $11 which grants players an extra 10,000 chips. "
        "$4 will fund Tournament Promotions.\"",
        "MGM Grand $120 NLH structure sheet (linked from the official poker page)", MGM_STRUCT),
}

MGM_EVENTS = [
    evt(id="mgm-120-am", room_id="mgm-grand", name="$120 No Limit Hold'em (late morning)",
        weekdays=["Mon", "Tue", "Wed", "Thu", "Fri", "Sun"], start="11:10",
        buy_in_usd=120, guarantee_usd=None, starting_chips=25000, level_minutes=15,
        late_reg_close="start of level 8", registration_opens=None,
        fee_split="$92 prize pool, $13 house fee, $11 voluntary gratuity (buys 10,000 extra chips), $4 promotions",
        entry_status="PAID_CHIPS", labels=["paid chip advantage"],
        status_note="No re-entry, rebuy or add-on clause in the sheet read end to end. Kept "
                    "out of the single-entry list because $11 of the $120 buys 10,000 extra "
                    "starting chips on a 15,000 base, so paying more buys a bigger stack.",
        rules=MGM_120_RULES,
        flags=["F62", "F60"],
        sources=[src("Official MGM Grand poker page: daily tournament times", MGM_PAGE),
                 src("MGM Grand weekly tournament schedule (official PDF)", MGM_SCHED),
                 src("MGM Grand $120 NLH structure sheet (official PDF)", MGM_STRUCT)],
        verified_on=VERIFIED_ON, last_checked=VERIFIED_ON),
    evt(id="mgm-120-pm", room_id="mgm-grand", name="$120 No Limit Hold'em (evening)",
        weekdays=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], start="19:10",
        buy_in_usd=120, guarantee_usd=None, starting_chips=25000, level_minutes=15,
        late_reg_close="start of level 8", registration_opens=None,
        fee_split="$92 prize pool, $13 house fee, $11 voluntary gratuity (buys 10,000 extra chips), $4 promotions",
        entry_status="PAID_CHIPS", labels=["paid chip advantage"],
        status_note="Same structure sheet as the 11:10 event. No re-entry clause; the $11 "
                    "gratuity buys 10,000 extra chips.",
        rules=MGM_120_RULES,
        flags=["F62", "F60"],
        sources=[src("Official MGM Grand poker page: daily tournament times", MGM_PAGE),
                 src("MGM Grand weekly tournament schedule (official PDF)", MGM_SCHED),
                 src("MGM Grand $120 NLH structure sheet (official PDF)", MGM_STRUCT)],
        verified_on=VERIFIED_ON, last_checked=VERIFIED_ON),
    evt(id="mgm-120-night", room_id="mgm-grand", name="$120 No Limit Hold'em (late night)",
        weekdays=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], start="23:10",
        buy_in_usd=120, guarantee_usd=None, starting_chips=25000, level_minutes=15,
        late_reg_close="start of level 8", registration_opens=None,
        fee_split="$92 prize pool, $13 house fee, $11 voluntary gratuity (buys 10,000 extra chips), $4 promotions",
        entry_status="PAID_CHIPS", labels=["paid chip advantage"],
        status_note="Same structure sheet as the 11:10 event. No re-entry clause; the $11 "
                    "gratuity buys 10,000 extra chips.",
        rules=MGM_120_RULES,
        flags=["F62", "F60"],
        sources=[src("Official MGM Grand poker page: daily tournament times", MGM_PAGE),
                 src("MGM Grand weekly tournament schedule (official PDF)", MGM_SCHED),
                 src("MGM Grand $120 NLH structure sheet (official PDF)", MGM_STRUCT)],
        verified_on=VERIFIED_ON, last_checked=VERIFIED_ON),
    evt(id="mgm-150-sat", room_id="mgm-grand", name="$150 No Limit Hold'em $2,000 GTD (Saturday)",
        weekdays=["Sat"], start="11:10", buy_in_usd=150, guarantee_usd=2000,
        starting_chips=25000, level_minutes=20, late_reg_close=None, registration_opens=None,
        fee_split=None,
        entry_status="UNV", labels=["guarantee", "no structure sheet published"],
        status_note="The official schedule PDF prints this event with a $2,000 guarantee, "
                    "25K chips and 20-minute levels, but no structure sheet for it is "
                    "published on the poker page, so its entry rule is not verified.",
        rules={
            "single_entry": rule("unverified", "No structure sheet for the $150 Saturday event "
                                 "is published on the official poker page. The page links one "
                                 "structure sheet only, for the $120 NLH.",
                                 "Official MGM Grand poker page", MGM_PAGE),
            "re_entry": rule("unverified", "No structure sheet published for this event.",
                             "Official MGM Grand poker page", MGM_PAGE),
            "add_on": rule("unverified", "No structure sheet published for this event.",
                           "Official MGM Grand poker page", MGM_PAGE),
            "fee": rule("unverified", "The official poker page prints no fee split for this event.",
                        "Official MGM Grand poker page", MGM_PAGE),
        },
        flags=["F63"],
        sources=[src("MGM Grand weekly tournament schedule (official PDF)", MGM_SCHED),
                 src("Official MGM Grand poker page (links only the $120 structure sheet)", MGM_PAGE)],
        verified_on=VERIFIED_ON, last_checked=VERIFIED_ON),
]


def orleans_rules(event_title, level_close, approx_time, withheld, addon=False):
    late = ("\"Late entries and re-entries are available until the start of %s, approximately "
            "%s. If there are alternates waiting, re-entries will be placed at the bottom of "
            "the alternate list.\"" % (level_close, approx_time))
    rules = {
        "single_entry": rule(
            "not single entry - re-entry is printed",
            "The official structure sheet for the %s states: %s" % (event_title, late),
            "2026 Orleans Poker Daily Schedule (official PDF)", ORL_SCHED),
        "re_entry": rule("re-entry allowed", late,
                         "2026 Orleans Poker Daily Schedule (official PDF)", ORL_SCHED),
        "add_on": rule(
            "add-on sold" if addon else "not mentioned",
            ("\"One-Time Add-On: $100 = 25,000 Chips\" and \"Add-on is optional and may be "
             "taken before any hand and prior to the end of level 11 unless registering during "
             "the dinner break. The add-on then must be taken while registering. Players may "
             "only add-on once per entry.\"") if addon else
            "The structure sheet prints no add-on clause; re-entry is the clause it prints.",
            "2026 Orleans Poker Daily Schedule (official PDF)", ORL_SCHED),
        "fee": rule("$%s withheld per entry for admin, staffing and promotional fees" % withheld,
                    "\"From each entry, $%s will be withheld for admin, staffing, and "
                    "promotional fees.\"%s" % (
                        withheld,
                        " \"All add-ons will be added directly to the prize pool with no fees "
                        "withheld.\"" if addon else ""),
                    "2026 Orleans Poker Daily Schedule (official PDF)", ORL_SCHED),
    }
    return rules


ORL = [
    dict(id="orl-sun-special", name="$200 NL Hold'em Sunday Special (RING EVENT)",
         weekdays=["Sun"], start="11:05", buy_in=200, gtd=50000, chips=25000, lmin=30,
         level_close="Level 12", approx="5:30pm", withheld="52", addon=True,
         labels=["re-entry", "add-on", "ring event"]),
    dict(id="orl-am-super", name="$100 NL Hold'em AM Super Stack",
         weekdays=["Mon", "Tue", "Wed", "Thu"], start="11:05", buy_in=100, gtd=4000, chips=25000,
         lmin=20, level_close="Level 9", approx="2:10pm", withheld="23",
         labels=["re-entry"]),
    dict(id="orl-fri-monster", name="$150 NL Hold'em Monster Stack (RING EVENT)",
         weekdays=["Fri"], start="11:05", buy_in=150, gtd=10000, chips=30000, lmin=30,
         level_close="Level 12", approx="5:30pm", withheld="30",
         labels=["re-entry", "ring event"]),
    dict(id="orl-sat-mega", name="$200 NL Hold'em Mega Stack (RING EVENT)",
         weekdays=["Sat"], start="11:05", buy_in=200, gtd=15000, chips=40000, lmin=30,
         level_close="Level 12", approx="5:30pm", withheld="35",
         labels=["re-entry", "ring event"]),
    dict(id="orl-mon-toe", name="$160 T.O.E.",
         weekdays=["Mon"], start="16:05", buy_in=160, gtd=3000, chips=25000, lmin=20,
         level_close="Level 11", approx="7:50pm", withheld="31", labels=["re-entry", "mixed game"]),
    dict(id="orl-tue-torse", name="$160 T.O.R.S.E.",
         weekdays=["Tue"], start="16:05", buy_in=160, gtd=3000, chips=25000, lmin=20,
         level_close="Level 11", approx="7:50pm", withheld="31", labels=["re-entry", "mixed game"]),
    dict(id="orl-wed-drama", name="$160 Drama Mix (Dramaha High / Dramaha 2-7)",
         weekdays=["Wed"], start="16:05", buy_in=160, gtd=4000, chips=25000, lmin=20,
         level_close="Level 11", approx="7:50pm", withheld="31", labels=["re-entry", "mixed game"]),
    dict(id="orl-thu-draw", name="$160 5 Game Draw Mix",
         weekdays=["Thu"], start="16:05", buy_in=160, gtd=3000, chips=25000, lmin=20,
         level_close="Level 11", approx="7:50pm", withheld="31", labels=["re-entry", "mixed game"]),
    dict(id="orl-fri-oe", name="$160 Omaha-8 / Stud-8",
         weekdays=["Fri"], start="16:05", buy_in=160, gtd=4000, chips=25000, lmin=20,
         level_close="Level 11", approx="7:50pm", withheld="31", labels=["re-entry", "mixed game"]),
    dict(id="orl-sat-ttd", name="$160 Triple-Triple Draw",
         weekdays=["Sat"], start="16:05", buy_in=160, gtd=3000, chips=25000, lmin=20,
         level_close="Level 11", approx="7:50pm", withheld="31", labels=["re-entry", "mixed game"]),
    dict(id="orl-sun-bigo", name="$200 Pot-Limit Big-O",
         weekdays=["Sun"], start="18:05", buy_in=200, gtd=4000, chips=25000, lmin=20,
         level_close="Level 11", approx="9:50pm", withheld="35", labels=["re-entry", "mixed game"]),
    dict(id="orl-pm-monster", name="$120 NL Hold'em PM Monster Stack",
         weekdays=["Mon", "Tue", "Wed", "Thu", "Sat"], start="18:05", buy_in=120, gtd=5000,
         chips=30000, lmin=20, level_close="Level 9", approx="9:10pm", withheld="24",
         labels=["re-entry"]),
    dict(id="orl-fri-night", name="$150 NL Hold'em 20K Monster Stack (RING EVENT)",
         weekdays=["Fri"], start="18:05", buy_in=150, gtd=20000, chips=30000, lmin=20,
         level_close="Level 11", approx="9:50pm", withheld="30",
         labels=["re-entry", "ring event"]),
]

ORLEANS_EVENTS = []
for item in ORL:
    ORLEANS_EVENTS.append(evt(
        id=item["id"], room_id="orleans", name=item["name"], weekdays=item["weekdays"],
        start=item["start"], buy_in_usd=item["buy_in"], guarantee_usd=item["gtd"],
        starting_chips=item["chips"], level_minutes=item["lmin"],
        late_reg_close="start of %s (%s)" % (item["level_close"], item["approx"]),
        registration_opens="1 hour before the start",
        fee_split="$%s withheld per entry for admin, staffing and promotions" % item["withheld"],
        entry_status="RE_ADD" if item.get("addon") else "RE",
        labels=item["labels"],
        status_note="The October-named PDF prints re-entry until %s; current validity is unverified.%s" % (
            item["level_close"],
            " It also prints a one-time $100 add-on for 25,000 chips." if item.get("addon") else ""),
        rules=orleans_rules(item["name"], item["level_close"], item["approx"],
                            item["withheld"], item.get("addon", False)),
        flags=["F65"],
        sources=[src("2026 Orleans Poker Daily Schedule (official PDF)", ORL_SCHED),
                 src("Official Orleans poker room page", ORL_PAGE)],
        verified_on=VERIFIED_ON, last_checked=VERIFIED_ON))

# --------------------------------------------------------------------------------------
# Rooms
# --------------------------------------------------------------------------------------
ROOMS = [
    {
        "id": "mgm-grand",
        "name": "MGM Grand",
        "operator": "MGM Resorts International",
        "strip_status": "on the Strip",
        "strip_note": "The official page is the MGM Grand property page; no address statement "
                      "was captured from it in this session.",
        "poker_room_status": "confirmed",
        "poker_room_quote": "\"Known for the deepest $1-$3 No Limit Hold 'Em action in Las "
                            "Vegas, the MGM Grand Poker Room is the Strip's #1 hotspot for "
                            "Texas Hold'em.\" Hours: \"Daily: 24 Hours\". Contact (702) 891-7434.",
        "schedule_status": "published",
        "schedule_note": "The official poker page links a weekly schedule PDF and one structure "
                         "sheet (the $120 NLH). Both were read on 2026-11-17.",
        "sources": [src("Official MGM Grand poker page", MGM_PAGE),
                    src("MGM Grand weekly tournament schedule (official PDF)", MGM_SCHED),
                    src("MGM Grand $120 NLH structure sheet (official PDF)", MGM_STRUCT),
                    src("MGM Resorts official poker hub (lists the properties with poker rooms)", MGM_HUB)],
        "events": MGM_EVENTS,
        "findings": [],
    },
    {
        "id": "orleans",
        "name": "The Orleans Hotel & Casino",
        "operator": "Boyd Gaming",
        "strip_status": "not stated on the official page read",
        "strip_note": "The official poker-room page read in this session prints no address and "
                      "no distance to the Strip, so no walking claim is made here.",
        "poker_room_status": "confirmed",
        "poker_room_quote": "\"this comfortable 35-table room has been enhanced with "
                            "state-of-the-art furnishings and 25 LED TV's\" and \"The Orleans "
                            "Poker Room is open daily 24 hours and features Texas Hold'Em, "
                            "Omaha Hi-Lo and 7-Card Stud.\"",
        "schedule_status": "October-named PDF - current validity unverified",
        "schedule_note": "The linked PDF filename refers to October 2026; its printed grid has no "
                         "validity period. It was read on 2026-11-17 but is not proof of the "
                         "current or November schedule; call the room to confirm.",
        "sources": [src("Official Orleans poker room page", ORL_PAGE),
                    src("2026 Orleans Poker Daily Schedule (official PDF)", ORL_SCHED)],
        "events": ORLEANS_EVENTS,
        "findings": [],
    },
    {
        "id": "westgate",
        "name": "Westgate Las Vegas Resort & Casino",
        "operator": "Westgate Resorts",
        "strip_status": "near the Strip; walking time unverified",
        "strip_note": "No hotel-to-room walking time or Strip proximity is assumed.",
        "poker_room_status": "confirmed",
        "poker_room_quote": "\"Tournaments are available every day (private tournament available "
                            "upon request)\", \"Seven (7) Poker Tables\", \"9 players per a table\", "
                            "\"Hours: Monday - Friday: - 12:00pm - Last Game | Saturday & Sunday: "
                            "10:00am - Last Game\" and \"For more information please contact the "
                            "Poker Room at (702) 732-5223.\" Official page read 2026-11-19.",
        "schedule_status": "daily tournaments confirmed; details unverified",
        "schedule_note": "The official room page confirms that tournaments run every day but gives "
                         "no tournament time, buy-in, guarantee or entry terms, and the official "
                         "\"Poker Events\" page it links lists cash-game promotions only - no "
                         "tournament schedule at all. Ask the room for a current event-specific "
                         "structure. Nothing about a tournament is published here beyond the room's "
                         "own sentence.",
        "sources": [src("Official Westgate poker room page (read 2026-11-19)", WESTGATE_PAGE),
                    src("Official Westgate Poker Events page (read 2026-11-19) - lists cash-game "
                        "promotions only, no tournament schedule", WESTGATE_EVENTS_PAGE)],
        "events": [],
        "findings": [{"text": "The room states that tournaments are available every day and gives "
                               "(702) 732-5223, but no official Westgate page publishes a "
                               "tournament time, buy-in, guarantee or entry rule, so no event row "
                               "is published and nothing here is ranked. Third-party listings of "
                               "Westgate tournaments are not used.",
                      "source": src("Official Westgate poker room page", WESTGATE_PAGE)}],
    },
    {
        "id": "south-point",
        "name": "South Point Hotel, Casino & Spa",
        "operator": "South Point (independent)",
        "strip_status": "off the Strip by its own words",
        "strip_note": "The official home page: \"South Point Hotel, Casino & Spa is a "
                      "full-service Las Vegas resort nestled in the southwest valley, just a "
                      "short drive from the iconic Las Vegas Strip!\"",
        "poker_room_status": "confirmed",
        "poker_room_quote": "\"We feature tournaments daily with aggressive guarantees at "
                            "10:10 am, 2:10 pm, 6:10 pm and 10:10 pm with buy-ins of $120 and "
                            "$300.\" The room is \"24-hour non-smoking\" and \"parking is "
                            "always free\".",
        "schedule_status": "image only - cannot be transcribed",
        "schedule_note": "The official \"Daily Tournament Schedule\" page publishes the schedule "
                         "and all eight rules sheets as images, with no text layer. The page's "
                         "own text gives the four start times and the two buy-in levels but "
                         "does not say which buy-in belongs to which time, so no row is built "
                         "from it.",
        "sources": [src("Official South Point poker room page", SP_PAGE),
                    src("Official South Point daily tournament schedule page (images only)", SP_SCHED),
                    src("Official South Point home page (location wording)", SP_HOME)],
        "events": [],
        "findings": [
            {"text": "The official room page states four daily start times (10:10 am, 2:10 pm, "
                     "6:10 pm, 10:10 pm) and two buy-in levels ($120 and $300) without mapping "
                     "one to the other. No row is built, because a row needs a buy-in and an "
                     "entry rule attached to a time.",
             "source": src("Official South Point poker room page", SP_PAGE)},
            {"text": "The eight rules sheets published on the official schedule page are named "
                     "for $120 and $200 events (NLH, NLH Chip Chop, Omaha-8 or Better, Crazy "
                     "Pineapple Turbo, NLH Turbo Mega Stack, NLH Bounty, Deep Stack, NLH Turbo "
                     "Bounty, all marked Oct2026). No $300 rules sheet is published, although "
                     "the room page advertises a $300 buy-in.",
             "source": src("Official South Point daily tournament schedule page (images only)", SP_SCHED)},
        ],
    },
    {
        "id": "horseshoe",
        "name": "Horseshoe Las Vegas",
        "operator": "Caesars Entertainment",
        "strip_status": "on the Strip",
        "strip_note": "Official Caesars property page for the centre-Strip casino.",
        "poker_room_status": "confirmed",
        "poker_room_quote": "\"The Hall of Fame Poker Room at Horseshoe Las Vegas features 20 "
                            "tables and offers many exciting varieties of live poker ... Test "
                            "your luck with 6 exciting tournament times daily.\"",
        "schedule_status": "not published",
        "schedule_note": "The official page confirms six daily tournaments but prints no start "
                         "time, buy-in, guarantee or structure, and no schedule PDF was found "
                         "on caesars.com on 2026-11-17. Third-party sites publish times and "
                         "buy-ins for these events; they are not official and are not used here.",
        "sources": [src("Official Horseshoe Las Vegas casino page", HORSESHOE_PAGE)],
        "events": [],
        "findings": [
            {"text": "Six daily tournaments are confirmed by the official page, but nothing "
                     "else about them is published there. The URLs tried on 2026-11-17 "
                     "(/casino/poker-room.html and /casino/poker) both resolve to the same "
                     "casino page, which carries no schedule.",
             "source": src("Official Horseshoe Las Vegas casino page", HORSESHOE_PAGE)},
        ],
    },
    {
        "id": "planet-hollywood",
        "name": "Planet Hollywood",
        "operator": "Caesars Entertainment",
        "strip_status": "on the Strip",
        "strip_note": "Official Caesars property page.",
        "poker_room_status": "confirmed",
        "poker_room_quote": "\"23 Live Poker Tables\" and \"Planet Hollywood Casino takes up a "
                            "notch with an exciting gaming floor, new live action poker room "
                            "and poolside blackjack.\"",
        "schedule_status": "not published",
        "schedule_note": "The official casino page confirms a live poker room and table count "
                         "but publishes no tournament schedule, buy-in or structure.",
        "sources": [src("Official Planet Hollywood casino page", PH_PAGE)],
        "events": [],
        "findings": [
            {"text": "Another session (88793bf4, PR #45) records a press report that this poker "
                     "room closed (Las Vegas Review-Journal, 28 January 2026). The official page "
                     "read here on 2026-11-17 still advertises it. A press report is not an "
                     "official source, so nothing is changed on the strength of it; the conflict "
                     "is flagged as F74 for a human to check with the property.",
             "source": src("Official Planet Hollywood casino page", PH_PAGE)},
        ],
    },
    {
        "id": "mandalay-bay",
        "name": "Mandalay Bay",
        "operator": "MGM Resorts International",
        "strip_status": "on the Strip",
        "strip_note": "Official MGM Resorts property page.",
        "poker_room_status": "confirmed",
        "poker_room_quote": "\"The cards are dealt, and the bets are in. Get set for hand after "
                            "hand of classic poker action.\" Hours: \"Wednesday - Monday: "
                            "10:00 AM - 4:00 AM\", \"Tuesday: Closed\". Price range \"$60 - "
                            "$1,000\".",
        "schedule_status": "not published",
        "schedule_note": "The official poker page publishes hours, a price range and a group "
                         "booking number, but no recurring tournament schedule. It says: \"To "
                         "set up a Poker Tournament as a group, please contact 702.632.7790.\"",
        "sources": [src("Official Mandalay Bay poker page", MB_PAGE)],
        "events": [],
        "findings": [],
    },
    {
        "id": "paris",
        "name": "Paris Las Vegas",
        "operator": "Caesars Entertainment",
        "strip_status": "on the Strip",
        "strip_note": "Official Caesars property page.",
        "poker_room_status": "none published",
        "poker_room_quote": "The official casino page lists \"Poker Derivative Table Games\" "
                            "(Face Up Pai Gow, Ultimate Texas Hold'Em, Let It Ride, Three Card "
                            "Poker, Mississippi Stud, I Luv Suits, Crazy 4 Poker) and no live "
                            "poker room.",
        "schedule_status": "not published",
        "schedule_note": "No live poker room is published on the official casino page, so there "
                         "is no tournament schedule to look for.",
        "sources": [src("Official Paris Las Vegas casino page", PARIS_PAGE)],
        "events": [],
        "findings": [],
    },
    {
        "id": "luxor",
        "name": "Luxor",
        "operator": "MGM Resorts International",
        "strip_status": "on the Strip",
        "strip_note": "Official MGM Resorts property page.",
        "poker_room_status": "none published",
        "poker_room_quote": "The official table-games page lists craps, roulette, blackjack, "
                            "3 Card Poker, mini baccarat, Free Bet Blackjack and Ultimate "
                            "Texas Hold'em, and no live poker room.",
        "schedule_status": "not published",
        "schedule_note": "No live poker room is published on the official page. See flag F71: "
                         "the MGM Resorts poker hub links this page under \"Luxor Poker "
                         "Tournaments\".",
        "sources": [src("Official Luxor table games page", LUXOR_PAGE),
                    src("MGM Resorts official poker hub (links Luxor here)", MGM_HUB)],
        "events": [],
        "findings": [],
    },
    {
        "id": "excalibur",
        "name": "Excalibur",
        "operator": "MGM Resorts International",
        "strip_status": "on the Strip",
        "strip_note": "Official MGM Resorts property page.",
        "poker_room_status": "none published",
        "poker_room_quote": "The official casino page lists Slots, $5 Live Blackjack, Table "
                            "Games and the BetMGM Sportsbook, and no poker room.",
        "schedule_status": "not published",
        "schedule_note": "No live poker room is published on the official casino page. See flag "
                         "F71: the MGM Resorts poker hub links excalibur.mgmresorts.com/en/"
                         "casino/poker-room.html, which redirects to this page.",
        "sources": [src("Official Excalibur casino page", EXCAL_PAGE),
                    src("MGM Resorts official poker hub (links Excalibur here)", MGM_HUB)],
        "events": [],
        "findings": [],
    },
    {
        "id": "sahara",
        "name": "SAHARA Las Vegas",
        "operator": "SAHARA Las Vegas (independent)",
        "strip_status": "on the Strip",
        "strip_note": "Official property page.",
        "poker_room_status": "none published",
        "poker_room_quote": "\"SAHARA Las Vegas delivers one of the most unique gaming "
                            "destinations on the Strip ... nearly 60,000 square foot casino ... "
                            "Over 600 slot machines ... Over 50 table games.\" No poker room is "
                            "listed.",
        "schedule_status": "not published",
        "schedule_note": "No live poker room is published on the official casino page.",
        "sources": [src("Official SAHARA Las Vegas casino page", SAHARA_PAGE)],
        "events": [],
        "findings": [],
    },
    {
        "id": "resorts-world",
        "name": "Resorts World Las Vegas",
        "operator": "Genting",
        "strip_status": "on the Strip",
        "strip_note": "Official property page.",
        "poker_room_status": "none published",
        "poker_room_quote": "The official gaming page lists High Limit, Slots, Table Games and "
                            "the Sky Casino, and no poker room. Its casino-events page lists "
                            "slot and free-play promotions only.",
        "schedule_status": "not published",
        "schedule_note": "No live poker room is published on the official gaming page or the "
                         "official casino-events page.",
        "sources": [src("Official Resorts World gaming page", RW_PAGE),
                    src("Official Resorts World casino events page",
                        "https://www.rwlasvegas.com/gaming/casino-events/")],
        "events": [],
        "findings": [],
    },
    {
        "id": "fontainebleau",
        "name": "Fontainebleau Las Vegas",
        "operator": "Fontainebleau Development",
        "strip_status": "on the Strip",
        "strip_note": "Official property page.",
        "poker_room_status": "none published",
        "poker_room_quote": "The official casino page lists table games, \"high-limit slots and "
                            "poker machines\" (electronic video poker) in the High Limit "
                            "enclave, and the race and sports book. No live poker room is listed.",
        "schedule_status": "not published",
        "schedule_note": "No live poker room is published on the official casino page.",
        "sources": [src("Official Fontainebleau casino page", FB_PAGE)],
        "events": [],
        "findings": [],
    },
    {
        "id": "the-strat",
        "name": "The STRAT Hotel, Casino & Tower",
        "operator": "Golden Entertainment",
        "strip_status": "north Strip",
        "strip_note": "Official property page.",
        "poker_room_status": "none published",
        "poker_room_quote": "\"our casino has 784 machines and 31 tables offering high-energy "
                            "games from craps and blackjack to baccarat and roulette.\" The "
                            "official casino page lists Slots, Table Games and the William Hill "
                            "Sports Book only.",
        "schedule_status": "not published",
        "schedule_note": "No live poker room is published on the official casino page. "
                         "thestrat.com/casino/poker returns the official 404 page.",
        "sources": [src("Official STRAT casino page", STRAT_PAGE)],
        "events": [],
        "findings": [],
    },
    {
        "id": "mirage",
        "name": "The Mirage (rebranding to Hard Rock Las Vegas)",
        "operator": "MGM Resorts International / Hard Rock International",
        "strip_status": "on the Strip",
        "strip_note": "Official property page reached from the MGM Resorts Mirage URL.",
        "poker_room_status": "none published",
        "poker_room_quote": "mirage.mgmresorts.com/en/casino/poker-tables.html now resolves to "
                            "the Hard Rock Las Vegas page: \"Coming Soon to the Las Vegas "
                            "Strip\". No poker room or schedule is published.",
        "schedule_status": "not published",
        "schedule_note": "The property page reached from the Mirage poker URL is a "
                         "coming-soon page for the rebrand, with no poker room.",
        "sources": [src("Hard Rock Las Vegas official page (reached from the Mirage poker URL)",
                        MIRAGE_PAGE)],
        "events": [],
        "findings": [],
    },
]

FLAGS = [
    ("F60", "Start times conflict inside one operator's own sources",
     "The official MGM Grand poker page prints \"Daily Texas Hold'em Tournaments 11:00am, "
     "7:00pm and 11:00pm\". The official schedule PDF linked from that same page prints "
     "11:10am, 7:10pm and 11:10pm.",
     "Both times are kept. The rows use the schedule PDF's times, because the PDF is the "
     "document that also prints the buy-in, chips and level length for each slot. The "
     "page's times are quoted on the row.",
     MGM_PAGE),
    ("F61", "The weekly schedule PDF carries a month in its title",
     "The PDF linked as \"Weekly Schedule\" prints the heading \"MGM Grand August Tournament "
     "Schedule\" and a grid of weekday columns with no dates and no year.",
     "The grid is stored as a recurring weekday schedule, not as dated rows. Which month it "
     "describes cannot be read from the document, so no date range is claimed.",
     MGM_SCHED),
    ("F62", "Extra chips can be bought inside the buy-in",
     "\"Each initial $120 buy-in is allocated as follows: $92 to Prize Pool, $13 House Fee and "
     "a one-time, voluntary gratuity of $11 which grants players an extra 10,000 chips. $4 will "
     "fund Tournament Promotions.\" and \"Players start with 25,000 tournament chips, including "
     "the chips for staff gratuity. (15,000 + 10,000)\".",
     "Paying $11 more takes a starting stack from 15,000 to 25,000 chips, so spending more buys "
     "an in-game advantage. These events are kept out of the single-entry list and shown in the "
     "separate section, which is what the brief asks for with events where money buys an "
     "advantage.",
     MGM_STRUCT),
    ("F63", "The Saturday $150 event has no published structure sheet",
     "The official poker page links one structure sheet only, the $120 NLH. The schedule PDF "
     "prints a Saturday 11:10am \"$150 NLH - $2,000\" with 25K chips and 20-minute levels.",
     "The row keeps the buy-in, guarantee, chips and level length printed on the schedule PDF. "
     "Its entry rule, fee split and late-registration close stay blank and unverified.",
     MGM_SCHED),
    ("F64", "The two MGM PDFs are hosted off the property domain",
     "Both PDFs are served from assets.contentstack.io, not from mgmgrand.mgmresorts.com. They "
     "are reached only through links on the official poker page.",
     "They are cited as \"linked from the official page\", the same treatment the site already "
     "gives the Bellagio flyers (F40). No value is taken from a PDF that the official page does "
     "not link.",
     MGM_PAGE),
    ("F65", "The Orleans schedule PDF's file name and its printed period do not agree",
     "The file is named 2026_orleans_october_poker_daily_tournaments_schedule_ada.pdf, while "
     "the official page links it as \"2026 Orleans Poker Daily Schedule\". Nothing inside the "
     "PDF prints a month, a year or a date range.",
     "The October-named PDF has an unconfirmed validity period and is "
     "not proof that the grid is current in November. Contact the room before relying on it.",
     ORL_SCHED),
    ("F66", "The Orleans PDF points at a dead URL",
     "The PDF's own footer prints: \"For tournament structures or questions, contact a Poker "
     "Room staff member at 702-365-7150 or go to our website: "
     "https://www.orleanscasino.com/play/casino-games/poker-room\". That URL returns \"Not "
     "Found\" on 2026-11-17.",
     "The live official page used instead is https://orleans.boydgaming.com/play/poker-room, "
     "which is where the PDF itself is linked from.",
     ORL_PAGE),
    ("F67", "The October-named Orleans PDF describes re-entry",
     "Each of the thirteen structure sheets in the linked PDF prints the same clause: "
     "\"Late entries and re-entries are available until the start of Level ...\". The Sunday "
     "Special additionally prints \"One-Time Add-On: $100 = 25,000 Chips\".",
     "All thirteen Orleans rows are stored with a re-entry rule and kept out of the "
     "single-entry list.",
     ORL_SCHED),
    ("F68", "South Point publishes its schedule and rules as images only",
     "The official \"Daily Tournament Schedule\" page carries one schedule image and sixteen "
     "rules-sheet images with no text layer. The eight named rules sheets are $120 and $200 "
     "events; the poker-room page advertises buy-ins of \"$120 and $300\".",
     "No South Point row is built. A row needs a buy-in and an entry rule tied to a start time, "
     "and neither can be read from an image here. The official text that does exist is quoted "
     "on this page instead.",
     SP_SCHED),
    ("F69", "Horseshoe confirms six daily tournaments and publishes nothing else about them",
     "\"Test your luck with 6 exciting tournament times daily.\" No time, buy-in, guarantee or "
     "structure appears on the official page, and no schedule PDF was found on caesars.com.",
     "Horseshoe is listed as a room with tournaments and no published schedule. Third-party "
     "schedules for it were found and deliberately not used.",
     HORSESHOE_PAGE),
    ("F70", "No live poker room is published for Paris, Luxor, Excalibur, SAHARA, Resorts "
     "World, Fontainebleau, The STRAT or the Mirage site",
     "Each property's own casino page was read on 2026-11-17 and lists no live poker room. "
     "Absence from an official page is weaker evidence than a printed statement, so these are "
     "recorded as \"no poker room published\", not as \"no poker room\".",
     "They are listed in the survey with the page read, and no rows are invented for them.",
     PARIS_PAGE),
    ("F71", "The MGM poker hub links two properties to pages that publish no poker room",
     "The hub lists \"Luxor Poker Tournaments\" with a link to "
     "luxor.mgmresorts.com/en/casino/table-games.html and \"Excalibur Poker Tournaments\" with "
     "a link to excalibur.mgmresorts.com/en/casino/poker-room.html, which redirects to "
     "excalibur.mgmresorts.com/en/casino.html. Neither page lists a live poker room.",
     "Both properties are recorded as \"no poker room published\", with the hub link and the "
     "page it resolves to.",
     MGM_HUB),
    ("F72", "No walking record exists for these rooms yet",
     "The site's walking table covers twelve hotel-to-poker-room pairs, all of them to the "
     "Venetian and Wynn poker rooms. No routed walking time was produced on 2026-11-17 from any "
     "hotel to MGM Grand, the Orleans or South Point.",
     "Walking cells for these rooms are blank and flagged. Producing them is logged as a "
     "request for the integration session in COORDINATION.md; none is estimated here.",
     MB_PAGE),
    ("F74", "Planet Hollywood: the official page still advertises a live poker room, while a "
     "press report says it closed",
     "The official Planet Hollywood casino page, read on 2026-11-17, prints \"23 Live Poker "
     "Tables\" and \"new live action poker room\". Session 88793bf4's PR #45 records a press "
     "report that the room closed (Las Vegas Review-Journal, 28 January 2026) and the same for "
     "Resorts World (Casino.org, 13 March 2026). Neither closure is confirmed on an official "
     "source, and this page does not treat a press report as a value.",
     "Planet Hollywood is recorded exactly as the official page prints it: a poker room with 23 "
     "tables and no tournament schedule. The conflict is flagged here instead of being resolved, "
     "because closing a room is not something this site can confirm from an operator page. Check "
     "with the property before planning around it.",
     PH_PAGE),
]

STATUS_CHIPS = {
    "SE": ("ok", "Single entry - affirmatively confirmed for this event"),
    "RE": ("bad", "Re-entry allowed"),
    "ADD": ("bad", "Add-on sold"),
    "RE_ADD": ("bad", "Re-entry and add-on"),
    "PAID_CHIPS": ("warn", "Extra spend buys chips"),
    "UNV": ("warn", "Unverified - no structure sheet published"),
}

METHOD = (
    "The original survey was checked against official websites on 2026-11-17; the added Westgate "
    "record was checked on 2026-11-19. A row "
    "is published only where an official page or an official PDF prints the value. Where the "
    "official source publishes a schedule as images with no text, nothing is transcribed and the "
    "gap is recorded instead. Third-party schedules were found for several of these rooms and "
    "were not used. \"No poker room published\" means the property's own casino page lists none; "
    "it is not a statement that the room does not exist."
)


def esc(value):
    return html.escape("" if value is None else str(value), quote=False)


def money(value):
    if value is None:
        return '<span class="muted">blank</span>'
    number = float(value)
    if number == int(number):
        return "$%s" % format(int(number), ",d")
    return "$%s" % format(number, ",.2f")


def links(sources):
    return ", ".join('<a href="%s">%s</a>' % (esc(s.get("url")), esc(s.get("label")))
                     for s in sources if isinstance(s, dict) and s.get("url"))


def chip(status):
    kind, text = STATUS_CHIPS.get(status, ("warn", status))
    return '<span class="chip %s">%s</span>' % (kind, esc(text))


def build_dataset():
    events = []
    for room in ROOMS:
        for event in room.get("events", []):
            events.append(event)
    return OrderedDict([
        ("verified_on", VERIFIED_ON),
        ("method", METHOD),
        ("note", "Recurring daily and weekly events at Las Vegas poker rooms other than the "
                 "Venetian and Wynn. These rooms print weekday schedules, not calendar dates, "
                 "so the rows carry weekdays and no date. They are kept in this file and out of "
                 "data/tournaments.json, whose rows are dated."),
        ("rooms", ROOMS),
        ("events", events),
        ("flags", [OrderedDict([("id", f[0]), ("title", f[1]), ("found", f[2]),
                                ("handling", f[3]), ("source", f[4])]) for f in FLAGS]),
        ("counts", OrderedDict([
            ("rooms_surveyed", len(ROOMS)),
            ("rooms_with_poker_room_published", len([r for r in ROOMS if r["poker_room_status"] == "confirmed"])),
            ("rooms_with_a_schedule_published", len([r for r in ROOMS if r["schedule_status"] == "published"])),
            ("rooms_with_no_poker_room_published", len([r for r in ROOMS if r["poker_room_status"] == "none published"])),
            ("events", len(events)),
            ("events_single_entry", len([e for e in events if e["entry_status"] == "SE"])),
            ("events_re_entry", len([e for e in events if e["entry_status"] in ("RE", "RE_ADD")])),
            ("events_paid_chips", len([e for e in events if e["entry_status"] == "PAID_CHIPS"])),
            ("events_unverified", len([e for e in events if e["entry_status"] == "UNV"])),
        ])),
    ])


# --------------------------------------------------------------------------------------
# Page generation
# --------------------------------------------------------------------------------------
def windows_section():
    """Show historical stay observations without ranking unlike dates/rooms."""
    try:
        with open(os.path.join(ROOT, "data", "schedule.json"), encoding="utf-8") as fh:
            schedule = json.load(fh)
        with open(os.path.join(ROOT, "data", "rates.json"), encoding="utf-8") as fh:
            rates = json.load(fh)
    except (OSError, ValueError):
        return '<p class="small muted">The dated quote log is unavailable.</p>'
    out = ['<p class="small">These are historical checkout observations for different dates '
           'and rooms, not like-for-like hotel offers or current prices. Confirm availability, '
           'cancellation terms, parking and all other charges before booking. An event count is '
           'not a playable itinerary; entry rules, overlaps and travel must be checked.</p>',
           '<table><thead><tr><th>Dated stay and occupancy</th><th>Nights</th>'
           '<th>Historical checkout / night</th><th>Historical checkout total</th>'
           '<th>Strictly confirmed entry options</th><th>Unverified sheet-review candidates</th>'
           '<th>Official source and retrieval date</th></tr></thead><tbody>']
    for q in sorted(rates.get("entries", []), key=lambda r: r.get("arrival", "")):
        arrival, departure = q.get("arrival"), q.get("departure")
        if not arrival or not departure:
            continue
        events = [e for day in schedule.get("days", []) if arrival <= day.get("date", "") < departure
                  for e in day.get("events", [])]
        strict = sum(e.get("entry_status") == "SE" for e in events)
        candidate = sum(e.get("entry_status") == "CAND" for e in events)
        out.append('<tr><td><strong>%s &rarr; %s</strong><br><span class="small">%s · %s · %s</span></td>'
                   '<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>'
                   '<td><a href="%s">official booking engine</a><br><span class="small">quote read %s</span></td></tr>'
                   % (esc(arrival), esc(departure), esc(q.get("property")), esc(q.get("room")),
                      esc(q.get("occupancy")), esc(q.get("nights")), money(q.get("true_cost_per_night_usd")),
                      money(q.get("checkout_total_usd")), strict, candidate, esc(q.get("source")),
                      esc(q.get("retrieved_on") or q.get("logged_on"))))
    out.append('</tbody></table>')
    return "\n".join(out)


def render_page(data):
    with open(os.path.join(ROOT, "assets", "style.css"), encoding="utf-8") as fh:
        css = fh.read()
    with open(os.path.join(ROOT, "assets", "app.js"), encoding="utf-8") as fh:
        js = fh.read()
    counts = data["counts"]

    head = """
<h1>Other Las Vegas poker rooms</h1>
<p class="lead">A survey of additional Las Vegas poker rooms using operator sources, mostly read on
2026-11-17; Westgate was added on 2026-11-19. Schedules and rates change. Blank means unverified.</p>
<div class="card callout"><strong>Method.</strong> %s</div>
<h2>Headline</h2>
<ul>
  <li><strong>MGM Grand's $120 structure sheet offers extra chips for an optional $11 gratuity.</strong>
      The sheet states late registration until Level 8 but does not affirm an event-wide entry
      limit. The paid 10,000-chip advantage on a 15,000 base excludes it from the strict
      single-entry shortlist regardless of the re-entry rule (F62).</li>
  <li><strong>The October-named Orleans PDF describes re-entry.</strong> Its thirteen sheets also
      include a Sunday $100 add-on, but the PDF does not establish whether the grid is current.
      Confirm the schedule and terms with the room before attending (F65, F67).</li>
  <li><strong>Westgate confirms daily tournaments</strong>, but its room page does not specify the
      rumored $70 event's time or entry policy. Call (702) 732-5223 for current terms.</li>
  <li><strong>South Point and Horseshoe run daily tournaments but publish nothing readable about
      them.</strong> South Point's schedule and rules sheets are images (F68); Horseshoe's page
      confirms six daily tournaments and prints no time, buy-in or structure (F69).</li>
  <li><strong>Eight property pages did not list a live poker room</strong> when checked (F70).
      That is not proof that a room does not exist; verify directly before visiting.</li>
  <li><strong>No walking time is published for these rooms</strong>, so none is stated here (F72).</li>
</ul>
<div class="grid">
  <div class="card tile"><h3>%s</h3><p>rooms surveyed on operator sites, 2026-11-17 to 2026-11-19</p></div>
  <div class="card tile"><h3>%s</h3><p>publish a live poker room</p></div>
  <div class="card tile"><h3>%s</h3><p>publish a readable tournament schedule</p></div>
  <div class="card tile"><h3>%s</h3><p>recurring event rows stored, all with an official source</p></div>
  <div class="card tile"><h3>%s</h3><p>of those rows are single entry</p></div>
</div>
""" % (esc(METHOD), esc(counts["rooms_surveyed"]), esc(counts["rooms_with_poker_room_published"]),
       esc(counts["rooms_with_a_schedule_published"]), esc(counts["events"]),
       esc(counts["events_single_entry"]))

    # Rooms surveyed.
    room_rows = ['<table><thead><tr><th>Room</th><th>Poker room on the official page</th>'
                 '<th>Tournament schedule</th><th>What the official page says</th>'
                 '<th>Source</th></tr></thead><tbody>']
    for room in ROOMS:
        status = ("<strong>Poker room published</strong>" if room["poker_room_status"] == "confirmed"
                  else "No poker room published")
        schedule = {"published": '<span class="chip ok">Schedule published</span>',
                    "not published": '<span class="chip warn">No schedule published</span>'}.get(
                        room["schedule_status"], '<span class="chip bad">%s</span>' % esc(room["schedule_status"]))
        room_rows.append(
            "<tr><td><strong>%s</strong><br><span class=\"small\">%s · %s</span></td>"
            "<td>%s</td><td>%s<br><span class=\"small\">%s</span></td>"
            "<td><span class=\"small\">%s</span></td><td><span class=\"small\">%s</span></td></tr>"
            % (esc(room["name"]), esc(room["operator"]), esc(room["strip_status"]), status,
               schedule, esc(room["schedule_note"]), esc(room["poker_room_quote"]),
               links(room["sources"])))
    room_rows.append("</tbody></table>")

    # Event rows.
    room_names = {r["id"]: r["name"] for r in ROOMS}
    ev_rows = ['<table><thead><tr><th>Event</th><th>Room</th><th>Days</th><th>Start</th>'
               '<th>Buy-in</th><th>Guarantee</th><th>Chips / levels</th><th>Late reg closes</th>'
               '<th>Entry rule</th><th>Rule excerpt (official)</th><th>Source</th>'
               '</tr></thead><tbody>']
    for event in data["events"]:
        excerpt = ""
        rules = event.get("rules") or {}
        for key in ("re_entry", "add_on", "single_entry"):
            if key in rules and rules[key].get("excerpt"):
                excerpt = rules[key]["excerpt"]
                break
        ev_rows.append(
            "<tr><td><strong>%s</strong>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>"
            "<td>%s</td><td>%s<br><span class=\"small\">%s min</span></td><td>%s</td>"
            "<td>%s<br><span class=\"small\">%s</span></td>"
            "<td><span class=\"small\">%s</span></td><td><span class=\"small\">%s</span></td></tr>"
            % (esc(event["name"]),
               "".join('<br><span class="chip info">%s</span>' % esc(x) for x in (event.get("labels") or [])),
               esc(room_names.get(event["room_id"], event["room_id"])),
               esc(", ".join(event.get("weekdays") or [])),
               esc(event.get("start")), money(event.get("buy_in_usd")),
               money(event.get("guarantee_usd")),
               esc(format(event["starting_chips"], ",d") if event.get("starting_chips") else "blank"),
               esc(event.get("level_minutes")), esc(event.get("late_reg_close") or "blank"),
               chip(event.get("entry_status")), esc(event.get("status_note") or ""),
               esc(excerpt), links(event.get("sources") or [])))
    ev_rows.append("</tbody></table>")

    # Fee splits (a second, narrower table so the excerpt column stays readable).
    fee_rows = ['<table><thead><tr><th>Event</th><th>Registration opens</th><th>Fee split '
                '(official wording)</th><th>Starting stack</th><th>Source</th></tr></thead><tbody>']
    for event in data["events"]:
        fee_rule = (event.get("rules") or {}).get("fee") or {}
        fee_rows.append(
            "<tr><td><strong>%s</strong></td><td>%s</td><td><span class=\"small\">%s</span></td>"
            "<td>%s</td><td><span class=\"small\">%s</span></td></tr>"
            % (esc(event["name"]), esc(event.get("registration_opens") or "blank"),
               esc(event.get("fee_split") or fee_rule.get("excerpt") or "blank"),
               esc(format(event["starting_chips"], ",d") if event.get("starting_chips") else "blank"),
               links(event.get("sources") or [])))
    fee_rows.append("</tbody></table>")

    # Findings from rooms with no readable schedule.
    findings = ['<table><thead><tr><th>Room</th><th>Finding</th><th>Source</th></tr></thead><tbody>']
    for room in ROOMS:
        for finding in room.get("findings", []):
            findings.append("<tr><td><strong>%s</strong></td><td>%s</td><td><span class=\"small\">%s</span></td></tr>"
                            % (esc(room["name"]), esc(finding["text"]), links([finding["source"]])))
    findings.append("</tbody></table>")

    # Flags.
    flag_rows = ['<table><thead><tr><th>#</th><th>Irregularity</th><th>What the official source '
                 'prints</th><th>How it is handled</th><th>Source</th></tr></thead><tbody>']
    for flag in data["flags"]:
        flag_rows.append(
            "<tr id=\"%s\"><td><strong>%s</strong></td><td>%s</td>"
            "<td><span class=\"small\">%s</span></td><td><span class=\"small\">%s</span></td>"
            "<td><a href=\"%s\">official source</a></td></tr>"
            % (esc(flag["id"].lower()), esc(flag["id"]), esc(flag["title"]), esc(flag["found"]),
               esc(flag["handling"]), esc(flag["source"])))
    flag_rows.append("</tbody></table>")

    # Everything after the lead sits inside #content, which is the container the headless
    # page smoke test looks for on every page.
    body = "\n".join([
        head,
        "<div id=\"content\">",
        "<h2 id=\"rooms\">1. Rooms surveyed</h2>", "\n".join(room_rows),
        "<h2 id=\"events\">2. Recurring events published by these rooms</h2>",
        "<p class=\"small\">These rooms print weekday schedules, not calendar dates, so the rows "
        "carry weekdays. They are not merged into the dated tables, which belong to the Venetian "
        "and Wynn series.</p>", "\n".join(ev_rows),
        "<h2 id=\"fees\">3. Registration and fee splits</h2>", "\n".join(fee_rows),
        "<h2 id=\"gaps\">4. Findings from rooms with no readable schedule</h2>", "\n".join(findings),
        "<h2 id=\"flags\">5. Irregularities and blank values (F60-F74)</h2>", "\n".join(flag_rows),
        "<h2 id=\"windows\">6. Historical dated stay observations</h2>",
        "<p class=\"small\">Different dates and rooms are not like-for-like. Nothing is forecast.</p>", windows_section(),
        "<h2 id=\"next\">7. What is still missing</h2>",
        "<ul>"
        "<li><strong>Walking times.</strong> No routed walking record exists yet for any of these "
        "rooms, so no hotel can be ranked against the 30-minute rule for them. Logged as a request "
        "in COORDINATION.md (F72).</li>"
        "<li><strong>South Point and Horseshoe schedules.</strong> Both need a text-readable "
        "official schedule or a call to the room (South Point is on its own site; the Horseshoe "
        "page publishes no number for the poker room).</li>"
        "<li><strong>MGM Grand Saturday $150.</strong> No structure sheet is published, so its "
        "entry rule is still unverified (F63).</li>"
        "<li><strong>The Orleans period.</strong> The filename references October 2026 but the "
        "grid itself has no validity dates; confirm whether it is current (F65).</li>"
        "</ul>",
        "<p class=\"small\"><a href=\"venues.html\">Back to the venue list →</a></p>",
        "</div>",
    ])

    return ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            "<title>Other Las Vegas poker rooms · Las Vegas Strip Poker Plan</title>\n<style>\n%s\n</style>\n"
            "</head>\n<body data-page=\"otherRooms\">\n<div id=\"site-header\"></div>\n<main>\n%s\n</main>\n"
            "<footer id=\"site-footer\"></footer>\n<script>\n%s\n</script>\n</body>\n</html>\n"
            % (css, body, js))


def main():
    data = build_dataset()
    with open(os.path.join(ROOT, "data", "other_rooms.json"), "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    page = render_page(data)
    with open(os.path.join(ROOT, "pages", "other-rooms.html"), "w", encoding="utf-8") as fh:
        fh.write(page)
    counts = data["counts"]
    print("wrote data/other_rooms.json and pages/other-rooms.html")
    print("   rooms surveyed %s (%s with a poker room published, %s with a readable schedule)"
          % (counts["rooms_surveyed"], counts["rooms_with_poker_room_published"],
             counts["rooms_with_a_schedule_published"]))
    print("   events %s (SE %s, re-entry %s, paid chips %s, unverified %s)"
          % (counts["events"], counts["events_single_entry"], counts["events_re_entry"],
             counts["events_paid_chips"], counts["events_unverified"]))


if __name__ == "__main__":
    main()
