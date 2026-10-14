import json, subprocess, warnings
warnings.filterwarnings("ignore")
from TTS.utils.synthesizer import Synthesizer
from hts_close import close_voice
lines = [
 "अल्ट्रासाउंड में भ्रूण में विकृति दिखी, पर कैरियोटाइप और माइक्रोऐरे सामान्य? अब आगे क्या? प्रीनेटल एक्सोम के बारे में देखिए.",
 "सोसाइटी गाइडेंस के अनुसार, प्रीनेटल एक्सोम तब सोचा जाता है, जब कई विकृतियां हों, या एक बड़ी विकृति जो जेनेटिक बीमारी की ओर इशारा करे, और माइक्रोऐरे नेगेटिव हो.",
 "दो बड़े अध्ययनों में, सामान्य कैरियोटाइप और माइक्रोऐरे के बाद, एक्सोम ने लगभग साढ़े आठ से दस प्रतिशत मामलों में कारण बताया. कई विकृतियों में यह लगभग पंद्रह प्रतिशत रहा, और कंकाल की विकृतियों में इससे भी ज़्यादा.",
 "पिछला बच्चा या भ्रूण, जिसमें मिलती जुलती विकृति थी, और कारण पता नहीं चला? ऐसे परिवार में कारण मिल जाए, तो अगली प्रेगनेंसी में जांच की योजना बन सकती है.",
 "ज़रूरी बातें. ट्रायो, यानी भ्रूण और माता पिता, तीनों के सैंपल. भ्रूण का सैंपल सी वी एस या एमनियोसेंटेसिस से. और अल्ट्रासाउंड की पूरी जानकारी, सैंपल के साथ.",
 "जांच से पहले और बाद में, विस्तार से काउंसलिंग ज़रूरी है. अनिश्चित वेरिएंट आ सकते हैं, और रिपोर्ट में समय लगता है. यह जांच सिर्फ बीमारी के लिए है. बच्चे का लिंग नहीं बताया जाता.",
 "ध्यान रहे, गर्भ में लक्षण सिर्फ अल्ट्रासाउंड से दिखते हैं, इसलिए यील्ड जन्म के बाद की जांच से कम होती है. बाद में नई जानकारी जोड़कर, दोबारा एनालिसिस से मदद मिल सकती है.",
 close_voice("क्या आपके क्लिनिक में ऐसे केस आते हैं?"),
]
import os
d = os.environ.get("HTS_MODEL", "/tmp/hi/hi/")
s = Synthesizer(tts_checkpoint=d + "fastpitch/best_model.pth", tts_config_path=d + "fastpitch/config.json",
                vocoder_checkpoint=d + "hifigan/best_model.pth", vocoder_config=d + "hifigan/config.json", use_cuda=False)
durs = []
for i, l in enumerate(lines):
    f = f"/tmp/w2r_{i}.wav"; s.save_wav(s.tts(l, speaker_name="female"), f)
    subprocess.run(["ffmpeg","-nostdin","-y","-loglevel","error","-i",f,"-af","rubberband=pitch=0.96:formant=preserved,equalizer=f=250:t=q:w=1:g=2,treble=g=-1.5:f=6000",f"/tmp/w2_{i}.wav"],check=True); f=f"/tmp/w2_{i}.wav"
    durs.append(float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).decode()))
json.dump(durs, open("/tmp/w2_durs.json", "w")); print([round(x, 1) for x in durs], round(sum(durs), 1))
