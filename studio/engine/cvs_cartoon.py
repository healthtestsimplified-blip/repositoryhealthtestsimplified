import math, sys
from cbc_cartoon import run
from chromo_cartoon import x_shape, PINK, SKYB
from dmarker_cartoon import MOM, LAV
from lft_cartoon2 import *

def womb(fr, cx, cy, t, target="placenta", p=1.0):
    d = ImageDraw.Draw(fr)
    d.ellipse((cx - 330, cy - 260, cx + 330, cy + 260), fill=(244, 143, 177))
    d.ellipse((cx - 300, cy - 230, cx + 300, cy + 230), fill=(207, 232, 252))                     # amniotic fluid
    d.chord((cx - 300, cy - 230, cx + 300, cy + 230), 200, 290, fill=(183, 28, 28))               # placenta
    bx, by = cx + 40, cy + 40
    d.ellipse((bx - 150, by - 80, bx + 90, by + 130), fill=(255, 205, 180))                       # baby body
    d.ellipse((bx + 30, by - 150, bx + 170, by - 10), fill=(255, 205, 180))                       # head
    d.ellipse((bx + 115, by - 95, bx + 131, by - 79), fill=(60, 40, 40))
    d.arc((bx + 100, by - 75, bx + 140, by - 45), 20, 160, fill=(200, 100, 100), width=4)
    d.line((bx - 60, by - 5, bx + 60, by - 40), fill=(255, 190, 160), width=24)
    d.line((bx - 150, by + 90, bx - 60, by + 140), fill=(255, 190, 160), width=24)
    d.text((cx - 140, cy - 150), "Placenta", font=font("Bold", 30), fill=WHITE, anchor="mm")
    # ultrasound probe on top
    px, py = cx + 200, cy - 330
    d.rounded_rectangle((px - 45, py - 70, px + 45, py + 20), 20, fill=(90, 100, 120))
    d.rounded_rectangle((px - 60, py + 10, px + 60, py + 40), 12, fill=(60, 70, 90))
    for k in range(3):
        r = 60 + ((t * 120 + k * 50) % 150)
        d.arc((px - r, py + 20 - r * 0.4, px + r, py + 20 + r * 1.2), 60, 120, fill=(0, 170, 200), width=5)
    # needle
    tx, ty = (cx - 180, cy - 120) if target == "placenta" else (cx - 235, cy + 40)
    sx, sy = cx - 60, cy - 380
    k = max(0, min(1, p))
    ex, ey = sx + (tx - sx) * k, sy + (ty - sy) * k
    d.line((sx, sy, ex, ey), fill=(120, 120, 130), width=8)
    d.rounded_rectangle((sx - 22, sy - 60, sx + 22, sy), 8, fill=(200, 210, 225), outline=(120, 120, 130), width=3)
    if k >= 1: d.ellipse((tx - 30, ty - 30, tx + 30, ty + 30), outline=YEL, width=8)

def stairs(d, p):
    steps = [("Double marker", "Screening", PINK), ("NIPT", "Screening", SKYB), ("CVS / Amnio", "DIAGNOSIS", GREEN)]
    for i, (a, b, c) in enumerate(steps):
        if p < i / 3: break
        x0 = 80 + i * 320; y0 = 820 - i * 170
        d.rounded_rectangle((x0, y0, x0 + 300, 900), 24, fill=c)
        d.text((x0 + 150, y0 + 50), a, font=font("Bold", 36), fill=WHITE, anchor="mm")
        d.text((x0 + 150, y0 + 100), b, font=font("Bold", 30), fill=YEL if i == 2 else WHITE, anchor="mm")

