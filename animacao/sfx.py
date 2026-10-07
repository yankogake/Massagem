"""Efeitos sonoros sintetizados (sem arquivos de terceiros) e montagem da trilha de efeitos.

Uso: python3 sfx.py eventos.json saida.wav duracao
eventos.json: lista de [tempo, tipo, variação] com tipo em pop | tick | stamp | whoosh | bonk.
"""
import json, sys, wave
import numpy as np

SR = 44100
rng = np.random.default_rng(3)

def env(n, attack=0.002, decay=0.05):
    t = np.arange(n) / SR
    return np.minimum(t / attack, 1) * np.exp(-t / decay)

def sweep(f0, f1, dur):
    t = np.arange(int(dur * SR)) / SR
    f = f0 * (f1 / f0) ** (t / dur)
    return np.sin(2 * np.pi * np.cumsum(f) / SR)

def pop(v=0.0):
    """'Pop' de bolha: sweep descendente rápido + clique."""
    base = 700 * 2 ** (v / 12)
    s = sweep(base * 1.6, base * 0.55, 0.09) * env(int(0.09 * SR), 0.001, 0.028)
    click = rng.normal(0, 1, int(0.004 * SR)) * 0.35
    s[:len(click)] += click
    return s * 0.9

def tick(v=0.0):
    """Toque leve para etiquetas de título."""
    s = sweep(1900 * 2 ** (v / 12), 1500, 0.04) * env(int(0.04 * SR), 0.001, 0.01)
    return s * 0.45

def stamp(v=0.0):
    """Carimbo: baque grave + ruído curto."""
    n = int(0.22 * SR)
    thud = sweep(150, 55, 0.22) * env(n, 0.001, 0.06)
    noise = rng.normal(0, 1, n) * env(n, 0.001, 0.015) * 0.6
    return (thud + noise) * 0.95

def whoosh(v=0.0):
    """Whoosh de transição: ruído filtrado que cresce e some."""
    n = int(0.28 * SR)
    noise = rng.normal(0, 1, n)
    k = 30
    lp = np.convolve(noise, np.ones(k) / k, mode="same")       # passa-baixa simples
    bp = lp - np.convolve(lp, np.ones(200) / 200, mode="same")  # tira o grave
    t = np.linspace(0, 1, n)
    return bp * np.sin(np.pi * t) ** 2 * 2.2

def bonk(v=0.0):
    """'Tok' de bloco de madeira (crouton batendo na cabeça)."""
    n = int(0.15 * SR)
    t = np.arange(n) / SR
    s = (np.sin(2 * np.pi * 820 * t) + 0.5 * np.sin(2 * np.pi * 1640 * t)) * env(n, 0.0005, 0.03)
    return s * 0.9

KINDS = {"pop": pop, "tick": tick, "stamp": stamp, "whoosh": whoosh, "bonk": bonk}

if __name__ == "__main__":
    events, out, dur = json.load(open(sys.argv[1])), sys.argv[2], float(sys.argv[3])
    track = np.zeros(int(dur * SR) + SR)
    for t, kind, v in events:
        s = KINDS[kind](v)
        i = int(max(t, 0) * SR)
        track[i:i + len(s)] += s[:len(track) - i]
    track = np.clip(track * 0.5, -1, 1)
    with wave.open(out, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((track[:int(dur * SR)] * 32767).astype(np.int16).tobytes())
