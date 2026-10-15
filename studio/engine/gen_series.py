"""Genetics Clinical Series: shared scene factories and lab-style visuals (realistic documentary style)."""
import math, random
from real_style import *

TOT = [16]
def dots(fr, n): fr.alpha_composite(chapter(n, TOT[0]), (0, 110))
def label(fr, text, x, y, col=SOFT, size=32, anchor="mm", weight="Medium"):
    lay, d = overlay(fr); d.text((x, y), text, font=font(weight, size), fill=col, anchor=anchor); fr.alpha_composite(lay)

TUBE = tube_sprite(); SEQ = "CCTTGGACCCAGAGGTTCTTTG"

# ---------------- lab visuals ----------------
CHR_LEN = [249, 242, 198, 190, 181, 171, 159, 145, 138, 134, 135, 133, 114, 107, 102, 90, 83, 80, 59, 64, 47, 51, 156, 57]
def karyogram(w=920, h=760, seed=4, extra21=False):
    """G-banded karyotype panel (grey banded chromosomes on white)."""
    r = random.Random(seed); im = Image.new("RGBA", (w, h), (246, 246, 242, 255)); d = ImageDraw.Draw(im)
    rows = [list(range(0, 5)), list(range(5, 12)), list(range(12, 18)), list(range(18, 24))]
    rowh = h / 4; scale = (rowh - 60) / 249
    for ri, row in enumerate(rows):
        n = len(row); cw = w / n
        for ci, k in enumerate(row):
            cx = cw * (ci + 0.5); base = rowh * (ri + 1) - 34
            L = CHR_LEN[k] * scale; copies = 2 if k < 22 else 1
            if extra21 and k == 20: copies = 3
            for c in range(copies):
                x = cx + (c - (copies - 1) / 2) * 22
                cen = base - L * (0.45 if k > 12 else 0.6)
                d.rounded_rectangle((x - 8, base - L, x + 8, base), 8, fill=(205, 205, 200))
                rr = random.Random(k * 7 + 1)
                y = base - L + 6
                while y < base - 8:
                    bh = rr.uniform(3, 9)
                    if rr.random() < 0.5: d.rectangle((x - 8, y, x + 8, y + bh), fill=(70, 70, 75))
                    y += bh + rr.uniform(3, 10)
                d.ellipse((x - 9, cen - 4, x + 9, cen + 4), fill=(246, 246, 242))
            lab = str(k + 1) if k < 22 else ("X" if k == 22 else "Y")
            d.text((cx, base + 18), lab, font=font("Medium", 20), fill=(60, 60, 70), anchor="mm")
    im = im.filter(ImageFilter.GaussianBlur(0.6))
    return im

def cma_plot(fr, x, y, w, h, t, tin, del_at=(0.55, 0.62), title="Chromosomal microarray (log2 ratio)"):
    panel(fr, x, y, w, h, title)
    lay, d = overlay(fr); r = random.Random(9); p = ease((t - tin) / 1.5)
    x0, x1, yc = x + 30, x + w - 30, y + h / 2 + 20; amp = (h - 140) / 4
    d.line((x0, yc, x1, yc), fill=(255, 255, 255, 60), width=2)
    for v in (1, -1):
        d.line((x0, yc - v * amp * 1.0, x1, yc - v * amp * 1.0), fill=(255, 255, 255, 25), width=1)
    for i in range(900):
        u = i / 900
        if u > p: break
        val = r.gauss(0, 0.18)
        if del_at[0] < u < del_at[1]: val += -1.0
        col = CORAL if del_at[0] < u < del_at[1] else (120, 200, 230)
        xx = x0 + u * (x1 - x0); yy = yc - val * amp
        d.ellipse((xx - 2, yy - 2, xx + 2, yy + 2), fill=(*col, 200))
    if p > del_at[1]:
        a, b = x0 + del_at[0] * (x1 - x0), x0 + del_at[1] * (x1 - x0)
        d.line((a, yc + amp, b, yc + amp), fill=CORAL, width=6)
        d.text(((a + b) / 2, yc + amp + 34), "Deletion", font=font("Bold", 28), fill=CORAL, anchor="mm")
    d.text((x0, y + h - 30), "chromosome position →".replace("→", ">"), font=font("Regular", 22), fill=MUTED)
    fr.alpha_composite(lay)

def gene_grid(fr, x, y, w, h, t, tin, highlight=None, n=600, title=None):
    """Exome view: many tiny gene tiles; highlight = set of indices lit (panel)."""
    if title: panel(fr, x, y, w, h, title)
    lay, d = overlay(fr); cols = 30; rows = n // cols; cw = (w - 40) / cols; ch = (h - (90 if title else 40)) / rows
    p = ease((t - tin) / 1.2); y0 = y + (75 if title else 20)
    for i in range(n):
        if i / n > p: break
        r_, c_ = divmod(i, cols); xx = x + 20 + c_ * cw; yy = y0 + r_ * ch
        lit = highlight is None or i in highlight
        d.rectangle((xx + 1, yy + 1, xx + cw - 2, yy + ch - 2), fill=(*(CYAN if lit else (60, 75, 100)), 230 if lit else 120))
    fr.alpha_composite(lay)

