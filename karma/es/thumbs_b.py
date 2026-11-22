"""B thumbnails (and B titles) for the Spanish episodes' YouTube A/B tests. Writes karma/es/thumbs_b.json."""
import json
ST = (json.load(open("karma/ep01_full.json")).get("thumbnail_style") or "") + "Maximum drama and shock, like the most clicked telenovela YouTube thumbnails: exaggerated raw emotion, faces huge and close to camera, frozen peak-action moment, intense saturated color with red accents, cinematic. "
Y, W, R = "#FFD400", "#FFFFFF", "#FF3B30"
c = lambda e: json.load(open(f"karma/es/ep{e}_es.json"))["cast"]
T = [
 ("ep01", "right", [c("01")["claire"], c("01")["daniel"], c("01")["vanessa"]], [("ELLA YA", W), ("LO SABÍA", R)], "",
  "Extreme tight close-up filling the left half: the bride from the first reference photo in her lace veil, mascara running, mouth open mid-scream of rage, eyes blazing straight into camera, gripping her phone that glows on her face. Behind her shoulder, in sharp focus, the groom from the second reference photo passionately kissing the bridesmaid from the third reference photo, caught red-handed, his hand on her waist. Harsh red and gold rim light, smoke, broken champagne glass flying. Right third dark and empty."),
 ("ep02", "left", [c("02")["emily"], c("02")["jason"], c("02")["michael"]], [("SE", W), ("RIERON.", R)], "",
  "Explosive moment in a dark law office. Right two thirds: the woman from the first reference photo slamming a single one-dollar bill onto the mahogany table, face twisted in furious tears, shouting. Inches from her face, the two men from the second and third reference photos laughing cruelly, mouths wide, one throwing his head back, one pointing at her. Papers flying, hard red side light, deep shadows. Left third dark and empty."),
 ("ep03", "left", [c("03")["rachel"], c("03")["adam"]], [("SU OTRA", W), ("FAMILIA", R)], "",
  "Night, heavy snow. Right two thirds: extreme close-up of the woman from the first reference photo pressed against a frosted window, palm flat on the glass, mouth open in a silent devastated scream, tears streaming. Through the glass, sharp and bright: the man from the second reference photo kissing a different woman under a Christmas tree while two small children hug his legs calling him dad. Cold blue night outside versus warm gold inside, strong contrast. Left third dark, empty."),
 ("ep04", "right", [c("04")["emma"], c("04")["victoria"], c("04")["ryan"]], [("TIENES", W), ("10 MINUTOS", Y)], "",
  "Thanksgiving dinner turned violent. Left two thirds: the older woman from the second reference photo in burgundy, face red with fury, mid-shout, has just thrown a full glass of red wine in the face of the young woman from the first reference photo; wine splashing in mid-air, droplets frozen. The young woman stands frozen, wine dripping, eyes cold and unbroken staring at camera. Behind them the man from the third reference photo looks away. Guests gasping, a plate shattering on the floor. Dramatic hard light. Right third dark and empty."),
 ("ep05", "left", [c("05")["thomas"], c("05")["olivia"]], [("ME DIERON", W), ("POR MUERTO", R)], "",
  "Right two thirds: a wedding chapel. The bride from the second reference photo in her gown collapses to her knees in the aisle, hands over her mouth, screaming in shock, bouquet falling. Behind her, framed in the blinding light of the flung-open doors, the older man from the first reference photo stands like a ghost in a worn work jacket, staring at her, eyes wet and furious. A dark-haired groom in a navy suit at the altar turns pale with terror. Guests standing up in panic. Strong backlight, dust in the air. Left third dark and empty."),
 ("ep07", "right", [c("07")["evelyn"], c("07")["anna"], c("07")["richard"]], [("40 AÑOS", W), ("ESPERÁNDOLA", Y)], "",
  "Left two thirds: Thanksgiving dinner table in chaos. The old man from the third reference photo has jumped up, face purple with rage, roaring and pointing at the front door, knocking over a chair, wine spilling across the white tablecloth. In the doorway stands the woman from the second reference photo, soaked by rain, holding a bundle of old yellowed letters, staring at him. Between them the old woman from the first reference photo clutches her chest, sobbing, reaching toward the woman at the door. Candles flickering, hard warm-and-red light. Right third dark and empty."),
]
spec = {"thumbnail_style": ST, "thumbnails": [
    {"id": e, "side": s, "refs": r, "lines": [{"text": t, "color": col} for t, col in l], "tag": tag, "image": img}
    for e, s, r, l, tag, img in T]}
json.dump(spec, open("karma/es/thumbs_b.json", "w"), ensure_ascii=False, indent=1)
print(len(spec["thumbnails"]), bool(ST))
