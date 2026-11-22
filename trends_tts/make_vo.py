"""Render a Shorts narration with ElevenLabs, with character timestamps, for two voices.

usage: python trends_tts/make_vo.py trends_tts/lsu_tennessee.json <out dir>
Writes <voice>.mp3 and <voice>.json (alignment) per voice.
"""
import base64, json, os, sys, urllib.error, urllib.request
from pathlib import Path

API = "https://api.elevenlabs.io/v1"
KEY = os.environ["ELEVENLABS_API_KEY"]


def call(path, body=None):
    req = urllib.request.Request(f"{API}{path}", data=json.dumps(body).encode() if body else None,
                                 headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)


def main():
    cfg = json.loads(Path(sys.argv[1]).read_text())
    out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    have = {v["name"].split(" ")[0].lower(): v["voice_id"] for v in call("/voices")["voices"]}
    made = 0
    for name, fallback in cfg["voices"].items():
        vid = have.get(name.lower(), fallback)
        for model, text in ((m, cfg["text_v3"] if m == "eleven_v3" else cfg["text_plain"]) for m in cfg["models"]):
            try:
                res = call(f"/text-to-speech/{vid}/with-timestamps?output_format=mp3_44100_192",
                           {"text": text, "model_id": model, "voice_settings": cfg.get("settings", {})})
            except urllib.error.HTTPError as e:
                print(f"FAILED {name}/{model}: HTTP {e.code} {e.read().decode(errors='replace')[:300]}")
                continue
            (out / f"{name}.mp3").write_bytes(base64.b64decode(res["audio_base64"]))
            (out / f"{name}.json").write_text(json.dumps({"model": model, "voice_id": vid, "text": text,
                                                          "alignment": res.get("alignment"),
                                                          "normalized_alignment": res.get("normalized_alignment")}))
            print(f"OK {name} via {model}"); made += 1
            break
    return 0 if made else 1


if __name__ == "__main__":
    sys.exit(main())
