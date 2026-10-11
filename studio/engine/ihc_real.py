"""IHC markers video, realistic documentary style."""
import math, sys
from cbc_cartoon import run
from real_style import *
from hts_close import close_scene

TOPIC = "IHC MARKERS  •  PATHOLOGY"
HE = he_tissue(1400, 3); HE2 = he_tissue(1200, 21, glands=6)
DAB = he_tissue(1400, 9, stain="dab")
HER = [her2_tex(i) for i in range(4)]
ER = nuclear_tex(0.65)
BLOCK = cassette_sprite(wax=True); SLIDE_HE = slide_sprite(HE); SLIDE_DAB = slide_sprite(DAB, "IHC")
REPORT = report_sprite()

def dots(fr, n): fr.alpha_composite(chapter(n, 9), (0, 110))
def ep(fr, tex, cx, cy, size, t, D, z0=1.0, z1=1.3, focus=0.0, pan=(0.3, 0.1), a=1.0):
    im = eyepiece(tex, size, t, z0, z1, D, pan, focus)
    put(fr, im, cx, cy, 1.0, a)
def label(fr, text, x, y, col=SOFT, size=32, anchor="mm"):
    lay, d = overlay(fr); d.text((x, y), text, font=font("Medium", size), fill=col, anchor=anchor); fr.alpha_composite(lay)

def i_hook(fr, t, D):
    fullbleed(fr, DAB, t, D, 1.0, 1.25)
    show(fr, kicker("IHC markers  •  Pathology", CYAN), 330, t, 0.1)
    type_on(fr, "Report says: IHC advised?", 410, t, 0.4, 72)
    if t > D * 0.35: type_on(fr, "Don't panic.", 600, t, D * 0.35, 72, AMBER)
    show(fr, callout("What IHC markers are, and why they matter", CYAN, 40), 1620, t, D * 0.6); fire("whoosh", D * 0.6)

def i_what(fr, t, D):
    dots(fr, 1)
    show(fr, kicker("What is IHC?"), 260, t, 0.1)
    show(fr, headline("ImmunoHistoChemistry", 64), 320, t, 0.3)
    ep(fr, HE, 290, 720, 420, t, D, 1.2, 1.3, a=ease((t - 0.4) / 0.6))
    ep(fr, HE, 790, 720, 420, t, D, 1.25, 1.35, pan=(-0.3, 0.2), a=ease((t - 0.7) / 0.6))
    if t > 1.0: label(fr, "Look alike?", 540, 980, AMBER, 44)
    if t > D * 0.5: ep(fr, DAB, 540, 1260, 380, t - D * 0.5, D, 1.0, 1.2, focus=max(0, 1 - (t - D * 0.5) / 1.0))
    show(fr, gcard("IHC shows which PROTEIN is in the cells, so the pathologist knows what type of cell it really is", CYAN, None, 34), 1500, t, D * 0.6)

def i_how(fr, t, D):
    dots(fr, 2)
    show(fr, kicker("How it works"), 260, t, 0.1)
    show(fr, headline("Antibody fits its protein like a key in a lock", 56), 320, t, 0.3)
    lay, d = overlay(fr)
    # cell membrane with receptor proteins
    y0 = 980; d.rounded_rectangle((60, y0, 1020, y0 + 260), 60, fill=(228, 222, 232, 235))
    d.text((540, y0 + 190), "Cell", font=font("Medium", 34), fill=(110, 110, 140), anchor="mm")
    pos = [160, 300, 440, 580, 720, 860]
    for i, x in enumerate(pos):
        target = i % 2 == 0
        c = (160, 90, 200) if target else (120, 160, 120)
        if target: d.polygon([(x - 26, y0), (x - 26, y0 - 40), (x - 8, y0 - 40), (x, y0 - 24), (x + 8, y0 - 40), (x + 26, y0 - 40), (x + 26, y0)], fill=c)
        else: d.ellipse((x - 26, y0 - 40, x + 26, y0 + 10), fill=c)
    bind = ease((t - D * 0.2) / (D * 0.35))
    for i, x in enumerate(pos):
        target = i % 2 == 0
        if target:
            yy = y0 - 60 - (1 - bind) * 380; ang = -math.pi / 2
        else:
            yy = y0 - 300 - 60 * math.sin(t * 1.5 + i); ang = -math.pi / 2 + 0.4 * math.sin(t + i)
        antibody(d, x, yy, 90, ang + math.pi, CYAN if target else (140, 170, 200), 255)
    brown = ease((t - D * 0.6) / (D * 0.2))
    if brown > 0:
        for i, x in enumerate(pos):
            if i % 2 == 0:
                for k in range(10):
                    xx = x + 40 * math.cos(k * 0.7 + i); yy = y0 - 140 + 30 * math.sin(k * 1.3)
                    d.ellipse((xx - 9, yy - 9, xx + 9, yy + 9), fill=(120, 65, 20, int(230 * brown)))
    fr.alpha_composite(lay)
    fire("ding", D * 0.55)
    show(fr, callout("Brown colour = protein present = POSITIVE", AMBER, 40), 1330, t, D * 0.65)
    if t > D * 0.2: label(fr, "Antibody", 240, 520, CYAN, 34)

