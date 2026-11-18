"""News front page: Tuesday 17 November 2026. 48 verified stories.

Draws a 1024x1024 newspaper front page with PIL only. Deterministic:
no network, no randomness, no timestamps, fixed data and fonts.
"""
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
     "Both bridges hit; utilities cut. 2026 toll tops any since 2022.",
     "EUROPE", 30.5, 50.4),
    (4, "ASIA · DIPLOMACY",
     "APEC leaders gather ahead of Trump\u2013Xi\u2013Putin summit",
     "3-way summit Thu, Shenzhen.",
     "ASIA", 114.0, 22.5),
    (5, "AMERICAS · HEALTH",
     "US, Mexico, Bolivia lose measles-free status",
     "US loses measles-free status.",
     "AMERICAS", -98.0, 39.0),
    (6, "AFRICA · HEALTH",
     "Ebola outbreak in DR Congo more than doubles",
     "11,000+ cases, 5,400 deaths.",
     "AFRICA", 23.0, -2.0),
    (7, "ASIA · DIPLOMACY",
     "Trump announces critical-minerals deals in Manila",
     "Quad signs minerals deals.",
     "ASIA", 121.0, 14.6),
    (8, "MIDDLE EAST · POLITICS",
     "Knesset elects Eisenkot ally as speaker",
     "Kahana wins 66\u201352.",
     "MIDDLE EAST", 35.0, 31.8),
    (9, "GLOBAL · CLIMATE",
     "COP31 enters final days split on fossil fuels",
     "Draft splits on fossil phaseout.",
     "GLOBAL", 30.7, 36.9),
    (10, "ASIA · POLITICS",
     "Mongolia\u2019s president says he will resign",
     "President denies taking $25m.",
     "ASIA", 106.0, 47.9),
    (11, "EUROPE · MARKETS",
     "Deutsche Bank shares fall on leak reports",
     "Shares fall 6% on leak reports.",
     "EUROPE", 8.7, 50.1),
    (12, "EUROPE · LABOUR",
     "French public-sector workers strike over pay",
     "146,000 march; CGT: 500k+.",
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
    if kind == 1:  # bridge over strait, smoke
        d.rectangle([x, y, x + w, y + h], fill=SKY)
        d.rectangle([x, y + h * 3 // 5, x + w, y + h], fill=SEA)
        d.line([x + 6, y + h // 2, x + w - 6, y + h // 2], fill=INK, width=4)
        d.arc([x + w // 4, y + h // 6, x + 3 * w // 4, y + h // 2 + 8],
              180, 360, fill=INK, width=4)
        for i in range(5):
            px = x + 12 + i * (w - 24) // 4
            d.line([px, y + h // 2, px, y + h * 3 // 5], fill=INK, width=2)
        d.ellipse([x + w - 52, y + 6, x + w - 22, y + 30], fill=(120, 120, 120))
        d.ellipse([x + w - 40, y + 2, x + w - 14, y + 22], fill=(150, 150, 150))
        d.polygon([(x + w - 30, y + h // 2), (x + w - 18, y + h // 2 - 12),
                   (x + w - 6, y + h // 2)], fill=(230, 140, 40))
    elif kind == 2:  # Gulf map, dashed drone path
        d.rectangle([x, y, x + w, y + h], fill=(240, 232, 214))
        d.polygon([(x + 10, y + 8), (x + w - 10, y + 8), (x + w - 10, y + h - 8),
                   (x + w // 2, y + h - 30), (x + 10, y + h - 8)],
                  fill=SEA)
        d.ellipse([x + w // 2 - 5, y + h // 3, x + w // 2 + 5, y + h // 3 + 10],
                  fill=(230, 140, 40))
        d.ellipse([x + w - 34, y + h - 34, x + w - 22, y + h - 22],
                  fill=(178, 34, 34))
        px, py = x + 16, y + h - 24
        for _ in range(7):
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(176, 92, 20))
            px += (w - 40) // 7
            py -= (h - 40) // 7
    elif kind == 3:  # bridge under strike
        d.rectangle([x, y, x + w, y + h], fill=SKY)
        d.rectangle([x, y + h * 2 // 3, x + w, y + h], fill=SEA)
        d.line([x + 6, y + h // 2, x + cx - 20, y + h // 2], fill=INK, width=4)
        d.line([cx + 20, y + h // 2, x + w - 6, y + h // 2], fill=INK, width=4)
        d.line([cx - 20, y + h // 2, cx - 8, y + h * 2 // 3], fill=INK, width=3)
        d.line([cx + 20, y + h // 2, cx + 8, y + h * 2 // 3], fill=INK, width=3)
        d.ellipse([cx - 26, y + 4, cx + 2, y + 28], fill=(120, 120, 120))
        d.ellipse([cx + 2, y + 10, cx + 26, y + 30], fill=(150, 150, 150))
        for dx, dy in [(-14, -8), (14, -8), (0, -16)]:
            d.polygon([(cx + dx, cy - 6 + dy), (cx + dx + 5, cy - 14 + dy),
                       (cx + dx + 10, cy - 6 + dy)], fill=(230, 140, 40))
    elif kind == 4:  # summit table with globe
        d.rectangle([x, y, x + w, y + h], fill=(232, 238, 228))
        d.ellipse([cx - 26, y + 8, cx + 26, y + 60], fill=(90, 140, 200))
        d.ellipse([cx - 26, y + 8, cx + 26, y + 60], outline=(30, 80, 140),
                  width=2)
        d.arc([cx - 26, y + 20, cx + 26, y + 48], 0, 360, fill=(40, 120, 60),
              width=2)
        d.rectangle([x + 8, y + h - 26, x + w - 8, y + h - 14], fill=(120, 70, 40))
        for fx in (x + 14, cx - 4, x + w - 30):
            d.rectangle([fx, y + h - 44, fx + 14, y + h - 26], fill=(178, 34, 34))
    elif kind == 5:  # virus cell
        d.rectangle([x, y, x + w, y + h], fill=(240, 230, 245))
        for ang in range(0, 360, 45):
            import math
            r = math.radians(ang)
            x1 = cx + int(20 * math.cos(r))
            y1 = cy + int(20 * math.sin(r))
            x2 = cx + int(32 * math.cos(r))
            y2 = cy + int(32 * math.sin(r))
            d.line([x1, y1, x2, y2], fill=(110, 60, 140), width=3)
            d.ellipse([x2 - 4, y2 - 4, x2 + 4, y2 + 4], fill=(110, 60, 140))
        d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=(150, 90, 180))
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(110, 60, 140))
    elif kind == 6:  # outbreak chart
        d.rectangle([x, y, x + w, y + h], fill=(228, 240, 230))
        bars = [12, 20, 30, 44]
        for i, bh in enumerate(bars):
            bx = x + 12 + i * (w - 24) // 4
            d.rectangle([bx, y + h - 14 - bh, bx + 18, y + h - 14],
                        fill=(34, 120, 60))
        d.line([x + 8, y + h - 14, x + w - 8, y + h - 14], fill=INK, width=2)
        d.ellipse([x + w - 34, y + 8, x + w - 12, y + 30], fill=(178, 34, 34))
    elif kind == 7:  # document and seal
        d.rectangle([x, y, x + w, y + h], fill=(238, 236, 224))
        d.rectangle([x + 14, y + 8, x + w - 30, y + h - 8], fill=WHITE,
                    outline=INK, width=2)
        for i in range(4):
            d.line([x + 20, y + 18 + i * 12, x + w - 38, y + 18 + i * 12],
                   fill=(120, 120, 120), width=2)
        d.ellipse([x + w - 34, y + h - 34, x + w - 10, y + h - 10],
                  fill=GOLD, outline=(150, 110, 20), width=2)
    elif kind == 8:  # gavel and vote bars (all inside the 40px strip)
        d.rectangle([x, y, x + w, y + h], fill=(240, 234, 220))
        d.rectangle([x + 12, y + 4, x + w - 12, y + 14], fill=(31, 78, 140))
        d.text((x + 16, y + 5), "66", font=F_BOLD(11), fill=WHITE)
        d.rectangle([x + 12, y + 18, x + w - 12, y + 28], fill=(120, 120, 120))
        d.text((x + 16, y + 19), "52", font=F_BOLD(11), fill=WHITE)
        d.rectangle([cx - 26, y + 32, cx + 26, y + 37], fill=(120, 70, 40))
        d.line([cx - 16, y + 36, cx + 16, y + 32], fill=(90, 50, 20),
               width=4)
    elif kind == 9:  # globe with leaf
        d.rectangle([x, y, x + w, y + h], fill=(226, 238, 240))
        d.ellipse([cx - 26, y + 6, cx + 26, y + 58], fill=(90, 140, 200))
        d.ellipse([cx - 14, y + 14, cx + 6, y + 34], fill=(40, 120, 60))
        d.ellipse([cx - 2, y + 36, cx + 16, y + 52], fill=(40, 120, 60))
        d.line([x + 10, y + h - 12, x + w - 10, y + h - 12], fill=INK, width=2)
    elif kind == 10:  # railway and coin
        d.rectangle([x, y, x + w, y + h], fill=(236, 232, 220))
        d.line([x + 8, y + h - 12, x + w - 40, y + 12], fill=INK, width=3)
        d.line([x + 30, y + h - 12, x + w - 18, y + 12], fill=INK, width=3)
        for i in range(4):
            t = i / 3.0
            sx = int(x + 14 + t * (w - 50))
            sy = int(y + h - 20 - t * (h - 30))
            d.line([sx - 8, sy + 4, sx + 8, sy - 4], fill=INK, width=2)
        d.ellipse([x + w - 36, y + 6, x + w - 8, y + 34], fill=GOLD,
                  outline=(150, 110, 20), width=2)
        d.text((x + w - 31, y + 13), "$", font=F_BOLD(14), fill=INK)
    elif kind == 11:  # falling chart
        d.rectangle([x, y, x + w, y + h], fill=(244, 228, 228))
        bars = [40, 34, 26, 16]
        for i, bh in enumerate(bars):
            bx = x + 12 + i * (w - 24) // 4
            d.rectangle([bx, y + h - 12 - bh, bx + 18, y + h - 12],
                        fill=(178, 34, 34))
        d.line([x + 10, y + 10, x + w - 30, y + h - 24], fill=(120, 0, 0),
               width=3)
        d.polygon([(x + w - 30, y + h - 24), (x + w - 14, y + h - 24),
                   (x + w - 22, y + h - 8)], fill=(120, 0, 0))
    else:  # 12: crowd and banner
        d.rectangle([x, y, x + w, y + h], fill=(232, 236, 244))
        bh = max(12, h // 4)
        d.rectangle([x + 10, y + 4, x + w - 10, y + 4 + bh], fill=NAVY)
        d.text((x + 16, y + 5), "PAY", font=F_BOLD(10), fill=WHITE)
        hy = y + 6 + bh
        for i in range(5):
            hx = x + 16 + i * (w - 32) // 4
            d.ellipse([hx - 7, hy, hx + 7, hy + 12], fill=(220, 180, 140))
            d.rectangle([hx - 11, hy + 13, hx + 11, y + h - 4],
                        fill=(31, 78, 140))


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
    for row, (gy, chunk) in enumerate([(234, MAINS[2:7]), (380, MAINS[7:12])]):
        for j, m in enumerate(chunk):
            num, tag, head, desc = m[0], m[1], m[2], m[3]
            x = grid_xs[j]
            d.rectangle([x, gy, x + grid_w, gy + 138], fill=WHITE,
                        outline=RULE, width=1)
            d.rectangle([x, gy, x + grid_w, gy + 4], fill=tag_color(tag))
            draw_illus_box(img, num, x + 6, gy + 10, grid_w - 12, 40)
            ty = gy + 54
            d.text((x + 8, ty), f"{num}  {tag}", font=F_BOLD(10),
                   fill=tag_color(tag))
            hlines = len(wrap(d, head, F_BOLD(15), grid_w - 16))
            hy_end = draw_wrapped(d, head, F_BOLD(15), x + 8, ty + 16,
                                  grid_w - 16, 3, INK, 1)
            draw_wrapped(d, desc, F_REG(11), x + 8, hy_end + 2,
                         grid_w - 16, 2 if hlines <= 2 else 1, MUTED, 1,
                         ellipsis=True)

    # ---- Bottom: map column ----
    d.text((14, 528), "WHERE IT HAPPENED", font=F_BOLD(13), fill=INK)
    d.line([14, 546, 304, 546], fill=RULE, width=1)
    mx, my, mw, mh = 14, 552, 290, 200
    d.rectangle([mx, my, mx + mw, my + mh], fill=(238, 232, 214),
                outline=RULE, width=1)
    # Simplified land masses (flat beige shapes).
    land = (222, 210, 178)
    d.polygon([(mx + 18, my + 52), (mx + 70, my + 28), (mx + 96, my + 44),
               (mx + 92, my + 96), (mx + 60, my + 128), (mx + 30, my + 100)],
              fill=land)  # North America
    d.polygon([(mx + 62, my + 128), (mx + 92, my + 128), (mx + 96, my + 168),
               (mx + 76, my + 190), (mx + 64, my + 158)], fill=land)
    d.polygon([(mx + 128, my + 40), (mx + 168, my + 30), (mx + 182, my + 60),
               (mx + 168, my + 108), (mx + 140, my + 96), (mx + 128, my + 66)],
              fill=land)  # Europe / Africa top
    d.polygon([(mx + 150, my + 104), (mx + 176, my + 104), (mx + 182, my + 150),
               (mx + 168, my + 172), (mx + 152, my + 140)], fill=land)
    d.polygon([(mx + 186, my + 44), (mx + 246, my + 34), (mx + 268, my + 70),
               (mx + 250, my + 118), (mx + 214, my + 110), (mx + 196, my + 76)],
              fill=land)  # Asia
    d.polygon([(mx + 238, my + 148), (mx + 268, my + 148), (mx + 262, my + 172),
               (mx + 240, my + 168)], fill=land)  # Oceania
    # Brief dots first (small, under the numbered mains).
    for b in BRIEFS:
        bx, by = lonlat_to_xy(b[4], b[5], mx, my, mw, mh)
        col = TAG_COLORS.get(b[3], (90, 90, 90))
        d.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=col,
                  outline=WHITE, width=1)
    # Numbered main dots (nudged apart where true positions collide).
    nudges = {1: (-14, 2), 2: (20, 2), 3: (4, -14), 4: (-10, -10),
              7: (10, 8), 8: (2, 16), 9: (-14, 10), 11: (-2, -16),
              12: (-16, -10)}
    for m in MAINS:
        bx, by = lonlat_to_xy(m[5], m[6], mx, my, mw, mh)
        dx, dy = nudges.get(m[0], (0, 0))
        bx, by = bx + dx, by + dy
        col = TAG_COLORS.get(m[4], (90, 90, 90))
        d.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=col,
                  outline=WHITE, width=2)
        label = str(m[0])
        lw = d.textlength(label, font=F_BOLD(10))
        d.text((bx - lw / 2, by - 7), label, font=F_BOLD(10), fill=WHITE)
    # Legend.
    ly = my + mh + 12
    d.text((14, ly), "EUROPE", font=F_BOLD(10), fill=TAG_COLORS["EUROPE"])
    d.text((86, ly), "MIDDLE EAST", font=F_BOLD(10),
           fill=TAG_COLORS["MIDDLE EAST"])
    d.text((186, ly), "ASIA", font=F_BOLD(10), fill=TAG_COLORS["ASIA"])
    d.text((236, ly), "AFRICA", font=F_BOLD(10), fill=TAG_COLORS["AFRICA"])
    ly += 16
    d.text((14, ly), "AMERICAS", font=F_BOLD(10), fill=TAG_COLORS["AMERICAS"])
    d.text((86, ly), "OCEANIA", font=F_BOLD(10), fill=TAG_COLORS["OCEANIA"])
    d.text((186, ly), "GLOBAL", font=F_BOLD(10), fill=TAG_COLORS["GLOBAL"])
    d.text((14, ly + 16), "Numbered dots = the top 12 stories.",
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
        ty += 20
    d.text((14, ty + 4), "48 stories in total: 12 top stories",
           font=F_REG(11), fill=MUTED)
    d.text((14, ty + 20), "numbered on the map, plus 36 briefs.",
           font=F_REG(11), fill=MUTED)

    # ---- Bottom right: briefs ----
    bx0, bw_col = 312, 344
    d.text((bx0, 528), "ALSO ON TUESDAY 17 NOVEMBER", font=F_BOLD(13),
           fill=INK)
    d.line([bx0, 546, 1010, 546], fill=RULE, width=1)
    row_h = 25
    for idx, b in enumerate(BRIEFS):
        num, head, desc = b[0], b[1], b[2]
        col = idx // 18
        row = idx % 18
        x = bx0 + col * (bw_col + 10)
        y = 554 + row * row_h
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
