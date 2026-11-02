"""Genetics Clinical Series, Episode 16: Rett syndrome and MECP2 (sales-team field guide, Bengali narration; Hindi teaser via hindi_teaser.py g016 5)."""
import sys
from cbc_cartoon import run
from gen_series import *
from hts_close import close_scene
from g013 import hbars

TOT[0] = 10
TOPIC = "GENETICS SERIES  •  EPISODE 16"
SRC_AI = "Khajuria et al., J Transl Genet Genom 2020;4:91-103 (AIIMS, New Delhi)"
SRC_LK = "Lallar et al., Indian Pediatr 2018;55:474-7 (SGPGI Lucknow, AIIMS)"
SRC_NI = "NICHD: How is Rett syndrome diagnosed?"
SRC_AC = "ACMG: trofinetide approved for Rett syndrome (FDA, March 2023)"

def course(fr, y, t, tin):
    """Development, regression, stabilisation (illustration)."""
    lay, d = overlay(fr); e = ease((t - tin) / 1.4)
    pts = [(0, 0.15), (0.3, 0.55), (0.42, 0.6), (0.58, 0.3), (1.0, 0.35)]
    x0, w, h = X0 + 20, TW - 40, 320
    P = [(x0 + u * w, y + h - v * h) for u, v in pts]
    n = max(2, int(len(P) * e + 0.999)); seg = P[:n]
    if len(seg) > 1: d.line(seg, fill=(*CYAN, 240), width=8, joint="curve")
    a = int(255 * ease((t - tin - 1.0) / 0.6))
    for (u, lab, c) in ((0.15, "Early months", TEALG), (0.5, "Regression", CORAL), (0.82, "Stabilises", AMBER)):
        d.text((x0 + u * w, y + h + 50), lab, font=font("Bold", 32), fill=(*c, a), anchor="mm")
    d.text((540, y + h + 110), "Illustration of the typical pattern", font=font("Medium", 28), fill=(*SOFT, a), anchor="mm")
    fr.alpha_composite(lay)

# ---------------- scenes ----------------
def sc0(fr, t, D):
    show(fr, kicker("Genetics Clinical Series  •  Episode 16", CYAN), 330, t, 0.1)
    show(fr, headline("Rett syndrome", 76), 410, t, -1)
    show(fr, headline("and the MECP2 gene", 52, (249, 196, 120)), 510, t, -1)
    if t > D * 0.3: type_on(fr, "A field guide for the sales team", 610, t, D * 0.3, 40, AMBER)
    course(fr, 760, t, 0.4)
    show(fr, callout("A girl who learned skills, then lost them", CYAN, 34), 1640, t, D * 0.6); fire("whoosh", D * 0.6)

def sc_what(fr, t, D):
    dots(fr, 1); show(fr, kicker("What is it?"), 260, t, 0.1)
    show(fr, headline("About 1 in 10,000 to 23,000 girls", 48), 330, t, 0.3)
    show(fr, gcard("Caused by changes in the MECP2 gene on the X chromosome", CYAN, 1, 32), 460, t, D * 0.2)
    show(fr, gcard("MECP2 is a key regulator of brain development", TEALG, 2, 33), 620, t, D * 0.32)
    show(fr, gcard("A common genetic cause of developmental impairment in girls", AMBER, 3, 32), 770, t, D * 0.44)
    show(fr, gcard("Similar pictures: CDKL5 and FOXG1 (atypical Rett)", LAV, 4, 32), 930, t, D * 0.56)
    show(fr, source_tag(SRC_AC), 1090, t, D * 0.65)
    for k in (0.2, 0.32, 0.44, 0.56): fire("pop", D * k)

sc_signs = s_cards(2, "The 5 signs doctors look for", None,
    [("Development, then regression, then stabilising", CORAL), ("Loss of purposeful hand use", AMBER), ("Loss of spoken language", LAV),
     ("Repeated hand movements: wringing, rubbing, clapping", CYAN), ("Abnormal walking", TEALG)],
    lambda fr, t, D, y: (show(fr, body("Also: slowing head growth between 3 months and 4 years", 31, SOFT), y + 20, t, D * 0.7),
                         show(fr, source_tag(SRC_NI), y + 100, t, D * 0.75)), size=31)

sc_doc = s_cards(3, "Which doctors to visit", None,
    [("Paediatric neurologists", CYAN), ("Developmental paediatricians", TEALG), ("Child development and therapy centres", AMBER),
     ("Paediatric orthopaedics (scoliosis)", LAV)],
    lambda fr, t, D, y: show(fr, body("These girls need lifelong, many-specialty care", 32, SOFT), y + 20, t, D * 0.7), size=33)

def sc_india(fr, t, D):
    dots(fr, 4); show(fr, kicker("Indian data"), 260, t, 0.1)
    show(fr, headline("MECP2 change found", 56), 320, t, 0.3)
    hbars(fr, 440, [("AIIMS, classic", 98.6, "98.6% (72 girls)", TEALG), ("Lucknow, classic", 93, "93% (13 of 14)", CYAN),
                    ("Atypical Rett", 20, "20% (1 of 5)", AMBER), ("Rett-like only", 0, "0 of 17", CORAL)], t, 0.6, 130, 290)
    show(fr, gcard("AIIMS: 1 in 10 found only by MLPA (large deletions)", LAV, None, 32), 880, t, D * 0.45)
    show(fr, gcard("Symptoms at 16 months; diagnosis at 42 months (medians)", AMBER, None, 32), 1040, t, D * 0.58)
    show(fr, source_tag(SRC_AI + "; " + SRC_LK), 1210, t, D * 0.68)
    fire("pop", D * 0.45); fire("pop", D * 0.58)

