from __future__ import annotations

from typing import Optional

import tipos as tp

from .abc_peca import Peca
from .abc_movimento import Movimento, MovimentoComplexo
from .xeque import testar_xeque
from .util import movements_vazio, board_copia, mover_peca
from .torre import Torre


class Roque(MovimentoComplexo):
    def __init__(self, acao_rei: tp. action, acao_torre: tp.action):
        """
        :param acao_rei: movimento a ser feito pelo rei
        :param acao_torre: movimento a ser feito pela torre
        """

        self.acao_rei = acao_rei
        self.acao_torre = acao_torre

    def executar(self, tabuleiro: tp.board, flags: list) -> None:
        mover_peca(tabuleiro, self.acao_rei)
        mover_peca(tabuleiro, self.acao_torre)


class Rei(Peca):
    nome = 'rei'

    def __init__(self, cor: bool, movimentou: bool = False):
        super().__init__(cor)
        self.movimentou = movimentou

    def notifica_movimento(self) -> None:
        self.movimentou = True

    def criar_movimento(
        self,
        tabuleiro: tp.board,
        acao: tp.action
    ) -> Optional[Movimento]:
        i, j = acao.nova_pos
        capturada = tabuleiro[i][j]
        if capturada is None or capturada.cor == self.cor:
            return Movimento(acao)
        return None

    def get_movimentos_simples(
        self,
        tabuleiro: tp.board,
        flags: list,
        pos: tp.coord
    ) -> tp.movements:
        # TODO Cuidado com xeque
        res = movements_vazio()
        i, j = pos

        # Posições a verificar
        VERIFICAR = (
            # Casas acima do rei
            tp.coord(i-1, j-1),
            tp.coord(i-1, j),
            tp.coord(i-1, j+1),

            # Casas do meio
            tp.coord(i, j-1),
            tp.coord(i, j+1),

            # Casas abaixo do rei
            tp.coord(i+1, j-1),
            tp.coord(i+1, j),
            tp.coord(i+1, j+1)
        )

        for nova_pos in VERIFICAR:
            if nova_pos.valida():
                m, n = nova_pos
                res[m][n] = self.criar_movimento(
                    tabuleiro,
                    tp.action(pos, nova_pos)
                )

        # Verifica se é possível fazer o Roque
        if not self.movimentou:
            torre = tabuleiro[i][0]
            eh_realmente_torre = (
                torre is not None
                and isinstance(torre, Torre)
                and torre.movimentou
            )
            if eh_realmente_torre:
                # TODO verifica se deixa o rei em xeque ou passa em casas em xeque

                pecas_entre = False
                for jj in range(1, j):
                    pecas_entre = pecas_entre or tabuleiro[i][jj] is not None

                tab = board_copia(tabuleiro)
                tab[i][3] = Rei(self.cor)
                tab[i][4] = None
                xeque = testar_xeque(tab, flags, tp.coord(i, 3))

                if not xeque:
                    tab = board_copia(tabuleiro)
                    tab[i][2] = Rei(self.cor)
                    tab[i][4] = None
                    xeque = testar_xeque(tab, flags, tp.coord(i, 2))

                if not pecas_entre and not xeque:
                    res[i][j-2] = Roque(
                        tp.action(tp.coord(i, j), tp.coord(i, j-2)),
                        tp.action(tp.coord(i, 0), tp.coord(i, j-1))
                    )

            torre = tabuleiro[i][7]
            eh_realmente_torre = (
                torre is not None
                and isinstance(torre, Torre)
                and torre.movimentou
            )
            if eh_realmente_torre:
                pecas_entre = False
                for jj in range(j + 1, 7):
                    pecas_entre = pecas_entre or tabuleiro[i][jj] is not None

                if not pecas_entre:
                    res[i][j+2] = Roque(
                        tp. action(tp.coord(i, j), tp. coord(i, j+2)),
                        tp. action(tp.coord(i, 7), tp.coord(i, j+1))
                    )

        return res
