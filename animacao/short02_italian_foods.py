"""Vídeo 02: "3 'Italian' foods Americans get wrong" (1080x1920, 65–80 s) para TikTok (Creator Rewards, >60 s)
e YouTube Shorts (<3 min). Reaproveita as cenas da Caesar salad do short01.

Os tempos saem do roteiro (BEATS): cada beat é uma cena, e cada "pop" dispara numa palavra da narração.
Sem áudio, os tempos são estimados pelas sílabas; com --audio voz.mp3 eles se alinham às pausas reais da fala.

Uso:
  python3 short02_italian_foods.py [--audio voz.mp3] > pagina.html
  python3 short02_italian_foods.py [--audio voz.mp3] --sfx | --srt | --script
"""
import json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import short01_caesar as s01
from short01_caesar import (fill, line, running, thin, text, tag, red_x, pop, gus, scene, bowl, crouton,
                            INK, RED, GOLD, CREAM, W, H, FONT, gb)

# ---------- roteiro ----------
# (cena, narração, [(id do pop | [ids escalonados], palavra que dispara)])
BEATS = [
    ("h0", "Psst. These three Italian foods Americans love? They're not what you think. "
           "And number one isn't even from Italy.",
     [("hz", "three"), ("hp", "Italian"), ("hs", "foods")]),
    ("p1", "Number three: pepperoni.", [([f"pp{i}" for i in range(8)], "pepperoni")]),
    ("p2", "Order a pepperoni pizza in Italy, and you might get bell peppers. "
           "Because in Italian, peperoni means peppers.",
     [("itf", "Italy,"), ([f"bp{i}" for i in range(8)], "bell"), ("p2t", "means")]),
    ("p3", "The spicy salami Americans love was born in Italian-American butcher shops in New York, "
           "around nineteen nineteen.",
     [("sa0", "spicy"), ("sa1", "salami"), ("sa2", "born"), ("p3t", "Italian-American"), ("p3y", "nineteen")]),
    ("a1", "Number two: Fettuccine Alfredo. This one really is from Rome. A chef named Alfredo made it "
           "for his pregnant wife, with just pasta, butter and cheese.",
     [("a1t", "Rome."), ("bt", "butter"), ("ch", "cheese.")]),
    ("a2", "No cream.", [("a2x", "cream.")]),
    ("a3", "Then two Hollywood stars ate it on their honeymoon in nineteen twenty, and brought it home to America.",
     [("ht0", "honeymoon"), ("ht1", "twenty,"), ("a3t", "honeymoon")]),
    ("a4", "Where cooks added heavy cream to thicken the sauce.", [("usf", "cooks"), ("a4t", "heavy")]),
    ("a5", "In Italy, the simple version is just called pasta al burro: buttered pasta.",
     [("bt5", "simple"), ("a5t", "burro:")]),
    ("s1", "And number one: Caesar salad.", [("flag", "Caesar"), ("flagx", "salad.")]),
    ("s2", "Not Julius. Not Rome. Not even Italy.", [("t0", "Julius."), ("t1", "Rome."), ("t2", "Italy.")]),
    ("s3", "It was invented in Tijuana, Mexico, in the nineteen twenties,", [("pin", "Tijuana,"), ("year", "twenties,")]),
    ("s4", "by an Italian immigrant named Caesar Cardini.", [("name", "named")]),
    ("s5", "Legend says on a busy Fourth of July, the kitchen ran low, so he tossed in what he had.",
     [("fire", "busy"), ([f"i{i}" for i in range(14)], "tossed")]),
    ("s6", "Julius Caesar never had a single crouton.", [("@tear", "Julius"), ("@crouton", "single")]),
    ("out", "Follow for more food secrets. And psst... which food should I expose next?",
     [("outb", "psst..."), ("outt", "which")]),
]
HEADERS = {"h0": "3 'ITALIAN' FOODS", "p1": "#3 PEPPERONI", "p2": "IN ITALY...", "p3": "NEW YORK",
           "a1": "#2 FETTUCCINE ALFREDO", "a2": "THE ORIGINAL", "a3": "HOLLYWOOD", "a4": "IN AMERICA",
           "a5": "IN ITALY"}
GUS_IDS = ["g0", "gp2", "ga4", "g1", "g6", "go"]

# ---------- desenhos novos ----------

