"""Genetics Clinical Series, Episode 2: Reading a genetic report (pathogenic, likely pathogenic, VUS)."""
import sys
from cbc_cartoon import run
from gen_series import *
from hts_close import close_scene

TOT[0] = 16
TOPIC = "GENETICS SERIES  •  EPISODE 2"
PAPER = paper_sprite(["Nabais Sá-de Vries", "syndrome type 1 in a", "Mexican girl: a case report"], "Cureus, 2026 (Mexico)")

def gen_report(highlight=None):
    """Mock genetic test report (illustrative, no real patient)."""
    w, h = 900, 1000; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((14, 14, w, h), fill=(0, 0, 0, 90)); d.rectangle((0, 0, w - 14, h - 14), fill=(251, 251, 248))
    d.rectangle((0, 0, w - 14, 90), fill=(16, 42, 78))
    d.text((30, 45), "GENETIC TEST REPORT  (sample layout)", font=font("Bold", 32), fill=WHITE, anchor="lm")
    rows = [("A", "Patient & indication", "Developmental delay, heart defect"), ("B", "Test", "Whole exome sequencing (proband)"),
            ("C", "Result summary", "Variant of uncertain significance")]
    y = 120
    for k, a, b in rows:
        hl = highlight == k
        if hl: d.rectangle((10, y - 8, w - 24, y + 62), fill=(255, 236, 170))
        d.text((30, y), a, font=font("Bold", 26), fill=(16, 42, 78)); d.text((30, y + 32), b, font=font("Regular", 24), fill=(60, 70, 90)); y += 92
    # variant table
    hl = highlight == "D"
    if hl: d.rectangle((10, y - 8, w - 24, y + 250), fill=(255, 236, 170))
    d.text((30, y), "Variant table", font=font("Bold", 26), fill=(16, 42, 78)); y += 42
    cols = [("Gene", 30), ("Variant", 150), ("Zygosity", 470), ("Class", 650)]
    for c, x in cols: d.text((x, y), c, font=font("Bold", 22), fill=(90, 100, 120))
    d.line((30, y + 32, w - 44, y + 32), fill=(190, 195, 205), width=2); y += 44
    vals = [("SPOP", 30), ("c.351G>T", 150), ("Heterozygous", 470), ("VUS", 650)]
    for c, x in vals: d.text((x, y), c, font=font("Medium", 24), fill=(20, 30, 60))
    d.text((150, y + 34), "p.(Met117Ile)", font=font("Medium", 24), fill=(20, 30, 60))
    d.text((30, y + 80), "Inheritance: autosomal dominant   •   Parental testing: not done", font=font("Regular", 21), fill=(90, 100, 120))
    y += 150
    for k, a, n in (("E", "Interpretation", 3), ("F", "Recommendations", 2), ("G", "Limitations", 2)):
        hl = highlight == k
        if hl: d.rectangle((10, y - 8, w - 24, y + 40 + n * 26), fill=(255, 236, 170))
        d.text((30, y), a, font=font("Bold", 26), fill=(16, 42, 78)); r = random.Random(len(a))
        for j in range(n): d.rounded_rectangle((30, y + 42 + j * 26, 30 + r.uniform(0.6, 0.95) * (w - 90), y + 52 + j * 26), 5, fill=(205, 210, 220))
        y += 60 + n * 26
    return im
REPORT = gen_report(); REPORT_D = gen_report("D")

def v_intro(fr, t, D): helix(fr, 760, 1200, 700, t, amp=170, alpha=150)

def sc0(fr, t, D):
    v_intro(fr, t, D)
    show(fr, kicker("Genetics Clinical Series  •  Episode 2", CYAN), 330, t, 0.1)
    type_on(fr, "Reading a genetic report", 410, t, 0.4, 68)
    if t > D * 0.35: type_on(fr, "Pathogenic, likely pathogenic, VUS", 520, t, D * 0.35, 46, AMBER)
    show(fr, callout("For doctors and healthcare teams  •  with a published case study", CYAN, 34), 1640, t, D * 0.55); fire("whoosh", D * 0.55)

def sc_parts(fr, t, D):
    dots(fr, 1); show(fr, kicker("Parts of a report"), 260, t, 0.1)
    put(fr, REPORT, 540, 860, 0.95, ease((t - 0.3) / 0.7))
    show(fr, callout("Indication  •  Result  •  Variant table  •  Interpretation  •  Limits", TEALG, 32), 1450, t, D * 0.6)

