"""SMA genetic test, documentary style (no cartoon characters). Uses the same voice files as sma_cartoon (/tmp/sma_)."""
import math, sys
from cbc_cartoon import run
from doc_style import *
from hts_close import close_scene

TOPIC = "GENETIC TEST  •  SMA"
CHROMO = chromosome_sprite("Chromosome 5", 0.62, "SMN1 gene (5q13)")
TUBE = tube_sprite()

def dots(fr, n): fr.alpha_composite(chapter(n, 9), (0, 110))

def d_hook(fr, t, D):
    helix(fr, 760, 1150, 700, t, amp=170, alpha=150)
    show(fr, kicker("Genetic test  •  SMA", CYAN), 330, t, 0.1)
    type_on(fr, "Baby can't hold the head up?", 410, t, 0.4, 74)
    if t > D * 0.3: type_on(fr, "Late to sit or walk?", 600, t, D * 0.3, 74, AMBER)
    show(fr, callout("One possible cause: SMA, a genetic condition", CORAL, 40), 1620, t, D * 0.6); fire("whoosh", D * 0.6)

def d_what(fr, t, D):
    dots(fr, 1)
    show(fr, kicker("What is SMA?"), 260, t, 0.1)
    show(fr, headline("Spinal Muscular Atrophy", 66), 320, t, 0.3)
    alive = 1 - 0.7 * ease((t - D * 0.45) / (D * 0.35))
    neuron(fr, 180, t, alive)
    d = ImageDraw.Draw(fr)
    d.text((145, 1150), "Spinal cord", font=font("Medium", 30), fill=MUTED, anchor="mm")
    d.text((915, 1060), "Muscle", font=font("Medium", 30), fill=MUTED, anchor="mm")
    show(fr, gcard("Motor nerve cells in the spinal cord slowly die", AMBER, 1, 38), 1230, t, D * 0.3)
    show(fr, gcard("Muscles get weak and thin", CORAL, 2, 38), 1380, t, D * 0.55)
    fire("pop", D * 0.3); fire("pop", D * 0.55)

def d_gene(fr, t, D):
    dots(fr, 2)
    show(fr, kicker("The gene"), 260, t, 0.1)
    show(fr, headline("SMN1, on chromosome 5", 62), 320, t, 0.3)
    p = ease((t - 0.5) / 0.8)
    if p > 0: put(fr, CHROMO, 60 + CHROMO.width / 2, 470 + CHROMO.height / 2 * 0.85, 0.85, p)
    exon_bar(fr, X0, 1270, TW, None, "Normal SMN1", t=t, tin=D * 0.25)
    exon_bar(fr, X0, 1420, TW, 6, "In most SMA patients: exon 7 missing (both copies)", t=t, tin=D * 0.35)
    fire("boom", D * 0.4)
    show(fr, gcard("Backup gene SMN2 makes a little protein. More SMN2 copies = usually milder.", TEALG, None, 34), 1540, t, D * 0.6)

def d_types(fr, t, D):
    dots(fr, 3)
    show(fr, kicker("Types"), 260, t, 0.1)
    show(fr, headline("When symptoms usually start", 62), 320, t, 0.3)
    lay, d = overlay(fr)
    rows = [("Type 1", "Birth to 6 months", CORAL), ("Type 2", "6 to 12 months", AMBER), ("Type 3", "After early childhood", CYAN), ("Type 4", "Adulthood, usually mild", TEALG)]
    x = 150; y0 = 560
    pl = ease((t - 0.4) / (D * 0.6))
    d.line((x, y0, x, y0 + 900 * pl), fill=(255, 255, 255, 80), width=4)
    for i, (a, b, c) in enumerate(rows):
        tin = 0.4 + i * D * 0.15; fire("pop", tin)
        if t < tin: continue
        y = y0 + i * 260; e = ease((t - tin) / 0.4)
        d.ellipse((x - 22, y - 22, x + 22, y + 22), fill=c)
        d.text((x + 70 - 30 * (1 - e), y - 40), a, font=font("Bold", 60), fill=c)
        d.text((x + 70 - 30 * (1 - e), y + 35), b, font=font("Regular", 42), fill=SOFT)
    fr.alpha_composite(lay)

def d_inherit(fr, t, D):
    dots(fr, 4)
    show(fr, kicker("How it passes on"), 260, t, 0.1)
    show(fr, headline("Carriers are healthy, and usually don't know", 58), 320, t, 0.3)
    pedigree(fr, 760, t, D * 0.15)
    for i in range(4): fire("pop", D * 0.15 + 0.6 + i * 0.5)
    d = ImageDraw.Draw(fr)
    if t > D * 0.2:
        for k, (lab, c) in enumerate((("Carrier", AMBER), ("Affected", CORAL))):
            xx = 300 + k * 330; d.rectangle((xx, 1150, xx + 34, 1184), fill=c); d.text((xx + 50, 1167), lab, font=font("Medium", 30), fill=MUTED, anchor="lm")
    show(fr, callout("Both parents carriers: 1 in 4 chance of SMA in each pregnancy", CORAL, 38), 1260, t, D * 0.75); fire("boom", D * 0.75)

