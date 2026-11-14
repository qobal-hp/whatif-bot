"""Build the spec for What If It Happens EP02 (long form): What If Humans Lived to 200?

Same engine as Karma Tales (karma/generate_drama.py): one narrator plus Maya's own voice,
Maya drawn from the portrait made for the EP02 short so both videos show the same woman.
Run: python whatif/build_ep02.py  ->  whatif/ep02_long.json
"""
import json
from pathlib import Path

M = "maya"
scenes = []
music = []


def S(image, *lines, maya=True, **extra):
    """One picture and the lines spoken over it. Lines are 'ROLE: text' (no role = narrator)."""
    parsed = []
    for line in lines:
        role, _, text = line.partition(": ") if line.startswith("MAYA: ") else ("NARRATOR", "", line)
        parsed.append([role, text])
    track = extra.pop("music", None)
    scene = {"id": f"L{len(scenes) + 1:03d}", "chars": [M] if maya else [], "image": image, "lines": parsed, "place": ""}
    scene.update(extra)
    scenes.append(scene)
    if track:
        music.append([scene["id"], track])


# ---------- Cold open: show the payoff in the first seconds ----------
S("Maya, looking about 45, blowing out candles on a cake with gold number candles 1-6-0 at a lively family party, close-up, joyful.",
  "[intrigued] This is Maya. Today is her one hundred and sixtieth birthday.", motion="Maya leans in and blows out the candles, flames flicker out, family behind her claps and cheers, confetti falls, slow camera push-in.", music="tension",
  sfx=[["Party poppers and a family crowd cheering at a birthday", 2.5, 0.3, "start"]])
S("Close-up of Maya's face, looking about 45, laughing, laugh lines but no deep wrinkles, warm party lights.",
  "She looks forty-five. She runs three miles every morning. And she just signed up for medical school.", motion="Maya laughs warmly and tilts her head, party lights twinkle softly in the background, gentle handheld camera.")
S("A college dorm move-in day, a smiling 18-year-old girl carrying boxes, Maya beside her carrying a lamp, both laughing.", 
  "Her great-great-great-granddaughter started college last week. They're in the same chemistry class.", motion="The two women walk forward carrying boxes and laugh at each other, students move in the background, tracking shot.")
S("Maya at a kitchen table at night looking at a retirement statement on a tablet, eyebrows raised in disbelief.",
  "[dryly] Her retirement? Seventy years away.")
S("A dramatic wide shot of a futuristic city skyline at golden hour, flying drones and green towers, title-card mood.",
  "What if every human lived to two hundred? Not as frail old people. But aging so slowly that a hundred is just middle age.", motion="Slow aerial drone flight toward the futuristic skyline at golden hour, flying drones glide between green towers.", maya=False, cut=True)
S("A fast montage-style composition: a wedding, a paycheck, a crowded city, a family dinner, arranged as four tiles.",
  "In the next ten minutes, we'll see what it does to your body, your money, your love life... and why the scariest part isn't what you think.", maya=False)

# ---------- Part 1: could this even happen? ----------
S("A Greenland shark gliding through dark icy Arctic water, ghostly and ancient.",
  "First, is this even possible? Nature says... maybe. This is a Greenland shark. Scientists estimate some of them have lived for around four hundred years.", motion="The ancient shark glides slowly toward the camera through dark icy water, particles drift, its tail sways gently.", music="wonder",
  maya=False, cut=True)
S("A bowhead whale surfacing in Arctic sea ice under a pale sky.",
  "Bowhead whales can pass two hundred. One was found with a harpoon tip in its blubber that was made in the eighteen hundreds.", motion="The bowhead whale surfaces and exhales a tall spout of mist, sea ice bobs in the water, slow cinematic motion.", maya=False)
S("A laboratory with mice in clean cages and a scientist in a white coat looking at a vial.",
  "And in the lab, some drugs have already made mice live noticeably longer, even when they started late in life.", maya=False)
S("A vintage birthday cake with candles shaped 1-2-2 on a lace tablecloth in a sunlit old French apartment, no people, nostalgic film look.",
  "The oldest human ever confirmed, Jeanne Calment, reached one hundred and twenty-two. So for us, two hundred would mean breaking the clock itself.", maya=False)
