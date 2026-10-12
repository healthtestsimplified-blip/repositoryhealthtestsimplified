import math, sys
from cbc_cartoon import run, BD
from alz_cartoon import tube, ELDER
from uric_cartoon import kidney, crystals
from lft_cartoon2 import *
from hts_close import close_scene

DATE = "TUESDAY HEALTH TIPS  •  13 OCT 2026"
BONE = (250, 245, 230); BONE_D = (190, 175, 145)
CA_COL = (0, 137, 123); P_COL = (230, 120, 20); NECK = (240, 120, 140)

def ion(d, x, y, lab, col, r=24):
    d.ellipse((x - r, y - r, x + r, y + r), fill=col, outline=tuple(max(0, c - 60) for c in col), width=3)
    d.text((x, y), lab, font=font("Bold", int(r * (0.85 if len(lab) > 1 else 1.0))), fill=WHITE, anchor="mm")

def bone(d, cx, cy, L=300, s=1.0, ang=0.0, face=False, mood="happy"):
    """Cartoon bone centred at cx,cy; ang in radians."""
    ca, sa = math.cos(ang), math.sin(ang); h = L / 2; w = 34 * s; r = 40 * s
    ends = [(-h, -r * 0.8), (-h, r * 0.8), (h, -r * 0.8), (h, r * 0.8)]
    pts = [(-h, -w), (h, -w), (h, w), (-h, w)]
    rot = lambda x, y: (cx + x * ca - y * sa, cy + x * sa + y * ca)
    for ex, ey in ends:
        X, Y = rot(ex, ey); d.ellipse((X - r - 5, Y - r - 5, X + r + 5, Y + r + 5), fill=BONE_D)
    d.polygon([rot(*p) for p in [(-h, -w - 5), (h, -w - 5), (h, w + 5), (-h, w + 5)]], fill=BONE_D)
    for ex, ey in ends:
        X, Y = rot(ex, ey); d.ellipse((X - r, Y - r, X + r, Y + r), fill=BONE)
    d.polygon([rot(*p) for p in pts], fill=BONE)
    if face:
        for dx in (-30, 30):
            X, Y = rot(dx * s, -6 * s); d.ellipse((X - 9 * s, Y - 9 * s, X + 9 * s, Y + 9 * s), fill=GREY)
        X, Y = rot(0, 14 * s)
        if mood == "happy": d.arc((X - 22 * s, Y - 16 * s, X + 22 * s, Y + 12 * s), 20, 160, fill=GREY, width=max(3, int(5 * s)))
        else: d.arc((X - 22 * s, Y - 2 * s, X + 22 * s, Y + 26 * s), 200, 340, fill=GREY, width=max(3, int(5 * s)))

def thyroid(d, cx, cy, s=1.0, glow=0.0, t=0.0):
    """Butterfly thyroid with 4 parathyroid dots."""
    d.ellipse((cx - 150 * s, cy - 90 * s, cx - 10 * s, cy + 90 * s), fill=NECK, outline=(190, 70, 95), width=5)
    d.ellipse((cx + 10 * s, cy - 90 * s, cx + 150 * s, cy + 90 * s), fill=NECK, outline=(190, 70, 95), width=5)
    d.rectangle((cx - 30 * s, cy - 10 * s, cx + 30 * s, cy + 40 * s), fill=NECK)
    for dx, dy in ((-95, -45), (-95, 45), (95, -45), (95, 45)):
        rr = 20 * s + glow * 6 * math.sin(t * 6)
        x, y = cx + dx * s, cy + dy * s
        if glow: d.ellipse((x - rr - 14, y - rr - 14, x + rr + 14, y + rr + 14), outline=YEL, width=5)
        d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=(255, 196, 0), outline=(200, 120, 0), width=3)

