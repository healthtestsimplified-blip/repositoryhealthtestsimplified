import math, sys, random
from cbc_cartoon import run
from chromo_cartoon import x_shape, PINK, SKYB
from dmarker_cartoon import MOM, LAV
from lft_cartoon2 import *

random.seed(11)
FRAGS = [(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(0, 6.28), random.random() < 0.15) for _ in range(140)]
FRAGS = [f for f in FRAGS if f[0] ** 2 + f[1] ** 2 < 0.75][:60]

def frag(d, x, y, a, col, L=60):
    dx, dy = L / 2 * math.cos(a), L / 2 * math.sin(a); nx, ny = -math.sin(a) * 9, math.cos(a) * 9
    d.line((x - dx + nx, y - dy + ny, x + dx + nx, y + dy + ny), fill=col, width=6)
    d.line((x - dx - nx, y - dy - ny, x + dx - nx, y + dy - ny), fill=col, width=6)
    for k in range(5):
        f = -0.4 + k * 0.2; d.line((x + dx * 2 * f + nx, y + dy * 2 * f + ny, x + dx * 2 * f - nx, y + dy * 2 * f - ny), fill=col, width=4)

def blood_zoom(fr, cx, cy, R, t, p=1.0, hl=False):
    d = ImageDraw.Draw(fr)
    d.ellipse((cx - R - 12, cy - R - 12, cx + R + 12, cy + R + 12), fill=(150, 20, 40))
    d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=(255, 225, 228))
    n = int(len(FRAGS) * max(0, min(1, p)))
    for (x, y, a, baby) in FRAGS[:n]:
        X = cx + x * R + 8 * math.sin(t * 2 + a * 3); Y = cy + y * R + 8 * math.cos(t * 1.7 + a * 2)
        col = SKYB if baby else (236, 64, 122)
        if hl and baby: d.ellipse((X - 42, Y - 42, X + 42, Y + 42), outline=YEL, width=6)
        frag(d, X, Y, a + t * 0.3, col)

