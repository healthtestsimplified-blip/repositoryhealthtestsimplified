import math, sys
from cbc_cartoon import run
from chromo_cartoon import x_shape, PINK, SKYB
from lft_cartoon2 import *

SOFT = (255, 240, 246); LAV = (149, 117, 205)

def mom_sprite(mood="happy"):
    w, h = 380, 640
    im = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    S = lambda *v: [x * SS for x in v]
    d.rounded_rectangle(S(150, 520, 180, 625), 12 * SS, fill=SKIN); d.rounded_rectangle(S(200, 520, 230, 625), 12 * SS, fill=SKIN)
    d.ellipse(S(130, 605, 190, 635), fill=(150, 60, 90)); d.ellipse(S(190, 605, 250, 635), fill=(150, 60, 90))
    d.polygon(S(130, 230, 250, 230, 300, 540, 80, 540), fill=(236, 64, 122))
    d.ellipse(S(170, 300, 330, 470), fill=(240, 98, 146))
    d.ellipse(S(250, 330, 290, 360), fill=(255, 170, 200))
    d.rounded_rectangle(S(140, 215, 240, 250), 16 * SS, fill=(236, 64, 122))
    d.line(S(230, 260, 280, 360, 245, 400), fill=SKIN, width=22 * SS)        # arm on belly
    d.line(S(140, 260, 105, 390), fill=SKIN, width=22 * SS)
    d.rectangle(S(175, 190, 205, 225), fill=SKIN)
    d.ellipse(S(130, 90, 250, 210), fill=SKIN)
    d.pieslice(S(122, 78, 258, 200), 180, 360, fill=(50, 30, 30)); d.ellipse(S(165, 40, 225, 100), fill=(50, 30, 30))
    d.rectangle(S(124, 130, 138, 175), fill=(50, 30, 30)); d.rectangle(S(242, 130, 256, 175), fill=(50, 30, 30))
    d.ellipse(S(162, 140, 176, 156), fill=(30, 30, 40)); d.ellipse(S(204, 140, 218, 156), fill=(30, 30, 40))
    d.ellipse(S(148, 162, 168, 176), fill=(255, 160, 170)); d.ellipse(S(212, 162, 232, 176), fill=(255, 160, 170))
    if mood == "happy": d.arc(S(168, 160, 212, 192), 20, 160, fill=(170, 60, 60), width=5 * SS)
    else: d.arc(S(172, 176, 208, 198), 200, 340, fill=(170, 60, 60), width=5 * SS)
    d.ellipse(S(186, 172, 194, 180), fill=(190, 40, 60))                     # bindi-ish dot below? (small smile accent)
    d.ellipse(S(186, 118, 194, 126), fill=(200, 30, 60))                     # bindi
    return im.resize((w, h), Image.LANCZOS)
MOM = mom_sprite(); MOM_W = mom_sprite("worried")

def heart_icon(d, x, y, s, col):
    d.ellipse((x - s, y - s * 0.6, x, y + s * 0.4), fill=col); d.ellipse((x, y - s * 0.6, x + s, y + s * 0.4), fill=col)
    d.polygon([(x - s * 0.95, y), (x + s * 0.95, y), (x, y + s * 1.1)], fill=col)

def timeline(d, p):
    x0, x1, y = 90, 990, 560
    d.rounded_rectangle((x0, y, x1, y + 60), 30, fill=(230, 236, 245))
    X = lambda wk: x0 + (x1 - x0) * wk / 40
    for wk in (0, 10, 20, 30, 40):
        d.text((X(wk), y + 100), f"{wk}", font=font("Bold", 32), fill=GREY, anchor="mm")
    d.text((540, y + 150), "weeks of pregnancy", font=font("Medium", 32), fill=GREY, anchor="mm")
    if p > 0.2:
        d.rounded_rectangle((X(11), y - 10, X(14), y + 70), 20, fill=GREEN)
        lx = (X(11) + X(14)) / 2 - 110
        d.line(((X(11) + X(14)) / 2, y - 10, lx, y - 40), fill=GREEN, width=4)
        d.text((lx, y - 130), "DOUBLE", font=font("Bold", 36), fill=GREEN, anchor="mm")
        d.text((lx, y - 82), "11–14 wks", font=font("Bold", 34), fill=GREEN, anchor="mm")
    if p > 0.6:
        d.rounded_rectangle((X(15), y - 10, X(20), y + 70), 20, fill=ORANGE)
        rx = (X(15) + X(20)) / 2 + 170
        d.line(((X(15) + X(20)) / 2, y - 10, rx, y - 40), fill=ORANGE, width=4)
        d.text((rx, y - 130), "TRIPLE / QUAD", font=font("Bold", 32), fill=ORANGE, anchor="mm")
        d.text((rx, y - 82), "15–20 wks", font=font("Bold", 34), fill=ORANGE, anchor="mm")

