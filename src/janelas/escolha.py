from __future__ import annotations

import pygame as pg

import tipos as tp
from recursos import Recursos
from pecas import Cavalo, Bispo, Torre, Rainha
from pecas import Promocao

from .abc_janela import Janela
from .menu import Menu


# TODO Não está aparecendo quando deveria acontecer uma promoção
class Escolha(Janela):
    def __init__(self, xadrez, promocao: Promocao):
        """
        Permite o usuário Escolher um peça entre:
        * Cavalo
        * Bispo
        * Torre
        * Rainha
        """
        self.xadrez = xadrez
        self.promocao = promocao
        self.cor = self.promocao.cor
        self.escolhido = None

        self._atualizacao = True
        self._escape = False
        self._qsize = 0, 0

        self.pecas = [
            Cavalo(self.cor),
            Bispo(self.cor),
            Torre(self.cor),
            Rainha(self.cor),
        ]
        for i in self.pecas:
            i.notifica_movimento()

    ##### Interface #####
    def event(self, event: pg.event.EventType) -> None:
        match event:
            case pg.event.EventType(type=pg.MOUSEBUTTONDOWN, button=1):
                # click esquerdo
                i = int(event.pos[1] // self._qsize[1])
                j = int(event.pos[0] // self._qsize[0])
                print(i, j)

                if i == 0 and 0 <= j - 2 < 4:
                    self.escolhido = self.pecas[j - 2]
                    print(self.escolhido)
            case pg.event.EventType(type=pg.KEYDOWN, key=pg.K_ESCAPE):
                self.escape = True

    def draw(self, canvas: pg.Surface) -> None:
        if not self.atualizacao:
            return

        recursos = Recursos()

        size = canvas.get_size()
        self._qsize = size[0] // 8, size[1] // 8

        canvas.fill(pg.Color(0, 0, 0))
        tabuleiro = pg.Surface((6 * self._qsize[0], 6 * self._qsize[1]))
        self.xadrez.draw(tabuleiro)
        canvas.blit(tabuleiro, (self._qsize[0], 2 * self._qsize[1]))

        offset_i, offset_j = 0, 2
        for jj, peca in enumerate(self.pecas):
            # i, j = y, x
            i, j = offset_i, offset_j + jj

            surf = pg.Surface(self._qsize)
            recursos.config.quadrado(surf, tp.coord(j, i), "vazio")
            peca.draw(surf)
            pos = j * self._qsize[0], i * self._qsize[1]
            canvas.blit(surf, pos)

        self.atualizacao = False
        self.xadrez.atualizacao = True
        pg.display.set_caption(recursos.config.titulo(self.cor))
        pg.display.flip()

    def new(self):
        if self.escolhido is not None:
            i, j = self.promocao.promocao
            self.xadrez.tabuleiro[i][j] = self.escolhido
            print(self.escolhido)
            return self.xadrez
        elif self._escape:
            self._escape = False
            self._atualizacao = True
            return Menu(self)
        else:
            return self
