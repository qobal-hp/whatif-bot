"""Find native Hindi male voices in the ElevenLabs library, add them, and render narration with timestamps.

usage: python trends_tts/make_vo_hi.py trends_tts/<job>.json <out dir>
"""
import base64, json, os, sys, urllib.error, urllib.parse, urllib.request
from pathlib import Path

API = "https://api.elevenlabs.io/v1"
KEY = os.environ["ELEVENLABS_API_KEY"]


def call(method, path, body=None):
    req = urllib.request.Request(f"{API}{path}", method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)


def pick(cfg):
    q = urllib.parse.urlencode({"language": cfg["language"], "gender": "male", "page_size": 40})
    found = call("GET", f"/shared-voices?{q}").get("voices", [])
    words = cfg["prefer_words"]
    def score(v):
        txt = " ".join(str(v.get(k, "")) for k in ("name", "description", "use_case", "descriptive", "accent")).lower()
        return (sum(w in txt for w in words), v.get("cloned_by_count", 0) or 0)
    found = [v for v in found if (v.get("accent") or "").lower() in ("", "standard", "indian", "hindi") or True]
    found.sort(key=score, reverse=True)
    want = cfg.get("prefer_names", [])
    if want:
        named = [v for n in want for v in found if v.get("name", "").startswith(n)]
        found = named + [v for v in found if v not in named]
    for v in found[:8]:
        print("CANDIDATE", json.dumps({k: v.get(k) for k in ("name", "accent", "age", "use_case", "descriptive", "description", "cloned_by_count")}, ensure_ascii=False))
    return found[: cfg["count"]]


def main():
    cfg = json.loads(Path(sys.argv[1]).read_text())
    out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    have = {v["name"]: v["voice_id"] for v in call("GET", "/voices")["voices"]}
    made = 0
    for i, v in enumerate(pick(cfg), 1):
        name = f"TR-HI-{v['name']}"[:40]
        vid = have.get(name)
        if not vid:
            try:
                vid = call("POST", f"/voices/add/{v['public_owner_id']}/{v['voice_id']}", {"new_name": name})["voice_id"]
            except urllib.error.HTTPError as e:
                print(f"ADD FAILED {name}: HTTP {e.code} -> trying the library voice id directly")
                vid = v["voice_id"]
        for model in cfg["models"]:
            text = cfg["text_v3"] if model == "eleven_v3" else cfg["text_plain"]
            try:
                res = call("POST", f"/text-to-speech/{vid}/with-timestamps?output_format=mp3_44100_192",
                           {"text": text, "model_id": model, "voice_settings": cfg.get("settings", {})})
            except urllib.error.HTTPError as e:
                print(f"FAILED {name}/{model}: HTTP {e.code} {e.read().decode(errors='replace')[:300]}"); continue
            tag = f"hi{i}"
            (out / f"{tag}.mp3").write_bytes(base64.b64decode(res["audio_base64"]))
            (out / f"{tag}.json").write_text(json.dumps({"model": model, "voice_id": vid, "voice_name": v["name"],
                "description": v.get("description"), "text": text, "alignment": res.get("alignment")}, ensure_ascii=False))
            print(f"OK {tag} {v['name']} via {model}"); made += 1
            break
    return 0 if made else 1


if __name__ == "__main__":
    sys.exit(main())
