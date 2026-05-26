"""
Piper TTS Engine — Offline text-to-speech synthesis.

Usage:
    python tts_engine.py "Your text here" [--output output.wav] [--model model_name]

Available models (downloaded to ~/piper_models/):
    en_US-lessac-medium   (English, female, medium quality) [default]
    en_US-lessac-low      (English, female, low quality / faster)
    en_US-amy-medium      (English, female, different voice)
    en_US-joe-medium      (English, male, medium quality)
    en_GB-alan-medium     (British English, male)
    en_GB-southern_male-medium (British English, male, southern)

First run auto-downloads the default model if not present.
"""

import os
import sys
import wave
import urllib.request
import json

MODEL_DIR = os.path.join(os.path.expanduser("~"), "piper_models")

# HuggingFace voice catalog (subset of popular English voices)
VOICES = {
    "en_US-lessac-medium": {
        "url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx",
        "size_mb": 60,
        "lang": "en-US",
        "gender": "female",
        "quality": "medium",
    },
    "en_US-lessac-low": {
        "url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/low/en_US-lessac-low.onnx",
        "size_mb": 25,
        "lang": "en-US",
        "gender": "female",
        "quality": "low",
    },
    "en_US-amy-medium": {
        "url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/amy/medium/en_US-amy-medium.onnx",
        "size_mb": 60,
        "lang": "en-US",
        "gender": "female",
        "quality": "medium",
    },
    "en_US-joe-medium": {
        "url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/joe/medium/en_US-joe-medium.onnx",
        "size_mb": 60,
        "lang": "en-US",
        "gender": "male",
        "quality": "medium",
    },
    "en_GB-alan-medium": {
        "url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/alan/medium/en_GB-alan-medium.onnx",
        "size_mb": 60,
        "lang": "en-GB",
        "gender": "male",
        "quality": "medium",
    },
    "en_GB-southern_male-medium": {
        "url": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_GB/southern_english_male/medium/en_GB-southern_male-medium.onnx",
        "size_mb": 60,
        "lang": "en-GB",
        "gender": "male",
        "quality": "medium",
    },
}


def download_voice(model_name: str) -> tuple[str, str]:
    """Download a voice model and its config. Returns (onnx_path, json_path)."""
    if model_name not in VOICES:
        raise ValueError(f"Unknown model: {model_name}. Available: {list(VOICES.keys())}")

    info = VOICES[model_name]
    os.makedirs(MODEL_DIR, exist_ok=True)

    base_name = model_name + ".onnx"
    onnx_path = os.path.join(MODEL_DIR, base_name)
    json_path = onnx_path + ".json"

    # Download ONNX model
    if not os.path.exists(onnx_path) or os.path.getsize(onnx_path) < 1000:
        print(f"Downloading {model_name} (~{info['size_mb']} MB)...", flush=True)
        req = urllib.request.Request(info["url"], headers={"User-Agent": "Mozilla/5.0"})
        opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler)
        resp = opener.open(req, timeout=300)
        data = resp.read()
        with open(onnx_path, "wb") as f:
            f.write(data)
        print(f"  Saved: {onnx_path} ({len(data)} bytes)", flush=True)
    else:
        print(f"Model already exists: {onnx_path}", flush=True)

    # Download JSON config
    if not os.path.exists(json_path) or os.path.getsize(json_path) < 100:
        json_url = info["url"] + ".json"
        print(f"Downloading config...", flush=True)
        req = urllib.request.Request(json_url, headers={"User-Agent": "Mozilla/5.0"})
        opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler)
        resp = opener.open(req, timeout=60)
        data = resp.read()
        with open(json_path, "wb") as f:
            f.write(data)
        print(f"  Saved: {json_path}", flush=True)

    return onnx_path, json_path


def synthesize(text: str, model_name: str = "en_US-lessac-medium",
               output_path: str | None = None) -> str:
    """
    Synthesize text to speech using Piper.

    Args:
        text: Text to convert to speech
        model_name: Voice model to use (default: en_US-lessac-medium)
        output_path: Output WAV file path (default: auto-generated)

    Returns:
        Path to the generated WAV file
    """
    from piper.voice import PiperVoice

    onnx_path, json_path = download_voice(model_name)

    if output_path is None:
        output_path = os.path.join(os.path.expanduser("~"), "piper_output.wav")

    print(f"Loading model: {onnx_path}", flush=True)
    voice = PiperVoice.load(onnx_path)

    print(f"Synthesizing ({len(text)} chars)...", flush=True)
    audio = voice.synthesize(text)

    all_audio = bytearray()
    chunk_count = 0
    for chunk in audio:
        b = chunk.audio_int16_bytes
        if b:
            all_audio.extend(b)
            chunk_count += 1

    # Determine sample rate
    sr = 22050
    if hasattr(voice, "config") and hasattr(voice.config, "sample_rate"):
        sr = voice.config.sample_rate

    duration_sec = len(all_audio) / (2 * sr)

    with wave.open(output_path, "w") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sr)
        wav.writeframes(bytes(all_audio))

    size_kb = os.path.getsize(output_path) / 1024
    print(f"Done! {chunk_count} chunks, {size_kb:.0f} KB, ~{duration_sec:.0f}s", flush=True)
    print(f"Output: {output_path}", flush=True)

    return output_path


def list_voices() -> list[dict]:
    """List all available voices and their download status."""
    voices = []
    for name, info in VOICES.items():
        onnx_path = os.path.join(MODEL_DIR, name + ".onnx")
        voices.append({
            "name": name,
            "lang": info["lang"],
            "gender": info["gender"],
            "quality": info["quality"],
            "size_mb": info["size_mb"],
            "downloaded": os.path.exists(onnx_path) and os.path.getsize(onnx_path) > 1000,
        })
    return voices


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Piper TTS — Offline text-to-speech")
    parser.add_argument("text", nargs="?", help="Text to synthesize")
    parser.add_argument("--output", "-o", help="Output WAV file path")
    parser.add_argument("--model", "-m", default="en_US-lessac-medium",
                        help="Voice model name (default: en_US-lessac-medium)")
    parser.add_argument("--list-voices", action="store_true",
                        help="List available voices")

    args = parser.parse_args()

    if args.list_voices:
        print("\nAvailable voices:")
        print(f"{'Name':<35} {'Lang':<8} {'Gender':<8} {'Quality':<8} {'Size':<8} {'Status'}")
        print("-" * 80)
        for v in list_voices():
            status = "Downloaded" if v["downloaded"] else "Not downloaded"
            print(f"{v['name']:<35} {v['lang']:<8} {v['gender']:<8} {v['quality']:<8} {v['size_mb']:<8} {status}")
        sys.exit(0)

    if not args.text:
        print("Error: Provide text to synthesize, or use --list-voices")
        print('Example: python tts_engine.py "Hello world"')
        sys.exit(1)

    output = synthesize(args.text, model_name=args.model, output_path=args.output)
    print(f"\nOutput file: {output}")
