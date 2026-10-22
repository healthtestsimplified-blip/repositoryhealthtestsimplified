"""Genetics Clinical Series, Episode 8: Gene panel or exome?"""
import sys, random
from cbc_cartoon import run
from gen_series import *
from hts_close import close_scene

TOT[0] = 14
TOPIC = "GENETICS SERIES  •  EPISODE 8"
PAPER = paper_sprite(["Infantile systemic", "hyalinosis: a familiar", "symptom, unusual disease"], "Cureus, 2026 (AIIMS Bhopal)")
PANEL = set(random.Random(8).sample(range(600), 24))
VIRT = set(random.Random(9).sample(range(600), 40))

def coverage(fr, x, y, w, h, t, tin):
    """Average read depth: panel deeper than exome (illustration)."""
    panel(fr, x, y, w, h, "Read depth (illustration)")
    lay, d = overlay(fr); e = ease((t - tin) / 1.2)
    for i, (lab, v, c) in enumerate((("Panel", 0.95, TEALG), ("Exome", 0.55, CYAN))):
        bx = x + 150 + i * 330; top = y + h - 70 - (h - 170) * v * e
        d.rounded_rectangle((bx, top, bx + 160, y + h - 70), 18, fill=(*c, 230))
        d.text((bx + 80, y + h - 36), lab, font=font("Bold", 32), fill=SOFT, anchor="mm")
    d.text((x + w - 30, y + 110), "Deeper = fewer gaps", font=font("Medium", 28), fill=AMBER, anchor="rm")
    fr.alpha_composite(lay)

def venn(fr, y, t, tin):
    """More genes analysed -> more VUS (illustration of counts)."""
    lay, d = overlay(fr); e = ease((t - tin) / 0.8); a = int(255 * e)
    cx, cy = 540, y + 230
    d.ellipse((cx - 210, cy - 210, cx + 210, cy + 210), outline=(*CYAN, a), width=5, fill=(*CYAN, int(30 * e)))
    d.ellipse((cx - 90, cy + 10, cx + 90, cy + 190), outline=(*TEALG, a), width=5, fill=(*TEALG, int(40 * e)))
    d.text((540, y + 272), "Panel", font=font("Bold", 30), fill=(*TEALG, a), anchor="mm")
    d.text((540, y + 60), "Exome", font=font("Bold", 30), fill=(*CYAN, a), anchor="mm")
    r = random.Random(4)
    for k in range(18):
        ang = r.uniform(0, 6.28); rad = r.uniform(120, 195); xx = 540 + rad * math.cos(ang); yy = y + 230 + rad * math.sin(ang)
        if ease((t - tin - 0.6 - k * 0.05) / 0.3) > 0.5: d.ellipse((xx - 9, yy - 9, xx + 9, yy + 9), fill=AMBER)
    for k in range(3):
        xx = 520 + k * 22; yy = y + 320
        if e > 0.9: d.ellipse((xx - 9, yy - 9, xx + 9, yy + 9), fill=AMBER)
    d.ellipse((X0 + TW - 120, y + 461, X0 + TW - 102, y + 479), fill=(*AMBER, a))
    d.text((X0 + TW, y + 470), "= VUS", font=font("Bold", 28), fill=(*AMBER, a), anchor="rm")
    fr.alpha_composite(lay)

# ---------------- scenes ----------------
def sc0(fr, t, D):
    show(fr, kicker("Genetics Clinical Series  •  Episode 8", CYAN), 330, t, 0.1)
    type_on(fr, "Gene panel", 410, t, 0.3, 72)
    type_on(fr, "or exome?", 500, t, 0.9, 72)
    if t > D * 0.3: type_on(fr, "Which to order, what each misses", 610, t, D * 0.3, 40, AMBER)
    gene_grid(fr, X0, 720, TW, 560, t, 0.6, highlight=PANEL, title="Exome: ~20,000 genes  •  Panel: a chosen few")
    show(fr, callout("For doctors and healthcare teams  •  with a published Indian case", CYAN, 34), 1640, t, D * 0.6); fire("whoosh", D * 0.6)

