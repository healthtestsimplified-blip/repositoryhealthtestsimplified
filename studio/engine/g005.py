"""Genetics Clinical Series, Episode 5: Genetic counselling and consent."""
import sys
from cbc_cartoon import run
from gen_series import *
from hts_close import close_scene
from g004 import ped

TOT[0] = 14
TOPIC = "GENETICS SERIES  •  EPISODE 5"
PAPER = paper_sprite(["WES helps molecular", "diagnosis in siblings:", "22q12 dup + recessive ichthyosis"], "F1000Research, 2015 (India)")

def consent_form(checks=(True, True, False, True)):
    w, h = 760, 900; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((14, 14, w, h), fill=(0, 0, 0, 90)); d.rectangle((0, 0, w - 14, h - 14), fill=(251, 251, 248))
    d.rectangle((0, 0, w - 14, 90), fill=(16, 42, 78))
    d.text((30, 45), "CONSENT FOR GENETIC TESTING (sample)", font=font("Bold", 28), fill=WHITE, anchor="lm")
    items = ["Purpose and limits of the test explained", "Possible results incl. VUS explained", "Report secondary findings?", "Store sample/data for re-analysis?",
             "Who may receive the report"]
    for i, txt in enumerate(items):
        y = 140 + i * 110
        d.rectangle((30, y, 70, y + 40), outline=(40, 50, 70), width=3)
        if i < len(checks) and checks[i]: d.line((36, y + 20, 48, y + 34, 66, y + 6), fill=(30, 140, 90), width=6)
        d.text((95, y + 20), txt, font=font("Medium", 28), fill=(20, 30, 60), anchor="lm")
    d.line((30, 760, 330, 760), fill=(120, 130, 150), width=2); d.text((30, 790), "Patient / guardian", font=font("Regular", 22), fill=(90, 100, 120))
    d.line((420, 760, 720, 760), fill=(120, 130, 150), width=2); d.text((420, 790), "Counsellor / doctor", font=font("Regular", 22), fill=(90, 100, 120))
    return im
FORM = consent_form()

def talk(fr, cx, cy, t, tin):
    """Two people in conversation (doctor/counsellor and family) — simple silhouettes with speech bubbles."""
    lay, d = overlay(fr); e = ease((t - tin) / 0.6); a = int(255 * e)
    for x, col in ((cx - 200, CYAN), (cx + 200, LAV)):
        d.ellipse((x - 55, cy - 190, x + 55, cy - 80), fill=(*col, a)); d.rounded_rectangle((x - 95, cy - 60, x + 95, cy + 150), 60, fill=(*col, a))
    if e > 0.5:
        k = int((t * 1.2) % 2)
        bx = cx - 120 if k == 0 else cx + 120
        d.rounded_rectangle((bx - 120, cy - 330, bx + 120, cy - 230), 40, fill=(255, 255, 255, 220))
        for j in range(3): d.ellipse((bx - 50 + j * 50 - 10, cy - 290, bx - 50 + j * 50 + 10, cy - 270), fill=(*INK, 255))
    fr.alpha_composite(lay)

CASE = ({"f": (390, 0, "m", "c"), "m": (690, 0, "f", "c"),
         "a": (300, 260, "u", "ap"), "b": (540, 260, "u", "a"), "p": (780, 260, "u", "")},
        [("f", "m", 0)], [(("f", "m"), ["a", "b", "p"])])
def case_at(dy): return {k: (x, y + dy, s, f) for k, (x, y, s, f) in CASE[0].items()}

# ---------------- scenes ----------------
def sc0(fr, t, D):
    show(fr, kicker("Genetics Clinical Series  •  Episode 5", CYAN), 330, t, 0.1)
    type_on(fr, "Genetic counselling", 410, t, 0.3, 70)
    type_on(fr, "and consent", 500, t, 0.9, 70)
    if t > D * 0.3: type_on(fr, "Before the test, and after the report", 610, t, D * 0.3, 42, AMBER)
    talk(fr, 540, 1100, t, 0.5)
    show(fr, callout("For doctors and healthcare teams  •  with a published Indian case", CYAN, 34), 1640, t, D * 0.6); fire("whoosh", D * 0.6)

def sc_what(fr, t, D):
    dots(fr, 1); show(fr, kicker("What is genetic counselling?"), 260, t, 0.1)
    talk(fr, 540, 700, t, 0.3)
    show(fr, gcard("Explains the condition, the test, and what results mean for patient and family", CYAN, 1, 33), 940, t, D * 0.3)
    show(fr, callout("Non-directive: the decision belongs to the family", AMBER, 36), 1110, t, D * 0.55); fire("ding", D * 0.55)

