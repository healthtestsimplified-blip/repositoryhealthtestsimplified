import math, sys
from cbc_cartoon import run
from chromo_cartoon import PINK, SKYB
from gene_cartoon import person
from dmarker_cartoon import MOM, LAV
from wes_cartoon import DAD
from alz_cartoon import tube
from lft_cartoon2 import *
from hts_close import close_scene

TOPIC = "WOMEN'S HEALTH  •  FERTILITY"
OVARY = (248, 187, 208); OV_D = (236, 64, 122); EGG = (255, 236, 179)

def ovary(d, cx, cy, s, n=14, t=0.0):
    d.ellipse((cx - s, cy - 0.65 * s, cx + s, cy + 0.65 * s), fill=OVARY, outline=OV_D, width=max(4, int(s * 0.04)))
    pts = [(-0.55, -0.2), (-0.2, -0.35), (0.2, -0.3), (0.55, -0.15), (-0.6, 0.15), (-0.25, 0.1), (0.1, 0.05), (0.45, 0.2),
           (-0.4, 0.38), (0.0, 0.35), (0.3, -0.05), (-0.05, -0.12), (0.65, 0.05), (-0.75, -0.02)]
    for k, (x, y) in enumerate(pts[:n]):
        r = s * (0.09 + 0.02 * math.sin(t * 2 + k))
        X, Y = cx + x * s, cy + y * s
        d.ellipse((X - r, Y - r, X + r, Y + r), fill=EGG, outline=(240, 180, 60), width=3)
        d.ellipse((X - r * 0.35, Y - r * 0.35, X + r * 0.35, Y + r * 0.35), fill=(255, 193, 7))

def piggy(d, cx, cy, s):
    d.ellipse((cx - s, cy - 0.7 * s, cx + s, cy + 0.7 * s), fill=PINK)
    d.ellipse((cx + 0.7 * s, cy - 0.2 * s, cx + 1.15 * s, cy + 0.2 * s), fill=(244, 143, 177))
    d.rounded_rectangle((cx - 0.3 * s, cy - 0.85 * s, cx + 0.3 * s, cy - 0.72 * s), 6, fill=GREY)
    for lx in (-0.5, 0.4): d.rounded_rectangle((cx + lx * s, cy + 0.55 * s, cx + (lx + 0.2) * s, cy + 0.95 * s), 8, fill=PINK)
    d.ellipse((cx + 0.35 * s, cy - 0.3 * s, cx + 0.48 * s, cy - 0.17 * s), fill=(30, 30, 40))

def age_bars(d, p):
    data = [("20s", 1.0), ("30–34", 0.8), ("35–39", 0.5), ("40+", 0.25)]
    base = 1000
    for i, (lab, v) in enumerate(data):
        if p < i / 4: break
        x = 210 + i * 220; h = 420 * v * ease(min(1, (p - i / 4) * 4))
        d.rounded_rectangle((x - 70, base - h, x + 70, base), 18, fill=blend(OV_D, (255, 255, 255), 0.15 * i))
        d.text((x, base + 45), lab, font=font("Bold", 38), fill=DBLUE, anchor="mm")
    d.line((110, base, 970, base), fill=(190, 200, 215), width=4)
    d.text((540, base + 105), "Age (years)", font=font("Medium", 32), fill=GREY, anchor="mm")

# ---------------- scenes ----------------
def h_hook(fr, t, D):
    rays(fr, 540, 900, t, (255, 140, 190), a=40)
    show(fr, pill(TOPIC, PINK, size=36), 230, t, 0.1)
    d = ImageDraw.Draw(fr); ovary(d, 540, 1230, 230, 14, t)
    pop(fr, white_text("Planning a baby?", 76), 540, 470, t, 0.3, "pop")
    pop(fr, white_text("Told to do an AMH test?", 70, color=YEL), 540, 640, t, D * 0.3, "boom")
    pop(fr, box_text("Don't panic! Watch till the end", GREEN, 44), 540, 840, t, D * 0.6, "whoosh")

