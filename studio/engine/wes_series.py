"""Whole Exome Sequencing clinical series for doctors (4 episodes), realistic documentary style.
Usage: python3 wes_series.py <w1|w2|w3|w4> [preview]"""
import math, sys
from cbc_cartoon import run
from real_style import *
from hts_close import close_scene

TUBE = tube_sprite()
US = us_base()
CHR = chromosome_sprite("A chromosome", 0.55, "Exons = coding parts")
SEQ = "CCTTGGACCCAGAGGTTCTTTG"

def dots(fr, n, tot=7): fr.alpha_composite(chapter(n, tot), (0, 110))
def label(fr, text, x, y, col=SOFT, size=32, anchor="mm", weight="Medium"):
    lay, d = overlay(fr); d.text((x, y), text, font=font(weight, size), fill=col, anchor=anchor); fr.alpha_composite(lay)

# ---------------- scene factories ----------------
def s_hook(ep_label, line1, line2, visual):
    def f(fr, t, D):
        visual(fr, t, D)
        show(fr, kicker(ep_label, CYAN), 330, t, 0.1)
        type_on(fr, line1, 410, t, 0.4, 62)
        if t > D * 0.35: type_on(fr, line2, 620, t, D * 0.35, 58, AMBER)
        show(fr, callout("Whole Exome Sequencing: clinical uses", CYAN, 38), 1660, t, D * 0.6); fire("whoosh", D * 0.6)
    return f

def s_what(n):
    def f(fr, t, D):
        dots(fr, n); show(fr, kicker("What WES reads"), 260, t, 0.1)
        show(fr, headline("Coding parts (exons) of ~20,000 genes in one test", 54), 320, t, 0.3)
        p = ease((t - 0.4) / 0.8)
        if p > 0: put(fr, CHR, 60 + CHR.width * 0.7 / 2, 500 + CHR.height * 0.7 / 2, 0.7, p)
        exon_bar(fr, X0, 1140, TW, None, "Exons of one gene", t=t, tin=D * 0.3)
        if t > D * 0.45: sanger(fr, X0, 1260, TW, 330, t, D * 0.45, SEQ, (9, "C"), title="Variant found (example)")
        fire("pop", D * 0.45)
    return f

def s_bars(n, kick, head, rows, src, note=None):
    def f(fr, t, D):
        dots(fr, n); show(fr, kicker(kick), 260, t, 0.1)
        show(fr, headline(head, 54), 320, t, 0.3)
        lay, d = overlay(fr); y = 560
        for i, row in enumerate(rows):
            lab, v, c = row[:3]; txt_override = row[3] if len(row) > 3 else None
            tin = D * (0.15 + 0.15 * i)
            if t < tin: continue
            fire("pop", tin); e = ease((t - tin) / 0.8)
            yy = y + i * 165
            d.text((X0, yy), lab, font=font("Medium", 34), fill=SOFT)
            d.rounded_rectangle((X0, yy + 56, X0 + TW, yy + 110), 27, fill=(255, 255, 255, 25))
            d.rounded_rectangle((X0, yy + 56, X0 + max(54, TW * v / 100 * e), yy + 110), 27, fill=c)
            txt = txt_override if (txt_override and e > 0.98) else (f"~{v * e:.0f}%" if float(v).is_integer() else f"~{v * e:.1f}%")
            d.text((X0 + max(54, TW * v / 100 * e) + 16, yy + 83), txt, font=font("Bold", 38), fill=WHITE, anchor="lm")
        fr.alpha_composite(lay)
        yb = y + len(rows) * 165 + 30
        if note: show(fr, gcard(note, TEALG, None, 34), yb, t, D * 0.7)
        show(fr, source_tag(src), yb + (150 if note else 0), t, D * 0.75)
        v_helix_low(fr, t, D)
    return f

