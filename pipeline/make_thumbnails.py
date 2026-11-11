"""Generate thumbnail background images and the props for the Remotion "Thumb" composition.

usage: python pipeline/make_thumbnails.py <spec.json>
Writes video/public/thumbs/<id>.jpg and <id>.json.
"""
import json
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import fal_client

OUT = Path(__file__).resolve().parent.parent / "video" / "public" / "thumbs"


def make(spec, thumb):
    last = None
    for _ in range(3):
        try:
            image = fal_client.subscribe(
                "fal-ai/nano-banana-2",
                arguments={
                    "prompt": spec["thumbnail_style"] + thumb["image"],
                    "aspect_ratio": "16:9",
                    "resolution": "2K",
                    "output_format": "jpeg",
                },
            )
            urllib.request.urlretrieve(image["images"][0]["url"], OUT / f"{thumb['id']}.jpg")
            props = {"image": f"thumbs/{thumb['id']}.jpg", "side": thumb["side"], "lines": thumb["lines"], "tag": thumb.get("tag", "")}
            (OUT / f"{thumb['id']}.json").write_text(json.dumps(props))
            print(f"{thumb['id']} done")
            return
        except Exception as err:
            last = err
            print(f"{thumb['id']} attempt failed: {err}")
    raise SystemExit(f"{thumb['id']} failed three times: {last}")


def main():
    spec = json.loads(Path(sys.argv[1]).read_text())
    OUT.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(4) as pool:
        list(pool.map(lambda t: make(spec, t), spec["thumbnails"]))


if __name__ == "__main__":
    main()
