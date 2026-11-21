"""Check that the Cloud Text-to-Speech service account can voice one Spanish word with a Gemini voice."""
import json, os, sys, urllib.request, urllib.error
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault("GOOGLE_TTS_SA_JSON", "")
if not os.environ["GOOGLE_TTS_SA_JSON"]:
    print("GOOGLE_TTS_SA_JSON is not set"); sys.exit(0)
import dub
print("service account:", json.loads(os.environ["GOOGLE_TTS_SA_JSON"]).get("client_email"))
body = {"input": {"prompt": "Say it warmly", "text": "Hola"}, "voice": {"languageCode": "es-MX", "name": "Kore", "modelName": "gemini-2.5-flash-tts"},
        "audioConfig": {"audioEncoding": "MP3"}}
try:
    with urllib.request.urlopen(urllib.request.Request("https://texttospeech.googleapis.com/v1/text:synthesize", json.dumps(body).encode(), dub.cloud_headers())) as r:
        print("cloud tts OK,", len(json.loads(r.read())["audioContent"]), "bytes")
except urllib.error.HTTPError as e:
    print("cloud tts", e.code, e.read().decode()[:400])
