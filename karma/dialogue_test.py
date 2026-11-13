"""Compare ways of voicing one dramatic exchange: the whole scene generated as one conversation
(ElevenLabs Text to Dialogue) with acting directions, on the newest model and on v3.

usage: python karma/dialogue_test.py <out dir>
"""
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

API = "https://api.elevenlabs.io/v1"
KEY = os.environ["ELEVENLABS_API_KEY"]
CAST = {"NARRATOR": "Brian", "CLAIRE": "Sarah", "DANIEL": "Will", "VANESSA": "Laura", "RICHARD": "Bill"}
SCENE = [
    ["NARRATOR", "The screen went black. A text message appeared. \"I can't wait until she's out of the picture.\" The laughter died. All at once."],
    ["VANESSA", "[panicked] That's fake! Claire, somebody is messing with you!"],
    ["DANIEL", "[low, furious] Claire. Turn that off. Right now."],
    ["CLAIRE", "[calm, amused] Why? We're just getting to the good part."],
    ["DANIEL", "[shouting] This is our WEDDING!"],
    ["CLAIRE", "[coldly] Exactly. And I wanted all two hundred of our closest friends to see what kind of man I married."],
    ["NARRATOR", "Daniel lunged for the projector remote. Claire didn't move."],
    ["CLAIRE", "[quietly] Don't bother. I have backups."],
    ["RICHARD", "[stern, threatening] Young lady, I strongly suggest you turn that projector off."],
    ["CLAIRE", "[sweetly] Why, Richard? Is there something inaccurate?"],
]


def voices():
    req = urllib.request.Request(f"{API}/voices", headers={"xi-api-key": KEY})
    found = json.load(urllib.request.urlopen(req, timeout=60)).get("voices", [])
    return {role: next(v["voice_id"] for v in found if v["name"].split(" ")[0] == name) for role, name in CAST.items()}


def dialogue(ids, model):
    body = json.dumps({"inputs": [{"text": text, "voice_id": ids[role]} for role, text in SCENE], "model_id": model}).encode()
    req = urllib.request.Request(
        f"{API}/text-to-dialogue/with-timestamps?output_format=mp3_44100_128",
        data=body,
        headers={"xi-api-key": KEY, "Content-Type": "application/json"},
    )
    try:
        data = json.load(urllib.request.urlopen(req, timeout=600))
    except urllib.error.HTTPError as err:
        print(f"{model}: HTTP {err.code} {err.read()[:400].decode(errors='replace')}")
        return None
    print(model, "keys:", sorted(data.keys()))
    segs = data.get("voice_segments") or []
    print(model, "segments:", len(segs), "first:", json.dumps(segs[0]) if segs else None)
    al = data.get("alignment") or {}
    chars = al.get("characters") or []
    print(model, "alignment chars:", len(chars), "sample:", "".join(chars[:90]).replace("\n", " "))
    return base64.b64decode(data["audio_base64"])


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    ids = voices()
    for model in ["eleven_v4", "eleven_v3"]:
        audio = dialogue(ids, model)
        if audio:
            (out / f"dialogue_{model}.mp3").write_bytes(audio)
            print("OK", f"dialogue_{model}.mp3", len(audio) // 1024, "KB")


if __name__ == "__main__":
    main()
