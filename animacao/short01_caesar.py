"""Short 01: "Caesar salad isn't from Italy" (1080x1920, ~36 s).

Gera um HTML com todas as cenas em SVG bordado e uma função JS setT(t) que posiciona
tudo no instante t (segundos). O render_html.js chama setT quadro a quadro.
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "personagem"))
import gerar_bordado as gb
from gerar_bordado import fill, line, running, INK

W, H = 1080, 1920
FONT = "'Baloo 2',sans-serif"
RED, GOLD, CREAM = "#C8323F", "#E9B83F", "#F6F2E8"

# ---------- elementos ----------

def thin(svg, w):
    return svg.replace(f'stroke-width="{gb.SW}"', f'stroke-width="{w}"')

def text(x, y, s, size, color=INK, anchor="middle", sat=80):
    a = f'x="{x}" y="{y}" text-anchor="{anchor}" font-family="{FONT}" font-weight="800" font-size="{size}"'
    return f'<text {a} fill="{color}">{s}</text><text {a} fill="url(#sat{sat})">{s}</text>'

def tag(cx, cy, s, size=58, color=CREAM, ink=INK, stitch=RED):
    w, h = len(s) * size * 0.58 + 90, size * 1.9
    x, y = cx - w / 2, cy - h / 2
    return (thin(fill("rect", f'x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{h/3:.0f}"', color, 0), 8)
            + f'<rect x="{x+14:.0f}" y="{y+14:.0f}" width="{w-28:.0f}" height="{h-28:.0f}" rx="{h/3-10:.0f}" fill="none" '
              f'stroke="{stitch}" stroke-width="4" stroke-dasharray="11 8"/>'
            + text(cx, cy + size * 0.36, s, size, ink))

def red_x(cx, cy, r):
    d = f"M{cx-r},{cy-r} L{cx+r},{cy+r} M{cx+r},{cy-r} L{cx-r},{cy+r}"
    return line(d, CREAM, r * 0.55, 0) + line(d, RED, r * 0.34, 45)

def pop(id_, cx, cy, inner):
    """Grupo que o JS escala em volta de (cx, cy)."""
    return f'<g id="{id_}" data-c="{cx},{cy}">{inner}</g>'

LEAVES = [(330, 850, 95, 55, -30, "#4E9A3E"), (640, 870, 85, 48, 35, "#6DB353"), (380, 770, 90, 50, -40, "#9BCB5A"),
          (580, 830, 100, 58, 20, "#4E9A3E"), (520, 750, 95, 52, 15, "#9BCB5A"), (450, 800, 110, 60, -10, "#6DB353"),
          (470, 862, 120, 55, 0, "#5FAE4A")]
CROUTONS = [(400, 790, 20), (505, 768, -15), (585, 805, 30), (440, 852, 8), (622, 842, -25)]

def leaf(cx, cy, rx, ry, rot, c):
    t = f'transform="rotate({rot} {cx} {cy})"'
    return (thin(fill("ellipse", f'cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"', c, 30, extra=t), 7)
            + f'<path d="M{cx-rx+20},{cy} L{cx+rx-20},{cy}" stroke="#CDE8A8" stroke-width="4" '
              f'stroke-dasharray="10 7" {t}/>')

def crouton(cx, cy, rot):
    t = f'transform="rotate({rot} {cx} {cy})"'
    return (thin(fill("rect", f'x="{cx-24}" y="{cy-24}" width="48" height="48" rx="11"', "#D9A441", 45, extra=t), 6)
            + f'<circle cx="{cx-7}" cy="{cy-6}" r="4" fill="#A8741F"/><circle cx="{cx+8}" cy="{cy+7}" r="4" fill="#A8741F"/>')

def bowl(prefix=None):
    """Tigela (coordenadas locais com a borda centrada em 470,880). Com prefix, cada ingrediente ganha id p/ animar."""
    back = thin(fill("ellipse", 'cx="470" cy="880" rx="270" ry="50"', "#E3D9C2", 0), 8)
    items = [leaf(*l) for l in LEAVES] + [crouton(*c) for c in CROUTONS]
    centers = [(l[0], l[1]) for l in LEAVES] + [(c[0], c[1]) for c in CROUTONS]
    items += ['<polygon points="352,815 372,808 368,828" fill="#F7EFC8" stroke="#262A36" stroke-width="3"/>',
              '<polygon points="540,815 562,812 552,832" fill="#F7EFC8" stroke="#262A36" stroke-width="3"/>']
    centers += [(362, 817), (551, 820)]
    if prefix:
        items = [pop(f"{prefix}{i}", cx, cy, it) for i, (it, (cx, cy)) in enumerate(zip(items, centers))]
    front = (fill("path", 'd="M200,880 Q215,1150 470,1170 Q725,1150 740,880 Q470,945 200,880 Z"', CREAM, 0)
             + line("M222,960 Q470,1010 718,960", "#2F7FC8", 18, 0)
             + running("M240,1030 Q470,1080 700,1030", "#2F7FC8", 4))
    return back + "".join(items) + front

def bust(sad=False):
    """Busto de mármore do Júlio César (coordenadas locais iguais às do Gus: cabeça em 500,340)."""
    m = "#F1EEE8"
    brows = ("M405,282 Q440,262 478,270 M522,270 Q560,262 595,282" if sad
             else "M405,268 Q440,282 478,284 M522,284 Q560,282 595,268")
    mouth = "M455,462 Q500,440 545,462" if sad else "M458,452 L542,452"
    return f'''
    {fill("rect", 'x="300" y="840" width="400" height="34" rx="8"', "#DAD5CB", 0)}
    {fill("rect", 'x="335" y="872" width="330" height="80" rx="8"', "#E6E1D7", 90)}
    {fill("path", 'd="M230,850 Q240,640 400,600 L600,600 Q760,640 770,850 Z"', "#ECE8E0", 20)}
    {running("M300,840 Q330,700 450,640")}{running("M560,630 Q690,690 720,840")}
    {fill("rect", 'x="440" y="470" width="120" height="160"', m, 90)}
    {thin(fill("ellipse", 'cx="352" cy="350" rx="24" ry="40"', m, 90), 8)}
    {thin(fill("ellipse", 'cx="648" cy="350" rx="24" ry="40"', m, 90), 8)}
    {fill("ellipse", 'cx="500" cy="340" rx="150" ry="178"', m, 60)}
    {gb.laurel()}
    {thin(fill("ellipse", 'cx="440" cy="330" rx="32" ry="15"', "#E2DED4", 0), 6)}
    {thin(fill("ellipse", 'cx="560" cy="330" rx="32" ry="15"', "#E2DED4", 0), 6)}
    {line(brows, INK, 11, 0)}
    <path d="M500,330 L482,408 Q500,420 518,408" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>
    <path d="{mouth}" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>
    '''

def chef():
    skin = "#EFC39C"
    return f'''
    {fill("path", 'd="M220,985 Q230,800 400,760 L600,760 Q770,800 780,985 Z"', CREAM, 20)}
    {"".join(thin(fill("circle", f'cx="{x}" cy="{y}" r="13"', GOLD, 0), 5) for x in (455, 545) for y in (870, 935))}
    {thin(fill("path", 'd="M410,748 L590,748 L500,840 Z"', RED, 60), 7)}
    {thin(fill("circle", 'cx="322" cy="575" r="36"', skin, 0), 8)}{thin(fill("circle", 'cx="678" cy="575" r="36"', skin, 0), 8)}
    {fill("circle", 'cx="500" cy="565" r="182"', skin, 70)}
    {fill("circle", 'cx="390" cy="290" r="95"', CREAM, 30)}{fill("circle", 'cx="610" cy="290" r="95"', CREAM, 120)}
    {fill("circle", 'cx="500" cy="240" r="115"', CREAM, 80)}
    {fill("rect", 'x="335" y="330" width="330" height="95" rx="12"', CREAM, 0)}
    {running("M355,360 L645,360", "#C9C2B0")}
    <ellipse cx="410" cy="625" rx="30" ry="17" fill="#E98494" opacity="0.6"/>
    <ellipse cx="590" cy="625" rx="30" ry="17" fill="#E98494" opacity="0.6"/>
    <circle cx="440" cy="550" r="17" fill="{INK}"/><circle cx="560" cy="550" r="17" fill="{INK}"/>
    <circle cx="446" cy="544" r="5" fill="#fff"/><circle cx="566" cy="544" r="5" fill="#fff"/>
    {line("M410,505 Q440,490 470,500 M530,500 Q560,490 590,505", INK, 10, 0)}
    {thin(fill("ellipse", 'cx="500" cy="602" rx="32" ry="25"', "#E2A57E", 0), 7)}
    {thin(fill("path", 'd="M500,640 Q450,612 402,640 Q378,656 394,678 Q432,664 500,664 Q568,664 606,678 Q622,656 598,640 Q550,612 500,640 Z"', "#3D2A1E", 0), 7)}
    <path d="M458,705 Q500,735 542,705" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>
    '''

def gus(scale, cx, cy, with_bubble=False, id_="g"):
    b = f'<g id="{id_}b" data-c="760,300">{gb.bubble()}</g>' if with_bubble else ""
    return (f'<g transform="translate({cx},{cy}) scale({scale}) translate(-500,-560)">'
            f'<g id="{id_}">{gb.pigeon("roma")}{b}</g></g>')

def scene(id_, inner, header=None):
    h = f'<g id="{id_}h" data-c="540,245">{tag(540, 245, header, 54)}</g>' if header else ""
    return f'<g id="{id_}" style="display:none"><g filter="url(#emb)">{inner}{h}</g></g>'

# ---------- cenas ----------

def scenes():
    s1 = scene("s1", f'''
      <g transform="translate(0,-40)">{bowl()}</g>
      {pop("flag", 800, 520, f"""<g transform="rotate(8 800 520)">
        {fill("rect", 'x="690" y="445" width="220" height="150" rx="14"', CREAM, 0)}
        {fill("rect", 'x="690" y="445" width="73" height="150"', "#2E8B4A", 90, stroke=False)}
        {fill("rect", 'x="837" y="445" width="73" height="150"', RED, 90, stroke=False)}
        <rect x="690" y="445" width="220" height="150" rx="14" fill="none" stroke="{INK}" stroke-width="9"/>
        {running("M705,460 L895,460 L895,580 L705,580 Z", "#C9C2B0", 3)}</g>""")}
      {pop("flagx", 800, 520, red_x(800, 520, 95))}
      {gus(0.46, 905, 1095, id_="g1")}''', "CAESAR SALAD")

    tags = "".join(pop(f"t{i}", 800, y, tag(820, y, s, 52) + red_x(612, y, 30))
                   for i, (s, y) in enumerate([("JULIUS", 560), ("ROME", 760), ("ITALY", 960)]))
    s2 = scene("s2", f'<g transform="translate(-95,330) scale(0.8)">{bust()}</g>{tags}', "WHO INVENTED IT?")

    s3 = scene("s3", f'''
      <clipPath id="mapc"><rect x="100" y="430" width="880" height="720" rx="40"/></clipPath>
      {fill("rect", 'x="100" y="430" width="880" height="720" rx="40"', "#E9D8AE", 30)}
      <g clip-path="url(#mapc)">
        {fill("path", 'd="M60,400 L320,400 Q290,520 330,620 Q370,760 340,860 Q330,980 420,1200 L60,1200 Z"', "#4F86C6", 0, stroke=False)}
        <path d="M320,400 Q290,520 330,620 Q370,760 340,860 Q330,980 420,1200" fill="none" stroke="{INK}" stroke-width="9"/>
        {running("M180,520 Q200,700 190,900", "#A9C8EA", 4)}
      </g>
      <rect x="100" y="430" width="880" height="720" rx="40" fill="none" stroke="{INK}" stroke-width="9"/>
      <path d="M352,760 Q520,730 660,755 Q820,780 980,740" fill="none" stroke="{RED}" stroke-width="8" stroke-dasharray="20 12" stroke-linecap="round"/>
      {text(690, 640, "USA", 90, "#5A4E3A")}
      {text(610, 1010, "MEXICO", 90, "#5A4E3A")}
      {pop("pin", 380, 800, f"""{tag(560, 850, "TIJUANA", 40)}
        {thin(fill("path", 'd="M380,800 Q330,740 330,705 Q330,655 380,655 Q430,655 430,705 Q430,740 380,800 Z"', RED, 60), 7)}
        <circle cx="380" cy="705" r="17" fill="{CREAM}" stroke="{INK}" stroke-width="5"/>""")}
      {pop("year", 880, 1070, thin(fill("circle", 'cx="880" cy="1070" r="75"', GOLD, 60), 8)
           + running("M880,1008 A62,62 0 1 1 879.9,1008", CREAM, 4) + text(880, 1091, "1924", 54))}''', "WHERE?")

    s4 = scene("s4", f'''<g transform="translate(65,250) scale(0.95)">{chef()}</g>
      {pop("name", 540, 1170, tag(540, 1170, "CAESAR CARDINI", 60))}''', "WHO?")

    s5 = scene("s5", f'''
      <g transform="rotate(-6 300 610)">
        {fill("rect", 'x="130" y="420" width="340" height="380" rx="24"', CREAM, 0)}
        {fill("path", 'd="M130,520 L130,444 Q130,420 154,420 L446,420 Q470,420 470,444 L470,520 Z"', RED, 0)}
        {text(300, 495, "JULY", 64, CREAM)}{text(300, 740, "4", 230)}
        <circle cx="210" cy="420" r="13" fill="{INK}"/><circle cx="390" cy="420" r="13" fill="{INK}"/>
      </g>
      {pop("fire", 820, 560, tag(820, 560, "BUSY!", 56, GOLD))}
      <g transform="translate(264,256) scale(0.8)">{bowl(prefix="i")}</g>''', "THE LEGEND")

    s6 = scene("s6", f'''<g transform="translate(-25,326) scale(0.85)">{bust(sad=True)}</g>
      <path id="tear" d="M357,620 Q345,640 357,650 Q369,640 357,620 Z" fill="#6FB3E8" stroke="{INK}" stroke-width="4"/>
      <g id="cr">{crouton(400, 448, 15)}</g>
      {gus(0.5, 875, 1010, id_="g6")}''', "POOR JULIUS")

    s7 = scene("s7", gus(0.95, 500, 870, with_bubble=True, id_="g7"))
    return s1 + s2 + s3 + s4 + s5 + s6 + s7

# ---------- linha do tempo ----------

SCENES = [("s1", 0.0, 4.2), ("s2", 4.2, 9.0), ("s3", 9.0, 15.0), ("s4", 15.0, 19.5),
          ("s5", 19.5, 27.0), ("s6", 27.0, 31.5), ("s7", 31.5, 36.0)]
CAPTIONS = [
    (0.0, 1.6, "Caesar salad"), (1.6, 2.7, "isn't from Italy."), (2.7, 4.2, "Not even close."),
    (4.2, 5.6, "Not Julius."), (5.6, 7.0, "Not Rome."), (7.0, 9.0, "Not even Italy."),
    (9.0, 10.6, "It was invented"), (10.6, 12.4, "in Tijuana, Mexico,"), (12.4, 15.0, "in the 1920s,"),
    (15.0, 17.0, "by an Italian immigrant"), (17.0, 19.5, "named Caesar Cardini."),
    (19.5, 21.2, "Legend says"), (21.2, 23.0, "on a busy Fourth of July,"), (23.0, 24.8, "the kitchen ran low,"),
    (24.8, 25.9, "so he tossed in"), (25.9, 27.0, "what he had."),
    (27.0, 29.0, "Julius Caesar never had"), (29.0, 31.5, "a single crouton."),
    (31.5, 33.3, "Psst..."), (33.3, 36.0, "Follow for more secrets."),
]
HIGHLIGHT = ["Italy.", "Tijuana,", "Mexico,", "Italian", "Cardini.", "Fourth", "July,", "crouton.", "secrets.", "1920s,"]
POPS = {"flag": 2.6, "flagx": 2.9, "t0": 4.3, "t1": 5.7, "t2": 7.1, "pin": 10.6, "year": 12.6, "name": 17.0,
        "fire": 21.3, "g7b": 32.0, "s1h": 0.05, "s2h": 4.25, "s3h": 9.05, "s4h": 15.05, "s5h": 19.55, "s6h": 27.05}
POPS.update({f"i{i}": 24.8 + i * 0.13 for i in range(14)})

JS = """
const clamp = x => Math.max(0, Math.min(1, x));
const outBack = t => { const c = 1.9; return 1 + (c + 1) * Math.pow(t - 1, 3) + c * Math.pow(t - 1, 2); };
const $ = id => document.getElementById(id);
function scaleAround(el, s, extra) {
  const [cx, cy] = el.dataset.c.split(',').map(Number);
  el.setAttribute('transform', `${extra || ''} translate(${cx},${cy}) scale(${s}) translate(${-cx},${-cy})`);
}
function caption(t) {
  const c = CAPTIONS.find(c => t >= c[0] && t < c[1]);
  const el = $('cap');
  if (!c) { el.innerHTML = ''; return; }
  const words = c[2].split(' ');
  const size = c[2].length > 21 ? 70 : 86;
  el.setAttribute('font-size', size);
  if (el.dataset.cur !== c[2]) {
    el.innerHTML = words.map(w => `<tspan fill="${HIGHLIGHT.includes(w) ? '#F5D547' : '#FFFFFF'}">${w} </tspan>`).join('');
    el.dataset.cur = c[2];
  }
  const s = 0.82 + 0.18 * outBack(clamp((t - c[0]) / 0.14));
  $('capg').setAttribute('transform', `translate(540,1395) scale(${s}) translate(-540,-1395)`);
}
function setT(t, frame) {
  $('turb').setAttribute('seed', [7, 11, 19][Math.floor(frame / 2) % 3]);
  for (const [id, a, b] of SCENES) {
    const el = $(id), on = t >= a && t < b;
    el.style.display = on ? '' : 'none';
    if (on) {
      const k = 1.07 - 0.07 * outBack(clamp((t - a) / 0.25)) + 0.035 * (t - a) / (b - a);
      el.setAttribute('transform', `translate(540,900) scale(${k}) translate(-540,-900)`);
    }
  }
  for (const [id, t0] of Object.entries(POPS)) {
    const el = $(id); if (el) scaleAround(el, outBack(clamp((t - t0) / 0.22)));
  }
  // Gus respira / balança
  for (const id of ['g1', 'g6', 'g7']) {
    $(id).setAttribute('transform', `translate(0,${Math.sin(t * 4.2) * 10}) rotate(${Math.sin(t * 2.6) * 3} 500 560)`);
  }
  // lágrima do César
  const tl = ((t - 27.3) % 1.2 + 1.2) % 1.2;
  $('tear').setAttribute('transform', `translate(0,${tl * 120})`);
  $('tear').style.opacity = t > 27.3 ? 1 - tl / 1.2 : 0;
  // croûton cai e quica na base do busto
  const ct = t - 29.2;
  let cy = -700;
  if (ct > 0) { const g = Math.min(ct, 0.45) / 0.45; cy = -700 + 700 * g * g;
    if (ct > 0.45) { const b = (ct - 0.45) / 0.35; cy = b < 1 ? -90 * Math.sin(Math.PI * b) : 0; } }
  $('cr').setAttribute('transform', `translate(0,${cy}) rotate(${ct > 0 ? Math.min(ct, 0.8) * 200 : 0} 400 448)`);
  caption(t);
}
"""

def build():
    base = gb.build("roma")
    defs = base[base.index("<defs>"):base.index("</defs>") + 7]
    defs = defs.replace('<feTurbulence type="fractalNoise" baseFrequency="0.035"',
                        '<feTurbulence id="turb" type="fractalNoise" baseFrequency="0.035"')
    defs = defs.replace('width="1000" height="1000">', f'width="{W}" height="{H}">')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  {defs}
  <rect width="{W}" height="{H}" fill="url(#pique)"/>
  <rect width="{W}" height="{H}" filter="url(#grain)"/>
  {scenes()}
  <rect width="{W}" height="{H}" fill="url(#vig)"/>
  <g id="capg"><text id="cap" style="white-space:pre" word-spacing="10" x="540" y="1420" text-anchor="middle" font-family="{FONT}" font-weight="800"
     font-size="86" stroke="{INK}" stroke-width="16" stroke-linejoin="round" paint-order="stroke"></text></g>
</svg>'''
    data = (f"const SCENES = {json.dumps(SCENES)};\nconst CAPTIONS = {json.dumps(CAPTIONS)};\n"
            f"const HIGHLIGHT = {json.dumps(HIGHLIGHT)};\nconst POPS = {json.dumps(POPS)};\n")
    return f'''<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@800&display=block" rel="stylesheet">
<style>body{{margin:0;background:#000}}</style></head><body>{svg}
<script>{data}{JS}</script></body></html>'''

if __name__ == "__main__":
    print(build())
