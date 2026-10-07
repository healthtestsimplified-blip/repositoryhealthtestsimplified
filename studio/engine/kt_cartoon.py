import math, sys
from cbc_cartoon import run
from chromo_cartoon import x_shape, karyotype, CHROMO, PINK, SKYB
from dmarker_cartoon import MOM, LAV
from wes_cartoon import KID, DAD, kid_sprite
from lft_cartoon2 import *

CPUR = (120, 70, 200)

def tube(d, x, y):
    d.rounded_rectangle((x - 40, y - 110, x + 40, y + 110), 30, fill=WHITE, outline=(150, 160, 175), width=6)
    d.rounded_rectangle((x - 34, y - 30, x + 34, y + 104), 26, fill=(200, 30, 45)); d.rectangle((x - 46, y - 120, x + 46, y - 80), fill=(120, 60, 200))

def dish(d, x, y, t):
    d.ellipse((x - 100, y - 45, x + 100, y + 45), fill=(235, 245, 255), outline=(150, 170, 200), width=6)
    for k in range(9):
        a = k * 0.7 + t * 0.5; r = 30 + (k % 3) * 18
        cx, cy = x + r * math.cos(a), y + r * 0.4 * math.sin(a)
        d.ellipse((cx - 11, cy - 9, cx + 11, cy + 9), fill=(240, 120, 150))

def microscope(d, x, y):
    c = (60, 75, 110)
    d.rounded_rectangle((x - 90, y + 80, x + 90, y + 110), 12, fill=c)
    d.line((x + 40, y + 85, x + 40, y - 40), fill=c, width=26)
    d.line((x + 40, y - 40, x - 20, y - 110), fill=c, width=34)
    d.rounded_rectangle((x - 50, y - 150, x + 0, y - 100), 10, fill=c)
    d.rectangle((x - 70, y + 10, x + 40, y + 26), fill=c)
    d.line((x - 30, y - 60, x - 30, y + 10), fill=c, width=16)

def mini_kary(d, x, y):
    d.rounded_rectangle((x - 100, y - 100, x + 100, y + 100), 18, fill=WHITE, outline=(200, 210, 225), width=4)
    for i in range(12):
        r, c = divmod(i, 4); xx = x - 66 + c * 44; yy = y - 60 + r * 60
        x_shape(d, xx - 9, yy, 26, SKYB, False); x_shape(d, xx + 9, yy, 26, PINK, False)

