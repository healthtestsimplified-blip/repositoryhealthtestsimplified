import json, math, subprocess, sys
from common import *

SS = 2
def blend(c1, c2, k): return tuple(int(a + (b - a) * k) for a, b in zip(c1, c2))

# ---------------- sprites (drawn at 2x, downsampled for smooth edges) ----------------
LIVER_PTS = [(-1.0,-0.2),(-0.88,-0.55),(-0.55,-0.72),(-0.05,-0.68),(0.45,-0.55),(0.9,-0.42),(1.08,-0.25),
             (0.95,-0.08),(0.55,0.12),(0.1,0.42),(-0.35,0.6),(-0.72,0.52),(-0.95,0.28)]
def liver_sprite(color, mood):
    w, h, s = 620, 460, 260
    im = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx, cy = w * SS / 2, h * SS / 2 + 30 * SS
    P = lambda x, y: (cx + x * s * SS, cy + y * s * SS)
    d.polygon([P(*p) for p in LIVER_PTS], fill=color)
    d.polygon([P(x * 0.9 - 0.05, y * 0.85 - 0.06) for x, y in LIVER_PTS[:7]] + [P(0.3, -0.3), P(-0.6, -0.2)],
              fill=blend(color, (255, 255, 255), 0.12))
    for ex in (-0.5, -0.12):
        d.ellipse([*P(ex - 0.12, -0.38), *P(ex + 0.12, -0.12)], fill=WHITE)
        py = -0.22 if mood != "sad" else -0.2
        d.ellipse([*P(ex - 0.05, py - 0.06), *P(ex + 0.07, py + 0.06)], fill=(30, 30, 40))
    if mood == "happy":
        d.arc([*P(-0.48, -0.12), *P(-0.12, 0.18)], 20, 160, fill=(80, 10, 10), width=9 * SS)
        for ex in (-0.68, 0.06): d.ellipse([*P(ex - 0.07, -0.08), *P(ex + 0.07, 0.02)], fill=(255, 150, 150))
    elif mood == "worried":
        d.arc([*P(-0.42, 0.0), *P(-0.18, 0.2)], 200, 340, fill=(80, 10, 10), width=8 * SS)
        d.line([*P(-0.62, -0.46), *P(-0.4, -0.42)], fill=(60, 20, 20), width=7 * SS)
        d.line([*P(-0.22, -0.42), *P(0.0, -0.46)], fill=(60, 20, 20), width=7 * SS)
    else:  # sad / sick
        d.arc([*P(-0.44, 0.02), *P(-0.16, 0.26)], 200, 340, fill=(80, 10, 10), width=9 * SS)
        d.line([*P(-0.62, -0.5), *P(-0.4, -0.42)], fill=(60, 20, 20), width=7 * SS)
        d.line([*P(-0.22, -0.42), *P(0.0, -0.5)], fill=(60, 20, 20), width=7 * SS)
        d.polygon([P(0.22, -0.62), P(0.17, -0.48), P(0.27, -0.48)], fill=(120, 190, 255))
        d.ellipse([*P(0.15, -0.53), *P(0.29, -0.4)], fill=(120, 190, 255))
    return im.resize((w, h), Image.LANCZOS)

