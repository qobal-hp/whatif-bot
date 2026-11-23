"""Print request/response schemas of the EvoLink endpoints we need (runs on the Actions runner)."""
import json
import urllib.request

def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read()

for p in ["image-series/nanobanana/nanobanana-2/nanobanana-2-image-generate.json",
          "video-series/kling/kling-v3-image-to-video.json",
          "video-series/seedance2.5/seedance-2.5-image-to-video.json"]:
    try:
        d = json.loads(get("https://evolink.ai/docs/en/api-manual/" + p))
    except Exception as err:
        print("ERR", p, err); continue
    for path, ops in d.get("paths", {}).items():
        for m, op in ops.items():
            print("==", p, m.upper(), path)
            body = op.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema", {})
            def walk(s, pre=""):
                if "$ref" in s:
                    ref = s["$ref"].split("/")[-1]; s = d["components"]["schemas"][ref]
                for k, v in s.get("properties", {}).items():
                    if "$ref" in v: v = d["components"]["schemas"][v["$ref"].split("/")[-1]]
                    print(f"  {pre}{k}: {v.get('type')} {str(v.get('enum', ''))[:80]} {str(v.get('default', ''))[:30]} | {str(v.get('description', ''))[:110]}")
                    if v.get("type") == "object" and pre.count(".") < 1:
                        walk(v, pre + k + ".")
                req = s.get("required")
                if req: print(f"  {pre}required: {req}")
            walk(body)
            for code, r in op.get("responses", {}).items():
                ex = json.dumps(r.get("content", {}).get("application/json", {}).get("example", r.get("content", {}).get("application/json", {}).get("examples", "")))[:500]
                print("  RESP", code, ex)
t = json.loads(get("https://evolink.ai/docs/en/api-manual/task-management/get-task-detail.json")) if False else None
try:
    txt = get("https://evolink.ai/docs/_llms/en/api-manual.txt").decode()
    import re
    for line in txt.splitlines():
        if re.search(r"task", line, re.I) and ".json" in line: print("TASKDOC", line[:200])
except Exception as err:
    print("ERR manual", err)
