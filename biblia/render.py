"""Render a calm Bible reading video: one TTS voice, one still image per chapter, looping music.

usage: python biblia/render.py <script.txt> <images dir> <music.mp3> <out dir> [max_chapters]
Script format: paragraphs separated by blank lines; chapter headings look like "Capítulo uno."
Writes episode.mp4 and description.txt (with YouTube chapter timestamps) to <out dir>.
"""
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

KEY = os.environ.get("ELEVENLABS_API_KEY", "")
VOICE = os.environ.get("BIBLIA_VOICE", "keBoNFxkGtsW2ezG8Aqn")
MODEL = os.environ.get("BIBLIA_MODEL", "eleven_flash_v2_5")
PARA_GAP, HEAD_GAP, CHAPTER_GAP = 0.9, 1.6, 3.0
NUMS = ("uno dos tres cuatro cinco seis siete ocho nueve diez once doce trece catorce quince dieciséis diecisiete "
        "dieciocho diecinueve veinte veintiuno veintidós veintitrés veinticuatro veinticinco veintiséis veintisiete "
        "veintiocho veintinueve treinta").split()


def spanish_number(words):
    words = words.strip()
    if words in NUMS:
        return NUMS.index(words) + 1
    tens = {"treinta": 30, "cuarenta": 40, "cincuenta": 50}
    parts = words.split(" y ")
    return tens[parts[0]] + (NUMS.index(parts[1]) + 1 if len(parts) > 1 else 0)


def sh(*args):
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True, check=True).stdout
    return float(out)


ENGINE = os.environ.get("BIBLIA_TTS", "elevenlabs")
GOOGLE_VOICE = os.environ.get("GOOGLE_VOICE", "es-US-Chirp3-HD-Sulafat")
RATE = float(os.environ.get("BIBLIA_RATE", "0.9"))


def google_chunks(text, limit=4000):
    """Split text on sentence ends so each request stays under Google's 5000-byte limit."""
    parts, cur = [], ""
    for sent in re.split(r"(?<=[.;:?!])\s+", text):
        if cur and len((cur + " " + sent).encode()) > limit:
            parts.append(cur)
            cur = sent
        else:
            cur = (cur + " " + sent).strip()
    return parts + [cur] if cur else parts


STYLE = os.environ.get("BIBLIA_STYLE", (
    "Read this Bible passage aloud in Latin American Spanish as a warm, gentle middle-aged woman reading scripture at "
    "bedtime. Slow, calm and reverent overall, with soft natural pauses. Let quiet emotion come through in the spoken "
    "lines: God's words solemn and majestic, the serpent's words sly and hushed, human voices tender, fearful or "
    "sorrowful as the story calls for, but never loud or theatrical."))
GEMINI_MODELS = os.environ.get("GEMINI_TTS_MODELS", "gemini-3.8-flash-tts,gemini-3.8-flash-lite-tts,gemini-2.5-flash-preview-tts").split(",")


