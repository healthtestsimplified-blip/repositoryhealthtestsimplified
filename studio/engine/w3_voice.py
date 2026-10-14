import json, subprocess, warnings
warnings.filterwarnings("ignore")
from TTS.utils.synthesizer import Synthesizer
from hts_close import close_voice
lines = [
 "एन आई सी यू में गंभीर रूप से बीमार नवजात, और कारण स्पष्ट नहीं? रैपिड एक्सोम कैसे मदद कर सकता है, देखिए.",
 "किन नवजात में सोचें? कई जन्मजात विकृतियां, बिना कारण दौरे, बहुत ज़्यादा ढीलापन, मेटाबॉलिक संकट, या असामान्य लक्षणों का समूह, जब शुरुआती जांच से कारण न मिले.",
 "जामा पीडियाट्रिक्स, दो हज़ार सत्रह के एक अध्ययन में, आई सी यू के दो सौ अठहत्तर शिशुओं में, एक्सोम से लगभग सैंतीस प्रतिशत में डायग्नोसिस मिला. रैपिड ट्रायो एक्सोम में, यह लगभग इक्यावन प्रतिशत था.",
 "रैपिड ट्रायो एक्सोम का मीडियन टर्नअराउंड, लगभग तेरह दिन था. यानी तब जवाब, जब फैसले जल्दी लेने होते हैं.",
 "उसी अध्ययन में, जिन शिशुओं में डायग्नोसिस मिला, उनमें से लगभग आधे में इलाज या देखभाल की योजना बदली. और परिवार को, अगली प्रेगनेंसी के खतरे की सही जानकारी मिली.",
 "ज़रूरी बातें. शिशु और दोनों माता पिता के ई डी टी ए सैंपल. नवजात से लगभग एक से दो एम एल खून काफी होता है. पूरा क्लिनिकल सार और जांचों के नतीजे साथ भेजें. और परिवार की काउंसलिंग.",
 "हर लैब का टर्नअराउंड अलग होता है. और नतीजे को हमेशा, क्लिनिकल टीम और जेनेटिक विशेषज्ञ मिलकर समझते हैं.",
 close_voice("क्या आपके एन आई सी यू में ऐसे शिशु आते हैं?"),
]
import os
d = os.environ.get("HTS_MODEL", "/tmp/hi/hi/")
s = Synthesizer(tts_checkpoint=d + "fastpitch/best_model.pth", tts_config_path=d + "fastpitch/config.json",
                vocoder_checkpoint=d + "hifigan/best_model.pth", vocoder_config=d + "hifigan/config.json", use_cuda=False)
durs = []
for i, l in enumerate(lines):
    f = f"/tmp/w3r_{i}.wav"; s.save_wav(s.tts(l, speaker_name="female"), f)
    subprocess.run(["ffmpeg","-nostdin","-y","-loglevel","error","-i",f,"-af","rubberband=pitch=0.96:formant=preserved,equalizer=f=250:t=q:w=1:g=2,treble=g=-1.5:f=6000",f"/tmp/w3_{i}.wav"],check=True); f=f"/tmp/w3_{i}.wav"
    durs.append(float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).decode()))
json.dump(durs, open("/tmp/w3_durs.json", "w")); print([round(x, 1) for x in durs], round(sum(durs), 1))