def i_sample(fr, t, D):
    dots(fr, 3)
    show(fr, kicker("New sample needed?"), 260, t, 0.1)
    show(fr, headline("Usually not", 80, TEALG), 320, t, 0.3)
    put(fr, BLOCK, 300, 720, 1.0, ease((t - 0.4) / 0.5))
    if t > D * 0.25:
        lay, d = overlay(fr); e = ease((t - D * 0.25) / 0.6)
        d.line((520, 720, 520 + 120 * e, 720), fill=CYAN, width=8)
        if e > 0.9: d.polygon([(640, 700), (670, 720), (640, 740)], fill=CYAN)
        fr.alpha_composite(lay)
        put(fr, SLIDE_DAB, 860, 720, 0.5, e)
    show(fr, gcard("Done on the SAME biopsy wax block", CYAN, 1, 38), 980, t, D * 0.3)
    show(fr, gcard("Biopsy done elsewhere? The block or slides are requested from there", AMBER, 2, 36), 1130, t, D * 0.55)
    fire("pop", D * 0.3); fire("pop", D * 0.55)

def i_uses(fr, t, D):
    dots(fr, 4)
    show(fr, kicker("Use 1: the right diagnosis"), 260, t, 0.1)
    show(fr, headline("Which type of cell is it?", 60), 320, t, 0.3)
    ep(fr, DAB, 540, 640, 420, t, D, 1.0, 1.3)
    rows = [("TTF-1", "Lung cancer", CYAN), ("S100", "Melanoma", LAV), ("CD20", "B-cell lymphoma", AMBER), ("CD3", "T-cell lymphoma", TEALG)]
    lay, d = overlay(fr)
    for i, (m, w, c) in enumerate(rows):
        tin = D * (0.2 + 0.14 * i); fire("pop", tin)
        if t < tin: continue
        e = ease((t - tin) / 0.4); y = 920 + i * 125
        d.rounded_rectangle((X0, y, X0 + TW, y + 105), 24, fill=(255, 255, 255, int(20 * e)), outline=(255, 255, 255, int(46 * e)), width=2)
        d.rounded_rectangle((X0 + 24, y + 22, X0 + 230, y + 83), 30, fill=(*c, int(255 * e)))
        d.text((X0 + 127, y + 52), m, font=font("Bold", 36), fill=(*INK, int(255 * e)), anchor="mm")
        d.text((X0 + 270, y + 52), "→" if False else "helps identify", font=font("Regular", 30), fill=(*MUTED, int(255 * e)), anchor="lm")
        d.text((X0 + 500, y + 52), w, font=font("Bold", 36), fill=(255, 255, 255, int(255 * e)), anchor="lm")
    fr.alpha_composite(lay)
    show(fr, source_tag("examples only; the pathologist chooses the markers"), 1430, t, D * 0.8)

def i_er(fr, t, D):
    dots(fr, 5)
    show(fr, kicker("Use 2: guiding treatment"), 260, t, 0.1)
    show(fr, headline("Breast cancer: ER, PR, HER2", 60), 320, t, 0.3)
    ep(fr, ER, 540, 680, 480, t, D, 1.0, 1.25)
    label(fr, "ER / PR: brown nuclei = positive cells", 540, 960, SOFT, 32)
    rows = [("Less than 1%", "Negative", (150, 165, 190)), ("1% to 10%", "Low positive", AMBER), ("More than 10%", "Positive", TEALG)]
    lay, d = overlay(fr)
    for i, (a, b, c) in enumerate(rows):
        tin = D * (0.3 + 0.12 * i); fire("pop", tin)
        if t < tin: continue
        y = 1040 + i * 105; e = ease((t - tin) / 0.4)
        d.rounded_rectangle((X0, y, X0 + TW, y + 90), 22, fill=(255, 255, 255, int(18 * e)), outline=(*c, int(200 * e)), width=3)
        d.text((X0 + 40, y + 45), a, font=font("Bold", 36), fill=(255, 255, 255, int(255 * e)), anchor="lm")
        d.text((X0 + TW - 40, y + 45), b, font=font("Bold", 36), fill=(*c, int(255 * e)), anchor="rm")
    fr.alpha_composite(lay)
    show(fr, gcard("Above 1%: hormone therapy may be an option", TEALG, None, 36), 1380, t, D * 0.7)
    show(fr, source_tag("American Cancer Society"), 1520, t, D * 0.75)

