"""Audition a drama cast: render a short scene with one ElevenLabs voice per character.

usage: python karma/cast_audition.py karma/cast_audition.json <out dir>
Writes table_read.mp3 (the whole scene) plus one file per line, and one file per alternate voice.
"""
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

API = "https://api.elevenlabs.io/v1"
KEY = os.environ["ELEVENLABS_API_KEY"]


def voices():
    req = urllib.request.Request(f"{API}/voices", headers={"xi-api-key": KEY})
    found = json.load(urllib.request.urlopen(req, timeout=60)).get("voices", [])
    for v in found:
        print("VOICE", v.get("name"), "|", json.dumps(v.get("labels")))
    return found


def find(available, name):
    for v in available:
        if v.get("name", "").split(" ")[0].lower() == name.lower():
            return v["voice_id"]
    raise SystemExit(f"No voice named {name} in this account")


def speak(voice_id, text):
    last = None
    for model in ["eleven_v3", "eleven_multilingual_v2"]:
        body = json.dumps({"text": text, "model_id": model}).encode()
        req = urllib.request.Request(
            f"{API}/text-to-speech/{voice_id}?output_format=mp3_44100_128",
            data=body,
            headers={"xi-api-key": KEY, "Content-Type": "application/json"},
        )
        try:
            return urllib.request.urlopen(req, timeout=300).read()
        except urllib.error.HTTPError as err:
            last = f"{model}: HTTP {err.code} {err.read()[:200].decode(errors='replace')}"
            print(last)
    raise SystemExit(f"Speech failed: {last}")


def main():
    spec = json.loads(Path(sys.argv[1]).read_text())
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    available = voices()
    ids = {role: find(available, name) for role, name in spec["cast"].items()}

    parts = []
    for i, (role, text) in enumerate(spec["scene"], start=1):
        path = out / f"{i:02d}_{role}_{spec['cast'][role]}.mp3"
        path.write_bytes(speak(ids[role], text))
        parts.append(path)
        print("OK", path.name)

    # Join the lines with a short pause between speakers.
    inputs, chain = [], ""
    for i, p in enumerate(parts):
        inputs += ["-i", str(p)]
        chain += f"[{i}:a]aresample=44100,apad=pad_dur=0.35[a{i}];"
    chain += "".join(f"[a{i}]" for i in range(len(parts))) + f"concat=n={len(parts)}:v=0:a=1[out]"
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", chain, "-map", "[out]", "-b:a", "128k", str(out / "table_read.mp3")],
        check=True,
    )
    print("OK table_read.mp3")

    for role, names in spec.get("alternates", {}).items():
        line = next(text for r, text in spec["scene"] if r == role)
        for name in names:
            (out / f"alt_{role}_{name}.mp3").write_bytes(speak(find(available, name), line))
            print("OK", f"alt_{role}_{name}.mp3")


if __name__ == "__main__":
    main()
