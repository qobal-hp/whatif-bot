"""Try ways to make Gemini Cloud TTS speak at a normal pace; print the length of each attempt."""
import base64, json, os, subprocess, sys, urllib.request, urllib.error
sys.path.insert(0, os.path.dirname(__file__))
import dub
TEXT = "Daniel se rio. Al otro lado de la mesa, Vanessa Collins, la dama de honor de Claire, dejó de sonreír."
variants = {
  "base": ({"prompt": "Speak as the narrator of a dramatic story, in neutral Latin American Spanish. Delivery: calm, suspenseful storytelling."}, {}),
  "fast_prompt": ({"prompt": "Read quickly and fluidly, like a fast-paced TV narrator, in neutral Latin American Spanish. No pauses between sentences. Suspenseful."}, {}),
  "rate125": ({"prompt": "Speak as the narrator of a dramatic story, in neutral Latin American Spanish. Delivery: calm, suspenseful storytelling."}, {"speakingRate": 1.25}),
  "fast_rate125": ({"prompt": "Read quickly and fluidly, like a fast-paced TV narrator, in neutral Latin American Spanish. No pauses between sentences. Suspenseful."}, {"speakingRate": 1.25}),
  "no_prompt": ({}, {}),
}
for model in ["gemini-2.5-flash-tts", "gemini-2.5-pro-tts"]:
    for name, (inp, ac) in variants.items():
        body = {"input": dict(inp, text=TEXT), "voice": {"languageCode": "es-MX", "name": "Charon", "modelName": model},
                "audioConfig": dict({"audioEncoding": "LINEAR16", "sampleRateHertz": 24000}, **ac)}
        try:
            with urllib.request.urlopen(urllib.request.Request("https://texttospeech.googleapis.com/v1/text:synthesize", json.dumps(body).encode(), dub.cloud_headers())) as r:
                b = base64.b64decode(json.loads(r.read())["audioContent"])
            open("/tmp/t.wav", "wb").write(b)
            d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", "/tmp/t.wav"], capture_output=True, text=True).stdout.strip()
            print(f"PACE {model} {name}: {d}s")
        except urllib.error.HTTPError as e:
            print(f"PACE {model} {name}: HTTP {e.code} {e.read().decode()[:200]}")
