"""Genetics Clinical Series, Episode 4: Inheritance patterns and the 3-generation pedigree."""
import sys
from cbc_cartoon import run
from gen_series import *
from hts_close import close_scene

TOT[0] = 14
TOPIC = "GENETICS SERIES  •  EPISODE 4"
PAPER = paper_sprite(["Congenital leptin receptor", "deficiency: a novel LEPR", "mutation in an Indian family"], "J Pediatr Endocrinol Diabetes, 2023")

def ped(fr, t, tin, P, couples, sibs, s=40, col=SOFT, aff=CORAL, gen=None, step=0.25, labels=None):
    """Pedigree: P = {id: (x, y, sex 'm'/'f', flags)} flags may include a(ffected) c(arrier) d(eceased) p(roband).
    couples = [(a, b, consang)], sibs = [((a, b), [children])]. Individuals fade in by generation (y)."""
    lay, d = overlay(fr)
    ys = sorted({v[1] for v in P.values()})
    def alpha(y): return int(255 * ease((t - tin - ys.index(y) * step) / 0.5))
    for a, b, cons in couples:
        (xa, ya, *_), (xb, yb, *_) = P[a], P[b]; al = alpha(ya)
        if al <= 0: continue
        x0, x1 = min(xa, xb) + s, max(xa, xb) - s
        if cons:
            d.line((x0, ya - 7, x1, ya - 7), fill=(*col, al), width=4); d.line((x0, ya + 7, x1, ya + 7), fill=(*col, al), width=4)
        else: d.line((x0, ya, x1, ya), fill=(*col, al), width=4)
    for (a, b), kids in sibs:
        (xa, ya, *_), (xb, yb, *_) = P[a], P[b]; ky = P[kids[0]][1]; al = alpha(ky)
        if al <= 0: continue
        mx = (xa + xb) / 2; mid = (ya + ky) / 2
        d.line((mx, ya, mx, mid), fill=(*col, al), width=4)
        xs = [P[k][0] for k in kids]
        d.line((min(xs + [mx]), mid, max(xs + [mx]), mid), fill=(*col, al), width=4)
        for k in kids: d.line((P[k][0], mid, P[k][0], ky - s), fill=(*col, al), width=4)
    for k, (x, y, sex, fl) in P.items():
        al = alpha(y)
        if al <= 0: continue
        fill = (*aff, al) if "a" in fl else (*INK2, al)
        box = (x - s, y - s, x + s, y + s)
        if sex == "m": d.rectangle(box, fill=fill, outline=(*col, al), width=5)
        elif sex == "f": d.ellipse(box, fill=fill, outline=(*col, al), width=5)
        else: d.polygon([(x, y - s * 1.2), (x + s * 1.2, y), (x, y + s * 1.2), (x - s * 1.2, y)], fill=fill, outline=(*col, al))
        if "c" in fl: d.ellipse((x - 10, y - 10, x + 10, y + 10), fill=(*AMBER, al))
        if "d" in fl: d.line((x - s - 14, y + s + 14, x + s + 14, y - s - 14), fill=(*col, al), width=5)
        if "p" in fl:
            d.line((x - s - 60, y + s + 50, x - s - 8, y + s - 2), fill=(*AMBER, al), width=6)
            d.polygon([(x - s - 4, y + s + 2), (x - s - 30, y + s - 2), (x - s - 10, y + s + 24)], fill=(*AMBER, al))
    if gen:
        for i, y in enumerate(ys): d.text((X0 - 10, y), gen[i], font=font("Bold", 30), fill=(*MUTED, alpha(y)), anchor="lm")
    if labels:
        for k, txt, c in labels:
            x, y = P[k][0], P[k][1]; d.text((x, y + s + 34), txt, font=font("Bold", 24), fill=(*c, alpha(y)), anchor="mm")
    fr.alpha_composite(lay)

# pedigree layouts ---------------------------------------------------------
GEN = ["I", "II", "III"]
AD = ({"a": (330, 420, "m", "a"), "b": (530, 420, "f", ""),
       "c": (200, 640, "m", "a"), "cs": (360, 640, "f", ""), "e": (600, 640, "f", ""), "g": (820, 640, "f", "a"), "gs": (980, 640, "m", ""),
       "h": (180, 860, "m", "a"), "i": (380, 860, "f", ""), "j": (820, 860, "f", "a"), "k": (980, 860, "m", "")},
      [("a", "b", 0), ("c", "cs", 0), ("g", "gs", 0)], [(("a", "b"), ["c", "e", "g"]), (("c", "cs"), ["h", "i"]), (("g", "gs"), ["j", "k"])])
