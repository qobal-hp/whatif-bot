"""Build every asset for one episode spec: narration with word timings, scene images, motion clips.

Usage: python pipeline/generate_assets.py pipeline/ep01_coldopen.json
Writes video/public/assets/* and video/public/props.json for the Remotion render.
"""
import base64
import json
import math
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

import fal_client

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "video" / "public"
ASSETS = PUBLIC / "assets"
FPS = 30
TTS_MODELS = ["eleven_v3", "eleven_multilingual_v2"]
IMAGE_MODEL = "fal-ai/nano-banana-2"
VIDEO_MODEL = "fal-ai/kling-video/v3/standard/image-to-video"


def narrate(text: str, voice_id: str) -> tuple[bytes, dict, str]:
    """Return (mp3 bytes, character alignment, model used)."""
    last_error = None
    for model_id in TTS_MODELS:
        url = (
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps"
            "?output_format=mp3_44100_128"
        )
        req = urllib.request.Request(
            url,
            data=json.dumps({"text": text, "model_id": model_id}).encode(),
            headers={
                "xi-api-key": os.environ["ELEVENLABS_API_KEY"],
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=600) as resp:
                data = json.load(resp)
        except urllib.error.HTTPError as err:
            last_error = f"{model_id}: HTTP {err.code} {err.read().decode(errors='replace')[:300]}"
            print("TTS failed,", last_error)
            continue
        alignment = data.get("alignment")
        if not alignment or not alignment.get("characters"):
            last_error = f"{model_id}: no alignment returned"
            print("TTS failed,", last_error)
            continue
        return base64.b64decode(data["audio_base64"]), alignment, model_id
    raise SystemExit(f"Narration failed: {last_error}")


def words_from_alignment(alignment: dict) -> list[dict]:
    chars = alignment["characters"]
    starts = alignment["character_start_times_seconds"]
    ends = alignment["character_end_times_seconds"]
    words, current = [], None
    for ch, start, end in zip(chars, starts, ends):
        if ch.isspace():
            if current:
                words.append(current)
                current = None
            continue
        if current is None:
            current = {"text": ch, "start": start, "end": end}
        else:
            current["text"] += ch
            current["end"] = end
    if current:
        words.append(current)
    return words


def scene_times(scenes: list[dict], alignment: dict) -> list[tuple[float, float]]:
    """Locate each scene's text in the aligned characters and return (first, last) spoken times."""
    aligned = "".join(alignment["characters"])
    starts = alignment["character_start_times_seconds"]
    ends = alignment["character_end_times_seconds"]
    cursor, spans = 0, []
    for scene in scenes:
        head = scene["text"][:24]
        pos = aligned.find(head, cursor)
        if pos < 0:
            raise SystemExit(f"Could not align scene {scene['id']} ({head!r})")
        spans.append(pos)
        cursor = pos + len(head)
    times = []
    for i, pos in enumerate(spans):
        last = (spans[i + 1] - 1) if i + 1 < len(spans) else len(aligned) - 1
        while last > pos and aligned[last].isspace():
            last -= 1
        times.append((starts[pos], ends[last]))
    return times


def download(url: str, path: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "whatif-bot"})
    with urllib.request.urlopen(req, timeout=600) as resp:
        path.write_bytes(resp.read())


def main() -> None:
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    scenes = spec["scenes"]
    ASSETS.mkdir(parents=True, exist_ok=True)

    text = "\n\n".join(s["text"] for s in scenes)
    audio, alignment, tts_model = narrate(text, spec["voice_id"])
    (ASSETS / "audio.mp3").write_bytes(audio)
    words = words_from_alignment(alignment)
    spoken = scene_times(scenes, alignment)
    audio_end = alignment["character_end_times_seconds"][-1]
    print(f"Narration: {tts_model}, {audio_end:.1f}s, {len(words)} words")

    # Cut between scenes in the middle of the pause that separates them.
    cuts = [0.0]
    for i in range(1, len(scenes)):
        cuts.append((spoken[i - 1][1] + spoken[i][0]) / 2)
    total = audio_end + 1.0
    cuts.append(total)

    out_scenes = []
    for i, scene in enumerate(scenes):
        start, end = cuts[i], cuts[i + 1]
        image = fal_client.subscribe(
            IMAGE_MODEL,
            arguments={
                "prompt": spec["style"] + scene["image"],
                "aspect_ratio": "16:9",
                "resolution": "2K",
                "output_format": "jpeg",
            },
        )
        image_url = image["images"][0]["url"]
        download(image_url, ASSETS / f"{scene['id']}.jpg")
        entry = {
            "id": scene["id"],
            "start": start,
            "end": end,
            "image": f"assets/{scene['id']}.jpg",
            "cut": scene.get("cut", "fade"),
        }
        print(f"Image {scene['id']}: {start:.2f}-{end:.2f}s")
        if scene.get("motion"):
            clip_seconds = min(10, max(3, math.ceil(end - start)))
            try:
                clip = fal_client.subscribe(
                    VIDEO_MODEL,
                    arguments={
                        "start_image_url": image_url,
                        "prompt": scene["motion"],
                        "duration": str(clip_seconds),
                        "generate_audio": False,
                    },
                )
                download(clip["video"]["url"], ASSETS / f"{scene['id']}.mp4")
                entry["video"] = f"assets/{scene['id']}.mp4"
                entry["videoSeconds"] = clip_seconds
                print(f"Clip {scene['id']}: {clip_seconds}s")
            except Exception as err:  # keep the still image if the clip fails
                print(f"Clip {scene['id']} failed, using the still image: {err}")
        out_scenes.append(entry)

    props = {
        "fps": FPS,
        "durationSec": total,
        "audio": "assets/audio.mp3",
        "scenes": out_scenes,
        "words": words,
    }
    (PUBLIC / "props.json").write_text(json.dumps(props, indent=1), encoding="utf-8")
    print(f"Wrote props.json: {len(out_scenes)} scenes, {total:.1f}s")


if __name__ == "__main__":
    main()
