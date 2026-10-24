import os
import sys
import math

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, KeepTogether, NextPageTemplate, CondPageBreak)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon, Circle, Wedge, Group

OUT = sys.argv[1]

# ---------- fonts ----------
FD = r"C:\Windows\Fonts"
pdfmetrics.registerFont(TTFont("UI", os.path.join(FD, "segoeui.ttf")))
pdfmetrics.registerFont(TTFont("UI-B", os.path.join(FD, "segoeuib.ttf")))
pdfmetrics.registerFont(TTFont("UI-SB", os.path.join(FD, "seguisb.ttf")))
pdfmetrics.registerFont(TTFont("UI-I", os.path.join(FD, "segoeuii.ttf")))
pdfmetrics.registerFont(TTFont("UI-L", os.path.join(FD, "segoeuil.ttf")))
pdfmetrics.registerFontFamily("UI", normal="UI", bold="UI-B", italic="UI-I", boldItalic="UI-B")

# ---------- palette ----------
NAVY = colors.HexColor("#161A33")
NAVY2 = colors.HexColor("#232A52")
VIOLET = colors.HexColor("#6C5CE7")
TEAL = colors.HexColor("#00A884")
AMBER = colors.HexColor("#F5A623")
RED = colors.HexColor("#E0525A")
INK = colors.HexColor("#1F2433")
MUTED = colors.HexColor("#5E6476")
LINE = colors.HexColor("#D9DCE6")
SOFT = colors.HexColor("#F3F4F9")
SOFTV = colors.HexColor("#ECEAFD")
SOFTT = colors.HexColor("#E3F6F1")
SOFTA = colors.HexColor("#FEF3E0")
SOFTR = colors.HexColor("#FCE8E9")
WHITE = colors.white

PAGE_W, PAGE_H = A4
MARGIN_X = 20 * mm
CONTENT_W = PAGE_W - 2 * MARGIN_X

# ---------- styles ----------
ST = {
    "body": ParagraphStyle("body", fontName="UI", fontSize=10, leading=15, textColor=INK,
                           spaceAfter=6, alignment=TA_LEFT, allowWidows=0, allowOrphans=0),
    "lead": ParagraphStyle("lead", fontName="UI-L", fontSize=12, leading=18, textColor=INK, spaceAfter=10),
    "h1": ParagraphStyle("H1", fontName="UI-B", fontSize=22, leading=28, textColor=NAVY, spaceAfter=4),
    "kicker": ParagraphStyle("kicker", fontName="UI-SB", fontSize=9, leading=12, textColor=VIOLET, spaceAfter=2),
    "h2": ParagraphStyle("H2", fontName="UI-SB", fontSize=13.5, leading=18, textColor=NAVY2,
                         spaceBefore=10, spaceAfter=5, keepWithNext=1),
    "cell": ParagraphStyle("cell", fontName="UI", fontSize=8.8, leading=12, textColor=INK),
    "cellb": ParagraphStyle("cellb", fontName="UI-SB", fontSize=8.8, leading=12, textColor=INK),
    "th": ParagraphStyle("th", fontName="UI-SB", fontSize=8.8, leading=12, textColor=WHITE),
    "bullet": ParagraphStyle("bullet", fontName="UI", fontSize=10, leading=15, textColor=INK,
                             leftIndent=14, bulletIndent=3, spaceAfter=3),
    "caption": ParagraphStyle("caption", fontName="UI-I", fontSize=8.5, leading=11, textColor=MUTED,
                              alignment=TA_CENTER, spaceBefore=3, spaceAfter=10),
    "callout": ParagraphStyle("callout", fontName="UI", fontSize=9.6, leading=14, textColor=INK),
    "toc1": ParagraphStyle("toc1", fontName="UI-SB", fontSize=11, leading=20, textColor=INK, leftIndent=0),
}

ALL_TEXT = []  # for glyph coverage check


def P(text, style="body"):
    ALL_TEXT.append(text)
    return Paragraph(text, ST[style])


def bullets(items, style="bullet"):
    out = []
    for it in items:
        ALL_TEXT.append(it)
        out.append(Paragraph(it, ST[style], bulletText="•"))
    return out


class H1(Paragraph):
    pass


def chapter(num, title, kicker):
    ALL_TEXT.extend([title, kicker])
    h = H1(f"{num}. {title}", ST["h1"])
    h.toc_text = f"{num}. {title}"
    k = Paragraph(kicker.upper(), ST["kicker"])
    bar = Table([[""]], colWidths=[40 * mm], rowHeights=[2.2], hAlign="LEFT")
    bar.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), VIOLET)]))
    return [k, h, Spacer(1, 3), bar, Spacer(1, 10)]


def h2(text):
    ALL_TEXT.append(text)
    return Paragraph(text, ST["h2"])


def table(rows, widths, header=True, zebra=True, first_col_bold=False, accent=NAVY2):
    data = []
    for r_i, row in enumerate(rows):
        cells = []
        for c_i, c in enumerate(row):
            ALL_TEXT.append(str(c))
            if header and r_i == 0:
                cells.append(Paragraph(str(c), ST["th"]))
            elif first_col_bold and c_i == 0:
                cells.append(Paragraph(str(c), ST["cellb"]))
            else:
                cells.append(Paragraph(str(c), ST["cell"]))
        data.append(cells)
    total = sum(widths)
    widths = [w * CONTENT_W / total for w in widths]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0, splitByRow=1)
    style = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, LINE),
        ("BOX", (0, 0), (-1, -1), 0.6, LINE),
    ]
    if header:
        style += [("BACKGROUND", (0, 0), (-1, 0), accent)]
    if zebra:
        start = 1 if header else 0
        for i in range(start, len(data)):
            if (i - start) % 2 == 1:
                style.append(("BACKGROUND", (0, i), (-1, i), SOFT))
    t.setStyle(TableStyle(style))
    return t


def callout(text, kind="info"):
    ALL_TEXT.append(text)
    bg, bar = {"info": (SOFTV, VIOLET), "ok": (SOFTT, TEAL), "warn": (SOFTA, AMBER), "risk": (SOFTR, RED)}[kind]
    t = Table([[Paragraph(text, ST["callout"])]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, -1), 3, bar),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return KeepTogether([t, Spacer(1, 8)])


def figure(drawing, caption):
    ALL_TEXT.append(caption)
    return KeepTogether([drawing, Paragraph(caption, ST["caption"])])


# ---------- drawing helpers ----------
def wrap_lines(text, font, size, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if stringWidth(test, font, size) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def box(d, x, y, w, h, title, sub=None, fill=SOFTV, stroke=VIOLET, tcolor=NAVY, tsize=9.5, ssize=7.6, radius=6, scolor=None):
    ALL_TEXT.append(title)
    if sub:
        ALL_TEXT.append(sub)
    d.add(Rect(x, y, w, h, rx=radius, ry=radius, fillColor=fill, strokeColor=stroke, strokeWidth=1))
    tl = wrap_lines(title, "UI-SB", tsize, w - 10)
    sl = wrap_lines(sub, "UI", ssize, w - 10) if sub else []
    total = len(tl) * (tsize + 2) + len(sl) * (ssize + 2)
    cy = y + h / 2 + total / 2 - tsize
    for ln in tl:
        d.add(String(x + w / 2, cy, ln, fontName="UI-SB", fontSize=tsize, fillColor=tcolor, textAnchor="middle"))
        cy -= tsize + 2
    for ln in sl:
        d.add(String(x + w / 2, cy, ln, fontName="UI", fontSize=ssize, fillColor=scolor or MUTED, textAnchor="middle"))
        cy -= ssize + 2


def arrow(d, x1, y1, x2, y2, color=MUTED, width=1.2, head=6, label=None, lsize=7.2, loff=(0, 4)):
    d.add(Line(x1, y1, x2, y2, strokeColor=color, strokeWidth=width))
    ang = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 - head * math.cos(ang - 0.4), y2 - head * math.sin(ang - 0.4))
    p2 = (x2 - head * math.cos(ang + 0.4), y2 - head * math.sin(ang + 0.4))
    d.add(Polygon([x2, y2, p1[0], p1[1], p2[0], p2[1]], fillColor=color, strokeColor=color))
    if label:
        ALL_TEXT.append(label)
        d.add(String((x1 + x2) / 2 + loff[0], (y1 + y2) / 2 + loff[1], label, fontName="UI", fontSize=lsize,
                     fillColor=MUTED, textAnchor="middle"))


def text(d, x, y, s, size=8, font="UI", color=INK, anchor="middle"):
    ALL_TEXT.append(s)
    d.add(String(x, y, s, fontName=font, fontSize=size, fillColor=color, textAnchor=anchor))