def i_her2(fr, t, D):
    dots(fr, 6)
    show(fr, kicker("HER2 score"), 260, t, 0.1)
    show(fr, headline("0 to 3+: brown cell borders", 60), 320, t, 0.3)
    labs = [("0", (150, 165, 190)), ("1+", AMBER), ("2+", (255, 150, 60)), ("3+", CORAL)]
    for i in range(4):
        tin = 0.4 + i * D * 0.12; fire("pop", tin)
        if t < tin: continue
        cx = 280 + (i % 2) * 520; cy = 640 + (i // 2) * 470
        ep(fr, HER[i], cx, cy, 380, t - tin, D, 1.15, 1.3, pan=(0, 0), a=ease((t - tin) / 0.4))
        label(fr, labs[i][0], cx, cy + 225, labs[i][1], 46)
    show(fr, gcard("3+ = HER2 positive", CORAL, 1, 38), 1380, t, D * 0.5)
    show(fr, gcard("2+ = may need FISH gene test", AMBER, 2, 38), 1510, t, D * 0.62)
    show(fr, gcard("1+, or 2+ with FISH negative = 'HER2-low'", LAV, 3, 36), 1640, t, D * 0.75)
    fire("pop", D * 0.5); fire("pop", D * 0.62); fire("pop", D * 0.75)

def i_report(fr, t, D):
    dots(fr, 7)
    show(fr, kicker("The report"), 260, t, 0.1)
    show(fr, headline("Each marker: positive or negative", 58), 320, t, 0.3)
    p = ease((t - 0.4) / 0.6)
    if p > 0:
        im = REPORT.copy(); d = ImageDraw.Draw(im)
        d.rectangle((24, 96, 520, 400), fill=(250, 250, 248))
        d.text((30, 110), "IHC (example format)", font=font("Bold", 24), fill=(20, 50, 100))
        rows = [("Marker A", "Positive, diffuse, strong"), ("Marker B", "Negative"), ("Marker C", "Positive in 80% of cells"), ("Marker D", "Score 1+")]
        for i, (m, r) in enumerate(rows):
            y = 160 + i * 56; d.text((30, y), m, font=font("Medium", 22), fill=(40, 40, 60)); d.text((200, y), r, font=font("Regular", 22), fill=(40, 40, 60))
            d.line((30, y + 40, 510, y + 40), fill=(220, 225, 232), width=1)
        put(fr, im, 540, 850, 0.8, p)
    show(fr, gcard("IHC can take a few extra days", AMBER, 1, 38), 1220, t, D * 0.35)
    show(fr, gcard("Pathologist writes the report; your doctor decides treatment", CYAN, 2, 36), 1370, t, D * 0.55)
    fire("pop", D * 0.35); fire("pop", D * 0.55)

def i_remember(fr, t, D):
    fullbleed(fr, HE2, t, D, 1.15, 1.3); dots(fr, 8)
    show(fr, kicker("Remember", TEALG), 300, t, 0.1)
    show(fr, headline("No single marker decides the diagnosis", 64), 370, t, 0.3)
    chips = [("Microscope picture", CYAN), ("Marker 1", AMBER), ("Marker 2", LAV), ("Marker 3", TEALG)]
    lay, d = overlay(fr)
    for i, (lab, c) in enumerate(chips):
        tin = D * (0.2 + 0.1 * i); fire("pop", tin)
        if t < tin: continue
        e = ease((t - tin) / 0.5); ang = -math.pi / 2 + i * math.pi / 2
        x = 540 + 300 * math.cos(ang) * (1.6 - 0.6 * e); y = 900 + 210 * math.sin(ang) * (1.6 - 0.6 * e)
        f = font("Bold", 32); tw = f.getlength(lab)
        d.line((x, y, 540, 900), fill=(*c, 90), width=3)
        d.rounded_rectangle((x - tw / 2 - 26, y - 32, x + tw / 2 + 26, y + 32), 32, fill=(*INK, 255), outline=c, width=3)
        d.text((x, y), lab, font=f, fill=c, anchor="mm")
    if t > D * 0.6:
        e = ease((t - D * 0.6) / 0.5)
        d.ellipse((540 - 90 * e, 900 - 90 * e, 540 + 90 * e, 900 + 90 * e), fill=(*TEALG, 230))
        d.text((540, 900), "Result", font=font("Bold", 34), fill=INK, anchor="mm")
    fr.alpha_composite(lay)
    show(fr, callout("Don't google a single marker and worry", CORAL, 40), 1450, t, D * 0.75); fire("ding", D * 0.75)

SC = [(film(i_hook), "doc"), (film(i_what), "doc"), (film(i_how), "doc"), (film(i_sample), "doc"), (film(i_uses), "doc"),
      (film(i_er), "doc"), (film(i_her2), "doc"), (film(i_report), "doc"), (film(i_remember), "doc"),
      (close_scene("Have you ever seen an IHC report?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        D = [14, 16, 18, 16, 20, 18, 18, 18, 17, 33]
        ims = []
        for si in range(10):
            fn, bg = SC[si]; d = D[si]; p = 0.95; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((360, 640)))
        s = Image.new("RGB", (360 * 5, 640 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 360, (i // 5) * 640))
        s.save("sheet.png")
    else: run(SC, "/tmp/ihc_", "IHC_Markers_Hindi.mp4")