AR = ({"a": (380, 440, "m", "c"), "b": (700, 440, "f", "c"),
       "c": (240, 700, "f", ""), "e": (440, 700, "m", "a"), "g": (640, 700, "f", "c"), "h": (840, 700, "m", "a")},
      [("a", "b", 1)], [(("a", "b"), ["c", "e", "g", "h"])])
XLR = ({"a": (330, 420, "m", ""), "b": (530, 420, "f", "c"),
        "c": (200, 640, "m", "a"), "e": (460, 640, "f", "c"), "es": (620, 640, "m", ""), "g": (880, 640, "m", ""),
        "h": (380, 860, "m", "a"), "i": (560, 860, "f", ""), "j": (740, 860, "m", "")},
       [("a", "b", 0), ("e", "es", 0)], [(("a", "b"), ["c", "e", "g"]), (("e", "es"), ["h", "i", "j"])])
MITO = ({"a": (330, 420, "m", ""), "b": (530, 420, "f", "a"),
         "c": (220, 640, "m", "a"), "cs": (380, 640, "f", ""), "e": (660, 640, "f", "a"), "es": (840, 640, "m", ""),
         "h": (220, 860, "m", ""), "i": (380, 860, "f", ""), "j": (660, 860, "m", "a"), "k": (840, 860, "f", "a")},
        [("a", "b", 0), ("c", "cs", 0), ("e", "es", 0)], [(("a", "b"), ["c", "e"]), (("c", "cs"), ["h", "i"]), (("e", "es"), ["j", "k"])])
CASE = ({"f": (390, 480, "m", "c"), "m": (690, 480, "f", "c"),
         "b1": (180, 760, "m", "ad"), "p": (360, 760, "f", "ap"), "s1": (540, 760, "f", "c"), "s2": (720, 760, "f", ""), "b2": (900, 760, "m", "a")},
        [("f", "m", 1)], [(("f", "m"), ["b1", "p", "s1", "s2", "b2"])])

def at_y(P, dy):
    return {k: (x, y + dy, sx, fl) for k, (x, y, sx, fl) in P.items()}

# ---------------- scenes ----------------
def sc0(fr, t, D):
    show(fr, kicker("Genetics Clinical Series  •  Episode 4", CYAN), 330, t, 0.1)
    type_on(fr, "Inheritance patterns", 410, t, 0.4, 70)
    if t > D * 0.3: type_on(fr, "and the 3-generation pedigree", 510, t, D * 0.3, 46, AMBER)
    P, c, s = AD; ped(fr, t, D * 0.35, at_y({k: (x * 0.8 + 20, y, sx, fl) for k, (x, y, sx, fl) in P.items()}, 300), c, s, s=32, step=0.3)
    show(fr, callout("For doctors and healthcare teams  •  with a published Indian case", CYAN, 34), 1640, t, D * 0.6); fire("whoosh", D * 0.6)

def sc_fh(fr, t, D):
    dots(fr, 1); show(fr, kicker("Family history"), 260, t, 0.1)
    show(fr, headline("The cheapest, fastest genetic test", 58), 320, t, 0.3)
    cards = [("Generation I: grandparents (both sides)", LAV), ("Generation II: parents, uncles, aunts", AMBER), ("Generation III: patient, siblings, cousins, children", CYAN)]
    for i, (txt, c) in enumerate(cards):
        fire("pop", D * (0.15 + 0.15 * i)); show(fr, gcard(txt, c, i + 1, 34), 480 + i * 150, t, D * (0.15 + 0.15 * i))
    P, c, s = AR; ped(fr, t, D * 0.55, at_y(P, 620), c, s, gen=["I", "II"])

def sc_symbols(fr, t, D):
    dots(fr, 2); show(fr, kicker("Pedigree symbols (standard notation)"), 260, t, 0.1)
    items = [("m", "", "Male"), ("f", "", "Female"), ("u", "", "Sex unknown"), ("m", "a", "Affected"), ("f", "c", "Carrier"), ("m", "d", "Deceased"), ("f", "ap", "Proband (patient)")]
    for i, (sx, fl, lab) in enumerate(items):
        tin = D * (0.05 + 0.08 * i); col, row = i % 2, i // 2
        x = 200 + col * 460; y = 400 + row * 170
        ped(fr, t, tin, {"x": (x, y, sx, fl)}, [], [], s=44)
        lay, d = overlay(fr); e = ease((t - tin) / 0.5)
        d.text((x + 90, y), lab, font=font("Medium", 32), fill=(*SOFT, int(255 * e)), anchor="lm"); fr.alpha_composite(lay)
    tin = D * 0.65
    ped(fr, t, tin, {"a": (200, 1130, "m", ""), "b": (420, 1130, "f", "")}, [("a", "b", 1)], [], s=40)
    lay, d = overlay(fr); e = ease((t - tin) / 0.5)
    d.text((500, 1130), "Double line: consanguinity", font=font("Medium", 32), fill=(*SOFT, int(255 * e)), anchor="lm"); fr.alpha_composite(lay)
    show(fr, source_tag("NSGC standardized pedigree nomenclature (Bennett et al., J Genet Couns 2008; updated 2022)"), 1260, t, D * 0.75)

