import math, sys
from cbc_cartoon import run
from chromo_cartoon import PINK, SKYB
from gene_cartoon import person
from wes_cartoon import KID, DAD
from dmarker_cartoon import MOM
from alz_cartoon import tube
from lft_cartoon2 import *
from hts_close import close_scene

TOPIC = "GENETIC TEST  •  SMA"
BONE = (236, 239, 241); MUSC = (239, 154, 154); MUSC_D = (229, 115, 115); NEU = (255, 202, 40)

def gene_bar(d, x, y, w, missing=None, col=BLUE, lab=None, h=56):
    n = 8; bw = w / n
    for i in range(n):
        x0 = x + i * bw + 4
        if missing is not None and i == missing:
            for k in range(0, int(bw - 8), 16): d.line((x0 + k, y, x0 + k + 8, y), fill=RED, width=4); d.line((x0 + k, y + h, x0 + k + 8, y + h), fill=RED, width=4)
            d.line((x0, y, x0, y + h), fill=RED, width=4); d.line((x0 + bw - 8, y, x0 + bw - 8, y + h), fill=RED, width=4)
            continue
        d.rounded_rectangle((x0, y, x0 + bw - 8, y + h), 12, fill=(255, 167, 38) if i == 6 else col)
        d.text((x0 + (bw - 8) / 2, y + h / 2), str(i + 1), font=font("Bold", 26), fill=WHITE, anchor="mm")
    if lab: d.text((x - 20, y + h / 2), lab, font=font("Bold", 34), fill=DBLUE, anchor="rm")

def spine_scene(d, t, fade):
    for k in range(6):
        y = 380 + k * 70
        d.rounded_rectangle((140, y, 280, y + 56), 18, fill=BONE, outline=(176, 190, 197), width=4)
    for k in range(3):
        y = 430 + k * 120; alive = k >= int(fade * 3 + 0.001)
        c = NEU if alive else (200, 200, 200)
        d.ellipse((190, y - 18, 230, y + 22), fill=c)
        d.line((230, y, 640, y + 40 * k - 40), fill=c, width=8)
        if alive:
            px = 230 + ((t * 250 + k * 120) % 410)
            d.ellipse((px - 12, y - 12 + (px - 230) / 410 * (40 * k - 40), px + 12, y + 12 + (px - 230) / 410 * (40 * k - 40)), fill=(255, 111, 0))
    s = 1 - 0.45 * fade
    d.ellipse((640, 520 - 150 * s, 960, 520 + 150 * s), fill=MUSC, outline=MUSC_D, width=6)
    for k in range(5):
        xx = 690 + k * 55; d.line((xx, 520 - 110 * s, xx + 30, 520 + 110 * s), fill=MUSC_D, width=5)
    d.text((210, 820), "Spinal cord", font=font("Bold", 34), fill=DBLUE, anchor="mm")
    d.text((800, 820), "Muscle", font=font("Bold", 34), fill=MUSC_D, anchor="mm")

def punnett(d, p):
    person(d, 230, 540, PINK); person(d, 850, 540, SKYB)
    d.text((230, 670), "Mother: carrier", font=font("Bold", 34), fill=PINK, anchor="mm")
    d.text((850, 670), "Father: carrier", font=font("Bold", 34), fill=SKYB, anchor="mm")
    d.text((540, 550), "+", font=font("Bold", 90), fill=GREY, anchor="mm")
    kids = [("Healthy", GREEN), ("Carrier", ORANGE), ("Carrier", ORANGE), ("SMA", RED)]
    for i, (lab, c) in enumerate(kids):
        if p < (i + 1) / 5: break
        x = 160 + i * 253; y = 900
        d.rounded_rectangle((x - 115, y - 140, x + 115, y + 140), 26, fill=blend(c, (255, 255, 255), 0.85), outline=c, width=6)
        person(d, x, y - 10, c, 0.8); d.text((x, y + 100), lab, font=font("Bold", 34), fill=c, anchor="mm")

# ---------------- scenes ----------------
def s_hook(fr, t, D):
    rays(fr, 540, 900, t, (255, 140, 190), a=40)
    show(fr, pill(TOPIC, PURPLE, size=40), 230, t, 0.1)
    put(fr, KID["sad"], 540, 1280, 1.2)
    pop(fr, white_text("Baby can't hold the head up?", 60), 540, 450, t, 0.3, "pop")
    pop(fr, white_text("Late sitting or walking?", 64, color=YEL), 540, 590, t, D * 0.3, "boom")
    pop(fr, box_text("One cause: SMA, a genetic disease", RED, 44), 540, 780, t, D * 0.6, "whoosh")

