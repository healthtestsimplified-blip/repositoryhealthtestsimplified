#!/usr/bin/env bash
# One-time setup for a fresh session: Hindi voice model + Python packages.
set -e
python3 -c "import TTS" 2>/dev/null || pip install --break-system-packages -q "coqui-tts==0.27.5"
# coqui-tts 0.27.5 needs torch < 2.9 (no torchcodec) and transformers 4.x; pin them so the voice model loads.
python3 -c "import torch, torchaudio, transformers; assert torch.__version__.startswith('2.8') and transformers.__version__.startswith('4.')" 2>/dev/null || \
  pip install --break-system-packages -q "torch==2.8.0" "torchaudio==2.8.0" "transformers>=4.57,<5"
python3 -c "import PIL, numpy" 2>/dev/null || pip install --break-system-packages -q pillow numpy
python3 -c "import playwright" 2>/dev/null || pip install --break-system-packages -q playwright
command -v ffmpeg >/dev/null || { echo "ffmpeg missing"; exit 1; }
if [ ! -f /tmp/hi/hi/fastpitch/best_model.pth ]; then
  curl -sSL -o /tmp/hi.zip https://github.com/AI4Bharat/Indic-TTS/releases/download/v1-checkpoints-release/hi.zip
  mkdir -p /tmp/hi && unzip -q -o /tmp/hi.zip -d /tmp/hi && rm -f /tmp/hi.zip
fi
sed -i 's#"models/v1/hi/fastpitch/speakers.pth"#"/tmp/hi/hi/fastpitch/speakers.pth"#g' /tmp/hi/hi/fastpitch/config.json
echo "setup ok"
