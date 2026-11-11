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

# Voices to render this round: name prefix -> fallback voice_id.
WANTED = {
    "Alice": "Xb7hH8MSUJpSbSDYk3k2",
    "Matilda": "XrExE9yKIg1WjnnlVkGX",
    "Lily": "pFZP5JQG7iQjIQuC34CR",
}


def list_voices() -> list:
    req = urllib.request.Request(
        "https://api.elevenlabs.io/v1/voices", headers={"xi-api-key": API_KEY}
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.load(resp).get("voices", [])
    except urllib.error.HTTPError as err:
        print(f"Could not list voices: HTTP {err.code} {err.read().decode(errors='replace')[:200]}")
        return []


def resolve_voices() -> dict:
    available = list_voices()
    for v in available:
        print("VOICE", json.dumps({"name": v.get("name"), "labels": v.get("labels"), "description": v.get("description")}))
    voices = {}
    for i, (name, fallback) in enumerate(WANTED.items(), start=1):
        match = next((v["voice_id"] for v in available if v.get("name", "").startswith(name)), fallback)
        voices[f"{i}_{name}"] = match
    return voices


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
    voices = resolve_voices()
    for name, voice_id in voices.items():
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
    print(f"{made} of {len(voices)} voices rendered")
    return 0 if made else 1


if __name__ == "__main__":
    sys.exit(main())
