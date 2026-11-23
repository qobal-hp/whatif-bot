import json, re, urllib.request
def get(u): return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read()
txt = get("https://evolink.ai/docs/_llms/en/api-manual.txt").decode()
for line in txt.splitlines():
    if re.search(r"file|upload|task-detail", line, re.I): print("LINE", line[:200])
for p in re.findall(r"\((/docs/en/api-manual/(?:file-management|task-management)/[^)]+\.json)\)", txt)[:6]:
    d = json.loads(get("https://evolink.ai" + p))
    for path, ops in d.get("paths", {}).items():
        for m, op in ops.items():
            print("==", m.upper(), path, d.get("servers", [{}])[0].get("url", ""))
            rb = op.get("requestBody", {}).get("content", {})
            for ct, c in rb.items():
                s = c.get("schema", {})
                if "$ref" in s: s = d["components"]["schemas"][s["$ref"].split("/")[-1]]
                print("  CT", ct, {k: (v.get("type"), str(v.get("description", ""))[:80]) for k, v in s.get("properties", {}).items()})
            for code, r in op.get("responses", {}).items():
                c = r.get("content", {}).get("application/json", {})
                s = c.get("schema", {})
                if "$ref" in s: s = d["components"]["schemas"][s["$ref"].split("/")[-1]]
                print("  RESP", code, json.dumps(c.get("example", ""))[:600], list(s.get("properties", {}))[:20])
