"""Genetics Clinical Series, Episode 11: Developmental delay & intellectual disability, a field guide for the sales team (Bengali narration)."""
import sys, random
from cbc_cartoon import run
from gen_series import *
from hts_close import close_scene

TOT[0] = 11
TOPIC = "GENETICS SERIES  •  EPISODE 11"
PAPER = paper_sprite(["The etiological profile", "of global developmental", "delay at a tertiary", "care hospital in India"], "Cureus, 2023 (Aurangabad)")

def bars(fr, y, rows, t, tin, vmax, labw=330):
    lay, d = overlay(fr); e = ease((t - tin) / 1.2)
    for i, (lab, v, txt, c) in enumerate(rows):
        yy = y + i * 110
        d.text((X0, yy + 28), lab, font=font("Medium", 30), fill=SOFT, anchor="lm")
        L = max(16, (TW - labw - 170) * v / vmax * e)
        d.rounded_rectangle((X0 + labw, yy, X0 + labw + L, yy + 56), 28, fill=c)
        d.text((X0 + labw + 18 + L, yy + 28), txt, font=font("Bold", 30), fill=WHITE, anchor="lm")
    fr.alpha_composite(lay)

def milestones(fr, y, t, tin):
    """Milestone track: expected vs delayed (illustration)."""
    lay, d = overlay(fr); e = ease((t - tin) / 1.0); a = int(255 * e)
    steps = ["Sits", "Walks", "First words", "Sentences"]
    x0, x1 = X0 + 40, X0 + TW - 40
    for row, (lab, shift, c) in enumerate((("Expected", 0.0, TEALG), ("Delayed", 0.16, AMBER))):
        yy = y + row * 150
        d.text((X0, yy - 50), lab, font=font("Bold", 28), fill=(*c, a), anchor="lm")
        d.line((x0, yy, x1, yy), fill=(255, 255, 255, int(70 * e)), width=4)
        for i, s in enumerate(steps):
            x = x0 + (0.08 + 0.22 * i + shift * (i + 1) * 0.5) * (x1 - x0)
            x = min(x, x1 - 10)
            d.ellipse((x - 16, yy - 16, x + 16, yy + 16), fill=(*c, a))
            d.text((x, yy + 44), s, font=font("Medium", 24), fill=(*SOFT, a), anchor="mm")
    fr.alpha_composite(lay)

def ladder(fr, y, t, tin):
    """Testing pathway as steps."""
    lay, d = overlay(fr)
    steps = [("Step 1", "Chromosomal microarray + Fragile X", CYAN), ("Step 2", "Exome (trio if possible)", TEALG),
             ("If features suggest", "Karyotype (e.g. Down syndrome) or metabolic tests", AMBER)]
    for i, (lab, txt, c) in enumerate(steps):
        e = ease((t - tin - i * 0.8) / 0.5); a = int(255 * e); yy = y + i * 170
        d.rounded_rectangle((X0 + i * 40, yy, X0 + TW, yy + 130), 24, fill=(*c, int(40 * e)), outline=(*c, a), width=3)
        d.text((X0 + i * 40 + 30, yy + 38), lab, font=font("Bold", 28), fill=(*c, a), anchor="lm")
        d.text((X0 + i * 40 + 30, yy + 90), txt, font=font("Medium", 30), fill=(*SOFT, a), anchor="lm")
    fr.alpha_composite(lay)

# ---------------- scenes ----------------
def sc0(fr, t, D):
    show(fr, kicker("Genetics Clinical Series  •  Episode 11", CYAN), 330, t, 0.1)
    show(fr, headline("Developmental delay &", 64), 410, t, -1)
    show(fr, headline("intellectual disability", 64), 495, t, -1)
    if t > D * 0.3: type_on(fr, "A field guide for the sales team", 610, t, D * 0.3, 40, AMBER)
    milestones(fr, 860, t, 0.5)
    show(fr, callout("Which doctors, which tests, in what order, what to say", CYAN, 34), 1640, t, D * 0.6); fire("whoosh", D * 0.6)