def h_what(fr, t, D):
    show(fr, pill("WHAT IS AMH?", PINK, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr); ovary(d, 330, 520, 200, 12, t); piggy(d, 830, 540, 140); fire("pop", 0.3)
    d.text((330, 700), "Ovary", font=font("Bold", 38), fill=OV_D, anchor="mm")
    d.text((830, 700), "Egg 'bank balance'", font=font("Bold", 36), fill=PINK, anchor="mm")
    show(fr, text_el("Anti-Müllerian Hormone", 52, color=DBLUE), 800, t, D * 0.15)
    show(fr, card("Made by small egg sacs in the ovaries", PINK, "1", size=38), 920, t, D * 0.3)
    show(fr, card("Shows roughly how many eggs are left", ORANGE, "2", size=38), 1055, t, D * 0.5)
    fire("pop", D * 0.3); fire("pop", D * 0.5)
    pop(fr, box_text("This is called OVARIAN RESERVE", PURPLE, 42), 540, 1240, t, D * 0.7, "ding")

def h_age(fr, t, D):
    show(fr, pill("AMH FALLS WITH AGE", ORANGE, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr); p = (t - 0.4) / (D * 0.5)
    for i in range(4): fire("pop", 0.4 + i / 4 * D * 0.5)
    show(fr, text_el("Number of eggs left (simple picture)", 40, "Medium", GREY), 420, t, 0.3)
    age_bars(d, p)
    pop(fr, box_text("Faster drop after 35", RED, 44), 540, 1260, t, D * 0.75, "boom")

def h_myth(fr, t, D):
    show(fr, pill("BIGGEST MYTH", RED, size=50), 230, t, 0.1)
    show(fr, text_el("MYTH: Low AMH = can't get pregnant", 48, color=RED), 420, t, 0.3); fire("boom", 0.3)
    pop(fr, stroke_text("NO!", 140, GREEN, WHITE, 10), 540, 600, t, D * 0.2, "pop")
    show(fr, card("AMH = egg COUNT, not QUALITY", BLUE, "1", size=40), 760, t, D * 0.35)
    show(fr, card("Big study, women 30–44 (JAMA 2017):", PURPLE, "2", size=38), 895, t, D * 0.55)
    show(fr, text_el("low AMH did not lower natural pregnancy chances", 40, "Medium", DBLUE), 1010, t, D * 0.6)
    fire("pop", D * 0.35); fire("pop", D * 0.55)
    d = ImageDraw.Draw(fr)
    if t > D * 0.75: put(fr, MOM, 540, 1350, 0.6); sparkles(fr, 540, 1300, 200, t, 6)
    fire("ding", D * 0.75)

def h_when(fr, t, D):
    show(fr, pill("WHEN IS IT USEFUL?", BLUE, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr); ovary(d, 300, 480, 150, 10, t); tube(d, 800, 470); fire("pop", 0.3)
    items = [("IVF planning: response to medicines", PURPLE, "1"), ("PCOS: AMH is often high", PINK, "2"),
             ("Egg freezing / planning baby later", ORANGE, "3"), ("After ovary surgery or chemotherapy", TEAL, "4")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.12 + 0.16 * i)); show(fr, card(txt, c, m, size=37), 720 + i * 132, t, D * (0.12 + 0.16 * i))
    show(fr, text_el("Always as your doctor advises", 42, "Medium", GREEN), 1290, t, D * 0.8)

def h_test(fr, t, D):
    show(fr, pill("THE TEST", GREEN, size=50), 230, t, 0.1)
    d = ImageDraw.Draw(fr); tube(d, 540, 480); fire("pop", 0.3)
    show(fr, card("Just one blood sample", RED, "1", size=42), 700, t, D * 0.15)
    show(fr, card("Any day of your period cycle", PINK, "2", size=42), 835, t, D * 0.3)
    show(fr, card("On birth control pills? Tell your doctor", ORANGE, "3", size=38), 970, t, D * 0.5)
    fire("pop", D * 0.15); fire("pop", D * 0.3); fire("pop", D * 0.5)
    show(fr, text_el("Pills can make AMH read lower", 40, "Medium", GREY), 1110, t, D * 0.65)

def h_report(fr, t, D):
    show(fr, pill("READING THE REPORT", ORANGE, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    rows = [("LOW", "Fewer eggs left: see a fertility doctor", ORANGE), ("NORMAL FOR AGE", "Reassuring", GREEN), ("HIGH", "Sometimes a sign of PCOS", PURPLE)]
    for i, (a, b, c) in enumerate(rows):
        tin = 0.4 + i * D * 0.2; fire("pop", tin)
        if t < tin: continue
        y = 370 + i * 230
        d.rounded_rectangle((70, y, W - 70, y + 200), 30, fill=WHITE, outline=c, width=8)
        d.text((W / 2, y + 66), a, font=font("Bold", 52), fill=c, anchor="mm")
        d.text((W / 2, y + 142), b, font=font("Medium", 34), fill=GREY, anchor="mm")
    pop(fr, box_text("Normal range depends on AGE and the LAB", BLUE, 40), 540, 1160, t, D * 0.75, "ding")

def h_know(fr, t, D):
    show(fr, pill("GOOD TO KNOW", PURPLE, size=48), 230, t, 0.1)
    ground(fr, 330, 720, 280); put(fr, MOM, 330, 540, 0.55)
    ground(fr, 750, 720, 260); put(fr, DAD, 750, 560, 0.75); d = ImageDraw.Draw(fr)
    d.text((540, 520), "+", font=font("Bold", 100), fill=GREY, anchor="mm")
    items = [("AMH alone doesn't decide anything", RED, "1"), ("Doctor also checks age & ultrasound", BLUE, "2"),
             ("Both partners matter: semen test for men", TEAL, "3")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.15 + 0.2 * i)); show(fr, card(txt, c, m, size=36), 820 + i * 135, t, D * (0.15 + 0.2 * i))

SC = [(h_hook, "purple"), (h_what, "light"), (h_age, "light"), (h_myth, "light"), (h_when, "light"),
      (h_test, "light"), (h_report, "light"), (h_know, "light"),
      (close_scene("Had you heard of the AMH test?", TOPIC), "light")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        D = [12, 16, 11, 19, 20, 14, 19, 16, 30]; tests = [(0, .9), (1, .95), (2, .95), (3, .95), (4, .95), (5, .95), (6, .95), (7, .95), (8, .9)]
        ims = []
        for si, p in tests:
            fn, bg = SC[si]; d = D[si]; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((360, 640)))
        s = Image.new("RGB", (360 * 5, 640 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 360, (i // 5) * 640))
        s.save("sheet.png")
    else: run(SC, "/tmp/amh_", "AMH_Test_Hindi.mp4")
