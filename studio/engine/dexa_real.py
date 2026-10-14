"""DEXA bone density scan, realistic documentary style."""
import math, sys, random
from cbc_cartoon import run
from real_style import *
from hts_close import close_scene

TOPIC = "DEXA  •  BONE DENSITY"

def _gray_noise(w, h, seed, s=1.2):
    a = np.random.default_rng(seed).normal(0, 1, (h, w)).astype(np.float32)
    return np.asarray(Image.fromarray(((a * 30) + 128).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(s))).astype(np.float32) / 255 - 0.5

def dexa_spine(w=620, h=1000, seed=2):
    im = Image.new("L", (w, h), 40); d = ImageDraw.Draw(im)
    d.rounded_rectangle((w * 0.18, 0, w * 0.82, h), 120, fill=62)
    ys = [0.06, 0.28, 0.5, 0.72]; bh = h * 0.19
    for i, y in enumerate(ys):
        y0 = y * h; x0 = w * 0.27 - i * 6; x1 = w * 0.73 + i * 6
        d.rounded_rectangle((x0 - 6, y0 - 6, x1 + 6, y0 + bh + 6), 34, fill=185)
        d.rounded_rectangle((x0 + 8, y0 + 8, x1 - 8, y0 + bh - 8), 28, fill=150)
        for sg in (-1, 1):
            cx = w / 2 + sg * (x1 - x0) * 0.32
            d.ellipse((cx - 28, y0 + bh * 0.25, cx + 28, y0 + bh * 0.7), fill=175)
    d.polygon([(w * 0.05, h * 0.95), (w * 0.3, h * 0.92), (w * 0.5, h * 0.96), (w * 0.7, h * 0.92), (w * 0.95, h * 0.95), (w, h), (0, h)], fill=160)
    im = im.filter(ImageFilter.GaussianBlur(4))
    a = np.asarray(im).astype(np.float32) / 255 + 0.08 * _gray_noise(w, h, seed, 1.5) + 0.04 * _gray_noise(w, h, seed + 1, 0.6)
    g = (a.clip(0, 1) * 255).astype(np.uint8)
    out = Image.merge("RGBA", (Image.fromarray(g), Image.fromarray(g), Image.fromarray((g * 0.97).astype(np.uint8)), Image.new("L", (w, h), 255)))
    dd = ImageDraw.Draw(out)
    for i, y in enumerate(ys):
        y0 = y * h; dd.rectangle((w * 0.22, y0 - 10, w * 0.78, y0 + bh + 10), outline=(80, 220, 120), width=3)
        dd.text((w * 0.12, y0 + bh / 2), f"L{i + 1}", font=font("Bold", 34), fill=(80, 220, 120), anchor="mm")
    return out

def dexa_hip(w=620, h=700, seed=5):
    im = Image.new("L", (w, h), 45); d = ImageDraw.Draw(im)
    d.polygon([(0, 0), (w * 0.45, 0), (w * 0.38, h * 0.3), (0, h * 0.45)], fill=120)
    d.ellipse((w * 0.22, h * 0.12, w * 0.5, h * 0.4), fill=190)
    d.polygon([(w * 0.42, h * 0.22), (w * 0.62, h * 0.34), (w * 0.58, h * 0.5), (w * 0.38, h * 0.36)], fill=175)
    d.ellipse((w * 0.55, h * 0.3, w * 0.78, h * 0.55), fill=185)
    d.rounded_rectangle((w * 0.56, h * 0.42, w * 0.8, h), 50, fill=180); d.rounded_rectangle((w * 0.6, h * 0.55, w * 0.76, h), 30, fill=150)
    im = im.filter(ImageFilter.GaussianBlur(5))
    a = np.asarray(im).astype(np.float32) / 255 + 0.08 * _gray_noise(w, h, seed, 1.5)
    g = (a.clip(0, 1) * 255).astype(np.uint8)
    out = Image.merge("RGBA", (Image.fromarray(g), Image.fromarray(g), Image.fromarray(g), Image.new("L", (w, h), 255)))
    dd = ImageDraw.Draw(out)
    box = [(w * 0.4, h * 0.24), (w * 0.6, h * 0.36), (w * 0.56, h * 0.5), (w * 0.36, h * 0.38)]
    dd.polygon(box, outline=(80, 220, 120)); dd.line(box + [box[0]], fill=(80, 220, 120), width=3)
    dd.text((w * 0.3, h * 0.55), "Femoral neck", font=font("Bold", 28), fill=(80, 220, 120))
    return out

