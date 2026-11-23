import urllib.request
def get(u): return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read().decode()
for p in ["file-series/upload-stream.md", "task-management/get-task-detail.md", "image-series/nanobanana/nanobanana-2/nanobanana-2-image-generate.md"]:
    t = get("https://evolink.ai/docs/en/api-manual/" + p)
    print("=====", p, len(t))
    for line in t.splitlines():
        s = line.strip()
        if s and not s.startswith(("|---", "<")) and len(s) < 220:
            print("D", s)