def google_tts(text, out):
    import base64
    mp3s = []
    gemini = ENGINE == "gemini"
    for k, chunk in enumerate(google_chunks(text, 3000 if gemini else 4000)):
        if gemini:
            body = None
            for model in list(GEMINI_MODELS):
                body = {"input": {"text": chunk, "prompt": STYLE},
                        "voice": {"languageCode": "es-US", "name": GOOGLE_VOICE.split("-")[-1], "modelName": model},
                        "audioConfig": {"audioEncoding": "MP3", "speakingRate": RATE, "sampleRateHertz": 44100}}
                req = urllib.request.Request(
                    f"https://texttospeech.googleapis.com/v1/text:synthesize?key={os.environ['GOOGLE_TTS_KEY']}",
                    data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
                try:
                    data = json.load(urllib.request.urlopen(req, timeout=300))
                    break
                except urllib.error.HTTPError as err:
                    msg = err.read()[:300]
                    print(f"{model}: {err.code} {msg}", flush=True)
                    if len(GEMINI_MODELS) > 1 and err.code in (400, 404):
                        GEMINI_MODELS.remove(model)
                        continue
                    raise RuntimeError(f"Gemini TTS {err.code}: {msg}")
            else:
                raise RuntimeError("no Gemini TTS model worked")
            f = out.with_name(f"{out.stem}_{k}.mp3")
            f.write_bytes(base64.b64decode(data["audioContent"]))
            mp3s.append(f)
            continue
        body = {"input": {"text": chunk}, "voice": {"languageCode": GOOGLE_VOICE[:5], "name": GOOGLE_VOICE},
                "audioConfig": {"audioEncoding": "MP3", "speakingRate": RATE, "sampleRateHertz": 44100}}
        req = urllib.request.Request(
            f"https://texttospeech.googleapis.com/v1/text:synthesize?key={os.environ['GOOGLE_TTS_KEY']}",
            data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
        try:
            data = json.load(urllib.request.urlopen(req, timeout=300))
        except urllib.error.HTTPError as err:
            raise RuntimeError(f"Google TTS {err.code}: {err.read()[:300]}")
        f = out.with_name(f"{out.stem}_{k}.mp3")
        f.write_bytes(base64.b64decode(data["audioContent"]))
        mp3s.append(f)
    lst = out.with_suffix(".lst")
    lst.write_text("".join(f"file '{m.resolve()}'\n" for m in mp3s))
    sh("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-ar", "44100", "-ac", "1", str(out))


def gemini_api_tts(text, out):
    """Gemini API (AI Studio key): style direction travels as speech_metadata, never spoken."""
    import base64
    key = os.environ["GEMINI_API_KEY"]
    voice = GOOGLE_VOICE.split("-")[-1]
    wavs = []
    for k, chunk in enumerate(google_chunks(text, 3000)):
        last = None
        for model in GEMINI_MODELS:
            for with_meta in (True, False):
                part = {"text": chunk}
                if with_meta:
                    part["speech_metadata"] = {"style": STYLE}
                body = {"contents": [{"parts": [part]}],
                        "generationConfig": {"responseModalities": ["AUDIO"],
                                             "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
                req = urllib.request.Request(
                    f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                    data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": key})
                try:
                    data = json.load(urllib.request.urlopen(req, timeout=300))
                    inline = data["candidates"][0]["content"]["parts"][0]["inlineData"]
                    raw = base64.b64decode(inline["data"])
                    f = out.with_name(f"{out.stem}_{k}.wav")
                    if raw[:4] == b"RIFF":
                        f.write_bytes(raw)
                    else:
                        pcm = f.with_suffix(".pcm")
                        pcm.write_bytes(raw)
                        rate = re.search(r"rate=(\d+)", inline.get("mimeType", ""))
                        sh("ffmpeg", "-y", "-f", "s16le", "-ar", rate.group(1) if rate else "24000", "-ac", "1",
                           "-i", str(pcm), str(f))
                    wavs.append(f)
                    break
                except urllib.error.HTTPError as err:
                    last = f"{model} meta={with_meta}: {err.code} {err.read()[:300]}"
                    print(last, flush=True)
                    if err.code == 429:
                        import time
                        time.sleep(30)
            else:
                continue
            break
        else:
            raise RuntimeError(f"Gemini API TTS failed: {last}")
    lst = out.with_suffix(".lst")
    lst.write_text("".join(f"file '{w.resolve()}'\n" for w in wavs))
    tempo = f"atempo={max(RATE, 0.5)}" if RATE != 1.0 else "anull"
    sh("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-af", tempo, "-ar", "44100", "-ac", "1", str(out))


def tts(job):
    text, prev, nxt, out = job
    if out.exists() and out.stat().st_size > 1000:
        return
    if ENGINE in ("google", "gemini", "gemini-api"):
        for attempt in range(4):
            try:
                return gemini_api_tts(text, out) if ENGINE == "gemini-api" else google_tts(text, out)
            except Exception as err:
                print(f"{out.name} attempt {attempt + 1} failed: {err}", flush=True)
        raise SystemExit(f"TTS failed for {out.name}")
    body = json.dumps({"text": text, "model_id": MODEL, "language_code": "es", "previous_text": prev, "next_text": nxt,
                       "voice_settings": {"stability": 0.65, "similarity_boost": 0.8, "style": 0.0, "speed": RATE}}).encode()
    for attempt in range(4):
        req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}?output_format=mp3_44100_128",
                                     data=body, headers={"xi-api-key": KEY, "Content-Type": "application/json"})
        try:
            mp3 = out.with_suffix(".mp3")
            mp3.write_bytes(urllib.request.urlopen(req, timeout=300).read())
            sh("ffmpeg", "-y", "-i", str(mp3), "-ar", "44100", "-ac", "1", str(out))
            return
        except Exception as err:
            print(f"{out.name} attempt {attempt + 1} failed: {err}", flush=True)
    raise SystemExit(f"TTS failed for {out.name}")


def main():
    script, images, music, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
    max_ch = int(sys.argv[5]) if len(sys.argv) > 5 and sys.argv[5] else 999
    out.mkdir(parents=True, exist_ok=True)
    work = out / "work"
    work.mkdir(exist_ok=True)

    # Units: (chapter number, kind, text). Chapter 0 = intro.
    # Headings: "Capítulo uno." or "Génesis, capítulo treinta y uno." Chapters are numbered in reading
    # order (1, 2, ...) to match images cap01, cap02, ...; labels keep the book and real chapter number.
    units, ch, labels = [], 0, {0: "Introducción"}
    for para in [p.strip() for p in script.read_text().split("\n\n") if p.strip()]:
        m = re.match(r"(?:([A-ZÁÉÍÓÚ][\wáéíóúñ ]+), c|C)ap[ií]tulo ([\wáéíóúñ ]+)\.$", para)
        if m:
            ch += 1
            labels[ch] = f"{m.group(1) or 'Génesis'} {spanish_number(m.group(2))}"
            units.append((ch, "head", para))
        else:
            units.append((ch, "para", para))
    last_ch = units[-1][0]
    outro = [u for u in units if u[0] == last_ch and u[1] == "para"][-1] if last_ch > max_ch else None
    units = [u for u in units if u[0] <= max_ch] + ([outro] if outro and max_ch < last_ch else [])
    texts = [u[2] for u in units]
    jobs = [(t, texts[i - 1] if i else "", texts[i + 1] if i + 1 < len(texts) else "", work / f"u{i:04d}.wav")
            for i, t in enumerate(texts)]
    print(f"{len(units)} units, {sum(map(len, texts))} characters, {ENGINE} {GOOGLE_VOICE if ENGINE != 'elevenlabs' else MODEL}", flush=True)
    with ThreadPoolExecutor(4) as pool:
        list(pool.map(tts, jobs))

    # Voice track with pauses; remember where each chapter starts.
    silence = {}
    for gap in (PARA_GAP, HEAD_GAP, CHAPTER_GAP):
        f = work / f"sil{gap}.wav"
        sh("ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=mono", "-t", str(gap), str(f))
        silence[gap] = f
    concat, t, starts = [], 2.0, {}
    lead = work / "lead.wav"
    sh("ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", "2", str(lead))
    concat.append(lead)
    for i, (c, kind, _) in enumerate(units):
        if kind == "head":
            if concat and i:
                concat.append(silence[CHAPTER_GAP]); t += CHAPTER_GAP
            starts[c] = t
        if c == 0 and 0 not in starts:
            starts[0] = 0.0
        concat.append(jobs[i][3]); t += duration(jobs[i][3])
        gap = HEAD_GAP if kind == "head" else PARA_GAP
        concat.append(silence[gap]); t += gap
    total = t + 6.0
    (work / "voice.txt").write_text("".join(f"file '{p.resolve()}'\n" for p in concat))
    voice = work / "voice.wav"
    sh("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(work / "voice.txt"), "-c", "pcm_s16le", str(voice))

    # Voice + looping music bed, gently faded.
    audio = work / "mix.m4a"
    sh("ffmpeg", "-y", "-i", str(voice), "-stream_loop", "-1", "-i", str(music), "-filter_complex",
       f"[0]apad,atrim=0:{total}[v];[1]atrim=0:{total},volume=0.13,afade=t=in:d=4,afade=t=out:st={total - 6}:d=6[m];"
       "[v][m]amix=inputs=2:duration=first:normalize=0,aresample=44100[a]",
       "-map", "[a]", "-c:a", "aac", "-b:a", "160k", str(audio))

    # One image per chapter (intro shows chapter 1's image).
    order = sorted(starts)
    lines = []
    for k, c in enumerate(order):
        end = starts[order[k + 1]] if k + 1 < len(order) else total
        img = next(images.glob(f"cap{max(c, 1):02d}.*"))
        lines.append(f"file '{img.resolve()}'\nduration {end - starts[c]:.3f}\n")
    lines.append(f"file '{next(images.glob(f'cap{max(order[-1], 1):02d}.*')).resolve()}'\n")
    (work / "images.txt").write_text("".join(lines))
    sh("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(work / "images.txt"), "-i", str(audio),
       "-vf", "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=6,format=yuv420p",
       "-c:v", "libx264", "-preset", "veryfast", "-tune", "stillimage", "-crf", "24", "-c:a", "copy",
       "-shortest", "-movflags", "+faststart", str(out / "episode.mp4"))

    def stamp(s):
        s = int(s)
        return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}" if total >= 3600 else f"{s // 60}:{s % 60:02d}"
    chapters = "\n".join(f"{stamp(0 if c == 0 else starts[c])} " + labels[c]
                         for c in order)
    (out / "chapters.txt").write_text(chapters + "\n")
    print(chapters)
    print(f"Total {total / 3600:.2f} h")


if __name__ == "__main__":
    main()
