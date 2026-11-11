"""Cut vertical shorts out of an already generated episode. No new audio or images are made.

usage: python pipeline/make_shorts.py <spec.json> <episode props.json> <out dir>
Writes one props file per short (<id>.json) for the Remotion "Short" composition.
"""
import json
import sys
from pathlib import Path


def main():
    spec = json.loads(Path(sys.argv[1]).read_text())
    props = json.loads(Path(sys.argv[2]).read_text())
    out = Path(sys.argv[3])
    out.mkdir(parents=True, exist_ok=True)
    ids = [s["id"] for s in props["scenes"]]
    for short in spec["shorts"]:
        scenes = props["scenes"][ids.index(short["from"]): ids.index(short["to"]) + 1]
        start, end = scenes[0]["start"], scenes[-1]["end"]
        cut = {
            "fps": props["fps"],
            "durationSec": round(end - start, 3),
            "audio": props["audio"],
            "audioStart": start,
            "title": short["title"],
            "scenes": [dict(s, start=s["start"] - start, end=s["end"] - start) for s in scenes],
            "words": [
                dict(w, start=w["start"] - start, end=w["end"] - start)
                for w in props["words"]
                if start - 0.01 <= w["start"] < end
            ],
        }
        (out / f"{short['id']}.json").write_text(json.dumps(cut))
        print(f"{short['id']}: {cut['durationSec']}s, {len(scenes)} scenes, {len(cut['words'])} words")


if __name__ == "__main__":
    main()
