"""Genetics Clinical Series, Episode 10: Reanalysis and secondary findings (Bengali narration)."""
import sys, random
from cbc_cartoon import run
from gen_series import *
from hts_close import close_scene

TOT[0] = 12
TOPIC = "GENETICS SERIES  •  EPISODE 10"
PAPER = paper_sprite(["Cerebellar ataxia,", "impaired intellectual", "development and", "disequilibrium syndrome-2"], "Cureus, 2025 (Florida, USA)")
ACT = set(random.Random(10).sample(range(600), 84))

def bars(fr, y, rows, t, tin, vmax, labw=300):
    lay, d = overlay(fr); e = ease((t - tin) / 1.2)
    for i, (lab, v, txt, c) in enumerate(rows):
        yy = y + i * 120
        d.text((X0, yy + 30), lab, font=font("Medium", 32), fill=SOFT, anchor="lm")
        L = max(16, (TW - labw - 190) * v / vmax * e)
        d.rounded_rectangle((X0 + labw, yy, X0 + labw + L, yy + 60), 30, fill=c)
        d.text((X0 + labw + 20 + L, yy + 30), txt, font=font("Bold", 32), fill=WHITE, anchor="lm")
    fr.alpha_composite(lay)

def timeline(fr, y, t, tin, steps):
    """Horizontal timeline: same data, analysed again later."""
    lay, d = overlay(fr); e = ease((t - tin) / 0.8); a = int(255 * e)
    d.line((X0 + 130, y, X0 + TW - 130, y), fill=(*SOFT, a), width=5)
    n = len(steps)
    for i, (lab, sub, c) in enumerate(steps):
        ei = ease((t - tin - 0.5 * i) / 0.5); ai = int(255 * ei)
        x = X0 + 130 + i * (TW - 260) / (n - 1)
        d.ellipse((x - 22, y - 22, x + 22, y + 22), fill=(*c, ai))
        d.text((x, y - 60), lab, font=font("Bold", 30), fill=(*c, ai), anchor="mm")
        for j, line in enumerate(wrap(sub, font("Medium", 26), 250)):
            d.text((x, y + 60 + j * 34), line, font=font("Medium", 26), fill=(*SOFT, ai), anchor="mm")
    fr.alpha_composite(lay)

def donut(fr, cx, cy, r, t, tin, parts):
    lay, d = overlay(fr); e = ease((t - tin) / 1.2); start = -90
    for lab, v, c in parts:
        sweep = 360 * v / 100 * e
        d.pieslice((cx - r, cy - r, cx + r, cy + r), start, start + sweep, fill=(*c, 235)); start += sweep
    d.ellipse((cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55), fill=(11, 27, 51, 255))
    d.text((cx, cy), "31 new", font=font("Bold", 34), fill=WHITE, anchor="mm")
    fr.alpha_composite(lay)

# ---------------- scenes ----------------
def sc0(fr, t, D):
    show(fr, kicker("Genetics Clinical Series  •  Episode 10", CYAN), 330, t, 0.1)
    show(fr, headline("Reanalysis and", 70), 410, t, -1)
    show(fr, headline("secondary findings", 70), 500, t, -1)
    if t > D * 0.3: type_on(fr, "A negative exome is not the last word", 620, t, D * 0.3, 40, AMBER)
    timeline(fr, 960, t, 0.5, [("Year 0", "Exome: negative", (120, 140, 170)), ("New genes", "Knowledge grows", AMBER), ("Reanalysis", "Same data, new look", TEALG)])
    show(fr, callout("For doctors and healthcare teams  •  with a published case", CYAN, 34), 1640, t, D * 0.6); fire("whoosh", D * 0.6)

def sc_what(fr, t, D):
    dots(fr, 1); show(fr, kicker("What is reanalysis?"), 260, t, 0.1)
    show(fr, headline("Same data, today's knowledge", 54), 320, t, 0.3)
    timeline(fr, 600, t, 0.6, [("First report", "Negative or VUS", (120, 140, 170)), ("Each year", "New genes, updated databases", AMBER), ("Reanalysis", "No new sample needed", TEALG)])
    show(fr, gcard("Not a new sample or new sequencing", CYAN, 1, 34), 900, t, D * 0.45)
    show(fr, gcard("Gene-disease knowledge grows every year", AMBER, 2, 34), 1050, t, D * 0.6)
    fire("pop", D * 0.45); fire("pop", D * 0.6)

