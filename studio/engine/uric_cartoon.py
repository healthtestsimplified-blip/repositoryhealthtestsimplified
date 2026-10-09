import math, sys
from cbc_cartoon import run
from chromo_cartoon import PINK, SKYB
from dmarker_cartoon import MOM
from wes_cartoon import DAD
from alz_cartoon import tube, ELDER
from lft_cartoon2 import *
from hts_close import close_scene

DATE = "SATURDAY HEALTH TIPS  •  10 OCT 2026"
SKIN = (255, 205, 160); SKIN_D = (220, 160, 115)
CRYS = (120, 200, 255)

def foot(d, cx, cy, s, t, pain=0.0):
    """Side-ish cartoon foot seen from above; big toe glows red with `pain`."""
    d.rounded_rectangle((cx - 120 * s, cy - 60 * s, cx + 120 * s, cy + 260 * s), int(110 * s), fill=SKIN, outline=SKIN_D, width=6)
    toes = [(-80, -105, 52), (-12, -118, 34), (40, -112, 30), (84, -98, 26), (118, -78, 22)]
    for i, (dx, dy, r) in enumerate(toes):
        x, y, r = cx + dx * s, cy + dy * s, r * s
        col = SKIN
        if i == 0 and pain > 0:
            k = pain * (0.75 + 0.25 * math.sin(t * 8)); col = tuple(int(SKIN[j] + (c - SKIN[j]) * k) for j, c in enumerate((235, 60, 50)))
            for q in range(3):
                rr = r + 18 * s + q * 22 * s + 8 * math.sin(t * 6 + q)
                d.ellipse((x - rr, y - rr, x + rr, y + rr), outline=(255, 80, 60), width=5)
        d.ellipse((x - r, y - r * 1.15, x + r, y + r * 1.15), fill=col, outline=SKIN_D, width=5)

def crystals(d, cx, cy, R, t, n=14, col=CRYS):
    for k in range(n):
        a = k * 2.399 + 0.2 * math.sin(t + k); r = R * (0.25 + 0.75 * ((k * 37) % 100) / 100)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a); L = 34 + (k % 4) * 10; ang = k * 0.9 + t * 0.3
        dx, dy = L * math.cos(ang), L * math.sin(ang); w = 7
        nx, ny = -math.sin(ang) * w, math.cos(ang) * w
        d.polygon([(x - dx, y - dy), (x + nx, y + ny), (x + dx, y + dy), (x - nx, y - ny)], fill=col, outline=(40, 120, 200))

def kidney(d, cx, cy, s=1.0, face=True):
    col = (200, 80, 90)
    d.ellipse((cx - 90 * s, cy - 130 * s, cx + 90 * s, cy + 130 * s), fill=col, outline=(150, 50, 60), width=6)
    d.ellipse((cx + 30 * s, cy - 40 * s, cx + 110 * s, cy + 40 * s), fill=(232, 240, 250))
    if face:
        d.ellipse((cx - 45 * s, cy - 40 * s, cx - 20 * s, cy - 10 * s), fill=WHITE); d.ellipse((cx - 38 * s, cy - 30 * s, cx - 26 * s, cy - 16 * s), fill=GREY)
        d.ellipse((cx - 5 * s, cy - 40 * s, cx + 20 * s, cy - 10 * s), fill=WHITE); d.ellipse((cx + 2 * s, cy - 30 * s, cx + 14 * s, cy - 16 * s), fill=GREY)
        d.arc((cx - 40 * s, cy + 0, cx + 10 * s, cy + 40 * s), 20, 160, fill=GREY, width=6)

def drops(d, cx, cy, t, col=(255, 210, 60)):
    for k in range(4):
        y = cy + ((t * 160 + k * 60) % 240)
        d.ellipse((cx - 14, y - 18, cx + 14, y + 18), fill=col)

def meat(d, cx, cy):
    d.ellipse((cx - 85, cy - 60, cx + 85, cy + 60), fill=(190, 60, 60), outline=(140, 40, 40), width=5)
    d.ellipse((cx - 40, cy - 25, cx + 10, cy + 20), fill=(250, 225, 220))