def calc(d, p, t):
    ins = [("Blood markers", PINK), ("NT scan", TEAL), ("Mother's age", LAV), ("Weight & details", ORANGE)]
    for i, (a, c) in enumerate(ins):
        if p < i / 5: break
        y = 400 + i * 120
        d.rounded_rectangle((60, y, 420, y + 90), 45, fill=c); d.text((240, y + 45), a, font=font("Bold", 34), fill=WHITE, anchor="mm")
        d.line((420, y + 45, 560, 620), fill=(200, 210, 225), width=6)
    if p > 0.8:
        d.rounded_rectangle((560, 500, 1020, 740), 34, fill=DBLUE)
        d.text((790, 560), "RISK =", font=font("Bold", 44), fill=WHITE, anchor="mm")
        d.text((790, 660), "1 in ____", font=font("Bold", 70), fill=YEL, anchor="mm")

# ---------------- scenes ----------------
def m_hook(fr, t, D):
    rays(fr, 540, 900, t, (255, 140, 190), a=40)
    put(fr, MOM, 540, 1390 + 8 * math.sin(t * 2), 0.8)
    pop(fr, white_text("Pregnant? Between 11 and 14 weeks?", 76), 540, 560, t, 0.1, "boom")
    pop(fr, white_text("Don't miss this one blood test!", 62, color=YEL), 540, 810, t, 1.8, "whoosh")
    pop(fr, box_text("Watch till the end: what 'high risk' REALLY means", GREEN, 38), 540, 1000, t, D * 0.55, "pop")

def m_what(fr, t, D):
    show(fr, pill("WHAT IS THE DOUBLE MARKER?", PINK, size=44), 230, t, 0.1)
    ground(fr, 300, 920, 320); put(fr, MOM, 300, 620, 0.8)
    ground(fr, 790, 900, 300); put(fr, DOC["idle"], 790, 660, 0.75)
    show(fr, card("A simple blood test for the mother", PINK, "1", size=40), 980, t, D * 0.2)
    show(fr, card("2 markers: beta-hCG & PAPP-A", LAV, "2", size=40), 1115, t, D * 0.4)
    show(fr, card("Read together with the NT scan", TEAL, "3", size=40), 1250, t, D * 0.6)
    for k in (0.2, 0.4, 0.6): fire("pop", D * k)
    show(fr, text_el("Part of first-trimester screening", 42, "Medium", GREEN), 1400, t, D * 0.78)

def m_when(fr, t, D):
    show(fr, pill("WHEN IS IT DONE?", GREEN, size=48), 230, t, 0.1)
    timeline(ImageDraw.Draw(fr), (t - 0.3) / (D * 0.5)); fire("ding", 0.3 + D * 0.1); fire("pop", 0.3 + D * 0.3)
    pop(fr, box_text("The window is short: don't miss it!", RED, 44), 540, 900, t, D * 0.6, "boom")
    show(fr, text_el("Missed it? Triple or Quad marker later, as doctor advises", 40, "Medium", GREY), 1040, t, D * 0.75)

def m_checks(fr, t, D):
    show(fr, pill("WHAT DOES IT SCREEN FOR?", BLUE, size=46), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    if t > 0.4:
        for k in range(3): x_shape(d, 400 + k * 140, 470, 110, (120, 70, 200) if k < 2 else RED)
        d.text((540, 590), "An extra chromosome", font=font("Bold", 40), fill=RED, anchor="mm")
    fire("pop", 0.4)
    items = [("Down syndrome (chromosome 21)", PURPLE, "1"), ("Edwards syndrome (chromosome 18)", BLUE, "2"),
             ("Patau syndrome (chromosome 13)", TEAL, "3")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.2 + 0.15 * i)); show(fr, card(txt, c, m, size=40), 680 + i * 135, t, D * (0.2 + 0.15 * i))
    show(fr, box_text("It does NOT reveal baby's sex: that is illegal in India", ORANGE, 38), 1120, t, D * 0.75)

