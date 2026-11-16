"""Verified source data for the Las Vegas Strip poker project.

Every row below was transcribed from an official source fetched on 2026-11-16.
Each row carries the URL(s) it came from (see SOURCES). Values that could not be
confirmed from an official source are left as None and listed under FLAGS.

Source key:
  VEN_SCHED  = https://www.venetianlasvegas.com/resort/casino/poker/deepstack-extravaganza-poker-tournament/dse-nov-2026.html
  VEN_S{n}   = https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/deepstack/2026/structures/dse_nov_2026-structure_{n}.pdf
"""

FETCHED = "2026-11-16"

VEN_SCHED = ("https://www.venetianlasvegas.com/resort/casino/poker/"
             "deepstack-extravaganza-poker-tournament/dse-nov-2026.html")
VEN_STRUCT = ("https://www.venetianlasvegas.com/content/dam/vlvweb/casino/poker/"
              "deepstack/2026/structures/dse_nov_2026-structure_{n}.pdf")


def vs(n):
    return VEN_STRUCT.format(n=n)


WYNN_WPT_SCHED = ("https://cdn.wynnresorts.com/image/upload/v1757097329/"
                  "visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Schedule.pdf")
WYNN_WPT_STRUCT = ("https://cdn.wynnresorts.com/image/upload/v1750864036/"
                   "visitwynn_pdfs_files/Poker/WPT/WPT_World_Championship_Structures.pdf")
WYNN_POSTER = ("https://cdn.wynnresorts.com/image/upload/v1752011166/"
               "visitwynn_pdfs_files/Poker/Daily%20Tournaments/poker-daily-tournament-poster.pdf")
WYNN_DAILY_STRUCT = ("https://cdn.wynnresorts.com/image/upload/v1752011191/"
                     "visitwynn_pdfs_files/Poker/Daily%20Tournaments/Poker-All_Daily_Structures.pdf")
WYNN_POKER_PAGE = "https://www.wynnlasvegas.com/casino/poker"

BELL_POKER_PAGE = "https://bellagio.mgmresorts.com/en/casino/poker.html"
BELL_FRI = ("https://assets.contentstack.io/v3/assets/bltc6ce635bc4868eb2/blt9cf95b0e60ec253e/"
            "6af491a3a9851d75c40be840/mgm-bellagio-poker-fridays-$600-nlh.pdf")
BELL_SAT = ("https://assets.contentstack.io/v3/assets/bltc6ce635bc4868eb2/blt6d47974bf5a7d9b6/"
            "6af491a391a6e8e4230c9e07/mgm-bellagio-poker-saturdays-$1000-nlh.pdf")
BELL_SUN = ("https://assets.contentstack.io/v3/assets/bltc6ce635bc4868eb2/blt07fcf1244a6da661/"
            "6af491a339e2b4f6b76a86ad/mgm-bellagio-poker-sundays-$400-horse.pdf")

VEN_HOTEL_TERMS = "https://www.venetianlasvegas.com/legal/hotel-terms-and-conditions.html"
VEN_SUITE_RATES = "https://www.venetianlasvegas.com/resort/casino/poker/suite-rates.html"
VEN_POKER_PAGE = "https://www.venetianlasvegas.com/resort/casino/poker.html"
WYNN_TERMS_OFFER = "https://www.wynnlasvegas.com/terms-and-conditions/848654"
WYNN_TERMS_OFFER2 = "https://www.wynnlasvegas.com/terms-and-conditions/848991"
WYNN_TERMS_SUITE = "https://www.wynnlasvegas.com/terms-and-conditions/850225"
CAESARS_HOTEL = "https://www.caesars.com/caesars-palace/hotel"

SOURCES = {
    "VEN_SCHED": {"title": "The Venetian: DeepStack Extravaganza IV schedule (official)", "url": VEN_SCHED, "publisher": "The Venetian Las Vegas (official)"},
    "VEN_POKER": {"title": "The Venetian: Poker Room (official)", "url": VEN_POKER_PAGE, "publisher": "The Venetian Las Vegas (official)"},
    "VEN_HOTEL": {"title": "The Venetian: Hotel Terms & Conditions (resort fee, room tax, parking)", "url": VEN_HOTEL_TERMS, "publisher": "The Venetian Las Vegas (official)"},
    "VEN_SUITE": {"title": "The Venetian: 2026 Poker Room Rates & Play Requirements", "url": VEN_SUITE_RATES, "publisher": "The Venetian Las Vegas (official)"},
    "WYNN_POKER": {"title": "Wynn Las Vegas: Poker Room (official)", "url": WYNN_POKER_PAGE, "publisher": "Wynn Las Vegas (official)"},
    "WYNN_POSTER": {"title": "Wynn: Daily Tournaments poster (official PDF)", "url": WYNN_POSTER, "publisher": "Wynn Las Vegas (official)"},
    "WYNN_DAILY_STRUCT": {"title": "Wynn: Daily Poker Tournaments terms and structure sheets (official PDF)", "url": WYNN_DAILY_STRUCT, "publisher": "Wynn Las Vegas (official)"},
    "WYNN_WPT_SCHED": {"title": "Wynn: WPT World Championship schedule Nov 27 – Dec 21, 2026 (official PDF)", "url": WYNN_WPT_SCHED, "publisher": "Wynn Las Vegas (official)"},
    "WYNN_WPT_STRUCT": {"title": "Wynn: WPT World Championship general terms & structures (official PDF, first page read)", "url": WYNN_WPT_STRUCT, "publisher": "Wynn Las Vegas (official)"},
    "WYNN_TERMS_OFFER": {"title": "Wynn: Special Offer Terms (resort fee $45 + tax; from $99 Sun–Thu / $169 Fri–Sat)", "url": WYNN_TERMS_OFFER, "publisher": "Wynn Las Vegas (official)"},
    "WYNN_TERMS_OFFER2": {"title": "Wynn: Special Offer Terms (resort fee $45 + tax)", "url": WYNN_TERMS_OFFER2, "publisher": "Wynn Las Vegas (official)"},
    "WYNN_TERMS_SUITE": {"title": "Wynn: Special Offer Terms (Tower Suite resort fee $55 + tax)", "url": WYNN_TERMS_SUITE, "publisher": "Wynn Las Vegas (official)"},
    "BELL_POKER": {"title": "Bellagio: Poker Room (official)", "url": BELL_POKER_PAGE, "publisher": "Bellagio Las Vegas (official)"},
    "BELL_FRI": {"title": "Bellagio: Friday $600 NLH structure (official PDF)", "url": BELL_FRI, "publisher": "Bellagio Las Vegas (official)"},
    "BELL_SAT": {"title": "Bellagio: Saturday NLH structure (official PDF, file name says $1,000, header says $1,100)", "url": BELL_SAT, "publisher": "Bellagio Las Vegas (official)"},
    "BELL_SUN": {"title": "Bellagio: Sunday $400 H.O.R.S.E. structure (official PDF)", "url": BELL_SUN, "publisher": "Bellagio Las Vegas (official)"},
    "CAESARS_HOTEL": {"title": "Caesars Palace: hotel page (official; resort fee not shown on fetched page)", "url": CAESARS_HOTEL, "publisher": "Caesars Entertainment (official)"},
}
for _n in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
           23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37]:
    SOURCES[f"VEN_S{_n}"] = {"title": f"Venetian DSE IV structure sheet #{_n} (official PDF)", "url": vs(_n), "publisher": "The Venetian Las Vegas (official)"}

