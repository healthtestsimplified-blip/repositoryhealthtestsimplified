import math, sys, random
from cbc_cartoon import run
from chromo_cartoon import x_shape, PINK, SKYB
from dna_cartoon import helix, BASE_COL
from gene_cartoon import person, mutation
from dmarker_cartoon import MOM, LAV
from lft_cartoon2 import *

GOLD = (255, 193, 7)

def kid_sprite(mood="sad", shirt=(255, 167, 38)):
    w, h = 300, 470
    im = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    S = lambda *v: [x * SS for x in v]
    d.rounded_rectangle(S(110, 330, 140, 440), 12 * SS, fill=(40, 70, 140)); d.rounded_rectangle(S(160, 330, 190, 440), 12 * SS, fill=(40, 70, 140))
    d.ellipse(S(95, 425, 150, 455), fill=(60, 40, 40)); d.ellipse(S(150, 425, 205, 455), fill=(60, 40, 40))
    d.rounded_rectangle(S(90, 200, 210, 345), 30 * SS, fill=shirt)
    d.line(S(100, 220, 65, 320), fill=SKIN, width=20 * SS); d.line(S(200, 220, 235, 320), fill=SKIN, width=20 * SS)
    d.rectangle(S(135, 175, 165, 205), fill=SKIN)
    d.ellipse(S(85, 60, 215, 190), fill=SKIN)
    d.pieslice(S(80, 50, 220, 160), 180, 360, fill=(40, 25, 20))
    d.ellipse(S(120, 115, 134, 131), fill=(30, 30, 40)); d.ellipse(S(166, 115, 180, 131), fill=(30, 30, 40))
    d.ellipse(S(105, 138, 125, 152), fill=(255, 160, 170)); d.ellipse(S(175, 138, 195, 152), fill=(255, 160, 170))
    if mood == "happy": d.arc(S(128, 135, 172, 168), 20, 160, fill=(170, 60, 60), width=5 * SS)
    else: d.arc(S(132, 150, 168, 172), 200, 340, fill=(170, 60, 60), width=5 * SS)
    return im.resize((w, h), Image.LANCZOS)

KID = {"sad": kid_sprite("sad"), "happy": kid_sprite("happy")}
DAD = kid_sprite("happy", SKYB)

