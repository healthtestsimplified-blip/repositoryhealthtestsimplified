"""Documentary / medical-infographic style for Health Test Simplified.
No cartoon characters: dark clinical backgrounds, realistic medical illustrations, kinetic typography.
Import AFTER lft_cartoon2 so BASES gets the new keys ("doc", "docl")."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from lft_cartoon2 import *
import lft_cartoon2 as L2

# ---------------- palette ----------------
INK = (8, 18, 38); INK2 = (16, 42, 78)
CYAN = (0, 188, 212); TEALG = (38, 198, 170); CORAL = (255, 110, 110); AMBER = (255, 193, 7)
LAV = (179, 157, 219); MUTED = (165, 184, 208); SOFT = (225, 235, 245)

# ---------------- backgrounds ----------------
def _doc_bg():
    y = np.linspace(0, 1, H)[:, None, None]; x = np.linspace(-1, 1, W)[None, :, None]
    base = np.array(INK) * (1 - y) + np.array(INK2) * y
    glow = np.exp(-(((x) ** 2) / 0.5 + ((y - 0.32) ** 2) / 0.08))
    arr = base + glow * np.array([0, 60, 80]) * 0.55
    vig = 1 - 0.35 * (x ** 2) * 0.8 - 0.25 * ((y - 0.5) * 2) ** 4
    arr = np.clip(arr * vig, 0, 255).astype(np.uint8)
    img = Image.fromarray(np.broadcast_to(arr, (H, W, 3)).copy()).convert("RGBA")
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for yy in range(200, H, 48):
        for xx in range(24, W, 48): d.ellipse((xx - 1.5, yy - 1.5, xx + 1.5, yy + 1.5), fill=(255, 255, 255, 16))
    img.alpha_composite(lay)
    b = img.copy(); b.alpha_composite(L2.HW, (0, 40)); return b

def _docl_bg():
    y = np.linspace(0, 1, H)[:, None]
    arr = (np.array([244, 248, 252]) * (1 - y)[..., None] + np.array([228, 238, 248]) * y[..., None]).repeat(W, 1)
    img = Image.fromarray(arr.astype(np.uint8)).convert("RGBA")
    b = img.copy(); b.alpha_composite(HEADER, (0, 40)); return b

BASES["doc"] = _doc_bg(); BASES["docl"] = _docl_bg()

# ---------------- typography ----------------
X0 = 80; TW = W - 2 * X0

def kicker(text, col=CYAN, size=30):
    f = font("Bold", size); sp = 4
    im = Image.new("RGBA", (W, size + 24), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((X0, size // 2 + 2, X0 + 56, size // 2 + 8), 3, fill=col)
    x = X0 + 76
    for ch in text.upper():
        d.text((x, 0), ch, font=f, fill=col); x += f.getlength(ch) + sp
    return im

def headline(text, size=72, col=WHITE, weight="Bold", maxw=TW, spacing=1.15):
    f = font(weight, size); lines = wrap(text, f, maxw); lh = int(size * spacing)
    im = Image.new("RGBA", (W, lh * len(lines) + 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, l in enumerate(lines): d.text((X0, i * lh), l, font=f, fill=col)
    return im

def body(text, size=40, col=MUTED):
    return headline(text, size, col, "Regular", spacing=1.35)

def gcard(text, accent=CYAN, idx=None, size=40, dark=True):
    f = font("Medium", size); lines = wrap(text, f, TW - 150); lh = int(size * 1.3); h = lh * len(lines) + 46
    im = Image.new("RGBA", (W, h + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    fill = (255, 255, 255, 20) if dark else (255, 255, 255, 235)
    edge = (255, 255, 255, 46) if dark else (200, 214, 232, 255)
    d.rounded_rectangle((X0, 0, X0 + TW, h), 26, fill=fill, outline=edge, width=2)
    d.rounded_rectangle((X0, 0, X0 + 10, h), 5, fill=accent)
    if idx is not None:
        d.text((X0 + 62, h / 2), str(idx), font=font("Bold", size + 6), fill=accent, anchor="mm")
    tx = X0 + (110 if idx is not None else 46)
    for i, l in enumerate(lines): d.text((tx, 23 + i * lh), l, font=f, fill=WHITE if dark else INK)
    return im

def callout(text, col=CORAL, size=40):
    f = font("Bold", size); lines = wrap(text, f, TW - 90); lh = int(size * 1.3); h = lh * len(lines) + 44
    im = Image.new("RGBA", (W, h + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((X0, 0, X0 + TW, h), 26, fill=(*col, 40), outline=col, width=3)
    for i, l in enumerate(lines): d.text((W / 2, 22 + i * lh + lh / 2), l, font=f, fill=WHITE, anchor="mm")
    return im

def source_tag(text):
    return headline("Source: " + text, 26, (130, 150, 175), "Regular")

def chapter(n, total=8):
    """small 'chapter' progress dots under the header"""
    im = Image.new("RGBA", (W, 30), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k in range(total):
        x = W - 80 - (total - 1 - k) * 26
        d.ellipse((x - 6, 9, x + 6, 21), fill=CYAN if k < n else (255, 255, 255, 50))
    return im

def type_on(fr, text, y, t, tin, size=72, col=WHITE, cps=28):
    """Typewriter headline"""
    k = int(max(0, t - tin) * cps)
    if k <= 0: return
    im = headline(text[:k], size, col); fr.alpha_composite(im, (0, int(y)))

def counter(fr, val, suffix, y, t, tin, dur=1.2, size=150, col=AMBER, prefix=""):
    p = ease((t - tin) / dur)
    if t < tin: return
    v = int(round(val * p))
    s = f"{prefix}{v}{suffix}"
    f = font("Bold", size); d = ImageDraw.Draw(fr)
    d.text((X0, y), s, font=f, fill=col)

# ---------------- sprites (supersampled) ----------------
def _ss(w, h, k=2): return Image.new("RGBA", (w * k, h * k), (0, 0, 0, 0))
def _down(im, k=2): return im.resize((im.width // k, im.height // k), Image.LANCZOS)
def with_glow(spr, col, r=18, a=150):
    g = Image.new("RGBA", spr.size, (*col, 0)); g.putalpha(spr.getchannel("A").point(lambda v: int(v * a / 255)))
    g = g.filter(ImageFilter.GaussianBlur(r)); g.alpha_composite(spr); return g

def helix(fr, cx, cy, h, t, amp=150, turns=2.2, col1=CYAN, col2=LAV, alpha=255, n=46):
    """Rotating DNA double helix, drawn per frame (depth-sorted)."""
    lay = Image.new("RGBA", fr.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    items = []
    for i in range(n):
        u = i / (n - 1); y = cy - h / 2 + u * h; a = u * turns * 2 * math.pi + t * 1.3
        for s, col in ((0, col1), (math.pi, col2)):
            z = math.cos(a + s); x = cx + amp * math.sin(a + s)
            items.append((z, x, y, col, i, s))
        if i % 2 == 0:
            xa = cx + amp * math.sin(a); xb = cx + amp * math.sin(a + math.pi)
            za = (math.cos(a) + math.cos(a + math.pi)) / 2
            items.append((za - 0.01, (xa, xb), y, None, i, -1))
    items.sort(key=lambda r: r[0])
    for z, x, y, col, i, s in items:
        k = 0.45 + 0.55 * (z + 1) / 2
        if col is None:
            d.line((x[0], y, x[1], y), fill=(200, 220, 240, int(alpha * 0.35)), width=4); continue
        r = 9 + 6 * (z + 1) / 2
        c = tuple(int(v * k) for v in col)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(*c, alpha))
    fr.alpha_composite(lay)

def chromosome_sprite(label="Chromosome 5", mark_frac=0.62, mark_lab="SMN1 (5q13)"):
    k = 2; w, h = 300, 820; im = _ss(w, h, k); d = ImageDraw.Draw(im)
    cx = w * k / 2; top = 30 * k; bot = (h - 120) * k; cen = top + (bot - top) * 0.28; arm = 62 * k
    for x0 in (cx - arm * 1.05, cx + arm * 0.05):
        d.rounded_rectangle((x0, top, x0 + arm, cen - 10 * k), arm // 2, fill=(120, 150, 210))
        d.rounded_rectangle((x0, cen + 10 * k, x0 + arm, bot), arm // 2, fill=(120, 150, 210))
    bands = [0.06, 0.12, 0.2, 0.36, 0.44, 0.52, 0.58, 0.7, 0.78, 0.86, 0.93]
    for b in bands:
        y = top + (bot - top) * b
        if abs(y - cen) < 18 * k: continue
        d.rectangle((cx - arm * 1.05 + 6, y, cx + arm * 1.05 - 6, y + 12 * k), fill=(60, 80, 140))
    d.ellipse((cx - 26 * k, cen - 22 * k, cx + 26 * k, cen + 22 * k), fill=(90, 110, 170))
    my = top + (bot - top) * mark_frac
    d.rectangle((cx - arm * 1.05, my, cx + arm * 1.05, my + 16 * k), fill=AMBER)
    im = _down(im, k)
    lay = Image.new("RGBA", (w + 420, h), (0, 0, 0, 0)); lay.alpha_composite(im, (0, 0)); d = ImageDraw.Draw(lay)
    myd = my / k + 8
    d.line((w / 2 + 70, myd, w + 40, myd), fill=AMBER, width=4)
    d.text((w + 50, myd), mark_lab, font=font("Bold", 38), fill=AMBER, anchor="lm")
    d.text((w / 2, h - 70), label, font=font("Medium", 34), fill=MUTED, anchor="mm")
    return with_glow(lay, (90, 130, 220), 14, 90)

def neuron_path():
    """Points of the axon from spinal cord (left) to muscle (right)."""
    return [(250 + i * 12, 640 + 60 * math.sin(i / 9)) for i in range(48)]

def neuron_sprite():
    k = 2; im = _ss(W, 1000, k); d = ImageDraw.Draw(im); S = lambda *p: tuple(v * k for v in p)
    # spinal cord segment (left)
    d.rounded_rectangle(S(40, 330, 250, 950), 100 * k, fill=(60, 80, 120))
    d.rounded_rectangle(S(80, 360, 210, 920), 70 * k, fill=(150, 160, 190))
    # cell body with dendrites
    cx, cy = 180, 640
    for a in range(0, 360, 45):
        r1 = 90; ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        d.line(S(cx, cy, cx + r1 * ca, cy + r1 * sa), fill=AMBER, width=8 * k)
        d.line(S(cx + r1 * ca, cy + r1 * sa, cx + (r1 + 30) * math.cos(math.radians(a + 20)), cy + (r1 + 30) * math.sin(math.radians(a + 20))), fill=AMBER, width=5 * k)
    d.ellipse(S(cx - 46, cy - 46, cx + 46, cy + 46), fill=(255, 202, 40))
    d.ellipse(S(cx - 18, cy - 18, cx + 18, cy + 18), fill=(230, 120, 30))
    # axon with myelin
    pts = neuron_path()
    d.line([S(*p) for p in pts], fill=(255, 202, 40), width=8 * k)
    for i in range(4, len(pts) - 4, 6):
        x, y = pts[i]; d.rounded_rectangle(S(x - 26, y - 15, x + 26, y + 15), 15 * k, fill=(120, 200, 150))
    ex, ey = pts[-1]
    # muscle bundle
    mx0, my0 = 800, 470
    for j in range(7):
        yy = my0 + j * 52
        d.rounded_rectangle(S(mx0, yy, mx0 + 230, yy + 46), 23 * k, fill=(200, 80, 80))
        for s in range(mx0 + 14, mx0 + 220, 14): d.line(S(s, yy + 8, s, yy + 38), fill=(160, 50, 55), width=2 * k)
    for j in range(5):
        d.line(S(ex, ey, mx0 + 10, my0 + 30 + j * 70), fill=(255, 202, 40), width=4 * k)
    im = _down(im, k)
    return with_glow(im, (255, 200, 80), 10, 60)

NEURON = None
def neuron(fr, y0, t, alive=1.0):
    global NEURON
    if NEURON is None: NEURON = neuron_sprite()
    spr = NEURON
    if alive < 1:
        spr = NEURON.copy(); g = spr.convert("LA").convert("RGBA"); spr = Image.blend(g, NEURON, alive)
    fr.alpha_composite(spr, (0, int(y0)))
    if alive > 0.4:
        d = ImageDraw.Draw(fr); pts = neuron_path()
        for k in range(3):
            i = int((t * 30 + k * 16) % len(pts)); x, y = pts[i]
            d.ellipse((x - 11, y0 + y - 11, x + 11, y0 + y + 11), fill=(255, 255, 255))

def cord_section(fr, cx, cy, r, t, loss=0.0):
    d = ImageDraw.Draw(fr)
    d.ellipse((cx - r, cy - r * 0.8, cx + r, cy + r * 0.8), fill=(220, 225, 235), outline=(150, 165, 190), width=6)
    gm = [(-0.55, -0.45), (-0.2, -0.15), (-0.12, 0.0), (-0.25, 0.2), (-0.6, 0.55), (-0.15, 0.35), (0, 0.15),
          (0.15, 0.35), (0.6, 0.55), (0.25, 0.2), (0.12, 0.0), (0.2, -0.15), (0.55, -0.45), (0, -0.1)]
    d.polygon([(cx + x * r, cy + y * r * 0.8) for x, y in gm], fill=(150, 125, 140))
    d.ellipse((cx - 10, cy - 8, cx + 10, cy + 12), fill=(90, 90, 110))
    cells = [(-0.45, 0.42), (-0.35, 0.5), (-0.52, 0.32), (0.45, 0.42), (0.35, 0.5), (0.52, 0.32)]
    for k, (x, y) in enumerate(cells):
        gone = k / len(cells) < loss
        c = (120, 120, 130) if gone else (255, 202, 40)
        rr = 13 if not gone else 8
        d.ellipse((cx + x * r - rr, cy + y * r * 0.8 - rr, cx + x * r + rr, cy + y * r * 0.8 + rr), fill=c)

def exon_bar(fr, x, y, w, missing=None, lab=None, h=64, t=0, tin=0):
    if t < tin: return
    lay = Image.new("RGBA", fr.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay); n = 8; bw = w / n
    if lab: d.text((x, y - 48), lab, font=font("Medium", 32), fill=MUTED)
    d.line((x, y + h / 2, x + w, y + h / 2), fill=(255, 255, 255, 120), width=3)
    for i in range(n):
        if t < tin + i * 0.06: break
        x0 = x + i * bw + 6
        if missing is not None and i == missing:
            for k2 in range(0, int(bw - 12), 14):
                d.line((x0 + k2, y, x0 + k2 + 7, y), fill=CORAL, width=3); d.line((x0 + k2, y + h, x0 + k2 + 7, y + h), fill=CORAL, width=3)
            d.line((x0, y, x0, y + h), fill=CORAL, width=3); d.line((x0 + bw - 12, y, x0 + bw - 12, y + h), fill=CORAL, width=3)
            continue
        col = AMBER if i == 6 else (70, 120, 200)
        d.rounded_rectangle((x0, y, x0 + bw - 12, y + h), 12, fill=col)
        d.text((x0 + (bw - 12) / 2, y + h / 2), str(i + 1), font=font("Bold", 28), fill=WHITE if i != 6 else INK, anchor="mm")
    fr.alpha_composite(lay)

def pedigree(fr, y, t, tin):
    """Standard pedigree: carriers half-shaded, affected filled."""
    d = ImageDraw.Draw(fr); s = 70; col = (230, 236, 245)
    def male(x, yy, kind):
        d.rectangle((x - s / 2, yy - s / 2, x + s / 2, yy + s / 2), outline=col, width=5)
        if kind == "c": d.rectangle((x - s / 2, yy - s / 2, x, yy + s / 2), fill=AMBER)
        if kind == "a": d.rectangle((x - s / 2 + 3, yy - s / 2 + 3, x + s / 2 - 3, yy + s / 2 - 3), fill=CORAL)
    def fem(x, yy, kind):
        d.ellipse((x - s / 2, yy - s / 2, x + s / 2, yy + s / 2), outline=col, width=5)
        if kind == "c": d.chord((x - s / 2, yy - s / 2, x + s / 2, yy + s / 2), 90, 270, fill=AMBER)
        if kind == "a": d.ellipse((x - s / 2 + 3, yy - s / 2 + 3, x + s / 2 - 3, yy + s / 2 - 3), fill=CORAL)
    if t < tin: return
    fem(380, y, "c"); male(700, y, "c")
    d.line((380 + s / 2, y, 700 - s / 2, y), fill=col, width=5); d.line((540, y, 540, y + 110), fill=col, width=5)
    d.text((380, y - 75), "Mother", font=font("Medium", 30), fill=MUTED, anchor="mm")
    d.text((700, y - 75), "Father", font=font("Medium", 30), fill=MUTED, anchor="mm")
    xs = [210, 430, 650, 870]; kids = [("n", "Not affected", TEALG), ("c", "Carrier", AMBER), ("c", "Carrier", AMBER), ("a", "SMA", CORAL)]
    if t < tin + 0.5: return
    d.line((xs[0], y + 110, xs[-1], y + 110), fill=col, width=5)
    for i, (x, (kd, lab, c)) in enumerate(zip(xs, kids)):
        if t < tin + 0.6 + i * 0.5: break
        d.line((x, y + 110, x, y + 160), fill=col, width=5)
        (male if i % 2 else fem)(x, y + 200, kd)
        d.text((x, y + 270), lab, font=font("Bold", 30), fill=c, anchor="mm")
        d.text((x, y + 310), "25%", font=font("Medium", 28), fill=MUTED, anchor="mm")

def person_grid(fr, n, hi, x0, y0, cols, t, tin, gap=62):
    d = ImageDraw.Draw(fr)
    for k in range(n):
        if t < tin + k * 0.025: break
        r, c = divmod(k, cols); x = x0 + c * gap; y = y0 + r * 84
        col = AMBER if k == hi else (90, 110, 140)
        d.ellipse((x - 13, y - 34, x + 13, y - 8), fill=col); d.rounded_rectangle((x - 20, y - 4, x + 20, y + 34), 14, fill=col)

def tube_sprite(cap=(149, 117, 205), lab="EDTA"):
    k = 2; w, h = 170, 560; im = _ss(w, h, k); d = ImageDraw.Draw(im); S = lambda *p: tuple(v * k for v in p)
    d.rounded_rectangle(S(30, 20, 140, 110), 16 * k, fill=cap)
    d.rectangle(S(36, 30, 50, 100), fill=tuple(min(255, c + 50) for c in cap))
    d.rounded_rectangle(S(40, 100, 130, 540), 45 * k, fill=(235, 242, 250, 120), outline=(220, 230, 245), width=3 * k)
    d.rounded_rectangle(S(46, 250, 124, 534), 39 * k, fill=(150, 20, 35))
    d.rectangle(S(46, 250, 124, 300), fill=(170, 30, 45))
    d.rectangle(S(40, 150, 130, 240), fill=(250, 250, 250))
    d.text(S(85, 195), lab, font=font("Bold", 20 * k), fill=(60, 60, 80), anchor="mm")
    d.rounded_rectangle(S(52, 110, 62, 520), 5 * k, fill=(255, 255, 255, 110))
    return with_glow(_down(im, k), (180, 60, 80), 16, 70)

def peaks(fr, x, y, w, h, heights, labels, t, tin, title=None, col=CYAN):
    """Electropherogram-style MLPA mini chart."""
    lay = Image.new("RGBA", fr.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((x, y, x + w, y + h), 20, fill=(255, 255, 255, 14), outline=(255, 255, 255, 40), width=2)
    if title: d.text((x + 24, y + 18), title, font=font("Bold", 32), fill=WHITE)
    base = y + h - 60; n = len(heights); p = ease((t - tin) / 1.0)
    pts = [(x + 20, base)]
    for i, hv in enumerate(heights):
        cxp = x + 60 + i * (w - 120) / max(1, n - 1)
        for k in range(-8, 9):
            xx = cxp + k * 6; yy = base - hv * p * (h - 130) * math.exp(-(k / 3.2) ** 2)
            pts.append((xx, yy))
        d.text((cxp, base + 30), labels[i], font=font("Medium", 26), fill=MUTED, anchor="mm")
    pts.append((x + w - 20, base))
    d.line(pts, fill=col, width=4); fr.alpha_composite(lay)

def capsule(fr, cx, cy, s, t, a=0.0):
    lay = Image.new("RGBA", (int(s * 2.4), int(s * 2.4)), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    c = s * 1.2
    d.rounded_rectangle((c - s, c - s * 0.42, c + s, c + s * 0.42), int(s * 0.42), fill=(240, 244, 250))
    d.rounded_rectangle((c - s, c - s * 0.42, c, c + s * 0.42), int(s * 0.42), fill=CYAN)
    d.rectangle((c - s * 0.5, c - s * 0.42, c, c + s * 0.42), fill=CYAN)
    d.rounded_rectangle((c - s * 0.8, c - s * 0.3, c + s * 0.7, c - s * 0.18), 6, fill=(255, 255, 255, 140))
    lay = lay.rotate(25 + 6 * math.sin(t), resample=Image.BICUBIC)
    lay = with_glow(lay, CYAN, 20, 80)
    fr.alpha_composite(lay, (int(cx - lay.width / 2), int(cy - lay.height / 2)))

def overlay(fr):
    """Context helper: returns (layer, draw); call fr.alpha_composite(layer) after drawing translucent shapes."""
    lay = Image.new("RGBA", fr.size, (0, 0, 0, 0)); return lay, ImageDraw.Draw(lay)
