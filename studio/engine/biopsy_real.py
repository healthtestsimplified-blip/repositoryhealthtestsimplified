"""Biopsy video, realistic documentary style."""
import math, sys
from cbc_cartoon import run
from real_style import *
from hts_close import close_scene

TOPIC = "BIOPSY  •  HISTOPATHOLOGY"
TEX = he_tissue(1400, 3)
TEX2 = he_tissue(1400, 21, glands=6)
DAB = he_tissue(1000, 9, stain="dab")
US = us_base()
JAR = jar_sprite(); CAS = cassette_sprite(); BLOCK = cassette_sprite(wax=True); SLIDE = slide_sprite(TEX)
NEED_CORE = needle_sprite("core"); NEED_FINE = needle_sprite("fine"); REPORT = report_sprite()
EP_CACHE = {}

def dots(fr, n): fr.alpha_composite(chapter(n, 9), (0, 110))

def ep(fr, tex, cx, cy, size, t, D, z0=1.0, z1=1.3, focus=0.0, pan=(0.3, 0.1)):
    im = eyepiece(tex, size, t, z0, z1, D, pan, focus)
    fr.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))

def b_hook(fr, t, D):
    fullbleed(fr, TEX, t, D, 1.0, 1.25)
    show(fr, kicker("Biopsy  •  Histopathology", CYAN), 330, t, 0.1)
    type_on(fr, "Doctor has advised a biopsy?", 410, t, 0.4, 72)
    if t > D * 0.35: type_on(fr, "Scared? Don't be.", 600, t, D * 0.35, 72, AMBER)
    show(fr, callout("What a biopsy is, and how it's done", CYAN, 40), 1620, t, D * 0.6); fire("whoosh", D * 0.6)

def b_what(fr, t, D):
    dots(fr, 1)
    show(fr, kicker("What is a biopsy?"), 260, t, 0.1)
    show(fr, headline("A tiny piece of tissue, checked under a microscope", 56), 320, t, 0.3)
    p = ease((t - 0.4) / 0.7)
    if p > 0: put(fr, JAR, 260, 760, 0.95, p)
    if t > D * 0.25: ep(fr, TEX, 730, 760, 520, t - D * 0.25, D, 1.0, 1.4, focus=max(0, 1 - (t - D * 0.25) / 1.2))
    show(fr, gcard("A small piece of tissue or a few cells are taken", CYAN, 1, 38), 1110, t, D * 0.2)
    show(fr, gcard("A pathologist (lab specialist doctor) examines it under a microscope", AMBER, 2, 36), 1260, t, D * 0.45)
    fire("pop", D * 0.2); fire("pop", D * 0.45)

def b_notcancer(fr, t, D):
    dots(fr, 2)
    show(fr, kicker("Remember", TEALG), 260, t, 0.1)
    show(fr, headline("Biopsy does not mean cancer", 64), 320, t, 0.3)
    ep(fr, TEX2, 540, 800, 620, t, D, 1.1, 1.35)
    chips = [("Infection", CYAN, 170, 560), ("Inflammation", AMBER, 830, 600), ("TB", LAV, 180, 1060), ("Tumour", CORAL, 880, 1040)]
    for i, (lab, c, x, y) in enumerate(chips):
        tin = D * (0.2 + 0.12 * i); fire("pop", tin)
        if t < tin: continue
        f = font("Bold", 36); tw = f.getlength(lab)
        lay, d = overlay(fr)
        d.rounded_rectangle((x - tw / 2 - 28, y - 34, x + tw / 2 + 28, y + 34), 34, fill=(*INK, 220), outline=c, width=3)
        d.text((x, y), lab, font=f, fill=c, anchor="mm"); fr.alpha_composite(lay)
    show(fr, gcard("It is done to get the right diagnosis", TEALG, None, 40), 1230, t, D * 0.7)

