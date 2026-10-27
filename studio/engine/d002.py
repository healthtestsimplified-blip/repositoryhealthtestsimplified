"""Aaj Ka Health Gyan, Day 2: HbA1c test (Hindi, Swara voice, purple & pink theme)."""
import sys
from cbc_cartoon import run
from pp_style import *

N = 2
SRC = "NIDDK (US National Institutes of Health): The A1C Test & Diabetes"

def meter(fr, y, t, tin, marker=None):
    """A1C scale with three zones."""
    lay, d = overlay(fr); e = ease((t - tin) / 0.8); a = int(255 * e)
    x0, x1 = X0 + 20, X0 + TW - 20; lo, hi = 4.5, 9.0
    def px(v): return x0 + (v - lo) / (hi - lo) * (x1 - x0)
    for a0, a1, c, lab in ((lo, 5.7, MINT, "Normal"), (5.7, 6.5, SUN, "Prediabetes"), (6.5, hi, ROSE, "Diabetes")):
        d.rounded_rectangle((px(a0), y, px(a1), y + 70), 18, fill=(*c, a))
        d.text(((px(a0) + px(a1)) / 2, y + 120), lab, font=font("Bold", 30), fill=(*c, a), anchor="mm")
    for v in (5.7, 6.5):
        d.text((px(v), y - 30), f"{v}%", font=font("Bold", 32), fill=(*WHITE, a), anchor="mm")
    if marker:
        m = ease((t - tin - 0.8) / 0.8); xv = px(lo + (marker - lo) * m)
        d.polygon([(xv - 18, y - 70), (xv + 18, y - 70), (xv, y - 40)], fill=(*WHITE, int(255 * m)))
    fr.alpha_composite(lay)

def s0(fr, t, D):
    show(fr, series_pill(N), 250, t, -1)
    show(fr, headline("HbA1c test", 100, WHITE), 340, t, -1)
    show(fr, headline("3 mahine ki sugar report", 60, (249, 168, 212)), 470, t, -1)
    show(fr, body("What it shows  •  How to read it", 42, LILAC), 590, t, -1)
    meter(fr, 900, t, -1)
    show(fr, callout("Watch till the end", PINK, 40), 1500, t, D * 0.5)

def s1(fr, t, D):
    show(fr, kicker("What it shows", PINK), 260, t, 0.1)
    show(fr, fact_card("Daily sugar test: only that moment", LILAC, 1, 38), 360, t, 0.3)
    show(fr, fact_card("HbA1c: average of about the last 3 months", MINT, 2, 38), 530, t, D * 0.3)
    show(fr, callout("No fasting needed: any time of day", PINK, 38), 720, t, D * 0.6)
    show(fr, source_tag(SRC), 880, t, D * 0.7)
    fire("pop", D * 0.3); fire("ding", D * 0.6)

def s2(fr, t, D):
    show(fr, kicker("How to read the report", PINK), 260, t, 0.1)
    meter(fr, 470, t, 0.3)
    show(fr, fact_card("Below 5.7%: normal", MINT, None, 36), 700, t, D * 0.2)
    show(fr, fact_card("5.7% to 6.4%: prediabetes", SUN, None, 36), 840, t, D * 0.35)
    show(fr, fact_card("6.5% or more: diabetes", ROSE, None, 36), 980, t, D * 0.5)
    show(fr, body("No symptoms? A repeat test on another day confirms it", 32, SOFT), 1130, t, D * 0.65)
    show(fr, source_tag(SRC), 1210, t, D * 0.7)

def s3(fr, t, D):
    show(fr, kicker("If you have diabetes", PINK), 260, t, 0.1)
    big_number(fr, "< 7%", "a common target", 470, t, 0.3)
    show(fr, fact_card("Your own target is set by your doctor", LILAC, None, 36), 700, t, D * 0.35)
    show(fr, fact_card("Test at least twice a year", MINT, None, 36), 850, t, D * 0.5)
    show(fr, source_tag(SRC), 1010, t, D * 0.65)

def s4(fr, t, D):
    show(fr, kicker("When the result can mislead", PINK), 260, t, 0.1)
    for i, (txt, c) in enumerate((("Anaemia, recent blood loss or transfusion", ROSE), ("Kidney or liver disease", SUN),
                                  ("Thalassemia, sickle cell and other haemoglobin variants", LILAC))):
        fire("pop", D * (0.1 + 0.15 * i)); show(fr, fact_card(txt, c, i + 1, 34), 360 + i * 160, t, D * (0.1 + 0.15 * i))
    show(fr, callout("Your doctor may choose another test", MINT, 36), 880, t, D * 0.65)
    show(fr, source_tag(SRC), 1030, t, D * 0.7)

SC = [(film(s0), "pp"), (film(s1), "pp"), (film(s2), "pp"), (film(s3), "pp"), (film(s4), "pp"),
      (close_pp("When did you last test HbA1c?", N), "ppl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si, (fn, bg) in enumerate(SC):
            d = 14 if si < len(SC) - 1 else 22; p = .95 if si else 0.01; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((300, 533)))
        s = Image.new("RGB", (300 * 6, 533), "white")
        for i, im in enumerate(ims): s.paste(im, (i * 300, 0))
        s.save("/tmp/sheet_d002.png")
    else: run(SC, "/tmp/d002_", "AajKaHealthGyan_Day02_HbA1c_Hindi.mp4", max_sec=120)
