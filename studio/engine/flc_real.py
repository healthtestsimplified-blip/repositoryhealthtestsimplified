"""Serum free light chain assay (kappa, lambda, ratio), realistic documentary style."""
import math, sys, random
from cbc_cartoon import run
from real_style import *
from hts_close import close_scene

TOPIC = "FREE LIGHT CHAINS  •  KAPPA / LAMBDA"
GK = ImageFont.truetype(F.replace("Poppins-", "DejaVuSans-Bold.ttf"), 40)
def gk(size): return ImageFont.truetype(F.replace("Poppins-", "DejaVuSans-Bold.ttf"), size)
HEAVY = (90, 170, 255); KAP = AMBER; LAM = (190, 150, 255)
TUBE = tube_sprite((200, 40, 40), "SERUM"); REPORT = report_sprite()

def dots(fr, n): fr.alpha_composite(chapter(n, 9), (0, 110))
def label(fr, text, x, y, col=SOFT, size=32, anchor="mm", weight="Medium", f=None):
    lay, d = overlay(fr); d.text((x, y), text, font=f or font(weight, size), fill=col, anchor=anchor); fr.alpha_composite(lay)

def igg(d, cx, cy, s, ang, lc, a=255):
    """Antibody: 2 heavy chains (Y) + 2 light chains on the outer arms."""
    ca, sa = math.cos(ang), math.sin(ang)
    def P(u, v): return (cx + (u * ca - v * sa) * s, cy + (u * sa + v * ca) * s)
    w = max(4, int(0.11 * s))
    for sg in (-1, 1):
        d.line((P(0.9, 0.05 * sg), P(0.0, 0.05 * sg)), fill=(*HEAVY, a), width=w)
        d.line((P(0.0, 0.05 * sg), P(-0.75, 0.62 * sg)), fill=(*HEAVY, a), width=w)
        d.line((P(0.05, 0.2 * sg), P(-0.62, 0.8 * sg)), fill=(*lc, a), width=w)
    for sg in (-1, 1):
        e = P(-0.75, 0.62 * sg); r = 0.07 * s; d.ellipse((e[0] - r, e[1] - r, e[0] + r, e[1] + r), fill=(*HEAVY, a))

def free_lc(d, x, y, s, ang, lc, a=255):
    ca, sa = math.cos(ang), math.sin(ang); w = max(4, int(0.11 * s))
    d.line((x, y, x + 0.7 * s * ca, y + 0.7 * s * sa), fill=(*lc, a), width=w)
    r = 0.06 * s; d.ellipse((x - r, y - r, x + r, y + r), fill=(*lc, a))

def plasma_sprite(size=420):
    k = 2; S = size * k; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im); r = random.Random(3)
    d.ellipse((S * 0.06, S * 0.14, S * 0.94, S * 0.86), fill=(70, 80, 170))
    d.ellipse((S * 0.12, S * 0.2, S * 0.88, S * 0.8), fill=(85, 95, 185))
    d.ellipse((S * 0.42, S * 0.36, S * 0.6, S * 0.6), fill=(200, 205, 235))
    nx, ny, nr = S * 0.3, S * 0.5, S * 0.2
    d.ellipse((nx - nr, ny - nr, nx + nr, ny + nr), fill=(70, 30, 110))
    for i in range(14):
        a = i / 14 * 2 * math.pi; rr = nr * 0.65
        x, y = nx + rr * math.cos(a), ny + rr * math.sin(a); q = nr * 0.17
        d.ellipse((x - q, y - q, x + q, y + q), fill=(40, 10, 70))
    d.ellipse((nx - nr * 0.2, ny - nr * 0.2, nx + nr * 0.2, ny + nr * 0.2), fill=(40, 10, 70))
    im = im.filter(ImageFilter.GaussianBlur(3)).resize((size, size), Image.LANCZOS)
    return with_glow(im, (120, 130, 255), 20, 90)
PLASMA = plasma_sprite()

