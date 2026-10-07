#!/usr/bin/env bash
# One-time setup for a fresh session: Hindi voice model + Python packages.
set -e
python3 -c "import TTS" 2>/dev/null || pip install --break-system-packages -q "coqui-tts==0.27.5"
python3 -c "import PIL, numpy" 2>/dev/null || pip install --break-system-packages -q pillow numpy
python3 -c "import playwright" 2>/dev/null || pip install --break-system-packages -q playwright
command -v ffmpeg >/dev/null || { echo "ffmpeg missing"; exit 1; }
if [ ! -f /tmp/hi/hi/fastpitch/best_model.pth ]; then
  curl -sSL -o /tmp/hi.zip https://github.com/AI4Bharat/Indic-TTS/releases/download/v1-checkpoints-release/hi.zip
  mkdir -p /tmp/hi && unzip -q -o /tmp/hi.zip -d /tmp/hi && rm -f /tmp/hi.zip
fi
sed -i 's#"models/v1/hi/fastpitch/speakers.pth"#"/tmp/hi/hi/fastpitch/speakers.pth"#g' /tmp/hi/hi/fastpitch/config.json
echo "setup ok"
