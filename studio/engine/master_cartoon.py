import math, sys
from cbc_cartoon import run
import gene_cartoon as GN, nucleus_cartoon as NU, dna_cartoon as DN, histone_cartoon as HS, chromo_cartoon as CH, cell_cartoon as CE
from lft_cartoon2 import *

PINK = CH.PINK
AA = [(229, 57, 53), (30, 136, 229), (67, 160, 71), (251, 140, 0), (142, 36, 170), (0, 150, 170)]

def protein_chain(d, cx, cy, t, n=14, fold=0.0):
    pts = []
    for k in range(n):
        u = k / (n - 1)
        x = cx - 400 + 800 * u; y = cy + 30 * math.sin(k * 0.9 + t * 2)
        fx = cx + 150 * math.cos(u * 5.5 + 0.4) * (0.4 + 0.6 * u); fy = cy + 120 * math.sin(u * 5.5 + 0.4) * (0.4 + 0.6 * u)
        pts.append((x + (fx - x) * fold, y + (fy - y) * fold))
    d.line(pts, fill=(120, 120, 140), width=8, joint="curve")
    for k, (x, y) in enumerate(pts): d.ellipse((x - 26, y - 26, x + 26, y + 26), fill=AA[k % 6], outline=WHITE, width=4)

# ---------- icons for chapter cards ----------
def icon(fr, kind, t):
    d = ImageDraw.Draw(fr)
    if kind == "protein": protein_chain(d, 540, 820, t, 12, 0.6)
    elif kind == "gene":
        DN.helix(fr, 540, 820, 700, 110, t); d.rounded_rectangle((420, 690, 660, 950), 26, outline=YEL, width=10)
    elif kind == "dna": DN.helix(fr, 540, 820, 800, 130, t)
    elif kind == "hist": HS.nucleosome(d, 540, 820, 150, 1.0)
    elif kind == "chr": put(fr, CH.CHROMO, 540, 820, 0.8)
    elif kind == "nuc": put(fr, NU.NUCS, 540, 820, 0.75)
    else:
        d.ellipse((290, 640, 790, 1000), fill=(255, 225, 235), outline=PINK, width=12); put(fr, NU.NUCS, 540, 820, 0.4)

def chapter(n, title, col, kind):
    def fn(fr, t, D):
        rays(fr, 540, 820, t, col, a=50)
        fire("whoosh", 0.05)
        pop(fr, stroke_text(f"CHAPTER {n}", 80, WHITE, col, 8), 540, 380, t, 0.05)
        icon(fr, kind, t)
        pop(fr, stroke_text(title, 110, YEL, col, 10), 540, 1180, t, 0.4, "boom")
    return fn

# ---------- new scenes ----------
def m_intro(fr, t, D):
    rays(fr, 540, 900, t, (120, 160, 255), a=40)
    DN.helix(fr, 540, 1480, 1000, 80, t, alpha=110)
    pop(fr, white_text("From one tiny PROTEIN", 80), 540, 520, t, 0.1, "boom")
    pop(fr, white_text("to 30 lakh crore CELLS!", 80, color=YEL), 540, 680, t, 1.4, "whoosh")
    show(fr, white_text("The complete story of your body", 52), 840, t, D * 0.4)
    pop(fr, box_text("7 chapters: watch till the end!", GREEN, 46), 540, 1080, t, D * 0.6, "pop")

def m_protein(fr, t, D):
    show(fr, pill("PROTEINS = THE WORKERS", GREEN, size=46), 230, t, 0.1)
    d = ImageDraw.Draw(fr)
    protein_chain(d, 540, 520, t, 14, ease((t - D * 0.15) / (D * 0.3))); fire("whoosh", D * 0.15)
    show(fr, text_el("Made of 20 kinds of amino acids", 46, "Medium", DBLUE), 720, t, D * 0.1)
    items = [("Haemoglobin: carries oxygen", RED, "1"), ("Insulin: controls sugar", ORANGE, "2"), ("Antibodies: fight germs", PURPLE, "3"),
             ("Enzymes: digest food", TEAL, "4"), ("Keratin: hair & nails", (121, 85, 72), "5")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.3 + 0.11 * i)); show(fr, card(txt, c, m, size=40), 820 + i * 122, t, D * (0.3 + 0.11 * i))

