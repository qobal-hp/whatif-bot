"""Render a trends Short from a trends-v2 job folder plus ElevenLabs narration (mp3 + character timestamps).

usage: python trends/render.py <job dir> <vo.mp3> <vo.json> <out dir>
Writes <out dir>/video.mp4 and <out dir>/qc.json.
"""
import json, math, os, random, subprocess, sys, hashlib
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from common import W, H, FPS, THUMB_END, Fonts, color, THEME_ACCENT, COLORS, load_job, chunk_timeline  # noqa: E402
import bgm  # noqa: E402

WHITE = (255, 255, 255); GREY = (190, 190, 205); PANEL = (14, 14, 26, 228)
ENC = ["-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-r", "30"]
MAX_LEN, MIN_LEN = 35.0, 25.0


def ease(x):
    x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3


def pop(x):
    x = max(0.0, min(1.0, x)); c = 1.7
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


def layer():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def tc(d, xy, s, f, fill, stroke=0, sf=(0, 0, 0)):
    d.text(xy, s, font=f, fill=fill, anchor="mm", stroke_width=stroke, stroke_fill=sf)


def rr(d, box, r, fill, outline=None, width=0):
    d.rounded_rectangle(box, r, fill=fill, outline=outline, width=width)


def paste_scaled(base, lay, cx, cy, sc, alpha=1.0):
    if sc <= 0.01 or alpha <= 0.01:
        return
    if abs(sc - 1) > 0.002:
        w, h = int(W * sc), int(H * sc); l2 = lay.resize((w, h), Image.BILINEAR); ox, oy = int(cx - cx * sc), int(cy - cy * sc)
    else:
        l2, ox, oy = lay, 0, 0
    if alpha < 1:
        l2 = l2.copy(); l2.putalpha(l2.getchannel("A").point(lambda v: int(v * alpha)))
    if ox < 0 or oy < 0:
        base.paste(l2, (ox, oy), l2)
    else:
        base.alpha_composite(l2, (ox, oy))


