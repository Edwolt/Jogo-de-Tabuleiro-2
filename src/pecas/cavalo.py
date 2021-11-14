from __future__ import annotations

import tipos as tp

from .abc_movimento import Movimento
from .abc_peca import Peca
from .util import movements_vazio


class Cavalo(Peca):
    nome: str = "cavalo"

    def __init__(self, cor: bool):
        super().__init__(cor)

    def _criar_movimento(
        self, tabuleiro: tp.board, acao: tp.action
    ) -> Movimento | None:
        """
        Retorna o Movimento usando acao se for valido
        Senão retorna None
        """
        i, j = acao.nova_pos
        capturada = tabuleiro[i][j]
        if capturada is None or capturada.cor != self.cor:
            return Movimento(acao)
        return None

    def get_movimentos_simples(
        self, tabuleiro: tp.board, flags: list, pos: tp.coord
    ) -> tp.movements:
        res = movements_vazio()
        i, j = pos

        # Direções a verificar
        DIRECOES = (
            # Casas acima
            tp.direction(-2, -1),
            tp.direction(-2, 1),
            # Casas abaixo
            tp.direction(2, -1),
            tp.direction(2, 1),
            # Casas a esquerda
            tp.direction(-1, -2),
            tp.direction(1, -2),
            # Casas a direita
            tp.direction(-1, 2),
            tp.direction(1, 2),
        )

        for direcao in DIRECOES:
            nova_pos = pos + direcao
            if nova_pos.valida():
                m, n = nova_pos
                res[m][n] = self._criar_movimento(
                    tabuleiro, tp.action(pos, nova_pos)
                )

        return res