def trabecular(n=700, thick=7, keep=1.0, seed=3):
    """Micro-CT style bone: white trabeculae on dark marrow."""
    from scipy.spatial import Voronoi
    r = np.random.default_rng(seed); rr = random.Random(seed)
    pts = r.uniform(-50, n + 50, (110, 2)); vor = Voronoi(pts)
    im = Image.new("L", (n, n), 18); d = ImageDraw.Draw(im)
    for (a, b) in vor.ridge_vertices:
        if a < 0 or b < 0 or rr.random() > keep: continue
        p, q = vor.vertices[a], vor.vertices[b]
        wdt = max(1, int(thick * rr.uniform(0.6, 1.3)))
        d.line((tuple(p), tuple(q)), fill=230, width=wdt)
    im = im.filter(ImageFilter.GaussianBlur(1.6))
    a = np.asarray(im).astype(np.float32) / 255 + 0.05 * _gray_noise(n, n, seed, 1.0)
    g = (a.clip(0, 1) * 255).astype(np.uint8)
    out = Image.merge("RGBA", (Image.fromarray(g), Image.fromarray((g * 0.97).astype(np.uint8)), Image.fromarray((g * 0.92).astype(np.uint8)), Image.new("L", (n, n), 255)))
    return out

SPINE = dexa_spine(); HIP = dexa_hip()
HEALTHY = trabecular(700, 9, 1.0, 3); OSTEO = trabecular(700, 3, 0.55, 3)

def framed(fr, im, cx, cy, sc=1.0, a=1.0, title=None):
    s = im.resize((int(im.width * sc), int(im.height * sc)), Image.BILINEAR)
    lay = Image.new("RGBA", (s.width + 16, s.height + 16), (255, 255, 255, 40)); lay.alpha_composite(s, (8, 8))
    put(fr, lay, cx, cy, 1.0, a)
    if title and a > 0.5:
        l, d = overlay(fr); d.text((cx, cy + lay.height / 2 + 30), title, font=font("Bold", 34), fill=SOFT, anchor="mm"); fr.alpha_composite(l)

def scanner(fr, cx, cy, t, D):
    lay, d = overlay(fr)
    d.rounded_rectangle((cx - 450, cy + 40, cx + 450, cy + 110), 30, fill=(225, 230, 238, 255))
    d.rounded_rectangle((cx - 430, cy + 110, cx - 380, cy + 300), 12, fill=(170, 180, 195, 255))
    d.rounded_rectangle((cx + 380, cy + 110, cx + 430, cy + 300), 12, fill=(170, 180, 195, 255))
    # patient (side silhouette)
    d.ellipse((cx - 400, cy - 30, cx - 300, cy + 50), fill=(205, 165, 135, 255))
    d.rounded_rectangle((cx - 310, cy - 20, cx + 330, cy + 45), 32, fill=(120, 150, 200, 255))
    d.rounded_rectangle((cx + 300, cy - 5, cx + 420, cy + 40), 20, fill=(90, 110, 150, 255))
    sx = cx - 300 + ((t * 70) % 600)
    d.rounded_rectangle((sx - 60, cy - 320, sx + 60, cy - 260), 16, fill=(240, 244, 250, 255))
    d.rectangle((sx + 40, cy - 300, sx + 60, cy + 40), fill=(200, 208, 220, 255))
    d.polygon([(sx - 30, cy - 260), (sx + 30, cy - 260), (sx + 70, cy + 30), (sx - 70, cy + 30)], fill=(120, 220, 255, 60))
    fr.alpha_composite(lay)

