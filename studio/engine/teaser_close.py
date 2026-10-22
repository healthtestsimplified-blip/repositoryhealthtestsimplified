"""End card for teaser Shorts cut from long videos: 'watch the full video' + standard close.
Usage: python3 teaser_close.py voice            -> make all voices
       python3 teaser_close.py render <id>      -> render /tmp/tz_<id>.mp4
"""
import json, subprocess, sys, os
from hts_close import close_voice, close_scene

T = {
    "g001": ("Which cases need genetic tests?", "आपके क्लिनिक में, किस तरह के केस में जेनेटिक जांच की ज़रूरत पड़ती है?"),
    "g002": ("How often do you see a VUS?", "आपकी प्रैक्टिस में, वी यू एस वाली रिपोर्ट कितनी बार आती है?"),
    "g003": ("Trio or singleton?", "आपकी प्रैक्टिस में, ट्रायो या सिंगलटन, कौन सा ज़्यादा चुना जाता है?"),
    "g004": ("Do you draw a pedigree?", "क्या आपके क्लिनिक में, हर जेनेटिक केस के लिए पेडिग्री बनाई जाती है?"),
    "g005": ("Who counsels before genetic tests?", "आपके क्लिनिक में, जेनेटिक टेस्ट से पहले काउंसलिंग कौन करता है?"),
    "g006": ("Do you order CMA first-tier?", "क्या आप डिले वाले बच्चों में, सी एम ए को पहला टेस्ट रखते हैं?"),
    "g007": ("When do you still order a karyotype?", "आप अपनी प्रैक्टिस में, कैरियोटाइप कब कराते हैं?"),
    "g008": ("Panel or exome first?", "आप पहले कौन सा टेस्ट कराते हैं, पैनल या एक्सोम?"),
    "story": ("Which chapter did you like most?", "आपको कौन सा चैप्टर सबसे अच्छा लगा?"),
}
LEAD = "पूरा वीडियो, हमारे यूट्यूब चैनल पर देखें. "

if __name__ == "__main__":
    if sys.argv[1] == "voice":
        import warnings; warnings.filterwarnings("ignore")
        from TTS.utils.synthesizer import Synthesizer
        d = os.environ.get("HTS_MODEL", "/tmp/hi/hi/")
        s = Synthesizer(tts_checkpoint=d + "fastpitch/best_model.pth", tts_config_path=d + "fastpitch/config.json",
                        vocoder_checkpoint=d + "hifigan/best_model.pth", vocoder_config=d + "hifigan/config.json", use_cuda=False)
        for k, (_, qh) in T.items():
            if len(sys.argv) > 2 and k not in sys.argv[2:]: continue
            f = f"/tmp/tzraw_{k}.wav"; s.save_wav(s.tts(LEAD + close_voice(qh), speaker_name="female"), f)
            subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", f, "-af",
                            "rubberband=pitch=0.96:formant=preserved,equalizer=f=250:t=q:w=1:g=2,treble=g=-1.5:f=6000",
                            f"/tmp/tz_{k}_0.wav"], check=True)
            du = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).decode())
            json.dump([du], open(f"/tmp/tz_{k}_durs.json", "w")); print(k, round(du, 1), flush=True)
    else:
        import doc_style  # registers doc/docl backgrounds
        from cbc_cartoon import run
        k = sys.argv[2]; qe, _ = T[k]
        run([(close_scene(qe, "WATCH THE FULL VIDEO ON OUR CHANNEL"), "docl")], f"/tmp/tz_{k}_", f"/tmp/tz_{k}.mp4", max_sec=180, cover_skip=0)