def balance(fr, cx, cy, tilt, kv="κ", lv="λ", a=1.0):
    lay, d = overlay(fr); A = int(255 * a)
    d.polygon([(cx, cy), (cx - 50, cy + 160), (cx + 50, cy + 160)], fill=(150, 165, 190, A))
    d.rectangle((cx - 110, cy + 160, cx + 110, cy + 180), fill=(150, 165, 190, A))
    L = 330; dx, dy = L * math.cos(tilt), L * math.sin(tilt)
    d.line((cx - dx, cy - dy, cx + dx, cy + dy), fill=(220, 230, 245, A), width=10)
    d.ellipse((cx - 16, cy - 16, cx + 16, cy + 16), fill=(220, 230, 245, A))
    for sg, lab, col in ((-1, kv, KAP), (1, lv, LAM)):
        px, py = cx + sg * dx, cy + sg * dy
        d.line((px, py, px - 70, py + 120), fill=(200, 210, 230, A), width=3); d.line((px, py, px + 70, py + 120), fill=(200, 210, 230, A), width=3)
        d.chord((px - 110, py + 70, px + 110, py + 170), 0, 180, fill=(*col, A))
        d.text((px, py + 220), lab, font=gk(64), fill=(*col, A), anchor="mm")
    fr.alpha_composite(lay)

def ratio_bar(fr, y, val, lo=0.26, hi=1.65, t=0, tin=0, title="κ / λ ratio", renal=None):
    lay, d = overlay(fr)
    x0, x1 = X0 + 20, X0 + TW - 20
    def X(v): return x0 + (math.log10(v) + 1) / 2.2 * (x1 - x0)
    d.text((X0, y - 70), title, font=gk(36), fill=WHITE)
    d.rounded_rectangle((x0, y, x1, y + 40), 20, fill=(255, 255, 255, 30))
    if renal: d.rounded_rectangle((X(renal[0]), y - 6, X(renal[1]), y + 46), 20, outline=LAV, width=4)
    d.rounded_rectangle((X(lo), y, X(hi), y + 40), 20, fill=(*TEALG, 200))
    for v in (0.1, 0.26, 1, 1.65, 10):
        d.text((X(v), y + 70), str(v), font=font("Medium", 26), fill=MUTED, anchor="mm")
    if val:
        p = ease((t - tin) / 1.0); v = 10 ** (math.log10(0.8) + (math.log10(val) - math.log10(0.8)) * p)
        inside = lo <= v <= hi; c = TEALG if inside else CORAL
        d.polygon([(X(v), y - 8), (X(v) - 18, y - 38), (X(v) + 18, y - 38)], fill=c)
        d.text((X(v), y - 56), f"{v:.2f}", font=font("Bold", 30), fill=c, anchor="mm")
    fr.alpha_composite(lay)

