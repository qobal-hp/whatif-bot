"""Find natural-sounding voices in the ElevenLabs voice library and audition them on real lines.

usage: python karma/voice_casting.py karma/voice_casting.json <out dir>
For every role it searches the shared library (American English, the role's gender and age), adds the most-used
matches to the account under a unique one-word name (e.g. "EmilyB"), and renders the role's lines with each
voice through eleven_v3 so the audio tags ([sighs], [laughs] ...) are performed. Writes <role>_<name>.mp3 and
casting.json (name, voice id, library description) to the out dir.
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.elevenlabs.io/v1"
KEY = os.environ["ELEVENLABS_API_KEY"]


def call(method, path, body=None, raw=False):
    req = urllib.request.Request(f"{API}{path}", method=method, headers={"xi-api-key": KEY, "Content-Type": "application/json"},
                                 data=json.dumps(body).encode() if body is not None else None)
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = resp.read()
    return data if raw else json.loads(data)


def search(role):
    params = [("page_size", "40"), ("language", "en"), ("accent", "american"), ("gender", role["gender"]),
              ("age", role["age"]), ("sort", "usage_character_count_1y")]
    params += [("use_cases", u) for u in role.get("use_cases", [])]
    found = []
    for extra in ([("search", role["search"])], []):  # try with the search words first, then without
        try:
            found += call("GET", "/shared-voices?" + urllib.parse.urlencode(params + extra))["voices"]
        except urllib.error.HTTPError as err:
            print(f"search failed: HTTP {err.code} {err.read().decode(errors='replace')[:200]}")
        if len(found) >= 3:
            break
    seen, out = set(), []
    for v in found:
        if v["voice_id"] not in seen and v.get("category") != "famous":
            seen.add(v["voice_id"])
            out.append(v)
    return out


def existing():
    return {v["name"]: v["voice_id"] for v in call("GET", "/voices")["voices"]}


def add(voice, name, have):
    if name in have:
        return have[name]
    try:
        return call("POST", f"/voices/add/{voice['public_owner_id']}/{voice['voice_id']}", {"new_name": name})["voice_id"]
    except urllib.error.HTTPError as err:
        print(f"could not add {voice['name']} as {name}: HTTP {err.code} {err.read().decode(errors='replace')[:300]}")
        return None


def speak(voice_id, lines):
    body = {"inputs": [{"text": t, "voice_id": voice_id} for t in lines], "model_id": "eleven_v3"}
    for model in ("eleven_v4", "eleven_v3"):
        body["model_id"] = model
        try:
            return call("POST", "/text-to-dialogue?output_format=mp3_44100_128", body, raw=True)
        except urllib.error.HTTPError as err:
            print(f"{model}: HTTP {err.code} {err.read().decode(errors='replace')[:200]}")
    return None


def main():
    spec = json.loads(Path(sys.argv[1]).read_text())
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    have = existing()
    report = {}
    for role, cfg in spec["roles"].items():
        report[role] = []
        for n, voice in enumerate(search(cfg)[: spec.get("keep", 3)]):
            name = role.split("_")[0].capitalize() + "ABCDEFGH"[n] + ("F" if role.endswith("_F") else "")
            voice_id = add(voice, name, have)
            if not voice_id:
                continue
            audio = speak(voice_id, cfg["lines"])
            if audio:
                (out / f"{role}_{name}.mp3").write_bytes(audio)
            entry = {"name": name, "voice_id": voice_id, "library_name": voice["name"],
                     "description": (voice.get("description") or "")[:200], "descriptive": voice.get("descriptive"),
                     "use_case": voice.get("use_case"), "used_1y": voice.get("usage_character_count_1y")}
            report[role].append(entry)
            print(role, json.dumps(entry))
    (out / "casting.json").write_text(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
