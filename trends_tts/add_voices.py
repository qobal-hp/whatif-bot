"""Add named ElevenLabs library voices to this account (needs voices_write) and print their ids."""
import json, os, sys, urllib.error, urllib.parse, urllib.request
API = "https://api.elevenlabs.io/v1"; KEY = os.environ["ELEVENLABS_API_KEY"]
def call(method, path, body=None):
    req = urllib.request.Request(f"{API}{path}", method=method, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r: return json.load(r)
wanted = json.loads(sys.argv[1])  # {"language": "hi", "names": {"TR-HI-Arjun": "Arjun - Indian Hinglish", ...}}
have = {v["name"]: v["voice_id"] for v in call("GET", "/voices")["voices"]}
q = urllib.parse.urlencode({"language": wanted["language"], "gender": "male", "page_size": 100})
lib = call("GET", f"/shared-voices?{q}").get("voices", [])
ok = 0
for new_name, prefix in wanted["names"].items():
    if new_name in have: print("ALREADY", new_name, have[new_name]); ok += 1; continue
    v = next((v for v in lib if v.get("name", "").startswith(prefix)), None)
    if not v: print("NOT FOUND", prefix); continue
    try:
        vid = call("POST", f"/voices/add/{v['public_owner_id']}/{v['voice_id']}", {"new_name": new_name})["voice_id"]
        print("ADDED", new_name, vid); ok += 1
    except urllib.error.HTTPError as e:
        print("FAILED", new_name, e.code, e.read().decode(errors="replace")[:200])
sys.exit(0 if ok else 1)