def b_types(fr, t, D):
    dots(fr, 3)
    show(fr, kicker("Types of biopsy"), 260, t, 0.1)
    show(fr, headline("Ultrasound / CT guided needle", 54), 320, t, 0.3)
    ultrasound(fr, 90, 430, t, US, (t - D * 0.15) / (D * 0.35))
    rows = [("FNAC", "thin needle: a few cells", CYAN), ("Trucut / core", "thicker needle: a tissue core", AMBER),
            ("Punch", "small round piece of skin", LAV), ("Surgical", "the whole lump is removed", CORAL)]
    lay, d = overlay(fr)
    for i, (a, b, c) in enumerate(rows):
        tin = D * (0.35 + 0.13 * i); fire("pop", tin)
        if t < tin: continue
        y = 1240 + i * 120; e = ease((t - tin) / 0.4)
        d.rounded_rectangle((X0, y, X0 + TW, y + 100), 22, fill=(255, 255, 255, int(20 * e)), outline=(255, 255, 255, int(46 * e)), width=2)
        d.text((X0 + 34, y + 50), a, font=font("Bold", 38), fill=(*c, int(255 * e)), anchor="lm")
        d.text((X0 + 360, y + 50), b, font=font("Regular", 34), fill=(*SOFT, int(255 * e)), anchor="lm")
    fr.alpha_composite(lay)

def b_prep(fr, t, D):
    dots(fr, 4)
    show(fr, kicker("Before the biopsy"), 260, t, 0.1)
    items = [("Tell the doctor all your medicines, especially blood thinners", CORAL),
             ("Stop a medicine only if the doctor says so", AMBER),
             ("Some biopsies need an empty stomach", CYAN),
             ("Allergy or pregnancy? Tell them", LAV), ("Bring someone along", TEALG)]
    for i, (txt, c) in enumerate(items):
        fire("pop", D * (0.08 + 0.15 * i)); show(fr, gcard(txt, c, i + 1, 37), 360 + i * 170, t, D * (0.08 + 0.15 * i))
    ep(fr, TEX2, 540, 1480, 380, t, D, 1.2, 1.4)

def b_feel(fr, t, D):
    dots(fr, 5)
    show(fr, kicker("Does it hurt?"), 260, t, 0.1)
    show(fr, headline("Usually done with numbing medicine", 60), 320, t, 0.3)
    put(fr, NEED_FINE, 540, 640, 1.0, ease((t - 0.4) / 0.6))
    show(fr, gcard("Mild pain or a bruise afterwards is common", AMBER, 1, 38), 800, t, D * 0.25)
    show(fr, headline("Contact your doctor if:", 46, CORAL), 990, t, D * 0.45)
    show(fr, gcard("Bleeding doesn't stop", CORAL, None, 38), 1080, t, D * 0.5)
    show(fr, gcard("Swelling, redness, or fever", CORAL, None, 38), 1210, t, D * 0.6)
    fire("pop", D * 0.25); fire("boom", D * 0.45)

STEPS = [("1", "Kept safe in formalin", "JAR"), ("2", "Set in a wax block", "BLOCK"), ("3", "Microtome cuts thin sections", "RIBBON"),
         ("4", "Stained on a glass slide", "SLIDE"), ("5", "Pathologist examines it", "SCOPE")]