def s_cards(n, kick, head, items, visual=None, vy=None):
    def f(fr, t, D):
        dots(fr, n); show(fr, kicker(kick), 260, t, 0.1)
        y = 320
        if head: show(fr, headline(head, 54), 320, t, 0.3); y = 470
        for i, (txt, c) in enumerate(items):
            fire("pop", D * (0.1 + 0.13 * i)); show(fr, gcard(txt, c, i + 1, 35), y + i * 150, t, D * (0.1 + 0.13 * i))
        if visual: visual(fr, t, D, y + len(items) * 150 + 40)
        else: v_helix_low(fr, t, D)
    return f

def s_quote(n, kick, quote, src, visual=None):
    def f(fr, t, D):
        dots(fr, n); show(fr, kicker(kick, TEALG), 260, t, 0.1)
        lay, d = overlay(fr); e = ease((t - 0.3) / 0.6)
        d.text((X0 - 10, 300), "“", font=font("Bold", 200), fill=(*TEALG, int(140 * e)))
        fr.alpha_composite(lay)
        show(fr, headline(quote, 50, WHITE, "Medium", spacing=1.3), 470, t, 0.5)
        show(fr, source_tag(src), 1150, t, D * 0.5)
        if visual: visual(fr, t, D)
    return f

def s_stat(n, kick, big, sub, cards, visual=None):
    def f(fr, t, D):
        dots(fr, n); show(fr, kicker(kick), 260, t, 0.1)
        lay, d = overlay(fr); e = ease((t - 0.3) / 0.6)
        d.text((X0, 330), big, font=font("Bold", 130), fill=(*AMBER, int(255 * e)))
        d.text((X0, 500), sub, font=font("Regular", 38), fill=(*SOFT, int(255 * e)))
        fr.alpha_composite(lay)
        if visual: visual(fr, t, D)
        for i, (txt, c) in enumerate(cards):
            fire("pop", D * (0.35 + 0.15 * i)); show(fr, gcard(txt, c, None, 35), 1180 + i * 150, t, D * (0.35 + 0.15 * i))
    return f

# ---------------- visuals ----------------
def v_helix(fr, t, D): helix(fr, 760, 1200, 720, t, amp=170, alpha=150)
def v_helix_low(fr, t, D): helix(fr, 540, 1560, 360, t, amp=300, turns=1.2, alpha=70, n=30)
def v_us(fr, t, D): ultrasound(fr, 90, 820, t, US, 0)
def v_tube(fr, t, D, y=1250): put(fr, TUBE, 540, y + 180, 0.7, ease((t - D * 0.3) / 0.6))
def v_ped(fr, t, D, y=1250): pedigree(fr, y + 80, t, D * 0.4, "Affected")
def v_seq(fr, t, D, y=1250): sanger(fr, X0, y, TW, 330, t, D * 0.5, SEQ, (9, "C"), title="Trio: child vs parents")
def v_clock(fr, t, D):
    lay, d = overlay(fr); cx, cy, r = 540, 850, 220
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(255, 255, 255, 120), width=8)
    for k in range(12):
        a = k / 12 * 2 * math.pi; d.line((cx + 0.85 * r * math.cos(a), cy + 0.85 * r * math.sin(a), cx + 0.95 * r * math.cos(a), cy + 0.95 * r * math.sin(a)), fill=(255, 255, 255, 140), width=4)
    a = -math.pi / 2 + t * 1.5; d.line((cx, cy, cx + 0.8 * r * math.cos(a), cy + 0.8 * r * math.sin(a)), fill=AMBER, width=10)
    a2 = -math.pi / 2 + t * 0.12; d.line((cx, cy, cx + 0.5 * r * math.cos(a2), cy + 0.5 * r * math.sin(a2)), fill=WHITE, width=12)
    fr.alpha_composite(lay)
def v_kidney(fr, t, D):
    from flc_real import KIDNEY
    put(fr, KIDNEY, 860, 520, 0.6, ease((t - 0.5) / 0.6))

