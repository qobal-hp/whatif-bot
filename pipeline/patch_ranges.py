"""Print the frame ranges that must be re-rendered when some scenes change.

Usage: patch_ranges.py props.json s32,s97
Each range covers the scene plus a one-second margin, so the fades into and out of it are redrawn too.
Overlapping ranges are merged. Output: one "first last" pair per line.
"""
import json, sys

props = json.load(open(sys.argv[1]))
ids = {s.strip() for s in sys.argv[2].split(",") if s.strip()}
fps = props["fps"]
last_frame = round(props["durationSec"] * fps) - 1
ranges = []
for i, scene in enumerate(props["scenes"]):
    if scene["id"] in ids:
        a = max(0, round(scene["start"] * fps) - fps)
        b = min(last_frame, round(scene["end"] * fps) + fps)
        ranges.append([a, b])
missing = ids - {s["id"] for s in props["scenes"]}
if missing:
    sys.exit(f"Unknown scene ids: {', '.join(sorted(missing))}")
ranges.sort()
merged = []
for a, b in ranges:
    if merged and a <= merged[-1][1] + 1:
        merged[-1][1] = max(merged[-1][1], b)
    else:
        merged.append([a, b])
for a, b in merged:
    print(a, b)
