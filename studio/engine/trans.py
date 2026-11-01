"""Transgender: is it in the chromosomes or genes? (Bengali awareness Reel, <= 3:00). Voice: BN_RATE=+8% python3 bn_tanishaa.py trans"""
import sys
from cbc_cartoon import run
from gen_series import *
from hts_close import close_scene

TOT[0] = 7
TOPIC = "GENETICS  •  AWARENESS"
SRC_TR = "Cankaya et al., J Clin Pract Res 2021 (67 transgender individuals, Izmir)"
KARYO = karyogram(920, 620, seed=7)

def two(fr, y, t, tin):
    lay, d = overlay(fr); e = ease((t - tin) / 0.6); a = int(255 * e)
    for i, (h, sub, c) in enumerate((("Sex at birth", "body, chromosomes, organs", CYAN), ("Gender identity", "how a person knows their own gender", LAV))):
        yy = y + i * 230
        d.rounded_rectangle((X0, yy, X0 + TW, yy + 190), 28, fill=(*c, int(40 * e)), outline=(*c, a), width=4)
        d.text((540, yy + 65), h, font=font("Bold", 44), fill=(*WHITE, a), anchor="mm")
        d.text((540, yy + 130), sub, font=font("Medium", 32), fill=(*SOFT, a), anchor="mm")
    fr.alpha_composite(lay)

def sc0(fr, t, D):
    show(fr, kicker("Genetics  •  Awareness", CYAN), 330, t, 0.1)
    show(fr, headline("Transgender:", 74), 410, t, -1)
    show(fr, headline("is it in the chromosomes?", 56, (249, 196, 120)), 510, t, -1)
    show(fr, gcard("Short answer: no chromosome or gene defect causes it", TEALG, None, 33), 680, t, D * 0.3)
    show(fr, gcard("No test can tell if a person is transgender", AMBER, None, 33), 840, t, D * 0.45)
    fire("pop", D * 0.3); fire("pop", D * 0.45)
    show(fr, callout("What the science says", CYAN, 36), 1640, t, D * 0.6); fire("whoosh", D * 0.6)

def sc_words(fr, t, D):
    dots(fr, 1); show(fr, kicker("Two different things"), 260, t, 0.1)
    two(fr, 340, t, 0.3)
    show(fr, gcard("Transgender: gender identity differs from the sex recorded at birth", TEALG, None, 32), 860, t, D * 0.55)
    fire("pop", D * 0.55)

def sc_chromo(fr, t, D):
    dots(fr, 2); show(fr, kicker("Chromosomes"), 260, t, 0.1)
    put(fr, KARYO, 540, 600, 0.95, ease((t - 0.3) / 0.6))
    show(fr, headline("66 of 67: typical chromosomes", 50), 960, t, D * 0.3)
    show(fr, gcard("1 of 67: mosaic Turner syndrome", AMBER, None, 33), 1060, t, D * 0.45)
    show(fr, gcard("Authors: karyotype not needed unless signs of a DSD", TEALG, None, 32), 1210, t, D * 0.6)
    show(fr, source_tag(SRC_TR), 1380, t, D * 0.7)

def sc_genes(fr, t, D):
    dots(fr, 3); show(fr, kicker("Genes"), 260, t, 0.1)
    gene_grid(fr, X0, 330, TW, 380, t, 0.3, highlight=set(range(3, 600, 37)), title="Many genes, each a small effect (illustration)")
    show(fr, gcard("Twin and family studies: genes may play a part, with other factors", CYAN, 1, 32), 780, t, D * 0.35)
    show(fr, gcard("No single gene has been found", CORAL, 2, 34), 950, t, D * 0.5)
    show(fr, source_tag("Polderman et al., Behavior Genetics 2018 (review)"), 1110, t, D * 0.6)
    fire("pop", D * 0.35); fire("pop", D * 0.5)

def sc_who(fr, t, D):
    dots(fr, 4); show(fr, kicker("Is it an illness?"), 260, t, 0.1)
    show(fr, headline("WHO, ICD-11", 64), 330, t, 0.3)
    show(fr, gcard("Gender incongruence moved out of the mental disorders chapter", LAV, 1, 32), 470, t, D * 0.25)
    show(fr, gcard("Now in the sexual health chapter", TEALG, 2, 34), 640, t, D * 0.4)
    show(fr, gcard("Reason given: not a mental illness; the old listing caused stigma", AMBER, 3, 32), 790, t, D * 0.55)
    show(fr, source_tag("World Health Organization, ICD-11 (announced 2018)"), 960, t, D * 0.65)
    fire("pop", D * 0.25); fire("pop", D * 0.4); fire("pop", D * 0.55)

def sc_dsd(fr, t, D):
    dots(fr, 5); show(fr, kicker("Where chromosome tests DO matter"), 260, t, 0.1)
    show(fr, headline("DSD / intersex", 64), 330, t, 0.3)
    show(fr, gcard("Born with atypical chromosomal, gonadal or body sex development", CYAN, None, 32), 460, t, D * 0.2)
    show(fr, gcard("First: karyotype and SRY", TEALG, 1, 34), 630, t, D * 0.32)
    show(fr, gcard("Then: microarray, gene panel (e.g. AR, CYP21A2)", AMBER, 2, 33), 770, t, D * 0.44)
    show(fr, gcard("Romania, 267 patients: gene panel found the cause in 50%", LAV, 3, 32), 940, t, D * 0.56)
    show(fr, source_tag("Society for Endocrinology UK guidance 2021; Miclea et al., Diagnostics 2021"), 1110, t, D * 0.66)

sc_take = s_cards(6, "Remember", None,
    [("Transgender and DSD are different", CYAN), ("Transgender people usually have typical chromosomes", TEALG),
     ("There is no test for being transgender", AMBER), ("What helps: respect and medical support", LAV)], size=33)

SC = [(film(sc0), "doc"), (film(sc_words), "doc"), (film(sc_chromo), "doc"), (film(sc_genes), "doc"),
      (film(sc_who), "doc"), (film(sc_dsd), "doc"), (film(sc_take), "doc"),
      (close_scene("Did you know there is no test for it?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si, (fn, bg) in enumerate(SC):
            d = 16 if si < len(SC) - 1 else 33; p = .95 if si else 0.01; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((450, 800)))
        s = Image.new("RGB", (450 * 4, 800 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 4) * 450, (i // 4) * 800))
        s.save("/tmp/sheet_trans.png")
    else: run(SC, "/tmp/transbn_", "Transgender_Chromosomes_Bengali.mp4", max_sec=180)
