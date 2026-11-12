"""Genetics Clinical Series, Episode 17: Spinal muscular atrophy (sales-team field guide, Bengali narration; Hindi teaser via hindi_teaser.py g017 5)."""
import sys
from cbc_cartoon import run
from gen_series import *
from hts_close import close_scene
from g013 import hbars

TOT[0] = 10
TOPIC = "GENETICS SERIES  •  EPISODE 17"
SRC_NI = "NINDS: Spinal muscular atrophy fact sheet"
SRC_MDA = "MDA: SMA fact sheet"
SRC_KL = "Aswathy et al., Indian J Exp Biol 2024;62:810-4 (Kerala)"
SRC_NI2 = "Kaur et al., J Family Med Prim Care 2022;11:7870-4 (North India)"
SRC_JD = "Shekhawat et al., J Neurosci Rural Pract 2025;16:271-9 (AIIMS Jodhpur)"

def copies(fr, y, t, tin):
    """SMN1 copy number: 2 = typical, 1 = carrier, 0 = SMA (illustration)."""
    lay, d = overlay(fr)
    rows = [("2 copies", "Typical", 2, TEALG), ("1 copy", "Carrier (healthy)", 1, AMBER), ("0 copies", "SMA", 0, CORAL)]
    for i, (lab, mean, n, c) in enumerate(rows):
        e = ease((t - tin - i * 0.35) / 0.6); a = int(255 * e); yy = y + i * 130
        d.text((X0, yy + 40), lab, font=font("Bold", 34), fill=(*WHITE, a), anchor="lm")
        for k in range(2):
            x = X0 + 230 + k * 120
            if k < n: d.rounded_rectangle((x, yy + 10, x + 100, yy + 70), 14, fill=(*c, a))
            else: d.rounded_rectangle((x, yy + 10, x + 100, yy + 70), 14, outline=(*c, a), width=4)
        d.text((X0 + 500, yy + 40), mean, font=font("Bold", 34), fill=(*c, a), anchor="lm")
    e = ease((t - tin - 1.4) / 0.6)
    d.text((540, y + 410), "SMN1 gene copies (illustration)", font=font("Medium", 30), fill=(*SOFT, int(255 * e)), anchor="mm")
    fr.alpha_composite(lay)

# ---------------- scenes ----------------
def sc0(fr, t, D):
    show(fr, kicker("Genetics Clinical Series  •  Episode 17", CYAN), 330, t, 0.1)
    show(fr, headline("Spinal muscular", 76), 410, t, -1)
    show(fr, headline("atrophy (SMA)", 76, (249, 196, 120)), 500, t, -1)
    if t > D * 0.3: type_on(fr, "A field guide for the sales team", 610, t, D * 0.3, 40, AMBER)
    copies(fr, 760, t, 0.4)
    show(fr, callout("A blood test that now leads to treatment", CYAN, 34), 1640, t, D * 0.6); fire("whoosh", D * 0.6)

def sc_what(fr, t, D):
    dots(fr, 1); show(fr, kicker("What is it?"), 260, t, 0.1)
    show(fr, headline("About 1 in 10,000 births", 54), 330, t, 0.3)
    show(fr, gcard("Motor nerve cells in the spinal cord are lost: muscles weaken", CYAN, 1, 32), 460, t, D * 0.2)
    show(fr, gcard("Cause: both copies of the SMN1 gene (chromosome 5) faulty", CORAL, 2, 32), 630, t, D * 0.32)
    show(fr, gcard("SMN2 gene: more copies usually means milder disease", AMBER, 3, 32), 800, t, D * 0.44)
    show(fr, gcard("Thinking and learning are not affected", TEALG, 4, 34), 970, t, D * 0.56)
    show(fr, source_tag(SRC_NI + "; " + SRC_MDA), 1130, t, D * 0.66)
    for k in (0.2, 0.32, 0.44, 0.56): fire("pop", D * k)

sc_types = s_cards(2, "The 4 types (NINDS)", None,
    [("Type 1: before 6 months; never sits without help", CORAL), ("Type 2: 6-18 months; sits, cannot stand or walk", AMBER),
     ("Type 3: after 18 months; can walk", LAV), ("Type 4: adult onset; milder weakness", TEALG)],
    lambda fr, t, D, y: show(fr, source_tag(SRC_NI), y + 20, t, D * 0.7), size=32)

