from pecas import Pecas


def tabuleiro_none() -> list:
    """
    :return: list 8x8 com todos os campos sendo None
    """

    return [[None] * 8 for _ in range(8)]


def tabuleiro_false() -> list:
    """
    :return: list 8x8 com todos os campos sendo False
    """

    return [[False] * 8 for _ in range(8)]


def tabuleiro_novo(pecas: Pecas) -> list:
    """
    :return: list 8x8 onde os espacos vazios valem None
    e os espacos com pecas são objetos
    """

    tabuleiro = tabuleiro_none()

    # Brancos
    tabuleiro[0][0] = pecas.Torre(False)
    tabuleiro[0][1] = pecas.Cavalo(False)
    tabuleiro[0][2] = pecas.Bispo(False)
    tabuleiro[0][3] = pecas.Rainha(False)
    tabuleiro[0][4] = pecas.Rei(False)
    tabuleiro[0][5] = pecas.Bispo(False)
    tabuleiro[0][6] = pecas.Cavalo(False)
    tabuleiro[0][7] = pecas.Torre(False)
    for i in range(8):  # Peões brancos
        tabuleiro[1][i] = pecas.Peao(False)

    # Pretos
    tabuleiro[7][0] = pecas.Torre(True)
    tabuleiro[7][1] = pecas.Cavalo(True)
    tabuleiro[7][2] = pecas.Bispo(True)
    tabuleiro[7][3] = pecas.Rainha(True)
    tabuleiro[7][4] = pecas.Rei(True)
    tabuleiro[7][5] = pecas.Bispo(True)
    tabuleiro[7][6] = pecas.Cavalo(True)
    tabuleiro[7][7] = pecas.Torre(True)
    for i in range(8):  # Peões pretos
        tabuleiro[6][i] = pecas.Peao(True)

    return tabuleiro
