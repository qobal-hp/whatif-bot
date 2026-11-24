"""Generate an original, calm ambient bed for one episode (no samples, no licensing).

usage: python biblia/make_music.py <out.mp3> <seed> [minutes]
Each seed gives a different key, tempo, chord progression, instrument colour and melody,
so no two episodes share a track. The track is built to loop (renderer loops it).
"""
import subprocess
import sys

import numpy as np
import zlib

from scipy.signal import fftconvolve, lfilter

SR = 44100
rng = np.random.default_rng(zlib.crc32(sys.argv[2].encode()))
out = sys.argv[1]
minutes = float(sys.argv[3]) if len(sys.argv) > 3 else 6

root = 48 + int(rng.integers(0, 12))  # C3..B3
minor = rng.random() < 0.5
scale = [0, 2, 3, 5, 7, 8, 10] if minor else [0, 2, 4, 5, 7, 9, 11]
progs = [[0, 5, 3, 4], [0, 3, 5, 4], [0, 4, 5, 3], [5, 3, 0, 4], [0, 5, 1, 4], [0, 2, 5, 4]]
prog = progs[int(rng.integers(len(progs)))]
chord_sec = float(rng.uniform(7, 11))
bright = float(rng.uniform(0.2, 0.7))   # how many upper harmonics the pad has
bell = rng.random() < 0.6               # soft piano-like melody notes or not
detune = float(rng.uniform(0.002, 0.006))


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


def deg(d, octave=0):
    return root + scale[d % 7] + 12 * (d // 7 + octave)


def pad(freqs, dur):
    t = np.arange(int(dur * SR)) / SR
    s = np.zeros_like(t)
    for f in freqs:
        for k, amp in ((1, 1.0), (2, 0.35 * bright), (3, 0.15 * bright)):
            for d in (-detune, 0, detune):
                s += amp * np.sin(2 * np.pi * f * k * (1 + d) * t + rng.uniform(0, 6.28))
    env = np.minimum(1, t / 2.5) * np.minimum(1, (dur - t) / 2.5)
    return s * env / (len(freqs) * 6)


def note(f, dur):
    t = np.arange(int(dur * SR)) / SR
    s = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t) * np.exp(-t * 3)
    return s * np.exp(-t * 1.2) * np.minimum(1, t / 0.02) * 0.22


total = int(minutes * 60 * SR)
mix = np.zeros(total + SR * 12)
pos, i = 0.0, 0
while pos * SR < total:
    d = prog[i % len(prog)]
    freqs = [hz(deg(d)), hz(deg(d + 2)), hz(deg(d + 4)), hz(deg(d, -1))]
    seg = pad(freqs, chord_sec + 3)
    a = int(pos * SR)
    mix[a:a + len(seg)] += seg[: len(mix) - a]
    if bell:
        for _ in range(int(rng.integers(1, 4))):
            when = pos + rng.uniform(0.5, chord_sec - 1)
            n = note(hz(deg(d + int(rng.choice([0, 2, 4, 7, 9])), 1)), 4)
            b = int(when * SR)
            mix[b:b + len(n)] += n[: len(mix) - b]
    pos += chord_sec
    i += 1
mix = mix[:total]

# Big soft hall reverb from decaying noise.
ir_t = np.arange(int(3.5 * SR)) / SR
ir = rng.standard_normal(len(ir_t)) * np.exp(-ir_t * 1.6)
wet = fftconvolve(mix, ir)[:total]
wet /= np.max(np.abs(wet)) + 1e-9
dry = mix / (np.max(np.abs(mix)) + 1e-9)
y = 0.55 * wet + 0.45 * dry
# Gentle low-pass for sleep: one-pole filter.
yl = lfilter([0.18], [1, -0.82], y)
yl /= np.max(np.abs(yl)) + 1e-9
fade = int(4 * SR)
yl[:fade] *= np.linspace(0, 1, fade)
yl[-fade:] *= np.linspace(1, 0, fade)
stereo = np.stack([yl, np.roll(yl, int(0.012 * SR))], 1)
pcm = (stereo * 0.7 * 32767).astype(np.int16).tobytes()
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "s16le", "-ar", str(SR), "-ac", "2", "-i", "-",
                "-b:a", "160k", "-f", "mp3", out], input=pcm, check=True)
print(f"{out}: root {root} {'minor' if minor else 'major'} prog {prog} {chord_sec:.1f}s/chord bell={bell}")
