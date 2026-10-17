"""ANCA (c-ANCA / p-ANCA, PR3 / MPO), realistic documentary style."""
import math, sys, random
from cbc_cartoon import run
from real_style import *
from hts_close import close_scene

TOPIC = "ANCA TEST  •  c-ANCA / p-ANCA"
NCH = 7
GREEN = (90, 255, 120)

def neut_ifa(kind="c", n=900, seed=4, cells=30):
    """Ethanol-fixed neutrophils under fluorescence (illustration): c = granular cytoplasmic, p = perinuclear, neg = none."""
    r = random.Random(seed); rng = np.random.default_rng(seed)
    g = Image.new("L", (n, n), 0); d = ImageDraw.Draw(g)
    pts = []; tries = 0
    while len(pts) < cells and tries < 4000:
        tries += 1; x, y = r.uniform(60, n - 60), r.uniform(60, n - 60)
        if all((x - a) ** 2 + (y - b) ** 2 > 130 ** 2 for a, b in pts): pts.append((x, y))
    for x, y in pts:
        R = r.uniform(48, 58)
        lobes = [(x + math.cos(k * 2.1 + r.uniform(-.3, .3)) * R * .35, y + math.sin(k * 2.1 + r.uniform(-.3, .3)) * R * .35, R * .3) for k in range(3)]
        if kind == "c":
            for _ in range(140):
                a = r.uniform(0, 2 * math.pi); q = math.sqrt(r.random()) * R
                xx, yy = x + math.cos(a) * q, y + math.sin(a) * q
                if any((xx - lx) ** 2 + (yy - ly) ** 2 < lr ** 2 for lx, ly, lr in lobes): continue
                s = r.uniform(3, 5); d.ellipse((xx - s, yy - s, xx + s, yy + s), fill=int(r.uniform(150, 255)))
        elif kind == "p":
            for lx, ly, lr in lobes:
                d.ellipse((lx - lr - 6, ly - lr - 6, lx + lr + 6, ly + lr + 6), fill=230)
            for lx, ly, lr in lobes:
                d.ellipse((lx - lr + 4, ly - lr + 4, lx + lr - 4, ly + lr - 4), fill=60)
        else:
            d.ellipse((x - R, y - R, x + R, y + R), fill=10)
    v = np.asarray(g.filter(ImageFilter.GaussianBlur(1.6))).astype(np.float32) / 255
    glow = np.asarray(g.filter(ImageFilter.GaussianBlur(9))).astype(np.float32) / 255
    v = np.clip(v + glow * 0.35 + rng.normal(0, 0.02, (n, n)).astype(np.float32), 0, 1)
    rgb = np.stack([v * 0.35 * 255, v * 255, v * 0.45 * 255, np.full_like(v, 255)], -1)
    return Image.fromarray(rgb.clip(0, 255).astype(np.uint8))

CTEX, PTEX, NTEX = neut_ifa("c", seed=3), neut_ifa("p", seed=5), neut_ifa("neg", seed=7)

def dots(fr, n): fr.alpha_composite(chapter(n, NCH), (0, 110))

def cards(fr, t, D, items, y0=340, size=35, gap=145, t0=0.1, step=0.11):
    for i, (txt, c) in enumerate(items):
        fire("pop", D * (t0 + step * i)); show(fr, gcard(txt, c, i + 1, size), y0 + i * gap, t, D * (t0 + step * i))

def scope(fr, tex, cx, cy, size, t, D, a=1.0, label=None, col=GREEN, z=(1.0, 1.25)):
    put(fr, eyepiece(tex, size, t, z[0], z[1], D), cx, cy, 1.0, a)
    if label and a > 0.5:
        lay, d = overlay(fr); d.text((cx, cy + size / 2 + 50), label, font=font("Bold", 32), fill=col, anchor="mm"); fr.alpha_composite(lay)

