"""Narrator audition: the same opening of What If EP04 read by several narrators,
each on the newest dialogue model with acting directions, so they can be compared by ear.

usage: python karma/narrator_test.py <out dir>
"""
import base64
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

API = "https://api.elevenlabs.io/v1"
KEY = os.environ["ELEVENLABS_API_KEY"]
NARRATORS = ["George", "Brian", "Bill"]
LINES = [
    "[warm, unhurried] Imagine waking up tomorrow. You make your coffee. You pull back the curtains. You look out toward the ocean...",
    "[a beat, quieter] And there's no ocean.",
    "No waves. No blue line on the horizon. Just a dark, endless emptiness, falling away farther than you can see.",
    "[slow, awed] Imagine standing at that edge. Looking down into the dark. Knowing that yesterday, all of that was water.",
    "[quiet dread] But here's the terrifying part. The missing water isn't the disaster. It's only the beginning.",
]


def voice_id(name):
    req = urllib.request.Request(f"{API}/voices", headers={"xi-api-key": KEY})
    found = json.load(urllib.request.urlopen(req, timeout=60)).get("voices", [])
    return next(v["voice_id"] for v in found if v["name"].split(" ")[0] == name)


def read(vid):
    for model in ("eleven_v4", "eleven_v3"):
        body = json.dumps({"inputs": [{"text": t, "voice_id": vid} for t in LINES], "model_id": model}).encode()
        req = urllib.request.Request(f"{API}/text-to-dialogue?output_format=mp3_44100_128", data=body,
                                     headers={"xi-api-key": KEY, "Content-Type": "application/json"})
        try:
            return urllib.request.urlopen(req, timeout=300).read(), model
        except urllib.error.HTTPError as err:
            print(model, "failed:", err.code, err.read()[:300])
    raise SystemExit("no model worked")


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    for i, name in enumerate(NARRATORS, 1):
        raw, model = read(voice_id(name))
        tmp = out / f"raw{i}.mp3"
        tmp.write_bytes(raw)
        final = out / f"narrator{i}_{name}.mp3"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(tmp), "-af", "loudnorm=I=-16:TP=-1.5", "-b:a", "160k", str(final)], check=True)
        tmp.unlink()
        print(f"{final.name}: {model}")


if __name__ == "__main__":
    main()