sc_pre = s_cards(2, "Pre-test counselling", None,
    [("Why this test", CYAN), ("What it can and cannot find", LAV), ("Possible results: positive, negative, VUS", AMBER),
     ("Turnaround time and cost", TEALG), ("Sample/data stored for re-analysis?", CORAL)], size=34)

def sc_consent(fr, t, D):
    dots(fr, 3); show(fr, kicker("Decisions in the consent form"), 260, t, 0.1)
    put(fr, FORM, 540, 830, 0.95, ease((t - 0.3) / 0.6))
    show(fr, gcard("Secondary findings: actionable results unrelated to the reason for testing", AMBER, None, 32), 1320, t, D * 0.5)

sc_family = s_cards(4, "Implications for the family", None,
    [("Results can show risk for siblings, children, parents", CYAN), ("Trio tests can reveal unexpected family-relationship information", AMBER),
     ("Discuss this before consent", TEALG)],
    lambda fr, t, D, y: ped(fr, t, D * 0.5, {k: (x, yy + y - 30, s, f) for k, (x, yy, s, f) in CASE[0].items()}, CASE[1], CASE[2], s=40))

def sc_minor(fr, t, D):
    dots(fr, 5); show(fr, kicker("Testing children"), 260, t, 0.1)
    show(fr, headline("Predictive testing for adult-onset disease", 56), 320, t, 0.3)
    show(fr, gcard("If nothing can be done in childhood: usually deferred until adulthood", AMBER, 1, 33), 520, t, D * 0.3)
    show(fr, callout("So the child can decide for themselves", TEALG, 36), 690, t, D * 0.5)
    show(fr, source_tag("ASHG position statement, Am J Hum Genet 2015"), 830, t, D * 0.55)
    talk(fr, 540, 1250, t, D * 0.6)

def sc_prenatal(fr, t, D):
    dots(fr, 6); show(fr, kicker("Prenatal testing (India)", CORAL), 260, t, 0.1)
    show(fr, gcard("PCPNDT Act: written consent required", CORAL, 1, 35), 340, t, 0.3)
    show(fr, gcard("Testing only for disease", AMBER, 2, 35), 490, t, D * 0.25)
    show(fr, callout("Sex of the baby is never disclosed", CORAL, 40), 660, t, D * 0.45); fire("ding", D * 0.45)
    put(fr, FORM, 540, 1220, 0.6, ease((t - D * 0.55) / 0.6))

sc_post = s_cards(7, "Post-test counselling", None,
    [("Explain the report in simple words", CYAN), ("Management plan and referrals", TEALG), ("Recurrence risk for future pregnancies", AMBER),
     ("Cascade testing of relatives", LAV), ("Emotional support; no big decisions on a VUS", CORAL)], size=33)

def sc_privacy(fr, t, D):
    dots(fr, 8); show(fr, kicker("Privacy"), 260, t, 0.1)
    show(fr, headline("Genetic information is sensitive", 58), 320, t, 0.3)
    lay, d = overlay(fr); e = ease((t - 0.6) / 0.6); cx, cy = 540, 700
    d.rounded_rectangle((cx - 130, cy - 40, cx + 130, cy + 160), 30, fill=(*AMBER, int(230 * e)))
    d.arc((cx - 90, cy - 170, cx + 90, cy + 10), 180, 360, fill=(*AMBER, int(255 * e)), width=30)
    d.ellipse((cx - 22, cy + 30, cx + 22, cy + 74), fill=(*INK, int(255 * e))); d.rectangle((cx - 9, cy + 60, cx + 9, cy + 120), fill=(*INK, int(255 * e)))
    fr.alpha_composite(lay)
    show(fr, gcard("ICMR National Ethical Guidelines: counselling, consent and privacy in genetic testing", CYAN, 1, 32), 940, t, D * 0.35)
    show(fr, gcard("Keep reports confidential; share only with consent", TEALG, 2, 34), 1110, t, D * 0.55)

def sc_case1(fr, t, D):
    dots(fr, 9); show(fr, kicker("Case study from India", CORAL), 260, t, 0.1)
    put(fr, PAPER, 540, 690, 0.72, ease((t - 0.4) / 0.6))
    show(fr, gcard("Two siblings, 8 and 6 years: collodion membrane at birth, fish-like scales", CYAN, None, 32), 1020, t, D * 0.35)
    show(fr, gcard("Out-turned eyelids, heat intolerance", AMBER, None, 34), 1190, t, D * 0.5)
    show(fr, source_tag("Gupta et al., F1000Research 2015;4:446 (Pune & Delhi), CC BY"), 1330, t, D * 0.55)