def cmp_table():
    rows = [("", "Double marker", "NIPT"), ("When", "11–14 weeks", "From 10 weeks"), ("Sample", "Blood + NT scan", "Blood only"),
            ("Down syndrome detection", "about 85–90%", "over 99%"), ("Cost", "Lower", "Higher")]
    colw = [360, 300, 300]; rh = 112; tw = sum(colw); x0 = (W - tw) // 2
    im = Image.new("RGBA", (W, rh * len(rows) + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((x0, 0, x0 + tw, rh * len(rows)), 28, fill=WHITE, outline=(200, 215, 235), width=3)
    d.rounded_rectangle((x0 + colw[0] + 8, 8, x0 + colw[0] + colw[1] - 8, rh - 8), 20, fill=PINK)
    d.rounded_rectangle((x0 + colw[0] + colw[1] + 8, 8, x0 + tw - 8, rh - 8), 20, fill=SKYB)
    for r, row in enumerate(rows):
        y = r * rh + rh / 2; x = x0
        for c, cell in enumerate(row):
            if r == 0: f, col = font("Bold", 34), WHITE
            elif c == 0: f, col = font("Bold", 30), DBLUE
            else: f, col = font("Bold", 32), (PINK if c == 1 else SKYB)
            lines = cell.split(" ") if (c == 0 and len(cell) > 14) else [cell]
            if len(lines) > 1: lines = [" ".join(lines[:2]), " ".join(lines[2:])]
            for j, l in enumerate(lines):
                d.text((x + colw[c] / 2, y + (j - (len(lines) - 1) / 2) * 36), l, font=f, fill=col, anchor="mm")
            x += colw[c]
        if 0 < r < len(rows) - 1: d.line((x0 + 24, (r + 1) * rh, x0 + tw - 24, (r + 1) * rh), fill=(225, 232, 242), width=2)
    return im

# ---------------- scenes ----------------
def p_hook(fr, t, D):
    rays(fr, 540, 900, t, (120, 170, 255), a=40)
    put(fr, MOM, 540, 1390 + 8 * math.sin(t * 2), 0.8)
    pop(fr, white_text("Double marker says HIGH RISK?", 80), 540, 560, t, 0.1, "boom")
    pop(fr, white_text("Don't panic! Know about NIPT", 64, color=YEL), 540, 790, t, 1.8, "whoosh")
    pop(fr, box_text("Watch till the end: a safe & more accurate next step", GREEN, 38), 540, 990, t, D * 0.55, "pop")

def p_what(fr, t, D):
    show(fr, pill("WHAT IS NIPT?", SKYB, size=50), 230, t, 0.1)
    ground(fr, 230, 900, 300); put(fr, MOM, 230, 610, 0.75)
    blood_zoom(fr, 720, 600, 245, t, (t - 0.3) / (D * 0.4), hl=t > D * 0.5); fire("whoosh", 0.3)
    d = ImageDraw.Draw(fr)
    if t > D * 0.5:
        d.text((720, 895), "Blue = baby's DNA pieces", font=font("Bold", 36), fill=SKYB, anchor="mm")
    fire("ding", D * 0.5)
    show(fr, text_el("Mother's blood carries tiny pieces of baby's DNA!", 48, color=DBLUE), 960, t, D * 0.55)
    show(fr, card("Non-Invasive Prenatal Test: just a blood sample", GREEN, "✓", size=40), 1130, t, D * 0.7)
    fire("pop", D * 0.7)

def p_when(fr, t, D):
    show(fr, pill("WHEN CAN IT BE DONE?", GREEN, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr); x0, x1, y = 90, 990, 560
    X = lambda wk: x0 + (x1 - x0) * wk / 40
    d.rounded_rectangle((x0, y, x1, y + 60), 30, fill=(230, 236, 245))
    for wk in (0, 10, 20, 30, 40): d.text((X(wk), y + 100), f"{wk}", font=font("Bold", 32), fill=GREY, anchor="mm")
    d.text((540, y + 150), "weeks of pregnancy", font=font("Medium", 32), fill=GREY, anchor="mm")
    p = ease((t - 0.4) / (D * 0.4))
    if t > 0.4:
        d.rounded_rectangle((X(10), y - 10, X(10) + (X(40) - X(10)) * p, y + 70), 30, fill=SKYB)
        d.text((X(10) + 120, y - 60), "NIPT: from 10 weeks", font=font("Bold", 40), fill=SKYB, anchor="mm")
    fire("whoosh", 0.4)
    show(fr, card("Results usually in about 1–2 weeks", ORANGE, "◷", size=40), 820, t, D * 0.55)
    show(fr, card("Safe for baby: no needle near the womb", GREEN, "✓", size=40), 960, t, D * 0.7)
    fire("pop", D * 0.55); fire("pop", D * 0.7)

def p_checks(fr, t, D):
    show(fr, pill("WHAT DOES NIPT SCREEN FOR?", BLUE, size=44), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    if t > 0.4:
        for k in range(3): x_shape(d, 400 + k * 140, 470, 110, (120, 70, 200) if k < 2 else RED)
        d.text((540, 590), "Extra chromosome check", font=font("Bold", 40), fill=RED, anchor="mm")
    fire("pop", 0.4)
    items = [("Down syndrome (chromosome 21)", PURPLE, "1"), ("Edwards syndrome (chromosome 18)", BLUE, "2"),
             ("Patau syndrome (chromosome 13)", TEAL, "3")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.2 + 0.13 * i)); show(fr, card(txt, c, m, size=40), 680 + i * 135, t, D * (0.2 + 0.13 * i))
    pop(fr, box_text("Detects over 99% of Down syndrome cases", GREEN, 42), 540, 1150, t, D * 0.62, "ding")
    show(fr, text_el("Baby's sex is NOT disclosed: illegal in India", 38, "Bold", ORANGE), 1290, t, D * 0.78)

def p_compare(fr, t, D):
    show(fr, pill("DOUBLE MARKER vs NIPT", LAV, size=48), 230, t, 0.1)
    fire("pop", 0.5); show(fr, cmp_table(), 400, t, 0.5)
    show(fr, text_el("Your doctor will suggest what suits you", 44, "Medium", GREEN), 1020, t, D * 0.7)
    show(fr, text_el("Screenshot this!", 44, "Bold", TEAL), 1110, t, D * 0.8)

def p_result(fr, t, D):
    show(fr, pill("READING THE RESULT", ORANGE, size=48), 230, t, 0.1)
    items = [("LOW RISK", "Very reassuring", GREEN), ("HIGH RISK", "Confirm with CVS or amniocentesis", RED),
             ("NO RESULT", "Sometimes a repeat sample is needed", ORANGE)]
    d = ImageDraw.Draw(fr)
    for i, (a, b, c) in enumerate(items):
        tin = 0.4 + i * D * 0.18; fire("pop", tin)
        if t < tin: break
        y = 380 + i * 210
        d.rounded_rectangle((70, y, W - 70, y + 180), 30, fill=WHITE, outline=c, width=8)
        d.text((W / 2, y + 60), a, font=font("Bold", 50), fill=c, anchor="mm")
        d.text((W / 2, y + 128), b, font=font("Medium", 36), fill=GREY, anchor="mm")
    pop(fr, stroke_text("STILL A SCREENING TEST", 70, PURPLE, WHITE, 7), 540, 1060, t, D * 0.72, "boom")

def p_limits(fr, t, D):
    show(fr, pill("GOOD TO KNOW", PURPLE, size=48), 230, t, 0.1)
    ground(fr, 250, 770, 300); put(fr, MOM, 250, 540, 0.6); sparkles(fr, 250, 520, 180, t, 5, (255, 150, 190))
    ground(fr, 790, 770, 300); put(fr, DOC["idle"], 790, 560, 0.7)
    items = [("Anomaly scan is still needed", BLUE, "1"), ("Doesn't check every condition", TEAL, "2"),
             ("Twins or IVF? Tell your doctor", PINK, "3"), ("Costlier than double marker", ORANGE, "4")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.12 + 0.18 * i)); show(fr, card(txt, c, m, size=40), 850 + i * 135, t, D * (0.12 + 0.18 * i))

def p_who(fr, t, D):
    show(fr, pill("WHO MAY CHOOSE NIPT?", SKYB, size=46), 230, t, 0.1)
    blood_zoom(fr, 540, 520, 190, t, 1.0)
    items = [("High risk on double marker", RED, "1"), ("Mother aged 35 or above", LAV, "2"),
             ("Past pregnancy with chromosome issue", PURPLE, "3"), ("Wants a more accurate screen", GREEN, "4")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.12 + 0.17 * i)); show(fr, card(txt, c, m, size=38), 770 + i * 135, t, D * (0.12 + 0.17 * i))
    show(fr, text_el("Always as your doctor advises", 42, "Medium", GREEN), 1330, t, D * 0.85)

def p_close(fr, t, D):
    show(fr, big_logo(), 210, t, 0.2)
    fire("ding", 0.8); show(fr, box_text("Take any medicine only as advised by your doctor", GREEN, 42), 820, t, 0.8)
    show(fr, text_el("Had you heard of NIPT before?", 54, color=DBLUE), 1020, t, D * 0.45)
    show(fr, text_el("Share with every mother-to-be you know!", 44, "Medium", GREY), 1120, t, D * 0.55)
    show(fr, pill("Follow Health Test Simplified", BLUE, size=40), 1300, t, D * 0.65)
    show(fr, text_el("For awareness only. Consult your doctor.", 30, "Regular", GREY), 1680, t, D * 0.7)

SC = [(p_hook, "navy"), (p_what, "light"), (p_when, "light"), (p_checks, "light"), (p_compare, "light"),
      (p_result, "light"), (p_limits, "light"), (p_who, "light"), (p_close, "light")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        D = [10, 15, 12, 15, 12, 14, 13, 13, 11]; tests = [(0, .8), (1, .95), (2, .95), (3, .95), (4, .95), (5, .95), (6, .95), (7, .95), (8, .9)]
        ims = []
        for si, p in tests:
            fn, bg = SC[si]; d = D[si]; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((270, 480)))
        s = Image.new("RGB", (270 * 5, 480 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 270, (i // 5) * 480))
        s.save("sheet.png")
    else: run(SC, "/tmp/np_", "NIPT_Test_Hindi.mp4")