sc_doc = s_cards(3, "Which doctors to visit", None,
    [("Paediatric neurologists", CYAN), ("Paediatricians and neonatologists (weak, floppy babies)", TEALG),
     ("Physiotherapy and rehabilitation centres", AMBER), ("Orthopaedics (scoliosis) and pulmonologists (breathing)", LAV)], size=31)

def sc_india(fr, t, D):
    dots(fr, 4); show(fr, kicker("Indian data"), 260, t, 0.1)
    show(fr, headline("Kerala: 33 children, low tone", 52), 320, t, 0.3)
    hbars(fr, 440, [("SMN1 deletion", 58, "58% (19 of 33)", TEALG), ("Of them, type 1", 68.4, "68.4%", CORAL)], t, 0.6, 100, 300)
    show(fr, gcard("All parents tested were healthy carriers", AMBER, None, 33), 680, t, D * 0.4)
    show(fr, gcard("North India: 1 in 30 healthy adults is a carrier", LAV, None, 33), 830, t, D * 0.52)
    show(fr, source_tag(SRC_KL + "; " + SRC_NI2), 990, t, D * 0.62)
    fire("pop", D * 0.4); fire("pop", D * 0.52)

def sc_tx(fr, t, D):
    dots(fr, 5); show(fr, kicker("Why diagnosis is urgent now"), 260, t, 0.1)
    show(fr, gcard("2016: nusinersen, injection into spinal fluid", CYAN, 1, 33), 340, t, 0.3)
    show(fr, gcard("2019: onasemnogene, one-time gene therapy (under 2 years)", AMBER, 2, 32), 490, t, D * 0.2)
    show(fr, gcard("2020: risdiplam, a medicine by mouth", TEALG, 3, 34), 660, t, D * 0.32)
    show(fr, gcard("India: a lower-cost generic risdiplam has been launched", LAV, 4, 32), 810, t, D * 0.44)
    show(fr, callout("Benefit is best when treatment starts early", CORAL, 34), 990, t, D * 0.56)
    show(fr, source_tag(SRC_MDA + "; " + SRC_NI + "; MrMed: risdiplam India launch"), 1150, t, D * 0.66)
    for k in (0.2, 0.32, 0.44): fire("pop", D * k)

def sc_test(fr, t, D):
    dots(fr, 6); show(fr, kicker("Which test"), 260, t, 0.1)
    show(fr, gcard("SMN1 deletion test (copy number by MLPA or ddPCR)", TEALG, 1, 33), 340, t, 0.3)
    show(fr, gcard("Finds at least 95% of type 1, 2 and 3 cases", CYAN, 2, 33), 500, t, D * 0.22)
    show(fr, gcard("SMN2 copy number: helps predict the likely course", AMBER, 3, 32), 650, t, D * 0.34)
    show(fr, gcard("AIIMS Jodhpur: MLPA and ddPCR agreed fully", LAV, 4, 33), 810, t, D * 0.46)
    show(fr, gcard("Not on our standard menu: confirm with the lab first", CORAL, 5, 32), 960, t, D * 0.58)
    show(fr, source_tag(SRC_NI + "; " + SRC_MDA + "; " + SRC_JD), 1120, t, D * 0.68)

sc_flags = s_cards(7, "Which children especially", None,
    [("Weak, floppy baby", CORAL), ("Not sitting or standing at the expected age", AMBER), ("Lost motor skills, falls more", LAV),
     ("Tongue twitching (fasciculations)", CYAN), ("Weak cry, feeding or breathing difficulty", TEALG)], size=32)

def sc_family(fr, t, D):
    dots(fr, 8); show(fr, kicker("The family"), 260, t, 0.1)
    show(fr, headline("Both parents are usually healthy carriers", 44), 330, t, 0.3)
    show(fr, gcard("Each pregnancy: 1 in 4 chance of an affected child", CORAL, 1, 33), 450, t, D * 0.25)
    show(fr, gcard("Carrier test for parents, brothers and sisters", TEALG, 2, 33), 600, t, D * 0.38)
    show(fr, gcard("Next pregnancy: prenatal testing with counselling", AMBER, 3, 33), 750, t, D * 0.5)
    show(fr, callout("Prenatal: disease testing only; sex never disclosed (PCPNDT)", CORAL, 31), 920, t, D * 0.62)
    show(fr, source_tag(SRC_NI + " (autosomal recessive); " + SRC_KL), 1080, t, D * 0.7)

