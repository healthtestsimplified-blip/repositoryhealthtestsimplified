import math, sys
from cbc_cartoon import run
from alz_cartoon import brain, ELDER
from dmarker_cartoon import MOM
from wes_cartoon import DAD, KID
from lft_cartoon2 import *
from hts_close import close_scene

TOPIC = "BRAIN & NERVES"
SKIN = (255, 213, 170); HAIR = (60, 45, 40); WIRE = [(229, 57, 53), (30, 136, 229), (67, 160, 71), (251, 140, 0), (142, 36, 170), (0, 150, 136)]
SCREEN = (20, 30, 50)

def head(d, cx, cy, s, eyes="open", leads=True):
    """Side-friendly front head with an electrode cap; wires go to (wx, wy) if given."""
    d.ellipse((cx - s, cy - 1.1 * s, cx + s, cy + 0.9 * s), fill=SKIN)
    d.chord((cx - s, cy - 1.15 * s, cx + s, cy + 0.6 * s), 180, 360, fill=HAIR)
    ey = cy + 0.15 * s
    for ex in (-0.35, 0.35):
        if eyes == "open":
            d.ellipse((cx + ex * s - 0.1 * s, ey - 0.1 * s, cx + ex * s + 0.1 * s, ey + 0.1 * s), fill=(30, 30, 40))
        else:
            d.arc((cx + ex * s - 0.13 * s, ey - 0.08 * s, cx + ex * s + 0.13 * s, ey + 0.1 * s), 20, 160, fill=(30, 30, 40), width=max(3, int(s * 0.05)))
    d.arc((cx - 0.22 * s, cy + 0.3 * s, cx + 0.22 * s, cy + 0.55 * s), 20, 160, fill=(170, 60, 60), width=max(3, int(s * 0.05)))
    if not leads: return []
    pts = []
    for k in range(9):
        a = math.radians(200 + k * 17.5)
        px, py = cx + 0.82 * s * math.cos(a), cy - 0.2 * s + 0.82 * s * math.sin(a)
        pts.append((px, py))
    pts += [(cx, cy - 0.55 * s), (cx - 0.4 * s, cy - 0.45 * s), (cx + 0.4 * s, cy - 0.45 * s)]
    for k, (px, py) in enumerate(pts):
        r = 0.09 * s
        d.ellipse((px - r, py - r, px + r, py + r), fill=WIRE[k % 6], outline=WHITE, width=3)
    return pts

def wires(d, pts, tx, ty):
    for k, (px, py) in enumerate(pts):
        mx = (px + tx) / 2 + 40 * math.sin(k)
        for i in range(12):
            a = i / 12; b = (i + 1) / 12
            def q(u): return ((1 - u) ** 2 * px + 2 * (1 - u) * u * mx + u * u * tx, (1 - u) ** 2 * py + 2 * (1 - u) * u * (py - 80) + u * u * ty)
            d.line((q(a), q(b)), fill=WIRE[k % 6], width=4)

def monitor(d, x0, y0, x1, y1, t, kind="normal", rows=4):
    d.rounded_rectangle((x0 - 14, y0 - 14, x1 + 14, y1 + 14), 26, fill=(70, 80, 100))
    d.rounded_rectangle((x0, y0), 18, fill=SCREEN) if False else d.rounded_rectangle((x0, y0, x1, y1), 18, fill=SCREEN)
    h = (y1 - y0) / rows
    for r in range(rows):
        yc = y0 + h * (r + 0.5); col = WIRE[r % 6]; prev = None
        for x in range(int(x0) + 10, int(x1) - 10, 4):
            u = (x - x0) / 40 + t * 3 + r
            if kind == "spike" and r in (1, 2) and int(u) % 7 == 0:
                y = yc - h * 0.42 * math.sin((u % 1) * math.pi)
            else:
                y = yc + h * 0.18 * (math.sin(u * 2.2) * 0.6 + math.sin(u * 5.3 + r) * 0.4)
            if prev: d.line((prev, (x, y)), fill=col, width=3)
            prev = (x, y)

