"""Assemble the full Episode 1 spec (karma/ep01_full.json) from the Act 1 spec plus Acts 2-7 and the epilogue."""
import json
from pathlib import Path

HERE = Path(__file__).parent
spec = json.loads((HERE / "ep01_act1.json").read_text())
spec["title"] = "Karma Tales EP01 - The Wedding Trap"
spec["style"] = (
    "Photorealistic still from a prestige American TV drama, shot on 35mm, cinematic lighting, shallow depth of field, "
    "natural skin texture, wide 16:9 frame. Keep every person's face and hair exactly consistent with their reference photo. "
    "No text, no captions, no watermark. "
)
spec["places"] = {
    "ballroom": "Setting: a lavish Manhattan hotel ballroom wedding reception at night with crystal chandeliers, white flowers and candlelight.",
    "hall": "Setting: the dim hallway of an upscale Manhattan apartment on a rainy night.",
    "apt": "Setting: the living room of an upscale Manhattan apartment with floor-to-ceiling windows.",
    "elevator": "Setting: inside a mirrored apartment-building elevator at night.",
    "taxi": "Setting: the back seat of a New York taxi on a rainy night.",
    "kitchen": "Setting: a comfortable suburban kitchen at midnight, one lamp on.",
    "office": "Setting: a wood-paneled Manhattan law office in morning light, bookshelves, an oak desk, leather chairs.",
    "bedroom": "Setting: a quiet bedroom in gray dawn light.",
    "city": "Setting: New York City.",
    "brooklyn": "Setting: a bright, newly renovated brick loft-style commercial building in Brooklyn in daytime, tall windows, fresh wood floors.",
    "memory": "Setting: a warm study with bookshelves.",
}
spec["cast"].update({"evelyn": "karma/cast/evelyn.jpg", "marcus": "karma/cast/marcus.jpg", "harris": "karma/cast/harris.jpg"})
same = "the same person as the reference photo, same face and hair, but wearing "
spec["looks"].update({
    "claire:work": f"Claire ({same}a camel wool coat over a cream blouse instead of the wedding gown)",
    "claire:home": f"Claire ({same}a gray cashmere sweater instead of the wedding gown)",
    "claire:brooklyn": f"Claire ({same}a tailored white blazer and jeans instead of the wedding gown)",
    "daniel:home": f"Daniel ({same}a white dress shirt with rolled sleeves instead of the tuxedo)",
    "evelyn": "Evelyn (the woman from the reference photo with chin-length auburn hair, in an emerald green dress and pearl earrings)",
    "evelyn:home": f"Evelyn ({same}a navy cardigan over a nightgown)",
    "evelyn:office": f"Evelyn ({same}a tan trench coat)",
    "evelyn:brooklyn": f"Evelyn ({same}a cream blazer)",
    "marcus": "Marcus (the man from the reference photo with close-cropped graying hair and wire-rimmed glasses, in a charcoal three-piece suit)",
    "harris": "Detective Harris (the man from the reference photo with short brown hair, in a tan trench coat over a shirt and dark tie)",
})
spec["ambiences"] = {
    "ballroom": ["Soft murmur of a large elegant crowd in a hotel ballroom, occasional clink of glasses, no music", 0.07],
    "hush": ["Tense hushed crowd in a large ballroom, faint whispers and shifting chairs, no music", 0.06],
    "rain": ["Steady rain against apartment windows at night, quiet room", 0.10],
    "office": ["Quiet office room tone, faint air conditioning, distant muffled city traffic", 0.06],
}
spec["ambience"] = [["s01", "ballroom"], ["s11", "hush"], ["s22", "rain"], ["s33", "none"], ["s36", "office"], ["s46", "none"], ["s54", "office"], ["s57", "hush"], ["s97", "none"]]
spec["music"] = [["s01", "tension"], ["s36", "wonder"], ["s46", "tension"], ["s95", "wonder"]]

CLICK = ["A single mechanical click of a slide projector remote", 1.0, 0.5, "start"]
BOOM = ["Deep cinematic boom impact with a low sub drop", 3.0, 0.45, "start"]
act1_sfx = {
    "s06": [["Polite applause from a large formal crowd", 4.0, 0.22, "start"]],
    "s10": [CLICK],
    "s11": [BOOM],
    "s14": [["A champagne glass shattering on a marble floor", 2.0, 0.5, "start"]],
    "s20": [CLICK],
}
for sc in spec["scenes"]:
    sc["place"] = "ballroom"
    if sc["id"] in act1_sfx:
        sc["sfx"] = act1_sfx[sc["id"]]

n = len(spec["scenes"])


