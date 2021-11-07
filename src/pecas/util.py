from __future__ import annotations

from copy import copy

import tipos as tp


##### Tabuleiro #####
def tabuleiro_false() -> tp.movements:
    """:return: list 8x8 com todos os campos sendo False"""
    return [[False] * 8 for _ in range(8)]


def tabuleiro_copia(tabuleiro: tp. board) -> tp.board:
    copia: tp. board = [[None] * 8 for _ in range(8)]  # list 8x8 com None
    for i, linha in enumerate(tabuleiro):
        for j, peca in enumerate(linha):
            if peca is not None:
                copia[i][j] = copy(peca)
    return copia


##### Movimento #####
def mover_peca(tabuleiro: tp.board, movimento: tp.action) -> None:
    (i, j), (m, n) = movimento
    tabuleiro[m][n] = tabuleiro[i][j]
    tabuleiro[m][n].notifica_movimento()
    tabuleiro[i][j] = None


def calcula_direcao(res: tp.movements, tabuleiro: tp. board, pos: tp. coord, direcoes: tuple[tp.direction, ...], cor: bool) -> None:
    for (di, dj) in direcoes:
        i, j = pos
        i, j = i + di, j + dj
        while tp.coord(i, j).valida():
            if tabuleiro[i][j] is None:
                res[i][j] = True
            else:
                res[i][j] = cor != tabuleiro[i][j].cor
                break  # Se a casa não está vazia, não tem porquê olhar adiante
            i, j = i + di, j + dj