def rule_list(d, x, ytop, title, rows, width, ksize=8.3, vsize=7.8, gap=6):
    """Key/value list beside a diagram; advances by the real number of wrapped lines."""
    text(d, x, ytop, title, 10, "UI-B", NAVY, "start")
    y = ytop - 20
    for k, v in rows:
        text(d, x, y, k, ksize, "UI-SB", NAVY, "start")
        y -= ksize + 3
        for ln in wrap_lines(v, "UI", vsize, width):
            text(d, x, y, ln, vsize, "UI", INK, "start")
            y -= vsize + 2.5
        y -= gap
    return y


# ---------- diagrams ----------
def fig_core_loop():
    W, H = CONTENT_W, 230
    d = Drawing(W, H)
    cx, cy, r = W / 2, H / 2 - 5, 82
    nodes = [
        ("Plaza Sosial", "nongkrong, party, chat", SOFTV, VIOLET),
        ("Bertanding", "Ranked / Custom / Relic", SOFTR, RED),
        ("Hadiah", "Gold, rank, statistik", SOFTA, AMBER),
        ("Wardrobe & Toko", "dandan, sewa, gacha", SOFTT, TEAL),
        ("Squad & Komunitas", "war mingguan, mentor", SOFT, NAVY2),
    ]
    bw, bh = 128, 44
    pos = []
    for i, n in enumerate(nodes):
        a = math.pi / 2 - i * 2 * math.pi / len(nodes)
        x, y = cx + r * 1.55 * math.cos(a), cy + r * math.sin(a)
        pos.append((x, y))
        box(d, x - bw / 2, y - bh / 2, bw, bh, n[0], n[1], fill=n[2], stroke=n[3])
    for i in range(len(pos)):
        (x1, y1), (x2, y2) = pos[i], pos[(i + 1) % len(pos)]
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        sx, sy = x1 + dx / L * 58, y1 + dy / L * 26
        ex, ey = x2 - dx / L * 58, y2 - dy / L * 26
        arrow(d, sx, sy, ex, ey, color=VIOLET)
    d.add(Circle(cx, cy, 30, fillColor=NAVY, strokeColor=NAVY))
    text(d, cx, cy + 2, "AVATAR", 9, "UI-B", WHITE)
    text(d, cx, cy - 9, "= kamu", 7.5, "UI", WHITE)
    return d


def fig_world():
    W, H = CONTENT_W, 250
    d = Drawing(W, H)
    cx, cy = W / 2, 150
    pw, ph = 180, 64
    box(d, cx - pw / 2, cy - ph / 2, pw, ph, "PLAZA (Kota)", "30–60 pemain per instance; berubah sesuai hasil Squad War",
        fill=NAVY, stroke=NAVY, tcolor=WHITE, tsize=11, scolor=colors.HexColor("#C9CDEB"))
    bw, bh = 148, 44
    gates = [
        (0, H - bh - 4, "Battle Gate", "Ranked, Quick, Custom Room", SOFTR, RED),
        (W - bw, H - bh - 4, "Relic Gate", "Dungeon PvE farming", SOFTA, AMBER),
        (0, 62, "Rest Room", "Ngobrol, minigame, couple room 18+", SOFTT, TEAL),
        (W - bw, 62, "Shop / Gacha / Wardrobe", "Belanja & dandan", SOFTV, VIOLET),
        (cx - bw / 2, 4, "Squad HQ", "Markas squad, dekorasi", SOFT, NAVY2),
    ]
    for x, y, t, s, f, st in gates:
        box(d, x, y, bw, bh, t, s, fill=f, stroke=st)
    # arrows from plaza edges to each gate
    arrow(d, cx - pw / 2, cy + 20, bw + 2, H - bh / 2 - 4)
    arrow(d, cx + pw / 2, cy + 20, W - bw - 2, H - bh / 2 - 4)
    arrow(d, cx - pw / 2, cy - 20, bw + 2, 62 + bh / 2)
    arrow(d, cx + pw / 2, cy - 20, W - bw - 2, 62 + bh / 2)
    arrow(d, cx, cy - ph / 2, cx, 4 + bh + 2)
    return d


def fig_layers():
    W, H = CONTENT_W, 166
    d = Drawing(W, H)
    layers = [
        ("Efek skin gear", "Kosmetik MiCash; tidak mengubah siluet", SOFTA, AMBER, "Ikut gear"),
        ("Gear tempur: Helm, Armor, Trinket, Senjata", "Memberi skill; bisa rontok saat Critical (kecuali senjata)", SOFTR, RED, "Bisa rontok"),
        ("Kostum avatar (Wardrobe)", "Identitas sosial; nol stat", SOFTT, TEAL, "Tidak pernah lepas"),
        ("Tubuh avatar (2 base body L/P)", "Shared humanoid rig; variasi bone scale/blendshape", SOFTV, VIOLET, "Permanen"),
    ]
    bw, bh, gap = 240, 34, 6
    x0 = 0
    y = H - bh - 6
    for t, s, f, st, tag in layers:
        box(d, x0, y, bw, bh, t, s, fill=f, stroke=st, tsize=8.8, ssize=7.2)
        d.add(Rect(x0 + bw + 8, y + 8, 92, 18, rx=9, ry=9, fillColor=st, strokeColor=st))
        text(d, x0 + bw + 54, y + 13.5, tag, 7.4, "UI-SB", WHITE)
        y -= bh + gap
    gx = x0 + bw + 112
    gw = W - gx
    d.add(Rect(gx, 6, gw, H - 12, rx=8, ry=8, fillColor=SOFT, strokeColor=LINE))
    text(d, gx + gw / 2, H - 24, "Lapisan gameplay", 9.5, "UI-B", NAVY)
    yy = H - 44
    for para in ["Hurtbox kapsul standar, sama untuk SEMUA pemain",
                 "Hitbox berasal dari senjata dan skill",
                 "Kostum dan skin tidak pernah mengubah box apa pun"]:
        for ln in wrap_lines(para, "UI", 7.8, gw - 16):
            text(d, gx + gw / 2, yy, ln, 7.8)
            yy -= 11
        yy -= 9
    return d


def fig_life():
    W, H = CONTENT_W, 190
    d = Drawing(W, H)
    y = 110
    box(d, 0, y, 84, 54, "HP > 0", "dipukul, darah turun", fill=SOFTT, stroke=TEAL)
    arrow(d, 86, y + 27, 104, y + 27, color=TEAL)
    box(d, 106, y, 86, 54, "Damage Gate", "HP berhenti di 0, tanpa overkill", fill=SOFTA, stroke=AMBER)
    arrow(d, 194, y + 27, 212, y + 27, color=AMBER)
    d.add(Rect(214, y - 6, 176, 66, rx=8, ry=8, fillColor=SOFTR, strokeColor=RED))
    text(d, 302, y + 47, "CRITICAL (HP = 0)", 9.5, "UI-B", RED)
    for i in range(3):
        sx = 224 + i * 54
        d.add(Rect(sx, y + 6, 48, 28, rx=5, ry=5, fillColor=WHITE, strokeColor=RED))
        text(d, sx + 24, y + 22, f"Stock {3 - i}", 7.6, "UI-SB", RED)
        text(d, sx + 24, y + 12, ["Helm", "Trinket", "Armor"][i], 7, "UI", MUTED)
    arrow(d, 392, y + 27, 408, y + 27, color=RED)
    box(d, 410, y, CONTENT_W - 410, 54, "KO", "senjata terpental (visual)", fill=NAVY, stroke=NAVY, tcolor=WHITE,
        scolor=colors.HexColor("#C9CDEB"))
    notes = [
        ("Masuk Critical", "pushback + knockdown + i-frame (reset netral)"),
        ("Pukulan berat", "memecahkan 1 stock langsung"),
        ("Pukulan ringan", "mengisi Break Meter; penuh = 1 stock"),
        ("Stock pecah", "hard knockdown + gear rontok; maks 1 stock per combo"),
        ("Saat Critical", "swap terkunci, heal = shield, gerak −10–15%, posisi terlihat"),
    ]
    yy = 82
    for k, v in notes:
        text(d, 6, yy, k, 8, "UI-SB", NAVY, "start")
        text(d, 110, yy, v, 8, "UI", INK, "start")
        yy -= 15
    return d