def S(place, chars, image, lines, **extra):
    global n
    n += 1
    scene = {"id": f"s{n:02d}" if n < 100 else f"s{n}", "place": place, "chars": chars, "image": image,
             "lines": [list(map(str.strip, l.split(":", 1))) for l in lines]}
    scene.update(extra)
    spec["scenes"].append(scene)


N, C, D, V, R, M, E, H = "NARRATOR", "CLAIRE", "DANIEL", "VANESSA", "RICHARD", "MARCUS", "EVELYN", "DETECTIVE"

# ---------------- ACT 2: nineteen days earlier ----------------
S("apt", [], "Rain-streaked floor-to-ceiling windows of a dark, empty living room, city lights blurred beyond.",
  [f"{N}: Nineteen days earlier, Claire came home from a business trip two days ahead of schedule. She was supposed to be in Boston until Friday. A canceled meeting had changed her plans. And that small change would save everything she had built."], cut=True)
S("hall", ["claire:work"], "Claire stepping in through the front door with a rolling suitcase and a paper takeout bag, coat damp, the apartment dim and quiet.",
  [f"{N}: Claire let herself into the apartment carrying takeout from Daniel's favorite restaurant. She heard voices from the bedroom."])
S("hall", ["claire:work"], "Claire frozen in the dim hallway, staring at a bedroom door left slightly ajar with warm light spilling out.",
  [f"{V}: [low, intimate] She really doesn't suspect anything?", f"{D}: [amused] Claire? Please. She thinks we're planning her birthday surprise.", f"{V}: And after the wedding?", f"{D}: [matter-of-fact] We wait six months. Then I file for divorce."])
S("hall", ["claire:work"], "Close-up of Claire's hand gripping a paper takeout bag so hard it crumples, knuckles white.",
  [f"{V}: And the money?", f"{D}: My father's handling that.", f"{N}: Claire froze. The takeout bag slipped slightly in her hand."])
S("hall", ["claire:work"], "Close-up of Claire's face in shadow, eyes glistening, a strip of warm light from the door across one cheek.",
  [f"{V}: [pleading] You promised me we'd be together.", f"{D}: [soothing] We will. But first, we need the Bennett money."])
S("memory", [], "A framed black-and-white photograph of a dignified elderly man in a suit standing in front of a brick commercial building, resting on a bookshelf.",
  [f"{N}: Claire's grandfather had left her a substantial inheritance. Not cash sitting in a checking account. A trust. Investments and commercial properties worth millions."])
S("apt", ["daniel:home", "claire:home"], "Daytime. Daniel on a sofa leaning over Claire's shoulder, pointing at a thick folder of legal documents on a coffee table, smiling reassuringly.",
  [f"{N}: Daniel had spent two years convincing Claire that his love had nothing to do with her money. Now she understood why he kept asking about the trust documents. Why he wanted their finances combined. And why he had insisted that his father's attorney handle the paperwork."])
S("hall", ["claire:work"], "Claire backing away down the hallway on tiptoe, holding her phone low with its screen glowing red.",
  [f"{N}: Claire backed away. Her phone was already recording. But as she reached the front door..."],
  sfx=[["A wooden floorboard creaking once in a quiet house", 1.5, 0.5, "end"]])
S("hall", ["daniel:home"], "Daniel stepping out of the bedroom doorway into the dim hallway, looking down the hall suspiciously, a phone lighting up in his hand.",
  [f"{D}: [sharp] Did you hear something?", f"{N}: Claire held her breath. The bedroom door opened. Daniel stepped into the hallway. For one terrible second, she thought he had seen her. Then his phone rang.", f"{D}: [casual] Dad? Yeah. Everything's on schedule."],
  sfx=[["Slow footsteps on a hardwood floor approaching", 3.0, 0.4, 1], ["A smartphone ringing with a classic ringtone, two rings", 2.5, 0.4, 2]])
S("elevator", ["claire:work"], "Claire slumped against the mirrored elevator wall, knees buckling, one hand over her mouth, suitcase beside her.",
  [f"{N}: Claire slipped outside. She made it to the elevator before her knees gave way."],
  sfx=[["Elevator doors sliding shut with a soft chime", 2.5, 0.4, "end"]])
S("elevator", ["claire:work"], "Close-up of Claire alone in the elevator, tears on her face, her jaw setting with resolve. Exactly one person in the frame, no mirror reflections, no second figure.",
  [f"{N}: She wanted to scream. She wanted to call Vanessa and demand an explanation. She wanted to cancel the wedding. But then she remembered something her grandfather used to say.",
   f"{N}: [slowly, gravely] \"When someone shows you they're a thief, don't tell them you know. Find out what they're stealing.\""])
S("taxi", ["claire:work"], "Claire in the back seat, rain on the window, phone to her ear, city lights streaking past.",
  [f"{N}: That night, Claire called the only person she trusted completely. Her mother.", f"{E}: [sleepy, worried] Sweetheart? It's almost midnight. What's wrong?", f"{C}: [voice breaking] Mom... Daniel's cheating on me. With Vanessa."])
