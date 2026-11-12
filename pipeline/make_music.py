"""Generate instrumental background music with ElevenLabs.

usage: python pipeline/make_music.py <list.json> <out dir>
list.json: {"tracks": [{"id": "...", "prompt": "...", "seconds": 30}]}
"""
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

API = "https://api.elevenlabs.io/v1"
KEY = os.environ["ELEVENLABS_API_KEY"]


def credits():
    req = urllib.request.Request(f"{API}/user/subscription", headers={"xi-api-key": KEY})
    try:
        data = json.loads(urllib.request.urlopen(req, timeout=60).read())
        return data.get("tier"), data.get("character_count"), data.get("character_limit")
    except Exception as err:
        return None, None, f"unavailable ({err})"


def compose(prompt, seconds):
    last = None
    for model in ["music_v2", "music_v1"]:
        body = json.dumps(
            {"prompt": prompt, "music_length_ms": int(seconds * 1000), "model_id": model, "force_instrumental": True}
        ).encode()
        req = urllib.request.Request(
            f"{API}/music?output_format=mp3_44100_128",
            data=body,
            headers={"xi-api-key": KEY, "Content-Type": "application/json"},
        )
        try:
            return model, urllib.request.urlopen(req, timeout=600).read()
        except urllib.error.HTTPError as err:
            last = f"{model}: HTTP {err.code} {err.read()[:400].decode(errors='replace')}"
            print(last)
    raise SystemExit(f"Music generation failed: {last}")


def main():
    spec = json.loads(Path(sys.argv[1]).read_text())
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    print("Plan and credits before:", credits())
    for track in spec["tracks"]:
        model, audio = compose(track["prompt"], track["seconds"])
        (out / f"{track['id']}.mp3").write_bytes(audio)
        print(f"{track['id']}: {model}, {track['seconds']}s, {len(audio)} bytes; credits now:", credits())


if __name__ == "__main__":
    main()
