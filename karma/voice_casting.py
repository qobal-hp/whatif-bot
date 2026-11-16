"""Generate concert crowd sound effects with ElevenLabs (temporary use of the voice-casting workflow).

usage: python karma/voice_casting.py <unused spec> <out dir>
"""
import json
import os
import sys
import urllib.request
from pathlib import Path

KEY = os.environ["ELEVENLABS_API_KEY"]
SOUNDS = {
    "cheer_big": ("Huge arena concert crowd erupting in loud cheering, screaming and whistling as the show starts, thousands of fans", 12),
    "cheer_end": ("Massive arena crowd cheering, applauding wildly and whistling at the end of a song, encore energy", 12),
    "crowd_bed": ("Continuous distant arena concert crowd ambience, steady excited murmur, occasional whoops and claps, no music", 22),
    "clap_along": ("Big concert crowd clapping along in rhythm to a song, arena reverb", 15),
    "kids_cheer": ("Large audience of parents and families cheering and clapping enthusiastically for children performing, big hall", 10),
}


def main():
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    for name, (text, sec) in SOUNDS.items():
        req = urllib.request.Request("https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_192", method="POST",
                                     headers={"xi-api-key": KEY, "Content-Type": "application/json"},
                                     data=json.dumps({"text": text, "duration_seconds": sec, "prompt_influence": 0.5}).encode())
        with urllib.request.urlopen(req, timeout=180) as resp:
            (out / f"{name}.mp3").write_bytes(resp.read())
        print("made", name)
    (out / "casting.json").write_text("{}")


if __name__ == "__main__":
    main()
