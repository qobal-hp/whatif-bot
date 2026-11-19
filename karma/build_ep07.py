"""Write karma/ep07_full.json, Karma Tales EP07 "The Empty Chair" (Thanksgiving special), from the user's 20-scene script.

usage: python karma/build_ep07.py
Polish over the draft: the cold open no longer plays as a first meeting (Evelyn and Anna have already met), Anna
visits the estate only on Thanksgiving, the intercepted letters pay off (Peter brings the originals, unopened),
Richard's and Michael's consequences land on screen, and Diane gets a turn at the end. eleven_v3 tags on every line.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

VOICES = {
    "NARRATOR": "FmtiHEcHpocK7YiZwa46",
    "EVELYN": "EVELYN_VOICE", "RICHARD": "RICHARD_VOICE", "MICHAEL": "MICHAEL_VOICE", "DIANE": "DIANE_VOICE",
    "CLAIRE": "CLAIRE_VOICE", "ANNA": "ANNA_VOICE", "PETER": "PETER_VOICE",
}
CASTING = ROOT / "karma" / "voices_ep07.json"
if CASTING.exists():
    VOICES.update(json.loads(CASTING.read_text()))

CAST = {c: f"karma/cast/ep07/{c}.jpg" for c in ["evelyn", "anna", "michael", "richard", "diane", "claire", "peter"]}

PORTRAIT = ("Photorealistic still from a prestige American TV drama, shot on 35mm, shallow depth of field, soft warm cinematic key light, "
            "natural skin texture, head-and-shoulders portrait facing slightly off camera, neutral dark background, an entirely "
            "fictional person who resembles no real celebrity, no text, no watermark. ")
PORTRAITS = {
    "diane": "Diane Whitmore, a 45-year-old American woman, wavy shoulder-length honey-blonde hair, blue eyes, tight composed mouth, small pearl drop earrings, deep plum wrap dress.",
    "claire": "Claire Whitmore, a 26-year-old American woman, light brown hair in a loose low ponytail, hazel eyes, a few freckles, thoughtful steady gaze, forest green sweater.",
    "peter": "Peter Hale, a 68-year-old American retired attorney, neat white hair and a trimmed white beard, wire-rimmed glasses, tired kind eyes, tweed jacket over a gray sweater.",
}

LOOKS = {
    "evelyn": "Evelyn (the silver-haired older woman from the reference photo, same face, in a deep burgundy knit wrap and pearl earrings)",
    "evelyn:day": "Evelyn (the silver-haired older woman from the reference photo, same face, in a camel wool coat over a cream blouse, pearl earrings)",
    "evelyn:home": "Evelyn (the silver-haired older woman from the reference photo, same face, in a soft gray cardigan, smiling gently)",
    "anna": "Anna (the brown-haired woman from the reference photo, same face, about 40, in a cream cable-knit sweater)",
    "anna:day": "Anna (the brown-haired woman from the reference photo, same face, about 40, in a navy wool coat and a scarf)",
    "anna:home": "Anna (the brown-haired woman from the reference photo, same face, about 40, relaxed and smiling, in a rust-colored sweater)",
    "richard": "Richard (the gray-haired older man from the reference photo, same face, in a dark charcoal suit jacket and open-collar shirt)",
    "richard:home": "Richard (the gray-haired older man from the reference photo, same face, in a navy cardigan over a collared shirt)",
    "michael": "Michael (the dark curly-haired bearded man from the reference photo, same face, in a dark brown sport coat over an open-collar shirt)",
    "michael:office": "Michael (the dark curly-haired bearded man from the reference photo, same face, in a white shirt and loosened navy tie)",
    "diane": "Diane (the honey-blonde woman from the reference photo, same face, in a deep plum dress)",
    "diane:home": "Diane (the honey-blonde woman from the reference photo, same face, in a camel coat, holding a pie dish)",
    "claire": "Claire (the young woman with light brown hair from the reference photo, same face, in a forest green sweater)",
    "peter": "Peter (the white-haired bearded man in glasses from the reference photo, same face, in a tweed jacket and gray sweater)",
}

PLACES = {
    "dining": "Setting: the grand formal dining room of an old New England family estate outside Boston on Thanksgiving evening, a long mahogany table with a roast turkey, candles, crystal glasses, autumn leaves and small pumpkins as decoration, tall windows with orange autumn trees outside, oil family portraits on dark wood-paneled walls.",
    "foyer": "Setting: the front entrance hall of an old New England family estate on Thanksgiving evening, a heavy dark wooden front door, a staircase, a chandelier, warm lamp light, autumn wreath.",
    "study": "Setting: a dark wood-paneled private study in an old New England estate, leather chairs, a heavy desk, shelves of books, a single green desk lamp, rain on the window.",
    "coffee": "Setting: a quiet cozy Boston coffee shop on a gray November afternoon, brick walls, rain-streaked window, warm pendant lights.",
    "anna_apt": "Setting: a small modest apartment in a Boston neighborhood, a kitchen table under a warm lamp, old shoe boxes and papers spread out, evening.",
    "kitchen": "Setting: a large warm farmhouse-style kitchen of an old New England estate on Thanksgiving afternoon, copper pots, pies cooling on the counter, steam, late golden light.",
    "hallway": "Setting: a dim upstairs hallway in an old New England estate, a door left half open with lamplight spilling out, old family photos along the wall.",
    "office": "Setting: a downtown Boston law office in the evening, campaign posters stacked against the wall, city lights through tall windows, a desk with files.",
    "porch": "Setting: the front steps and heavy wooden door of an old New England estate on a cold rainy autumn evening twenty-four years ago, porch light glowing, wet stone steps.",
    "hospital": "Setting: a 1980s hospital maternity room, pale green walls, a window with gray winter light, a hospital bed and a small bassinet.",
    "diner": "Setting: a quiet small-town diner on Thanksgiving night, red vinyl booths, a long counter, neon sign in the window, almost empty, warm light.",
    "law_office": "Setting: a bright modern Boston law office conference room in spring, glass walls, a long table with document binders, sunlight.",
    "cottage": "Setting: a small cozy cottage dining room and kitchen on Thanksgiving, mismatched chairs around a wooden table, a roast turkey, candles, string lights, autumn branches in a jar, warm and lived-in.",
    "estate_empty": "Setting: the same grand formal dining room of the old New England estate on Thanksgiving night one year later, the long mahogany table almost empty, only a few candles, dark and silent.",
}

N = "NARRATOR"
S = []


def sc(place, chars, image, lines, **extra):
    S.append((place, chars, image, lines, extra))


# SCENE 01 - COLD OPEN: THE EMPTY CHAIR
sc("dining", [], "A long candlelit Thanksgiving table seen from the end, a family seated, one carved chair empty with a full place setting.",
   [(N, "[low, deliberate] Every Thanksgiving, Evelyn Whitmore set the table for her family. [pause] This year, she set one extra place.")],
   sfx=[["Thanksgiving dinner, cutlery, glasses clinking, quiet conversation in a large dining room", 4.0, 0.3, "start"]], music="tension")
sc("dining", ["michael"], "Michael at the table, frowning at the empty chair beside him.",
   [("MICHAEL", "[light, puzzled] Mom... why is there an extra chair?"),
    ("EVELYN", "[calm, quiet] Because someone's missing.")])
sc("dining", ["diane"], "Diane glancing around the table with a tight smile.",
   [("DIANE", "[brisk, a little impatient] Everyone's here."),
    ("EVELYN", "[softly, firm] No, Diane. Everyone isn't.")])
sc("dining", ["richard"], "Richard at the head of the table, setting down his glass very slowly.",
   [("RICHARD", "[low warning] Evelyn. [pause] Don't start.")])
sc("dining", ["claire"], "Claire leaning toward her grandmother, curious and uneasy.",
   [("CLAIRE", "[gently] Grandma? Who are we waiting for?"),
    ("EVELYN", "[steady] Your aunt.")],
   sfx=[["A silver fork dropping onto a china plate", 1.0, 0.5, "end"]])
sc("dining", ["michael"], "Michael staring at his mother, half laughing.",
   [("MICHAEL", "[a short disbelieving laugh] What aunt?")])
sc("dining", ["evelyn"], "Evelyn at the table in candlelight, hands folded, looking straight at her husband.",
   [("EVELYN", "[slow, every word weighed] The daughter your grandfather made me give away... forty years ago.")],
   sfx=[["Sudden silence in a large room, a clock ticking", 2.5, 0.25, "start"]])
sc("dining", ["richard", "diane"], "Richard rigid at the head of the table; Diane staring at her mother, stunned.",
   [("RICHARD", "[sharp] That's enough."),
    ("DIANE", "[shaken] Mom, what are you talking about?"),
    ("EVELYN", "[tender] Her name is Anna.")])
sc("dining", ["michael", "evelyn"], "Michael leaning toward Evelyn, voice dropping.",
   [("MICHAEL", "[too quickly] You never had another daughter."),
    ("EVELYN", "[quiet, certain] Yes, Michael. I did.")])
sc("dining", ["richard"], "Richard's face hard in the candlelight.",
   [("RICHARD", "[cold] You're embarrassing yourself."),
    ("EVELYN", "[quiet fury] No, Richard. I've spent forty years embarrassing myself... pretending she never existed.")])
sc("foyer", [], "The heavy front door of the estate from inside, a silhouette behind its frosted glass.",
   [(N, "[low] Then the doorbell rang.")],
   sfx=[["An old deep doorbell chiming through a large house", 2.0, 0.5, "start"]])
sc("dining", ["richard", "claire"], "Claire half rising from her chair; Richard pointing at her.",
   [("CLAIRE", "I'll get it."),
    ("RICHARD", "[hard, commanding] Nobody opens that door."),
    ("EVELYN", "[gentle] Claire, sweetheart. Please.")])
sc("foyer", ["claire", "anna:day"], "Claire opening the heavy front door; Anna on the step in a navy coat, autumn wind behind her.",
   [("ANNA", "[nervous, polite] Hello. I'm Anna Morgan."),
    ("CLAIRE", "[breath catching, almost a whisper] Oh my God. [pause] You have her eyes.")],
   sfx=[["Heavy front door opening, autumn wind and leaves", 2.0, 0.45, "start"]], motion="the door swings open and wind lifts Anna's scarf")
sc("foyer", ["evelyn", "anna:day"], "Evelyn walking into the foyer, reaching out both hands to Anna.",
   [("EVELYN", "[warm, trembling] You came."),
    ("ANNA", "[small, unsure] You asked me to.")])
sc("foyer", ["richard"], "Richard appearing in the dining room doorway behind them, blocking it.",
   [("RICHARD", "[icy] She isn't staying.")])
sc("foyer", ["anna:day"], "Close-up of Anna looking past Evelyn, straight at Richard, very calm.",
   [("ANNA", "[calm, measured] Actually, Mr. Whitmore... before I leave, there's something your family should know. [pause] I've been inside this house before. [pause] You opened the door.")],
   sfx=[["Deep dramatic musical sting", 2.0, 0.45, "end"]])
sc("foyer", ["richard"], "Close-up of Richard, the color draining from his face.",
   [(N, "[slow] To understand what she meant... we have to go back three weeks. [pause] To a phone call Evelyn had waited forty years for.")],
   sfx=[["Low sustained tone fading out", 3.0, 0.3, "start"]])

# SCENE 02 - THREE WEEKS EARLIER: THE CALL
sc("kitchen", ["evelyn:home"], "Three weeks earlier: Evelyn alone in the big kitchen in the morning, answering an old wall phone.",
   [(N, "Three weeks earlier."),
    ("EVELYN", "[pleasant, distracted] Hello?"),
    ("ANNA~phone", "[nervous] Is this Evelyn Whitmore?"),
    ("EVELYN", "Speaking.")],
   sfx=[["Old landline phone ringing in a quiet kitchen", 2.5, 0.4, "start"]], music="wonder", cut=True)
sc("anna_apt", ["anna:home"], "Anna at her small kitchen table, phone at her ear, an old yellowed envelope in her other hand.",
   [("ANNA", "[taking a breath] My name is Anna Morgan.")],
   sfx=[["Silence on a phone line", 2.0, 0.2, "end"]])
sc("kitchen", ["evelyn:home"], "Evelyn gripping the edge of the counter, frozen.",
   [("EVELYN", "[faint] I'm sorry... could you repeat that?"),
    ("ANNA~phone", "[gently] Anna Morgan. [pause] I believe you may be my biological mother.")])
sc("kitchen", ["evelyn:home"], "Close-up of Evelyn's hand trembling on the phone cord.",
   [("EVELYN", "[barely] Who gave you this number?"),
    ("ANNA~phone", "I found an old letter among my adoptive mother's things.")])
sc("anna_apt", [], "Close-up of an old handwritten letter on yellowed paper, addressed 'To my baby, Anna'.",
   [("EVELYN~phone", "[whisper] What did it say?"),
    ("ANNA", "[reading, voice soft] I did not leave you because I didn't love you.")])
sc("kitchen", ["evelyn:home"], "Evelyn sliding down to sit on a kitchen stool, hand over her mouth.",
   [("ANNA~phone", "[worried] Mrs. Whitmore?"),
    ("EVELYN", "[breaking, a whisper] I wrote that.")],
   sfx=[["A sharp breath catching, then silence", 1.5, 0.3, "start"]])
sc("anna_apt", ["anna:home"], "Anna pressing the letter to her chest, eyes filling.",
   [("ANNA", "[shaking] Then it's true?"),
    ("EVELYN~phone", "[through tears] Yes."),
    ("ANNA", "[crying softly] I've waited forty years to hear someone say that.")])
sc("kitchen", ["evelyn:home"], "Evelyn wiping her eyes, glancing toward the kitchen door.",
   [("EVELYN", "[urgent, low] Anna, there's so much I need to tell you."),
    ("ANNA~phone", "[steadier] Then tell me why you gave me away."),
    ("EVELYN", "Not over the telephone.")])
sc("kitchen", [], "No people visible. An empty kitchen doorway from inside the quiet kitchen, only the long dark shadow of a man falling across the hallway floor beyond it.",
   [("ANNA~phone", "[confused] Why not?"),
    ("EVELYN", "[very quiet] Because the man who made me do it... is still living in my house.")],
   sfx=[["Footsteps passing in a hallway", 2.0, 0.35, "start"]])

# SCENE 03 - THE PERFECT IMAGE
sc("dining", ["diane:home", "evelyn:home"], "Days later: Diane arranging place cards on the long dining table, Evelyn folding napkins.",
   [("DIANE", "[brisk, managing] Mother, the caterers arrive at four on Thanksgiving."),
    ("EVELYN", "I know."),
    ("DIANE", "And please don't invite any more of your old friends.")],
   sfx=[["Plates and silverware being arranged", 3.0, 0.3, "start"]], music="tension", cut=True)
sc("dining", ["evelyn:home"], "Evelyn calmly folding a napkin.",
   [("EVELYN", "[mild] I invited one guest."),
    ("DIANE", "[sharp] Who?"),
    ("EVELYN", "Someone important.")])
sc("dining", ["diane:home"], "Diane holding a place card with the name of the governor's wife, eyebrows raised.",
   [("DIANE", "[dry] More important than the governor's wife?"),
    ("EVELYN", "[a small smile] Considerably."),
    ("DIANE", "[exasperated] Mother.")])
sc("dining", ["evelyn:home"], "Evelyn setting the napkin down, looking at her daughter.",
   [("EVELYN", "[tired] Diane, when did Thanksgiving become a networking event?"),
    ("DIANE", "[flat] When Michael started running for district attorney.")])
sc("dining", ["diane:home", "evelyn:home"], "Mother and daughter facing each other across the table.",
   [("EVELYN", "[pointed] So the entire family must pretend to be perfect?"),
    ("DIANE", "[defensive] We're not pretending."),
    ("EVELYN", "[softly] Aren't we?")])
sc("dining", ["richard:home"], "Richard walking in, reading glasses in hand, eyeing the place cards.",
   [("RICHARD", "[pleasant] What's all this?"),
    ("DIANE", "[tattling] Mother invited a mystery guest."),
    ("RICHARD", "[still pleasant] Who?")],
   sfx=[["Footsteps on hardwood, door opening", 1.5, 0.35, "start"]])
sc("dining", ["evelyn:home"], "Evelyn meeting her husband's eyes without blinking.",
   [("EVELYN", "[evenly] Someone I should have invited years ago."),
    ("RICHARD", "[the smile gone] Evelyn."),
    ("EVELYN", "[same tone] Richard.")])
sc("dining", ["richard:home"], "Richard holding the door open to the hall, jaw tight.",
   [("RICHARD", "[quiet, controlled] We need to talk. [pause] Privately.")])

# SCENE 04 - THE WARNING
sc("study", ["richard:home", "evelyn:home"], "Richard shutting the heavy study door, turning on his silver-haired wife Evelyn under the green desk lamp; nobody else in the room.",
   [("RICHARD", "[low, furious] Tell me you haven't contacted that woman.")],
   sfx=[["Heavy study door closing, rain on the window", 3.0, 0.4, "start"]], music="tension", cut=True)
sc("study", ["evelyn:home"], "Evelyn alone by the rainy study window, arms folded, the green desk lamp beside her.",
   [("EVELYN", "[cool] Her name is Anna."),
    ("RICHARD", "[snapping] I know her name."),
    ("EVELYN", "[cutting] You haven't spoken it in forty years.")])
sc("study", ["richard:home"], "Richard pouring a whiskey, not looking at her.",
   [("RICHARD", "[dismissive] Because we agreed to put it behind us."),
    ("EVELYN", "[voice rising] You agreed. [pause] I cried until I couldn't breathe.")])
sc("study", ["richard:home", "evelyn:home"], "The two of them facing each other across the dark study.",
   [("RICHARD", "[righteous] We were protecting the family."),
    ("EVELYN", "[incredulous] From a newborn baby?"),
    ("RICHARD", "[hard] From a scandal that would have destroyed everything."),
    ("EVELYN", "[quiet] You destroyed something anyway.")])
sc("study", ["richard:home"], "Richard swirling his glass, contemptuous.",
   [("RICHARD", "[sneering] She's probably after money."),
    ("EVELYN", "She hasn't asked for a penny."),
    ("RICHARD", "[knowing] They always start that way.")])
sc("study", ["evelyn:home"], "Evelyn stepping closer, eyes bright.",
   [("EVELYN", "[fierce] You don't know her."),
    ("RICHARD", "[cold] Neither do you.")],
   sfx=[["Rain on the window, silence", 2.0, 0.25, "start"]])
sc("study", ["richard:home"], "Richard leaning on the desk, voice dropping to a threat.",
   [("RICHARD", "[very low] If you bring her into this house... you will regret it.")])
sc("study", ["evelyn:home"], "Close-up of Evelyn, tears standing in her eyes, chin up.",
   [("EVELYN", "[quiet, steady] I've regretted something every Thanksgiving for forty years."),
    ("RICHARD", "What?"),
    ("EVELYN", "[breaking softly] Setting a table without my daughter.")])

# SCENE 05 - THE FIRST MEETING
sc("coffee", ["anna:day"], "Anna alone at a corner table in a rainy coffee shop, both hands around a cup, watching the door.",
   [(N, "[soft] They met for the first time in a coffee shop in Boston. [pause] Anna had arrived forty minutes early.")],
   sfx=[["Quiet coffee shop, espresso machine, rain outside", 4.0, 0.3, "start"]], music="wonder", cut=True)
sc("coffee", ["evelyn:day", "anna:day"], "Evelyn sitting down across from Anna, neither knowing what to do with their hands.",
   [("ANNA", "[nervous laugh] I almost didn't come."),
    ("EVELYN", "[gently] Why?"),
    ("ANNA", "[quiet] I thought you might look at me... and change your mind.")])
sc("coffee", ["evelyn:day"], "Evelyn looking at Anna as if memorizing her face.",
   [("EVELYN", "[immediately] Never."),
    ("ANNA", "[guarded] You don't know me."),
    ("EVELYN", "[aching] No. And that's my greatest regret.")])
sc("coffee", ["anna:day"], "Anna turning her cup slowly.",
   [("ANNA", "[warm] My adoptive parents were wonderful."),
    ("EVELYN", "[sincerely] I'm glad."),
    ("ANNA", "[softer] My mother died last spring.")])
sc("coffee", ["anna:day"], "Anna reaching into her bag.",
   [("EVELYN", "[gently] I'm so sorry."),
    ("ANNA", "Before she died, she told me she'd kept something from me."),
    ("EVELYN", "The letter?"),
    ("ANNA", "[setting it down] And a photograph.")],
   sfx=[["A photograph sliding across a wooden table", 1.0, 0.45, "start"]])
sc("coffee", [], "Close-up of a faded 1980s photograph on the table: a young dark-haired woman in a hospital bed holding a newborn wrapped in a pink blanket.",
   [("EVELYN", "[a whisper] That's me."),
    ("ANNA", "You're holding a baby."),
    ("EVELYN", "[barely] You.")])
sc("coffee", ["anna:day"], "Anna alone in frame at the coffee shop table, her composure cracking, an empty chair behind her.",
   [("ANNA", "[voice catching] I thought you never wanted me."),
    ("EVELYN", "[urgent, tender] Anna, I held you for three days.")])
sc("hospital", [], "Flashback, forty years ago: a young dark-haired mother in a hospital bed cradling a newborn, gray winter light, the door opening behind her.",
   [("ANNA", "[stunned] Three days?"),
    ("EVELYN", "[remembering, hollow] Then Richard came to the hospital... with an attorney.")],
   sfx=[["Soft hospital room tone, a door opening", 3.0, 0.3, "start"]], motion="the young mother looks up from the baby as the door opens")
sc("coffee", ["evelyn:day"], "Evelyn staring at the photo, back in that room.",
   [("ANNA", "[quiet] What did they tell you?"),
    ("EVELYN", "[flat with old pain] That if I kept you... I'd lose Michael and Diane.")])
sc("coffee", ["anna:day"], "Anna leaning in, disbelieving.",
   [("ANNA", "Your other children?"),
    ("EVELYN", "Yes."),
    ("ANNA", "[horrified] He threatened to take them?"),
    ("EVELYN", "[quietly] He said he'd make sure I never saw them again.")])
sc("coffee", ["evelyn:day"], "Close-up of Evelyn, ashamed.",
   [("ANNA", "[searching] And you believed him?"),
    ("EVELYN", "[low] I was thirty-four, frightened, and I didn't have a dollar of my own.")])
sc("coffee", ["anna:day"], "Anna's eyes hardening slightly, hurt.",
   [("ANNA", "[sharper] You could have found me later."),
    ("EVELYN", "I tried."),
    ("ANNA", "When?"),
    ("EVELYN", "[simply] Every year.")])
sc("coffee", ["anna:day"], "Close-up of Anna alone in frame, tears spilling over, the rainy window behind her.",
   [("ANNA", "[breaking] Then why did nobody ever come?")],
   sfx=[["Rain on the window, silence", 2.5, 0.25, "start"]])
sc("coffee", ["evelyn:day", "anna:day"], "Evelyn reaching across the table and taking Anna's hand.",
   [("EVELYN", "[soft] You can call me Evelyn. [pause] But I hope... someday... you'll call me Mom."),
    ("ANNA", "[a wet half laugh] Let's start with Evelyn.")])

# SCENE 06 - THE LETTERS
sc("anna_apt", ["evelyn:day", "anna:home"], "A week later in Anna's small apartment: Evelyn setting a worn shoe box on the kitchen table.",
   [("EVELYN", "[careful] These are copies."),
    ("ANNA", "Copies of what?"),
    ("EVELYN", "[quiet] Letters I wrote to you.")],
   sfx=[["Small apartment, a box lid lifted, papers rustling", 3.0, 0.35, "start"]], music="wonder", cut=True)
sc("anna_apt", [], "No faces visible. Overhead close-up of a shoe box on a kitchen table overflowing with handwritten letters, birthday cards and Christmas cards, all addressed to Anna, two pairs of hands, one older, lifting them out.",
   [("ANNA", "[overwhelmed] There are so many."),
    ("EVELYN", "Forty birthdays. [pause] Forty Christmases.")],
   motion="hands slowly lift a stack of old letters out of the shoe box")
sc("anna_apt", ["anna:home"], "Anna reading one card, her hand over her mouth.",
   [("ANNA", "[whisper] You wrote every year?"),
    ("EVELYN", "Sometimes more."),
    ("ANNA", "[confused] Why didn't you send them?")])
sc("anna_apt", ["evelyn:day"], "Evelyn shaking her head slowly.",
   [("EVELYN", "[firm] I did. [pause] Through the adoption agency. They wrote back that contact wasn't permitted."),
    ("ANNA", "[stunned] My parents said nobody ever contacted them.")])
sc("anna_apt", ["evelyn:day"], "Close-up of Evelyn's face going still and cold.",
   [("EVELYN", "[very quiet] Then someone lied.")],
   sfx=[["Low ominous tone", 2.0, 0.3, "end"]])
sc("anna_apt", ["anna:home"], "Anna setting the card down, hesitating.",
   [("ANNA", "[hesitant] Evelyn... there's something else."),
    ("EVELYN", "What?"),
    ("ANNA", "[quiet] I came to your house. When I was sixteen.")])
sc("porch", [], "Flashback: a sixteen-year-old girl with long brown hair in a rain jacket standing on the wet stone steps of the estate, ringing the bell.",
   [("ANNA", "[remembering] My father found an old address. I took two buses in the rain. I wanted to know if it was yours.")],
   sfx=[["Rain on stone steps, a doorbell", 3.0, 0.4, "start"]], motion="the teenage girl reaches up and rings the bell in the rain")
sc("porch", [], "Flashback: the front door opening; a tall man in his fifties with dark-gray hair in the doorway, looking down at the teenage girl.",
   [("EVELYN", "[barely] What happened?"),
    ("ANNA", "A man answered the door."),
    ("EVELYN", "[closing her eyes] Richard.")])
sc("anna_apt", ["anna:home"], "Anna looking down at her hands.",
   [("ANNA", "[steady but hurt] He said you knew about me. [pause] He said you'd paid him to make sure I never came back.")],
   sfx=[["Silence, a ticking kitchen clock", 2.5, 0.25, "start"]])
sc("anna_apt", ["evelyn:day"], "Evelyn with both hands pressed to her chest, devastated.",
   [("EVELYN", "[breaking] Oh, Anna..."),
    ("ANNA", "[quiet] I believed him."),
    ("EVELYN", "[fierce through tears] I never said that.")])
sc("anna_apt", ["anna:home"], "Anna reaching for an old envelope at the bottom of her bag.",
   [("ANNA", "[softly] I know that now."),
    ("EVELYN", "How?"),
    ("ANNA", "[deliberate] Because I still have what he gave me.")])

# SCENE 07 - THE CHECK
sc("anna_apt", [], "Close-up of an old personal check, never cashed, five thousand dollars, a bold signature 'Richard Whitmore'.",
   [("ANNA", "[quiet] He handed me this. At the door."),
    ("EVELYN", "[disbelief] A check?"),
    ("ANNA", "Five thousand dollars.")],
   sfx=[["An old envelope being opened", 1.5, 0.4, "start"]], music="tension")
sc("anna_apt", ["evelyn:day"], "Evelyn staring at the check.",
   [("EVELYN", "[hollow] Richard's signature."),
    ("ANNA", "[simply] I never cashed it."),
    ("EVELYN", "Why not?")])
sc("anna_apt", ["anna:home"], "Close-up of Anna, calm and wounded.",
   [("ANNA", "[quiet, steady] I wanted a mother. [pause] Not money.")],
   sfx=[["Silence", 2.0, 0.2, "start"]])
sc("anna_apt", ["evelyn:day"], "Evelyn holding the old check in trembling fingers.",
   [("EVELYN", "[faint] May I hold it?"),
    ("ANNA", "Of course."),
    ("EVELYN", "[low, shaking] I knew he could be cruel.")])
sc("anna_apt", ["evelyn:day"], "Close-up of Evelyn, anger rising through the grief.",
   [("ANNA", "[gently] Evelyn—"),
    ("EVELYN", "[voice hardening] But I never imagined he'd look into my daughter's face... and tell her I didn't want her.")])
sc("anna_apt", ["anna:home", "evelyn:day"], "Evelyn folding the check back into its envelope and handing it to Anna with resolve.",
   [("ANNA", "[small] What happens now?"),
    ("EVELYN", "[decided] Now you come to Thanksgiving."),
    ("ANNA", "[worried] He won't want me there."),
    ("EVELYN", "[iron] For once, Richard doesn't get to decide who belongs in this family.")])

# SCENE 08 - MICHAEL'S SECRET
sc("office", ["michael:office"], "Michael alone in his law office at night, campaign posters reading 'Whitmore for D.A.' stacked against the wall, phone buzzing.",
   [("MICHAEL", "[distracted] Dad?"),
    ("RICHARD~phone", "[grim] Your mother has found Anna.")],
   sfx=[["Phone vibrating on a desk, quiet office at night", 2.5, 0.4, "start"]], music="tension", cut=True)
sc("office", ["michael:office"], "Close-up of Michael, utterly still.",
   [("MICHAEL", "[quiet] I know.")],
   sfx=[["Silence, distant city traffic", 2.0, 0.2, "start"]])
sc("study", ["richard:home"], "Richard in his dark study, phone at his ear, frowning.",
   [("RICHARD", "[sharp] What did you say?"),
    ("MICHAEL~phone", "[flat] I know who she is."),
    ("RICHARD", "How?")])
sc("office", ["michael:office"], "Michael loosening his tie, leaning back in his chair.",
   [("MICHAEL", "[matter-of-fact] She contacted me two years ago."),
    ("RICHARD~phone", "[stunned] And you didn't tell me?"),
    ("MICHAEL", "[smooth] I handled it.")])
sc("study", ["richard:home"], "Richard setting down his whiskey.",
   [("RICHARD", "[cold] Define handled."),
    ("MICHAEL~phone", "I told her the family wasn't interested."),
    ("RICHARD", "[satisfied] Good.")])
sc("office", ["michael:office"], "Michael spinning a pen, avoiding his own reflection in the dark window.",
   [("MICHAEL", "[casual] I also told her Mother was in poor health. [pause] Too confused to understand who she was."),
    ("RICHARD~phone", "Why?"),
    ("MICHAEL", "[cool] Because I didn't want her showing up.")])
sc("study", ["richard:home"], "Richard pacing in the study.",
   [("RICHARD", "[pressing] Did you give her money?"),
    ("MICHAEL~phone", "No."),
    ("RICHARD", "Then we're fine.")])
sc("office", ["michael:office"], "Michael sitting forward, worried for the first time.",
   [("MICHAEL", "[tense] We're not fine. [pause] She has documents."),
    ("RICHARD~phone", "[alarmed] What documents?"),
    ("MICHAEL", "[frustrated] I don't know.")])
sc("study", ["richard:home"], "Close-up of Richard, eyes narrowed.",
   [("RICHARD", "[hard] Find out."),
    ("MICHAEL~phone", "[exasperated] Dad, I'm in the middle of an election campaign."),
    ("RICHARD", "[icy] Then you'd better make sure this family doesn't become tomorrow's headline.")],
   sfx=[["Phone hanging up", 1.0, 0.4, "end"]])

# SCENE 09 - CLAIRE OVERHEARS
sc("hallway", ["claire"], "Thanksgiving morning: Claire on the dim upstairs landing, stopping outside a half-open door, lamplight and voices spilling out.",
   [("MICHAEL", "[urgent, hushed, from inside] Diane, listen to me.")],
   sfx=[["Old house hallway, muffled voices behind a door", 3.0, 0.3, "start"]], music="tension", cut=True)
sc("hallway", ["michael", "diane"], "Through the gap in the door: Michael and Diane arguing in low voices in a guest bedroom.",
   [("DIANE", "[shocked] You knew about Anna?"),
    ("MICHAEL", "[hissing] Keep your voice down."),
    ("DIANE", "[incredulous] For two years?")])
sc("hallway", ["michael"], "Michael pacing, rubbing his forehead.",
   [("MICHAEL", "[defensive] I was protecting Mom."),
    ("DIANE", "[disgusted] From her own daughter?"),
    ("MICHAEL", "[sharp] From a woman who could destroy this family.")])
sc("hallway", ["diane"], "Diane staring at her brother.",
   [("DIANE", "[cold] Do you hear yourself?"),
    ("MICHAEL", "[low] Think about what happens if she starts asking questions."),
    ("DIANE", "About what?")])
sc("hallway", ["michael"], "Close-up of Michael, voice dropping further.",
   [("MICHAEL", "[barely audible] The adoption. Dad's business. [pause] The money."),
    ("DIANE", "[confused] What money?")],
   sfx=[["An old floorboard creaking loudly", 1.0, 0.5, "end"]])
sc("hallway", ["michael"], "Michael spinning toward the door.",
   [("MICHAEL", "[sharp] Who's there?"),
    ("CLAIRE", "[quiet] It's me.")],
   sfx=[["Door swinging open", 1.0, 0.4, "start"]])
sc("hallway", ["claire"], "Claire in the doorway, arms crossed, chin up.",
   [("MICHAEL", "[forced calm] Claire. How much did you hear?"),
    ("CLAIRE", "[steady] Enough.")])
sc("hallway", ["michael"], "Michael pointing a finger at his daughter.",
   [("MICHAEL", "[warning] This doesn't concern you."),
    ("CLAIRE", "[hurt, disbelieving] You lied to Grandma."),
    ("MICHAEL", "[dismissive] You don't understand.")])
sc("hallway", ["claire"], "Close-up of Claire, eyes bright with anger.",
   [("CLAIRE", "[challenging] Then explain it."),
    ("MICHAEL", "[cold] Stay out of it."),
    ("CLAIRE", "[quiet, devastating] That's what everyone in this family says... whenever they're hiding something.")])

# SCENE 10 - THE SECOND BETRAYAL
sc("kitchen", ["evelyn", "claire"], "Thanksgiving afternoon in the steamy kitchen: Evelyn basting the turkey, Claire hovering at her elbow.",
   [("CLAIRE", "[nervous] Grandma, can we talk?"),
    ("EVELYN", "[warm, busy] Of course, sweetheart.")],
   sfx=[["Busy kitchen, oven door, sizzling, a timer ticking", 3.0, 0.35, "start"]], music="wonder", cut=True)
sc("kitchen", ["claire"], "Claire biting her lip, then blurting it out.",
   [("CLAIRE", "[rushed, quiet] Dad knew about Anna."),
    ("EVELYN", "[freezing] What?"),
    ("CLAIRE", "She contacted him two years ago.")])
sc("kitchen", ["evelyn"], "Evelyn slowly setting down the baster.",
   [("EVELYN", "[faint] Are you sure?"),
    ("CLAIRE", "[sad] I heard him say it.")],
   sfx=[["Kitchen noise fading to silence", 2.0, 0.25, "start"]])
sc("kitchen", ["evelyn"], "Close-up of Evelyn, staring at nothing.",
   [("EVELYN", "[hollow] Two years."),
    ("CLAIRE", "[gently] Grandma, I'm sorry."),
    ("EVELYN", "[remembering] I called him on my birthday that year.")])
sc("kitchen", ["evelyn"], "Evelyn gripping the edge of the counter, voice cracking.",
   [("EVELYN", "[cracking] I told him I'd been dreaming about a little girl again. [pause] He said I should stop living in the past.")])
sc("kitchen", ["claire"], "Claire wiping her eyes.",
   [("CLAIRE", "[whisper] He knew."),
    ("EVELYN", "[quiet] Yes."),
    ("CLAIRE", "What are you going to do?")])
sc("kitchen", ["evelyn"], "Evelyn taking one extra china plate down from a high cabinet.",
   [("EVELYN", "[calm, resolved] Set another plate."),
    ("CLAIRE", "[confused] That's it?"),
    ("EVELYN", "[a small, dangerous smile] No. [pause] That's where it begins.")],
   motion="she lifts an extra china plate down from the cabinet")
sc("kitchen", ["evelyn"], "Evelyn at the kitchen phone, speaking quietly with her back to the door.",
   [(N, "[low] Before dinner, Evelyn made one more phone call. [pause] To a man she hadn't spoken to in forty years.")],
   sfx=[["Rotary-style phone dialing", 1.5, 0.35, "start"]])

# SCENE 11 - THE THANKSGIVING DINNER (back to the cold open)
sc("dining", [], "The long Thanksgiving table at dusk, candles lit, the family seated, the empty chair waiting.",
   [(N, "[measured] Which brings us back to Thanksgiving dinner."),
    ("DIANE", "[polite] The turkey looks beautiful."),
    ("RICHARD", "[impatient] Let's eat before it gets cold.")],
   sfx=[["Thanksgiving dinner, quiet conversation, glasses", 3.0, 0.3, "start"]], music="tension", cut=True)
sc("dining", ["michael"], "Michael raising his glass toward his father.",
   [("MICHAEL", "[smooth] Dad, perhaps you should say grace."),
    ("EVELYN", "[quiet] I'll do it.")],
   sfx=[["Chairs shifting, a hush", 1.5, 0.3, "start"]])
sc("dining", ["evelyn"], "Evelyn with her eyes closed and hands folded at the candlelit table, everyone's heads bowed.",
   [("EVELYN", "[slow, deliberate] Dear God, thank you for bringing this family together. [pause] For the food on our table. For the people we love. [pause] And for the chance to tell the truth... before it's too late.")])
sc("dining", ["richard"], "Richard opening his eyes and staring hard at his wife.",
   [("RICHARD", "[clipped] Amen."),
    ("EVELYN", "[calm] Amen.")],
   sfx=[["Silence, a clock ticking", 2.0, 0.2, "start"]])
sc("foyer", [], "The front door from inside, the doorbell button glowing, Claire hurrying across the foyer.",
   [(N, "[low] And the conversation went exactly as Evelyn knew it would. [pause] Until the doorbell rang."),
    ("CLAIRE", "[from the hall] She's here.")],
   sfx=[["An old deep doorbell chiming", 2.0, 0.5, "start"]])

# SCENE 12 - THE UNINVITED GUEST
sc("dining", ["evelyn", "anna"], "Evelyn leading Anna, coat now off, into the candlelit dining room, every head turning.",
   [("EVELYN", "[warm, proud] Everyone. This is Anna. Come in, sweetheart.")],
   music="tension")
sc("dining", ["richard"], "Richard rising from the head of the table.",
   [("RICHARD", "[icy] I said she isn't welcome."),
    ("EVELYN", "[without turning] You don't get to decide that.")])
sc("dining", ["michael"], "Michael standing, hands raised, his campaign smile on.",
   [("MICHAEL", "[reasonable, tight] Mom, can we please discuss this privately?")])
sc("dining", ["anna", "michael"], "Anna and Michael looking at each other across the table, recognition in both faces.",
   [("ANNA", "[quiet] Hello, Michael."),
    ("MICHAEL", "[stiff] Anna."),
    ("DIANE", "[confused] You two... know each other?")])
sc("dining", ["anna"], "Anna turning to Diane, voice steady.",
   [("ANNA", "[calm] He told me our mother didn't want to see me."),
    ("EVELYN", "[sharp] Michael?"),
    ("MICHAEL", "[quickly] That's not what happened.")])
sc("dining", ["anna"], "Close-up of Anna, unflinching.",
   [("ANNA", "[quiet, precise] You said she was too sick to understand who I was."),
    ("MICHAEL", "[defensive] I was trying not to upset her.")])
sc("dining", ["evelyn"], "Evelyn standing at her place, trembling with anger.",
   [("EVELYN", "[low, shaking] You let me believe my daughter was lost to me."),
    ("MICHAEL", "[pleading] Mom—"),
    ("EVELYN", "[breaking] You watched me cry every single birthday.")])
sc("dining", ["michael"], "Michael looking down at his plate.",
   [("MICHAEL", "[weak] I didn't know what to do."),
    ("EVELYN", "[cold] You could have told me the truth.")])
sc("dining", ["anna", "richard"], "Anna facing Richard across the length of the table.",
   [("ANNA", "[gentle, to the table] I didn't come here to take anyone's place."),
    ("RICHARD", "[contemptuous] Then why are you here?"),
    ("ANNA", "Because your wife invited me.")])
sc("dining", ["richard"], "Richard leaning on the table with both fists.",
   [("RICHARD", "[cold] And what exactly do you expect from us?"),
    ("ANNA", "An answer."),
    ("RICHARD", "[scoffing] To what?")])
sc("dining", ["anna"], "Close-up of Anna, voice dropping, every word deliberate.",
   [("ANNA", "[slow, quiet] To why you told a sixteen-year-old girl... that her mother had paid to make her disappear.")],
   sfx=[["Gasps around a table, then silence", 2.0, 0.4, "start"]])

# SCENE 13 - THE CHECK ON THE TABLE
sc("dining", [], "Close-up of the old uncashed check laid on the white tablecloth between the turkey and the candles.",
   [("ANNA", "[calm] Do you recognize this?"),
    ("RICHARD", "[flat] No."),
    ("ANNA", "It's your signature.")],
   sfx=[["Paper placed on a wooden table", 1.0, 0.45, "start"]], music="tension")
sc("dining", ["richard"], "Richard not looking at the check.",
   [("RICHARD", "[dismissive] That proves nothing."),
    ("ANNA", "[steady] You handed it to me at your front door. In the rain.")])
sc("dining", ["diane"], "Diane staring at the check, then at her father.",
   [("DIANE", "[small, stunned] Dad?"),
    ("RICHARD", "[smooth] She was a confused teenager.")])
sc("dining", ["anna"], "Anna's voice rising for the first time.",
   [("ANNA", "[rising] I was sixteen. I wasn't confused about wanting to meet my mother."),
    ("MICHAEL", "[cutting in] Anna, this isn't helping."),
    ("ANNA", "[without looking at him] I wasn't talking to you.")])
sc("dining", ["richard"], "Richard sitting back, playing the generous man.",
   [("RICHARD", "[magnanimous] I gave you money because I felt sorry for you."),
    ("ANNA", "[sharp] You told me never to come back."),
    ("RICHARD", "[righteous] I was protecting my wife.")])
sc("dining", ["evelyn"], "Evelyn slowly turning to her husband.",
   [("EVELYN", "[dangerously quiet] From what?"),
    ("RICHARD", "From reopening a terrible chapter."),
    ("EVELYN", "[voice breaking] That terrible chapter was our daughter.")])
sc("dining", ["richard"], "Richard smiling thinly.",
   [("RICHARD", "[cold] Evelyn, you agreed to the adoption."),
    ("EVELYN", "[fierce] Under threats."),
    ("RICHARD", "[shrugging] That's your version.")])
sc("dining", ["anna"], "Anna glancing toward the foyer.",
   [("ANNA", "[calm] Then maybe we should hear the version your old attorney remembers.")],
   sfx=[["Doorbell ringing again through a big house", 2.0, 0.5, "end"]])

# SCENE 14 - THE ATTORNEY
sc("dining", ["peter"], "Peter Hale stepping into the dining room doorway in a tweed jacket, holding an old leather document box.",
   [("PETER", "[quiet, heavy] Good evening, Richard."),
    ("RICHARD", "[stunned] Peter Hale.")],
   sfx=[["Footsteps on hardwood, a door closing", 2.0, 0.4, "start"]], music="tension", motion="he steps into the doorway holding an old leather box")
sc("dining", ["peter"], "Peter standing at the end of the table, everyone staring.",
   [("PETER", "[dry] It's been a long time."),
    ("MICHAEL", "[sharp] Who invited him?"),
    ("EVELYN", "[calm] I did.")])
sc("dining", ["richard"], "Richard rising, pointing to the door.",
   [("RICHARD", "[furious, controlled] This is a private family dinner."),
    ("PETER", "I know."),
    ("RICHARD", "Then leave.")])
sc("dining", ["peter"], "Peter setting the leather box down on the sideboard.",
   [("PETER", "[steady] Evelyn asked me to explain something that should have been explained decades ago."),
    ("DIANE", "[anxious] What?")])
sc("dining", ["peter"], "Close-up of Peter, glasses in hand.",
   [("PETER", "[measured] Forty years ago, Richard instructed me to prepare the papers for Anna's adoption."),
    ("RICHARD", "[warning] Be careful, Peter."),
    ("PETER", "[quiet] I intend to be.")])
sc("dining", ["evelyn"], "Evelyn looking at Peter, steeling herself.",
   [("EVELYN", "[firm] Tell them about the threats.")])
sc("dining", ["peter"], "Peter speaking slowly to the whole table.",
   [("PETER", "[plain, heavy] Richard told Evelyn that if she refused, he'd go after custody of Michael and Diane. [pause] And use every legal advantage he had to make sure she lost.")])
sc("dining", ["michael"], "Michael leaning forward, lawyer mode.",
   [("MICHAEL", "[sharp] You can't prove that."),
    ("PETER", "[calm] I kept notes of every meeting. Dated. In my own hand."),
    ("RICHARD", "[sneering] Notes can be misunderstood.")])
sc("dining", ["peter"], "Peter nodding slowly.",
   [("PETER", "[honest] They can. I won't pretend my notes are a court judgment. [pause] But I was in that hospital room. And I remember what was said.")])
sc("dining", ["evelyn"], "Close-up of Evelyn, forty years of hurt in her eyes.",
   [("EVELYN", "[quiet, raw] Then why didn't you help me?")],
   sfx=[["Total silence, candles flickering", 2.5, 0.2, "start"]])
sc("dining", ["peter"], "Peter looking down, ashamed.",
   [("PETER", "[heavy] Because I was young, ambitious... and more worried about keeping a powerful client than doing the right thing."),
    ("ANNA", "[quiet] And I paid the price."),
    ("PETER", "[simply] Yes. [pause] You did.")])
sc("dining", ["peter"], "Peter opening the old leather box; inside, bundles of unopened envelopes tied with string.",
   [("PETER", "[slow] There's one more thing. [pause] The adoption agency never refused your letters, Evelyn. [pause] Richard had them forwarded to my office.")],
   sfx=[["An old box lid opening, paper rustling", 2.0, 0.45, "start"]], motion="he lifts the lid, revealing bundles of old unopened envelopes")
sc("dining", [], "Close-up of stacks of yellowed, unopened envelopes in a box, each addressed in the same handwriting: 'For Anna'.",
   [(N, "[soft, devastating] Forty years of birthday cards. [pause] Forty years of Christmas letters. [pause] Every one of them... still sealed.")])
sc("dining", ["evelyn"], "Evelyn staring at the box, a hand over her heart, then turning to her husband.",
   [("EVELYN", "[barely a whisper] You kept them. [pause] All this time... you kept them from her.")])
sc("dining", ["anna"], "Anna lifting one envelope, her own name on it in her mother's handwriting, tears falling.",
   [("ANNA", "[a broken whisper] They're addressed to me."),
    ("PETER", "[gently] I should have given them to you years ago. [pause] I'm sorry.")])

# SCENE 15 - THE MONEY
sc("dining", ["michael"], "Michael standing, trying to take control of the room.",
   [("MICHAEL", "[loud, lawyerly] Fine. Dad behaved terribly forty years ago. [pause] What does any of that have to do with today?"),
    ("PETER", "[quiet] More than you might think.")],
   music="tension")
sc("dining", ["richard"], "Richard's hand tightening on his glass.",
   [("RICHARD", "[low, urgent] Peter, don't."),
    ("EVELYN", "[firm] Let him speak.")])
sc("dining", ["peter"], "Peter taking a bound document from the box.",
   [("PETER", "[measured] Richard's father set up a family trust before he died."),
    ("DIANE", "[impatient] We know about the trust."),
    ("PETER", "The trust provided for Richard's children.")])
sc("dining", ["michael"], "Michael with a confident smile.",
   [("MICHAEL", "[confident] Meaning Diane and me."),
    ("PETER", "[pause] Not necessarily.")])
sc("dining", ["anna"], "Close-up of Anna, realizing.",
   [("ANNA", "[slowly] I was born before your grandfather died.")],
   sfx=[["Silence, a chair creaking", 2.0, 0.25, "start"]])
sc("dining", ["diane", "richard"], "Diane turning to her father; Richard avoiding her eyes.",
   [("DIANE", "[shaken] Dad?"),
    ("RICHARD", "[stiff] She wasn't raised in this family."),
    ("PETER", "[calm] That doesn't automatically decide whether she qualifies under the trust.")])
sc("dining", ["michael"], "Michael's smile gone.",
   [("MICHAEL", "[tight] You're saying Anna could have a claim?"),
    ("PETER", "I'm saying the original documents need an independent review."),
    ("MICHAEL", "[scoffing] This is ridiculous.")])
sc("dining", ["anna"], "Anna raising her hands, shaking her head.",
   [("ANNA", "[earnest] I didn't know about any trust until last month."),
    ("RICHARD", "[triumphant sneer] There it is. [pause] The money.")])
sc("dining", ["anna"], "Close-up of Anna, quiet and sure.",
   [("ANNA", "[quiet] No. [pause] There it is. The reason you were so determined to erase me.")])
sc("dining", ["evelyn"], "Evelyn turning slowly to Richard.",
   [("EVELYN", "[very quiet] Richard. Did you hide her... because of the trust?"),
    ("RICHARD", "[cold, unrepentant] I did what was necessary.")])
sc("dining", ["evelyn", "richard"], "Husband and wife facing each other across the candlelit table.",
   [("EVELYN", "[sharp] Necessary for whom?"),
    ("RICHARD", "[hard] For our family.")])
sc("dining", ["anna"], "Close-up of Anna, a single tear, voice barely above a whisper.",
   [("ANNA", "[quiet, devastating] I was your family.")],
   sfx=[["Silence, candles flickering", 3.0, 0.2, "start"]])

# SCENE 16 - THE SON'S FINAL LIE
sc("dining", ["michael"], "Michael turning to his mother, spreading his hands.",
   [("MICHAEL", "[pleading, reasonable] Mom, you can't seriously believe these people."),
    ("EVELYN", "[cool] These people?"),
    ("MICHAEL", "Anna and Peter.")],
   music="tension")
sc("dining", ["evelyn"], "Evelyn looking at her son as if seeing a stranger.",
   [("EVELYN", "[icy] One is my daughter. The other was your father's attorney."),
    ("MICHAEL", "[urgent] Anna is manipulating you.")])
sc("dining", ["anna", "michael"], "Anna meeting Michael's eyes calmly.",
   [("ANNA", "[calm] I haven't asked Evelyn for anything."),
    ("MICHAEL", "[cold] Yet.")])
sc("dining", ["claire"], "Claire standing up at her place.",
   [("CLAIRE", "[firm] Dad, stop."),
    ("MICHAEL", "[sharp] Claire, stay out of this."),
    ("CLAIRE", "[steady] No.")])
sc("dining", ["michael"], "Michael staring at his daughter in disbelief.",
   [("MICHAEL", "[dangerous] Excuse me?"),
    ("CLAIRE", "You knew about Anna two years ago."),
    ("MICHAEL", "[impatient] We've established that.")])
sc("dining", ["claire"], "Close-up of Claire, scared but determined, phone in her hand.",
   [("CLAIRE", "[quiet] But there's something you haven't told Grandma."),
    ("MICHAEL", "[warning] Claire."),
    ("CLAIRE", "[steady] I saw the email you sent your campaign lawyer.")])
sc("dining", ["michael"], "Michael going pale.",
   [("MICHAEL", "[furious] You had no right—"),
    ("CLAIRE", "[cutting him off] You asked whether an undisclosed family member could complicate the trust.")],
   sfx=[["Silence", 2.0, 0.2, "start"]])
sc("dining", ["evelyn"], "Evelyn turning slowly toward her son.",
   [("EVELYN", "[barely] Michael?"),
    ("MICHAEL", "[too fast] It was a hypothetical question."),
    ("CLAIRE", "[quiet] You used Anna's name.")])
sc("dining", ["diane"], "Diane staring at her brother, betrayed.",
   [("DIANE", "[stunned] You knew there might be money involved?"),
    ("MICHAEL", "[exploding] I was protecting our interests!")])
sc("dining", ["anna"], "Anna rising slowly from her chair.",
   [("ANNA", "[slow, quiet] So you didn't just hide me from my mother. [pause] You were worried I might be owed something.")])
sc("dining", ["michael"], "Michael red-faced, pointing at Anna.",
   [("MICHAEL", "[shouting] You have no idea what this family has sacrificed!")])
sc("dining", ["anna"], "Close-up of Anna, calm and heartbreaking.",
   [("ANNA", "[softly] You're right. I don't. [pause] Because none of you ever let me belong to it.")],
   sfx=[["Silence, a clock ticking", 2.5, 0.2, "start"]])

# SCENE 17 - THE MATRIARCH'S DECISION
sc("dining", ["evelyn"], "Evelyn rising from her chair at the table, candles before her, everyone falling silent.",
   [("EVELYN", "[quiet, absolute] Enough.")],
   sfx=[["A chair scraping back on hardwood, then silence", 2.0, 0.45, "start"]], music="wonder", motion="she slowly rises from her chair as the candles flicker")
sc("dining", ["evelyn"], "Close-up of Evelyn, voice steady and low.",
   [("EVELYN", "[steady] Forty years ago, Richard told me I had to choose between my daughter and the rest of my family."),
    ("RICHARD", "[warning] Evelyn—"),
    ("EVELYN", "[firm] I made the wrong choice.")])
sc("dining", ["evelyn"], "Evelyn looking at Anna across the table.",
   [("EVELYN", "[aching] And then I spent forty years believing I had no way to correct it.")])
sc("dining", ["michael", "evelyn"], "Michael reaching toward his mother.",
   [("MICHAEL", "[pleading] Mom, please. Don't make another mistake."),
    ("EVELYN", "[cold] Michael, you had two years to tell me my daughter was looking for me."),
    ("MICHAEL", "[weak] I thought—")])
sc("dining", ["evelyn"], "Close-up of Evelyn, cutting him off.",
   [("EVELYN", "[cutting] You thought about your campaign. Your reputation. [pause] Your inheritance."),
    ("MICHAEL", "That's not fair."),
    ("EVELYN", "[quiet] Neither was what you did to Anna.")])
sc("dining", ["diane"], "Diane, shaken, looking at her mother.",
   [("DIANE", "[small] Mom... what happens now?")])
sc("dining", ["evelyn", "richard"], "Evelyn facing Richard down the length of the table.",
   [("EVELYN", "[businesslike] I've hired my own attorney to review the trust and the adoption records."),
    ("RICHARD", "[furious] You went behind my back?"),
    ("EVELYN", "[cool] You taught me what happens when I let you make every decision.")])
sc("dining", ["richard"], "Richard standing, red with rage.",
   [("RICHARD", "[shouting] You're tearing this family apart!"),
    ("EVELYN", "[calm] No, Richard. [pause] I'm refusing to hold it together with lies.")])
sc("dining", ["anna", "evelyn"], "Anna touching Evelyn's arm, worried.",
   [("ANNA", "[quiet] Evelyn, I didn't come here to ruin your marriage."),
    ("EVELYN", "[gentle, sad] Sweetheart... my marriage was broken long before you walked through that door.")])
sc("dining", ["richard"], "Richard, suddenly unsure.",
   [("RICHARD", "[unsteady] And what about me?"),
    ("EVELYN", "[quiet] You can spend tonight thinking about the daughter you turned away. [pause] I've arranged somewhere else to stay.")])
sc("dining", ["richard"], "Close-up of Richard, the arrogance cracking for the first time.",
   [("RICHARD", "[stunned] You're leaving?"),
    ("EVELYN", "Yes."),
    ("RICHARD", "[disbelief] On Thanksgiving?")])
sc("dining", ["evelyn"], "Close-up of Evelyn, eyes wet, completely calm.",
   [("EVELYN", "[slow, steady] Forty Thanksgivings ago, I watched someone take my baby away. [pause] Tonight... I get to leave with her.")],
   sfx=[["Quiet piano", 4.0, 0.25, "start"]])
sc("foyer", ["evelyn", "anna"], "Evelyn and Anna walking out the heavy front door together into the autumn night, Anna holding the box of letters.",
   [(N, "[warm] She didn't pack a suitcase. She took her coat... and her daughter's hand.")],
   sfx=[["Front door opening, autumn wind, footsteps on stone", 3.0, 0.4, "start"]], motion="they walk out the front door together into the night, leaves blowing")

# SCENE 18 - THE EMPTY CHAIR IS FILLED
sc("diner", ["evelyn", "anna"], "Two hours later: Evelyn and Anna in a red vinyl booth of an almost empty diner, two slices of pumpkin pie between them, the box of letters on the seat.",
   [(N, "[soft] Two hours later, Evelyn and Anna sat across from each other in a quiet diner. [pause] No chandeliers. No silver. No family portraits watching from the walls. [pause] Just two women and two slices of pumpkin pie.")],
   sfx=[["Quiet diner at night, coffee pouring, soft jukebox", 4.0, 0.3, "start"]], music="wonder", cut=True)
sc("diner", ["anna"], "Anna shaking her head with a small disbelieving laugh.",
   [("ANNA", "[half laughing] You really left?"),
    ("EVELYN", "[dry] Apparently."),
    ("ANNA", "After all those years?"),
    ("EVELYN", "[quiet] I should have done it sooner.")])
sc("diner", ["anna"], "Anna turning her coffee cup.",
   [("ANNA", "[uncertain] I'm not sure what happens next."),
    ("EVELYN", "Neither am I."),
    ("ANNA", "What if we don't get along?"),
    ("EVELYN", "[a small smile] Then we'll argue.")])
sc("diner", ["evelyn"], "Evelyn looking at her daughter with soft attention.",
   [("ANNA", "What if I'm nothing like you imagined?"),
    ("EVELYN", "[gently] Then I'll get to know the woman you actually are.")])
sc("diner", ["anna"], "Anna's eyes filling, voice dropping.",
   [("ANNA", "[quiet] What if I'm angry?"),
    ("EVELYN", "You have every right to be."),
    ("ANNA", "[honest] I spent so many years thinking you didn't want me. [pause] Sometimes I hated you.")])
sc("diner", ["evelyn"], "Close-up of Evelyn accepting it.",
   [("EVELYN", "[soft] I understand."),
    ("ANNA", "[tearful] I don't know if I can forgive you yet."),
    ("EVELYN", "[gently] I'm not asking you to.")],
   sfx=[["Diner sounds fading, silence", 2.0, 0.2, "start"]])
sc("diner", ["anna"], "Anna wiping her eyes with a paper napkin.",
   [("ANNA", "[small] Then what are you asking?"),
    ("EVELYN", "[hopeful, shy] Could we have dinner together again? Next week?")])
sc("diner", ["evelyn", "anna"], "Both women smiling at each other across the booth, neon light on their faces.",
   [("ANNA", "[surprised] Next week?"),
    ("EVELYN", "If you're free."),
    ("ANNA", "[a slow smile] I think I'd like that.")])

# SCENE 19 - SIX MONTHS LATER
sc("law_office", ["peter"], "Six months later: Peter at a bright conference table covered in document binders.",
   [(N, "Six months later."),
    ("PETER", "[measured] The trust review is still ongoing."),
    ("ANNA", "I expected that.")],
   sfx=[["Bright office, papers shuffling, spring birds outside", 3.0, 0.3, "start"]], music="wonder", cut=True)
sc("law_office", ["peter"], "Peter tapping a binder of old records.",
   [("PETER", "There are serious questions about the records... and how certain payments were handled over the years."),
    ("EVELYN", "And Richard?"),
    ("PETER", "[dry] He's cooperating through his lawyers. Reluctantly.")])
sc("law_office", ["anna:day", "evelyn:day"], "Anna and Evelyn sitting side by side at the table.",
   [("ANNA", "[quiet wonder] I never imagined my life would turn into this."),
    ("EVELYN", "[soft] Neither did I.")])
sc("law_office", ["peter"], "Peter taking off his glasses, serious.",
   [("PETER", "Anna, you should have your own lawyer. Your interests may not be the same as Evelyn's."),
    ("ANNA", "I understand.")])
sc("law_office", ["evelyn:day", "anna:day"], "Evelyn putting her hand over Anna's on the table.",
   [("EVELYN", "[firm, warm] Whatever happens with the money, I don't want it deciding what we are to each other."),
    ("ANNA", "[smiling] Neither do I.")])
sc("law_office", ["peter"], "Peter smiling for the first time.",
   [("PETER", "[wry] That may be the wisest thing anyone in this family has said in forty years.")],
   sfx=[["Light laughter in an office", 2.0, 0.3, "end"]])
sc("office", ["michael:office"], "Michael alone in an emptied campaign office, posters face-down, a TV news screen glowing.",
   [(N, "[measured] Michael withdrew from the district attorney's race three weeks after his family's story reached the newspapers. [pause] His campaign lawyer's email was quoted in all of them.")],
   sfx=[["Muffled TV news, an empty office", 3.0, 0.3, "start"]])
sc("study", ["richard:home"], "Richard alone in his dark study, a stack of legal letters in front of him, staring at the rain.",
   [(N, "Richard spent the spring answering questions about forty years of trust records. [pause] The legal fights were far from over.")])
sc("study", ["richard:home"], "Close-up of Richard looking at an old family photograph with one face missing from it.",
   [(N, "[slow] But the greatest consequence had already landed. [pause] Neither man would ever again decide whether Anna was allowed to know her mother.")])

# SCENE 20 - NEXT THANKSGIVING
sc("cottage", ["claire"], "One year later: Claire in the small cozy cottage kitchen, opening the oven, smoke puffing out, laughing.",
   [(N, "[warm] One year later. [pause] A much smaller house. A much smaller table."),
    ("CLAIRE", "[cheerful shout] Grandma, the turkey's ready!")],
   sfx=[["Small kitchen, oven timer beeping, laughter", 3.0, 0.35, "start"]], music="wonder", cut=True)
sc("cottage", ["evelyn:home"], "Evelyn in an apron, waving a dish towel at the smoke.",
   [("EVELYN", "[mock stern] Then take it out before we have another disaster."),
    ("ANNA", "[amused] Another disaster?")])
sc("cottage", ["claire", "anna:home"], "Claire grinning at Anna, who is laughing at the counter.",
   [("CLAIRE", "[teasing] Last spring Grandma nearly set the kitchen on fire."),
    ("EVELYN", "[indignant] That is a terrible exaggeration."),
    ("CLAIRE", "[deadpan] The smoke alarm disagrees.")],
   sfx=[["Warm laughter", 2.0, 0.35, "end"]])
sc("cottage", ["diane:home"], "The cottage front door opening; Diane standing there in a camel coat holding a pie dish, unsure of her welcome.",
   [("DIANE", "[hesitant, quiet] I'm late. [pause] I wasn't sure if I was invited."),
    ("EVELYN", "[warm] There's a chair for everyone who wants to be here, Diane.")],
   sfx=[["A small front door opening, wind chimes", 2.0, 0.4, "start"]])
sc("cottage", ["diane:home", "anna:home"], "Diane holding the pie out awkwardly to Anna; Anna taking it with a small smile.",
   [("DIANE", "[awkward, sincere] I brought pie. [pause] And... I'm sorry, Anna. For last year. For all of it."),
    ("ANNA", "[gently] It's a start. [pause] Come in.")])
sc("cottage", ["anna:home"], "Anna standing by the table, looking at the chairs.",
   [("ANNA", "[shy] Evelyn? [pause] Where should I sit?")],
   sfx=[["Brief quiet", 1.5, 0.2, "start"]])
sc("cottage", ["evelyn:home"], "Evelyn pulling out the carved chair beside her own, the same chair from the old estate.",
   [("EVELYN", "[softly] Right here."),
    ("ANNA", "[surprised] At the head of the table?"),
    ("EVELYN", "[tender] Beside me.")],
   motion="she pulls out the old carved chair beside her own")
sc("cottage", [], "No people in the frame. Close-up of an empty ornate carved wooden chair from the estate standing at a small wooden table among mismatched chairs, candlelight on it.",
   [("ANNA", "[quiet] Is that... the chair?"),
    ("EVELYN", "[soft] The only thing I took from that house. [pause] I've been saving it for forty-one years.")])
sc("cottage", ["anna:home", "evelyn:home"], "Anna sitting down in the carved chair beside Evelyn, both smiling with tears.",
   [("ANNA", "[warm, teasing] Then I guess I shouldn't keep you waiting."),
    ("EVELYN", "[gently] No. [pause] You've waited long enough.")],
   sfx=[["A chair sliding in, gentle piano", 3.0, 0.3, "start"]])
sc("estate_empty", ["richard"], "Across town, Richard alone at the far end of the long, dark estate dining table on Thanksgiving, a single place setting, every other chair empty.",
   [(N, "[slow, measured] Across town, a long mahogany table was set for one. [pause] For forty years, Richard Whitmore had decided who belonged at it. [pause] This year, no one came.")],
   sfx=[["A large silent room, a clock ticking, a fork against china", 4.0, 0.3, "start"]], motion="the candle beside him gutters in the dark empty room")
sc("cottage", ["evelyn:home", "anna:home", "claire", "diane:home"], "The small cottage table full and warm, candles and string lights, everyone laughing and passing dishes.",
   [(N, "[reflective] For forty years, Evelyn Whitmore had lived in a house full of expensive furniture, beautiful paintings, and people who called themselves family. [pause] But every Thanksgiving, something was missing. [pause] Not money. Not status. Not another perfect photograph. [pause] A daughter.")])
sc("cottage", ["anna:home"], "Close-up of Anna at the table, a dish of potatoes just out of reach.",
   [("ANNA", "[casual, then catching herself] Mom? [pause] Could you pass the potatoes?")],
   sfx=[["The room going quiet for a heartbeat", 1.5, 0.2, "start"]])
sc("cottage", ["evelyn:home"], "Close-up of Evelyn freezing, eyes instantly filling, then smiling the brightest smile.",
   [("EVELYN", "[voice trembling with joy] Of course, sweetheart.")],
   sfx=[["Soft laughter around a table", 2.0, 0.3, "end"]])
sc("cottage", [], "The cottage window from outside at night, warm golden light, silhouettes laughing around a full table, autumn leaves falling.",
   [(N, "[slow, final] The family had spent decades protecting its secrets. [pause] And in the end, those secrets cost them the one thing they claimed to value most. [pause] Each other."),
    (N, "[warm] The empty chair was finally filled. [pause] This has been Karma Tales. Every betrayal has a price. And karma always collects.")],
   motion="leaves drift past the glowing window")


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
    title = "My Mother Set an Extra Plate at Thanksgiving. Nobody Knew Who It Was For."
    spec = {
        "title": "Karma Tales EP07 - The Empty Chair",
        "voices": {r: VOICES[r] for r in sorted(roles)},
        "cast": CAST,
        "portraits": {k: PORTRAIT + v for k, v in PORTRAITS.items()},
        "looks": LOOKS,
        "style": "Photorealistic still from a prestige American TV drama, shot on 35mm, warm candlelit cinematic lighting, shallow depth of field, natural skin texture, rich autumn color palette, wide 16:9 frame. Keep every person's face and hair exactly consistent with their reference photo. No text, no captions, no watermark. ",
        "resolution": "2K",
        "music": music,
        "places": PLACES,
        "ambiences": {
            "dining": ["Large formal dining room, candles, very faint clock ticking, distant wind outside", 0.05],
            "foyer": ["Large old house entrance hall, faint wind outside", 0.05],
            "study": ["Quiet wood-paneled study, rain on a window", 0.06],
            "coffee": ["Quiet coffee shop, soft murmur, rain outside", 0.06],
            "apt": ["Small quiet apartment, refrigerator hum, distant city", 0.05],
            "kitchen": ["Warm kitchen, oven hum, faint simmering", 0.05],
            "hall": ["Old house hallway, creaking, muffled voices", 0.04],
            "office": ["Quiet office at night, muffled city traffic", 0.05],
            "rain": ["Steady rain on stone steps", 0.07],
            "hospital": ["Quiet hospital room tone", 0.04],
            "diner": ["Quiet diner at night, soft jukebox far away, coffee machine", 0.06],
            "bright": ["Bright office, faint birds outside", 0.04],
            "cottage": ["Small cozy house, crackling fireplace, warm murmur", 0.06],
            "empty": ["Large empty silent room, slow clock ticking", 0.05]},
        "ambience": [],
        "scenes": scenes,
        "youtube": {
            "title": title,
            "description": "Every Thanksgiving, Evelyn Whitmore set the table for her family. This year, she set one extra place. When her son asked who it was for, she answered: \"Your aunt.\"\n\nBut the woman who rang the doorbell had been to this house once before. And the man who answered that day is still sitting at the head of the table.\n\nA Karma Tales Thanksgiving special: revenge and twist stories where the people who scheme always get what they deserve.\n\nThis story is fiction. Any resemblance to real people or events is coincidental. Narration and images are AI-generated.\n\n#karmatales #thanksgiving #familysecrets #revengestory",
            "tags": ["karma tales", "thanksgiving story", "family secrets", "revenge story", "adoption story", "mother and daughter", "family betrayal", "twist ending", "audio drama", "thanksgiving drama"],
            "category": "24",
            "shorts_description": "Watch the full story on Karma Tales: EPISODE_URL\n" + title + "\n\n#shorts #karmatales #thanksgiving #familysecrets",
        },
        "thumbnail_file": "karma/ep07_thumb.jpg",
        "shorts_end_card": "Watch the full story|on our channel",
        "shorts": [],
    }
    tone = {"dining": "dining", "foyer": "foyer", "study": "study", "coffee": "coffee", "anna_apt": "apt", "kitchen": "kitchen",
            "hallway": "hall", "office": "office", "porch": "rain", "hospital": "hospital", "diner": "diner",
            "law_office": "bright", "cottage": "cottage", "estate_empty": "empty"}
    last = None
    for s in scenes:
        key = tone.get(s.get("place", ""))
        if key and key != last:
            spec["ambience"].append([s["id"], key])
            last = key
    out = ROOT / "karma" / "ep07_full.json"
    out.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")
    words = sum(len(t.split()) for s in scenes for _, t in s["lines"])
    print(f"{out.name}: {len(scenes)} scenes, {words} words, {sum(1 for s in scenes if s.get('motion'))} moving clips")


if __name__ == "__main__":
    main()
