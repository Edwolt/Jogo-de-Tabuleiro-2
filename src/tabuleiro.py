from __future__ import annotations

import pygame as pg
from pecas import Promocao

import tipos as tp
from recursos import Recursos
from pecas import Movimento, MovimentoComplexo
from pecas import Roque
from pecas import board_inicial, testar_xeque


# TODO tranformar em uma classe que possa ser passada para peças
class Tabuleiro:
    def __init__(self):
        self.tabuleiro = board_inicial()
        self.vez = True
        self.flags = list()
        self._rei = tp.pb(tp.coord(0, 4), tp.coord(7, 4))

    def movimenta_peca(self, acao: tp.action) -> bool:
        """
        Movimenta a peça se o movimento for validao
        retornando se foi possível ou não

        :param pos: Posição da peça a ser movimentada
        :param nova_pos: Para onde será movimentada
        :return: Se a peça foi movimentada
        """
        (i, j), (m, n) = acao
        peca = self.tabuleiro[i][j]
        if peca is None:
            return False

        mov = peca.get_movimentos_simples(
            self.tabuleiro,
            self.flags,
            # self.rei[self.vez],
            acao.pos
        )[m][n]

        if mov is None:
            return False

        elif isinstance(mov, MovimentoComplexo):
            mov.executar(self.tabuleiro, self.flags)

            match mov:
                case Roque():
                    if self._rei.branco == mov.rei:
                        self._rei.branco = mov.acao_rei.nova_pos
                    elif self._rei.preto == mov.rei:
                        self._rei.preto = mov.acao_rei.nova_pos
                case Promocao():
                    self.promocao = mov

            self.flags.clear()
            mov.atualiza_flags(self.flags)
            return True

        elif isinstance(mov, Movimento):
            mov.executar(self.tabuleiro, self.flags)

            if mov.rei:
                self._rei[self.vez] = acao.nova_pos

            self.flags.clear()
            return True

        return False

    def get_movimentos(self, pos: tp.coord) -> tp.movements | None:
        """
        :return: Retorna um matriz movements com os movimentos legais para peça
        em pos
        Se pos não for uma peça aliada retorna None
        """
        i, j = pos
        peca = self.tabuleiro[i][j]
        if peca is None:
            return None
        elif peca.cor == self.vez:
            return peca.get_movimentos_simples(
                self.tabuleiro,
                self.flags,
                # self.rei[self.vez],
                pos
            )
        else:
            return None

    def _tipo_casa(
        self,
        pos: tp.coord,
        click: tp.coord | None,
        movimento: tp.movements | None
    ) -> str:
        i, j = pos

        if click is not None and pos == click:
            return 'click'

        if movimento is not None and movimento[i][j] is not None:
            mov = movimento[i][j]
            if mov is not None:
                if isinstance(mov, MovimentoComplexo) and mov.especial:
                    return 'especial'
                else:
                    return 'movimento'

        em_xeque = (
            tp.coord(i, j) == self._rei.branco
            or tp.coord(i, j) == self._rei.preto
        ) and testar_xeque(
            self.tabuleiro,
            self.flags,
            tp.coord(i, j)
        )

        if em_xeque:
            return 'xeque'

        return 'vazio'

    def draw(
        self,
        canvas: pg.Surface,
        click: tp.coord | None,
        movimento: tp.movements | None
    ) -> None:
        recursos = Recursos()

        size = canvas.get_size()
        size = size[0] // 8, size[1] // 8

        for y, linha in enumerate(self.tabuleiro):
            for x, peca in enumerate(linha):
                # i, j = y, x

                surf = pg.Surface(size)
                tipo = self._tipo_casa(tp.coord(y, x), click, movimento)
                recursos.config.quadrado(surf, tp.coord(y, x), tipo)

                if peca:
                    peca.draw(surf)

                pos = x * size[0], y * size[1]
                canvas.blit(surf, pos)
