"""Purple & pink theme for the daily series "Aaj Ka Health Gyan" (short Hindi videos, under 2 minutes).
Import this instead of doc_style; registers BASES["pp"] (dark scenes) and BASES["ppl"] (light closing card)."""
import numpy as np
from real_style import *
from doc_style import *
import doc_style as DS
import lft_cartoon2 as L2

PURPLE = (124, 58, 237); PINK = (236, 72, 153); MAGENTA = (217, 70, 239); ROSE = (251, 113, 133)
LILAC = (196, 181, 253); MINT = (52, 211, 153); SUN = (251, 191, 36); SKY = (56, 189, 248)
DEEP = (36, 12, 64); DEEP2 = (76, 18, 96)

def _pp_bg():
    y = np.linspace(0, 1, H)[:, None, None]; x = np.linspace(-1, 1, W)[None, :, None]
    base = np.array(DEEP) * (1 - y) + np.array(DEEP2) * y
    glow1 = np.exp(-(((x + 0.6) ** 2) / 0.35 + ((y - 0.18) ** 2) / 0.05))
    glow2 = np.exp(-(((x - 0.7) ** 2) / 0.4 + ((y - 0.82) ** 2) / 0.06))
    arr = base + glow1 * np.array([110, 30, 150]) * 0.6 + glow2 * np.array([170, 40, 110]) * 0.5
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    img = Image.fromarray(np.broadcast_to(arr, (H, W, 3)).copy()).convert("RGBA")
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for yy in range(220, H, 56):
        for xx in range(28, W, 56): d.ellipse((xx - 1.5, yy - 1.5, xx + 1.5, yy + 1.5), fill=(255, 210, 240, 18))
    img.alpha_composite(lay)
    b = img.copy(); b.alpha_composite(L2.HW, (0, 40)); return b

def _ppl_bg():
    y = np.linspace(0, 1, H)[:, None]
    arr = (np.array([253, 242, 250]) * (1 - y)[..., None] + np.array([240, 230, 252]) * y[..., None]).repeat(W, 1)
    img = Image.fromarray(arr.astype(np.uint8)).convert("RGBA")
    b = img.copy(); b.alpha_composite(HEADER, (0, 40)); return b

BASES["pp"] = _pp_bg(); BASES["ppl"] = _ppl_bg()

SERIES = "AAJ KA HEALTH GYAN"

def series_pill(n):
    return pill(f"{SERIES}  •  DAY {n}", PINK, size=30)

def fact_card(text, accent=PINK, idx=None, size=40):
    return gcard(text, accent, idx, size)

def big_number(fr, val, unit, y, t, tin, col=SUN, size=170):
    lay, d = overlay(fr); e = ease((t - tin) / 0.6); a = int(255 * e)
    d.text((W / 2, y), val, font=font("Bold", size), fill=(*col, a), anchor="mm")
    d.text((W / 2, y + size * 0.72), unit, font=font("Medium", 40), fill=(*SOFT, a), anchor="mm")
    fr.alpha_composite(lay)

def icon_row(fr, y, t, tin, items):
    """Row of round icons with labels: items = [(emoji-free short label, colour)]."""
    lay, d = overlay(fr); n = len(items); gap = TW / n
    for i, (lab, c) in enumerate(items):
        e = ease((t - tin - 0.25 * i) / 0.4); a = int(255 * e); cx = X0 + gap * (i + 0.5)
        d.ellipse((cx - 85, y - 85, cx + 85, y + 85), fill=(*c, int(60 * e)), outline=(*c, a), width=5)
        for j, line in enumerate(wrap(lab, font("Bold", 28), 160)):
            d.text((cx, y - 14 * (len(wrap(lab, font("Bold", 28), 160)) - 1) + j * 32), line, font=font("Bold", 28), fill=(*WHITE, a), anchor="mm")
    fr.alpha_composite(lay)

# ---------------- closing card (all daily videos) ----------------
IG = (225, 48, 108); FB = (24, 119, 242); YT = (230, 0, 0)

def social3(fr, y, t, tin):
    if t < tin: return
    a = min(1, (t - tin) / 0.3)
    im = Image.new("RGBA", (W, 110), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, (col, lab) in enumerate(((IG, "Instagram"), (FB, "Facebook"), (YT, "YouTube"))):
        x0 = 50 + i * 330
        d.rounded_rectangle((x0, 5, x0 + 310, 100), 48, fill=col)
        d.text((x0 + 155, 53), lab, font=font("Bold", 36), fill=WHITE, anchor="mm")
    if a < 1: im.putalpha(im.getchannel("A").point(lambda v: int(v * a)))
    fr.alpha_composite(im, (0, y))

def doctor_box(fr, y, t, tin):
    if t < tin: return
    im = Image.new("RGBA", (W, 270), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((50, 0, W - 50, 260), 26, fill=(252, 231, 243), outline=PINK, width=4)
    lines = ["Disclaimer: for general awareness only.", "This video does not replace your doctor's opinion.",
             "Please consult your doctor before any test,", "diet change or medicine."]
    for i, l in enumerate(lines):
        d.text((W / 2, 50 + i * 52), l, font=font("Bold" if i == 0 else "Medium", 34 if i == 0 else 31), fill=(131, 24, 67) if i == 0 else GREY, anchor="mm")
    fr.alpha_composite(im, (0, y))

def close_pp(question_en, n):
    def s(fr, t, D):
        show(fr, big_logo(), 190, t, 0.2)
        fire("ding", 0.8); show(fr, box_text("Take any medicine only as advised by your doctor", GREEN, 42), 800, t, 0.8)
        show(fr, text_el(question_en, 50, color=(88, 28, 135)), 960, t, D * 0.3)
        show(fr, text_el("Comment, like & share!", 42, "Medium", GREY), 1060, t, D * 0.36)
        fire("pop", D * 0.45)
        show(fr, text_el("Follow for daily health tips", 42, color=(88, 28, 135)), 1160, t, D * 0.45)
        social3(fr, 1235, t, D * 0.5)
        show(fr, series_pill(n), 1385, t, D * 0.58)
        doctor_box(fr, 1480, t, D * 0.65)
    return s

def close_voice_hi(question_hi):
    return ("याद रखें, कोई भी दवा, सिर्फ डॉक्टर की सलाह से ही लें. " + question_hi +
            " कमेंट करें, लाइक और शेयर करें, और रोज़ की हेल्थ टिप्स के लिए फॉलो करें. "
            "यह वीडियो सिर्फ जानकारी के लिए है, डॉक्टर की राय की जगह नहीं ले सकता.")
