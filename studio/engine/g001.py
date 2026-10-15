"""Genetics Clinical Series, Episode 1: Which genetic test, when?"""
import sys
from cbc_cartoon import run
from gen_series import *
from hts_close import close_scene

TOT[0] = 16
TOPIC = "GENETICS SERIES  •  EPISODE 1"
KARYO = karyogram()
CHR = chromosome_sprite("Chromosome", 0.4, "Gene")
PAPER = paper_sprite(["Role of genetics in", "infantile epilepsy:", "a case series of three cases"], "J Family Med Prim Care, 2025 (India)")

def v_intro(fr, t, D):
    helix(fr, 760, 1200, 700, t, amp=170, alpha=150)

def sc0(fr, t, D):
    v_intro(fr, t, D)
    show(fr, kicker("Genetics Clinical Series  •  Episode 1", CYAN), 330, t, 0.1)
    type_on(fr, "Which genetic test, when?", 410, t, 0.4, 68)
    if t > D * 0.35: type_on(fr, "Karyotype, microarray, panel or exome", 520, t, D * 0.35, 46, AMBER)
    show(fr, callout("For doctors and healthcare teams  •  with a published case study", CYAN, 34), 1640, t, D * 0.55); fire("whoosh", D * 0.55)

def sc_levels(fr, t, D):
    dots(fr, 1); show(fr, kicker("Where can the change be?"), 260, t, 0.1)
    items = [("Whole chromosome number (e.g. Down syndrome)", CORAL), ("Missing / extra piece: copy number variant (CNV)", AMBER),
             ("Inside one gene: single letter change or small deletion", CYAN), ("Special: repeat expansion (e.g. Fragile X)", LAV)]
    for i, (txt, c) in enumerate(items):
        fire("pop", D * (0.12 + 0.14 * i)); show(fr, gcard(txt, c, i + 1, 35), 340 + i * 150, t, D * (0.12 + 0.14 * i))
    if t > D * 0.5: sanger(fr, X0, 980, TW, 330, t, D * 0.5, SEQ, (9, "C"), title="A single-letter change")
    show(fr, callout("Each test sees only some of these", TEALG, 38), 1380, t, D * 0.75)

def sc_karyo(fr, t, D):
    dots(fr, 2); show(fr, kicker("Karyotype"), 260, t, 0.1)
    show(fr, headline("Chromosomes under the microscope", 56), 320, t, 0.3)
    put(fr, KARYO, 540, 860, 1.0, ease((t - 0.5) / 0.8))
    show(fr, gcard("Sees: chromosome number, balanced translocations", TEALG, 1, 35), 1280, t, D * 0.35)
    show(fr, gcard("Often misses changes of 5–10 Mb or smaller", CORAL, 2, 35), 1430, t, D * 0.6)
    fire("pop", D * 0.35); fire("pop", D * 0.6)

sc_karyo2 = s_cards(3, "When karyotype still matters", None,
    [("Obvious chromosomal syndrome (e.g. Down syndrome)", CYAN), ("Recurrent miscarriage: suspected parental balanced translocation", AMBER),
     ("Family history of chromosomal rearrangement", LAV)], lambda fr, t, D, y: put(fr, karyogram(extra21=True), 540, y + 300, 0.62, ease((t - D * 0.4) / 0.6)))

def sc_cma(fr, t, D):
    dots(fr, 4); show(fr, kicker("Chromosomal microarray (CMA)"), 260, t, 0.1)
    show(fr, headline("Finds small deletions and duplications genome-wide", 54), 320, t, 0.3)
    cma_plot(fr, X0, 480, TW, 420, t, 0.5)
    lay, d = overlay(fr)
    if t > D * 0.35:
        e = ease((t - D * 0.35) / 0.8)
        for i, (lab, v, c, txt) in enumerate((("CMA", 17.5, TEALG, "15–20%"), ("Karyotype", 3, (150, 165, 190), "~3%"))):
            yy = 950 + i * 110; d.text((X0, yy), lab, font=font("Medium", 32), fill=SOFT)
            d.rounded_rectangle((X0 + 230, yy, X0 + 230 + (TW - 330) * v / 20 * e, yy + 46), 23, fill=c)
            d.text((X0 + 240 + (TW - 330) * v / 20 * e, yy + 23), txt, font=font("Bold", 32), fill=WHITE, anchor="lm")
    fr.alpha_composite(lay)
    show(fr, gcard("2010 consensus: first-tier for unexplained DD/ID, autism, multiple anomalies. Misses balanced changes.", CYAN, None, 32), 1200, t, D * 0.55)
    show(fr, source_tag("Miller et al., Am J Hum Genet 2010 (ISCA consensus)"), 1400, t, D * 0.6)

