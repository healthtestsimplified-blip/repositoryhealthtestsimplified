import json, math, subprocess, wave, sys
import numpy as np
from PIL import ImageChops
import lft_cartoon2 as L2
from lft_cartoon2 import *

# ---------------- sprites ----------------
def drop_sprite(color, mood):
    w, h = 380, 480
    im = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    S = lambda *v: [x * SS for x in v]
    d.ellipse(S(40, 160, 340, 460), fill=color)
    d.polygon(S(190, 10, 60, 250, 320, 250), fill=color)
    d.ellipse(S(95, 210, 150, 290), fill=blend(color, (255, 255, 255), 0.4))
    for ex in (150, 240):
        d.ellipse(S(ex - 30, 270, ex + 30, 335), fill=WHITE); d.ellipse(S(ex - 13, 292, ex + 15, 322), fill=(30, 30, 40))
    if mood == "happy":
        d.arc(S(145, 320, 245, 400), 20, 160, fill=(90, 0, 10), width=10 * SS)
        for ex in (100, 290): d.ellipse(S(ex - 22, 345, ex + 22, 375), fill=(255, 150, 160))
    else:
        d.arc(S(155, 360, 235, 410), 200, 340, fill=(90, 0, 10), width=9 * SS)
        d.line(S(115, 255, 175, 268), fill=(70, 0, 10), width=8 * SS); d.line(S(215, 268, 275, 255), fill=(70, 0, 10), width=8 * SS)
        if mood == "sick":
            d.polygon(S(300, 200, 288, 232, 312, 232), fill=(120, 190, 255)); d.ellipse(S(284, 220, 316, 252), fill=(120, 190, 255))
    return im.resize((w, h), Image.LANCZOS)
B_OK = (210, 25, 45); B_SICK = (220, 150, 160)
BD = {"happy": drop_sprite(B_OK, "happy"), "worried": drop_sprite(blend(B_OK, B_SICK, 0.5), "worried"), "sick": drop_sprite(B_SICK, "sick")}
def drop_mix(k): return BD["happy"] if k < 0.33 else (BD["worried"] if k < 0.7 else BD["sick"])

def anaemia_sprite():
    w = h = 300
    im = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    S = lambda *v: [x * SS for x in v]
    col = (120, 110, 140)
    d.ellipse(S(55, 50, 245, 240), fill=col)
    pts = [(55, 150)] + [(55 + k * 190 / 6, 270 - (20 if k % 2 else 0)) for k in range(7)] + [(245, 150)]
    d.polygon(S(*[c for p in pts for c in p]), fill=col)
    d.rounded_rectangle(S(70, 110, 230, 150), 18 * SS, fill=(40, 30, 60))  # thief mask
    for ex in (115, 185): d.ellipse(S(ex - 14, 118, ex + 14, 142), fill=WHITE); d.ellipse(S(ex - 6, 124, ex + 6, 136), fill=(200, 0, 0))
    d.line(S(80, 95, 135, 110), fill=(30, 20, 40), width=7 * SS); d.line(S(165, 110, 220, 95), fill=(30, 20, 40), width=7 * SS)
    d.line(S(115, 195, 135, 185, 150, 195, 165, 185, 185, 195), fill=(30, 20, 40), width=6 * SS)
    d.rounded_rectangle(S(205, 170, 285, 215), 10 * SS, fill=(150, 90, 40))   # stolen "Fe" bag
    d.text((245 * SS, 192 * SS), "Fe", font=font("Bold", 30 * SS), fill=WHITE, anchor="mm")
    return im.resize((w, h), Image.LANCZOS)

def bacteria_sprite():
    w = h = 300
    im = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    S = lambda *v: [x * SS for x in v]
    for k in range(6):
        y = 90 + k * 25
        d.line(S(40, y, 15, y - 15, 0, y + 5), fill=(120, 60, 140), width=5 * SS)
        d.line(S(260, y, 285, y + 15, 300, y - 5), fill=(120, 60, 140), width=5 * SS)
    d.rounded_rectangle(S(35, 75, 265, 235), 80 * SS, fill=(150, 80, 170))
    for (x, y) in [(80, 110), (220, 200), (200, 100), (90, 200)]: d.ellipse(S(x - 9, y - 9, x + 9, y + 9), fill=(110, 50, 130))
    angry_face(d, 150, 155, 70, S)
    im = im.rotate(-12, resample=Image.BICUBIC)
    return im.resize((w, h), Image.LANCZOS)

