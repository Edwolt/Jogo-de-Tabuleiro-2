from copy import copy


##### Tabuleiro #####
def tabuleiro_false() -> list[list[bool]]:
    """:return: list 8x8 com todos os campos sendo False"""
    return [[False] * 8 for _ in range(8)]


def tabuleiro_copia(tabuleiro) -> list[list]:
    copia = [[None] * 8 for _ in range(8)]  # list 8x8 com None
    for i, linha in enumerate(tabuleiro):
        for j, peca in enumerate(linha):
            if peca is not None:
                copia[i][j] = copy(peca)
    return copia


##### Movimento #####
def mover_peca(tabuleiro: list[list], pos: tuple[int, int], nova_pos: tuple[int, int]) -> None:
    i, j = pos
    m, n = nova_pos
    tabuleiro[m][n] = tabuleiro[i][j]
    tabuleiro[m][n].notifica_movimento()
    tabuleiro[i][j] = None


def valida_coordenadas(a: int, b: int = 0) -> bool:
    """
    valida_coordenada(a):    Verifica se a é um valor válido para componente de uma coordenada
    valida_coordenada(a, b): Verifica se (a, b) é uma coordenada válida
    """

    return 0 <= a < 8 and 0 <= b < 8


def calcula_direcao(res: list[list], tabuleiro: list[list], pos: tuple[int, int], direcoes: tuple[tuple[int, int], ...], cor: bool) -> None:
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