# ---------------- episodes ----------------
EPS = {
 "w1": dict(title="WES_Ep1_Child_Development_Epilepsy_Hindi.mp4", topic="WES SERIES  •  EP 1: CHILD NEURO", q="Children with no diagnosis yet?", scenes=[
    s_hook("WES series  •  Episode 1 of 4", "Developmental delay? Intellectual disability?", "Early-onset epilepsy?", v_helix),
    s_what(1),
    s_bars(2, "Diagnostic yield", "Neurodevelopmental disorders", [("WES, all NDD", 36, CYAN), ("WES, NDD + other conditions", 53, TEALG), ("Chromosomal microarray", 17.5, (150, 165, 190), "15–20%")],
           "Srivastava et al., Genet Med 2019 (meta-analysis); CMA ~15–20%"),
    s_bars(3, "Epilepsy", "Systematic review, 154 studies", [("Exome sequencing", 24, AMBER)], "Sheidley et al., Epilepsia (systematic review)",
           "A genetic cause can also help plan treatment"),
    s_quote(4, "Guideline", "ACMG 2021: ES/GS as a first- or second-tier test for congenital anomalies (onset before 1 year) or developmental delay / intellectual disability (onset before 18 years).",
            "Manickam et al., Genet Med 2021", v_helix_low),
    s_cards(5, "Sending a sample", None, [("EDTA blood sample", CORAL), ("Full clinical details, previous tests, family history", CYAN), ("Trio with both parents, when possible", AMBER), ("Genetic counselling before and after", TEALG)], v_seq),
    s_cards(6, "Know the limits", None, [("Misses repeat expansions (e.g. Fragile X)", CORAL), ("Misses mitochondrial DNA and many large deletions", AMBER), ("Variants of uncertain significance (VUS) can be reported", LAV), ("Negative report: can be reanalysed later", TEALG)]),
 ]),
 "w2": dict(title="WES_Ep2_Fetal_Anomalies_Hindi.mp4", topic="WES SERIES  •  EP 2: FETAL", q="Do you see such cases in your clinic?", scenes=[
    s_hook("WES series  •  Episode 2 of 4", "Fetal anomaly on scan?", "Karyotype & microarray normal?", v_us),
    s_cards(1, "When to consider prenatal exome", "Society guidance", [("Multiple anomalies", CORAL), ("One major anomaly suggesting a genetic disorder", AMBER), ("Microarray negative / non-diagnostic", CYAN)], v_tube),
    s_bars(2, "Diagnostic yield", "After normal karyotype + microarray", [("PAGE study (610 trios)", 8.5, CYAN), ("Petrovski et al. (234 trios)", 10, TEALG), ("Multiple anomalies (PAGE)", 15.4, AMBER)],
           "Lord et al., Lancet 2019; Petrovski et al., Lancet 2019", "Skeletal anomalies: higher (15–24%)"),
    s_cards(3, "Previous affected pregnancy", "Undiagnosed prior child or fetus with similar anomalies?", [("Finding the cause helps plan testing in the next pregnancy", TEALG)], v_ped),
    s_cards(4, "Requirements", None, [("Trio: fetus + both parents", CYAN), ("Fetal sample by CVS or amniocentesis", AMBER), ("Detailed ultrasound findings with the sample", TEALG)], v_seq),
    s_cards(5, "Counselling", None, [("Detailed pre- and post-test counselling", CYAN), ("Uncertain variants possible; results take time", AMBER), ("For disease only. Baby's sex is never disclosed.", CORAL)]),
    s_cards(6, "Limits", "Prenatal yield is lower than after birth", [("Only ultrasound features are available", AMBER), ("Reanalysis with new findings can help later", TEALG)], lambda fr, t, D, y: ultrasound(fr, 90, y + 10, t, US, 0)),
 ]),
 "w3": dict(title="WES_Ep3_NICU_Rapid_Exome_Hindi.mp4", topic="WES SERIES  •  EP 3: NICU", q="Such infants in your NICU?", scenes=[
    s_hook("WES series  •  Episode 3 of 4", "Critically ill newborn?", "Cause still unclear?", v_helix),
    s_cards(1, "Which newborns?", None, [("Multiple congenital anomalies", CORAL), ("Unexplained seizures or severe hypotonia", AMBER), ("Metabolic crisis", CYAN), ("Unusual combination of features, initial tests negative", LAV)]),
    s_bars(2, "Diagnostic yield", "278 infants in ICU (JAMA Pediatrics 2017)", [("All exome types", 36.7, CYAN), ("Rapid (critical) trio exome", 50.8, TEALG)], "Meng et al., JAMA Pediatrics 2017"),
    s_stat(3, "Speed", "~13 days", "median turnaround, rapid trio exome", [("Answers while decisions are still being made", TEALG)], v_clock),
    s_bars(4, "Impact", "Among infants with a diagnosis", [("Management changed", 52, AMBER)], "Meng et al., JAMA Pediatrics 2017", "Families also get accurate recurrence-risk counselling"),
    s_cards(5, "Requirements", None, [("EDTA samples: baby + both parents", CYAN), ("Newborn: about 1–2 mL blood is enough", AMBER), ("Clinical summary and test results with the sample", TEALG), ("Family counselling", LAV)], v_tube),
    s_cards(6, "Note", None, [("Turnaround differs by lab", AMBER), ("Results are read with the clinical team and a genetics expert", TEALG)], v_seq),
 ]),
 "w4": dict(title="WES_Ep4_Adult_Specialties_Hindi.mp4", topic="WES SERIES  •  EP 4: ADULTS", q="One disease running in a family?", scenes=[
    s_hook("WES series  •  Episode 4 of 4", "Genetic disease in adults?", "Early onset? Family history?", v_helix),
    s_bars(1, "Adults", "486 adults with exome sequencing", [("All adults", 17.5, CYAN), ("Age 18–30", 23.9, TEALG), ("Over 30", 10.4, (150, 165, 190))], "Posey et al., Genet Med 2016"),
    s_bars(2, "Kidney disease", "3,315 patients with CKD (NEJM 2019)", [("All CKD", 9.3, CYAN), ("Nephropathy of unknown cause", 17.1, AMBER)], "Groopman et al., N Engl J Med 2019"),
    s_cards(3, "Other uses", None, [("Inherited cardiomyopathy & arrhythmia", CORAL), ("Neuromuscular disorders", AMBER), ("Inherited retinal disease", CYAN), ("Early-onset unusual neurological features", LAV)]),
    s_cards(4, "Why a diagnosis helps", None, [("Right treatment", TEALG), ("Better idea of prognosis", CYAN), ("Cascade testing of relatives", AMBER)], v_seq),
    s_cards(5, "Requirements", None, [("EDTA blood sample", CORAL), ("Detailed clinical information", CYAN), ("Family history: at least 3 generations", AMBER), ("Sometimes a targeted gene panel first", LAV)]),
    s_cards(6, "Consent & follow-up", None, [("Consent before testing", CYAN), ("Decide about secondary findings", AMBER), ("Negative / uncertain reports can be reviewed later", TEALG)], v_tube),
 ]),
}

if __name__ == "__main__":
    ep = sys.argv[1]; E = EPS[ep]
    SC = [(film(fn), "doc") for fn in E["scenes"]] + [(close_scene(E["q"], E["topic"]), "docl")]
    if len(sys.argv) > 2 and sys.argv[2] == "preview":
        ims = []
        for si, (fn, bg) in enumerate(SC):
            d = 16 if si < len(SC) - 1 else 33; p = 0.95; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((360, 640)))
        s = Image.new("RGB", (360 * 4, 640 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 4) * 360, (i // 4) * 640))
        s.save(f"sheet_{ep}.png")
    else: run(SC, f"/tmp/{ep}_", E["title"])
