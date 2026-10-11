"""Realistic procedural visuals: H&E microscope tissue, ultrasound, lab objects, film grain.
Builds on doc_style (dark clinical look)."""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
from doc_style import *

RNG = np.random.default_rng(7); random.seed(7)

def _noise(n, scale, seed=0, aniso=1.0, rot=0):
    r = np.random.default_rng(seed); big = int(n * 1.5) if rot else n
    w = max(4, int(big / scale)); h = max(4, int(big / scale / aniso))
    a = r.random((h, w)).astype(np.float32)
    im = Image.fromarray((a * 255).astype(np.uint8)).resize((big, big), Image.BICUBIC)
    if rot:
        im = im.rotate(rot, resample=Image.BICUBIC); o = (big - n) // 2; im = im.crop((o, o, o + n, o + n))
    return np.asarray(im).astype(np.float32) / 255

def _mix(c1, c2, k):
    k = k[..., None]; return np.array(c1) * (1 - k) + np.array(c2) * k

# ---------------- H&E histology ----------------
def he_tissue(n=1400, seed=3, glands=15, stain="he"):
    """Procedural H&E (or IHC 'dab') stained tissue section."""
    r = random.Random(seed)
    f1 = _noise(n, 160, seed); f2 = _noise(n, 40, seed + 1); fib = _noise(n, 22, seed + 2, aniso=5, rot=35) * 0.6 + _noise(n, 26, seed + 3, aniso=4, rot=-20) * 0.4
    k = np.clip(0.6 * f1 + 0.25 * f2 + 0.22 * fib - 0.12, 0, 1)
    if stain == "dab":
        light, deep = (236, 232, 236), (190, 175, 200)
    else:
        light, deep = (246, 205, 222), (214, 112, 160)
    arr = _mix(light, deep, k)
    holes = _noise(n, 220, seed + 5) + 0.25 * _noise(n, 50, seed + 6)
    wm = np.clip((holes - 0.82) * 8, 0, 1)
    arr = _mix(tuple(arr.reshape(-1, 3).mean(0)), (250, 244, 248), wm) * wm[..., None] + arr * (1 - wm[..., None])
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGB")
    d = ImageDraw.Draw(im)
    nuc_d = (70, 40, 120) if stain == "he" else (120, 70, 30)
    nuc_l = (120, 80, 170) if stain == "he" else (165, 105, 50)
    if stain == "dab": nuc_d, nuc_l = (75, 80, 145), (115, 120, 175)
    for _ in range(int(n * n / 900)):
        x, y = r.uniform(0, n), r.uniform(0, n); a = r.uniform(0, math.pi)
        if r.random() < 0.3:
            rr = r.uniform(3.5, 5); d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=nuc_d)
        else:
            L = r.uniform(6, 13); Wd = r.uniform(2.6, 4.5); c = nuc_d if r.random() < 0.5 else nuc_l
            pts = [(x + L * math.cos(a) * math.cos(t) - Wd * math.sin(a) * math.sin(t),
                    y + L * math.sin(a) * math.cos(t) + Wd * math.cos(a) * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 9)]
            d.polygon(pts, fill=c)
    # glands: ring of epithelial nuclei around a clear lumen
    for g in range(glands):
        cx, cy = r.uniform(0.1, 0.9) * n, r.uniform(0.1, 0.9) * n; R = r.uniform(60, 150); ry = R * r.uniform(0.55, 1.0)
        rot = r.uniform(0, math.pi)
        poly = []
        for a in np.linspace(0, 2 * math.pi, 40):
            rr = 1 + 0.12 * math.sin(3 * a + g)
            x, y = R * rr * math.cos(a), ry * rr * math.sin(a)
            poly.append((cx + x * math.cos(rot) - y * math.sin(rot), cy + x * math.sin(rot) + y * math.cos(rot)))
        d.polygon(poly, fill=(236, 170, 205) if stain == "he" else (225, 215, 222))
        inner = [(cx + (px - cx) * 0.62, cy + (py - cy) * 0.62) for px, py in poly]
        d.polygon(inner, fill=(252, 246, 250))
        for a in np.linspace(0, 2 * math.pi, int(R / 4)):
            rr = 0.8 + r.uniform(-0.03, 0.03)
            x, y = R * rr * math.cos(a), ry * rr * math.sin(a)
            px, py = cx + x * math.cos(rot) - y * math.sin(rot), cy + x * math.sin(rot) + y * math.cos(rot)
            ang = math.atan2(py - cy, px - cx); L = r.uniform(7, 10); Wd = r.uniform(4, 5.5)
            pts = [(px + L * math.cos(ang) * math.cos(t) - Wd * math.sin(ang) * math.sin(t),
                    py + L * math.sin(ang) * math.cos(t) + Wd * math.cos(ang) * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 10)]
            pos = stain == "dab" and r.random() < 0.6
            d.polygon(pts, fill=(110, 60, 25) if pos else ((80, 85, 150) if stain == "dab" else nuc_d))
    # stromal nuclei + lymphocytes
    # red blood cells in vessels
    for _ in range(6):
        vx, vy = r.uniform(0, n), r.uniform(0, n)
        for _ in range(25):
            x, y = vx + r.gauss(0, 18), vy + r.gauss(0, 10)
            d.ellipse((x - 4, y - 4, x + 4, y + 4), fill=(225, 70, 90))
    im = im.filter(ImageFilter.GaussianBlur(0.9))
    a = np.asarray(im).astype(np.float32)
    a += np.random.default_rng(seed).normal(0, 3.5, a.shape)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")

