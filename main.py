"""News front page: Tuesday 17 November 2026. 48 verified stories.

Draws a 1024x1024 newspaper front page with PIL only. Deterministic:
no network, no randomness, no timestamps, fixed data and fonts.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
NAVY = (20, 33, 61)
GOLD = (201, 162, 39)
INK = (26, 26, 26)
MUTED = (90, 86, 76)
RULE = (180, 172, 150)
WHITE = (255, 255, 255)
SKY = (214, 228, 240)
SEA = (178, 205, 228)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)
F_REG = lambda s: font("DejaVuSans.ttf", s)

TAG_COLORS = {
    "EUROPE": (31, 78, 140),
    "MIDDLE EAST": (176, 92, 20),
    "ASIA": (178, 34, 34),
    "AFRICA": (34, 120, 60),
    "AMERICAS": (110, 60, 140),
    "GLOBAL": (90, 90, 90),
    "OCEANIA": (0, 130, 130),
}

# (number, tag, headline, description, continent, lon, lat)
MAINS = [
    (1, "EUROPE · UKRAINE WAR",
     "Ukraine strikes Crimean Bridge for a second day",
     "A road section falls into the Kerch Strait; Zelenskyy hails an "
     "\u201cunprecedented operation\u201d.",
     "EUROPE", 33.0, 45.0),
    (2, "MIDDLE EAST · IRAN WAR",
     "Iran fires drones at US radar in Bahrain",
     "Bahrain says all drones intercepted; US jets hit Iran\u2019s "
     "Qeshm Island missile site.",
     "MIDDLE EAST", 50.5, 26.2),
    (3, "EUROPE · UKRAINE WAR",
     "Russian strikes hit two key Kyiv bridges",
     "Water, heat, power cut. UN: 2026 toll tops any since 2022.",
     "EUROPE", 30.5, 50.4),
    (4, "ASIA · DIPLOMACY",
     "APEC leaders gather ahead of Trump\u2013Xi\u2013Putin summit",
     "Agenda: denuclearisation, Iran, Ukraine, trade.",
     "ASIA", 114.0, 22.5),
    (5, "AMERICAS · HEALTH",
     "US, Mexico, Bolivia lose measles-free status",
     "PAHO: US held status 26 years; 5,400+ cases in 2026.",
     "AMERICAS", -98.0, 39.0),
    (6, "AFRICA · HEALTH",
     "Ebola outbreak in DR Congo more than doubles",
     "11,000+ cases, 5,400 deaths.",
     "AFRICA", 23.0, -2.0),
    (7, "ASIA · DIPLOMACY",
     "Trump announces critical-minerals deals in Manila",
     "Trump says Quad signed minerals deals.",
     "ASIA", 121.0, 14.6),
    (8, "MIDDLE EAST · POLITICS",
     "Knesset elects Eisenkot ally as speaker",
     "Kahana wins 66\u201352.",
     "MIDDLE EAST", 35.0, 31.8),
    (9, "GLOBAL · CLIMATE",
     "COP31 enters final days split on fossil fuels",
     "Draft splits: phaseout, $120bn; Robinson: IPCC budget \u201cvital\u201d.",
     "GLOBAL", 30.7, 36.9),
    (10, "ASIA · POLITICS",
     "Mongolia\u2019s president says he will resign",
     "Ex-mayor alleges $25m rail link; president denies it.",
     "ASIA", 106.0, 47.9),
    (11, "EUROPE · MARKETS",
     "Deutsche Bank shares fall on leak reports",
     "Shares drop over 6% on leak reports.",
     "EUROPE", 8.7, 50.1),
    (12, "EUROPE · LABOUR",
     "French public-sector workers strike over pay",
     "146,000 march, govt says; CGT claims 500,000+.",
     "EUROPE", 2.35, 48.85),
]

# (number, headline, description, continent, lon, lat)
BRIEFS = [
    (13, "Suspected Russian jets enter Japanese airspace",
     "Tokyo scrambles fighters and protests.", "ASIA", 139.0, 36.0),
    (14, "Five EU states plan migrant return hub in Rwanda",
     "First transfers in 2027; HRW warns it risks violating "
     "international law.", "EUROPE", 30.0, -2.0),
    (15, "Xi and Carney agree new tariff cuts",
     "China cuts duties on C$400m of pork and seafood; Canada extends "
     "steel relief.", "AMERICAS", -106.0, 56.0),
    (16, "Netanyahu faces inquiry calls over election-day arrests",
     "His office is alleged to have tipped police against Arab party "
     "workers.", "MIDDLE EAST", 35.0, 31.8),
    (17, "UK sanctions eight settlement builders and Tzav 9",
     "Asset freezes target West Bank builders and a group accused of "
     "blocking Gaza aid.", "EUROPE", -1.5, 52.0),
    (18, "Depardieu drops appeal and accepts assault conviction",
     "Actor withdraws his challenge to a sexual assault conviction in "
     "a Paris court.", "EUROPE", 2.35, 48.85),
    (19, "Houthis advance as Yemeni forces retreat to defend Aden",
     "Forces pull back from the Red Sea coast to defend Aden.",
     "MIDDLE EAST", 45.0, 15.0),
    (20, "Yemen parliament lists Houthis as terrorists",
     "Law criminalises activities and financing; sent to al-Alimi to "
     "sign.", "MIDDLE EAST", 45.0, 15.0),
    (21, "Geneva talks on \u201ckiller robots\u201d open",
     "Delegates of 128 states meet at the UN to weigh a treaty banning "
     "lethal autonomous weapons.", "GLOBAL", 6.1, 46.2),
    (22, "US officials say Iran weighs a \u201cdirty bomb\u201d plot",
     "US intelligence says Iran is developing plans to target Trump "
     "aides; the claim is unconfirmed.", "MIDDLE EAST", 51.0, 32.0),
    (23, "US moves to close AI chip loophole",
     "Commerce acts to stop China renting US computing power.",
     "ASIA", -77.0, 39.0),
    (24, "Estonia to shut Russia border",
     "Crossings close 1 December after a foiled bomb plot on a drone "
     "plant.", "EUROPE", 25.0, 59.0),
    (25, "Pentagon fails audit for ninth year",
     "$4.8 trillion in assets could not be verified.", "AMERICAS",
     -77.0, 39.0),
    (26, "Third US carrier, USS Theodore Roosevelt, joins the Gulf force.",
     "", "MIDDLE EAST", 52.0, 26.0),
    (27, "Microsoft explains last week\u2019s global outage",
     "A latent defect knocked out 80% of servers.", "AMERICAS",
     -122.0, 47.5),
    (28, "White House orders agencies to get approval before testifying "
     "to Congress.", "", "AMERICAS", -77.0, 39.0),
    (29, "Thirteen babies born with measles in the US",
     "Cases reach their highest total since 1991.", "AMERICAS",
     -98.0, 39.0),
    (30, "Venezuela frees 39 political prisoners",
     "Freed after US-backed talks; 344 still held.", "AMERICAS",
     -66.0, 7.0),
    (31, "Australia sanctions Israeli settlers",
     "Canberra sanctions settler leader Daniella Weiss and a "
     "construction company.", "OCEANIA", 149.0, -35.0),
    (32, "Bus plunges into gorge in Uttarakhand",
     "At least eight killed as a bus falls 100 metres into a ravine; "
     "PM Modi sends condolences.", "ASIA", 79.0, 30.0),
    (33, "Guinea jails 224 in gold-mining crackdown",
     "22 ex-officials get two years, 202 miners three years over "
     "illegal Siguiri mining.", "AFRICA", -11.0, 10.0),
    (34, "Kenya: WFP aids families fleeing Moyale clashes",
     "Some 30,000 crossed from Ethiopia after inter-communal clashes; "
     "food aid began 11 Nov.", "AFRICA", 39.0, 3.5),
    (35, "Wall Street falls for a fourth day",
     "S&P 500 \u22121.03% to 7,340.53, its lowest close since July; "
     "Dow \u22121.64%; Salesforce \u22129.45%.", "AMERICAS", -74.0, 40.7),
    (36, "Bangladesh police tear-gas garment workers",
     "Workers want minimum wage raised to 30,000 taka from 12,500; "
     "500+ factories halted.", "ASIA", 90.4, 23.8),
    (37, "Serbia: student-led parliament first meets",
     "New assembly holds inaugural session in Belgrade; Student List "
     "won 140 of 250 seats.", "EUROPE", 20.5, 44.8),
    (38, "Moldova: airspace shut over Shahed-type drone",
     "Drone detected heading toward Chi\u0219in\u0103u; seven drones seen, "
     "five fell.", "EUROPE", 28.8, 47.0),
    (39, "Prague: two trains collide, 46 injured",
     "Head-on crash near main station; four seriously hurt.", "EUROPE",
     14.4, 50.1),
    (40, "Turkey takes Sozcu TV off air",
     "Authorities raid the pro-opposition channel, appoint a trustee; "
     "four executives detained.", "EUROPE", 32.9, 39.9),
    (41, "An-12 crash in Siberia kills all 19",
     "Military transport goes down in Kemerovo region; ministry cites "
     "technical malfunction.", "ASIA", 86.0, 55.0),
    (42, "Macron visit seals Malaysia partnership",
     "France and Malaysia upgrade ties; rare-earths curbs eased, "
     "defence and energy deals signed.", "ASIA", 101.7, 3.1),
    (43, "West Bank settlers kill woman, 72",
     "Settlers shoot Fadha Wadha near Jericho; 10 wounded, officials "
     "say.", "MIDDLE EAST", 35.4, 31.9),
    (44, "Gaza winter rains flood shelters",
     "UN: one day of rain damaged tens of thousands of tents; baby "
     "dies of hypothermia.", "MIDDLE EAST", 34.5, 31.5),
    (45, "Brazil beat Singapore 7-0, Vinicius hat-trick",
     "Vinicius scores three in 21 minutes in Brazil\u2019s final game "
     "of 2026.", "AMERICAS", -52.0, -10.0),
    (46, "Pope Leo XIV returns to Rome after tour",
     "Lands Tuesday after 12-day Uruguay\u2013Argentina\u2013Peru trip; "
     "speaks to press aboard flight.", "EUROPE", 12.5, 41.9),
    (47, "Apple outage; firm blames an update",
     "iCloud, App Store, Apple Pay hit; Apple says internal update, "
     "not a cyberattack.", "GLOBAL", -122.0, 37.3),
    (48, "Two giant black holes found in one early galaxy",
     "Nature: pair of quasars shone less than a billion years after "
     "the Big Bang.", "GLOBAL", 0.0, 0.0),
]


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap measured with PIL; returns list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def trunc(draw, text, fnt, max_w):
    """Truncate one line with an ellipsis so it fits max_w."""
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    ell = "\u2026"
    while text and draw.textlength(text + ell, font=fnt) > max_w:
        text = text[:-1]
    return text + ell


def ellipsize(draw, text, fnt, max_w):
    """Shorten one line so it ends with a trailing ellipsis that fits.

    Whole words are dropped first, so the line never ends mid-word.
    (The old trunc() path could never add an ellipsis here: wrapped
    lines already fit max_w, so it returned them unchanged.)
    """
    ell = "\u2026"
    while text and draw.textlength(text + ell, font=fnt) > max_w:
        if " " in text:
            text = text.rsplit(" ", 1)[0]
        else:
            text = text[:-1]
    return text + ell if text else ell


def draw_wrapped(draw, text, fnt, x, y, max_w, max_lines, fill, spacing=3,
                 ellipsis=False):
    lines = wrap(draw, text, fnt, max_w)[:max_lines]
    if len(wrap(draw, text, fnt, max_w)) > max_lines and lines:
        if ellipsis:
            lines[-1] = ellipsize(draw, lines[-1], fnt, max_w)
        else:
            lines[-1] = trunc(draw, lines[-1], fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def tag_color(tag):
    for key, col in TAG_COLORS.items():
        if tag.startswith(key):
            return col
    return (90, 90, 90)


def draw_illus(d, kind, x, y, w, h):
    """Original flat geometric illustration inside box (x, y, w, h)."""
    cx, cy = x + w // 2, y + h // 2
    if kind == 1:  # arched bridge, collapsed deck, drones, smoke
        d.rectangle([x, y, x + w, y + h], fill=SKY)
        d.rectangle([x, y + h * 2 // 3, x + w, y + h], fill=SEA)
        d.rectangle([x, y + h * 2 // 3, x + w, y + h * 2 // 3 + 3],
                    fill=(140, 175, 205))
        # Deck in two parts with a collapsed gap at centre-right.
        deck_y = y + h // 2
        d.line([x + 6, deck_y, x + w // 2 - 6, deck_y], fill=INK, width=5)
        d.line([x + w // 2 + 34, deck_y, x + w - 6, deck_y], fill=INK,
               width=5)
        d.line([x + w // 2 - 6, deck_y, x + w // 2 + 12, deck_y + 26],
               fill=INK, width=4)
        # Arch + towers.
        d.arc([x + 14, deck_y - 34, x + w - 50, deck_y + 6], 180, 360,
              fill=INK, width=4)
        for tx in (x + 22, x + w // 2 - 14, x + w - 26):
            d.line([tx, deck_y - 26, tx, deck_y], fill=INK, width=3)
        # Fire + smoke at the gap.
        d.polygon([(x + w // 2 + 2, deck_y), (x + w // 2 + 12, deck_y - 18),
                   (x + w // 2 + 22, deck_y)], fill=(230, 120, 30))
        d.polygon([(x + w // 2 + 10, deck_y), (x + w // 2 + 18, deck_y - 12),
                   (x + w // 2 + 28, deck_y)], fill=(245, 190, 60))
        d.ellipse([x + w // 2 - 2, y + 8, x + w // 2 + 30, y + 34],
                  fill=(110, 110, 110))
        d.ellipse([x + w // 2 + 16, y + 2, x + w // 2 + 44, y + 24],
                  fill=(140, 140, 140))
        d.ellipse([x + w // 2 + 34, y + 12, x + w // 2 + 56, y + 30],
                  fill=(110, 110, 110))
        # Three drone silhouettes above.
        for dx, dy in [(x + 22, y + 14), (x + 52, y + 8), (x + w - 34, y + 12)]:
            d.line([dx - 8, dy, dx + 8, dy], fill=INK, width=3)
            d.line([dx, dy - 3, dx, dy + 3], fill=INK, width=3)
            d.ellipse([dx - 2, dy - 2, dx + 2, dy + 2], fill=INK)
    elif kind == 2:  # Gulf map, radar sweep, dashed drone paths
        d.rectangle([x, y, x + w, y + h], fill=(240, 232, 214))
        # Gulf water.
        d.polygon([(x + 8, y + 18), (x + w - 8, y + 8), (x + w - 8, y + h - 8),
                   (x + w // 2 + 6, y + h - 8), (x + 8, y + h - 34)],
                  fill=SEA)
        d.line([x + 8, y + 18, x + w - 8, y + 8], fill=(120, 150, 180),
               width=2)
        # Bahrain island + Qeshm island.
        d.ellipse([x + w // 2 - 14, y + h // 2 - 6, x + w // 2 + 2,
                   y + h // 2 + 12], fill=(222, 205, 160),
                  outline=(150, 130, 95), width=1)
        d.polygon([(x + w - 52, y + h - 40), (x + w - 14, y + h - 46),
                   (x + w - 10, y + h - 26), (x + w - 44, y + h - 22)],
                  fill=(222, 205, 160), outline=(150, 130, 95))
        # Radar sweep arcs from Bahrain.
        bx, by = x + w // 2 - 6, y + h // 2 + 3
        for r in (12, 22, 32):
            d.arc([bx - r, by - r, bx + r, by + r], -60, 60,
                  fill=(176, 92, 20), width=2)
        d.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(176, 92, 20))
        # Dashed drone paths from Qeshm toward Bahrain.
        for k in range(6):
            t = k / 5.0
            px = int(x + w - 30 - t * (w - 30 - (bx + 8)))
            py = int(y + h - 32 - t * (h - 32 - (by - 4)))
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(178, 34, 34))
        d.ellipse([x + w - 34, y + h - 36, x + w - 26, y + h - 28],
                  fill=(178, 34, 34))
    elif kind == 3:  # skyline, river, two bridges, one broken, smoke
        d.rectangle([x, y, x + w, y + h], fill=(206, 222, 236))
        # City skyline behind.
        for sx, sw, sh in [(4, 18, 14), (26, 12, 20), (42, 20, 10),
                           (66, 12, 18), (120, 16, 12), (140, 14, 20),
                           (158, 18, 9)]:
            d.rectangle([x + sx, y + 16 - sh + 8, x + sx + sw, y + 24],
                        fill=(90, 105, 125))
        d.rectangle([x, y + 24, x + w, y + h], fill=(178, 205, 228))
        # River at the bottom.
        d.rectangle([x, y + h - 12, x + w, y + h], fill=SEA)
        # First bridge (left, intact) and second bridge (right, broken).
        d.line([x + 8, y + 26, x + w // 2 - 8, y + 26], fill=INK, width=3)
        d.line([x + w // 2 + 14, y + 26, x + w - 8, y + 26], fill=INK,
               width=3)
        d.line([x + w // 2 - 8, y + 26, x + w // 2 + 2, y + h - 12],
               fill=INK, width=3)
        d.line([x + w // 2 + 14, y + 26, x + w // 2 + 24, y + h - 12],
               fill=INK, width=3)
        # Smoke + flame at the break.
        d.ellipse([x + w // 2 - 2, y + 2, x + w // 2 + 16, y + 16],
                  fill=(110, 110, 110))
        d.ellipse([x + w // 2 + 10, y + 6, x + w // 2 + 24, y + 18],
                  fill=(140, 140, 140))
        d.polygon([(x + w // 2 + 2, y + 26), (x + w // 2 + 8, y + 16),
                   (x + w // 2 + 14, y + 26)], fill=(230, 120, 30))
    elif kind == 4:  # three flags on poles above a summit table
        d.rectangle([x, y, x + w, y + h], fill=(232, 238, 228))
        flags = [(x + 10, "us"), (x + w // 2 - 16, "cn"),
                 (x + w - 46, "ru")]
        for fx, code in flags:
            d.line([fx + 2, y + 4, fx + 2, y + h - 10], fill=(120, 90, 60),
                   width=2)
            if code == "us":  # stars and stripes
                for s in range(4):
                    d.rectangle([fx + 4, y + 4 + s * 4, fx + 32, y + 7 + s * 4],
                                fill=(178, 34, 34) if s % 2 == 0 else WHITE)
                d.rectangle([fx + 4, y + 4, fx + 15, y + 11], fill=(31, 78, 140))
            elif code == "cn":  # red, yellow stars
                d.rectangle([fx + 4, y + 4, fx + 32, y + 20], fill=(178, 34, 34))
                d.ellipse([fx + 7, y + 7, fx + 12, y + 12], fill=(245, 200, 40))
                for sx, sy in [(16, 6), (20, 10), (16, 14), (12, 11)]:
                    d.ellipse([fx + sx, y + sy, fx + sx + 3, y + sy + 3],
                              fill=(245, 200, 40))
            else:  # white-blue-red tricolour
                d.rectangle([fx + 4, y + 4, fx + 32, y + 9], fill=WHITE)
                d.rectangle([fx + 4, y + 9, fx + 32, y + 14], fill=(31, 78, 140))
                d.rectangle([fx + 4, y + 14, fx + 32, y + 20],
                            fill=(178, 34, 34))
        d.rectangle([x + 8, y + h - 10, x + w - 8, y + h - 4],
                    fill=(120, 70, 40))
    elif kind == 5:  # virus + syringe
        d.rectangle([x, y, x + w, y + h], fill=(240, 230, 245))
        vx, vy = x + 52, y + h // 2 + 2
        for ang in range(0, 360, 40):
            r = math.radians(ang)
            x1 = vx + int(18 * math.cos(r))
            y1 = vy + int(18 * math.sin(r))
            x2 = vx + int(28 * math.cos(r))
            y2 = vy + int(28 * math.sin(r))
            d.line([x1, y1, x2, y2], fill=(110, 60, 140), width=3)
            d.ellipse([x2 - 4, y2 - 4, x2 + 4, y2 + 4], fill=(110, 60, 140))
        d.ellipse([vx - 18, vy - 18, vx + 18, vy + 18], fill=(150, 90, 180))
        d.ellipse([vx - 8, vy - 8, vx + 8, vy + 8], fill=(110, 60, 140))
        # Syringe, diagonal across the right side.
        d.line([x + w - 16, y + 6, x + w - 52, y + h - 8], fill=(90, 90, 90),
               width=3)
        d.line([x + w - 52, y + h - 8, x + w - 58, y + h - 2],
               fill=(90, 90, 90), width=2)
        d.rectangle([x + w - 40, y + 2, x + w - 22, y + 16], fill=WHITE,
                    outline=(90, 90, 90), width=2)
        d.rectangle([x + w - 36, y + 5, x + w - 30, y + 13],
                    fill=(90, 140, 200))
        d.line([x + w - 40, y + 16, x + w - 52, y + h - 8], fill=(90, 90, 90),
               width=5)
    elif kind == 6:  # DR Congo outline + rising chart + virus dots
        d.rectangle([x, y, x + w, y + h], fill=(228, 240, 230))
        # Simplified DR Congo outline.
        d.polygon([(x + 14, y + 10), (x + 66, y + 6), (x + 78, y + 16),
                   (x + 70, y + 30), (x + 52, y + 26), (x + 46, y + 36),
                   (x + 28, y + 34), (x + 12, y + 22)],
                  fill=(120, 190, 120), outline=(34, 120, 60), width=2)
        d.ellipse([x + 34, y + 14, x + 40, y + 20], fill=(178, 34, 34))
        d.ellipse([x + 52, y + 18, x + 58, y + 24], fill=(178, 34, 34))
        # Rising bars on the right.
        bars = [8, 14, 20, 28]
        for i, bh in enumerate(bars):
            bx = x + 96 + i * 18
            d.rectangle([bx, y + h - 6 - bh, bx + 12, y + h - 6],
                        fill=(34, 120, 60))
        d.line([x + 92, y + h - 6, x + w - 6, y + h - 6], fill=INK, width=2)
    elif kind == 7:  # handshake + mineral crystals
        d.rectangle([x, y, x + w, y + h], fill=(238, 236, 224))
        # Forearms meeting in a handshake at centre.
        d.polygon([(x + 4, y + 12), (x + 78, y + 12), (x + 70, y + 26),
                   (x + 4, y + 26)], fill=(31, 78, 140))
        d.polygon([(x + w - 4, y + 12), (x + 96, y + 12), (x + 104, y + 26),
                   (x + w - 4, y + 26)], fill=(90, 90, 90))
        d.ellipse([x + 68, y + 8, x + 106, y + 30], fill=(220, 180, 140))
        for fx in (76, 84, 92):
            d.arc([fx, y + 10, fx + 12, y + 28], 90, 270,
                  fill=(190, 140, 100), width=2)
        # Faceted mineral crystals below.
        for cx0, ch, col in [(x + 22, 12, (40, 120, 140)),
                             (x + 46, 16, (30, 90, 160)),
                             (x + 74, 11, (60, 140, 120)),
                             (x + 128, 14, (40, 120, 140))]:
            d.polygon([(cx0, y + h - 4), (cx0 + 4, y + h - 4 - ch),
                       (cx0 + 12, y + h - 4 - ch - 3),
                       (cx0 + 16, y + h - 4)], fill=col)
            d.line([cx0 + 8, y + h - 4 - ch - 1, cx0 + 8, y + h - 6],
                   fill=WHITE, width=1)
        d.ellipse([x + w - 26, y + h - 20, x + w - 8, y + h - 4], fill=GOLD,
                  outline=(150, 110, 20), width=1)
    elif kind == 8:  # vote bars 66 vs 52 + gavel on its block
        d.rectangle([x, y, x + w, y + h], fill=(240, 234, 220))
        d.rectangle([x + 8, y + 4, x + 96, y + 13], fill=(31, 78, 140))
        d.text((x + 12, y + 4), "66", font=F_BOLD(10), fill=WHITE)
        d.rectangle([x + 8, y + 16, x + 80, y + 25], fill=(120, 120, 120))
        d.text((x + 12, y + 16), "52", font=F_BOLD(10), fill=WHITE)
        # Gavel: angled head + handle, striking the block.
        d.polygon([(x + 128, y + 6), (x + 158, y + 16), (x + 152, y + 26),
                   (x + 122, y + 16)], fill=(120, 70, 40))
        d.polygon([(x + 136, y + 12), (x + 142, y + 8), (x + 156, y + 18),
                   (x + 150, y + 22)], fill=(90, 50, 20))
        d.line([x + 140, y + 20, x + 128, y + 36], fill=(90, 50, 20), width=4)
        d.rectangle([x + 118, y + 34, x + 146, y + 38], fill=(120, 70, 40))
    elif kind == 9:  # globe split: oil drop vs leaf
        d.rectangle([x, y, x + w, y + h], fill=(226, 238, 240))
        gx, gy = x + 62, y + h // 2
        d.ellipse([gx - 26, gy - 18, gx + 26, gy + 18], fill=(90, 140, 200))
        # Left half: dark oil; right half: green leaf.
        d.pieslice([gx - 26, gy - 18, gx + 26, gy + 18], 90, 270,
                   fill=(40, 50, 70))
        d.pieslice([gx - 26, gy - 18, gx + 26, gy + 18], 270, 90,
                   fill=(60, 160, 80))
        d.ellipse([gx - 26, gy - 18, gx + 26, gy + 18],
                  outline=(30, 80, 140), width=2)
        # Oil drop on the dark half.
        d.ellipse([gx - 18, gy - 6, gx - 8, gy + 4], fill=(20, 25, 35))
        d.polygon([(gx - 18, gy - 4), (gx - 13, gy - 14), (gx - 8, gy - 4)],
                  fill=(20, 25, 35))
        # Leaf on the green half.
        d.ellipse([gx + 8, gy - 8, gx + 20, gy + 8], fill=(230, 245, 220),
                  outline=(30, 100, 40), width=1)
        d.line([gx + 9, gy + 6, gx + 19, gy - 6], fill=(30, 100, 40), width=1)
        # Small oil barrel + sprout at the sides.
        d.rectangle([x + 6, y + h - 16, x + 22, y + h - 4], fill=(40, 50, 70))
        d.rectangle([x + 6, y + h - 13, x + 22, y + h - 12], fill=(90, 100, 115),
                    width=1)
        d.line([x + w - 14, y + h - 4, x + w - 14, y + h - 16],
               fill=(40, 120, 60), width=2)
        d.ellipse([x + w - 20, y + h - 20, x + w - 14, y + h - 14],
                  fill=(60, 160, 80))
        d.ellipse([x + w - 14, y + h - 20, x + w - 8, y + h - 14],
                  fill=(60, 160, 80))
    elif kind == 10:  # podium + railway + $25m tag
        d.rectangle([x, y, x + w, y + h], fill=(236, 232, 220))
        # Railway diagonal at the back.
        d.line([x + 70, y + h - 6, x + w - 8, y + 4], fill=INK, width=3)
        d.line([x + 92, y + h - 6, x + w - 8, y + 14], fill=INK, width=3)
        for i in range(3):
            t = i / 2.0
            sx = int(x + 82 + t * (w - 110))
            sy = int(y + h - 8 - t * (h - 18))
            d.line([sx - 8, sy + 3, sx + 8, sy - 3], fill=INK, width=2)
        # Speaker silhouette at a podium.
        d.ellipse([x + 26, y + 4, x + 40, y + 18], fill=(60, 60, 70))
        d.polygon([(x + 18, y + 36), (x + 48, y + 36), (x + 42, y + 18),
                   (x + 24, y + 18)], fill=(31, 78, 140))
        d.line([x + 40, y + 6, x + 48, y + 2], fill=INK, width=2)
        d.ellipse([x + 47, y + 1, x + 51, y + 5], fill=INK)
        d.rectangle([x + 10, y + 36, x + 56, y + h - 4], fill=(90, 60, 40))
        # "$25m" tag (verified figure).
        d.rectangle([x + w - 58, y + 4, x + w - 6, y + 18], fill=GOLD,
                    outline=(150, 110, 20), width=1)
        d.text((x + w - 55, y + 5), "$25m", font=F_BOLD(11), fill=INK)
    elif kind == 11:  # bank building + falling chart
        d.rectangle([x, y, x + w, y + h], fill=(244, 228, 228))
        # Classical bank: pediment + columns.
        d.polygon([(x + 12, y + 12), (x + 62, y + 12), (x + 37, y + 2)],
                  fill=(140, 150, 170))
        for cx0 in (16, 30, 44):
            d.rectangle([x + cx0, y + 14, x + cx0 + 7, y + h - 6],
                        fill=(170, 180, 195))
        d.rectangle([x + 10, y + h - 6, x + 64, y + h - 3], fill=(140, 150, 170))
        # Falling bars + red trend arrow on the right.
        bars = [26, 20, 13, 6]
        for i, bh in enumerate(bars):
            bx = x + 84 + i * 22
            d.rectangle([bx, y + h - 8 - bh, bx + 14, y + h - 8],
                        fill=(178, 34, 34))
        d.line([x + 84, y + 6, x + w - 12, y + h - 14], fill=(120, 0, 0),
               width=3)
        d.polygon([(x + w - 12, y + h - 14), (x + w - 26, y + h - 16),
                   (x + w - 16, y + h - 2)], fill=(120, 0, 0))
    else:  # 12: crowd with placards, PAY banner
        d.rectangle([x, y, x + w, y + h], fill=(232, 236, 244))
        # Banner held high on two poles.
        d.line([x + 16, y + 4, x + 16, y + 18], fill=(90, 60, 40), width=2)
        d.line([x + w - 16, y + 4, x + w - 16, y + 18], fill=(90, 60, 40),
               width=2)
        d.rectangle([x + 16, y + 4, x + w - 16, y + 16], fill=NAVY)
        d.text((x + w // 2 - 12, y + 5), "PAY", font=F_BOLD(10), fill=WHITE)
        # Marching crowd: heads + shoulders, varied tones.
        tones = [(220, 180, 140), (200, 150, 110), (235, 200, 165),
                 (180, 130, 95), (220, 180, 140), (200, 150, 110)]
        shirts = [(31, 78, 140), (178, 34, 34), (34, 120, 60),
                  (110, 60, 140), (176, 92, 20), (31, 78, 140)]
        for i in range(6):
            hx = x + 20 + i * (w - 40) // 5
            hy = y + 20
            d.ellipse([hx - 7, hy, hx + 7, hy + 12], fill=tones[i])
            d.rectangle([hx - 11, hy + 13, hx + 11, y + h - 4],
                        fill=shirts[i])
        # Small placard on a stick at the right.
        d.line([x + w - 34, y + 18, x + w - 34, y + h - 6], fill=(90, 60, 40),
               width=2)
        d.rectangle([x + w - 48, y + 18, x + w - 20, y + 28], fill=WHITE,
                    outline=INK, width=1)


def draw_illus_box(img, kind, x, y, w, h):
    """Draw an illustration clipped exactly to its box."""
    from PIL import Image as _Image
    from PIL import ImageDraw as _Draw
    layer = _Image.new("RGB", (w, h), PAPER)
    ld = _Draw.Draw(layer)
    draw_illus(ld, kind, 0, 0, w, h)
    img.paste(layer, (x, y))


def lonlat_to_xy(lon, lat, bx, by, bw, bh):
    # Equirectangular over lon -170..190, lat -58..84.
    fx = (lon + 170.0) / 360.0
    fy = (84.0 - lat) / 142.0
    return bx + int(fx * bw), by + int(fy * bh)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Header ----
    d.rectangle([0, 0, W, 86], fill=NAVY)
    d.text((14, 10), "THE DAY IN WORLD NEWS", font=F_BOLD(13), fill=GOLD)
    d.text((14, 28), "Tuesday 17 November 2026", font=F_SERIF(44), fill=WHITE)
    cnt = "48 STORIES \u00b7 6 CONTINENTS \u00b7 ONE DAY"
    d.text((W - 14 - d.textlength(cnt, font=F_BOLD(13)), 12), cnt,
           font=F_BOLD(13), fill=GOLD)
    d.rectangle([0, 86, W, 90], fill=GOLD)

    # ---- Heroes (panels 1-2) ----
    hero_y, hero_h = 96, 130
    hero_w = 493
    for i, m in enumerate(MAINS[:2]):
        num, tag, head, desc = m[0], m[1], m[2], m[3]
        x = 14 + i * (hero_w + 10)
        d.rectangle([x, hero_y, x + hero_w, hero_y + hero_h], fill=WHITE,
                    outline=RULE, width=1)
        d.rectangle([x, hero_y, x + hero_w, hero_y + 4],
                    fill=tag_color(tag))
        draw_illus_box(img, num, x + 10, hero_y + 14, 150, hero_h - 24)
        tx = x + 170
        tw = hero_w - 180
        d.text((tx, hero_y + 12), f"{num}  {tag}", font=F_BOLD(11),
               fill=tag_color(tag))
        draw_wrapped(d, head, F_BOLD(19), tx, hero_y + 32, tw, 3, INK, 2)
        draw_wrapped(d, desc, F_REG(12), tx, hero_y + 32 + 3 * 21, tw, 2,
                     MUTED, 2)

    # ---- Grid rows (panels 3-7, 8-12) ----
    grid_xs = [14, 215, 416, 617, 818]
    grid_w = 192
    for row, (gy, chunk) in enumerate([(234, MAINS[2:7]), (386, MAINS[7:12])]):
        for j, m in enumerate(chunk):
            num, tag, head, desc = m[0], m[1], m[2], m[3]
            x = grid_xs[j]
            d.rectangle([x, gy, x + grid_w, gy + 144], fill=WHITE,
                        outline=RULE, width=1)
            d.rectangle([x, gy, x + grid_w, gy + 4], fill=tag_color(tag))
            draw_illus_box(img, num, x + 6, gy + 10, grid_w - 12, 40)
            ty = gy + 54
            d.text((x + 8, ty), f"{num}  {tag}", font=F_BOLD(10),
                   fill=tag_color(tag))
            hlines = len(wrap(d, head, F_BOLD(15), grid_w - 16))
            hy_end = draw_wrapped(d, head, F_BOLD(15), x + 8, ty + 16,
                                  grid_w - 16, 3, INK, 0)
            # 144px panels fit two description lines even under a
            # three-line headline (headline ends gy+115, desc ends gy+141).
            draw_wrapped(d, desc, F_REG(11), x + 8, hy_end + 2,
                         grid_w - 16, 2, MUTED, 1, ellipsis=True)

    # ---- Bottom: map column ----
    d.text((14, 536), "WHERE IT HAPPENED", font=F_BOLD(13), fill=INK)
    d.line([14, 554, 304, 554], fill=RULE, width=1)
    mx, my, mw, mh = 14, 560, 290, 200
    d.rectangle([mx, my, mx + mw, my + mh], fill=(238, 232, 214),
                outline=RULE, width=1)
    # Land masses, drawn to read as the real continents.
    land = (222, 210, 178)
    d.polygon([(mx + 2, my + 25), (mx + 12, my + 18), (mx + 24, my + 20),
               (mx + 36, my + 20), (mx + 48, my + 23), (mx + 60, my + 21),
               (mx + 69, my + 25), (mx + 74, my + 31), (mx + 82, my + 37),
               (mx + 89, my + 41), (mx + 94, my + 49), (mx + 93, my + 52),
               (mx + 85, my + 56), (mx + 81, my + 59), (mx + 77, my + 62),
               (mx + 76, my + 69), (mx + 73, my + 73), (mx + 72, my + 83),
               (mx + 69, my + 76), (mx + 65, my + 76), (mx + 62, my + 76),
               (mx + 59, my + 82), (mx + 59, my + 96), (mx + 63, my + 97),
               (mx + 68, my + 101), (mx + 70, my + 106), (mx + 75, my + 107),
               (mx + 73, my + 100), (mx + 67, my + 89), (mx + 52, my + 90),
               (mx + 48, my + 85), (mx + 45, my + 77), (mx + 40, my + 70),
               (mx + 36, my + 62), (mx + 36, my + 49), (mx + 32, my + 42),
               (mx + 28, my + 37), (mx + 24, my + 34), (mx + 12, my + 34),
               (mx + 4, my + 34)], fill=land)  # North America
    d.polygon([(mx + 90, my + 28), (mx + 95, my + 23), (mx + 101, my + 20),
               (mx + 105, my + 20), (mx + 111, my + 23), (mx + 117, my + 20),
               (mx + 119, my + 20), (mx + 113, my + 27), (mx + 105, my + 34),
               (mx + 97, my + 34), (mx + 92, my + 34)], fill=land)  # Greenland
    d.polygon([(mx + 75, my + 107), (mx + 79, my + 103), (mx + 85, my + 104),
               (mx + 89, my + 107), (mx + 95, my + 111), (mx + 97, my + 118),
               (mx + 102, my + 123), (mx + 109, my + 130), (mx + 109, my + 140),
               (mx + 104, my + 147), (mx + 103, my + 151), (mx + 99, my + 158),
               (mx + 96, my + 165), (mx + 91, my + 172), (mx + 88, my + 176),
               (mx + 84, my + 182), (mx + 82, my + 189), (mx + 81, my + 194),
               (mx + 78, my + 189), (mx + 78, my + 180), (mx + 78, my + 170),
               (mx + 79, my + 160), (mx + 81, my + 146), (mx + 81, my + 139),
               (mx + 77, my + 135), (mx + 73, my + 127), (mx + 72, my + 123),
               (mx + 73, my + 116)], fill=land)  # South America
    d.polygon([(mx + 129, my + 68), (mx + 130, my + 58), (mx + 134, my + 51),
               (mx + 136, my + 48), (mx + 139, my + 46), (mx + 143, my + 41),
               (mx + 143, my + 37), (mx + 147, my + 39), (mx + 152, my + 39),
               (mx + 154, my + 37), (mx + 160, my + 34), (mx + 161, my + 25),
               (mx + 160, my + 18), (mx + 153, my + 20), (mx + 147, my + 27),
               (mx + 141, my + 34), (mx + 137, my + 41), (mx + 133, my + 48),
               (mx + 130, my + 56), (mx + 130, my + 66), (mx + 132, my + 68),
               (mx + 137, my + 64), (mx + 139, my + 59), (mx + 143, my + 56),
               (mx + 147, my + 56), (mx + 148, my + 62), (mx + 153, my + 59),
               (mx + 156, my + 62), (mx + 158, my + 65), (mx + 161, my + 68),
               (mx + 159, my + 69), (mx + 155, my + 66), (mx + 150, my + 65),
               (mx + 147, my + 59), (mx + 143, my + 56)], fill=land)  # Europe
    d.polygon([(mx + 133, my + 48), (mx + 135, my + 44), (mx + 133, my + 40),
               (mx + 135, my + 37), (mx + 136, my + 38), (mx + 137, my + 44),
               (mx + 135, my + 48)], fill=land)  # UK
    d.polygon([(mx + 123, my + 97), (mx + 123, my + 90), (mx + 126, my + 80),
               (mx + 129, my + 75), (mx + 132, my + 70), (mx + 137, my + 68),
               (mx + 145, my + 66), (mx + 146, my + 70), (mx + 153, my + 73),
               (mx + 157, my + 73), (mx + 161, my + 75), (mx + 163, my + 75),
               (mx + 165, my + 79), (mx + 167, my + 87), (mx + 169, my + 93),
               (mx + 170, my + 101), (mx + 172, my + 103), (mx + 176, my + 103),
               (mx + 178, my + 104), (mx + 178, my + 116), (mx + 176, my + 121),
               (mx + 171, my + 126), (mx + 170, my + 133), (mx + 170, my + 140),
               (mx + 168, my + 147), (mx + 165, my + 152), (mx + 163, my + 158),
               (mx + 160, my + 165), (mx + 157, my + 166), (mx + 153, my + 168),
               (mx + 150, my + 166), (mx + 148, my + 159), (mx + 147, my + 147),
               (mx + 147, my + 135), (mx + 148, my + 130), (mx + 144, my + 120),
               (mx + 144, my + 113), (mx + 140, my + 110), (mx + 135, my + 111),
               (mx + 131, my + 111), (mx + 127, my + 107), (mx + 123, my + 101)],
              fill=land)  # Africa
    d.polygon([(mx + 161, my + 68), (mx + 166, my + 68), (mx + 171, my + 65),
               (mx + 176, my + 64), (mx + 181, my + 65), (mx + 184, my + 65),
               (mx + 187, my + 66), (mx + 190, my + 68), (mx + 194, my + 69),
               (mx + 197, my + 73), (mx + 200, my + 76), (mx + 203, my + 79),
               (mx + 207, my + 82), (mx + 210, my + 83), (mx + 211, my + 87),
               (mx + 214, my + 90), (mx + 216, my + 93), (mx + 218, my + 97),
               (mx + 219, my + 102), (mx + 222, my + 105), (mx + 224, my + 105),
               (mx + 225, my + 100), (mx + 225, my + 93), (mx + 224, my + 87),
               (mx + 223, my + 79), (mx + 221, my + 73), (mx + 219, my + 68),
               (mx + 218, my + 62), (mx + 216, my + 56), (mx + 215, my + 51),
               (mx + 213, my + 45), (mx + 211, my + 39), (mx + 210, my + 34),
               (mx + 208, my + 28), (mx + 207, my + 23), (mx + 205, my + 17),
               (mx + 202, my + 15), (mx + 198, my + 17), (mx + 194, my + 17),
               (mx + 190, my + 20), (mx + 185, my + 21), (mx + 181, my + 21),
               (mx + 177, my + 23), (mx + 173, my + 23), (mx + 169, my + 23),
               (mx + 165, my + 24), (mx + 163, my + 25), (mx + 161, my + 31),
               (mx + 160, my + 34), (mx + 161, my + 37), (mx + 160, my + 39),
               (mx + 158, my + 42), (mx + 157, my + 45), (mx + 155, my + 48),
               (mx + 153, my + 51), (mx + 152, my + 54), (mx + 150, my + 56),
               (mx + 148, my + 56), (mx + 150, my + 59), (mx + 153, my + 62),
               (mx + 157, my + 65), (mx + 160, my + 65)],
              fill=land)  # Asia
    d.polygon([(mx + 192, my + 85), (mx + 195, my + 90), (mx + 199, my + 97),
               (mx + 202, my + 104), (mx + 202, my + 109), (mx + 199, my + 107),
               (mx + 197, my + 100), (mx + 194, my + 90)], fill=land)  # India
    d.polygon([(mx + 216, my + 96), (mx + 218, my + 102), (mx + 219, my + 107),
               (mx + 221, my + 110), (mx + 219, my + 116), (mx + 218, my + 113),
               (mx + 216, my + 107), (mx + 215, my + 101)], fill=land)  # SE Asia
    d.polygon([(mx + 219, my + 115), (mx + 220, my + 117), (mx + 221, my + 116),
               (mx + 219, my + 110)], fill=land)  # Malay Peninsula
    d.polygon([(mx + 251, my + 56), (mx + 253, my + 56), (mx + 252, my + 59),
               (mx + 250, my + 59)], fill=land)  # Hokkaido
    d.polygon([(mx + 242, my + 70), (mx + 246, my + 69), (mx + 250, my + 65),
               (mx + 251, my + 63), (mx + 249, my + 66), (mx + 244, my + 70)],
              fill=land)  # Honshu
    d.polygon([(mx + 242, my + 74), (mx + 243, my + 72), (mx + 241, my + 73)],
              fill=land)  # Kyushu
    d.polygon([(mx + 228, my + 149), (mx + 230, my + 163), (mx + 232, my + 168),
               (mx + 237, my + 165), (mx + 242, my + 163), (mx + 247, my + 168),
               (mx + 250, my + 172), (mx + 254, my + 172), (mx + 258, my + 171),
               (mx + 261, my + 163), (mx + 261, my + 156), (mx + 258, my + 150),
               (mx + 255, my + 145), (mx + 252, my + 140), (mx + 252, my + 134),
               (mx + 248, my + 135), (mx + 244, my + 135), (mx + 239, my + 137),
               (mx + 234, my + 146)], fill=land)  # Australia
    d.polygon([(mx + 243, my + 120), (mx + 247, my + 121), (mx + 251, my + 123),
               (mx + 255, my + 127), (mx + 258, my + 131), (mx + 255, my + 130),
               (mx + 251, my + 130), (mx + 247, my + 127), (mx + 244, my + 124)],
              fill=land)  # New Guinea
    d.polygon([(mx + 273, my + 176), (mx + 274, my + 178), (mx + 277, my + 172),
               (mx + 279, my + 172), (mx + 277, my + 176), (mx + 274, my + 180),
               (mx + 273, my + 182), (mx + 271, my + 178)], fill=land)  # NZ
    # Continent labels (placed clear of the numbered dots).
    lab = F_BOLD(8)
    for lx, ly, txt in [(24, 6, "N. AMERICA"), (70, 152, "S. AMERICA"),
                        (88, 12, "EUROPE"), (150, 156, "AFRICA"),
                        (240, 40, "ASIA"), (222, 182, "OCEANIA")]:
        d.text((mx + lx, my + ly), txt, font=lab, fill=(140, 130, 105))
    # GLOBAL box (bottom-left): placeless stories only (lon/lat 0,0).
    d.rounded_rectangle([mx + 8, my + mh - 32, mx + 104, my + mh - 4],
                        radius=8, fill=WHITE, outline=RULE, width=1)
    d.text((mx + 16, my + mh - 24), "GLOBAL", font=F_BOLD(10),
           fill=TAG_COLORS["GLOBAL"])
    gx, gy = mx + 82, my + mh - 18
    d.ellipse([gx - 9, gy - 9, gx + 9, gy + 9], fill=TAG_COLORS["GLOBAL"],
              outline=WHITE, width=2)
    d.text((gx - 6, gy - 6), "48", font=F_BOLD(10), fill=WHITE)
    # Numbered dots for every located story (nudged apart in clusters).
    nudges = {1: (12, 5), 2: (43, -9), 3: (22, -17), 4: (13, -17),
              5: (0, 0), 6: (-9, -7), 7: (8, 6), 8: (17, 63), 9: (-23, 26),
              10: (0, 0), 11: (-18, -16), 12: (-15, 6), 13: (9, -10),
              14: (-23, 11), 15: (2, -3), 16: (43, 56), 17: (-28, -5),
              18: (-25, 22), 19: (-27, 55), 20: (27, 55), 21: (16, -3),
              22: (22, -7), 23: (1, -17), 24: (-13, -11), 25: (-8, 29),
              26: (47, 10), 27: (0, 0), 28: (10, 17), 29: (-12, 15),
              30: (0, 0), 31: (0, 0), 32: (-16, 14), 33: (-22, 12),
              34: (-6, 25), 35: (19, -1), 36: (-1, 22), 37: (-10, 13),
              38: (36, -8), 39: (15, -24), 40: (-2, 18), 41: (8, -14),
              42: (10, 9), 43: (6, 35), 44: (26, 43), 45: (0, 0),
              46: (-27, 41), 47: (-13, 6)}

    def num_dot(num, lon, lat, region):
        bx, by = lonlat_to_xy(lon, lat, mx, my, mw, mh)
        dx, dy = nudges.get(num, (0, 0))
        bx, by = bx + dx, by + dy
        col = TAG_COLORS.get(region, (90, 90, 90))
        d.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=col,
                  outline=WHITE, width=2)
        label = str(num)
        lw = d.textlength(label, font=F_BOLD(10))
        d.text((bx - lw / 2, by - 7), label, font=F_BOLD(10), fill=WHITE)

    # Brief dots first (story 48 is placeless: lives in the GLOBAL box).
    for b in BRIEFS:
        if b[4] == 0.0 and b[5] == 0.0:
            continue
        num_dot(b[0], b[4], b[5], b[3])
    # Numbered main dots (drawn last, on top).
    for m in MAINS:
        num_dot(m[0], m[5], m[6], m[4])
    # Legend: colour key with dots (two rows, like the reference).
    ly = my + mh + 12
    for dx0, name in [(16, "EUROPE"), (82, "MIDDLE EAST"), (175, "ASIA"),
                      (223, "AFRICA")]:
        d.ellipse([dx0, ly + 1, dx0 + 9, ly + 10], fill=TAG_COLORS[name])
        d.text((dx0 + 13, ly), name, font=F_BOLD(10), fill=INK)
    ly += 16
    for dx0, name in [(16, "AMERICAS"), (94, "OCEANIA"), (167, "GLOBAL")]:
        d.ellipse([dx0, ly + 1, dx0 + 9, ly + 10], fill=TAG_COLORS[name])
        d.text((dx0 + 13, ly), name, font=F_BOLD(10), fill=INK)
    d.text((14, ly + 16), "Numbered dots = all 48 stories.",
           font=F_REG(10), fill=MUTED)
    # Region tally, counted from the data above.
    counts = {}
    for m in MAINS:
        counts[m[4]] = counts.get(m[4], 0) + 1
    for b in BRIEFS:
        counts[b[3]] = counts.get(b[3], 0) + 1
    ty = ly + 30
    d.text((14, ty), "STORIES BY REGION", font=F_BOLD(12), fill=INK)
    d.line([14, ty + 18, 304, ty + 18], fill=RULE, width=1)
    ty += 24
    for name in ["EUROPE", "MIDDLE EAST", "ASIA", "AFRICA", "AMERICAS",
                 "OCEANIA", "GLOBAL"]:
        n = counts.get(name, 0)
        d.ellipse([16, ty + 2, 26, ty + 12], fill=TAG_COLORS[name])
        d.text((32, ty), name.title(), font=F_BOLD(12), fill=INK)
        d.text((290, ty), str(n), font=F_BOLD(12), fill=INK)
        ty += 18
    d.text((14, ty + 4), "48 stories in total, all numbered on the map.",
           font=F_REG(11), fill=MUTED)

    # ---- Bottom right: briefs ----
    bx0, bw_col = 312, 344
    d.text((bx0, 536), "ALSO ON TUESDAY 17 NOVEMBER", font=F_BOLD(13),
           fill=INK)
    d.line([bx0, 554, 1010, 554], fill=RULE, width=1)
    row_h = 24
    for idx, b in enumerate(BRIEFS):
        num, head, desc = b[0], b[1], b[2]
        col = idx // 18
        row = idx % 18
        x = bx0 + col * (bw_col + 10)
        y = 562 + row * row_h
        d.ellipse([x, y + 1, x + 16, y + 17], fill=NAVY)
        label = str(num)
        lw = d.textlength(label, font=F_BOLD(9))
        d.text((x + 8 - lw / 2, y + 3), label, font=F_BOLD(9), fill=WHITE)
        tx = x + 22
        tw = bw_col - 22
        if desc:
            d.text((tx, y), trunc(d, head, F_BOLD(12), tw), font=F_BOLD(12),
                   fill=INK)
            d.text((tx, y + 13), trunc(d, desc, F_REG(11), tw),
                   font=F_REG(11), fill=MUTED)
        else:
            draw_wrapped(d, head, F_BOLD(12), tx, y, tw, 2, INK, 0)

    # ---- Footer ----
    d.text((W // 2 - d.textlength(
        "Every story was reported on Tuesday 17 November 2026; disputed "
        "claims are attributed. Sources: Reuters, AP, AFP, BBC, Al Jazeera, "
        "France 24, UN News and others. Original drawings.",
        font=F_REG(10)) / 2, 1012),
        "Every story was reported on Tuesday 17 November 2026; disputed "
        "claims are attributed. Sources: Reuters, AP, AFP, BBC, Al Jazeera, "
        "France 24, UN News and others. Original drawings.",
        font=F_REG(10), fill=MUTED)

    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out, exist_ok=True)
    img.save(os.path.join(out, "entry.png"), "PNG", optimize=True)


if __name__ == "__main__":
    build()
