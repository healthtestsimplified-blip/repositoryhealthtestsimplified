"""Genetics Clinical Series, Episode 9: Whole genome sequencing: what it adds."""
import sys, random
from cbc_cartoon import run
from gen_series import *
from hts_close import close_scene

TOT[0] = 12
TOPIC = "GENETICS SERIES  •  EPISODE 9"
PAPER = paper_sprite(["Whole genome sequencing", "finds a novel structural", "variant: X-linked agamma-", "globulinemia family"], "PLoS ONE, 2021 (India)")
EXONS = [(0.05, 0.08), (0.17, 0.19), (0.31, 0.35), (0.46, 0.48), (0.6, 0.63), (0.74, 0.76), (0.88, 0.92)]

def genome_bar(fr, y, t, tin, mode="both"):
    """Long DNA bar: exons (coding) as small blocks; genome reads everything."""
    lay, d = overlay(fr); e = ease((t - tin) / 0.8); a = int(255 * e)
    x0, x1 = X0, X0 + TW
    d.rounded_rectangle((x0, y, x1, y + 70), 20, fill=(60, 75, 100, int(200 * e)))
    for s, f in EXONS:
        d.rectangle((x0 + s * TW, y, x0 + f * TW, y + 70), fill=(*CYAN, a))
    d.text((x0, y + 110), "Exome: only the coding blocks (1-2%)", font=font("Medium", 30), fill=(*CYAN, a), anchor="lm")
    if mode == "both":
        g = ease((t - tin - 1.0) / 1.2)
        d.rounded_rectangle((x0, y + 160, x0 + TW * g, y + 200), 14, fill=(*TEALG, 230))
        d.text((x0, y + 245), "Genome: almost everything", font=font("Medium", 30), fill=(*TEALG, int(255 * g)), anchor="lm")
    fr.alpha_composite(lay)

def depth_tracks(fr, y, t, tin):
    """Read depth along a gene: exome patchy (capture), genome even (illustration)."""
    panel(fr, X0, y, TW, 470, "Read depth along a gene (illustration)")
    lay, d = overlay(fr); p = ease((t - tin) / 1.4); r = random.Random(2)
    for row, (lab, c, patchy) in enumerate((("Exome", CYAN, True), ("Genome", TEALG, False))):
        base = y + 230 + row * 190
        d.text((X0 + 30, base - 100), lab, font=font("Bold", 28), fill=c)
        n = 120
        for i in range(n):
            if i / n > p: break
            u = i / n; inex = any(s <= u <= f for s, f in EXONS)
            if patchy: h = (r.uniform(40, 95) if inex else r.uniform(0, 8))
            else: h = r.uniform(45, 60)
            xx = X0 + 30 + u * (TW - 60)
            d.rectangle((xx, base - h, xx + (TW - 60) / n - 1, base), fill=(*c, 220))
    fr.alpha_composite(lay)

def btk_del(fr, y, t, tin):
    """BTK gene model with exons; deletion removes exons 3-5; read pile-up with a gap."""
    lay, d = overlay(fr); e = ease((t - tin) / 0.6); a = int(255 * e); m = ease((t - tin - 1.0) / 0.8)
    xs = [X0 + 40 + i * (TW - 80) / 18 for i in range(19)]
    d.line((X0 + 20, y + 40, X0 + TW - 20, y + 40), fill=(*SOFT, a), width=4)
    for k in range(19):
        c = CORAL if 2 <= k <= 4 and m > 0.3 else CYAN
        d.rectangle((xs[k] - 12, y + 18, xs[k] + 12, y + 62), fill=(*c, a))
    d.text((X0, y - 20), "BTK gene (exons, illustration)", font=font("Medium", 28), fill=(*SOFT, a), anchor="lm")
    if m > 0.3:
        gx0, gx1 = xs[2] - 30, xs[4] + 30
        d.line((gx0, y + 80, gx0, y + 100), fill=CORAL, width=4); d.line((gx1, y + 80, gx1, y + 100), fill=CORAL, width=4)
        d.line((gx0, y + 100, gx1, y + 100), fill=CORAL, width=4)
        d.text((gx1 + 20, y + 100), "5,296 bp deleted: exons 3-5", font=font("Bold", 28), fill=CORAL, anchor="lm")
    r = random.Random(7)
    for row in range(9):
        yy = y + 150 + row * 26
        x = X0 + r.uniform(0, 60)
        while x < X0 + TW - 60:
            L = r.uniform(70, 120)
            if not (xs[2] - 30 < x + L / 2 < xs[4] + 30) or m < 0.3:
                d.rounded_rectangle((x, yy, x + L, yy + 16), 6, fill=(150, 170, 200, int(200 * e)))
            x += L + r.uniform(8, 30)
    if m > 0.6:
        d.text(((xs[2] + xs[4]) / 2, y + 420), "No reads", font=font("Bold", 32), fill=AMBER, anchor="mm")
    fr.alpha_composite(lay)

