"""BRCA1/BRCA2 genetic test, short public video, realistic documentary style."""
import math, sys, random
from cbc_cartoon import run
from real_style import *
from hts_close import close_scene
from g004 import ped

TOPIC = "BRCA1 / BRCA2 TEST"
NCH = 7
SEQ = "CCTTGGACCCAGAGGTTCTTTG"
CHR17 = chromosome_sprite("Chromosome 17", 0.6, "BRCA1 (17q21)")
CHR13 = chromosome_sprite("Chromosome 13", 0.45, "BRCA2 (13q13)")

def dots(fr, n): fr.alpha_composite(chapter(n, NCH), (0, 110))

def cards(fr, t, D, items, y0=340, size=35, gap=145, t0=0.1, step=0.11):
    for i, (txt, c) in enumerate(items):
        fire("pop", D * (t0 + step * i)); show(fr, gcard(txt, c, i + 1, size), y0 + i * gap, t, D * (t0 + step * i))

def riskbars(fr, x, y, t, tin, title, rows, vmax=70):
    panel(fr, x, y, TW, 110 + 100 * len(rows), title)
    lay, d = overlay(fr); e = ease((t - tin) / 1.0)
    for i, (lab, v, txt, c) in enumerate(rows):
        yy = y + 90 + i * 100
        d.text((x + 24, yy + 23), lab, font=font("Medium", 30), fill=SOFT, anchor="lm")
        L = max(14, (TW - 470) * v / vmax * e)
        d.rounded_rectangle((x + 260, yy, x + 260 + L, yy + 46), 23, fill=c)
        d.text((x + 276 + L, yy + 23), txt, font=font("Bold", 32), fill=WHITE, anchor="lm")
    fr.alpha_composite(lay)

FAM = ({"a": (330, 0, "m", ""), "b": (530, 0, "f", "a"),
        "c": (200, 220, "f", "a"), "cs": (360, 220, "m", ""), "e": (620, 220, "m", ""), "g": (840, 220, "f", "a"),
        "h": (200, 440, "f", "p"), "i": (380, 440, "m", "")},
       [("a", "b", 0), ("c", "cs", 0)], [(("a", "b"), ["c", "e", "g"]), (("c", "cs"), ["h", "i"])])
def fam_at(dy): return {k: (x, y + dy, s, f) for k, (x, y, s, f) in FAM[0].items()}

# ---------------- scenes ----------------
def s_hook(fr, t, D):
    show(fr, kicker("Genetic test explained", CYAN), 250, t, 0.1)
    type_on(fr, "BRCA1 / BRCA2 test", 310, t, 0.3, 74)
    if t > D * 0.25: type_on(fr, "Can cancer risk run in families?", 420, t, D * 0.25, 44, AMBER)
    ped(fr, t, D * 0.35, {k: (x * 0.75 + 20, y, s, f) for k, (x, y, s, f) in fam_at(720).items()}, FAM[1], FAM[2], s=34, step=0.3)
    show(fr, callout("Watch till the end", CORAL, 38), 1600, t, D * 0.8)

def s_what(fr, t, D):
    dots(fr, 1); show(fr, kicker("What are BRCA genes?"), 260, t, 0.1)
    put(fr, CHR17, 300, 720, 0.62, ease((t - 0.3) / 0.6)); put(fr, CHR13, 780, 720, 0.62, ease((t - 0.6) / 0.6))
    show(fr, gcard("Normal genes in everyone: they repair DNA damage and protect against cancer", TEALG, 1, 33), 1040, t, D * 0.25)
    show(fr, gcard("A harmful change weakens this protection", CORAL, 2, 34), 1200, t, D * 0.4)
    show(fr, gcard("Inherited from mother or father; each child has a 50% chance", AMBER, 3, 33), 1345, t, D * 0.6)
    fire("pop", D * 0.25); fire("pop", D * 0.4); fire("pop", D * 0.6)

def s_risk(fr, t, D):
    dots(fr, 2); show(fr, kicker("How much risk? (lifetime, women)"), 260, t, 0.1)
    riskbars(fr, X0, 330, t, 0.3, "Breast cancer", [("General", 13, "~13%", (120, 140, 170)), ("BRCA1 / 2", 62, "> 60%", CORAL)])
    riskbars(fr, X0, 690, t, D * 0.3, "Ovarian cancer", [("General", 1.1, "~1%", (120, 140, 170)), ("BRCA1", 58, "39-58%", CORAL), ("BRCA2", 29, "13-29%", AMBER)])
    show(fr, gcard("Men: higher risk of breast, prostate and pancreatic cancer", CYAN, None, 33), 1150, t, D * 0.6)
    show(fr, source_tag("US National Cancer Institute, BRCA gene changes fact sheet"), 1300, t, D * 0.65)

