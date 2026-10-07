import math, sys
from cbc_cartoon import run
from lft_cartoon2 import *

PINK = (216, 27, 96); SKYB = (30, 136, 229)

def x_shape(d, cx, cy, s, col, band=True, lab=None):
    for sgn in (-1, 1):
        x0, y0, x1, y1 = cx - sgn * 0.42 * s, cy - 0.5 * s, cx + sgn * 0.42 * s, cy + 0.5 * s
        d.line((x0, y0, x1, y1), fill=col, width=max(4, int(0.26 * s)))
        r = 0.13 * s
        for (x, y) in ((x0, y0), (x1, y1)): d.ellipse((x - r, y - r, x + r, y + r), fill=col)
        if band:
            for f in (0.22, 0.78):
                bx, by = x0 + (x1 - x0) * f, y0 + (y1 - y0) * f
                d.ellipse((bx - 0.09 * s, by - 0.05 * s, bx + 0.09 * s, by + 0.05 * s), fill=blend(col, (255, 255, 255), 0.45))
    d.ellipse((cx - 0.1 * s, cy - 0.1 * s, cx + 0.1 * s, cy + 0.1 * s), fill=blend(col, (0, 0, 0), 0.25))
    if lab: d.text((cx, cy + 0.72 * s), lab, font=font("Bold", max(14, int(0.28 * s))), fill=GREY, anchor="mm")

def chromo_sprite(mood="happy"):
    w = h = 460
    im = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    x_shape(d, 230 * SS, 230 * SS, 380 * SS, (120, 70, 200))
    d.ellipse((150 * SS, 160 * SS, 310 * SS, 320 * SS), fill=(140, 90, 215))
    for ex in (195, 265):
        d.ellipse(((ex - 22) * SS, 200 * SS, (ex + 22) * SS, 248 * SS), fill=WHITE)
        d.ellipse(((ex - 10) * SS, 214 * SS, (ex + 12) * SS, 238 * SS), fill=(30, 30, 40))
    d.arc((195 * SS, 240 * SS, 265 * SS, 295 * SS), 20, 160, fill=WHITE, width=7 * SS)
    for ex in (172, 288): d.ellipse(((ex - 14) * SS, 252 * SS, (ex + 14) * SS, 272 * SS), fill=(255, 150, 190))
    return im.resize((w, h), Image.LANCZOS)
CHROMO = chromo_sprite()

