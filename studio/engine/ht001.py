"""High-End Tests, Episode 1: Liquid biopsy and NGS cancer panels (sales-team field guide, Bengali narration; Hindi teaser via hindi_teaser.py ht001 5)."""
import sys, random, math
from cbc_cartoon import run
from gen_series import *
from hts_close import close_scene
from g013 import hbars

TOT[0] = 10
TOPIC = "HIGH-END TESTS  •  EPISODE 1"
SRC_TM = "Veldore et al., Lung Cancer: Targets Ther 2018;9:1-11 (Tata Memorial, Mumbai)"
SRC_HY = "Sharma et al., Front Genet 2023 (Hyderabad, 53 lung adenocarcinomas)"
SRC_IA = "IASLC consensus on liquid biopsy, Rolfo et al., J Thorac Oncol 2021"

def stream(fr, y, t, tin):
    """A blood vessel carrying normal and tumour DNA fragments (illustration)."""
    lay, d = overlay(fr); e = ease((t - tin) / 0.8); a = int(255 * e)
    d.rounded_rectangle((X0, y, X0 + TW, y + 300), 150, fill=(180, 40, 60, int(70 * e)), outline=(220, 70, 90, a), width=5)
    r = random.Random(3)
    for i in range(26):
        u = (r.random() + t * 0.08 * (0.6 + r.random())) % 1.0
        x = X0 + 60 + u * (TW - 160); yy = y + 60 + r.random() * 180
        tum = i % 6 == 0; c = CORAL if tum else (*SOFT,)
        d.line((x, yy, x + 70, yy + 10 * math.sin(i)), fill=(*c[:3], a), width=9 if tum else 6)
    d.text((540, y + 350), "Tumour DNA (red) travels in the blood", font=font("Medium", 30), fill=(*SOFT, a), anchor="mm")
    fr.alpha_composite(lay)

# ---------------- scenes ----------------
def sc0(fr, t, D):
    show(fr, kicker("High-End Tests  •  Episode 1", CYAN), 330, t, 0.1)
    show(fr, headline("Liquid biopsy", 76), 410, t, -1)
    show(fr, headline("and NGS cancer panels", 52, (249, 196, 120)), 510, t, -1)
    if t > D * 0.3: type_on(fr, "A field guide for the sales team", 610, t, D * 0.3, 40, AMBER)
    stream(fr, 760, t, 0.4)
    show(fr, callout("Cancer gene testing from a blood sample", CYAN, 34), 1640, t, D * 0.6); fire("whoosh", D * 0.6)

def sc_what(fr, t, D):
    dots(fr, 1); show(fr, kicker("What is it?"), 260, t, 0.1)
    stream(fr, 330, t, 0.3)
    show(fr, gcard("Tumours release DNA pieces into the blood (ctDNA)", CORAL, 1, 33), 760, t, D * 0.3)
    show(fr, gcard("Liquid biopsy reads that DNA from a blood sample", TEALG, 2, 33), 910, t, D * 0.42)
    show(fr, gcard("NGS reads many cancer genes in one test", AMBER, 3, 34), 1060, t, D * 0.54)
    show(fr, gcard("Example in this episode: advanced lung cancer", LAV, 4, 33), 1200, t, D * 0.66)
    for k in (0.3, 0.42, 0.54, 0.66): fire("pop", D * k)

def sc_why(fr, t, D):
    dots(fr, 2); show(fr, kicker("Why genes matter in lung cancer"), 260, t, 0.1)
    show(fr, headline("Targeted medicines need a gene report", 46), 330, t, 0.3)
    hbars(fr, 520, [("Any actionable", 79, "79% (42 of 53)", TEALG), ("EGFR ex19/L858R", 20.8, "20.8%", CYAN),
                    ("Gene fusions", 11.3, "11.3%", AMBER)], t, 0.6, 110, 280)
    show(fr, gcard("Fusions: ALK, RET, NTRK, MET exon 14. One 46-gene panel, Hyderabad", LAV, None, 31), 860, t, D * 0.5)
    show(fr, source_tag(SRC_HY), 1030, t, D * 0.6)
    fire("pop", D * 0.5)

sc_doc = s_cards(3, "Which doctors to visit", None,
    [("Medical oncologists", CYAN), ("Pulmonologists (lung cancer diagnosis)", TEALG), ("Pathologists and cancer hospitals", AMBER),
     ("Tumour boards", LAV)],
    lambda fr, t, D, y: show(fr, body("IASLC advises a molecular tumour board to guide treatment", 31, SOFT), y + 20, t, D * 0.7), size=33)

def sc_india(fr, t, D):
    dots(fr, 4); show(fr, kicker("Indian data  •  Tata Memorial"), 260, t, 0.1)
    show(fr, headline("163 advanced lung cancer patients", 48), 320, t, 0.3)
    hbars(fr, 440, [("Agreed with tissue", 97, "97%", TEALG), ("Sensitivity", 91.1, "91.1%", CYAN), ("Specificity", 100, "100%", AMBER)], t, 0.6, 110, 300)
    show(fr, gcard("31 of 163 (about 1 in 5) had no tissue for testing", CORAL, None, 32), 780, t, D * 0.42)
    show(fr, gcard("Plasma found EGFR in 16% of them: a path to targeted medicine", LAV, None, 32), 930, t, D * 0.55)
    show(fr, source_tag(SRC_TM), 1100, t, D * 0.65)
    fire("pop", D * 0.42); fire("pop", D * 0.55)

