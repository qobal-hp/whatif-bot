"""Build the assets for a multi-voice drama spec: dialogue with word timings and scene images
that keep each character's face consistent by passing their reference portrait to the image model.

usage: python karma/generate_drama.py karma/ep01_act1.json
Scene images already in video/public/assets are reused; REDO_IMAGES=s07,s15 forces those to be remade.
Writes video/public/assets/* and video/public/props.json for the Remotion "Episode" composition.
"""
import base64
import hashlib
import json
import shutil
import mimetypes
import subprocess
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import fal_client

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gemini_media  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "pipeline"))
from generate_assets import ASSETS, FPS, PUBLIC, download, media_seconds  # noqa: E402

import os  # noqa: E402

REDO = {s.strip() for s in os.environ.get("REDO_IMAGES", "").split(",") if s.strip()}
EDIT_MODEL = "fal-ai/nano-banana-2/edit"
TEXT_MODEL = "fal-ai/nano-banana-2"


def voice_ids(names):
    req = urllib.request.Request("https://api.elevenlabs.io/v1/voices", headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"]})
    available = json.load(urllib.request.urlopen(req, timeout=60)).get("voices", [])
    ids = {}
    for role, name in names.items():
        match = next((v["voice_id"] for v in available if v.get("name", "").split(" ")[0].lower() == name.lower()), None)
        if not match and len(name) >= 20 and name.isalnum():
            match = name  # a voice id, e.g. a voice-library voice used directly
        if not match:
            raise SystemExit(f"No voice named {name}")
        ids[role] = match
    return ids


DIALOGUE_MODELS = ["eleven_v4", "eleven_v3"]
CHUNK_CHARS = 1500  # the conversation endpoint takes up to 2,000 characters a request
CHUNK_GAP = 0.6  # silence between conversation chunks, seconds
TARGET_DB = -21.0  # every line is brought to this average level so no voice is louder than another


def converse(lines, ids):
    """Voice a run of lines as one acted conversation. Returns (mp3 bytes, response, model)."""
    last = None
    for model in DIALOGUE_MODELS:
        body = json.dumps({"inputs": [{"text": text, "voice_id": ids[role.split("~")[0]]} for role, text in lines], "model_id": model}).encode()
        req = urllib.request.Request(
            "https://api.elevenlabs.io/v1/text-to-dialogue/with-timestamps?output_format=mp3_44100_128",
            data=body,
            headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"},
        )
        try:
            data = json.load(urllib.request.urlopen(req, timeout=900))
        except urllib.error.HTTPError as err:
            last = f"{model}: HTTP {err.code} {err.read()[:300].decode(errors='replace')}"
            print("Dialogue failed,", last)
            continue
        if data.get("voice_segments") and data.get("alignment"):
            return base64.b64decode(data["audio_base64"]), data, model
        last = f"{model}: response had no timings"
    raise SystemExit(f"Dialogue failed: {last}")


def spoken_words(alignment, breaks=()):
    """Words with timings, leaving out acting directions written in [brackets].

    `breaks` are character positions where a new speaker's line starts, so the last word of one
    line is never glued to the first word of the next.
    """
    words, current, depth = [], None, 0
    breaks = set(breaks)
    for i, (ch, start, end) in enumerate(zip(alignment["characters"], alignment["character_start_times_seconds"], alignment["character_end_times_seconds"])):
        if i in breaks and current:
            words.append(current)
            current = None
        if ch == "[":
            depth += 1
        if depth or ch.isspace():
            if current:
                words.append(current)
                current = None
            if ch == "]":
                depth = max(0, depth - 1)
            continue
        if current is None:
            current = {"text": ch, "start": start, "end": end}
        else:
            current["text"] += ch
            current["end"] = end
    if current:
        words.append(current)
    return words


def mean_db(path, start, end):
    out = subprocess.run(
        ["ffmpeg", "-nostdin", "-hide_banner", "-ss", str(start), "-to", str(end), "-i", str(path), "-af", "volumedetect", "-vn", "-f", "null", "-"],
        capture_output=True, text=True,
    ).stderr
    found = [l for l in out.splitlines() if "mean_volume" in l]
    return float(found[0].split("mean_volume:")[1].split("dB")[0]) if found else TARGET_DB


def record(spec, tmp):
    """Voice the script as acted conversations; return (words, scene times, total seconds)."""
    ids = voice_ids(spec["voices"])

    # Group whole scenes into chunks so each request is one continuous conversation.
    chunks, current, size = [], [], 0
    for scene in spec["scenes"]:
        n = sum(len(t) for _, t in scene["lines"])
        if current and size + n > CHUNK_CHARS:
            chunks.append(current)
            current, size = [], 0
        current.append(scene)
        size += n
    chunks.append(current)

    def one(chunk):
        lines = [l for scene in chunk for l in scene["lines"]]
        return converse(lines, ids)

    with ThreadPoolExecutor(3) as pool:
        results = list(pool.map(one, chunks))

    words, times, wavs, cursor, line_starts = [], [], [], 0.0, {}
    for n, (chunk, (audio, data, model)) in enumerate(zip(chunks, results)):
        raw = tmp / f"chunk{n}.mp3"
        raw.write_bytes(audio)
        segments = sorted(data["voice_segments"], key=lambda s: s["dialogue_input_index"])
        lines = [(scene["id"], role) for scene in chunk for role, _ in scene["lines"]]

        # Level every line to the same loudness.
        gains = []
        for seg in segments:
            level = mean_db(raw, seg["start_time_seconds"], seg["end_time_seconds"])
            gain = max(-8.0, min(8.0, TARGET_DB - level))
            window = f"between(t,{seg['start_time_seconds']:.3f},{seg['end_time_seconds']:.3f})"
            gains.append(f"volume=enable='{window}':volume={gain:.1f}dB")
            sid, role = lines[seg["dialogue_input_index"]]
            if role.endswith("~phone"):  # a recording played back: thin it like a phone speaker
                gains.append(f"highpass=f=450:enable='{window}'")
                gains.append(f"lowpass=f=2800:enable='{window}'")
            line_starts.setdefault(sid, []).append(seg["start_time_seconds"] + cursor)
            print(f"{sid} {role:9s} {seg['end_time_seconds'] - seg['start_time_seconds']:5.1f}s level {level:6.1f} dB, gain {gain:+.1f} ({model})")
        wav = tmp / f"chunk{n}.wav"
        subprocess.run(
            ["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(raw), "-af", ",".join(gains) + f",apad=pad_dur={CHUNK_GAP}", "-ar", "44100", "-ac", "1", str(wav)],
            check=True,
        )
        length = media_seconds(wav)

        for w in spoken_words(data["alignment"], [s["character_start_index"] for s in segments]):
            words.append({"text": w["text"], "start": w["start"] + cursor, "end": w["end"] + cursor})

        # A scene starts halfway through the pause before its first line.
        first, index = {}, 0
        for scene in chunk:
            first[scene["id"]] = index
            index += len(scene["lines"])
        starts = []
        for scene in chunk:
            i = first[scene["id"]]
            starts.append(0.0 if i == 0 else (segments[i - 1]["end_time_seconds"] + segments[i]["start_time_seconds"]) / 2)
        for k in range(len(chunk)):
            end = starts[k + 1] if k + 1 < len(chunk) else length
            times.append((starts[k] + cursor, end + cursor))
        wavs.append(wav)
        cursor += length

    listing = tmp / "list.txt"
    listing.write_text("".join(f"file '{w}'\n" for w in wavs))
    subprocess.run(
        ["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(listing), "-b:a", "192k", str(ASSETS / "audio.mp3")],
        check=True,
    )
    return words, times, cursor, line_starts


def reference_url(path):
    """Give the image model a URL for a local portrait."""
    try:
        return fal_client.upload_file(str(path))
    except Exception as err:
        print(f"Upload of {path.name} failed ({err}); sending it inline")
        mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
        return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def picture(spec, scene, refs):
    target = ASSETS / f"{scene['id']}.jpg"
    if target.exists() and scene["id"] not in REDO:
        print(f"Image {scene['id']} reused")
        return
    who = scene.get("chars", [])
    place = spec.get("places", {}).get(scene.get("place", ""), "")
    prompt = spec["style"] + place + " " + " ".join(spec["looks"][c] + "." for c in who) + " " + scene["image"]
    args = {"prompt": prompt, "aspect_ratio": spec.get("aspect", "16:9"), "resolution": spec.get("resolution", "2K"), "output_format": "jpeg"}
    model = TEXT_MODEL
    if who:
        model = EDIT_MODEL
        if not gemini_media.enabled():
            args["image_urls"] = [refs[c.split(":")[0]] for c in who]
    last = None
    for _ in range(3):
        try:
            if gemini_media.enabled():
                paths = [ROOT / spec["cast"][c.split(":")[0]] for c in who]
                (ASSETS / f"{scene['id']}.jpg").write_bytes(gemini_media.image(prompt, paths, args["aspect_ratio"], args["resolution"]))
                return
            result = fal_client.subscribe(model, arguments=args)
            download(result["images"][0]["url"], ASSETS / f"{scene['id']}.jpg")
            return
        except Exception as err:
            last = err
            print(f"Image {scene['id']} attempt failed: {err}")
    raise SystemExit(f"Image {scene['id']} failed three times: {last}")


VIDEO_MODEL = "fal-ai/kling-video/v3/standard/image-to-video"


def clip(scene, seconds):
    """Turn a scene's picture into a short moving clip; keeps the still if it fails."""
    try:
        if gemini_media.enabled():
            data, used = gemini_media.video(ASSETS / f"{scene['id']}.jpg", scene["motion"], seconds)
            (ASSETS / f"{scene['id']}.mp4").write_bytes(data)
            return used
        result = fal_client.subscribe(VIDEO_MODEL, arguments={
            "start_image_url": reference_url(ASSETS / f"{scene['id']}.jpg"),
            "prompt": scene["motion"], "duration": str(seconds), "generate_audio": False})
        download(result["video"]["url"], ASSETS / f"{scene['id']}.mp4")
        return seconds
    except Exception as err:
        print(f"Clip {scene['id']} failed, keeping the still: {err}")
        return False


def clips(spec, lengths):
    """Make clips for scenes that ask for motion; returns {scene id: clip seconds}."""
    jobs = []
    for s in spec["scenes"]:
        if not s.get("motion") or s["id"] not in lengths:
            continue
        seconds = 10 if lengths[s["id"]] > 7 else 5
        if (ASSETS / f"{s['id']}.mp4").exists() and s["id"] not in REDO:
            jobs.append((s, seconds, True))
        else:
            jobs.append((s, seconds, None))
    with ThreadPoolExecutor(4) as pool:
        made = list(pool.map(lambda j: j[2] or clip(j[0], j[1]), jobs))
    done = {s["id"]: (ok if isinstance(ok, int) and not isinstance(ok, bool) else seconds) for (s, seconds, _), ok in zip(jobs, made) if ok}
    print(f"Clips: {len(done)} of {len(jobs)}")
    return done


def attach_clips(props, done):
    for scene in props["scenes"]:
        if scene["id"] in done:
            scene["video"] = f"assets/{scene['id']}.mp4"
            scene["videoSeconds"] = done[scene["id"]]


NUMBERS = {w: i for i, w in enumerate("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}


def countdown(o, index, times, words):
    """A floating countdown over one or more scenes. In "spoken" mode it shows each number
    the narrator says on its own ("Ten." "Nine.") or before "seconds"; in "live" mode it ticks
    down once a second from start_value."""
    start = times[index][0]
    end = times[min(index + o.get("span", 1) - 1, len(times) - 1)][1]
    out = dict(o, start=start, end=end)
    if o.get("mode", "spoken") == "spoken":
        inside = [w for w in words if start <= w["start"] < end]
        ticks = []
        for i, w in enumerate(inside):
            word = w["text"].strip().lower().strip(".,!?\"'")
            if word not in NUMBERS:
                continue
            alone = w["text"].strip().endswith(".") and (i == 0 or inside[i - 1]["text"].strip()[-1:] in ".!?")
            before_seconds = i + 1 < len(inside) and inside[i + 1]["text"].lower().startswith("second")
            if alone or before_seconds:
                ticks.append([round(w["start"], 2), NUMBERS[word]])
        out["ticks"] = ticks
    return out


def sound(prompt, seconds):
    """Generate one sound effect; returns the asset path, or None if it could not be made."""
    name = "sfx_" + hashlib.md5(f"{prompt}|{seconds}".encode()).hexdigest()[:10] + ".mp3"
    if (ASSETS / name).exists():
        return f"assets/{name}"
    body = json.dumps({"text": prompt, "duration_seconds": seconds, "prompt_influence": 0.4}).encode()
    req = urllib.request.Request(
        "https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_128",
        data=body,
        headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"},
    )
    try:
        (ASSETS / name).write_bytes(urllib.request.urlopen(req, timeout=300).read())
        return f"assets/{name}"
    except Exception as err:
        print(f"Sound effect skipped ({prompt[:40]}): {err}")
        return None


def sounds(spec, times, line_starts, total):
    """Spot effects placed on scenes, and looping room tone that runs from one cue to the next."""
    ids = [s["id"] for s in spec["scenes"]]
    spots = []
    for scene, (start, end) in zip(spec["scenes"], times):
        for prompt, seconds, volume, when in scene.get("sfx", []):
            src = sound(prompt, seconds)
            if not src:
                continue
            if when == "end":
                at = max(start, end - seconds)
            elif isinstance(when, int):
                at = line_starts.get(scene["id"], [start])[min(when, len(line_starts.get(scene["id"], [start])) - 1)] - 0.15
            else:
                at = start + 0.05
            spots.append({"src": src, "start": max(0.0, at), "volume": volume})
    beds, cues = [], spec.get("ambience", [])
    for i, (sid, key) in enumerate(cues):
        if key == "none":
            continue
        src = sound(spec["ambiences"][key][0], 14)
        if not src:
            continue
        stop = times[ids.index(cues[i + 1][0])][0] if i + 1 < len(cues) else total
        beds.append({"src": src, "start": times[ids.index(sid)][0], "end": stop, "volume": spec["ambiences"][key][1]})
    return spots, beds


def main():
    spec = json.loads(Path(sys.argv[1]).read_text())
    ASSETS.mkdir(parents=True, exist_ok=True)
    tmp = ROOT / "karma" / ".tmp"
    tmp.mkdir(exist_ok=True)

    # Images first: they are kept and reused by a later run if anything after this fails,
    # while a voiced performance cannot be reused.
    todo = [s for s in spec["scenes"] if s["id"] in REDO or not (ASSETS / f"{s['id']}.jpg").exists()]
    needed = {c.split(":")[0] for s in todo for c in s.get("chars", [])}
    for name in needed:
        path = ROOT / spec["cast"][name]
        if not path.exists() and spec.get("portraits", {}).get(name):
            # A character without a portrait yet: draw one, and every scene uses it as the reference.
            path.parent.mkdir(parents=True, exist_ok=True)
            if gemini_media.enabled():
                path.write_bytes(gemini_media.image(spec["portraits"][name], (), "3:4", "1K"))
            else:
                result = fal_client.subscribe(TEXT_MODEL, arguments={"prompt": spec["portraits"][name], "aspect_ratio": "3:4", "resolution": "1K", "output_format": "jpeg"})
                download(result["images"][0]["url"], path)
            if path.resolve() != (ASSETS / f"portrait_{name}.jpg").resolve():
                shutil.copy(path, ASSETS / f"portrait_{name}.jpg")  # kept with the assets so it can be saved later
            print(f"Portrait of {name} drawn")
    refs = {} if gemini_media.enabled() else {name: reference_url(ROOT / path) for name, path in spec["cast"].items() if name in needed}
    with ThreadPoolExecutor(6) as pool:
        list(pool.map(lambda s: picture(spec, s, refs), spec["scenes"]))
    print("Images done")
    if os.environ.get("IMAGES_ONLY"):
        # A patch run: add any missing clips to the existing episode's props.
        path = PUBLIC / "props.json"
        if path.exists() and any(s.get("motion") for s in spec["scenes"]):
            props = json.loads(path.read_text())
            done = clips(spec, {s["id"]: s["end"] - s["start"] for s in props["scenes"]})
            attach_clips(props, done)
            path.write_text(json.dumps(props))
        return

    words, times, total, line_starts = record(spec, tmp)
    print(f"Dialogue done: {total:.1f}s, {len(words)} words")

    scenes, overlays = [], []
    for scene, (start, end) in zip(spec["scenes"], times):
        scenes.append({"id": scene["id"], "start": start, "end": end, "image": f"assets/{scene['id']}.jpg", "cut": bool(scene.get("cut")), "tall": spec.get("aspect") == "9:16"})
        for o in ([scene["overlay"]] if isinstance(scene.get("overlay"), dict) else scene.get("overlay", [])):
            if o.get("type") == "countdown":
                overlays.append(countdown(o, len(scenes) - 1, times, words))
            else:
                overlays.append(dict(o, start=start + 0.6, end=end - 0.2))
    tail = spec.get("tail", 0)
    if tail:
        # Hold the last picture (and any end card) for a moment after the last word.
        total += tail
        scenes[-1]["end"] = total
        if overlays and spec["scenes"][-1].get("overlay"):
            overlays[-1]["end"] = total
    attach_clips({"scenes": scenes}, clips(spec, {s["id"]: s["end"] - s["start"] for s in scenes}))
    spots, beds = sounds(spec, times, line_starts, total)
    print(f"Sounds: {len(spots)} effects, {len(beds)} room tones")
    props = {"fps": FPS, "durationSec": total, "audio": "assets/audio.mp3", "scenes": scenes, "words": words, "overlays": overlays, "sfx": spots, "ambience": beds}
    if spec.get("title_band"):
        props["title"] = spec["title_band"]
    (PUBLIC / "props.json").write_text(json.dumps(props))
    print(f"Wrote props: {len(scenes)} scenes, {len(overlays)} overlays")


if __name__ == "__main__":
    main()
