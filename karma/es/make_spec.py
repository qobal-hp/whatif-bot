"""Write karma/es/<ep>_es.json, the upload spec of a Spanish episode, from the English spec and karma/es/<ep>_lines.py.

usage: python karma/es/make_spec.py ep02
"""
import importlib.util, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ep = sys.argv[1]
spec = importlib.util.spec_from_file_location("lines", ROOT / "karma" / "es" / f"{ep}_lines.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
s = json.loads((ROOT / "karma" / f"{ep}_full.json").read_text())
s["youtube"] = dict(mod.YOUTUBE, shorts_description="Mira la historia completa en Karma Tales en Español.\n#shorts #karmatales #telenovela")
s["thumbnail_file"] = f"karma/es/{ep}_thumb.jpg"
s["shorts"] = []
s.pop("shorts_end_card", None)
(ROOT / "karma" / "es" / f"{ep}_es.json").write_text(json.dumps(s, indent=1, ensure_ascii=False) + "\n")
print(ep, s["youtube"]["title"])
