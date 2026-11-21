"""Dub a finished English Karma Tales episode into Spanish with Gemini TTS, keeping every scene exactly as long as in English.

usage: python karma/es/dub.py <episode, e.g. ep01>
Runs inside the karma-episode workflow after the English assets were downloaded to video/public (render_only).
Reads karma/es/<episode>_lines.py (LINES, OVERLAYS, VOICES) and replaces video/public/assets/audio.mp3, the words
and the overlay texts in video/public/props.json. Scene timing, pictures, clips, effects and music are untouched,
so the Spanish video is cut exactly like the English one.
"""
import base64, importlib.util, json, os, re, subprocess, sys, time, urllib.error, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "video" / "public"
TMP = ROOT / "karma" / ".tmp_es"; TMP.mkdir(parents=True, exist_ok=True)
RATE = 24000
MODELS = ["gemini-3.1-flash-tts-preview", "gemini-2.5-flash-preview-tts"]
KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
SA_JSON = os.environ.get("GOOGLE_TTS_SA_JSON")  # Cloud Text-to-Speech service account: Gemini voices without the AI Studio 100-a-day cap
CLOUD_KEY = bool(SA_JSON)
_token = {"value": None, "at": 0.0, "project": None}


def cloud_headers():
    """Bearer token for the service account, refreshed every 45 minutes."""
    if not _token["value"] or time.time() - _token["at"] > 2700:
        from google.oauth2 import service_account
        import google.auth.transport.requests
        info = json.loads(SA_JSON)
        creds = service_account.Credentials.from_service_account_info(info, scopes=["https://www.googleapis.com/auth/cloud-platform"])
        creds.refresh(google.auth.transport.requests.Request())
        _token.update(value=creds.token, at=time.time(), project=info.get("project_id"))
    h = {"Content-Type": "application/json", "Authorization": f"Bearer {_token['value']}"}
    if _token["project"]:
        h["x-goog-user-project"] = _token["project"]
    return h
CLOUD_MODELS = ["gemini-2.5-flash-tts", "gemini-2.5-pro-tts"]
TARGET_DB = -20.0
LEAD, GAP, TAIL = 0.3, 0.45, 0.3      # natural silences around and between lines
MIN_LEAD, MIN_GAP, MIN_TAIL = 0.12, 0.22, 0.12
MAX_SPEEDUP, MAX_SLOWDOWN = 1.45, 0.93


def run(*cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True)


