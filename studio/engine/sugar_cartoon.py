import math, sys
from cbc_cartoon import run
from chromo_cartoon import PINK, SKYB
from gene_cartoon import person
from dmarker_cartoon import MOM, LAV
from wes_cartoon import KID, DAD
from alz_cartoon import tube, ELDER
from lft_cartoon2 import *
from hts_close import close_scene

DATE = "FRIDAY HEALTH TIPS  •  9 OCT 2026"
SUGAR = (255, 255, 255)

def cube(d, x, y, s, rot=0.0):
    pts = [(x + s * math.cos(rot + k * math.pi / 2 + math.pi / 4), y + s * math.sin(rot + k * math.pi / 2 + math.pi / 4)) for k in range(4)]
    d.polygon(pts, fill=WHITE, outline=(190, 200, 215)); d.line(pts + [pts[0]], fill=(190, 200, 215), width=4)

def clock(d, cx, cy, r, hours, t, col=BLUE):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=WHITE, outline=col, width=10)
    for k in range(12):
        a = k * math.pi / 6; d.line((cx + 0.82 * r * math.cos(a), cy + 0.82 * r * math.sin(a), cx + 0.92 * r * math.cos(a), cy + 0.92 * r * math.sin(a)), fill=GREY, width=5)
    a = -math.pi / 2 + t * 1.2; d.line((cx, cy, cx + 0.75 * r * math.cos(a), cy + 0.75 * r * math.sin(a)), fill=col, width=9)
    d.line((cx, cy, cx, cy - 0.5 * r), fill=GREY, width=12); d.ellipse((cx - 12, cy - 12, cx + 12, cy + 12), fill=col)
    d.text((cx, cy + r + 45), hours, font=font("Bold", 40), fill=col, anchor="mm")

def plate(d, cx, cy):
    d.ellipse((cx - 150, cy - 70, cx + 150, cy + 70), fill=(235, 238, 245), outline=(200, 205, 215), width=5)
    d.ellipse((cx - 100, cy - 45, cx - 10, cy + 25), fill=(255, 245, 225))          # rice
    for k in range(3): d.ellipse((cx + 10 + k * 40, cy - 40, cx + 50 + k * 40, cy), fill=(230, 160, 60))   # roti
    d.ellipse((cx + 10, cy + 5, cx + 110, cy + 50), fill=(255, 193, 7))               # dal

def glass(d, cx, cy, t):
    d.polygon((cx - 70, cy - 120, cx + 70, cy - 120, cx + 55, cy + 110, cx - 55, cy + 110), fill=(225, 240, 252), outline=(150, 175, 200))
    lvl = cy - 60 + 10 * math.sin(t * 2)
    d.polygon((cx - 63, lvl, cx + 63, lvl, cx + 55, cy + 108, cx - 55, cy + 108), fill=(255, 250, 220))
    d.text((cx, cy + 20), "75 g", font=font("Bold", 40), fill=ORANGE, anchor="mm")

def bands(d, y, rows):
    for i, (rng, lab, c) in enumerate(rows):
        yy = y + i * 120
        d.rounded_rectangle((70, yy, W - 70, yy + 104), 26, fill=WHITE, outline=c, width=7)
        d.text((300, yy + 52), rng, font=font("Bold", 42), fill=c, anchor="mm")
        d.text((760, yy + 52), lab, font=font("Bold", 38), fill=DBLUE, anchor="mm")

