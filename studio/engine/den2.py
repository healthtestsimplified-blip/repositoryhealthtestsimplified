"""Awareness Reel: Can dengue happen again? (Bengali, <= 3:00)."""
import sys
from cbc_cartoon import run
from gen_series import *
from hts_close import close_scene

TOT[0] = 6
TOPIC = "DENGUE  •  AWARENESS"
SRC_IM = "Immunize.org: Ask the experts, dengue"
SRC_GV = "Gavi VaccinesWork: why a second dengue infection can be deadlier"
SRC_CDC = "CDC: Manage dengue"

def four(fr, y, t, tin, hit=0):
    lay, d = overlay(fr)
    cols = (CYAN, AMBER, LAV, CORAL)
    for i in range(4):
        e = ease((t - tin - i * 0.25) / 0.5); a = int(255 * e)
        cx = X0 + 110 + i * (TW - 220) // 3
        d.ellipse((cx - 95, y - 95, cx + 95, y + 95), fill=(*cols[i], int(60 * e)), outline=(*cols[i], a), width=6)
        d.text((cx, y - 15), f"DENV-{i+1}", font=font("Bold", 34), fill=(*WHITE, a), anchor="mm")
        d.text((cx, y + 35), "type", font=font("Medium", 26), fill=(*SOFT, a), anchor="mm")
    fr.alpha_composite(lay)

def sc0(fr, t, D):
    show(fr, kicker("Dengue  •  Awareness", CYAN), 330, t, 0.1)
    show(fr, headline("Can dengue", 80), 410, t, -1)
    show(fr, headline("happen again?", 80, (249, 196, 120)), 510, t, -1)
    four(fr, 820, t, 0.4)
    show(fr, callout("Yes. Up to 4 times in a lifetime.", CORAL, 40), 1100, t, D * 0.45); fire("ding", D * 0.45)
    show(fr, source_tag(SRC_IM), 1250, t, D * 0.55)

def sc_types(fr, t, D):
    dots(fr, 1); show(fr, kicker("Why it can happen again"), 260, t, 0.1)
    four(fr, 440, t, 0.3)
    show(fr, gcard("There are 4 types of dengue virus", CYAN, 1, 34), 640, t, D * 0.25)
    show(fr, gcard("After one infection: long protection against THAT type", TEALG, 2, 32), 790, t, D * 0.38)
    show(fr, gcard("Against the other 3 types: protection can fade in about 2 months", CORAL, 3, 32), 960, t, D * 0.52)
    show(fr, source_tag(SRC_IM + "; " + SRC_GV), 1140, t, D * 0.64)
    for k in (0.25, 0.38, 0.52): fire("pop", D * k)

def sc_second(fr, t, D):
    dots(fr, 2); show(fr, kicker("The second time is riskier"), 260, t, 0.1)
    show(fr, headline("Second infection: most likely to turn severe", 46), 330, t, 0.3)
    show(fr, gcard("Old antibodies stick to the new type but cannot stop it", AMBER, 1, 32), 470, t, D * 0.25)
    show(fr, gcard("They can even help the virus enter immune cells and multiply", CORAL, 2, 32), 640, t, D * 0.4)
    show(fr, gcard("A very strong immune reaction can cause bleeding", LAV, 3, 33), 810, t, D * 0.55)
    show(fr, source_tag(SRC_IM + "; " + SRC_GV), 970, t, D * 0.65)
    for k in (0.25, 0.4, 0.55): fire("pop", D * k)

sc_warn = s_cards(3, "Warning signs: go to hospital at once", None,
    [("Belly pain or tenderness", CORAL), ("Vomiting 3 or more times in 24 hours", AMBER), ("Bleeding from nose or gums", CORAL),
     ("Vomiting blood, or blood in the stool", AMBER), ("Very tired, restless or irritable", LAV)],
    lambda fr, t, D, y: (show(fr, callout("Often 24-48 hours AFTER the fever goes away", CYAN, 32), y + 40, t, D * 0.7),
                         show(fr, source_tag(SRC_CDC), y + 160, t, D * 0.75)), size=32)

def sc_care(fr, t, D):
    dots(fr, 4); show(fr, kicker("If you have dengue"), 260, t, 0.1)
    show(fr, gcard("Rest, and drink plenty of fluids", TEALG, 1, 34), 340, t, 0.3)
    show(fr, gcard("For fever and pain: paracetamol", CYAN, 2, 34), 490, t, D * 0.22)
    show(fr, gcard("Avoid aspirin and ibuprofen", CORAL, 3, 34), 640, t, D * 0.34)
    show(fr, gcard("Had dengue before? Tell your doctor", AMBER, 4, 34), 790, t, D * 0.46)
    show(fr, gcard("Stop mosquito bites, every season", LAV, 5, 34), 940, t, D * 0.58)
    show(fr, source_tag(SRC_CDC), 1100, t, D * 0.68)
    for k in (0.22, 0.34, 0.46, 0.58): fire("pop", D * k)

SC = [(film(sc0), "doc"), (film(sc_types), "doc"), (film(sc_second), "doc"), (film(sc_warn), "doc"), (film(sc_care), "doc"),
      (close_scene("Have you had dengue before?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si, (fn, bg) in enumerate(SC):
            d = 16 if si < len(SC) - 1 else 33; p = .95 if si else 0.01; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((300, 533)))
        s = Image.new("RGB", (300 * 6, 533), "white")
        for i, im in enumerate(ims): s.paste(im, (i * 300, 0))
        s.save("/tmp/sheet_den2.png")
    else: run(SC, "/tmp/den2bn_", "Dengue_Again_Bengali.mp4", max_sec=180)