def mosquito_sprite():
    w = h = 300
    im = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    S = lambda *v: [x * SS for x in v]
    flap = 0
    d.ellipse(S(40, 40, 145, 120), fill=(190, 215, 240)); d.ellipse(S(155, 40, 260, 120), fill=(190, 215, 240))
    for s_ in (-1, 1):
        for k in range(3):
            d.line(S(150, 170 + k * 20, 150 + s_ * (95 + k * 12), 250 + k * 15), fill=(40, 40, 50), width=5 * SS)
    d.ellipse(S(120, 120, 180, 260), fill=(45, 45, 55))
    for k in range(4): d.rectangle(S(122, 165 + k * 22, 178, 173 + k * 22), fill=WHITE)
    d.ellipse(S(100, 70, 200, 160), fill=(45, 45, 55))
    d.line(S(115, 140, 60, 175), fill=(45, 45, 55), width=6 * SS)  # proboscis
    for ex in (130, 170): d.ellipse(S(ex - 15, 95, ex + 15, 125), fill=WHITE); d.ellipse(S(ex - 6, 104, ex + 6, 116), fill=(220, 0, 0))
    d.line(S(108, 88, 140, 100), fill=WHITE, width=5 * SS); d.line(S(160, 100, 192, 88), fill=WHITE, width=5 * SS)
    return im.resize((w, h), Image.LANCZOS)

VIL["fat"] = anaemia_sprite(); VIL["virus"] = bacteria_sprite(); VIL["bottle"] = mosquito_sprite()
VLAB["fat"] = mini_label("ANAEMIA", (110, 100, 130)); VLAB["virus"] = mini_label("INFECTION", (140, 70, 160))
VLAB["bottle"] = mini_label("DENGUE", (45, 45, 55))
L2.WEAP2[:] = [("fat", "Iron-rich food", GREEN), ("virus", "Clean hands & safe water", BLUE), ("bottle", "No stagnant water", TEAL)]

