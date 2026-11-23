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


VERTEX_IMAGE_MODELS = ["gemini-3-pro-image-preview", "gemini-2.5-flash-image"]


def _vertex_image(parts, aspect, size):
    project, headers = _vertex()
    last = None
    for model in VERTEX_IMAGE_MODELS:
        config = {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": aspect}}
        if "2.5" not in model:
            config["imageConfig"]["imageSize"] = size
        url = f"https://aiplatform.googleapis.com/v1/projects/{project}/locations/global/publishers/google/models/{model}:generateContent"
        body = {"contents": [{"role": "user", "parts": [{"inlineData": p["inline_data"]} if "inline_data" in p else p for p in parts]}],
                "generationConfig": config}
        for _ in range(6):
            try:
                req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers)
                out = json.loads(urllib.request.urlopen(req, timeout=300).read())
            except urllib.error.HTTPError as err:
                last = f"vertex {model}: HTTP {err.code} {err.read()[:200]}"
                if err.code in (400, 403, 404):
                    break
                time.sleep(30)
                continue
            for cand in out.get("candidates", []):
                for part in cand.get("content", {}).get("parts", []):
                    data = part.get("inlineData") or part.get("inline_data")
                    if data:
                        return base64.b64decode(data["data"])
            last = f"vertex {model}: no image"
    raise RuntimeError(last)


def image(prompt, ref_paths=(), aspect="16:9", size="2K"):
    """Return JPEG/PNG bytes for one picture, passing reference portraits."""
    if os.environ.get("IMAGE_VIA") == "vertex" and os.environ.get("GOOGLE_TTS_SA_JSON"):
        return _vertex_image([_inline(p) for p in ref_paths] + [{"text": prompt}], aspect, size)
    try:
        return _studio_image(prompt, ref_paths, aspect, size)
    except RuntimeError as err:
        if os.environ.get("GOOGLE_TTS_SA_JSON") and ("402" in str(err) or "429" in str(err)):
            print(f"AI Studio image failed ({str(err)[:80]}), trying Vertex AI")
            os.environ["IMAGE_VIA"] = "vertex"
            return _vertex_image([_inline(p) for p in ref_paths] + [{"text": prompt}], aspect, size)
        raise


def _studio_image(prompt, ref_paths=(), aspect="16:9", size="2K"):
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
                if err.code in (400, 402, 403, 404):
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


_VEO = []


def _veo_models():
    """The Veo models this key can run, newest and fastest first."""
    if not _VEO:
        found, token = [], ""
        while True:
            page = _call(f"{API}/models?pageSize=200" + (f"&pageToken={token}" if token else ""))
            found += [m["name"].split("/")[-1] for m in page.get("models", [])
                      if "veo" in m["name"] and "predictLongRunning" in m.get("supportedGenerationMethods", [])]
            token = page.get("nextPageToken")
            if not token:
                break
        found.sort(key=lambda n: ("fast" not in n, "lite" in n, [-int(x) for x in __import__("re").findall(r"\d+", n)[:2]]))
        print(f"Veo models: {found}")
        _VEO.extend(found or VIDEO_MODELS)
    return _VEO


VERTEX_MODELS = ["veo-3.1-fast-generate-001", "veo-3.1-fast-generate-preview", "veo-3.0-fast-generate-001", "veo-2.0-generate-001"]


def _vertex():
    """(project, headers) from the Google Cloud service account, or None."""
    raw = os.environ.get("GOOGLE_TTS_SA_JSON")
    if not raw:
        return None
    from google.oauth2 import service_account
    import google.auth.transport.requests
    info = json.loads(raw)
    creds = service_account.Credentials.from_service_account_info(info, scopes=["https://www.googleapis.com/auth/cloud-platform"])
    creds.refresh(google.auth.transport.requests.Request())
    return info["project_id"], {"Authorization": f"Bearer {creds.token}", "Content-Type": "application/json"}


def _vertex_video(start_image, prompt, seconds):
    project, headers = _vertex()
    base = f"https://us-central1-aiplatform.googleapis.com/v1/projects/{project}/locations/us-central1/publishers/google/models"
    body = {"instances": [{"prompt": prompt + ". Subtle, realistic cinematic motion, no new people, no text.",
                           "image": {"bytesBase64Encoded": base64.b64encode(open(start_image, "rb").read()).decode(), "mimeType": "image/jpeg"}}],
            "parameters": {"aspectRatio": "16:9", "durationSeconds": seconds, "sampleCount": 1, "generateAudio": False}}
    last = None
    for model in VERTEX_MODELS:
        def post(url, data):
            req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers)
            return json.loads(urllib.request.urlopen(req, timeout=300).read())
        try:
            op = post(f"{base}/{model}:predictLongRunning", body)
        except urllib.error.HTTPError as err:
            last = f"vertex {model}: HTTP {err.code} {err.read()[:300]}"
            print(last)
            continue
        for _ in range(90):
            time.sleep(10)
            op = post(f"{base}/{model}:fetchPredictOperation", {"operationName": op["name"]})
            if op.get("done"):
                break
        if not op.get("done") or op.get("error"):
            last = f"vertex {model}: {op.get('error') or 'timed out'}"
            print(last)
            continue
        vids = op.get("response", {}).get("videos") or []
        if vids and vids[0].get("bytesBase64Encoded"):
            return base64.b64decode(vids[0]["bytesBase64Encoded"]), seconds
        last = f"vertex {model}: no video ({json.dumps(op.get('response'))[:300]})"
        print(last)
    raise RuntimeError(last)


def video(start_image, prompt, seconds):
    """Return MP4 bytes animating start_image (Veo). seconds is rounded to 4, 6 or 8."""
    if os.environ.get("GOOGLE_TTS_SA_JSON"):
        try:
            return _vertex_video(start_image, prompt, 8 if seconds > 6 else 6)
        except Exception as err:
            print(f"Vertex Veo failed: {err}")
    seconds = 8 if seconds > 6 else 6
    body = {"instances": [{"prompt": prompt + ". Subtle, realistic cinematic motion, no new people, no text.",
                           "image": {"bytesBase64Encoded": base64.b64encode(open(start_image, "rb").read()).decode(), "mimeType": "image/jpeg"}}],
            "parameters": {"aspectRatio": "16:9", "durationSeconds": seconds}}
    last = None
    for model in _veo_models():
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