def sc_what(fr, t, D):
    dots(fr, 1); show(fr, kicker("Panel vs exome"), 260, t, 0.1)
    gene_grid(fr, X0, 330, TW, 460, t, 0.3, highlight=PANEL if t < D * 0.45 else None,
              title="Panel: genes for one question" if t < D * 0.45 else "Exome: coding parts of ~20,000 genes")
    show(fr, gcard("Panel: tens to a few hundred chosen genes", TEALG, 1, 34), 850, t, D * 0.2)
    show(fr, gcard("Exome: about 1-2% of the genome", CYAN, 2, 34), 1000, t, D * 0.5)
    show(fr, gcard("Where most known disease-causing variants lie", AMBER, 3, 34), 1150, t, D * 0.65)
    fire("pop", D * 0.2); fire("pop", D * 0.5); fire("pop", D * 0.65)

def sc_panel(fr, t, D):
    dots(fr, 2); show(fr, kicker("When a panel fits"), 260, t, 0.1)
    show(fr, headline("Clear clinical picture, known genes", 54), 320, t, 0.3)
    for i, (txt, c) in enumerate((("Hearing loss", CYAN), ("Cardiomyopathy", CORAL), ("Hereditary cancer risk", LAV))):
        fire("pop", D * (0.12 + 0.08 * i)); show(fr, gcard(txt, c, i + 1, 34), 470 + i * 140, t, D * (0.12 + 0.08 * i))
    coverage(fr, X0, 920, TW, 420, t, D * 0.4)
    show(fr, body("Usually fewer VUS and fewer unrelated findings", 34, SOFT), 1400, t, D * 0.65)

sc_exome = s_cards(3, "When exome fits", "Broad picture, no single panel fits",
    [("Developmental delay / intellectual disability", CYAN), ("Multiple congenital anomalies", AMBER),
     ("Multi-system disease", LAV), ("ACMG 2021: exome or genome first- or second-tier", TEALG)],
    lambda fr, t, D, y: show(fr, source_tag("Manickam et al., Genet Med 2021 (ACMG guideline)"), y + 10, t, D * 0.6), size=33)

def sc_virtual(fr, t, D):
    dots(fr, 4); show(fr, kicker("Virtual panel and reanalysis"), 260, t, 0.1)
    show(fr, headline("Sequence the exome, analyse a gene list first", 50), 320, t, 0.3)
    gene_grid(fr, X0, 480, TW, 440, t, 0.6, highlight=VIRT if t < D * 0.55 else None, title="Analyse list first, widen if needed")
    show(fr, gcard("Expand to more genes if the first look is negative", TEALG, 1, 33), 980, t, D * 0.55)
    show(fr, gcard("Data can be reanalysed later as new genes are found", AMBER, 2, 33), 1130, t, D * 0.7)
    fire("pop", D * 0.55); fire("pop", D * 0.7)

def sc_trio(fr, t, D):
    dots(fr, 5); show(fr, kicker("Trio testing"), 260, t, 0.1)
    lay, d = overlay(fr); e = ease((t - 0.4) / 0.6); a = int(255 * e)
    for (x, y, lab, c) in ((360, 520, "Father", CYAN), (720, 520, "Mother", LAV), (540, 820, "Child", AMBER)):
        d.ellipse((x - 90, y - 90, x + 90, y + 90), outline=(*c, a), width=6, fill=(*c, int(40 * e)))
        d.text((x, y), lab, font=font("Bold", 32), fill=(*WHITE, a), anchor="mm")
    d.line((360, 610, 540, 730), fill=(255, 255, 255, int(90 * e)), width=4); d.line((720, 610, 540, 730), fill=(255, 255, 255, int(90 * e)), width=4)
    fr.alpha_composite(lay)
    show(fr, gcard("De novo (new) changes found faster", TEALG, 1, 34), 1000, t, D * 0.35)
    show(fr, gcard("Clearer report", CYAN, 2, 34), 1150, t, D * 0.5)
    show(fr, callout("More in Episode 3", AMBER, 34), 1320, t, D * 0.65)
    fire("pop", D * 0.35); fire("pop", D * 0.5)

