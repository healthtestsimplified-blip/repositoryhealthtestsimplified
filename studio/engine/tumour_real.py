"""Tumour markers (PSA, CA-125, CA 19-9, CEA, AFP), realistic documentary style."""
import math, sys, random
from cbc_cartoon import run
from real_style import *
from hts_close import close_scene

TOPIC = "TUMOUR MARKERS"
NCH = 7
TUBE = tube_sprite((200, 60, 60), "SERUM")

def dots(fr, n): fr.alpha_composite(chapter(n, NCH), (0, 110))

def trend(fr, x, y, w, h, t, tin, title="Tumour marker over time (illustration)"):
    panel(fr, x, y, w, h, title)
    lay, d = overlay(fr); p = ease((t - tin) / 2.0)
    pts = [(0, 0.85), (0.15, 0.9), (0.3, 0.45), (0.45, 0.25), (0.6, 0.2), (0.75, 0.22), (0.9, 0.55), (1.0, 0.75)]
    x0, x1, y0, y1 = x + 40, x + w - 40, y + h - 80, y + 90
    P = [(x0 + u * (x1 - x0), y0 - v * (y0 - y1)) for u, v in pts]
    d.line((x0, y0, x1, y0), fill=(255, 255, 255, 80), width=2)
    vis = [q for q, (u, v) in zip(P, pts) if u <= p]
    if len(vis) > 1: d.line(vis, fill=CYAN, width=6)
    for q in vis: d.ellipse((q[0] - 9, q[1] - 9, q[0] + 9, q[1] + 9), fill=CYAN)
    if p > 0.32: d.text((P[2][0], y0 + 34), "Treatment", font=font("Bold", 26), fill=TEALG, anchor="mm")
    if p > 0.92: d.text((x1 - 10, y1 - 30), "Rising again: check", font=font("Bold", 26), fill=CORAL, anchor="rm")
    fr.alpha_composite(lay)

def marker_scene(n, kick, name, organ, col, also, note=None, src=None):
    def f(fr, t, D):
        dots(fr, n); show(fr, kicker(kick, col), 260, t, 0.1)
        lay, d = overlay(fr); e = ease((t - 0.3) / 0.6)
        d.text((X0, 330), name, font=font("Bold", 110), fill=(*col, int(255 * e)))
        d.text((X0, 480), organ, font=font("Medium", 38), fill=(*SOFT, int(255 * e)))
        fr.alpha_composite(lay)
        show(fr, body("Can also rise in:", 36, MUTED), 580, t, D * 0.25)
        for i, txt in enumerate(also):
            tin = D * (0.3 + 0.08 * i); fire("pop", tin)
            show(fr, gcard(txt, AMBER, i + 1, 33), 650 + i * 130, t, tin)
        yy = 650 + len(also) * 130 + 30
        if note: show(fr, callout(note, TEALG, 32), yy, t, D * 0.72)
        if src: show(fr, source_tag(src), yy + 120, t, D * 0.75)
    return f

# ---------------- scenes ----------------
def s_hook(fr, t, D):
    show(fr, kicker("Blood test explained", CYAN), 250, t, 0.1)
    type_on(fr, "Tumour Markers", 310, t, 0.3, 78)
    type_on(fr, "PSA • CA-125 • CEA • CA 19-9 • AFP", 420, t, 0.9, 40, AMBER)
    for i in range(3): put(fr, TUBE, 300 + i * 240, 820, 0.85, ease((t - 0.3 - 0.2 * i) / 0.5))
    show(fr, gcard("High report = cancer for sure?", CORAL, None, 38), 1150, t, D * 0.45)
    show(fr, callout("Watch till the end", CORAL, 38), 1600, t, D * 0.8)

def s_what(fr, t, D):
    dots(fr, 1); show(fr, kicker("What are tumour markers?"), 260, t, 0.1)
    show(fr, gcard("Proteins made by some cancer cells, or by the body in response to cancer", CYAN, 1, 33), 340, t, 0.3)
    show(fr, gcard("Measured with a blood test", TEALG, 2, 35), 510, t, D * 0.25)
    show(fr, callout("Can also rise in normal states and other diseases", AMBER, 34), 670, t, D * 0.5)
    fire("pop", 0.3); fire("pop", D * 0.25)
    put(fr, TUBE, 540, 1150, 1.0, ease((t - D * 0.55) / 0.5))

