import math, sys
from cbc_cartoon import run, BD
from alz_cartoon import tube
from lft_cartoon2 import *
from hts_close import close_scene

DATE = "MONDAY HEALTH TIPS  •  12 OCT 2026"
RUST = (176, 84, 40); BROWN = (120, 72, 40)

def fe_ball(d, x, y, r=22, col=RUST):
    d.ellipse((x - r, y - r, x + r, y + r), fill=col, outline=(90, 40, 15), width=3)
    d.text((x, y), "Fe", font=font("Bold", int(r * 0.95)), fill=WHITE, anchor="mm")

def truck(d, x, y, filled, col=BLUE):
    d.rounded_rectangle((x, y, x + 150, y + 70), 12, fill=WHITE, outline=col, width=6)
    d.rounded_rectangle((x + 150, y + 15, x + 205, y + 70), 10, fill=col)
    d.rectangle((x + 165, y + 25, x + 195, y + 45), fill=(200, 230, 255))
    for wx in (x + 35, x + 165): d.ellipse((wx - 17, y + 58, wx + 17, y + 92), fill=GREY)
    if filled:
        for k in range(3): fe_ball(d, x + 32 + k * 43, y + 35, 19)

def warehouse(d, cx, cy, t):
    d.polygon([(cx - 170, cy - 40), (cx, cy - 150), (cx + 170, cy - 40)], fill=BROWN)
    d.rectangle((cx - 150, cy - 40, cx + 150, cy + 130), fill=(240, 220, 190), outline=BROWN, width=6)
    d.rectangle((cx - 55, cy + 30, cx + 55, cy + 130), fill=(160, 110, 70))
    for k in range(5): fe_ball(d, cx - 120 + k * 60, cy - 5, 22)
    d.text((cx, cy - 75), "FERRITIN", font=font("Bold", 34), fill=WHITE, anchor="mm")

def sun(d, cx, cy, t):
    for k in range(10):
        a = k * math.pi / 5 + t * 0.6
        d.line((cx + 70 * math.cos(a), cy + 70 * math.sin(a), cx + 100 * math.cos(a), cy + 100 * math.sin(a)), fill=(255, 170, 0), width=10)
    d.ellipse((cx - 55, cy - 55, cx + 55, cy + 55), fill=(255, 200, 40))
    d.text((cx, cy + 135), "Morning", font=font("Bold", 36), fill=ORANGE, anchor="mm")

def stat(d, cx, cy, big, l1, l2, col, k):
    r = 165
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(225, 230, 240), width=26)
    d.arc((cx - r, cy - r, cx + r, cy + r), -90, -90 + 360 * k, fill=col, width=26)
    d.text((cx, cy - 10), big, font=font("Bold", 84), fill=col, anchor="mm")
    d.text((cx, cy + r + 50), l1, font=font("Bold", 36), fill=DBLUE, anchor="mm")
    d.text((cx, cy + r + 95), l2, font=font("Medium", 30), fill=GREY, anchor="mm")

def chip(d, x, y, txt, col):
    f = font("Bold", 32); w = f.getlength(txt) + 50
    d.rounded_rectangle((x, y, x + w, y + 66), 33, fill=col)
    d.text((x + w / 2, y + 33), txt, font=f, fill=WHITE, anchor="mm")
    return w

# ---------------- scenes ----------------
def s_hook(fr, t, D):
    rays(fr, 540, 1300, t, (255, 140, 90), a=40)
    show(fr, pill(DATE, ORANGE, size=36), 230, t, 0.1)
    put(fr, BD["sick"], 540, 1380, 0.85 + 0.03 * math.sin(t * 5))
    if t > D * 0.4: NOW["shake"] = 4 if t < D * 0.46 else 0
    pop(fr, white_text("Always tired? Pale? Breathless?", 62), 540, 420, t, 0.3, "boom")
    pop(fr, white_text("Craving ice or clay?", 60), 540, 560, t, D * 0.25, "pop")
    pop(fr, white_text("It could be LOW IRON!", 76, color=YEL), 540, 720, t, D * 0.42, "whoosh")
    pop(fr, box_text("Iron studies & Ferritin: watch till the end", GREEN, 40), 540, 920, t, D * 0.65, "pop")

def s_what(fr, t, D):
    show(fr, pill("IRON STUDIES = 4 CLUES", BLUE, size=46), 230, t, 0.1)
    show(fr, text_el("Iron makes haemoglobin, which carries oxygen", 38, color=RED), 330, t, 0.2)
    d = ImageDraw.Draw(fr)
    if t > 0.3:
        x = 60 + 30 * math.sin(t * 2)
        truck(d, x, 470, True); truck(d, x, 590, False, TEAL)
        d.text((x + 105, 700), "Transferrin taxis", font=font("Bold", 30), fill=BLUE, anchor="mm")
        warehouse(d, 790, 560, t)
    items = [("Serum iron: iron in blood right now", RED, "1"), ("TIBC / Transferrin: the iron 'taxis'", BLUE, "2"),
             ("Transferrin saturation: % of taxis filled", TEAL, "3"), ("Ferritin: iron stored in the body's 'warehouse'", RUST, "4")]
    for i, (txt, c, m) in enumerate(items):
        tin = D * (0.2 + 0.17 * i); fire("pop", tin); show(fr, card(txt, c, m, size=34), 790 + i * 140, t, tin)

