"""Write karma/ep04_full.json, Karma Tales EP04 "The Thanksgiving Betrayal", from the user's revised 18-scene script.

usage: python karma/build_ep04.py
Dialogue-led, with eleven_v3 audio tags on nearly every line so the delivery is acted.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

VOICES = {
    "NARRATOR": "FmtiHEcHpocK7YiZwa46",  # Jason - channel narrator
    "EMMA": "AEu9YBjNQiyxUMNdplQu",  # Carrie - warm, grounded, expressive
    "VICTORIA": "8fwYhwfiWkLjR4FKLHSQ",  # Elise Hart - clear, polished
    "RYAN": "6gRQLqLxbhpnX3JtUvf8",  # Max Michael - polished, smooth
    "GRACE": "yM93hbw8Qtvdma2wCnJG",  # Ivanna - young, casual
    "BROOKS": "qAZH0aMXY8tw1QufPN0D",  # Flint - deep, raspy, warm
    "MARGARET": "wGcFBfKz5yUQqhqr0mVy",  # Maria Moody - grandmotherly
}

CAST = {c: f"karma/cast/ep04/{c}.jpg" for c in ["emma", "victoria", "ryan", "grace", "brooks", "margaret"]}

PORTRAIT = ("Photorealistic still from a prestige American TV drama, shot on 35mm, shallow depth of field, soft cinematic key light, "
            "natural skin texture, head-and-shoulders portrait facing slightly off camera, neutral dark background, an entirely "
            "fictional person who resembles no real celebrity, no text, no watermark. ")
PORTRAITS = {
    "grace": "Grace Parker, a 32-year-old American woman, long wavy chestnut-brown hair, sharp hazel eyes, a sardonic half-smile, burgundy knit sweater.",
    "brooks": "Martin Brooks, a 62-year-old American attorney, short silver hair, neat gray beard, kind but sharp blue eyes, charcoal three-piece suit, dark green tie.",
    "margaret": "Margaret Ashford, an 80-year-old American grandmother, soft white hair in a loose bun, laugh lines, bright knowing eyes, pale blue cardigan with a small brooch.",
}

LOOKS = {
    "emma": "Emma (the woman from the reference photo, same face, long tousled light-brown hair, in a cream wool coat over a rust-colored sweater)",
    "emma:dinner": "Emma (the same woman as the reference photo, same face, light-brown hair half up, in a simple forest-green dress)",
    "emma:home": "Emma (the same woman as the reference photo, same face, light-brown hair in a messy bun, in a gray cardigan)",
    "emma:fall": "Emma (the same woman as the reference photo, same face, hair loose, relaxed and smiling, in a mustard-yellow sweater)",
    "victoria": "Victoria (the older blonde woman from the reference photo, same face, hair in an elegant updo, in a burgundy velvet dress with a pearl necklace and pearl earrings)",
    "victoria:home": "Victoria (the same older woman as the reference photo, same face, in a cream silk blouse and pearls)",
    "ryan": "Ryan (the man from the reference photo, same face and short brown hair, in a navy sweater over a collared shirt)",
    "ryan:suit": "Ryan (the same man as the reference photo, same face, in a slim gray suit, no tie)",
    "grace": "Grace (the woman with wavy chestnut hair from the reference photo, in a burgundy sweater)",
    "brooks": "Mr. Brooks (the silver-bearded man from the reference photo, in a charcoal three-piece suit)",
    "margaret": "Margaret (the elderly white-haired woman from the reference photo, in a pale blue cardigan)",
}

PLACES = {
    "dining": "Setting: the grand dining room of a Connecticut mansion on Thanksgiving night, crystal chandelier, a long table with a roast turkey, candles and autumn flowers, fourteen well-dressed guests.",
    "mansion_kitchen": "Setting: a huge white marble kitchen in a Connecticut mansion on Thanksgiving afternoon, pies cooling, copper pots, autumn light.",
    "mansion_hall": "Setting: an upstairs hallway of a Connecticut mansion, dark wood paneling, oil paintings, a door left slightly open with lamplight inside.",
    "mansion_study": "Setting: a dark wood-paneled home study in a Connecticut mansion at night, a desk lamp, leather chairs, bookshelves.",
    "living": "Setting: the formal living room of a Connecticut mansion at night, a crackling stone fireplace, antique furniture, family portraits.",
    "kitchen_home": "Setting: a modest modern townhouse kitchen on a gray November morning, coffee maker, a stack of papers on the counter.",
    "car": "Setting: inside a car parked at a gas station at night in pouring rain, rain streaming down the windshield, neon station lights blurred.",
    "office": "Setting: a traditional law office in Hartford, Connecticut, dark wood, tall windows with gray November light, file boxes, a brass desk lamp.",
    "coffee": "Setting: a small cozy New England coffee shop on a rainy afternoon, wooden tables, fogged windows, warm lamps.",
    "grandma_house": "Setting: a small cozy house with a white porch outside Hartford on Thanksgiving a year later, a modest dining table full of homemade food, warm lamplight, autumn leaves outside the window.",
}

N = "NARRATOR"
S = []


def sc(place, chars, image, lines, **extra):
    S.append((place, chars, image, lines, extra))


# SCENE 1 - COLD OPEN
sc("dining", ["victoria"], "Victoria standing at the head of a long Thanksgiving table, glass raised, looking down the table with a cold smile.",
   [("VICTORIA", "[sharp, cutting through the chatter] Emma. Stand up.")],
   sfx=[["Thanksgiving dinner chatter, silverware, soft jazz piano", 4.0, 0.25, "start"]])
sc("dining", ["emma:dinner"], "Emma seated at the table, fork frozen halfway, looking up in confusion.",
   [("EMMA", "[thrown, quiet] Excuse me?"),
    ("VICTORIA", "[slowly, enjoying it] You heard me. Stand. Up.")])
sc("dining", ["victoria"], "Close-up of Victoria tapping a crystal glass with a silver spoon, guests turning to look.",
   [("VICTORIA", "[loud, theatrical] For four years, I have tolerated a woman who married my son for his money.")],
   sfx=[["A spoon tapping a crystal glass, then the room going silent", 2.0, 0.4, "start"]])
sc("dining", ["victoria", "emma:dinner"], "Victoria pointing down the table at Emma, guests staring.",
   [("VICTORIA", "[cold] You have ten minutes to collect your things and get out of my house.")],
   sfx=[["Guests gasping", 1.5, 0.35, "end"]])
sc("dining", ["emma:dinner"], "Emma standing, sliding her wedding ring off, setting it beside her untouched plate.",
   [("EMMA", "[steady, barely above a whisper] Before I go, Victoria... are you absolutely certain this house belongs to you?")],
   motion="she slowly slides the ring off her finger and sets it down beside the plate")
sc("dining", ["victoria"], "Victoria laughing in disbelief, one hand on her pearls.",
   [("VICTORIA", "[scoffs] Of course it does."),
    ("EMMA", "[calm, cold] Then I hope you have the paperwork.")],
   sfx=[["Music cuts out abruptly, then a deep cinematic boom", 3.0, 0.45, "start"]])
sc("dining", ["ryan"], "Ryan at the table, pale, avoiding everyone's eyes, his hand trembling around his glass.",
   [(N, "[low] Behind her, Victoria laughed. But Ryan didn't. [pause] Because he knew something his mother didn't. And Emma was about to find out.")],
   music="tension")

# SCENE 2 - THREE WEEKS EARLIER
sc("kitchen_home", ["ryan", "emma:home"], "Three weeks earlier: Ryan rushing into the kitchen holding a thick stack of papers and a pen; Emma pouring coffee.",
   [(N, "Three weeks earlier."),
    ("RYAN", "[hurried, distracted] Babe, I need you to sign something."),
    ("EMMA", "[dry, half smiling] Good morning to you too.")],
   sfx=[["Coffee maker gurgling, morning kitchen", 3.0, 0.25, "start"]], music="wonder", cut=True)
sc("kitchen_home", ["ryan"], "Ryan dropping a thick stack of documents on the counter and clicking a pen.",
   [("RYAN", "[sighs] Sorry. I'm running late. Just business documents."),
    ("EMMA", "[flipping pages] Forty-seven pages?"),
    ("RYAN", "[too casual] Standard paperwork.")],
   sfx=[["Heavy stack of papers dropped on a counter", 1.0, 0.4, "start"]])
sc("kitchen_home", ["emma:home"], "Emma reading the documents closely, frowning, finger stopping on a line.",
   [("EMMA", "[slowly] Why does it say three million dollars?"),
    ("RYAN", "It's a credit facility."),
    ("EMMA", "Secured by what?"),
    ("RYAN", "[quick] Company assets.")])
sc("kitchen_home", ["emma:home", "ryan"], "Emma looking up at Ryan skeptically; Ryan checking his watch.",
   [("EMMA", "Then why does it need my signature?"),
    ("RYAN", "[impatient] Because we're married."),
    ("EMMA", "[flat] That's not how business loans work, Ryan."),
    ("RYAN", "[groans] Oh, here we go.")])
sc("kitchen_home", ["ryan"], "Ryan leaning on the counter, jaw tight, irritated.",
   [("RYAN", "[sharp] You always have to question everything."),
    ("EMMA", "I worked in finance before I joined your company. I know what a personal guarantee looks like."),
    ("RYAN", "[cold] Are you calling me a liar?")])
sc("kitchen_home", ["emma:home"], "Emma calmly setting down her coffee, holding his gaze.",
   [("EMMA", "[calm] I'm asking you to explain it."),
    ("RYAN", "[snapping] Forget it.")])
sc("kitchen_home", ["ryan"], "Ryan snatching the papers off the counter.",
   [(N, "He grabbed the papers. But not before Emma had seen enough. [pause] And not before she quietly took a photo of the first page.")],
   sfx=[["Papers snatched off a counter", 1.0, 0.45, "start"]], motion="he sweeps the stack of papers off the counter and turns away")
sc("kitchen_home", ["emma:home", "ryan"], "Emma at the counter, worried; Ryan at the door with his coat half on.",
   [("EMMA", "[softer, worried] Ryan... are we in trouble?"),
    ("RYAN", "No."),
    ("EMMA", "[quiet] Then look me in the eye.")],
   sfx=[["Tense silence, a clock ticking", 2.0, 0.25, "start"]])
sc("kitchen_home", ["ryan"], "Ryan at the door turning back, his face cold.",
   [("RYAN", "[cold, deliberate] My mother was right about you."),
    ("EMMA", "[hurt] What does that mean?"),
    ("RYAN", "You don't understand loyalty.")],
   sfx=[["Front door slamming", 1.0, 0.5, "end"]])

# SCENE 3 - THE PHONE CALL
sc("", ["ryan:suit"], "Ryan sitting alone in his parked car in an office garage, phone to his ear, rubbing his forehead.",
   [("VICTORIA~phone", "[clipped] Did she sign?"),
    ("RYAN", "[tired] No."),
    ("VICTORIA~phone", "[disgusted] Unbelievable.")],
   sfx=[["Phone ringing, then a car interior", 2.0, 0.3, "start"]], music="tension", cut=True)
sc("mansion_study", ["victoria:home"], "Victoria in her study, phone pressed to her ear, standing at the window, her reflection in the glass.",
   [("RYAN~phone", "She started asking questions."),
    ("VICTORIA", "[icy] Then stop giving her opportunities to ask."),
    ("RYAN~phone", "[pleading] Mom, I need her signature.")])
sc("mansion_study", ["victoria:home"], "Close-up of Victoria, a slow calculating smile.",
   [("VICTORIA", "[patient, like explaining to a child] No, darling. You need her cooperation. There's a difference."),
    ("RYAN~phone", "And how am I supposed to get it?"),
    ("VICTORIA", "[softly] Make her understand what she stands to lose.")])
sc("mansion_study", ["victoria:home"], "Victoria turning from the window, decision made.",
   [("RYAN~phone", "[wary] What are you suggesting?"),
    ("VICTORIA", "Thanksgiving is in three weeks. Bring her. [pause] I'll handle the rest.")],
   sfx=[["Low ominous drone", 2.5, 0.3, "end"]])
sc("", ["ryan:suit"], "Ryan in his car, hesitating, phone at his ear.",
   [("RYAN", "[uneasy] Mom..."),
    ("VICTORIA~phone", "[hard] Do you want to save your company or not?")],
   sfx=[["Call ending beep", 1.0, 0.35, "end"]])
sc("", ["ryan:suit"], "Ryan staring at his phone screen in the dark car, the glow on his face.",
   [(N, "Ryan stared at his phone. Then he opened an email from the lender.")],
   overlay={"type": "message", "from": "Bayview Commercial Lending", "to": "Ryan", "text": "Additional authorization required. Deadline: December 1."},
   sfx=[["Phone notification chime", 1.0, 0.4, "start"]])

# SCENE 4 - GRACE HEARS SOMETHING
sc("mansion_hall", ["grace"], "Grace walking down the dim upstairs hallway, stopping at a door left ajar with voices inside.",
   [("GRACE", "[calling out, casual] Mom? You upstairs?")],
   sfx=[["Footsteps on hardwood in a quiet hallway", 2.0, 0.35, "start"]], cut=True)
sc("mansion_hall", ["grace"], "Grace freezing in the hallway, listening at the gap of the door.",
   [("VICTORIA~phone", "[muffled, through the door] She has to believe she's losing everything, Ryan."),
    ("RYAN~phone", "[muffled] And if she still refuses?"),
    ("VICTORIA~phone", "[muffled] Then we move to the second option.")],
   motion="she stops mid-step and slowly leans toward the half-open door")
sc("mansion_hall", ["grace"], "Close-up of Grace's face, eyes widening, holding her breath.",
   [("RYAN~phone", "[muffled, anxious] You promised we wouldn't need that."),
    ("VICTORIA~phone", "[muffled hiss] Keep your voice down.")])
sc("mansion_study", ["grace", "victoria:home", "ryan"], "Grace pushing the study door open; Victoria and Ryan turning, startled.",
   [("GRACE", "[flat] What second option?"),
    ("VICTORIA", "[startled, then composed] Grace! How long have you been standing there?"),
    ("GRACE", "[dry] Long enough.")],
   sfx=[["A door creaking open", 1.5, 0.45, "start"]])
sc("mansion_study", ["ryan", "grace"], "Ryan waving it off; Grace crossing her arms, unconvinced.",
   [("RYAN", "[too quick] It's business."),
    ("GRACE", "[sarcastic] Since when is Emma part of your business negotiations?"),
    ("VICTORIA", "[cold] This is a private conversation.")])
sc("mansion_study", ["grace"], "Grace backing out of the doorway, eyes on her mother.",
   [("GRACE", "[pointed] So is whatever you're planning for Thanksgiving."),
    ("RYAN", "[warning] Grace. Stay out of it."),
    ("GRACE", "[shrugs] Fine.")])
sc("mansion_hall", ["grace"], "Grace walking away down the hallway, jaw set, glancing back once.",
   [(N, "Grace walked away. [pause] But she didn't believe a word of it.")])

# SCENE 5 - THE THANKSGIVING TRAP
sc("mansion_kitchen", ["emma"], "Thanksgiving afternoon: Emma carrying two homemade pies into the mansion's marble kitchen.",
   [(N, "Thanksgiving. Emma had been in Victoria's kitchen since seven a.m."),
    ("EMMA", "[cheerful, trying] Victoria, where do you want the pies?")],
   sfx=[["Busy kitchen, oven timer beeping, pots clanking", 3.0, 0.3, "start"]], music="wonder", cut=True)
sc("mansion_kitchen", ["victoria", "emma"], "Victoria not even looking up from arranging flowers; Emma holding a pecan pie.",
   [("VICTORIA", "[bored] In the kitchen. Obviously."),
    ("EMMA", "[hopeful] I made your favorite. Pecan."),
    ("VICTORIA", "[flat] How thoughtful.")])
sc("mansion_kitchen", ["emma"], "Emma setting the pie down, studying Victoria.",
   [("EMMA", "Is something wrong?"),
    ("VICTORIA", "[too sweet] Why would something be wrong?"),
    ("EMMA", "You've barely spoken to me all morning.")])
sc("mansion_kitchen", ["victoria"], "Victoria walking out of the kitchen with the flower vase, not looking back.",
   [("VICTORIA", "[clipped] I'm hosting fourteen people, Emma. I have responsibilities. [pause] Perhaps you should finish setting the table.")],
   motion="she sweeps out of the kitchen carrying the vase without looking back")
sc("dining", ["emma"], "Emma setting the long dining table alone, laying silverware, the chandelier above.",
   [(N, "So Emma set the table. Fourteen places. And on the sideboard, under a stack of holiday cards, she noticed an envelope.")],
   sfx=[["Silverware being placed on a table, quiet room", 3.0, 0.25, "start"]])
sc("dining", [], "Close-up of an official-looking envelope on a sideboard, a return-address logo with a small oak tree emblem, the printed text soft and unreadable.",
   [(N, "[slowly] The return address said Ashford Family Trust. [pause] Ashford. Her grandmother's name.")],
   sfx=[["Low curious musical note", 2.0, 0.3, "start"]])
sc("dining", ["emma"], "Emma holding the envelope, puzzled, glancing toward the doorway.",
   [(N, "Before she could think about it, footsteps."),
    ("GRACE", "[low, urgent] Emma. Can I talk to you?")],
   sfx=[["Footsteps approaching on hardwood", 1.5, 0.35, "start"]])
sc("dining", ["grace", "emma"], "Grace pulling Emma into a corner of the dining room, speaking quietly.",
   [("GRACE", "[whispering] Did Ryan ask you to sign anything recently?"),
    ("EMMA", "[cautious] Why?"),
    ("GRACE", "Just answer me."),
    ("EMMA", "Some business papers. I said no.")])
sc("dining", ["grace"], "Close-up of Grace, relieved and worried at once.",
   [("GRACE", "[exhales] Good."),
    ("EMMA", "Grace, what's going on?"),
    ("GRACE", "[honest] I don't know yet.")])
sc("dining", ["grace", "emma"], "Grace glancing toward the hallway as someone calls her name, gripping Emma's arm.",
   [("VICTORIA~phone", "[distant, calling] Grace! Come here!"),
    ("GRACE", "[urgent whisper] Emma... whatever happens tonight, don't sign anything.")],
   sfx=[["Tense musical sting", 2.0, 0.35, "end"]])

# SCENE 6 - GET OUT
sc("dining", [], "Thanksgiving dinner in full swing: fourteen guests around the long candlelit table, the chandelier glowing, a carved turkey.",
   [(N, "Seven fifteen. Fourteen guests. Candles lit. The turkey carved. [pause] And then Victoria stood up.")],
   sfx=[["Dinner guests laughing and chatting, glasses clinking", 4.0, 0.3, "start"]], music="tension", cut=True)
sc("dining", ["victoria"], "Victoria standing at the head of the table, raising her champagne glass with a gracious smile.",
   [("VICTORIA", "[gracious, smiling] I'd like to make a toast."),
    ("EMMA", "[hopeful, raising her glass] To family?"),
    ("VICTORIA", "[the smile freezing] To knowing who deserves to be called family.")])
sc("dining", ["victoria"], "Victoria setting her glass down hard, her face turning cold.",
   [("VICTORIA", "[cold] Emma. Stand up.")],
   sfx=[["Glass set down hard on a table", 1.0, 0.45, "start"]])
sc("dining", ["victoria", "emma:dinner"], "Emma slowly standing, confused, while guests exchange looks.",
   [("EMMA", "Victoria, if there's a problem, we can talk after dinner."),
    ("VICTORIA", "[loud] Oh, no. I want everyone to hear this.")])
sc("dining", ["victoria"], "Victoria addressing the guests like a speech, gesturing at Emma.",
   [("VICTORIA", "[theatrical] For four years, I have tolerated a woman who married my son for his money. She came into this family with nothing. No money. No connections. [pause] Not even a respectable family name.")])
sc("dining", ["emma:dinner"], "Close-up of Emma, cheeks burning, voice shaking but firm.",
   [("EMMA", "[shaking] That's not true. [firmer] And don't talk about my family."),
    ("VICTORIA", "[contempt] Then stop pretending you're one of us.")])
sc("dining", ["emma:dinner", "ryan"], "Emma turning to Ryan beside her; Ryan staring at his plate.",
   [("EMMA", "[desperate] Ryan. Say something."),
    ("RYAN", "[mumbling] Emma, please. Don't make this worse."),
    ("EMMA", "[stunned] I'm making it worse?")])
sc("dining", ["victoria"], "Victoria checking a delicate gold watch on her wrist, smiling.",
   [("VICTORIA", "[cold, savoring it] You have ten minutes to collect your things and get out of my house.")],
   sfx=[["Guests gasping, a fork dropping on a plate", 2.0, 0.4, "start"]])
sc("dining", ["emma:dinner"], "Emma staring at Victoria in disbelief.",
   [("EMMA", "[disbelief] You're throwing me out... on Thanksgiving?"),
    ("VICTORIA", "[sweetly] Consider it my holiday gift to you.")])
sc("dining", ["ryan"], "Ryan finally looking up, weak and guilty.",
   [("EMMA", "[barely a whisper] Ryan?"),
    ("RYAN", "[can't look at her] Maybe it's better if you go. Just for tonight. We'll talk tomorrow.")])
sc("dining", ["emma:dinner"], "Emma pushing her chair back, standing tall, eyes wet but steady.",
   [("EMMA", "[quiet, breaking] Four years. [pause] Four years, and you can't even stand up for me.")],
   sfx=[["A chair scraping back on a wooden floor", 1.5, 0.45, "start"]])
sc("dining", ["emma:dinner"], "Close-up of Emma's hand sliding off her wedding ring and setting it beside her untouched plate.",
   [(N, "Emma slowly took off her wedding ring. And set it down beside her untouched plate.")],
   motion="she slides the ring off her finger and places it gently on the tablecloth")
sc("dining", ["emma:dinner", "victoria"], "Emma looking straight at Victoria across the table.",
   [("EMMA", "[steady] Before I go, Victoria. One question."),
    ("VICTORIA", "[impatient] Make it quick."),
    ("EMMA", "[slow, deliberate] Are you absolutely certain this house belongs to you?")])
sc("dining", ["victoria"], "Close-up of Victoria, a flicker of fear behind the scoff.",
   [("VICTORIA", "[scoffs, too quickly] Of course it does."),
    ("EMMA", "[calm] Then I hope you have the paperwork.")],
   sfx=[["Music cuts out, a deep cinematic boom", 3.0, 0.45, "start"]])
sc("dining", ["emma"], "Emma in her coat walking out through the mansion's grand front doors into the cold dark rain.",
   [("VICTORIA", "[calling after her] Your ten minutes are almost up!"),
    ("EMMA", "[not turning around] Keep your ten minutes.")],
   sfx=[["Heavy front door slamming, rain outside", 2.0, 0.5, "end"]], motion="she walks out the front doors into the rain without looking back")

# SCENE 7 - THE CALL IN THE RAIN
sc("car", ["emma"], "Emma in her car at a gas station in pouring rain, mascara running, gripping the steering wheel.",
   [(N, "Emma made it as far as a gas station two miles away. Then she couldn't drive anymore."),
    ("EMMA", "[crying, to herself] Come on, Ryan. Call me. Tell me you're sorry.")],
   sfx=[["Heavy rain on a car roof, engine idling", 4.0, 0.35, "start"]], music="tension", cut=True)
sc("car", ["emma"], "Emma grabbing her buzzing phone off the passenger seat.",
   [("EMMA", "[hopeful] Ryan?"),
    ("BROOKS~phone", "[calm, gravelly] Emma? It's Martin Brooks. Your grandmother's attorney.")],
   sfx=[["Phone vibrating on a seat", 1.5, 0.4, "start"]])
sc("office", ["brooks"], "Mr. Brooks at his desk late at night, lamp on, phone to his ear, a thick file open.",
   [("EMMA", "[confused] Mr. Brooks?"),
    ("BROOKS", "[apologetic] I'm sorry to call on Thanksgiving. But we have a serious problem. The property at 18 Ashford Lane."),
    ("EMMA", "[thrown] Victoria's house?")])
sc("office", ["brooks"], "Close-up of Mr. Brooks, grave.",
   [("BROOKS", "[measured] Emma... that house belongs to your grandmother's family trust. It has for twelve years.")],
   sfx=[["Thunder rolling", 3.0, 0.45, "start"]])
sc("car", ["emma"], "Emma frozen in the car, rain streaming down the windshield, her face lit by neon.",
   [("EMMA", "[stunned] What? But Victoria says..."),
    ("BROOKS~phone", "Victoria has an occupancy agreement. She lives there. She doesn't own it.")],
   motion="rain streams down the windshield as she sits completely still")
sc("car", ["emma"], "Emma pressing her hand against her forehead.",
   [("EMMA", "[slowly] And you're telling me this tonight because...?"),
    ("BROOKS~phone", "[grave] Because someone tried to use that house as collateral for a three-million-dollar loan.")])
sc("car", ["emma"], "Close-up of Emma's eyes hardening.",
   [("EMMA", "[cold, certain] Ryan."),
    ("BROOKS~phone", "[careful] Come to my office in the morning. First, we protect the trust. Then we find out exactly who signed what.")],
   sfx=[["Deep dramatic impact", 2.5, 0.45, "end"]])

# SCENE 8 - THE REAL OWNER
sc("office", ["brooks", "emma"], "Next morning: Mr. Brooks opening a thick folder across his desk to Emma.",
   [(N, "The next morning."),
    ("BROOKS", "Your grandmother bought that house fifteen years ago. After Victoria's family lost almost everything."),
    ("EMMA", "[shocked] Grandma knew Victoria?"),
    ("BROOKS", "[nodding] Very well.")],
   sfx=[["Quiet office, folder opening, papers rustling", 3.0, 0.25, "start"]], cut=True)
sc("office", ["emma"], "Emma shaking her head, overwhelmed.",
   [("EMMA", "Why didn't she ever tell me?"),
    ("BROOKS", "[gentle] She wanted you to build your own life. Without the weight of other people's expectations.")])
sc("office", [], "Close-up of an appraisal document and a photo of the Connecticut mansion clipped to it, the printed text soft and unreadable.",
   [("EMMA", "How much is the house worth?"),
    ("BROOKS", "The last appraisal? About six million dollars. [pause] And it's one of eleven properties in the trust.")])
sc("office", ["emma"], "Emma sitting back, stunned, almost laughing.",
   [("EMMA", "[a stunned laugh] Eleven. [pause] Victoria spent four years calling me poor."),
    ("BROOKS", "[dry] She knew she didn't own that house."),
    ("EMMA", "Did she know about me?")])
sc("office", ["brooks"], "Mr. Brooks shaking his head slowly.",
   [("BROOKS", "I don't believe she knew you were the primary beneficiary."),
    ("EMMA", "[slowly] So the woman who threw me out of her mansion..."),
    ("BROOKS", "[evenly] Was living in a house that belongs to your grandmother's trust.")],
   sfx=[["Long tense silence, a clock ticking", 2.5, 0.25, "end"]])
sc("office", ["emma"], "Close-up of Emma, the hurt in her eyes turning to resolve.",
   [("EMMA", "[firm] Mr. Brooks? [pause] I want to see the loan documents.")])

# SCENE 9 - THE FORGED SIGNATURE
sc("office", [], "Close-up of loan documents slid across the desk, two signature lines visible, the printed text soft and unreadable.",
   [("EMMA", "That's Ryan's company. Parker Holdings. And that's his signature."),
    ("BROOKS", "Correct.")],
   sfx=[["Paper sliding across a wooden desk", 1.5, 0.45, "start"]], cut=True)
sc("office", ["emma", "brooks"], "Emma pointing at the second signature; Brooks leaning back.",
   [("EMMA", "And who signed here? The trustee line."),
    ("BROOKS", "[dry] Supposedly, me."),
    ("EMMA", "Supposedly?"),
    ("BROOKS", "[flat] I've never seen this document in my life.")])
sc("office", ["emma"], "Emma pulling out her phone, scrolling to a photo.",
   [("EMMA", "[quickly] Three weeks ago Ryan tried to make me sign something. I said no. [pause] But I took a picture.")],
   sfx=[["Phone unlocking", 1.0, 0.35, "start"]])
sc("office", ["brooks"], "Mr. Brooks zooming in on Emma's phone, eyebrows rising.",
   [("BROOKS", "[slowly] Interesting. These name a second borrower. Another two million dollars."),
    ("EMMA", "[stunned] Five million dollars?"),
    ("BROOKS", "Using the same house. Twice.")],
   sfx=[["Low tense musical sting", 2.0, 0.35, "end"]])
sc("office", ["emma"], "Emma staring out the rainy window, betrayed.",
   [("EMMA", "[hollow] Ryan told me everything was fine."),
    ("BROOKS", "[grim] Then your husband has a great deal of explaining to do.")])

# SCENE 10 - THE HUSBAND'S THREAT
sc("office", ["emma"], "Emma outside the law office building in the rain, answering her phone.",
   [(N, "That afternoon, Ryan finally called."),
    ("RYAN~phone", "[annoyed] Emma, where are you?"),
    ("EMMA", "[dry] Somewhere you can't throw me out.")],
   sfx=[["Rain on a sidewalk, a phone ringing", 2.0, 0.3, "start"]], cut=True)
sc("mansion_study", ["ryan"], "Ryan pacing in the mansion study with his phone.",
   [("RYAN", "[sarcastic] Very funny. Listen, we need to talk about the documents."),
    ("EMMA~phone", "[pointed] Which ones?")],
   sfx=[["A beat of silence on a phone line", 1.5, 0.2, "start"]])
sc("mansion_study", ["ryan"], "Ryan stopping dead, his face draining.",
   [("RYAN", "[careful] What do you mean?"),
    ("EMMA~phone", "The three-million-dollar loan? [pause] Or the other two million?"),
    ("RYAN", "[sharp] Who told you about that?")])
sc("", ["emma"], "Emma under an awning in the rain, phone at her ear, cold and composed.",
   [("EMMA", "[quiet] So there is another loan."),
    ("RYAN~phone", "[controlled anger] Emma, listen carefully. Those are confidential business matters."),
    ("EMMA", "You tried to make me sign them.")])
sc("mansion_study", ["ryan"], "Ryan shouting into the phone, red-faced.",
   [("RYAN", "[shouting] Because you're my wife!"),
    ("EMMA~phone", "[calm] Not for much longer."),
    ("RYAN", "[scoffs] Don't be dramatic.")])
sc("", ["emma"], "Emma with the phone, eyes steady, rain behind her.",
   [("EMMA", "I'm calling a divorce attorney."),
    ("RYAN~phone", "[threatening, low] If you do that, I'll make sure you walk away with nothing."),
    ("EMMA", "[almost amused] You already tried that on Thanksgiving.")])
sc("mansion_study", ["ryan"], "Ryan gripping the phone, sneering.",
   [("RYAN", "[sneering] You think you're so clever?"),
    ("EMMA~phone", "[steady] No, Ryan. [pause] I think I'm finally paying attention.")],
   sfx=[["Call disconnecting", 1.0, 0.4, "end"]])

# SCENE 11 - THE SECOND PLAN
sc("mansion_study", ["ryan", "victoria:home"], "Ryan bursting into the study and shutting the door; Victoria looking up from her desk.",
   [("RYAN", "[panicked] Mom. Emma knows about the loans."),
    ("VICTORIA", "[sharp] How?"),
    ("RYAN", "Martin Brooks called her.")],
   sfx=[["A door shutting firmly", 1.0, 0.45, "start"]], music="tension", cut=True)
sc("mansion_study", ["victoria:home"], "Victoria rising from her desk, eyes narrowing.",
   [("VICTORIA", "[bitter] That man has always been a problem."),
    ("RYAN", "We need another way to get the money."),
    ("VICTORIA", "[slowly] You told me the paperwork was valid.")])
sc("mansion_study", ["ryan"], "Ryan unable to meet his mother's eyes.",
   [("RYAN", "[evasive] It was supposed to be. Someone questioned the trustee authorization."),
    ("VICTORIA", "[quietly, dangerous] Ryan. Did you forge that signature?")],
   sfx=[["Silence, a clock ticking", 2.5, 0.25, "start"]])
sc("mansion_study", ["ryan"], "Close-up of Ryan, sweating, choosing his words.",
   [("RYAN", "[evasive] I had Trent prepare the documents."),
    ("VICTORIA", "[sharp] That's not what I asked."),
    ("RYAN", "[weak] I didn't personally sign his name.")])
sc("mansion_study", ["victoria:home"], "Victoria sinking into her chair, a hand over her mouth.",
   [("VICTORIA", "[horrified whisper] Oh, God."),
    ("RYAN", "[desperate] Mom, we need the money."),
    ("VICTORIA", "[shaking] How much trouble are we in?")])
sc("mansion_study", ["ryan"], "Ryan leaning on the desk, defeated.",
   [("RYAN", "[hollow] More than you know. [pause] The company could collapse before Christmas.")],
   sfx=[["Low dramatic musical sting", 2.5, 0.4, "end"]])

# SCENE 12 - VICTORIA'S SECRET
sc("living", ["grace", "victoria:home"], "Late at night: Grace confronting Victoria by the fireplace in the formal living room.",
   [("GRACE", "[direct] Mom. Why did you tell everyone you owned this house?"),
    ("VICTORIA", "[defensive] Because it's our home."),
    ("GRACE", "[sharp] That's not the same thing.")],
   sfx=[["Crackling fireplace in a large quiet room", 4.0, 0.3, "start"]], cut=True)
sc("living", ["victoria:home"], "Victoria staring into the fire, her composure cracking.",
   [("VICTORIA", "[tired] You wouldn't understand."),
    ("GRACE", "Try me."),
    ("VICTORIA", "[quietly] Your father lost almost everything. Fifteen years ago. We were weeks from losing the house.")],
   motion="firelight flickers across her face as she stares into the flames")
sc("living", ["grace"], "Grace stunned, sitting down slowly on the arm of a chair.",
   [("GRACE", "[stunned] What?"),
    ("VICTORIA", "[barely audible] Margaret Ashford helped us."),
    ("GRACE", "[slowly] Emma's grandmother?")])
sc("living", ["victoria:home"], "Close-up of Victoria, ashamed, twisting her pearls.",
   [("VICTORIA", "She had her trust buy the house. And she let us stay. [pause] For twelve years."),
    ("GRACE", "[incredulous] And you never told Emma?"),
    ("VICTORIA", "[defensive] Why would I?")])
sc("living", ["grace"], "Grace standing up, furious.",
   [("GRACE", "[angry] Because you spent four years treating her like she was beneath us!"),
    ("VICTORIA", "[weak] I didn't know she was the beneficiary."),
    ("GRACE", "[cold] That doesn't make it better.")])
sc("living", ["grace", "victoria:home"], "Grace at the doorway, turning back to her mother by the fire.",
   [("VICTORIA", "[pleading] Grace, please."),
    ("GRACE", "[quiet] You know what the worst part is? [pause] Emma would've helped you. Even if she'd never known about the house.")],
   sfx=[["Silence except the crackling fire", 3.0, 0.3, "end"]])

# SCENE 13 - THE SISTER CHOOSES A SIDE
sc("coffee", ["emma"], "Emma at a coffee shop window table, looking up in surprise as someone sits down.",
   [("EMMA", "[surprised] Grace? I wasn't expecting you."),
    ("GRACE", "[awkward, sincere] I owe you an apology.")],
   sfx=[["Quiet coffee shop, rain outside, cups clinking", 4.0, 0.25, "start"]], music="wonder", cut=True)
sc("coffee", ["grace"], "Grace with both hands around a coffee cup, eyes down, ashamed.",
   [("EMMA", "For what?"),
    ("GRACE", "[quiet] For laughing when Mom insulted you. For not saying anything. For pretending it was normal.")])
sc("coffee", ["emma"], "Emma softening, touched.",
   [("EMMA", "[softly] Thank you."),
    ("GRACE", "[leaning in] There's something else. Ryan knew Mom was going to throw you out."),
    ("EMMA", "[tired] I figured.")])
sc("coffee", ["grace"], "Grace leaning across the table, serious.",
   [("GRACE", "No. I mean they planned it. Weeks before Thanksgiving. [pause] Ryan needed you scared enough to sign."),
    ("EMMA", "[slowly] So the whole dinner was staged?")])
sc("coffee", ["grace", "emma"], "The two women facing each other across the small table.",
   [("GRACE", "I heard Mom say you had to believe you were losing everything."),
    ("EMMA", "[quiet] And Ryan agreed?"),
    ("GRACE", "[softly] He didn't stop her.")],
   sfx=[["A coffee cup set down on a saucer", 1.0, 0.4, "end"]])
sc("coffee", ["emma"], "Close-up of Emma, calm resolve settling over her face.",
   [("EMMA", "[steady] Thank you for telling me."),
    ("GRACE", "What are you going to do?"),
    ("EMMA", "[quiet, final] I'm going to stop protecting him.")])

# SCENE 14 - THE FAMILY MEETING
sc("living", ["victoria:home"], "Victoria opening the mansion's front door to find Emma standing there in her coat.",
   [(N, "Four days after Thanksgiving, the doorbell rang at 18 Ashford Lane."),
    ("VICTORIA", "[startled] Emma? What are you doing here?"),
    ("EMMA", "[calm] Hello, Victoria. I brought someone.")],
   sfx=[["Doorbell chime echoing in a large house", 2.0, 0.4, "start"]], music="tension", cut=True)
sc("living", ["brooks", "ryan"], "Mr. Brooks stepping into the foyer with a briefcase; Ryan coming down the staircase, freezing.",
   [("BROOKS", "[pleasant] Good afternoon."),
    ("RYAN", "[alarmed] Martin Brooks?"),
    ("BROOKS", "We need to discuss this property. And some disputed financing documents.")])
sc("living", ["victoria:home"], "Victoria drawing herself up, outraged.",
   [("VICTORIA", "[outraged] This is my home!"),
    ("EMMA", "[evenly] Your home, yes. [pause] Your property? No.")])
sc("living", ["brooks"], "Mr. Brooks laying a copy of a deed on the coffee table.",
   [("BROOKS", "[calm] The Ashford Family Trust holds the deed."),
    ("VICTORIA", "[shrill] I've lived here for twelve years!"),
    ("BROOKS", "Under an occupancy agreement.")],
   sfx=[["Papers placed on a table", 1.0, 0.4, "start"]])
sc("living", ["ryan", "emma"], "Ryan stepping toward Emma, angry; Emma unmoved.",
   [("RYAN", "[angry] Emma, this is ridiculous."),
    ("EMMA", "[cold] What's ridiculous is trying to borrow five million dollars using documents you wouldn't let me read."),
    ("RYAN", "[shouting] You don't understand the business!")])
sc("living", ["emma"], "Emma turning to face the whole room, arms crossed.",
   [("EMMA", "[calm] Then explain it. To everyone.")],
   sfx=[["Heavy silence in a large room", 2.5, 0.25, "start"]])
sc("living", ["emma", "ryan"], "Ryan with his mouth open, nothing coming out; Emma waiting.",
   [("EMMA", "[quiet, pointed] Go ahead, Ryan. [pause] We're listening.")])

# SCENE 15 - THE LIES COLLAPSE
sc("living", ["victoria:home"], "Victoria turning to her son, her voice shaking.",
   [("VICTORIA", "[shaking] Ryan. Tell me the truth."),
    ("RYAN", "[through his teeth] Mom, not now."),
    ("VICTORIA", "[louder] Did you submit those documents?")], cut=True)
sc("living", ["ryan"], "Ryan cornered by the fireplace, hands raised.",
   [("RYAN", "[defensive] Trent handled the paperwork."),
    ("EMMA", "[sharp] With Mr. Brooks's signature on it?"),
    ("RYAN", "[shouting] I didn't forge anything!")])
sc("living", ["brooks"], "Mr. Brooks calmly checking his phone, then looking up.",
   [("BROOKS", "[dry] Interesting you'd say that. Trent called the lender this morning. [pause] He told them you asked him to sign my name.")],
   sfx=[["Deep cinematic boom", 3.0, 0.45, "start"]])
sc("living", ["ryan"], "Close-up of Ryan's face collapsing, color draining.",
   [("RYAN", "[hollow] He... what?")])
sc("living", ["grace"], "Grace stepping forward from the doorway.",
   [("GRACE", "[cold] Ryan, you told me Emma was stealing money from the company."),
    ("RYAN", "[snapping] Grace, stay out of this!"),
    ("EMMA", "[stunned] You told her what?")])
sc("living", ["emma"], "Emma turning slowly to Ryan, hurt and furious.",
   [("EMMA", "[slow fury] I worked for you for almost a year without a real salary."),
    ("RYAN", "[defensive] We were married!"),
    ("EMMA", "[steel] That didn't make my work free.")])
sc("living", ["victoria:home"], "Victoria gripping the back of a chair, looking at her son like a stranger.",
   [("VICTORIA", "[quietly] Ryan... how much of this is true?"),
    ("RYAN", "[desperate] I was trying to save the business!"),
    ("EMMA", "By lying to everyone.")])
sc("living", ["emma"], "Close-up of Emma, calm and devastating.",
   [("RYAN", "[shouting] I had no choice!"),
    ("EMMA", "[quiet] You had plenty of choices, Ryan. [pause] You just kept choosing the ones that hurt other people.")],
   sfx=[["Low musical impact", 2.5, 0.4, "end"]])

# SCENE 16 - THE FIRST APOLOGY
sc("living", ["victoria:home"], "Victoria sitting down slowly on the sofa, suddenly old and small.",
   [(N, "For the first time in four years, Victoria Parker had nothing to say. [pause] Almost nothing."),
    ("VICTORIA", "[small voice] Emma...")],
   sfx=[["Quiet room, fire crackling softly", 3.0, 0.25, "start"]], music="wonder", cut=True)
sc("living", ["victoria:home", "emma"], "Victoria looking up at Emma standing before her.",
   [("EMMA", "Yes?"),
    ("VICTORIA", "[humbled] I may have misjudged you."),
    ("EMMA", "[dry] You think?")])
sc("living", ["emma"], "Emma looking down at Victoria, hurt in her eyes.",
   [("VICTORIA", "I didn't know about the trust."),
    ("EMMA", "[quiet] You knew Grandma saved your family."),
    ("VICTORIA", "[whisper] Yes."),
    ("EMMA", "And you still called my family worthless.")])
sc("living", ["victoria:home"], "Close-up of Victoria, tears in her eyes, finally honest.",
   [("VICTORIA", "[breaking] I was wrong."),
    ("EMMA", "[softly] That's the first honest thing you've said to me in four years.")],
   sfx=[["Silence, a single piano note", 2.0, 0.3, "start"]])
sc("living", ["victoria:home"], "Victoria clutching her pearls, frightened.",
   [("VICTORIA", "[pleading] Will you forgive me?"),
    ("EMMA", "I don't know."),
    ("VICTORIA", "[afraid] What happens to the house?")])
sc("living", ["emma"], "Emma standing straight, composed and fair.",
   [("EMMA", "[even] The trustees will decide. [pause] I'm not going to throw you into the street, Victoria. But I'm not going to protect you from what you did, either.")])
sc("living", ["victoria:home", "emma"], "Victoria reaching out a trembling hand; Emma not taking it.",
   [("VICTORIA", "[whisper] Please."),
    ("EMMA", "[quiet] Funny. That's what I said on Thanksgiving. [pause] And nobody listened.")])

# SCENE 17 - THE FINAL REVENGE
sc("living", ["ryan"], "Ryan stepping toward Emma, desperate, reaching for her hands.",
   [("RYAN", "[desperate, soft] Emma, please. We can fix this. Our marriage."),
    ("EMMA", "No."),
    ("RYAN", "[pleading] I love you.")], cut=True)
sc("living", ["emma"], "Emma pulling her hands away, calm.",
   [("EMMA", "[calm] You loved having someone who'd do anything for you."),
    ("RYAN", "That's not fair."),
    ("EMMA", "[steel] Neither was what you did to me.")])
sc("living", ["ryan"], "Ryan spreading his hands, broken.",
   [("RYAN", "[broken] What do you want?"),
    ("EMMA", "A divorce. [pause] And a full accounting of every dollar that went through your company.")])
sc("living", ["ryan", "brooks"], "Ryan turning red; Mr. Brooks stepping forward with a folder.",
   [("RYAN", "[furious] You can't demand that!"),
    ("BROOKS", "[calm] She doesn't have to. The lender's fraud unit already has. And so does the state's attorney.")])
sc("living", [], "Close-up of divorce papers set down on the coffee table next to the deed.",
   [(N, "Emma placed a single envelope on the table. Divorce papers. Already signed. [pause] Her signature. The only one in this story that was real.")],
   sfx=[["An envelope set down on a table", 1.0, 0.45, "start"]])
sc("living", ["ryan"], "Ryan staring at the papers, shaking.",
   [("RYAN", "[shaking] You're destroying my life!"),
    ("EMMA", "[calm] No, Ryan. You made those decisions. [pause] I'm just refusing to pay for them.")])
sc("living", ["emma"], "Emma buttoning her coat at the front door, looking back once.",
   [("EMMA", "[quiet] You told me to leave on Thanksgiving. Remember?"),
    ("RYAN", "[whisper] Emma, please."),
    ("EMMA", "[final] This time, I'm leaving because I choose to.")],
   sfx=[["Footsteps on marble, a heavy door closing", 2.5, 0.45, "end"]], motion="she turns and walks out through the front door, closing it behind her")
sc("living", ["ryan", "victoria:home", "grace"], "Wide shot: Ryan staring at the papers, Victoria on the sofa, Grace looking at the empty doorway, the fire dying.",
   [(N, "[slow] Ryan stared at the papers. Victoria stared at the deed. And Grace looked at the empty doorway. [pause] For the first time, the Parker family had run out of people to blame.")],
   sfx=[["A low sustained musical chord", 3.0, 0.3, "start"]])

# SCENE 18 - ONE YEAR LATER
sc("grandma_house", ["emma:fall", "grace"], "One year later: Emma and Grace laughing in a cozy small kitchen, a homemade turkey and pies on the counter.",
   [(N, "[warm] One year later."),
    ("GRACE", "[delighted] Emma, this smells incredible."),
    ("EMMA", "[smiling] It's Grandma's recipe.")],
   sfx=[["Warm kitchen sounds, soft acoustic Thanksgiving music, friends chatting", 4.0, 0.3, "start"]], music="wonder", cut=True)
sc("grandma_house", ["grace"], "Grace pointing at a pecan pie, grinning.",
   [("GRACE", "[teasing] You made the pecan pie? [laughs] Mom used to complain about your pies."),
    ("EMMA", "[dry] Your mother complained about everything."),
    ("GRACE", "[laughing] Fair point.")],
   sfx=[["Two women laughing", 2.0, 0.35, "start"]])
sc("grandma_house", ["emma:fall"], "Wide shot of the small dining table with a few friends, candles and homemade food, autumn leaves outside.",
   [(N, "One year after the worst Thanksgiving of her life, Emma was hosting dinner in her grandmother's little house. No chandeliers. No marble. Just people who were glad she was there.")],
   motion="candles flicker as friends pass dishes around the small table")
sc("", ["ryan"], "Ryan in a cheap suit leaving a courthouse alone, head down, gray winter day.",
   [(N, "Ryan pleaded guilty to bank fraud. Trent's testimony saw to that. His company is gone. He'll spend the next three years in federal prison.")],
   sfx=[["Courthouse steps, cold wind, a car door", 3.0, 0.3, "start"]])
sc("", ["victoria:home"], "Victoria alone in a small plain rented apartment, unpacking boxes, no chandelier, no guests.",
   [(N, "Victoria moved out of 18 Ashford Lane in January. She rents a two-bedroom condo now. [pause] Not one of her fourteen Thanksgiving guests has called.")])
sc("grandma_house", ["emma:fall"], "Emma opening the door to Mr. Brooks holding a small wooden box.",
   [(N, "And Emma went back to work as an interior designer."),
    ("EMMA", "[warm] That must be Mr. Brooks. Come in!"),
    ("BROOKS", "[gentle] Happy Thanksgiving, Emma. I brought something your grandmother wanted you to have.")],
   sfx=[["Doorbell, a door opening, cold wind", 2.0, 0.35, "start"]])
sc("grandma_house", [], "Close-up of an old cassette recorder in a wooden box on the table, a hand pressing play.",
   [("EMMA", "What is it?"),
    ("BROOKS", "[softly] A recording.")],
   sfx=[["An old recorder clicking on, soft tape hiss", 2.0, 0.4, "end"]])
sc("grandma_house", ["margaret"], "A warm golden memory: Margaret in her armchair years ago, smiling, speaking to someone off camera.",
   [("MARGARET", "[warm, slow] My darling Emma... If you're listening to this, I hope you've finally learned something. [pause] You can be kind without being weak. You can forgive without forgetting.")],
   motion="the old woman smiles gently and tilts her head as she speaks")
sc("grandma_house", ["emma:fall"], "Close-up of Emma listening, tears in her eyes, a hand over her heart.",
   [("MARGARET", "[tender] And you can love someone without letting them destroy you. [pause] Remember, sweetheart. A house is just walls and a roof. [softly] A home is where you are loved.")],
   sfx=[["Recording clicking off", 1.0, 0.35, "end"]])
sc("grandma_house", ["grace", "emma:fall"], "Grace gently touching Emma's shoulder at the table.",
   [("GRACE", "[softly] Emma? You okay?"),
    ("EMMA", "[a small laugh through tears] Yeah. [pause] I think I finally am.")])
sc("grandma_house", [], "The small white-porched house at dusk, warm light in the windows, autumn leaves blowing across the lawn.",
   [(N, "[reflective] Victoria spent years bragging about a mansion she didn't own. Ryan tried to save his business with money he had no right to borrow. Both of them treated Emma like she was worth nothing. [pause] But when the truth came out, the woman they threw away was the only one who walked away free.")],
   motion="autumn leaves drift across the lawn as the windows glow warm")
sc("grandma_house", ["emma:fall"], "Emma at the head of her small table raising a glass, friends smiling around her.",
   [(N, "[slow, final] Sometimes karma doesn't knock. [pause] Sometimes it waits until Thanksgiving... and lets you open the door yourself."),
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
    title = "My Mother-in-Law Kicked Me Out on Thanksgiving. She Forgot One Thing."
    spec = {
        "title": "Karma Tales EP04 - The Thanksgiving Betrayal",
        "voices": {r: VOICES[r] for r in sorted(roles)},
        "cast": CAST,
        "portraits": {k: PORTRAIT + v for k, v in PORTRAITS.items()},
        "looks": LOOKS,
        "style": "Photorealistic still from a prestige American TV drama, shot on 35mm, cinematic lighting, shallow depth of field, natural skin texture, warm autumn Thanksgiving color palette of amber, burgundy and gold, wide 16:9 frame. Keep every person's face and hair exactly consistent with their reference photo. No text, no captions, no watermark. ",
        "resolution": "2K",
        "music": music,
        "places": PLACES,
        "ambiences": {
            "dinner": ["Large elegant dining room, low murmur of dinner guests, soft jazz far away, silverware", 0.06],
            "house": ["Quiet large house room tone, distant clock, faint wind outside", 0.05],
            "kitchen": ["Quiet home kitchen, refrigerator hum, morning birds outside", 0.05],
            "rain_car": ["Heavy rain on a car roof, engine idling", 0.1],
            "office": ["Quiet law office, rain against tall windows, faint clock", 0.06],
            "fire": ["Crackling fireplace in a large quiet living room", 0.08],
            "coffee": ["Quiet coffee shop, rain outside, soft music far away", 0.07],
            "cozy": ["Warm small house, soft acoustic music, friends chatting quietly", 0.07],
        },
        "ambience": [],
        "scenes": scenes,
        "youtube": {
            "title": title,
            "description": "On Thanksgiving night, in front of fourteen guests, Victoria Parker told her daughter-in-law to get out of her house. Her husband just sat there.\n\nBefore she left, Emma asked one question: \"Are you absolutely certain this house belongs to you?\"\n\nKarma Tales: revenge and twist stories where the people who scheme always get what they deserve.\n\nThis story is fiction. Any resemblance to real people or events is coincidental. Narration and images are AI-generated.\n\n#karmatales #revengestory #motherinlaw #thanksgivingdrama",
            "tags": ["karma tales", "revenge story", "mother in law", "thanksgiving drama", "family betrayal", "hidden inheritance", "kicked out", "twist ending", "karma", "audio drama"],
            "category": "24",
            "shorts_description": f"Full story on Karma Tales: {title}\n\n#shorts #karmatales #revengestory #thanksgiving",
        },
        "thumbnail_file": "karma/ep04_thumb.jpg",
    }
    tone = {"dining": "dinner", "mansion_kitchen": "house", "mansion_hall": "house", "mansion_study": "house", "living": "fire",
            "kitchen_home": "kitchen", "car": "rain_car", "office": "office", "coffee": "coffee", "grandma_house": "cozy"}
    last = None
    for s in scenes:
        key = tone.get(s.get("place", ""))
        if key and key != last:
            spec["ambience"].append([s["id"], key])
            last = key
    out = ROOT / "karma" / "ep04_full.json"
    out.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")
    words = sum(len(t.split()) for s in scenes for _, t in s["lines"])
    print(f"{out.name}: {len(scenes)} scenes, {words} words, {sum(1 for s in scenes if s.get('motion'))} moving clips")


if __name__ == "__main__":
    main()
