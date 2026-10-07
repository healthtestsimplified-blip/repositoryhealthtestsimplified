import math, sys
from cbc_cartoon import run
from chromo_cartoon import PINK, SKYB
from gene_cartoon import person
from dmarker_cartoon import LAV
from wes_cartoon import DAD
from lft_cartoon2 import *
from hts_close import close_scene

TOPIC = "MEMORY & BRAIN HEALTH"
BRAIN = (244, 143, 177); BRAIN_D = (216, 96, 140)

def elder_sprite(mood="confused"):
    w, h = 320, 560
    im = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    S = lambda *v: [x * SS for x in v]
    d.rounded_rectangle(S(120, 380, 150, 530), 12 * SS, fill=(90, 90, 100)); d.rounded_rectangle(S(170, 380, 200, 530), 12 * SS, fill=(90, 90, 100))
    d.ellipse(S(105, 515, 160, 545), fill=(60, 40, 40)); d.ellipse(S(160, 515, 215, 545), fill=(60, 40, 40))
    d.rounded_rectangle(S(95, 220, 225, 395), 34 * SS, fill=(141, 110, 99))          # kurta
    d.line(S(105, 240, 70, 360), fill=SKIN, width=20 * SS); d.line(S(215, 240, 260, 330), fill=SKIN, width=20 * SS)
    d.line(S(262, 330, 262, 540), fill=(120, 80, 50), width=10 * SS)                   # walking stick
    d.rectangle(S(145, 195, 175, 225), fill=SKIN)
    d.ellipse(S(95, 75, 225, 205), fill=SKIN)
    d.chord(S(92, 70, 228, 170), 180, 360, fill=(225, 225, 230))                      # grey hair
    d.ellipse(S(88, 120, 110, 160), fill=(225, 225, 230)); d.ellipse(S(210, 120, 232, 160), fill=(225, 225, 230))
    for ex in (135, 185):                                                              # glasses
        d.ellipse(S(ex - 20, 118, ex + 20, 152), outline=(60, 60, 70), width=4 * SS)
        d.ellipse(S(ex - 6, 128, ex + 6, 142), fill=(30, 30, 40))
    d.line(S(155, 135, 165, 135), fill=(60, 60, 70), width=4 * SS)
    d.line(S(125, 170, 195, 170), fill=(225, 225, 230), width=10 * SS)                # moustache
    if mood == "happy": d.arc(S(140, 168, 180, 195), 20, 160, fill=(170, 60, 60), width=5 * SS)
    else: d.arc(S(145, 182, 175, 200), 200, 340, fill=(170, 60, 60), width=5 * SS)
    return im.resize((w, h), Image.LANCZOS)
ELDER = {"confused": elder_sprite("confused"), "happy": elder_sprite("happy")}

def brain(d, cx, cy, s, col=BRAIN, dark=BRAIN_D, fade=0.0, face="happy"):
    d.ellipse((cx - s, cy - 0.72 * s, cx + s, cy + 0.72 * s), fill=col)
    d.line((cx, cy - 0.7 * s, cx, cy + 0.68 * s), fill=dark, width=max(4, int(s * 0.05)))
    for k in range(6):
        for sg in (-1, 1):
            x = cx + sg * (0.25 + 0.12 * (k % 3)) * s; y = cy - 0.45 * s + k * 0.17 * s
            d.arc((x - 0.25 * s, y - 0.12 * s, x + 0.25 * s, y + 0.12 * s), 200 if sg < 0 else -20, 340 if sg < 0 else 160, fill=dark, width=max(3, int(s * 0.04)))
    if fade > 0:   # damaged patches
        for (fx, fy) in ((-0.5, -0.2), (0.45, 0.1), (-0.2, 0.35), (0.25, -0.4)):
            r = 0.18 * s * fade
            d.ellipse((cx + fx * s - r, cy + fy * s - r, cx + fx * s + r, cy + fy * s + r), fill=(200, 190, 200))
    ey = cy + 0.05 * s
    for ex in (-0.28, 0.28):
        d.ellipse((cx + ex * s - 0.1 * s, ey - 0.1 * s, cx + ex * s + 0.1 * s, ey + 0.1 * s), fill=WHITE)
        d.ellipse((cx + ex * s - 0.045 * s, ey - 0.045 * s, cx + ex * s + 0.045 * s, ey + 0.045 * s), fill=(30, 30, 40))
    if face == "happy": d.arc((cx - 0.18 * s, ey + 0.08 * s, cx + 0.18 * s, ey + 0.32 * s), 20, 160, fill=(150, 40, 70), width=max(3, int(s * 0.04)))
    else: d.arc((cx - 0.15 * s, ey + 0.2 * s, cx + 0.15 * s, ey + 0.36 * s), 200, 340, fill=(150, 40, 70), width=max(3, int(s * 0.04)))