def bed(d, cx, cy, w):
    d.rounded_rectangle((cx - w / 2, cy, cx + w / 2, cy + 60), 20, fill=(144, 202, 249))
    d.rounded_rectangle((cx - w / 2, cy + 60, cx - w / 2 + 30, cy + 170), 8, fill=GREY)
    d.rounded_rectangle((cx + w / 2 - 30, cy + 60, cx + w / 2, cy + 170), 8, fill=GREY)

# ---------------- scenes ----------------
def e_hook(fr, t, D):
    rays(fr, 540, 900, t, (120, 180, 255), a=40)
    show(fr, pill(TOPIC, PURPLE, size=40), 230, t, 0.1)
    d = ImageDraw.Draw(fr); brain(d, 540, 1250, 230, face="sad" if t < D * 0.6 else "happy")
    for k in range(3):
        a = t * 4 + k * 2.1
        d.line((540 + 260 * math.cos(a), 1250 + 180 * math.sin(a), 540 + 300 * math.cos(a + 0.2), 1250 + 210 * math.sin(a + 0.2)), fill=YEL, width=10)
    pop(fr, white_text("Fainting? Fits?", 80), 540, 470, t, 0.3, "pop")
    pop(fr, white_text("Blanking out for a few seconds?", 56, color=YEL), 540, 630, t, D * 0.3, "boom")
    pop(fr, box_text("The doctor may ask for an EEG", GREEN, 46), 540, 830, t, D * 0.6, "whoosh")

