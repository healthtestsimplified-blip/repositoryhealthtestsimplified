import math, sys
from cbc_cartoon import run, BD, bacteria_sprite
from chromo_cartoon import PINK
from alz_cartoon import tube
from lft_cartoon2 import *
from hts_close import close_scene

DATE = "SUNDAY HEALTH TIPS  •  11 OCT 2026"
BLOOD = (200, 30, 45); PLASMA = (255, 236, 160)
BACT = bacteria_sprite()

def smoke_alarm(d, cx, cy, t, on=True):
    d.ellipse((cx - 150, cy - 150, cx + 150, cy + 150), fill=WHITE, outline=(170, 180, 195), width=8)
    d.ellipse((cx - 105, cy - 105, cx + 105, cy + 105), outline=(210, 215, 225), width=6)
    for k in range(6):
        a = k * math.pi / 3
        d.ellipse((cx + 60 * math.cos(a) - 9, cy + 60 * math.sin(a) - 9, cx + 60 * math.cos(a) + 9, cy + 60 * math.sin(a) + 9), fill=(190, 198, 210))
    blink = on and math.sin(t * 9) > 0
    d.ellipse((cx - 28, cy - 28, cx + 28, cy + 28), fill=(255, 40, 40) if blink else (120, 30, 30))
    if blink:
        for q in range(3):
            r = 175 + q * 30
            d.arc((cx - r, cy - r, cx + r, cy + r), 200, 250, fill=RED, width=8)
            d.arc((cx - r, cy - r, cx + r, cy + r), 290, 340, fill=RED, width=8)

def flame(d, cx, cy, s, t):
    k = 1 + 0.08 * math.sin(t * 10)
    d.polygon([(cx, cy - 120 * s * k), (cx + 60 * s, cy - 20 * s), (cx + 50 * s, cy + 40 * s), (cx - 50 * s, cy + 40 * s), (cx - 60 * s, cy - 20 * s)], fill=(255, 120, 30))
    d.polygon([(cx, cy - 60 * s * k), (cx + 30 * s, cy + 0), (cx + 25 * s, cy + 35 * s), (cx - 25 * s, cy + 35 * s), (cx - 30 * s, cy + 0)], fill=(255, 220, 60))

def esr_tube(d, cx, top, h, clear, label, col):
    """Westergren-style tall tube; `clear` = height (px) of clear plasma at top."""
    d.rounded_rectangle((cx - 42, top - 20, cx + 42, top + h + 20), 30, fill=WHITE, outline=(150, 160, 175), width=6)
    d.rectangle((cx - 30, top, cx + 30, top + clear), fill=PLASMA)
    d.rounded_rectangle((cx - 30, top + clear, cx + 30, top + h), 20, fill=BLOOD)
    for k in range(0, h + 1, 40):
        d.line((cx + 44, top + k, cx + 62, top + k), fill=GREY, width=3)
    d.line((cx - 70, top, cx - 70, top + clear), fill=col, width=6)
    if clear > 30:
        d.polygon([(cx - 82, top + clear - 22), (cx - 58, top + clear - 22), (cx - 70, top + clear)], fill=col)
    d.text((cx, top + h + 70), label, font=font("Bold", 38), fill=col, anchor="mm")

def clock(d, cx, cy, r, t):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=WHITE, outline=DBLUE, width=7)
    a = -math.pi / 2 + t * 1.2
    d.line((cx, cy, cx + r * 0.75 * math.cos(a), cy + r * 0.75 * math.sin(a)), fill=RED, width=7)
    d.line((cx, cy, cx, cy - r * 0.5), fill=DBLUE, width=8)
    d.text((cx, cy + r + 40), "1 hour", font=font("Bold", 36), fill=DBLUE, anchor="mm")

def graph(d, t, D, x0=110, y0=380, w=860, h=430):
    d.rounded_rectangle((x0 - 30, y0 - 30, x0 + w + 30, y0 + h + 90), 30, fill=WHITE, outline=(200, 210, 225), width=4)
    d.line((x0, y0 + h, x0 + w, y0 + h), fill=GREY, width=5); d.line((x0, y0, x0, y0 + h), fill=GREY, width=5)
    d.text((x0 + w / 2, y0 + h + 45), "Days  ›", font=font("Medium", 32), fill=GREY, anchor="mm")
    prog = max(0, min(1, (t - D * 0.12) / (D * 0.5)))
    def crp(x): return math.exp(-((x - 0.17) / 0.09) ** 2) if x < 0.17 else math.exp(-((x - 0.17) / 0.18) ** 2)
    def esr(x): return 0.75 / (1 + math.exp(-(x - 0.3) * 18)) * (1 if x < 0.55 else math.exp(-(x - 0.55) * 2.2))
    for fn, col in ((esr, ORANGE), (crp, RED)):
        pts = [(x0 + w * i / 100, y0 + h - (h - 30) * fn(i / 100)) for i in range(int(100 * prog) + 1)]
        if len(pts) > 1: d.line(pts, fill=col, width=10, joint="curve")
    if prog > 0.3:
        d.text((x0 + w * 0.17 + 20, y0 + 10), "CRP: fast", font=font("Bold", 36), fill=RED, anchor="lm")
    if prog > 0.8:
        d.text((x0 + w * 0.62, y0 + h - (h - 30) * 0.75 - 30), "ESR: slow", font=font("Bold", 36), fill=ORANGE, anchor="mm")

