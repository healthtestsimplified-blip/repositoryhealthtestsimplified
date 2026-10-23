"""TPMT & NUDT15 gene test (thiopurine safety), short public video, realistic documentary style."""
import math, sys, random
from cbc_cartoon import run
from real_style import *
from hts_close import close_scene

TOPIC = "TPMT & NUDT15 GENE TEST"
NCH = 7

def dots(fr, n): fr.alpha_composite(chapter(n, NCH), (0, 110))

def cards(fr, t, D, items, y0=340, size=35, gap=145, t0=0.1, step=0.11):
    for i, (txt, c) in enumerate(items):
        fire("pop", D * (t0 + step * i)); show(fr, gcard(txt, c, i + 1, size), y0 + i * gap, t, D * (t0 + step * i))

def pill(d, cx, cy, w, h, c1, c2, a):
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), int(h / 2), fill=(*c1, a))
    d.rounded_rectangle((cx, cy - h / 2, cx + w / 2, cy + h / 2), int(h / 2), fill=(*c2, a))
    d.rectangle((cx, cy - h / 2, cx + h / 2, cy + h / 2), fill=(*c2, a))

def pills(fr, y, t, tin):
    lay, d = overlay(fr); e = ease((t - tin) / 0.6); a = int(255 * e)
    for i, (lab, c) in enumerate((("Azathioprine", CYAN), ("6-Mercaptopurine", AMBER))):
        cx = 300 + i * 480
        pill(d, cx, y, 220, 90, (240, 244, 250), c, a)
        d.text((cx, y + 95), lab, font=font("Bold", 32), fill=(*SOFT, a), anchor="mm")
    fr.alpha_composite(lay)

def flowdrug(fr, y, t, tin, slow=False):
    """Drug -> enzymes (TPMT, NUDT15) -> safe level; if gene change, drug builds up."""
    lay, d = overlay(fr); e = ease((t - tin) / 0.6); a = int(255 * e)
    boxes = [("Medicine", CYAN), ("TPMT + NUDT15", TEALG if not slow else CORAL), ("Safe level" if not slow else "Builds up", TEALG if not slow else CORAL)]
    for i, (lab, c) in enumerate(boxes):
        x = X0 + i * (TW / 3)
        d.rounded_rectangle((x + 10, y, x + TW / 3 - 30, y + 110), 22, fill=(*c, int(200 * e)))
        d.text((x + TW / 6 - 10, y + 55), lab, font=font("Bold", 28), fill=(*INK, a), anchor="mm")
        if i < 2: d.polygon([(x + TW / 3 - 24, y + 40), (x + TW / 3 - 4, y + 55), (x + TW / 3 - 24, y + 70)], fill=(*SOFT, a))
    fr.alpha_composite(lay)

def bars(fr, y, rows, t, tin, vmax):
    lay, d = overlay(fr); e = ease((t - tin) / 1.2)
    for i, (lab, v, txt, c) in enumerate(rows):
        yy = y + i * 130
        d.text((X0, yy + 30), lab, font=font("Medium", 32), fill=SOFT, anchor="lm")
        L = max(16, (TW - 470) * v / vmax * e)
        d.rounded_rectangle((X0 + 290, yy, X0 + 290 + L, yy + 60), 30, fill=c)
        d.text((X0 + 310 + L, yy + 30), txt, font=font("Bold", 32), fill=WHITE, anchor="lm")
    fr.alpha_composite(lay)

def gauge(fr, y, t, tin):
    """Three result types with the dose message."""
    lay, d = overlay(fr)
    rows = [("Normal", "Usual dose", TEALG), ("Intermediate", "Doctor may start lower", AMBER), ("Poor metabolizer", "Much lower dose or another medicine", CORAL)]
    for i, (lab, msg, c) in enumerate(rows):
        e = ease((t - tin - i * 0.7) / 0.5); a = int(255 * e); yy = y + i * 190
        d.rounded_rectangle((X0, yy, X0 + 300, yy + 140), 24, fill=(*c, int(230 * e)))
        d.text((X0 + 150, yy + 70), lab, font=font("Bold", 30), fill=(*INK, a), anchor="mm")
        d.rounded_rectangle((X0 + 320, yy, X0 + TW, yy + 140), 24, fill=(255, 255, 255, int(22 * e)), outline=(*c, a), width=3)
        ls = wrap(msg, font("Medium", 32), TW - 380); y1 = yy + 70 - (len(ls) - 1) * 21
        for j, line in enumerate(ls):
            d.text((X0 + 350, y1 + j * 42), line, font=font("Medium", 32), fill=(*SOFT, a), anchor="lm")
    fr.alpha_composite(lay)

# ---------------- scenes ----------------
def s_hook(fr, t, D):
    show(fr, kicker("Gene test before medicine", CYAN), 250, t, 0.0)
    show(fr, headline("TPMT & NUDT15", 78), 310, t, -1)
    show(fr, headline("gene test", 78), 410, t, -1)
    if t > D * 0.25: type_on(fr, "Before azathioprine or 6-MP", 530, t, D * 0.25, 44, AMBER)
    pills(fr, 800, t, -1)
    show(fr, callout("Watch till the end", CORAL, 38), 1600, t, D * 0.8)