S("kitchen", ["evelyn:home"], "Evelyn standing in the kitchen with a phone pressed to her ear, one hand gripping the counter, shocked.",
  [f"{E}: [gently] Oh, Claire. Come home. Right now.", f"{C}: [steadier] There's more. They're after Grandpa's trust.", f"{N}: A long silence followed. Then Evelyn's voice changed."])
S("kitchen", ["evelyn:home"], "Close-up of Evelyn's face hardening with resolve, lit by a single lamp.",
  [f"{E}: [firm, low] Listen carefully. Do not confront him. Do not sign anything. And tomorrow morning, we're calling Marcus Reed.", f"{C}: Grandpa's attorney?",
   f"{E}: [grim] Yes. Because fifteen years ago, your grandfather beat a man named Richard Whitmore in court. The night you brought Daniel home, he swore to me he barely spoke to his father. I wanted to believe him."],
  sfx=[["Low ominous cinematic sting, single dark orchestral hit fading out", 3.0, 0.4, "end"]])

# ---------------- ACT 3: the family secret ----------------
S("office", ["marcus", "claire:work"], "Marcus seated behind the oak desk with his hands folded, Claire sitting across from him with her back straight.",
  [f"{N}: The next morning, Claire sat across from Marcus Reed. Her grandfather's longtime attorney. A man who rarely smiled. And never wasted words."], cut=True)
S("office", ["marcus"], "Marcus leaning forward slightly, studying someone across the desk over his wire-rimmed glasses.",
  [f"{M}: Claire, before we begin, I need to ask you something. Has Daniel asked you to sign a marital property agreement?", f"{C}: Yes. He said it was just routine paperwork.", f"{M}: Have you signed it?", f"{C}: Not yet."])
S("office", ["marcus"], "Marcus sliding a thick stapled contract across the desk, one finger pinning a page marked with a yellow tab.",
  [f"{N}: Marcus exhaled.", f"{M}: [dry] Good. Because the agreement he sent you is not routine.", f"{C}: What is it?", f"{M}: Buried on page eleven is one clause. It hands day-to-day control of your grandfather's properties to a new management company."],
  sfx=[["A stack of paper sliding across a wooden desk", 1.5, 0.4, "start"]])
S("office", ["claire:work"], "Close-up of Claire staring down at a contract on the desk, stunned.",
  [f"{C}: And who owns that company?", f"{M}: [flat] Richard Whitmore.", f"{N}: Claire stared at him.", f"{C}: [slowly] So Daniel was supposed to marry me... and I'd sign away control of Grandpa's properties?", f"{M}: That's what they're trying to arrange. But there's something else."])
S("office", [], "An open manila folder on the oak desk holding old photographs of a brick commercial building and yellowed court papers, out of focus.",
  [f"{N}: Marcus opened a folder. Inside were photographs of a commercial building.", f"{M}: Fifteen years ago, Richard Whitmore tried to buy one of your grandfather's properties. Your grandfather refused. So Richard tried to force the sale with forged paperwork."])
S("office", ["marcus", "claire:work"], "Marcus and Claire facing each other across the desk, the open folder between them.",
  [f"{C}: What happened?", f"{M}: Your grandfather took him to court. Richard lost. And according to your grandfather, he never forgave the humiliation.", f"{C}: [disbelieving] You're saying this is revenge?", f"{M}: I'm saying your marriage may have been a business strategy from the beginning."])
S("office", ["claire:work"], "Extreme close-up of Claire's hand resting on the desk, a large diamond engagement ring catching the light.",
  [f"{N}: Claire looked down at her engagement ring. The diamond sparkled beneath the office lights. For two years, she'd believed it represented love. Now it looked like a price tag."])
S("office", ["claire:work", "marcus"], "Claire looking up at Marcus, composed but pale.",
  [f"{C}: How much of my grandfather's estate are they targeting?", f"{M}: Approximately eight million dollars in assets.", f"{N}: Claire went completely still.", f"{C}: [whispers] Eight million?", f"{M}: Yes.", f"{C}: And Vanessa?", f"{M}: We don't know how deeply she's involved. Yet."])
S("office", ["claire:work"], "Claire leaning back in the leather chair, eyes narrowing, a plan forming.",
  [f"{N}: Claire leaned back. Then she asked the question that would change everything.", f"{C}: [quiet, deliberate] What if I don't cancel the wedding?", f"{M}: [warning] Claire...", f"{C}: What if I let them think their plan is working?", f"{M}: That could be dangerous.", f"{C}: [steely] Then we make sure they never get control of anything. And we find out exactly how far they're willing to go."])