def sc_panel(fr, t, D):
    dots(fr, 5); show(fr, kicker("Gene panel"), 260, t, 0.1)
    show(fr, headline("Selected genes for one disease group", 56), 320, t, 0.3)
    hl = set(range(40, 70)) | set(range(330, 345))
    gene_grid(fr, X0, 480, TW, 420, t, 0.5, hl, title="Panel: only the lit genes are read")
    show(fr, gcard("Good when features clearly point to one disease group", TEALG, 1, 35), 960, t, D * 0.4)
    show(fr, gcard("Epilepsy: a panel of 25+ genes is also a first-tier option", AMBER, 2, 35), 1110, t, D * 0.6)
    fire("pop", D * 0.4); fire("pop", D * 0.6)
    show(fr, source_tag("Epilepsy genetic testing guideline (Smith et al., endorsed by American Epilepsy Society)"), 1270, t, D * 0.7)

def sc_wes(fr, t, D):
    dots(fr, 6); show(fr, kicker("Whole exome sequencing"), 260, t, 0.1)
    show(fr, headline("Coding parts of ~20,000 genes", 56), 320, t, 0.3)
    gene_grid(fr, X0, 430, TW, 330, t, 0.4, None, title="Exome: all genes read")
    lay, d = overlay(fr)
    if t > D * 0.3:
        e = ease((t - D * 0.3) / 0.8)
        d.text((X0, 800), "~36%", font=font("Bold", 120), fill=(*AMBER, int(255 * e)))
        d.text((X0, 950), "yield in neurodevelopmental disorders", font=font("Regular", 34), fill=(*SOFT, int(255 * e)))
    fr.alpha_composite(lay)
    show(fr, gcard("Misses: repeat expansions, mitochondrial DNA, many large CNVs", CORAL, None, 35), 1040, t, D * 0.55)
    show(fr, source_tag("Srivastava et al., Genet Med 2019 (meta-analysis)"), 1190, t, D * 0.6)

sc_special = s_cards(7, "Special tests", "Some diseases need their own test",
    [("Fragile X: PCR (repeat expansion)", CYAN), ("SMA and other deletions: MLPA", AMBER), ("Imprinting disorders: methylation test", LAV)],
    lambda fr, t, D, y: show(fr, callout("The right test starts with the right question", TEALG, 38), y + 40, t, D * 0.7))

def sc_flow(fr, t, D):
    dots(fr, 8); show(fr, kicker("A practical approach"), 260, t, 0.1)
    flow(fr, t, D, [("Obvious chromosomal syndrome?", "Karyotype", CYAN), ("Unexplained DD or multiple anomalies?", "Microarray, or exome first", AMBER),
                    ("Clearly one disease group?", "Panel or specific test", TEALG), ("Unsure?", "Discuss with a geneticist", LAV)], 340)

def sc_trio(fr, t, D):
    dots(fr, 9); show(fr, kicker("Trio testing"), 260, t, 0.1)
    show(fr, headline("Patient + both parents", 58), 320, t, 0.3)
    for i, (title, mut) in enumerate((("Child", (9, "C")), ("Mother", None), ("Father", None))):
        tin = 0.5 + i * D * 0.15
        if t > tin: sanger(fr, X0, 450 + i * 330, TW, 300, t, tin, SEQ, mut, title=title)
    show(fr, callout("Change only in the child = de novo", AMBER, 38), 1470, t, D * 0.65); fire("ding", D * 0.65)

def sc_report(fr, t, D):
    dots(fr, 10); show(fr, kicker("Reading the report"), 260, t, 0.1)
    show(fr, headline("Five categories (ACMG/AMP)", 58), 320, t, 0.3)
    five_tier(fr, 460, t, 0.5)
    show(fr, gcard("No treatment decisions on a VUS; classification can change over time", AMBER, None, 35), 1100, t, D * 0.6)
    show(fr, source_tag("Richards et al., Genet Med 2015"), 1260, t, D * 0.65)

