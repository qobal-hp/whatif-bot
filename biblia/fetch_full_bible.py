"""Save the whole Reina-Valera 1909 (scrollmapper SpaRV) as out/rv1909.json: {book: {chapter: [verses]}}."""
import json
import os
import urllib.request

url = "https://raw.githubusercontent.com/scrollmapper/bible_databases/master/formats/json/SpaRV.json"
data = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "x"}), timeout=120).read())
books = data["books"] if isinstance(data, dict) else data
bible = {b["name"]: {str(c["chapter"]): [v["text"] for v in c["verses"]] for c in b["chapters"]} for b in books}
os.makedirs("out", exist_ok=True)
json.dump(bible, open("out/rv1909.json", "w"), ensure_ascii=False)
print(len(bible), "books;", sum(len(c) for b in bible.values() for c in b.values()), "verses")
print(list(bible)[:5], list(bible)[-5:])