S("office", ["marcus"], "Marcus with the faintest trace of a smile, closing a folder on his desk.",
  [f"{N}: Marcus studied her for several seconds.", f"{M}: [approving] Your grandfather would have liked that answer. But we do this legally. No hacking. No fake evidence. We protect your assets first.", f"{C}: Agreed.", f"{M}: And Claire? If Richard Whitmore is involved, expect him to have a second plan.", f"{N}: Marcus was right. And the second plan was far more dangerous than the first."])

# ---------------- ACT 4: the trap inside the trap ----------------
S("bedroom", ["claire:home"], "A phone lit up on a nightstand, Claire's hand reaching for it from the bed.",
  [f"{N}: Eleven days before the wedding, Claire woke up to a voicemail. From Vanessa. Twenty-three seconds long. No hello. No goodbye. Just muffled voices, like a phone left unlocked inside a purse. A pocket dial. Or so Claire thought."],
  cut=True, sfx=[["A smartphone vibrating on a wooden nightstand, two buzzes", 2.0, 0.45, "start"], ["A voicemail beep tone", 1.0, 0.4, "end"]])
S("bedroom", ["claire:home"], "Claire sitting up in bed with a phone held to her ear, eyes widening.",
  [f"{R}~phone: The five hundred thousand goes into the holding account before the ceremony.", f"{D}~phone: And if Claire refuses to sign?", f"{R}~phone: Then we use the other documents.", f"{V}~phone: What other documents?", f"{R}~phone: That's not your concern."])
S("bedroom", ["claire:home"], "Claire on the edge of the bed staring at her phone, thumb over the screen, face set.",
  [f"{N}: The message ran on for a few seconds more. Claire played all of it three times. Then she forwarded it to Marcus. The next morning, Marcus called with disturbing news."])
S("office", ["marcus"], "Marcus standing at his office window on the phone, a printed document in his other hand.",
  [f"{M}: The Whitmores have created a company called Bennett Legacy Management.", f"{C}: [sharp] Using my name?", f"{M}: Yes. And a document has been submitted to a commercial lender. It appears to carry your signature.", f"{C}: I never signed anything for that company.", f"{M}: I know."])
S("apt", ["claire:home"], "Daytime. Claire pacing by the tall windows with her phone to her ear, tense.",
  [f"{C}: Are they trying to borrow money against my properties?", f"{M}: That's what it looks like.", f"{N}: The situation had changed. This was no longer just about a cheating fiancé. Someone had forged Claire's signature. And tried to use her inheritance as collateral."])
S("office", [], "Close-up of a fountain pen lying across the signature line of a loan document, the handwriting soft and out of focus.",
  [f"{C}: Can we stop it?", f"{M}: We've notified the trustee and the lender. The transaction is on hold. Your assets are protected.", f"{C}: Then why do you still sound worried?", f"{M}: Because the lender's file contains something we didn't expect.", f"{C}: What?", f"{M}: A letter claiming that your mother approved the arrangement."])
S("apt", ["claire:home"], "Daytime. Claire slowly lowering her phone, the color draining from her face.",
  [f"{N}: Claire felt the blood drain from her face.", f"{C}: [shaken] My mother would never...", f"{M}: I know. That's why I want you both here tomorrow."])
S("apt", ["claire:home"], "Evening. Claire alone on the sofa in the dim living room, holding a framed photograph and staring at it with doubt.",
  [f"{N}: For the first time, Claire wondered whether someone close to her had been helping the Whitmores. Someone beyond Daniel. Beyond Vanessa. Someone who knew her family. Her grandfather. And the trust."])
S("office", ["evelyn:office", "claire:work"], "Evelyn entering through the office door, Claire rising from a leather chair to face her, tense.",
  [f"{E}: Claire?", f"{C}: [tight] Mom... did you sign a letter for Richard Whitmore?"],
  sfx=[["A heavy wooden office door opening", 1.5, 0.4, "start"]])
S("office", ["evelyn:office"], "Evelyn holding a sheet of paper up close, reading glasses on, her expression hardening.",
  [f"{N}: Evelyn looked at the document. Her face hardened.", f"{E}: [cold] No. That is not my signature. But I know whose hand it is.", f"{C}: What?", f"{E}: Look at the capital E. That little hook at the top. Fifteen years ago, someone signed your grandfather's name with that same hook. We proved it in court."])
S("office", ["claire:work", "evelyn:office"], "Claire and Evelyn side by side over a document on the desk, sharing a look of grim understanding.",
  [f"{N}: Claire stared at her mother.", f"{C}: [realizing] Richard's forger.", f"{E}: [satisfied] The very same. And this time... he's made the same mistake twice."])

