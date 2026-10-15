"""X-ray vs CT vs MRI: differences and when doctors recommend each (realistic documentary style)."""
import math, sys, random
from cbc_cartoon import run
from real_style import *
from hts_close import close_scene

TOPIC = "X-RAY  •  CT  •  MRI"
NCH = 8

def _gn(w, h, seed, s=1.2):
    a = np.random.default_rng(seed).normal(0, 1, (h, w)).astype(np.float32)
    return np.asarray(Image.fromarray(((a * 30) + 128).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(s))).astype(np.float32) / 255 - 0.5

def _finish(im, seed, blur=4, n1=0.08, n2=0.04, tint=(1, 1, 1)):
    im = im.filter(ImageFilter.GaussianBlur(blur)); w, h = im.size
    a = np.asarray(im).astype(np.float32) / 255 + n1 * _gn(w, h, seed, 1.5) + n2 * _gn(w, h, seed + 1, 0.6)
    g = a.clip(0, 1) * 255
    return Image.merge("RGBA", tuple(Image.fromarray((g * k).clip(0, 255).astype(np.uint8)) for k in tint) + (Image.new("L", (w, h), 255),))

def chest_xray(w=700, h=800, seed=3):
    im = Image.new("L", (w, h), 12); d = ImageDraw.Draw(im)
    d.polygon([(w * .08, h), (w * .1, h * .3), (w * .25, h * .12), (w * .4, h * .06), (w * .6, h * .06), (w * .75, h * .12), (w * .9, h * .3), (w * .92, h)], fill=95)
    for sg in (-1, 1):  # lungs
        cx = w / 2 + sg * w * .19
        d.ellipse((cx - w * .15, h * .16, cx + w * .15, h * .86), fill=38)
    d.ellipse((w * .38, h * .45, w * .66, h * .82), fill=150)  # heart shadow (to patient's left = image right)
    d.rectangle((w * .465, 0, w * .535, h), fill=165)  # spine/mediastinum
    for sg in (-1, 1):  # clavicles
        d.line((w / 2 + sg * w * .05, h * .17, w / 2 + sg * w * .33, h * .12), fill=200, width=16)
    for k in range(9):  # ribs
        y = h * (.19 + k * .072)
        for sg in (-1, 1):
            pts = [(w / 2 + sg * (w * .05 + u * w * .33), y + math.sin(u * math.pi) * -h * .03 + u * h * .07) for u in [i / 20 for i in range(21)]]
            d.line(pts, fill=175, width=11)
    for sg in (-1, 1):  # diaphragm
        cx = w / 2 + sg * w * .2; d.chord((cx - w * .2, h * .78, cx + w * .2, h * 1.0), 180, 360, fill=120)
    return _finish(im, seed, 5, tint=(1, 1, 1.02))

def ct_slice(n=700, seed=6):
    im = Image.new("L", (n, n), 5); d = ImageDraw.Draw(im); c = n / 2
    d.ellipse((n * .06, n * .16, n * .94, n * .84), fill=70)            # subcutaneous fat (dark grey)
    d.ellipse((n * .1, n * .2, n * .9, n * .8), fill=95)               # muscle wall
    d.ellipse((n * .14, n * .24, n * .86, n * .76), fill=60)           # intra-abdominal fat
    d.polygon([(n * .14, n * .45), (n * .2, n * .27), (n * .38, n * .24), (n * .5, n * .3), (n * .48, n * .52), (n * .3, n * .62), (n * .17, n * .6)], fill=135)  # liver
    d.ellipse((n * .62, n * .3, n * .82, n * .48), fill=125)           # spleen
    for x in (.33, .67): d.ellipse((n * (x - .07), n * .5, n * (x + .07), n * .66), fill=150)  # kidneys
    d.ellipse((n * .52, n * .52, n * .58, n * .58), fill=200)          # aorta (contrast)
    d.ellipse((n * .43, n * .6, n * .57, n * .74), fill=230); d.rectangle((n * .48, n * .7, n * .52, n * .78), fill=220)  # vertebra
    r = random.Random(seed)
    for _ in range(9):
        x, y = r.uniform(.4, .75), r.uniform(.33, .5); d.ellipse((n * (x - .04), n * (y - .03), n * (x + .04), n * (y + .03)), fill=115, outline=150, width=3)
    return _finish(im, seed, 2.5, 0.06, 0.05)

