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
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

KEY = os.environ["ELEVENLABS_API_KEY"]
VOICE = os.environ.get("BIBLIA_VOICE", "keBoNFxkGtsW2ezG8Aqn")
MODEL = os.environ.get("BIBLIA_MODEL", "eleven_flash_v2_5")
PARA_GAP, HEAD_GAP, CHAPTER_GAP = 0.9, 1.6, 3.0
NUMS = ("uno dos tres cuatro cinco seis siete ocho nueve diez once doce trece catorce quince dieciséis diecisiete "
        "dieciocho diecinueve veinte veintiuno veintidós veintitrés veinticuatro veinticinco veintiséis veintisiete "
        "veintiocho veintinueve treinta").split()


def sh(*args):
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True, check=True).stdout
    return float(out)


def tts(job):
    text, prev, nxt, out = job
    if out.exists() and out.stat().st_size > 1000:
        return
    body = json.dumps({"text": text, "model_id": MODEL, "language_code": "es", "previous_text": prev, "next_text": nxt,
                       "voice_settings": {"stability": 0.65, "similarity_boost": 0.8, "style": 0.0, "speed": 0.9}}).encode()
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
    units, ch = [], 0
    for para in [p.strip() for p in script.read_text().split("\n\n") if p.strip()]:
        m = re.match(r"Cap[ií]tulo (\w+)\.$", para)
        if m:
            ch = NUMS.index(m.group(1)) + 1
            units.append((ch, "head", para))
        else:
            units.append((ch, "para", para))
    last_ch = units[-1][0]
    outro = [u for u in units if u[0] == last_ch and u[1] == "para"][-1] if last_ch > max_ch else None
    units = [u for u in units if u[0] <= max_ch] + ([outro] if outro and max_ch < last_ch else [])
    texts = [u[2] for u in units]
    jobs = [(t, texts[i - 1] if i else "", texts[i + 1] if i + 1 < len(texts) else "", work / f"u{i:04d}.wav")
            for i, t in enumerate(texts)]
    print(f"{len(units)} units, {sum(map(len, texts))} characters, model {MODEL}", flush=True)
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
        img = images / f"cap{max(c, 1):02d}.png"
        lines.append(f"file '{img.resolve()}'\nduration {end - starts[c]:.3f}\n")
    lines.append(f"file '{(images / f'cap{max(order[-1], 1):02d}.png').resolve()}'\n")
    (work / "images.txt").write_text("".join(lines))
    sh("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(work / "images.txt"), "-i", str(audio),
       "-vf", "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=6,format=yuv420p",
       "-c:v", "libx264", "-preset", "veryfast", "-tune", "stillimage", "-crf", "24", "-c:a", "copy",
       "-shortest", "-movflags", "+faststart", str(out / "episode.mp4"))

    def stamp(s):
        s = int(s)
        return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}" if total >= 3600 else f"{s // 60}:{s % 60:02d}"
    chapters = "\n".join(f"{stamp(0 if c == 0 else starts[c])} " + ("Introducción" if c == 0 else f"Génesis {c}")
                         for c in order)
    (out / "chapters.txt").write_text(chapters + "\n")
    print(chapters)
    print(f"Total {total / 3600:.2f} h")


if __name__ == "__main__":
    main()