def sun(d, cx, cy, t, r=55):
    for k in range(10):
        a = k * math.pi / 5 + t * 0.6
        d.line((cx + (r + 15) * math.cos(a), cy + (r + 15) * math.sin(a), cx + (r + 45) * math.cos(a), cy + (r + 45) * math.sin(a)), fill=(255, 170, 0), width=10)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 200, 40))
    d.text((cx, cy), "D", font=font("Bold", int(r * 1.1)), fill=ORANGE, anchor="mm")

def seesaw(d, cx, cy, tilt, t):
    """Calcium vs phosphorus see-saw; tilt in -1..1 (positive = calcium side up)."""
    a = 0.28 * tilt; L = 360
    x1, y1 = cx - L * math.cos(a), cy + L * math.sin(a); x2, y2 = cx + L * math.cos(a), cy - L * math.sin(a)
    d.polygon([(cx, cy + 10), (cx - 60, cy + 110), (cx + 60, cy + 110)], fill=GREY)
    d.line((x1, y1, x2, y2), fill=DBLUE, width=18)
    for k in range(3): ion(d, x1 + 40 + k * 55, y1 - 45 - 0 * k, "Ca", CA_COL, 28)
    for k in range(3): ion(d, x2 - 150 + k * 55, y2 - 45, "P", P_COL, 28)

def chip(d, x, y, txt, col, size=32):
    f = font("Bold", size); w = f.getlength(txt) + 50
    d.rounded_rectangle((x, y, x + w, y + 66), 33, fill=col)
    d.text((x + w / 2, y + 33), txt, font=f, fill=WHITE, anchor="mm")
    return w

def chip_rows(d, rows, y0, t, D, start, step, cols):
    ci = 0
    for ri, r in enumerate(rows):
        f = font("Bold", 32); tw = sum(f.getlength(x) + 50 for x in r) + 20 * (len(r) - 1); x = (W - tw) / 2
        for txt in r:
            if t > D * (start + step * ci): x += chip(d, x, y0 + ri * 90, txt, cols[ci % len(cols)]) + 20
            else: x += f.getlength(txt) + 70
            ci += 1

def cellrow(d, y, cells, cols, fill, xs, size=34, h=82):
    d.rectangle((xs[0], y, xs[-1], y + h), fill=fill)
    for i, c in enumerate(cells):
        d.text(((xs[i] + xs[i + 1]) / 2, y + h / 2), c, font=font("Bold", size), fill=cols[i], anchor="mm")

# ---------------- scenes ----------------
def s_hook(fr, t, D):
    rays(fr, 540, 1300, t, (120, 200, 255), a=40)
    show(fr, pill(DATE, ORANGE, size=36), 230, t, 0.1)
    put(fr, ELDER["confused"], 540, 1400, 0.8 + 0.02 * math.sin(t * 5))
    if t > D * 0.4: NOW["shake"] = 4 if t < D * 0.46 else 0
    pop(fr, white_text("Leg cramps at night?", 64), 540, 400, t, 0.3, "boom")
    pop(fr, white_text("Tingling hands & feet? Kidney stones?", 54), 540, 540, t, D * 0.2, "pop")
    pop(fr, white_text("Check your CALCIUM balance!", 70, color=YEL), 540, 710, t, D * 0.4, "whoosh")
    pop(fr, box_text("Calcium & Phosphorus test: watch till the end", GREEN, 40), 540, 920, t, D * 0.62, "pop")