def sc_case2(fr, t, D):
    dots(fr, 10); show(fr, kicker("Case: an extra finding"), 260, t, 0.1)
    put(fr, karyogram(), 540, 700, 0.62, ease((t - 0.3) / 0.6))
    lay, d = overlay(fr); e = ease((t - D * 0.3) / 0.5)
    d.rounded_rectangle((640, 830, 760, 930), 16, outline=(*AMBER, int(255 * e)), width=6)
    d.text((700, 970), "22q12 dup", font=font("Bold", 30), fill=(*AMBER, int(255 * e)), anchor="mm"); fr.alpha_composite(lay)
    show(fr, gcard("Karyotype: 22q12 duplication in father and both children", AMBER, 1, 33), 1060, t, D * 0.4)
    show(fr, gcard("No features of cat eye syndrome; relevance unclear", LAV, 2, 33), 1210, t, D * 0.55)
    show(fr, body("Karyogram is an illustration", 26, MUTED), 1360, t, D * 0.6)

def sc_case3(fr, t, D):
    dots(fr, 11); show(fr, kicker("Case: the exome answer"), 260, t, 0.1)
    ped(fr, t, 0.3, case_at(420), CASE[1], CASE[2], labels=[("f", "carrier", AMBER), ("m", "carrier", AMBER), ("p", "pregnancy", MUTED)])
    show(fr, gcard("Exome: homozygous TGM1 variant; parents carriers", CYAN, 1, 34), 880, t, D * 0.3)
    show(fr, gcard("Diagnosis: lamellar ichthyosis (autosomal recessive)", TEALG, 2, 34), 1030, t, D * 0.45)
    show(fr, gcard("Isotretinoin: marked improvement over 2 years", LAV, 3, 34), 1180, t, D * 0.6)

def sc_case4(fr, t, D):
    dots(fr, 12); show(fr, kicker("Why counselling mattered"), 260, t, 0.1)
    show(fr, gcard("Mother pregnant again: 25% risk in each pregnancy", CORAL, 1, 34), 340, t, 0.3)
    show(fr, gcard("Prenatal testing planned using this result", AMBER, 2, 34), 490, t, D * 0.25)
    show(fr, gcard("Explaining the uncertain 22q12 duplication", LAV, 3, 34), 640, t, D * 0.45)
    fire("pop", 0.3); fire("pop", D * 0.25); fire("pop", D * 0.45)
    ped(fr, t, D * 0.55, case_at(950), CASE[1], CASE[2])

sc_lesson = s_cards(13, "Lessons from this case", None,
    [("A correct diagnosis opens new choices for the family", CYAN), ("Prenatal testing: with proper consent and PCPNDT rules", CORAL),
     ("Explaining uncertain findings is part of counselling", AMBER)], size=33)

sc_take = s_cards(14, "Key messages", None,
    [("Counselling and written consent before every genetic test", CYAN), ("Decide on secondary findings and data sharing upfront", AMBER),
     ("Care with predictive testing in children", LAV), ("After the report: recurrence risk, cascade testing, support", TEALG), ("Refer to a genetic counsellor when needed", CORAL)], size=32)

SC = [(film(sc0), "doc"), (film(sc_what), "doc"), (film(sc_pre), "doc"), (film(sc_consent), "doc"), (film(sc_family), "doc"),
      (film(sc_minor), "doc"), (film(sc_prenatal), "doc"), (film(sc_post), "doc"), (film(sc_privacy), "doc"), (film(sc_case1), "doc"),
      (film(sc_case2), "doc"), (film(sc_case3), "doc"), (film(sc_case4), "doc"), (film(sc_lesson), "doc"), (film(sc_take), "doc"),
      (close_scene("Who counsels before genetic tests?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si, (fn, bg) in enumerate(SC):
            d = 16 if si < len(SC) - 1 else 33; p = .95 if si else 0.125; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((300, 533)))
        s = Image.new("RGB", (300 * 6, 533 * 3), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 6) * 300, (i // 6) * 533))
        s.save("sheet_g005.png")
    else: run(SC, "/tmp/g005_", "Genetics_Ep05_Counselling_Consent_Hindi.mp4", max_sec=480)
