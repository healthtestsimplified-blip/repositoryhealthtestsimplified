import math, sys
from cbc_cartoon import run
from eeg_cartoon import monitor, SKIN, WIRE
from emg_cartoon import arm, sticker, NERVE, SKIN_D
from lft_cartoon2 import *
from chromo_cartoon import PINK
from hts_close import close_scene

TOPIC = "NERVES  •  NCV TEST"
MYELIN = (129, 199, 132); AXON = (255, 202, 40)

def foot(d, cx, cy, s):
    d.rounded_rectangle((cx - 60 * s, cy - 220 * s, cx + 60 * s, cy + 20 * s), int(50 * s), fill=SKIN, outline=SKIN_D, width=4)
    d.rounded_rectangle((cx - 60 * s, cy - 40 * s, cx + 220 * s, cy + 60 * s), int(50 * s), fill=SKIN, outline=SKIN_D, width=4)
    for k in range(5):
        d.ellipse((cx + 170 * s + k * 0, cy - 40 * s + k * 20 * s, cx + 230 * s, cy - 15 * s + k * 20 * s), fill=SKIN, outline=SKIN_D, width=3)

def cable(d, x0, x1, y, h, t, mode="good", label=True):
    """A nerve drawn as an insulated wire: yellow axon inside green myelin; pulse moves along."""
    if mode != "bare":
        for k in range(int((x1 - x0) // 90)):
            xx = x0 + k * 90 + 6
            if mode == "myelin_bad" and k % 2 == 1: continue
            d.rounded_rectangle((xx, y - h / 2, xx + 78, y + h / 2), int(h / 2), fill=MYELIN, outline=(56, 142, 60), width=3)
    aw = h * 0.28 if mode != "axon_bad" else h * 0.12
    d.rounded_rectangle((x0, y - aw / 2, x1, y + aw / 2), int(aw / 2), fill=AXON)
    speed = {"good": 420, "myelin_bad": 140, "axon_bad": 420, "block": 420, "bare": 420}[mode]
    px = x0 + (t * speed) % (x1 - x0)
    stop = x0 + (x1 - x0) * 0.55
    if mode == "block" and px > stop: px = stop
    r = h * (0.45 if mode != "axon_bad" else 0.22)
    d.ellipse((px - r, y - r, px + r, y + r), fill=(255, 111, 0), outline=WHITE, width=4)
    if mode == "block":
        d.line((stop + 30, y - h, stop + 30, y + h), fill=RED, width=12)

def gauge(d, cx, cy, r, v):
    d.arc((cx - r, cy - r, cx + r, cy + r), 180, 360, fill=(200, 210, 225), width=28)
    d.arc((cx - r, cy - r, cx + r, cy + r), 180, 180 + 180 * v, fill=GREEN if v > 0.5 else ORANGE, width=28)
    a = math.pi + math.pi * v
    d.line((cx, cy, cx + 0.8 * r * math.cos(a), cy + 0.8 * r * math.sin(a)), fill=DBLUE, width=10)
    d.ellipse((cx - 18, cy - 18, cx + 18, cy + 18), fill=DBLUE)

# ---------------- scenes ----------------
def n_hook(fr, t, D):
    rays(fr, 540, 900, t, (255, 200, 80), a=40)
    show(fr, pill(TOPIC, PURPLE, size=40), 230, t, 0.1)
    d = ImageDraw.Draw(fr); arm(d, 160, 1300, 720, 1.2, t)
    for k in range(10):
        x = 260 + k * 50 + 15 * math.cos(t * 5 + k); y = 1230 + 25 * math.sin(t * 6 + k * 2)
        d.ellipse((x - 10, y - 10, x + 10, y + 10), fill=YEL)
    pop(fr, white_text("Burning or numb feet?", 72), 540, 470, t, 0.3, "pop")
    pop(fr, white_text("Tingling hands?", 76, color=YEL), 540, 620, t, D * 0.3, "boom")
    pop(fr, box_text("Doctor may ask for an NCV test", GREEN, 46), 540, 820, t, D * 0.6, "whoosh")

def n_wire(fr, t, D):
    show(fr, pill("NERVE = ELECTRIC WIRE", BLUE, size=46), 230, t, 0.1)
    d = ImageDraw.Draw(fr); cable(d, 100, 980, 480, 110, t); fire("pop", 0.3)
    d.text((300, 600), "Axon: the wire", font=font("Bold", 38), fill=(230, 160, 0), anchor="mm")
    d.text((780, 600), "Myelin: the cover", font=font("Bold", 38), fill=(56, 142, 60), anchor="mm")
    show(fr, text_el("Brain  =  nerves  =  hands & feet", 42, "Bold", DBLUE), 1060, t, D * 0.7)
    show(fr, card("Myelin is like plastic on a wire", GREEN, "1", size=40), 760, t, D * 0.3)
    show(fr, card("It helps signals travel FAST", ORANGE, "2", size=40), 895, t, D * 0.55)
    fire("pop", D * 0.3); fire("pop", D * 0.55)

def n_what(fr, t, D):
    show(fr, pill("WHAT DOES NCV MEASURE?", ORANGE, size=46), 230, t, 0.1)
    d = ImageDraw.Draw(fr); arm(d, 120, 470, 620, 0.9, t)
    sticker(d, 230, 420, WIRE[0]); sticker(d, 520, 420, WIRE[1])
    d.line((230, 560, 520, 560), fill=DBLUE, width=5); d.text((375, 595), "distance", font=font("Bold", 32), fill=DBLUE, anchor="mm")
    gauge(d, 880, 520, 120, min(1, 0.2 + t / max(1, D) * 1.2)); fire("pop", 0.3)
    show(fr, text_el("Nerve Conduction Velocity", 52, color=DBLUE), 740, t, D * 0.15)
    show(fr, card("SPEED of the nerve signal", BLUE, "1", size=40), 860, t, D * 0.3)
    show(fr, card("STRENGTH of the signal", PURPLE, "2", size=40), 995, t, D * 0.45)
    fire("pop", D * 0.3); fire("pop", D * 0.45)
    pop(fr, box_text("Speed = distance ÷ time", TEAL, 44), 540, 1170, t, D * 0.65, "ding")

def n_damage(fr, t, D):
    show(fr, pill("WHAT CAN GO WRONG?", RED, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    rows = [("axon_bad", "Wire damaged = WEAK signal", ORANGE), ("myelin_bad", "Cover damaged = SLOW signal", PURPLE), ("block", "Nerve pressed = signal BLOCKED", RED)]
    for i, (m, txt, c) in enumerate(rows):
        tin = 0.3 + i * D * 0.25; fire("pop", tin)
        if t < tin: continue
        y = 400 + i * 300
        cable(d, 120, 960, y, 80, t - tin, m)
        d.text((540, y + 100), txt, font=font("Bold", 42), fill=c, anchor="mm")

def n_cond(fr, t, D):
    show(fr, pill("HELPS FIND", PURPLE, size=50), 230, t, 0.1)
    items = [("Diabetic neuropathy", ORANGE, "1"), ("Carpal tunnel syndrome", BLUE, "2"), ("Bell's palsy (face)", PINK, "3"),
             ("Guillain-Barré syndrome", RED, "4"), ("Nerve injury", TEAL, "5"), ("Nerve pressed by a spine disc", PURPLE, "6")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.08 + 0.13 * i)); show(fr, card(txt, c, m, size=40), 400 + i * 128, t, D * (0.08 + 0.13 * i))
    show(fr, text_el("Only if your doctor advises", 42, "Medium", GREEN), 1200, t, D * 0.88)

def n_how(fr, t, D):
    show(fr, pill("HOW IS IT DONE?", GREEN, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr); arm(d, 140, 500, 640, 1.0, t)
    sticker(d, 250, 450, WIRE[0]); sticker(d, 560, 450, WIRE[1]); sticker(d, 770, 450, WIRE[2])
    if int(t * 3) % 2 == 0 and t > 0.5:
        for k in range(4): d.line((250, 450, 230 + 40 * math.cos(k * 1.6), 380 + 20 * math.sin(k)), fill=YEL, width=6)
    monitor(d, 820, 580, 1010, 740, t, rows=2); fire("pop", 0.3)
    show(fr, card("Sticker electrodes on the skin", BLUE, "1", size=40), 860, t, D * 0.15)
    show(fr, card("Mild pulse: a quick 'jhatka'", ORANGE, "2", size=40), 995, t, D * 0.3)
    show(fr, card("No pain afterwards", GREEN, "3", size=40), 1130, t, D * 0.45)
    show(fr, card("Usually NO needle (EMG uses one)", PURPLE, "4", size=38), 1265, t, D * 0.65)
    for k in (0.15, 0.3, 0.45, 0.65): fire("pop", D * k)

def n_prep(fr, t, D):
    show(fr, pill("BEFORE THE TEST", PURPLE, size=48), 230, t, 0.1)
    items = [("No lotion, cream, oil, sunscreen, perfume", RED, "1"), ("Wear loose clothes", BLUE, "2"),
             ("Pacemaker? Tell them first", ORANGE, "3"), ("Keep hands & feet WARM", GREEN, "4")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.08 + 0.15 * i)); show(fr, card(txt, c, m, size=36), 420 + i * 135, t, D * (0.08 + 0.15 * i))
    d = ImageDraw.Draw(fr); show(fr, text_el("Cold nerve = slow signal", 46, color=DBLUE), 1010, t, D * 0.7)
    if t > D * 0.7:
        cable(d, 160, 920, 1150, 70, t, "myelin_bad")
        d.text((540, 1250), "= report may be wrong", font=font("Bold", 40), fill=RED, anchor="mm")

def n_time(fr, t, D):
    show(fr, pill("TIME & AGE", BLUE, size=50), 230, t, 0.1)
    d = ImageDraw.Draw(fr); cx, cy, r = 540, 510, 140
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=WHITE, outline=BLUE, width=12)
    a = -math.pi / 2 + t * 1.2
    d.line((cx, cy, cx + 0.8 * r * math.cos(a), cy + 0.8 * r * math.sin(a)), fill=RED, width=10); fire("pop", 0.3)
    show(fr, card("15 minutes to over 1 hour", BLUE, "1", size=42), 740, t, D * 0.15)
    show(fr, text_el("depends on how many nerves are tested", 36, "Medium", GREY), 850, t, D * 0.2)
    show(fr, card("Small children: slower nerves", PINK, "2", size=40), 970, t, D * 0.5)
    show(fr, text_el("so results are read by AGE", 40, "Medium", DBLUE), 1080, t, D * 0.55)
    fire("pop", D * 0.15); fire("pop", D * 0.5)

def n_report(fr, t, D):
    show(fr, pill("THE REPORT", ORANGE, size=50), 230, t, 0.1)
    d = ImageDraw.Draw(fr); monitor(d, 120, 360, 960, 620, t, rows=3); fire("pop", 0.3)
    show(fr, text_el("Normal NCV does not always mean", 44, color=RED), 740, t, D * 0.15)
    show(fr, text_el("the nerve has no damage", 44, color=RED), 805, t, D * 0.15); fire("boom", D * 0.15)
    show(fr, card("Normal range differs a little by lab", BLUE, "1", size=38), 930, t, D * 0.4)
    fire("pop", D * 0.4)
    pop(fr, box_text("Doctor reads it with your symptoms", GREEN, 42), 540, 1110, t, D * 0.6, "ding")

SC = [(n_hook, "purple"), (n_wire, "light"), (n_what, "light"), (n_damage, "light"), (n_cond, "light"),
      (n_how, "light"), (n_prep, "light"), (n_time, "light"), (n_report, "light"),
      (close_scene("Do your feet ever burn or feel numb?", TOPIC), "light")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si in range(10):
            fn, bg = SC[si]; d = 14; p = 0.95; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((360, 640)))
        s = Image.new("RGB", (360 * 5, 640 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 360, (i // 5) * 640))
        s.save("sheet.png")
    else: run(SC, "/tmp/ncv_", "NCV_Nerve_Test_Hindi.mp4")
