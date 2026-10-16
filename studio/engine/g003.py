"""Genetics Clinical Series, Episode 3: Trio vs singleton testing."""
import sys
from cbc_cartoon import run
from gen_series import *
from hts_close import close_scene

TOT[0] = 14
TOPIC = "GENETICS SERIES  •  EPISODE 3"
PAPER = paper_sprite(["Whole-exome sequencing", "revealed a de novo", "variant in SETBP1"], "Frontiers in Genetics, 2025")

def person(d, x, y, female, fill, a=255, s=46, col=SOFT):
    if female: d.ellipse((x - s, y - s, x + s, y + s), fill=(*fill, a) if fill else None, outline=(*col, a), width=5)
    else: d.rectangle((x - s, y - s, x + s, y + s), fill=(*fill, a) if fill else None, outline=(*col, a), width=5)

def family(fr, cx, y, t, tin, which=("child", "mother", "father"), affected_child=True, label=True):
    lay, d = overlay(fr); e = ease((t - tin) / 0.6); a = int(255 * e)
    if a <= 0: return
    fx, mx = cx - 170, cx + 170
    on = lambda k: k in which
    dim = lambda k: a if on(k) else int(a * 0.25)
    person(d, fx, y, False, None, dim("father")); person(d, mx, y, True, None, dim("mother"))
    d.line((fx + 46, y, mx - 46, y), fill=(*SOFT, int(a * 0.6)), width=4); d.line((cx, y, cx, y + 120), fill=(*SOFT, int(a * 0.6)), width=4)
    person(d, cx, y + 170, True, CORAL if affected_child else None, dim("child"))
    if label:
        for x, yy, k, txt in ((fx, y - 80, "father", "Father"), (mx, y - 80, "mother", "Mother"), (cx, y + 255, "child", "Patient")):
            d.text((x, yy), txt, font=font("Medium", 28), fill=(*SOFT, dim(k)), anchor="mm")
    fr.alpha_composite(lay)

def phase(fr, x, y, t, tin, mode="trans"):
    """Two homologous chromosome copies with two variants: in trans (one per copy) or in cis."""
    lay, d = overlay(fr); e = ease((t - tin) / 0.6); a = int(255 * e)
    for i, (lab, col) in enumerate((("From mother", LAV), ("From father", CYAN))):
        yy = y + i * 110
        d.rounded_rectangle((x, yy, x + 420, yy + 46), 23, fill=(*col, int(a * 0.85)))
        d.text((x + 440, yy + 23), lab, font=font("Medium", 28), fill=(*SOFT, a), anchor="lm")
    pos = [(x + 130, y), (x + 290, y + 110)] if mode == "trans" else [(x + 130, y), (x + 290, y)]
    for px, py in pos:
        d.rectangle((px - 10, py - 8, px + 10, py + 54), fill=(*CORAL, a))
    fr.alpha_composite(lay)

def bars(fr, x, y, w, t, tin, rows, title, vmax=50):
    panel(fr, x, y, w, 110 + 100 * len(rows), title)
    lay, d = overlay(fr); e = ease((t - tin) / 1.0)
    for i, (lab, v, c) in enumerate(rows):
        yy = y + 90 + i * 100
        d.text((x + 24, yy + 22), lab, font=font("Medium", 30), fill=SOFT, anchor="lm")
        L = (w - 440) * v / vmax * e
        d.rounded_rectangle((x + 300, yy, x + 300 + L, yy + 46), 23, fill=c)
        d.text((x + 316 + L, yy + 23), f"{v}%", font=font("Bold", 32), fill=WHITE, anchor="lm")
    fr.alpha_composite(lay)