POLAR = [(0, 0), (0.56, 20), (0.56, 92), (0.56, 164), (0.56, 236), (0.56, 308), (0.3, 130), (0.3, 300)]

def _pol(cx, cy, r, f, deg):
    import math
    a = math.radians(deg)
    return cx + r * f * math.cos(a), cy + r * f * math.sin(a)

def pizza(cx, cy, r, topping=None, prefix=None):
    out = thin(fill("circle", f'cx="{cx}" cy="{cy}" r="{r}"', "#E2A65A", 30), 9)
    out += thin(fill("circle", f'cx="{cx}" cy="{cy}" r="{r*0.84:.0f}"', "#C8323F", 60), 6)
    for f, deg in [(0.45, 50), (0.62, 140), (0.4, 230), (0.66, 320), (0.15, 90), (0.7, 250)]:
        x, y = _pol(cx, cy, r, f, deg)
        out += fill("ellipse", f'cx="{x:.0f}" cy="{y:.0f}" rx="{r*0.2:.0f}" ry="{r*0.14:.0f}"', "#F5D27A", 0, stroke=False)
    for deg in (0, 60, 120):
        x1, y1 = _pol(cx, cy, r, 0.84, deg); x2, y2 = _pol(cx, cy, r, 0.84, deg + 180)
        out += f'<path d="M{x1:.0f},{y1:.0f} L{x2:.0f},{y2:.0f}" stroke="{CREAM}" stroke-width="4" stroke-dasharray="11 8" opacity="0.8"/>'
    for i, (f, deg) in enumerate(POLAR):
        x, y = _pol(cx, cy, r, f, deg)
        if topping == "pepperoni":
            el = (thin(fill("circle", f'cx="{x:.0f}" cy="{y:.0f}" r="{r*0.14:.0f}"', "#A3262F", 45), 6)
                  + f'<circle cx="{x-r*0.04:.0f}" cy="{y-r*0.03:.0f}" r="{r*0.025:.0f}" fill="#7A1A20"/>'
                  + f'<circle cx="{x+r*0.05:.0f}" cy="{y+r*0.04:.0f}" r="{r*0.02:.0f}" fill="#7A1A20"/>')
        elif topping == "peppers":
            c = "#3E9A3E" if i % 2 else "#D9412E"
            el = (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r*0.12:.0f}" fill="none" stroke="{INK}" stroke-width="{r*0.09:.0f}"/>'
                  + f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r*0.12:.0f}" fill="none" stroke="{c}" stroke-width="{r*0.05:.0f}"/>')
        else:
            continue
        out += pop(f"{prefix}{i}", round(x), round(y), el) if prefix else el
    return out

def bell_pepper(cx, cy, s, color):
    body = (f'M{cx-50*s},{cy-40*s} Q{cx-75*s},{cy+60*s} {cx-22*s},{cy+72*s} Q{cx},{cy+58*s} {cx+22*s},{cy+72*s} '
            f'Q{cx+75*s},{cy+60*s} {cx+50*s},{cy-40*s} Q{cx},{cy-62*s} {cx-50*s},{cy-40*s} Z')
    return (thin(fill("path", f'd="{body}"', color, 80), 7)
            + line(f"M{cx},{cy-50*s} Q{cx+6*s},{cy-80*s} {cx+24*s},{cy-88*s}", "#2E7D32", 14 * s, 0))

def salami(x, y, ln=300):
    out = f'<path d="M{x},{y-70} L{x},{y}" stroke="{INK}" stroke-width="6"/>'
    out += thin(fill("rect", f'x="{x-48}" y="{y}" width="96" height="{ln}" rx="48"', "#8E2B2B", 90), 8)
    for dx, dy in [(-18, 60), (14, 110), (-10, 170), (20, 220), (-20, 250), (8, 70)]:
        if dy < ln - 30:
            out += f'<circle cx="{x+dx}" cy="{y+dy}" r="7" fill="#F3E3D3"/>'
    out += running(f"M{x-30},{y+20} L{x+30},{y+20}", "#E7C48D", 4)
    return out