def mri_brain(w=700, h=700, seed=9):
    im = Image.new("L", (w, h), 4); d = ImageDraw.Draw(im)
    d.ellipse((w * .08, h * .06, w * .92, h * .86), fill=150)  # scalp
    d.ellipse((w * .11, h * .09, w * .89, h * .83), fill=25)   # skull (dark on MRI)
    d.ellipse((w * .14, h * .12, w * .86, h * .8), fill=70)    # CSF / cortex border
    d.ellipse((w * .16, h * .14, w * .84, h * .72), fill=120)  # grey matter
    d.ellipse((w * .24, h * .22, w * .76, h * .62), fill=170)  # white matter
    r = random.Random(seed)
    for k in range(70):  # sulci
        ang = r.uniform(math.pi * 1.0, math.pi * 2.05); rr = r.uniform(.27, .35)
        x = w / 2 + math.cos(ang) * w * rr; y = h * .43 + math.sin(ang) * h * rr * .95
        x2 = w / 2 + math.cos(ang) * w * (rr - .09); y2 = h * .43 + math.sin(ang) * h * (rr - .09) * .95
        d.line((x, y, x2, y2), fill=70, width=5)
    d.arc((w * .32, h * .3, w * .7, h * .55), 190, 350, fill=225, width=18)  # corpus callosum
    d.ellipse((w * .55, h * .58, w * .82, h * .8), fill=125)               # cerebellum
    for k in range(6): d.arc((w * .57, h * (.6 + k * .03), w * .8, h * (.66 + k * .03)), 0, 180, fill=80, width=3)
    d.polygon([(w * .48, h * .52), (w * .56, h * .52), (w * .56, h * .95), (w * .48, h * .95)], fill=140)  # brainstem/cord
    return _finish(im, seed, 2.2, 0.05, 0.04)

XR = chest_xray(); CT = ct_slice(); MR = mri_brain()

def framed(fr, im, cx, cy, sc=1.0, a=1.0, title=None, col=SOFT):
    s = im.resize((int(im.width * sc), int(im.height * sc)), Image.BILINEAR)
    lay = Image.new("RGBA", (s.width + 12, s.height + 12), (255, 255, 255, 50)); lay.alpha_composite(s, (6, 6))
    put(fr, lay, cx, cy, 1.0, a)
    if title and a > 0.5:
        l, d = overlay(fr); d.text((cx, cy + lay.height / 2 + 34), title, font=font("Bold", 36), fill=col, anchor="mm"); fr.alpha_composite(l)

def dots(fr, n): fr.alpha_composite(chapter(n, NCH), (0, 110))

def gantry(fr, cx, cy, t, D, rot=True):
    """CT ring with rotating tube/detector and a sweeping slice line."""
    lay, d = overlay(fr); R = 300
    d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=(225, 230, 238, 255)); d.ellipse((cx - R + 14, cy - R + 14, cx + R - 14, cy + R - 14), outline=(190, 198, 210, 255), width=6)
    d.ellipse((cx - 170, cy - 170, cx + 170, cy + 170), fill=(20, 32, 55, 255))
    a = t * 2.4 if rot else 0
    for off, col in ((0, AMBER), (math.pi, CYAN)):
        x = cx + math.cos(a + off) * 235; y = cy + math.sin(a + off) * 235
        d.ellipse((x - 26, y - 26, x + 26, y + 26), fill=(*col, 255))
    x1, y1 = cx + math.cos(a) * 200, cy + math.sin(a) * 200; x2, y2 = cx - math.cos(a) * 200, cy - math.sin(a) * 200
    d.line((x1, y1, x2, y2), fill=(*AMBER, 140), width=8)
    d.ellipse((cx - 110, cy - 70, cx + 110, cy + 70), fill=(150, 160, 175, 255))  # patient cross-section
    d.rounded_rectangle((cx - 200, cy + 75, cx + 200, cy + 100), 10, fill=(200, 205, 215, 255))  # table
    fr.alpha_composite(lay)

def magnet(fr, cx, cy, t):
    lay, d = overlay(fr)
    d.rounded_rectangle((cx - 380, cy - 260, cx + 380, cy + 260), 120, fill=(228, 232, 240, 255))
    d.ellipse((cx - 190, cy - 190, cx + 190, cy + 190), fill=(18, 30, 52, 255))
    for k in range(3):  # radio-wave rings
        r = 60 + ((t * 80 + k * 50) % 150); a = int(200 * (1 - (r - 60) / 150))
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(*CYAN, a), width=4)
    d.rounded_rectangle((cx - 330, cy + 120, cx + 330, cy + 150), 12, fill=(200, 205, 215, 255))
    fr.alpha_composite(lay)