def sc_why(fr, t, D):
    dots(fr, 2); show(fr, kicker("Where new diagnoses come from"), 260, t, 0.1)
    donut(fr, 540, 640, 270, t, 0.3, [("new", 42, TEALG), ("reseq", 29, CYAN), ("pipe", 19, AMBER), ("follow", 10, LAV)])
    for i, (txt, c) in enumerate((("New or broader gene-disease links: 42%", TEALG), ("Resequencing: 29%", CYAN),
                                  ("Better analysis pipelines: 19%", AMBER), ("Family testing or functional studies: 10%", LAV))):
        show(fr, gcard(txt, c, None, 32), 970 + i * 140, t, D * (0.25 + 0.1 * i))
    show(fr, source_tag("Schobers et al., Genome Med 2022;14:66 (Radboud, 31 new diagnoses)"), 1540, t, D * 0.65)

def sc_evid(fr, t, D):
    dots(fr, 3); show(fr, kicker("The evidence"), 260, t, 0.1)
    show(fr, headline("150 children, about 5 years", 52), 320, t, 0.3)
    bars(fr, 450, [("First analysis", 31, "31%", (120, 140, 170)), ("After reanalysis", 53, "53%", TEALG)], t, 0.6, 60, 320)
    show(fr, source_tag("Schobers et al., Genome Med 2022"), 700, t, D * 0.3)
    show(fr, headline("Europe: 6,004 families", 52), 800, t, D * 0.4)
    show(fr, gcard("New diagnosis in 12.6% of families (8.4% systematic + 4.1% expert review)", AMBER, None, 31), 930, t, D * 0.5)
    show(fr, source_tag("Laurie et al., Nat Med 2025 (Solve-RD)"), 1100, t, D * 0.55)

sc_when = s_cards(4, "When to ask for reanalysis", None,
    [("New symptoms or signs", CYAN), ("Another family member affected", CORAL),
     ("VUS in the report: re-evaluate it first", AMBER), ("Time has passed (Radboud authors: about yearly)", TEALG)], size=33)

sc_prac = s_cards(5, "Making reanalysis work", None,
    [("Send the lab updated clinical details", CYAN), ("Ask the lab's reanalysis policy and cost", AMBER),
     ("Keep the old report and data safely", TEALG)], size=34)

def sc_sf(fr, t, D):
    dots(fr, 6); show(fr, kicker("Secondary findings"), 260, t, 0.1)
    show(fr, headline("Important results outside the test question", 50), 320, t, 0.3)
    gene_grid(fr, X0, 480, TW, 420, t, 0.6, highlight=ACT, title="Actionable genes looked at (illustration)")
    for i, (txt, c) in enumerate((("Hereditary cancer risk", CORAL), ("Some heart conditions", CYAN), ("Familial hypercholesterolaemia", AMBER))):
        fire("pop", D * (0.4 + 0.1 * i)); show(fr, gcard(txt, c, i + 1, 34), 960 + i * 140, t, D * (0.4 + 0.1 * i))

def sc_list(fr, t, D):
    dots(fr, 7); show(fr, kicker("ACMG SF v3.3 (2025)"), 260, t, 0.1)
    lay, d = overlay(fr); e = ease((t - 0.3) / 0.8)
    d.text((540, 520), str(int(84 * e)), font=font("Bold", 220), fill=(*TEALG, int(255 * e)), anchor="mm")
    d.text((540, 680), "medically actionable genes", font=font("Medium", 40), fill=(*SOFT, int(255 * e)), anchor="mm")
    fr.alpha_composite(lay)
    show(fr, gcard("Added in 2025: ABCD1, CYP27A1, PLN", AMBER, None, 34), 800, t, D * 0.45)
    show(fr, source_tag("ACMG SF v3.3, Genet Med 2025 (doi:10.1016/j.gim.2025.101454)"), 960, t, D * 0.55)

