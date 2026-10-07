import math, sys, random
from cbc_cartoon import run
from chromo_cartoon import x_shape, CHROMO, PINK, SKYB
from dmarker_cartoon import MOM, LAV
from wes_cartoon import KID, DAD
from kt_cartoon import tube
from lft_cartoon2 import *

CPUR = (120, 70, 200); C750 = (0, 137, 123); C315 = (94, 53, 177)

def chromo_strip(d, x0, y, w, h, gap=None, dup=None):
    """horizontal chromosome with bands; gap=(a,b) fraction deleted, dup=(a,b) extra."""
    d.rounded_rectangle((x0, y - h / 2, x0 + w, y + h / 2), int(h / 2), fill=(200, 185, 235))
    for k in range(14):
        bx = x0 + 30 + k * (w - 60) / 14
        d.rectangle((bx, y - h / 2 + 4, bx + (w - 60) / 28, y + h / 2 - 4), fill=CPUR if k % 2 else (160, 130, 220))
    d.ellipse((x0 + w * 0.38 - 18, y - h / 2 - 4, x0 + w * 0.38 + 18, y + h / 2 + 4), fill=(90, 50, 160))
    if gap:
        d.rectangle((x0 + w * gap[0], y - h / 2 - 6, x0 + w * gap[1], y + h / 2 + 6), fill=(245, 248, 252))
        d.rectangle((x0 + w * gap[0], y - h / 2 - 6, x0 + w * gap[1], y + h / 2 + 6), outline=RED, width=5)
    if dup:
        d.rounded_rectangle((x0 + w * dup[0], y - h / 2 - 34, x0 + w * dup[1], y - h / 2 - 6), 10, fill=ORANGE)

def maps(p, t):
    im = Image.new("RGBA", (W, 520), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, (title, sub, col) in enumerate((("KARYOTYPE", "Sees only big changes", BLUE), ("MICROARRAY", "Zooms into tiny pieces", C750))):
        if p < i * 0.5: break
        x0 = 60 + i * 490
        d.rounded_rectangle((x0, 0, x0 + 470, 500), 30, fill=WHITE, outline=col, width=7)
        d.text((x0 + 235, 50), title, font=font("Bold", 42), fill=col, anchor="mm")
        if i == 0:
            x_shape(d, x0 + 235, 240, 220, CPUR)
        else:
            chromo_strip(d, x0 + 40, 200, 390, 60, gap=(0.62, 0.7))
            cx, cy = x0 + 40 + 390 * 0.66, 200
            r = 70 + 6 * math.sin(t * 4)
            d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=GREY, width=10)
            d.line((cx + r * 0.7, cy + r * 0.7, cx + r * 1.5, cy + r * 1.5), fill=GREY, width=18)
            d.text((x0 + 235, 330), "missing piece!", font=font("Bold", 34), fill=RED, anchor="mm")
        d.text((x0 + 235, 440), sub, font=font("Medium", 32), fill=DBLUE, anchor="mm")
    return im

def chip(d, x, y, t, n=12):
    d.rounded_rectangle((x - 150, y - 150, x + 150, y + 150), 24, fill=(40, 55, 90))
    s = 240 / n
    for r in range(n):
        for c in range(n):
            v = (math.sin(r * 1.7 + c * 2.3 + t * 3) + 1) / 2
            col = blend((60, 200, 120), (255, 80, 80), v) if (r * 7 + c * 3) % 5 else (255, 214, 0)
            cx, cy = x - 120 + c * s + s / 2, y - 120 + r * s + s / 2
            d.ellipse((cx - s * 0.32, cy - s * 0.32, cx + s * 0.32, cy + s * 0.32), fill=col)

