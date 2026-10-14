import json, subprocess, warnings
warnings.filterwarnings("ignore")
from TTS.utils.synthesizer import Synthesizer
from hts_close import close_voice
lines = [
 "विकास में देरी, बौद्धिक अक्षमता, या कम उम्र में मिर्गी. कई बच्चों में कारण जेनेटिक होता है. होल एक्सोम सीक्वेंसिंग कैसे मदद करता है, देखिए.",
 "होल एक्सोम सीक्वेंसिंग, लगभग बीस हज़ार जीन के कोडिंग हिस्से को, एक साथ पढ़ता है. ज्ञात जेनेटिक बीमारियों के ज़्यादातर बदलाव, इसी हिस्से में मिलते हैं.",
 "न्यूरोडेवलपमेंटल डिसऑर्डर पर एक बड़े मेटा एनालिसिस में, एक्सोम की डायग्नोस्टिक यील्ड लगभग छत्तीस प्रतिशत थी. साथ में दूसरी समस्याएं हों, तो लगभग तिरेपन प्रतिशत. माइक्रोऐरे से यह लगभग पंद्रह से बीस प्रतिशत रहती है.",
 "मिर्गी पर एक सिस्टमैटिक रिव्यू में, एक्सोम की यील्ड लगभग चौबीस प्रतिशत थी. जेनेटिक कारण मिलने से, इलाज की योजना में भी मदद मिल सकती है.",
 "ए सी एम जी गाइडलाइन, दो हज़ार इक्कीस, एक साल से पहले जन्मजात विकृति, या अठारह साल से पहले विकास में देरी या बौद्धिक अक्षमता में, एक्सोम या जीनोम को पहली या दूसरी पंक्ति की जांच के रूप में सुझाती है.",
 "सैंपल भेजते समय क्या चाहिए? ई डी टी ए ब्लड सैंपल. पूरा क्लिनिकल ब्योरा, पिछली जांचें, और पारिवारिक इतिहास. संभव हो, तो माता पिता के साथ ट्रायो. और जांच से पहले और बाद में, जेनेटिक काउंसलिंग.",
 "सीमाएं भी जानें. एक्सोम, फ्रैजाइल एक्स जैसे रिपीट एक्सपेंशन, माइटोकॉन्ड्रियल डी एन ए, और कई बड़े डिलीशन ठीक से नहीं पकड़ता. अनिश्चित वेरिएंट आ सकते हैं. और नेगेटिव रिपोर्ट को, बाद में दोबारा एनालाइज़ किया जा सकता है.",
 close_voice("क्या आपके पास ऐसे बच्चे आते हैं, जिनका कारण अभी तक नहीं मिला?"),
]
import os
d = os.environ.get("HTS_MODEL", "/tmp/hi/hi/")
s = Synthesizer(tts_checkpoint=d + "fastpitch/best_model.pth", tts_config_path=d + "fastpitch/config.json",
                vocoder_checkpoint=d + "hifigan/best_model.pth", vocoder_config=d + "hifigan/config.json", use_cuda=False)
durs = []
for i, l in enumerate(lines):
    f = f"/tmp/w1r_{i}.wav"; s.save_wav(s.tts(l, speaker_name="female"), f)
    subprocess.run(["ffmpeg","-nostdin","-y","-loglevel","error","-i",f,"-af","rubberband=pitch=0.96:formant=preserved,equalizer=f=250:t=q:w=1:g=2,treble=g=-1.5:f=6000",f"/tmp/w1_{i}.wav"],check=True); f=f"/tmp/w1_{i}.wav"
    durs.append(float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).decode()))
json.dump(durs, open("/tmp/w1_durs.json", "w")); print([round(x, 1) for x in durs], round(sum(durs), 1))