# ---------------- scenes ----------------
def s_hook(fr, t, D):
    rays(fr, 540, 1250, t, (255, 120, 80), a=40)
    show(fr, pill(DATE, ORANGE, size=36), 230, t, 0.1)
    put(fr, BD["sick"], 540, 1330, 0.9 + 0.03 * math.sin(t * 5))
    if t > D * 0.35: NOW["shake"] = 4 if t < D * 0.42 else 0
    pop(fr, white_text("Fever that won't go? Joint pain & stiffness?", 62), 540, 450, t, 0.3, "boom")
    pop(fr, white_text("Doctor wrote ESR & CRP?", 72, color=YEL), 540, 690, t, D * 0.4, "whoosh")
    pop(fr, box_text("What these 2 tests tell: watch till the end", GREEN, 42), 540, 880, t, D * 0.62, "pop")

def s_what(fr, t, D):
    show(fr, pill("INFLAMMATION = BODY'S ALARM", BLUE, size=44), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    if t > 0.3:
        flame(d, 250, 600, 2.2, t); put(fr, BACT, 390, 690, 0.5)
    if t > D * 0.3:
        fire("ding", D * 0.3); d = ImageDraw.Draw(fr); smoke_alarm(d, 780, 520, t)
        d.text((780, 720), "ESR & CRP", font=font("Bold", 44), fill=RED, anchor="mm")
    show(fr, card("Inflammation: the body's response to infection, injury or disease", ORANGE, "1", size=34), 820, t, D * 0.12)
    show(fr, card("ESR & CRP work like smoke alarms", RED, "2", size=38), 975, t, D * 0.32)
    show(fr, card("They say inflammation is there, not WHERE or WHY", PURPLE, "3", size=36), 1110, t, D * 0.6)
    for k in (0.12, 0.32, 0.6): fire("pop", D * k)

def s_esr(fr, t, D):
    show(fr, pill("ESR: THE SETTLING TEST", ORANGE, size=46), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    k = max(0, min(1, (t - 0.5) / (D * 0.55)))
    esr_tube(d, 300, 360, 400, int(45 * k), "Usual", GREEN)
    esr_tube(d, 560, 360, 400, int(170 * k), "High ESR", RED)
    clock(d, 850, 520, 95, t)
    show(fr, text_el("Erythrocyte Sedimentation Rate", 44, color=DBLUE), 900, t, D * 0.1)
    show(fr, card("Blood stands in a tall thin tube", BLUE, "1", size=38), 990, t, D * 0.2)
    show(fr, card("How many mm red cells settle in 1 hour (mm/hr)", ORANGE, "2", size=36), 1135, t, D * 0.4)
    show(fr, card("Inflammation: cells usually settle faster = higher ESR", RED, "3", size=34), 1290, t, D * 0.65)
    for q in (0.2, 0.4, 0.65): fire("pop", D * q)

def s_crp(fr, t, D):
    show(fr, pill("CRP: MADE BY THE LIVER", RED, size=46), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    put(fr, LV["happy"], 250, 410, 0.42)
    d.text((250, 520), "Liver", font=font("Bold", 34), fill=(150, 40, 40), anchor="mm")
    for i in range(5):
        x = 400 + ((t * 120 + i * 110) % 560); y = 410 + 25 * math.sin(t * 3 + i)
        d.ellipse((x - 18, y - 18, x + 18, y + 18), fill=RED); d.text((x, y), "C", font=font("Bold", 22), fill=WHITE, anchor="mm")
    d.text((680, 500), "C-Reactive Protein", font=font("Bold", 36), fill=RED, anchor="mm")
    graph(d, t, D, y0=600, h=330)
    show(fr, card("CRP: rises within hours, falls quickly when better", RED, "1", size=34), 1130, t, D * 0.3)
    show(fr, card("ESR: rises in 1–2 days, may take weeks to settle", ORANGE, "2", size=34), 1265, t, D * 0.62)
    fire("pop", D * 0.3); fire("pop", D * 0.62)

def s_who(fr, t, D):
    show(fr, pill("WHEN DO DOCTORS ORDER IT?", GREEN, size=44), 230, t, 0.1)
    ground(fr, 540, 640, 300); put(fr, DOC["idle"], 540, 470, 0.6)
    items = [("Long, unexplained fever", RED, "1"), ("Joint pain, swelling or stiffness", ORANGE, "2"), ("Muscle pain", BLUE, "3"),
             ("Suspected infection", PURPLE, "4"), ("Arthritis & similar: is treatment working?", TEAL, "5")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.1 + 0.13 * i)); show(fr, card(txt, c, m, size=36), 720 + i * 128, t, D * (0.1 + 0.13 * i))
    show(fr, text_el("Or when your doctor advises", 38, "Medium", GREY), 1380, t, D * 0.8)

def s_prep(fr, t, D):
    show(fr, pill("HOW IS IT DONE?", BLUE, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr); tube(d, 330, 500)
    d.text((330, 650), "Blood test", font=font("Bold", 38), fill=RED, anchor="mm")
    d.rounded_rectangle((620, 410, 880, 590), 24, fill=(255, 235, 238), outline=RED, width=6)
    d.text((750, 480), "hs-CRP", font=font("Bold", 50), fill=RED, anchor="mm")
    d.text((750, 540), "high sensitivity", font=font("Medium", 28), fill=GREY, anchor="mm")
    fire("pop", 0.3)
    show(fr, card("Usually no fasting needed: follow your lab", BLUE, "1", size=36), 760, t, D * 0.12)
    show(fr, card("Tell your doctor about medicines you take", GREEN, "2", size=36), 895, t, D * 0.3)
    show(fr, card("hs-CRP picks up very small amounts of CRP", RED, "3", size=36), 1030, t, D * 0.5)
    show(fr, card("Sometimes used to estimate heart disease risk", PURPLE, "4", size=36), 1165, t, D * 0.7)
    for k in (0.12, 0.3, 0.5, 0.7): fire("pop", D * k)

def row(d, y, cells, cols, fill, bold=False):
    xs = [90, 520, 990]
    d.rectangle((xs[0], y, xs[-1], y + 80), fill=fill)
    for i, c in enumerate(cells):
        d.text(((xs[i] + xs[i + 1]) / 2, y + 40), c, font=font("Bold" if bold else "Medium", 34), fill=cols[i], anchor="mm")

def s_read(fr, t, D):
    show(fr, pill("READING THE REPORT", PURPLE, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    if t > 0.3:
        d.text((540, 395), "ESR (approximately, mm/hr)", font=font("Bold", 40), fill=ORANGE, anchor="mm")
        row(d, 445, ["", "Up to"], [WHITE, WHITE], ORANGE, True)
        row(d, 525, ["Men under 50", "~15"], [DBLUE, DBLUE], WHITE)
        row(d, 605, ["Women under 50", "~20"], [DBLUE, DBLUE], (255, 243, 224))
        row(d, 685, ["Over 50", "a little higher"], [DBLUE, DBLUE], WHITE)
        d.rectangle((90, 445, 990, 765), outline=ORANGE, width=4)
    show(fr, card("CRP: very low in most healthy people", RED, "1", size=38), 840, t, D * 0.45)
    show(fr, card("Units differ: mg/L or mg/dL (10 mg/L = 1 mg/dL)", BLUE, "2", size=34), 985, t, D * 0.58)
    fire("pop", D * 0.45); fire("pop", D * 0.58)
    pop(fr, box_text("Ranges vary by lab: always check the range printed on your report", TEAL, 38), 540, 1260, t, D * 0.75, "ding")

def s_know(fr, t, D):
    show(fr, pill("GOOD TO KNOW", TEAL, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    show(fr, card("ESR can be higher: older age, women, pregnancy, anaemia", ORANGE, "1", size=33), 340, t, 0.3)
    show(fr, card("CRP can rise mildly: obesity, smoking", RED, "2", size=38), 475, t, D * 0.18)
    fire("pop", 0.3); fire("pop", D * 0.18)
    if t > D * 0.32:
        fire("whoosh", D * 0.32)
        d.text((540, 620), "MYTH BUSTER", font=font("Bold", 50), fill=ORANGE, anchor="mm")
        d.rounded_rectangle((70, 670, 1010, 830), 28, fill=(255, 235, 238), outline=RED, width=5)
        d.text((560, 725), "Myth: High ESR = surely", font=font("Bold", 38), fill=RED, anchor="mm")
        d.text((560, 780), "TB or cancer", font=font("Bold", 38), fill=RED, anchor="mm")
        d.line((120, 710, 180, 790), fill=RED, width=12); d.line((120, 790, 180, 710), fill=RED, width=12)
    show(fr, card("Truth: many common causes. Doctor checks symptoms & other tests", GREEN, "✓", size=33), 870, t, D * 0.5)
    fire("ding", D * 0.5)
    pop(fr, box_text("A normal report doesn't rule out every disease", PURPLE, 38), 540, 1110, t, D * 0.78, "pop")

SC = [(s_hook, "navy"), (s_what, "light"), (s_esr, "light"), (s_crp, "light"), (s_who, "light"),
      (s_prep, "light"), (s_read, "light"), (s_know, "light"), (close_scene("Ever had an ESR or CRP test?", DATE), "light")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        D = [13, 15, 16, 15, 16, 18, 19, 20, 30]; tests = [(i, .95) for i in range(9)]
        ims = []
        for si, p in tests:
            fn, bg = SC[si]; d = D[si]; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((360, 640)))
        s = Image.new("RGB", (360 * 5, 640 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 360, (i // 5) * 640))
        s.save("sheet.png")
    else: run(SC, "/tmp/esc_", "Sunday_Health_Tips_11Oct2026_ESR_CRP_Hindi.mp4")
