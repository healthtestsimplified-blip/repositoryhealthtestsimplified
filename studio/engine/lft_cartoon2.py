import json, math, subprocess, wave
import numpy as np
from PIL import ImageChops
from lft_cartoon import *   # sprites + helpers (render code there only runs as __main__)

PURPLE = (123, 31, 162); YEL = (255, 214, 0)

# ---------------- backgrounds ----------------
def grad(top, bot, waves=True):
    y = np.linspace(0, 1, H)[:, None]
    arr = (np.array(top) * (1 - y)[..., None] + np.array(bot) * y[..., None]).repeat(W, 1)
    img = Image.fromarray(arr.astype(np.uint8)).convert("RGBA"); d = ImageDraw.Draw(img)
    if waves:
        d.polygon([(x, 1780 + 40 * math.sin(x / 170)) for x in range(0, W + 1, 10)] + [(W, H), (0, H)], fill=BLUE)
        d.polygon([(x, 1830 + 30 * math.sin(x / 140 + 2)) for x in range(0, W + 1, 10)] + [(W, H), (0, H)], fill=GREEN)
    return img
def header_white():
    im = Image.new("RGBA", (W, 170), (0, 0, 0, 0))
    sm = logo.resize((120, 120), Image.LANCZOS); im.paste(sm, (60, 25), sm)
    d = ImageDraw.Draw(im)
    d.text((200, 38), "Health Test", font=font("Bold", 44), fill=WHITE)
    d.text((200, 90), "Simplified", font=font("Medium", 34), fill=(210, 220, 235))
    return im
HW = header_white()
def mk(bg, dark):
    b = bg.copy(); b.alpha_composite(HW if dark else HEADER, (0, 40)); return b
BASES = {"light": mk(BG.convert("RGBA"), False), "red": mk(grad((45, 0, 8), (140, 15, 30)), True),
         "purple": mk(grad((20, 8, 55), (75, 30, 125)), True), "navy": mk(grad((6, 16, 45), (20, 55, 115)), True),
         "gold": mk(grad((255, 248, 220), (255, 255, 255)), False)}

# ---------------- events (for sound effects) ----------------
EVENTS = []; NOW = {"t": 0.0, "t0": 0.0, "shake": 0.0}
def fire(kind, at):
    if at <= NOW["t"] < at + 1 / FPS: EVENTS.append((NOW["t0"] + at, kind))

