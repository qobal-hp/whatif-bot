"""Original synthesized sports/news tension bed (no samples, no licensed audio)."""
import numpy as np, soundfile as sf
SR = 48000

def make_bgm(TOTAL, Q4, FINAL, out_path, seed=3, bpm=120):
    BPM = bpm; beat = 60 / BPM
    n = int(TOTAL * SR); out = np.zeros((n, 2))
    rng = np.random.default_rng(seed)
    t_all = np.arange(n) / SR

    def add(sig, at, pan=0.0, g=1.0):
        i = int(at * SR)
        if i >= n: return
        sig = sig[: n - i]
        out[i:i + len(sig), 0] += sig * g * (1 - max(0, pan))
        out[i:i + len(sig), 1] += sig * g * (1 + min(0, pan))

    def kick():
        t = np.arange(int(0.35 * SR)) / SR
        f = 50 + 90 * np.exp(-t * 30)
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)
    def snare():
        t = np.arange(int(0.25 * SR)) / SR
        nz = rng.standard_normal(len(t)); nz = np.diff(np.concatenate([[0], nz]))
        return (0.6 * nz + 0.4 * np.sin(2 * np.pi * 190 * t)) * np.exp(-t * 18)
    def hat():
        t = np.arange(int(0.06 * SR)) / SR
        nz = np.diff(np.concatenate([[0], rng.standard_normal(len(t))]))
        return nz * np.exp(-t * 70)
    def bass(freq, dur):
        t = np.arange(int(dur * SR)) / SR
        s = 2 * ((freq * t) % 1) - 1
        s = np.convolve(s, np.ones(24) / 24, 'same')   # soften the saw
        env = np.minimum(1, t * 200) * np.exp(-t * 3)
        return s * env
    def hit():
        t = np.arange(int(1.6 * SR)) / SR
        k = kick()[: len(t)]; k = np.pad(k, (0, len(t) - len(k)))
        nz = rng.standard_normal(len(t)) * np.exp(-t * 4) * 0.35
        chord = sum(np.sin(2 * np.pi * f * t) for f in (110, 164.8, 220, 261.6)) * np.exp(-t * 2) * 0.25
        return 1.3 * k + nz + chord

    roots = [55.0, 55.0, 43.65, 49.0]  # A A F G (minor, driving)
    nb = int(TOTAL / beat) + 1
    for b in range(nb):
        at = 0.3 + b * beat
        if at >= TOTAL - 0.6: break
        q4 = at >= Q4
        bar = b // 4
        add(kick(), at, g=0.9)
        if b % 4 in (1, 3): add(snare(), at, g=0.45 if not q4 else 0.6)
        add(hat(), at + beat / 2, pan=0.3, g=0.25)
        if q4: add(hat(), at, pan=-0.3, g=0.18); add(kick(), at + beat * 0.75, g=0.5) if b % 2 else None
        r = roots[bar % 4]
        add(bass(r, beat * 0.5), at, g=0.35)
        add(bass(r * 2 if q4 else r, beat * 0.45), at + beat / 2, g=0.25)

    # riser into Q4
    rl = 1.6; t = np.arange(int(rl * SR)) / SR
    riser = rng.standard_normal(len(t)) * (t / rl) ** 2 * 0.35
    add(riser, Q4 - rl, g=1.0)
    add(hit(), Q4, g=0.8)
    add(hit(), FINAL, g=0.7)
    # fade out tail
    fo = int(1.2 * SR); out[-fo:] *= np.linspace(1, 0, fo)[:, None]
    out /= np.max(np.abs(out)) + 1e-9
    sf.write(str(out_path), out * 0.9, SR)
