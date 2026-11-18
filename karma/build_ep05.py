"""Write karma/ep05_full.json, Karma Tales EP05 "The Father They Buried", from the user's 18-scene script.

usage: python karma/build_ep05.py
Polish over the draft: the cold open is the same chapel moment the story returns to, Mia's recording and Sarah's
arrival are set up before they pay off, Catherine learns she was lied to as well, and James cuts Ethan loose.
eleven_v3 audio tags on nearly every line so the delivery is acted.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

VOICES = {
    "NARRATOR": "FmtiHEcHpocK7YiZwa46",  # Jason - channel narrator
    "THOMAS": "THOMAS_VOICE",
    "OLIVIA": "OLIVIA_VOICE",
    "ETHAN": "ETHAN_VOICE",
    "CATHERINE": "CATHERINE_VOICE",
    "JAMES": "JAMES_VOICE",
    "MIA": "MIA_VOICE",
    "SARAH": "SARAH_VOICE",
    "OFFICIANT": "wAGzRVkxKEs8La0lmdrE",  # older, measured
}
CASTING = ROOT / "karma" / "voices_ep05.json"
if CASTING.exists():
    VOICES.update(json.loads(CASTING.read_text()))

CAST = {c: f"karma/cast/ep05/{c}.jpg" for c in ["olivia", "thomas", "ethan", "catherine", "james", "mia", "sarah", "officiant"]}

PORTRAIT = ("Photorealistic still from a prestige American TV drama, shot on 35mm, shallow depth of field, soft cinematic key light, "
            "natural skin texture, head-and-shoulders portrait facing slightly off camera, neutral dark background, an entirely "
            "fictional person who resembles no real celebrity, no text, no watermark. ")
PORTRAITS = {
    "ethan": "Ethan Blackwood, a 34-year-old American man, handsome, dark brown hair neatly swept back, clean-shaven strong jaw, cool gray eyes, a polished confident half-smile, navy suit with a white shirt.",
    "catherine": "Catherine Blackwood, a 59-year-old American woman, sleek ash-blonde bob, high cheekbones, cool blue eyes, a thin polite smile, pearl earrings, ivory silk blouse.",
    "james": "James Blackwood, a 65-year-old American businessman, thick swept-back white hair, clean-shaven, heavy brows, stern dark eyes, charcoal suit with a burgundy tie.",
    "mia": "Mia Torres, a 30-year-old American woman, dark curly shoulder-length hair, warm brown skin, expressive dark eyes, a bold direct look, small gold hoop earrings, olive green jacket.",
    "sarah": "Sarah Mitchell, a 48-year-old American attorney, auburn hair in a low neat bun, sharp green eyes, light freckles, tortoiseshell glasses, tailored navy blazer.",
    "officiant": "Reverend Hale, a 70-year-old American minister, thinning white hair, kind tired eyes, wire-rimmed glasses, white clerical robe with a gold stole.",
}

LOOKS = {
    "olivia": "Olivia (the woman from the reference photo, same face, chestnut-brown hair in a soft updo with loose strands, in a lace wedding dress and long veil, calm expression unless the scene says otherwise)",
    "olivia:casual": "Olivia (the same woman as the reference photo, same face, chestnut-brown hair loose, in a camel coat over a cream sweater)",
    "olivia:dinner": "Olivia (the same woman as the reference photo, same face, chestnut-brown hair down, in a simple black cocktail dress)",
    "olivia:night": "Olivia (the same woman as the reference photo, same face, chestnut-brown hair loose, in a gray hoodie, eyes tired)",
    "olivia:yard": "Olivia (the same woman as the reference photo, same face, chestnut-brown hair in a ponytail, relaxed and smiling, in a denim shirt)",
    "thomas": "Thomas (the older man from the reference photo, same face, gray hair and gray beard, in a dark gray mechanic's work shirt with grease stains)",
    "thomas:wedding": "Thomas (the older man from the reference photo, same face, gray hair and gray beard, in a worn dark brown jacket over a gray button-up shirt, no tie)",
    "thomas:home": "Thomas (the same older man as the reference photo, same face, in a plain flannel shirt)",
    "thomas:yard": "Thomas (the same older man as the reference photo, same face, smiling, in an old faded blue shirt)",
    "ethan": "Ethan (the dark-haired man from the reference photo, same face, in a black tuxedo with a white boutonniere)",
    "ethan:suit": "Ethan (the dark-haired man from the reference photo, same face, in a navy suit, no tie)",
    "catherine": "Catherine (the ash-blonde woman from the reference photo, same face, in a pale blue silk mother-of-the-groom dress and pearls)",
    "catherine:home": "Catherine (the ash-blonde woman from the reference photo, same face, in an ivory silk blouse and pearls)",
    "james": "James (the white-haired man from the reference photo, same face, in a charcoal suit)",
    "mia": "Mia (the curly-haired woman from the reference photo, same face, in a sage-green bridesmaid dress)",
    "mia:casual": "Mia (the curly-haired woman from the reference photo, same face, in an olive green jacket)",
    "sarah": "Sarah (the auburn-haired woman with glasses from the reference photo, same face, in a tailored navy suit)",
    "officiant": "the minister (the white-haired man in glasses from the reference photo, in a white clerical robe)",
}

PLACES = {
    "chapel": "Setting: a historic stone chapel in Philadelphia on a bright fall morning, stained glass, white flowers on every pew, about two hundred well-dressed wedding guests, a long aisle to the altar.",
    "garage": "Setting: a small old auto repair garage in a working-class Philadelphia neighborhood, an open bay door, an old sedan on a lift, tools on pegboard, a radio on a shelf, afternoon light.",
    "garage_night": "Setting: the same small auto repair garage at night, bay door closed, one hanging work lamp, a desk with an old phone and a coffee mug.",
    "restaurant": "Setting: an elegant upscale restaurant in Philadelphia's Rittenhouse Square at night, white tablecloths, candles, crystal glasses, dark wood.",
    "street": "Setting: a Philadelphia city sidewalk at night outside an upscale restaurant, wet pavement, streetlights, a black luxury car at the curb.",
    "mansion": "Setting: the bright formal music room of a Main Line Philadelphia mansion, a grand piano, tall windows, fresh flowers, a table covered in wedding programs and seating charts.",
    "apartment": "Setting: a sleek modern high-rise apartment in Center City Philadelphia at night, floor-to-ceiling windows with city lights, gray minimalist furniture.",
    "kitchen": "Setting: a small modest row-house kitchen in Philadelphia in the evening, an old table for two, a small birthday cake with candles, a wall calendar.",
    "law_office": "Setting: a downtown Philadelphia law office, tall windows over the city, bookshelves of legal binders, a large wooden desk with files.",
    "hotel": "Setting: an upscale hotel suite in Philadelphia the night before a wedding, a wedding dress hanging on a closet door, an open suitcase on the bed, soft lamps.",
    "backyard": "Setting: a small Philadelphia row-house backyard on a sunny late-summer afternoon, a charcoal grill, string lights, a picnic table with a checkered cloth.",
}

N = "NARRATOR"
S = []


def sc(place, chars, image, lines, **extra):
    S.append((place, chars, image, lines, extra))


# SCENE 1 - COLD OPEN: THE DEAD MAN AT THE WEDDING
sc("chapel", [], "Wide shot down the aisle of a packed chapel, the bride and groom at the altar in soft morning light.",
   [(N, "[low, deliberate] The bride had told everyone her father was dead.")],
   sfx=[["Gentle wedding string quartet in a stone chapel, guests whispering", 4.0, 0.25, "start"]], music="tension")
sc("chapel", ["officiant"], "The minister at the altar, open book in his hands, looking out at the guests.",
   [("OFFICIANT", "[warm, ceremonial] If anyone here knows of a reason these two should not be joined in marriage... [pause] speak now.")])
sc("chapel", [], "The heavy carved wooden chapel doors swinging open, daylight pouring in behind the dark silhouette of a broad-shouldered older man in a jacket, seen from inside the chapel.",
   [(N, "[quiet] Then the chapel doors opened.")],
   sfx=[["Heavy old church doors creaking open, echo in a stone hall", 2.5, 0.5, "start"]], motion="the heavy doors swing open and light floods into the aisle")
sc("chapel", ["thomas:wedding"], "Thomas standing alone at the back of the aisle in a worn jacket, light behind him, every guest turning.",
   [("THOMAS", "[clear, steady, carrying across the chapel] I do.")],
   sfx=[["String music stopping abruptly, a crowd gasping", 2.0, 0.45, "start"]])
sc("chapel", ["olivia"], "Olivia at the altar in her wedding dress, turning, her bouquet slipping in her hands, face drained of color.",
   [("OLIVIA", "[breath catching, a whisper] ...Dad?")],
   motion="she turns slowly toward the doors, her bouquet trembling")
sc("chapel", ["ethan"], "Ethan at the altar in a tuxedo, jaw tight, eyes narrowing at the back of the chapel.",
   [("ETHAN", "[low, through his teeth] Who the hell is that?"),
    ("THOMAS", "[walking slowly down the aisle] My name is Thomas Reed. [pause] I'm the bride's father.")])
sc("chapel", ["catherine", "james"], "Front pew: Catherine gripping James's arm, staring at the aisle as if she has seen a ghost.",
   [("CATHERINE", "[horrified whisper] That's impossible."),
    ("JAMES", "[low] Catherine?"),
    ("CATHERINE", "[barely audible] Ethan told me he was dead. [pause] I printed his name in the program.")])
sc("chapel", [], "Close-up of a wedding program on a pew, the words 'In Loving Memory' printed above a name.",
   [(N, "[slow] Two hundred guests were holding a wedding program with his name in it. [pause] Under the words: In loving memory.")])
sc("chapel", ["olivia", "ethan"], "Olivia stepping toward the aisle; Ethan catching her wrist hard.",
   [("OLIVIA", "[shaking, pleading] Dad, please. You have to leave. [pause] Because if you stay..."),
    ("ETHAN", "[quiet, cold, gripping her wrist] Olivia. Don't say another word.")])
sc("chapel", ["thomas:wedding"], "Thomas halfway down the aisle, stopping, eyes locked on Ethan's hand around Olivia's wrist.",
   [("THOMAS", "[very quiet, dangerous] Take your hand off my daughter.")],
   sfx=[["Deep cinematic boom", 2.0, 0.4, "end"]])
sc("chapel", ["thomas:wedding"], "Close-up of Thomas's weathered face, eyes wet but steady.",
   [(N, "[low] To understand how a living man ended up in his own memorial... we have to go back six months. [pause] To a phone call in a garage.")],
   sfx=[["Low sustained chord fading out", 3.0, 0.3, "start"]])

# SCENE 2 - SIX MONTHS EARLIER: THE GARAGE
sc("garage", ["thomas"], "Six months earlier: Thomas leaning into the engine of an old sedan, wrench in hand, sleeves rolled up.",
   [(N, "Six months earlier."),
    ("THOMAS", "[straining, muttering to the car] Come on, old girl. One more turn.")],
   sfx=[["Garage ambience, a wrench clinking, old radio playing soft rock", 4.0, 0.3, "start"]], music="wonder", cut=True)
sc("garage", ["thomas"], "Thomas stepping back from the sedan as the engine catches, wiping his hands on a rag, grinning.",
   [("THOMAS", "[satisfied chuckle] There we go.")],
   sfx=[["An old car engine sputtering then starting and idling", 3.0, 0.45, "start"]], motion="he steps back from the running engine and wipes his hands on a rag")
sc("garage", [], "No people in the frame. A small crowded Philadelphia garage wall: faded photos of a little girl in a school play, a graduation cap, all pinned beside the tool pegboard.",
   [(N, "[warm] Thomas Reed had spent thirty-five years fixing cars in the same small Philadelphia garage. He wasn't wealthy. His work shirts always smelled like motor oil.")])
sc("garage", [], "Close-up of an old faded photo of Thomas holding a little girl on his shoulders at a fair.",
   [(N, "But he had raised Olivia alone after her mother died. He worked weekends to pay her college tuition. He never missed a school play, a graduation, or a birthday. [pause] Then Olivia met Ethan Blackwood. [pause] And everything changed.")])
sc("garage", ["thomas"], "Thomas answering an old phone with a greasy hand, face lighting up.",
   [("THOMAS", "[bright, warm] Hey, pumpkin!"),
    ("OLIVIA~phone", "[a tired sigh] Dad, don't call me that."),
    ("THOMAS", "[sheepish laugh] Sorry. Old habit. [pause] How's my favorite daughter?")],
   sfx=[["Old phone ringing in a garage", 2.0, 0.4, "start"]])
sc("apartment", ["olivia:casual"], "Olivia on a phone call by a tall window in a sleek apartment, smiling faintly despite herself.",
   [("OLIVIA", "[small smile in her voice] I'm your only daughter."),
    ("THOMAS~phone", "[proud] Exactly. Undefeated champion."),
    ("OLIVIA", "[hesitant] Dad... I need to tell you something.")])
sc("garage", ["thomas"], "Thomas turning down the radio, suddenly worried.",
   [("THOMAS", "[concerned] What's wrong?"),
    ("OLIVIA~phone", "[quiet] Ethan proposed."),
    ("THOMAS", "[stunned, then overjoyed] He did? [laughs] Olivia, that's wonderful!")],
   sfx=[["Radio clicked off", 0.8, 0.35, "start"]])
sc("apartment", ["olivia:casual"], "Olivia looking down at a large diamond ring on her hand, not smiling.",
   [("OLIVIA", "[flat] Thanks."),
    ("THOMAS~phone", "[excited] When's the wedding?"),
    ("OLIVIA", "[too quickly] We haven't decided.")])
sc("garage", ["thomas"], "Thomas sitting down on an overturned bucket, grinning, phone at his ear.",
   [("THOMAS", "[warm, certain] Well, whenever it is, I'll be there."),
    ("OLIVIA~phone", "[hesitating] Dad..."),
    ("THOMAS", "What?")])
sc("apartment", ["olivia:casual"], "Olivia pressing her forehead against the cold window glass.",
   [("OLIVIA", "[carefully] Ethan's family is very... traditional."),
    ("THOMAS~phone", "[chuckling] So am I. I still use a paper calendar."),
    ("OLIVIA", "[pained] I'm serious.")])
sc("garage", ["thomas"], "Thomas's smile fading as he listens.",
   [("THOMAS", "[gently] So am I."),
    ("OLIVIA~phone", "[strained] They have expectations."),
    ("THOMAS", "[slowly] About what?"),
    ("OLIVIA~phone", "[almost a whisper] Everything.")])
sc("garage", ["thomas"], "Thomas looking down at his grease-stained hands.",
   [("THOMAS", "[trying to lighten it] Well... I can rent a tuxedo."),
    ("OLIVIA~phone", "[quiet] It's not about the tuxedo.")],
   sfx=[["Silence, only an idling engine in the background", 2.0, 0.2, "start"]])
sc("garage", ["thomas"], "Close-up of Thomas, phone at his ear, waiting.",
   [("THOMAS", "[softly] Then what is it about?"),
    ("OLIVIA~phone", "[rushed] I have to go. I'll call you later.")],
   sfx=[["Call disconnect tone", 1.0, 0.4, "end"]])
sc("garage", ["thomas"], "Thomas alone in the garage, slowly lowering the phone, the radio silent.",
   [(N, "[slow] She didn't call later. Not that night. Not the next. [pause] And for the first time in twenty-nine years, Thomas wondered whether his daughter was ashamed of him.")],
   motion="he slowly lowers the phone and stares at the floor")

# SCENE 3 - THE BLACKWOOD DINNER
sc("restaurant", ["catherine:home", "james"], "Catherine and James Blackwood at a candlelit table, Catherine smiling over her wine glass.",
   [("CATHERINE", "[sweet, probing] Olivia, darling. Tell us about your family.")],
   sfx=[["Upscale restaurant, glasses clinking, soft piano", 4.0, 0.3, "start"]], music="tension", cut=True)
sc("restaurant", ["olivia:dinner"], "Olivia at the table, napkin twisted in her lap, forcing a polite smile.",
   [("OLIVIA", "[polite, careful] There's not much to tell."),
    ("JAMES", "[businesslike] Your mother?"),
    ("OLIVIA", "[quietly] She passed away when I was young.")])
sc("restaurant", ["catherine:home"], "Catherine tilting her head with practiced sympathy.",
   [("CATHERINE", "[practiced sympathy] How tragic. [pause] And your father?"),
    ("OLIVIA", "[hesitating] He...")])
sc("restaurant", ["ethan:suit", "olivia:dinner"], "Ethan smoothly cutting in, hand on Olivia's shoulder, smiling at his parents.",
   [("ETHAN", "[smooth, cutting in] Olivia's father isn't in the picture."),
    ("CATHERINE", "[eyebrows rising] Oh?"),
    ("OLIVIA", "[startled] Ethan—")])
sc("restaurant", ["ethan:suit", "olivia:dinner"], "Ethan squeezing Olivia's hand on the table a little too tightly.",
   [("ETHAN", "[gently, firmly] It's a difficult subject, Mom."),
    ("CATHERINE", "[cool] I see.")])
sc("restaurant", ["james"], "James setting down his fork, looking at Olivia over his glasses.",
   [("JAMES", "[measured] Well. Family history is important when two families come together."),
    ("ETHAN", "[tight] Dad, please."),
    ("CATHERINE", "[pleasant, persistent] No, James has a point. [pause] Olivia, was your father a businessman?")])
sc("restaurant", ["olivia:dinner"], "Olivia lifting her chin.",
   [("OLIVIA", "[quiet pride] He was a mechanic."),
    ("CATHERINE", "[a beat too long] A mechanic?"),
    ("ETHAN", "[quickly] He owned a small repair shop.")])
sc("restaurant", ["catherine:home"], "Catherine's thin polite smile, eyes cold.",
   [("CATHERINE", "[sweetly, condescending] How... [pause] hardworking."),
    ("OLIVIA", "[firm] He worked very hard."),
    ("CATHERINE", "[dismissive] Of course, dear.")])
sc("restaurant", ["catherine:home", "james"], "Catherine and James exchanging a silent knowing look across the table.",
   [(N, "[low] Olivia noticed the look Catherine gave James. [pause] And Ethan noticed Olivia noticing.")])
sc("street", ["olivia:dinner", "ethan:suit"], "Outside the restaurant at night, Olivia stopping on the wet sidewalk, turning on Ethan.",
   [("OLIVIA", "[hurt, keeping her voice down] Why did you tell them my dad wasn't in the picture?"),
    ("ETHAN", "[calm] Because you were uncomfortable."),
    ("OLIVIA", "I was about to answer.")],
   sfx=[["City street at night, distant traffic, light rain", 3.0, 0.3, "start"]], cut=True)
sc("street", ["ethan:suit"], "Ethan stepping close, cupping her face, voice soft.",
   [("ETHAN", "[soft, reasonable] Olivia, my mother is difficult. I'm trying to make things easier for you."),
    ("OLIVIA", "[sharp] By lying?"),
    ("ETHAN", "[evenly] By protecting our future.")])
sc("street", ["olivia:dinner"], "Olivia pulling back from his hands, eyes wet.",
   [("OLIVIA", "[quiet, firm] My father raised me."),
    ("ETHAN", "[smiling] And I'm sure he's a wonderful man. [pause] But do you really want my parents judging you before they even know you?")])
sc("street", ["ethan:suit", "olivia:dinner"], "Ethan opening the door of a black car for her.",
   [("OLIVIA", "[small] I don't want to hide him."),
    ("ETHAN", "[gently] Then don't. [pause] Just let me handle my family.")],
   sfx=[["Heavy car door closing", 1.0, 0.45, "end"]])

# SCENE 4 - THE FIRST WARNING
sc("garage", ["thomas"], "Thomas under a car on a creeper, only his boots visible, a pair of polished heels stepping into the garage.",
   [("THOMAS", "[from under the car] We're closed!"),
    ("SARAH", "[amused] Even for an old friend?")],
   sfx=[["Garage door rattling, footsteps in heels on concrete", 3.0, 0.35, "start"]], music="tension", cut=True)
sc("garage", ["sarah"], "Sarah Mitchell standing in the garage bay in a sharp navy suit, briefcase in hand, smiling.",
   [("THOMAS", "[rolling out, squinting] Sarah Mitchell? [laughs] Well, I'll be damned."),
    ("SARAH", "[warm] Good to see you, Thomas.")])
sc("garage", ["thomas"], "Thomas getting up, wiping his hands, curious.",
   [("THOMAS", "[teasing] What brings a fancy lawyer to my garage?"),
    ("SARAH", "[serious now] The Blackwoods.")],
   sfx=[["A wrench set down on a metal tray, then silence", 1.5, 0.4, "end"]])
sc("garage", ["sarah", "thomas"], "Sarah and Thomas facing each other beside a workbench.",
   [("THOMAS", "[guarded] What about them?"),
    ("SARAH", "Your daughter's engaged to Ethan Blackwood."),
    ("THOMAS", "You know him?"),
    ("SARAH", "[carefully] I know his father.")])
sc("garage", [], "Close-up of an old yellowed court file in Sarah's hands labeled with a fifteen-year-old date.",
   [("SARAH", "[measured] Do you remember the commercial property dispute fifteen years ago?"),
    ("THOMAS", "[bitter] The one that nearly cost me my garage?"),
    ("SARAH", "Yes.")])
sc("garage", ["thomas"], "Thomas closing his eyes, shaking his head slowly.",
   [("THOMAS", "[groaning] Don't tell me."),
    ("SARAH", "[quiet] James Blackwood's investment company was behind it."),
    ("THOMAS", "[shrugging it off] That was a long time ago.")])
sc("garage", ["sarah"], "Sarah holding up her phone showing an engagement announcement.",
   [("SARAH", "[gently] I know. But I saw your daughter's engagement announcement. And I thought you should know.")])
sc("garage", ["thomas"], "Thomas looking at the photo of Olivia pinned on the wall.",
   [("THOMAS", "[firm, protective] Olivia has nothing to do with that old fight."),
    ("SARAH", "[soft] I hope you're right."),
    ("THOMAS", "[sighs] Sarah, I appreciate the warning. But my daughter loves this man. I'm not going to ruin that over something that happened fifteen years ago.")])
sc("garage", ["sarah"], "Sarah handing Thomas a business card at the garage door.",
   [("SARAH", "[serious] Then promise me one thing."),
    ("THOMAS", "What?"),
    ("SARAH", "[holding his gaze] If anything feels wrong... call me.")],
   motion="she presses a business card into his hand and walks out into the daylight")

# SCENE 5 - A CONVENIENT DEATH
sc("mansion", ["catherine:home", "olivia:casual"], "Catherine at a table covered with wedding programs and seating charts, Olivia beside her, a grand piano behind.",
   [("CATHERINE", "[brisk, cheerful] Olivia, we need to finalize the wedding program."),
    ("OLIVIA", "[polite] Of course.")],
   sfx=[["Large quiet mansion room, someone playing soft piano in the next room", 4.0, 0.25, "start"]], music="tension", cut=True)
sc("mansion", ["catherine:home"], "Catherine running a manicured finger down a printed schedule.",
   [("CATHERINE", "[light] And the father-daughter dance?"),
    ("OLIVIA", "[hesitant] I haven't decided."),
    ("CATHERINE", "[casually] Ethan mentioned your father wasn't around.")])
sc("mansion", ["olivia:casual"], "Olivia setting down a seating chart, uneasy.",
   [("OLIVIA", "[uneasy] That's... complicated."),
    ("CATHERINE", "[patting her hand] Darling, you don't need to explain. Some people have unfortunate family circumstances.")])
sc("mansion", ["olivia:casual", "catherine:home"], "Olivia pulling her hand away; Catherine smiling serenely.",
   [("OLIVIA", "[firm] My father is a good man."),
    ("CATHERINE", "[gently] I'm sure he was.")],
   sfx=[["Piano stops mid-phrase, silence", 2.0, 0.3, "start"]])
sc("mansion", ["olivia:casual"], "Close-up of Olivia freezing, staring at Catherine.",
   [("OLIVIA", "[slowly] ...Was?"),
    ("CATHERINE", "[surprised] Ethan told me he passed away.")])
sc("mansion", ["olivia:casual"], "Olivia going pale, gripping the edge of the table.",
   [("OLIVIA", "[stunned] He told you what?"),
    ("CATHERINE", "[soothing] Oh, dear. I hope I haven't upset you."),
    ("OLIVIA", "[faint] No. I just...")])
sc("mansion", ["catherine:home"], "Catherine holding up a cream-colored wedding program proudly.",
   [("CATHERINE", "[delighted] We'll include a small tribute in the program. [reading softly] In loving memory of Thomas Reed. [pause] Wouldn't that be beautiful?")])
sc("mansion", [], "Close-up of an elegant printed wedding program page: 'In Loving Memory of Thomas Reed, Beloved Father of the Bride'.",
   [(N, "[low] Olivia stared at the page. Her father's name. And beneath it: Beloved father of the bride. Forever in our hearts.")])
sc("mansion", ["olivia:casual"], "Olivia standing up abruptly, the program crumpling in her fist.",
   [("OLIVIA", "[barely controlled] I need to speak with Ethan.")],
   sfx=[["Chair scraping back on hardwood", 1.0, 0.4, "start"]], motion="she stands abruptly, the program crumpling in her hand")

# SCENE 6 - THE PRICE OF SAYING NO
sc("apartment", ["olivia:casual"], "Olivia storming into the dark apartment, slamming the crumpled program on the kitchen island.",
   [("OLIVIA", "[furious, shaking] You told your mother my father was dead?")],
   sfx=[["Apartment door slamming, keys thrown on a counter", 2.0, 0.45, "start"]], music="tension", cut=True)
sc("apartment", ["ethan:suit"], "Ethan by the window loosening his tie, not even turning around.",
   [("ETHAN", "[calm, cold] Lower your voice."),
    ("OLIVIA", "[shouting] Answer me!"),
    ("ETHAN", "[evenly] I told her you lost your father.")])
sc("apartment", ["olivia:casual"], "Olivia in the middle of the room, tears of anger in her eyes.",
   [("OLIVIA", "[incredulous] He's alive!"),
    ("ETHAN", "[flat] I know that."),
    ("OLIVIA", "[breaking] Then why?")])
sc("apartment", ["ethan:suit"], "Ethan turning from the window, his face expressionless, city lights behind him.",
   [("ETHAN", "[quiet, matter-of-fact] Because your father is a problem.")],
   sfx=[["Low tense musical sting", 2.0, 0.35, "end"]])
sc("apartment", ["olivia:casual", "ethan:suit"], "Olivia stepping back as if struck; Ethan pouring himself a drink.",
   [("OLIVIA", "[stunned] What did you just say?"),
    ("ETHAN", "[pouring a drink] My father knows who Thomas Reed is. There was a legal dispute years ago."),
    ("OLIVIA", "That had nothing to do with me.")])
sc("apartment", ["ethan:suit"], "Ethan swirling his glass, eyes hard.",
   [("ETHAN", "[sharp] It has everything to do with us."),
    ("OLIVIA", "[pleading] Then tell your parents the truth."),
    ("ETHAN", "[scoffs] And destroy the wedding?")])
sc("apartment", ["olivia:casual"], "Olivia pulling the engagement ring halfway off her finger.",
   [("OLIVIA", "[shaking, determined] I'd rather cancel it than pretend my dad is dead."),
    ("ETHAN", "[very quiet] Be careful.")])
sc("apartment", ["ethan:suit"], "Ethan setting down his glass, calm and menacing.",
   [("OLIVIA", "[disbelieving] Is that a threat?"),
    ("ETHAN", "[smiling, cold] It's advice.")],
   sfx=[["A phone set down hard on a glass table", 1.0, 0.45, "end"]])
sc("apartment", [], "Close-up of Ethan's phone on the glass table showing a loan document with signatures.",
   [("ETHAN", "[casually] Remember the loan you co-signed for our new business?"),
    ("OLIVIA", "[wary] What about it?"),
    ("ETHAN", "Your father guaranteed part of it.")])
sc("apartment", ["olivia:casual"], "Olivia staring at the phone, confused.",
   [("OLIVIA", "[confused] He guaranteed the equipment lease."),
    ("ETHAN", "[patiently, like explaining to a child] And if the business defaults... the lender goes after the guarantor.")])
sc("apartment", ["olivia:casual"], "Close-up of Olivia's face as the realization sinks in.",
   [("OLIVIA", "[faltering] You said the company was doing well."),
    ("ETHAN", "[lightly] It is. [pause] As long as nobody creates problems.")])
sc("apartment", ["ethan:suit", "olivia:casual"], "Ethan walking past Olivia, pausing beside her ear.",
   [("OLIVIA", "[whisper] You wouldn't deliberately let him lose his garage."),
    ("ETHAN", "[softly, at her ear] Then let's not find out.")],
   sfx=[["Silence, a distant siren far below", 2.0, 0.25, "start"]])
sc("apartment", ["olivia:casual"], "Olivia alone by the window, the ring back on her finger, city lights reflected in tears.",
   [(N, "[slow] Olivia had just learned the real price of her wedding. [pause] Her father's livelihood.")],
   motion="she slowly pushes the ring back onto her finger, tears reflecting the city lights")

# SCENE 7 - THE FATHER'S BIRTHDAY
sc("kitchen", ["thomas:home"], "Thomas at a small kitchen table with a small birthday cake, two plates set out, answering the phone hopefully.",
   [("THOMAS", "[hopeful] Hello?"),
    ("OLIVIA~phone", "[soft] Happy birthday, Dad.")],
   sfx=[["Phone ringing in a quiet kitchen, a clock ticking", 2.5, 0.35, "start"]], music="wonder", cut=True)
sc("kitchen", ["thomas:home"], "Thomas beaming, leaning back in his chair.",
   [("THOMAS", "[delighted] There she is! [laughs] I was beginning to think you forgot."),
    ("OLIVIA~phone", "[warm, sad] Never."),
    ("THOMAS", "[playful] Sixty-two years old. Still handsome. [chuckles] Still can't figure out the TV remote.")])
sc("apartment", ["olivia:night"], "Olivia sitting on a sofa in the dark, phone at her ear, holding back tears.",
   [("OLIVIA", "[voice catching] Dad..."),
    ("THOMAS~phone", "[instantly worried] What's wrong?"),
    ("OLIVIA", "[too fast] Nothing.")])
sc("kitchen", ["thomas:home"], "Thomas's smile fading, gently knowing.",
   [("THOMAS", "[gently] You never were a good liar."),
    ("OLIVIA~phone", "[sighs] I'm just tired."),
    ("THOMAS", "[coaxing] Come by this weekend. I'll make pancakes.")])
sc("apartment", ["olivia:night"], "Olivia pressing a hand over her mouth to keep from crying out loud.",
   [("OLIVIA", "[tight] I can't."),
    ("THOMAS~phone", "[hopeful] Next weekend?"),
    ("OLIVIA", "[barely] I don't know.")])
sc("kitchen", ["thomas:home"], "Close-up of Thomas staring at the second empty plate.",
   [("THOMAS", "[quiet, hurt] Olivia... [pause] did I do something?")],
   sfx=[["Silence, just a clock ticking", 2.0, 0.25, "start"]])
sc("apartment", ["olivia:night"], "Olivia crying silently, shaking her head.",
   [("OLIVIA", "[whispering, tearful] No, Dad."),
    ("THOMAS~phone", "[softly] Then why does it feel like I'm losing you?")])
sc("apartment", ["olivia:night"], "Olivia curled on a gray sofa, phone pressed to her cheek.",
   [("OLIVIA", "[breaking] I love you."),
    ("THOMAS~phone", "[tender] I love you too, pumpkin."),
    ("OLIVIA", "[a broken whisper] Please don't call me that.")])
sc("kitchen", ["thomas:home"], "Thomas nodding to himself, swallowing.",
   [("THOMAS", "[quietly] Right. [pause] Sorry.")],
   sfx=[["Call ending tone", 1.0, 0.4, "end"]])
sc("kitchen", ["thomas:home"], "Thomas alone at the table, one candle burning on a small cake, the second plate untouched.",
   [(N, "[slow, heavy] Thomas sat alone beside a birthday cake he'd bought for two. He waited another hour. [pause] Then he put the second plate away.")],
   motion="the single candle flickers as he slowly picks up the second plate")

# SCENE 8 - THE DISCOVERY
sc("garage", ["mia:casual"], "Mia standing hesitantly at the open garage door, holding a folded piece of paper.",
   [("MIA", "[uncertain] Mr. Reed?")],
   sfx=[["Garage, old radio playing quietly", 3.0, 0.25, "start"]], music="tension", cut=True)
sc("garage", ["thomas"], "Thomas looking up from a workbench, breaking into a big smile.",
   [("THOMAS", "[warm surprise] Mia? Well, look at you! [laughs] How's my daughter's favorite troublemaker?"),
    ("MIA", "[forced smile] I'm okay."),
    ("THOMAS", "[squinting] You don't look okay.")])
sc("garage", ["mia:casual"], "Mia twisting the folded paper in her hands.",
   [("MIA", "[careful] Have you talked to Olivia?"),
    ("THOMAS", "Not much lately."),
    ("MIA", "Did she tell you about the wedding?"),
    ("THOMAS", "[shrugs] They're still planning it.")])
sc("garage", ["mia:casual"], "Close-up of Mia, eyes full of pity.",
   [("MIA", "[gently] Mr. Reed... [pause] it's Saturday."),
    ("THOMAS", "[confused] What?"),
    ("MIA", "[quiet] The wedding is this Saturday.")],
   sfx=[["Radio clicked off, silence", 1.5, 0.3, "start"]])
sc("garage", ["thomas"], "Thomas setting his wrench down very slowly.",
   [("THOMAS", "[hollow] This Saturday?"),
    ("MIA", "[apologetic] I thought you knew."),
    ("THOMAS", "[barely] No.")])
sc("garage", ["mia:casual", "thomas"], "Mia unfolding the paper and holding it out to Thomas.",
   [("MIA", "[reluctant] There's something else. [pause] The wedding website... says you passed away."),
    ("THOMAS", "[disbelief] What did you say?"),
    ("MIA", "I brought a printout.")],
   sfx=[["Paper unfolding", 1.0, 0.45, "start"]])
sc("garage", [], "Close-up of a printed wedding website page held in a grease-stained hand: 'In Loving Memory of Thomas Reed'.",
   [("THOMAS", "[reading, barely a whisper] In loving memory... of Thomas Reed.")])
sc("garage", ["thomas"], "Thomas staring at the page, his hand trembling.",
   [("MIA", "[softly] I'm sorry."),
    ("THOMAS", "[cracking] My daughter told people I was dead?"),
    ("MIA", "[urgent] I don't think it's that simple.")])
sc("garage", ["mia:casual"], "Mia stepping closer, lowering her voice.",
   [("THOMAS", "[raw] Then explain it to me."),
    ("MIA", "[frustrated] I can't. [pause] But I think Ethan is hiding something."),
    ("THOMAS", "How do you know?")])
sc("garage", ["mia:casual"], "Close-up of Mia, serious and scared.",
   [("MIA", "[low] Because Olivia called me crying last night. [pause] And when I asked what was wrong... Ethan took her phone.")],
   sfx=[["Low ominous tone", 2.0, 0.35, "end"]])

# SCENE 9 - THE OLD CASE
sc("law_office", ["sarah"], "Sarah behind her desk in a downtown law office, files spread out, gesturing for Thomas to sit.",
   [("SARAH", "[relieved] Thomas. I'm glad you called."),
    ("THOMAS", "[grim] I need to know what happened fifteen years ago. [pause] All of it.")],
   sfx=[["Quiet office, city traffic far below, papers shuffling", 3.0, 0.3, "start"]], music="tension", cut=True)
sc("law_office", [], "Close-up of an old site plan map of a city block with a small lot circled in red.",
   [("SARAH", "[laying out a map] Your garage sat on land Blackwood Development wanted for a commercial project."),
    ("THOMAS", "I remember."),
    ("SARAH", "They tried to terminate your lease early. We fought it.")])
sc("law_office", ["thomas:home"], "Thomas sitting across the desk in a flannel shirt, arms crossed.",
   [("THOMAS", "[dry] And won."),
    ("SARAH", "We settled. Your lease was protected, with renewal rights."),
    ("THOMAS", "[frowning] Then why would they care about me now?")])
sc("law_office", ["sarah"], "Sarah sliding a new stack of filings across the desk.",
   [("SARAH", "[carefully] Because the Blackwoods are buying up the neighboring lots again."),
    ("THOMAS", "[slowly] They still want my garage?"),
    ("SARAH", "[nodding] Possibly. [pause] And there's something else.")])
sc("law_office", [], "Close-up of a public business filing with the name 'Ethan Blackwood' listed as managing member.",
   [("SARAH", "[pointing] The newest development company on that block? It belongs to Ethan."),
    ("THOMAS", "[stunned] His son?"),
    ("SARAH", "Yes.")])
sc("law_office", ["thomas:home"], "Close-up of Thomas, the pieces falling into place.",
   [("THOMAS", "[slowly, horrified] So he knew who I was... before he ever met Olivia?"),
    ("SARAH", "[cautious] We can't prove that yet."),
    ("THOMAS", "[quiet] But it's possible."),
    ("SARAH", "Yes.")])
sc("law_office", ["thomas:home"], "Thomas standing up, pulling on his jacket.",
   [("THOMAS", "[resolved] Then I need to talk to my daughter."),
    ("SARAH", "[warning] Thomas, don't confront them alone."),
    ("THOMAS", "I'm not going there to fight.")])
sc("law_office", ["thomas:home"], "Thomas at the office door, looking back at Sarah, eyes wet.",
   [("SARAH", "[softly] Then why are you going?"),
    ("THOMAS", "[voice thick] Because my little girl is getting married. [pause] And somebody convinced her that her father had to be dead for that to happen.")],
   sfx=[["Door closing softly", 1.0, 0.35, "end"]])

# SCENE 10 - THE NIGHT BEFORE
sc("hotel", ["olivia:night"], "The night before the wedding: Olivia throwing clothes into an open suitcase, the wedding dress hanging behind her.",
   [("OLIVIA", "[frantic whisper] Mia, I can't do this.")],
   sfx=[["Hotel room, suitcase zipper, hangers rattling", 3.0, 0.35, "start"]], music="tension", cut=True)
sc("hotel", ["mia:casual"], "Mia sitting on the edge of the bed , arms crossed.",
   [("MIA", "[instantly] Then don't."),
    ("OLIVIA", "[exhausted] It's not that easy."),
    ("MIA", "[incredulous] Olivia, your wedding program says your living father is dead. Nothing about this is normal.")])
sc("hotel", ["olivia:night"], "Olivia sinking onto the bed beside the suitcase.",
   [("OLIVIA", "[desperate] Ethan says if I leave, he'll let the business fail."),
    ("MIA", "Then call a lawyer."),
    ("OLIVIA", "[shaking her head] Dad guaranteed the equipment lease.")])
sc("hotel", ["mia:casual"], "Mia leaning in, grabbing Olivia's hands.",
   [("MIA", "[firm] A guarantee doesn't mean Ethan gets to control your life."),
    ("OLIVIA", "[tearful] What if Dad loses everything?"),
    ("MIA", "[quiet, fierce] What if you marry a man who's already threatening your family?")])
sc("hotel", [], "A hotel door opening; Ethan standing in the doorway in a dark suit.",
   [("ETHAN", "[smooth] Am I interrupting?"),
    ("MIA", "[flat] Actually, yes.")],
   sfx=[["Hotel key card beep, door opening", 1.5, 0.45, "start"]])
sc("hotel", ["ethan:suit"], "Ethan stepping into the suite, looking at the half-packed suitcase.",
   [("ETHAN", "[polite, cold] Mia, could you give us a minute?"),
    ("MIA", "No."),
    ("ETHAN", "[warning] Olivia?"),
    ("OLIVIA", "[quiet but firm] Mia stays.")])
sc("hotel", [], "Close-up of Mia's hand resting on her phone on the dresser; her thumb taps the screen, a small red dot glowing.",
   [(N, "[low, almost a whisper] Mia's phone was lying face-up on the dresser. [pause] Nobody noticed her thumb touch the screen.")],
   motion="her thumb lightly taps the phone screen and a small red dot begins to glow")
sc("hotel", ["ethan:suit"], "Ethan shrugging, standing over the suitcase.",
   [("ETHAN", "[sighs] Fine. [pause] I just came to remind you that tomorrow is the most important day of our lives."),
    ("OLIVIA", "[quiet, bitter] Then why does it feel like a funeral?")],
   sfx=[["Silence", 1.5, 0.2, "start"]])
sc("hotel", ["ethan:suit"], "Ethan's face hardening.",
   [("ETHAN", "[sharp] Don't start this again."),
    ("OLIVIA", "[steady] I want my father there."),
    ("ETHAN", "[through his teeth] We've discussed this.")])
sc("hotel", ["olivia:night"], "Olivia standing up to face him, trembling.",
   [("OLIVIA", "[shaking but firm] I'm done discussing it."),
    ("ETHAN", "[low, slow, every word deliberate] Then think carefully about what happens to his garage.")],
   sfx=[["Low tense musical sting", 2.0, 0.35, "end"]])
sc("hotel", ["mia:casual", "ethan:suit"], "Mia shooting up from the bed, pointing at Ethan.",
   [("MIA", "[furious] Did you seriously just threaten her father?"),
    ("ETHAN", "[icy] This is a private matter."),
    ("MIA", "[cold] Not anymore.")])

# SCENE 11 - THE CALL
sc("garage_night", ["thomas:home"], "Thomas alone in the garage at night under a single work lamp, a phone buzzing on the desk.",
   [("THOMAS", "[tired] Hello?"),
    ("MIA~phone", "[hushed, urgent] Mr. Reed? It's Mia.")],
   sfx=[["Phone vibrating on a wooden desk, quiet garage at night", 2.5, 0.4, "start"]], music="tension", cut=True)
sc("hotel", ["mia:casual"], "Mia in a dark hotel hallway, whispering into her phone, glancing at a closed door.",
   [("MIA", "[low, fast] I need you to listen carefully. Olivia's wedding is tomorrow at eleven. St. Andrew's Chapel."),
    ("THOMAS~phone", "[heavy] I know.")])
sc("hotel", ["mia:casual"], "Close-up of Mia, determined.",
   [("MIA", "[firm] You need to come."),
    ("THOMAS~phone", "[hurt] She doesn't want me there."),
    ("MIA", "[insistent] That's not true.")])
sc("garage_night", ["thomas:home"], "Thomas sitting under the work lamp, rubbing his eyes.",
   [("THOMAS", "[bitter, quiet] Then why did she tell everyone I was dead?"),
    ("MIA~phone", "[low] Because Ethan threatened her."),
    ("THOMAS", "[sharp] With what?"),
    ("MIA~phone", "[quiet] Your garage.")],
   sfx=[["Silence, a single dripping faucet", 2.0, 0.25, "end"]])
sc("garage_night", [], "No people in the frame. The empty old garage at night, the work lamp swaying slightly over the car on the lift.",
   [("THOMAS", "[slowly, dangerously calm] He threatened my daughter... with my garage?"),
    ("MIA~phone", "Yes.")],
   motion="the hanging work lamp sways gently, shadows moving over the car")
sc("garage_night", ["thomas:home"], "Close-up of Thomas, jaw clenched, eyes wet.",
   [("THOMAS", "[softly] Mia... does she know you're calling?"),
    ("MIA~phone", "No."),
    ("THOMAS", "[barely] Then tell me one thing. [pause] Is she safe?")])
sc("hotel", ["mia:casual"], "Mia leaning against the hallway wall, closing her eyes.",
   [("MIA", "[quiet] She's with me. [pause] But I don't think she'll be safe if she marries him."),
    ("THOMAS~phone", "[steady] I'll be there.")])
sc("garage_night", ["thomas:home"], "Thomas picking up Sarah's old business card from the desk and dialing.",
   [(N, "[low] When the call ended, Thomas didn't go to bed. He pulled an old business card from the corner of his desk."),
    ("THOMAS", "[quiet, resolved] Sarah. You said if anything felt wrong, call you. [pause] Can you be at St. Andrew's Chapel tomorrow at eleven?")],
   sfx=[["Phone dial tones", 1.5, 0.35, "start"]])

# SCENE 12 - THE CHURCH DOORS (back to the cold open)
sc("chapel", ["thomas:wedding", "ethan"], "Back in the chapel: Thomas stopped in the aisle; Ethan still gripping Olivia's wrist at the altar.",
   [(N, "[low] Which brings us back to the chapel."),
    ("THOMAS", "[very quiet] I said, take your hand off my daughter."),
    ("ETHAN", "[shouting toward the back] Security!")],
   sfx=[["Large crowd murmuring nervously in a stone chapel", 4.0, 0.35, "start"]], music="tension", cut=True)
sc("chapel", ["thomas:wedding"], "Thomas raising his empty hands, calm, guests whispering around him.",
   [("THOMAS", "[calm, loud enough for everyone] I'm not here to hurt anyone."),
    ("CATHERINE", "[shrill] This is outrageous!")])
sc("chapel", ["james"], "James standing up in the front pew, staring hard at Thomas.",
   [("JAMES", "[cold, low] You're supposed to be dead."),
    ("THOMAS", "[evenly] Why? [pause] Because your family told everyone I was?")])
sc("chapel", ["olivia"], "Olivia at the altar, tears running, unable to look at her father.",
   [("OLIVIA", "[crying] Dad, please..."),
    ("THOMAS", "[gently] Sweetheart, look at me."),
    ("OLIVIA", "[shaking her head] I can't.")])
sc("chapel", ["thomas:wedding"], "Thomas reaching the front of the aisle, looking up at Olivia, voice soft.",
   [("THOMAS", "[softly] Did you tell them I died?")],
   sfx=[["Total silence in a large stone chapel", 2.5, 0.2, "start"]])
sc("chapel", ["olivia"], "Close-up of Olivia, mascara streaked, nodding.",
   [("OLIVIA", "[a broken whisper] Yes."),
    ("THOMAS", "[barely] Why?")])
sc("chapel", ["ethan", "thomas:wedding"], "Ethan in his tuxedo stepping between the bride and Thomas, the two men glaring at each other.",
   [("ETHAN", "[sharp] That's enough."),
    ("THOMAS", "[without looking at him] I wasn't talking to you."),
    ("ETHAN", "[hissing] You're ruining our wedding.")])
sc("chapel", ["thomas:wedding", "ethan"], "Thomas and Ethan face to face at the altar steps.",
   [("THOMAS", "[low, steady] Then tell everyone why you threatened my daughter."),
    ("ETHAN", "[smiling for the crowd] I have no idea what you're talking about.")])
sc("chapel", ["mia"], "Mia in her bridesmaid dress stepping out of the line of bridesmaids, holding her phone.",
   [("MIA", "[loud, clear] I do.")],
   sfx=[["Guests whispering, gasps", 2.0, 0.35, "start"]])

# SCENE 13 - THE BRIDE SPEAKS
sc("chapel", ["ethan"], "Ethan glaring at Mia, pointing at her.",
   [("ETHAN", "[warning] Mia. Sit down."),
    ("MIA", "No."),
    ("OLIVIA", "[pleading] Mia...")])
sc("chapel", ["mia"], "Mia looking at Olivia, eyes kind but unyielding.",
   [("MIA", "[gentle, firm] Tell them, Olivia."),
    ("ETHAN", "[low] Don't.")])
sc("chapel", ["thomas:wedding", "olivia"], "Thomas taking Olivia's trembling hand at the altar steps.",
   [("THOMAS", "[tender] Honey, whatever it is, you can tell me."),
    ("OLIVIA", "[sobbing] Dad, I'm so sorry."),
    ("THOMAS", "For what?")])
sc("chapel", ["olivia"], "Olivia turning to face the guests, veil trembling.",
   [("OLIVIA", "[shaky, then stronger] I told them you were dead because Ethan said his family would never accept me.")])
sc("chapel", ["catherine"], "Catherine in the front pew, rising halfway, staring at her son.",
   [("CATHERINE", "[stunned] Ethan... what is she saying?")])
sc("chapel", ["olivia"], "Olivia looking straight at Ethan now, tears falling.",
   [("OLIVIA", "[gaining strength] And when I wanted to tell the truth, he said he'd let the business default."),
    ("ETHAN", "[sharp] Olivia!"),
    ("OLIVIA", "[to Thomas, breaking] He said the lender would come after your garage.")])
sc("chapel", ["thomas:wedding"], "Close-up of Thomas, absorbing it.",
   [("THOMAS", "[quiet] My garage?"),
    ("OLIVIA", "[crying] I thought I was protecting you."),
    ("THOMAS", "[heartbroken] Oh, sweetheart.")])
sc("chapel", ["thomas:wedding", "olivia"], "Thomas cupping Olivia's face in his rough hands.",
   [("OLIVIA", "[whisper] I know it was wrong."),
    ("THOMAS", "[gentle, honest] Yes. It was. [pause] But you should never have had to face that alone.")])
sc("chapel", ["ethan"], "Ethan laughing nervously, spreading his hands to the guests.",
   [("ETHAN", "[scoffing] This is absurd."),
    ("THOMAS", "[turning, hard] Did you threaten her?"),
    ("ETHAN", "[smooth] I explained the financial consequences of her decisions.")])
sc("chapel", ["mia", "ethan"], "Mia stepping forward, Ethan smirking at her.",
   [("MIA", "[fierce] You told her you'd destroy her father's livelihood."),
    ("ETHAN", "[smirking] You can't prove that."),
    ("MIA", "[holding up her phone, a slow smile] Actually... [pause] I can.")],
   sfx=[["Deep dramatic musical hit", 2.0, 0.45, "end"]])

# SCENE 14 - THE RECORDING
sc("chapel", ["mia"], "Mia handing her phone to a sound technician beside the chapel speakers.",
   [("MIA", "[calm] I recorded our conversation last night. [pause] I was in the room.")],
   sfx=[["Microphone feedback squeal, then speaker hum", 2.0, 0.4, "start"]], music="tension", cut=True)
sc("chapel", [], "Close-up of a chapel speaker on a stand, the guests' heads turning toward it.",
   [("ETHAN~phone", "[recorded, low, deliberate] Then think carefully about what happens to his garage."),
    ("MIA~phone", "[recorded, furious] Did you seriously just threaten her father?"),
    ("ETHAN~phone", "[recorded, icy] This is a private matter.")])
sc("chapel", [], "Wide shot of the silent chapel, two hundred guests frozen, all eyes on the groom.",
   [(N, "[slow] The recording ended. [pause] And the chapel went completely silent.")],
   sfx=[["Recording clicking off, then dead silence in a large room", 2.5, 0.3, "start"]])
sc("chapel", ["james"], "James slowly turning to his son, face like stone.",
   [("JAMES", "[low, dangerous] Ethan?"),
    ("ETHAN", "[quickly] Dad, it's out of context.")])
sc("chapel", ["catherine"], "Catherine glancing around at the staring guests, clutching her pearls.",
   [("CATHERINE", "[shrill, desperate] This is a private family matter!"),
    ("THOMAS", "[firm] No. [pause] This is my daughter's life.")])
sc("chapel", ["ethan", "olivia"], "Ethan grabbing Olivia's hand, smiling too wide.",
   [("ETHAN", "[urgent, smiling for the crowd] Olivia. Tell them we're fine."),
    ("OLIVIA", "[pulling her hand back] We're not fine.")])
sc("chapel", ["ethan"], "Ethan's smile collapsing into anger.",
   [("ETHAN", "[hissing] You're embarrassing yourself."),
    ("OLIVIA", "[steady] No. [pause] For the first time in months, I'm telling the truth.")])
sc("chapel", ["ethan", "thomas:wedding", "olivia"], "Ethan leaning toward Olivia; Thomas stepping between them.",
   [("ETHAN", "[low, venomous] You'll regret this."),
    ("THOMAS", "[iron] Don't threaten her again.")])
sc("chapel", ["james", "thomas:wedding"], "James and Thomas facing each other across the altar steps, two old men measuring each other.",
   [("JAMES", "[cold recognition] Thomas Reed."),
    ("THOMAS", "[evenly] James Blackwood."),
    ("JAMES", "I remember you."),
    ("THOMAS", "[dry] I remember you too.")])
sc("chapel", ["james"], "James glancing at the guests, lowering his voice.",
   [("JAMES", "[tight] This isn't the place to settle old business."),
    ("THOMAS", "[quiet, cutting] Then why did your son make my daughter's wedding part of it?")],
   sfx=[["Low tense musical sting", 2.0, 0.35, "end"]])

# SCENE 15 - THE REAL REASON
sc("chapel", ["james"], "James turning on Ethan.",
   [("JAMES", "[sharp] Ethan. What is he talking about?"),
    ("ETHAN", "[too fast] Nothing.")],
   music="tension")
sc("chapel", ["thomas:wedding"], "Thomas addressing James directly, the guests listening.",
   [("THOMAS", "[measured] Fifteen years ago, your company tried to force me out of my garage."),
    ("JAMES", "That dispute was settled."),
    ("THOMAS", "It was. [pause] But now your son has a development company buying up the same block.")])
sc("chapel", ["ethan"], "Ethan shrugging, defiant.",
   [("ETHAN", "[defensive] That's business."),
    ("THOMAS", "And the loan on Olivia's business? The one I guaranteed? It's tied to my garage.")])
sc("chapel", ["ethan", "olivia"], "Olivia turning on Ethan in shock.",
   [("ETHAN", "[cold] She agreed to the terms."),
    ("OLIVIA", "[stunned, rising] You told me it was just an equipment lease!"),
    ("ETHAN", "[contemptuous] You should've read the documents.")])
sc("chapel", ["thomas:wedding"], "Close-up of Thomas laying it out, voice controlled.",
   [("THOMAS", "[slowly, connecting it] So that was the plan. [pause] Get close to my daughter. Get me to sign a guarantee. [pause] Then use the debt to force me off my land.")])
sc("chapel", ["ethan"], "Ethan straightening his tuxedo, regaining his composure.",
   [("ETHAN", "[smooth] You're making accusations you can't prove."),
    ("SARAH", "[calm, carrying from the back] Then perhaps we should discuss the documents.")],
   sfx=[["Heels clicking down a stone aisle", 2.5, 0.45, "start"]])
sc("chapel", ["sarah"], "Sarah walking down the aisle in a navy suit, a thick folder under her arm, guests parting.",
   [("JAMES", "[irritated] And who are you?"),
    ("SARAH", "[crisp] Sarah Mitchell. [pause] Mr. Reed's attorney.")],
   motion="she walks steadily down the aisle with a thick folder as guests turn to watch")
sc("chapel", ["sarah"], "Sarah at the front, opening the folder.",
   [("SARAH", "[professional] We've reviewed the guarantee, the lender's notices, and the development filings. [pause] The way this loan was presented to Olivia and Thomas raises serious questions."),
    ("ETHAN", "[scoffing] This is ridiculous."),
    ("SARAH", "[cool] Then you'll have no problem answering them through counsel.")])
sc("chapel", ["thomas:wedding"], "Thomas looking Ethan straight in the eye.",
   [("THOMAS", "[quiet] Ethan. Did you know who I was... when you first met my daughter?")],
   sfx=[["Total silence, a single heartbeat-like low thump", 2.5, 0.3, "start"]])
sc("chapel", ["ethan"], "Close-up of Ethan, cornered, jaw working.",
   [("ETHAN", "[through clenched teeth] ...Yes."),
    ("OLIVIA", "[a breath] What?"),
    ("ETHAN", "[louder] I knew.")])
sc("chapel", ["olivia"], "Olivia staring at Ethan, the realization hitting her.",
   [("OLIVIA", "[shaking] Before our first date?"),
    ("ETHAN", "Yes."),
    ("OLIVIA", "[horrified] You knew who my father was?"),
    ("ETHAN", "[exploding] Yes!")])
sc("chapel", ["ethan", "olivia"], "Ethan and Olivia face to face at the altar, her veil trembling.",
   [("OLIVIA", "[barely] Then why didn't you tell me?"),
    ("ETHAN", "[frustrated] Because you would've thought it was about the property!"),
    ("OLIVIA", "[quiet, devastating] ...Wasn't it?")],
   sfx=[["Silence", 2.0, 0.2, "end"]])
sc("chapel", ["james"], "James staring at his son with cold disgust.",
   [("JAMES", "[very quiet] You used my name for this?"),
    ("ETHAN", "[desperate] Dad, I did it for the company. For you!"),
    ("JAMES", "[ice] My company settled with this man fifteen years ago. In writing.")])
sc("chapel", ["james", "thomas:wedding"], "James turning to Thomas and giving a stiff, formal nod.",
   [("JAMES", "[formal, measured] Mr. Reed. Whatever my son signed, Blackwood Development had no part of it. [pause] [turning to Ethan] And as of Monday, you don't work for me.")],
   sfx=[["Crowd gasping", 1.5, 0.35, "end"]])
sc("chapel", ["catherine"], "Catherine sinking back into the pew, staring at her son in disbelief.",
   [("CATHERINE", "[hollow] You told me he was dead, Ethan. [pause] You let me print his name in a memorial.")])

# SCENE 16 - THE WOMAN WHO CHOSE HERSELF
sc("chapel", ["ethan"], "Ethan turning to Olivia, softening his face, reaching for her.",
   [("ETHAN", "[pleading, soft] Olivia. I love you."),
    ("OLIVIA", "[quiet] You lied to me."),
    ("ETHAN", "[quick] I made mistakes.")],
   music="wonder")
sc("chapel", ["olivia"], "Olivia stepping back from him, voice steadying.",
   [("OLIVIA", "You threatened my father."),
    ("ETHAN", "[defensive] I was under pressure."),
    ("OLIVIA", "You knew who he was before you met me.")])
sc("chapel", ["ethan"], "Ethan's earnest face, reaching for her hand.",
   [("ETHAN", "[earnest] I fell in love with you anyway."),
    ("OLIVIA", "[a bitter half laugh] ...Anyway?"),
    ("ETHAN", "[backpedaling] That's not what I meant.")])
sc("chapel", ["olivia"], "Close-up of Olivia, tears drying, chin lifting.",
   [("OLIVIA", "[steady, quiet] You made me believe that loving you meant pretending my father was dead."),
    ("ETHAN", "[desperate] Olivia, please.")])
sc("chapel", ["olivia"], "Olivia at the altar, back straight, facing Ethan and two hundred guests.",
   [("OLIVIA", "[clear, final] I can't marry you.")],
   sfx=[["A crowd gasping in a chapel", 2.0, 0.45, "start"]])
sc("chapel", ["catherine"], "Catherine half rising from the pew, hand on her chest.",
   [("CATHERINE", "[desperate] Think about the scandal!"),
    ("OLIVIA", "[calm] For once, Catherine... I don't care what people think.")])
sc("chapel", ["ethan"], "Ethan red-faced, shouting.",
   [("ETHAN", "[furious] You can't do this to me!"),
    ("OLIVIA", "[quiet] I didn't do this to you. [pause] You did.")])
sc("chapel", [], "Close-up of a diamond engagement ring being set down on the white altar cloth.",
   [(N, "[soft] She slid the ring off her finger and set it on the altar.")],
   sfx=[["A ring set down on a wooden altar, a tiny click", 1.0, 0.5, "start"]], motion="a hand gently sets the diamond ring down on the altar cloth")
sc("chapel", ["olivia", "thomas:wedding"], "Olivia turning to her father, a small trembling smile.",
   [("OLIVIA", "[small, hopeful] Dad?"),
    ("THOMAS", "[tender] Yes, sweetheart?"),
    ("OLIVIA", "[softly] Would you walk me out?")])
sc("chapel", ["thomas:wedding"], "Close-up of Thomas, tears in his eyes, offering his arm.",
   [("THOMAS", "[voice thick] I'd be honored.")])
sc("chapel", ["olivia", "thomas:wedding"], "From behind: Olivia in her wedding dress on Thomas's arm, walking up the aisle toward the open doors and the bright daylight.",
   [(N, "[warm] She had walked into that chapel alone. [pause] She walked out on her father's arm.")],
   sfx=[["Footsteps on stone, heavy chapel doors opening, birds outside", 4.0, 0.4, "start"]], motion="they walk slowly up the aisle toward the bright open doors")

# SCENE 17 - THREE MONTHS LATER
sc("law_office", ["sarah"], "Three months later: Sarah at her desk, reading glasses on, a file open.",
   [(N, "Three months later, Thomas and Olivia sat in Sarah Mitchell's office."),
    ("OLIVIA", "[nervous] So what happens to the loan?")],
   sfx=[["Quiet office, papers turning, winter wind outside", 3.0, 0.3, "start"]], music="wonder", cut=True)
sc("law_office", ["sarah"], "Sarah sliding a letter across the desk.",
   [("SARAH", "[reassuring] The lender has frozen collection while they review how the guarantee was obtained."),
    ("THOMAS", "And the garage?"),
    ("SARAH", "[smiling] Still yours. Nobody touches it while I'm on this.")])
sc("law_office", ["olivia:casual", "thomas:home"], "Olivia and Thomas sitting side by side across the desk.",
   [("OLIVIA", "[guarded] And Ethan?"),
    ("SARAH", "[dry] His development company is under investigation. There are civil claims pending. [pause] And his father's lawyers aren't returning his calls.")])
sc("law_office", ["thomas:home"], "Thomas nodding slowly, a grim little smile.",
   [("THOMAS", "So he's not walking away from this."),
    ("SARAH", "[calm] He's going to have to answer some very difficult questions."),
    ("OLIVIA", "[quiet] Good.")])
sc("law_office", ["thomas:home", "olivia:casual"], "Thomas turning to Olivia, serious and gentle.",
   [("THOMAS", "[gently] Olivia... you know I would've sold that garage if it meant keeping you safe."),
    ("OLIVIA", "[shaking her head] Dad, no."),
    ("THOMAS", "[shrugs] It's just a building.")])
sc("law_office", ["olivia:casual"], "Olivia looking at her father, eyes filling.",
   [("OLIVIA", "[tearful] It's your whole life."),
    ("THOMAS", "[softly] No. [pause] You're my whole life.")],
   sfx=[["Quiet gentle piano", 4.0, 0.25, "start"]])
sc("law_office", ["olivia:casual", "thomas:home"], "Olivia crying quietly, reaching for the hand of her father Thomas in his flannel shirt.",
   [("OLIVIA", "[breaking] I'm so sorry I let him make me ashamed of you."),
    ("THOMAS", "[tender] I know."),
    ("OLIVIA", "[whisper] Can you forgive me?")])
sc("law_office", ["thomas:home", "olivia:casual"], "Thomas in his flannel shirt squeezing Olivia's hand across the desk, smiling through tears.",
   [("THOMAS", "[warm] I already have. [pause] But next time you're scared, come to me. [a teary chuckle] Don't bury me while I'm still alive."),
    ("OLIVIA", "[laughing through tears] Deal.")],
   sfx=[["Two people laughing softly through tears", 2.0, 0.3, "end"]])

# SCENE 18 - ONE YEAR LATER
sc("backyard", ["thomas:yard"], "One year later: Thomas at a charcoal grill in a small backyard, flipping burgers, string lights overhead.",
   [(N, "[warm] One year after the wedding that never happened, Thomas stood in his backyard in an old blue shirt, grilling burgers.")],
   sfx=[["Backyard on a summer afternoon, birds singing, burgers sizzling on a grill", 4.0, 0.3, "start"]], music="wonder", cut=True,
   motion="he flips a burger on the grill as smoke drifts up")
sc("backyard", ["olivia:yard"], "Olivia laying a checkered cloth and plates on a picnic table, smiling.",
   [(N, "Olivia was setting the table. [pause] And Mia showed up carrying a cake.")])
sc("backyard", ["mia:casual"], "Mia coming through the backyard gate holding a birthday cake, grinning.",
   [("MIA", "[cheerful, sing-song] Happy birthday, Mr. Reed!"),
    ("THOMAS", "[proud] Sixty-three. Still handsome. [chuckles] Still can't work the TV remote.")],
   sfx=[["Wooden gate creaking open", 1.0, 0.35, "start"]])
sc("backyard", ["olivia:yard"], "Olivia rolling her eyes affectionately.",
   [("OLIVIA", "[teasing] Some things never change."),
    ("MIA", "[holding up the cake] I brought cake."),
    ("THOMAS", "[delighted] You are officially my favorite person.")])
sc("backyard", ["olivia:yard", "thomas:yard"], "Olivia hands on hips, mock offended; Thomas laughing.",
   [("OLIVIA", "[mock offended] Excuse me?"),
    ("THOMAS", "[laughing] Relax. You're still the undefeated champion, pumpkin.")])
sc("backyard", ["olivia:yard"], "Close-up of Olivia smiling softly at her father.",
   [("OLIVIA", "[soft] You can call me that, you know."),
    ("THOMAS", "[surprised, touched] Really?"),
    ("OLIVIA", "[warm] Really.")],
   sfx=[["Gentle laughter", 2.0, 0.3, "end"]])
sc("", ["ethan:suit"], "Ethan alone in an emptied office with moving boxes, a 'For Lease' sign in the window, gray day.",
   [(N, "[measured] Ethan's development company collapsed within the year. His investors pulled out. His father never took his calls again.")],
   sfx=[["Empty office echo, tape ripping off a box", 3.0, 0.3, "start"]])
sc("", ["catherine:home"], "Catherine alone at a long empty dining table set for a party nobody came to.",
   [(N, "Catherine Blackwood stopped hosting dinners. [pause] People had started asking her about the memorial program.")])
sc("garage", ["thomas"], "Thomas's small garage on a sunny day, a hand-painted sign above the bay: 'Reed Auto Repair'.",
   [(N, "But Thomas still had his garage. Olivia rebuilt her career. [pause] And for the first time in years, father and daughter talked every single day.")])
sc("backyard", ["olivia:yard", "thomas:yard"], "Olivia and Thomas sitting side by side at the picnic table at sunset.",
   [("OLIVIA", "[thoughtful] Dad?"),
    ("THOMAS", "Yeah?"),
    ("OLIVIA", "[quiet] Do you ever wish you'd stayed home that day? [pause] At the wedding?")])
sc("backyard", ["thomas:yard"], "Thomas looking out at the sunset, smiling gently.",
   [("THOMAS", "[without hesitation] Not for a second."),
    ("OLIVIA", "Even after everything?"),
    ("THOMAS", "[softly] Sweetheart...")])
sc("backyard", ["thomas:yard"], "Close-up of Thomas, warm golden light on his face.",
   [("THOMAS", "[slow, wise] You can lose money. You can lose a business. You can even lose people you thought would love you forever. [pause] But when someone you love needs you... [pause] you show up.")])
sc("backyard", ["olivia:yard", "thomas:yard"], "Olivia leaning her head on her father's shoulder, both laughing.",
   [("OLIVIA", "[teasing, teary] Even when they tell everyone you're dead?"),
    ("THOMAS", "[laughing] Especially then.")],
   sfx=[["Father and daughter laughing, birds at sunset", 2.5, 0.3, "start"]], motion="she leans her head on his shoulder and they both laugh")
sc("backyard", [], "No people in the frame. The empty small backyard at dusk, string lights glowing, a half-eaten birthday cake on the table.",
   [(N, "[reflective] Ethan Blackwood thought he could erase a father from his daughter's life. He thought money could buy her silence. And he thought a wedding would make his lies permanent. [pause] But he forgot one thing. [pause] The man he tried to bury was still alive.")],
   motion="the string lights glow and sway gently in the evening breeze")
sc("backyard", ["thomas:yard"], "Thomas at the picnic table at dusk, smiling, string lights behind him.",
   [(N, "[slow, final] Sometimes the strongest revenge isn't destroying someone. [pause] It's refusing to disappear when they want you gone."),
    (N, "[warm] This has been Karma Tales. Every betrayal has a price. And karma always collects.")])


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
    title = "My Daughter Told Everyone I Was Dead. Then I Showed Up at Her Wedding."
    spec = {
        "title": "Karma Tales EP05 - The Father They Buried",
        "voices": {r: VOICES[r] for r in sorted(roles)},
        "cast": CAST,
        "portraits": {k: PORTRAIT + v for k, v in PORTRAITS.items()},
        "looks": LOOKS,
        "style": "Photorealistic still from a prestige American TV drama, shot on 35mm, cinematic lighting, shallow depth of field, natural skin texture, muted warm color palette, wide 16:9 frame. Keep every person's face and hair exactly consistent with their reference photo. No text, no captions, no watermark. ",
        "resolution": "2K",
        "music": music,
        "places": PLACES,
        "ambiences": {
            "chapel": ["Large stone chapel full of people, soft rustling and murmurs, faint echo", 0.06],
            "garage": ["Small auto repair garage, distant street traffic, an old radio very faint", 0.06],
            "garage_night": ["Empty garage at night, buzzing work lamp, crickets outside", 0.06],
            "restaurant": ["Upscale restaurant, quiet conversations, soft piano far away", 0.06],
            "street": ["City street at night, light rain, distant traffic", 0.07],
            "house": ["Large quiet mansion room tone, faint clock", 0.05],
            "apartment": ["High-rise apartment at night, quiet city hum far below", 0.05],
            "kitchen": ["Small quiet kitchen, refrigerator hum, wall clock ticking", 0.05],
            "office": ["Quiet downtown office, muffled city traffic", 0.05],
            "hotel": ["Quiet hotel room, air conditioning hum", 0.05],
            "yard": ["Backyard summer afternoon, birds, distant neighborhood kids", 0.07],
        },
        "ambience": [],
        "scenes": scenes,
        "youtube": {
            "title": title,
            "description": "Halfway through the ceremony, the chapel doors opened. The bride's father walked in. The man whose name was printed in her wedding program, under the words \"In loving memory.\"\n\nWhy did Olivia tell everyone her father was dead? And why did the groom's mother whisper, \"That's impossible\"?\n\nKarma Tales: revenge and twist stories where the people who scheme always get what they deserve.\n\nThis story is fiction. Any resemblance to real people or events is coincidental. Narration and images are AI-generated.\n\n#karmatales #revengestory #weddingdrama #fatheranddaughter",
            "tags": ["karma tales", "revenge story", "wedding drama", "father and daughter", "family betrayal", "wedding objection", "twist ending", "karma", "audio drama", "dead father"],
            "category": "24",
            "shorts_description": "Watch the full story on Karma Tales: https://youtu.be/ON48F2uLrRA\n" + title + "\n\n#shorts #karmatales #revengestory #weddingdrama",
        },
        "thumbnail_file": "karma/ep05_thumb.jpg",
        "shorts_end_card": "Watch the full story|on our channel",
        "shorts": [
            {"id": "short1", "title": "Her father was dead.|Then the doors opened.", "from": "s01", "to": "s11",
             "youtube_title": "She Told Everyone Her Father Was Dead. Then He Walked Into Her Wedding. #shorts"},
            {"id": "short2", "title": "\"You can't prove that.\"|\"Actually... I can.\"", "from": "s133", "to": "s140",
             "youtube_title": "The Groom Said Nobody Could Prove It. The Maid of Honor Pressed Play. #shorts"},
            {"id": "short3", "title": "\"I can't marry you.\"", "from": "s161", "to": "s171",
             "youtube_title": "She Took Off the Ring at the Altar. Then She Asked Her Dad One Thing. #shorts"},
        ],
    }
    tone = {"chapel": "chapel", "garage": "garage", "garage_night": "garage_night", "restaurant": "restaurant", "street": "street",
            "mansion": "house", "apartment": "apartment", "kitchen": "kitchen", "law_office": "office", "hotel": "hotel", "backyard": "yard"}
    last = None
    for s in scenes:
        key = tone.get(s.get("place", ""))
        if key and key != last:
            spec["ambience"].append([s["id"], key])
            last = key
    out = ROOT / "karma" / "ep05_full.json"
    out.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")
    words = sum(len(t.split()) for s in scenes for _, t in s["lines"])
    print(f"{out.name}: {len(scenes)} scenes, {words} words, {sum(1 for s in scenes if s.get('motion'))} moving clips")


if __name__ == "__main__":
    main()
