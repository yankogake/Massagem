# Harmonie — vídeo de divulgação

Vídeo vertical (1080×1920, 30 fps, 20,5 s) para Reels/Stories/TikTok do
**Harmonie ✨ Estética & Beleza** — Rua Maranhão, 2270, Praia Azul, Americana-SP.

Resultado: [`harmonie-divulgacao.mp4`](harmonie-divulgacao.mp4)

## Roteiro

| Tempo | Cena |
|---|---|
| 0–2,6 s | Logo **harmonie** + "Estética & Beleza" |
| 2,6–4,6 s | "Um novo *conceito* de beleza." |
| 4,6–13,6 s | 5 serviços em sequência: Nails · Cabelos · Estética · Massagem · Pele |
| 13,6–16,6 s | Grade com 9 fotos: "Tudo em *um só lugar.*" |
| 16,6–20,5 s | Chamada: "*Agende* seu horário", endereço, @harmonie.americana, WhatsApp |

Estilo: fundo creme, tipografia serifada fina (Cormorant Garamond) + Jost,
cortes rápidos com revelações em máscara.

## Editar e renderizar

- `video.html` — animação. Abra no navegador para pré-visualizar em loop.
  Textos, serviços e tempos ficam no topo do `<script>` (`SERVICOS`, `GRADE`, `C1`…`C5`).
- `assets/fotos/` — fotos usadas. Foram recortadas dos prints do feed
  (`tools/recortar_fotos.py`), então têm baixa resolução: **troque pelos
  arquivos originais com os mesmos nomes** para um vídeo bem mais nítido.
- Renderizar o MP4 (precisa de `ffmpeg` e Chromium):

```bash
npm install
npm run render          # gera harmonie-divulgacao.mp4
```

O vídeo sai sem áudio de propósito: no Instagram, adicione uma música em alta
na hora de postar (ajuda no alcance).