# ---------------------------------------------------------------------------
# VENETIAN — SINGLE-ENTRY, SINGLE-DAY (verified: schedule + structure sheet read)
# fields: event, date, start, name, buy_in, gtd, house_fee, prize_pool, structure, eligibility, notes
# house_fee / prize_pool are the amounts printed on the structure sheet.
# ---------------------------------------------------------------------------
ADULT = "21+ with Venetian Rewards card"
V = []  # list of dicts (built below)


def v(event, date, start, name, buy_in, gtd, fee, pool, struct, elig=ADULT, notes="", bounty=False, gtd_note=None):
    V.append(dict(event=event, date=date, start=start, name=name, buy_in=buy_in, gtd=gtd,
                  house_fee=fee, prize_pool=pool, struct=struct, eligibility=elig, notes=notes,
                  bounty=bounty, gtd_note=gtd_note))


# 1-day standard NLH
v(2, "2026-11-18", "11:10 AM", "$300 No Limit Hold'em (1Day)", 300, 10000, 58, 242, 5,
  notes="Sheet 5 read. Late registration window not printed on sheet 5.")
v(3, "2026-11-19", "10:10 AM", "$200 No Limit Hold'em RaceDay Stack (1Day)", 200, None, 35, 165, 18,
  notes="Official schedule: 'Race to finish before the Race'. No guarantee printed on schedule or structure sheet.")
v(4, "2026-11-20", "10:10 AM", "$200 No Limit Hold'em RaceDay Stack (1Day)", 200, None, 35, 165, 18,
  notes="Same RaceDay structure as Event 3. No guarantee printed.")
v(5, "2026-11-21", "10:10 AM", "$200 No Limit Hold'em RaceDay Stack (1Day)", 200, None, 35, 165, 18,
  notes="Same RaceDay structure as Event 3. No guarantee printed.")
v(6, "2026-11-22", "11:10 AM", "$200 No Limit Hold'em (1Day)", 200, None, 40, 160, 29,
  notes="No guarantee printed on schedule or structure sheet.")
v(8, "2026-11-23", "5:10 PM", "$200 No Limit Hold'em PKO (Progressive Knock-Out Bounty) (1Day)", 200, 8000, 40, 160, 30,
  bounty=True, gtd_note="$8,000 guarantee = prize pool + total bounty money awarded.")
v(9, "2026-11-24", "5:10 PM", "$200 No Limit Hold'em Bounty $8K GTD (1Day)", 200, 8000, 40, 160, 1,
  bounty=True, gtd_note="$8,000 guarantee = prize pool + total bounties ($50 per elimination, sheet 1).")
v(10, "2026-11-25", "11:10 AM", "$400 No Limit Hold'em $15K GTD (1Day)", 400, 15000, 65, 335, 6)
v(11, "2026-11-25", "5:10 PM", "$200 No Limit Hold'em Bounty $8K GTD (1Day)", 200, 8000, 40, 160, 1,
  bounty=True, gtd_note="$8,000 guarantee = prize pool + total bounties.")
v(12, "2026-11-26", "11:10 AM", "$300 No Limit Hold'em $10K GTD (1Day)", 300, 10000, 58, 242, 5)
v(13, "2026-11-26", "5:10 PM", "$200 No Limit Hold'em Bounty $8K GTD (1Day)", 200, 8000, 40, 160, 1,
  bounty=True, gtd_note="$8,000 guarantee = prize pool + total bounties.")
v(14, "2026-11-27", "11:10 AM", "$600 No Limit Hold'em $30K GTD (1Day)", 600, 30000, 90, 510, 7)
v(15, "2026-11-27", "5:10 PM", "$200 No Limit Hold'em Bounty $8K GTD (1Day)", 200, 8000, 40, 160, 1,
  bounty=True, gtd_note="$8,000 guarantee = prize pool + total bounties.")
v(16, "2026-11-28", "11:10 AM", "$600 No Limit Hold'em Bounty $30K GTD (1Day)", 600, 30000, 90, 510, 11,
  bounty=True, gtd_note="$30,000 guarantee = prize pool + total bounties. $200 bounties to start, $500 once in the money.")
v(17, "2026-11-28", "12:10 PM", "$400 Pot Limit Omaha Bounty $15K GTD (1Day)", 400, 15000, 60, 340, 26,
  bounty=True, gtd_note="$15,000 guarantee = prize pool + total bounties ($100 bounty).")
v(18, "2026-11-28", "5:10 PM", "$200 No Limit Hold'em PokerAtlas Valuetown Bounty $20K GTD (1Day)", 200, 20000, 40, 160, 8,
  bounty=True, gtd_note="$20,000 guarantee = prize pool + total bounties.",
  notes="Schedule: PokerAtlas PRO member $20 rake discount. Local notes (sheet 8, rule 7): discount applies to initial buy-in only. Membership-linked.")
v(20, "2026-11-29", "12:10 PM", "$300 Pot Limit Omaha Double Board Bomb Pot $10K GTD (1Day)", 300, 10000, 58, 242, 22,
  notes="Double-board bomb pot format (schedule).")
v(21, "2026-11-29", "5:10 PM", "$200 No Limit Hold'em Bounty $8K GTD (1Day)", 200, 8000, 40, 160, 1,
  bounty=True, gtd_note="$8,000 guarantee = prize pool + total bounties.")
v(22, "2026-11-30", "5:10 PM", "$200 No Limit Hold'em Bounty $8K GTD (1Day)", 200, 8000, 40, 160, 1,
  bounty=True, gtd_note="$8,000 guarantee = prize pool + total bounties.")
v(23, "2026-12-01", "5:10 PM", "$200 No Limit Hold'em Bounty $8K GTD (1Day)", 200, 8000, 40, 160, 1,
  bounty=True, gtd_note="$8,000 guarantee = prize pool + total bounties.")
