"""Genetics Clinical Series, Episode 13: Epilepsy in infancy (sales-team field guide, Bengali narration; Hindi teaser via hindi_teaser.py g013 5)."""
import sys, random, math
from cbc_cartoon import run
from gen_series import *
from hts_close import close_scene

TOT[0] = 10
TOPIC = "GENETICS SERIES  •  EPISODE 13"
PAPER = paper_sprite(["Landscape of genetic", "infantile epileptic", "spasms syndrome:", "124 children from India"], "Epilepsia Open, 2023 (6 centres)")

def eeg(fr, y, t, tin, burst=True):
    """EEG-like trace: calm, then a burst (illustration)."""
    panel(fr, X0, y, TW, 300, "EEG (illustration)")
    lay, d = overlay(fr); p = ease((t - tin) / 1.6); r = random.Random(5)
    pts = []; n = 220
    for i in range(int(n * p)):
        u = i / n; x = X0 + 30 + u * (TW - 60)
        amp = 70 if (burst and 0.45 < u < 0.7) else 14
        pts.append((x, y + 180 + math.sin(i * 0.9) * amp * 0.5 + r.gauss(0, amp * 0.35)))
    if len(pts) > 1: d.line(pts, fill=(*CYAN, 230), width=3)
    fr.alpha_composite(lay)

def hbars(fr, y, rows, t, tin, vmax, labw=330):
    lay, d = overlay(fr); e = ease((t - tin) / 1.2)
    for i, (lab, v, txt, c) in enumerate(rows):
        yy = y + i * 100
        d.text((X0, yy + 26), lab, font=font("Medium", 30), fill=SOFT, anchor="lm")
        L = max(16, (TW - labw - 120) * v / vmax * e)
        d.rounded_rectangle((X0 + labw, yy, X0 + labw + L, yy + 52), 26, fill=c)
        d.text((X0 + labw + 16 + L, yy + 26), txt, font=font("Bold", 30), fill=WHITE, anchor="lm")
    fr.alpha_composite(lay)

# ---------------- scenes ----------------
def sc0(fr, t, D):
    show(fr, kicker("Genetics Clinical Series  •  Episode 13", CYAN), 330, t, 0.1)
    show(fr, headline("Epilepsy in infancy", 70), 410, t, -1)
    show(fr, headline("seizures before age 1", 50, (249, 196, 120)), 510, t, -1)
    if t > D * 0.3: type_on(fr, "A field guide for the sales team", 610, t, D * 0.3, 40, AMBER)
    eeg(fr, 800, t, 0.4)
    show(fr, callout("Which doctors, why test, which test, what to say", CYAN, 34), 1640, t, D * 0.6); fire("whoosh", D * 0.6)

def sc_what(fr, t, D):
    dots(fr, 1); show(fr, kicker("What we mean"), 260, t, 0.1)
    eeg(fr, 330, t, 0.3)
    show(fr, gcard("Infantile spasms: a common epilepsy starting before age 1", CYAN, 1, 33), 700, t, D * 0.3)
    show(fr, gcard("Developmental & epileptic encephalopathy: seizures plus delayed development", AMBER, 2, 32), 860, t, D * 0.45)
    show(fr, gcard("Many have a genetic cause", TEALG, 3, 34), 1050, t, D * 0.6)
    fire("pop", D * 0.3); fire("pop", D * 0.45); fire("pop", D * 0.6)

sc_who = s_cards(2, "Which doctors to visit", None,
    [("Paediatric neurologists", CYAN), ("Paediatricians", TEALG), ("Neonatologists (seizures in NICU)", AMBER), ("Epilepsy centres", LAV)], size=34)

def sc_why(fr, t, D):
    dots(fr, 3); show(fr, kicker("Why a cause matters"), 260, t, 0.1)
    show(fr, gcard("ALDH7A1 (pyridoxine-dependent epilepsy): treated with vitamin B6", TEALG, 1, 32), 340, t, 0.3)
    show(fr, gcard("SCN1A: some seizure medicines can make seizures worse", CORAL, 2, 32), 510, t, D * 0.3)
    show(fr, gcard("Recurrence risk for the next child", AMBER, 3, 34), 680, t, D * 0.5)
    show(fr, source_tag("GeneReviews: pyridoxine-dependent epilepsy; SCN1A seizure disorders"), 840, t, D * 0.6)
    fire("pop", D * 0.3); fire("pop", D * 0.5)

def sc_india(fr, t, D):
    dots(fr, 4); show(fr, kicker("Indian data  •  6 centres"), 260, t, 0.1)
    show(fr, headline("124 children with genetic infantile spasms", 46), 320, t, 0.3)
    hbars(fr, 510, [("Trisomy 21", 14, "14", CYAN), ("ALDH7A1", 10, "10 (vitamin B6)", TEALG), ("SCN2A", 7, "7", LAV),
                    ("CDKL5", 6, "6", AMBER), ("ALG13", 5, "5", CORAL)], t, 0.6, 18, 280)
    show(fr, gcard("Spasms began at 5 months; genetic diagnosis at 12 months (medians)", AMBER, None, 31), 1040, t, D * 0.5)
    put(fr, PAPER, 540, 1420, 0.4, ease((t - D * 0.55) / 0.6))
    show(fr, source_tag("Nagarajan et al., Epilepsia Open 2023;8(4):1383-1404"), 1630, t, D * 0.6)