def sc_case1(fr, t, D):
    dots(fr, 11); show(fr, kicker("Case study", CORAL), 260, t, 0.1)
    show(fr, headline("A published case from India", 58), 320, t, 0.3)
    put(fr, PAPER, 540, 880, 0.9, ease((t - 0.5) / 0.6))
    show(fr, gcard("6-month-old boy, normal development so far, with seizures", CYAN, None, 36), 1300, t, D * 0.55)
    show(fr, source_tag("Kadian et al., PGIMS Rohtak; J Family Med Prim Care 2025;14(11):4891-3 (Case 2)"), 1450, t, D * 0.6)

sc_case2 = s_cards(12, "Case: work-up", None,
    [("MRI brain: normal", TEALG), ("EEG: normal", TEALG), ("Metabolic screen: negative", TEALG),
     ("Phenytoin: seizure-free 3 months, then recurred", AMBER), ("Whole exome sequencing to look for a channelopathy", CYAN)])

def sc_case3(fr, t, D):
    dots(fr, 13); show(fr, kicker("Case: the answer"), 260, t, 0.1)
    show(fr, headline("PRRT2 frameshift variant", 60), 320, t, 0.3)
    sanger(fr, X0, 460, TW, 360, t, 0.5, SEQ, (11, "T"), title="Exome finding (illustration)")
    show(fr, gcard("Diagnosis: self-limited infantile epilepsy, often confused with epileptic encephalopathy", CYAN, None, 34), 880, t, D * 0.4)
    show(fr, gcard("With medicines, the child became seizure-free", TEALG, None, 36), 1060, t, D * 0.6)
    fire("ding", D * 0.4)

def sc_case4(fr, t, D):
    dots(fr, 14); show(fr, kicker("What the diagnosis means"), 260, t, 0.1)
    lay, d = overlay(fr); e = ease((t - 0.4) / 0.6)
    d.text((X0, 330), "By ~2 years", font=font("Bold", 110), fill=(*AMBER, int(255 * e)))
    d.text((X0, 470), "seizures usually stop; development normal", font=font("Regular", 38), fill=(*SOFT, int(255 * e)))
    fr.alpha_composite(lay)
    items = [("Reassurance for the family", TEALG), ("Correct prognosis", CYAN), ("Avoids unnecessary tests", AMBER)]
    for i, (txt, c) in enumerate(items):
        fire("pop", D * (0.3 + 0.13 * i)); show(fr, gcard(txt, c, i + 1, 36), 600 + i * 150, t, D * (0.3 + 0.13 * i))
    show(fr, source_tag("GeneReviews: PRRT2-associated paroxysmal disorders"), 1080, t, D * 0.7)

sc_take = s_cards(15, "Key messages", None,
    [("Right question, right test", CYAN), ("Microarray and exome have different roles", AMBER), ("Trio + good clinical details = clearer reports", TEALG),
     ("Every report with genetic counselling", LAV)], lambda fr, t, D, y: helix(fr, 540, y + 260, 360, t, amp=300, turns=1.2, alpha=70, n=30))

SC = [(film(sc0), "doc"), (film(sc_levels), "doc"), (film(sc_karyo), "doc"), (film(sc_karyo2), "doc"), (film(sc_cma), "doc"),
      (film(sc_panel), "doc"), (film(sc_wes), "doc"), (film(sc_special), "doc"), (film(sc_flow), "doc"), (film(sc_trio), "doc"),
      (film(sc_report), "doc"), (film(sc_case1), "doc"), (film(sc_case2), "doc"), (film(sc_case3), "doc"), (film(sc_case4), "doc"),
      (film(sc_take), "doc"), (close_scene("Which cases need genetic tests?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si, (fn, bg) in enumerate(SC):
            d = 16 if si < len(SC) - 1 else 33; NOW.update(t=d * .95, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * .95, d); ims.append(fr.convert("RGB").resize((300, 533)))
        s = Image.new("RGB", (300 * 6, 533 * 3), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 6) * 300, (i // 6) * 533))
        s.save("sheet_g001.png")
    else: run(SC, "/tmp/g001_", "Genetics_Ep01_Which_Test_When_Hindi.mp4", max_sec=480)
