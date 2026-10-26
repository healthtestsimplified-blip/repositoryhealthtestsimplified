"""Genetics Clinical Series, Episode 12: Autism, when to test (sales-team field guide, Bengali narration)."""
import sys, random
from cbc_cartoon import run
from gen_series import *
from hts_close import close_scene

TOT[0] = 12
TOPIC = "GENETICS SERIES  •  EPISODE 12"
PAPER = paper_sprite(["Comparative yield of", "molecular diagnostic", "algorithms for autism", "in India"], "BMC Neurology, 2023 (Ahmedabad)")

def bars(fr, y, rows, t, tin, vmax, labw=330):
    lay, d = overlay(fr); e = ease((t - tin) / 1.2)
    for i, (lab, v, txt, c) in enumerate(rows):
        yy = y + i * 110
        d.text((X0, yy + 28), lab, font=font("Medium", 30), fill=SOFT, anchor="lm")
        L = max(16, (TW - labw - 170) * v / vmax * e)
        d.rounded_rectangle((X0 + labw, yy, X0 + labw + L, yy + 56), 28, fill=c)
        d.text((X0 + labw + 18 + L, yy + 28), txt, font=font("Bold", 30), fill=WHITE, anchor="lm")
    fr.alpha_composite(lay)

def clinic_vs_lab(fr, y, t, tin):
    """Two boxes: diagnosis by the doctor (behaviour) vs cause by genetic test."""
    lay, d = overlay(fr); e = ease((t - tin) / 0.6); a = int(255 * e)
    for i, (head, sub, c) in enumerate((("Autism diagnosis", "By the doctor: behaviour and communication", CYAN), ("Genetic test", "Looks for the cause behind it", TEALG))):
        x = X0 + i * (TW / 2 + 10); w = TW / 2 - 10
        d.rounded_rectangle((x, y, x + w, y + 300), 26, fill=(*c, int(40 * e)), outline=(*c, a), width=3)
        d.text((x + w / 2, y + 70), head, font=font("Bold", 34), fill=(*c, a), anchor="mm")
        for j, line in enumerate(wrap(sub, font("Medium", 30), w - 50)):
            d.text((x + w / 2, y + 150 + j * 42), line, font=font("Medium", 30), fill=(*SOFT, a), anchor="mm")
    fr.alpha_composite(lay)

# ---------------- scenes ----------------
def sc0(fr, t, D):
    show(fr, kicker("Genetics Clinical Series  •  Episode 12", CYAN), 330, t, 0.1)
    show(fr, headline("Autism:", 72), 410, t, -1)
    show(fr, headline("when to test", 72), 500, t, -1)
    if t > D * 0.3: type_on(fr, "A field guide for the sales team", 620, t, D * 0.3, 40, AMBER)
    clinic_vs_lab(fr, 820, t, 0.5)
    show(fr, callout("Which doctors, which children, which test, what to say", CYAN, 34), 1640, t, D * 0.6); fire("whoosh", D * 0.6)

def sc_first(fr, t, D):
    dots(fr, 1); show(fr, kicker("First, be clear"), 260, t, 0.1)
    clinic_vs_lab(fr, 360, t, 0.3)
    show(fr, callout("A genetic test does not diagnose autism", CORAL, 36), 760, t, D * 0.5); fire("ding", D * 0.5)

sc_who = s_cards(2, "Which doctors and centres to visit", None,
    [("Paediatricians, paediatric neurologists", CYAN), ("Developmental paediatricians", TEALG), ("Child psychiatrists and psychologists", LAV),
     ("Autism therapy, speech and OT centres", AMBER), ("Special schools", CORAL)], size=33)

sc_why = s_cards(3, "Why a cause matters", None,
    [("Recurrence risk for the next child", AMBER), ("Some causes change seizure treatment or monitoring", TEALG),
     ("Ends years of doctor-hopping", CYAN), ("Families can join condition-specific support groups", LAV)], size=33)

def sc_india1(fr, t, D):
    dots(fr, 4); show(fr, kicker("Indian data  •  Ahmedabad"), 260, t, 0.1)
    show(fr, headline("101 children with autism, trio testing", 50), 320, t, 0.3)
    bars(fr, 470, [("Karyotype", 0, "0%", (120, 140, 170)), ("Fragile X (boys)", 0, "0%", (120, 140, 170)),
                   ("Microarray", 2.9, "2.9%", CYAN), ("Exome", 29.7, "29.7%", TEALG)], t, 0.6, 35)
    put(fr, PAPER, 540, 1170, 0.42, ease((t - D * 0.5) / 0.6))
    show(fr, source_tag("Sheth et al., BMC Neurology 2023;23:292 (FRIGE, Ahmedabad), CC BY"), 1400, t, D * 0.55)

def sc_india2(fr, t, D):
    dots(fr, 5); show(fr, kicker("Who had a cause found?"), 260, t, 0.1)
    bars(fr, 360, [("With seizures", 53.6, "53.6%", CORAL), ("Without seizures", 20.5, "20.5%", AMBER)], t, 0.3, 60, 360)
    show(fr, gcard("Most common: MECP2 (Rett syndrome)", LAV, 1, 34), 640, t, D * 0.35)
    show(fr, gcard("About two-thirds were new (de novo) changes", TEALG, 2, 34), 790, t, D * 0.5)
    show(fr, source_tag("Sheth et al., BMC Neurology 2023"), 950, t, D * 0.55)
    fire("pop", D * 0.35); fire("pop", D * 0.5)

