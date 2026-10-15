# Genetics Clinical Series (for doctors and the sales team)

100 planned episodes: `studio/tools/genetics_series.json` (id g001..g100, group, title, status).
The owner asks for one episode at a time ("make second", "make third"...). Make the next episode whose status is not "done".

Each episode:
1. Research with WebSearch/WebFetch: guidelines, diagnostic yields, test choice, limits. Every number needs a source.
2. A REAL published case report (prefer open-access, prefer Indian authors). Summarise it in our own words; never copy text or figures; cite it and link the original article. Never invent patients or results.
3. Video: Hindi voice + English on-screen text, realistic documentary style (`real_style.py`, `doc_style.py`), detailed; may exceed 3 min (pass max_sec, about 8 min cap). Keep the standard close (`close_scene`/`close_voice`) and the disclaimer.
4. Case-study PDF for reps: `site/cases/<id>.pdf` (A4, 1–2 pages): case summary, what the test showed, how it helped, talking points for the doctor visit, references, disclaimer. Website section "Genetics Clinical Series" offers Watch / Case study PDF / Share on WhatsApp.
5. Add the video to data.js (c:"gen"), set the episode status "done" with "video": <id> in genetics_series.json, copy it to site/data/genetics.json, build, seo_build, test, push.
