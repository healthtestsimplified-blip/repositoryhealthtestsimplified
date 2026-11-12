"""Build one crawlable page per video at site/watch/<id>/index.html, plus a full sitemap.
Called from seo_build.py with the video data read from the built homepage."""
import json, os, html as H, datetime

SITE = "https://healthtestsimplified.netlify.app/"
FB = "https://www.facebook.com/profile.php?id=61594730205462"
YT = "https://www.youtube.com/@Healthtestsimplified"

CSS = """:root{--ink:#0b2545;--muted:#5a6b7d;--line:#e1e8ef;--teal:#0f8b8d;--teal-soft:#e6f5f5;--navy-soft:#e9eff7;--amber-soft:#fff4e3;--bg2:#f4f8fb}
*{box-sizing:border-box}body{margin:0;background:#fff;color:var(--ink);font:400 1.05rem/1.6 Mukta,system-ui,sans-serif}
h1,h2,h3{font-family:"Plus Jakarta Sans",system-ui,sans-serif;line-height:1.2;margin:0;letter-spacing:-.01em}
a{color:var(--teal)}.wrap{max-width:1080px;margin-inline:auto;padding-inline:20px}
.hdr{border-bottom:1px solid var(--line);background:#fff}.top{display:flex;align-items:center;gap:10px;padding-block:10px}
.top img{width:40px;height:40px;border-radius:50%;border:1px solid var(--line)}.top .n{font-family:"Plus Jakarta Sans",system-ui,sans-serif;font-weight:800;color:var(--ink);text-decoration:none;font-size:1.1rem}.top .n b{color:var(--teal)}
.top .g{flex:1}.top .home{font-family:"Plus Jakarta Sans",system-ui,sans-serif;font-weight:700;font-size:.9rem;text-decoration:none;border:1px solid var(--line);border-radius:999px;padding:6px 14px;color:var(--ink)}
.crumb{font-size:.88rem;color:var(--muted);margin:16px 0 6px}.crumb a{color:var(--muted)}
.main{display:grid;grid-template-columns:minmax(0,380px) minmax(0,1fr);gap:32px;align-items:start;padding-block:10px 30px}
video{width:100%;aspect-ratio:9/16;background:#000;border-radius:18px;display:block}
.meta{display:flex;gap:6px;flex-wrap:wrap;font:700 .75rem "Plus Jakarta Sans",system-ui,sans-serif;margin-bottom:10px}.meta span{background:var(--navy-soft);border-radius:999px;padding:2px 10px}.meta .l{background:var(--teal-soft);color:var(--teal)}
h1{font-size:clamp(1.6rem,3.4vw,2.3rem);font-weight:800}.sum{color:var(--muted);font-size:1.08rem;margin:10px 0 16px}
dl{display:grid;gap:12px;margin:0 0 18px}dt{font:700 .85rem "Plus Jakarta Sans",system-ui,sans-serif;color:var(--teal);text-transform:uppercase;letter-spacing:.05em}dd{margin:2px 0 0}
.acts{display:flex;flex-wrap:wrap;gap:8px;margin:6px 0 18px}.btn{display:inline-flex;align-items:center;font:700 .92rem "Plus Jakarta Sans",system-ui,sans-serif;text-decoration:none;border-radius:999px;padding:10px 18px}
.wa{background:#25d366;color:#06331a}.pdf{background:var(--navy-soft);color:var(--ink)}.fb{background:#1877f2;color:#fff}.yt{background:#e00000;color:#fff}
.disc{background:var(--amber-soft);border-radius:12px;padding:10px 14px;font-size:.92rem;margin:0 0 10px}
.rel{background:var(--bg2);border-top:1px solid var(--line);padding-block:28px 36px}.rel h2{font-size:1.4rem;margin-bottom:14px}
.rg{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}.rc{text-decoration:none;color:var(--ink);background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden}
.rc img{width:100%;aspect-ratio:4/5;object-fit:cover;object-position:center 30%;display:block}.rc b{display:block;padding:8px 10px;font:700 .92rem/1.3 "Plus Jakarta Sans",system-ui,sans-serif}
footer{color:var(--muted);font-size:.9rem;padding-block:20px 36px}
@media(max-width:760px){.main{grid-template-columns:minmax(0,1fr)}video{max-height:78vh}.rg{grid-template-columns:repeat(2,minmax(0,1fr))}}"""

def iso(d):
    m, s = d.split(":"); return f"PT{int(m)}M{int(s)}S"

