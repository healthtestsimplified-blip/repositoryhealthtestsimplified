import math, sys
from cbc_cartoon import run
from chromo_cartoon import PINK, SKYB
from gene_cartoon import person
from dmarker_cartoon import MOM, LAV
from wes_cartoon import DAD
from lft_cartoon2 import *
from hts_close import close_scene

DATE = "THURSDAY HEALTH TIPS  •  8 OCT 2026"
HEART = (229, 57, 53); HEART_D = (183, 28, 28)
PAPER = (255, 240, 240); GRID = (248, 190, 190); TRACE = (25, 35, 60)

def beat(t, bpm=72):
    ph = (t * bpm / 60) % 1
    return math.exp(-((ph - 0.05) / 0.06) ** 2)          # 0..1 pulse

def heart(d, cx, cy, s, t=0.0, bpm=72, face="happy"):
    k = 1 + 0.08 * beat(t, bpm); s = s * k
    r = 0.52 * s
    d.ellipse((cx - 1.0 * s, cy - 0.75 * s, cx - 1.0 * s + 2 * r, cy - 0.75 * s + 2 * r), fill=HEART)
    d.ellipse((cx + 1.0 * s - 2 * r, cy - 0.75 * s, cx + 1.0 * s, cy - 0.75 * s + 2 * r), fill=HEART)
    d.polygon([(cx - 0.98 * s, cy - 0.15 * s), (cx + 0.98 * s, cy - 0.15 * s), (cx, cy + 0.95 * s)], fill=HEART)
    d.ellipse((cx - 0.75 * s, cy - 0.6 * s, cx - 0.45 * s, cy - 0.35 * s), fill=(255, 140, 140))   # shine
    ey = cy - 0.05 * s
    for ex in (-0.3, 0.3):
        d.ellipse((cx + ex * s - 0.11 * s, ey - 0.11 * s, cx + ex * s + 0.11 * s, ey + 0.11 * s), fill=WHITE)
        d.ellipse((cx + ex * s - 0.05 * s, ey - 0.05 * s, cx + ex * s + 0.05 * s, ey + 0.05 * s), fill=(30, 30, 40))
    w = max(3, int(s * 0.05))
    if face == "happy": d.arc((cx - 0.2 * s, ey + 0.08 * s, cx + 0.2 * s, ey + 0.36 * s), 20, 160, fill=HEART_D, width=w)
    else: d.arc((cx - 0.17 * s, ey + 0.22 * s, cx + 0.17 * s, ey + 0.4 * s), 200, 340, fill=HEART_D, width=w)

def pqrst(x):
    """one beat shape, x in 0..1 -> height (-0.3 .. 1)"""
    g = lambda m, sd, a: a * math.exp(-((x - m) / sd) ** 2)
    return g(0.18, 0.035, 0.15) - g(0.33, 0.012, 0.12) + g(0.36, 0.014, 1.0) - g(0.39, 0.012, 0.25) + g(0.62, 0.06, 0.28)

def ecg_strip(d, x0, y0, w, h, t, bpm=72, irregular=False, col=TRACE, paper=True, lw=6):
    if paper:
        d.rounded_rectangle((x0, y0, x0 + w, y0 + h), 18, fill=PAPER)
        for gx in range(int(x0) + 20, int(x0 + w), 30): d.line((gx, y0 + 4, gx, y0 + h - 4), fill=GRID, width=2 if (gx - int(x0) - 20) % 150 else 4)
        for gy in range(int(y0) + 15, int(y0 + h), 30): d.line((x0 + 4, gy, x0 + w - 4, gy), fill=GRID, width=2 if (gy - int(y0) - 15) % 150 else 4)
    period = 260 * 72 / bpm; base = y0 + h * 0.62; amp = h * 0.48
    off = t * 220; pts = []
    for px in range(0, int(w) - 20, 3):
        u = px + off
        if irregular: u = u + 60 * math.sin(u / 170)
        y = base - amp * pqrst((u % period) / period)
        pts.append((x0 + 10 + px, y))
    d.line(pts, fill=col, width=lw, joint="curve")