def m_calc(fr, t, D):
    show(fr, pill("HOW IS THE RISK CALCULATED?", LAV, size=44), 230, t, 0.1)
    p = (t - 0.3) / (D * 0.55)
    for i in range(4): fire("pop", 0.3 + i / 5 * D * 0.55)
    fire("ding", 0.3 + 0.8 * D * 0.55)
    calc(ImageDraw.Draw(fr), p, t)
    show(fr, text_el("Software combines everything into one number", 44, color=DBLUE), 960, t, D * 0.75)

def m_result(fr, t, D):
    show(fr, pill("READING YOUR RESULT", ORANGE, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    if t > 0.4:
        d.rounded_rectangle((60, 360, 520, 640), 34, fill=(232, 245, 233), outline=GREEN, width=8)
        d.text((290, 420), "LOW RISK", font=font("Bold", 46), fill=GREEN, anchor="mm")
        d.text((290, 510), "e.g. 1 in 5,000", font=font("Bold", 38), fill=DBLUE, anchor="mm")
        d.text((290, 580), "Reassuring", font=font("Medium", 34), fill=GREY, anchor="mm")
    if t > D * 0.25:
        d.rounded_rectangle((560, 360, 1020, 640), 34, fill=(255, 243, 224), outline=ORANGE, width=8)
        d.text((790, 420), "HIGH RISK", font=font("Bold", 46), fill=ORANGE, anchor="mm")
        d.text((790, 510), "e.g. 1 in 100", font=font("Bold", 38), fill=DBLUE, anchor="mm")
        d.text((790, 580), "Needs more tests", font=font("Medium", 34), fill=GREY, anchor="mm")
    fire("pop", 0.4); fire("pop", D * 0.25)
    pop(fr, stroke_text("SCREENING ≠ DIAGNOSIS", 72, PURPLE, WHITE, 7), 540, 730, t, D * 0.45, "boom")
    show(fr, text_el("Most high-risk results still have healthy babies", 44, color=GREEN), 820, t, D * 0.55)
    show(fr, card("Doctor may advise NIPT, CVS or amniocentesis", BLUE, "→" if False else "+", size=40), 950, t, D * 0.7)
    fire("pop", D * 0.7)

def m_prep(fr, t, D):
    show(fr, pill("TIPS FOR MOTHERS-TO-BE", PINK, size=46), 230, t, 0.1)
    ground(fr, 250, 770, 300); put(fr, MOM, 250, 540, 0.6); sparkles(fr, 250, 520, 180, t, 5, (255, 150, 190))
    ground(fr, 790, 770, 300); put(fr, DOC["idle"], 790, 560, 0.7)
    items = [("Usually no fasting needed", GREEN, "1"), ("Fill form right: dates, weight, IVF", BLUE, "2"),
             ("Carry your NT scan report", TEAL, "3"), ("Discuss results only with your doctor", PINK, "4")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.12 + 0.18 * i)); show(fr, card(txt, c, m, size=40), 850 + i * 135, t, D * (0.12 + 0.18 * i))

def m_close(fr, t, D):
    show(fr, big_logo(), 210, t, 0.2)
    fire("ding", 0.8); show(fr, box_text("Take any medicine only as advised by your doctor", GREEN, 42), 820, t, 0.8)
    show(fr, text_el("Did your doctor tell you about this test?", 52, color=DBLUE), 1020, t, D * 0.45)
    show(fr, text_el("Share with every mother-to-be you know!", 44, "Medium", GREY), 1180, t, D * 0.55)
    show(fr, pill("Follow Health Test Simplified", BLUE, size=40), 1340, t, D * 0.65)
    show(fr, text_el("For awareness only. Consult your doctor.", 30, "Regular", GREY), 1680, t, D * 0.7)

SC = [(m_hook, "purple"), (m_what, "light"), (m_when, "light"), (m_checks, "light"), (m_calc, "light"),
      (m_result, "light"), (m_prep, "light"), (m_close, "light")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        D = [10, 14, 12, 15, 12, 16, 14, 11]; tests = [(0, .8), (1, .95), (2, .95), (3, .95), (4, .95), (5, .95), (6, .95), (7, .9)]
        ims = []
        for si, p in tests:
            fn, bg = SC[si]; d = D[si]; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((270, 480)))
        s = Image.new("RGB", (270 * 4, 480 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 4) * 270, (i // 4) * 480))
        s.save("sheet.png")
    else: run(SC, "/tmp/dm_", "Double_Marker_Test_Hindi.mp4")