sc_ask = s_cards(3, "What to ask", None,
    [("Age when the illness started", CYAN), ("Age and cause of death", LAV), ("Miscarriages, stillbirths, deaths in infancy", CORAL),
     ("Consanguineous marriage", AMBER), ("Similar illness in the family", TEALG)], size=34)

def sc_ad(fr, t, D):
    dots(fr, 4); show(fr, kicker("Autosomal dominant", CORAL), 260, t, 0.1)
    P, c, s = AD; ped(fr, t, 0.3, P, c, s, gen=GEN)
    show(fr, gcard("Affected in every generation; males and females equally", CORAL, 1, 33), 1000, t, D * 0.4)
    show(fr, gcard("Father-to-son transmission possible", AMBER, 2, 34), 1145, t, D * 0.52)
    show(fr, callout("Each child of an affected parent: 50% risk", AMBER, 36), 1300, t, D * 0.65); fire("ding", D * 0.65)

sc_adcav = s_cards(5, "Autosomal dominant: watch out for", None,
    [("Reduced penetrance: can seem to skip a generation", AMBER), ("Variable expressivity: different symptoms in one family", LAV),
     ("De novo: no one else in the family affected", CYAN)], lambda fr, t, D, y: ped(fr, t, D * 0.55, at_y(AD[0], y - 280), AD[1], AD[2], s=34))

def sc_ar(fr, t, D):
    dots(fr, 6); show(fr, kicker("Autosomal recessive", AMBER), 260, t, 0.1)
    P, c, s = AR; ped(fr, t, 0.3, at_y(P, -60), c, s, gen=["I", "II"])
    lay, d = overlay(fr); e = ease((t - D * 0.35) / 1.0)
    segs = [(0.25, CORAL, "25% affected"), (0.5, AMBER, "50% carrier"), (0.25, TEALG, "25% neither")]; x = X0
    for f, c_, lab in segs:
        w = TW * f * e
        if w > 10: d.rounded_rectangle((x + 3, 800, x + w - 3, 880), 18, fill=c_)
        if e > 0.9: d.text((x + TW * f / 2, 920), lab, font=font("Bold", 30), fill=c_, anchor="mm")
        x += TW * f * e
    d.text((X0, 760), "Each pregnancy, both parents carriers:", font=font("Medium", 30), fill=(*SOFT, int(255 * ease((t - D * 0.35) / 0.5))))
    fr.alpha_composite(lay)
    show(fr, gcard("Usually seen in siblings; parents healthy carriers", AMBER, 1, 34), 1000, t, D * 0.5)
    show(fr, gcard("Consanguinity increases the chance", CORAL, 2, 34), 1150, t, D * 0.65)

def sc_xlr(fr, t, D):
    dots(fr, 7); show(fr, kicker("X-linked recessive", CYAN), 260, t, 0.1)
    P, c, s = XLR; ped(fr, t, 0.3, P, c, s, gen=GEN)
    show(fr, gcard("Mostly males affected, through carrier mothers; never father to son", CYAN, 1, 33), 1000, t, D * 0.4)
    show(fr, gcard("Carrier mother: each son 50% affected, each daughter 50% carrier", AMBER, 2, 33), 1160, t, D * 0.55)
    show(fr, callout("e.g. Duchenne muscular dystrophy, haemophilia", LAV, 34), 1320, t, D * 0.7)

def sc_xld_mito(fr, t, D):
    dots(fr, 8); show(fr, kicker("X-linked dominant & mitochondrial", LAV), 260, t, 0.1)
    show(fr, gcard("X-linked dominant: affected father → all daughters affected, no sons".replace("→", "passes to"), LAV, None, 33), 330, t, 0.3)
    P, c, s = MITO; ped(fr, t, D * 0.3, at_y(P, 180), c, s, gen=GEN)
    show(fr, gcard("Mitochondrial: passed only from the mother, never from the father; severity varies", TEALG, None, 33), 1160, t, D * 0.55)

