"""Genetics Clinical Series, Episode 6: Chromosomal microarray in practice."""
import sys, random
from cbc_cartoon import run
from gen_series import *
from hts_close import close_scene

TOT[0] = 13
TOPIC = "GENETICS SERIES  •  EPISODE 6"
PAPER = paper_sprite(["Chromosomal microarray", "detects 11p14.3-p12", "microdeletion: WAGR"], "Cureus, 2024 (Pune, India)")

def baf_plot(fr, x, y, w, h, t, tin, roh=(0.35, 0.7), title="SNP array: B-allele frequency"):
    """Three bands (AA, AB, BB); the middle AB band disappears in a region of homozygosity."""
    panel(fr, x, y, w, h, title)
    lay, d = overlay(fr); r = random.Random(3); p = ease((t - tin) / 1.5)
    x0, x1 = x + 30, x + w - 30; top, bot = y + 90, y + h - 60
    for i in range(1100):
        u = i / 1100
        if u > p: break
        k = r.random()
        if roh[0] < u < roh[1]: v = 0.0 if k < 0.5 else 1.0
        else: v = 0.0 if k < 0.33 else (0.5 if k < 0.66 else 1.0)
        v += r.gauss(0, 0.03)
        xx = x0 + u * (x1 - x0); yy = bot - v * (bot - top)
        col = AMBER if roh[0] < u < roh[1] else (120, 200, 230)
        d.ellipse((xx - 2, yy - 2, xx + 2, yy + 2), fill=(*col, 200))
    if p > roh[1]:
        a, b = x0 + roh[0] * (x1 - x0), x0 + roh[1] * (x1 - x0)
        d.text(((a + b) / 2, (top + bot) / 2), "No AB band", font=font("Bold", 30), fill=AMBER, anchor="mm")
    fr.alpha_composite(lay)

def iscn(fr, y, t, tin):
    """ISCN line with parts highlighted."""
    lay, d = overlay(fr); e = ease((t - tin) / 0.6); a = int(255 * e)
    d.rounded_rectangle((X0, y, X0 + TW, y + 120), 22, fill=(255, 255, 255, int(24 * e)), outline=(255, 255, 255, int(70 * e)), width=2)
    parts = [("arr[GRCh38] ", SOFT), ("11p14.3p12", CYAN), ("(22,560,576_38,466,045)", LAV), ("x1", CORAL)]
    fnt = font("Bold", 30); xx = X0 + 24
    for txt, c in parts:
        d.text((xx, y + 60), txt, font=fnt, fill=(*c, a), anchor="lm"); xx += fnt.getlength(txt)
    fr.alpha_composite(lay)

# ---------------- scenes ----------------
def sc0(fr, t, D):
    show(fr, kicker("Genetics Clinical Series  •  Episode 6", CYAN), 330, t, 0.1)
    type_on(fr, "Chromosomal microarray", 410, t, 0.3, 66)
    type_on(fr, "in practice", 500, t, 0.9, 66)
    if t > D * 0.3: type_on(fr, "What it finds, what it misses, how to read it", 610, t, D * 0.3, 40, AMBER)
    cma_plot(fr, X0, 760, TW, 520, t, 0.6)
    show(fr, callout("For doctors and healthcare teams  •  with a published Indian case", CYAN, 34), 1640, t, D * 0.6); fire("whoosh", D * 0.6)

def sc_what(fr, t, D):
    dots(fr, 1); show(fr, kicker("What does CMA detect?"), 260, t, 0.1)
    show(fr, headline("Missing or extra pieces of DNA (copy number variants)", 52), 320, t, 0.3)
    cma_plot(fr, X0, 520, TW, 480, t, 0.6, del_at=(0.4, 0.5), title="Deletion = one copy lost")
    show(fr, gcard("Karyotype sees changes of about 5-10 Mb", AMBER, 1, 34), 1060, t, D * 0.4)
    show(fr, gcard("CMA: much smaller, depending on the platform", TEALG, 2, 34), 1210, t, D * 0.55)
    fire("pop", D * 0.4); fire("pop", D * 0.55)

def sc_when(fr, t, D):
    dots(fr, 2); show(fr, kicker("When to order it"), 260, t, 0.1)
    show(fr, headline("First-tier test", 58), 320, t, 0.3)
    for i, (txt, c) in enumerate((("Unexplained developmental delay / intellectual disability", CYAN), ("Autism spectrum disorder", LAV),
                                  ("Multiple congenital anomalies", AMBER), ("Structural anomaly on fetal scan (prenatal)", CORAL), ("Pregnancy loss / stillbirth tissue", TEALG))):
        fire("pop", D * (0.12 + 0.1 * i)); show(fr, gcard(txt, c, i + 1, 32), 440 + i * 145, t, D * (0.12 + 0.1 * i))
    show(fr, source_tag("ISCA consensus, Am J Hum Genet 2010; ACOG Committee Opinion 682"), 1190, t, D * 0.7)