def s_what(fr, t, D):
    show(fr, pill("WHAT IS SMA?", BLUE, size=50), 230, t, 0.1)
    d = ImageDraw.Draw(fr); spine_scene(d, t, min(1, max(0, (t - D * 0.3) / (D * 0.5)))); fire("pop", 0.3)
    show(fr, text_el("Spinal Muscular Atrophy", 54, color=DBLUE), 930, t, D * 0.15)
    show(fr, card("Nerves in the spinal cord slowly die", PURPLE, "1", size=38), 1060, t, D * 0.3)
    show(fr, card("Muscles become weak and thin", RED, "2", size=40), 1195, t, D * 0.55)
    fire("pop", D * 0.3); fire("pop", D * 0.55)

def s_gene(fr, t, D):
    show(fr, pill("THE GENE: SMN1", PURPLE, size=50), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    gene_bar(d, 230, 380, 760, None, BLUE, "Normal")
    if t > D * 0.2: gene_bar(d, 230, 500, 760, 6, BLUE, "SMA"); fire("boom", D * 0.2)
    if t > D * 0.2: d.text((230 + 6 * 95 + 45, 600), "Exon 7 missing", font=font("Bold", 36), fill=RED, anchor="mm")
    show(fr, card("Most patients: exon 7 missing in BOTH copies", RED, "1", size=34), 720, t, D * 0.3)
    show(fr, card("SMN2 'backup gene' makes a little protein", GREEN, "2", size=35), 855, t, D * 0.55)
    fire("pop", D * 0.3); fire("pop", D * 0.55)
    pop(fr, box_text("More SMN2 copies = usually milder", TEAL, 42), 540, 1030, t, D * 0.75, "ding")

def s_types(fr, t, D):
    show(fr, pill("TYPES OF SMA", ORANGE, size=50), 230, t, 0.1)
    rows = [("Type 1", "Birth to 6 months", RED), ("Type 2", "6 to 12 months", ORANGE), ("Type 3", "After early childhood", BLUE), ("Type 4", "Adulthood (mild)", GREEN)]
    d = ImageDraw.Draw(fr)
    for i, (a, b, c) in enumerate(rows):
        tin = 0.3 + i * D * 0.18; fire("pop", tin)
        if t < tin: continue
        y = 380 + i * 175
        d.rounded_rectangle((90, y, W - 90, y + 150), 30, fill=WHITE, outline=c, width=8)
        d.text((260, y + 75), a, font=font("Bold", 52), fill=c, anchor="mm")
        d.text((690, y + 75), b, font=font("Medium", 40), fill=GREY, anchor="mm")
    show(fr, text_el("When symptoms usually start", 40, "Medium", DBLUE), 1130, t, D * 0.85)

def s_inherit(fr, t, D):
    show(fr, pill("HOW IT PASSES ON", RED, size=50), 230, t, 0.1)
    d = ImageDraw.Draw(fr); p = (t - 0.4) / (D * 0.6)
    for i in range(4): fire("pop", 0.4 + (i + 1) / 5 * D * 0.6)
    punnett(d, p)
    show(fr, text_el("Carriers are healthy and usually don't know", 38, "Medium", GREY), 360, t, 0.3)
    pop(fr, box_text("Both carriers: 1 in 4 chance each pregnancy", RED, 38), 540, 1150, t, D * 0.8, "boom")

def s_india(fr, t, D):
    show(fr, pill("CARRIERS IN INDIA", PURPLE, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    for k in range(38):
        if t < 0.3 + k * 0.03: break
        r, c = divmod(k, 13); x = 120 + c * 70; y = 380 + r * 90
        col = ORANGE if k == 20 else (196, 205, 220)
        d.ellipse((x - 14, y - 32, x + 14, y - 4), fill=col); d.rounded_rectangle((x - 20, y - 2, x + 20, y + 34), 12, fill=col)
    fire("whoosh", 0.3)
    pop(fr, stroke_text("About 1 in 38", 110, ORANGE, WHITE, 9), 540, 760, t, D * 0.3, "boom")
    show(fr, text_el("healthy people were carriers (North India study)", 36, color=DBLUE), 870, t, D * 0.35)
    show(fr, card("Being a carrier is NOT a disease", GREEN, "1", size=40), 1000, t, D * 0.5)
    show(fr, card("Nothing to be ashamed of", BLUE, "2", size=40), 1135, t, D * 0.62)
    fire("pop", D * 0.5); fire("pop", D * 0.62)
    show(fr, text_el("It helps families plan", 42, "Medium", PURPLE), 1270, t, D * 0.75)

def s_test(fr, t, D):
    show(fr, pill("THE TEST: SMN1 BY MLPA", GREEN, size=46), 230, t, 0.1)
    d = ImageDraw.Draw(fr); tube(d, 200, 470); fire("pop", 0.3)
    d.text((620, 400), "One blood sample", font=font("Bold", 44), fill=DBLUE, anchor="mm")
    d.text((620, 470), "counts SMN1 copies", font=font("Medium", 40), fill=GREY, anchor="mm")
    rows = [("0 copies", "SMA confirmed", RED), ("1 copy", "Carrier", ORANGE), ("2 copies", "Usually normal", GREEN)]
    for i, (a, b, c) in enumerate(rows):
        tin = D * (0.2 + 0.15 * i); fire("pop", tin)
        if t < tin: continue
        y = 620 + i * 140
        d.rounded_rectangle((90, y, W - 90, y + 120), 28, fill=WHITE, outline=c, width=8)
        d.text((300, y + 60), a, font=font("Bold", 48), fill=c, anchor="mm")
        d.text((720, y + 60), b, font=font("Bold", 42), fill=GREY, anchor="mm")
    pop(fr, box_text("A few with 2 copies can still be carriers", PURPLE, 36), 540, 1110, t, D * 0.7, "ding")
    show(fr, text_el("Understand the report with a genetic counsellor", 36, "Medium", DBLUE), 1230, t, D * 0.8)

def s_who(fr, t, D):
    show(fr, pill("WHO SHOULD TEST?", BLUE, size=48), 230, t, 0.1)
    items = [("Child with SMA-like signs", RED, "1"), ("SMA in the family", ORANGE, "2"),
             ("Couples planning marriage / baby", PURPLE, "3"), ("Both carriers: test baby in pregnancy", BLUE, "4")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.1 + 0.15 * i)); show(fr, card(txt, c, m, size=37), 400 + i * 135, t, D * (0.1 + 0.15 * i))
    pop(fr, box_text("Only for disease. Baby's sex is NOT told.", RED, 38), 540, 1000, t, D * 0.75, "boom")
    if t > D * 0.4: put(fr, MOM, 330, 1300, 0.5); put(fr, DAD, 750, 1320, 0.65)

def s_treat(fr, t, D):
    show(fr, pill("GOOD NEWS", GREEN, size=52), 230, t, 0.1)
    put(fr, KID["happy"], 540, 560, 0.75); sparkles(fr, 540, 520, 220, t, 7); fire("ding", 0.3)
    show(fr, card("SMA now has treatment", GREEN, "1", size=42), 840, t, D * 0.15)
    show(fr, card("Medicine available in India too", BLUE, "2", size=40), 975, t, D * 0.3)
    show(fr, card("Earlier start = better results", ORANGE, "3", size=40), 1110, t, D * 0.45)
    show(fr, card("Rare disease policy: financial help", PURPLE, "4", size=38), 1245, t, D * 0.6)
    for k in (0.15, 0.3, 0.45, 0.6): fire("pop", D * k)
    show(fr, text_el("Treatment decided only by a specialist", 38, "Medium", RED), 1390, t, D * 0.8)

SC = [(s_hook, "purple"), (s_what, "light"), (s_gene, "light"), (s_types, "light"), (s_inherit, "light"),
      (s_india, "light"), (s_test, "light"), (s_who, "light"), (s_treat, "light"),
      (close_scene("Had you heard of SMA before?", TOPIC), "light")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si in range(10):
            fn, bg = SC[si]; d = 14; p = 0.95; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((360, 640)))
        s = Image.new("RGB", (360 * 5, 640 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 360, (i // 5) * 640))
        s.save("sheet.png")
    else: run(SC, "/tmp/sma_", "SMA_Genetic_Test_Hindi.mp4")
