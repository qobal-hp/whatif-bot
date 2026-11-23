"""Make the narration for a trends-v2 job with ElevenLabs (mp3 + character timestamps).

usage: python trends/tts.py <job dir> <out dir>    (needs ELEVENLABS_API_KEY)
The voice is chosen from trends/voices.json by country and voice_style.
"""
import base64, json, os, sys, urllib.error, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from common import load_job, narration_text  # noqa: E402

API = "https://api.elevenlabs.io/v1"
STABILITY = {"sports": 0.0, "pop_culture": 0.0, "lifestyle_viral": 0.0, "tech_business": 0.5, "serious_news": 0.5}


def call(method, path, body=None):
    req = urllib.request.Request(f"{API}{path}", method=method, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)


def pick_voice(prod):
    table = json.loads((Path(__file__).resolve().parent / "voices.json").read_text())
    ch = table.get(prod["country"], {})
    name = ch.get(prod.get("voice_style", "")) or ch.get("default")
    if not name:
        raise SystemExit(f"no voice configured for {prod['country']} in trends/voices.json")
    mine = {v["name"]: v["voice_id"] for v in call("GET", "/voices")["voices"]}
    if name not in mine:
        raise SystemExit(f"voice {name!r} is not in the ElevenLabs account (My Voices)")
    return name, mine[name]


def main(job_dir, out_dir):
    prod, _ = load_job(job_dir)
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    name, vid = pick_voice(prod)
    settings = {"stability": STABILITY.get(prod.get("voice_style"), 0.5), "similarity_boost": 0.8}
    last = None
    for model, text in (("eleven_v3", narration_text(prod, True)), ("eleven_multilingual_v2", narration_text(prod, False))):
        try:
            res = call("POST", f"/text-to-speech/{vid}/with-timestamps?output_format=mp3_44100_192",
                       {"text": text, "model_id": model, "voice_settings": settings})
        except urllib.error.HTTPError as e:
            last = f"{model}: HTTP {e.code} {e.read().decode(errors='replace')[:300]}"; print("FAILED", last); continue
        (out / "vo.mp3").write_bytes(base64.b64decode(res["audio_base64"]))
        (out / "vo.json").write_text(json.dumps({"voice": name, "model": model, "text": text, "alignment": res["alignment"]}, ensure_ascii=False))
        print(f"OK voice={name} model={model}")
        return 0
    raise SystemExit(f"narration failed: {last}")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
