from __future__ import annotations

import tipos as tp

from .abc_peca import Peca
from .util import movements_vazio, calcula_direcao


class Rainha(Peca):
    nome = "rainha"

    def __init__(self, cor: bool):
        super().__init__(cor)

    def get_movimentos_simples(
        self, tabuleiro: tp.board, flags: list, pos: tp.coord
    ) -> tp.movements:
        res = movements_vazio()
        direcoes = (
            tp.direction(-1, 0),  # Cima
            tp.direction(1, 0),  # Baixo
            tp.direction(0, -1),  # Esquerda
            tp.direction(0, 1),  # Direita
            tp.direction(-1, 1),  # Cima Direita
            tp.direction(-1, -1),  # Cima Esquerda
            tp.direction(1, 1),  # Baixo Direita
            tp.direction(1, -1),  # Baixo Esquerda
        )
        calcula_direcao(res, tabuleiro, pos, direcoes, self.cor)
        return res
