from __future__ import annotations

import tipos as tp

from .abc_peca import Peca
from .util import movements_vazio, calcula_direcao


class Torre(Peca):
    nome: str = "torre"

    def __init__(self, cor: bool, movimentou: bool = False):
        super().__init__(cor)
        self.movimentou = movimentou

    def notifica_movimento(self) -> None:
        self.movimentou = True

    def get_movimentos_simples(
        self, tabuleiro: tp.board, flags: list, pos: tp.coord
    ) -> tp.movements:
        res = movements_vazio()
        DIRECOES = (
            tp.direction(-1, 0),  # Cima
            tp.direction(1, 0),  # Baixo
            tp.direction(0, -1),  # Esquerda
            tp.direction(0, 1),  # Direita
        )
        calcula_direcao(res, tabuleiro, pos, DIRECOES, self.cor)
        return res
