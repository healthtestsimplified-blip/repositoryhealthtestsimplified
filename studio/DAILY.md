# Daily video runbook (Health Test Simplified)

Run every day at 00:00 IST. Goal: make the day's video from `studio/tools/calendar.json`, fact-check it, publish it on the website, and hand the MP4 + Facebook caption to the owner.

Repo layout: `site/` is what Netlify publishes (auto-deploys on every push to `main`). `studio/engine/` is the cartoon video engine, `studio/tools/` builds the website.

## 0. Setup (every fresh session)
```
cd <repo>/studio && bash setup.sh        # ~2–4 min: Hindi voice model (1.5 GB) + packages
```

## 1. Pick today's topic
Today = current date in Asia/Kolkata. In `studio/tools/calendar.json` take the topic whose `date` == today and `status` == "planned". If none (missed day), take the earliest planned topic with date <= today. If nothing is due, stop and report "no topic due".
The topic's `tests` list holds the exact Suraksha test names it covers.

## 2. Research and fact-check (mandatory)
- Use WebSearch/WebFetch. Prefer: WHO, ICMR, Indian professional bodies (API, FOGSI, IAP, Indian Thyroid Society), NHS, MedlinePlus, Mayo Clinic, Lab Tests Online, PubMed/PMC, major society guidelines.
- Every number, range, prevalence, timing and "who should test" claim must be backed by a source. If sources disagree or a value is lab-dependent, say "approximately", "varies by lab", or "as your doctor advises".
- India context: say "in India" only with an Indian source. Do not claim a test is universal/mandatory in India unless a source says so.
- Never give dosing. Never tell people to stop or change medicine. Never say "show this video to your doctor".
- Sensitive topics: no stigma (carriers, HIV, infertility, genetic conditions). Pregnancy videos must say the baby's sex is not disclosed (PCPNDT) where relevant.
- Save a short source list for the report.

## 3. Write the video (Hindi voice, English on-screen text)
Copy `studio/engine/example_voice.py` and `studio/engine/example_cartoon.py` (Thyroid, 7 Oct 2026) to new files named after the topic id, e.g. `ecg_voice.py`, `ecg_cartoon.py`. Use a new /tmp prefix (e.g. `/tmp/ecg_`).
- 9 scenes, about 2–2.5 minutes total: hook (navy/purple bg), what it is, why/when, what it shows, who should test, preparation, how to read the result, myth buster or good-to-know, close.
- Voice: Hindi, plain words, `.` not `।`, numbers in Hindi words. Hook ends with "आखिर तक देखिए".
- Daily pill on screen: e.g. `THURSDAY HEALTH TIPS  •  8 OCT 2026` (weekday + date in IST).
- Closing scene: ALWAYS `close_scene("<question in English>?", DATE)` from `hts_close.py`, and the voice line from `close_voice("<same question in Hindi>?")`. It says "Take any medicine only as advised by your doctor", "follow our Facebook page & YouTube channel to get more information", and shows + speaks the DISCLAIMER (general awareness only; facts may change; don't compare your condition with the video; consult your doctor and follow only their advice). The disclaimer is mandatory in every video: the Hindi text is `DISCLAIMER_HI` in hts_close.py and must be the end of the last voice line.
- Voice post-processing is already in example_voice.py (female voice, rubberband pitch 0.96, formant preserved). Keep it.
- Run the voice script in the background (`nohup python3 x_voice.py > /tmp/x_voice.log 2>&1 &`) and poll; it writes `/tmp/<prefix>durs.json`.

## 4. Check visuals before rendering
`python3 x_cartoon.py preview` writes `sheet.png` (9 thumbnails). Open it with Read and fix: overlapping text, text wrapping into other elements, missing glyphs (Poppins lacks →, ♥, ⁵ and similar; use plain words or "="), empty-looking scenes. Repeat until clean.

## 5. Render
`nohup python3 x_cartoon.py > /tmp/x_render.log 2>&1 &` then poll for `done` (8–10 min). Output MP4 is written in the engine folder: name it like `Thursday_Health_Tips_8Oct2026_ECG_Hindi.mp4`. Do not commit full-size MP4s from the engine folder; only the compressed site copy.

## 6. Publish on the website
From repo root:
```
ffmpeg -nostdin -y -loglevel error -i <MP4> -vf scale=540:960 -c:v libx264 -crf 30 -preset medium -c:a aac -b:a 64k -ac 1 -movflags +faststart site/v/<id>.mp4
ffmpeg -nostdin -y -loglevel error -ss 3 -i <MP4> -frames:v 1 -vf scale=360:640 -q:v 4 site/p/<id>.jpg
```
- In `studio/tools/data.js`, add an entry to `V` (before the `{id:"fever"` entry), same shape as the thyroid entry: `id`, `c` (one of tests / preg / gen / bio / daily; daily tips use "daily"), `t` title, `l:"Hindi"`, `d` duration m:ss, `s` one-line summary with the weekday + date, `x` 4–5 rows of [label, text] using only fact-checked content. Add search keywords to `KEYS` (common names, Hindi words people type, abbreviations).
- In `studio/tools/calendar.json`, set the topic `status` to "done" and add `"video": "<id>"`. Then regenerate the public copy:
```
python3 - <<'EOF'
import json; c=json.load(open('studio/tools/calendar.json'))
for t in c['topics']: t.pop('tests',None)
json.dump(c,open('site/data/calendar.json','w'),ensure_ascii=False,separators=(',',':'))
EOF
```
- Build: `python3 studio/tools/build.py <id>` (sets "Today's video") then `python3 studio/tools/seo_build.py` (pre-renders cards, JSON-LD, sitemap). (Upload dates come from calendar.json automatically.)
- Test: serve `site/` with `python3 -m http.server` and use Playwright (`executable_path='/opt/pw-browsers/chromium'`): no page errors, the new card exists, search for the topic finds it, today card shows it.
- Commit (author "Health Test Simplified <healthtestsimplified@gmail.com>") and push to `main`. Netlify deploys automatically in under a minute.

## 7. Report to the owner
Send the full-size MP4 with SendUserFile, and a short message with:
- what the video covers (5–7 bullets),
- the Facebook caption (must include the line "⚠️ For general awareness only. Facts may change. Don't compare your condition with this video; consult your doctor and follow their advice."): hook line, "Watch till the end 👀", a question, "Share with your family 🙏", "👉 Follow our Facebook page & YouTube channel to get more information", the direct link `https://healthtestsimplified.netlify.app/#<id>`, then hashtags. Always include: #HealthTestSimplified #india #WestBengal #assam #jharkhand #Bihar #science #biology #ReelsIndia #FBReels #viralreelschallenge plus 4–5 topic tags,
- the sources used, and anything lab-specific the owner should confirm with Suraksha's lab team.
If any step fails, publish nothing broken: report what failed and leave the website unchanged.