def flow(fr, t, D, steps, y0=360):
    """Vertical decision flow: list of (question, answer, colour)."""
    lay, d = overlay(fr)
    for i, (q, a, c) in enumerate(steps):
        tin = D * (0.1 + 0.16 * i)
        if t < tin: continue
        e = ease((t - tin) / 0.5); y = y0 + i * 250
        d.rounded_rectangle((X0, y, X0 + 440, y + 170), 22, fill=(255, 255, 255, int(22 * e)), outline=(255, 255, 255, int(60 * e)), width=2)
        for j, line in enumerate(wrap(q, font("Medium", 32), 400)):
            d.text((X0 + 26, y + 26 + j * 42), line, font=font("Medium", 32), fill=(*SOFT, int(255 * e)))
        d.line((X0 + 450, y + 85, X0 + 495, y + 85), fill=(*c, int(255 * e)), width=6)
        d.polygon([(X0 + 495, y + 72), (X0 + 517, y + 85), (X0 + 495, y + 98)], fill=(*c, int(255 * e)))
        d.rounded_rectangle((X0 + 525, y + 20, X0 + TW, y + 150), 22, fill=(*c, int(230 * e)))
        lines = wrap(a, font("Bold", 32), TW - 565); y1 = y + 85 - len(lines) * 20
        for j, line in enumerate(lines):
            d.text((X0 + 545, y1 + j * 40), line, font=font("Bold", 32), fill=(*INK, int(255 * e)))
    fr.alpha_composite(lay)

def five_tier(fr, y, t, tin):
    lay, d = overlay(fr)
    tiers = [("Pathogenic", CORAL), ("Likely pathogenic", (255, 150, 90)), ("VUS", AMBER), ("Likely benign", (120, 200, 180)), ("Benign", TEALG)]
    for i, (lab, c) in enumerate(tiers):
        tin_i = tin + i * 0.5
        if t < tin_i: continue
        e = ease((t - tin_i) / 0.5); yy = y + i * 120
        d.rounded_rectangle((X0, yy, X0 + TW * (0.35 + 0.65 * e), yy + 100), 24, fill=(*c, int(230 * e)))
        d.text((X0 + 30, yy + 50), lab, font=font("Bold", 42), fill=(*INK, int(255 * e)), anchor="lm")
    fr.alpha_composite(lay)

def paper_sprite(title_lines, journal):
    w, h = 620, 780; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((14, 14, w, h), fill=(0, 0, 0, 90)); d.rectangle((0, 0, w - 14, h - 14), fill=(251, 251, 248))
    d.text((36, 40), "CASE REPORT", font=font("Bold", 24), fill=(160, 40, 60))
    yy = 86
    for line in title_lines:
        d.text((36, yy), line, font=font("Bold", 30), fill=(20, 30, 60)); yy += 40
    d.text((36, yy + 10), journal, font=font("Medium", 22), fill=(80, 90, 110))
    r = random.Random(5)
    for k in range(14):
        y = yy + 70 + k * 30; L = r.uniform(0.55, 0.95) * (w - 90)
        d.rounded_rectangle((36, y, 36 + L, y + 11), 5, fill=(205, 210, 220))
    return im

# ---------------- scene factories ----------------
def s_title(n, kick, head, sub=None, visual=None, head_size=56):
    def f(fr, t, D):
        if n: dots(fr, n)
        show(fr, kicker(kick), 260, t, 0.1)
        show(fr, headline(head, head_size), 320, t, 0.3)
        if sub: show(fr, body(sub, 38, SOFT), 330 + 70 * len(wrap(head, font("Bold", head_size), TW)), t, 0.6)
        if visual: visual(fr, t, D)
    return f

def s_cards(n, kick, head, items, visual=None, y_items=None, size=35):
    def f(fr, t, D):
        dots(fr, n); show(fr, kicker(kick), 260, t, 0.1)
        y = 320
        if head: show(fr, headline(head, 54), 320, t, 0.3); y = 330 + 70 * len(wrap(head, font("Bold", 54), TW)) + 20
        if y_items: y = y_items
        for i, (txt, c) in enumerate(items):
            fire("pop", D * (0.1 + 0.12 * i)); show(fr, gcard(txt, c, i + 1, size), y + i * 150, t, D * (0.1 + 0.12 * i))
        if visual: visual(fr, t, D, y + len(items) * 150 + 30)
    return f