def xl_pedigree(fr, y, t, tin):
    """X-linked recessive pattern: carrier mother, affected sons (illustration)."""
    lay, d = overlay(fr); e = ease((t - tin) / 0.6); a = int(255 * e)
    def sq(x, yy, aff): d.rectangle((x - 40, yy - 40, x + 40, yy + 40), outline=(*SOFT, a), width=4, fill=(*CORAL, a) if aff else None)
    def ci(x, yy, car):
        d.ellipse((x - 40, yy - 40, x + 40, yy + 40), outline=(*SOFT, a), width=4)
        if car: d.ellipse((x - 12, yy - 12, x + 12, yy + 12), fill=(*AMBER, a))
    sq(400, y, False); ci(680, y, True); d.line((440, y, 640, y), fill=(*SOFT, a), width=4)
    d.line((540, y, 540, y + 90), fill=(*SOFT, a), width=4); d.line((260, y + 90, 820, y + 90), fill=(*SOFT, a), width=4)
    for x, kind in ((260, "aff"), (447, "car"), (633, "no"), (820, "aff")):
        d.line((x, y + 90, x, y + 140), fill=(*SOFT, a), width=4)
        if kind == "aff": sq(x, y + 180, True)
        elif kind == "car": ci(x, y + 180, True)
        else: sq(x, y + 180, False)
    d.rectangle((X0, y + 276, X0 + 28, y + 304), fill=(*CORAL, a)); d.text((X0 + 44, y + 290), "Affected boy", font=font("Medium", 26), fill=(*CORAL, a), anchor="lm")
    d.ellipse((X0 + 330, y + 276, X0 + 358, y + 304), fill=(*AMBER, a)); d.text((X0 + 374, y + 290), "Carrier woman", font=font("Medium", 26), fill=(*AMBER, a), anchor="lm")
    d.text((X0 + TW, y + 290), "Illustration", font=font("Medium", 24), fill=(*SOFT, a), anchor="rm")
    fr.alpha_composite(lay)

# ---------------- scenes ----------------
def sc0(fr, t, D):
    show(fr, kicker("Genetics Clinical Series  •  Episode 9", CYAN), 330, t, 0.1)
    type_on(fr, "Whole genome", 410, t, 0.3, 72)
    type_on(fr, "sequencing", 500, t, 0.9, 72)
    if t > D * 0.3: type_on(fr, "What it adds beyond the exome", 610, t, D * 0.3, 40, AMBER)
    genome_bar(fr, 760, t, 0.5)
    show(fr, callout("For doctors and healthcare teams  •  with a published Indian case", CYAN, 34), 1640, t, D * 0.6); fire("whoosh", D * 0.6)

def sc_what(fr, t, D):
    dots(fr, 1); show(fr, kicker("Exome vs genome"), 260, t, 0.1)
    show(fr, headline("About 3 billion bases", 56), 320, t, 0.3)
    genome_bar(fr, 470, t, 0.6)
    show(fr, gcard("Exome: coding parts only, 1-2%", CYAN, 1, 34), 830, t, D * 0.4)
    show(fr, gcard("Genome: coding and non-coding", TEALG, 2, 34), 980, t, D * 0.6)
    fire("pop", D * 0.4); fire("pop", D * 0.6)

