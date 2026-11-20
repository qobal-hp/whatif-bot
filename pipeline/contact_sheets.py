"""Contact sheets of an episode's scene pictures: python pipeline/contact_sheets.py <assets dir> <out dir>"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw

src, out = Path(sys.argv[1]), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
files = sorted(p for p in src.glob("*.jpg") if not p.name.startswith(("portrait_", "thumb")))
tiles = []
for f in files:
    im = Image.open(f).convert("RGB")
    im.thumbnail((320, 320))
    tile = Image.new("RGB", (320, 180))
    tile.paste(im.resize((320, 180)) if im.width > im.height else im, (0, 0))
    ImageDraw.Draw(tile).text((5, 5), f.stem, fill="yellow")
    tiles.append(tile)
for k in range(0, len(tiles), 36):
    sheet = Image.new("RGB", (320 * 6, 180 * 6))
    for i, t in enumerate(tiles[k:k + 36]):
        sheet.paste(t, ((i % 6) * 320, (i // 6) * 180))
    sheet.save(out / f"sheet{k // 36:02d}.jpg", quality=80)
portraits = sorted(src.glob("portrait_*.jpg"))
if portraits:
    sheet = Image.new("RGB", (200 * len(portraits), 300))
    for i, f in enumerate(portraits):
        im = Image.open(f).convert("RGB")
        im.thumbnail((200, 300))
        ImageDraw.Draw(im).text((5, 5), f.stem[9:], fill="yellow")
        sheet.paste(im, (i * 200, 0))
    sheet.save(out / "portraits.jpg", quality=85)
print(f"{len(tiles)} scenes")
