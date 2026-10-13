"""Protein electrophoresis (SPEP), realistic documentary style."""
import math, sys
from cbc_cartoon import run
from real_style import *
from hts_close import close_scene

TOPIC = "PROTEIN ELECTROPHORESIS  •  SPEP"
FILM = spep_film(8, 1400, 1400, 3)
TUBE = tube_sprite((200, 40, 40), "SERUM")
REPORT = report_sprite()

def dots(fr, n): fr.alpha_composite(chapter(n, 9), (0, 110))
def label(fr, text, x, y, col=SOFT, size=32, anchor="mm", weight="Medium"):
    lay, d = overlay(fr); d.text((x, y), text, font=font(weight, size), fill=col, anchor=anchor); fr.alpha_composite(lay)
def lane(fr, prof, x, y, w, h, prog=1.0, a=1.0):
    s = spep_strip(w, h, prof, prog)
    if a < 1: s.putalpha(s.getchannel("A").point(lambda v: int(v * a)))
    fr.alpha_composite(s, (int(x), int(y)))

FILM_TILT = with_glow(FILM.resize((860, 860)).rotate(-7, expand=True, resample=Image.BICUBIC), (0, 0, 0), 30, 200)
def p_hook(fr, t, D):
    put(fr, FILM_TILT, 540, 1170, 0.7 + 0.04 * t / D, ease(t / 0.8))
    show(fr, kicker("Protein electrophoresis  •  SPEP", CYAN), 330, t, 0.1)
    type_on(fr, "Total protein high?", 410, t, 0.4, 72)
    if t > D * 0.35: type_on(fr, "What is an M-spike?", 600, t, D * 0.35, 72, AMBER)
    show(fr, callout("Protein electrophoresis, explained", CYAN, 40), 1620, t, D * 0.6); fire("whoosh", D * 0.6)

def p_what(fr, t, D):
    dots(fr, 1)
    show(fr, kicker("What is it?"), 260, t, 0.1)
    show(fr, headline("Serum on a gel + electric current = proteins separate", 54), 320, t, 0.3)
    put(fr, TUBE, 170, 760, 0.85, ease((t - 0.4) / 0.5))
    lay, d = overlay(fr)
    d.rounded_rectangle((310, 600, 1010, 920), 24, fill=(40, 60, 90, 200), outline=(255, 255, 255, 60), width=2)
    d.text((340, 760), "+", font=font("Bold", 70), fill=CORAL, anchor="mm"); d.text((985, 760), "−", font=font("Bold", 70), fill=CYAN, anchor="mm")
    fr.alpha_composite(lay)
    prog = ease((t - D * 0.2) / (D * 0.55))
    for k, kind in enumerate(("normal", "normal", "normal")):
        lane(fr, spep_profile(kind), 370, 640 + k * 95, 580, 70, max(0.02, prog))
    if t > D * 0.2:
        for k in range(5):
            x = 960 - (t * 120 + k * 120) % 560
            label(fr, "⚡" if False else "•", x, 935, AMBER, 40)
    show(fr, gcard("Proteins move by size and charge, and form separate bands", CYAN, None, 36), 1020, t, D * 0.6)

def p_fractions(fr, t, D):
    dots(fr, 2)
    show(fr, kicker("Five parts"), 260, t, 0.1)
    show(fr, headline("Albumin, alpha-1, alpha-2, beta, gamma", 54), 320, t, 0.3)
    lane(fr, spep_profile("normal"), X0 + 30, 490, TW - 60, 80, 1.0, ease((t - 0.4) / 0.5))
    densito(fr, X0, 610, TW, 460, spep_profile("normal"), t, 0.6, "Densitometry scan")
    show(fr, gcard("Gamma = immunoglobulins (antibodies), made by plasma cells", AMBER, None, 36), 1110, t, D * 0.55)

def p_when(fr, t, D):
    dots(fr, 3)
    show(fr, kicker("When is it advised?"), 260, t, 0.1)
    items = [("Unexplained anaemia", CORAL), ("Bone pain", AMBER), ("Repeated infections", CYAN), ("Kidney problems", LAV), ("High calcium or high total protein", TEALG)]
    for i, (txt, c) in enumerate(items):
        fire("pop", D * (0.08 + 0.13 * i)); show(fr, gcard(txt, c, i + 1, 38), 360 + i * 150, t, D * (0.08 + 0.13 * i))
    show(fr, callout("Key test when multiple myeloma is suspected", AMBER, 38), 1150, t, D * 0.8)

def p_mspike(fr, t, D):
    dots(fr, 4)
    show(fr, kicker("The M-spike"), 260, t, 0.1)
    densito(fr, X0, 340, TW, 380, spep_profile("normal"), t, 0.4, "Normal: broad gamma", shade=False)
    lane(fr, spep_profile("normal"), X0 + 30, 735, TW - 60, 50, 1.0, ease((t - 0.4) / 0.5))
    if t > D * 0.4:
        densito(fr, X0, 830, TW, 380, spep_profile("mspike"), t, D * 0.4, "M-spike: one tall, narrow peak", col=AMBER, shade=False, highlight=0.82)
        lane(fr, spep_profile("mspike"), X0 + 30, 1225, TW - 60, 50, 1.0, ease((t - D * 0.4) / 0.5)); fire("boom", D * 0.55)
    show(fr, gcard("One group of plasma cells making lots of ONE protein = monoclonal protein", AMBER, None, 35), 1320, t, D * 0.7)

