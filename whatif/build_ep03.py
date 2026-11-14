"""Build the specs for What If It Happens EP03: What If the World's Population Doubled Overnight?

Long form (L ids) and the short (s ids). Ethan, a Chicago delivery driver, carries the story;
his portrait is drawn on the first run and reused by the second.
Run: python whatif/build_ep03.py  ->  whatif/ep03_long.json, whatif/ep03_short.json
"""
import json
from pathlib import Path

E_ = "ethan"
LOOKS = {E_: "Ethan: early 30s man, short dark-blond hair, light stubble, blue-grey eyes, a small scar through his left eyebrow, wearing a navy work jacket, same face as the reference portrait"}
PORTRAIT = "Photorealistic head-and-shoulders portrait of a man in his early 30s, short dark-blond hair, light stubble, blue-grey eyes, a small scar through his left eyebrow, navy work jacket, friendly tired expression, plain soft grey background, soft window light, sharp focus, 85mm lens."
CAST = {E_: "video/public/assets/portrait_ethan.jpg"}
STYLE_TAIL = "shallow depth of field, natural cinematic color grade, present-day setting, no text other than what is described. "


def builder(prefix, width):
    scenes, music = [], []

    def S(image, *lines, ethan=True, **extra):
        parsed = [["ETHAN", l[7:]] if l.startswith("ETHAN: ") else ["NARRATOR", l] for l in lines]
        track = extra.pop("music", None)
        scene = {"id": f"{prefix}{len(scenes) + 1:0{width}d}", "chars": [E_] if ethan else [], "image": image, "lines": parsed, "place": ""}
        scene.update(extra)
        scenes.append(scene)
        if track:
            music.append([scene["id"], track])
    return scenes, music, S


# ================= LONG FORM =================
scenes, music, S = builder("L", 3)

# Cold open
S("Ethan in a small Chicago apartment at dawn, opening his front door in boxers and a T-shirt, the hallway outside packed shoulder to shoulder with confused strangers in pajamas.",
  "[intrigued] Six a.m. Ethan opens his front door... and the hallway is full of people he has never seen in his life.", music="tension",
  motion="Ethan slowly opens the door and freezes, the crowd of confused strangers in the hallway turns to look at him, handheld camera.")
S("Wide shot of a Chicago street at sunrise jammed with thousands of bewildered people in pajamas and blankets, cars stuck, steam rising from vents.",
  "Outside, it's the same. Every street. Every city. Every country.", ethan=False,
  motion="Slow drone push over the crowded street, people mill around confused, steam drifts from street vents.")
S("A giant digital world population counter on a dark screen glowing, numbers blurred and spinning, dramatic light.",
  "Overnight, the world's population has doubled. From about eight billion people... to over sixteen billion.", ethan=False)
S("A mixed crowd of new arrivals of every age — babies in arms, kids, grandparents — standing in a parking lot with nothing, no bags, looking around.",
  "Every new person is real. Babies, kids, grandparents. But they arrived with nothing. No home. No job. No ID. Not even a bank account.", ethan=False)
S("Ethan on his apartment balcony staring down at the packed street, holding a coffee cup, stunned.",
  "ETHAN: [stunned, half-laughing] Okay... who are all these people?")
S("A split composition: a calm clock reading 6:00 and a cracked clock reading 6:00 one year later, symbolic, dark background.",
  "It took humanity forty-eight years to go from four billion people to eight billion. Today it happened in one night. In the next ten minutes, we'll follow the first hour, the first week, and the first year... and find out if we'd survive it.", ethan=False, cut=True)
S("A world map glowing with population hotspots, India and China burning brightest, dark oceans, infographic style without text.",
  "And they didn't appear randomly. Every place doubled. Tokyo, Lagos, Sao Paulo, Chicago. India and China each gained more than a billion people in a single night.", ethan=False)

# Hour one
S("A cell phone screen showing 'No Service' held by a worried woman in a crowd, many people holding up phones searching for signal.",
  "[urgent] Hour one. Eight billion people reach for a phone at the same time... except half of them don't have one. And the half that do can't get a signal.", ethan=False, cut=True, music="tension")
