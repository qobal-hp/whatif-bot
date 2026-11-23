"""Drop-in stand-in for fal_client that runs the same jobs on EvoLink.

Used when EVOLINK_API_KEY is set (and MEDIA_PROVIDER is not "fal"). Only the calls this repo makes are mapped:
nano-banana-2 (text and edit) images and Kling image-to-video. Results come back in fal's shape.
"""
import json
import mimetypes
import os
import time
import urllib.request
import uuid

# EvoLink's file CDN refuses Python's default user agent, so every download in the process gets a browser one.
_opener = urllib.request.build_opener()
_opener.addheaders = [("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) whatif-bot")]
urllib.request.install_opener(_opener)

API = "https://api.evolink.ai"
FILES = "https://files-api.evolink.ai/api/v1/files/upload/stream"
IMAGE_MODEL = os.environ.get("EVOLINK_IMAGE_MODEL", "gemini-3.1-flash-image-preview")
VIDEO_MODEL = os.environ.get("EVOLINK_VIDEO_MODEL", "kling-v3-image-to-video")


def _key():
    return os.environ["EVOLINK_API_KEY"]


def _call(method, url, body=None, headers=None, raw=None):
    h = {"Authorization": f"Bearer {_key()}", "User-Agent": "whatif-bot"}
    data = raw
    if body is not None:
        data = json.dumps(body).encode()
        h["Content-Type"] = "application/json"
    h.update(headers or {})
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    try:
        return json.load(urllib.request.urlopen(req, timeout=300))
    except urllib.error.HTTPError as err:
        raise RuntimeError(f"EvoLink {err.code}: {err.read()[:400]!r}") from None


def _urls(obj):
    """Every http(s) URL inside a JSON value, in order."""
    if isinstance(obj, str):
        return [obj] if obj.startswith("http") else []
    if isinstance(obj, dict):
        return [u for v in obj.values() for u in _urls(v)]
    if isinstance(obj, list):
        return [u for v in obj for u in _urls(v)]
    return []


def _wait(task, timeout=1800):
    tid = task.get("id") or task.get("task_id") or task.get("data", {}).get("id")
    if not tid:
        raise RuntimeError(f"EvoLink gave no task id: {str(task)[:300]}")
    start = time.time()
    while time.time() - start < timeout:
        t = _call("GET", f"{API}/v1/tasks/{tid}")
        status = str(t.get("status", "")).lower()
        if status == "completed":
            urls = _urls(t.get("results")) or _urls(t.get("result_data")) or _urls(t)
            if not urls:
                raise RuntimeError(f"EvoLink task {tid} completed without a URL")
            return urls
        if status in ("failed", "error", "cancelled"):
            raise RuntimeError(f"EvoLink task {tid} {status}: {str(t)[:300]}")
        time.sleep(5)
    raise RuntimeError(f"EvoLink task {tid} timed out")


def upload_file(path):
    path = str(path)
    boundary = uuid.uuid4().hex
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    name = os.path.basename(path)
    body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{name}\"\r\n"
            f"Content-Type: {mime}\r\n\r\n").encode() + open(path, "rb").read() + f"\r\n--{boundary}--\r\n".encode()
    r = _call("POST", FILES, raw=body, headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    data = r.get("data", r)
    url = data.get("file_url") or data.get("download_url") or (_urls(data) or [None])[0]
    if not url:
        raise RuntimeError(f"EvoLink upload gave no URL: {str(r)[:300]}")
    return url


def subscribe(model, arguments):
    a = arguments
    if "nano-banana" in model or "image" in model and "video" not in model:
        body = {"model": IMAGE_MODEL, "prompt": a["prompt"], "size": a.get("aspect_ratio", "auto"),
                "quality": a.get("resolution", "2K")}
        if a.get("image_urls"):
            body["image_urls"] = a["image_urls"]
        urls = _wait(_call("POST", f"{API}/v1/images/generations", body))
        return {"images": [{"url": u} for u in urls]}
    if "kling" in model or "video" in model:
        body = {"model": VIDEO_MODEL, "image_start": a["start_image_url"], "prompt": a.get("prompt", ""),
                "duration": int(a.get("duration", 5)), "quality": "720p",
                "sound": "on" if a.get("generate_audio") else "off"}
        if a.get("end_image_url"):
            body["image_end"] = a["end_image_url"]
        urls = _wait(_call("POST", f"{API}/v1/videos/generations", body))
        return {"video": {"url": next((u for u in urls if ".mp4" in u), urls[0])}}
    raise RuntimeError(f"No EvoLink mapping for {model}")