def lab_flow(p, t):
    im = Image.new("RGBA", (W, 340), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    xs = [120, 380, 640, 910]; labs = ["Blood", "Grow cells", "Stain & photo", "Arrange pairs"]
    for i, x in enumerate(xs):
        if p < i / 4: break
        cy = 140
        if i == 0: tube(d, x, cy)
        elif i == 1: dish(d, x, cy, t)
        elif i == 2: microscope(d, x, cy)
        else: mini_kary(d, x, cy)
        d.text((x, 300), labs[i], font=font("Bold", 32), fill=DBLUE, anchor="mm")
        if i < 3 and p > (i + 1) / 4: d.text((x + 130, cy), "›", font=font("Bold", 90), fill=ORANGE, anchor="mm")
    return im

def finds_grid(p):
    im = Image.new("RGBA", (W, 860), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    data = [("EXTRA one", "Down syndrome (+21)", PURPLE), ("MISSING one", "Turner syndrome (45,X)", PINK),
            ("Extra X in men", "Klinefelter (47,XXY)", SKYB), ("Pieces SWAPPED", "Translocation", ORANGE)]
    for i, (a, b, c) in enumerate(data):
        if p < i / 4: break
        r, cc = divmod(i, 2); x0 = 60 + cc * 490; y0 = r * 430
        d.rounded_rectangle((x0, y0, x0 + 470, y0 + 400), 30, fill=WHITE, outline=c, width=7)
        cx, cy = x0 + 235, y0 + 140
        if i == 0:
            for k in range(3): x_shape(d, cx - 110 + k * 110, cy, 100, RED if k == 2 else CPUR, False)
        elif i == 1:
            x_shape(d, cx - 60, cy, 110, PINK, False)
            d.rounded_rectangle((cx + 10, cy - 55, cx + 120, cy + 55), 16, outline=(190, 200, 215), width=5)
            d.text((cx + 65, cy), "?", font=font("Bold", 64), fill=(190, 200, 215), anchor="mm")
        elif i == 2:
            for k, (ch, col) in enumerate((("X", PINK), ("X", RED), ("Y", SKYB))):
                d.text((cx - 110 + k * 110, cy), ch, font=font("Bold", 110), fill=col, anchor="mm")
        else:
            for k, (top, bot) in enumerate(((ORANGE, CPUR), (CPUR, ORANGE))):
                x = cx - 70 + k * 140
                d.rounded_rectangle((x - 28, cy - 100, x + 28, cy - 10), 24, fill=top)
                d.rounded_rectangle((x - 28, cy + 10, x + 28, cy + 100), 24, fill=bot)
                d.ellipse((x - 16, cy - 16, x + 16, cy + 16), fill=GREY)
            d.text((cx, cy), "⇄", font=font("Bold", 60), fill=GREY, anchor="mm") if False else None
        d.text((cx, y0 + 285), a, font=font("Bold", 40), fill=c, anchor="mm")
        d.text((cx, y0 + 345), b, font=font("Medium", 32), fill=DBLUE, anchor="mm")
    return im

def chromo_bar(d, x, y, top, bot, h=300):
    for dx in (-30, 30):
        d.rounded_rectangle((x + dx - 26, y - h / 2, x + dx + 26, y - 12), 26, fill=top)
        d.rounded_rectangle((x + dx - 26, y + 12, x + dx + 26, y + h / 2), 26, fill=bot)
    d.ellipse((x - 30, y - 22, x + 30, y + 22), fill=blend(bot, (0, 0, 0), 0.3))

# ---------------- scenes ----------------
def k_hook(fr, t, D):
    rays(fr, 540, 900, t, (200, 140, 255), a=40)
    put(fr, CHROMO, 540, 1380 + 15 * math.sin(t * 3), 0.9)
    pop(fr, white_text("Repeated miscarriages? Trouble having a baby?", 72), 540, 470, t, 0.1, "boom")
    pop(fr, white_text("ONE test counts all 46 chromosomes!", 64, color=YEL), 540, 730, t, D * 0.45, "whoosh")
    pop(fr, box_text("Karyotyping: watch till the end", GREEN, 44), 540, 920, t, D * 0.7, "pop")

def k_what(fr, t, D):
    show(fr, pill("WHAT IS KARYOTYPING?", PURPLE, size=48), 230, t, 0.1)
    fire("whoosh", 0.3); fr.alpha_composite(karyotype((t - 0.3) / (D * 0.5)), (0, 330))
    show(fr, text_el("All 46 chromosomes, in 23 pairs", 50, color=DBLUE), 1150, t, D * 0.55)
    show(fr, card("Half from mother, half from father", PINK, "♀", size=40), 1290, t, D * 0.7)
    fire("ding", D * 0.55); fire("pop", D * 0.7)

def k_how(fr, t, D):
    show(fr, pill("HOW IS IT DONE?", BLUE, size=48), 230, t, 0.1)
    p = (t - 0.3) / (D * 0.5)
    for k in range(4): fire("pop", 0.3 + k / 4 * D * 0.5)
    fr.alpha_composite(lab_flow(p, t), (0, 360))
    show(fr, card("Usually just a blood sample", RED, "1", size=40), 820, t, D * 0.15)
    show(fr, card("Cells grown, stained & photographed", PURPLE, "2", size=40), 955, t, D * 0.45)
    show(fr, card("In pregnancy: CVS / amnio sample", PINK, "3", size=38), 1090, t, D * 0.75)
    fire("pop", D * 0.15); fire("pop", D * 0.45); fire("pop", D * 0.75)

def k_finds(fr, t, D):
    show(fr, pill("WHAT CAN IT FIND?", ORANGE, size=48), 230, t, 0.1)
    p = (t - 0.4) / (D * 0.8)
    for i in range(4): fire("pop", 0.4 + i / 4 * D * 0.8)
    fr.alpha_composite(finds_grid(p), (0, 340))
    show(fr, text_el("Screenshot this!", 44, "Bold", TEAL), 1250, t, D * 0.9)

def k_trans(fr, t, D):
    show(fr, pill("BALANCED TRANSLOCATION", ORANGE, size=46), 230, t, 0.1)
    d = ImageDraw.Draw(fr); sw = t > D * 0.3
    chromo_bar(d, 360, 540, ORANGE if sw else CPUR, CPUR)
    chromo_bar(d, 720, 540, CPUR if sw else ORANGE, ORANGE)
    if sw: sparkles(fr, 540, 440, 230, t, 6)
    fire("zap", D * 0.3)
    show(fr, text_el("Two chromosomes swap pieces", 50, color=DBLUE), 770, t, D * 0.2)
    show(fr, card("The person is completely healthy", GREEN, "✓", size=40), 900, t, D * 0.4)
    show(fr, card("Baby may get an unbalanced part", RED, "!", size=38), 1035, t, D * 0.55)
    show(fr, card("Can cause repeated miscarriages", ORANGE, "!", size=40), 1170, t, D * 0.68)
    fire("pop", D * 0.4); fire("pop", D * 0.55); fire("pop", D * 0.68)
    pop(fr, box_text("So BOTH husband & wife are tested", BLUE, 42), 540, 1360, t, D * 0.82, "ding")

def k_who(fr, t, D):
    show(fr, pill("WHO SHOULD GET IT?", GREEN, size=48), 230, t, 0.1)
    ground(fr, 230, 640, 260); put(fr, MOM, 230, 470, 0.5)
    ground(fr, 540, 640, 220); put(fr, DAD, 540, 470, 0.7)
    ground(fr, 850, 640, 260); put(fr, DOC["idle"], 850, 440, 0.55)
    items = [("2 or more miscarriages", RED, "1"), ("Infertility / very low sperm count", BLUE, "2"),
             ("Child with delay or birth defects", PURPLE, "3"), ("Girl: short height, no periods", PINK, "4"),
             ("Some blood cancers (bone marrow)", TEAL, "5")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.1 + 0.15 * i)); show(fr, card(txt, c, m, size=38), 720 + i * 130, t, D * (0.1 + 0.15 * i))

def k_report(fr, t, D):
    show(fr, pill("READING THE REPORT", ORANGE, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    rows = [("46,XX", "Normal female", PINK), ("46,XY", "Normal male", SKYB), ("47,XY,+21", "Down syndrome (extra 21)", RED)]
    for i, (a, b, c) in enumerate(rows):
        tin = 0.4 + i * D * 0.2; fire("pop", tin)
        if t < tin: break
        y = 370 + i * 230
        d.rounded_rectangle((70, y, W - 70, y + 200), 30, fill=WHITE, outline=c, width=8)
        d.text((W / 2, y + 68), a, font=font("Bold", 64), fill=c, anchor="mm")
        d.text((W / 2, y + 148), b, font=font("Medium", 38), fill=GREY, anchor="mm")
    pop(fr, box_text("First number = total chromosomes", PURPLE, 42), 540, 1150, t, D * 0.78, "ding")

def k_know(fr, t, D):
    show(fr, pill("GOOD TO KNOW", PURPLE, size=48), 230, t, 0.1)
    put(fr, CHROMO, 540, 520 + 10 * math.sin(t * 3), 0.6)
    items = [("Report takes about 2–3 weeks", BLUE, "1"), ("Tiny changes need microarray / exome", ORANGE, "2"),
             ("Baby's sex is NOT disclosed in pregnancy", PINK, "3"), ("Understand the report with your doctor", GREEN, "4")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.1 + 0.18 * i)); show(fr, card(txt, c, m, size=36), 800 + i * 140, t, D * (0.1 + 0.18 * i))

def k_close(fr, t, D):
    show(fr, big_logo(), 210, t, 0.2)
    fire("ding", 0.8); show(fr, box_text("Take any medicine only as advised by your doctor", GREEN, 42), 820, t, 0.8)
    show(fr, text_el("Had you heard of karyotyping before?", 54, color=DBLUE), 1020, t, D * 0.4)
    show(fr, text_el("Share with someone who needs it!", 44, "Medium", GREY), 1180, t, D * 0.5)
    show(fr, pill("Follow Health Test Simplified", BLUE, size=40), 1320, t, D * 0.6)
    show(fr, text_el("For awareness only. Consult your doctor.", 30, "Regular", GREY), 1680, t, D * 0.7)

SC = [(k_hook, "purple"), (k_what, "light"), (k_how, "light"), (k_finds, "light"), (k_trans, "light"),
      (k_who, "light"), (k_report, "light"), (k_know, "light"), (k_close, "light")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        D = [13, 16, 18, 15, 17, 18, 16, 18, 14]; tests = [(0, .9), (1, .95), (2, .95), (3, .95), (4, .95), (5, .95), (6, .95), (7, .95), (8, .9)]
        ims = []
        for si, p in tests:
            fn, bg = SC[si]; d = D[si]; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((360, 640)))
        s = Image.new("RGB", (360 * 5, 640 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 360, (i // 5) * 640))
        s.save("sheet.png")
    else: run(SC, "/tmp/kt_", "Karyotyping_Hindi.mp4")