S("A busy 911 dispatch center with every operator on a call and every line blinking red.",
  "Cell networks are built for a normal busy day. Not for double. Emergency lines overflow within minutes.", ethan=False)
S("A packed subway platform in Chicago, people pressed against the train doors, nobody can get on.",
  "Rush hour is impossible. Trains, buses, roads... everything was sized for half as many people.", ethan=False,
  motion="The packed train doors try to close and bounce back open on bodies, crowd sways, handheld camera.")
S("Ethan in his delivery van stuck in gridlock traffic, honking cars everywhere, pedestrians walking between the cars.",
  "ETHAN: [frustrated] I deliver groceries for a living. Today I can't even get out of the parking lot.")
S("A wall of frozen streaming screens and spinning loading icons in a dim living room, a family staring at them.",
  "The internet crawls. Streaming freezes. Banking apps time out. The digital world was built for eight billion users, and sixteen billion just logged on.", ethan=False)
S("A government office overwhelmed with endless lines of people holding paper forms, clerks buried under stacks of documents.",
  "And then there's paperwork. Eight billion people with no birth certificate, no Social Security number, no address. Governments would face the biggest registration job in history, just to know who exists.", ethan=False)

# Day one to three: food
S("A supermarket at 9 a.m. with nearly empty shelves and a crowd pushing carts, a few bags of rice left.",
  "[serious] Day one. And the first real problem... is food. Most supermarkets only hold a few days of stock. With twice the shoppers, the shelves are empty by lunch.", ethan=False, cut=True)
S("An enormous grain silo farm under a dramatic sky, harvest trucks lined up.",
  "Here's the math. Right now, the world grows enough food to give every person roughly twenty-nine hundred calories a day. That's more than we need.", ethan=False)
S("A dinner plate cut neatly in half with a knife, one half empty, dramatic overhead light.",
  "Cut that in half... and everyone gets about fourteen hundred and fifty. Below what an adult body needs. For everyone. Everywhere.", ethan=False)
S("Long lines of people at a food distribution point run by volunteers in a stadium parking lot.",
  "Governments would open emergency reserves. But grain stockpiles are measured in months, not years. The clock starts ticking.", ethan=False)

# Week one: water, power, hospitals
S("A city water tower against a hazy sky, a gauge on a pipe showing pressure dropping into the red.",
  "Week one. Water systems start to struggle. Pumps, pipes and treatment plants were designed for the population we had yesterday.", ethan=False, cut=True)
S("A city skyline at night with entire neighborhoods going dark in rolling blackouts, only a few towers still lit.",
  "Power grids keep only a small safety margin above normal demand. Double the people, double the phones, heaters and air conditioners... and the lights start going out.", ethan=False,
  motion="Blocks of city lights switch off one after another across the skyline, slow camera drift.")
S("A crowded hospital emergency room with patients on chairs and floors, exhausted nurses.",
  "Hospitals? The US has fewer than three hospital beds for every thousand people. Overnight, that becomes about one and a half.", ethan=False)
S("Ethan helping an elderly stranger sit down on the stairs of his building, handing her a bottle of water.",
  "ETHAN: [softly] Her name's Rosa. She just... appeared in my building's stairwell. She's eighty. She has nowhere to go.")
S("An overflowing elementary school classroom with sixty kids squeezed into desks meant for thirty, a frazzled teacher.",
  "Schools reopen with twice the kids and the same number of teachers. Classes of sixty. Kids learning in hallways, gyms and cafeterias.", ethan=False)
S("Farmland irrigation sprinklers spraying over dry fields under a hot sun, cracked earth at the edges.",
  "And the real water problem isn't your faucet. About seventy percent of the fresh water humans use goes to farming. To grow twice the food, we'd need far more water than many rivers can give.", ethan=False)

# Month one: housing
S("A football stadium turned into a giant shelter, rows of cots across the field, Red Cross tents.",
  "Month one. Every stadium, school gym and convention center becomes a shelter. And it's still not enough.", ethan=False, cut=True, music="wonder",
  motion="Slow aerial pull-back over the stadium field filled with cots and people, volunteers walking between rows.")