def sc_yield(fr, t, D):
    dots(fr, 3); show(fr, kicker("Diagnostic yield"), 260, t, 0.1)
    lay, d = overlay(fr); e = ease((t - 0.4) / 1.2)
    rows = [("Karyotype", 3, "~3%", (120, 140, 170)), ("CMA", 20, "15-20%", TEALG)]
    for i, (lab, v, txt, c) in enumerate(rows):
        yy = 400 + i * 130
        d.text((X0, yy + 30), lab, font=font("Medium", 36), fill=SOFT, anchor="lm")
        L = max(16, (TW - 420) * v / 22 * e)
        d.rounded_rectangle((X0 + 230, yy, X0 + 230 + L, yy + 60), 30, fill=c)
        d.text((X0 + 250 + L, yy + 30), txt, font=font("Bold", 36), fill=WHITE, anchor="lm")
    fr.alpha_composite(lay)
    show(fr, source_tag("Miller et al., Am J Hum Genet 2010 (33 studies, 21,698 patients)"), 680, t, 0.8)
    show(fr, headline("India: 18 of 86 children (20.9%)", 50), 820, t, D * 0.4)
    show(fr, body("with intellectual disability had a pathogenic CNV", 36, SOFT), 900, t, D * 0.45)
    show(fr, source_tag("Boggula et al., Indian J Med Res 2015 (SGPGIMS, Lucknow)"), 990, t, D * 0.5)

def sc_snp(fr, t, D):
    dots(fr, 4); show(fr, kicker("Extra from a SNP array"), 260, t, 0.1)
    baf_plot(fr, X0, 330, TW, 470, t, 0.3)
    show(fr, gcard("Long runs of homozygosity: parents related, or uniparental disomy", AMBER, 1, 32), 860, t, D * 0.35)
    show(fr, gcard("Can point towards recessive genes in that region", TEALG, 2, 33), 1020, t, D * 0.5)
    show(fr, gcard("Can also detect triploidy", LAV, 3, 34), 1170, t, D * 0.62)
    fire("pop", D * 0.35); fire("pop", D * 0.5); fire("pop", D * 0.62)

sc_miss = s_cards(5, "What CMA misses", None,
    [("Balanced translocations and inversions: use karyotype", AMBER), ("Low-level mosaicism", LAV),
     ("Single-gene changes: use panel or exome", CYAN), ("Repeat expansions, e.g. Fragile X: separate test", CORAL)],
    lambda fr, t, D, y: put(fr, KARYO, 540, y + 330, 0.62, ease((t - D * 0.6) / 0.6)), size=33)
KARYO = karyogram()

def sc_report(fr, t, D):
    dots(fr, 6); show(fr, kicker("Reading the report"), 260, t, 0.1)
    iscn(fr, 340, t, 0.3)
    for i, (txt, c) in enumerate((("Region on the chromosome", CYAN), ("Start and end position", LAV), ("x1 = one copy (deletion); x3 = duplication", CORAL))):
        show(fr, gcard(txt, c, i + 1, 32), 500 + i * 140, t, D * (0.2 + 0.12 * i)); fire("pop", D * (0.2 + 0.12 * i))
    show(fr, body("Then: size, genes in the region, and classification", 34, SOFT), 950, t, D * 0.55)
    five_tier(fr, 1040, t, D * 0.6)

def sc_vus(fr, t, D):
    dots(fr, 7); show(fr, kicker("VUS and inherited CNVs"), 260, t, 0.1)
    cards = [("Uncertain CNV: test the parents", AMBER), ("Inherited from a healthy parent does not always mean harmless", CORAL),
             ("Some CNVs show variable expression, e.g. 15q11.2, 16p11.2", LAV), ("Some CNVs may be common, harmless variants in Indians", TEALG)]
    for i, (txt, c) in enumerate(cards):
        fire("pop", D * (0.1 + 0.14 * i)); show(fr, gcard(txt, c, i + 1, 32), 340 + i * 160, t, D * (0.1 + 0.14 * i))
    show(fr, source_tag("Boggula et al., Indian J Med Res 2015; ACMG/ClinGen CNV standards 2020"), 1020, t, D * 0.7)

