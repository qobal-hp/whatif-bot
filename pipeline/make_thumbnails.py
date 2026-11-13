"""Generate thumbnail background images and the props for the Remotion "Thumb" composition.

usage: python pipeline/make_thumbnails.py <spec.json>
Writes video/public/thumbs/<id>.jpg and <id>.json.
"""
import base64
import json
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import fal_client

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "video" / "public" / "thumbs"


def make(spec, thumb):
    last = None
    for _ in range(3):
        try:
            args = {"prompt": spec["thumbnail_style"] + thumb["image"], "aspect_ratio": "16:9", "resolution": "2K", "output_format": "jpeg"}
            model = "fal-ai/nano-banana-2"
            if thumb.get("ref"):
                # Keep a recurring character's face: pass their portrait to the edit model.
                ref = ROOT / thumb["ref"]
                args["image_urls"] = ["data:image/jpeg;base64," + base64.b64encode(ref.read_bytes()).decode()]
                model = "fal-ai/nano-banana-2/edit"
            image = fal_client.subscribe(model, arguments=args)
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