def skyline(base=1210):
    b = [(90, 130, 300, "#7C8BA5"), (225, 105, 430, "#6C7A93"), (335, 140, 270, "#8796AE"), (480, 100, 560, "#5F6C84"),
         (585, 135, 350, "#7C8BA5"), (725, 115, 460, "#6C7A93"), (845, 145, 290, "#8796AE")]
    out = ""
    for x, w, h, c in b:
        y = base - h
        if h == 560:  # prédio com antena, estilo Empire State
            out += thin(fill("rect", f'x="{x+30}" y="{y-60}" width="40" height="70"', c, 90), 7)
            out += f'<path d="M{x+50},{y-60} L{x+50},{y-130}" stroke="{INK}" stroke-width="7"/>'
        out += fill("rect", f'x="{x}" y="{y}" width="{w}" height="{h}"', c, 90)
        for wy in range(y + 30, base - 30, 55):
            for wx in range(x + 20, x + w - 25, 38):
                out += f'<rect x="{wx}" y="{wy}" width="16" height="24" rx="3" fill="#F5D547" opacity="0.75"/>'
    return out

def pasta_bowl(dx=0, dy=0, s=1.0):
    noodles = ""
    for k in range(6):
        y = 880 - 18 - k * 20
        d = f"M{260+k*18},{y} C{340},{y-60} {400},{y+40} {470},{y-20} S{600},{y+30} {690-k*18},{y-10}"
        noodles += line(d, INK, 30, 0) + line(d, "#F1D27B", 20, 90)
    front = (fill("path", 'd="M200,880 Q215,1150 470,1170 Q725,1150 740,880 Q470,945 200,880 Z"', CREAM, 0)
             + line("M222,960 Q470,1010 718,960", RED, 18, 0) + running("M240,1030 Q470,1080 700,1030", RED, 4))
    inner = thin(fill("ellipse", 'cx="470" cy="880" rx="270" ry="50"', "#E3D9C2", 0), 8) + noodles + front
    return f'<g transform="translate({dx},{dy}) translate(470,880) scale({s}) translate(-470,-880)">{inner}</g>'

def butter(cx, cy, s=1.0):
    return (f'<g transform="translate({cx},{cy}) scale({s})">'
            + thin(fill("rect", 'x="-90" y="-50" width="180" height="100" rx="14"', "#F7E07A", 0), 8)
            + thin(fill("path", 'd="M-90,-50 L-60,-80 L120,-80 L90,-50 Z"', "#FBEFA8", 0), 7)
            + running("M-70,-30 L70,-30", "#E8C64A", 4) + "</g>")

def cheese(cx, cy, s=1.0):
    return (f'<g transform="translate({cx},{cy}) scale({s})">'
            + thin(fill("path", 'd="M-110,60 L110,60 L110,-10 L-110,-70 Z"', "#F5C842", 20), 8)
            + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#DDA52A"/>' for x, y, r in [(-50, 10, 14), (30, 30, 10), (70, 0, 12)])
            + "</g>")

def carton(cx, cy, s=1.0):
    return (f'<g transform="translate({cx},{cy}) scale({s})">'
            + thin(fill("rect", 'x="-30" y="-250" width="60" height="40"', CREAM, 0), 7)
            + fill("path", 'd="M-120,-120 L0,-215 L120,-120 Z"', "#E9E4D8", 30)
            + fill("rect", 'x="-120" y="-120" width="240" height="340" rx="10"', CREAM, 90)
            + fill("rect", 'x="-120" y="10" width="240" height="110"', "#2F7FC8", 0, stroke=False)
            + text(0, 88, "CREAM", 62, CREAM)
            + running("M-100,-100 L100,-100 L100,200 L-100,200 Z", "#C9C2B0", 4) + "</g>")

def heart(cx, cy, s=1.0):
    return thin(fill("path", f'd="M0,32 C-64,-20 -32,-74 0,-36 C32,-74 64,-20 0,32 Z" '
                             f'transform="translate({cx},{cy}) scale({s})"', RED, 60), 7)

def clapper(cx, cy):
    return (f'<g transform="translate({cx},{cy})">'
            + fill("rect", 'x="-200" y="-90" width="400" height="260" rx="16"', "#2B2F3A", 0)
            + running("M-170,-40 L170,-40 M-170,40 L170,40 M0,-40 L0,140", "#F6F2E8", 4)
            + f'<g transform="rotate(-12 -200 -90)">'
            + fill("rect", 'x="-200" y="-160" width="400" height="70" rx="10"', "#F6F2E8", 0)
            + "".join(f'<path d="M{x},-160 L{x+40},-160 L{x+10},-90 L{x-30},-90 Z" fill="#2B2F3A"/>' for x in range(-170, 200, 80))
            + "</g></g>")

