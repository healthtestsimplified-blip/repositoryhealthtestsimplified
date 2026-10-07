import math, sys
from cbc_cartoon import run
from chromo_cartoon import x_shape, CHROMO, PINK, SKYB
from lft_cartoon2 import *

BASE_COL = {"A": (229, 57, 53), "T": (30, 136, 229), "G": (67, 160, 71), "C": (251, 140, 0)}
SEQ = "ATGCGTACCGATTGCAATGCCGTA"
PAIR = {"A": "T", "T": "A", "G": "C", "C": "G"}

def helix(fr, cx, cy, width, amp, t, letters=False, alpha=255):
    lay = Image.new("RGBA", fr.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    k = 2 * math.pi / 360; x0 = cx - width / 2; ph = t * 2.2
    n = int(width // 30)
    for i in range(n + 1):
        x = x0 + i * 30; a = k * (x - x0) + ph
        y1, y2 = cy + amp * math.sin(a), cy - amp * math.sin(a)
        b = SEQ[i % len(SEQ)]
        if i % 1 == 0:
            ym = (y1 + y2) / 2
            d.line((x, y1, x, ym), fill=(*BASE_COL[b], alpha), width=10)
            d.line((x, ym, x, y2), fill=(*BASE_COL[PAIR[b]], alpha), width=10)
            if letters and abs(y1 - y2) > amp * 1.4:
                d.text((x, y1 + (22 if y1 > y2 else -22)), b, font=font("Bold", 26), fill=(*BASE_COL[b], alpha), anchor="mm")
    for sgn, col in ((1, (90, 60, 180)), (-1, (0, 150, 170))):
        pts = [(x0 + j * 6, cy + sgn * amp * math.sin(k * j * 6 + ph)) for j in range(int(width / 6) + 1)]
        d.line(pts, fill=(*col, alpha), width=16, joint="curve")
    fr.alpha_composite(lay)

def letters_panel(p):
    im = Image.new("RGBA", (W, 560), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, b in enumerate("ATGC"):
        if p < i / 4: break
        x = 150 + i * 260
        d.rounded_rectangle((x - 100, 0, x + 100, 200), 34, fill=BASE_COL[b])
        d.text((x, 100), b, font=font("Bold", 130), fill=WHITE, anchor="mm")
    if p > 0.75:
        for j, (a, b) in enumerate((("A", "T"), ("G", "C"))):
            x = 280 + j * 520
            d.rounded_rectangle((x - 200, 280, x + 200, 420), 40, fill=WHITE, outline=(215, 225, 238), width=4)
            d.text((x - 100, 350), a, font=font("Bold", 90), fill=BASE_COL[a], anchor="mm")
            d.text((x, 350), "+", font=font("Bold", 70), fill=GREY, anchor="mm")
            d.text((x + 100, 350), b, font=font("Bold", 90), fill=BASE_COL[b], anchor="mm")
        d.text((W / 2, 490), "Always pair like this!", font=font("Bold", 44), fill=DBLUE, anchor="mm")
    return im

def coil(fr, cx, cy, t):
    d = ImageDraw.Draw(fr)
    for k in range(7):
        r = 70 - k * 6; y = cy - 120 + k * 40
        d.ellipse((cx - r, y - 22, cx + r, y + 22), outline=(90, 60, 180), width=10)

# ---------------- scenes ----------------
def d_hook(fr, t, D):
    rays(fr, 540, 900, t, (120, 160, 255), a=40)
    helix(fr, 540, 1450, 1000, 90, t, alpha=110)
    pop(fr, white_text("You share 99.9% of your DNA with every human!", 74), 540, 620, t, 0.1, "boom")
    pop(fr, white_text("So why do we all look different?", 60, color=YEL), 540, 900, t, 2.0, "whoosh")
    pop(fr, box_text("Watch till the end to find out!", GREEN, 44), 540, 1110, t, D * 0.6, "pop")

def d_what(fr, t, D):
    show(fr, pill("WHAT IS DNA?", PURPLE, size=50), 230, t, 0.1)
    helix(fr, 540, 620, 980, 150, t, letters=True); fire("whoosh", 0.3)
    show(fr, text_el("Your body's secret code", 66, color=DBLUE), 900, t, D * 0.2)
    pop(fr, box_text("Shape: a twisted ladder called a DOUBLE HELIX", TEAL, 42), 540, 1130, t, D * 0.5, "ding")

def d_letters(fr, t, D):
    show(fr, pill("THE CODE HAS ONLY 4 LETTERS", BLUE, size=44), 230, t, 0.1)
    p = (t - 0.3) / (D * 0.55)
    for i in range(4): fire("pop", 0.3 + i * D * 0.55 / 4)
    fr.alpha_composite(letters_panel(p), (0, 400))
    pop(fr, box_text("Your DNA has about 3 billion letters!", PINK, 44), 540, 1120, t, D * 0.75, "ding")

def d_pack(fr, t, D):
    show(fr, pill("DNA PACKS INTO CHROMOSOMES", PURPLE, size=44), 230, t, 0.1)
    helix(fr, 230, 640, 300, 60, t)
    d = ImageDraw.Draw(fr)
    if t > D * 0.2:
        d.text((410, 640), "›", font=font("Bold", 90), fill=ORANGE, anchor="mm"); coil(fr, 560, 650, t)
    fire("whoosh", D * 0.2); fire("ding", D * 0.4)
    if t > D * 0.4:
        d.text((710, 640), "›", font=font("Bold", 90), fill=ORANGE, anchor="mm")
        put(fr, CHROMO, 880, 640, 0.5 * min(1, (t - D * 0.4) / 0.3))
    show(fr, text_el("Wrapped tightly like thread on a spool", 48, color=DBLUE), 900, t, D * 0.45)
    pop(fr, box_text("About 2 metres of DNA fits inside every tiny cell!", TEAL, 42), 540, 1110, t, D * 0.65, "pop")

def d_genes(fr, t, D):
    show(fr, pill("GENES = RECIPES", GREEN, size=48), 230, t, 0.1)
    helix(fr, 540, 520, 980, 110, t)
    lay = ImageDraw.Draw(fr)
    if t > D * 0.15:
        lay.rounded_rectangle((330, 380, 690, 660), 30, outline=YEL, width=10)
        lay.text((510, 360), "1 GENE", font=font("Bold", 40), fill=ORANGE, anchor="mm")
    fire("pop", D * 0.15)
    for i, (txt, c) in enumerate([("Eye colour", BLUE), ("Blood group", RED), ("Hair type", ORANGE)]):
        fire("pop", D * (0.25 + 0.1 * i)); show(fr, pill(txt, c, size=40), 760 + i * 100, t, D * (0.25 + 0.1 * i))
    show(fr, text_el("Humans have about 20,000 genes", 52, color=DBLUE), 1100, t, D * 0.55)
    pop(fr, box_text("The tiny 0.1% difference makes YOU unique!", PURPLE, 44), 540, 1260, t, D * 0.72, "ding")

def d_family(fr, t, D):
    show(fr, pill("HALF FROM MOM, HALF FROM DAD", ORANGE, size=44), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    for (x, col, lab) in ((230, PINK, "MOTHER"), (850, SKYB, "FATHER")):
        d.ellipse((x - 120, 380, x + 120, 620), fill=blend(col, (255, 255, 255), 0.8), outline=col, width=8)
        d.ellipse((x - 40, 420, x + 40, 500), fill=SKIN); d.rounded_rectangle((x - 60, 505, x + 60, 590), 30, fill=col)
        d.text((x, 660), lab, font=font("Bold", 40), fill=col, anchor="mm")
    if t > D * 0.25:
        p = min(1, (t - D * 0.25) / (D * 0.3))
        for (x0, col) in ((230, PINK), (850, SKYB)):
            x = x0 + (540 - x0) * ease(p)
            d.ellipse((x - 26, 540 + 200 * ease(p) - 26, x + 26, 540 + 200 * ease(p) + 26), fill=col)
    fire("whoosh", D * 0.25)
    if t > D * 0.55:
        d.ellipse((420, 700, 660, 940), fill=(255, 245, 225), outline=GREEN, width=8)
        d.ellipse((500, 745, 580, 825), fill=SKIN); d.rounded_rectangle((480, 830, 600, 910), 30, fill=GREEN)
        d.text((540, 985), "YOU", font=font("Bold", 46), fill=GREEN, anchor="mm")
    fire("ding", D * 0.55)
    show(fr, text_el("That's why some diseases run in families", 46, color=DBLUE), 1080, t, D * 0.7)

def d_tests(fr, t, D):
    show(fr, pill("WHAT CAN DNA TESTS DO?", BLUE, size=46), 230, t, 0.1)
    ground(fr, 270, 800, 300); put(fr, DOC["aim"], 270, 560, 0.75); beam(fr, 270 + 175 * 0.75, 525, 700, 560, t)
    helix(fr, 840, 560, 300, 70, t); fire("zap", 0.3)
    items = [("Genetic diseases like thalassaemia", RED, "1"), ("Some cancer risk genes", PURPLE, "2"),
             ("Family relation (paternity) tests", BLUE, "3"), ("Crime investigation", GREY, "4")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.12 + 0.17 * i)); show(fr, card(txt, c, m, size=40), 860 + i * 135, t, D * (0.12 + 0.17 * i))

def d_thal(fr, t, D):
    show(fr, pill("IMPORTANT FOR EASTERN INDIA", RED, size=44), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    if t > 0.4:
        for (x, col) in ((380, PINK), (700, SKYB)):
            d.ellipse((x - 90, 420, x + 90, 600), fill=blend(col, (255, 255, 255), 0.8), outline=col, width=8)
            d.ellipse((x - 30, 450, x + 30, 510), fill=SKIN); d.rounded_rectangle((x - 45, 512, x + 45, 580), 24, fill=col)
        d.ellipse((508, 478, 542, 512), fill=RED); d.ellipse((538, 478, 572, 512), fill=RED); d.polygon([(510, 500), (570, 500), (540, 540)], fill=RED)
    fire("pop", 0.4)
    pop(fr, stroke_text("THALASSAEMIA", 92, RED, WHITE, 8), 540, 700, t, D * 0.15, "boom")
    show(fr, text_el("is common in Bengal & Eastern India", 50, color=DBLUE), 790, t, D * 0.25)
    show(fr, card("Carrier check before marriage or pregnancy", GREEN, "✓", size=42), 930, t, D * 0.45)
    show(fr, card("Simple blood test, as doctor advises", BLUE, "+", size=42), 1110, t, D * 0.6)
    fire("pop", D * 0.45); fire("pop", D * 0.6)

def d_close(fr, t, D):
    show(fr, big_logo(), 210, t, 0.2)
    fire("ding", 0.8); show(fr, box_text("Take any medicine only as advised by your doctor", GREEN, 42), 820, t, 0.8)
    show(fr, text_el("Which DNA fact surprised you the most?", 52, color=DBLUE), 1020, t, D * 0.45)
    show(fr, text_el("Tell us in the comments!", 44, "Medium", GREY), 1180, t, D * 0.55)
    show(fr, pill("Follow Health Test Simplified", BLUE, size=40), 1340, t, D * 0.65)
    show(fr, text_el("For awareness only. Consult your doctor.", 30, "Regular", GREY), 1680, t, D * 0.7)

SC = [(d_hook, "navy"), (d_what, "light"), (d_letters, "light"), (d_pack, "light"), (d_genes, "light"),
      (d_family, "light"), (d_tests, "light"), (d_thal, "light"), (d_close, "light")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        D = [10, 9, 14, 12, 16, 12, 14, 10, 12]; tests = [(0, .8), (1, .9), (2, .9), (3, .9), (4, .9), (5, .9), (6, .9), (7, .9), (8, .9), (2, .4)]
        ims = []
        for si, p in tests:
            fn, bg = SC[si]; d = D[si]; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((270, 480)))
        s = Image.new("RGB", (270 * 5, 480 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 270, (i // 5) * 480))
        s.save("sheet.png")
    else: run(SC, "/tmp/dn_", "What_is_DNA_Hindi.mp4")