def d_india(fr, t, D):
    dots(fr, 5)
    show(fr, kicker("Carriers in India"), 260, t, 0.1)
    person_grid(fr, 38, 20, 160, 420, 13, t, 0.4)
    fire("whoosh", 0.4)
    if t > D * 0.3:
        lay, d = overlay(fr); e = ease((t - D * 0.3) / 0.5)
        d.text((X0, 720), "About 1 in 38", font=font("Bold", 120), fill=(*AMBER, int(255 * e))); fr.alpha_composite(lay)
    show(fr, body("healthy people with no family history were carriers in a north Indian study", 40, SOFT), 880, t, D * 0.35)
    show(fr, gcard("Being a carrier is not a disease", TEALG, 1, 38), 1090, t, D * 0.55)
    show(fr, gcard("Nothing to be ashamed of. It helps families plan.", CYAN, 2, 38), 1240, t, D * 0.68)
    fire("pop", D * 0.55); fire("pop", D * 0.68)
    show(fr, source_tag("Nilay et al., north Indian population study, 2021"), 1430, t, D * 0.75)

def d_test(fr, t, D):
    dots(fr, 6)
    show(fr, kicker("The test"), 260, t, 0.1)
    show(fr, headline("One blood sample. MLPA counts SMN1 copies.", 54), 320, t, 0.3)
    p = ease((t - 0.4) / 0.6)
    if p > 0: put(fr, TUBE, 190, 900, 1.0, p)
    rows = [([1, 0], "0 copies: SMA confirmed", CORAL), ([1, 0.5], "1 copy: carrier", AMBER), ([1, 1], "2 copies: usually normal", TEALG)]
    for i, (hv, title, c) in enumerate(rows):
        tin = D * (0.2 + 0.15 * i); fire("pop", tin)
        if t < tin: continue
        peaks(fr, 340, 520 + i * 270, 660, 240, hv, ["Ref", "SMN1"], t, tin, title, c)
    show(fr, callout("A few people with 2 copies can still be carriers", LAV, 36), 1360, t, D * 0.7); fire("ding", D * 0.7)
    show(fr, body("Understand the report with a genetic counsellor", 38, SOFT), 1500, t, D * 0.8)

def d_who(fr, t, D):
    dots(fr, 7)
    show(fr, kicker("Who should test?"), 260, t, 0.1)
    items = [("A child with signs of SMA", CORAL), ("SMA in the family", AMBER), ("Couples planning marriage or a baby", CYAN), ("If both are carriers: baby can be tested in pregnancy", LAV)]
    for i, (txt, c) in enumerate(items):
        fire("pop", D * (0.1 + 0.15 * i)); show(fr, gcard(txt, c, i + 1, 38), 360 + i * 160, t, D * (0.1 + 0.15 * i))
    show(fr, callout("For disease only. The baby's sex is never disclosed.", CORAL, 38), 1060, t, D * 0.75); fire("boom", D * 0.75)
    helix(fr, 540, 1520, 380, t, amp=260, turns=1.2, alpha=90, n=30)

def d_treat(fr, t, D):
    dots(fr, 8)
    show(fr, kicker("Good news", TEALG), 260, t, 0.1)
    show(fr, headline("SMA is now treatable", 70), 320, t, 0.3)
    capsule(fr, 540, 620, 150, t); fire("ding", 0.3)
    show(fr, gcard("Medicine is available in India", CYAN, 1, 38), 830, t, D * 0.2)
    show(fr, gcard("Earlier start, ideally before symptoms = better results", TEALG, 2, 38), 980, t, D * 0.35)
    show(fr, gcard("Rare disease policy: financial support may be available", AMBER, 3, 38), 1170, t, D * 0.55)
    for k in (0.2, 0.35, 0.55): fire("pop", D * k)
    show(fr, body("Treatment is decided only by a specialist doctor", 38, CORAL), 1380, t, D * 0.75)

SC = [(d_hook, "doc"), (d_what, "doc"), (d_gene, "doc"), (d_types, "doc"), (d_inherit, "doc"),
      (d_india, "doc"), (d_test, "doc"), (d_who, "doc"), (d_treat, "doc"),
      (close_scene("Had you heard of SMA before?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        D = [14.9, 14.5, 20, 13.9, 20.6, 16.8, 25.6, 22.7, 19.4, 33.4]
        ims = []
        for si in range(10):
            fn, bg = SC[si]; d = D[si]; p = 0.95; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((360, 640)))
        s = Image.new("RGB", (360 * 5, 640 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 360, (i // 5) * 640))
        s.save("sheet.png")
        if len(sys.argv) > 2:
            si = int(sys.argv[2]); fn, bg = SC[si]; d = D[si]; NOW.update(t=d * .95, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * .95, d); fr.convert("RGB").save("frame.png")
    else: run(SC, "/tmp/sma_", "SMA_Genetic_Test_Documentary_Hindi.mp4")
