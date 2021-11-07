from __future__ import annotations

import pygame as pg
from typing import Optional
from pecas.peao import Promocao


import tipos as tp
from recursos import Recursos
from pecas import Movimento, MovimentoComplexo
from pecas import Roque
from pecas import board_inicial, testar_xeque


class Tabuleiro:
    def __init__(self):
        self.tabuleiro = board_inicial()
        self.vez = True
        self.flags = list()
        self.rei = tp.pb(tp.coord(0, 4), tp.coord(7, 4))

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

            if isinstance(mov, Roque):
                if self.rei.branco == mov.rei:
                    self.rei.branco = mov.acao_rei.nova_pos
                elif self.rei.preto == mov.rei:
                    self.rei.preto = mov.acao_rei.nova_pos
            elif isinstance(mov, Promocao):
                self.promocao = mov

            self.flags.clear()
            mov.atualiza_flags(self.flags)
            return True

        elif isinstance(mov, Movimento):
            mov.executar(self.tabuleiro, self.flags)

            if mov.rei:
                self.rei[self.vez] = acao.nova_pos

            self.flags.clear()
            return True

        return False

    def get_movimentos(self, pos: tp.coord) -> Optional[tp.movements]:
        """

        :param pos: [description]
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

    def draw(self, canvas: pg.Surface, click: Optional[tp.coord], movimento: Optional[tp.movements]) -> None:

        recursos = Recursos()

        size = canvas.get_size()
        size = size[0] // 8, size[1] // 8

        for y, linha in enumerate(self.tabuleiro):
            for x, peca in enumerate(linha):
                # i, j = y, x

                tipo = 'vazio'
                if click and tp.coord(y, x) == click:
                    tipo = 'click'
                elif movimento is not None and movimento[y][x]:
                    mov = movimento[y][x]
                    if isinstance(mov, MovimentoComplexo) and mov.especial:
                        tipo = 'especial'
                    else:
                        tipo = 'movimento'
                elif (
                    (
                        tp.coord(y, x) == self.rei.branco
                        or tp.coord(y, x) == self.rei.preto
                    )
                    and testar_xeque(
                        self.tabuleiro,
                        self.flags,
                        tp.coord(y, x)
                    )
                ):
                    tipo = 'xeque'

                surf = pg.Surface(size)
                recursos.config.quadrado(surf, tp.coord(x, y), tipo)

                if peca:
                    peca.draw(surf)

                pos = x * size[0], y * size[1]
                canvas.blit(surf, pos)
