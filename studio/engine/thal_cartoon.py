import math, sys
from cbc_cartoon import run
from chromo_cartoon import PINK, SKYB
from gene_cartoon import punnett, person
from dmarker_cartoon import MOM
from lft_cartoon2 import *

DATE = "TUESDAY HEALTH TIPS  •  6 OCT 2026"

def rbc(d, cx, cy, r, col, inner, face=None):
    d.ellipse((cx - r, cy - r * 0.8, cx + r, cy + r * 0.8), fill=col)
    d.ellipse((cx - r * 0.5, cy - r * 0.35, cx + r * 0.5, cy + r * 0.35), fill=inner)
    if face:
        for ex in (-0.3, 0.3):
            d.ellipse((cx + ex * r - r * 0.12, cy - r * 0.45, cx + ex * r + r * 0.12, cy - r * 0.2), fill=WHITE)
            d.ellipse((cx + ex * r - r * 0.05, cy - r * 0.38, cx + ex * r + r * 0.06, cy - r * 0.26), fill=(30, 30, 40))
        if face == "happy": d.arc((cx - r * 0.25, cy + r * 0.05, cx + r * 0.25, cy + r * 0.45), 20, 160, fill=WHITE, width=max(3, int(r * 0.07)))
        else: d.arc((cx - r * 0.2, cy + r * 0.25, cx + r * 0.2, cy + r * 0.5), 200, 340, fill=(90, 40, 40), width=max(3, int(r * 0.07)))

