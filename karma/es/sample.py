"""Make the same ~35 s Spanish (Latin American neutral) dub sample twice: Gemini TTS and ElevenLabs v3.

usage: python karma/es/sample.py <out dir>
Env: GEMINI_API_KEY (or GOOGLE_API_KEY), ELEVENLABS_API_KEY. Writes gemini.mp3, elevenlabs.mp3 and a log.
"""
import base64, json, os, subprocess, sys, urllib.parse, urllib.request, urllib.error
from pathlib import Path

OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
LINES = json.loads((Path(__file__).parent / "sample_lines.json").read_text())
GAP = 0.35

GEMINI_VOICES = {"NARRATOR": "Charon", "CLAIRE": "Kore", "DANIEL": "Orus", "VANESSA": "Aoede"}
GEMINI_MODELS = ["gemini-3.1-flash-tts-preview", "gemini-2.5-flash-preview-tts", "gemini-2.5-pro-preview-tts"]
GENDER = {"NARRATOR": ("male", "middle_aged"), "CLAIRE": ("female", "young"), "DANIEL": ("male", "young"), "VANESSA": ("female", "young")}


def http(url, data=None, headers=None, method=None):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read()


def concat(parts, out):
    lst = OUT / f"{out}.txt"
    sil = OUT / "gap.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", str(GAP), str(sil)], check=True)
    norm = []
    for i, p in enumerate(parts):
        q = OUT / f"{out}_{i:02d}.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(p), "-ar", "24000", "-ac", "1", str(q)], check=True)
        norm += [q, sil]
    lst.write_text("".join(f"file '{p.resolve()}'\n" for p in norm))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-af", "loudnorm=I=-16", "-b:a", "160k", str(OUT / f"{out}.mp3")], check=True)


def gemini():
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        print("gemini: no key"); return
    parts = []
    for model in GEMINI_MODELS:
        try:
            parts = []
            for i, (role, style, text) in enumerate(LINES):
                prompt = (f"Read this line from a dramatic Spanish-language telenovela, in neutral Latin American Spanish with a light "
                          f"Mexican accent, fully acted and emotional. Delivery: {style}. Line: {text}")
                body = {"contents": [{"parts": [{"text": prompt}]}],
                        "generationConfig": {"responseModalities": ["AUDIO"],
                                             "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": GEMINI_VOICES[role]}}}}}
                raw = http(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}",
                           json.dumps(body).encode(), {"Content-Type": "application/json"})
                j = json.loads(raw)
                if "content" not in j["candidates"][0]:
                    print("gemini empty:", json.dumps(j)[:300]); raise urllib.error.HTTPError(model, 0, "empty", None, None)
                data = j["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
                pcm = OUT / f"g_{i:02d}.pcm"; pcm.write_bytes(base64.b64decode(data))
                wav = OUT / f"g_{i:02d}.wav"
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", str(pcm), str(wav)], check=True)
                parts.append(wav)
            print(f"gemini: {model} ok"); (OUT / "gemini_model.txt").write_text(model)
            break
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors='replace')[:400] if e.fp else ''
            print(f"gemini {model}: HTTP {e.code} {body}")
    if parts:
        concat(parts, "gemini")


def eleven():
    key = os.environ["ELEVENLABS_API_KEY"]; h = {"xi-api-key": key}
    voices, used = {}, set()
    for role, (g, age) in GENDER.items():
        for accent in ("mexican", "latin american", None):
            q = [("page_size", "30"), ("language", "es"), ("gender", g), ("age", age), ("sort", "usage_character_count_1y")]
            if accent: q.append(("accent", accent))
            if role != "NARRATOR": q.append(("use_cases", "characters_animation"))
            try:
                found = json.loads(http("https://api.elevenlabs.io/v1/shared-voices?" + urllib.parse.urlencode(q), headers=h))["voices"]
            except urllib.error.HTTPError as e:
                print("search", e.code); found = []
            found = [v for v in found if v["voice_id"] not in used and v.get("category") != "famous"]
            if found:
                v = found[0]; voices[role] = v; used.add(v["voice_id"])
                print(f"eleven {role}: {v['name']} ({v.get('accent')}) {v['voice_id']}"); break
    (OUT / "eleven_voices.json").write_text(json.dumps({r: {"voice_id": v["voice_id"], "name": v["name"], "accent": v.get("accent"), "public_owner_id": v.get("public_owner_id")} for r, v in voices.items()}, indent=1))
    parts = []
    for i, (role, style, text) in enumerate(LINES):
        v = voices[role]
        body = {"text": f"[{style}] {text}", "model_id": "eleven_v3", "language_code": "es"}
        try:
            raw = http(f"https://api.elevenlabs.io/v1/text-to-speech/{v['voice_id']}?output_format=mp3_44100_128",
                       json.dumps(body).encode(), {**h, "Content-Type": "application/json"})
        except urllib.error.HTTPError as e:
            print("tts", e.code, e.read().decode(errors="replace")[:300])
            # library voice may need adding first
            add = http(f"https://api.elevenlabs.io/v1/voices/add/{v['public_owner_id']}/{v['voice_id']}",
                       json.dumps({"new_name": f"ES {role} {v['name']}"[:40]}).encode(), {**h, "Content-Type": "application/json"})
            vid = json.loads(add)["voice_id"]; v["voice_id"] = vid
            raw = http(f"https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128",
                       json.dumps(body).encode(), {**h, "Content-Type": "application/json"})
        p = OUT / f"e_{i:02d}.mp3"; p.write_bytes(raw); parts.append(p)
    concat(parts, "elevenlabs")


if __name__ == "__main__":
    for f in ((gemini,) if os.environ.get("ONLY") == "gemini" else (gemini, eleven)):
        try:
            f()
        except Exception as e:  # keep the other sample
            print(f"{f.__name__} failed: {e!r}")
    for p in OUT.glob("*"):
        if p.suffix in (".wav", ".pcm", ".txt") and p.name != "gemini_model.txt" or p.name.startswith("e_"):
            p.unlink()