def sc_india(fr, t, D):
    dots(fr, 6); show(fr, kicker("Indian data"), 260, t, 0.1)
    show(fr, headline("78 children with neurodevelopmental disorders", 50), 320, t, 0.3)
    show(fr, body("Clinical exome, Thiruvananthapuram", 36, SOFT), 470, t, 0.5)
    lay, d = overlay(fr); e = ease((t - 0.8) / 1.2)
    rows = [("Pathogenic / likely pathogenic", 41, "41%", TEALG), ("VUS", 33.3, "33%", AMBER)]
    for i, (lab, v, txt, c) in enumerate(rows):
        yy = 580 + i * 170
        d.text((X0, yy), lab, font=font("Medium", 34), fill=SOFT, anchor="lm")
        L = max(16, (TW - 160) * v / 50 * e)
        d.rounded_rectangle((X0, yy + 40, X0 + L, yy + 100), 30, fill=c)
        d.text((X0 + L + 20, yy + 70), txt, font=font("Bold", 36), fill=WHITE, anchor="lm")
    fr.alpha_composite(lay)
    show(fr, source_tag("Valaparambil et al., Indian J Pediatr 2025;92:185-190 (SCTIMST)"), 960, t, D * 0.5)

def sc_vus(fr, t, D):
    dots(fr, 7); show(fr, kicker("The other side of exome"), 260, t, 0.1)
    show(fr, headline("More genes, more VUS", 56), 320, t, 0.3)
    venn(fr, 420, t, 0.6)
    show(fr, gcard("Secondary findings: important results unrelated to the question", CORAL, 1, 31), 960, t, D * 0.45)
    show(fr, gcard("Counsel first; written consent on what to report", TEALG, 2, 33), 1120, t, D * 0.6)
    fire("pop", D * 0.45); fire("pop", D * 0.6)

sc_miss = s_cards(8, "What both can miss", None,
    [("Large deletions and duplications: use CMA", CYAN), ("Repeat expansions, e.g. Fragile X", AMBER),
     ("Deep intronic changes", LAV), ("Methylation (imprinting) disorders", TEALG), ("Low-level mosaicism", CORAL)],
    lambda fr, t, D, y: show(fr, callout("A negative exome does not rule out a genetic disease", CORAL, 32), y + 20, t, D * 0.75), size=33)

def sc_sample(fr, t, D):
    dots(fr, 9); show(fr, kicker("Sample"), 260, t, 0.1)
    put(fr, tube_sprite((149, 117, 205), "EDTA"), 300, 640, 1.0, ease((t - 0.3) / 0.5))
    lay, d = overlay(fr); e = ease((t - 0.5) / 0.5)
    d.text((300, 950), "Blood (EDTA)", font=font("Bold", 34), fill=(*SOFT, int(255 * e)), anchor="mm"); fr.alpha_composite(lay)
    show(fr, gcard("Trio: parents' samples too", TEALG, 1, 33), 1010, t, D * 0.25)
    show(fr, gcard("Prenatal: amniotic fluid or CVS", LAV, 2, 33), 1160, t, D * 0.4)
    show(fr, callout("Prenatal: disease testing only; sex never disclosed (PCPNDT)", CORAL, 32), 1320, t, D * 0.55)
    fire("pop", D * 0.25); fire("pop", D * 0.4)