def seconds(path):
    return float(run("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)).stdout)


def split_tag(text):
    m = re.match(r"\s*\[([^\]]+)\]\s*(.*)", text, re.S)
    return (m.group(1), m.group(2)) if m else ("", text)


def speak(role, text, out):
    style, words = split_tag(text)
    base = role.split("~")[0]
    if not style:
        style = "calm, suspenseful storytelling" if base == "NARRATOR" else "natural, conversational"
    who = "the narrator of a dramatic story" if base == "NARRATOR" else f"{base.title()}, a character in a dramatic telenovela"
    prompt = (f"Speak as {who}, in neutral Latin American Spanish with a light Mexican accent. Fully acted, emotional and "
              f"believable, at a brisk natural pace with no long pauses. Delivery: {style}. Say exactly this and nothing else: {words}")
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": VOICES[base]}}}}}
    last = None
    for attempt in range(int(os.environ.get('TTS_ATTEMPTS', '30'))):
        model = MODELS[attempt % len(MODELS)] if attempt >= 4 else MODELS[0]
        try:
            raw = out.with_suffix(".raw.wav")
            if CLOUD_KEY:
                cmodel = CLOUD_MODELS[(attempt // 3) % len(CLOUD_MODELS)]
                cbody = {"input": {"prompt": prompt.split(" Say exactly this")[0], "text": words},
                         "voice": {"languageCode": "es-MX", "name": VOICES[base], "modelName": cmodel},
                         "audioConfig": {"audioEncoding": "LINEAR16", "sampleRateHertz": RATE}}
                req = urllib.request.Request("https://texttospeech.googleapis.com/v1/text:synthesize",
                                             json.dumps(cbody).encode(), cloud_headers())
                with urllib.request.urlopen(req, timeout=180) as r:
                    j = json.loads(r.read())
                wavbytes = base64.b64decode(j["audioContent"])
                tmpw = out.with_suffix(".in.wav"); tmpw.write_bytes(wavbytes)
                run("ffmpeg", "-v", "error", "-y", "-i", str(tmpw), "-ar", str(RATE), "-ac", "1", str(raw))
            else:
                req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={KEY}",
                                             json.dumps(body).encode(), {"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=180) as r:
                    j = json.loads(r.read())
                part = j["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
                pcm = out.with_suffix(".pcm"); pcm.write_bytes(base64.b64decode(part))
                run("ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(RATE), "-ac", "1", "-i", str(pcm), str(raw))
            # trim the ends and shorten any long pause inside the line
            run("ffmpeg", "-v", "error", "-y", "-i", str(raw), "-af",
                "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,"
                "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,areverse,"
                "silenceremove=stop_periods=-1:stop_duration=0.55:stop_threshold=-45dB:stop_silence=0.4",
                str(out))
            if seconds(out) < 0.2:
                raise ValueError("empty audio")
            return out
        except (urllib.error.HTTPError, urllib.error.URLError, KeyError, ValueError, IndexError, TimeoutError) as e:
            last = e
            code = getattr(e, "code", None)
            if code in (400, 403, 404, 429) and attempt in (0, 3, 6):
                try:
                    print("429:", e.read().decode(errors="replace")[:500].replace("\n", " "), flush=True)
                except Exception:
                    pass
            time.sleep(min(60, 4 * (attempt + 1)) if code in (429, 500, 503, None) else 5)
    raise RuntimeError(f"{role}: {words[:60]} failed: {last!r}")


def level(path):
    err = subprocess.run(["ffmpeg", "-nostdin", "-i", str(path), "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = re.search(r"mean_volume: (-?[\d.]+) dB", err)
    return float(m.group(1)) if m else TARGET_DB


def main():
    global VOICES
    ep = sys.argv[1]
    spec_mod = importlib.util.spec_from_file_location("lines", ROOT / "karma" / "es" / f"{ep}_lines.py")
    mod = importlib.util.module_from_spec(spec_mod); spec_mod.loader.exec_module(mod)
    LINES, OVERLAYS, VOICES = mod.LINES, getattr(mod, "OVERLAYS", {}), mod.VOICES
    props = json.loads((PUBLIC / "props.json").read_text())

    jobs = [(sid, i, role, text) for s in props["scenes"] for sid in [s["id"]] for i, (role, text) in enumerate(LINES[sid])]
    print(f"{len(jobs)} lines to voice")
    done = {}

    def work(job):
        sid, i, role, text = job
        out = TMP / f"{sid}_{i:02d}.wav"
        if not out.exists():
            speak(role, text, out)
        done[(sid, i)] = out
        return out

    with ThreadPoolExecutor(int(os.environ.get("TTS_WORKERS", "3"))) as pool:
        for n, _ in enumerate(pool.map(work, jobs), 1):
            if n % 25 == 0:
                print(f"  voiced {n}/{len(jobs)}", flush=True)

    words, pieces, report = [], [], []
    for s in props["scenes"]:
        sid, T = s["id"], s["end"] - s["start"]
        lines = LINES[sid]
        files = [done[(sid, i)] for i in range(len(lines))]
        durs = [seconds(f) for f in files]
        n = len(files)
        speech = sum(durs)
        natural_sil = LEAD + TAIL + GAP * (n - 1)
        min_sil = MIN_LEAD + MIN_TAIL + MIN_GAP * (n - 1)
        tempo = 1.0
        if speech + natural_sil > T:
            room = max(0.5, T - min_sil)
            tempo = min(MAX_SPEEDUP, max(1.0, speech / room))
        elif speech < 0.7 * (T - natural_sil):
            tempo = MAX_SLOWDOWN
        spoken = [d / tempo for d in durs]
        sil = max(min_sil, T - sum(spoken)) if n else T
        # share the silence in the same proportions as the natural layout
        weights = [LEAD] + [GAP] * (n - 1) + [TAIL]
        unit = sil / sum(weights)
        lead, gaps, tail = LEAD * unit, [GAP * unit] * (n - 1), TAIL * unit
        over = lead + sum(spoken) + sum(gaps) + tail - T
        report.append((sid, round(T, 2), round(tempo, 2), round(max(0, over), 2)))

        cursor = s["start"] + lead
        filt = []
        for k, (f, (role, text)) in enumerate(zip(files, lines)):
            gain = max(-10.0, min(10.0, TARGET_DB - level(f)))
            chain = f"volume={gain:.1f}dB"
            if tempo != 1.0:
                chain += f",atempo={tempo:.4f}"
            if role.endswith("~phone"):
                chain += ",highpass=f=450,lowpass=f=2800"
            g = TMP / f"{sid}_{k:02d}_fit.wav"
            run("ffmpeg", "-v", "error", "-y", "-i", str(f), "-af", chain, "-ar", "44100", "-ac", "1", str(g))
            d = seconds(g)
            pieces.append((cursor, g))
            # caption words spread over the line by length
            _, plain = split_tag(text)
            toks = plain.split()
            weights_w = [len(t) + 2 for t in toks]
            total_w = sum(weights_w) or 1
            t0 = cursor
            for tok, w in zip(toks, weights_w):
                span = d * w / total_w
                words.append({"text": tok, "start": round(t0, 3), "end": round(t0 + span * 0.92, 3)})
                t0 += span
            cursor += d + (gaps[k] if k < len(gaps) else 0)

    # lay every line at its time on a silent track as long as the episode
    total = props["durationSec"]
    track = TMP / "track.wav"
    inputs, mix = ["-f", "lavfi", "-t", f"{total:.3f}", "-i", "anullsrc=r=44100:cl=mono"], []
    chunks = [pieces[i:i + 60] for i in range(0, len(pieces), 60)]
    layers = []
    for c, chunk in enumerate(chunks):
        args = ["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-t", f"{total:.3f}", "-i", "anullsrc=r=44100:cl=mono"]
        parts = []
        for j, (at, g) in enumerate(chunk, 1):
            args += ["-i", str(g)]
            ms = int(at * 1000)
            parts.append(f"[{j}]adelay={ms}|{ms}[a{j}]")
        labels = "".join(f"[a{j}]" for j in range(1, len(chunk) + 1))
        graph = ";".join(parts) + f";[0]{labels}amix=inputs={len(chunk) + 1}:normalize=0:duration=first"
        layer = TMP / f"layer{c}.wav"
        run(*args, "-filter_complex", graph, str(layer))
        layers.append(layer)
    args = ["ffmpeg", "-v", "error", "-y"]
    for l in layers:
        args += ["-i", str(l)]
    run(*args, "-filter_complex", "".join(f"[{i}]" for i in range(len(layers))) + f"amix=inputs={len(layers)}:normalize=0:duration=first",
        "-b:a", "192k", str(PUBLIC / "assets" / "audio.mp3"))

    # translated on-screen texts
    for o in props.get("overlays", []):
        for s in props["scenes"]:
            if s["start"] <= o["start"] < s["end"] and s["id"] in OVERLAYS:
                o.update(OVERLAYS[s["id"]])
    props["words"] = words
    (PUBLIC / "props.json").write_text(json.dumps(props))
    fast = [r for r in report if r[2] > 1.15]
    over = [r for r in report if r[3] > 0]
    print(f"Spanish dub done: {len(words)} words, {len(fast)} scenes sped up >15%, {len(over)} scenes over length")
    for r in fast + over:
        print("  ", r)


if __name__ == "__main__":
    main()