def b_lab(fr, t, D):
    dots(fr, 6)
    show(fr, kicker("Journey in the lab"), 260, t, 0.1)
    seg = (D - 1.0) / len(STEPS); k = min(len(STEPS) - 1, int(max(0, t - 0.5) / seg)); lt = t - 0.5 - k * seg
    num, lab, obj = STEPS[k]; fire("whoosh", 0.5 + k * seg)
    a = min(1, lt / 0.4, (seg - lt) / 0.3) if k < len(STEPS) - 1 else min(1, lt / 0.4)
    a = max(0, a); sc = 1.0 + 0.04 * lt / seg
    if obj == "JAR": put(fr, JAR, 540, 860, 1.4 * sc, a)
    elif obj == "BLOCK": put(fr, BLOCK, 540, 860, 1.6 * sc, a); put(fr, CAS, 300, 1120, 0.6, a * 0.8)
    elif obj == "RIBBON": put(fr, ribbon_sprite(t), 540, 860, 1.0 * sc, a)
    elif obj == "SLIDE": put(fr, SLIDE, 540, 860, 1.15 * sc, a)
    else:
        im = eyepiece(TEX, 640, lt, 1.0, 1.4, seg, (0.3, 0.1), max(0, 1 - lt / 1.0))
        put(fr, im, 540, 860, 1.0, a)
    lay, d = overlay(fr)
    for i in range(len(STEPS)):
        x = 240 + i * 150; c = CYAN if i <= k else (255, 255, 255, 60)
        d.ellipse((x - 22, 1290 - 22, x + 22, 1290 + 22), fill=c if i <= k else None, outline=c, width=3)
        d.text((x, 1290), str(i + 1), font=font("Bold", 24), fill=INK if i <= k else (255, 255, 255, 120), anchor="mm")
        if i < len(STEPS) - 1: d.line((x + 26, 1290, x + 124, 1290), fill=(255, 255, 255, 60), width=3)
    d.text((540, 1420), lab, font=font("Bold", 52), fill=(255, 255, 255, int(255 * a)), anchor="mm")
    fr.alpha_composite(lay)

def b_report(fr, t, D):
    dots(fr, 7)
    show(fr, kicker("The report"), 260, t, 0.1)
    show(fr, headline("Usually a few days to about a week", 58), 320, t, 0.3)
    put(fr, REPORT, 330, 800, 0.85, ease((t - 0.4) / 0.6))
    if t > D * 0.3:
        ep(fr, DAB, 790, 760, 420, t - D * 0.3, D, 1.0, 1.25)
        lay, d = overlay(fr); d.text((790, 1010), "IHC special stain", font=font("Medium", 32), fill=SOFT, anchor="mm"); fr.alpha_composite(lay)
    show(fr, gcard("Special tests like IHC may take longer", AMBER, 1, 38), 1150, t, D * 0.4)
    show(fr, gcard("Always understand the report with your doctor", CYAN, 2, 38), 1300, t, D * 0.65)
    fire("pop", D * 0.4); fire("pop", D * 0.65)

def b_myth(fr, t, D):
    fullbleed(fr, TEX2, t, D, 1.15, 1.3); dots(fr, 8)
    show(fr, kicker("Myth vs fact", CORAL), 300, t, 0.1)
    show(fr, headline("“Biopsy spreads cancer”", 62, WHITE), 370, t, 0.3)
    if t > D * 0.25:
        lay, d = overlay(fr); e = ease((t - D * 0.25) / 0.4)
        d.line((X0 - 10, 412, X0 - 10 + 820 * e, 412), fill=CORAL, width=9); fr.alpha_composite(lay); fire("boom", D * 0.25)
    show(fr, headline("FACT: extremely rare", 74, TEALG), 640, t, D * 0.35)
    show(fr, body("American Cancer Society: the benefits of a biopsy far outweigh this very small risk.", 40, SOFT), 770, t, D * 0.45)
    show(fr, callout("Right diagnosis = right treatment", TEALG, 44), 1500, t, D * 0.7); fire("ding", D * 0.7)

SC = [(film(b_hook), "doc"), (film(b_what), "doc"), (film(b_notcancer), "doc"), (film(b_types), "doc"), (film(b_prep), "doc"),
      (film(b_feel), "doc"), (film(b_lab), "doc"), (film(b_report), "doc"), (film(b_myth), "doc"),
      (close_scene("Were you ever scared of a biopsy?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        D = [14, 14, 15, 22, 18, 18, 24, 17, 20, 33]; ps = [0.95] * 10
        if len(sys.argv) > 2: ps = [float(sys.argv[2])] * 10
        ims = []
        for si in range(10):
            fn, bg = SC[si]; d = D[si]; p = ps[si]; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((360, 640)))
        s = Image.new("RGB", (360 * 5, 640 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 360, (i // 5) * 640))
        s.save("sheet.png")
    else: run(SC, "/tmp/bio_", "Biopsy_Test_Hindi.mp4")