# ---------------- scenes ----------------
def sc0(fr, t, D):
    helix(fr, 900, 1250, 650, t, amp=170, alpha=140)
    show(fr, kicker("Genetics Clinical Series  •  Episode 3", CYAN), 330, t, 0.1)
    type_on(fr, "Trio or singleton?", 410, t, 0.4, 72)
    if t > D * 0.3: type_on(fr, "Test only the patient, or the parents too?", 520, t, D * 0.3, 44, AMBER)
    family(fr, 540, 820, t, D * 0.4)
    show(fr, callout("For doctors and healthcare teams  •  with a published case study", CYAN, 34), 1640, t, D * 0.6); fire("whoosh", D * 0.6)

def sc_terms(fr, t, D):
    dots(fr, 1); show(fr, kicker("Three ways to test"), 260, t, 0.1)
    for i, (which, lab, c) in enumerate(((("child",), "Singleton: patient only", CYAN), (("child", "mother"), "Duo: patient + one parent", AMBER),
                                         (("child", "mother", "father"), "Trio: patient + both parents", TEALG))):
        tin = D * (0.08 + 0.2 * i); yy = 380 + i * 420
        if t < tin: continue
        family(fr, 300, yy, t, tin, which, label=False)
        lay, d = overlay(fr); e = ease((t - tin) / 0.5)
        for j, line in enumerate(wrap(lab, font("Bold", 36), 420)):
            d.text((560, yy + 60 + j * 46), line, font=font("Bold", 36), fill=(*c, int(255 * e)))
        fr.alpha_composite(lay); fire("pop", tin)
    show(fr, body("Exome or genome can be done in any of these ways", 32, MUTED), 1640, t, D * 0.7)

def sc_denovo(fr, t, D):
    dots(fr, 2); show(fr, kicker("Reason 1: de novo variants"), 260, t, 0.1)
    for i, (title, mut) in enumerate((("Patient", (4, "T")), ("Mother", None), ("Father", None))):
        tin = 0.4 + i * D * 0.12
        if t > tin: sanger(fr, X0, 340 + i * 280, TW, 250, t, tin, SEQ, mut, title=title)
    show(fr, gcard("Present in the patient, absent in both parents = de novo", AMBER, None, 34), 1200, t, D * 0.5)
    show(fr, gcard("Confirmed de novo = strong ACMG evidence (PS2); common in severe neurodevelopmental disorders", TEALG, None, 32), 1360, t, D * 0.65)

def sc_phase(fr, t, D):
    dots(fr, 3); show(fr, kicker("Reason 2: recessive disease (phase)"), 260, t, 0.1)
    show(fr, headline("Two variants in one gene: same copy or different copies?", 50), 320, t, 0.3)
    lay, d = overlay(fr); e = ease((t - D * 0.2) / 0.5)
    d.text((X0, 560), "In trans: compound heterozygous", font=font("Bold", 34), fill=(*TEALG, int(255 * e)))
    fr.alpha_composite(lay)
    phase(fr, X0, 630, t, D * 0.2, "trans")
    lay, d = overlay(fr); e = ease((t - D * 0.45) / 0.5)
    d.text((X0, 930), "In cis: both on one copy", font=font("Bold", 34), fill=(*CORAL, int(255 * e)))
    fr.alpha_composite(lay)
    phase(fr, X0, 1000, t, D * 0.45, "cis")
    show(fr, callout("Parents' testing shows the phase", AMBER, 36), 1320, t, D * 0.65); fire("ding", D * 0.65)

def sc_filter(fr, t, D):
    dots(fr, 4); show(fr, kicker("Reason 3: filtering"), 260, t, 0.1)
    lay, d = overlay(fr)
    steps = [("Variants in the patient", 1.0, CYAN), ("After quality & population filters", 0.8, LAV), ("After comparing with parents", 0.6, AMBER)]
    for i, (lab, w_, c) in enumerate(steps):
        tin = D * (0.1 + 0.18 * i); e = ease((t - tin) / 0.6)
        if t < tin: continue
        yy = 360 + i * 180; L = TW * w_
        d.rounded_rectangle((540 - L / 2, yy, 540 + L / 2, yy + 120), 30, fill=(*c, int(220 * e)))
        d.text((540, yy + 60), lab, font=font("Bold", 30), fill=(*INK, int(255 * e)), anchor="mm")
    fr.alpha_composite(lay)
    show(fr, gcard("Fewer variants to review, faster report", TEALG, 1, 35), 960, t, D * 0.6)
    show(fr, gcard("Often fewer VUS", AMBER, 2, 35), 1110, t, D * 0.72)
    fire("pop", D * 0.6); fire("pop", D * 0.72)