def cell_team():
    im = Image.new("RGBA", (W, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    # RBC
    cx = 190; d.ellipse((cx - 110, 60, cx + 110, 240), fill=(210, 30, 45)); d.ellipse((cx - 55, 110, cx + 55, 190), fill=(170, 15, 30))
    # WBC
    cx = 540
    for a in range(0, 360, 30):
        d.ellipse((cx + 95 * math.cos(math.radians(a)) - 30, 150 + 95 * math.sin(math.radians(a)) - 30,
                   cx + 95 * math.cos(math.radians(a)) + 30, 150 + 95 * math.sin(math.radians(a)) + 30), fill=(205, 190, 240))
    d.ellipse((cx - 100, 50, cx + 100, 250), fill=(215, 200, 245))
    for (x, y, r) in [(-35, -20, 40), (30, 10, 42), (-10, 45, 34)]: d.ellipse((cx + x - r, 150 + y - r, cx + x + r, 150 + y + r), fill=(120, 70, 180))
    # Platelets
    cx = 890
    for (x, y, r) in [(-50, -30, 32), (40, -50, 26), (10, 20, 38), (-60, 50, 24), (60, 40, 28)]:
        d.ellipse((cx + x - r, 150 + y - r * 0.7, cx + x + r, 150 + y + r * 0.7), fill=(245, 190, 60))
    for cx, name, role, col in [(190, "RBC", "Carry oxygen", RED), (540, "WBC", "Fight germs", PURPLE), (890, "Platelets", "Stop bleeding", ORANGE)]:
        d.text((cx, 300), name, font=font("Bold", 46), fill=col, anchor="mm")
        d.text((cx, 360), role, font=font("Medium", 34), fill=GREY, anchor="mm")
    return im

def cbc_table():
    rows = [("Test", "Normal (approx.)"), ("Hemoglobin", "M 13–17 | F 12–15 g/dL"), ("WBC", "4,000 – 11,000 /cumm"),
            ("Platelets", "1.5 – 4.5 lakh /cumm")]
    colw = [330, 620]; rh = 120; tw = sum(colw); x0 = (W - tw) // 2
    im = Image.new("RGBA", (W, rh * len(rows) + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((x0, 0, x0 + tw, rh * len(rows)), 28, fill=WHITE, outline=(200, 215, 235), width=3)
    d.rounded_rectangle((x0 + 8, 8, x0 + tw - 8, rh - 8), 22, fill=BLUE)
    cols = [None, RED, PURPLE, ORANGE]
    for r, (a, b) in enumerate(rows):
        y = r * rh + rh / 2
        if r == 0:
            d.text((x0 + colw[0] / 2, y), a, font=font("Bold", 36), fill=WHITE, anchor="mm")
            d.text((x0 + colw[0] + colw[1] / 2, y), b, font=font("Bold", 36), fill=WHITE, anchor="mm")
        else:
            d.ellipse((x0 + 30, y - 14, x0 + 58, y + 14), fill=cols[r])
            d.text((x0 + 76, y), a, font=font("Bold", 36), fill=DBLUE, anchor="lm")
            d.text((x0 + colw[0] + colw[1] / 2, y), b, font=font("Bold", 36), fill=GREY, anchor="mm")
            if r < len(rows) - 1: d.line((x0 + 24, (r + 1) * rh, x0 + tw - 24, (r + 1) * rh), fill=(225, 232, 242), width=2)
    return im

# ---------------- scenes ----------------
def c_hook(fr, t, D):
    rays(fr, 540, 900, t, (255, 60, 60), a=40)
    for i, k in enumerate(("fat", "virus", "bottle")):
        put(fr, darken(VIL[k]), 230 + i * 310, 1450 + 20 * math.sin(t * 4 + i), 1.0)
    NOW["shake"] = 10 if t < 0.5 else 0
    pop(fr, white_text("Tired all the time? Fever again and again?", 72), 540, 640, t, 0.1, "boom")
    pop(fr, white_text("Your blood may be under ATTACK!", 60, color=YEL), 540, 920, t, 1.8, "whoosh")
    pop(fr, box_text("Watch till the end: 3 weapons to win!", GREEN, 42), 540, 1150, t, D * 0.55, "pop")

def c_intro(fr, t, D):
    show(fr, pill("MEET YOUR BLOOD", RED, size=46), 230, t, 0.1)
    hp_bar(fr, 540, 400, 560, 1.0, "BLOOD HEALTH")
    ground(fr, 540, 920, 380); put(fr, BD["happy"], 540, 680 + 14 * math.sin(t * 3), 0.85)
    sparkles(fr, 540, 680, 280, t, 6, (255, 200, 60))
    show(fr, text_el("Carries oxygen & fights germs, 24x7", 52, color=DBLUE), 980, t, D * 0.18)
    pop(fr, box_text("DID YOU KNOW? Your body makes about 2 million red blood cells every second!", PURPLE, 40), 540, 1300, t, D * 0.5, "ding")

def c_attack(fr, t, D):
    vs = D * 0.22
    if t < vs:
        put(fr, BD["happy"], 240, 760, 0.6); villains(fr, t, VPOS2)
        pop(fr, VS_IMG, 560, 760, t, 0.15, "boom"); NOW["shake"] = 12 if 0.15 < t < 0.5 else 0
        show(fr, pill("BLOOD  vs  3 ENEMIES", RED, size=48), 230, t, 0.1); return
    show(fr, pill("THE ENEMIES ATTACK!", RED, size=46), 230, t, vs)
    k = ease((t - vs) / (D * 0.65)); hp_bar(fr, 270, 470, 380, 1 - 0.7 * k, "BLOOD", WHITE)
    hits = [vs + 0.4 + j * (D - vs - 1.2) / 5 for j in range(5)]
    for h in hits: fire("zap", h)
    hit = any(0 <= t - h < 0.25 for h in hits); NOW["shake"] = 8 if hit else 0
    ground(fr, 270, 1020, 340)
    put(fr, drop_mix(k), 270 + (6 * math.sin(t * 40) if hit else 0), 780, 0.62)
    villains(fr, t, VPOS2)
    if hit:
        d = ImageDraw.Draw(fr)
        for kk in ("fat", "virus", "bottle"):
            x, y = VPOS2[kk]; pts = [(x - 110, y)]
            for j in range(1, 6): pts.append((x - 110 - j * 65, y + (780 - y) * j / 6 + (25 if j % 2 else -25)))
            d.line(pts, fill=YEL, width=9)
    show(fr, white_text("They drain your strength silently", 52, color=YEL), 1330, t, D * 0.6)

def c_team(fr, t, D):
    show(fr, pill("MEET THE BLOOD TEAM", BLUE, size=46), 230, t, 0.1)
    fire("pop", 0.5); show(fr, cell_team(), 420, t, 0.5)
    fire("pop", D * 0.45); show(fr, card("Hemoglobin inside RBCs carries oxygen", RED, "●"), 950, t, D * 0.45)
    pop(fr, box_text("If the team is weak, you feel weak!", ORANGE, 44), 540, 1250, t, D * 0.7, "ding")

def c_doctor(fr, t, D):
    show(fr, pill("HERO ENTRY!", GREEN, size=48), 230, t, 0.1)
    p = t / (0.35 * D)
    if p >= 1: rays(fr, 270, 720, t, (120, 230, 140), a=60)
    ground(fr, 790, 980, 340); ground(fr, 270, 1000, 340)
    put(fr, BD["sick"], 790, 760, 0.55); fire("whoosh", 0.1)
    if p < 1: put(fr, DOC["w0" if int(t * 6) % 2 else "w1"], -220 + 490 * p, 720 + 6 * abs(math.sin(t * 9)))
    else: put(fr, DOC["aim"], 270, 720)
    pop(fr, stroke_text("DR. HEALTH", 100, GREEN, WHITE, 8), 540, 1130, t, 0.37 * D, "ding")
    show(fr, text_el("Weapon: CBC test", 62, color=BLUE), 1250, t, 0.55 * D)
    show(fr, text_el("Complete Blood Count: the most common blood test", 42, "Medium", GREEN), 1360, t, 0.7 * D)

def c_scan(fr, t, D):
    show(fr, pill("WHAT CBC CHECKS", BLUE, size=46), 230, t, 0.1)
    ground(fr, 800, 820, 330); ground(fr, 230, 880, 320)
    put(fr, DOC["aim"], 230, 600, 0.9); beam(fr, 230 + 175 * 0.9, 560, 770, 600, t); fire("zap", 0.2)
    put(fr, BD["worried"], 800, 610, 0.5)
    rows = [("Hemoglobin & RBC: anaemia check", RED), ("WBC: infection check", PURPLE), ("Platelets: dengue & bleeding check", ORANGE)]
    for i, (txt, c) in enumerate(rows):
        fire("pop", D * (0.12 + 0.22 * i)); show(fr, card(txt, c, "●", size=42), 960 + i * 150, t, D * (0.12 + 0.22 * i))

def c_cheat(fr, t, D):
    show(fr, pill("REPORT CHEAT SHEET", PURPLE, size=46), 230, t, 0.1)
    put(fr, BD["worried"], 540, 460 + 10 * math.sin(t * 3), 0.42)
    fire("pop", 0.6); show(fr, cbc_table(), 650, t, 0.6)
    show(fr, text_el("Ranges vary slightly between labs", 42, "Medium", GREY), 1200, t, D * 0.7)
    show(fr, text_el("Screenshot this!", 44, "Bold", TEAL), 1300, t, D * 0.8)

def c_who(fr, t, D):
    show(fr, pill("WHO SHOULD GET TESTED?", ORANGE, size=44), 230, t, 0.1)
    ground(fr, 250, 770, 300); ground(fr, 760, 760, 300)
    put(fr, DOC["idle"], 250, 560, 0.75); put(fr, BD["worried"], 760, 590, 0.45)
    items = [("Tiredness, weakness or pale skin", RED, "!"), ("Fever for 2 days or more", ORANGE, "!"),
             ("Pregnant women", (216, 27, 96), "♥"), ("Yearly health check-up", BLUE, "✓")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.12 + 0.2 * i)); show(fr, card(txt, c, m, size=40), 850 + i * 140, t, D * (0.12 + 0.2 * i))

def c_victory(fr, t, D):
    rays(fr, 600, 640, t, (255, 200, 40), a=45)
    show(fr, pill("VICTORY!", GREEN, size=54), 230, t, 0.1); fire("chime", 0.1)
    hp_bar(fr, 600, 400, 520, 0.3 + 0.7 * ease(t / (D * 0.4)), "BLOOD HEALTH")
    ground(fr, 640, 900, 360); ground(fr, 190, 900, 280)
    put(fr, DOC["idle"], 190, 700, 0.75)
    put(fr, BD["happy"], 640, 680 + 14 * math.sin(t * 4), 0.75); sparkles(fr, 640, 670, 270, t, 10)
    fire("pop", D * 0.3); show(fr, card("No fasting needed for CBC", GREEN, "✓"), 1000, t, D * 0.3)
    fire("pop", D * 0.6); show(fr, card("Fever in dengue season? Doctor may repeat platelet count", ORANGE, "!", size=40), 1180, t, D * 0.6)

def c_close(fr, t, D):
    show(fr, big_logo(), 210, t, 0.2)
    fire("ding", 0.8); show(fr, box_text("Take any medicine only as advised by your doctor", GREEN, 42), 820, t, 0.8)
    show(fr, text_el("Which test should Dr. Health explain next?", 52, color=DBLUE), 1020, t, D * 0.45)
    show(fr, text_el("Tell us in the comments!", 44, "Medium", GREY), 1180, t, D * 0.55)
    show(fr, pill("Follow Health Test Simplified", BLUE, size=40), 1340, t, D * 0.65)
    show(fr, text_el("For awareness only. Consult your doctor.", 30, "Regular", GREY), 1680, t, D * 0.7)

SC = [(c_hook, "red"), (c_intro, "light"), (c_attack, "purple"), (c_team, "light"), (c_doctor, "light"), (c_scan, "light"),
      (c_cheat, "light"), (c_who, "light"), (s_fight, "navy"), (c_victory, "gold"), (c_close, "light")]

def run(SC, P, OUTF):
    vd = json.load(open(P + "durs.json"))
    durs = [round(v + 1.3, 2) for v in vd]; durs[0] = max(durs[0], 6.0); durs[-1] = max(durs[-1], 7.5)
    starts, acc = [], 0.0
    for dsec in durs: starts.append(acc + 0.3); acc += int(dsec * FPS) / FPS
    inputs, flt = [], []
    for i, st in enumerate(starts):
        inputs += ["-i", f"{P}{i}.wav"]; flt.append(f"[{i}:a]aresample=44100,adelay={int(st*1000)}|{int(st*1000)}[a{i}]")
    flt.append("".join(f"[a{i}]" for i in range(len(starts))) + f"amix=inputs={len(starts)}:normalize=0,apad,atrim=0:{acc},loudnorm=I=-16[out]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(flt), "-map", "[out]",
                    "-ac", "1", "-ar", "44100", P + "voice.wav"], check=True)
    proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
        "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", P + "video.mp4"], stdin=subprocess.PIPE)
    total = sum(int(x * FPS) for x in durs); fidx = 0; t0 = 0.0
    for (fn, bgk), D in zip(SC, durs):
        base = BASES[bgk]; n = int(D * FPS)
        for f in range(n):
            t = f / FPS; NOW.update(t=t, t0=t0, shake=0.0)
            fr = base.copy(); fn(fr, t, D)
            if NOW["shake"]: fr = ImageChops.offset(fr, int(NOW["shake"] * math.sin(t * 60)), int(NOW["shake"] * math.cos(t * 47)))
            a = min(1, t / 0.2, (D - t) / 0.25)
            if a < 1: fr = Image.blend(base, fr, max(0, a))
            ImageDraw.Draw(fr).rectangle((0, 0, int(W * (fidx + 1) / total), 10), fill=YEL)
            proc.stdin.write(fr.convert("RGB").tobytes()); fidx += 1
        t0 += n / FPS
    proc.stdin.close(); proc.wait()
    v = read_wav(P + "voice.wav"); N = len(v); m = music(N / SR + 0.1)[:N]; m = np.pad(m, (0, N - len(m)))
    envv = np.convolve(np.abs(v), np.ones(int(0.25 * SR)) / int(0.25 * SR), "same"); duck = 1 - 0.6 * np.clip(envv / 0.04, 0, 1)
    fx = np.zeros(N)
    for (tt, kind) in EVENTS:
        s = sfx(kind); i0 = int(tt * SR); k = min(len(s), N - i0)
        if k > 0 and i0 >= 0: fx[i0:i0 + k] += s[:k]
    mix = v + m * 0.13 * duck + fx * 0.45; mix = mix / max(1.0, np.abs(mix).max() / 0.97)
    pcm = (np.repeat(mix[:, None], 2, axis=1) * 32767).astype(np.int16)
    with wave.open(P + "final.wav", "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", P + "video.mp4", "-i", P + "final.wav", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", OUTF], check=True)
    print("done", round(fidx / FPS, 1), "s,", len(EVENTS), "sfx")

def preview(SC):
    D = [7, 12, 12, 10, 10, 13, 13, 12, 15, 12, 10]
    tests = [(0, .7), (1, .85), (2, .1), (2, .7), (3, .9), (4, .85), (5, .9), (6, .9), (7, .9), (8, .25), (8, .55), (9, .9), (10, .9)]
    ims = []
    for si, p in tests:
        fn, bg = SC[si]; d = D[si]; NOW.update(t=d * p, t0=0, shake=0)
        fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((270, 480)))
    s = Image.new("RGB", (270 * 7, 480 * 2), "white")
    for i, im in enumerate(ims): s.paste(im, ((i % 7) * 270, (i // 7) * 480))
    s.save("sheet.png")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview": preview(SC)
    else: run(SC, "/tmp/cb_", "CBC_Doctor_vs_Disease_Hindi.mp4")