def s_use(fr, t, D):
    dots(fr, 2); show(fr, kicker("Main use"), 260, t, 0.1)
    show(fr, headline("Monitoring after a cancer diagnosis", 56), 320, t, 0.3)
    trend(fr, X0, 480, TW, 520, t, 0.6)
    show(fr, gcard("Screening with a panel of markers: not helpful", CORAL, 1, 34), 1060, t, D * 0.5)
    show(fr, gcard("The trend over time matters more than one report", TEALG, 2, 34), 1210, t, D * 0.65)
    show(fr, source_tag("NHS Scotland / IBMS tumour marker requesting guidance"), 1360, t, D * 0.7)

s_psa = marker_scene(3, "Men", "PSA", "Prostate", CYAN, ["Enlarged prostate (BPH)", "Urine infection, prostatitis", "Urinary catheter"],
                     "Sample taken before a rectal exam; free PSA adds information")
s_ca125 = marker_scene(4, "Women", "CA-125", "Ovary", LAV, ["Periods, pregnancy", "Endometriosis", "Liver or kidney disease"],
                       "High report does not always mean cancer")

def s_cea(fr, t, D):
    dots(fr, 5); show(fr, kicker("CEA and CA 19-9"), 260, t, 0.1)
    lay, d = overlay(fr); e = ease((t - 0.3) / 0.6)
    d.text((X0, 330), "CEA", font=font("Bold", 96), fill=(*TEALG, int(255 * e))); d.text((X0 + 330, 390), "Bowel (monitoring)", font=font("Medium", 34), fill=(*SOFT, int(255 * e)), anchor="lm")
    fr.alpha_composite(lay)
    show(fr, gcard("Also rises with smoking and inflammatory diseases", AMBER, None, 33), 480, t, D * 0.2)
    if t > D * 0.45:
        lay, d = overlay(fr); e = ease((t - D * 0.45) / 0.6)
        d.text((X0, 700), "CA 19-9", font=font("Bold", 96), fill=(*CORAL, int(255 * e))); d.text((X0 + 430, 760), "Pancreas, bile duct", font=font("Medium", 34), fill=(*SOFT, int(255 * e)), anchor="lm")
        fr.alpha_composite(lay)
    show(fr, gcard("Also rises in jaundice and pancreatitis", AMBER, None, 33), 850, t, D * 0.55)
    show(fr, gcard("Some people cannot make CA 19-9 at all", LAV, None, 33), 1000, t, D * 0.7)

s_afp = marker_scene(6, "AFP", "AFP", "Liver; some testis/ovary tumours", AMBER, ["Hepatitis, cirrhosis", "Pregnancy"],
                     "Chronic liver disease: doctor may check it with ultrasound")

def s_remember(fr, t, D):
    dots(fr, 7); show(fr, kicker("Remember"), 260, t, 0.1)
    for i, (txt, c) in enumerate((("Normal report does not fully rule out cancer", AMBER), ("High report is not a cancer diagnosis", CORAL),
                                  ("Diagnosis needs scans and biopsy", CYAN), ("Follow-up tests in the same lab; don't panic", TEALG))):
        fire("pop", D * (0.1 + 0.15 * i)); show(fr, gcard(txt, c, i + 1, 34), 340 + i * 150, t, D * (0.1 + 0.15 * i))
    trend(fr, X0, 980, TW, 440, t, D * 0.5, "Watch the trend (illustration)")

SC = [(film(s_hook), "doc"), (film(s_what), "doc"), (film(s_use), "doc"), (film(s_psa), "doc"), (film(s_ca125), "doc"),
      (film(s_cea), "doc"), (film(s_afp), "doc"), (film(s_remember), "doc"), (close_scene("Had a tumour marker test?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si, (fn, bg) in enumerate(SC):
            d = 16 if si < len(SC) - 1 else 33; p = .95 if si else 0.125; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((360, 640)))
        s = Image.new("RGB", (360 * 5, 640 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 360, (i // 5) * 640))
        s.save("sheet_tum.png")
    else: run(SC, "/tmp/tum_", "Tumour_Markers_Hindi.mp4")
