import math, sys
from cbc_cartoon import run
from alz_cartoon import brain
from eeg_cartoon import monitor, SKIN, WIRE
from lft_cartoon2 import *
from chromo_cartoon import PINK
from hts_close import close_scene

TOPIC = "NERVES & MUSCLES"
NERVE = (255, 202, 40); MUSCLE = (239, 83, 80); SKIN_D = (230, 170, 120)

def arm(d, x0, y, x1, s=1.0, t=0.0, pulse=True, nerve=True, muscle=False, blocked=None):
    """Horizontal forearm from x0 (elbow) to x1 (wrist) with a hand."""
    h = 120 * s
    d.rounded_rectangle((x0, y - h / 2, x1, y + h / 2), int(h / 2), fill=SKIN, outline=SKIN_D, width=4)
    d.ellipse((x1 - 30 * s, y - 85 * s, x1 + 130 * s, y + 85 * s), fill=SKIN, outline=SKIN_D, width=4)
    for k in range(4):
        fy = y - 60 * s + k * 40 * s
        d.rounded_rectangle((x1 + 100 * s, fy - 14 * s, x1 + 190 * s, fy + 14 * s), int(14 * s), fill=SKIN, outline=SKIN_D, width=3)
    if muscle:
        d.ellipse((x0 + 40 * s, y - 45 * s, x0 + (x1 - x0) * 0.6, y + 45 * s), fill=(255, 138, 128))
        for k in range(5):
            xx = x0 + 70 * s + k * (x1 - x0) * 0.09
            d.line((xx, y - 30 * s, xx + 20 * s, y + 30 * s), fill=MUSCLE, width=4)
    if nerve:
        d.line((x0 - 60 * s, y + 20 * s, x1 + 60 * s, y + 20 * s), fill=NERVE, width=int(10 * s))
        if pulse:
            for k in range(3):
                px = x0 - 60 * s + ((t * 300 * s + k * (x1 - x0) / 3) % (x1 - x0 + 120 * s))
                if blocked and px > blocked: continue
                d.polygon([(px, y - 10 * s), (px + 16 * s, y + 20 * s), (px + 4 * s, y + 20 * s), (px + 14 * s, y + 50 * s), (px - 10 * s, y + 12 * s), (px + 2 * s, y + 12 * s)], fill=(255, 111, 0))
        if blocked:
            d.ellipse((blocked - 30 * s, y - 10 * s, blocked + 30 * s, y + 50 * s), outline=RED, width=int(7 * s))

def sticker(d, x, y, col, s=1.0):
    d.ellipse((x - 28 * s, y - 28 * s, x + 28 * s, y + 28 * s), fill=WHITE, outline=col, width=5)
    d.ellipse((x - 9 * s, y - 9 * s, x + 9 * s, y + 9 * s), fill=col)

def needle(d, x, y, s=1.0):
    d.line((x, y, x + 120 * s, y - 160 * s), fill=(176, 190, 197), width=int(5 * s))
    d.rounded_rectangle((x + 110 * s, y - 210 * s, x + 150 * s, y - 150 * s), 8, fill=(144, 164, 174))
    d.line((x + 145 * s, y - 200 * s, x + 260 * s, y - 280 * s), fill=WIRE[1], width=5)

# ---------------- scenes ----------------
def m_hook(fr, t, D):
    rays(fr, 540, 900, t, (255, 200, 80), a=40)
    show(fr, pill(TOPIC, PURPLE, size=40), 230, t, 0.1)
    d = ImageDraw.Draw(fr); arm(d, 180, 1250, 700, 1.1, t, pulse=True)
    for k in range(6):
        a = t * 5 + k
        x = 420 + 60 * k; y = 1100 + 25 * math.sin(a)
        d.text((x, y), "*", font=font("Bold", 70), fill=YEL, anchor="mm")
    pop(fr, white_text("Tingling? Numbness?", 76), 540, 470, t, 0.3, "pop")
    pop(fr, white_text("Weak muscles?", 76, color=YEL), 540, 620, t, D * 0.3, "boom")
    pop(fr, box_text("Doctor may ask for EMG & NCV", GREEN, 48), 540, 820, t, D * 0.6, "whoosh")

