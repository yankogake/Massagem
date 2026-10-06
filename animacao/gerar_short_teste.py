"""Gera o SVG base do teste de abertura de Short (1080x1920) com o Gus bordado.
Os elementos animados têm ids (gus, bub, rev, needle, tag, turb) que o render_frames.js altera quadro a quadro."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "personagem"))
import gerar_bordado as gb

W, H = 1080, 1920

def build():
    base = gb.build("roma")
    defs = base[base.index("<defs>"):base.index("</defs>") + 7]
    defs = defs.replace('<feTurbulence type="fractalNoise" baseFrequency="0.035"',
                        '<feTurbulence id="turb" type="fractalNoise" baseFrequency="0.035"')
    defs = defs.replace('width="1000" height="1000">', f'width="{W}" height="{H}">')
    title = f'''
    <clipPath id="revc"><rect id="rev" x="0" y="0" width="0" height="{H}"/></clipPath>
    <g clip-path="url(#revc)" filter="url(#emb)">
      <text x="540" y="380" text-anchor="middle" font-family="'Baloo 2',sans-serif" font-weight="800"
            font-size="250" fill="#E9B83F" stroke="{gb.INK}" stroke-width="12" paint-order="stroke">ROME</text>
      <text x="540" y="380" text-anchor="middle" font-family="'Baloo 2',sans-serif" font-weight="800"
            font-size="250" fill="url(#sat80)">ROME</text>
      <path d="M180,420 L900,420" stroke="#C8323F" stroke-width="6" stroke-dasharray="16 10" stroke-linecap="round"/>
    </g>
    <g id="needle"><path d="M0,0 L-70,0" stroke="#C8323F" stroke-width="3"/>
      <path d="M0,-6 L90,0 L0,6 Z" fill="#C9CED6" stroke="{gb.INK}" stroke-width="3"/>
      <ellipse cx="14" cy="0" rx="7" ry="2.5" fill="#4A4F5C"/></g>'''
    tag = f'''<g id="tag"><g filter="url(#emb)">
      <rect x="110" y="1660" width="860" height="150" rx="40" fill="#F3EBD8" stroke="{gb.INK}" stroke-width="10"/>
      <rect x="110" y="1660" width="860" height="150" rx="40" fill="url(#sat0)"/>
      <rect x="135" y="1685" width="810" height="100" rx="26" fill="none" stroke="#C8323F" stroke-width="4" stroke-dasharray="11 8"/>
      <text x="540" y="1760" text-anchor="middle" font-family="'Baloo 2',sans-serif" font-weight="800"
            font-size="60" fill="{gb.INK}">12 SECRETS TOURISTS MISS</text></g></g>'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  {defs}
  <rect width="{W}" height="{H}" fill="url(#pique)"/>
  <rect width="{W}" height="{H}" filter="url(#grain)"/>
  {title}
  <g id="gus"><g filter="url(#emb)">{gb.pigeon("roma")}</g>
    <g id="bub" filter="url(#emb)">{gb.bubble()}</g></g>
  {tag}
  <rect width="{W}" height="{H}" fill="url(#vig)"/>
</svg>'''

if __name__ == "__main__":
    print(build())
