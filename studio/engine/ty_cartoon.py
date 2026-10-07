import math, sys
from cbc_cartoon import run
from chromo_cartoon import PINK, SKYB
from gene_cartoon import person
from dmarker_cartoon import MOM, LAV
from wes_cartoon import KID, DAD
from lft_cartoon2 import *
from hts_close import close_scene

DATE = "WEDNESDAY HEALTH TIPS  •  7 OCT 2026"
BUTTER = (236, 64, 122)

def butterfly(d, cx, cy, s, col=BUTTER, flap=0.0):
    k = 1 - 0.12 * flap
    for sg in (-1, 1):
        x0 = cx + sg * 0.05 * s
        a, b = sorted((x0, x0 + sg * 0.55 * s * k)); d.ellipse((a, cy - 0.45 * s, b, cy + 0.25 * s), fill=col)
        a, b = sorted((x0, x0 + sg * 0.42 * s * k)); d.ellipse((a, cy + 0.05 * s, b, cy + 0.5 * s), fill=blend(col, (255, 255, 255), 0.25))
    d.rounded_rectangle((cx - 0.07 * s, cy - 0.35 * s, cx + 0.07 * s, cy + 0.45 * s), int(0.07 * s), fill=blend(col, (0, 0, 0), 0.35))

def neck(d, cx, cy, t):
    d.ellipse((cx - 150, cy - 420, cx + 150, cy - 120), fill=SKIN)                     # head
    d.ellipse((cx - 70, cy - 300, cx - 40, cy - 270), fill=(30, 30, 40)); d.ellipse((cx + 40, cy - 300, cx + 70, cy - 270), fill=(30, 30, 40))
    d.arc((cx - 50, cy - 240, cx + 50, cy - 180), 20, 160, fill=(170, 60, 60), width=8)
    d.pieslice((cx - 160, cy - 440, cx + 160, cy - 200), 180, 360, fill=(50, 30, 30))
    d.rectangle((cx - 70, cy - 150, cx + 70, cy + 40), fill=SKIN)                       # neck
    d.rounded_rectangle((cx - 260, cy + 10, cx + 260, cy + 300), 90, fill=(0, 150, 170))  # shoulders
    butterfly(d, cx, cy - 40, 120, flap=(math.sin(t * 5) + 1) / 2)

def speedo(d, cx, cy, r, v, lab, col):
    d.arc((cx - r, cy - r, cx + r, cy + r), 180, 360, fill=(220, 226, 236), width=26)
    d.arc((cx - r, cy - r, cx + r, cy + r), 180, 180 + 180 * v, fill=col, width=26)
    a = math.pi * (1 + v)
    d.line((cx, cy, cx + (r - 40) * math.cos(a), cy + (r - 40) * math.sin(a)), fill=GREY, width=10)
    d.ellipse((cx - 16, cy - 16, cx + 16, cy + 16), fill=GREY)
    d.text((cx, cy + 50), lab, font=font("Bold", 40), fill=col, anchor="mm")

# ---------------- scenes ----------------
def y_hook(fr, t, D):
    rays(fr, 540, 900, t, (255, 120, 170), a=40)
    show(fr, pill(DATE, ORANGE, size=36), 230, t, 0.1)
    put(fr, MOM, 540, 1430 + 6 * math.sin(t * 2), 0.75)
    pop(fr, white_text("Always tired? Weight going up? Hair falling?", 74), 540, 520, t, 0.3, "boom")
    pop(fr, white_text("It could be your THYROID!", 70, color=YEL), 540, 790, t, D * 0.4, "whoosh")
    pop(fr, box_text("Thyroid test: watch till the end", GREEN, 44), 540, 980, t, D * 0.65, "pop")