def sc_india3(fr, t, D):
    dots(fr, 6); show(fr, kicker("Indian data  •  Mumbai"), 260, t, 0.1)
    show(fr, headline("137 children, trio exome: 16.1% found", 50), 320, t, 0.3)
    bars(fr, 480, [("Syndromic features", 35, "35%", CORAL), ("Autism only", 8.2, "8.2%", (120, 140, 170))], t, 0.6, 45, 380)
    show(fr, gcard("91.3% of the changes found were de novo", TEALG, None, 34), 760, t, D * 0.5)
    show(fr, source_tag("Bajaj et al., J Hum Genet 2025;70:611-624 (Mumbai)"), 920, t, D * 0.55)

sc_flags = s_cards(7, "Which children: higher chance of an answer", None,
    [("Seizures", CORAL), ("Dysmorphic features or birth defects", AMBER), ("Intellectual disability as well", LAV),
     ("Girls who lose skills: think Rett syndrome", TEALG)], size=34)

def sc_test(fr, t, D):
    dots(fr, 8); show(fr, kicker("Which test?"), 260, t, 0.1)
    show(fr, gcard("Guidelines: offer genetic testing to every child with autism", CYAN, 1, 32), 340, t, 0.3)
    show(fr, gcard("Traditional first tests: microarray + Fragile X", AMBER, 2, 33), 500, t, D * 0.25)
    show(fr, gcard("Indian authors: exome first, trio if possible", TEALG, 3, 33), 650, t, D * 0.45)
    show(fr, callout("The final choice is always the doctor's", LAV, 34), 830, t, D * 0.65)
    show(fr, source_tag("AAP clinical report 2020 (Hyman et al.); Sheth et al. 2023"), 960, t, D * 0.7)
    fire("pop", D * 0.25); fire("pop", D * 0.45)

def sc_talk(fr, t, D):
    dots(fr, 9); show(fr, kicker("How to start the conversation"), 260, t, 0.1)
    for i, (txt, c) in enumerate((("Ask: \"Do you test autistic children who also have seizures?\"", CYAN),
                                  ("Fact: in Ahmedabad, over half of them had a cause found", AMBER), ("Leave the 2-page case PDF", TEALG))):
        fire("pop", D * (0.1 + 0.18 * i)); show(fr, gcard(txt, c, i + 1, 32), 340 + i * 165, t, D * (0.1 + 0.18 * i))

def sc_obj(fr, t, D):
    dots(fr, 10); show(fr, kicker("When the doctor says..."), 260, t, 0.1)
    rows = [("\"Therapy is the real treatment\"", "Yes, therapy continues. A cause adds recurrence risk and sometimes changes seizure care.", TEALG),
            ("\"Reports come back uncertain\"", "Trio testing gives clearer reports; no major decisions on a VUS.", LAV)]
    lay, d = overlay(fr)
    for i, (q, a_, c) in enumerate(rows):
        e = ease((t - D * (0.1 + 0.35 * i)) / 0.5); al = int(255 * e); yy = 340 + i * 300
        d.rounded_rectangle((X0, yy, X0 + TW, yy + 260), 24, fill=(255, 255, 255, int(20 * e)), outline=(*c, al), width=3)
        d.text((X0 + 30, yy + 50), q, font=font("Bold", 34), fill=(*c, al), anchor="lm")
        for j, line in enumerate(wrap(a_, font("Medium", 32), TW - 60)):
            d.text((X0 + 30, yy + 115 + j * 42), line, font=font("Medium", 32), fill=(*SOFT, al), anchor="lm")
    fr.alpha_composite(lay)

sc_rules = s_cards(11, "Sample and field rules", None,
    [("EDTA blood; parents too for trio", CYAN), ("Counselling and written consent first", TEALG),
     ("Never say the test cures autism", CORAL), ("No guarantees; sourced facts only; confirm price and report time", AMBER)], size=32)

sc_take = s_cards(12, "Key messages", None,
    [("Genetic tests find the cause, not the autism diagnosis", CYAN), ("India: trio exome found up to about 30%", TEALG),
     ("Higher chance with seizures, syndromic features or ID", AMBER), ("Therapy centres are a big opportunity", LAV)], size=32)

SC = [(film(sc0), "doc"), (film(sc_first), "doc"), (film(sc_who), "doc"), (film(sc_why), "doc"), (film(sc_india1), "doc"),
      (film(sc_india2), "doc"), (film(sc_india3), "doc"), (film(sc_flags), "doc"), (film(sc_test), "doc"),
      (film(sc_talk), "doc"), (film(sc_obj), "doc"), (film(sc_rules), "doc"), (film(sc_take), "doc"),
      (close_scene("Where do autism cases come?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si, (fn, bg) in enumerate(SC):
            d = 16 if si < len(SC) - 1 else 33; p = .95 if si else 0.01; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((300, 533)))
        s = Image.new("RGB", (300 * 5, 533 * 3), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 300, (i // 5) * 533))
        s.save("/tmp/sheet_g012.png")
    elif len(sys.argv) > 1 and sys.argv[1] == "teaser":
        import doc_style
        run([(close_scene("Where do autism cases come?", "WATCH THE FULL VIDEO ON OUR CHANNEL"), "docl")], "/tmp/tzbn_g012_", "/tmp/tzbn_g012.mp4", max_sec=180, cover_skip=0)
    else: run(SC, "/tmp/g012bn_", "Genetics_Ep12_Autism_When_To_Test_Bengali.mp4", max_sec=480)