# ---------------- ACT 5: back to the wedding ----------------
B = "ballroom"
S(B, ["claire"], "Claire standing in front of a giant glowing projector screen, facing two hundred hushed guests, immaculate and still.",
  [f"{N}: Nineteen days after discovering the affair, Claire stood in front of two hundred guests. Her wedding dress was immaculate. Her makeup was perfect. And Richard Whitmore's name was glowing on a twelve-foot screen. Right beside a five-hundred-thousand-dollar transfer."], cut=True)
S(B, ["richard"], "Richard rising slowly from his seat at the head table, one hand flat on the tablecloth, glaring.",
  [f"{R}: [low, threatening] Young lady, I strongly suggest you turn that projector off.", f"{C}: [innocent] Why? Is there something inaccurate?", f"{R}: You have no idea what you're talking about.", f"{C}: Then explain the money."])
S(B, ["richard", "claire"], "Richard and Claire facing each other across the head table, guests frozen behind them.",
  [f"{R}: [stiff] It was a legitimate business transaction.", f"{C}: To Bennett Legacy Management?", f"{N}: Richard's expression changed. Just slightly. But Claire saw it.", f"{R}: That is confidential information.", f"{C}: [lightly] Interesting. Because the company was created using my family name. And someone submitted a document with my forged signature."])
S(B, ["daniel", "claire"], "Daniel stepping in front of Claire with his hands out, sweating, bow tie askew.",
  [f"{D}: [desperate] Claire, stop! You're humiliating my family!", f"{C}: [icy] Daniel. You were planning to divorce me after six months. I think your family can survive six minutes of embarrassment."],
  sfx=[["A large formal crowd gasping in shock", 2.0, 0.4, "end"]])
S(B, ["vanessa", "claire"], "Vanessa tearful, hands clasped, pleading; Claire regarding her without pity.",
  [f"{V}: [crying] Claire, please! We made a mistake!", f"{C}: [quiet fury] A mistake? Vanessa, you slept with my fiancé. You helped him lie to me. And you discussed my inheritance like it was a lottery jackpot.", f"{V}: I never wanted any of this!", f"{C}: Then why did you ask Daniel how much he'd give you?"])
S(B, [], "The darkened ballroom seen from the back, a giant projector screen glowing, guests' silhouettes turned toward it.",
  [f"{N}: Another message appeared. \"I want my share before you leave her.\" Vanessa's face went pale."],
  overlay={"type": "message", "from": "Vanessa", "to": "Daniel", "text": "I want my share before you leave her."}, sfx=[CLICK])
S(B, ["daniel", "vanessa"], "Daniel wheeling on Vanessa and pointing at her, furious; Vanessa recoiling.",
  [f"{D}: [blurting, furious] You said you deleted that!", f"{N}: The words escaped before he could stop them. The entire room heard. Claire smiled."])
S(B, ["claire"], "Claire holding up a slim silver tablet in one hand with a faint smile.",
  [f"{C}: [amused] She did delete it, Daniel. You didn't. The tablet you gave me last Christmas is still signed in to your account. Every message you ever sent her landed in my kitchen drawer."])
S(B, ["daniel", "claire"], "Daniel gripping Claire's forearm hard, his face twisted; Claire staring him down.",
  [f"{N}: Daniel grabbed Claire's arm.", f"{D}: [snarling] Enough!", f"{C}: [low, dangerous] Take your hand off me.", f"{N}: He didn't. Then a voice came from behind them."])
S(B, ["marcus"], "Marcus striding through the parted crowd, two large security guards in black suits behind him.",
  [f"{M}: [calm, commanding] Mr. Whitmore. I recommend you release my client. Immediately.", f"{N}: Marcus Reed stepped forward. Two security guards stood behind him. Daniel let go."],
  sfx=[["Firm dress-shoe footsteps crossing a marble floor", 3.0, 0.35, "start"]])
S(B, ["richard", "marcus"], "Richard squaring up to Marcus with his chin raised; Marcus unreadable.",
  [f"{R}: [contemptuous] Who the hell are you?", f"{M}: Marcus Reed. Counsel for Claire Bennett and the Bennett family trust.", f"{R}: Then you should know better than to make accusations in public.", f"{M}: I do. Which is why the evidence was delivered to the authorities this morning."])
S(B, ["richard"], "Close-up of Richard, his practiced smile gone, jaw clenched.",
  [f"{N}: Richard's smile vanished.", f"{M}: And the lender has confirmed that forged documents were used to apply for a loan.", f"{R}: [defiant] You can't prove I authorized anything.", f"{M}: Perhaps not from the documents alone."])
S(B, ["marcus", "claire"], "Marcus nodding to Claire, who raises her phone toward the sound system.",
  [f"{N}: Marcus turned toward the projector.", f"{M}: Claire? Play him the rest of the voicemail."])
