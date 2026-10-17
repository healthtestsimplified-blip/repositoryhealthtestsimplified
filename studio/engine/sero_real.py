"""Serology profile (HIV 1&2, HBsAg, anti-HCV, VDRL/RPR), realistic documentary style."""
import math, sys, random
from cbc_cartoon import run
from real_style import *
from hts_close import close_scene

TOPIC = "SEROLOGY PROFILE"
NCH = 7
TUBE = tube_sprite((200, 60, 60), "SERUM")

def dots(fr, n): fr.alpha_composite(chapter(n, NCH), (0, 110))

def cards(fr, t, D, items, y0=340, size=35, gap=145, t0=0.1, step=0.11):
    for i, (txt, c) in enumerate(items):
        fire("pop", D * (t0 + step * i)); show(fr, gcard(txt, c, i + 1, size), y0 + i * gap, t, D * (t0 + step * i))

def plate_sprite(seed=3, pos=(5, 18, 40)):
    """ELISA 96-well microplate; a few wells turn yellow (reactive) — illustration."""
    w, h = 860, 600; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((14, 14, w, h), 30, fill=(0, 0, 0, 90)); d.rounded_rectangle((0, 0, w - 14, h - 14), 30, fill=(236, 240, 246))
    r = random.Random(seed)
    for i in range(8):
        d.text((30, 70 + i * 64), "ABCDEFGH"[i], font=font("Bold", 24), fill=(90, 100, 120), anchor="mm")
        for j in range(12):
            x = 80 + j * 63; y = 70 + i * 64; k = i * 12 + j
            if k in pos: col = (250, 205, 40)
            elif k < 4: col = (250, 236, 170) if k == 1 else (240, 244, 250)
            else: col = (250, 248, 225) if r.random() < 0.15 else (242, 246, 250)
            d.ellipse((x - 24, y - 24, x + 24, y + 24), fill=col, outline=(180, 188, 200), width=3)
    for j in range(12): d.text((80 + j * 63, 32), str(j + 1), font=font("Bold", 22), fill=(90, 100, 120), anchor="mm")
    return with_glow(im, (200, 230, 255), 10, 40)
PLATE = plate_sprite()

def sero_report():
    w, h = 820, 720; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((14, 14, w, h), fill=(0, 0, 0, 90)); d.rectangle((0, 0, w - 14, h - 14), fill=(251, 251, 248))
    d.rectangle((0, 0, w - 14, 90), fill=(16, 42, 78))
    d.text((30, 45), "SEROLOGY PROFILE  (sample layout)", font=font("Bold", 30), fill=WHITE, anchor="lm")
    d.text((30, 130), "Test", font=font("Bold", 26), fill=(90, 100, 120)); d.text((470, 130), "Result", font=font("Bold", 26), fill=(90, 100, 120))
    d.line((30, 170, w - 44, 170), fill=(190, 195, 205), width=2)
    rows = [("HIV 1 & 2 (Ag/Ab)", "Non-reactive"), ("HBsAg", "Non-reactive"), ("Anti-HCV", "Non-reactive"), ("VDRL / RPR", "Non-reactive")]
    for i, (a, b) in enumerate(rows):
        y = 200 + i * 100
        d.text((30, y), a, font=font("Medium", 30), fill=(20, 30, 60)); d.text((470, y), b, font=font("Bold", 30), fill=(30, 140, 90))
        d.line((30, y + 60, w - 44, y + 60), fill=(225, 228, 235), width=2)
    d.text((30, 620), "Reactive results need confirmatory testing.", font=font("Regular", 24), fill=(90, 100, 120))
    return im
REPORT = sero_report()

def window(fr, y, t, tin):
    panel(fr, X0, y, TW, 330, "HIV lab test (antigen/antibody): when can it detect?")
    lay, d = overlay(fr); e = ease((t - tin) / 1.2)
    x0, x1 = X0 + 40, X0 + TW - 40; yy = y + 190; sc = (x1 - x0) / 90
    d.line((x0, yy, x0 + (x1 - x0) * e, yy), fill=(*SOFT, 200), width=5)
    if e > 0.2: d.rounded_rectangle((x0 + 18 * sc, yy - 30, x0 + min(45, 90 * e) * sc, yy + 30), 20, fill=(*AMBER, 200))
    for dday, lab in ((0, "Exposure"), (18, "Day 18"), (45, "Day 45")):
        if dday / 90 > e: continue
        xx = x0 + dday * sc; d.line((xx, yy - 50, xx, yy + 50), fill=(*WHITE, 230), width=4)
        d.text((xx, yy + 80), lab, font=font("Bold", 28), fill=SOFT, anchor="mm")
    if e > 0.6: d.text((x0 + 31.5 * sc, yy - 60), "can detect", font=font("Bold", 28), fill=AMBER, anchor="mm")
    fr.alpha_composite(lay)

# ---------------- scenes ----------------
def s_hook(fr, t, D):
    show(fr, kicker("Blood test explained", CYAN), 250, t, 0.1)
    type_on(fr, "Serology Profile", 310, t, 0.3, 76)
    if t > D * 0.22: type_on(fr, "HIV • Hepatitis B • Hepatitis C • Syphilis", 420, t, D * 0.22, 40, AMBER)
    for i in range(4): put(fr, TUBE, 210 + i * 220, 830, 0.85, ease((t - 0.6 - 0.2 * i) / 0.5))
    for i, (txt, c) in enumerate((("Before surgery", CYAN), ("In pregnancy", LAV), ("Before dialysis", TEALG))):
        fire("pop", D * (0.45 + 0.1 * i)); show(fr, gcard(txt, c, None, 36), 1130 + i * 140, t, D * (0.45 + 0.1 * i))
    show(fr, callout("Watch till the end", CORAL, 38), 1600, t, D * 0.8)