S("A sprawling tent city on the edge of a modern city, smoke from cooking fires, children playing between tents.",
  "Tent cities spread around every major city on Earth. Eight billion people need a roof... and building that many homes would take decades.", ethan=False,
  motion="Slow pan across the tent city as cooking smoke drifts and children run between tents, golden light.")
S("Ethan's tiny apartment living room now crowded with a family of four strangers sleeping on the floor and the couch, Ethan stepping over them with a coffee.",
  "ETHAN: [wry] My one-bedroom has six people in it now. We take turns with the shower. I'm not complaining. Okay... I'm complaining a little.")
S("A real estate office window with rent prices in red skyrocketing, shocked passersby staring.",
  "And if you rent? With twice the demand and the same number of homes, rents explode. A one-bedroom could cost what a house did last year.", ethan=False)
S("A packed outdoor bar at night full of young people laughing and flirting, warm string lights.",
  "[playful] Not everything is bad news, though. If you're single... your dating pool just doubled. Overnight.", ethan=False)
S("A sold-out baseball stadium with fans packed into every seat and even standing in the aisles, sunny day.",
  "Concerts, ballgames, theme parks? Twice the fans fighting for the same seats. Good luck getting tickets ever again.", ethan=False)

# Jobs and economy
S("A massive line of job seekers wrapped around a city block outside a warehouse with a 'Now Hiring' banner.",
  "[thoughtful] Now, money. Billions of new people need work. In the short term, that's a disaster. Too many workers, too few jobs. Wages drop.", ethan=False, cut=True, music="tension")
S("A busy construction site at sunrise with hundreds of workers framing new apartment buildings, cranes overhead.",
  "But look closer. Everyone needs homes, food, clothes, power. That's the biggest wave of demand in history. Construction, farming and energy would boom.", ethan=False)
S("A young woman in a makeshift classroom in a tent city teaching kids with a small whiteboard, focused.",
  "And here's the part people forget. Twice as many people also means twice as many doctors, inventors and engineers. Twice the chance of the next Einstein.", ethan=False)
S("A bustling market street in a city with new shops opening, busy shoppers, energetic mood.",
  "Economists would argue about this for decades. In the long run, more people usually means a bigger economy. More workers, more customers, more ideas. The hard part is surviving the first few years.", ethan=False)

# Food fix
S("A huge dumpster behind a supermarket overflowing with perfectly good fruit, vegetables and bread.",
  "[upbeat] So could we actually feed sixteen billion? Maybe. First, about a third of all the food we produce today is lost or wasted. Stop that... and the math changes fast.", ethan=False, cut=True, music="wonder")
S("Vast green pastures with grazing cattle stretching to the horizon, golden hour.",
  "Second, meat. Livestock uses most of the world's farmland, but provides less than a fifth of our calories. Grow food for people instead of for cows, and the same land feeds far more people.", ethan=False)
S("A glowing indoor vertical farm with stacked racks of lettuce under pink LED lights, workers in white suits.",
  "Add vertical farms, better crops, and more fishing... and sixteen billion becomes possible. Not easy. Not comfortable. But possible.", ethan=False)
S("A scientist in a lab looking at a glowing hologram of Earth with numbers floating around it, thoughtful.",
  "So how many people can Earth actually hold? Scientists have argued about this for a century. Their estimates range from under two billion... to well over a hundred billion. The answer depends almost entirely on how we live.", ethan=False)
S("A family eating a simple plant-based meal at a small kitchen table, warm light.",
  "Sixteen billion people living like the average American? Impossible. Sixteen billion people eating more plants, sharing more, wasting less? That's a different story.", ethan=False)

# Nature and climate
S("A rainforest edge being cleared by bulldozers, smoke rising, a toucan watching from a branch.",
  "[serious] But nature pays the bill. More farms means more forests cut down. More cities means less space for animals.", ethan=False, cut=True)
S("Factory smokestacks and highways at dusk under an orange polluted sky.",
  "And emissions? Twice the people driving, heating and cooking could push carbon emissions toward double. Climate goals would be thrown out the window.", ethan=False)
S("An empty quiet beach at sunrise with a single set of footprints, peaceful.",
  "Quiet places disappear. Empty beaches, open roads, a seat on the train. Those become luxuries.", ethan=False)
