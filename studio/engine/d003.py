"""Aaj Ka Health Gyan, Day 3: Thyroid (TSH) test, kab karayein (Hindi, Swara voice, purple & pink theme)."""
import sys
from cbc_cartoon import run
from pp_style import *

N = 3
SRC = "MedlinePlus (US National Library of Medicine): TSH test"
SRC_IN = "Unnikrishnan et al., Indian J Endocrinol Metab 2013 (8 cities incl. Kolkata)"

def seesaw(fr, y, t, tin):
    """TSH vs thyroid hormone: they move in opposite directions."""
    lay, d = overlay(fr); e = ease((t - tin) / 0.8); a = int(255 * e)
    for i, (head, l1, l2, c) in enumerate((("TSH HIGH", "Too little hormone", "Underactive thyroid", ROSE),
                                           ("TSH LOW", "Too much hormone", "Overactive thyroid", SKY))):
        x = X0 + i * (TW // 2 + 10); w = TW // 2 - 10
        d.rounded_rectangle((x, y, x + w, y + 300), 28, fill=(*c, int(50 * e)), outline=(*c, a), width=4)
        arrow = "▲" if i == 0 else "▼"
        d.text((x + w / 2, y + 70), f"{head}", font=font("Bold", 46), fill=(*c, a), anchor="mm")
        d.text((x + w / 2, y + 150), l1, font=font("Bold", 32), fill=(*WHITE, a), anchor="mm")
        d.text((x + w / 2, y + 205), l2, font=font("Medium", 30), fill=(*LILAC, a), anchor="mm")
    fr.alpha_composite(lay)

def s0(fr, t, D):
    show(fr, series_pill(N), 250, t, -1)
    show(fr, headline("Thyroid (TSH) test", 88, WHITE), 340, t, -1)
    show(fr, headline("Kab karayein?", 70, (249, 168, 212)), 460, t, -1)
    show(fr, body("Signs  •  How to read it  •  Tips", 42, LILAC), 580, t, -1)
    seesaw(fr, 800, t, -1)
    show(fr, callout("Watch till the end", PINK, 40), 1500, t, D * 0.5)

def s1(fr, t, D):
    show(fr, kicker("What TSH is", PINK), 260, t, 0.1)
    show(fr, fact_card("The brain's pituitary makes TSH", LILAC, 1, 38), 360, t, 0.3)
    show(fr, fact_card("TSH tells the thyroid how much hormone to make", MINT, 2, 36), 520, t, D * 0.25)
    seesaw(fr, 720, t, D * 0.45)
    show(fr, source_tag(SRC), 1080, t, D * 0.7)
    fire("pop", D * 0.25); fire("ding", D * 0.45)

def s2(fr, t, D):
    show(fr, kicker("Signs of an underactive thyroid", PINK), 260, t, 0.1)
    for i, (txt, c) in enumerate((("Tiredness, weight gain", ROSE), ("Feeling cold, dry skin, thin hair", SUN),
                                  ("Irregular periods, trouble conceiving", LILAC), ("Constipation, low mood", MINT))):
        fire("pop", D * (0.1 + 0.13 * i)); show(fr, fact_card(txt, c, i + 1, 36), 360 + i * 150, t, D * (0.1 + 0.13 * i))
    show(fr, callout("Often develops slowly", PINK, 38), 980, t, D * 0.65)
    show(fr, source_tag(SRC), 1130, t, D * 0.72)

def s3(fr, t, D):
    show(fr, kicker("Signs of an overactive thyroid", PINK), 260, t, 0.1)
    for i, (txt, c) in enumerate((("Weight loss despite eating normally", SKY), ("Fast or irregular heartbeat", ROSE),
                                  ("Nervousness, poor sleep, shaky hands", SUN), ("Feeling hot; swelling in the neck (goitre)", LILAC))):
        fire("pop", D * (0.1 + 0.13 * i)); show(fr, fact_card(txt, c, i + 1, 35), 360 + i * 150, t, D * (0.1 + 0.13 * i))
    show(fr, source_tag(SRC), 1000, t, D * 0.7)

def s4(fr, t, D):
    show(fr, kicker("In India", PINK), 260, t, 0.1)
    big_number(fr, "1 in 10", "adults had an underactive thyroid", 470, t, 0.3)
    show(fr, fact_card("8-city study, including Kolkata: 10.95%", LILAC, None, 36), 700, t, D * 0.3)
    show(fr, fact_card("1 in 3 of them did not know (3.47% of all)", ROSE, None, 36), 850, t, D * 0.45)
    show(fr, fact_card("More common in women", MINT, None, 38), 1000, t, D * 0.6)
    show(fr, source_tag(SRC_IN), 1150, t, D * 0.7)

def s5(fr, t, D):
    show(fr, kicker("Test tips", PINK), 260, t, 0.1)
    show(fr, fact_card("No fasting needed, unless other tests are done too", MINT, 1, 35), 360, t, 0.3)
    show(fr, fact_card("Tell your doctor about your medicines; don't stop any yourself", SUN, 2, 34), 520, t, D * 0.22)
    show(fr, fact_card("Abnormal TSH: doctor may add T3, T4 and antibody tests", LILAC, 3, 34), 700, t, D * 0.36)
    show(fr, fact_card("Pregnant with a thyroid history? Talk to your doctor", ROSE, 4, 34), 880, t, D * 0.5)
    show(fr, source_tag(SRC), 1050, t, D * 0.65)
    for k in (0.22, 0.36, 0.5): fire("pop", D * k)

SC = [(film(s0), "pp"), (film(s1), "pp"), (film(s2), "pp"), (film(s3), "pp"), (film(s4), "pp"), (film(s5), "pp"),
      (close_pp("Have you ever checked your TSH?", N), "ppl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si, (fn, bg) in enumerate(SC):
            d = 14 if si < len(SC) - 1 else 22; p = .95 if si else 0.01; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((300, 533)))
        s = Image.new("RGB", (300 * 7, 533), "white")
        for i, im in enumerate(ims): s.paste(im, (i * 300, 0))
        s.save("/tmp/sheet_d003.png")
    else: run(SC, "/tmp/d003_", "AajKaHealthGyan_Day03_Thyroid_TSH_Hindi.mp4", max_sec=120)
