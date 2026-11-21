"""Fetch Reina-Valera 1909 (scrollmapper SpaRV) and save Genesis..Exodus chapters as JSON in out/."""
import json
import os
import urllib.request

def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "x"}), timeout=120).read()

base = "https://raw.githubusercontent.com/scrollmapper/bible_databases/master/"
print(get(base + "sources/es/SpaRV/README.md").decode()[:800])
data = json.loads(get(base + "formats/json/SpaRV.json"))
print(type(data), list(data)[:5] if isinstance(data, dict) else len(data))
books = data["books"] if isinstance(data, dict) else data
os.makedirs("out", exist_ok=True)
keep = {}
for b in books:
    if b["name"] in ("Genesis", "Exodus"):
        keep[b["name"]] = {c["chapter"]: [v["text"] for v in c["verses"]] for c in b["chapters"]}
print({k: len(v) for k, v in keep.items()})
print(keep["Genesis"][1][0])
print(keep["Genesis"][31][0])
json.dump(keep, open("out/gen_exo.json", "w"), ensure_ascii=False)