v(24, "2026-12-02", "10:10 AM", "$600 No Limit Hold'em Seniors $40K GTD (1Day) — 50+ only", 600, 40000, 90, 510, 17,
  elig="50+ with Venetian Rewards card",
  notes="15% of field paid (local notes, sheet 17).")
v(25, "2026-12-02", "5:10 PM", "$200 No Limit Hold'em Bounty $8K GTD (1Day)", 200, 8000, 40, 160, 1,
  bounty=True, gtd_note="$8,000 guarantee = prize pool + total bounties.")
v(27, "2026-12-03", "12:10 PM", "$600 BIG O $25K GTD (1Day)", 600, 25000, 90, 510, 28,
  notes="Event name as printed: BIG O.")
v(28, "2026-12-06", "11:10 AM", "$600 No Limit Hold'em $40K GTD (1Day)", 600, 40000, 90, 510, 7)
v(29, "2026-12-06", "5:10 PM", "$300 No Limit Hold'em Bounty $15K GTD (1Day)", 300, 15000, 50, 250, 15,
  bounty=True, gtd_note="$15,000 guarantee = prize pool + total bounties.")
v(30, "2026-12-07", "11:10 AM", "$600 No Limit Hold'em Bounty $40K GTD (1Day)", 600, 40000, 90, 510, 11,
  bounty=True, gtd_note="$40,000 guarantee = prize pool + total bounties. $200 bounties to start, $500 once in the money.")
v(31, "2026-12-07", "5:10 PM", "$300 No Limit Hold'em Bounty $15K GTD (1Day)", 300, 15000, 50, 250, 15,
  bounty=True, gtd_note="$15,000 guarantee = prize pool + total bounties.")
v(32, "2026-12-08", "10:10 AM", "$600 No Limit Hold'em Seniors $40K GTD (1Day) — 50+ only", 600, 40000, 90, 510, 17,
  elig="50+ with Venetian Rewards card",
  notes="15% of field paid (local notes, sheet 17).")
v(34, "2026-12-08", "5:10 PM", "$300 No Limit Hold'em Bounty $15K GTD (1Day)", 300, 15000, 50, 250, 15,
  bounty=True, gtd_note="$15,000 guarantee = prize pool + total bounties.")
v(36, "2026-12-09", "11:10 AM", "$800 No Limit Hold'em Bounty $75K GTD (1Day)", 800, 75000, 100, 700, 16,
  bounty=True, gtd_note="$75,000 guarantee = prize pool + total bounties. $200 bounties to start, $500 once in the money.")
v(38, "2026-12-09", "5:10 PM", "$300 No Limit Hold'em Bounty $15K GTD (1Day)", 300, 15000, 50, 250, 15,
  bounty=True, gtd_note="$15,000 guarantee = prize pool + total bounties.")
v(40, "2026-12-10", "12:10 PM", "$600 Pot Limit Omaha Bounty $25K GTD (1Day)", 600, 25000, 90, 510, 27,
  bounty=True, gtd_note="$25,000 guarantee = prize pool + total bounties ($200 bounty).")
v(42, "2026-12-10", "5:10 PM", "$300 No Limit Hold'em Bounty $15K GTD (1Day)", 300, 15000, 50, 250, 15,
  bounty=True, gtd_note="$15,000 guarantee = prize pool + total bounties.")
v(43, "2026-12-11", "11:10 AM", "$600 No Limit Hold'em LIPS KINGS & QUEENS Bounty $30K GTD (1Day)", 600, 30000, 90, 510, 33,
  elig="Open to all players (schedule: KINGS and QUEENS, open to all)",
  bounty=True, gtd_note="$30,000 guarantee = prize pool + total bounties ($200 bounty).",
  notes="$80 house fee plus $10 flat fee to LIPS (Vegas Connected, Inc.) — $90 total withheld; $510 prize pool.")
v(50, "2026-12-13", "5:10 PM", "$300 No Limit Hold'em Bounty $15K GTD (1Day)", 300, 15000, 50, 250, 15,
  bounty=True, gtd_note="$15,000 guarantee = prize pool + total bounties.")
v(51, "2026-12-14", "5:10 PM", "$300 No Limit Hold'em Bounty $15K GTD (1Day)", 300, 15000, 50, 250, 15,
  bounty=True, gtd_note="$15,000 guarantee = prize pool + total bounties.")
v(52, "2026-12-15", "11:10 AM", "$1,100 No Limit Hold'em PKO (Progressive Knock-Out Bounty) $75K GTD (1Day)", 1100, 75000, 130, 970, 34,
  bounty=True, gtd_note="$75,000 guarantee = prize pool + total bounty money (schedule: PKO).")
v(53, "2026-12-15", "5:10 PM", "$300 No Limit Hold'em Bounty $15K GTD (1Day)", 300, 15000, 50, 250, 15,
  bounty=True, gtd_note="$15,000 guarantee = prize pool + total bounties.")
v(54, "2026-12-16", "11:10 AM", "$600 No Limit Hold'em Bounty $50K GTD (1Day)", 600, 50000, 90, 510, 11,
  bounty=True, gtd_note="$50,000 guarantee = prize pool + total bounties. $200 bounties to start, $500 once in the money.")
v(55, "2026-12-16", "5:10 PM", "$300 No Limit Hold'em Bounty $15K GTD (1Day)", 300, 15000, 50, 250, 15,
  bounty=True, gtd_note="$15,000 guarantee = prize pool + total bounties.")
v(57, "2026-12-17", "12:10 PM", "$600 Pot Limit Omaha Double Board Bomb Pot $25K GTD (1Day)", 600, 25000, 90, 510, 23,
  notes="Double-board bomb pot format (schedule).")
v(58, "2026-12-19", "5:10 PM", "$200 No Limit Hold'em PokerAtlas Valuetown Bounty $20K GTD (1Day)", 200, 20000, 40, 160, 8,
  bounty=True, gtd_note="$20,000 guarantee = prize pool + total bounties.",
  notes="Schedule: PokerAtlas PRO member $20 rake discount. Membership-linked.")
v(60, "2026-12-20", "5:10 PM", "$200 No Limit Hold'em Bounty $8K GTD (1Day)", 200, 8000, 40, 160, 1,
  bounty=True, gtd_note="$8,000 guarantee = prize pool + total bounties.")
v(61, "2026-12-21", "5:10 PM", "$200 No Limit Hold'em Bounty $8K GTD (1Day)", 200, 8000, 40, 160, 1,
  bounty=True, gtd_note="$8,000 guarantee = prize pool + total bounties.")
