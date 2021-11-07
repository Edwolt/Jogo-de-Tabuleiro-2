from __future__ import annotations

import tipos as tp

from .abc_peca import Peca
from .util import tabuleiro_false


class Cavalo(Peca):
    def __init__(self, cor: bool):
        super().__init__(cor, nome='cavalo')

    def valida_posicao(self, tabuleiro: tp.board, pos: tp.coord) -> bool:
        i, j = pos
        return tabuleiro[i][j] is None or tabuleiro[i][j].cor != self.cor

    def get_movimentos_simples(self, tabuleiro: tp.board, flags: list, pos: tp.coord) -> tp.movements:
        res = tabuleiro_false()
        i, j = pos

        # Casas acima
        if tp.coord(i-2, j-1).valida():
            res[i-2][j-1] = self.valida_posicao(tabuleiro, tp.coord(i-2, j-1))
        if tp.coord(i-2, j+1).valida():
            res[i-2][j+1] = self.valida_posicao(tabuleiro, tp.coord(i-2, j+1))

        # Casas abaixo
        if tp.coord(i+2, j-1).valida():
            res[i+2][j-1] = self.valida_posicao(tabuleiro, tp.coord(i+2, j-1))
        if tp.coord(i+2, j+1).valida():
            res[i+2][j+1] = self.valida_posicao(tabuleiro, tp.coord(i+2, j+1))

        # Casas a esquerda
        if tp.coord(i-1, j-2).valida():
            res[i-1][j-2] = self.valida_posicao(tabuleiro, tp.coord(i-1, j-2))
        if tp.coord(i+1, j-2).valida():
            res[i+1][j-2] = self.valida_posicao(tabuleiro, tp.coord(i+1, j-2))

        # Casas a direira
        if tp.coord(i-1, j+2).valida():
            res[i-1][j+2] = self.valida_posicao(tabuleiro, tp.coord(i-1, j+2))
        if tp.coord(i+1, j+2).valida():
            res[i+1][j+2] = self.valida_posicao(tabuleiro, tp.coord(i+1, j+2))

        return res