def plot(p):
    im = Image.new("RGBA", (W, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    x0, x1, y0 = 90, 990, 210
    d.rounded_rectangle((60, 0, W - 60, 400), 26, fill=WHITE, outline=(210, 220, 235), width=3)
    d.line((x0, y0, x1, y0), fill=(200, 210, 225), width=3)
    random.seed(3); n = int(170 * max(0, min(1, p)))
    for k in range(n):
        x = x0 + k * (x1 - x0) / 170; f = k / 170
        off = 80 if 0.25 < f < 0.36 else (-80 if 0.68 < f < 0.78 else 0)
        y = y0 + off + random.uniform(-18, 18)
        col = RED if off > 0 else (ORANGE if off < 0 else (120, 140, 170))
        d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=col)
    if p > 0.45: d.text((x0 + 0.3 * (x1 - x0), y0 + 150), "LESS (deletion)", font=font("Bold", 32), fill=RED, anchor="mm")
    if p > 0.85: d.text((x0 + 0.73 * (x1 - x0), y0 - 140), "EXTRA (duplication)", font=font("Bold", 32), fill=ORANGE, anchor="mm")
    return im

def cmp_table():
    rows = [("", "750K", "315K"), ("Probes", "~7.5 lakh", "~3.15 lakh"), ("Detail", "Finer", "Focused"),
            ("Mostly for", "Children & adults", "Pregnancy & loss"), ("Sample", "Blood", "CVS / amnio / tissue")]
    colw = [260, 350, 350]; rh = 120; tw = sum(colw); x0 = (W - tw) // 2
    im = Image.new("RGBA", (W, rh * len(rows) + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((x0, 0, x0 + tw, rh * len(rows)), 28, fill=WHITE, outline=(200, 215, 235), width=3)
    d.rounded_rectangle((x0 + colw[0] + 8, 8, x0 + colw[0] + colw[1] - 8, rh - 8), 20, fill=C750)
    d.rounded_rectangle((x0 + colw[0] + colw[1] + 8, 8, x0 + tw - 8, rh - 8), 20, fill=C315)
    for r, row in enumerate(rows):
        y = r * rh + rh / 2; x = x0
        for c, cell in enumerate(row):
            if r == 0: f, col = font("Bold", 52), WHITE
            elif c == 0: f, col = font("Bold", 32), DBLUE
            else: f, col = font("Bold", 32), (C750 if c == 1 else C315)
            d.text((x + colw[c] / 2, y), cell, font=f, fill=col, anchor="mm"); x += colw[c]
        if 0 < r < len(rows) - 1: d.line((x0 + 24, (r + 1) * rh, x0 + tw - 24, (r + 1) * rh), fill=(225, 232, 242), width=2)
    return im

def pix_heart(d, cx, cy, size, cells, col):
    s = size / cells
    for r in range(cells):
        for c in range(cells):
            u = (c + 0.5) / cells * 2.6 - 1.3; v = 1.2 - (r + 0.5) / cells * 2.5
            inside = (u * u + v * v - 1) ** 3 - u * u * v ** 3 <= 0
            x, y = cx - size / 2 + c * s, cy - size / 2 + r * s
            d.rectangle((x + 1, y + 1, x + s - 1, y + s - 1), fill=col if inside else (236, 240, 247))

def bars(p):
    im = Image.new("RGBA", (W, 560), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    data = [("Karyotype", "3–5%", 0.045, BLUE), ("Microarray", "15–20%", 0.18, C750)]
    base = 470
    for i, (lab, txt, v, c) in enumerate(data):
        x = 330 + i * 420; h = 2100 * v * ease(max(0, min(1, (p - i * 0.3) / 0.5)))
        d.rounded_rectangle((x - 110, base - h, x + 110, base), 20, fill=c)
        if h > 5: d.text((x, base - h - 45), txt, font=font("Bold", 52), fill=c, anchor="mm")
        d.text((x, base + 50), lab, font=font("Bold", 40), fill=DBLUE, anchor="mm")
    d.line((140, base, 940, base), fill=(190, 200, 215), width=4)
    return im

# ---------------- scenes ----------------
def c_hook(fr, t, D):
    rays(fr, 540, 900, t, (120, 220, 200), a=40)
    put(fr, KID["sad"], 540, 1340 + 6 * math.sin(t * 2), 0.8)
    pop(fr, white_text("Karyotype normal, but child still has delay or autism?", 70), 540, 480, t, 0.1, "boom")
    pop(fr, white_text("The change may be too tiny to see!", 62, color=YEL), 540, 750, t, D * 0.35, "whoosh")
    pop(fr, box_text("Chromosomal Microarray: 750K vs 315K. Watch till the end!", GREEN, 38), 540, 940, t, D * 0.65, "pop")

def c_what(fr, t, D):
    show(fr, pill("WHAT IS MICROARRAY?", C750, size=48), 230, t, 0.1)
    fire("pop", 0.4); fire("whoosh", D * 0.3)
    fr.alpha_composite(maps((t - 0.4) / (D * 0.5), t), (0, 340))
    show(fr, text_el("Karyotype = state map. Microarray = street map!", 44, color=DBLUE), 930, t, D * 0.45)
    show(fr, card("DELETION: tiny piece missing", RED, "−", size=40), 1080, t, D * 0.65)
    show(fr, card("DUPLICATION: tiny piece extra", ORANGE, "+", size=40), 1215, t, D * 0.8)
    fire("pop", D * 0.65); fire("pop", D * 0.8)

def c_how(fr, t, D):
    show(fr, pill("HOW IS IT DONE?", BLUE, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    if t > 0.3:
        tube(d, 220, 500); d.text((220, 650), "DNA from blood", font=font("Bold", 32), fill=RED, anchor="mm")
    if t > D * 0.3:
        d.text((420, 500), "›", font=font("Bold", 110), fill=ORANGE, anchor="mm")
        chip(d, 700, 490, t); d.text((700, 690), "Chip with lakhs of probes", font=font("Bold", 32), fill=DBLUE, anchor="mm")
    fire("pop", 0.3); fire("zap", D * 0.3)
    show(fr, text_el("Pregnancy: CVS / amnio. After loss: tissue", 38, "Medium", GREY), 770, t, D * 0.2)
    fire("whoosh", D * 0.55)
    if t > D * 0.55: fr.alpha_composite(plot((t - D * 0.55) / (D * 0.35)), (0, 860))

def c_compare(fr, t, D):
    show(fr, pill("750K vs 315K", LAV, size=56), 230, t, 0.1)
    show(fr, text_el("Number = probes on the chip", 48, color=DBLUE), 360, t, 0.3)
    fire("pop", D * 0.2); show(fr, cmp_table(), 470, t, D * 0.2)
    show(fr, text_el("Screenshot this!", 44, "Bold", TEAL), 1160, t, D * 0.85)

def c_camera(fr, t, D):
    show(fr, pill("THINK OF A CAMERA", ORANGE, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    for i, (lab, sub, cells, col, tin) in enumerate((("750K", "More pixels: every detail sharp", 26, C750, 0.4),
                                                     ("315K", "Fewer pixels: key areas sharp", 13, C315, D * 0.35))):
        if t < tin: continue
        cx = 290 + i * 500
        d.rounded_rectangle((cx - 230, 340, cx + 230, 960), 30, fill=WHITE, outline=col, width=7)
        d.text((cx, 400), lab, font=font("Bold", 60), fill=col, anchor="mm")
        pix_heart(d, cx, 640, 360, cells, col)
        d.text((cx, 880), sub.split(": ")[0], font=font("Bold", 34), fill=DBLUE, anchor="mm")
        d.text((cx, 925), sub.split(": ")[1], font=font("Medium", 30), fill=GREY, anchor="mm")
    fire("pop", 0.4); fire("pop", D * 0.35)
    pop(fr, box_text("Your doctor decides which one", GREEN, 42), 540, 1090, t, D * 0.7, "ding")

def c_who(fr, t, D):
    show(fr, pill("WHO NEEDS IT?", GREEN, size=48), 230, t, 0.1)
    ground(fr, 230, 640, 260); put(fr, MOM, 230, 470, 0.5)
    ground(fr, 540, 640, 220); put(fr, KID["sad"], 540, 490, 0.6)
    ground(fr, 850, 640, 260); put(fr, DOC["idle"], 850, 440, 0.55)
    items = [("Developmental delay / learning issues", PURPLE, "1"), ("Autism", BLUE, "2"), ("Birth defects in many organs", TEAL, "3"),
             ("Baby's scan shows a problem", PINK, "4"), ("Repeated miscarriage / stillbirth", RED, "5")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.1 + 0.15 * i)); show(fr, card(txt, c, m, size=37), 720 + i * 130, t, D * (0.1 + 0.15 * i))

def c_why(fr, t, D):
    show(fr, pill("WHY MICROARRAY?", C750, size=48), 230, t, 0.1)
    show(fr, text_el("Delay / autism: cause found in", 46, color=DBLUE), 360, t, 0.3)
    for i in range(2): fire("pop", 0.6 + i * D * 0.3)
    fr.alpha_composite(bars((t - 0.6) / (D * 0.6)), (0, 460))
    pop(fr, box_text("Often doctors' FIRST genetic test", PURPLE, 42), 540, 1150, t, D * 0.8, "ding")

def c_know(fr, t, D):
    show(fr, pill("GOOD TO KNOW", PURPLE, size=48), 230, t, 0.1)
    put(fr, CHROMO, 540, 500 + 10 * math.sin(t * 3), 0.55)
    items = [("Misses balanced translocation: karyotype", ORANGE, "1"), ("Misses 1-letter changes: exome", RED, "2"),
             ("Parents' samples may be needed", BLUE, "3"), ("Baby's sex NOT disclosed in pregnancy", PINK, "4"),
             ("Understand the report with your doctor", GREEN, "5")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.08 + 0.15 * i)); show(fr, card(txt, c, m, size=35), 740 + i * 130, t, D * (0.08 + 0.15 * i))

def c_close(fr, t, D):
    show(fr, big_logo(), 210, t, 0.2)
    fire("ding", 0.8); show(fr, box_text("Take any medicine only as advised by your doctor", GREEN, 42), 820, t, 0.8)
    show(fr, text_el("Had you heard of microarray before?", 54, color=DBLUE), 1020, t, D * 0.4)
    show(fr, text_el("Share with a family who needs it!", 44, "Medium", GREY), 1180, t, D * 0.5)
    show(fr, pill("Follow Health Test Simplified", BLUE, size=40), 1320, t, D * 0.6)
    show(fr, text_el("For awareness only. Consult your doctor.", 30, "Regular", GREY), 1680, t, D * 0.7)

SC = [(c_hook, "navy"), (c_what, "light"), (c_how, "light"), (c_compare, "light"), (c_camera, "light"),
      (c_who, "light"), (c_why, "light"), (c_know, "light"), (c_close, "light")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        D = [15, 18, 19, 22, 14, 15, 16, 20, 14]; tests = [(0, .9), (1, .95), (2, .95), (3, .95), (4, .95), (5, .95), (6, .95), (7, .95), (8, .9)]
        ims = []
        for si, p in tests:
            fn, bg = SC[si]; d = D[si]; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((360, 640)))
        s = Image.new("RGB", (360 * 5, 640 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 360, (i // 5) * 640))
        s.save("sheet.png")
    else: run(SC, "/tmp/cm_", "Chromosomal_Microarray_750K_315K_Hindi.mp4")