def m_what(fr, t, D):
    show(fr, pill("WHAT ARE EMG & NCV?", BLUE, size=46), 230, t, 0.1)
    d = ImageDraw.Draw(fr); brain(d, 180, 500, 110); arm(d, 330, 520, 760, 0.9, t, muscle=True); fire("pop", 0.3)
    d.text((540, 660), "Brain  =  nerve  =  muscle", font=font("Bold", 40), fill=DBLUE, anchor="mm")
    show(fr, card("EMG: electrical activity of MUSCLES", PURPLE, "1", size=38), 800, t, D * 0.3)
    show(fr, card("NCV: how fast & strong NERVE signals go", ORANGE, "2", size=36), 935, t, D * 0.55)
    fire("pop", D * 0.3); fire("pop", D * 0.55)
    pop(fr, box_text("Often done together", TEAL, 44), 540, 1110, t, D * 0.75, "ding")

def m_when(fr, t, D):
    show(fr, pill("WHEN IS IT ADVISED?", ORANGE, size=48), 230, t, 0.1)
    items = [("Tingling or numbness: hands, feet, face", PURPLE, "1"), ("Muscle weakness", RED, "2"),
             ("Cramps, spasms or twitching", BLUE, "3"), ("Paralysis of any muscle", ORANGE, "4")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.1 + 0.17 * i)); show(fr, card(txt, c, m, size=37), 420 + i * 135, t, D * (0.1 + 0.17 * i))
    d = ImageDraw.Draw(fr); arm(d, 220, 1150, 720, 0.9, t, blocked=520 if t > D * 0.6 else None)
    show(fr, text_el("Only if your doctor advises", 42, "Medium", GREEN), 1350, t, D * 0.8)

def m_conditions(fr, t, D):
    show(fr, pill("HELPS FIND", PURPLE, size=50), 230, t, 0.1)
    items = [("Carpal tunnel: nerve pressed at wrist", BLUE, "1"), ("Neuropathy: common in diabetes", ORANGE, "2"),
             ("Nerve pressed by a spine disc", RED, "3"), ("Myasthenia gravis", PURPLE, "4"), ("Some muscle diseases", TEAL, "5")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.1 + 0.14 * i)); show(fr, card(txt, c, m, size=37), 420 + i * 135, t, D * (0.1 + 0.14 * i))
    pop(fr, box_text("Shows WHERE and HOW MUCH damage", GREEN, 42), 540, 1160, t, D * 0.85, "ding")

def m_ncv(fr, t, D):
    show(fr, pill("STEP 1: NCV", ORANGE, size=50), 230, t, 0.1)
    d = ImageDraw.Draw(fr); arm(d, 150, 520, 640, 1.0, t)
    sticker(d, 260, 470, WIRE[0]); sticker(d, 560, 470, WIRE[1]); sticker(d, 760, 470, WIRE[2])
    if int(t * 3) % 2 == 0 and t > 0.5:
        for k in range(4): d.line((260, 470, 240 + 40 * math.cos(k * 1.6), 400 + 20 * math.sin(k)), fill=YEL, width=6)
    monitor(d, 820, 600, 1010, 760, t, rows=2); fire("pop", 0.3)
    show(fr, card("Sticker electrodes on the skin", BLUE, "1", size=40), 880, t, D * 0.2)
    show(fr, card("Very mild electric pulse", ORANGE, "2", size=40), 1015, t, D * 0.4)
    show(fr, card("A quick tingle for a few seconds", GREEN, "3", size=40), 1150, t, D * 0.6)
    fire("pop", D * 0.2); fire("pop", D * 0.4); fire("pop", D * 0.6)