def s_what(fr, t, D):
    dots(fr, 1); show(fr, kicker("Thiopurine medicines"), 260, t, 0.1)
    pills(fr, 420, t, 0.3)
    cards(fr, t, D, [("Inflammatory bowel disease: Crohn's, ulcerative colitis", CYAN), ("Blood cancer: acute lymphoblastic leukaemia (ALL)", CORAL),
                     ("Some autoimmune diseases", LAV)], 640, 33, 150, 0.25, 0.15)

def s_how(fr, t, D):
    dots(fr, 2); show(fr, kicker("Why the genes matter"), 260, t, 0.1)
    flowdrug(fr, 340, t, 0.3, slow=False)
    show(fr, body("Gene change: the enzymes work less", 36, AMBER), 520, t, D * 0.3)
    flowdrug(fr, 590, t, D * 0.35, slow=True)
    cards(fr, t, D, [("Bone marrow is suppressed", CORAL), ("Very low white cells: repeated infections", AMBER), ("Risk of bleeding", LAV)], 800, 34, 145, 0.5, 0.1)

def s_india(fr, t, D):
    dots(fr, 3); show(fr, kicker("Indian data"), 260, t, 0.1)
    show(fr, headline("119 IBD patients on thiopurines", 52), 320, t, 0.3)
    bars(fr, 470, [("NUDT15 change", 10.9, "10.9%", CORAL), ("TPMT change", 4.2, "4.2%", AMBER)], t, 0.6, 15)
    show(fr, gcard("With the NUDT15 change, over half (53.8%) had low white cells", CORAL, None, 32), 760, t, D * 0.4)
    show(fr, gcard("In Indians, NUDT15 matters as much as TPMT", TEALG, None, 34), 920, t, D * 0.6)
    show(fr, source_tag("Grover et al., BMC Gastroenterology 2021;21:327 (North India), CC BY"), 1080, t, D * 0.65)

def s_result(fr, t, D):
    dots(fr, 4); show(fr, kicker("What the report says"), 260, t, 0.1)
    gauge(fr, 340, t, 0.3)
    show(fr, source_tag("CPIC guideline for thiopurines, TPMT and NUDT15 (Relling et al., 2019)"), 940, t, D * 0.6)
    show(fr, callout("Dose is decided only by your doctor", AMBER, 36), 1040, t, D * 0.7)

def s_who(fr, t, D):
    dots(fr, 5); show(fr, kicker("Who should get tested?"), 260, t, 0.1)
    cards(fr, t, D, [("Before starting azathioprine or 6-mercaptopurine", CYAN), ("People with IBD (Crohn's, ulcerative colitis)", AMBER),
                     ("Children and adults with ALL", CORAL), ("Earlier side effects from these medicines", LAV)], 340, 33, 150, 0.08, 0.12)

def s_test(fr, t, D):
    dots(fr, 6); show(fr, kicker("The test"), 260, t, 0.1)
    put(fr, tube_sprite((149, 117, 205), "EDTA"), 330, 640, 1.0, ease((t - 0.3) / 0.5))
    lay, d = overlay(fr); e = ease((t - 0.5) / 0.5)
    d.text((330, 950), "Blood (EDTA)", font=font("Bold", 34), fill=(*SOFT, int(255 * e)), anchor="mm"); fr.alpha_composite(lay)
    show(fr, gcard("No fasting needed", TEALG, 1, 34), 1010, t, D * 0.3)
    show(fr, gcard("Genes do not change: usually tested once in life", AMBER, 2, 33), 1160, t, D * 0.5)
    fire("pop", D * 0.3); fire("pop", D * 0.5)

def s_remember(fr, t, D):
    dots(fr, 7); show(fr, kicker("Remember"), 260, t, 0.1)
    cards(fr, t, D, [("Even with a normal report, CBC checks continue as advised", CYAN), ("Never change the dose yourself", CORAL)], 340, 33, 170, 0.12, 0.25)
    show(fr, callout("Safer medicine starts with the right test", TEALG, 36), 760, t, D * 0.7); fire("ding", D * 0.7)

SC = [(film(s_hook), "doc"), (film(s_what), "doc"), (film(s_how), "doc"), (film(s_india), "doc"), (film(s_result), "doc"),
      (film(s_who), "doc"), (film(s_test), "doc"), (film(s_remember), "doc"), (close_scene("Ever been given azathioprine?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si, (fn, bg) in enumerate(SC):
            d = 16 if si < len(SC) - 1 else 33; p = 0.95 if si else 0.01; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((360, 640)))
        s = Image.new("RGB", (360 * 5, 640 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 360, (i // 5) * 640))
        s.save("/tmp/sheet_tpmt.png")
    elif len(sys.argv) > 1 and sys.argv[1] == "bn": run(SC, "/tmp/tpmtbn_", "TPMT_NUDT15_Test_Bengali.mp4")
    else: run(SC, "/tmp/tpmt_", "TPMT_NUDT15_Test_Hindi.mp4")