v(62, "2026-12-22", "5:10 PM", "$200 No Limit Hold'em Bounty $8K GTD (1Day)", 200, 8000, 40, 160, 1,
  bounty=True, gtd_note="$8,000 guarantee = prize pool + total bounties.")
v(63, "2026-12-23", "11:10 AM", "$600 No Limit Hold'em $30K GTD (1Day)", 600, 30000, 90, 510, 7)
v(64, "2026-12-23", "5:10 PM", "$200 No Limit Hold'em Bounty $8K GTD (1Day)", 200, 8000, 40, 160, 1,
  bounty=True, gtd_note="$8,000 guarantee = prize pool + total bounties.")

# ---------------------------------------------------------------------------
# VENETIAN — MULTI-FLIGHT (player may enter more than one flight; separate section)
# ---------------------------------------------------------------------------
VEN_MULTI = [
    dict(event=1, date="2026-11-16", start="11:10 AM / 5:10 PM (1A/1B); 11:10 AM / 5:10 PM Nov 17 (1C/1D)",
         name="$300 No Limit Hold'em 1A–1D $75K GTD (flights)", buy_in=300, gtd=75000, house_fee=60, prize_pool=240,
         structure=[10, 9], why="Flights 1A–1D on official schedule. Structure sheet rule 8: a player who bags chips for Day 2 may not play a subsequent flight, so a player can buy into more than one flight before bagging.",
         notes="Day 2 restart Wed Nov 18, 12:00 PM. Sheet 10 (1A/1C) read; sheet 9 (1B/1D) linked on schedule but NOT read — flagged."),
    dict(event=7, date="2026-11-23", start="11:10 AM (1A, Nov 23); 11:10 AM (1B, Nov 24)",
         name="$400 No Limit Hold'em 1A/1B $75K GTD (flights)", buy_in=400, gtd=75000, house_fee=70, prize_pool=330,
         structure=[2], why="Flights 1A and 1B. Structure rule 8: a player who bags chips for Day 2 may not play a subsequent flight.",
         notes="Day 2 restart Wed Nov 25, 11:00 AM."),
    dict(event=19, date="2026-11-29", start="11:10 AM (1A Nov 29; 1B Nov 30; 1C Dec 1)",
         name="$400 No Limit Hold'em 1A/1B/1C $75K GTD (flights)", buy_in=400, gtd=75000, house_fee=None, prize_pool=None,
         structure=[3], why="Flights 1A, 1B and 1C on official schedule (multi-flight label). Sheet 3 linked but NOT read — fee breakdown unverified.",
         notes="Day 2 restart Wed Dec 2, 11:00 AM."),
    dict(event=26, date="2026-12-03", start="11:10 AM / 5:10 PM across Dec 3–5 (1A–1F)",
         name="$800 No Limit Hold'em 1A–1F $500K GTD (flights, incl. Turbo 1F)", buy_in=800, gtd=500000, house_fee=None, prize_pool=None,
         structure=[12, 13, 14], why="Six flights (1A–1F) on official schedule — multi-flight. Structure sheets 12/13/14 linked, not read.",
         notes="Day 2 restart Sun Dec 6, 12:00 PM. Fee breakdown unverified."),
    dict(event=47, date="2026-12-12", start="10:10 AM (1A, Dec 12); 6:10 PM (1B, Dec 12)",
         name="$2,200 No Limit Hold'em 1A/1B $1 Million GTD — PokerAtlas Championship Title Event", buy_in=2200, gtd=1000000, house_fee=None, prize_pool=None,
         structure=[21, 37], why="Flights 1A and 1B on official schedule — multi-flight. Sheets 21/37 linked, not read.",
         notes="Day 2 restart Sun Dec 13, 1:00 PM; Day 3 restart Mon Dec 14, 11:00 AM."),
    dict(event=49, date="2026-12-13", start="10:10 AM (1A Dec 13); 10:10 AM (1B Dec 14)",
         name="$1,100 No Limit Hold'em Seniors 1A/1B $300K GTD — 50+ only", buy_in=1100, gtd=300000, house_fee=None, prize_pool=None,
         structure=[20], why="Flights 1A and 1B on official schedule — multi-flight. 50+ only. Sheet 20 linked, not read.",
         notes="Day 2 restart Tue Dec 15, 10:00 AM."),
    dict(event=56, date="2026-12-17", start="10:10 AM (1A Dec 17); 6:10 PM (1B Dec 17); 10:10 AM (1C Dec 18); 6:10 PM (1D Dec 18); 10:10 AM (1E Dec 19)",
         name="$1,100 No Limit Hold'em 1A–1E $500K GTD (flights)", buy_in=1100, gtd=500000, house_fee=None, prize_pool=None,
         structure=[35, 36], why="Flights 1A–1E on official schedule — multi-flight. Schedule notes a $40 rake discount for entries before 10:10 AM / 6:10 PM. Sheets 35/36 linked, not read.",
         notes="Day 2 restart Sun Dec 20, 11:00 AM."),
    dict(event=59, date="2026-12-20", start="11:10 AM (1A Dec 20); 11:10 AM (1B Dec 21); 11:10 AM (1C Dec 22)",
         name="$600 No Limit Hold'em 1A–1C $150K GTD (flights)", buy_in=600, gtd=150000, house_fee=None, prize_pool=None,
         structure=[4], why="Flights 1A–1C on official schedule — multi-flight. Schedule notes a $20 rake discount for entries before 11:10 AM. Sheet 4 linked, not read.",
         notes="Day 2 restart Wed Dec 23, 11:00 AM."),
]