def patient_bed(d, cx, cy, t):
    d.rounded_rectangle((cx - 380, cy + 40, cx + 380, cy + 90), 20, fill=(120, 144, 156))            # bed
    d.rectangle((cx - 360, cy + 90, cx - 330, cy + 190), fill=(96, 125, 139)); d.rectangle((cx + 330, cy + 90, cx + 360, cy + 190), fill=(96, 125, 139))
    d.rounded_rectangle((cx - 380, cy - 10, cx - 250, cy + 45), 20, fill=WHITE)                     # pillow
    d.ellipse((cx - 370, cy - 90, cx - 230, cy + 30), fill=SKIN)                                    # head
    d.pieslice((cx - 375, cy - 95, cx - 225, cy + 20), 180, 290, fill=(50, 30, 30))
    d.ellipse((cx - 285, cy - 45, cx - 265, cy - 25), fill=(30, 30, 40))
    d.arc((cx - 300, cy - 20, cx - 255, cy + 5), 20, 160, fill=(170, 60, 60), width=5)
    d.rounded_rectangle((cx - 240, cy - 50, cx + 120, cy + 45), 40, fill=(0, 150, 170))              # body
    d.rounded_rectangle((cx + 100, cy - 30, cx + 380, cy + 40), 30, fill=(66, 66, 110))               # legs
    pads = [(cx - 160, cy - 30), (cx - 100, cy - 20), (cx - 40, cy - 30), (cx + 20, cy - 25), (cx - 200, cy + 20), (cx + 300, cy + 5)]
    mx, my = cx + 250, cy - 330
    for (px, py) in pads:
        d.line((px, py, mx - 80, my + 80), fill=(90, 90, 110), width=3)
    for (px, py) in pads: d.ellipse((px - 14, py - 14, px + 14, py + 14), fill=WHITE, outline=(120, 130, 150), width=4)
    d.rounded_rectangle((mx - 150, my - 110, mx + 150, my + 110), 22, fill=(55, 71, 79))              # machine
    d.rounded_rectangle((mx - 130, my - 90, mx + 130, my + 40), 12, fill=(15, 30, 40))
    ecg_strip(d, mx - 130, my - 90, 260, 130, t, col=(0, 230, 118), paper=False, lw=4)
    d.ellipse((mx - 110, my + 60, mx - 80, my + 90), fill=(0, 230, 118)); d.rounded_rectangle((mx - 40, my + 62, mx + 120, my + 88), 10, fill=(120, 140, 150))

def no_zap(d, cx, cy, s):
    d.polygon([(cx - 0.2 * s, cy - s), (cx + 0.35 * s, cy - s), (cx + 0.05 * s, cy - 0.1 * s), (cx + 0.35 * s, cy - 0.1 * s),
               (cx - 0.3 * s, cy + s), (cx - 0.05 * s, cy + 0.15 * s), (cx - 0.35 * s, cy + 0.15 * s)], fill=(255, 193, 7))
    d.ellipse((cx - 1.05 * s, cy - 1.05 * s, cx + 1.05 * s, cy + 1.05 * s), outline=RED, width=int(0.14 * s))
    d.line((cx - 0.75 * s, cy - 0.75 * s, cx + 0.75 * s, cy + 0.75 * s), fill=RED, width=int(0.14 * s))

def ambulance(d, cx, cy, t):
    x = cx + 14 * math.sin(t * 3)
    d.rounded_rectangle((x - 200, cy - 110, x + 120, cy + 60), 22, fill=WHITE, outline=(170, 180, 195), width=5)
    d.rounded_rectangle((x + 100, cy - 60, x + 210, cy + 60), 20, fill=WHITE, outline=(170, 180, 195), width=5)
    d.rounded_rectangle((x + 130, cy - 45, x + 195, cy), 8, fill=(144, 202, 249))
    d.rectangle((x - 60 - 15, cy - 75, x - 60 + 15, cy + 15), fill=RED); d.rectangle((x - 60 - 45, cy - 45, x - 60 + 45, cy - 15), fill=RED)
    d.rectangle((x - 200, cy + 20, x + 210, cy + 35), fill=RED)
    for wx in (x - 120, x + 140): d.ellipse((wx - 38, cy + 30, wx + 38, cy + 106), fill=(40, 40, 50)); d.ellipse((wx - 14, cy + 54, wx + 14, cy + 82), fill=(180, 180, 190))
    lit = int(t * 4) % 2
    d.rounded_rectangle((x - 30, cy - 140, x + 30, cy - 110), 10, fill=(33, 150, 243) if lit else RED)