def cmp_table():
    rows = [("", "CVS", "Amniocentesis"), ("When", "11–14 weeks", "From 15 weeks"), ("Sample", "Tiny bit of placenta", "Fluid around baby"),
            ("Quick result", "2–3 days", "2–3 days"), ("Full report", "about 2–3 weeks", "about 2–3 weeks"), ("Miscarriage risk", "Small (<1%)", "Small (<1%)")]
    colw = [300, 330, 330]; rh = 104; tw = sum(colw); x0 = (W - tw) // 2
    im = Image.new("RGBA", (W, rh * len(rows) + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((x0, 0, x0 + tw, rh * len(rows)), 28, fill=WHITE, outline=(200, 215, 235), width=3)
    d.rounded_rectangle((x0 + colw[0] + 8, 8, x0 + colw[0] + colw[1] - 8, rh - 8), 20, fill=(183, 28, 28))
    d.rounded_rectangle((x0 + colw[0] + colw[1] + 8, 8, x0 + tw - 8, rh - 8), 20, fill=SKYB)
    for r, row in enumerate(rows):
        y = r * rh + rh / 2; x = x0
        for c, cell in enumerate(row):
            if r == 0: f, col = font("Bold", 34), WHITE
            elif c == 0: f, col = font("Bold", 30), DBLUE
            else: f, col = font("Bold", 30), ((183, 28, 28) if c == 1 else SKYB)
            d.text((x + colw[c] / 2, y), cell, font=f, fill=col, anchor="mm"); x += colw[c]
        if 0 < r < len(rows) - 1: d.line((x0 + 24, (r + 1) * rh, x0 + tw - 24, (r + 1) * rh), fill=(225, 232, 242), width=2)
    return im

# ---------------- scenes ----------------
def v_hook(fr, t, D):
    rays(fr, 540, 900, t, (120, 220, 160), a=40)
    put(fr, MOM, 540, 1390 + 8 * math.sin(t * 2), 0.8)
    pop(fr, white_text("NIPT says HIGH RISK? Now what?", 80), 540, 560, t, 0.1, "boom")
    pop(fr, white_text("Get a CONFIRMED answer", 64, color=YEL), 540, 780, t, 1.8, "whoosh")
    pop(fr, box_text("CVS or Amniocentesis: is it safe? Watch till the end!", GREEN, 38), 540, 980, t, D * 0.55, "pop")

def v_stairs(fr, t, D):
    show(fr, pill("SCREENING vs DIAGNOSIS", BLUE, size=46), 230, t, 0.1)
    p = (t - 0.3) / (D * 0.5)
    for i in range(3): fire("pop" if i < 2 else "ding", 0.3 + i / 3 * D * 0.5)
    stairs(ImageDraw.Draw(fr), p)
    show(fr, text_el("Screening tells the CHANCE", 50, color=DBLUE), 980, t, D * 0.6)
    show(fr, text_el("Diagnosis gives a CONFIRMED answer", 50, color=GREEN), 1070, t, D * 0.72)

def v_cvs(fr, t, D):
    show(fr, pill("CVS: CHORIONIC VILLUS SAMPLING", (183, 28, 28), size=40), 230, t, 0.1)
    womb(fr, 540, 770, t, "placenta", (t - D * 0.2) / (D * 0.25)); fire("whoosh", D * 0.2); fire("ding", D * 0.45)
    items = [("Done at 11–14 weeks", GREEN, "1"), ("Takes a tiny sample of placenta", (183, 28, 28), "2"),
             ("Through tummy (or cervix), under ultrasound", BLUE, "3")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.45 + 0.13 * i)); show(fr, card(txt, c, m, size=38), 1080 + i * 130, t, D * (0.45 + 0.13 * i))

def v_amnio(fr, t, D):
    show(fr, pill("AMNIOCENTESIS", SKYB, size=48), 230, t, 0.1)
    womb(fr, 540, 770, t, "fluid", (t - D * 0.2) / (D * 0.25)); fire("whoosh", D * 0.2); fire("ding", D * 0.45)
    items = [("Done from 15 weeks", GREEN, "1"), ("Takes 3–4 teaspoons of fluid", SKYB, "2"),
             ("The fluid carries baby's cells", PURPLE, "3")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.45 + 0.13 * i)); show(fr, card(txt, c, m, size=40), 1080 + i * 130, t, D * (0.45 + 0.13 * i))

def v_compare(fr, t, D):
    show(fr, pill("CVS vs AMNIOCENTESIS", LAV, size=48), 230, t, 0.1)
    fire("pop", 0.5); show(fr, cmp_table(), 380, t, 0.5)
    show(fr, text_el("Your doctor chooses based on your weeks", 44, "Medium", GREEN), 1060, t, D * 0.7)
    show(fr, text_el("Screenshot this!", 44, "Bold", TEAL), 1150, t, D * 0.8)

