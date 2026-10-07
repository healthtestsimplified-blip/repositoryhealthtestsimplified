import math, sys
from cbc_cartoon import run
from chromo_cartoon import PINK, SKYB
from dna_cartoon import helix, BASE_COL
from lft_cartoon2 import *

def person(d, x, y, col, s=1.0):
    d.ellipse((x - 34 * s, y - 80 * s, x + 34 * s, y - 12 * s), fill=SKIN)
    d.rounded_rectangle((x - 55 * s, y - 8 * s, x + 55 * s, y + 90 * s), int(30 * s), fill=col)

def cookbook(p):
    im = Image.new("RGBA", (W, 460), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    data = [("DNA", "Cookbook", PURPLE), ("GENE", "One recipe", ORANGE), ("PROTEIN", "The dish", GREEN)]
    for i, (a, b, c) in enumerate(data):
        if p < i / 3: break
        x = 180 + i * 360
        d.rounded_rectangle((x - 140, 0, x + 140, 300), 30, fill=WHITE, outline=c, width=8)
        if i == 0:
            d.rounded_rectangle((x - 75, 50, x + 75, 210), 12, fill=c); d.rectangle((x - 75, 50, x - 55, 210), fill=blend(c, (0, 0, 0), 0.3))
            for k in range(3): d.line((x - 40, 90 + k * 35, x + 55, 90 + k * 35), fill=WHITE, width=6)
        elif i == 1:
            d.rounded_rectangle((x - 70, 40, x + 70, 220), 12, fill=(255, 248, 230), outline=c, width=5)
            for k in range(4): d.line((x - 45, 80 + k * 35, x + 45, 80 + k * 35), fill=c, width=6)
        else:
            d.ellipse((x - 95, 120, x + 95, 230), fill=(235, 235, 240)); d.ellipse((x - 70, 105, x + 70, 195), fill=(255, 170, 60))
            for k in range(3): d.arc((x - 40 + k * 30, 40, x - 10 + k * 30, 100), 200, 340, fill=GREY, width=5)
        d.text((x, 255), a, font=font("Bold", 40), fill=c, anchor="mm")
        d.text((x, 350), b, font=font("Bold", 36), fill=DBLUE, anchor="mm")
        if i < 2 and p > (i + 1) / 3: d.text((x + 180, 150), "›", font=font("Bold", 80), fill=GREY, anchor="mm")
    return im

def mutation(p):
    im = Image.new("RGBA", (W, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    good, bad = "ATGCGTACC", "ATGCATACC"
    for r, (seq, lab, col) in enumerate(((good, "Correct gene", GREEN), (bad, "Spelling mistake!", RED))):
        if r == 1 and p < 0.5: break
        y = 60 + r * 200
        for i, ch in enumerate(seq):
            x = 140 + i * 100
            wrong = r == 1 and ch != good[i]
            d.rounded_rectangle((x - 40, y - 50, x + 40, y + 50), 14, fill=RED if wrong else BASE_COL[ch])
            d.text((x, y), ch, font=font("Bold", 56), fill=WHITE, anchor="mm")
        d.text((W / 2, y + 85), lab, font=font("Bold", 40), fill=col, anchor="mm")
    return im

def punnett(p):
    im = Image.new("RGBA", (W, 760), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    person(d, 230, 120, PINK); person(d, 850, 120, SKYB)
    d.text((230, 250), "Mother: carrier", font=font("Bold", 34), fill=PINK, anchor="mm")
    d.text((850, 250), "Father: carrier", font=font("Bold", 34), fill=SKYB, anchor="mm")
    d.text((540, 130), "+", font=font("Bold", 90), fill=GREY, anchor="mm")
    kids = [("Healthy", GREEN, 0), ("Carrier", ORANGE, 1), ("Carrier", ORANGE, 2), ("Thalassaemia major", RED, 3)]
    for lab, c, i in kids:
        if p < (i + 1) / 5: break
        x = 160 + i * 253; y = 470
        d.rounded_rectangle((x - 115, y - 150, x + 115, y + 150), 26, fill=blend(c, (255, 255, 255), 0.85), outline=c, width=6)
        person(d, x, y - 20, c, 0.8)
        words = lab.split(" ")
        for j, wd in enumerate(words): d.text((x, y + 85 + j * 36), wd, font=font("Bold", 30), fill=c, anchor="mm")
    if p > 0.9:
        d.text((W / 2, 690), "Each pregnancy: 1 in 4 chance of thalassaemia major", font=font("Bold", 34), fill=RED, anchor="mm")
    return im

# ---------------- scenes ----------------
def g_hook(fr, t, D):
    rays(fr, 540, 900, t, (120, 160, 255), a=40)
    helix(fr, 540, 1450, 1000, 90, t, alpha=110)
    pop(fr, white_text("Got your father's nose? Your mother's smile?", 72), 540, 620, t, 0.1, "boom")
    pop(fr, white_text("Thank your GENES!", 80, color=YEL), 540, 880, t, 2.0, "whoosh")
    pop(fr, box_text("Watch till the end: a test every couple must know!", GREEN, 40), 540, 1090, t, D * 0.6, "pop")

def g_what(fr, t, D):
    show(fr, pill("WHAT IS A GENE?", ORANGE, size=50), 230, t, 0.1)
    helix(fr, 540, 470, 980, 110, t)
    d = ImageDraw.Draw(fr)
    if t > 0.5:
        d.rounded_rectangle((340, 330, 700, 610), 30, outline=YEL, width=10); d.text((520, 312), "1 GENE", font=font("Bold", 40), fill=ORANGE, anchor="mm")
    fire("pop", 0.5)
    show(fr, text_el("A small part of your DNA", 58, color=DBLUE), 660, t, D * 0.15)
    fr.alpha_composite(cookbook((t - D * 0.3) / (D * 0.5)), (0, 800))
    for i in range(3): fire("pop", D * (0.3 + i * 0.5 / 3))

def g_decide(fr, t, D):
    show(fr, pill("WHAT DO GENES DECIDE?", BLUE, size=46), 230, t, 0.1)
    helix(fr, 540, 460, 900, 90, t)
    for i, (txt, c) in enumerate([("Eye & hair colour", BLUE), ("Height", TEAL), ("Blood group", RED), ("Some disease risks", ORANGE)]):
        fire("pop", D * (0.12 + 0.1 * i)); show(fr, pill(txt, c, size=42), 640 + i * 110, t, D * (0.12 + 0.1 * i))
    pop(fr, box_text("Every gene comes in 2 copies: one from mom, one from dad", PURPLE, 40), 540, 1180, t, D * 0.6, "ding")

def g_mut(fr, t, D):
    show(fr, pill("WHEN A GENE HAS A MISTAKE", RED, size=44), 230, t, 0.1)
    p = (t - 0.4) / (D * 0.5); fire("pop", 0.4); fire("boom", 0.4 + D * 0.25)
    fr.alpha_composite(mutation(p), (0, 380))
    if 0.4 + D * 0.25 < t < 0.4 + D * 0.25 + 0.35: NOW["shake"] = 10
    show(fr, text_el("A tiny spelling mistake = a faulty recipe", 48, color=DBLUE), 860, t, D * 0.5)
    show(fr, card("Can cause thalassaemia, sickle cell & more", RED, "!", size=42), 980, t, D * 0.65)
    fire("pop", D * 0.65)

def g_carrier(fr, t, D):
    show(fr, pill("2 HEALTHY CARRIERS = A HIDDEN RISK", RED, size=40), 230, t, 0.1)
    p = (t - 0.4) / (D * 0.65)
    for i in range(4): fire("pop", 0.4 + (i + 1) / 5 * D * 0.65)
    fr.alpha_composite(punnett(p), (0, 340))
    show(fr, box_text("Carriers look healthy, yet pass it on!", ORANGE, 42), 1120, t, D * 0.8)

def g_life(fr, t, D):
    show(fr, pill("GENES vs LIFESTYLE", GREEN, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    ang = -0.12 + 0.24 * ease((t - D * 0.4) / (D * 0.3))
    cx, cy = 540, 560
    d.polygon([(cx, cy), (cx - 50, cy + 200), (cx + 50, cy + 200)], fill=GREY)
    lx, ly = cx - 330 * math.cos(ang), cy - 330 * math.sin(ang); rx, ry = cx + 330 * math.cos(ang), cy + 330 * math.sin(ang)
    d.line((lx, ly, rx, ry), fill=DBLUE, width=14)
    d.rounded_rectangle((lx - 120, ly - 110, lx + 120, ly - 10), 24, fill=PURPLE); d.text((lx, ly - 60), "GENES", font=font("Bold", 40), fill=WHITE, anchor="mm")
    d.rounded_rectangle((rx - 140, ry - 110, rx + 140, ry - 10), 24, fill=GREEN); d.text((rx, ry - 60), "LIFESTYLE", font=font("Bold", 40), fill=WHITE, anchor="mm")
    fire("ding", D * 0.4)
    show(fr, text_el("Diabetes or heart disease in family? Your risk is higher...", 44, color=DBLUE), 800, t, D * 0.1)
    show(fr, text_el("...but lifestyle can change it!", 52, color=GREEN), 940, t, D * 0.45)
    for i, (txt, c, m) in enumerate([("Walk daily", TEAL, "✓"), ("Eat healthy", ORANGE, "✓"), ("Regular check-ups", BLUE, "✓")]):
        fire("pop", D * (0.55 + 0.1 * i)); show(fr, card(txt, c, m, size=42), 1060 + i * 125, t, D * (0.55 + 0.1 * i))

def g_tests(fr, t, D):
    show(fr, pill("GENE-RELATED TESTS", BLUE, size=46), 230, t, 0.1)
    ground(fr, 270, 800, 300); put(fr, DOC["aim"], 270, 560, 0.75); beam(fr, 270 + 175 * 0.75, 525, 700, 560, t)
    helix(fr, 840, 560, 300, 70, t); fire("zap", 0.3)
    items = [("Thalassaemia carrier test (HPLC)", RED, "1"), ("Before marriage or pregnancy", PINK, "2"),
             ("Other genetic tests, as doctor advises", PURPLE, "3"), ("Newborn screening", TEAL, "4")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.12 + 0.17 * i)); show(fr, card(txt, c, m, size=40), 860 + i * 135, t, D * (0.12 + 0.17 * i))

def g_close(fr, t, D):
    show(fr, big_logo(), 210, t, 0.2)
    fire("ding", 0.8); show(fr, box_text("Take any medicine only as advised by your doctor", GREEN, 42), 820, t, 0.8)
    show(fr, text_el("Which feature did you get from your parents?", 52, color=DBLUE), 1020, t, D * 0.45)
    show(fr, text_el("Tell us in the comments!", 44, "Medium", GREY), 1180, t, D * 0.55)
    show(fr, pill("Follow Health Test Simplified", BLUE, size=40), 1340, t, D * 0.65)
    show(fr, text_el("For awareness only. Consult your doctor.", 30, "Regular", GREY), 1680, t, D * 0.7)

SC = [(g_hook, "navy"), (g_what, "light"), (g_decide, "light"), (g_mut, "light"), (g_carrier, "light"),
      (g_life, "light"), (g_tests, "light"), (g_close, "light")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        D = [10, 16, 13, 12, 18, 16, 14, 12]; tests = [(0, .8), (1, .95), (2, .9), (3, .9), (4, .95), (5, .95), (6, .9), (7, .9)]
        ims = []
        for si, p in tests:
            fn, bg = SC[si]; d = D[si]; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((270, 480)))
        s = Image.new("RGB", (270 * 4, 480 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 4) * 270, (i // 4) * 480))
        s.save("sheet.png")
    else: run(SC, "/tmp/gn_", "What_is_Gene_Hindi.mp4")