def sc_what(fr, t, D):
    dots(fr, 1); show(fr, kicker("What it means"), 260, t, 0.1)
    show(fr, headline("Milestones later than expected", 54), 320, t, 0.3)
    milestones(fr, 560, t, 0.6)
    show(fr, gcard("After about age 5, often called intellectual disability", LAV, 1, 33), 900, t, D * 0.4)
    show(fr, gcard("Parents ask: why, and will the next child have it?", AMBER, 2, 33), 1050, t, D * 0.55)
    fire("pop", D * 0.4); fire("pop", D * 0.55)

sc_who = s_cards(2, "Which doctors to visit", None,
    [("Paediatricians", CYAN), ("Paediatric neurologists", TEALG), ("Developmental paediatricians", LAV),
     ("Neonatologists (NICU follow-up)", AMBER), ("Child psychiatrists (autism)", CORAL),
     ("Physio, occupational and speech therapy centres", CYAN)], size=33)

sc_why = s_cards(3, "Why doctors look for a cause", None,
    [("Prognosis: what to expect", CYAN), ("Recurrence risk for the next child", AMBER),
     ("Some conditions need specific treatment or monitoring", TEALG), ("Ends years of tests and doctor-hopping", LAV)], size=33)

def sc_india(fr, t, D):
    dots(fr, 4); show(fr, kicker("Indian data"), 260, t, 0.1)
    show(fr, headline("52 children with global developmental delay", 48), 320, t, 0.3)
    bars(fr, 470, [("Genetic", 32.7, "32.7%", TEALG), ("Birth asphyxia (HIE)", 26.9, "26.9%", AMBER),
                   ("Chromosomal", 7.7, "7.7%", CYAN), ("Unknown", 11.6, "11.6%", (120, 140, 170))], t, 0.6, 40)
    show(fr, gcard("Half had a cause before birth (prenatal)", LAV, None, 33), 940, t, D * 0.5)
    put(fr, PAPER, 540, 1330, 0.42, ease((t - D * 0.55) / 0.6))
    show(fr, source_tag("Sharma et al., Cureus 2023;15(6):e41066 (MGM Aurangabad), CC BY"), 1560, t, D * 0.6)

def sc_path(fr, t, D):
    dots(fr, 5); show(fr, kicker("Testing order (guidelines)"), 260, t, 0.1)
    show(fr, headline("No clear cause? Start here", 54), 320, t, 0.3)
    ladder(fr, 460, t, 0.6)
    show(fr, source_tag("AAP 2014; ACMG 2021 (exome/genome first- or second-tier); CHOP clinical pathway"), 1010, t, D * 0.6)

def sc_yield(fr, t, D):
    dots(fr, 6); show(fr, kicker("How often is a cause found?"), 260, t, 0.1)
    bars(fr, 360, [("Microarray", 20, "15-20%", CYAN), ("Exome", 31, "about 31%", TEALG), ("Exome + other features", 53, "up to 53%", LAV)], t, 0.3, 60, 380)
    show(fr, source_tag("CHOP DD/ID clinical pathway"), 710, t, D * 0.3)
    show(fr, headline("India", 50), 800, t, D * 0.4)
    show(fr, gcard("Microarray: 20.9% (Lucknow, 86 children with ID)", CYAN, 1, 32), 880, t, D * 0.45)
    show(fr, gcard("Clinical exome: 41% (Kerala, 78 children)", TEALG, 2, 32), 1030, t, D * 0.55)
    fire("pop", D * 0.45); fire("pop", D * 0.55)

def sc_talk(fr, t, D):
    dots(fr, 7); show(fr, kicker("How to start the conversation"), 260, t, 0.1)
    for i, (txt, c) in enumerate((("Ask: \"For a child with unexplained delay, what do you send first?\"", CYAN),
                                  ("Give one fact, with its source", AMBER), ("Show 30 seconds of Episode 6 or 8", TEALG),
                                  ("Leave the 2-page case PDF", LAV))):
        fire("pop", D * (0.1 + 0.15 * i)); show(fr, gcard(txt, c, i + 1, 32), 340 + i * 160, t, D * (0.1 + 0.15 * i))