def t_scale(fr, y, val, t, tin):
    lay, d = overlay(fr)
    x0, x1 = X0 + 20, X0 + TW - 20
    def X(v): return x0 + (1.5 - v) / 5.5 * (x1 - x0)
    zones = [(1.5, -1.0, TEALG, "Normal"), (-1.0, -2.5, AMBER, "Osteopenia"), (-2.5, -4.0, CORAL, "Osteoporosis")]
    for i, (a, b, c, lab) in enumerate(zones):
        tin_i = tin + i * 0.6
        if t < tin_i: continue
        e = ease((t - tin_i) / 0.5)
        d.rectangle((X(a), y, X(a) + (X(b) - X(a)) * e, y + 70), fill=(*c, 220))
        d.text(((X(a) + X(b)) / 2, y + 120), lab, font=font("Bold", 34), fill=(*c, int(255 * e)), anchor="mm")
    for v in (1, 0, -1, -2, -2.5, -3, -4):
        d.line((X(v), y + 70, X(v), y + 84), fill=(255, 255, 255, 140), width=2)
        if v in (1, -1, -2.5, -4): d.text((X(v), y - 26), f"{v:+g}" if v else "0", font=font("Medium", 28), fill=SOFT, anchor="mm")
    if val is not None and t > tin + 2.0:
        e = ease((t - tin - 2.0) / 1.2); v = 0.8 + (val - 0.8) * e
        d.polygon([(X(v), y - 50), (X(v) - 18, y - 80), (X(v) + 18, y - 80)], fill=WHITE)
    fr.alpha_composite(lay)

def dots(fr, n): fr.alpha_composite(chapter(n, 9), (0, 110))
def label(fr, text, x, y, col=SOFT, size=32, anchor="mm", weight="Medium"):
    lay, d = overlay(fr); d.text((x, y), text, font=font(weight, size), fill=col, anchor=anchor); fr.alpha_composite(lay)

# ---------------- scenes ----------------
def x_hook(fr, t, D):
    framed(fr, SPINE, 540, 1220, 0.72 + 0.03 * t / D, ease(t / 0.8))
    show(fr, kicker("DEXA  •  Bone density scan", CYAN), 330, t, 0.1)
    type_on(fr, "Bone broke from a small fall?", 410, t, 0.4, 66)
    if t > D * 0.35: type_on(fr, "Are your bones weak inside?", 600, t, D * 0.35, 64, AMBER)
    show(fr, callout("The answer: a DEXA scan", CYAN, 40), 1680, t, D * 0.6); fire("whoosh", D * 0.6)

def x_what(fr, t, D):
    dots(fr, 1)
    show(fr, kicker("What is DEXA?"), 260, t, 0.1)
    show(fr, headline("Dual-Energy X-ray Absorptiometry", 56), 320, t, 0.3)
    framed(fr, SPINE, 300, 860, 0.5, ease((t - 0.4) / 0.6), "Lumbar spine")
    framed(fr, HIP, 790, 800, 0.62, ease((t - 0.8) / 0.6), "Hip")
    show(fr, gcard("Two low-energy X-ray beams measure bone mineral density (BMD)", CYAN, None, 36), 1250, t, D * 0.35)
    show(fr, gcard("Usually the lower spine and the hip", AMBER, None, 38), 1410, t, D * 0.6)