S("A naked mole rat in a sandy underground tunnel, lit like a nature documentary.",
  "Then there's this little guy. The naked mole rat. A rodent the size of a mouse... that can live more than thirty years. Ten times longer than a mouse should.", maya=False)
S("A dramatic microscope view of a human cell with tiny glowing cracks and frayed DNA strands.",
  "So what is aging, really? Mostly, it's damage piling up. Broken DNA. Worn-out cells that refuse to die. Proteins that get stiff and sticky. Year after year, the repairs fall behind.", maya=False)
S("A glowing scientific visualization of a human cell with a slowly turning clock inside it.",
  "So let's imagine it happens. A treatment slows aging down to half speed. Your body ages one year for every two you live.", maya=False)

# ---------- Part 2: your new life timeline ----------
S("Maya at about 20 at a university library, books everywhere, bright and curious.",
  "Childhood stays the same. You still grow up by twenty. But after that... the clock slows.", cut=True)
S("Maya at 50 looking about 35, in a sleek office giving a confident presentation.",
  "At fifty, you look thirty-five. At a hundred, you look like today's fifty-year-olds.")
S("Maya, looking about 40, in a chef's kitchen in a white chef's coat, plating food with intense focus.",
  "MAYA: [laughing] I was an architect for forty years. Then a chef. Now I'm thinking about medicine.")
S("A busy career fair hall where people of visibly mixed apparent ages browse booths together.",
  "Careers would change completely. Nobody stays in one job for a hundred and thirty years. You'd have three, four, maybe five careers.", maya=False)
S("A university lecture hall where a student who looks 40 sits next to students who look 19, all taking notes.",
  "Going back to school at ninety would be totally normal. Your classmates could be eighteen... or a hundred and eighteen.", maya=False)
S("A quiet, half-empty hospital cardiology ward with bright windows and a nurse walking past empty beds.",
  "Your health would change too. Cancer, heart disease, dementia... the big killers today are mostly diseases of aging. Slow the aging, and they get pushed back by decades.", maya=False)
S("A professional football stadium at night, a veteran quarterback who looks 35 but has gray at the temples throwing a pass.",
  "Sports would get strange. An athlete could stay at their peak for forty years. Imagine the same quarterback winning Super Bowls with three different generations of teammates.", motion="The quarterback throws a long spiral pass, the crowd roars and stands up, camera follows the ball briefly.", maya=False,
  sfx=[["A huge stadium crowd roaring", 2.5, 0.25, "start"]])
S("A rider in full gear looking hesitantly at a motorcycle in a garage, then at a 'Life Expectancy 200' poster on the wall.",
  "And here's a twist. If old age stops killing you, accidents become the main danger. Would you still ride a motorcycle... if you had a hundred and fifty years left to lose?", maya=False)

# ---------- Part 3: love and family ----------
S("Maya, looking about 42, in an elegant wedding dress dancing with her new husband under string lights.",
  "And love? This is where it gets weird. 'Till death do us part'... could mean a hundred and seventy years.", music="wonder", cut=True,
  sfx=[["Distant church wedding bells ringing", 2.5, 0.25, "start"]])
S("A sleek modern office with a lawyer handing a couple a contract labeled 'Marriage - 50 Year Term'.",
  "Some people think marriage might start to look like a contract. Fifty years, with an option to renew.", maya=False)
S("Maya, looking about 42, on a first date at a cozy wine bar, smiling a little nervously.",
  "MAYA: [amused] My first date in sixty years. I didn't know what an app was.")
S("A huge Thanksgiving table in a warm dining room with seven generations who all look between 5 and 65, Maya at the head looking about 65 with silver streaks.",
  "Now think about family. If everyone had kids around thirty, Maya at two hundred could share Thanksgiving with seven generations.")
S("Maya, silver-streaked, wagging a finger at a sheepish 30-year-old man across the Thanksgiving table while everyone laughs.",
  "MAYA: [teasing] You're a hundred and ten. Sit up straight.",
  sfx=[["Clinking glasses and cheerful family chatter at a dinner table", 3.0, 0.25, "start"]])
S("A lawyer's office where a man who looks 60 and is 170 waits impatiently, checking his watch, with a will document on the desk.",
  "And inheritance? Your parents might live to two hundred. You could be a hundred and seventy before you inherit a thing.", maya=False)