SKIN = (236, 190, 150); NAVY = (30, 40, 70)
def doctor_sprite(pose="idle", step=0):
    w, h = 440, 600
    im = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    S = lambda *v: [x * SS for x in v]
    lo = [(0, 0), (14, -14)][step] if pose == "walk" else (0, 0)
    d.rounded_rectangle(S(108 + lo[0], 430, 140 + lo[0], 555), 10 * SS, fill=NAVY)
    d.rounded_rectangle(S(160 + lo[1], 430, 192 + lo[1], 555), 10 * SS, fill=NAVY)
    d.ellipse(S(96 + lo[0], 540, 150 + lo[0], 575), fill=(20, 20, 20))
    d.ellipse(S(150 + lo[1], 540, 204 + lo[1], 575), fill=(20, 20, 20))
    # coat
    d.rounded_rectangle(S(68, 215, 232, 450), 30 * SS, fill=WHITE, outline=(200, 210, 225), width=3 * SS)
    d.polygon(S(125, 215, 175, 215, 150, 300), fill=(66, 133, 244))
    d.line(S(150, 300, 150, 445), fill=(200, 210, 225), width=3 * SS)
    d.rounded_rectangle(S(170, 330, 215, 360), 6 * SS, fill=(66, 133, 244))  # pocket badge
    # stethoscope
    d.arc(S(108, 180, 192, 290), 20, 160, fill=(90, 90, 100), width=6 * SS)
    d.line(S(118, 268, 112, 330), fill=(90, 90, 100), width=6 * SS)
    d.ellipse(S(98, 322, 126, 350), fill=(160, 160, 170), outline=(90, 90, 100), width=4 * SS)
    # arms
    d.rounded_rectangle(S(42, 230, 76, 395), 16 * SS, fill=WHITE, outline=(200, 210, 225), width=3 * SS)
    d.ellipse(S(40, 385, 78, 423), fill=SKIN)
    if pose == "aim":
        d.rounded_rectangle(S(205, 245, 330, 280), 16 * SS, fill=WHITE, outline=(200, 210, 225), width=3 * SS)
        d.ellipse(S(318, 243, 352, 282), fill=SKIN)
        d.rounded_rectangle(S(330, 225, 425, 300), 16 * SS, fill=BLUE)
        d.rounded_rectangle(S(345, 238, 410, 287), 10 * SS, fill=(120, 230, 140))
        d.line(S(352, 262, 365, 262, 372, 248, 382, 276, 390, 262, 404, 262), fill=(20, 110, 40), width=3 * SS)
    else:
        d.rounded_rectangle(S(224, 230, 258, 395), 16 * SS, fill=WHITE, outline=(200, 210, 225), width=3 * SS)
        d.ellipse(S(222, 385, 260, 423), fill=SKIN)
    # head
    d.rectangle(S(135, 190, 165, 225), fill=SKIN)
    d.ellipse(S(88, 85, 212, 209), fill=SKIN)
    d.pieslice(S(84, 74, 216, 180), 180, 360, fill=(40, 30, 30))
    d.rectangle(S(86, 120, 100, 150), fill=(40, 30, 30)); d.rectangle(S(200, 120, 214, 150), fill=(40, 30, 30))
    d.ellipse(S(80, 135, 96, 165), fill=SKIN); d.ellipse(S(204, 135, 220, 165), fill=SKIN)
    d.ellipse(S(122, 140, 138, 158), fill=(30, 30, 40)); d.ellipse(S(162, 140, 178, 158), fill=(30, 30, 40))
    d.line(S(116, 130, 140, 127), fill=(40, 30, 30), width=4 * SS); d.line(S(160, 127, 184, 130), fill=(40, 30, 30), width=4 * SS)
    d.arc(S(126, 155, 174, 190), 20, 160, fill=(150, 60, 60), width=5 * SS)
    # head mirror
    d.line(S(96, 106, 204, 106), fill=(120, 120, 130), width=5 * SS)
    d.ellipse(S(132, 84, 168, 120), fill=(225, 235, 245), outline=(120, 120, 130), width=4 * SS)
    return im.resize((w, h), Image.LANCZOS)

def angry_face(d, cx, cy, r, S):
    d.line(S(cx - 0.55 * r, cy - 0.45 * r, cx - 0.12 * r, cy - 0.25 * r), fill=(20, 20, 20), width=7 * SS)
    d.line(S(cx + 0.12 * r, cy - 0.25 * r, cx + 0.55 * r, cy - 0.45 * r), fill=(20, 20, 20), width=7 * SS)
    for ex in (-0.32, 0.32):
        d.ellipse(S(cx + ex * r - 0.14 * r, cy - 0.22 * r, cx + ex * r + 0.14 * r, cy + 0.06 * r), fill=WHITE)
        d.ellipse(S(cx + ex * r - 0.06 * r, cy - 0.12 * r, cx + ex * r + 0.06 * r, cy + 0.0 * r), fill=(200, 0, 0))
    pts = []
    for k in range(7):
        pts += [cx - 0.4 * r + k * 0.8 * r / 6, cy + (0.3 if k % 2 else 0.42) * r]
    d.line(S(*pts), fill=(20, 20, 20), width=6 * SS)