def m_emg(fr, t, D):
    show(fr, pill("STEP 2: NEEDLE EMG", PURPLE, size=48), 230, t, 0.1)
    d = ImageDraw.Draw(fr); arm(d, 150, 640, 640, 1.0, t, nerve=False, muscle=True); needle(d, 330, 620, 0.85)
    monitor(d, 680, 400, 1010, 580, t, kind="spike", rows=2); fire("pop", 0.3)
    show(fr, card("Very thin needle into the muscle", PURPLE, "1", size=38), 800, t, D * 0.15)
    show(fr, card("Relax the muscle, then tighten gently", BLUE, "2", size=37), 935, t, D * 0.3)
    show(fr, card("Some pain: settles soon after", ORANGE, "3", size=38), 1070, t, D * 0.5)
    fire("pop", D * 0.15); fire("pop", D * 0.3); fire("pop", D * 0.5)
    pop(fr, box_text("Too painful? Tell the doctor", RED, 42), 540, 1240, t, D * 0.75, "ding")

def m_prep(fr, t, D):
    show(fr, pill("BEFORE THE TEST", GREEN, size=48), 230, t, 0.1)
    items = [("Bathe before the test", BLUE, "1"), ("No cream, lotion or oil on skin", RED, "2"),
             ("Wear loose clothes", PURPLE, "3"), ("Usually no fasting needed", GREEN, "4")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.1 + 0.18 * i)); show(fr, card(txt, c, m, size=40), 440 + i * 140, t, D * (0.1 + 0.18 * i))
    d = ImageDraw.Draw(fr)
    for k in range(7):
        bx = 260 + k * 95; by = 1100 + 20 * math.sin(t * 3 + k)
        d.ellipse((bx - 24, by - 24, bx + 24, by + 24), outline=(100, 180, 255), width=5)

def m_tell(fr, t, D):
    show(fr, pill("TELL YOUR DOCTOR", RED, size=50), 230, t, 0.1)
    show(fr, card("Pacemaker or heart device", RED, "!", size=42), 440, t, 0.3)
    show(fr, card("Blood thinner medicines", ORANGE, "!", size=42), 580, t, D * 0.25)
    fire("boom", 0.3); fire("pop", D * 0.25)
    pop(fr, box_text("Never stop any medicine on your own", PURPLE, 42), 540, 790, t, D * 0.5, "ding")
    show(fr, text_el("Ask your doctor first", 44, "Medium", GREEN), 920, t, D * 0.65)
    if t > D * 0.65: put(fr, DOC["aim"], 540, 1250, 0.8)

def m_after(fr, t, D):
    show(fr, pill("TIME & REPORT", BLUE, size=50), 230, t, 0.1)
    d = ImageDraw.Draw(fr); cx, cy, r = 540, 520, 150
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=WHITE, outline=BLUE, width=12)
    a = -math.pi / 2 + t * 1.2
    d.line((cx, cy, cx + 0.8 * r * math.cos(a), cy + 0.8 * r * math.sin(a)), fill=RED, width=10)
    d.line((cx, cy, cx + 0.5 * r * math.cos(a / 12), cy + 0.5 * r * math.sin(a / 12)), fill=DBLUE, width=12); fire("pop", 0.3)
    show(fr, card("About 30 minutes to 1.5 hours", BLUE, "1", size=40), 760, t, D * 0.15)
    show(fr, text_el("depends on how many nerves are tested", 36, "Medium", GREY), 870, t, D * 0.2)
    show(fr, card("Mild soreness or bruise for 1–2 days", ORANGE, "2", size=38), 980, t, D * 0.45)
    show(fr, card("Report by a neurologist", PURPLE, "3", size=40), 1115, t, D * 0.65)
    fire("pop", D * 0.15); fire("pop", D * 0.45); fire("pop", D * 0.65)
    pop(fr, box_text("Doctor explains it with your symptoms", GREEN, 40), 540, 1290, t, D * 0.8, "ding")

SC = [(m_hook, "purple"), (m_what, "light"), (m_when, "light"), (m_conditions, "light"), (m_ncv, "light"),
      (m_emg, "light"), (m_prep, "light"), (m_tell, "light"), (m_after, "light"),
      (close_scene("Do your hands or feet tingle?", TOPIC), "light")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si in range(10):
            fn, bg = SC[si]; d = 14; p = 0.95; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((360, 640)))
        s = Image.new("RGB", (360 * 5, 640 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 360, (i // 5) * 640))
        s.save("sheet.png")
    else: run(SC, "/tmp/emg_", "EMG_NCV_Test_Hindi.mp4")