# ---------------- scenes ----------------
def t_hook(fr, t, D):
    rays(fr, 540, 900, t, (255, 90, 110), a=40)
    show(fr, pill(DATE, ORANGE, size=38), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    for k in range(5): rbc(d, 160 + k * 190, 1450 + 25 * math.sin(t * 2 + k), 70, (120, 30, 40), (80, 20, 30))
    pop(fr, white_text("ONE blood test before marriage", 80), 540, 560, t, 0.3, "boom")
    pop(fr, white_text("can protect your future child!", 66, color=YEL), 540, 820, t, 1.8, "whoosh")
    pop(fr, box_text("Thalassaemia: watch till the end", GREEN, 44), 540, 1060, t, D * 0.55, "pop")

def t_what(fr, t, D):
    show(fr, pill("WHAT IS THALASSAEMIA?", RED, size=46), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    if t > 0.4:
        rbc(d, 290, 520, 150, (210, 30, 45), (170, 15, 30), "happy"); d.text((290, 700), "Normal red cell", font=font("Bold", 36), fill=RED, anchor="mm")
    if t > D * 0.25:
        rbc(d, 790, 530, 100, (240, 150, 160), (250, 205, 210), "sad"); d.text((790, 700), "Thalassaemia cell", font=font("Bold", 36), fill=(200, 100, 110), anchor="mm")
        d.text((790, 745), "small & pale", font=font("Medium", 32), fill=GREY, anchor="mm")
    fire("pop", 0.4); fire("pop", D * 0.25)
    show(fr, text_el("An inherited blood disorder", 54, color=DBLUE), 830, t, D * 0.4)
    show(fr, card("Body makes less haemoglobin", RED, "1", size=42), 950, t, D * 0.55)
    show(fr, card("Less oxygen reaches the body", ORANGE, "2", size=42), 1080, t, D * 0.7)
    fire("pop", D * 0.55); fire("pop", D * 0.7)

def t_types(fr, t, D):
    show(fr, pill("CARRIER vs MAJOR", PURPLE, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    for (x0, col, title, sub, lines, tin) in [(60, ORANGE, "CARRIER", "(Thalassaemia minor / trait)", ["Usually healthy", "Mild anaemia at most", "Often doesn't know!"], 0.4),
                                             (560, RED, "MAJOR", "(Serious disease)", ["Severe anaemia from", "early childhood", "Blood transfusion", "every 2–4 weeks, for life"], D * 0.4)]:
        if t < tin: continue
        d.rounded_rectangle((x0, 360, x0 + 460, 1000), 34, fill=WHITE, outline=col, width=8)
        d.rounded_rectangle((x0 + 30, 390, x0 + 430, 500), 24, fill=col)
        d.text((x0 + 230, 445), title, font=font("Bold", 52), fill=WHITE, anchor="mm")
        d.text((x0 + 230, 550), sub, font=font("Medium", 26), fill=GREY, anchor="mm")
        person(d, x0 + 230, 680, col, 0.9)
        for j, l in enumerate(lines): d.text((x0 + 230, 800 + j * 46), l, font=font("Bold", 30), fill=DBLUE, anchor="mm")
    fire("pop", 0.4); fire("boom", D * 0.4)
    show(fr, text_el("A carrier is NOT a patient", 52, color=GREEN), 1060, t, D * 0.75)

def t_inherit(fr, t, D):
    show(fr, pill("WHEN BOTH PARENTS ARE CARRIERS", RED, size=42), 230, t, 0.1)
    p = (t - 0.4) / (D * 0.65)
    for i in range(4): fire("pop", 0.4 + (i + 1) / 5 * D * 0.65)
    fr.alpha_composite(punnett(p), (0, 340))
    show(fr, box_text("One carrier parent alone: no major in the child", GREEN, 40), 1120, t, D * 0.82)

def t_india(fr, t, D):
    show(fr, pill("WHY INDIA MUST KNOW", ORANGE, size=48), 230, t, 0.1)
    pop(fr, stroke_text("10,000+", 150, RED, WHITE, 10), 540, 470, t, 0.4, "boom")
    show(fr, text_el("babies born with thalassaemia major in India every year", 44, color=DBLUE), 580, t, 0.9)
    show(fr, card("Carriers are more common in Bengal & Eastern India", ORANGE, "!", size=40), 800, t, D * 0.4)
    show(fr, card("Most carriers don't know their status", PURPLE, "?", size=40), 950, t, D * 0.6)
    fire("pop", D * 0.4); fire("pop", D * 0.6)
    pop(fr, box_text("But it can be PREVENTED with one test!", GREEN, 44), 540, 1150, t, D * 0.78, "ding")

def t_myth(fr, t, D):
    show(fr, pill("MYTH BUSTER", RED, size=50), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    if t > 0.4:
        d.rounded_rectangle((300, 380, 780, 560), 40, fill=(120, 80, 60))
        for k in range(5): d.ellipse((350 + k * 85, 440, 410 + k * 85, 500), fill=(200, 60, 50))
        d.text((540, 610), "Iron tablets", font=font("Bold", 40), fill=(120, 80, 60), anchor="mm")
        d.line((300, 380, 780, 560), fill=RED, width=14); d.line((780, 380, 300, 560), fill=RED, width=14)
    fire("boom", 0.4)
    show(fr, text_el("MYTH: All anaemia needs iron", 50, color=RED), 700, t, D * 0.25)
    show(fr, text_el("FACT: Carrier anaemia isn't low iron", 50, color=GREEN), 800, t, D * 0.45)
    show(fr, box_text("Test first. Take iron only as your doctor advises.", BLUE, 42), 930, t, D * 0.65)

def t_test(fr, t, D):
    show(fr, pill("THE TEST: SIMPLE & ONCE IN A LIFETIME", BLUE, size=40), 230, t, 0.1)
    ground(fr, 270, 800, 300); put(fr, DOC["aim"], 270, 560, 0.75); beam(fr, 270 + 175 * 0.75, 525, 720, 560, t)
    d = ImageDraw.Draw(fr); rbc(d, 840, 560, 90, (240, 150, 160), (250, 205, 210)); fire("zap", 0.3)
    items = [("CBC: first clue (small red cells)", RED, "1"), ("HPLC: confirms carrier status", PURPLE, "2"),
             ("Best: before marriage or pregnancy", GREEN, "3"), ("Also if anyone in family has it", ORANGE, "4")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.12 + 0.17 * i)); show(fr, card(txt, c, m, size=38), 850 + i * 135, t, D * (0.12 + 0.17 * i))

def t_plan(fr, t, D):
    show(fr, pill("BOTH CARRIERS? DON'T WORRY, PLAN!", GREEN, size=42), 230, t, 0.1)
    ground(fr, 300, 900, 320); put(fr, MOM, 300, 620, 0.75)
    ground(fr, 790, 900, 300); put(fr, DOC["idle"], 790, 660, 0.75)
    show(fr, card("Genetic counselling with your doctor", PURPLE, "1", size=40), 970, t, D * 0.15)
    show(fr, card("In pregnancy, CVS can check the baby", (183, 28, 28), "2", size=38), 1105, t, D * 0.35)
    fire("pop", D * 0.15); fire("pop", D * 0.35)
    pop(fr, box_text("Healthy children are absolutely possible!", GREEN, 44), 540, 1330, t, D * 0.6, "chime")

def t_close(fr, t, D):
    show(fr, big_logo(), 210, t, 0.2)
    fire("ding", 0.8); show(fr, box_text("Take any medicine only as advised by your doctor", GREEN, 42), 820, t, 0.8)
    show(fr, text_el("Know your thalassaemia status?", 54, color=DBLUE), 1010, t, D * 0.4)
    show(fr, text_el("Share with every young couple!", 44, "Medium", GREY), 1110, t, D * 0.5)
    show(fr, pill("Follow Health Test Simplified", BLUE, size=40), 1270, t, D * 0.6)
    show(fr, pill(DATE, ORANGE, size=32), 1410, t, D * 0.65)
    show(fr, text_el("For awareness only. Consult your doctor.", 30, "Regular", GREY), 1680, t, D * 0.7)

SC = [(t_hook, "navy"), (t_what, "light"), (t_types, "light"), (t_inherit, "light"), (t_india, "light"),
      (t_myth, "light"), (t_test, "light"), (t_plan, "light"), (t_close, "light")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        D = [10, 14, 15, 15, 13, 13, 15, 12, 11]; tests = [(0, .8), (1, .95), (2, .95), (3, .95), (4, .95), (5, .95), (6, .95), (7, .95), (8, .9)]
        ims = []
        for si, p in tests:
            fn, bg = SC[si]; d = D[si]; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((270, 480)))
        s = Image.new("RGB", (270 * 5, 480 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 270, (i // 5) * 480))
        s.save("sheet.png")
    else: run(SC, "/tmp/th2_", "Tuesday_Health_Tips_6Oct2026_Thalassaemia_Hindi.mp4")