def villain_sprite(kind):
    w = h = 300
    im = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    S = lambda *v: [x * SS for x in v]
    if kind == "fat":
        for a in range(0, 360, 40):
            d.ellipse(S(150 + 95 * math.cos(math.radians(a)) - 45, 160 + 80 * math.sin(math.radians(a)) - 45,
                        150 + 95 * math.cos(math.radians(a)) + 45, 160 + 80 * math.sin(math.radians(a)) + 45), fill=(250, 205, 60))
        d.ellipse(S(55, 75, 245, 245), fill=(252, 215, 80))
        for (x, y) in [(90, 110), (205, 200), (110, 215)]: d.ellipse(S(x - 12, y - 12, x + 12, y + 12), fill=(255, 235, 150))
        angry_face(d, 150, 160, 95, S)
    elif kind == "virus":
        for a in range(0, 360, 30):
            ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
            d.line(S(150 + 80 * ca, 150 + 80 * sa, 150 + 125 * ca, 150 + 125 * sa), fill=(60, 130, 40), width=10 * SS)
            d.ellipse(S(150 + 125 * ca - 15, 150 + 125 * sa - 15, 150 + 125 * ca + 15, 150 + 125 * sa + 15), fill=(200, 60, 120))
        d.ellipse(S(60, 60, 240, 240), fill=(110, 185, 60))
        for (x, y) in [(95, 100), (200, 190), (180, 90)]: d.ellipse(S(x - 10, y - 10, x + 10, y + 10), fill=(80, 150, 40))
        angry_face(d, 150, 150, 90, S)
    else:  # bottle
        d.rounded_rectangle(S(122, 10, 178, 40), 8 * SS, fill=(200, 40, 40))
        d.rectangle(S(128, 38, 172, 100), fill=(110, 60, 25))
        d.rounded_rectangle(S(80, 90, 220, 290), 40 * SS, fill=(130, 70, 30))
        d.rounded_rectangle(S(90, 105, 115, 270), 12 * SS, fill=(170, 105, 55))
        d.rectangle(S(86, 215, 214, 262), fill=(245, 235, 210))
        d.text((150 * SS, 238 * SS), "XXX", font=font("Bold", 30 * SS), fill=(130, 70, 30), anchor="mm")
        angry_face(d, 150, 160, 70, S)
    return im.resize((w, h), Image.LANCZOS)