def vessel(fr, cx, cy, t, inflamed=0.0):
    """Cross-section of a blood vessel; inflamed wall thickens and reddens."""
    lay, d = overlay(fr); R = 200
    wall = (int(200 + 55 * inflamed), int(120 - 50 * inflamed), int(130 - 60 * inflamed))
    th = 40 + 45 * inflamed
    d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=(*wall, 255))
    d.ellipse((cx - R + th, cy - R + th, cx + R - th, cy + R - th), fill=(150, 20, 35, 255))
    r = random.Random(4)
    for _ in range(int(10 + 50 * inflamed)):
        a = r.uniform(0, 2 * math.pi); q = r.uniform(R - th, R - 6)
        x, y = cx + math.cos(a) * q, cy + math.sin(a) * q
        d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=(90, 40, 140, 230))
    fr.alpha_composite(lay)

# ---------------- scenes ----------------
def s_hook(fr, t, D):
    fullbleed(fr, CTEX, t, D, 1.0, 1.2)
    show(fr, kicker("Blood test explained", CYAN), 250, t, 0.1)
    type_on(fr, "ANCA test", 310, t, 0.3, 80)
    type_on(fr, "c-ANCA  •  p-ANCA", 420, t, 0.9, 52, AMBER)
    for i, (txt, c) in enumerate((("Nosebleeds, sinus problems", CORAL), ("Blood in cough", AMBER), ("Blood or protein in urine", LAV))):
        fire("pop", D * (0.45 + 0.1 * i)); show(fr, gcard(txt, c, None, 36), 1130 + i * 140, t, D * (0.45 + 0.1 * i))
    show(fr, callout("Watch till the end", CORAL, 38), 1600, t, D * 0.8)

def s_what(fr, t, D):
    dots(fr, 1); show(fr, kicker("What is ANCA?"), 260, t, 0.1)
    show(fr, headline("Anti-Neutrophil Cytoplasmic Antibody", 54), 320, t, 0.3)
    vessel(fr, 540, 760, t, ease((t - D * 0.35) / 1.5))
    lay, d = overlay(fr); e = ease((t - 0.6) / 0.5)
    d.text((540, 1010), "Blood vessel (illustration)", font=font("Medium", 30), fill=(*MUTED, int(255 * e)), anchor="mm"); fr.alpha_composite(lay)
    show(fr, gcard("Antibodies made by mistake against white blood cells (neutrophils)", CORAL, 1, 33), 1080, t, D * 0.25)
    show(fr, gcard("Linked to vasculitis: inflammation of blood vessels", AMBER, 2, 34), 1240, t, D * 0.45)
    fire("pop", D * 0.25); fire("pop", D * 0.45)

def s_patterns(fr, t, D):
    dots(fr, 2); show(fr, kicker("Two patterns under the microscope"), 260, t, 0.1)
    scope(fr, CTEX, 285, 600, 400, t, D, ease((t - 0.3) / 0.6), "c-ANCA: cytoplasm glows", GREEN)
    scope(fr, PTEX, 795, 600, 400, t, D, ease((t - D * 0.35) / 0.6), "p-ANCA: ring around nucleus", GREEN)
    show(fr, gcard("c-ANCA: usually PR3 antibody", CYAN, 1, 35), 940, t, D * 0.3)
    show(fr, gcard("p-ANCA: usually MPO antibody", LAV, 2, 35), 1090, t, D * 0.55)
    show(fr, body("Fluorescence images are illustrations", 28, MUTED), 1250, t, D * 0.6)