def e_what(fr, t, D):
    show(fr, pill("WHAT IS AN EEG?", BLUE, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr); pts = head(d, 300, 560, 170); wires(d, pts, 640, 520); monitor(d, 600, 380, 1000, 680, t); fire("pop", 0.3)
    show(fr, text_el("Electro-Encephalo-Gram", 54, color=DBLUE), 820, t, D * 0.15)
    show(fr, card("Small sensors stuck on the scalp", BLUE, "1", size=40), 950, t, D * 0.3)
    show(fr, card("They record the brain's electric waves", PURPLE, "2", size=38), 1085, t, D * 0.5)
    fire("pop", D * 0.3); fire("pop", D * 0.5)
    pop(fr, box_text("Brain cells talk using tiny electric signals", TEAL, 38), 540, 1260, t, D * 0.7, "ding")

def e_safe(fr, t, D):
    show(fr, pill("DOES IT HURT?", GREEN, size=50), 230, t, 0.1)
    pop(fr, stroke_text("NO!", 150, GREEN, WHITE, 10), 540, 430, t, 0.3, "pop")
    d = ImageDraw.Draw(fr); pts = head(d, 540, 760, 160)
    if t > D * 0.3: sparkles(fr, 540, 720, 230, t, 6)
    show(fr, card("Painless: sensors only LISTEN", GREEN, "1", size=40), 1010, t, D * 0.3)
    show(fr, card("No electric current goes into the body", BLUE, "2", size=37), 1145, t, D * 0.5)
    fire("pop", D * 0.3); fire("pop", D * 0.5)

def e_when(fr, t, D):
    show(fr, pill("WHEN IS IT DONE?", ORANGE, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr); brain(d, 540, 470, 150); fire("pop", 0.3)
    items = [("Fits / seizures / epilepsy", RED, "1"), ("Fainting or unexplained spells", ORANGE, "2"),
             ("After a head injury", BLUE, "3"), ("Some sleep problems", PURPLE, "4"), ("Very sick patients in ICU", TEAL, "5")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.12 + 0.14 * i)); show(fr, card(txt, c, m, size=38), 690 + i * 128, t, D * (0.12 + 0.14 * i))
    show(fr, text_el("Only if your doctor advises", 42, "Medium", GREEN), 1340, t, D * 0.85)

def e_prep(fr, t, D):
    show(fr, pill("BEFORE THE TEST", PURPLE, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr); head(d, 540, 560, 140, leads=False)
    for k in range(6):
        bx = 300 + k * 96; by = 365 + 18 * math.sin(t * 3 + k)
        d.ellipse((bx - 18, by - 18, bx + 18, by + 18), outline=(100, 180, 255), width=4)
    fire("pop", 0.3)
    items = [("Wash hair: clean and dry", BLUE, "1"), ("No oil, gel or conditioner", RED, "2"),
             ("Don't stop medicines on your own", ORANGE, "3"), ("Eat normally", GREEN, "4")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.12 + 0.17 * i)); show(fr, card(txt, c, m, size=40), 760 + i * 132, t, D * (0.12 + 0.17 * i))
    show(fr, text_el("Medicines: as your doctor advises", 40, "Medium", GREY), 1320, t, D * 0.85)

def e_sleep(fr, t, D):
    show(fr, pill("SLEEP EEG", BLUE, size=50), 230, t, 0.1)
    d = ImageDraw.Draw(fr); d.rounded_rectangle((60, 340, W - 60, 700), 40, fill=(40, 50, 90))
    d.ellipse((800, 380, 900, 480), fill=YEL); d.ellipse((830, 370, 930, 470), fill=(40, 50, 90))
    head(d, 400, 560, 110, eyes="closed")
    for k in range(3):
        d.text((560 + k * 60, 470 - k * 50), "z", font=font("Bold", 50 + k * 15), fill=WHITE, anchor="mm")
    fire("pop", 0.3)
    show(fr, card("May need less sleep the night before", PURPLE, "1", size=40), 800, t, D * 0.2)
    show(fr, card("Do NOT drive after this test", RED, "2", size=40), 935, t, D * 0.45)
    show(fr, card("Bring someone along with you", GREEN, "3", size=40), 1070, t, D * 0.65)
    fire("pop", D * 0.2); fire("boom", D * 0.45); fire("pop", D * 0.65)

def e_during(fr, t, D):
    show(fr, pill("DURING THE TEST", TEAL, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr); bed(d, 330, 600, 440); pts = head(d, 230, 530, 85, eyes="closed")
    wires(d, pts, 640, 470); monitor(d, 640, 360, 1010, 620, t, rows=4); fire("pop", 0.3)
    show(fr, card("Lie down, eyes closed, relax", BLUE, "1", size=40), 860, t, D * 0.15)
    show(fr, card("Recording: about 20–40 minutes", ORANGE, "2", size=40), 995, t, D * 0.35)
    show(fr, card("Deep breathing / flashing light", PURPLE, "3", size=40), 1130, t, D * 0.55)
    fire("pop", D * 0.15); fire("pop", D * 0.35); fire("pop", D * 0.55)
    show(fr, text_el("These can bring out hidden changes", 40, "Medium", GREY), 1270, t, D * 0.7)
    if t > D * 0.55 and int(t * 6) % 2 == 0:
        d.ellipse((470, 380, 530, 440), fill=YEL)

def e_report(fr, t, D):
    show(fr, pill("THE REPORT", ORANGE, size=50), 230, t, 0.1)
    d = ImageDraw.Draw(fr); monitor(d, 120, 360, 960, 640, t, kind="spike", rows=4); fire("pop", 0.3)
    show(fr, text_el("A NORMAL EEG does not rule out epilepsy", 44, color=RED), 760, t, D * 0.2); fire("boom", D * 0.2)
    show(fr, card("Fits may not show during a short test", BLUE, "1", size=38), 880, t, D * 0.35)
    show(fr, card("Repeat / sleep / long or video EEG", PURPLE, "2", size=38), 1015, t, D * 0.5)
    fire("pop", D * 0.35); fire("pop", D * 0.5)
    pop(fr, box_text("Doctor decides with your symptoms", GREEN, 42), 540, 1200, t, D * 0.7, "ding")

SC = [(e_hook, "purple"), (e_what, "light"), (e_safe, "light"), (e_when, "light"), (e_prep, "light"),
      (e_sleep, "light"), (e_during, "light"), (e_report, "light"),
      (close_scene("Anyone in your family had an EEG?", TOPIC), "light")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        D = [12, 16, 11, 19, 20, 14, 19, 16, 30]
        ims = []
        for si in range(9):
            fn, bg = SC[si]; d = D[si]; p = 0.95; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((360, 640)))
        s = Image.new("RGB", (360 * 5, 640 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 360, (i // 5) * 640))
        s.save("sheet.png")
    else: run(SC, "/tmp/eeg_", "EEG_Test_Hindi.mp4")
