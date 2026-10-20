"""Genetics Clinical Series, Episode 7: When karyotype still matters."""
import sys, random
from cbc_cartoon import run
from gen_series import *
from hts_close import close_scene

TOT[0] = 14
TOPIC = "GENETICS SERIES  •  EPISODE 7"
PAPER = paper_sprite(["Double segment imbalance", "due to inherited", "translocation: CMA"], "Indian Pediatrics, 2017 (Lucknow)")
KARYO = karyogram()
KARYO21 = karyogram(extra21=True)
GREY = (205, 205, 200)

def chrom(d, x, top, L, segs=(), w=36, a=255, cen=0.35, lab=None):
    """Vertical banded chromosome. segs: (from, to, colour) as fractions of length from the top."""
    d.rounded_rectangle((x - w / 2, top, x + w / 2, top + L), int(w / 2), fill=(*GREY, a))
    rr = random.Random(int(L) + int(x)); y = top + 8
    while y < top + L - 10:
        bh = rr.uniform(4, 11)
        if rr.random() < 0.5: d.rectangle((x - w / 2 + 3, y, x + w / 2 - 3, y + bh), fill=(70, 70, 75, a))
        y += bh + rr.uniform(4, 12)
    for f0, f1, c in segs:
        d.rounded_rectangle((x - w / 2, top + f0 * L, x + w / 2, top + f1 * L), 10, fill=(*c, a))
    cy = top + cen * L; d.ellipse((x - w / 2 - 2, cy - 6, x + w / 2 + 2, cy + 6), fill=(11, 27, 51, a))
    if lab: d.text((x, top + L + 34), lab, font=font("Bold", 30), fill=(*SOFT, a), anchor="mm")

def robertsonian(fr, y, t, tin):
    """Chromosomes 14 and 21 fuse at the centromere (Robertsonian translocation)."""
    lay, d = overlay(fr); e = ease((t - tin) / 0.6); a = int(255 * e); m = ease((t - tin - 1.2) / 1.2)
    cx = 540; gap = 200 * (1 - m)
    if m < 0.98:
        chrom(d, cx - 60 - gap, y, 300, [(0, 0.08, CYAN)], a=a, cen=0.06, lab="14")
        chrom(d, cx + 60 + gap, y + 140, 160, [(0, 0.15, AMBER)], a=a, cen=0.1, lab="21")
    if m > 0.02:
        b = int(255 * m)
        chrom(d, cx, y - 20, 300, [(0.6, 1.0, AMBER)], a=b, cen=0.6, lab=None)
        d.text((cx, y + 330), "rob(14;21)", font=font("Bold", 36), fill=(*AMBER, b), anchor="mm")
    fr.alpha_composite(lay)

def reciprocal(fr, y, t, tin, la="7", lb="11", fish=False):
    """Balanced reciprocal translocation: the tips of two chromosomes swap places."""
    lay, d = overlay(fr); e = ease((t - tin) / 0.6); a = int(255 * e); m = ease((t - tin - 1.0) / 1.0)
    xs = (210, 400, 680, 870)
    chrom(d, xs[0], y, 330, [(0.82, 1, CYAN)], a=a, cen=0.4, lab=la)
    chrom(d, xs[1], y + 20, 300, [(0.8, 1, CORAL)], a=a, cen=0.35, lab=lb)
    tips = ((CORAL, 0.82), (CYAN, 0.8))
    chrom(d, xs[2], y, 330, [(0.82, 1, CYAN if m < 0.5 else CORAL)], a=a, cen=0.4, lab="der(" + la + ")")
    chrom(d, xs[3], y + 20, 300, [(0.8, 1, CORAL if m < 0.5 else CYAN)], a=a, cen=0.35, lab="der(" + lb + ")")
    d.text((305, y - 40), "Normal", font=font("Medium", 30), fill=(*SOFT, a), anchor="mm")
    d.text((775, y - 40), "Balanced carrier", font=font("Medium", 30), fill=(*AMBER, a), anchor="mm")
    if fish and m > 0.9:
        for xx, yy, c in ((xs[2], y + 318, (255, 90, 90)), (xs[3], y + 308, (90, 255, 120))):
            d.ellipse((xx - 11, yy - 11, xx + 11, yy + 11), fill=c)
        d.text((775, y + 420), "FISH: tip probes swapped", font=font("Bold", 30), fill=(*TEALG, a), anchor="mm")
    fr.alpha_composite(lay)