sc_consent = s_cards(8, "Consent comes first", None,
    [("Before the test: does the patient want secondary findings?", CYAN), ("Children: discuss carefully in counselling", AMBER),
     ("Results can matter for the whole family", LAV)], size=33)

def sc_case1(fr, t, D):
    dots(fr, 9); show(fr, kicker("Published case", CORAL), 260, t, 0.1)
    put(fr, PAPER, 540, 610, 0.56, ease((t - 0.4) / 0.6))
    for i, (txt, c) in enumerate((("Girl: cerebellar ataxia diagnosed at 18 months", CYAN), ("MRI: cerebellar atrophy", AMBER),
                                  ("Trio exome, mtDNA, CMA, ataxia panel, SMA: all negative", (120, 140, 170)))):
        show(fr, gcard(txt, c, None, 31), 870 + i * 150, t, D * (0.25 + 0.12 * i))
    show(fr, source_tag("Hochman, Drummond & Morgan, Cureus 2025;17(1):e78066, CC BY"), 1340, t, D * 0.65)

def sc_case2(fr, t, D):
    dots(fr, 10); show(fr, kicker("Case: reanalysis at age 5"), 260, t, 0.1)
    timeline(fr, 470, t, 0.3, [("Early", "Trio exome negative", (120, 140, 170)), ("Age 5", "Re-referred to genetics", AMBER), ("Reanalysis", "Same trio data", TEALG)])
    show(fr, gcard("WDR81: change in both copies; both parents carriers", CORAL, 1, 32), 760, t, D * 0.45)
    show(fr, callout("Diagnosis: CAMRQ2 (cerebellar ataxia, intellectual disability, disequilibrium syndrome 2)", TEALG, 31), 930, t, D * 0.6)
    fire("ding", D * 0.6)

def sc_case3(fr, t, D):
    dots(fr, 11); show(fr, kicker("Case: what it meant"), 260, t, 0.1)
    show(fr, headline("No new sample. Just a new look at old data.", 50), 320, t, 0.3)
    for i, (txt, c) in enumerate((("Physiotherapy and occupational therapy", CYAN), ("Walks; keeps up at school with tutoring", TEALG),
                                  ("Authors: re-evaluate genetic data periodically", AMBER))):
        fire("pop", D * (0.3 + 0.13 * i)); show(fr, gcard(txt, c, i + 1, 33), 520 + i * 150, t, D * (0.3 + 0.13 * i))

sc_take = s_cards(12, "Key messages", None,
    [("A negative exome is not the last word", CYAN), ("Reanalysis can diagnose without a new sample", TEALG),
     ("Ask for it with new symptoms or after time passes", AMBER), ("Secondary findings: 84 actionable genes (ACMG v3.3)", LAV),
     ("Everything with consent and counselling", CORAL)], size=31)

SC = [(film(sc0), "doc"), (film(sc_what), "doc"), (film(sc_why), "doc"), (film(sc_evid), "doc"), (film(sc_when), "doc"),
      (film(sc_prac), "doc"), (film(sc_sf), "doc"), (film(sc_list), "doc"), (film(sc_consent), "doc"),
      (film(sc_case1), "doc"), (film(sc_case2), "doc"), (film(sc_case3), "doc"), (film(sc_take), "doc"),
      (close_scene("Ever requested a reanalysis?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si, (fn, bg) in enumerate(SC):
            d = 16 if si < len(SC) - 1 else 33; p = .95 if si else 0.01; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((300, 533)))
        s = Image.new("RGB", (300 * 5, 533 * 3), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 300, (i // 5) * 533))
        s.save("/tmp/sheet_g010.png")
    elif len(sys.argv) > 1 and sys.argv[1] == "teaser":
        import doc_style
        run([(close_scene("Ever requested a reanalysis?", "WATCH THE FULL VIDEO ON OUR CHANNEL"), "docl")], "/tmp/tzbn_g010_", "/tmp/tzbn_g010.mp4", max_sec=180, cover_skip=0)
    else: run(SC, "/tmp/g010bn_", "Genetics_Ep10_Reanalysis_Secondary_Findings_Bengali.mp4", max_sec=480)
