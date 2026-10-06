"""Gera o Bartô como bordado em tecido piquê (estilo logo bordado de camisa polo)."""
import math, sys

INK = "#262A36"   # linha do contorno
SW = 9

def sat(angle):
    return f"url(#sat{angle})"

def fill(tag, attrs, color, angle, stroke=True, extra=""):
    """Forma com cor sólida + camada de ponto cheio (satin) na direção `angle`."""
    st = f'stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"' if stroke else ""
    return (f'<{tag} {attrs} fill="{color}" {st} {extra}/>'
            f'<{tag} {attrs} fill="{sat(angle)}" {extra}/>')

def line(d, color, w, angle, extra=""):
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" {extra}/>'
            f'<path d="{d}" fill="none" stroke="{sat(angle)}" stroke-width="{w}" stroke-linecap="round" {extra}/>')

def running(d, color="#F6F2E8", w=4):
    """Ponto corrido (pesponto) decorativo."""
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-dasharray="11 8" stroke-linecap="round" opacity="0.9"/>'

def laurel():
    s = []
    cx, cy, r = 500, 268, 160
    for side in (-1, 1):
        for i in range(7):
            a = math.radians(200 + i * 19) if side < 0 else math.radians(340 - i * 19)
            x, y = cx + r * math.cos(a), cy + r * math.sin(a) * 0.5
            rot = math.degrees(a) + (90 if side < 0 else -90) + side * 35
            c = "#5FAE4A" if i % 2 else "#3F8F36"
            s.append(fill("ellipse", f'cx="{x:.1f}" cy="{y:.1f}" rx="17" ry="35"', c, 90,
                          extra=f'transform="rotate({rot:.1f} {x:.1f} {y:.1f})"').replace(f'stroke-width="{SW}"', 'stroke-width="6"'))
    s.append(fill("circle", 'cx="500" cy="190" r="14"', "#E9B83F", 30).replace(f'stroke-width="{SW}"', 'stroke-width="6"'))
    return "".join(s)

def beret():
    g = fill("path", 'd="M360,250 Q370,160 500,150 Q650,150 655,245 Q600,275 500,272 Q400,272 360,250 Z"', "#C8323F", 20)
    g += running("M378,244 Q440,262 500,262 Q590,262 638,238")
    g += line("M492,150 q4,-26 18,-30", INK, 10, 0)
    return f'<g transform="translate(0,-28) rotate(-10 500 220)">{g}</g>'

def eye(cx, cy, l1, l2, cid):
    return f'''
    <clipPath id="{cid}"><circle cx="{cx}" cy="{cy}" r="50"/></clipPath>
    {fill("circle", f'cx="{cx}" cy="{cy}" r="50"', "#FBF8F1", 0, stroke=False)}
    <g clip-path="url(#{cid})">
      {fill("circle", f'cx="{cx+14}" cy="{cy+8}" r="34"', "#F07F1E", 70, stroke=False)}
      {fill("circle", f'cx="{cx+18}" cy="{cy+10}" r="17"', "#191B22", 20, stroke=False)}
      <circle cx="{cx+26}" cy="{cy+2}" r="7" fill="#FFFFFF"/>
      {fill("polygon", f'points="{cx-60},{cy-70} {cx+60},{cy-70} {cx+60},{l2} {cx-60},{l1}"', "#97A1B5", 0, stroke=False)}
      <line x1="{cx-60}" y1="{l1}" x2="{cx+60}" y2="{l2}" stroke="{INK}" stroke-width="8"/>
    </g>
    <circle cx="{cx}" cy="{cy}" r="50" fill="none" stroke="{INK}" stroke-width="{SW}"/>'''