def fish(d, cx, cy):
    d.ellipse((cx - 90, cy - 45, cx + 50, cy + 45), fill=(100, 160, 220), outline=(50, 100, 170), width=5)
    d.polygon((cx + 40, cy, cx + 95, cy - 45, cx + 95, cy + 45), fill=(100, 160, 220), outline=(50, 100, 170))
    d.ellipse((cx - 65, cy - 15, cx - 45, cy + 5), fill=WHITE); d.ellipse((cx - 60, cy - 10, cx - 50, cy), fill=GREY)
def beer(d, cx, cy):
    d.rounded_rectangle((cx - 50, cy - 70, cx + 50, cy + 80), 14, fill=(255, 190, 40), outline=(190, 130, 20), width=5)
    d.ellipse((cx - 58, cy - 95, cx + 58, cy - 50), fill=WHITE)
    d.arc((cx + 35, cy - 40, cx + 95, cy + 40), 270, 90, fill=(190, 130, 20), width=12)
def soda(d, cx, cy):
    d.rounded_rectangle((cx - 45, cy - 80, cx + 45, cy + 80), 18, fill=(220, 40, 60), outline=(150, 20, 40), width=5)
    d.rectangle((cx - 45, cy - 20, cx + 45, cy + 20), fill=WHITE); d.text((cx, cy), "SUGAR", font=font("Bold", 22), fill=(220, 40, 60), anchor="mm")
def dal(d, cx, cy):
    d.ellipse((cx - 100, cy - 30, cx + 100, cy + 30), fill=(255, 193, 7), outline=(200, 140, 0), width=4)
    d.chord((cx - 100, cy - 70, cx + 100, cy + 70), 0, 180, fill=(240, 240, 245), outline=(180, 185, 200), width=5)
def spinach(d, cx, cy):
    for k in range(5):
        a = -math.pi / 2 + (k - 2) * 0.45; x, y = cx + 55 * math.cos(a), cy + 55 * math.sin(a)
        d.ellipse((x - 32, y - 48, x + 32, y + 48), fill=(56, 142, 60), outline=(27, 94, 32), width=4)
    d.line((cx, cy + 10, cx, cy + 70), fill=(27, 94, 32), width=8)

def tile(d, cx, cy, lab, col, draw, hw=150):
    d.rounded_rectangle((cx - hw, cy - 140, cx + hw, cy + 140), 30, fill=WHITE, outline=col, width=6)
    draw(d, cx, cy - 25); d.text((cx, cy + 100), lab, font=font("Bold", 34), fill=col, anchor="mm")

def cross(d, cx, cy, s=40):
    d.line((cx - s, cy - s, cx + s, cy + s), fill=RED, width=12); d.line((cx - s, cy + s, cx + s, cy - s), fill=RED, width=12)

# ---------------- scenes ----------------
def s_hook(fr, t, D):
    rays(fr, 540, 1250, t, (255, 120, 80), a=40)
    show(fr, pill(DATE, ORANGE, size=36), 230, t, 0.1)
    d = ImageDraw.Draw(fr); foot(d, 540, 1320, 1.15, t, pain=min(1, t / 2))
    if t > D * 0.35: NOW["shake"] = 4 if t < D * 0.42 else 0
    pop(fr, white_text("Sudden severe pain in the big toe? Swelling, redness, often at night?", 62), 540, 470, t, 0.3, "boom")
    pop(fr, white_text("Check your Uric Acid!", 72, color=YEL), 540, 740, t, D * 0.4, "whoosh")
    pop(fr, box_text("Uric acid test: watch till the end", GREEN, 42), 540, 900, t, D * 0.62, "pop")

