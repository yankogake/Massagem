"""Gera a trilha sonora do vídeo: música original (deep house minimalista)
e efeitos sonoros sincronizados com os eventos da animação.

Uso: python3 tools/trilha.py roteiro-som.json saida.wav

O JSON vem de video.html (window.SOM), exportado por tools/renderizar.mjs:
  { "duracao": 20, "musica": {...}, "eventos": [{"t": 2.0, "tipo": "impacto"}, ...] }

Tudo é sintetizado aqui (sem samples), então a trilha é livre de direitos autorais.
"""
import json
import sys
import wave

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

SR = 44100
rng = np.random.default_rng(7)


# ---------------------------------------------------------------- utilidades
def midi(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def tempo(dur):
    return np.arange(int(dur * SR)) / SR


def filtro(x, tipo, freq, ordem=2):
    sos = butter(ordem, freq, btype=tipo, fs=SR, output="sos")
    return sosfilt(sos, x, axis=0)


def lpf_variavel(x, cortes):
    """Passa-baixa de um polo com frequência de corte variando por amostra."""
    a = 1 - np.exp(-2 * np.pi * np.clip(cortes, 20, SR / 2.2) / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc += a[i] * (x[i] - acc)
        y[i] = acc
    return y


def estereo(mono, pan=0.0):
    """pan de -1 (esquerda) a 1 (direita); aceita pan variável (array)."""
    ang = (np.asarray(pan) + 1) * np.pi / 4
    return np.stack([mono * np.cos(ang), mono * np.sin(ang)], axis=1)


def soma(pista, som, t):
    i = int(round(t * SR))
    if i >= len(pista):
        return
    if i < 0:
        som, i = som[-i:], 0
    n = min(len(som), len(pista) - i)
    pista[i:i + n] += som[:n]


def ruido(n):
    return rng.standard_normal(n)


# ---------------------------------------------------------------- instrumentos
def bumbo(forte=1.0):
    t = tempo(0.45)
    f = 48 + 120 * np.exp(-t / 0.028)
    corpo = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.22)
    clique = filtro(ruido(len(t)), "highpass", 3000) * np.exp(-t / 0.004) * 0.25
    return np.tanh(1.6 * (corpo + clique)) * forte


def chimbal(aberto=False):
    t = tempo(0.25 if aberto else 0.08)
    env = np.exp(-t / (0.06 if aberto else 0.018))
    return filtro(ruido(len(t)), "highpass", 7500) * env


def palma():
    t = tempo(0.3)
    env = sum(np.exp(-np.clip(t - d, 0, None) / 0.008) * (t >= d) for d in (0, 0.011, 0.023))
    env = env + 0.6 * np.exp(-np.clip(t - 0.03, 0, None) / 0.09) * (t >= 0.03)
    return filtro(ruido(len(t)), "bandpass", [900, 2600]) * env


def tecla(freq, dur, harm=8, detune=0.0, ataque=0.25, solta=0.6):
    """Pad suave: soma de harmônicos (dente de serra limitado em banda)."""
    t = tempo(dur + solta)
    f = freq * 2 ** (detune / 1200)
    s = sum(np.sin(2 * np.pi * k * f * t + k) / k for k in range(1, harm + 1))
    env = np.minimum(1, t / ataque) * np.where(t < dur, 1, np.exp(-(t - dur) / (solta / 3)))
    return s * env


def pluck(freq):
    t = tempo(0.5)
    s = np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(4 * np.pi * freq * t) + 0.1 * np.sin(6 * np.pi * freq * t)
    return s * np.exp(-t / 0.16) * np.minimum(1, t / 0.003)


def baixo(freq, dur=0.22):
    t = tempo(dur)
    s = np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(4 * np.pi * freq * t)
    env = np.minimum(1, t / 0.005) * np.exp(-t / 0.12)
    return np.tanh(1.5 * s) * env


def sino(freq, dur=2.5):
    """Sino FM (brilho)."""
    t = tempo(dur)
    mod = 2.2 * np.exp(-t / 0.4) * np.sin(2 * np.pi * freq * 3.5 * t)
    return np.sin(2 * np.pi * freq * t + mod) * np.exp(-t / 0.7) * np.minimum(1, t / 0.002)


# ---------------------------------------------------------------- efeitos
def whoosh(dur=0.45):
    """Centrado no instante do corte: sobe, passa e some."""
    t = tempo(dur)
    x = t / dur
    env = np.sin(np.pi * x) ** 2
    cortes = 400 + 7000 * np.sin(np.pi * x) ** 3
    mono = lpf_variavel(ruido(len(t)), cortes) * env
    return estereo(mono * 2.2, -0.7 + 1.4 * x)


def riser(dur):
    t = tempo(dur)
    x = t / dur
    cortes = 300 + 9000 * x ** 2.5
    sweep = np.sin(2 * np.pi * np.cumsum(200 + 1600 * x ** 2) / SR) * 0.12
    mono = (lpf_variavel(ruido(len(t)), cortes) * 1.4 + sweep) * x ** 2.2
    return estereo(mono)


def impacto():
    t = tempo(1.6)
    f = 32 + 70 * np.exp(-t / 0.06)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.5)
    estalo = filtro(ruido(len(t)), "lowpass", 2500) * np.exp(-t / 0.08) * 0.7
    return estereo(np.tanh(1.8 * (boom + estalo)))


