"""High-End Tests, Ep 1 sales update: Lung Cancer Panel Liquid Biopsy, 12 Gene, on the Suraksha menu (Bengali, <= 3:00)."""
import sys
from cbc_cartoon import run
from gen_series import *
from hts_close import close_scene
from g013 import hbars
from ht001 import stream, SRC_TM, SRC_IA

TOT[0] = 5
TOPIC = "HIGH-END TESTS  •  SALES UPDATE"
NAME = "Lung Cancer Panel Liquid Biopsy, 12 Gene"

def sc0(fr, t, D):
    show(fr, kicker("High-End Tests  •  Sales update", CYAN), 330, t, 0.1)
    show(fr, headline("Liquid lung panel", 74), 410, t, -1)
    show(fr, headline("now on our menu", 54, (249, 196, 120)), 510, t, -1)
    show(fr, gcard(NAME, TEALG, None, 34), 640, t, D * 0.25); fire("pop", D * 0.25)
    stream(fr, 860, t, 0.4)
    show(fr, callout("Builds on High-End Tests Episode 1", CYAN, 34), 1640, t, D * 0.6)

def sc_what(fr, t, D):
    dots(fr, 1); show(fr, kicker("What to say it is"), 260, t, 0.1)
    show(fr, gcard("A blood (plasma) gene test for lung cancer", CYAN, 1, 34), 340, t, 0.3)
    show(fr, gcard("12 cancer genes in one test", TEALG, 2, 34), 490, t, D * 0.2)
    show(fr, gcard("For doctors treating advanced lung cancer", AMBER, 3, 34), 640, t, D * 0.32)
    show(fr, gcard("Before pitching, get from the lab: the 12 genes, blood tube, report time, MRP", CORAL, 4, 32), 790, t, D * 0.44)
    show(fr, gcard("Other cancers: ask about the OncoPro Pan-Cancer Panel (liquid biopsy)", LAV, 5, 32), 980, t, D * 0.58)
    for k in (0.2, 0.32, 0.44, 0.58): fire("pop", D * k)

def sc_when(fr, t, D):
    dots(fr, 2); show(fr, kicker("When doctors use it"), 260, t, 0.1)
    show(fr, gcard("Tissue not enough, or no biopsy possible", TEALG, 1, 34), 340, t, 0.3)
    show(fr, gcard("At diagnosis, alongside tissue", CYAN, 2, 34), 490, t, D * 0.22)
    show(fr, gcard("Cancer growing again on a targeted medicine", AMBER, 3, 34), 640, t, D * 0.34)
    show(fr, source_tag(SRC_IA), 800, t, D * 0.45)
    hbars(fr, 900, [("No tissue", 19, "about 1 in 5", CORAL), ("Agreed with tissue", 97, "97%", TEALG)], t, D * 0.5, 110, 300)
    show(fr, source_tag(SRC_TM), 1130, t, D * 0.6)

def sc_rules(fr, t, D):
    dots(fr, 3); show(fr, kicker("Field rules"), 260, t, 0.1)
    show(fr, gcard("Plasma negative: the next step is a tissue test", CORAL, 1, 33), 340, t, 0.3)
    show(fr, gcard("Never say it replaces a biopsy for diagnosis", AMBER, 2, 33), 490, t, D * 0.22)
    show(fr, gcard("Not a screening test for healthy people", LAV, 3, 34), 640, t, D * 0.34)
    show(fr, gcard("Treatment is always the oncologist's decision", TEALG, 4, 33), 790, t, D * 0.46)
    show(fr, gcard("Ask: \"When tissue is not enough, do you send a plasma gene panel?\"", CYAN, 5, 32), 960, t, D * 0.6)
    for k in (0.22, 0.34, 0.46, 0.6): fire("pop", D * k)

SC = [(film(sc0), "doc"), (film(sc_what), "doc"), (film(sc_when), "doc"), (film(sc_rules), "doc"),
      (close_scene("Which oncologists will you visit first?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si, (fn, bg) in enumerate(SC):
            d = 16 if si < len(SC) - 1 else 33; p = .95 if si else 0.01; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((360, 640)))
        s = Image.new("RGB", (360 * 5, 640), "white")
        for i, im in enumerate(ims): s.paste(im, (i * 360, 0))
        s.save("/tmp/sheet_ht001u.png")
    else: run(SC, "/tmp/ht001ubn_", "HighEnd_Update_Liquid_Lung_Panel_Bengali.mp4", max_sec=180)
