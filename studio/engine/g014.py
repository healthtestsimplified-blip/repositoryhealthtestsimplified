"""Genetics Clinical Series, Episode 14: Developmental & epileptic encephalopathies (sales-team field guide, Bengali narration; Hindi teaser via hindi_teaser.py g014 5)."""
import sys, random, math
from cbc_cartoon import run
from gen_series import *
from hts_close import close_scene
from g013 import eeg, hbars

TOT[0] = 10
TOPIC = "GENETICS SERIES  •  EPISODE 14"
SRC_IN = "Epilepsy Research 2020;166:106398 (epilepsy centre, Thiruvananthapuram)"

def twin(fr, y, t, tin):
    """Seizures + development, both affected."""
    lay, d = overlay(fr); e = ease((t - tin) / 0.6); a = int(255 * e)
    for i, (lab, c) in enumerate((("Seizures", CORAL), ("Development", AMBER))):
        cx = 360 + i * 360
        d.ellipse((cx - 190, y - 190, cx + 190, y + 190), fill=(*c, int(55 * e)), outline=(*c, a), width=5)
        d.text((cx + (-70 if i == 0 else 70), y), lab, font=font("Bold", 32), fill=(*WHITE, a), anchor="mm")
    d.text((540, y + 250), "DEE: both affected", font=font("Bold", 38), fill=(*TEALG, a), anchor="mm")
    fr.alpha_composite(lay)

# ---------------- scenes ----------------
def sc0(fr, t, D):
    show(fr, kicker("Genetics Clinical Series  •  Episode 14", CYAN), 330, t, 0.1)
    show(fr, headline("Developmental &", 70), 410, t, -1)
    show(fr, headline("epileptic encephalopathy", 60), 500, t, -1)
    if t > D * 0.3: type_on(fr, "A field guide for the sales team", 610, t, D * 0.3, 40, AMBER)
    twin(fr, 950, t, 0.4)
    show(fr, callout("How a genetic report helps choose the medicine", CYAN, 34), 1640, t, D * 0.6); fire("whoosh", D * 0.6)

def sc_what(fr, t, D):
    dots(fr, 1); show(fr, kicker("What is DEE? (ILAE 2022)"), 260, t, 0.1)
    twin(fr, 560, t, 0.3)
    show(fr, gcard("Cause: the underlying condition, the seizures, or both", CYAN, 1, 33), 1000, t, D * 0.35)
    show(fr, gcard("Examples: Dravet, Lennox-Gastaut, early-infantile DEE", AMBER, 2, 33), 1160, t, D * 0.5)
    fire("pop", D * 0.35); fire("pop", D * 0.5)

sc_who = s_cards(2, "Which doctors to visit", None,
    [("Paediatric neurologists", CYAN), ("Epilepsy centres", TEALG), ("Paediatricians", AMBER), ("Child development and therapy centres", LAV)],
    lambda fr, t, D, y: show(fr, body("These children need many medicines and frequent visits", 32, SOFT), y + 20, t, D * 0.6), size=34)

def sc_india(fr, t, D):
    dots(fr, 3); show(fr, kicker("Indian data  •  Kerala"), 260, t, 0.1)
    show(fr, headline("82 children, DEE before age 1", 50), 320, t, 0.3)
    hbars(fr, 470, [("All children", 31.7, "31.7% cause found", TEALG), ("Dravet-like", 36.4, "36.4%", CORAL)], t, 0.6, 50, 300)
    show(fr, gcard("Commonest gene: SCN1A", CYAN, None, 36), 740, t, D * 0.45)
    show(fr, source_tag(SRC_IN), 900, t, D * 0.55)
    fire("pop", D * 0.45)

