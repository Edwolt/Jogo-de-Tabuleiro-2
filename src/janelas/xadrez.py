from __future__ import annotations

import pygame as pg

import tipos as tp
from recursos import Recursos
from tabuleiro import Tabuleiro

from .abc_janela import Janela
from .menu import Menu
from .escolha import Escolha


class Xadrez(Janela):
    """Toda a lógica do jogo"""

    def __init__(self):
        self.tabuleiro = Tabuleiro()

        self._atualizacao = True
        self._escape = False
        self._promocao = None

        self._click = None
        self._qsize = 0, 0
        self.movimento: tp.movements | None = None

    def atualiza_movimentos(self, pos: tp.coord) -> None:
        self.movimento = self.tabuleiro.get_movimentos(pos)

    ##### Interface #####
    def event(self, event: pg.event.EventType) -> None:
        match event:
            case pg.event.EventType(type=pg.MOUSEBUTTONDOWN, button=1):
                # click esquerdo
                click_antigo = self._click

                self._click = tp.coord(
                    int(event.pos[1] // self._qsize[1]),
                    int(event.pos[0] // self._qsize[0]),
                )

                movimentado = False
                if self.movimento and click_antigo:
                    movimento_oconteceu = self.tabuleiro.movimenta_peca(
                        tp.action(click_antigo, self._click)
                    )
                    if movimento_oconteceu:
                        self.movimento = None
                        movimentado = True

                if not movimentado:
                    self.atualiza_movimentos(self._click)
                else:
                    # TODO isso não deveria ser resposabilidade de xadrez
                    self.tabuleiro.vez = not self.tabuleiro.vez

                self._atualizacao = True
            case pg.event.EventType(type=pg.KEYDOWN, key=pg.K_ESCAPE):
                self._escape = True

    def draw(self, canvas: pg.Surface) -> None:
        if not self._atualizacao:
            return

        size = canvas.get_size()
        self._qsize = size[0] // 8, size[1] // 8

        self.tabuleiro.draw(canvas, self._click, self.movimento)

        self._atualizacao = False
        pg.display.set_caption(Recursos().config.titulo(self.tabuleiro.vez))
        pg.display.flip()

    def new(self):
        if self._escape:
            self._atualizacao = True
            self._escape = False
            return Menu(self)
        elif self._promocao is not None:
            self._atualizacao = True
            promocao = self._promocao
            self._promocao = None
            return Escolha(self, promocao)
        else:
            return self
