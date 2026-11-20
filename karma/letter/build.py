"""Build the Karma Tales spec for "The Letter That Never Came" (1-hour narrated format).

Inputs next to this file: units.json (script split into scenes) and prompts.json (image prompts).
Run: python karma/letter/build.py -> karma/letter/episode.json
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
units = json.loads((HERE / "units.json").read_text())
prompts = json.loads((HERE / "prompts.json").read_text())

STYLE = ("Photorealistic still from a prestige American period drama film, shot on 35mm, warm cinematic lighting, "
         "shallow depth of field, natural skin texture, wide 16:9 frame. Keep every person's face and hair exactly "
         "consistent with their reference photo. No text, no captions, no readable writing, no watermark. ")
P = ("Photorealistic 35mm film portrait, head and shoulders, soft natural window light, plain muted background, "
     "looking slightly off camera, period-accurate, ")
CAST = {
    "maggie_young": "karma/cast/letter/maggie_young.jpg", "maggie_old": "karma/cast/letter/maggie_old.jpg",
    "daniel_young": "karma/cast/letter/daniel_young.jpg",
}
PORTRAITS = {
    "maggie_mid": P + "a 45-year-old American woman in 1970, auburn wavy shoulder-length hair with a few grey strands, freckles, warm hazel eyes, small pearl earrings, modest cardigan, a librarian.",
    "daniel_old": P + "a 71-year-old American man in 1996, tall and lean, thick white curly hair, deep brown eyes, weathered kind face, dark wool coat, retired railway engineer.",
    "charles_young": P + "a 31-year-old American man in 1952, broad jaw, neatly combed sandy blond hair, pale grey eyes, tailored charcoal three-piece suit, polished banker's son, faint confident smile.",
    "charles_mid": P + "a 55-year-old American man in 1975, broad jaw, sandy hair turning silver and neatly combed, pale grey eyes, tailored navy suit, successful small-town banker.",
    "charles_old": P + "a 75-year-old American man in 1996, broad jaw now gaunt, thin silver hair, pale grey eyes, frail and ill, beige cardigan over a collared shirt.",
    "eleanor": P + "a 53-year-old American woman in 1952, narrow stern face, severe silver hair in a tight bun, burgundy high-collared dress, thin lips, anxious eyes.",
    "laura_child": P + "a 12-year-old American girl in 1965, chestnut hair in a ponytail, brown eyes, plaid school dress.",
    "laura": P + "a 43-year-old American woman in 1996, chestnut shoulder-length hair, brown eyes, determined chin, practical oatmeal cardigan, school counselor.",
    "rose": P + "a 43-year-old American woman in 1997, dark wavy hair, brown eyes, determined chin, soft green sweater, music teacher.",
    "ruth_mid": P + "a 49-year-old American woman in 1974, short dark hair, fine delicate features, conservative navy dress, worried eyes.",
    "ruth_old": P + "a 71-year-old American woman in 1996, short dark hair gone mostly grey, fine features, navy cardigan, frightened gentle eyes.",
    "helen": P + "a 68-year-old Black American woman in 1996, tightly curled silver hair, precise composed manner, reading glasses on a chain, lavender blouse, retired nurse.",
    "rebecca": P + "a 49-year-old American woman attorney in 1996, dark cropped hair, understated charcoal suit, calm compassionate eyes.",
    "joseph": P + "a small weary American man of 50 in 1952, wire-framed spectacles, thinning hair, white hospital clerk's coat.",
    "edith": P + "a 25-year-old American woman in 1952, cheerful round face, brown hair in a scarf, flour-dusted apron, baker.",
}
for k in PORTRAITS:
    CAST[k] = f"karma/cast/letter/{k}.jpg"
LOOKS = {
    "maggie_young": "Maggie (the young woman from her reference photo: auburn wavy curls, freckles, red lipstick, 1950s cotton dress)",
    "maggie_mid": "Maggie (the middle-aged woman from her reference photo)",
    "maggie_old": "Maggie (the elderly woman from her reference photo: grey curly hair, pearl earrings, brown knit cardigan)",
    "daniel_young": "Daniel (the young man from his reference photo: dark curly hair, work shirt with suspenders)",
    "daniel_old": "Daniel (the elderly man from his reference photo: white curly hair, dark coat)",
    "charles_young": "Charles (the man from his reference photo, in a tailored suit)",
    "charles_mid": "Charles (the man from his reference photo, in a tailored suit)",
    "charles_old": "Charles (the frail old man from his reference photo, in a cardigan)",
    "eleanor": "Eleanor (the stern woman from her reference photo, burgundy dress, silver bun)",
    "laura_child": "young Laura (the girl from her reference photo)",
    "laura": "Laura (the woman from her reference photo, cardigan)",
    "rose": "Rose (the woman from her reference photo)",
    "ruth_mid": "Ruth (the woman from her reference photo, navy dress)",
    "ruth_old": "Ruth (the elderly woman from her reference photo, navy cardigan)",
    "helen": "Helen (the woman from her reference photo)",
    "rebecca": "Rebecca (the attorney from her reference photo, charcoal suit)",
    "joseph": "Joseph (the man from his reference photo, wire spectacles)",
    "edith": "Edith (the young woman from her reference photo, apron)",
}
VOICES = {"NARRATOR": "id:XHyGEEXDSpWQ3Yc8VlsJ", "MAGGIE": "id:XHyGEEXDSpWQ3Yc8VlsJ", "CHARLES": "id:a8cgM0zKDg7aTA2vJNFj"}

scenes = []
for u in units:
    p = prompts[u["id"]]
    s = {"id": u["id"], "chars": p.get("chars", []), "image": p["image"], "lines": u["lines"], "place": ""}
    if p.get("motion"):
        s["motion"] = p["motion"]
    if u.get("part_title"):
        num, _, name = u["part_title"].partition(" — ")
        s["overlay"] = {"type": "text", "text": f"{num}|{name}"}
        s["cut"] = True
    scenes.append(s)
scenes[0]["sfx"] = [["Steady rain on old windows and a slow grandfather clock ticking in a quiet room", 4.0, 0.3, "start"]]
scenes[9]["sfx"] = [["A grandfather clock's ticking suddenly stops, then silence", 2.0, 0.4, "end"]]
scenes[10]["cut"] = True

MUSIC = [["t001", "tension"], ["t012", "wonder"], ["t050", "tension"], ["t094", "wonder"], ["t124", "tension"],
         ["t156", "wonder"], ["t179", "tension"], ["t199", "wonder"], ["t236", "tension"], ["t266", "wonder"]]
AMBIENCES = {
    "rain": ["Steady rain against old house windows at night, quiet room, faint clock ticking", 0.08],
    "library": ["Quiet old library room tone, creaking floorboards, a distant freight train passing", 0.06],
    "house": ["Quiet 1950s house interior room tone, a clock ticking softly", 0.05],
    "hospital": ["Quiet hospital corridor room tone, distant footsteps and murmurs", 0.05],
    "office": ["Quiet office room tone, faint radiator hum", 0.05],
    "outdoors": ["Gentle outdoor breeze, distant birds, faraway train", 0.06],
}
AMBIENCE = [["t001", "rain"], ["t012", "library"], ["t024", "house"], ["t059", "hospital"], ["t068", "house"],
            ["t124", "rain"], ["t156", "office"], ["t170", "house"], ["t199", "outdoors"], ["t236", "office"], ["t266", "house"]]

TITLE = "Her Husband Hid His Letter for 44 Years. Then She Found It."
SHORTS = [
    ("short1", "t001", "t010", "SHE FOUND HIS LETTER|44 YEARS LATE", "Her Husband Hid His Letter for 44 Years 💌 #shorts"),
    ("short2", "t050", "t058", "SHE WAITED FOR|HIS LETTER", "She Waited for His Letter. Then a Stranger Called. #shorts"),
    ("short3", "t059", "t065", "TWO INITIALS IN|A VISITOR BOOK", "She Found Her Husband's Initials in the Hospital Visitor Book #shorts"),
    ("short4", "t099", "t103", "SHE HEARD|TWO BABIES CRY", "She Heard Two Babies Cry. They Gave Her Only One. #shorts"),
    ("short5", "t125", "t127", "BEHIND THEIR|WEDDING PHOTO", "Her Wedding Photo Hid His Letter for 44 Years #shorts"),
    ("short6", "t179", "t185", "THE WOMAN|AT THE GATE", "A Stranger Stood at Her Gate in 1974. 22 Years Later She Learned Why. #shorts"),
    ("short7", "t157", "t161", "ONE LINE IN|A 1953 HOSPITAL LOG", "She Mourned Her Baby for 43 Years. Then She Read the Hospital Log. #shorts"),
    ("short8", "t214", "t218", "THE NOTE HE KEPT|FOR 44 YEARS", "He Carried Her Goodbye Note for 44 Years. She Never Wrote It. #shorts"),
]
spec = {
    "title": "Karma Tales - The Letter That Never Came",
    "voices": VOICES, "cast": CAST, "portraits": PORTRAITS, "looks": LOOKS, "style": STYLE, "resolution": "2K",
    "music": MUSIC, "places": {}, "ambiences": AMBIENCES, "ambience": AMBIENCE, "tail": 3.0, "scenes": scenes,
    "thumbnail_file": "karma/letter_thumb.jpg",
    "youtube": {
        "title": TITLE, "category": "24",
        "description": ("In 1952, Maggie Bennett waited for a letter from the man she loved. It never came.\n\n"
                        "Forty-four years later, while repairing the frame of her own wedding photograph, an envelope slid onto the table. "
                        "It was addressed to her, in Daniel's handwriting. And it was only the first secret her husband had kept.\n\n"
                        "Karma Tales: stories where the truth always finds its way home.\n\n"
                        "This story is fiction. Any resemblance to real people or events is coincidental. Narration and images are AI-generated.\n\n"
                        "#karmatales #familysecrets #dramastory #lovestory"),
        "tags": ["karma tales", "family secrets", "drama story", "hidden letter", "lost love", "betrayal story", "twin sisters",
                 "audio drama", "story for adults", "1950s love story", "revenge story"],
        "shorts_description": f"Full story on Karma Tales: {TITLE}\n\n#shorts #karmatales #familysecrets",
    },
    "shorts": [{"id": i, "from": a, "to": b, "title": t, "youtube_title": y} for i, a, b, t, y in SHORTS],
}
ids = {s["id"] for s in scenes}
assert all(c in CAST for s in scenes for c in s["chars"]), "unknown character key"
assert all(a in ids and b in ids for _, a, b, _, _ in SHORTS) and all(m[0] in ids for m in MUSIC + AMBIENCE)
(HERE / "episode.json").write_text(json.dumps(spec, indent=1))
chars = sum(len(t) for s in scenes for _, t in s["lines"])
print(f"{len(scenes)} scenes, {sum(1 for s in scenes if s.get('motion'))} clips, {chars} characters")
