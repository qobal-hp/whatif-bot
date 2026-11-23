"""Build a verse-captioned reading script from the RV1909 JSON.

usage: python biblia/build_script.py <book_en> <book_es> <first> <last> <out.txt> "<intro>" "<outro>"
"""
import json
import re
import sys

U = ("uno dos tres cuatro cinco seis siete ocho nueve diez once doce trece catorce quince dieciséis diecisiete "
     "dieciocho diecinueve veinte veintiuno veintidós veintitrés veinticuatro veinticinco veintiséis veintisiete "
     "veintiocho veintinueve").split()


def words(n):
    if n < 30:
        return U[n - 1]
    tens = {30: "treinta", 40: "cuarenta", 50: "cincuenta", 60: "sesenta", 70: "setenta", 80: "ochenta",
            90: "noventa"}[n // 10 * 10]
    return tens if n % 10 == 0 else f"{tens} y {U[n % 10 - 1]}"


def fix(v):
    v = re.sub(r"\s+", " ", v.strip())
    m = re.match(r"^([A-ZÁÉÍÓÚÑ]{2,})(\b.*)", v)
    return m.group(1).capitalize() + m.group(2) if m else v


en, es, a, b, path, intro, outro = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], sys.argv[6], sys.argv[7]
book = json.load(open(sys.argv[8] if len(sys.argv) > 8 else "/tmp/tx/out/pentateuch.json"))[en]
out = [intro]
for c in range(a, b + 1):
    out.append(f"{es}, capítulo {words(c)}.")
    verses = [(f"{es} {c}:{i}", fix(v)) for i, v in enumerate(book[str(c)], 1) if v.strip()]
    paras, cur, n = [], [], 0
    for ref, v in verses:
        cur.append(f"[[{ref}]] {v}")
        n += len(v)
        if n > 650:
            paras.append(cur)
            cur, n = [], 0
    if cur:
        if paras and n < 200:
            paras[-1] += cur
        else:
            paras.append(cur)
    out += ["\n".join(p) for p in paras]
out.append(outro)
open(path, "w").write("\n\n".join(out) + "\n")
