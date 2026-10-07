import subprocess, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
import os
_HERE = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(_HERE, "..", "assets", "fonts", "Poppins-")
def font(w, s): return ImageFont.truetype(F + w + ".ttf", s)

BLUE = (13, 71, 161); DBLUE = (10, 45, 110); GREEN = (67, 160, 71)
ORANGE = (245, 124, 0); TEAL = (0, 150, 170); GREY = (55, 65, 80); RED = (211, 47, 47)
WHITE = (255, 255, 255)

# ---------- background ----------
def make_bg():
    y = np.linspace(0, 1, H)[:, None]
    top = np.array([236, 245, 255]); bot = np.array([255, 255, 255])
    arr = (top * (1 - y)[..., None] + bot * y[..., None]).repeat(W, 1)
    img = Image.fromarray(arr.astype(np.uint8))
    d = ImageDraw.Draw(img)
    # bottom waves
    pts = [(x, 1780 + 40 * math.sin(x / 170)) for x in range(0, W + 1, 10)]
    d.polygon(pts + [(W, H), (0, H)], fill=BLUE)
    pts2 = [(x, 1830 + 30 * math.sin(x / 140 + 2)) for x in range(0, W + 1, 10)]
    d.polygon(pts2 + [(W, H), (0, H)], fill=GREEN)
    return img
BG = make_bg()

logo = Image.open(os.path.join(_HERE, "..", "assets", "logo_full.png")).convert("RGBA")
# make white background transparent-ish via circular mask
mask = Image.new("L", logo.size, 0)
ImageDraw.Draw(mask).ellipse((0, 0, logo.size[0], logo.size[1]), fill=255)
logo.putalpha(mask)

def header_strip():
    im = Image.new("RGBA", (W, 170), (0, 0, 0, 0))
    small = logo.resize((120, 120), Image.LANCZOS)
    im.paste(small, (60, 25), small)
    d = ImageDraw.Draw(im)
    d.text((200, 38), "Health Test", font=font("Bold", 44), fill=BLUE)
    d.text((200, 90), "Simplified", font=font("Medium", 34), fill=GREY)
    return im
HEADER = header_strip()

# ---------- element builders ----------
def wrap(text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if fnt.getlength(t) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur); return lines

