from recursos import Recursos


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


def tabuleiro_novo(recursos: Recursos) -> list:
    """
    :param pecas: objeto da classe Peca
    :return: list 8x8 onde os espacos vazios valem None
    e os espacos com pecas são objetos
    """
    # TODO resolver o problema com imports circulares
    from pecas import Rei, Rainha, Bispo, Cavalo, Torre, Peao

    tabuleiro = tabuleiro_none()

    # Brancas
    tabuleiro[0][0] = Torre(recursos, False)
    tabuleiro[0][1] = Cavalo(recursos, False)
    tabuleiro[0][2] = Bispo(recursos, False)
    tabuleiro[0][3] = Rainha(recursos, False)
    tabuleiro[0][4] = Rei(recursos, False)
    tabuleiro[0][5] = Bispo(recursos, False)
    tabuleiro[0][6] = Cavalo(recursos, False)
    tabuleiro[0][7] = Torre(recursos, False)
    for i in range(8):  # Peões
        tabuleiro[1][i] = Peao(recursos, False)

    # Pretas
    tabuleiro[7][0] = Torre(recursos, True)
    tabuleiro[7][1] = Cavalo(recursos, True)
    tabuleiro[7][2] = Bispo(recursos, True)
    tabuleiro[7][3] = Rainha(recursos, True)
    tabuleiro[7][4] = Rei(recursos, True)
    tabuleiro[7][5] = Bispo(recursos, True)
    tabuleiro[7][6] = Cavalo(recursos, True)
    tabuleiro[7][7] = Torre(recursos, True)
    for i in range(8):  # Peões
        tabuleiro[6][i] = Peao(recursos, True)

    return tabuleiro