def s_who(fr, t, D):
    dots(fr, 3); show(fr, kicker("Who should consider testing?"), 260, t, 0.1)
    cards(fr, t, D, [("Breast cancer at age 50 or younger", CORAL), ("Ovarian cancer at any age", CORAL), ("Breast cancer in a man", AMBER),
                     ("Pancreatic or advanced prostate cancer", AMBER), ("Known BRCA change in the family", LAV)], 330, 34, 140, 0.06, 0.1)
    show(fr, callout("Decide with a doctor or genetic counsellor", TEALG, 36), 1060, t, D * 0.7)

def s_test(fr, t, D):
    dots(fr, 4); show(fr, kicker("The test"), 260, t, 0.1)
    put(fr, tube_sprite((149, 117, 205), "EDTA"), 330, 640, 1.0, ease((t - 0.3) / 0.5))
    lay, d = overlay(fr); e = ease((t - 0.5) / 0.5)
    d.text((330, 950), "Blood", font=font("Bold", 34), fill=(*SOFT, int(255 * e)), anchor="mm")
    d.text((750, 950), "or saliva", font=font("Bold", 34), fill=(*SOFT, int(255 * e)), anchor="mm")
    d.rounded_rectangle((680, 520, 820, 840), 30, fill=(230, 235, 242, int(255 * e))); d.rectangle((690, 640, 810, 820), fill=(205, 225, 245, int(255 * e)))
    fr.alpha_composite(lay)
    show(fr, gcard("Genetic counselling before the test and after the report", TEALG, 1, 34), 990, t, D * 0.35)
    show(fr, gcard("Usually not done in children under 18", AMBER, 2, 34), 1140, t, D * 0.55)
    fire("pop", D * 0.35); fire("pop", D * 0.55)

def s_result(fr, t, D):
    dots(fr, 5); show(fr, kicker("Three possible results"), 260, t, 0.1)
    if t > 0.3: sanger(fr, X0, 330, TW, 300, t, 0.3, SEQ, (4, "T"), title="DNA sequence (illustration)")
    cards(fr, t, D, [("Positive: higher risk, but cancer is not certain", CORAL), ("Negative: no harmful change found; usual risk remains", TEALG),
                     ("VUS (uncertain): no big decisions based on it", AMBER)], 690, 33, 160, 0.2, 0.18)

def s_pos(fr, t, D):
    dots(fr, 6); show(fr, kicker("If positive"), 260, t, 0.1)
    cards(fr, t, D, [("Earlier and more frequent screening, e.g. mammography plus MRI", CYAN), ("Preventive surgery options: discussed with a specialist", LAV),
                     ("If cancer is present: can help guide treatment", TEALG)], 340, 33, 165, 0.1, 0.2)
    show(fr, callout("Every decision only with your doctor", AMBER, 36), 900, t, D * 0.72)

def s_family(fr, t, D):
    dots(fr, 7); show(fr, kicker("For the whole family"), 260, t, 0.1)
    P = fam_at(470); ped(fr, t, 0.3, P, FAM[1], FAM[2], s=40, step=0.3)
    show(fr, gcard("Brothers, sisters and children can test for the same change, men too", AMBER, 1, 33), 1040, t, D * 0.45)
    show(fr, callout("Don't fear it: knowing helps prevention", TEALG, 36), 1210, t, D * 0.65); fire("ding", D * 0.65)
    show(fr, body("Family tree shown is an illustration", 26, MUTED), 1340, t, D * 0.7)

SC = [(film(s_hook), "doc"), (film(s_what), "doc"), (film(s_risk), "doc"), (film(s_who), "doc"), (film(s_test), "doc"),
      (film(s_result), "doc"), (film(s_pos), "doc"), (film(s_family), "doc"), (close_scene("Cancer in your family?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si, (fn, bg) in enumerate(SC):
            d = 16 if si < len(SC) - 1 else 33; NOW.update(t=d * .95, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * .95, d); ims.append(fr.convert("RGB").resize((360, 640)))
        s = Image.new("RGB", (360 * 5, 640 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 360, (i // 5) * 640))
        s.save("sheet_brca.png")
    else: run(SC, "/tmp/brca_", "BRCA_Test_Hindi.mp4")