# ---------------- scenes ----------------
def e_hook(fr, t, D):
    rays(fr, 540, 900, t, (255, 90, 90), a=40)
    show(fr, pill(DATE, ORANGE, size=36), 230, t, 0.1)
    pop(fr, white_text("Chest pain? Heart racing? Dizzy or breathless?", 72), 540, 470, t, 0.3, "boom")
    d = ImageDraw.Draw(fr)
    if t > D * 0.3: heart(d, 540, 820, 170, t, bpm=110, face="sad")
    fire("pop", D * 0.3)
    if t > D * 0.4: ecg_strip(d, 90, 1060, 900, 230, t, bpm=90)
    pop(fr, white_text("Doctors often start with an ECG", 62, color=YEL), 540, 1400, t, D * 0.45, "whoosh")
    pop(fr, box_text("ECG test: watch till the end", GREEN, 44), 540, 1570, t, D * 0.7, "pop")

def e_what(fr, t, D):
    show(fr, pill("WHAT IS AN ECG?", RED, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr); heart(d, 270, 520, 150, t)
    if t > 0.5:
        for k in range(3):   # spark from heart
            a = (t * 2 + k) % 1
            d.line((420 + 80 * k, 500 - 30 * math.sin(a * 6), 470 + 80 * k, 470), fill=(255, 193, 7), width=10)
    if t > D * 0.15: ecg_strip(d, 580, 400, 420, 230, t)
    fire("zap", 0.5); fire("pop", D * 0.15)
    show(fr, text_el("Every heartbeat makes a tiny electrical signal", 46, color=DBLUE), 800, t, D * 0.12)
    show(fr, text_el("ECG = Electrocardiogram: records it as waves", 44, "Medium", RED), 930, t, D * 0.3)
    show(fr, card("Painless: takes only a few minutes", GREEN, "1", size=40), 1080, t, D * 0.5)
    show(fr, card("NO current goes into your body", BLUE, "2", size=40), 1215, t, D * 0.66)
    fire("pop", D * 0.5); fire("ding", D * 0.66)
    if t > D * 0.75: no_zap(d, 540, 1450, 95)
    fire("boom", D * 0.75)

def e_why(fr, t, D):
    show(fr, pill("WHEN DO DOCTORS ADVISE IT?", PURPLE, size=44), 230, t, 0.1)
    ground(fr, 260, 690, 260); put(fr, DAD, 260, 500, 0.7)
    d = ImageDraw.Draw(fr); heart(d, 780, 500, 140, t, bpm=120, face="sad"); fire("pop", 0.3)
    items = [("Chest pain or heaviness", RED, "1"), ("Fast or irregular heartbeat", ORANGE, "2"), ("Dizziness or fainting", PURPLE, "3"),
             ("Breathlessness", BLUE, "4"), ("Suspected heart attack", HEART_D, "5")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.12 + 0.14 * i)); show(fr, card(txt, c, m, size=40), 790 + i * 135, t, D * (0.12 + 0.14 * i))

def e_shows(fr, t, D):
    show(fr, pill("WHAT DOES IT SHOW?", BLUE, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr); ecg_strip(d, 90, 360, 900, 290, t); fire("whoosh", 0.3)
    items = [("Heart RATE: how fast it beats", RED, "1"), ("Heart RHYTHM: regular or not", ORANGE, "2"),
             ("Signs of heart attack or damage", PURPLE, "3"), ("Effect of pacemaker or some medicines", BLUE, "4")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.1 + 0.17 * i)); show(fr, card(txt, c, m, size=38), 780 + i * 150, t, D * (0.1 + 0.17 * i))

