"""Shared helpers for the trends Shorts pipeline: fonts, colours, job loading, narration timing."""
import json, os, unicodedata
from pathlib import Path
from PIL import ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "fonts"
W, H, FPS = 1080, 1920, 30
THUMB_END = 0.30

LAYOUTS = {"title_card", "hero_number", "scoreboard", "bars", "progress", "versus", "list_card", "trend_card"}
THEMES = {"stage", "stadium", "pitch", "news", "tech", "viral"}
COUNTRIES = {"US": "en", "IN": "hi", "ID": "id", "BR": "pt", "MX": "es"}

COLORS = {"red": (239, 68, 68), "green": (46, 204, 113), "blue": (66, 145, 255), "gold": (255, 200, 90),
          "pink": (255, 120, 160), "teal": (80, 220, 210), "orange": (255, 153, 51), "white": (255, 255, 255),
          "purple": (160, 110, 255), "grey": (190, 190, 205)}
THEME_ACCENT = {"stage": "pink", "stadium": "orange", "pitch": "orange", "news": "blue", "tech": "teal", "viral": "gold"}


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def color(name, accent):
    if not name or name == "accent":
        return accent
    if isinstance(name, str) and name.startswith("#"):
        return hex2rgb(name)
    return COLORS.get(name, accent)


class Fonts:
    """Picks fonts by language. Devanagari text uses Mukta; Latin text uses Inter; plain numbers use Anton."""
    def __init__(self, lang):
        self.lang = lang
        if lang == "hi":
            self.black = FONTS / "Mukta-ExtraBold.ttf"; self.xbold = FONTS / "Mukta-ExtraBold.ttf"; self.bold = FONTS / "Mukta-Bold.ttf"
        else:
            self.black = FONTS / "Inter-Black.otf"; self.xbold = FONTS / "Inter-ExtraBold.otf"; self.bold = FONTS / "Inter-Bold.otf"
        self.num = FONTS / "Anton-Regular.ttf"
        self._c = {}

    def get(self, path, size):
        k = (str(path), int(size))
        if k not in self._c:
            self._c[k] = ImageFont.truetype(str(path), int(size), layout_engine=ImageFont.Layout.RAQM)
        return self._c[k]

    def number_font(self, text):
        return self.num if all(c in "0123456789#+-–/.,:%×xKMBkmb " for c in str(text)) else self.black

    def fit(self, text, path, size, maxw, minsize=22):
        s = size
        while s > minsize and self.get(path, s).getlength(text) > maxw:
            s -= 2
        return self.get(path, s)


def load_job(job_dir):
    job_dir = Path(job_dir)
    prod = json.loads((job_dir / "production.json").read_text(encoding="utf-8"))
    facts_p = job_dir / "facts.json"
    facts = json.loads(facts_p.read_text(encoding="utf-8")) if facts_p.exists() else {}
    return prod, facts


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'), ("—", "-"), ("–", "-")):
        s = s.replace(a, b)
    return s


TAGS = {"excited": "[excited] ", "shouting": "[shouting] ", "curious": "[curious] ", "calm": "[calm] "}


def narration_text(prod, with_tags=True):
    parts = []
    for s in prod["sentences"]:
        body = " ".join(c["spoken"].strip() for c in s["chunks"])
        tag = TAGS.get(s.get("delivery", "normal"), "") if with_tags else ""
        parts.append(tag + body)
    return " ".join(parts)


def chunk_timeline(prod, alignment, start=THUMB_END, speed=1.0):
    """Map every chunk to (start, end) seconds in the final video using ElevenLabs character timestamps."""
    chars = alignment["characters"]
    st = [x / speed for x in alignment["character_start_times_seconds"]]
    en = [x / speed for x in alignment["character_end_times_seconds"]]
    nchars, nmap = [], []
    for i, c in enumerate(chars):
        for d in norm(c):
            nchars.append(d); nmap.append(i)
    hay = "".join(nchars)
    pos, out = 0, []
    for s in prod["sentences"]:
        for j, c in enumerate(s["chunks"]):
            needle = norm(c["spoken"].strip())
            k = hay.find(needle, pos)
            if k < 0:
                raise ValueError(f"chunk not found in narration timing: {c['spoken']!r}")
            pos = k + len(needle)
            out.append({"sentence": s["id"], "idx": j, "caption": c["caption"], "start": start + st[nmap[k]],
                        "end": start + en[nmap[k + len(needle) - 1]]})
    for a, b in zip(out, out[1:]):
        if b["start"] - a["end"] < 1.0:
            a["end"] = b["start"]
    return out