class Short:
    def __init__(self, job_dir, vo_json, speed=1.0):
        self.job_dir = Path(job_dir)
        self.prod, self.facts = load_job(job_dir)
        p = self.prod
        self.F = Fonts(p.get("language", "en"))
        self.theme = p.get("theme", "news")
        self.accent = color(p.get("accent") or THEME_ACCENT.get(self.theme, "blue"), COLORS["blue"])
        al = json.loads(Path(vo_json).read_text(encoding="utf-8"))["alignment"]
        self.chunks = chunk_timeline(p, al, THUMB_END, speed)
        self.vo_end = self.chunks[-1]["end"] if self.chunks else 5
        self.total = round(self.vo_end + 1.1, 2)
        sent_first = {}
        for c in self.chunks:
            sent_first.setdefault(c["sentence"], c["start"])
        self.scenes = p["scenes"]
        starts = [THUMB_END] + [sent_first[sc["sentences"][0]] - 0.1 for sc in self.scenes[1:]]
        self.sc_bounds = starts + [self.total]
        for i, sc in enumerate(self.scenes):
            sc["_chunks"] = [c for c in self.chunks if c["sentence"] in sc["sentences"]]
            sc["_t0"], sc["_t1"] = self.sc_bounds[i], self.sc_bounds[i + 1]
        seed = int(hashlib.md5(p.get("job_id", "x").encode()).hexdigest()[:8], 16)
        self.rng = random.Random(seed)
        self._build_background()
        self._static = [self._static_layer(sc) for sc in self.scenes]

    # ---------- helpers ----------
    def chunk_start(self, sc, k):
        ch = sc["_chunks"]
        if not ch:
            return sc["_t0"]
        return ch[min(max(int(k), 0), len(ch) - 1)]["start"]

    def col(self, name):
        return color(name, self.accent)

    # ---------- background themes ----------
    def _build_background(self):
        r = self.rng
        grads = {"stage": ((14, 8, 26), (34, 14, 44)), "stadium": ((8, 10, 20), (12, 34, 22)), "pitch": ((8, 11, 22), (18, 35, 32)),
                 "news": ((8, 12, 24), (16, 24, 44)), "tech": ((6, 12, 18), (10, 30, 40)), "viral": ((20, 10, 30), (40, 18, 40))}
        a, b = grads.get(self.theme, grads["news"])
        bg = Image.new("RGBA", (W, H), (0, 0, 0, 255)); d = ImageDraw.Draw(bg)
        for y in range(H):
            k = y / H; d.line((0, y, W, y), fill=tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3)) + (255,))
        glow = layer(); gd = ImageDraw.Draw(glow)
        for cx in (140, 940):
            gd.ellipse((cx - 260, -220, cx + 260, 240), fill=self.accent + (45,))
        bg.alpha_composite(glow.filter(ImageFilter.GaussianBlur(90)))
        if self.theme == "pitch":
            pl = layer(); pd = ImageDraw.Draw(pl)
            pd.polygon([(430, 1380), (650, 1380), (820, 1920), (260, 1920)], fill=(196, 164, 110, 28))
            for y in (1440, 1800):
                x0 = 540 - (110 + 300 * (y - 1380) / 540); pd.line((x0 - 30, y, W - x0 + 30, y), fill=(255, 255, 255, 45), width=4)
            bg.alpha_composite(pl)
        if self.theme in ("news", "tech"):
            gl = layer(); g = ImageDraw.Draw(gl)
            for x in range(0, W, 90):
                g.line((x, 300, x, H), fill=(255, 255, 255, 10), width=1)
            for y in range(300, H, 90):
                g.line((0, y, W, y), fill=(255, 255, 255, 10), width=1)
            bg.alpha_composite(gl)
        self.bg = bg
        if self.theme == "stadium":
            strip = Image.new("RGBA", (W, H + 240), (0, 0, 0, 0)); sd = ImageDraw.Draw(strip)
            for y in range(0, H + 240, 120):
                sd.rectangle((0, y, W, y + 60), fill=(20, 60, 30, 60)); sd.line((0, y, W, y), fill=(255, 255, 255, 34), width=4)
            mask = Image.linear_gradient("L").resize((W, H)).point(lambda v: max(0, min(255, int((v - 110) * 2.2))))
            self.field, self.field_mask = strip, mask
        palette = [self.accent, WHITE, COLORS["gold"]]
        self.parts = [(r.uniform(0, W), r.uniform(0, H), r.uniform(1.5, 3.5), r.uniform(20, 60), r.uniform(0, 6.28), r.choice(palette)) for _ in range(40)]
        hdr = layer(); hd = ImageDraw.Draw(hdr)
        f = self.F.fit(self.prod.get("header", ""), self.F.xbold, 40, 760)
        rr(hd, (130, 170, 950, 262), 46, (0, 0, 0, 190), outline=(255, 255, 255, 60), width=2)
        tc(hd, (540, 216), self.prod.get("header", ""), f, WHITE)
        self.header = hdr

    def base(self, t):
        z = 1.0 + 0.035 * (t / 32); w, h = int(W * z), int(H * z)
        img = self.bg.resize((w, h), Image.BILINEAR).crop(((w - W) // 2, (h - H) // 2, (w - W) // 2 + W, (h - H) // 2 + H))
        d = ImageDraw.Draw(img)
        if self.theme == "stage":
            L = Image.new("RGBA", (W // 2, H // 2), (0, 0, 0, 0)); ld = ImageDraw.Draw(L)
            for ox, colr, ph in ((60, self.accent, 0), (480, COLORS["teal"], 2.1), (270, COLORS["gold"], 4.2)):
                ang = math.sin(t * 0.6 + ph) * 0.35; tip = (ox + math.sin(ang) * 900, math.cos(ang) * 900); nx, ny = math.cos(ang) * 70, -math.sin(ang) * 70
                ld.polygon([(ox, -10), (tip[0] - nx, tip[1] - ny), (tip[0] + nx, tip[1] + ny)], fill=colr + (34,))
            img.alpha_composite(L.filter(ImageFilter.GaussianBlur(14)).resize((W, H), Image.BILINEAR))
            n = 24; bw = W / n
            for i in range(n):
                hh = 40 + 110 * abs(math.sin(t * (2.1 + 0.37 * (i % 5)) + i * 0.9)) * (0.6 + 0.4 * math.sin(i * 0.5 + t))
                x = i * bw + 6; c = (self.accent, COLORS["teal"], COLORS["gold"])[i % 3]
                d.rounded_rectangle((x, H - 40 - hh, x + bw - 12, H - 40), 8, fill=c + (55,))
        elif self.theme == "stadium":
            off = int((t * 90) % 120); strip = self.field.crop((0, 120 - off, W, 120 - off + H))
            from PIL import ImageChops
            strip.putalpha(ImageChops.multiply(strip.getchannel("A"), self.field_mask)); img.alpha_composite(strip)
        elif self.theme in ("news", "tech"):
            y = 300 + (t * 160) % (H - 300); d.line((0, y, W, y), fill=self.accent + (40,), width=3)
        elif self.theme == "viral":
            for i in range(9):
                cx = (i * 137 + t * 30 * (1 + i % 3)) % (W + 200) - 100; cy = 1450 + 260 * math.sin(t * 0.7 + i)
                rad = 40 + 18 * (i % 4); d.ellipse((cx - rad, cy - rad, cx + rad, cy + rad), outline=self.accent + (60,), width=5)
        for x, y, rad, v, ph, c in self.parts:
            yy = (y - v * t) % H; xx = x + 16 * math.sin(t * 0.7 + ph); a = int(80 + 60 * math.sin(t * 2 + ph))
            d.ellipse((xx - rad, yy - rad, xx + rad, yy + rad), fill=c + (a,))
        img.alpha_composite(self.header)
        return img

    # ---------- static layers per layout ----------
    def card(self, d, outline=None, box=(100, 330, 980, 1010)):
        rr(d, box, 40, PANEL, outline=(outline or self.accent) + (210,), width=4)

    def source(self, d, sc, y=1105):
        if sc.get("source"):
            tc(d, (540, y), sc["source"], self.F.fit(sc["source"], self.F.bold, 30, 860), (180, 182, 198))

    def _static_layer(self, sc):
        L = layer(); d = ImageDraw.Draw(L); D = sc.get("data", {}); F = self.F; lay = sc["layout"]
        if lay == "title_card":
            self.card(d)
            if D.get("kicker"):
                f = F.fit(D["kicker"], F.black, 36, 600); w = f.getlength(D["kicker"]) + 70
                rr(d, (540 - w / 2, 385, 540 + w / 2, 455), 35, self.accent + (255,)); tc(d, (540, 420), D["kicker"], f, (12, 12, 20))
            lines = D.get("lines", [])
            for i, ln in enumerate(lines):
                tc(d, (540, 620 - (len(lines) - 1) * 55 + i * 110), ln, F.fit(ln, F.black, 92, 780), WHITE)
            if D.get("sub"):
                tc(d, (540, 880), D["sub"], F.fit(D["sub"], F.bold, 42, 780), GREY)
        elif lay == "hero_number":
            self.card(d, self.col(D.get("color")))
            if D.get("kicker"):
                tc(d, (540, 400), D["kicker"], F.fit(D["kicker"], F.black, 66, 780), WHITE)
            if D.get("label"):
                tc(d, (540, 810), D["label"], F.fit(D["label"], F.bold, 40, 780), GREY)
            if D.get("sub"):
                tc(d, (540, 900), D["sub"], F.fit(D["sub"], F.xbold, 42, 780), COLORS["gold"])
        elif lay == "scoreboard":
            rows = D.get("rows", [])[:3]
            self.card(d, (255, 255, 255))
            if D.get("kicker"):
                tc(d, (540, 395), D["kicker"], F.fit(D["kicker"], F.xbold, 44, 780), GREY)
            gap = 180 if len(rows) <= 2 else 150
            for i, r in enumerate(rows):
                y = 530 + i * gap; c = self.col(r.get("color"))
                rr(d, (130, y - 72, 950, y + 72), 26, c + (40,), outline=c + (200,), width=3)
                d.text((165, y - 18), r.get("name", ""), font=F.fit(r.get("name", ""), F.black, 52, 520), fill=WHITE, anchor="lm")
                if r.get("sub"):
                    d.text((165, y + 38), r["sub"], font=F.get(F.bold, 32), fill=GREY, anchor="lm")
                sc_txt = str(r.get("score", ""))
                d.text((920, y + 4), sc_txt, font=F.fit(sc_txt, F.number_font(sc_txt), 118, 300), fill=c, anchor="rm")
        elif lay == "bars":
            self.card(d)
            tc(d, (540, 405), D.get("title", ""), F.fit(D.get("title", ""), F.black, 62, 800), WHITE)
            if D.get("sub"):
                tc(d, (540, 470), D["sub"], F.fit(D["sub"], F.bold, 36, 780), GREY)
        elif lay == "progress":
            self.card(d)
            tc(d, (540, 405), D.get("title", ""), F.fit(D.get("title", ""), F.black, 58, 800), WHITE)
        elif lay == "versus":
            if D.get("title"):
                tc(d, (540, 365), D["title"], F.fit(D["title"], F.black, 56, 800), WHITE)
        elif lay == "list_card":
            self.card(d)
            tc(d, (540, 410), D.get("title", ""), F.fit(D.get("title", ""), F.black, 50, 800), self.accent)
            rows = D.get("rows", [])[:4]
            for i, r in enumerate(rows):
                y0 = 480 + i * 140; hl = r.get("highlight")
                rr(d, (150, y0, 930, y0 + 120), 24, (self.accent + (60,)) if hl else (40, 36, 58, 255), outline=(self.accent + (255,)) if hl else None, width=3)
                d.text((180, y0 + 36), r.get("tag", ""), font=F.get(F.black if hl else F.bold, 28), fill=self.accent if hl else GREY, anchor="lm")
                d.text((180, y0 + 84), r.get("text", ""), font=F.fit(r.get("text", ""), F.xbold, 42, 720), fill=WHITE, anchor="lm")
        elif lay == "trend_card":
            rr(d, (90, 330, 990, 1030), 40, (250, 249, 252, 242))
            dark = (30, 32, 48)
            y = 405
            tc(d, (540, y), D.get("platform", ""), F.fit(D.get("platform", ""), F.xbold, 42, 800), dark)
            if D.get("title"):
                tc(d, (540, y + 58), D["title"], F.fit(D["title"], F.black, 52, 800), self.accent)
            big = str(D.get("big", ""))
            tc(d, (540, 640), big, F.fit(big, F.number_font(big), 220, 760), self.accent)
            if D.get("query"):
                qf = F.fit(D["query"], F.black, 46, 760); w = qf.getlength(D["query"]) + 70
                rr(d, (540 - w / 2, 775, 540 + w / 2, 845), 35, (232, 236, 246, 255)); tc(d, (540, 810), D["query"], qf, dark)
            if D.get("sub"):
                tc(d, (540, 885), D["sub"], F.fit(D["sub"], F.bold, 36, 800), (70, 72, 90))
            if D.get("chip"):
                cf = F.fit(D["chip"], F.black, 38, 640); w = cf.getlength(D["chip"]) + 70
                rr(d, (540 - w / 2, 915, 540 + w / 2, 975), 30, self.accent + (255,)); tc(d, (540, 945), D["chip"], cf, WHITE)
            if D.get("observed"):
                tc(d, (540, 1002), D["observed"], F.fit(D["observed"], F.bold, 26, 800), (100, 102, 118))
        if lay != "trend_card":
            self.source(d, sc)
        return L

    # ---------- dynamic parts ----------
    def stamp_img(self, text, colr, size=78, rot=-5):
        f = self.F.fit(text, self.F.black, size, 760); tw = int(f.getlength(text)) + 80
        im = Image.new("RGBA", (tw, int(size * 1.6)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        rr(d, (5, 5, tw - 5, im.height - 5), 20, None, outline=colr, width=10); tc(d, (tw // 2, im.height // 2), text, f, colr)
        return im.rotate(rot, expand=True, resample=Image.BICUBIC)

    def dynamic(self, img, sc, t, u):
        D = sc.get("data", {}); F = self.F; d = ImageDraw.Draw(img); lay = sc["layout"]
        if lay == "hero_number":
            num = str(D.get("number", "")); c = self.col(D.get("color"))
            shown = num
            if D.get("count_up") and num.isdigit():
                shown = str(int(round(int(num) * ease((u - 0.1) / 1.0))))
            tc(d, (540, 635), shown, F.fit(num, F.number_font(num), 280, 760), c)
        elif lay == "scoreboard" and D.get("banner"):
            tb = self.chunk_start(sc, D.get("banner_at_chunk", 1))
            if t >= tb:
                k = ease((t - tb) / 0.25); bf = F.fit(D["banner"], F.black, 46, 640); w = bf.getlength(D["banner"]) + 90
                y = 900 if len(D.get("rows", [])) <= 2 else 965
                L = layer(); ld = ImageDraw.Draw(L)
                rr(ld, (540 - w / 2, y - 48, 540 + w / 2, y + 48), 48, self.col(D.get("banner_color", "green")) + (255,)); tc(ld, (540, y), D["banner"], bf, (8, 20, 12))
                paste_scaled(img, L, 540, y, 0.9 + 0.1 * pop((t - tb) / 0.4), alpha=k)
        elif lay == "bars":
            items = D.get("items", [])[:4]; mx = D.get("max") or max([it["value"] for it in items] + [1]) * 1.15
            ts = self.chunk_start(sc, D.get("start_chunk", 0))
            for i, it in enumerate(items):
                y = 590 + i * 120; k = ease((t - ts - i * 0.25) / 0.8)
                d.text((150, y - 32), it["label"], font=F.fit(it["label"], F.black, 42, 600), fill=WHITE, anchor="lm")
                rr(d, (150, y + 2, 930, y + 44), 21, (40, 46, 62, 255)); wb = 780 * (it["value"] / mx) * k
                if wb > 42:
                    rr(d, (150, y + 2, 150 + wb, y + 44), 21, (self.accent if i == 0 else self.col(it.get("color", "grey"))) + (255,))
                val = it["value"] * k; txt = str(int(round(val))) if float(it["value"]).is_integer() else f"{val:.1f}"
                d.text((930, y - 32), txt, font=F.get(F.num, 54), fill=self.accent if i == 0 else GREY, anchor="rm")
        elif lay == "progress":
            mx = float(D.get("max", 100)); ts = self.chunk_start(sc, D.get("start_chunk", 0)); k = ease((t - ts) / 1.4) if t >= ts else 0
            v = D.get("from", 0) + (D.get("value", 0) - D.get("from", 0)) * k
            x0, x1, y = 140, 940, 610
            rr(d, (x0, y - 40, x1, y + 40), 40, (40, 46, 62, 255)); wb = (x1 - x0) * v / mx
            if wb > 80:
                rr(d, (x0, y - 40, x0 + wb, y + 40), 40, self.col(D.get("color")) + (255,))
            if D.get("target") is not None:
                tx = x0 + (x1 - x0) * float(D["target"]) / mx
                d.line((tx, y - 62, tx, y + 62), fill=COLORS["gold"], width=6)
                d.text((tx, y - 92), str(D.get("target_label", D["target"])), font=F.get(F.num, 46), fill=COLORS["gold"], anchor="mm")
            pt = int(D.get("pips_total", 0)); p = int(round(D.get("pips_from", 0) + (D.get("pips", 0) - D.get("pips_from", 0)) * k))
            txt = D.get("value_fmt", "{v}").format(v=int(round(v)), p=p)
            tc(d, (540, y + 150), txt, F.fit(txt, F.number_font(txt), 150, 760), WHITE)
            for i in range(pt):
                cx = 540 - (pt - 1) * 35 + i * 70; yy = y + 290
                d.ellipse((cx - 22, yy - 22, cx + 22, yy + 22), fill=(COLORS["red"] + (255,)) if i < p else (55, 60, 78, 255))
        elif lay == "versus":
            for side, x0, at in (("left", 100, 0), ("right", 580, D.get("right_at_chunk", 0))):
                S = D.get(side) or {}
                ts = self.chunk_start(sc, at) - (0.2 if side == "right" else 0)
                if t < ts:
                    continue
                k = ease((t - ts) / 0.5); c = self.col(S.get("color")); L = layer(); ld = ImageDraw.Draw(L)
                rr(ld, (x0, 420, x0 + 400, 780), 30, PANEL, outline=c + (220,), width=4)
                top = str(S.get("top", "")); tc(ld, (x0 + 200, 515), top, F.fit(top, F.number_font(top), 104, 340), c)
                for j, ln in enumerate(S.get("lines", [])[:3]):
                    tc(ld, (x0 + 200, 630 + j * 56), ln, F.fit(ln, F.black, 44, 360), WHITE)
                dx = int((200 if side == "right" else -200) * (1 - k)); img.alpha_composite(L, (dx, 0)) if dx >= 0 else img.paste(L, (dx, 0), L)
            if t >= self.chunk_start(sc, D.get("right_at_chunk", 0)):
                tc(d, (540, 600), "×", F.get(F.xbold if self.F.lang != "hi" else FontsLatin().xbold, 110), WHITE)
            if D.get("chip") and t >= self.chunk_start(sc, D.get("chip_at_chunk", 0)) + 0.3:
                cf = F.fit(D["chip"], F.black, 40, 620); w = cf.getlength(D["chip"]) + 80
                rr(d, (540 - w / 2, 850, 540 + w / 2, 935), 42, COLORS["teal"] + (255,)); tc(d, (540, 892), D["chip"], cf, (10, 20, 25))
        st = D.get("stamp") or sc.get("stamp")
        if st:
            ts = self.chunk_start(sc, st.get("at_chunk", 0)) + 0.2
            if t >= ts:
                key = (id(sc), "stamp")
                if key not in self.__dict__.setdefault("_stamps", {}):
                    self._stamps[key] = self.stamp_img(st["text"], self.col(st.get("color", "red")))
                s = self._stamps[key]; k = ease((t - ts) / 0.25); sc_ = 1.6 - 0.6 * k
                im = s.resize((max(1, int(s.width * sc_)), max(1, int(s.height * sc_))), Image.BICUBIC)
                y = 300 if st.get("pos") == "top" else 950
                img.alpha_composite(im, (int(540 - im.width / 2), int(y - im.height / 2)))

    # ---------- captions ----------
    def caption(self, img, t):
        cur = next((c for c in self.chunks if c["start"] <= t < c["end"]), None)
        if not cur:
            return
        size = 70 if self.F.lang == "hi" else 62
        while True:
            f = self.F.get(self.F.black, size); lines = wrap(cur["caption"], f, 840)
            if len(lines) <= 2 or size <= 46:
                break
            size -= 4
        k = ease((t - cur["start"]) / 0.12); d = ImageDraw.Draw(img); lh = int(size * 1.3)
        y0 = 1300 - (len(lines) - 1) * lh // 2 + int((1 - k) * 14)
        for j, ln in enumerate(lines):
            tc(d, (540, y0 + j * lh), ln, f, WHITE, stroke=9)

    def frame(self, t):
        img = self.base(t)
        i = next((j for j in range(len(self.scenes)) if t < self.sc_bounds[j + 1]), len(self.scenes) - 1)
        sc = self.scenes[i]; u = t - self.sc_bounds[i]
        cy = 680 if sc["layout"] == "trend_card" else 670
        if sc["layout"] == "versus":
            img.alpha_composite(self._static[i])
        else:
            paste_scaled(img, self._static[i], 540, cy, 0.88 + 0.12 * pop(u / 0.45), alpha=ease(u / 0.22))
        self.dynamic(img, sc, t, u)
        for c in self.sc_bounds[1:-1]:
            if 0 <= t - c < 0.1:
                img.alpha_composite(Image.new("RGBA", (W, H), (255, 245, 235, int(90 * (1 - (t - c) / 0.1)))))
        self.caption(img, t)
        return img.convert("RGB")


class FontsLatin(Fonts):
    def __init__(self):
        super().__init__("en")


def wrap(s, f, maxw):
    words = s.split(); lines = [""]
    for w_ in words:
        tst = (lines[-1] + " " + w_).strip()
        if f.getlength(tst) <= maxw or not lines[-1]:
            lines[-1] = tst
        else:
            lines.append(w_)
    if len(lines) == 2:  # balance two lines so a single word is never left alone
        best = None
        for k in range(1, len(words)):
            a, b = " ".join(words[:k]), " ".join(words[k:])
            m = max(f.getlength(a), f.getlength(b))
            if m <= maxw and (best is None or m < best[0]):
                best = (m, [a, b])
        if best:
            lines = best[1]
    return lines


def encode_range(short, t0, t1, path):
    n0, n1 = round(t0 * FPS), round(t1 * FPS); tmp = str(path) + ".tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-framerate", "30",
                          "-i", "-", *ENC, tmp], stdin=subprocess.PIPE)
    for n in range(n0, n1):
        p.stdin.write(short.frame(n / FPS).tobytes())
    p.stdin.close()
    if p.wait() != 0:
        raise RuntimeError(f"ffmpeg failed for {path}")
    os.replace(tmp, path)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(" ".join(cmd[:4]) + " failed: " + r.stderr[-400:])
    return r.stdout


def duration(path):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]).strip())


def render(job_dir, vo_mp3, vo_json, out_dir, workers=2):
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True); tmp = out / "_parts"; tmp.mkdir(exist_ok=True)
    qc = {"warnings": [], "errors": []}
    # fit the narration into 35 s by speeding up (max 1.15x) before anything is timed
    probe = Short.__new__(Short)
    prod, _ = load_job(job_dir)
    al = json.loads(Path(vo_json).read_text(encoding="utf-8"))["alignment"]
    raw_end = max(al["character_end_times_seconds"])
    speed = 1.0
    if THUMB_END + raw_end + 1.1 > MAX_LEN:
        speed = (THUMB_END + raw_end + 1.1) / (MAX_LEN - 0.2)
        if speed > 1.15:
            qc["errors"].append(f"narration too long: {raw_end:.1f}s even at 1.15x; shorten the script")
            speed = 1.15
        qc["warnings"].append(f"narration sped up {speed:.2f}x to fit 35 s")
    short = Short(job_dir, vo_json, speed)
    if short.total < MIN_LEN:
        qc["warnings"].append(f"video is {short.total:.1f}s, under 25 s; add a sentence")
    # thumbnail intro, exactly 0.00-0.30 s
    thumb = Path(job_dir) / "thumbnail.png"
    run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-i", str(thumb), "-vf",
         f"scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,format=yuv420p,loop=-1:1,trim=duration={THUMB_END}",
         *ENC, str(tmp / "p00.mp4")])
    # scenes, rendered in parallel worker processes
    jobs = [(i + 1, short.sc_bounds[i], short.sc_bounds[i + 1]) for i in range(len(short.scenes))]
    procs = []
    for wi in range(workers):
        mine = [j for j in jobs if (j[0] - 1) % workers == wi]
        pid = os.fork()
        if pid == 0:
            try:
                for idx, a, b in mine:
                    encode_range(short, a, b, tmp / f"p{idx:02d}.mp4")
                os._exit(0)
            except Exception as e:  # noqa
                print("worker error", e, file=sys.stderr); os._exit(1)
        procs.append(pid)
    bad = [p for p in procs if os.waitpid(p, 0)[1] != 0]
    if bad:
        raise RuntimeError("scene rendering failed")
    (tmp / "list.txt").write_text("".join(f"file 'p{i:02d}.mp4'\n" for i in range(len(jobs) + 1)))
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(tmp / "list.txt"), "-c", "copy", str(tmp / "v.mp4")])
    # audio: narration (sped up if needed) + original synthesized bed, ducked under the voice
    T = short.total
    af = f"atempo={speed:.4f}," if speed > 1.0001 else ""
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(vo_mp3), "-af",
         f"{af}adelay={int(THUMB_END * 1000)}:all=1,apad,atrim=0:{T},loudnorm=I=-15:TP=-2:LRA=11,aresample=48000", "-ar", "48000", str(tmp / "vo.wav")])
    mid = short.sc_bounds[max(1, len(short.scenes) // 2)]; last = short.sc_bounds[len(short.scenes) - 1]
    seed = short.rng.randint(1, 10_000); bpm = {"stage": 118, "stadium": 124, "pitch": 122, "news": 100, "tech": 110, "viral": 116}.get(short.theme, 112)
    bgm.make_bgm(T, mid, last, tmp / "bgm.wav", seed=seed, bpm=bpm)
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp / "bgm.wav"), "-af", "loudnorm=I=-29:TP=-8,aresample=48000", "-ar", "48000", str(tmp / "bgmn.wav")])
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp / "vo.wav"), "-i", str(tmp / "bgmn.wav"), "-filter_complex",
         "[0]asplit[v][sc];[1][sc]sidechaincompress=threshold=0.03:ratio=3:attack=20:release=300[b];[v][b]amix=inputs=2:normalize=0,volume=2dB,alimiter=limit=0.89",
         "-ar", "48000", str(tmp / "mix.wav")])
    final = out / "video.mp4"
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp / "v.mp4"), "-i", str(tmp / "mix.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
         "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out / "video.tmp.mp4")])
    os.replace(out / "video.tmp.mp4", final)
    # QC: length, first 0.30 s equals the thumbnail
    qc["duration"] = round(duration(final), 2)
    if not (MIN_LEN - 0.5 <= qc["duration"] <= MAX_LEN + 0.05):
        qc["warnings"].append(f"final length {qc['duration']}s is outside 25-35 s")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(final), "-frames:v", "10", str(tmp / "f%02d.png")])
    ref = Image.open(thumb).convert("RGB")
    if ref.size != (W, H):
        ref = Image.open(tmp / "f01.png").convert("RGB")
    a = np.asarray(ref, float)
    diffs = [round(float(np.abs(a - np.asarray(Image.open(tmp / f"f{i:02d}.png").convert("RGB"), float)).mean()), 1) for i in range(1, 11)]
    qc["first_frames_vs_thumbnail"] = diffs
    if max(diffs[:9]) > 4:
        qc["errors"].append("first 0.30 s does not match the thumbnail")
    qc["speed"] = round(speed, 3); qc["scenes"] = [round(x, 2) for x in short.sc_bounds]
    # contact sheet of the busiest moments for a human glance
    sheet = Image.new("RGB", (360 * len(short.scenes), 640))
    for i in range(len(short.scenes)):
        t = min(short.sc_bounds[i + 1] - 0.2, short.sc_bounds[i] + 1.8)
        sheet.paste(short.frame(t).resize((360, 640)), (360 * i, 0))
    sheet.save(out / "contact_sheet.jpg", quality=85)
    (out / "qc.json").write_text(json.dumps(qc, indent=2, ensure_ascii=False))
    import shutil
    shutil.rmtree(tmp, ignore_errors=True)
    return qc


if __name__ == "__main__":
    print(json.dumps(render(*sys.argv[1:5]), indent=2, ensure_ascii=False))