S("A maternity ward nursery with rows of newborn babies in cribs, nurses walking between them.",
  "And it doesn't stop. Twice as many people means roughly twice as many babies every year. Unless families choose to have fewer kids, the curve keeps climbing.", ethan=False)
S("A busy international airport terminal with endless queues at passport control.",
  "Borders, visas and citizenship would become the hottest debate on the planet. Every country would have to decide how to handle billions of people who, on paper, don't exist.", ethan=False)
S("A calm graph-like landscape: a gentle hill of glowing light rising and flattening on the horizon at dawn, symbolic.",
  "For comparison, in our real world, the United Nations expects the population to peak around ten billion later this century. Sixteen billion would blow far past anything we've ever planned for.", ethan=False)

# Year one
S("A city one year later: rows of brand-new modular apartment blocks rising beside the old skyline, cranes everywhere.",
  "[hopeful] Year one. And something surprising happens. Humans adapt. Factories run around the clock. New neighborhoods rise in months, not years.", ethan=False, cut=True, music="wonder")
S("A long communal dinner in a converted warehouse, new arrivals and locals eating together, string lights.",
  "Strangers become neighbors. Neighbors become friends. Cities get louder, more crowded, more alive.", ethan=False)
S("Ethan driving his delivery van on a busy but moving street with Rosa riding in the passenger seat, both laughing.",
  "ETHAN: [warm] Rosa helps me with deliveries now. She knows more about the city than I do. Turns out she ran a bakery for forty years.")
S("A gleaming dense city ten years in the future with towering green residential towers, elevated trains and rooftop farms, bright morning.",
  "Ten years later, the world looks different. Taller cities. Faster trains. Rooftop farms on every block. Some countries handle it brilliantly. Others are still struggling. And everyone remembers exactly where they were the morning the world doubled.", ethan=False,
  motion="Slow cinematic drone glide between green residential towers as an elevated train passes, morning light.")

# Ending
S("A view from space of Earth at night, city lights twice as dense and bright as today, glowing.",
  "[reflective] So would doubling humanity destroy us? Probably not. But it would test everything. Our food, our cities, our patience... and our kindness.", ethan=False, cut=True)
S("Ethan on a rooftop at sunset looking over a dense glowing city, Rosa and the new family beside him, quiet.",
  "ETHAN: [thoughtful] Sixteen billion people. Feels like the end of the world some days. Other days... it feels like the start of a new one.",
  motion="Slow orbit around Ethan and his new neighbors on the rooftop as the city lights flicker on, warm sunset.")
S("Close-up of a crowded city crosswalk from above, hundreds of people crossing in every direction, beautiful pattern.",
  "Would you want to live in a world with twice as many people? Blessing... or nightmare? Tell me in the comments. And subscribe, because next time we're asking an even crazier question.", ethan=False)

long = {
    "title": "What If the World's Population Doubled Overnight?",
    "aspect": "16:9", "resolution": "2K", "tail": 2.0,
    "voices": {"NARRATOR": "George", "ETHAN": "Will"},
    "cast": CAST, "portraits": {E_: PORTRAIT}, "looks": LOOKS,
    "style": "Cinematic photorealistic film still, 16:9 widescreen, " + STYLE_TAIL,
    "places": {}, "ambiences": {}, "ambience": [],
    "music": music, "scenes": scenes,
    "youtube": {
        "title": "What If the World's Population Doubled Overnight?",
        "description": "",
        "tags": ["what if", "population", "overpopulation", "16 billion", "world population", "hypothetical", "science", "future", "food", "what if it happens"],
        "shorts_description": "",
    },
    "shorts": [{"id": "short1", "youtube_title": "You Wake Up and There Are 16 Billion People \U0001F633 #shorts"}],
    "thumbnail_style": "YouTube thumbnail background, hyper-detailed cinematic photorealism, extreme contrast, saturated colors, one huge clear subject readable at tiny size, dramatic rim lighting, 16:9, absolutely no text, no letters, no numbers, no watermark, no logos. ",
    "thumbnails": [
        {"id": "thumb1", "side": "left", "ref": CAST[E_],
         "lines": [{"text": "16 BILLION", "color": "#FFD400"}, {"text": "OVERNIGHT", "color": "#FFFFFF"}], "tag": "WHAT IF?",
         "image": "The man from the reference image on the right half of the frame, in pajamas, standing in his open apartment doorway with a shocked face, the hallway behind him jammed with hundreds of strangers, dramatic light, left third dark and empty."},
        {"id": "thumb2", "side": "right",
         "lines": [{"text": "TWICE THE", "color": "#FFFFFF"}, {"text": "PEOPLE", "color": "#FFD400"}], "tag": "HALF THE FOOD",
         "image": "An impossibly crowded city street seen from above on the left half of the frame, an ocean of people packed shoulder to shoulder between skyscrapers, one empty supermarket cart in the foreground, right half darker and empty."},
        {"id": "thumb3", "side": "left",
         "lines": [{"text": "EARTH", "color": "#FFFFFF"}, {"text": "x2", "color": "#FFD400"}], "tag": "COULD WE SURVIVE?",
         "image": "Planet Earth at night on the right half of the frame with city lights blazing impossibly bright and dense, glowing like it is overloaded, a faint ghost duplicate of Earth behind it, black space on the left."},
    ],
}

