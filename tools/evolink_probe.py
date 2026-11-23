"""Print EvoLink model ids and prices relevant to us (runs on the Actions runner)."""
import json
import re
import urllib.request


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read()


cat = json.loads(get("https://api.evolink.ai/web/api/models/pricing"))
text = json.dumps(cat, ensure_ascii=False)
print("TOP KEYS", list(cat)[:10] if isinstance(cat, dict) else type(cat))
items = cat.get("data", cat) if isinstance(cat, dict) else cat
if isinstance(items, dict):
    items = items.get("models", items.get("list", list(items.values())))
for m in items if isinstance(items, list) else []:
    s = json.dumps(m, ensure_ascii=False)
    if re.search(r"banana|gemini.*image|kling|seedance-2\.5|suno", s, re.I):
        print(s[:400])
for path in ["https://evolink.ai/docs/llms.txt"]:
    try:
        t = get(path).decode()
        for line in t.splitlines():
            if re.search(r"banana|kling|suno|task", line, re.I):
                print("DOC", line[:200])
    except Exception as err:
        print("DOC ERR", err)