def eyepiece(tex, size, t, zoom0=1.0, zoom1=1.25, D=10, pan=(0.0, 0.0), focus=0.0):
    """Circular microscope field of view with slow zoom/pan; focus>0 blurs (rack focus)."""
    z = zoom0 + (zoom1 - zoom0) * min(1, t / max(1, D))
    cw = tex.width / z; cx = tex.width / 2 + pan[0] * t * 20; cy = tex.height / 2 + pan[1] * t * 20
    crop = tex.crop((int(cx - cw / 2), int(cy - cw / 2), int(cx + cw / 2), int(cy + cw / 2))).resize((size, size), Image.BILINEAR)
    if focus > 0.05: crop = crop.filter(ImageFilter.GaussianBlur(focus * 8))
    m = Image.new("L", (size, size), 0); ImageDraw.Draw(m).ellipse((0, 0, size, size), fill=255)
    vg = np.linspace(-1, 1, size); rr = np.sqrt(vg[None, :] ** 2 + vg[:, None] ** 2)
    shade = np.clip(1.05 - 0.45 * rr ** 3, 0, 1)
    arr = np.asarray(crop).astype(np.float32); arr[..., :3] *= shade[..., None]
    out = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)); out.putalpha(m)
    ring = Image.new("RGBA", (size + 40, size + 40), (0, 0, 0, 0)); dr = ImageDraw.Draw(ring)
    dr.ellipse((0, 0, size + 39, size + 39), fill=(10, 12, 18, 255))
    ring.alpha_composite(out, (20, 20))
    return ring

def fullbleed(fr, tex, t, D, zoom0=1.0, zoom1=1.15, dark=0.55):
    """Fill the frame with a slowly zooming texture, darkened for text."""
    z = zoom0 + (zoom1 - zoom0) * min(1, t / max(1, D))
    ar = H / W; cw = tex.width / z; ch = min(tex.height, cw * ar)
    if ch == tex.height: cw = ch / ar
    cx, cy = tex.width / 2 + t * 6, tex.height / 2
    crop = tex.crop((int(cx - cw / 2), int(cy - ch / 2), int(cx + cw / 2), int(cy + ch / 2))).resize((W, H), Image.BILINEAR)
    fr.alpha_composite(crop)
    fr.alpha_composite(SHADE_FULL if dark else SHADE_LIGHT)
    fr.alpha_composite(L2.HW, (0, 40))