# ---------------------------------------------------------------------------
# VENETIAN — SATELLITES AND UNVERIFIED-RULE EVENTS (schedule-level values only)
# ---------------------------------------------------------------------------
VEN_OTHER = [
    dict(event=33, date="2026-12-08", start="4:10 PM", name="$100 NLH LIPS Ladies Milestone Satellite (1Day) — awards direct entry to Event 39", buy_in=100, gtd=None, structure=[19], kind="Satellite (entry ticket)", notes="Structure sheet 19 linked, not read."),
    dict(event=37, date="2026-12-09", start="4:10 PM", name="$100 NLH LIPS Ladies Milestone Satellite (1Day) — awards direct entry to Event 39", buy_in=100, gtd=None, structure=[19], kind="Satellite (entry ticket)", notes="Structure sheet 19 linked, not read."),
    dict(event=41, date="2026-12-10", start="4:10 PM", name="$260 NLH Milestone Satellite (1Day) — awards direct entry to Event 47", buy_in=260, gtd=None, structure=[24], kind="Satellite (entry ticket)", notes="Structure sheet 24 linked, not read."),
    dict(event=44, date="2026-12-11", start="4:10 PM", name="$260 NLH Milestone Satellite (1Day) — awards direct entry to Event 47", buy_in=260, gtd=None, structure=[24], kind="Satellite (entry ticket)", notes="Structure sheet 24 linked, not read."),
    dict(event=45, date="2026-12-11", start="8:10 PM", name="$260 NLH Turbo Milestone Satellite (1Day) — awards direct entry to Event 47", buy_in=260, gtd=None, structure=[25], kind="Satellite (entry ticket)", notes="Structure sheet 25 linked, not read."),
    dict(event=46, date="2026-12-12", start="9:10 AM", name="$260 NLH Turbo Milestone Satellite (1Day) — awards direct entry to Event 47", buy_in=260, gtd=None, structure=[25], kind="Satellite (entry ticket)", notes="Structure sheet 25 linked, not read."),
    dict(event=48, date="2026-12-12", start="12:10 PM", name="$260 NLH Turbo Milestone Satellite (1Day) — awards direct entry to Event 47", buy_in=260, gtd=None, structure=[25], kind="Satellite (entry ticket)", notes="Structure sheet 25 linked, not read."),
    dict(event=35, date="2026-12-09", start="10:10 AM", name="$600 NLH LIPS Poker Jingle Tag Team $10K GTD (1Day) — tag teams (F/F or F/M)", buy_in=600, gtd=10000, structure=[31], kind="Tag-team format — single-entry status unverified", notes="Structure sheet 31 linked, not read."),
    dict(event=39, date="2026-12-10", start="10:10 AM (2-Day; Day 2 Dec 11 10:00 AM; final table 7:00 PM streamed)", name="$800 NLH LIPS Ladies $40K GTD (2Day) — Women in Poker Main Event", buy_in=800, gtd=40000, structure=[32], kind="2-day event — entry rules unverified", notes="Structure sheet 32 linked, not read. Eligibility per schedule title only."),
]

# ---------------------------------------------------------------------------
# WYNN — DAILY (official poster + daily terms). ALL are multi-entry (re-entry / rebuy / add-on).
# ---------------------------------------------------------------------------
WYNN_DAILY = [
    dict(days="Mon–Thu", start="12:00 PM", name="$200 NLH — $10,000 GTD (single day)", buy_in=200, gtd=10000,
         entry="Re-entry allowed through Level 9 (~4:30 PM). Starting chips 25,000; 30-minute levels.",
         fee="$26 tournament fee + $12 staff service charge; $162 to prize pool", struct=WYNN_DAILY_STRUCT, poster=WYNN_POSTER),
    dict(days="Friday", start="12:00 PM", name="$240 NLH Rebuy & Add-on — $40,000 GTD", buy_in=240, gtd=40000,
         entry="Re-entry NOT allowed. $200 rebuys (25,000 chips) and one $100 add-on (15,000 chips).",
         fee="$35 tournament fee + $15 staff; $190 of each entry to prize pool", struct=WYNN_DAILY_STRUCT, poster=WYNN_POSTER),
    dict(days="Sat & Sun", start="12:00 PM", name="$200 NLH — $25,000 GTD (single day)", buy_in=200, gtd=25000,
         entry="Re-entry allowed and one $100 add-on per entry until start of Level 11 (~5:30 PM).",
         fee="$26 tournament fee + $12 staff; $162 to prize pool", struct=WYNN_DAILY_STRUCT, poster=WYNN_POSTER),
    dict(days="Nightly (Mon–Sun)", start="6:00 PM", name="$160 NLH — $10,000 GTD (single day)", buy_in=160, gtd=10000,
         entry="Re-entry and one $100 add-on per entry through Level 9 (~9:00 PM). 20-minute levels.",
         fee="$20 tournament fee + $10 staff; $130 to prize pool", struct=WYNN_DAILY_STRUCT, poster=WYNN_POSTER),
]

# ---------------------------------------------------------------------------
# BELLAGIO — official weekly events. ALL allow re-entry and/or voluntary chip-for-$ gratuity.
# ---------------------------------------------------------------------------
BELL = [
    dict(day="Friday", start="11:00 AM", name="$600 No Limit Hold'em", buy_in=600, gtd=None,
         entry="Re-entry through Level 8. 30,000 starting chips.",
         fee="$50 house fee; $510 prize pool; $40 VOLUNTARY staff gratuity that grants an extra 15,000 starting chips",
         struct=BELL_FRI, note="Bellagio guarantees combined pool only in Saturday event (see below). Friday: no GTD printed."),
    dict(day="Saturday", start="11:00 AM", name="No Limit Hold'em (sheet header $1,100; file name and page say $1,000)", buy_in=None, gtd=50000,
         entry="Re-entry/flight structure per official PDF (see Flagged: fee and name conflict). Combined Day 2 per PDF.",
         fee="Sheet rule 7: $510 to prize pool, $50 admin, $40 optional gratuity (= $600 total). Gratuity grants extra 20,000 chips.",
         struct=BELL_SAT, note="IRREGULARITY: file name and official page say $1,000; sheet header says $1,100; fee math sums to $600. Combined prize pool guaranteed at least $50,000 (rule 8)."),
    dict(day="Sunday", start="11:00 AM", name="$400 H.O.R.S.E.", buy_in=400, gtd=None,
         entry="Re-entry through Level 8.",
         fee="$35 house fee; $340 prize pool; $25 VOLUNTARY staff gratuity granting an extra 15,000 chips",
         struct=BELL_SUN, note="Payout approx. 12.5% of field. No GTD printed."),
]

