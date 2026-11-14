"""Write an .srt subtitle file from an episode's props (word timings).

usage: python pipeline/make_srt.py <props.json> <out.srt>
Cues break at sentence ends, at pauses, or when a line would pass 42 characters.
"""
import json
import sys


def stamp(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def cues(words, limit=42):
    out, cur = [], []
    for i, w in enumerate(words):
        text = w["text"].strip()
        if not text:
            continue
        if cur and (len(" ".join(x["text"].strip() for x in cur)) + 1 + len(text) > limit or w["start"] - cur[-1]["end"] > 0.6):
            out.append(cur)
            cur = []
        cur.append(w)
        if text[-1] in ".?!" and len(" ".join(x["text"].strip() for x in cur)) > 12:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def main():
    props = json.load(open(sys.argv[1]))
    lines = []
    for n, cue in enumerate(cues(props["words"]), 1):
        end = max(cue[-1]["end"], cue[0]["start"] + 0.8)
        lines.append(f"{n}\n{stamp(cue[0]['start'])} --> {stamp(end)}\n{' '.join(w['text'].strip() for w in cue)}\n")
    open(sys.argv[2], "w").write("\n".join(lines))
    print(f"{len(lines)} cues")


if __name__ == "__main__":
    main()