def qmarks(fr, cx, cy, t, n=3):
    d = ImageDraw.Draw(fr)
    for k in range(n):
        a = t * 1.5 + k * 2.1
        x = cx + 150 * math.cos(a); y = cy - 60 + 40 * math.sin(a * 1.3)
        d.text((x, y), "?", font=font("Bold", 80), fill=(255, 214, 0), anchor="mm")

def mri(d, cx, cy, s, t):
    d.ellipse((cx - s, cy - s, cx + s, cy + s), fill=(220, 228, 240), outline=(150, 165, 190), width=10)
    d.ellipse((cx - 0.55 * s, cy - 0.55 * s, cx + 0.55 * s, cy + 0.55 * s), fill=(40, 55, 90))
    d.rounded_rectangle((cx - 1.3 * s, cy + 0.15 * s, cx + 1.3 * s, cy + 0.3 * s), 8, fill=(170, 180, 200))
    for k in range(3):
        r = 0.3 * s + ((t * 60 + k * 30) % 90)
        d.arc((cx - r, cy - r, cx + r, cy + r), 200, 340, fill=(0, 170, 200), width=5)

def tube(d, x, y):
    d.rounded_rectangle((x - 34, y - 95, x + 34, y + 95), 26, fill=WHITE, outline=(150, 160, 175), width=6)
    d.rounded_rectangle((x - 28, y - 20, x + 28, y + 89), 22, fill=(200, 30, 45)); d.rectangle((x - 40, y - 105, x + 40, y - 70), fill=(120, 60, 200))

def clipboard(d, x, y):
    d.rounded_rectangle((x - 70, y - 90, x + 70, y + 95), 16, fill=(141, 110, 99))
    d.rounded_rectangle((x - 58, y - 75, x + 58, y + 85), 10, fill=WHITE)
    d.rounded_rectangle((x - 30, y - 100, x + 30, y - 75), 8, fill=GREY)
    for k in range(4):
        d.line((x - 40, y - 45 + k * 34, x + 40, y - 45 + k * 34), fill=(180, 190, 205), width=6)
        d.text((x - 48, y - 45 + k * 34), "✓" if k < 3 else "", font=font("Bold", 1), fill=GREEN)

# ---------------- scenes ----------------
def a_hook(fr, t, D):
    rays(fr, 540, 900, t, (180, 140, 255), a=40)
    show(fr, pill(TOPIC, PURPLE, size=36), 230, t, 0.1)
    put(fr, ELDER["confused"], 540, 1400 + 5 * math.sin(t * 2), 0.95); qmarks(fr, 540, 1150, t)
    pop(fr, white_text("Forgetting keys is normal.", 70), 540, 480, t, 0.3, "pop")
    pop(fr, white_text("Forgetting the way home?", 70, color=YEL), 540, 640, t, D * 0.25, "boom")
    pop(fr, box_text("It may be Alzheimer's. Watch till the end", GREEN, 42), 540, 860, t, D * 0.6, "whoosh")

def a_what(fr, t, D):
    show(fr, pill("WHAT IS ALZHEIMER'S?", PURPLE, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr); f = max(0, min(1, (t - D * 0.3) / (D * 0.3)))
    brain(d, 540, 560, 250, fade=f, face="sad" if f > 0.5 else "happy"); fire("pop", 0.3); fire("zap", D * 0.3)
    show(fr, text_el("The most common cause of dementia", 48, color=DBLUE), 850, t, D * 0.15)
    show(fr, card("Brain cells slowly get damaged", PINK, "1", size=40), 980, t, D * 0.35)
    show(fr, card("Memory, thinking & daily work suffer", ORANGE, "2", size=40), 1115, t, D * 0.5)
    fire("pop", D * 0.35); fire("pop", D * 0.5)
    pop(fr, box_text("It is NOT a normal part of ageing", RED, 44), 540, 1300, t, D * 0.72, "ding")

def a_signs(fr, t, D):
    show(fr, pill("WARNING SIGNS", ORANGE, size=48), 230, t, 0.1)
    put(fr, ELDER["confused"], 860, 560, 0.62); qmarks(fr, 860, 470, t, 2)
    d = ImageDraw.Draw(fr); brain(d, 300, 520, 170, fade=0.6, face="sad")
    items = [("Forgets recent events", PURPLE, "1"), ("Asks the same question again", BLUE, "2"),
             ("Gets lost in familiar places", RED, "3"), ("Trouble with money or daily tasks", TEAL, "4"),
             ("Changes in mood or behaviour", ORANGE, "5")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.1 + 0.15 * i)); show(fr, card(txt, c, m, size=38), 820 + i * 130, t, D * (0.1 + 0.15 * i))

