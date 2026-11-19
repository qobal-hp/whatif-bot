"""Turn chosen Voice Design previews into permanent voices and print their ids.

usage: python karma/create_voices.py <designs.json> <picks, e.g. serpent=1,eve=1> <name prefix>
"""
import json
import os
import sys
import urllib.request

API = "https://api.elevenlabs.io/v1"
KEY = os.environ["ELEVENLABS_API_KEY"]
designs = json.load(open(sys.argv[1]))
picks = dict(p.split("=") for p in sys.argv[2].split(","))
prefix = sys.argv[3]
for role, n in picks.items():
    d = designs[role]
    body = json.dumps({"voice_name": f"{prefix} {role.title()}", "voice_description": d["description"],
                       "generated_voice_id": d["previews"][int(n) - 1]}).encode()
    req = urllib.request.Request(f"{API}/text-to-voice", data=body, headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    try:
        voice = json.load(urllib.request.urlopen(req, timeout=120))
        print(f"VOICE {role}={voice['voice_id']}")
    except urllib.error.HTTPError as err:
        print(f"FAILED {role}: {err.code} {err.read()[:300]}")