def sc_hgvs(fr, t, D):
    dots(fr, 2); show(fr, kicker("How a variant is written (HGVS)"), 260, t, 0.1)
    lay, d = overlay(fr); e = ease((t - 0.4) / 0.6)
    d.text((540, 400), "c.351G>T", font=font("Bold", 110), fill=(*CYAN, int(255 * e)), anchor="mm")
    fr.alpha_composite(lay)
    show(fr, gcard("c. = coding DNA: at position 351, G is replaced by T", CYAN, None, 34), 500, t, D * 0.2)
    if t > D * 0.45:
        lay, d = overlay(fr); e = ease((t - D * 0.45) / 0.6)
        d.text((540, 800), "p.Met117Ile", font=font("Bold", 110), fill=(*AMBER, int(255 * e)), anchor="mm")
        fr.alpha_composite(lay)
    show(fr, gcard("p. = protein: at amino acid 117, methionine becomes isoleucine (missense)", AMBER, None, 34), 900, t, D * 0.5)
    if t > D * 0.6: sanger(fr, X0, 1120, TW, 320, t, D * 0.6, SEQ, (4, "T"), title="One-letter change (illustration)")

def sc_tiers(fr, t, D):
    dots(fr, 3); show(fr, kicker("Five classes (ACMG/AMP 2015)"), 260, t, 0.1)
    five_tier(fr, 340, t, 0.4)
    show(fr, gcard("Likely pathogenic = more than 90% certainty that it causes disease", CORAL, None, 35), 980, t, D * 0.55)
    show(fr, source_tag("Richards et al., Genet Med 2015;17(5):405-424"), 1150, t, D * 0.6)

sc_evidence = s_cards(4, "What decides the class?", "Evidence from many sources",
    [("Population frequency (gnomAD)", CYAN), ("Computational & functional studies", LAV), ("Segregation in the family", AMBER),
     ("De novo (new) in the patient", CORAL), ("Match with the patient's features", TEALG)], size=34)

def sc_zyg(fr, t, D):
    dots(fr, 5); show(fr, kicker("Zygosity & inheritance"), 260, t, 0.1)
    items = [("Heterozygous: change in one copy", CYAN), ("Homozygous: change in both copies", AMBER),
             ("Recessive disease + one copy = usually a carrier, not affected", CORAL)]
    for i, (txt, c) in enumerate(items):
        fire("pop", D * (0.12 + 0.15 * i)); show(fr, gcard(txt, c, i + 1, 35), 340 + i * 150, t, D * (0.12 + 0.15 * i))
    lay, d = overlay(fr); p = ease((t - D * 0.55) / 0.6)
    if p > 0:
        for j, (lab, a, b) in enumerate((("Hetero", CORAL, SOFT), ("Homo", CORAL, CORAL))):
            cx = 330 + j * 420
            for k, col in enumerate((a, b)):
                d.rounded_rectangle((cx - 60 + k * 70, 900, cx - 20 + k * 70, 1260), 20, fill=(*SOFT, int(220 * p)))
                d.ellipse((cx - 60 + k * 70, 1050, cx - 20 + k * 70, 1090), fill=(*col, int(255 * p)))
            d.text((cx, 1310), lab, font=font("Bold", 34), fill=(*SOFT, int(255 * p)), anchor="mm")
    fr.alpha_composite(lay)
    show(fr, callout("Always read with the inheritance pattern", TEALG, 36), 1420, t, D * 0.7)

def sc_pheno(fr, t, D):
    dots(fr, 6); show(fr, kicker("The key question"), 260, t, 0.1)
    show(fr, headline("Does the variant fit the patient?", 60), 320, t, 0.3)
    lay, d = overlay(fr); e = ease((t - D * 0.25) / 0.6)
    for i, (lab, c) in enumerate((("Variant", CYAN), ("Clinical picture", AMBER))):
        cx = 400 + i * 280
        d.ellipse((cx - 230, 620, cx + 230, 1080), fill=(*c, int(70 * e)), outline=(*c, int(255 * e)), width=5)
        d.text((cx + (-110 if i == 0 else 110), 850), lab.replace(" ", "\n"), font=font("Bold", 34), fill=(*WHITE, int(255 * e)), anchor="mm", align="center")
    d.text((540, 850), "Fit?", font=font("Bold", 40), fill=(*WHITE, int(255 * e)), anchor="mm")
    fr.alpha_composite(lay)
    show(fr, gcard("Even a pathogenic variant may not explain the current illness if it does not fit", CORAL, None, 34), 1160, t, D * 0.55)

