"""Check that sound effects can be generated with this API key.

usage: python karma/sfx_test.py <out dir>
"""
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

KEY = os.environ["ELEVENLABS_API_KEY"]
TESTS = {
    "glass_shatter": ("A champagne glass shattering on a marble floor", 2.0),
    "ballroom_murmur": ("Quiet murmur of a large crowd in an elegant ballroom, soft clinking of glasses, no music", 8.0),
}


def credits():
    req = urllib.request.Request("https://api.elevenlabs.io/v1/user/subscription", headers={"xi-api-key": KEY})
    try:
        d = json.load(urllib.request.urlopen(req, timeout=60))
        return d.get("character_count"), d.get("character_limit")
    except Exception as err:
        return None, str(err)[:80]


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    print("credits before:", credits())
    for name, (text, seconds) in TESTS.items():
        body = json.dumps({"text": text, "duration_seconds": seconds, "prompt_influence": 0.4}).encode()
        req = urllib.request.Request(
            "https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_128",
            data=body,
            headers={"xi-api-key": KEY, "Content-Type": "application/json"},
        )
        try:
            audio = urllib.request.urlopen(req, timeout=300).read()
        except urllib.error.HTTPError as err:
            print(f"FAILED {name}: HTTP {err.code} {err.read()[:300].decode(errors='replace')}")
            continue
        (out / f"sfx_{name}.mp3").write_bytes(audio)
        print(f"OK sfx_{name}.mp3 {len(audio) // 1024} KB; credits now:", credits())


if __name__ == "__main__":
    main()
