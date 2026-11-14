"""Build the specs for What If It Happens EP03: Everyone Got a Death Countdown. One Baby Reached Zero.

Script: the reviewed version in the "What If EP03 — Death Countdown (수정본)" doc.
Long form (L ids) + two Shorts (s ids). Daniel and Thomas use faces cropped from the chosen
thumbnails (whatif/cast/), Emma and Dr. Brooks get portraits drawn on the first run.
Run: python whatif/build_ep03.py -> whatif/ep03_long.json, ep03_short1.json, ep03_short2.json
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
CAST = {"daniel": "whatif/cast/daniel.jpg", "thomas": "whatif/cast/thomas.jpg",
        "emma": "video/public/assets/portrait_emma.jpg", "brooks": "video/public/assets/portrait_brooks.jpg"}
PORTRAITS = {
    "emma": "Photorealistic head-and-shoulders portrait of a woman about 30, shoulder-length auburn hair, green eyes, light freckles, grey knit cardigan, gentle tired expression, plain soft grey background, soft window light, 85mm lens.",
    "brooks": "Photorealistic head-and-shoulders portrait of a woman in her mid-50s, short silver-blonde bob, thin reading glasses, white lab coat over a navy blouse, sharp intelligent eyes, plain soft grey background, soft light, 85mm lens.",
}
LOOKS = {
    "daniel": "Daniel: man about 30, messy dark-brown hair, stubble, brown eyes, navy hoodie, same face as his reference image",
    "emma": "Emma: woman about 30, shoulder-length auburn hair, green eyes, light freckles, grey cardigan, same face as her reference image",
    "brooks": "Dr. Evelyn Brooks: woman in her mid-50s, short silver-blonde bob, thin reading glasses, white lab coat, same face as her reference image",
    "thomas": "Thomas Reed: man about 61, swept-back grey hair, neatly trimmed grey beard, dark wool coat and scarf, same face as his reference image",
}
LILY = "a three-week-old newborn baby girl in a pink-and-blue striped knit hat and a striped hospital-style blanket"
VOICES = {"NARRATOR": "George", "DANIEL": "Will", "EMMA": "Sarah", "BROOKS": "Matilda", "THOMAS": "Bill",
          "MARCUS": "Eric", "SARAH": "Laura", "ASSISTANT": "Roger", "DOCTOR": "Roger", "ANCHOR": "Brian"}
STYLE_TAIL = "shallow depth of field, moody cinematic sci-fi color grade with red accents, present day, no readable text or numbers unless described. "


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


D, E, B, T = ["daniel"], ["emma"], ["brooks"], ["thomas"]
RED = {"type": "countdown", "mode": "spoken"}

# =============================== LONG FORM ===============================
scenes, music, S = builder("L", 3)

# ---- Chapter 1 — Ten Seconds
S(f"Extreme close-up of {LILY} sleeping in a dim nursery at dawn, a glowing red holographic frame floating above her head, red light on her cheeks.",
  "[slow, hushed] Ten.", "Nine.", "Eight.", music="tension",
  overlay=dict(RED, span=8),
  sfx=[["A single slow heartbeat, then a short digital beep", 3.0, 0.45, "start"]])
S("Daniel in a small nursery at dawn, exhausted, rocking a newborn in his arms, baby bottles and diapers on a dresser, soft lamp light.",
  "Daniel Carter had spent three weeks learning how to be a father. How to hold a newborn. How to survive on two hours of sleep. How to tell a hungry cry from a sleepy one.", chars=D)
S(f"Daniel staring up in shock at a glowing red light floating above {LILY} in his arms, red light on his face.",
  "Nothing could have prepared him for the morning a glowing red number appeared above his daughter's head.", "Seven.", chars=D)
S("Emma frozen in a kitchen doorway at dawn in pajamas, hand over her mouth, red light spilling across her face.",
  "EMMA: [frozen, whispering] Daniel... what is that?", chars=E)
S("Daniel and Emma standing in the nursery, a pale blue glowing number floating above each of their heads, both staring at each other in disbelief.",
  "He couldn't answer. Above his own head floated a pale blue number. Sixty-three years. Above Emma's: forty-two years. And above their three-week-old daughter, Lily... five seconds.", chars=D + E)
S("Daniel clutching the newborn to his chest, shouting toward Emma who holds a phone with shaking hands.",
  "DANIEL: [panicked] Emma, call somebody!", "EMMA: [shaking] Who? What do I even tell them?", "Four.", "Three.", chars=D + E)
S(f"Daniel pressing his forehead gently against {LILY}, eyes shut, tears on his cheeks, red glow above them.",
  "Daniel pressed his forehead against his daughter's.",
  "DANIEL: [whispering, breaking] Please. Please don't. I'm right here. I'm not going anywhere.", chars=D)
S(f"Macro close-up of {LILY}'s face bathed in red light, eyes open, looking up.",
  "Two.", "One.", "Zero.", sfx=[["A heartbeat that stops, followed by silence", 2.5, 0.4, "start"]])
S(f"{LILY} smiling a tiny perfect smile up at the camera in soft warm morning light, the red glow gone.",
  "Lily stared up at him. Then she smiled. A tiny, perfect smile. She was alive. And the number above her head was gone.",
  motion="The newborn blinks slowly and breaks into a tiny smile, warm light drifts across her face, slow push-in.")
S("Daniel crying with relief while Emma wraps her arms around him and the baby, warm light.",
  "Daniel started to cry. Emma wrapped her arms around them both.", chars=D + E)
S("A smartphone on a nursery dresser lighting up with a flood of notifications, vibrating.",
  "And then Daniel's phone began to vibrate. One notification. Then twenty. Then hundreds.",
  sfx=[["A smartphone vibrating rapidly with many notification chimes", 3.0, 0.35, "start"]])
S("Aerial view of a city street at sunrise full of people looking up at glowing red and blue numbers floating above everyone's heads.",
  "Across the planet, billions of people had woken up with numbers above their heads. And some of those numbers were already reaching zero.",
  motion="Slow drone glide over the crowd as people turn and point at the glowing numbers above each other's heads.")
S("Daniel at the nursery window at sunrise holding the baby, looking out at the city, silhouette, thoughtful.",
  "For the first time in history, everyone thought they knew exactly how much time they had left.", "They were wrong. And the truth would change everything.", chars=D)

# ---- Chapter 2 — The Day the World Changed
S("Montage composition of New York, Tokyo and London streets at morning, crowds with glowing numbers floating above every head.",
  "At eight a.m. Eastern Time, the numbers appeared everywhere at once. Not on phones. Not on screens. Above people. Floating like impossible holograms. They moved when people moved. And no technology on Earth could explain them.",
  cut=True)
S("A tense TV news anchor at a desk in a studio, a screen behind her showing crowds with glowing numbers.",
  "ANCHOR: [tense, professional] We are asking everyone to stay calm. We do not know what these numbers are.")
S("A New York taxi driver standing beside his yellow cab, staring at pedestrians with glowing numbers above their heads on a busy crosswalk.",
  "In New York, a taxi driver stepped out of his cab and stared at the sidewalk. A woman crossing the street had sixty-four years. The man beside her had three months.")
S("A little boy holding his mother's hand at a crosswalk, a soft red glow floating above his head with no readable digits, the mother noticing it with horror.",
  "And a little boy holding his mother's hand had thirty-seven seconds. His mother screamed and yanked him back onto the curb.")
S("A delivery truck skidding past an empty crosswalk on a city street, motion blur, people jumping back on the sidewalk.",
  "Seconds later, a delivery truck skidded through the spot where they had been standing.",
  sfx=[["Truck tires screeching on asphalt and a loud horn", 2.0, 0.4, "start"]])
S("A mother on her knees on a sidewalk hugging her little son tightly, crowd around them, no number above him.",
  "The boy was safe. His countdown vanished. His mother sank to her knees, sure she had just beaten death.")
S("An empty café table by a window with a half-finished coffee and a chair pushed back, people gathered blurred in the background, somber.",
  "Across town, a man sat at a café table as his number reached zero. A sudden heart attack. People rushed to help him, but he was gone.")
S("Split composition: on the left the mother hugging her son, on the right the empty café chair, cold and warm light.",
  "Two zeros. Two completely different endings. But the world only noticed one of them. People were dying when their numbers hit zero.")
S("A wall of phone screens and social media feeds showing glowing red numbers and panicked crowds, dark room.",
  "Within an hour, the internet had given it a name. The Death Clock. The name spread faster than any explanation. And fear spread faster still.",
  overlay={"type": "text", "text": "THE|DEATH CLOCK"})

# ---- Chapter 3 — The Price of Knowing
S("A stock exchange trading floor in chaos, red screens everywhere, traders shouting.",
  "By lunchtime, financial markets were in free fall. Airlines faced mass cancellations as passengers refused to fly. Hospitals filled with people demanding tests.", cut=True)
S("An insurance office boardroom, executives staring at a screen of red numbers, tense.",
  "And insurance companies faced a question they were never built to answer. What happens when everyone believes they know when they'll die?")
S("A young man in a suit walking out of a Chicago office tower carrying a box of his things, a faint red glow above his head with no readable digits, determined.",
  "In Chicago, a thirty-year-old accountant saw four months above his head. He quit his job that afternoon.")
S("A married couple in Los Angeles staring at each other in their kitchen, a soft blue glow above the man's head and a red glow above the woman's, no readable digits, emotional.",
  "In Los Angeles, a married couple looked at each other. He had forty-eight years. She had eleven days.")
S("The same couple laughing on a sunny beach with their two kids, building a sandcastle, golden hour.",
  "They canceled every plan they had. They stopped answering emails. They took their kids to the beach, and for the first time in years, they spent an entire day together.")
S("A bank loan officer sliding a rejected application back across a desk to a worried man with a short glowing number above his head.",
  "But not everyone answered with love. Some banks began quietly reconsidering loans. Some employers changed who they hired. People with short numbers were treated as risks. People with long numbers were treated as assets.")
S("A crowded city sidewalk where people glance suspiciously at each other's glowing numbers, cold blue light.",
  "A person's worth was no longer measured only by money, looks, or achievements. Now it was measured by the number above their head.")
S(f"Daniel sitting on the floor beside a crib at night watching {LILY} sleep, no number above her, lamp light.",
  "Meanwhile, Daniel refused to leave the house. Lily slept in her crib. No number. No countdown. Just an ordinary baby. But every time he looked at her, he relived those ten seconds. People were dying. Other people were surviving. There had to be a reason.", chars=D)

# ---- Chapter 4 — The Scientist
S("Dr. Brooks walking through a high-tech research lab with monitors and volunteers in hospital chairs, focused.",
  "Dr. Evelyn Brooks had spent twenty-five years studying human consciousness. She didn't believe in prophecy. She believed in evidence. And the evidence in front of her made no sense at all.", chars=B, cut=True)
S("A row of twelve volunteers in a lab wired to heart and brain monitors, glowing numbers above their heads, clinical light.",
  "Her team had gathered twelve volunteers whose numbers would reach zero within the hour. Heart rate, blood pressure, brain activity, oxygen. All monitored. And nothing suggested any of them was about to die.")
S("Dr. Brooks sitting beside a nervous 52-year-old man with glasses and a cardigan in a lab chair, a red number above his head.",
  "The first was a fifty-two-year-old schoolteacher named Marcus. Nineteen seconds.",
  "BROOKS: [calm, clinical] Marcus, how do you feel?", "MARCUS: [shaky laugh] Terrified.",
  "BROOKS: Any pain? Dizziness?", "MARCUS: No. Nothing.", chars=B, overlay=dict(RED, span=2))
S("Close-up of the 52-year-old man with glasses squeezing his eyes shut in a lab chair, researchers watching tensely.",
  "The lab went silent. Five. Three. One. Zero.", "Marcus closed his eyes. Then opened them.", "MARCUS: [whispering] Am I... dead?",
  motion="The man slowly opens his eyes and exhales, the researchers behind him break into nervous smiles.")
S("Researchers in a lab celebrating, one laughing in relief, monitors showing steady heartbeat lines.",
  "A nervous laugh escaped one of the researchers. His heart was beating normally. He was alive. And his countdown was gone.")
S("Close-up of a man's hands holding a phone showing a text conversation, Dr. Brooks noticing from beside him.",
  "The team celebrated. Dr. Brooks didn't. Because she had noticed Marcus's phone, buzzing in his hand the whole time. A message from his daughter. Eleven years of silence. And just before zero, Marcus had finally typed three words back.",
  overlay={"type": "message", "from": "Marcus", "to": "Rachel", "text": "I forgive you."})
S("Dr. Brooks writing in a leather notebook at a lab desk late at night, thoughtful.",
  "I forgive you. Dr. Brooks wrote those words in her notebook. She didn't know why. But they felt important.", chars=B)

# ---- Chapter 5 — The Impossible Pattern
S("Dr. Brooks surrounded by screens of case files and video clips in a dark lab, exhausted, coffee cups everywhere.",
  "Over the next forty-eight hours, Dr. Brooks studied thousands of recorded zeros. Some people died. Most did not.", chars=B, cut=True, music="wonder")
S("A firefighter carrying a child out of a smoky building doorway, heroic silhouette, embers.",
  "A firefighter hit zero seconds before pulling a child from a burning building.")
S("A woman shaking hands with an interviewer in a glass office, a world map on the wall behind them.",
  "A woman hit zero the moment she accepted a job on the other side of the world.")
S("A young man in a car at night making a U-turn on an empty highway, headlights, rain.",
  "A young man hit zero as he turned his car around and drove home.")
S(f"Daniel holding {LILY}, their eyes locked, red glow fading, intimate close-up.",
  "And a newborn baby hit zero while looking into her father's eyes.", chars=D)
S("A glass wall covered in sticky notes and photos grouped into clusters, Dr. Brooks standing before it with a marker.",
  "She began sorting them. Death. Survival. Decisions. Discoveries. Encounters. Every single one was a moment that permanently changed the direction of a life.", chars=B)
S("Dr. Brooks turning toward a young male lab assistant at a computer, lab lights low, tense discovery moment.",
  "BROOKS: [slowly] What if we're asking the wrong question?", "ASSISTANT: What do you mean?",
  "BROOKS: What if the clock isn't measuring the end of a life?", "ASSISTANT: Then what is it measuring?",
  "BROOKS: [quiet] The end of the life you were going to have.", chars=B)
S("A dramatic visualization of a glowing path splitting into many branching futures in darkness.",
  "The room went quiet. It was only a theory. But if it was true, the numbers weren't predicting death. They were marking the moments when a person's future changed forever. And that raised a far more disturbing question. If the numbers knew when your future would change... was the future already written?")

# ---- Chapter 6 — The Man Without a Number
S("Grainy black-and-white security camera footage of a crowded subway station, everyone with glowing numbers above their heads.",
  "Three days later, a video began spreading online. A crowded train station in Washington, D.C. Every person in the frame had a number above their head.", cut=True, music="tension")
S("Security-camera view of an older man in a dark coat standing still in a moving crowd, the only person without a glowing number, looking up at the camera.",
  "Except one. An older man in a dark coat. Gray hair. A neatly trimmed beard. No countdown.", chars=T,
  motion="The crowd streams past as the older man stops, turns his head toward the security camera and slowly smiles.")
S("Close-up of Thomas looking directly into a security camera with a faint knowing smile, grainy footage look.",
  "He stopped, turned toward the security camera, and smiled.", "THOMAS: [calm, almost amused] You're all measuring the wrong thing.", chars=T)
S("A wall of news screens showing the station footage of Thomas, with view counters soaring.",
  "The clip was viewed a hundred million times. Within hours, investigators had a name. Thomas Reed. Sixty-one. Former professor of mathematics. Out of public life for almost twenty years.")
S("Thomas and Dr. Brooks sitting across a metal table in a quiet interview room, a worn leather notebook between them.",
  "Dr. Brooks expected a fraud. Instead, Thomas laid a worn notebook on the table. The first page was dated twenty years ago. Across the top, three words. The Turning Point.", chars=T + B)
S("Close-up of Dr. Brooks staring at Thomas across the table, stunned.",
  "BROOKS: [stunned] How did you know?", "THOMAS: [quietly] Because I've seen the numbers before.", chars=B)

# ---- Chapter 7 — Twenty Years Earlier
S("Flashback: a younger Thomas in his early 40s with dark hair writing equations on a chalkboard in a university lab at night, warm sepia tones.",
  "THOMAS: [reflective] Twenty years ago, I was building a mathematical model of human decisions. How tiny choices produce enormous changes. A missed train. A phone call. Choosing one street instead of another.", cut=True)
S("A chalkboard covered in branching diagrams labeled with arrows, sepia flashback light.",
  "They called it the Branching Future Model. Not a machine that could see the future. Just an attempt to describe how futures split apart.")
S("Flashback: younger Thomas alone in the lab looking up in shock at a faint glowing number above his own head.",
  "Then one night, working alone, Thomas looked up and saw a number above his own head. Three minutes.",
  "THOMAS: I thought I was losing my mind. Then it hit zero... and my phone rang.")
S("Flashback: a hospital corridor at night, younger Thomas running toward a door, blurred nurses.",
  "His wife had been in a car accident. She survived. But she never walked again.")
S("Thomas in the present sitting with Dr. Brooks, looking down at his hands, quiet grief.",
  "THOMAS: [quiet] I left the university to take care of her. For twenty years, that was my whole life. She passed away last spring.",
  "BROOKS: [gently] And you never told anyone?", "THOMAS: [a tired smile] I told everyone. Nobody believed me.", chars=T + B)
S("Close-up of an open notebook with dense equations and one handwritten sentence underlined in red ink.",
  "He opened the notebook. Page after page of equations. And one sentence, underlined in red.",
  "The countdown does not predict the future. It marks the moment the future changes.",
  overlay={"type": "letter", "text": "The countdown does not predict the future. It marks the moment the future changes."})
S("Thomas looking out a rain-streaked window, reflection in the glass, no number above his head.",
  "THOMAS: And when your future changes, the clock starts over. A zero isn't the end of the road. It's a fork in it.",
  "BROOKS: Then why is there no number above you now?", "Thomas looked toward the window.",
  "THOMAS: [softly] I've been asking myself that for three days.", chars=T)

# ---- Chapter 8 — Can You Change Your Countdown?
S("Dr. Brooks briefing a small group of volunteers in a lab conference room, a whiteboard behind her.",
  "Dr. Brooks decided to test the theory. Volunteers with less than twenty-four hours. One simple instruction. Change your plans.", chars=B, cut=True)
S("Three-panel composition: a man canceling a flight at an airport counter, a woman signing a new job contract, a man sitting alone in a locked apartment, glowing numbers above each.",
  "A man canceled his flight. His number didn't move. A woman switched jobs. Nothing. Another man refused to leave his apartment at all. The numbers kept falling. If the future could change, why couldn't they change the clock?")
S("A woman in her late 30s with a dark ponytail and a grey hoodie sitting alone in a lab waiting room staring at her hands, a red number above her head.",
  "Then came Sarah Lane. A nurse who had walked away from her job a year ago, burned out and broken. Seventeen minutes left. She sat in the lab's waiting room, staring at her hands.")
S("An elderly man in a waiting room stumbling and falling to the floor, people jumping up from their chairs in alarm.",
  "Across the room, an elderly man stood up... and collapsed.", sfx=[["A chair scraping and a startled gasp from a small room", 1.5, 0.4, "start"]])
S("The woman with the dark ponytail frozen in her chair, eyes wide, conflicted, people panicking in the background.",
  "Everyone froze. Sarah didn't move.", "SARAH: [to herself, shaking] I'm not a nurse anymore. I'm not...")
S("The woman with the dark ponytail kneeling beside the elderly man on the waiting room floor checking his breathing, focused and commanding.",
  "Then she was on her knees beside him, checking his breathing, calling out orders like she had never left.",
  "SARAH: [sharp, focused] Call 911. Somebody find me the defibrillator. Now!")
S("Close-up of the red number above the kneeling woman's head racing down in a blur of digits.",
  "Above her head, the number began to race. Seventeen minutes. Ten. Two. Ten seconds. Five. Three. One. Zero.")
S("Paramedics rushing through a door as the elderly man sits up coughing, the woman with the dark ponytail sitting back on her heels in shock.",
  "The man coughed. He was breathing. Paramedics burst through the door. And above Sarah's head, the number was gone.")
S("Dr. Brooks crouching beside the woman with the dark ponytail in the waiting room, both breathless.",
  "BROOKS: [breathless] Sarah... what did you do?", "SARAH: [stunned, quiet] I stopped running.", chars=B)
S("Dr. Brooks alone in the lab at night writing on a glass board: a line pulled toward a glowing point, realization on her face.",
  "And Dr. Brooks finally understood. The clock wasn't counting toward a fixed event. It was counting toward a turning point. And a single choice could pull that moment closer.", chars=B)

# ---- Chapter 9 — The Second Number
S(f"The Carter living room at night, rain on the windows, Daniel feeding {LILY} a bottle on the couch.",
  "On the fifth night, Daniel was giving Lily her bottle when Emma walked in. She was pale.", chars=D, cut=True, music="tension",
  sfx=[["Steady rain against a window at night", 4.0, 0.25, "start"]])
S("Emma standing in the dark living room doorway, red light glowing above her head and on her face, no digits anywhere in the image, scared.",
  "EMMA: [unsteady] Daniel. Look at me.", "Her forty-two years were gone. In their place, a new number. Eleven minutes, forty-two seconds.",
  chars=E, overlay={"type": "countdown", "mode": "live", "start_value": 702, "span": 2})
S("Daniel jumping up from the couch in horror, staring at Emma, the baby bottle slipping from his hand.",
  "DANIEL: [horrified] No. No, no, no.", "EMMA: Daniel, don't panic.", "DANIEL: [frantic] Eleven minutes, Emma! We have to do something!", chars=D)
S("Daniel frantically locking windows and unplugging appliances in a dark kitchen, rain outside.",
  "He checked every window. Locked every door. Turned off the stove. Unplugged everything he could reach. Emma watched him tear through the house.", chars=D)
S("Emma standing calmly in the kitchen, looking at Daniel with sudden clarity, red glow above her.",
  "EMMA: [quiet, steady] Daniel. What if it isn't counting down to something that happens to me? What if it's counting down to something I do?", chars=E)
S("Emma answering a ringing phone in the kitchen, her face falling, red glow above her.",
  "Before he could answer, her phone rang. A hospital. Her younger sister, Jess, had been in an accident. She was awake, but she couldn't make an urgent medical decision. Emma was her emergency contact. The doctors needed her. Now.",
  "Emma looked up. Eight minutes. She took the call.", chars=E,
  sfx=[["A smartphone ringing in a quiet room", 2.0, 0.35, "start"]])

# ---- Chapter 10 — The Choice
S("Emma at the kitchen table on a laptop video call with a doctor in scrubs, Daniel standing behind her, tense.",
  "The doctor laid it out carefully. Two treatment options. Both had risks. Neither came with a guarantee.", chars=E + D, cut=True)
S("Close-up of Emma listening intently, tears in her eyes, a faded childhood photo of two sisters on the table beside the laptop.",
  "Emma asked questions. She listened. And she thought about Jess. The little sister she used to walk to school. The woman she had barely spoken to in three years.", chars=E)
S("Daniel leaning over Emma's shoulder pleading, Emma looking back at him with firm resolve.",
  "DANIEL: [pleading] Emma, please. What if this is the moment?", "EMMA: [firm, tears in her eyes] Then I need to make the right choice for her.",
  "One minute.", chars=D + E, overlay={"type": "countdown", "mode": "spoken", "start_value": 60, "span": 3})
S("A doctor in scrubs on a laptop screen asking a serious question, hospital background.",
  "DOCTOR: Do you understand the risks?", "EMMA: [steady] Yes. Proceed.")
S("Daniel gripping Emma's hand on the kitchen table, both staring upward at the red glow, frozen.",
  "The number jumped. Ten seconds. Daniel grabbed her hand. Three. One. Zero.", chars=D + E)
S("Emma and Daniel holding each other in the kitchen at dawn, the red glow gone, rain stopped, soft blue light.",
  "Nothing happened. Emma was alive. The countdown vanished. And by morning, the doctors called back. The surgery had gone well. Jess was going to be okay.", chars=E + D)
S("Emma crying with relief at the kitchen window at sunrise.",
  "Emma cried. Not because she had escaped death. Because she finally understood. The numbers weren't telling people how much life they had left. They were telling them how long until life would never be the same again.", chars=E)

# ---- Chapter 11 — The World After the Truth
S("Dr. Brooks at a press conference podium facing a wall of cameras and microphones.",
  "Within days, Dr. Brooks published her findings. She was careful. Nothing was proven. No one knew where the numbers came from, or who, or what, had made them. But the evidence pointed one way. Turning points. Some ended in tragedy. Many ended in courage.", chars=B, cut=True, music="wonder")
S("A montage composition: a woman hugging her elderly father at a doorstep, a man walking out of an office smiling, people embracing in a park.",
  "The world changed again. People called estranged parents. People quit jobs they hated. Others became obsessed with forcing their numbers to zero, and governments begged them to stop.")
S("Thomas standing at the front door of a small suburban house on a sunny morning, Daniel opening the door holding the baby.",
  "A few days later, Thomas Reed knocked on the Carters' door. He wanted to meet the baby from the very first zero.", chars=T + D)
S(f"Thomas and Daniel sitting in a sunlit living room, Daniel holding {LILY}, Thomas leaning forward gently.",
  "THOMAS: [gentle] Daniel, in those ten seconds, before Lily's clock hit zero... what did you decide?", "Daniel looked at his daughter for a long time.", chars=T + D)
S(f"Close-up of Daniel looking down at {LILY} in his arms, eyes wet, soft smile.",
  "DANIEL: [quietly] I was supposed to go back to work that week. Eighty-hour weeks. I'd already missed half her first month. When I held her, I told her I wasn't going anywhere. And I meant it. I quit two days later.", chars=D)
S("Thomas smiling softly at Daniel and the baby, warm window light on his face.",
  "THOMAS: [smiling softly] Then that was her turning point. Not something that happened to her. Something that happened for her. She's going to grow up with a father who stayed.", chars=T)
S("Daniel on a backyard swing holding the baby, a faint pale blue glow above his head with no readable digits that he ignores, golden afternoon.",
  "Above Daniel's head, his own number still read sixty-three years. It never changed. And after that day, he stopped looking up at it.", chars=D)
S("A baby girl a few months old in the pink-and-blue striped hat laughing and reaching for her parents' hands on a blanket in the grass.",
  "Lily learned to smile. Then to laugh. Then to reach for her parents' hands.")
S("A quiet city street at dawn, a man looking up as the glowing number above his head freezes and flickers.",
  "But on the seventh morning... every countdown on Earth stopped.")

# ---- Chapter 12 — The Final Ten Seconds
S("A businessman on a New York sidewalk at 8 a.m. staring up as his glowing number freezes.",
  "Eight a.m. exactly. A businessman in New York watched his number freeze. A teacher in London saw hers dissolve. A student in Tokyo looked up as the glowing digits drifted away like dust.",
  cut=True, music="tension", sfx=[["Many ticking clocks all stopping at once, then silence", 3.0, 0.4, "start"]])
S("A crowded Tokyo intersection where glowing digits dissolve into drifting particles above everyone's heads.",
  "Within seconds, every personal countdown on Earth was gone.")
S("An enormous empty glowing red rectangular hologram frame filling the sky above a city skyline at dawn, no digits inside it, crowds in the streets looking up in terror.",
  "Then the sky changed. Above every city. Every ocean. Every mountain. One enormous number.", "Ten seconds.",
  overlay=dict(RED, span=7, color="#ff1e1e"),
  motion="Clouds churn around the enormous glowing red hologram in the sky as crowds below stop and stare upward, slow tilt up.")
S("People screaming and cars stopped in the middle of a city street, everyone staring at the red sky.",
  "People screamed. Cars stopped in the middle of the road. Dr. Brooks grabbed her phone.")
S("Dr. Brooks on a rooftop under the red sky holding a phone to her ear, urgent.",
  "BROOKS: [urgent] Thomas, what is happening?", "THOMAS: [afraid, for the first time] I hoped we'd have more time.", "Nine. Eight.", chars=B)
S("Thomas standing alone on a balcony under the red sky, the only person in view without fear, looking up.",
  "And suddenly she understood.", "BROOKS: [realizing] That's why you didn't have a number. Your turning point wasn't yours alone. It was this.",
  "THOMAS: [quiet] It's everyone's now.", "Seven. Six. Five.", chars=T)
S("Close-up of Dr. Brooks whispering into her phone, red light on her face, eyes wide.",
  "BROOKS: [whispering] Then what does this one mean?", "THOMAS: That humanity is about to make a choice.", chars=B)
S("A vast crowd in Times Square frozen, faces lit red, all looking up at the sky, holding their breath.",
  "Four. Three. Two. One.")
S("The sky over the city suddenly empty and grey, the red hologram gone, total stillness.",
  "Zero.", sfx=[["A deep low boom fading into total silence", 3.0, 0.4, "start"]])
S("Thousands of smartphones lighting up at once in a crowd's hands, all showing the same glowing white screen.",
  "The number disappeared. For one long second, nothing happened. Then every phone on Earth lit up with the same message.",
  motion="Phones light up one after another across the crowd, people lifting them in confusion, glow spreading.")
S("Close-up of a smartphone screen glowing white with two large buttons, cinematic, dark background.",
  "You have been given a choice. And beneath it, two buttons. Remember. Forget. No explanation. No instructions. Just two words.",
  overlay={"type": "text", "text": "YOU HAVE BEEN GIVEN A CHOICE|REMEMBER  ·  FORGET"})
S(f"Daniel in the kitchen holding his phone in one hand and {LILY} in the other, his thumb hovering over the screen, the baby's tiny fingers wrapping around his thumb.",
  "In the Carters' kitchen, Daniel held his phone in one hand and his daughter in the other. His thumb hovered over the screen. And Lily reached up and wrapped her tiny fingers around it.", chars=D,
  motion="The baby's tiny hand reaches up and wraps around Daniel's thumb above the glowing phone, slow push-in.")
S("Thomas alone on the balcony looking at his glowing phone, a faint sad smile.",
  "THOMAS: [softly] Now we find out what kind of species we really are.", chars=T, cut=True)
S("Pure black frame with a faint glowing red outline of a countdown display in the center.",
  "If you could see every turning point in your life coming... would you choose to remember? Or would you rather forget? Tell me what you'd press in the comments.",
  overlay={"type": "text", "text": "REMEMBER|OR FORGET?"})

LONG = {
    "title": "What If Everyone Could See Their Death Countdown?",
    "aspect": "16:9", "resolution": "2K", "tail": 3.0,
    "voices": VOICES, "cast": CAST, "portraits": PORTRAITS, "looks": LOOKS,
    "style": "Cinematic photorealistic film still, 16:9 widescreen, " + STYLE_TAIL,
    "places": {}, "ambiences": {}, "ambience": [],
    "music": music, "scenes": scenes,
}

CHAPTERS = """0:00 Ten Seconds
1:34 The Day the World Changed
2:56 The Price of Knowing
4:25 The Scientist
5:54 The Impossible Pattern
7:09 The Man Without a Number
8:06 Twenty Years Earlier
9:32 Can You Change Your Countdown?
11:05 The Second Number
12:05 The Choice
13:05 The World After the Truth
14:42 The Final Ten Seconds"""
TAGS = ["what if", "death countdown", "death clock", "sci-fi story", "mystery", "thriller", "turning point",
        "what if it happens", "short film", "fate", "free will", "ai film"]
LONG["thumbnail_file"] = "whatif/ep03_thumb.jpg"
LONG["youtube"] = {
    "title": "What If Everyone Could See Their Death Countdown?",
    "category": "24",
    "description": (
        "One morning, every human wakes up with a mysterious countdown above their head. "
        "But when a newborn baby's timer reaches zero, something impossible happens.\n\n" + CHAPTERS +
        "\n\nWould you press REMEMBER or FORGET? Tell me in the comments.\n\n"
        "A fictional sci-fi story. All characters and scenes are AI-generated.\n\n"
        "#whatif #scifi #deathclock #mystery #story"),
    "tags": TAGS,
}
LONG["shorts"] = [
    {"id": "short1", "youtube_title": "Your Baby Has 10 Seconds Left \u23F3 #shorts",
     "description": "Every human woke up with a countdown above their head. Hers said 10 seconds.\nFull story on the channel: What If Everyone Could See Their Death Countdown?\n\n#whatif #scifi #deathclock #shorts"},
    {"id": "short2", "youtube_title": "The Only Man With No Countdown \U0001F440 #shorts",
     "description": "Billions of people. Billions of countdowns. Except one man.\nThe answer is in the full episode on the channel.\n\n#whatif #scifi #mystery #shorts"},
]

# =============================== SHORT 1 ===============================
s1, m1, S = builder("a", 2)
S(f"Vertical close-up of a terrified father holding {LILY}, an empty glowing red hologram frame floating above the baby with no digits, dark hospital-like room with red light.",
  "[intense] You wake up. And there's a number floating above your baby's head.", chars=D, music="tension",
  overlay=dict(RED, span=7, start_value=10))
S(f"Close-up of {LILY} sleeping, red glow above her.", "Ten seconds.")
S("Emma in a kitchen doorway at dawn, hand over mouth, red light on her face.", "EMMA: [whispering] Daniel... what is that?", chars=E)
S("Daniel and Emma staring at each other in a dim room, a soft pale blue glow above each of their heads, no readable digits.",
  "Above your head: sixty-three years. Above your wife's: forty-two. Above your three-week-old daughter... five seconds.", chars=D + E)
S("Daniel clutching the baby, shouting toward Emma holding a phone.", "DANIEL: [panicked] Call somebody!", "Four.", "Three.", chars=D)
S(f"Daniel pressing his forehead against {LILY}, eyes shut, tears.", "DANIEL: [breaking] Please. I'm right here. I'm not going anywhere.", chars=D)
S(f"Macro close-up of {LILY}'s face in red light.", "Two.", "One.", "Zero.")
S(f"{LILY} smiling up in warm light, red glow gone.", "She smiles. She's alive. And the number is gone.",
  motion="The newborn blinks and breaks into a tiny smile, warm light, slow push-in.")
S("A smartphone exploding with notifications on a dresser.",
  "Then his phone explodes. Every human on Earth just woke up with a countdown. And it isn't counting what everyone thinks.",
  overlay={"type": "text", "text": "FULL STORY|ON THE CHANNEL"})
SHORT1 = dict({k: v for k, v in LONG.items() if k not in ("youtube", "shorts", "thumbnail_file")}, title="Your Baby Has 10 Seconds Left", title_band="YOUR BABY HAS|10 SECONDS LEFT", aspect="9:16", tail=2.5,
              scenes=s1, music=m1, style="Cinematic photorealistic film still, vertical 9:16 composition with the subject centered, " + STYLE_TAIL)

# =============================== SHORT 2 ===============================
s2, m2, S = builder("b", 2)
S("Vertical shot of a grey-bearded older man in a dark coat standing in a rainy crowded city street at night, everyone around him has a glowing red countdown above their head, he has none, he looks up.",
  "[mysterious] Every person on Earth woke up with a number above their head. Their countdown.", chars=T, music="tension",
  motion="The crowd moves around the still older man as he slowly lifts his gaze, rain falling through red glow.")
S("Grainy security camera footage of a crowded Washington D.C. train station, glowing numbers above everyone.",
  "Three days later, this video went viral. A train station in Washington, D.C. Thousands of people. Thousands of numbers.")
S("Security-camera view of the older man in a dark coat standing still in a moving crowd, no number above him.",
  "Except one man.", chars=T)
S("Close-up of the older man looking straight into the security camera with a faint smile.",
  "No countdown. He stops. He turns to the camera. And he smiles.", "THOMAS: [calm] You're all measuring the wrong thing.", chars=T)
S("A worn leather notebook on a metal table, its first page dated twenty years ago.",
  "His name is Thomas Reed. A math professor who vanished twenty years ago. And he has a notebook... dated twenty years before the numbers appeared.")
S("Dr. Brooks across a metal table from the older man, stunned.", "BROOKS: How did you know?", "THOMAS: [quietly] Because I've seen the numbers before.", chars=B)
S("Close-up of the older man's face under red light, no number above him, enigmatic.",
  "So why doesn't he have one?", chars=T, overlay={"type": "text", "text": "THE ANSWER IS IN|THE FULL EPISODE"})
SHORT2 = dict(SHORT1, title="The Only Man With No Countdown", title_band="THE ONLY MAN WITH|NO COUNTDOWN", scenes=s2, music=m2)

for name, spec in (("ep03_long.json", LONG), ("ep03_short1.json", SHORT1), ("ep03_short2.json", SHORT2)):
    ids = {s["id"] for s in spec["scenes"]}
    assert all(cue in ids for cue, _ in spec["music"]), name
    roles = {r for s in spec["scenes"] for r, _ in s["lines"]}
    assert roles <= set(VOICES), roles - set(VOICES)
    (HERE / name).write_text(json.dumps(spec, indent=1))
    words = sum(len(t.split()) for s in spec["scenes"] for _, t in s["lines"])
    print(f"{name}: {len(spec['scenes'])} scenes, {words} words, ~{words / 150:.1f} min, clips {sum(1 for s in spec['scenes'] if s.get('motion'))}")
