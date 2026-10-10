import math, sys
from cbc_cartoon import run
from alz_cartoon import brain
from ecg_cartoon import heart
from eeg_cartoon import head, monitor, WIRE, SKIN
from lft_cartoon2 import *
from chromo_cartoon import PINK
from hts_close import close_scene

TOPIC = "SLEEP & BREATHING"
NIGHT = (35, 45, 85); BLANKET = (126, 87, 194); PILLOW = (236, 239, 241); AIR = (129, 212, 250)

def sleeper(d, cx, cy, s, eyes="closed", mask=False, sensors=False):
    """Person lying in bed, head on the left."""
    d.rounded_rectangle((cx - 2.6 * s, cy + 0.35 * s, cx + 2.6 * s, cy + 0.75 * s), 20, fill=(141, 110, 99))
    d.rounded_rectangle((cx - 2.5 * s, cy - 0.45 * s, cx - 1.3 * s, cy + 0.4 * s), 30, fill=PILLOW)
    d.rounded_rectangle((cx - 1.25 * s, cy - 0.5 * s, cx + 2.5 * s, cy + 0.45 * s), 40, fill=BLANKET)
    pts = head(d, cx - 1.75 * s, cy - 0.15 * s, 0.55 * s, eyes=eyes, leads=sensors)
    if mask:
        hx, hy = cx - 1.75 * s, cy - 0.15 * s
        d.rounded_rectangle((hx - 0.25 * s, hy + 0.12 * s, hx + 0.25 * s, hy + 0.45 * s), 18, fill=(225, 245, 254), outline=(2, 136, 209), width=5)
        d.line((hx + 0.25 * s, hy + 0.3 * s, hx + 0.9 * s, hy + 0.2 * s, cx - 0.3 * s, cy - 0.7 * s), fill=(2, 136, 209), width=10)
        d.rounded_rectangle((cx - 0.6 * s, cy - 1.1 * s, cx + 0.2 * s, cy - 0.65 * s), 14, fill=(176, 190, 197))
        d.text((cx - 0.2 * s, cy - 0.88 * s), "CPAP", font=font("Bold", int(0.2 * s)), fill=WHITE, anchor="mm")
    return pts

def zzz(d, x, y, t, col=WHITE, n=3, big=1.0):
    for k in range(n):
        ph = (t * 0.8 + k / n) % 1
        d.text((x + ph * 120 * big, y - ph * 160 * big), "Z", font=font("Bold", int((40 + ph * 50) * big)), fill=col, anchor="mm")

def airway(d, cx, cy, h, closed=0.0, t=0.0):
    """Simple throat tube; closed 0..1 narrows it with the tongue."""
    w = 110
    d.rounded_rectangle((cx - w - 30, cy - h / 2, cx + w + 30, cy + h / 2), 50, fill=(255, 205, 210))
    gap = w * (1 - 0.92 * closed)
    d.rounded_rectangle((cx - gap / 2 - 10, cy - h / 2 + 20, cx + gap / 2 + 10, cy + h / 2 - 20), 30, fill=(255, 255, 255))
    d.ellipse((cx - w - 60 + closed * 120, cy - 70, cx - 20 + closed * 120, cy + 70), fill=(229, 115, 115))
    if closed < 0.5:
        for k in range(4):
            yy = cy + h / 2 - ((t * 200 + k * h / 4) % h)
            d.polygon([(cx, yy - 25), (cx - 18, yy + 5), (cx + 18, yy + 5)], fill=AIR)
    else:
        d.line((cx - 50, cy - 50, cx + 50, cy + 50), fill=RED, width=14); d.line((cx - 50, cy + 50, cx + 50, cy - 50), fill=RED, width=14)

# ---------------- scenes ----------------
def s_hook(fr, t, D):
    show(fr, pill(TOPIC, PURPLE, size=40), 230, t, 0.1)
    d = ImageDraw.Draw(fr); d.ellipse((820, 960, 960, 1100), fill=YEL)
    for (a, b, r) in ((860, 1000, 14), (915, 1040, 18), (870, 1060, 10)): d.ellipse((a - r, b - r, a + r, b + r), fill=(240, 200, 60))
    sleeper(d, 560, 1250, 150); zzz(d, 430, 1100, t, YEL, big=1.4)
    pop(fr, white_text("Loud snoring at night?", 72), 540, 470, t, 0.3, "pop")
    pop(fr, white_text("Tired all day?", 76, color=YEL), 540, 610, t, D * 0.3, "boom")
    pop(fr, box_text("It could be SLEEP APNOEA", RED, 50), 540, 800, t, D * 0.6, "whoosh")