def s_what(fr, t, D):
    show(fr, pill("WHAT IS URIC ACID?", BLUE, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    # food + cells -> purines -> uric acid -> kidney -> urine
    tile(d, 220, 520, "Purines", ORANGE, lambda d, x, y: (meat(d, x - 45, y + 10), spinach(d, x + 75, y + 15)), hw=170)
    d.text((420, 520), "›", font=font("Bold", 110), fill=GREY, anchor="mm")
    if t > D * 0.25:
        fire("pop", D * 0.25); d.ellipse((480, 400, 700, 620), fill=WHITE, outline=PURPLE, width=6); crystals(d, 590, 510, 80, t, 9)
        d.text((590, 665), "Uric acid", font=font("Bold", 36), fill=PURPLE, anchor="mm")
    if t > D * 0.55:
        fire("pop", D * 0.55); d.text((750, 520), "›", font=font("Bold", 110), fill=GREY, anchor="mm"); kidney(d, 900, 500, 1.0); drops(d, 900, 650, t)
    show(fr, card("Waste made when purines break down", PURPLE, "1", size=38), 960, t, D * 0.15)
    show(fr, card("Purines: in our cells and some foods", ORANGE, "2", size=38), 1095, t, D * 0.35)
    show(fr, card("Most leaves the body through kidneys in urine", BLUE, "3", size=36), 1230, t, D * 0.6)

def s_gout(fr, t, D):
    show(fr, pill("WHEN IT GOES HIGH", RED, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    show(fr, text_el("Body makes too much, or kidneys remove too little", 42, color=DBLUE), 340, t, 0.3)
    if t > D * 0.25:
        fire("boom", D * 0.3)
        d.ellipse((90, 520, 510, 940), fill=WHITE, outline=RED, width=8); crystals(d, 300, 730, 170, t, 18)
        d.text((300, 990), "Needle-like crystals", font=font("Bold", 34), fill=RED, anchor="mm")
        d.text((300, 1040), "in joints = GOUT", font=font("Bold", 34), fill=RED, anchor="mm")
    if t > D * 0.6:
        fire("pop", D * 0.6); kidney(d, 780, 720, 1.2, face=False)
        for k in range(3): d.polygon([(760 + k * 30, 690 + k * 20), (775 + k * 30, 670 + k * 20), (795 + k * 30, 690 + k * 20), (778 + k * 30, 712 + k * 20)], fill=(250, 235, 200), outline=GREY)
        d.text((780, 990), "Kidney stones", font=font("Bold", 34), fill=ORANGE, anchor="mm")
        d.text((780, 1040), "in some people", font=font("Medium", 32), fill=GREY, anchor="mm")
    pop(fr, box_text("High uric acid in blood = hyperuricemia", PURPLE, 40), 540, 1230, t, D * 0.8, "ding")

def s_raise(fr, t, D):
    show(fr, pill("WHAT CAN RAISE IT?", ORANGE, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    items = [("Red & organ meat", RED, meat), ("Some seafood", BLUE, fish), ("Alcohol, esp. beer", ORANGE, beer), ("Sugary soft drinks", PINK, soda)]
    for i, (lab, c, fn) in enumerate(items):
        tin = 0.3 + i * D * 0.12; fire("pop", tin)
        if t > tin: tile(d, 280 + (i % 2) * 520, 500 + (i // 2) * 320, lab, c, fn, hw=235)
    show(fr, card("Extra weight, kidney disease, some medicines", PURPLE, "+", size=36), 1030, t, D * 0.62)
    show(fr, card("Gout in the family", TEAL, "+", size=40), 1165, t, D * 0.78)
    fire("pop", D * 0.62); fire("pop", D * 0.78)

def s_who(fr, t, D):
    show(fr, pill("WHO SHOULD TEST?", GREEN, size=48), 230, t, 0.1)
    ground(fr, 260, 640, 260); put(fr, DAD, 260, 470, 0.6)
    ground(fr, 820, 640, 260); put(fr, ELDER["happy"], 820, 470, 0.5)
    items = [("Sudden joint pain & swelling (big toe)", RED, "1"), ("Kidney stones", ORANGE, "2"), ("On gout treatment (follow-up)", BLUE, "3"),
             ("Kidney disease", PURPLE, "4"), ("During some cancer treatments", TEAL, "5")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.1 + 0.13 * i)); show(fr, card(txt, c, m, size=36), 720 + i * 128, t, D * (0.1 + 0.13 * i))
    show(fr, text_el("Or when your doctor advises", 38, "Medium", GREY), 1380, t, D * 0.8)

def s_prep(fr, t, D):
    show(fr, pill("HOW IS IT DONE?", BLUE, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr); tube(d, 330, 500)
    d.text((330, 650), "Blood test", font=font("Bold", 38), fill=RED, anchor="mm")
    d.rounded_rectangle((640, 400, 860, 600), 24, fill=(255, 248, 200), outline=(200, 160, 0), width=6)
    d.text((750, 500), "24 hr", font=font("Bold", 46), fill=(160, 110, 0), anchor="mm")
    d.text((750, 650), "Urine (sometimes)", font=font("Bold", 34), fill=(160, 110, 0), anchor="mm")
    fire("pop", 0.3)
    show(fr, card("Some labs ask for a few hours fasting: follow your lab", BLUE, "1", size=34), 760, t, D * 0.15)
    show(fr, card("Avoid alcohol before the test", RED, "2", size=38), 895, t, D * 0.35)
    show(fr, card("Tell your doctor about medicines you take", GREEN, "3", size=36), 1030, t, D * 0.5)
    show(fr, card("24-hr urine uric acid: mainly for kidney stones", ORANGE, "4", size=34), 1165, t, D * 0.75)
    for k in (0.15, 0.35, 0.5, 0.75): fire("pop", D * k)

def s_read(fr, t, D):
    show(fr, pill("READING THE REPORT", PURPLE, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    # gauge bar
    x0, x1, y = 110, 970, 520
    d.rounded_rectangle((x0, y, x1, y + 70), 35, fill=(230, 235, 245))
    lo, hi = x0 + (x1 - x0) * 0.3, x0 + (x1 - x0) * 0.62
    d.rounded_rectangle((lo, y, hi, y + 70), 20, fill=GREEN)
    d.rounded_rectangle((hi, y, x1, y + 70), 35, fill=(255, 205, 210))
    d.text(((lo + hi) / 2, y + 35), "Usual range", font=font("Bold", 34), fill=WHITE, anchor="mm")
    d.text((lo, y + 115), "~3.5", font=font("Bold", 40), fill=DBLUE, anchor="mm"); d.text((hi, y + 115), "~7", font=font("Bold", 40), fill=DBLUE, anchor="mm")
    d.text(((hi + x1) / 2, y + 35), "High", font=font("Bold", 34), fill=RED, anchor="mm")
    mx = x0 + (x1 - x0) * (0.2 + 0.35 * (0.5 + 0.5 * math.sin(t * 1.3)))
    d.polygon((mx - 22, y - 45, mx + 22, y - 45, mx, y - 5), fill=DBLUE)
    show(fr, text_el("About 3.5 to 7 mg/dL (approximately)", 48, color=DBLUE), 700, t, 0.4)
    show(fr, card("Women: usually a little lower", PINK, "1", size=40), 830, t, D * 0.3)
    show(fr, card("Range varies by lab: see your report", ORANGE, "2", size=40), 965, t, D * 0.48)
    fire("pop", D * 0.3); fire("pop", D * 0.48)
    pop(fr, box_text("One number doesn't decide a disease: the doctor reads it with your symptoms", TEAL, 36), 540, 1210, t, D * 0.7, "ding")

def s_know(fr, t, D):
    show(fr, pill("GOOD TO KNOW", TEAL, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    show(fr, card("During a gout attack, uric acid can be normal", BLUE, "1", size=36), 340, t, 0.3)
    show(fr, card("Many with high uric acid never get gout", PURPLE, "2", size=38), 475, t, D * 0.22)
    show(fr, card("Medicine or not? Your doctor decides", GREEN, "3", size=38), 610, t, D * 0.36)
    fire("pop", 0.3); fire("pop", D * 0.22); fire("pop", D * 0.36)
    if t > D * 0.52:
        fire("whoosh", D * 0.52)
        d.text((540, 790), "MYTH BUSTER", font=font("Bold", 50), fill=ORANGE, anchor="mm")
        tile(d, 270, 990, "Dal & spinach", GREEN, lambda d, x, y: (dal(d, x - 70, y + 20), spinach(d, x + 110, y)), hw=215)
        tile(d, 810, 990, "Meat, seafood, beer", RED, lambda d, x, y: (meat(d, x - 80, y + 10), beer(d, x + 100, y + 10)), hw=215)
        d.text((540, 990), "vs", font=font("Bold", 60), fill=GREY, anchor="mm")
    pop(fr, box_text("Studies: dal & purine-rich vegetables don't raise gout risk like meat, seafood & beer", GREEN, 34), 540, 1290, t, D * 0.7, "ding")

SC = [(s_hook, "navy"), (s_what, "light"), (s_gout, "light"), (s_raise, "light"), (s_who, "light"),
      (s_prep, "light"), (s_read, "light"), (s_know, "light"), (close_scene("Have you ever had a uric acid test?", DATE), "light")]

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
    else: run(SC, "/tmp/ua_", "Saturday_Health_Tips_10Oct2026_Uric_Acid_Hindi.mp4")