sc_caution = s_cards(5, "But be careful", "A variant in a healthy parent is not always harmless",
    [("Reduced penetrance", AMBER), ("Variable expressivity (different symptoms)", LAV), ("Mosaicism in a parent", CYAN),
     ("Consent: unexpected family-relationship findings are possible", CORAL)], size=34)

def sc_tan(fr, t, D):
    dots(fr, 6); show(fr, kicker("Evidence: head-to-head study"), 260, t, 0.1)
    bars(fr, X0, 330, TW, t, 0.4, [("Singleton", 36.7, CYAN), ("Trio", 40.0, TEALG)], "Same 30 children, exome analysed both ways")
    show(fr, gcard("Trio removed the need for separate parental Sanger testing", TEALG, 1, 33), 700, t, D * 0.3)
    show(fr, gcard("But total cost nearly doubled", CORAL, 2, 34), 850, t, D * 0.45)
    show(fr, gcard("Singleton first, trio only if undiagnosed: cost-saving", AMBER, 3, 33), 1000, t, D * 0.6)
    fire("pop", D * 0.3); fire("pop", D * 0.45); fire("pop", D * 0.6)
    show(fr, source_tag("Tan et al., Eur J Hum Genet 2019;27(12):1791-1799 (Australia)"), 1160, t, D * 0.7)

def sc_kiel(fr, t, D):
    dots(fr, 7); show(fr, kicker("Evidence: genome sequencing"), 260, t, 0.1)
    bars(fr, X0, 330, TW, t, 0.4, [("Singleton GS", 30.4, CYAN), ("Trio GS", 36.8, TEALG)], "448 patients with rare disease (prospective)")
    show(fr, gcard("Trio helps, but how much depends on patients and lab", AMBER, None, 34), 720, t, D * 0.5)
    show(fr, source_tag("Kaschta et al., Kiel (Germany), 2025: trio vs singleton genome sequencing"), 880, t, D * 0.6)
    family(fr, 540, 1080, t, D * 0.6)

def sc_india(fr, t, D):
    dots(fr, 8); show(fr, kicker("Data from India", CORAL), 260, t, 0.1)
    show(fr, headline("Trio exome in 137 children with autism (Mumbai)", 50), 320, t, 0.3)
    counter(fr, 16, "%", 480, t, 0.6, size=130, prefix="~")
    show(fr, body("had a pathogenic / likely pathogenic variant (22 of 137)", 34, SOFT), 650, t, 0.9)
    bars(fr, X0, 760, TW, t, D * 0.35, [("Syndromic", 35.0, CORAL), ("Non-syndromic", 8.2, CYAN)], "Yield by type of autism")
    show(fr, callout("91% of significant variants were de novo", AMBER, 36), 1140, t, D * 0.65); fire("ding", D * 0.65)
    show(fr, source_tag("Bajaj et al., J Hum Genet 2025;70:611-624 (NH SRCC Children's Hospital, Mumbai)"), 1290, t, D * 0.7)

def sc_choose(fr, t, D):
    dots(fr, 9); show(fr, kicker("Which to choose?"), 260, t, 0.1)
    flow(fr, t, D, [("Critically ill newborn?", "Trio (rapid): time matters", TEALG), ("Severe DD or multiple anomalies?", "Trio preferred", TEALG),
                    ("Prenatal anomaly?", "Trio", TEALG), ("Cost limits / parents unavailable?", "Singleton, then targeted parental tests", AMBER)], 340)

