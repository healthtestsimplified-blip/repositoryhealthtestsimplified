"""Standard closing scene + closing voice line for every Health Test Simplified video (from 8 Oct 2026 on)."""
from lft_cartoon2 import *

# Hindi voice for the last scene. Put the video-specific question in `question_hi`.
def close_voice(question_hi):
    return ("याद रखें, कोई भी दवा सिर्फ डॉक्टर की सलाह से ही लें. " + question_hi +
            " कमेंट में बताइए, और शेयर करें. और ज़्यादा जानकारी के लिए, हमारा फेसबुक पेज और यूट्यूब चैनल फॉलो करें. हेल्थ टेस्ट सिम्प्लिफाइड.")

FB_BLUE = (24, 119, 242); YT_RED = (230, 0, 0)

def social_row(fr, y, t, tin):
    if t < tin: return
    a = min(1, (t - tin) / 0.3)
    im = Image.new("RGBA", (W, 120), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for x0, col, lab, icon in ((70, FB_BLUE, "Facebook page", "f"), (560, YT_RED, "YouTube channel", "yt")):
        d.rounded_rectangle((x0, 10, x0 + 450, 110), 50, fill=col)
        cx = x0 + 60
        if icon == "f":
            d.ellipse((cx - 30, 30, cx + 30, 90), fill=WHITE)
            d.text((cx + 2, 62), "f", font=font("Bold", 52), fill=col, anchor="mm")
        else:
            d.rounded_rectangle((cx - 34, 38, cx + 34, 82), 12, fill=WHITE)
            d.polygon((cx - 10, 48, cx - 10, 72, cx + 14, 60), fill=col)
        d.text((x0 + 275, 60), lab, font=font("Bold", 36), fill=WHITE, anchor="mm")
    if a < 1: im.putalpha(im.getchannel("A").point(lambda v: int(v * a)))
    fr.alpha_composite(im, (0, y))

def close_scene(question_en, date_pill=None):
    def s(fr, t, D):
        show(fr, big_logo(), 190, t, 0.2)
        fire("ding", 0.8); show(fr, box_text("Take any medicine only as advised by your doctor", GREEN, 42), 800, t, 0.8)
        show(fr, text_el(question_en, 50, color=DBLUE), 960, t, D * 0.3)
        show(fr, text_el("Comment & share!", 42, "Medium", GREY), 1070, t, D * 0.38)
        fire("pop", D * 0.5)
        show(fr, text_el("Follow our Facebook page & YouTube channel to get more information", 42, color=DBLUE), 1190, t, D * 0.5)
        social_row(fr, 1290, t, D * 0.55)
        if date_pill: show(fr, pill(date_pill, ORANGE, size=32), 1470, t, D * 0.65)
        show(fr, text_el("For awareness only. Consult your doctor.", 30, "Regular", GREY), 1680, t, D * 0.7)
    return s

if __name__ == "__main__":
    fn = close_scene("Have you ever done this test?", "THURSDAY HEALTH TIPS  •  8 OCT 2026")
    NOW.update(t=9, t0=0, shake=0); fr = BASES["light"].copy(); fn(fr, 9.0, 10.0)
    fr.convert("RGB").resize((540, 960)).save("close_preview.png")