def s_what(fr, t, D):
    show(fr, pill("WHAT IS SLEEP APNOEA?", BLUE, size=46), 230, t, 0.1)
    d = ImageDraw.Draw(fr); c = 1.0 if (t % 3) > 1.5 and t > D * 0.2 else 0.0
    airway(d, 300, 520, 300, 0.0, t); airway(d, 780, 520, 300, 1.0, t)
    d.text((300, 710), "Awake: open", font=font("Bold", 38), fill=GREEN, anchor="mm")
    d.text((780, 710), "Apnoea: blocked", font=font("Bold", 38), fill=RED, anchor="mm")
    fire("pop", 0.3)
    show(fr, card("Throat closes again and again in sleep", BLUE, "1", size=37), 850, t, D * 0.2)
    show(fr, card("Breathing stops 10 seconds or more", RED, "2", size=38), 985, t, D * 0.4)
    show(fr, card("Then a gasp or jerk to breathe again", ORANGE, "3", size=37), 1120, t, D * 0.55)
    fire("pop", D * 0.2); fire("boom", D * 0.4); fire("pop", D * 0.55)
    pop(fr, box_text("Often the PARTNER notices it first", PURPLE, 40), 540, 1300, t, D * 0.75, "ding")

def s_india(fr, t, D):
    show(fr, pill("SLEEP APNOEA IN INDIA", RED, size=46), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    for k in range(100):
        if t < 0.3 + k * 0.012: break
        r, c = divmod(k, 20); x = 85 + c * 48; y = 360 + r * 62
        col = RED if k in (2, 9, 15, 23, 34, 41, 48, 57, 66, 78, 91) else (196, 205, 220)
        d.ellipse((x - 11, y - 26, x + 11, y - 4), fill=col); d.rounded_rectangle((x - 16, y - 2, x + 16, y + 26), 10, fill=col)
    fire("whoosh", 0.3)
    pop(fr, stroke_text("About 11 in 100", 104, RED, WHITE, 9), 540, 760, t, D * 0.25, "boom")
    show(fr, text_el("adults in India may have it", 46, color=DBLUE), 880, t, D * 0.3)
    show(fr, card("About 10 crore people", PURPLE, "!", size=42), 1010, t, D * 0.45)
    show(fr, card("Most of them don't know it", ORANGE, "?", size=42), 1145, t, D * 0.65)
    fire("pop", D * 0.45); fire("pop", D * 0.65)
    show(fr, text_el("Source: AIIMS New Delhi study, 2023", 30, "Medium", GREY), 1290, t, D * 0.7)

def s_signs(fr, t, D):
    show(fr, pill("WARNING SIGNS", ORANGE, size=48), 230, t, 0.1)
    items = [("Loud snoring", PURPLE, "1"), ("Breathing pauses / choking sounds", RED, "2"), ("Morning headache", ORANGE, "3"),
             ("Very sleepy in the daytime", BLUE, "4"), ("Poor focus, irritable mood", TEAL, "5")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.08 + 0.12 * i)); show(fr, card(txt, c, m, size=40), 400 + i * 132, t, D * (0.08 + 0.12 * i))
    pop(fr, box_text("Not everyone who snores has apnoea", GREEN, 40), 540, 1120, t, D * 0.75, "ding")

def s_risk(fr, t, D):
    show(fr, pill("WHO IS AT MORE RISK?", PURPLE, size=46), 230, t, 0.1)
    items = [("Extra weight or a thick neck", ORANGE, "1"), ("Older age", BLUE, "2"), ("Runs in the family", PINK, "3"),
             ("Alcohol and smoking", RED, "4"), ("Large tonsils", TEAL, "5"), ("Sleeping on the back", PURPLE, "6")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.08 + 0.12 * i)); show(fr, card(txt, c, m, size=40), 390 + i * 128, t, D * (0.08 + 0.12 * i))
    show(fr, text_el("Children and young people can have it too", 38, "Medium", GREY), 1180, t, D * 0.85)

def s_risky(fr, t, D):
    show(fr, pill("WHY TREAT IT?", RED, size=50), 230, t, 0.1)
    d = ImageDraw.Draw(fr); heart(d, 300, 500, 140, t, bpm=110, face="sad"); brain(d, 780, 500, 140, face="sad"); fire("boom", 0.3)
    items = [("High blood pressure", RED, "1"), ("Heart disease & irregular beat", ORANGE, "2"), ("Stroke", PURPLE, "3"),
             ("Road accidents from daytime sleepiness", BLUE, "4")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.12 + 0.17 * i)); show(fr, card(txt, c, m, size=37), 760 + i * 132, t, D * (0.12 + 0.17 * i))

