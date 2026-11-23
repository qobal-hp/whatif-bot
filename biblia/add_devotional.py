"""Wrap a reading script with our own devotional text: introduction, short reflections between chapters,
and a closing meditation and prayer. Each sentence becomes a captioned unit labelled on screen.

usage: python biblia/add_devotional.py <script.txt> <devotional.json> <out.txt>
devotional.json: {"intro": "...", "reflections": {"5": "...", ...} (shown before that chapter heading),
                  "meditation": "...", "prayer": "...", "farewell": "..."}
"""
import json
import re
import sys

src, dev, out = open(sys.argv[1]).read(), json.load(open(sys.argv[2])), sys.argv[3]


def block(label, text):
    sentences = [s for s in re.split(r"(?<=[.!?»])\s+(?=[A-ZÁÉÍÓÚÑ¡¿«])", text.strip()) if s]
    return "\n".join(f"[[{label}]] {s}" for s in sentences)


paras = [p for p in src.split("\n\n") if p.strip()]
heads = [i for i, p in enumerate(paras) if re.match(r"[A-ZÁÉÍÓÚ][\wáéíóúñ ]+, capítulo .+\.$", p.strip())]
body = paras[heads[0]:-1]  # drop the old one-line welcome and farewell
result = [block("Introducción", dev["intro"])]
for p in body:
    m = re.match(r"[A-ZÁÉÍÓÚ][\wáéíóúñ ]+, capítulo (.+)\.$", p.strip())
    if m:
        import importlib.util
        spec = importlib.util.spec_from_file_location("r", __file__.replace("add_devotional.py", "render.py"))
        n = None
        words = m.group(1)
        nums = ("uno dos tres cuatro cinco seis siete ocho nueve diez once doce trece catorce quince dieciséis "
                "diecisiete dieciocho diecinueve veinte veintiuno veintidós veintitrés veinticuatro veinticinco "
                "veintiséis veintisiete veintiocho veintinueve").split()
        tens = {"treinta": 30, "cuarenta": 40, "cincuenta": 50}
        if words in nums:
            n = nums.index(words) + 1
        else:
            a = words.split(" y ")
            n = tens[a[0]] + (nums.index(a[1]) + 1 if len(a) > 1 else 0)
        if str(n) in dev.get("reflections", {}):
            result.append(block("Reflexión", dev["reflections"][str(n)]))
    result.append(p)
result += [block("Meditación", dev["meditation"]), block("Oración", dev["prayer"]), dev["farewell"]]
open(out, "w").write("\n\n".join(result) + "\n")