def genome_grid(p, t):
    """100 squares = whole DNA; 2 gold squares = exome."""
    im = Image.new("RGBA", (W, 640), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    s, g = 52, 10; x0 = (W - (10 * s + 9 * g)) // 2
    gold = {(3, 6), (7, 2)}
    n = int(100 * min(1, max(0, p * 2)))
    for k in range(n):
        r, c = divmod(k, 10); x, y = x0 + c * (s + g), 20 + r * (s + g)
        hl = (r, c) in gold and p > 0.6
        col = GOLD if hl else (205, 214, 228)
        if hl:
            pul = 6 + 4 * math.sin(t * 6)
            d.rounded_rectangle((x - pul, y - pul, x + s + pul, y + s + pul), 14, fill=(255, 236, 160))
        d.rounded_rectangle((x, y, x + s, y + s), 10, fill=col)
    return im

def lab_flow(p, t):
    im = Image.new("RGBA", (W, 330), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    # tube
    if p > 0:
        d.rounded_rectangle((110, 40, 190, 260), 30, fill=WHITE, outline=(150, 160, 175), width=6)
        d.rounded_rectangle((116, 120, 184, 254), 26, fill=(200, 30, 45)); d.rectangle((104, 30, 196, 70), fill=(120, 60, 200))
        d.text((150, 300), "Blood", font=font("Bold", 34), fill=RED, anchor="mm")
    if p > 0.33:
        d.text((290, 150), "›", font=font("Bold", 110), fill=GREY, anchor="mm")
        d.rounded_rectangle((360, 50, 700, 260), 30, fill=(40, 55, 90))
        d.rounded_rectangle((385, 75, 675, 200), 16, fill=(10, 20, 40))
        seq = "ATGCGTACCGATTGCAATGC"; off = int(t * 8)
        for i in range(9):
            ch = seq[(i + off) % len(seq)]
            d.text((410 + i * 32, 138), ch, font=font("Bold", 38), fill=BASE_COL[ch], anchor="mm")
        for k in range(3): d.ellipse((400 + k * 40, 220, 425 + k * 40, 245), fill=(120, 230, 140) if (int(t * 4) + k) % 3 else (60, 90, 70))
        d.text((530, 300), "Sequencer", font=font("Bold", 34), fill=DBLUE, anchor="mm")
    if p > 0.66:
        d.text((770, 150), "›", font=font("Bold", 110), fill=GREY, anchor="mm")
        d.rounded_rectangle((830, 60, 1010, 200), 16, fill=(40, 55, 90)); d.rounded_rectangle((845, 75, 995, 185), 10, fill=(225, 240, 255))
        for k in range(4): d.line((860, 95 + k * 24, 860 + 60 + 50 * ((k * 37) % 3), 95 + k * 24), fill=TEAL, width=8)
        d.rectangle((900, 200, 940, 235), fill=(40, 55, 90)); d.rounded_rectangle((860, 232, 980, 250), 8, fill=(40, 55, 90))
        d.text((920, 300), "Computer", font=font("Bold", 34), fill=DBLUE, anchor="mm")
    return im

def zoom_table(p):
    rows = [("Karyotype", "Chromosome count & big changes", 1, PURPLE),
            ("Microarray", "Small missing or extra pieces", 2, BLUE),
            ("Gene panel", "A few chosen genes", 3, TEAL),
            ("Whole exome", "~20,000 genes, letter by letter", 4, GREEN)]
    rh = 190; im = Image.new("RGBA", (W, rh * 4 + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, (a, b, z, c) in enumerate(rows):
        if p < i / 4: break
        y = i * rh; last = i == 3
        d.rounded_rectangle((60, y, W - 60, y + rh - 22), 28, fill=blend(c, (255, 255, 255), 0.88) if last else WHITE, outline=c, width=8 if last else 4)
        d.text((100, y + 50), a, font=font("Bold", 46), fill=c, anchor="lm")
        d.text((100, y + 115), b, font=font("Medium", 34), fill=DBLUE, anchor="lm")
        for k in range(4):   # zoom level dots
            x = 790 + k * 52
            d.ellipse((x, y + 30, x + 36, y + 66), fill=c if k < z else (220, 226, 236))
        d.text((868, y + 112), "detail", font=font("Medium", 28), fill=GREY, anchor="mm")
    return im

def result_boxes(fr, t, D, items, y0=360, step=230):
    d = ImageDraw.Draw(fr)
    for i, (a, b, c) in enumerate(items):
        tin = 0.4 + i * D * 0.2; fire("pop", tin)
        if t < tin: break
        y = y0 + i * step
        d.rounded_rectangle((70, y, W - 70, y + 200), 30, fill=WHITE, outline=c, width=8)
        d.text((W / 2, y + 62), a, font=font("Bold", 52), fill=c, anchor="mm")
        d.text((W / 2, y + 140), b, font=font("Medium", 34), fill=GREY, anchor="mm")

# ---------------- scenes ----------------
def w_hook(fr, t, D):
    rays(fr, 540, 900, t, (120, 160, 255), a=40)
    helix(fr, 540, 1550, 1000, 80, t, alpha=110)
    put(fr, KID["sad"], 540, 1320 + 6 * math.sin(t * 2), 0.8)
    pop(fr, white_text("Child keeps having fits? Late to walk or talk?", 72), 540, 470, t, 0.1, "boom")
    pop(fr, white_text("All reports normal?", 66, color=YEL), 540, 720, t, D * 0.25, "whoosh")
    pop(fr, box_text("The answer may be in the genes. Watch till the end!", GREEN, 40), 540, 900, t, D * 0.55, "pop")

def w_what(fr, t, D):
    show(fr, pill("WHAT IS THE EXOME?", PURPLE, size=48), 230, t, 0.1)
    show(fr, text_el("Your DNA = a giant book of 3 billion letters", 44, color=DBLUE), 340, t, 0.3)
    fire("whoosh", 0.3); fr.alpha_composite(genome_grid((t - 0.5) / (D * 0.5), t), (0, 440))
    fire("ding", D * 0.35)
    show(fr, card("EXOME = just 1–2%: the protein recipes", GOLD, "★", size=38), 1130, t, D * 0.4)
    pop(fr, box_text("Most known disease-causing mistakes hide here!", RED, 40), 540, 1330, t, D * 0.7, "boom")

def w_how(fr, t, D):
    show(fr, pill("HOW IS IT DONE?", BLUE, size=48), 230, t, 0.1)
    p = (t - 0.3) / (D * 0.45)
    for k in range(3): fire("pop", 0.3 + k * D * 0.15)
    fr.alpha_composite(lab_flow(p, t), (0, 380))
    show(fr, text_el("Reads ~20,000 genes, letter by letter", 44, color=DBLUE), 790, t, D * 0.35)
    fire("zap", D * 0.55)
    if t > D * 0.55: fr.alpha_composite(mutation(ease((t - D * 0.55) / (D * 0.25))), (0, 900))
    show(fr, card("Just a blood (or saliva) sample", GREEN, "✓", size=38), 1390, t, D * 0.8)

def w_who(fr, t, D):
    show(fr, pill("WHO MAY NEED IT?", ORANGE, size=48), 230, t, 0.1)
    ground(fr, 270, 690, 260); put(fr, KID["sad"], 270, 470, 0.75)
    ground(fr, 790, 690, 300); put(fr, DOC["idle"], 790, 460, 0.6)
    items = [("Delayed development or learning", PURPLE, "1"), ("Unexplained fits or muscle weakness", RED, "2"),
             ("Birth defects in many organs", BLUE, "3"), ("Unknown genetic illness in family", TEAL, "4"),
             ("All other tests gave no answer", ORANGE, "5")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.1 + 0.15 * i)); show(fr, card(txt, c, m, size=37), 760 + i * 130, t, D * (0.1 + 0.15 * i))

def w_compare(fr, t, D):
    show(fr, pill("GENETIC TESTS: HOW DEEP?", LAV, size=46), 230, t, 0.1)
    p = (t - 0.4) / (D * 0.75)
    for i in range(4): fire("pop", 0.4 + i / 4 * D * 0.75)
    fr.alpha_composite(zoom_table(p), (0, 420))
    show(fr, text_el("Screenshot this!", 44, "Bold", TEAL), 1270, t, D * 0.85)

def w_result(fr, t, D):
    show(fr, pill("READING THE REPORT", ORANGE, size=48), 230, t, 0.1)
    result_boxes(fr, t, D, [("POSITIVE", "Cause found", GREEN), ("NEGATIVE", "No cause found (genetic not ruled out)", BLUE),
                            ("VUS", "Change of uncertain meaning", ORANGE)])
    d = ImageDraw.Draw(fr)
    if t > D * 0.75:
        for k in range(3): person(d, 400 + k * 140, 1150, GREEN if k == 0 else (190, 200, 215), 1.0)
    fire("ding", D * 0.75)
    show(fr, text_el("About 1 in 3 families find an answer", 46, color=GREEN), 1290, t, D * 0.78)

def w_know(fr, t, D):
    show(fr, pill("GOOD TO KNOW", PURPLE, size=48), 230, t, 0.1)
    ground(fr, 540, 720, 600)
    put(fr, MOM, 330, 540, 0.55); put(fr, KID["happy"], 540, 600, 0.55); put(fr, DAD, 750, 530, 0.85)
    show(fr, pill("TRIO = child + both parents", GREEN, size=36), 800, t, 0.4); fire("pop", 0.4)
    items = [("Trio gives more reliable results", GREEN, "1"), ("Report in about 3–6 weeks", BLUE, "2"),
             ("Can't catch every change (e.g. Fragile X)", ORANGE, "3"), ("Genetic counselling before & after", PURPLE, "4")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.15 + 0.17 * i)); show(fr, card(txt, c, m, size=37), 920 + i * 132, t, D * (0.15 + 0.17 * i))

def w_benefit(fr, t, D):
    show(fr, pill("WHY AN ANSWER MATTERS", GREEN, size=46), 230, t, 0.1)
    ground(fr, 300, 720, 300); put(fr, KID["happy"], 300, 520, 0.8); sparkles(fr, 300, 470, 200, t, 6)
    ground(fr, 780, 720, 300); put(fr, DOC["idle"], 780, 500, 0.65)
    items = [("Ends years of running around", ORANGE, "1"), ("Right treatment & care plan", GREEN, "2"),
             ("Testing for other family members", BLUE, "3"), ("Options in the next pregnancy", PINK, "4")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.12 + 0.18 * i)); show(fr, card(txt, c, m, size=38), 820 + i * 135, t, D * (0.12 + 0.18 * i))

def w_close(fr, t, D):
    show(fr, big_logo(), 210, t, 0.2)
    fire("ding", 0.8); show(fr, box_text("Take any medicine only as advised by your doctor", GREEN, 42), 820, t, 0.8)
    show(fr, text_el("Had you heard of exome sequencing before?", 52, color=DBLUE), 1020, t, D * 0.4)
    show(fr, text_el("Share with a family who needs it!", 44, "Medium", GREY), 1180, t, D * 0.5)
    show(fr, pill("Follow Health Test Simplified", BLUE, size=40), 1320, t, D * 0.6)
    show(fr, text_el("For awareness only. Consult your doctor.", 30, "Regular", GREY), 1680, t, D * 0.7)

SC = [(w_hook, "navy"), (w_what, "light"), (w_how, "light"), (w_who, "light"), (w_compare, "light"),
      (w_result, "light"), (w_know, "light"), (w_benefit, "light"), (w_close, "light")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        D = [11, 16, 14, 15, 14, 17, 17, 12, 13]; tests = [(0, .8), (1, .95), (2, .95), (3, .95), (4, .95), (5, .95), (6, .95), (7, .95), (8, .9)]
        ims = []
        for si, p in tests:
            fn, bg = SC[si]; d = D[si]; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((360, 640)))
        s = Image.new("RGB", (360 * 5, 640 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 360, (i // 5) * 640))
        s.save("sheet.png")
    else: run(SC, "/tmp/wes_", "Whole_Exome_Sequencing_Hindi.mp4")
