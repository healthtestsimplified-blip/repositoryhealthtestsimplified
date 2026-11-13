"""Cancer Series, Episode 2: Breast cancer (public awareness, Bengali narration; Hindi teaser via hindi_teaser.py c002 5)."""
import sys
from cbc_cartoon import run
from gen_series import *
from hts_close import close_scene
from g013 import hbars

TOT[0] = 9
TOPIC = "CANCER SERIES  •  EPISODE 2"
SRC_IN = "Vemula & Dhakshanamoorthy, Indian J Med Paediatr Oncol 2025 (NCRP)"
SRC_SV = "ICMR-led survival study, Cancer 2024 (17,331 women, 11 registries)"
SRC_ACS = "American Cancer Society: breast cancer signs and symptoms"
SRC_NHM = "National NCD programme: cancer screening operational framework"
SRC_VIC = "Cancer Council Victoria: diagnosing breast cancer"
PINKR = (244, 114, 182)

def ribbon(fr, cx, cy, t, tin, s=1.0):
    """Awareness ribbon drawn with two strokes (illustration)."""
    lay, d = overlay(fr); e = ease((t - tin) / 0.8); a = int(255 * e)
    w = int(34 * s)
    d.line([(cx - 120 * s, cy + 220 * s), (cx + 60 * s, cy - 40 * s), (cx + 40 * s, cy - 150 * s), (cx, cy - 200 * s)], fill=(*PINKR, a), width=w, joint="curve")
    d.line([(cx + 120 * s, cy + 220 * s), (cx - 60 * s, cy - 40 * s), (cx - 40 * s, cy - 150 * s), (cx, cy - 200 * s)], fill=(*(219, 39, 119), a), width=w, joint="curve")
    fr.alpha_composite(lay)

# ---------------- scenes ----------------
def sc0(fr, t, D):
    show(fr, kicker("Cancer Series  •  Episode 2", CYAN), 330, t, 0.1)
    show(fr, headline("Breast cancer", 80), 410, t, -1)
    show(fr, headline("signs, tests, early detection", 50, (249, 196, 120)), 510, t, -1)
    ribbon(fr, 540, 1000, t, 0.3)
    show(fr, callout("The most common cancer in Indian women", PINKR, 34), 1500, t, D * 0.5); fire("whoosh", D * 0.5)

def sc_india(fr, t, D):
    dots(fr, 1); show(fr, kicker("Breast cancer in India"), 260, t, 0.1)
    show(fr, headline("No. 1 cancer in women", 60), 330, t, 0.3)
    hbars(fr, 450, [("Age 15-39", 27.05, "27%", CYAN), ("Age 40-64", 32.3, "32%", PINKR), ("Age 65+", 22.7, "23%", LAV)], t, 0.6, 40, 220)
    show(fr, body("Share of top cancers in women (2024 estimates)", 28, SOFT), 790, t, D * 0.3)
    show(fr, gcard("About 2.3 lakh new cases estimated for 2025", AMBER, None, 33), 870, t, D * 0.4)
    show(fr, gcard("Starts about 10 years earlier than in Western women", CORAL, None, 33), 1020, t, D * 0.52)
    show(fr, gcard("Most are found when already advanced", LAV, None, 33), 1170, t, D * 0.64)
    show(fr, source_tag(SRC_IN), 1320, t, D * 0.72)
    for k in (0.4, 0.52, 0.64): fire("pop", D * k)

def sc_surv(fr, t, D):
    dots(fr, 2); show(fr, kicker("Why early matters"), 260, t, 0.1)
    big = ("66.4%", "of women in India alive 5 years after diagnosis")
    show(fr, headline(big[0], 130, AMBER), 380, t, 0.3)
    show(fr, body(big[1], 34, SOFT), 590, t, 0.4)
    show(fr, gcard("In the USA: more than 90%", CYAN, None, 34), 690, t, D * 0.3)
    show(fr, callout("Found early (local stage): survival 4.4 times higher than when spread", TEALG, 32), 860, t, D * 0.45)
    show(fr, source_tag(SRC_SV), 1050, t, D * 0.6)
    fire("pop", D * 0.3); fire("ding", D * 0.45)

sc_signs = s_cards(3, "Signs to watch", None,
    [("A new lump or thickening in the breast", PINKR), ("Swelling of part or all of the breast", AMBER),
     ("Skin dimpling (like orange peel), redness, flaking", LAV), ("Nipple turning inward, or discharge (not milk)", CYAN),
     ("Swelling under the arm or near the collarbone", TEALG)],
    lambda fr, t, D, y: (show(fr, body("Most lumps are not cancer, but always get checked", 32, SOFT), y + 20, t, D * 0.7),
                         show(fr, source_tag(SRC_ACS), y + 90, t, D * 0.75)), size=31)