# ---------------------------------------------------------------------------
# WYNN WPT WORLD CHAMPIONSHIP (Nov 27 – Dec 21, 2026). Schedule-level only; rules NOT verified.
# (date, time, name, buy_in, gtd)  — from official schedule PDF. Flight/Day labels preserved.
# ---------------------------------------------------------------------------
WPT = [
    ("2026-11-27", "11:00 AM", "No Limit Hold'em Day 1A", 600, 400000),
    ("2026-11-27", "12:00 PM", "TORSE", 600, None),
    ("2026-11-27", "1:00 PM", "PLO", 400, None),
    ("2026-11-27", "5:00 PM", "No Limit Hold'em Day 1B", 600, 400000),
    ("2026-11-28", "11:00 AM", "No Limit Hold'em Day 1C", 600, 400000),
    ("2026-11-28", "12:00 PM", "Mixed Triple Draw (A-5, 2-7, Badugi)", 600, None),
    ("2026-11-28", "5:00 PM", "No Limit Hold'em Day 1D", 600, 400000),
    ("2026-11-29", "11:00 AM", "No Limit Hold'em Day 1E", 600, 400000),
    ("2026-11-29", "6:00 PM", "No Limit Hold'em Day 1F", 600, 400000),
    ("2026-11-30", "11:00 AM", "No Limit Hold'em Day 1A", 800, 1000000),
    ("2026-11-30", "12:00 PM", "Limit Omaha 8", 600, None),
    ("2026-11-30", "1:00 PM", "No Limit Hold'em Day 2", 800, 1000000),
    ("2026-11-30", "5:00 PM", "No Limit Hold'em Day 1B", 800, 1000000),
    ("2026-12-01", "11:00 AM", "No Limit Hold'em Day 1C", 800, 1000000),
    ("2026-12-01", "12:00 PM", "Limit Omaha 8/5/Stud 8", 600, None),
    ("2026-12-01", "1:00 PM", "PLO", 1100, None),
    ("2026-12-01", "5:00 PM", "No Limit Hold'em Day 1D", 800, 1000000),
    ("2026-12-02", "11:00 AM", "No Limit Hold'em Day 1E", 800, 1000000),
    ("2026-12-02", "6:00 PM", "No Limit Hold'em Day 1F", 800, 1000000),
    ("2026-12-03", "11:00 AM", "No Limit Hold'em Day 1A", 1600, 1000000),
    ("2026-12-03", "1:00 PM", "No Limit Hold'em Day 2", 1600, 1000000),
    ("2026-12-03", "7:00 PM", "Double Play Milestone Satellite (2 x $1,100 ticket)", 400, None),
    ("2026-12-04", "11:00 AM", "No Limit Hold'em Day 1B", 1600, 1000000),
    ("2026-12-04", "12:00 PM", "HORSE", 600, None),
    ("2026-12-04", "7:00 PM", "Double Play Milestone Satellite (2 x $1,100 ticket)", 400, None),
    ("2026-12-05", "11:00 AM", "No Limit Hold'em Day 2", 1100, 5000000),
    ("2026-12-05", "11:00 AM", "WPT Prime Championship Day 1A", 1100, 5000000),
    ("2026-12-05", "9:00 PM", "NLH Turbo", 600, 50000),
    ("2026-12-06", "11:00 AM", "WPT Prime Championship Day 1B", 1100, 5000000),
    ("2026-12-06", "11:00 AM", "PLO Mystery Bounty Day 1A", 1600, 500000),
    ("2026-12-06", "12:00 PM", "Milestone Satellite to $1,100 Prime Championship", 200, None),
    ("2026-12-06", "6:00 PM", "PLO Mystery Bounty Day 1B", 1600, 500000),
    ("2026-12-06", "7:00 PM", "Double Play Milestone Satellite (2 x $1,100 ticket)", 400, None),
    ("2026-12-06", "9:00 PM", "NLH Turbo", 600, 50000),
    ("2026-12-07", "11:00 AM", "WPT Prime Championship Day 1C", 1100, 5000000),
    ("2026-12-07", "11:00 AM", "HORSE (2 Day)", 1100, None),
    ("2026-12-07", "12:00 PM", "PLO Mystery Bounty Day 2", None, None),
    ("2026-12-07", "1:00 PM", "PLO $500 Bounty", 1600, 100000),
    ("2026-12-07", "7:00 PM", "Milestone Satellite Package to Prime and World Championship", 1600, None),
    ("2026-12-07", "9:00 PM", "NLH Turbo", 600, 50000),
    ("2026-12-08", "11:00 AM", "WPT Prime Championship Day 1D", 1100, 5000000),
    ("2026-12-08", "7:00 PM", "Milestone Satellite to $10,400 World Championship", 1100, None),
    ("2026-12-08", "9:00 PM", "NLH Turbo", 600, 50000),
    ("2026-12-09", "11:00 AM", "No Limit Hold'em (2 Day)", 1600, 1000000),
    ("2026-12-09", "12:00 PM", "WPT Prime Championship Day 2", None, None),
    ("2026-12-09", "1:00 PM", "PLO $1,000 Bounty", 3000, 250000),
    ("2026-12-09", "1:00 PM", "Limit Omaha 8", 800, None),
    ("2026-12-09", "2:00 PM", "Milestone Satellite to $10,400 World Championship", 1100, None),
    ("2026-12-09", "7:00 PM", "Milestone Satellite to $10,400 World Championship", 1100, None),
    ("2026-12-09", "9:00 PM", "NLH Turbo", 600, 50000),
    ("2026-12-10", "10:00 AM", "Super Gold Million Mystery Bounty Day 1A", 400, 3000000),
    ("2026-12-10", "12:00 PM", "WPT Prime Championship Day 3", None, None),
    ("2026-12-10", "6:00 PM", "Super Gold Million Mystery Bounty Day 1B", 400, 3000000),
    ("2026-12-11", "10:00 AM", "Super Gold Million Mystery Bounty Day 1C", 400, 3000000),
    ("2026-12-11", "12:00 PM", "WPT Prime Championship Day 4", None, None),
    ("2026-12-11", "6:00 PM", "Super Gold Million Mystery Bounty Day 1D", 400, 3000000),
    ("2026-12-12", "10:00 AM", "No Limit Hold'em", 800, 100000),
    ("2026-12-12", "1:00 PM", "PLO", 3000, 250000),
    ("2026-12-12", "2:00 PM", "WPT Prime Championship Final Table", None, None),
    ("2026-12-12", "2:00 PM", "Super Gold Million Mystery Bounty Day 2", None, None),
    ("2026-12-12", "2:00 PM", "Milestone Satellite to $10,400 World Championship 1A/8", 1100, None),
    ("2026-12-12", "4:00 PM", "Milestone Satellite to $10,400 Ladies NLH Championship", 200, None),
    ("2026-12-12", "7:00 PM", "Milestone Satellite to $10,400 World Championship 1A/8", 1100, None),
    ("2026-12-12", "9:00 PM", "NLH Turbo", 600, 50000),
    ("2026-12-13", "11:00 AM", "WPT World Championship Day 1A ($1,000,000 added)", 10400, None),
    ("2026-12-13", "11:00 AM", "Ladies NLH Championship (2 Day)", 1100, 250000),
    ("2026-12-13", "11:00 AM", "No Limit Hold'em Day 1A", 800, 500000),
    ("2026-12-13", "12:00 PM", "PLO Day 1A", 1600, 1000000),
    ("2026-12-13", "12:00 PM", "Milestone Satellite to $10,400 World Championship 1B", 1100, None),
    ("2026-12-13", "1:00 PM", "Super Gold Million Mystery Bounty Day 3", None, None),
    ("2026-12-13", "6:00 PM", "Milestone Satellite to $10,400 World Championship 1B/C", 1100, None),
    ("2026-12-14", "11:00 AM", "WPT World Championship Day 1B ($1,000,000 added)", 10400, None),
    ("2026-12-14", "11:00 AM", "No Limit Hold'em Day 1B", 800, 500000),
    ("2026-12-14", "12:00 PM", "PLO Day 1B", 1600, 1000000),
    ("2026-12-14", "12:00 PM", "Mixed Triple Draw (A-5, 2-7, Badugi) (2 Day)", 1100, None),
    ("2026-12-14", "12:00 PM", "Milestone Satellite to $10,400 World Championship 1C", 1100, None),
    ("2026-12-14", "2:00 PM", "Super Gold Million Mystery Bounty Final Table", None, None),
    ("2026-12-14", "6:00 PM", "Milestone Satellite to $10,400 World Championship 1C", 1100, None),
    ("2026-12-14", "7:00 PM", "PLO Turbo", 1100, 100000),
    ("2026-12-14", "9:00 PM", "NLH Turbo", 600, 50000),
    ("2026-12-15", "11:00 AM", "WPT World Championship Day 1C ($1,000,000 added)", 10400, None),
    ("2026-12-15", "11:00 AM", "No Limit Hold'em Day 2", None, None),
    ("2026-12-15", "11:00 AM", "Milestone Satellite to $10,400 World Championship 1C/Day 2", 1100, None),
    ("2026-12-15", "12:00 PM", "PLO Day 2", None, None),
    ("2026-12-15", "12:00 PM", "Big O", 1100, None),
    ("2026-12-15", "1:00 PM", "PLO Progressive Bounty (PKO)", 3000, 250000),
    ("2026-12-15", "6:00 PM", "Milestone Satellite to $10,400 World Championship Day 2", 1100, None),
    ("2026-12-15", "7:00 PM", "NIH $500 Bounty Turbo (as printed on official schedule)", 1600, 100000),
    ("2026-12-17", "11:00 AM", "Seniors NLH Championship (3 Day)", 1100, 500000),
    ("2026-12-17", "11:00 AM", "Wynn Mixed Championship (2 Day)", 1600, None),
    ("2026-12-17", "12:00 PM", "WPT World Championship Day 3", None, None),
    ("2026-12-17", "12:00 PM", "No Limit Hold'em Day 2", None, None),
    ("2026-12-17", "12:00 PM", "No Limit Hold'em Day 1A", 3000, 2000000),
    ("2026-12-17", "1:00 PM", "NLH High Roller (2 Day)", 25800, None),
    ("2026-12-17", "2:00 PM", "Milestone Satellite to $3,000 NLH", 400, None),
    ("2026-12-17", "7:00 PM", "Milestone Satellite to $3,000 NLH", 400, None),
    ("2026-12-18", "10:00 AM", "Milestone Satellite to $3,000 NLH", 400, None),
    ("2026-12-18", "11:00 AM", "No Limit Hold'em Day 1A", 1100, 1000000),
    ("2026-12-18", "12:00 PM", "WPT World Championship Day 2 (registration open until start of Day 2)", None, None),
    ("2026-12-18", "12:00 PM", "PLO Double Board Bomb Pot", 800, None),
    ("2026-12-18", "12:00 PM", "No Limit Hold'em Day 1B", 3000, 2000000),
    ("2026-12-18", "12:00 PM", "Limit Omaha 8 Championship (2 Day)", 1600, None),
    ("2026-12-18", "12:00 PM", "No Limit Hold'em", 600, 100000),
    ("2026-12-18", "1:00 PM", "PLO 6-Max", 10500, None),
    ("2026-12-18", "1:00 PM", "HORSE", 800, None),
    ("2026-12-18", "1:00 PM", "NLH 6-Max", 10500, None),
    ("2026-12-18", "2:00 PM", "Milestone Satellite to $5,000 Seniors High Roller", 600, None),
    ("2026-12-18", "6:00 PM", "Milestone Satellite to $25K NIH High Roller", 3000, None),
    ("2026-12-18", "6:00 PM", "Milestone Satellite to $3,000 NLH", 400, None),
    ("2026-12-18", "6:00 PM", "NLH Turbo", 1100, 100000),
    ("2026-12-18", "7:00 PM", "No Limit Hold'em Day 1B", 1100, 1000000),
    ("2026-12-19", "11:00 AM", "Seniors High Roller (3 Day)", 5000, 250000),
    ("2026-12-19", "11:00 AM", "NLH Mystery Bounty Day 1A", 1600, 1000000),
    ("2026-12-19", "12:00 PM", "WPT World Championship Day 5", None, None),
    ("2026-12-19", "12:00 PM", "No Limit Hold'em Day 2", None, None),
    ("2026-12-19", "12:00 PM", "Milestone Satellite to $1,600 Mystery Bounty", 300, None),
    ("2026-12-19", "1:00 PM", "PLO", 10500, None),
    ("2026-12-19", "1:00 PM", "NLH 6-Max", 3000, 500000),
    ("2026-12-19", "1:00 PM", "TORSE Championship (2 Day)", 1600, None),
    ("2026-12-19", "5:00 PM", "Milestone Satellite to $1,600 Mystery Bounty", 300, None),
    ("2026-12-19", "6:00 PM", "NLH 6-Max Turbo", 600, 50000),
    ("2026-12-19", "7:00 PM", "NLH Mystery Bounty Day 1B", 1600, 1000000),
    ("2026-12-20", "11:00 AM", "NLH Mystery Bounty Day 1C", 1600, 1000000),
    ("2026-12-20", "12:00 PM", "No Limit Hold'em Final Table", None, None),
    ("2026-12-20", "12:00 PM", "No Limit Hold'em", 600, 50000),
    ("2026-12-20", "1:00 PM", "NLH 8-Max", 10500, None),
    ("2026-12-20", "1:00 PM", "Mixed Triple Draw (A-5, 2-7, Badugi)", 600, None),
    ("2026-12-20", "2:00 PM", "WPT World Championship Final Table", None, None),
    ("2026-12-20", "6:00 PM", "5-Card PLO Turbo", 600, 50000),
    ("2026-12-20", "7:00 PM", "NLH Mystery Bounty Day 1D", 1600, 1000000),
    ("2026-12-21", "12:00 PM", "No Limit Hold'em", 1100, 100000),
    ("2026-12-21", "1:00 PM", "NLH Mystery Bounty Day 2", None, None),
    ("2026-12-21", "8:00 PM", "NLH Turbo", 600, 50000),
]

