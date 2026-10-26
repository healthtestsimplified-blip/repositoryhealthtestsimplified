"""Hindi narration with Microsoft's hi-IN-SwaraNeural voice (edge-tts via the HTTPS proxy).
Usage: python3 hi_swara.py d001   -> /tmp/d001_<i>.wav and /tmp/d001_durs.json
Lines come from studio/engine/<id>_voice.py (list `lines`). Env HI_RATE (e.g. +5%) to speed up."""
import asyncio, importlib, json, os, subprocess, sys
import edge_tts

VOICE = "hi-IN-SwaraNeural"
RATE = os.environ.get("HI_RATE", "+0%")
PROXY = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")

async def say(text, mp3):
    for attempt in range(4):
        try:
            await edge_tts.Communicate(text, VOICE, rate=RATE, proxy=PROXY).save(mp3)
            if os.path.getsize(mp3) > 1000: return
        except Exception as e:
            print("retry", attempt, e, flush=True)
        await asyncio.sleep(3)
    raise SystemExit("TTS failed: " + text[:40])

def to_wav(mp3, wav):
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", mp3, "-af", "aresample=44100,equalizer=f=250:t=q:w=1:g=1.5", "-ac", "1", wav], check=True)
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", wav]).decode())

async def main(k):
    m = importlib.import_module(f"{k}_voice")
    durs = []
    for i, l in enumerate(m.lines):
        await say(l, f"/tmp/{k}_{i}.mp3"); durs.append(to_wav(f"/tmp/{k}_{i}.mp3", f"/tmp/{k}_{i}.wav"))
    json.dump(durs, open(f"/tmp/{k}_durs.json", "w"))
    print([round(x, 1) for x in durs], "speech", round(sum(durs), 1), "video ~", round(sum(durs) + 1.3 * len(durs), 1))

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1]))