def sc_add1(fr, t, D):
    dots(fr, 2); show(fr, kicker("What it adds  •  1"), 260, t, 0.1)
    show(fr, headline("No capture step: more even coverage", 52), 320, t, 0.3)
    depth_tracks(fr, 470, t, 0.6)
    show(fr, gcard("Small variants and copy number changes in one test", AMBER, 1, 32), 1010, t, D * 0.55); fire("pop", D * 0.55)

sc_add2 = s_cards(3, "What it adds  •  2", None,
    [("Structural variants: inversions, translocation breakpoints", CORAL), ("Deep intronic and regulatory changes", LAV),
     ("Mitochondrial DNA", CYAN), ("Some repeat expansions, with special analysis", AMBER)], size=33)

def sc_evid(fr, t, D):
    dots(fr, 4); show(fr, kicker("The evidence in children"), 260, t, 0.1)
    show(fr, headline("Meta-analysis of 39 studies", 54), 320, t, 0.3)
    bars(fr, 470, [("Genome", 38.6, "38.6%", TEALG), ("Exome", 37.8, "37.8%", CYAN), ("Usual care", 7.8, "7.8%", (120, 140, 170))], t, 0.6, 45)
    show(fr, gcard("Similar yields; genome slightly ahead on direct comparison", AMBER, None, 32), 870, t, D * 0.55)
    show(fr, source_tag("Nurchis et al., Arch Public Health 2023;81:93"), 1030, t, D * 0.6)

def bars(fr, y, rows, t, tin, vmax):
    lay, d = overlay(fr); e = ease((t - tin) / 1.2)
    for i, (lab, v, txt, c) in enumerate(rows):
        yy = y + i * 120
        d.text((X0, yy + 30), lab, font=font("Medium", 34), fill=SOFT, anchor="lm")
        L = max(16, (TW - 420) * v / vmax * e)
        d.rounded_rectangle((X0 + 230, yy, X0 + 230 + L, yy + 60), 30, fill=c)
        d.text((X0 + 250 + L, yy + 30), txt, font=font("Bold", 34), fill=WHITE, anchor="lm")
    fr.alpha_composite(lay)

sc_when = s_cards(5, "When to consider genome", None,
    [("Exome negative but strong suspicion", CYAN), ("Suspected structural variant", CORAL),
     ("One test instead of CMA plus exome", TEALG), ("Rapid genome for critically ill newborns (some centres)", AMBER)],
    lambda fr, t, D, y: show(fr, source_tag("ACMG guideline 2021: exome or genome (Manickam et al., Genet Med)"), y + 10, t, D * 0.6), size=33)

sc_limit = s_cards(6, "Limits", None,
    [("Higher cost and very large data", (120, 140, 170)), ("Non-coding changes are hard to interpret: more VUS", AMBER),
     ("Short-read genome can miss methylation disorders", LAV), ("Low-level mosaicism and some difficult regions", CORAL),
     ("Long-read sequencing is closing some gaps", TEALG)], size=32)

sc_prac = s_cards(7, "In practice", None,
    [("Trio gives a clearer report", CYAN), ("Counsel first; written consent on secondary findings", AMBER),
     ("Data can be reanalysed later", TEALG)], size=34)

def sc_sample(fr, t, D):
    dots(fr, 8); show(fr, kicker("Sample"), 260, t, 0.1)
    put(fr, tube_sprite((149, 117, 205), "EDTA"), 300, 640, 1.0, ease((t - 0.3) / 0.5))
    lay, d = overlay(fr); e = ease((t - 0.5) / 0.5)
    d.text((300, 950), "Blood (EDTA)", font=font("Bold", 34), fill=(*SOFT, int(255 * e)), anchor="mm"); fr.alpha_composite(lay)
    show(fr, gcard("Trio: parents' samples too", TEALG, 1, 33), 1010, t, D * 0.25)
    show(fr, gcard("Prenatal: amniotic fluid or CVS", LAV, 2, 33), 1160, t, D * 0.4)
    show(fr, callout("Prenatal: disease testing only; sex never disclosed (PCPNDT)", CORAL, 32), 1320, t, D * 0.55)
    fire("pop", D * 0.25); fire("pop", D * 0.4)