def zoom_chain(p):
    im = Image.new("RGBA", (W, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    xs = [140, 400, 660, 920]; cy = 160; labels = ["Body", "Cell", "Nucleus", "Chromosome"]
    for i, x in enumerate(xs):
        if p < i / 4: break
        d.ellipse((x - 110, cy - 110, x + 110, cy + 110), fill=WHITE, outline=[BLUE, TEAL, PURPLE, PINK][i], width=8)
        if i == 0:
            d.ellipse((x - 26, cy - 85, x + 26, cy - 33), fill=SKIN); d.rounded_rectangle((x - 45, cy - 30, x + 45, cy + 80), 30, fill=BLUE)
        elif i == 1:
            d.ellipse((x - 80, cy - 70, x + 80, cy + 70), fill=(255, 220, 230)); d.ellipse((x - 30, cy - 30, x + 30, cy + 30), fill=PURPLE)
        elif i == 2:
            d.ellipse((x - 80, cy - 80, x + 80, cy + 80), fill=(225, 205, 245))
            for k in range(5): x_shape(d, x - 45 + (k % 3) * 45, cy - 30 + (k // 3) * 60, 45, (120, 70, 200), False)
        else:
            x_shape(d, x, cy, 150, (120, 70, 200))
        d.text((x, cy + 160), labels[i], font=font("Bold", 38), fill=DBLUE, anchor="mm")
        if i < 3 and p > (i + 1) / 4: d.text((x + 130, cy), "›", font=font("Bold", 70), fill=ORANGE, anchor="mm")
    return im

def karyotype(p):
    im = Image.new("RGBA", (W, 760), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((50, 0, W - 50, 740), 30, fill=WHITE, outline=(215, 225, 238), width=3)
    n = int(23 * max(0, min(1, p)))
    for i in range(n):
        r, c = divmod(i, 6); x = 140 + c * 160; y = 100 + r * 175
        if i == 22: x = 140 + 5 * 160
        s = 70 - i * 1.2
        x_shape(d, x - 30, y, s, SKYB, False); x_shape(d, x + 30, y, s if i < 22 else s, PINK, False)
        d.text((x, y + 70), str(i + 1) if i < 22 else "XX / XY", font=font("Bold", 26), fill=GREY, anchor="mm")
    return im

def xx_xy(p):
    im = Image.new("RGBA", (W, 640), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((60, 0, 500, 260), 30, fill=WHITE, outline=PINK, width=6)
    d.text((280, 40), "MOTHER", font=font("Bold", 40), fill=PINK, anchor="mm")
    d.text((280, 150), "X  X", font=font("Bold", 90), fill=PINK, anchor="mm")
    d.text((280, 225), "gives only X", font=font("Medium", 30), fill=GREY, anchor="mm")
    d.rounded_rectangle((580, 0, 1020, 260), 30, fill=WHITE, outline=SKYB, width=6)
    d.text((800, 40), "FATHER", font=font("Bold", 40), fill=SKYB, anchor="mm")
    d.text((800, 150), "X  Y", font=font("Bold", 90), fill=SKYB, anchor="mm")
    d.text((800, 225), "gives X or Y", font=font("Medium", 30), fill=GREY, anchor="mm")
    if p > 0.4:
        d.rounded_rectangle((60, 320, 500, 520), 30, fill=(252, 228, 236))
        d.text((280, 380), "X + X", font=font("Bold", 60), fill=PINK, anchor="mm"); d.text((280, 465), "= Girl", font=font("Bold", 50), fill=PINK, anchor="mm")
    if p > 0.7:
        d.rounded_rectangle((580, 320, 1020, 520), 30, fill=(227, 242, 253))
        d.text((800, 380), "X + Y", font=font("Bold", 60), fill=SKYB, anchor="mm"); d.text((800, 465), "= Boy", font=font("Bold", 50), fill=SKYB, anchor="mm")
    return im

MYTH = stroke_text("MYTH BUSTED!", 110, YEL, RED, 10)

# ---------------- scenes ----------------
def k_hook(fr, t, D):
    rays(fr, 540, 900, t, (180, 120, 255), a=45)
    put(fr, darken(CHROMO, 0.6), 540, 1380 + 20 * math.sin(t * 3), 1.1)
    pop(fr, white_text("Why do you look like your parents?", 80), 540, 620, t, 0.1, "boom")
    pop(fr, white_text("The answer: CHROMOSOMES!", 66, color=YEL), 540, 880, t, 1.8, "whoosh")
    pop(fr, box_text("Watch till the end: a myth will break!", GREEN, 42), 540, 1080, t, D * 0.55, "pop")

def k_zoom(fr, t, D):
    show(fr, pill("LET'S ZOOM INSIDE YOU", BLUE, size=46), 230, t, 0.1)
    p = (t - 0.3) / (D * 0.6)
    for i in range(4): fire("pop", 0.3 + i * D * 0.15)
    fr.alpha_composite(zoom_chain(p), (0, 420))
    show(fr, text_el("Trillions of cells. Each has a nucleus.", 48, color=DBLUE), 950, t, D * 0.55)
    pop(fr, box_text("Chromosomes live inside the nucleus!", PURPLE, 44), 540, 1150, t, D * 0.72, "ding")

def k_what(fr, t, D):
    show(fr, pill("MEET CHROMO!", PURPLE, size=48), 230, t, 0.1)
    put(fr, CHROMO, 540, 560 + 14 * math.sin(t * 3), 0.85 + 0.03 * math.sin(t * 5))
    sparkles(fr, 540, 560, 260, t, 6)
    show(fr, text_el("Your body's instruction book", 58, color=DBLUE), 800, t, D * 0.1)
    for i, (txt, c, m) in enumerate([("Made of DNA", PURPLE, "1"), ("DNA has genes = recipes", TEAL, "2"),
                                     ("Decide eye colour, height & more", ORANGE, "3")]):
        fire("pop", D * (0.2 + 0.13 * i)); show(fr, card(txt, c, m, size=40), 900 + i * 125, t, D * (0.2 + 0.13 * i))
    pop(fr, box_text("DID YOU KNOW? DNA from ONE cell is about 2 metres long!", PINK, 40), 540, 1360, t, D * 0.68, "ding")

def k_46(fr, t, D):
    show(fr, pill("46 CHROMOSOMES = 23 PAIRS", BLUE, size=44), 230, t, 0.1)
    fr.alpha_composite(karyotype((t - 0.3) / (D * 0.45)), (0, 330)); fire("pop", 0.3)
    d = ImageDraw.Draw(fr)
    if t > D * 0.55:
        d.rounded_rectangle((120, 1130, 520, 1210), 40, fill=PINK); d.text((320, 1170), "23 from Mother", font=font("Bold", 36), fill=WHITE, anchor="mm")
        d.rounded_rectangle((560, 1130, 960, 1210), 40, fill=SKYB); d.text((760, 1170), "23 from Father", font=font("Bold", 36), fill=WHITE, anchor="mm")
    fire("ding", D * 0.55)
    show(fr, text_el("That's why you look like both!", 52, color=GREEN), 1260, t, D * 0.72)

def k_myth(fr, t, D):
    show(fr, pill("BOY OR GIRL: WHO DECIDES?", ORANGE, size=44), 230, t, 0.1)
    fr.alpha_composite(xx_xy((t - 0.3) / (D * 0.45)), (0, 360))
    fire("pop", D * 0.15); fire("pop", D * 0.32)
    if t > D * 0.5: NOW["shake"] = 12 if t < D * 0.5 + 0.35 else 0
    pop(fr, MYTH, 540, 1000, t, D * 0.5, "boom")
    show(fr, white_text("The mother does NOT decide baby's sex", 46, color=WHITE), 1080, t, D * 0.55)
    show(fr, box_text("Girl or boy, both are blessings!", GREEN, 42), 1200, t, D * 0.7)
    show(fr, text_el("Sex determination before birth is illegal in India", 34, "Bold", YEL), 1340, t, D * 0.8)

def k_change(fr, t, D):
    show(fr, pill("WHEN CHROMOSOMES CHANGE", RED, size=44), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    if t > 0.4:
        for k in range(3):
            x_shape(d, 380 + k * 160, 520, 120, (120, 70, 200) if k < 2 else RED)
        d.text((540, 650), "Chromosome 21: an extra copy", font=font("Bold", 38), fill=RED, anchor="mm")
    fire("boom", 0.4)
    show(fr, text_el("Sometimes a chromosome is extra or missing", 46, color=DBLUE), 730, t, D * 0.15)
    for i, (txt, c) in enumerate([("Extra 21st = Down syndrome", PURPLE), ("Repeated miscarriages", ORANGE),
                                  ("Some cases of infertility", TEAL)]):
        fire("pop", D * (0.3 + 0.12 * i)); show(fr, card(txt, c, "●", size=40), 860 + i * 125, t, D * (0.3 + 0.12 * i))
    show(fr, box_text("With the right support, children with Down syndrome live happy lives", GREEN, 38), 1270, t, D * 0.72)

def k_tests(fr, t, D):
    show(fr, pill("CHROMOSOME TESTS", BLUE, size=46), 230, t, 0.1)
    rays(fr, 270, 640, t, (120, 230, 140), a=40)
    ground(fr, 270, 900, 320); put(fr, DOC["aim"], 270, 640, 0.85); beam(fr, 270 + 175 * 0.85, 600, 760, 640, t)
    put(fr, CHROMO, 820, 640, 0.45 + 0.02 * math.sin(t * 5)); fire("zap", 0.3)
    show(fr, card("Karyotyping: blood test that counts & checks chromosomes", BLUE, "1", size=38), 960, t, D * 0.2)
    show(fr, card("Double marker / NIPT: pregnancy screening", PINK, "2", size=38), 1150, t, D * 0.5)
    fire("pop", D * 0.2); fire("pop", D * 0.5)
    show(fr, text_el("Done only as your doctor advises", 42, "Medium", GREEN), 1340, t, D * 0.72)

def k_who(fr, t, D):
    show(fr, pill("WHO MAY NEED IT?", ORANGE, size=46), 230, t, 0.1)
    ground(fr, 250, 770, 300); put(fr, DOC["idle"], 250, 560, 0.75); put(fr, CHROMO, 780, 570, 0.5)
    items = [("Repeated miscarriages (couple)", ORANGE, "!"), ("Pregnancy, especially 35+", PINK, "♥"),
             ("Child with delayed development", PURPLE, "!"), ("Infertility check-up", TEAL, "+")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.1 + 0.16 * i)); show(fr, card(txt, c, m, size=40), 850 + i * 135, t, D * (0.1 + 0.16 * i))
    show(fr, text_el("Always with a doctor or genetic counsellor", 40, "Medium", GREEN), 1420, t, D * 0.8)

def k_close(fr, t, D):
    show(fr, big_logo(), 210, t, 0.2)
    fire("ding", 0.8); show(fr, box_text("Take any medicine only as advised by your doctor", GREEN, 42), 820, t, 0.8)
    show(fr, text_el("Did you know the father's chromosome decides baby's sex?", 48, color=DBLUE), 1010, t, D * 0.4)
    show(fr, text_el("Tell us in the comments!", 44, "Medium", GREY), 1200, t, D * 0.55)
    show(fr, pill("Follow Health Test Simplified", BLUE, size=40), 1340, t, D * 0.65)
    show(fr, text_el("For awareness only. Consult your doctor.", 30, "Regular", GREY), 1680, t, D * 0.7)

SC = [(k_hook, "purple"), (k_zoom, "light"), (k_what, "light"), (k_46, "light"), (k_myth, "navy"),
      (k_change, "light"), (k_tests, "light"), (k_who, "light"), (k_close, "light")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        D = [8, 10, 16, 11, 20, 14, 12, 15, 11]; tests = [(0, .8), (1, .9), (2, .9), (3, .9), (4, .9), (5, .9), (6, .9), (7, .9), (8, .9), (4, .4)]
        ims = []
        for si, p in tests:
            fn, bg = SC[si]; d = D[si]; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((270, 480)))
        s = Image.new("RGB", (270 * 5, 480 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 270, (i // 5) * 480))
        s.save("sheet.png")
    else: run(SC, "/tmp/ch_", "What_is_Chromosome_Hindi.mp4")