def mini_label(text, col, size=30):
    f = font("Bold", size); tw = f.getlength(text)
    im = Image.new("RGBA", (int(tw + 50), size + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, tw + 49, size + 29), (size + 30) // 2, fill=col)
    d.text(((tw + 50) / 2, (size + 30) / 2), text, font=f, fill=WHITE, anchor="mm")
    return im

LIVER_OK = (183, 58, 58); LIVER_SICK = (205, 165, 70)
LV = {"happy": liver_sprite(LIVER_OK, "happy"), "worried": liver_sprite(blend(LIVER_OK, LIVER_SICK, 0.5), "worried"),
      "sick": liver_sprite(LIVER_SICK, "sad")}
DOC = {"idle": doctor_sprite("idle"), "aim": doctor_sprite("aim"),
       "w0": doctor_sprite("walk", 0), "w1": doctor_sprite("walk", 1)}
VIL = {k: villain_sprite(k) for k in ("fat", "virus", "bottle")}
VLAB = {"fat": mini_label("FATTY LIVER", (214, 160, 0)), "virus": mini_label("HEPATITIS VIRUS", (70, 150, 40)),
        "bottle": mini_label("ALCOHOL", (130, 70, 30))}

# ---------------- frame helpers ----------------
def ease(x): x = max(0, min(1, x)); return 1 - (1 - x) ** 3
def put(fr, spr, cx, cy, sc=1.0, a=1.0, flip=False):
    if sc <= 0.02 or a <= 0.01: return
    s = spr
    if flip: s = s.transpose(Image.FLIP_LEFT_RIGHT)
    if sc != 1.0: s = s.resize((max(1, int(s.width * sc)), max(1, int(s.height * sc))), Image.BILINEAR)
    if a < 1:
        s = s.copy(); al = s.getchannel("A").point(lambda v: int(v * a)); s.putalpha(al)
    fr.alpha_composite(s, (int(cx - s.width / 2), int(cy - s.height / 2)))
def show(fr, im, y, t, tin):
    p = (t - tin) / 0.5
    if p <= 0: return
    e = ease(p); layer = im
    if e < 1:
        layer = im.copy(); layer.putalpha(layer.getchannel("A").point(lambda v: int(v * e)))
    fr.alpha_composite(layer, (0, int(y + (1 - e) * 50)))
def burst(fr, cx, cy, r, a):
    lay = Image.new("RGBA", fr.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    pts = []
    for k in range(20):
        rr = r if k % 2 == 0 else r * 0.45; ang = math.pi * k / 10
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=(255, 200, 40, int(230 * a)))
    d.ellipse((cx - r * 0.35, cy - r * 0.35, cx + r * 0.35, cy + r * 0.35), fill=(255, 255, 255, int(255 * a)))
    fr.alpha_composite(lay)
def sparkles(fr, cx, cy, R, t, n=8, col=(255, 215, 0)):
    d = ImageDraw.Draw(fr)
    for k in range(n):
        ang = t * 1.5 + k * 2 * math.pi / n; rr = R + 20 * math.sin(t * 3 + k)
        x, y = cx + rr * math.cos(ang), cy + rr * math.sin(ang) * 0.8; s = 14 + 6 * math.sin(t * 5 + k)
        d.polygon([(x, y - s), (x + s * 0.3, y - s * 0.3), (x + s, y), (x + s * 0.3, y + s * 0.3),
                   (x, y + s), (x - s * 0.3, y + s * 0.3), (x - s, y), (x - s * 0.3, y - s * 0.3)], fill=col)
def beam(fr, x0, y0, x1, y1, t, col=(120, 230, 140)):
    lay = Image.new("RGBA", fr.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    a = int(110 + 60 * math.sin(t * 10)); spread = 150
    d.polygon([(x0, y0 - 14), (x0, y0 + 14), (x1, y1 + spread), (x1, y1 - spread)], fill=(*col, a))
    for k in range(4):
        yy = y1 - spread + ((t * 400 + k * 75) % (2 * spread))
        d.line((x1 - 40, yy, x1 + 40, yy), fill=(255, 255, 255, 180), width=5)
    fr.alpha_composite(lay)
def ground(fr, cx, y, w):
    d = ImageDraw.Draw(fr); d.ellipse((cx - w / 2, y - 18, cx + w / 2, y + 18), fill=(205, 222, 240))
def liver_mix(k):  # 0 healthy -> 1 sick
    return LV["happy"] if k < 0.33 else (LV["worried"] if k < 0.7 else LV["sick"])

# ---------------- scenes: fn(fr, t, dur) ----------------
def s_intro(fr, t, D):
    show(fr, pill("LIVER FUNCTION TEST (LFT)", RED, size=46), 230, t, 0.1)
    ground(fr, 540, 900, 520)
    put(fr, LV["happy"], 540, 690 + 18 * math.sin(t * 3))
    sparkles(fr, 540, 690, 330, t, 6, (255, 200, 60))
    show(fr, text_el("Meet your Liver", 70, color=DBLUE), 980, t, 0.8)
    show(fr, text_el("The body's silent hero", 50, "Medium", GREEN), 1080, t, 1.4)
    for i, (txt, c) in enumerate([("Digests food", BLUE), ("Cleans toxins", TEAL), ("Stores energy", ORANGE)]):
        show(fr, pill(txt, c, size=40), 1240 + i * 120, t, D * (0.38 + 0.14 * i))

VPOS = {"fat": (845, 470), "virus": (870, 790), "bottle": (845, 1090)}
def draw_villains(fr, t, xoff=0.0, scales=None, labels=True):
    for i, k in enumerate(("fat", "virus", "bottle")):
        x, y = VPOS[k]; sc = 1.0 if scales is None else scales[k]
        x += xoff; y += 12 * math.sin(t * 4 + i * 2)
        put(fr, VIL[k], x, y, 0.72 * sc)
        if labels and sc > 0.6: put(fr, VLAB[k], x, y + 118 * sc, sc)

def s_attack(fr, t, D):
    show(fr, pill("THE ENEMIES ATTACK!", RED, size=46), 230, t, 0.1)
    k = ease((t / D - 0.25) / 0.6)
    ground(fr, 330, 930, 460)
    shake = 6 * math.sin(t * 40) * k
    put(fr, liver_mix(k), 330 + shake, 720, 0.8)
    xoff = (1 - ease(t / (0.35 * D))) * 600
    draw_villains(fr, t, xoff)
    if t > 0.4 * D:
        d = ImageDraw.Draw(fr)
        for i, k2 in enumerate(("fat", "virus", "bottle")):
            if int(t * 6 + i) % 2 == 0:
                x, y = VPOS[k2]; pts = [(x - 120, y)]
                for j in range(1, 6): pts.append((x - 120 - j * 55, y + (720 - y) * j / 6 + (25 if j % 2 else -25)))
                d.line(pts, fill=RED, width=8)
    show(fr, text_el("The liver suffers in silence", 54, color=DBLUE), 1290, t, 0.6 * D)
    show(fr, text_el("No early symptoms", 46, "Medium", RED), 1390, t, 0.7 * D)

def s_symptoms(fr, t, D):
    show(fr, pill("WARNING SIGNS COME LATE", ORANGE, size=44), 230, t, 0.1)
    ground(fr, 540, 820, 420)
    put(fr, LV["sick"], 540 + 4 * math.sin(t * 30), 640, 0.85)
    for i, txt in enumerate(["Tiredness", "Loss of appetite", "Yellow eyes (jaundice)", "Dark urine"]):
        show(fr, card(txt, ORANGE, "!"), 900 + i * 125, t, D * (0.15 + 0.17 * i))

def s_doctor(fr, t, D):
    show(fr, pill("THE DOCTOR ARRIVES!", GREEN, size=46), 230, t, 0.1)
    ground(fr, 780, 920, 440); ground(fr, 270, 1000, 340)
    put(fr, LV["sick"], 780, 720, 0.75)
    p = t / (0.4 * D)
    if p < 1:
        x = -220 + 490 * ease(p) if False else -220 + 490 * p
        put(fr, DOC["w0" if int(t * 6) % 2 else "w1"], x, 720 + 6 * abs(math.sin(t * 9)))
    else:
        put(fr, DOC["aim"], 270, 720)
        if t > 0.5 * D:
            g = 0.5 + 0.5 * math.sin(t * 8)
            lay = Image.new("RGBA", fr.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
            d.ellipse((330 + 107 - 70, 682 - 70, 330 + 107 + 70, 682 + 70), fill=(120, 230, 140, int(90 * g)))
            fr.alpha_composite(lay)
    show(fr, text_el("His weapon:", 50, "Medium", GREY), 1170, t, 0.45 * D)
    show(fr, text_el("Liver Function Test (LFT)", 66, color=BLUE), 1250, t, 0.55 * D)
    show(fr, text_el("A simple blood test", 44, "Medium", GREEN), 1420, t, 0.7 * D)

def s_scan(fr, t, D):
    show(fr, pill("WHAT LFT CHECKS", BLUE, size=46), 230, t, 0.1)
    ground(fr, 790, 800, 400); ground(fr, 230, 880, 320)
    put(fr, DOC["aim"], 230, 600, 0.9)
    beam(fr, 230 + 175 * 0.9, 560, 760, 610, t)
    put(fr, LV["sick"], 790, 620, 0.7)
    rows = [("SGPT & SGOT: damage alarm", RED), ("Bilirubin: jaundice check", ORANGE),
            ("Albumin: liver strength", GREEN), ("ALP: bile flow", PURPLE if 'PURPLE' in globals() else TEAL)]
    for i, (txt, c) in enumerate(rows):
        show(fr, card(txt, c, "●"), 960 + i * 125, t, D * (0.14 + 0.19 * i))

def s_who(fr, t, D):
    show(fr, pill("WHO SHOULD GET TESTED?", ORANGE, size=44), 230, t, 0.1)
    ground(fr, 250, 770, 300); ground(fr, 760, 720, 360)
    put(fr, DOC["idle"], 250, 560, 0.75)
    put(fr, LV["worried"], 760, 580, 0.6 + 0.02 * math.sin(t * 3))
    items = [("Drink alcohol regularly", (130, 70, 30), "!"), ("Overweight or diabetic", (214, 160, 0), "!"),
             ("On long-term medicines", BLUE, "+"), ("Yellow eyes or dark urine", ORANGE, "!"),
             ("Past hepatitis B or C", (70, 150, 40), "!")]
    for i, (txt, c, m) in enumerate(items):
        show(fr, card(txt, c, m), 840 + i * 122, t, D * (0.12 + 0.15 * i))

WEAP = [("fat", "Less oil & sugar", GREEN), ("virus", "Hepatitis B vaccine", BLUE), ("bottle", "No alcohol", TEAL)]
def s_fight(fr, t, D):
    show(fr, pill("THE FIGHT!", RED, size=50), 230, t, 0.1)
    ground(fr, 230, 900, 320)
    scales = {}; cur = None
    for i, (k, txt, c) in enumerate(WEAP):
        t0 = D * (0.06 + 0.3 * i); t1 = t0 + D * 0.16
        if t < t1: scales[k] = 1.0
        else: scales[k] = max(0.0, 1 - (t - t1) / (D * 0.06))
        if t0 <= t < t1 + D * 0.1: cur = (k, txt, c, t0, t1)
    draw_villains(fr, t, 0, scales)
    recoil = 0
    if cur:
        k, txt, c, t0, t1 = cur
        x0, y0 = 230 + 175 * 0.95, 680; x1, y1 = VPOS[k]
        if t < t1:
            p = (t - t0) / (t1 - t0); recoil = 12 * (1 - p)
            put(fr, mini_label(txt, c, 34), x0 + (x1 - 120 - x0) * ease(p), y0 + (y1 - y0) * ease(p))
        else:
            a = 1 - (t - t1) / (D * 0.1); burst(fr, x1, y1, 170 * (1.2 - a * 0.4), max(0, a))
        show(fr, text_el(txt, 64, color=c), 1300, t, t0)
    put(fr, DOC["aim"], 230 - recoil, 720, 0.95)
    if t > D * 0.94 or all(v == 0 for v in scales.values()):
        show(fr, text_el("Enemies defeated!", 64, color=GREEN), 1300, t, D * 0.94)

def s_victory(fr, t, D):
    show(fr, pill("VICTORY! HEALTHY LIVER", GREEN, size=46), 230, t, 0.1)
    ground(fr, 640, 820, 460); ground(fr, 200, 860, 280)
    put(fr, DOC["idle"], 200, 660, 0.75)
    put(fr, LV["happy"], 640, 620 + 14 * math.sin(t * 4), 0.85)
    sparkles(fr, 640, 610, 300, t, 10)
    show(fr, card("Fasting may be advised: follow your lab's instructions", BLUE, "◷"), 960, t, D * 0.3)
    show(fr, card("Tell your doctor about all your medicines", ORANGE, "!"), 1200, t, D * 0.6)

def s_close(fr, t, D):
    show(fr, big_logo(), 220, t, 0.2)
    show(fr, pill("Show this video to your doctor", GREEN, size=44), 830, t, 1.0)
    show(fr, text_el("Which test should we explain next?", 54, color=DBLUE), 990, t, 2.4)
    show(fr, text_el("Comment below. Your question could be our next video!", 42, "Medium", GREY), 1140, t, 3.2)
    show(fr, pill("Follow Health Test Simplified", BLUE, size=40), 1370, t, 4.6)
    show(fr, text_el("For awareness only. Consult your doctor.", 30, "Regular", GREY), 1680, t, 5.0)

SCENES = [s_intro, s_attack, s_symptoms, s_doctor, s_scan, s_who, s_fight, s_victory, s_close]

# ---------------- render ----------------
if __name__ == "__main__":
    vd = json.load(open("/tmp/lv_durs.json"))
    durs = [round(v + 1.4, 2) for v in vd]; durs[-1] = max(durs[-1], 7.0)
    starts, acc = [], 0.0
    for dsec in durs: starts.append(acc + 0.35); acc += int(dsec * FPS) / FPS
    inputs, flt = [], []
    for i, st in enumerate(starts):
        inputs += ["-i", f"/tmp/lv_{i}.wav"]
        flt.append(f"[{i}:a]aresample=44100,adelay={int(st*1000)}|{int(st*1000)}[a{i}]")
    flt.append("".join(f"[a{i}]" for i in range(len(starts))) +
               f"amix=inputs={len(starts)}:normalize=0,apad,atrim=0:{acc},loudnorm=I=-16[out]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(flt),
                    "-map", "[out]", "-ac", "2", "-ar", "44100", "/tmp/lv_track.wav"], check=True)
    OUT = "LFT_Doctor_vs_Disease_Hindi.mp4"
    proc = subprocess.Popen(["ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
        "-i", "-", "-i", "/tmp/lv_track.wav", "-shortest", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    base = BG.convert("RGBA"); base.alpha_composite(HEADER, (0, 40))
    total = sum(int(x * FPS) for x in durs); fidx = 0
    only = [int(a) for a in sys.argv[1:]]
    for si, (fn, D) in enumerate(zip(SCENES, durs)):
        n = int(D * FPS)
        for f in range(n):
            t = f / FPS; fr = base.copy(); fn(fr, t, D)
            a = min(1, t / 0.25, (D - t) / 0.3)
            if a < 1: fr = Image.blend(base, fr, max(0, a))
            ImageDraw.Draw(fr).rectangle((0, 0, int(W * (fidx + 1) / total), 10), fill=GREEN)
            proc.stdin.write(fr.convert("RGB").tobytes()); fidx += 1
    proc.stdin.close(); proc.wait(); print("done", round(fidx / FPS, 1), "s")