def a_india(fr, t, D):
    show(fr, pill("DEMENTIA IN INDIA", RED, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    for k in range(100):
        if t < 0.3 + k * 0.012: break
        r, c = divmod(k, 20); x = 85 + c * 48; y = 360 + r * 62
        col = RED if k in (3, 17, 31, 46, 58, 72, 89) else (196, 205, 220)
        d.ellipse((x - 11, y - 26, x + 11, y - 4), fill=col); d.rounded_rectangle((x - 16, y - 2, x + 16, y + 26), 10, fill=col)
    fire("whoosh", 0.3)
    pop(fr, stroke_text("About 7 in 100", 110, RED, WHITE, 9), 540, 760, t, D * 0.3, "boom")
    show(fr, text_el("people over 60 in India have dementia", 46, color=DBLUE), 880, t, D * 0.35)
    show(fr, card("About 88 lakh people", PURPLE, "!", size=42), 1010, t, D * 0.5)
    show(fr, card("More common in women & in villages", PINK, "♀", size=40), 1145, t, D * 0.65)
    fire("pop", D * 0.5); fire("pop", D * 0.65)
    show(fr, text_el("Source: LASI-DAD national study, 2023", 30, "Medium", GREY), 1290, t, D * 0.7)

def a_how(fr, t, D):
    show(fr, pill("IS THERE ONE ALZHEIMER'S TEST?", BLUE, size=44), 230, t, 0.1)
    pop(fr, stroke_text("NO!", 130, RED, WHITE, 10), 540, 400, t, 0.3, "boom")
    show(fr, text_el("Doctors check in 3 ways", 52, color=DBLUE), 540, t, D * 0.2)
    d = ImageDraw.Draw(fr)
    data = [("Memory tests", "e.g. MMSE", PURPLE, D * 0.3), ("Blood tests", "find treatable causes", RED, D * 0.45), ("Brain scan", "MRI or CT", TEAL, D * 0.6)]
    for i, (a, b, c, tin) in enumerate(data):
        fire("pop", tin)
        if t < tin: continue
        x = 190 + i * 350
        d.rounded_rectangle((x - 160, 640, x + 160, 1080), 30, fill=WHITE, outline=c, width=7)
        if i == 0: clipboard(d, x, 790)
        elif i == 1: tube(d, x, 790)
        else: mri(d, x, 790, 95, t)
        d.text((x, 960), a, font=font("Bold", 40), fill=c, anchor="mm")
        d.text((x, 1015), b, font=font("Medium", 28), fill=GREY, anchor="mm")
    show(fr, text_el("Usually by a neurologist or psychiatrist", 40, "Medium", GREEN), 1170, t, D * 0.78)

def a_blood(fr, t, D):
    show(fr, pill("WHY BLOOD TESTS?", RED, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr); tube(d, 220, 470); brain(d, 760, 470, 170, face="happy"); fire("pop", 0.3)
    show(fr, text_el("Some memory problems have TREATABLE causes", 44, color=DBLUE), 700, t, D * 0.12)
    items = [("Low vitamin B12", RED, "1"), ("Thyroid problems", PINK, "2"), ("Sugar (diabetes)", ORANGE, "3"),
             ("Anaemia (CBC)", PURPLE, "4"), ("Kidney or liver problems", TEAL, "5")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.2 + 0.11 * i)); show(fr, card(txt, c, m, size=38), 830 + i * 120, t, D * (0.2 + 0.11 * i))
    pop(fr, box_text("Treating them can improve memory", GREEN, 42), 540, 1480, t, D * 0.8, "ding")

def a_scan(fr, t, D):
    show(fr, pill("BRAIN SCAN", TEAL, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr); mri(d, 540, 540, 220, t); fire("whoosh", 0.3)
    show(fr, card("MRI / CT: rules out stroke, tumour, fluid", TEAL, "1", size=38), 860, t, D * 0.2)
    show(fr, card("Can show shrinking of the brain", PURPLE, "2", size=40), 995, t, D * 0.4)
    show(fr, card("Sometimes: PET scan or spinal fluid test", BLUE, "3", size=38), 1130, t, D * 0.6)
    fire("pop", D * 0.2); fire("pop", D * 0.4); fire("pop", D * 0.6)

def a_blood2(fr, t, D):
    show(fr, pill("NOW AVAILABLE: A BLOOD TEST", PURPLE, size=44), 230, t, 0.1)
    d = ImageDraw.Draw(fr); tube(d, 230, 470); brain(d, 760, 460, 160, face="happy"); fire("ding", 0.3)
    show(fr, text_el("pTau217 / Amyloid ratio blood test", 46, color=DBLUE), 660, t, D * 0.08)
    show(fr, card("Blood sample, report in about 48 hours", GREEN, "1", size=38), 770, t, D * 0.16)
    show(fr, card("For adults 50+ WITH memory symptoms", ORANGE, "2", size=38), 895, t, D * 0.26)
    fire("pop", D * 0.16); fire("pop", D * 0.26)
    rows = [("POSITIVE", "High chance of Alzheimer's changes", GREEN), ("GREY ZONE", "More tests may be needed", ORANGE),
            ("NEGATIVE", "Very low chance", BLUE)]
    for i, (a, b, c) in enumerate(rows):
        tin = D * (0.4 + 0.1 * i); fire("pop", tin)
        if t < tin: continue
        y = 1030 + i * 125
        d.rounded_rectangle((70, y, W - 70, y + 105), 26, fill=WHITE, outline=c, width=6)
        d.text((230, y + 52), a, font=font("Bold", 38), fill=c, anchor="mm")
        d.text((680, y + 52), b, font=font("Medium", 32), fill=GREY, anchor="mm")
    pop(fr, box_text("Not a screening test. Your doctor reads it with other tests.", RED, 38), 540, 1505, t, D * 0.75, "boom")

def a_protect(fr, t, D):
    show(fr, pill("PROTECT YOUR BRAIN", GREEN, size=48), 230, t, 0.1)
    put(fr, ELDER["happy"], 250, 560, 0.62); d = ImageDraw.Draw(fr); brain(d, 780, 470, 150, face="happy"); sparkles(fr, 780, 470, 200, t, 6)
    pop(fr, stroke_text("Up to 45%", 100, GREEN, WHITE, 8), 540, 790, t, D * 0.15, "boom")
    show(fr, text_el("of dementia may be prevented or delayed (Lancet, 2024)", 36, "Medium", DBLUE), 880, t, D * 0.2)
    items = [("Control BP, sugar & cholesterol", RED, "1"), ("Treat hearing & vision loss", BLUE, "2"),
             ("Walk daily, no smoking", ORANGE, "3"), ("Stay social, keep learning", PURPLE, "4")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.35 + 0.13 * i)); show(fr, card(txt, c, m, size=38), 990 + i * 130, t, D * (0.35 + 0.13 * i))

SC = [(a_hook, "purple"), (a_what, "light"), (a_signs, "light"), (a_india, "light"), (a_how, "light"),
      (a_blood, "light"), (a_scan, "light"), (a_blood2, "light"), (a_protect, "light"),
      (close_scene("Elder at home forgetting things?", TOPIC), "light")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        D = [14, 15, 14, 12, 14, 17, 13, 32, 19, 26]; tests = [(0, .9), (1, .95), (2, .95), (3, .95), (4, .95), (5, .95), (6, .95), (7, .95), (8, .95), (9, .9)]
        ims = []
        for si, p in tests:
            fn, bg = SC[si]; d = D[si]; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((360, 640)))
        s = Image.new("RGB", (360 * 5, 640 * 2), "white"); ims = ims[4:]
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 360, (i // 5) * 640))
        s.save("sheet.png")
    else: run(SC, "/tmp/alz2_", "Alzheimers_Test_Hindi.mp4")