def sc_talk(fr, t, D):
    dots(fr, 9); show(fr, kicker("How to start the conversation"), 260, t, 0.1)
    for i, (txt, c) in enumerate((("Ask: \"In a weak, floppy baby, do you send the SMN1 test early?\"", CYAN),
                                  ("Fact: in Kerala, 58% of tested children with low tone had SMA", AMBER),
                                  ("Fact: treatment works best when started early", TEALG), ("Leave the 2-page PDF", LAV))):
        fire("pop", D * (0.1 + 0.16 * i)); show(fr, gcard(txt, c, i + 1, 32), 340 + i * 170, t, D * (0.1 + 0.16 * i))

def sc_obj(fr, t, D):
    dots(fr, 10); show(fr, kicker("When the doctor says..."), 260, t, 0.1)
    rows = [("\"Let us do EMG first\"", "The SMN1 blood test finds at least 95% of cases (NINDS), without a needle test.", TEALG),
            ("\"Treatment is unaffordable\"", "Risdiplam is a medicine by mouth, and a lower-cost generic is now in India. The doctor decides.", LAV)]
    lay, d = overlay(fr)
    for i, (q, a_, c) in enumerate(rows):
        e = ease((t - D * (0.1 + 0.35 * i)) / 0.5); al = int(255 * e); yy = 340 + i * 300
        d.rounded_rectangle((X0, yy, X0 + TW, yy + 260), 24, fill=(255, 255, 255, int(20 * e)), outline=(*c, al), width=3)
        d.text((X0 + 30, yy + 50), q, font=font("Bold", 34), fill=(*c, al), anchor="lm")
        for j, line in enumerate(wrap(a_, font("Medium", 32), TW - 60)):
            d.text((X0 + 30, yy + 115 + j * 42), line, font=font("Medium", 32), fill=(*SOFT, al), anchor="lm")
    fr.alpha_composite(lay)

def sc_sample(fr, t, D):
    dots(fr, 11); show(fr, kicker("Sample and field rules"), 260, t, 0.1)
    put(fr, tube_sprite((149, 117, 205), "EDTA"), 300, 600, 0.9, ease((t - 0.3) / 0.5))
    show(fr, gcard("EDTA blood; parents for carrier testing", TEALG, 1, 33), 900, t, D * 0.2)
    show(fr, gcard("Counselling and written consent first", LAV, 2, 33), 1050, t, D * 0.32)
    show(fr, gcard("Never promise a cure; medicine choice is the doctor's", CORAL, 3, 32), 1200, t, D * 0.45)
    show(fr, gcard("Never blame the parents; carriers are healthy", AMBER, 4, 33), 1350, t, D * 0.58)

sc_take = s_cards(12, "Key messages", None,
    [("SMA: a treatable genetic cause of weakness in babies", CYAN), ("SMN1 blood test finds 95% or more", TEALG),
     ("Earlier treatment, better results", AMBER), ("Paediatric neurologists and paediatricians first", LAV)], size=32)

SC = [(film(sc0), "doc"), (film(sc_what), "doc"), (film(sc_types), "doc"), (film(sc_doc), "doc"), (film(sc_india), "doc"),
      (film(sc_tx), "doc"), (film(sc_test), "doc"), (film(sc_flags), "doc"), (film(sc_family), "doc"), (film(sc_talk), "doc"),
      (film(sc_obj), "doc"), (film(sc_sample), "doc"), (film(sc_take), "doc"),
      (close_scene("Who sees weak babies most?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si, (fn, bg) in enumerate(SC):
            d = 16 if si < len(SC) - 1 else 33; p = .95 if si else 0.01; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((300, 533)))
        s = Image.new("RGB", (300 * 7, 533 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 7) * 300, (i // 7) * 533))
        s.save("/tmp/sheet_g017.png")
    else: run(SC, "/tmp/g017bn_", "Genetics_Ep17_SMA_Bengali.mp4", max_sec=480)
