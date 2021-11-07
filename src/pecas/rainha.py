from __future__ import annotations

import tipos as tp

from .abc_peca import Peca
from .util import tabuleiro_false, calcula_direcao


class Rainha(Peca):
    def __init__(self, cor: bool):
        super().__init__(cor, nome='rainha')

    def get_movimentos_simples(self, tabuleiro: tp.board, flags: list, pos: tp.coord) -> tp.movements:
        res = tabuleiro_false()
        direcoes = (
            tp.direction(-1, 0),   # Cima
            tp.direction(1, 0),    # Baixo
            tp.direction(0, -1),   # Esquerda
            tp.direction(0, 1),    # Direita
            tp.direction(-1, 1),   # Cima Direita
            tp.direction(-1, -1),  # Cima Esquerda
            tp.direction(1, 1),    # Baixo Direita
            tp.direction(1, -1),   # Baixo Esquerda
        )
        calcula_direcao(res, tabuleiro, pos, direcoes, self.cor)
        return res
