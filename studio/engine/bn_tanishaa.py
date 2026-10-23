"""Bengali narration with Microsoft's bn-IN-TanishaaNeural voice (edge-tts, through the HTTPS proxy).
Usage: python3 bn_tanishaa.py g009      -> /tmp/g009bn_<i>.wav, /tmp/g009bn_durs.json, teaser /tmp/tzbn_g009_0.wav
Lines come from <id>_bn_voice.py (lines, close_voice_bn, TEASER_Q)."""
import asyncio, importlib, json, os, subprocess, sys
import edge_tts

VOICE = "bn-IN-TanishaaNeural"
RATE = os.environ.get("BN_RATE", "+0%")
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
    m = importlib.import_module(f"{k}_bn_voice")
    durs = []
    for i, l in enumerate(m.lines):
        await say(l, f"/tmp/{k}bn_{i}.mp3"); durs.append(to_wav(f"/tmp/{k}bn_{i}.mp3", f"/tmp/{k}bn_{i}.wav"))
    json.dump(durs, open(f"/tmp/{k}bn_durs.json", "w")); print([round(x, 1) for x in durs], round(sum(durs), 1), flush=True)
    lead = "পুরো ভিডিও, আমাদের ইউটিউব চ্যানেলে দেখুন. "
    await say(lead + m.close_voice_bn(m.TEASER_Q), f"/tmp/tzbn_{k}_0.mp3")
    du = to_wav(f"/tmp/tzbn_{k}_0.mp3", f"/tmp/tzbn_{k}_0.wav"); json.dump([du], open(f"/tmp/tzbn_{k}_durs.json", "w")); print("teaser", round(du, 1))

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1]))