# ---------- Part 4: money ----------
S("A retirement party banner reading 'HAPPY RETIREMENT' crossed out with red tape, office workers staring at it.",
  "[serious] Now, the money. Today, full retirement age in the US is sixty-seven. In a two-hundred-year world, retiring at sixty-seven means a hundred and thirty years without a paycheck.", music="tension",
  maya=False, cut=True)
S("A government building with a pension office, long lines of ageless-looking people out the door.",
  "No pension system on Earth could pay for that. So almost everyone would keep working... for a very, very long time.", maya=False)
S("A golden glowing coin stack growing into a tower over a timeline from 1 to 150 years.",
  "But here's the upside. Time is the secret ingredient of compound interest. Ten thousand dollars growing at seven percent a year...", maya=False)
S("A shocked young man staring at his glowing phone, mouth open, the screen seen from behind so no numbers are visible.",
  "After forty years, about a hundred and fifty thousand. After a hundred and fifty years? Over two hundred and fifty million dollars. Before inflation, of course.", maya=False,
  sfx=[["A cash register ding", 1.0, 0.35, "end"]])
S("A cozy family-owned bookshop with a sign 'Since 1990' and the same smiling owner behind the counter, looking about 60.",
  "Patient people could become extremely rich. Families could hold wealth for centuries without ever passing it down.", maya=False)
S("A young graduate in a cap and gown holding a diploma, looking at a giant scroll of bills unrolling at her feet.",
  "On the other hand... a thirty-year mortgage? A forty-year student loan? Those suddenly sound short. Banks might offer hundred-year loans.", maya=False)
S("A smiling elderly-looking man who looks about 60 handing his 140th birthday cake slice to coworkers in a busy modern office.",
  "And your coworkers? The guy at the next desk might have a hundred years more experience than you. Good luck getting that promotion.", maya=False)

# ---------- Part 5: housing and crowding ----------
S("A young couple in their late twenties on a sidewalk staring longingly at a charming suburban house with a 'NOT FOR SALE' sign.",
  "[dryly] And that house you want? Your great-grandparents still live in it.", music="wonder", maya=False, cut=True,
  sfx=[["A short burst of a small audience laughing", 1.5, 0.25, "end"]])
S("On the porch of the same house, a cheerful couple who look about 60 but are 170, waving and holding iced tea.",
  "If people stopped dying young, homes would almost never come up for sale. Prices could go through the roof.", maya=False)
S("An extremely crowded futuristic megacity street at rush hour, layered sky bridges, neon and greenery.",
  "And the population would keep growing for a long time. Unless... people had far fewer kids. Which is exactly what many experts think would happen.", maya=False)
S("A packed futuristic subway car at rush hour, ageless commuters in work clothes, Maya squeezed among them holding a coffee.",
  "Fewer babies. Older cities. A world where kids are rare, and a playground is something you have to look for.")
S("Vast vertical farms with glowing LED racks of vegetables inside a skyscraper, workers in white suits.",
  "Feeding everyone would get harder too. More people, living longer, all needing food, water, and energy. Vertical farms and lab-grown meat would stop being a novelty. They'd be survival.", maya=False)
S("A lone small-town street with closed shops and a 'School Closed' sign, autumn leaves blowing.",
  "Meanwhile, some small towns could empty out. Schools close because there aren't enough kids, while retirement homes fill up with people who look forty.", maya=False)

# ---------- Part 6: power ----------
S("The exterior of the US Supreme Court building on a grey day, dramatic low angle.",
  "[ominous] Now here's something most people never think about. Power.", music="tension", maya=False, cut=True)
S("Nine judges' empty high-backed chairs behind a long wooden bench in a grand courtroom.",
  "Supreme Court justices serve for life. In a two-hundred-year world, one justice could sit on that bench for a hundred and fifty years.", maya=False)
S("A boardroom where a powerful CEO who looks 60 sits at the head of a long table, a framed photo behind him dated 1985.",
  "The same billionaire running the same company for a century. The same politicians, the same ideas, never making room.", maya=False)
S("A frustrated young employee looking up at a towering corporate ladder full of people who never move.",
  "Some scientists joke that progress happens one funeral at a time. What happens when the funerals... stop?", maya=False)