def fig_guard():
    W, H = CONTENT_W, 190
    d = Drawing(W, H)
    cx, cy, r = 150, 92, 70
    d.add(Circle(cx, cy, r, fillColor=SOFTR, strokeColor=RED, strokeWidth=0.8))
    d.add(Wedge(cx, cy, r, -90, 90, fillColor=SOFTT, strokeColor=TEAL, strokeWidth=1))
    d.add(Circle(cx, cy, 12, fillColor=NAVY, strokeColor=NAVY))
    arrow(d, cx, cy, cx + 40, cy, color=WHITE, width=2, head=5)
    text(d, cx + r * 0.55, cy + 34, "Depan 180°", 8.5, "UI-SB", TEAL)
    text(d, cx + r * 0.55, cy + 23, "TERTANGKIS", 7.5, "UI", TEAL)
    text(d, cx - r * 0.55, cy + 34, "Belakang", 8.5, "UI-SB", RED)
    text(d, cx - r * 0.55, cy + 23, "TEMBUS", 7.5, "UI", RED)
    for ax, ay, col in [(cx + 110, cy + 30, TEAL), (cx - 110, cy - 30, RED)]:
        d.add(Circle(ax, ay, 9, fillColor=col, strokeColor=col))
        arrow(d, ax + (-12 if ax > cx else 12), ay + (-4 if ay > cy else 4),
              cx + (r - 4 if ax > cx else -r + 4) * 0.8, cy + (12 if ay > cy else -12), color=col)
    rx = 315
    rules = [
        ("Lock Facing", "arah hadap terkunci selama guard ditahan"),
        ("Pivot", "berbalik butuh lepas guard / pivot (ada celah)"),
        ("Auto-Face", "guard tanpa arah → hadap musuh terdekat (6 m)"),
        ("Guard Gauge", "habis → Guard Crush → Faint"),
        ("Aim-assist", "serangan snap ±22,5° ke musuh terdekat"),
    ]
    rule_list(d, rx, H - 12, "Aturan guard & arah", rules, W - rx - 4, gap=4)
    return d


def fig_arena():
    W, H = CONTENT_W, 215
    d = Drawing(W, H)
    d.add(Rect(10, 10, 330, 195, rx=10, ry=10, fillColor=colors.HexColor("#2B2F4A"), strokeColor=NAVY))
    text(d, 175, 194, "DropZone (jurang)", 8, "UI-SB", WHITE)
    d.add(Rect(40, 32, 270, 150, rx=14, ry=14, fillColor=colors.HexColor("#DCE4F2"), strokeColor=NAVY2, strokeWidth=1.2))
    d.add(Rect(52, 82, 48, 50, rx=6, ry=6, fillColor=SOFTV, strokeColor=VIOLET))
    text(d, 76, 104, "Spawn A", 7.8, "UI-SB", VIOLET)
    d.add(Rect(250, 82, 48, 50, rx=6, ry=6, fillColor=SOFTR, strokeColor=RED))
    text(d, 274, 104, "Spawn B", 7.8, "UI-SB", RED)
    d.add(Circle(175, 107, 22, fillColor=SOFTA, strokeColor=AMBER))
    text(d, 175, 104, "Tengah", 7.5, "UI-SB", INK)
    # fall example (bottom-right edge of the floor)
    px = 285
    d.add(Circle(px, 40, 6, fillColor=NAVY, strokeColor=NAVY))          # last grounded position
    arrow(d, px + 4, 35, px + 22, 16, color=RED, width=1.4)             # falls off the edge
    text(d, px + 36, 13, "1. jatuh", 7.2, "UI-SB", WHITE)
    d.add(Rect(px - 30, 36, 12, 9, fillColor=AMBER, strokeColor=AMBER))  # ejected gear
    text(d, 150, 38, "2. gear → titik lantai terakhir", 7.2, "UI-SB", INK)
    d.add(Circle(px - 18, 66, 6, fillColor=TEAL, strokeColor=TEAL))      # sky-drop point (pulled inward)
    arrow(d, px + 24, 20, px - 13, 61, color=TEAL, width=1.2)
    text(d, 168, 63, "3. Sky-Drop ±3 m ke dalam", 7.2, "UI-SB", INK)
    rx = 352
    rows = [
        ("HP > 0", "fall damage ±15%, berhenti di 0"),
        ("Critical", "pecah 1 Break Stock"),
        ("Gear rontok", "dilontarkan ke titik lantai terakhir"),
        ("Kembali", "Sky-Drop dekat titik jatuh"),
        ("Stagger", "0,5–0,6 s, tak bisa diserang/menyerang"),
        ("Atribusi", "musuh terakhir yang memukul (10 s)"),
    ]
    rule_list(d, rx, H - 12, "Aturan DropZone", rows, W - rx - 2, gap=3)
    return d


def fig_arch():
    W, H = CONTENT_W, 255
    d = Drawing(W, H)
    # client
    d.add(Rect(0, 120, 160, 125, rx=8, ry=8, fillColor=SOFTV, strokeColor=VIOLET))
    text(d, 80, 230, "Unity Client (PC)", 10, "UI-B", NAVY)
    box(d, 12, 182, 136, 36, "Render & Animasi", "sampling (anim, frame); tanpa root motion", fill=WHITE, stroke=VIOLET)
    box(d, 12, 132, 136, 40, "Combat Core (prediksi)", "C# murni, fixed-point, 60 Hz", fill=NAVY, stroke=NAVY, tcolor=WHITE)
    # game server
    d.add(Rect(W - 160, 120, 160, 125, rx=8, ry=8, fillColor=SOFTR, strokeColor=RED))
    text(d, W - 80, 230, "Game Server (.NET 8)", 10, "UI-B", NAVY)
    box(d, W - 148, 182, 136, 36, "Wasit / otoritas", "≥ 20 match per vCPU (target)", fill=WHITE, stroke=RED)
    box(d, W - 148, 132, 136, 40, "Combat Core (otoritas)", "kode yang SAMA dengan client", fill=NAVY, stroke=NAVY, tcolor=WHITE)
    # udp
    arrow(d, 162, 165, W - 162, 165, color=RED, label="input per tick (UDP, unreliable, redundan)", loff=(0, 5))
    arrow(d, W - 162, 145, 162, 145, color=RED, label="snapshot delta 30–60 Hz", loff=(0, -11))
    # nakama
    nx = W / 2 - 115
    d.add(Rect(nx, 8, 230, 92, rx=8, ry=8, fillColor=SOFTT, strokeColor=TEAL))
    text(d, nx + 115, 86, "Nakama (meta backend)", 10, "UI-B", NAVY)
    for i, s in enumerate(["Akun & role • party • chat • squad", "Matchmaker • leaderboard • MMR",
                           "Wallet Gold/Ticket/MiCash • inventory sewa", "Plaza (authoritative match, Go)"]):
        text(d, nx + 115, 71 - i * 12, s, 7.8)
    arrow(d, 120, 118, nx + 40, 100, color=TEAL)
    text(d, nx - 6, 88, "HTTPS / WebSocket", 7.2, "UI-SB", TEAL, "end")
    arrow(d, W - 120, 118, nx + 190, 100, color=TEAL)
    text(d, nx + 236, 88, "hasil match (server-to-server)", 7.2, "UI-SB", TEAL, "start")
    # cdn
    box(d, 0, 30, 120, 50, "CDN Konten", "data hero ber-hash + bundle kosmetik", fill=SOFTA, stroke=AMBER)
    arrow(d, 40, 82, 40, 118, color=AMBER)
    box(d, W - 120, 30, 120, 50, "PostgreSQL", "data akun, ekonomi, statistik", fill=SOFT, stroke=NAVY2)
    arrow(d, W - 120, 55, nx + 232, 55, color=NAVY2)
    return d


def fig_flow():
    W, H = CONTENT_W, 150
    d = Drawing(W, H)
    steps = [
        ("1", "Plaza", "party dibentuk"),
        ("2", "Antrean / Room", "matchmaker Nakama"),
        ("3", "Alokasi server", "IP:port + matchId"),
        ("4", "Loadout 3 hero", "cek kepemilikan & sewa"),
        ("5", "Tiket join", "token bertanda tangan"),
        ("6", "Match 60 Hz", "game server UDP"),
        ("7", "Laporan hasil", "server → Nakama"),
        ("8", "Kembali", "Plaza + layar hasil"),
    ]
    per_row = 4
    bw, bh = (W - 3 * 18) / per_row, 50
    for i, (n, t, s) in enumerate(steps):
        row, col = divmod(i, per_row)
        if row == 1:
            col = per_row - 1 - col
        x = col * (bw + 18)
        y = H - 60 - row * 82
        box(d, x, y, bw, bh, t, s, fill=SOFTV if i % 2 == 0 else SOFTT, stroke=VIOLET if i % 2 == 0 else TEAL)
        d.add(Circle(x + 10, y + bh - 2, 9, fillColor=NAVY, strokeColor=WHITE))
        text(d, x + 10, y + bh - 5, n, 8, "UI-B", WHITE)
        if i < len(steps) - 1:
            if (i + 1) % per_row == 0:
                arrow(d, x + bw / 2, y - 2, x + bw / 2, y - 30, color=MUTED)
            elif row == 0:
                arrow(d, x + bw + 1, y + bh / 2, x + bw + 17, y + bh / 2, color=MUTED)
            else:
                arrow(d, x - 1, y + bh / 2, x - 17, y + bh / 2, color=MUTED)
    return d