def s_india(fr, t, D):
    show(fr, pill("ANAEMIA IN INDIA (NFHS-5)", RED, size=44), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    k = max(0, min(1, (t - 0.3) / (D * 0.3)))
    if t > 0.3:
        stat(d, 290, 520, "~57%", "Women 15-49 yrs", "had anaemia", RED, 0.57 * k)
        stat(d, 790, 520, "~67%", "Children 6-59 mths", "had anaemia", ORANGE, 0.67 * k)
        d.text((540, 840), "Survey 2019-21. Low iron is one common cause.", font=font("Medium", 32), fill=GREY, anchor="mm")
    if t > D * 0.45:
        fire("ding", D * 0.45); d = ImageDraw.Draw(fr)
        d.text((540, 930), "Common signs", font=font("Bold", 46), fill=DBLUE, anchor="mm")
        rows = [["Tiredness", "Weakness", "Pale skin"], ["Breathless", "Fast heartbeat", "Headache"], ["Cold hands & feet", "Brittle nails"]]
        cols = [RED, ORANGE, PURPLE, BLUE, TEAL, GREEN, RUST, GREY]; ci = 0
        for ri, r in enumerate(rows):
            f = font("Bold", 32); tw = sum(f.getlength(x) + 50 for x in r) + 20 * (len(r) - 1); x = (W - tw) / 2
            for txt in r:
                if t > D * (0.5 + 0.05 * ci): x += chip(d, x, 1000 + ri * 95, txt, cols[ci]) + 20
                else: x += f.getlength(txt) + 70
                ci += 1

def cellrow(d, y, cells, cols, fill, bold=False, xs=(70, 400, 700, 1010)):
    d.rectangle((xs[0], y, xs[-1], y + 82), fill=fill)
    for i, c in enumerate(cells):
        d.text(((xs[i] + xs[i + 1]) / 2, y + 41), c, font=font("Bold" if bold or i else "Medium", 36), fill=cols[i], anchor="mm")

def s_pattern(fr, t, D):
    show(fr, pill("WHAT THE REPORT SHOWS", PURPLE, size=46), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    if t > 0.3:
        cellrow(d, 360, ["Test", "Low iron", "Too much iron"], [WHITE] * 3, PURPLE, True)
        rows = [("Ferritin", "LOW", "HIGH"), ("Serum iron", "LOW", ""), ("TIBC", "HIGH", ""), ("Saturation", "LOW", "HIGH")]
        for i, (a, b, c) in enumerate(rows):
            vis = t > D * (0.12 + 0.08 * i)
            cb = (RED if b == "LOW" else BLUE) if vis else WHITE
            cc = (BLUE if c == "HIGH" else GREY) if (vis and t > D * 0.5) else WHITE
            cellrow(d, 442 + i * 82, [a, b, c or "-"], [DBLUE, cb, cc], WHITE if i % 2 else (245, 238, 250))
        d.rectangle((70, 360, 1010, 770), outline=PURPLE, width=4)
        d.text((540, 810), "Usual pattern (approximately)", font=font("Medium", 32), fill=GREY, anchor="mm")
    for i in range(4): fire("pop", D * (0.12 + 0.08 * i))
    fire("whoosh", D * 0.5)
    if t > D * 0.65:
        d = ImageDraw.Draw(fr); put(fr, LV["worried"], 300, 1080, 0.45)
        d.text((300, 1200), "Liver", font=font("Bold", 34), fill=(150, 40, 40), anchor="mm")
        d.ellipse((640, 990, 760, 1100), fill=RED); d.ellipse((720, 990, 840, 1100), fill=RED)
        d.polygon([(645, 1065), (835, 1065), (740, 1190)], fill=RED)
        d.text((740, 1230), "Heart", font=font("Bold", 34), fill=RED, anchor="mm")
    pop(fr, box_text("Too much iron can also harm the liver, heart & other organs", ORANGE, 38), 540, 1400, t, D * 0.72, "ding")

def s_who(fr, t, D):
    show(fr, pill("WHO MAY NEED IT?", GREEN, size=46), 230, t, 0.1)
    ground(fr, 540, 560, 240); put(fr, DOC["idle"], 540, 420, 0.48)
    items = [("Anaemia or small red cells on CBC", RED, "1"), ("Heavy periods", PURPLE, "2"), ("Pregnancy", ORANGE, "3"),
             ("Poor diet: some children & vegetarians", BLUE, "4"), ("Frequent blood donors; stomach or gut disease", TEAL, "5"),
             ("Many blood transfusions (e.g. thalassaemia): MRI may check liver & heart iron", RUST, "6")]
    for i, (txt, c, m) in enumerate(items):
        tin = D * (0.08 + 0.12 * i); fire("pop", tin); show(fr, card(txt, c, m, size=32), 610 + i * 145, t, tin)
    show(fr, text_el("As your doctor advises", 38, "Medium", GREY), 1500, t, D * 0.85)

def s_prep(fr, t, D):
    show(fr, pill("HOW TO PREPARE", BLUE, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr); tube(d, 300, 470)
    d.text((300, 620), "Blood test", font=font("Bold", 38), fill=RED, anchor="mm")
    sun(d, 780, 450, t)
    items = [("Serum iron is highest in the morning: morning sample is better", ORANGE, "1"),
             ("Many labs ask for about 8 hours fasting", BLUE, "2"), ("Ferritin alone: usually no fasting needed", GREEN, "3"),
             ("On iron tablets or injections? Tell your doctor before the test", RED, "4")]
    for i, (txt, c, m) in enumerate(items):
        tin = D * (0.08 + 0.18 * i); fire("pop", tin); show(fr, card(txt, c, m, size=33), 700 + i * 150, t, tin)
    pop(fr, box_text("Follow your lab's instructions", TEAL, 40), 540, 1370, t, D * 0.65, "ding")

def s_read(fr, t, D):
    show(fr, pill("READING THE REPORT", PURPLE, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    if t > 0.3:
        d.rounded_rectangle((70, 340, 1010, 620), 30, fill=(253, 236, 228), outline=RUST, width=5)
        d.text((540, 395), "FERRITIN (WHO, healthy, age 5+)", font=font("Bold", 38), fill=RUST, anchor="mm")
        d.text((540, 480), "below ~15 ng/mL", font=font("Bold", 58), fill=RED, anchor="mm")
        d.text((540, 565), "= iron deficiency", font=font("Medium", 38), fill=DBLUE, anchor="mm")
    if t > D * 0.4:
        fire("pop", D * 0.4)
        d.text((540, 690), "Transferrin saturation (approx.)", font=font("Bold", 38), fill=TEAL, anchor="mm")
        cellrow(d, 740, ["Men", "20-50%", ""], [DBLUE, TEAL, WHITE], (225, 245, 248), xs=(170, 450, 900, 910))
        cellrow(d, 822, ["Women", "15-45%", ""], [DBLUE, TEAL, WHITE], WHITE, xs=(170, 450, 900, 910))
        d.rectangle((170, 740, 910, 904), outline=TEAL, width=4)
    pop(fr, box_text("Normal ranges vary by lab: always check the range printed on your report", GREEN, 38), 540, 1110, t, D * 0.7, "ding")

def s_know(fr, t, D):
    show(fr, pill("GOOD TO KNOW", TEAL, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    show(fr, card("Infection, inflammation or liver disease raise ferritin: it may look normal even when iron is low", ORANGE, "!", size=31), 330, t, 0.3)
    fire("pop", 0.3)
    if t > D * 0.25:
        fire("whoosh", D * 0.25)
        d.text((540, 560), "MYTH BUSTER", font=font("Bold", 50), fill=ORANGE, anchor="mm")
        d.rounded_rectangle((70, 610, 1010, 780), 28, fill=(255, 235, 238), outline=RED, width=5)
        d.text((570, 668), "Myth: every anaemia is low iron,", font=font("Bold", 36), fill=RED, anchor="mm")
        d.text((570, 725), "just take iron tablets", font=font("Bold", 36), fill=RED, anchor="mm")
        d.line((100, 655, 160, 735), fill=RED, width=12); d.line((100, 735, 160, 655), fill=RED, width=12)
    show(fr, card("Truth: thalassaemia trait also makes small red cells & doesn't need iron. Test first, then your doctor's advice", GREEN, "✓", size=31), 820, t, D * 0.42)
    fire("ding", D * 0.42)
    pop(fr, box_text("Less tea with meals, more vitamin C fruits: helps iron absorption", PURPLE, 38), 540, 1190, t, D * 0.78, "pop")

SC = [(s_hook, "navy"), (s_what, "light"), (s_india, "light"), (s_pattern, "light"), (s_who, "light"),
      (s_prep, "light"), (s_read, "light"), (s_know, "light"), (close_scene("Ever had a ferritin test?", DATE), "light")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        D = [13, 20, 20, 17, 22, 22, 20, 25, 30]; tests = [(i, .95) for i in range(9)]
        ims = []
        for si, p in tests:
            fn, bg = SC[si]; d = D[si]; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((360, 640)))
        s = Image.new("RGB", (360 * 5, 640 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 360, (i // 5) * 640))
        s.save("sheet.png")
    else: run(SC, "/tmp/irn_", "Monday_Health_Tips_12Oct2026_Iron_Ferritin_Hindi.mp4")
