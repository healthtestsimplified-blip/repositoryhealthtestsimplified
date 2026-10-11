"""Beta thalassemia mutation analysis, realistic documentary style."""
import math, sys
from cbc_cartoon import run
from real_style import *
from hts_close import close_scene

TOPIC = "GENETIC TEST  •  BETA THALASSEMIA"
SMEAR = rbc_smear(1400, 4, True)
CHR11 = chromosome_sprite("Chromosome 11", 0.2, "HBB gene (11p15.4)")
TUBE = tube_sprite()
SEQ = "CCTTGGACCCAGAGGTTCTTTG"

def dots(fr, n): fr.alpha_composite(chapter(n, 9), (0, 110))
def ep(fr, tex, cx, cy, size, t, D, z0=1.6, z1=2.0, focus=0.0, pan=(0.2, 0.1), a=1.0):
    put(fr, eyepiece(tex, size, t, z0, z1, D, pan, focus), cx, cy, 1.0, a)
def label(fr, text, x, y, col=SOFT, size=32, anchor="mm", weight="Medium"):
    lay, d = overlay(fr); d.text((x, y), text, font=font(weight, size), fill=col, anchor=anchor); fr.alpha_composite(lay)

def m_hook(fr, t, D):
    fullbleed(fr, SMEAR, t, D, 1.6, 2.0)
    show(fr, kicker("Genetic test  •  Beta thalassemia", CYAN), 330, t, 0.1)
    type_on(fr, "HPLC says: thalassemia carrier?", 410, t, 0.4, 68)
    if t > D * 0.35: type_on(fr, "Next: mutation analysis", 600, t, D * 0.35, 68, AMBER)
    show(fr, callout("What it is, and why it matters", CYAN, 40), 1620, t, D * 0.6); fire("whoosh", D * 0.6)

def m_gene(fr, t, D):
    dots(fr, 1)
    show(fr, kicker("The gene"), 260, t, 0.1)
    show(fr, headline("HBB: the recipe for beta globin", 58), 320, t, 0.3)
    p = ease((t - 0.4) / 0.8)
    if p > 0: put(fr, CHR11, 60 + CHR11.width * 0.85 / 2, 480 + CHR11.height * 0.85 / 2, 0.85, p)
    if t > D * 0.35: ep(fr, SMEAR, 820, 1290, 360, t - D * 0.35, D, 2.2, 2.6)
    show(fr, gcard("A change (mistake) in this gene = MUTATION", CORAL, None, 38), 1520, t, D * 0.6)
    if t > D * 0.35: label(fr, "Red blood cells", 820, 1500 - 20, SOFT, 28)

def m_vs(fr, t, D):
    dots(fr, 2)
    show(fr, kicker("Screening vs DNA test"), 260, t, 0.1)
    hplc_chart(fr, X0, 340, TW, 380, t, 0.4)
    label(fr, "Tells: carrier or not", 540, 760, AMBER, 36, weight="Bold")
    if t > D * 0.35:
        sanger(fr, X0, 830, TW, 400, t, D * 0.35, SEQ, (9, "C"))
        label(fr, "Tells: exactly WHICH mutation", 540, 1270, TEALG, 36, weight="Bold")
    show(fr, gcard("A DNA test done on a blood sample", CYAN, None, 38), 1360, t, D * 0.7)

def m_india(fr, t, D):
    dots(fr, 3)
    show(fr, kicker("Common in India"), 260, t, 0.1)
    show(fr, headline("Many mutations, a few very common", 58), 320, t, 0.3)
    lay, d = overlay(fr)
    p = ease((t - D * 0.2) / 1.2)
    if t > D * 0.2:
        d.text((X0, 560), "IVS1-5", font=font("Bold", 52), fill=AMBER)
        d.rounded_rectangle((X0, 650, X0 + TW, 720), 35, fill=(255, 255, 255, 25))
        d.rounded_rectangle((X0, 650, X0 + TW * 0.466 * p, 720), 35, fill=AMBER)
        d.text((X0 + TW * 0.466 * p + 20, 685), f"~{int(round(46.6 * p))}%", font=font("Bold", 44), fill=WHITE, anchor="lm")
        d.text((X0, 750), "of beta carriers (West Bengal hospital study)", font=font("Regular", 34), fill=SOFT)
    if t > D * 0.5:
        e = ease((t - D * 0.5) / 0.5)
        d.text((X0, 880), "Next most common:", font=font("Medium", 36), fill=(*MUTED, int(255 * e)))
        d.text((X0, 940), "Codon 26 = HbE", font=font("Bold", 60), fill=(*TEALG, int(255 * e)))
        d.text((X0, 1030), "common in East & North-East India", font=font("Regular", 34), fill=(*SOFT, int(255 * e)))
    fr.alpha_composite(lay)
    fire("whoosh", D * 0.2); fire("pop", D * 0.5)
    show(fr, source_tag("Int J Hematol 2014, hospital study, West Bengal"), 1160, t, D * 0.6)

def m_method(fr, t, D):
    dots(fr, 4)
    show(fr, kicker("How it's tested"), 260, t, 0.1)
    gel(fr, X0, 320, TW, 430, t, 0.4, [[0.32, 0.62], [0.32], [0.32, 0.62], [0.62]])
    label(fr, "1. ARMS-PCR: checks the common mutations", 540, 790, AMBER, 34, weight="Bold")
    if t > D * 0.35:
        sanger(fr, X0, 860, TW, 400, t, D * 0.35, SEQ, (9, "C"), title="2. Sanger: reads the gene letter by letter")
    show(fr, gcard("3. Separate test for missing pieces (deletions)", LAV, None, 37), 1310, t, D * 0.7)
    fire("pop", D * 0.35); fire("pop", D * 0.7)

