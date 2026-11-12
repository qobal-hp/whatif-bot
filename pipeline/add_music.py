"""Add background music cues to an episode's props.

usage: python pipeline/add_music.py <spec.json> <props.json>
The spec lists [scene id, track] pairs; each track plays from that scene until the next cue.
"""
import json
import sys
from pathlib import Path

# Tracks are normalised to the same loudness before this runs; 0.14 keeps them well under the voice.
VOLUME = {"tension": 0.14, "wonder": 0.14}


def main():
    spec = json.loads(Path(sys.argv[1]).read_text())
    path = Path(sys.argv[2])
    props = json.loads(path.read_text())
    starts = {s["id"]: s["start"] for s in props["scenes"]}
    cues = [(starts[scene], track) for scene, track in spec.get("music", [])]
    props["music"] = [
        {
            "src": f"assets/music_{track}.mp3",
            "start": start,
            "end": cues[i + 1][0] if i + 1 < len(cues) else props["durationSec"],
            "volume": VOLUME.get(track, 0.15),
        }
        for i, (start, track) in enumerate(cues)
    ]
    path.write_text(json.dumps(props))
    print(f"{len(props['music'])} music cues added")


if __name__ == "__main__":
    main()
