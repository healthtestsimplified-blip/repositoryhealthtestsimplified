"""Aaj Ka Health Gyan, Day 1: Vitamin D ki kami (Hindi, Swara voice, purple & pink theme)."""
import sys, math
from cbc_cartoon import run
from pp_style import *

N = 1

def sun(fr, cx, cy, r, t, tin):
    lay, d = overlay(fr); e = ease((t - tin) / 0.6); a = int(255 * e); rot = t * 0.4
    for k in range(12):
        ang = rot + k * math.pi / 6
        x1, y1 = cx + math.cos(ang) * (r + 20), cy + math.sin(ang) * (r + 20)
        x2, y2 = cx + math.cos(ang) * (r + 70), cy + math.sin(ang) * (r + 70)
        d.line((x1, y1, x2, y2), fill=(*SUN, a), width=12)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(*SUN, a))
    d.text((cx, cy), "D", font=font("Bold", int(r * 1.1)), fill=(*DEEP, a), anchor="mm")
    fr.alpha_composite(lay)

def s0(fr, t, D):
    show(fr, series_pill(N), 250, t, -1)
    show(fr, headline("Vitamin D", 96, WHITE), 340, t, -1)
    show(fr, headline("ki kami", 96, (249, 168, 212)), 450, t, -1)
    show(fr, body("Symptoms  •  Food  •  Test", 44, LILAC), 590, t, -1)
    sun(fr, 540, 1000, 170, t, -1)
    show(fr, callout("Watch till the end", PINK, 40), 1500, t, D * 0.5)

def s1(fr, t, D):
    show(fr, kicker("Why it matters", PINK), 260, t, 0.1)
    for i, (txt, c) in enumerate((("Helps the body absorb calcium for bones", MINT), ("Low vitamin D: bones become weak and soft", ROSE),
                                  ("Children: rickets  •  Adults: osteomalacia", LILAC))):
        fire("pop", D * (0.1 + 0.2 * i)); show(fr, fact_card(txt, c, i + 1, 38), 360 + i * 175, t, D * (0.1 + 0.2 * i))
    show(fr, source_tag("MedlinePlus (US National Library of Medicine): Vitamin D"), 930, t, D * 0.7)

def s2(fr, t, D):
    show(fr, kicker("Where to get it", PINK), 260, t, 0.1)
    sun(fr, 540, 520, 110, t, 0.2)
    show(fr, body("Skin makes it in sunlight; less with clouds, shade and darker skin", 34, SOFT), 730, t, D * 0.2)
    icon_row(fr, 1010, t, D * 0.45, [("Fish", SKY), ("Egg yolk", SUN), ("Mushroom", LILAC), ("Fortified milk", MINT)])
    show(fr, source_tag("MedlinePlus: Vitamin D"), 1160, t, D * 0.7)

def s3(fr, t, D):
    show(fr, kicker("How much per day?", PINK), 260, t, 0.1)
    big_number(fr, "600 IU", "per day, age 1 to 70", 470, t, 0.3)
    show(fr, fact_card("Over 70 years: 800 IU per day", LILAC, None, 38), 700, t, D * 0.35)
    show(fr, callout("Too much supplement can raise blood calcium and cause kidney stones", ROSE, 34), 870, t, D * 0.6)
    show(fr, source_tag("MedlinePlus: Vitamin D"), 1060, t, D * 0.7)

def s4(fr, t, D):
    show(fr, kicker("The test", PINK), 260, t, 0.1)
    put(fr, tube_sprite((251, 191, 36), "VIT D"), 300, 620, 0.95, ease((t - 0.3) / 0.5))
    lay, d = overlay(fr); e = ease((t - 0.5) / 0.5)
    d.text((660, 560), "25-hydroxy", font=font("Bold", 42), fill=(*WHITE, int(255 * e)), anchor="lm")
    d.text((660, 620), "vitamin D", font=font("Bold", 42), fill=(*WHITE, int(255 * e)), anchor="lm"); fr.alpha_composite(lay)
    show(fr, fact_card("2024 guideline: no routine test for healthy adults", LILAC, 1, 34), 900, t, D * 0.3)
    show(fr, fact_card("Bone pain, weakness, osteoporosis: your doctor decides", MINT, 2, 34), 1060, t, D * 0.5)
    show(fr, source_tag("Endocrine Society clinical practice guideline, 2024"), 1240, t, D * 0.65)

SC = [(film(s0), "pp"), (film(s1), "pp"), (film(s2), "pp"), (film(s3), "pp"), (film(s4), "pp"),
      (close_pp("Ever tested your vitamin D?", N), "ppl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si, (fn, bg) in enumerate(SC):
            d = 14 if si < len(SC) - 1 else 22; p = .95 if si else 0.01; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((300, 533)))
        s = Image.new("RGB", (300 * 6, 533), "white")
        for i, im in enumerate(ims): s.paste(im, (i * 300, 0))
        s.save("/tmp/sheet_d001.png")
    else: run(SC, "/tmp/d001_", "AajKaHealthGyan_Day01_VitaminD_Hindi.mp4", max_sec=120)
