"""Smoke test of the EvoLink stand-in: two images (text and edit) and one 5 s Kling clip."""
import os
import sys
import time
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))
import evolink_shim as fal  # noqa: E402

os.makedirs("out", exist_ok=True)
t = time.time()
a = fal.subscribe("fal-ai/nano-banana-2", {"prompt": "Cinematic photo, an elderly woman in a cozy kitchen reading an old letter by the window, warm evening light, emotional, realistic", "aspect_ratio": "16:9", "resolution": "1K"})
urllib.request.urlretrieve(a["images"][0]["url"], "out/a.jpg")
print("IMAGE A", round(time.time() - t), "s", a["images"][0]["url"][:80])
ref = fal.upload_file("out/a.jpg")
print("UPLOAD", ref[:80])
t = time.time()
b = fal.subscribe("fal-ai/nano-banana-2/edit", {"prompt": "The same woman now standing at the front door of her house, holding the letter, surprised, same face and clothes", "aspect_ratio": "16:9", "resolution": "1K", "image_urls": [ref]})
urllib.request.urlretrieve(b["images"][0]["url"], "out/b.jpg")
print("IMAGE B", round(time.time() - t), "s")
t = time.time()
c = fal.subscribe("fal-ai/kling-video/v3/standard/image-to-video", {"start_image_url": ref, "prompt": "She slowly lowers the letter and looks up, tears in her eyes, gentle camera push in", "duration": "5", "generate_audio": False})
urllib.request.urlretrieve(c["video"]["url"], "out/clip.mp4")
print("CLIP", round(time.time() - t), "s")