def text_el(text, size=60, weight="Bold", color=DBLUE, maxw=940, align="center", spacing=1.25):
    fnt = font(weight, size)
    lines = wrap(text, fnt, maxw)
    lh = int(size * spacing)
    im = Image.new("RGBA", (W, lh * len(lines) + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, l in enumerate(lines):
        x = (W - fnt.getlength(l)) / 2 if align == "center" else 70
        d.text((x, i * lh), l, font=fnt, fill=color)
    return im

def pill(text, bg=BLUE, fg=WHITE, size=46):
    fnt = font("Bold", size)
    tw = fnt.getlength(text)
    im = Image.new("RGBA", (W, size + 60), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x0 = (W - tw) / 2 - 45
    d.rounded_rectangle((x0, 0, x0 + tw + 90, size + 50), radius=(size + 50) // 2, fill=bg)
    d.text((x0 + 45, 15), text, font=fnt, fill=fg)
    return im

def card(text, icon_color=GREEN, mark="✓", size=44, width=940):
    fnt = font("Medium", size)
    lines = wrap(text, fnt, width - 170)
    lh = int(size * 1.3)
    h = lh * len(lines) + 50
    im = Image.new("RGBA", (W, h + 12), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    x0 = (W - width) // 2
    ImageDraw.Draw(sh).rounded_rectangle((x0, 8, x0 + width, h + 8), 28, fill=(0, 40, 90, 40))
    im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(6)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((x0, 0, x0 + width, h), 28, fill=WHITE)
    cy = h // 2
    d.ellipse((x0 + 30, cy - 36, x0 + 102, cy + 36), fill=icon_color)
    mf = ImageFont.truetype(os.path.join(_HERE, "..", "assets", "fonts", "DejaVuSans-Bold.ttf"), 42)
    mw = mf.getlength(mark)
    d.text((x0 + 66 - mw / 2, cy - 26), mark, font=mf, fill=WHITE)
    for i, l in enumerate(lines):
        d.text((x0 + 130, 25 + i * lh), l, font=fnt, fill=GREY)
    return im

def table_el():
    rows = [("", "Normal", "Pre-\ndiabetes", "Diabetes"),
            ("HbA1c", "< 5.7%", "5.7–6.4%", "≥ 6.5%"),
            ("Fasting\nsugar", "< 100", "100–125", "≥ 126")]
    colw = [250, 230, 230, 230]; rh = [130, 140, 140]
    tw = sum(colw); x0 = (W - tw) // 2
    im = Image.new("RGBA", (W, sum(rh) + 10), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((x0, 0, x0 + tw, sum(rh)), 26, fill=WHITE, outline=(200, 215, 235), width=3)
    hdr_cols = [None, GREEN, ORANGE, RED]
    y = 0
    for r, row in enumerate(rows):
        x = x0
        for c, cell in enumerate(row):
            if r == 0 and c > 0:
                d.rounded_rectangle((x + 8, 8, x + colw[c] - 8, rh[0] - 8), 18, fill=hdr_cols[c])
                col, fnt = WHITE, font("Bold", 34)
            elif c == 0:
                col, fnt = DBLUE, font("Bold", 36)
            else:
                col, fnt = hdr_cols[c], font("Bold", 42)
            ls = cell.split("\n"); lh = fnt.size * 1.15
            ty = y + (rh[r] - lh * len(ls)) / 2
            for i, l in enumerate(ls):
                d.text((x + (colw[c] - fnt.getlength(l)) / 2, ty + i * lh), l, font=fnt, fill=col)
            x += colw[c]
        y += rh[r]
        if r < 2: d.line((x0 + 20, y, x0 + tw - 20, y), fill=(220, 228, 240), width=2)
    return im

def photo_vs_video():
    im = Image.new("RGBA", (W, 520), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # photo
    d.rounded_rectangle((90, 20, 490, 380), 30, fill=WHITE, outline=ORANGE, width=8)
    d.rectangle((150, 90, 430, 290), fill=(255, 236, 214))
    d.ellipse((250, 140, 330, 220), fill=ORANGE)
    d.text((290 - font("Bold", 40).getlength("Today") / 2, 395), "Today", font=font("Bold", 40), fill=ORANGE)
    d.text((290 - font("Medium", 32).getlength("Sugar test = photo") / 2, 450), "Sugar test = photo", font=font("Medium", 32), fill=GREY)
    # video
    d.rounded_rectangle((590, 20, 990, 380), 30, fill=WHITE, outline=GREEN, width=8)
    for i in range(5):
        d.rectangle((620 + i * 72, 40, 650 + i * 72, 60), fill=GREEN)
        d.rectangle((620 + i * 72, 340, 650 + i * 72, 360), fill=GREEN)
    d.polygon([(740, 140), (740, 260), (850, 200)], fill=GREEN)
    d.text((790 - font("Bold", 40).getlength("3 months") / 2, 395), "3 months", font=font("Bold", 40), fill=GREEN)
    d.text((790 - font("Medium", 32).getlength("HbA1c = video") / 2, 450), "HbA1c = video", font=font("Medium", 32), fill=GREY)
    return im

def organs():
    items = [("Kidneys", BLUE), ("Eyes", TEAL), ("Nerves", ORANGE), ("Heart", RED)]
    im = Image.new("RGBA", (W, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    fnt = font("Bold", 34)
    for i, (t, c) in enumerate(items):
        cx = 150 + i * 260
        d.ellipse((cx - 85, 0, cx + 85, 170), fill=c)
        d.text((cx - fnt.getlength(t) / 2, 62), t, font=fnt, fill=WHITE)
    return im

def big_logo():
    s = logo.resize((560, 560), Image.LANCZOS)
    im = Image.new("RGBA", (W, 580), (0, 0, 0, 0)); im.paste(s, ((W - 560) // 2, 0), s)
    return im

