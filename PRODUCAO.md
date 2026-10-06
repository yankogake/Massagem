# Canal do Gus: guia de produção

**Conceito:** Gus, um pombo de rua de Nova York que viaja o mundo e conta os segredos que "ouviu dos telhados".
**Público:** EUA (narração em inglês). **Estilo:** tudo bordado (satin stitch, pesponto, fundo de piquê), animado a 12 fps com "tremor" de linha.

## Estrutura do repositório

| Pasta | Conteúdo |
|---|---|
| `personagem/` | Gus em sticker e bordado (`gerar_bordado.py` gera as variantes de chapéu: `roma`, `paris`) |
| `roteiros/` | Roteiros dos episódios (narração em inglês + cenas em português) |
| `animacao/` | Teste de abertura de Short (`gerar_short_teste.py` + `render_frames.js`) |

Para gerar o teste de Short:
```bash
cd animacao
python3 gerar_short_teste.py > short_teste.svg
NODE_PATH=$(npm root -g) node render_frames.js short_teste.svg frames 96
ffmpeg -framerate 12 -i frames/f%03d.png -vf "fps=30,format=yuv420p" -c:v libx264 -crf 18 gus_short_teste_rome.mp4
```

## Fluxo de um episódio

1. **Roteiro:** 12 curiosidades em escala crescente, do gancho ao #1 mais chocante, com o gancho do próximo episódio no final. Conferir cada fato na lista de checagem do roteiro.
2. **Voz:** ElevenLabs (ou similar). Uma voz fixa para o Gus: grave, levemente rouca, sotaque de Nova York, ritmo de fofoca. Sempre o mesmo preset, para manter a consistência entre episódios.
3. **Cenas:** uma imagem por bloco de 5 a 10 segundos (~60 a 80 por episódio). Usar o prompt base abaixo com Midjourney, Ideogram, Leonardo ou similar, e o PNG do Gus como referência de personagem.
4. **Animação:**
   - Parallax e zoom lento nas cenas.
   - O Gus entra por cima (PNG recortado) com movimento simples: pulo, inclinação, asa.
   - "Tremor" de linha: alternar 2 ou 3 versões levemente diferentes da mesma imagem a cada 2 quadros (12 fps).
5. **Edição:** CapCut ou DaVinci Resolve. Legendas sempre ativas, com fonte arredondada e pesada (Baloo 2). Trilha leve, tipo "jazz de rua", e efeitos de agulha e tecido nas transições.
6. **Shorts:** cortar de 6 a 8 Shorts de cada episódio, com o gancho falado nos primeiros 2 segundos.
7. **Thumbnail:** o Gus grande com a expressão da fofoca e o chapéu da cidade, mais um elemento "proibido" do tema, e 3 palavras no máximo.

## Prompt base para as cenas (manter fixo)

```
[DESCRIÇÃO DA CENA], embroidered patch art, satin stitch embroidery, visible thread texture,
running stitch outlines, sewn onto cream cotton piqué fabric, flat colors, slight 3D thread relief,
soft studio light, cute cartoon style, no text
```

Exemplo: `the Pantheon dome seen from below with rain falling through the oculus, embroidered patch art, ...`

## Paleta de linhas

| Uso | Cor |
|---|---|
| Contorno | `#262A36` |
| Gus (corpo / cabeça) | `#9EA8BB` / `#A5AFC1` |
| Colar | `#1FA88F` `#2F7FC8` `#8550BF` |
| Destaque (balão / títulos) | `#F5D547` / `#E9B83F` |
| Vermelho (boina / pesponto) | `#C8323F` |
| Tecido | `#F4F1E9` |

## Calendário inicial sugerido

| Semana | Longo | Shorts |
|---|---|---|
| 1 | EP01 Rome | 4 |
| 2 | EP02 Paris (catacumbas como #1) | 4 |
| 3 | EP03 New York (a "casa" do Gus) | 4 |
| 4 | EP04 London | 4 |
