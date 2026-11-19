"""Build the specs for What If It Happens EP05: What If Eve Never Ate the Forbidden Fruit?

Animated comedy: 2D cartoon stills with light camera moves, cartoon voices designed for the show.
Script: the reviewed version in the "What If EP05 — Eve Never Ate the Fruit (수정본)" doc.
Run: python whatif/build_ep05.py -> whatif/ep05_long.json, ep05_short1.json, ep05_short2.json
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
CAST = {"eve": "whatif/cast/eve.jpg", "serpent": "whatif/cast/serpent.jpg",
        "adam": "video/public/assets/portrait_adam.jpg", "god": "video/public/assets/portrait_god.jpg",
        "noah": "video/public/assets/portrait_noah.jpg"}
TOON = "2D cartoon character portrait in a bold comic animation style, thick black outlines, flat vibrant warm colors, exaggerated friendly features, lush green garden background, "
PORTRAITS = {
    "adam": TOON + "a big friendly young man with a short dark curly beard and messy curly dark hair, simple brown tunic, goofy hopeful grin.",
    "god": TOON + "a kindly old man with a long flowing white beard and white hair, simple white robe, warm gentle smile, a soft golden glow around him.",
    "noah": TOON + "a short grumpy old man with a huge bushy grey beard, a sailor's captain hat, holding a clipboard, scowling.",
}
LOOKS = {
    "eve": "Eve: young woman with big curly brown hair with a leaf in it, green draped dress with a rope belt, same cartoon design as her reference",
    "serpent": "the Serpent: green cartoon snake with a monocle, red waistcoat and red bow tie, same cartoon design as his reference",
    "adam": "Adam: big friendly young man, short dark curly beard, brown tunic, same cartoon design as his reference",
    "god": "God: kindly old man with a long white beard, white robe, sandals, soft golden glow, same cartoon design as his reference",
    "noah": "Noah: short grumpy old man, huge grey beard, captain's hat, clipboard, same cartoon design as his reference",
}
VOICES = {"NARRATOR": "id:2rpzxhNBNuXVRJVjr5QH", "SERPENT": "id:bii88OaheA4bdDUwQuDd", "EVE": "id:P7jgmEXYk2gR2mB80OnS",
          "ADAM": "id:6NqMyKytfzLZlSWffLI0", "GOD": "id:dFnyy1eeXimhOPPSguMn", "NOAH": "id:5WiTd557XIKWEMi0mkNC",
          "NEIGHBOR": "Roger", "WOMAN": "Laura", "UPSTAIRS": "Jessica", "TOPFLOOR": "Chris", "MOSQUITO": "Matilda",
          "TOOTHBRUSH": "Eric", "DOWNSTAIRS": "Brian"}
GOAT = "a small white cartoon goat with a brown patch over one eye"
TREE = "the Tree of Knowledge rebuilt as a towering, wobbly treehouse apartment complex with dozens of crammed balconies, laundry lines and ladders"
STYLE_TAIL = "2D cartoon illustration in the same art style as the reference images: thick black outlines, flat vibrant warm colors, sunny lush Garden of Eden, exaggerated comedic expressions, animated comedy film look, no speech bubbles, no captions, one single image (never comic panels or split screens). Adam always wears his brown tunic; nobody is ever shirtless or dressed in leaves. "
E, S_, A, G, N = ["eve"], ["serpent"], ["adam"], ["god"], ["noah"]


def fx(prompt, seconds=1.5, volume=0.35, at="start"):
    return [prompt, seconds, volume, at]


def builder(prefix, width):
    scenes, music = [], []

    def S(image, *lines, chars=(), **extra):
        parsed = []
        for line in lines:
            role, sep, text = line.partition(": ")
            parsed.append([role, text] if sep and role in VOICES else ["NARRATOR", line])
        track = extra.pop("music", None)
        sfx = extra.pop("sfx", None)
        scene = {"id": f"{prefix}{len(scenes) + 1:0{width}d}", "chars": list(chars), "image": image, "lines": parsed, "place": ""}
        if sfx:
            scene["sfx"] = sfx if isinstance(sfx[0], list) else [sfx]
        scene.update(extra)
        scenes.append(scene)
        if track:
            music.append([scene["id"], track])
    return scenes, music, S


scenes, music, S = builder("L", 3)

# ---- 01 The Offer
S("Extreme close-up of a shiny red fruit hanging from a branch, the Serpent curled around the branch leaning toward the camera with a sly grin.",
  "SERPENT: [smooth, oily] One bite... and you'll know everything.", chars=S_, music="wonder", sfx=fx("Cartoon boing spring sound"))
S("Eve on a crowded balcony looking at the Serpent with a flat, unimpressed face, arms crossed.",
  "EVE: [flat, unimpressed] Do you know why my rent went up?", chars=E)
S("The Serpent beaming with delight, holding up a tiny inspection checklist.",
  "SERPENT: [delighted] Twelve percent! And your branch is due for inspection.", chars=S_)
S("Eve squinting suspiciously at the Serpent.", "EVE: [suspicious] How do you know that?", chars=E)
S("The Serpent unrolling an enormously long lease scroll that tumbles down the tree trunk and keeps going.",
  "SERPENT: [smug] I own the building.", chars=S_, sfx=fx("Long paper scroll unrolling with a comic whoosh", 2.0))
S(f"Wide shot revealing {TREE}, a neighbor on an upper balcony shaking a dusty rug onto a man eating breakfast on the balcony below.",
  "DOWNSTAIRS: [outraged] MY EGGS!", sfx=fx("A rug being beaten and a frying pan clatter", 1.5))
S("A sunny golden Garden of Eden with a single shiny gold coin falling through the air in the center, lots of empty sky at the top. No text, no letters, no signs anywhere.",
  "NARRATOR: [storybook, warm] Nine hundred years earlier, the serpent made Eve the very same offer.",
  overlay={"type": "text", "text": "WHAT IF EVE NEVER ATE|THE FORBIDDEN FRUIT?"}, sfx=fx("Cash register cha-ching", 1.2), cut=True)
S("The same branch with the red fruit in an empty, peaceful, untouched Garden of Eden, the Serpent leaning toward Eve.",
  "SERPENT: [smooth] One bite... and you'll know everything.", chars=S_ + E)
S("Eve narrowing her eyes at the Serpent, one eyebrow raised.", "EVE: [narrowing her eyes] How much does it cost?", chars=E)
S("The Serpent grinning far too widely, sweating slightly.", "SERPENT: [way too fast] It's free!", chars=S_)
S("Eve leaning back, deeply suspicious.", "EVE: [suspicious] Then why are you talking like that?", chars=E)
S("Eve walking away into the garden while the Serpent stares after her, puzzled.",
  "SERPENT: [muttering] Too much eye contact?", chars=S_ + E)
S("Adam cheerfully dragging a huge log past the tree, pointing at an empty branch.",
  "ADAM: [cheerful, oblivious] Hey! Can I put a shelf here?", chars=A, sfx=fx("A heavy log scraping across grass", 1.5))
S("The Serpent looking at Adam, then at the many empty branches, his pupils turning into little gold coins.",
  "SERPENT: [slow, delighted whisper] ...Absolutely.", chars=S_, sfx=fx("Twinkling coin sparkle sound", 1.2))
S("Adam happily hammering a single small shelf onto the giant empty tree as the Serpent holds out a contract and a quill.",
  "NARRATOR: And that is how the first lease was signed.", chars=A + S_)

# ---- 02 Five Minutes of Sun
S("A sunny Garden of Eden filled with happy families, babies everywhere, new treehouse floors going up on every tree.",
  "NARRATOR: In this Eden, nobody ever ate the fruit. So nobody ever left. People grew up, but nobody grew old. Babies kept coming. And so did the second floors.",
  cut=True, music="wonder")
S("Eve setting a little wooden chair in a perfect square of sunlight at the foot of the crowded tree, smiling.",
  "EVE: [content sigh] Ahh. Finally.", chars=E)
S("A new balcony swinging out right above Eve, casting her chair into shadow, Eve looking up furious.",
  "EVE: [furious] HEY! You just built over my sun!", chars=E, sfx=fx("A loud wooden CLUNK", 1.0))
S("Adam leaning over the new balcony railing above, surprised and waving.", "ADAM: [from above, surprised] Eve?", chars=A)
S("Eve staring up in disbelief.", "EVE: [disbelieving] Adam?! You live up there?", chars=E)
S("Adam proudly gesturing around his tiny balcony, a woman's deck visible directly above him.",
  "ADAM: [proud] Since breakfast! The woman above me put in a deck.", chars=A)
S("A woman on the deck above Adam, hands on hips, defensive, pointing upward.",
  "UPSTAIRS: [defensive] I HAD to! The man above me got a goat!")
S("A man on a very high balcony shouting down with cupped hands.",
  "TOPFLOOR: [shouting down] HALF a goat! My brother has him on weekends!")
S(f"Two neighboring balconies, {GOAT} stretched across the gap so the same goat's head pokes over both railings.",
  "NARRATOR: [amused] It was the same goat.", sfx=fx("A goat bleating loudly", 1.5))
S("Eve climbing a rickety ladder up the crowded tree toward a sunny landing, determined.",
  "NARRATOR: So Eve climbed. And every time she reached a sunny landing...", chars=E)
S("Eve reaching a sunny landing just as a new floor slams into place above her, plunging her into shadow, Eve furious.",
  "NARRATOR: ...somebody built a new floor over it.", chars=E, sfx=fx("Three wooden CLUNKs in a row", 2.0))
S("At the very top of the tree, the Serpent lounging beside an empty deck chair in full sun with a sand timer, Eve arriving panting.",
  "EVE: [panting, furious] There you are. MOVE. THE CHAIR. I just want to sit in the sun!", chars=E + S_)
S("The Serpent sweetly holding up the sand timer.", "SERPENT: [sweet] Two figs. Five minutes.", chars=S_)
S("Eve outraged, arms thrown wide.", "EVE: [outraged] You're charging me for the SUN?!", chars=E)
S("The Serpent smugly patting the chair.", "SERPENT: [patient, smug] The sun is free. You're paying for the chair.", chars=S_)
S("Eve sitting on the floor beside the chair as the Serpent opens a parasol over her head, blocking the sun.",
  "EVE: [through gritted teeth] How much to close that?", chars=E + S_, sfx=fx("An umbrella popping open", 1.0))
S("The Serpent beaming proudly like a teacher.", "SERPENT: [proud] Look at you. Asking the right questions!", chars=S_)

# ---- 03 The Waiting List
S("A long, winding line of people stretching across the garden, some sleeping in line, one holding a sign.",
  "NARRATOR: By the third century, the waiting list had a waiting list.", cut=True)
S("Adam hanging a big wooden sign at the garden gate that reads EDEN IS FULL, a very pregnant woman tapping his shoulder.",
  "WOMAN: [desperate] My baby's due TODAY. Where do I put him?", chars=A)
S("Adam turning with a polite, clueless smile, holding a tiny clipboard.", "ADAM: [polite, clueless] Do you have a reservation?", chars=A)
S("The pregnant woman staring at Adam in stunned silence, Adam sweating nervously.",
  "ADAM: [nervous] Right. Of course. Uh... how small are we thinking?", chars=A, sfx=fx("A single cricket chirping", 1.5))
S("A tired older neighbor handing Eve a cracked clay token marked with a big number.",
  "NEIGHBOR: [weary] Is this still good? I've been waiting for a ground-floor unit since I was thirty.", chars=E)
S("Eve looking sympathetic, holding the clay token.", "EVE: [sympathetic] Oh no. How old are you now?", chars=E)
S("The neighbor's completely deadpan face, close-up.", "NEIGHBOR: [deadpan] Thirty.")
S("Eve turning to Adam, exasperated, pointing across a small sparkling creek to an empty green meadow.",
  "EVE: [exasperated] Why don't we just build on the OTHER side of the creek?!", chars=E + A)
S("Adam earnestly explaining, hands raised.", "ADAM: [earnest] I asked the serpent. He said it's too dangerous to cross on foot.", chars=A)
S("Eve leaning in, slow and suspicious.", "EVE: [slow, suspicious] Did he say that before... or AFTER he started selling boat tickets?", chars=E)
S("Adam looking down at an enormous teetering stack of boat tickets in his arms.",
  "ADAM: [small voice] ...There was a group rate.", chars=A)
S("Eve alone, dangerously calm, one eye twitching, no other people.", "EVE: [dangerously calm] How many did you buy?", chars=E)
S("Adam proudly holding up the ticket stack, then shrinking.", "ADAM: [proud, then shrinking] Enough to make it a very good deal.", chars=A)
S("The bow of a huge wooden ark backing slowly into the garden past the trees, people jumping aside.",
  "NARRATOR: And then the ark backed into the garden.", sfx=fx("A huge ship horn then truck reversing beeps", 3.0))
S("The middle of the enormous ark's hull still sliding past the trees, endless planks.",
  "NARRATOR: It took...", sfx=fx("Truck reversing beeps", 2.0))
S("Still the middle of the ark's hull, even longer, people sitting down to wait.",
  "NARRATOR: [deadpan] ...a while.", sfx=fx("Truck reversing beeps", 2.0))
S("A giraffe on the ark's deck popping up from under a clothesline wearing three pairs of shorts around its neck.",
  "NARRATOR: [amused] The giraffe took that personally.", sfx=fx("A silly cartoon slide whistle", 1.2))

# ---- 04 Two of Every Kind
S("Noah at the ark's ramp holding a clipboard, a crowd led by Eve and Adam arriving carrying chairs, beds and a bathtub.",
  "NOAH: [gruff, bored] All right. Two of every kind.", chars=N + E + A, cut=True, music="tension")
S("Adam excited, waving his tickets.", "ADAM: [excited] Great! Two from each family?", chars=A)
S("Noah flat and unimpressed.", "NOAH: [flat] Two humans.", chars=N)
S("The whole crowd slowly turning to stare at Adam, who quietly lowers his stack of tickets.",
  "EVE: [to Noah] How many tickets did you actually sell him?", chars=A + E)
S("Noah checking his clipboard.", "NOAH: Two. He bought standby.", chars=N)
S("Adam confused, scratching his head.", "ADAM: [confused] I thought that meant we could stand!", chars=A)
S("Noah pointing to a spot on the grass one step farther from the ramp.", "NOAH: [pointing] It means you can stand... right there.", chars=N + A)
S("Adam indignant, pointing at the ark.", "ADAM: [indignant] Fine! What about the mosquitoes? Give me THEIR seats!", chars=A)
S("Noah shrugging and pointing past Adam, Adam in his brown tunic.", "NOAH: You can ask. They're behind you.", chars=N + A)
S("Two snooty cartoon mosquitoes in tiny hats pulling a tiny suitcase past the line.",
  "MOSQUITO: [tiny, high-pitched, snooty] Excuse us. We checked in online.", sfx=fx("A buzzing mosquito flying past", 1.5))
S("Adam outraged, pointing at the mosquitoes flying up the ramp.", "ADAM: [outraged] THEY CAN FLY!", chars=A)
S("Noah completely deadpan.", "NOAH: [deadpan] The giraffes can walk. I'm trying to make this fair.", chars=N)
S(f"{GOAT} on the ramp happily chewing the passenger list while Eve narrows her eyes at Noah.",
  "EVE: [narrowing her eyes] Noah. How deep is the creek today?", chars=E)
S("Noah alone on the ark ramp puffing out his chest proudly, no other people.", "NOAH: [proud] Deep enough to float my boat.", chars=N)
S("The huge ark grinding against a rock in a tiny shallow creek, everyone wincing.",
  "NARRATOR: [deadpan] The boat disagreed.", sfx=fx("A long slow wooden scraping groan", 2.5))

# ---- 05 The Lifetime Lease
S("A tiny cluttered treehouse apartment, Adam stuffing a bathtub into a travel bag, Eve throwing up her hands.",
  "EVE: [exasperated] Leave the bathtub!", "ADAM: [hurt] You said pack the things that are hard to replace!", chars=E + A, cut=True)
S("Eve shouting, pointing out the window at the creek.", "EVE: [shouting] WE HAVE A CREEK!", "ADAM: [small] The boat guy says we can't use it.", chars=E + A)
S("Eve crouching to look at stone clay tablets wedged under a wobbly table leg.",
  "EVE: What are these?", "ADAM: [cheerful] The lease!", chars=E + A)
S("Eve horrified, holding up the clay tablets.", "EVE: [horrified] You're using the LEASE to hold up the TABLE?!", chars=E)
S("Adam proudly patting the wobbly table.", "ADAM: [proud] It's the only thing in this house with a lifetime guarantee!", chars=A)
S("The table tilting, a fig rolling off and out the window, the Serpent outside catching it with his tail.",
  "SERPENT: [sing-song] Late fee!", chars=S_, sfx=fx("A crash and a comic catching pop", 1.5))
S("The Serpent sliding a fresh notice under the door that reads RENT +12%.",
  "SERPENT: [smug] Oh, and twelve percent. Starting Monday.", chars=S_)
S("Eve staring at the notice, realizing, the opening scene's branch visible through the window.",
  "NARRATOR: [wry] And that brings us back to where we started.", chars=E)
S("Eve standing firm, arms crossed, facing the Serpent at the window.",
  "EVE: [firm] We're moving out.", "SERPENT: [sweet] I'll need Adam's permission. He signed for the whole tree.", chars=E + S_)
S("Eve slowly turning her head toward Adam with an icy stare, Adam in his brown tunic sweating.", "EVE: [slowly turning] Adam. Why did you sign for the WHOLE TREE?", chars=E + A)
S("Adam defensive, holding up his hands.", "ADAM: [defensive] It was just a shelf at the time!", chars=A)
S("Eve leaning in.", "EVE: And the LIFETIME part?", chars=E)
S("Adam brightly holding up a small plain wooden bowl like a trophy.", "ADAM: [brightening] We got a free bowl!", chars=A)
S("Eve shoving the wooden bowl at the Serpent.", "EVE: Here. We're even.", chars=E + S_)
S("The Serpent examining the bowl with a jeweler's loupe.", "SERPENT: [examining it] You've had it for three hundred years. I'll have to charge for wear.", chars=S_)
S("Eve snatching the bowl back and storming out the door, Adam calling after her.",
  "ADAM: [calling after her] Where are you going?!", "EVE: [determined] To find somebody who remembers who planted this tree!", chars=E + A)

# ---- 06 The Complaint Department
S("At the giant roots of the tree, Eve pulling an old brass handbell out of the moss beside a mossy stone plaque.",
  "NARRATOR: At the very bottom of the tree, under nine hundred years of moss, Eve found something.", chars=E, cut=True, music="wonder")
S("Adam nervously peering at the bell over Eve's shoulder.", "ADAM: [nervous] Eve, I think that's for REAL emergencies.", chars=A + E)
S("A bathtub smashed into the grass exactly where Adam was standing, Adam one step to the side, frozen, hair standing up.",
  "ADAM: [high-pitched] Ring it twice.", chars=A, sfx=fx("A long falling whistle then a big comic crash", 2.0))
S("Eve ringing the brass bell, the whole crowded tree frozen mid-motion, thunder clouds rolling in far away.",
  "NARRATOR: [hushed] Everyone froze.", chars=E, sfx=[fx("Two clear bell rings", 1.5), fx("Distant rolling thunder", 2.5, 0.3, "end")])
S("Noah on the ark's deck far away, shouting triumphantly with his hands cupped.",
  "NOAH: [from the dock, triumphant] I TOLD you it was gonna rain!", chars=N)
S("Eve shouting back across the garden.", "EVE: [shouting back] You told me the END was near!", chars=E)
S("Noah shouting back.", "NOAH: [shouting] The end of BOARDING!", chars=N)
S("Light rain, every balcony of the tree draining onto the one below, a man on the lowest floor calmly opening an umbrella indoors without looking up.",
  "NARRATOR: [wry] It barely drizzled. But on a tree with four hundred floors, it rained on the bottom for a week.", sfx=fx("Light rain dripping and splashing", 3.0, 0.3))
S("The garden gate, the Serpent at a little booth with a cash box and his best smile, only a pair of glowing sandals visible stepping up.",
  "SERPENT: [salesman voice] Two figs to get in!", chars=S_, sfx=fx("A little gate bell jingle", 1.0))
S("Close-up of the glowing sandals and the hem of a white robe at the gate.", "GOD: [calm, warm, slightly amused] I made this garden.")
S("The Serpent alone in his little ticket booth at the garden gate, grinning, no other people.", "SERPENT: [without missing a beat] Then you remember when it was free!", chars=S_)
S("God stepping into frame softly glowing, kind and calm, while Adam slowly hides a wooden bowl behind his back.",
  "NARRATOR: [hushed] Adam hid the bowl.", chars=G + A, sfx=fx("A soft heavenly choir chord", 2.0))

# ---- 07 Who Owns the Tree?
S("Eve pointing furiously from God to the Serpent.", "EVE: [pointing, outraged] You said we couldn't eat from ONE tree! How did HE end up owning it?!", chars=E, cut=True)
S("God calm and firm, hand raised gently.", "GOD: [gentle, firm] He doesn't own it.", chars=G)
S("The Serpent hissing a whisper behind his tail, a man far above holding a pen over a contract.",
  "SERPENT: [hissed whisper] Could you say that a little quieter? I'm signing somebody for the top floor.", chars=S_)
S("God looking up patiently at the towering tree.", "GOD: [patient] Adam. How many floors did you put on that tree?", chars=G)
S("Adam thinking very hard, counting on his fingers.", "ADAM: [thinking hard] Counting the shelf?", chars=A)
S("God leaning back, then stepping back, squinting up at a tree so tall it disappears into the clouds.",
  "GOD: [squinting] I can't see the shelf.", chars=G)
S("God alone catching a falling wooden shutter with a little hanging sign, no other people.", "GOD: [reading slowly] Original... garden view.", chars=G, sfx=fx("A wooden shutter clattering", 1.0))
S("The Serpent proudly presenting the shutter like a real estate agent.", "SERPENT: [proud] That's our premium unit.", chars=S_)
S("God peeking through the shutter's opening, a man right on the other side brushing his teeth, foam everywhere.",
  "GOD: [politely] Hello.", "TOOTHBRUSH: [mouth full of foam, annoyed] Do you MIND?!", chars=G)
S("God handing the shutter to Adam, kind and tired.", "GOD: [kind, tired] Adam... you know there's land on the other side of the creek, right?", chars=G + A)
S("Adam confident, pointing at the giant ark.", "ADAM: [confident] We're waiting for the boat.", "GOD: Why?", chars=A + G)
S("Adam gesturing grandly at the enormous ark sitting in the tiny creek.",
  "ADAM: [as if it's obvious] Look at it! He built a boat THAT big. You don't build a boat that big for a little creek!", chars=A)
S("Noah alone poking his head over the ark's rail, helpful, no other people.", "NOAH: [helpful] I built it on a hill. Adam paid extra to have it brought here.", chars=N)
S("Eve slowly turning to glare at Adam, who looks defensive.", "ADAM: [defensive] The delivery was free! We paid to turn it AROUND.", chars=E + A)

# ---- 08 The Goat
S(f"{GOAT} trotting down the ark's ramp toward the creek with the passenger list in its mouth, Noah chasing.",
  "NOAH: [panicked] HEY! You're CHECKED IN!", chars=N, cut=True, music="tension")
S(f"{GOAT} stepping into the creek, everyone on the bank holding their breath.",
  "NARRATOR: [hushed] Everyone held their breath. The water came up...", sfx=fx("A small splash", 1.0))
S(f"{GOAT} standing in the creek with the water barely reaching its knees, looking bored.",
  "NARRATOR: [deadpan] ...to its knees.", sfx=fx("A single cricket chirping", 1.5, 0.3, "end"))
S(f"{GOAT} on the far bank happily munching grass in a wide, sunny, empty meadow, the whole crowd staring from the other side.",
  "EVE: [very quiet, very dangerous] Adam. Did you ever check how deep it was?", chars=E)
S("Adam shrinking to a tiny size in embarrassment.", "ADAM: [tiny] I asked Noah.", chars=A)
S("Eve exploding with rage, steam coming out of her ears.", "EVE: [exploding] You asked the guy SELLING THE BOAT TICKETS?!", chars=E, sfx=fx("A cartoon kettle whistle", 1.0))
S("God hitching up his robe and wading across the shallow creek, the pregnant woman following holding her shoes.",
  "WOMAN: [hopeful] Can we just... live over here?", chars=G)
S("God turning, smiling warmly.", "GOD: [warm] Yes.", chars=G)
S("The pregnant woman suspicious.", "WOMAN: [suspicious] Do we need a number?", "GOD: [puzzled] For what?", chars=G)
S("A single image of the tired old neighbor kneeling at the creek fishing his cracked clay token out of the water.",
  "NEIGHBOR: [deadpan] I waited a long time for that.", sfx=fx("A tiny plop", 0.8))
S("The whole crowd stampeding across the shallow creek in a giant splash, carrying beds and chairs.",
  "NARRATOR: And then everybody ran.", sfx=fx("A huge crowd running and splashing through water", 2.5))
S("Two people on the far bank holding a door upright between them, each politely gesturing for the other to go first.",
  "NARRATOR: [amused] Some habits take longer to leave.")

# ---- 09 Garden View
S("Eve in her little chair in the middle of a wide-open sunny meadow, eyes closed, face lifted to the sun, blissful.",
  "EVE: [blissful sigh] Ohhh. That's the stuff.", chars=E, cut=True, music="wonder")
S("Adam setting the bathtub down beside Eve's chair with a thud, beaming.",
  "EVE: [eyes still closed] Why did you bring that?", "ADAM: [proud] It's paid off.", chars=E + A, sfx=fx("A heavy thud", 0.8))
S("The Serpent sliding in with a tiny potted cutting of the tree and a little sign that reads GARDEN VIEW 2 FIGS EXTRA.",
  "NARRATOR: [wry] Of course.", chars=S_)
S("God walking up, frowning at the potted cutting.", "GOD: [frowning] Is that my tree?", "SERPENT: [innocent] It's a cutting.", chars=G + S_)
S("God alone, stern, arms crossed, no other people.", "GOD: [stern] Did you ask?", chars=G)
S("A single image of the Serpent beside a potted plant, brightening with a big salesman grin.", "SERPENT: [brightening] Would you like to invest?", chars=S_)
S("The Serpent holding out a contract to God, Adam reaching for the pen, Eve with eyes still closed plucking the pen out of Adam's hand.",
  "NARRATOR: [amused] Eve never even opened her eyes.", chars=S_ + A + E)
S("God sitting on the edge of Adam's bathtub in the meadow, watching the crowd and the impossibly tall tree across the creek, tired.",
  "GOD: [tired sigh, to himself] Maybe she should've just eaten the fruit.", chars=G, cut=True)
S("A wobbly dreamy thought bubble: Eve biting the red fruit, thunder, Adam and Eve walking out of the garden gate heads down into a wide empty wilderness.",
  "GOD: [dreamy, smiling] Everybody leaves. Quiet garden. No balconies. No goat...", sfx=fx("A dreamy harp glissando", 2.0))
S("Inside the thought bubble, just past the garden gate, a huge billboard reading EAST OF EDEN LUXURY CONDOS, the Serpent in a hard hat waving at Adam and Eve.",
  "SERPENT: [cheerful] Welcome! First month free!", chars=S_)
S("The thought bubble popping, God staring blankly into space.", "GOD: [flat] ...Never mind.", chars=G, sfx=fx("A bubble pop", 0.6))
S(f"{GOAT} bleating right into God's ear, God wincing.", "NARRATOR: [warm] The end.", chars=G, sfx=fx("A loud goat bleat", 1.5, 0.4))

LONG = {
    "title": "What If Eve Never Ate the Forbidden Fruit?",
    "aspect": "16:9", "resolution": "2K", "tail": 2.0,
    "voices": VOICES, "cast": CAST, "portraits": PORTRAITS, "looks": LOOKS,
    "style": STYLE_TAIL, "places": {}, "ambiences": {}, "ambience": [], "music": music,
    "scenes": scenes,
    "thumbnail_file": "whatif/ep05_thumb.jpg",
}

# ---- Short 1 — I Own the Building
s1, m1, S = builder("a", 2)
S("Vertical close-up of a shiny red fruit on a branch, the Serpent curled around it grinning slyly.",
  "SERPENT: [smooth, oily] One bite... and you'll know everything.", chars=S_, music="wonder")
S("Eve on a crowded balcony, flat and unimpressed.", "EVE: [flat] Do you know why my rent went up?", chars=E)
S("The Serpent delighted, holding a checklist.", "SERPENT: [delighted] Twelve percent! And your branch is due for inspection.", chars=S_)
S("Eve suspicious.", "EVE: [suspicious] How do you know that?", chars=E)
S("The Serpent unrolling an endless lease scroll down the tree.", "SERPENT: [smug] I own the building.", chars=S_)
S(f"Vertical view of {TREE}, a neighbor shaking a rug onto another's breakfast below.", "DOWNSTAIRS: [outraged] MY EGGS!")
S("A golden garden with a gold coin dropping out of a big letter O.",
  "NARRATOR: [storybook] In this Eden, nobody ever ate the fruit. And now... Eden is full.",
  overlay={"type": "text", "text": "FULL EPISODE|ON THE CHANNEL"})
SHORT1 = dict({k: v for k, v in LONG.items() if k != "thumbnail_file"}, title="I Own the Building", title_band="WHAT IF EVE NEVER|ATE THE FRUIT?",
              aspect="9:16", tail=2.0, scenes=s1, music=m1, style=STYLE_TAIL + "Vertical 9:16 composition. ")

# ---- Short 2 — The Goat Knew
s2, m2, S = builder("b", 2)
S("Vertical: the whole crowd of Eden waiting by a tiny creek next to a giant ark, Adam holding a huge stack of boat tickets.",
  "NARRATOR: [storybook] Everyone in Eden was waiting for the boat. The serpent said the creek was too dangerous.", chars=A, music="tension")
S(f"{GOAT} trotting down the ark's ramp with the passenger list in its mouth, Noah chasing.", "NOAH: [panicked] HEY! You're CHECKED IN!", chars=N)
S(f"{GOAT} stepping into the creek, everyone holding their breath.", "NARRATOR: [hushed] The water came up...")
S(f"{GOAT} standing in water that barely reaches its knees, bored.", "NARRATOR: [deadpan] ...to its knees.")
S("Eve turning to Adam, very quiet and very dangerous.", "EVE: [very quiet] Adam. Did you ever check how deep it was?", chars=E)
S("Adam shrinking.", "ADAM: [tiny] I asked Noah.", chars=A)
S("Eve exploding with steam out of her ears.", "EVE: [exploding] You asked the guy SELLING THE BOAT TICKETS?!", chars=E,
  overlay={"type": "text", "text": "FULL EPISODE|ON THE CHANNEL"})
SHORT2 = dict(SHORT1, title="The Goat Knew", title_band="THE GOAT|KNEW", scenes=s2, music=m2)

LONG["youtube"] = {
    "title": "What If Eve Never Ate the Forbidden Fruit? | A Bible Story Reimagined",
    "category": "23",
    "description": "In this Eden, nobody ever ate the forbidden fruit. So nobody ever left... and nine hundred years later, the Garden is FULL. The serpent is the landlord, Adam signed a lifetime lease, Noah is selling boat tickets, and Eve just wants five minutes of sun.\n\nA funny animated Bible story, reimagined.\n\n#whatif #bible #comedy #animation #eden",
    "tags": ["what if", "eve", "forbidden fruit", "garden of eden", "bible comedy", "animated comedy", "serpent", "noah's ark", "funny", "what if it happens"],
}
LONG["shorts"] = [
    {"id": "short1", "youtube_title": "The Serpent Owns the Building \U0001F40D #shorts", "description": "In this Eden, nobody ate the fruit. Now the serpent is the landlord.\nFull episode on the channel.\n\n#whatif #eden #comedy #animation #shorts"},
    {"id": "short2", "youtube_title": "The Goat Knew All Along \U0001F410 #shorts", "description": "Everyone waited for the boat. The goat just walked.\nFull episode on the channel.\n\n#whatif #eden #comedy #animation #shorts"},
]

for name, spec in (("ep05_long.json", LONG), ("ep05_short1.json", SHORT1), ("ep05_short2.json", SHORT2)):
    ids = {s["id"] for s in spec["scenes"]}
    assert all(cue in ids for cue, _ in spec["music"]), name
    assert all(t for s in spec["scenes"] for _, t in s["lines"]), name
    assert {r for s in spec["scenes"] for r, _ in s["lines"]} <= set(VOICES)
    (HERE / name).write_text(json.dumps(spec, indent=1))
    words = sum(len(t.split()) for s in spec["scenes"] for _, t in s["lines"])
    print(f"{name}: {len(spec['scenes'])} scenes, {words} words")