S(B, [], "Hundreds of guests in the dim ballroom listening in dead silence, faces lit by the screen, some covering their mouths.",
  [f"{R}~phone: If Claire refuses to sign, we use the other documents.", f"{D}~phone: And if somebody checks the signature?", f"{R}~phone: By then, the money will already be moving."])
S(B, ["daniel", "richard"], "Daniel turning to his father, stricken, whispering; Richard staring straight ahead, cornered.",
  [f"{N}: Nobody moved. Nobody spoke. Then Daniel whispered...", f"{D}: [whispers] Dad... you said nobody would ever know.", f"{N}: And just like that, Richard Whitmore lost control of the room."])

# ---------------- ACT 6: the final betrayal ----------------
S(B, ["richard"], "Richard jabbing a finger toward the screen, red-faced, shouting.",
  [f"{R}: [shouting] That recording is out of context!", f"{C}: [calm] Then you can explain the context to the investigators."])
S(B, ["richard", "claire"], "Richard walking toward tall ballroom doors with his back to camera; Claire in the foreground, turning her head.",
  [f"{N}: Richard turned toward the ballroom doors. But before he reached them, Claire spoke again.", f"{C}: There's one more thing.", f"{D}: [exhausted] What now?", f"{C}: The part I still don't understand."])
S(B, ["claire", "vanessa"], "Claire looking directly at Vanessa across the head table; Vanessa trembling.",
  [f"{N}: Claire looked directly at Vanessa.", f"{C}: [quietly] Why did you call me eleven days ago?", f"{V}: [shaky] It was an accident. A pocket dial.", f"{C}: Was it?"])
S(B, ["vanessa"], "Close-up of Vanessa, eyes filling with tears, mascara starting to run.",
  [f"{N}: Vanessa's eyes filled with tears.", f"{C}: You knew exactly when Richard would be discussing the payment. You knew my number. And you knew I'd listen to a voicemail from you."])
S(B, ["daniel", "vanessa"], "Daniel staring at Vanessa in dawning horror; Vanessa unable to meet his eyes.",
  [f"{D}: [stunned] Vanessa?", f"{V}: [breaking] I didn't know how else to tell her.", f"{N}: The room fell silent again."])
S(B, ["vanessa"], "Vanessa hugging her own arms, speaking through tears, the crowd blurred behind her.",
  [f"{V}: [tearful] I thought Daniel loved me. I thought we'd be together after the divorce. But then I heard Richard talking about the documents. And the loans. And what would happen if Claire found out.", f"{C}: What did he say?", f"{V}: He said they'd make you look unstable. That they'd say you couldn't manage your own money."])
S(B, ["daniel", "vanessa"], "Daniel shouting at Vanessa, who shouts back at him, both leaning in.",
  [f"{D}: [shouting] Vanessa, shut up!", f"{V}: [screaming back] No! You promised me everything! And then your father said I was disposable too!"])
S(B, ["vanessa", "claire"], "Vanessa sobbing openly; Claire watching her, expression unreadable.",
  [f"{N}: Vanessa was crying openly now.", f"{V}: [sobbing] I called Claire because I was scared. I wanted her to hear the truth. But I couldn't bring myself to say it.", f"{C}: So you called me after midnight, when you knew my phone would be on silent. And you let it record.", f"{V}: [small] Yes."])
S(B, ["claire", "vanessa"], "Claire stepping close to Vanessa, face to face, quiet and devastating.",
  [f"{N}: For a moment, Claire said nothing. Then she walked closer.", f"{C}: [softly] You could've told me the truth nineteen days ago.", f"{V}: I know.", f"{C}: You could've apologized.", f"{V}: [whispers] I know."])
S(B, ["claire"], "Close-up of Claire, eyes bright with held-back tears, perfectly composed.",
  [f"{C}: [controlled, hurt] Instead, you stood beside me at the altar. Held my flowers. Fixed my veil. And watched me marry a man you knew was trying to steal from me.", f"{N}: Vanessa couldn't answer.", f"{C}: You weren't protecting me. You were protecting yourself."])
S(B, ["vanessa", "claire"], "Vanessa reaching a hand toward Claire, who does not move.",
  [f"{V}: [pleading] Claire, please. We've been friends for fifteen years.", f"{C}: [cold] No, Vanessa. We were friends for fourteen years and eleven months. The last nineteen days? I was just waiting to see whether you'd finally tell the truth."])
S(B, ["claire"], "Close-up of Claire's hands unclasping a delicate diamond bracelet and setting it on the white tablecloth.",
  [f"{N}: Claire unclasped the diamond bracelet Vanessa had given her that morning. She set it on the table.", f"{C}: You can have this back. And Daniel? You can have him too."])