# ================= SHORT =================
ss, smusic, S = builder("s", 2)
S("Ethan opening his apartment door at dawn in a T-shirt, the hallway behind it packed with confused strangers in pajamas, vertical close-up.",
  "[intrigued] You wake up... and there are sixteen billion people on Earth.", music="tension",
  motion="Ethan opens the door and freezes as the crowd of strangers turns toward him, handheld.")
S("A Chicago street at sunrise jammed with thousands of bewildered people, vertical aerial view.",
  "The population doubled overnight.", ethan=False)
S("A supermarket with completely empty shelves and a crowd pushing carts.",
  "[urgent] By lunch, the supermarkets are empty.", ethan=False)
S("A dinner plate cut neatly in half with a knife, one half empty, overhead light.",
  "The world grows enough food for everyone... once. Split it in half, and nobody gets enough.", ethan=False)
S("A city skyline at night with neighborhoods going dark in rolling blackouts.",
  "Week one. The power grid can't keep up. Blackouts roll from city to city.", ethan=False)
S("A football stadium turned into a giant shelter, rows of cots across the field.",
  "Every stadium becomes a shelter. And it's still not enough.", ethan=False)
S("Ethan's tiny apartment crowded with a family of strangers sleeping on the floor, Ethan stepping over them holding coffee.",
  "ETHAN: [wry] My one-bedroom has six people in it now.")
S("A massive line of job seekers wrapped around a city block.",
  "[serious] Billions need jobs. Wages crash. Rents explode.", ethan=False)
S("A young woman teaching kids on a whiteboard in a tent-city classroom.",
  "[hopeful] But twice the people also means twice the doctors... twice the inventors... twice the chance of the next Einstein.", ethan=False)
S("Earth at night from space with city lights twice as dense and bright.",
  "[thoughtful] So... would we survive?", ethan=False, cut=True)
S("An impossibly crowded crosswalk seen from above, hundreds crossing in every direction.",
  "Would you want to live in a world with twice as many people?", ethan=False,
  overlay={"type": "text", "text": "Blessing|or nightmare?"})

short = dict(long, title="What If the Population Doubled? (Short)", title_band="WHAT IF THE WORLD|DOUBLED OVERNIGHT?",
             aspect="9:16", tail=3.0, scenes=ss, music=smusic,
             style="Cinematic photorealistic film still, vertical 9:16 composition with the subject centered, " + STYLE_TAIL)
for k in ("youtube", "shorts", "thumbnails", "thumbnail_style"):
    short.pop(k)

for name, spec in (("ep03_long.json", long), ("ep03_short.json", short)):
    ids = {s["id"] for s in spec["scenes"]}
    assert all(cue in ids for cue, _ in spec["music"])
    Path(__file__).with_name(name).write_text(json.dumps(spec, indent=1))
    words = sum(len(t.split()) for s in spec["scenes"] for _, t in s["lines"])
    print(f"{name}: {len(spec['scenes'])} scenes, {words} words, ~{words / 150:.1f} min, clips {sum(1 for s in spec['scenes'] if s.get('motion'))}")
