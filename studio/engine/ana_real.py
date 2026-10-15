"""ANA by IFA (HEp-2), realistic documentary style."""
import math, sys, random
from cbc_cartoon import run
from real_style import *
from hts_close import close_scene

TOPIC = "ANA  •  IFA (HEp-2)"
NCH = 7
GREEN = (90, 255, 120)

def hep2(kind="homogeneous", n=900, seed=4, cells=26, bright=1.0):
    """HEp-2 cells under fluorescence: nuclei glow green in the given pattern (illustration)."""
    r = random.Random(seed); rng = np.random.default_rng(seed)
    base = Image.new("L", (n, n), 0); d = ImageDraw.Draw(base)
    cyto = Image.new("L", (n, n), 0); dc = ImageDraw.Draw(cyto)
    pts = []
    tries = 0
    while len(pts) < cells and tries < 4000:
        tries += 1; x, y = r.uniform(70, n - 70), r.uniform(70, n - 70)
        if all((x - a) ** 2 + (y - b) ** 2 > 150 ** 2 for a, b, _ in pts): pts.append((x, y, r.uniform(48, 64)))
    for x, y, rad in pts:
        dc.ellipse((x - rad * 1.6, y - rad * 1.4, x + rad * 1.6, y + rad * 1.4), fill=14)
        if kind == "negative": continue
        mitotic = r.random() < 0.08
        if kind == "homogeneous":
            d.ellipse((x - rad, y - rad * .85, x + rad, y + rad * .85), fill=int(200 * bright))
        elif kind in ("speckled", "dfs"):
            d.ellipse((x - rad, y - rad * .85, x + rad, y + rad * .85), fill=int((70 if kind == "speckled" else 110) * bright))
            for _ in range(160 if kind == "dfs" else 90):
                a = r.uniform(0, 2 * math.pi); q = math.sqrt(r.random()) * rad * .9
                s = r.uniform(2, 3) if kind == "dfs" else r.uniform(3, 6)
                xx, yy = x + math.cos(a) * q, y + math.sin(a) * q * .85
                d.ellipse((xx - s, yy - s, xx + s, yy + s), fill=int(r.uniform(180, 255) * bright))
        elif kind == "centromere":
            d.ellipse((x - rad, y - rad * .85, x + rad, y + rad * .85), fill=12)
            for _ in range(45):
                a = r.uniform(0, 2 * math.pi); q = math.sqrt(r.random()) * rad * .85
                xx, yy = x + math.cos(a) * q, y + math.sin(a) * q * .85
                d.ellipse((xx - 3.5, yy - 3.5, xx + 3.5, yy + 3.5), fill=int(255 * bright))
        elif kind == "nucleolar":
            d.ellipse((x - rad, y - rad * .85, x + rad, y + rad * .85), fill=int(35 * bright))
            for _ in range(r.randint(2, 4)):
                a = r.uniform(0, 2 * math.pi); q = r.uniform(.1, .5) * rad; s = r.uniform(9, 15)
                xx, yy = x + math.cos(a) * q, y + math.sin(a) * q
                d.ellipse((xx - s, yy - s * .8, xx + s, yy + s * .8), fill=int(240 * bright))
        if mitotic and kind in ("homogeneous", "dfs"):
            d.ellipse((x - rad, y - rad * .85, x + rad, y + rad * .85), fill=0)
            d.rounded_rectangle((x - rad * .7, y - 9, x + rad * .7, y + 9), 8, fill=int(255 * bright))
    g = np.asarray(base.filter(ImageFilter.GaussianBlur(1.8))).astype(np.float32) / 255
    c = np.asarray(cyto.filter(ImageFilter.GaussianBlur(10))).astype(np.float32) / 255
    noise = rng.normal(0, 0.025, (n, n)).astype(np.float32)
    v = np.clip(g + c + noise, 0, 1)
    glow = np.asarray(Image.fromarray((g * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(8))).astype(np.float32) / 255
    v = np.clip(v + glow * 0.35, 0, 1)
    rgb = np.stack([v * 0.35 * 255, v * 255, v * 0.45 * 255, np.full_like(v, 255)], -1)
    return Image.fromarray(rgb.clip(0, 255).astype(np.uint8))

TEX = {k: hep2(k, seed=i + 3) for i, k in enumerate(("homogeneous", "speckled", "centromere", "nucleolar", "dfs", "negative"))}
DIL = [hep2("homogeneous", 600, 11, 12, b) for b in (1.0, 0.75, 0.45, 0.18)]

def dots(fr, n): fr.alpha_composite(chapter(n, NCH), (0, 110))

def scope(fr, tex, cx, cy, size, t, D, a=1.0, label=None, col=GREEN, zoom=(1.0, 1.25)):
    ep = eyepiece(tex, size, t, zoom[0], zoom[1], D)
    put(fr, ep, cx, cy, 1.0, a)
    if label and a > 0.5:
        lay, d = overlay(fr); d.text((cx, cy + size / 2 + 50), label, font=font("Bold", 32), fill=col, anchor="mm"); fr.alpha_composite(lay)

def cards(fr, t, D, items, y0=340, size=35, gap=145, t0=0.1, step=0.11):
    for i, (txt, c) in enumerate(items):
        fire("pop", D * (t0 + step * i)); show(fr, gcard(txt, c, i + 1, size), y0 + i * gap, t, D * (t0 + step * i))

def antibodies(fr, cx, cy, t, D, tin, n=7, col=CYAN, glowc=None):
    lay, d = overlay(fr); e = ease((t - tin) / 0.8)
    for i in range(n):
        a = i / n * 2 * math.pi + 0.3; rr = 330 - 150 * e
        x, y = cx + math.cos(a) * rr, cy + math.sin(a) * rr
        antibody(d, x, y, 40, a, glowc or col, int(255 * min(1, (t - tin) * 2)) if t > tin else 0)
    fr.alpha_composite(lay)

# ---------------- scenes ----------------
def s_hook(fr, t, D):
    fullbleed(fr, TEX["homogeneous"], t, D, 1.0, 1.2)
    show(fr, kicker("Autoimmune test explained", CYAN), 250, t, 0.1)
    type_on(fr, "ANA test by IFA", 310, t, 0.3, 76)
    if t > D * 0.25: type_on(fr, "Antinuclear antibody  •  immunofluorescence", 420, t, D * 0.25, 40, AMBER)
    for i, (txt, c) in enumerate((("Joint pain with swelling", CORAL), ("Facial rash in sunlight", AMBER))):
        fire("pop", D * (0.4 + 0.12 * i)); show(fr, gcard(txt, c, None, 36), 1150 + i * 140, t, D * (0.4 + 0.12 * i))
    show(fr, callout("Watch till the end", CORAL, 38), 1620, t, D * 0.8)

def s_what(fr, t, D):
    dots(fr, 1); show(fr, kicker("What is ANA?"), 260, t, 0.1)
    show(fr, headline("Antibodies against your own cell nucleus", 56), 320, t, 0.3)
    lay, d = overlay(fr); cx, cy = 540, 820; e = ease((t - 0.4) / 0.6)
    d.ellipse((cx - 250, cy - 200, cx + 250, cy + 200), fill=(120, 150, 190, int(70 * e)), outline=(180, 200, 230, int(200 * e)), width=4)
    d.ellipse((cx - 110, cy - 95, cx + 110, cy + 95), fill=(90, 110, 200, int(200 * e)))
    d.text((cx, cy), "Nucleus", font=font("Bold", 34), fill=(*WHITE, int(255 * e)), anchor="mm")
    d.text((cx, cy + 240), "Your own cell", font=font("Medium", 28), fill=(*SOFT, int(255 * e)), anchor="mm")
    fr.alpha_composite(lay)
    antibodies(fr, cx, cy, t, D, D * 0.25, col=CORAL)
    show(fr, gcard("Immune system mistakenly targets the nucleus", CORAL, None, 34), 1110, t, D * 0.35)
    show(fr, gcard("Seen in lupus (SLE), Sjögren's, scleroderma and others", CYAN, None, 34), 1260, t, D * 0.55)

def s_ifa(fr, t, D):
    dots(fr, 2); show(fr, kicker("How IFA works"), 260, t, 0.1)
    steps = [("1", "Patient serum on a slide of HEp-2 cells"), ("2", "ANA binds the nucleus"), ("3", "Add fluorescent-tagged antibody"), ("4", "Nucleus glows green under the microscope")]
    lay, d = overlay(fr)
    for i, (k, txt) in enumerate(steps):
        tin = D * (0.08 + 0.12 * i); e = ease((t - tin) / 0.5)
        if t < tin: continue
        y = 330 + i * 100
        d.ellipse((X0, y, X0 + 64, y + 64), fill=(*CYAN, int(255 * e))); d.text((X0 + 32, y + 32), k, font=font("Bold", 34), fill=(*INK, int(255 * e)), anchor="mm")
        d.text((X0 + 90, y + 32), txt, font=font("Medium", 34), fill=(*SOFT, int(255 * e)), anchor="lm")
    fr.alpha_composite(lay)
    scope(fr, TEX["homogeneous"], 540, 1080, 520, t, D, ease((t - D * 0.5) / 0.6), "HEp-2 cells, fluorescence (illustration)")
    show(fr, callout("ACR: HEp-2 IFA is the gold standard", AMBER, 36), 1480, t, D * 0.7); fire("ding", D * 0.7)

def s_titer(fr, t, D):
    dots(fr, 3); show(fr, kicker("Titer"), 260, t, 0.1)
    show(fr, headline("Highest dilution that still glows", 58), 320, t, 0.3)
    labs = ["1:80", "1:160", "1:320", "1:640"]
    for i in range(4):
        tin = D * (0.15 + 0.12 * i)
        if t < tin: continue
        cx = 150 + (i % 2) * 0 + i * 260
        ep = eyepiece(DIL[i], 220, t, 1.0, 1.05, D); put(fr, ep, cx, 640, 1.0, ease((t - tin) / 0.5))
        lay, d = overlay(fr); d.text((cx, 790), labs[i], font=font("Bold", 34), fill=GREEN if i < 3 else MUTED, anchor="mm"); fr.alpha_composite(lay)
    show(fr, callout("Here: titer 1:320 (last dilution with clear glow)", GREEN, 32), 870, t, D * 0.65)
    show(fr, gcard("Higher titer = higher chance of autoimmune disease", AMBER, None, 34), 1020, t, D * 0.72)
    show(fr, gcard("Cut-off differs by laboratory (often 1:80 or 1:160)", CYAN, None, 34), 1170, t, D * 0.8)

def s_patterns(fr, t, D):
    dots(fr, 4); show(fr, kicker("Patterns on the report"), 260, t, 0.1)
    items = [("homogeneous", "Homogeneous", "Often SLE"), ("speckled", "Speckled", "Many autoimmune diseases"), ("centromere", "Centromere", "Limited scleroderma"),
             ("nucleolar", "Nucleolar", "Systemic sclerosis"), ("dfs", "Dense fine speckled", "Often no autoimmune disease")]
    for i, (k, lab, dis) in enumerate(items):
        tin = D * (0.06 + 0.16 * i)
        if t < tin: continue
        col, row = i % 2, i // 2
        cx = 300 + col * 480 if i < 4 else 540; cy = 520 + row * 440
        ep = eyepiece(TEX[k], 270, t - tin, 1.4, 1.6, D); put(fr, ep, cx, cy, 1.0, ease((t - tin) / 0.5)); fire("pop", tin)
        lay, d = overlay(fr); e = ease((t - tin) / 0.5)
        d.text((cx, cy + 172), lab, font=font("Bold", 32), fill=(*GREEN, int(255 * e)), anchor="mm")
        d.text((cx, cy + 210), dis, font=font("Medium", 28), fill=(*SOFT, int(255 * e)), anchor="mm")
        fr.alpha_composite(lay)
    show(fr, source_tag("Labcorp ANA IFA (HEp-2) patterns; ACR/rheumatology reviews"), 1720, t, D * 0.85)

def s_when(fr, t, D):
    dots(fr, 5); show(fr, kicker("When do doctors order it?"), 260, t, 0.1)
    cards(fr, t, D, [("Joint pain with swelling", CORAL), ("Facial rash after sun exposure", AMBER), ("Mouth ulcers", LAV),
                     ("Fingers turn white or blue in cold", CYAN), ("Dry eyes and dry mouth", TEALG)], 330, 34, 140, 0.06, 0.11)
    show(fr, callout("Only tiredness or body ache? Usually not needed", CORAL, 34), 1180, t, D * 0.72)

def s_pos(fr, t, D):
    dots(fr, 6); show(fr, kicker("Positive ANA is not always disease"), 260, t, 0.1)
    counter(fr, 14, "%", 320, t, 0.3, size=150, prefix="~")
    show(fr, body("of people aged 12+ were ANA positive in a large US survey (NHANES 1999-2004)", 34, SOFT), 510, t, 0.7)
    show(fr, gcard("Infections and some medicines can also cause it", AMBER, 1, 34), 680, t, D * 0.42)
    show(fr, gcard("If positive, doctor may order anti-dsDNA or ENA profile", TEALG, 2, 34), 825, t, D * 0.6)
    fire("pop", D * 0.42); fire("pop", D * 0.6)
    scope(fr, TEX["negative"], 540, 1400, 320, t, D, ease((t - D * 0.7) / 0.5), "Negative: no nuclear glow", MUTED)

def s_prep(fr, t, D):
    dots(fr, 7); show(fr, kicker("Good to know"), 260, t, 0.1)
    cards(fr, t, D, [("Usually no fasting needed", TEALG), ("Tell the doctor about all medicines", AMBER), ("One report alone is not a diagnosis", CORAL),
                     ("Don't repeat without medical advice", LAV)], 330, 34, 145, 0.08, 0.12)
    put(fr, tube_sprite((200, 60, 60), "SERUM"), 540, 1340, 1.0, ease((t - D * 0.65) / 0.5))

SC = [(film(s_hook), "doc"), (film(s_what), "doc"), (film(s_ifa), "doc"), (film(s_titer), "doc"), (film(s_patterns), "doc"),
      (film(s_when), "doc"), (film(s_pos), "doc"), (film(s_prep), "doc"), (close_scene("Have you had an ANA test?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si, (fn, bg) in enumerate(SC):
            d = 16 if si < len(SC) - 1 else 33; NOW.update(t=d * .95, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * .95, d); ims.append(fr.convert("RGB").resize((360, 640)))
        s = Image.new("RGB", (360 * 5, 640 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 360, (i // 5) * 640))
        s.save("sheet_ana.png")
    else: run(SC, "/tmp/ana_", "ANA_IFA_Test_Hindi.mp4")