def tique():
    t = tempo(0.06)
    s = np.sin(2 * np.pi * 2400 * t) * np.exp(-t / 0.008)
    s += filtro(ruido(len(t)), "highpass", 5000) * np.exp(-t / 0.004) * 0.3
    return estereo(s * 0.6)


PENTA = [72, 74, 76, 79, 81, 84, 86, 88, 91]


def pop(i=0):
    t = tempo(0.22)
    f0 = midi(PENTA[i % len(PENTA)])
    f = f0 * (1 + 0.5 * np.exp(-t / 0.01))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.05)
    return estereo(s * 0.55, ((i % 3) - 1) * 0.5)


def brilho():
    """Arpejo rápido de sinos (Fmaj9) para o logo."""
    out = np.zeros((int(3.2 * SR), 2))
    for k, m in enumerate([77, 81, 84, 88, 91]):
        soma(out, estereo(sino(midi(m)) * 0.35, -0.6 + 0.3 * k), k * 0.06)
    return out


EFEITOS = {"whoosh": lambda e: (whoosh(), -0.225),
           "riser": lambda e: (riser(e["dur"]), 0.0),
           "impacto": lambda e: (impacto(), 0.0),
           "tique": lambda e: (tique(), 0.0),
           "pop": lambda e: (pop(e.get("i", 0)), 0.0),
           "brilho": lambda e: (brilho(), 0.0)}


# ---------------------------------------------------------------- música
# Fmaj7 · Em7 · Dm7 · Cmaj7 (um acorde por compasso)
ACORDES = [[53, 57, 60, 64], [52, 55, 59, 62], [50, 53, 57, 60], [48, 52, 55, 59]]
BAIXOS = [41, 40, 38, 36]


def reverb(x, dur=2.4, decai=0.55):
    t = tempo(dur)
    ir = np.stack([ruido(len(t)), ruido(len(t))], axis=1) * np.exp(-t / decai)[:, None]
    ir = filtro(ir, "lowpass", 6000)
    ir /= np.sqrt((ir ** 2).sum(axis=0))
    return np.stack([fftconvolve(x[:, c], ir[:, c])[:len(x)] for c in range(2)], axis=1)