def y_what(fr, t, D):
    show(fr, pill("WHAT IS THE THYROID?", PINK, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr); neck(d, 540, 820, t)
    fire("pop", 0.3)
    show(fr, text_el("A butterfly-shaped gland in your neck", 46, color=DBLUE), 1180, t, D * 0.15)
    show(fr, text_el("It controls your body's SPEED", 54, color=PINK), 1290, t, D * 0.35)
    d = ImageDraw.Draw(fr)
    for i, (txt, c) in enumerate([("Energy", ORANGE), ("Weight", BLUE), ("Heartbeat", RED), ("Mood", PURPLE)]):
        fire("pop", D * (0.5 + 0.1 * i))
        if t < D * (0.5 + 0.1 * i): continue
        x = 165 + i * 250
        d.rounded_rectangle((x - 110, 1380, x + 110, 1450), 35, fill=c)
        d.text((x, 1415), txt, font=font("Bold", 34), fill=WHITE, anchor="mm")

def y_types(fr, t, D):
    show(fr, pill("TOO SLOW or TOO FAST", PURPLE, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    cols = [(60, BLUE, "HYPO", "(slow thyroid)", 0.15, ["Tiredness", "Weight gain", "Feeling cold", "Hair fall", "Constipation"], 0.4),
            (560, RED, "HYPER", "(fast thyroid)", 0.85, ["Weight loss", "Fast heartbeat", "Sweating", "Shaky hands", "Anxiety"], D * 0.5)]
    for (x0, col, title, sub, v, lines, tin) in cols:
        if t < tin: continue
        d.rounded_rectangle((x0, 350, x0 + 460, 1180), 34, fill=WHITE, outline=col, width=8)
        speedo(d, x0 + 230, 560, 140, v, title, col)
        d.text((x0 + 230, 670), sub, font=font("Medium", 30), fill=GREY, anchor="mm")
        for j, l in enumerate(lines):
            d.text((x0 + 230, 760 + j * 78), l, font=font("Bold", 38), fill=DBLUE, anchor="mm")
    fire("pop", 0.4); fire("boom", D * 0.5)

def y_india(fr, t, D):
    show(fr, pill("WHY INDIA MUST KNOW", ORANGE, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    for k in range(10):
        if t < 0.3 + k * 0.12: break
        x = 140 + (k % 5) * 200; y = 470 + (k // 5) * 260
        person(d, x, y, RED if k == 9 else (190, 200, 215), 1.3)
    fire("pop", 0.3)
    pop(fr, stroke_text("1 in 10", 140, RED, WHITE, 10), 540, 1000, t, D * 0.3, "boom")
    show(fr, text_el("adults in India have hypothyroidism", 46, color=DBLUE), 1130, t, D * 0.4)
    show(fr, card("More common in women", PINK, "♀", size=40), 1260, t, D * 0.55)
    show(fr, card("Many people don't know they have it", PURPLE, "?", size=40), 1395, t, D * 0.7)
    fire("pop", D * 0.55); fire("pop", D * 0.7)

def y_test(fr, t, D):
    show(fr, pill("THE TEST: ONE BLOOD SAMPLE", BLUE, size=44), 230, t, 0.1)
    ground(fr, 270, 760, 300); put(fr, DOC["aim"], 270, 520, 0.7); fire("zap", 0.3)
    d = ImageDraw.Draw(fr); butterfly(d, 820, 520, 220, flap=(math.sin(t * 5) + 1) / 2)
    items = [("TSH: the signal from the brain", PURPLE, "1"), ("T3 & T4: the thyroid hormones", PINK, "2")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.15 + 0.15 * i)); show(fr, card(txt, c, m, size=40), 830 + i * 135, t, D * (0.15 + 0.15 * i))
    show(fr, card("TSH HIGH = usually a SLOW thyroid", BLUE, "↑", size=40), 1130, t, D * 0.55)
    show(fr, card("TSH LOW = usually a FAST thyroid", RED, "↓", size=40), 1265, t, D * 0.7)
    fire("ding", D * 0.55); fire("ding", D * 0.7)
    show(fr, text_el("Screenshot this!", 44, "Bold", TEAL), 1420, t, D * 0.85)

def y_who(fr, t, D):
    show(fr, pill("WHO SHOULD TEST?", GREEN, size=48), 230, t, 0.1)
    ground(fr, 230, 640, 260); put(fr, MOM, 230, 470, 0.5)
    ground(fr, 540, 640, 220); put(fr, DAD, 540, 470, 0.7)
    ground(fr, 850, 640, 260); put(fr, DOC["idle"], 850, 440, 0.55)
    items = [("Women over 35", PINK, "1"), ("Planning pregnancy / pregnant", LAV, "2"), ("After delivery", ORANGE, "3"),
             ("Thyroid in the family", BLUE, "4"), ("Diabetes, PCOD, irregular periods", RED, "5"), ("Newborn: ask doctor about screening", GREEN, "6")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.08 + 0.13 * i)); show(fr, card(txt, c, m, size=37), 710 + i * 125, t, D * (0.08 + 0.13 * i))

def y_prep(fr, t, D):
    show(fr, pill("HOW TO PREPARE", TEAL, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    if t > 0.3:   # sun = morning
        d.ellipse((440, 360, 640, 560), fill=(255, 193, 7))
        for k in range(12):
            a = k * math.pi / 6 + t * 0.5
            d.line((540 + 120 * math.cos(a), 460 + 120 * math.sin(a), 540 + 160 * math.cos(a), 460 + 160 * math.sin(a)), fill=(255, 193, 7), width=12)
    fire("pop", 0.3)
    items = [("Usually no fasting needed", GREEN, "1"), ("Morning sample is best", ORANGE, "2"),
             ("On thyroid tablet? Give sample before the dose (as your doctor says)", PURPLE, "3"), ("Taking biotin? Tell your doctor", RED, "4")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.1 + 0.18 * i)); show(fr, card(txt, c, m, size=36), 700 + i * 150, t, D * (0.1 + 0.18 * i))

def y_myth(fr, t, D):
    show(fr, pill("MYTH BUSTER", RED, size=50), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    if t > 0.4:
        d.rounded_rectangle((360, 380, 720, 560), 40, fill=WHITE, outline=(200, 210, 225), width=6)
        for k in range(4): d.ellipse((400 + k * 80, 440, 460 + k * 80, 500), fill=(255, 255, 255), outline=(150, 160, 180), width=5)
        d.line((360, 380, 720, 560), fill=RED, width=14); d.line((720, 380, 360, 560), fill=RED, width=14)
    fire("boom", 0.4)
    show(fr, text_el("MYTH: Feeling better? Stop the tablet!", 48, color=RED), 680, t, D * 0.2)
    show(fr, text_el("FACT: Never stop or change the dose yourself", 44, color=GREEN), 820, t, D * 0.45)
    pop(fr, box_text("When to recheck TSH? Your doctor decides.", BLUE, 42), 540, 1060, t, D * 0.7, "ding")

def y_close(fr, t, D):
    show(fr, big_logo(), 210, t, 0.2)
    fire("ding", 0.8); show(fr, box_text("Take any medicine only as advised by your doctor", GREEN, 42), 820, t, 0.8)
    show(fr, text_el("Have you ever done a thyroid test?", 54, color=DBLUE), 1010, t, D * 0.4)
    show(fr, text_el("Share with your family!", 44, "Medium", GREY), 1170, t, D * 0.5)
    show(fr, pill("Follow Health Test Simplified", BLUE, size=40), 1300, t, D * 0.6)
    show(fr, pill(DATE, ORANGE, size=32), 1430, t, D * 0.65)
    show(fr, text_el("For awareness only. Consult your doctor.", 30, "Regular", GREY), 1680, t, D * 0.7)

SC = [(y_hook, "navy"), (y_what, "light"), (y_types, "light"), (y_india, "light"), (y_test, "light"),
      (y_who, "light"), (y_prep, "light"), (y_myth, "light"), (close_scene("Have you ever done a thyroid test?", DATE), "light")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        D = [12, 13, 18, 11, 17, 18, 17, 12, 14]; tests = [(0, .9), (1, .95), (2, .95), (3, .95), (4, .95), (5, .95), (6, .95), (7, .95), (8, .9)]
        ims = []
        for si, p in tests:
            fn, bg = SC[si]; d = D[si]; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((360, 640)))
        s = Image.new("RGB", (360 * 5, 640 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 360, (i // 5) * 640))
        s.save("sheet.png")
    else: run(SC, "/tmp/ty_", "Wednesday_Health_Tips_7Oct2026_Thyroid_Hindi.mp4")