def s_what(fr, t, D):
    show(fr, pill("CALCIUM & PHOSPHORUS", BLUE, size=46), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    if t > 0.3:
        bone(d, 540, 420, 520, 1.3, 0.04 * math.sin(t * 2))
        for k in range(5): ion(d, 380 + k * 80, 420 + (12 if k % 2 else -12), "Ca" if k % 2 == 0 else "P", CA_COL if k % 2 == 0 else P_COL, 22)
    show(fr, card("About 98-99% of calcium & about 85% of phosphorus are in bones and teeth", CA_COL, "1", size=32), 560, t, D * 0.12)
    fire("pop", D * 0.12)
    show(fr, card("The small amount in blood is vital for muscles & nerves", RED, "2", size=33), 720, t, D * 0.3)
    fire("pop", D * 0.3)
    if t > D * 0.45:
        fire("ding", D * 0.45); d = ImageDraw.Draw(fr)
        thyroid(d, 230, 1000, 0.75, 1.0, t); d.text((230, 1110), "Parathyroid", font=font("Bold", 30), fill=DBLUE, anchor="mm")
        sun(d, 540, 990, t, 50); d.text((540, 1110), "Vitamin D", font=font("Bold", 30), fill=ORANGE, anchor="mm")
        kidney(d, 850, 990, 0.55); d.text((850, 1110), "Kidneys", font=font("Bold", 30), fill=(150, 50, 60), anchor="mm")
        d.text((540, 1170), "...work together to control the levels", font=font("Medium", 32), fill=GREY, anchor="mm")
    if t > D * 0.7:
        fire("whoosh", D * 0.7); d = ImageDraw.Draw(fr)
        seesaw(d, 540, 1330, math.sin((t - D * 0.7) * 1.5), t)
    show(fr, text_el("Calcium up, phosphorus often down: so both are tested together", 34, "Medium", GREY), 1480, t, D * 0.75)

def s_signs(fr, t, D):
    show(fr, pill("SIGNS OF IMBALANCE", RED, size=46), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    if t > 0.3:
        d.rounded_rectangle((60, 330, 1020, 650), 30, fill=(225, 245, 243), outline=CA_COL, width=5)
        d.text((540, 385), "LOW calcium may cause", font=font("Bold", 44), fill=CA_COL, anchor="mm")
        for k in range(3):
            y = 470 + 20 * math.sin(t * 9 + k)
            d.line((120 + k * 30, y, 150 + k * 30, y + 30), fill=YEL, width=6)
    chip_rows(d, [["Tingling: fingers, toes, lips"], ["Muscle cramps", "Twitching"]], 450, t, D, 0.08, 0.08, [CA_COL, TEAL, BLUE])
    d = ImageDraw.Draw(fr)
    if t > D * 0.4:
        fire("whoosh", D * 0.4)
        d.rounded_rectangle((60, 690, 1020, 1140), 30, fill=(255, 236, 228), outline=RED, width=5)
        d.text((540, 745), "HIGH calcium", font=font("Bold", 44), fill=RED, anchor="mm")
        d.text((540, 800), "Often NO symptoms at first. Later:", font=font("Medium", 32), fill=GREY, anchor="mm")
    chip_rows(d, [["Thirst", "Passing urine often"], ["Tiredness", "Constipation", "Nausea"], ["Kidney stones"]], 850, t, D, 0.5, 0.06,
              [RED, ORANGE, PURPLE, (120, 72, 40), TEAL, RED])
    if t > D * 0.9: put(fr, BD["worried"], 540, 1420, 0.55 + 0.02 * math.sin(t * 4))
    show(fr, text_el("These signs have many causes: only a test can tell", 34, "Medium", GREY), 1200, t, D * 0.88)

def s_causes(fr, t, D):
    show(fr, pill("WHAT CAN CHANGE IT?", PURPLE, size=46), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    if t > 0.3:
        thyroid(d, 230, 420, 0.7, 1.0, t)
        d.text((640, 390), "HIGH calcium: most often", font=font("Bold", 36), fill=RED, anchor="mm")
        d.text((640, 445), "overactive parathyroid", font=font("Bold", 36), fill=DBLUE, anchor="mm")
        d.text((640, 500), "or some cancers", font=font("Bold", 36), fill=DBLUE, anchor="mm")
    xs = (60, 300, 1020)
    if t > D * 0.25:
        fire("pop", D * 0.25)
        d.rectangle((60, 590, 300, 754), fill=CA_COL); d.text((180, 672), "LOW Ca", font=font("Bold", 34), fill=WHITE, anchor="mm")
        d.rectangle((300, 590, 1020, 754), fill=(225, 245, 243))
        d.text((660, 631), "Low vitamin D, underactive parathyroid,", font=font("Bold", 30), fill=DBLUE, anchor="mm")
        d.text((660, 713), "kidney disease, low albumin or magnesium", font=font("Bold", 30), fill=DBLUE, anchor="mm")
    if t > D * 0.45:
        fire("pop", D * 0.45)
        d.rectangle((60, 780, 300, 862), fill=P_COL); d.text((180, 821), "HIGH P", font=font("Bold", 34), fill=WHITE, anchor="mm")
        d.rectangle((300, 780, 1020, 862), fill=(255, 240, 225)); d.text((660, 821), "Often a kidney problem", font=font("Bold", 32), fill=DBLUE, anchor="mm")
    if t > D * 0.6:
        fire("pop", D * 0.6)
        d.rectangle((60, 880, 300, 1044), fill=P_COL); d.text((180, 962), "LOW P", font=font("Bold", 34), fill=WHITE, anchor="mm")
        d.rectangle((300, 880, 1020, 1044), fill=(255, 240, 225))
        d.text((660, 921), "Low vitamin D, very poor nutrition,", font=font("Bold", 30), fill=DBLUE, anchor="mm")
        d.text((660, 1003), "alcohol, overactive parathyroid", font=font("Bold", 30), fill=DBLUE, anchor="mm")
    if t > D * 0.7:
        d = ImageDraw.Draw(fr); kidney(d, 300, 1260, 0.7); crystals(d, 300, 1260, 60, t, 6, (240, 240, 250))
        bone(d, 760, 1260, 300, 0.8, -0.3, face=True, mood="sad")
    pop(fr, box_text("Your doctor finds the cause: often with PTH & vitamin D tests", ORANGE, 36), 540, 1460, t, D * 0.75, "ding")

def s_who(fr, t, D):
    show(fr, pill("WHO MAY NEED IT?", GREEN, size=46), 230, t, 0.1)
    ground(fr, 540, 560, 240); put(fr, DOC["idle"], 540, 420, 0.48)
    items = [("Routine health check-up (often in a blood panel)", BLUE, "1"), ("Cramps, tingling or other symptoms above", CA_COL, "2"),
             ("Kidney disease", RED, "3"), ("Parathyroid or bone problems", PURPLE, "4"),
             ("Repeated kidney stones: urine calcium-creatinine ratio or 24-hour urine test", ORANGE, "5"),
             ("On medicines that affect calcium (monitoring)", TEAL, "6")]
    for i, (txt, c, m) in enumerate(items):
        tin = D * (0.08 + 0.12 * i); fire("pop", tin); show(fr, card(txt, c, m, size=32), 610 + i * 145, t, tin)
    show(fr, text_el("As your doctor advises", 38, "Medium", GREY), 1500, t, D * 0.85)

def s_prep(fr, t, D):
    show(fr, pill("HOW TO PREPARE", BLUE, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr); tube(d, 300, 470)
    d.text((300, 620), "Blood test", font=font("Bold", 38), fill=RED, anchor="mm")
    if t > 0.3:
        for k, (lab, col) in enumerate((("Calcium", CA_COL), ("Vitamin D", ORANGE), ("Antacid", BLUE), ("Water pill", PURPLE))):
            x, y = 640 + (k % 2) * 220, 400 + (k // 2) * 130
            d.rounded_rectangle((x - 95, y - 40, x + 95, y + 40), 40, fill=col)
            d.text((x, y), lab, font=font("Bold", 28), fill=WHITE, anchor="mm")
    items = [("Calcium test alone: usually no special preparation", GREEN, "1"),
             ("With other tests: a few hours of fasting may be asked", BLUE, "2"),
             ("Tell your doctor about calcium, vitamin D, antacids, water pills, thyroid medicine", ORANGE, "3"),
             ("Do not stop any medicine on your own", RED, "4")]
    for i, (txt, c, m) in enumerate(items):
        tin = D * (0.08 + 0.18 * i); fire("pop", tin); show(fr, card(txt, c, m, size=32), 700 + i * 150, t, tin)
    pop(fr, box_text("Follow your lab's instructions", TEAL, 40), 540, 1370, t, D * 0.72, "ding")

def s_read(fr, t, D):
    show(fr, pill("READING THE REPORT", PURPLE, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr); xs = (70, 470, 1010)
    if t > 0.3:
        cellrow(d, 340, ["Adults", "Approx. range (mg/dL)"], [WHITE, WHITE], PURPLE, xs, 36)
        rows = [("Total calcium", "8.5 - 10.2", CA_COL), ("Ionised calcium", "4.5 - 5.6", TEAL), ("Phosphorus", "2.8 - 4.5", P_COL)]
        for i, (a, b, c) in enumerate(rows):
            if t > D * (0.1 + 0.15 * i):
                cellrow(d, 422 + i * 90, [a, b], [DBLUE, c], WHITE if i % 2 else (245, 238, 250), xs, 38, 90)
        d.rectangle((70, 340, 1010, 692), outline=PURPLE, width=4)
    for i in range(3): fire("pop", D * (0.1 + 0.15 * i))
    show(fr, card("Children: phosphorus is normally higher, because bones are growing", ORANGE, "!", size=33), 740, t, D * 0.55)
    fire("ding", D * 0.55)
    pop(fr, box_text("Normal ranges vary by lab: always check the range printed on your report", GREEN, 38), 540, 1060, t, D * 0.75, "ding")

def s_know(fr, t, D):
    show(fr, pill("GOOD TO KNOW", TEAL, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    show(fr, card("About half of blood calcium rides on albumin protein. Low albumin can make total calcium look low: the doctor may order ionised calcium", ORANGE, "!", size=30), 320, t, 0.3)
    fire("pop", 0.3)
    if t > D * 0.25:
        fire("whoosh", D * 0.25)
        d.text((540, 600), "MYTH BUSTER", font=font("Bold", 50), fill=ORANGE, anchor="mm")
        d.rounded_rectangle((70, 650, 1010, 820), 28, fill=(255, 235, 238), outline=RED, width=5)
        d.text((570, 708), "Myth: normal blood calcium", font=font("Bold", 36), fill=RED, anchor="mm")
        d.text((570, 765), "means strong bones", font=font("Bold", 36), fill=RED, anchor="mm")
        d.line((100, 695, 160, 775), fill=RED, width=12); d.line((100, 775, 160, 695), fill=RED, width=12)
    show(fr, card("Truth: the body takes calcium from bones to keep blood level steady. Bone strength is checked by a bone density (DEXA) scan", GREEN, "✓", size=30), 860, t, D * 0.38)
    fire("ding", D * 0.38)
    pop(fr, box_text("'Calcium score' is a CT scan of heart arteries, not a blood test", PURPLE, 36), 540, 1230, t, D * 0.75, "pop")

SC = [(s_hook, "navy"), (s_what, "light"), (s_signs, "light"), (s_causes, "light"), (s_who, "light"),
      (s_prep, "light"), (s_read, "light"), (s_know, "light"), (close_scene("Ever had a calcium test?", DATE), "light")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        D = [13, 24, 18, 22, 22, 20, 20, 28, 30]; tests = [(i, .95) for i in range(9)]
        ims = []
        for si, p in tests:
            fn, bg = SC[si]; d = D[si]; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((360, 640)))
        s = Image.new("RGB", (360 * 5, 640 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 360, (i // 5) * 640))
        s.save("sheet.png")
    else: run(SC, "/tmp/cal_", "Tuesday_Health_Tips_13Oct2026_Calcium_Phosphorus_Hindi.mp4")