# ---------- Part 6b: who gets it? ----------
S("A sleek luxury clinic lobby with marble floors and a price board showing an enormous number, a wealthy couple at reception.",
  "[serious] And that raises the most uncomfortable question of all. Who gets the treatment first?", maya=False, cut=True)
S("A long line of ordinary people in the rain outside a clinic gate, looking at a glowing luxury clinic across the street.",
  "New medicine usually starts out expensive. If only the rich could afford two hundred years, the gap between rich and poor wouldn't just be money anymore. It would be time.", maya=False)
S("Two old friends at a café table: one looks 45, the other looks genuinely elderly with deep wrinkles, holding hands across the table.",
  "Imagine two friends, born the same year. One takes the treatment. One can't. At ninety, one of them looks forty-five... and the other is saying goodbye.", maya=False)
S("A massive peaceful protest crowd in a city square holding blank glowing signs at dusk.",
  "Countries would fight over it. People would protest for it. Some would refuse it, for religious or personal reasons. The world could split in two: the long-lived... and everyone else.", maya=False)
S("Maya, looking about 45, standing in a crowd at a polling station holding a ballot, thoughtful.",
  "MAYA: [thoughtful] When I got it, it cost more than a house. Now it's cheaper than a phone. But those first fifty years... they were ugly.")

# ---------- Part 7: the mind ----------
S("Maya, looking about 60 with silver streaks, sitting by a window holding an old photo album, nostalgic.",
  "And then there's your mind. Your body might stay young. But would your memory keep up?", music="wonder", cut=True)
S("Maya flipping through an old photo album showing a younger Maya with friends who look different, faded photos.",
  "MAYA: [quietly] I've had friends I can't picture anymore. Whole decades that feel like someone else's life.")
S("A golden retriever puppy curled up on Maya's lap in a sunlit living room, Maya gently smiling.",
  "And you'd still say goodbye to the things that don't live as long. Dogs. Cats. Some friends who chose not to take the treatment.")
S("Maya on a couch surrounded by towers of books, vinyl records and a giant TV showing a streaming menu, looking slightly bored.",
  "Then there's boredom. In two hundred years, you could read ten thousand books. Watch every great movie ever made. Visit every country... twice. And then what?")
S("A wise-looking woman who looks 50 teaching a pottery class to young students in a sunlit studio.",
  "But maybe we'd also become wiser. Imagine learning from your mistakes for a hundred and fifty years. Imagine a teacher who has actually lived through two centuries of history.", maya=False)
S("A split image: one side people celebrating in sunshine, the other side a lone person staring at the ocean at dusk.",
  "Some people would love every minute. Others would find two hundred years... exhausting.", maya=False)

# ---------- Ending: callback to Maya ----------
S("Maya, now 200 but looking about 65 with silver hair, alone by a dark window at night, city lights reflected.",
  "[softer, thoughtful] Which brings us back to Maya.", cut=True)
S("Maya, silver-haired, at a small kitchen table in a dim room in front of a cake with candles shaped 2-0-0, empty chairs around her.",
  "It's her two hundredth birthday. Seven generations will come over tomorrow. But tonight, she's alone with a question.",
  sfx=[["A soft low cinematic drone swelling then fading", 4.0, 0.3, "start"]])
S("Close-up of Maya's face lit by candlelight, silver hair, a small sincere smile, eyes glistening.",
  "MAYA: [sincere, gentle] If you could have another hundred years... what would you do with them?")
S("Maya blows out the 2-0-0 candles, smoke curling upward in the dark, hopeful mood.",
  "[warm] Living to two hundred wouldn't just give us more time. It would change what time means. Would you take it? Blessing... or curse? Tell me in the comments. And subscribe, because next time, we're asking an even stranger question.", motion="Maya gently blows out the candles, thin smoke curls upward in the dark room, she smiles softly, slow push-in.",
  sfx=[["Gentle candle blow-out puff", 1.0, 0.35, "start"]])