def sc_risk(fr, t, D):
    dots(fr, 4); show(fr, kicker("Who has higher risk?"), 260, t, 0.1)
    show(fr, gcard("Family history, especially relatives diagnosed young", PINKR, 1, 32), 340, t, 0.3)
    show(fr, gcard("Inherited gene changes: BRCA1, BRCA2, PALB2, CHEK2", AMBER, 2, 32), 510, t, D * 0.25)
    show(fr, gcard("Rising age", LAV, 3, 34), 680, t, D * 0.4)
    show(fr, callout("Strong family history? Ask your doctor about genetic counselling", TEALG, 31), 840, t, D * 0.55)
    show(fr, source_tag(SRC_IN), 1010, t, D * 0.65)
    fire("pop", D * 0.25); fire("pop", D * 0.4)

def sc_screen(fr, t, D):
    dots(fr, 5); show(fr, kicker("Free screening in India"), 260, t, 0.1)
    show(fr, headline("Clinical breast examination", 54), 330, t, 0.3)
    show(fr, gcard("For women aged 30 to 65", PINKR, 1, 34), 450, t, D * 0.2)
    show(fr, gcard("Once every 5 years", AMBER, 2, 34), 590, t, D * 0.32)
    show(fr, gcard("At the sub-centre or PHC, by the ANM with ASHA", LAV, 3, 33), 730, t, D * 0.44)
    show(fr, gcard("Suspicious finding: surgeon, ultrasound and biopsy", CYAN, 4, 33), 880, t, D * 0.56)
    show(fr, source_tag(SRC_NHM), 1040, t, D * 0.66)
    for k in (0.2, 0.32, 0.44, 0.56): fire("pop", D * k)

def sc_tests(fr, t, D):
    dots(fr, 6); show(fr, kicker("If a change is found: the tests"), 260, t, 0.1)
    show(fr, gcard("Ultrasound: often first for a lump, or under 30", CYAN, 1, 33), 340, t, 0.3)
    show(fr, gcard("Mammogram: low-dose X-ray, finds changes too small to feel", PINKR, 2, 32), 490, t, D * 0.22)
    show(fr, gcard("MRI: for high risk or special cases", LAV, 3, 34), 660, t, D * 0.34)
    show(fr, gcard("Biopsy: the only test that confirms cancer", AMBER, 4, 34), 800, t, D * 0.46)
    show(fr, callout("8 in 10 women who have a biopsy do NOT have cancer", TEALG, 32), 960, t, D * 0.6)
    show(fr, source_tag(SRC_VIC + "; WCI: diagnosis"), 1120, t, D * 0.7)

def sc_recep(fr, t, D):
    dots(fr, 7); show(fr, kicker("Tests on the cancer guide treatment"), 260, t, 0.1)
    hbars(fr, 360, [("ER / PR positive", 75, "about 70-80%", PINKR), ("HER2 positive", 17.5, "about 15-20%", AMBER), ("Triple negative", 15, "about 10-20%", LAV)], t, 0.4, 100, 300)
    show(fr, gcard("ER/PR positive: hormone therapy", PINKR, 1, 34), 700, t, D * 0.35)
    show(fr, gcard("HER2 positive: targeted therapy", AMBER, 2, 34), 840, t, D * 0.47)
    show(fr, gcard("Triple negative: usually chemotherapy", LAV, 3, 34), 980, t, D * 0.59)
    show(fr, source_tag(SRC_VIC), 1130, t, D * 0.68)
    for k in (0.35, 0.47, 0.59): fire("pop", D * k)

sc_take = s_cards(8, "Remember", None,
    [("Know what is normal for your body", PINKR), ("Any change: see a doctor quickly", AMBER),
     ("From 30: clinical breast examination", CYAN), ("Family history: ask about counselling", TEALG)],
    lambda fr, t, D, y: show(fr, body("Share this with the women in your family", 32, SOFT), y + 20, t, D * 0.7), size=34)

SC = [(film(sc0), "doc"), (film(sc_india), "doc"), (film(sc_surv), "doc"), (film(sc_signs), "doc"), (film(sc_risk), "doc"),
      (film(sc_screen), "doc"), (film(sc_tests), "doc"), (film(sc_recep), "doc"), (film(sc_take), "doc"),
      (close_scene("Who will you share this with?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si, (fn, bg) in enumerate(SC):
            d = 16 if si < len(SC) - 1 else 33; p = .95 if si else 0.01; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((300, 533)))
        s = Image.new("RGB", (300 * 5, 533 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 300, (i // 5) * 533))
        s.save("/tmp/sheet_c002.png")
    else: run(SC, "/tmp/c002bn_", "Cancer_Ep02_Breast_Cancer_Bengali.mp4", max_sec=480)
