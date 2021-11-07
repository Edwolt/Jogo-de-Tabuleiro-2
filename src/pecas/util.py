from copy import copy

from tipos import board, movements, direction, coord, action


##### Tabuleiro #####
def tabuleiro_false() -> movements:
    """:return: list 8x8 com todos os campos sendo False"""
    return [[False] * 8 for _ in range(8)]


def tabuleiro_copia(tabuleiro: board) -> board:
    copia: board = [[None] * 8 for _ in range(8)]  # list 8x8 com None
    for i, linha in enumerate(tabuleiro):
        for j, peca in enumerate(linha):
            if peca is not None:
                copia[i][j] = copy(peca)
    return copia


##### Movimento #####
def mover_peca(tabuleiro: board, movimento: action) -> None:
    (i, j), (m, n) = movimento
    tabuleiro[m][n] = tabuleiro[i][j]
    tabuleiro[m][n].notifica_movimento()
    tabuleiro[i][j] = None


def calcula_direcao(res: movements, tabuleiro: board, pos: coord, direcoes: tuple[direction, ...], cor: bool) -> None:
    for (di, dj) in direcoes:
        i, j = pos
        i, j = i + di, j + dj
        while coord(i, j).valida:
            if tabuleiro[i][j] is None:
                res[i][j] = True
            else:
                res[i][j] = cor != tabuleiro[i][j].cor
                break  # Se a casa não está vazia, não tem porquê olhar adiante
            i, j = i + di, j + dj
