"""Recorta as fotos do feed (prints do Instagram) para usar no vídeo.

Os prints são apenas um ponto de partida: para o vídeo final, substitua os
arquivos em assets/fotos/ pelas fotos originais em alta resolução
(mesmos nomes) e renderize novamente.
"""
import sys
from pathlib import Path
from PIL import Image, ImageFilter

S = 1284 / 924  # escala do print (pontos -> pixels)
COLS = [(0, 306), (309, 615), (618, 924)]

# nome: (print, coluna, topo, base[, margem direita]) em pontos;
# o topo é cortado para remover o ícone de vídeo e a margem remove a barra de rolagem
RECORTES = {
    "cabelo-escuro": (1, 1, 500, 842),
    "unhas-rosa": (1, 2, 500, 842),
    "estetica-facial": (1, 0, 905, 1254),
    "cabelo-loiro": (1, 1, 905, 1254),
    "unhas-vermelhas": (1, 2, 905, 1254),
    "massagem-corpo": (1, 1, 1325, 1664),
    "unhas-nude": (1, 2, 1330, 1664, 10),
    "led-facial": (1, 0, 1735, 1999),
    "unhas-pele-negra": (1, 2, 1735, 1999),
    "unhas-anel": (2, 2, 1380, 1706, 10),
}


def main(print1, print2, saida):
    prints = {1: Image.open(print1).convert("RGB"), 2: Image.open(print2).convert("RGB")}
    saida = Path(saida)
    saida.mkdir(parents=True, exist_ok=True)
    for nome, (p, c, top, bot, *margem) in RECORTES.items():
        x0, x1 = COLS[c]
        direita = margem[0] if margem else 2
        box = tuple(round(v * S) for v in (x0 + 2, top, x1 - direita, bot - 2))
        img = prints[p].crop(box)
        w, h = img.size
        img = img.resize((w * 3, h * 3), Image.LANCZOS)
        img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
        img.save(saida / f"{nome}.jpg", quality=92)
        print(nome, img.size)


if __name__ == "__main__":
    main(*sys.argv[1:4])