def pigeon(hat):
    feet = "M430,820 L430,880 M430,880 L395,905 M430,880 L432,915 M430,880 L468,905 " \
           "M575,820 L575,880 M575,880 L540,905 M575,880 L577,915 M575,880 L613,905"
    strap = "M655,470 Q520,620 360,760"
    return f'''
    {line(feet, INK, 32, 0)}{line(feet, "#E26D74", 17, 0)}
    <!-- corpo -->
    {fill("ellipse", 'cx="500" cy="640" rx="235" ry="215"', "#9EA8BB", 75)}
    {fill("ellipse", 'cx="510" cy="690" rx="150" ry="140"', "#C7CEDA", 105, stroke=False)}
    {running("M392,610 Q420,560 510,552 Q630,560 652,680")}
    <!-- asa com as duas faixas -->
    {fill("path", 'd="M290,520 Q215,620 250,760 Q300,800 345,770 Q370,650 340,540 Z"', "#87919F", 100)}
    {line("M262,640 Q300,650 352,628", INK, 15, 0)}{line("M258,690 Q302,700 355,680", INK, 15, 0)}
    <!-- colar furta-cor: 3 faixas de linha -->
    <clipPath id="neckc"><ellipse cx="500" cy="470" rx="190" ry="85"/></clipPath>
    <g clip-path="url(#neckc)">
      {fill("rect", 'x="300" y="380" width="140" height="180"', "#1FA88F", 60, stroke=False)}
      {fill("rect", 'x="440" y="380" width="120" height="180"', "#2F7FC8", 90, stroke=False)}
      {fill("rect", 'x="560" y="380" width="140" height="180"', "#8550BF", 120, stroke=False)}
    </g>
    <ellipse cx="500" cy="470" rx="190" ry="85" fill="none" stroke="{INK}" stroke-width="{SW}"/>
    <!-- alça e bolsa -->
    {line(strap, INK, 34, 0)}{line(strap, "#86552A", 20, 45)}
    {running(strap, "#E7C48D", 3)}
    <g transform="rotate(-10 360 790)">
      <g transform="rotate(-18 338 750)">
        {fill("rect", 'x="318" y="690" width="40" height="120" rx="18"', "#EFE3C4", 0).replace(f'stroke-width="{SW}"', 'stroke-width="7"')}
        {line("M300,722 L322,730", "#C8323F", 10, 0)}
      </g>
      {fill("rect", 'x="270" y="740" width="190" height="135" rx="26"', "#C17E3C", 0)}
      {fill("path", 'd="M270,770 Q270,740 296,740 L434,740 Q460,740 460,770 L460,800 Q365,830 270,800 Z"', "#9D6229", 90)}
      {running("M285,770 Q285,755 300,755 L430,755 Q445,755 445,770 L445,790 Q365,812 285,790 Z", "#E7C48D", 3)}
      {running("M285,815 L285,860 L445,860 L445,815", "#E7C48D", 3)}
      {fill("circle", 'cx="365" cy="812" r="11"', "#E9B83F", 0).replace(f'stroke-width="{SW}"', 'stroke-width="5"')}
      <!-- broche de estrela -->
      {fill("circle", 'cx="310" cy="840" r="19"', "#2B4A9A", 0).replace(f'stroke-width="{SW}"', 'stroke-width="5"')}
      <polygon points="310,826 314,836 325,837 317,844 319,855 310,849 301,855 303,844 295,837 306,836" fill="#F6F2E8"/>
      {fill("path", 'd="M418,836 q-12,-14 -20,0 q-6,12 20,26 q26,-14 20,-26 q-8,-14 -20,0 Z"', "#C8323F", 0).replace(f'stroke-width="{SW}"', 'stroke-width="5"')}
    </g>
    <!-- cabeça -->
    {fill("path", 'd="M478,188 Q455,130 488,110 Q482,150 505,182 Z"', "#A5AFC1", 80).replace(f'stroke-width="{SW}"', 'stroke-width="7"')}
    {fill("path", 'd="M505,184 Q520,120 560,118 Q530,150 528,190 Z"', "#A5AFC1", 110).replace(f'stroke-width="{SW}"', 'stroke-width="7"')}
    {fill("circle", 'cx="500" cy="340" r="160"', "#A5AFC1", 60)}
    {running("M368,300 Q380,215 470,190")}
    {laurel() if hat == "roma" else beret()}
    <ellipse cx="392" cy="402" rx="30" ry="17" fill="#E98494" opacity="0.7"/>
    <ellipse cx="612" cy="402" rx="30" ry="17" fill="#E98494" opacity="0.7"/>
    {eye(440, 330, 318, 300, "eL")}
    {eye(565, 330, 296, 312, "eR")}
    {line("M392,262 Q440,252 482,266", INK, 14, 0)}
    {line("M522,236 Q565,206 612,236", INK, 14, 0)}
    <!-- bico -->
    {fill("path", 'd="M474,392 Q502,380 528,392 L508,440 Q501,450 494,440 Z"', "#363B47", 90).replace(f'stroke-width="{SW}"', 'stroke-width="7"')}
    {fill("ellipse", 'cx="501" cy="388" rx="22" ry="12"', "#F3F1EC", 0).replace(f'stroke-width="{SW}"', 'stroke-width="6"')}
    <!-- asa cochichando -->
    {fill("path", 'd="M700,560 Q760,470 720,380 Q700,345 668,352 Q640,360 650,392 Q640,388 628,400 Q615,418 632,436 Q612,446 620,470 Q632,500 690,510 Z"', "#87919F", 70)}
    {running("M690,520 Q735,460 712,395")}
    '''