def _shade(top_a, bot_a, mid_a):
    y = np.linspace(0, 1, H)[:, None]
    a = np.where(y < 0.5, top_a + (mid_a - top_a) * (y / 0.5), mid_a + (bot_a - mid_a) * ((y - 0.5) / 0.5))
    arr = np.zeros((H, W, 4), np.uint8); arr[..., 0] = INK[0]; arr[..., 1] = INK[1]; arr[..., 2] = INK[2]
    arr[..., 3] = np.repeat((a * 255).astype(np.uint8), W, 1)
    return Image.fromarray(arr, "RGBA")
SHADE_FULL = _shade(0.92, 0.95, 0.45); SHADE_LIGHT = _shade(0.6, 0.7, 0.15)

# ---------------- ultrasound ----------------
def us_base(w=900, h=760, seed=11):
    r = np.random.default_rng(seed)
    speck = r.rayleigh(0.35, (h, w)).astype(np.float32)
    sp = Image.fromarray(np.clip(speck * 255, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.1))
    sp = sp.resize((w, h * 2)).filter(ImageFilter.BoxBlur(0)).resize((w, h))
    a = np.asarray(sp).astype(np.float32) / 255
    yy = np.linspace(0, 1, h)[:, None]; xx = np.linspace(-1, 1, w)[None, :]
    layers = 0.55 + 0.35 * np.exp(-((yy - 0.08) / 0.02) ** 2) + 0.25 * np.exp(-((yy - 0.3) / 0.03) ** 2) * (1 + 0.2 * np.sin(xx * 6))
    a = a * layers * (1 - 0.55 * yy)
    edge = 1 + 0.18 * (_noise(max(w, h), 60, seed + 3)[:h, :w] - 0.5)
    les = (((xx - 0.1) / 0.28) ** 2 + ((yy - 0.6) / 0.14) ** 2) * edge
    a = a * np.where(les < 1, 0.35, 1.0) + np.where(np.abs(les - 1) < 0.15, 0.18, 0) * a * 2
    a = a * (1 + 0.25 * (les < 1) * (yy > 0.74))
    img = Image.fromarray(np.clip(a * 255, 0, 255).astype(np.uint8)).convert("RGB")
    m = Image.new("L", (w, h), 0); dm = ImageDraw.Draw(m)
    dm.pieslice((-w * 0.5, -h * 0.95, w * 1.5, h * 1.0), 56, 124, fill=255)
    dm.rectangle((w * 0.22, 0, w * 0.78, 8), fill=255)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 255)); out.paste(img, (0, 0), m)
    d = ImageDraw.Draw(out)
    for k in range(0, 8):
        y = 30 + k * (h - 60) / 7; d.line((w - 40, y, w - 25, y), fill=(200, 200, 200), width=2)
        d.text((w - 50, y), str(k), font=font("Regular", 18), fill=(180, 180, 180), anchor="rm")
    d.text((20, 16), "L 12 MHz", font=font("Regular", 20), fill=(200, 200, 200))
    d.text((20, 42), "GAIN 54", font=font("Regular", 20), fill=(200, 200, 200))
    return out

def ultrasound(fr, x, y, t, base, prog):
    im = base.copy(); d = ImageDraw.Draw(im); w, h = im.size
    x0, y0 = w * 0.2, h * 0.05; x1, y1 = w * 0.55, h * 0.6
    p = max(0, min(1, prog))
    xe, ye = x0 + (x1 - x0) * p, y0 + (y1 - y0) * p
    d.line((x0, y0, xe, ye), fill=(250, 250, 250), width=5)
    if p > 0.95: d.ellipse((xe - 9, ye - 9, xe + 9, ye + 9), outline=(255, 230, 120), width=3)
    fr.alpha_composite(im, (int(x), int(y)))

# ---------------- lab objects (shaded) ----------------
def cyl_shade(w, h, col, hi=0.5):
    x = np.linspace(0, 1, w)
    prof = 0.55 + 0.45 * np.sin(np.pi * x) + 0.35 * np.exp(-((x - 0.28) / 0.05) ** 2)
    prof = prof * (0.85 + 0.15 * hi)
    arr = np.clip(np.array(col)[None, None, :] * prof[None, :, None], 0, 255).repeat(h, 0)
    return Image.fromarray(arr.astype(np.uint8)).convert("RGBA")

