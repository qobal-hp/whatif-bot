"""Write karma/ep02_full.json, Karma Tales EP02 "The Second Envelope", from the final script.

usage: python karma/build_ep02.py
Lines carry eleven_v3 audio tags ([softly], [sighs], [voice breaking] ...) so the delivery sounds acted, not read.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

VOICES = {  # voice-library voices picked in the casting round, used by id
    "NARRATOR": "FmtiHEcHpocK7YiZwa46",  # Jason - Warm American Storyteller
    "EMILY": "052jzHJceQiZr7ltnY0C",  # Mia - Lively, Crisp, Expressive
    "JASON": "SF9uvIlY93SJRMdV5jeP",  # Andrew Griffin - calm middle-aged
    "MICHAEL": "UgBBYS2sOqTuMpoF3BR0",  # Mark - Natural Conversations
    "WHITAKER": "wAGzRVkxKEs8La0lmdrE",  # Sully - Mature, Deep
    "ROBERT": "TTyZrDYo6LQowrH8mixJ",  # Joseph Ortman - Deep & Raspy
    "SARAH": "Awx8TeMHHpDzbm42nIB6",  # Kristen - Friendly and Casual
    "REYES": "3dzJXoCYueSQiptQ6euE",  # Alexandra - Confident, Clear
}

CAST = {c: f"karma/cast/ep02/{c}.jpg" for c in ["emily", "jason", "michael", "whitaker", "robert", "sarah", "reyes"]}

PORTRAIT = ("Photorealistic still from a prestige American TV drama, shot on 35mm, shallow depth of field, soft cinematic key light, "
            "natural skin texture, head-and-shoulders portrait facing slightly off camera, neutral dark studio background, an entirely "
            "fictional person who resembles no real celebrity, no text, no watermark. ")
PORTRAITS = {
    "emily": "Emily Carter, a 32-year-old American woman, long dark-brown hair loosely pinned back, warm brown eyes, tired but kind face, no heavy makeup, simple black dress, small gold hoop earrings.",
    "jason": "Jason Carter, a 43-year-old American businessman, short dark hair with a little gray at the temples, square jaw, cold confident expression, charcoal suit, white shirt, navy tie.",
    "michael": "Michael Carter, a 39-year-old American man, tousled brown hair, light stubble, smirking restless expression, navy blazer over an open-collar white shirt, no tie.",
    "whitaker": "Thomas Whitaker, a 68-year-old American attorney, neatly combed silver-white hair, rimless glasses, calm precise expression, gray three-piece suit, burgundy tie.",
    "robert": "Robert Carter, a 76-year-old American man, thinning white hair, weathered face with deep lines, kind tired gray eyes, a faint stubborn set to his jaw, brown cardigan over a plaid shirt.",
    "sarah": "Sarah, a 32-year-old American woman, curly auburn hair to the shoulders, freckles, open friendly face, denim jacket over a white t-shirt.",
    "reyes": "Dana Reyes, a 50-year-old Latina American bank executive, sleek black hair in a low bun, sharp dark eyes, unimpressed expression, black tailored pantsuit, small pearl earrings.",
}

LOOKS = {
    "emily": "Emily (the woman from the reference photo with wavy dark-brown hair loosely pinned back, in a simple black dress)",
    "emily:home": "Emily (the same person as the reference photo, same face and hair, but in a soft gray sweater and jeans)",
    "emily:dinner": "Emily (the same person as the reference photo, same face, hair down, in a fitted navy dress)",
    "emily:board": "Emily (the same person as the reference photo, same face and hair, in a tailored cream blazer over a black top)",
    "emily:porch": "Emily (the same person as the reference photo, same face, hair loose, in a rust-colored knit sweater)",
    "jason": "Jason (the man from the reference photo, in a charcoal suit with a gold wristwatch)",
    "michael": "Michael (the man from the reference photo, in a navy blazer and open-collar shirt)",
    "whitaker": "Mr. Whitaker (the silver-haired man with dark-rimmed glasses from the reference photo, in a gray three-piece suit)",
    "robert": "Robert (the elderly man from the reference photo, in a brown cardigan)",
    "robert:hospital": "Robert (the same elderly man as the reference photo, frail, in a hospital gown, lying in a hospital bed)",
    "sarah": "Sarah (the woman with curly auburn hair from the reference photo, in a denim jacket)",
    "reyes": "Ms. Reyes (the woman from the reference photo, in a black pantsuit)",
}

PLACES = {
    "office": "Setting: a wood-paneled Boston law office on a rainy afternoon, rain streaking the tall windows, a polished mahogany conference table, green banker's lamps.",
    "home": "Setting: the cozy but cluttered living room of an older Boston-area family home, medicine bottles on a side table, a recliner, soft lamp light.",
    "hospital": "Setting: a dim hospital room at three in the morning, monitors glowing, rain on the window.",
    "thanksgiving": "Setting: the same family home's dining room on Thanksgiving afternoon, a modest turkey dinner on the table.",
    "willow_out": "Setting: a modest two-story New England house with blue shutters and a big old maple tree in the front yard, overcast morning.",
    "willow_in": "Setting: inside that old house, a warm living room with wooden floors, lavender light through lace curtains, family photographs on the walls.",
    "study": "Setting: a small wood-paneled home study with a locked oak cabinet, a desk lamp, dust in the light.",
    "kitchen": "Setting: the old house's kitchen at night, rain on the window, family photographs spread across the table.",
    "steakhouse": "Setting: an expensive downtown Boston steakhouse at night, dark leather booths, low amber light, white tablecloths.",
    "boardroom": "Setting: a glass-walled corporate boardroom high above Boston in daylight, a long dark table, a dozen people in suits.",
    "porch": "Setting: the front porch of the blue-shuttered house six months later, the maple tree bright red with autumn leaves, golden morning light.",
}

# (place, chars, picture, lines, extras)
S = []


def sc(place, chars, image, lines, **extra):
    S.append((place, chars, image, lines, extra))


N = "NARRATOR"

# ACT 1 - ONE DOLLAR
sc("office", [], "A single crisp one-dollar bill lying alone on a polished mahogany table, rain-streaked window behind, moody low light.",
   [(N, "[low, deliberate] Her brothers inherited twelve million dollars. [pause] She got one. One single dollar.")],
   sfx=[["Slow wall clock ticking in a quiet room", 6.0, 0.25, "start"]])
sc("office", ["jason", "michael"], "Two brothers in suits laughing across a mahogany conference table, one leaning back in his chair.",
   [(N, "And when the lawyer read the number out loud... her brothers laughed.")],
   sfx=[["Two men laughing in a quiet office", 3.0, 0.3, "start"]])
sc("office", ["whitaker"], "Close-up of an elderly lawyer's hand drawing a cream envelope sealed with red wax out of a leather briefcase.",
   [(N, "[quietly] But then he reached into his briefcase and pulled out a second envelope. And what happened next... took everything they thought they owned.")],
   sfx=[["Deep cinematic boom with distant thunder", 3.0, 0.4, "end"]], motion="the envelope slides slowly out of the briefcase, rain on the window behind")
sc("", [], "Street-level exterior of an old red-brick Boston office building on a rainy Thursday afternoon, people with black umbrellas hurrying along the wet sidewalk, gray sky, seen from across the street.",
   [(N, "The reading of Robert Carter's will took place on a rainy Thursday afternoon in Boston.")], cut=True)
sc("office", ["jason", "michael", "emily"], "Wide shot of three adult siblings seated around a long mahogany conference table, the two brothers close together, the sister alone at the far end.",
   [(N, "His three children sat around a polished mahogany table.")])
sc("office", ["jason"], "Jason adjusting an expensive gold watch on his wrist, a practiced, solemn expression.",
   [(N, "Jason Carter, the eldest, wore a twelve-thousand-dollar watch... and an expression of practiced grief.")])
sc("office", ["michael"], "Michael slouched in his chair, scrolling on his phone under the table, bored.",
   [(N, "Michael, the middle son, kept checking his phone.")])
sc("office", ["emily"], "Emily sitting quietly at the far end of the table, eyes red and swollen from crying, hands folded.",
   [(N, "[softer] And Emily Carter sat quietly at the far end of the table. Her eyes swollen from crying. [pause] Unlike her brothers, she had been there when their father died.")])
sc("office", ["whitaker"], "Mr. Whitaker at the head of the table reading from a document through his glasses.",
   [("WHITAKER", "[formal, measured] Mr. Carter's estate is divided as follows. To Jason Carter, I leave my ownership interest in Carter Development Group. To Michael Carter, the remaining business holdings."),
    ("MICHAEL", "[leaning in] Wait. So how much is that worth?")])
sc("office", ["whitaker", "jason"], "Jason leaning back with a satisfied smile while the lawyer reads.",
   [("WHITAKER", "Based on the most recent valuation... approximately twelve million dollars combined."),
    ("JASON", "[satisfied, quietly] Not bad, Dad. Not bad at all.")])
sc("office", ["michael", "emily"], "Michael grinning across the table at his younger sister, who looks down.",
   [(N, "Michael grinned. Then he looked across the table at his sister."),
    ("MICHAEL", "[smirking] Well, little sister. Let's see what Dad left you.")])
sc("office", ["whitaker"], "Close-up of Mr. Whitaker pausing, looking over his glasses, the page in his hand.",
   [("WHITAKER", "[pause] To my daughter, Emily Carter... I leave the sum of one dollar.")],
   sfx=[["A ticking clock that suddenly stops, then silence", 2.0, 0.35, "end"]])
sc("office", ["emily"], "Emily frozen, stunned, staring at the lawyer.",
   [("EMILY", "[barely a whisper] I'm sorry?"),
    ("WHITAKER", "[gently] One dollar.")])
sc("office", ["jason", "michael"], "The two brothers bursting into laughter, Michael slapping the table.",
   [("MICHAEL", "[laughs] Oh, you've got to be kidding me!"),
    ("JASON", "[chuckling] Dad always did have a sense of humor."),
    ("MICHAEL", "[laughing] Hey, Emily. Don't spend it all in one place.")],
   sfx=[["Two men laughing loudly in an office", 3.0, 0.3, "start"]])
sc("office", ["emily"], "Emily staring at the table, a single tear falling, her brothers blurred in the background.",
   [(N, "[slowly] Emily stared at the table. Ten years. Ten years of hospital visits, medication schedules, sleepless nights... and canceled vacations. And her father had left her one dollar.")],
   music="tension")
sc("office", ["jason", "emily"], "Jason speaking to Emily with false sympathy, one hand raised.",
   [("JASON", "[condescending] Don't take it personally, Emily. Dad knew who could actually run a business."),
    ("EMILY", "[quiet, hurt] I wasn't expecting the business."),
    ("MICHAEL", "[snorts] Clearly.")])
sc("office", ["emily"], "Emily rising from her chair to leave, picking up her coat.",
   [("EMILY", "[voice catching] I just thought... [sighs] Never mind."),
    (N, "She stood to leave. But Mr. Whitaker raised one hand.")])
sc("office", ["whitaker"], "Mr. Whitaker sliding a cream envelope with a red wax seal across the mahogany table.",
   [("WHITAKER", "[firm but kind] Miss Carter. Please sit down. [pause] There is another envelope.")],
   sfx=[["Paper envelope sliding across a wooden table", 1.5, 0.5, "end"]], motion="the envelope slides slowly across the polished table toward camera")
sc("office", ["jason", "michael", "whitaker"], "The brothers staring at the sealed envelope, smiles gone.",
   [("JASON", "[thrown] Another envelope?"),
    ("WHITAKER", "Your father's instructions were clear. It may only be opened after the first distribution has been read."),
    ("MICHAEL", "[uneasy] What's in it?"),
    ("WHITAKER", "[dry] A warning. For the two of you.")],
   sfx=[["Deep cinematic boom impact with a low sub drop", 3.0, 0.4, "end"]])

# ACT 2 - THE DAUGHTER WHO STAYED
sc("", ["robert"], "Robert Carter in his sixties, strong and proud, in a hard hat in front of a Boston construction site with blueprints, a framed old photo look.",
   [(N, "[reflective] To understand what happened in that room, you need to understand the ten years that came before it. Robert Carter built Carter Development Group from a small construction business into a regional real estate company.")],
   music="wonder", cut=True)
sc("", ["robert"], "In a busy construction company office years ago, Robert at a desk, stern and demanding, pointing at a document.",
   [(N, "He was demanding. Stubborn. [pause] And, according to his sons... worth every penny he had.")])
sc("hospital", ["robert:hospital"], "Robert in a hospital bed after a stroke, one side of his face slack, monitors glowing.",
   [(N, "[somber] Then, at sixty-eight, Robert suffered a stroke.")], sfx=[["Slow hospital heart monitor beeping", 4.0, 0.25, "start"]])
sc("home", ["emily:home"], "Emily carrying a cardboard moving box through the front door of her father's house.",
   [(N, "Jason was busy expanding the company. Michael was busy enjoying the money. [pause] And Emily moved back home.")])
sc("home", ["robert", "emily:home"], "Robert in a recliner, looking at Emily, who kneels beside him holding his hand.",
   [("ROBERT", "[gruff, tired] You don't have to do this, sweetheart."),
    ("EMILY", "[gently] Do what?"),
    ("ROBERT", "Give up your apartment. Your job. Your life."),
    ("EMILY", "[warm, a small laugh] Dad, I'm not giving up my life. I'm making sure you're still part of it.")])
sc("home", ["robert", "emily:home"], "Emily helping her father take slow steps with a walker in the living room.",
   [(N, "Emily worked remotely when she could. She drove her father to appointments. She helped him learn to walk again.")],
   motion="the old man takes one slow careful step with the walker as the woman steadies his arm")
sc("hospital", ["emily:home", "robert:hospital"], "Emily asleep in a chair beside her father's hospital bed at 3 a.m., holding his hand.",
   [(N, "[softly] And when he got worse, she was the one beside his hospital bed at three in the morning.")])
sc("home", [], "A vase of cheap supermarket flowers with a small card on a side table among medicine bottles.",
   [(N, "Jason visited twice a year. Michael sent flowers. [pause] Sometimes.")])
sc("home", ["sarah", "emily:home"], "Emily and her friend Sarah on a worn couch with mugs of coffee, Sarah looking at her with concern.",
   [(N, "Her best friend Sarah was the only one who ever asked how Emily was doing."),
    ("SARAH", "[half teasing, half worried] When's the last time you slept more than four hours?"),
    ("EMILY", "[tired laugh] What year is it?")])
sc("home", ["sarah", "emily:home"], "Sarah leaning forward, serious now, Emily looking away.",
   [("SARAH", "[serious] That's not funny, Em. Your brothers have money. Make them help."),
    ("EMILY", "[sighs] They'd say I'm the one wasting it.")])
sc("thanksgiving", ["jason", "emily:home"], "Jason arriving in a cashmere coat holding an expensive bottle of wine, looking around the dining room with disapproval.",
   [(N, "She was right. One Thanksgiving, Jason arrived with an expensive bottle of wine. He stayed forty minutes."),
    ("JASON", "[disapproving] You've really let this place go, Emily.")])
sc("thanksgiving", ["jason", "emily:home"], "Emily standing tense in the dining room facing Jason.",
   [("EMILY", "[tight] I've been a little busy."),
    ("JASON", "Dad's paying for everything. You could at least hire a cleaning service."),
    ("EMILY", "Dad's medical bills aren't cheap, Jason."),
    ("JASON", "[cold] That's why he has money. Every month you spend more of it.")])
sc("thanksgiving", ["michael"], "Michael leaning in the doorway with a beer, smirking.",
   [("MICHAEL", "[snide] Come on, Emily. It's not like you have a real job anymore."),
    ("EMILY", "[hurt] I still work."),
    ("MICHAEL", "[shrugs] Sure. Whatever you call it.")])
sc("thanksgiving", ["robert"], "Robert at the head of the Thanksgiving table, silent, watching his children, his face unreadable.",
   [(N, "[slowly] Robert heard every word. But he said nothing. Not that day. Not the next. And for years, Emily believed his silence meant he agreed with them.")])
sc("home", ["robert", "emily:home"], "Evening light, Robert in his recliner looking seriously at Emily sitting across from him.",
   [(N, "Then, six months before his death, Robert asked her a strange question."),
    ("ROBERT", "[quietly] Emily... if I left you nothing, would you hate me?")])
sc("home", ["robert", "emily:home"], "Emily looking at her father, confused and hurt.",
   [("EMILY", "[confused] What? Dad, why would you ask that?"),
    ("ROBERT", "[insistent] Just answer me."),
    ("EMILY", "[thinks, then softly] I'd be hurt. But I wouldn't hate you."),
    ("ROBERT", "Why not?")])
sc("home", ["emily:home"], "Close-up of Emily smiling sadly at her father.",
   [("EMILY", "[gentle, a little smile] Because you're my dad. Not my retirement plan.")])
sc("home", ["robert"], "Robert turning toward the window, a slow small smile spreading on his weathered face, golden evening light.",
   [(N, "[warm] Robert turned toward the window. And smiled. [pause] Emily didn't know it then. But that answer would decide the rest of her life.")],
   motion="the old man slowly turns his head toward the window and a faint smile appears")

# ACT 3 - THE SECOND ENVELOPE
sc("office", ["jason"], "Back in the law office, Jason checking his gold watch impatiently.",
   [("JASON", "[impatient] Can we get this over with? I have a meeting at four.")], music="tension", cut=True)
sc("office", ["whitaker"], "Close-up of Mr. Whitaker breaking the red wax seal of the envelope, a handwritten letter inside.",
   [(N, "Mr. Whitaker broke the seal. Inside was a letter in Robert Carter's unmistakable handwriting.")],
   sfx=[["Wax seal cracking and paper unfolding", 2.0, 0.5, "start"]])
sc("office", ["whitaker"], "Mr. Whitaker reading the handwritten letter aloud, holding it at arm's length.",
   [("WHITAKER", "[reading] \"To my sons, Jason and Michael. You have spent years asking what my company is worth. Today you will learn the difference between what a company is worth... and what it owes.\"")])
sc("office", ["michael", "whitaker"], "Michael frowning, confused.",
   [("MICHAEL", "[confused] What does that mean?"),
    ("WHITAKER", "[reading] \"Before you celebrate, read page two.\"")])
sc("office", ["jason"], "Jason grabbing the second page, his face draining of color as he reads.",
   [(N, "Jason grabbed the second page. His eyes moved down the lines. And the color left his face."),
    ("JASON", "[stunned] Nine million dollars?")],
   sfx=[["Deep cinematic boom impact with a low sub drop", 3.0, 0.4, "end"]])
sc("office", ["michael", "whitaker"], "Michael looking from his brother to the lawyer in alarm.",
   [("MICHAEL", "[alarmed] Nine million what?"),
    ("WHITAKER", "[matter-of-fact] Debt. Loans against every property the company owns. Two tenant lawsuits. And a lender demanding more collateral by the end of the quarter.")])
sc("office", ["michael", "whitaker"], "Michael half rising from his chair, Mr. Whitaker calm.",
   [("MICHAEL", "[protesting] But the company's worth twelve!"),
    ("WHITAKER", "[dry] The buildings are worth twelve, Mr. Carter. The company owes nine of it. [pause] What you inherited today is mostly a very large bill.")])
sc("office", ["jason", "michael"], "The two brothers sitting in stunned silence, no longer laughing.",
   [(N, "[quietly] Nobody laughed now.")])
sc("office", ["whitaker"], "Mr. Whitaker placing an accountant's report on the table.",
   [("WHITAKER", "There is one more item. Your father's accountant found eight hundred thousand dollars in payments he could not explain. Payments approved while the two of you ran daily operations.")])
sc("office", ["jason", "michael"], "Michael glancing at Jason; Jason looking away.",
   [(N, "Michael looked at his brother. Jason looked away."),
    ("JASON", "[defensive] Dad knew about those transactions."),
    ("WHITAKER", "[dry] Then I'm sure the records will say so.")])
sc("office", ["emily"], "Emily watching her brothers closely, eyes narrowing.",
   [(N, "Emily caught the glance between her brothers. It was brief. But she knew it. The same look they shared as boys whenever they'd broken something... and needed someone else to blame.")])
sc("office", ["emily", "jason"], "Emily speaking up; Jason turning on her sharply.",
   [("EMILY", "[steady] What happened to the money?"),
    ("JASON", "[snapping] Stay out of this, Emily. You got your dollar. This doesn't concern you.")])
sc("office", ["whitaker", "emily"], "Mr. Whitaker turning toward Emily with a meaningful look.",
   [("WHITAKER", "[calm] Actually, Mr. Carter, your sister is the only person in this room who hasn't received all of her father's instructions."),
    ("WHITAKER", "[to Emily, gently] Your father left you something else. Just not in this will.")])

# ACT 4 - WILLOW STREET
sc("willow_out", [], "A modest two-story house with blue shutters and a huge old maple tree, seen from the street.",
   [(N, "[gentle] The next morning, Emily drove to a small house on Willow Street. Two stories. Blue shutters. An old maple tree in the front yard.")],
   music="wonder", sfx=[["Car door closing, wind through trees, birds", 3.0, 0.3, "start"]], cut=True,
   motion="leaves of the big maple tree sway gently in the wind")
sc("willow_out", ["emily"], "Emily standing on the sidewalk looking up at the house, astonished.",
   [(N, "The house she grew up in. Her father had sold it twenty years ago. [pause] Or so she'd been told.")])
sc("willow_out", ["whitaker", "emily"], "Mr. Whitaker waiting on the porch; Emily walking up the steps.",
   [("EMILY", "Why are we here?"),
    ("WHITAKER", "Because your father wanted you to see it before your brothers did.")])
sc("willow_out", ["whitaker", "emily"], "Emily and Mr. Whitaker on the porch, Emily confused.",
   [("EMILY", "[confused] I thought he sold this house."),
    ("WHITAKER", "[a faint smile] That's what he told all of you. He moved it into a trust instead. The Willow Family Trust. Last year, you became the sole beneficiary.")])
sc("willow_out", ["emily", "whitaker"], "Emily staring at the house with her hand on her chest.",
   [("EMILY", "[disbelief] Dad owned this house the whole time?"),
    ("WHITAKER", "It's outside the estate. Your brothers can't touch it, sell it, or borrow against it. He made sure of that.")])
sc("willow_in", ["emily"], "Emily stepping into the warm old living room, light through lace curtains.",
   [(N, "[softly] Emily walked through the front door. The living room smelled of old wood and lavender.")])
sc("willow_in", [], "A framed photograph of a smiling young mother on the wall of the living room.",
   [(N, "On the wall hung a photograph of her mother, who died when Emily was twelve."),
    ("EMILY", "[emotional] Mom loved this house."),
    ("WHITAKER", "[gently] Your father knew that. He left you a note.")])
sc("willow_in", [], "Close-up of a woman's hands holding a small folded cream note card, the handwriting on it soft and out of focus so no words can be read, warm window light.",
   [(N, "One line, in her father's handwriting."),
    ("ROBERT", "[tired, tender] \"Behind your mother's picture. Take it to Whitaker. And don't let your brothers tell you that you owe them anything.\"")],
   sfx=[["Low ominous musical drone swelling", 3.0, 0.3, "end"]])
sc("willow_in", ["emily"], "Emily lifting the framed photograph off the wall; a small brass key falls into her palm.",
   [(N, "Emily lifted the frame from the wall. A small brass key fell into her palm.")],
   sfx=[["A small metal key dropping into a hand", 1.0, 0.5, "end"]], motion="she lifts the frame away from the wall and a small brass key drops into her open hand")
sc("willow_in", [], "Extreme close-up of a small brass key with a paper tag that has handwriting on it, in a woman's palm.",
   [(N, "[slowly] A paper tag hung from it. Three words. \"The original ledger.\"")])

# ACT 5 - THE LEDGER
sc("study", ["emily"], "Emily turning the brass key in the lock of an old oak cabinet in the study.",
   [(N, "The key opened a locked cabinet in Robert's old study.")], sfx=[["An old lock turning and a cabinet door creaking open", 2.0, 0.5, "start"]], music="tension", cut=True)
sc("study", [], "Inside the cabinet: a thick leather accounting ledger and a small silver digital voice recorder.",
   [(N, "Inside was a thick accounting ledger. And a small digital recorder.")])
sc("study", ["whitaker", "emily"], "Mr. Whitaker at the desk turning ledger pages, his expression hardening; Emily watching.",
   [(N, "Mr. Whitaker turned the pages slowly. His expression hardened."),
    ("EMILY", "[anxious] What is it?"),
    ("WHITAKER", "Your father's own records. And a report from a forensic accountant he hired eight months before he died.")])
sc("study", [], "Close-up of ledger pages with long columns of handwritten payment entries, two company names circled in red ink.",
   [(N, "Page after page showed payments to consulting firms Emily had never heard of. Northbridge Advisory. Meridian Strategic Partners. Five years of payments. Starting the month Jason took over operations.")])
sc("study", ["emily", "whitaker"], "Emily looking up from the ledger at Mr. Whitaker.",
   [("EMILY", "Who owns these companies?"),
    ("WHITAKER", "[grave] Northbridge is registered to Michael. Meridian traces back to Jason. Eight hundred thousand dollars, paid by the company... to your brothers.")])
sc("study", ["emily"], "Emily sinking into a chair, stunned.",
   [("EMILY", "[stunned, quiet] They were paying themselves."),
    (N, "Emily sat down. For years, her brothers had complained that their father's care was draining the family. They questioned every prescription. Every hospital bill. [pause] Meanwhile, hundreds of thousands of dollars were walking out the back door.")])
sc("study", ["emily"], "Close-up of Emily, tears welling, her voice breaking.",
   [("EMILY", "[voice breaking] They made me feel guilty for buying Dad a better wheelchair."),
    ("EMILY", "[crying] Jason told me I was bankrupting the family.")])
sc("study", ["whitaker"], "Mr. Whitaker placing the small silver recorder on the desk in front of her.",
   [("WHITAKER", "[gently] Your father asked me to give you this only after you found the ledger."),
    (N, "Emily pressed play.")], sfx=[["A small recorder button click", 1.0, 0.5, "end"]])
sc("study", ["emily"], "The small recorder on the desk, its red light on, Emily's hands around it.",
   [("ROBERT~phone", "[weak, raspy] Emily... if you're hearing this, I'm gone. [sighs] And I owe you an apology. I should have defended you when your brothers made you feel small. I thought keeping the peace would keep the family together. [pause] I was wrong.")],
   motion="the recorder's red light blinks softly on the desk")
sc("study", ["emily"], "Emily closing her eyes, tears running down her cheeks.",
   [(N, "Emily closed her eyes."),
    ("ROBERT~phone", "[bitter, tired] When I asked Jason about those payments, he told the accountant I was confused. That I didn't know what I was signing anymore. [pause] My own son. So I stopped asking him. And I started keeping records.")],
   sfx=[["Low tense musical sting", 2.0, 0.3, "start"]])
sc("study", ["emily"], "Emily listening, her face slowly hardening with resolve.",
   [("ROBERT~phone", "[gentle] I can't tell you what to do with any of this. But I can tell you one thing. The people who call you selfish for setting boundaries... are usually the ones who benefited when you had none.")],
   sfx=[["Recorder click off", 1.0, 0.5, "end"]])
sc("study", ["emily", "whitaker"], "Emily wiping her tears, looking up at Mr. Whitaker with determination.",
   [(N, "Emily sat in silence for a long time. Then she wiped her tears."),
    ("EMILY", "[steady] Mr. Whitaker?"),
    ("WHITAKER", "Yes?"),
    ("EMILY", "[firm] I want the truth. All of it.")])

# ACT 6 - THE THREAT
sc("kitchen", ["emily:home"], "Emily at the kitchen table at night surrounded by old family photographs, rain on the window, her phone buzzing.",
   [(N, "[calm] Three days later, Emily was sitting in the kitchen on Willow Street, surrounded by photographs of her childhood. For the first time in ten years, she had slept through the night. Then her phone rang.")],
   sfx=[["Phone vibrating on a wooden table", 2.0, 0.4, "end"]], cut=True)
sc("", ["jason"], "Jason on his phone in a dark luxury high-rise office at night, tense, standing by a window.",
   [("JASON~phone", "[controlled anger] Emily. We need to talk. About Willow Street. We know Dad gave it to you."),
    ("EMILY", "[calm] And?"),
    ("JASON~phone", "That property should have been part of the estate.")])
sc("kitchen", ["emily:home"], "Emily on the phone, calm and composed.",
   [("EMILY", "It wasn't. Dad put it in a trust years ago."),
    ("JASON~phone", "[hissing] You manipulated a sick old man."),
    ("EMILY", "[cool] Be careful, Jason. You might have to prove that in court.")])
sc("", ["jason"], "Jason pacing by the floor-to-ceiling window of a dark high-rise office at night, gripping his phone.",
   [("JASON~phone", "[pressing] The bank wants two million dollars in new collateral by the end of the month. We need that house."),
    ("EMILY", "[flat] Then I guess you have a problem."),
    ("JASON~phone", "[shouting] You lived off Dad for ten years!")])
sc("kitchen", ["emily:home"], "Close-up of Emily, eyes hard.",
   [("EMILY", "[quiet, firm] I took care of Dad for ten years. There's a difference."),
    ("JASON~phone", "[threatening] Sign it over, Emily. Or we'll challenge the trust and drag you through court until there's nothing left."),
    ("EMILY", "Do what you think you have to do.")])
sc("kitchen", ["emily:home"], "Emily holding the phone, a cold steady look.",
   [("JASON~phone", "[venomous] You'll regret this."),
    ("EMILY", "I already regret something."),
    ("JASON~phone", "What's that?"),
    ("EMILY", "[cold, deliberate] Thirty-two years of believing you were my brother.")],
   sfx=[["A phone call disconnecting beep", 1.0, 0.4, "end"]])
sc("kitchen", ["emily:home"], "Emily's hand trembling on the table next to the phone.",
   [(N, "Emily set the phone down. Her hands were shaking. Not from fear. [pause] From anger. A few minutes later, it rang again. Michael.")],
   sfx=[["Phone vibrating on a wooden table", 2.0, 0.4, "end"]])
sc("", ["michael"], "Michael on his phone in a messy apartment at night, nervous, running a hand through his hair.",
   [("MICHAEL~phone", "[nervous] Em, listen. Jason's freaking out."),
    ("EMILY", "Then he should calm down."),
    ("MICHAEL~phone", "If the bank calls the loans, we lose everything. [pleading] We're family.")])
sc("kitchen", ["emily:home"], "Emily on the phone, unmoved.",
   [("EMILY", "[dry] Funny. Nobody remembered that when Dad needed help."),
    ("MICHAEL~phone", "That was different."),
    ("EMILY", "It always is when you're the one who needs something.")])
sc("", ["michael"], "Michael in his messy apartment at night lowering his voice, glancing over his shoulder.",
   [(N, "Michael's voice dropped."),
    ("MICHAEL~phone", "[low, scared] You don't know what Jason's capable of. He's not going to go down alone."),
    ("EMILY", "[resolute] Then maybe it's time somebody found out.")])

# ACT 7 - THE DINNER
sc("steakhouse", [], "An upscale Boston steakhouse at night, low amber light, a corner booth with two glasses of whiskey and an empty third chair.",
   [(N, "One week later, Jason invited Emily to dinner at an expensive steakhouse in downtown Boston. Michael was already there. Two glasses of whiskey sat on the table. A third chair waited for her.")],
   sfx=[["Upscale restaurant murmur and soft piano", 4.0, 0.2, "start"]], music="tension", cut=True)
sc("steakhouse", ["jason", "michael", "emily:dinner"], "Jason standing with a polished smile as Emily arrives at the table; Michael seated.",
   [("JASON", "[smooth] Emily. Glad you came."),
    ("EMILY", "[cool] You said you wanted to apologize."),
    ("JASON", "We do. Both of us."),
    ("MICHAEL", "[awkward] We were jerks at the will reading.")])
sc("steakhouse", ["emily:dinner", "jason"], "Emily seated, unimpressed; Jason's smile tightening.",
   [("EMILY", "That's one way to put it."),
    ("JASON", "[sighs] Dad's death has been hard on everyone."),
    ("EMILY", "[pointed] Especially on the people who visited twice a year.")])
sc("steakhouse", ["jason"], "Jason sliding a leather folder with documents across the white tablecloth.",
   [(N, "Jason's smile tightened. He slid a folder across the table."),
    ("JASON", "[businesslike] A property transfer. You sign the house over, and when the company's back on its feet, we give you two hundred thousand dollars.")],
   sfx=[["A leather folder placed on a table", 1.0, 0.4, "start"]])
sc("steakhouse", ["emily:dinner"], "Emily looking at the folder, then raising an eyebrow at Jason.",
   [("EMILY", "[incredulous] You want a house worth almost a million dollars... for a promise of two hundred thousand?"),
    ("JASON", "It's a fair offer."),
    ("EMILY", "[sharp] Then why don't you sell one of your cars? Or the boat? Or the condo in Miami?")])
sc("steakhouse", ["jason", "emily:dinner"], "Jason slamming his hand on the table; diners at nearby tables turning to look.",
   [("JASON", "[slams the table, shouting] That's enough!"),
    (N, "Several diners turned to look. Emily didn't flinch.")],
   sfx=[["A hand slamming a table, glasses rattling, restaurant going quiet", 2.0, 0.45, "start"]])
sc("steakhouse", ["jason"], "Jason leaning across the table, jabbing a finger.",
   [("JASON", "[seething] You think you're clever because Whitaker's protecting you? Dad was confused. He barely knew what he was signing!"),
    ("EMILY", "[slowly] Interesting."),
    ("JASON", "What?")])
sc("steakhouse", ["emily:dinner"], "Close-up of Emily, calm, almost smiling.",
   [("EMILY", "[calm, deliberate] That's exactly what you told the accountant. When Dad asked about the consulting payments.")],
   sfx=[["Low tense musical sting", 2.0, 0.35, "start"]])
sc("steakhouse", ["michael"], "Michael freezing with his whiskey glass halfway to his mouth.",
   [(N, "Michael's glass stopped halfway to his mouth."),
    ("EMILY", "Northbridge Advisory. Registered to you, Michael. Meridian Strategic Partners. Registered to you, Jason. [pause] Eight hundred thousand dollars.")],
   sfx=[["A glass set down hard on a table", 1.0, 0.45, "end"]])
sc("steakhouse", ["michael", "jason"], "Michael's face gone gray; Jason leaning forward, dangerous.",
   [(N, "Michael's face went gray. Jason leaned forward."),
    ("JASON", "[low, dangerous] Where did you get those names?"),
    ("EMILY", "Dad kept records. He kept everything.")])
sc("steakhouse", ["jason", "emily:dinner"], "Emily standing up from the table, Jason glaring up at her.",
   [("JASON", "[threatening] You have no idea what you're doing."),
    ("EMILY", "[steady] You're right about one thing. I didn't know what I was doing for ten years, trying to hold this family together. [pause] But I know exactly what I'm doing now.")])
sc("steakhouse", ["jason", "emily:dinner"], "Emily turning to leave as Jason half rises from the booth.",
   [("JASON", "[barking] Sit down!"),
    ("EMILY", "No."),
    ("JASON", "[furious] Walk out that door and don't ever ask us for anything again.")])
sc("steakhouse", ["emily:dinner"], "Emily looking back over her shoulder with a small, cool smile.",
   [("EMILY", "[a small smile] Jason... that's the first offer you've made tonight that I actually like.")],
   sfx=[["Chair sliding back and heels walking away on a wooden floor", 3.0, 0.4, "end"]], motion="she turns and walks away from the table through the dim restaurant")

# ACT 8 - THE BOARDROOM
sc("boardroom", [], "A glass-walled boardroom high above Boston, a long table full of executives and lawyers in suits.",
   [(N, "Two weeks later, the boardroom of Carter Development Group was full. The board. The company's lawyers. Ms. Dana Reyes, from the bank that held nine million dollars of its debt.")],
   sfx=[["Conference room murmur, papers rustling", 3.0, 0.25, "start"]], music="tension", cut=True)
sc("boardroom", ["emily:board", "jason"], "Emily seated at the far end of the boardroom table; Jason entering and stopping short.",
   [(N, "And at the far end of the table... Emily."),
    ("JASON", "[angry] What is she doing here?"),
    ("WHITAKER", "Miss Carter found her father's ledger. As executor, I asked her to attend.")])
sc("boardroom", ["reyes"], "Ms. Reyes opening a thick report at the table, looking at Jason over it.",
   [("REYES", "[brisk] Let's begin. Mr. Carter, the forensic report shows eight hundred thousand dollars paid to two firms with no employees, no offices, and no work product. One registered to you. One to your brother.")])
sc("boardroom", ["jason", "reyes"], "Jason defensive; Ms. Reyes unimpressed.",
   [("JASON", "[defensive] Those were legitimate consulting fees."),
    ("REYES", "[flat] Then show me one contract. One invoice. One report they delivered.")],
   sfx=[["Tense silence in a large room, a clock ticking", 3.0, 0.25, "end"]])
sc("boardroom", ["michael"], "Michael reaching into his jacket and putting his phone on the table.",
   [(N, "Jason said nothing. And then Michael did something no one expected. He put his phone on the table."),
    ("MICHAEL", "[shaky, then firm] Jason set it up. All of it. The firms, the invoices. He told me Dad would never check.")])
sc("boardroom", ["jason", "michael"], "Jason turning on Michael in fury; Michael refusing to back down.",
   [("JASON", "[through his teeth] Michael. Shut up."),
    ("MICHAEL", "[panicked, loud] I have the emails. I'm not going down for you.")],
   sfx=[["Deep cinematic boom impact", 3.0, 0.4, "end"]])
sc("boardroom", ["jason"], "Jason turning white, gripping the edge of the table.",
   [(N, "[quietly] Jason turned white. Michael had warned Emily what his brother was capable of. He just never said what he himself was capable of.")])
sc("boardroom", ["reyes"], "Ms. Reyes closing the report with finality.",
   [("REYES", "[cold] Then we're done here. Effective today, the bank is calling the loans. And gentlemen... you each signed personal guarantees. The company's debt is now your debt.")])
sc("boardroom", ["michael", "reyes"], "Michael staring in horror; Ms. Reyes calm.",
   [("MICHAEL", "[horrified] Our... personal debt?"),
    ("REYES", "Your houses. Your cars. Your boat. Whatever it takes to cover two point four million dollars.")])
sc("boardroom", ["whitaker", "jason"], "Mr. Whitaker sliding one more page across the table to Jason.",
   [(N, "Mr. Whitaker slid one more page across the table."),
    ("WHITAKER", "[measured] The board voted this morning. Jason, you are removed as chief executive. Effective immediately. The findings go to the district attorney this afternoon.")],
   sfx=[["Deep cinematic boom with a low sub drop", 3.0, 0.45, "end"]])
sc("boardroom", ["jason", "emily:board"], "Jason turning to Emily, his face softened and desperate.",
   [(N, "Jason turned toward his sister. For the first time, his voice was soft."),
    ("JASON", "[pleading] Emily... we're your brothers. You can't let us lose everything.")])
sc("boardroom", ["emily:board"], "Emily looking at Jason calmly across the table.",
   [("EMILY", "[calm] I didn't take anything from you. You had twelve million dollars to run. I had one dollar. [pause] Remember?"),
    ("JASON", "[desperate] Emily, please.")])
sc("boardroom", ["emily:board"], "Close-up of Emily, eyes steady, voice controlled.",
   [("EMILY", "[controlled, hurt underneath] You laughed when Dad's will was read. You told me I wasn't worth a real inheritance. Then you tried to take the only home he left me.")])
sc("boardroom", [], "Close-up of a woman's hand placing a single one-dollar bill on the dark boardroom table.",
   [(N, "Emily opened her purse. She placed a single dollar bill on the table.")],
   sfx=[["Paper bill laid gently on a wooden table", 1.0, 0.45, "end"]], motion="a hand slowly sets a single dollar bill down on the table and withdraws")
sc("boardroom", ["michael", "emily:board"], "Michael staring at the dollar bill; Emily looking at her brothers.",
   [("MICHAEL", "[confused] What's that supposed to mean?"),
    ("EMILY", "[evenly] My inheritance. The one you thought was so funny. It's yours. One hundred percent."),
    ("JASON", "What are you doing?")])
sc("boardroom", ["emily:board"], "Emily standing, composed and powerful.",
   [("EMILY", "[firm] I won't sign over my house. I won't guarantee your debts. And I won't help you hide what you did to Dad's company. [pause] But you can keep the dollar. Consider it my contribution to your retirement.")])
sc("boardroom", ["jason"], "Jason opening his mouth, then closing it, defeated.",
   [(N, "[slowly] Jason opened his mouth. Then closed it. For once, there was nothing he could say that would make Emily smaller.")],
   sfx=[["Long tense silence in a large room", 3.0, 0.2, "start"]])
sc("boardroom", ["emily:board"], "Emily picking up her bag to leave.",
   [("EMILY", "Dad left you the company because you spent years insisting you deserved it. Now it's yours. All of it.")])
sc("boardroom", ["jason", "emily:board"], "Emily at the glass door, turning back to Jason who has stood up.",
   [(N, "She walked to the door."),
    ("JASON", "[shouting after her] Emily! You're really going to walk away from your own family?"),
    ("EMILY", "[quiet, final] No, Jason. I'm walking away from the people who kept walking all over me.")],
   sfx=[["A heavy glass door closing", 1.5, 0.45, "end"]], motion="she pushes through the glass door and walks away down the bright corridor")

# ACT 9 - THE LAST LETTER
sc("porch", ["emily:porch"], "Emily sitting on the porch steps with a cup of coffee, the maple tree blazing red, golden morning light.",
   [(N, "[warm, unhurried] Six months later, Emily sat on the porch of the Willow Street house. The maple tree had turned bright red. The garden was blooming again.")],
   music="wonder", sfx=[["Birds singing on a quiet autumn morning", 4.0, 0.25, "start"]], cut=True,
   motion="red maple leaves drift slowly down in the morning light")
sc("", [], "A shut-down corporate office lobby seen through a padlocked glass door, empty reception desk, dust sheets over the furniture, gray daylight. No signs, no lettering anywhere.",
   [(N, "Carter Development Group had been sold to pay its creditors. Jason's house, his boat, and the Miami condo went to the bank. He's awaiting trial on fraud charges.")])
sc("", ["michael"], "Michael alone in a small bare one-bedroom apartment, sitting on a mattress, looking at his phone.",
   [(N, "Michael is cooperating with prosecutors. He lives in a one-bedroom apartment now. [pause] Neither has called to apologize. And Emily no longer waits for the phone to ring.")])
sc("porch", ["sarah"], "Sarah walking up the driveway holding two coffee cups, smiling.",
   [("SARAH", "[cheerful] You ready?"),
    ("EMILY", "[smiling] Almost.")], sfx=[["Footsteps on a gravel driveway", 2.0, 0.35, "start"]])
sc("porch", ["sarah", "emily:porch"], "Emily and Sarah sitting together on the porch steps with coffee.",
   [(N, "Emily had gone back to work full-time, at a nonprofit that supports family caregivers. People like the woman she'd been for ten years."),
    ("SARAH", "[warm] You know, your dad would be proud of you."),
    ("EMILY", "[softly] I hope so.")])
sc("porch", ["sarah", "emily:porch"], "Sarah nudging Emily's shoulder affectionately.",
   [("SARAH", "You kept the house. You kept your head. And you didn't let them turn you into someone you're not."),
    ("EMILY", "[wistful] I still wish things had been different."),
    ("SARAH", "[gently] Of course you do.")])
sc("porch", ["emily:porch"], "Emily opening a cream envelope on the porch, a handwritten letter inside.",
   [(N, "That morning, Emily had finally opened the last envelope Mr. Whitaker gave her. She'd been too afraid to read it. [pause] Until now.")],
   sfx=[["Envelope tearing open and paper unfolding", 2.0, 0.45, "start"]])
sc("porch", [], "Close-up of an old man's shaky handwriting on cream letter paper, autumn leaves resting on it.",
   [("ROBERT", "[tender, slow] \"My sweet Emily. You once told me that home isn't a building. It's the place where someone is waiting for you. For ten years, you made sure I never came home to an empty house. [pause] Now I want you to have one of your own.\"")])
sc("willow_in", ["robert", "emily:home"], "A warm golden memory: Robert in his recliner laughing with Emily, years earlier, soft dreamy light.",
   [("ROBERT", "[gentle] \"I left your brothers the business because they wanted power. I left you the house because I wanted you to have peace. And I left you one dollar for a reason. Not because you were worth less. [pause] Because I wanted you to remember that your value was never what someone else chose to give you.\"")])
sc("porch", ["emily:porch"], "Close-up of Emily reading, tears on her cheeks, a smile forming.",
   [("ROBERT", "[voice thick with emotion] \"You gave me ten years of your life. Please don't spend the next ten trying to earn love you already had. Go live. Be happy. [pause] Your mother and I loved you long before there was anything to inherit.\"")],
   motion="a tear rolls down her cheek as she slowly begins to smile")
sc("porch", ["sarah", "emily:porch"], "Emily folding the letter, smiling through tears; Sarah beside her.",
   [(N, "Emily folded the letter. A tear rolled down her cheek. But this time, she was smiling."),
    ("SARAH", "[softly] You okay?"),
    ("EMILY", "[a small laugh through tears] Yeah. I think I finally am.")])
sc("willow_out", [], "The blue-shuttered house and the red maple tree at golden hour, wide and peaceful, the porch and yard completely empty, no people anywhere in the frame.",
   [(N, "[reflective] Her brothers inherited a company worth millions on paper. Along with its debts, its lies, and every consequence of their own choices. Emily inherited a modest house. A second chance. [pause] And something her brothers never understood. Freedom.")])
sc("willow_in", [], "A single one-dollar bill tucked into the corner of a framed photo of Emily and her father on a mantel, warm light.",
   [(N, "[slow, final] Sometimes karma doesn't arrive with a scream. Sometimes it arrives in a second envelope. And sometimes... the one who receives the least... walks away with the most."),
    (N, "[warm] This has been Karma Tales. Every betrayal has a price. And karma always collects.")])


def main():
    scenes, music, ambience = [], [], []
    for i, (place, chars, image, lines, extra) in enumerate(S, start=1):
        sid = f"s{i:02d}"
        scene = {"id": sid, "chars": chars, "image": image, "lines": [list(l) for l in lines]}
        if place:
            scene["place"] = place
        if extra.get("cut"):
            scene["cut"] = True
        if extra.get("sfx"):
            scene["sfx"] = extra["sfx"]
        if extra.get("motion"):
            scene["motion"] = extra["motion"]
        if extra.get("music"):
            music.append([sid, extra["music"]])
        scenes.append(scene)
    roles = {r.split("~")[0] for s in scenes for r, _ in s["lines"]}
    voices = {r: VOICES[r] for r in sorted(roles)}
    title = "My Brothers Inherited $12 Million. I Got $1."
    spec = {
        "title": "Karma Tales EP02 - The Second Envelope",
        "voices": voices,
        "cast": CAST,
        "portraits": {k: PORTRAIT + v for k, v in PORTRAITS.items()},
        "looks": LOOKS,
        "style": "Photorealistic still from a prestige American TV drama, shot on 35mm, cinematic lighting, shallow depth of field, natural skin texture, wide 16:9 frame. Keep every person's face and hair exactly consistent with their reference photo. No text, no captions, no watermark. ",
        "resolution": "2K",
        "music": music,
        "places": PLACES,
        "ambiences": {
            "office": ["Quiet office room tone with steady rain against tall windows, faint clock ticking", 0.07],
            "house": ["Quiet old house room tone, faint wind outside, a distant clock", 0.06],
            "rain": ["Steady rain against a kitchen window at night, quiet room", 0.09],
            "restaurant": ["Upscale restaurant ambience, low murmur of conversation, cutlery, soft piano far away", 0.07],
            "boardroom": ["Large quiet corporate room tone, faint air conditioning", 0.05],
            "outdoors": ["Gentle wind through trees and birdsong on a quiet street", 0.07],
        },
        "ambience": [],
        "scenes": scenes,
        "youtube": {
            "title": title,
            "description": "Her brothers inherited twelve million dollars. She got one. One single dollar. And when the lawyer read it out loud, they laughed.\n\nThen he opened a second envelope.\n\nFor ten years, Emily Carter took care of her father while her brothers stayed away. When his will left her one dollar, it looked like the final insult. It wasn't. It was the first move in a plan her father set up before he died.\n\nKarma Tales: revenge and twist stories where the people who scheme always get what they deserve.\n\nThis story is fiction. Any resemblance to real people or events is coincidental. Narration and images are AI-generated.\n\n#karmatales #revengestory #inheritance #familydrama",
            "tags": ["karma tales", "revenge story", "inheritance", "family drama", "will reading", "greedy siblings", "caregiver", "twist ending", "karma", "audio drama"],
            "category": "24",
            "shorts_description": f"Full story on Karma Tales: {title}\n\n#shorts #karmatales #revengestory #inheritance",
        },
        "thumbnail_file": "karma/ep02_thumb.jpg",
        "shorts": [
            {"id": "short1", "title": "Her brothers got $12 million.|She got $1.", "from": "s09", "to": "s19",
             "youtube_title": "Her Brothers Laughed When Dad Left Her $1. Then the Lawyer Kept Reading. #shorts"},
            {"id": "short2", "title": "He turned on his own brother|in front of the board", "from": "s98", "to": "s105",
             "youtube_title": "He Stole $800K From Their Dad's Company. His Brother Had the Emails. #shorts"},
            {"id": "short3", "title": "\"Consider it my contribution|to your retirement.\"", "from": "s106", "to": "s113",
             "youtube_title": "She Gave Her Greedy Brothers Her Entire Inheritance: $1 #shorts"},
        ],
    }
    # Room tone per place, switched at the first scene of each new place.
    tone = {"office": "office", "home": "house", "hospital": "house", "thanksgiving": "house", "willow_out": "outdoors",
            "willow_in": "house", "study": "house", "kitchen": "rain", "steakhouse": "restaurant", "boardroom": "boardroom", "porch": "outdoors"}
    last = None
    for s in scenes:
        key = tone.get(s.get("place", ""))
        if key and key != last:
            spec["ambience"].append([s["id"], key])
            last = key
    out = ROOT / "karma" / "ep02_full.json"
    out.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")
    words = sum(len(t.split()) for s in scenes for _, t in s["lines"])
    print(f"{out.name}: {len(scenes)} scenes, {words} words, {sum(1 for s in scenes if s.get('motion'))} moving clips")


if __name__ == "__main__":
    main()
