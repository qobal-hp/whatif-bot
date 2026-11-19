"""Design new cartoon voices with ElevenLabs Voice Design and save previews to listen to.

usage: python karma/voice_design_test.py <out dir>
Writes <role>_<n>.mp3 for each preview and designs.json with the generated ids, so the
chosen preview can be turned into a permanent voice later.
"""
import base64
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

API = "https://api.elevenlabs.io/v1"
KEY = os.environ["ELEVENLABS_API_KEY"]
ROLES = {
    "narrator": ("A warm, friendly American man in his forties narrating a classic animated family film. Cozy storybook tone, gentle humor, crisp and clear, slightly playful.",
                 "Nine hundred years earlier, the serpent made Eve the very same offer. And that is how the first lease was signed. By the third century, the waiting list had a waiting list."),
    "serpent": ("A cartoon snake villain who talks like a slick used-car salesman. Middle-aged American man, smooth and oily, sly and smug, very theatrical, with a subtle hiss stretching his S sounds.",
                "One bite... and you'll know everything. Twelve percent! And your branch is due for inspection. The sun is free. You're paying for the chair. Look at you. Asking the right questions!"),
    "eve": ("A sassy, quick-witted cartoon heroine. Young American woman, bright and expressive, constantly exasperated, sharp comedic timing like a sitcom lead.",
            "Do you know why my rent went up? HEY! You just built over my sun! You're charging me for the SUN?! You asked the guy SELLING THE BOAT TICKETS?!"),
    "adam": ("A lovable, dim cartoon husband. Young American man, goofy, earnest and cheerful, a little dopey, very expressive like an animated sitcom dad.",
             "Hey! Can I put a shelf here? There was a group rate. It's the only thing in this house with a lifetime guarantee! The delivery was free! We paid to turn it around."),
    "god": ("A kind elderly grandfather in an animated film. Deep, soft and warm American voice, patient, gently amused and a little tired.",
            "I made this garden. Adam... you know there's land on the other side of the creek, right? Is that my tree? Did you ask? He doesn't own it."),
    "noah": ("A grumpy old cartoon boat captain. Gravelly, gruff American man in his seventies, bossy and deadpan, sounds like he has explained this too many times.",
             "All right. Two of every kind. Two humans. He bought standby. The giraffes can walk. I'm trying to make this fair. Deep enough to float my boat."),
}


def design(description, text):
    for model in ("eleven_ttv_v3", "eleven_multilingual_ttv_v2"):
        body = json.dumps({"voice_description": description, "text": text, "model_id": model}).encode()
        req = urllib.request.Request(f"{API}/text-to-voice/design", data=body,
                                     headers={"xi-api-key": KEY, "Content-Type": "application/json"})
        try:
            return json.load(urllib.request.urlopen(req, timeout=300))["previews"], model
        except urllib.error.HTTPError as err:
            print(model, "failed:", err.code, err.read()[:300])
    raise SystemExit("voice design failed")


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    saved = {}
    for role, (description, text) in ROLES.items():
        previews, model = design(description, text)
        saved[role] = {"description": description, "model": model, "previews": []}
        for n, p in enumerate(previews[:3], 1):
            raw = out / f"raw_{role}_{n}.mp3"
            raw.write_bytes(base64.b64decode(p["audio_base_64"]))
            final = out / f"{role}_{n}.mp3"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-af", "loudnorm=I=-16:TP=-1.5", "-b:a", "160k", str(final)], check=True)
            raw.unlink()
            saved[role]["previews"].append(p["generated_voice_id"])
        print(f"{role}: {len(saved[role]['previews'])} previews ({model})")
    (out / "designs.json").write_text(json.dumps(saved, indent=1))


if __name__ == "__main__":
    main()
