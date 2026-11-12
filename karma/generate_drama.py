"""Build the assets for a multi-voice drama spec: dialogue with word timings and scene images
that keep each character's face consistent by passing their reference portrait to the image model.

usage: python karma/generate_drama.py karma/ep01_act1.json
Writes video/public/assets/* and video/public/props.json for the Remotion "Episode" composition.
"""
import base64
import json
import mimetypes
import subprocess
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import fal_client

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "pipeline"))
from generate_assets import ASSETS, FPS, PUBLIC, download, media_seconds, narrate, words_from_alignment  # noqa: E402

import os  # noqa: E402

EDIT_MODEL = "fal-ai/nano-banana-2/edit"
TEXT_MODEL = "fal-ai/nano-banana-2"
LINE_GAP = 0.3  # pause after each line, seconds
SCENE_GAP = 0.55  # pause after the last line of a scene


def voice_ids(names):
    req = urllib.request.Request("https://api.elevenlabs.io/v1/voices", headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"]})
    available = json.load(urllib.request.urlopen(req, timeout=60)).get("voices", [])
    ids = {}
    for role, name in names.items():
        match = next((v["voice_id"] for v in available if v.get("name", "").split(" ")[0].lower() == name.lower()), None)
        if not match:
            raise SystemExit(f"No voice named {name}")
        ids[role] = match
    return ids


def record(spec, tmp):
    """Speak every line with its character's voice; return (words, scene times, total seconds)."""
    ids = voice_ids(spec["voices"])
    jobs = [(s["id"], i, role, text) for s in spec["scenes"] for i, (role, text) in enumerate(s["lines"])]

    def one(job):
        sid, i, role, text = job
        audio, alignment, model = narrate(text, ids[role])
        raw = tmp / f"{sid}_{i}.mp3"
        raw.write_bytes(audio)
        return job, raw, alignment, model

    with ThreadPoolExecutor(4) as pool:
        done = list(pool.map(one, jobs))

    words, times, wavs, cursor = [], [], [], 0.0
    for scene in spec["scenes"]:
        start = cursor
        mine = [d for d in done if d[0][0] == scene["id"]]
        for n, (job, raw, alignment, model) in enumerate(mine):
            gap = SCENE_GAP if n == len(mine) - 1 else LINE_GAP
            wav = raw.with_suffix(".wav")
            subprocess.run(
                ["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-af", f"apad=pad_dur={gap}", "-ar", "44100", "-ac", "1", str(wav)],
                check=True,
            )
            for w in words_from_alignment(alignment):
                words.append({"text": w["text"], "start": w["start"] + cursor, "end": w["end"] + cursor})
            length = media_seconds(wav)
            print(f"{scene['id']} {job[2]:9s} {length:5.1f}s {model}")
            wavs.append(wav)
            cursor += length
        times.append((start, cursor))

    listing = tmp / "list.txt"
    listing.write_text("".join(f"file '{w}'\n" for w in wavs))
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(listing), "-b:a", "192k", str(ASSETS / "audio.mp3")],
        check=True,
    )
    return words, times, cursor


def reference_url(path):
    """Give the image model a URL for a local portrait."""
    try:
        return fal_client.upload_file(str(path))
    except Exception as err:
        print(f"Upload of {path.name} failed ({err}); sending it inline")
        mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
        return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def picture(spec, scene, refs):
    who = scene.get("chars", [])
    prompt = spec["style"] + " ".join(spec["looks"][c] + "." for c in who) + " " + scene["image"]
    args = {"prompt": prompt, "aspect_ratio": "16:9", "resolution": spec.get("resolution", "2K"), "output_format": "jpeg"}
    model = TEXT_MODEL
    if who:
        model = EDIT_MODEL
        args["image_urls"] = [refs[c] for c in who]
    last = None
    for _ in range(3):
        try:
            result = fal_client.subscribe(model, arguments=args)
            download(result["images"][0]["url"], ASSETS / f"{scene['id']}.jpg")
            return
        except Exception as err:
            last = err
            print(f"Image {scene['id']} attempt failed: {err}")
    raise SystemExit(f"Image {scene['id']} failed three times: {last}")


def main():
    spec = json.loads(Path(sys.argv[1]).read_text())
    ASSETS.mkdir(parents=True, exist_ok=True)
    tmp = ROOT / "karma" / ".tmp"
    tmp.mkdir(exist_ok=True)

    # Dialogue first: if the voice service fails, nothing has been spent on images yet.
    words, times, total = record(spec, tmp)
    print(f"Dialogue done: {total:.1f}s, {len(words)} words")

    refs = {name: reference_url(ROOT / path) for name, path in spec["cast"].items()}
    with ThreadPoolExecutor(6) as pool:
        list(pool.map(lambda s: picture(spec, s, refs), spec["scenes"]))
    print("Images done")

    scenes, overlays = [], []
    for scene, (start, end) in zip(spec["scenes"], times):
        scenes.append({"id": scene["id"], "start": start, "end": end, "image": f"assets/{scene['id']}.jpg", "cut": bool(scene.get("cut"))})
        if scene.get("overlay"):
            overlays.append(dict(scene["overlay"], start=start + 0.6, end=end - 0.2))
    props = {"fps": FPS, "durationSec": total, "audio": "assets/audio.mp3", "scenes": scenes, "words": words, "overlays": overlays}
    (PUBLIC / "props.json").write_text(json.dumps(props))
    print(f"Wrote props: {len(scenes)} scenes, {len(overlays)} overlays")


if __name__ == "__main__":
    main()