def jar_sprite():
    w, h = 360, 460; im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    body = cyl_shade(300, 330, (215, 228, 238)); m = Image.new("L", (300, 330), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, 299, 329), 40, fill=150); body.putalpha(m)
    liquid = cyl_shade(284, 250, (235, 232, 205)); ml = Image.new("L", (284, 250), 0)
    ImageDraw.Draw(ml).rounded_rectangle((0, 0, 283, 249), 34, fill=150); liquid.putalpha(ml)
    im.alpha_composite(body, (30, 110)); im.alpha_composite(liquid, (38, 182))
    d = ImageDraw.Draw(im)
    d.ellipse((150, 300, 215, 340), fill=(210, 150, 140)); d.ellipse((165, 306, 200, 326), fill=(225, 175, 160))
    lid = cyl_shade(320, 90, (245, 245, 248)); im.alpha_composite(lid, (20, 30))
    for k in range(20, 340, 12): d.line((k, 34, k, 116), fill=(215, 215, 222), width=2)
    d.rounded_rectangle((60, 196, 300, 270), 8, fill=(255, 255, 255, 235))
    d.text((180, 220), "10% FORMALIN", font=font("Bold", 26), fill=(200, 40, 40), anchor="mm")
    d.text((180, 250), "Biopsy specimen", font=font("Regular", 20), fill=(60, 60, 70), anchor="mm")
    return with_glow(im, (180, 210, 230), 14, 60)

def cassette_sprite(col=(46, 125, 200), wax=False, tissue=True):
    w, h = 420, 330; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 20, 410, 320), 18, fill=tuple(int(c * 0.7) for c in col))
    d.rounded_rectangle((0, 0, 400, 300), 18, fill=col)
    d.polygon([(0, 0), (90, 0), (90, 300), (0, 300)], fill=tuple(min(255, int(c * 1.15)) for c in col))
    d.text((45, 150), "S-1024", font=font("Bold", 24), fill=(20, 30, 50), anchor="mm")
    if wax:
        d.rounded_rectangle((110, 20, 385, 280), 14, fill=(236, 214, 160))
        d.rounded_rectangle((120, 30, 375, 270), 12, fill=(244, 226, 178))
        if tissue: d.ellipse((190, 105, 315, 190), fill=(205, 140, 120)); d.ellipse((215, 120, 285, 170), fill=(220, 165, 145))
    else:
        for yy in range(30, 280, 22):
            for xx in range(115, 380, 30): d.rounded_rectangle((xx, yy, xx + 22, yy + 10), 4, fill=tuple(int(c * 0.45) for c in col))
    d.line((92, 4, 396, 4), fill=(255, 255, 255, 120), width=3)
    return with_glow(im, (120, 170, 230), 12, 50)

def ribbon_sprite(t=0):
    w, h = 900, 300; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 120, w, h), 30, fill=(40, 90, 140, 200))
    for k in range(6):
        x = 40 + k * 140; y = 150 + 6 * math.sin(t * 2 + k)
        d.rounded_rectangle((x, y, x + 128, y + 90), 6, fill=(250, 240, 220, 170), outline=(255, 255, 255, 140), width=2)
        d.ellipse((x + 34, y + 22, x + 94, y + 66), fill=(225, 190, 175, 200))
    d.text((w / 2, 60), "Sections thinner than a hair", font=font("Medium", 34), fill=SOFT, anchor="mm")
    return im

