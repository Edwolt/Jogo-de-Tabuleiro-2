from __future__ import annotations

from copy import copy

import tipos as tp

from .abc_movimento import Movimento


##### Tabuleiro #####
def movements_vazio() -> tp.movements:
    """:return: matriz movements com todos os valores None"""
    return tp.movements([[None] * 8 for _ in range(8)])


def board_vazio() -> tp.board:
    """:return: matriz board com todos os valores None"""
    return tp.board([[None]*8 for _ in range(8)])


def board_inicial() -> tp.board:
    """
    Um tabuleiro com as peças na posição inicial
    :param pecas: objeto da classe Peca
    :return: matriz board onde os espacos vazios valem None
    e os espacos com pecas são objetos
    """

    from .rei import Rei
    from .rainha import Rainha
    from .torre import Torre
    from .bispo import Bispo
    from .cavalo import Cavalo
    from .peao import Peao

    tabuleiro = board_vazio()

    # Pretas
    tabuleiro[0][0] = Torre(False)
    tabuleiro[0][1] = Cavalo(False)
    tabuleiro[0][2] = Bispo(False)
    tabuleiro[0][3] = Rainha(False)
    tabuleiro[0][4] = Rei(False)
    tabuleiro[0][5] = Bispo(False)
    tabuleiro[0][6] = Cavalo(False)
    tabuleiro[0][7] = Torre(False)
    for i in range(8):  # Peões
        tabuleiro[1][i] = Peao(False)

    # Brancas
    tabuleiro[7][0] = Torre(True)
    tabuleiro[7][1] = Cavalo(True)
    tabuleiro[7][2] = Bispo(True)
    tabuleiro[7][3] = Rainha(True)
    tabuleiro[7][4] = Rei(True)
    tabuleiro[7][5] = Bispo(True)
    tabuleiro[7][6] = Cavalo(True)
    tabuleiro[7][7] = Torre(True)
    for i in range(8):  # Peões
        tabuleiro[6][i] = Peao(True)

    return tabuleiro


def board_copia(tabuleiro: tp. board) -> tp.board:
    copia = board_vazio()
    for i, linha in enumerate(tabuleiro):
        for j, peca in enumerate(linha):
            if peca is not None:
                copia[i][j] = copy(peca)
    return copia


##### Movimento #####
def mover_peca(tabuleiro: tp.board, movimento: tp.action) -> None:
    (i, j), (m, n) = movimento
    tabuleiro[m][n] = tabuleiro[i][j]
    tabuleiro[i][j] = None

    peca = tabuleiro[m][n]
    peca is None or peca.notifica_movimento()


def calcula_direcao(
        res: tp.movements,
        tabuleiro: tp.board,
        pos: tp.coord,
        direcoes: tuple[tp.direction, ...],
        cor: bool,
        rei: bool = False
) -> None:
    for di, dj in direcoes:
        i, j = pos
        i, j = i + di, j + dj
        while tp.coord(i, j).valida():
            peca = tabuleiro[i][j]
            if peca is None:
                res[i][j] = Movimento(tp.action(pos, tp.coord(i, j)), rei)
            else:
                if cor != peca.cor:
                    res[i][j] = Movimento(tp.action(pos, tp.coord(i, j)), rei)
                break  # Se a casa não está vazia, não tem porquê olhar adiante
            i, j = i + di, j + dj
