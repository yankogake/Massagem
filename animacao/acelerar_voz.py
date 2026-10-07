"""Deixa a narração mais rápida: encurta as pausas entre frases e acelera a fala (sem mudar o tom).

Uso: python3 acelerar_voz.py voz.mp3 saida.wav mapa.json [tempo=1.12] [pausa_max=0.12]
O mapa.json guarda os pontos (tempo_original, tempo_novo) para reposicionar as animações.
"""
import json, re, subprocess, sys, wave
import numpy as np

src, out_wav, out_map = sys.argv[1:4]
TEMPO = float(sys.argv[4]) if len(sys.argv) > 4 else 1.12
GAP = float(sys.argv[5]) if len(sys.argv) > 5 else 0.12
SR = 44100

# 1) pausas da fala
log = subprocess.run(["ffmpeg", "-hide_banner", "-i", src, "-af", "silencedetect=noise=-35dB:d=0.12", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
silences = list(zip(starts, ends))

# 2) áudio bruto
raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", src, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                     capture_output=True).stdout
x = np.frombuffer(raw, dtype=np.int16)
total = len(x) / SR

# 3) monta o áudio novo encurtando cada pausa para no máximo GAP (mantém a metade inicial e a final da pausa)
pieces, points, cur_old, cur_new = [], [(0.0, 0.0)], 0.0, 0.0
for s, e in silences:
    pieces.append(x[int(cur_old * SR):int(s * SR)]); cur_new += s - cur_old
    points.append((s, cur_new))
    dur = e - s
    if dur > GAP:
        h = GAP / 2
        pieces.append(x[int(s * SR):int((s + h) * SR)]); pieces.append(x[int((e - h) * SR):int(e * SR)])
        cur_new += GAP
    else:
        pieces.append(x[int(s * SR):int(e * SR)]); cur_new += dur
    points.append((e, cur_new)); cur_old = e
pieces.append(x[int(cur_old * SR):]); cur_new += total - cur_old
points.append((total, cur_new))
y = np.concatenate(pieces)

tmp = out_wav + ".tmp.wav"
with wave.open(tmp, "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(y.tobytes())

# 4) acelera mantendo o tom
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmp, "-af", f"atempo={TEMPO}", out_wav], check=True)
subprocess.run(["rm", "-f", tmp])

points = [(o, n / TEMPO) for o, n in points]
json.dump({"tempo": TEMPO, "gap": GAP, "points": points}, open(out_map, "w"), indent=1)
print(f"original {total:.2f}s -> novo {points[-1][1]:.2f}s")