def s_test(fr, t, D):
    show(fr, pill("THE TEST: SLEEP STUDY", GREEN, size=46), 230, t, 0.1)
    d = ImageDraw.Draw(fr); d.rounded_rectangle((40, 330, W - 40, 680), 40, fill=NIGHT)
    pts = sleeper(d, 420, 520, 110, sensors=True); monitor(d, 760, 380, 1010, 560, t, rows=3)
    d.text((885, 620), "SpO2 96%", font=font("Bold", 34), fill=(105, 240, 174), anchor="mm"); fire("pop", 0.3)
    show(fr, text_el("Polysomnography (PSG)", 52, color=DBLUE), 760, t, D * 0.12)
    show(fr, card("Sensors while you sleep at night", BLUE, "1", size=40), 880, t, D * 0.2)
    show(fr, card("Breathing, oxygen, heartbeat, brain waves", PURPLE, "2", size=35), 1015, t, D * 0.35)
    show(fr, card("Painless", GREEN, "3", size=42), 1150, t, D * 0.55)
    show(fr, card("Some people: home test, doctor decides", ORANGE, "4", size=37), 1285, t, D * 0.7)
    for k in (0.2, 0.35, 0.55, 0.7): fire("pop", D * k)

def s_report(fr, t, D):
    show(fr, pill("PREPARE & READ THE REPORT", ORANGE, size=42), 230, t, 0.1)
    show(fr, card("Test day: no tea, coffee or alcohol", RED, "!", size=38), 360, t, 0.3)
    show(fr, card("Sleeping pills: only if doctor says", PURPLE, "!", size=38), 490, t, D * 0.15)
    fire("pop", 0.3); fire("pop", D * 0.15)
    show(fr, text_el("AHI = pauses per hour of sleep", 44, color=DBLUE), 630, t, D * 0.35)
    d = ImageDraw.Draw(fr)
    rows = [("Below 5", "Normal", GREEN), ("5 – 14", "Mild", YEL), ("15 – 29", "Moderate", ORANGE), ("30 or more", "Severe", RED)]
    for i, (a, b, c) in enumerate(rows):
        tin = D * (0.45 + 0.1 * i); fire("pop", tin)
        if t < tin: continue
        y = 710 + i * 118
        d.rounded_rectangle((110, y, W - 110, y + 100), 26, fill=WHITE, outline=c, width=7)
        d.text((330, y + 50), a, font=font("Bold", 44), fill=DBLUE, anchor="mm")
        d.text((750, y + 50), b, font=font("Bold", 44), fill=c if c != YEL else (200, 160, 0), anchor="mm")
    show(fr, text_el("Doctor reads it with your symptoms", 38, "Medium", GREY), 1220, t, D * 0.85)

def s_treat(fr, t, D):
    show(fr, pill("GOOD NEWS: IT'S TREATABLE", GREEN, size=44), 230, t, 0.1)
    d = ImageDraw.Draw(fr); d.rounded_rectangle((40, 330, W - 40, 680), 40, fill=NIGHT)
    sleeper(d, 560, 560, 120, mask=t > D * 0.5)
    if t > D * 0.5: sparkles(fr, 340, 520, 160, t, 5)
    else: zzz(d, 400, 430, t, YEL)
    items = [("Lose extra weight", GREEN, "1"), ("Stop alcohol & smoking", RED, "2"), ("Sleep on your side", BLUE, "3"),
             ("CPAP machine if doctor advises", PURPLE, "4")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.1 + 0.16 * i)); show(fr, card(txt, c, m, size=40), 770 + i * 132, t, D * (0.1 + 0.16 * i))
    show(fr, text_el("CPAP: gentle air through a mask keeps the throat open", 34, "Medium", GREY), 1310, t, D * 0.75)

SC = [(s_hook, "purple"), (s_what, "light"), (s_india, "light"), (s_signs, "light"), (s_risk, "light"),
      (s_risky, "light"), (s_test, "light"), (s_report, "light"), (s_treat, "light"),
      (close_scene("Does anyone at home snore loudly?", TOPIC), "light")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        D = [14] * 10
        ims = []
        for si in range(10):
            fn, bg = SC[si]; d = D[si]; p = 0.95; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((360, 640)))
        s = Image.new("RGB", (360 * 5, 640 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 360, (i // 5) * 640))
        s.save("sheet.png")
    else: run(SC, "/tmp/slp_", "Sleep_Study_Apnoea_Hindi.mp4")
