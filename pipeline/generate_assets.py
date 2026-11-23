"""Build every asset for one episode spec: narration with word timings, scene images, motion clips.

Usage: python pipeline/generate_assets.py pipeline/ep01_coldopen.json
Writes video/public/assets/* and video/public/props.json for the Remotion render.
"""
import base64
import json
import math
import os
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import os as _os
if _os.environ.get("EVOLINK_API_KEY") and _os.environ.get("MEDIA_PROVIDER", "evolink") != "fal":
    import sys as _sys
    _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "pipeline"))
    import evolink_shim as fal_client  # same calls, run on EvoLink
else:
    import fal_client

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "video" / "public"
ASSETS = PUBLIC / "assets"
FPS = 30
TTS_MODELS = ["eleven_v3", "eleven_multilingual_v2"]
IMAGE_MODEL = "fal-ai/nano-banana-2"
VIDEO_MODEL = "fal-ai/kling-video/v3/standard/image-to-video"
CHUNK_CHARS = 2400  # stay well under the per-request limit of the v3 voice model
CHUNK_GAP = 0.5  # silence inserted between narration chunks, in seconds


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


def media_seconds(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        check=True, capture_output=True, text=True,
    )
    return float(out.stdout.strip())


def chunk_scenes(scenes: list[dict]) -> list[list[dict]]:
    chunks, current, size = [], [], 0
    for scene in scenes:
        if current and size + len(scene["text"]) > CHUNK_CHARS:
            chunks.append(current)
            current, size = [], 0
        current.append(scene)
        size += len(scene["text"]) + 2
    if current:
        chunks.append(current)
    return chunks


def narrate_episode(scenes: list[dict], voice_id: str) -> tuple[list[dict], list[tuple[float, float]], float]:
    """Narrate in chunks, join them into assets/audio.mp3, return (words, spoken spans, total seconds)."""
    words, spoken, offset = [], [], 0.0
    wavs = []
    with tempfile.TemporaryDirectory() as tmp:
        for n, chunk in enumerate(chunk_scenes(scenes)):
            text = "\n\n".join(s["text"] for s in chunk)
            audio, alignment, model = narrate(text, voice_id)
            mp3 = Path(tmp) / f"chunk{n}.mp3"
            wav = Path(tmp) / f"chunk{n}.wav"
            mp3.write_bytes(audio)
            subprocess.run(
                ["ffmpeg", "-v", "error", "-y", "-i", str(mp3), "-af", f"apad=pad_dur={CHUNK_GAP}",
                 "-ar", "44100", "-ac", "1", str(wav)],
                check=True,
            )
            for word in words_from_alignment(alignment):
                words.append({"text": word["text"], "start": word["start"] + offset, "end": word["end"] + offset})
            for first, last in scene_times(chunk, alignment):
                spoken.append((first + offset, last + offset))
            seconds = media_seconds(wav)
            print(f"Narration chunk {n}: {model}, {len(text)} chars, {seconds:.1f}s")
            offset += seconds
            wavs.append(wav)
        listing = Path(tmp) / "list.txt"
        listing.write_text("".join(f"file '{w}'\n" for w in wavs))
        subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(listing),
             "-c:a", "libmp3lame", "-b:a", "160k", str(ASSETS / "audio.mp3")],
            check=True,
        )
    return words, spoken, offset


def make_image(spec: dict, scene: dict) -> str:
    last = None
    for _ in range(3):
        try:
            image = fal_client.subscribe(
                IMAGE_MODEL,
                arguments={
                    "prompt": spec["style"] + scene["image"],
                    "aspect_ratio": "16:9",
                    "resolution": spec.get("resolution", "2K"),
                    "output_format": "jpeg",
                },
            )
            url = image["images"][0]["url"]
            download(url, ASSETS / f"{scene['id']}.jpg")
            return url
        except Exception as err:
            last = err
            print(f"Image {scene['id']} attempt failed: {err}")
    raise SystemExit(f"Image {scene['id']} failed three times: {last}")


def make_clip(scene: dict, image_url: str, seconds: int) -> bool:
    try:
        clip = fal_client.subscribe(
            VIDEO_MODEL,
            arguments={
                "start_image_url": image_url,
                "prompt": scene["motion"],
                "duration": str(seconds),
                "generate_audio": False,
            },
        )
        download(clip["video"]["url"], ASSETS / f"{scene['id']}.mp4")
        return True
    except Exception as err:  # keep the still image if the clip fails
        print(f"Clip {scene['id']} failed, using the still image: {err}")
        return False


def main() -> None:
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    scenes = spec["scenes"]
    ASSETS.mkdir(parents=True, exist_ok=True)

    words, spoken, audio_len = narrate_episode(scenes, spec["voice_id"])
    print(f"Narration total: {audio_len:.1f}s, {len(words)} words")

    # Cut between scenes in the middle of the pause that separates them.
    cuts = [0.0]
    for i in range(1, len(scenes)):
        cuts.append((spoken[i - 1][1] + spoken[i][0]) / 2)
    total = spoken[-1][1] + 1.2
    cuts.append(total)

    with ThreadPoolExecutor(max_workers=6) as pool:
        image_urls = list(pool.map(lambda sc: make_image(spec, sc), scenes))
    print(f"Images done: {len(image_urls)}")

    clip_jobs = []
    for i, scene in enumerate(scenes):
        if scene.get("motion"):
            seconds = min(10, max(3, math.ceil(cuts[i + 1] - cuts[i])))
            clip_jobs.append((i, seconds))
    with ThreadPoolExecutor(max_workers=4) as pool:
        clip_ok = list(pool.map(lambda job: make_clip(scenes[job[0]], image_urls[job[0]], job[1]), clip_jobs))
    clips = {i: seconds for (i, seconds), ok in zip(clip_jobs, clip_ok) if ok}
    print(f"Clips done: {len(clips)} of {len(clip_jobs)}")

    out_scenes = []
    for i, scene in enumerate(scenes):
        entry = {
            "id": scene["id"],
            "start": cuts[i],
            "end": cuts[i + 1],
            "image": f"assets/{scene['id']}.jpg",
            "cut": scene.get("cut", "fade"),
        }
        if i in clips:
            entry["video"] = f"assets/{scene['id']}.mp4"
            entry["videoSeconds"] = clips[i]
        out_scenes.append(entry)

    props = {
        "fps": FPS,
        "durationSec": total,
        "audio": "assets/audio.mp3",
        "scenes": out_scenes,
        "words": words,
    }
    (PUBLIC / "props.json").write_text(json.dumps(props, indent=1), encoding="utf-8")
    longest = max(s["end"] - s["start"] for s in out_scenes)
    print(f"Wrote props.json: {len(out_scenes)} scenes, {total:.1f}s, longest scene {longest:.1f}s")


if __name__ == "__main__":
    main()
