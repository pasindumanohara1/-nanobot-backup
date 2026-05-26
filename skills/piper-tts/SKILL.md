---
name: piper-tts
description: Offline text-to-speech synthesis using Piper TTS. Trigger when the user wants to generate speech/audio from text, create voiceovers, or use text-to-speech. Supports multiple English voices. Runs entirely offline after model download.
---

# Piper TTS — Offline Text-to-Speech

Generate high-quality speech from text entirely offline using the Piper TTS engine.

## Quick Start

```powershell
cd "C:\Users\pasindu\.nanobot\workspace\skills\piper-tts"
python tts_engine.py "Your text here"
python tts_engine.py "Your text here" --model en_US-joe-medium --output my_audio.wav
python tts_engine.py --list-voices
```

## Available Voices

| Model | Language | Gender | Quality | Size |
|-------|----------|--------|---------|------|
| en_US-lessac-medium | English (US) | Female | Medium | ~60 MB |
| en_US-lessac-low | English (US) | Female | Low (faster) | ~25 MB |
| en_US-amy-medium | English (US) | Female | Medium | ~60 MB |
| en_US-joe-medium | English (US) | Male | Medium | ~60 MB |
| en_GB-alan-medium | English (UK) | Male | Medium | ~60 MB |
| en_GB-southern_male-medium | English (UK) | Male | Medium | ~60 MB |

**Default voice:** en_US-lessac-medium (female, US English)

## Python API

```python
import sys
sys.path.insert(0, r"C:\Users\pasindu\.nanobot\workspace\skills\piper-tts")
from tts_engine import synthesize, list_voices

# Generate speech
output_path = synthesize("Hello, this is a test.", model_name="en_US-lessac-medium")

# List available voices
voices = list_voices()
for v in voices:
    print(v["name"], v["downloaded"])
```

## Output Format

- **Format:** WAV (PCM 16-bit, mono)
- **Sample rate:** 22050 Hz
- **Auto-named:** `piper_output.wav` in user home, or specify `--output`

## Model Storage

Models are stored in `~\piper_models\` and auto-downloaded on first use.

## Sending to Telegram

After generating, use OWL's `message` tool:
- `content`: description of the audio
- `media`: array with the WAV file path
- `channel`: `telegram`
- `chat_id`: target chat ID

## Notes

- First run downloads the model (~60 MB) — subsequent runs are fully offline
- Synthesis is fast: ~3 min of speech generates in ~8 seconds
- For long text, the engine handles chunking automatically
- piper-tts Python package must be installed: `pip install piper-tts`