def sc_test(fr, t, D):
    dots(fr, 5); show(fr, kicker("Which test (guideline)"), 260, t, 0.1)
    show(fr, gcard("Genetic testing for every unexplained epilepsy, any age", CYAN, 1, 33), 340, t, 0.3)
    show(fr, gcard("First: exome or genome, or an epilepsy panel of more than 25 genes", TEALG, 2, 32), 500, t, D * 0.25)
    show(fr, gcard("Then: chromosomal microarray", AMBER, 3, 34), 670, t, D * 0.4)
    show(fr, gcard("Exome or genome preferred over a panel", LAV, 4, 34), 820, t, D * 0.55)
    show(fr, source_tag("Smith et al., NSGC evidence-based practice guideline, J Genet Couns 2023"), 980, t, D * 0.65)

sc_flags = s_cards(6, "Which children especially", None,
    [("Seizures starting before age 1", CORAL), ("Delayed development", AMBER), ("Seizures not controlled by medicines", LAV),
     ("MRI and metabolic tests found no cause", CYAN), ("Similar illness in the family", TEALG)], size=33)

def sc_talk(fr, t, D):
    dots(fr, 7); show(fr, kicker("How to start the conversation"), 260, t, 0.1)
    for i, (txt, c) in enumerate((("Ask: \"Do you test infants whose seizures have no clear cause?\"", CYAN),
                                  ("Fact: in the Indian study, the 2nd commonest cause is treatable with vitamin B6", AMBER), ("Leave the 2-page PDF", TEALG))):
        fire("pop", D * (0.1 + 0.18 * i)); show(fr, gcard(txt, c, i + 1, 32), 340 + i * 175, t, D * (0.1 + 0.18 * i))

def sc_obj(fr, t, D):
    dots(fr, 8); show(fr, kicker("When the doctor says..."), 260, t, 0.1)
    rows = [("\"MRI and EEG are done\"", "They show where; a genetic test looks for why.", TEALG),
            ("\"Reports take time\"", "Treatment continues; the test runs alongside. Confirm report time with the lab.", LAV)]
    lay, d = overlay(fr)
    for i, (q, a_, c) in enumerate(rows):
        e = ease((t - D * (0.1 + 0.35 * i)) / 0.5); al = int(255 * e); yy = 340 + i * 300
        d.rounded_rectangle((X0, yy, X0 + TW, yy + 260), 24, fill=(255, 255, 255, int(20 * e)), outline=(*c, al), width=3)
        d.text((X0 + 30, yy + 50), q, font=font("Bold", 34), fill=(*c, al), anchor="lm")
        for j, line in enumerate(wrap(a_, font("Medium", 32), TW - 60)):
            d.text((X0 + 30, yy + 115 + j * 42), line, font=font("Medium", 32), fill=(*SOFT, al), anchor="lm")
    fr.alpha_composite(lay)

def sc_sample(fr, t, D):
    dots(fr, 9); show(fr, kicker("Sample and field rules"), 260, t, 0.1)
    put(fr, tube_sprite((149, 117, 205), "EDTA"), 300, 600, 0.9, ease((t - 0.3) / 0.5))
    show(fr, gcard("EDTA blood; parents too for trio", TEALG, 1, 33), 900, t, D * 0.2)
    show(fr, gcard("Counselling and written consent first", LAV, 2, 33), 1050, t, D * 0.35)
    show(fr, gcard("Never say the test will stop the seizures", CORAL, 3, 33), 1200, t, D * 0.5)
    show(fr, callout("Prenatal: disease testing only; sex never disclosed (PCPNDT)", CORAL, 31), 1360, t, D * 0.65)

sc_take = s_cards(10, "Key messages", None,
    [("Seizures before age 1 are often genetic", CYAN), ("Some causes are treatable; some change the medicine", TEALG),
     ("Guideline: exome, genome or a large epilepsy panel first", AMBER), ("Paediatric neurologists are our key doctors", LAV)], size=32)

SC = [(film(sc0), "doc"), (film(sc_what), "doc"), (film(sc_who), "doc"), (film(sc_why), "doc"), (film(sc_india), "doc"),
      (film(sc_test), "doc"), (film(sc_flags), "doc"), (film(sc_talk), "doc"), (film(sc_obj), "doc"),
      (film(sc_sample), "doc"), (film(sc_take), "doc"),
      (close_scene("Who sees infant seizures most?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si, (fn, bg) in enumerate(SC):
            d = 16 if si < len(SC) - 1 else 33; p = .95 if si else 0.01; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((300, 533)))
        s = Image.new("RGB", (300 * 6, 533 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 6) * 300, (i // 6) * 533))
        s.save("/tmp/sheet_g013.png")
    else: run(SC, "/tmp/g013bn_", "Genetics_Ep13_Epilepsy_In_Infancy_Bengali.mp4", max_sec=480)
