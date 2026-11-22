"""B thumbnails (and B titles) for the Spanish episodes' YouTube A/B tests. Writes karma/es/thumbs_b.json."""
import json
ST = json.load(open("karma/ep01_full.json")).get("thumbnail_style") or ""
Y, W, R = "#FFD400", "#FFFFFF", "#FF3B30"
c = lambda e: json.load(open(f"karma/es/ep{e}_es.json"))["cast"]
T = [
 ("ep01", "right", [c("01")["claire"], c("01")["daniel"], c("01")["vanessa"]], [("ELLA YA", W), ("LO SABÍA", Y)], "",
  "Close-up on the left half of the frame: the bride from the first reference photo in an ivory lace wedding gown and veil, eyes wet but a cold knowing half-smile, holding her phone at chest height. Behind her, small and out of focus, the groom from the second reference photo in a tuxedo kissing the bridesmaid from the third reference photo in a dusty-rose dress in a dim corridor. Warm candlelight. Right third of the frame is dark and empty."),
 ("ep02", "left", [c("02")["emily"], c("02")["jason"], c("02")["michael"]], [("SE", W), ("RIERON.", Y)], "",
  "Right two thirds: a dark law office with a long mahogany table. In the foreground the woman from the first reference photo, plain dark cardigan, red-rimmed eyes, holding up a single one-dollar bill between two fingers, jaw set. Behind her the two men from the second and third reference photos in expensive suits laughing at her, one pointing. Rainy window light. Left third dark and empty."),
 ("ep03", "left", [c("03")["rachel"], c("03")["adam"]], [("SU OTRA", W), ("FAMILIA", Y)], "",
  "Night, falling snow. Right two thirds: the woman from the first reference photo in a winter coat standing in the snow, face lit by a warm window, tears freezing, hand over her mouth. Through the big window beside her, a cozy living room with a Christmas tree where the man from the second reference photo laughs on a sofa with a different woman and two small children opening presents. Left third dark blue night, empty."),
 ("ep04", "right", [c("04")["emma"], c("04")["victoria"], c("04")["ryan"]], [("TIENES", W), ("10 MINUTOS", Y)], "",
  "Left two thirds: a grand dining room on Thanksgiving, roast turkey and candles. The young woman from the first reference photo stands holding her coat and a small suitcase, calm, chin up, looking straight at camera with a faint dangerous smile. Behind her the older woman from the second reference photo in a burgundy dress points at the door with a smug sneer, and the man from the third reference photo looks away ashamed. Right third dark and empty."),
 ("ep05", "left", [c("05")["thomas"], c("05")["olivia"]], [("ME DIERON", W), ("POR MUERTO", Y)], "",
  "Right two thirds: a white wedding chapel, doors flung open with bright daylight behind. The older man from the first reference photo, in a worn work jacket, stands in the doorway, jaw clenched, eyes wet, staring down the aisle. In the background at the altar, small, the bride from the second reference photo turns in shock and a dark-haired groom in a navy suit glares. Guests turn in their pews. Left third dark and empty."),
 ("ep07", "right", [c("07")["evelyn"], c("07")["anna"], c("07")["richard"]], [("40 AÑOS", W), ("ESPERÁNDOLA", Y)], "",
  "Left two thirds: an open front door at dusk, autumn leaves. The old woman from the first reference photo, silver hair, cardigan, both hands over her heart, tears streaming, facing the woman from the second reference photo who stands on the doorstep in a dark coat holding a bundle of old yellowed letters tied with string. Behind the old woman, the old man from the third reference photo in the hallway, pale with shock. Warm hallway light, Thanksgiving table blurred behind. Right third dark and empty."),
]
spec = {"thumbnail_style": ST, "thumbnails": [
    {"id": e, "side": s, "refs": r, "lines": [{"text": t, "color": col} for t, col in l], "tag": tag, "image": img}
    for e, s, r, l, tag, img in T]}
json.dump(spec, open("karma/es/thumbs_b.json", "w"), ensure_ascii=False, indent=1)
print(len(spec["thumbnails"]), bool(ST))