# ---------------- scenes ----------------
def s_hook(fr, t, D):
    rays(fr, 540, 900, t, (255, 190, 80), a=40)
    show(fr, pill(DATE, ORANGE, size=36), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    for k in range(6): cube(d, 140 + k * 160, 1250 + 30 * math.sin(t * 2 + k), 45, t * 0.8 + k)
    put(fr, DAD, 540, 1560, 0.75)
    pop(fr, white_text("Always thirsty? Passing urine often? Slow healing?", 70), 540, 500, t, 0.3, "boom")
    pop(fr, white_text("Your sugar may be high!", 66, color=YEL), 540, 760, t, D * 0.4, "whoosh")
    pop(fr, box_text("Fasting, PP & GTT: watch till the end", GREEN, 42), 540, 950, t, D * 0.65, "pop")

def s_india(fr, t, D):
    show(fr, pill("DIABETES IN INDIA", RED, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    for k in range(100):
        if t < 0.3 + k * 0.012: break
        r, c = divmod(k, 20); x = 85 + c * 48; y = 360 + r * 62
        col = RED if k % 9 == 3 else (ORANGE if k % 7 == 1 else (196, 205, 220))
        d.ellipse((x - 11, y - 26, x + 11, y - 4), fill=col); d.rounded_rectangle((x - 16, y - 2, x + 16, y + 26), 10, fill=col)
    fire("whoosh", 0.3)
    pop(fr, stroke_text("10 crore+", 120, RED, WHITE, 9), 540, 760, t, D * 0.25, "boom")
    show(fr, text_el("people in India have diabetes (about 11%)", 44, color=DBLUE), 880, t, D * 0.3)
    show(fr, card("About 13.6 crore have prediabetes", ORANGE, "!", size=40), 1010, t, D * 0.5)
    show(fr, card("Many don't know it yet", PURPLE, "?", size=40), 1145, t, D * 0.68)
    fire("pop", D * 0.5); fire("pop", D * 0.68)
    show(fr, text_el("Source: ICMR-INDIAB study, 2023", 30, "Medium", GREY), 1290, t, D * 0.72)

def s_three(fr, t, D):
    show(fr, pill("3 MAIN SUGAR TESTS", BLUE, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    data = [("FASTING", "Empty stomach", BLUE, 0.3), ("PP", "2 hrs after meal", GREEN, D * 0.35), ("GTT", "After glucose drink", ORANGE, D * 0.65)]
    for i, (a, b, c, tin) in enumerate(data):
        fire("pop", tin)
        if t < tin: continue
        x = 190 + i * 350
        d.rounded_rectangle((x - 160, 380, x + 160, 900), 30, fill=WHITE, outline=c, width=7)
        if i == 0: clock(d, x, 560, 95, "", t, c)
        elif i == 1: plate(d, x, 590)
        else: glass(d, x, 590, t)
        d.text((x, 760), a, font=font("Bold", 52), fill=c, anchor="mm")
        d.text((x, 830), b, font=font("Medium", 30), fill=GREY, anchor="mm")
    show(fr, text_el("All need just a blood sample", 46, "Medium", DBLUE), 1000, t, D * 0.8)

def s_fast(fr, t, D):
    show(fr, pill("FASTING BLOOD SUGAR", BLUE, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr); clock(d, 300, 500, 130, "8+ hours", t)
    d.text((760, 450), "Nothing to eat", font=font("Bold", 42), fill=RED, anchor="mm")
    d.text((760, 520), "Plain water is OK", font=font("Bold", 42), fill=GREEN, anchor="mm")
    fire("pop", 0.3)
    if t > D * 0.3:
        fire("pop", D * 0.3); fire("pop", D * 0.42); fire("boom", D * 0.55)
        rows = [("Below 100", "Normal", GREEN), ("100 – 125", "Prediabetes", ORANGE), ("126 or more", "May be diabetes", RED)]
        k = 1 + int((t - D * 0.3) / (D * 0.12)); bands(d, 760, rows[:min(3, k)])
    show(fr, text_el("mg/dL (ADA criteria)", 32, "Medium", GREY), 1160, t, D * 0.6)

def s_pp(fr, t, D):
    show(fr, pill("PP (POST-MEAL) SUGAR", GREEN, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr); plate(d, 300, 520); clock(d, 790, 500, 120, "2 hours", t, GREEN)
    d.text((540, 520), "+", font=font("Bold", 90), fill=GREY, anchor="mm"); fire("pop", 0.3)
    show(fr, card("Exactly 2 hours from the START of the meal", GREEN, "1", size=36), 760, t, D * 0.2)
    show(fr, card("Eat your usual, normal meal", BLUE, "2", size=40), 895, t, D * 0.35)
    fire("pop", D * 0.2); fire("pop", D * 0.35)
    pop(fr, box_text("Usually below 140 mg/dL is normal", GREEN, 42), 540, 1080, t, D * 0.55, "ding")
    show(fr, text_el("Lab ranges may vary slightly", 36, "Medium", GREY), 1200, t, D * 0.7)

def s_gtt(fr, t, D):
    show(fr, pill("GTT (GLUCOSE TOLERANCE TEST)", ORANGE, size=44), 230, t, 0.1)
    d = ImageDraw.Draw(fr); tube(d, 180, 470); glass(d, 540, 470, t); clock(d, 890, 450, 95, "2 hrs", t, ORANGE)
    d.text((340, 470), "›", font=font("Bold", 90), fill=GREY, anchor="mm"); d.text((720, 470), "›", font=font("Bold", 90), fill=GREY, anchor="mm")
    fire("pop", 0.3)
    show(fr, text_el("Fasting sample, 75 g glucose, test at 2 hrs", 40, color=DBLUE), 690, t, D * 0.12)
    if t > D * 0.3:
        fire("pop", D * 0.3); fire("pop", D * 0.4); fire("boom", D * 0.5)
        rows = [("Below 140", "Normal", GREEN), ("140 – 199", "Prediabetes", ORANGE), ("200 or more", "Diabetes", RED)]
        k = 1 + int((t - D * 0.3) / (D * 0.1)); bands(d, 800, rows[:min(3, k)])
    pop(fr, box_text("Don't eat, sit quietly during the 2 hours", BLUE, 40), 540, 1260, t, D * 0.75, "ding")

def s_preg(fr, t, D):
    show(fr, pill("SUGAR TEST IN PREGNANCY", PINK, size=46), 230, t, 0.1)
    put(fr, MOM, 270, 560, 0.6); d = ImageDraw.Draw(fr); glass(d, 790, 480, t); fire("pop", 0.3)
    show(fr, text_el("DIPSI test (used in India)", 48, color=PINK), 800, t, D * 0.12)
    show(fr, card("75 g glucose, fasting NOT needed", ORANGE, "1", size=40), 910, t, D * 0.25)
    show(fr, card("2 hours later: 140 or more = GDM", RED, "2", size=40), 1045, t, D * 0.42)
    show(fr, card("First visit, again at 24–28 weeks", BLUE, "3", size=40), 1180, t, D * 0.6)
    fire("pop", D * 0.25); fire("pop", D * 0.42); fire("pop", D * 0.6)
    show(fr, text_el("GDM = diabetes in pregnancy", 36, "Medium", GREY), 1320, t, D * 0.75)

def s_who(fr, t, D):
    show(fr, pill("WHO SHOULD TEST?", GREEN, size=48), 230, t, 0.1)
    ground(fr, 230, 640, 260); put(fr, MOM, 230, 470, 0.5)
    ground(fr, 540, 640, 220); put(fr, DAD, 540, 470, 0.7)
    ground(fr, 850, 640, 260); put(fr, ELDER["happy"], 850, 470, 0.5)
    items = [("Everyone above 30 years", BLUE, "1"), ("Diabetes in the family", PURPLE, "2"), ("Overweight or high BP", RED, "3"),
             ("PCOD", PINK, "4"), ("Thirst, frequent urine, tiredness", ORANGE, "5")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.08 + 0.12 * i)); show(fr, card(txt, c, m, size=38), 720 + i * 128, t, D * (0.08 + 0.12 * i))
    pop(fr, box_text("One report isn't final: doctors confirm with a repeat test", TEAL, 36), 540, 1450, t, D * 0.78, "ding")

SC = [(s_hook, "navy"), (s_india, "light"), (s_three, "light"), (s_fast, "light"), (s_pp, "light"),
      (s_gtt, "light"), (s_preg, "light"), (s_who, "light"), (close_scene("When did you last test sugar?", DATE), "light")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        D = [13, 12, 12, 16, 14, 20, 20, 19, 30]; tests = [(0, .9), (1, .95), (2, .95), (3, .95), (4, .95), (5, .95), (6, .95), (7, .95), (8, .9)]
        ims = []
        for si, p in tests:
            fn, bg = SC[si]; d = D[si]; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((360, 640)))
        s = Image.new("RGB", (360 * 5, 640 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 360, (i // 5) * 640))
        s.save("sheet.png")
    else: run(SC, "/tmp/sg_", "Friday_Health_Tips_9Oct2026_Blood_Sugar_Hindi.mp4")