def sc_sample(fr, t, D):
    dots(fr, 8); show(fr, kicker("Sample"), 260, t, 0.1)
    put(fr, tube_sprite((149, 117, 205), "EDTA"), 300, 640, 1.0, ease((t - 0.3) / 0.5))
    lay, d = overlay(fr); e = ease((t - 0.5) / 0.5)
    d.text((300, 950), "Blood (EDTA)", font=font("Bold", 34), fill=(*SOFT, int(255 * e)), anchor="mm"); fr.alpha_composite(lay)
    show(fr, gcard("Prenatal: amniotic fluid or CVS", LAV, 1, 33), 1010, t, D * 0.3)
    show(fr, gcard("Pregnancy loss: tissue; no cell culture needed", AMBER, 2, 33), 1160, t, D * 0.45)
    show(fr, callout("Prenatal: disease testing only; sex never disclosed (PCPNDT)", CORAL, 32), 1320, t, D * 0.6)
    fire("pop", D * 0.3); fire("pop", D * 0.45)

def sc_case1(fr, t, D):
    dots(fr, 9); show(fr, kicker("Case study from India", CORAL), 260, t, 0.1)
    put(fr, PAPER, 540, 690, 0.72, ease((t - 0.4) / 0.6))
    show(fr, gcard("Baby boy, parents related, birth weight 2.1 kg", CYAN, None, 33), 1020, t, D * 0.25)
    show(fr, gcard("At birth: undescended testes, hypospadias, small penis", AMBER, None, 33), 1170, t, D * 0.38)
    show(fr, gcard("3 months: poor eye contact; both irises absent (aniridia)", LAV, None, 32), 1320, t, D * 0.52)
    show(fr, source_tag("Majjigudda et al., Cureus 2024;16(10):e72479 (Pune), CC BY"), 1480, t, D * 0.6)

def sc_case2(fr, t, D):
    dots(fr, 10); show(fr, kicker("Case: the microarray answer"), 260, t, 0.1)
    cma_plot(fr, X0, 330, TW, 460, t, 0.3, del_at=(0.3, 0.58), title="Chromosome 11 (illustration)")
    show(fr, gcard("CMA: 15.9 Mb deletion at 11p14.3-p12", CORAL, 1, 34), 850, t, D * 0.35)
    show(fr, gcard("About 100 genes, including WT1 and PAX6", AMBER, 2, 34), 1000, t, D * 0.48)
    show(fr, callout("Diagnosis: WAGR syndrome", TEALG, 40), 1160, t, D * 0.6); fire("ding", D * 0.6)

def sc_case3(fr, t, D):
    dots(fr, 11); show(fr, kicker("Why it changed care"), 260, t, 0.1)
    for i, (txt, c) in enumerate((("WT1 lost: kidney ultrasound every 3 months until age 8 (Wilms tumour)", CORAL), ("Kidney function checks from about age 10", AMBER),
                                  ("PAX6: yearly eye-pressure checks (glaucoma)", CYAN), ("Planned surgery, physiotherapy, development therapy", LAV),
                                  ("Counselling; prenatal microarray offered in future pregnancy", TEALG))):
        fire("pop", D * (0.1 + 0.12 * i)); show(fr, gcard(txt, c, i + 1, 31), 340 + i * 165, t, D * (0.1 + 0.12 * i))

sc_take = s_cards(12, "Key messages", None,
    [("CMA is first-tier for unexplained delay, autism and multiple anomalies", CYAN), ("Know what it misses; pick karyotype, panel or exome when needed", AMBER),
     ("Read the region, size, genes and class", LAV), ("Test parents for uncertain CNVs", TEALG), ("The genes in a deletion can guide surveillance", CORAL)], size=31)

SC = [(film(sc0), "doc"), (film(sc_what), "doc"), (film(sc_when), "doc"), (film(sc_yield), "doc"), (film(sc_snp), "doc"),
      (film(sc_miss), "doc"), (film(sc_report), "doc"), (film(sc_vus), "doc"), (film(sc_sample), "doc"), (film(sc_case1), "doc"),
      (film(sc_case2), "doc"), (film(sc_case3), "doc"), (film(sc_take), "doc"),
      (close_scene("Do you order CMA first-tier?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si, (fn, bg) in enumerate(SC):
            d = 16 if si < len(SC) - 1 else 33; p = .95 if si else 0.125; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((300, 533)))
        s = Image.new("RGB", (300 * 5, 533 * 3), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 300, (i // 5) * 533))
        s.save("sheet_g006.png")
    else: run(SC, "/tmp/g006_", "Genetics_Ep06_Microarray_in_Practice_Hindi.mp4", max_sec=480)
