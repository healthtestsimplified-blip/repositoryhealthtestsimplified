"""Cancer Series, Episode 1: Why cancer happens, and the types of cancer (public awareness, Bengali narration; Hindi teaser via hindi_teaser.py c001 5)."""
import sys, random, math
from cbc_cartoon import run
from gen_series import *
from hts_close import close_scene
from g013 import hbars

TOT[0] = 9
TOPIC = "CANCER SERIES  •  EPISODE 1"
SRC_WHO = "WHO cancer fact sheet"
SRC_IARC = "WHO/IARC news release, 3 February 2026"
SRC_IN = "Sathishkumar et al., Indian J Med Res 2022 (ICMR-NCRP estimates)"
SRC_CRUK = "Cancer Research UK: inherited genes and cancer"
SRC_WCD = "World Cancer Day (UICC): what is cancer"

def cells(fr, y, t, tin, n_bad=None):
    """A sheet of normal cells; a few turn abnormal and multiply (illustration)."""
    lay, d = overlay(fr); e = ease((t - tin) / 0.6); a = int(255 * e)
    cols, rows, r = 9, 5, 44
    grow = max(0.0, min(1.0, (t - tin - 0.8) / 3.0))
    bad = n_bad if n_bad is not None else int(1 + grow * 14)
    order = sorted(range(cols * rows), key=lambda k: abs(k % cols - 6) + abs(k // cols - 2))
    badset = set(order[:bad])
    for k in range(cols * rows):
        cx = X0 + 60 + (k % cols) * 102 + (k // cols % 2) * 51; cy = y + 60 + (k // cols) * 96
        b = k in badset; c = CORAL if b else TEALG
        rr = r + (6 if b else 0)
        d.ellipse((cx - rr, cy - rr * 0.85, cx + rr, cy + rr * 0.85), fill=(*c, int((150 if b else 80) * e)), outline=(*c, a), width=3)
        d.ellipse((cx - 12, cy - 10, cx + 12, cy + 10), fill=(*WHITE, int(200 * e)))
    d.text((X0, y + 560), "Normal cells", font=font("Bold", 30), fill=(*TEALG, a), anchor="lm")
    d.text((X0 + TW, y + 560), "Abnormal cells multiplying", font=font("Bold", 30), fill=(*CORAL, a), anchor="rm")
    d.text((540, y + 610), "Illustration", font=font("Medium", 26), fill=(*SOFT, int(200 * e)), anchor="mm")
    fr.alpha_composite(lay)

# ---------------- scenes ----------------
def sc0(fr, t, D):
    show(fr, kicker("Cancer Series  •  Episode 1", CYAN), 330, t, 0.1)
    show(fr, headline("Why does cancer", 72), 410, t, -1)
    show(fr, headline("happen?", 72, (249, 196, 120)), 500, t, -1)
    if t > D * 0.3: type_on(fr, "What cancer is, its causes and its types", 610, t, D * 0.3, 38, AMBER)
    cells(fr, 720, t, 0.4)
    show(fr, callout("Simple facts, from WHO and ICMR", CYAN, 34), 1640, t, D * 0.6); fire("whoosh", D * 0.6)

def sc_what(fr, t, D):
    dots(fr, 1); show(fr, kicker("What is cancer?"), 260, t, 0.1)
    cells(fr, 320, t, 0.3)
    show(fr, gcard("Abnormal cells grow beyond their usual limits", CORAL, 1, 33), 1000, t, D * 0.3)
    show(fr, gcard("They can invade nearby tissue", AMBER, 2, 34), 1150, t, D * 0.42)
    show(fr, gcard("And spread to other organs (metastasis)", LAV, 3, 33), 1290, t, D * 0.54)
    show(fr, source_tag(SRC_WHO), 1440, t, D * 0.64)
    for k in (0.3, 0.42, 0.54): fire("pop", D * k)

def sc_why(fr, t, D):
    dots(fr, 2); show(fr, kicker("Why does it happen?"), 260, t, 0.1)
    show(fr, headline("Changes in a cell's genes, step by step", 46), 330, t, 0.3)
    show(fr, gcard("Your own genetic factors, plus outside agents:", CYAN, None, 33), 470, t, D * 0.18)
    show(fr, gcard("Physical: UV rays and radiation", AMBER, 1, 34), 620, t, D * 0.28)
    show(fr, gcard("Chemical: tobacco smoke, alcohol, aflatoxin, arsenic, asbestos", CORAL, 2, 32), 760, t, D * 0.4)
    show(fr, gcard("Biological: some viruses, bacteria and parasites", LAV, 3, 33), 930, t, D * 0.52)
    show(fr, gcard("Risk rises with age", TEALG, 4, 34), 1080, t, D * 0.64)
    show(fr, source_tag(SRC_WHO), 1230, t, D * 0.72)
    for k in (0.28, 0.4, 0.52, 0.64): fire("pop", D * k)

def sc_prev(fr, t, D):
    dots(fr, 3); show(fr, kicker("Good news: much can be prevented"), 260, t, 0.1)
    show(fr, headline("About 4 in 10 cancers are preventable", 46), 330, t, 0.3)
    hbars(fr, 460, [("Tobacco", 15, "15%", CORAL), ("Infections", 10, "10%", AMBER), ("Alcohol", 3, "3%", LAV)], t, 0.6, 20, 260)
    show(fr, gcard("Infections: HPV, hepatitis B and C, H. pylori, EBV", CYAN, None, 32), 790, t, D * 0.45)
    show(fr, gcard("Also: unhealthy diet, inactivity, air pollution", TEALG, None, 33), 940, t, D * 0.56)
    show(fr, source_tag(SRC_IARC + "; " + SRC_WHO), 1100, t, D * 0.66)
    fire("pop", D * 0.45); fire("pop", D * 0.56)

def sc_inh(fr, t, D):
    dots(fr, 4); show(fr, kicker("Is it in the family?"), 260, t, 0.1)
    show(fr, headline("Up to 12 in 100 cancers", 56), 330, t, 0.3)
    show(fr, body("are linked to an inherited gene change", 38, SOFT), 420, t, 0.4)
    show(fr, gcard("Examples: BRCA1 and BRCA2 (breast, ovary, prostate, pancreas)", AMBER, 1, 32), 520, t, D * 0.3)
    show(fr, gcard("Lynch syndrome (mainly bowel cancer)", LAV, 2, 33), 690, t, D * 0.42)
    show(fr, callout("Most cancers are NOT inherited", TEALG, 36), 860, t, D * 0.56)
    show(fr, source_tag(SRC_CRUK), 1010, t, D * 0.66)
    fire("pop", D * 0.3); fire("pop", D * 0.42)

def sc_india(fr, t, D):
    dots(fr, 5); show(fr, kicker("Cancer in India"), 260, t, 0.1)
    show(fr, headline("About 14.6 lakh new cases (2022)", 50), 330, t, 0.3)
    show(fr, gcard("About 1 in 9 people may get cancer in their lifetime", CORAL, 1, 32), 460, t, D * 0.2)
    show(fr, gcard("Men: lung cancer is the most common", CYAN, 2, 33), 630, t, D * 0.32)
    show(fr, gcard("Women: breast cancer is the most common", LAV, 3, 33), 780, t, D * 0.44)
    show(fr, gcard("Children: lymphoid leukaemia is the most common", AMBER, 4, 32), 930, t, D * 0.56)
    show(fr, source_tag(SRC_IN), 1090, t, D * 0.66)
    for k in (0.2, 0.32, 0.44, 0.56): fire("pop", D * k)

sc_types = s_cards(6, "The main types of cancer", None,
    [("Carcinoma: lining cells (breast, lung, prostate, colon)", CORAL), ("Sarcoma: bone and soft tissue", AMBER),
     ("Leukaemia: blood cells and bone marrow", LAV), ("Lymphoma and myeloma: immune cells", CYAN),
     ("Brain and spinal cord tumours", TEALG)],
    lambda fr, t, D, y: show(fr, source_tag(SRC_WCD), y + 20, t, D * 0.7), size=31)

def sc_early(fr, t, D):
    dots(fr, 7); show(fr, kicker("Why early detection matters"), 260, t, 0.1)
    show(fr, headline("Many cancers can be cured if found early", 46), 330, t, 0.3)
    show(fr, gcard("Early diagnosis: notice symptoms, see a doctor quickly", TEALG, 1, 32), 470, t, D * 0.25)
    show(fr, gcard("Screening: tests that find cancer or pre-cancer before symptoms", CYAN, 2, 32), 640, t, D * 0.38)
    show(fr, gcard("Your doctor decides which tests you need", AMBER, 3, 33), 810, t, D * 0.5)
    show(fr, source_tag(SRC_WHO), 970, t, D * 0.6)
    fire("pop", D * 0.25); fire("pop", D * 0.38); fire("pop", D * 0.5)

sc_next = s_cards(8, "Coming next in this series", None,
    [("One cancer at a time", CYAN), ("Warning signs to watch", CORAL), ("Tests that help find it early", TEALG),
     ("How to lower your risk", AMBER)],
    lambda fr, t, D, y: show(fr, body("Follow us so you don't miss an episode", 32, SOFT), y + 20, t, D * 0.7), size=34)

SC = [(film(sc0), "doc"), (film(sc_what), "doc"), (film(sc_why), "doc"), (film(sc_prev), "doc"), (film(sc_inh), "doc"),
      (film(sc_india), "doc"), (film(sc_types), "doc"), (film(sc_early), "doc"), (film(sc_next), "doc"),
      (close_scene("Which fact surprised you most?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si, (fn, bg) in enumerate(SC):
            d = 16 if si < len(SC) - 1 else 33; p = .95 if si else 0.01; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((300, 533)))
        s = Image.new("RGB", (300 * 5, 533 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 300, (i // 5) * 533))
        s.save("/tmp/sheet_c001.png")
    else: run(SC, "/tmp/c001bn_", "Cancer_Ep01_Why_Cancer_Happens_Bengali.mp4", max_sec=480)
