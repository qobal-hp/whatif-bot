"""Swap re-rendered stretches into a finished episode without re-encoding the rest.

Usage: splice.py old.mp4 props.json ranges.txt workdir render_cmd
For each frame range, the stretch is widened to the original video's keyframes, so the
untouched parts can be copied byte for byte. render_cmd is called as: render_cmd FIRST LAST OUT.mp4
and must write an H.264 clip with the same size and frame rate. The sound is copied unchanged.
"""
import json, subprocess, sys
from pathlib import Path

old, props, ranges, work, render = sys.argv[1], sys.argv[2], sys.argv[3], Path(sys.argv[4]), sys.argv[5]
fps = json.load(open(props))["fps"]
work.mkdir(parents=True, exist_ok=True)

out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-skip_frame", "nokey", "-show_entries",
                      "frame=pts_time", "-of", "csv=p=0", old], capture_output=True, text=True, check=True).stdout
keys = sorted({round(float(t) * fps) for t in out.replace(",", " ").split() if t.strip()})
total = int(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets", "-show_entries",
                            "stream=nb_read_packets", "-of", "csv=p=0", old], capture_output=True, text=True, check=True).stdout.strip())

spans = []
for line in Path(ranges).read_text().split("\n"):
    if not line.strip():
        continue
    a, b = map(int, line.split())
    start = max(k for k in keys if k <= a)
    after = [k for k in keys if k > b]
    end = after[0] if after else total  # first frame that is kept from the old video
    if spans and start <= spans[-1][1]:
        spans[-1][1] = max(spans[-1][1], end)
    else:
        spans.append([start, end])

# Cut the old picture at every span edge in one pass; the edges are keyframes, so the cut is exact.
edges = sorted({e for span in spans for e in span if 0 < e < total})
pieces = work / "old"
pieces.mkdir(exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", old, "-map", "0:v", "-c", "copy", "-f", "segment",
                "-segment_frames", ",".join(map(str, edges)), "-reset_timestamps", "1", str(pieces / "p%04d.mp4")], check=True)
bounds = [0, *edges, total]

parts = []
for i, (first, stop) in enumerate(zip(bounds, bounds[1:])):
    if any(s <= first and stop <= e for s, e in spans):
        new = work / f"new{i:04d}.mp4"
        print(f"Re-rendering frames {first}-{stop - 1}", flush=True)
        subprocess.run([*render.split(), str(first), str(stop - 1), str(new)], check=True)
        parts.append(new)
    else:
        parts.append(pieces / f"p{i:04d}.mp4")

(work / "list.txt").write_text("".join(f"file '{p.resolve()}'\n" for p in parts))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(work / "list.txt"), "-i", old,
                "-map", "0:v", "-map", "1:a", "-c", "copy", "-movflags", "+faststart", str(work / "episode.mp4")], check=True)
print("Spliced", len(spans), "stretches into", work / "episode.mp4")