def s_what(fr, t, D):
    dots(fr, 1); show(fr, kicker("What is checked?"), 260, t, 0.1)
    cards(fr, t, D, [("HIV 1 & 2", CORAL), ("Hepatitis B: HBsAg", AMBER), ("Hepatitis C: anti-HCV", LAV), ("Syphilis: VDRL or RPR", CYAN)], 330, 36, 140, 0.08, 0.1)
    put(fr, PLATE, 540, 1150, 0.95, ease((t - D * 0.45) / 0.6))
    show(fr, body("ELISA / CLIA plate (illustration)  •  No fasting needed", 30, MUTED), 1470, t, D * 0.5)
    show(fr, callout("Report says: Reactive or Non-reactive", TEALG, 36), 1560, t, D * 0.65)

def s_why(fr, t, D):
    dots(fr, 2); show(fr, kicker("Why is it done?"), 260, t, 0.1)
    cards(fr, t, D, [("Before surgery, endoscopy, dialysis: protects patient and health workers", CYAN), ("In pregnancy: to protect the baby", LAV),
                     ("After a needle-stick injury", AMBER)], 330, 33, 165, 0.1, 0.15)
    put(fr, needle_sprite("core"), 540, 1060, 0.8, ease((t - D * 0.55) / 0.6))

def s_hiv(fr, t, D):
    dots(fr, 3); show(fr, kicker("HIV 1 & 2", CORAL), 260, t, 0.1)
    show(fr, gcard("Lab test checks antibody and antigen", CORAL, 1, 35), 330, t, 0.3)
    window(fr, 490, t, D * 0.15)
    show(fr, gcard("Tested too early? A repeat test may be needed", AMBER, 2, 34), 880, t, D * 0.4)
    show(fr, gcard("Reactive: confirmatory tests are essential", CYAN, 3, 34), 1030, t, D * 0.55)
    show(fr, callout("Done with consent; the result is confidential", TEALG, 34), 1190, t, D * 0.7)
    show(fr, source_tag("HIV.gov: HIV testing overview (window periods)"), 1330, t, D * 0.72)

def s_hbv(fr, t, D):
    dots(fr, 4); show(fr, kicker("Hepatitis B: HBsAg", AMBER), 260, t, 0.1)
    show(fr, headline("HBsAg present = current hepatitis B infection", 54), 320, t, 0.3)
    cards(fr, t, D, [("Present for more than 6 months: chronic infection", AMBER), ("Doctor orders liver tests and more", CYAN),
                     ("Family can be protected by the vaccine", TEALG)], 520, 34, 150, 0.25, 0.15)

def s_hcv(fr, t, D):
    dots(fr, 5); show(fr, kicker("Hepatitis C: anti-HCV", LAV), 260, t, 0.1)
    show(fr, headline("Antibody = infection now or in the past", 56), 320, t, 0.3)
    cards(fr, t, D, [("HCV RNA test confirms current infection", CYAN), ("Some people clear the virus on their own", LAV)], 520, 34, 150, 0.2, 0.15)
    counter(fr, 95, "%", 860, t, D * 0.55, size=140, col=TEALG, prefix=">")
    show(fr, body("cure rate with today's medicines (direct-acting antivirals)", 34, SOFT), 1040, t, D * 0.6)
    show(fr, source_tag("WHO hepatitis C fact sheet"), 1160, t, D * 0.65)

def s_vdrl(fr, t, D):
    dots(fr, 6); show(fr, kicker("Syphilis: VDRL / RPR", CYAN), 260, t, 0.1)
    show(fr, headline("A screening test", 58), 320, t, 0.3)
    cards(fr, t, D, [("Can be falsely positive: pregnancy, TB, autoimmune disease, some viral infections", AMBER),
                     ("Confirmed with a specific test such as TPHA", CYAN), ("Treatable with penicillin; vital in pregnancy", TEALG)], 450, 33, 165, 0.2, 0.15)

def s_remember(fr, t, D):
    dots(fr, 7); show(fr, kicker("Remember"), 260, t, 0.1)
    put(fr, REPORT, 540, 640, 0.72, ease((t - 0.3) / 0.6))
    cards(fr, t, D, [("Reactive screening is not a final diagnosis", AMBER), ("These infections can be treated or controlled: no fear, no blame", TEALG),
                     ("Keep the report confidential; show your doctor", CYAN)], 960, 33, 160, 0.3, 0.15)

SC = [(film(s_hook), "doc"), (film(s_what), "doc"), (film(s_why), "doc"), (film(s_hiv), "doc"), (film(s_hbv), "doc"),
      (film(s_hcv), "doc"), (film(s_vdrl), "doc"), (film(s_remember), "doc"), (close_scene("Had this test before surgery?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si, (fn, bg) in enumerate(SC):
            d = 16 if si < len(SC) - 1 else 33; p = .95 if si else 0.125; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((360, 640)))
        s = Image.new("RGB", (360 * 5, 640 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 360, (i // 5) * 640))
        s.save("sheet_sero.png")
    else: run(SC, "/tmp/ser_", "Serology_Profile_Hindi.mp4")