sc_why = s_cards(9, "Why the pedigree matters", None,
    [("Choosing the right test", CYAN), ("Interpreting a VUS: does it track with disease in the family?", AMBER),
     ("Counselling on recurrence risk", TEALG), ("Cascade testing of relatives", LAV)], size=33)

def sc_case1(fr, t, D):
    dots(fr, 10); show(fr, kicker("Case study from India", CORAL), 260, t, 0.1)
    show(fr, headline("A published case from Mumbai", 58), 320, t, 0.3)
    put(fr, PAPER, 540, 790, 0.76, ease((t - 0.5) / 0.6))
    show(fr, gcard("8-year-old girl: normal birth weight, rapid weight gain from 3-6 months, extreme hunger", CYAN, None, 32), 1130, t, D * 0.35)
    show(fr, gcard("19 kg at 11 months; two bariatric surgeries without benefit", AMBER, None, 33), 1310, t, D * 0.55)
    show(fr, source_tag("Patil et al., J Pediatr Endocrinol Diabetes 2023;3(1):29-33 (Mumbai)"), 1460, t, D * 0.6)

def sc_case2(fr, t, D):
    dots(fr, 11); show(fr, kicker("Case: the pedigree"), 260, t, 0.1)
    P, c, s = CASE; ped(fr, t, 0.3, P, c, s, labels=[("b1", "died ~1.5 y", MUTED), ("p", "proband", AMBER), ("b2", "brother", CORAL)])
    show(fr, gcard("Consanguineous, healthy parents; five children", AMBER, 1, 34), 950, t, D * 0.45)
    show(fr, gcard("Affected brother and sister: both sexes, one generation", CORAL, 2, 34), 1100, t, D * 0.55)
    show(fr, callout("Pattern suggests autosomal recessive", TEALG, 36), 1260, t, D * 0.7); fire("ding", D * 0.7)
    show(fr, body("Birth order of unaffected sisters shown for illustration", 26, MUTED), 1380, t, D * 0.7)

def sc_case3(fr, t, D):
    dots(fr, 12); show(fr, kicker("Case: the genetic answer"), 260, t, 0.1)
    show(fr, gcard("Exome: homozygous LEPR (leptin receptor) variant in affected children", CYAN, 1, 33), 330, t, 0.3)
    P, c, s = CASE; ped(fr, t, D * 0.2, at_y(P, 200), c, s, labels=[("f", "carrier", AMBER), ("m", "carrier", AMBER), ("s1", "carrier", AMBER), ("s2", "non-carrier", TEALG)])
    show(fr, gcard("Parents: heterozygous carriers (Sanger confirmed)", AMBER, 2, 34), 1180, t, D * 0.5)
    show(fr, callout("Diagnosis: congenital leptin receptor deficiency (AR)", TEALG, 34), 1340, t, D * 0.65); fire("ding", D * 0.65)

sc_case4 = s_cards(13, "Lessons from this case", None,
    [("The pedigree pointed to recessive inheritance before any genetic test", CYAN), ("Early genetic testing can avoid long, unsuccessful work-up and treatment", AMBER),
     ("Each future pregnancy: 25% risk; genetic counselling essential", CORAL), ("Carrier testing for relatives", LAV)], size=33)

sc_take = s_cards(14, "Key messages", None,
    [("Draw a 3-generation pedigree in every genetic case", CYAN), ("Ask about consanguinity, miscarriages, infant deaths", AMBER),
     ("The pattern guides the test and the counselling", TEALG), ("Every report with genetic counselling", LAV)], size=33)

SC = [(film(sc0), "doc"), (film(sc_fh), "doc"), (film(sc_symbols), "doc"), (film(sc_ask), "doc"), (film(sc_ad), "doc"),
      (film(sc_adcav), "doc"), (film(sc_ar), "doc"), (film(sc_xlr), "doc"), (film(sc_xld_mito), "doc"), (film(sc_why), "doc"),
      (film(sc_case1), "doc"), (film(sc_case2), "doc"), (film(sc_case3), "doc"), (film(sc_case4), "doc"), (film(sc_take), "doc"),
      (close_scene("Do you draw a pedigree?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si, (fn, bg) in enumerate(SC):
            d = 16 if si < len(SC) - 1 else 33; NOW.update(t=d * .95, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * .95, d); ims.append(fr.convert("RGB").resize((300, 533)))
        s = Image.new("RGB", (300 * 6, 533 * 3), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 6) * 300, (i // 6) * 533))
        s.save("sheet_g004.png")
    else: run(SC, "/tmp/g004_", "Genetics_Ep04_Inheritance_Pedigree_Hindi.mp4", max_sec=480)
