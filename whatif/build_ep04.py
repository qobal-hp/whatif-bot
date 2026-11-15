"""Build the specs for What If It Happens EP04: What If All the Oceans Disappeared Overnight?

Script: the reviewed version in the "What If EP04 — Oceans Vanished (수정본)" doc.
Narrator Will (chosen in the audition), Nora and Mia drawn from portraits made on the first run.
Run: python whatif/build_ep04.py -> whatif/ep04_long.json, ep04_short1.json, ep04_short2.json
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
CAST = {"nora": "video/public/assets/portrait_nora.jpg", "mia": "video/public/assets/portrait_mia.jpg"}
PORTRAITS = {
    "nora": "Photorealistic head-and-shoulders portrait of a Latina woman about 58, sun-weathered skin, grey-streaked black hair in a thick braid, dark brown eyes, navy boat captain's jacket, strong kind face, plain soft grey background, soft window light, 85mm lens.",
    "mia": "Photorealistic head-and-shoulders portrait of a 16-year-old girl, wavy dark-brown hair, light freckles, olive skin, hazel eyes, simple sand-colored linen shirt, curious expression, plain soft grey background, soft window light, 85mm lens.",
}
LOOKS = {
    "nora": "Nora: Latina woman about 58, sun-weathered skin, grey-streaked black braid, navy captain's jacket, same face as her reference image",
    "mia": "Mia: 16-year-old girl, wavy dark-brown hair, light freckles, olive skin, sand-colored linen shirt, same face as her reference image",
}
VOICES = {"NARRATOR": "Will", "NORA": "Sarah", "MIA": "Jessica"}
STYLE_TAIL = "natural documentary color grade, epic scale, present day unless described, no text, no letters, no numbers. "
N, M = ["nora"], ["mia"]
WAVES = ["Gentle ocean waves on a beach with distant seagulls", 6.0, 0.35, "start"]


def builder(prefix, width):
    scenes, music = [], []

    def S(image, *lines, chars=(), **extra):
        parsed = []
        for line in lines:
            role, sep, text = line.partition(": ")
            parsed.append([role, text] if sep and role in VOICES else ["NARRATOR", line])
        track = extra.pop("music", None)
        scene = {"id": f"{prefix}{len(scenes) + 1:0{width}d}", "chars": list(chars), "image": image, "lines": parsed, "place": ""}
        scene.update(extra)
        scenes.append(scene)
        if track:
            music.append([scene["id"], track])
    return scenes, music, S


scenes, music, S = builder("L", 3)

# ---- Chapter 1 — The Morning the Ocean Vanished
S("A cozy beach-house kitchen at sunrise, a hand holding a steaming coffee mug, sheer curtains glowing with morning light, ocean glimpsed beyond.",
  "[relaxed, conversational] Imagine waking up tomorrow. You make your coffee. You pull back the curtains. You look out toward the ocean...",
  sfx=[WAVES], music="wonder")
S("View through an open window at sunrise: where the ocean should be there is only a vast dark empty basin falling away to the horizon, no water anywhere.",
  "[a beat, quieter] And there's no ocean.",
  sfx=[["Sudden total silence after a soft low whoosh", 2.0, 0.3, "start"]],
  motion="Sheer curtains drift in the breeze revealing the vast empty basin where the sea should be, slow push-in.")
S("Wide aerial view of a coastline at dawn ending at a sheer drop into an endless dark empty basin, mist hanging in it.",
  "No waves. No blue line on the horizon. Just a dark, endless emptiness, falling away farther than you can see.")
S("Neighbors in bathrobes standing in a seaside street staring toward the empty coast, one filming with a phone, one screaming. The sea is completely gone: dry seabed, mud and rock where the water used to be, no water anywhere.",
  "[hushed] At first, you think you're still dreaming. You step outside. Your neighbors are standing in the street in their robes, staring at the coast. Someone is screaming. Someone else is filming.")
S("Nora running down a Miami marina dock at sunrise toward empty slips, boats lying in mud far below.",
  "In Miami, Nora Reyes runs down to the marina where she's kept her tugboat for thirty years.", chars=N)
S("Close-up of Nora at the end of the dock, hands on her head in disbelief, looking down. The sea is completely gone: dry seabed, mud and rock where the water used to be, no water anywhere.",
  "NORA: [breathless, disbelieving] No... no, no. Where is it? Where's the water?", chars=N)
S("A red tugboat lying on its side in grey mud forty feet below a marina dock, mooring lines hanging down from the dock.",
  "Her boat is lying on its side in the mud, forty feet below the dock.")
S("The exposed Atlantic seafloor seen from the Florida coast: rock, grey mud and deep canyons stretching to the horizon under a pale sky.",
  "Where the Atlantic was yesterday, there's now a raw landscape of rock, mud, and canyons. It didn't drain. It didn't drift out with the tide.",
  "[flat, stunned] It's just... gone. Every ocean on Earth, gone overnight.",
  sfx=[["A deep low cinematic impact", 2.0, 0.35, "end"]])
S("The California coast seen from cliffs above, the Pacific replaced by an immense empty basin, Highway 1 running along the rim.",
  "In California, the Pacific coast is now the rim of an immense, empty basin.")
S("New York Harbor completely dry, the Statue of Liberty standing above a muddy plain with stranded ferries.",
  "In New York, the harbor isn't a harbor anymore.")
S("The Mariana Trench exposed to the sky, a colossal dark chasm seen from its rim, clouds drifting inside it.",
  "And on the other side of the world, the Mariana Trench lies open to the sky. Almost eleven kilometers deep. Drop Mount Everest into it, and the peak would still be two kilometers below the rim.",
  motion="Slow drone flight over the rim of the colossal chasm as clouds drift down into its depths.")
S("A tiny human figure standing at the edge of the vast trench looking down into darkness, epic scale.",
  "[slow, awed] Imagine standing at that edge. Looking down into the dark. Knowing that yesterday, all of that was water.")
S("Earth seen from space with the oceans gone, continents surrounded by dark brown and white basins, eerie.",
  "[quiet dread] But here's the terrifying part. The missing water isn't the disaster. It's only the beginning. Because the ocean isn't just the blue stuff between continents. It's the engine that keeps this planet alive. And we just switched it off.")
S("A lone lighthouse standing on a cliff above the empty seabed at dusk, its beam sweeping over nothing.",
  "How long before our cities start to fail? Could we survive? And what would Earth look like a hundred years from now? Let's find out. Starting with the first twenty-four hours.")

# ---- Chapter 2 — The First 24 Hours
S("A TV news studio with an emergency banner graphic glow, anchors looking stunned, wall screens showing dry seabeds.",
  "First, the rules. This is impossible. Every drop of seawater disappears, and nothing else changes. The rivers and lakes are still here. The air is still here. Gravity still works. Now... let's play it out.",
  cut=True, music="tension", sfx=[["Emergency broadcast alert tones", 2.5, 0.3, "start"]])
S("A giant container ship settling onto the muddy seabed, tilting, containers sliding, dust and mud splashing. The sea is completely gone: dry seabed, mud and rock where the water used to be, no water anywhere.",
  "[urgent] Within minutes, the world is in a crisis like nothing in history. Every ship at sea has lost the water holding it up. Container ships, tankers, cruise liners, fishing boats. They all settle onto the seabed.",
  motion="The giant container ship slowly lists to one side as it settles into the mud, containers shifting, mud spraying.")
S("A cruise ship broken in half on rocky seafloor, its decks exposed, a cracked hull. The sea is completely gone: dry seabed, mud and rock where the water used to be, no water anywhere.",
  "Some tip over. Some snap in half under stresses they were never built for.")
S("An offshore oil platform standing on tall steel legs above dry seafloor, rigs and cranes silhouetted at dawn.",
  "Oil platforms stand on stilts over dry ground.")
S("Close-up of soft sliding wet sediment and collapsing mud cliffs on the exposed seafloor, treacherous.",
  "And the seafloor isn't a neat, dry desert. It's wet sediment and sliding mud. Cliffs of soft rock. In a lot of places, just walking out there could kill you.")
S("Astonished people on a coastal cliff shading their eyes, looking out at a glittering white expanse. The sea is completely gone: dry seabed, mud and rock where the water used to be, no water anywhere.",
  "[a beat] And then people notice something else. The seafloor is white.")
S("Endless white salt plains glittering under the sun stretching to the horizon, a stranded fishing boat tiny in the distance.",
  "[awed] Seawater is about three and a half percent salt. The water vanished... the salt didn't. All across the old ocean floor, there are now vast plains of salt. In places, tens of meters thick.",
  motion="Low drone glide over endless glittering white salt plains toward a tiny stranded boat, heat shimmer.")
S("Earth from space with oceans turned blinding white, continents dark between them.",
  "From space, the oceans didn't turn brown. They turned white.")
S("A huge silent container port with idle cranes and stacked containers, ships lying in a dry harbor basin. The sea is completely gone: dry seabed, mud and rock where the water used to be, no water anywhere.",
  "Meanwhile, the world's ports go silent. Los Angeles. Shanghai. Rotterdam. Singapore. About eighty percent of everything the world trades travels by sea.")
S("A stranded cargo ship in mud with pallets of medicine boxes and grain sacks visible through broken containers.",
  "Medicine bound for California. Grain crossing the Atlantic. Fuel for half a continent. All of it, stranded in the mud.")
S("A grocery store with empty shelves and a long line of cars at a gas station outside, tense evening.",
  "[tense] Within hours, markets crash. Governments declare emergencies. Grocery stores are stripped bare. Gas stations have lines around the block. And the whole internet asks one question. Where did the water go?")
S("A scientist alone in a dark lab staring at blank ocean data screens, baffled.",
  "[low] Nobody has an answer. And there's a problem coming that almost nobody is thinking about yet.")

# ---- Chapter 3 — The Planet's Air Conditioner Is Gone
S("A family playing in cool waves on a hot summer beach, golden afternoon.",
  "Think about the last time you were at the beach. Even on a hot day, the water felt cool. And in winter, coastal cities stay milder than places inland.", cut=True, music="wonder")
S("A glowing visualization of warm and cold ocean currents looping around the globe like rivers of light.",
  "That's because water holds an incredible amount of heat. The oceans soak it up, carry it around the planet, and slowly let it go. In fact, they've absorbed about ninety percent of the extra heat we've added to the climate. They're the planet's thermal battery.")
S("The same glowing current visualization fading out, leaving a dark empty globe.",
  "[quiet] And that battery is gone.")
S("Split landscape: one side a scorching cracked desert city under a red sun, the other a frozen coastal town in a blizzard.",
  "You might think everywhere just gets hotter. It's stranger than that. Without ocean currents moving heat around, some places swing toward brutal heat, while others slide into deep cold.")
S("A seaside town's promenade with people bundled in coats under a harsh grey sky, empty basin beyond the railings. The sea is completely gone: dry seabed, mud and rock where the water used to be, no water anywhere.",
  "Coastal cities lose the gentle weather they always took for granted. And it wouldn't happen in an afternoon. It would creep in, season by season.")
S("London's Tower Bridge under heavy snow and a grim grey sky, Thames frozen at the edges.",
  "Take Western Europe. London and Paris are mild partly because the Atlantic carries warmth north. Take that away, and their winters could look very different.")
S("The Golden Gate Bridge in harsh clear sunlight with no fog, standing over an empty dry bay.",
  "Or San Francisco. Its famous summer fog rolls in off the Pacific. No Pacific... no fog.")
S("A weather map wall in a forecasting center gone chaotic, meteorologists staring at it.",
  "Nobody can tell you exactly what the new climate looks like. But one thing is certain. Earth would no longer have the climate we know.",
  "[ominous] And we're about to lose something even more important. Rain.")

# ---- Chapter 4 — When the Rain Stops
S("Rain on a window with a blurry green garden behind it, cozy and quiet.",
  "[soft] If it's raining where you are right now, think about where that water came from. Most likely... the ocean.", cut=True,
  sfx=[["Gentle rain on a window slowly fading to silence", 5.0, 0.3, "start"]])
S("Sunlight over the sea with visible vapor rising into towering clouds, the water cycle in action.",
  "About eighty-six percent of all the water that evaporates on Earth rises from the sea. The sun warms the ocean, the water rises, clouds form, and rain falls on our fields and forests.")
S("A sky with thin shrinking clouds over a dry salt basin, harsh sun.",
  "Remove the oceans, and the planet's biggest source of rain disappears.",
  motion="Thin clouds slowly evaporate and vanish across a harsh blue sky over the dry basin, time-lapse.")
S("A lake shore and forest under drifting grey clouds, a hint of drizzle, uneasy light.",
  "The rain wouldn't stop all at once. There's still water in the air. Lakes, rivers, soil and plants keep breathing out moisture. For a while, the sky might even behave strangely. But season by season, the water cycle that has run for billions of years starts to wind down.")
S("A green healthy Kansas wheat field under a big sky, a farmer walking through it in the morning.",
  "Picture a farmer in Kansas. The first summer looks almost normal. The soil is still damp. The wheat is still growing.")
S("The same Kansas field now cracked, dry and brown, the farmer kneeling to touch the broken soil.",
  "But the next season, the rain doesn't come when it should. The reservoirs drop. The fields crack.")
S("A row of empty grain silos and a supermarket price board, worried shoppers, harsh light.",
  "Now multiply that across the whole planet. Wheat. Corn. Rice. Fruit. Almost everything we eat depends on rain. Prices spike. Countries stop exporting food to protect their own people. Nations that import most of their food face real hunger.")
S("A crowded city street at dusk, people of many backgrounds looking up at a cloudless orange sky.",
  "[serious] And that's when this stops being a coastal problem. It becomes everyone's problem.",
  "But we aren't the only ones in trouble.", sfx=[["A quiet slow heartbeat", 3.0, 0.3, "end"]])

# ---- Chapter 5 — The Death of the Ocean World
S("A vibrant coral reef full of colorful fish and a sea turtle, shafts of sunlight, underwater.",
  "[tender] The oceans were home to most of the living space on Earth. Whales. Sharks. Coral reefs. Jellyfish. Countless fish. And creatures so small you'd never see them.", cut=True)
S("The same coral reef now dry, pale, crusted with white salt under harsh sun, no water.",
  "[somber] Without water, almost all of them are gone within days. A few might hang on in isolated pools or deep wet mud. But the largest ecosystem on the planet collapses.")
S("Nora walking alone across a dry pale reef crusted with salt, old whale bones nearby, wind in her braid.",
  "NORA: [quiet, heavy] My father fished these waters. His father too. Now I walk out where the reef used to be... and it's just bones and salt.", chars=N)
S("A small fishing town harbor with boats lying in mud, fishermen sitting idle on the dock, nets drying.",
  "About three billion people rely on fish for a big part of their protein. Fishing towns lose everything overnight. Whole industries disappear.")
S("A macro view of glowing green phytoplankton cells drifting in sunlit water.",
  "And then there's the air. Tiny ocean plants called phytoplankton make about half of the oxygen produced on Earth.")
S("A child taking a deep breath of fresh air on a green hilltop under a blue sky, calm.",
  "[reassuring] So do we suffocate? No. And that's important. Our atmosphere holds a huge reserve of oxygen, enough to last for thousands of years. The air wouldn't run out. But the planet's slow chemistry would start to drift in ways nobody can fully predict.")
S("A dramatic visualization of carbon flowing from smokestacks into a vanished ocean, now just a dry basin.",
  "The oceans also hold about fifty times more carbon than the atmosphere. For a century, they've been quietly soaking up our emissions. Without them, the system that kept Earth's climate steady for millions of years is simply... gone.")
S("A glass of water on a kitchen table in harsh light, a dry landscape outside the window.",
  "[low] And while scientists try to understand this new planet, the rest of us face a much simpler question. Where do we get water to drink?")

# ---- Chapter 6 — The Fight for Fresh Water
S("A dripping kitchen faucet in close-up, a single drop falling.",
  "[a little lighter] Here's the good news. The oceans are gone, but not all the water is. The lakes are still here. The rivers still flow, at least at first. Groundwater is still underground. The glaciers are still frozen.",
  cut=True, sfx=[["A single faucet dripping slowly", 3.0, 0.3, "start"]])
S("A huge glacier and a small blue lake beneath it, tiny compared with a vast dry basin beyond.",
  "[serious] Here's the bad news. About ninety-seven percent of Earth's water was in the oceans. Fresh water was always the tiny remainder. And most of that is locked in ice or buried deep underground.")
S("A long line of people with plastic jugs at a water station in Phoenix heat, desert mountains behind.",
  "Imagine living in Phoenix. For the first few days, the tap still runs. But every reservoir is now being pulled in every direction at once. Drinking water. Farms. Factories. Power plants.")
S("A half-empty reservoir behind a dam with a white bathtub ring on the canyon walls.",
  "Cities start rationing. Farms lose their irrigation. Thirsty industries shut down.")
S("A desalination plant standing idle beside an empty dry seabed, intake pipes hanging over nothing.",
  "And the usual emergency fix? Desalination turns seawater into drinking water. No seawater... no desalination.")
S("Nora standing in a long water line in the Miami heat holding two empty jugs, tired half-smile.",
  "NORA: [tired, half-laughing] Three hours in line for two gallons. Funny. I spent my whole life on the water. Now I stand in line for it.", chars=N)
S("A high-tech water recycling plant with gleaming tanks and an indoor vertical farm next to it.",
  "The richest countries race to build new systems. Recycling every drop of wastewater. Catching every bit of rain that still falls. Growing food indoors. But nothing can replace an ocean. And you can't recycle water you don't have.")
S("A glowing city built around a lake in a dry landscape at dusk, other distant cities dark.",
  "[slow] Imagine a world where the cities that survive aren't the richest or the most powerful... but the ones sitting on fresh water. The most ordinary thing in your kitchen has become the most valuable thing on Earth.",
  "[ominous] And as the years pass, people notice something even stranger. The ground itself is moving.")

# ---- Chapter 7 — The Planet Underneath
S("A dramatic cross-section of Earth's crust under a dry ocean basin, layers of rock, glowing mantle below.",
  "Here's something almost nobody thinks about. Water is heavy. The oceans hold about one point three billion cubic kilometers of it. More than a billion billion tons, pressing down on the planet's crust.",
  cut=True, music="tension", sfx=[["A deep low geological rumble", 4.0, 0.35, "start"]])
S("Raised old beaches as stepped terraces on a rocky coast in northern Canada, far above the old waterline.",
  "Take that weight away, and the crust begins to rise. Slowly. We've actually seen this happen. When the giant ice sheets of the last Ice Age melted, the land beneath them began to lift. In parts of Canada and Scandinavia, it's still rising today.")
S("A long crack opening across a salt plain with a faint plume from a distant volcano.",
  "Removing the oceans would be that, on a planetary scale. Nobody can say exactly where the stress would build, or when. Not every volcano erupts at once. But the ground beneath our feet would not stay still.")
S("The exposed Mid-Atlantic Ridge as a colossal mountain chain stretching to the horizon across white salt plains, epic.",
  "[awed] And the world would look like an alien planet. The Mid-Atlantic Ridge, a mountain chain longer than any on land, would rise across the old Atlantic.",
  motion="Slow sweeping aerial flight along the colossal mountain ridge rising out of the white salt plains.")
S("A black undersea volcano standing alone on endless white salt, a deep trench like a scar beside it.",
  "Trenches would gape like wounds. Undersea volcanoes would stand alone on endless salt.")
S("Crumbling sediment cliffs and a gigantic canyon on the exposed seafloor, a tiny off-road truck at the edge.",
  "And don't picture easy new highways between continents. Out there are cliffs of crumbling sediment, salt flats, and canyons that make the Grand Canyon look small. Every map we've ever drawn... would be useless.")
S("An old paper world map on a table, its blue oceans faded, a compass resting on it, dusty light.",
  "So what does Earth look like a century later? Do we rebuild? Or do we slowly fade away?")

# ---- Chapter 8 — One Hundred Years Later
S("Aerial view over what used to be the Pacific: mountains, trenches and endless white plains, a small blue lake with green plants at its edge.",
  "[reflective] A hundred years have passed. Imagine flying over what used to be the Pacific. Below you is a landscape no human was ever meant to see. Mountains. Trenches. Endless white plains. Here and there, a small lake fed by rain or groundwater, with a few stubborn plants around its edges.",
  cut=True, music="wonder", sfx=[["Wind sweeping across an empty landscape", 5.0, 0.3, "start"]])
S("A farming belt shifted north: green fields beside an old abandoned southern farm town in the dust.",
  "The great forests have shifted. The farming belts have moved. And people live where the water is.")
S("A small domed city glowing in a dry valley at dusk, greenhouses and solar panels around it.",
  "Picture one of those cities. Every building is designed to save water. Food grows indoors, under lights. Every drop is recycled again and again.")
S("Children in a domed city classroom looking at a water meter display on the wall, curious.",
  "Children grow up knowing exactly how many gallons their family gets each week.")
S("A lone traveler on a ridge overlooking a mostly empty land with a few distant settlements, dusk.",
  "Could a civilization like this survive? Maybe. But far fewer people would be alive. Some regions would still be livable. Others would be almost impossible. It would all depend on how much fresh water was left, how the climate settled... and whether people chose to cooperate, or to fight.")
S("An old photograph of the ocean lying on a wooden table in warm lamp light.",
  "[a beat, quieter] But there's one possibility we haven't talked about. What if the oceans came back?")

# ---- Chapter 9 — The Final Twist
S("A small town built on the old seafloor: houses, farms and roads across white salt, a sheer old continental cliff behind.",
  "A century has gone by. Whole generations have never seen a wave. There are towns now, built down on the old seafloor. Roads across the salt. Farms in the ancient basins.",
  cut=True, sfx=[["Silence then a faint distant rumble", 4.0, 0.25, "end"]])
S("Mia sitting on her bedroom floor in a seafloor town, looking at an old faded photograph of a woman on a tugboat at sea.",
  "Nora's great-granddaughter, Mia, lives in one of them. She's sixteen. She's only ever seen the ocean in Nora's old photographs.", chars=M)
S("Close-up of Mia holding the old photograph, wistful, warm window light.",
  "MIA: [curious, wistful] Great-grandma Nora used to say the sea had a sound. Like breathing. I always wondered what she meant.", chars=M)
S("Dawn over the seafloor town, people stopping in the street and turning toward a distant rising roar and a dark line on the horizon.",
  "Then one morning...", sfx=[["A deep rising roar of approaching water", 4.0, 0.4, "start"]], music="tension")
S("A colossal wall of blue water rising out of thin air across the salt plains, towering over a tiny seafloor town.",
  "[urgent, hushed] The water comes back. Every ocean. Every sea. All at once. Not over thousands of years. Instantly.",
  motion="An enormous wall of blue water surges across the white salt plain toward the tiny town, spray rising, epic slow motion.")
S("An abandoned ship on the dry seabed with water suddenly rising around it, roads disappearing under blue water.",
  "Every town on the seafloor. Every road. Every farm. Swallowed in a single moment. A second catastrophe, caused not by the oceans leaving... but by them coming home.")
S("Mia standing alone on a high ridge above a flooded basin, staring at endless blue ocean for the first time, wind in her hair.",
  "Mia stood on the ridge above what used to be her town. And for the first time in her life... she heard it.", chars=M,
  sfx=[WAVES],
  motion="Gentle waves roll in below the ridge as Mia's hair moves in the sea breeze, slow push-in on her face.")
S("Close-up of Mia's face with tears and wonder, ocean light reflecting in her eyes.",
  "MIA: [whispering, awed and afraid] Oh... It really does sound like breathing.", chars=M)
S("A calm blue ocean horizon at sunrise from a beach, waves rolling in, peaceful.",
  "[warm, slow] We think of the oceans as empty space between the places we live. Something we fly over. Something we visit on vacation. But they're not separate from our world. They're the machinery that keeps it running. They move the heat. They make the rain. They feed billions of people. They keep the climate steady. Without them, Earth wouldn't just be a planet with more land. It would be a completely different world.",
  music="wonder")
S("Footprints on wet sand as a wave rolls in at golden hour, intimate.",
  "[soft] So the next time you're standing on a beach, watching a wave roll in... remember. That water isn't just scenery. It's part of the reason you're alive.")
S("Earth from space, oceans brilliant blue again, a soft sunrise along the edge.",
  "[final, quiet] What if the oceans disappeared tomorrow? The scariest question isn't where the water went. It's how long we'd last without it.",
  overlay={"type": "text", "text": "WHAT IF IT HAPPENS|The impossible, explored."})

LONG = {
    "title": "What If All the Oceans Disappeared Overnight?",
    "aspect": "16:9", "resolution": "2K", "tail": 3.0,
    "voices": VOICES, "cast": CAST, "portraits": PORTRAITS, "looks": LOOKS,
    "style": "Cinematic photorealistic film still, 16:9 widescreen, " + STYLE_TAIL,
    "places": {}, "ambiences": {}, "ambience": [], "music": music, "scenes": scenes,
    "thumbnail_file": "whatif/ep04_thumb.jpg",
}

# ---- Short 1 — You Wake Up and the Ocean Is Gone
s1, m1, S = builder("a", 2)
S("Vertical view through an open window at sunrise where the ocean should be: a vast dark empty basin to the horizon.",
  "[relaxed, conversational] You wake up. You pull back the curtains... and there's no ocean.", music="tension", sfx=[WAVES],
  motion="Curtains drift open revealing the vast empty basin, slow push-in.")
S("A red tugboat lying on its side in mud far below a marina dock.", "Every ocean on Earth. Gone overnight.")
S("Nora at the end of a marina dock staring down in disbelief, hands on her head, below the dock only mud and stranded boats, the sea completely gone, no water anywhere.", "NORA: [breathless] Where is it? Where's the water?", chars=N)
S("A giant container ship tilting as it settles onto a dry muddy seabed, the sea completely gone, no water anywhere.", "[urgent] Ships collapse onto the seabed. Ports go silent.")
S("Endless glittering white salt plains to the horizon.", "[awed] And the seafloor? It's white. Salt, tens of meters thick.")
S("Thin clouds vanishing over a dry basin.", "Then the rain starts to fade. Because most of it came from the ocean.")
S("A long line of people with jugs at a water station in the heat.", "[serious] And soon, the most valuable thing on Earth... is a glass of water.")
S("Earth from space with its oceans turned white.", "[quiet] How long would we last?",
  overlay={"type": "text", "text": "FULL EPISODE|ON THE CHANNEL"})
SHORT1 = dict({k: v for k, v in LONG.items() if k != "thumbnail_file"}, title="You Wake Up and the Ocean Is Gone",
              title_band="WHAT IF THE OCEANS|VANISHED OVERNIGHT?", aspect="9:16", tail=2.5, scenes=s1, music=m1,
              style="Cinematic photorealistic film still, vertical 9:16 composition with the subject centered, " + STYLE_TAIL)

# ---- Short 2 — The Day the Oceans Came Back
s2, m2, S = builder("b", 2)
S("Vertical shot of a small town built on white salt plains on the old seafloor, a giant old cliff behind.",
  "[relaxed, conversational] A hundred years after the oceans vanished, people live on the old seafloor.", music="tension")
S("Mia in her small bedroom in a town on the dry old seafloor, holding an old photograph of a woman on a tugboat, white salt plains visible through the window, no sea.", "Mia is sixteen. She has never seen a wave.", chars=M)
S("Close-up of Mia, wistful.", "MIA: [wistful] Great-grandma said the sea sounded like breathing.", chars=M)
S("Ordinary townspeople in simple clothes standing in a dusty street of a small town on dry white salt plains at dawn, turning toward a dark line on the horizon.", "Then one morning...",
  sfx=[["A deep rising roar of approaching water", 3.0, 0.4, "start"]])
S("A colossal wall of blue water rising across the salt plains toward a tiny town.", "[urgent, hushed] The oceans come back. All at once.",
  motion="An enormous wall of water surges across the salt plain toward the tiny town, epic slow motion.")
S("Mia alone on a high ridge above a flooded basin staring at the ocean for the first time.", "And for the first time... she hears it.", chars=M, sfx=[WAVES])
S("Mia seen from behind on a high grassy ridge, wind in her hair, looking out over an endless calm blue ocean at sunrise.", "MIA: [whispering] It really does sound like breathing.", chars=M,
  overlay={"type": "text", "text": "FULL STORY|ON THE CHANNEL"})
SHORT2 = dict(SHORT1, title="The Day the Oceans Came Back", title_band="THE DAY THE OCEANS|CAME BACK", scenes=s2, music=m2)

LONG["youtube"] = {
    "title": "What If All the Oceans Disappeared Overnight?",
    "category": "28",
    "description": "",
    "tags": ["what if", "oceans disappeared", "no ocean", "earth without oceans", "science", "hypothetical",
             "climate", "water cycle", "mariana trench", "what if it happens"],
}
LONG["shorts"] = [
    {"id": "short1", "youtube_title": "You Wake Up and the Ocean Is Gone \U0001F30A #shorts",
     "description": "Every ocean on Earth, gone overnight. What happens next?\nFull episode on the channel: What If All the Oceans Disappeared Overnight?\n\n#whatif #ocean #science #shorts"},
    {"id": "short2", "youtube_title": "She Had Never Seen a Wave... Until Today \U0001F30A #shorts",
     "description": "A hundred years after the oceans vanished, they came back. All at once.\nFull story on the channel.\n\n#whatif #ocean #story #shorts"},
]

for name, spec in (("ep04_long.json", LONG), ("ep04_short1.json", SHORT1), ("ep04_short2.json", SHORT2)):
    ids = {s["id"] for s in spec["scenes"]}
    assert all(cue in ids for cue, _ in spec["music"]), name
    assert {r for s in spec["scenes"] for r, _ in s["lines"]} <= set(VOICES)
    (HERE / name).write_text(json.dumps(spec, indent=1))
    words = sum(len(t.split()) for s in spec["scenes"] for _, t in s["lines"])
    print(f"{name}: {len(spec['scenes'])} scenes, {words} words, ~{words / 150:.1f} min, clips {sum(1 for s in spec['scenes'] if s.get('motion'))}")