def sc_case1(fr, t, D):
    dots(fr, 9); show(fr, kicker("Case study from India", CORAL), 260, t, 0.1)
    put(fr, PAPER, 540, 610, 0.56, ease((t - 0.4) / 0.6))
    for i, (txt, c) in enumerate((("Large family: 5 boys with repeated infections from 5-12 months", CYAN),
                                  ("Tiny or absent tonsils, low antibodies, almost no B cells", AMBER),
                                  ("X-linked agammaglobulinemia; all on IVIG", LAV))):
        show(fr, gcard(txt, c, None, 31), 870 + i * 160, t, D * (0.25 + 0.12 * i))
    show(fr, source_tag("Jain et al., PLoS ONE 2021;16(7):e0254407 (CSIR-IGIB and others), CC BY"), 1360, t, D * 0.65)

def sc_case2(fr, t, D):
    dots(fr, 10); show(fr, kicker("Case: exome missed it, genome found it"), 260, t, 0.1)
    show(fr, gcard("Flow cytometry: low BTK protein", CYAN, 1, 33), 330, t, 0.3)
    show(fr, gcard("Exome in 4 boys: no matching small variant", (120, 140, 170), 2, 32), 480, t, D * 0.15)
    btk_del(fr, 700, t, D * 0.3)
    show(fr, gcard("Not in global or Indian (IndiGen) databases; MLPA confirmed", TEALG, 3, 31), 1220, t, D * 0.7)

def sc_case3(fr, t, D):
    dots(fr, 11); show(fr, kicker("Case: what it meant for the family"), 260, t, 0.1)
    xl_pedigree(fr, 380, t, 0.3)
    show(fr, gcard("17 relatives tested: 7 women were carriers", AMBER, 1, 33), 760, t, D * 0.3)
    show(fr, gcard("2 boys: transplant from matched siblings, reported disease-free", TEALG, 2, 31), 910, t, D * 0.45)
    show(fr, gcard("Exome struggles to call structural variants", CORAL, 3, 33), 1080, t, D * 0.6)
    fire("pop", D * 0.3); fire("pop", D * 0.45); fire("ding", D * 0.6)

sc_take = s_cards(12, "Key messages", None,
    [("Genome reads coding and non-coding DNA", CYAN), ("Small variants, CNVs and structural variants in one test", TEALG),
     ("Consider it when exome is negative but suspicion is strong", AMBER), ("It still misses some things: clinical picture matters", LAV),
     ("The right variant helps the whole family", CORAL)], size=31)

SC = [(film(sc0), "doc"), (film(sc_what), "doc"), (film(sc_add1), "doc"), (film(sc_add2), "doc"), (film(sc_evid), "doc"),
      (film(sc_when), "doc"), (film(sc_limit), "doc"), (film(sc_prac), "doc"), (film(sc_sample), "doc"),
      (film(sc_case1), "doc"), (film(sc_case2), "doc"), (film(sc_case3), "doc"), (film(sc_take), "doc"),
      (close_scene("Used genome sequencing yet?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si, (fn, bg) in enumerate(SC):
            d = 16 if si < len(SC) - 1 else 33; p = .95 if si else 0.125; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((300, 533)))
        s = Image.new("RGB", (300 * 5, 533 * 3), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 300, (i // 5) * 533))
        s.save(sys.argv[2] if len(sys.argv) > 2 else "/tmp/sheet_g009.png")
    elif len(sys.argv) > 1 and sys.argv[1] == "bn":
        run(SC, "/tmp/g009bn_", "Genetics_Ep09_Whole_Genome_Sequencing_Bengali.mp4", max_sec=480)
    elif len(sys.argv) > 1 and sys.argv[1] == "bn_teaser":
        import doc_style
        run([(close_scene("Used genome sequencing yet?", "WATCH THE FULL VIDEO ON OUR CHANNEL"), "docl")], "/tmp/tzbn_g009_", "/tmp/tzbn_g009.mp4", max_sec=180, cover_skip=0)
    else: run(SC, "/tmp/g009_", "Genetics_Ep09_Whole_Genome_Sequencing_Hindi.mp4", max_sec=480)