def sc_case1(fr, t, D):
    dots(fr, 10); show(fr, kicker("Case study from India", CORAL), 260, t, 0.1)
    put(fr, PAPER, 540, 650, 0.62, ease((t - 0.4) / 0.6))
    for i, (txt, c) in enumerate((("Girl, 7 months; parents related", CYAN), ("2 months of watery diarrhoea, severe malnutrition", AMBER),
                                  ("Thick skin, dark patches over knuckles", LAV), ("Elbow contractures, gum swelling, ear nodules", TEALG))):
        show(fr, gcard(txt, c, None, 31), 930 + i * 140, t, D * (0.22 + 0.1 * i))
    show(fr, source_tag("Nayek et al., Cureus 2026;18(2):e103465 (AIIMS Bhopal), CC BY"), 1500, t, D * 0.65)

def sc_case2(fr, t, D):
    dots(fr, 11); show(fr, kicker("Case: the search"), 260, t, 0.1)
    for i, (txt, c) in enumerate((("Stool tests, ultrasound, gut biopsy: nothing specific", (120, 140, 170)),
                                  ("Stool electrolytes normal: not CF or congenital chloride diarrhoea", (120, 140, 170)))):
        show(fr, gcard(txt, c, i + 1, 31), 330 + i * 160, t, D * (0.08 + 0.12 * i))
    gene_grid(fr, X0, 680, TW, 420, t, D * 0.4, highlight={311}, title="Exome")
    if t > D * 0.55:
        lay, d = overlay(fr); cw = (TW - 40) / 30; ch = (420 - 90) / 20; r_, c_ = divmod(311, 30)
        gx = X0 + 20 + c_ * cw + cw / 2; gy = 680 + 75 + r_ * ch + ch / 2
        d.ellipse((gx - 34, gy - 34, gx + 34, gy + 34), outline=CORAL, width=6); fr.alpha_composite(lay)
    show(fr, gcard("ANTXR2: pathogenic change in both copies", CORAL, 3, 33), 1160, t, D * 0.6)
    show(fr, callout("Infantile systemic hyalinosis", TEALG, 40), 1320, t, D * 0.72); fire("ding", D * 0.72)

def sc_case3(fr, t, D):
    dots(fr, 12); show(fr, kicker("Why exome fitted, and what followed"), 260, t, 0.1)
    show(fr, headline("Gut, skin, joints, gums: no single panel fitted", 48), 320, t, 0.3)
    for i, (txt, c) in enumerate((("Nutrition, albumin, physiotherapy", CYAN), ("Diarrhoea controlled; weight stable", TEALG),
                                  ("Motor improvement minimal", AMBER), ("Family counselled on recurrence risk", LAV))):
        fire("pop", D * (0.2 + 0.12 * i)); show(fr, gcard(txt, c, i + 1, 33), 520 + i * 150, t, D * (0.2 + 0.12 * i))

sc_take = s_cards(13, "Key messages", None,
    [("Clear picture with known genes: panel", TEALG), ("Broad or unclear picture: exome, ideally trio", CYAN),
     ("Virtual panels and reanalysis give the best of both", LAV), ("Counsel on VUS and secondary findings first", AMBER),
     ("A negative report is not the final answer", CORAL)], size=32)

SC = [(film(sc0), "doc"), (film(sc_what), "doc"), (film(sc_panel), "doc"), (film(sc_exome), "doc"), (film(sc_virtual), "doc"),
      (film(sc_trio), "doc"), (film(sc_india), "doc"), (film(sc_vus), "doc"), (film(sc_miss), "doc"), (film(sc_sample), "doc"),
      (film(sc_case1), "doc"), (film(sc_case2), "doc"), (film(sc_case3), "doc"), (film(sc_take), "doc"),
      (close_scene("Panel or exome first?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si, (fn, bg) in enumerate(SC):
            d = 16 if si < len(SC) - 1 else 33; p = .95 if si else 0.125; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((300, 533)))
        s = Image.new("RGB", (300 * 5, 533 * 3), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 300, (i // 5) * 533))
        s.save(sys.argv[2] if len(sys.argv) > 2 else "/tmp/sheet_g008.png")
    else: run(SC, "/tmp/g008_", "Genetics_Ep08_Panel_or_Exome_Hindi.mp4", max_sec=480)