sc_vus = s_cards(7, "A VUS on the report?", None,
    [("Do not base treatment decisions on it", CORAL), ("Do not use it for predictive testing of relatives", CORAL),
     ("Do: correlate with clinical features", TEALG), ("Do: test parents / relatives if advised", TEALG), ("Do: ask for re-analysis over time", TEALG)], size=34)

def sc_recl(fr, t, D):
    dots(fr, 8); show(fr, kicker("Can a VUS change?"), 260, t, 0.1)
    counter(fr, 25, "%", 330, t, 0.4, size=150, prefix="~")
    show(fr, body("(24.9%) of reported VUS were reclassified (1.45 million people tested, 2006-2016, hereditary cancer)", 34, SOFT), 520, t, 0.8)
    lay, d = overlay(fr)
    if t > D * 0.4:
        e = ease((t - D * 0.4) / 0.9)
        for i, (lab, v, c) in enumerate((("To benign / likely benign", 91.2, TEALG), ("To pathogenic / likely pathogenic", 8.7, CORAL))):
            yy = 760 + i * 170; d.text((X0, yy), lab, font=font("Medium", 32), fill=SOFT)
            d.rounded_rectangle((X0, yy + 50, X0 + (TW - 170) * v / 100 * e, yy + 100), 25, fill=c)
            d.text((X0 + (TW - 170) * v / 100 * e + 16, yy + 75), f"{v}%", font=font("Bold", 34), fill=WHITE, anchor="lm")
    fr.alpha_composite(lay)
    show(fr, gcard("Median time to reclassification: ~1.2 years (down), ~1.9 years (up)", AMBER, None, 33), 1130, t, D * 0.6)
    show(fr, source_tag("Mersch, Ross et al., JAMA 2018 (as reported by Healio)"), 1300, t, D * 0.65)

def sc_parents(fr, t, D):
    dots(fr, 9); show(fr, kicker("Why test the parents?"), 260, t, 0.1)
    for i, (title, mut) in enumerate((("Child", (4, "T")), ("Mother", None), ("Father", None))):
        tin = 0.4 + i * D * 0.12
        if t > tin: sanger(fr, X0, 340 + i * 280, TW, 250, t, tin, SEQ, mut, title=title)
    show(fr, gcard("Confirmed de novo = strong evidence (PS2); assumed only = moderate (PM6)", AMBER, None, 33), 1200, t, D * 0.55)
    show(fr, gcard("Same variant in a healthy parent can lower suspicion (depends on the disease)", CYAN, None, 33), 1370, t, D * 0.7)

def sc_sf(fr, t, D):
    dots(fr, 10); show(fr, kicker("Secondary findings"), 260, t, 0.1)
    show(fr, headline("Actionable results not linked to the reason for testing", 52), 320, t, 0.3)
    hl = set(range(55, 60)) | set(range(210, 214)) | set(range(400, 404))
    gene_grid(fr, X0, 520, TW, 360, t, 0.5, hl, title="Exome: a few actionable genes lit")
    show(fr, gcard("ACMG list: 80+ genes, e.g. some cancer and heart conditions (SF v3.3, 2025)", CORAL, 1, 33), 940, t, D * 0.45)
    show(fr, gcard("Reported or not: decided at consent, before the test", TEALG, 2, 34), 1110, t, D * 0.62)
    fire("pop", D * 0.45); fire("pop", D * 0.62)

sc_neg = s_cards(11, "A negative report", "Does not rule out a genetic disease",
    [("Exome misses some variant types (repeats, many CNVs, mtDNA)", CORAL), ("New gene discoveries every year", CYAN),
     ("Re-analysis after 1-2 years can give a new diagnosis", TEALG)],
    lambda fr, t, D, y: helix(fr, 540, y + 230, 300, t, amp=300, turns=1.2, alpha=70, n=30))

def sc_case1(fr, t, D):
    dots(fr, 12); show(fr, kicker("Case study", CORAL), 260, t, 0.1)
    show(fr, headline("A published case from Mexico", 58), 320, t, 0.3)
    put(fr, PAPER, 540, 820, 0.8, ease((t - 0.5) / 0.6))
    show(fr, gcard("IVF twin girl: breathing difficulty; echo showed PDA, PFO, pulmonary hypertension", CYAN, None, 33), 1200, t, D * 0.4)
    show(fr, gcard("Distinct facial features, developmental delay", AMBER, None, 34), 1370, t, D * 0.55)
    show(fr, source_tag("Olivares-Huerta et al., Cureus 2026;18(4):e107064"), 1510, t, D * 0.6)