def v_checks(fr, t, D):
    show(fr, pill("WHAT CAN THEY CONFIRM?", GREEN, size=46), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    if t > 0.4:
        for k in range(3): x_shape(d, 400 + k * 140, 460, 100, (120, 70, 200) if k < 2 else RED)
    fire("pop", 0.4)
    items = [("Chromosome issues (e.g. Down)", PURPLE, "1"), ("Thalassaemia major in baby", RED, "2"),
             ("Other genetic diseases, if needed", TEAL, "3")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.15 + 0.15 * i)); show(fr, card(txt, c, m, size=38), 600 + i * 135, t, D * (0.15 + 0.15 * i))
    pop(fr, box_text("Both parents thalassaemia carriers? This can check the baby!", RED, 38), 540, 1080, t, D * 0.6, "ding")
    show(fr, text_el("Baby's sex is NOT disclosed: illegal in India", 38, "Bold", ORANGE), 1230, t, D * 0.8)

def v_safe(fr, t, D):
    show(fr, pill("IS IT SAFE?", ORANGE, size=50), 230, t, 0.1)
    ground(fr, 250, 770, 300); put(fr, MOM, 250, 540, 0.6)
    ground(fr, 790, 770, 300); put(fr, DOC["idle"], 790, 560, 0.7)
    items = [("Done by an expert, under ultrasound", BLUE, "1"), ("Takes a few minutes: feels like pressure", TEAL, "2"),
             ("Small miscarriage risk, usually under 1%", ORANGE, "3"), ("Rh-negative mother? Anti-D may be needed", RED, "4")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.12 + 0.18 * i)); show(fr, card(txt, c, m, size=38), 850 + i * 135, t, D * (0.12 + 0.18 * i))

def v_after(fr, t, D):
    show(fr, pill("AFTER THE TEST", PINK, size=48), 230, t, 0.1)
    put(fr, MOM, 540, 560, 0.65); sparkles(fr, 540, 540, 200, t, 5, (255, 150, 190))
    show(fr, card("Rest for the day", GREEN, "1", size=42), 860, t, D * 0.15)
    show(fr, card("Avoid heavy work for 1–2 days", BLUE, "2", size=42), 990, t, D * 0.3)
    fire("pop", D * 0.15); fire("pop", D * 0.3)
    show(fr, box_text("Call your doctor if: fever, bleeding, leaking fluid or strong pain", RED, 38), 1140, t, D * 0.5)
    fire("boom", D * 0.5)

def v_choice(fr, t, D):
    show(fr, pill("YOUR CHOICE, YOUR RIGHT", LAV, size=46), 230, t, 0.1)
    ground(fr, 300, 900, 320); put(fr, MOM, 300, 620, 0.75)
    ground(fr, 790, 900, 300); put(fr, DOC["idle"], 790, 660, 0.75)
    pop(fr, box_text("Decide only after genetic counselling with your doctor", PURPLE, 40), 540, 1050, t, D * 0.3, "ding")
    show(fr, text_el("Ask all your questions. There are no silly ones!", 44, "Medium", GREEN), 1210, t, D * 0.6)

def v_close(fr, t, D):
    show(fr, big_logo(), 210, t, 0.2)
    fire("ding", 0.8); show(fr, box_text("Take any medicine only as advised by your doctor", GREEN, 42), 820, t, 0.8)
    show(fr, text_el("Want a thalassaemia video next?", 54, color=DBLUE), 1020, t, D * 0.45)
    show(fr, text_el("Tell us in the comments!", 44, "Medium", GREY), 1120, t, D * 0.55)
    show(fr, pill("Follow Health Test Simplified", BLUE, size=40), 1300, t, D * 0.65)
    show(fr, text_el("For awareness only. Consult your doctor.", 30, "Regular", GREY), 1680, t, D * 0.7)

SC = [(v_hook, "navy"), (v_stairs, "light"), (v_cvs, "light"), (v_amnio, "light"), (v_compare, "light"),
      (v_checks, "light"), (v_safe, "light"), (v_after, "light"), (v_choice, "light"), (v_close, "light")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        D = [10, 12, 15, 14, 12, 15, 14, 12, 10, 11]; tests = [(0, .8), (1, .95), (2, .95), (3, .95), (4, .95), (5, .95), (6, .95), (7, .95), (8, .9), (9, .9)]
        ims = []
        for si, p in tests:
            fn, bg = SC[si]; d = D[si]; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((270, 480)))
        s = Image.new("RGB", (270 * 5, 480 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 270, (i // 5) * 480))
        s.save("sheet.png")
    else: run(SC, "/tmp/cv_", "CVS_Amniocentesis_Hindi.mp4")