def sc_case1(fr, t, D):
    dots(fr, 10); show(fr, kicker("Case study", CORAL), 260, t, 0.1)
    show(fr, headline("A published case report", 58), 320, t, 0.3)
    put(fr, PAPER, 540, 800, 0.78, ease((t - 0.5) / 0.6))
    show(fr, gcard("5-year-old girl, healthy parents: motor & speech delay, poor coordination, attention problems", CYAN, None, 32), 1150, t, D * 0.4)
    show(fr, gcard("MRI, EMG and metabolic screen: normal", TEALG, None, 34), 1330, t, D * 0.55)
    show(fr, source_tag("Pan et al., Front Genet 2025;16 (China), CC BY"), 1470, t, D * 0.6)

def sc_case2(fr, t, D):
    dots(fr, 11); show(fr, kicker("Case: singleton exome, then parents"), 260, t, 0.1)
    show(fr, gcard("Singleton exome: SETBP1 c.1630C>T p.(Arg544Ter), nonsense", AMBER, 1, 33), 330, t, 0.3)
    fire("pop", 0.3)
    family(fr, 540, 640, t, D * 0.3, label=False)
    lay, d = overlay(fr); e = ease((t - D * 0.55) / 0.5)
    for x in (370, 710): d.text((x, 570), "absent", font=font("Bold", 30), fill=(*TEALG, int(255 * e)), anchor="mm")
    d.text((540, 905), "Patient: variant present", font=font("Bold", 30), fill=(*CORAL, int(255 * e)), anchor="mm")
    fr.alpha_composite(lay)
    show(fr, gcard("Sanger testing of parents and younger sister: variant absent in all three", TEALG, 2, 33), 980, t, D * 0.55)
    show(fr, callout("De novo confirmed", AMBER, 40), 1160, t, D * 0.7); fire("ding", D * 0.7)

sc_case3 = s_cards(12, "Case: the diagnosis", None,
    [("De novo confirmation supported a pathogenic classification", TEALG), ("Diagnosis: SETBP1-related intellectual disability (MRD29)", CYAN),
     ("Family counselled for future pregnancies", LAV), ("De novo: recurrence risk usually low, but not zero", AMBER)], size=33)

def sc_lesson(fr, t, D):
    dots(fr, 13); show(fr, kicker("The lesson"), 260, t, 0.1)
    flow(fr, t, D, [("Singleton exome finds a candidate", "Test parents for that variant", AMBER), ("Trio exome from the start", "Same answer, sooner", TEALG),
                    ("How to choose?", "Patient's condition, time and cost", CYAN)], 360)

sc_take = s_cards(14, "Key messages", None,
    [("Trio shows de novo status and phase", CYAN), ("Higher yield, but higher cost", AMBER), ("Singleton + targeted parental testing is a good option", TEALG),
     ("Send parents' samples together when possible", LAV), ("Every report with genetic counselling", CORAL)], size=33)

SC = [(film(sc0), "doc"), (film(sc_terms), "doc"), (film(sc_denovo), "doc"), (film(sc_phase), "doc"), (film(sc_filter), "doc"),
      (film(sc_caution), "doc"), (film(sc_tan), "doc"), (film(sc_kiel), "doc"), (film(sc_india), "doc"), (film(sc_choose), "doc"),
      (film(sc_case1), "doc"), (film(sc_case2), "doc"), (film(sc_case3), "doc"), (film(sc_lesson), "doc"), (film(sc_take), "doc"),
      (close_scene("Trio or singleton?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si, (fn, bg) in enumerate(SC):
            d = 16 if si < len(SC) - 1 else 33; NOW.update(t=d * .95, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * .95, d); ims.append(fr.convert("RGB").resize((300, 533)))
        s = Image.new("RGB", (300 * 6, 533 * 3), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 6) * 300, (i // 6) * 533))
        s.save("sheet_g003.png")
    else: run(SC, "/tmp/g003_", "Genetics_Ep03_Trio_vs_Singleton_Hindi.mp4", max_sec=480)