def sc_case2(fr, t, D):
    dots(fr, 13); show(fr, kicker("Case: the work-up"), 260, t, 0.1)
    show(fr, gcard("Karyotype: 46,XX (normal)", TEALG, 1, 35), 330, t, 0.3)
    show(fr, gcard("Whole exome sequencing", CYAN, 2, 35), 480, t, D * 0.2)
    fire("pop", 0.3); fire("pop", D * 0.2)
    put(fr, REPORT_D, 540, 1150, 0.72, ease((t - D * 0.35) / 0.7))
    show(fr, callout("SPOP c.351G>T p.(Met117Ile): reported as VUS", AMBER, 34), 1560, t, D * 0.6); fire("ding", D * 0.6)

sc_case3 = s_cards(14, "Case: adding up the evidence", None,
    [("PM2: absent from population databases", CYAN), ("PM1: in a critical protein domain (MATH)", LAV),
     ("PP3: computer tools predict damage", AMBER), ("PM6: de novo assumed from the pedigree", CORAL)],
    lambda fr, t, D, y: show(fr, callout("Authors: likely pathogenic  >  Nabais Sá-de Vries syndrome type 1", TEALG, 32), y + 20, t, D * 0.7))

def sc_case4(fr, t, D):
    dots(fr, 15); show(fr, kicker("The lesson from this case"), 260, t, 0.1)
    show(fr, gcard("No parental testing (no segregation)", CORAL, 1, 35), 330, t, 0.3)
    show(fr, gcard("No functional study", CORAL, 2, 35), 480, t, D * 0.15)
    pedigree_y = 680
    if t > D * 0.3:
        lay, d = overlay(fr); e = ease((t - D * 0.3) / 0.6)
        d.rectangle((340, pedigree_y, 440, pedigree_y + 100), outline=(*SOFT, int(255 * e)), width=5)
        d.ellipse((640, pedigree_y, 740, pedigree_y + 100), outline=(*SOFT, int(255 * e)), width=5)
        d.line((440, pedigree_y + 50, 640, pedigree_y + 50), fill=(*SOFT, int(255 * e)), width=5)
        d.line((540, pedigree_y + 50, 540, pedigree_y + 190), fill=(*SOFT, int(255 * e)), width=5)
        d.ellipse((490, pedigree_y + 190, 590, pedigree_y + 290), fill=(*CORAL, int(255 * e)))
        for x in (390, 690): d.text((x, pedigree_y + 140), "?", font=font("Bold", 56), fill=(*AMBER, int(255 * e)), anchor="mm")
        d.text((540, pedigree_y + 340), "Test both parents", font=font("Bold", 36), fill=(*AMBER, int(255 * e)), anchor="mm")
        fr.alpha_composite(lay)
    show(fr, gcard("Confirmed de novo would make the evidence stronger (PS2)", TEALG, None, 34), 1110, t, D * 0.55)
    show(fr, callout("Trio testing is often the simplest way to resolve a VUS", AMBER, 34), 1290, t, D * 0.7); fire("ding", D * 0.7)

sc_take = s_cards(16, "Key messages", None,
    [("Know the five classes", CYAN), ("Read with phenotype and inheritance", AMBER), ("No clinical decisions on a VUS", CORAL),
     ("Parental testing and re-analysis can resolve it", TEALG), ("Every report with genetic counselling", LAV)], size=34)

SC = [(film(sc0), "doc"), (film(sc_parts), "doc"), (film(sc_hgvs), "doc"), (film(sc_tiers), "doc"), (film(sc_evidence), "doc"),
      (film(sc_zyg), "doc"), (film(sc_pheno), "doc"), (film(sc_vus), "doc"), (film(sc_recl), "doc"), (film(sc_parents), "doc"),
      (film(sc_sf), "doc"), (film(sc_neg), "doc"), (film(sc_case1), "doc"), (film(sc_case2), "doc"), (film(sc_case3), "doc"),
      (film(sc_case4), "doc"), (film(sc_take), "doc"), (close_scene("How often do you see a VUS?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si, (fn, bg) in enumerate(SC):
            d = 16 if si < len(SC) - 1 else 33; NOW.update(t=d * .95, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * .95, d); ims.append(fr.convert("RGB").resize((300, 533)))
        s = Image.new("RGB", (300 * 6, 533 * 3), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 6) * 300, (i // 6) * 533))
        s.save("sheet_g002.png")
    else: run(SC, "/tmp/g002_", "Genetics_Ep02_Reading_a_Report_Hindi.mp4", max_sec=480)