def dose_bars(fr, x, y, t, tin):
    panel(fr, x, y, TW, 470, "Radiation vs natural background (typical adult)")
    lay, d = overlay(fr); e = ease((t - tin) / 1.2)
    rows = [("Chest X-ray", "0.1 mSv", "~10 days", 10, TEALG), ("CT head", "1.6 mSv", "~7 months", 210, AMBER),
            ("CT abdomen", "7.7 mSv", "~2.6 years", 950, CORAL), ("MRI", "0", "no X-ray radiation", 0, CYAN)]
    for i, (lab, ms, eq, days, c) in enumerate(rows):
        yy = y + 90 + i * 92
        d.text((x + 24, yy), lab, font=font("Medium", 30), fill=SOFT)
        d.text((x + 24, yy + 38), ms, font=font("Regular", 24), fill=MUTED)
        L = (TW - 330) * math.sqrt(days / 950) * e
        if days: d.rounded_rectangle((x + 250, yy + 6, x + 250 + max(L, 14), yy + 50), 22, fill=c)
        d.text((x + 266 + max(L, 14) if days else x + 250, yy + 28), eq, font=font("Bold", 28), fill=WHITE if days else CYAN, anchor="lm")
    fr.alpha_composite(lay)

def cards(fr, t, D, items, y0=340, size=36, gap=150, t0=0.1, step=0.12):
    for i, (txt, c) in enumerate(items):
        fire("pop", D * (t0 + step * i)); show(fr, gcard(txt, c, i + 1, size), y0 + i * gap, t, D * (t0 + step * i))

# ---------------- scenes ----------------
def s_hook(fr, t, D):
    show(fr, kicker("Scan tests explained", CYAN), 250, t, 0.1)
    type_on(fr, "X-ray vs CT vs MRI", 310, t, 0.3, 74)
    if t > D * 0.25: type_on(fr, "What's the difference? When is each used?", 420, t, D * 0.25, 42, AMBER)
    for i, (im, lab, c) in enumerate(((XR, "X-ray", TEALG), (CT, "CT", AMBER), (MR, "MRI", CYAN))):
        framed(fr, im, 200 + i * 340, 820, 0.42, ease((t - D * (0.35 + 0.12 * i)) / 0.5), lab, c)
        fire("pop", D * (0.35 + 0.12 * i))
    show(fr, callout("Watch till the end", CORAL, 38), 1450, t, D * 0.8)

def s_xr(fr, t, D):
    dots(fr, 1); show(fr, kicker("X-ray", TEALG), 260, t, 0.1)
    show(fr, headline("A quick 2D picture", 60), 320, t, 0.3)
    framed(fr, XR, 540, 760, 0.62, ease((t - 0.5) / 0.7), "Chest X-ray (illustration)")
    cards(fr, t, D, [("Low-dose X-rays pass through the body; bone looks white", TEALG), ("Takes a few seconds", CYAN)], 1110, 34, 150, 0.35, 0.15)
    show(fr, callout("Chest X-ray ≈ 10 days of natural background radiation", AMBER, 32), 1440, t, D * 0.7)

def s_xr_when(fr, t, D):
    dots(fr, 2); show(fr, kicker("When X-ray?", TEALG), 260, t, 0.1)
    cards(fr, t, D, [("Suspected fracture", TEALG), ("Chest infection, pneumonia, suspected TB", CYAN), ("Dental check", LAV), ("Joint arthritis", AMBER)], 330, 36)
    framed(fr, XR, 540, 1180, 0.4, ease((t - D * 0.55) / 0.6))
    show(fr, callout("Often the first test: quick and low cost", TEALG, 36), 1560, t, D * 0.7)

def s_ct(fr, t, D):
    dots(fr, 3); show(fr, kicker("CT scan", AMBER), 260, t, 0.1)
    show(fr, headline("X-rays from all around: slices like bread", 54), 320, t, 0.3)
    if t < D * 0.4: gantry(fr, 540, 820, t, D)
    else: framed(fr, CT, 540, 800, 0.62, ease((t - D * 0.4) / 0.6), "CT slice of the abdomen (illustration)")
    show(fr, gcard("Cross-section slices of the body, in a few minutes", AMBER, None, 34), 1150, t, D * 0.25)
    if t > D * 0.6: dose_bars(fr, X0, 1290, t, D * 0.6)

def s_ct_when(fr, t, D):
    dots(fr, 4); show(fr, kicker("When CT?", AMBER), 260, t, 0.1)
    cards(fr, t, D, [("Head injury", CORAL), ("Stroke: to check for bleeding in the brain", CORAL), ("Accident: internal injury", AMBER),
                     ("Sudden severe belly pain, kidney stone", AMBER)], 330, 35, 140, 0.08, 0.12)
    show(fr, callout("Contrast injection sometimes: tell about allergy or kidney disease", CORAL, 32), 1080, t, D * 0.7)
    framed(fr, CT, 540, 1400, 0.38, ease((t - D * 0.6) / 0.6))