def bubble():
    return f'''<g transform="rotate(8 830 200)">
    {fill("path", 'd="M700,140 Q700,95 745,95 L905,95 Q950,95 950,140 L950,215 Q950,260 905,260 L800,260 L760,300 L765,260 L745,260 Q700,260 700,215 Z"', "#F5D547", 0)}
    {running("M722,140 Q722,117 745,117 L905,117 Q928,117 928,140 L928,215 Q928,238 905,238 L745,238 Q722,238 722,215 Z", "#FFF6C4", 3)}
    <text x="825" y="202" text-anchor="middle" font-family="'Baloo 2','DejaVu Sans',sans-serif"
          font-weight="800" font-size="70" fill="{INK}">psst...</text>
    <text x="825" y="202" text-anchor="middle" font-family="'Baloo 2','DejaVu Sans',sans-serif"
          font-weight="800" font-size="70" fill="url(#sat100)">psst...</text></g>'''

def build(hat="roma"):
    pats = "".join(
        f'<pattern id="sat{a}" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate({a})">'
        f'<rect x="0" y="0" width="2.2" height="6" fill="#000" fill-opacity="0.20"/>'
        f'<rect x="3" y="0" width="1.4" height="6" fill="#fff" fill-opacity="0.22"/></pattern>'
        for a in (0, 20, 30, 45, 60, 70, 75, 80, 90, 100, 105, 110, 120))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    {pats}
    <pattern id="pique" width="12" height="20" patternUnits="userSpaceOnUse">
      <rect width="12" height="20" fill="#E4DFD3"/>
      <rect x="1" y="1" width="10" height="8" rx="4" fill="#F4F1E9"/>
      <rect x="-5" y="11" width="10" height="8" rx="4" fill="#F4F1E9"/>
      <rect x="7" y="11" width="10" height="8" rx="4" fill="#F4F1E9"/>
    </pattern>
    <radialGradient id="vig" cx="0.45" cy="0.4" r="0.8">
      <stop offset="0.5" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.28"/>
    </radialGradient>
    <filter id="grain" filterUnits="userSpaceOnUse" x="0" y="0" width="1000" height="1000"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="3"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.3  0 0 0 0 0.28  0 0 0 0 0.25  0 0 0 0.35 0"/></filter>
    <filter id="emb" x="-5%" y="-5%" width="110%" height="115%" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="7" result="t"/>
      <feDisplacementMap in="SourceGraphic" in2="t" scale="4" result="src"/>
      <feColorMatrix in="src" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0.3 0.59 0.11 0 0" result="lum"/>
      <feGaussianBlur in="src" stdDeviation="5" result="pb"/>
      <feColorMatrix in="pb" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0" result="puff"/>
      <feComposite in="puff" in2="lum" operator="arithmetic" k2="0.8" k3="0.45" result="h"/>
      <feDiffuseLighting in="h" surfaceScale="5" diffuseConstant="1.15" result="dl">
        <feDistantLight azimuth="225" elevation="50"/></feDiffuseLighting>
      <feSpecularLighting in="h" surfaceScale="5" specularConstant="0.55" specularExponent="18" result="sl">
        <feDistantLight azimuth="225" elevation="50"/></feSpecularLighting>
      <feBlend in="src" in2="dl" mode="multiply" result="m"/>
      <feComposite in="sl" in2="src" operator="in" result="slc"/>
      <feComposite in="m" in2="slc" operator="arithmetic" k2="1" k3="0.6" result="lit"/>
      <feComposite in="lit" in2="src" operator="in" result="final"/>
      <feGaussianBlur in="src" stdDeviation="3" result="sb"/>
      <feOffset in="sb" dx="3" dy="5" result="so"/>
      <feColorMatrix in="so" type="matrix" values="0 0 0 0 0.1  0 0 0 0 0.08  0 0 0 0 0.05  0 0 0 0.45 0" result="shadow"/>
      <feMerge><feMergeNode in="shadow"/><feMergeNode in="final"/></feMerge>
    </filter>
  </defs>
  <rect width="1000" height="1000" fill="url(#pique)"/>
  <rect width="1000" height="1000" filter="url(#grain)"/>
  <g filter="url(#emb)">{pigeon(hat)}</g>
  <g filter="url(#emb)">{bubble()}</g>
  <rect width="1000" height="1000" fill="url(#vig)"/>
</svg>'''

if __name__ == "__main__":
    print(build(sys.argv[1] if len(sys.argv) > 1 else "roma"))