def sc_obj(fr, t, D):
    dots(fr, 8); show(fr, kicker("When the doctor says..."), 260, t, 0.1)
    rows = [("\"Too costly\"", "Step-wise: microarray first, exome only if needed", AMBER),
            ("\"Therapy goes on anyway\"", "A cause changes recurrence risk, and sometimes treatment", TEALG),
            ("\"Parents aren't ready\"", "We support counselling", LAV)]
    lay, d = overlay(fr)
    for i, (q, a_, c) in enumerate(rows):
        e = ease((t - D * (0.1 + 0.25 * i)) / 0.5); al = int(255 * e); yy = 340 + i * 270
        d.rounded_rectangle((X0, yy, X0 + TW, yy + 230), 24, fill=(255, 255, 255, int(20 * e)), outline=(*c, al), width=3)
        d.text((X0 + 30, yy + 50), q, font=font("Bold", 34), fill=(*c, al), anchor="lm")
        for j, line in enumerate(wrap(a_, font("Medium", 32), TW - 60)):
            d.text((X0 + 30, yy + 115 + j * 42), line, font=font("Medium", 32), fill=(*SOFT, al), anchor="lm")
    fr.alpha_composite(lay)

def sc_sample(fr, t, D):
    dots(fr, 9); show(fr, kicker("Sample and consent"), 260, t, 0.1)
    put(fr, tube_sprite((149, 117, 205), "EDTA"), 300, 640, 1.0, ease((t - 0.3) / 0.5))
    lay, d = overlay(fr); e = ease((t - 0.5) / 0.5)
    d.text((300, 950), "Blood (EDTA)", font=font("Bold", 34), fill=(*SOFT, int(255 * e)), anchor="mm"); fr.alpha_composite(lay)
    show(fr, gcard("Trio: parents' samples too", TEALG, 1, 33), 1010, t, D * 0.25)
    show(fr, gcard("Counselling and written consent first", LAV, 2, 33), 1160, t, D * 0.4)
    show(fr, callout("Prenatal: disease testing only; sex never disclosed (PCPNDT)", CORAL, 32), 1320, t, D * 0.55)
    fire("pop", D * 0.25); fire("pop", D * 0.4)

sc_rules = s_cards(10, "Field rules", None,
    [("Never promise a diagnosis", CORAL), ("Quote facts only with their source", AMBER),
     ("Treatment decisions are always the doctor's", TEALG), ("Confirm price and report time before quoting", CYAN)], size=34)

sc_take = s_cards(11, "Key messages", None,
    [("Delay cases come daily to paediatric and therapy clinics", CYAN), ("Step 1: microarray + Fragile X", TEALG),
     ("Step 2: exome, ideally trio", LAV), ("India: about 1 in 3 had a genetic cause", AMBER),
     ("Go with a question, a fact and a case study", CORAL)], size=31)

SC = [(film(sc0), "doc"), (film(sc_what), "doc"), (film(sc_who), "doc"), (film(sc_why), "doc"), (film(sc_india), "doc"),
      (film(sc_path), "doc"), (film(sc_yield), "doc"), (film(sc_talk), "doc"), (film(sc_obj), "doc"),
      (film(sc_sample), "doc"), (film(sc_rules), "doc"), (film(sc_take), "doc"),
      (close_scene("Which doctor sees delay cases?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si, (fn, bg) in enumerate(SC):
            d = 16 if si < len(SC) - 1 else 33; p = .95 if si else 0.01; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((300, 533)))
        s = Image.new("RGB", (300 * 5, 533 * 3), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 300, (i // 5) * 533))
        s.save("/tmp/sheet_g011.png")
    elif len(sys.argv) > 1 and sys.argv[1] == "teaser":
        import doc_style
        run([(close_scene("Which doctor sees delay cases?", "WATCH THE FULL VIDEO ON OUR CHANNEL"), "docl")], "/tmp/tzbn_g011_", "/tmp/tzbn_g011.mp4", max_sec=180, cover_skip=0)
    else: run(SC, "/tmp/g011bn_", "Genetics_Ep11_Developmental_Delay_Sales_Guide_Bengali.mp4", max_sec=480)
