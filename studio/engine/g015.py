"""Genetics Clinical Series, Episode 15: Fragile X syndrome (sales-team field guide, Bengali narration; Hindi teaser via hindi_teaser.py g015 5)."""
import sys, random, math
from cbc_cartoon import run
from gen_series import *
from hts_close import close_scene
from g013 import hbars

TOT[0] = 10
TOPIC = "GENETICS SERIES  •  EPISODE 15"
SRC_UW = "UW Lab Medicine test guide: FMR1-related disorders"
SRC_KOL = "Bhowmik et al., J Clin Diagn Res 2009;3:1266-73 (Kolkata)"

def ladder(fr, y, t, tin, hi=3):
    """FMR1 CGG repeat categories as a rising ladder."""
    rows = [("Normal", "up to 44", TEALG, 0.22), ("Intermediate", "45-54", CYAN, 0.36),
            ("Premutation", "55-200", AMBER, 0.62), ("Full mutation", "over 200", CORAL, 1.0)]
    lay, d = overlay(fr)
    for i, (lab, rng, c, w) in enumerate(rows):
        e = ease((t - tin - i * 0.35) / 0.6); a = int(255 * e); yy = y + i * 110
        L = max(20, (TW - 520) * w * e)
        d.text((X0, yy + 30), lab, font=font("Bold", 32), fill=(*WHITE, a), anchor="lm")
        d.rounded_rectangle((X0 + 300, yy, X0 + 300 + L, yy + 60), 30, fill=(*c, int(230 * e)))
        d.text((X0 + 316 + L, yy + 30), rng, font=font("Bold", 30), fill=(*c, a), anchor="lm")
    e = ease((t - tin - 1.6) / 0.6)
    d.text((540, y + 470), "Number of CGG repeats in the FMR1 gene", font=font("Medium", 30), fill=(*SOFT, int(255 * e)), anchor="mm")
    fr.alpha_composite(lay)

# ---------------- scenes ----------------
def sc0(fr, t, D):
    show(fr, kicker("Genetics Clinical Series  •  Episode 15", CYAN), 330, t, 0.1)
    show(fr, headline("Fragile X syndrome", 76), 410, t, -1)
    show(fr, headline("one gene, three families of conditions", 44, (249, 196, 120)), 510, t, -1)
    if t > D * 0.3: type_on(fr, "A field guide for the sales team", 610, t, D * 0.3, 40, AMBER)
    ladder(fr, 760, t, 0.4)
    show(fr, callout("A test that exome can miss: order it by name", CYAN, 34), 1640, t, D * 0.6); fire("whoosh", D * 0.6)

def sc_what(fr, t, D):
    dots(fr, 1); show(fr, kicker("What is it?"), 260, t, 0.1)
    ladder(fr, 340, t, 0.3)
    show(fr, gcard("Over 200 repeats: the gene is switched off, causing Fragile X syndrome", CORAL, 1, 32), 900, t, D * 0.45)
    show(fr, gcard("55-200 repeats (premutation): a carrier with other health risks", AMBER, 2, 32), 1070, t, D * 0.6)
    show(fr, source_tag(SRC_UW), 1240, t, D * 0.7)
    fire("pop", D * 0.45); fire("pop", D * 0.6)

def sc_who(fr, t, D):
    dots(fr, 2); show(fr, kicker("Who is affected"), 260, t, 0.1)
    show(fr, headline("About 1 in 4,000 to 6,250 males", 50), 330, t, 0.3)
    show(fr, gcard("Girls: about half as often, usually milder", LAV, 1, 33), 460, t, D * 0.2)
    show(fr, gcard("Learning and intellectual disability, developmental delay", CYAN, 2, 33), 610, t, D * 0.35)
    show(fr, gcard("Some also have seizures", AMBER, 3, 33), 760, t, D * 0.5)
    show(fr, source_tag(SRC_UW), 920, t, D * 0.6)
    fire("pop", D * 0.2); fire("pop", D * 0.35); fire("pop", D * 0.5)

sc_doc = s_cards(3, "Which doctors to visit", None,
    [("Paediatric neurologists and developmental paediatricians", CYAN), ("Child psychiatrists and autism centres", TEALG),
     ("Gynaecologists and IVF centres (early menopause)", AMBER), ("Neurologists (tremor and imbalance after 50)", LAV)],
    lambda fr, t, D, y: show(fr, body("One family can need all four", 32, SOFT), y + 20, t, D * 0.7), size=32)

def sc_india(fr, t, D):
    dots(fr, 4); show(fr, kicker("Indian data"), 260, t, 0.1)
    show(fr, headline("Kolkata: 157 patients tested", 54), 320, t, 0.3)
    hbars(fr, 450, [("Kolkata clinic", 3.18, "3.18% (5 of 157)", TEALG), ("Tamil Nadu boys", 10.34, "10.3% (3 of 29)", CORAL)], t, 0.6, 12, 300)
    show(fr, gcard("Kolkata: patients with behaviour and learning problems, Manovikas Kendra", CYAN, None, 31), 720, t, D * 0.4)
    show(fr, gcard("Tamil Nadu: boys with intellectual disability (small study)", AMBER, None, 31), 880, t, D * 0.5)
    show(fr, gcard("Rural West Bengal school screen: 0 of 179. Test the right children.", LAV, None, 31), 1040, t, D * 0.6)
    show(fr, source_tag(SRC_KOL + "; Nagarathinam et al., Adv Genet 2021; Dutta et al., IJMR 2009"), 1220, t, D * 0.7)
    fire("pop", D * 0.4); fire("pop", D * 0.5); fire("pop", D * 0.6)