def fig_economy():
    W, H = CONTENT_W, 200
    d = Drawing(W, H)
    srcs = [("Bermain match", SOFTT, TEAL), ("Minigame & quest", SOFTT, TEAL), ("Event & battle pass", SOFTA, AMBER),
            ("Top-up uang asli", SOFTR, RED)]
    curs = [("GOLD", "bermain", AMBER), ("TICKET", "untuk gacha", VIOLET), ("MiCASH", "premium", RED)]
    sinks = [("Hero (juga bisa Gold)", "beli hero"), ("Sewa 7/30 hari", "Gold sink utama"),
             ("Rent-to-own", "sewa → kredit permanen"), ("Gacha transparan", "rate + pity"),
             ("Kosmetik permanen & skin", "nol stat"), ("Relic, ganti nama, dye", "Gold sink tambahan")]
    for i, (s, f, st) in enumerate(srcs):
        box(d, 0, H - 46 - i * 46, 110, 36, s, fill=f, stroke=st, tsize=8.5)
    for i, (c, s, col) in enumerate(curs):
        y = H - 58 - i * 62
        d.add(Circle(W / 2 - 40, y + 18, 26, fillColor=col, strokeColor=col))
        text(d, W / 2 - 40, y + 20, c, 8.5, "UI-B", WHITE)
        text(d, W / 2 - 40, y + 9, s, 6.8, "UI", WHITE)
    links = [(0, 0), (1, 0), (2, 1), (2, 0), (3, 2), (3, 1)]
    for si, ci in links:
        sy = H - 46 - si * 46 + 18
        cy = H - 58 - ci * 62 + 18
        arrow(d, 112, sy, W / 2 - 68, cy, color=LINE, width=1)
    sx = W - 170
    for i, (t, s) in enumerate(sinks):
        box(d, sx, H - 40 - i * 32, 170, 28, t, s, fill=SOFT, stroke=NAVY2, tsize=8, ssize=6.8)
    for ci, sis in [(0, [0, 1, 2, 5]), (1, [3]), (2, [0, 2, 4])]:
        cy = H - 58 - ci * 62 + 18
        for si in sis:
            arrow(d, W / 2 - 12, cy, sx - 2, H - 40 - si * 32 + 14, color=LINE, width=1)
    return d


def fig_roadmap():
    W, H = CONTENT_W, 175
    d = Drawing(W, H)
    phases = [
        ("Fase 0", "Desain & riset", "SELESAI", TEAL, 0, 0.16),
        ("Fase 1", "Spike netcode + uji Quantum", "2–3 minggu", RED, 0.16, 0.34),
        ("Fase 2", "Vertical slice (MVP)", "durasi ditetapkan setelah spike", VIOLET, 0.34, 0.66),
        ("Fase 3", "Konten & sosial", "Squad War, Relic, gacha, 5v5", AMBER, 0.66, 0.86),
        ("Fase 4", "Live-ops", "season, event, mobile", NAVY2, 0.86, 1.0),
    ]
    # left column: phase name + description; right: bar track (no text over the bars)
    x0, x1 = 200, W - 4
    row_h = 30
    top = H - 30
    for i, (p, t, s, col, a, b) in enumerate(phases):
        y = top - i * row_h
        text(d, 0, y + 9, f"{p} — {t}", 8.4, "UI-B", NAVY, "start")
        text(d, 0, y - 1, s, 7.4, "UI", MUTED, "start")
        d.add(Rect(x0, y - 2, x1 - x0, 18, rx=4, ry=4, fillColor=SOFT, strokeColor=None))
        d.add(Rect(x0 + a * (x1 - x0), y - 2, (b - a) * (x1 - x0), 18, rx=4, ry=4, fillColor=col, strokeColor=col))
    gates = [(0.16, "Gate 1: desain dikunci", 12), (0.34, "Gate 2: lulus kriteria spike", 1), (0.66, "Gate 3: MVP playtest", 12)]
    for xpos, lbl, gy in gates:
        gx = x0 + xpos * (x1 - x0)
        d.add(Line(gx, 24, gx, H - 8, strokeColor=NAVY, strokeWidth=0.6, strokeDashArray=[2, 2]))
        text(d, gx, gy, lbl, 7, "UI-SB", NAVY)
    return d