def e_who(fr, t, D):
    show(fr, pill("WHY INDIA MUST KNOW", ORANGE, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    for k in range(3):
        if t < 0.3 + k * 0.2: break
        person(d, 340 + k * 200, 520, RED if k == 2 else (190, 200, 215), 1.5)
    fire("pop", 0.3)
    pop(fr, stroke_text("Nearly 1 in 3", 120, RED, WHITE, 10), 540, 720, t, D * 0.12, "boom")
    show(fr, text_el("deaths in India are due to heart & blood vessel diseases", 42, color=DBLUE), 850, t, D * 0.17)
    show(fr, text_el("Doctors may also advise ECG:", 42, "Bold", GREEN), 990, t, D * 0.35)
    items = [("Before an operation", BLUE, "1"), ("Past heart problem", PURPLE, "2"),
             ("Strong family history of heart disease", RED, "3"), ("Have a pacemaker", TEAL, "4")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.42 + 0.12 * i)); show(fr, card(txt, c, m, size=38), 1100 + i * 125, t, D * (0.42 + 0.12 * i))
    show(fr, text_el("Source: Sample Registration System, 2021-23", 28, "Medium", GREY), 1620, t, D * 0.5)

def e_prep(fr, t, D):
    show(fr, pill("HOW TO PREPARE", TEAL, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr); patient_bed(d, 560, 770, t); fire("pop", 0.3)
    items = [("Wear a top that opens easily", BLUE, "1"), ("No cream, oil or powder on chest", RED, "2"),
             ("No exercise or cold water just before", ORANGE, "3"), ("Tell about your medicines", PURPLE, "4"),
             ("Lie still & relax: only a few minutes", GREEN, "5")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.1 + 0.15 * i)); show(fr, card(txt, c, m, size=38), 1030 + i * 125, t, D * (0.1 + 0.15 * i))

def e_read(fr, t, D):
    show(fr, pill("READING THE REPORT", GREEN, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr); heart(d, 200, 470, 110, t); fire("pop", 0.3)
    if t > 0.4:
        d.rounded_rectangle((360, 350, 1000, 590), 30, fill=WHITE, outline=GREEN, width=7)
        d.text((680, 420), "Resting heart rate", font=font("Medium", 36), fill=GREY, anchor="mm")
        d.text((680, 500), "about 60 - 100 / min", font=font("Bold", 52), fill=GREEN, anchor="mm")
        d.text((680, 560), "and a regular rhythm", font=font("Medium", 30), fill=GREY, anchor="mm")
    show(fr, text_el("ECG records only a few seconds", 44, color=DBLUE), 680, t, D * 0.25)
    pop(fr, box_text("A normal ECG does not rule out every heart problem", RED, 40), 540, 830, t, D * 0.35, "boom")
    show(fr, text_el("If needed, your doctor may advise:", 40, "Medium", GREY), 990, t, D * 0.5)
    items = [("Holter: 24-48 hour ECG", PURPLE, "1"), ("TMT: treadmill stress test", ORANGE, "2"), ("ECHO: heart ultrasound", TEAL, "3")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.55 + 0.08 * i)); show(fr, card(txt, c, m, size=38), 1100 + i * 128, t, D * (0.55 + 0.08 * i))
    show(fr, text_el("Your doctor reads the ECG with your symptoms", 38, "Bold", BLUE), 1520, t, D * 0.8)

def e_alert(fr, t, D):
    show(fr, pill("HEART ATTACK WARNING SIGNS", RED, size=44), 230, t, 0.1)
    ground(fr, 260, 690, 260); put(fr, DAD, 260, 500, 0.7)
    d = ImageDraw.Draw(fr); ambulance(d, 760, 500, t) if t > D * 0.7 else heart(d, 780, 500, 140, t, bpm=130, face="sad")
    items = [("Chest pain or pressure", RED, "1"), ("Spreading to arm, jaw or back", ORANGE, "2"),
             ("Sweating, breathlessness, uneasiness", PURPLE, "3")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.08 + 0.1 * i)); show(fr, card(txt, c, m, size=38), 780 + i * 130, t, D * (0.08 + 0.1 * i))
    show(fr, card("Women, elderly & diabetics may have NO chest pain", PINK, "!", size=36), 1200, t, D * 0.45)
    fire("ding", D * 0.45)
    pop(fr, box_text("Don't wait! Call an ambulance or go to the nearest hospital NOW", RED, 42), 540, 1440, t, D * 0.7, "boom")

SC = [(e_hook, "navy"), (e_what, "light"), (e_why, "light"), (e_shows, "light"), (e_who, "light"),
      (e_prep, "light"), (e_read, "light"), (e_alert, "light"), (close_scene("Have you ever had an ECG?", DATE), "light")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        try:
            import json; D = [round(v + 1.3, 2) for v in json.load(open("/tmp/ecg_durs.json"))]
        except Exception: D = [12, 16, 13, 16, 18, 18, 22, 20, 30]
        tests = [(0, .9), (1, .95), (2, .95), (3, .95), (4, .95), (5, .95), (6, .95), (7, .95), (8, .9)]
        ims = []
        for si, p in tests:
            fn, bg = SC[si]; d = D[si]; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((360, 640)))
        s = Image.new("RGB", (360 * 5, 640 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 360, (i // 5) * 640))
        s.save("sheet.png")
    else: run(SC, "/tmp/ecg_", "Thursday_Health_Tips_8Oct2026_ECG_Hindi.mp4")