def musica(cfg, n):
    beat = 60 / cfg["bpm"]
    compasso = 4 * beat
    drop, pausa, fim_bat, dur = cfg["drop"], cfg["pausa"], cfg["fimBateria"], cfg["duracao"]
    bateria = np.zeros((n, 2))
    harm = np.zeros((n, 2))
    grave = np.zeros((n, 2))
    lateral = np.zeros(n)  # envelope de sidechain

    batidas = np.arange(0, fim_bat - 1e-6, beat)
    for b in batidas:
        if pausa[0] <= b < pausa[1]:
            continue
        soma(bateria, estereo(bumbo(0.9)), b)
        k = np.arange(n) / SR - b
        lateral += np.where(k >= 0, np.exp(-np.clip(k, 0, None) / 0.13), 0)
        if b < drop:
            continue
        idx = round(b / beat)
        if idx % 2 == 1:
            soma(bateria, estereo(palma() * 0.45, 0.1), b)
        soma(bateria, estereo(chimbal(aberto=True) * 0.22, 0.3), b + beat / 2)
        soma(bateria, estereo(chimbal() * 0.12, -0.3), b + beat / 4)
        soma(bateria, estereo(chimbal() * 0.1, -0.2), b + 3 * beat / 4)

    nc = int(np.ceil(dur / compasso))
    for c in range(nc):
        t0 = c * compasso
        acorde = ACORDES[c % 4]
        ultimo = t0 + compasso >= dur - 1e-6
        d = compasso + (1.5 if ultimo else 0)
        for m in acorde:
            for det, pan in ((-7, -0.6), (7, 0.6), (0, 0)):
                soma(harm, estereo(tecla(midi(m), d, detune=det) * 0.06, pan), t0)
        if t0 >= drop and t0 < fim_bat:
            for j in range(8):  # baixo nos contratempos (house)
                tb = t0 + j * beat / 2
                if j % 2 == 1 and not (pausa[0] <= tb < pausa[1]):
                    soma(grave, estereo(baixo(midi(BAIXOS[c % 4]))), tb)
            notas = [m + 12 for m in acorde]
            for j, k in enumerate([0, 2, 1, 3, 2, 1, 3, 2]):  # arpejo
                tp = t0 + j * beat / 2
                if not (pausa[0] <= tp < pausa[1]):
                    soma(harm, estereo(pluck(midi(notas[k])) * 0.11, -0.4 if j % 2 else 0.4), tp)

    harm = filtro(harm, "lowpass", 2600)
    # antes do drop: tudo abafado (efeito "rádio"), depois abre
    abafa = int(drop * SR)
    bateria[:abafa] = filtro(bateria[:abafa], "lowpass", 500)
    harm[:abafa] = filtro(harm[:abafa], "lowpass", 900)

    duck = (1 - 0.7 * np.clip(lateral, 0, 1))[:, None]
    harm = harm * duck
    grave = grave * duck
    mix = bateria * 0.85 + grave * 0.45 + harm * 0.9
    mix += reverb(harm * 0.5 + bateria * 0.08)
    return mix


# ---------------------------------------------------------------- principal
def main(roteiro, saida):
    with open(roteiro) as f:
        r = json.load(f)
    dur = r["duracao"]
    n = int(dur * SR)
    mus = musica({**r["musica"], "duracao": dur}, n)

    sfx = np.zeros((n, 2))
    for e in r["eventos"]:
        som, desloc = EFEITOS[e["tipo"]](e)
        soma(sfx, som * e.get("vol", 1.0), e["t"] + desloc)
    mix = mus + sfx * 0.55 + reverb(sfx * 0.25, 1.8, 0.4)

    # fade de saída e masterização simples
    fim = int(1.2 * SR)
    mix[-fim:] *= np.linspace(1, 0, fim)[:, None] ** 2
    mix = filtro(mix, "highpass", 28)
    mix /= np.abs(mix).max() + 1e-9
    mix = np.tanh(1.4 * mix) / np.tanh(1.4)
    mix *= 10 ** (-1 / 20)

    pcm = (mix * 32767).astype("<i2")
    with wave.open(saida, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print(f"trilha: {saida} ({dur:.1f}s, {len(r['eventos'])} efeitos)")


if __name__ == "__main__":
    main(*sys.argv[1:3])
