"""Find a Reina-Valera 1909 source and print what it holds (run on the Actions runner)."""
import json
import urllib.request

def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "x"}), timeout=60).read()

tree = json.loads(get("https://api.github.com/repos/scrollmapper/bible_databases/git/trees/master?recursive=1"))
names = [t["path"] for t in tree["tree"] if "spa" in t["path"].lower() or "rv" in t["path"].lower()]
print("\n".join(names[:80]))