def p_mgus(fr, t, D):
    dots(fr, 5)
    show(fr, kicker("M-spike is not always cancer", TEALG), 260, t, 0.1)
    show(fr, headline("Most often it is MGUS, which is not cancer", 56), 320, t, 0.3)
    lay, d = overlay(fr)
    if t > D * 0.3:
        e = ease((t - D * 0.3) / 0.6)
        d.text((X0, 520), "About 3 in 100", font=font("Bold", 100), fill=(*AMBER, int(255 * e)))
        d.text((X0, 650), "people over 50 have MGUS", font=font("Regular", 40), fill=(*SOFT, int(255 * e)))
        for k in range(100):
            r, c = divmod(k, 20); x = X0 + 20 + c * 46; y = 760 + r * 50
            col = AMBER if k in (13, 48, 77) else (80, 100, 130)
            if k / 100 < e: d.ellipse((x - 12, y - 12, x + 12, y + 12), fill=col)
    if t > D * 0.6:
        e = ease((t - D * 0.6) / 0.6)
        d.text((X0, 1050), "About 1% per year may progress", font=font("Bold", 50), fill=(*CORAL, int(255 * e)))
    fr.alpha_composite(lay)
    show(fr, callout("So regular follow-up tests matter", TEALG, 40), 1180, t, D * 0.75)
    show(fr, source_tag("Mayo Clinic"), 1320, t, D * 0.75)

def p_patterns(fr, t, D):
    dots(fr, 6)
    show(fr, kicker("Other patterns"), 260, t, 0.1)
    rows = [("lowalb", "Low albumin", "liver or kidney disease, poor nutrition", CYAN, 0.18),
            ("alpha2", "High alpha-2", "inflammation, nephrotic syndrome", LAV, 0.5),
            ("poly", "Broad high gamma", "chronic infection, autoimmune disease", AMBER, 0.84)]
    for i, (k, a, b, c, hl) in enumerate(rows):
        tin = D * (0.1 + 0.25 * i); fire("pop", tin)
        if t < tin: continue
        y = 350 + i * 440
        densito(fr, X0, y, TW, 290, spep_profile(k), t, tin, None, labels=False, col=c, shade=False, highlight=hl)
        label(fr, a, X0, y + 320, c, 40, "lm", "Bold"); label(fr, b, X0, y + 372, SOFT, 32, "lm")

def p_next(fr, t, D):
    dots(fr, 7)
    show(fr, kicker("Next tests if M-spike found"), 260, t, 0.1)
    ife_gel(fr, X0, 330, TW, 560, t, 0.4)
    label(fr, "Example: IgG kappa", 540, 930, AMBER, 38, weight="Bold")
    show(fr, gcard("Immunofixation: which type of protein (IgG, IgA, IgM; kappa or lambda)", CYAN, 1, 34), 1000, t, D * 0.3)
    show(fr, gcard("Serum free light chains + urine protein test", LAV, 2, 36), 1150, t, D * 0.5)
    show(fr, gcard("Bone marrow test, if the doctor advises", CORAL, 3, 36), 1280, t, D * 0.68)
    for k in (0.3, 0.5, 0.68): fire("pop", D * k)

def p_prep(fr, t, D):
    dots(fr, 8)
    show(fr, kicker("Preparation & report"), 260, t, 0.1)
    show(fr, headline("Usually just one blood sample", 60), 320, t, 0.3)
    put(fr, TUBE, 220, 720, 0.8, ease((t - 0.4) / 0.5))
    p = ease((t - 0.6) / 0.6)
    if p > 0:
        im = REPORT.copy(); d = ImageDraw.Draw(im)
        d.rectangle((0, 0, 545, 80), fill=(225, 235, 245)); d.text((30, 40), "LAB REPORT", font=font("Bold", 28), fill=(20, 50, 100), anchor="lm")
        d.rectangle((24, 96, 520, 430), fill=(250, 250, 248))
        d.text((30, 110), "SPEP (example format)", font=font("Bold", 24), fill=(20, 50, 100))
        for i, m in enumerate(["Albumin", "Alpha-1", "Alpha-2", "Beta", "Gamma", "M-spike"]):
            yy = 160 + i * 44; d.text((30, yy), m, font=font("Medium", 22), fill=(40, 40, 60)); d.text((260, yy), "g/dL" if m != "M-spike" else "seen / not seen", font=font("Regular", 22), fill=(110, 110, 130))
        put(fr, im, 700, 760, 0.75, p)
    show(fr, gcard("No special preparation usually; follow your lab's instructions", CYAN, 1, 36), 1080, t, D * 0.35)
    show(fr, gcard("Always understand the report with your doctor", TEALG, 2, 38), 1230, t, D * 0.6)

SC = [(film(p_hook), "doc"), (film(p_what), "doc"), (film(p_fractions), "doc"), (film(p_when), "doc"), (film(p_mspike), "doc"),
      (film(p_mgus), "doc"), (film(p_patterns), "doc"), (film(p_next), "doc"), (film(p_prep), "doc"),
      (close_scene("Heard of the M-spike before?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        D = [14, 16, 16, 18, 20, 22, 18, 20, 18, 33]
        ims = []
        for si in range(10):
            fn, bg = SC[si]; d = D[si]; p = 0.95; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((360, 640)))
        s = Image.new("RGB", (360 * 5, 640 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 360, (i // 5) * 640))
        s.save("sheet.png")
    else: run(SC, "/tmp/spep_", "Protein_Electrophoresis_Hindi.mp4")