# ---------------- extra visual helpers ----------------
def stroke_text(text, size, fill, stroke, sw=8):
    f = font("Bold", size); tw = f.getlength(text) + 2 * sw
    im = Image.new("RGBA", (int(tw + 20), int(size * 1.4)), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((im.width / 2, im.height / 2), text, font=f, fill=fill, anchor="mm", stroke_width=sw, stroke_fill=stroke)
    return im
def white_text(text, size=60, weight="Bold", color=WHITE, maxw=940):
    return text_el(text, size, weight, color, maxw)
def pop(fr, im, cx, cy, t, tin, sfx=None):
    if sfx: fire(sfx, tin)
    p = (t - tin) / 0.35
    if p <= 0: return
    put(fr, im, cx, cy, 1.7 - 0.7 * ease(p), min(1, p * 2))
def hp_bar(fr, cx, y, w, val, label="", lab_col=DBLUE):
    d = ImageDraw.Draw(fr); val = max(0, min(1, val))
    col = GREEN if val > 0.6 else (ORANGE if val > 0.3 else RED)
    d.rounded_rectangle((cx - w / 2 - 6, y - 6, cx + w / 2 + 6, y + 40), 22, fill=(20, 25, 40))
    if val > 0.01: d.rounded_rectangle((cx - w / 2, y, cx - w / 2 + w * val, y + 34), 17, fill=col)
    d.text((cx, y + 17), f"{int(round(val * 100))}%", font=font("Bold", 26), fill=WHITE, anchor="mm")
    if label: d.text((cx, y - 30), label, font=font("Bold", 30), fill=lab_col, anchor="mm")
def rays(fr, cx, cy, t, col, n=14, a=55, R=900):
    lay = Image.new("RGBA", fr.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for k in range(n):
        a0 = t * 0.4 + k * 2 * math.pi / n; a1 = a0 + math.pi / n * 0.6
        d.polygon([(cx, cy), (cx + R * math.cos(a0), cy + R * math.sin(a0)), (cx + R * math.cos(a1), cy + R * math.sin(a1))], fill=(*col, a))
    fr.alpha_composite(lay)
def darken(spr, k=0.15):
    s = spr.copy(); rgb = Image.new("RGBA", s.size, (20, 0, 0, 255)); rgb.putalpha(s.getchannel("A").point(lambda v: int(v * (1 - k)))); return rgb
def box_text(text, bg, size=42, width=940):
    f = font("Bold", size); lines = []; cur = ""
    for w_ in text.split():
        tt = (cur + " " + w_).strip()
        if f.getlength(tt) <= width - 80: cur = tt
        else: lines.append(cur); cur = w_
    lines.append(cur); lh = int(size * 1.3); h = lh * len(lines) + 50
    im = Image.new("RGBA", (W, h + 6), (0, 0, 0, 0)); d = ImageDraw.Draw(im); x0 = (W - width) / 2
    d.rounded_rectangle((x0, 0, x0 + width, h), 34, fill=bg)
    for i, l in enumerate(lines): d.text((W / 2, 25 + i * lh + lh / 2), l, font=f, fill=WHITE, anchor="mm")
    return im
def range_table():
    rows = [("Test", "Normal (approx.)"), ("SGPT (ALT)", "up to ~40 U/L"), ("SGOT (AST)", "up to ~40 U/L"),
            ("Bilirubin (total)", "0.3 – 1.2 mg/dL"), ("Albumin", "3.5 – 5.0 g/dL")]
    colw = [470, 470]; rh = 118; tw = sum(colw); x0 = (W - tw) // 2
    im = Image.new("RGBA", (W, rh * len(rows) + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((x0, 0, x0 + tw, rh * len(rows)), 28, fill=WHITE, outline=(200, 215, 235), width=3)
    d.rounded_rectangle((x0 + 8, 8, x0 + tw - 8, rh - 8), 22, fill=BLUE)
    cols = [None, RED, RED, ORANGE, GREEN]
    for r, (a, b) in enumerate(rows):
        y = r * rh + rh / 2
        if r == 0:
            d.text((x0 + colw[0] / 2, y), a, font=font("Bold", 38), fill=WHITE, anchor="mm")
            d.text((x0 + colw[0] + colw[1] / 2, y), b, font=font("Bold", 38), fill=WHITE, anchor="mm")
        else:
            d.ellipse((x0 + 34, y - 14, x0 + 62, y + 14), fill=cols[r])
            d.text((x0 + 80, y), a, font=font("Bold", 38), fill=DBLUE, anchor="lm")
            d.text((x0 + colw[0] + colw[1] / 2, y), b, font=font("Bold", 40), fill=GREY, anchor="mm")
            if r < len(rows) - 1: d.line((x0 + 24, (r + 1) * rh, x0 + tw - 24, (r + 1) * rh), fill=(225, 232, 242), width=2)
    return im

VS_IMG = stroke_text("VS", 230, YEL, RED, 12)
KO_IMG = stroke_text("K.O.!", 120, YEL, RED, 10)

# ---------------- scenes ----------------
def s_hook(fr, t, D):
    rays(fr, 540, 900, t, (255, 60, 60), a=40)
    for i, k in enumerate(("fat", "virus", "bottle")):
        put(fr, darken(VIL[k]), 230 + i * 310, 1450 + 20 * math.sin(t * 4 + i), 1.0)
    NOW["shake"] = 10 if t < 0.5 else 0
    pop(fr, white_text("Your liver is under ATTACK!", 84), 540, 640, t, 0.1, "boom")
    pop(fr, white_text("No pain. No warning.", 60, color=YEL), 540, 900, t, 1.6, "whoosh")
    pop(fr, box_text("Watch till the end: 3 weapons to save it!", GREEN, 42), 540, 1130, t, D * 0.55, "pop")

def s_intro(fr, t, D):
    show(fr, pill("MEET YOUR LIVER", RED, size=46), 230, t, 0.1)
    hp_bar(fr, 540, 400, 560, 1.0, "LIVER HEALTH")
    ground(fr, 540, 860, 500)
    put(fr, LV["happy"], 540, 660 + 16 * math.sin(t * 3), 0.95)
    sparkles(fr, 540, 660, 320, t, 6, (255, 200, 60))
    show(fr, text_el("500+ jobs every day!", 60, color=DBLUE), 950, t, D * 0.18)
    for i, (txt, c) in enumerate([("Digests food", BLUE), ("Cleans toxins", TEAL), ("Stores energy", ORANGE)]):
        fire("pop", D * (0.28 + 0.1 * i)); show(fr, pill(txt, c, size=40), 1060 + i * 105, t, D * (0.28 + 0.1 * i))
    pop(fr, box_text("DID YOU KNOW? Your liver can regrow itself!", PURPLE, 42), 540, 1440, t, D * 0.66, "ding")

VPOS2 = {"fat": (830, 520), "virus": (870, 830), "bottle": (830, 1130)}
def villains(fr, t, pos, xoff=0, sc=None, hp=None, lab=True):
    for i, k in enumerate(("fat", "virus", "bottle")):
        x, y = pos[k]; s = 1.0 if sc is None else sc[k]; x += xoff; y += 12 * math.sin(t * 4 + i * 2)
        put(fr, VIL[k], x, y, 0.72 * s)
        if lab and s > 0.6: put(fr, VLAB[k], x, y + 118 * s, s)
        if hp is not None and s > 0.05: hp_bar(fr, x, y - 140, 200, hp[k])

def s_attack(fr, t, D):
    vs = D * 0.22
    if t < vs:
        put(fr, LV["happy"], 250, 760, 0.6); villains(fr, t, VPOS2)
        pop(fr, VS_IMG, 560, 760, t, 0.15, "boom"); NOW["shake"] = 12 if 0.15 < t < 0.5 else 0
        show(fr, pill("LIVER  vs  3 ENEMIES", RED, size=48), 230, t, 0.1)
        return
    show(fr, pill("THE ENEMIES ATTACK!", RED, size=46), 230, t, vs)
    k = ease((t - vs) / (D * 0.65)); hp = 1 - 0.7 * k
    hp_bar(fr, 300, 470, 380, hp, "LIVER", WHITE)
    for j in range(5): fire("zap", vs + 0.4 + j * (D - vs - 1.2) / 5)
    hit = any(0 <= t - (vs + 0.4 + j * (D - vs - 1.2) / 5) < 0.25 for j in range(5))
    NOW["shake"] = 8 if hit else 0
    ground(fr, 300, 960, 440)
    put(fr, liver_mix(k), 300 + (6 * math.sin(t * 40) if hit else 0), 760, 0.75)
    villains(fr, t, VPOS2)
    if hit:
        d = ImageDraw.Draw(fr)
        for i, kk in enumerate(("fat", "virus", "bottle")):
            x, y = VPOS2[kk]; pts = [(x - 110, y)]
            for j in range(1, 6): pts.append((x - 110 - j * 60, y + (760 - y) * j / 6 + (25 if j % 2 else -25)))
            d.line(pts, fill=YEL, width=9)
    show(fr, white_text("Damage happens silently", 54, color=YEL), 1330, t, D * 0.6)

def s_symptoms(fr, t, D):
    show(fr, pill("WARNING SIGNS COME LATE", ORANGE, size=44), 230, t, 0.1)
    hp_bar(fr, 540, 400, 460, 0.3 if int(t * 3) % 2 else 0.3, "LIVER HEALTH")
    ground(fr, 540, 820, 420)
    put(fr, LV["sick"], 540 + 4 * math.sin(t * 30), 650, 0.85)
    for i, txt in enumerate(["Tiredness", "Loss of appetite", "Yellow eyes (jaundice)", "Dark urine"]):
        fire("pop", D * (0.12 + 0.17 * i)); show(fr, card(txt, ORANGE, "!"), 910 + i * 125, t, D * (0.12 + 0.17 * i))

def s_doctor(fr, t, D):
    show(fr, pill("HERO ENTRY!", GREEN, size=48), 230, t, 0.1)
    p = t / (0.35 * D)
    if p >= 1: rays(fr, 270, 720, t, (120, 230, 140), a=60)
    ground(fr, 790, 920, 420); ground(fr, 270, 1000, 340)
    put(fr, LV["sick"], 790, 720, 0.72)
    fire("whoosh", 0.1)
    if p < 1: put(fr, DOC["w0" if int(t * 6) % 2 else "w1"], -220 + 490 * p, 720 + 6 * abs(math.sin(t * 9)))
    else: put(fr, DOC["aim"], 270, 720)
    pop(fr, stroke_text("DR. HEALTH", 100, GREEN, WHITE, 8), 540, 1130, t, 0.37 * D, "ding")
    show(fr, text_el("Weapon: Liver Function Test (LFT)", 54, color=BLUE), 1250, t, 0.55 * D)
    show(fr, text_el("Just a simple blood test", 44, "Medium", GREEN), 1400, t, 0.7 * D)

def s_scan(fr, t, D):
    show(fr, pill("WHAT LFT CHECKS", BLUE, size=46), 230, t, 0.1)
    ground(fr, 790, 800, 400); ground(fr, 230, 880, 320)
    put(fr, DOC["aim"], 230, 600, 0.9); beam(fr, 230 + 175 * 0.9, 560, 760, 610, t); fire("zap", 0.2)
    put(fr, LV["sick"], 790, 620, 0.7)
    rows = [("SGPT & SGOT: damage alarm", RED), ("Bilirubin: jaundice check", ORANGE),
            ("Albumin: liver strength", GREEN), ("ALP: bile flow", TEAL)]
    for i, (txt, c) in enumerate(rows):
        fire("pop", D * (0.12 + 0.19 * i)); show(fr, card(txt, c, "●"), 960 + i * 125, t, D * (0.12 + 0.19 * i))

def s_cheat(fr, t, D):
    show(fr, pill("REPORT CHEAT SHEET", PURPLE, size=46), 230, t, 0.1)
    put(fr, LV["worried"], 540, 470 + 10 * math.sin(t * 3), 0.55)
    fire("pop", 0.6); show(fr, range_table(), 640, t, 0.6)
    show(fr, text_el("Ranges vary slightly between labs", 42, "Medium", GREY), 1300, t, D * 0.7)
    show(fr, text_el("Screenshot this!", 44, "Bold", TEAL), 1400, t, D * 0.8)

def s_who(fr, t, D):
    show(fr, pill("WHO SHOULD GET TESTED?", ORANGE, size=44), 230, t, 0.1)
    ground(fr, 250, 770, 300); ground(fr, 760, 720, 360)
    put(fr, DOC["idle"], 250, 560, 0.75); put(fr, LV["worried"], 760, 580, 0.6)
    items = [("Drink alcohol regularly", (130, 70, 30), "!"), ("Overweight or diabetic", (214, 160, 0), "!"),
             ("On long-term medicines", BLUE, "+"), ("Past jaundice or hepatitis", (70, 150, 40), "!")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.15 + 0.19 * i)); show(fr, card(txt, c, m), 860 + i * 135, t, D * (0.15 + 0.19 * i))

WEAP2 = [("fat", "Less oil & sugar", GREEN), ("virus", "Hepatitis B vaccine", BLUE), ("bottle", "No alcohol", TEAL)]
def s_fight(fr, t, D):
    show(fr, pill("FINAL BATTLE!", RED, size=50), 230, t, 0.1)
    rays(fr, 540, 900, t, (80, 140, 255), a=30)
    sc, hp, cur = {}, {}, None
    for i, (k, txt, c) in enumerate(WEAP2):
        t0 = D * (0.1 + 0.29 * i); t1 = t0 + D * 0.12
        fire("whoosh", t0); fire("boom", t1)
        hp[k] = 1.0 if t < t1 else 0.0
        sc[k] = 1.0 if t < t1 + D * 0.08 else max(0.0, 1 - (t - t1 - D * 0.08) / (D * 0.05))
        if t0 <= t < t1 + D * 0.17: cur = (k, txt, c, t0, t1, i)
        if t1 <= t < t1 + 0.3: NOW["shake"] = 14
    ground(fr, 230, 900, 320)
    villains(fr, t, VPOS2, sc=sc, hp=hp)
    recoil = 0
    if cur:
        k, txt, c, t0, t1, i = cur
        x0, y0 = 230 + 175 * 0.95, 680; x1, y1 = VPOS2[k]
        if t < t1:
            p = (t - t0) / (t1 - t0); recoil = 12 * (1 - p)
            put(fr, mini_label(txt, c, 34), x0 + (x1 - 120 - x0) * ease(p), y0 + (y1 - y0) * ease(p))
        else:
            a = 1 - (t - t1) / (D * 0.12); burst(fr, x1, y1, 170 * (1.2 - a * 0.4), max(0, a))
            pop(fr, KO_IMG, x1 - 120, y1 - 40, t, t1)
        show(fr, pill(f"WEAPON {i + 1}", c, size=40), 1290, t, t0)
        show(fr, white_text(txt, 64, color=WHITE), 1400, t, t0)
    put(fr, DOC["aim"], 230 - recoil, 720, 0.95)

def s_victory(fr, t, D):
    rays(fr, 600, 640, t, (255, 200, 40), a=45)
    show(fr, pill("VICTORY!", GREEN, size=54), 230, t, 0.1); fire("chime", 0.1)
    hp_bar(fr, 600, 400, 520, 0.3 + 0.7 * ease(t / (D * 0.4)), "LIVER HEALTH")
    ground(fr, 640, 860, 460); ground(fr, 190, 900, 280)
    put(fr, DOC["idle"], 190, 700, 0.75)
    put(fr, LV["happy"], 640, 660 + 14 * math.sin(t * 4), 0.85); sparkles(fr, 640, 650, 300, t, 10)
    fire("pop", D * 0.35); show(fr, card("Early fatty liver can often be reversed with diet & exercise", GREEN, "✓"), 990, t, D * 0.35)
    fire("pop", D * 0.65); show(fr, card("Fasting may be advised before the test: follow your lab", BLUE, "◷"), 1240, t, D * 0.65)

def s_close(fr, t, D):
    show(fr, big_logo(), 210, t, 0.2)
    fire("ding", 0.8); show(fr, box_text("Take any medicine only as advised by your doctor", GREEN, 42), 820, t, 0.8)
    show(fr, text_el("Which disease should Dr. Health fight next?", 52, color=DBLUE), 1020, t, D * 0.45)
    show(fr, text_el("Tell us in the comments!", 44, "Medium", GREY), 1180, t, D * 0.55)
    show(fr, pill("Follow Health Test Simplified", BLUE, size=40), 1340, t, D * 0.65)
    show(fr, text_el("For awareness only. Consult your doctor.", 30, "Regular", GREY), 1680, t, D * 0.7)

SCENES2 = [(s_hook, "red"), (s_intro, "light"), (s_attack, "purple"), (s_symptoms, "light"), (s_doctor, "light"),
           (s_scan, "light"), (s_cheat, "light"), (s_who, "light"), (s_fight, "navy"), (s_victory, "gold"), (s_close, "light")]

# ---------------- audio synthesis ----------------
SR = 44100
def env(n, a=0.01, r=0.2):
    e = np.ones(n); na, nr = min(n, int(a * SR)), min(n, int(r * SR))
    if n == 0: return e
    e[:na] = np.linspace(0, 1, na); e[-nr:] *= np.linspace(1, 0, nr); return e
def sfx(kind):
    rng = np.random.default_rng(1)
    if kind == "boom":
        n = int(0.7 * SR); tt = np.arange(n) / SR
        return (np.sin(2 * np.pi * (70 - 30 * tt) * tt) * np.exp(-tt * 6) * 0.9 + rng.normal(0, 0.3, n) * np.exp(-tt * 12)) * 0.8
    if kind == "zap":
        n = int(0.25 * SR); tt = np.arange(n) / SR; f = 1400 * np.exp(-tt * 9) + 200
        return np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-tt * 10) * 0.25
    if kind == "whoosh":
        n = int(0.5 * SR); x = rng.normal(0, 1, n); x = np.convolve(x, np.ones(30) / 30, "same")
        return x * np.sin(np.linspace(0, np.pi, n)) ** 2 * 1.2
    if kind == "pop":
        n = int(0.09 * SR); tt = np.arange(n) / SR
        return np.sin(2 * np.pi * (900 - 3000 * tt) * tt) * np.exp(-tt * 40) * 0.35
    if kind in ("ding", "chime"):
        notes = [1046.5] if kind == "ding" else [523.25, 659.25, 783.99, 1046.5]
        out = np.zeros(int((0.12 * len(notes) + 0.8) * SR))
        for i, f in enumerate(notes):
            n = int(0.8 * SR); tt = np.arange(n) / SR; s = int(i * 0.12 * SR)
            out[s:s + n] += (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt)) * np.exp(-tt * 5) * 0.25
        return out
    return np.zeros(10)
def music(total):
    n = int(total * SR); out = np.zeros(n); beat = 60 / 100
    chords = [(220.0, 261.63, 329.63), (174.61, 220.0, 261.63), (130.81, 164.81, 196.0), (196.0, 246.94, 293.66)]
    seg = 8 * beat; i = 0; rng = np.random.default_rng(3)
    while i * seg < total:
        s = int(i * seg * SR); e = min(n, int((i + 1) * seg * SR)); m = e - s; tt = np.arange(m) / SR
        ch = chords[i % 4]
        pad = sum(np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(4 * np.pi * f * tt) for f in ch) * 0.05 * env(m, 0.4, 0.4)
        out[s:e] += pad
        for b in range(8):
            bs = s + int(b * beat * SR)
            if bs >= n: break
            k = min(n - bs, int(0.3 * SR)); tk = np.arange(k) / SR
            out[bs:bs + k] += np.sin(2 * np.pi * (ch[0] / 2) * tk) * np.exp(-tk * 7) * 0.12          # bass
            if b % 2 == 0: out[bs:bs + k] += np.sin(2 * np.pi * (60 - 25 * tk) * tk) * np.exp(-tk * 14) * 0.35  # kick
            hs = bs + int(beat / 2 * SR); hk = min(n - hs, int(0.04 * SR))
            if hk > 0: out[hs:hs + hk] += np.diff(rng.normal(0, 1, hk + 1)) * np.exp(-np.arange(hk) / SR * 80) * 0.05
        i += 1
    return out / (np.abs(out).max() + 1e-9)
def read_wav(p):
    with wave.open(p) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, w.getnchannels()).astype(np.float32) / 32768
    return x.mean(axis=1)

