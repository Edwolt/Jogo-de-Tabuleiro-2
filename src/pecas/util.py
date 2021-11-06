from copy import copy

from tipos import matriz_tabuleiro, matriz_movimento, direction, coord, mov


##### Tabuleiro #####
def tabuleiro_false() -> matriz_movimento:
    """:return: list 8x8 com todos os campos sendo False"""
    return [[False] * 8 for _ in range(8)]


def tabuleiro_copia(tabuleiro: matriz_tabuleiro) -> matriz_tabuleiro:
    copia = [[None] * 8 for _ in range(8)]  # list 8x8 com None
    for i, linha in enumerate(tabuleiro):
        for j, peca in enumerate(linha):
            if peca is not None:
                copia[i][j] = copy(peca)
    return copia


##### Movimento #####
def mover_peca(tabuleiro: matriz_tabuleiro, movimento: mov) -> None:
    (i, j), (m, n) = movimento
    tabuleiro[m][n] = tabuleiro[i][j]
    tabuleiro[m][n].notifica_movimento()
    tabuleiro[i][j] = None


def valida_coordenadas(a: int, b: int = 0) -> bool:
    """
    valida_coordenada(a):    Verifica se a é um valor válido para componente de uma coordenada
    valida_coordenada(a, b): Verifica se (a, b) é uma coordenada válida
    """

    return 0 <= a < 8 and 0 <= b < 8


def calcula_direcao(res: matriz_movimento, tabuleiro: matriz_tabuleiro, pos: coord, direcoes: tuple[direction, ...], cor: bool) -> None:
    for (di, dj) in direcoes:
        i, j = pos
        i, j = i + di, j + dj
        while valida_coordenadas(i, j):
            if tabuleiro[i][j] is None:
                res[i][j] = True
            else:
                res[i][j] = cor != tabuleiro[i][j].cor
                break  # Se a casa não está vazia, não tem porquê olhar adiante
            i, j = i + di, j + dj
