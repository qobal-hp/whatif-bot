"""Vertical Bible Shorts: one passage each, voiced verse by verse, with verse captions and a hook title.

usage: python biblia/make_shorts.py <shorts.json> <images dir> <music.mp3> <out dir>
shorts.json: {"script": episode script with [[ref]] lines, "voice": Google voice,
              "shorts": [{"id", "passage": "Génesis 1:1-5", "image": "cap01", "hook": "..."}]}
"""
import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render  # noqa: E402

W, H = 1080, 1920
FONTS = Path(__file__).resolve().parent / "fonts"


def verses_of(script, passage):
    table = {}
    for line in Path(script).read_text().splitlines():
        m = re.match(r"\[\[(.+?)\]\]\s*(.+)", line.strip())
        if m:
            table[m.group(1)] = m.group(2)
    book_ch, rng = passage.rsplit(":", 1)
    a, b = (int(x) for x in rng.split("-"))
    return [(f"{book_ch}:{v}", table[f"{book_ch}:{v}"]) for v in range(a, b + 1)]


def ass(cues, hook, end_at, path):
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Verse,Cormorant Garamond,76,&H00F2F6FA,&H00F2F6FA,&H00000000,&H96000000,1,0,0,0,100,100,0,0,1,4,3,2,80,80,330,1
Style: Hook,Cinzel,62,&H0078C8EC,&H0078C8EC,&H00000000,&H96000000,1,0,0,0,100,100,0,0,1,4,3,8,70,70,170,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = [f"Dialogue: 1,{render.ass_time(0)},{render.ass_time(end_at)},Hook,,0,0,0,,{{\\fad(400,0)}}{hook}"]
    for start, end, ref, text in cues:
        parts, cur = [], ""
        for piece in re.split(r"(?<=[,;:.?!])\s+", text):
            if cur and len(cur) + len(piece) > 105:
                parts.append(cur)
                cur = piece
            else:
                cur = (cur + " " + piece).strip()
        parts.append(cur)
        total = sum(len(p) for p in parts) or 1
        t = start
        for k, part in enumerate(parts):
            t2 = end if k + 1 == len(parts) else t + (end - start) * len(part) / total
            last = 0.3 if k + 1 == len(parts) else 0
            lines.append(f"Dialogue: 0,{render.ass_time(t)},{render.ass_time(t2 + last)},Verse,,0,0,0,,"
                         f"{{\\fad(200,200)}}{{\\fnCinzel\\fs50\\c&H78C8EC&}}{ref}\\N{{\\r}}{part}")
            t = t2
    lines.append(f"Dialogue: 0,{render.ass_time(end_at - 3.2)},{render.ass_time(end_at)},Verse,,0,0,0,,"
                 "{\\fad(300,0)}{\\fnCinzel\\fs48\\c&H78C8EC&}" + END_CARD)
    path.write_text(head + "\n".join(lines) + "\n")


END_CARD = "▶ Lectura completa\\N{\\r}en el enlace del video"