def slide_sprite(tex, stain="H&E"):
    w, h = 820, 290; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((6, 10, w - 1, h - 1), 10, fill=(20, 30, 45, 150))
    d.rounded_rectangle((0, 0, w - 8, h - 12), 10, fill=(225, 240, 245, 120), outline=(240, 250, 255, 220), width=3)
    d.rectangle((2, 2, 220, h - 14), fill=(240, 240, 236))
    d.text((110, 90), "S-1024", font=font("Bold", 30), fill=(40, 40, 60), anchor="mm")
    d.text((110, 140), stain, font=font("Bold", 34), fill=(180, 40, 120) if stain == "H&E" else (130, 75, 25), anchor="mm")
    d.text((110, 190), "Histopath", font=font("Regular", 24), fill=(60, 60, 70), anchor="mm")
    patch = tex.resize((420, 420)).crop((0, 80, 420, 330)); mask = Image.new("L", patch.size, 0)
    md = ImageDraw.Draw(mask); md.polygon([(30, 60), (140, 10), (300, 30), (400, 110), (360, 220), (200, 240), (60, 200)], fill=235)
    mask = mask.filter(ImageFilter.GaussianBlur(6)); patch.putalpha(mask)
    im.alpha_composite(patch.resize((400, 240)), (300, 12))
    d.line((230, 6, w - 20, 6), fill=(255, 255, 255, 200), width=2)
    return with_glow(im, (200, 230, 255), 10, 40)

