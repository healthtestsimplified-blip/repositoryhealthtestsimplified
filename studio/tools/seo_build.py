"""Pre-render video cards into index.html and regenerate JSON-LD + sitemap. Run after any content change."""
import json, re, subprocess, sys, time, datetime
from playwright.sync_api import sync_playwright
import os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "site")
SITE = "https://healthtestsimplified.netlify.app/"
FB = "https://www.facebook.com/profile.php?id=61594730205462"
YT = "https://www.youtube.com/@Healthtestsimplified"
UPLOAD = {"thyroid": "2026-10-07"}  # default 2026-10-06
try:
    for _t in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "calendar.json")))["topics"]:
        if _t.get("status") == "done": UPLOAD[_t.get("video", _t["id"])] = _t["date"]
except Exception: pass
html = open(f"{ROOT}/index.html", encoding="utf-8").read()
srv = subprocess.Popen([sys.executable, "-m", "http.server", "8799"], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium"); pg = b.new_page()
        pg.goto("http://localhost:8799/"); pg.evaluate("localStorage.clear()"); pg.goto("http://localhost:8799/"); pg.wait_for_timeout(600)
        main_html = pg.eval_on_selector("#main", "e => e.innerHTML")
        data = pg.evaluate("V.map(v => ({id:v.id, t:v.t, s:v.s, l:v.l, d:v.d, k:(KEYS[v.id]||'')}))")
        b.close()
finally:
    srv.terminate()
# 1. static cards inside <main>
html = re.sub(r'<main id="main">.*?</main>', '<main id="main">' + main_html + '</main>', html, flags=re.S)
# 2. JSON-LD
def iso(d): m, s = d.split(":"); return f"PT{int(m)}M{int(s)}S"
vids = [{"@type": "VideoObject", "name": v["t"], "description": v["s"],
         "thumbnailUrl": SITE + f"p/{v['id']}.jpg", "contentUrl": SITE + f"v/{v['id']}.mp4",
         "uploadDate": UPLOAD.get(v["id"], "2026-10-06") + "T08:00:00+05:30", "duration": iso(v["d"]),
         "inLanguage": "bn" if v["l"] == "Bengali" else "hi", "url": SITE + "#" + v["id"], "keywords": v["k"]} for v in data]
ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "Organization", "@id": SITE + "#org", "name": "Health Test Simplified", "url": SITE,
     "logo": SITE + "logo.jpg", "sameAs": [FB, YT]},
    {"@type": "WebSite", "name": "Health Test Simplified", "url": SITE, "inLanguage": ["en", "hi", "bn"], "publisher": {"@id": SITE + "#org"}},
    {"@type": "ItemList", "name": "Health test videos", "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": v} for i, v in enumerate(vids)]}]}
block = '<script type="application/ld+json" id="ld">' + json.dumps(ld, ensure_ascii=False) + '</script>'
if 'id="ld"' in html: html = re.sub(r'<script type="application/ld\+json" id="ld">.*?</script>', lambda m: block, html, flags=re.S)
else: html = html.replace("</head>", block + "\n</head>", 1)
open(f"{ROOT}/index.html", "w", encoding="utf-8").write(html)
# 3. sitemap + robots
today = datetime.date.today().isoformat()
open(f"{ROOT}/sitemap.xml", "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url><loc>{SITE}</loc><lastmod>{today}</lastmod><changefreq>daily</changefreq><priority>1.0</priority></url>\n</urlset>\n')
open(f"{ROOT}/robots.txt", "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n")
print("ok", len(data), "videos")