def _kidney_sprite(s=150):
    k = 2; S = int(s * 2.8 * k); im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx = cy = S / 2; R = s * k
    for i in range(10):
        c = (200 - i * 9, 85 - i * 4, 95 - i * 4, 255); g = i * 4 * k
        d.ellipse((cx - R + g, cy - R * 1.35 + g, cx + R - g, cy + R * 1.35 - g), fill=c)
    m = Image.new("L", (S, S), 255); dm = ImageDraw.Draw(m)
    dm.ellipse((cx + R * 0.45, cy - R * 0.45, cx + R * 1.35, cy + R * 0.45), fill=0)
    m = m.filter(ImageFilter.GaussianBlur(6)); a = Image.new("L", (S, S), 0); a.paste(im.getchannel("A"), (0, 0), m); im.putalpha(a)
    d = ImageDraw.Draw(im); d.line((cx + R * 0.55, cy, cx + R * 1.25, cy + R * 1.0), fill=(225, 205, 130, 255), width=14 * k)
    d.ellipse((cx - R * 0.55, cy - R * 0.2, cx - R * 0.1, cy + R * 0.25), fill=(225, 120, 120, 120))
    return with_glow(im.resize((S // k, S // k), Image.LANCZOS), (220, 90, 90), 16, 80)
KIDNEY = _kidney_sprite()
def kidney(fr, cx, cy, s, t):
    put(fr, KIDNEY, cx, cy, 1.0 + 0.02 * math.sin(t))

# ---------------- scenes ----------------
def f_hook(fr, t, D):
    lay, d = overlay(fr); r = random.Random(1)
    for k in range(16):
        x = r.uniform(80, 1000) + 30 * math.sin(t * 0.6 + k); y = r.uniform(820, 1560) + 25 * math.cos(t * 0.5 + k)
        igg(d, x, y, r.uniform(45, 85), r.uniform(0, 6.28) + t * 0.2 * (1 if k % 2 else -1), KAP if k % 2 else LAM, 170)
    for k in range(14):
        x = r.uniform(60, 1020) + 20 * math.sin(t + k); y = r.uniform(780, 1600)
        free_lc(d, x, y, r.uniform(40, 60), r.uniform(0, 6.28) + t * 0.5, KAP if k % 3 else LAM, 200)
    fr.alpha_composite(lay.filter(ImageFilter.GaussianBlur(0.6)))
    show(fr, kicker("Serum free light chains", CYAN), 330, t, 0.1)
    type_on(fr, "Kappa? Lambda? Ratio?", 410, t, 0.4, 76)
    if t > D * 0.35: type_on(fr, "What does it mean?", 600, t, D * 0.35, 72, AMBER)
    show(fr, callout("Free light chain test, explained", CYAN, 40), 1660, t, D * 0.6); fire("whoosh", D * 0.6)

def f_struct(fr, t, D):
    dots(fr, 1)
    show(fr, kicker("An antibody"), 260, t, 0.1)
    show(fr, headline("2 heavy chains + 2 light chains", 60), 320, t, 0.3)
    lay, d = overlay(fr); e = ease((t - 0.4) / 0.8)
    igg(d, 540, 850, 420 * (0.85 + 0.15 * e), math.pi / 2 + 0.03 * math.sin(t), KAP, int(255 * e))
    fr.alpha_composite(with_glow(lay, (120, 170, 255), 12, 60) if e > 0.5 else lay)
    if t > D * 0.25: label(fr, "Blue = heavy chains", 320, 1320, HEAVY, 34, weight="Bold")
    if t > D * 0.4: label(fr, "Yellow = light chains", 770, 1320, KAP, 34, weight="Bold")
    if t > D * 0.55:
        lay, d = overlay(fr)
        d.rounded_rectangle((X0, 1420, X0 + TW, 1560), 26, fill=(255, 255, 255, 20), outline=(255, 255, 255, 46), width=2)
        d.text((X0 + TW * 0.25, 1490), "κ  kappa", font=gk(48), fill=KAP, anchor="mm")
        d.text((X0 + TW * 0.75, 1490), "λ  lambda", font=gk(48), fill=LAM, anchor="mm")
        fr.alpha_composite(lay); fire("pop", D * 0.55)
    label(fr, "Light chains are of 2 types:", 540, 1390, SOFT, 32) if t > D * 0.55 else None

def f_free(fr, t, D):
    dots(fr, 2)
    show(fr, kicker("Free light chains"), 260, t, 0.1)
    show(fr, headline("Plasma cells make a few extra light chains", 56), 320, t, 0.3)
    put(fr, PLASMA, 300, 760, 1.0 + 0.02 * math.sin(t), ease((t - 0.4) / 0.6))
    label(fr, "Plasma cell", 300, 1000, SOFT, 30)
    lay, d = overlay(fr)
    for k in range(10):
        ph = ((t * 0.25 + k / 10) % 1)
        if t < 0.8: break
        x = 470 + ph * 520; y = 600 + (k % 5) * 70 + 20 * math.sin(t + k)
        if k % 3 == 0: igg(d, x, y, 55, t + k, KAP if k % 2 else LAM, int(220 * (1 - ph * 0.5)))
        else: free_lc(d, x, y, 50, t * 1.5 + k, KAP if k % 2 else LAM, int(230 * (1 - ph * 0.5)))
    fr.alpha_composite(lay)
    show(fr, gcard("Unattached light chains float freely in the blood = FREE light chains", CYAN, None, 35), 1090, t, D * 0.4)
    show(fr, gcard("The test measures free kappa AND free lambda", AMBER, None, 38), 1250, t, D * 0.65)
    fire("pop", D * 0.4); fire("pop", D * 0.65)

def f_ratio(fr, t, D):
    dots(fr, 3)
    show(fr, kicker("The key: the ratio"), 260, t, 0.1)
    lay, d = overlay(fr); e = ease((t - 0.3) / 0.6)
    d.text((540, 380), "κ ÷ λ", font=gk(110), fill=(255, 255, 255, int(255 * e)), anchor="mm"); fr.alpha_composite(lay)
    balance(fr, 540, 600, 0.03 * math.sin(t * 1.5), a=ease((t - 0.5) / 0.6))
    if t > D * 0.35: ratio_bar(fr, 1180, 0.8, t=t, tin=D * 0.35)
    show(fr, body("A common reference range: 0.26 to 1.65. Ranges differ by lab and machine.", 36, SOFT), 1330, t, D * 0.55)

def f_abn(fr, t, D):
    dots(fr, 4)
    show(fr, kicker("When the balance breaks"), 260, t, 0.1)
    show(fr, headline("One clone of plasma cells makes ONE type in excess", 54), 320, t, 0.3)
    tilt = -0.32 * ease((t - D * 0.25) / 0.8)
    balance(fr, 540, 640, tilt, a=1.0)
    if t > D * 0.25: fire("boom", D * 0.25)
    if t > D * 0.45: ratio_bar(fr, 1240, 6.5, t=t, tin=D * 0.45)
    show(fr, gcard("Kappa high = ratio goes UP;  lambda high = ratio goes DOWN", CORAL, None, 36), 1400, t, D * 0.65)

def f_why(fr, t, D):
    dots(fr, 5)
    show(fr, kicker("Why it matters"), 260, t, 0.1)
    lay, d = overlay(fr)
    if t > 0.4:
        e = ease((t - 0.4) / 0.6)
        d.text((X0, 330), "About 15%", font=font("Bold", 110), fill=(*AMBER, int(255 * e)))
        d.text((X0, 470), "of multiple myeloma makes ONLY light chains", font=font("Regular", 38), fill=(*SOFT, int(255 * e)))
    fr.alpha_composite(lay)
    if t > D * 0.25:
        densito(fr, X0, 560, TW, 330, spep_profile("normal"), t, D * 0.25, "SPEP can look normal", col=CYAN, shade=False)
    if t > D * 0.45:
        lay, d = overlay(fr); e = ease((t - D * 0.45) / 0.8)
        d.text((X0, 950), "Free light chains", font=font("Bold", 36), fill=WHITE)
        for i, (lab, v, c) in enumerate((("κ", 0.95, KAP), ("λ", 0.18, LAM))):
            y = 1020 + i * 80
            d.text((X0, y + 20), lab, font=gk(44), fill=c, anchor="lm")
            d.rounded_rectangle((X0 + 70, y, X0 + TW, y + 40), 20, fill=(255, 255, 255, 25))
            d.rounded_rectangle((X0 + 70, y, X0 + 70 + (TW - 70) * v * e, y + 40), 20, fill=c)
        fr.alpha_composite(lay); fire("ding", D * 0.45)
    show(fr, gcard("Doctors often order it with SPEP and immunofixation", CYAN, None, 38), 1230, t, D * 0.7)
    show(fr, source_tag("Parkview Health laboratory test directory"), 1380, t, D * 0.75)

def f_kidney(fr, t, D):
    dots(fr, 6)
    show(fr, kicker("Kidneys matter"), 260, t, 0.1)
    show(fr, headline("Free light chains are cleared by the kidneys", 56), 320, t, 0.3)
    kidney(fr, 300, 720, 150, t)
    lay, d = overlay(fr)
    for k in range(int(min(18, max(0, t - 0.5) * 3))):
        x = 620 + (k % 6) * 60; y = 600 + (k // 6) * 70
        free_lc(d, x, y, 45, 0.6 + k, KAP if k % 2 else LAM, 230)
    fr.alpha_composite(lay)
    show(fr, gcard("Weak kidneys: both kappa and lambda can rise; ratio can go up a little", AMBER, None, 35), 1000, t, D * 0.35)
    if t > D * 0.55: ratio_bar(fr, 1300, None, renal=(0.37, 3.1), title="Kidney-disease range (one study): 0.37 to 3.1")
    show(fr, source_tag("Hutchison et al., BMC Nephrology 2008"), 1420, t, D * 0.65)

def f_uses(fr, t, D):
    dots(fr, 7)
    show(fr, kicker("What it helps with"), 260, t, 0.1)
    items = [("Detecting myeloma, especially light-chain types", CYAN), ("Monitoring during treatment", TEALG), ("Judging risk in MGUS", AMBER)]
    for i, (txt, c) in enumerate(items):
        fire("pop", D * (0.1 + 0.15 * i)); show(fr, gcard(txt, c, i + 1, 38), 360 + i * 160, t, D * (0.1 + 0.15 * i))
    show(fr, callout("A very unbalanced ratio is an important signal for the doctor", CORAL, 38), 900, t, D * 0.6)
    show(fr, body("e.g. IMWG: involved/uninvolved ratio of 100 or more (with involved FLC of 100 mg/L or more) is one myeloma criterion.", 30, MUTED), 1080, t, D * 0.7)
    put(fr, PLASMA, 540, 1430, 0.7, ease((t - D * 0.3) / 0.6))

def f_prep(fr, t, D):
    dots(fr, 8)
    show(fr, kicker("Preparation & report"), 260, t, 0.1)
    show(fr, headline("Just one blood sample", 64), 320, t, 0.3)
    put(fr, TUBE, 220, 720, 0.8, ease((t - 0.4) / 0.5))
    p = ease((t - 0.6) / 0.6)
    if p > 0:
        im = REPORT.copy(); d = ImageDraw.Draw(im)
        d.rectangle((0, 0, 545, 80), fill=(225, 235, 245)); d.text((30, 40), "LAB REPORT", font=font("Bold", 28), fill=(20, 50, 100), anchor="lm")
        d.rectangle((24, 96, 520, 400), fill=(250, 250, 248))
        d.text((30, 110), "Free light chains (example format)", font=font("Bold", 22), fill=(20, 50, 100))
        for i, (m, u) in enumerate((("Free kappa", "mg/L"), ("Free lambda", "mg/L"), ("Kappa/lambda ratio", ""))):
            yy = 170 + i * 60; d.text((30, yy), m, font=font("Medium", 24), fill=(40, 40, 60)); d.text((330, yy), u, font=font("Regular", 22), fill=(110, 110, 130))
        put(fr, im, 700, 760, 0.75, p)
    show(fr, gcard("Usually no fasting; follow your lab's instructions", CYAN, 1, 38), 1080, t, D * 0.35)
    show(fr, gcard("Don't judge from one report; the doctor reads it with other tests", TEALG, 2, 36), 1230, t, D * 0.6)

SC = [(film(f_hook), "doc"), (film(f_struct), "doc"), (film(f_free), "doc"), (film(f_ratio), "doc"), (film(f_abn), "doc"),
      (film(f_why), "doc"), (film(f_kidney), "doc"), (film(f_uses), "doc"), (film(f_prep), "doc"),
      (close_scene("Seen a kappa/lambda ratio before?", TOPIC), "docl")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        D = [12, 14, 18, 18, 16, 22, 18, 18, 18, 33]
        ims = []
        for si in range(10):
            fn, bg = SC[si]; d = D[si]; p = 0.95; NOW.update(t=d * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d * p, d); ims.append(fr.convert("RGB").resize((360, 640)))
        s = Image.new("RGB", (360 * 5, 640 * 2), "white")
        for i, im in enumerate(ims): s.paste(im, ((i % 5) * 360, (i // 5) * 640))
        s.save("sheet.png")
    else: run(SC, "/tmp/flc_", "Free_Light_Chain_Test_Hindi.mp4")