def sc_prec(fr, t, D):
    dots(fr, 4); show(fr, kicker("How the report changed treatment"), 260, t, 0.1)
    for i, (txt, c) in enumerate((("SCN1A: avoid lamotrigine and carbamazepine", CORAL), ("SCN2A, SCN8A: high-dose sodium channel blockers helped", TEALG),
                                  ("Pyridoxine-dependent epilepsy: vitamin B6; development normalised in 2", AMBER))):
        fire("pop", D * (0.1 + 0.18 * i)); show(fr, gcard(txt, c, i + 1, 32), 340 + i * 170, t, D * (0.1 + 0.18 * i))
    show(fr, callout("18 of 82 children could be offered targeted therapy", LAV, 34), 880, t, D * 0.7)
    show(fr, source_tag(SRC_IN), 1040, t, D * 0.75)

def sc_test(fr, t, D):
    dots(fr, 5); show(fr, kicker("Which test"), 260, t, 0.1)
    show(fr, gcard("First: exome or genome, or an epilepsy panel of more than 25 genes", TEALG, 1, 32), 340, t, 0.3)
    show(fr, gcard("Then: chromosomal microarray", AMBER, 2, 34), 510, t, D * 0.25)
    show(fr, gcard("Kerala authors: sequence when MRI and metabolic tests are normal", LAV, 3, 32), 660, t, D * 0.45)
    show(fr, source_tag("NSGC practice guideline (Smith et al., J Genet Couns 2023); " + SRC_IN), 840, t, D * 0.6)

sc_flags = s_cards(6, "Which children especially", None,
    [("Long seizures with fever in the first year", CORAL), ("Seizures not controlled by medicines", AMBER),
     ("Delayed development or loss of skills", LAV), ("Normal MRI and metabolic tests", CYAN)], size=33)

def sc_talk(fr, t, D):
    dots(fr, 7); show(fr, kicker("How to start the conversation"), 260, t, 0.1)
    for i, (txt, c) in enumerate((("Ask: \"In Dravet-like seizures, do you test SCN1A before choosing medicines?\"", CYAN),
                                  ("Fact: in Kerala, about 1 in 5 children could be offered targeted therapy", AMBER), ("Leave the 2-page PDF", TEALG))):
        fire("pop", D * (0.1 + 0.18 * i)); show(fr, gcard(txt, c, i + 1, 32), 340 + i * 175, t, D * (0.1 + 0.18 * i))

def sc_obj(fr, t, D):
    dots(fr, 8); show(fr, kicker("When the doctor says..."), 260, t, 0.1)
    rows = [("\"The diagnosis is clinical\"", "Yes; the genetic report confirms it and helps choose medicines.", TEALG),
            ("\"Too expensive\"", "One exome or panel can replace many separate tests. Confirm price and report time first.", LAV)]
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
    show(fr, gcard("Never promise seizure control; medicine changes are the doctor's call", CORAL, 3, 31), 1200, t, D * 0.5)
    show(fr, callout("Prenatal: disease testing only; sex never disclosed (PCPNDT)", CORAL, 31), 1380, t, D * 0.65)

sc_take = s_cards(10, "Key messages", None,
    [("DEE: seizures and development both affected", CYAN), ("India: about 1 in 3 had a genetic cause", TEALG),
     ("The report helps choose the medicine", AMBER), ("Paediatric neurologists and epilepsy centres first", LAV)], size=32)

SC = [(film(sc0), "doc"), (film(sc_what), "doc"), (film(sc_who), "doc"), (film(sc_india), "doc"), (film(sc_prec), "doc"),
      (film(sc_test), "doc"), (film(sc_flags), "doc"), (film(sc_talk), "doc"), (film(sc_obj), "doc"),
      (film(sc_sample), "doc"), (film(sc_take), "doc"),
      (close_scene("Who sees Dravet-like seizures?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si, (fn, bg) in enumerate(SC):
            d = 16 if si < len(SC) - 1 else 33; p = .95 if si else 0.01; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((300, 533)))
        s = Image.new("RGB", (300 * 6, 533 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 6) * 300, (i // 6) * 533))
        s.save("/tmp/sheet_g014.png")
    else: run(SC, "/tmp/g014bn_", "Genetics_Ep14_DEE_Bengali.mp4", max_sec=480)