def s_method(fr, t, D):
    dots(fr, 3); show(fr, kicker("How it is tested today"), 260, t, 0.1)
    flowc = [("PR3 and MPO tests (immunoassay)", "First test", TEALG), ("Strong suspicion but negative, or low positive", "Add microscope test (IIF)", AMBER)]
    lay, d = overlay(fr)
    for i, (q, a, c) in enumerate(flowc):
        tin = D * (0.12 + 0.25 * i); e = ease((t - tin) / 0.5)
        if t < tin: continue
        y = 360 + i * 260
        d.rounded_rectangle((X0, y, X0 + 460, y + 190), 22, fill=(255, 255, 255, int(22 * e)), outline=(255, 255, 255, int(60 * e)), width=2)
        for j, line in enumerate(wrap(q, font("Medium", 32), 420)): d.text((X0 + 22, y + 26 + j * 42), line, font=font("Medium", 32), fill=(*SOFT, int(255 * e)))
        d.rounded_rectangle((X0 + 500, y + 40, X0 + TW, y + 150), 22, fill=(*c, int(230 * e)))
        for j, line in enumerate(wrap(a, font("Bold", 32), TW - 540)): d.text((X0 + 520, y + 60 + j * 40), line, font=font("Bold", 32), fill=(*INK, int(255 * e)))
    fr.alpha_composite(lay)
    show(fr, source_tag("Revised 2017 international consensus on ANCA testing; Mayo Clinic Laboratories"), 920, t, D * 0.6)
    scope(fr, CTEX, 540, 1290, 380, t, D, ease((t - D * 0.55) / 0.6))

def s_disease(fr, t, D):
    dots(fr, 4); show(fr, kicker("Which disease?"), 260, t, 0.1)
    cards(fr, t, D, [("PR3 / c-ANCA: often GPA (nose, lungs, kidneys)", CYAN), ("MPO / p-ANCA: often microscopic polyangiitis and EGPA", LAV),
                     ("p-ANCA can also appear in some other diseases and with some medicines", AMBER)], 340, 33, 170, 0.1, 0.2)
    vessel(fr, 540, 1180, t, 1.0)

def s_when(fr, t, D):
    dots(fr, 5); show(fr, kicker("When do doctors order it?"), 260, t, 0.1)
    cards(fr, t, D, [("Long-standing sinus problems, nasal crusting, nosebleeds", CORAL), ("Blood in cough", CORAL), ("Blood or protein in urine, rising creatinine", AMBER),
                     ("Skin rash, numbness in hands or feet", LAV), ("Unexplained fever and weight loss", CYAN), ("Asthma with high eosinophils", TEALG)], 330, 32, 135, 0.06, 0.09)

def s_report(fr, t, D):
    dots(fr, 6); show(fr, kicker("Reading the report"), 260, t, 0.1)
    scope(fr, NTEX, 540, 560, 380, t, D, ease((t - 0.3) / 0.6), "Negative (illustration)", MUTED)
    cards(fr, t, D, [("Positive alone is not a diagnosis", AMBER), ("Negative does not fully rule out vasculitis", CORAL),
                     ("Doctor decides with symptoms, other tests, sometimes a biopsy", TEALG)], 870, 33, 160, 0.3, 0.15)

def s_note(fr, t, D):
    dots(fr, 7); show(fr, kicker("Important", CORAL), 260, t, 0.1)
    show(fr, headline("Kidney vasculitis can progress fast", 58), 320, t, 0.3)
    show(fr, callout("Early diagnosis and treatment matter", AMBER, 36), 480, t, D * 0.25); fire("ding", D * 0.25)
    cards(fr, t, D, [("Blood sample; no fasting needed", CYAN), ("Doctor may repeat it during treatment", TEALG)], 640, 34, 150, 0.45, 0.15)
    put(fr, tube_sprite((200, 60, 60), "SERUM"), 540, 1200, 1.0, ease((t - D * 0.6) / 0.5))

SC = [(film(s_hook), "doc"), (film(s_what), "doc"), (film(s_patterns), "doc"), (film(s_method), "doc"), (film(s_disease), "doc"),
      (film(s_when), "doc"), (film(s_report), "doc"), (film(s_note), "doc"), (close_scene("Heard of the ANCA test?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        ims = []
        for si, (fn, bg) in enumerate(SC):
            d = 16 if si < len(SC) - 1 else 33; p = .95 if si else 0.125; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((360, 640)))
        s = Image.new("RGB", (360 * 5, 640 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 360, (i // 5) * 640))
        s.save("sheet_anca.png")
    else: run(SC, "/tmp/anca_", "ANCA_Test_Hindi.mp4")
