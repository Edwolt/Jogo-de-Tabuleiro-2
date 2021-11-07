from __future__ import annotations

import pygame as pg
from typing import Optional

import tipos as tp
from recursos import Recursos
from tabuleiro import Tabuleiro

from .abc_janela import Janela
from .menu import Menu
from .escolha import Escolha


class Xadrez(Janela):
    """Toda a lógica do jogo"""

    def __init__(self):
        self.atualizacao = True
        self.tabuleiro = Tabuleiro()
        self.escape = False
        self.promocao = None
        self.flags = list()

        self.click = None
        self.movimento: Optional[tp.movements] = None
        self.qsize = 0, 0

    def atualiza_movimentos(self, pos: tp.coord) -> None:
        self.movimento = self.tabuleiro.get_movimentos(pos)

    ##### Interface #####
    def event(self, event: pg.event.Event) -> None:
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # click esquerdo
            click_antigo = self.click

            self.click = tp.coord(
                int(event.pos[1] // self.qsize[1]),
                int(event.pos[0] // self.qsize[0])
            )

            movimentado = False
            if self.movimento and click_antigo:
                if self.tabuleiro.movimenta_peca(click_antigo, self.click, self.movimento):
                    self.movimento = None
                    movimentado = True

            if not movimentado:
                self.atualiza_movimentos(self.click)
            else:
                self.vez = not self.vez

            self.atualizacao = True

        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.escape = True

    def draw(self, canvas: pg.Surface) -> None:
        if not self.atualizacao:
            return

        size = canvas.get_size()
        self.qsize = size[0] // 8, size[1] // 8

        self.tabuleiro.draw(canvas, self.click, self.movimento)

        self.atualizacao = False
        pg.display.set_caption(Recursos().config.titulo(self.vez))
        pg.display.flip()

    def new(self):
        if self.escape:
            self.atualizacao = True
            self.escape = False
            return Menu(self)
        elif self.promocao is not None:
            self.atualizacao = True
            promocao = self.promocao
            self.promocao = None
            return Escolha(self, promocao)
        else:
            return self