S(B, ["daniel", "claire"], "Daniel reaching for Claire with both hands, pleading, eyes wet; Claire turning away.",
  [f"{D}: [begging] Claire, baby, please. I love you.", f"{C}: [flat] No. You loved what you thought you could take from me. There's a difference."])

# ---------------- ACT 7: karma arrives ----------------
S(B, ["harris"], "Tall ballroom doors swinging open, Detective Harris walking in with two plainclothes investigators, guests turning to look.",
  [f"{N}: At that moment, two investigators entered the ballroom. Behind them stood Detective Harris."],
  cut=True, sfx=[["Heavy double doors swinging open in a large hall", 2.0, 0.45, "start"]])
S(B, ["harris", "richard"], "Detective Harris facing Richard and holding up a folded document; Richard indignant.",
  [f"{H}: Richard Whitmore?", f"{R}: What is this?", f"{H}: [even] We need to speak with you about suspected financial fraud and forged documents connected to Bennett Legacy Management.", f"{R}: [blustering] This is ridiculous!", f"{H}: You're not under arrest at this moment, sir. But we have a court order for your records and your devices. And we expect your cooperation."])
S(B, ["richard", "daniel"], "Richard gripping Daniel's shoulder and hissing an order; Daniel bewildered.",
  [f"{N}: Richard turned to Daniel.", f"{R}: [hissing] Call our lawyer. Now.", f"{D}: [lost] Dad, what's happening?", f"{R}: [snapping] Just do it!"])
S(B, ["daniel"], "Daniel staring down at a phone lighting up in his hand, face slack.",
  [f"{N}: But Daniel's phone was already ringing. His bank. Then his business partner. Then his father's attorney. Every call brought worse news. The lender had frozen the loan. The trust was untouched. And the Whitmore family business was now under investigation."],
  sfx=[["A smartphone vibrating insistently with an incoming call", 3.0, 0.35, "start"]])
S(B, ["richard", "claire"], "Richard looking at Claire, defeated and hollow; Claire meeting his gaze calmly.",
  [f"{N}: Richard looked at Claire. For the first time in his life, he had nothing clever to say.", f"{R}: [hoarse] You planned this.", f"{C}: [even] I planned to protect what my grandfather built. You did the rest."])
S(B, ["daniel", "claire"], "Daniel, pale and sweating, hands pressed together, begging Claire.",
  [f"{N}: Daniel stepped toward her. His face was pale.", f"{D}: [pleading] Claire, please. We can fix this. We can get counseling. Start over. I'll do anything.", f"{C}: Anything?", f"{D}: Yes. Anything.", f"{C}: [crisp] Then sign the annulment papers when Marcus sends them. And don't contact me again."])
S(B, ["claire", "daniel"], "Claire tilting her head at Daniel with a small, merciless smile.",
  [f"{D}: Claire...", f"{C}: [lightly] Oh, and Daniel? You kept asking whether I signed your father's agreement. Remember?", f"{D}: [wary] Yes...", f"{C}: I didn't.", f"{N}: Daniel stared at her."])
S(B, ["claire"], "Claire speaking calmly, investigators in trench coats visible out of focus behind her.",
  [f"{C}: [matter-of-fact] I told you it was signed and sitting with my attorney until after the honeymoon. It wasn't. It was sitting with the investigators. The trustee knew. And the lender was warned before a single dollar could move.", f"{D}: [hollow] So... you knew?", f"{C}: For nineteen days.", f"{D}: And you still married me?"])
S(B, ["claire", "daniel"], "Claire looking down at Daniel, who has sunk onto a gold banquet chair.",
  [f"{C}: [quietly] I let you believe your plan was working. I wanted to see who else was involved. And I wanted you to hear the truth in front of everyone you lied to."])
S(B, ["daniel"], "Daniel slumped in a chair, a tipped champagne flute spilling across the white tablecloth beside him.",
  [f"{N}: Daniel sank into a chair. His champagne glass tipped over. It spread across the white tablecloth, slowly. Like a secret nobody could hide anymore.", f"{C}: [dry] You wanted a rich wife. Congratulations. You married one. For a few hours."])
S(B, ["claire"], "Claire turning to address the whole ballroom, arms slightly open, gracious as a host.",
  [f"{N}: Then Claire turned to the guests.", f"{C}: [warm, wry] I'm sorry this wasn't the celebration you expected. But the food is paid for. The band is paid for. And I refuse to waste a perfectly good cake on a perfectly terrible husband."],
  sfx=[["A few people in a crowd laughing nervously", 2.5, 0.3, "end"]])