def build(root, data, cats, upload):
    e = H.escape
    catname = {c["id"]: c["name"] for c in cats}
    os.makedirs(f"{root}/watch", exist_ok=True)
    urls = []
    for v in data:
        vid = v["id"]; url = f"{SITE}watch/{vid}/"; urls.append((url, v))
        lang = "bn" if v["l"] == "Bengali" else "hi"
        title = f'{v["t"]} | {v["l"]} video | Health Test Simplified'
        desc = v["s"][:300]
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "VideoObject", "name": v["t"], "description": v["s"], "thumbnailUrl": SITE + f"p/{vid}.jpg",
             "contentUrl": SITE + f"v/{vid}.mp4", "uploadDate": upload.get(vid, "2026-10-06") + "T08:00:00+05:30",
             "duration": iso(v["d"]), "inLanguage": lang, "url": url, "keywords": v.get("k", ""),
             "publisher": {"@type": "Organization", "name": "Health Test Simplified", "logo": {"@type": "ImageObject", "url": SITE + "logo.jpg"}}},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE},
                {"@type": "ListItem", "position": 2, "name": catname.get(v["c"], "Videos"), "item": SITE + "#library"},
                {"@type": "ListItem", "position": 3, "name": v["t"], "item": url}]}]}
        dl = "".join(f"<dt>{e(a)}</dt><dd>{e(b)}</dd>" for a, b in v["x"])
        pdf = f'<a class="btn pdf" href="../../cases/{vid}.pdf" download>Download the 2-page PDF</a>' if os.path.exists(f"{root}/cases/{vid}.pdf") else ""
        wa = "https://wa.me/?text=" + H.escape(__import__("urllib.parse").parse.quote(f'{v["t"]}: watch this short {v["l"]} video: {url}'))
        rel = [r for r in data if r["c"] == v["c"] and r["id"] != vid][:8]
        if len(rel) < 4: rel += [r for r in data if r["id"] != vid and r not in rel][:4 - len(rel)]
        relh = "".join(f'<a class="rc" href="../{r["id"]}/"><img src="../../p/{r["id"]}.jpg" alt="" loading="lazy" width="360" height="640"><b>{e(r["t"])}</b></a>' for r in rel)
        page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="keywords" content="{e(v.get('k',''))}">
<meta name="robots" content="index, follow, max-image-preview:large, max-video-preview:-1">
<link rel="canonical" href="{url}">
<meta property="og:site_name" content="Health Test Simplified"><meta property="og:type" content="video.other">
<meta property="og:title" content="{e(v['t'])}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}p/{vid}.jpg">
<meta property="og:video" content="{SITE}v/{vid}.mp4"><meta property="og:video:type" content="video/mp4">
<meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#0b2545">
<link rel="icon" href="../../logo.jpg">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=Mukta:wght@400;500;600&display=swap">
<style>{CSS}</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head><body>
<header class="hdr"><div class="wrap top"><img src="../../logo.jpg" alt="Health Test Simplified logo" width="40" height="40"><a class="n" href="../../">Health <b>Test</b> Simplified</a><span class="g"></span><a class="home" href="../../#library">All videos</a></div></header>
<div class="wrap">
<p class="crumb"><a href="../../">Home</a> › <a href="../../#library">{e(catname.get(v['c'],'Videos'))}</a> › {e(v['t'])}</p>
<div class="main">
<video controls playsinline preload="metadata" poster="../../p/{vid}.jpg" src="../../v/{vid}.mp4"></video>
<article>
<div class="meta"><span>{e(catname.get(v['c'],''))}</span><span class="l">{e(v['l'])}</span><span>{e(v['d'])} min</span></div>
<h1>{e(v['t'])}</h1>
<p class="sum">{e(v['s'])}</p>
<dl>{dl}</dl>
<div class="acts"><a class="btn wa" href="{wa}" target="_blank" rel="noopener">Share on WhatsApp</a>{pdf}</div>
<p class="disc">For general awareness only. Facts may change over time. Don't compare your condition with a video; always consult your doctor and follow their advice. Take any medicine only as advised by your doctor.</p>
<div class="acts"><a class="btn fb" href="{FB}" target="_blank" rel="noopener">Follow on Facebook</a><a class="btn yt" href="{YT}" target="_blank" rel="noopener">Subscribe on YouTube</a></div>
</article></div></div>
<section class="rel"><div class="wrap"><h2>More videos</h2><div class="rg">{relh}</div></div></section>
<div class="wrap"><footer>Health Test Simplified · <a href="../../">Home</a> · Free health test videos in Hindi &amp; Bengali</footer></div>
</body></html>"""
        os.makedirs(f"{root}/watch/{vid}", exist_ok=True)
        open(f"{root}/watch/{vid}/index.html", "w", encoding="utf-8").write(page)
    # sitemap with video entries
    today = datetime.date.today().isoformat()
    def vx(url, v):
        return (f"  <url><loc>{url}</loc><lastmod>{upload.get(v['id'], '2026-10-06')}</lastmod>"
                f"<video:video><video:thumbnail_loc>{SITE}p/{v['id']}.jpg</video:thumbnail_loc>"
                f"<video:title>{e(v['t'])}</video:title><video:description>{e(v['s'][:2000])}</video:description>"
                f"<video:content_loc>{SITE}v/{v['id']}.mp4</video:content_loc>"
                f"<video:duration>{int(v['d'].split(':')[0])*60+int(v['d'].split(':')[1])}</video:duration></video:video></url>\n")
    sm = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
          'xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">\n'
          f"  <url><loc>{SITE}</loc><lastmod>{today}</lastmod><changefreq>daily</changefreq><priority>1.0</priority></url>\n"
          + "".join(vx(u, v) for u, v in urls) + "</urlset>\n")
    open(f"{root}/sitemap.xml", "w", encoding="utf-8").write(sm)
    return len(urls)