spec = {
    "title": "What If Humans Lived to 200 Years Old?",
    "aspect": "16:9",
    "resolution": "2K",
    "tail": 2.0,
    "voices": {"NARRATOR": "George", "MAYA": "Matilda"},
    "cast": {M: "video/public/assets/portrait_maya.jpg"},
    "looks": {M: "Maya: shoulder-length wavy dark-brown hair, hazel eyes, light olive skin, a small beauty mark on her left cheek, same face as the reference portrait"},
    "style": "Cinematic photorealistic film still, 16:9 widescreen, shallow depth of field, natural warm color grade, near-future setting, no text other than what is described. ",
    "places": {}, "ambiences": {}, "ambience": [],
    "music": music,
    "scenes": scenes,
    "thumbnail_file": "whatif/ep02_thumb.jpg",
    "youtube": {
        "title": "What If Humans Lived to 200 Years Old?",
        "description": "She's 160. She looks 45. And her retirement is 70 years away. What would living to 200 really do to your body, your money, your love life \u2014 and who gets to live that long first?\n\n0:00 Meet Maya, age 160\n0:36 Could humans really live to 200?\n1:45 Your new life timeline\n2:55 Love, marriage & 7 generations\n3:33 Money: retiring at 67 vs. compound interest\n4:39 Housing, crowding & food\n5:30 Power that never leaves\n5:59 Who gets the treatment first?\n6:49 Memory, boredom & wisdom\n7:39 Maya at 200\n\nA hypothetical science story. Characters and scenes are AI-generated illustrations.\n\n#whatif #longevity #aging #science #future",
        "tags": ["what if", "live to 200", "longevity", "aging", "lifespan", "future", "hypothetical", "science", "compound interest", "what if it happens"],
        "shorts_description": "What if 100 was only middle age? You'd switch careers at 80, fall in love again at 120\u2026 and your great-great-grandma would still be telling you what to do.\nWould you want to live to 200 \u2014 blessing or curse? Tell me below \U0001F447\n\nFull video on the channel.\n\n#whatif #longevity #aging #future #science #hypothetical #shorts"
    },
    "shorts": [{"id": "short1", "youtube_title": "Living to 200 Sounds Great\u2026 Until You See This \U0001F633 #shorts"}],
    "thumbnail_style": "YouTube thumbnail background, hyper-detailed cinematic photorealism, extreme contrast, saturated colors, one huge clear subject readable at tiny size, dramatic rim lighting, 16:9, absolutely no text, no letters, no numbers, no watermark, no logos. ",
    "thumbnails": [
        {"id": "thumb1", "side": "left", "ref": "video/public/assets/portrait_maya.jpg",
         "lines": [{"text": "SHE'S 160", "color": "#FFFFFF"}, {"text": "LOOKS 45", "color": "#FFD400"}], "tag": "WHAT IF WE LIVED TO 200?",
         "image": "The woman from the reference image, looking about 45, fills the right half of the frame in a tight close-up, eyes wide with a mischievous smile, holding up a birthday cake with blazing candles right next to her face, warm golden party light, dark blurred background on the left third."},
        {"id": "thumb2", "side": "right", "ref": "video/public/assets/portrait_maya.jpg",
         "lines": [{"text": "LIVE TO 200?", "color": "#FFFFFF"}, {"text": "BLESSING OR CURSE", "color": "#FFD400"}], "tag": "",
         "image": "Split face composition on the left half of the frame: the left side of the woman's face from the reference image looks about 40 with dark wavy hair, the right side of the same face looks about 70 with silver hair, a sharp glowing line divides them, dramatic dark background, right half of the frame dark and empty."},
        {"id": "thumb3", "side": "left",
         "lines": [{"text": "$10K", "color": "#FFFFFF"}, {"text": "\u2192 $250M", "color": "#FFD400"}], "tag": "IF YOU LIVED 200 YEARS",
         "image": "A shocked young man on the right half of the frame, jaw dropped, eyes huge, holding a glowing smartphone, a towering pile of gold coins and cash erupting behind him, dramatic green and gold light, left third dark and empty."},
    ],
}
ids = {s["id"] for s in scenes}
assert all(cue in ids for cue, _ in spec["music"])
Path(__file__).with_name("ep02_long.json").write_text(json.dumps(spec, indent=1))
words = sum(len(t.split()) for s in scenes for _, t in s["lines"])
print(f"{len(scenes)} scenes, {words} words, ~{words / 150:.1f} min")