def x_osteo(fr, t, D):
    dots(fr, 2)
    show(fr, kicker("Osteoporosis"), 260, t, 0.1)
    show(fr, headline("Bones become thin and weak inside", 60), 320, t, 0.3)
    put(fr, eyepiece(HEALTHY, 400, t, 1.0, 1.15, D, (0, 0)), 290, 720, 1.0, ease((t - 0.4) / 0.6))
    if t > D * 0.25: put(fr, eyepiece(OSTEO, 400, t, 1.0, 1.15, D, (0, 0)), 790, 720, 1.0, ease((t - D * 0.25) / 0.6))
    label(fr, "Healthy bone", 290, 960, TEALG, 36, weight="Bold")
    if t > D * 0.25: label(fr, "Osteoporosis", 790, 960, CORAL, 36, weight="Bold"); fire("boom", D * 0.25)
    show(fr, gcard("It grows silently; often the first sign is a fracture", CORAL, None, 38), 1060, t, D * 0.45)
    show(fr, gcard("A major health problem in India", AMBER, None, 38), 1210, t, D * 0.65)
    show(fr, source_tag("ISBMR position statement, Archives of Osteoporosis 2021"), 1350, t, D * 0.7)

def x_who(fr, t, D):
    dots(fr, 3)
    show(fr, kicker("Who should get it?"), 260, t, 0.1)
    items = [("Women after menopause; older men", CYAN), ("A bone broken by a minor fall or injury", CORAL), ("Lost 1.5 inches (3.8 cm) or more in height", AMBER),
             ("Long-term steroid medicines", LAV), ("Smokers", (150, 165, 190))]
    for i, (txt, c) in enumerate(items):
        fire("pop", D * (0.08 + 0.13 * i)); show(fr, gcard(txt, c, i + 1, 37), 360 + i * 150, t, D * (0.08 + 0.13 * i))
    show(fr, callout("Your doctor decides if you need it", TEALG, 40), 1150, t, D * 0.8)

def x_safe(fr, t, D):
    dots(fr, 4)
    show(fr, kicker("Is it safe?"), 260, t, 0.1)
    show(fr, headline("Yes. Very low radiation, painless", 60), 320, t, 0.3)
    scanner(fr, 540, 790, t, D)
    lay, d = overlay(fr); e = ease((t - D * 0.3) / 0.8)
    if t > D * 0.3:
        d.text((X0, 1140), "Radiation", font=font("Bold", 36), fill=WHITE)
        for i, (lab, v, c) in enumerate((("Chest X-ray", 1.0, (150, 165, 190)), ("DEXA", 0.08, TEALG))):
            y = 1200 + i * 90
            d.text((X0, y + 22), lab, font=font("Medium", 32), fill=SOFT, anchor="lm")
            d.rounded_rectangle((X0 + 270, y, X0 + 270 + (TW - 270) * v * e, y + 44), 22, fill=c)
        d.text((X0, 1400), "DEXA: less than one-tenth of a chest X-ray", font=font("Regular", 32), fill=SOFT)
    fr.alpha_composite(lay)
    show(fr, gcard("10 to 30 minutes. Pregnant? Tell them first.", AMBER, None, 38), 1470, t, D * 0.6)

def x_prep(fr, t, D):
    dots(fr, 5)
    show(fr, kicker("Preparation"), 260, t, 0.1)
    items = [("Eat normally", TEALG), ("No calcium tablets for 24 hours before", CORAL), ("Loose clothes, no metal; remove jewellery", CYAN),
             ("Recent barium test or CT contrast? Tell them; you may need to wait some days", AMBER)]
    for i, (txt, c) in enumerate(items):
        fire("pop", D * (0.08 + 0.17 * i)); show(fr, gcard(txt, c, i + 1, 36), 360 + i * 165, t, D * (0.08 + 0.17 * i))
    framed(fr, HIP, 540, 1330, 0.5, ease((t - D * 0.5) / 0.6))

