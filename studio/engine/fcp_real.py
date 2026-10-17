"""Fecal calprotectin, realistic documentary style."""
import math, sys, random
from cbc_cartoon import run
from real_style import *
from hts_close import close_scene

TOPIC = "FECAL CALPROTECTIN"
NCH = 7

def neutrophils(tex, count=260, seed=7, rim=True):
    """Add neutrophil clusters (multi-lobed purple nuclei, pale cytoplasm) onto an H&E texture."""
    im = tex.copy(); d = ImageDraw.Draw(im, "RGBA"); r = random.Random(seed); n = im.width
    for _ in range(count):
        x, y = r.uniform(0, n), r.uniform(0, n); s = r.uniform(7, 10)
        d.ellipse((x - s * 1.6, y - s * 1.6, x + s * 1.6, y + s * 1.6), fill=(235, 190, 215, 170))
        for k in range(r.randint(3, 4)):
            a = k * 2.1 + r.uniform(-.3, .3)
            xx, yy = x + math.cos(a) * s * .7, y + math.sin(a) * s * .7
            d.ellipse((xx - s * .45, yy - s * .45, xx + s * .45, yy + s * .45), fill=(70, 30, 120, 240))
    return im.filter(ImageFilter.GaussianBlur(0.7))

NORMAL = he_tissue(1100, seed=3, glands=14)
INFLAMED = neutrophils(he_tissue(1100, seed=5, glands=10), 420, 8)

