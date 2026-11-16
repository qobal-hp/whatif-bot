"""Write karma/ep03_full.json, Karma Tales EP03 "The Other Wife Knew", from the final script.

usage: python karma/build_ep03.py
Lines carry eleven_v3 audio tags so the delivery is acted. Every place has its own room tone, and scenes carry
sound effects (snow, muffled carols, rain on a car roof, a bank lobby) so the story sounds like it happens somewhere.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

VOICES = {  # voice-library voices, used by id
    "NARRATOR": "FmtiHEcHpocK7YiZwa46",  # Jason - Warm American Storyteller (channel narrator)
    "RACHEL": "YyqkX0AHv8W5D1vxG9lR",  # Hazel - Warm, Witty & Conversational
    "ADAM": "7JxQktePrzZL8mtvQqOy",  # Rocco - Energetic & Charming
    "LAUREN": "DODLEQrClDo8wCz460ld",  # Lauren - Friendly, Comforting and Soft
    "DAVID": "KCO0afdAdW1HAOmQjNUc",  # American Joshua - Calm & Professional
    "ORTIZ": "SkTrsOLN0P3ZmVSoI2k7",  # Halit - Warm, Natural, deep
    "BEN": "Bk8cLrXXi9WCZ4GQU4Ah",  # Clara Louise - high, clear (child)
}

CAST = {c: f"karma/cast/ep03/{c}.jpg" for c in ["rachel", "adam", "lauren", "ben", "maya", "david", "ortiz"]}

PORTRAIT = ("Photorealistic still from a prestige American TV drama, shot on 35mm, shallow depth of field, soft cinematic key light, "
            "natural skin texture, head-and-shoulders portrait facing slightly off camera, neutral dark background, an entirely "
            "fictional person who resembles no real celebrity, no text, no watermark. ")
PORTRAITS = {
    "david": "David Chen, a 37-year-old Chinese-American attorney, short neat black hair, thin dark-framed glasses, calm thoughtful expression, navy suit, light blue shirt, no tie.",
    "ortiz": "Detective Ortiz, a 50-year-old Latino American police detective, close-cropped graying hair, trimmed salt-and-pepper beard, tired observant eyes, gray wool overcoat over a dark sweater.",
}

LOOKS = {
    "rachel": "Rachel (the woman from the reference photo, same face, dark-brown hair pulled into a sleek low ponytail, in a camel wool coat and a gray scarf)",
    "rachel:home": "Rachel (the same woman as the reference photo, same face, dark-brown hair in a low ponytail, in a cream cable-knit sweater)",
    "rachel:work": "Rachel (the same woman as the reference photo, same face, dark-brown hair in a sleek low ponytail, in a tailored charcoal blazer over a black turtleneck)",
    "rachel:cabin": "Rachel (the same woman as the reference photo, same face, hair loose and relaxed, in an oversized red flannel shirt)",
    "adam": "Adam (the man from the reference photo, same face and wavy dark hair, in a dark wool coat over a crisp white shirt)",
    "adam:home": "Adam (the same man as the reference photo, same face, in a navy quarter-zip sweater)",
    "adam:suit": "Adam (the same man as the reference photo, same face, in a sharp charcoal suit and silver tie)",
    "adam:prison": "Adam (the same man as the reference photo, same face, unshaven, in an orange prison jumpsuit)",
    "lauren": "Lauren (the woman from the reference photo, same face, long loose brown hair, in a dark green wool coat)",
    "lauren:home": "Lauren (the same woman as the reference photo, same face, long brown hair, in a soft ivory sweater)",
    "ben": "Ben (the 12-year-old boy from the reference photo, same face, in a red-and-navy plaid flannel shirt)",
    "maya": "Maya (the 9-year-old girl from the reference photo, same face, long light-brown hair with a sparkly clip, in a white knit sweater)",
    "david": "David (the man from the reference photo with dark-framed glasses, in a navy suit)",
    "ortiz": "Detective Ortiz (the bearded man from the reference photo, in a gray wool overcoat)",
}

PLACES = {
    "street": "Setting: a quiet snowy suburban street in Naperville, Illinois on Christmas Eve night, houses glowing with holiday lights, fresh snow, falling flakes.",
    "lauren_house": "Setting: the warm living room of a two-story suburban house on Christmas Eve, a big Christmas tree covered in golden lights, presents and wrapping paper on the floor, fireplace.",
    "kitchen": "Setting: Rachel and Adam's modern Chicago townhouse kitchen, white marble island, pendant lights, gray winter light through the window.",
    "fundraiser": "Setting: an elegant charity gala ballroom in downtown Chicago years ago, chandeliers, warm golden light, people in evening wear.",
    "coffee": "Setting: a nearly empty neighborhood coffee shop on Christmas morning, snow outside the big front window, string lights, steam rising from cups.",
    "law_office": "Setting: a modern law office high above downtown Chicago in winter, glass walls, snow drifting past the windows, a tidy desk with files.",
    "car": "Setting: inside a parked car in a grocery store parking lot on a gray rainy afternoon, rain streaking the windshield, the dashboard glowing, fogged side windows.",
    "bank": "Setting: a glass-walled conference room on the twelfth floor of a downtown Chicago bank, a long white table, a city view of snowy rooftops, a decorated Christmas tree visible in the lobby beyond the glass.",
    "cabin": "Setting: a cozy log cabin near Lake Michigan on Christmas Eve night, a crackling stone fireplace, a small Christmas tree, snow falling over the dark lake outside the window.",
}

N = "NARRATOR"
S = []


def sc(place, chars, image, lines, **extra):
    S.append((place, chars, image, lines, extra))


def msg(text, frm="Unknown number"):
    return {"type": "message", "from": frm, "to": "Rachel", "text": text}


# ACT 1 - CHRISTMAS EVE
sc("street", ["rachel"], "Rachel standing alone in the snow on a dark suburban sidewalk at night, her breath visible, staring at a glowing house across the street.",
   [(N, "[low, intimate] On Christmas Eve, Rachel Morgan found out her husband had another family.")],
   sfx=[["Muffled Christmas carol drifting from inside a house, winter wind, snow crunching under boots", 6.0, 0.3, "start"]],
   motion="snow falls slowly around her as she stands still, breath fogging in the cold")
sc("street", [], "A beautiful two-story suburban house glowing with Christmas lights in the snow, a wreath on the door, warm golden windows.",
   [(N, "Not an affair. Not one stupid night. [pause] A family. A woman. Two children. And a house forty minutes from her own.")])
sc("street", ["rachel"], "Close-up of Rachel's face lit by the glow of her phone screen in the dark, snowflakes on her eyelashes.",
   [(N, "[quiet] But the worst part wasn't watching him through a stranger's window. [pause] It was the text message she got while she was standing there.")],
   sfx=[["Phone vibrating in a coat pocket", 1.5, 0.45, "end"]])
sc("lauren_house", [], "View through a frosted front window from outside at night: a warm living room with a huge glowing Christmas tree, wrapping paper everywhere.",
   [(N, "Rachel stood in the snow outside a two-story house in Naperville, Illinois. Through the front window, a Christmas tree wrapped in golden lights.")], cut=True)
sc("lauren_house", ["ben", "maya"], "Through the window: a boy tearing wrapping paper off a present and a little girl laughing by the Christmas tree.",
   [(N, "A boy tearing paper off a present. A little girl laughing.")],
   motion="the boy rips the wrapping paper open while the little girl laughs and claps")
sc("lauren_house", ["adam", "ben", "maya"], "Through the window: Adam on the couch in a cozy sweater, smiling, arm around the boy, the girl leaning on him, Christmas tree glowing behind.",
   [(N, "[pause] And on the couch beside them... Adam.")],
   sfx=[["Low cinematic boom, muffled", 2.5, 0.35, "start"]])
sc("street", ["rachel"], "Rachel outside in the snow, one gloved hand over her mouth, eyes filling with tears.",
   [(N, "[quietly] Her Adam. Her husband of eleven years. The man who kissed her goodbye that morning and said he had to work late.")], music="tension")
sc("lauren_house", ["adam", "ben"], "Through the glass: Adam laughing as the boy holds up a new toy drone in its box.",
   [("ADAM~phone", "[warm, laughing, muffled through glass] Hey, buddy! What did Santa bring you?"),
    ("BEN~phone", "[excited, muffled] Dad! Look! It's the one I wanted!")])
sc("street", ["rachel"], "Extreme close-up of Rachel's eyes reflecting the warm window light, devastated.",
   [(N, "Dad. [pause] That word hit harder than anything else. For years, Rachel and Adam had talked about kids. And for years, Adam said he wasn't ready.")])
sc("street", ["rachel"], "Rachel stepping back off the curb, looking down at her buzzing phone.",
   [(N, "Rachel took a step back. Her phone buzzed again. Unknown number.")],
   sfx=[["Phone vibrating twice", 1.5, 0.45, "end"]],
   overlay=msg("Don't let him see you."))
sc("street", [], "A dark silver SUV parked across a snowy street at night, under a streetlight, snow on its roof.",
   [(N, "Another message.")], overlay=msg("Silver SUV. Across the street. I can see you."))
sc("street", [], "Looking up at a dark second-floor window of the house; a curtain shifting slightly, a faint silhouette behind it.",
   [(N, "[tense] Rachel looked at the driveway. Then up at the dark second-floor window. [pause] A curtain moved.")],
   sfx=[["Tense low musical pulse", 3.0, 0.3, "start"]], motion="the curtain in the dark upstairs window shifts slightly as a shadow moves behind it")
sc("street", ["rachel"], "Rachel typing on her phone with trembling fingers in the snow.",
   [(N, "Another message. Meet me tomorrow. Nine a.m. Alone."),
    ("RACHEL", "[whispering as she types, shaken] Who is this?")], overlay=msg("Meet me tomorrow. 9 a.m. Alone."))
sc("street", ["rachel"], "Close-up of the phone screen glow on Rachel's stunned face.",
   [(N, "The answer came right away.")], overlay=msg("The woman you think stole your husband."),
   sfx=[["Sharp dramatic musical sting", 2.0, 0.4, "start"]])
sc("street", ["rachel"], "Rachel frozen in the falling snow, the glowing house behind her out of focus.",
   [(N, "[slow] Then one more.")], overlay=msg("And Rachel? He's lying to both of us."),
   sfx=[["Deep cinematic boom with a long tail", 3.0, 0.4, "end"]])

# ACT 2 - THE PERFECT HUSBAND
sc("fundraiser", ["adam", "rachel:work"], "Years earlier at a charity gala: a younger Adam in a tuxedo making Rachel laugh, both holding champagne, warm golden light.",
   [(N, "[reflective] Eleven years earlier, Rachel met Adam at a charity fundraiser in downtown Chicago. He was handsome. Funny. And he paid attention.")],
   music="wonder", sfx=[["Elegant party chatter and a jazz quartet", 4.0, 0.2, "start"]], cut=True)
sc("", ["rachel:work"], "Rachel at her office desk years ago smiling at a big bouquet of flowers with a card, a coffee cup with her name on it beside her.",
   [(N, "He remembered her coffee order. He sent flowers to her office. When her mother was in the hospital, he drove three hours at midnight to bring her a change of clothes.")])
sc("", ["adam:suit", "rachel:work"], "A small elegant wedding at a Chicago venue, Adam and Rachel laughing as guests throw petals.",
   [(N, "He seemed like the kind of man who would never leave. They married two years later.")])
sc("kitchen", ["adam:home"], "Adam zipping up a carry-on suitcase by the front door, kissing the air toward the kitchen, morning light.",
   [(N, "Rachel worked in financial analysis. Adam called himself an independent business consultant. He traveled. Milwaukee. Indianapolis. St. Louis. Sometimes for days. [pause] Rachel never questioned it. Until last summer.")])
sc("kitchen", ["rachel:home"], "Summer: Rachel at the kitchen island with a laptop open to a credit card statement, frowning.",
   [("RACHEL", "[puzzled] Adam, why is there a charge from a pediatric clinic on our credit card?"),
    ("ADAM", "[easy, not looking up] Oh. That's probably a client expense.")],
   sfx=[["Soft flashback whoosh", 1.5, 0.3, "start"]])
sc("kitchen", ["adam:home", "rachel:home"], "Adam leaning on the counter with a casual smile, Rachel looking at him skeptically.",
   [("RACHEL", "A pediatric clinic?"),
    ("ADAM", "One of my clients runs a medical practice. I covered an invoice, they paid me back."),
    ("RACHEL", "That's a strange way to do business."),
    ("ADAM", "[charming laugh] Honey, you're the numbers person. I'm the people person.")])
sc("kitchen", ["adam:home", "rachel:home"], "Adam kissing Rachel's forehead as she closes her eyes.",
   [(N, "He kissed her forehead. And she let it go.")])
sc("kitchen", [], "Close-up on the kitchen island: a crumpled receipt for children's snow boots next to a printed hotel booking.",
   [(N, "Then came a receipt for children's snow boots. A hotel booking for two adults and two children.")])
sc("kitchen", ["rachel:home"], "Rachel staring at her phone showing a social media photo of a smiling family in front of a Christmas tree.",
   [(N, "And a photo on social media. Adam, smiling beside a woman Rachel had never seen. The caption: \"Another wonderful year with our favorite guy.\"")])
sc("kitchen", ["rachel:home", "adam:home"], "Rachel holding up her phone to Adam, tense; Adam calm and smiling.",
   [("RACHEL", "[tight] Who is Lauren Parker?"),
    ("ADAM", "[smooth] A client."),
    ("RACHEL", "And the kids?"),
    ("ADAM", "Hers.")])
sc("kitchen", ["adam:home"], "Close-up of Adam, patient and reassuring, reaching for Rachel's hand.",
   [("RACHEL", "Then why are you in their family Christmas photo?"),
    ("ADAM", "[sighs, patient] Because I kept her business alive through the pandemic. She's grateful. That's all.")])
sc("kitchen", ["rachel:home"], "Rachel alone at the kitchen window at night in December, holding her phone, a text on the screen.",
   [(N, "Rachel wanted to believe him. So she did. [pause] Until December twenty-second, when a text arrived from a number she didn't know.")],
   overlay=msg("Check where your husband is on Christmas Eve."), sfx=[["Phone vibrating on a counter", 1.5, 0.4, "start"]])
sc("kitchen", ["rachel:home"], "Christmas Eve: an old tablet glowing on the dark kitchen counter showing a map with a single blue location dot.",
   [(N, "She deleted it. Probably a scam. But on Christmas Eve, Adam's old tablet lit up on the kitchen counter. He'd never turned off location sharing. [pause] And the little blue dot wasn't in Milwaukee.")],
   motion="the tablet screen glows in the dark kitchen as the blue dot pulses on the map")
sc("street", ["rachel"], "Rachel driving at night through falling snow, wipers moving, her face lit by the dashboard.",
   [(N, "So Rachel drove there herself. And now she was standing in the snow, watching her husband live a second life. [pause] But someone inside that house had been waiting for her.")],
   sfx=[["Car door closing, engine starting, windshield wipers in snow", 4.0, 0.3, "start"]])

# ACT 3 - THE OTHER WOMAN
sc("coffee", ["rachel"], "Christmas morning: Rachel alone at a window table in a nearly empty coffee shop, untouched coffee, dark circles under her eyes, snow outside.",
   [(N, "Christmas morning. A coffee shop that was almost empty. Rachel hadn't slept.")],
   sfx=[["Quiet coffee shop, espresso machine hiss, a bell over the door", 4.0, 0.25, "start"]], music="tension", cut=True)
sc("coffee", ["lauren"], "Lauren walking into the coffee shop in a dark green coat, snow on her shoulders, looking around carefully.",
   [(N, "At exactly nine o'clock, a woman walked in. Dark green coat. Long brown hair. Tired eyes. No wedding ring. [pause] Lauren Parker.")],
   motion="she steps through the door, brushes snow off her coat and scans the room")
sc("coffee", ["lauren", "rachel"], "Lauren sitting down across from Rachel; both women tense.",
   [("LAUREN", "[quiet] Rachel?"),
    ("RACHEL", "[flat] You knew I was outside last night."),
    ("LAUREN", "Yes. I saw your car on the doorbell camera.")])
sc("coffee", ["rachel"], "Close-up of Rachel, guarded, gripping her cup.",
   [("RACHEL", "You knew who I was?"),
    ("LAUREN", "[pause] For eight months."),
    ("RACHEL", "[stunned] Eight months?")])
sc("coffee", ["lauren"], "Close-up of Lauren speaking quietly, eyes down.",
   [("LAUREN", "Adam told me you were his ex-wife. He said the divorce was finalized years ago."),
    ("RACHEL", "[cold] We're still married."),
    ("LAUREN", "I know that now.")])
sc("coffee", ["rachel", "lauren"], "The two women facing each other across the small table, tension in the air.",
   [("RACHEL", "And you stayed with him?"),
    ("LAUREN", "I needed to understand what he was doing."),
    ("RACHEL", "You could have called me."),
    ("LAUREN", "[gently] Would you have believed me?")])
sc("coffee", ["rachel"], "Rachel looking away out the snowy window, jaw tight.",
   [(N, "Rachel opened her mouth. Then closed it. The pediatric clinic. The snow boots. The photo. [pause] She hadn't believed her own eyes.")])
sc("coffee", ["lauren"], "Lauren holding her cup with both hands, speaking softly.",
   [("RACHEL", "[barely audible] Are those his kids?"),
    ("LAUREN", "No. Ben and Maya are from my first marriage. Their dad died nine years ago. Maya was a baby. [pause] Adam came into our lives a year later. He's the only father she remembers.")])
sc("", ["ben", "maya"], "A framed family photo on a mantel: the boy and girl younger, smiling with Adam at a pumpkin patch.",
   [(N, "[quiet] Eight years. While Rachel planned anniversaries, he was building another home. With children who had done nothing wrong.")])
sc("coffee", ["lauren", "rachel"], "Lauren leaning in, lowering her voice.",
   [("RACHEL", "Why are you telling me now?"),
    ("LAUREN", "Because three months ago, Adam asked me to sign something. A loan. He wanted my house as collateral for a business investment."),
    ("RACHEL", "Did you sign?")])
sc("coffee", ["lauren"], "Close-up of Lauren, her voice shaking slightly, remembering.",
   [("LAUREN", "No. And when I said no... [swallows] he became someone I'd never seen. He screamed. He threatened to leave. Then he apologized and bought the kids presents. [pause] The next week, he asked again.")])
sc("coffee", ["lauren"], "Lauren sliding a manila folder across the coffee shop table.",
   [(N, "Lauren slid a folder across the table."),
    ("LAUREN", "So I started reading his paperwork. And I found your name.")],
   sfx=[["Paper folder sliding across a table", 1.5, 0.45, "start"]])
sc("coffee", [], "Close-up of a loan application document on the table; the signature line at the bottom in sharp focus, the printed text soft and unreadable.",
   [(N, "A business loan application. Two million dollars. And at the bottom, next to her name... a signature.")])
sc("coffee", ["rachel", "lauren"], "Rachel staring at the document, then up at Lauren.",
   [("RACHEL", "[sharp] I never signed this."),
    ("LAUREN", "I know."),
    (N, "Rachel studied it. It looked almost perfect. [pause] Almost.")])
sc("coffee", ["rachel"], "Close-up of Rachel's finger tracing the signature, her face hardening.",
   [("RACHEL", "[slowly] He's been practicing my signature."),
    ("LAUREN", "That's what I think."),
    ("RACHEL", "[suspicious] And I'm supposed to believe you're innocent?")])
sc("coffee", ["lauren"], "Lauren holding Rachel's gaze, steady and serious.",
   [("LAUREN", "No. I want you to believe the paperwork.")],
   sfx=[["Music darkens into a low drone", 3.0, 0.3, "end"]])
sc("coffee", ["lauren"], "Extreme close-up of Lauren leaning in, almost whispering.",
   [("LAUREN", "[leaning in, low] And there's something else. Adam isn't planning to leave one of us. [pause] He's planning to disappear.")],
   sfx=[["Deep cinematic boom impact", 3.0, 0.45, "end"]])

# ACT 4 - THE MONEY TRAIL
sc("law_office", ["rachel:work", "david"], "Rachel across a desk from David in a glass-walled law office, papers spread between them, snow drifting outside.",
   [(N, "The next day, Rachel sat across from David Chen, a lawyer she'd known since college. She put everything on his desk. The application. The receipts. The texts. David read every page without saying a word.")],
   sfx=[["Quiet office, keyboard typing, papers rustling", 4.0, 0.2, "start"]], cut=True)
sc("law_office", ["david"], "David looking up from the documents, calm and serious.",
   [("DAVID", "[calm] First, we protect you. Today we report the forged signature to the lender's fraud department, and we freeze your credit."),
    ("RACHEL", "And Adam?"),
    ("DAVID", "Don't confront him. Not yet. Let me see what he's already filed... and whether any money has moved.")])
sc("law_office", [], "Close-up of bank statements on a desk with several withdrawals highlighted in yellow marker, the text soft and unreadable.",
   [(N, "It had. The paperwork led to a company called Northstar Capital Solutions. Large transfers out. Small payments that went nowhere. And every month, a withdrawal from the joint account Rachel used for the mortgage.")])
sc("law_office", ["rachel:work", "david"], "Rachel staring at the statements, stunned; David watching her.",
   [("RACHEL", "[disbelief] He's been taking money from our joint account."),
    ("DAVID", "For three years. [pause] One hundred and eighty thousand dollars.")],
   sfx=[["Low tense musical sting", 2.0, 0.35, "end"]])
sc("law_office", ["rachel:work"], "Rachel with a hand over her stomach, looking sick, gazing out at the snow.",
   [(N, "Rachel felt sick. That was her savings. The kitchen they never remodeled. Retirement. The future Adam kept promising her."),
    ("RACHEL", "[quiet] What was he doing with it?"),
    ("DAVID", "Paying for a second house. [pause] And getting ready for something bigger.")])
sc("law_office", ["rachel:work"], "Rachel's phone ringing on the desk, the screen showing a contact named Adam with a heart.",
   [(N, "Then Rachel's phone rang. Adam.")], sfx=[["Phone ringing on a desk", 2.0, 0.45, "start"]])
sc("", ["adam"], "Adam on his phone outside a suburban house in the snow, smiling, the Christmas-lit house behind him.",
   [("ADAM~phone", "[warm, apologetic] Hey, sweetheart. Merry Christmas. I'm so sorry about last night. The client dinner went forever."),
    ("RACHEL", "[carefully neutral] Did it?"),
    ("ADAM~phone", "[sighs] Total nightmare.")])
sc("law_office", ["rachel:work"], "Rachel on the phone, her face perfectly calm while her free hand grips the desk edge.",
   [("RACHEL", "Where are you now?"),
    ("ADAM~phone", "Still in Milwaukee."),
    (N, "Rachel looked at David. Adam was lying. Again. Easily. Like breathing.")])
sc("law_office", ["rachel:work"], "Close-up of Rachel on the phone, eyes cold, voice sweet.",
   [("RACHEL", "When are you coming home?"),
    ("ADAM~phone", "Tomorrow morning."),
    ("RACHEL", "Good. [pause] We should finally sit down and organize our finances.")])
sc("", ["adam"], "Adam on the phone in the snow, his smile faltering for a second.",
   [("ADAM~phone", "[a beat, then a little too quick] Absolutely. Actually... I have some paperwork we should go over.")],
   sfx=[["A beat of tense silence on a phone line", 1.5, 0.2, "start"]])
sc("law_office", ["rachel:work"], "Rachel closing her eyes, phone to her ear.",
   [(N, "Rachel closed her eyes. There it was. The paperwork he'd been preparing for months."),
    ("RACHEL", "[sweetly] Of course, honey. Bring it home.")],
   sfx=[["Phone call ending beep", 1.0, 0.35, "end"]])
sc("law_office", ["rachel:work", "david"], "Rachel setting the phone down, hands shaking; David looking at her with concern.",
   [("DAVID", "[impressed] You handled that well."),
    ("RACHEL", "[shaking] I wanted to scream."),
    ("DAVID", "I know.")])
sc("law_office", ["david"], "Close-up of David, gentle but firm.",
   [("RACHEL", "David... if I hadn't followed him on Christmas Eve, would he have taken everything?"),
    ("DAVID", "[gently] Yes. [pause] But you did follow him. And now we get to choose how this ends.")])

# ACT 5 - LAUREN'S CONFESSION
sc("car", ["lauren", "rachel"], "Inside a parked car in the rain: Lauren in the driver's seat, Rachel in the passenger seat, both staring ahead at the streaming windshield.",
   [(N, "That afternoon, Rachel met Lauren again. A grocery store parking lot. Lauren's car, engine running. Lauren looked like she hadn't slept in a week.")],
   sfx=[["Heavy rain drumming on a car roof, car heater humming", 4.0, 0.3, "start"]], cut=True)
sc("car", ["rachel"], "Rachel in the passenger seat turning toward Lauren.",
   [("RACHEL", "You said he's planning to disappear. How do you know?"),
    ("LAUREN", "[quiet] I found a plane ticket in his email. One way.")])
sc("car", [], "Close-up of a phone screen in the car showing an airline booking confirmation, the text blurred except a small airplane icon.",
   [("RACHEL", "To where?"),
    ("LAUREN", "Lisbon. January fifteenth."),
    ("RACHEL", "For all of you?"),
    ("LAUREN", "[bitter laugh] No. Just him.")])
sc("car", ["rachel"], "Rachel looking out the rain-streaked side window, devastated.",
   [(N, "Rachel looked out at the rain. Adam wasn't choosing between two women. He was leaving both of them. And two kids who called him Dad.")])
sc("car", ["lauren", "rachel"], "Lauren gripping the steering wheel, eyes red.",
   [("RACHEL", "Why didn't you tell me this at the coffee shop?"),
    ("LAUREN", "Because I was scared you'd call the police before I could protect my kids."),
    ("RACHEL", "Protect them from what?")])
sc("car", ["lauren"], "Close-up of Lauren, ashamed, holding a crumpled bank letter.",
   [("LAUREN", "Adam registered one of his companies at my address. And last month a bank letter came saying I'm a guarantor on one of his loans."),
    ("RACHEL", "Did you sign it?"),
    ("LAUREN", "[shaking her head] Not that one. But years ago I signed a lot of his business papers without reading them. Because I trusted him.")])
sc("car", ["rachel"], "Rachel studying Lauren's face, her expression softening slightly.",
   [(N, "For the first time, Rachel saw something familiar in Lauren's face. Shame. The kind that comes from realizing someone has been steering you for years.")])
sc("car", ["rachel", "lauren"], "The two women in the car, rain on the glass, a cold distance between them.",
   [("RACHEL", "[hard] You should have told me sooner."),
    ("LAUREN", "I know."),
    ("RACHEL", "And I'm not forgiving you for waiting."),
    ("LAUREN", "[steady] I'm not asking you to.")])
sc("car", [], "Close-up of a printed email in Rachel's hands with one sentence highlighted in yellow, the words soft and unreadable.",
   [(N, "Lauren handed Rachel a printed email. Adam to his business partner. One sentence was highlighted."),
    ("ADAM", "[cold, confident, like a memory] \"Once the funding clears, neither Rachel nor Lauren will be able to trace a dime.\"")],
   sfx=[["Low dramatic impact", 2.5, 0.4, "end"]])
sc("car", ["rachel", "lauren"], "Rachel staring at the page, Lauren watching her.",
   [("RACHEL", "[very quiet] He planned this."),
    ("LAUREN", "Yes."),
    ("RACHEL", "Both of us."),
    ("LAUREN", "[whisper] Yes.")])
sc("car", ["rachel"], "Close-up of Rachel lifting her eyes from the page, a cold, decided look.",
   [(N, "Rachel stared at the page for a long time. Then she said something Lauren didn't expect."),
    ("RACHEL", "[calm, decided] We're not going to warn him.")])
sc("car", ["rachel", "lauren"], "Inside the parked car: Lauren in the driver's seat turning to Rachel in surprise; Rachel in the passenger seat with a faint, dangerous smile. Through the windshield only a blurred rainy parking lot, no store signs, no logos, no lettering anywhere.",
   [("LAUREN", "What?"),
    ("RACHEL", "We're going to let him think he's winning.")],
   sfx=[["Rising tense musical swell", 3.0, 0.35, "end"]])

# ACT 6 - THE SIGNATURE
sc("kitchen", ["adam", "rachel:home"], "Adam coming through the front door into the kitchen with a bouquet of red roses and a designer shopping bag, snow on his coat.",
   [(N, "Adam came home on December twenty-sixth. With flowers. A designer handbag. And a stack of documents.")],
   sfx=[["Front door opening, keys tossed on a counter", 2.0, 0.4, "start"]], cut=True)
sc("kitchen", ["adam", "rachel:home"], "Adam grinning, holding out the flowers; Rachel smiling back politely.",
   [("ADAM", "[bright, charming] Rachel! Merry late Christmas!"),
    ("RACHEL", "[smiling] You shouldn't have."),
    ("ADAM", "Come on. I know I've been distracted lately."),
    ("RACHEL", "[light] That's one word for it.")])
sc("kitchen", ["adam:home"], "Adam laughing a little too loudly, then spreading papers on the marble island.",
   [(N, "Adam laughed. A little too loud."),
    ("ADAM", "Listen. I have big news. An investment. If it works, we retire in five years. [pause] I just need your signature on a few things.")])
sc("kitchen", [], "Close-up of loan documents fanned out on a white marble kitchen island next to red roses, a pen on top.",
   [(N, "Northstar Capital Solutions. Two million dollars. The same loan. Only this time, he needed her real signature. [pause] Because David's fraud report had made the bank nervous. And the bank now wanted the wife to sign in person.")])
sc("kitchen", ["rachel:home", "adam:home"], "Rachel reading the first page with innocent curiosity; Adam waving his hand dismissively.",
   [("RACHEL", "[curious, innocent] That's a lot of money. Secured by what?"),
    ("ADAM", "[waving it off] Just some assets. Nothing to worry about."),
    ("RACHEL", "Which assets?")])
sc("kitchen", ["adam:home"], "Close-up of Adam's smile slipping into irritation.",
   [(N, "Adam's smile slipped."),
    ("ADAM", "[irritated] Rachel, do we really have to do this?"),
    ("RACHEL", "Do what?"),
    ("ADAM", "Interrogate each other?")])
sc("kitchen", ["adam:home", "rachel:home"], "Adam snatching the papers off the island, turning away.",
   [("RACHEL", "[even] I'm asking about a two-million-dollar loan."),
    ("ADAM", "[snatching the papers] You know what? Forget it. I thought you'd be happy.")],
   sfx=[["Papers snatched off a counter", 1.0, 0.4, "start"]])
sc("kitchen", ["adam:home"], "Adam stopping in the doorway, turning back.",
   [("RACHEL", "[softly] Adam?"),
    ("ADAM", "[stops] What?"),
    ("RACHEL", "I love you.")])
sc("kitchen", ["adam:home"], "Close-up of relief washing over Adam's face.",
   [(N, "He turned. Relief washed over his face."),
    ("ADAM", "[relieved] I love you too, baby.")])
sc("kitchen", ["rachel:home"], "Close-up of Rachel, warm smile, eyes cold.",
   [("RACHEL", "That's why I want it done properly. I'll sign. [pause] At the bank. In front of the notary. With David there.")])
sc("kitchen", ["adam:home"], "Adam frozen mid-step, the smile gone.",
   [(N, "Adam froze."),
    ("ADAM", "[tight] David Chen?"),
    ("RACHEL", "He's my lawyer. If it's as safe as you say, you've got nothing to worry about.")],
   sfx=[["Tense silence, a kitchen clock ticking", 3.0, 0.3, "end"]])
sc("kitchen", ["adam:home"], "Close-up of Adam's eyes calculating, then the charming smile sliding back into place.",
   [(N, "For one second, Rachel saw the real Adam. Not the charming husband. Not the smiling man from the Christmas photos. A man doing math. [pause] Then the smile came back."),
    ("ADAM", "[smooth again] Fine. The bank said Wednesday at ten. Downtown."),
    ("RACHEL", "[sweet] Perfect.")])
sc("kitchen", ["adam:home"], "Adam alone on the staircase of the townhouse with his phone to his ear, smirking. No one else in the frame.",
   [(N, "Adam kissed her cheek and went upstairs to call his partner. [pause] He thought he'd just won. He had no idea who else would be in that room on Wednesday.")],
   sfx=[["Ominous low drone", 3.0, 0.3, "end"]])

# ACT 7 - THE CLOSING
sc("bank", [], "A downtown Chicago bank tower on a snowy morning, a huge decorated Christmas tree in the marble lobby.",
   [(N, "Wednesday. December thirtieth. Ten a.m. A glass conference room on the twelfth floor of a downtown Chicago bank.")],
   sfx=[["Echoing marble bank lobby, footsteps, distant holiday music", 4.0, 0.25, "start"]], music="tension", cut=True)
sc("bank", ["adam:suit", "rachel:work"], "Adam in his best suit striding into the glass conference room with a pen already in hand, Rachel beside him.",
   [(N, "Adam arrived early, in his best suit, with a pen already in his hand."),
    ("ADAM", "[cheerful] Big day."),
    ("RACHEL", "[smiling] It really is.")])
sc("bank", ["david", "ortiz"], "David seated at the conference table; in the background by the glass door, a quiet bearded man in a gray overcoat.",
   [(N, "David sat beside Rachel. Across the table, a bank officer. And by the door, a quiet man in a gray overcoat that Adam didn't bother to look at."),
    ("ADAM", "[smooth] Thanks for coming, David. Just a formality."),
    ("DAVID", "[dry] We'll see.")])
sc("bank", ["adam:suit", "rachel:work"], "Loan documents slid in front of Rachel; Adam leaning close, pointing to the signature line.",
   [("ADAM", "[low, encouraging] Right there, honey. Bottom of each page."),
    ("RACHEL", "[pen hovering] Before I sign... can I see the first application? The one from September."),
    ("ADAM", "[too fast] There wasn't one.")])
sc("bank", ["david"], "David calmly placing a single sheet of paper in the middle of the table.",
   [(N, "David placed a single sheet on the table. The September application. With Rachel's name. And a signature that was almost hers."),
    ("RACHEL", "[calm] Then whose signature is this?")],
   sfx=[["Low tense musical sting", 2.0, 0.4, "end"]])
sc("bank", ["adam:suit"], "Close-up of Adam forcing a laugh, sweat at his temple.",
   [("ADAM", "[forced laugh] Okay... that... that's a draft. My assistant must have—")])
sc("bank", ["lauren"], "The glass conference room door opening; Lauren stepping in, dark green coat, snow in her hair, steady expression.",
   [(N, "And then the door opened. [pause] Lauren Parker walked in. Dark green coat. Snow still in her hair.")],
   sfx=[["Door opening, then a deep cinematic boom", 3.0, 0.5, "start"]],
   motion="the glass door swings open and she walks in slowly, snow melting in her hair")
sc("bank", ["adam:suit"], "Adam's face draining of all color as he stares at the door.",
   [("ADAM", "[the color draining from his voice] Lauren?"),
    ("LAUREN", "[quiet, steady] Hi, Adam. [pause] Should I tell her about your divorce... or should you?")])
sc("bank", ["rachel:work", "adam:suit", "lauren"], "Adam standing between the two women in the glass room, looking from one to the other, trapped.",
   [(N, "Adam looked from one woman to the other. Two wives. Two lives. One room. [pause] For the first time in eight years, he had no story ready.")],
   motion="the man turns his head slowly from one woman to the other, frozen")
sc("bank", ["lauren"], "Lauren laying papers and a printed airline ticket on the table one by one.",
   [("LAUREN", "[laying papers on the table] This is the guarantee you filed with my name on it. I never signed it. And this... is your ticket to Lisbon. January fifteenth. One way. [pause] Just you.")],
   sfx=[["Papers set down one at a time on a table", 2.0, 0.4, "start"]])
sc("bank", ["rachel:work", "adam:suit"], "Rachel standing up, cold; Adam turning to her, desperate.",
   [("RACHEL", "[cold] You were going to leave all of us. Me. Her. Those kids."),
    ("ADAM", "[desperate] Rachel, listen to me. I can explain—"),
    ("RACHEL", "[cutting him off] Which part? The lies? The money? Or the family you hid for eight years?")])
sc("bank", ["adam:suit"], "Adam with tears in his eyes, hands open, pleading.",
   [("ADAM", "[voice breaking] I made mistakes.")])
sc("bank", ["rachel:work"], "Close-up of Rachel, steel in her eyes.",
   [("RACHEL", "[steel] No, Adam. A mistake is forgetting an anniversary. You built two lives... and lied to everyone in both of them.")],
   sfx=[["Deep cinematic impact", 2.5, 0.45, "end"]])
sc("bank", ["ortiz"], "The bearded man in the gray overcoat stepping forward, holding up a police badge.",
   [(N, "The man in the gray overcoat stepped forward."),
    ("ORTIZ", "[flat, unhurried] Adam Morgan. Detective Ortiz, Chicago PD, financial crimes. The bank's fraud unit called us after Mr. Chen's report. [pause] You're under arrest for bank fraud and forgery.")])
sc("bank", ["adam:suit", "ortiz"], "The detective handcuffing Adam at the conference table, Adam twisting to look back.",
   [("ADAM", "[panicking] This is insane! Lauren— Lauren, think about Ben and Maya!"),
    ("LAUREN", "[quiet fury] I am. That's why I'm here.")],
   sfx=[["Handcuffs clicking shut", 1.5, 0.5, "start"]], motion="the detective snaps handcuffs onto the man's wrists behind his back")
sc("bank", ["ortiz"], "Detective Ortiz holding out his hand.",
   [("ORTIZ", "And Mr. Morgan? We'll be holding on to your passport.")])
sc("bank", ["adam:suit", "ortiz"], "Adam in handcuffs being walked past the bank's giant Christmas tree in the marble lobby, people staring.",
   [(N, "They walked him out past the glass walls. Past the tellers. Past the Christmas tree in the lobby. [pause] He looked back once. Neither woman looked at him.")],
   sfx=[["Footsteps echoing in a marble lobby, murmurs", 4.0, 0.3, "start"]],
   motion="the handcuffed man is led across the lobby past the glowing Christmas tree")

# ACT 8 - THE WOMAN WHO KNEW
sc("law_office", ["rachel:work", "lauren", "david"], "Rachel and Lauren sitting in chairs a careful distance apart in David's office, David behind his desk, snow falling outside.",
   [(N, "Two weeks later, Rachel and Lauren sat in David's office. They were not friends. They might never be. But they had agreed on one thing. Neither of them would let Adam hide behind the other.")],
   sfx=[["Quiet office, snow against the window", 3.0, 0.2, "start"]], music="wonder", cut=True)
sc("law_office", ["david"], "David reading from a file, relieved.",
   [("DAVID", "[businesslike] The bank froze every Northstar account. Most of your hundred and eighty thousand is sitting in one of them, Rachel. You'll get it back. [to Lauren] And the guarantee with your name on it has been voided."),
    ("LAUREN", "[exhales] Thank God."),
    ("DAVID", "His partner is cooperating. Adam's lawyer is already talking about a plea.")])
sc("law_office", ["rachel:work"], "Rachel leaning back in her chair, closing her eyes, finally breathing.",
   [(N, "Rachel leaned back. For the first time in weeks, she could breathe. [pause] Then Lauren reached into her bag.")])
sc("law_office", ["lauren"], "Close-up of Lauren alone in her chair in the law office, hesitating, turning slightly to her side, snowy window behind her. No one else in the frame.",
   [("LAUREN", "[hesitant] Rachel... there's something I haven't told you."),
    ("RACHEL", "[tired] What now?"),
    ("LAUREN", "On Christmas Eve, I didn't just see your car on the camera. [pause] I knew you'd be there.")])
sc("law_office", ["lauren"], "Close-up of Lauren confessing, ashamed but honest.",
   [("RACHEL", "[slowly] How?"),
    ("LAUREN", "That text on December twenty-second. \"Check where your husband is on Christmas Eve.\" [pause] That was me.")],
   sfx=[["Low musical sting", 2.0, 0.4, "end"]])
sc("law_office", ["rachel:work"], "Rachel staring at Lauren in disbelief.",
   [("RACHEL", "[stunned] You led me to your house?"),
    ("LAUREN", "Yes."),
    ("RACHEL", "Why?")])
sc("law_office", ["lauren"], "Lauren speaking softly, eyes down.",
   [("LAUREN", "[quietly] Because I called you twice in October. You didn't answer. I left a voicemail. You blocked my number.")])
sc("law_office", ["rachel:work"], "A memory: Rachel months earlier, glancing at an unknown caller on her phone and swiping it away.",
   [(N, "Rachel remembered. A woman's voice. A voicemail she never played. She'd assumed it was a scam.")],
   sfx=[["Phone buzz, then a swipe", 1.5, 0.3, "start"]])
sc("law_office", ["lauren", "rachel:work"], "Lauren and Rachel facing each other, raw emotion.",
   [("LAUREN", "I knew you'd never believe a stranger saying your husband had another family. So I made sure you could see it with your own eyes."),
    ("RACHEL", "[hurt, angry] You used me."),
    ("LAUREN", "I gave you the truth. [pause] But I should have told you how.")])
sc("law_office", ["rachel:work"], "Rachel standing at the tall office window, her back to the room, Chicago buried in snow below.",
   [(N, "Rachel stood and walked to the window. Below them, Chicago was buried in snow."),
    ("RACHEL", "[not turning around] You should have given me a choice."),
    ("LAUREN", "[softly] You're right.")],
   motion="snow drifts past the window as she stands still looking down at the city")
sc("law_office", ["rachel:work", "lauren"], "Rachel turning back to face Lauren.",
   [(N, "For a long moment, neither woman spoke. Then Rachel turned around."),
    ("RACHEL", "I don't know if I'll ever trust you."),
    ("LAUREN", "I understand."),
    ("RACHEL", "[a long breath] But I'm glad I found out."),
    ("LAUREN", "[a small, sad smile] So am I.")])
sc("law_office", ["rachel:work", "lauren"], "The two women side by side at the snowy window, not touching, both looking out.",
   [(N, "Adam wasn't the only one in this story keeping secrets. [pause] But he was the only one whose secrets were built to hurt people.")])

# EPILOGUE - ONE YEAR LATER
sc("cabin", ["rachel:cabin"], "One year later: Rachel curled up by the crackling fireplace in a cozy log cabin with a mug of cocoa, a small Christmas tree glowing.",
   [(N, "[warm, unhurried] One year later, Rachel spent Christmas in a small cabin near Lake Michigan. She was divorced. Her savings were back. And she'd started a new job, teaching women how to read the fine print of their own finances.")],
   sfx=[["Crackling fireplace, soft Christmas music on an old radio", 5.0, 0.3, "start"]], cut=True,
   motion="the fire crackles and the tree lights twinkle as she sips from her mug")
sc("", ["adam:prison"], "Adam in an orange prison jumpsuit sitting alone on a bunk in a gray cell, staring at the floor.",
   [(N, "Adam pleaded guilty to bank fraud and aggravated identity theft. The judge gave him six years in federal prison. [pause] He never made it to Lisbon.")],
   sfx=[["Heavy cell door clanging shut, echo", 2.0, 0.45, "start"]])
sc("", ["lauren:home", "ben", "maya"], "Lauren and her two kids carrying moving boxes into a bright new house, the kids laughing.",
   [(N, "Lauren sold the house in Naperville and moved with Ben and Maya closer to her sister. Rachel and Lauren still message now and then. Nothing sentimental. Nothing forced. Just two women who survived the same lie.")])
sc("cabin", ["rachel:cabin"], "Rachel's phone lighting up on the cabin table next to her mug.",
   [(N, "On Christmas Eve, Rachel's phone buzzed."),
    ("LAUREN~phone", "[warm] \"Merry Christmas. The kids are doing great. I hope you are too.\"")],
   sfx=[["Phone vibrating on a wooden table", 1.5, 0.4, "start"]],
   overlay={"type": "message", "from": "Lauren", "to": "Rachel", "text": "Merry Christmas. The kids are doing great. I hope you are too."})
sc("cabin", ["rachel:cabin"], "Rachel smiling as she types a reply by the fire.",
   [("RACHEL", "[smiling as she types] \"Merry Christmas. I am.\"")])
sc("cabin", [], "Snow falling softly over a dark frozen Lake Michigan seen through the cabin window, the warm reflection of the fire on the glass. No people anywhere in the frame.",
   [(N, "Rachel set the phone down. Outside, snow fell softly over the lake. A year ago, she stood in the cold, watching her husband open presents with another family. [pause] Tonight she was alone. And she had never felt less lonely.")],
   motion="snow falls gently over the dark lake beyond the window")
sc("street", [], "The Naperville house from Act 1 now dark and empty with a For Sale sign in the snow, no lights, at night.",
   [(N, "[slow, final] Adam thought he could live two lives. He thought he could control two women. And he thought he'd be gone before either of them found the truth. [pause] He made one mistake. He underestimated both of them.")],
   sfx=[["Cold winter wind, piano rising", 4.0, 0.3, "start"]])
sc("cabin", ["rachel:cabin"], "Rachel by the fire, looking into the flames with a calm, peaceful smile.",
   [(N, "He had two families. Two women. And a thousand lies. [pause] In the end... he lost all of it. And the truth followed him all the way to a prison cell."),
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
    title = "My Husband Had a Secret Family for 8 Years. His Other Wife Knew About Me."
    spec = {
        "title": "Karma Tales EP03 - The Other Wife Knew",
        "voices": {r: VOICES[r] for r in sorted(roles)},
        "cast": CAST,
        "portraits": {k: PORTRAIT + v for k, v in PORTRAITS.items()},
        "looks": LOOKS,
        "style": "Photorealistic still from a prestige American TV drama, shot on 35mm, cinematic lighting, shallow depth of field, natural skin texture, warm Christmas color palette with cold blue winter shadows, wide 16:9 frame. Keep every person's face and hair exactly consistent with their reference photo. No text, no captions, no watermark. ",
        "resolution": "2K",
        "music": music,
        "places": PLACES,
        "ambiences": {
            "snow_night": ["Quiet snowy suburban street at night, soft winter wind, faint muffled Christmas carols from houses", 0.08],
            "home": ["Quiet modern home room tone, refrigerator hum, faint winter wind outside", 0.05],
            "gala": ["Elegant party murmur and soft jazz in a ballroom", 0.06],
            "coffee": ["Nearly empty coffee shop, low espresso machine hum, soft holiday music far away", 0.07],
            "office": ["Quiet high-rise office room tone, faint air conditioning, snow wind against glass", 0.05],
            "car_rain": ["Steady rain drumming on a parked car roof, car heater humming", 0.1],
            "bank": ["Large quiet bank interior, distant lobby echo, faint holiday music", 0.05],
            "cabin": ["Crackling fireplace in a quiet wooden cabin, soft wind outside", 0.09],
        },
        "ambience": [],
        "scenes": scenes,
        "youtube": {
            "title": title,
            "description": "On Christmas Eve, Rachel Morgan watched her husband open presents with another woman and two children who called him Dad. Then her phone buzzed. A text from the other woman: \"He's lying to both of us.\"\n\nTwo wives. Two lives. One forged signature on a two-million-dollar loan. And a one-way ticket to Lisbon he never got to use.\n\nKarma Tales: revenge and twist stories where the people who scheme always get what they deserve.\n\nThis story is fiction. Any resemblance to real people or events is coincidental. Narration and images are AI-generated.\n\n#karmatales #revengestory #secretfamily #christmasdrama",
            "tags": ["karma tales", "revenge story", "secret family", "cheating husband", "christmas drama", "other woman", "double life", "forgery", "twist ending", "audio drama"],
            "category": "24",
            "shorts_description": f"Full story on Karma Tales: {title}\n\n#shorts #karmatales #revengestory #secretfamily",
        },
        "thumbnail_file": "karma/ep03_thumb.jpg",
        "shorts": [
            {"id": "short1", "title": "She caught her husband|with another family", "from": "s01", "to": "s15",
             "youtube_title": "She Followed Her Husband on Christmas Eve. Then the Other Woman Texted Her. #shorts"},
            {"id": "short2", "title": "His two wives.|One room.", "from": "s88", "to": "s95",
             "youtube_title": "He Brought His Wife to Sign the Loan. His Other Wife Walked In. #shorts"},
            {"id": "short3", "title": "\"A mistake is forgetting|an anniversary.\"", "from": "s96", "to": "s101",
             "youtube_title": "He Said He Made Mistakes. She Had the Perfect Answer. #shorts"},
        ],
    }
    tone = {"street": "snow_night", "lauren_house": "snow_night", "kitchen": "home", "fundraiser": "gala", "coffee": "coffee",
            "law_office": "office", "car": "car_rain", "bank": "bank", "cabin": "cabin"}
    last = None
    for s in scenes:
        key = tone.get(s.get("place", ""))
        if key and key != last:
            spec["ambience"].append([s["id"], key])
            last = key
    out = ROOT / "karma" / "ep03_full.json"
    out.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")
    words = sum(len(t.split()) for s in scenes for _, t in s["lines"])
    print(f"{out.name}: {len(scenes)} scenes, {words} words, {sum(1 for s in scenes if s.get('motion'))} moving clips")


if __name__ == "__main__":
    main()