S(B, ["claire", "evelyn"], "Claire raising a champagne flute, Evelyn stepping up beside her with proud eyes, guests beginning to applaud.",
  [f"{C}: [bright] So please. Eat. Dance. And enjoy yourselves. Because tonight, we're celebrating something better than a wedding.", f"{E}: [fond] What's that, sweetheart?", f"{C}: [smiling] My freedom."],
  sfx=[["Warm applause and cheering building in a large ballroom", 5.0, 0.35, "end"]])

# ---------------- EPILOGUE ----------------
K = "brooklyn"
S("city", [], "The Manhattan skyline on a bright clear morning, seen from across the river in Brooklyn. Empty waterfront, no people anywhere in the frame.",
  [f"{N}: Six months later, the Whitmore name no longer opened quite so many doors. The investigation into the forged documents was still going. Richard's company had lost its biggest partners. Daniel's marriage had been annulled. And Vanessa had moved away from Manhattan."], cut=True)
S(K, ["claire:brooklyn"], "Claire standing in the middle of the bright loft space, looking around with quiet pride.",
  [f"{N}: Claire? Claire had never been better. She was standing inside a newly renovated building in Brooklyn. A building her grandfather had left her. The same building Richard Whitmore had tried to take fifteen years earlier. Now it was home to a foundation for women rebuilding their lives after financial abuse."])
S(K, ["claire:brooklyn", "evelyn:brooklyn"], "Evelyn and Claire standing together by a tall window, laughing softly.",
  [f"{E}: [warm] Your grandfather would be proud of you.", f"{C}: I hope so.", f"{E}: You know what he always said?", f"{C}: [teasing] Never trust a man who talks more about your money than your dreams?", f"{E}: [laughs] That too."])
S(K, ["evelyn:brooklyn", "claire:brooklyn"], "Evelyn holding out a yellowed envelope to Claire.",
  [f"{N}: They laughed. Then Evelyn handed Claire an old envelope.", f"{E}: [gently] I found this in his papers. He wrote it years ago. It's addressed to you."])
S(K, ["claire:brooklyn"], "Claire unfolding a handwritten letter by the window, sunlight on the paper.",
  [f"{N}: Claire opened the letter. Inside were just two sentences.", f"{N}: [tender, slowly] \"My darling Claire, wealth isn't what people can take from you. It's knowing who you are when they try.\""],
  overlay={"type": "letter", "text": "My darling Claire, wealth isn't what people can take from you. It's knowing who you are when they try."})
S(K, ["claire:brooklyn", "evelyn:brooklyn"], "Claire holding the folded letter to her chest, crying and smiling at once, Evelyn's hand on her shoulder.",
  [f"{N}: Claire folded the letter carefully. For the first time in months, she cried. Not because she'd lost a husband. Or a best friend. But because she finally understood what her grandfather had been trying to teach her."])
S(B, ["daniel", "vanessa", "richard"], "Wide shot of Daniel, Vanessa and Richard standing far apart in the emptying ballroom, each alone and ruined.",
  [f"{N}: Daniel thought he was marrying eight million dollars. Vanessa thought she was stealing another woman's future. And Richard Whitmore thought he was finally getting his revenge. But all three forgot one very important thing."])
S(B, ["claire"], "Claire in her wedding gown looking straight into the camera with a slow, knowing smile, chandeliers glowing behind her.",
  [f"{N}: Never underestimate the woman who already knows your secrets. Especially when she's smiling."])
S(K, ["claire:brooklyn"], "Claire walking out of the brick building into golden evening light, seen from behind, the city beyond.",
  [f"{N}: [slow, final] Because sometimes... the best revenge isn't destroying your enemies. It's letting them destroy themselves.", f"{N}: This has been Karma Tales. Every betrayal has a price. And karma always collects."])

(HERE / "ep01_full.json").write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")

import re
words = sum(len(re.sub(r"\[[^\]]*\]", "", t).split()) for s in spec["scenes"] for _, t in s["lines"])
chars = sum(len(t) for s in spec["scenes"] for _, t in s["lines"])
roles = {r.split("~")[0] for s in spec["scenes"] for r, _ in s["lines"]}
missing = [c for s in spec["scenes"] for c in s["chars"] if c not in spec["looks"]]
ids = [s["id"] for s in spec["scenes"]]
bad = [x for x, _ in spec["ambience"] + spec["music"] if x not in ids]
print(len(spec["scenes"]), "scenes,", words, "spoken words,", chars, "chars; roles", sorted(roles))
print("missing looks:", missing, "| bad cue ids:", bad, "| roles without voice:", roles - set(spec["voices"]))
print("longest scene chars:", max(sum(len(t) for _, t in s["lines"]) for s in spec["scenes"]), "| sfx:", sum(len(s.get("sfx", [])) for s in spec["scenes"]))
print(ids[21], spec["scenes"][21]["lines"][0][0], "|", ids[-1])