def bars(fr, y, rows, t, tin, vmax):
    lay, d = overlay(fr); e = ease((t - tin) / 1.2)
    for i, (lab, v, txt, c) in enumerate(rows):
        yy = y + i * 120
        d.text((X0, yy + 30), lab, font=font("Medium", 34), fill=SOFT, anchor="lm")
        L = max(16, (TW - 470) * v / vmax * e)
        d.rounded_rectangle((X0 + 300, yy, X0 + 300 + L, yy + 60), 30, fill=c)
        d.text((X0 + 320 + L, yy + 30), txt, font=font("Bold", 34), fill=WHITE, anchor="lm")
    fr.alpha_composite(lay)

def cells(fr, y, t, tin, n=30, odd=(4, 11, 19, 26)):
    """30 metaphase cells counted; a few carry a different chromosome count (mosaicism)."""
    lay, d = overlay(fr); p = ease((t - tin) / 2.0)
    for i in range(n):
        if i / n > p: break
        cx = X0 + 60 + (i % 10) * ((TW - 120) / 9); cy = y + (i // 10) * 120
        c = AMBER if i in odd else (120, 200, 230)
        d.ellipse((cx - 42, cy - 42, cx + 42, cy + 42), outline=(*c, 230), width=4, fill=(*c, 40))
        d.text((cx, cy), "45,X" if i in odd else "46,XX", font=font("Bold", 20), fill=c, anchor="mm")
    fr.alpha_composite(lay)

def ends_plot(fr, y, t, tin, gain7=True):
    """Two chromosome-end changes in opposite directions (illustration)."""
    lay, d = overlay(fr); e = ease((t - tin) / 0.6); a = int(255 * e)
    for j, (lab, up) in enumerate((("Chr 7 end (7q36)", gain7), ("Chr 11 end (11q24-q25)", not gain7))):
        x0 = X0 + j * (TW / 2 + 10); w = TW / 2 - 10; yy = y
        d.rounded_rectangle((x0, yy, x0 + w, yy + 260), 22, fill=(255, 255, 255, int(20 * e)), outline=(255, 255, 255, int(60 * e)), width=2)
        d.text((x0 + w / 2, yy + 34), lab, font=font("Medium", 26), fill=(*SOFT, a), anchor="mm")
        mid = yy + 125; d.line((x0 + 20, mid, x0 + w - 20, mid), fill=(255, 255, 255, int(70 * e)), width=2)
        r = random.Random(j + (0 if gain7 else 9))
        for i in range(70):
            u = i / 70; xx = x0 + 24 + u * (w - 48)
            off = (-42 if up else 42) if u > 0.6 else 0
            yv = mid + off + r.gauss(0, 7)
            col = (TEALG if up else CORAL) if u > 0.6 else (150, 170, 200)
            d.ellipse((xx - 4, yv - 4, xx + 4, yv + 4), fill=(*col, a))
        d.text((x0 + w / 2, yy + 236), "GAIN (x3)" if up else "LOSS (x1)", font=font("Bold", 28), fill=(*(TEALG if up else CORAL), a), anchor="mm")
    fr.alpha_composite(lay)

# ---------------- scenes ----------------
def sc0(fr, t, D):
    show(fr, kicker("Genetics Clinical Series  •  Episode 7", CYAN), 330, t, 0.1)
    type_on(fr, "When karyotype", 410, t, 0.3, 70)
    type_on(fr, "still matters", 500, t, 0.9, 70)
    if t > D * 0.3: type_on(fr, "Microarray tells how much. Karyotype tells how.", 610, t, D * 0.3, 38, AMBER)
    put(fr, KARYO, 540, 1080, 0.86, ease((t - 0.6) / 0.6))
    show(fr, callout("For doctors and healthcare teams  •  with a published Indian case", CYAN, 34), 1520, t, D * 0.6); fire("whoosh", D * 0.6)

def sc_how(fr, t, D):
    dots(fr, 1); show(fr, kicker("How much vs how"), 260, t, 0.1)
    show(fr, gcard("CMA: how much DNA (losses and gains)", CYAN, 1, 34), 330, t, 0.3)
    show(fr, gcard("Karyotype: how chromosomes are arranged, cell by cell", AMBER, 2, 33), 480, t, D * 0.25)
    reciprocal(fr, 720, t, D * 0.4, la="A", lb="B")
    show(fr, callout("Balanced change: nothing lost or gained, so CMA looks normal", CORAL, 32), 1290, t, D * 0.7); fire("pop", D * 0.7)

def sc_down(fr, t, D):
    dots(fr, 2); show(fr, kicker("1. Down syndrome: free or translocation?"), 260, t, 0.1)
    show(fr, gcard("CMA / QF-PCR: extra chromosome 21 material", CYAN, 1, 33), 330, t, 0.3)
    show(fr, gcard("Only karyotype shows if it is attached to another chromosome", AMBER, 2, 32), 480, t, D * 0.2)
    robertsonian(fr, 720, t, D * 0.35)
    show(fr, callout("This changes the risk in the next pregnancy", CORAL, 36), 1200, t, D * 0.75); fire("ding", D * 0.75)
    put(fr, KARYO21, 540, 1600, 0.5, ease((t - D * 0.82) / 0.6))

sc_risk = s_cards(3, "If a translocation is found", "Karyotype both parents",
    [("Mother a balanced carrier: risk about 10-15%", AMBER), ("Father a balanced carrier: about 1-3%", CYAN),
     ("Parent with rob(21;21): almost 100%", CORAL)],
    lambda fr, t, D, y: show(fr, source_tag("Recurrence risks as cited by Kunda et al., Cureus 2026"), y + 10, t, D * 0.6), size=34)

def sc_india(fr, t, D):
    dots(fr, 4); show(fr, kicker("Indian data"), 260, t, 0.1)
    show(fr, headline("1,597 Down syndrome cases on karyotype", 50), 320, t, 0.3)
    show(fr, body("from 9,313 samples, Hyderabad", 36, SOFT), 470, t, 0.5)
    bars(fr, 560, [("Free trisomy 21", 91.7, "91.7%", (120, 140, 170)), ("Robertsonian", 5.6, "90 cases (5.6%)", AMBER)], t, 0.7, 100)
    show(fr, gcard("rob(14;21): 42 cases", CYAN, 1, 34), 840, t, D * 0.45)
    show(fr, gcard("rob(21;21): 36 cases", CORAL, 2, 34), 990, t, D * 0.55)
    show(fr, source_tag("Kunda et al., Cureus 2026;18(3):e104606 (AMPATH, Hyderabad), CC BY"), 1150, t, D * 0.6)
    fire("pop", D * 0.45); fire("pop", D * 0.55)

def sc_rpl(fr, t, D):
    dots(fr, 5); show(fr, kicker("2. Recurrent miscarriage"), 260, t, 0.1)
    show(fr, headline("2-5% of couples: one partner is a balanced carrier", 50), 320, t, 0.3)
    reciprocal(fr, 560, t, 0.8, la="A", lb="B")
    show(fr, gcard("Carriers are healthy; CMA is normal", CYAN, 1, 33), 1080, t, D * 0.4)
    show(fr, gcard("ASRM: karyotype both parents", AMBER, 2, 33), 1230, t, D * 0.5)
    show(fr, gcard("ESHRE: not routine; decide case by case", LAV, 3, 33), 1380, t, D * 0.6)
    show(fr, source_tag("Li & Marren, Aust J Gen Pract 2018 (summary of ASRM, RCOG, ESHRE)"), 1530, t, D * 0.65)
    fire("pop", D * 0.4); fire("pop", D * 0.5); fire("pop", D * 0.6)

sc_sex = s_cards(6, "3. Sex chromosomes and infertility", None,
    [("Girl with short stature or no periods: karyotype for Turner", LAV), ("Count at least 30 cells so mosaicism is not missed", AMBER),
     ("Man with azoospermia, or count <5 million/mL with high FSH", CYAN), ("Karyotype for Klinefelter (47,XXY)", TEALG)],
    lambda fr, t, D, y: show(fr, source_tag("ACMG Turner lab guideline 2010; AUA/ASRM male infertility guideline 2024"), y + 10, t, D * 0.6), size=32)

def sc_mosaic(fr, t, D):
    dots(fr, 7); show(fr, kicker("4. Mosaicism and marker chromosomes"), 260, t, 0.1)
    show(fr, headline("Karyotype looks at each cell", 54), 320, t, 0.3)
    cells(fr, 480, t, 0.6)
    show(fr, gcard("Low-level mosaicism can be missed by CMA", AMBER, 1, 33), 850, t, D * 0.45)
    show(fr, gcard("Small extra marker chromosome: identify with FISH or CMA", LAV, 2, 32), 1000, t, D * 0.6)
    fire("pop", D * 0.45); fire("pop", D * 0.6)

sc_limit = s_cards(8, "Karyotype has limits too", "Right question, right test",
    [("Misses changes smaller than about 5-10 Mb", CORAL), ("CMA for small deletions and duplications", CYAN),
     ("FISH for a targeted region or a carrier check", TEALG), ("Often the tests work together", AMBER)], size=33)

def sc_sample(fr, t, D):
    dots(fr, 9); show(fr, kicker("Sample"), 260, t, 0.1)
    put(fr, tube_sprite((60, 160, 90), "Na HEP"), 300, 640, 1.0, ease((t - 0.3) / 0.5))
    lay, d = overlay(fr); e = ease((t - 0.5) / 0.5)
    d.text((300, 950), "Sodium heparin (green top)", font=font("Bold", 34), fill=(*SOFT, int(255 * e)), anchor="mm"); fr.alpha_composite(lay)
    show(fr, gcard("Live cells are cultured: do not freeze", AMBER, 1, 33), 1010, t, D * 0.3)
    show(fr, gcard("Prenatal: amniotic fluid or CVS", LAV, 2, 33), 1160, t, D * 0.45)
    show(fr, callout("Prenatal: disease testing only; sex never disclosed (PCPNDT)", CORAL, 32), 1320, t, D * 0.6)
    fire("pop", D * 0.3); fire("pop", D * 0.45)

def sc_case1(fr, t, D):
    dots(fr, 10); show(fr, kicker("Case study from India", CORAL), 260, t, 0.1)
    put(fr, PAPER, 540, 690, 0.72, ease((t - 0.4) / 0.6))
    show(fr, gcard("Girl: heart defect (ASD, PDA), facial features", CYAN, None, 33), 1020, t, D * 0.3)
    show(fr, gcard("Developmental delay", AMBER, None, 34), 1170, t, D * 0.42)
    show(fr, gcard("Karyotype at 550 bands: normal", LAV, None, 34), 1320, t, D * 0.6)
    show(fr, source_tag("Tuteja, Agarwal & Phadke, Indian Pediatr 2017;54:879-81 (SGPGIMS, Lucknow)"), 1480, t, D * 0.65)

def sc_case2(fr, t, D):
    dots(fr, 11); show(fr, kicker("Case: what CMA found"), 260, t, 0.1)
    ends_plot(fr, 330, t, 0.3, gain7=True)
    show(fr, gcard("Girl: about 9 Mb extra at 7q36, about 13 Mb missing at 11q24-q25", CORAL, 1, 31), 660, t, D * 0.25)
    show(fr, body("Her father's cousin's daughter:", 34, SOFT), 840, t, D * 0.45)
    ends_plot(fr, 900, t, D * 0.5, gain7=False)
    show(fr, gcard("The opposite pattern; her prenatal karyotype was also normal", AMBER, 2, 31), 1230, t, D * 0.65)

def sc_case3(fr, t, D):
    dots(fr, 12); show(fr, kicker("Case: finding the carrier"), 260, t, 0.1)
    show(fr, headline("Opposite changes at two chromosome ends = suspect a balanced parental translocation", 42), 320, t, 0.3)
    reciprocal(fr, 600, t, D * 0.25, fish=True)
    show(fr, gcard("Too small for karyotype; balanced, so CMA is normal", AMBER, 1, 31), 1130, t, D * 0.5)
    show(fr, gcard("FISH in the father confirmed t(7;11)", TEALG, 2, 33), 1280, t, D * 0.62)
    show(fr, gcard("Next family pregnancy: CVS at 11 weeks found it; counselling", LAV, 3, 31), 1430, t, D * 0.74)
    fire("ding", D * 0.62)

sc_take = s_cards(13, "Key messages", None,
    [("CMA tells how much; karyotype tells how", CYAN), ("Down syndrome: karyotype to tell free trisomy from translocation", AMBER),
     ("Recurrent miscarriage, Turner, Klinefelter: karyotype still useful", LAV), ("Opposite end changes: check parents by karyotype or FISH", TEALG),
     ("Take a family history and draw a pedigree", CORAL)], size=31)

SC = [(film(sc0), "doc"), (film(sc_how), "doc"), (film(sc_down), "doc"), (film(sc_risk), "doc"), (film(sc_india), "doc"),
      (film(sc_rpl), "doc"), (film(sc_sex), "doc"), (film(sc_mosaic), "doc"), (film(sc_limit), "doc"), (film(sc_sample), "doc"),
      (film(sc_case1), "doc"), (film(sc_case2), "doc"), (film(sc_case3), "doc"), (film(sc_take), "doc"),
      (close_scene("When do you still order a karyotype?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si, (fn, bg) in enumerate(SC):
            d = 16 if si < len(SC) - 1 else 33; p = .95 if si else 0.125; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((300, 533)))
        s = Image.new("RGB", (300 * 5, 533 * 3), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 300, (i // 5) * 533))
        s.save(sys.argv[2] if len(sys.argv) > 2 else "/tmp/sheet_g007.png")
    else: run(SC, "/tmp/g007_", "Genetics_Ep07_When_Karyotype_Still_Matters_Hindi.mp4", max_sec=480)