def m_couple(fr, t, D):
    dots(fr, 5)
    show(fr, kicker("Why it matters"), 260, t, 0.1)
    show(fr, headline("Both partners carriers?", 62), 320, t, 0.3)
    pedigree(fr, 640, t, D * 0.12, "Thal major")
    for i in range(4): fire("pop", D * 0.12 + 0.6 + i * 0.5)
    show(fr, callout("1 in 4 chance of thalassemia major in each pregnancy", CORAL, 38), 1060, t, D * 0.45); fire("boom", D * 0.45)
    show(fr, gcard("Testing the baby is possible only when BOTH parents' mutations are known", CYAN, None, 36), 1230, t, D * 0.7)

def m_prenatal(fr, t, D):
    dots(fr, 6)
    show(fr, kicker("Testing in pregnancy"), 260, t, 0.1)
    show(fr, headline("CVS: usually 10 to 13 weeks", 60), 320, t, 0.3)
    lay, d = overlay(fr)
    x0, x1, y = X0 + 20, X0 + TW - 20, 600; p = ease((t - 0.5) / 1.0)
    d.line((x0, y, x0 + (x1 - x0) * p, y), fill=(255, 255, 255, 90), width=6)
    for wk in (0, 10, 20, 30, 40):
        xx = x0 + (x1 - x0) * wk / 40
        if xx > x0 + (x1 - x0) * p: break
        d.line((xx, y - 14, xx, y + 14), fill=(255, 255, 255, 140), width=3)
        d.text((xx, y + 44), str(wk), font=font("Medium", 28), fill=MUTED, anchor="mm")
    if p > 0.5:
        a = x0 + (x1 - x0) * 10 / 40; b = x0 + (x1 - x0) * 13 / 40
        d.rounded_rectangle((a, y - 30, b, y + 30), 12, fill=(*TEALG, 200))
        d.text(((a + b) / 2, y - 60), "CVS", font=font("Bold", 34), fill=TEALG, anchor="mm")
    d.text((540, y + 100), "weeks of pregnancy", font=font("Regular", 30), fill=MUTED, anchor="mm")
    fr.alpha_composite(lay)
    show(fr, gcard("The baby's sample is checked for the SAME family mutations", CYAN, 1, 36), 820, t, D * 0.35)
    show(fr, callout("For disease only. The baby's sex is never disclosed.", CORAL, 38), 1010, t, D * 0.6); fire("boom", D * 0.6)
    put(fr, TUBE, 540, 1420, 0.7, ease((t - D * 0.2) / 0.5))

def m_severity(fr, t, D):
    dots(fr, 7)
    show(fr, kicker("For patients"), 260, t, 0.1)
    show(fr, headline("Mutation type gives a clue to severity", 58), 320, t, 0.3)
    lay, d = overlay(fr)
    rows = [("Beta-zero mutation", "no beta globin made", 0.0, CORAL), ("Beta-plus mutation", "some beta globin made", 0.4, AMBER), ("HbE + beta thal", "often a middle (intermedia-like) form", 0.55, LAV)]
    for i, (a, b, v, c) in enumerate(rows):
        tin = D * (0.15 + 0.18 * i); fire("pop", tin)
        if t < tin: continue
        e = ease((t - tin) / 0.6); y = 520 + i * 200
        d.text((X0, y), a, font=font("Bold", 46), fill=c)
        d.text((X0, y + 62), b, font=font("Regular", 32), fill=SOFT)
        d.rounded_rectangle((X0 + 560, y + 20, X0 + TW, y + 64), 22, fill=(255, 255, 255, 25))
        if v > 0: d.rounded_rectangle((X0 + 560, y + 20, X0 + 560 + (TW - 560) * v * e, y + 64), 22, fill=c)
        else: d.text((X0 + 580, y + 42), "0", font=font("Bold", 30), fill=c, anchor="lm")
    d.text((X0 + 560, 470), "beta globin made", font=font("Medium", 26), fill=MUTED)
    fr.alpha_composite(lay)
    show(fr, callout("Treatment is decided only by the doctor", TEALG, 40), 1200, t, D * 0.75)

def m_who(fr, t, D):
    dots(fr, 8)
    show(fr, kicker("Who should get it?"), 260, t, 0.1)
    items = [("Carrier couples, before planning a pregnancy", CYAN), ("Family with a thalassemia major child", CORAL),
             ("Unclear reports, e.g. borderline HbA2", AMBER), ("People with thalassemia", LAV)]
    for i, (txt, c) in enumerate(items):
        fire("pop", D * (0.1 + 0.15 * i)); show(fr, gcard(txt, c, i + 1, 38), 360 + i * 160, t, D * (0.1 + 0.15 * i))
    show(fr, callout("Understand the report with a genetic counsellor", TEALG, 38), 1060, t, D * 0.75)
    ep(fr, SMEAR, 540, 1480, 360, t, D, 2.2, 2.5)

SC = [(film(m_hook), "doc"), (film(m_gene), "doc"), (film(m_vs), "doc"), (film(m_india), "doc"), (film(m_method), "doc"),
      (film(m_couple), "doc"), (film(m_prenatal), "doc"), (film(m_severity), "doc"), (film(m_who), "doc"),
      (close_scene("Have you both been tested?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        D = [14, 16, 16, 18, 18, 18, 18, 20, 20, 33]
        ims = []
        for si in range(10):
            fn, bg = SC[si]; d = D[si]; p = 0.95; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((360, 640)))
        s = Image.new("RGB", (360 * 5, 640 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 360, (i // 5) * 640))
        s.save("sheet.png")
    else: run(SC, "/tmp/btm_", "Beta_Thalassemia_Mutation_Analysis_Hindi.mp4")