def needle_sprite(kind="core"):
    w, h = 900, 120; im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    shaft = cyl_shade(70, 640 if kind == "core" else 700, (200, 205, 215)).rotate(90, expand=True)
    sh = 70 if kind == "core" else 34
    shaft = shaft.resize((660, sh)); im.alpha_composite(shaft, (200, (h - sh) // 2))
    d = ImageDraw.Draw(im)
    d.polygon([(860, h / 2), (855 if kind != 'core' else 860, h / 2 - sh / 2), (860, h / 2 + sh / 2)], fill=(210, 215, 225))
    d.polygon([(860, h / 2 - sh / 2), (900, h / 2), (860, h / 2 + sh / 2)], fill=(220, 225, 235))
    hub = cyl_shade(200, 100, (240, 240, 245) if kind == "core" else (90, 160, 230)).rotate(90, expand=True).resize((200, 100))
    im.alpha_composite(hub, (0, 10))
    if kind == "core":
        d.rounded_rectangle((640, h / 2 - 12, 820, h / 2 + 14), 6, fill=(120, 60, 60))
        d.rounded_rectangle((650, h / 2 - 8, 810, h / 2 + 10), 5, fill=(205, 140, 130))
    return im

def report_sprite():
    w, h = 560, 720; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((14, 14, w, h), fill=(0, 0, 0, 90)); d.rectangle((0, 0, w - 14, h - 14), fill=(250, 250, 248))
    d.rectangle((0, 0, w - 14, 80), fill=(225, 235, 245))
    d.text((30, 40), "HISTOPATHOLOGY REPORT", font=font("Bold", 28), fill=(20, 50, 100), anchor="lm")
    r = random.Random(4)
    for k in range(16):
        y = 120 + k * 34; L = r.uniform(0.4, 0.95) * (w - 80)
        d.rounded_rectangle((30, y, 30 + L, y + 12), 6, fill=(200, 205, 215))
        if k in (5, 11): d.text((30, y - 4), "Microscopy:" if k == 5 else "Impression:", font=font("Bold", 22), fill=(40, 40, 60));
    d.rounded_rectangle((30, 650, 240, 664), 6, fill=(160, 170, 190))
    return im

# ---------------- film finish ----------------
def _grain(seed):
    a = np.random.default_rng(seed).normal(128, 30, (H // 2, W // 2)).astype(np.uint8)
    g = Image.fromarray(a).resize((W, H), Image.NEAREST).convert("L")
    out = Image.new("RGBA", (W, H), (128, 128, 128, 0)); out.putalpha(g.point(lambda v: int(abs(v - 128) * 0.18)))
    return out
GRAIN = [_grain(s) for s in range(4)]
def film(fn):
    def wrapped(fr, t, D):
        fn(fr, t, D); fr.alpha_composite(GRAIN[int(t * 30) % 4])
    return wrapped

# ---------------- IHC-specific textures ----------------
def _cells(n, seed, count):
    from scipy.spatial import Voronoi
    r = np.random.default_rng(seed)
    g = int(math.sqrt(count)); pts = []
    for i in range(g + 2):
        for j in range(g + 2):
            pts.append(((i - 1 + 0.5 * (j % 2) + r.uniform(-0.25, 0.25)) * n / g, (j - 1 + r.uniform(-0.25, 0.25)) * n / g))
    pts = np.array(pts); vor = Voronoi(pts); cells = []
    for i, reg in enumerate(vor.point_region):
        verts = vor.regions[reg]
        if -1 in verts or not verts: continue
        poly = [tuple(vor.vertices[v]) for v in verts]
        cx, cy = pts[i]
        if -60 < cx < n + 60 and -60 < cy < n + 60: cells.append(((cx, cy), poly))
    return cells

def her2_tex(level, n=700, seed=5):
    """HER2 IHC membrane staining: level 0,1,2,3."""
    r = random.Random(seed + level)
    im = Image.new("RGB", (n, n), (238, 234, 240)); d = ImageDraw.Draw(im)
    cells = _cells(n, seed, 70)
    col = {0: None, 1: (205, 170, 120), 2: (160, 100, 45), 3: (95, 50, 15)}[level]
    wid = {0: 0, 1: 2, 2: 4, 3: 7}[level]
    for (c, poly) in cells:
        d.polygon(poly, fill=(228, 222, 232))
    for (c, poly) in cells:
        if col and r.random() < (0.35 if level == 1 else 0.85 if level == 2 else 0.97):
            k = len(poly); start = r.randrange(k); span = k if level >= 2 else max(2, k // 2)
            seg = [poly[(start + j) % k] for j in range(span + 1)]
            d.line(seg, fill=col, width=wid, joint="curve")
        elif level == 0 and r.random() < 0.08:
            d.line(poly[:3], fill=(215, 195, 165), width=1)
    for (c, poly) in cells:
        x, y = c; a = r.uniform(0, math.pi); L = r.uniform(11, 15); Wd = r.uniform(8, 11)
        pts = [(x + L * math.cos(a) * math.cos(t) - Wd * math.sin(a) * math.sin(t), y + L * math.sin(a) * math.cos(t) + Wd * math.cos(a) * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 12)]
        d.polygon(pts, fill=(95, 100, 160))
    im = im.filter(ImageFilter.GaussianBlur(0.8))
    mod = (0.88 + 0.2 * _noise(n, 90, seed + 7) + 0.06 * _noise(n, 20, seed + 8))[..., None]
    a = np.asarray(im).astype(np.float32) * mod + np.random.default_rng(seed).normal(0, 3, (n, n, 3))
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")

def nuclear_tex(frac, n=900, seed=8):
    """ER/PR style nuclear staining: frac of nuclei brown."""
    r = random.Random(seed)
    im = Image.new("RGB", (n, n), (236, 232, 238)); d = ImageDraw.Draw(im)
    cells = _cells(n, seed, 170)
    for (c, poly) in cells: d.polygon(poly, fill=(226, 220, 230), outline=(214, 206, 220))
    for (c, poly) in cells:
        x, y = c; a = r.uniform(0, math.pi); L = r.uniform(12, 17); Wd = r.uniform(9, 13)
        pts = [(x + L * math.cos(a) * math.cos(t) - Wd * math.sin(a) * math.sin(t), y + L * math.sin(a) * math.cos(t) + Wd * math.cos(a) * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 12)]
        brown = r.random() < frac; s = r.uniform(0.8, 1.15)
        d.polygon(pts, fill=tuple(int(v * s) for v in ((120, 65, 20) if brown else (100, 105, 165))))
    im = im.filter(ImageFilter.GaussianBlur(0.8))
    mod = (0.86 + 0.22 * _noise(n, 90, seed + 7))[..., None]
    a = np.asarray(im).astype(np.float32) * mod + np.random.default_rng(seed).normal(0, 3, (n, n, 3))
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")

def antibody(d, x, y, s, ang, col=CYAN, a=255):
    """Y-shaped antibody, stem pointing along ang (radians) away from target."""
    ca, sa = math.cos(ang), math.sin(ang)
    def P(u, v): return (x + (u * ca - v * sa) * s, y + (u * sa + v * ca) * s)
    w = max(3, int(0.16 * s))
    d.line((P(0.0, 0), P(0.55, 0)), fill=(*col, a), width=w)
    for sg in (-1, 1):
        d.line((P(0.0, 0), P(-0.42, 0.38 * sg)), fill=(*col, a), width=w)
        e = P(-0.42, 0.38 * sg); rr = 0.11 * s; d.ellipse((e[0] - rr, e[1] - rr, e[0] + rr, e[1] + rr), fill=(*col, a))
    e = P(0.6, 0); rr = 0.1 * s; d.ellipse((e[0] - rr, e[1] - rr, e[0] + rr, e[1] + rr), fill=(255, 200, 80, a))

# ---------------- blood / molecular lab visuals ----------------
def rbc_smear(n=1400, seed=4, thal=True):
    """Peripheral blood smear: pale RBCs with central pallor; thal = microcytes, target cells, variable shape."""
    r = random.Random(seed)
    base = _mix((236, 224, 228), (226, 210, 218), _noise(n, 120, seed))
    im = Image.fromarray(base.astype(np.uint8)).convert("RGB"); d = ImageDraw.Draw(im)
    placed = []
    for _ in range(int(n * n / (700 if thal else 900))):
        x, y = r.uniform(0, n), r.uniform(0, n)
        rad = r.uniform(13, 19) if thal else r.uniform(20, 24)
        if any((x - a) ** 2 + (y - b) ** 2 < (rad + c) ** 2 * 0.72 for a, b, c in placed[-260:]): continue
        placed.append((x, y, rad))
        ex = 1 + (r.uniform(-0.25, 0.35) if thal else r.uniform(-0.06, 0.08)); a = r.uniform(0, math.pi)
        pts = [(x + rad * ex * math.cos(t) * math.cos(a) - rad * math.sin(t) * math.sin(a),
                y + rad * ex * math.cos(t) * math.sin(a) + rad * math.sin(t) * math.cos(a)) for t in np.linspace(0, 2 * math.pi, 22)]
        d.polygon(pts, fill=(214, 120, 140), outline=(190, 95, 120))
        pr = rad * (0.55 if thal else 0.4)
        d.ellipse((x - pr, y - pr, x + pr, y + pr), fill=(232, 190, 200))
        if thal and r.random() < 0.18:
            q = pr * 0.45; d.ellipse((x - q, y - q, x + q, y + q), fill=(212, 125, 145))
    for _ in range(3):
        x, y = r.uniform(80, n - 80), r.uniform(80, n - 80)
        d.ellipse((x - 30, y - 30, x + 30, y + 30), fill=(205, 175, 205))
        for k in range(3): d.ellipse((x - 18 + k * 10, y - 16 + 6 * k, x + 2 + k * 10, y + 4 + 6 * k), fill=(95, 55, 140))
    im = im.filter(ImageFilter.GaussianBlur(0.9))
    a = np.asarray(im).astype(np.float32) + np.random.default_rng(seed).normal(0, 3, (n, n, 3))
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")

def panel(fr, x, y, w, h, title=None, sub=None):
    lay, d = overlay(fr)
    d.rounded_rectangle((x, y, x + w, y + h), 22, fill=(6, 12, 24, 235), outline=(255, 255, 255, 50), width=2)
    if title: d.text((x + 26, y + 20), title, font=font("Bold", 30), fill=WHITE)
    if sub: d.text((x + w - 26, y + 24), sub, font=font("Regular", 24), fill=MUTED, anchor="ra")
    fr.alpha_composite(lay)

def hplc_chart(fr, x, y, w, h, t, tin, a2_high=True):
    """HPLC chromatogram with F, A0, A2 peaks; A2 window highlighted."""
    panel(fr, x, y, w, h, "HPLC (screening)")
    lay, d = overlay(fr); p = ease((t - tin) / 1.2)
    bx0, by = x + 40, y + h - 70; bw = w - 80; top = y + 80
    peaks = [(0.18, 0.08, "F"), (0.47, 1.0, "A0"), (0.74, 0.22 if a2_high else 0.1, "A2")]
    pts = []
    for i in range(301):
        u = i / 300; v = 0.02 * math.sin(u * 40)
        for c, hgt, _ in peaks: v += hgt * math.exp(-((u - c) / 0.022) ** 2)
        xx = bx0 + u * bw; yy = by - v * (by - top) * 0.92 * p
        pts.append((xx, yy))
    d.line(pts, fill=CYAN, width=3); d.line((bx0, by, bx0 + bw, by), fill=(255, 255, 255, 90), width=2)
    for c, hgt, lab in peaks:
        d.text((bx0 + c * bw, by + 26), lab, font=font("Bold", 26), fill=SOFT, anchor="mm")
    if a2_high and p > 0.9:
        cx = bx0 + 0.74 * bw; d.rounded_rectangle((cx - 40, top - 10, cx + 40, by), 12, outline=AMBER, width=3)
        d.text((cx, top - 30), "HbA2 high", font=font("Bold", 26), fill=AMBER, anchor="mm")
    fr.alpha_composite(lay)

BASECOL = {"A": (67, 200, 110), "C": (80, 150, 255), "G": (240, 240, 240), "T": (255, 90, 90)}
def sanger(fr, x, y, w, h, t, tin, seq="CCTTGGACCCAGAGGTTCTTTG", mut=None, scroll=True, title="DNA sequencing (Sanger)"):
    """Sanger chromatogram with base calls; mut=(index, other_base) draws a double peak (heterozygous)."""
    panel(fr, x, y, w, h, title)
    lay, d = overlay(fr); p = ease((t - tin) / 1.5)
    n = len(seq); bx0 = x + 30; bw = w - 60; by = y + h - 80; top = y + 90
    step = bw / n
    for b in "ACGT":
        pts = []
        for i in range(400):
            u = i / 399; xx = bx0 + u * bw
            if xx > bx0 + bw * p: break
            v = 0
            for k, ch in enumerate(seq):
                c = (k + 0.5) / n; amp = 0.0
                if ch == b: amp = 0.75 + 0.2 * math.sin(k * 2.3)
                if mut and k == mut[0]:
                    amp = 0.5 if (ch == b or mut[1] == b) else 0
                v += amp * math.exp(-((u - c) / (0.32 / n)) ** 2)
            pts.append((xx, by - v * (by - top)))
        if len(pts) > 1: d.line(pts, fill=BASECOL[b], width=3)
    for k, ch in enumerate(seq):
        xx = bx0 + (k + 0.5) * step
        if xx > bx0 + bw * p: break
        col = BASECOL[ch]
        if mut and k == mut[0]:
            d.rounded_rectangle((xx - step / 2, top - 6, xx + step / 2, by + 50), 8, outline=AMBER, width=3)
            d.text((xx, by + 30), "S", font=font("Bold", 28), fill=AMBER, anchor="mm")
        else:
            d.text((xx, by + 30), ch, font=font("Bold", 26), fill=col, anchor="mm")
    fr.alpha_composite(lay)

def gel(fr, x, y, w, h, t, tin, lanes):
    """Agarose gel photo: lanes = list of band position lists (0..1 from top); lane 0 is a ladder."""
    panel(fr, x, y, w, h, "ARMS-PCR gel")
    lay = Image.new("RGBA", (w - 40, h - 90), (10, 14, 22, 255)); d = ImageDraw.Draw(lay)
    p = ease((t - tin) / 1.2); n = len(lanes) + 1; lw = (w - 40) / (n + 1)
    ladder = [0.15, 0.25, 0.34, 0.42, 0.5, 0.58, 0.66, 0.74, 0.82]
    for li, bands in enumerate([ladder] + lanes):
        cx = lw * (li + 1)
        d.rectangle((cx - lw * 0.3, 8, cx + lw * 0.3, 20), fill=(40, 46, 60))
        for b in bands:
            yy = 30 + b * (h - 140) * p; inten = 150 if li == 0 else 235
            d.rounded_rectangle((cx - lw * 0.3, yy - 5, cx + lw * 0.3, yy + 5), 4, fill=(inten, 255, inten + 10 if inten < 245 else 255))
    glow = lay.filter(ImageFilter.GaussianBlur(5)); lay = Image.blend(lay, glow, 0.4)
    fr.alpha_composite(lay, (x + 20, y + 70))