def sc_family(fr, t, D):
    dots(fr, 5); show(fr, kicker("Premutation carriers: the family"), 260, t, 0.1)
    hbars(fr, 340, [("Early menopause, women", 28, "12-28%", AMBER), ("Tremor-ataxia, men", 40, "about 40%", CORAL),
                    ("Tremor-ataxia, women", 20, "16-20%", LAV)], t, 0.4, 60, 400)
    show(fr, body("Menopause before 40; tremor and ataxia usually from age 60-65", 30, SOFT), 660, t, D * 0.3)
    show(fr, gcard("One child's report starts testing for the mother and relatives", TEALG, None, 32), 800, t, D * 0.45)
    show(fr, gcard("A genetic counsellor explains each relative's risk", CYAN, None, 32), 960, t, D * 0.6)
    show(fr, source_tag(SRC_UW + " (FXPOI, FXTAS)"), 1130, t, D * 0.7)

def sc_test(fr, t, D):
    dots(fr, 6); show(fr, kicker("Which test"), 260, t, 0.1)
    show(fr, gcard("FMR1 CGG repeat analysis by PCR (Fragile X mutation analysis)", TEALG, 1, 32), 340, t, 0.3)
    show(fr, gcard("Large expansions: confirm by Southern blot or methylation test", AMBER, 2, 32), 510, t, D * 0.25)
    show(fr, gcard("Exome and microarray can miss repeat expansions", CORAL, 3, 33), 680, t, D * 0.4)
    show(fr, gcard("Autism: microarray and Fragile X are the traditional first tests", LAV, 4, 32), 840, t, D * 0.55)
    show(fr, source_tag(SRC_UW + "; " + SRC_KOL + "; AAP 2020"), 1010, t, D * 0.65)

sc_flags = s_cards(7, "Who to test", None,
    [("Unexplained intellectual disability or developmental delay", CYAN), ("Autism, boys and girls", TEALG),
     ("Family history of learning disability", AMBER), ("Women with menopause before 40", LAV), ("Adults over 50 with new tremor and imbalance", CORAL)], size=31)

def sc_talk(fr, t, D):
    dots(fr, 8); show(fr, kicker("How to start the conversation"), 260, t, 0.1)
    for i, (txt, c) in enumerate((("Ask: \"When the exome is negative, do you also test Fragile X?\"", CYAN),
                                  ("Fact: in a Kolkata clinic study, about 3 in 100 patients had Fragile X", AMBER), ("Leave the 2-page PDF", TEALG))):
        fire("pop", D * (0.1 + 0.18 * i)); show(fr, gcard(txt, c, i + 1, 32), 340 + i * 175, t, D * (0.1 + 0.18 * i))

def sc_obj(fr, t, D):
    dots(fr, 9); show(fr, kicker("When the doctor says..."), 260, t, 0.1)
    rows = [("\"Exome is already done\"", "Exome can miss repeat expansions. Fragile X needs its own PCR test.", TEALG),
            ("\"Fragile X is rare\"", "Kolkata clinic study: 3.18%. One result also guides the mother and relatives.", LAV)]
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
    show(fr, gcard("A carrier is not a patient; never blame the mother", CORAL, 3, 32), 1180, t, D * 0.45)
    show(fr, callout("Prenatal: disease testing only; sex never disclosed (PCPNDT)", CORAL, 31), 1360, t, D * 0.6)

sc_take = s_cards(11, "Key messages", None,
    [("FMR1 repeats over 200: Fragile X syndrome", CYAN), ("Kolkata clinic study: 3.18%", TEALG),
     ("Exome can miss it: order the PCR test by name", AMBER), ("Carriers: early menopause, tremor; test the family", LAV)], size=32)

SC = [(film(sc0), "doc"), (film(sc_what), "doc"), (film(sc_who), "doc"), (film(sc_doc), "doc"), (film(sc_india), "doc"),
      (film(sc_family), "doc"), (film(sc_test), "doc"), (film(sc_flags), "doc"), (film(sc_talk), "doc"), (film(sc_obj), "doc"),
      (film(sc_sample), "doc"), (film(sc_take), "doc"),
      (close_scene("Who sees these children most?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si, (fn, bg) in enumerate(SC):
            d = 16 if si < len(SC) - 1 else 33; p = .95 if si else 0.01; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((300, 533)))
        s = Image.new("RGB", (300 * 7, 533 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 7) * 300, (i // 7) * 533))
        s.save("/tmp/sheet_g015.png")
    else: run(SC, "/tmp/g015bn_", "Genetics_Ep15_Fragile_X_Bengali.mp4", max_sec=480)