def x_tscore(fr, t, D):
    dots(fr, 6)
    show(fr, kicker("The T-score"), 260, t, 0.1)
    show(fr, headline("Your bone vs a healthy young adult", 58), 320, t, 0.3)
    t_scale(fr, 640, -1.8, t, D * 0.15)
    show(fr, gcard("-1 or higher: normal", TEALG, 1, 38), 900, t, D * 0.3)
    show(fr, gcard("Between -1 and -2.5: osteopenia (low bone mass)", AMBER, 2, 36), 1030, t, D * 0.48)
    show(fr, gcard("-2.5 or lower: osteoporosis", CORAL, 3, 38), 1175, t, D * 0.66)
    for k in (0.3, 0.48, 0.66): fire("pop", D * k)
    show(fr, source_tag("RadiologyInfo (ACR/RSNA), Mayo Clinic"), 1320, t, D * 0.75)

def x_zscore(fr, t, D):
    dots(fr, 7)
    show(fr, kicker("The Z-score"), 260, t, 0.1)
    show(fr, headline("Your bone vs people of your own age", 58), 320, t, 0.3)
    lay, d = overlay(fr); p = ease((t - 0.4) / 1.2)
    x0, x1, by, top = X0 + 20, X0 + TW - 20, 950, 580
    pts = []
    for i in range(201):
        u = i / 200
        if u > p: break
        z = -4 + 8 * u; pts.append((x0 + u * (x1 - x0), by - math.exp(-z * z / 2) * (by - top)))
    if len(pts) > 2: d.polygon(pts + [(pts[-1][0], by), (pts[0][0], by)], fill=(*CYAN, 50)); d.line(pts, fill=CYAN, width=4)
    d.line((x0, by, x1, by), fill=(255, 255, 255, 90), width=2)
    for z in (-3, -2, -1, 0, 1, 2, 3):
        xx = x0 + (z + 4) / 8 * (x1 - x0); d.text((xx, by + 30), str(z), font=font("Medium", 28), fill=MUTED, anchor="mm")
    if t > D * 0.45:
        xx = x0 + (-2.6 + 4) / 8 * (x1 - x0); d.line((xx, top, xx, by), fill=CORAL, width=5)
        d.text((xx, top - 30), "Very low", font=font("Bold", 30), fill=CORAL, anchor="mm"); fire("pop", D * 0.45)
    fr.alpha_composite(lay)
    show(fr, gcard("Mainly used for children, young adults, and women before menopause", CYAN, 1, 36), 1060, t, D * 0.3)
    show(fr, gcard("Very low Z-score: the doctor may look for a cause with more tests", CORAL, 2, 36), 1220, t, D * 0.6)

def x_tips(fr, t, D):
    dots(fr, 8)
    show(fr, kicker("Good to know"), 260, t, 0.1)
    items = [("Repeat scans: same centre, same machine, for a fair comparison", CYAN), ("Spine arthritis or past spine surgery can affect results", AMBER),
             ("Treatment is decided only by your doctor", TEALG)]
    for i, (txt, c) in enumerate(items):
        fire("pop", D * (0.1 + 0.2 * i)); show(fr, gcard(txt, c, i + 1, 36), 360 + i * 170, t, D * (0.1 + 0.2 * i))
    framed(fr, SPINE, 540, 1330, 0.42, ease((t - D * 0.4) / 0.6))

SC = [(film(x_hook), "doc"), (film(x_what), "doc"), (film(x_osteo), "doc"), (film(x_who), "doc"), (film(x_safe), "doc"),
      (film(x_prep), "doc"), (film(x_tscore), "doc"), (film(x_zscore), "doc"), (film(x_tips), "doc"),
      (close_scene("Anyone at home had a DEXA scan?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        D = [12, 16, 14, 18, 18, 18, 18, 16, 14, 33]
        ims = []
        for si in range(10):
            fn, bg = SC[si]; d = D[si]; p = 0.95; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((360, 640)))
        s = Image.new("RGB", (360 * 5, 640 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 360, (i // 5) * 640))
        s.save("sheet.png")
    else: run(SC, "/tmp/dexa_", "DEXA_Bone_Density_Hindi.mp4")
