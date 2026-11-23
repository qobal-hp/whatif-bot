"""Turn a ChatGPT devotional script ([INTRO]/[VERSO]/[EXPLICACIÓN]/[MEDITACIÓN]/[ORACIÓN]/[DESPEDIDA])
into a render script. Verse text is always taken from Reina-Valera 1909 (public domain), never from the draft.

usage: python biblia/build_devotional.py <guion.txt> <out.txt> [pause_seconds]
"""
import json
import re
import sys
from pathlib import Path

BOOKS = {"génesis": "Genesis", "éxodo": "Exodus", "levítico": "Leviticus", "números": "Numbers",
         "deuteronomio": "Deuteronomy", "josué": "Joshua", "jueces": "Judges", "rut": "Ruth",
         "1 samuel": "I Samuel", "2 samuel": "II Samuel", "1 reyes": "I Kings", "2 reyes": "II Kings",
         "1 crónicas": "I Chronicles", "2 crónicas": "II Chronicles", "esdras": "Ezra", "nehemías": "Nehemiah",
         "ester": "Esther", "job": "Job", "salmo": "Psalms", "salmos": "Psalms", "proverbios": "Proverbs",
         "eclesiastés": "Ecclesiastes", "cantares": "Song of Solomon", "isaías": "Isaiah", "jeremías": "Jeremiah",
         "lamentaciones": "Lamentations", "ezequiel": "Ezekiel", "daniel": "Daniel", "oseas": "Hosea",
         "joel": "Joel", "amós": "Amos", "abdías": "Obadiah", "jonás": "Jonah", "miqueas": "Micah",
         "nahúm": "Nahum", "habacuc": "Habakkuk", "sofonías": "Zephaniah", "hageo": "Haggai",
         "zacarías": "Zechariah", "malaquías": "Malachi", "mateo": "Matthew", "marcos": "Mark", "lucas": "Luke",
         "juan": "John", "hechos": "Acts", "romanos": "Romans", "1 corintios": "I Corinthians",
         "2 corintios": "II Corinthians", "gálatas": "Galatians", "efesios": "Ephesians", "filipenses": "Philippians",
         "colosenses": "Colossians", "1 tesalonicenses": "I Thessalonians", "2 tesalonicenses": "II Thessalonians",
         "1 timoteo": "I Timothy", "2 timoteo": "II Timothy", "tito": "Titus", "filemón": "Philemon",
         "hebreos": "Hebrews", "santiago": "James", "1 pedro": "I Peter", "2 pedro": "II Peter",
         "1 juan": "I John", "2 juan": "II John", "3 juan": "III John", "judas": "Jude", "apocalipsis": "Revelation of John"}
LABELS = {"INTRO": "Introducción", "EXPLICACIÓN": "Explicación", "MEDITACIÓN": "Meditación",
          "ORACIÓN": "Oración", "DESPEDIDA": "Despedida"}
BIBLE = json.load(open(Path(__file__).with_name("rv1909.json")))


def fix(v):
    v = re.sub(r"\s+", " ", v.strip())
    m = re.match(r"^([A-ZÁÉÍÓÚÑ]{2,})(\b.*)", v)
    return m.group(1).capitalize() + m.group(2) if m else v


def verses(ref):
    m = re.match(r"(.+?)\s+(\d+):(\d+)(?:\s*[-–]\s*(\d+))?$", ref.strip())
    book, ch, a, b = m.group(1), m.group(2), int(m.group(3)), int(m.group(4) or m.group(3))
    en = BOOKS[book.lower()]
    shown = "Salmos" if book.lower() == "salmo" else book
    return shown, ch, a, b, [(f"{shown} {ch}:{v}", fix(BIBLE[en][ch][v - 1])) for v in range(a, b + 1)]


def sentences(label, text):
    parts = [s for s in re.split(r"(?<=[.!?»])\s+(?=[A-ZÁÉÍÓÚÑ¡¿«])", re.sub(r"\s+", " ", text.strip())) if s]
    return "\n".join(f"[[{label}]] {s}" for s in parts)


def main():
    src, out = Path(sys.argv[1]).read_text(), Path(sys.argv[2])
    pause = int(sys.argv[3]) if len(sys.argv) > 3 else 20
    blocks = re.split(r"^\[([A-ZÁÉÍÓÚ]+)\][ \t]*(.*)$", src, flags=re.M)
    paras, n = [], 0
    for i in range(1, len(blocks), 3):
        tag, arg, body = blocks[i], blocks[i + 1].strip(), blocks[i + 2].strip()
        if tag == "VERSO":
            shown, ch, a, b, vs = verses(arg)
            n += 1
            paras.append(f"[[#{shown} {ch}:{a}{'-' + str(b) if b != a else ''}]]")  # new image, chapter label
            span = f"versículo {a}" if a == b else f"versículos {a} al {b}"
            paras.append(f"[[{shown} {ch}]] {shown}, capítulo {ch}, {span}.")
            paras.append("\n".join(f"[[{r}]] {t}" for r, t in vs))
        elif tag in LABELS:
            for p in [p for p in re.split(r"\n\s*\n", body) if p.strip()]:
                paras.append(sentences(LABELS[tag], p))
            if tag == "MEDITACIÓN":
                paras.append(f"[[#pausa {pause}]]")
    out.write_text("\n\n".join(paras) + "\n")
    print(f"{n} passages -> {out}")


if __name__ == "__main__":
    main()