def sc_why(fr, t, D):
    dots(fr, 5); show(fr, kicker("Why the report matters"), 260, t, 0.1)
    show(fr, gcard("Confirms the diagnosis, together with the clinical signs", TEALG, 1, 32), 340, t, 0.3)
    show(fr, gcard("2023: first medicine approved for Rett (trofinetide, USA, age 2+)", AMBER, 2, 32), 510, t, D * 0.25)
    show(fr, gcard("Guides counselling for parents and relatives", LAV, 3, 32), 680, t, D * 0.4)
    show(fr, gcard("Ends the search for a cause; therapy can be planned", CYAN, 4, 32), 850, t, D * 0.55)
    show(fr, source_tag(SRC_AC + "; " + SRC_AI), 1020, t, D * 0.65)

def sc_test(fr, t, D):
    dots(fr, 6); show(fr, kicker("Which test"), 260, t, 0.1)
    show(fr, gcard("MECP2 sequencing PLUS deletion test (MLPA)", TEALG, 1, 33), 340, t, 0.3)
    show(fr, gcard("Negative or atypical: CDKL5, FOXG1, gene panel or exome with CNV", AMBER, 2, 32), 500, t, D * 0.25)
    show(fr, gcard("A positive test alone does not diagnose; the doctor's assessment does", LAV, 3, 32), 670, t, D * 0.4)
    show(fr, gcard("Not on our standard menu: confirm with the lab first", CORAL, 4, 32), 840, t, D * 0.55)
    show(fr, source_tag(SRC_AI + "; " + SRC_NI), 1010, t, D * 0.65)

sc_flags = s_cards(7, "Which girls especially", None,
    [("Normal early months, then lost skills", CORAL), ("Stopped using her hands on purpose", AMBER), ("Lost words she used to say", LAV),
     ("Constant hand wringing or clapping", CYAN), ("Head growth slowing", TEALG)], size=33)

def sc_talk(fr, t, D):
    dots(fr, 8); show(fr, kicker("How to start the conversation"), 260, t, 0.1)
    for i, (txt, c) in enumerate((("Ask: \"In a girl who lost hand use and speech, do you test MECP2 with MLPA?\"", CYAN),
                                  ("Fact: at AIIMS, a cause was found in 98.6% of classic Rett girls", AMBER),
                                  ("Fact: diagnosis came about 2 years after symptoms", LAV), ("Leave the 2-page PDF", TEALG))):
        fire("pop", D * (0.1 + 0.16 * i)); show(fr, gcard(txt, c, i + 1, 32), 340 + i * 170, t, D * (0.1 + 0.16 * i))

def sc_obj(fr, t, D):
    dots(fr, 9); show(fr, kicker("When the doctor says..."), 260, t, 0.1)
    rows = [("\"The diagnosis is clinical\"", "Yes; the report confirms it, and 1 in 10 at AIIMS needed MLPA to find the change.", TEALG),
            ("\"There is no treatment\"", "A first medicine was approved in the USA in 2023; the report also guides family counselling.", LAV)]
    lay, d = overlay(fr)
    for i, (q, a_, c) in enumerate(rows):
        e = ease((t - D * (0.1 + 0.35 * i)) / 0.5); al = int(255 * e); yy = 340 + i * 300
        d.rounded_rectangle((X0, yy, X0 + TW, yy + 260), 24, fill=(255, 255, 255, int(20 * e)), outline=(*c, al), width=3)
        d.text((X0 + 30, yy + 50), q, font=font("Bold", 34), fill=(*c, al), anchor="lm")
        for j, line in enumerate(wrap(a_, font("Medium", 32), TW - 60)):
            d.text((X0 + 30, yy + 115 + j * 42), line, font=font("Medium", 32), fill=(*SOFT, al), anchor="lm")
    fr.alpha_composite(lay)

def sc_sample(fr, t, D):
    dots(fr, 10); show(fr, kicker("Sample and field rules"), 260, t, 0.1)
    put(fr, tube_sprite((149, 117, 205), "EDTA"), 300, 600, 0.9, ease((t - 0.3) / 0.5))
    show(fr, gcard("EDTA blood", TEALG, 1, 34), 900, t, D * 0.2)
    show(fr, gcard("Counselling and written consent first", LAV, 2, 33), 1040, t, D * 0.32)
    show(fr, gcard("Never promise a cure; medicines are the doctor's decision", CORAL, 3, 32), 1180, t, D * 0.45)
    show(fr, callout("Prenatal: disease testing only; sex never disclosed (PCPNDT)", CORAL, 31), 1360, t, D * 0.6)

sc_take = s_cards(11, "Key messages", None,
    [("Rett: skills gained, then lost, mostly in girls", CYAN), ("India: MECP2 change in over 9 of 10 classic cases", TEALG),
     ("Order sequencing PLUS MLPA", AMBER), ("Paediatric neurologists and therapy centres first", LAV)], size=32)

SC = [(film(sc0), "doc"), (film(sc_what), "doc"), (film(sc_signs), "doc"), (film(sc_doc), "doc"), (film(sc_india), "doc"),
      (film(sc_why), "doc"), (film(sc_test), "doc"), (film(sc_flags), "doc"), (film(sc_talk), "doc"), (film(sc_obj), "doc"),
      (film(sc_sample), "doc"), (film(sc_take), "doc"),
      (close_scene("Who sees these girls most?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si, (fn, bg) in enumerate(SC):
            d = 16 if si < len(SC) - 1 else 33; p = .95 if si else 0.01; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((300, 533)))
        s = Image.new("RGB", (300 * 7, 533 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 7) * 300, (i // 7) * 533))
        s.save("/tmp/sheet_g016.png")
    else: run(SC, "/tmp/g016bn_", "Genetics_Ep16_Rett_MECP2_Bengali.mp4", max_sec=480)