def neutro_sprite(s=150):
    im = Image.new("RGBA", (s * 2, s * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((10, 10, s * 2 - 10, s * 2 - 10), fill=(240, 200, 222, 235), outline=(255, 230, 240, 255), width=4)
    r = random.Random(2)
    for _ in range(120):
        x, y = r.uniform(30, s * 2 - 30), r.uniform(30, s * 2 - 30)
        if (x - s) ** 2 + (y - s) ** 2 < (s - 30) ** 2: d.ellipse((x - 3, y - 3, x + 3, y + 3), fill=(215, 160, 200, 200))
    for k in range(4):
        a = k * 1.6 - 2.3; x, y = s + math.cos(a) * s * .38, s + math.sin(a) * s * .38
        d.ellipse((x - s * .26, y - s * .22, x + s * .26, y + s * .22), fill=(80, 35, 130, 255))
    return im.filter(ImageFilter.GaussianBlur(1.2))
NEUT = neutro_sprite()

def pot_sprite():
    w, h = 300, 380; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((40, 20, 260, 90), 14, fill=(30, 90, 190, 255)); d.rectangle((40, 70, 260, 90), fill=(25, 75, 165, 255))
    for i in range(10): d.line((52 + i * 22, 26, 52 + i * 22, 84), fill=(20, 60, 140, 255), width=3)
    body = cyl_shade(200, 270, (235, 238, 242)); im.alpha_composite(body, (50, 92))
    d.rectangle((62, 160, 238, 280), fill=(255, 255, 255, 255)); d.rectangle((62, 160, 238, 190), fill=(200, 60, 60, 255))
    d.text((150, 175), "STOOL", font=font("Bold", 24), fill=WHITE, anchor="mm")
    d.text((150, 225), "Calprotectin", font=font("Bold", 22), fill=(40, 40, 60), anchor="mm")
    d.text((150, 255), "Name / Date", font=font("Regular", 20), fill=(90, 90, 100), anchor="mm")
    return with_glow(im, (200, 230, 255), 10, 40)
POT = pot_sprite()

def dots(fr, n): fr.alpha_composite(chapter(n, NCH), (0, 110))

def cards(fr, t, D, items, y0=340, size=35, gap=145, t0=0.1, step=0.11):
    for i, (txt, c) in enumerate(items):
        fire("pop", D * (t0 + step * i)); show(fr, gcard(txt, c, i + 1, size), y0 + i * gap, t, D * (t0 + step * i))

def scope(fr, tex, cx, cy, size, t, D, a=1.0, label=None, col=SOFT):
    put(fr, eyepiece(tex, size, t, 1.0, 1.25, D), cx, cy, 1.0, a)
    if label and a > 0.5:
        lay, d = overlay(fr); d.text((cx, cy + size / 2 + 50), label, font=font("Bold", 32), fill=col, anchor="mm"); fr.alpha_composite(lay)

def gauge(fr, y, t, tin, val=None):
    lay, d = overlay(fr); e = ease((t - tin) / 0.8)
    x0, x1 = X0, X0 + TW; segs = [(0, .3, TEALG, "Normal", "< 50"), (.3, .55, AMBER, "Borderline", "repeat"), (.55, 1, CORAL, "High", "inflammation")]
    for a, b, c, lab, sub in segs:
        xa, xb = x0 + a * TW, x0 + b * TW * 1.0
        if (xa - x0) / TW > e: continue
        xb = min(xb, x0 + e * TW)
        if xb - xa < 12: continue
        d.rounded_rectangle((xa + 4, y, xb - 4, y + 70), 20, fill=(*c, 235))
        d.text(((xa + x0 + b * TW) / 2, y + 110), lab, font=font("Bold", 32), fill=c, anchor="mm")
        d.text(((xa + x0 + b * TW) / 2, y + 150), sub, font=font("Medium", 28), fill=SOFT, anchor="mm")
    d.text((x0, y - 40), "µg/g of stool", font=font("Medium", 28), fill=MUTED)
    fr.alpha_composite(lay)

# ---------------- scenes ----------------
def s_hook(fr, t, D):
    fullbleed(fr, INFLAMED, t, D, 1.0, 1.2)
    show(fr, kicker("Stool test explained", CYAN), 250, t, 0.1)
    type_on(fr, "Fecal Calprotectin", 310, t, 0.3, 74)
    if t > D * 0.25: type_on(fr, "IBS or IBD? A simple stool test helps", 420, t, D * 0.25, 42, AMBER)
    for i, (txt, c) in enumerate((("Frequent loose motions", CORAL), ("Belly pain", AMBER), ("Mucus in stool", LAV))):
        fire("pop", D * (0.4 + 0.1 * i)); show(fr, gcard(txt, c, None, 36), 1100 + i * 140, t, D * (0.4 + 0.1 * i))
    show(fr, callout("Watch till the end", CORAL, 38), 1600, t, D * 0.8)

def s_what(fr, t, D):
    dots(fr, 1); show(fr, kicker("What is calprotectin?"), 260, t, 0.1)
    show(fr, headline("A protein from neutrophils (white blood cells)", 54), 320, t, 0.3)
    put(fr, NEUT, 540, 640, 1.0, ease((t - 0.5) / 0.6))
    lay, d = overlay(fr); e = ease((t - 0.8) / 0.5); d.text((540, 810), "Neutrophil", font=font("Bold", 32), fill=(*LAV, int(255 * e)), anchor="mm"); fr.alpha_composite(lay)
    show(fr, gcard("Gut inflamed: neutrophils gather in the gut wall", CORAL, 1, 34), 900, t, D * 0.35)
    show(fr, gcard("Calprotectin comes out in the stool", AMBER, 2, 34), 1045, t, D * 0.5)
    show(fr, callout("More inflammation = more calprotectin", TEALG, 36), 1210, t, D * 0.65)
    fire("pop", D * 0.35); fire("pop", D * 0.5); fire("ding", D * 0.65)

def s_ibs(fr, t, D):
    dots(fr, 2); show(fr, kicker("IBS vs IBD"), 260, t, 0.1)
    scope(fr, NORMAL, 285, 600, 400, t, D, ease((t - 0.3) / 0.6), "IBS: no inflammation", TEALG)
    scope(fr, INFLAMED, 795, 600, 400, t, D, ease((t - D * 0.3) / 0.6), "IBD: inflamed gut", CORAL)
    show(fr, gcard("IBS: sensitive gut, calprotectin usually normal", TEALG, 1, 34), 930, t, D * 0.2)
    show(fr, gcard("IBD (Crohn's, ulcerative colitis): calprotectin raised", CORAL, 2, 34), 1080, t, D * 0.4)
    show(fr, callout("Helps decide who needs a colonoscopy", AMBER, 36), 1250, t, D * 0.6)
    show(fr, body("Gut tissue images are illustrations", 28, MUTED), 1400, t, D * 0.6)

def s_when(fr, t, D):
    dots(fr, 3); show(fr, kicker("When do doctors order it?"), 260, t, 0.1)
    cards(fr, t, D, [("Long-lasting diarrhoea, belly pain or mucus", CYAN), ("To tell IBS apart from IBD", AMBER), ("Known IBD: check disease activity", LAV),
                     ("Known IBD: check if treatment is working", TEALG)], 340, 34, 150, 0.08, 0.15)
    put(fr, POT, 540, 1220, 0.9, ease((t - D * 0.5) / 0.6))

def s_result(fr, t, D):
    dots(fr, 4); show(fr, kicker("Reading the report"), 260, t, 0.1)
    gauge(fr, 420, t, 0.3)
    show(fr, gcard("Below 50 µg/g: usually normal", TEALG, 1, 34), 680, t, D * 0.3)
    show(fr, gcard("Borderline: repeat after a few weeks may be advised", AMBER, 2, 34), 830, t, D * 0.45)
    show(fr, gcard("High: points to gut inflammation", CORAL, 3, 34), 980, t, D * 0.6)
    show(fr, source_tag("Ranges differ by laboratory (e.g. Labcorp: <50 normal, 50-120 borderline, >120 abnormal)"), 1140, t, D * 0.7)

def s_other(fr, t, D):
    dots(fr, 5); show(fr, kicker("Not only IBD"), 260, t, 0.1)
    show(fr, headline("Other things that can raise it", 58), 320, t, 0.3)
    cards(fr, t, D, [("Stomach / gut infection", CORAL), ("Painkillers (NSAIDs)", AMBER), ("Acidity medicines (PPIs)", AMBER),
                     ("Coeliac disease, diverticular disease", LAV), ("Colon polyps or cancer", CORAL)], 440, 34, 140, 0.15, 0.1)
    show(fr, callout("Children under 2: normally a little higher", CYAN, 34), 1180, t, D * 0.72)

def s_sample(fr, t, D):
    dots(fr, 6); show(fr, kicker("How to give the sample"), 260, t, 0.1)
    put(fr, POT, 540, 560, 1.0, ease((t - 0.3) / 0.6))
    cards(fr, t, D, [("Small amount of stool in a clean container, as the lab says", CYAN), ("No urine or water mixed in", AMBER),
                     ("Keep the outside of the container clean", LAV), ("Deliver within the time the lab gives", TEALG)], 820, 33, 145, 0.2, 0.13)

def s_alert(fr, t, D):
    dots(fr, 7); show(fr, kicker("Important", CORAL), 260, t, 0.1)
    show(fr, headline("Don't wait for this test if you have:", 56), 320, t, 0.3)
    cards(fr, t, D, [("Blood in stool", CORAL), ("Weight loss", CORAL), ("Anaemia (low blood)", CORAL), ("New change in bowel habit at an older age", CORAL)], 470, 34, 140, 0.12, 0.1)
    show(fr, callout("See a doctor promptly", AMBER, 38), 1060, t, D * 0.55); fire("ding", D * 0.55)
    show(fr, gcard("Taking painkillers or acidity medicines? Tell your doctor; don't stop them on your own", TEALG, None, 33), 1220, t, D * 0.7)

SC = [(film(s_hook), "doc"), (film(s_what), "doc"), (film(s_ibs), "doc"), (film(s_when), "doc"), (film(s_result), "doc"),
      (film(s_other), "doc"), (film(s_sample), "doc"), (film(s_alert), "doc"), (close_scene("Had a calprotectin test?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si, (fn, bg) in enumerate(SC):
            d = 16 if si < len(SC) - 1 else 33; NOW.update(t=d * .95, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * .95, d); ims.append(fr.convert("RGB").resize((360, 640)))
        s = Image.new("RGB", (360 * 5, 640 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 360, (i // 5) * 640))
        s.save("sheet_fcp.png")
    else: run(SC, "/tmp/fcp_", "Fecal_Calprotectin_Hindi.mp4")