def s_mri(fr, t, D):
    dots(fr, 5); show(fr, kicker("MRI", CYAN), 260, t, 0.1)
    show(fr, headline("Strong magnet + radio waves", 60), 320, t, 0.3)
    if t < D * 0.35: magnet(fr, 540, 780, t)
    else: framed(fr, MR, 540, 760, 0.6, ease((t - D * 0.35) / 0.6), "MRI of the brain (illustration)")
    cards(fr, t, D, [("No X-ray radiation", TEALG), ("Very fine detail of soft tissue", CYAN), ("Usually 20-40 minutes; loud noise", AMBER)], 1130, 34, 140, 0.4, 0.13)

def s_mri_when(fr, t, D):
    dots(fr, 6); show(fr, kicker("When MRI?", CYAN), 260, t, 0.1)
    cards(fr, t, D, [("Brain and spinal cord problems", CYAN), ("Slip disc", LAV), ("Knee / shoulder ligament injury", AMBER), ("Nerve problems", TEALG)], 330, 35, 140, 0.08, 0.1)
    show(fr, callout("Before MRI tell: pacemaker, implant, any metal in body, fear of closed spaces", CORAL, 32), 940, t, D * 0.55); fire("ding", D * 0.55)
    framed(fr, MR, 540, 1360, 0.42, ease((t - D * 0.6) / 0.6))

def s_compare(fr, t, D):
    dots(fr, 7); show(fr, kicker("Side by side"), 260, t, 0.1)
    lay, d = overlay(fr); e = ease((t - 0.3) / 0.8)
    cols = [("", None), ("X-ray", TEALG), ("CT", AMBER), ("MRI", CYAN)]
    rows = [("Uses", ["X-rays", "X-rays", "Magnet"]), ("Time", ["Seconds", "Minutes", "20-40 min"]),
            ("Radiation", ["Low", "Higher", "None"]), ("Best for", ["Bone, chest", "Emergency", "Soft tissue"])]
    cw = [230, 250, 250, 250]; xs = [X0]
    for w_ in cw[:-1]: xs.append(xs[-1] + w_)
    y = 340
    for j, (lab, c) in enumerate(cols):
        if c: d.rounded_rectangle((xs[j] + 6, y, xs[j] + cw[j] - 6, y + 70), 18, fill=(*c, int(230 * e))); d.text((xs[j] + cw[j] / 2, y + 35), lab, font=font("Bold", 34), fill=(*INK, int(255 * e)), anchor="mm")
    for i, (lab, vals) in enumerate(rows):
        yy = y + 100 + i * 110; ei = ease((t - 0.5 - i * D * 0.08) / 0.5)
        d.rounded_rectangle((X0, yy, X0 + sum(cw), yy + 92), 16, fill=(255, 255, 255, int(18 * ei)))
        d.text((xs[0] + 16, yy + 46), lab, font=font("Bold", 30), fill=(*SOFT, int(255 * ei)), anchor="lm")
        for j, v in enumerate(vals): d.text((xs[j + 1] + cw[j + 1] / 2, yy + 46), v, font=font("Medium", 30), fill=(*WHITE, int(255 * ei)), anchor="mm")
    fr.alpha_composite(lay)
    show(fr, callout("Pregnant or might be? Tell before any scan. If imaging is needed, doctors often prefer MRI", AMBER, 32), 900, t, D * 0.45)
    show(fr, gcard("Which scan: your doctor decides by symptoms, urgency and safety", TEALG, None, 34), 1130, t, D * 0.6)
    show(fr, gcard("Avoid unnecessary repeat scans", CORAL, None, 34), 1280, t, D * 0.72)
    show(fr, source_tag("RadiologyInfo.org (ACR/RSNA) dose table; Healthline: CT vs MRI"), 1430, t, D * 0.75)

SC = [(film(s_hook), "doc"), (film(s_xr), "doc"), (film(s_xr_when), "doc"), (film(s_ct), "doc"), (film(s_ct_when), "doc"),
      (film(s_mri), "doc"), (film(s_mri_when), "doc"), (film(s_compare), "doc"), (close_scene("Which scan have you had?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si, (fn, bg) in enumerate(SC):
            d = 16 if si < len(SC) - 1 else 33; NOW.update(t=d * .95, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * .95, d); ims.append(fr.convert("RGB").resize((360, 640)))
            if si in (3, 5):
                NOW.update(t=d * .2); fr = BASES[bg].copy(); fn(fr, d * .2, d); ims.append(fr.convert("RGB").resize((360, 640)))
        s = Image.new("RGB", (360 * 6, 640 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 6) * 360, (i // 6) * 640))
        s.save("sheet_imaging.png")
    else: run(SC, "/tmp/img_", "Xray_CT_MRI_Difference_Hindi.mp4")
