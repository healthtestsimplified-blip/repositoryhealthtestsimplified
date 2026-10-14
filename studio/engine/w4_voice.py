import json, subprocess, warnings
warnings.filterwarnings("ignore")
from TTS.utils.synthesizer import Synthesizer
from hts_close import close_voice
lines = [
 "बड़ों में भी जेनेटिक बीमारी? हां. जब कम उम्र में बीमारी हो, परिवार में कई लोग प्रभावित हों, या कारण न मिले, तो एक्सोम मदद कर सकता है. देखिए.",
 "एक अध्ययन में, चार सौ छियासी वयस्कों में, एक्सोम से लगभग साढ़े सत्रह प्रतिशत में डायग्नोसिस मिला. अठारह से तीस साल की उम्र में, यह लगभग चौबीस प्रतिशत था.",
 "किडनी में, न्यू इंग्लैंड जर्नल के एक अध्ययन में, क्रोनिक किडनी डिज़ीज़ के तीन हज़ार से ज़्यादा मरीज़ों में, लगभग नौ प्रतिशत में जेनेटिक कारण मिला. अज्ञात कारण वाली किडनी बीमारी में, लगभग सत्रह प्रतिशत.",
 "दूसरे उपयोग. वंशानुगत कार्डियोमायोपैथी और दिल की धड़कन की बीमारियां, न्यूरोमस्कुलर बीमारियां, आंख की रेटिना की वंशानुगत बीमारियां, और कम उम्र में असामान्य न्यूरोलॉजिकल लक्षण.",
 "डायग्नोसिस से सही इलाज, बीमारी का अनुमान, और परिवार के दूसरे लोगों की जांच, यानी कैस्केड टेस्टिंग, संभव होती है.",
 "ज़रूरी बातें. ई डी टी ए ब्लड सैंपल, विस्तृत क्लिनिकल जानकारी, और कम से कम तीन पीढ़ियों का पारिवारिक इतिहास. कुछ मामलों में, एक्सोम से पहले टार्गेटेड जीन पैनल भी विकल्प होता है.",
 "जांच से पहले सहमति लें, और तय करें कि सेकेंडरी फाइंडिंग्स रिपोर्ट करनी हैं या नहीं. नेगेटिव या अनिश्चित रिपोर्ट को, समय के साथ दोबारा देखा जा सकता है.",
 close_voice("क्या आपके पास ऐसे मरीज़ हैं, जिनके परिवार में एक ही बीमारी बार बार दिखती है?"),
]
import os
d = os.environ.get("HTS_MODEL", "/tmp/hi/hi/")
s = Synthesizer(tts_checkpoint=d + "fastpitch/best_model.pth", tts_config_path=d + "fastpitch/config.json",
                vocoder_checkpoint=d + "hifigan/best_model.pth", vocoder_config=d + "hifigan/config.json", use_cuda=False)
durs = []
for i, l in enumerate(lines):
    f = f"/tmp/w4r_{i}.wav"; s.save_wav(s.tts(l, speaker_name="female"), f)
    subprocess.run(["ffmpeg","-nostdin","-y","-loglevel","error","-i",f,"-af","rubberband=pitch=0.96:formant=preserved,equalizer=f=250:t=q:w=1:g=2,treble=g=-1.5:f=6000",f"/tmp/w4_{i}.wav"],check=True); f=f"/tmp/w4_{i}.wav"
    durs.append(float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).decode()))
json.dump(durs, open("/tmp/w4_durs.json", "w")); print([round(x, 1) for x in durs], round(sum(durs), 1))