def flag_it(cx, cy, w=220, h=150, rot=8):
    x, y = cx - w / 2, cy - h / 2
    return (f'<g transform="rotate({rot} {cx} {cy})">'
            + fill("rect", f'x="{x}" y="{y}" width="{w}" height="{h}" rx="14"', CREAM, 0)
            + fill("rect", f'x="{x}" y="{y}" width="{w/3:.0f}" height="{h}"', "#2E8B4A", 90, stroke=False)
            + fill("rect", f'x="{x+2*w/3:.0f}" y="{y}" width="{w/3:.0f}" height="{h}"', RED, 90, stroke=False)
            + f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="none" stroke="{INK}" stroke-width="9"/></g>')

def flag_us(cx, cy, w=240, h=160, rot=-6):
    x, y = cx - w / 2, cy - h / 2
    stripes = "".join(fill("rect", f'x="{x}" y="{y + i*h/7:.1f}" width="{w}" height="{h/7:.1f}"',
                           RED if i % 2 == 0 else CREAM, 0, stroke=False) for i in range(7))
    stars = "".join(f'<circle cx="{x+22+c*28}" cy="{y+18+r*24}" r="5" fill="{CREAM}"/>' for c in range(3) for r in range(3))
    return (f'<g transform="rotate({rot} {cx} {cy})">' + stripes
            + fill("rect", f'x="{x}" y="{y}" width="{w*0.42:.0f}" height="{h*4/7:.0f}"', "#2B4A9A", 0, stroke=False) + stars
            + f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="none" stroke="{INK}" stroke-width="9"/></g>')

# ---------- cenas ----------

def new_scenes():
    sc = {}
    sc["h0"] = (pop("hz", 220, 440, pizza(220, 440, 105, "pepperoni"))
                + pop("hp", 540, 430, pasta_bowl(70, -450, 0.36))
                + pop("hs", 860, 440, f'<g transform="translate(390,-440) translate(470,880) scale(0.36) translate(-470,-880)">{bowl()}</g>')
                + gus(0.85, 540, 1010, id_="g0"))
    sc["p1"] = pizza(540, 800, 340, "pepperoni", prefix="pp")
    sc["p2"] = (pizza(540, 780, 300, "peppers", prefix="bp")
                + pop("itf", 820, 450, flag_it(840, 440, 200, 135))
                + pop("p2t", 540, 1200, tag(540, 1200, "PEPERONI = PEPPERS", 52))
                + gus(0.36, 175, 1110, id_="gp2"))
    sc["p3"] = (skyline(1210)
                + f'<path d="M150,430 L930,430" stroke="#86552A" stroke-width="18" stroke-linecap="round"/>'
                + running("M160,430 L920,430", "#E7C48D", 3)
                + pop("sa0", 300, 430, salami(300, 430, 290)) + pop("sa1", 540, 430, salami(540, 430, 340))
                + pop("sa2", 780, 430, salami(780, 430, 270))
                + pop("p3t", 540, 1290, tag(540, 1290, "ITALIAN-AMERICAN", 50))
                + pop("p3y", 860, 860, thin(fill("circle", 'cx="860" cy="860" r="78"', GOLD, 60), 8) + text(860, 882, "1919", 56)))
    sc["a1"] = (pasta_bowl(70, -10, 1.0)
                + pop("a1t", 540, 1250, tag(540, 1250, "MADE IN ROME", 54))
                + pop("bt", 280, 560, butter(280, 560)) + pop("ch", 800, 560, cheese(800, 560)))
    sc["a2"] = carton(540, 780, 1.4) + pop("a2x", 540, 800, red_x(540, 800, 230))
    sc["a3"] = (clapper(540, 760) + pop("ht0", 300, 470, heart(300, 470, 1.5)) + pop("ht1", 790, 450, heart(790, 450, 1.9))
                + pop("a3t", 540, 1150, tag(540, 1150, "1920 HONEYMOON", 54)))
    sc["a4"] = (carton(430, 800, 1.2) + pop("usf", 790, 560, flag_us(790, 560))
                + pop("a4t", 540, 1250, tag(540, 1250, "+ HEAVY CREAM", 54)) + gus(0.38, 870, 1080, id_="ga4"))
    sc["a5"] = (pasta_bowl(70, -10, 1.0) + pop("bt5", 540, 560, butter(540, 560, 1.2))
                + pop("a5t", 540, 1250, tag(540, 1250, "PASTA AL BURRO", 54)))
    sc["out"] = (gus(0.95, 500, 860, id_="go")
                 + pop("outb", 747, 613, f'<g transform="translate(500,860) scale(0.95) translate(-500,-560)">{gb.bubble()}</g>')
                 + pop("outt", 540, 1290, tag(540, 1290, "WHICH FOOD NEXT?", 58, GOLD)))
    return "".join(scene(k, v, HEADERS.get(k)) for k, v in sc.items())

def caesar_scenes():
    """Cenas s1–s6 do short01, com o título '#1 CAESAR SALAD'. A s7 (despedida antiga) fica sem uso."""
    s = s01.scenes()
    s = s.replace(">CAESAR SALAD<", ">#1 CAESAR SALAD<")
    return s

# ---------- tempos ----------

def syl(word):
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    n = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and not w.endswith(("le", "ee")) and n > 1:
        n -= 1
    return max(n, 1)

def speech_segments(audio):
    log = subprocess.run(["ffmpeg", "-hide_banner", "-i", audio, "-af", "silencedetect=noise=-35dB:d=0.1",
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    dur = float(re.search(r"Duration: (\d+):(\d+):([\d.]+)", log).groups()[2]) + \
        60 * float(re.search(r"Duration: (\d+):(\d+):", log).groups()[1])
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
    segs, cur = [], 0.0
    for s, e in zip(st, en):
        if s > cur:
            segs.append((cur, s))
        cur = e
    if cur < dur:
        segs.append((cur, dur))
    return [(a, b) for a, b in segs if b - a > 0.05], dur

def word_times(audio=None):
    """Tempo (s) de início de cada palavra do roteiro, e a duração total."""
    words = [(bi, w) for bi, (_, txt, _) in enumerate(BEATS) for w in txt.split()]
    weights = [syl(w) for _, w in words]
    if not audio:  # estimativa: 4,4 sílabas/s + pausa nas pontuações
        t, out = 0.2, []
        for (bi, w), k in zip(words, weights):
            out.append(t)
            t += k / 4.4 + (0.3 if w[-1] in ".?:" else 0.12 if w[-1] == "," else 0)
        return words, out, t + 1.0
    segs, dur = speech_segments(audio)
    speech = sum(b - a for a, b in segs)
    total = sum(weights)
    out, acc = [], 0.0
    for k in weights:
        target = acc / total * speech  # posição no "relógio só de fala"
        for a, b in segs:              # converte para o tempo real
            if target <= b - a:
                out.append(a + target); break
            target -= b - a
        else:
            out.append(segs[-1][1])
        acc += k
    # cada beat começa no início de um trecho de fala (pausas reais são as fronteiras naturais)
    starts = [a for a, _ in segs]
    for bi in range(len(BEATS)):
        idx = next(i for i, (b, _) in enumerate(words) if b == bi)
        near = min(starts, key=lambda s: abs(s - out[idx]))
        if abs(near - out[idx]) < 0.7:
            shift = near - out[idx]
            j = idx
            while j < len(words) and words[j][0] == bi:
                out[j] += shift * (1 - (j - idx) / max(1, sum(1 for b, _ in words if b == bi)))
                j += 1
    return words, out, dur + 1.2

def timeline(audio=None):
    words, wt, dur = word_times(audio)
    first = {}
    for (bi, _), t in zip(words, wt):
        first.setdefault(bi, t)
    starts = [max(0.0, first[bi] - 0.08) if bi else 0.0 for bi in range(len(BEATS))]
    scenes_t = [(BEATS[i][0], round(starts[i], 3), round(starts[i + 1] if i + 1 < len(BEATS) else dur, 3))
                for i in range(len(BEATS))]
    pops, tear, crouton_t = {}, None, None
    for bi, (sid, _, plist) in enumerate(BEATS):
        bw = [(w, t) for (b, w), t in zip(words, wt) if b == bi]
        pops[f"{sid}h"] = round(starts[bi] + 0.03, 3)
        for ids, trig in plist:
            norm = lambda x: re.sub(r"[^a-z-]", "", x.lower())
            match = [t for w, t in bw if norm(w) == norm(trig)]
            assert match, f"palavra '{trig}' não está no beat {sid}"
            t = match[0]
            if ids == "@tear":
                tear = t
            elif ids == "@crouton":
                crouton_t = t - 0.25
            elif isinstance(ids, list):
                for k, i in enumerate(ids):
                    pops[i] = round(t + k * 0.07, 3)
            else:
                pops[ids] = round(t, 3)
    caps = []
    for bi, (sid, txt, _) in enumerate(BEATS):  # legendas de 2–4 palavras para o .srt
        bw = [(w, t) for (b, w), t in zip(words, wt) if b == bi]
        for i in range(0, len(bw), 3):
            a = bw[i][1]
            b = bw[i + 3][1] if i + 3 < len(bw) else scenes_t[bi][2]
            caps.append((round(a, 3), round(b, 3), " ".join(w for w, _ in bw[i:i + 3])))
    return scenes_t, pops, tear, crouton_t, caps, round(dur, 2)

def sfx_events(scenes_t, pops, crouton_t):
    ev = []
    for k, t in pops.items():
        if k in ("flagx", "t0", "t1", "t2", "a2x"):
            ev.append([t, "stamp", 0])
        elif k.endswith("h") and any(k == f"{s}h" for s, _, _ in scenes_t):
            ev.append([t, "tick", 0])
        elif re.fullmatch(r"(i|pp|bp)\d+", k):
            ev.append([t, "pop", int(re.sub(r"\D", "", k))])
        else:
            ev.append([t, "pop", 0])
    ev += [[a - 0.1, "whoosh", 0] for _, a, _ in scenes_t[1:]]
    ev.append([crouton_t + s01.FALL, "bonk", 0])
    return sorted(ev)

def build(audio=None):
    scenes_t, pops, tear, crouton_t, caps, dur = timeline(audio)
    base = gb.build("roma")
    defs = base[base.index("<defs>"):base.index("</defs>") + 7]
    defs = defs.replace('<feTurbulence type="fractalNoise" baseFrequency="0.035"',
                        '<feTurbulence id="turb" type="fractalNoise" baseFrequency="0.035"')
    defs = defs.replace('width="1000" height="1000">', f'width="{W}" height="{H}">')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  {defs}
  <rect width="{W}" height="{H}" fill="url(#pique)"/>
  <rect width="{W}" height="{H}" filter="url(#grain)"/>
  {new_scenes()}{caesar_scenes()}
  <rect width="{W}" height="{H}" fill="url(#vig)"/>
  <g id="capg"><text id="cap"></text></g>
</svg>'''
    js = s01.JS.replace("for (const id of ['g1', 'g6', 'g7'])", "for (const id of GUS_IDS)")
    data = (f"const SCENES = {json.dumps(scenes_t)};\nconst CAPTIONS = [];\nconst HIGHLIGHT = [];\n"
            f"const POPS = {json.dumps(pops)};\nconst GUS_IDS = {json.dumps(GUS_IDS)};\n"
            f"const TEAR = {tear}, CROUTON_DROP = {crouton_t}, FALL = {s01.FALL}, BOUNCE = {s01.BOUNCE}, SHOW_CAPTIONS = false;\n")
    return f'''<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@800&display=block" rel="stylesheet">
<style>body{{margin:0;background:#000}}</style></head><body>{svg}
<script>{data}{js}</script></body></html>''', dur

if __name__ == "__main__":
    audio = sys.argv[sys.argv.index("--audio") + 1] if "--audio" in sys.argv else None
    scenes_t, pops, tear, crouton_t, caps, dur = timeline(audio)
    if "--script" in sys.argv:
        print(" ".join(t for _, t, _ in BEATS))
    elif "--srt" in sys.argv:
        ts = lambda x: f"{int(x//3600):02d}:{int(x%3600//60):02d}:{int(x%60):02d},{int(round(x%1*1000)):03d}"
        print("\n".join(f"{i}\n{ts(a)} --> {ts(b)}\n{t}\n" for i, (a, b, t) in enumerate(caps, 1)))
    elif "--sfx" in sys.argv:
        print(json.dumps({"duration": dur, "events": sfx_events(scenes_t, pops, crouton_t)}))
    elif "--times" in sys.argv:
        print(dur); [print(s) for s in scenes_t]
    else:
        print(build(audio)[0])