def main():
    cfg = json.load(open(sys.argv[1]))
    images, music, out = Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
    out.mkdir(parents=True, exist_ok=True)
    render.ENGINE = "google"
    render.GOOGLE_VOICE = cfg["voice"]
    render.VERSE_VOICE = cfg.get("verse_voice") or cfg["voice"]
    render.RATE = float(cfg.get("rate", 0.8))
    global END_CARD
    if cfg.get("end_card"):
        END_CARD = cfg["end_card"]
    for s in cfg["shorts"]:
        work = out / f"work_{s['id']}"
        work.mkdir(exist_ok=True)
        vs = verses_of(cfg["script"], s["passage"])
        if s.get("question"):  # question-led short: ask, read the passage, then answer it in our own words
            vs = [("Pregunta", s["question"])] + vs + [("Respuesta", s["answer"])]
        elif s.get("interpretation"):  # the passage, then what it means, in our own words
            vs.append(("Interpretación", s["interpretation"]))
        elif s.get("reflection"):  # a line of our own after the passage: what it means for us today
            vs.append(("Reflexión", s["reflection"]))
        jobs = [(t, "", "", work / f"v{i:02d}.wav", *render.voice_and_rate("verse", r)) for i, (r, t) in enumerate(vs)]
        with ThreadPoolExecutor(2) as pool:
            list(pool.map(render.tts, jobs))
        gap = work / "gap.wav"
        render.sh("ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", "0.4", str(gap))
        lead = 1.2
        lead_f = work / "lead.wav"
        render.sh("ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", str(lead), str(lead_f))
        concat, t, cues, switch = [lead_f], lead, [], None
        for k, ((ref, text), job) in enumerate(zip(vs, jobs)):
            d = render.duration(job[3])
            if ref == "Interpretación":
                switch = t - 0.6
            cues.append((t, t + d, ref, text))
            extra = 1 if k + 1 < len(vs) and vs[k + 1][0] in ("Reflexión", "Respuesta", "Interpretación") or ref == "Pregunta" else 0
            concat += [job[3]] + [gap] * (1 + extra)
            t += d + 0.4 * (1 + extra)
        total = t + 3.0
        (work / "voice.txt").write_text("".join(f"file '{p.resolve()}'\n" for p in concat))
        voice = work / "voice.wav"
        render.sh("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(work / "voice.txt"), str(voice))
        ass(cues, s["hook"], total, work / "subs.ass")
        names = s.get("images") or [s["image"]]
        imgs = [next(images.glob(f"{n}.*")) for n in names]
        grad = Path(__file__).resolve().parent / "caption_grad.png"
        if len(imgs) > 1 and switch:  # second picture for the interpretation, dissolving in
            spans = [(0, switch + 1.0), (switch, total - switch)]
        else:
            imgs, spans = imgs[:1], [(0, total)]
        bg = work / "bg.mp4"
        parts = []
        for k, (img, (st, dur)) in enumerate(zip(imgs, spans)):
            frames = int(dur * 30)
            z = f"1+0.08*on/{frames}" if k % 2 == 0 else f"1.08-0.08*on/{frames}"
            clip = work / f"bg{k}.mp4"
            render.sh("ffmpeg", "-y", "-loop", "1", "-framerate", "30", "-t", f"{dur:.2f}", "-i", str(img), "-vf",
                      f"scale=-2:{H}*1.5,crop={W}*1.5:{H}*1.5,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
                      f":d=1:s={W}x{H}:fps=30", "-frames:v", str(frames), "-c:v", "libx264", "-preset", "veryfast",
                      "-crf", "18", "-pix_fmt", "yuv420p", str(clip))
            parts.append(clip)
        if len(parts) > 1:
            render.sh("ffmpeg", "-y", "-i", str(parts[0]), "-i", str(parts[1]), "-filter_complex",
                      f"[0][1]xfade=transition=fade:duration=1:offset={switch:.2f}", "-c:v", "libx264",
                      "-preset", "veryfast", "-crf", "18", str(bg))
        else:
            bg = parts[0]
        vf = (f"[0]null[bg];"
              f"movie={grad},scale={W}:700[g];[bg][g]overlay=0:H-h,"
              f"subtitles={work / 'subs.ass'}:fontsdir={FONTS},format=yuv420p[v];"
              f"[1]apad,atrim=0:{total}[vo];[2]atrim=0:{total},volume=0.13,afade=t=in:d=2,afade=t=out:st={total - 2.5}:d=2.5[m];"
              "[vo][m]amix=inputs=2:duration=first:normalize=0[a]")
        render.sh("ffmpeg", "-y", "-i", str(bg), "-i", str(voice), "-stream_loop", "-1", "-i", str(music),
                  "-filter_complex", vf, "-map", "[v]", "-map", "[a]", "-t", f"{total:.2f}",
                  "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-c:a", "aac", "-b:a", "160k",
                  "-movflags", "+faststart", str(out / f"{s['id']}.mp4"))
        print(f"{s['id']}: {s['passage']} {total:.1f}s", flush=True)


if __name__ == "__main__":
    main()