# ---------- page decorations ----------
def on_cover(c, doc):
    c.saveState()
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(NAVY2)
    c.circle(PAGE_W - 40 * mm, PAGE_H - 55 * mm, 70 * mm, fill=1, stroke=0)
    c.setFillColor(VIOLET)
    c.circle(PAGE_W - 25 * mm, PAGE_H - 95 * mm, 30 * mm, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.circle(PAGE_W - 75 * mm, PAGE_H - 120 * mm, 9 * mm, fill=1, stroke=0)
    c.setFillColor(AMBER)
    c.rect(MARGIN_X, PAGE_H - 150 * mm, 30 * mm, 2.5, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#B9BEE0"))
    c.setFont("UI-SB", 11)
    c.drawString(MARGIN_X, PAGE_H - 160 * mm, "PROPOSAL GAME  •  GAME DESIGN & TECHNICAL ARCHITECTURE")
    c.setFillColor(WHITE)
    c.setFont("UI-B", 40)
    c.drawString(MARGIN_X, PAGE_H - 180 * mm, "Nexus Saga:")
    c.drawString(MARGIN_X, PAGE_H - 196 * mm, "Chronicles")
    c.setFont("UI-L", 13)
    c.setFillColor(colors.HexColor("#D6D9F0"))
    c.drawString(MARGIN_X, PAGE_H - 210 * mm, "Social-Competitive Action RPG Hybrid")
    c.drawString(MARGIN_X, PAGE_H - 217 * mm, "Avatar sosial ala AyoDance  •  Brawler ala LostSaga  •  Ekonomi kosmetik non-P2W")
    c.setFillColor(colors.HexColor("#9AA0C8"))
    c.setFont("UI", 9.5)
    meta = [("Versi", "1.0 — Base Model Terkunci"), ("Tanggal", "24 Oktober 2026"),
            ("Status", "Siap untuk persetujuan Fase 1 (Spike)"), ("Klasifikasi", "Rahasia — internal")]
    y = 40 * mm
    for k, v in meta:
        c.setFont("UI-SB", 9.5)
        c.setFillColor(colors.HexColor("#9AA0C8"))
        c.drawString(MARGIN_X, y, k.upper())
        c.setFont("UI", 10)
        c.setFillColor(WHITE)
        c.drawString(MARGIN_X + 28 * mm, y, v)
        y -= 6.5 * mm
    c.restoreState()


def on_page(c, doc):
    c.saveState()
    c.setFillColor(NAVY)
    c.rect(0, PAGE_H - 12 * mm, PAGE_W, 12 * mm, fill=1, stroke=0)
    c.setFillColor(VIOLET)
    c.rect(0, PAGE_H - 12 * mm - 1.6, PAGE_W, 1.6, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("UI-B", 9)
    c.drawString(MARGIN_X, PAGE_H - 7.6 * mm, "NEXUS SAGA: CHRONICLES")
    c.setFont("UI", 8.5)
    c.setFillColor(colors.HexColor("#B9BEE0"))
    c.drawRightString(PAGE_W - MARGIN_X, PAGE_H - 7.6 * mm, "Proposal Game v1.0")
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    c.line(MARGIN_X, 14 * mm, PAGE_W - MARGIN_X, 14 * mm)
    c.setFont("UI", 8)
    c.setFillColor(MUTED)
    c.drawString(MARGIN_X, 9.5 * mm, "Rahasia — hanya untuk penggunaan internal")
    c.drawRightString(PAGE_W - MARGIN_X, 9.5 * mm, f"Halaman {doc.page}")
    c.restoreState()


class Doc(BaseDocTemplate):
    def __init__(self, fn, **kw):
        super().__init__(fn, pagesize=A4, title="Nexus Saga: Chronicles — Proposal Game",
                         author="Tim Pengembang Nexus Saga", subject="Game Design & Technical Proposal", **kw)
        cover = Frame(0, 0, PAGE_W, PAGE_H, id="cover", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        body = Frame(MARGIN_X, 20 * mm, CONTENT_W, PAGE_H - 20 * mm - 22 * mm, id="body",
                     leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([PageTemplate("cover", [cover], onPage=on_cover),
                               PageTemplate("normal", [body], onPage=on_page)])

    def afterFlowable(self, f):
        if isinstance(f, H1):
            self.notify("TOCEntry", (0, f.toc_text, self.page))


# ---------- content ----------
story = [Spacer(1, 1), NextPageTemplate("normal"), PageBreak()]

# TOC
toc = TableOfContents()
toc.levelStyles = [ST["toc1"]]
toc.dotsMinLevel = 0
story += [Paragraph("DAFTAR ISI", ST["kicker"]), Paragraph("Isi Proposal", ST["h1"]), Spacer(1, 12), toc, PageBreak()]

# 1 Executive summary
story += chapter(1, "Ringkasan Eksekutif", "Gambaran satu halaman")
story += [P("<b>Nexus Saga: Chronicles</b> adalah game PC online bergenre <b>Social-Competitive Action RPG Hybrid</b>. "
            "Pemain memiliki <b>avatar</b> yang menjadi identitas dirinya, bersosialisasi di sebuah kota (Plaza), lalu "
            "bertarung dalam tim memakai <b>hero</b> berupa set senjata dan pakaian perang yang bisa rontok di tengah "
            "pertarungan. Monetisasi hanya melalui kosmetik, sehingga game tetap adil dan tidak pay-to-win.", "lead")]
story.append(table([
    ["Aspek", "Ringkasan"],
    ["Genre", "Social-Competitive Action RPG Hybrid (brawler tim + hub sosial avatar)"],
    ["Referensi utama", "AyoDance (avatar & lobi sosial), LostSaga (combat & gear), Roblox (ekonomi kosmetik, live-ops), Dota 2/MLBB (rank & statistik)"],
    ["Platform", "PC terlebih dahulu; mobile pada fase berikutnya"],
    ["Rating umur", "13+; couple/dating room khusus 18+ dengan verifikasi umur"],
    ["Format pertandingan", "1v1 sampai 5v5; mode Survival (ronde) dan Team Deathmatch"],
    ["Kamera", "Arena 3D free-roam (gerak 8 arah) dengan kamera quarter-view terkunci"],
    ["Monetisasi", "3 mata uang (Gold, Ticket, MiCash); sewa 7/30 hari/permanen; rent-to-own; gacha transparan; nol stat dari uang asli"],
    ["Teknologi", "Unity (client) + Combat Core C# deterministik + game server .NET + Nakama (backend)"],
    ["Tim", "Solo architect dibantu AI; aset memakai shared humanoid rig agar animasi & kostum bisa dipakai ulang"],
    ["Status", "Desain & arsitektur dasar terkunci; siap masuk Fase 1 (spike netcode 2–3 minggu)"],
], [1.1, 3.6], first_col_bold=True))
story.append(Spacer(1, 10))
story.append(h2("Yang membuat Nexus Saga berbeda"))
story += bullets([
    "<b>Avatar adalah pemain itu sendiri.</b> Kostum yang dibeli dipakai di kota, rest room, dan arena; kostum tidak pernah lepas.",
    "<b>Pertarungan yang dramatis sampai detik terakhir.</b> HP berhenti di 0, lalu pemain masuk kondisi Critical dengan 3 Break Stock. Gear rontok satu per satu dan bisa dipungut siapa saja.",
    "<b>Swap hero di tengah combo.</b> Tiap pemain membawa 3 hero dengan satu HP bersama.",
    "<b>Dunia yang berubah karena komunitas.</b> Hasil Squad War mengubah warna dan bendera distrik di kota.",
    "<b>Adil dan transparan.</b> Uang asli hanya membeli tampilan; peluang gacha ditulis jelas dan dijamin pity.",
])
story.append(Spacer(1, 6))
story.append(callout("<b>Permintaan persetujuan:</b> menyetujui base model desain pada dokumen ini dan memulai <b>Fase 1 — Spike Netcode (2–3 minggu)</b> dengan kriteria lulus/gagal yang terukur (Bab 13).", "ok"))
story.append(PageBreak())

# 2 Vision
story += chapter(2, "Visi & Pilar Desain", "Kenapa game ini ada")
story.append(P("Visi: <b>membangun dunia game tempat pemain merasa \"hidup\" sebagai avatarnya</b> — berkumpul, tampil, "
               "berteman, dan membuktikan kemampuan di arena — dengan konten yang terus diperbarui tanpa membuat pemain "
               "yang tidak berbelanja merasa kalah.", "lead"))
story.append(table([
    ["#", "Pilar", "Artinya dalam desain"],
    ["1", "Avatar adalah identitas", "Avatar yang sama dipakai di lobi, rest room, dan arena. Uang dibelanjakan untuk tampil, bukan untuk menang."],
    ["2", "Skill > dompet", "Semua yang memengaruhi kemenangan bisa didapat dengan bermain (Gold). Cash hanya mempercepat atau mengubah tampilan."],
    ["3", "Dunia hidup tapi ringan", "Hub kota kecil + instance pertandingan terpisah, bukan MMO open-world berat."],
    ["4", "Komunitas sebagai konten", "Squad, rest room, event komunitas, perebutan distrik: pemain menjadi konten bagi sesamanya."],
    ["5", "Update terus tanpa patch berat", "Balancing, harga, event, dan drop rate disimpan sebagai data di server dan bundle ber-hash."],
], [0.3, 1.4, 3.6], first_col_bold=True))
story.append(Spacer(1, 10))
story.append(figure(fig_core_loop(), "Gambar 1 — Core loop: avatar menjadi pusat seluruh aktivitas pemain."))
story.append(h2("Target pemain"))
story.append(table([
    ["Segmen", "Motivasi", "Fitur yang melayani"],
    ["Sosial / kreatif", "Tampil, berteman, nongkrong", "Wardrobe, Plaza, Rest Room, Dance Duel, couple room 18+"],
    ["Kompetitif", "Rank, gengsi, statistik", "Ranked 1v1–5v5, tier Bronze–Mythic, profil KDA, Leader Duel"],
    ["Komunitas / squad", "Kebersamaan, wilayah", "Squad HQ, Squad War mingguan, mentor"],
    ["Kolektor", "Mengoleksi item langka", "Relic, gacha transparan, kosmetik musiman"],
], [1.1, 1.4, 2.6], first_col_bold=True))
story.append(PageBreak())

# 3 World
story += chapter(3, "Dunia, Plaza & Rest Room", "Tempat pemain berkumpul")
story.append(P("Pemain memulai di <b>Plaza</b>, sebuah kota kecil tempat 30–60 avatar berjalan, berdansa, dan mengobrol secara "
               "real-time. Dari Plaza, pemain menuju berbagai \"gate\" untuk aktivitas lain. Tampilan distrik kota berubah "
               "mengikuti hasil Squad War mingguan, dan patung pemain Mythic terbaik muncul di alun-alun."))
story.append(figure(fig_world(), "Gambar 2 — Struktur dunia: Plaza sebagai hub, aktivitas di instance terpisah."))
story.append(table([
    ["Area", "Fungsi", "Catatan desain"],
    ["Battle Gate", "Ranked, Quick Match, Custom Room ala LostSaga", "Party solo/duo/trio/5; room bisa dibuat dan diatur sendiri"],
    ["Relic Gate", "Dungeon PvE 1–4 pemain untuk farming", "Masuk dengan Gold (hadiah standar) atau Ticket (peti spesial + pity)"],
    ["Rest Room", "Ngobrol, kenalan, minigame", "Dance Duel ritme 60 detik, mancing, kuis; Gold kecil"],
    ["Couple room", "Social matching / kenalan", "Khusus 18+ terverifikasi; block, report, mute, filter chat"],
    ["Shop / Gacha / Wardrobe", "Belanja dan dandan", "Kosmetik nol stat; sewa dan permanen"],
    ["Squad HQ", "Markas squad", "Dekorasi furnitur (world building oleh pemain)"],
    ["Dev Lounge", "Area khusus developer", "Hanya akun dengan role Developer di server"],
], [1.1, 1.7, 2.4], first_col_bold=True))
story.append(PageBreak())

# 4 Avatar & hero
story += chapter(4, "Avatar, Wardrobe & Hero", "Siapa pemain di dalam game")
story.append(P("Nexus Saga memisahkan <b>avatar</b> (identitas sosial pemain) dari <b>hero</b> (kit tempur). Hero adalah "
               "set senjata dan pakaian perang yang dikenakan <b>di atas</b> kostum avatar. Dengan begitu pemain selalu "
               "tampil dengan gayanya, sedangkan lawan tetap mudah membaca hero apa yang sedang dipakai."))
story.append(figure(fig_layers(), "Gambar 3 — Lapisan visual avatar dan aturan siluet gameplay."))
story.append(h2("Komposisi hero"))
story.append(table([
    ["Slot", "Fungsi", "Bisa rontok?", "Bisa dipungut lawan?"],
    ["Senjata", "Menentukan moveset dasar dan combo", "Tidak (hanya terpental visual saat KO)", "Tidak"],
    ["Helm", "Memberi 1 skill", "Ya, saat Critical", "Ya"],
    ["Armor", "Memberi 1 skill", "Ya, saat Critical", "Ya"],
    ["Trinket", "Memberi 1 skill (jubah/aksesori)", "Ya, saat Critical", "Ya"],
], [0.9, 2.0, 1.6, 1.2], first_col_bold=True))
story.append(Spacer(1, 8))
story.append(h2("Keputusan produksi aset"))
story += bullets([
    "<b>Shared humanoid rig:</b> semua hero memakai kerangka yang sama, sehingga skill gear dan kostum bisa dipakai lintas hero, dan animasi humanoid siap pakai dapat di-retarget.",
    "<b>2 base body (laki-laki/perempuan)</b> ala AyoDance; variasi tinggi/gempal lewat bone scale dan blendshape. Setiap kostum cukup dibuat 2 kali, bukan per body type.",
    "<b>Hurtbox kapsul tunggal</b> untuk semua pemain. Avatar kecil tidak lebih sulit dipukul, sehingga body type dan kostum tidak pernah menjadi pay-to-win terselubung.",
    "Perbedaan rasa antar-hero diatur lewat <b>defense multiplier</b> dan <b>weight</b> (seberapa jauh terpental), bukan HP.",
])
story.append(PageBreak())

# 5 Combat
story += chapter(5, "Sistem Pertarungan", "Inti gameplay arena")
story.append(P("Arena berupa ruang 3D dengan kamera quarter-view terkunci, sehingga mekanik khas LostSaga seperti mengitari "
               "lawan yang sedang guard, mendorong lawan ke jurang, dan memungut gear di lantai tetap hidup. Seluruh "
               "frame data berjalan pada 60 tick per detik: 1 tick = 1 frame animasi."))
story.append(table([
    ["Aksi", "Deskripsi"],
    ["Gerak 8 arah", "Jalan dan lari bebas di bidang X/Z; lompat pada sumbu Y"],
    ["Pukul & combo", "Pukulan dapat disambung (cancel) bila mengenai lawan atau guard (movecontact)"],
    ["Juggle", "Lawan dapat dilempar ke udara dan dipukul lagi; batas juggle milik korban"],
    ["Skill", "Dari senjata dan dari gear (Helm/Armor/Trinket)"],
    ["Dash", "Gerak cepat untuk menghindar / mendekat"],
    ["Guard", "Menangkis dari arah depan 180°; memiliki guard gauge"],
    ["Interact", "Memungut gear di lantai"],
    ["Swap / Burst", "Ganti hero (Bab 6)"],
], [1.2, 4.0], first_col_bold=True))
story.append(Spacer(1, 8))
story.append(figure(fig_guard(), "Gambar 4 — Busur guard 180° dan aturan arah hadap."))
story.append(PageBreak())
story.append(h2("Status karakter"))
story.append(table([
    ["Kelompok", "State", "Catatan"],
    ["Netral", "Idle, Run, Dash, Jump/Airborne, Land", "Menerima input"],
    ["Bertahan", "Guard, Guard-hit, Guard Crush", "Guard gauge habis → Faint"],
    ["Menyerang", "Serangan & skill (dari data hero), Grab", "Cancel via contact / hit-confirm"],
    ["Terkena", "Hit, Launched, Fall, Bounce, Down, Get-up", "Get-up memiliki i-frame penuh"],
    ["Kontrol", "Faint/Stun, Frozen, Bound", "Durasi ditentukan oleh HitDef penyerang"],
    ["Khusus", "DropZone Fall, Return, Swap Out/In, KO, Respawn", "Lihat Bab 6"],
], [1.0, 2.6, 2.0], first_col_bold=True))
story.append(Spacer(1, 6))
story.append(h2("Hero MVP (vertical slice)"))
story.append(table([
    ["Hero", "Arketipe", "State yang diuji"],
    ["Pegulat", "Melee / Grappler", "Dash, Guard, Hitstun, Bound (grab), Down, i-frame bangun, gear rontok"],
    ["Zoner", "Ranged / kontrol area", "Airborne (launcher), Faint, Frozen, proyektil vs guard"],
    ["(Fase 3) Support", "Pelindung / escape", "Shield, buff gerak; heal tidak berlaku saat Critical"],
], [1.0, 1.3, 3.2], first_col_bold=True))
story.append(Spacer(1, 8))
story.append(callout("<b>Prinsip data-driven:</b> reaksi korban (stagger, terpental, pingsan, beku) ditentukan oleh data serangan penyerang (HitDef), mengikuti model engine fighting game Ikemen GO. Balancing cukup mengubah data, tanpa mengubah kode.", "info"))
story.append(PageBreak())

# 6 Survival
story += chapter(6, "Nyawa, Gear Drop & Hero Swap", "Aturan yang membuat setiap match dramatis")
story.append(P("Prinsip utama: <b>tidak ada pemain yang mati karena satu kejadian.</b> Satu-satunya jalan menuju KO adalah "
               "melalui kondisi Critical dan pecahnya 3 Break Stock."))
story.append(figure(fig_life(), "Gambar 5 — Alur nyawa: HP → Damage Gate → Critical (3 Break Stock) → KO."))
story.append(h2("Gear di lantai"))
story.append(table([
    ["Aturan", "Detail"],
    ["Siapa cepat dia dapat", "Helm, Armor, Trinket bisa dipungut siapa saja termasuk lawan; senjata tidak"],
    ["Efek pickup", "Memberi skill gear tersebut sampai rontok lagi atau KO; tampil versi default (MVP: aura/ikon)"],
    ["Satu slot satu gear", "Memungut saat slot terisi = menukar (gear lama jatuh)"],
    ["Tidak menambah nyawa", "Break Stock selalu 3, tidak bergantung jumlah gear"],
    ["Milik match", "Inventory dan kepemilikan item pemilik asli tidak pernah berubah"],
], [1.5, 4.0], first_col_bold=True))
story.append(PageBreak())
story.append(h2("DropZone (jurang)"))
story.append(figure(fig_arena(), "Gambar 6 — Contoh layout arena dan alur pemain yang jatuh ke DropZone."))
story.append(h2("Hero Swap"))
story.append(P("Setiap pemain membawa <b>3 hero</b> dalam satu match (MVP memproduksi 2 hero). HP milik pemain, bukan milik hero."))
story.append(table([
    ["Jenis swap", "Kapan boleh", "Cooldown", "Efek"],
    ["Swap biasa", "Idle/Run/Jump, atau setelah serangan kena/di-guard", "3 detik", "Menyambung combo"],
    ["Burst Swap", "Saat hitstun, atau membatalkan recovery serangan yang meleset", "12 detik", "Pushback + i-frame singkat"],
    ["Terkunci", "Saat Critical (HP 0)", "—", "Mencegah \"nyawa tambahan\" dari hero lain"],
], [1.0, 2.4, 0.8, 1.6], first_col_bold=True))
story.append(Spacer(1, 6))
story += bullets([
    "Satu <b>timer cooldown bersama</b>; durasinya mengikuti jenis swap terakhir.",
    "<b>Batas juggle milik korban</b>, sehingga swap tidak bisa membuat combo tanpa batas.",
    "Swap dari serangan yang meleset hanya bisa dengan Burst (12 detik), sehingga serangan berat tetap berisiko.",
])
story.append(PageBreak())

# 7 Modes & rank
story += chapter(7, "Mode, Matchmaking & Rank", "Struktur kompetitif")
story.append(table([
    ["Mode", "Format", "Aturan", "Penentu pemenang"],
    ["Survival / Elimination", "1v1, 3v3; ronde 90–120 detik", "KO = tereliminasi sampai ronde berikutnya; nyawa baru tiap ronde",
     "Anggota hidup → total stock → total % HP → sudden death 20 detik (Break Meter 2×)"],
    ["Team Deathmatch", "Sampai 5v5", "Respawn; jeda naik mengikuti waktu match (5 s → 10 s), sama untuk semua pemain",
     "Skor KO tim / waktu habis"],
    ["Custom Room", "Bebas", "Room ala LostSaga: buat, atur tim, ready", "Sesuai mode"],
    ["Relic (PvE)", "1–4 pemain", "Farming material, avatar item, relic", "—"],
], [1.2, 1.1, 2.0, 1.8], first_col_bold=True))
story.append(Spacer(1, 6))
story.append(callout("<b>Kenapa respawn tidak bertambah per kematian?</b> Timer yang naik per individu membuat tim yang sedang kalah makin lama hidup kembali (snowball). Timer berbasis waktu match menjaga peluang comeback.", "warn"))
story.append(h2("Rank & MMR"))
story.append(table([
    ["Komponen", "Desain"],
    ["Tier", "Bronze → Silver → Gold → Platinum → Diamond → Mythic (+ leaderboard Top 100)"],
    ["Dua angka", "Hidden MMR (matchmaking, rating Bayesian tim, mis. OpenSkill) dan Rank Points yang terlihat"],
    ["Party", "Solo/duo/trio/5; party besar hanya melawan party ≥ 3"],
    ["Season", "8–10 minggu, soft reset"],
    ["KO", "Pemecah Break Stock terakhir; jatuh ke jurang → musuh terakhir yang memukul (10 detik)"],
    ["Assist", "Siapa pun yang memberi damage/break dalam 10 detik terakhir"],
    ["Profil", "Win rate, KDA, hero favorit, statistik per hero, riwayat match, peak tier per season"],
], [1.1, 4.2], first_col_bold=True))
story.append(PageBreak())

# 8 Social
story += chapter(8, "Komunitas & Keamanan Sosial", "Pemain sebagai konten")
story.append(table([
    ["Fitur", "Deskripsi", "Nilai bagi game"],
    ["Squad & Squad HQ", "Guild dengan markas yang bisa didekorasi", "Retensi, identitas kelompok"],
    ["Squad War mingguan", "Perebutan distrik di Plaza", "Dunia berubah karena komunitas"],
    ["Leader Duel", "Ketua squad duel 1v1, tayang di layar Plaza", "Momen tontonan & gengsi"],
    ["Mentor", "Pemain Diamond+ membimbing pemula; hadiah bersama", "Onboarding & komunitas sehat"],
    ["Dance Duel", "Minigame ritme 60 detik", "Jembatan sosial–kompetitif (DNA AyoDance)"],
    ["Rest Room", "Ruang santai, mancing, kuis", "Istirahat dari mode kompetitif"],
], [1.3, 2.4, 1.8], first_col_bold=True))
story.append(Spacer(1, 8))
story.append(h2("Keselamatan pemain (wajib sejak awal)"))
story += bullets([
    "Rating 13+; couple/dating room <b>hanya 18+</b> dengan verifikasi umur.",
    "Block, report, mute, filter chat, dan moderator.",
    "Seluruh aksi moderator/GM dicatat di audit log.",
    "Klasifikasi gim nasional (IGRS) dan pendaftaran PSE diverifikasi ke sumber resmi sebelum rilis.",
])
story.append(PageBreak())

# 9 Economy
story += chapter(9, "Ekonomi & Monetisasi", "Adil, transparan, berkelanjutan")
story.append(figure(fig_economy(), "Gambar 7 — Aliran tiga mata uang dari sumber ke penggunaan."))
story.append(table([
    ["Mata uang", "Sumber", "Penggunaan"],
    ["Gold", "Match, minigame, quest harian", "Hero, sewa kosmetik 7/30 hari, masuk Relic, ganti nama, dye"],
    ["Ticket", "Quest, event, battle pass, pembelian", "Gacha"],
    ["MiCash", "Uang asli", "Kosmetik permanen, skin & efek skill, battle pass premium, hero (alternatif cepat)"],
], [0.9, 1.9, 3.0], first_col_bold=True))
story.append(Spacer(1, 8))
story.append(h2("Aturan anti pay-to-win"))
story.append(table([
    ["Aturan", "Penjelasan"],
    ["Kosmetik nol stat", "Kostum, skin, dan efek tidak mengubah damage, defense, hitbox, atau timing"],
    ["Hero juga dijual Gold", "Hero MiCash dapat dibeli dengan Gold (mis. 2 minggu setelah rilis)"],
    ["Durasi hanya untuk kosmetik", "Sewa 7/30 hari/permanen tidak berlaku untuk stat"],
    ["Rent-to-own", "Sebagian biaya sewa menjadi kredit pembelian permanen — Gold sink utama"],
    ["Gacha transparan", "Rate dipublikasikan, pity terlihat, duplikat menjadi shard"],
    ["Sewa habis di tengah match", "Tetap berlaku sampai match selesai (dicek saat kunci loadout)"],
], [1.5, 4.0], first_col_bold=True))
story.append(PageBreak())

# 10 Liveops & dev
story += chapter(10, "Live-Ops & Developer Mode", "Game yang terus diperbarui")
story.append(table([
    ["Elemen", "Rencana"],
    ["Season", "8–10 minggu: soft reset rank, battle pass kosmetik, hero/skin baru"],
    ["Event mingguan", "Double Gold, Relic khusus, turnamen Leader Duel"],
    ["Content bundle ber-hash", "Data hero/balancing diunduh saat login dari CDN; balancing tanpa update store"],
    ["Data ekonomi", "Harga, drop rate, jadwal event disimpan di server (Nakama)"],
], [1.4, 4.0], first_col_bold=True))
story.append(Spacer(1, 10))
story.append(h2("Developer Mode"))
story.append(P("Developer mode <b>tidak</b> berupa flag di aplikasi pemain (yang mudah di-patch cheater). Hak akses ditentukan oleh "
               "<b>role di server</b>; aplikasi hanya menampilkan panel bila server mengizinkan, dan setiap perintah divalidasi "
               "server serta dicatat."))
story.append(table([
    ["Role", "Kemampuan"],
    ["Player", "Bermain normal"],
    ["Mentor", "Fitur bimbingan pemula"],
    ["Moderator", "Mute, kick, laporan"],
    ["GM", "Ban, event, bantuan pemain"],
    ["Developer", "Spawn item, ubah cuaca Plaza, set MMR untuk testing, akses Dev Lounge"],
], [1.1, 4.2], first_col_bold=True))
story.append(PageBreak())

# 11 Tech architecture
story += chapter(11, "Arsitektur Teknis", "Bagaimana game ini dibangun")
story.append(figure(fig_arch(), "Gambar 8 — Arsitektur sistem: Combat Core yang sama berjalan di client dan server."))
story.append(table([
    ["Lapisan", "Pilihan", "Alasan"],
    ["Client", "Unity (C#)", "Pipeline avatar, wardrobe, dan retarget humanoid paling matang; siap untuk mobile"],
    ["Combat Core", "Library C# murni, deterministik, fixed-point, data-oriented", "Kode identik di client (prediksi) dan server (otoritas); tanpa UnityEngine dan tanpa root motion"],
    ["Game server", ".NET 8 console + UDP (LiteNetLib)", "Ringan dan murah; banyak match per proses"],
    ["Meta backend", "Nakama + PostgreSQL", "Akun, party, chat, squad, matchmaker, leaderboard, wallet sudah tersedia"],
    ["Plaza", "Nakama authoritative match (Go), 10–15 Hz", "Tidak butuh combat; gerak dicek kewajarannya"],
    ["Konten", "Addressables + CDN, ber-hash", "Update data tanpa patch store"],
    ["Cadangan", "Photon Quantum", "Dipakai bila spike netcode custom tidak lulus"],
], [1.0, 1.9, 2.6], first_col_bold=True))
story.append(PageBreak())
story.append(h2("Pipeline per tick (60 Hz)"))
story.append(table([
    ["Tahap", "Proses"],
    ["T0", "Kumpulkan input per tick (input terlambat dipakai di tick berikutnya)"],
    ["T1", "Update command buffer (dibekukan selama hitpause)"],
    ["T2–T3", "Command → perubahan state; jalankan controller state aktif (re-run maks 4×)"],
    ["T4", "Physics: velocity, gravitasi, friksi, collision arena; simpan lastGroundedPos"],
    ["T5", "Push resolution antar karakter (urut entity id)"],
    ["T6", "Hit detection 3D (urut prioritas lalu id), hurtbox korban di-rewind (lag compensation ≤ 150 ms)"],
    ["T7", "Hasil hit: hitpause, damage (Damage Gate), Break Meter/Stock, antrian reaksi"],
    ["T8", "Loadout: gear drop/pickup, Hero Swap"],
    ["T9–T10", "Timer & animasi; quantize state; server membangun snapshot"],
], [0.8, 4.6], first_col_bold=True))
story.append(Spacer(1, 8))
story.append(h2("Netcode"))
story.append(table([
    ["Aspek", "Desain"],
    ["Input", "Struct ukuran tetap per tick berisi arah 8, tombol, dan aimYaw (aim-assist dihitung client, divalidasi server ±22,5°); 3 input terakhir dikirim redundan"],
    ["Snapshot", "Per penonton, 30–60 Hz, delta terhadap snapshot yang sudah di-ack, CRC + resync; target < 1 KB untuk 10 pemain"],
    ["Prediksi", "Rollback-replay pemain lokal; reaksi korban diprediksi dari HitDef (predicted hit reaction)"],
    ["Pemain lain", "Interpolasi; koreksi dihaluskan hanya pada transform visual"],
    ["Reliable", "KO, Hero Swap, Gear Drop/pickup, akhir match disimpan sebagai state persisten"],
], [1.0, 4.4], first_col_bold=True))
story.append(PageBreak())

# 12 Flow & security
story += chapter(12, "Alur Lobi → Match & Keamanan", "Dari kota ke arena dan kembali")
story.append(figure(fig_flow(), "Gambar 9 — Delapan langkah dari Plaza ke pertandingan dan kembali."))
story.append(table([
    ["Ancaman", "Perlindungan"],
    ["Memalsukan hadiah / MMR", "Hasil match hanya dari laporan game server ke Nakama (server-to-server), idempoten per matchId"],
    ["Hack aplikasi (speed, damage)", "Server-authoritative; client hanya mengirim input"],
    ["Bobol developer mode", "Role di server + audit log; tidak ada otorisasi di client"],
    ["Transaksi ganda", "Ledger wallet + idempotency key (matchId/orderId)"],
    ["Masuk match tanpa izin", "Tiket join bertanda tangan dengan TTL pendek"],
    ["Data balancing berbeda", "Hash konten wajib cocok sebelum join"],
    ["Disconnect", "Tiket diterbitkan ulang dalam jendela ±60 detik; slot ditahan"],
], [1.6, 3.9], first_col_bold=True))
story.append(PageBreak())

# 13 Roadmap
story += chapter(13, "Rencana Produksi", "Bertahap dengan gerbang keputusan")
story.append(figure(fig_roadmap(), "Gambar 10 — Fase produksi dan gerbang keputusan. Durasi Fase 2 ke atas ditetapkan setelah hasil spike."))
story.append(h2("Fase 1 — Spike netcode: kriteria lulus"))
story.append(P("Diuji pada kondisi jaringan buatan: <b>ping 150 ms, jitter 20 ms, packet loss 2%</b>. Selama spike, Photon Quantum juga diuji 2–3 hari sebagai pembanding."))
story.append(table([
    ["#", "Metrik", "Target", "Jika gagal"],
    ["1", "Reaksi korban terlihat di layar penyerang", "≤ 1 frame setelah hit-confirm lokal", "Evaluasi Photon Quantum"],
    ["2", "Hit-confirm / combat state misprediction", "< 5% (koreksi gerak biasa tidak dihitung)", "Evaluasi Photon Quantum"],
    ["3", "Koreksi posisi korban setelah rollback", "< 0,5 m pada 95% kasus, dihaluskan ≤ 6 frame", "Evaluasi Photon Quantum"],
    ["4", "Kapasitas server", "≥ 20 match 10 pemain per 1 vCPU", "Optimasi"],
    ["5", "Bandwidth", "< 64 kbps per pemain", "Optimasi"],
], [0.3, 2.0, 2.0, 1.3], first_col_bold=True))
story.append(Spacer(1, 8))
story.append(h2("Fase 2 — Vertical slice (MVP)"))
story.append(table([
    ["Komponen", "Isi"],
    ["Akun & role", "Login, role Player/GM/Developer"],
    ["Plaza", "1 distrik, chat, emote"],
    ["Wardrobe & toko", "5 slot kostum, toko Gold (sewa/permanen)"],
    ["Arena", "1v1 dan 2v2, 2 hero (Pegulat + Zoner), Critical, Gear Drop, DropZone"],
    ["Kompetitif", "MMR, tier, profil sederhana"],
    ["Developer", "Panel spawn item, set MMR, kick/ban dengan audit log"],
    ["Tooling", "Hitbox editor di Unity (wajib sebelum hero kedua)"],
], [1.3, 4.2], first_col_bold=True))
story.append(PageBreak())

# 14 Risks
story += chapter(14, "Risiko & Mitigasi", "Dinilai secara jujur")
story.append(table([
    ["Risiko", "Dampak", "Mitigasi"],
    ["Netcode custom adalah bagian tersulit", "Tinggi", "Spike 2–3 minggu dengan kriteria terukur; cadangan Photon Quantum; Core data-oriented agar mudah dipindah"],
    ["Rasa combo saat lag (reaksi korban remote)", "Tinggi", "Predicted hit reaction dari HitDef; menjadi kriteria lulus spike"],
    ["Kapasitas tim solo: konten 3D/animasi", "Tinggi", "Shared humanoid rig, animasi siap pakai, gaya stylized, hitbox editor"],
    ["Biaya wardrobe per body type", "Sedang", "2 base body + bone scale/blendshape"],
    ["Data client/server tidak sinkron", "Sedang", "Hash konten wajib di setiap match"],
    ["Durasi ronde terlalu panjang (HP + 3 stock)", "Sedang", "TTK diukur di prototipe; tie-break & sudden death"],
    ["Regulasi (rating umur, gacha, PSE)", "Sedang", "Verifikasi ke sumber resmi sebelum rilis; rate gacha dipublikasikan"],
    ["Lisensi / hak cipta referensi", "Sedang", "Riset clean-room: hanya mempelajari desain; tidak menyalin kode, aset, atau data"],
], [1.7, 0.7, 3.1], first_col_bold=True))
story.append(PageBreak())

# 15 Research basis
story += chapter(15, "Dasar Riset", "Dari mana desain ini berasal")
story.append(table([
    ["Sumber", "Metode", "Yang diambil"],
    ["Ikemen GO v1.0.0 (open-source)", "Membaca source code", "Model state data-driven, urutan proses per frame, HitDef, juggle, cancel, buffer input"],
    ["DDNet 20.1.1 (open-source)", "Membaca source code", "Tick tetap, input per tick, snapshot delta, prediksi & rekonsiliasi, quantize"],
    ["AyoDance (client lokal)", "Analisis statis file", "Struktur avatar/wardrobe & lobi (dijadwalkan setelah core combat)"],
    ["LostSaga (client LSRebirth)", "Analisis statis + observasi", "Identitas mekanik gear & arena; biner terproteksi tidak dibongkar"],
    ["Algoritma publik", "Dokumentasi", "OpenSkill/Glicko-2 untuk MMR; Nakama untuk backend"],
], [1.6, 1.3, 2.7], first_col_bold=True))
story.append(Spacer(1, 8))
story.append(callout("<b>Etika riset:</b> seluruh analisis bersifat clean-room. Kami mempelajari desain dan perilaku, lalu menulis spesifikasi dan kode sendiri. Proteksi anti-cheat/packer tidak dibongkar, game ber-anti-cheat tidak dijalankan di bawah debugger, dan tidak ada kode, aset, atau data milik pihak lain yang disalin.", "ok"))
story.append(h2("Dokumentasi pendukung"))
story.append(P("Seluruh keputusan tercatat di repositori proyek (folder <b>docs/</b>): visi (01), matriks referensi (02), peta sistem (04), "
               "kamera & avatar (06), arsitektur core combat (08), arsitektur sistem (09), review kritis (10), "
               "konsep bahasa sederhana (11), dan decision log (90)."))
story.append(PageBreak())

# 16 Decision & next steps
story += chapter(16, "Keputusan Terkunci & Langkah Berikutnya", "Ringkasan untuk persetujuan")
story.append(table([
    ["Area", "Keputusan"],
    ["Kamera & arena", "3D free-roam 8 arah, kamera quarter-view terkunci, maks 5v5"],
    ["Guard", "Depan 180°, lock facing + pivot, auto-face 6 m, guard gauge"],
    ["Nyawa", "Damage Gate HP 0 → Critical 3 Break Stock → KO; maks 1 stock per combo"],
    ["Gear", "Helm/Trinket/Armor rontok saat Critical; pickup siapa cepat; senjata tidak pernah rontok"],
    ["DropZone", "Bukan KO; fall damage/pecah stock; gear ejection; Sky-Drop + stagger"],
    ["Hero", "3 hero per match, HP bersama; swap 3 s / Burst 12 s, terkunci saat Critical"],
    ["Mode", "Survival (ronde 90–120 s) dan TDM (respawn berbasis waktu match)"],
    ["Ekonomi", "Gold/Ticket/MiCash, nol stat, sewa + rent-to-own, gacha transparan"],
    ["Teknologi", "Unity + Core C# + .NET server + Nakama; content bundle ber-hash"],
    ["Aset", "Shared humanoid rig, 2 base body, hurtbox kapsul tunggal"],
], [1.2, 4.3], first_col_bold=True))
story.append(Spacer(1, 10))
story.append(h2("Yang dimohonkan"))
story.append(table([
    ["#", "Permohonan", "Keterangan"],
    ["1", "Persetujuan base model desain", "Seluruh keputusan pada dokumen ini"],
    ["2", "Persetujuan Fase 1 — Spike netcode", "2–3 minggu; hasil berupa laporan metrik lulus/gagal"],
    ["3", "Sumber daya Fase 1", "Lisensi Unity sesuai ketentuan, 1 VPS uji (region Asia Tenggara), akses asset store/animasi"],
    ["4", "Review hasil spike", "Gerbang keputusan: lanjut custom netcode atau Photon Quantum"],
], [0.3, 2.0, 3.2], first_col_bold=True))
story.append(Spacer(1, 10))
story.append(callout("Setelah spike lulus, durasi dan kebutuhan Fase 2 (vertical slice) akan diajukan dengan estimasi yang didasarkan pada data hasil spike, bukan perkiraan awal.", "info"))

# ---------- glyph check ----------
face = pdfmetrics.getFont("UI").face
missing = set()
import re
for t in ALL_TEXT:
    plain = re.sub(r"<[^>]+>", "", str(t)).replace("&amp;", "&")
    for ch in plain:
        if ord(ch) > 127 and ord(ch) not in face.charWidths:
            missing.add(ch)
if missing:
    print("MISSING GLYPHS:", [hex(ord(c)) + " " + c for c in missing])
    sys.exit(2)

doc = Doc(OUT, leftMargin=MARGIN_X, rightMargin=MARGIN_X, topMargin=22 * mm, bottomMargin=20 * mm)
doc.multiBuild(story)
print("OK", OUT)




