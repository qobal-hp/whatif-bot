"""Write karma/ep08_full.json, Karma Tales EP08 "Replaced", from the user's 32-scene script.

usage: python karma/build_ep08.py
The first minute (the cold open through "Then ask him who I am") is cut fast and almost every shot moves (image-to-video);
after that the story runs on stills. The narrator voices the details the dialogue can't carry, and every line has
eleven_v3 delivery tags following the script's voice direction (Rachel gets quieter as she gets angrier; Ben is
charming right before he asks for something; Frank pauses when the truth would cost him; Megan's stage voice is
polished and her own voice is plain).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

VOICES = {
    "NARRATOR": "FmtiHEcHpocK7YiZwa46",
    "RACHEL": "RACHEL_VOICE", "BEN": "BEN_VOICE", "FRANK": "FRANK_VOICE", "MEGAN": "MEGAN_VOICE",
    "NINA": "NINA_VOICE", "MARA": "MARA_VOICE",
    "HOST": "Chris", "SERVER": "Jessica", "CAMERAMAN": "Roger", "LINDA": "Matilda", "LEO": "Liam", "CUSTOMER": "Alice",
}
CASTING = ROOT / "karma" / "voices_ep08.json"
if CASTING.exists():
    VOICES.update(json.loads(CASTING.read_text()))

CAST = {c: f"karma/cast/ep08/{c}.jpg" for c in ["rachel", "frank", "megan", "ben", "nina", "mara", "linda", "leo", "host", "cameraman"]}

PORTRAIT = ("Photorealistic still from a prestige American TV drama, shot on 35mm, shallow depth of field, soft warm cinematic key light, "
            "natural skin texture, head-and-shoulders portrait facing slightly off camera, neutral dark background, an entirely "
            "fictional person who resembles no real celebrity, no text, no watermark. ")
PORTRAITS = {
    "ben": "Ben, a 42-year-old American man, short neat dark-brown hair with a little gray at the temples, clean-shaven, an easy charming smile that doesn't reach his eyes, charcoal suit with an open white collar.",
    "nina": "Nina, a 46-year-old American woman, dark hair pulled back tight under a bandana, strong dry expression, small silver hoop earrings, black baker's T-shirt dusted with flour.",
    "mara": "Mara, a 54-year-old American businesswoman, short silver-blonde hair, reading glasses pushed up on her head, warm attentive eyes, navy blazer over a striped shirt.",
    "linda": "Aunt Linda, a 66-year-old American woman, soft white curls, rosy cheeks, big friendly smile, lavender cardigan and a brooch.",
    "leo": "Leo, a 22-year-old American baker, curly black hair under a backwards cap, thin mustache, earnest nervous eyes, white kitchen jacket.",
    "host": "The party host, a 50-year-old American man, bald, round glasses, a big professional grin, tan blazer and a bow tie.",
    "cameraman": "A 35-year-old American videographer, scruffy beard, gray beanie, black hoodie, a camera strap over his shoulder.",
}

LOOKS = {
    "rachel": "Rachel (the woman with a chestnut bob from the reference photo, same face, late 30s, in a dark teal baker's work jacket dusted with flour)",
    "rachel:home": "Rachel (the woman with a chestnut bob from the reference photo, same face, late 30s, in a soft gray sweater, hair loose, tired but calm)",
    "frank": "Frank (the silver-haired older man from the reference photo, same face, mid 60s, in a navy suit and a dark patterned tie)",
    "frank:shop": "Frank (the silver-haired older man from the reference photo, same face, mid 60s, in a tan cardigan over a collared shirt)",
    "megan": "Megan (the blonde woman with a braided bun from the reference photo, same face, early 30s, in a sleeveless burgundy satin dress)",
    "megan:coat": "Megan (the blonde woman with a braided bun from the reference photo, same face, early 30s, in a camel coat over a burgundy dress)",
    "ben": "Ben (the dark-haired man from the reference photo, same face, early 40s, in a charcoal suit with an open white collar)",
    "ben:shop": "Ben (the dark-haired man from the reference photo, same face, early 40s, in rolled-up shirtsleeves and a badly tied baker's apron, flour on his hands)",
    "nina": "Nina (the dark-haired woman in a bandana from the reference photo, same face, in a black baker's T-shirt and apron)",
    "mara": "Mara (the silver-blonde woman from the reference photo, same face, in a navy blazer)",
    "linda": "Aunt Linda (the white-haired older woman from the reference photo, same face, in a lavender cardigan)",
    "leo": "Leo (the young curly-haired baker from the reference photo, same face, in a white kitchen jacket)",
    "host": "the host (the bald man in round glasses from the reference photo, same face, in a tan blazer and bow tie)",
    "cameraman": "the videographer (the bearded man in a gray beanie from the reference photo, same face, in a black hoodie)",
}

PLACES = {
    "ballroom": "Setting: a hotel ballroom in a mid-sized American town during an evening retirement party, round tables with white cloths, gold string lights, a small stage with a microphone stand and a banner reading HAPPY RETIREMENT FRANK, a videographer's camera on a tripod, warm amber light.",
    "aisle": "Setting: the center aisle between round party tables in a hotel ballroom during a retirement party, guests in their good clothes turning in their chairs, gold string lights.",
    "stage": "Setting: a small ballroom stage at a retirement party, a microphone stand, a heavy dark-red curtain behind it, warm spotlights.",
    "backstage": "Setting: behind a heavy dark-red stage curtain in a hotel ballroom, cables on the floor, a stack of folding chairs, a strip of warm light through a gap in the curtain.",
    "corridor": "Setting: a narrow hotel service corridor behind a ballroom, steel service carts, fluorescent light, swinging kitchen doors with round windows.",
    "stairwell": "Setting: a concrete hotel stairwell with a narrow wired-glass window looking into a lit ballroom, cold fluorescent light.",
    "office": "Setting: a tiny cramped venue office, three folding chairs, a desk with event schedules, a calendar, one desk lamp, the door barely closing.",
    "catering": "Setting: a hotel catering hall, stainless counters, a walk-in fridge door, two white bakery boxes on rolling carts, bright work lights.",
    "av": "Setting: the audio-visual table at the back of a hotel ballroom, a laptop, a video monitor, a soundboard, cables, a camera on a tripod.",
    "window": "Setting: a tall window at the edge of a hotel ballroom, the dark parking lot outside, the party glowing behind.",
    "foyer": "Setting: a hotel foyer and coat check at night, a brass coat rack, glass front doors, cold night outside.",
    "apartment": "Setting: a small tidy apartment kitchen at night, a refrigerator, a little table, a phone on the counter, a single warm lamp.",
    "apartment_day": "Setting: the same small apartment kitchen in late afternoon sunlight, a wooden table with two chairs.",
    "bakery_dark": "Setting: the glass front door of a small family bakery at 4 A.M., street lamps, dark street, lights just coming on inside.",
    "bakery_kitchen": "Setting: the back kitchen of a small family bakery before dawn, steel worktables, deck ovens, sheet pans, flour on everything, a schedule taped to the wall.",
    "bakery_front": "Setting: the front counter of a small warm family bakery in the morning, bread racks, a glass pastry case, chalkboard menu, little café tables by the window.",
    "bakery_desk": "Setting: a cluttered little desk in the back of a family bakery, old payroll binders, a corded phone, a framed photo of the bakery's opening day.",
    "video": "Setting: a video playing on a small monitor, footage of a cozy family bakery counter.",
}

N = "NARRATOR"
S = []


def sc(place, chars, image, lines, **extra):
    S.append((place, chars, image, lines, extra))


# ── 01 DAD, WHO IS SHE? (cold open, every shot moves) ───────────────────────────────────────────────
sc("stage", ["megan"], "Close-up of Megan at a live microphone on the small stage, smiling fondly, spotlight on her.",
   [("MEGAN", "[fond, polished, as if she's told it a hundred times] I dropped Dad's birthday cake when I was twelve. [pause] He stuck the candles in the part that landed right side up.")],
   sfx=[["Live microphone hum in a quiet ballroom", 2.0, 0.3, "start"]], motion="she leans into the microphone, smiling, the spotlight glinting on her earrings")
sc("ballroom", [], "Wide shot of the ballroom: a hundred guests at round tables laughing toward the stage.",
   [(N, "[low, intimate] The room laughed.")],
   sfx=[["A large party crowd laughing warmly", 2.5, 0.5, "start"]], motion="guests laugh and lean back in their chairs, glasses raised")
sc("aisle", ["rachel"], "At the back of the ballroom, Rachel frozen in the aisle, a white cake box tied with string pressed against her flour-dusted work jacket.",
   [(N, "[quiet] At the back of the room, a woman in a flour-dusted work jacket stopped walking. [pause] She was holding the birthday cake.")],
   motion="Rachel stops dead, the cake box pressed against her chest, the laughter rolling past her", music="tension")
sc("stage", ["host"], "The host stepping up beside the stage with his arm out, grinning.",
   [("HOST", "[big, warm, showman] Frank's daughter, Rachel, everybody!")],
   sfx=[["Applause in a ballroom", 2.5, 0.5, "end"]], motion="the host sweeps his arm toward the woman at the microphone as applause starts")
sc("stage", ["frank", "megan"], "Frank hugging Megan on stage; over her shoulder his eyes have found someone at the back of the room.",
   [(N, "[slow] Frank hugged her. [pause] Over her shoulder, he saw his real daughter. [pause] His hand stayed on the stranger's back.")],
   motion="Frank pulls Megan into a hug, then his eyes lift over her shoulder and lock on someone; his hand stays on her back")
sc("aisle", ["rachel"], "Close-up of Rachel's face, very still, eyes on the stage.",
   [("RACHEL", "[just loud enough, very still] Dad. [pause] Who is she?")],
   sfx=[["Applause dying out unevenly", 1.5, 0.3, "start"]], motion="the applause dies around her; she doesn't blink")

# ── 02 SHE'S WITH THE BAKERY ───────────────────────────────────────────────────────────────────────
sc("aisle", ["ben"], "Ben cutting across the aisle with a drink in his hand, smile switched on, waving at a server.",
   [("BEN", "[bright, smiling too wide, to a server] Perfect! The cake's here. [pause] Could you show her to the kitchen?")],
   motion="Ben strides down the aisle with a drink, smile switching on")
sc("aisle", ["rachel", "ben"], "Rachel and Ben face to face in the aisle, guests watching from the tables.",
   [("RACHEL", "[flat, quiet] It's me, Ben."),
    ("BEN", "[holding the smile, through his teeth] She's with the bakery."),
    ("RACHEL", "[quieter] I run the bakery.")],
   motion="Ben keeps smiling at the guests while Rachel stares at him")
sc("aisle", [], "A young server in a black vest taking one step back; a woman at a nearby table turning her chair to watch.",
   [(N, "[dry] The server took one step back. [pause] A woman near the aisle turned her chair around.")],
   motion="the server backs away; a guest swivels her chair to watch")
sc("aisle", ["ben"], "Ben leaning in close to Rachel, voice dropped, eyes on the guests.",
   [("BEN", "[under his breath, charming] Can we do this outside?"),
    ("RACHEL", "[low] Where did she hear that story?"),
    ("BEN", "[a light shrug] It's a party. People tell stories.")],
   motion="Ben leans in close, still smiling for the room")
sc("aisle", ["rachel"], "Close-up of Rachel, jaw tight, holding the cake box.",
   [("RACHEL", "[quiet, precise] Dad tells everybody the cake landed on the table. [pause] It landed on the floor. [pause] I told you the real version on Sunday.")],
   motion="her grip tightens on the cake box")
sc("aisle", ["ben", "rachel"], "Ben reaching for the cake box; Rachel pulling it back against her chest.",
   [("BEN", "[a tight smile] You're standing in the middle of the aisle."),
    ("RACHEL", "Then let me through.")],
   motion="Ben reaches for the box and Rachel pulls it back against her chest")
sc("aisle", ["ben"], "Close-up of Ben, smile gone soft, almost pleading.",
   [("BEN", "[soft, as if asking a favor] Dad gets one night."),
    ("RACHEL", "[very quiet] Then ask him who I am.")],
   motion="Ben's smile fades into something softer and more dangerous")

# ── 03 GO AHEAD, SWEETHEART ────────────────────────────────────────────────────────────────────────
sc("stage", ["megan"], "Megan on stage lowering the microphone, uncertain, looking toward the aisle.",
   [("MEGAN", "[polish cracking, one note of uncertainty] Do we... need to stop?")],
   music="tension", cut=True)
sc("stage", ["frank"], "Frank taking the microphone from Megan, looking down the room toward his daughter.",
   [(N, "[slow] Frank took the microphone. [pause] He looked straight down the aisle at Rachel. [pause] She shifted the cake box onto one arm, ready to lift her hand when he said her name.")])
sc("stage", ["frank", "megan"], "Frank handing the microphone back to Megan with a gentle smile.",
   [("FRANK", "[gently, warm public voice, to Megan] Go ahead, sweetheart.")],
   sfx=[["A single person clapping once, then stopping", 1.5, 0.4, "end"]])
sc("aisle", ["rachel"], "Rachel in the aisle with her hand half raised, slowly lowering it.",
   [(N, "[very quiet] Somebody clapped once. [pause] Then stopped.")])
sc("stage", ["megan"], "Megan setting the microphone down on the stand, pale.",
   [("MEGAN", "[small] Could I get a glass of water?")])
sc("stage", ["host", "ben"], "The host catching Ben by the sleeve at the edge of the stage, grinning through clenched teeth.",
   [("HOST", "[through his smile] What do you want me to do up here?"),
    ("BEN", "[breezy] Tell them there's cake."),
    ("HOST", "[deadpan] Is there cake?")])
sc("stage", ["ben"], "Ben looking at an empty rolling cart beside the stage.",
   [(N, "[dry] Ben looked at the empty cart beside the stage.")])

# ── 04 ONE MORE THING TO FILM ──────────────────────────────────────────────────────────────────────
sc("backstage", ["megan", "rachel"], "Behind the curtain, Megan pulling a folded page out of her dress pocket while Rachel watches.",
   [("MEGAN", "[quick, keeping her voice down] They told me it was a reenactment. I asked if you were coming. [pause] He said you'd be watching at home."),
    ("RACHEL", "[low] What else did they give you?")])
sc("backstage", ["megan"], "Megan holding out the folded page.",
   [("MEGAN", "This goes after the cake. [pause] He told me to look straight into the camera.")])
sc("backstage", [], "Close-up of a printed page: the words FINAL TAKE at the top, one sentence highlighted in yellow underneath.",
   [("RACHEL", "[reading slowly, each word heavier] \"Starting tomorrow... Ben will run the bakery. [pause] This was my decision.\"")],
   overlay={"type": "letter", "text": "FINAL TAKE — \"Starting tomorrow, Ben will run the bakery. This was my decision.\""})
sc("backstage", ["megan", "rachel"], "Megan studying Rachel's face; Rachel staring at the page.",
   [("MEGAN", "[careful] Are you stepping down?"),
    ("RACHEL", "[a dry, exhausted breath] I opened the bakery at four this morning. [pause] He texted me to ask where we keep the keys.")])
sc("backstage", [], "Through a gap in the red curtain: the videographer's camera on its tripod turning toward an empty spot beside Frank on stage.",
   [("BEN~phone", "[over the speakers, cheerful] Can we get Rachel back up here? We've got one more thing to film!")],
   sfx=[["Microphone feedback squeal, short", 1.0, 0.3, "start"]])
sc("backstage", ["megan", "rachel"], "Both women turning toward the stage at the same moment, faces lit through the curtain gap.",
   [(N, "[a beat, then low] Both women looked toward the stage."),
    (N, "[slow, heavy] Karma Tales. [pause] Replaced.")],
   sfx=[["Deep dramatic musical sting", 2.5, 0.5, "end"]], overlay={"type": "text", "text": "REPLACED."})

# ── 05 THEY ALREADY SHOT IT ────────────────────────────────────────────────────────────────────────
sc("corridor", ["rachel"], "Rachel setting the cake box down on a steel service cart in the corridor.",
   [(N, "[matter-of-fact] Rachel set the cake down on a service cart. [pause] Then she walked straight to the camera.")], music="wonder", cut=True)
sc("corridor", ["rachel", "cameraman"], "Rachel standing squarely in front of the videographer's lens, controlled.",
   [("RACHEL", "[controlled, quiet] That page she was about to read? I've never said any of it. [pause] Please stop filming.")])
sc("corridor", ["cameraman"], "The videographer lowering his camera, confused.",
   [("CAMERAMAN", "[uneasy, helpful] Do you want us to skip the speech and just use the shop footage?"),
    ("RACHEL", "[a beat] What shop footage?")])
sc("video", ["megan"], "On a small video monitor: Megan behind a bakery counter tying a flour-stained apron, smiling for the camera.",
   [("MEGAN~phone", "[bright, rehearsed] My dad opened this place before I was born. Pretty much everything I know... I learned right here.")])
sc("video", [], "Close-up on the monitor: the flour stain on the apron pocket.",
   [(N, "[quiet] Rachel knew that apron. [pause] She knew the flour stain on the pocket. [pause] It was hers.")])
sc("corridor", ["rachel", "cameraman"], "Rachel staring at the monitor; the videographer beside her.",
   [("RACHEL", "[barely moving] When was that?"),
    ("CAMERAMAN", "Tuesday. A little after six.")])
sc("bakery_front", [], "Memory: the small family bakery at dusk, the CLOSED sign being flipped on the glass door.",
   [(N, "[low] On Tuesday, Ben had offered to close for her. [pause] It was the first time he'd offered in three years.")])
sc("corridor", ["rachel"], "Rachel leaning toward the monitor.",
   [("RACHEL", "[steady] Can you play what happens next?")])
sc("video", ["megan"], "On the monitor: Megan turning toward someone off camera, unsure.",
   [("MEGAN~phone", "[normal voice, unsure] Was that better?"),
    ("BEN~phone", "[off-camera, casual] Yeah. Next time, stay behind the counter. [pause] I don't want anyone outside getting a good look at you.")])
sc("corridor", ["cameraman"], "The videographer stopping the clip himself, embarrassed.",
   [("CAMERAMAN", "[embarrassed] He told me she worked there."),
    ("RACHEL", "[not unkind] You took direction from him. I get it. [pause] Who has the footage?"),
    ("CAMERAMAN", "I sent him the previews this morning. [pause] The originals are with me.")])

# ── 06 THE APRON ───────────────────────────────────────────────────────────────────────────────────
sc("stairwell", ["rachel"], "Rachel in the concrete stairwell, phone to her ear.",
   [("NINA~phone", "[machinery behind her, dry] If this is about the lemon filling, I put it on the bottom shelf.")],
   sfx=[["Industrial mixer and kitchen machinery over a phone line", 2.0, 0.3, "start"]])
sc("stairwell", ["rachel"], "Close-up of Rachel, one hand on the stair rail.",
   [("RACHEL", "[low] Tuesday night. Did you see anybody behind my counter?")])
sc("bakery_kitchen", ["nina"], "Nina in the bakery kitchen with the phone wedged against her shoulder, flour on her arms.",
   [("NINA~phone", "[dry] Ben sent me home early. Said he was taking pictures of the ovens for insurance. [pause] Why?"),
    ("RACHEL", "[very quiet] Did he ask you to leave my apron out?")])
sc("bakery_kitchen", ["nina"], "Nina stopping, wiping her hands on a towel.",
   [("NINA~phone", "[dry, a little amused] He asked which one you wear on camera. [pause] I told him you wear the same one until I physically take it off you.")])
sc("stairwell", ["rachel"], "Rachel pressing her knuckles to her mouth, almost laughing, eyes wet.",
   [(N, "[quiet] Rachel almost laughed. [pause] Nina heard her breathing change."),
    ("NINA~phone", "[softening] Rachel. [pause] What happened?")])
sc("stairwell", ["rachel"], "Rachel looking down the stairwell.",
   [("RACHEL", "[steady] Have you seen tomorrow's schedule?"),
    ("NINA~phone", "[flat] Got a new one an hour ago. Same start time. [pause] Different name at the top."),
    ("RACHEL", "Who does it say to call if something goes wrong?"),
    ("NINA~phone", "[dry] Ben. [pause] I called him twice about the delivery. He hasn't picked up.")])
sc("stairwell", ["ben"], "Through the wired-glass stairwell window: Ben in the ballroom showing a guest his phone; the screen lights up with an incoming call and he flips it face down.",
   [(N, "[slow] Through the stairwell window, Rachel watched Ben show a guest something on his phone. [pause] A call lit up the screen. [pause] He turned it face down.")])
sc("stairwell", ["rachel"], "Close-up of Rachel, eyes hard.",
   [("RACHEL", "[quiet, decided] Keep that schedule. [pause] And send me a picture before he changes it.")])

# ── 07 SAY IT LIKE HER ─────────────────────────────────────────────────────────────────────────────
sc("corridor", ["megan:coat"], "Megan standing beside the cake cart with her coat over one arm, ready to leave.",
   [("MEGAN", "[awkward, plain voice] I was going to leave your page with the cake."),
    ("RACHEL", "[tired] It's his page. You can keep it.")])
sc("corridor", ["megan:coat", "rachel"], "Megan turning to go; Rachel stopping her with a question.",
   [("RACHEL", "[a sudden thought, quiet] Who told you how I wear the towel?")])
sc("corridor", ["megan:coat"], "Megan pausing, embarrassed.",
   [("MEGAN", "[honest] Ben showed me a video. You were making something with your dad. [pause] You kept wiping your hands every time he asked you a question."),
    ("RACHEL", "[a faint, sad smile] He was trying to get me to look up for the camera.")])
sc("corridor", ["megan:coat"], "Megan miming a little downward glance and smile.",
   [("MEGAN", "Ben wanted me to copy that thing you do before you answer. [pause] Where you look down and... kind of smile to yourself.")])
sc("corridor", ["rachel"], "Rachel looking down with a tiny private smile, then catching herself.",
   [(N, "[soft] Rachel looked down. [pause] She caught herself."),
    ("MEGAN", "[gently] That. [pause] Sorry.")])
sc("corridor", ["rachel"], "Close-up of Rachel, eyes glistening.",
   [("RACHEL", "[quiet, it costs her] I made that video for Dad. [pause] He was supposed to watch it after the party.")])
sc("corridor", ["megan:coat"], "Megan glancing toward the ballroom doors as the host's voice calls the family up.",
   [("HOST~phone", "[distant, over the speakers] Could we get Frank and the family up here for a photo?"),
    ("MEGAN", "[a breath] I can tell the camera guy what they hired me for."),
    ("RACHEL", "[looking at the closed doors] Would you tell the people in there?")])
sc("corridor", ["megan"], "Megan sliding her coat off her arm and laying it over the cart handle.",
   [(N, "[slow] Megan looked toward the ballroom. [pause] Then she slid her coat off her arm."),
    ("MEGAN", "[plain, steady] If you're in there with me.")])

# ── 08 HE SAID YOU ASKED ───────────────────────────────────────────────────────────────────────────
sc("corridor", ["mara"], "Mara stepping into the corridor with two glasses of water, handing one over.",
   [("MARA", "[friendly, getting right to it] I thought I saw you come in. [pause] Can we talk about tomorrow?"),
    ("RACHEL", "[careful] If Ben told you the tasting's canceled... it isn't.")], music="tension", cut=True)
sc("corridor", ["mara", "rachel"], "Mara and Rachel close together in the corridor.",
   [("MARA", "[exact] He told me it was going ahead. [pause] He said you asked him to take over."),
    ("RACHEL", "[very quiet] When?"),
    ("MARA", "Monday. I asked to speak to you. [pause] He said you were too upset. [pause] So I called your dad.")])
sc("ballroom", ["frank", "ben"], "Through the glass of the ballroom door: Frank making room for Ben in the family photo, an empty spot on his other side.",
   [(N, "[slow] Through the glass, Frank made room for Ben in the family photo. [pause] On his other side, there was an empty spot.")])
sc("corridor", ["rachel"], "Close-up of Rachel, holding very still.",
   [("RACHEL", "[almost no voice] What did Dad say?"),
    ("MARA", "[gently] \"Give Ben a chance.\" [pause] I thought he meant a chance to run the meeting. [pause] Then I got this.")])
sc("corridor", [], "Close-up of Mara's phone: an email from Frank with a speech attached.",
   [("RACHEL", "[quiet] Can you forward it?")],
   overlay={"type": "message", "from": "Frank", "to": "Mara", "text": "Subject: Tomorrow's handover. Speech attached."})
sc("corridor", ["rachel"], "Rachel reading her phone, the glow on her face.",
   [(N, "[low] Her phone buzzed a moment later. [pause] On Frank's copy, there was a note at the bottom. [pause] It wasn't on Megan's.")])
sc("corridor", [], "Close-up of a phone screen with a typed note at the bottom of a speech.",
   [("RACHEL", "[almost too quiet to hear] \"Do this after the cake. [pause] She'll have gone home by then.\"")],
   overlay={"type": "letter", "text": "\"Do this after the cake. She'll have gone home by then.\""}, sfx=[["Low ominous tone", 2.5, 0.35, "start"]])
sc("corridor", ["megan", "rachel"], "Rachel lifting the cake box off the cart; Megan beside her.",
   [("MEGAN", "[uncertain] Where are we going?"),
    ("RACHEL", "[steady, quiet] I want to hear my dad say it.")])

# ── 09 MOVE IN A LITTLE ────────────────────────────────────────────────────────────────────────────
sc("stage", ["linda"], "Aunt Linda beaming from the front row, patting an empty chair.",
   [(N, "[light] The photographer was calling for everyone to move in a little."),
    ("LINDA", "[fond, oblivious] There she is! I saved you a chair.")], music="wonder", cut=True)
sc("stage", ["frank", "rachel"], "Rachel setting the cake box on the edge of the stage; Frank's eyes on the box.",
   [("FRANK", "[warm public voice] You made the one with lemon."),
    ("RACHEL", "[flat] You asked me to.")])
sc("stage", ["rachel"], "The photographer's camera raised; Rachel looking only at her father.",
   [("RACHEL", "[quiet, direct] Did you email Mara on Monday?"),
    ("FRANK", "[light, deflecting] Honey, she's here as a guest."),
    ("RACHEL", "[quieter] She was a guest when you told her I quit?")])
sc("stage", ["ben"], "Ben sliding between his father and the center of the room, hand up to the photographer.",
   [("BEN", "[smooth, to the photographer] Can you give us one minute? [pause] Dad needs to sit down.")])
sc("stage", ["frank"], "Frank standing still, not sitting.",
   [(N, "[dry] The photographer lowered the camera. [pause] Frank made no move to sit.")])
sc("stage", ["linda"], "Aunt Linda's smile falling.",
   [("LINDA", "[confused, hurt] Why would you tell somebody Rachel quit?"),
    ("BEN", "[smooth] She hasn't quit. We're changing a few things. Dad wanted to tell you himself."),
    ("RACHEL", "[a thin smile] I'd love that.")])
sc("stage", ["frank"], "Frank glancing at the camera, which now points at the floor.",
   [("FRANK", "[low, his small private voice] Come out here with me.")])
sc("stage", ["frank"], "Close-up of Frank avoiding his daughter's eyes.",
   [(N, "[intimate, slow] Rachel had watched her father tell customers they'd lost an order. Lost a deposit. Lost the power on Christmas Eve. [pause] He always looked them in the eye. [pause] He still hadn't looked at her... since he'd put his arm around that woman.")])

# ── 10 THE LITTLE ROOM ─────────────────────────────────────────────────────────────────────────────
sc("office", ["frank", "rachel"], "The tiny venue office: Frank leaving the door open an inch, Rachel pushing it shut behind them.",
   [(N, "[quiet] The office was barely big enough for three chairs. [pause] Frank left the door open an inch. [pause] Rachel closed it.")],
   sfx=[["A door clicking shut in a small room", 1.0, 0.4, "end"]], cut=True)
sc("office", ["frank"], "Frank sitting heavily, weary.",
   [("FRANK", "[weary, trying for tender] Your brother came to me in September. [pause] He said he wanted to come home."),
    ("RACHEL", "[even] I offered him the Tuesday close.")])
sc("office", ["frank", "rachel"], "Father and daughter facing each other across the small desk.",
   [("FRANK", "That's one shift."),
    ("RACHEL", "[quiet] He took it once. [pause] You just saw what he did with it."),
    ("FRANK", "[a small shrug] He's good with people. You've always known that.")])
sc("office", ["rachel"], "Close-up of Rachel.",
   [("RACHEL", "[controlled] The woman he hired thought she was here to tell a funny story about me."),
    ("FRANK", "[defensive] I was told she knew what the whole thing was for."),
    ("RACHEL", "[quieter] What did you think the whole thing was for?")])
sc("office", ["frank"], "Frank rubbing the pale strip on his wrist where his watch usually sits.",
   [("FRANK", "[slow, half to himself] I wanted people to keep coming in Monday morning. Same bread. Same girls behind the counter. [pause] They hear I'm retiring and they start to worry. [pause] I wanted them to see we'd figured it out. [pause] As a family.")])
sc("office", ["rachel"], "Rachel waiting, arms folded.",
   [("RACHEL", "[very quiet] Which part did we figure out together?")])
sc("office", ["frank"], "Frank looking at the door instead of his daughter.",
   [("FRANK", "[a pause that costs him, then] You could have asked me for the business years ago."),
    ("RACHEL", "[quietly] I did. [pause] You said we'd talk when you retired.")])
sc("office", ["rachel"], "Close-up of Rachel, a silence hanging.",
   [(N, "[a long silence, then softly] Silence."),
    ("RACHEL", "[almost gentle] We're at your retirement party, Dad.")], sfx=[["Faint muffled party music through a wall", 2.5, 0.2, "start"]])

# ── 11 WHAT DID YOU PROMISE THEM? ──────────────────────────────────────────────────────────────────
sc("office", ["ben"], "Ben letting himself into the office, all business.",
   [("BEN", "[brisk, charming] Mara's still here. [pause] We need to give her one story."),
    ("RACHEL", "[flat] Give her the real one.")], music="tension", cut=True)
sc("office", ["ben"], "Ben leaning on the desk.",
   [("BEN", "[easy] The real one is she wants a bigger order than you wanted to take. [pause] I said yes."),
    ("RACHEL", "[precise] She wanted to run a tasting. We hadn't agreed to the order.")])
sc("office", ["ben", "rachel"], "Ben and Rachel facing off in the cramped room.",
   [("BEN", "[a flash of irritation] That's because every time she asked what we could do, you told her what could go wrong."),
    ("RACHEL", "[quiet] I told her we had one oven that could hold temperature.")])
sc("office", ["frank"], "Frank looking up, surprised.",
   [("FRANK", "[to Ben, confused] I thought the second one was fixed."),
    ("RACHEL", "[tired] It was quoted. [pause] I sent you the quote twice.")])
sc("office", ["ben"], "Ben spreading his hands with a laugh.",
   [("BEN", "[a short laugh, charming again] Listen to us. We're at Dad's party arguing over an oven. [pause] This is exactly why I said I'd handle the business side."),
    ("RACHEL", "[very quiet] How many stores did you promise?")])
sc("office", ["ben"], "Close-up of Ben taking a drink, then setting the glass down deliberately.",
   [(N, "[slow] Ben took a drink. [pause] He set the glass down very carefully."),
    ("BEN", "[flat] Six.")], sfx=[["A glass set down on a wooden desk", 1.0, 0.4, "start"]])
sc("office", ["frank"], "Frank turning to look at his son for the first time.",
   [("FRANK", "[stunned, small] You said two."),
    ("BEN", "[a shrug] Two was last week. She got excited.")])
sc("office", ["rachel"], "Rachel, arms crossed, eyes narrowed.",
   [("RACHEL", "[quiet, exact] She saw samples for two stores. [pause] Did you tell her who'd be making the six-store order?"),
    ("BEN", "[as if it's obvious] I told her we had a team.")])

# ── 12 EVERY MORNING SOMEBODY DID ──────────────────────────────────────────────────────────────────
sc("office", [], "Close-up of Rachel's phone on the desk: a photo of a new staff schedule and six handwritten sample labels laid out in a row.",
   [(N, "[low] Rachel's phone lit up. Nina had sent the new schedule. [pause] And a photo of six labels, laid out in a row.")],
   overlay={"type": "message", "from": "Nina", "to": "Rachel", "text": "New schedule + the labels he left out. 6 of them."})
sc("office", ["rachel", "ben"], "Rachel sliding the phone between her father and brother.",
   [("RACHEL", "[quiet] Is there supposed to be a tray for each of those?"),
    ("BEN", "[breezy] It photographs better.")])
sc("office", ["rachel"], "Close-up of Rachel.",
   [("RACHEL", "[very even] On which day were you going to tell us to make six trays?")])
sc("office", ["ben"], "Ben waving a hand.",
   [("BEN", "[impatient] They don't have to be the exact same thing we'd ship. [pause] Let somebody make it look good for the meeting."),
    ("RACHEL", "[flat] You invited a buyer to a tasting. [pause] She'll taste it.")])
sc("office", ["frank", "ben"], "Frank turning to Ben, uneasy.",
   [("FRANK", "[uneasy] Ben, just tell her we need more time."),
    ("BEN", "[sharp] You tell her. You're the one she trusts.")])
sc("office", ["frank"], "Frank's hand moving toward his jacket pocket, then stopping.",
   [(N, "[quiet] Frank's hand moved toward his jacket pocket. [pause] Then it stopped.")])
sc("office", ["ben"], "Ben leaning close to Rachel, voice dropping, persuasive.",
   [("BEN", "[dropping his voice, generous] You can still come in tomorrow. [pause] If that's what you're worried about."),
    ("RACHEL", "What time?"),
    ("BEN", "[easy] Your regular time."),
    ("RACHEL", "[quiet] Which is?")])
sc("office", ["frank", "ben"], "Ben looking at Frank; Frank looking down at the schedule on the phone.",
   [(N, "[slow] Ben looked at Frank. [pause] Frank looked down at the schedule."),
    ("RACHEL", "[waits, then, softly] Right.")])
sc("bakery_dark", [], "Memory: the family bakery before dawn, one light on in the back, a coffee mug steaming on the counter.",
   [(N, "[intimate, slow] Every morning Frank arrived, there was coffee in his mug and bread on the rack. [pause] Sometimes he'd tell a customer he still opened the place himself. [pause] Rachel used to think it was a joke."),
    (N, "[quiet] Standing between the two men, she realized... neither of them knew when the first person came through the door.")])

# ── 13 THE DRESS REHEARSAL ─────────────────────────────────────────────────────────────────────────
sc("backstage", ["rachel"], "Rachel slipping out into the backstage area, stopping at the curtain because she hears her father's voice.",
   [(N, "[low] The host needed Ben for his next cue. Rachel slipped out. [pause] From behind the curtain, she heard her father talking to Megan.")], cut=True)
sc("backstage", ["frank", "megan"], "Frank and Megan behind the curtain, Frank pointing at the page in her hand.",
   [("FRANK", "[careful, almost kind] At the end, say, \"I decided.\""),
    ("MEGAN", "[plain] My page says, \"This was my decision.\"")])
sc("backstage", ["frank"], "Close-up of Frank, a little impatient.",
   [("FRANK", "[soft] Yes. Either way. [pause] Ben's copy says, \"We decided.\" I don't want that in there."),
    ("MEGAN", "[quiet, pointed] What if she never decided?")])
sc("backstage", ["rachel"], "Rachel standing behind the curtain, the red fabric almost brushing her face.",
   [(N, "[very quiet] Silence. [pause] Rachel stood so close to the curtain the fabric almost brushed her face.")])
sc("backstage", ["frank", "megan"], "Frank sighing at Megan.",
   [("FRANK", "[tired] I'm asking you to get us through the evening."),
    ("MEGAN", "[steady] I think you should ask her.")])
sc("backstage", ["frank"], "Frank's irritation showing.",
   [("FRANK", "[irritation breaking through] I know how that conversation would go. [pause] I've been her father for thirty-eight years.")])
sc("backstage", ["rachel"], "Rachel pulling the curtain aside.",
   [("RACHEL", "[quiet, cold] Then you know exactly what you're doing.")],
   sfx=[["A heavy curtain pulled aside", 1.0, 0.4, "start"]])
sc("backstage", ["frank"], "Frank folding the page in half, holding it halfway between himself and his daughter.",
   [("FRANK", "[small] I wanted to spare you a scene."),
    ("RACHEL", "[quiet] On Monday, you could've called me before you wrote that down.")])
sc("backstage", ["frank", "rachel"], "Father and daughter face to face behind the curtain.",
   [("FRANK", "[a pause that costs him] On Monday I thought I still had time."),
    ("RACHEL", "[barely audible] You had my number.")])

# ── 14 WHEN WERE YOU GOING TO TELL ME? ─────────────────────────────────────────────────────────────
sc("backstage", ["frank"], "Frank opening his mouth, closing it again.",
   [(N, "[soft] Megan stepped away to give them space. [pause] Frank opened his mouth twice before he spoke."),
    ("FRANK", "[small] I was going to tell you after breakfast tomorrow.")], music="wonder", cut=True)
sc("backstage", ["rachel"], "Close-up of Rachel.",
   [("RACHEL", "[quiet] Who was making breakfast tomorrow?"),
    ("FRANK", "I mean at the shop. After the first rush.")])
sc("backstage", ["rachel"], "Rachel counting it off, voice low and even.",
   [("RACHEL", "[low, even, every item landing] After I open. After I make the samples. [pause] After I stand there while Ben meets with Mara.")])
sc("backstage", ["frank"], "Frank trying for gentle.",
   [("FRANK", "[gentle, wheedling] I thought you'd be relieved. You've said a hundred times you're exhausted."),
    ("RACHEL", "[quiet] I asked you for Sundays off.")])
sc("backstage", ["frank"], "Frank sitting down on a creaky folding chair in the wings.",
   [(N, "[quiet] Frank sat on a folding chair in the wings. It creaked under him."),
    ("FRANK", "[tired] He told me he could make it easier for you.")], sfx=[["A metal folding chair creaking", 1.0, 0.4, "start"]])
sc("backstage", ["rachel"], "Rachel standing over him.",
   [("RACHEL", "Did he tell you which part he was taking off my plate?"),
    ("FRANK", "[weak] I thought he'd deal with the things you don't like.")])
sc("backstage", ["rachel"], "Close-up of Rachel, eyes wet, voice very low.",
   [("RACHEL", "[very low] When you asked the actress to say I was leaving... who was supposed to show up at four the next morning?")])
sc("backstage", ["frank"], "Frank with no answer, staring at his hands.",
   [(N, "[slow] Frank had no answer. [pause] Rachel started to walk away."),
    ("FRANK", "[soft, almost proud] You were very good at it, honey.")])
sc("backstage", ["rachel"], "Rachel stopping with her back to him.",
   [(N, "[quiet] She stopped."),
    ("RACHEL", "[quiet, without turning] Dad. [pause] I know.")])

# ── 15 THE ORIGINAL RECORDING ──────────────────────────────────────────────────────────────────────
sc("catering", ["rachel"], "In the catering hallway, Rachel holding her phone, one finger in her other ear, a home video playing on the screen.",
   [(N, "[low] In the catering hall, Rachel plugged one ear and played the video she'd made for her father.")],
   sfx=[["Phone speaker playing laughter in a kitchen", 2.0, 0.3, "start"]], cut=True)
sc("video", ["rachel", "frank:shop"], "Phone video: Rachel and Frank in the bakery kitchen, laughing, flour on the counter.",
   [("RACHEL~phone", "[casual, smiling through the words] Anyway, I know you tell everybody the cake landed on the table. [pause] It hit the floor. I saw you blow the dust off before you stuck the candles in."),
    ("FRANK~phone", "[laughing] Nobody ate that part!"),
    ("RACHEL~phone", "[laughing] You ate that part. You said I should've put more butter in it.")])
sc("catering", ["megan", "rachel"], "Megan coming close enough to hear; Rachel keeping the video playing.",
   [("RACHEL~phone", "[warmer, softer] I think that was the first time I knew I wanted to work with you. [pause] You made me finish something before I got to be mad about how it turned out. [pause] I don't think I've ever told you that.")])
sc("catering", ["rachel"], "Rachel stopping the recording, the screen going dark in her hand.",
   [(N, "[quiet] Rachel stopped the recording."),
    ("MEGAN", "[soft] They cut it right before that.")])
sc("catering", ["megan"], "Megan nodding, ashamed.",
   [("RACHEL", "[quiet] In the clip Ben gave you?"),
    ("MEGAN", "[plain] I asked if there was more. [pause] He said they only wanted the funny part.")])
sc("catering", ["rachel"], "Rachel holding the blank phone against her palm.",
   [("RACHEL", "[very quiet] I sent it to him so he could put it on a screen... for Dad.")])

# ── 16 USE THE SHOP VERSION ────────────────────────────────────────────────────────────────────────
sc("av", ["megan", "cameraman"], "At the AV table, Megan facing the videographer, Rachel just behind her.",
   [("MEGAN", "[businesslike, a slight tremor underneath] I'm taking myself out of the handover piece. [pause] You can tell Ben I said that directly."),
    ("CAMERAMAN", "[relieved] I can stop making it. [pause] He has a preview on his phone.")], music="tension", cut=True)
sc("av", ["ben"], "Ben arriving at the AV table, too cheerful.",
   [("BEN", "[arriving, too cheerful] A preview we paid for. [pause] Can I borrow her for a second?"),
    ("MEGAN", "[flat] I'm here.")])
sc("av", ["ben", "megan"], "Ben and Megan face to face, Ben smiling.",
   [("BEN", "[charming, persuasive] Then take a breath. All we need is one line. [pause] You can read it from the sheet."),
    ("MEGAN", "[level] You want me to tell people she chose to leave.")])
sc("av", ["ben"], "Close-up of Ben's smile going thin.",
   [("BEN", "[smile going thin] You're an actor. Last I checked, that's the job."),
    ("MEGAN", "[level, quiet] What job did you give the people watching?")])
sc("av", ["cameraman"], "The videographer moving his hand away from the controls.",
   [(N, "[dry] The camera operator moved his hand away from the controls.")])
sc("av", ["ben"], "Ben turning to the videographer, decisive.",
   [("BEN", "[brisk] Forget the speech. Play the shop version. [pause] Dad can explain the rest."),
    ("CAMERAMAN", "[disbelieving] You want me to put that up while she's standing here?"),
    ("BEN", "[cheerful] Yes. Then everybody gets cake and goes home.")])
sc("av", ["rachel"], "Rachel placing her hand flat on the edge of the AV table.",
   [("RACHEL", "[quiet, immovable] If it goes up... I'm staying in the room.")])
sc("av", ["ben"], "Ben studying his sister, deciding how hard to push.",
   [(N, "[slow] Ben watched her for a moment. [pause] Deciding how hard to push.")])

# ── 17 TELL HER SHE HAS A JOB ──────────────────────────────────────────────────────────────────────
sc("window", ["rachel"], "Rachel answering her phone by the window.",
   [("NINA~phone", "[quiet, under the hiss of a kitchen vent] Is the shop closing?"),
    ("RACHEL", "[alarmed, low] No. Who told you that?")], cut=True)
sc("bakery_kitchen", ["nina"], "Nina in the bakery kitchen at night, phone to her ear, Leo hovering behind her.",
   [("NINA~phone", "[worried, dry] Leo asked if he should take his knives home. He heard Ben was bringing in a new crew for wholesale. [pause] I told him I'd ask you.")])
sc("ballroom", ["ben", "frank"], "Across the ballroom, Ben showing Frank something on his phone.",
   [(N, "[quiet] Across the room, Ben was showing Frank the preview on his phone."),
    ("RACHEL", "[gently] Is Leo there now?")])
sc("bakery_kitchen", ["leo"], "Leo holding the phone, embarrassed, knife roll under his arm.",
   [("LEO~phone", "[embarrassed to be asking] Sorry. I know you're at a party."),
    ("RACHEL", "[gentle] Tell me what you heard.")])
sc("bakery_kitchen", ["leo"], "Close-up of Leo, anxious.",
   [("LEO~phone", "[anxious, fast] I overheard Ben on the phone. He said if everybody can't do three in the morning, he has people who will. [pause] I can't do three. I can get a ride at four. My brother starts at five.")])
sc("window", ["rachel"], "Rachel at the window, eyes closed for one beat.",
   [("RACHEL", "[quiet] Who's told you your shift changed?"),
    ("LEO~phone", "[small] Nobody. [pause] I just thought somebody would tell me before they told everybody else.")])
sc("window", ["rachel"], "Close-up of Rachel opening her eyes, steady.",
   [("RACHEL", "[steady, warm] You're on at four. That's what the schedule Nina sent me says. [pause] Go by the one you have until somebody actually talks to you."),
    ("LEO~phone", "[hopeful] Okay. [pause] Are you coming in?")])
sc("window", ["rachel"], "Rachel letting the question sit, looking out at the dark parking lot.",
   [(N, "[soft] Rachel let the question sit."),
    ("RACHEL", "[quiet, honest] I'll tell you myself when I know.")])

# ── 18 THE LAST FAVOR ──────────────────────────────────────────────────────────────────────────────
sc("window", ["ben"], "Ben finding Rachel by the window, tired, for once not checking who's watching.",
   [(N, "[quiet] Ben found her by the window. [pause] For once, he didn't check who was watching."),
    ("BEN", "[tired, almost honest] Mara's order would have been the first thing I could point to. [pause] Something I brought in.")], music="wonder", cut=True)
sc("window", ["rachel"], "Rachel looking at him.",
   [("RACHEL", "[quiet] You could have brought it in with me."),
    ("BEN", "[bitter, low] Every time I showed up, somebody asked whether you knew I was there.")])
sc("window", ["ben", "rachel"], "Brother and sister side by side at the window.",
   [("RACHEL", "[gentle but firm] You were offering people shifts I couldn't cover."),
    ("BEN", "[rubbing his face] I know. I know how it looked.")])
sc("window", ["rachel"], "Close-up of Rachel.",
   [("RACHEL", "You heard Leo asking if he still had a job?"),
    ("BEN", "[defensive] He has a job. I was talking to a temp company. I wanted people on call. That's all."),
    ("RACHEL", "[quiet] Then tell him that... before he takes his knives home.")])
sc("window", ["ben"], "Ben putting his phone in his pocket and not reaching for it again.",
   [(N, "[soft] Ben put his phone in his pocket. [pause] He didn't reach for it again."),
    ("BEN", "[pleading, charming one last time] Please. Let Dad finish the night. Tomorrow you and I can run the tasting together. [pause] I'll tell people it's a partnership.")])
sc("window", ["rachel"], "Rachel turning to him.",
   [("RACHEL", "In front of Mara?"),
    ("BEN", "[quick] Sure."),
    ("RACHEL", "[quiet] Say it now. In front of Dad.")])
sc("window", ["ben"], "Ben glancing back into the ballroom.",
   [("BEN", "[low, defeated] He's already told people I'm taking over.")])
sc("window", ["ben", "rachel"], "Brother and sister standing at the window facing the same direction, not looking at each other.",
   [(N, "[slow] Rachel nodded once. [pause] The two of them stood by the window, facing the same direction.")])

# ── 19 THE SECOND BOX ──────────────────────────────────────────────────────────────────────────────
sc("catering", [], "A server rolling out a second white bakery box on a cart next to Rachel's box.",
   [(N, "[low] In the catering hall, a server rolled out a second white bakery box."),
    ("RACHEL", "[wary] Whose is that?")], cut=True)
sc("catering", [], "A young server in a black vest beside the two cake boxes.",
   [("SERVER", "[helpful] It came with the venue package. They had us hold it in the walk-in... in case the other one didn't come.")])
sc("catering", [], "Close-up of an open sheet cake with a printed photo of the bakery storefront and the words FRANK & SON in icing.",
   [(N, "[slow] On the sheet cake, a printer-perfect portrait of the bakery. [pause] And under it, two words. [pause] Frank... and Son.")],
   sfx=[["Low ominous tone", 2.0, 0.35, "start"]], overlay={"type": "letter", "text": "FRANK & SON"})
sc("catering", ["rachel"], "Rachel shutting the lid.",
   [("SERVER", "[innocent] Are we serving both?")],
   sfx=[["A cardboard box lid shutting", 1.0, 0.4, "start"]])
sc("catering", ["megan", "rachel"], "Megan coming up beside Rachel at the two boxes.",
   [("MEGAN", "[quiet] They had me practice cutting that one yesterday. [pause] I wondered why it didn't have your name."),
    ("RACHEL", "[very quiet] I thought I was bringing the cake... because Dad wanted me to make one.")])
sc("catering", [], "The server looking from one box to the other.",
   [("SERVER", "[helpful] I can put yours in the fridge. The other one's already chilled."),
    ("RACHEL", "[firm, quiet] I'll take mine with me.")])
sc("catering", ["rachel"], "Rachel lifting her box, then freezing at a voice from the stage.",
   [("FRANK~phone", "[distant, near a live mic] No, bring the one Rachel made. [pause] People know her cakes.")])
sc("catering", ["rachel"], "Close-up of Rachel with the box against her chest, eyes closing.",
   [(N, "[quiet] Rachel stopped with the box against her chest."),
    ("MEGAN", "[gently] You can go if you want."),
    ("RACHEL", "[after a beat] Help me get it up the stairs.")])

# ── 20 PUT THE MIC BACK ────────────────────────────────────────────────────────────────────────────
sc("aisle", ["rachel", "megan"], "Rachel and Megan wheeling the cake cart up the side aisle of the ballroom.",
   [(N, "[building] They wheeled the cake through the side aisle. [pause] Ben saw them from the stage. [pause] He put on his best smile.")], music="tension", cut=True)
sc("stage", ["ben"], "Ben on stage with the microphone, beaming.",
   [("BEN", "[into the mic, big and charming] There we go! We've got a little surprise for Dad.")],
   sfx=[["Applause in a ballroom", 2.5, 0.5, "end"]])
sc("stage", ["ben", "rachel"], "Ben leaning down off-mic to Rachel at the foot of the stage stairs.",
   [("BEN", "[off mic, through his smile] Just put it here. I'll get somebody to cut it."),
    ("RACHEL", "[quiet] I can carry it."),
    ("BEN", "[sharper] I'm trying to help you.")])
sc("stage", ["rachel"], "Close-up of Rachel looking up at him.",
   [("RACHEL", "[very quiet, immovable] Then put the microphone back on the stand.")])
sc("ballroom", ["linda", "mara"], "The photographer lining up the shot; Aunt Linda in the front row; Mara standing at the end of the row.",
   [(N, "[low] Ben looked around. The photographer was lining up the shot. Aunt Linda had moved to the front row. [pause] Mara was standing at the end of it.")])
sc("stage", ["ben"], "Ben setting the microphone back on its stand with a smile.",
   [("BEN", "[back on mic, smiling] My sister has something she wants to say.")])
sc("stage", ["rachel"], "Rachel adjusting the microphone down to her height, her hand shaking once.",
   [(N, "[quiet] Rachel adjusted the mic down to her height. Her hand shook once. [pause] She let go before anybody could get a second look.")],
   sfx=[["A microphone stand being adjusted, a soft thump over the speakers", 1.5, 0.4, "start"]])
sc("stage", ["rachel", "megan"], "Rachel at the microphone with Megan beside her, the room watching.",
   [("RACHEL", "[clear, quiet, carrying] One thing first. [pause] The woman you just saw up here is standing right beside me. [pause] I'd like you to hear her name from her.")])
sc("stage", ["ben"], "Ben's smile holding half a second too long.",
   [("BEN", "[a nervous laugh] Rach, we can explain the reenactment."),
    ("RACHEL", "[calm] Okay. [pause] Let her.")])

# ── 21 MY NAME IS RACHEL ───────────────────────────────────────────────────────────────────────────
sc("stage", ["megan"], "Megan stepping to the microphone; she shakes her head once at the camera operator.",
   [(N, "[quiet] Megan stepped to the microphone. The camera operator looked to her. [pause] She shook her head once. He lowered the camera.")], cut=True)
sc("stage", ["megan"], "Close-up of Megan at the microphone, polished smile.",
   [("MEGAN", "[in her polished stage voice, bright and sweet] My name is Rachel.")],
   sfx=[["A murmur spreading through a ballroom", 2.0, 0.35, "end"]])
sc("stage", ["megan"], "Close-up of Megan dropping the smile, taking a breath.",
   [("MEGAN", "[in her own plain voice, lower, unpolished] That's what they paid me to say. [pause] My name is Megan. [pause] I was hired to reenact a family story. Then they gave me a page that said she was leaving the bakery of her own free will.")])
sc("stage", ["ben"], "Ben stepping forward with a hand up.",
   [("BEN", "[quick, smooth] Because it was a dramatization."),
    ("MEGAN", "[level] Show them where that word is in my script.")])
sc("stage", ["megan", "ben"], "Megan holding the page out to Ben; Ben looking down at it without taking it.",
   [(N, "[dry] She held the page out. [pause] Ben looked at it. He didn't take it.")])
sc("stage", ["megan"], "Megan speaking to the room, voice shaking a little.",
   [("MEGAN", "[steady, a little shake underneath] I asked if Rachel would be here. You told me she'd agreed to watch from home. [pause] I'm saying that in front of her now... because I believed you.")])
sc("stage", ["megan", "rachel"], "Megan turning to Rachel.",
   [("MEGAN", "[quiet, still audible] I'm sorry I repeated a story you'd told your dad in private."),
    (N, "[soft] Rachel accepted that with a small nod.")])
sc("ballroom", ["linda"], "Aunt Linda standing up in the front row.",
   [("LINDA", "[no longer oblivious] Frank. [pause] When you hugged her... did you know Rachel was standing back there?")])
sc("stage", ["frank"], "Frank reaching for a water glass; it's empty; he puts it back down.",
   [(N, "[slow] Frank reached for his water. [pause] The glass was empty. [pause] He put it back down.")],
   sfx=[["An empty glass set down in a silent room", 1.0, 0.4, "start"]])

# ── 22 YOU WOULD'VE SAID NO ────────────────────────────────────────────────────────────────────────
sc("ballroom", [], "The whole ballroom silent, every face turned to the stage, a fork resting on a plate.",
   [(N, "[very quiet] The room had gone quiet enough to hear someone set down a fork.")],
   sfx=[["A single fork set down on a plate in a silent room", 1.0, 0.4, "start"]], cut=True)
sc("stage", ["frank", "rachel"], "Frank at the microphone stand turning toward his daughter Rachel beside him.",
   [("FRANK", "[to Rachel, quiet] I saw you when you came in."),
    ("RACHEL", "[softly] Okay.")])
sc("stage", ["rachel"], "Close-up of Rachel absorbing it.",
   [(N, "[soft] She gave herself time to absorb that."),
    ("RACHEL", "[quiet] You could see me. [pause] You told her to go ahead.")])
sc("stage", ["frank"], "Frank searching for words.",
   [("FRANK", "[slow] I thought if we stopped right there... it would be worse for you."),
    ("RACHEL", "[very quiet] Worse than you introducing her as your daughter?")])
sc("stage", ["frank"], "Frank not looking at Ben.",
   [(N, "[quiet] Frank didn't look at Ben. He could hear the question on his own."),
    ("FRANK", "[small] I wanted you both to have a place in it.")])
sc("stage", ["rachel", "ben"], "Rachel at the mic; Ben stepping in quickly.",
   [("RACHEL", "[quiet] Where was my place tomorrow morning?"),
    ("BEN", "[quickly] We just talked about this.")])
sc("stage", ["rachel"], "Close-up of Rachel looking straight at her father.",
   [("RACHEL", "[steady, very quiet] Dad. [pause] Did you ever ask me if I wanted to step down?")])
sc("stage", ["frank"], "Close-up of Frank, a long pause, letting the safer answer pass.",
   [(N, "[a long hold] Frank let the safer answer pass."),
    ("FRANK", "[with quiet certainty] You would've said no.")], sfx=[["Total silence, a faint room tone", 2.0, 0.2, "start"]])
sc("stage", ["rachel"], "Rachel looking down at the closed cake box.",
   [(N, "[quiet] Rachel looked down at the cake box. [pause] She left it closed.")])
sc("stage", ["rachel"], "Rachel at the microphone addressing the room.",
   [("RACHEL", "[to the room, steady] He's right. [pause] I would have said no. [pause] If you hear a different version tomorrow, you can ask me. [pause] That's all I wanted to say.")])
sc("stage", ["rachel", "ben"], "Rachel stepping away from the microphone while Ben hurries in to take it.",
   [(N, "[dry] She stepped away from the mic. Ben got there before anyone else.")])

# ── 23 I'LL SEE YOU AT NINE ────────────────────────────────────────────────────────────────────────
sc("stage", ["ben"], "Ben grabbing the microphone, smile back on, a little too loud.",
   [("BEN", "[grabbing for control, too loud] We can get into a lot of family history up here. [pause] Tomorrow morning we have a tasting. The bakery will be open, the staff will be there, and anybody who'd like to see how we work is welcome!")], music="tension", cut=True)
sc("stage", ["mara"], "Mara walking to the edge of the stage, speaking at normal volume.",
   [("MARA", "[normal volume, exact] Are you the person leading my tasting?"),
    ("BEN", "[confident] Yes.")])
sc("stage", ["mara"], "Close-up of Mara.",
   [("MARA", "[one question at a time] Is Rachel scheduled to be there?")])
sc("stage", ["ben"], "Ben looking at Rachel, realizing she won't answer for him.",
   [(N, "[slow] Ben looked at Rachel. [pause] It took him a second to realize she wasn't going to answer for him."),
    ("BEN", "[a little thinner] She can come if she wants.")])
sc("stage", ["mara"], "Mara nodding, businesslike.",
   [("MARA", "[calm, exact] I'll be there at nine. [pause] I want to see what the bakery can make with the people you have scheduled. [pause] Please let them know that's what I'm coming to see.")])
sc("stage", ["ben"], "Ben nodding as if he's just closed a deal.",
   [(N, "[dry] Ben nodded like he'd just closed a deal.")])
sc("stage", ["rachel"], "Rachel speaking to Ben at her normal work volume.",
   [("RACHEL", "[at her normal work volume, practical] The lemon filling is on the bottom shelf. Nina has the schedule you sent. [pause] If you need her earlier, ask her before you put it on the board."),
    ("BEN", "[confident] We'll figure it out."),
    ("RACHEL", "[quiet, not unkind] I know you'll try.")])
sc("stage", ["rachel"], "Rachel picking up the cake box and walking down the front stairs of the stage.",
   [(N, "[quiet] She picked up the cake. [pause] This time, she took the front stairs down.")])

# ── 24 THE FRONT DOOR ──────────────────────────────────────────────────────────────────────────────
sc("foyer", ["megan:coat", "rachel"], "Rachel and Megan stopping at the coat check in the hotel foyer.",
   [(N, "[soft] Coats rustled in the foyer."),
    ("MEGAN", "[the adrenaline wearing off, plain] For a second up there, I thought I was going to apologize to him.")], music="wonder", cut=True)
sc("foyer", ["rachel"], "Rachel glancing at her.",
   [("RACHEL", "Ben?"),
    ("MEGAN", "[quiet] Your dad. I kept hearing him say \"sweetheart.\" [pause] It felt like I was disappointing somebody I'd known my whole life.")])
sc("foyer", ["rachel"], "Rachel letting out a breath that's almost a laugh.",
   [(N, "[soft] Rachel let out a small breath that was almost a laugh."),
    ("RACHEL", "[wry] Yeah. [pause] He's good at that.")])
sc("foyer", ["megan:coat"], "Megan holding the glass door open while Rachel gets the box through.",
   [("MEGAN", "[curious] Did you make that cake before or after your shift?"),
    ("RACHEL", "[tired, a little smile] During. I kept taking it in and out of the fridge whenever we got a rush. [pause] The writing's probably crooked by now.")])
sc("foyer", ["megan:coat"], "Close-up of Megan.",
   [("MEGAN", "[gently] What does it say?")])
sc("foyer", ["rachel"], "Close-up of Rachel looking at the box.",
   [("RACHEL", "[a beat, quiet] \"Take a day off, Dad.\"")])
sc("foyer", ["megan:coat", "rachel"], "The two women looking at each other in the doorway, cold night behind them.",
   [(N, "[very soft] Neither of them said anything for a moment."),
    ("MEGAN", "[gentle] Do you want me to carry it to the car?")])
sc("foyer", [], "Close-up of Rachel's fingers marked red where the string has dug in.",
   [(N, "[quiet] Rachel looked down at the marks the string had left in her fingers."),
    ("RACHEL", "[a small surrender] Actually... yeah. Thanks.")])
sc("foyer", ["megan:coat", "rachel"], "From behind: Megan carrying the cake box, the two women walking out into the night together.",
   [(N, "[soft] She handed Megan the box. [pause] They walked out together.")],
   sfx=[["Glass doors closing, cold night wind outside", 2.0, 0.35, "start"]])

# ── 25 THE FIRST ALARM ─────────────────────────────────────────────────────────────────────────────
sc("apartment", ["rachel:home"], "Rachel in her small apartment kitchen at night, sliding the white box into the fridge.",
   [(N, "[intimate] Inside Rachel's apartment, the white box went into the fridge.")],
   sfx=[["A refrigerator door opening and closing", 1.5, 0.35, "start"]], cut=True)
sc("apartment", [], "Close-up of a phone on the counter showing an alarm at 3:12 A.M.",
   [(N, "[quiet] Her alarm went off at three twelve. [pause] She turned it off. [pause] Then she sat down and called Nina.")],
   sfx=[["A phone alarm ringing, then stopping", 2.0, 0.4, "start"]])
sc("bakery_kitchen", ["nina"], "Nina in the dark bakery kitchen, answering the phone.",
   [("NINA~phone", "[dry, half asleep] If you're about to tell me you're coming in at three, I'm hanging up."),
    ("RACHEL", "[quiet] I'm not coming in.")])
sc("bakery_kitchen", ["nina"], "Nina going still.",
   [(N, "[soft] Quiet at the other end."),
    ("NINA~phone", "[careful] Okay. [pause] Are you sure?")])
sc("apartment", ["rachel:home"], "Rachel at her little kitchen table in the dark, phone to her ear.",
   [("RACHEL", "[honest, a little rueful] Ask me again in ten minutes and I might change my mind. [pause] So I'm telling you now."),
    ("NINA~phone", "[a hint of a smile] Okay. You're not coming in.")])
sc("apartment", ["rachel:home"], "Close-up of Rachel.",
   [("RACHEL", "[practical] I wanted you to hear it from me. If he asks you to make six trays, tell him what's in the fridge and what you can actually do. [pause] I don't want anybody working off the clock to fix this."),
    ("NINA~phone", "[dry] I know.")])
sc("apartment", ["rachel:home"], "Rachel rubbing her eyes.",
   [("RACHEL", "[gentle] And you don't have to walk out on my account. I know who's got rent due.")])
sc("bakery_kitchen", ["nina"], "Nina tying her apron.",
   [("NINA~phone", "[grateful, matter-of-fact] I've got a shift at four. So does Leo. We'll make the bread. [pause] He can decide what he's doing about the tasting.")])
sc("apartment", [], "Close-up of Rachel's hand resting on the phone on the table, the screen dark.",
   [(N, "[very soft] Rachel put the phone down. [pause] For a few seconds, her hand stayed on it.")])

# ── 26 ONE SET OF KEYS ─────────────────────────────────────────────────────────────────────────────
sc("bakery_dark", ["ben"], "4:01 A.M. Ben at the bakery's glass door fumbling a ring of metal keys under a street lamp, a coffee carrier in his other hand.",
   [(N, "[dry] Four oh-one A.M. A ring of keys scraped against a lock. [pause] Ben tried another one.")],
   sfx=[["Keys scraping in a lock, a dark quiet street", 3.0, 0.4, "start"]], music="tension", cut=True)
sc("bakery_kitchen", ["nina", "leo"], "Inside, Nina and Leo watching Ben through the glass.",
   [("LEO", "[low] Should we go around back?"),
    ("NINA", "[dry] Stay here. He sees us.")])
sc("bakery_front", ["ben:shop"], "Ben finally getting the door open, holding up a carrier of coffees, too bright.",
   [("BEN", "[too bright for the hour] Morning! I brought coffee."),
    ("NINA", "[flat] Thanks. Who's on the second batch?")], sfx=[["A shop door bell jingling", 1.0, 0.4, "start"]])
sc("bakery_kitchen", ["ben:shop"], "Ben looking around the kitchen.",
   [("BEN", "[breezy] Can you show me where we keep the trays for the tasting?"),
    ("NINA", "[same flat tone] Sure. Who's on the second batch?"),
    ("BEN", "Put Leo on it.")])
sc("bakery_kitchen", ["leo"], "Leo at the oven with a sheet pan.",
   [("LEO", "[polite, worried] I'm on bread. If I take the second batch now, who's opening the counter?")])
sc("bakery_kitchen", ["ben:shop"], "Ben looking from his phone to the printed schedule Nina holds out.",
   [("BEN", "[confused] It's always three of you on these mornings."),
    ("NINA", "[dry] It was. [pause] Rachel was the third.")])
sc("bakery_kitchen", ["ben:shop"], "Ben glancing at the back door as if she might walk in late.",
   [("BEN", "[slowly getting it] She's been doing the third spot... and running the place?"),
    ("NINA", "[dry] You can ask her when you see her. [pause] In the meantime, you want to wash your hands and help me get these pans out?")])
sc("bakery_kitchen", [], "Close-up of a coat hook by the back door where Ben's suit jacket now hangs, an empty spot where an apron usually goes.",
   [(N, "[quiet] Ben hung his jacket on the hook that usually held Rachel's apron.")])

# ── 27 THE SAMPLE WITH THE BLUE DOT ────────────────────────────────────────────────────────────────
sc("bakery_kitchen", ["ben:shop"], "Ben setting three handwritten labels on the steel counter, metal trays everywhere.",
   [("BEN", "[trying to sound in charge] Which of these is the one Mara approved?"),
    ("NINA", "The one with the blue dot.")], sfx=[["Oven fan starting and stopping, sheet pans clanking", 2.5, 0.35, "start"]], cut=True)
sc("bakery_kitchen", [], "Close-up of two handwritten labels with blue dots, one marked TUESDAY, one marked THURSDAY.",
   [("BEN", "[frustrated] There are two blue dots."),
    ("NINA", "[patient] One says Tuesday. That was the first version. [pause] One says Thursday. Rachel was still changing the filling on Thursday.")])
sc("bakery_kitchen", ["nina"], "Nina taking a small container from the walk-in fridge: barely a spoonful inside.",
   [("BEN", "Then I want Thursday."),
    (N, "[dry] Nina took a small container out of the fridge. [pause] There was barely a spoonful inside.")])
sc("bakery_kitchen", ["ben:shop", "nina"], "Ben staring at the nearly empty container.",
   [("BEN", "[thrown] Where's the rest?"),
    ("NINA", "[quiet, pointed] What do you think she was coming in early to make?")])
sc("bakery_kitchen", ["ben:shop"], "Close-up of Ben, quiet, looking at the container.",
   [("BEN", "[small] I thought the samples were ready."),
    ("NINA", "[practical] They were on her list. I can do the filling from the batch sheet she left. It'll chill by nine if I start now. [pause] You'll have to work the front when we open.")])
sc("bakery_kitchen", ["ben:shop", "nina"], "Ben and Nina across the worktable.",
   [("BEN", "I need to be here when Mara comes in."),
    ("NINA", "[dry] That's at nine. We open at seven. You can do both. [pause] Rachel did.")])
sc("bakery_kitchen", ["ben:shop"], "Ben starting a reply as an oven timer goes off; Nina doesn't move.",
   [(N, "[dry] Ben had the start of a reply. [pause] Then the oven timer went off. Nina didn't move. [pause] She waited.")],
   sfx=[["A loud bakery oven timer beeping", 2.0, 0.5, "start"]])
sc("bakery_kitchen", ["nina"], "Close-up of Nina, deadpan.",
   [("BEN", "[lost] Which one is it?"),
    ("NINA", "[deadpan] The one making the noise.")])

# ── 28 YOUR NUMBER'S ON THE BOARD ──────────────────────────────────────────────────────────────────
sc("bakery_front", [], "A pleasant woman in a raincoat at the counter placing a cake order slip down, the shop bell above the door.",
   [("CUSTOMER", "[pleasant] Birthday pickup, nine o'clock. I'm early. [pause] Rachel texted me last night that I could wait inside if it was raining.")],
   sfx=[["A shop door bell, rain outside", 1.5, 0.4, "start"]], cut=True)
sc("bakery_front", ["ben:shop"], "Ben checking the rack behind the counter.",
   [("BEN", "[polite] What name?"),
    ("CUSTOMER", "[warm, amused] Isabel. It's for my kid. He picked lemon. Then he changed it to chocolate. [pause] Then he got afraid Rachel would be mad at him and changed it back to lemon.")])
sc("bakery_front", [], "Close-up of a cake box on the rack with ISABEL written on it in marker and a tiny hand-drawn lemon beside the name.",
   [(N, "[soft] Ben found the box. Rachel had written Isabel's name on it. [pause] And drawn a little lemon next to it."),
    ("BEN", "[quiet] Is this it?"),
    ("CUSTOMER", "[delighted] That's it. Tell her thanks.")])
sc("bakery_kitchen", ["leo"], "Leo calling from the oven with a phone in his hand.",
   [("LEO", "[calling out] There's a supplier on the phone who wants to know where to put forty cases."),
    ("BEN", "[from the front] What cases?")], sfx=[["A phone ringing in a busy kitchen", 1.5, 0.4, "start"]])
sc("bakery_kitchen", ["leo"], "Close-up of Leo, a little too pleased to say it.",
   [("LEO", "[plain] The ones you ordered for the six stores.")])
sc("bakery_front", ["ben:shop"], "Ben looking out at the empty sidewalk, putting the order slip down very carefully.",
   [(N, "[slow] Ben looked out at the empty sidewalk. [pause] He put the order slip down very carefully."),
    ("BEN", "[quiet] Tell him to wait one minute.")])
sc("bakery_kitchen", ["leo"], "Leo pointing at a whiteboard by the phone with Ben's number written on it.",
   [("LEO", "[dry] I put him on hold. Your number's on the board. [pause] He's already tried it twice.")])
sc("bakery_front", ["ben:shop"], "Ben pulling out his phone: two missed calls.",
   [(N, "[quiet] Ben pulled out his phone. Two missed calls. [pause] He called the supplier back himself.")])

# ── 29 THE TASTING ─────────────────────────────────────────────────────────────────────────────────
sc("bakery_front", ["mara"], "Nine o'clock: Mara pulling up a chair at the little table by the window.",
   [(N, "[measured] Nine o'clock. Mara pulled up a chair at the little table by the window.")], music="tension", cut=True)
sc("bakery_front", ["ben:shop"], "Ben setting down a plate of samples, composed again.",
   [("BEN", "[composed, charming again] Sorry about last night. It got a little personal. [pause] The recipe's the same. Same ingredients, same people.")])
sc("bakery_front", [], "Close-up of a fork cutting into a lemon pastry sample, a little filling leaking onto the plate.",
   [(N, "[quiet] Mara cut into a sample. A little filling leaked onto the plate."),
    ("MARA", "[pleasant, exact] Who made this batch?")])
sc("bakery_front", ["ben:shop"], "Ben glancing at Nina behind the counter.",
   [("BEN", "[smooth] We all pitched in."),
    (N, "[dry] Nina set her coffee cup down at the counter. Ben saw her.")])
sc("bakery_front", ["ben:shop"], "Ben correcting himself.",
   [("BEN", "[correcting himself, plainer] Nina made the filling. Leo baked it. I was at the counter."),
    ("MARA", "[warm] Thank you. [pause] Could you make it taste the same again tomorrow?")])
sc("bakery_front", ["ben:shop"], "Ben looking at the different labels stuck to the backs of the sample plates.",
   [(N, "[slow] Nina waited for Ben to answer. He looked at the different labels on the backs of the plates."),
    ("BEN", "[honest, uneasy] We'd need to run it a few more times.")])
sc("bakery_front", ["mara"], "Close-up of Mara.",
   [("MARA", "[one question at a time] How many stores can you supply... with the crew you had this morning?")])
sc("bakery_front", ["ben:shop"], "Ben starting to say six, catching himself.",
   [(N, "[quiet] Ben started to say six. [pause] He caught himself."),
    ("BEN", "[small, honest] I don't know.")])
sc("bakery_front", ["mara"], "Mara putting down her fork.",
   [("MARA", "[calm, exact] I'm holding the order. [pause] I'd come back for another tasting when you know what you can make consistently. [pause] You can send me two good trays. We can start there.")])
sc("bakery_front", ["ben:shop", "mara"], "Ben leaning in hopefully; Mara standing.",
   [("BEN", "[hopeful] Can I tell Dad we still have a shot?"),
    ("MARA", "[gentle, firm] You can tell him exactly what I just told you.")])
sc("bakery_front", ["mara"], "Mara taking one more small bite of the sample before she goes.",
   [(N, "[soft] Mara took one more small bite before she left. [pause] Nina noticed. [pause] So did Ben.")])

# ── 30 ONE DAY ─────────────────────────────────────────────────────────────────────────────────────
sc("bakery_kitchen", ["frank:shop", "ben:shop"], "Frank arriving in the back kitchen; Ben scraping dried filling off the worktable.",
   [("FRANK", "[hopeful] How'd it go?"),
    ("BEN", "[flat, tired] She's holding the order. [pause] She asked me how much we can make, and I told her I don't know.")], music="wonder", cut=True)
sc("bakery_front", [], "The bakery front through the kitchen door: every table full, a line at the counter.",
   [(N, "[slow] Frank looked at the front windows. The shop was open. The tables were full. [pause] His son was wearing an apron he hadn't tied properly.")])
sc("bakery_kitchen", ["frank:shop"], "Frank turning to Ben.",
   [("FRANK", "[quiet] Call your sister."),
    ("BEN", "[stubborn] I can finish the shift."),
    ("FRANK", "That's not what I meant."),
    ("BEN", "[a beat, then] Then you call her.")])
sc("bakery_desk", ["frank:shop"], "Frank at the little back desk where he used to do payroll, holding the corded phone.",
   [(N, "[soft] Frank made the call from the desk where he used to do payroll. [pause] Rachel answered on the fourth ring.")],
   sfx=[["A phone ringing four times on the other end", 3.0, 0.3, "start"]])
sc("bakery_desk", ["frank:shop"], "Close-up of Frank on the phone, slipping into an old habit.",
   [("FRANK", "[soft, slipping into an old habit] Could you come in? [pause] Just for today."),
    ("RACHEL~phone", "[even] What do you need?")])
sc("bakery_desk", ["frank:shop"], "Frank rubbing his forehead.",
   [("FRANK", "[wheedling] Everything's backed up. Ben's doing his best. If you can give us a couple of hours... we'd really appreciate it.")])
sc("apartment_day", ["rachel:home"], "Rachel in her sunny kitchen taking a plate out of a cabinet and setting it down, phone at her ear.",
   [(N, "[quiet] Rachel took a plate out of a cabinet. Set it down."),
    ("RACHEL", "[quiet, direct] Did you tell the crew I wanted to leave?")])
sc("bakery_desk", ["frank:shop"], "Frank at the desk, an oven timer ringing in the background.",
   [("BEN~phone", "[distant] I've got it!"),
    ("FRANK", "[a long pause, then small] I said you'd agreed.")], sfx=[["An oven timer ringing in a bakery", 1.5, 0.3, "start"]])
sc("apartment_day", ["rachel:home"], "Close-up of Rachel, calm.",
   [("RACHEL", "[calm] They need to hear from you that I didn't."),
    ("FRANK~phone", "[uneasy] You want me to say that in front of everybody?"),
    ("RACHEL", "[simply] You said the other thing in front of everybody.")])

# ── 31 THE CORRECTION ──────────────────────────────────────────────────────────────────────────────
sc("bakery_front", ["frank:shop"], "Frank asking the crew to come to the counter; customers at tables looking up.",
   [(N, "[quiet] Frank asked the crew to come to the counter. Leo stayed near the prep table, a towel over his shoulder. [pause] Ben put down his pen.")], cut=True)
sc("bakery_front", ["frank:shop"], "Close-up of Frank speaking to his staff, awkward.",
   [("FRANK", "[awkward, speaking to the people, not the room] I told Nina that Rachel wanted to step down. I said it to Mara, too. [pause] Rachel never agreed to it. [pause] I wanted Ben in charge. And I wanted people to think we'd all come to that decision together.")])
sc("bakery_front", [], "A customer at a table stopping mid-stir with a coffee spoon.",
   [(N, "[soft] Someone at a table stopped stirring a coffee. [pause] Frank could have lowered his voice. [pause] He didn't.")])
sc("bakery_front", ["frank:shop"], "Frank, voice steady now.",
   [("FRANK", "[steady, ashamed] When I said she needed a break, I knew she'd still come in early if we asked. [pause] I counted on it.")])
sc("bakery_front", ["nina"], "Nina with her arms folded.",
   [("NINA", "[dry] Is she coming in today?"),
    ("FRANK", "[quiet] No. [pause] And I asked.")])
sc("bakery_front", ["frank:shop", "ben:shop"], "Frank sliding the printed schedule toward Ben across the counter.",
   [("FRANK", "[firm, quiet] You told them you could run this. [pause] Tell them what you're doing about tomorrow.")])
sc("bakery_front", ["ben:shop"], "Ben picking up the sheet; a long beat.",
   [(N, "[slow] Ben picked up the sheet. [pause] There was a long beat before he spoke."),
    ("BEN", "[plain, for once] Leo, your shift's at four. I'll come in at three to take the delivery. [pause] Nina, if I write anything down that we don't have enough people to do, tell me before I send it out.")])
sc("bakery_front", ["nina"], "Close-up of Nina.",
   [("NINA", "[dry] I did.")])
sc("bakery_front", ["ben:shop"], "Ben nodding, not arguing.",
   [(N, "[soft] Ben looked at her. He didn't argue."),
    ("BEN", "[quiet, plain] Okay. [pause] I'll listen this time.")])

# ── 32 THE FIRST SLICE ─────────────────────────────────────────────────────────────────────────────
sc("apartment_day", ["nina"], "Late afternoon: Nina at Rachel's apartment door holding a neatly folded, flour-stained apron.",
   [(N, "[warm] Late afternoon. A knock at Rachel's door."),
    ("NINA", "[dry, warm underneath] Washed it. [pause] Stain didn't come out."),
    ("RACHEL", "[a small smile] It never does. Come in.")], sfx=[["A knock on an apartment door", 1.0, 0.4, "start"]], music="wonder", cut=True)
sc("apartment_day", ["rachel:home"], "Rachel taking the white box out of the fridge and opening it on the table.",
   [(N, "[soft] Nina set the apron over the back of a chair. Rachel took the cake out of the fridge and opened the box.")])
sc("apartment_day", [], "Close-up of a lemon cake in an open white box, a little frosting caught on the lid, slightly crooked piped writing reading TAKE A DAY OFF, DAD.",
   [(N, "[quiet] A little frosting had caught on the lid. [pause] The message was still legible.")],
   overlay={"type": "letter", "text": "Take a day off, Dad."})
sc("apartment_day", ["nina"], "Nina leaning over the cake.",
   [("NINA", "[curious] Did he really tell you to take the day off?"),
    ("RACHEL", "[looking at the cake, a trace of a smile] No. [pause] I wrote it for him.")])
sc("apartment_day", [], "Close-up of Rachel's phone lighting up with a text message.",
   [(N, "[soft] Rachel's phone lit up. A message from Frank.")],
   overlay={"type": "message", "from": "Dad", "to": "Rachel", "text": "I told them. I'll call you Sunday, if you want."})
sc("apartment_day", ["rachel:home"], "Rachel typing a short reply, then putting the phone face down.",
   [(N, "[soft] She read it. [pause] She typed: Sunday afternoon. [pause] Then she put the phone face down.")])
sc("apartment_day", ["nina"], "Nina holding out her hand.",
   [("NINA", "[practical] Got a knife?")])
sc("apartment_day", ["rachel:home"], "Rachel studying the cake with a knife in hand, then cutting a generous slice.",
   [(N, "[warm, slow] Rachel got one from a drawer. For a moment she studied the cake, like she was working out how many people it could serve. [pause] Then she cut a generous slice.")])
sc("apartment_day", ["nina"], "Nina teasing gently.",
   [("NINA", "[teasing, gently] Who's the first piece for?")])
sc("apartment_day", ["rachel:home", "nina"], "Rachel pulling her own plate with a slice of lemon cake closer, a small unapologetic smile, Nina laughing across the table.",
   [("RACHEL", "[small smile, no apology, finally unhurried] Mine. [pause] For once.")],
   sfx=[["A plate sliding across a wooden table", 1.0, 0.4, "end"]])
sc("apartment_day", [], "The sunny kitchen table from a distance: two women, one slice of lemon cake, an apron over a chair.",
   [(N, "[warm, final] For years, everyone in that family had counted on Rachel showing up before anyone asked. [pause] The morning she didn't... they finally learned what she'd been carrying."),
    (N, "[warm] This has been Karma Tales. [pause] Every betrayal has a price. And karma always collects.")])


def main():
    scenes, music = [], []
    for i, (place, chars, image, lines, extra) in enumerate(S, start=1):
        sid = f"s{i:02d}"
        scene = {"id": sid, "chars": chars, "image": image, "lines": [list(l) for l in lines]}
        if place:
            scene["place"] = place
        for key in ("cut", "sfx", "motion", "overlay"):
            if extra.get(key):
                scene[key] = extra[key]
        if extra.get("music"):
            music.append([sid, extra["music"]])
        scenes.append(scene)
    roles = {r.split("~")[0] for s in scenes for r, _ in s["lines"]}
    looks = {c for s in scenes for c in s["chars"]}
    assert looks <= set(LOOKS), looks - set(LOOKS)
    assert all(not v.endswith("_VOICE") for r, v in VOICES.items() if r in roles), "voices not cast yet"
    title = "My Dad Hired an Actress to Play Me at His Retirement Party. I Walked In With the Cake."
    spec = {
        "title": "Karma Tales EP08 - Replaced",
        "voices": {r: VOICES[r] for r in sorted(roles)},
        "cast": CAST,
        "portraits": {k: PORTRAIT + v for k, v in PORTRAITS.items()},
        "looks": LOOKS,
        "style": "Photorealistic still from a prestige American TV drama, shot on 35mm, warm amber cinematic lighting, shallow depth of field, natural skin texture, rich contrast, wide 16:9 frame. Keep every person's face and hair exactly consistent with their reference photo. No text, no captions, no watermark unless the scene asks for written words. Any party banner reads exactly HAPPY RETIREMENT FRANK, never any other name; otherwise show no signs. ",
        "resolution": "2K",
        "music": music,
        "places": PLACES,
        "ambiences": {
            "party": ["Large hotel ballroom party, murmuring crowd, glasses clinking, soft band far away", 0.05],
            "back": ["Backstage behind a curtain, muffled party voices through fabric", 0.04],
            "corridor": ["Hotel service corridor, fluorescent hum, distant kitchen clatter", 0.05],
            "stairs": ["Concrete stairwell echo, muffled music through a door", 0.04],
            "office": ["Small office, muffled party through the wall", 0.04],
            "kitchen": ["Commercial bakery kitchen, oven fans, mixer hum", 0.06],
            "front": ["Small busy bakery, murmur of customers, espresso machine", 0.06],
            "street": ["Empty street before dawn, distant traffic", 0.05],
            "night": ["Quiet apartment at night, refrigerator hum", 0.04],
            "day": ["Quiet apartment afternoon, birds outside", 0.04]},
        "ambience": [],
        "scenes": scenes,
        "youtube": {
            "title": title,
            "description": "Rachel brought the cake to her father's retirement party. She walked in just as a woman at the microphone was telling a story about Dad's birthday cake. Her story. Then the host said: \"Frank's daughter, Rachel, everybody.\"\n\nHer father saw her standing in the aisle. And told the stranger, \"Go ahead, sweetheart.\"\n\nKarma Tales: revenge and twist stories where the people who scheme always get what they deserve.\n\nThis story is fiction. Any resemblance to real people or events is coincidental. Narration and images are AI-generated.\n\n#karmatales #familydrama #revengestory #familybusiness",
            "tags": ["karma tales", "family drama", "revenge story", "family betrayal", "family business", "retirement party", "father and daughter", "sibling rivalry", "audio drama", "twist ending"],
            "category": "24",
            "shorts_description": "Watch the full story on Karma Tales: https://youtu.be/aPS3d-FoZL0\n" + title + "\n\n#shorts #karmatales #familydrama",
        },
        "thumbnail_file": "karma/ep08_thumb.jpg",
        "shorts_end_card": "Watch the full story|on our channel",
        "shorts": [
            {"id": "short1", "title": "\"Dad.|Who is she?\"", "from": "s01", "to": "s13",
             "youtube_title": "A Stranger Told My Story at Dad's Party. Then He Called Her His Daughter. #shorts"},
            {"id": "short2", "title": "FINAL TAKE", "from": "s21", "to": "s26",
             "youtube_title": "The Actress Had One More Line to Read. About Me. #shorts"},
            {"id": "short3", "title": "\"My name is Rachel.\"", "from": "s159", "to": "s166",
             "youtube_title": "They Paid Her to Say My Name. So She Told Everyone Hers. #shorts"},
            {"id": "short4", "title": "\"Did you ever|ask me?\"", "from": "s168", "to": "s177",
             "youtube_title": "I Asked My Dad One Question in Front of Everyone #shorts"},
            {"id": "short5", "title": "\"Which one is it?\"", "from": "s213", "to": "s220",
             "youtube_title": "He Took Over Her Bakery. He Lasted Until the First Oven Timer. #shorts"},
        ],
    }
    tone = {"ballroom": "party", "aisle": "party", "stage": "party", "av": "party", "window": "party", "backstage": "back",
            "corridor": "corridor", "catering": "corridor", "foyer": "corridor", "stairwell": "stairs", "office": "office",
            "bakery_kitchen": "kitchen", "bakery_front": "front", "bakery_desk": "kitchen", "bakery_dark": "street",
            "apartment": "night", "apartment_day": "day"}
    last = None
    for s in scenes:
        key = tone.get(s.get("place", ""))
        if key and key != last:
            spec["ambience"].append([s["id"], key])
            last = key
    out = ROOT / "karma" / "ep08_full.json"
    out.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")
    words = sum(len(t.split()) for s in scenes for _, t in s["lines"])
    print(f"{out.name}: {len(scenes)} scenes, {words} words, {sum(1 for s in scenes if s.get('motion'))} moving clips")


if __name__ == "__main__":
    main()
