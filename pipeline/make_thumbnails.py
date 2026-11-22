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

import os
import urllib.error

try:
    import fal_client
except ImportError:
    fal_client = None

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "video" / "public" / "thumbs"


GEMINI_MODELS = ["gemini-3-pro-image-preview", "gemini-3.1-flash-image-preview", "gemini-2.5-flash-image"]


def gemini_image(prompt, refs):
    """Make one 16:9 image with Gemini (Nano Banana), passing the reference portraits."""
    parts = [{"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode((ROOT / r).read_bytes()).decode()}} for r in refs]
    parts.append({"text": prompt})
    body = {"contents": [{"parts": parts}],
            "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "16:9"}}}
    last = None
    for model in GEMINI_MODELS:
        req = urllib.request.Request(
            f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
            data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": os.environ["GEMINI_API_KEY"]})
        try:
            out = json.loads(urllib.request.urlopen(req, timeout=180).read())
        except urllib.error.HTTPError as err:
            last = f"{model}: {err.code} {err.read()[:300]}"
            print(last)
            continue
        for part in out["candidates"][0]["content"]["parts"]:
            data = part.get("inlineData") or part.get("inline_data")
            if data:
                print(f"made with {model}")
                return base64.b64decode(data["data"])
        last = f"{model}: no image in reply"
    raise RuntimeError(last)


def make(spec, thumb):
    last = None
    for _ in range(3):
        try:
            args = {"prompt": spec["thumbnail_style"] + thumb["image"], "aspect_ratio": "16:9", "resolution": "2K", "output_format": "jpeg"}
            model = "fal-ai/nano-banana-2"
            refs = thumb.get("refs") or ([thumb["ref"]] if thumb.get("ref") else [])
            if refs:
                # Keep recurring characters' faces: pass their portraits to the edit model.
                args["image_urls"] = ["data:image/jpeg;base64," + base64.b64encode((ROOT / r).read_bytes()).decode() for r in refs]
                model = "fal-ai/nano-banana-2/edit"
            if os.environ.get("GEMINI_API_KEY") and os.environ.get("THUMB_ENGINE", "gemini") == "gemini":
                (OUT / f"{thumb['id']}.jpg").write_bytes(gemini_image(args["prompt"], refs))
            else:
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