def sc_when(fr, t, D):
    dots(fr, 5); show(fr, kicker("When to use it (IASLC 2021)"), 260, t, 0.1)
    show(fr, gcard("At diagnosis: complements tissue; plasma-first is acceptable", TEALG, 1, 32), 340, t, 0.3)
    show(fr, gcard("Progression on targeted medicine: plasma preferred first", AMBER, 2, 32), 510, t, D * 0.25)
    show(fr, gcard("Monitoring targeted therapy: an emerging use", LAV, 3, 33), 680, t, D * 0.4)
    show(fr, gcard("Use a clinically validated NGS panel", CYAN, 4, 34), 840, t, D * 0.55)
    show(fr, source_tag(SRC_IA), 1000, t, D * 0.65)

def sc_limit(fr, t, D):
    dots(fr, 6); show(fr, kicker("Know the limits"), 260, t, 0.1)
    show(fr, gcard("A negative plasma result does not rule out a mutation", CORAL, 1, 32), 340, t, 0.3)
    show(fr, gcard("Tata Memorial: 4 of 45 EGFR-positive patients were missed", AMBER, 2, 32), 510, t, D * 0.25)
    show(fr, gcard("Uninformative plasma: the next step is a tissue biopsy", TEALG, 3, 32), 680, t, D * 0.4)
    show(fr, gcard("Not a screening test for healthy people", LAV, 4, 34), 850, t, D * 0.55)
    show(fr, source_tag(SRC_TM + "; " + SRC_IA), 1010, t, D * 0.65)

def sc_test(fr, t, D):
    dots(fr, 7); show(fr, kicker("Which test to suggest"), 260, t, 0.1)
    show(fr, gcard("Enough tissue: tissue NGS panel", TEALG, 1, 34), 340, t, 0.3)
    show(fr, gcard("Little or no tissue, or progression: plasma (liquid biopsy) NGS", AMBER, 2, 32), 490, t, D * 0.25)
    show(fr, gcard("Where NGS is not possible: EGFR PCR as a first step", LAV, 3, 32), 660, t, D * 0.4)
    show(fr, gcard("Confirm with the lab: genes covered, blood tube, report time", CORAL, 4, 32), 830, t, D * 0.55)
    show(fr, source_tag(SRC_IA), 1000, t, D * 0.65)

sc_flags = s_cards(8, "Which patients especially", None,
    [("Advanced lung cancer, tissue not enough for gene tests", CORAL), ("Biopsy not possible or not available", AMBER),
     ("Cancer growing again on a targeted medicine", LAV), ("Waiting for a gene result to start treatment", CYAN)], size=32)

def sc_talk(fr, t, D):
    dots(fr, 9); show(fr, kicker("How to start the conversation"), 260, t, 0.1)
    for i, (txt, c) in enumerate((("Ask: \"When tissue is not enough for EGFR and ALK, do you send plasma NGS?\"", CYAN),
                                  ("Fact: at Tata Memorial, about 1 in 5 had no tissue for testing", AMBER),
                                  ("Fact: plasma agreed with tissue in 97%", TEALG), ("Leave the 2-page PDF", LAV))):
        fire("pop", D * (0.1 + 0.16 * i)); show(fr, gcard(txt, c, i + 1, 32), 340 + i * 170, t, D * (0.1 + 0.16 * i))

def sc_obj(fr, t, D):
    dots(fr, 10); show(fr, kicker("When the doctor says..."), 260, t, 0.1)
    rows = [("\"Tissue is the gold standard\"", "Agreed. Plasma complements it; a positive plasma result was 100% specific at Tata Memorial.", TEALG),
            ("\"What if plasma is negative?\"", "Then a tissue test is the next step; a negative plasma result does not rule out a mutation.", LAV)]
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
    put(fr, tube_sprite((120, 130, 150), "DNA"), 300, 600, 0.9, ease((t - 0.3) / 0.5))
    show(fr, gcard("Blood in the special tube the lab specifies", TEALG, 1, 33), 890, t, D * 0.2)
    show(fr, gcard("Follow the lab's transport time and temperature", AMBER, 2, 33), 1030, t, D * 0.32)
    show(fr, gcard("Never say it replaces a biopsy for diagnosis", CORAL, 3, 33), 1190, t, D * 0.45)
    show(fr, gcard("Never promise a medicine will work; that is the oncologist's call", LAV, 4, 31), 1330, t, D * 0.58)

sc_take = s_cards(12, "Key messages", None,
    [("Liquid biopsy: cancer gene testing from blood", CYAN), ("Tata Memorial: 97% agreement with tissue", TEALG),
     ("Best when tissue is not enough, or at progression", AMBER), ("Negative plasma: tissue test next", LAV)], size=32)

SC = [(film(sc0), "doc"), (film(sc_what), "doc"), (film(sc_why), "doc"), (film(sc_doc), "doc"), (film(sc_india), "doc"),
      (film(sc_when), "doc"), (film(sc_limit), "doc"), (film(sc_test), "doc"), (film(sc_flags), "doc"), (film(sc_talk), "doc"),
      (film(sc_obj), "doc"), (film(sc_sample), "doc"), (film(sc_take), "doc"),
      (close_scene("Which oncologists do you meet?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si, (fn, bg) in enumerate(SC):
            d = 16 if si < len(SC) - 1 else 33; p = .95 if si else 0.01; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((300, 533)))
        s = Image.new("RGB", (300 * 7, 533 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 7) * 300, (i // 7) * 533))
        s.save("/tmp/sheet_ht001.png")
    else: run(SC, "/tmp/ht001bn_", "HighEnd_Ep01_Liquid_Biopsy_NGS_Bengali.mp4", max_sec=480)
