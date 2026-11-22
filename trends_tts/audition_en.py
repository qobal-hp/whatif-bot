"""Audition young, upbeat American voices for trend-news Shorts: renders the same script per voice with timestamps."""
import base64, json, os, sys, urllib.error, urllib.parse, urllib.request
from pathlib import Path
API = "https://api.elevenlabs.io/v1"; KEY = os.environ["ELEVENLABS_API_KEY"]
def call(method, path, body=None):
    req = urllib.request.Request(f"{API}{path}", method=method, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r: return json.load(r)
GOOD = ["social media", "social_media", "youtube", "tiktok", "upbeat", "energetic", "hype", "excited", "host", "presenter",
        "news", "entertainment", "pop culture", "trend", "reels", "shorts", "vlog", "conversational", "young", "bright"]
BAD = ["documentary", "calm", "meditation", "audiobook", "asmr", "deep", "narrator", "soothing", "old", "british", "whisper", "villain"]
def score(v):
    t = " ".join(str(v.get(k, "")) for k in ("name", "description", "use_case", "descriptive", "age", "accent")).lower()
    return sum(w in t for w in GOOD) * 3 - sum(w in t for w in BAD) * 4 + min(v.get("cloned_by_count", 0) or 0, 20000) / 5000
cfg = json.loads(Path(sys.argv[1]).read_text()); out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
picked = []
for gender in ("female", "male"):
    pool = {}
    for extra in ({}, {"use_cases": "social_media"}, {"search": "youtube energetic"}):
        q = urllib.parse.urlencode({"language": "en", "gender": gender, "age": "young", "page_size": 100, **extra})
        try:
            for v in call("GET", f"/shared-voices?{q}").get("voices", []): pool[v["voice_id"]] = v
        except urllib.error.HTTPError as e: print("SEARCH FAILED", extra, e.code)
    vs = [v for v in pool.values() if (v.get("accent") or "american").lower() in ("american", "standard", "us", "")]
    vs.sort(key=score, reverse=True)
    for v in vs[:8]:
        print("CAND", gender, json.dumps({k: v.get(k) for k in ("name", "accent", "age", "use_case", "descriptive", "cloned_by_count")}))
    picked += [(gender[0] + str(i + 1), v) for i, v in enumerate(vs[:2])]
have = {v["name"]: v["voice_id"] for v in call("GET", "/voices")["voices"]}
meta = {}
for tag, v in picked:
    name = f"TR-EN-{v['name'].split(' ')[0]}"[:40]
    vid = have.get(name)
    if not vid:
        try: vid = call("POST", f"/voices/add/{v['public_owner_id']}/{v['voice_id']}", {"new_name": name})["voice_id"]
        except urllib.error.HTTPError as e: print("ADD FAILED", name, e.code); vid = v["voice_id"]
    res = call("POST", f"/text-to-speech/{vid}/with-timestamps?output_format=mp3_44100_192",
               {"text": cfg["text_v3"], "model_id": "eleven_v3", "voice_settings": cfg.get("settings", {})})
    (out / f"{tag}.mp3").write_bytes(base64.b64decode(res["audio_base64"]))
    (out / f"{tag}.json").write_text(json.dumps({"voice_id": vid, "voice_name": v["name"], "saved_as": name,
        "description": v.get("description"), "text": cfg["text_v3"], "alignment": res["alignment"]}))
    meta[tag] = {"name": v["name"], "saved_as": name, "descriptive": v.get("descriptive"), "use_case": v.get("use_case"), "description": (v.get("description") or "")[:200]}
    print("OK", tag, v["name"])
(out / "candidates.json").write_text(json.dumps(meta, indent=2))