def m_journey(fr, t, D):
    show(fr, pill("THE BIG PICTURE", BLUE, size=50), 230, t, 0.1)
    steps = [("PROTEIN", GREEN), ("GENE", ORANGE), ("DNA", BLUE), ("HISTONES", (66, 133, 244)), ("CHROMOSOME", (120, 70, 200)),
             ("NUCLEUS", PURPLE), ("CELL", PINK)]
    d = ImageDraw.Draw(fr)
    for i, (s, c) in enumerate(steps):
        tin = 0.3 + i * D * 0.09; fire("pop", tin)
        if t < tin: break
        y = 360 + i * 140; w = 300 + i * 70
        d.rounded_rectangle((540 - w / 2, y, 540 + w / 2, y + 96), 48, fill=c)
        d.text((540, y + 48), s, font=font("Bold", 44), fill=WHITE, anchor="mm")
        if i < 6: d.text((540 + w / 2 + 50, y + 70), "inside ▲" if False else "", font=font("Bold", 24), fill=GREY, anchor="mm")
    pop(fr, stroke_text("= YOU!", 120, YEL, RED, 10), 540, 1400, t, 0.3 + 7 * D * 0.09, "chime")

def m_lab(fr, t, D):
    show(fr, pill("YOUR LAB TESTS CHECK EVERY LEVEL", BLUE, size=42), 230, t, 0.1)
    ground(fr, 540, 640, 300); put(fr, DOC["idle"], 540, 450, 0.6)
    items = [("Albumin & total protein: PROTEIN", GREEN, "1"), ("HPLC: haemoglobin & thalassaemia", RED, "2"),
             ("Karyotype: CHROMOSOMES", (120, 70, 200), "3"), ("Pap smear: CELLS & NUCLEI", PINK, "4"), ("CBC: counts blood CELLS", BLUE, "5")]
    for i, (txt, c, m) in enumerate(items):
        fire("pop", D * (0.12 + 0.15 * i)); show(fr, card(txt, c, m, size=40), 720 + i * 135, t, D * (0.12 + 0.15 * i))

def m_close(fr, t, D):
    show(fr, big_logo(), 210, t, 0.2)
    fire("ding", 0.8); show(fr, box_text("Take any medicine only as advised by your doctor", GREEN, 42), 820, t, 0.8)
    show(fr, text_el("How did you like this journey?", 54, color=DBLUE), 1020, t, D * 0.45)
    show(fr, text_el("Tell us in the comments!", 44, "Medium", GREY), 1120, t, D * 0.55)
    show(fr, pill("Follow Health Test Simplified", BLUE, size=40), 1300, t, D * 0.65)
    show(fr, text_el("For awareness only. Consult your doctor.", 30, "Regular", GREY), 1680, t, D * 0.7)

SC = [(m_intro, "navy"),
      (chapter(1, "PROTEIN", GREEN, "protein"), "navy"), (m_protein, "light"),
      (chapter(2, "GENE", ORANGE, "gene"), "navy"), (GN.g_what, "light"), (NU.n_work, "light"),
      (chapter(3, "DNA", BLUE, "dna"), "navy"), (DN.d_what, "light"), (DN.d_letters, "light"),
      (chapter(4, "HISTONES", (66, 133, 244), "hist"), "navy"), (HS.h_wrap, "light"), (HS.h_switch, "light"),
      (chapter(5, "CHROMOSOME", (120, 70, 200), "chr"), "navy"), (CH.k_46, "light"), (CH.k_myth, "navy"),
      (chapter(6, "NUCLEUS", PURPLE, "nuc"), "navy"), (NU.n_parts, "light"),
      (chapter(7, "CELL", PINK, "cell"), "navy"), (CE.c_factory, "light"), (CE.c_types, "light"),
      (m_journey, "light"), (m_lab, "light"), (m_close, "light")]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        tests = [(0, 9, .8), (1, 4, .9), (2, 22, .95), (20, 18, .95), (21, 20, .95), (17, 4, .9)]
        ims = []
        for si, d_, p in tests:
            fn, bg = SC[si]; NOW.update(t=d_ * p, t0=0, shake=0)
            fr = BASES[bg].copy(); fn(fr, d_ * p, d_); ims.append(fr.convert("RGB").resize((270, 480)))
        s = Image.new("RGB", (270 * 6, 480), "white")
        for i, im in enumerate(ims): s.paste(im, (i * 270, 0))
        s.save("sheet.png")
    else: run(SC, "/tmp/ms_", "Protein_to_Cell_Full_Story_Hindi.mp4")
