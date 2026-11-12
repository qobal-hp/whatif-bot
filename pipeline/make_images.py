"""Generate a small set of standalone images (logos, banners) from a JSON list.

usage: python pipeline/make_images.py <list.json> <out dir>
"""
import json
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import fal_client


def make(style, item, out):
    last = None
    for _ in range(3):
        try:
            image = fal_client.subscribe(
                "fal-ai/nano-banana-2",
                arguments={
                    "prompt": style + item["prompt"],
                    "aspect_ratio": item.get("aspect", "1:1"),
                    "resolution": "1K",
                    "output_format": "png",
                },
            )
            urllib.request.urlretrieve(image["images"][0]["url"], out / f"{item['id']}.png")
            print(f"{item['id']} done")
            return
        except Exception as err:
            last = err
            print(f"{item['id']} attempt failed: {err}")
    raise SystemExit(f"{item['id']} failed three times: {last}")


def main():
    spec = json.loads(Path(sys.argv[1]).read_text())
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(4) as pool:
        list(pool.map(lambda i: make(spec["style"], i, out), spec["images"]))


if __name__ == "__main__":
    main()
