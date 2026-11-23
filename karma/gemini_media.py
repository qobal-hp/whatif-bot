"""Images (Nano Banana) and image-to-video clips (Veo) through the Gemini API, used when GEMINI_API_KEY is set
and MEDIA_ENGINE is not "fal"."""
import base64
import json
import os
import time
import urllib.error
import urllib.request

API = "https://generativelanguage.googleapis.com/v1beta"
IMAGE_MODELS = ["gemini-3.1-flash-image-preview", "gemini-3-pro-image-preview", "gemini-2.5-flash-image"]
VIDEO_MODELS = ["veo-3.1-fast-generate-preview", "veo-3.0-fast-generate-001"]


def enabled():
    return bool(os.environ.get("GEMINI_API_KEY")) and os.environ.get("MEDIA_ENGINE", "gemini") != "fal"


def _call(url, body=None, raw=False, timeout=300):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Content-Type": "application/json", "x-goog-api-key": os.environ["GEMINI_API_KEY"]})
    data = urllib.request.urlopen(req, timeout=timeout).read()
    return data if raw else json.loads(data)


def _inline(path):
    return {"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode(open(path, "rb").read()).decode()}}


def image(prompt, ref_paths=(), aspect="16:9", size="2K"):
    """Return JPEG/PNG bytes for one picture, passing reference portraits."""
    parts = [_inline(p) for p in ref_paths] + [{"text": prompt}]
    last = None
    for model in IMAGE_MODELS:
        config = {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": aspect}}
        if "2.5" not in model:
            config["imageConfig"]["imageSize"] = size
        for attempt in range(8):
            try:
                out = _call(f"{API}/models/{model}:generateContent", {"contents": [{"parts": parts}], "generationConfig": config})
            except urllib.error.HTTPError as err:
                last = f"{model}: HTTP {err.code} {err.read()[:200]}"
                if err.code in (400, 403, 404):
                    break
                time.sleep(60 if err.code == 429 else 5)  # spend/rate limit: wait it out on the same model
                continue
            for cand in out.get("candidates", []):
                for part in cand.get("content", {}).get("parts", []):
                    data = part.get("inlineData") or part.get("inline_data")
                    if data:
                        return base64.b64decode(data["data"])
            last = f"{model}: no image ({json.dumps(out)[:200]})"
    raise RuntimeError(last)


def video(start_image, prompt, seconds):
    """Return MP4 bytes animating start_image (Veo). seconds is rounded to 4, 6 or 8."""
    seconds = 8 if seconds > 6 else 6
    body = {"instances": [{"prompt": prompt + ". Subtle, realistic cinematic motion, no new people, no text.",
                           "image": {"bytesBase64Encoded": base64.b64encode(open(start_image, "rb").read()).decode(), "mimeType": "image/jpeg"}}],
            "parameters": {"aspectRatio": "16:9", "durationSeconds": seconds}}
    last = None
    for model in VIDEO_MODELS:
        try:
            op = _call(f"{API}/models/{model}:predictLongRunning", body)
        except urllib.error.HTTPError as err:
            last = f"{model}: HTTP {err.code} {err.read()[:300]}"
            print(last)
            continue
        for _ in range(120):
            time.sleep(10)
            op = _call(f"{API}/{op['name']}")
            if op.get("done"):
                break
        if not op.get("done") or op.get("error"):
            last = f"{model}: {op.get('error') or 'timed out'}"
            continue
        samples = op["response"]["generateVideoResponse"].get("generatedSamples") or []
        if not samples:
            last = f"{model}: no video ({json.dumps(op['response'])[:300]})"
            continue
        uri = samples[0]["video"]["uri"]
        req = urllib.request.Request(uri, headers={"x-goog-api-key": os.environ["GEMINI_API_KEY"]})
        return urllib.request.urlopen(req, timeout=300).read(), seconds
    raise RuntimeError(last)
