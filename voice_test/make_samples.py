"""Render the same script excerpt with several ElevenLabs voices for comparison."""
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

API_KEY = os.environ["ELEVENLABS_API_KEY"]
HERE = Path(__file__).parent
OUT = HERE / "output"
TEXT = (HERE / "sample_text.txt").read_text(encoding="utf-8").strip()

# ElevenLabs default (premade) voices suited to documentary narration.
VOICES = {
    "1_George": "JBFqnCBsd6RMkjVDRZzb",
    "2_Brian": "nPczCjzI2devNBz1zQrb",
    "3_Daniel": "onwK4e9ZLuTAKqWW03F9",
    "4_Bill": "pqHfZKP75CVOlQylNhV4",
}
MODELS = ["eleven_v3", "eleven_multilingual_v2"]  # try v3 first, then fall back


def synth(voice_id: str, model_id: str) -> bytes:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format=mp3_44100_128"
    body = json.dumps({"text": TEXT, "model_id": model_id}).encode()
    req = urllib.request.Request(
        url,
        data=body,
        headers={"xi-api-key": API_KEY, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        return resp.read()


def main() -> int:
    OUT.mkdir(exist_ok=True)
    made = 0
    for name, voice_id in VOICES.items():
        for model_id in MODELS:
            try:
                audio = synth(voice_id, model_id)
            except urllib.error.HTTPError as err:
                detail = err.read().decode(errors="replace")[:300]
                print(f"FAILED {name} / {model_id}: HTTP {err.code} {detail}")
                continue
            path = OUT / f"{name}_{model_id}.mp3"
            path.write_bytes(audio)
            print(f"OK {path.name} ({len(audio) // 1024} KB)")
            made += 1
            break
    print(f"{made} of {len(VOICES)} voices rendered")
    return 0 if made else 1


if __name__ == "__main__":
    sys.exit(main())
