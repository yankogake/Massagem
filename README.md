# Harmonie — vídeo de divulgação

Vídeo vertical (1080×1920, 30 fps, 20 s, com som) para Reels/Stories/TikTok do
**Harmonie ✨ Estética & Beleza** — Rua Maranhão, 2270, Praia Azul, Americana-SP.

Resultado: [`harmonie-divulgacao.mp4`](harmonie-divulgacao.mp4)

## Roteiro (tudo no tempo da música, 120 BPM)

| Tempo | Cena | Som |
|---|---|---|
| 0–2 s | **Gancho**: fotos em fusão suave + "Americana, anota esse *endereço.*" | batida abafada + riser |
| 2–4 s | Logo **harmonie** com clarão suave | impacto (drop) + brilho |
| 4–11,5 s | 5 serviços, um a cada 3 batidas, com barra de progresso | whoosh em cada corte |
| 11,5–14 s | Grade com 9 fotos: "Tudo em *um só lugar.*" | pop a cada foto |
| 14–20 s | Chamada: "*Agende* seu horário", endereço, @, WhatsApp, "Envie pra quem merece esse cuidado." | pausa + riser → impacto, sino no logo |

Por que funciona melhor nas redes:
- **gancho nos 2 primeiros segundos** (fotos em fusão + frase direta) para segurar quem está rolando o feed;
- **trocas de cena no tempo da música**, com movimentos suaves (sem pulsar), que dão ritmo sem cansar;
- **pedido de compartilhamento** no final ("Envie pra quem merece…"), que gera envios por DM;
- textos dentro da **área segura do Reels** (não ficam atrás da legenda nem dos botões);
- áudio normalizado em **-14 LUFS**, o padrão das redes sociais.

A trilha é **original**, sintetizada em `tools/trilha.py` (sem samples), então não
tem risco de bloqueio por direitos autorais.

## Editar e renderizar

- `video.html` — animação. Abra no navegador para pré-visualizar (sem som).
  Textos, serviços, tempos e efeitos sonoros (`SOM`) ficam no topo do `<script>`.
- `tools/trilha.py` — música e efeitos sonoros, gerados a partir de `SOM`.
- `assets/fotos/` — fotos usadas. Foram recortadas dos prints do feed
  (`tools/recortar_fotos.py`), então têm baixa resolução: **troque pelos
  arquivos originais com os mesmos nomes** para um vídeo bem mais nítido.
- Renderizar o MP4 (precisa de `ffmpeg`, Chromium e Python com numpy/scipy):

```bash
npm install
pip install -r requirements.txt
npm run render          # gera harmonie-divulgacao.mp4
```

## Dicas para postar

- Legenda curta com pergunta + CTA, ex.: *"Qual desses você faria primeiro? 💅💆‍♀️ Agende pelo link da bio."*
- Hashtags locais: `#americanasp #salaodebelezaamericana #esteticaamericana #unhasamericana`.
- Marque a localização (Praia Azul, Americana) e poste entre 18h e 21h.
- Use o mesmo vídeo nos Stories com o adesivo de link para o agendamento.
