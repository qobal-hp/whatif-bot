"""Check a trends-v2 job before spending ElevenLabs credits.

usage: python trends/validate.py <job dir>   -> prints JSON {errors, warnings}; exit 1 on errors
"""
import json, sys
from pathlib import Path
from PIL import Image
from fontTools.ttLib import TTFont

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from common import LAYOUTS, THEMES, COUNTRIES, Fonts, load_job  # noqa: E402

REQUIRED = {"title_card": ["lines"], "hero_number": ["number"], "scoreboard": ["rows"], "bars": ["items"],
            "progress": ["max", "value"], "versus": ["left", "right"], "list_card": ["rows"], "trend_card": ["big"]}
WPS = {"en": 2.6, "es": 2.8, "pt": 2.7, "id": 2.6, "hi": 3.3}  # spoken words per second, rough


def strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if not k.startswith("_"):
                yield from strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from strings(v)


def cmap_of(path):
    return set(TTFont(str(path)).getBestCmap().keys())


def validate(job_dir):
    job = Path(job_dir); errors, warnings = [], []
    for f in ("production.json", "thumbnail.png"):
        if not (job / f).exists():
            errors.append(f"missing {f}")
    if errors:
        return {"errors": errors, "warnings": warnings}
    try:
        prod, facts = load_job(job)
    except Exception as e:
        return {"errors": [f"cannot read json: {e}"], "warnings": []}
    if prod.get("schema") != "trends-v2":
        errors.append('production.json "schema" must be "trends-v2"')
    if prod.get("country") not in COUNTRIES:
        errors.append(f"country must be one of {sorted(COUNTRIES)}")
    elif prod.get("language") != COUNTRIES[prod["country"]]:
        errors.append(f"language for {prod['country']} must be {COUNTRIES[prod['country']]}")
    if prod.get("theme") not in THEMES:
        warnings.append(f"theme {prod.get('theme')!r} unknown; using news")
    for k in ("job_id", "header", "title", "description", "first_comment"):
        if not prod.get(k):
            errors.append(f"missing {k}")
    if prod.get("title", "").count("#shorts") != 1:
        warnings.append("title should end with #shorts exactly once")
    sents = prod.get("sentences", [])
    ids = [s.get("id") for s in sents]
    if not (4 <= len(sents) <= 9):
        warnings.append(f"{len(sents)} sentences; 4-8 is the target")
    words = 0
    for s in sents:
        if not s.get("chunks"):
            errors.append(f"sentence {s.get('id')} has no chunks"); continue
        for c in s["chunks"]:
            if not c.get("spoken") or not c.get("caption"):
                errors.append(f"sentence {s.get('id')}: every chunk needs spoken and caption")
                continue
            words += len(c["spoken"].split())
            if len(c["caption"].split()) > 8:
                warnings.append(f"long caption chunk: {c['caption']!r}")
            if any(q in c["spoken"] for q in "“”\"()[]"):
                warnings.append(f"quotes/brackets in spoken text: {c['spoken']!r}")
    est = 0.3 + words / WPS.get(prod.get("language", "en"), 2.6) + 1.1
    if est > 39:
        errors.append(f"script too long: ~{est:.0f}s estimated for {words} words")
    elif est < 24:
        warnings.append(f"script may be short: ~{est:.0f}s estimated for {words} words")
    used = []
    for i, sc in enumerate(prod.get("scenes", [])):
        lay = sc.get("layout")
        if lay not in LAYOUTS:
            errors.append(f"scene {i + 1}: unknown layout {lay!r}"); continue
        for k in REQUIRED[lay]:
            if k not in sc.get("data", {}):
                errors.append(f"scene {i + 1} ({lay}): data.{k} is required")
        used += sc.get("sentences", [])
    if used != ids:
        errors.append(f"scenes must use every sentence once, in order: scenes cover {used}, sentences are {ids}")
    # every character on screen must exist in the font (no tofu boxes)
    F = Fonts(prod.get("language", "en"))
    have = cmap_of(F.black) | cmap_of(F.bold)
    latin = cmap_of(Fonts("en").black) | cmap_of(F.num)
    missing = set()
    for s in strings({k: prod.get(k) for k in ("header", "sentences", "scenes")}):
        for ch in s:
            if ch.isspace():
                continue
            if ord(ch) not in have and ord(ch) not in latin:
                missing.add(ch)
    if missing:
        errors.append("characters the fonts cannot draw: " + " ".join(sorted(missing)))
    try:
        im = Image.open(job / "thumbnail.png")
        if im.size != (1080, 1920):
            if abs(im.size[0] / im.size[1] - 9 / 16) < 0.01:
                warnings.append(f"thumbnail is {im.size}, will be scaled to 1080x1920")
            else:
                errors.append(f"thumbnail is {im.size}; it must be 9:16 (1080x1920)")
    except Exception as e:
        errors.append(f"thumbnail unreadable: {e}")
    conflicts = facts.get("CONFLICT") or facts.get("conflicts") or []
    if conflicts:
        errors.append(f"facts.json has {len(conflicts)} unresolved CONFLICT item(s)")
    if facts.get("verify_needed"):
        warnings.append(f"verify_needed: {facts['verify_needed']}")
    if not (job / "trends_screenshot.png").exists():
        warnings.append("no trends_screenshot.png evidence in the package")
    return {"errors": errors, "warnings": warnings, "estimated_seconds": round(est, 1)}


if __name__ == "__main__":
    r = validate(sys.argv[1]); print(json.dumps(r, indent=2, ensure_ascii=False)); sys.exit(1 if r["errors"] else 0)