# ---------------------------------------------------------------------------
# HOTELS — only official-source values. None = not confirmed (flagged).
# ---------------------------------------------------------------------------
TAX_RATE = 0.1338  # Clark County room tax stated on The Venetian official hotel terms


def true_cost(rate, fee, tax=TAX_RATE):
    if rate is None or fee is None:
        return None
    return round((rate + fee) * (1 + tax), 2)


HOTELS = [
    dict(
        name="The Venetian Resort (Venetian tower)",
        tournaments="DeepStack Extravaganza IV: single-entry Venetian events (Section A)",
        in_building="Yes — The Venetian Poker Room is on level 2 of The Palazzo, Grand Canal Shoppes (official poker page). Same resort campus.",
        base_rate_from=119, rate_basis="Poker suite rate 'as low as $119' (Luxury King Suite, 2026). Conditional: poker-room play each night (6 hours live cash OR buy-in to a $300+ tournament per night stayed). Not a guaranteed nightly rate. Date-specific rate not verified.",
        resort_fee=55, resort_fee_basis="Venetian hotel terms: $55 + applicable tax per night (official)",
        room_tax=TAX_RATE, parking="Hotel guests: $20/day self-parking, $40/day valet (official hotel terms). Poker-room players: complimentary self-parking after 3+ hours of play (official poker page). Non-guest rates NOT verified.",
        walking="In-building for DSE events (official). Walking distance to other properties: NOT VERIFIED.",
        quality="NOT VERIFIED from official source (no rating source fetched).",
        sources=["VEN_SUITE", "VEN_HOTEL", "VEN_POKER", "VEN_SCHED"],
        flags=["Nightly rate is a floor for qualifying poker players, not an advertised nightly price.", "Room tax assumed to apply to the resort fee too ('plus applicable tax' stated) — confirm at check-in."],
    ),
    dict(
        name="The Palazzo (same resort; poker room on Palazzo side)",
        tournaments="DeepStack Extravaganza IV (Section A) — poker room location",
        in_building="Yes — poker room is 'The Palazzo, level 2, Grand Canal Shoppes' (official).",
        base_rate_from=209, rate_basis="Poker suite rate 'as low as $209' (Palazzo Luxury King Suite, 2026). Same qualifying-play conditions as The Venetian.",
        resort_fee=55, resort_fee_basis="Official poker suite page: '$55 resort fee per night stayed' for both The Venetian and The Palazzo.",
        room_tax=TAX_RATE, parking="Same Venetian/Palazzo parking policy (official).",
        walking="In-building for DSE (official).",
        quality="NOT VERIFIED from official source.",
        sources=["VEN_SUITE", "VEN_HOTEL", "VEN_POKER"],
        flags=["Starting rate; check date-specific rate at booking (not captured here).", "Tax on resort fee assumed — confirm."],
    ),
    dict(
        name="Wynn Las Vegas",
        tournaments="Daily Wynn tournaments (multi-entry, Section B) and WPT World Championship (Nov 27 – Dec 21; rules unverified, Section C)",
        in_building="Wynn daily poker room is in Encore at Wynn Las Vegas (official Wynn terms reference). Same resort complex.",
        base_rate_from=None, rate_basis="NOT VERIFIED for current dates. Undated official offer (terms 848654) lists 'from $99 Sun–Thu / $169 Fri–Sat' for Resort King with a 3-night minimum. Offer 850225 (Tower Suites) is EXPIRED: travel window ended Aug 31, 2026. Neither is a current nightly price.",
        resort_fee=None, resort_fee_basis="NOT VERIFIED for current dates. Undated offer 848654 says $45 + tax per night. Expired offer 850225 says $55 + tax per night. Conflict left blank; not used in totals.",
        room_tax=None, parking="NOT VERIFIED from official source (offer 848654 says parking is 'complimentary' only for resort fee holders; stated as an amenity, not a rate).",
        walking="In-building for Wynn daily events (Encore). Walking distance to other venues NOT VERIFIED.",
        quality="NOT VERIFIED from official source.",
        sources=["WYNN_TERMS_OFFER", "WYNN_TERMS_OFFER2", "WYNN_TERMS_SUITE", "WYNN_POKER", "WYNN_DAILY_STRUCT"],
        flags=["Official Wynn base-rate and fee pages (wynnlasvegas.com/hotel) are dead. No current official nightly rate or resort fee was retrieved.", "Resort fee conflict in official Wynn offer terms ($45 undated vs $55 expired).", "Room tax rate for Wynn not stated on a Wynn source; not applied.", "Wynn daily T&C say registration is in 'Encore at Wynn'; verify poker room location (see Flagged)."],
    ),
    dict(
        name="Bellagio",
        tournaments="Weekly Bellagio events (multi-entry / gratuity-advantage, Section B)",
        in_building="Yes — Bellagio poker room is on the north side of the casino (official).",
        base_rate_from=None, rate_basis="NOT VERIFIED — no official nightly rate fetched.",
        resort_fee=None, resort_fee_basis="NOT VERIFIED from official MGM source. Secondary sites say $55 + tax (not used in calculations).",
        room_tax=None, parking="NOT VERIFIED from official source.",
        walking="In-building for Bellagio events (official). Other venues: NOT VERIFIED.",
        quality="NOT VERIFIED from official source.",
        sources=["BELL_POKER"],
        flags=["Official MGM resort-fee and room-rate pages were not retrievable in this session.", "Secondary-source resort fee ($55 + tax) left unverified and excluded from totals."],
    ),
    dict(
        name="Caesars Palace",
        tournaments="None verified (no official Caesars poker schedule retrieved)",
        in_building="NOT APPLICABLE — no verified tournament venue in this report.",
        base_rate_from=None, rate_basis="NOT VERIFIED.",
        resort_fee=None, resort_fee_basis="CONFLICT across non-official sources ($49.95, $55, $62.30). Official hotel page fetched did not show the fee. NOT VERIFIED.",
        room_tax=None, parking="NOT VERIFIED.",
        walking="NOT VERIFIED.",
        quality="Official page states THE VILLAS Caesars Palace holds AAA Five Diamond designation (official Caesars statement; AAA not checked directly).",
        sources=["CAESARS_HOTEL"],
        flags=["Included for comparison only; no verified tournament link.", "Resort fee unverified."],
    ),
]


def build_hotel_costs():
    out = []
    for h in HOTELS:
        h = dict(h)
        h["true_cost_from_per_night"] = true_cost(h["base_rate_from"], h["resort_fee"])
        out.append(h)
    return out