if __name__ == "__main__":
    vd = json.load(open("/tmp/l2_durs.json"))
    durs = [round(v + 1.3, 2) for v in vd]; durs[0] = max(durs[0], 6.0); durs[-1] = max(durs[-1], 7.5)
    starts, acc = [], 0.0
    for dsec in durs: starts.append(acc + 0.3); acc += int(dsec * FPS) / FPS
    # voice track
    inputs, flt = [], []
    for i, st in enumerate(starts):
        inputs += ["-i", f"/tmp/l2_{i}.wav"]; flt.append(f"[{i}:a]aresample=44100,adelay={int(st*1000)}|{int(st*1000)}[a{i}]")
    flt.append("".join(f"[a{i}]" for i in range(len(starts))) + f"amix=inputs={len(starts)}:normalize=0,apad,atrim=0:{acc},loudnorm=I=-16[out]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(flt), "-map", "[out]",
                    "-ac", "1", "-ar", "44100", "/tmp/l2_voice.wav"], check=True)
    # video
    proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
        "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "/tmp/l2_video.mp4"],
        stdin=subprocess.PIPE)
    total = sum(int(x * FPS) for x in durs); fidx = 0; t0 = 0.0
    for (fn, bgk), D in zip(SCENES2, durs):
        base = BASES[bgk]; n = int(D * FPS)
        for f in range(n):
            t = f / FPS; NOW.update(t=t, t0=t0, shake=0.0)
            fr = base.copy(); fn(fr, t, D)
            if NOW["shake"]:
                fr = ImageChops.offset(fr, int(NOW["shake"] * math.sin(t * 60)), int(NOW["shake"] * math.cos(t * 47)))
            a = min(1, t / 0.2, (D - t) / 0.25)
            if a < 1: fr = Image.blend(base, fr, max(0, a))
            ImageDraw.Draw(fr).rectangle((0, 0, int(W * (fidx + 1) / total), 10), fill=YEL)
            proc.stdin.write(fr.convert("RGB").tobytes()); fidx += 1
        t0 += n / FPS
    proc.stdin.close(); proc.wait()
    # audio mix: voice + ducked music + sfx
    v = read_wav("/tmp/l2_voice.wav"); N = len(v)
    m = music(N / SR)[:N]
    envv = np.convolve(np.abs(v), np.ones(int(0.25 * SR)) / int(0.25 * SR), "same")
    duck = 1 - 0.6 * np.clip(envv / 0.04, 0, 1)
    fx = np.zeros(N)
    for (tt, kind) in EVENTS:
        s = sfx(kind); i0 = int(tt * SR); k = min(len(s), N - i0)
        if k > 0: fx[i0:i0 + k] += s[:k]
    mix = v + m * 0.13 * duck + fx * 0.45
    mix = mix / max(1.0, np.abs(mix).max() / 0.97)
    pcm = (np.repeat(mix[:, None], 2, axis=1) * 32767).astype(np.int16)
    with wave.open("/tmp/l2_final.wav", "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "/tmp/l2_video.mp4", "-i", "/tmp/l2_final.wav", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", "LFT_Doctor_vs_Disease_Hindi_v2.mp4"], check=True)
    print("done", round(fidx / FPS, 1), "s,", len(EVENTS), "sound effects")
